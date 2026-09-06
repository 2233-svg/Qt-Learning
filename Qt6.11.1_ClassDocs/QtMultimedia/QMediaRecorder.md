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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QMediaRecorder::EncodingMode`

**作用与语义：**

枚举编码模式。
- `QMediaRecorder::ConstantQualityEncoding`：`0`;编码旨在保持恒定的质量，并调整码率以适应。
- `QMediaRecorder::ConstantBitRateEncoding`：`1`;编码时使用恒定比特率，并调整质量以适应。
- `QMediaRecorder::AverageBitRateEncoding`：`2`;编码会尝试保持平均码率设置，但根据需要使用更多或更少的码率。
- `QMediaRecorder::TwoPassEncoding`：`3`;介质先被处理以确定特性，然后第二次处理，分配更多位给需要的区域。

### `enum QMediaRecorder::Quality`

**作用与语义：**

枚举质量编码级别。
- `QMediaRecorder::VeryLowQuality`：`0`
- `QMediaRecorder::LowQuality`：`1`
- `QMediaRecorder::NormalQuality`：`2`
- `QMediaRecorder::HighQuality`：`3`
- `QMediaRecorder::VeryHighQuality`：`4`

### `[read-only] actualLocation : QUrl`

**作用与语义：**

该属性包含了最后媒体内容的实际位置。
当分配新的`outputLocation`或非空`outputDevice`时，实际位置会被重置。当调用`record()`且`outputDevice` `null`或不可写时，记录器会根据以下规则生成实际位置。
- 如果`outputLocation`空、目录或无扩展名的文件，录制器会根据所选媒体格式和系统MIME类型生成相应的扩展名。
- 如果`outputLocation`是目录，录音机会在其中生成一个新文件名。
- 如果`outputLocation`为空，录音机会在系统特定目录中生成新的音频或视频文件名。
- 录制器在发射 `recorderStateChanged(RecordingState)` 前先生成实际位置。

**如何使用：** 调用 `actualLocation()` 读取当前值；它不会修改应用状态。

### `audioBitRate : int`

**作用与语义：**

该属性表示压缩音频流的比特率（比特每秒）。

**如何使用：** 调用 `audioBitRate()` 读取当前值；它不会修改应用状态。

### `audioChannelCount : int`

**作用与语义：**

此属性保存音频通道的数量。

**如何使用：** 调用 `audioChannelCount()` 读取当前值；它不会修改应用状态。

### `audioSampleRate : int`

**作用与语义：**

该特性保持音频采样率以Hz为单位。

**如何使用：** 调用 `audioSampleRate()` 读取当前值；它不会修改应用状态。

### `autoStop : bool`

**作用与语义：**

该特性控制媒体录制器是否在所有媒体输入报告流结束或被关闭时自动停止。
流结束时会通过发送一个空媒体帧来报告，你可以通过`QVideoFrameInput`或`QAudioBufferInput`显式发送。
视频输入，特别是 `QCamera`、`QScreenCapture` 和 `QWindowCapture`，可以通过功能`setActive`关闭。
默认是`false`。
QMediaRecorder：：autoStop 仅支持 FFmpeg 后端。

**如何使用：** 调用 `autoStop()` 读取当前值；它不会修改应用状态。

### `[read-only] duration : qint64`

**作用与语义：**

该特性将录制的介质时长保持在毫秒级。

**如何使用：** 调用 `duration()` 读取当前值；它不会修改应用状态。

### `encodingMode : QMediaRecorder::EncodingMode`

**作用与语义：**

该属性表示编码模式。

**如何使用：** 调用 `encodingMode()` 读取当前值；它不会修改应用状态。

### `[read-only] error : QMediaRecorder::Error`

**作用与语义：**

返回当前错误状态。

**如何使用：** 调用 `error()` 读取当前值；它不会修改应用状态。

### `[read-only] errorString : QString`

**作用与语义：**

返回描述当前错误状态的字符串。

**如何使用：** 调用 `errorString()` 读取当前值；它不会修改应用状态。

### `mediaFormat : QMediaFormat`

**作用与语义：**

该属性承载着录制器当前的`QMediaFormat`。
当调用`record()`时，该属性的值可能会发生变化。如果发生这种情况，就会发出 mediaFormatChanged() 信号。如果 `QMediaFormat::audioCodec` 或 `QMediaFormat::fileFormat` 属性设置为未指定，这种情况总是会发生。如果视频源（`QCamera`、`QScreenCapture` 或 `QVideoFrameInput`）连接到了`QMediaCaptureSession`，也必须指定 `QMediaFormat::videoCodec`。如果媒体后端不支持所选的文件格式或编解码器，`QMediaFormat::audioCodec`和`QMediaFormat::videoCodec`属性值也可能发生变化。
如果请求视频格式但未连接视频源，则`QMediaFormat::fileFormat`属性值也可能变为仅`audio`格式，`QMediaCaptureSession`则不连接视频源。例如，如果`QMediaFormat::fileFormat`设置为`QMediaFormat::MPEG4`，则可能改为`QMediaFormat::Mpeg4Audio`。
应用程序可以通过调用`QMediaFormat::isSupported()`函数来判断录制开始前`mediaFormat`是否会变更。在无视频输入录制时，如果满足以下情况，`record()` `QMediaFormat`不会改变：
- `QMediaFormat::fileFormat` 指定
- `QMediaFormat::audioCodec` 被指定
- `QMediaFormat::videoCodec`未具体说明
- `QMediaFormat::isSupported()` `true`
在使用视频输入录制时，如果满足以下情况，`mediaFormat`不会改变：
- `QMediaFormat::fileFormat` 指定
- `QMediaFormat::audioCodec` 指定
- `QMediaFormat::videoCodec` 被指定
- `QMediaFormat::isSupported()` 返回`true`
注意：`QMediaRecorder`在确定`QMediaFormat::fileFormat`时不会考虑`outputLocation`属性中的文件扩展名，且如果指定了扩展名，也不会调整`outputLocation` `QUrl`的扩展名以匹配所选文件格式。因此，应用程序应确保将`QMediaRecorder::mediaFormat::fileFormat`设置为与文件扩展名匹配，或不指定文件扩展名。如果未指定文件扩展名，`actualLocation`文件扩展名将更新为与录制时使用的文件格式一致。

**如何使用：** 调用 `mediaFormat()` 读取当前值；它不会修改应用状态。

### `metaData : QMediaMetaData`

**作用与语义：**

返回与录制相关的元数据。

**如何使用：** 调用 `metaData()` 读取当前值；它不会修改应用状态。

### `outputLocation : QUrl`

**作用与语义：**

此属性保存媒体内容的目标位置。
设置位置可能失败，例如当服务仅支持本地文件系统位置，但传入了网络 URL 时。如果操作失败，将发出 `errorOccurred()` 信号。
如果已为录制器分配可写 `outputDevice`，则输出位置将被忽略。此行为将来可能更改，因此建议只设置一个输出，即 `outputLocation` 或 `outputDevice`。
输出位置可以为空、为目录或文件。目录或文件路径可以是相对路径或绝对路径。`record()` 方法根据指定的输出位置和系统特定设置生成实际位置。详细信息请参阅 `actualLocation` 属性描述。

**如何使用：** 调用 `outputLocation()` 读取当前值；它不会修改应用状态。

### `quality : Quality`

**作用与语义：**

恢复了录制质量。

**如何使用：** 调用 `quality()` 读取当前值；它不会修改应用状态。

### `[read-only] recorderState : QMediaRecorder::RecorderState`

**作用与语义：**

该属性保存了媒体记录器的现状。
状态属性代表用户请求，在`record()`、`pause()`或`stop()`调用时同步变化。录制失败时，录音器状态也可能异步变化。

**如何使用：** 调用 `recorderState()` 读取当前值；它不会修改应用状态。

### `[since 6.6] videoBitRate : int`

**作用与语义：**

该属性表示压缩视频流的比特率（比特每秒）。

**如何使用：** 调用 `videoBitRate()` 读取当前值；它不会修改应用状态。

### `[since 6.6] videoFrameRate : qreal`

**作用与语义：**

该属性表示视频帧率。
值为0表示录制设备应根据视频源可用的内容和编解码器的限制做出最优选择。

**如何使用：** 调用 `videoFrameRate()` 读取当前值；它不会修改应用状态。

### `[since 6.6] videoResolution : QSize`

**作用与语义：**

该属性决定了编码视频的分辨率。
空的`QSize`表示录像机会根据视频源可用的分辨率和编解码器的限制选择最优分辨率。

**如何使用：** 调用 `videoResolution()` 读取当前值；它不会修改应用状态。

### `QMediaRecorder::QMediaRecorder(QObject *parent = nullptr)`

**作用与语义：**

构建一个媒体记录器。媒体记录器是`parent`的产物。

### `[override virtual noexcept] QMediaRecorder::~QMediaRecorder()`

**作用与语义：**

摧毁一个媒体记录器。

### `[signal] void QMediaRecorder::actualLocationChanged(const QUrl &location)`

**作用与语义：**

该属性包含了最后媒体内容的实际位置。
当分配新的`outputLocation`或非空`outputDevice`时，实际位置会被重置。当调用`record()`且`outputDevice` `null`或不可写时，记录器会根据以下规则生成实际位置。
- 如果`outputLocation`空、目录或无扩展名的文件，录制器会根据所选媒体格式和系统MIME类型生成相应的扩展名。
- 如果`outputLocation`是目录，录音机会在其中生成一个新文件名。
- 如果`outputLocation`为空，录音机会在系统特定目录中生成新的音频或视频文件名。
- 录制器在发射 `recorderStateChanged(RecordingState)` 前先生成实际位置。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `actualLocation` 的变化，不要把它当作普通函数主动调用。

### `void QMediaRecorder::addMetaData(const QMediaMetaData &metaData)`

**作用与语义：**

为录制的媒体增添一些`metaData`。

### `int QMediaRecorder::audioBitRate() const`

**作用与语义：**

返回压缩音频流的比特率（比特每秒）。
注意：音频比特率属性的获取函数。

### `[signal] void QMediaRecorder::audioBitRateChanged()`

**作用与语义：**

该属性表示压缩音频流的比特率（比特每秒）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `audioBitRate` 的变化，不要把它当作普通函数主动调用。

### `int QMediaRecorder::audioChannelCount() const`

**作用与语义：**

返回音频通道数量。
注意：属性audioChannelCount的Getter函数。

### `[signal] void QMediaRecorder::audioChannelCountChanged()`

**作用与语义：**

此属性保存音频通道的数量。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `audioChannelCount` 的变化，不要把它当作普通函数主动调用。

### `int QMediaRecorder::audioSampleRate() const`

**作用与语义：**

返回音频采样率（Hz）。
注意：属性audioSampleRate的获取函数。

### `[signal] void QMediaRecorder::audioSampleRateChanged()`

**作用与语义：**

该特性保持音频采样率以Hz为单位。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `audioSampleRate` 的变化，不要把它当作普通函数主动调用。

### `QMediaCaptureSession *QMediaRecorder::captureSession() const`

**作用与语义：**

返回媒体捕获会话。

### `[signal] void QMediaRecorder::durationChanged(qint64 duration)`

**作用与语义：**

该特性将录制的介质时长保持在毫秒级。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `duration` 的变化，不要把它当作普通函数主动调用。

### `QMediaRecorder::EncodingMode QMediaRecorder::encodingMode() const`

**作用与语义：**

返回编码模式。
注意：属性编码模式的获取函数。

### `[signal] void QMediaRecorder::encodingModeChanged()`

**作用与语义：**

该属性表示编码模式。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `encodingMode` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QMediaRecorder::errorOccurred(QMediaRecorder::Error error, const QString &errorString)`

