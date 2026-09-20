# Qt QWriteLocker：写锁的作用域管理

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QWriteLocker>`  
> 所属模块：`Qt6::Core`  
> 类型性质：非模板 RAII 写锁管理器  
> 相关类型：`QReadWriteLock`、`QReadLocker`

## 1. 它解决什么问题

`QWriteLocker` 把 `QReadWriteLock` 的独占写入阶段包装成一个作用域对象：

```cpp
QReadWriteLock lock;
QByteArray data;

void replaceData(const QByteArray &newData)
{
    QWriteLocker locker(&lock);
    data = newData;
} // 自动释放写锁
```

构造时取得写锁，离开作用域时释放写锁。这样即使函数中途 `return`，也不会因为遗漏 `unlock()` 而长期阻塞读者和其他写者。

## 2. 它不是什么

`QWriteLocker` 不是：

- `QReadWriteLock` 本身；
- 被写入数据的副本；
- 锁对象的所有权容器；
- 带超时的写锁获取器；
- 读锁升级工具；
- 自动解决并发冲突或死锁的机制。

它只借用传入的 `QReadWriteLock *`。锁对象必须在 locker 的整个生命周期内有效，locker 析构不会销毁它。

## 3. 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QWriteLocker>
```

## 4. 最小可用代码

```cpp
#include <QReadWriteLock>
#include <QWriteLocker>
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

写函数只在修改共享状态的最小范围内持有写锁。校验、格式化等不依赖共享状态的慢操作可以先在锁外完成。

## 5. 核心使用模型

### 5.1 构造时立即取得写锁

```cpp
QWriteLocker locker(&lock);
```

构造函数保存指针，然后调用 `relock()`；对非空锁指针，`relock()` 调用 `lockForWrite()`。如果有读者或其他写者，构造过程可能阻塞。

写锁是独占锁：取得成功后，其他线程不能通过同一把 `QReadWriteLock` 取得读锁或写锁。

### 5.2 析构时释放写锁

```cpp
bool updateIfChanged(const QByteArray &newData)
{
    QWriteLocker locker(&lock);
    if (data == newData)
        return false;

    data = newData;
    return true;
}
```

两个返回路径都会经过析构函数。`QWriteLocker` 不拥有底层锁对象，析构只释放当前写锁，不会删除 `QReadWriteLock`。

### 5.3 `nullptr` 表示未激活

```cpp
QWriteLocker locker(nullptr);
Q_ASSERT(locker.readWriteLock() == nullptr);
```

空指针不会触发锁操作。`unlock()`、`relock()` 和析构也不会访问底层对象，因此形成未激活 locker。它不保护任何数据，也不会在之后自动关联新的锁。

## 6. 写锁与读锁的边界

### 6.1 写锁排斥所有同锁读写者

写锁持有期间：

- 新的 `QReadLocker` 会等待；
- 新的 `QWriteLocker` 会等待；
- 直接调用同一把锁的读写获取函数也会等待；
- 只有释放写锁后，等待者才可能继续。

这种独占性适合修改容器结构、替换共享对象、更新多个相互依赖的字段等操作。

### 6.2 不要在写锁内执行慢任务

网络、磁盘、用户回调、等待线程和长时间计算都会让所有读者停顿。通常先在锁外生成候选结果，再在写锁内快速提交：

```cpp
const QByteArray prepared = buildDataOutsideLock();
{
    QWriteLocker locker(&lock);
    data = prepared;
}
```

### 6.3 不要在写锁内再次取得同一把锁

非递归 `QReadWriteLock` 不允许把写锁当成可重入锁。写锁内再次创建 `QReadLocker` 或 `QWriteLocker`，可能导致自我阻塞。即使锁配置为递归模式，也不应把递归当作无条件安全的设计替代品。

### 6.4 写锁不是事务回滚

`QWriteLocker` 只管理同步，不记录旧值，也不会在异常或提前返回时回滚已经写入的部分状态。需要原子提交或回滚时，先在锁外准备副本，再在锁内一次性替换。

## 7. 手动暂停和恢复

### 7.1 `unlock()`：提前提交并释放

```cpp
QWriteLocker locker(&lock);
applySmallChange();
locker.unlock();

