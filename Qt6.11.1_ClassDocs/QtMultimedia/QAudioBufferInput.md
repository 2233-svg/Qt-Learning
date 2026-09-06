# QAudioBufferInput

> Qt 6.11.1 · Qt Multimedia

## 1. 先建立直觉

**一句话定位：** `QAudioBufferInput` 是 Qt Multimedia 的“音频缓冲区输入”类型，参与媒体源、设备、格式、播放/采集状态或音视频数据处理。

**模块背景：** Qt Multimedia 提供音频、视频、摄像头、媒体会话和设备访问能力。

### 这是什么

`QAudioBufferInput` 是 多媒体设备与会话机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

**适用场景：** 先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

## 2. 依赖与对象关系

- 头文件：`#include <QAudioBufferInput>`
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

- `QAudioBufferInput(QObject *parent = nullptr)`
- `QAudioBufferInput(const QAudioFormat &format, QObject *parent = nullptr)`
- `virtual ~QAudioBufferInput() override`
- `QMediaCaptureSession * captureSession() const`
- `QAudioFormat format() const`
- `bool sendAudioBuffer(const QAudioBuffer &audioBuffer)`

### 信号

- `void readyToSendAudioBuffer()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QAudioBufferInput::QAudioBufferInput(QObject *parent = nullptr)`

**作用与语义：**

构建一个新的QAudioBufferInput对象，`parent`。

### `[explicit] QAudioBufferInput::QAudioBufferInput(const QAudioFormat &format, QObject *parent = nullptr)`

**作用与语义：**

构建一个新的QAudioBufferInput对象，带有音频`format`和`parent`。
指定的`format`将作为调用`QMediaRecorder::record()`时初始化匹配音频编码器的提示。如果格式未指定或无效，音频编码器将在发送第一个音频缓冲区时初始化。
如果你事先知道要发送哪种音频缓冲区，建议你先指定格式。

### `[override virtual noexcept] QAudioBufferInput::~QAudioBufferInput()`

**作用与语义：**

摧毁了该物体。

### `QMediaCaptureSession *QAudioBufferInput::captureSession() const`

**作用与语义：**

返回该音频缓冲输入连接的捕获会话，若音频缓冲输入未连接捕获会话则返回`nullptr`。
用`QMediaCaptureSession::setAudioBufferInput()`把音频缓冲输入连接到会话。

### `QAudioFormat QAudioBufferInput::format() const`

**作用与语义：**

返回构建音频缓冲输入时指定的音频格式。

### `[signal] void QAudioBufferInput::readyToSendAudioBuffer()`

**作用与语义：**

可以发送到音频缓冲输入端的信号。收到信号后，如果你有音频日期要发送，可以调用一次或循环调用`sendAudioBuffer`直到返回`false`。

### `bool QAudioBufferInput::sendAudioBuffer(const QAudioBuffer &audioBuffer)`

**作用与语义：**

通过`QMediaCaptureSession` `QAudioBuffer`去`QMediaRecorder`。
如果指定`audioBuffer`已成功发送到目的地，返回`true`。返回 `false`，如果缓冲区未发送，这种情况可能发生在实例未分配给`QMediaCaptureSession`、会话没有媒体录制器、媒体录制器未启动或队列已满时。一旦目标能够处理新的音频缓冲区，`readyToSendAudioBuffer()`信号将立即发出。
发送空音频缓冲区时，`QMediaRecorder` 视为输入流的结束。`QMediaRecorder` 会在`QMediaRecorder::autoStop`被`true`且所有输入都报告流的结束时自动停止录音。

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

`QAudioBufferInput` 所属机制类型：多媒体设备与会话机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
