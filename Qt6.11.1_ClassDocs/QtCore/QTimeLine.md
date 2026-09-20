# QTimeLine
> Qt 6.11.1 · Qt Core · 来自 `QTimeLine`
## 作用定位
`QTimeLine` 产生随时间变化的数值帧，用于简单动画进度、缓动曲线和状态过渡。复杂属性动画优先用 `QPropertyAnimation`。
## API 速查
| API | 是做什么的 |
|---|---|
| `setDuration()` | 设置动画总时长。 |
| `setFrameRange()` | 设置整数帧范围。 |
| `setEasingCurve()` | 设置缓动曲线。 |
| `start/stop/pause/resume` | 控制时间线。 |
| `valueChanged/frameChanged` | 输出进度或帧。 |
| `finished()` | 时间线结束信号。 |
## 使用场景
驱动自定义绘制组件的过渡值，并在 `valueChanged` 中调用 `update()`。
## 常见坑与经验
- 它依赖事件循环，阻塞 GUI 线程会丢帧。
- 不自动修改对象属性，需你把值应用到目标。
- 动画目标销毁时断开连接或让 timeline 有合适父对象。
## 知识点覆盖
时间线、缓动、帧、事件循环、自绘动画、生命周期。
