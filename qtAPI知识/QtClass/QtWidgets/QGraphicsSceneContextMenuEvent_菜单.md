# QGraphicsSceneContextMenuEvent：场景中的上下文菜单请求

> Qt 6.11.1 · `#include <QGraphicsSceneContextMenuEvent>` · 模块：`Qt6::Widgets` · 继承：`QGraphicsSceneEvent`

`QGraphicsSceneContextMenuEvent` 是 `QGraphicsView` 把 `QContextMenuEvent` 转换给场景和 item 后的事件对象。它说明“用户想在这个位置打开上下文菜单”，并附带触发原因、修饰键和三套坐标。

## 使用场景

在 `QGraphicsItem::contextMenuEvent()` 里根据 `pos()` 判断 item 内部区域，根据 `scenePos()` 查找场景对象，根据 `screenPos()` 弹出 `QMenu::exec()`。键盘触发菜单时，`reason()` 会是 `Keyboard`，此时位置语义应更谨慎，可能需要用当前选中项或焦点项定位菜单。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QGraphicsSceneContextMenuEvent(QEvent::Type type = None)` | 构造场景上下文菜单事件；通常由 Qt 创建。 |
| `Reason` | `Mouse`、`Keyboard`、`Other`，表示触发上下文菜单的原因。 |
| `pos() const` | item 局部坐标中的请求位置。 |
| `scenePos() const` | scene 坐标中的请求位置。 |
| `screenPos() const` | 屏幕坐标中的请求位置，弹出菜单常用。 |
| `modifiers() const` | 请求菜单时的键盘修饰键。 |
| `reason() const` | 返回触发原因；键盘触发时不要完全依赖鼠标坐标。 |
| `set...()` 系列 | 主要供框架或测试构造事件使用。 |
