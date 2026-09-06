# QMediaRecorder

> Qt 6.11.1 · Qt Multimedia

## 1. 先建立直觉

**一句话定位：** `QMediaRecorder` 是 Qt Multimedia 的“媒体Recorder”类型，参与媒体源、设备、格式、播放/采集状态或音视频数据处理。

**模块背景：** Qt Multimedia 提供音频、视频、摄像头、媒体会话和设备访问能力。

### 这是什么

`QMediaRecorder` 是 多媒体设备与会话机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

**适用场景：** 先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

## 2. 依赖与对象关系

- 头文件：`#include <QMediaRecorder>`
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

- `enum EncodingMode { ConstantQualityEncoding, ConstantBitRateEncoding, AverageBitRateEncoding, TwoPassEncoding }`
- `enum Error { NoError, ResourceError, FormatError, OutOfSpaceError, LocationNotWritable }`
- `enum Quality { VeryLowQuality, LowQuality, NormalQuality, HighQuality, VeryHighQuality }`
- `enum RecorderState { StoppedState, RecordingState, PausedState }`

### 属性

- `actualLocation : QUrl`
- `audioBitRate : int`
- `audioChannelCount : int`
- `audioSampleRate : int`
- `autoStop : bool`
- `duration : qint64`
- `encodingMode : QMediaRecorder::EncodingMode`
- `error : QMediaRecorder::Error`
- `errorString : QString`
- `mediaFormat : QMediaFormat`
- `metaData : QMediaMetaData`
- `outputLocation : QUrl`
- `quality : Quality`
- `recorderState : QMediaRecorder::RecorderState`
- `(since 6.6) videoBitRate : int`
- `(since 6.6) videoFrameRate : qreal`
- `(since 6.6) videoResolution : QSize`

### 公有函数

- `QMediaRecorder(QObject *parent = nullptr)`
- `virtual ~QMediaRecorder() override`
- `QUrl actualLocation() const`
- `void addMetaData(const QMediaMetaData &metaData)`
- `int audioBitRate() const`
- `int audioChannelCount() const`
- `int audioSampleRate() const`
- `bool autoStop() const`
- `QMediaCaptureSession * captureSession() const`
- `qint64 duration() const`
- `QMediaRecorder::EncodingMode encodingMode() const`
- `QMediaRecorder::Error error() const`
- `QString errorString() const`
- `bool isAvailable() const`
- `QMediaFormat mediaFormat() const`
- `QMediaMetaData metaData() const`
- `QIODevice * outputDevice() const`
- `QUrl outputLocation() const`
- `QMediaRecorder::Quality quality() const`
- `QMediaRecorder::RecorderState recorderState() const`
- `void setAudioBitRate(int bitRate)`
- `void setAudioChannelCount(int channels)`
- `void setAudioSampleRate(int sampleRate)`
- `void setAutoStop(bool autoStop)`
- `void setEncodingMode(QMediaRecorder::EncodingMode mode)`
- `void setMediaFormat(const QMediaFormat &format)`
- `void setMetaData(const QMediaMetaData &metaData)`
- `void setOutputDevice(QIODevice *device)`
- `void setOutputLocation(const QUrl &location)`
- `void setQuality(QMediaRecorder::Quality quality)`
- `void setVideoBitRate(int bitRate)`
- `void setVideoFrameRate(qreal frameRate)`
- `void setVideoResolution(const QSize &size)`
- `void setVideoResolution(int width, int height)`
- `int videoBitRate() const`
- `qreal videoFrameRate() const`
- `QSize videoResolution() const`

### 公有槽函数

- `void pause()`
- `void record()`
- `void stop()`

### 信号

- `void actualLocationChanged(const QUrl &location)`
- `void audioBitRateChanged()`
- `void audioChannelCountChanged()`
- `void audioSampleRateChanged()`
- `void autoStopChanged()`
- `void durationChanged(qint64 duration)`
- `void encodingModeChanged()`
- `void errorChanged()`
- `void errorOccurred(QMediaRecorder::Error error, const QString &errorString)`
- `void mediaFormatChanged()`
- `void metaDataChanged()`
- `void qualityChanged()`
- `void recorderStateChanged(QMediaRecorder::RecorderState state)`
- `void videoBitRateChanged()`
- `void videoFrameRateChanged()`
- `void videoResolutionChanged()`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 77 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QMediaRecorder::EncodingMode`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QMediaRecorder` 暴露的类型声明 `Encoding、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:EncodingMode`。
- 属性名：`QMediaRecorder`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QMediaRecorder::Quality`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QMediaRecorder` 暴露的类型声明 `Quality`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Quality`。
- 属性名：`QMediaRecorder`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] actualLocation : QUrl`

