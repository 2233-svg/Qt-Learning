# QPanGesture：连续平移手势的数据对象

> Qt 6.11.1 · `#include <QPanGesture>` · 模块：`Qt6::Widgets` · 继承：`QGesture`

`QPanGesture` 描述用户在触摸板、触摸屏或其它输入设备上的平移动作。它主要提供累计位移、上一次位移和本次增量，供视图拖动、画布移动、图片浏览等场景使用。

## 使用场景

目标 widget 需要先 grab `Qt::PanGesture`，然后在 `QGestureEvent` 中取出 `QPanGesture`。实际 UI 更新通常使用 `delta()` 做增量移动；需要从手势起点计算绝对位置时用 `offset()`。

不要把 pan 与 kinetic scrolling 混为一谈。平移手势只是输入识别结果；带惯性的滚动体验通常交给 `QScroller`。

## 属性语义

`offset()` 是从手势开始到当前的总位移。`lastOffset()` 是上一次事件投递时的总位移。`delta()` 等于二者差值，用于一次事件内的增量更新。`acceleration()` 描述触点运动加速度，具体稳定性取决于平台输入设备。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QPanGesture(QObject *parent = nullptr)` | 构造平移手势；通常由 Qt 创建。 |
| `lastOffset() const` | 上一次事件中的累计位移；第一次通常为零。 |
| `setLastOffset(const QPointF &)` | 设置上次累计位移，主要供 recognizer 使用。 |
| `offset() const` | 当前从手势起点到当前位置的累计位移。 |
| `setOffset(const QPointF &)` | 设置累计位移，主要供 recognizer 使用。 |
| `delta() const` | 当前事件相对上次事件的位移增量。 |
| `acceleration() const` | 当前运动加速度。 |
| `setAcceleration(qreal)` | 设置加速度，主要供 recognizer 使用。 |
| `state()` | 继承自 `QGesture`，连续手势通常处理 `GestureUpdated`。 |
