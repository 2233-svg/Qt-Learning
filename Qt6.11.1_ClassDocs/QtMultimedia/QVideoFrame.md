# QVideoFrame

> Qt 6.11.1 · Qt Multimedia

## 1. 先建立直觉

**一句话定位：** `QVideoFrame` 是 Qt Multimedia 的“视频帧”类型，参与媒体源、设备、格式、播放/采集状态或音视频数据处理。

**模块背景：** Qt Multimedia 提供音频、视频、摄像头、媒体会话和设备访问能力。

### 这是什么

`QVideoFrame` 是 多媒体设备与会话机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

**适用场景：** 先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

## 2. 依赖与对象关系

- 头文件：`#include <QVideoFrame>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Multimedia)
target_link_libraries(mytarget PRIVATE Qt6::Multimedia)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

### 状态、生命周期和线程

**生命周期：** 设备或媒体对象要在使用期间保持有效，开始前配置输入/输出和格式，停止后释放会话或解除设备占用。状态、媒体状态和错误信号共同决定下一步操作。

**状态与结果：** 区分无媒体、加载中、已加载、播放中、暂停、停止、结束和错误。进度、时长、缓冲和设备可用性不是同一个状态，不能只用一个 bool 表示。

**线程与事件循环：** 媒体对象通常依赖事件循环和平台线程边界；GUI 展示对象在 GUI 线程，后台处理要使用类明确支持的线程模型。

## 3. 直接使用

先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum HandleType { NoHandle, RhiTextureHandle }`
- `enum MapMode { NotMapped, ReadOnly, WriteOnly, ReadWrite }`

### 公有函数

- `QVideoFrame()`
- `(since 6.8) QVideoFrame(const QImage &image)`
- `QVideoFrame(const QVideoFrameFormat &format)`
- `(since 6.8) QVideoFrame(std::unique_ptr<QAbstractVideoBuffer> videoBuffer)`
- `QVideoFrame(const QVideoFrame &other)`
- `QVideoFrame(QVideoFrame &&other)`
- `~QVideoFrame()`
- `uchar * bits(int plane)`
- `const uchar * bits(int plane) const`
- `int bytesPerLine(int plane) const`
- `qint64 endTime() const`
- `QVideoFrame::HandleType handleType() const`
- `int height() const`
- `bool isMapped() const`
- `bool isReadable() const`
- `bool isValid() const`
- `bool isWritable() const`
- `bool map(QVideoFrame::MapMode mode)`
- `QVideoFrame::MapMode mapMode() const`
- `int mappedBytes(int plane) const`
- `bool mirrored() const`
- `void paint(QPainter *painter, const QRectF &rect, const QVideoFrame::PaintOptions &options)`
- `QVideoFrameFormat::PixelFormat pixelFormat() const`
- `int planeCount() const`
- `QtVideo::Rotation rotation() const`
- `void setEndTime(qint64 time)`
- `void setMirrored(bool mirrored)`
- `void setRotation(QtVideo::Rotation angle)`
- `void setStartTime(qint64 time)`
- `void setStreamFrameRate(qreal rate)`
- `void setSubtitleText(const QString &text)`
- `QSize size() const`
- `qint64 startTime() const`
- `qreal streamFrameRate() const`
- `QString subtitleText() const`
- `QVideoFrameFormat surfaceFormat() const`
- `void swap(QVideoFrame &other)`
- `QImage toImage() const`
- `void unmap()`
- `int width() const`
- `bool operator!=(const QVideoFrame &other) const`
- `QVideoFrame & operator=(QVideoFrame &&other)`
- `QVideoFrame & operator=(const QVideoFrame &other)`
- `bool operator==(const QVideoFrame &other) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QVideoFrame::HandleType`

**作用与语义：**

识别视频缓冲区手柄的类型。
- `QVideoFrame::NoHandle`：`0`;缓冲区没有句柄，其数据只能通过映射缓冲区来访问。
- `QVideoFrame::RhiTextureHandle`：`1`;缓冲区的句柄由Qt渲染硬件接口（RHI）定义。RHI是Qt为3D API（如OpenGL、Vulkan、Metal和Direct 3D）提供的内部图形抽象。

### `enum QVideoFrame::MapMode`

**作用与语义：**

