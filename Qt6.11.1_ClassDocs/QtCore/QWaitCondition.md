# QWaitCondition
> Qt 6.11.1 · Qt Core · 来自 `QWaitCondition`
## 作用定位
`QWaitCondition` 让线程在某个条件未满足时释放互斥锁并睡眠，直到被唤醒后重新竞争锁。它通常与 `QMutex` 和共享状态一起使用。
## API 速查
| API | 是做什么的 |
|---|---|
| `wait(mutex)` | 释放锁并等待唤醒，返回后重新持锁。 |
| `wakeOne()` | 唤醒一个等待线程。 |
| `wakeAll()` | 唤醒所有等待线程。 |
| 超时 wait | 在截止时间或毫秒超时后返回。 |
## 使用场景
```cpp
mutex.lock();
while (queue.isEmpty())
    notEmpty.wait(&mutex);
auto item = queue.dequeue();
mutex.unlock();
```
## 常见坑与经验
- 永远在循环中检查条件，处理虚假唤醒和竞争。
- 修改共享状态和 wake 应在同一协议下完成。
- 不要在 GUI 线程等待条件变量。
## 知识点覆盖
条件变量、生产者消费者、虚假唤醒、互斥锁、阻塞线程。
