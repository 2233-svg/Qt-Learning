# QElapsedTimer
> Qt 6.11.1 · Qt Core · 来自 `QElapsedTimer`

## 作用定位
`QElapsedTimer` 使用单调时钟测量经过时间，适合性能统计、超时预算和帧耗时，不受系统墙钟被用户或 NTP 修改影响。

## API 速查
| API | 是做什么的 |
|---|---|
| `start()` | 记录起点。|
| `restart()` | 返回已过时间并重新开始。|
| `elapsed()` | 返回经过毫秒数。|
| `nsecsElapsed()` | 返回更高精度的纳秒数。|
| `hasExpired(timeout)` | 判断经过时间是否超过给定毫秒。|
| `msecsSinceReference()` | 读取单调参考时钟值。|
| `durationElapsed()` | 以 chrono duration 获取耗时。|

## 使用场景
测量解析或绘制耗时、实现一个函数内部的总超时预算、记录性能回归数据。

## 常见坑与经验
- 不能将 `msecsSinceReference()` 持久化或与其他机器比较；它不是 UTC 时间戳。
- 单次测量容易受缓存、调度和预热影响，性能结论要取多次统计。
- `hasExpired()` 适合检查，不会中断阻塞操作。

## 知识点覆盖
单调时钟、性能测量、超时、chrono、基准测试、墙钟区别。
