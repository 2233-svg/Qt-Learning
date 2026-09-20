# QReadWriteLock
> Qt 6.11.1 · Qt Core · 来自 `QReadWriteLock`

## 作用定位
`QReadWriteLock` 提供“多个读者可并行、写者独占”的互斥机制。相比普通 `QMutex`，它在共享数据读多写少时能提高并发读取能力；写入频繁或临界区极短时，额外协调成本未必值得。

默认锁为非递归模式。选择递归模式只是为了兼容确实会重入同一锁的旧设计，不应把它当作修复锁顺序或调用结构问题的常规手段。

## API 速查
| API | 是做什么的 |
|---|---|
| `QReadWriteLock(NonRecursive)` | 创建默认非递归读写锁。 |
| `QReadWriteLock(Recursive)` | 允许同一线程重复锁定；每次锁定仍需对应解锁。 |
| `lockForRead()` | 阻塞直到获得共享读锁。 |
| `lockForWrite()` | 阻塞直到获得独占写锁。 |
| `tryLockForRead(int)` | 在毫秒超时内尝试读锁；负数表示无限等待。 |
| `tryLockForWrite(int)` | 在毫秒超时内尝试写锁。 |
| `tryLockForRead(QDeadlineTimer)` | 以截止时间尝试读锁，Qt 6.6 起可用。 |
| `tryLockForWrite(QDeadlineTimer)` | 以截止时间尝试写锁，Qt 6.6 起可用。 |
| `unlock()` | 释放一次已获得的锁；未锁定时调用是严重错误。 |
| `QReadLocker` / `QWriteLocker` | 推荐的作用域读锁、写锁包装。 |

## 使用场景

### 保护读多写少的缓存
```cpp
QReadWriteLock lock;
QHash<QString, QByteArray> cache;

QByteArray lookup(const QString &key)
{
    QReadLocker guard(&lock);
    return cache.value(key);
}

void replace(const QString &key, QByteArray value)
{
    QWriteLocker guard(&lock);
    cache.insert(key, std::move(value));
}
```

### 带截止时间的后台尝试
```cpp
if (lock.tryLockForWrite(QDeadlineTimer(50))) {
    updateSharedState();
    lock.unlock();
} else {
    deferUpdate();
}
```
超时失败是正常控制流，不能在失败后假定自己持锁或调用 `unlock()`。

## 常见坑与经验
- 同一线程已持读锁时再请求写锁会死锁；本类不支持原子升级。释放读锁、请求写锁后必须重新检查条件。
- 持写锁时不能再请求读锁。需要读取也应在写锁内直接访问被保护数据。
- 锁顺序必须全局一致：若代码有 A、B 两把锁，所有路径都按同一顺序请求。
- 递归锁会掩盖重入设计问题，并不能解决两个不同锁之间的死锁。
- 销毁仍被线程使用的锁是未定义行为；先停止使用者并等待退出。
- GUI 主线程不要长时间持锁做磁盘、网络或复杂计算。

## 知识点覆盖
读写锁、排他写入、递归锁、RAII locker、超时与截止时间、锁升级、死锁预防、临界区性能、GUI 响应性。
