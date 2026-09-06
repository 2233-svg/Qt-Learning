# QImage

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QImage` 是可直接访问像素数据的图像值类型，适合加载、转换、处理和离屏绘制。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QImage` 是可直接访问像素数据的图像值类型，适合加载、转换、处理和离屏绘制。

**内部模型：** QImage 偏向 CPU 端像素处理，QPixmap 偏向窗口系统显示。format 决定像素布局；bits/scanLine 访问原始内存时必须遵守 bytesPerLine 和格式。

**适用场景：** 图片读写、像素算法、离屏绘制、截图处理和跨线程图像数据使用。最终显示到 QWidget 时通常转换为 QPixmap。

**典型调用链：** load/fromData -> isNull/format/size -> convertToFormat/scanLine -> QPainter(&image) -> save/toPixmap。

**先记住的坑：** 不要假定每像素 4 字节；写像素前确认 format；跨线程传递隐式共享图像时注意 detach 和修改成本；资源读取失败要检查 isNull。

## 2. 依赖与对象关系

- 头文件：`#include <QImage>`
- 继承自：QPaintDevice
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

QImage 偏向 CPU 端像素处理，QPixmap 偏向窗口系统显示。format 决定像素布局；bits/scanLine 访问原始内存时必须遵守 bytesPerLine 和格式。

### 状态、生命周期和线程

**生命周期：** 绘制上下文必须绑定有效的 paint device，并在合法的绘制阶段使用。QWidget 上通常只在 `paintEvent()` 内创建 painter；离屏图像、打印设备和 pixmap 则有各自的设备生命周期。

**状态与结果：** `save()`/`restore()` 用于隔离局部状态；改变坐标系、画笔或合成模式后要么恢复，要么明确后续绘制也需要该状态。重绘请求和真正绘制是两个阶段，业务状态变化应调用 `update()`。

**线程与事件循环：** 同一个 GUI 控件的绘制在 GUI 线程完成；离屏 QImage 可以按数据所有权在后台处理，但不要让后台线程直接绘制或访问正在显示的 QWidget/QPixmap 资源。

## 3. 直接使用

图片读写、像素算法、离屏绘制、截图处理和跨线程图像数据使用。最终显示到 QWidget 时通常转换为 QPixmap。 使用时通常按这个过程组织：load/fromData -> isNull/format/size -> convertToFormat/scanLine -> QPainter(&image) -> save/toPixmap。

```cpp
QImage image(320, 200, QImage::Format_ARGB32_Premultiplied);
image.fill(Qt::white);
{
    QPainter painter(&image);
    painter.drawText(image.rect(), Qt::AlignCenter, QStringLiteral("Qt"));
}
image.save(QStringLiteral("preview.png"));
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum Format { Format_Invalid, Format_Mono, Format_MonoLSB, Format_Indexed8, Format_RGB32, …, Format_CMYK8888 }`
- `enum InvertMode { InvertRgb, InvertRgba }`

### 公有函数

