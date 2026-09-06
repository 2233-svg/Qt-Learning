# QImageWriter

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QImageWriter` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QImageWriter>`
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

- `enum ImageWriterError { DeviceError, UnsupportedFormatError, InvalidImageError, UnknownError }`

### 公有函数

- `QImageWriter()`
- `QImageWriter(QIODevice *device, const QByteArray &format)`
- `QImageWriter(const QString &fileName, const QByteArray &format = QByteArray())`
- `~QImageWriter()`
- `bool canWrite() const`
- `int compression() const`
- `QIODevice * device() const`
- `QImageWriter::ImageWriterError error() const`
- `QString errorString() const`
- `QString fileName() const`
- `QByteArray format() const`
- `bool optimizedWrite() const`
- `bool progressiveScanWrite() const`
- `int quality() const`
- `void setCompression(int compression)`
- `void setDevice(QIODevice *device)`
- `void setFileName(const QString &fileName)`
- `void setFormat(const QByteArray &format)`
- `void setOptimizedWrite(bool optimize)`
- `void setProgressiveScanWrite(bool progressive)`
- `void setQuality(int quality)`
- `void setSubType(const QByteArray &type)`
- `void setText(const QString &key, const QString &text)`
- `void setTransformation(QImageIOHandler::Transformations transform)`
- `QByteArray subType() const`
- `QList<QByteArray> supportedSubTypes() const`
- `bool supportsOption(QImageIOHandler::ImageOption option) const`
- `QImageIOHandler::Transformations transformation() const`
- `bool write(const QImage &image)`

### 静态公有成员

- `QList<QByteArray> imageFormatsForMimeType(const QByteArray &mimeType)`
- `QList<QByteArray> supportedImageFormats()`
- `QList<QByteArray> supportedMimeTypes()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QImageWriter::ImageWriterError`

**作用与语义：**

该枚举描述了在用`QImageWriter`写图像时可能出现的错误。
- `QImageWriter::DeviceError`：`1`;`QImageWriter`在写入图像数据时遇到设备错误。请查阅您的设备以了解问题所在。
- `QImageWriter::UnsupportedFormatError`：`2`;Qt 不支持所请求的图像格式。
- `QImageWriter::InvalidImageError`：`3`;尝试写入无效的`QImage`。无效图像的一个例子是空`QImage`。
- `QImageWriter::UnknownError`：`0`;发生了未知错误。如果调用`write()`后得到该值，很可能是由`QImageWriter`中的某个漏洞引起的。

### `QImageWriter::QImageWriter()`

**作用与语义：**

构造一个空的 QImageWriter 对象。在写入之前，你必须调用 `setFormat()` 设置图像格式，然后调用 `setDevice()` 或 `setFileName()`。

### `[explicit] QImageWriter::QImageWriter(QIODevice *device, const QByteArray &format)`

**作用与语义：**

利用设备`device`和图像格式`format`构建QImageWriter对象。

### `[explicit] QImageWriter::QImageWriter(const QString &fileName, const QByteArray &format = QByteArray())`

**作用与语义：**

构建一个 QImageWriter 对象，使用图像格式 `format` 写入名为 `fileName` 的文件。如果未提供`format`，QImageWriter 将通过检查 `fileName` 的扩展名来检测图像格式。

### `[noexcept] QImageWriter::~QImageWriter()`

**作用与语义：**

摧毁`QImageWriter`物体。

### `bool QImageWriter::canWrite() const`

**作用与语义：**

如果 `QImageWriter` 可以写入图像，即图像格式受支持且分配的设备已打开以供读取，则返回 `true`。

### `int QImageWriter::compression() const`

**作用与语义：**

返回图像的压缩。

### `QIODevice *QImageWriter::device() const`

**作用与语义：**

返回当前分配给`QImageWriter`的设备，若未分配设备则返回`nullptr`。

### `QImageWriter::ImageWriterError QImageWriter::error() const`

**作用与语义：**

返回最后一次发生的错误类型。

### `QString QImageWriter::errorString() const`

**作用与语义：**

返回对最后一次错误的人类可读描述。

### `QString QImageWriter::fileName() const`

**作用与语义：**

如果当前分配的设备是一个文件，或者`setFileName()`被调用过，该函数返回`QImageWriter`写入的文件名称。否则（即未分配设备或设备不是文件），返回空`QString`。

### `QByteArray QImageWriter::format() const`

**作用与语义：**

返回`QImageWriter`用于写图片的格式。

### `[static] QList<QByteArray> QImageWriter::imageFormatsForMimeType(const QByteArray &mimeType)`

**作用与语义：**

返回对应`mimeType`的图像格式列表。
注意，调用该函数前必须创建`QGuiApplication`实例。

### `bool QImageWriter::optimizedWrite() const`

**作用与语义：**

返回是否开启了写入图像的优化。

### `bool QImageWriter::progressiveScanWrite() const`

**作用与语义：**

返回图像是否应以逐行图像形式书写。

### `int QImageWriter::quality() const`

**作用与语义：**

返回图像格式的画质设置。

### `void QImageWriter::setCompression(int compression)`

**作用与语义：**

这是一个针对图像格式的特定函数，用于设置图像的压缩。对于不支持设置压缩的图像格式，该值被忽略。
`compression`的值范围取决于图像格式。例如，“tiff”格式支持两个值，0（无压缩）和1（LZW压缩）。

### `void QImageWriter::setDevice(QIODevice *device)`

**作用与语义：**

将`QImageWriter`的设备设置为`device`。如果设备已被设置，旧设备会从`QImageWriter`中移除，其他设置保持不变。
如果设备尚未打开，`QImageWriter`会通过调用open()尝试以`QIODeviceBase::WriteOnly`模式打开设备。注意，这对某些设备不适用，如`QProcess`、`QTcpSocket`和`QUdpSocket`，因为需要更多逻辑才能打开设备。

