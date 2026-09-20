# QRecursiveMutex
> Qt 6.11.1 · Qt Core · 来自 `QRecursiveMutex`

## 作用定位
`QRecursiveMutex` 是允许同一线程重复加锁的互斥量。每次 `lock()` 都增加持有层数，必须以相同次数 `unlock()` 才真正释放给其他线程。

它适用于不可避免的同步重入，例如一个已加锁的公共函数调用同样需要锁的内部公共函数。新代码优先把“无锁私有实现”和“负责加锁的公开入口”分开，通常比递归锁更易推理。

## API 速查
| API | 是做什么的 |
|---|---|
| `lock()` | 阻塞直到获得锁；持有者是当前线程时递归计数加一。 |
| `unlock()` | 递减持有计数，归零后才真正释放。 |
| `tryLock(int)` | 在毫秒超时内尝试获得锁。 |
| `tryLock(QDeadlineTimer)` | 以绝对截止时间尝试获得锁，Qt 6.6 起可用。 |
| `try_lock()` | 适配标准库 Lockable 约定的非阻塞尝试。 |
| `try_lock_for(duration)` | 适配标准库时长超时语义。 |
| `try_lock_until(timePoint)` | 适配标准库截止时间语义。 |
| `QMutexLocker` | 推荐的 RAII 管理方式。 |

## 使用场景
```cpp
class Registry {
    QRecursiveMutex m_mutex;

public:
    void clear()
    {
        QMutexLocker lock(&m_mutex);
        removeAll(); // 历史接口也会加同一把锁
    }

    void removeAll()
    {
        QMutexLocker lock(&m_mutex);
        m_items.clear();
    }
};
```
这段代码能工作，但更清晰的长期结构是 `clear()` 和 `removeAll()` 都调用不加锁的 `removeAllUnlocked()`，由最外层负责一次加锁。

## 常见坑与经验
- 递归只针对“同一线程、同一把锁”；两个线程的互相等待依然会死锁。
- 重复 `lock()` 就必须重复 `unlock()`。RAII 应嵌套在匹配作用域中，别手工猜计数。
- 它无法保护没遵循同一互斥量的访问路径。
- 不要在持锁时触发未知回调、发阻塞信号或进入事件循环；重入会让共享状态处于中间态。
- 等待超时后锁并未获得，后续访问必须走降级路径。

## 知识点覆盖
递归互斥、可重入性、锁计数、RAII、标准库 Lockable、临界区设计、回调重入、死锁与重构策略。
