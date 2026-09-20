# QGraphicsSceneResizeEvent

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsSceneResizeEvent`

## 1. 先建立直觉

`QGraphicsSceneResizeEvent` 表示 `QGraphicsWidget` 的尺寸发生变化。它提供旧尺寸和新尺寸，适合在场景内 widget 调整大小后重新排布内部细节。

它对应的是 Graphics View 世界，不是普通 `QResizeEvent`。普通 QWidget resize 用 `QResizeEvent`；`QGraphicsWidget` resize 用这个事件。

## 2. 类说明

`QGraphicsSceneResizeEvent` 继承自 `QGraphicsSceneEvent`。通常在 `QGraphicsWidget::resizeEvent()` 中收到。

图形布局系统、手动 `resize()`、父布局重新分配空间，都可能导致该事件出现。处理时要区分“响应尺寸变化”和“主动再改尺寸”。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `oldSize()` | 调整前尺寸。 |
| `newSize()` | 调整后尺寸。 |
| `QGraphicsWidget::resizeEvent()` | 接收该事件的常用入口。 |
| `QGraphicsWidget::setGeometry()` | 可能触发尺寸变化。 |
| `QGraphicsLayout` | 父布局可能驱动 graphics widget resize。 |

## 4. 关键用法

```cpp
void NodePanel::resizeEvent(QGraphicsSceneResizeEvent *event)
{
    rebuildPortPositions(event->newSize());
    QGraphicsWidget::resizeEvent(event);
}
```

根据尺寸调整子 item：

```cpp
titleBar->setGeometry(QRectF(0, 0, event->newSize().width(), 24));
```

## 5. 使用场景

适合场景内面板、节点、浮动窗口、自定义 `QGraphicsWidget` 中根据尺寸重排子 item、同步连接线端点、刷新背景路径。

如果只是普通 item 的 `boundingRect()` 变化，自定义 item 的几何管理和 `prepareGeometryChange()` 更重要。

## 6. 常见坑与经验

不要在 resize event 里无条件调用 `resize()`，容易递归。需要约束尺寸时，优先设置 minimum/preferred/maximum size。

布局驱动的 resize 不一定来自用户拖拽。业务逻辑不要假设每次 resize 都是用户操作。

尺寸变化后，如果自绘缓存依赖尺寸，要同步失效缓存并 `update()`。
