# QMediaCaptureSession

> Qt 6.11.1 · Qt Multimedia

## 1. 先建立直觉

**一句话定位：** `QMediaCaptureSession` 是 Qt Multimedia 的“媒体采集会话”类型，参与媒体源、设备、格式、播放/采集状态或音视频数据处理。

**模块背景：** Qt Multimedia 提供音频、视频、摄像头、媒体会话和设备访问能力。

### 这是什么

`QMediaCaptureSession` 是 多媒体设备与会话机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

**适用场景：** 先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

## 2. 依赖与对象关系

- 头文件：`#include <QMediaCaptureSession>`
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

### 属性

- `(since 6.8) audioBufferInput : QAudioBufferInput*`
- `audioInput : QAudioInput*`
- `audioOutput : QAudioOutput*`
- `camera : QCamera*`
- `imageCapture : QImageCapture*`
- `recorder : QMediaRecorder*`
- `(since 6.5) screenCapture : QScreenCapture*`
- `(since 6.8) videoFrameInput : QVideoFrameInput*`
- `videoOutput : QObject*`
- `(since 6.6) windowCapture : QWindowCapture*`

### 公有函数

- `QMediaCaptureSession(QObject *parent = nullptr)`
- `virtual ~QMediaCaptureSession() override`
- `QAudioBufferInput * audioBufferInput() const`
- `QAudioInput * audioInput() const`
- `QAudioOutput * audioOutput() const`
- `QCamera * camera() const`
- `QImageCapture * imageCapture()`
- `QMediaRecorder * recorder()`
- `QScreenCapture * screenCapture()`
- `void setAudioBufferInput(QAudioBufferInput *input)`
- `void setAudioInput(QAudioInput *input)`
- `void setAudioOutput(QAudioOutput *output)`
- `void setCamera(QCamera *camera)`
- `void setImageCapture(QImageCapture *imageCapture)`
- `void setRecorder(QMediaRecorder *recorder)`
- `void setScreenCapture(QScreenCapture *screenCapture)`
- `void setVideoFrameInput(QVideoFrameInput *input)`
- `void setVideoOutput(QObject *output)`
- `void setVideoSink(QVideoSink *sink)`
- `void setWindowCapture(QWindowCapture *windowCapture)`
- `QVideoFrameInput * videoFrameInput() const`
- `QObject * videoOutput() const`
- `QVideoSink * videoSink() const`
- `QWindowCapture * windowCapture()`

### 信号

- `void audioBufferInputChanged()`
- `void audioInputChanged()`
- `void audioOutputChanged()`
- `void cameraChanged()`
- `void imageCaptureChanged()`
- `void recorderChanged()`
- `void screenCaptureChanged()`
- `void videoFrameInputChanged()`
- `void videoOutputChanged()`
- `void windowCaptureChanged()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[since 6.8] audioBufferInput : QAudioBufferInput*`

**作用与语义：**

该属性包含用于向`QMediaRecorder`发送自定义音频缓冲区的对象。

**如何使用：** 调用 `audioBufferInput()` 读取当前值；它不会修改应用状态。

### `audioInput : QAudioInput*`

**作用与语义：**

返回用于录音的设备。

**如何使用：** 调用 `audioInput()` 读取当前值；它不会修改应用状态。

### `audioOutput : QAudioOutput*`

**作用与语义：**

返回会话的音频输出。

**如何使用：** 调用 `audioOutput()` 读取当前值；它不会修改应用状态。

### `camera : QCamera*`

**作用与语义：**

该特性可容纳用于拍摄视频的摄像机。
通过使用该属性添加摄像机，录制视频或拍摄图像。

**如何使用：** 调用 `camera()` 读取当前值；它不会修改应用状态。

### `imageCapture : QImageCapture*`

**作用与语义：**

该属性包含用于捕捉静态图像的物体。
在拍摄会话中添加一个`QImageCapture`对象，以实现从相机捕捉静态图像。

**如何使用：** 调用 `imageCapture()` 读取当前值；它不会修改应用状态。

### `recorder : QMediaRecorder*`

**作用与语义：**

该属性包含用于捕捉音频/视频的录音对象。
在捕获会话中添加`QMediaRecorder`对象，以实现录制捕获会话中的音频和/或视频。

**如何使用：** 调用 `recorder()` 读取当前值；它不会修改应用状态。

### `[since 6.5] screenCapture : QScreenCapture*`

**作用与语义：**

该属性包含用于捕捉屏幕的对象。
通过使用该属性向捕获会话添加屏幕捕获对象来录制屏幕。

**如何使用：** 调用 `screenCapture()` 读取当前值；它不会修改应用状态。

