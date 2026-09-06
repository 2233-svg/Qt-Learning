# QImageReader

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QImageReader` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QImageReader>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum ImageReaderError { FileNotFoundError, DeviceError, UnsupportedFormatError, InvalidDataError, UnknownError }`

### 公有函数

- `QImageReader()`
- `QImageReader(QIODevice *device, const QByteArray &format = QByteArray())`
- `QImageReader(const QString &fileName, const QByteArray &format = QByteArray())`
- `~QImageReader()`
- `bool autoDetectImageFormat() const`
- `bool autoTransform() const`
- `QColor backgroundColor() const`
- `bool canRead() const`
- `QRect clipRect() const`
- `int currentImageNumber() const`
- `QRect currentImageRect() const`
- `bool decideFormatFromContent() const`
- `QIODevice * device() const`
- `QImageReader::ImageReaderError error() const`
- `QString errorString() const`
- `QString fileName() const`
- `QByteArray format() const`
- `int imageCount() const`
- `QImage::Format imageFormat() const`
- `bool jumpToImage(int imageNumber)`
- `bool jumpToNextImage()`
- `int loopCount() const`
- `int nextImageDelay() const`
- `int quality() const`
- `QImage read()`
- `bool read(QImage *image)`
- `QRect scaledClipRect() const`
- `QSize scaledSize() const`
- `void setAutoDetectImageFormat(bool enabled)`
- `void setAutoTransform(bool enabled)`
- `void setBackgroundColor(const QColor &color)`
- `void setClipRect(const QRect &rect)`
- `void setDecideFormatFromContent(bool ignored)`
- `void setDevice(QIODevice *device)`
- `void setFileName(const QString &fileName)`
- `void setFormat(const QByteArray &format)`
- `void setQuality(int quality)`
- `void setScaledClipRect(const QRect &rect)`
- `void setScaledSize(const QSize &size)`
- `QSize size() const`
- `QByteArray subType() const`
- `QList<QByteArray> supportedSubTypes() const`
- `bool supportsAnimation() const`
- `bool supportsOption(QImageIOHandler::ImageOption option) const`
- `QString text(const QString &key) const`
- `QStringList textKeys() const`
- `QImageIOHandler::Transformations transformation() const`

### 静态公有成员

- `(since 6.0) int allocationLimit()`
- `QByteArray imageFormat(QIODevice *device)`
- `QByteArray imageFormat(const QString &fileName)`
- `QList<QByteArray> imageFormatsForMimeType(const QByteArray &mimeType)`
- `(since 6.0) void setAllocationLimit(int mbLimit)`
- `QList<QByteArray> supportedImageFormats()`
- `QList<QByteArray> supportedMimeTypes()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QImageReader::ImageReaderError`

**作用与语义：**

本枚举描述了在读取带有`QImageReader`图像时可能出现的不同类型的错误。
- `QImageReader::FileNotFoundError`：`1`;`QImageReader` 与一个文件名一起使用，但没有找到该名称的文件。如果文件名没有扩展名，且正确扩展名的文件不被 Qt 支持，也会发生这种情况。
- `QImageReader::DeviceError`：`2`;`QImageReader`读取图像时遇到设备错误。你可以查阅你所在的设备，了解更多问题所在。
- `QImageReader::UnsupportedFormatError`：`3`;Qt 不支持所请求的图像格式。
- `QImageReader::InvalidDataError`：`4`;图像数据无效，`QImageReader`无法读取图像。如果图像文件损坏，就会发生这种情况。
- `QImageReader::UnknownError`：`0`;发生了未知错误。如果调用`read()`后得到该值，很可能是由`QImageReader`中的某个漏洞引起的。

### `QImageReader::QImageReader()`

**作用与语义：**

构造一个空的 QImageReader 对象。在读取图像前，调用 `setDevice()` 或 `setFileName()`。

### `[explicit] QImageReader::QImageReader(QIODevice *device, const QByteArray &format = QByteArray())`

**作用与语义：**

