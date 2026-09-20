# QGraphicsSceneMoveEvent：QGraphicsWidget 的位置变化事件

> Qt 6.11.1 · `#include <QGraphicsSceneMoveEvent>` · 模块：`Qt6::Widgets` · 继承：`QGraphicsSceneEvent`

`QGraphicsSceneMoveEvent` 在 `QGraphicsWidget` 的本地位置变化时发送，类似 widget 世界里的 `QMoveEvent`，但位置类型是 `QPointF`。它是图形 widget 的几何通知，不是鼠标拖动事件。

## 使用场景

当自定义 `QGraphicsWidget` 需要在移动后更新连接线、吸附辅助线、缓存区域或外部模型坐标时，可以处理该事件。普通 `QGraphicsItem` 的位置变化更多通过 `itemChange()` 观察；这个事件主要面向 `QGraphicsWidget`。

事件会在位置改变时立即发送，旧位置和新位置都是 item 的本地位置语义，不是 scene 坐标。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QGraphicsSceneMoveEvent()` | 构造移动事件；通常由 Qt 创建。 |
| `oldPos() const` | 返回移动前的位置。 |
| `newPos() const` | 返回移动后的位置。 |
| `setOldPos(const QPointF &)` | 设置旧位置，主要供事件构造端使用。 |
| `setNewPos(const QPointF &)` | 设置新位置，主要供事件构造端使用。 |
| 适用对象 | 主要用于 `QGraphicsWidget`，不要和鼠标移动事件混淆。 |
