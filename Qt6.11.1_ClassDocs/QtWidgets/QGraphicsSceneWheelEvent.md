# QGraphicsSceneWheelEvent

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsSceneWheelEvent`

## 1. 先建立直觉

`QGraphicsSceneWheelEvent` 是 Graphics View 中传给 item 的滚轮事件。它常用于在 item 上滚动数值、缩放局部内容、切换层级或把滚轮交给父视图处理。

滚轮既可能来自传统鼠标滚轮，也可能来自触控板。触控板滚动更连续，交互设计要避免只按“每次 120”这种老式鼠标刻度思路写死。

## 2. 类说明

`QGraphicsSceneWheelEvent` 继承自 `QGraphicsSceneEvent`。它提供 item/scene/screen 坐标、滚轮 delta、方向、按钮和修饰键。

如果滚轮用于 view 缩放，通常在 `QGraphicsView::wheelEvent()` 中处理更合适；如果滚轮只影响某个 item，比如节点内部参数，则在 item 事件中处理。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `pos()` / `scenePos()` / `screenPos()` | 滚轮发生位置的 item、scene、screen 坐标。 |
| `delta()` | 滚轮增量，传统鼠标常见一步 120。 |
| `orientation()` | 滚动方向，水平或垂直。 |
| `buttons()` | 事件发生时按下的鼠标按钮。 |
| `modifiers()` | 键盘修饰键，例如 Ctrl 缩放、Shift 横向滚动。 |

## 4. 关键用法

```cpp
void DialItem::wheelEvent(QGraphicsSceneWheelEvent *event)
{
    const int step = event->delta() > 0 ? 1 : -1;
    setValue(value() + step);
    event->accept();
}
```

带 Ctrl 时缩放，普通滚轮忽略给 view：

```cpp
if (event->modifiers() & Qt::ControlModifier) {
    zoomLocal(event->delta());
    event->accept();
} else {
    event->ignore();
}
```

## 5. 使用场景

适合场景 item 内部数值调整、局部缩放、图层切换、时间轴刻度调整、节点端口滚动选择。

整张画布缩放通常放在 view 层更统一，避免每个 item 都抢滚轮。

## 6. 常见坑与经验

不要无条件 accept 滚轮。item 不处理时应 ignore，让外层 view 或 scroll area 有机会滚动。

触控板滚动可能更细腻，硬编码大步进会显得突兀。可以累计 delta 或做平滑处理。

滚轮位置很有价值。缩放时围绕鼠标所在 scene 点，比围绕视图中心更符合用户预期。
