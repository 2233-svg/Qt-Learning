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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 206 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QPainter::CompositionMode`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QPainter` 暴露的类型声明 `Composition、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:CompositionMode`。
- 属性名：`QPainter`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QPainter::PixmapFragmentHintflags QPainter::PixmapFragmentHints`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QPainter` 暴露的类型声明 `Pixmap、Fragment、Hintflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:PixmapFragmentHintflags QPainter::PixmapFragmentHints`。
- 属性名：`QPainter`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QPainter::RenderHintflags QPainter::RenderHints`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QPainter` 暴露的类型声明 `渲染、Hintflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:RenderHintflags QPainter::RenderHints`。
- 属性名：`QPainter`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPainter::QPainter()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QPainter::QPainter(QPaintDevice *device)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `device`：类型为 `QPaintDevice *`。没有默认值，调用时必须提供。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QPainter::~QPainter()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QBrush &QPainter::background() const`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::background` 用于计算、查询或取得与“background”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QBrush &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QBrush &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::BGMode QPainter::backgroundMode() const`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::backgroundMode` 用于计算、查询或取得与“background、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::BGMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::BGMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPainter::begin(QPaintDevice *device)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `begin`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`bool`。
- 参数 `device`：类型为 `QPaintDevice *`。没有默认值，调用时必须提供。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。

**正确调用组合：** 开始后要在合法设备上绘制，结束时调用 `end()` 或让 painter 析构；绘制状态可用 `save()`/`restore()` 隔离。

### `void QPainter::beginNativePainting()`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `beginNativePainting`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 开始后要在合法设备上绘制，结束时调用 `end()` 或让 painter 析构；绘制状态可用 `save()`/`restore()` 隔离。