**API 类别：** 属性说明

**中文解读：** 这是 `QMediaRecorder` 的状态/能力属性。通常通过 `actualLocation()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`QUrl`。
- 属性名：`actualLocation`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `audioBitRate : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QMediaRecorder` 的配置属性。初始化或状态切换时通过 `setAudioBitRate(...)` 设置，之后用 `audioBitRate()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`audioBitRate`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `audioChannelCount : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QMediaRecorder` 的配置属性。初始化或状态切换时通过 `setAudioChannelCount(...)` 设置，之后用 `audioChannelCount()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`audioChannelCount`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `audioSampleRate : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QMediaRecorder` 的配置属性。初始化或状态切换时通过 `setAudioSampleRate(...)` 设置，之后用 `audioSampleRate()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`audioSampleRate`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `autoStop : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QMediaRecorder` 的配置属性。初始化或状态切换时通过 `setAutoStop(...)` 设置，之后用 `autoStop()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`autoStop`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] duration : qint64`

**API 类别：** 属性说明

**中文解读：** 这是 `QMediaRecorder` 的状态/能力属性。通常通过 `duration()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`qint64`。
- 属性名：`duration`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `encodingMode : QMediaRecorder::EncodingMode`

**API 类别：** 属性说明

**中文解读：** 这是 `QMediaRecorder` 的配置属性。初始化或状态切换时通过 `setEncodingMode(...)` 设置，之后用 `EncodingMode()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QMediaRecorder::EncodingMode`。
- 属性名：`encodingMode`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] error : QMediaRecorder::Error`

**API 类别：** 属性说明

**中文解读：** 这是 `QMediaRecorder` 的状态/能力属性。通常通过 `Error()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`QMediaRecorder::Error`。
- 属性名：`error`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] errorString : QString`

**API 类别：** 属性说明

**中文解读：** 这是 `QMediaRecorder` 的状态/能力属性。通常通过 `errorString()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`QString`。
- 属性名：`errorString`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `mediaFormat : QMediaFormat`

**API 类别：** 属性说明

**中文解读：** 这是 `QMediaRecorder` 的配置属性。初始化或状态切换时通过 `setMediaFormat(...)` 设置，之后用 `mediaFormat()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QMediaFormat`。
- 属性名：`mediaFormat`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `metaData : QMediaMetaData`

**API 类别：** 属性说明

**中文解读：** 这是 `QMediaRecorder` 的配置属性。初始化或状态切换时通过 `setMetaData(...)` 设置，之后用 `metaData()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QMediaMetaData`。
- 属性名：`metaData`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `outputLocation : QUrl`

**API 类别：** 属性说明

**中文解读：** 这是 `QMediaRecorder` 的配置属性。初始化或状态切换时通过 `setOutputLocation(...)` 设置，之后用 `outputLocation()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QUrl`。
- 属性名：`outputLocation`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `quality : Quality`

**API 类别：** 属性说明

**中文解读：** 这是 `QMediaRecorder` 的配置属性。初始化或状态切换时通过 `setQuality(...)` 设置，之后用 `quality()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`Quality`。
- 属性名：`quality`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] recorderState : QMediaRecorder::RecorderState`

**API 类别：** 属性说明

**中文解读：** 这是 `QMediaRecorder` 的状态/能力属性。通常通过 `RecorderState()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`QMediaRecorder::RecorderState`。
- 属性名：`recorderState`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] videoBitRate : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QMediaRecorder` 的配置属性。初始化或状态切换时通过 `setVideoBitRate(...)` 设置，之后用 `videoBitRate()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`videoBitRate`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] videoFrameRate : qreal`

**API 类别：** 属性说明

**中文解读：** 这是 `QMediaRecorder` 的配置属性。初始化或状态切换时通过 `setVideoFrameRate(...)` 设置，之后用 `videoFrameRate()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`qreal`。
- 属性名：`videoFrameRate`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] videoResolution : QSize`

**API 类别：** 属性说明

**中文解读：** 这是 `QMediaRecorder` 的配置属性。初始化或状态切换时通过 `setVideoResolution(...)` 设置，之后用 `videoResolution()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QSize`。
- 属性名：`videoResolution`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMediaRecorder::QMediaRecorder(QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaRecorder` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual noexcept] QMediaRecorder::~QMediaRecorder()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaRecorder` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QMediaRecorder::actualLocationChanged(const QUrl &location)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaRecorder` 发出的通知信号 `actualLocationChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `const QUrl &`。没有默认值，调用时必须提供。传入 `const QUrl &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMediaRecorder::addMetaData(const QMediaMetaData &metaData)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QMediaRecorder` 添加依赖、数据或子对象的 API `addMetaData`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `metaData`：类型为 `const QMediaMetaData &`。没有默认值，调用时必须提供。传入 `const QMediaMetaData &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QMediaRecorder::audioBitRate() const`

**API 类别：** 成员函数说明

**中文解读：** `QMediaRecorder::audioBitRate` 用于计算、查询或取得与“audio、Bit、Rate”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QMediaRecorder::audioBitRateChanged()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaRecorder` 发出的通知信号 `audioBitRateChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QMediaRecorder::audioChannelCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QMediaRecorder::audioChannelCount` 用于计算、查询或取得与“audio、Channel、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QMediaRecorder::audioChannelCountChanged()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaRecorder` 发出的通知信号 `audioChannelCountChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QMediaRecorder::audioSampleRate() const`

**API 类别：** 成员函数说明

**中文解读：** `QMediaRecorder::audioSampleRate` 用于计算、查询或取得与“audio、Sample、Rate”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QMediaRecorder::audioSampleRateChanged()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaRecorder` 发出的通知信号 `audioSampleRateChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMediaCaptureSession *QMediaRecorder::captureSession() const`

