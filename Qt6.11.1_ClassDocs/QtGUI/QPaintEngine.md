# QPaintEngine

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QPaintEngine` 是 Qt GUI 绘制体系中的类型，负责画笔、画刷、字体、图像、绘制设备或绘制状态。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QPaintEngine` 是 二维绘制状态机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 绘制对象维护一组状态：画笔、画刷、字体、变换、裁剪、合成模式和渲染提示。每次 draw 调用都会使用当前状态；坐标通常经过当前 transform 映射到目标设备。

**适用场景：** 开始绘制后配置必要状态，使用 save/restore 包围局部变换，按设备坐标绘制，结束时让上下文析构或调用 end。绘制文本和图片时同时考虑字体度量、devicePixelRatio、裁剪和性能。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要直接调用 paintEvent；不要在绘制函数里修改会再次触发绘制的状态；不要假定所有图像都是四字节像素；不要忘记 transform 会影响坐标和 boundingRect。

## 2. 依赖与对象关系

- 头文件：`#include <QPaintEngine>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

绘制对象维护一组状态：画笔、画刷、字体、变换、裁剪、合成模式和渲染提示。每次 draw 调用都会使用当前状态；坐标通常经过当前 transform 映射到目标设备。

### 状态、生命周期和线程

**生命周期：** 绘制上下文必须绑定有效的 paint device，并在合法的绘制阶段使用。QWidget 上通常只在 `paintEvent()` 内创建 painter；离屏图像、打印设备和 pixmap 则有各自的设备生命周期。

**状态与结果：** `save()`/`restore()` 用于隔离局部状态；改变坐标系、画笔或合成模式后要么恢复，要么明确后续绘制也需要该状态。重绘请求和真正绘制是两个阶段，业务状态变化应调用 `update()`。

**线程与事件循环：** 同一个 GUI 控件的绘制在 GUI 线程完成；离屏 QImage 可以按数据所有权在后台处理，但不要让后台线程直接绘制或访问正在显示的 QWidget/QPixmap 资源。

## 3. 直接使用

开始绘制后配置必要状态，使用 save/restore 包围局部变换，按设备坐标绘制，结束时让上下文析构或调用 end。绘制文本和图片时同时考虑字体度量、devicePixelRatio、裁剪和性能。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

```cpp
void Widget::paintEvent(QPaintEvent *)
{
    QPainter painter(this);
    painter.save();
    // 设置画笔、画刷、字体或变换后进行绘制
    painter.restore();
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum DirtyFlag { DirtyPen, DirtyBrush, DirtyBrushOrigin, DirtyFont, DirtyBackground, …, AllDirty }`
- `flags DirtyFlags`
- `enum PaintEngineFeature { AlphaBlend, Antialiasing, BlendModes, BrushStroke, ConicalGradientFill, …, AllFeatures }`
- `flags PaintEngineFeatures`
- `enum PolygonDrawMode { OddEvenMode, WindingMode, ConvexMode, PolylineMode }`
- `enum Type { X11, Windows, MacPrinter, CoreGraphics, QuickDraw, …, Direct2D }`

### 公有函数

- `QPaintEngine(QPaintEngine::PaintEngineFeatures caps = PaintEngineFeatures())`
- `virtual ~QPaintEngine()`
- `virtual bool begin(QPaintDevice *pdev) = 0`
- `virtual void drawEllipse(const QRectF &rect)`
- `virtual void drawEllipse(const QRect &rect)`
- `virtual void drawImage(const QRectF &rectangle, const QImage &image, const QRectF &sr, Qt::ImageConversionFlags flags = Qt::AutoColor)`
- `virtual void drawLines(const QLineF *lines, int lineCount)`
- `virtual void drawLines(const QLine *lines, int lineCount)`
- `virtual void drawPath(const QPainterPath &path)`
- `virtual void drawPixmap(const QRectF &r, const QPixmap &pm, const QRectF &sr) = 0`
- `virtual void drawPoints(const QPoint *points, int pointCount)`
- `virtual void drawPoints(const QPointF *points, int pointCount)`
- `virtual void drawPolygon(const QPointF *points, int pointCount, QPaintEngine::PolygonDrawMode mode)`
- `virtual void drawPolygon(const QPoint *points, int pointCount, QPaintEngine::PolygonDrawMode mode)`
- `virtual void drawRects(const QRectF *rects, int rectCount)`
- `virtual void drawRects(const QRect *rects, int rectCount)`
- `virtual void drawTextItem(const QPointF &p, const QTextItem &textItem)`
- `virtual void drawTiledPixmap(const QRectF &rect, const QPixmap &pixmap, const QPointF &p)`
- `virtual bool end() = 0`
- `bool hasFeature(QPaintEngine::PaintEngineFeatures feature) const`
- `bool isActive() const`
- `QPaintDevice * paintDevice() const`
- `QPainter * painter() const`
- `void setActive(bool state)`
- `virtual QPaintEngine::Type type() const = 0`
- `virtual void updateState(const QPaintEngineState &state) = 0`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 34 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QPaintEngine::DirtyFlagflags QPaintEngine::DirtyFlags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QPaintEngine` 暴露的类型声明 `Dirty、Flagflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:DirtyFlagflags QPaintEngine::DirtyFlags`。
- 属性名：`QPaintEngine`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QPaintEngine::PaintEngineFeatureflags QPaintEngine::PaintEngineFeatures`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QPaintEngine` 暴露的类型声明 `绘制、Engine、Featureflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:PaintEngineFeatureflags QPaintEngine::PaintEngineFeatures`。
- 属性名：`QPaintEngine`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QPaintEngine::QPaintEngine(QPaintEngine::PaintEngineFeatures caps = PaintEngineFeatures())`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPaintEngine` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `caps`：类型为 `QPaintEngine::PaintEngineFeatures`。默认值为 `PaintEngineFeatures()`。传入 `QPaintEngine::PaintEngineFeatures` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QPaintEngine::~QPaintEngine()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPaintEngine` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] bool QPaintEngine::begin(QPaintDevice *pdev)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `begin`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`bool`。
- 参数 `pdev`：类型为 `QPaintDevice *`。没有默认值，调用时必须提供。传入 `QPaintDevice *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 开始后要在合法设备上绘制，结束时调用 `end()` 或让 painter 析构；绘制状态可用 `save()`/`restore()` 隔离。

### `[virtual] void QPaintEngine::drawEllipse(const QRectF &rect)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPaintEngine` 的核心操作 `drawEllipse`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `rect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `[virtual] void QPaintEngine::drawEllipse(const QRect &rect)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPaintEngine` 的核心操作 `drawEllipse`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `rect`：类型为 `const QRect &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `[virtual] void QPaintEngine::drawImage(const QRectF &rectangle, const QImage &image, const QRectF &sr, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPaintEngine` 的核心操作 `drawImage`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `rectangle`：类型为 `const QRectF &`。没有默认值，调用时必须提供。传入 `const QRectF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `image`：类型为 `const QImage &`。没有默认值，调用时必须提供。传入 `const QImage &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sr`：类型为 `const QRectF &`。没有默认值，调用时必须提供。传入 `const QRectF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `Qt::ImageConversionFlags`。默认值为 `Qt::AutoColor`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `[virtual] void QPaintEngine::drawLines(const QLineF *lines, int lineCount)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPaintEngine` 的核心操作 `drawLines`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `lines`：类型为 `const QLineF *`。没有默认值，调用时必须提供。传入 `const QLineF *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `lineCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `[virtual] void QPaintEngine::drawLines(const QLine *lines, int lineCount)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPaintEngine` 的核心操作 `drawLines`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `lines`：类型为 `const QLine *`。没有默认值，调用时必须提供。传入 `const QLine *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `lineCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `[virtual] void QPaintEngine::drawPath(const QPainterPath &path)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPaintEngine` 的核心操作 `drawPath`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `path`：类型为 `const QPainterPath &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `[pure virtual] void QPaintEngine::drawPixmap(const QRectF &r, const QPixmap &pm, const QRectF &sr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPaintEngine` 的核心操作 `drawPixmap`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `r`：类型为 `const QRectF &`。没有默认值，调用时必须提供。传入 `const QRectF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pm`：类型为 `const QPixmap &`。没有默认值，调用时必须提供。传入 `const QPixmap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sr`：类型为 `const QRectF &`。没有默认值，调用时必须提供。传入 `const QRectF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `[virtual] void QPaintEngine::drawPoints(const QPoint *points, int pointCount)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPaintEngine` 的核心操作 `drawPoints`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `points`：类型为 `const QPoint *`。没有默认值，调用时必须提供。传入 `const QPoint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pointCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `[virtual] void QPaintEngine::drawPoints(const QPointF *points, int pointCount)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPaintEngine` 的核心操作 `drawPoints`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `points`：类型为 `const QPointF *`。没有默认值，调用时必须提供。传入 `const QPointF *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pointCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `[virtual] void QPaintEngine::drawPolygon(const QPointF *points, int pointCount, QPaintEngine::PolygonDrawMode mode)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPaintEngine` 的核心操作 `drawPolygon`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `points`：类型为 `const QPointF *`。没有默认值，调用时必须提供。传入 `const QPointF *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pointCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mode`：类型为 `QPaintEngine::PolygonDrawMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `[virtual] void QPaintEngine::drawPolygon(const QPoint *points, int pointCount, QPaintEngine::PolygonDrawMode mode)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPaintEngine` 的核心操作 `drawPolygon`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `points`：类型为 `const QPoint *`。没有默认值，调用时必须提供。传入 `const QPoint *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pointCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mode`：类型为 `QPaintEngine::PolygonDrawMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `[virtual] void QPaintEngine::drawRects(const QRectF *rects, int rectCount)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPaintEngine` 的核心操作 `drawRects`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `rects`：类型为 `const QRectF *`。没有默认值，调用时必须提供。传入 `const QRectF *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `rectCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `[virtual] void QPaintEngine::drawRects(const QRect *rects, int rectCount)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPaintEngine` 的核心操作 `drawRects`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `rects`：类型为 `const QRect *`。没有默认值，调用时必须提供。传入 `const QRect *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `rectCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `[virtual] void QPaintEngine::drawTextItem(const QPointF &p, const QTextItem &textItem)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPaintEngine` 的核心操作 `drawTextItem`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `p`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `textItem`：类型为 `const QTextItem &`。没有默认值，调用时必须提供。传入 `const QTextItem &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `[virtual] void QPaintEngine::drawTiledPixmap(const QRectF &rect, const QPixmap &pixmap, const QPointF &p)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPaintEngine` 的核心操作 `drawTiledPixmap`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `rect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。
- 参数 `pixmap`：类型为 `const QPixmap &`。没有默认值，调用时必须提供。传入 `const QPixmap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `p`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 绘制结果受当前 pen、brush、font、transform、clip 和 composition mode 共同影响。

### `[pure virtual] bool QPaintEngine::end()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `end`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPaintEngine::hasFeature(QPaintEngine::PaintEngineFeatures feature) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasFeature`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `feature`：类型为 `QPaintEngine::PaintEngineFeatures`。没有默认值，调用时必须提供。传入 `QPaintEngine::PaintEngineFeatures` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPaintEngine::isActive() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isActive`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPaintDevice *QPaintEngine::paintDevice() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPaintEngine` 的核心操作 `paintDevice`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QPaintDevice *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPainter *QPaintEngine::painter() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPaintEngine` 的核心操作 `painter`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QPainter *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPaintEngine::setActive(bool state)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setActive`。调用它会改变 `QPaintEngine` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `state`：类型为 `bool`。没有默认值，调用时必须提供。状态值或状态对象；它描述调用时的阶段，不能把某个状态下有效的 API 用到其他阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QPaintEngine::Type QPaintEngine::type() const`

**API 类别：** 成员函数说明

**中文解读：** `QPaintEngine::type` 用于计算、查询或取得与“类型”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPaintEngine::Type`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPaintEngine::Type`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QPaintEngine::updateState(const QPaintEngineState &state)`

**API 类别：** 成员函数说明

**中文解读：** `QPaintEngine::updateState` 用于执行与“更新、State”相关的操作。调用时要先确认当前状态和 `state` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `state`：类型为 `const QPaintEngineState &`。没有默认值，调用时必须提供。状态值或状态对象；它描述调用时的阶段，不能把某个状态下有效的 API 用到其他阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum DirtyFlag { DirtyPen, DirtyBrush, DirtyBrushOrigin, DirtyFont, DirtyBackground, …, AllDirty }`

**API 类别：** 公有类型

**中文解读：** 这是 `QPaintEngine` 暴露的类型声明 `Dirty、Flag`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags DirtyFlags`

**API 类别：** 公有类型

**中文解读：** 这是 `QPaintEngine` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum PaintEngineFeature { AlphaBlend, Antialiasing, BlendModes, BrushStroke, ConicalGradientFill, …, AllFeatures }`

**API 类别：** 公有类型

**中文解读：** 这是 `QPaintEngine` 暴露的类型声明 `绘制、Engine、Feature`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags PaintEngineFeatures`

**API 类别：** 公有类型

**中文解读：** 这是 `QPaintEngine` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum PolygonDrawMode { OddEvenMode, WindingMode, ConvexMode, PolylineMode }`

**API 类别：** 公有类型

**中文解读：** 这是 `QPaintEngine` 暴露的类型声明 `Polygon、绘制、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum Type { X11, Windows, MacPrinter, CoreGraphics, QuickDraw, …, Direct2D }`

**API 类别：** 公有类型

**中文解读：** 这是 `QPaintEngine` 暴露的类型声明 `类型`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

绘制上下文必须绑定有效的 paint device，并在合法的绘制阶段使用。QWidget 上通常只在 `paintEvent()` 内创建 painter；离屏图像、打印设备和 pixmap 则有各自的设备生命周期。

### 状态和错误边界

`save()`/`restore()` 用于隔离局部状态；改变坐标系、画笔或合成模式后要么恢复，要么明确后续绘制也需要该状态。重绘请求和真正绘制是两个阶段，业务状态变化应调用 `update()`。

### 线程边界

同一个 GUI 控件的绘制在 GUI 线程完成；离屏 QImage 可以按数据所有权在后台处理，但不要让后台线程直接绘制或访问正在显示的 QWidget/QPixmap 资源。

### 最容易出现的错误

不要直接调用 paintEvent；不要在绘制函数里修改会再次触发绘制的状态；不要假定所有图像都是四字节像素；不要忘记 transform 会影响坐标和 boundingRect。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QPaintEngine` 所属机制类型：二维绘制状态机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
