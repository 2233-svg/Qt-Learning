# QThread
> Qt 6.11.1 · Qt Core · 来自 `QThread`

## 作用定位
`QThread` 管理一个操作系统线程和可选事件循环。关键区别：`QThread` 对象本身通常属于创建它的线程，而 `run()` 中执行的是新线程。
## API 速查
| API | 是做什么的 |
|---|---|
| `start()` | 启动线程并调用 `run()`。 |
| `run()` | 线程入口；默认调用 `exec()` 开事件循环。 |
| `quit()` / `exit()` | 请求事件循环退出。 |
| `wait()` | 等待线程结束。 |
| `moveToThread()` | 将 QObject 的线程亲和性切到目标线程。 |
| `currentThread()` / `currentThreadId()` | 查询当前执行线程。 |
| `finished()` / `started()` | 生命周期信号。 |
| `requestInterruption()` | 发出协作式中断请求。 |
## 使用场景
把 worker 对象移动到线程，用 queued signal 启动工作，完成后退出并清理。
## 常见坑与经验
- 不要在 `QThread` 子类对象的槽里直接操作工作数据，槽默认在对象所属线程执行。
- GUI 只能在主线程更新。
- 析构前必须让线程停止并 `wait()`。
- 中断请求不是强制杀线程，worker 要定期检查。
## 知识点覆盖
线程亲和性、事件循环、worker 模式、queued connection、协作取消、GUI 线程。