构建一个带有设备`device`和图像格式`format`的QImageReader对象。

### `[explicit] QImageReader::QImageReader(const QString &fileName, const QByteArray &format = QByteArray())`

**作用与语义：**

构建一个QImageReader对象，文件名为`fileName`，图像格式为`format`。

### `[noexcept] QImageReader::~QImageReader()`

**作用与语义：**

摧毁`QImageReader`物体。

### `[static, since 6.0] int QImageReader::allocationLimit()`

**作用与语义：**

返回当前的分配限制，单位为兆字节。

### `bool QImageReader::autoDetectImageFormat() const`

**作用与语义：**

如果该图像读取器启用了图像格式自动检测，返回`true`;否则返回`false`。默认情况下，自动检测是启用的。

### `bool QImageReader::autoTransform() const`

**作用与语义：**

返回`true`图像处理程序是否会对`read()`应用变换元数据。

### `QColor QImageReader::backgroundColor() const`

**作用与语义：**

返回读取图像时使用的背景色。如果图像格式不支持设置背景色，则返回无效颜色。

### `bool QImageReader::canRead() const`

**作用与语义：**

如果可以读取设备图像（即支持图像格式且设备似乎包含有效数据），返回`true`;否则返回`false`。
canRead() 是一个轻量级函数，仅做快速测试以确认图像数据是否有效。如果图像数据损坏，canRead() 返回 `true` 后，`read()` 仍可能返回 false。
注意：`QMimeDatabase`查询通常比该函数更适合识别潜在非图像文件或数据。
对于支持动画的图像，canRead() 在所有帧都被读取后返回`false`。

### `QRect QImageReader::clipRect() const`

**作用与语义：**

返回图像的裁剪矩形图（也称为ROI，或兴趣区域）。如果未设置剪辑矩形，则返回无效`QRect`。

### `int QImageReader::currentImageNumber() const`

**作用与语义：**

对于支持动画的图像格式，该函数返回当前帧的序列号。如果图像格式不支持动画，则返回0。
如果发生错误，该函数返回 -1。

### `QRect QImageReader::currentImageRect() const`

**作用与语义：**

对于支持动画的图像格式，该函数返回当前帧的rect。否则返回空rect。

### `bool QImageReader::decideFormatFromContent() const`

**作用与语义：**

返回图像阅读器是否应仅根据数据流内容而非文件扩展名决定使用哪个插件。

### `QIODevice *QImageReader::device() const`

**作用与语义：**

返回当前分配给`QImageReader`的设备，若未分配设备则返回`nullptr`。

### `QImageReader::ImageReaderError QImageReader::error() const`

**作用与语义：**

返回上次发生的错误类型。

### `QString QImageReader::errorString() const`

**作用与语义：**

返回对最后一次错误的人类可读描述。

### `QString QImageReader::fileName() const`

**作用与语义：**

如果当前分配的设备是`QFile`，或者`setFileName()`已被调用，该函数返回`QImageReader`读取的文件名称。否则（即未分配设备或设备非`QFile`），返回空的`QString`。

### `QByteArray QImageReader::format() const`

**作用与语义：**

返回`QImageReader`用于阅读图像的格式。
你可以在将设备分配给读取器后调用该函数，以确定设备的格式。例如：
如果读取器无法读取设备中的任何图像（例如，设备中没有图像，或者该图像已被读取），或者该格式不被支持，该函数返回一个空的 QByteArray()。

**官方示例：**

```cpp
 QImageReader reader("image.png");
 // reader.format() == "png"
```

### `int QImageReader::imageCount() const`

**作用与语义：**

对于支持动画的图像格式，该函数返回动画中的总图像数。如果格式不支持动画，则返回 0。
如果发生错误，该函数返回 -1。

### `QImage::Format QImageReader::imageFormat() const`

**作用与语义：**

返回图像格式，但未实际读取图像内容。格式描述`QImageReader::read()`返回的图像格式，而非实际图像的格式。
如果图片格式不支持此功能，该函数将返回无效格式。

