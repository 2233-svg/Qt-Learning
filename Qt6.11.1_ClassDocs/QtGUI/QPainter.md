# QPainter

> Qt 6.11.1 · Qt GUI · 来自 `QPainter`

## 1. 先建立直觉

`QPainter` 是 Qt 的二维绘制上下文。你可以把它理解成“拿着当前画笔、画刷、字体、变换、裁剪和合成规则，在某个 paint device 上落笔”的对象。它能画线、矩形、路径、文字、图片、pixmap，也能把内容画到 `QWidget`、`QImage`、`QPixmap`、`QPicture`、`QPdfWriter`、`QPrinter` 等设备上。

`QPainter` 的关键不是某个 `draw...()` 函数，而是 **绘制状态**。同一段 `drawRect()`，在不同 pen、brush、transform、clip、opacity、composition mode 下会得到完全不同的结果。因此写绘制代码时，最重要的习惯是用 `save()` / `restore()` 管住状态边界。

## 2. 类说明

- 头文件：`#include <QPainter>`
- CMake：`Qt6::Gui`
- 直接派生类：`QStylePainter`
- 绑定对象：一次只能绑定一个 `QPaintDevice`
- 常见设备：`QWidget`、`QImage`、`QPixmap`、`QPicture`、`QPdfWriter`、`QPrinter`

在 `QWidget` 上绘制时，通常只在 `paintEvent()` 中创建 `QPainter painter(this)`。不要缓存一个长期存活的 `QPainter`，也不要手动调用 `paintEvent()`；状态变了就调用 `update()`，让事件循环安排真正的重绘。

## 3. API 速查

| API 族 | 作用 |
| --- | --- |
| `QPainter()` / `QPainter(QPaintDevice*)` | 创建未绑定或立即绑定设备的 painter。 |
| `begin(device)` / `end()` / `isActive()` | 手动控制绘制生命周期；构造绑定设备时通常由析构自动结束。 |
| `device()` / `paintEngine()` | 查看当前绘制目标和后端引擎。 |
| `save()` / `restore()` | 压栈/恢复完整绘制状态，是局部样式和局部变换的基本工具。 |
| `setPen()` / `pen()` | 控制轮廓线、直线、路径描边、文字颜色；Qt 6.11 支持 `QPen&&`。 |
| `setBrush()` / `brush()` | 控制填充；Qt 6.9 起可直接传 `QColor` / `Qt::GlobalColor`，Qt 6.11 支持 `QBrush&&`。 |
| `setFont()` / `font()` / `fontMetrics()` | 控制和测量文本绘制。 |
| `setOpacity()` / `opacity()` | 设置整体透明度，会影响后续绘制操作。 |
| `setCompositionMode()` | 设置源像素和目标像素如何合成。 |
| `setRenderHint(s)` / `testRenderHint()` | 控制抗锯齿、文字抗锯齿、平滑图片、无损图片等渲染倾向。 |
| `translate()` / `scale()` / `rotate()` / `shear()` | 在当前世界变换上继续叠加变换。 |
| `setTransform()` / `transform()` / `resetTransform()` | 设置或读取当前变换。 |
| `setWorldTransform()` / `worldTransform()` | 控制世界坐标变换。 |
| `setWindow()` / `setViewport()` | 建立逻辑坐标窗口与设备视口的映射。 |
| `deviceTransform()` / `combinedTransform()` | 查看世界、视口和设备变换组合后的结果。 |
| `setClipRect()` / `setClipPath()` / `setClipRegion()` | 限制后续绘制区域。 |
| `hasClipping()` / `clipBoundingRect()` | 查询当前裁剪状态和大致边界。 |
| `drawPoint(s)` / `drawLine(s)` | 绘制点和线。 |
| `drawRect(s)` / `drawRoundedRect()` / `drawEllipse()` | 绘制常见几何图形。 |
| `drawArc()` / `drawChord()` / `drawPie()` | 绘制椭圆相关的弧、弦、扇形，角度单位是 1/16 度。 |
| `drawPolygon()` / `drawPolyline()` / `drawConvexPolygon()` | 绘制多边形、折线、凸多边形。 |
| `drawPath()` / `fillPath()` / `strokePath()` | 用 `QPainterPath` 绘制复杂形状。 |
| `drawText()` / `boundingRect()` | 绘制文本和估算文本占用矩形。 |
| `drawStaticText()` / `drawGlyphRun()` | 绘制预布局文本或字形序列，适合更精细/高频文本场景。 |
| `drawImage()` | 绘制 CPU 图像数据，适合像素处理后的结果。 |
| `drawPixmap()` | 绘制平台图形资源，适合屏幕显示。 |
| `drawPixmapFragments()` | 从同一 pixmap 批量绘制许多片段。 |
| `drawTiledPixmap()` | 平铺 pixmap 填充区域。 |
| `fillRect()` / `eraseRect()` | 快速填充或擦除矩形区域。 |
| `drawPicture()` | 回放 `QPicture` 记录的绘图命令。 |
| `beginNativePainting()` / `endNativePainting()` | 临时交给原生图形 API，如 OpenGL；返回后继续 Qt 绘制。 |

## 4. 关键用法

### QWidget 自定义绘制

