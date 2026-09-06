# QImageCapture

> Qt 6.11.1 · Qt Multimedia

## 1. 先建立直觉

**一句话定位：** `QImageCapture` 是 Qt Multimedia 的“图像采集”类型，参与媒体源、设备、格式、播放/采集状态或音视频数据处理。

**模块背景：** Qt Multimedia 提供音频、视频、摄像头、媒体会话和设备访问能力。

### 这是什么

`QImageCapture` 是 多媒体设备与会话机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

**适用场景：** 先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

## 2. 依赖与对象关系

- 头文件：`#include <QImageCapture>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Multimedia)
target_link_libraries(mytarget PRIVATE Qt6::Multimedia)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

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

- `enum Error { NoError, NotReadyError, ResourceError, OutOfSpaceError, NotSupportedFeatureError, FormatError }`
- `enum FileFormat { UnspecifiedFormat, JPEG, PNG, WebP, Tiff }`
- `enum Quality { VeryLowQuality, LowQuality, NormalQuality, HighQuality, VeryHighQuality }`

### 属性

- `error : Error`
- `errorString : QString`
- `fileFormat : FileFormat`
- `metaData : QMediaMetaData`
- `quality : Quality`
- `readyForCapture : bool`
- `supportedFormats : const QList<FileFormat>`

### 公有函数

- `QImageCapture(QObject *parent = nullptr)`
- `virtual ~QImageCapture() override`
- `void addMetaData(const QMediaMetaData &metaData)`
- `QMediaCaptureSession * captureSession() const`
- `QImageCapture::Error error() const`
- `QString errorString() const`
- `QImageCapture::FileFormat fileFormat() const`
- `bool isAvailable() const`
- `bool isReadyForCapture() const`
- `QMediaMetaData metaData() const`
- `QImageCapture::Quality quality() const`
- `QSize resolution() const`
- `void setFileFormat(QImageCapture::FileFormat format)`
- `void setMetaData(const QMediaMetaData &metaData)`
- `void setQuality(QImageCapture::Quality quality)`
- `void setResolution(const QSize &resolution)`
- `void setResolution(int width, int height)`

### 公有槽函数

- `int capture()`
- `int captureToFile(const QString &file = QString())`

### 信号

- `void errorChanged()`
- `void errorOccurred(int id, QImageCapture::Error error, const QString &errorString)`
- `void fileFormatChanged()`
- `void imageAvailable(int id, const QVideoFrame &frame)`
- `void imageCaptured(int id, const QImage &preview)`
- `void imageExposed(int id)`
- `void imageMetadataAvailable(int id, const QMediaMetaData &metaData)`
- `void imageSaved(int id, const QString &fileName)`
- `void metaDataChanged()`
- `void qualityChanged()`
- `void readyForCaptureChanged(bool ready)`
- `void resolutionChanged()`

### 静态公有成员

- `QString fileFormatDescription(QImageCapture::FileFormat f)`
- `QString fileFormatName(QImageCapture::FileFormat f)`
- `QList<QImageCapture::FileFormat> supportedFormats()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QImageCapture::FileFormat`

**作用与语义：**

请选择以下图片格式之一：
- `QImageCapture::UnspecifiedFormat`：`0`;未指定格式
- `QImageCapture::JPEG`：`1`;`.jpg`或 `.jpeg` 格式
- `QImageCapture::PNG`：`2`;`.png` 格式
- `QImageCapture::WebP`：`3`;`.webp` 格式
- `QImageCapture::Tiff`：`4`;`.tiff` 格式

### `enum QImageCapture::Quality`

**作用与语义：**

枚举质量编码级别。
- `QImageCapture::VeryLowQuality`：`0`
- `QImageCapture::LowQuality`：`1`
- `QImageCapture::NormalQuality`：`2`
- `QImageCapture::HighQuality`：`3`
- `QImageCapture::VeryHighQuality`：`4`

### `[read-only] error : Error`

**作用与语义：**

返回当前错误状态。

**如何使用：** 调用 `error()` 读取当前值；它不会修改应用状态。

### `[read-only] errorString : QString`

**作用与语义：**

返回描述当前错误状态的字符串。

**如何使用：** 调用 `errorString()` 读取当前值；它不会修改应用状态。

### `fileFormat : FileFormat`

**作用与语义：**

该属性表示图像格式。

**如何使用：** 调用 `fileFormat()` 读取当前值；它不会修改应用状态。

### `metaData : QMediaMetaData`

**作用与语义：**

该属性包含将嵌入图像中的元数据。
注意：摄像机后端可能会添加时间戳或位置等额外字段。

**如何使用：** 调用 `metaData()` 读取当前值；它不会修改应用状态。

### `quality : Quality`

**作用与语义：**

该属性表示图像编码质量。

**如何使用：** 调用 `quality()` 读取当前值；它不会修改应用状态。

### `[read-only] readyForCapture : bool`

**作用与语义：**

如果相机准备好立即拍摄图像，则保持`true`。在`readyForCapture`时调用`capture()`不被允许`false`，否则会导致错误。

**如何使用：** 调用 `readyForCapture()` 读取当前值；它不会修改应用状态。

### `[read-only] supportedFormats : const QList<FileFormat>`

**作用与语义：**

该属性包含支持的文件格式列表。

**如何使用：** 调用 `supportedFormats()` 读取当前值；它不会修改应用状态。

### `[explicit] QImageCapture::QImageCapture(QObject *parent = nullptr)`

**作用与语义：**

从`parent`构建一个图像捕捉对象，能够捕捉由相机产生的单个静态图像。
你必须将图像捕获对象和`QCamera`连接到捕获会话以进行图像捕捉。

### `[override virtual noexcept] QImageCapture::~QImageCapture()`

**作用与语义：**

图像被摧毁，捕捉物体。

### `void QImageCapture::addMetaData(const QMediaMetaData &metaData)`

**作用与语义：**

为嵌入在捕获图像中的现有元数据添加额外 `metaData`。

### `[slot] int QImageCapture::capture()`

**作用与语义：**

捕获图像并作为`QImage`提供。该操作在大多数情况下是异步的，随后是信号 `QImageCapture::imageExposed()`、`QImageCapture::imageCaptured()` 或 `QImageCapture::error()`。
QImageCapture：：capture 返回捕获 Id 参数，用于 `imageExposed()`、`imageCaptured()` 和 `imageSaved()` 信号。

### `QMediaCaptureSession *QImageCapture::captureSession() const`

**作用与语义：**

返回该摄像机所连接的捕获会话，若摄像机未连接捕获会话则返回nullptr。
使用`QMediaCaptureSession::setImageCapture()`将图像捕获连接到会话。

### `[slot] int QImageCapture::captureToFile(const QString &file = QString())`

**作用与语义：**

捕获图像并保存到`file`。大多数情况下，该操作是异步的，随后是信号`QImageCapture::imageExposed()`、`QImageCapture::imageCaptured()`、`QImageCapture::imageSaved()`或`QImageCapture::error()`。
如果传递空 `file`，摄像机后端会选择系统中照片的默认位置和命名方案，如果只指定文件名且未标明完整路径，图片会保存到默认目录，并用 `imageCaptured()` 和 `imageSaved()` 信号报告完整路径。
`QCamera`保存所有拍摄参数，如曝光设置或图像处理参数，因此调用`capture()`后相机参数的更改不会影响之前的拍摄请求。
`QImageCapture::capture`返回捕获Id参数，用于`imageExposed()`、`imageCaptured()`和`imageSaved()`信号。

### `[signal] void QImageCapture::errorOccurred(int id, QImageCapture::Error error, const QString &errorString)`

**作用与语义：**

通过`error`和`errorString`描述表示捕获请求失败`id`信号。

### `[static] QString QImageCapture::fileFormatDescription(QImageCapture::FileFormat f)`

**作用与语义：**

返回给定文件格式的描述，`f`。

### `[static] QString QImageCapture::fileFormatName(QImageCapture::FileFormat f)`

**作用与语义：**

返回给定格式的名称，`f`。

### `[signal] void QImageCapture::imageAvailable(int id, const QVideoFrame &frame)`

**作用与语义：**

当请求`id`的`frame`可用时发出的信号。

### `[signal] void QImageCapture::imageCaptured(int id, const QImage &preview)`

**作用与语义：**

当请求`id`帧被捕获但尚未处理和保存时发出的信号。帧`preview`可以显示给用户。

### `[signal] void QImageCapture::imageExposed(int id)`

**作用与语义：**

当带有请求`id`的帧被暴露时发出的信号。

### `[signal] void QImageCapture::imageMetadataAvailable(int id, const QMediaMetaData &metaData)`

**作用与语义：**

这表示`id`识别的图像已经有`metaData`。

### `[signal] void QImageCapture::imageSaved(int id, const QString &fileName)`

**作用与语义：**

当QImageCapture：：CaptureToFile被设置且包含请求`id`的帧保存到`fileName`时发出的信号。

### `bool QImageCapture::isAvailable() const`

**作用与语义：**

如果图像捕获服务准备好使用，则返回为真。

### `[signal] void QImageCapture::readyForCaptureChanged(bool ready)`

**作用与语义：**

如果相机准备好立即拍摄图像，则保持`true`。在`readyForCapture`时调用`capture()`不被允许`false`，否则会导致错误。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `readyForCapture` 的变化，不要把它当作普通函数主动调用。

### `QSize QImageCapture::resolution() const`

**作用与语义：**

返回编码图像的分辨率。

### `[signal] void QImageCapture::resolutionChanged()`

**作用与语义：**

图像分辨率变化时会发出信号。

### `void QImageCapture::setFileFormat(QImageCapture::FileFormat format)`

**作用与语义：**

该属性表示图像格式。

**如何使用：** 调用 `setFileFormat(...)` 修改 `fileFormat`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QImageCapture::setMetaData(const QMediaMetaData &metaData)`

