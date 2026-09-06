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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QImage::Format`

**作用与语义：**

以下图像格式可用Qt。请见表格后的注释。
- `QImage::Format_Invalid`：`0`;该图像无效。
- `QImage::Format_Mono`：`1`;图像以每像素1位存储。字节先打包最高有效位（MSB）。
- `QImage::Format_MonoLSB`：`2`;图像以每像素1位存储。字节先用低有效位（LSB）打包。
- `QImage::Format_Indexed8`：`3`;图像通过8位索引存储为色彩映射。
- `QImage::Format_RGB32`：`4`;图像使用32位RGB格式（0xffRRGGBB）存储。
- `QImage::Format_ARGB32`：`5`;图像使用32位ARGB格式（0xAARRGGBB）存储。
- `QImage::Format_ARGB32_Premultiplied`：`6`;图像使用预乘法的32位ARGB格式（0xAARRGGBB）存储，即红、绿、蓝通道乘以α分量除以255。（如果RR、GG或BB的值高于alpha通道，结果未定义。）某些操作（如使用alpha混合的图像合成）使用预乘法ARGB32比普通ARGB32更快。
- `QImage::Format_RGB16`：`7`;图像使用16位RGB格式（5-6-5）存储。
- `QImage::Format_ARGB8565_Premultiplied`：`8`;图像使用预乘法的24位ARGB格式（8-5-6-5）存储。
- `QImage::Format_RGB666`：`9`;图像使用24位RGB格式（6-6-6）存储。未使用的最高有效位始终为零。
- `QImage::Format_ARGB6666_Premultiplied`：`10`;图像使用预乘法的24位ARGB格式（6-6-6-6）存储。
- `QImage::Format_RGB555`：`11`;图像使用16位RGB格式（5-5-5）存储。未使用的最高有效位始终为零。
- `QImage::Format_ARGB8555_Premultiplied`：`12`;图像使用预乘法的24位ARGB格式（8-5-5-5）存储。
- `QImage::Format_RGB888`：`13`;图像使用24位RGB格式（8-8-8）存储。
- `QImage::Format_RGB444`：`14`;图像使用16位RGB格式（4-4-4）存储。未使用的位始终为零。
- `QImage::Format_ARGB4444_Premultiplied`：`15`;图像使用预乘法的16位ARGB格式（4-4-4-4）存储。
- `QImage::Format_RGBX8888 (since Qt 5.2)`：`16`;图像采用32位字节顺序的RGB（x）格式（8-8-8-8）存储。这与Format_RGBA8888相同，但alpha必须始终为255。
- `QImage::Format_RGBA8888 (since Qt 5.2)`：`17`;图像采用32位字节排序的RGBA格式（8-8-8-8）存储。
- `QImage::Format_RGBA8888_Premultiplied (since Qt 5.2)`：`18`;图像使用预乘的32位字节顺序RGBA格式（8-8-8-8）存储。
- `QImage::Format_BGR30 (since Qt 5.4)`：`19`;图像使用32位BGR格式（x-10-10-10）存储。
- `QImage::Format_A2BGR30_Premultiplied (since Qt 5.4)`：`20`;图像使用32位预乘法ABGR格式（2-10-10-10）存储。
- `QImage::Format_RGB30 (since Qt 5.4)`：`21`;图像使用32位RGB格式（x-10-10-10）存储。
- `QImage::Format_A2RGB30_Premultiplied (since Qt 5.4)`：`22`;图像采用32位预乘法ARGB格式（2-10-10-10）存储。
- `QImage::Format_Alpha8 (since Qt 5.5)`：`23`;图像采用8位仅Alpha格式存储。
- `QImage::Format_Grayscale8 (since Qt 5.5)`：`24`;图像采用8位灰度格式存储。
- `QImage::Format_Grayscale16 (since Qt 5.13)`：`28`;图像采用16位灰度格式存储。
- `QImage::Format_RGBX64 (since Qt 5.12)`：`25`;图像采用64位半字序RGB（x）格式（16-16-16-16）存储。这与Format_RGBA64相同，但alpha必须始终为65535。
- `QImage::Format_RGBA64 (since Qt 5.12)`：`26`;图像使用64位半字序RGBA格式（16-16-16-16）存储。
- `QImage::Format_RGBA64_Premultiplied (since Qt 5.12)`：`27`;图像使用预乘的64位半字序RGBA格式（16-16-16-16）存储。
- `QImage::Format_BGR888 (since Qt 5.14)`：`29`;图像使用24位BGR格式存储。
- `QImage::Format_RGBX16FPx4 (since Qt 6.2)`：`30`;图像使用四个16位半字浮点RGBx格式（16FP-16FP-16FP-16FP）存储。这与Format_RGBA16FPx4相同，但alpha必须始终为1.0。
- `QImage::Format_RGBA16FPx4 (since Qt 6.2)`：`31`;图像使用四位16位半字浮点RGBA格式存储（16FP-16FP-16FP-16FP）。
- `QImage::Format_RGBA16FPx4_Premultiplied (since Qt 6.2)`：`32`;图像使用预乘的四位16位半字浮点RGBA格式存储（16FP-16FP-16FP-16FP）。
- `QImage::Format_RGBX32FPx4 (since Qt 6.2)`：`33`;图像使用四位32位浮点RGBx格式存储（32FP-32FP-32FP-32FP）。这与Format_RGBA32FPx4相同，但alpha必须始终为1.0。
- `QImage::Format_RGBA32FPx4 (since Qt 6.2)`：`34`;图像采用四位32位浮点RGBA格式（32FP-32FP-32FP-32FP）存储。
- `QImage::Format_RGBA32FPx4_Premultiplied (since Qt 6.2)`：`35`;图像使用预乘的四位32位浮点RGBA格式（32FP-32FP-32FP-32FP）存储。
- `QImage::Format_CMYK8888 (since Qt 6.8)`：`36`;图像采用32位字节顺序的CMYK格式存储。
字节排序格式具有`QPixelFormat::UnsignedByte` `QPixelFormat::typeInterpretation()`，意味着单个颜色成分以固定顺序存储在内存中，例如 0xRR、0xGG、0xBB、0xAA，无论平台的端序如何。这些格式应作为单个字节读取，若分大块读取则应被解释为`QPixelFormat::BigEndian`。
注意：不支持格式为 QImage：：Format_Indexed8 或 QImage：：Format_CMYK8888 的 `QImage`。
注意：避免使用`QPainter`直接渲染到大多数格式。渲染最适合`Format_RGB32`和`Format_ARGB32_Premultiplied`格式，其次是渲染到`Format_RGB16`、`Format_RGBX8888`、`Format_RGBA8888_Premultiplied`、`Format_RGBX64`和`Format_RGBA64_Premultiplied`格式。

### `enum QImage::InvertMode`

**作用与语义：**

该枚举类型用于描述像素值在`invertPixels()`函数中应如何反转。
- `QImage::InvertRgb`：`0`;仅反转RGB值，保持阿尔法通道不变。
- `QImage::InvertRgba`：`1`;反转所有通道，包括阿尔法通道。

### `[noexcept] QImage::QImage()`

**作用与语义：**

构造一个空像。

### `[explicit] QImage::QImage(const char *const[] xpm)`

**作用与语义：**

从给定的`xpm`图像构造图像。
确保图片是有效的 XPM 图像。错误会被默理。
请注意，可以通过使用一个不寻常的声明来稍微压缩 XPM 变量：
额外的 `const`使整个定义只读，这稍微更高效（例如代码在共享库中时），并且可以随应用程序存储在 ROM 中。

**官方示例：**

```cpp
 static const char * const start_xpm[] = {
     "16 15 8 1",
     "a c #cec6bd",
     // etc.
 };