```cpp
void Meter::paintEvent(QPaintEvent *)
{
    QPainter p(this);
    p.setRenderHint(QPainter::Antialiasing);

    p.save();
    p.translate(width() / 2.0, height() / 2.0);
    p.setPen(QPen(Qt::white, 2));
    p.setBrush(QColor(40, 120, 200));
    p.drawEllipse(QPointF(0, 0), 40, 40);
    p.restore();
}
```

`save()` / `restore()` 的意义是让平移、画笔、画刷只影响这一小段。复杂控件通常会把每个绘制层都包在自己的状态边界里。

### 离屏绘制到 QImage

```cpp
QImage image(QSize(800, 600), QImage::Format_ARGB32_Premultiplied);
image.fill(Qt::transparent);

QPainter p(&image);
p.setCompositionMode(QPainter::CompositionMode_SourceOver);
p.setRenderHint(QPainter::Antialiasing);
p.drawPath(path);
```

需要透明和合成时，`Format_ARGB32_Premultiplied` 通常比普通 ARGB 更适合 `QPainter` 的栅格引擎。

### 文本绘制先测量再落笔

```cpp
QTextOption option;
option.setWrapMode(QTextOption::WordWrap);
option.setAlignment(Qt::AlignCenter);

const QRectF area(0, 0, width(), 80);
p.drawText(area, title, option);
```

`drawText(QPointF, QString)` 的点通常是文本基线附近的位置；`drawText(QRectF, ..., QTextOption)` 更适合多行、对齐和换行。做精细布局时配合 `QFontMetrics`、`QTextLayout` 或 `QStaticText`。

### 图片与 pixmap 的选择

```cpp
p.setRenderHint(QPainter::SmoothPixmapTransform, true);
p.drawPixmap(targetRect, iconPixmap, sourceRect);
```

`QImage` 更适合像素读写和后台处理，`QPixmap` 更适合 GUI 显示。高 DPI 资源要关注 `devicePixelRatio()`，否则图像可能尺寸正确但发虚，或源矩形切错。

## 5. 使用场景

- 自定义 `QWidget`：仪表盘、图表、波形、时间轴、编辑器标尺。
- 离屏生成图片：缩略图、水印、报表预览、缓存图层。
- PDF/打印输出：通过 `QPdfWriter`、`QPrinter`、`QPagedPaintDevice` 绘制页面。
- 简单 2D 可视化：路径、文字、图像叠加、区域填色。
- 资源预处理：把多张图片合成一张 pixmap 或生成图集。
- 需要像素级合成规则的场景：遮罩、擦除、叠加、高亮、半透明层。

## 6. 常见坑与经验

- **不要在 `paintEvent()` 外随意画 QWidget。** QWidget 的内容由系统重绘事件驱动；状态变化后调用 `update()`。
- **不要缓存活跃的 `QPainter`。** 它是一次绘制会话，不是长期画布对象。
- **状态会继续影响后续绘制。** 设置了 transform、clip、opacity、composition mode 后，最好用 `save()` / `restore()` 包起来。
- **弧度单位不是度。** `drawArc()`、`drawPie()`、`drawChord()` 的角度单位是 1/16 度，`90 * 16` 才是 90 度。
- **抗锯齿会影响像素对齐。** 画 1 像素线时，要理解整数坐标、半像素偏移和 cosmetic pen 的差异。
- **裁剪不是布局。** clip 只限制绘制结果，不会自动改变文本换行、图片缩放或几何计算。
- **高 DPI 要按逻辑像素思考。** `QPainter` 通常在逻辑坐标中绘制，图片资源的 `devicePixelRatio` 决定它如何映射到物理像素。
- **合成模式依赖目标格式。** 透明擦除、乘法叠加等效果需要目标有 alpha，并且格式最好适合 premultiplied alpha。
- **`beginNativePainting()` 会打断 Qt 状态假设。** 原生绘制结束后要恢复必要的 GL/图形状态，再调用 `endNativePainting()`。

## 7. 渲染提示与合成模式要点

`RenderHint` 是“请求后端尽量这样做”，不是所有设备都能完全满足：

- `Antialiasing`：几何抗锯齿，常用于路径和曲线。
- `TextAntialiasing`：文字抗锯齿。
- `SmoothPixmapTransform`：图片缩放时平滑采样，质量更好但可能更慢。
- `VerticalSubpixelPositioning`：让文本垂直位置具备子像素精度。
- `LosslessImageRendering`：对支持的目标请求无损图像嵌入，常见于 PDF。
- `NonCosmeticBrushPatterns`：让画刷图案参与变换，而不是固定在设备像素上。

`CompositionMode_SourceOver` 是默认透明叠加。做擦除常用 `CompositionMode_Clear` 或 `CompositionMode_DestinationOut`；做遮罩常看 `SourceIn` / `DestinationIn`；做亮度叠加常看 `Plus`、`Multiply`、`Screen`。如果效果不符合预期，先检查目标图像格式、alpha 通道和当前 opacity。

## 8. 知识点覆盖

- 绘制生命周期：构造、`begin()`、`end()`、析构
- QWidget 绘制事件与离屏绘制的差异
- pen、brush、font、opacity、composition mode 的状态模型
- 坐标变换、视口/窗口映射、设备变换
- 裁剪区域、脏区重绘和局部状态管理
- 几何图形、路径、文本、图片、pixmap 的绘制族
- 高 DPI、premultiplied alpha、图片缩放质量
- 原生绘制与 Qt 绘制状态之间的边界
