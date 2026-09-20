# Qt QReadLocker 深入笔记：读锁 RAII 与安全快照访问

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QReadLocker>`  
> 所属模块：`Qt6::Core`  
> 配套类：`QReadWriteLock`、`QWriteLocker`  
> 定位：在作用域内自动取得和释放 QReadWriteLock 的读锁

`QReadLocker` 是 QReadWriteLock 的读模式 RAII 包装器。构造时调用 `lockForRead()`，析构时释放读锁；它允许多个 QReadLocker 同时存在，但会阻塞写者直到所有读锁离开。

## 1. CMake 与最小可用代码

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QReadLocker>
#include <QReadWriteLock>
#include <QHash>

class Catalog
{
public:
    QString name(int id) const
    {
        QReadLocker locker(&m_lock);
        return m_names.value(id); // 返回副本
    }

private:
    mutable QReadWriteLock m_lock;
    QHash<int, QString> m_names;
};
```

`QReadLocker` 没有模板参数，也没有复制/移动接口；它专门接收 `QReadWriteLock *`。

## 2. 构造和析构语义

```cpp
QReadLocker locker(&lock);
```

构造会立即取得读锁，可能阻塞到当前写者完成。析构会调用 `QReadWriteLock::unlock()`。因此底层锁必须比 locker 活得久：

```cpp
{
    QReadLocker locker(&m_lock);
    inspect();
} // 读锁释放
```

传入 `nullptr` 时 QReadLocker 什么也不做：

```cpp
QReadLocker optionalLocker(enabled ? &m_lock : nullptr);
```

这种可选同步会让函数安全性依赖运行时分支，应在 API 设计中谨慎使用。

## 3. 读临界区能做什么

读锁允许多个读者并发，但只保证受保护状态在观察期间不会被写者修改。推荐：

- 复制出值或不可变快照；
- 在锁内完成短小、纯读取逻辑；
- 不调用会写状态或获取写锁的函数；
- 不执行网络、磁盘或长时间计算；
- 不返回内部容器的引用、指针和迭代器。

```cpp
QVector<Item> Catalog::snapshot() const
{
    QReadLocker locker(&m_lock);
    return m_items; // Qt 隐式共享，按值返回快照
}
```

若容器很大，可在写锁内替换 `std::shared_ptr<const Data>`，读锁只复制共享指针，随后在锁外消费不可变数据。

## 4. `unlock()` 与 `relock()`

```cpp
QReadLocker locker(&m_lock);
Snapshot snapshot = makeSnapshot();

locker.unlock();
useOutsideLock(snapshot);

locker.relock();
verifyVersionAndContinue();
```

`unlock()` 提前释放读锁，`relock()` 再次以读模式取得同一锁。relock 之后不能假定解锁期间状态未变；若计算结果基于旧版本，必须重新验证版本号或键值。

如果后续不需要再加锁，优先用嵌套作用域代替手工 unlock/relock：

```cpp
Snapshot snapshot;
{
    QReadLocker locker(&m_lock);
    snapshot = makeSnapshot();
}
useOutsideLock(snapshot);
```

不要对已解锁 locker 再次 `unlock()`，也不要对仍锁定的 locker 调用 `relock()`；这会破坏锁状态或产生自死锁。

## 5. `readWriteLock()`

```cpp
QReadWriteLock *lock = locker.readWriteLock();
```

该函数返回构造时关联的底层锁指针，主要用于需要原始 QReadWriteLock 的 API。它不转移所有权，也不延长锁的生命周期。

```cpp
QReadLocker locker(&m_lock);
// QWaitCondition::wait(locker.readWriteLock()) 的场景需谨慎：
// 条件等待更推荐使用 QMutex，避免读写模式与条件协议混杂。
```

不要把指针保存到 locker 或底层锁销毁之后。

## 6. 读锁不是升级令牌

下面的代码会自死锁：

```cpp
QReadLocker readLocker(&m_lock);
if (!contains(key)) {
    QWriteLocker writeLocker(&m_lock); // 不能持读锁再取写锁
    insert(key);
}
```

正确做法是释放读锁，取得写锁并重新检查：

```cpp
{
    QReadLocker readLocker(&m_lock);
    if (contains(key))
        return;
}

QWriteLocker writeLocker(&m_lock);
if (!contains(key))
    insert(key);
```

