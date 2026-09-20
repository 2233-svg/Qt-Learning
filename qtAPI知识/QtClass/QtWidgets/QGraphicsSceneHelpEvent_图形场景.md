# QGraphicsSceneHelpEvent：场景中的 tooltip 请求

> Qt 6.11.1 · `#include <QGraphicsSceneHelpEvent>` · 模块：`Qt6::Widgets` · 继承：`QGraphicsSceneEvent`

`QGraphicsSceneHelpEvent` 表示 Graphics View 中一次 tooltip 请求。`QGraphicsView` 收到 `QEvent::ToolTip` 后创建该事件并转发给场景；默认场景会显示鼠标下 z 值最高 item 的 tooltip。

## 使用场景

大多数情况下给 item 设置 `setToolTip()` 就够了。需要自定义 tooltip 内容、延迟加载说明、或根据 scene 位置动态选择帮助文本时，可以在场景或 item 的事件处理中读取 `scenePos()` 和 `screenPos()`。

注意：`QGraphicsView` 默认不会把 What's This 和 status tip 帮助请求作为该事件转发。需要这些能力时，要重写 `QGraphicsView::viewportEvent()` 自行转发。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QGraphicsSceneHelpEvent(QEvent::Type type = None)` | 构造帮助事件；通常由 Qt 创建。 |
| `scenePos() const` | tooltip 请求发生的 scene 坐标。 |
| `screenPos() const` | tooltip 请求发生的屏幕坐标，显示自定义浮窗常用。 |
| `setScenePos(const QPointF &)` | 设置 scene 坐标，主要供事件构造端使用。 |
| `setScreenPos(const QPoint &)` | 设置屏幕坐标，主要供事件构造端使用。 |
| 默认行为 | 场景显示鼠标下最高 z 值 item 的 tooltip。 |
| 非 tooltip 帮助 | What's This/status tip 默认不通过该事件转发。 |