- `QImage()`
- `QImage(const char *const[] xpm)`
- `QImage(const QSize &size, QImage::Format format)`
- `QImage(const QString &fileName, const char *format = nullptr)`
- `QImage(int width, int height, QImage::Format format)`
- `QImage(const uchar *data, int width, int height, QImage::Format format, QImageCleanupFunction cleanupFunction = nullptr, void *cleanupInfo = nullptr)`
- `QImage(uchar *data, int width, int height, QImage::Format format, QImageCleanupFunction cleanupFunction = nullptr, void *cleanupInfo = nullptr)`
- `QImage(const uchar *data, int width, int height, qsizetype bytesPerLine, QImage::Format format, QImageCleanupFunction cleanupFunction = nullptr, void *cleanupInfo = nullptr)`
- `QImage(uchar *data, int width, int height, qsizetype bytesPerLine, QImage::Format format, QImageCleanupFunction cleanupFunction = nullptr, void *cleanupInfo = nullptr)`
- `QImage(const QImage &image)`
- `QImage(QImage &&other)`
- `virtual ~QImage()`
- `bool allGray() const`
- `void applyColorTransform(const QColorTransform &transform)`
- `(since 6.8) void applyColorTransform(const QColorTransform &transform, QImage::Format toFormat, Qt::ImageConversionFlags flags = Qt::AutoColor)`
- `int bitPlaneCount() const`
- `uchar * bits()`
- `const uchar * bits() const`
- `qsizetype bytesPerLine() const`
- `qint64 cacheKey() const`
- `QRgb color(int i) const`
- `int colorCount() const`
- `QColorSpace colorSpace() const`
- `QList<QRgb> colorTable() const`
- `(since 6.4) QImage colorTransformed(const QColorTransform &transform) const &`
- `(since 6.8) QImage colorTransformed(const QColorTransform &transform, QImage::Format toFormat, Qt::ImageConversionFlags flags = Qt::AutoColor) const &`
- `(since 6.4) QImage colorTransformed(const QColorTransform &transform) &&`
- `(since 6.8) QImage colorTransformed(const QColorTransform &transform, QImage::Format format, Qt::ImageConversionFlags flags = Qt::AutoColor) &&`
- `const uchar * constBits() const`
- `const uchar * constScanLine(int i) const`
- `void convertTo(QImage::Format format, Qt::ImageConversionFlags flags = Qt::AutoColor)`
- `void convertToColorSpace(const QColorSpace &colorSpace)`
- `(since 6.8) void convertToColorSpace(const QColorSpace &colorSpace, QImage::Format format, Qt::ImageConversionFlags flags = Qt::AutoColor)`
- `QImage convertToFormat(QImage::Format format, Qt::ImageConversionFlags flags = Qt::AutoColor) &&`
- `QImage convertToFormat(QImage::Format format, Qt::ImageConversionFlags flags = Qt::AutoColor) const &`
- `QImage convertToFormat(QImage::Format format, const QList<QRgb> &colorTable, Qt::ImageConversionFlags flags = Qt::AutoColor) const`
- `(since 6.0) QImage convertedTo(QImage::Format format, Qt::ImageConversionFlags flags = Qt::AutoColor) &&`
- `(since 6.0) QImage convertedTo(QImage::Format format, Qt::ImageConversionFlags flags = Qt::AutoColor) const &`
- `QImage convertedToColorSpace(const QColorSpace &colorSpace) const`
- `(since 6.8) QImage convertedToColorSpace(const QColorSpace &colorSpace, QImage::Format format, Qt::ImageConversionFlags flags = Qt::AutoColor) &&`
- `(since 6.8) QImage convertedToColorSpace(const QColorSpace &colorSpace, QImage::Format format, Qt::ImageConversionFlags flags = Qt::AutoColor) const &`
- `QImage copy(const QRect &rectangle = QRect()) const`
- `QImage copy(int x, int y, int width, int height) const`
- `QImage createAlphaMask(Qt::ImageConversionFlags flags = Qt::AutoColor) const`
- `QImage createHeuristicMask(bool clipTight = true) const`
- `QImage createMaskFromColor(QRgb color, Qt::MaskMode mode = Qt::MaskInColor) const`
- `int depth() const`
- `(since 6.2) QSizeF deviceIndependentSize() const`
- `qreal devicePixelRatio() const`
- `int dotsPerMeterX() const`
- `int dotsPerMeterY() const`
- `void fill(uint pixelValue)`
- `void fill(Qt::GlobalColor color)`
- `void fill(const QColor &color)`
- `(since 6.9) void flip(Qt::Orientations orient = Qt::Vertical)`
- `(since 6.9) QImage flipped(Qt::Orientations orient = Qt::Vertical) &&`
- `(since 6.9) QImage flipped(Qt::Orientations orient = Qt::Vertical) const &`
- `QImage::Format format() const`
- `bool hasAlphaChannel() const`
- `int height() const`
- `void invertPixels(QImage::InvertMode mode = InvertRgb)`
- `bool isGrayscale() const`
- `bool isNull() const`
- `bool load(const QString &fileName, const char *format = nullptr)`
- `bool load(QIODevice *device, const char *format)`
- `(since 6.2) bool loadFromData(QByteArrayView data, const char *format = nullptr)`
- `bool loadFromData(const QByteArray &data, const char *format = nullptr)`
- `bool loadFromData(const uchar *data, int len, const char *format = nullptr)`
- `(since 6.0, until 6.13) void mirror(bool horizontal = false, bool vertical = true)`
- `(until 6.13) QImage mirrored(bool horizontal = false, bool vertical = true) &&`
- `(until 6.13) QImage mirrored(bool horizontal = false, bool vertical = true) const &`
- `QPoint offset() const`
- `QRgb pixel(const QPoint &position) const`
- `QRgb pixel(int x, int y) const`
- `QColor pixelColor(const QPoint &position) const`
- `QColor pixelColor(int x, int y) const`
- `QPixelFormat pixelFormat() const`
- `int pixelIndex(const QPoint &position) const`
- `int pixelIndex(int x, int y) const`
- `QRect rect() const`
- `bool reinterpretAsFormat(QImage::Format format)`
- `(since 6.0) void rgbSwap()`
- `QImage rgbSwapped() &&`
- `QImage rgbSwapped() const &`
- `bool save(const QString &fileName, const char *format = nullptr, int quality = -1) const`
- `bool save(QIODevice *device, const char *format = nullptr, int quality = -1) const`
- `QImage scaled(const QSize &size, Qt::AspectRatioMode aspectRatioMode = Qt::IgnoreAspectRatio, Qt::TransformationMode transformMode = Qt::FastTransformation) const`
- `QImage scaled(int width, int height, Qt::AspectRatioMode aspectRatioMode = Qt::IgnoreAspectRatio, Qt::TransformationMode transformMode = Qt::FastTransformation) const`
- `QImage scaledToHeight(int height, Qt::TransformationMode mode = Qt::FastTransformation) const`
- `QImage scaledToWidth(int width, Qt::TransformationMode mode = Qt::FastTransformation) const`
- `uchar * scanLine(int i)`
- `const uchar * scanLine(int i) const`
- `void setAlphaChannel(const QImage &alphaChannel)`
- `void setColor(int index, QRgb colorValue)`
- `void setColorCount(int colorCount)`
- `void setColorSpace(const QColorSpace &colorSpace)`
- `void setColorTable(const QList<QRgb> &colors)`
- `void setDevicePixelRatio(qreal scaleFactor)`
- `void setDotsPerMeterX(int x)`
- `void setDotsPerMeterY(int y)`
- `void setOffset(const QPoint &offset)`
- `void setPixel(const QPoint &position, uint index_or_rgb)`
- `void setPixel(int x, int y, uint index_or_rgb)`
- `void setPixelColor(const QPoint &position, const QColor &color)`
- `void setPixelColor(int x, int y, const QColor &color)`
- `void setText(const QString &key, const QString &text)`
- `QSize size() const`
- `qsizetype sizeInBytes() const`
- `void swap(QImage &other)`
- `QString text(const QString &key = QString()) const`
- `QStringList textKeys() const`
- `CGImageRef toCGImage() const`
- `(since 6.0) HBITMAP toHBITMAP() const`
- `(since 6.0) HICON toHICON(const QImage &mask = {}) const`
- `QImage transformed(const QTransform &matrix, Qt::TransformationMode mode = Qt::FastTransformation) const`
- `bool valid(const QPoint &pos) const`
- `bool valid(int x, int y) const`
- `int width() const`
- `operator QVariant() const`
- `bool operator!=(const QImage &image) const`
- `QImage & operator=(QImage &&other)`
- `QImage & operator=(const QImage &image)`
- `bool operator==(const QImage &image) const`

