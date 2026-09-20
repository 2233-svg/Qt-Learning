# QReadLocker
> Qt 6.11.1 · Qt Core · 来自 `QReadLocker`

## 作用定位
`QReadLocker` 是 `QReadWriteLock` 的读锁 RAII 包装。构造时获得共享读锁，离开作用域自动释放，使“每条成功加锁路径都必须解锁”的责任由 C++ 生命周期保证。

它适合读远多于写的共享缓存、配置快照和索引。它只保护约定由同一把锁保护的数据；没有使用这把锁的代码仍可造成数据竞争。

## API 速查
| API | 是做什么的 |
|---|---|
| `QReadLocker(QReadWriteLock *)` | 立即取得读锁；传空指针时成为空操作。 |
| 析构函数 | 若当前持锁则自动释放读锁。 |
| `unlock()` | 在作用域尚未结束前暂时放开读锁。 |
| `relock()` | 对此前 `unlock()` 的 locker 重新取得读锁。 |
| `readWriteLock()` | 取得关联的锁指针，便于断言或低层协调。 |

## 使用场景
```cpp
QString Cache::lookup(const QString &key) const
{
    QReadLocker locker(&m_lock);
    return m_values.value(key);
}
```
多个读取者可同时进入；写线程获得写锁前需等待现有读者结束。读锁范围应只包住共享数据访问，不要在锁内调用可能发信号、I/O 或回调未知代码的函数。

临时放锁的合理用途是先读出必要副本，再执行慢操作：
```cpp
QReadLocker locker(&m_lock);
const auto snapshot = m_values;
locker.unlock();
writeSnapshot(snapshot);
```

## 常见坑与经验
- `QReadLocker` 不能把读锁升级为写锁。需要修改时先释放读锁，再竞争写锁并重新验证条件。
- 空指针可用于条件性加锁，但会掩盖配置错误；一般更推荐保证锁始终存在。
- 不要在一个线程持有读锁时等待另一个需要写锁的线程完成，这很容易死锁。
- locker 持有时不要让被保护对象提前销毁；通常锁和数据拥有相同或更长生命周期。
- 读锁不是“只读对象”承诺；团队必须约定所有读写路径都使用同一锁。

## 知识点覆盖
RAII、共享锁、读多写少、临界区、锁粒度、锁升级限制、死锁、快照复制、线程安全契约。