### `QRectF QPainter::boundingRect(const QRectF &rectangle, int flags, const QString &text)`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::boundingRect` 用于计算、查询或取得与“bounding、Rect”相关的操作。调用时要先确认当前状态和 `rectangle`、`flags`、`text` 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数 `rectangle`：类型为 `const QRectF &`。没有默认值，调用时必须提供。传入 `const QRectF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `int`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRect QPainter::boundingRect(const QRect &rectangle, int flags, const QString &text)`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::boundingRect` 用于计算、查询或取得与“bounding、Rect”相关的操作。调用时要先确认当前状态和 `rectangle`、`flags`、`text` 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数 `rectangle`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `int`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRectF QPainter::boundingRect(const QRectF &rectangle, const QString &text, const QTextOption &option = QTextOption())`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::boundingRect` 用于计算、查询或取得与“bounding、Rect”相关的操作。调用时要先确认当前状态和 `rectangle`、`text`、`option` 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数 `rectangle`：类型为 `const QRectF &`。没有默认值，调用时必须提供。传入 `const QRectF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `option`：类型为 `const QTextOption &`。默认值为 `QTextOption()`。选项或绘制/行为配置对象；调用前确认其中的状态、矩形和样式信息已经初始化。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRect QPainter::boundingRect(int x, int y, int w, int h, int flags, const QString &text)`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::boundingRect` 用于计算、查询或取得与“bounding、Rect”相关的操作。调用时要先确认当前状态和 `x`、`y`、`w`、`h`、`flags`、`text` 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `w`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `h`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `int`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QBrush &QPainter::brush() const`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::brush` 用于计算、查询或取得与“brush”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QBrush &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QBrush &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPoint QPainter::brushOrigin() const`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::brushOrigin` 用于计算、查询或取得与“brush、Origin”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPoint`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPoint`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.11] QPointF QPainter::brushOriginF() const`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::brushOriginF` 用于计算、查询或取得与“brush、Origin、F”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPointF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPointF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRectF QPainter::clipBoundingRect() const`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::clipBoundingRect` 用于计算、查询或取得与“clip、Bounding、Rect”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPainterPath QPainter::clipPath() const`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::clipPath` 用于计算、查询或取得与“clip、Path”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPainterPath`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPainterPath`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRegion QPainter::clipRegion() const`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::clipRegion` 用于计算、查询或取得与“clip、Region”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRegion`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRegion`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTransform QPainter::combinedTransform() const`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::combinedTransform` 用于计算、查询或取得与“combined、Transform”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTransform`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTransform`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPainter::CompositionMode QPainter::compositionMode() const`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::compositionMode` 用于计算、查询或取得与“composition、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPainter::CompositionMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPainter::CompositionMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPaintDevice *QPainter::device() const`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::device` 用于计算、查询或取得与“device”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPaintDevice *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPaintDevice *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QTransform &QPainter::deviceTransform() const`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::deviceTransform` 用于计算、查询或取得与“device、Transform”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QTransform &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QTransform &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::drawArc(const QRectF &rectangle, int startAngle, int spanAngle)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawArc`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRectF &`。没有默认值，调用时必须提供。传入 `const QRectF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `startAngle`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `spanAngle`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawArc(const QRect &rectangle, int startAngle, int spanAngle)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawArc`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `startAngle`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `spanAngle`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawArc(int x, int y, int width, int height, int startAngle, int spanAngle)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawArc`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `startAngle`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `spanAngle`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawChord(const QRectF &rectangle, int startAngle, int spanAngle)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawChord`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRectF &`。没有默认值，调用时必须提供。传入 `const QRectF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `startAngle`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `spanAngle`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawChord(const QRect &rectangle, int startAngle, int spanAngle)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawChord`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `startAngle`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `spanAngle`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawChord(int x, int y, int width, int height, int startAngle, int spanAngle)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawChord`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `startAngle`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `spanAngle`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawConvexPolygon(const QPointF *points, int pointCount)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawConvexPolygon`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `points`：类型为 `const QPointF *`。没有默认值，调用时必须提供。传入 `const QPointF *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pointCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawConvexPolygon(const QPolygon &polygon)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawConvexPolygon`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `polygon`：类型为 `const QPolygon &`。没有默认值，调用时必须提供。传入 `const QPolygon &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawConvexPolygon(const QPolygonF &polygon)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawConvexPolygon`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `polygon`：类型为 `const QPolygonF &`。没有默认值，调用时必须提供。传入 `const QPolygonF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawConvexPolygon(const QPoint *points, int pointCount)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawConvexPolygon`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `points`：类型为 `const QPoint *`。没有默认值，调用时必须提供。传入 `const QPoint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pointCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawEllipse(const QRectF &rectangle)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawEllipse`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRectF &`。没有默认值，调用时必须提供。传入 `const QRectF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawEllipse(const QRect &rectangle)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawEllipse`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawEllipse(const QPoint &center, int rx, int ry)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawEllipse`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `center`：类型为 `const QPoint &`。没有默认值，调用时必须提供。传入 `const QPoint &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `rx`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `ry`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawEllipse(const QPointF &center, qreal rx, qreal ry)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawEllipse`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `center`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `rx`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `ry`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawEllipse(int x, int y, int width, int height)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawEllipse`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawGlyphRun(const QPointF &position, const QGlyphRun &glyphs)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawGlyphRun`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `position`：类型为 `const QPointF &`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `glyphs`：类型为 `const QGlyphRun &`。没有默认值，调用时必须提供。传入 `const QGlyphRun &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawImage(const QRectF &target, const QImage &image, const QRectF &source, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawImage`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `const QRectF &`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `image`：类型为 `const QImage &`。没有默认值，调用时必须提供。传入 `const QImage &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `source`：类型为 `const QRectF &`。没有默认值，调用时必须提供。源对象、源索引或源数据；它通常决定操作的输入，转换后要确认源的生命周期和线程归属。
- 参数 `flags`：类型为 `Qt::ImageConversionFlags`。默认值为 `Qt::AutoColor`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawImage(const QPoint &point, const QImage &image)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawImage`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `point`：类型为 `const QPoint &`。没有默认值，调用时必须提供。传入 `const QPoint &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `image`：类型为 `const QImage &`。没有默认值，调用时必须提供。传入 `const QImage &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawImage(const QPointF &point, const QImage &image)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawImage`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `point`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `image`：类型为 `const QImage &`。没有默认值，调用时必须提供。传入 `const QImage &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawImage(const QRect &rectangle, const QImage &image)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawImage`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `image`：类型为 `const QImage &`。没有默认值，调用时必须提供。传入 `const QImage &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawImage(const QRectF &rectangle, const QImage &image)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawImage`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRectF &`。没有默认值，调用时必须提供。传入 `const QRectF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `image`：类型为 `const QImage &`。没有默认值，调用时必须提供。传入 `const QImage &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawImage(const QPoint &point, const QImage &image, const QRect &source, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawImage`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `point`：类型为 `const QPoint &`。没有默认值，调用时必须提供。传入 `const QPoint &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `image`：类型为 `const QImage &`。没有默认值，调用时必须提供。传入 `const QImage &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `source`：类型为 `const QRect &`。没有默认值，调用时必须提供。源对象、源索引或源数据；它通常决定操作的输入，转换后要确认源的生命周期和线程归属。
- 参数 `flags`：类型为 `Qt::ImageConversionFlags`。默认值为 `Qt::AutoColor`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawImage(const QPointF &point, const QImage &image, const QRectF &source, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawImage`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `point`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `image`：类型为 `const QImage &`。没有默认值，调用时必须提供。传入 `const QImage &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `source`：类型为 `const QRectF &`。没有默认值，调用时必须提供。源对象、源索引或源数据；它通常决定操作的输入，转换后要确认源的生命周期和线程归属。
- 参数 `flags`：类型为 `Qt::ImageConversionFlags`。默认值为 `Qt::AutoColor`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawImage(const QRect &target, const QImage &image, const QRect &source, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawImage`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `const QRect &`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `image`：类型为 `const QImage &`。没有默认值，调用时必须提供。传入 `const QImage &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `source`：类型为 `const QRect &`。没有默认值，调用时必须提供。源对象、源索引或源数据；它通常决定操作的输入，转换后要确认源的生命周期和线程归属。
- 参数 `flags`：类型为 `Qt::ImageConversionFlags`。默认值为 `Qt::AutoColor`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawImage(int x, int y, const QImage &image, int sx = 0, int sy = 0, int sw = -1, int sh = -1, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawImage`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `image`：类型为 `const QImage &`。没有默认值，调用时必须提供。传入 `const QImage &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sx`：类型为 `int`。默认值为 `0`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sy`：类型为 `int`。默认值为 `0`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sw`：类型为 `int`。默认值为 `-1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sh`：类型为 `int`。默认值为 `-1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `Qt::ImageConversionFlags`。默认值为 `Qt::AutoColor`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawLine(const QLineF &line)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawLine`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `line`：类型为 `const QLineF &`。没有默认值，调用时必须提供。传入 `const QLineF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawLine(const QLine &line)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawLine`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `line`：类型为 `const QLine &`。没有默认值，调用时必须提供。传入 `const QLine &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawLine(const QPoint &p1, const QPoint &p2)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawLine`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `p1`：类型为 `const QPoint &`。没有默认值，调用时必须提供。传入 `const QPoint &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `p2`：类型为 `const QPoint &`。没有默认值，调用时必须提供。传入 `const QPoint &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawLine(const QPointF &p1, const QPointF &p2)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawLine`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `p1`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `p2`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawLine(int x1, int y1, int x2, int y2)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawLine`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `x1`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y1`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `x2`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y2`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawLines(const QLineF *lines, int lineCount)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawLines`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `lines`：类型为 `const QLineF *`。没有默认值，调用时必须提供。传入 `const QLineF *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `lineCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawLines(const QList<QLine> &lines)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawLines`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `lines`：类型为 `const QList<QLine> &`。没有默认值，调用时必须提供。传入 `const QList<QLine> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawLines(const QList<QLineF> &lines)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawLines`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `lines`：类型为 `const QList<QLineF> &`。没有默认值，调用时必须提供。传入 `const QList<QLineF> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawLines(const QList<QPoint> &pointPairs)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawLines`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `pointPairs`：类型为 `const QList<QPoint> &`。没有默认值，调用时必须提供。传入 `const QList<QPoint> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawLines(const QList<QPointF> &pointPairs)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawLines`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `pointPairs`：类型为 `const QList<QPointF> &`。没有默认值，调用时必须提供。传入 `const QList<QPointF> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawLines(const QLine *lines, int lineCount)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawLines`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `lines`：类型为 `const QLine *`。没有默认值，调用时必须提供。传入 `const QLine *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `lineCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawLines(const QPoint *pointPairs, int lineCount)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawLines`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `pointPairs`：类型为 `const QPoint *`。没有默认值，调用时必须提供。传入 `const QPoint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `lineCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawLines(const QPointF *pointPairs, int lineCount)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawLines`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `pointPairs`：类型为 `const QPointF *`。没有默认值，调用时必须提供。传入 `const QPointF *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `lineCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPath(const QPainterPath &path)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPath`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `path`：类型为 `const QPainterPath &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPicture(const QPointF &point, const QPicture &picture)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPicture`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `point`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `picture`：类型为 `const QPicture &`。没有默认值，调用时必须提供。传入 `const QPicture &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPicture(const QPoint &point, const QPicture &picture)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPicture`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `point`：类型为 `const QPoint &`。没有默认值，调用时必须提供。传入 `const QPoint &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `picture`：类型为 `const QPicture &`。没有默认值，调用时必须提供。传入 `const QPicture &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPicture(int x, int y, const QPicture &picture)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPicture`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `picture`：类型为 `const QPicture &`。没有默认值，调用时必须提供。传入 `const QPicture &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPie(const QRectF &rectangle, int startAngle, int spanAngle)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPie`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRectF &`。没有默认值，调用时必须提供。传入 `const QRectF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `startAngle`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `spanAngle`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPie(const QRect &rectangle, int startAngle, int spanAngle)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPie`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `startAngle`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `spanAngle`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPie(int x, int y, int width, int height, int startAngle, int spanAngle)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPie`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `startAngle`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `spanAngle`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPixmap(const QRectF &target, const QPixmap &pixmap, const QRectF &source)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPixmap`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `const QRectF &`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `pixmap`：类型为 `const QPixmap &`。没有默认值，调用时必须提供。传入 `const QPixmap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `source`：类型为 `const QRectF &`。没有默认值，调用时必须提供。源对象、源索引或源数据；它通常决定操作的输入，转换后要确认源的生命周期和线程归属。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPixmap(const QPoint &point, const QPixmap &pixmap)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPixmap`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `point`：类型为 `const QPoint &`。没有默认值，调用时必须提供。传入 `const QPoint &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pixmap`：类型为 `const QPixmap &`。没有默认值，调用时必须提供。传入 `const QPixmap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPixmap(const QPointF &point, const QPixmap &pixmap)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPixmap`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `point`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pixmap`：类型为 `const QPixmap &`。没有默认值，调用时必须提供。传入 `const QPixmap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPixmap(const QRect &rectangle, const QPixmap &pixmap)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPixmap`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pixmap`：类型为 `const QPixmap &`。没有默认值，调用时必须提供。传入 `const QPixmap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPixmap(const QPoint &point, const QPixmap &pixmap, const QRect &source)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPixmap`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `point`：类型为 `const QPoint &`。没有默认值，调用时必须提供。传入 `const QPoint &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pixmap`：类型为 `const QPixmap &`。没有默认值，调用时必须提供。传入 `const QPixmap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `source`：类型为 `const QRect &`。没有默认值，调用时必须提供。源对象、源索引或源数据；它通常决定操作的输入，转换后要确认源的生命周期和线程归属。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPixmap(const QPointF &point, const QPixmap &pixmap, const QRectF &source)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPixmap`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `point`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pixmap`：类型为 `const QPixmap &`。没有默认值，调用时必须提供。传入 `const QPixmap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `source`：类型为 `const QRectF &`。没有默认值，调用时必须提供。源对象、源索引或源数据；它通常决定操作的输入，转换后要确认源的生命周期和线程归属。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPixmap(const QRect &target, const QPixmap &pixmap, const QRect &source)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPixmap`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `const QRect &`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `pixmap`：类型为 `const QPixmap &`。没有默认值，调用时必须提供。传入 `const QPixmap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `source`：类型为 `const QRect &`。没有默认值，调用时必须提供。源对象、源索引或源数据；它通常决定操作的输入，转换后要确认源的生命周期和线程归属。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPixmap(int x, int y, const QPixmap &pixmap)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPixmap`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pixmap`：类型为 `const QPixmap &`。没有默认值，调用时必须提供。传入 `const QPixmap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPixmap(int x, int y, int width, int height, const QPixmap &pixmap)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPixmap`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `pixmap`：类型为 `const QPixmap &`。没有默认值，调用时必须提供。传入 `const QPixmap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPixmap(int x, int y, const QPixmap &pixmap, int sx, int sy, int sw, int sh)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPixmap`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pixmap`：类型为 `const QPixmap &`。没有默认值，调用时必须提供。传入 `const QPixmap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sx`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sy`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sw`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sh`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPixmap(int x, int y, int w, int h, const QPixmap &pixmap, int sx, int sy, int sw, int sh)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPixmap`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `w`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `h`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pixmap`：类型为 `const QPixmap &`。没有默认值，调用时必须提供。传入 `const QPixmap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sx`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sy`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sw`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sh`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPixmapFragments(const QPainter::PixmapFragment *fragments, int fragmentCount, const QPixmap &pixmap, QPainter::PixmapFragmentHints hints = PixmapFragmentHints())`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPixmapFragments`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `fragments`：类型为 `const QPainter::PixmapFragment *`。没有默认值，调用时必须提供。传入 `const QPainter::PixmapFragment *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `fragmentCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pixmap`：类型为 `const QPixmap &`。没有默认值，调用时必须提供。传入 `const QPixmap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `hints`：类型为 `QPainter::PixmapFragmentHints`。默认值为 `PixmapFragmentHints()`。传入 `QPainter::PixmapFragmentHints` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPoint(const QPointF &position)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPoint`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `position`：类型为 `const QPointF &`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPoint(const QPoint &position)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPoint`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `position`：类型为 `const QPoint &`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPoint(int x, int y)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPoint`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPoints(const QPointF *points, int pointCount)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPoints`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `points`：类型为 `const QPointF *`。没有默认值，调用时必须提供。传入 `const QPointF *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pointCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPoints(const QPolygon &points)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPoints`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `points`：类型为 `const QPolygon &`。没有默认值，调用时必须提供。传入 `const QPolygon &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPoints(const QPolygonF &points)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPoints`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `points`：类型为 `const QPolygonF &`。没有默认值，调用时必须提供。传入 `const QPolygonF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPoints(const QPoint *points, int pointCount)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPoints`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `points`：类型为 `const QPoint *`。没有默认值，调用时必须提供。传入 `const QPoint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pointCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPolygon(const QPointF *points, int pointCount, Qt::FillRule fillRule = Qt::OddEvenFill)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPolygon`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `points`：类型为 `const QPointF *`。没有默认值，调用时必须提供。传入 `const QPointF *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pointCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `fillRule`：类型为 `Qt::FillRule`。默认值为 `Qt::OddEvenFill`。传入 `Qt::FillRule` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPolygon(const QPolygon &points, Qt::FillRule fillRule = Qt::OddEvenFill)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPolygon`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `points`：类型为 `const QPolygon &`。没有默认值，调用时必须提供。传入 `const QPolygon &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `fillRule`：类型为 `Qt::FillRule`。默认值为 `Qt::OddEvenFill`。传入 `Qt::FillRule` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPolygon(const QPolygonF &points, Qt::FillRule fillRule = Qt::OddEvenFill)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPolygon`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `points`：类型为 `const QPolygonF &`。没有默认值，调用时必须提供。传入 `const QPolygonF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `fillRule`：类型为 `Qt::FillRule`。默认值为 `Qt::OddEvenFill`。传入 `Qt::FillRule` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPolygon(const QPoint *points, int pointCount, Qt::FillRule fillRule = Qt::OddEvenFill)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPolygon`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `points`：类型为 `const QPoint *`。没有默认值，调用时必须提供。传入 `const QPoint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pointCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `fillRule`：类型为 `Qt::FillRule`。默认值为 `Qt::OddEvenFill`。传入 `Qt::FillRule` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPolyline(const QPointF *points, int pointCount)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPolyline`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `points`：类型为 `const QPointF *`。没有默认值，调用时必须提供。传入 `const QPointF *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pointCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPolyline(const QPolygon &points)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPolyline`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `points`：类型为 `const QPolygon &`。没有默认值，调用时必须提供。传入 `const QPolygon &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPolyline(const QPolygonF &points)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPolyline`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `points`：类型为 `const QPolygonF &`。没有默认值，调用时必须提供。传入 `const QPolygonF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawPolyline(const QPoint *points, int pointCount)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawPolyline`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `points`：类型为 `const QPoint *`。没有默认值，调用时必须提供。传入 `const QPoint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pointCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawRect(const QRectF &rectangle)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawRect`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRectF &`。没有默认值，调用时必须提供。传入 `const QRectF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawRect(const QRect &rectangle)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawRect`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawRect(int x, int y, int width, int height)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawRect`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawRects(const QRectF *rectangles, int rectCount)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawRects`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangles`：类型为 `const QRectF *`。没有默认值，调用时必须提供。传入 `const QRectF *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `rectCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawRects(const QList<QRect> &rectangles)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawRects`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangles`：类型为 `const QList<QRect> &`。没有默认值，调用时必须提供。传入 `const QList<QRect> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawRects(const QList<QRectF> &rectangles)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawRects`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangles`：类型为 `const QList<QRectF> &`。没有默认值，调用时必须提供。传入 `const QList<QRectF> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawRects(const QRect *rectangles, int rectCount)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawRects`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangles`：类型为 `const QRect *`。没有默认值，调用时必须提供。传入 `const QRect *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `rectCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawRoundedRect(const QRectF &rect, qreal xRadius, qreal yRadius, Qt::SizeMode mode = Qt::AbsoluteSize)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawRoundedRect`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `rect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。
- 参数 `xRadius`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `yRadius`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mode`：类型为 `Qt::SizeMode`。默认值为 `Qt::AbsoluteSize`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawRoundedRect(const QRect &rect, qreal xRadius, qreal yRadius, Qt::SizeMode mode = Qt::AbsoluteSize)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawRoundedRect`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `rect`：类型为 `const QRect &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。
- 参数 `xRadius`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `yRadius`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mode`：类型为 `Qt::SizeMode`。默认值为 `Qt::AbsoluteSize`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawRoundedRect(int x, int y, int w, int h, qreal xRadius, qreal yRadius, Qt::SizeMode mode = Qt::AbsoluteSize)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawRoundedRect`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `w`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `h`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `xRadius`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `yRadius`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mode`：类型为 `Qt::SizeMode`。默认值为 `Qt::AbsoluteSize`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawStaticText(const QPointF &topLeftPosition, const QStaticText &staticText)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `drawStaticText`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `topLeftPosition`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `staticText`：类型为 `const QStaticText &`。没有默认值，调用时必须提供。传入 `const QStaticText &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawStaticText(const QPoint &topLeftPosition, const QStaticText &staticText)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `drawStaticText`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `topLeftPosition`：类型为 `const QPoint &`。没有默认值，调用时必须提供。传入 `const QPoint &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `staticText`：类型为 `const QStaticText &`。没有默认值，调用时必须提供。传入 `const QStaticText &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawStaticText(int left, int top, const QStaticText &staticText)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `drawStaticText`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `left`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `top`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `staticText`：类型为 `const QStaticText &`。没有默认值，调用时必须提供。传入 `const QStaticText &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawText(const QPointF &position, const QString &text)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawText`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `position`：类型为 `const QPointF &`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawText(const QPoint &position, const QString &text)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawText`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `position`：类型为 `const QPoint &`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawText(const QRectF &rectangle, const QString &text, const QTextOption &option = QTextOption())`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawText`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRectF &`。没有默认值，调用时必须提供。传入 `const QRectF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `option`：类型为 `const QTextOption &`。默认值为 `QTextOption()`。选项或绘制/行为配置对象；调用前确认其中的状态、矩形和样式信息已经初始化。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawText(int x, int y, const QString &text)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawText`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawText(const QRect &rectangle, int flags, const QString &text, QRect *boundingRect = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawText`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `int`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `boundingRect`：类型为 `QRect *`。默认值为 `nullptr`。传入 `QRect *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawText(const QRectF &rectangle, int flags, const QString &text, QRectF *boundingRect = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawText`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRectF &`。没有默认值，调用时必须提供。传入 `const QRectF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `int`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `boundingRect`：类型为 `QRectF *`。默认值为 `nullptr`。传入 `QRectF *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawText(int x, int y, int width, int height, int flags, const QString &text, QRect *boundingRect = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawText`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `flags`：类型为 `int`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `boundingRect`：类型为 `QRect *`。默认值为 `nullptr`。传入 `QRect *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawTiledPixmap(const QRectF &rectangle, const QPixmap &pixmap, const QPointF &position = QPointF())`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawTiledPixmap`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRectF &`。没有默认值，调用时必须提供。传入 `const QRectF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pixmap`：类型为 `const QPixmap &`。没有默认值，调用时必须提供。传入 `const QPixmap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `position`：类型为 `const QPointF &`。默认值为 `QPointF()`。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawTiledPixmap(const QRect &rectangle, const QPixmap &pixmap, const QPoint &position = QPoint())`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawTiledPixmap`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pixmap`：类型为 `const QPixmap &`。没有默认值，调用时必须提供。传入 `const QPixmap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `position`：类型为 `const QPoint &`。默认值为 `QPoint()`。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `void QPainter::drawTiledPixmap(int x, int y, int width, int height, const QPixmap &pixmap, int sx = 0, int sy = 0)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `drawTiledPixmap`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `pixmap`：类型为 `const QPixmap &`。没有默认值，调用时必须提供。传入 `const QPixmap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sx`：类型为 `int`。默认值为 `0`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sy`：类型为 `int`。默认值为 `0`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `bool QPainter::end()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `end`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::endNativePainting()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `endNativePainting`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::eraseRect(const QRectF &rectangle)`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::eraseRect` 用于执行与“erase、Rect”相关的操作。调用时要先确认当前状态和 `rectangle` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRectF &`。没有默认值，调用时必须提供。传入 `const QRectF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::eraseRect(const QRect &rectangle)`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::eraseRect` 用于执行与“erase、Rect”相关的操作。调用时要先确认当前状态和 `rectangle` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::eraseRect(int x, int y, int width, int height)`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::eraseRect` 用于执行与“erase、Rect”相关的操作。调用时要先确认当前状态和 `x`、`y`、`width`、`height` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::fillPath(const QPainterPath &path, const QBrush &brush)`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::fillPath` 用于执行与“fill、Path”相关的操作。调用时要先确认当前状态和 `path`、`brush` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `path`：类型为 `const QPainterPath &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。
- 参数 `brush`：类型为 `const QBrush &`。没有默认值，调用时必须提供。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::fillRect(const QRectF &rectangle, const QBrush &brush)`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::fillRect` 用于执行与“fill、Rect”相关的操作。调用时要先确认当前状态和 `rectangle`、`brush` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRectF &`。没有默认值，调用时必须提供。传入 `const QRectF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `brush`：类型为 `const QBrush &`。没有默认值，调用时必须提供。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::fillRect(const QRect &rectangle, QGradient::Preset preset)`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::fillRect` 用于执行与“fill、Rect”相关的操作。调用时要先确认当前状态和 `rectangle`、`preset` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `preset`：类型为 `QGradient::Preset`。没有默认值，调用时必须提供。传入 `QGradient::Preset` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::fillRect(const QRect &rectangle, Qt::BrushStyle style)`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::fillRect` 用于执行与“fill、Rect”相关的操作。调用时要先确认当前状态和 `rectangle`、`style` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `style`：类型为 `Qt::BrushStyle`。没有默认值，调用时必须提供。传入 `Qt::BrushStyle` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::fillRect(const QRect &rectangle, Qt::GlobalColor color)`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::fillRect` 用于执行与“fill、Rect”相关的操作。调用时要先确认当前状态和 `rectangle`、`color` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `color`：类型为 `Qt::GlobalColor`。没有默认值，调用时必须提供。传入 `Qt::GlobalColor` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::fillRect(const QRect &rectangle, const QBrush &brush)`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::fillRect` 用于执行与“fill、Rect”相关的操作。调用时要先确认当前状态和 `rectangle`、`brush` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `brush`：类型为 `const QBrush &`。没有默认值，调用时必须提供。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::fillRect(const QRect &rectangle, const QColor &color)`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::fillRect` 用于执行与“fill、Rect”相关的操作。调用时要先确认当前状态和 `rectangle`、`color` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `color`：类型为 `const QColor &`。没有默认值，调用时必须提供。传入 `const QColor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::fillRect(const QRectF &rectangle, QGradient::Preset preset)`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::fillRect` 用于执行与“fill、Rect”相关的操作。调用时要先确认当前状态和 `rectangle`、`preset` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRectF &`。没有默认值，调用时必须提供。传入 `const QRectF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `preset`：类型为 `QGradient::Preset`。没有默认值，调用时必须提供。传入 `QGradient::Preset` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::fillRect(const QRectF &rectangle, Qt::BrushStyle style)`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::fillRect` 用于执行与“fill、Rect”相关的操作。调用时要先确认当前状态和 `rectangle`、`style` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRectF &`。没有默认值，调用时必须提供。传入 `const QRectF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `style`：类型为 `Qt::BrushStyle`。没有默认值，调用时必须提供。传入 `Qt::BrushStyle` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::fillRect(const QRectF &rectangle, Qt::GlobalColor color)`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::fillRect` 用于执行与“fill、Rect”相关的操作。调用时要先确认当前状态和 `rectangle`、`color` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRectF &`。没有默认值，调用时必须提供。传入 `const QRectF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `color`：类型为 `Qt::GlobalColor`。没有默认值，调用时必须提供。传入 `Qt::GlobalColor` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::fillRect(const QRectF &rectangle, const QColor &color)`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::fillRect` 用于执行与“fill、Rect”相关的操作。调用时要先确认当前状态和 `rectangle`、`color` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRectF &`。没有默认值，调用时必须提供。传入 `const QRectF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `color`：类型为 `const QColor &`。没有默认值，调用时必须提供。传入 `const QColor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::fillRect(int x, int y, int width, int height, QGradient::Preset preset)`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::fillRect` 用于执行与“fill、Rect”相关的操作。调用时要先确认当前状态和 `x`、`y`、`width`、`height`、`preset` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `preset`：类型为 `QGradient::Preset`。没有默认值，调用时必须提供。传入 `QGradient::Preset` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::fillRect(int x, int y, int width, int height, Qt::BrushStyle style)`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::fillRect` 用于执行与“fill、Rect”相关的操作。调用时要先确认当前状态和 `x`、`y`、`width`、`height`、`style` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `style`：类型为 `Qt::BrushStyle`。没有默认值，调用时必须提供。传入 `Qt::BrushStyle` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::fillRect(int x, int y, int width, int height, Qt::GlobalColor color)`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::fillRect` 用于执行与“fill、Rect”相关的操作。调用时要先确认当前状态和 `x`、`y`、`width`、`height`、`color` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `color`：类型为 `Qt::GlobalColor`。没有默认值，调用时必须提供。传入 `Qt::GlobalColor` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::fillRect(int x, int y, int width, int height, const QBrush &brush)`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::fillRect` 用于执行与“fill、Rect”相关的操作。调用时要先确认当前状态和 `x`、`y`、`width`、`height`、`brush` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `brush`：类型为 `const QBrush &`。没有默认值，调用时必须提供。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::fillRect(int x, int y, int width, int height, const QColor &color)`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::fillRect` 用于执行与“fill、Rect”相关的操作。调用时要先确认当前状态和 `x`、`y`、`width`、`height`、`color` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `color`：类型为 `const QColor &`。没有默认值，调用时必须提供。传入 `const QColor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QFont &QPainter::font() const`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::font` 用于计算、查询或取得与“字体”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QFont &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QFont &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFontInfo QPainter::fontInfo() const`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::fontInfo` 用于计算、查询或取得与“字体、Info”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFontInfo`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFontInfo`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFontMetrics QPainter::fontMetrics() const`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::fontMetrics` 用于计算、查询或取得与“字体、Metrics”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFontMetrics`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFontMetrics`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPainter::hasClipping() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasClipping`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPainter::isActive() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isActive`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::LayoutDirection QPainter::layoutDirection() const`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::layoutDirection` 用于计算、查询或取得与“layout、Direction”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::LayoutDirection`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::LayoutDirection`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QPainter::opacity() const`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::opacity` 用于计算、查询或取得与“opacity”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPaintEngine *QPainter::paintEngine() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `paintEngine`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QPaintEngine *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QPen &QPainter::pen() const`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::pen` 用于计算、查询或取得与“pen”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QPen &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QPen &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPainter::RenderHints QPainter::renderHints() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPainter` 的核心操作 `renderHints`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QPainter::RenderHints`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::resetTransform()`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::resetTransform` 用于执行与“重置、Transform”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::restore()`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::restore` 用于执行与“恢复”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::rotate(qreal angle)`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::rotate` 用于执行与“rotate”相关的操作。调用时要先确认当前状态和 `angle` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `angle`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::save()`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::save` 用于执行与“保存”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::scale(qreal sx, qreal sy)`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::scale` 用于执行与“scale”相关的操作。调用时要先确认当前状态和 `sx`、`sy` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `sx`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sy`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::setBackground(const QBrush &brush)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBackground`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `brush`：类型为 `const QBrush &`。没有默认值，调用时必须提供。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::setBackgroundMode(Qt::BGMode mode)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBackgroundMode`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `Qt::BGMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::setBrush(const QBrush &brush)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBrush`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `brush`：类型为 `const QBrush &`。没有默认值，调用时必须提供。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.11] void QPainter::setBrush(QBrush &&brush)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBrush`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `brush`：类型为 `QBrush &&`。没有默认值，调用时必须提供。传入 `QBrush &&` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] void QPainter::setBrush(QColor color)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBrush`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `color`：类型为 `QColor`。没有默认值，调用时必须提供。传入 `QColor` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::setBrush(Qt::BrushStyle style)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBrush`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `style`：类型为 `Qt::BrushStyle`。没有默认值，调用时必须提供。传入 `Qt::BrushStyle` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] void QPainter::setBrush(Qt::GlobalColor color)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBrush`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `color`：类型为 `Qt::GlobalColor`。没有默认值，调用时必须提供。传入 `Qt::GlobalColor` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::setBrushOrigin(const QPointF &position)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBrushOrigin`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `position`：类型为 `const QPointF &`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::setBrushOrigin(const QPoint &position)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBrushOrigin`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `position`：类型为 `const QPoint &`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::setBrushOrigin(int x, int y)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBrushOrigin`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::setClipPath(const QPainterPath &path, Qt::ClipOperation operation = Qt::ReplaceClip)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setClipPath`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `path`：类型为 `const QPainterPath &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。
- 参数 `operation`：类型为 `Qt::ClipOperation`。默认值为 `Qt::ReplaceClip`。传入 `Qt::ClipOperation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::setClipRect(const QRectF &rectangle, Qt::ClipOperation operation = Qt::ReplaceClip)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setClipRect`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRectF &`。没有默认值，调用时必须提供。传入 `const QRectF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `operation`：类型为 `Qt::ClipOperation`。默认值为 `Qt::ReplaceClip`。传入 `Qt::ClipOperation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::setClipRect(int x, int y, int width, int height, Qt::ClipOperation operation = Qt::ReplaceClip)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setClipRect`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `operation`：类型为 `Qt::ClipOperation`。默认值为 `Qt::ReplaceClip`。传入 `Qt::ClipOperation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::setClipRect(const QRect &rectangle, Qt::ClipOperation operation = Qt::ReplaceClip)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setClipRect`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `operation`：类型为 `Qt::ClipOperation`。默认值为 `Qt::ReplaceClip`。传入 `Qt::ClipOperation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::setClipRegion(const QRegion &region, Qt::ClipOperation operation = Qt::ReplaceClip)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setClipRegion`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `region`：类型为 `const QRegion &`。没有默认值，调用时必须提供。传入 `const QRegion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `operation`：类型为 `Qt::ClipOperation`。默认值为 `Qt::ReplaceClip`。传入 `Qt::ClipOperation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::setClipping(bool enable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setClipping`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::setCompositionMode(QPainter::CompositionMode mode)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setCompositionMode`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `QPainter::CompositionMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::setFont(const QFont &font)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFont`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `font`：类型为 `const QFont &`。没有默认值，调用时必须提供。传入 `const QFont &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::setLayoutDirection(Qt::LayoutDirection direction)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setLayoutDirection`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `direction`：类型为 `Qt::LayoutDirection`。没有默认值，调用时必须提供。方向枚举，决定排列、遍历或坐标增长方向；要结合该类定义的枚举值判断实际方向。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::setOpacity(qreal opacity)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setOpacity`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `opacity`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::setPen(const QPen &pen)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPen`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `pen`：类型为 `const QPen &`。没有默认值，调用时必须提供。传入 `const QPen &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.11] void QPainter::setPen(QPen &&pen)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPen`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `pen`：类型为 `QPen &&`。没有默认值，调用时必须提供。传入 `QPen &&` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::setPen(Qt::PenStyle style)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPen`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `style`：类型为 `Qt::PenStyle`。没有默认值，调用时必须提供。传入 `Qt::PenStyle` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::setPen(const QColor &color)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPen`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `color`：类型为 `const QColor &`。没有默认值，调用时必须提供。传入 `const QColor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::setRenderHint(QPainter::RenderHint hint, bool on = true)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setRenderHint`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `hint`：类型为 `QPainter::RenderHint`。没有默认值，调用时必须提供。传入 `QPainter::RenderHint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `on`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::setRenderHints(QPainter::RenderHints hints, bool on = true)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setRenderHints`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `hints`：类型为 `QPainter::RenderHints`。没有默认值，调用时必须提供。传入 `QPainter::RenderHints` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `on`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::setTransform(const QTransform &transform, bool combine = false)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTransform`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `transform`：类型为 `const QTransform &`。没有默认值，调用时必须提供。传入 `const QTransform &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `combine`：类型为 `bool`。默认值为 `false`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::setViewTransformEnabled(bool enable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setViewTransformEnabled`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::setViewport(const QRect &rectangle)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setViewport`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::setViewport(int x, int y, int width, int height)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setViewport`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::setWindow(const QRect &rectangle)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setWindow`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::setWindow(int x, int y, int width, int height)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setWindow`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::setWorldMatrixEnabled(bool enable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setWorldMatrixEnabled`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::setWorldTransform(const QTransform &matrix, bool combine = false)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setWorldTransform`。调用它会改变 `QPainter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `matrix`：类型为 `const QTransform &`。没有默认值，调用时必须提供。传入 `const QTransform &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `combine`：类型为 `bool`。默认值为 `false`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::shear(qreal sh, qreal sv)`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::shear` 用于执行与“shear”相关的操作。调用时要先确认当前状态和 `sh`、`sv` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `sh`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sv`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::strokePath(const QPainterPath &path, const QPen &pen)`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::strokePath` 用于执行与“stroke、Path”相关的操作。调用时要先确认当前状态和 `path`、`pen` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `path`：类型为 `const QPainterPath &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。
- 参数 `pen`：类型为 `const QPen &`。没有默认值，调用时必须提供。传入 `const QPen &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPainter::testRenderHint(QPainter::RenderHint hint) const`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::testRenderHint` 用于计算、查询或取得与“test、渲染、Hint”相关的操作。调用时要先确认当前状态和 `hint` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `hint`：类型为 `QPainter::RenderHint`。没有默认值，调用时必须提供。传入 `QPainter::RenderHint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QTransform &QPainter::transform() const`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::transform` 用于计算、查询或取得与“transform”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QTransform &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QTransform &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::translate(const QPointF &offset)`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `translate`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`void`。
- 参数 `offset`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::translate(const QPoint &offset)`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `translate`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`void`。
- 参数 `offset`：类型为 `const QPoint &`。没有默认值，调用时必须提供。传入 `const QPoint &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPainter::translate(qreal dx, qreal dy)`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `translate`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`void`。
- 参数 `dx`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `dy`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPainter::viewTransformEnabled() const`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::viewTransformEnabled` 用于计算、查询或取得与“view、Transform、启用状态”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRect QPainter::viewport() const`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::viewport` 用于计算、查询或取得与“viewport”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRect QPainter::window() const`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::window` 用于计算、查询或取得与“window”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPainter::worldMatrixEnabled() const`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::worldMatrixEnabled` 用于计算、查询或取得与“world、Matrix、启用状态”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QTransform &QPainter::worldTransform() const`

**API 类别：** 成员函数说明

**中文解读：** `QPainter::worldTransform` 用于计算、查询或取得与“world、Transform”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QTransform &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QTransform &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `class PixmapFragment`

**API 类别：** 公有类型

**中文解读：** 这是 `QPainter` 暴露的类型声明 `Pixmap、Fragment`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum PixmapFragmentHint { OpaqueHint }`

**API 类别：** 公有类型

**中文解读：** 这是 `QPainter` 暴露的类型声明 `Pixmap、Fragment、Hint`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags PixmapFragmentHints`

**API 类别：** 公有类型

**中文解读：** 这是 `QPainter` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum RenderHint { Antialiasing, TextAntialiasing, SmoothPixmapTransform, VerticalSubpixelPositioning, LosslessImageRendering, NonCosmeticBrushPatterns }`

**API 类别：** 公有类型

**中文解读：** 这是 `QPainter` 暴露的类型声明 `渲染、Hint`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags RenderHints`

**API 类别：** 公有类型

**中文解读：** 这是 `QPainter` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