### `[static] QByteArray QImageReader::imageFormat(QIODevice *device)`

**作用与语义：**

如果支持，该函数返回设备的图像格式`device`。否则返回空字符串。

### `[static] QByteArray QImageReader::imageFormat(const QString &fileName)`

**作用与语义：**

如果支持，该函数返回文件的图像格式`fileName`。否则返回空字符串。

### `[static] QList<QByteArray> QImageReader::imageFormatsForMimeType(const QByteArray &mimeType)`

**作用与语义：**

返回对应`mimeType`的图像格式列表。
注意，调用该函数前必须创建`QGuiApplication`实例。

### `bool QImageReader::jumpToImage(int imageNumber)`

**作用与语义：**

对于支持动画的图像格式，该函数会跳转到序列号为`imageNumber`的图像，成功时返回真，找不到对应图像时返回假。
下一次调用`read()`将尝试阅读这张图片。

### `bool QImageReader::jumpToNextImage()`

**作用与语义：**

对于支持动画的图像格式，该函数会跳过当前图像，成功时返回true，动画中没有后续图像时返回false。
默认实现调用`read()`，然后丢弃生成的图像，但图像处理程序可能有更高效的实现方式。

### `int QImageReader::loopCount() const`

**作用与语义：**

对于支持动画的图像格式，该函数返回动画应循环的次数。如果该函数返回 -1，则可能表示动画应永远循环，或表示发生错误。如果发生错误，`canRead()` 返回 false。

### `int QImageReader::nextImageDelay() const`

**作用与语义：**

对于支持动画的图像格式，该函数返回等待动画下一帧的毫秒数。如果图像格式不支持动画，则返回0。
如果发生错误，该函数返回 -1。

### `int QImageReader::quality() const`

**作用与语义：**

返回图像格式的画质设置。

### `QImage QImageReader::read()`

**作用与语义：**

读取设备中的图像。成功后返回读取的图像;否则返回空`QImage`。你可以调用`error()`查找发生的错误类型，或用`errorString()`获取人类可读的错误描述。
对于支持动画的图像格式，反复调用read()会返回下一帧。当所有帧都被读取后，返回一个空图像。

### `bool QImageReader::read(QImage *image)`

**作用与语义：**

将设备中的图像读取到`image`，该图像必须指向`QImage`。成功时返回`true`;否则返回`false`。
如果`image`与即将读取的图像数据格式和大小相同，该函数可能不需要在读取前分配新图像。因此，它可能比另一个读取()重载更快，后者总是构建新图像;尤其是在读取多个格式和大小相同图像时。
对于支持动画的图像格式，反复调用read()会返回下一帧。当所有帧都被读取后，返回一个空图像。

**官方示例：**

```cpp
 QImage icon(64, 64, QImage::Format_RGB32);
 QImageReader reader("icon_64x64.bmp");
 if (reader.read(&icon)) {
     // Display icon
 }
```

### `QRect QImageReader::scaledClipRect() const`

**作用与语义：**

返回缩放后的图像剪辑矩形。

### `QSize QImageReader::scaledSize() const`

**作用与语义：**

返回图像的缩放尺寸。

### `[static, since 6.0] void QImageReader::setAllocationLimit(int mbLimit)`

**作用与语义：**

将分配限制设置为`mbLimit`兆字节。需要超过该限制的内存分配`QImage`的图像将被拒绝。如果`mbLimit`为0，分配大小检查将被禁用。
该限制有助于应用程序避免加载损坏图像文件时意外占用大量内存。通常不需要更改该限制。默认限制足够大，适用于所有常用图像大小。
运行时，该值可能会被环境变量 `QT_IMAGEIO_MAXALLOC` 覆盖。
注意：内存需求计算时每个像素至少为32位，因为Qt在图形界面中通常会将图像转换为该深度。这意味着有效分配限制明显小于读取1 bpp和8 bpp图像时的`mbLimit`。

### `void QImageReader::setAutoDetectImageFormat(bool enabled)`

**作用与语义：**