### `[since 6.8] videoFrameInput : QVideoFrameInput*`

**作用与语义：**

该属性包含用于发送自定义视频帧到`QMediaRecorder`或视频输出的对象。

**如何使用：** 调用 `videoFrameInput()` 读取当前值；它不会修改应用状态。

### `videoOutput : QObject*`

**作用与语义：**

返回会话的视频输出。

**如何使用：** 调用 `videoOutput()` 读取当前值；它不会修改应用状态。

### `[since 6.6] windowCapture : QWindowCapture*`

**作用与语义：**

该属性包含用于捕捉窗口的对象。
通过在捕获会话中添加一个窗口捕获对象，利用该属性来记录一个窗口。

**如何使用：** 调用 `windowCapture()` 读取当前值；它不会修改应用状态。

### `[explicit] QMediaCaptureSession::QMediaCaptureSession(QObject *parent = nullptr)`

**作用与语义：**

创建一个会话用于从`parent`对象中捕获媒体。

### `[override virtual noexcept] QMediaCaptureSession::~QMediaCaptureSession()`

**作用与语义：**

会毁掉整个游戏。

### `void QMediaCaptureSession::setAudioInput(QAudioInput *input)`

**作用与语义：**

返回用于录音的设备。

**如何使用：** 调用 `setAudioInput(...)` 修改 `audioInput`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QMediaCaptureSession::setAudioOutput(QAudioOutput *output)`

**作用与语义：**

返回会话的音频输出。

**如何使用：** 调用 `setAudioOutput(...)` 修改 `audioOutput`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QMediaCaptureSession::setVideoOutput(QObject *output)`

**作用与语义：**

返回会话的视频输出。

**如何使用：** 调用 `setVideoOutput(...)` 修改 `videoOutput`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QMediaCaptureSession::setVideoSink(QVideoSink *sink)`

**作用与语义：**

设置一个`QVideoSink`（`sink`），作为捕获会话的视频预览。
基于`QObject`的预览通常会有一个可调用的`videoSink()`方法返回`QVideoSink`。
之前设定的预告是分离的。

### `QVideoSink *QMediaCaptureSession::videoSink() const`

**作用与语义：**

退还了本场的`QVideoSink`。

### `QAudioBufferInput * audioBufferInput() const`

**作用与语义：**

该属性包含用于向`QMediaRecorder`发送自定义音频缓冲区的对象。

**如何使用：** 调用 `audioBufferInput()` 读取当前值；它不会修改应用状态。

### `QAudioInput * audioInput() const`

**作用与语义：**

返回用于录音的设备。

**如何使用：** 调用 `audioInput()` 读取当前值；它不会修改应用状态。

### `QAudioOutput * audioOutput() const`

**作用与语义：**

返回会话的音频输出。

**如何使用：** 调用 `audioOutput()` 读取当前值；它不会修改应用状态。

### `QCamera * camera() const`

**作用与语义：**

该特性可容纳用于拍摄视频的摄像机。
通过使用该属性添加摄像机，录制视频或拍摄图像。

**如何使用：** 调用 `camera()` 读取当前值；它不会修改应用状态。

### `QImageCapture * imageCapture()`

**作用与语义：**

该属性包含用于捕捉静态图像的物体。
在拍摄会话中添加一个`QImageCapture`对象，以实现从相机捕捉静态图像。

**如何使用：** 调用 `imageCapture()` 读取当前值；它不会修改应用状态。

### `QMediaRecorder * recorder()`

**作用与语义：**

该属性包含用于捕捉音频/视频的录音对象。
在捕获会话中添加`QMediaRecorder`对象，以实现录制捕获会话中的音频和/或视频。

**如何使用：** 调用 `recorder()` 读取当前值；它不会修改应用状态。

### `QScreenCapture * screenCapture()`

**作用与语义：**

该属性包含用于捕捉屏幕的对象。
通过使用该属性向捕获会话添加屏幕捕获对象来录制屏幕。

**如何使用：** 调用 `screenCapture()` 读取当前值；它不会修改应用状态。

### `void setAudioBufferInput(QAudioBufferInput *input)`

**作用与语义：**

该属性包含用于向`QMediaRecorder`发送自定义音频缓冲区的对象。

**如何使用：** 调用 `setAudioBufferInput(...)` 修改 `audioBufferInput`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setCamera(QCamera *camera)`

**作用与语义：**

该特性可容纳用于拍摄视频的摄像机。
通过使用该属性添加摄像机，录制视频或拍摄图像。