枚举视频缓冲区数据如何映射到系统内存。
- `QVideoFrame::NotMapped`：`0x00`;视频缓冲区不映射到内存。
- `QVideoFrame::ReadOnly`：`0x01`;映射存储器在映射时会填充视频缓冲区的数据，但在未映射时，映射内存的内容可能会被丢弃。
- `QVideoFrame::WriteOnly`：`0x02`;映射后的内存在映射时未初始化，但可能被修改的内容会用于填充视频缓冲区。
- `QVideoFrame::ReadWrite`：`ReadOnly | WriteOnly`;映射内存由视频缓冲区的数据填充，当映射内存取消映射时，视频缓冲区会重新填充映射存储器的内容。

### `QVideoFrame::QVideoFrame()`

**作用与语义：**

构造一个空视频帧。

### `[explicit, since 6.8] QVideoFrame::QVideoFrame(const QImage &image)`

**作用与语义：**

从`QImage`构造一个QVideoFrame。
如果`QImage::Format`与`QVideoFrameFormat::PixelFormat`中的某个格式匹配，QVideoFrame会保留该 `image` 实例并使用该格式，无需任何像素格式转换。在这种情况下，只有当你带着`WriteOnly`标志调用 `QVideoFrame::map` 并保留原始图像时，像素数据才会被复制。
否则，如果`QImage::Format`与任何视频格式都不匹配，图像首先会通过带有`Qt::AutoColor`标志的`QImage::convertedTo()`转换为支持的（A）RGB格式。这可能会带来性能损失。
如果`QImage::isNull()`对输入`QImage`值为真，QVideoFrame将无效，`QVideoFrameFormat::isValid()`返回假。

### `QVideoFrame::QVideoFrame(const QVideoFrameFormat &format)`

**作用与语义：**

构造给定像素`format`的视频帧。

### `[explicit, since 6.8] QVideoFrame::QVideoFrame(std::unique_ptr<QAbstractVideoBuffer> videoBuffer)`

**作用与语义：**

从`QAbstractVideoBuffer`构造QVideoFrame。
指定的`videoBuffer`指的是重新实现的`QAbstractVideoBuffer`实例。实例预期包含预分配的自定义视频缓冲区，并必须实现GPU内容的`QAbstractVideoBuffer::format`、`QAbstractVideoBuffer::map`和`QAbstractVideoBuffer::unmap`。
如果`videoBuffer`空或`QVideoFrameFormat`无效，构造函数会生成无效的视频帧。
创建的帧将在其生命周期内拥有指定视频缓冲区的所有权。考虑到QVideoFrame是通过共享私有对象实现的，当创建的视频帧最后一份副本被销毁时，指定的视频缓冲区将被销毁。
注意，如果视频帧已传递给`QMediaRecorder`或渲染管道，帧的寿命未定义，媒体录制器可以在其他线程中销毁该帧。
QVideoFrame 将包含自己的 `QVideoFrameFormat` 实例。调用 `setStreamFrameRate`、`setMirrored` 或 `setRotation` 时，可以修改内部格式，`surfaceFormat` 返回一个分离的实例。

### `QVideoFrame::QVideoFrame(const QVideoFrame &other)`

**作用与语义：**

构造`other`的浅层副本。由于QVideoFrame是显式共享的，这两个实例将反映同一帧。

### `[constexpr noexcept] QVideoFrame::QVideoFrame(QVideoFrame &&other)`

**作用与语义：**

通过从`other`移动来构造QVideoFrame。

### `[noexcept] QVideoFrame::~QVideoFrame()`

**作用与语义：**

会毁掉视频帧。

### `uchar *QVideoFrame::bits(int plane)`

**作用与语义：**

返回指向帧数据缓冲区起始点的指针，用于一个`plane`。
该值仅在帧数据处于 `mapped` 时有效。
通过该指针访问的数据（映射为写权限时）只有在调用`unmap()`且缓冲区被映射为写入时，才保证被持久化。

### `const uchar *QVideoFrame::bits(int plane) const`

**作用与语义：**

返回指向帧数据缓冲区起点的指针，用于一个`plane`。
该值仅在帧数据处于`mapped`状态时有效。
如果缓冲区没有映射为读取访问，该缓冲区的内容最初将被取消初始化。

### `int QVideoFrame::bytesPerLine(int plane) const`

**作用与语义：**

返回`plane`扫描行中的字节数。
该值仅在帧数据处于 `mapped` 时有效。

### `qint64 QVideoFrame::endTime() const`

**作用与语义：**

当某帧应停止显示时，返回显示时间（以微秒为单位）。
无效时间表示为-1。

### `QVideoFrame::HandleType QVideoFrame::handleType() const`