读锁与写锁之间存在空窗期，必须接受并发变化，不能把这段流程误称为原子升级。

## 7. 与 const 成员函数配合

```cpp
QString Catalog::name(int id) const
{
    QReadLocker locker(&m_lock);
    return m_names.value(id);
}
```

`const` 只表示该接口不改变对外逻辑状态；若函数内部更新缓存、访问统计或惰性索引，就不再是纯读操作，应改用写锁或独立同步。

## 8. 写者优先下的延迟

QReadWriteLock 在已有写者等待时会阻止新的读者插队，避免写者无限饥饿。因此 QReadLocker 构造可能在“当前没有写者持锁”时仍然等待：队列中已有等待写者就是原因。

不能用“读锁通常很快”推断它一定立即成功。需要有界延迟时，底层锁应改用 `tryLockForRead(int)` 或 `tryLockForRead(QDeadlineTimer)`，但 QReadLocker 本身没有超时构造函数。

## 9. 常见错误

### 错误 1：返回内部引用

```cpp
const QString &name(int id) const; // 锁释放后引用可能被写者修改/失效
```

返回值快照或共享不可变数据。

### 错误 2：读锁内修改容器

即使函数标记 const，只要发生写入就必须用写锁。读者之间的并发写会破坏容器。

### 错误 3：把 QReadLocker 当作可升级锁

它只管理读模式，不能安全地转为写模式。释放后重取并重查条件。

### 错误 4：底层锁先析构

locker 保存的是原始指针，底层 QReadWriteLock 必须覆盖 locker 全生命周期。

### 错误 5：持读锁调用未知回调

回调可能尝试写锁或取得其他锁，造成死锁或观察半完成状态。先复制必要数据，解锁后回调。

## API 速查表
`QReadLocker` 只表达“当前作用域持有读锁”，并不保证返回出去的引用、指针或迭代器在锁释放后仍有效。查 API 时先确认数据是要在锁内使用，还是要复制成能安全交给调用方的快照。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QReadLocker(QReadWriteLock *lock)` | 构造时对 `QReadWriteLock` 取得读锁。 | 可能阻塞；传 `nullptr` 时无操作；底层锁必须比 locker 活得久。 |
| 析构 | `~QReadLocker()` | 析构时释放当前持有的读锁。 | 只能释放它自己取得且尚未 `unlock()` 的锁；不要直接操作底层锁破坏状态。 |
| 提前释放 | `unlock()` | 在作用域结束前释放读锁。 | 释放后其他写者可能修改共享状态；后续使用旧引用、迭代器或版本假设都不安全。 |
| 重新加锁 | `relock()` | 再次以读模式取得同一把锁。 | 空窗期状态可能变化，必须重新检查条件；不能把它当成原子读写升级。 |
| 底层指针 | `readWriteLock()` | 返回构造时关联的 `QReadWriteLock *`。 | 不转移所有权；不要保存到超过 locker 或底层锁生命周期的位置。 |
| 读快照 | 与 `QReadWriteLock::lockForRead()` 配合 | 用 RAII 管理只读临界区，允许多个读者并发。 | 读锁内不要修改受保护状态，返回给调用方时应返回值副本或不可变快照。 |
| 取舍 | 与 `QWriteLocker` 对比 | `QReadLocker` 只表达观察，`QWriteLocker` 才表达修改提交。 | const 函数若更新 cache、统计或惰性字段，也不能只用读锁。 |

## 11. 总结

1. QReadLocker 是 QReadWriteLock 读模式的 RAII 包装器。
2. 多个读者可并发，但等待写者会阻止新读者继续插队。
3. 构造可能阻塞，析构释放读锁；底层锁必须活得更久。
4. 读临界区应短小、纯读取，并返回副本或不可变快照。
5. `unlock()`/`relock()` 之间状态可能改变，重新加锁后必须重查。
6. QReadLocker 不能升级到写锁，不能替代原子读改写协议。
7. `readWriteLock()` 只返回指针，不转移所有权。
8. const 函数若更新 cache 或统计，不能仅凭 const 使用读锁。
9. 需要超时读锁时，直接使用 QReadWriteLock 的 tryLock API。
10. 优先在解锁后调用未知回调，避免读写锁与外部锁形成等待环。
