# QPen：定义路径和图元的笔画轮廓

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPen>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Gui)`，并链接 `Qt6::Gui`

`QPen` 描述 `QPainter` 如何给线、路径边界和图形轮廓描边：笔画填充使用什么 `QBrush`，宽度多大，实线还是虚线，线端如何收尾，以及折线转角如何连接。

它是隐式共享的值类型。可以把一支配置好的笔按值保存、传给绘制函数或复用到多个 painter；修改某个副本时会分离其数据，不会反过来改掉其他副本。

## 先看一支笔真正控制什么

```cpp
QPen pen(QColor("#1565c0"), 4,
         Qt::DashLine,
         Qt::RoundCap,
         Qt::RoundJoin);

QPainter painter(this);
painter.setPen(pen);
painter.setBrush(Qt::NoBrush);
painter.drawPath(route);
```

上例里：

- `QColor` 只是笔画刷的简单形式；笔画也可以用渐变、纹理等 `QBrush` 填充。
- `4` 是逻辑坐标中的宽度。默认的非 cosmetic pen 会随 painter 的缩放而放大或缩小。
- `DashLine` 决定沿路径排布的短划线。
- `RoundCap` 让开放线段和每个虚线段两端呈圆形。
- `RoundJoin` 让折线拐角呈圆弧。

默认 `QPen` 为黑色实线、宽度 `1`、`Qt::SquareCap` 和 `Qt::BevelJoin`。不要把默认端点或转角误认为圆形。

## 宽度 0、cosmetic pen 与缩放

`width()` 是整数宽度，`widthF()` 支持浮点宽度。宽度为 `0` 表示 cosmetic pen：无论 painter 应用了怎样的几何变换，笔画都以一个设备像素宽绘制。`setCosmetic(true)` 也要求笔画不随变换缩放。

```cpp
QPen gridPen(QColor("#90a4ae"));
gridPen.setWidth(0); // 设备像素宽的网格线

painter.scale(8, 8);
painter.setPen(gridPen);
painter.drawLine(QPointF(0, 0), QPointF(100, 0));
```

cosmetic pen 适合编辑器网格、选中框、坐标辅助线等“无论视图缩放多少都保持细”的 UI 提示。它不适合需要随对象比例变大的图稿轮廓，也不能代替高 DPI 与打印输出的视觉验证：一个“设备像素”在不同目标的物理尺寸并不相同。

宽度为 `0` 与“没有线”完全不同；禁止描边应使用 `Qt::NoPen`。在缩放图纸、导出 PDF 或切换高 DPI 屏幕后，先明确自己要的是逻辑线宽还是设备像素线宽。

## 端点与连接：路径几何之外的可见范围

端点样式作用于开放线段和虚线段；连接样式作用于连续线段的拐角。二者主要对宽度至少为 `1` 的线有效。

| 样式 | 可见效果 |
| --- | --- |
| `Qt::FlatCap` | 线在几何端点处截止，不向外延伸。 |
| `Qt::SquareCap` | 线端是矩形，并向端点外延伸半个线宽。 |
| `Qt::RoundCap` | 线端是半圆，并向端点外延伸半个线宽。 |
| `Qt::BevelJoin` | 将尖角削平，默认值。 |
| `Qt::MiterJoin` | 延长两条边直到相交，锐角会形成很长的尖刺。 |
| `Qt::RoundJoin` | 用圆弧填补转角。 |

若把一条标尺线或虚线看成“刚好从 A 到 B”，`SquareCap` 和 `RoundCap` 会让其在两端各多出半个笔宽。精确对齐时使用 `FlatCap`，或把这一可见扩张纳入布局/命中范围计算。

`MiterJoin` 的尖刺长度由 `miterLimit` 限制。限制值以**笔宽为单位**计量，默认是 `2`；只有 `MiterJoin` 时才有效。尖锐折线、宽描边或地图边界常应选择 `RoundJoin` / `BevelJoin`，或者降低 miter limit，避免近乎平行的线段生成很长的突刺。

## 实线、内置虚线与自定义虚线

`Qt::SolidLine` 是普通实线，`Qt::DashLine`、`DotLine`、`DashDotLine`、`DashDotDotLine` 是内置模式，`Qt::NoPen` 不绘制轮廓。

自定义模式要求一个元素数为偶数的 `QList<qreal>`：第 1、3、5… 个值是划线长度，第 2、4、6… 个值是空白长度。它们以**笔宽的倍数**表示，而不是固定像素。

```cpp
QPen marchingAnts(Qt::black, 2);
marchingAnts.setDashPattern({3, 2}); // 6 逻辑像素划线，4 逻辑像素空白
marchingAnts.setDashOffset(1.5);     // 改变模式的起始相位
```

`setDashPattern()` 会把样式隐式改为 `Qt::CustomDashLine`。`setDashOffset()` 也以该模式单位移动起点，并会使笔转为自定义虚线。更新虚线时不要随后又 `setStyle(Qt::SolidLine)`，否则刚设置的模式不会再参与绘制。

虚线的真实可见长度还会受端点样式影响：`SquareCap` 和 `RoundCap` 会在每段两端各延伸半个线宽。例如模式中的长度 `1` 加上方形端点，视觉长度可能显著大于配置值。制作“蚂蚁线”动画时持续增加 `dashOffset`，但要在目标缩放级别观察实际效果。

## 颜色、画刷与比较

`setColor()` 是 `setBrush(QBrush(color))` 的便捷形式。若笔画需要线性渐变、纹理或图案，使用 `setBrush()`；这时 `color()` 只给出该画刷的颜色属性，不能替代完整的画刷信息。

```cpp
QLinearGradient gradient(0, 0, 160, 0);
gradient.setColorAt(0, "#00acc1");
gradient.setColorAt(1, "#7cb342");