**如何使用：** 调用 `setCamera(...)` 修改 `camera`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setImageCapture(QImageCapture *imageCapture)`

**作用与语义：**

该属性包含用于捕捉静态图像的物体。
在拍摄会话中添加一个`QImageCapture`对象，以实现从相机捕捉静态图像。

**如何使用：** 调用 `setImageCapture(...)` 修改 `imageCapture`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setRecorder(QMediaRecorder *recorder)`

**作用与语义：**

该属性包含用于捕捉音频/视频的录音对象。
在捕获会话中添加`QMediaRecorder`对象，以实现录制捕获会话中的音频和/或视频。

**如何使用：** 调用 `setRecorder(...)` 修改 `recorder`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setScreenCapture(QScreenCapture *screenCapture)`

**作用与语义：**

该属性包含用于捕捉屏幕的对象。
通过使用该属性向捕获会话添加屏幕捕获对象来录制屏幕。

**如何使用：** 调用 `setScreenCapture(...)` 修改 `screenCapture`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setVideoFrameInput(QVideoFrameInput *input)`

**作用与语义：**

该属性包含用于发送自定义视频帧到`QMediaRecorder`或视频输出的对象。

**如何使用：** 调用 `setVideoFrameInput(...)` 修改 `videoFrameInput`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setWindowCapture(QWindowCapture *windowCapture)`

**作用与语义：**

该属性包含用于捕捉窗口的对象。
通过在捕获会话中添加一个窗口捕获对象，利用该属性来记录一个窗口。

**如何使用：** 调用 `setWindowCapture(...)` 修改 `windowCapture`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QVideoFrameInput * videoFrameInput() const`

**作用与语义：**

该属性包含用于发送自定义视频帧到`QMediaRecorder`或视频输出的对象。

**如何使用：** 调用 `videoFrameInput()` 读取当前值；它不会修改应用状态。

### `QObject * videoOutput() const`

**作用与语义：**

返回会话的视频输出。

**如何使用：** 调用 `videoOutput()` 读取当前值；它不会修改应用状态。

### `QWindowCapture * windowCapture()`

**作用与语义：**

该属性包含用于捕捉窗口的对象。
通过在捕获会话中添加一个窗口捕获对象，利用该属性来记录一个窗口。

**如何使用：** 调用 `windowCapture()` 读取当前值；它不会修改应用状态。

### `void audioBufferInputChanged()`

**作用与语义：**

该属性包含用于向`QMediaRecorder`发送自定义音频缓冲区的对象。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `audioBufferInput` 的变化，不要把它当作普通函数主动调用。

### `void audioInputChanged()`

**作用与语义：**

返回用于录音的设备。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `audioInput` 的变化，不要把它当作普通函数主动调用。

### `void audioOutputChanged()`

**作用与语义：**

返回会话的音频输出。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `audioOutput` 的变化，不要把它当作普通函数主动调用。

### `void cameraChanged()`

**作用与语义：**

该特性可容纳用于拍摄视频的摄像机。
通过使用该属性添加摄像机，录制视频或拍摄图像。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `camera` 的变化，不要把它当作普通函数主动调用。

### `void imageCaptureChanged()`

**作用与语义：**

该属性包含用于捕捉静态图像的物体。
在拍摄会话中添加一个`QImageCapture`对象，以实现从相机捕捉静态图像。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `imageCapture` 的变化，不要把它当作普通函数主动调用。

### `void recorderChanged()`

**作用与语义：**

该属性包含用于捕捉音频/视频的录音对象。
在捕获会话中添加`QMediaRecorder`对象，以实现录制捕获会话中的音频和/或视频。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `recorder` 的变化，不要把它当作普通函数主动调用。

### `void screenCaptureChanged()`

**作用与语义：**

该属性包含用于捕捉屏幕的对象。
通过使用该属性向捕获会话添加屏幕捕获对象来录制屏幕。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `screenCapture` 的变化，不要把它当作普通函数主动调用。

### `void videoFrameInputChanged()`

**作用与语义：**

该属性包含用于发送自定义视频帧到`QMediaRecorder`或视频输出的对象。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `videoFrameInput` 的变化，不要把它当作普通函数主动调用。

### `void videoOutputChanged()`

**作用与语义：**

返回会话的视频输出。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `videoOutput` 的变化，不要把它当作普通函数主动调用。

### `void windowCaptureChanged()`

**作用与语义：**

该属性包含用于捕捉窗口的对象。
通过在捕获会话中添加一个窗口捕获对象，利用该属性来记录一个窗口。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `windowCapture` 的变化，不要把它当作普通函数主动调用。

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

`QMediaCaptureSession` 所属机制类型：多媒体设备与会话机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
