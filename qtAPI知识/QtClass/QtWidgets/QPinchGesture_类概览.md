# QPinchGesture：缩放、旋转和中心点变化的捏合手势

> Qt 6.11.1 · `#include <QPinchGesture>` · 模块：`Qt6::Widgets` · 继承：`QGesture`

`QPinchGesture` 描述两指捏合类输入，常用于缩放、旋转或围绕中心点移动内容。它同时保存当前变化、上一次变化和整个手势累计变化。

## 使用场景

在图片查看器、地图、画布或图形场景中，grab `Qt::PinchGesture` 后读取 `QPinchGesture`。实时缩放通常看 `scaleFactor()` 或 `totalScaleFactor()`；旋转看 `rotationAngle()` 或 `totalRotationAngle()`；围绕触点操作则使用 `centerPoint()`。

`changeFlags()` 告诉你本次事件哪些属性变了，避免每次都同时更新缩放、旋转和位置。`totalChangeFlags()` 表示从手势开始以来出现过哪些变化。

## 边界提示

用户可能松开一个手指再放到新位置，手势仍继续更新；此时 total 值可能跨多个阶段累积，和当前阶段值不完全相同。处理复杂变换时，应明确使用“本次变化”还是“总变化”，不要混用。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QPinchGesture(QObject *parent = nullptr)` | 构造捏合手势；通常由 Qt 创建。 |
| `ChangeFlag` / `ChangeFlags` | 标记 scale、rotation、centerPoint 哪些属性变化。 |
| `changeFlags() const` | 本次事件中变化的属性集合。 |
| `totalChangeFlags() const` | 从手势开始以来变化过的属性集合。 |
| `scaleFactor() const` | 当前阶段缩放因子。 |
| `lastScaleFactor() const` | 上一次事件的缩放因子。 |
| `totalScaleFactor() const` | 从手势开始累计的缩放因子。 |
| `rotationAngle() const` | 当前阶段旋转角度。 |
| `lastRotationAngle() const` | 上一次事件的旋转角度。 |
| `totalRotationAngle() const` | 累计旋转角度。 |
| `startCenterPoint() const` | 手势开始时的中心点。 |
| `lastCenterPoint() const` | 上一次事件的中心点。 |
| `centerPoint() const` | 当前两输入点的中心点。 |
| `set...()` 系列 | 设置属性，主要供 recognizer 或自定义手势系统使用。 |