**作用与语义：**

`error`发生的信号，`errorString`包含错误描述。

### `bool QMediaRecorder::isAvailable() const`

**作用与语义：**

退货 `true` 媒体录制服务已准备好使用。

### `[signal] void QMediaRecorder::metaDataChanged()`

**作用与语义：**

返回与录制相关的元数据。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `metaData` 的变化，不要把它当作普通函数主动调用。

### `QIODevice *QMediaRecorder::outputDevice() const`

**作用与语义：**

返回媒体内容的输出输入输出设备。

### `[slot] void QMediaRecorder::pause()`

**作用与语义：**

暂停录制。
录制器状态变为`QMediaRecorder::PausedState`。
根据平台，暂停录制可能不支持。此时录音状态保持不变。

### `[signal] void QMediaRecorder::qualityChanged()`

**作用与语义：**

恢复了录制质量。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `quality` 的变化，不要把它当作普通函数主动调用。

### `[slot] void QMediaRecorder::record()`

**作用与语义：**

开始录音。
虽然录音状态立即切换为c{`QMediaRecorder::RecordingState`}，但录制可以异步开始。
如果录音失败`error()`信号会发出，录音机状态会被重置回`QMediaRecorder::StoppedState`。
该方法根据生成规则更新`actualLocation`。
注意：在移动设备上，录制会按照设备在录制时的方向进行，并在录制期间保持锁定。为避免用户界面出现瑕疵，我们建议只要录制仍在进行，用户界面就保持在同一方向，使用`QWindow`的contentOrientation属性，录制结束后再解锁。

