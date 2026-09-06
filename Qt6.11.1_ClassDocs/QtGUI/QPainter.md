# QPainter

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QPainter` 是 Qt 二维绘制上下文，统一把线、路径、文字、图像和变换绘制到 QWidget、QImage、QPixmap 等设备。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QPainter` 是 Qt 二维绘制上下文，统一把线、路径、文字、图像和变换绘制到 QWidget、QImage、QPixmap 等设备。

**内部模型：** QPainter 的状态包含画笔、画刷、字体、变换、裁剪和合成模式；save/restore 用来隔离局部状态。绘制只能在合法的 paintEvent 或有效 paint device 生命周期内进行。

**适用场景：** 自定义控件绘制、离屏图像、打印、图表和简单二维图形使用。复杂高性能场景应评估 QQuick/scene graph/OpenGL。

**典型调用链：** 创建 painter(device) -> save -> setPen/setBrush/setFont/setTransform -> draw... -> restore -> 析构或 end。

**先记住的坑：** 不要在 paintEvent 外永久缓存 QPainter；不要忘记高 DPI 和坐标系；绘制时避免改变业务状态；使用 update() 请求重绘而不是直接调用 paintEvent。

## 2. 依赖与对象关系

- 头文件：`#include <QPainter>`
- 继承自：未在类页中列出
- 直接派生类：QStylePainter

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

QPainter 的状态包含画笔、画刷、字体、变换、裁剪和合成模式；save/restore 用来隔离局部状态。绘制只能在合法的 paintEvent 或有效 paint device 生命周期内进行。

### 状态、生命周期和线程

**生命周期：** 绘制上下文必须绑定有效的 paint device，并在合法的绘制阶段使用。QWidget 上通常只在 `paintEvent()` 内创建 painter；离屏图像、打印设备和 pixmap 则有各自的设备生命周期。

**状态与结果：** `save()`/`restore()` 用于隔离局部状态；改变坐标系、画笔或合成模式后要么恢复，要么明确后续绘制也需要该状态。重绘请求和真正绘制是两个阶段，业务状态变化应调用 `update()`。

**线程与事件循环：** 同一个 GUI 控件的绘制在 GUI 线程完成；离屏 QImage 可以按数据所有权在后台处理，但不要让后台线程直接绘制或访问正在显示的 QWidget/QPixmap 资源。

## 3. 直接使用

自定义控件绘制、离屏图像、打印、图表和简单二维图形使用。复杂高性能场景应评估 QQuick/scene graph/OpenGL。 使用时通常按这个过程组织：创建 painter(device) -> save -> setPen/setBrush/setFont/setTransform -> draw... -> restore -> 析构或 end。

