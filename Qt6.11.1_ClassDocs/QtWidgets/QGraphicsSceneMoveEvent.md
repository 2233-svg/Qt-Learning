# QGraphicsSceneMoveEvent

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsSceneMoveEvent`

## 1. 先建立直觉

`QGraphicsSceneMoveEvent` 表示 `QGraphicsWidget` 在场景中移动了。它提供旧位置和新位置，便于同步连线、吸附、布局外状态或辅助 UI。

它不是鼠标拖动事件。鼠标拖动可能导致移动，但这个事件关注结果：对象的位置从哪里变到哪里。

## 2. 类说明

`QGraphicsSceneMoveEvent` 继承自 `QGraphicsSceneEvent`。通常在 `QGraphicsWidget::moveEvent()` 中收到。

如果是普通 `QGraphicsItem`，更常用 `itemChange(ItemPositionChange/HasChanged)` 监听位置变化；move event 主要面向 graphics widget。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `oldPos()` | 移动前位置。 |
| `newPos()` | 移动后位置。 |
| `QGraphicsWidget::moveEvent()` | 接收该事件的常用入口。 |
| `QGraphicsItem::itemChange()` | 普通 item 监听位置变化的替代入口。 |

## 4. 关键用法

```cpp
void PanelWidget::moveEvent(QGraphicsSceneMoveEvent *event)
{
    updateAttachedConnectors(event->oldPos(), event->newPos());
    QGraphicsWidget::moveEvent(event);
}
```

只关心位移量：

```cpp
const QPointF delta = event->newPos() - event->oldPos();
```

## 5. 使用场景

适合场景内窗口、浮动面板、图形 widget 移动后同步附属对象、保存布局位置、更新连接线。

普通 item 的拖动限制和吸附，很多时候放在 `itemChange()` 更早、更可控。

## 6. 常见坑与经验

不要在 move event 中无限触发新的移动，否则容易形成递归更新。需要修正位置时要小心条件。

移动事件是结果通知，不是交互开始/结束通知。拖动期间的状态管理应结合鼠标事件或 item change。

如果 item 在布局中，手动移动可能被布局下一次计算覆盖。