### `QMediaRecorder::RecorderState QMediaRecorder::recorderState() const`

**作用与语义：**

返回当前的媒体记录状态。
注意：property recorderState的获取函数。

### `[signal] void QMediaRecorder::recorderStateChanged(QMediaRecorder::RecorderState state)`

**作用与语义：**

该属性保存了媒体记录器的现状。
状态属性代表用户请求，在`record()`、`pause()`或`stop()`调用时同步变化。录制失败时，录音器状态也可能异步变化。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `recorderState` 的变化，不要把它当作普通函数主动调用。

### `void QMediaRecorder::setAudioBitRate(int bitRate)`

**作用与语义：**

该属性表示压缩音频流的比特率（比特每秒）。

**如何使用：** 调用 `setAudioBitRate(...)` 修改 `audioBitRate`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QMediaRecorder::setAudioChannelCount(int channels)`

**作用与语义：**

此属性保存音频通道的数量。

**如何使用：** 调用 `setAudioChannelCount(...)` 修改 `audioChannelCount`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QMediaRecorder::setAudioSampleRate(int sampleRate)`

**作用与语义：**

该特性保持音频采样率以Hz为单位。

**如何使用：** 调用 `setAudioSampleRate(...)` 修改 `audioSampleRate`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QMediaRecorder::setEncodingMode(QMediaRecorder::EncodingMode mode)`

**作用与语义：**

该属性表示编码模式。

**如何使用：** 调用 `setEncodingMode(...)` 修改 `encodingMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QMediaRecorder::setMetaData(const QMediaMetaData &metaData)`

**作用与语义：**

返回与录制相关的元数据。

**如何使用：** 调用 `setMetaData(...)` 修改 `metaData`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QMediaRecorder::setOutputDevice(QIODevice *device)`

