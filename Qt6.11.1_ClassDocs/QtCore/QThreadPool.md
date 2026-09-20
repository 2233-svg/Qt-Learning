# QThreadPool
> Qt 6.11.1 · Qt Core · 来自 `QThreadPool`

## 作用定位
`QThreadPool` 复用一组工作线程运行 `QRunnable`，适合短任务和批量并发任务，避免频繁创建销毁线程。
## API 速查
| API | 是做什么的 |
|---|---|
| `globalInstance()` | 获取应用全局线程池。 |
| `start(QRunnable*)` | 提交任务。 |
| `tryStart()` | 有可用线程时才提交。 |
| `setMaxThreadCount()` | 限制并发线程数。 |
| `activeThreadCount()` | 查询当前活跃线程数。 |
| `waitForDone()` | 等待已提交任务完成。 |
| `reserveThread()` / `releaseThread()` | 为外部阻塞工作调整容量。 |
| `clear()` / `tryTake()` | 管理尚未开始的任务。 |
## 使用场景
CPU 密集型小任务、缩略图生成、批量解析文件。结果回 GUI 线程用 queued invoke 或信号。
## 常见坑与经验
- 任务没有事件循环假设；需要 QObject 异步 I/O 时另设线程模型。
- auto-delete runnable 提交后不要再访问裸指针。
- 阻塞任务过多会占满线程池，影响其他 QtConcurrent 工作。
## 知识点覆盖
线程复用、任务调度、并发上限、线程池饥饿、结果投递、QRunnable 所有权。