```cpp
void Widget::paintEvent(QPaintEvent *)
{
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);
    painter.setPen(Qt::blue);
    painter.drawLine(10, 10, width() - 10, height() - 10);
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `class PixmapFragment`
- `enum CompositionMode { CompositionMode_SourceOver, CompositionMode_DestinationOver, CompositionMode_Clear, CompositionMode_Source, CompositionMode_Destination, …, RasterOp_SourceOrNotDestination }`
- `enum PixmapFragmentHint { OpaqueHint }`
- `flags PixmapFragmentHints`
- `enum RenderHint { Antialiasing, TextAntialiasing, SmoothPixmapTransform, VerticalSubpixelPositioning, LosslessImageRendering, NonCosmeticBrushPatterns }`
- `flags RenderHints`

### 公有函数

- `QPainter()`
- `QPainter(QPaintDevice *device)`
- `~QPainter()`
- `const QBrush & background() const`
- `Qt::BGMode backgroundMode() const`
- `bool begin(QPaintDevice *device)`
- `void beginNativePainting()`
- `QRectF boundingRect(const QRectF &rectangle, int flags, const QString &text)`
- `QRect boundingRect(const QRect &rectangle, int flags, const QString &text)`
- `QRectF boundingRect(const QRectF &rectangle, const QString &text, const QTextOption &option = QTextOption())`
- `QRect boundingRect(int x, int y, int w, int h, int flags, const QString &text)`
- `const QBrush & brush() const`
- `QPoint brushOrigin() const`
- `(since 6.11) QPointF brushOriginF() const`
- `QRectF clipBoundingRect() const`
- `QPainterPath clipPath() const`
- `QRegion clipRegion() const`
- `QTransform combinedTransform() const`
- `QPainter::CompositionMode compositionMode() const`
- `QPaintDevice * device() const`
- `const QTransform & deviceTransform() const`
- `void drawArc(const QRectF &rectangle, int startAngle, int spanAngle)`
- `void drawArc(const QRect &rectangle, int startAngle, int spanAngle)`
- `void drawArc(int x, int y, int width, int height, int startAngle, int spanAngle)`
- `void drawChord(const QRectF &rectangle, int startAngle, int spanAngle)`
- `void drawChord(const QRect &rectangle, int startAngle, int spanAngle)`
- `void drawChord(int x, int y, int width, int height, int startAngle, int spanAngle)`
- `void drawConvexPolygon(const QPointF *points, int pointCount)`
- `void drawConvexPolygon(const QPolygon &polygon)`
- `void drawConvexPolygon(const QPolygonF &polygon)`
- `void drawConvexPolygon(const QPoint *points, int pointCount)`
- `void drawEllipse(const QRectF &rectangle)`
- `void drawEllipse(const QRect &rectangle)`
- `void drawEllipse(const QPoint &center, int rx, int ry)`
- `void drawEllipse(const QPointF &center, qreal rx, qreal ry)`
- `void drawEllipse(int x, int y, int width, int height)`
- `void drawGlyphRun(const QPointF &position, const QGlyphRun &glyphs)`
- `void drawImage(const QRectF &target, const QImage &image, const QRectF &source, Qt::ImageConversionFlags flags = Qt::AutoColor)`
- `void drawImage(const QPoint &point, const QImage &image)`
- `void drawImage(const QPointF &point, const QImage &image)`
- `void drawImage(const QRect &rectangle, const QImage &image)`
- `void drawImage(const QRectF &rectangle, const QImage &image)`
- `void drawImage(const QPoint &point, const QImage &image, const QRect &source, Qt::ImageConversionFlags flags = Qt::AutoColor)`
- `void drawImage(const QPointF &point, const QImage &image, const QRectF &source, Qt::ImageConversionFlags flags = Qt::AutoColor)`
- `void drawImage(const QRect &target, const QImage &image, const QRect &source, Qt::ImageConversionFlags flags = Qt::AutoColor)`
- `void drawImage(int x, int y, const QImage &image, int sx = 0, int sy = 0, int sw = -1, int sh = -1, Qt::ImageConversionFlags flags = Qt::AutoColor)`
- `void drawLine(const QLineF &line)`
- `void drawLine(const QLine &line)`
- `void drawLine(const QPoint &p1, const QPoint &p2)`
- `void drawLine(const QPointF &p1, const QPointF &p2)`
- `void drawLine(int x1, int y1, int x2, int y2)`
- `void drawLines(const QLineF *lines, int lineCount)`
- `void drawLines(const QList<QLine> &lines)`
- `void drawLines(const QList<QLineF> &lines)`
- `void drawLines(const QList<QPoint> &pointPairs)`
- `void drawLines(const QList<QPointF> &pointPairs)`
- `void drawLines(const QLine *lines, int lineCount)`
- `void drawLines(const QPoint *pointPairs, int lineCount)`
- `void drawLines(const QPointF *pointPairs, int lineCount)`
- `void drawPath(const QPainterPath &path)`
- `void drawPicture(const QPointF &point, const QPicture &picture)`
- `void drawPicture(const QPoint &point, const QPicture &picture)`
- `void drawPicture(int x, int y, const QPicture &picture)`
- `void drawPie(const QRectF &rectangle, int startAngle, int spanAngle)`
- `void drawPie(const QRect &rectangle, int startAngle, int spanAngle)`
- `void drawPie(int x, int y, int width, int height, int startAngle, int spanAngle)`
- `void drawPixmap(const QRectF &target, const QPixmap &pixmap, const QRectF &source)`
- `void drawPixmap(const QPoint &point, const QPixmap &pixmap)`
- `void drawPixmap(const QPointF &point, const QPixmap &pixmap)`
- `void drawPixmap(const QRect &rectangle, const QPixmap &pixmap)`
- `void drawPixmap(const QPoint &point, const QPixmap &pixmap, const QRect &source)`
- `void drawPixmap(const QPointF &point, const QPixmap &pixmap, const QRectF &source)`
- `void drawPixmap(const QRect &target, const QPixmap &pixmap, const QRect &source)`
- `void drawPixmap(int x, int y, const QPixmap &pixmap)`
- `void drawPixmap(int x, int y, int width, int height, const QPixmap &pixmap)`
- `void drawPixmap(int x, int y, const QPixmap &pixmap, int sx, int sy, int sw, int sh)`
- `void drawPixmap(int x, int y, int w, int h, const QPixmap &pixmap, int sx, int sy, int sw, int sh)`
- `void drawPixmapFragments(const QPainter::PixmapFragment *fragments, int fragmentCount, const QPixmap &pixmap, QPainter::PixmapFragmentHints hints = PixmapFragmentHints())`
- `void drawPoint(const QPointF &position)`
- `void drawPoint(const QPoint &position)`
- `void drawPoint(int x, int y)`
- `void drawPoints(const QPointF *points, int pointCount)`
- `void drawPoints(const QPolygon &points)`
- `void drawPoints(const QPolygonF &points)`
- `void drawPoints(const QPoint *points, int pointCount)`
- `void drawPolygon(const QPointF *points, int pointCount, Qt::FillRule fillRule = Qt::OddEvenFill)`
- `void drawPolygon(const QPolygon &points, Qt::FillRule fillRule = Qt::OddEvenFill)`
- `void drawPolygon(const QPolygonF &points, Qt::FillRule fillRule = Qt::OddEvenFill)`
- `void drawPolygon(const QPoint *points, int pointCount, Qt::FillRule fillRule = Qt::OddEvenFill)`
- `void drawPolyline(const QPointF *points, int pointCount)`
- `void drawPolyline(const QPolygon &points)`
- `void drawPolyline(const QPolygonF &points)`
- `void drawPolyline(const QPoint *points, int pointCount)`
- `void drawRect(const QRectF &rectangle)`
- `void drawRect(const QRect &rectangle)`
- `void drawRect(int x, int y, int width, int height)`
- `void drawRects(const QRectF *rectangles, int rectCount)`
- `void drawRects(const QList<QRect> &rectangles)`
- `void drawRects(const QList<QRectF> &rectangles)`
- `void drawRects(const QRect *rectangles, int rectCount)`
- `void drawRoundedRect(const QRectF &rect, qreal xRadius, qreal yRadius, Qt::SizeMode mode = Qt::AbsoluteSize)`
- `void drawRoundedRect(const QRect &rect, qreal xRadius, qreal yRadius, Qt::SizeMode mode = Qt::AbsoluteSize)`
- `void drawRoundedRect(int x, int y, int w, int h, qreal xRadius, qreal yRadius, Qt::SizeMode mode = Qt::AbsoluteSize)`
- `void drawStaticText(const QPointF &topLeftPosition, const QStaticText &staticText)`
- `void drawStaticText(const QPoint &topLeftPosition, const QStaticText &staticText)`
- `void drawStaticText(int left, int top, const QStaticText &staticText)`
- `void drawText(const QPointF &position, const QString &text)`
- `void drawText(const QPoint &position, const QString &text)`
- `void drawText(const QRectF &rectangle, const QString &text, const QTextOption &option = QTextOption())`
- `void drawText(int x, int y, const QString &text)`
- `void drawText(const QRect &rectangle, int flags, const QString &text, QRect *boundingRect = nullptr)`
- `void drawText(const QRectF &rectangle, int flags, const QString &text, QRectF *boundingRect = nullptr)`
- `void drawText(int x, int y, int width, int height, int flags, const QString &text, QRect *boundingRect = nullptr)`
- `void drawTiledPixmap(const QRectF &rectangle, const QPixmap &pixmap, const QPointF &position = QPointF())`
- `void drawTiledPixmap(const QRect &rectangle, const QPixmap &pixmap, const QPoint &position = QPoint())`
- `void drawTiledPixmap(int x, int y, int width, int height, const QPixmap &pixmap, int sx = 0, int sy = 0)`
- `bool end()`
- `void endNativePainting()`
- `void eraseRect(const QRectF &rectangle)`
- `void eraseRect(const QRect &rectangle)`
- `void eraseRect(int x, int y, int width, int height)`
- `void fillPath(const QPainterPath &path, const QBrush &brush)`
- `void fillRect(const QRectF &rectangle, const QBrush &brush)`
- `void fillRect(const QRect &rectangle, QGradient::Preset preset)`
- `void fillRect(const QRect &rectangle, Qt::BrushStyle style)`
- `void fillRect(const QRect &rectangle, Qt::GlobalColor color)`
- `void fillRect(const QRect &rectangle, const QBrush &brush)`
- `void fillRect(const QRect &rectangle, const QColor &color)`
- `void fillRect(const QRectF &rectangle, QGradient::Preset preset)`
- `void fillRect(const QRectF &rectangle, Qt::BrushStyle style)`
- `void fillRect(const QRectF &rectangle, Qt::GlobalColor color)`
- `void fillRect(const QRectF &rectangle, const QColor &color)`
- `void fillRect(int x, int y, int width, int height, QGradient::Preset preset)`
- `void fillRect(int x, int y, int width, int height, Qt::BrushStyle style)`
- `void fillRect(int x, int y, int width, int height, Qt::GlobalColor color)`
- `void fillRect(int x, int y, int width, int height, const QBrush &brush)`
- `void fillRect(int x, int y, int width, int height, const QColor &color)`
- `const QFont & font() const`
- `QFontInfo fontInfo() const`
- `QFontMetrics fontMetrics() const`
- `bool hasClipping() const`
- `bool isActive() const`
- `Qt::LayoutDirection layoutDirection() const`
- `qreal opacity() const`
- `QPaintEngine * paintEngine() const`
- `const QPen & pen() const`
- `QPainter::RenderHints renderHints() const`
- `void resetTransform()`
- `void restore()`
- `void rotate(qreal angle)`
- `void save()`
- `void scale(qreal sx, qreal sy)`
- `void setBackground(const QBrush &brush)`
- `void setBackgroundMode(Qt::BGMode mode)`
- `void setBrush(const QBrush &brush)`
- `(since 6.11) void setBrush(QBrush &&brush)`
- `(since 6.9) void setBrush(QColor color)`
- `void setBrush(Qt::BrushStyle style)`
- `(since 6.9) void setBrush(Qt::GlobalColor color)`
- `void setBrushOrigin(const QPointF &position)`
- `void setBrushOrigin(const QPoint &position)`
- `void setBrushOrigin(int x, int y)`
- `void setClipPath(const QPainterPath &path, Qt::ClipOperation operation = Qt::ReplaceClip)`
- `void setClipRect(const QRectF &rectangle, Qt::ClipOperation operation = Qt::ReplaceClip)`
- `void setClipRect(int x, int y, int width, int height, Qt::ClipOperation operation = Qt::ReplaceClip)`
- `void setClipRect(const QRect &rectangle, Qt::ClipOperation operation = Qt::ReplaceClip)`
- `void setClipRegion(const QRegion &region, Qt::ClipOperation operation = Qt::ReplaceClip)`
- `void setClipping(bool enable)`
- `void setCompositionMode(QPainter::CompositionMode mode)`
- `void setFont(const QFont &font)`
- `void setLayoutDirection(Qt::LayoutDirection direction)`
- `void setOpacity(qreal opacity)`
- `void setPen(const QPen &pen)`
- `(since 6.11) void setPen(QPen &&pen)`
- `void setPen(Qt::PenStyle style)`
- `void setPen(const QColor &color)`
- `void setRenderHint(QPainter::RenderHint hint, bool on = true)`
- `void setRenderHints(QPainter::RenderHints hints, bool on = true)`
- `void setTransform(const QTransform &transform, bool combine = false)`
- `void setViewTransformEnabled(bool enable)`
- `void setViewport(const QRect &rectangle)`
- `void setViewport(int x, int y, int width, int height)`
- `void setWindow(const QRect &rectangle)`
- `void setWindow(int x, int y, int width, int height)`
- `void setWorldMatrixEnabled(bool enable)`
- `void setWorldTransform(const QTransform &matrix, bool combine = false)`
- `void shear(qreal sh, qreal sv)`
- `void strokePath(const QPainterPath &path, const QPen &pen)`
- `bool testRenderHint(QPainter::RenderHint hint) const`
- `const QTransform & transform() const`
- `void translate(const QPointF &offset)`
- `void translate(const QPoint &offset)`
- `void translate(qreal dx, qreal dy)`
- `bool viewTransformEnabled() const`
- `QRect viewport() const`
- `QRect window() const`
- `bool worldMatrixEnabled() const`
- `const QTransform & worldTransform() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QPainter::CompositionMode`

**作用与语义：**

定义了数字图像合成所支持的模式。合成模式用于指定一张图像（源）中的像素如何与另一张图像（目标图像）中的像素合并。
请注意，位元光栅操作模式（以 RasterOp 前缀表示）仅在 X11 和光栅绘制引擎中原生支持。这意味着在 Mac 上使用这些模式的唯一方式是通过`QImage`。带有 alpha 组件的笔和画笔不支持光栅操作的混合模式。此外，开启 `QPainter::Antialiasing` 渲染提示会有效禁用光栅操作模式。
最常见的类型是SourceOver（通常简称alpha混合），即将源像素叠加在目标像素之上，使得源像素的alpha分量定义了像素的半透明性。
多种合成模式需要源图像或目标图像中的α通道才能产生效果。为了获得最佳性能，优先采用图像格式`Format_ARGB32_Premultiplied`。
当构图模式设置为时，它适用于所有绘画操作员、钢笔、画笔、渐变以及像素地图/图像绘图。
- `QPainter::CompositionMode_SourceOver`：`0`;这是默认模式。源的α用于将目标像素上方的像素混合。
- `QPainter::CompositionMode_DestinationOver`：`1`;目标像素的α用于在源像素上进行混合。该模式是CompositionMode_SourceOver的反向。
- `QPainter::CompositionMode_Clear`：`2`;目标像素被清除（设置为完全透明），与来源无关。
- `QPainter::CompositionMode_Source`：`3`;输出是源像素。（这意味着一个基本的复制操作，当源像素不透明时，与SourceOver相同。）
- `QPainter::CompositionMode_Destination`：`4`;输出是目标像素。这意味着混合没有影响。该模式是CompositionMode_Source的反。
- `QPainter::CompositionMode_SourceIn`：`5`;输出为源，其中α减去目的的α。
- `QPainter::CompositionMode_DestinationIn`：`6`;输出为目的，其中α减去源端的α。该模式是CompositionMode_SourceIn的倒数。
- `QPainter::CompositionMode_SourceOut`：`7`;输出为源，其中α被目的的倒数减去。
- `QPainter::CompositionMode_DestinationOut`：`8`;输出是目的，α 被源的倒数减小。该模式是 CompositionMode_SourceOut 的逆。
- `QPainter::CompositionMode_SourceAtop`：`9`;源像素在目标像素之上混合，源像素的α减去目标像素的α。
- `QPainter::CompositionMode_DestinationAtop`：`10`;目标像素在源像素之上混合，目的像素的α减去目标像素的α。该模式是CompositionMode_SourceAtop的反函数。
- `QPainter::CompositionMode_Xor`：`11`;源的α以目的α的逆约化后，与目的α被源α的逆约化的目的合并。CompositionMode_Xor与逐位Xor不同。
- `QPainter::CompositionMode_Plus`：`12`;将源像素和目标像素的阿尔法和颜色相加。
- `QPainter::CompositionMode_Multiply`：`13`;输出是源色乘以目标色。将颜色与白色相乘保持颜色不变，而将颜色与黑色相乘则得到黑色。
- `QPainter::CompositionMode_Screen`：`14`;源色和目标色被反转后乘以。用白色遮蔽颜色会产生白色，而用黑色遮蔽颜色则保持颜色不变。
- `QPainter::CompositionMode_Overlay`：`15`;根据目的地颜色乘法或遮蔽颜色。目标颜色与源色混合，以反映目的地的明暗。
- `QPainter::CompositionMode_Darken`：`16`;选择源色和目标色中较深的颜色。
- `QPainter::CompositionMode_Lighten`：`17`;选择源色和目标色中较浅的颜色。
- `QPainter::CompositionMode_ColorDodge`：`18`;目标颜色被调亮以反映源颜色。黑色源颜色保持目标颜色不变。
- `QPainter::CompositionMode_ColorBurn`：`19`;目标颜色被调暗以反映源颜色。白色源颜色保持目标颜色不变。
- `QPainter::CompositionMode_HardLight`：`20`;根据源色乘法或筛查颜色。光源颜色会使目标颜色变亮，而暗源颜色则会使目标颜色变暗。
- `QPainter::CompositionMode_SoftLight`：`21`;根据源色变暗或变亮颜色。类似于CompositionMode_HardLight。
- `QPainter::CompositionMode_Difference`：`22`;用较浅的颜色减去较深的颜色。用白色绘画会反转目标颜色，而用黑色绘制则目标颜色保持不变。
- `QPainter::CompositionMode_Exclusion`：`23`;与CompositionMode_Difference类似，但对比度较低。用白色绘画会反转目标颜色，而用黑色绘制则目标颜色保持不变。
- `QPainter::RasterOp_SourceOrDestination`：`24`;对源像素和目的像素进行按位的或操作（src 或 dst）。
- `QPainter::RasterOp_SourceAndDestination`：`25`;对源像素和目标像素进行逐位与运算（src 和 dst）。
- `QPainter::RasterOp_SourceXorDestination`：`26`;对源像素和目标像素进行比特异或操作（src XOR dst）。
- `QPainter::RasterOp_NotSourceAndNotDestination`：`27`;对源像素和目标像素进行逐位NOR操作（非src和非dst）。
- `QPainter::RasterOp_NotSourceOrNotDestination`：`28`;对源像素和目标像素进行位 NAND 操作（（非 src）或 （非 dst））。
- `QPainter::RasterOp_NotSourceXorDestination`：`29`;进行一个位位操作，将源像素反转后与目标像素进行异或（非 src）XOR DST 进行 XOR）。
- `QPainter::RasterOp_NotSource`：`30`;执行一个按位操作，将源像素反转（非src）。
- `QPainter::RasterOp_NotSourceAndDestination`：`31`;执行一个位位操作，先将源反转，然后与目的节点进行与（非 src）和 dst）。
- `QPainter::RasterOp_SourceAndNotDestination`：`32`;执行一个按位操作，将源节点与倒置的目标像素进行与（src AND，非 DST）。
- `QPainter::RasterOp_NotSourceOrDestination`：`33`;执行一个按位操作，先将源反转，然后与目的节点进行 OR 处理（非 src 或 dst）。
- `QPainter::RasterOp_ClearDestination`：`35`;目标节点中的像素被清除（设为0），与源无关。
- `QPainter::RasterOp_SetDestination`：`36`;目标节点中的像素设置为（设为1），与源无关。
- `QPainter::RasterOp_NotDestination`：`37`;执行一个按位的操作，目标像素反转（非DST）。
- `QPainter::RasterOp_SourceOrNotDestination`：`34`;执行一个按位操作，将源节点与倒置的目标像素进行OR处理（src OR，非DST）。

### `enum QPainter::PixmapFragmentHintflags QPainter::PixmapFragmentHints`

**作用与语义：**

- `QPainter::OpaqueHint`：`0x01`;表示要绘制的像素图片段是不透明的。不透明的片段可能绘制得更快。
PixmapFragmentHints 类型是 QFlags 的 typedef<PixmapFragmentHint>。它存储 PixmapFragmentHint 值的 OR 组合。

### `enum QPainter::RenderHintflags QPainter::RenderHints`

**作用与语义：**

渲染提示用于指定 `QPainter` 的标志，这些标志可能被任何给定引擎尊重也可能不会。
- `QPainter::Antialiasing`：`0x01`;表示发动机应对原图边缘进行抗锯齿处理（如可能）。
- `QPainter::TextAntialiasing`：`0x02`;表示引擎应在可能的情况下对文本进行抗锯齿处理。要强制禁用文本的抗锯齿，请不要使用此提示。相反，请在字体样式策略中设置`QFont::NoAntialias`。
- `QPainter::SmoothPixmapTransform`：`0x04`;表示引擎应使用光滑像素图变换算法（如双线性），而非最近邻。
- `QPainter::VerticalSubpixelPositioning`：`0x08`;允许文本在垂直和水平上都按像素的比例排列，前提是字体引擎支持。目前，当`QFont::PreferNoHinting`提示偏好时，Freetype在所有平台上支持此功能，macOS也支持。对于大多数用例，这不会提升视觉质量，但可能会增加内存消耗并降低文本渲染性能。因此，除非使用场景需要，否则不建议启用此功能。其中一个用例可能是将字形与其他视觉基元对齐。该值在Qt 6.1中加入。
- `QPainter::LosslessImageRendering`：`0x40`;尽可能使用无损图像渲染。目前，该提示仅在使用 `QPainter` 通过 `QPrinter` 或 `QPdfWriter` 输出 PDF 文件时使用，`drawImage()`/`drawPixmap()` 调用将使用无损压缩算法编码图像，而非有损 JPEG 压缩。该值在 Qt 5.13 中添加。
- `QPainter::NonCosmeticBrushPatterns`：`0x80`;用预定义的图案样式之一的画笔绘制时，也要变换图案，同时变换被绘制的物体。默认情况下，图案将图案视为外观，因此图案像素将直接映射到设备像素，独立于任何主动变换。该值在Qt 6.4中添加。
RenderHints 类型是 QFlags 的 typedef<RenderHint>。它存储 RenderHint 值的 OR 组合。

### `QPainter::QPainter()`

**作用与语义：**

构造画家。

### `[explicit] QPainter::QPainter(QPaintDevice *device)`

**作用与语义：**

制作一个立即开始上色油漆`device`的油漆工。
该构造器对短命画师（例如`QWidget::paintEvent()`中）很方便，且应仅使用一次。构造器会为你调用`begin()`，QPainter的解构器会自动调用`end()`。
这里有一个使用`begin()`和`end()`的例子：
同样的例子，使用该构造函数：
由于构造函数无法在画器初始化失败时提供反馈，你应该用`begin()`和`end()`来绘制外部设备，比如打印机。

**官方示例：**

```cpp
 void MyWidget::paintEvent(QPaintEvent *)
 {
     QPainter p;
     p.begin(this);
     p.drawLine(drawingCode);        // drawing code
     p.end();
 }
