# QImageIOHandler

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QImageIOHandler` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QImageIOHandler>`
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

- `enum ImageOption { Size, ClipRect, ScaledSize, ScaledClipRect, Description, …, ImageTransformation }`
- `enum Transformation { TransformationNone, TransformationMirror, TransformationFlip, TransformationRotate180, TransformationRotate90, …, TransformationRotate270 }`
- `flags Transformations`

### 公有函数

- `QImageIOHandler()`
- `virtual ~QImageIOHandler()`
- `virtual bool canRead() const = 0`
- `virtual int currentImageNumber() const`
- `virtual QRect currentImageRect() const`
- `QIODevice * device() const`
- `QByteArray format() const`
- `virtual int imageCount() const`
- `virtual bool jumpToImage(int imageNumber)`
- `virtual bool jumpToNextImage()`
- `virtual int loopCount() const`
- `virtual int nextImageDelay() const`
- `virtual QVariant option(QImageIOHandler::ImageOption option) const`
- `virtual bool read(QImage *image) = 0`
- `void setDevice(QIODevice *device)`
- `void setFormat(const QByteArray &format)`
- `void setFormat(const QByteArray &format) const`
- `virtual void setOption(QImageIOHandler::ImageOption option, const QVariant &value)`
- `virtual bool supportsOption(QImageIOHandler::ImageOption option) const`
- `virtual bool write(const QImage &image)`

### 静态公有成员

- `(since 6.0) bool allocateImage(QSize size, QImage::Format format, QImage *image)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QImageIOHandler::ImageOption`

**作用与语义：**

这个枚举描述了 `QImageIOHandler` 支持的不同选项。一些选项用于查询图像属性，其他选项用于切换图像的写入方式。
- `QImageIOHandler::Size`: `0`; 图像的原始尺寸。支持此选项的处理程序应从图像元数据中读取图像大小，并将此尺寸作为 `QSize` 从 `option()` 返回。
- `QImageIOHandler::ClipRect`: `1`; 裁剪矩形或感兴趣区域（ROI）。支持此选项的处理程序应仅从原始图像的 `read()` 中读取提供的 `QRect` 区域，然后应用其他任何转换。
- `QImageIOHandler::ScaledSize`: `4`; 图像的缩放尺寸。支持此选项的处理程序应在应用任何裁剪矩形转换（ClipRect）后，将图像缩放到提供的尺寸（`QSize`）。如果处理程序不支持此选项，`QImageReader` 将在读取图像后执行缩放。
- `QImageIOHandler::ScaledClipRect`: `3`; 图像的缩放裁剪矩形（或 ROI, 感兴趣区域）。支持此选项的处理程序应在应用任何缩放（ScaleSize）或常规裁剪（ClipRect）后，应用提供的裁剪矩形（`QRect`）。如果处理程序不支持此选项，`QImageReader` 将在读取图像后应用缩放裁剪矩形。
- `QImageIOHandler::Description`: `2`; 图像描述。一些图像格式，如 GIF 和 PNG, 允许将文本或注释嵌入图像数据中（例如用于存储版权信息）。文本通常以键值对形式存储，但某些格式将所有文本存储在一个连续块中。`QImageIOHandler` 将文本作为一个 `QString` 返回，其中键和值用 ':' 分隔，键值对之间用两个换行符（\n\n）分隔。例如，"Title: Sunset\n\nAuthor: Jim Smith\nSarah Jones\n\n"。存储文本为单个块的格式可以使用 "Description" 作为键。
- `QImageIOHandler::CompressionRatio`: `5`; 图像数据的压缩比。支持此选项的处理程序在写入时应根据此选项的值（int）设置压缩率。
- `QImageIOHandler::Gamma`: `6`; 图像的伽马等级。支持此选项的处理程序在写入时应根据此选项的值（float）设置图像伽马等级。
- `QImageIOHandler::Quality`: `7`; 图像的质量等级。支持此选项的处理程序在写入时应根据此选项的值（int）设置图像质量等级。
- `QImageIOHandler::Name`: `8`; 图像名称。支持此选项的处理程序应从图像元数据中读取名称并作为 `QString` 返回，或者在写入图像时将名称存储在图像元数据中。
- `QImageIOHandler::SubType`: `9`; 图像子类型。支持此选项的处理程序可以使用子类型值在读取和写入图像时提供帮助。例如，PPM 处理程序的子类型值可能为 "ppm" 或 "ppmraw"。
- `QImageIOHandler::IncrementalReading`: `10`; 支持此选项的处理程序应以类似动画的方式分多次读取图像。`QImageReader` 将把图像视为动画。
- `QImageIOHandler::Endianness`：`11`;图像的端序。某些图像格式可以存储为BigEndian或LittleEndian。支持端序的处理器会利用该选项的值来决定图像应如何存储。
- `QImageIOHandler::Animation`：`12`;支持动画的图像格式在`supportsOption()`中返回该值为真;否则返回为假。
- `QImageIOHandler::BackgroundColor`：`13`;某些图像格式允许指定背景色。支持背景色的处理器在读取图像时会将背景色初始化为该选项（`QColor`）。
- `QImageIOHandler::ImageFormat`：`14`;处理程序返回的图像数据格式。这可以是`QImage::Format`中列出的任何格式。
- `QImageIOHandler::SupportedSubTypes`：`15`;支持不同保存变体的图像格式应在此选项中返回支持变体名称列表（<`QByteArray`>`QList`）。
- `QImageIOHandler::OptimizedWrite`：`16`;支持此选项的处理器在写入时应启用优化标志。
- `QImageIOHandler::ProgressiveScanWrite`：`17`;支持此选项的处理器预期将图像写入为逐行扫描图像。
- `QImageIOHandler::ImageTransformation`：`18`;支持此选项的处理器可以读取图像的转换元数据。支持该选项的处理器不应直接应用该转换。

