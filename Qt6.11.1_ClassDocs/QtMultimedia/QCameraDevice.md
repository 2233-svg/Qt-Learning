# QCameraDevice

> Qt 6.11.1 · Qt Multimedia

## 1. 先建立直觉

**一句话定位：** `QCameraDevice` 是 Qt Multimedia 的“摄像头设备”类型，参与媒体源、设备、格式、播放/采集状态或音视频数据处理。

**模块背景：** Qt Multimedia 提供音频、视频、摄像头、媒体会话和设备访问能力。

### 这是什么

`QCameraDevice` 是 多媒体设备与会话机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

**适用场景：** 先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

## 2. 依赖与对象关系

- 头文件：`#include <QCameraDevice>`
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

- `enum Position { UnspecifiedPosition, BackFace, FrontFace }`

### 属性

- `(since 6.7) correctionAngle : const QtVideo::Rotation`
- `description : const QString`
- `id : const QByteArray`
- `isDefault : const bool`
- `position : const Position`
- `videoFormats : const QList<QCameraFormat>`

### 公有函数

- `QCameraDevice()`
- `QCameraDevice(const QCameraDevice &other)`
- `~QCameraDevice()`
- `QtVideo::Rotation correctionAngle() const`
- `QString description() const`
- `QByteArray id() const`
- `bool isDefault() const`
- `bool isNull() const`
- `QList<QSize> photoResolutions() const`
- `QCameraDevice::Position position() const`
- `QList<QCameraFormat> videoFormats() const`
- `bool operator!=(const QCameraDevice &other) const`
- `QCameraDevice & operator=(const QCameraDevice &other)`
- `bool operator==(const QCameraDevice &other) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QCameraDevice::Position`

**作用与语义：**

该枚举指定了摄像机在系统硬件上的物理位置。
- `QCameraDevice::UnspecifiedPosition`：`0`;摄像机位置未明确或未知。
- `QCameraDevice::BackFace`：`1`;摄像头位于系统硬件的背面。例如，在移动设备上，这意味着摄像头位于与屏幕相反的一侧。
- `QCameraDevice::FrontFace`：`2`;摄像头位于系统硬件的前面板上。例如，在移动设备上，这意味着摄像头与屏幕在同一侧。前置摄像头生成的视频帧`QVideoFrame::mirrored`属性设置为`true`。这意味着这些帧的呈现绕垂直轴反转，以显示视频输出为镜面，而录制时仅考虑`QVideoFrame::surfaceFormat`中指定的表面变换。

### `[read-only, since 6.7] correctionAngle : const QtVideo::Rotation`

**作用与语义：**

返回为补偿相机物理旋转所需的旋转角度，相较于其原生方向。换句话说，该属性表示输出图像需要旋转的顺时针角度，以便在设备屏幕上保持其原生方向的直立。由于`correctionAngle`相对于原生方向，因此该值不会因更改设备方向（竖向/横向）而改变。校正角度在Android上可能并非零，因为原生和相机方向由制造商定义。

**如何使用：** 调用 `correctionAngle()` 读取当前值；它不会修改应用状态。

### `[read-only] description : const QString`

**作用与语义：**

返回对相机的人类可读描述。
使用该字符串向用户展示设备。

**如何使用：** 调用 `description()` 读取当前值；它不会修改应用状态。

### `[read-only] id : const QByteArray`

**作用与语义：**

返回相机的设备ID。
这是一个用于识别摄像头的唯一ID，可能无法被人类读取。

**如何使用：** 调用 `id()` 读取当前值；它不会修改应用状态。

### `[read-only] isDefault : const bool`

**作用与语义：**

如果这是默认摄像头设备，则返回为true。

**如何使用：** 调用 `isDefault()` 读取当前值；它不会修改应用状态。

### `[read-only] position : const Position`

**作用与语义：**

返回相机在硬件系统上的物理位置。

**如何使用：** 调用 `position()` 读取当前值；它不会修改应用状态。

### `[read-only] videoFormats : const QList<QCameraFormat>`

**作用与语义：**

返回相机支持的视频格式。

**如何使用：** 调用 `videoFormats()` 读取当前值；它不会修改应用状态。

### `QCameraDevice::QCameraDevice()`

**作用与语义：**

构建一个零摄像机装置。

### `QCameraDevice::QCameraDevice(const QCameraDevice &other)`

**作用与语义：**

复制了`other`。

### `[noexcept] QCameraDevice::~QCameraDevice()`

**作用与语义：**

毁掉`QCameraDevice`。

### `bool QCameraDevice::isNull() const`

**作用与语义：**

如果`QCameraDevice`为空或无效，则返回为真。

### `QList<QSize> QCameraDevice::photoResolutions() const`

**作用与语义：**

返回相机可用来捕捉静态图像的分辨率列表。

### `bool QCameraDevice::operator!=(const QCameraDevice &other) const`

**作用与语义：**

如果该`QCameraDevice`与`other`不代表同一设备，则返回为真。

### `QCameraDevice &QCameraDevice::operator=(const QCameraDevice &other)`

**作用与语义：**

将`QCameraDevice`对象设置为 `other`。

### `bool QCameraDevice::operator==(const QCameraDevice &other) const`

**作用与语义：**

如果该`QCameraDevice`代表与`other`相同的设备，则返回为真。
由于`QCameraDevice`中属性的行为，即使两个`QCameraDevice`实例不完全相等，也可以被视为相等。

### `QtVideo::Rotation correctionAngle() const`

**作用与语义：**

返回为补偿相机物理旋转所需的旋转角度，相较于其原生方向。换句话说，该属性表示输出图像需要旋转的顺时针角度，以便在设备屏幕上保持其原生方向的直立。由于`correctionAngle`相对于原生方向，因此该值不会因更改设备方向（竖向/横向）而改变。校正角度在Android上可能并非零，因为原生和相机方向由制造商定义。

**如何使用：** 调用 `correctionAngle()` 读取当前值；它不会修改应用状态。

### `QString description() const`

**作用与语义：**

返回对相机的人类可读描述。
使用该字符串向用户展示设备。

**如何使用：** 调用 `description()` 读取当前值；它不会修改应用状态。

### `QByteArray id() const`

**作用与语义：**

返回相机的设备ID。
这是一个用于识别摄像头的唯一ID，可能无法被人类读取。

**如何使用：** 调用 `id()` 读取当前值；它不会修改应用状态。

### `bool isDefault() const`

**作用与语义：**

如果这是默认摄像头设备，则返回为true。

**如何使用：** 调用 `isDefault()` 读取当前值；它不会修改应用状态。

### `QCameraDevice::Position position() const`

**作用与语义：**

返回相机在硬件系统上的物理位置。

**如何使用：** 调用 `position()` 读取当前值；它不会修改应用状态。

### `QList<QCameraFormat> videoFormats() const`

**作用与语义：**

返回相机支持的视频格式。

**如何使用：** 调用 `videoFormats()` 读取当前值；它不会修改应用状态。

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

`QCameraDevice` 所属机制类型：多媒体设备与会话机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