```

### `[noexcept] QPainter::~QPainter()`

**作用与语义：**

毁了画家。

### `const QBrush &QPainter::background() const`

**作用与语义：**

返回当前的背景画笔。

### `Qt::BGMode QPainter::backgroundMode() const`

**作用与语义：**

返回当前的背景模式。

### `bool QPainter::begin(QPaintDevice *device)`

**作用与语义：**

开始涂漆`device`，成功时返回`true`;否则返回`false`。
注意，所有画家设置（`setPen()`、`setBrush()`等）在调用 bein() 时都会被重置为默认值。
可能出现的错误是严重问题，例如：
注意大多数情况下，你可以用其中一个构造函数代替 begin()，而且`end()`在摧毁时会自动完成。
警告：一个油漆装置一次只能由一名油漆工进行绘制。
警告：不支持在`QImage`上用`QImage::Format_Indexed8`格式作画。

**官方示例：**

```cpp
 painter->begin(nullptr); // impossible - paint device cannot be null

 QPixmap image(0, 0);
 painter->begin(&image); // impossible - image.isNull() == true;

 painter->begin(myWidget);
 painter2->begin(myWidget); // impossible - only one painter at a time
```

### `void QPainter::beginNativePainting()`

**作用与语义：**

刷新绘画流水线，并为用户直接向底层图形上下文发送命令做准备。必须接着调用 `endNativePainting()`。
注意，只有底层绘图引擎更改的状态会被重置为各自的默认状态。我们重置的状态可能会随着版本而变化。OpenGL 2 引擎中目前重置的状态如下：
- 禁用混合
- 深度、模板和剪刀测试被禁用
- 活动纹理单元重置为0
- 深度遮罩、深度函数和净深度重置为默认值
- 模板遮罩、模板操作和模板功能被重置为默认值
- 当前颜色重置为纯白色
例如，如果用户在 beginNativePaint()/`endNativePainting()` 块内更改了 OpenGL 多边形模式，`endNativePainting()` 不会将其重置为默认状态。这里有一个示例，展示了画家命令与原始 OpenGL 命令的混合情况：

**官方示例：**

```cpp
 QPainter painter(this);
 painter.fillRect(0, 0, 128, 128, Qt::green);
 painter.beginNativePainting();

 glEnable(GL_SCISSOR_TEST);
 glScissor(0, 0, 64, 64);

 glClearColor(1, 0, 0, 1);
 glClear(GL_COLOR_BUFFER_BIT);

 glDisable(GL_SCISSOR_TEST);

 painter.endNativePainting();