### `enum QImageIOHandler::Transformationflags QImageIOHandler::Transformations`

**作用与语义：**

该枚举描述了某些图像格式支持的不同变换或方向，通常通过EXIF实现。
- `QImageIOHandler::TransformationNone`：`0`;不应应用任何变换。
- `QImageIOHandler::TransformationMirror`：`1`;水平镜像图像。
- `QImageIOHandler::TransformationFlip`：`2`;垂直镜像。
- `QImageIOHandler::TransformationRotate180`：`TransformationMirror | TransformationFlip`;将图像旋转180度。这等同于水平和垂直镜像。
- `QImageIOHandler::TransformationRotate90`：`4`;将图像旋转90度。
- `QImageIOHandler::TransformationMirrorAndRotate90`：`TransformationMirror | TransformationRotate90`;将图像水平镜像，然后旋转90度。
- `QImageIOHandler::TransformationFlipAndRotate90`：`TransformationFlip | TransformationRotate90`;垂直镜像图像，然后旋转90度。
- `QImageIOHandler::TransformationRotate270`：`TransformationRotate180 | TransformationRotate90`;将图像旋转270度。这相当于水平、垂直镜像，然后旋转90度。
变换类型是QFlag的typedef<Transformation>。它存储了变换值的或组合。

### `QImageIOHandler::QImageIOHandler()`

**作用与语义：**

构建一个QImageIOHandler对象。

### `[virtual noexcept] QImageIOHandler::~QImageIOHandler()`

**作用与语义：**

摧毁`QImageIOHandler`物体。

### `[static, since 6.0] bool QImageIOHandler::allocateImage(QSize size, QImage::Format format, QImage *image)`

**作用与语义：**

这是子类读取函数的一种便捷方法。如果所需分配超过当前分配限制，图像格式处理程序必须拒绝加载图像。该函数检查参数和限制，并在分配有效且必要时执行。成功返回后，`image`将成为给定`size`和`format`的有效分离 `QImage`。

### `[pure virtual] bool QImageIOHandler::canRead() const`

**作用与语义：**

如果可以从设备读取图像（即支持图像格式，设备可读取且初始头信息显示图像可读），返回`true`;否则返回`false`。
在重新实现 canRead() 时，确保 I/O 设备（`device()`）保持其原始状态（例如，使用 peek() 而非 `read()`）。

### `[virtual] int QImageIOHandler::currentImageNumber() const`

**作用与语义：**

对于支持动画的图像格式，该函数返回动画中当前图像的序列号。如果在`read()`图像之前调用该函数，则返回-1。序列中第一张图像的编号为0。
如果图像格式不支持动画，则返回0。

### `[virtual] QRect QImageIOHandler::currentImageRect() const`

**作用与语义：**

返回当前图像的rect。如果没有为图像定义rect，则返回空的QRect()。
该功能适用于动画，因为动画中每次只能更新帧的部分。

### `QIODevice *QImageIOHandler::device() const`

**作用与语义：**

返回当前分配给`QImageIOHandler`的设备。如果设备未被分配，则返回`nullptr`。

### `QByteArray QImageIOHandler::format() const`

**作用与语义：**

返回当前分配给`QImageIOHandler`的格式。如果没有分配格式，则返回空字符串。

### `[virtual] int QImageIOHandler::imageCount() const`

**作用与语义：**

对于支持动画的图像格式，该函数返回动画中的图像数量。如果图像格式不支持动画，或者无法确定图像数量，则返回0。
默认实现返回1，如果`canRead()`返回`true`;否则返回0。

### `[virtual] bool QImageIOHandler::jumpToImage(int imageNumber)`

**作用与语义：**

对于支持动画的图像格式，该函数会跳转到序列号为`imageNumber`的图像。下一次调用`read()`将尝试读取该图像。
默认实现不做任何操作，返回`false`。

### `[virtual] bool QImageIOHandler::jumpToNextImage()`

**作用与语义：**

对于支持动画的图像格式，这个函数会跳转到下一张图片。
默认实现不做任何操作，返回`false`。

### `[virtual] int QImageIOHandler::loopCount() const`

**作用与语义：**

