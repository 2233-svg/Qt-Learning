# Qt QReadLocker：读锁的作用域管理

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QReadLocker>`  
> 所属模块：`Qt6::Core`  
> 类型性质：非模板 RAII 读锁管理器  
> 相关类型：`QReadWriteLock`、`QWriteLocker`

## 1. 它解决什么问题

`QReadWriteLock` 允许多个读者并发读取共享数据，同时让写入者独占访问。`QReadLocker` 为其中的“读侧临界区”提供作用域管理：

```cpp
QReadWriteLock lock;
QByteArray data;

QByteArray snapshot() const
{
    QReadLocker locker(&lock);
    return data;
} // 自动释放读锁
```

它把构造时的 `lockForRead()` 和离开作用域时的 `unlock()` 绑定起来，适合有多个返回路径的查询函数，也能减少遗漏解锁的风险。

## 2. 它不是什么

`QReadLocker` 不是：

- `QReadWriteLock` 本身；
- 数据的快照或副本；
- 读写锁的所有权容器；
- 带超时的读锁获取器；
- 把读锁升级为写锁的工具；
- 自动延长 `QReadWriteLock` 生命周期的智能指针。

它只借用传入的 `QReadWriteLock *`。锁对象必须在 locker 的整个生命周期内有效，locker 析构不会销毁它。

## 3. 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QReadLocker>
```

## 4. 最小可用代码

```cpp
#include <QReadLocker>
#include <QReadWriteLock>
#include <QString>

class SettingsCache
{
public:
    QString value() const
    {
        QReadLocker locker(&lock);
        return currentValue;
    }

    void setValue(const QString &value)
    {
        QWriteLocker locker(&lock);
        currentValue = value;
    }

private:
    mutable QReadWriteLock lock;
    QString currentValue;
};
```

读函数复制出快照后就可以在锁外使用，避免把后续慢操作继续放在读锁内。

## 5. 核心使用模型

### 5.1 构造时立即取得读锁

```cpp
QReadLocker locker(&lock);
```

构造函数保存指针，然后调用 `relock()`；对非空锁指针，`relock()` 调用 `lockForRead()`。如果写者当前持有锁，构造过程可能阻塞。

因此构造点就是同步等待点。不要在已经持有其他锁时随意构造 `QReadLocker`，除非项目定义了明确一致的锁顺序。

### 5.2 析构时释放读锁

```cpp
bool contains(const QString &key) const
{
    QReadLocker locker(&lock);
    if (!index.contains(key))
        return false;
    return true;
}
```

无论函数从哪个分支返回，locker 析构都会调用 `unlock()`。`QReadLocker` 不拥有 `QReadWriteLock`，所以析构只改变锁状态，不释放锁对象内存。

### 5.3 `nullptr` 表示不激活

```cpp
QReadLocker<QReadWriteLock> locker(nullptr); // 错误：QReadLocker 不是模板
```

正确形式是：

```cpp
QReadLocker locker(nullptr);
Q_ASSERT(locker.readWriteLock() == nullptr);
```

空指针会形成未激活的 locker：构造、`unlock()`、`relock()` 和析构都不会访问锁对象。它可以表达“可选锁”场景，但不代表任何数据已经受到保护；对空 locker 调用 `relock()` 也不会自动关联新锁。

## 6. 读锁和写锁的边界

### 6.1 多个读者可以并发

多个线程可以同时持有同一 `QReadWriteLock` 的读锁，前提是它们都只读共享数据。`QReadLocker` 不会复制数据，也不会阻止其他读者。

### 6.2 写者需要独占

`QWriteLocker` 持有写锁时，其他读者和写者都必须等待。读锁释放后，等待中的写者才可能继续。

### 6.3 读锁不能直接升级为写锁

下面的意图不能通过 `QReadLocker` 自动完成：

```cpp
QReadLocker readLocker(&lock);
// 发现需要修改，直接再取得写锁
```