### 静态公有成员

- `(since 6.2) QImage fromData(QByteArrayView data, const char *format = nullptr)`
- `QImage fromData(const QByteArray &data, const char *format = nullptr)`
- `QImage fromData(const uchar *data, int size, const char *format = nullptr)`
- `(since 6.0) QImage fromHBITMAP(HBITMAP hbitmap)`
- `(since 6.0) QImage fromHICON(HICON icon)`
- `QImage::Format toImageFormat(QPixelFormat format)`
- `QPixelFormat toPixelFormat(QImage::Format format)`
- `QTransform trueMatrix(const QTransform &matrix, int width, int height)`

### 相关非成员函数

- `QImageCleanupFunction`
- `QDataStream & operator<<(QDataStream &stream, const QImage &image)`
- `QDataStream & operator>>(QDataStream &stream, QImage &image)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 136 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QImage::Format`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QImage` 暴露的类型声明 `格式化`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Format`。
- 属性名：`QImage`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QImage::InvertMode`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QImage` 暴露的类型声明 `Invert、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:InvertMode`。
- 属性名：`QImage`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QImage::QImage()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QImage` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QImage::QImage(const char *const[] xpm)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QImage` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `xpm`：类型为 `const char *const[]`。没有默认值，调用时必须提供。传入 `const char *const[]` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImage::QImage(const QSize &size, QImage::Format format)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QImage` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `size`：类型为 `const QSize &`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。
- 参数 `format`：类型为 `QImage::Format`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QImage::QImage(const QString &fileName, const char *format = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QImage` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。
- 参数 `format`：类型为 `const char *`。默认值为 `nullptr`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImage::QImage(int width, int height, QImage::Format format)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QImage` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `format`：类型为 `QImage::Format`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImage::QImage(const uchar *data, int width, int height, QImage::Format format, QImageCleanupFunction cleanupFunction = nullptr, void *cleanupInfo = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QImage` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `data`：类型为 `const uchar *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `format`：类型为 `QImage::Format`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `cleanupFunction`：类型为 `QImageCleanupFunction`。默认值为 `nullptr`。传入 `QImageCleanupFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cleanupInfo`：类型为 `void *`。默认值为 `nullptr`。传入 `void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImage::QImage(uchar *data, int width, int height, QImage::Format format, QImageCleanupFunction cleanupFunction = nullptr, void *cleanupInfo = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QImage` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `data`：类型为 `uchar *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `format`：类型为 `QImage::Format`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `cleanupFunction`：类型为 `QImageCleanupFunction`。默认值为 `nullptr`。传入 `QImageCleanupFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cleanupInfo`：类型为 `void *`。默认值为 `nullptr`。传入 `void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImage::QImage(const uchar *data, int width, int height, qsizetype bytesPerLine, QImage::Format format, QImageCleanupFunction cleanupFunction = nullptr, void *cleanupInfo = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QImage` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `data`：类型为 `const uchar *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `bytesPerLine`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `QImage::Format`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `cleanupFunction`：类型为 `QImageCleanupFunction`。默认值为 `nullptr`。传入 `QImageCleanupFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cleanupInfo`：类型为 `void *`。默认值为 `nullptr`。传入 `void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImage::QImage(uchar *data, int width, int height, qsizetype bytesPerLine, QImage::Format format, QImageCleanupFunction cleanupFunction = nullptr, void *cleanupInfo = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QImage` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `data`：类型为 `uchar *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `bytesPerLine`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `QImage::Format`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `cleanupFunction`：类型为 `QImageCleanupFunction`。默认值为 `nullptr`。传入 `QImageCleanupFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cleanupInfo`：类型为 `void *`。默认值为 `nullptr`。传入 `void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImage::QImage(const QImage &image)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QImage` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `image`：类型为 `const QImage &`。没有默认值，调用时必须提供。传入 `const QImage &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QImage::QImage(QImage &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QImage` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `QImage &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QImage::~QImage()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QImage` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QImage::allGray() const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::allGray` 用于计算、查询或取得与“all、Gray”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QImage::applyColorTransform(const QColorTransform &transform)`

**API 类别：** 成员函数说明

**中文解读：** `QImage::applyColorTransform` 用于执行与“应用、Color、Transform”相关的操作。调用时要先确认当前状态和 `transform` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `transform`：类型为 `const QColorTransform &`。没有默认值，调用时必须提供。传入 `const QColorTransform &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] void QImage::applyColorTransform(const QColorTransform &transform, QImage::Format toFormat, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**API 类别：** 成员函数说明

**中文解读：** `QImage::applyColorTransform` 用于执行与“应用、Color、Transform”相关的操作。调用时要先确认当前状态和 `transform`、`toFormat`、`flags` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `transform`：类型为 `const QColorTransform &`。没有默认值，调用时必须提供。传入 `const QColorTransform &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `toFormat`：类型为 `QImage::Format`。没有默认值，调用时必须提供。传入 `QImage::Format` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `Qt::ImageConversionFlags`。默认值为 `Qt::AutoColor`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QImage::bitPlaneCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::bitPlaneCount` 用于计算、查询或取得与“bit、Plane、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `uchar *QImage::bits()`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `bits`，用于取得 `QImage` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`uchar *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const uchar *QImage::bits() const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `bits`，用于取得 `QImage` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`const uchar *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QImage::bytesPerLine() const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::bytesPerLine` 用于计算、查询或取得与“字节、Per、行”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QImage::cacheKey() const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::cacheKey` 用于计算、查询或取得与“cache、Key”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRgb QImage::color(int i) const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::color` 用于计算、查询或取得与“color”相关的操作。调用时要先确认当前状态和 `i` 的有效范围；返回类型是 `QRgb`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRgb`。
- 参数 `i`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QImage::colorCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::colorCount` 用于计算、查询或取得与“color、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QColorSpace QImage::colorSpace() const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::colorSpace` 用于计算、查询或取得与“color、Space”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QColorSpace`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QColorSpace`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QRgb> QImage::colorTable() const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::colorTable` 用于计算、查询或取得与“color、Table”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QRgb>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QRgb>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.4] QImage QImage::colorTransformed(const QColorTransform &transform) const &`

**API 类别：** 成员函数说明

**中文解读：** `QImage::colorTransformed` 用于计算、查询或取得与“color、Transformed”相关的操作。调用时要先确认当前状态和 `transform` 的有效范围；返回类型是 `QImage`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `transform`：类型为 `const QColorTransform &`。没有默认值，调用时必须提供。传入 `const QColorTransform &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] QImage QImage::colorTransformed(const QColorTransform &transform, QImage::Format toFormat, Qt::ImageConversionFlags flags = Qt::AutoColor) const &`

**API 类别：** 成员函数说明

**中文解读：** `QImage::colorTransformed` 用于计算、查询或取得与“color、Transformed”相关的操作。调用时要先确认当前状态和 `transform`、`toFormat`、`flags` 的有效范围；返回类型是 `QImage`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `transform`：类型为 `const QColorTransform &`。没有默认值，调用时必须提供。传入 `const QColorTransform &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `toFormat`：类型为 `QImage::Format`。没有默认值，调用时必须提供。传入 `QImage::Format` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `Qt::ImageConversionFlags`。默认值为 `Qt::AutoColor`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.4] QImage QImage::colorTransformed(const QColorTransform &transform) &&`

**API 类别：** 成员函数说明

**中文解读：** `QImage::colorTransformed` 用于计算、查询或取得与“color、Transformed”相关的操作。调用时要先确认当前状态和 `transform` 的有效范围；返回类型是 `QImage`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `transform`：类型为 `const QColorTransform &`。没有默认值，调用时必须提供。传入 `const QColorTransform &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] QImage QImage::colorTransformed(const QColorTransform &transform, QImage::Format format, Qt::ImageConversionFlags flags = Qt::AutoColor) &&`

**API 类别：** 成员函数说明

**中文解读：** `QImage::colorTransformed` 用于计算、查询或取得与“color、Transformed”相关的操作。调用时要先确认当前状态和 `transform`、`format`、`flags` 的有效范围；返回类型是 `QImage`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `transform`：类型为 `const QColorTransform &`。没有默认值，调用时必须提供。传入 `const QColorTransform &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `QImage::Format`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `flags`：类型为 `Qt::ImageConversionFlags`。默认值为 `Qt::AutoColor`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const uchar *QImage::constBits() const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `constBits`，用于取得 `QImage` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`const uchar *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const uchar *QImage::constScanLine(int i) const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::constScanLine` 用于计算、查询或取得与“const、Scan、行”相关的操作。调用时要先确认当前状态和 `i` 的有效范围；返回类型是 `const uchar *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const uchar *`。
- 参数 `i`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QImage::convertTo(QImage::Format format, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `convertTo`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`void`。
- 参数 `format`：类型为 `QImage::Format`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `flags`：类型为 `Qt::ImageConversionFlags`。默认值为 `Qt::AutoColor`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QImage::convertToColorSpace(const QColorSpace &colorSpace)`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `convertToColorSpace`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`void`。
- 参数 `colorSpace`：类型为 `const QColorSpace &`。没有默认值，调用时必须提供。传入 `const QColorSpace &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] void QImage::convertToColorSpace(const QColorSpace &colorSpace, QImage::Format format, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `convertToColorSpace`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`void`。
- 参数 `colorSpace`：类型为 `const QColorSpace &`。没有默认值，调用时必须提供。传入 `const QColorSpace &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `QImage::Format`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `flags`：类型为 `Qt::ImageConversionFlags`。默认值为 `Qt::AutoColor`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImage QImage::convertToFormat(QImage::Format format, Qt::ImageConversionFlags flags = Qt::AutoColor) &&`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `convertToFormat`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `format`：类型为 `QImage::Format`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `flags`：类型为 `Qt::ImageConversionFlags`。默认值为 `Qt::AutoColor`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImage QImage::convertToFormat(QImage::Format format, const QList<QRgb> &colorTable, Qt::ImageConversionFlags flags = Qt::AutoColor) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `convertToFormat`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `format`：类型为 `QImage::Format`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `colorTable`：类型为 `const QList<QRgb> &`。没有默认值，调用时必须提供。传入 `const QList<QRgb> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `Qt::ImageConversionFlags`。默认值为 `Qt::AutoColor`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QImage QImage::convertedTo(QImage::Format format, Qt::ImageConversionFlags flags = Qt::AutoColor) &&`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `convertedTo`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `format`：类型为 `QImage::Format`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `flags`：类型为 `Qt::ImageConversionFlags`。默认值为 `Qt::AutoColor`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImage QImage::convertedToColorSpace(const QColorSpace &colorSpace) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `convertedToColorSpace`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `colorSpace`：类型为 `const QColorSpace &`。没有默认值，调用时必须提供。传入 `const QColorSpace &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] QImage QImage::convertedToColorSpace(const QColorSpace &colorSpace, QImage::Format format, Qt::ImageConversionFlags flags = Qt::AutoColor) &&`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `convertedToColorSpace`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `colorSpace`：类型为 `const QColorSpace &`。没有默认值，调用时必须提供。传入 `const QColorSpace &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `QImage::Format`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `flags`：类型为 `Qt::ImageConversionFlags`。默认值为 `Qt::AutoColor`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImage QImage::copy(const QRect &rectangle = QRect()) const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::copy` 用于计算、查询或取得与“copy”相关的操作。调用时要先确认当前状态和 `rectangle` 的有效范围；返回类型是 `QImage`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `rectangle`：类型为 `const QRect &`。默认值为 `QRect()`。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImage QImage::copy(int x, int y, int width, int height) const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::copy` 用于计算、查询或取得与“copy”相关的操作。调用时要先确认当前状态和 `x`、`y`、`width`、`height` 的有效范围；返回类型是 `QImage`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImage QImage::createAlphaMask(Qt::ImageConversionFlags flags = Qt::AutoColor) const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::createAlphaMask` 用于计算、查询或取得与“创建、Alpha、Mask”相关的操作。调用时要先确认当前状态和 `flags` 的有效范围；返回类型是 `QImage`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `flags`：类型为 `Qt::ImageConversionFlags`。默认值为 `Qt::AutoColor`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImage QImage::createHeuristicMask(bool clipTight = true) const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::createHeuristicMask` 用于计算、查询或取得与“创建、Heuristic、Mask”相关的操作。调用时要先确认当前状态和 `clipTight` 的有效范围；返回类型是 `QImage`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `clipTight`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImage QImage::createMaskFromColor(QRgb color, Qt::MaskMode mode = Qt::MaskInColor) const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::createMaskFromColor` 用于计算、查询或取得与“创建、Mask、转换进入、Color”相关的操作。调用时要先确认当前状态和 `color`、`mode` 的有效范围；返回类型是 `QImage`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `color`：类型为 `QRgb`。没有默认值，调用时必须提供。传入 `QRgb` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mode`：类型为 `Qt::MaskMode`。默认值为 `Qt::MaskInColor`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QImage::depth() const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::depth` 用于计算、查询或取得与“depth”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] QSizeF QImage::deviceIndependentSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::deviceIndependentSize` 用于计算、查询或取得与“device、Independent、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSizeF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSizeF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QImage::devicePixelRatio() const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::devicePixelRatio` 用于计算、查询或取得与“device、Pixel、Ratio”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QImage::dotsPerMeterX() const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::dotsPerMeterX` 用于计算、查询或取得与“dots、Per、Meter、X”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QImage::dotsPerMeterY() const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::dotsPerMeterY` 用于计算、查询或取得与“dots、Per、Meter、Y”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QImage::fill(uint pixelValue)`

**API 类别：** 成员函数说明

**中文解读：** `QImage::fill` 用于执行与“fill”相关的操作。调用时要先确认当前状态和 `pixelValue` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `pixelValue`：类型为 `uint`。没有默认值，调用时必须提供。传入 `uint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QImage::fill(Qt::GlobalColor color)`

**API 类别：** 成员函数说明

**中文解读：** `QImage::fill` 用于执行与“fill”相关的操作。调用时要先确认当前状态和 `color` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `color`：类型为 `Qt::GlobalColor`。没有默认值，调用时必须提供。传入 `Qt::GlobalColor` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QImage::fill(const QColor &color)`