**API 类别：** 成员函数说明

**中文解读：** `QMediaRecorder::captureSession` 用于计算、查询或取得与“capture、Session”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMediaCaptureSession *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMediaCaptureSession *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QMediaRecorder::durationChanged(qint64 duration)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaRecorder` 发出的通知信号 `durationChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `duration`：类型为 `qint64`。没有默认值，调用时必须提供。持续时间，通常以毫秒表示；要确认 0、负数、循环和平台精度。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMediaRecorder::EncodingMode QMediaRecorder::encodingMode() const`

**API 类别：** 成员函数说明

**中文解读：** `QMediaRecorder::encodingMode` 用于计算、查询或取得与“encoding、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMediaRecorder::EncodingMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMediaRecorder::EncodingMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QMediaRecorder::encodingModeChanged()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaRecorder` 发出的通知信号 `encodingModeChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QMediaRecorder::errorOccurred(QMediaRecorder::Error error, const QString &errorString)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaRecorder` 发出的通知信号 `errorOccurred`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `error`：类型为 `QMediaRecorder::Error`。没有默认值，调用时必须提供。错误输出对象或错误状态。解析/执行后要检查它，而不能只看主返回值。
- 参数 `errorString`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMediaRecorder::isAvailable() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isAvailable`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QMediaRecorder::metaDataChanged()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaRecorder` 发出的通知信号 `metaDataChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QIODevice *QMediaRecorder::outputDevice() const`

**API 类别：** 成员函数说明

**中文解读：** `QMediaRecorder::outputDevice` 用于计算、查询或取得与“output、Device”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QIODevice *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QIODevice *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QMediaRecorder::pause()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `pause`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QMediaRecorder::qualityChanged()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaRecorder` 发出的通知信号 `qualityChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QMediaRecorder::record()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `record`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMediaRecorder::RecorderState QMediaRecorder::recorderState() const`

**API 类别：** 成员函数说明

**中文解读：** `QMediaRecorder::recorderState` 用于计算、查询或取得与“recorder、State”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMediaRecorder::RecorderState`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMediaRecorder::RecorderState`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QMediaRecorder::recorderStateChanged(QMediaRecorder::RecorderState state)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaRecorder` 发出的通知信号 `recorderStateChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `state`：类型为 `QMediaRecorder::RecorderState`。没有默认值，调用时必须提供。状态值或状态对象；它描述调用时的阶段，不能把某个状态下有效的 API 用到其他阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMediaRecorder::setAudioBitRate(int bitRate)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAudioBitRate`。调用它会改变 `QMediaRecorder` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `bitRate`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMediaRecorder::setAudioChannelCount(int channels)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAudioChannelCount`。调用它会改变 `QMediaRecorder` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `channels`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMediaRecorder::setAudioSampleRate(int sampleRate)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAudioSampleRate`。调用它会改变 `QMediaRecorder` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `sampleRate`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMediaRecorder::setEncodingMode(QMediaRecorder::EncodingMode mode)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setEncodingMode`。调用它会改变 `QMediaRecorder` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `QMediaRecorder::EncodingMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMediaRecorder::setMetaData(const QMediaMetaData &metaData)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMetaData`。调用它会改变 `QMediaRecorder` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `metaData`：类型为 `const QMediaMetaData &`。没有默认值，调用时必须提供。传入 `const QMediaMetaData &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMediaRecorder::setOutputDevice(QIODevice *device)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setOutputDevice`。调用它会改变 `QMediaRecorder` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `device`：类型为 `QIODevice *`。没有默认值，调用时必须提供。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMediaRecorder::setVideoBitRate(int bitRate)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setVideoBitRate`。调用它会改变 `QMediaRecorder` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `bitRate`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMediaRecorder::setVideoFrameRate(qreal frameRate)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setVideoFrameRate`。调用它会改变 `QMediaRecorder` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `frameRate`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMediaRecorder::setVideoResolution(const QSize &size)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setVideoResolution`。调用它会改变 `QMediaRecorder` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `const QSize &`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMediaRecorder::setVideoResolution(int width, int height)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setVideoResolution`。调用它会改变 `QMediaRecorder` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QMediaRecorder::stop()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `stop`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QMediaRecorder::videoBitRate() const`

