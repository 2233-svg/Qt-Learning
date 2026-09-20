# QGraphicsSceneResizeEvent：QGraphicsWidget 的尺寸变化事件

> Qt 6.11.1 · `#include <QGraphicsSceneResizeEvent>` · 模块：`Qt6::Widgets` · 继承：`QGraphicsSceneEvent`

`QGraphicsSceneResizeEvent` 在 `QGraphicsWidget` 的几何尺寸变化时发送，类似 `QResizeEvent`，但尺寸类型是 `QSizeF`。它用于响应图形 widget 的布局和几何变化。

## 使用场景

自定义 `QGraphicsWidget` 需要在 resize 后重新排布内部 item、更新缓存、重算端口位置或通知外部布局时，可处理该事件。它描述的是 widget 几何尺寸变化，不是 view 窗口 resize，也不是 sceneRect 变化。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QGraphicsSceneResizeEvent()` | 构造 resize 事件；通常由 Qt 创建。 |
| `oldSize() const` | 返回 resize 前尺寸。 |
| `newSize() const` | 返回 resize 后尺寸。 |
| `setOldSize(const QSizeF &)` | 设置旧尺寸，主要供事件构造端使用。 |
| `setNewSize(const QSizeF &)` | 设置新尺寸，主要供事件构造端使用。 |
| 适用对象 | 主要用于 `QGraphicsWidget`。 |
| 与 view resize | 不表示 `QGraphicsView` 视口尺寸变化。 |