notifyOutsideLock();
```

`unlock()` 只有在内部标记为已激活时才调用底层 `unlock()`。重复调用不会再次解锁同一把锁。

调用后：

- locker 不再持有写锁；
- `readWriteLock()` 仍返回原来的锁指针；
- 析构时不会重复释放；
- 后续共享状态访问不再受这个 locker 保护。

### 7.2 `relock()`：重新取得写锁

```cpp
locker.unlock();
// 锁外完成不依赖共享状态的工作
locker.relock();
```

对非空锁指针且当前未激活时，`relock()` 调用 `lockForWrite()`，可能再次阻塞。已经激活的 locker 调用 `relock()` 不会重复加锁。

`relock()` 没有超时参数和失败返回值。需要超时写锁时，应使用 `QReadWriteLock::tryLockForWrite(...)`。

## 8. 生命周期、不可复制和内部表示

### 8.1 锁对象必须先于 locker 销毁

```cpp
// 错误：返回后 localLock 已销毁
QWriteLocker badLocker()
{
    QReadWriteLock localLock;
    return QWriteLocker(&localLock);
}
```

返回的 locker 保存悬空指针，后续析构或手动操作都是未定义行为。应让调用方拥有锁对象，或者只在锁对象有效的作用域内创建 locker。

### 8.2 不可复制，也不可移动

Qt 6.11.1 头文件对 `QWriteLocker` 使用 `Q_DISABLE_COPY`，没有移动构造或移动赋值。一个 locker 对应一份明确的写锁释放责任，不能通过复制或移动隐式转交。

不要把它放进需要复制或移动元素的容器，也不要从函数返回引用局部锁的 locker。

### 8.3 低位状态标志是实现细节

实现内部把锁指针与“当前是否激活”的低位标志合并保存，并在调试构建中检查指针对齐。应用代码不应依赖这个布局，只使用公开成员函数。

## 9. 并发和死锁边界

### 9.1 统一多锁顺序

如果一个线程先锁 A 再锁 B，另一个线程先锁 B 再锁 A，两个 locker 仍然可能互相等待。RAII 保证释放路径，但不会替调用方建立锁顺序。

### 9.2 不要持写锁等待依赖它的线程

写锁内等待另一个线程完成时，那个线程如果需要取得同一把读写锁，就会形成死锁。等待之前应先释放锁，或改用不依赖该锁的同步协议。

### 9.3 信号和回调通常放到锁外

发信号、调用插件或用户回调都可能重入当前对象、取得其他锁或等待事件循环。更稳妥的方式是锁内更新并复制通知所需数据，解锁后再发出通知。

### 9.4 所有访问路径都要遵守保护协议

如果写路径使用 `QWriteLocker`，读路径却绕过同一把锁，数据竞争仍然存在。读者应使用 `QReadLocker`，写者应使用 `QWriteLocker` 或等价的底层 API。

## 10. 逐项 API 语义

### 10.1 `QWriteLocker(QReadWriteLock *readWriteLock)`

```cpp
QWriteLocker(QReadWriteLock *readWriteLock);
```

- 保存传入的锁指针；
- 对非空指针立即取得写锁；
- 可能阻塞；
- `nullptr` 形成未激活 locker；
- 不拥有锁对象；
- 不提供超时和失败返回值。

### 10.2 `~QWriteLocker()`

```cpp
~QWriteLocker();
```

调用 `unlock()`。如果 locker 已激活，则释放写锁；如果为空或已经手动解锁，则不重复访问底层锁。

### 10.3 `unlock()`

```cpp
void unlock();
```

释放当前持有的写锁并标记为未激活。对未激活状态调用不会重复解锁。它不会清空 `readWriteLock()` 返回的指针。

### 10.4 `relock()`

```cpp
void relock();
```

当 locker 关联非空锁且当前未激活时，再次调用 `lockForWrite()`；成功后恢复激活。对已激活或空 locker 不执行加锁。

### 10.5 `readWriteLock() const`

```cpp
QReadWriteLock *readWriteLock() const;
```

返回关联的 `QReadWriteLock *`。手动 `unlock()` 后仍返回原指针；空 locker 返回 `nullptr`。返回值不转移所有权，也不表示当前一定持有写锁。

## 11. 实际使用模式

### 11.1 锁内只做状态提交

```cpp
bool Document::replace(const QByteArray &newBytes)
{
    QWriteLocker locker(&lock);
    if (bytes == newBytes)
        return false;

    bytes = newBytes;
    return true;
}
```

### 11.2 锁外准备，锁内交换

```cpp
void Cache::refresh()
{
    const auto next = loadAndValidate();
    {
        QWriteLocker locker(&lock);
        entries = next;
    }
    emit refreshed();
}
```

通知在锁外发出，避免槽函数重入时再次依赖当前锁。

### 11.3 需要超时时使用底层 API

```cpp
if (!lock.tryLockForWrite(50))
    return false;

updateState();
lock.unlock();
return true;
```

这类手工路径要确保所有成功分支都释放锁。控制流复杂时，应重新设计作用域，或者使用项目已有的可超时 RAII 封装。

## 12. 常见错误

### 12.1 把写锁当作数据备份

locker 不保存旧值，也不会阻止锁外别名修改数据。需要一致性快照时，必须在统一的锁协议下复制数据。

### 12.2 写锁内调用外部回调

回调可能再次进入当前对象、取得同一把锁或等待其他线程。通常应先更新并复制所需结果，解锁后再回调。

### 12.3 写锁内申请读锁

同一线程已经独占写锁时，再申请读锁可能自我阻塞。需要读取刚写入的数据时，直接在当前写临界区内读取，不要重新申请读锁。

### 12.4 以为 `relock()` 有超时

`relock()` 调用的是阻塞式 `lockForWrite()`。要设置超时，使用 `tryLockForWrite(int)` 或 Qt 6.6 起的 `tryLockForWrite(QDeadlineTimer)`。

### 12.5 只给写路径加锁

没有同步的读路径仍可能与写入并发，导致数据竞争。所有访问共享状态的路径都必须使用同一套保护规则。

## API 速查表
| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QWriteLocker(QReadWriteLock *)` | 构造并立即取得写锁 | 可能阻塞；`nullptr` 创建未激活 locker；不拥有锁对象 |
| `~QWriteLocker()` | 自动释放当前写锁 | 对未激活状态不重复解锁；依赖锁对象仍有效 |
| `unlock()` | 提前释放写锁 | 解锁后共享数据不再受此 locker 保护；指针仍保留 |
| `relock()` | 重新取得写锁 | 可能阻塞；无超时和返回值；空 locker 不会关联新锁 |
| `readWriteLock()` | 返回关联的锁指针 | 不表示当前一定持有写锁，不转移所有权 |

## 14. 一句话总结

`QWriteLocker` 是 `QReadWriteLock` 的写侧 RAII 包装：构造时取得独占写锁，析构时释放；它只借用锁对象、不可复制移动、不提供超时。实际使用应把慢工作和回调放到锁外，并确保所有读写路径都遵守同一套同步协议。