**API 类别：** 成员函数说明

**中文解读：** `QMediaRecorder::videoBitRate` 用于计算、查询或取得与“video、Bit、Rate”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QMediaRecorder::videoBitRateChanged()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaRecorder` 发出的通知信号 `videoBitRateChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QMediaRecorder::videoFrameRate() const`

**API 类别：** 成员函数说明

**中文解读：** `QMediaRecorder::videoFrameRate` 用于计算、查询或取得与“video、Frame、Rate”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QMediaRecorder::videoFrameRateChanged()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaRecorder` 发出的通知信号 `videoFrameRateChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSize QMediaRecorder::videoResolution() const`

**API 类别：** 成员函数说明

**中文解读：** `QMediaRecorder::videoResolution` 用于计算、查询或取得与“video、Resolution”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QMediaRecorder::videoResolutionChanged()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaRecorder` 发出的通知信号 `videoResolutionChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum Error { NoError, ResourceError, FormatError, OutOfSpaceError, LocationNotWritable }`

**API 类别：** 公有类型

**中文解读：** 这是 `QMediaRecorder` 暴露的类型声明 `错误`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum RecorderState { StoppedState, RecordingState, PausedState }`

**API 类别：** 公有类型

**中文解读：** 这是 `QMediaRecorder` 暴露的类型声明 `Recorder、State`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QUrl actualLocation() const`

**API 类别：** 公有函数

**中文解读：** `QMediaRecorder::actualLocation` 用于计算、查询或取得与“actual、Location”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QUrl`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QUrl`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool autoStop() const`

**API 类别：** 公有函数

**中文解读：** `QMediaRecorder::autoStop` 用于计算、查询或取得与“auto、停止”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 duration() const`

**API 类别：** 公有函数

**中文解读：** `QMediaRecorder::duration` 用于计算、查询或取得与“持续时间”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMediaRecorder::Error error() const`

**API 类别：** 公有函数

**中文解读：** `QMediaRecorder::error` 用于计算、查询或取得与“错误”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMediaRecorder::Error`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMediaRecorder::Error`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString errorString() const`

**API 类别：** 公有函数

**中文解读：** `QMediaRecorder::errorString` 用于计算、查询或取得与“错误、字符串”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMediaFormat mediaFormat() const`

**API 类别：** 公有函数

**中文解读：** `QMediaRecorder::mediaFormat` 用于计算、查询或取得与“media、格式化”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMediaFormat`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMediaFormat`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMediaMetaData metaData() const`

**API 类别：** 公有函数

**中文解读：** `QMediaRecorder::metaData` 用于计算、查询或取得与“meta、数据访问”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMediaMetaData`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMediaMetaData`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QUrl outputLocation() const`

**API 类别：** 公有函数

**中文解读：** `QMediaRecorder::outputLocation` 用于计算、查询或取得与“output、Location”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QUrl`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QUrl`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMediaRecorder::Quality quality() const`

**API 类别：** 公有函数

**中文解读：** `QMediaRecorder::quality` 用于计算、查询或取得与“quality”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMediaRecorder::Quality`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMediaRecorder::Quality`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setAutoStop(bool autoStop)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setAutoStop`。调用它会改变 `QMediaRecorder` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `autoStop`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setMediaFormat(const QMediaFormat &format)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setMediaFormat`。调用它会改变 `QMediaRecorder` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `format`：类型为 `const QMediaFormat &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setOutputLocation(const QUrl &location)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setOutputLocation`。调用它会改变 `QMediaRecorder` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `location`：类型为 `const QUrl &`。没有默认值，调用时必须提供。传入 `const QUrl &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setQuality(QMediaRecorder::Quality quality)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setQuality`。调用它会改变 `QMediaRecorder` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `quality`：类型为 `QMediaRecorder::Quality`。没有默认值，调用时必须提供。传入 `QMediaRecorder::Quality` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void autoStopChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `autoStopChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void errorChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `errorChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void mediaFormatChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `mediaFormatChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

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

`QMediaRecorder` 所属机制类型：多媒体设备与会话机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
