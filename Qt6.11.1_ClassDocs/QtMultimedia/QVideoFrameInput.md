# QVideoFrameInput

> Qt 6.11.1 · Qt Multimedia

## 1. 先建立直觉

**一句话定位：** `QVideoFrameInput` 是 Qt Multimedia 的“视频帧输入”类型，参与媒体源、设备、格式、播放/采集状态或音视频数据处理。

**模块背景：** Qt Multimedia 提供音频、视频、摄像头、媒体会话和设备访问能力。

### 这是什么

`QVideoFrameInput` 是 多媒体设备与会话机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

**适用场景：** 先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

## 2. 依赖与对象关系

- 头文件：`#include <QVideoFrameInput>`
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

### 公有函数

- `QVideoFrameInput(QObject *parent = nullptr)`
- `QVideoFrameInput(const QVideoFrameFormat &format, QObject *parent = nullptr)`
- `virtual ~QVideoFrameInput() override`
- `QMediaCaptureSession * captureSession() const`
- `QVideoFrameFormat format() const`
- `bool sendVideoFrame(const QVideoFrame &frame)`

### 信号

- `void readyToSendVideoFrame()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QVideoFrameInput::QVideoFrameInput(QObject *parent = nullptr)`

**作用与语义：**

构建一个新的QVideoFrameInput对象，`parent`。

### `[explicit] QVideoFrameInput::QVideoFrameInput(const QVideoFrameFormat &format, QObject *parent = nullptr)`

**作用与语义：**

构建一个新的QVideoFrameInput对象，包含视频帧`format`和`parent`。
指定的`format`在调用`QMediaRecorder::record()`时作为匹配视频编码器初始化的提示。如果格式未指定或无效，视频编码器将在发送第一帧时初始化。在匹配视频编码器初始化后发送不同像素格式和尺寸的视频帧可能会导致录制时的性能损失。
如果你提前知道要发送什么样的帧，我们建议你先指定格式。

### `[override virtual noexcept] QVideoFrameInput::~QVideoFrameInput()`

**作用与语义：**

摧毁了该物体。

### `QMediaCaptureSession *QVideoFrameInput::captureSession() const`

**作用与语义：**

返回该视频帧输入所连接的捕获会话，或者如果视频帧输入未连接到捕获会话，则返回`nullptr`。
用`QMediaCaptureSession::setVideoFrameInput()`将视频帧输入连接到会话。

### `QVideoFrameFormat QVideoFrameInput::format() const`

**作用与语义：**

返回构建视频帧输入时指定的视频帧格式。

### `[signal] void QVideoFrameInput::readyToSendVideoFrame()`

**作用与语义：**

信号表明可以向视频帧输入发送新的帧。收到信号后，如果你还有帧要发送，可以调用一次或循环调用`sendVideoFrame`，直到它返回`false`。

### `bool QVideoFrameInput::sendVideoFrame(const QVideoFrame &frame)`

**作用与语义：**

通过`QMediaCaptureSession`发送`QVideoFrame`到`QMediaRecorder`或视频输出。
如果指定的`frame`已成功发送到目的地，返回`true`。返回`false`，如果帧尚未发送，这种情况可能发生在实例未分配给`QMediaCaptureSession`、会话没有视频输出或媒体录制设备、媒体录制器未启动或队列已满时。信号`readyToSendVideoFrame`将在目标能够处理新帧时立即发送。
发送空视频帧时，`QMediaRecorder`视为输入流的结束。如果视频`QMediaRecorder::autoStop` `true`且所有输入都报告了流的结束，`QMediaRecorder`会自动停止录制。

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

`QVideoFrameInput` 所属机制类型：多媒体设备与会话机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