**作用与语义：**

该属性包含将嵌入图像中的元数据。
注意：摄像机后端可能会添加时间戳或位置等额外字段。

**如何使用：** 调用 `setMetaData(...)` 修改 `metaData`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QImageCapture::setQuality(QImageCapture::Quality quality)`

**作用与语义：**

该属性表示图像编码质量。

**如何使用：** 调用 `setQuality(...)` 修改 `quality`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QImageCapture::setResolution(const QSize &resolution)`

**作用与语义：**

设置编码图像的`resolution`。
空的`QSize`表示编码器应根据图像源的可用信息和编解码器的限制做出最优选择。

### `void QImageCapture::setResolution(int width, int height)`

**作用与语义：**

设定编码图像分辨率的`width`和`height`。

### `[static] QList<QImageCapture::FileFormat> QImageCapture::supportedFormats()`

**作用与语义：**

返回支持的文件格式列表。
注意：支持属性格式的获取函数。

### `enum Error { NoError, NotReadyError, ResourceError, OutOfSpaceError, NotSupportedFeatureError, FormatError }`

**作用与语义：**

- `QImageCapture::NoError`：`0`;无错误。
- `QImageCapture::NotReadyError`：`1`;该服务尚未准备好捕获。
- `QImageCapture::ResourceError`：`2`;设备尚未准备好或不可用。
- `QImageCapture::OutOfSpaceError`：`3`;设备无剩余空间。
- `QImageCapture::NotSupportedFeatureError`：`4`;设备不支持静态图像拍摄。
- `QImageCapture::FormatError`：`5`;不支持当前格式。

