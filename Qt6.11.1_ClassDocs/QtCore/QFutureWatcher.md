# QFutureWatcher
> Qt 6.11.1 · Qt Core · 来自 `QFutureWatcher`

## 作用定位
`QFutureWatcher<T>` 把 `QFuture<T>` 的完成、进度、结果就绪和取消状态转换为 QObject 信号，方便在 GUI 或事件驱动代码中观察任务。

## API 速查
| API | 是做什么的 |
|---|---|
| `setFuture()` | 开始观察一个 future。|
| `future()` | 取得当前 future。|
| `finished()` | future 结束时通知。|
| `resultReadyAt()` | 某个结果索引可读取。|
| `resultsReadyAt()` | 一段结果可读取。|
| `progressValueChanged()` | 任务进度变化。|
| `canceled()` | future 被取消时通知。|
| `cancel()` | 向关联任务请求取消。|

## 使用场景
界面启动后台计算后，把 watcher 作为页面对象子项；连接进度条、完成结果和错误处理，页面销毁时 watcher 一同失效。

## 常见坑与经验
- `finished()` 只代表任务结束，不代表没有异常；读取结果时仍需处理错误。
- 重复 `setFuture()` 前先明确旧任务是否仍要继续；watcher 改观察对象并不会自动取消旧任务。
- 观察器的线程事件循环负责信号分发，UI watcher 必须在 GUI 线程。

## 知识点覆盖
Future 观察、信号槽、进度、多结果、取消、异常、UI 线程。