```

### `QImage::QImage(const QSize &size, QImage::Format format)`

**作用与语义：**

构造出给定`size`和`format`的图像。
如果无法分配内存，则返回`null`图像。
警告：这会创建一个包含未初始化数据的QImage。在用`QPainter`绘制之前，请调用`fill()`填充合适的像素值。

### `[explicit] QImage::QImage(const QString &fileName, const char *format = nullptr)`

**作用与语义：**

构建一张图像，并尝试从带有指定`fileName`的文件中加载图像。
加载器尝试使用指定的`format`读取图像。如果未指定`format`（默认为默认），则根据文件后缀和头部自动检测。详情请参见 {`QImageReader::setAutoDetectImageFormat()`}{`QImageReader`}。
如果图像加载失败，该对象为空图像。
文件名可以指磁盘上的实际文件，也可以指应用程序的嵌入式资源之一。有关如何将镜像和其他资源文件嵌入应用程序可执行文件的详细信息，请参见资源系统概述。

### `QImage::QImage(int width, int height, QImage::Format format)`

**作用与语义：**

构造给定`width`、`height`和`format`的图像。
如果无法分配内存，会返回`null`图像。
警告：这将生成一个包含未初始化数据的QImage。在用 `QPainter` 绘制之前，请调用 `fill()` 填充合适的像素值。

### `QImage::QImage(const uchar *data, int width, int height, QImage::Format format, QImageCleanupFunction cleanupFunction = nullptr, void *cleanupInfo = nullptr)`

**作用与语义：**

构造给定`width` `height`和`format`的图像，使用现有的只读存储缓冲区 `data`。`width`和`height`必须以像素为单位，`data`必须为32位对齐，且图像中每条扫描线数据也必须为32位对齐。
缓冲区必须在整个QImage及其未被修改或以其他方式分离的副本的整个生命周期内保持有效。映像在销毁时不会删除缓冲区。你可以提供函数指针`cleanupFunction`以及一个额外的指针`cleanupInfo`，当最后一份副本被销毁时调用。
如果`format`是索引色格式，图像颜色表最初是空的，必须通过`setColorCount()`或`setColorTable()`充分展开后才能使用图像。
与类似的QImage构造器使用非const数据缓冲区不同，该版本永远不会改变缓冲区的内容。例如，调用`QImage::bits()`会返回图像的深度副本，而非传递给构造器的缓冲区。这使得从原始数据高效构建QImage，而无需更改原始数据。

### `QImage::QImage(uchar *data, int width, int height, QImage::Format format, QImageCleanupFunction cleanupFunction = nullptr, void *cleanupInfo = nullptr)`

**作用与语义：**

构造给定`width` `height`和`format`，利用现有内存缓冲区 `data`。`width`和`height`必须以像素为单位，`data`必须32位对齐，且图像中每条扫描线数据也必须32位对齐。
缓冲区必须在整个QImage及其未被修改或分离的副本的整个生命周期内保持有效。图像在销毁时不会删除缓冲区。你可以提供函数指针`cleanupFunction`以及一个额外的指针`cleanupInfo`，当最后一份副本被销毁时调用。
如果`format`是索引色格式，图像颜色表最初是空的，必须通过`setColorCount()`或`setColorTable()`充分展开后才能使用图像。

### `QImage::QImage(const uchar *data, int width, int height, qsizetype bytesPerLine, QImage::Format format, QImageCleanupFunction cleanupFunction = nullptr, void *cleanupInfo = nullptr)`

**作用与语义：**

构造一个图像，使用给定的`width` `height`和`format`，使用现有的内存缓冲区 `data`。`width`和`height`必须以像素为单位表示。`bytesPerLine` 指定每行的字节数（步幅）。
缓冲区必须在整个QImage生命周期内保持有效，所有未被修改或以其他方式脱离原始缓冲区的副本。图像在缓冲区销毁时不会删除。你可以提供函数指针`cleanupFunction`以及一个额外的指针`cleanupInfo`，当最后一份副本被销毁时调用。
如果`format`是索引色格式，图像颜色表最初是空的，必须通过`setColorCount()`或`setColorTable()`展开足够多，才能使用图像。
与类似的QImage构造器使用非const数据缓冲区不同，该版本永远不会改变缓冲区的内容。例如，调用`QImage::bits()`返回的是图像的深度副本，而非传递给构造器的缓冲区。这使得从原始数据构建QImage变得高效，而无需更改原始数据。

### `QImage::QImage(uchar *data, int width, int height, qsizetype bytesPerLine, QImage::Format format, QImageCleanupFunction cleanupFunction = nullptr, void *cleanupInfo = nullptr)`

**作用与语义：**

构造给定`width` `height`和`format`的图像，使用现有的内存缓冲区 `data`。`width`和`height`必须以像素为单位表示。`bytesPerLine` 表示每行的字节数（步幅）。
缓冲区必须在整个QImage的生命周期内保持有效，所有未被修改或以其他方式分离的副本。图像在销毁时不会删除缓冲区。你可以提供函数指针`cleanupFunction`以及一个额外的指针`cleanupInfo`，当最后一个副本被销毁时调用。
如果`format`是索引色格式，图像颜色表最初是空的，必须通过`setColorCount()`或`setColorTable()`充分展开后才能使用图像。

### `QImage::QImage(const QImage &image)`

**作用与语义：**

构造给定`image`的浅层复制品。
有关浅层复制的更多信息，请参见隐式数据共享文档。

### `[noexcept] QImage::QImage(QImage &&other)`

**作用与语义：**

Move构造一个QImage实例，使其指向`other`指向的同一个对象。

### `[virtual noexcept] QImage::~QImage()`

**作用与语义：**

毁掉画面并清理。

### `bool QImage::allGray() const`

**作用与语义：**

如果图像中所有颜色都是灰色调（即它们的红、绿、蓝成分相等）则返回`true`;否则为假。
注意，对于没有颜色表的图像，这个功能会比较慢。

### `void QImage::applyColorTransform(const QColorTransform &transform)`

**作用与语义：**

对图像中的所有像素应用颜色变换`transform`。

### `[since 6.8] void QImage::applyColorTransform(const QColorTransform &transform, QImage::Format toFormat, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**作用与语义：**

对图像中的所有像素应用颜色变换`transform`，并将图像格式转换为`toFormat`。
指定的图像转换`flags`控制格式转换过程中图像数据的处理方式。

### `int QImage::bitPlaneCount() const`

**作用与语义：**

返回图像中的位面数。
位平面数是每个像素的颜色和透明度信息的位数。这与图像格式包含未使用位时的深度不同（即深度小于）。

### `uchar *QImage::bits()`

**作用与语义：**

返回指向第一个像素数据的指针。这等价于 `scanLine`（0）。
注意，`QImage`使用隐式数据共享。该函数对共享像素数据进行深度复制，确保该`QImage`是唯一使用当前返回值的。

### `const uchar *QImage::bits() const`

**作用与语义：**

注意`QImage`使用隐式数据共享，但该函数不会对共享像素数据进行深度复制，因为返回的数据是const的。

### `qsizetype QImage::bytesPerLine() const`

**作用与语义：**

返回每张图像扫描线的字节数。
如果 `height()` 非零，这等价于 `sizeInBytes()` / `height()`。

### `qint64 QImage::cacheKey() const`

**作用与语义：**

返回一个编号，用于识别该`QImage`对象的内容。不同的`QImage`对象只有在指向相同内容时才能拥有相同的密钥。
当图像被修改时，键也会改变。

### `QRgb QImage::color(int i) const`

**作用与语义：**

返回颜色表中索引`i`的颜色。第一个颜色位于索引0。
图像色彩表中的颜色被指定为 ARGB 四重态（`QRgb`）。使用`qAlpha()`、`qRed()`、`qGreen()` 和 `qBlue()` 函数来获取颜色值分量。

### `int QImage::colorCount() const`

**作用与语义：**

返回图像颜色表的大小。
注意colorCount()对于32-bpp图像返回0，因为这些图像不使用颜色表，而是将像素值编码为ARGB四重态。

### `QColorSpace QImage::colorSpace() const`

**作用与语义：**

如果定义了颜色空间，返回图像的色彩空间。

### `QList<QRgb> QImage::colorTable() const`

**作用与语义：**

返回图像颜色表中的颜色列表，若图像没有颜色表则返回空列表。

### `[since 6.4] QImage QImage::colorTransformed(const QColorTransform &transform) const &`

**作用与语义：**

返回图像中所有像素的颜色转换后`transform`。
注意：如果`transform`的源色彩空间与该图像格式不兼容，则返回空`QImage`。如果`transform`的目标色彩空间与该图像格式不兼容，图像也会被转换为兼容格式。关于目标像素格式选择的更多控制，请参见该方法的三参数重载。

### `[since 6.8] QImage QImage::colorTransformed(const QColorTransform &transform, QImage::Format toFormat, Qt::ImageConversionFlags flags = Qt::AutoColor) const &`

**作用与语义：**

返回图像中所有像素的颜色转换后，使用`transform`，返回格式为`toFormat`的图像。
指定的图像转换`flags`控制格式转换过程中图像数据的处理方式。
注意：如果`transform`的源色彩空间与该图像格式不兼容，或目标色彩空间与`toFormat`不兼容，则返回空`QImage`。

### `[since 6.4] QImage QImage::colorTransformed(const QColorTransform &transform) &&`

**作用与语义：**

返回图像中所有像素的`transform`变换后的颜色。

### `[since 6.8] QImage QImage::colorTransformed(const QColorTransform &transform, QImage::Format format, Qt::ImageConversionFlags flags = Qt::AutoColor) &&`

**作用与语义：**

返回图像中所有像素的`transform`变换后的颜色。

### `const uchar *QImage::constBits() const`

**作用与语义：**

返回指向第一个像素数据的指针。
注意`QImage`使用隐式数据共享，但该函数不会对共享像素数据进行深度复制，因为返回的数据是const的。

### `const uchar *QImage::constScanLine(int i) const`

**作用与语义：**

返回指向扫描线像素数据的指针，索引为`i`。第一条扫描线位于索引0。
扫描线数据最低为32位对齐。对于64位格式，它遵循64位整数的原生对齐（大多数平台为64位，但i386上显著为32位）。
注意`QImage`使用隐式数据共享，但该函数不会对共享像素数据进行深度复制，因为返回的数据是const。

### `void QImage::convertTo(QImage::Format format, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**作用与语义：**

将图像转换为原位`format`，必要时分离。
指定的图像转换`flags`控制图像数据在转换过程中的处理方式。

### `void QImage::convertToColorSpace(const QColorSpace &colorSpace)`

**作用与语义：**

将图片转换为`colorSpace`。
如果图像没有有效的色彩空间，方法就不做任何事。
注意：如果`colorSpace`与当前格式不兼容，图片将被转换为当前格式。

### `[since 6.8] void QImage::convertToColorSpace(const QColorSpace &colorSpace, QImage::Format format, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**作用与语义：**

将图像转换为`colorSpace`和`format`。
如果图像没有有效的色彩空间，方法无效;颜色空间与格式不兼容也无效。
指定的图像转换`flags`控制格式转换过程中图像数据的处理方式。

### `QImage QImage::convertToFormat(QImage::Format format, Qt::ImageConversionFlags flags = Qt::AutoColor) &&`

**作用与语义：**

返回给定`format`图像的副本。
指定的图像转换`flags`控制图像数据在转换过程中的处理方式。

### `QImage QImage::convertToFormat(QImage::Format format, const QList<QRgb> &colorTable, Qt::ImageConversionFlags flags = Qt::AutoColor) const`

**作用与语义：**

返回给定`format`图像的副本。
指定的图像转换`flags`控制图像数据在转换过程中的处理方式。

### `[since 6.0] QImage QImage::convertedTo(QImage::Format format, Qt::ImageConversionFlags flags = Qt::AutoColor) &&`

**作用与语义：**

返回给定`format`图像的副本。
指定的图像转换`flags`控制图像数据在转换过程中的处理方式。

### `QImage QImage::convertedToColorSpace(const QColorSpace &colorSpace) const`

**作用与语义：**

返回转换为`colorSpace`的图像。
如果图像没有有效的色彩空间，则返回空`QImage`。
注意：如果`colorSpace`与当前格式不兼容，返回的图像也会被转换为当前格式。如需更好地控制返回图像格式，请参见该方法的三参数重载。

### `[since 6.8] QImage QImage::convertedToColorSpace(const QColorSpace &colorSpace, QImage::Format format, Qt::ImageConversionFlags flags = Qt::AutoColor) &&`

**作用与语义：**

返回转换为`colorSpace`和`format`的图像。
如果图像没有有效的色彩空间，则返回空`QImage`。
指定的图像转换`flags`控制格式转换过程中图像数据的处理方式。

### `QImage QImage::copy(const QRect &rectangle = QRect()) const`

**作用与语义：**

返回图像的一个子区域作为新图像。
返回的图像是从图像中位置（`rectangle`.x()， `rectangle`.y()）复制而来，并且始终具有给定`rectangle`的大小。
在图像之外的区域，像素设置为0。对于32位RGB图像，这意味着黑色;对于32位ARGB图像，这意味着透明黑色;对于8位图像，这意味着颜色表中索引为0的颜色，可以是任意颜色;对于1位图像，这意味着`Qt::color0`。
如果给定`rectangle`是零矩形，则整个图像被复制。

### `QImage QImage::copy(int x, int y, int width, int height) const`

**作用与语义：**

返回的图像是从该图像中的位置（`x`，`y`）复制而来，并且始终保持给定的`width`和`height`。在图像之外的区域，像素设置为0。

### `QImage QImage::createAlphaMask(Qt::ImageConversionFlags flags = Qt::AutoColor) const`

**作用与语义：**

从该图像的 alpha 缓冲区构建并返回一个 1-bpp 的遮罩。如果图像格式为`QImage::Format_RGB32`，则返回空图像。
`flags`参数是`Qt::ImageConversionFlags`的逐位或，控制转换过程。为标志传递0则设置所有默认选项。
返回的图像具有小端位序（即图像格式为`QImage::Format_MonoLSB`），您可以使用`convertToFormat()`函数将其转换为大端序（`QImage::Format_Mono`）。

### `QImage QImage::createHeuristicMask(bool clipTight = true) const`

**作用与语义：**

为该图像创建并返回一个1-bpp的启发式遮罩。
该函数的工作原理是从一个角落选择颜色，然后从所有边缘开始削减该颜色的像素。四个角落投票决定要遮蔽哪种颜色。如果出现平纸（通常意味着该函数不适用于图像），结果是任意的。
返回的图像具有小端序（即图像格式为`QImage::Format_MonoLSB`），您可以使用`convertToFormat()`函数将其转换为大端序（`QImage::Format_Mono`）。
如果`clipTight`为真（默认），遮罩大小刚好能覆盖像素;否则，遮罩大于数据像素。
注意，该函数不考虑 alpha 缓冲区。

### `QImage QImage::createMaskFromColor(QRgb color, Qt::MaskMode mode = Qt::MaskInColor) const`

**作用与语义：**

根据给定的`color`值为该图像创建并返回遮罩。如果`mode`是MaskInColor（默认值），所有匹配`color`的像素都是遮罩中的不透明像素。如果`mode`是MaskOutColor，则所有匹配给定颜色的像素都是透明的。

### `int QImage::depth() const`

**作用与语义：**

返回图像的深度。
图像深度是用于存储单个像素的比特数，也称为每像素比特数（bpp）。
支撑深度为1、8、16、24、32和64。

### `[since 6.2] QSizeF QImage::deviceIndependentSize() const`

**作用与语义：**

返回图像的尺寸（单位为设备无关像素）。
在计算用户界面大小时应使用该值。
返回值等同于图像。`size()` / 图像。`devicePixelRatio()`。

### `qreal QImage::devicePixelRatio() const`

**作用与语义：**

返回图像的设备像素比。这是设备像素与设备无关像素之间的比值。
在根据图像尺寸计算布局几何时，请使用该函数：`QSize` layoutSize = 图像。`size()` / image.devicePixelRatio()。
默认值是1.0。

### `int QImage::dotsPerMeterX() const`

**作用与语义：**

返回物理测光表中水平可容纳的像素数。与`dotsPerMeterY()`一起，该数字定义了图像的预期比例和宽高比。

### `int QImage::dotsPerMeterY() const`

**作用与语义：**

返回物理测光表中垂直安装的像素数。与`dotsPerMeterX()`一起，该数字定义了图像的预期比例和宽高比。

### `void QImage::fill(uint pixelValue)`

**作用与语义：**

用给定的 `pixelValue` 填充整个图像。
如果图像深度为1，则只使用最低位。如果你说填充（0）、填充（2）等，图像填充0。如果说填充（1）、填充（3）等，图像填充1。如果深度为8，使用最低8位;如果深度为16，则使用最低16位。
如果图像深度高于32位，结果则未定义。
注意：没有对应的值获取器，但对于索引格式`QImage::pixelIndex()`返回相同的值，RGB32、ARGB32 和 ARGB32PM 格式则返回`QImage::pixel()`值。

### `void QImage::fill(Qt::GlobalColor color)`

**作用与语义：**

用给定的`color`填充图像，描述为标准全局颜色。

### `void QImage::fill(const QColor &color)`

**作用与语义：**

用给定的 `color` 填充整个图像。
如果图像深度为1，则当`color`等于`Qt::color1`时，图像将被填充为1;否则图像将被填充为0。
如果图像深度为8，图像将填充对应颜色表中`color`的索引（如存在）;否则填充为0。

### `[since 6.9] void QImage::flip(Qt::Orientations orient = Qt::Vertical)`

**作用与语义：**

根据`orient`不同情况，可以根据不同方向在水平和/或垂直方向翻转或镜像图像。

### `[since 6.9] QImage QImage::flipped(Qt::Orientations orient = Qt::Vertical) &&`

**作用与语义：**

返回图像的翻转或镜像版本，水平和/或垂直方向根据`orient`对应。
请注意，原始图像没有被更改。

### `QImage::Format QImage::format() const`

**作用与语义：**

返回图像格式。

### `[static, since 6.2] QImage QImage::fromData(QByteArrayView data, const char *format = nullptr)`

**作用与语义：**

从给定的`QByteArrayView` `data`构建图像。加载器尝试使用指定的`format`读取图像。如果未指定`format`（这是默认），加载器会探测数据的头部以猜测文件格式。
如果指定`format`，必须是`QImageReader::supportedImageFormats()`返回的某个值。
如果图像加载失败，返回的图像将是空图。

### `[static] QImage QImage::fromData(const QByteArray &data, const char *format = nullptr)`

**作用与语义：**

从给定的`QByteArray` `data`构造一个`QImage`。

### `[static] QImage QImage::fromData(const uchar *data, int size, const char *format = nullptr)`

**作用与语义：**

从给定二进制`data`的前`size`字节构造一个`QImage`。

### `[static, since 6.0] QImage QImage::fromHBITMAP(HBITMAP hbitmap)`

**作用与语义：**

返回一个等价于给定`hbitmap`的`QImage`。
HBITMAP 不存储关于 alpha 通道的信息。
在标准情况下，忽略Alpha通道，生成完全不透明的图像（通常格式为`QImage::Format_RGB32`）。
不过，在某些情况下，alpha通道会被用于应用图标或系统卡图标。在这种情况下，应在返回的图像上调用`reinterpretAsFormat(QImage::Format_ARGB32)`，以确保格式正确。

### `[static, since 6.0] QImage QImage::fromHICON(HICON icon)`

**作用与语义：**

返回的`QImage`等价于给定`icon`。

### `bool QImage::hasAlphaChannel() const`

**作用与语义：**

如果图像格式尊重alpha通道，返回`true`;否则返回`false`。

### `int QImage::height() const`

**作用与语义：**

返回图像高度。

### `void QImage::invertPixels(QImage::InvertMode mode = InvertRgb)`

**作用与语义：**

将图像中的所有像素值反转。
给定的反转仅在图像深度为32时`mode`有意义。默认`mode`为`InvertRgb`，保持alpha通道不变。如果`mode`为`InvertRgba`，alpha位也被反转。
反转8位图像意味着将所有颜色索引为i的像素替换为色指数为255减去i的像素。1位图像也是同样的情况。注意颜色表未被更改。
如果图像有预乘法的α通道，首先将图像转换为未预乘法的图像格式进行反转，然后再转换回去。

### `bool QImage::isGrayscale() const`

**作用与语义：**

对于32位图像，该函数等价于`allGray()`。
对于彩色索引图像，如果color（i）对颜色表的所有索引都是`QRgb`（i， i， i），该函数返回`true`;否则返回`false`。

### `bool QImage::isNull() const`

**作用与语义：**

如果是空图像，返回`true`，否则返回`false`。
空图中所有参数均为零且无分配数据。

### `bool QImage::load(const QString &fileName, const char *format = nullptr)`

**作用与语义：**

从带有指定`fileName`的文件中加载图像。如果图像成功加载，返回`true`;否则无效图像并返回`false`。
加载器尝试使用指定的`format`（如PNG或JPG）读取图像。如果未指定`format`（默认为默认），则根据文件后缀和头部自动检测。详情请参见 `QImageReader::setAutoDetectImageFormat()`。
文件名可以指磁盘上的实际文件，也可以指应用程序的嵌入式资源之一。有关如何将镜像和其他资源文件嵌入应用程序可执行文件的详细信息，请参见资源系统概述。

### `bool QImage::load(QIODevice *device, const char *format)`

**作用与语义：**

该函数读取给定`device`的 `QImage`。例如，这可以用来直接将图像加载到`QByteArray`中。

### `[since 6.2] bool QImage::loadFromData(QByteArrayView data, const char *format = nullptr)`

**作用与语义：**

从给定`QByteArrayView` `data`加载图像。如果图像成功加载，返回`true`;否则返回图像无效并返回`false`。
加载器尝试使用指定的`format`（如PNG或JPG）读取图像。如果未指定`format`（默认为默认），加载器会探测文件头部以猜测文件格式。

### `bool QImage::loadFromData(const QByteArray &data, const char *format = nullptr)`

**作用与语义：**

加载给定`QByteArray` `data`的图片。

### `bool QImage::loadFromData(const uchar *data, int len, const char *format = nullptr)`

**作用与语义：**

从给定二进制`data`的前`len`字节加载图像。

### `[since 6.0, until 6.13] void QImage::mirror(bool horizontal = false, bool vertical = true)`

**作用与语义：**

该函数计划在 6.13 版本中弃用。
改用 flip（`Qt::Orientations`） 代替。
图像在水平和/或垂直方向的镜像，取决于`horizontal`和`vertical`设置为真或假。

### `[until 6.13] QImage QImage::mirrored(bool horizontal = false, bool vertical = true) &&`

**作用与语义：**

该函数计划在 6.13 版本中弃用。
改用flipped（`Qt::Orientations`）代替。
返回图像的镜像，水平和/或垂直方向镜像，具体取决于`horizontal`和`vertical`设置为真或假。
请注意，原始图像没有被更改。

### `QPoint QImage::offset() const`

**作用与语义：**

返回相对于其他图像定位时，图像预期以的像素数偏移。

### `QRgb QImage::pixel(const QPoint &position) const`

**作用与语义：**

返回像素在给定`position`的颜色。
如果`position`无效，结果则未定义。
警告：当用于大规模像素操作时，该功能成本较高。当需要读取大量像素时，请使用`constBits()`或`constScanLine()`。

### `QRgb QImage::pixel(int x, int y) const`

**作用与语义：**

返回坐标（`x`，`y`）处像素的颜色。

### `QColor QImage::pixelColor(const QPoint &position) const`

**作用与语义：**

将给定`position`像素的颜色作为`QColor`返回。
如果`position`无效，则返回无效`QColor`。
警告：当用于大规模像素操作时，该功能成本较高。当需要读取大量像素时，请使用`constBits()`或`constScanLine()`。

### `QColor QImage::pixelColor(int x, int y) const`

**作用与语义：**

返回坐标（`x`、`y`）处像素的颜色，作为`QColor`。

### `[noexcept] QPixelFormat QImage::pixelFormat() const`

**作用与语义：**

`QImage::Format`作为`QPixelFormat`归还。

### `int QImage::pixelIndex(const QPoint &position) const`

**作用与语义：**

返回给定`position`的像素索引。
如果`position`不成立，或者图像不是调色板图像（`depth()` > 8），结果则未定义。

### `int QImage::pixelIndex(int x, int y) const`

**作用与语义：**

返回像素索引，位于（`x`， `y`）。

### `QRect QImage::rect() const`

**作用与语义：**

返回图像的包围矩形（0， 0， `width()`， `height()`）。

### `bool QImage::reinterpretAsFormat(QImage::Format format)`

**作用与语义：**

在不改变数据的情况下，将图像格式改为`format`。仅在相同深度的格式之间有效。
如果成功，退货`true`。
如果数据已知仅为不透明，该函数可用于将带有alpha通道的图像转换为对应的不透明格式，或者在覆盖新数据前更改给定图像缓冲区的格式。
警告：该函数不会检查图像数据在新格式下的有效性，如果深度兼容，仍会返回`true`。对数据无效的图像的操作未定义。
警告：如果图像未被分离，数据将被复制。

### `[since 6.0] void QImage::rgbSwap()`

**作用与语义：**

交换所有像素的红蓝分量值，有效地将RGB图像转换为BGR图像。

### `QImage QImage::rgbSwapped() &&`

**作用与语义：**

返回一个 `QImage`，其中所有像素的红蓝分量值都被交换了，实际上将 RGB 图像转换为 BGR 图像。
原始`QImage`未被更改。

### `bool QImage::save(const QString &fileName, const char *format = nullptr, int quality = -1) const`

**作用与语义：**

将图像保存到带有给定`fileName`的文件中，使用给定的图像文件`format`和`quality`因子。如果`format` `nullptr`，`QImage`会通过查看`fileName`的后缀尝试猜测格式。
`quality`因子必须在0到100或-1范围内。指定0以获取小型压缩文件，100用于获取大型未压缩文件，-1（默认）用于默认设置。
如果图像成功保存，返回`true`;否则返回`false`。

### `bool QImage::save(QIODevice *device, const char *format = nullptr, int quality = -1) const`

**作用与语义：**

该函数为给定`device`写入`QImage`。
例如，这可以用来直接将图像保存到`QByteArray`中：

**官方示例：**

```cpp
 QImage image;
 QByteArray ba;
 QBuffer buffer(&ba);
 buffer.open(QIODevice::WriteOnly);
 image.save(&buffer, "PNG"); // writes image into ba in PNG format
```

### `QImage QImage::scaled(const QSize &size, Qt::AspectRatioMode aspectRatioMode = Qt::IgnoreAspectRatio, Qt::TransformationMode transformMode = Qt::FastTransformation) const`

**作用与语义：**

返回图像的缩放到由给定`size`根据给定`aspectRatioMode`和`transformMode`定义的矩形。
- 如果`aspectRatioMode` `Qt::IgnoreAspectRatio`，图像被缩放为`size`。
- 如果`aspectRatioMode` `Qt::KeepAspectRatio`，图像会在`size`内尽可能放大为矩形，保持宽高比。
- 如果`aspectRatioMode` `Qt::KeepAspectRatioByExpanding`，图像在`size`外缩放到尽可能小的矩形，保持宽高比。
如果给定`size`为空，该函数返回空图。

### `QImage QImage::scaled(int width, int height, Qt::AspectRatioMode aspectRatioMode = Qt::IgnoreAspectRatio, Qt::TransformationMode transformMode = Qt::FastTransformation) const`

**作用与语义：**

返回一张缩放为矩形的图像副本，`width`和`height`根据给定的`aspectRatioMode`和`transformMode`。
如果`width`或`height`为零或负，该函数返回零图像。

### `QImage QImage::scaledToHeight(int height, Qt::TransformationMode mode = Qt::FastTransformation) const`

**作用与语义：**

返回图像的缩放副本。返回的图像通过指定的变换`mode`对应给定`height`进行缩放。
该函数自动计算图像宽度，以保持图像的比例。
如果给定的`height`为0或负，则返回一个空图。

### `QImage QImage::scaledToWidth(int width, Qt::TransformationMode mode = Qt::FastTransformation) const`

**作用与语义：**

返回图像的缩放副本。返回的图像通过指定的变换`mode`缩放到给定的`width`。
该函数会自动计算图像的高度，以确保其宽高比得以保持。
如果给定的`width`为0或负，则返回一个空图。

### `uchar *QImage::scanLine(int i)`

**作用与语义：**

返回指向扫描线像素数据的指针，索引为`i`。第一条扫描线位于索引0。
扫描线数据最低为32位对齐。对于64位格式，它遵循64位整数的原生对齐（大多数平台为64位，但i386上显著为32位）。
例如，去除图像中每个像素的绿色分量：
警告：如果您访问的是32位像素的图像数据，请将返回的指针投射到`QRgb*`（`QRgb`为32位大小），并用它来读写像素值。你不能直接使用`uchar*`指针，因为像素格式取决于底层平台的字节顺序。使用`qRed()`、`qGreen()`、`qBlue()`和`qAlpha()`来访问这些像素。

**官方示例：**

```cpp
 for (int y = 0; y < image.height(); ++y) {
     QRgb *line = reinterpret_cast<QRgb*>(image.scanLine(y));
     for (int x = 0; x < image.width(); ++x) {
         QRgb &rgb = line[x];
         rgb = qRgba(qRed(rgb), qGreen(0), qBlue(rgb), qAlpha(rgb));
     }
 }
```

### `const uchar *QImage::scanLine(int i) const`

**作用与语义：**

返回指向扫描线像素数据的指针，索引为`i`。第一条扫描线位于索引0。
扫描线数据最低为32位对齐。对于64位格式，它遵循64位整数的原生对齐（大多数平台为64位，但i386上显著为32位）。
例如，去除图像中每个像素的绿色分量：
警告：如果您访问的是32位像素的图像数据，请将返回的指针投射到`QRgb*`（`QRgb`为32位大小），并用它来读写像素值。你不能直接使用`uchar*`指针，因为像素格式取决于底层平台的字节顺序。使用`qRed()`、`qGreen()`、`qBlue()`和`qAlpha()`来访问这些像素。

**官方示例：**

```cpp
 for (int y = 0; y < image.height(); ++y) {
     QRgb *line = reinterpret_cast<QRgb*>(image.scanLine(y));
     for (int x = 0; x < image.width(); ++x) {
         QRgb &rgb = line[x];
         rgb = qRgba(qRed(rgb), qGreen(0), qBlue(rgb), qAlpha(rgb));
     }
 }
```

### `void QImage::setAlphaChannel(const QImage &alphaChannel)`

**作用与语义：**

将该图像的α通道设置为给定的`alphaChannel`。
如果`alphaChannel`是8位alpha图像，则直接使用alpha值。否则，`alphaChannel`转换为8位灰度，并使用像素值的强度。
如果图片已经有alpha通道，现有的alpha通道会与新的通道相乘。如果图片没有alpha通道，它会被转换成有通道的格式。
操作类似于用`QPainter::CompositionMode_DestinationIn`将`alphaChannel`绘制为该图像的α图像。

### `void QImage::setColor(int index, QRgb colorValue)`

**作用与语义：**

将颜色在颜色表中给定`index`的颜色设置为给定的`colorValue`。颜色值为ARGB四重态。
如果`index`不在当前颜色表的大小范围内，则会用`setColorCount()`展开。

### `void QImage::setColorCount(int colorCount)`

**作用与语义：**

调整颜色表大小以包含`colorCount`条。
如果颜色表展开，所有额外的颜色都会设置为透明（即`qRgba`（0， 0， 0， 0））。
使用图像时，颜色表必须足够大，以包含图像中所有像素/索引值的条目，否则结果未定义。

### `void QImage::setColorSpace(const QColorSpace &colorSpace)`

**作用与语义：**

将图像色彩空间设置为`colorSpace`，无需对图像数据进行任何转换。

### `void QImage::setColorTable(const QList<QRgb> &colors)`

**作用与语义：**

将用于将颜色索引转换为`QRgb`值的颜色表设置为指定的`colors`。
使用图像时，颜色表必须足够大，以包含图像中所有像素/索引值的条目，否则结果未定义。

### `void QImage::setDevicePixelRatio(qreal scaleFactor)`

**作用与语义：**

设置图像的设备像素比率。这是图像像素与设备无关像素之间的比例。
默认`scaleFactor`是1.0。设置成其他模式有两个效果：
在图像上打开的QPainter会被缩放。例如，如果在200x200的图像上绘画，且比例为2.0，则有效（与设备无关的）绘画边界为100x100。
基于图像尺寸计算布局几何的Qt代码路径会考虑该比例：`QSize` layoutSize = 图像。`size()` / 图像。`devicePixelRatio()` 这的净效果是图像显示为高DPI图像，而非大图像（参见绘制高分辨率像素地图和图像版本）。

### `void QImage::setDotsPerMeterX(int x)`

**作用与语义：**

设置物理计量表中水平可容纳的像素数为`x`。
与`dotsPerMeterY()`一起，这个数字定义了图像的预期比例和宽高比，并决定了`QPainter`在图像上绘制图形的比例。当图像在其他绘画设备上渲染时，它不会改变图像的比例或宽高比。

### `void QImage::setDotsPerMeterY(int y)`

**作用与语义：**

将物理计量表垂直安装的像素数设置为`y`。
与`dotsPerMeterX()`一起，这个数字定义了图像的预期比例和宽高比，并决定了`QPainter`在图像上绘制图形的比例。当图像在其他绘图设备上渲染时，它不会改变图像的比例或宽高比。

### `void QImage::setOffset(const QPoint &offset)`

**作用与语义：**

将图像相对于其他图像定位时预期偏移的像素数设置为`offset`。

### `void QImage::setPixel(const QPoint &position, uint index_or_rgb)`

**作用与语义：**

将给定`position`的像素索引或颜色设置为`index_or_rgb`。
如果图像格式是单色或调色板，给定的`index_or_rgb`值必须是图像色彩表中的索引，否则参数必须是`QRgb`值。
如果`position`在图像中不是有效的坐标对，或者在单色和调色板图像中`index_or_rgb` >= `colorCount()`，结果则未定义。
警告：由于调用内部调用的内部 `detach()` 函数，该函数成本较高;如果性能是问题，我们建议使用 `scanLine()` 或 `bits()` 直接访问像素数据。

### `void QImage::setPixel(int x, int y, uint index_or_rgb)`

**作用与语义：**

将像素索引或颜色在（`x`， `y`）设置为`index_or_rgb`。

### `void QImage::setPixelColor(const QPoint &position, const QColor &color)`

**作用与语义：**

将给定`position`的颜色设置为`color`。
如果`position`不是图像中的有效坐标对，或者图像格式是单色或调色板，结果则未定义。
警告：由于调用内部调用的 `detach()` 函数，该函数成本较高;如果性能是问题，建议使用 `scanLine()` 或 `bits()` 直接访问像素数据。

### `void QImage::setPixelColor(int x, int y, const QColor &color)`

**作用与语义：**

将像素颜色设置为（`x`， `y`）为`color`。

### `void QImage::setText(const QString &key, const QString &text)`

**作用与语义：**

将图像文本设置为给定的`text`，并将其与给定的`key`关联起来。
如果你只想存储单个文本块（即“评论”或仅仅是描述），你可以选择传递空密钥，或者使用通用密钥，比如“描述”。
当你调用`save()`或`QImageWriter::write()`时，图像文本会嵌入到图像数据中。
并非所有图片格式都支持嵌入文本。您可以通过使用`QImageWriter::supportsOption()`来了解某张图片或格式是否支持嵌入文本。我们举个例子：
你可以用`QImageWriter::supportedImageFormats()`来了解有哪些图片格式适合你。

**官方示例：**

```cpp
     QImageWriter writer;
     writer.setFormat("png");
     if (writer.supportsOption(QImageIOHandler::Description))
         qDebug() << "Png supports embedded text";
```

### `QSize QImage::size() const`

**作用与语义：**

返回图像大小，即其 `width()` 和 `height()`。

### `qsizetype QImage::sizeInBytes() const`

**作用与语义：**

返回图像数据大小（字节单位）。

### `[noexcept] void QImage::swap(QImage &other)`

**作用与语义：**

将该图像与`other`交换。这个操作非常快，而且从未失败过。

### `QString QImage::text(const QString &key = QString()) const`

**作用与语义：**

返回与给定 `key` 相关的图像文本。如果指定的`key`为空字符串，则返回整个图像文本，每个关键文本对之间用换行分隔。

### `QStringList QImage::textKeys() const`

**作用与语义：**

返回这张图片的文本键。
你可以用这些键和`text()`来列出某个键的图片文本。

### `CGImageRef QImage::toCGImage() const`

**作用与语义：**

创建与该`QImage`等价的 `CGImage`，并返回 `CGImageRef` 句柄。
返回的CGImageRef参与`QImage`隐式共享，并持有对`QImage`数据的引用。CGImage是不可变的，永远不会分离`QImage`。写入`QImage`时会像往常一样分离。
该功能速度快，且不复制或转换图像数据。
如果图像格式无法转换，则返回空CGImageRef。使用此功能的用户可以先将`QImage`转换为支持的格式，例如`Format_ARGB32_Premultiplied`。
如果图像没有设置色彩空间，CGImageRef 的色彩空间会设置为 sRGB 色彩空间。

### `[since 6.0] HBITMAP QImage::toHBITMAP() const`

**作用与语义：**

创造了`HBITMAP`相当于`QImage`的效果。
还原`HBITMAP`手柄。
使用后释放`HBITMAP`数据由调用者负责。
对于标准GDI调用，如`BitBlt()`，图像应采用格式`QImage::Format_RGB32`。
当将生成的HBITMAP用于`AlphaBlend()` GDI函数时，图像应具有格式`QImage::Format_ARGB32_Premultiplied`（使用`convertToFormat()`）。
当将生成的HBITMAP作为应用图标或系统托盘图标使用时，图像应具有格式`QImage::Format_ARGB32`。

### `[since 6.0] HICON QImage::toHICON(const QImage &mask = {}) const`

**作用与语义：**

`HICON` `QPixmap`的对应物，应用掩`mask`。
如果`mask`不是空，则格式必须为`QImage::Format_Mono`。返回`HICON`句柄。
调用者有责任在使用后释放 `HICON` 数据。

### `[static noexcept] QImage::Format QImage::toImageFormat(QPixelFormat format)`

**作用与语义：**

将`format`转变为`QImage::Format`。

### `[static noexcept] QPixelFormat QImage::toPixelFormat(QImage::Format format)`

**作用与语义：**

将`format`转换为`QPixelFormat`。

### `QImage QImage::transformed(const QTransform &matrix, Qt::TransformationMode mode = Qt::FastTransformation) const`

**作用与语义：**

返回使用给定变换`matrix`和变换`mode`进行变换的图像副本。
返回的图像通常与原始图像具有相同的{图像格式}{格式}。然而，复杂的变换可能导致图像中并非所有像素都被原图像的转换像素覆盖。在这种情况下，这些背景像素会被赋予透明颜色值，变换后的图像会获得带有alpha通道的格式，即使原始图像本身没有该通道。
变换`matrix`内部调整以补偿不需要的平移;即生成的图像是包含原始图像所有变换点的最小图像。使用`trueMatrix()`函数检索用于图像转换的实际矩阵。
与其他超载功能不同，该函数可用于对图像进行透视变换。

### `[static] QTransform QImage::trueMatrix(const QTransform &matrix, int width, int height)`

**作用与语义：**

返回用于变换图像的实际矩阵，其给定`width`、`height`和`matrix`。
在使用`transformed()`函数进行图像变换时，变换矩阵会在内部进行调整以补偿不需要的平移，即`transformed()`返回包含原始图像所有变换点的最小图像。该函数返回修改后的矩阵，将原始图像的点正确映射到新图像。
与其他超载功能不同，该函数创建可用于对图像进行透视变换的变换矩阵。

### `bool QImage::valid(const QPoint &pos) const`

**作用与语义：**

如果`pos`是图像中的有效坐标对，返回`true`;否则返回`false`。

### `bool QImage::valid(int x, int y) const`

**作用与语义：**

如果 `QPoint`（`x`， `y`） 是图像中的有效坐标对，返回 `true`;否则返回 `false`。

### `int QImage::width() const`

**作用与语义：**

返回图像宽度。

### `QImage::operator QVariant() const`

**作用与语义：**

返回图像为`QVariant`。

### `bool QImage::operator!=(const QImage &image) const`

**作用与语义：**

如果该图像与给定`image`内容不同，返回`true`;否则返回 `false`。
比较过程可能很慢，除非存在明显差异，比如宽度不同，这种情况下函数会很快返回。

### `[noexcept] QImage &QImage::operator=(QImage &&other)`

**作用与语义：**

Move-assign `other`到该`QImage`实例。

### `QImage &QImage::operator=(const QImage &image)`

**作用与语义：**

将给定`image`的浅层副本分配给该图像，并返回该图像的引用。
有关浅层复制的更多信息，请参见隐式数据共享文档。

### `bool QImage::operator==(const QImage &image) const`

**作用与语义：**

如果该图像与给定`image`内容相同，返回`true`;否则返回`false`。
比较过程可能较慢，除非存在明显差异（例如大小或格式不同），此时函数会很快返回。

### `QImageCleanupFunction`

**作用与语义：**

一个带有以下签名的函数，可用于实现基本的图像内存管理：

**官方示例：**

```cpp
 void myImageCleanupHandler(void *info);
```

### `QDataStream &operator<<(QDataStream &stream, const QImage &image)`

**作用与语义：**

将给定`image`写入给定`stream`，作为PNG图像，或如果流版本为1则写入BMP图像。注意，将流写入文件不会产生有效的图像文件。

### `QDataStream &operator>>(QDataStream &stream, QImage &image)`

**作用与语义：**

读取给定`stream`中的图像并存储在给定`image`中。

### `QImage convertToFormat(QImage::Format format, Qt::ImageConversionFlags flags = Qt::AutoColor) const &`

**作用与语义：**

返回转换为指定`format`的图像副本，使用指定的`colorTable`。
从RGB格式转换为索引格式是一个缓慢的过程，且采用简单的最近色彩方法，没有抖动。

### `(since 6.0) QImage convertedTo(QImage::Format format, Qt::ImageConversionFlags flags = Qt::AutoColor) const &`

**作用与语义：**

返回给定`format`图像的副本。
指定的图像转换`flags`控制图像数据在转换过程中的处理方式。

### `(since 6.8) QImage convertedToColorSpace(const QColorSpace &colorSpace, QImage::Format format, Qt::ImageConversionFlags flags = Qt::AutoColor) const &`

**作用与语义：**

返回转换为`colorSpace`和`format`的图像。
如果图像没有有效的色彩空间，则返回空`QImage`。
指定的图像转换`flags`控制格式转换过程中图像数据的处理方式。

### `(since 6.9) QImage flipped(Qt::Orientations orient = Qt::Vertical) const &`

**作用与语义：**

返回图像的翻转或镜像版本，水平和/或垂直方向根据`orient`对应。
请注意，原始图像没有被更改。

### `(until 6.13) QImage mirrored(bool horizontal = false, bool vertical = true) const &`

**作用与语义：**

该函数计划在 6.13 版本中弃用。
改用flipped（`Qt::Orientations`）代替。
返回图像的镜像，水平和/或垂直方向镜像，具体取决于`horizontal`和`vertical`设置为真或假。
请注意，原始图像没有被更改。

### `QImage rgbSwapped() const &`

**作用与语义：**

返回一个 `QImage`，其中所有像素的红蓝分量值都被交换了，实际上将 RGB 图像转换为 BGR 图像。
原始`QImage`未被更改。

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
