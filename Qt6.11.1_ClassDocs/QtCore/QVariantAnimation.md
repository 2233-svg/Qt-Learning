# QVariantAnimation
> Qt 6.11.1 · Qt Core · 来自 `QVariantAnimation`
## 作用定位
`QVariantAnimation` 在起止 `QVariant` 值之间插值，按时间产生当前值。它是 `QPropertyAnimation` 的基础，但不自动写入某个对象属性。
## API 速查
| API | 是做什么的 |
|---|---|
| `setStartValue()` / `setEndValue()` | 设置插值两端。 |
| `setKeyValueAt()` | 设置中间关键帧。 |
| `setDuration()` | 设置时长。 |
| `setEasingCurve()` | 设置缓动。 |
| `currentValue()` | 获取当前插值结果。 |
| `valueChanged()` | 当前值变化信号。 |
| `interpolated()` | 自定义类型插值。 |
## 使用场景
驱动颜色、矩形、透明度等值，并在 `valueChanged` 中应用到绘制状态。
## 常见坑与经验
- 只有 Qt 知道如何插值的类型才自动工作；自定义类型要注册插值函数或重写。
- 动画依赖事件循环。
- 目标对象销毁时断开连接。
## 知识点覆盖
动画插值、QVariant、缓动、关键帧、自定义类型、事件循环。