QPen pen;
pen.setBrush(gradient);
pen.setWidthF(3.5);
```

`operator==` 比较整支笔的值，而不是只比较颜色。`QPen` 还可与 `QColor` 或 `Qt::PenStyle` 比较，用于简短条件判断；复杂业务条件仍建议检查 `brush()`、`style()`、`widthF()` 等明确属性。

## 与 QPainterPathStroker 的关系

`QPainter::drawPath()` 根据当前 `QPen` 在渲染时描边。若要把“笔画本身”变成可填充、可裁切、可命中的几何区域，使用 `QPainterPathStroker` 并复制对应的宽度、端点、连接、miter 和虚线设置。`QPen` 只是样式描述，不直接提供笔画轮廓。

## 常见错误

- 把 `setWidth(0)` 当作隐藏线：它会绘制一像素宽的 cosmetic line；隐藏要用 `Qt::NoPen`。
- 在被 `QPainter::scale()` 放大的图形上仍期待普通 `width=1` 为一设备像素：默认笔会一起缩放。
- 自定义虚线用奇数个元素：模式必须按划线/空白配对。
- 使用 `MiterJoin` 绘制锐角宽折线却不设限：会出现长尖刺。
- 用 `SquareCap` 绘制要求精确端点的刻度线：线会超出端点半个笔宽。
- 只设置 `color()` 后期改为渐变笔刷，却仍把 `color()` 当作完整样式来源。

## API 速查表

### 构造与值语义

| API | 语义与使用边界 |
| --- | --- |
| `QPen()` | 默认黑色实线，宽度 `1`，方形端点、斜角连接。 |
| `QPen(Qt::PenStyle)` | 用指定线型构造笔；`Qt::NoPen` 表示不描边。 |
| `QPen(QColor)` | 用纯色构造默认样式笔。 |
| `QPen(QBrush, width, style, cap, join)` | 一次设置笔画刷、宽度、线型、端点和连接。 |
| 拷贝/移动构造、赋值、`swap()` | 隐式共享值语义；修改副本时分离。 |
| `operator=(QColor)` | 改成该颜色的默认实线笔，并使用默认端点和连接。 |
| `operator=(Qt::PenStyle)` | 改成指定样式；赋值 `Qt::NoPen` 禁止轮廓绘制。 |
| `operator QVariant()` | 转换为 `QVariant`，可用于属性和通用数据存储。 |

### 线型和虚线

| API | 语义与使用边界 |
| --- | --- |
| `style()` / `setStyle(Qt::PenStyle)` | 读取或设置实线、内置虚线、`CustomDashLine`、`NoPen` 等样式。 |
| `dashPattern()` | 返回当前虚线模式。 |
| `setDashPattern(QList<qreal>)` | 设置划线/空白交替模式，元素数必须为偶数；单位是笔宽，并隐式设为 `CustomDashLine`。 |
| `dashOffset()` / `setDashOffset(qreal)` | 读取或设置虚线起始相位；单位与 dash pattern 相同，设置时使用自定义虚线模式。 |
| `isSolid()` | 判断当前笔是否为实线笔。 |

### 宽度、端点和连接

| API | 语义与使用边界 |
| --- | --- |
| `width()` / `setWidth(int)` | 读取或设置整数逻辑宽度；`0` 表示 cosmetic pen。 |
| `widthF()` / `setWidthF(qreal)` | 读取或设置浮点逻辑宽度；适合高精度几何。 |
| `isCosmetic()` / `setCosmetic(bool)` | 查询或设置笔画是否不随 painter 几何变换缩放。 |
| `capStyle()` / `setCapStyle(Qt::PenCapStyle)` | 读取或设置 `FlatCap`、`SquareCap`、`RoundCap`；会改变端点和虚线段可见长度。 |
| `joinStyle()` / `setJoinStyle(Qt::PenJoinStyle)` | 读取或设置 `BevelJoin`、`MiterJoin`、`RoundJoin`；作用于折线转角。 |
| `miterLimit()` / `setMiterLimit(qreal)` | 读取或设置 miter 最大延伸，单位为笔宽；仅 `MiterJoin` 有效，默认 `2`。 |

### 笔画刷和比较

| API | 语义与使用边界 |
| --- | --- |
| `color()` / `setColor(QColor)` | 读取或设置纯色属性；渐变/纹理笔画应使用完整 `QBrush`。 |
| `brush()` / `setBrush(QBrush)` | 读取或设置笔画的填充画刷，可为颜色、渐变、纹理或图案。 |
| `operator==` / `operator!=` | 比较整支笔的值。 |
| 与 `QColor`、`Qt::PenStyle` 的比较 | 分别用于简便颜色或样式判断；不能代表其他笔属性相同。 |
| `isDetached()` | 查询是否拥有独立数据；这是隐式共享的调试/低层状态，普通业务逻辑不应依赖它。 |
| `QDataStream <<` / `>>` | 写入/读取 Qt 二进制流；外部输入需要检查流状态。 |
| `QDebug <<` | 输出调试表示；仅在启用调试流时可用。 |