**作用与语义：**

返回视频帧的句号类型。
句柄类型可以是`NoHandle`，表示帧基于内存，也可以是RHI纹理。

### `int QVideoFrame::height() const`

**作用与语义：**

返回视频帧的高度。

### `bool QVideoFrame::isMapped() const`

**作用与语义：**

识别视频帧内容是否当前映射到系统内存。
这是一个方便函数，用于检查帧的 `MapMode` 不等于 `QVideoFrame::NotMapped`。
如果视频帧内容映射到系统内存，则返回 true;否则返回 false。

### `bool QVideoFrame::isReadable() const`

**作用与语义：**

识别视频帧映射内容是否在映射时从该帧读取。
这是一个方便函数，用于检查`MapMode`是否包含`QVideoFrame::WriteOnly`标志。
如果映射内存内容是从视频帧读取的，则返回为真;否则返回为假。

### `bool QVideoFrame::isValid() const`

**作用与语义：**

识别视频帧是否有效。
无效帧没有关联视频缓冲。
如果帧有效，则返回真;如果无效，则返回假。

### `bool QVideoFrame::isWritable() const`

**作用与语义：**

识别当视频帧未映射时，映射内容是否会被保留。
这是一个方便函数，用于检查`MapMode`是否包含`QVideoFrame::WriteOnly`标志。
如果视频帧在未映射时会更新，则返回 true;否则返回 false。
注意：修改只读模式映射帧数据的结果未定义。根据缓冲区实现，这些更改可能会被持久化，甚至更糟的是改变共享缓冲区。

### `bool QVideoFrame::map(QVideoFrame::MapMode mode)`

**作用与语义：**

将视频帧内容映射到系统（CPU可寻址）内存。
在某些情况下，视频帧数据可能存储在视频存储器或其他无法访问的内存中，因此在访问像素数据之前必须先映射帧。这可能涉及对内容进行复制，因此除非必要，请避免映射和解映射。
映射`mode`指示是否应从映射内存内容读取和/或写入帧。如果映射模式包含`QVideoFrame::ReadOnly`标志，映射内存在初始映射时将填充视频帧的内容。如果映射模式包含`QVideoFrame::WriteOnly`标志，可能修改后的映射内存内容在未映射时会写回帧。
映射时，视频帧的内容可以通过`bits()`函数返回的指针直接访问。
当不再需要访问数据时，务必调用`unmap()`函数释放映射内存，并可能更新视频帧内容。
如果视频帧已以只读模式映射，允许多次映射为只读模式（并相应次数地解映射）。在其他情况下，必须先解除映射帧，再进行第二次映射。
注意：写入映射为只读的内存未定义，可能导致共享数据变更或崩溃。
如果帧在给定`mode`中映射到内存，则返回真;否则返回假。

### `QVideoFrame::MapMode QVideoFrame::mapMode() const`

**作用与语义：**

返回视频帧映射到系统内存的模式。

### `int QVideoFrame::mappedBytes(int plane) const`

**作用与语义：**

返回映射帧数据平面`plane`占用的字节数。
该值仅在帧数据处于 `mapped` 时有效。

### `bool QVideoFrame::mirrored() const`

**作用与语义：**

返回显示前是否应围绕垂直轴镜像帧。
`QVideoFrame`的变换，特别是旋转和镜像，仅用于显示视频帧，并且应用在由`QVideoFrameFormat`决定的表面变换之上。镜像是在旋转之后应用的。
镜像通常用于来自移动设备前置摄像头的视频帧。

### `void QVideoFrame::paint(QPainter *painter, const QRectF &rect, const QVideoFrame::PaintOptions &options)`

**作用与语义：**

使用`QPainter` `painter`将该`QVideoFrame`渲染成`rect`。PaintOptions `options`可用于指定背景色及视频填充`rect`方式。
注意：使用这种方法时，渲染通常不会在没有硬件加速的情况下进行。

### `QVideoFrameFormat::PixelFormat QVideoFrame::pixelFormat() const`

**作用与语义：**

返回该视频帧的像素格式。

### `int QVideoFrame::planeCount() const`

**作用与语义：**

返回视频帧中的飞机数量。

### `QtVideo::Rotation QVideoFrame::rotation() const`

**作用与语义：**

返回显示前画面顺时针旋转的角度。
`QVideoFrame`的变换，特别是旋转和镜像，仅用于显示视频帧，并且应用在由`QVideoFrameFormat`决定的表面变换之上。旋转是在镜像之前应用的。