**API 类别：** 成员函数说明

**中文解读：** `QImage::fill` 用于执行与“fill”相关的操作。调用时要先确认当前状态和 `color` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `color`：类型为 `const QColor &`。没有默认值，调用时必须提供。传入 `const QColor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] void QImage::flip(Qt::Orientations orient = Qt::Vertical)`

**API 类别：** 成员函数说明

**中文解读：** `QImage::flip` 用于执行与“flip”相关的操作。调用时要先确认当前状态和 `orient` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `orient`：类型为 `Qt::Orientations`。默认值为 `Qt::Vertical`。传入 `Qt::Orientations` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] QImage QImage::flipped(Qt::Orientations orient = Qt::Vertical) &&`

**API 类别：** 成员函数说明

**中文解读：** `QImage::flipped` 用于计算、查询或取得与“flipped”相关的操作。调用时要先确认当前状态和 `orient` 的有效范围；返回类型是 `QImage`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `orient`：类型为 `Qt::Orientations`。默认值为 `Qt::Vertical`。传入 `Qt::Orientations` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImage::Format QImage::format() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `format`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QImage::Format`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.2] QImage QImage::fromData(QByteArrayView data, const char *format = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromData`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `data`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `format`：类型为 `const char *`。默认值为 `nullptr`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QImage QImage::fromData(const QByteArray &data, const char *format = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromData`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `data`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `format`：类型为 `const char *`。默认值为 `nullptr`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QImage QImage::fromData(const uchar *data, int size, const char *format = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromData`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `data`：类型为 `const uchar *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `size`：类型为 `int`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。
- 参数 `format`：类型为 `const char *`。默认值为 `nullptr`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.0] QImage QImage::fromHBITMAP(HBITMAP hbitmap)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromHBITMAP`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `hbitmap`：类型为 `HBITMAP`。没有默认值，调用时必须提供。传入 `HBITMAP` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.0] QImage QImage::fromHICON(HICON icon)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromHICON`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `icon`：类型为 `HICON`。没有默认值，调用时必须提供。传入 `HICON` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QImage::hasAlphaChannel() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasAlphaChannel`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QImage::height() const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::height` 用于计算、查询或取得与“高度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QImage::invertPixels(QImage::InvertMode mode = InvertRgb)`

**API 类别：** 成员函数说明

**中文解读：** `QImage::invertPixels` 用于执行与“invert、Pixels”相关的操作。调用时要先确认当前状态和 `mode` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `QImage::InvertMode`。默认值为 `InvertRgb`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QImage::isGrayscale() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isGrayscale`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QImage::isNull() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isNull`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QImage::load(const QString &fileName, const char *format = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `load`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`bool`。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。
- 参数 `format`：类型为 `const char *`。默认值为 `nullptr`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QImage::load(QIODevice *device, const char *format)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `load`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`bool`。
- 参数 `device`：类型为 `QIODevice *`。没有默认值，调用时必须提供。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。
- 参数 `format`：类型为 `const char *`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] bool QImage::loadFromData(QByteArrayView data, const char *format = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `loadFromData`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`bool`。
- 参数 `data`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `format`：类型为 `const char *`。默认值为 `nullptr`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QImage::loadFromData(const QByteArray &data, const char *format = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `loadFromData`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`bool`。
- 参数 `data`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `format`：类型为 `const char *`。默认值为 `nullptr`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QImage::loadFromData(const uchar *data, int len, const char *format = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `loadFromData`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`bool`。
- 参数 `data`：类型为 `const uchar *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `len`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `const char *`。默认值为 `nullptr`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0, until 6.13] void QImage::mirror(bool horizontal = false, bool vertical = true)`

**API 类别：** 成员函数说明

**中文解读：** `QImage::mirror` 用于执行与“mirror”相关的操作。调用时要先确认当前状态和 `horizontal`、`vertical` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `horizontal`：类型为 `bool`。默认值为 `false`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `vertical`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[until 6.13] QImage QImage::mirrored(bool horizontal = false, bool vertical = true) &&`

