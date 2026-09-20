# QChronoTimer
> Qt 6.11.1 · Qt Core · 来自 `QChronoTimer`

## 作用定位
`QChronoTimer` 是以 `std::chrono` 时长为核心的 QObject 定时器，支持比 `QTimer` 更宽的时间范围与更明确的单位。

## API 速查
| API | 是做什么的 |
|---|---|
| `setInterval()` | 用 chrono duration 设置周期。|
| `start()` / `stop()` | 启动或停止。|
| `setSingleShot()` | 设置一次性触发。|
| `timeout()` | 到期时发出的信号。|
| `remainingTimeAsDuration()` | 查询剩余时间。|
| `setTimerType()` | 选择精确度与功耗取舍。|

## 使用场景
需要长时间间隔、明确纳秒/毫秒单位或与 C++ chrono API 协作的调度任务。

## 常见坑与经验
- 定时器依赖所属线程事件循环；跨线程启动/停止会出问题。
- 定时器不是实时保证，系统负载下 timeout 可延后，应让业务逻辑按实际时间计算。

## 知识点覆盖
chrono、事件循环、定时精度、单次计时、线程亲和性、时间漂移。
