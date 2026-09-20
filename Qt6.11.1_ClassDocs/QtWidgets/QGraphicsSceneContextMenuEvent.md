# QGraphicsSceneContextMenuEvent

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsSceneContextMenuEvent`

## 1. 先建立直觉

`QGraphicsSceneContextMenuEvent` 是 Graphics View 中的上下文菜单事件。它可能来自鼠标右键、键盘菜单键或其他平台手势。

它让 item 能在正确位置弹出菜单，并知道用户为什么请求菜单。这对可访问性和键盘操作很重要。

## 2. 类说明

`QGraphicsSceneContextMenuEvent` 继承自 `QGraphicsSceneEvent`。常在 `QGraphicsItem::contextMenuEvent()` 中处理。

它提供 item、scene、screen 坐标，以及 `reason()`。显示 `QMenu` 时通常使用 `screenPos()`，因为菜单需要全局屏幕坐标。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `pos()` | 事件在 item 坐标中的位置。 |
| `scenePos()` | 事件在场景坐标中的位置。 |
| `screenPos()` | 事件在屏幕坐标中的位置，弹菜单常用。 |
| `modifiers()` | 触发时的键盘修饰键。 |
| `reason()` | 触发原因：鼠标、键盘或其他。 |
| `Reason::Mouse` | 鼠标触发的上下文菜单。 |
| `Reason::Keyboard` | 键盘触发的上下文菜单。 |
| `Reason::Other` | 其他平台原因。 |

## 4. 关键用法

```cpp
void NodeItem::contextMenuEvent(QGraphicsSceneContextMenuEvent *event)
{
    QMenu menu;
    menu.addAction("Rename", [this] { rename(); });
    menu.addAction("Delete", [this] { removeNode(); });
    menu.exec(event->screenPos());
    event->accept();
}
```

键盘触发时可以不依赖鼠标点，而是用 item 中心或当前选择位置决定菜单语义。

## 5. 使用场景

适合节点菜单、画布空白处菜单、端口操作、图形对象属性入口、场景内快捷命令。

如果菜单是整个 view 的，不依赖 item，放在 `QGraphicsView` 或外层 widget 处理也可以。

## 6. 常见坑与经验

弹出 `QMenu::exec()` 要用屏幕坐标，不是 scene 坐标。

不要假设上下文菜单都来自鼠标。键盘用户也应该能打开同样菜单。

item 菜单和 scene 空白菜单要区分。命中 item 时处理 item 命令，空白区域处理粘贴、全选、视图设置等命令。
