# QTimer
> Qt 6.11.1 · Qt Core · 来自 `QTimer`
## 作用定位
`QTimer` 在对象所属线程的事件循环中按时间间隔发出 `timeout()`。它是调度回调，不是实时系统计时器。
## API 速查
| API | 是做什么的 |
|---|---|
| `start()` / `stop()` | 启停定时器。 |
| `setInterval()` | 设置间隔。 |
| `setSingleShot()` | 设置只触发一次。 |
| `singleShot()` | 静态一次性延迟调用。 |
| `setTimerType()` | 控制精度与省电策略。 |
| `remainingTime()` | 查询剩余时间。 |
| `timeout()` | 到期信号。 |
## 使用场景
定期刷新状态、延迟执行、输入防抖、超时取消。
## 常见坑与经验
- 所在线程必须有事件循环。
- 超时回调执行太久会推迟后续触发。
- 精确计时或耗时测量用 `QElapsedTimer`。
- 修改 UI 的 timer 应在 GUI 线程。
## 知识点覆盖
事件循环、单次定时、防抖、timer type、线程亲和性、非实时调度。