如果`enabled`为真，则启用图像格式自动检测;否则，自动检测被禁用。默认情况下，自动检测是启用的。
`QImageReader` 采用了广泛的方法来检测图像格式;首先，如果你把文件名传给 `QImageReader`，它会尝试检测该文件名是否指向已有文件，方法是在给定文件名后添加一个支持的默认扩展名。然后它采用以下方法检测图像格式：
- 图像插件首先被查询，基于可选格式字符串或文件名后缀（如果源设备是文件）。此阶段不进行内容检测。`QImageReader`会选择支持读取该格式的第一个插件。
- 如果没有插件支持该图像格式，Qt 内置的处理程序会根据可选格式字符串或文件名后缀进行检查。
- 如果找不到具备功能支持的插件或内置处理程序，则通过检查数据流内容来测试每个插件。
- 如果没有插件能基于数据内容检测图像格式，则通过检查内容测试每个内置图像处理程序。
- 最后，如果上述所有方法都失败，`QImageReader`在尝试读取图像时会报告失败。
通过关闭图像格式自动检测，`QImageReader`只会根据格式字符串查询插件和内置处理器（即不测试文件扩展名）。

### `void QImageReader::setAutoTransform(bool enabled)`

**作用与语义：**

确定`read()`返回的图像如果`true`，应自动应用变换元数据`enabled`。

### `void QImageReader::setBackgroundColor(const QColor &color)`

**作用与语义：**

将背景颜色设置为`color`。支持此操作的图像格式通常会先初始化背景为`color`再读取图像。

### `void QImageReader::setClipRect(const QRect &rect)`

**作用与语义：**

将图像剪辑矩阵（也称为ROI，或兴趣区域）设置为`rect`。`rect`的坐标相对于未变换的图像尺寸，`size()`返回。

### `void QImageReader::setDecideFormatFromContent(bool ignored)`

**作用与语义：**

如果`ignored`设置为true，图像读取器会忽略指定的格式或文件扩展名，仅根据数据流内容决定使用哪个插件。
设置这个标志意味着所有图片插件都会被加载。每个插件会读取图像数据中的前几个字节，并决定插件是否兼容。
这也会禁用自动检测图像格式的功能。

### `void QImageReader::setDevice(QIODevice *device)`

**作用与语义：**

将`QImageReader`的设备设置为`device`。如果设备已被设置，旧设备会从`QImageReader`中移除，其他设置保持不变。
如果设备尚未打开，`QImageReader`会通过调用open()尝试以`ReadOnly`模式打开设备。注意，这对某些设备（如`QProcess`、`QTcpSocket`和`QUdpSocket`）不适用，因为需要更多逻辑才能打开设备。

### `void QImageReader::setFileName(const QString &fileName)`

**作用与语义：**

将`QImageReader`的文件名设置为`fileName`。内部，`QImageReader`会创建一个`QFile`对象并以`ReadOnly`模式打开，读取图像时使用该格式。
如果`fileName`不包含文件扩展名（例如.png或.bmp），`QImageReader`会循环使用所有支持的扩展名，直到找到匹配的文件。

### `void QImageReader::setFormat(const QByteArray &format)`

**作用与语义：**

将`QImageReader`阅读图像时使用的格式设置为`format`。`format` 是一个不区分大小写的文本字符串。示例：
你可以致电`supportedImageFormats()`获取完整的格式`QImageReader`支持列表。

**官方示例：**

```cpp
 QImageReader reader;
 reader.setFormat("png"); // same as reader.setFormat("PNG");
```

### `void QImageReader::setQuality(int quality)`

**作用与语义：**

将图像格式的画质设置设置为`quality`。
某些图像格式，尤其是有损格式，涉及在a）图像的视觉质量和b）解码执行时间之间做出权衡。该函数为支持该格式的图像格式设定了这种权衡水平。
在缩放图像读取中，质量设置也可能影响缩放算法视觉质量与执行速度之间的权衡水平。
`quality`的值范围取决于图像格式。例如，“jpeg”格式支持从0（低视觉质量）到100（高视觉质量）的质量范围。

