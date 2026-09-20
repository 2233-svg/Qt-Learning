# QPainterPathStroker

> Qt 6.11.1 · Qt GUI · 来自 `QPainterPathStroker`

## 1. 先建立直觉

`QPainterPathStroker` 的作用是把一条“没有面积的中心线路径”转换成“有面积的描边轮廓路径”。`QPainter::strokePath()` 是直接画描边；`QPainterPathStroker::createStroke()` 则把描边结果变成一个新的 `QPainterPath`，随后你可以填充、裁剪、命中测试或做布尔运算。

它适合回答这类问题：鼠标是否点中了这条 6 像素宽的曲线？一条道路的外轮廓是什么？虚线每段的端点要不要圆角？尖角处斜接要延伸多远？

## 2. 类说明

- 头文件：`#include <QPainterPathStroker>`
- CMake：`Qt6::Gui`
- 输入：一个 `QPainterPath`
- 输出：表示描边区域的可填充 `QPainterPath`
- 关键参数：宽度、端点样式、连接样式、虚线模式、斜接限制、曲线展平阈值

生成的路径应按填充区域使用，通常保持默认的 `Qt::WindingFill` 语义。它描述的是“描边覆盖的面积”，不是新的中心线。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `QPainterPathStroker()` | 创建默认描边器。 |
| `QPainterPathStroker(const QPen &pen)` | 从 `QPen` 提取宽度、端点、连接、虚线等描边设置。 |
| `createStroke(const QPainterPath &path)` | 生成表示描边轮廓的路径。 |
| `setWidth()` / `width()` | 设置描边宽度，轮廓大约向中心线两侧各扩展一半。 |
| `setCapStyle()` / `capStyle()` | 设置开放子路径端点样式：平头、方头、圆头。 |
| `setJoinStyle()` / `joinStyle()` | 设置折线连接处样式：斜接、圆角、斜 bevel 等。 |
| `setMiterLimit()` / `miterLimit()` | 限制尖角斜接延伸距离，只对 `MiterJoin` 有意义。 |
| `setDashPattern(Qt::PenStyle)` | 使用 Qt 预定义虚线样式。 |
| `setDashPattern(QList<qreal>)` | 自定义虚线/空白长度序列。 |
| `setDashOffset()` / `dashOffset()` | 控制虚线模式从路径上的哪个偏移开始。 |
| `setCurveThreshold()` / `curveThreshold()` | 控制曲线转轮廓时的展平精度。 |

## 4. 关键用法

### 给线条做精准命中区域

```cpp
QPainterPathStroker stroker;
stroker.setWidth(8.0);
stroker.setCapStyle(Qt::RoundCap);
stroker.setJoinStyle(Qt::RoundJoin);

const QPainterPath hitArea = stroker.createStroke(centerLine);
if (hitArea.contains(mousePos))
    selectRoad();
```

用路径的 `contains()` 直接测中心线通常没有意义，因为线没有面积。先 stroker，再 contains，才符合用户“点在线条附近也算选中”的直觉。

### 把描边区域用于布尔运算

```cpp
QPainterPathStroker stroker(QPen(Qt::black, 12, Qt::DashLine));
QPainterPath roadPaint = stroker.createStroke(roadCenterPath);
QPainterPath visible = roadPaint.intersected(viewportPath);
```

这里得到的是虚线每一段实际覆盖的区域。后续可以填充、裁剪、相交或相减。

## 5. 使用场景

- 图形编辑器：选中曲线、拖动线条、判断鼠标是否击中描边。
- 地图和 CAD：由中心线生成道路、管线、线路外轮廓。
- 自定义虚线：需要拿到虚线段几何而不只是绘制结果。
- 遮罩制作：把路径描边转换成 alpha 区域或裁剪区域。
- 布尔组合：先把线条变区域，再和其他区域做合并/相交/相减。

## 6. 常见坑与经验

- **输出路径不是中心线。** `createStroke()` 返回的是描边覆盖区域，适合 fill，不适合再当作原始轨迹。
- **宽度向两侧扩展。** `width = 10` 大致表示中心线两边各 5 个逻辑单位。
- **cap 只影响开放端点。** 闭合子路径没有端点，`capStyle()` 对它们没有可见影响。
- **join 决定折角气质。** `RoundJoin` 更平滑，`MiterJoin` 保留尖角但可能产生很长的尖刺。
- **miter limit 是宽度倍数。** 实际限制约等于 `miterLimit * width`，不是固定像素。
- **虚线模式按宽度相关单位解释。** 自定义 dash pattern 的数值和 `QPen` 一样，描述 dash/gap 交替长度。
- **曲线阈值别随便调太小。** 更小会更平滑，也会生成更多几何元素，复杂路径可能明显变慢。

## 7. 知识点覆盖

- 中心线、描边、填充区域三者的区别
- cap、join、miter limit 对几何轮廓的影响
- 虚线模式和偏移量的实际用途
- 命中测试、布尔运算和裁剪前的“线转面”
- 曲线展平精度与性能之间的取舍
- `QPen` 绘制语义与路径几何语义的对应关系