**API 类别：** 成员函数说明

**中文解读：** `QImage::mirrored` 用于计算、查询或取得与“mirrored”相关的操作。调用时要先确认当前状态和 `horizontal`、`vertical` 的有效范围；返回类型是 `QImage`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `horizontal`：类型为 `bool`。默认值为 `false`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `vertical`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPoint QImage::offset() const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::offset` 用于计算、查询或取得与“offset”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPoint`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPoint`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRgb QImage::pixel(const QPoint &position) const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::pixel` 用于计算、查询或取得与“pixel”相关的操作。调用时要先确认当前状态和 `position` 的有效范围；返回类型是 `QRgb`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRgb`。
- 参数 `position`：类型为 `const QPoint &`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRgb QImage::pixel(int x, int y) const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::pixel` 用于计算、查询或取得与“pixel”相关的操作。调用时要先确认当前状态和 `x`、`y` 的有效范围；返回类型是 `QRgb`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRgb`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QColor QImage::pixelColor(const QPoint &position) const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::pixelColor` 用于计算、查询或取得与“pixel、Color”相关的操作。调用时要先确认当前状态和 `position` 的有效范围；返回类型是 `QColor`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QColor`。
- 参数 `position`：类型为 `const QPoint &`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QColor QImage::pixelColor(int x, int y) const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::pixelColor` 用于计算、查询或取得与“pixel、Color”相关的操作。调用时要先确认当前状态和 `x`、`y` 的有效范围；返回类型是 `QColor`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QColor`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QPixelFormat QImage::pixelFormat() const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::pixelFormat` 用于计算、查询或取得与“pixel、格式化”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPixelFormat`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPixelFormat`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QImage::pixelIndex(const QPoint &position) const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::pixelIndex` 用于计算、查询或取得与“pixel、索引”相关的操作。调用时要先确认当前状态和 `position` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `position`：类型为 `const QPoint &`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QImage::pixelIndex(int x, int y) const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::pixelIndex` 用于计算、查询或取得与“pixel、索引”相关的操作。调用时要先确认当前状态和 `x`、`y` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRect QImage::rect() const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::rect` 用于计算、查询或取得与“rect”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QImage::reinterpretAsFormat(QImage::Format format)`

