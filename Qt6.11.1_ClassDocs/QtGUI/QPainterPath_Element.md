# QPainterPath::Element

> Qt 6.11.1 · Qt GUI · 来自 `QPainterPath::Element`

## 1. 先建立直觉

`QPainterPath::Element` 是 `QPainterPath` 内部路径命令的一个节点。它记录一个坐标点和一个类型：移动到、连线到、曲线开始，或者曲线控制数据。你通常不会手动创建它，而是在调试、分析、编辑路径时通过 `QPainterPath::elementAt()` 读取。

最重要的细节是曲线不是一个元素就能完整表达。三次贝塞尔曲线由一个 `CurveToElement` 加两个紧随其后的 `CurveToDataElement` 组成；二次曲线最终也会被路径表示成内部曲线元素。遍历元素时如果只把每个元素当成独立点，会误读曲线结构。

## 2. 类说明

- 头文件：`#include <QPainterPath>`
- 所属类：`QPainterPath`
- 类型性质：公开结构式元素，包含 `x`、`y`、`type`
- 主要用途：检查、遍历、修改路径元素
- 获取入口：`QPainterPath::elementAt(int index)`

`Element` 是路径序列的低层视图。对于普通绘制，用 `moveTo()`、`lineTo()`、`cubicTo()`、`addRect()`、`addEllipse()` 这些高层 API 更安全；只有当你需要路径编辑器、导出器、命中调试或自定义几何分析时，才需要直接看元素。

## 3. API 速查

| API / 字段 | 作用 |
| --- | --- |
| `x` / `y` | 元素携带的坐标。 |
| `type` | 元素类型：`MoveToElement`、`LineToElement`、`CurveToElement`、`CurveToDataElement`。 |
| `isMoveTo()` | 判断该元素是否开始新的子路径。 |
| `isLineTo()` | 判断该元素是否表示直线终点。 |
| `isCurveTo()` | 判断该元素是否是曲线命令的起始元素。 |
| `operator QPointF()` | 把元素当作坐标点使用。 |
| `operator==` / `operator!=` | 比较元素的类型和坐标是否相同。 |

## 4. 关键用法

### 遍历路径元素

```cpp
for (int i = 0; i < path.elementCount(); ++i) {
    const QPainterPath::Element e = path.elementAt(i);

    if (e.isMoveTo()) {
        startSubpath(QPointF(e));
    } else if (e.isLineTo()) {
        addLine(QPointF(e));
    } else if (e.isCurveTo()) {
        const auto c1 = QPointF(e);
        const auto c2 = QPointF(path.elementAt(i + 1));
        const auto end = QPointF(path.elementAt(i + 2));
        addCubic(c1, c2, end);
        i += 2;
    }
}
```

遍历曲线时要一次消费三个元素。`CurveToDataElement` 本身不表示新的绘制命令，它只是前一个 `CurveToElement` 的补充数据。

### 调整某个元素坐标

```cpp
if (index >= 0 && index < path.elementCount())
    path.setElementPositionAt(index, newX, newY);
```

路径编辑器可以用这种方式拖动锚点或控制点。修改前要确认该 index 是否属于曲线控制点，避免把用户以为的“端点”改成了控制柄。

## 5. 使用场景

- 路径编辑器：显示锚点、控制点、拖动曲线手柄。
- SVG/自定义格式导出：把 `QPainterPath` 转成外部路径命令。
- 几何调试：检查 `addEllipse()`、`addText()` 展开后实际产生了哪些元素。
- 命中测试辅助：为复杂路径构造可视化调试点。
- 动画：对路径节点做插值或局部变形。

## 6. 常见坑与经验

- **曲线元素是成组出现的。** `CurveToElement` 后面必须跟两个 `CurveToDataElement`，遍历时要跳过补充数据。
- **`operator QPointF()` 只给坐标，不给语义。** 坐标点是 move、line 还是 curve 控制点，要继续看 `type`。
- **便利图形会展开成元素序列。** `addRect()`、`addEllipse()`、`addText()` 都会变成 move/line/curve 组合，不保留“这是一个矩形”的原始语义。
- **直接改元素容易破坏路径。** 特别是曲线三元组和闭合子路径，编辑时要维护命令结构。
- **元素顺序就是绘制顺序。** 子路径之间不会自动连线，除非源路径里有明确的 line 或 connect 操作。

## 7. 知识点覆盖

- `QPainterPath` 的命令序列模型
- `MoveToElement`、`LineToElement`、`CurveToElement`、`CurveToDataElement` 的区别
- 三次贝塞尔曲线在元素数组中的存储方式
- 路径遍历、导出、编辑和调试
- 元素坐标与命令语义的分离
