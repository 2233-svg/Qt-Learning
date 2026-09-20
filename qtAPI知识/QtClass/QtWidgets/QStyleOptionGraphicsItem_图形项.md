# Qt QStyleOptionGraphicsItem 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QStyleOptionGraphicsItem>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QStyleOption -> QStyleOptionGraphicsItem`  
> 定位：Graphics View 在调用 `QGraphicsItem::paint()` 时传入的绘制状态与性能提示

## 1. 它解决的是“这一帧要画多少细节”

`QStyleOptionGraphicsItem` 是 `QGraphicsItem::paint()` 的第二个参数类型。它不是图元，不管理几何、事件、层级或场景；它描述当前绘制请求的状态，尤其是可见区域和缩放级别。

```cpp
void NodeItem::paint(QPainter *painter,
                     const QStyleOptionGraphicsItem *option,
                     QWidget *widget)
{
    // option 是本次调用的上下文，不是持久业务状态。
}
```

Graphics View 的基本调用链：

```text
QGraphicsScene / QGraphicsView
  └─ 判断哪些 item 需要重绘
       └─ QGraphicsItem::paint(painter, option, widget)
            ├─ option->state：选中、禁用、焦点等状态
            ├─ option->exposedRect：局部坐标中的可见区域提示
            └─ world transform：可用于推导 LOD
```

它适合解决两个性能问题：

- 一个很大的图元只有小块区域暴露时，不必计算或绘制整个图元的细节；
- 视图缩放很小时，不必画文字、锚点、阴影、复杂路径等肉眼看不见的细节。

它不替代：

- `boundingRect()`：图元的几何边界与场景索引依据；
- `shape()`：精确命中和碰撞形状；
- `update()`：请求未来重绘；
- `QGraphicsItem` 的持久状态。

## 2. `paint()` 中坐标系必须先想清楚

`QGraphicsItem::paint()` 在**图元局部坐标**中工作：

```text
option->exposedRect    -> 图元局部坐标
boundingRect()         -> 图元局部坐标
painter 的 worldTransform -> 局部坐标到设备坐标的映射
```

因此不要拿 `exposedRect` 直接和 `sceneBoundingRect()` 比较，也不要把 view 的像素坐标当成 item 坐标。最可靠的基线是：

```cpp
const QRectF itemBounds = boundingRect();
const QRectF visiblePart = option->exposedRect;
```

`boundingRect()` 必须覆盖所有可能绘制的像素，包括描边向外伸出的半个 pen 宽度。Qt 文档明确说明 `QGraphicsView` 不会替你把 painter 裁剪在 `boundingRect()` 内；一旦画出边界，会留下渲染残影或造成重绘错误。

## 3. `exposedRect`：只把可见区域当作性能提示

`exposedRect` 表示当前暴露、需要重绘的区域，单位是 item 坐标。

```text
图元 boundingRect: 0,0,2000,2000
本次 exposedRect: 950,950,100,100

可以只重算和绘制中央 100 x 100 区域附近的昂贵细节
```

适合的实际场景：

- 大型网格图元仅绘制当前视口内的格线与标签；
- 地图、流程图或波形图在局部更新时跳过远离暴露区域的元素；
- 一个图元内部有很多 decoration，只画与 `exposedRect` 相交的部分。

```cpp
void GridItem::paint(QPainter *painter,
                     const QStyleOptionGraphicsItem *option,
                     QWidget *)
{
    const QRectF area = option->exposedRect.intersected(boundingRect());

    const int firstColumn = qFloor(area.left() / m_cellWidth);
    const int lastColumn = qCeil(area.right() / m_cellWidth);

    for (int column = firstColumn; column <= lastColumn; ++column)
        drawColumn(painter, column);
}
```

### 3.1 先启用 `ItemUsesExtendedStyleOption`

想获得细粒度的 `exposedRect`，必须在图元上启用：

```cpp
setFlag(QGraphicsItem::ItemUsesExtendedStyleOption, true);
```

Qt 文档说明：默认 `exposedRect` 为 `boundingRect()`；设置这个 flag 后，Graphics View 才会为 style option 准备更细粒度的值。类页也强调该成员只为使用此 flag 的图元初始化。因此最安全的规则是：

```text
没有 ItemUsesExtendedStyleOption
  -> 不要依赖 exposedRect 做局部裁剪优化，按整个 boundingRect 绘制。

启用 ItemUsesExtendedStyleOption
  -> 可以将 exposedRect 作为局部绘制的性能提示。
```

这个 flag 不是白送的性能开关。它让框架计算更精确的暴露区域，而图元也必须真的利用它来减少昂贵工作，才可能有收益。

### 3.2 `exposedRect` 不是自动裁剪

即使 `exposedRect` 很小，painter 也不保证被裁剪到这个区域。它告诉你“哪些部分值得画”，而不是强制限制你的绘制。

若你的绘制本身会越过 `boundingRect()`，问题仍然存在；应修正 `boundingRect()` 或在自己的绘制中设置合理 clip。不要误以为检查 exposed rect 就能掩盖越界绘制。

## 4. `levelOfDetailFromTransform()`：按缩放层级画不同复杂度

`levelOfDetailFromTransform(const QTransform &worldTransform)` 是静态函数，用 painter 的 world transform 推导一个 LOD 值：

```text
未缩放：LOD = 1
缩小到 1:2：LOD = 0.5
放大到 2:1：LOD = 2
```

它的语义不是简单读取 `m11()`。函数返回的是“单位矩形经 world transform 映射后，宽和高中的较大值”，所以旋转、剪切和非等比缩放下也能给出适合复杂度判断的量级。

