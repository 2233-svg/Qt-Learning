# QWriteLocker
> Qt 6.11.1 · Qt Core · 来自 `QWriteLocker`
## 作用定位
`QWriteLocker` 是 `QReadWriteLock` 的写锁 RAII 包装。构造时获得独占写锁，析构时释放，保护共享数据的修改阶段。
## API 速查
| API | 是做什么的 |
|---|---|
| `QWriteLocker(lock)` | 立即取得写锁。 |
| `unlock()` | 提前释放写锁。 |
| `relock()` | 重新获得写锁。 |
| `readWriteLock()` | 返回关联锁。 |
## 使用场景
```cpp
QWriteLocker locker(&lock);
cache.insert(key, value);
```
## 常见坑与经验
- 写锁会阻塞所有读者和写者，临界区要短。
- 从读锁升级到写锁不是原子操作，释放后要重新检查条件。
- 不要在持写锁时调用未知回调或发阻塞信号。
## 知识点覆盖
独占锁、RAII、读写锁、临界区、锁升级、死锁规避。