**API 类别：** 成员函数说明

**中文解读：** `QImage::reinterpretAsFormat` 用于计算、查询或取得与“reinterpret、As、格式化”相关的操作。调用时要先确认当前状态和 `format` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `format`：类型为 `QImage::Format`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] void QImage::rgbSwap()`

**API 类别：** 成员函数说明

**中文解读：** `QImage::rgbSwap` 用于执行与“rgb、Swap”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImage QImage::rgbSwapped() &&`

**API 类别：** 成员函数说明

**中文解读：** `QImage::rgbSwapped` 用于计算、查询或取得与“rgb、Swapped”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QImage`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QImage`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QImage::save(const QString &fileName, const char *format = nullptr, int quality = -1) const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::save` 用于计算、查询或取得与“保存”相关的操作。调用时要先确认当前状态和 `fileName`、`format`、`quality` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。
- 参数 `format`：类型为 `const char *`。默认值为 `nullptr`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `quality`：类型为 `int`。默认值为 `-1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QImage::save(QIODevice *device, const char *format = nullptr, int quality = -1) const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::save` 用于计算、查询或取得与“保存”相关的操作。调用时要先确认当前状态和 `device`、`format`、`quality` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `device`：类型为 `QIODevice *`。没有默认值，调用时必须提供。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。
- 参数 `format`：类型为 `const char *`。默认值为 `nullptr`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `quality`：类型为 `int`。默认值为 `-1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImage QImage::scaled(const QSize &size, Qt::AspectRatioMode aspectRatioMode = Qt::IgnoreAspectRatio, Qt::TransformationMode transformMode = Qt::FastTransformation) const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::scaled` 用于计算、查询或取得与“scaled”相关的操作。调用时要先确认当前状态和 `size`、`aspectRatioMode`、`transformMode` 的有效范围；返回类型是 `QImage`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `size`：类型为 `const QSize &`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。
- 参数 `aspectRatioMode`：类型为 `Qt::AspectRatioMode`。默认值为 `Qt::IgnoreAspectRatio`。传入 `Qt::AspectRatioMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `transformMode`：类型为 `Qt::TransformationMode`。默认值为 `Qt::FastTransformation`。传入 `Qt::TransformationMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImage QImage::scaled(int width, int height, Qt::AspectRatioMode aspectRatioMode = Qt::IgnoreAspectRatio, Qt::TransformationMode transformMode = Qt::FastTransformation) const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::scaled` 用于计算、查询或取得与“scaled”相关的操作。调用时要先确认当前状态和 `width`、`height`、`aspectRatioMode`、`transformMode` 的有效范围；返回类型是 `QImage`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `aspectRatioMode`：类型为 `Qt::AspectRatioMode`。默认值为 `Qt::IgnoreAspectRatio`。传入 `Qt::AspectRatioMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `transformMode`：类型为 `Qt::TransformationMode`。默认值为 `Qt::FastTransformation`。传入 `Qt::TransformationMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImage QImage::scaledToHeight(int height, Qt::TransformationMode mode = Qt::FastTransformation) const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::scaledToHeight` 用于计算、查询或取得与“scaled、转换输出、高度”相关的操作。调用时要先确认当前状态和 `height`、`mode` 的有效范围；返回类型是 `QImage`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `mode`：类型为 `Qt::TransformationMode`。默认值为 `Qt::FastTransformation`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImage QImage::scaledToWidth(int width, Qt::TransformationMode mode = Qt::FastTransformation) const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::scaledToWidth` 用于计算、查询或取得与“scaled、转换输出、宽度”相关的操作。调用时要先确认当前状态和 `width`、`mode` 的有效范围；返回类型是 `QImage`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `mode`：类型为 `Qt::TransformationMode`。默认值为 `Qt::FastTransformation`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `uchar *QImage::scanLine(int i)`

