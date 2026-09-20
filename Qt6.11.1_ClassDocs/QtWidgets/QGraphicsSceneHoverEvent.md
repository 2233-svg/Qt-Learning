# QGraphicsSceneHoverEvent

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsSceneHoverEvent`

## 1. 先建立直觉

`QGraphicsSceneHoverEvent` 是鼠标在 item 上方移动但没有按下按钮时的事件。它用于悬停高亮、显示提示、改变光标、预览可连接端口。

默认 item 不一定接收 hover。需要调用 `setAcceptHoverEvents(true)`，Qt 才会把 hover enter/move/leave 事件送进来。

## 2. 类说明

`QGraphicsSceneHoverEvent` 继承自 `QGraphicsSceneEvent`。它提供当前位置、上一次位置，以及 scene/screen 坐标。

它通常进入 `hoverEnterEvent()`、`hoverMoveEvent()`、`hoverLeaveEvent()`。因为没有按钮按下，它适合轻量反馈，不适合执行重要命令。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `pos()` | 当前 item 坐标。 |
| `scenePos()` | 当前场景坐标。 |
| `screenPos()` | 当前屏幕坐标。 |
| `lastPos()` | 上一次 item 坐标。 |
| `lastScenePos()` | 上一次场景坐标。 |
| `lastScreenPos()` | 上一次屏幕坐标。 |
| `modifiers()` | 当前键盘修饰键。 |
| `QGraphicsItem::setAcceptHoverEvents(true)` | 让 item 接收 hover 事件。 |

## 4. 关键用法

```cpp
NodeItem::NodeItem()
{
    setAcceptHoverEvents(true);
}

void NodeItem::hoverEnterEvent(QGraphicsSceneHoverEvent *)
{
    hovered = true;
    update();
}

void NodeItem::hoverLeaveEvent(QGraphicsSceneHoverEvent *)
{
    hovered = false;
    update();
}
```

## 5. 使用场景

适合端口高亮、节点 hover 状态、连接预览、工具提示、光标变化、显示可拖拽控制柄。

触摸设备没有传统 hover。面向触摸优先的界面不要把关键功能只放在悬停里。

## 6. 常见坑与经验

忘记 `setAcceptHoverEvents(true)` 是最常见问题。

hover move 可能很频繁，里面不要做昂贵计算。复杂命中可以缓存，必要时节流。

悬停反馈应可有可无。用户没有 hover 能力时，界面仍应可理解、可操作。