### `QImageCapture::Error error() const`

**作用与语义：**

返回当前错误状态。

**如何使用：** 调用 `error()` 读取当前值；它不会修改应用状态。

### `QString errorString() const`

**作用与语义：**

返回描述当前错误状态的字符串。

**如何使用：** 调用 `errorString()` 读取当前值；它不会修改应用状态。

### `QImageCapture::FileFormat fileFormat() const`

**作用与语义：**

该属性表示图像格式。

**如何使用：** 调用 `fileFormat()` 读取当前值；它不会修改应用状态。

### `bool isReadyForCapture() const`

**作用与语义：**

如果相机准备好立即拍摄图像，则保持`true`。在`readyForCapture`时调用`capture()`不被允许`false`，否则会导致错误。

**如何使用：** 调用 `isReadyForCapture()` 读取当前值；它不会修改应用状态。

### `QMediaMetaData metaData() const`

**作用与语义：**

该属性包含将嵌入图像中的元数据。
注意：摄像机后端可能会添加时间戳或位置等额外字段。

**如何使用：** 调用 `metaData()` 读取当前值；它不会修改应用状态。

### `QImageCapture::Quality quality() const`

**作用与语义：**

该属性表示图像编码质量。

**如何使用：** 调用 `quality()` 读取当前值；它不会修改应用状态。

### `void errorChanged()`

**作用与语义：**

返回当前错误状态。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `error` 的变化，不要把它当作普通函数主动调用。

### `void fileFormatChanged()`

**作用与语义：**

该属性表示图像格式。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `fileFormat` 的变化，不要把它当作普通函数主动调用。

### `void metaDataChanged()`

**作用与语义：**

该属性包含将嵌入图像中的元数据。
注意：摄像机后端可能会添加时间戳或位置等额外字段。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `metaData` 的变化，不要把它当作普通函数主动调用。

### `void qualityChanged()`

**作用与语义：**

该属性表示图像编码质量。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `quality` 的变化，不要把它当作普通函数主动调用。

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

`QImageCapture` 所属机制类型：多媒体设备与会话机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