**API 类别：** 成员函数说明

**中文解读：** `QImage::scanLine` 用于计算、查询或取得与“scan、行”相关的操作。调用时要先确认当前状态和 `i` 的有效范围；返回类型是 `uchar *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`uchar *`。
- 参数 `i`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const uchar *QImage::scanLine(int i) const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::scanLine` 用于计算、查询或取得与“scan、行”相关的操作。调用时要先确认当前状态和 `i` 的有效范围；返回类型是 `const uchar *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const uchar *`。
- 参数 `i`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QImage::setAlphaChannel(const QImage &alphaChannel)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAlphaChannel`。调用它会改变 `QImage` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `alphaChannel`：类型为 `const QImage &`。没有默认值，调用时必须提供。传入 `const QImage &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QImage::setColor(int index, QRgb colorValue)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setColor`。调用它会改变 `QImage` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `colorValue`：类型为 `QRgb`。没有默认值，调用时必须提供。传入 `QRgb` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QImage::setColorCount(int colorCount)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setColorCount`。调用它会改变 `QImage` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `colorCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QImage::setColorSpace(const QColorSpace &colorSpace)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setColorSpace`。调用它会改变 `QImage` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `colorSpace`：类型为 `const QColorSpace &`。没有默认值，调用时必须提供。传入 `const QColorSpace &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QImage::setColorTable(const QList<QRgb> &colors)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setColorTable`。调用它会改变 `QImage` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `colors`：类型为 `const QList<QRgb> &`。没有默认值，调用时必须提供。传入 `const QList<QRgb> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QImage::setDevicePixelRatio(qreal scaleFactor)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDevicePixelRatio`。调用它会改变 `QImage` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `scaleFactor`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QImage::setDotsPerMeterX(int x)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDotsPerMeterX`。调用它会改变 `QImage` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QImage::setDotsPerMeterY(int y)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDotsPerMeterY`。调用它会改变 `QImage` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QImage::setOffset(const QPoint &offset)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setOffset`。调用它会改变 `QImage` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `offset`：类型为 `const QPoint &`。没有默认值，调用时必须提供。传入 `const QPoint &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QImage::setPixel(const QPoint &position, uint index_or_rgb)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPixel`。调用它会改变 `QImage` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `position`：类型为 `const QPoint &`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `index_or_rgb`：类型为 `uint`。没有默认值，调用时必须提供。传入 `uint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QImage::setPixel(int x, int y, uint index_or_rgb)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPixel`。调用它会改变 `QImage` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `index_or_rgb`：类型为 `uint`。没有默认值，调用时必须提供。传入 `uint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QImage::setPixelColor(const QPoint &position, const QColor &color)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPixelColor`。调用它会改变 `QImage` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `position`：类型为 `const QPoint &`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `color`：类型为 `const QColor &`。没有默认值，调用时必须提供。传入 `const QColor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QImage::setPixelColor(int x, int y, const QColor &color)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPixelColor`。调用它会改变 `QImage` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `color`：类型为 `const QColor &`。没有默认值，调用时必须提供。传入 `const QColor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QImage::setText(const QString &key, const QString &text)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setText`。调用它会改变 `QImage` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `key`：类型为 `const QString &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSize QImage::size() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `size`，返回 `QImage` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QImage::sizeInBytes() const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::sizeInBytes` 用于计算、查询或取得与“尺寸或数量、In、字节”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QImage::swap(QImage &other)`

**API 类别：** 成员函数说明

