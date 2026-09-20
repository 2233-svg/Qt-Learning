# QPainterPath::Element：路径内部元素流中的一个坐标与类型

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPainterPath>`  
> 所属模块：`Qt6::Gui`  
> 所属类型：`QPainterPath`

`QPainterPath::Element` 是 `QPainterPath` 内部元素序列中的一个轻量值。它公开保存坐标 `x`、`y` 与类型 `type`，由 `QPainterPath::elementAt()` 返回，用于检查或分析路径如何由移动、直线和曲线组成。

它不是独立的可编辑路径节点，也不持有对原 `QPainterPath` 的引用。`elementAt()` 返回的是副本，修改副本字段不会修改路径；要更改已有元素的位置，只能调用 `QPainterPath::setElementPositionAt()`。

## 它解决的问题

大多数绘制、命中测试和布尔运算直接操作 `QPainterPath` 即可。但在矢量编辑器、SVG/自定义路径导入导出、路径调试和几何分析中，需要查看路径的底层指令流：

- 新子路径从哪里开始；
- 某段是直线还是曲线；
- 曲线控制点和终点在哪；
- 导入的路径是否形成了预期元素序列。

`Element` 提供了这个只读检查入口。它和 `elementCount()`、`elementAt()` 一起使用。

## 实际使用场景

### 1. 列出路径中移动和直线元素

```cpp
for (int i = 0; i < path.elementCount(); ++i) {
    const QPainterPath::Element element = path.elementAt(i);

    if (element.isMoveTo())
        qDebug() << "move to" << element.x << element.y;
    else if (element.isLineTo())
        qDebug() << "line to" << element.x << element.y;
}
```

此类遍历适合调试 `moveTo()`、`lineTo()` 或导入后的轮廓结构。曲线不能仅靠这两种判断处理，见下节。

### 2. 以三个元素为一组读取三次贝塞尔曲线

```cpp
for (int i = 0; i < path.elementCount();) {
    const QPainterPath::Element element = path.elementAt(i);

    if (element.isMoveTo()) {
        consumeMoveTo(QPointF(element));
        ++i;
    } else if (element.isLineTo()) {
        consumeLineTo(QPointF(element));
        ++i;
    } else if (element.isCurveTo()
               && i + 2 < path.elementCount()) {
        const auto control2 = path.elementAt(i + 1);
        const auto endPoint = path.elementAt(i + 2);

        if (control2.type != QPainterPath::CurveToDataElement
            || endPoint.type != QPainterPath::CurveToDataElement) {
            reportMalformedPath();
            break;
        }

        consumeCubicTo(QPointF(element),
                       QPointF(control2),
                       QPointF(endPoint));
        i += 3;
    } else {
        reportMalformedPath();
        break;
    }
}
```

一次 `cubicTo(c1, c2, end)` 在元素流中由三个连续元素表示：第一个是 `CurveToElement`，保存第一个控制点；后两个是 `CurveToDataElement`，分别保存第二个控制点和终点。二次曲线也会以曲线元素形式存储。遍历时不能把每个 `CurveToDataElement` 误认为独立线段。

### 3. 仅调整既有元素坐标

```cpp
for (int i = 0; i < path.elementCount(); ++i) {
    const auto element = path.elementAt(i);
    path.setElementPositionAt(i, element.x + 20.0, element.y);
}
```

这会平移每个存储点，包括曲线控制点与终点。它是低层编辑手段：如果只想平移整个路径，应优先使用 `translate()` 或 `translated()`；如果要改变结构、元素类型或子路径数量，应重建路径。

## 元素类型与路径语义

| `QPainterPath::ElementType` | 含义 | 通常由什么产生 |
| --- | --- | --- |
| `MoveToElement` | 开始一个新子路径，移动 current position，不画线。 | `moveTo()`。 |
| `LineToElement` | 从当前位置连接一条直线到该元素坐标。 | `lineTo()`。 |
| `CurveToElement` | 曲线记录的第一个元素。 | `cubicTo()`、`quadTo()`。 |
| `CurveToDataElement` | 补充曲线描述所需的后续数据。 | 紧跟在 `CurveToElement` 后。 |

`addRect()`、`addEllipse()`、`addText()`、`addPath()` 等方便函数最终也会把结果加入为由 `moveTo()`、`lineTo()` 和 `cubicTo()` 构成的元素集合。因此元素遍历能看到“路径如何实现”，而不一定保留调用者最初使用的高层 API 名称。

## 核心语义与边界

### `x`、`y` 是元素存储坐标，不总是图形终点

对于 `MoveToElement` 和 `LineToElement`，`x`、`y` 是新当前位置。对于曲线三元组：

1. `CurveToElement` 的坐标是第一个控制点；
2. 第一个 `CurveToDataElement` 的坐标是第二个控制点；
3. 第二个 `CurveToDataElement` 的坐标才是曲线终点。

因此，“遍历所有元素的坐标”不等于“遍历所有可见顶点”。若要拿曲线的真实边界，使用 `controlPointRect()` 或 `boundingRect()`；若要采样曲线，使用 `pointAtPercent()` 等高层 API。

### 三个布尔辅助函数的范围

- `isMoveTo()` 等价于 `type == MoveToElement`；
- `isLineTo()` 等价于 `type == LineToElement`；
- `isCurveTo()` 等价于 `type == CurveToElement`。

特别注意：对于 `CurveToDataElement`，这三个函数都返回 `false`。它不是一条独立曲线的开头，而是前一个曲线记录的一部分。

### 返回值是副本

```cpp
auto element = path.elementAt(0);
element.x = 100; // 只改局部副本
```

这不会改动 `path`。应使用：

```cpp
path.setElementPositionAt(0, 100, element.y);
```

`setElementPositionAt()` 只能更新坐标，不能把直线元素改成曲线元素，也不能插入或删除元素。此类结构变化应该通过新的 `QPainterPath` 和 `moveTo()` / `lineTo()` / `cubicTo()` 构建。

### 相等比较不是严格的浮点字节比较

`operator==` 要求元素类型相同，并使用 Qt 的模糊浮点比较判断坐标位置；`operator!=` 是其否定。它适合判断几何上近似相同的元素，不适合作为精确序列化校验、哈希键或需要逐 bit 复现的格式验证。

### 生命周期与线程

`Element` 是普通轻量值，不依赖事件循环或窗口。它从 `QPainterPath` 取出后可安全按值保存。

但如果路径仍由其他线程或 GUI 交互代码修改，应先复制稳定的 `QPainterPath` 快照，再遍历其元素。不要在一个线程调用 `setElementPositionAt()` 时让另一个线程读取同一个路径的元素序列。

## 常见错误

### 将 `CurveToDataElement` 当成异常元素而跳过

这样会丢掉曲线的第二控制点和终点。遇到 `CurveToElement` 时应检查并整体消费后面两个数据元素。

### 只修改 `elementAt()` 的返回对象

返回的是副本，原路径不会变化。需要改坐标时用 `setElementPositionAt()`。

### 用元素坐标直接计算可见边界

曲线控制点可能落在可见曲线外；直接包围所有元素会得到控制点包围盒，而不是精确绘制边界。按需求选择 `controlPointRect()` 或 `boundingRect()`。

### 重建曲线时遗漏 current position

元素流里的曲线描述依赖此前的 current position。导出或重建时必须按原顺序处理 `MoveToElement`、`LineToElement` 与曲线三元组，而不能孤立地解释每个元素。

## API 速查表

### 公共字段

| API | 说明 | 使用时重点 |
| --- | --- | --- |
| `qreal x` | 元素位置的 X 坐标。 | 从 `elementAt()` 取得时是副本字段；曲线中可能是控制点 X。 |
| `qreal y` | 元素位置的 Y 坐标。 | 从 `elementAt()` 取得时是副本字段；曲线中可能是控制点 Y。 |
| `QPainterPath::ElementType type` | 元素类型。 | 先根据它或三个判定函数决定如何消费元素。 |

### 成员函数

| API | 说明 | 使用时重点 |
| --- | --- | --- |
| `isMoveTo() const` | 是否为 `MoveToElement`。 | 表示新子路径开始；不产生可见线段。 |
| `isLineTo() const` | 是否为 `LineToElement`。 | 当前元素坐标是该直线终点。 |
| `isCurveTo() const` | 是否为 `CurveToElement`。 | 只识别曲线三元组的第一个元素；随后读取两个 `CurveToDataElement`。 |
| `operator QPointF() const` | 把当前 `x`、`y` 转为 `QPointF`。 | 方便传递坐标；不解释它在曲线中的角色。 |
| `operator==(const Element &other) const` | 比较类型和近似坐标是否相等。 | 浮点比较是模糊的，不是序列化级精确比较。 |
| `operator!=(const Element &other) const` | `operator==` 的否定。 | 用于元素差异检测。 |

### 获取和修改元素的 `QPainterPath` API

| API | 说明 | 使用时重点 |
| --- | --- | --- |
| `elementCount() const` | 返回路径元素数量。 | 遍历上界；曲线至少按三个元素处理。 |
| `elementAt(int index) const` | 返回指定下标的 `Element` 副本。 | 先检查下标范围；返回对象不连接原路径。 |
| `setElementPositionAt(int index, qreal x, qreal y)` | 修改现有元素的坐标。 | 只改位置，不能改类型或结构；曲线控制点和终点都会受影响。 |

一句话记忆：`QPainterPath::Element` 是路径指令流的一格数据；直线可逐个读，曲线必须从 `CurveToElement` 开始连同后面两个数据元素一起读。