**作用与语义：**

设置媒体内容的输出输入设备。
`device`必须在录制开始前以`WriteOnly`或`ReadWrite`模式打开。
媒体录制器不拥有指定的`device`。如果录制已经开始，设备必须保持活跃并保持开启，直到信号`recorderStateChanged(StoppedState)`发出。
除非`null`指定的`device`，否则该方法会立即重置`actualLocation`。
如果录音机被分配了可写输出设备，`outputLocation`会被忽略，录制开始时不会生成`actualLocation`。这种行为未来可能会改变，因此我们建议只设置一个输出，分别是`outputLocation`或`outputDevice`。
`QMediaRecorder::setOutputDevice`只支持FFmpeg后端。

### `void QMediaRecorder::setVideoBitRate(int bitRate)`

**作用与语义：**

该属性表示压缩视频流的比特率（比特每秒）。

**如何使用：** 调用 `setVideoBitRate(...)` 修改 `videoBitRate`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QMediaRecorder::setVideoFrameRate(qreal frameRate)`

**作用与语义：**

该属性表示视频帧率。
值为0表示录制设备应根据视频源可用的内容和编解码器的限制做出最优选择。

**如何使用：** 调用 `setVideoFrameRate(...)` 修改 `videoFrameRate`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QMediaRecorder::setVideoResolution(const QSize &size)`

