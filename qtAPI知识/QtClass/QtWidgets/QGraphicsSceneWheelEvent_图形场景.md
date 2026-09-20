# QGraphicsSceneWheelEvent：Graphics View 的滚轮与触控板滚动事件

> Qt 6.11.1 · `#include <QGraphicsSceneWheelEvent>` · 模块：`Qt6::Widgets` · 继承：`QGraphicsSceneEvent`

`QGraphicsSceneWheelEvent` 把 view 收到的 `QWheelEvent` 转换成场景/item 可用的数据。它既支持传统滚轮的离散 `delta()`，也支持高精度触控板的 `pixelDelta()`、滚动阶段和自然滚动方向。

## 使用场景

画布缩放常用 `scenePos()` 作为缩放中心，用 `delta()` 或 `pixelDelta()` 推导缩放比例；平滑平移则优先使用 `pixelDelta()`。如果 `pixelDelta()` 为空，再退回传统 `delta()`。

不要假设正值一定表示“向上滚”。平台可能启用自然滚动，`isInverted()` 会告诉你 delta 方向是否已反转。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QGraphicsSceneWheelEvent(QEvent::Type type = None)` | 构造场景滚轮事件；通常由 Qt 创建。 |
| `pos()` / `scenePos()` / `screenPos()` | 分别返回 item、scene、屏幕坐标中的滚轮位置。 |
| `buttons() const` | 滚动时按住的鼠标按钮集合。 |
| `modifiers() const` | 滚动时的键盘修饰键，常用于 Ctrl+滚轮缩放。 |
| `delta() const` | 传统滚轮增量，单位为 1/8 度，常见一格为 120。 |
| `orientation() const` | 传统滚轮主方向。 |
| `pixelDelta() const` | 高精度像素滚动距离；可能为空点。 |
| `phase() const` | 滚动阶段，适合触控板和惯性滚动处理。 |
| `isInverted() const` | 是否启用自然滚动方向反转。 |
| `set...()` 系列 | 主要供事件构造端使用，处理事件时通常只读。 |
