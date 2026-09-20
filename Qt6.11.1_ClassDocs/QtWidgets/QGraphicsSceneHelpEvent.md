# QGraphicsSceneHelpEvent

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsSceneHelpEvent`

## 1. 先建立直觉

`QGraphicsSceneHelpEvent` 是 Graphics View 中的帮助事件，主要服务 tooltip 和 What's This。它告诉 item 用户在哪个位置请求帮助。

它不是弹窗本身，而是帮助系统传来的“请在这里解释一下”的事件。

## 2. 类说明

`QGraphicsSceneHelpEvent` 继承自 `QGraphicsSceneEvent`。它提供 scene 和 screen 坐标。item 可以根据位置显示不同提示。

简单场景中，直接给 item 设置 tooltip 就够；复杂 item 中，可在 help event 里按子区域决定提示内容。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `scenePos()` | 帮助请求发生的场景坐标。 |
| `screenPos()` | 帮助请求发生的屏幕坐标，显示 tooltip 常用。 |
| `QGraphicsItem::setToolTip()` | 简单 tooltip 的常用入口。 |
| `QToolTip::showText()` | 自定义显示 tooltip。 |
| `QWhatsThis` | 更详细的“这是什么？”帮助机制。 |

## 4. 关键用法

```cpp
void NodeItem::helpEvent(QGraphicsSceneHelpEvent *event)
{
    const QString text = helpForPortAt(mapFromScene(event->scenePos()));
    if (!text.isEmpty())
        QToolTip::showText(event->screenPos(), text);
    else
        QGraphicsItem::helpEvent(event);
}
```

## 5. 使用场景

适合复杂节点端口提示、图形对象局部说明、流程图元素解释、画布工具帮助。

简单固定提示优先用 `setToolTip()`，不用为每个 item 写事件处理。

## 6. 常见坑与经验

显示 tooltip 用 screen 坐标；做命中测试通常先把 scene 坐标映射到 item 坐标。

帮助文本要短。tooltip 解释即时问题，长文档应跳到帮助页或 What's This。

不要在 help event 中做昂贵查询。鼠标悬停触发帮助时，界面应该保持轻快。