**作用与语义：**

该属性决定了编码视频的分辨率。
空的`QSize`表示录像机会根据视频源可用的分辨率和编解码器的限制选择最优分辨率。

**如何使用：** 调用 `setVideoResolution(...)` 修改 `videoResolution`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QMediaRecorder::setVideoResolution(int width, int height)`

**作用与语义：**

该属性决定了编码视频的分辨率。
空的`QSize`表示录像机会根据视频源可用的分辨率和编解码器的限制选择最优分辨率。

**如何使用：** 调用 `setVideoResolution(...)` 修改 `videoResolution`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `[slot] void QMediaRecorder::stop()`

**作用与语义：**

录制器会停止录制。处理待处理的视频和音频数据仍可能需要一些时间。一旦媒体录制器状态变为`QMediaRecorder::StoppedState`，录制就完成了。

### `int QMediaRecorder::videoBitRate() const`

**作用与语义：**

返回压缩视频流的比特率（比特每秒）。
注意：属性 videoBitRate 的 Getter 函数。

### `[signal] void QMediaRecorder::videoBitRateChanged()`

**作用与语义：**

该属性表示压缩视频流的比特率（比特每秒）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `videoBitRate` 的变化，不要把它当作普通函数主动调用。

### `qreal QMediaRecorder::videoFrameRate() const`

**作用与语义：**

返回视频帧率。
注意：属性 videoFrameRate 的获取函数。

### `[signal] void QMediaRecorder::videoFrameRateChanged()`

**作用与语义：**

该属性表示视频帧率。
值为0表示录制设备应根据视频源可用的内容和编解码器的限制做出最优选择。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `videoFrameRate` 的变化，不要把它当作普通函数主动调用。

### `QSize QMediaRecorder::videoResolution() const`

**作用与语义：**

返回编码视频的分辨率。
注意：属性视频分辨率的获取函数。

### `[signal] void QMediaRecorder::videoResolutionChanged()`

**作用与语义：**

该属性决定了编码视频的分辨率。
空的`QSize`表示录像机会根据视频源可用的分辨率和编解码器的限制选择最优分辨率。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `videoResolution` 的变化，不要把它当作普通函数主动调用。

### `enum Error { NoError, ResourceError, FormatError, OutOfSpaceError, LocationNotWritable }`

**作用与语义：**

- `QMediaRecorder::NoError`：`0`;无错误。
- `QMediaRecorder::ResourceError`：`1`;设备尚未准备好或不可用。
- `QMediaRecorder::FormatError`：`2`;不支持当前格式。
- `QMediaRecorder::OutOfSpaceError`：`3`;设备无剩余空间。
- `QMediaRecorder::LocationNotWritable`：`4`;输出位置不可写。

### `enum RecorderState { StoppedState, RecordingState, PausedState }`

**作用与语义：**

- `QMediaRecorder::StoppedState`：`0`;录音机不激活。
- `QMediaRecorder::RecordingState`：`1`;录音请求。
- `QMediaRecorder::PausedState`：`2`;录音机暂停。

### `QUrl actualLocation() const`

**作用与语义：**

该属性包含了最后媒体内容的实际位置。
当分配新的`outputLocation`或非空`outputDevice`时，实际位置会被重置。当调用`record()`且`outputDevice` `null`或不可写时，记录器会根据以下规则生成实际位置。
- 如果`outputLocation`空、目录或无扩展名的文件，录制器会根据所选媒体格式和系统MIME类型生成相应的扩展名。
- 如果`outputLocation`是目录，录音机会在其中生成一个新文件名。
- 如果`outputLocation`为空，录音机会在系统特定目录中生成新的音频或视频文件名。
- 录制器在发射 `recorderStateChanged(RecordingState)` 前先生成实际位置。

**如何使用：** 调用 `actualLocation()` 读取当前值；它不会修改应用状态。

### `bool autoStop() const`

**作用与语义：**

该特性控制媒体录制器是否在所有媒体输入报告流结束或被关闭时自动停止。
流结束时会通过发送一个空媒体帧来报告，你可以通过`QVideoFrameInput`或`QAudioBufferInput`显式发送。
视频输入，特别是 `QCamera`、`QScreenCapture` 和 `QWindowCapture`，可以通过功能`setActive`关闭。
默认是`false`。
QMediaRecorder：：autoStop 仅支持 FFmpeg 后端。

**如何使用：** 调用 `autoStop()` 读取当前值；它不会修改应用状态。

### `qint64 duration() const`

**作用与语义：**

该特性将录制的介质时长保持在毫秒级。

**如何使用：** 调用 `duration()` 读取当前值；它不会修改应用状态。

### `QMediaRecorder::Error error() const`

**作用与语义：**

返回当前错误状态。

**如何使用：** 调用 `error()` 读取当前值；它不会修改应用状态。

### `QString errorString() const`

**作用与语义：**

返回描述当前错误状态的字符串。

**如何使用：** 调用 `errorString()` 读取当前值；它不会修改应用状态。

### `QMediaFormat mediaFormat() const`

**作用与语义：**

该属性承载着录制器当前的`QMediaFormat`。
当调用`record()`时，该属性的值可能会发生变化。如果发生这种情况，就会发出 mediaFormatChanged() 信号。如果 `QMediaFormat::audioCodec` 或 `QMediaFormat::fileFormat` 属性设置为未指定，这种情况总是会发生。如果视频源（`QCamera`、`QScreenCapture` 或 `QVideoFrameInput`）连接到了`QMediaCaptureSession`，也必须指定 `QMediaFormat::videoCodec`。如果媒体后端不支持所选的文件格式或编解码器，`QMediaFormat::audioCodec`和`QMediaFormat::videoCodec`属性值也可能发生变化。
如果请求视频格式但未连接视频源，则`QMediaFormat::fileFormat`属性值也可能变为仅`audio`格式，`QMediaCaptureSession`则不连接视频源。例如，如果`QMediaFormat::fileFormat`设置为`QMediaFormat::MPEG4`，则可能改为`QMediaFormat::Mpeg4Audio`。
应用程序可以通过调用`QMediaFormat::isSupported()`函数来判断录制开始前`mediaFormat`是否会变更。在无视频输入录制时，如果满足以下情况，`record()` `QMediaFormat`不会改变：
- `QMediaFormat::fileFormat` 指定
- `QMediaFormat::audioCodec` 被指定
- `QMediaFormat::videoCodec`未具体说明
- `QMediaFormat::isSupported()` `true`
在使用视频输入录制时，如果满足以下情况，`mediaFormat`不会改变：
- `QMediaFormat::fileFormat` 指定
- `QMediaFormat::audioCodec` 指定
- `QMediaFormat::videoCodec` 被指定
- `QMediaFormat::isSupported()` 返回`true`
注意：`QMediaRecorder`在确定`QMediaFormat::fileFormat`时不会考虑`outputLocation`属性中的文件扩展名，且如果指定了扩展名，也不会调整`outputLocation` `QUrl`的扩展名以匹配所选文件格式。因此，应用程序应确保将`QMediaRecorder::mediaFormat::fileFormat`设置为与文件扩展名匹配，或不指定文件扩展名。如果未指定文件扩展名，`actualLocation`文件扩展名将更新为与录制时使用的文件格式一致。

**如何使用：** 调用 `mediaFormat()` 读取当前值；它不会修改应用状态。

### `QMediaMetaData metaData() const`

**作用与语义：**

返回与录制相关的元数据。

**如何使用：** 调用 `metaData()` 读取当前值；它不会修改应用状态。

### `QUrl outputLocation() const`

**作用与语义：**

此属性保存媒体内容的目标位置。
设置位置可能失败，例如当服务仅支持本地文件系统位置，但传入了网络 URL 时。如果操作失败，将发出 `errorOccurred()` 信号。
如果已为录制器分配可写 `outputDevice`，则输出位置将被忽略。此行为将来可能更改，因此建议只设置一个输出，即 `outputLocation` 或 `outputDevice`。
输出位置可以为空、为目录或文件。目录或文件路径可以是相对路径或绝对路径。`record()` 方法根据指定的输出位置和系统特定设置生成实际位置。详细信息请参阅 `actualLocation` 属性描述。

**如何使用：** 调用 `outputLocation()` 读取当前值；它不会修改应用状态。

### `QMediaRecorder::Quality quality() const`

**作用与语义：**

恢复了录制质量。

**如何使用：** 调用 `quality()` 读取当前值；它不会修改应用状态。

### `void setAutoStop(bool autoStop)`

**作用与语义：**

该特性控制媒体录制器是否在所有媒体输入报告流结束或被关闭时自动停止。
流结束时会通过发送一个空媒体帧来报告，你可以通过`QVideoFrameInput`或`QAudioBufferInput`显式发送。
视频输入，特别是 `QCamera`、`QScreenCapture` 和 `QWindowCapture`，可以通过功能`setActive`关闭。
默认是`false`。
QMediaRecorder：：autoStop 仅支持 FFmpeg 后端。

**如何使用：** 调用 `setAutoStop(...)` 修改 `autoStop`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMediaFormat(const QMediaFormat &format)`