**中文解读：** `QImage::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QImage &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QImage::text(const QString &key = QString()) const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::text` 用于计算、查询或取得与“文本”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `key`：类型为 `const QString &`。默认值为 `QString()`。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList QImage::textKeys() const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::textKeys` 用于计算、查询或取得与“文本、Keys”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `CGImageRef QImage::toCGImage() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toCGImage`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`CGImageRef`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] HBITMAP QImage::toHBITMAP() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toHBITMAP`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`HBITMAP`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] HICON QImage::toHICON(const QImage &mask = {}) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toHICON`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`HICON`。
- 参数 `mask`：类型为 `const QImage &`。默认值为 `{}`。传入 `const QImage &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static noexcept] QImage::Format QImage::toImageFormat(QPixelFormat format)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `toImageFormat`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QImage::Format`。
- 参数 `format`：类型为 `QPixelFormat`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static noexcept] QPixelFormat QImage::toPixelFormat(QImage::Format format)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `toPixelFormat`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QPixelFormat`。
- 参数 `format`：类型为 `QImage::Format`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImage QImage::transformed(const QTransform &matrix, Qt::TransformationMode mode = Qt::FastTransformation) const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::transformed` 用于计算、查询或取得与“transformed”相关的操作。调用时要先确认当前状态和 `matrix`、`mode` 的有效范围；返回类型是 `QImage`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `matrix`：类型为 `const QTransform &`。没有默认值，调用时必须提供。传入 `const QTransform &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mode`：类型为 `Qt::TransformationMode`。默认值为 `Qt::FastTransformation`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QTransform QImage::trueMatrix(const QTransform &matrix, int width, int height)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `trueMatrix`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QTransform`。
- 参数 `matrix`：类型为 `const QTransform &`。没有默认值，调用时必须提供。传入 `const QTransform &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QImage::valid(const QPoint &pos) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `valid`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `pos`：类型为 `const QPoint &`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QImage::valid(int x, int y) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `valid`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QImage::width() const`

**API 类别：** 成员函数说明

**中文解读：** `QImage::width` 用于计算、查询或取得与“宽度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImage::operator QVariant() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QImage` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`由运算符声明决定`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QImage::operator!=(const QImage &image) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QImage` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `image`：类型为 `const QImage &`。没有默认值，调用时必须提供。传入 `const QImage &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QImage &QImage::operator=(QImage &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QImage` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QImage &`。
- 参数 `other`：类型为 `QImage &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImage &QImage::operator=(const QImage &image)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QImage` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QImage &`。
- 参数 `image`：类型为 `const QImage &`。没有默认值，调用时必须提供。传入 `const QImage &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QImage::operator==(const QImage &image) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QImage` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `image`：类型为 `const QImage &`。没有默认值，调用时必须提供。传入 `const QImage &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImageCleanupFunction`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QImage` 的 `Q、Image、Cleanup、Function` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDataStream &operator<<(QDataStream &stream, const QImage &image)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QImage` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDataStream &`。
- 参数 `stream`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `image`：类型为 `const QImage &`。没有默认值，调用时必须提供。传入 `const QImage &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDataStream &operator>>(QDataStream &stream, QImage &image)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QImage` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDataStream &`。
- 参数 `stream`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `image`：类型为 `QImage &`。没有默认值，调用时必须提供。传入 `QImage &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImage convertToFormat(QImage::Format format, Qt::ImageConversionFlags flags = Qt::AutoColor) const &`

**API 类别：** 公有函数

**中文解读：** 这是转换/映射 API `convertToFormat`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `format`：类型为 `QImage::Format`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `flags`：类型为 `Qt::ImageConversionFlags`。默认值为 `Qt::AutoColor`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.0) QImage convertedTo(QImage::Format format, Qt::ImageConversionFlags flags = Qt::AutoColor) const &`

**API 类别：** 公有函数

**中文解读：** 这是转换/映射 API `convertedTo`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `format`：类型为 `QImage::Format`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `flags`：类型为 `Qt::ImageConversionFlags`。默认值为 `Qt::AutoColor`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.8) QImage convertedToColorSpace(const QColorSpace &colorSpace, QImage::Format format, Qt::ImageConversionFlags flags = Qt::AutoColor) const &`

**API 类别：** 公有函数

**中文解读：** 这是转换/映射 API `convertedToColorSpace`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `colorSpace`：类型为 `const QColorSpace &`。没有默认值，调用时必须提供。传入 `const QColorSpace &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `QImage::Format`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `flags`：类型为 `Qt::ImageConversionFlags`。默认值为 `Qt::AutoColor`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.9) QImage flipped(Qt::Orientations orient = Qt::Vertical) const &`

**API 类别：** 公有函数

**中文解读：** `QImage::flipped` 用于计算、查询或取得与“flipped”相关的操作。调用时要先确认当前状态和 `orient` 的有效范围；返回类型是 `QImage`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `orient`：类型为 `Qt::Orientations`。默认值为 `Qt::Vertical`。传入 `Qt::Orientations` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(until 6.13) QImage mirrored(bool horizontal = false, bool vertical = true) const &`

**API 类别：** 公有函数

**中文解读：** `QImage::mirrored` 用于计算、查询或取得与“mirrored”相关的操作。调用时要先确认当前状态和 `horizontal`、`vertical` 的有效范围；返回类型是 `(until 6.13) QImage`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`(until 6.13) QImage`。
- 参数 `horizontal`：类型为 `bool`。默认值为 `false`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `vertical`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImage rgbSwapped() const &`

**API 类别：** 公有函数

**中文解读：** `QImage::rgbSwapped` 用于计算、查询或取得与“rgb、Swapped”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QImage`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QImage`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

绘制上下文必须绑定有效的 paint device，并在合法的绘制阶段使用。QWidget 上通常只在 `paintEvent()` 内创建 painter；离屏图像、打印设备和 pixmap 则有各自的设备生命周期。

### 状态和错误边界

`save()`/`restore()` 用于隔离局部状态；改变坐标系、画笔或合成模式后要么恢复，要么明确后续绘制也需要该状态。重绘请求和真正绘制是两个阶段，业务状态变化应调用 `update()`。

### 线程边界

同一个 GUI 控件的绘制在 GUI 线程完成；离屏 QImage 可以按数据所有权在后台处理，但不要让后台线程直接绘制或访问正在显示的 QWidget/QPixmap 资源。

### 最容易出现的错误

不要假定每像素 4 字节；写像素前确认 format；跨线程传递隐式共享图像时注意 detach 和修改成本；资源读取失败要检查 isNull。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QImage` 所属机制类型：二维绘制状态机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