在 `paint()` 中常见写法：

```cpp
void NodeItem::paint(QPainter *painter,
                     const QStyleOptionGraphicsItem *option,
                     QWidget *)
{
    const qreal lod =
        QStyleOptionGraphicsItem::levelOfDetailFromTransform(
            painter->worldTransform());

    drawNodeBody(painter);

    if (lod >= 0.35)
        drawPorts(painter);
    if (lod >= 0.8)
        drawLabel(painter);
    if (lod >= 2.0)
        drawFineGrid(painter);

    if (option->state & QStyle::State_Selected)
        drawSelectionOutline(painter);
}
```

阈值 `0.35`、`0.8`、`2.0` 只是示例，应按图元大小、字体可读性、设备像素比和实际性能测试决定。LOD 用来减少不必要细节，不应改变图元的基本形状、命中区域或业务语义。

## 5. `state` 仍然重要：选择态不靠自建布尔变量

虽然本类只新增 `exposedRect`，它继承的 `QStyleOption::state` 会携带常见绘制状态，例如选中、启用、焦点、鼠标悬停等。

```cpp
const bool selected = option->state & QStyle::State_Selected;
const bool enabled = option->state & QStyle::State_Enabled;
```

这份状态是框架在本次绘制时给出的快照。若图元要持久改变选择或启用状态，应调用 `setSelected()`、`setEnabled()`；不要试图通过改 option 的 `state` 回写图元。

## 6. 与 `boundingRect()`、`shape()` 的三角关系

| 成员/概念 | 解决什么问题 | 关键约束 |
| --- | --- | --- |
| `boundingRect()` | 告诉场景图元大致占多大区域，用于索引、裁剪判断和重绘范围 | 必须覆盖所有绘制，几何改变前调用 `prepareGeometryChange()` |
| `shape()` | 提供更准确的命中与碰撞形状 | 复杂路径可能较慢 |
| `option->exposedRect` | 告诉 `paint()` 当前哪一块可能需要重绘 | 是性能提示；局部优化应启用 `ItemUsesExtendedStyleOption` |
| LOD | 告诉 `paint()` 当前缩放下细节是否值得画 | 不应破坏基本外形和交互语义 |

不要为了让绘制少一点就缩小 `boundingRect()`。这会破坏场景索引和重绘正确性。正确做法是保持准确边界，再用 exposed rect 与 LOD 决定内部细节。

## 7. 常见错误

### 7.1 未启用扩展 style option 却用 exposed rect 跳过绘制

症状：平移或局部更新后，有些区域没有被画出来。

原因：把 `exposedRect` 当成始终精确的部分重绘区域。

处理：只有设置 `ItemUsesExtendedStyleOption` 后才做精细局部优化；否则按 `boundingRect()` 绘制。

### 7.2 把 exposed rect 当成 scene 坐标

症状：图元移动到场景其他位置后，局部 culling 逻辑失效。

原因：`exposedRect` 属于 item 坐标，不是 scene 或 viewport 坐标。

处理：与 `boundingRect()`、图元内部元素坐标直接比较；跨坐标系时显式 map。

### 7.3 只根据 LOD 不画全部内容，却没有请求 update

症状：缩放后文字或细节没有恢复。

原因：图元在相同状态下输出不同画面，却没有让框架获知需要重绘。

处理：缩放通常会触发 view 重绘；若自身状态影响细节，改变状态后调用 `update()`，并保证未调用 update 的连续 `paint()` 输出一致。

### 7.4 绘制越过 boundingRect

症状：移动、缩放或删除图元后留下残影。

原因：Graphics View 不会自动裁剪 painter 到 `boundingRect()`。

处理：扩大准确的 `boundingRect()`，变化前调用 `prepareGeometryChange()`，并约束所有绘制在边界内。

## API 速查表
以下列出 Qt 6.11.1 类文档中 `QStyleOptionGraphicsItem` 直接声明的类型、构造函数、公开字段和静态函数。继承自 `QStyleOption` 的 `state`、`rect`、`palette` 等通用状态不在此表内。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举常量 | `StyleOptionType::Type = SO_GraphicsItem` | 标识这是 Graphics Item 的 style option。 | 供 `qstyleoption_cast()` 和框架内部识别。 |
| 枚举常量 | `StyleOptionVersion::Version = 1` | 标识本结构版本。 | 普通图元绘制不需手动检查。 |
| 构造 | `QStyleOptionGraphicsItem()` | 创建一份图元绘制状态。 | 通常由 Graphics View 传入 `paint()`；很少需要业务代码自行创建。 |
| 构造 | `QStyleOptionGraphicsItem(const QStyleOptionGraphicsItem &other)` | 复制一份图元绘制状态。 | 是值复制，不拥有 `QGraphicsItem` 或 scene。 |
| 静态函数 | `levelOfDetailFromTransform(const QTransform &worldTransform)` | 从 world transform 计算当前缩放下的细节等级。 | 用它分级绘制；旋转与非等比缩放下不要手算单一缩放因子。 |
| 公开字段 | `QRectF exposedRect` | 保存本次需重绘的暴露区域，坐标在 item 本地。 | 要做精细局部优化时设置 `ItemUsesExtendedStyleOption`；它不是自动 clip。 |

## 9. 一句话总结

`QStyleOptionGraphicsItem` 把“本次画到哪里、当前缩放有多大、图元处于什么状态”交给 `QGraphicsItem::paint()`；准确的 `boundingRect()` 保证正确性，`exposedRect` 和 LOD 则在启用并正确使用时换来性能。