### `void QImageReader::setScaledClipRect(const QRect &rect)`

**作用与语义：**

将缩放后的剪辑rect设为`rect`。缩放后的剪辑rect是图像缩放后应用的剪辑rect（也称为ROI，或兴趣区域）。

### `void QImageReader::setScaledSize(const QSize &size)`

**作用与语义：**

将图像的缩放尺寸设置为`size`。缩放在初始剪辑rect之后，但在应用缩放后的剪辑rect之前进行。缩放算法取决于图像格式。默认情况下（即如果图像格式不支持缩放），`QImageReader`将使用 QImage：：scale() 和 Qt：：SmoothScaling。
如果`size`中只设置一个维度，另一个维度将根据图像的自然尺寸计算，以保持宽高比。

### `QSize QImageReader::size() const`

**作用与语义：**

返回图像大小，但不实际读取图像内容。
如果图像格式不支持此功能，该函数会返回无效的大小。Qt 内置的图像处理程序都支持此功能，但不需要自定义图像格式插件来实现此功能。

### `QByteArray QImageReader::subType() const`

**作用与语义：**

返回图像的子类型。

### `[static] QList<QByteArray> QImageReader::supportedImageFormats()`

**作用与语义：**

返回`QImageReader`支持的图像格式列表。
默认情况下，Qt 可以读取以下格式：
- `Format`：哑剧类型;描述
- `BMP`：image/bmp;Windows 位图
- `GIF`：图片/动图;图形交换格式（可选）
- `JPG`：图像/jpeg;联合摄影专家组
- `PNG`：image/png;便携式网络图形
- `PBM`：image/x-可移动位图;便携位图
- `PGM`：image/x-portable-graymap;便携式灰图
- `PPM`：image/x-portable-pixmap;便携式Pixmap（便携式像素图）
- `XBM`：image/x-xbitmap;X11 位图
- `XPM`：image/x-xpixmap;X11 像素映射
- `SVG`：图像/SVG xml;可缩放矢量图形
通过 Qt SVG 模块支持读写 SVG 文件。Qt 图像格式模块支持其他图像格式。
注意，调用该函数之前必须创建`QCoreApplication`实例。

### `[static] QList<QByteArray> QImageReader::supportedMimeTypes()`

**作用与语义：**

返回`QImageReader`支持的MIME类型列表。
注意，调用该函数之前必须创建 `QApplication` 实例。

### `QList<QByteArray> QImageReader::supportedSubTypes() const`

**作用与语义：**

返回图像支持的子类型列表。

### `bool QImageReader::supportsAnimation() const`

**作用与语义：**

如果图像格式支持动画，返回`true`;否则返回 false。

### `bool QImageReader::supportsOption(QImageIOHandler::ImageOption option) const`

**作用与语义：**

如果读取器支持`option`，则返回`true`;否则返回假。
不同的图片格式支持不同的选项。调用该函数来判断当前格式是否支持某个选项。例如，PNG 格式允许您将文本嵌入图像的元数据（参见 `text()`），而 BMP 格式允许您在不将整张图片加载到内存的情况下确定图片大小（参见 `size()`）。

**官方示例：**

```cpp
 QImageReader reader(":/image.png");
 if (reader.supportsOption(QImageIOHandler::Size))
     qDebug() << "Size:" << reader.size();
```

### `QString QImageReader::text(const QString &key) const`

**作用与语义：**

返回与`key`关联的图片文本。
该选项的支持通过`QImageIOHandler::Description`实现。

### `QStringList QImageReader::textKeys() const`

**作用与语义：**

返回该图片的文本键。你可以用这些键和`text()`列出某个键的图片文本。
该选项的支持通过`QImageIOHandler::Description`实现。

### `QImageIOHandler::Transformations QImageReader::transformation() const`

**作用与语义：**

返回图像的转换元数据，包括图像方向。如果格式不支持转换元数据，则返回`QImageIOHandler::TransformationNone`。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QImageReader` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