**作用与语义：**

该属性承载着录制器当前的`QMediaFormat`。
当调用`record()`时，该属性的值可能会发生变化。如果发生这种情况，就会发出 mediaFormatChanged() 信号。如果 `QMediaFormat::audioCodec` 或 `QMediaFormat::fileFormat` 属性设置为未指定，这种情况总是会发生。如果视频源（`QCamera`、`QScreenCapture` 或 `QVideoFrameInput`）连接到了`QMediaCaptureSession`，也必须指定 `QMediaFormat::videoCodec`。如果媒体后端不支持所选的文件格式或编解码器，`QMediaFormat::audioCodec`和`QMediaFormat::videoCodec`属性值也可能发生变化。
如果请求视频格式但未连接视频源，则`QMediaFormat::fileFormat`属性值也可能变为仅`audio`格式，`QMediaCaptureSession`则不连接视频源。例如，如果`QMediaFormat::fileFormat`设置为`QMediaFormat::MPEG4`，则可能改为`QMediaFormat::Mpeg4Audio`。
应用程序可以通过调用`QMediaFormat::isSupported()`函数来判断录制开始前`mediaFormat`是否会变更。在无视频输入录制时，如果满足以下情况，`record()` `QMediaFormat`不会改变：
- `QMediaFormat::fileFormat` 指定
- `QMediaFormat::audioCodec` 被指定
- `QMediaFormat::videoCodec`未具体说明
- `QMediaFormat::isSupported()` `true`
在使用视频输入录制时，如果满足以下情况，`mediaFormat`不会改变：
- `QMediaFormat::fileFormat` 指定
- `QMediaFormat::audioCodec` 指定
- `QMediaFormat::videoCodec` 被指定
- `QMediaFormat::isSupported()` 返回`true`
注意：`QMediaRecorder`在确定`QMediaFormat::fileFormat`时不会考虑`outputLocation`属性中的文件扩展名，且如果指定了扩展名，也不会调整`outputLocation` `QUrl`的扩展名以匹配所选文件格式。因此，应用程序应确保将`QMediaRecorder::mediaFormat::fileFormat`设置为与文件扩展名匹配，或不指定文件扩展名。如果未指定文件扩展名，`actualLocation`文件扩展名将更新为与录制时使用的文件格式一致。