这可能导致自我阻塞或死锁。应先释放读锁、重新检查条件，再按明确顺序获取写锁；如果必须原子地完成检查和修改，应重新设计临界区。

### 6.4 不要把读锁当作不可变性证明

读锁只表示遵守同一把 `QReadWriteLock` 的线程之间形成了同步关系。它不能阻止没有使用该锁的代码写入数据，也不能保护通过外部别名暴露出去的可变对象。

## 7. 手动暂停和恢复

### 7.1 `unlock()` 是安全的提前释放

```cpp
QReadLocker locker(&lock);
const QByteArray result = data;
locker.unlock();

emitReady(result);
```

`unlock()` 检查内部状态：只有当前处于激活状态时才调用底层 `QReadWriteLock::unlock()`。因此重复 `unlock()` 不会再次解锁同一把锁。

调用后：

- locker 不再持有读锁；
- `readWriteLock()` 仍返回原来的锁指针；
- 析构时不会重复释放；
- 后续访问共享数据不再受此 locker 保护。

### 7.2 `relock()` 会重新阻塞

```cpp
locker.unlock();
// 锁外进行不依赖共享状态的工作
locker.relock();
```

对非空锁指针且当前未激活时，`relock()` 调用 `lockForRead()`，可能阻塞；重新取得成功后才恢复激活状态。对已经激活的 locker 调用 `relock()` 不会再次加锁。

`relock()` 没有超时参数，也没有 `bool` 返回值。需要超时读锁时，应直接调用 `QReadWriteLock::tryLockForRead(...)`，而不是构造 `QReadLocker` 后再尝试取消等待。

## 8. 生命周期、不可复制和内部表示

### 8.1 锁对象必须覆盖 locker 生命周期

```cpp
// 错误：返回后 localLock 已销毁
QReadLocker badLocker()
{
    QReadWriteLock localLock;
    return QReadLocker(&localLock);
}
```

返回的 locker 保存悬空指针，后续析构或操作都是未定义行为。应让调用方拥有锁对象，或者只在锁对象仍然有效的作用域内创建 locker。

### 8.2 不可复制，也不可移动

Qt 6.11.1 头文件对 `QReadLocker` 使用 `Q_DISABLE_COPY`，没有移动构造或移动赋值。原因是一个 locker 对应一份明确的解锁责任，复制或隐式转移都会让责任边界不清晰。

因此不要把它放进需要复制或移动元素的容器，也不要从函数返回一个引用局部锁的 locker。

### 8.3 低位标志是实现细节

实现内部把锁指针和一个激活标志压在同一个整数中，最低位表示当前是否已经取得读锁。构造时会断言锁指针满足对齐要求。应用代码不应读取或构造这种内部表示，只通过公开 API 管理状态。

## 9. 并发和死锁边界

### 9.1 临界区保持短小

读锁内适合读取和复制共享状态，不适合执行网络请求、磁盘 I/O、用户回调或长时间计算。复制快照后尽快释放锁，通常更容易控制等待时间。

### 9.2 读锁内等待写者相关事件

如果读锁内等待某个任务完成，而该任务需要取得同一把写锁才能完成，就会形成死锁。RAII 只能保证最终释放，不能打破这种等待依赖。

### 9.3 统一锁顺序

同时使用多把锁时，所有线程都必须遵守同一顺序。`QReadLocker` 和 `QWriteLocker` 只是把底层加锁动作包装起来，不会替调用方推导或验证锁顺序。

### 9.4 保护规则必须统一

如果一部分代码使用 `QReadLocker`，另一部分代码直接写共享数据，读写锁就没有形成完整的保护协议。应明确哪些字段由哪一把锁保护，并让所有访问路径遵守同一规则。

## 10. 逐项 API 语义

### 10.1 `QReadLocker(QReadWriteLock *readWriteLock)`

```cpp
QReadLocker(QReadWriteLock *readWriteLock);
```

- 保存传入的锁指针；
- 对非空指针立即取得读锁；
- 可能阻塞；
- 传入 `nullptr` 时创建未激活 locker；
- 不拥有锁对象；
- 不提供超时和失败返回值。

