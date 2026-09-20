# Qt QWriteLocker 深入笔记：写锁 RAII 与独占提交

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QWriteLocker>`  
> 所属模块：`Qt6::Core`  
> 配套类：`QReadWriteLock`、`QReadLocker`  
> 定位：在作用域内自动取得和释放 QReadWriteLock 的写锁

`QWriteLocker` 是 QReadWriteLock 的写模式 RAII 包装器。构造时调用 `lockForWrite()`，析构时释放写锁。写锁取得期间没有其他读者或写者可以进入受保护临界区，因此适合提交共享状态、更新容器和维护跨字段不变量。

## 1. CMake 与最小可用代码

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QReadWriteLock>
#include <QWriteLocker>
#include <QHash>

class UserCache
{
public:
    void put(int id, QString name)
    {
        QWriteLocker locker(&m_lock);
        m_names.insert(id, std::move(name));
        ++m_version;
    }

private:
    QReadWriteLock m_lock;
    QHash<int, QString> m_names;
    quint64 m_version = 0;
};
```

返回、异常和提前退出都会先析构 `locker`，因此不需要在每个分支手动调用 `unlock()`。

## 2. 写锁的职责：维护完整不变量

写锁不只是“让某个容器不能同时写”。它应包住必须作为一个原子观察单位的全部字段：

```cpp
QWriteLocker locker(&m_lock);
if (amount > m_available)
    return false;

m_available -= amount;
m_reserved += amount;
m_lastOperation = operation;
return true;
```

其他线程只能看到写锁释放后的完整状态，不能观察中间的 `m_available` 已减少但 `m_reserved` 尚未增加的时刻。

如果只更新一个独立原子整数，可以使用 `std::atomic`；但多个字段、容器结构和“检查后再修改”通常需要同一把写锁。

## 3. 构造和析构

```cpp
QWriteLocker locker(&m_lock);
```

构造可能阻塞，直到现有读者和写者离开。传入 `nullptr` 时不执行任何操作：

```cpp
QWriteLocker optionalLocker(enabled ? &m_lock : nullptr);
```

底层 `QReadWriteLock` 必须比 locker 活得久。不要让 locker 保存已经离开作用域的锁指针，也不要在仍有后台访问时先析构底层锁。

写锁的释放必须发生在所有对共享状态的访问完成之后。若需要把耗时工作移到锁外，应先复制输入/版本，再在重新加锁后重新验证。

## 4. 为什么 RAII 比手工 `lockForWrite()`/`unlock()` 安全

手工代码在多个 return 分支和异常路径中容易漏解锁：

```cpp
m_lock.lockForWrite();
if (!validate())
    return false; // 错误：没有 unlock
m_lock.unlock();
```

RAII 版本：

```cpp
QWriteLocker locker(&m_lock);
if (!validate())
    return false;
commit();
return true;
```

异常也会正确释放：

```cpp
void Store::replace(Data data)
{
    QWriteLocker locker(&m_lock);
    validateOrThrow(data);
    m_data = std::move(data);
}
```

RAII 只负责锁的生命周期，不会自动回滚已经写入一半的业务状态。需要异常安全时，先在锁外构造新对象，或在锁内使用事务式临时状态，最后一次性提交。

## 5. `unlock()` 与 `relock()`

```cpp
QWriteLocker locker(&m_lock);
Prepared update = prepareOutsideLock(); // 示例中此调用不应实际发生在锁内
```

更合理的写法是先锁外准备，再锁内提交：

```cpp
Prepared update = prepareOutsideLock();

QWriteLocker locker(&m_lock);
if (m_version != update.baseVersion)
    return false;
applyLocked(update);
```

必须在持锁状态中临时释放时：

```cpp
QWriteLocker locker(&m_lock);
Snapshot snapshot = copyStateLocked();

locker.unlock();
Result result = slowCalculation(snapshot);

locker.relock();
if (m_version != snapshot.version)
    return false; // 释放期间状态发生了变化
commitLocked(std::move(result));
```

`unlock()` 后其他读者和写者都可进入；`relock()` 重新取得的是未来某一时刻的写锁，不保证仍是原来的状态。优先用花括号缩小作用域，只有确实要复用同一个 locker 或需要把它传给条件等待时才使用手工 unlock/relock。

对已解锁 locker 再调用 `unlock()` 或对仍持锁 locker 调用 `relock()` 都是错误的状态操作。

## 6. `readWriteLock()`

```cpp
QReadWriteLock *lock = locker.readWriteLock();
```

它返回构造时传入的底层锁指针，不转移所有权，也不改变锁状态。通常只用于需要原始锁指针的底层辅助代码。

```cpp
void updateWithHelper(QWriteLocker &locker)
{
    QReadWriteLock *lock = locker.readWriteLock();
    Q_ASSERT(lock != nullptr);
    helperThatExpectsLock(lock);
}
```

辅助函数必须明确调用者已经持有写锁，避免它再次 `lockForWrite()` 形成递归需求或死锁。

## 7. 写锁与读锁的关系

写锁期间：

- 后来的读者等待；
- 后来的写者等待；
- 之前已经取得的读锁必须先释放；
- 只有写锁释放后所有等待者才可能继续。

QReadWriteLock 会优先处理等待中的写者，防止新读者无限挤压写者。但这意味着写锁争用高时，后来的读操作也会出现尾部延迟。

不要在持有读锁时构造 QWriteLocker：QReadWriteLock 不支持原子读写升级，即使锁采用 Recursive 模式也不能改变锁类型。

