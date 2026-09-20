# QMediaRecorder：把采集会话编码并保存为媒体

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMediaRecorder>`  
> 所属模块：`Qt6::Multimedia`  
> 继承：`QObject -> QMediaRecorder`  
> 类型性质：异步录制控制器

## 它解决什么问题

`QMediaRecorder` 接收 `QMediaCaptureSession` 提供的音频、视频或屏幕内容，交给平台后端编码并写入文件或输出设备。它负责“何时开始、暂停、停止、采用什么容器和编码参数”，而摄像头、麦克风、屏幕捕获和自定义帧输入由会话中的其它对象提供。

典型组合是：

```text
QCamera / QScreenCapture / QWindowCapture / QVideoFrameInput
                                      \
QAudioInput / QAudioBufferInput -> QMediaCaptureSession -> QMediaRecorder
```

它适合：

- 录制摄像头视频、麦克风音频；
- 录制屏幕或窗口；
- 将自定义 `QVideoFrame`、`QAudioBuffer` 编码成文件；
- 选择容器、视频/音频编码器、质量、码率和分辨率；
- 监听录制时长、实际输出文件、状态和错误。

录制是异步的。调用 `record()` 后状态请求会立即改变，但编码器初始化、文件创建和实际写入可能稍后才完成。

## 实际使用场景：最小录音示例

```cpp
QMediaCaptureSession session;
QAudioInput audioInput;
QMediaRecorder recorder;

session.setAudioInput(&audioInput);
session.setRecorder(&recorder);

connect(&recorder, &QMediaRecorder::errorOccurred,
        [](QMediaRecorder::Error error, const QString &message) {
    qWarning() << error << message;
});

recorder.setOutputLocation(
    QUrl::fromLocalFile("/tmp/recording.m4a"));
