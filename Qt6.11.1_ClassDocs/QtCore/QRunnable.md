# QRunnable
> Qt 6.11.1 · Qt Core · 来自 `QRunnable`

## 作用定位
`QRunnable` 表示交给 `QThreadPool` 执行的一段无返回值任务。它不是线程，也不自带事件循环；`run()` 在池中的某个工作线程执行。

## API 速查
| API | 是做什么的 |
|---|---|
| `run()` | 实现任务主体。 |
| `QRunnable::create(callable)` | 用无参 callable 快速创建 runnable。 |
| `setAutoDelete(bool)` | 设置线程池完成后是否删除该对象，必须在 `start()` 前调用。 |
| `autoDelete()` | 查询当前所有权策略。 |

## 使用场景
```cpp
QThreadPool::globalInstance()->start(
    QRunnable::create([path] {
        const auto result = parseFile(path);
        QMetaObject::invokeMethod(qApp, [result] { showResult(result); });
    }));
```
工作线程只计算或执行阻塞 I/O；涉及 QWidget/QML 的操作必须回到 GUI 线程。

## 常见坑与经验
- 默认 `autoDelete` 为真，线程池运行完会删除任务，提交后不能继续访问裸指针。
- 关闭自动删除后，调用者必须在确认任务不再运行后释放对象。
- 不要把同一个 auto-delete runnable 多次提交，除非你完全理解线程池的重入与删除时机。
- `QRunnable` 没有取消协议；用共享原子标志、`QPromise` 或更高层 `QtConcurrent` 设计取消。
- `run()` 异常不能穿过线程边界；在任务内部捕获并把错误传回调用方。

## 知识点覆盖
线程池、任务所有权、GUI 线程、异常边界、取消设计、工作线程与事件循环。
