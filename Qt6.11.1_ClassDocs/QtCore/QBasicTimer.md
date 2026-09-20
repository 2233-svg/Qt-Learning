# QBasicTimer
> Qt 6.11.1 · Qt Core · 来自 `QBasicTimer`

## 作用定位
`QBasicTimer` 是轻量值类型定时器，用 `timerEvent()` 回调而非信号槽调度周期任务。

## API 速查
| API | 是做什么的 |
|---|---|
| `start(interval, object)` | 在对象所属线程启动定时器。|
| `start(duration, timerType, object)` | 用 chrono 与计时器类型启动。|
| `stop()` | 停止计时器。|
| `isActive()` | 查询是否运行。|
| `timerId()` | 返回关联 timer ID。|

## 使用场景
一个 QObject 管理少量高频内部刷新，且不需要 `timeout()` 信号连接时使用。

## 常见坑与经验
- 必须在拥有目标 QObject 的线程启动和停止。
- `timerEvent()` 可能被多个 timer 调用，应比较 event 的 ID。
- 需要方便连接、单次触发或动态回调时 `QTimer` 更清晰。

## 知识点覆盖
定时器、timerEvent、线程亲和性、chrono、事件循环、轻量调度。
