# QTimerEvent
> Qt 6.11.1 · Qt Core · 来自 `QTimerEvent`
## 作用定位
`QTimerEvent` 是低层 `QObject::startTimer()` 触发的事件对象，携带 timer id，供重写 `timerEvent()` 的类区分多个计时器。
## API 速查
| API | 是做什么的 |
|---|---|
| `timerId()` | 返回触发本事件的 timer id。 |
## 使用场景
在高频轻量对象中避免创建多个 `QTimer` 子对象，直接用 `startTimer()`/`killTimer()` 管理。
## 常见坑与经验
- 记住保存 timer id，停止时传给 `killTimer()`。
- 和 `QTimer` 一样依赖事件循环。
- 多个 timer 共享 `timerEvent()` 时必须检查 id。
## 知识点覆盖
低层计时器、事件分发、timer id、QObject 事件循环。