recorder.setQuality(QMediaRecorder::HighQuality);
recorder.record();
```

录制视频时，把 `QCamera`、`QScreenCapture`、`QWindowCapture` 或 `QVideoFrameInput` 也接到同一个 `QMediaCaptureSession`。没有视频输入时，后端可能把原本的视频格式调整为纯音频格式。

## 生命周期、所有权和线程

- `QMediaRecorder` 是 `QObject`，不可复制；有父对象时由父对象销毁。
- `captureSession()` 返回所属会话的观察指针。通常通过 `QMediaCaptureSession::setRecorder()` 建立连接，不要直接管理内部关系。
- 输入对象和输出 `QIODevice` 的生命周期由应用负责。录制期间不能让输入、输出设备提前销毁或关闭。
- `QMediaRecorder` 依赖事件循环处理编码器启动、数据写入、状态变化和错误通知。通常在创建 `QMediaCaptureSession` 的线程中使用。
- `record()`、`pause()`、`stop()` 是槽，调用返回只表示请求已提交或状态已改变，不代表文件已经可播放。

## 输出位置和实际位置

`outputLocation()` 是应用给出的目标提示，`actualLocation()` 是本次录制最终使用的真实位置。

- 设置新的 `outputLocation`，或设置非空 `outputDevice`，会重置 `actualLocation`；
- 输出位置可以是空 URL、目录或文件，可以是相对路径或绝对路径；
- 位置为空、是目录，或是没有扩展名的文件时，录制器会根据媒体格式和系统 MIME 类型生成合适扩展名；
- 位置是目录时，录制器会在目录中生成文件名；
- 位置为空时，录制器会在系统音频/视频目录生成文件；
- `actualLocation` 通常在开始录制前生成，并在 `recorderStateChanged(RecordingState)` 前发出。

如果指定了带扩展名的文件名，录制器不会根据扩展名自动推断 `QMediaFormat::fileFormat`，也不会替换扩展名。应主动让扩展名和 `mediaFormat().fileFormat()` 一致，或不写扩展名而让录制器生成。

`outputDevice` 优先级高于 `outputLocation`：只要有可写设备，位置会被忽略，且不会生成 `actualLocation`。这条路径目前只由 FFmpeg 后端支持；实际项目最好只选择一种输出方式。

## 录制状态和错误

`recorderState()` 有三种值：

- `StoppedState`：录制器不活动；
- `RecordingState`：已请求录制，实际编码可能仍在异步初始化；
- `PausedState`：已暂停。

`record()` 会立即把状态设为 `RecordingState`，若启动失败则发出 `errorOccurred()`，并回到 `StoppedState`。`pause()` 在不支持暂停的平台上可能不改变状态。编码写盘期间发生空间不足、格式不支持或设备不可用，也可能异步改变状态。

## 格式与编码参数的关系

`mediaFormat` 同时描述容器、视频编码器和音频编码器。调用 `record()` 时，后端可能修正未指定或不支持的字段，并发出 `mediaFormatChanged()`。

- 有视频输入时，通常必须明确指定视频编码器；
- 未指定音频编码器或文件格式时，后端会选择默认值；
- 后端不支持所选容器/编码器组合时，可能替换编码器，甚至报 `FormatError`；
- 没有视频输入时，视频容器请求可能变成音频格式；
- 不能只看 `outputLocation` 的扩展名判断最终格式，使用 `mediaFormat()` 和 `actualLocation()` 确认。

可以先用 `QMediaFormat::isSupported()` 检查组合，但最终可用性仍取决于当前输入、平台、驱动和安装的编解码器。

## 输入速率和背压

摄像头、屏幕捕获或窗口捕获产生视频帧的速度可能高于编码器写入速度。编码器可能丢帧。使用 `QVideoFrameInput` 时，内部帧队列满了以后 `sendVideoFrame()` 返回 `false`，此时应等 `readyToSendVideoFrame()` 再发送；若业务不能丢帧，需要自己实现有界队列并评估内存。

这意味着 `QMediaRecorder` 不是无限容量的缓存。高分辨率、软件编码、慢磁盘和复杂编码参数都会增加背压概率。

## 自动停止（Qt 6.8）

`autoStop` 默认是 `false`。启用后，当所有媒体输入都报告输入结束或已停用时，录制器自动停止。

自定义 `QVideoFrameInput` 或 `QAudioBufferInput` 可以通过发送空帧/空 buffer 报告输入结束；摄像头、屏幕和窗口捕获则可以通过 `setActive(false)` 停用。该属性目前只由 FFmpeg 后端支持，不能把它当作所有平台的通用行为。

## 元数据

`setMetaData()` 设置整组录制元数据，`addMetaData()` 在现有元数据上增加/合并条目。是否写入、支持哪些键以及何时固化由容器和后端决定；通常应在 `record()` 前设置。

## 成员类型

### `enum Quality`

| 值 | 含义 |
| --- | --- |
| `VeryLowQuality` | 极低质量。 |
| `LowQuality` | 低质量。 |
| `NormalQuality` | 普通质量。 |
| `HighQuality` | 高质量。 |
| `VeryHighQuality` | 极高质量。 |

质量是后端编码策略的抽象等级，不是固定码率。若需要精确控制，应配合码率、分辨率和帧率，并检查后端最终采用的格式。

### `enum EncodingMode`

| 值 | 含义 |
| --- | --- |
| `ConstantQualityEncoding` | 尽量保持质量，码率随内容调整。 |
| `ConstantBitRateEncoding` | 尽量保持固定码率，质量随码率限制调整。 |
| `AverageBitRateEncoding` | 以平均码率为目标，允许短时高低变化。 |
| `TwoPassEncoding` | 先分析媒体，再二次编码分配码率；后端未必支持。 |

### `enum RecorderState`

| 值 | 含义 |
| --- | --- |
| `StoppedState` | 录制器不活动。 |
| `RecordingState` | 已请求录制。 |
| `PausedState` | 已暂停。 |

### `enum Error`

| 值 | 含义 |
| --- | --- |
| `NoError` | 没有错误。 |
| `ResourceError` | 设备未准备好或不可用。 |
| `FormatError` | 当前格式不支持。 |
| `OutOfSpaceError` | 设备没有剩余空间。 |
| `LocationNotWritable` | 输出位置不可写。 |

## 逐项 API 说明

### 构造和服务

#### `QMediaRecorder(QObject *parent = nullptr)`

创建录制器，可由父对象管理生命周期。它不自动连接采集输入，也不自动选择输出位置。

#### `~QMediaRecorder()`

销毁录制器及其平台编码器。销毁前应主动 `stop()` 并等待需要保存的状态完成。

#### `bool isAvailable() const`

返回录制服务是否可用。返回 `true` 不等于当前格式、输入组合或编码器一定可用。

#### `QMediaCaptureSession *captureSession() const`

返回当前所属采集会话。连接关系通常由 `QMediaCaptureSession::setRecorder()` 管理。

#### `QPlatformMediaRecorder *platformRecoder() const`

返回 Qt 内部平台录制器指针。它是内部扩展接口，不应作为普通应用 API 使用或自行销毁。

### 输出

#### `QUrl outputLocation() const`

返回应用设置的目标 URL。它可能是空 URL、目录或文件，并不一定等于最终生成的路径。

#### `void setOutputLocation(const QUrl &location)`

设置文件/目录目标。设置成功与否可能在调用时或开始录制时才确定；新位置会重置 `actualLocation`。如果位置不能使用，会通过 `errorOccurred()` 报告。

#### `void setOutputDevice(QIODevice *device)`

设置输出设备。设备应可写并在录制期间保持打开和有效；可写设备会优先于 `outputLocation`。该 API 目前只支持 FFmpeg 后端。

#### `QIODevice *outputDevice() const`

返回当前输出设备指针；不转移所有权。空指针表示没有设置设备输出。

#### `QUrl actualLocation() const`

返回上一次录制使用的真实位置。新设置输出目标后会被清除；设备输出模式下通常为空。

### 状态和计时

#### `RecorderState recorderState() const`

返回停止、录制或暂停状态。状态在控制槽调用时通常同步改变，但失败时也可能异步回到停止。

#### `qint64 duration() const`

返回已经录制的媒体时长，单位毫秒。它是媒体时间，不是从调用 `record()` 开始计算的墙钟时间。

#### `Error error() const`

返回当前错误枚举。

#### `QString errorString() const`

返回当前错误的文字说明。用于日志和界面，不应作为稳定的程序判断条件。

### 格式与编码

#### `QMediaFormat mediaFormat() const`

返回当前容器和编解码器配置。调用 `record()` 后它可能被后端修正。

#### `void setMediaFormat(const QMediaFormat &format)`

设置目标媒体格式。未指定或不支持的字段可能在录制开始时被解析成其它值；格式变化通过 `mediaFormatChanged()` 通知。

#### `EncodingMode encodingMode() const`

返回编码策略。

#### `void setEncodingMode(EncodingMode mode)`

设置恒定质量、恒定码率、平均码率或两遍编码策略。最终是否使用由后端和编码器能力决定。

#### `Quality quality() const`

返回抽象录制质量等级。

#### `void setQuality(Quality quality)`

设置质量等级。它通常与编码器的码率/质量参数关联，不保证对应固定数值。

#### `QSize videoResolution() const`

返回编码视频分辨率。空 `QSize` 表示让录制器根据输入和编码器选择合适分辨率。

#### `void setVideoResolution(const QSize &size)`

设置编码视频宽高；空尺寸恢复自动选择倾向。编码器可能要求特定对齐或最大尺寸。

#### `void setVideoResolution(int width, int height)`

用宽高设置视频分辨率，等价于 `setVideoResolution(QSize(width, height))`。

#### `qreal videoFrameRate() const`

返回目标视频帧率，单位帧/秒。值为 `0` 表示让录制器自动选择。

#### `void setVideoFrameRate(qreal frameRate)`

设置目标视频帧率。输入源、编码器和平台可能无法精确满足，最终输出应以实际媒体为准。

#### `int videoBitRate() const`

返回压缩视频码率，单位 bit/s。该属性自 Qt 6.6 提供。

#### `void setVideoBitRate(int bitRate)`

设置目标视频码率，单位 bit/s。负值或特殊值的具体处理由后端决定，不能代替格式支持检查。

#### `int audioBitRate() const`

返回压缩音频码率，单位 bit/s。

#### `void setAudioBitRate(int bitRate)`

设置压缩音频码率，单位 bit/s。编码器可能把它调整到可用档位。

#### `int audioChannelCount() const`

返回目标音频声道数。

#### `void setAudioChannelCount(int channels)`

设置声道数。传 `-1` 表示根据音频输入和编码器自动选择。

#### `int audioSampleRate() const`

返回目标音频采样率，单位 Hz。

#### `void setAudioSampleRate(int sampleRate)`

设置采样率，单位 Hz。传 `-1` 表示根据输入和编码器自动选择。

### 元数据和自动停止

#### `QMediaMetaData metaData() const`

返回当前录制元数据值。

#### `void setMetaData(const QMediaMetaData &metaData)`

替换录制元数据。通常应在开始录制前设置。

#### `void addMetaData(const QMediaMetaData &metaData)`

把给定元数据合并到当前配置中。重复键的覆盖规则由元数据对象/后端处理，多个属性变化通常只产生一次 `metaDataChanged()`。

#### `bool autoStop() const`

返回是否在所有输入结束或停用后自动停止。该属性自 Qt 6.8 提供。

#### `void setAutoStop(bool autoStop)`

启用或关闭自动停止。自定义输入通过空帧报告结束；该功能目前仅 FFmpeg 后端支持。

### 控制槽

#### `void record()`

开始或继续录制。状态会立即变为 `RecordingState`，但实际编码启动异步进行；失败会发错并回到 `StoppedState`。开始时会生成/更新 `actualLocation`。

#### `void pause()`

暂停录制并请求进入 `PausedState`。平台不支持时状态可能不变。

#### `void stop()`

停止录制并结束输出。文件封装器通常需要在停止时写入尾部索引，应用应等待状态和错误通知再把文件视为完成。

### 信号

#### `recorderStateChanged(RecorderState state)`

录制状态改变时发出。

#### `durationChanged(qint64 duration)`

已录制时长改变时发出，单位毫秒。

#### `actualLocationChanged(const QUrl &location)`

实际输出位置改变时发出，通常发生在开始录制前后。

#### `errorOccurred(Error error, const QString &errorString)`

发生错误时发出，是记录错误事件和提示用户的主要信号。

#### `errorChanged()`

错误属性改变时发出。

#### `metaDataChanged()`

录制元数据改变时发出。

#### `mediaFormatChanged()`

当前媒体格式改变时发出，尤其要注意 `record()` 期间后端自动修正格式的情况。

#### `encodingModeChanged()` / `qualityChanged()`

编码策略或质量等级改变时发出。

#### `videoResolutionChanged()` / `videoFrameRateChanged()` / `videoBitRateChanged()`

视频分辨率、目标帧率或码率改变时发出。

#### `audioBitRateChanged()` / `audioChannelCountChanged()` / `audioSampleRateChanged()`

音频码率、声道数或采样率改变时发出。

#### `autoStopChanged()`（Qt 6.8）

自动停止设置改变时发出。

#### `encoderSettingsChanged()`（已弃用）

旧版兼容信号，自 Qt 6.9 起弃用，应使用具体的格式、质量、码率等变化信号。

## 常见误区

- 只设置了文件扩展名，未设置匹配的 `QMediaFormat`。
- 把 `record()` 返回当作文件已经可以读取；应等待停止完成并检查错误。
- 把 `outputLocation` 和 `actualLocation` 混用。
- 同时设置 `outputDevice` 和 `outputLocation`，却期待两者同时写入。
- 不判断 `isAvailable()` 或格式支持，就认为所有平台都有同样编码器。
- 认为 `pause()` 在所有后端都有相同语义。
- 自定义视频帧持续发送而不处理 `sendVideoFrame()` 的 `false` 返回。
- 录制期间关闭或销毁输出设备。
- 误以为 `autoStop` 是所有后端都支持；Qt 6.11.1 文档明确它只支持 FFmpeg。

## API 速查表

| 类别 | API | 作用 | 边界与重点 |
| --- | --- | --- | --- |
| 构造 | `QMediaRecorder(QObject *)` | 创建录制器。 | QObject 生命周期；默认未连接会话。 |
| 服务 | `isAvailable()` | 查询录制服务。 | 不保证格式和编码器组合可用。 |
| 会话 | `captureSession()` | 查询所属会话。 | 连接通常由 `QMediaCaptureSession` 管理。 |
| 输出 | `outputLocation()` / `setOutputLocation()` | 设置文件或目录目标。 | 不是最终路径；失败异步可见。 |
| 输出 | `outputDevice()` / `setOutputDevice()` | 使用可写 `QIODevice` 输出。 | FFmpeg 支持；优先于 location；不转移所有权。 |
| 输出 | `actualLocation()` | 查询最终文件路径。 | 设置新目标会清除；设备输出通常为空。 |
| 控制 | `record()` / `pause()` / `stop()` | 开始、暂停、停止。 | 编码和封装异步；停止时才完成文件尾部。 |
| 状态 | `recorderState()` | 查询停止/录制/暂停。 | 失败可能异步回到停止。 |
| 时间 | `duration()` | 录制时长。 | 单位毫秒。 |
| 格式 | `mediaFormat()` / `setMediaFormat()` | 查询/设置容器和编解码器。 | `record()` 时可能被后端修正。 |
| 编码 | `encodingMode()` / `setEncodingMode()` | 设置编码策略。 | 后端可能不支持两遍等模式。 |
| 质量 | `quality()` / `setQuality()` | 设置抽象质量等级。 | 不是固定码率。 |
| 视频 | `videoResolution()` / `setVideoResolution()` | 设置分辨率。 | 空尺寸为自动选择；编码器可能调整。 |
| 视频 | `videoFrameRate()` / `setVideoFrameRate()` | 设置帧率，帧/秒。 | 0 为自动选择。 |
| 视频 | `videoBitRate()` / `setVideoBitRate()` | 设置视频码率，bit/s。 | 自 Qt 6.6；最终值可能调整。 |
| 音频 | `audioBitRate()` / `setAudioBitRate()` | 设置音频码率，bit/s。 | 编码器可能调整档位。 |
| 音频 | `audioChannelCount()` / `setAudioChannelCount()` | 设置声道数。 | `-1` 为自动选择。 |
| 音频 | `audioSampleRate()` / `setAudioSampleRate()` | 设置采样率，Hz。 | `-1` 为自动选择。 |
| 元数据 | `metaData()` / `setMetaData()` | 查询/替换元数据。 | 容器和后端决定实际写入能力。 |
| 元数据 | `addMetaData()` | 合并元数据。 | 通常在 `record()` 前设置。 |
| 自动停止 | `autoStop()` / `setAutoStop()` | 输入全部结束后自动停止。 | Qt 6.8；仅 FFmpeg 支持。 |
| 事件 | `recorderStateChanged()` | 观察状态机。 | 录制启动失败也可能引起状态变化。 |
| 事件 | `durationChanged()` / `actualLocationChanged()` | 更新时长和实际路径。 | 路径通常在开始前确定。 |
| 事件 | `errorOccurred()` / `errorChanged()` | 处理错误。 | 优先连接带参数的 `errorOccurred()`。 |
| 事件 | `mediaFormatChanged()` | 观察后端格式修正。 | 尤其关注 `record()` 前后。 |
| 事件 | 各编码参数 `...Changed()` | 更新设置界面。 | 使用具体信号，不用已弃用总信号。 |

---

### 一句话总结

`QMediaRecorder` 只负责编码和写出，输入由 `QMediaCaptureSession` 提供；真正可靠的录制流程必须同时处理格式协商、输出生命周期、编码背压、异步错误和停止完成时机。
