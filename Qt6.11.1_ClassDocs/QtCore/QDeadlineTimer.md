# QDeadlineTimer
> Qt 6.11.1 · Qt Core · 来自 `QDeadlineTimer`

## 作用定位
`QDeadlineTimer` 表示一个绝对截止时间或“永不超时”，用于把剩余超时预算稳定地传递给锁、条件变量和等待操作。

## API 速查
| API | 是做什么的 |
|---|---|
| `setRemainingTime()` | 从相对时长设置截止点。|
| `setDeadline()` | 设置绝对 deadline。|
| `remainingTime()` | 查询剩余毫秒。|
| `remainingTimeAsDuration()` | 用 chrono duration 查询剩余时间。|
| `hasExpired()` | 判断是否已到期。|
| `isForever()` | 判断是否无限等待。|
| `addNSecs()` | 在当前 deadline 上增减时间。|

## 使用场景
一次操作总预算 5 秒，经过多次 I/O 或锁等待后仍将“剩余预算”传给下一步，而不是每一步重新给 5 秒。

## 常见坑与经验
- 它适合超时控制，不适合度量耗时；度量用 `QElapsedTimer`。
- 传递 `Forever` 前确认不会在应用退出或线程停止时导致永久阻塞。

## 知识点覆盖
deadline、超时预算、chrono、等待、永久等待、耗时测量区分。
