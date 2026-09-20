# QGraphicsSceneEvent

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsSceneEvent`

## 1. 先建立直觉

`QGraphicsSceneEvent` 是 Graphics View 场景事件的基类。鼠标、悬停、拖放、滚轮、上下文菜单、帮助、移动、调整大小等事件都从它派生。

它和普通 `QMouseEvent` 最大区别是坐标体系更多：item 坐标、scene 坐标、screen 坐标，以及事件来自哪个 `QWidget` viewport。

## 2. 类说明

`QGraphicsSceneEvent` 继承自 `QEvent`。它通常由 Qt 创建并传给 `QGraphicsItem` 的事件处理函数，例如 `mousePressEvent()`、`hoverMoveEvent()`、`contextMenuEvent()`。

事件对象生命周期只在处理期间有效，不应保存指针。需要持久状态时，把坐标或业务信息复制出来。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `widget()` | 返回产生该事件的 viewport widget，可能为空。 |
| `QGraphicsSceneMouseEvent` | 鼠标按下、移动、释放、双击事件。 |
| `QGraphicsSceneHoverEvent` | 鼠标悬停进入、移动、离开事件。 |
| `QGraphicsSceneContextMenuEvent` | 上下文菜单事件。 |
| `QGraphicsSceneDragDropEvent` | 拖放进入、移动、离开、释放事件。 |
| `QGraphicsSceneWheelEvent` | 滚轮事件。 |
| `QGraphicsSceneHelpEvent` | tooltip / What's This 帮助事件。 |
| `QGraphicsSceneMoveEvent` | `QGraphicsWidget` 移动事件。 |
| `QGraphicsSceneResizeEvent` | `QGraphicsWidget` 调整大小事件。 |

## 4. 关键用法

```cpp
void NodeItem::hoverMoveEvent(QGraphicsSceneHoverEvent *event)
{
    const QPointF p = event->pos();       // item 坐标
    const QPointF s = event->scenePos();  // scene 坐标
    Q_UNUSED(p);
    Q_UNUSED(s);
}
```

如果要显示全局菜单：

```cpp
menu.exec(event->screenPos());
```

## 5. 使用场景

适合自定义 `QGraphicsItem` / `QGraphicsWidget` 交互：拖拽节点、连接端口、悬停高亮、场景菜单、滚轮缩放、拖放素材。

普通 QWidget 事件不要用它；它只属于 Graphics View 事件分发。

## 6. 常见坑与经验

坐标系一定要看函数名。`pos()` 通常是 item 坐标，`scenePos()` 是场景坐标，`screenPos()` 是屏幕坐标。

事件指针不要保存。保存 `QPointF`、按钮状态或自己的命令对象即可。

多个 view 观察同一个 scene 时，`widget()` 可以帮助你知道事件从哪个视图来。