### 10.2 `~QReadLocker()`

```cpp
~QReadLocker();
```

调用 `unlock()`。如果 locker 已激活，则释放读锁；如果是空 locker 或已经手动解锁，则不再访问底层锁。

### 10.3 `unlock()`

```cpp
void unlock();
```

释放当前持有的读锁并标记为未激活。对未激活状态调用不会重复解锁。它不会清空 `readWriteLock()` 返回的指针。

### 10.4 `relock()`

```cpp
void relock();
```

当 locker 关联非空锁且当前未激活时，再次调用 `lockForRead()`；成功后恢复激活。对已激活或空 locker 不执行加锁。

### 10.5 `readWriteLock() const`

```cpp
QReadWriteLock *readWriteLock() const;
```

返回关联的 `QReadWriteLock *`。手动 `unlock()` 后仍返回原指针；空 locker 返回 `nullptr`。返回值不转移所有权，也不表示当前一定持有读锁。

## 11. 实际使用模式

### 11.1 读取并复制快照

```cpp
QVector<Row> Model::rows() const
{
    QReadLocker locker(&lock);
    return rowsData;
}
```

返回值复制或共享快照后，locker 析构释放读锁。调用方不需要持有内部锁。

### 11.2 读锁内只做快速判断

```cpp
bool Cache::contains(const QString &key) const
{
    QReadLocker locker(&lock);
    return values.contains(key);
}
```

### 11.3 需要超时时使用底层锁 API

```cpp
if (!lock.tryLockForRead(50))
    return false;

const auto snapshot = data;
lock.unlock();
useSnapshot(snapshot);
return true;
```

这段代码必须保证每条成功路径都调用 `unlock()`；如果控制流复杂，应该重新组织作用域或使用项目已有的超时 RAII 封装。

## 12. 常见错误

### 12.1 以为 locker 保存的是数据副本

locker 只保存锁指针和状态，不保存被保护的数据。解锁后，之前读取的引用或指针仍可能因其他线程写入而失效。

### 12.2 读锁内直接返回内部引用

```cpp
// 风险：返回后读锁已释放，引用可能立即失去同步保护
const QString &name() const;
```

优先返回值或共享快照；如果接口必须返回引用，就必须另行设计对象生命周期和同步协议。

### 12.3 直接把读锁升级为写锁

读锁持有期间再申请写锁，可能等待自己释放读锁。应先结束读侧作用域，再重新检查并取得写锁。

### 12.4 忘记空指针只表示“未激活”

`QReadLocker(nullptr)` 不会保护任何数据，也不会在之后自动连接到某个锁。可选锁场景需要由调用方确保未激活路径的数据访问本身是安全的。

### 12.5 在锁内调用外部代码

信号发射、插件回调和用户提供的函数都可能重入当前对象或等待其他锁。通常应先复制必要数据，再在锁外调用。

## API 速查表
| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QReadLocker(QReadWriteLock *)` | 构造并立即取得读锁 | 可能阻塞；`nullptr` 创建未激活 locker；不拥有锁对象 |
| `~QReadLocker()` | 自动释放当前读锁 | 对未激活状态不重复解锁；依赖锁对象仍有效 |
| `unlock()` | 提前释放读锁 | 解锁后共享数据不再受此 locker 保护；指针仍保留 |
| `relock()` | 重新取得读锁 | 可能阻塞；无超时和返回值；空 locker 不会关联新锁 |
| `readWriteLock()` | 返回关联的锁指针 | 不表示当前一定持有读锁，不转移所有权 |

## 14. 一句话总结

`QReadLocker` 是 `QReadWriteLock` 的读侧 RAII 包装：构造时取得读锁，析构时释放；它只借用锁对象、不可复制移动、不提供超时，并且不能把已有读锁直接升级成写锁。实际使用应尽快复制快照、缩短读锁范围，并让所有访问路径遵守同一把锁的保护协议。