```

### `QRectF QPainter::boundingRect(const QRectF &rectangle, int flags, const QString &text)`

**作用与语义：**

返回`text`的边界矩形，显示在指定`rectangle`内绘制时的样子，使用当前设定的`font()` `flags`;也就是说，函数告诉你在给定相同参数时，`drawText()`函数将绘制在哪里。
如果`text`在指定`flags`下无法符合给定`rectangle`，函数返回所需的矩形。
`flags`论证是以下标志的位元或：
- `Qt::AlignLeft`
- `Qt::AlignRight`
- `Qt::AlignHCenter`
- `Qt::AlignTop`
- `Qt::AlignBottom`
- `Qt::AlignVCenter`
- `Qt::AlignCenter`
- `Qt::TextSingleLine`
- `Qt::TextExpandTabs`
- `Qt::TextShowMnemonic`
- `Qt::TextWordWrap`
- `Qt::TextIncludeTrailingSpaces`
如果设置多个水平或多个垂直对齐标志，则最终的对齐是未定义的。

### `QRect QPainter::boundingRect(const QRect &rectangle, int flags, const QString &text)`

**作用与语义：**

返回`text`的边界矩形，在指定`rectangle`内绘制时的形状，并使用当前设置的`font()`，`flags`。

### `QRectF QPainter::boundingRect(const QRectF &rectangle, const QString &text, const QTextOption &option = QTextOption())`

**作用与语义：**

该重载函数不再以`Qt::AlignmentFlag`和`Qt::TextFlag`的位或来指定标志，而是采用`option`参数。`QTextOption`类提供了一般富文本属性的描述。

### `QRect QPainter::boundingRect(int x, int y, int w, int h, int flags, const QString &text)`

**作用与语义：**

返回给定`text`的边界矩形，当从宽度为`w`、高度为`h`的点（`x`、`y`）开始绘制时所呈现的矩形。

### `const QBrush &QPainter::brush() const`

**作用与语义：**

还回画家当前的画笔。

### `QPoint QPainter::brushOrigin() const`

**作用与语义：**

返回当前画刷原点。更倾向于用`QPainter::brushOriginF()`来获得精确的原点。

### `[since 6.11] QPointF QPainter::brushOriginF() const`

**作用与语义：**

返回当前的画刷原点。

### `QRectF QPainter::clipBoundingRect() const`

**作用与语义：**

如果有剪辑，返回当前剪辑的边界矩形;否则返回空矩形。注意剪辑区域以逻辑坐标给出。
边界矩形并不保证一定很紧。

### `QPainterPath QPainter::clipPath() const`

**作用与语义：**

返回当前的逻辑坐标剪辑路径。
警告：`QPainter` 不会显式存储合并剪辑，因为这由底层`QPaintEngine`处理，路径需按需重建并转换为当前逻辑坐标系。这可能是一项昂贵的操作。

### `QRegion QPainter::clipRegion() const`

**作用与语义：**

返回当前设置的剪辑区域。注意剪辑区域以逻辑坐标表示。
警告：`QPainter` 不会显式存储合并剪辑，因为这由底层`QPaintEngine`处理，路径需按需重建并转换为当前逻辑坐标系。这可能是一项昂贵的操作。

### `QTransform QPainter::combinedTransform() const`

**作用与语义：**

返回将当前窗口/视口和世界转换结合起来的变换矩阵。

### `QPainter::CompositionMode QPainter::compositionMode() const`

**作用与语义：**

返回当前的合成模式。

### `QPaintDevice *QPainter::device() const`

**作用与语义：**

返回该画家当前正在作画的绘画设备，若画家未活跃则`nullptr`。

### `const QTransform &QPainter::deviceTransform() const`

**作用与语义：**

返回从逻辑坐标转换为平台相关涂装设备的设备坐标的矩阵。
该函数仅在使用平台绘制命令对平台依赖的句柄（`Qt::HANDLE`）时使用，且平台本身不进行变换。
可以查询`QPaintEngine::PaintEngineFeature`枚举以确定平台是否执行这些变换。

### `void QPainter::drawArc(const QRectF &rectangle, int startAngle, int spanAngle)`

**作用与语义：**

绘制由给定`rectangle`、`startAngle`和`spanAngle`定义的弧。
`startAngle`和`spanAngle`必须以1/16度表示，即圆圈等于5760（16乘360）。正值表示逆时针方向，负数表示顺时针方向。零度位于3点钟方向。
- '`: `QRectF' 矩形（10.0， 20.0， 80.0， 60.0）;
int startAngle = 30 * 16;
整数 spanAngle = 120 * 16;

`QPainter`画家（此）;
painter.drawArc（rectangle， startAngle， spanAngle）;

### `void QPainter::drawArc(const QRect &rectangle, int startAngle, int spanAngle)`

**作用与语义：**

绘制由给定`rectangle`、`startAngle`和`spanAngle`所定义的弧。

### `void QPainter::drawArc(int x, int y, int width, int height, int startAngle, int spanAngle)`

**作用与语义：**

绘制由从（`x`， `y`）开始的矩形定义的弧线，具有指定的`width`和`height`，以及给定的`startAngle`和`spanAngle`。

### `void QPainter::drawChord(const QRectF &rectangle, int startAngle, int spanAngle)`

**作用与语义：**

绘制由给定`rectangle`、`startAngle`和`spanAngle`定义的和弦。和弦填充当前`brush()`。
起始角和spanAngle必须以1/16度表示，即一个完整的圆圈等于5760（16乘360）。角度的正值表示逆时针方向，负值表示顺时针方向。零度位于3点钟方向。
- '`: `QRectF' 矩形（10.0， 20.0， 80.0， 60.0）;
int startAngle = 30 * 16;
整数 spanAngle = 120 * 16;

`QPainter`画家（此）;
painter.drawChord（rect， startAngle， spanAngle）;

### `void QPainter::drawChord(const QRect &rectangle, int startAngle, int spanAngle)`

**作用与语义：**

绘制由给定`rectangle`、`startAngle`和`spanAngle`定义的弦。

### `void QPainter::drawChord(int x, int y, int width, int height, int startAngle, int spanAngle)`

**作用与语义：**

绘制由从（`x`， `y`）开始的矩形定义的弦，矩形为指定的`width`和`height`，以及给定的`startAngle`和`spanAngle`。

### `void QPainter::drawConvexPolygon(const QPointF *points, int pointCount)`

**作用与语义：**

`points`当前笔绘制由数组中前`pointCount`点定义的凸多边形。
- '`: static const `QPointF' 点[4] = {
`QPointF`（10.0， 80.0），。
`QPointF`（20.0， 10.0），。
`QPointF`（80.0， 30.0），。
`QPointF`（90.0， 70.0）。
};

`QPainter`画家（此）;
painter.drawConvexPolygon（点，4）;
第一个点隐式连接到最后一个点，多边形被当前`brush()`填充。如果提供的多边形不是凸的，即至少有一个角度大于180度，结果是未定义的。
在某些平台上（例如 X11），drawConvexPolygon() 函数可能比 `drawPolygon()` 函数更快。

### `void QPainter::drawConvexPolygon(const QPolygon &polygon)`

**作用与语义：**

用当前的笔和画笔绘制由`polygon`定义的凸多边形。

### `void QPainter::drawConvexPolygon(const QPolygonF &polygon)`

**作用与语义：**

用当前的笔和画笔绘制由`polygon`定义的凸多边形。

### `void QPainter::drawConvexPolygon(const QPoint *points, int pointCount)`

**作用与语义：**

使用当前笔绘制由数组中前`pointCount`点定义的凸多边形`points`。

### `void QPainter::drawEllipse(const QRectF &rectangle)`

**作用与语义：**

绘制由给定`rectangle`定义的椭圆。
填充椭圆的大小为`rectangle`。`size()`。描边椭圆的大小为`rectangle`。`size()`加上笔宽。
- “`: `QRectF”矩形（10.0， 20.0， 80.0， 60.0）;

`QPainter`画家（此）;
painter.drawEllipse（矩形）;

### `void QPainter::drawEllipse(const QRect &rectangle)`

**作用与语义：**

绘制由给定`rectangle`定义的椭圆。

### `void QPainter::drawEllipse(const QPoint &center, int rx, int ry)`

**作用与语义：**

绘制位于`center`的椭圆，半径为`rx`和`ry`。

### `void QPainter::drawEllipse(const QPointF &center, qreal rx, qreal ry)`

**作用与语义：**

绘制位于`center`的椭圆，半径为`rx`和`ry`。

### `void QPainter::drawEllipse(int x, int y, int width, int height)`

**作用与语义：**

绘制由从（`x`， `y`）起始的矩形定义的椭圆，且`width`和`height`。

### `void QPainter::drawGlyphRun(const QPointF &position, const QGlyphRun &glyphs)`

**作用与语义：**

绘制`glyphs`表示的字形`position`。`position`为字形串的基线边缘。字形将从`glyphs`和由`glyphs`位置给出的偏移量中提取。

### `void QPainter::drawImage(const QRectF &target, const QImage &image, const QRectF &source, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**作用与语义：**

将给定`image` `source`矩形部分画入绘画装置中的`target`矩形。
注意：如果图片和矩形大小不一致，图片会根据矩形大小进行缩放。
注意：关于`QImage::devicePixelRatio()`如何影响图像和图像的高分辨率版本，请参见“绘制高分辨率版本”。
如果需要修改图像以适应较低分辨率的结果（例如从32位转换为8位），请使用`flags`指定你希望如何实现。

### `void QPainter::drawImage(const QPoint &point, const QImage &image)`

**作用与语义：**

在给定`point`抽取给定`image`。

### `void QPainter::drawImage(const QPointF &point, const QImage &image)`

**作用与语义：**

在给定`point`抽取给定`image`。

### `void QPainter::drawImage(const QRect &rectangle, const QImage &image)`

**作用与语义：**

将给定`image`纳入给定的`rectangle`。
注意：如果图片和矩形大小不一致，图片会根据矩形大小进行缩放。

### `void QPainter::drawImage(const QRectF &rectangle, const QImage &image)`

**作用与语义：**

将给定`image`纳入给定的`rectangle`。
注意：如果图片和矩形大小不一致，图片会根据矩形大小进行缩放。

### `void QPainter::drawImage(const QPoint &point, const QImage &image, const QRect &source, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**作用与语义：**

绘制给定`image` `source`矩形部分，原点为给定`point`。

### `void QPainter::drawImage(const QPointF &point, const QImage &image, const QRectF &source, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**作用与语义：**

绘制给定`image` `source`矩形部分，原点为给定`point`。

### `void QPainter::drawImage(const QRect &target, const QImage &image, const QRect &source, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**作用与语义：**

将给定`image` `source`矩形部分画入绘画装置中的`target`矩形。
注意：如果图片和矩形大小不一致，图片会根据矩形大小进行缩放。

### `void QPainter::drawImage(int x, int y, const QImage &image, int sx = 0, int sy = 0, int sw = -1, int sh = -1, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**作用与语义：**

通过将`image`的一部分复制到绘画设备`y` `x`中，绘制图像。
（`x`， `y`） 指定绘图装置中要绘制的左上角点。（`sx`， `sy`） 指定`image`中要绘制的左上角点。默认为 （0， 0）。
（`sw`， `sh`）指定要绘制图像的大小。默认的（0， 0）（和负数）表示一直到图像的右下角。

### `void QPainter::drawLine(const QLineF &line)`

**作用与语义：**

画出一条由`line`定义的线。
- '`: `QLineF' 行（10.0， 80.0， 90.0， 20.0）;

`QPainter`画家（本作）;
画家.drawLine（线）;

### `void QPainter::drawLine(const QLine &line)`

**作用与语义：**

画出一条由`line`定义的线。

### `void QPainter::drawLine(const QPoint &p1, const QPoint &p2)`

**作用与语义：**

从`p1`到`p2`划一条线。

### `void QPainter::drawLine(const QPointF &p1, const QPointF &p2)`

**作用与语义：**

从`p1`到`p2`划一条线。

### `void QPainter::drawLine(int x1, int y1, int x2, int y2)`

**作用与语义：**

从（`x1`， `y1`）到（`x2`， `y2`）画一条线。

### `void QPainter::drawLines(const QLineF *lines, int lineCount)`

**作用与语义：**

用当前的笔画数组的前`lineCount` `lines`线。

### `void QPainter::drawLines(const QList<QLine> &lines)`

**作用与语义：**

用当前的笔和画笔绘制列表`lines`定义的线条集合。

### `void QPainter::drawLines(const QList<QLineF> &lines)`

**作用与语义：**

用当前的笔和画笔绘制列表`lines`定义的线条集合。

### `void QPainter::drawLines(const QList<QPoint> &pointPairs)`

**作用与语义：**

使用当前笔为向量中的每对点画`pointPairs`一条线。

### `void QPainter::drawLines(const QList<QPointF> &pointPairs)`

**作用与语义：**

使用当前笔为向量中的每对点画`pointPairs`线。如果数组中点数为奇数，最后一个点将被忽略。

### `void QPainter::drawLines(const QLine *lines, int lineCount)`

**作用与语义：**

用当前的笔画数组的前`lineCount` `lines`线。

### `void QPainter::drawLines(const QPoint *pointPairs, int lineCount)`

**作用与语义：**

使用当前的笔绘制数组中的前`lineCount`行`pointPairs`。

### `void QPainter::drawLines(const QPointF *pointPairs, int lineCount)`

**作用与语义：**

使用当前笔绘制数组中的前`lineCount`条线`pointPairs`。线条被指定为点对，因此`pointPairs`中的条目数至少为`lineCount` × 2。

### `void QPainter::drawPath(const QPainterPath &path)`

**作用与语义：**

用当前笔描绘轮廓，当前画笔填充，`path`绘制给定画家。
- '`: `QPainterPath' 路径;
path.moveTo（20， 80）;
path.lineTo（20， 30）;
path.cubicTo（80， 0， 50， 50， 80， 80）;

`QPainter`画家（此）;
painter.drawPath（path）;

### `void QPainter::drawPicture(const QPointF &point, const QPicture &picture)`

**作用与语义：**

在给定的`point`重播给定的`picture`。
`QPicture`类是一个绘制设备，用于记录和重放`QPainter`命令。图像将绘图命令序列化到输入输出设备，格式与平台无关。所有可以在控件或像素地图上绘制的内容也可以存储在图像中。
当调用 `point` = `QPointF`（0， 0） 时，该函数与 `QPicture::play()` 完全相同。
注：画家状态由此功能保持。

### `void QPainter::drawPicture(const QPoint &point, const QPicture &picture)`

**作用与语义：**

在指定`point`重玩给定`picture`。

### `void QPainter::drawPicture(int x, int y, const QPicture &picture)`

**作用与语义：**

在点（`x`， `y`）绘制给定的`picture`。

### `void QPainter::drawPie(const QRectF &rectangle, int startAngle, int spanAngle)`

**作用与语义：**

绘制由给定`rectangle`、`startAngle`和`spanAngle`定义的饼。
馅饼里装满了当前的`brush()`。
起始角和spanAngle必须以1/16度表示，即一个完整的圆圈等于5760（16乘360）。角度的正值表示逆时针方向，负值表示顺时针方向。零度位于3点钟方向。
- '`: `QRectF' 矩形（10.0， 20.0， 80.0， 60.0）;
int startAngle = 30 * 16;
整数 spanAngle = 120 * 16;

`QPainter`画家（此）;
painter.drawPie（rectangle， startAngle， spanAngle）;

### `void QPainter::drawPie(const QRect &rectangle, int startAngle, int spanAngle)`

**作用与语义：**

绘制由给定`rectangle`、`startAngle`和`spanAngle`定义的饼。

### `void QPainter::drawPie(int x, int y, int width, int height, int startAngle, int spanAngle)`

**作用与语义：**

绘制由从（`x`， `y`）开始的矩形定义的饼，矩形为指定的`width`和`height`，以及给定的`startAngle`和`spanAngle`。

### `void QPainter::drawPixmap(const QRectF &target, const QPixmap &pixmap, const QRectF &source)`

**作用与语义：**

将给定`pixmap` `source`矩形部分绘制到绘画装置中的指定`target`中。
注意：如果像素图和矩形大小不一致，像素地图会根据矩形大小进行缩放。
注意：关于`QPixmap::devicePixelRatio()`如何影响图像，请参见“绘制高分辨率像素地图和图像版本”。
如果`pixmap`是`QBitmap`，则用笔颜色“设置”的位绘制。如果`backgroundMode`为`Qt::OpaqueMode`，则“未设置”的位使用背景画笔的颜色绘制;如果`backgroundMode`为`Qt::TransparentMode`，则“未设置”的位是透明的。不支持绘制带有渐变色或纹理颜色的位图。

### `void QPainter::drawPixmap(const QPoint &point, const QPixmap &pixmap)`

**作用与语义：**

绘制给定`pixmap`，其原点为给定`point`。

### `void QPainter::drawPixmap(const QPointF &point, const QPixmap &pixmap)`

**作用与语义：**

绘制给定`pixmap`，其原点为给定`point`。

### `void QPainter::drawPixmap(const QRect &rectangle, const QPixmap &pixmap)`

**作用与语义：**

将给定`pixmap`抽入给定`rectangle`。
注意：如果像素图和矩形大小不一致，像素地图会根据矩形大小进行缩放。

### `void QPainter::drawPixmap(const QPoint &point, const QPixmap &pixmap, const QRect &source)`

**作用与语义：**

绘制给定`pixmap` `source`矩形部分，其原点为给定`point`。

### `void QPainter::drawPixmap(const QPointF &point, const QPixmap &pixmap, const QRectF &source)`

**作用与语义：**

绘制给定`pixmap` `source`矩形部分，其原点为给定`point`。

### `void QPainter::drawPixmap(const QRect &target, const QPixmap &pixmap, const QRect &source)`

**作用与语义：**

将给定`pixmap` `source`矩形部分画入绘画装置中的指定`target`。
注意：如果像素图和矩形大小不一致，像素地图会根据矩形大小进行缩放。

### `void QPainter::drawPixmap(int x, int y, const QPixmap &pixmap)`

**作用与语义：**

在位置（`x`，`y`）绘制给定的`pixmap`。

### `void QPainter::drawPixmap(int x, int y, int width, int height, const QPixmap &pixmap)`

**作用与语义：**

将`pixmap`画入矩形，位置为（`x`，`y`），并`height`给定`width`。

### `void QPainter::drawPixmap(int x, int y, const QPixmap &pixmap, int sx, int sy, int sw, int sh)`

**作用与语义：**

通过将给定`pixmap`的一部分复制到绘图设备中，绘制像素映射（`x`， `y`）。
（`x`， `y`） 指定绘制装置中要绘制的左上角点。（`sx`， `sy`） 指定`pixmap`中要绘制的左上点。默认为 （0， 0）。
（`sw`， `sh`）指定要绘制的像素图大小。默认的（0， 0）（和负数）意味着一直到像素图的右下角。

### `void QPainter::drawPixmap(int x, int y, int w, int h, const QPixmap &pixmap, int sx, int sy, int sw, int sh)`

**作用与语义：**

绘制矩形部分，原点为（`sx`， `sy`）、宽度`sw`、高度`sh` `pixmap`，位于点（`x`， `y`），宽度为`w`，高度为`h`。如果sw或sh等于零，则使用像素图的宽度/高度，并由偏移sx/sy调整;

### `void QPainter::drawPixmapFragments(const QPainter::PixmapFragment *fragments, int fragmentCount, const QPixmap &pixmap, QPainter::PixmapFragmentHints hints = PixmapFragmentHints())`

**作用与语义：**

该函数用于绘制`pixmap`，即`pixmap`子矩形，分布在多个不同比例、旋转和透明度的位置。`fragments` 是一个由`fragmentCount`元素组成的数组，指定绘制每个像素图片段所用参数。`hints`参数可用于传递绘图提示。
该功能可能比多次调用`drawPixmap()`更快，因为后端可以优化状态变化。

### `void QPainter::drawPoint(const QPointF &position)`

**作用与语义：**

用当前笔的颜色在给定`position`画一个点。

### `void QPainter::drawPoint(const QPoint &position)`

**作用与语义：**

用当前笔的颜色在给定`position`画一个点。

### `void QPainter::drawPoint(int x, int y)`

**作用与语义：**

在位置（`x`，`y`）抽取一个点。

### `void QPainter::drawPoints(const QPointF *points, int pointCount)`

**作用与语义：**

`points`使用当前笔的颜色绘制数组中的前`pointCount`点。

### `void QPainter::drawPoints(const QPolygon &points)`

**作用与语义：**

绘制向量中的点`points`。

### `void QPainter::drawPoints(const QPolygonF &points)`

**作用与语义：**

绘制向量中的点`points`。

### `void QPainter::drawPoints(const QPoint *points, int pointCount)`

**作用与语义：**

`points`使用当前笔的颜色绘制数组中的前`pointCount`点。

### `void QPainter::drawPolygon(const QPointF *points, int pointCount, Qt::FillRule fillRule = Qt::OddEvenFill)`

**作用与语义：**

使用当前的笔和画笔绘制数组中前`pointCount`点定义的多边形`points`。
- '`: static const `QPointF' 点[4] = {
`QPointF`（10.0， 80.0），。
`QPointF`（20.0， 10.0），。
`QPointF`（80.0， 30.0），。
`QPointF`（90.0， 70.0）。
};

`QPainter`画家（此）;
painter.drawPolygon（点，4）;
第一个点隐式连接到最后一个点，多边形被当前`brush()`填充。
如果`fillRule` `Qt::WindingFill`，则使用绕过填充算法填充多边形。如果`fillRule` `Qt::OddEvenFill`，则使用奇偶填充算法填充多边形。关于这些填充规则的更详细描述，请参见 `Qt::FillRule`。

### `void QPainter::drawPolygon(const QPolygon &points, Qt::FillRule fillRule = Qt::OddEvenFill)`

**作用与语义：**

使用填充规则 `fillRule` 绘制由给定`points`定义的多边形。

### `void QPainter::drawPolygon(const QPolygonF &points, Qt::FillRule fillRule = Qt::OddEvenFill)`

**作用与语义：**

使用填充规则 `fillRule` 绘制由给定`points`定义的多边形。

### `void QPainter::drawPolygon(const QPoint *points, int pointCount, Qt::FillRule fillRule = Qt::OddEvenFill)`

**作用与语义：**

绘制由数组中前`pointCount`点定义的多边形`points`。

### `void QPainter::drawPolyline(const QPointF *points, int pointCount)`

**作用与语义：**

用当前笔绘制`points`中前`pointCount`点定义的多段线。
注意，与`drawPolygon()`函数不同，最后一个点不与第一个点相连，多条线也未被填充。

### `void QPainter::drawPolyline(const QPolygon &points)`

**作用与语义：**

用当前笔绘制给定`points`定义的多段线。

### `void QPainter::drawPolyline(const QPolygonF &points)`

**作用与语义：**

用当前笔绘制给定`points`定义的多段线。

### `void QPainter::drawPolyline(const QPoint *points, int pointCount)`

**作用与语义：**

使用当前笔绘制`points`中前`pointCount`点所定义的多段线。

### `void QPainter::drawRect(const QRectF &rectangle)`

**作用与语义：**

用当前的笔和画笔绘制当前`rectangle`。
填充矩形的大小为`rectangle`。`size()`。带笔画的矩形大小为`rectangle`。`size()`加上笔宽。
- '`: `QRectF' 矩形（10.0， 20.0， 80.0， 60.0）;

`QPainter`画家（此）;
painter.drawRect（矩形）;

### `void QPainter::drawRect(const QRect &rectangle)`

**作用与语义：**

用当前的笔和画笔画出当前的`rectangle`。

### `void QPainter::drawRect(int x, int y, int width, int height)`

**作用与语义：**

绘制一个矩形，左上角位于（`x`， `y`），`width`和`height`。

### `void QPainter::drawRects(const QRectF *rectangles, int rectCount)`

**作用与语义：**

用当前的笔和画笔绘制给定`rectangles`的第一个`rectCount`。

### `void QPainter::drawRects(const QList<QRect> &rectangles)`

**作用与语义：**

用当前的笔和画笔绘制给定的`rectangles`。

### `void QPainter::drawRects(const QList<QRectF> &rectangles)`

**作用与语义：**

用当前的笔和画笔绘制给定的`rectangles`。

### `void QPainter::drawRects(const QRect *rectangles, int rectCount)`

**作用与语义：**

用当前的笔和画笔绘制给定`rectangles`的第一个`rectCount`。

### `void QPainter::drawRoundedRect(const QRectF &rect, qreal xRadius, qreal yRadius, Qt::SizeMode mode = Qt::AbsoluteSize)`

**作用与语义：**

绘制给定的矩形`rect`圆角。
`xRadius`和`yRadius`参数指定了定义圆角矩形角的椭圆半径。当`mode`为`Qt::RelativeSize`时，`xRadius`和`yRadius`分别以矩形宽度和高度的一半百分比表示，应在0.0到100.0之间。
填充矩形的大小为矩形。`size()`。带笔画的矩形大小为矩形。`size()`加上笔宽。
- “`: `QRectF”矩形（10.0， 20.0， 80.0， 60.0）;

`QPainter`画家（此）;
painter.drawRoundedRect（矩形，20.0,15.0）;

### `void QPainter::drawRoundedRect(const QRect &rect, qreal xRadius, qreal yRadius, Qt::SizeMode mode = Qt::AbsoluteSize)`

**作用与语义：**

绘制给定的矩形`rect`，带有圆角。

### `void QPainter::drawRoundedRect(int x, int y, int w, int h, qreal xRadius, qreal yRadius, Qt::SizeMode mode = Qt::AbsoluteSize)`

**作用与语义：**

绘制给定矩形`x`、`y`、`w`、`h`，角为圆角。

### `void QPainter::drawStaticText(const QPointF &topLeftPosition, const QStaticText &staticText)`

**作用与语义：**

在给定`topLeftPosition`抽取给定`staticText`。
文本将使用画家上的字体和变换集绘制。如果画家上的字体和/或变换集与用于初始化`QStaticText`布局的不符，则需要重新计算布局。使用`QStaticText::prepare()`初始化`staticText`，使用字体和后续绘制的变换。
如果`topLeftPosition`与`staticText`初始化时或上次绘制时不同，那么在将文本翻译到新位置时会有轻微的开销。
注意：如果画家的变换不是仿射，则`staticText`将通过常规调用来`drawText()`绘制，从而失去性能提升的潜力。
注意：y 位置用作字体顶部。

### `void QPainter::drawStaticText(const QPoint &topLeftPosition, const QStaticText &staticText)`

**作用与语义：**

`topLeftPosition`处画`staticText`。
注意：y 位置用作字体顶部。

### `void QPainter::drawStaticText(int left, int top, const QStaticText &staticText)`

**作用与语义：**

在坐标`left`和`top`绘制`staticText`。
注意：y 位置用作字体顶部。

### `void QPainter::drawText(const QPointF &position, const QString &text)`

**作用与语义：**

从给定的`position`开始，绘制当前定义的文本方向的给定`text`。
该函数不处理换行字符（\n），因为它不能将文本拆分成多行，也无法显示换行字符。如果你想用换行字符绘制多行文本，或者想让文本被环绕，可以使用QPainter：:d rawText()重载，它会取一个矩形。
默认情况下，`QPainter`会用抗锯齿绘制文本。
注意：y 位置用作字体的基线。

### `void QPainter::drawText(const QPoint &position, const QString &text)`

**作用与语义：**

从给定`position`开始绘制当前定义的文本方向的给定`text`。
默认情况下，`QPainter`会进行抗锯齿绘制文本。
注意：y 位置用作字体的基线。

### `void QPainter::drawText(const QRectF &rectangle, const QString &text, const QTextOption &option = QTextOption())`

**作用与语义：**

利用`option`控制`rectangle`的位置、方向和方向，绘制指定`text`。`option`中提供的选项覆盖了`QPainter`对象本身设置的选项。
默认情况下，`QPainter`会用抗锯齿绘制文本。
注意：`rectangle`的y坐标作为字体顶部。

### `void QPainter::drawText(int x, int y, const QString &text)`

**作用与语义：**

使用画家当前定义的文本方向，在位置（`x`、`y`）绘制给定的`text`。
默认情况下，`QPainter`会进行抗锯齿绘制文本。
注意：y 位置用作字体的基线。

### `void QPainter::drawText(const QRect &rectangle, int flags, const QString &text, QRect *boundingRect = nullptr)`

**作用与语义：**

根据规定的`flags`，在所给`rectangle`内绘制给定的`text`。
`boundingRect`（如果不是空）设置为边界矩形应有的大小，以便包围整个文本。例如，在下图中，虚线表示函数计算的 `boundingRect`，虚线表示`rectangle`：
- '`: `QPainter' 画师（此）;
`QFont` font = painter.font();
font.setPixelSize（48）;
painter.setFont（font）;

cont `QRect`矩形 = `QRect`（0， 0， 100， 50）;
`QRect` boundingRect;
painter.drawText（rectangle， 0， tr（“Hello”）和boundingRect）;

`QPen` 笔 = 画家。笔();
pen.setStyle（Qt：:D otLine）;
painter.setPen（钢笔）;
painter.drawRect（boundingRect.adjusted（0， 0， -pen.width()， -pen.width()）;

pen.setStyle（Qt：:D ashLine）;
painter.setPen（钢笔）;
painter.drawRect（rectangle.adjusted（0， 0， -pen.width()， -pen.width()）;
默认情况下，`QPainter`会进行抗锯齿绘制文本。
注意：`rectangle`的y坐标用作字体顶部。

### `void QPainter::drawText(const QRectF &rectangle, int flags, const QString &text, QRectF *boundingRect = nullptr)`

**作用与语义：**

在所给`rectangle`内绘制给定`text`。`rectangle`与对齐`flags`共同定义了`text`的锚点。
- '`: `QPainter' 画师（此）;
painter.drawText（rect， Qt：：AlignCenter， tr（“Qt\nProject”））;
`boundingRect`（如果不是空）设置为包围整个文本的边界矩形。例如，在下图中，虚线表示函数计算的 `boundingRect`，虚线表示`rectangle`：
- '`: `QPainter' 画师（此）;
`QFont` font = painter.font();
font.setPixelSize（48）;
painter.setFont（font）;

cont `QRect`矩形 = `QRect`（0， 0， 100， 50）;
`QRect` boundingRect;
painter.drawText（rectangle， 0， tr（“Hello”）和boundingRect）;

`QPen` 笔 = 画家。笔();
pen.setStyle（Qt：:D otLine）;
painter.setPen（钢笔）;
painter.drawRect（boundingRect.adjusted（0， 0， -pen.width()， -pen.width()）;

pen.setStyle（Qt：:D ashLine）;
painter.setPen（钢笔）;
painter.drawRect（rectangle.adjusted（0， 0， -pen.width()， -pen.width()）;
`flags`论元是以下标志的位元或：
- `Qt::AlignLeft`
- `Qt::AlignRight`
- `Qt::AlignHCenter`
- `Qt::AlignJustify`
- `Qt::AlignTop`
- `Qt::AlignBottom`
- `Qt::AlignVCenter`
- `Qt::AlignCenter`
- `Qt::TextDontClip`
- `Qt::TextSingleLine`
- `Qt::TextExpandTabs`
- `Qt::TextShowMnemonic`
- `Qt::TextWordWrap`
- `Qt::TextIncludeTrailingSpaces`
默认情况下，`QPainter`会进行抗锯齿绘制文字。
注意：`rectangle`的y坐标用作字体顶部。

### `void QPainter::drawText(int x, int y, int width, int height, int flags, const QString &text, QRect *boundingRect = nullptr)`

**作用与语义：**

在矩形内绘制给定的`text`，原点为（`x`、`y`）、`width`和`height`。
`boundingRect`（如果不是空）设置为边界矩形应有的大小，以便包围整个文本。例如，在下图中，虚线表示由函数计算的 `boundingRect`，虚线表示由 `x`、`y`、`width` 和 `height` 定义的矩形：
- '`: `QPainter' 画师（此）;
`QFont` font = painter.font();
font.setPixelSize（48）;
painter.setFont（font）;

cont `QRect`矩形 = `QRect`（0， 0， 100， 50）;
`QRect` boundingRect;
painter.drawText（rectangle， 0， tr（“Hello”）和boundingRect）;

`QPen` 笔 = 画家。笔();
pen.setStyle（Qt：:D otLine）;
painter.setPen（钢笔）;
painter.drawRect（boundingRect.adjusted（0， 0， -pen.width()， -pen.width()）;

pen.setStyle（Qt：:D ashLine）;
painter.setPen（钢笔）;
painter.drawRect（rectangle.adjusted（0， 0， -pen.width()， -pen.width()）;
`flags`论证是以下标志的位元或：
- `Qt::AlignLeft`
- `Qt::AlignRight`
- `Qt::AlignHCenter`
- `Qt::AlignJustify`
- `Qt::AlignTop`
- `Qt::AlignBottom`
- `Qt::AlignVCenter`
- `Qt::AlignCenter`
- `Qt::TextSingleLine`
- `Qt::TextExpandTabs`
- `Qt::TextShowMnemonic`
- `Qt::TextWordWrap`
默认情况下，`QPainter`会进行抗锯齿绘制文本。
注意：y 位置用作字体顶部。

### `void QPainter::drawTiledPixmap(const QRectF &rectangle, const QPixmap &pixmap, const QPointF &position = QPointF())`

**作用与语义：**

在给定`rectangle`内绘制一个瓦片`pixmap`，其起点位于给定`position`。
调用 drawTiledPixmap() 类似于多次调用 `drawPixmap()` 来填充（铺装）一个区域，但根据底层窗口系统，效率可能更高。
drawTiledPixmap() 在高 dpi 显示器（devicePixelRatio > 1）上会产生与普通 dpi 显示器相同的视觉拼贴图案。在`pixmap`上设置 devicePixelRatio 以控制图块大小。例如，将其设置为 2 倍，tile 宽度和高度（无论是在 1x 显示器上还是 2x 显示器上），在 2x 显示器上也能产生高分辨率输出。
`position`偏移量以设备独立像素相对于`rectangle`左上角提供。该`position`可用于对齐`rectangle`内的重复图案。

### `void QPainter::drawTiledPixmap(const QRect &rectangle, const QPixmap &pixmap, const QPoint &position = QPoint())`

**作用与语义：**

在给定`rectangle`内绘制一个瓷砖`pixmap`，其起点位于给定`position`。

### `void QPainter::drawTiledPixmap(int x, int y, int width, int height, const QPixmap &pixmap, int sx = 0, int sy = 0)`

**作用与语义：**

在指定的矩形中绘制一个瓷砖`pixmap`。
（`x`，`y`）指定了要绘制的绘画装置左上角;并附上给定的`width`和`height`。
（`sx`， `sy`） 指定像素映射绘制的指定矩形内的原点。原点位置以设备无关像素相对于 （`x`， `y`） 指定。默认为 （0， 0）。

### `bool QPainter::end()`

**作用与语义：**

结束绘画。绘画过程中使用的资源会被释放。通常不需要调用，因为它是由毁灭者调用的。
如果画家不再活跃，则返回`true`;否则返回`false`。

### `void QPainter::endNativePainting()`

**作用与语义：**

手动发送本地绘画命令后恢复画家。允许画家在调用其他画家命令前恢复它依赖的任何原生状态。

### `void QPainter::eraseRect(const QRectF &rectangle)`

**作用与语义：**

抹去给定`rectangle`内的区域。等同于调用。

**官方示例：**

```cpp
 fillRect(rectangle, background());
```

### `void QPainter::eraseRect(const QRect &rectangle)`

**作用与语义：**

抹去给定`rectangle`内的区域。

### `void QPainter::eraseRect(int x, int y, int width, int height)`

**作用与语义：**

用给定的`width`和`height`擦除矩形内从（`x`， `y`）开始的区域。

### `void QPainter::fillPath(const QPainterPath &path, const QBrush &brush)`

**作用与语义：**

用给定的`brush`填充给定的`path`。轮廓不画。
或者，你可以指定一个`QColor`而不是`QBrush`;`QBrush`构造函数（取一个`QColor`参数）会自动生成一个实心图案画刷。

### `void QPainter::fillRect(const QRectF &rectangle, const QBrush &brush)`

**作用与语义：**

用指定`brush`填充给定`rectangle`。
或者，你可以指定一个`QColor`而不是`QBrush`;`QBrush`构造函数（取一个`QColor`参数）会自动创建一个实心图案画刷。

### `void QPainter::fillRect(const QRect &rectangle, QGradient::Preset preset)`

**作用与语义：**

用指定的梯度`preset`填充给定的`rectangle`。

### `void QPainter::fillRect(const QRect &rectangle, Qt::BrushStyle style)`

**作用与语义：**

用指定的画刷填充给定`rectangle` `style`。

### `void QPainter::fillRect(const QRect &rectangle, Qt::GlobalColor color)`

**作用与语义：**

用指定的`color`填充给定的`rectangle`。

### `void QPainter::fillRect(const QRect &rectangle, const QBrush &brush)`

**作用与语义：**

用指定的`brush`填充给定的`rectangle`。

### `void QPainter::fillRect(const QRect &rectangle, const QColor &color)`

**作用与语义：**

用指定的`color`填充给定的`rectangle`。

### `void QPainter::fillRect(const QRectF &rectangle, QGradient::Preset preset)`

**作用与语义：**

用指定的梯度`preset`填充给定的`rectangle`。

### `void QPainter::fillRect(const QRectF &rectangle, Qt::BrushStyle style)`

**作用与语义：**

用指定的画刷填充给定`rectangle` `style`。

### `void QPainter::fillRect(const QRectF &rectangle, Qt::GlobalColor color)`

**作用与语义：**

用指定的`color`填充给定的`rectangle`。

### `void QPainter::fillRect(const QRectF &rectangle, const QColor &color)`

**作用与语义：**

用指定的`color`填充给定的`rectangle`。

### `void QPainter::fillRect(int x, int y, int width, int height, QGradient::Preset preset)`

**作用与语义：**

用给定的梯度`preset`填充从（`x`， `y`）开始的矩形，`width`和`height`。

### `void QPainter::fillRect(int x, int y, int width, int height, Qt::BrushStyle style)`

**作用与语义：**

用指定的刷`style`子填充从（`x`， `y`）开始的矩形，`width`和`height`。

### `void QPainter::fillRect(int x, int y, int width, int height, Qt::GlobalColor color)`

**作用与语义：**

用给定的`color`填充从（`x`， `y`）开始的矩形，使用给定的`width`和`height`。

### `void QPainter::fillRect(int x, int y, int width, int height, const QBrush &brush)`

**作用与语义：**

用给定的`brush`填充从（`x`， `y`）开始的矩形，`width`和`height`。

### `void QPainter::fillRect(int x, int y, int width, int height, const QColor &color)`

**作用与语义：**

用给定的`color`填充从（`x`， `y`）开始的矩形，使用给定的`width`和`height`。

### `const QFont &QPainter::font() const`

**作用与语义：**

返回当前用于绘制文本的设置字体。

### `QFontInfo QPainter::fontInfo() const`

**作用与语义：**

如果画家处于激活状态，则返回画家的字体信息。否则，返回值未定义。

### `QFontMetrics QPainter::fontMetrics() const`

**作用与语义：**

如果画家处于激活状态，则返回该画家的字体度量。否则，返回值未定义。

### `bool QPainter::hasClipping() const`

**作用与语义：**

如果已设置裁剪，则返回 `true`；否则返回 `false`。

### `bool QPainter::isActive() const`

**作用与语义：**

返回`true`如果`begin()`已被称为并且`end()`尚未被调用；否则返回`false`。

### `Qt::LayoutDirection QPainter::layoutDirection() const`

**作用与语义：**

返回画家绘制文字时使用的布局方向。

### `qreal QPainter::opacity() const`

**作用与语义：**

返回画家的不透明度。默认值是1。

### `QPaintEngine *QPainter::paintEngine() const`

**作用与语义：**

如果油漆工处于激活状态，返回当前操作的油漆引擎;否则为0。

### `const QPen &QPainter::pen() const`

**作用与语义：**

归还画家现在的笔。

### `QPainter::RenderHints QPainter::renderHints() const`

**作用与语义：**

返回一个标志，指定为该画家设置的渲染提示。

### `void QPainter::resetTransform()`

**作用与语义：**

重置使用`translate()`、`scale()`、`shear()`、`rotate()`、`setWorldTransform()`、`setViewport()`和`setWindow()`所做的所有变换。

### `void QPainter::restore()`

**作用与语义：**

恢复当前的画家状态（从栈中弹出已保存状态）。

### `void QPainter::rotate(qreal angle)`

**作用与语义：**

顺时针旋转坐标系。给定的`angle`参数以度为单位。

### `void QPainter::save()`

**作用与语义：**

保存当前的画家状态（将状态推入栈）。save() 后必须跟相应的 `restore()`;`end()` 函数会解开栈。

### `void QPainter::scale(qreal sx, qreal sy)`

**作用与语义：**

坐标系按（`sx`， `sy`）缩放。

### `void QPainter::setBackground(const QBrush &brush)`

**作用与语义：**

将画家的背景画笔设定在给定的`brush`上。
背景刷是在绘制不透明文本、点线和位图时填充的画刷。背景刷在透明背景模式（默认模式）中没有影响。

### `void QPainter::setBackgroundMode(Qt::BGMode mode)`

**作用与语义：**

将画家的背景模式设置为给定的`mode`。
`Qt::TransparentMode`（默认）绘制点线和文字，但不设置背景像素。`Qt::OpaqueMode`用当前背景色填充这些空间。
请注意，要透明地绘制位图或像素图，必须使用`QPixmap::setMask()`。

### `void QPainter::setBrush(const QBrush &brush)`

**作用与语义：**

将画笔调到指定`brush`。
画家的画笔定义了形状的填充方式。

### `[since 6.11] void QPainter::setBrush(QBrush &&brush)`

**作用与语义：**

将画笔调到指定`brush`。
画家的画笔定义了形状的填充方式。

### `[since 6.9] void QPainter::setBrush(QColor color)`

**作用与语义：**

将画笔用指定的`color`调到实心画笔上。

### `void QPainter::setBrush(Qt::BrushStyle style)`

**作用与语义：**

将画笔设置为黑色，并设定为指定的`style`。

### `[since 6.9] void QPainter::setBrush(Qt::GlobalColor color)`

**作用与语义：**

将画笔用指定的`color`调到实心画笔上。

### `void QPainter::setBrushOrigin(const QPointF &position)`

**作用与语义：**

将画刷原点设为`position`。
画笔原点指定了画家画笔的（0， 0）坐标。
注意，虽然在Qt 3中采用父背景时需要`brushOrigin()`，但现在情况不同，因为Qt 4的画家不会绘制背景，除非你通过将控件的`autoFillBackground`属性设置为true明确指示。

### `void QPainter::setBrushOrigin(const QPoint &position)`

**作用与语义：**

将画笔的起点设定为给定的`position`。

### `void QPainter::setBrushOrigin(int x, int y)`

**作用与语义：**

将画笔的起点设定为尖点（`x`，`y`）。

### `void QPainter::setClipPath(const QPainterPath &path, Qt::ClipOperation operation = Qt::ReplaceClip)`

**作用与语义：**

启用裁剪功能，并将画家的剪辑路径设置为给定的`path`，并`operation`剪辑。
注意，剪辑路径是用逻辑坐标（画家坐标）来指定的。

### `void QPainter::setClipRect(const QRectF &rectangle, Qt::ClipOperation operation = Qt::ReplaceClip)`

**作用与语义：**

启用裁剪，并使用给定的剪辑`operation`将剪辑区域设置为给定的`rectangle`。默认操作是替换当前剪辑矩形。
注意，剪辑矩形是用逻辑坐标（画家）坐标指定的。

### `void QPainter::setClipRect(int x, int y, int width, int height, Qt::ClipOperation operation = Qt::ReplaceClip)`

**作用与语义：**

启用裁剪，并将剪辑区域设置为从（`x`， `y`）开始的矩形，并以给定的`width`和`height`。

### `void QPainter::setClipRect(const QRect &rectangle, Qt::ClipOperation operation = Qt::ReplaceClip)`

**作用与语义：**

启用裁剪功能，并使用给定的剪辑`operation`将剪辑区域设置为给定的`rectangle`。

### `void QPainter::setClipRegion(const QRegion &region, Qt::ClipOperation operation = Qt::ReplaceClip)`

**作用与语义：**

使用指定的剪辑`operation`将剪辑区域设置为给定的`region`。默认剪辑操作是替换当前剪辑区域。
注意，剪辑区域以逻辑坐标表示。

### `void QPainter::setClipping(bool enable)`

**作用与语义：**

如果`enable`为真，则启用削波;如果`enable`为假，则关闭削波。

### `void QPainter::setCompositionMode(QPainter::CompositionMode mode)`

**作用与语义：**

将合成模式设置为给定的`mode`。
警告：只有运行在`QImage`上的 `QPainter` 才完全支持所有合成模式。如`compositionMode()`所述，X11 支持 RasterOp 模式。

### `void QPainter::setFont(const QFont &font)`

**作用与语义：**

将画家字体设置为给定的`font`。
该字体被后续的 `drawText()` 函数使用。文本颜色与钢笔颜色相同。
如果你设置了一个不可用的字体，Qt 会找到一个接近的匹配字体。`font()` 会返回你用 setFont() 设置的字体，`fontInfo()` 返回实际使用的字体（可能是相同的）。

### `void QPainter::setLayoutDirection(Qt::LayoutDirection direction)`

**作用与语义：**

将画家绘制文字时使用的布局方向设置为指定的`direction`。
默认是`Qt::LayoutDirectionAuto`，这会隐含决定绘制文本的方向。

### `void QPainter::setOpacity(qreal opacity)`

**作用与语义：**

将画家的不透明度设置为`opacity`。值应在0.0到1.0之间，0.0表示完全透明，1.0表示完全不透明。
画家的不透明度集分别应用于每个绘图操作。填充形状和绘制轮廓被视为不同的绘图操作。

### `void QPainter::setPen(const QPen &pen)`

**作用与语义：**

将画家的笔设定为给定的`pen`。
`pen`定义了如何绘制线条和轮廓，也定义了文本颜色。

### `[since 6.11] void QPainter::setPen(QPen &&pen)`

**作用与语义：**

将画家的笔设定为给定的`pen`。
`pen`定义了如何绘制线条和轮廓，也定义了文本颜色。

### `void QPainter::setPen(Qt::PenStyle style)`

**作用与语义：**

将画家的笔设置为给定的笔`style`、宽度1和黑色。

### `void QPainter::setPen(const QColor &color)`

**作用与语义：**

设置画家笔的样式`Qt::SolidLine`，宽度为1，且`color`指定。

### `void QPainter::setRenderHint(QPainter::RenderHint hint, bool on = true)`

**作用与语义：**

如果`on`为真，则将给定的渲染`hint`设置给画家;否则清除渲染提示。

### `void QPainter::setRenderHints(QPainter::RenderHints hints, bool on = true)`

**作用与语义：**

如果为真，则将给定的渲染`hints`设置给画家`on`;否则清除渲染提示。

### `void QPainter::setTransform(const QTransform &transform, bool combine = false)`

**作用与语义：**

设定世界变换矩阵。如果`combine`为真，指定`transform`与当前矩阵结合;否则替换当前矩阵。

### `void QPainter::setViewTransformEnabled(bool enable)`

**作用与语义：**

如果`enable`为真，则启用视图转换;如果`enable`为假，则禁用视图转换。

### `void QPainter::setViewport(const QRect &rectangle)`

**作用与语义：**

将画家的视口矩形设置为给定的`rectangle`，并支持视图变换。
视口矩形是视角变换的一部分。视口指定设备坐标系。其姊妹窗口`window()`指定逻辑坐标系。
默认的视口矩形和设备的矩形是一样的。

### `void QPainter::setViewport(int x, int y, int width, int height)`

**作用与语义：**

将画家的视口矩形设置为从（`x`， `y`）开始的矩形，且`width`和`height`。

### `void QPainter::setWindow(const QRect &rectangle)`

**作用与语义：**

将画家窗口设置为给定的`rectangle`，并实现视图变换。
窗口矩形是视图变换的一部分。窗口指定逻辑坐标系。其姊妹窗口`viewport()`表示设备坐标系。
默认窗口矩形和设备的矩形是一样的。

### `void QPainter::setWindow(int x, int y, int width, int height)`

**作用与语义：**

将画家窗口设置为从（`x`， `y`）开始的矩形，并达到给定的`width`和`height`。

### `void QPainter::setWorldMatrixEnabled(bool enable)`

**作用与语义：**

如果`enable`为真，则启用变换;如果`enable`为假，则禁用变换。世界变换矩阵不会被更改。

### `void QPainter::setWorldTransform(const QTransform &matrix, bool combine = false)`

**作用与语义：**

设置世界变换矩阵。如果`combine`为真，指定`matrix`将与当前矩阵结合;否则替换当前矩阵。

### `void QPainter::shear(qreal sh, qreal sv)`

**作用与语义：**

对坐标系剪切为（`sh`， `sv`）。

### `void QPainter::strokePath(const QPainterPath &path, const QPen &pen)`

**作用与语义：**

用笔绘制`path`路径的轮廓（笔画），由`pen`。

### `bool QPainter::testRenderHint(QPainter::RenderHint hint) const`

**作用与语义：**

如果设置了 `hint`，则返回 `true`；否则返回 `false`。

### `const QTransform &QPainter::transform() const`

**作用与语义：**

`worldTransform()`的别名。返回世界变换矩阵。

### `void QPainter::translate(const QPointF &offset)`

**作用与语义：**

将坐标系平移为给定的`offset`;即给定`offset`相加到点上。

### `void QPainter::translate(const QPoint &offset)`

**作用与语义：**

将坐标系平移为给定`offset`。

### `void QPainter::translate(qreal dx, qreal dy)`

**作用与语义：**

将坐标系平移为向量（`dx`，`dy`）。

### `bool QPainter::viewTransformEnabled() const`

**作用与语义：**

如果启用视图变换，返回`true`;否则返回false。

### `QRect QPainter::viewport() const`

**作用与语义：**

返回视口矩形。

### `QRect QPainter::window() const`

**作用与语义：**

返回窗口矩形。

### `bool QPainter::worldMatrixEnabled() const`

**作用与语义：**

如果启用了世界变换，返回`true`;否则返回false。

### `const QTransform &QPainter::worldTransform() const`

**作用与语义：**

返回世界变换矩阵。

### `class PixmapFragment`

**作用与语义：**

该类与 QPainter：:d rawPixmapFragments() 函数结合使用，用于指定如何绘制像素地图或像素地图的子矩形态。
`sourceLeft`、`sourceTop`、`width`和`height`变量作为pixmap中的源矩形，传递到`QPainter::drawPixmapFragments()`函数中。变量`x`、`y`、`width`和`height`用于计算绘制的目标矩形。`x`和`y`表示目标矩形的中心。目标矩形中的`width`和`height`会按`scaleX`和`scaleY`的值进行比例调整。生成的目标矩形随后围绕`x`中心点旋转`rotation`度，`y`中心点。

### `enum PixmapFragmentHint { OpaqueHint }`

**作用与语义：**

- `QPainter::OpaqueHint`：`0x01`;表示要绘制的像素图片段是不透明的。不透明的片段可能绘制得更快。
PixmapFragmentHints 类型是 QFlags 的 typedef<PixmapFragmentHint>。它存储 PixmapFragmentHint 值的 OR 组合。

### `flags PixmapFragmentHints`

**作用与语义：**

- `QPainter::OpaqueHint`：`0x01`;表示要绘制的像素图片段是不透明的。不透明的片段可能绘制得更快。
PixmapFragmentHints 类型是 QFlags 的 typedef<PixmapFragmentHint>。它存储 PixmapFragmentHint 值的 OR 组合。

### `enum RenderHint { Antialiasing, TextAntialiasing, SmoothPixmapTransform, VerticalSubpixelPositioning, LosslessImageRendering, NonCosmeticBrushPatterns }`

**作用与语义：**

渲染提示用于指定 `QPainter` 的标志，这些标志可能被任何给定引擎尊重也可能不会。
- `QPainter::Antialiasing`：`0x01`;表示发动机应对原图边缘进行抗锯齿处理（如可能）。
- `QPainter::TextAntialiasing`：`0x02`;表示引擎应在可能的情况下对文本进行抗锯齿处理。要强制禁用文本的抗锯齿，请不要使用此提示。相反，请在字体样式策略中设置`QFont::NoAntialias`。
- `QPainter::SmoothPixmapTransform`：`0x04`;表示引擎应使用光滑像素图变换算法（如双线性），而非最近邻。
- `QPainter::VerticalSubpixelPositioning`：`0x08`;允许文本在垂直和水平上都按像素的比例排列，前提是字体引擎支持。目前，当`QFont::PreferNoHinting`提示偏好时，Freetype在所有平台上支持此功能，macOS也支持。对于大多数用例，这不会提升视觉质量，但可能会增加内存消耗并降低文本渲染性能。因此，除非使用场景需要，否则不建议启用此功能。其中一个用例可能是将字形与其他视觉基元对齐。该值在Qt 6.1中加入。
- `QPainter::LosslessImageRendering`：`0x40`;尽可能使用无损图像渲染。目前，该提示仅在使用 `QPainter` 通过 `QPrinter` 或 `QPdfWriter` 输出 PDF 文件时使用，`drawImage()`/`drawPixmap()` 调用将使用无损压缩算法编码图像，而非有损 JPEG 压缩。该值在 Qt 5.13 中添加。
- `QPainter::NonCosmeticBrushPatterns`：`0x80`;用预定义的图案样式之一的画笔绘制时，也要变换图案，同时变换被绘制的物体。默认情况下，图案将图案视为外观，因此图案像素将直接映射到设备像素，独立于任何主动变换。该值在Qt 6.4中添加。
RenderHints 类型是 QFlags 的 typedef<RenderHint>。它存储 RenderHint 值的 OR 组合。

### `flags RenderHints`

**作用与语义：**

渲染提示用于指定 `QPainter` 的标志，这些标志可能被任何给定引擎尊重也可能不会。
- `QPainter::Antialiasing`：`0x01`;表示发动机应对原图边缘进行抗锯齿处理（如可能）。
- `QPainter::TextAntialiasing`：`0x02`;表示引擎应在可能的情况下对文本进行抗锯齿处理。要强制禁用文本的抗锯齿，请不要使用此提示。相反，请在字体样式策略中设置`QFont::NoAntialias`。
- `QPainter::SmoothPixmapTransform`：`0x04`;表示引擎应使用光滑像素图变换算法（如双线性），而非最近邻。
- `QPainter::VerticalSubpixelPositioning`：`0x08`;允许文本在垂直和水平上都按像素的比例排列，前提是字体引擎支持。目前，当`QFont::PreferNoHinting`提示偏好时，Freetype在所有平台上支持此功能，macOS也支持。对于大多数用例，这不会提升视觉质量，但可能会增加内存消耗并降低文本渲染性能。因此，除非使用场景需要，否则不建议启用此功能。其中一个用例可能是将字形与其他视觉基元对齐。该值在Qt 6.1中加入。
- `QPainter::LosslessImageRendering`：`0x40`;尽可能使用无损图像渲染。目前，该提示仅在使用 `QPainter` 通过 `QPrinter` 或 `QPdfWriter` 输出 PDF 文件时使用，`drawImage()`/`drawPixmap()` 调用将使用无损压缩算法编码图像，而非有损 JPEG 压缩。该值在 Qt 5.13 中添加。
- `QPainter::NonCosmeticBrushPatterns`：`0x80`;用预定义的图案样式之一的画笔绘制时，也要变换图案，同时变换被绘制的物体。默认情况下，图案将图案视为外观，因此图案像素将直接映射到设备像素，独立于任何主动变换。该值在Qt 6.4中添加。
RenderHints 类型是 QFlags 的 typedef<RenderHint>。它存储 RenderHint 值的 OR 组合。

## 6. 深入实践与常见坑

### 生命周期和资源边界

绘制上下文必须绑定有效的 paint device，并在合法的绘制阶段使用。QWidget 上通常只在 `paintEvent()` 内创建 painter；离屏图像、打印设备和 pixmap 则有各自的设备生命周期。

### 状态和错误边界

`save()`/`restore()` 用于隔离局部状态；改变坐标系、画笔或合成模式后要么恢复，要么明确后续绘制也需要该状态。重绘请求和真正绘制是两个阶段，业务状态变化应调用 `update()`。

### 线程边界

同一个 GUI 控件的绘制在 GUI 线程完成；离屏 QImage 可以按数据所有权在后台处理，但不要让后台线程直接绘制或访问正在显示的 QWidget/QPixmap 资源。

### 最容易出现的错误

不要在 paintEvent 外永久缓存 QPainter；不要忘记高 DPI 和坐标系；绘制时避免改变业务状态；使用 update() 请求重绘而不是直接调用 paintEvent。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QPainter` 所属机制类型：二维绘制状态机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