## 8. 写锁不是事务和回滚机制

```cpp
QWriteLocker locker(&m_lock);
m_a = newA;
mayThrow();
m_b = newB;
```

如果 `mayThrow()` 抛出，锁会释放，但 `m_a` 已修改而 `m_b` 未修改，业务不变量仍可能破坏。应先构造完整新状态：

```cpp
State next = makeNextState(currentInput); // 锁外，可抛异常

QWriteLocker locker(&m_lock);
m_state = std::move(next);                // 一次提交
```

或者在锁内使用临时副本，验证无误后交换。QWriteLocker 只提供互斥，不提供数据库式 commit/rollback。

## 9. 写锁内的回调和信号

不要默认在写锁内发出信号或调用外部回调：连接可能是 direct，槽可能同步回入并再次取锁，或取得另一把锁形成等待环。

推荐：

```cpp
Snapshot snapshot;
{
    QWriteLocker locker(&m_lock);
    updateLocked();
    snapshot = makeSnapshotLocked();
}

emit changed(snapshot); // 锁已释放
```

如果必须在锁内调用回调，必须把它视为锁协议的一部分，记录允许的重入、锁顺序和异常行为，而不是依赖 QWriteLocker 自动解决。

## 10. 写锁中的耗时控制

写临界区通常应只包含：

- 校验版本和关键前置条件；
- 修改共享容器；
- 更新关联计数和索引；
- 复制通知所需的快照。

不应包含：

- 网络请求、磁盘 I/O；
- `sleep()`；
- 等待其他线程完成；
- 大规模排序或压缩；
- 用户代码回调。

可把这些工作放在锁外，锁内只做短暂的版本检查和提交。若必须分阶段提交，使用显式状态机，让其他读者看到每个状态都是合法的。

## 11. 常见错误

### 错误 1：在构造前手动加锁

```cpp
m_lock.lockForWrite();
QWriteLocker locker(&m_lock); // 再次加锁，非递归模式会死锁
```

让 locker 从头负责加锁，或使用明确的 adopt-lock 方案；QWriteLocker 本身没有 adopt 构造。

### 错误 2：直接操作底层锁解锁

```cpp
QWriteLocker locker(&m_lock);
m_lock.unlock(); // locker 仍认为自己持锁，析构会再次 unlock
```

必须调用 `locker.unlock()`，同步包装器的内部状态。

### 错误 3：把写锁当作升级锁

持有 QReadLocker 时再创建 QWriteLocker 会死锁。释放读锁、取得写锁、重新检查条件。

### 错误 4：锁释放后继续使用旧迭代器

其他写者可能改变容器并使迭代器失效。只把值快照带出锁。

### 错误 5：认为析构会回滚

locker 只解锁，不撤销业务写入。异常安全必须由状态构造和提交策略保证。

### 错误 6：底层锁生命周期不足

QWriteLocker 保存原始指针；锁先析构会使 locker 析构时访问悬空地址。

## API 速查表
`QWriteLocker` 表达的是独占修改期，而不是事务系统。查表时要区分“锁住时维护不变量”“暂时释放锁后重新验证状态”和“析构自动解锁”这三件事，避免把它误解为自动回滚。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QWriteLocker(QReadWriteLock *lock)` | 构造时对 `QReadWriteLock` 取得写锁。 | 可能阻塞到所有读者和写者离开；传 `nullptr` 时无操作。 |
| 析构 | `~QWriteLocker()` | 析构时释放当前持有的写锁。 | 底层锁必须仍存活；析构只解锁，不会回滚已经写入的业务状态。 |
| 提前释放 | `unlock()` | 在作用域结束前释放写锁。 | 释放后其他读者/写者都可能进入；不要继续使用内部引用或迭代器。 |
| 重新加锁 | `relock()` | 再次以写模式取得同一把锁。 | 空窗期状态可能变化，必须重新验证版本、条件和迭代器有效性。 |
| 底层指针 | `readWriteLock()` | 返回构造时关联的 `QReadWriteLock *`。 | 不转移所有权；辅助函数若使用它，应明确调用者已持有写锁。 |
| 写提交 | 与 `QReadWriteLock::lockForWrite()` 配合 | 用 RAII 管理独占修改期。 | 适合维护跨字段不变量；异常安全和回滚需要业务自己设计。 |
| 取舍 | 与 `QReadLocker` 对比 | `QWriteLocker` 阻塞所有读者和写者，`QReadLocker` 允许并发读。 | 不支持从读锁原子升级到写锁；释放读锁再写锁后必须重新检查条件。 |

## 13. 总结

1. QWriteLocker 是 QReadWriteLock 写模式的 RAII 包装器。
2. 写锁保证读写完全独占，适合一次性维护多个字段的不变量。
3. 构造可能阻塞，析构释放；底层锁必须覆盖 locker 的完整生命周期。
4. `unlock()`/`relock()` 之间状态可能变化，重新加锁后必须重新验证版本和条件。
5. 写锁不会自动提供事务回滚；异常安全需要先构造新状态再一次提交。
6. 不支持从读锁原子升级到写锁，也不应在锁内调用未知回调。
7. 需要通知时通常复制快照、释放写锁后再发信号。
8. `readWriteLock()` 只提供底层指针，不改变所有权。
9. QWriteLocker 没有 adopt-lock 或超时构造，相关需求应使用底层 tryLock 和明确的 scope guard。
10. 写锁临界区越短，读者等待越少，系统尾延迟越可控。