**如何使用：** 调用 `setMediaFormat(...)` 修改 `mediaFormat`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setOutputLocation(const QUrl &location)`

**作用与语义：**

此属性保存媒体内容的目标位置。
设置位置可能失败，例如当服务仅支持本地文件系统位置，但传入了网络 URL 时。如果操作失败，将发出 `errorOccurred()` 信号。
如果已为录制器分配可写 `outputDevice`，则输出位置将被忽略。此行为将来可能更改，因此建议只设置一个输出，即 `outputLocation` 或 `outputDevice`。
输出位置可以为空、为目录或文件。目录或文件路径可以是相对路径或绝对路径。`record()` 方法根据指定的输出位置和系统特定设置生成实际位置。详细信息请参阅 `actualLocation` 属性描述。

**如何使用：** 调用 `setOutputLocation(...)` 修改 `outputLocation`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setQuality(QMediaRecorder::Quality quality)`

**作用与语义：**

恢复了录制质量。

**如何使用：** 调用 `setQuality(...)` 修改 `quality`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void autoStopChanged()`

**作用与语义：**

该特性控制媒体录制器是否在所有媒体输入报告流结束或被关闭时自动停止。
流结束时会通过发送一个空媒体帧来报告，你可以通过`QVideoFrameInput`或`QAudioBufferInput`显式发送。
视频输入，特别是 `QCamera`、`QScreenCapture` 和 `QWindowCapture`，可以通过功能`setActive`关闭。
默认是`false`。
QMediaRecorder：：autoStop 仅支持 FFmpeg 后端。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `autoStop` 的变化，不要把它当作普通函数主动调用。

### `void errorChanged()`

**作用与语义：**

返回当前错误状态。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `error` 的变化，不要把它当作普通函数主动调用。

### `void mediaFormatChanged()`

**作用与语义：**

该属性承载着录制器当前的`QMediaFormat`。
当调用`record()`时，该属性的值可能会发生变化。如果发生这种情况，就会发出 mediaFormatChanged() 信号。如果 `QMediaFormat::audioCodec` 或 `QMediaFormat::fileFormat` 属性设置为未指定，这种情况总是会发生。如果视频源（`QCamera`、`QScreenCapture` 或 `QVideoFrameInput`）连接到了`QMediaCaptureSession`，也必须指定 `QMediaFormat::videoCodec`。如果媒体后端不支持所选的文件格式或编解码器，`QMediaFormat::audioCodec`和`QMediaFormat::videoCodec`属性值也可能发生变化。
如果请求视频格式但未连接视频源，则`QMediaFormat::fileFormat`属性值也可能变为仅`audio`格式，`QMediaCaptureSession`则不连接视频源。例如，如果`QMediaFormat::fileFormat`设置为`QMediaFormat::MPEG4`，则可能改为`QMediaFormat::Mpeg4Audio`。
应用程序可以通过调用`QMediaFormat::isSupported()`函数来判断录制开始前`mediaFormat`是否会变更。在无视频输入录制时，如果满足以下情况，`record()` `QMediaFormat`不会改变：
- `QMediaFormat::fileFormat` 指定
- `QMediaFormat::audioCodec` 被指定
- `QMediaFormat::videoCodec`未具体说明
- `QMediaFormat::isSupported()` `true`
在使用视频输入录制时，如果满足以下情况，`mediaFormat`不会改变：
- `QMediaFormat::fileFormat` 指定
- `QMediaFormat::audioCodec` 指定
- `QMediaFormat::videoCodec` 被指定
- `QMediaFormat::isSupported()` 返回`true`
注意：`QMediaRecorder`在确定`QMediaFormat::fileFormat`时不会考虑`outputLocation`属性中的文件扩展名，且如果指定了扩展名，也不会调整`outputLocation` `QUrl`的扩展名以匹配所选文件格式。因此，应用程序应确保将`QMediaRecorder::mediaFormat::fileFormat`设置为与文件扩展名匹配，或不指定文件扩展名。如果未指定文件扩展名，`actualLocation`文件扩展名将更新为与录制时使用的文件格式一致。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `mediaFormat` 的变化，不要把它当作普通函数主动调用。

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