对于支持动画的图像格式，该函数返回动画应循环的次数。如果图像格式不支持动画，则返回0。

### `[virtual] int QImageIOHandler::nextImageDelay() const`

**作用与语义：**

对于支持动画的图像格式，该函数返回等待读取下一张图像的毫秒数。如果图像格式不支持动画，则返回0。

### `[virtual] QVariant QImageIOHandler::option(QImageIOHandler::ImageOption option) const`

**作用与语义：**

返回分配给`option`的`QVariant`值。该值的类型取决于期权。例如，option（Size） 返回`QSize`变体。

### `[pure virtual] bool QImageIOHandler::read(QImage *image)`

**作用与语义：**

从设备读取图像，并存储在`image`中。如果图像成功读取，返回`true`;否则返回false。
对于支持增量加载的图像格式和动画格式，图像处理器可以假设`image`指向上一帧。

### `void QImageIOHandler::setDevice(QIODevice *device)`

**作用与语义：**

将`QImageIOHandler`的设备设置为`device`。图像处理程序在读取和写入图像时将使用该设备。
设备只能设置一次，必须在调用`canRead()`、`read()`、`write()`等之前设置好。如果需要读取多个文件，可以构建多个相应`QImageIOHandler`子类的实例。

### `void QImageIOHandler::setFormat(const QByteArray &format)`

**作用与语义：**

将`QImageIOHandler`的格式设置为`format`。该格式对支持多种图像格式的处理程序最为有用。

### `void QImageIOHandler::setFormat(const QByteArray &format) const`

**作用与语义：**

将`QImageIOHandler`格式设置为`format`。该格式对支持多种图像格式的处理程序最为有用。
该函数被声明为 const，以便从`canRead()`调用。

### `[virtual] void QImageIOHandler::setOption(QImageIOHandler::ImageOption option, const QVariant &value)`

**作用与语义：**

用价值`value`来设置期权`option`。

### `[virtual] bool QImageIOHandler::supportsOption(QImageIOHandler::ImageOption option) const`

**作用与语义：**

如果`QImageIOHandler`支持选项`option`，则返回`true`;否则返回`false`。例如，如果`QImageIOHandler`支持`Size`选项，supportsOption（Size） 必须返回true。

### `[virtual] bool QImageIOHandler::write(const QImage &image)`

**作用与语义：**

将映像`image`写入指定设备。成功时返回`true`;否则返回`false`。
默认实现不做任何操作，只是返回`false`。

### `enum Transformation { TransformationNone, TransformationMirror, TransformationFlip, TransformationRotate180, TransformationRotate90, …, TransformationRotate270 }`

**作用与语义：**

该枚举描述了某些图像格式支持的不同变换或方向，通常通过EXIF实现。
- `QImageIOHandler::TransformationNone`：`0`;不应应用任何变换。
- `QImageIOHandler::TransformationMirror`：`1`;水平镜像图像。
- `QImageIOHandler::TransformationFlip`：`2`;垂直镜像。
- `QImageIOHandler::TransformationRotate180`：`TransformationMirror | TransformationFlip`;将图像旋转180度。这等同于水平和垂直镜像。
- `QImageIOHandler::TransformationRotate90`：`4`;将图像旋转90度。
- `QImageIOHandler::TransformationMirrorAndRotate90`：`TransformationMirror | TransformationRotate90`;将图像水平镜像，然后旋转90度。
- `QImageIOHandler::TransformationFlipAndRotate90`：`TransformationFlip | TransformationRotate90`;垂直镜像图像，然后旋转90度。
- `QImageIOHandler::TransformationRotate270`：`TransformationRotate180 | TransformationRotate90`;将图像旋转270度。这相当于水平、垂直镜像，然后旋转90度。
变换类型是QFlag的typedef<Transformation>。它存储了变换值的或组合。

### `flags Transformations`

**作用与语义：**

该枚举描述了某些图像格式支持的不同变换或方向，通常通过EXIF实现。
- `QImageIOHandler::TransformationNone`：`0`;不应应用任何变换。
- `QImageIOHandler::TransformationMirror`：`1`;水平镜像图像。
- `QImageIOHandler::TransformationFlip`：`2`;垂直镜像。
- `QImageIOHandler::TransformationRotate180`：`TransformationMirror | TransformationFlip`;将图像旋转180度。这等同于水平和垂直镜像。
- `QImageIOHandler::TransformationRotate90`：`4`;将图像旋转90度。
- `QImageIOHandler::TransformationMirrorAndRotate90`：`TransformationMirror | TransformationRotate90`;将图像水平镜像，然后旋转90度。
- `QImageIOHandler::TransformationFlipAndRotate90`：`TransformationFlip | TransformationRotate90`;垂直镜像图像，然后旋转90度。
- `QImageIOHandler::TransformationRotate270`：`TransformationRotate180 | TransformationRotate90`;将图像旋转270度。这相当于水平、垂直镜像，然后旋转90度。
变换类型是QFlag的typedef<Transformation>。它存储了变换值的或组合。

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

`QImageIOHandler` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
