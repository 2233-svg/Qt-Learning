# QPropertyAnimation
> Qt 6.11.1 · Qt Core · 来自 `QPropertyAnimation`

## 作用定位
`QPropertyAnimation` 在给定时长内插值修改 QObject 的可写属性，是 Qt 状态过渡与界面动效的常用动画类。

## API 速查
| API | 是做什么的 |
|---|---|
| `setTargetObject()` | 设置被动画驱动的 QObject。|
| `setPropertyName()` | 设置要修改的属性名。|
| `setStartValue()` / `setEndValue()` | 设置起止值。|
| `setKeyValueAt()` | 在时间线插入关键帧。|
| `setDuration()` | 设置动画时长。|
| `setEasingCurve()` | 设置进度缓动曲线。|
| `start()` / `stop()` | 控制动画。|
| `finished()` | 动画到达结束时通知。|

## 使用场景
淡入淡出 `opacity`、展开 `geometry`、平移 `pos`、在 Qt Quick 或 Widgets 中驱动具备可写属性的对象。

## 常见坑与经验
- 目标属性必须可写且类型可插值；自定义类型可能需注册插值器。
- 动画持续写属性，会打断 QML/C++ 绑定或与 layout/其他动画竞争；明确哪一方在动画期间拥有该属性。
- 目标对象销毁后动画不应继续访问它，通常将动画设为目标的子对象或使用 `DeleteWhenStopped`。

## 知识点覆盖
属性动画、插值、关键帧、缓动、QObject 属性、绑定竞争、对象生命周期。
