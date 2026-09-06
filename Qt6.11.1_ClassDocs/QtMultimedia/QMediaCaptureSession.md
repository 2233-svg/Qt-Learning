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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 44 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[since 6.8] audioBufferInput : QAudioBufferInput*`

**API 类别：** 属性说明

**中文解读：** 这是 `QMediaCaptureSession` 的配置属性。初始化或状态切换时通过 `setAudioBufferInput(...)` 设置，之后用 `audioBufferInput()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QAudioBufferInput*`。
- 属性名：`audioBufferInput`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `audioInput : QAudioInput*`

**API 类别：** 属性说明

**中文解读：** 这是 `QMediaCaptureSession` 的配置属性。初始化或状态切换时通过 `setAudioInput(...)` 设置，之后用 `audioInput()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QAudioInput*`。
- 属性名：`audioInput`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `audioOutput : QAudioOutput*`

**API 类别：** 属性说明

**中文解读：** 这是 `QMediaCaptureSession` 的配置属性。初始化或状态切换时通过 `setAudioOutput(...)` 设置，之后用 `audioOutput()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QAudioOutput*`。
- 属性名：`audioOutput`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `camera : QCamera*`

**API 类别：** 属性说明

**中文解读：** 这是 `QMediaCaptureSession` 的配置属性。初始化或状态切换时通过 `setCamera(...)` 设置，之后用 `camera()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QCamera*`。
- 属性名：`camera`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `imageCapture : QImageCapture*`

**API 类别：** 属性说明

**中文解读：** 这是 `QMediaCaptureSession` 的配置属性。初始化或状态切换时通过 `setImageCapture(...)` 设置，之后用 `imageCapture()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QImageCapture*`。
- 属性名：`imageCapture`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `recorder : QMediaRecorder*`

**API 类别：** 属性说明

**中文解读：** 这是 `QMediaCaptureSession` 的配置属性。初始化或状态切换时通过 `setRecorder(...)` 设置，之后用 `recorder()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QMediaRecorder*`。
- 属性名：`recorder`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] screenCapture : QScreenCapture*`

**API 类别：** 属性说明

**中文解读：** 这是 `QMediaCaptureSession` 的配置属性。初始化或状态切换时通过 `setScreenCapture(...)` 设置，之后用 `screenCapture()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QScreenCapture*`。
- 属性名：`screenCapture`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] videoFrameInput : QVideoFrameInput*`

**API 类别：** 属性说明

**中文解读：** 这是 `QMediaCaptureSession` 的配置属性。初始化或状态切换时通过 `setVideoFrameInput(...)` 设置，之后用 `videoFrameInput()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QVideoFrameInput*`。
- 属性名：`videoFrameInput`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `videoOutput : QObject*`

**API 类别：** 属性说明

**中文解读：** 这是 `QMediaCaptureSession` 的配置属性。初始化或状态切换时通过 `setVideoOutput(...)` 设置，之后用 `videoOutput()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QObject*`。
- 属性名：`videoOutput`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] windowCapture : QWindowCapture*`

**API 类别：** 属性说明

