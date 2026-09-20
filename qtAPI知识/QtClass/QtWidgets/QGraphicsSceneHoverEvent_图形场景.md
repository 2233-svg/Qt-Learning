# QGraphicsSceneHoverEvent：场景 item 的 hover 移入、移动和移出事件

> Qt 6.11.1 · `#include <QGraphicsSceneHoverEvent>` · 模块：`Qt6::Widgets` · 继承：`QGraphicsSceneEvent`

`QGraphicsSceneHoverEvent` 是 view 收到 hover 输入后转给场景/item 的事件。它用于无需按下鼠标按钮的悬停交互，例如高亮、显示提示、预览连接点或更新光标。

## 使用场景

item 需要先启用 hover 接收能力，例如 `setAcceptHoverEvents(true)`。之后可在 `hoverEnterEvent()`、`hoverMoveEvent()`、`hoverLeaveEvent()` 中读取当前位置和上一次位置。`pos()` 是 item 坐标，适合命中 item 内部区域；`scenePos()` 适合和其它场景对象比较。

hover 高频触发，处理逻辑要轻，不要在每次移动中做昂贵布局或 I/O。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QGraphicsSceneHoverEvent(QEvent::Type type = None)` | 构造 hover 事件；通常由 Qt 创建。 |
| `pos()` / `scenePos()` / `screenPos()` | 当前 hover 位置的 item、scene、屏幕坐标。 |
| `lastPos()` | 上一次 hover/鼠标事件的 item 坐标。 |
| `lastScenePos()` | 上一次位置的 scene 坐标。 |
| `lastScreenPos()` | 上一次位置的屏幕坐标。 |
| `modifiers() const` | hover 时的键盘修饰键。 |
| `set...()` 系列 | 主要供事件构造端使用。 |
| 前置条件 | item 通常要 `setAcceptHoverEvents(true)` 才会收到 hover。 |