### `void QVideoFrame::setEndTime(qint64 time)`

**作用与语义：**

设置展示`time`（以微秒计）一个帧应停止显示的时间。
无效时间表示为-1。

### `void QVideoFrame::setMirrored(bool mirrored)`

**作用与语义：**

在显示前，设置画面是否应绕垂直轴`mirrored`。
`QVideoFrame`的变换，特别是旋转和镜像，仅用于显示视频帧，并且会在表面变换之上应用，而表面变换由`QVideoFrameFormat`决定。镜像是在旋转之后应用的。
镜像通常用于来自移动设备前置摄像头的视频帧。
默认值是`false`。

### `void QVideoFrame::setRotation(QtVideo::Rotation angle)`

**作用与语义：**

设置了`angle`画面应顺时针旋转后再显示。
`QVideoFrame`的变换，特别是旋转和镜像，仅用于显示视频帧，并且应用在由`QVideoFrameFormat`决定的表面变换之上。旋转是在镜像之前应用的。
默认值是`QtVideo::Rotation::None`。

### `void QVideoFrame::setStartTime(qint64 time)`

**作用与语义：**

设置展示`time`（以微秒计）帧应初始显示的时间。
无效时间表示为-1。

### `void QVideoFrame::setStreamFrameRate(qreal rate)`

**作用与语义：**

将视频流的帧`rate`数设置为每秒帧数。

### `void QVideoFrame::setSubtitleText(const QString &text)`

**作用与语义：**

将应与该视频帧一起渲染的字幕文本设置为`text`。

### `QSize QVideoFrame::size() const`

**作用与语义：**

返回视频帧的尺寸。

### `qint64 QVideoFrame::startTime() const`

**作用与语义：**

在应显示帧时返回呈现时间（以微秒为单位）。
无效时间表示为-1。

### `qreal QVideoFrame::streamFrameRate() const`

**作用与语义：**

返回视频流的帧率（帧每秒）。

### `QString QVideoFrame::subtitleText() const`

**作用与语义：**

返回应与该视频帧一起渲染的字幕文本。

### `QVideoFrameFormat QVideoFrame::surfaceFormat() const`

**作用与语义：**

返回该视频帧的表面格式。

### `[noexcept] void QVideoFrame::swap(QVideoFrame &other)`

**作用与语义：**

将当前视频帧与`other`互换。

### `QImage QVideoFrame::toImage() const`

**作用与语义：**

将当前视频帧转换为图像。
转换基于当前像素数据和表面格式。帧的变换不会影响结果，因为它们仅用于展示。

### `void QVideoFrame::unmap()`

**作用与语义：**

释放由`map()`函数映射的内存。
如果`MapMode`包含`QVideoFrame::WriteOnly`标志，则映射内存的当前内容会持续存在于视频帧上。
如果函数失败，不应调用 UNMAP（`map()`。

### `int QVideoFrame::width() const`

**作用与语义：**

返回视频帧的宽度。

### `bool QVideoFrame::operator!=(const QVideoFrame &other) const`

**作用与语义：**

如果`QVideoFrame`和`other`不反映相同的帧，返回`true`。

### `[noexcept] QVideoFrame &QVideoFrame::operator=(QVideoFrame &&other)`

**作用与语义：**

`other`进入这个`QVideoFrame`。

### `QVideoFrame &QVideoFrame::operator=(const QVideoFrame &other)`

**作用与语义：**

将`other`的内容分配到该视频帧。由于`QVideoFrame`是显式共享的，这两个实例将反映同一帧。

### `bool QVideoFrame::operator==(const QVideoFrame &other) const`

**作用与语义：**

如果`QVideoFrame`和`other`反映的是相同的参考帧，返回`true`。

## 6. 深入实践与常见坑

### 生命周期和资源边界

设备或媒体对象要在使用期间保持有效，开始前配置输入/输出和格式，停止后释放会话或解除设备占用。状态、媒体状态和错误信号共同决定下一步操作。

### 状态和错误边界

区分无媒体、加载中、已加载、播放中、暂停、停止、结束和错误。进度、时长、缓冲和设备可用性不是同一个状态，不能只用一个 bool 表示。

### 线程边界

媒体对象通常依赖事件循环和平台线程边界；GUI 展示对象在 GUI 线程，后台处理要使用类明确支持的线程模型。

### 最容易出现的错误

不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QVideoFrame` 所属机制类型：多媒体设备与会话机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
