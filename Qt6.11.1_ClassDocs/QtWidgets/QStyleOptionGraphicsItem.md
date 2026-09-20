# QStyleOptionGraphicsItem

> Qt 6.11.1 · Qt Widgets · 来自 `QStyleOptionGraphicsItem`

## 1. 先建立直觉

`QStyleOptionGraphicsItem` 是 `QGraphicsItem::paint()` 收到的绘制上下文参数。它告诉 item 当前暴露区域、状态、细节级别等信息。

它不是传统 widget style option，虽然名字里也有 StyleOption。它服务 Graphics View item 绘制。

## 2. 类说明

`QStyleOptionGraphicsItem` 继承自 `QStyleOption`。最常用字段是 `exposedRect`，表示需要重绘的 item 局部区域。静态函数 `levelOfDetailFromTransform()` 可以根据 view transform 判断当前缩放细节。

大场景 item 可以根据细节级别决定画完整内容、简化内容还是只画占位。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `exposedRect` | 当前需要重绘的 item 局部区域。 |
| `levelOfDetailFromTransform(QTransform)` | 根据变换计算细节级别。 |
| `state` | item 绘制状态，如 selected、has focus 等。 |
| `rect` | 绘制矩形。 |
| `QGraphicsItem::paint()` | 接收该 option 的主要入口。 |

## 4. 关键用法

```cpp
void NodeItem::paint(QPainter *p, const QStyleOptionGraphicsItem *option, QWidget *)
{
    const qreal lod = QStyleOptionGraphicsItem::levelOfDetailFromTransform(
        p->worldTransform());

    if (lod < 0.3) {
        p->drawRect(boundingRect());
        return;
    }

    drawFullDetails(p, option->exposedRect);
}
```

## 5. 使用场景

适合自定义 `QGraphicsItem`、大场景性能优化、缩放时简化绘制、只重绘暴露区域。

普通 widget 绘制不用它；widget 用 `QStyleOption` 系列。

## 6. 常见坑与经验

`exposedRect` 是优化提示，不应该改变绘制语义。即使只画暴露区域，结果也要和完整绘制一致。

LOD 很适合大图元。缩小时少画文字和细节，能显著改善性能和可读性。

不要在 paint 中修改 item 几何或场景结构。绘制函数应尽量无副作用。