**中文解读：** 这是 `QMediaCaptureSession` 的配置属性。初始化或状态切换时通过 `setWindowCapture(...)` 设置，之后用 `windowCapture()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QWindowCapture*`。
- 属性名：`windowCapture`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QMediaCaptureSession::QMediaCaptureSession(QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaCaptureSession` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual noexcept] QMediaCaptureSession::~QMediaCaptureSession()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaCaptureSession` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMediaCaptureSession::setAudioInput(QAudioInput *input)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAudioInput`。调用它会改变 `QMediaCaptureSession` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `input`：类型为 `QAudioInput *`。没有默认值，调用时必须提供。传入 `QAudioInput *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMediaCaptureSession::setAudioOutput(QAudioOutput *output)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAudioOutput`。调用它会改变 `QMediaCaptureSession` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `output`：类型为 `QAudioOutput *`。没有默认值，调用时必须提供。传入 `QAudioOutput *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMediaCaptureSession::setVideoOutput(QObject *output)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setVideoOutput`。调用它会改变 `QMediaCaptureSession` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `output`：类型为 `QObject *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMediaCaptureSession::setVideoSink(QVideoSink *sink)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setVideoSink`。调用它会改变 `QMediaCaptureSession` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `sink`：类型为 `QVideoSink *`。没有默认值，调用时必须提供。传入 `QVideoSink *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVideoSink *QMediaCaptureSession::videoSink() const`

**API 类别：** 成员函数说明

**中文解读：** `QMediaCaptureSession::videoSink` 用于计算、查询或取得与“video、Sink”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVideoSink *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVideoSink *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAudioBufferInput * audioBufferInput() const`

**API 类别：** 公有函数

**中文解读：** `QMediaCaptureSession::audioBufferInput` 用于计算、查询或取得与“audio、Buffer、Input”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAudioBufferInput *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAudioBufferInput *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAudioInput * audioInput() const`

**API 类别：** 公有函数

**中文解读：** `QMediaCaptureSession::audioInput` 用于计算、查询或取得与“audio、Input”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAudioInput *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAudioInput *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAudioOutput * audioOutput() const`

**API 类别：** 公有函数

**中文解读：** `QMediaCaptureSession::audioOutput` 用于计算、查询或取得与“audio、Output”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAudioOutput *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAudioOutput *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCamera * camera() const`

**API 类别：** 公有函数

**中文解读：** `QMediaCaptureSession::camera` 用于计算、查询或取得与“camera”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QCamera *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCamera *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImageCapture * imageCapture()`

**API 类别：** 公有函数

**中文解读：** `QMediaCaptureSession::imageCapture` 用于计算、查询或取得与“image、Capture”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QImageCapture *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QImageCapture *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMediaRecorder * recorder()`

**API 类别：** 公有函数

**中文解读：** `QMediaCaptureSession::recorder` 用于计算、查询或取得与“recorder”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMediaRecorder *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMediaRecorder *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QScreenCapture * screenCapture()`

**API 类别：** 公有函数

**中文解读：** `QMediaCaptureSession::screenCapture` 用于计算、查询或取得与“screen、Capture”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QScreenCapture *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QScreenCapture *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setAudioBufferInput(QAudioBufferInput *input)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setAudioBufferInput`。调用它会改变 `QMediaCaptureSession` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `input`：类型为 `QAudioBufferInput *`。没有默认值，调用时必须提供。传入 `QAudioBufferInput *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setCamera(QCamera *camera)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setCamera`。调用它会改变 `QMediaCaptureSession` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `camera`：类型为 `QCamera *`。没有默认值，调用时必须提供。传入 `QCamera *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setImageCapture(QImageCapture *imageCapture)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setImageCapture`。调用它会改变 `QMediaCaptureSession` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `imageCapture`：类型为 `QImageCapture *`。没有默认值，调用时必须提供。传入 `QImageCapture *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setRecorder(QMediaRecorder *recorder)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setRecorder`。调用它会改变 `QMediaCaptureSession` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `recorder`：类型为 `QMediaRecorder *`。没有默认值，调用时必须提供。传入 `QMediaRecorder *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setScreenCapture(QScreenCapture *screenCapture)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setScreenCapture`。调用它会改变 `QMediaCaptureSession` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `screenCapture`：类型为 `QScreenCapture *`。没有默认值，调用时必须提供。传入 `QScreenCapture *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setVideoFrameInput(QVideoFrameInput *input)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setVideoFrameInput`。调用它会改变 `QMediaCaptureSession` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `input`：类型为 `QVideoFrameInput *`。没有默认值，调用时必须提供。传入 `QVideoFrameInput *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setWindowCapture(QWindowCapture *windowCapture)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setWindowCapture`。调用它会改变 `QMediaCaptureSession` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `windowCapture`：类型为 `QWindowCapture *`。没有默认值，调用时必须提供。传入 `QWindowCapture *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVideoFrameInput * videoFrameInput() const`

**API 类别：** 公有函数

**中文解读：** `QMediaCaptureSession::videoFrameInput` 用于计算、查询或取得与“video、Frame、Input”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVideoFrameInput *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVideoFrameInput *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QObject * videoOutput() const`

**API 类别：** 公有函数

**中文解读：** `QMediaCaptureSession::videoOutput` 用于计算、查询或取得与“video、Output”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QObject *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QObject *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QWindowCapture * windowCapture()`

**API 类别：** 公有函数

**中文解读：** `QMediaCaptureSession::windowCapture` 用于计算、查询或取得与“window、Capture”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QWindowCapture *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QWindowCapture *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void audioBufferInputChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `audioBufferInputChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void audioInputChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `audioInputChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void audioOutputChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `audioOutputChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void cameraChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `cameraChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void imageCaptureChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `imageCaptureChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void recorderChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `recorderChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void screenCaptureChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `screenCaptureChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void videoFrameInputChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `videoFrameInputChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void videoOutputChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `videoOutputChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void windowCaptureChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `windowCaptureChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