### `void QImageWriter::setFileName(const QString &fileName)`

**作用与语义：**

将`QImageWriter`的文件名设置为`fileName`。内部，`QImageWriter`会创建一个`QFile`并以`QIODevice::WriteOnly`模式打开，写入图像时使用该文件。

### `void QImageWriter::setFormat(const QByteArray &format)`

**作用与语义：**

将`QImageWriter`在写入图片时使用的格式设置为`format`。`format` 是一个不区分大小写的文本字符串。示例：
你可以致电`supportedImageFormats()`获取完整的格式`QImageWriter`支持列表。

**官方示例：**

```cpp
 QImageWriter writer;
 writer.setFormat("png"); // same as writer.setFormat("PNG");
```

### `void QImageWriter::setOptimizedWrite(bool optimize)`

**作用与语义：**

这是一个针对图像格式的专用函数，用于在写入图像时设置`optimize`标志。对于不支持设置`optimize`标志的图像格式，该值被忽略。
默认是假的。

### `void QImageWriter::setProgressiveScanWrite(bool progressive)`

**作用与语义：**

这是一个针对图像格式的专用功能，在写入图像时启用`progressive`扫描。对于不支持设置`progressive`扫描标志的图像格式，该值被忽略。
默认是假的。

### `void QImageWriter::setQuality(int quality)`

**作用与语义：**

将图像格式的画质设置设置为`quality`。
某些图像格式，尤其是有损格式，涉及在a）图像的视觉质量和b）编码执行时间及压缩水平之间进行权衡。该函数为支持该格式的图像格式设定了该权衡水平。对于其他格式，这一值被忽略。
`quality`的数值范围取决于图像格式。例如，“jpeg”格式支持从0（低视觉质量，高压缩率）到100（高视觉质量，低压缩）的质量范围。

### `void QImageWriter::setSubType(const QByteArray &type)`

**作用与语义：**

这是一个针对图像格式的函数，将图像的子类型设置为`type`。子类型可以被处理程序用来决定保存图像时应采用哪种格式。
例如，将图像保存为DDS格式，子类型A8R8G8R8：

**官方示例：**

```cpp
 QImageWriter writer("some/image.dds");
 if (writer.supportsOption(QImageIOHandler::SubType))
     writer.setSubType("A8R8G8B8");
 writer.write(image);
```

### `void QImageWriter::setText(const QString &key, const QString &text)`

**作用与语义：**

将与关键图关联的图像文本设置为`key`为`text`。这对于存储版权信息或其他关于图片的信息非常有用。示例：
如果你想存储单个数据块（例如注释），可以传递空键，或者使用通用键，比如“描述”。
调用`write()`后，密钥和文本会嵌入到图像数据中。
该选项的支持通过`QImageIOHandler::Description`实现。

**官方示例：**

```cpp
 QImage image("some/image.jpeg");
 QImageWriter writer("images/outimage.png", "png");
 writer.setText("Author", "John Smith");
 writer.write(image);
```

### `void QImageWriter::setTransformation(QImageIOHandler::Transformations transform)`

**作用与语义：**

设置图像变换的元数据，包括`transform`的方向。
如果图像格式不支持变换元数据，则在写入前应用变换。

### `QByteArray QImageWriter::subType() const`

**作用与语义：**

返回图像的子类型。

### `[static] QList<QByteArray> QImageWriter::supportedImageFormats()`

**作用与语义：**

返回`QImageWriter`支持的图像格式列表。
默认情况下，Qt 可以编写以下格式：
- `Format`：哑剧类型;描述
- `BMP`：image/bmp;Windows 位图
- `JPG`：图像/jpeg;联合摄影专家组
- `PNG`：image/png;便携式网络图形
- `PBM`：image/x-可移植位图;便携位图
- `PGM`：image/x-可移植灰图;便携灰图
- `PPM`：image/x-便携像素地图;便携像素地图
- `XBM`：image/x-xbitmap;X11 位图
- `XPM`：image/x-xpixmap;X11 像素映射
通过 Qt SVG 模块支持读写 SVG 文件。Qt 图像格式模块支持其他图像格式。
注意，调用该函数前必须创建 `QApplication` 实例。

### `[static] QList<QByteArray> QImageWriter::supportedMimeTypes()`

**作用与语义：**

返回`QImageWriter`支持的MIME类型列表。
注意，调用该函数前必须创建 `QApplication` 实例。

### `QList<QByteArray> QImageWriter::supportedSubTypes() const`

**作用与语义：**

返回图像支持的子类型列表。

### `bool QImageWriter::supportsOption(QImageIOHandler::ImageOption option) const`

**作用与语义：**

如果写者支持`option`，则返回`true`;否则返回 false。
不同的图片格式支持不同的选项。调用该函数来判断当前格式是否支持某个选项。例如，PNG格式允许您将文本嵌入图片的元数据中（参见文本（text））。
选项可以在作者与某种格式关联后进行测试。

**官方示例：**

```cpp
 QImageWriter writer(fileName);
 if (writer.supportsOption(QImageIOHandler::Description))
     writer.setText("Author", "John Smith");
```

### `QImageIOHandler::Transformations QImageWriter::transformation() const`

**作用与语义：**

返回图像被设定为写入的变换和方向。

### `bool QImageWriter::write(const QImage &image)`

**作用与语义：**

将映像`image`写入指定的设备或文件名。成功时返回`true`;否则返回`false`。如果操作失败，你可以调用`error()`查找发生的错误类型，或`errorString()`获取人力可读的错误描述。

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

`QImageWriter` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
