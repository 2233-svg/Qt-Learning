# QAbstractAnimation
> Qt 6.11.1 · Qt Core · 来自 `QAbstractAnimation`

## 作用定位
`QAbstractAnimation` 是 Qt 动画时间线的基类。它负责运行状态、循环、方向和当前时间；属性值如何变化由 `QPropertyAnimation` 等子类决定。

## API 速查
| API | 是做什么的 |
|---|---|
| `start()` | 启动或重启动画。|
| `stop()` / `pause()` / `resume()` | 控制运行状态。|
| `setDuration()` | 子类定义总时长。|
| `setLoopCount()` | 设置循环次数，`-1` 为无限循环。|
| `setDirection()` | 正向或反向播放。|
| `setCurrentTime()` | 跳到指定毫秒位置。|
| `stateChanged()` / `finished()` | 观察状态转换和最终完成。|

## 使用场景
用 `QPropertyAnimation` 做属性过渡、用动画组编排步骤；业务逻辑监听 `finished()`，不要依赖估算的定时器。

## 常见坑与经验
- 无限循环动画不会发出最终 `finished()`。
- 在 `finished()` 中立刻删除动画时，需保证它没有被动画组或父对象继续引用。
- GUI 属性动画应留在 GUI 线程运行。

## 知识点覆盖
时间线、状态机、循环、反向播放、动画完成时机、QObject 生命周期。
