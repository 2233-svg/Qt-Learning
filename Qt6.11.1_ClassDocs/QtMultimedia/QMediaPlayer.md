# QMediaPlayer

> Qt 6.11.1 · Qt Multimedia

## 1. 先建立直觉

**一句话定位：** `QMediaPlayer` 是 Qt Multimedia 的“媒体Player”类型，参与媒体源、设备、格式、播放/采集状态或音视频数据处理。

**模块背景：** Qt Multimedia 提供音频、视频、摄像头、媒体会话和设备访问能力。

### 这是什么

`QMediaPlayer` 是 多媒体设备与会话机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

**适用场景：** 先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

## 2. 依赖与对象关系

- 头文件：`#include <QMediaPlayer>`
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

- `enum Error { NoError, ResourceError, FormatError, NetworkError, AccessDeniedError }`
- `enum Loops { Infinite, Once }`
- `enum MediaStatus { NoMedia, LoadingMedia, LoadedMedia, StalledMedia, BufferingMedia, …, InvalidMedia }`
- `(since 6.10) enum class PitchCompensationAvailability { AlwaysOn, Available, Unavailable }`
- `enum PlaybackState { StoppedState, PlayingState, PausedState }`

### 属性

- `activeAudioTrack : int`
- `activeSubtitleTrack : int`
- `activeVideoTrack : int`
- `(since 6.8) audioBufferOutput : QAudioBufferOutput*`
- `audioOutput : QAudioOutput*`
- `audioTracks : QList<QMediaMetaData>`
- `bufferProgress : float`
- `duration : qint64`
- `error : Error`
- `errorString : QString`
- `hasAudio : bool`
- `hasVideo : bool`
- `loops : int`
- `mediaStatus : MediaStatus`
- `metaData : QMediaMetaData`
- `(since 6.10) pitchCompensation : bool`
- `(since 6.10) pitchCompensationAvailability : const PitchCompensationAvailability`
- `(since 6.10) playbackOptions : QPlaybackOptions`
- `playbackRate : qreal`
- `playbackState : PlaybackState`
- `(since 6.5) playing : bool`
- `position : qint64`
- `seekable : bool`
- `source : QUrl`
- `subtitleTracks : QList<QMediaMetaData>`
- `videoOutput : QObject*`
- `videoTracks : QList<QMediaMetaData>`

### 公有函数

- `QMediaPlayer(QObject *parent = nullptr)`
- `virtual ~QMediaPlayer() override`
- `int activeAudioTrack() const`
- `int activeSubtitleTrack() const`
- `int activeVideoTrack() const`
- `QAudioBufferOutput * audioBufferOutput() const`
- `QAudioOutput * audioOutput() const`
- `QList<QMediaMetaData> audioTracks() const`
- `float bufferProgress() const`
- `QMediaTimeRange bufferedTimeRange() const`
- `qint64 duration() const`
- `QMediaPlayer::Error error() const`
- `QString errorString() const`
- `bool hasAudio() const`
- `bool hasVideo() const`
- `bool isAvailable() const`
- `bool isPlaying() const`
- `bool isSeekable() const`
- `int loops() const`
- `QMediaPlayer::MediaStatus mediaStatus() const`
- `QMediaMetaData metaData() const`
- `(since 6.10) bool pitchCompensation() const`
- `(since 6.10) QMediaPlayer::PitchCompensationAvailability pitchCompensationAvailability() const`
- `QPlaybackOptions playbackOptions() const`
- `qreal playbackRate() const`
- `QMediaPlayer::PlaybackState playbackState() const`
- `qint64 position() const`
- `void setActiveAudioTrack(int index)`
- `void setActiveSubtitleTrack(int index)`
- `void setActiveVideoTrack(int index)`
- `void setAudioBufferOutput(QAudioBufferOutput *output)`
- `void setAudioOutput(QAudioOutput *output)`
- `void setLoops(int loops)`
- `void setVideoOutput(QObject *)`
- `void setVideoSink(QVideoSink *sink)`
- `QUrl source() const`
- `const QIODevice * sourceDevice() const`
- `QList<QMediaMetaData> subtitleTracks() const`
- `QObject * videoOutput() const`
- `QVideoSink * videoSink() const`
- `QList<QMediaMetaData> videoTracks() const`

### 公有槽函数

- `void pause()`
- `void play()`
- `void resetPlaybackOptions()`
- `(since 6.10) void setPitchCompensation(bool enabled) const`
- `void setPlaybackOptions(const QPlaybackOptions &options)`
- `void setPlaybackRate(qreal rate)`
- `void setPosition(qint64 position)`
- `void setSource(const QUrl &source)`
- `void setSourceDevice(QIODevice *device, const QUrl &sourceUrl = QUrl())`
- `void stop()`

### 信号

- `void activeTracksChanged()`
- `void audioBufferOutputChanged()`
- `void audioOutputChanged()`
- `void bufferProgressChanged(float filled)`
- `void durationChanged(qint64 duration)`
- `void errorChanged()`
- `void errorOccurred(QMediaPlayer::Error error, const QString &errorString)`
- `void hasAudioChanged(bool available)`
- `void hasVideoChanged(bool videoAvailable)`
- `void loopsChanged()`
- `void mediaStatusChanged(QMediaPlayer::MediaStatus status)`
- `void metaDataChanged()`
- `void pitchCompensationChanged(bool)`
- `void playbackOptionsChanged()`
- `void playbackRateChanged(qreal rate)`
- `void playbackStateChanged(QMediaPlayer::PlaybackState newState)`
- `void playingChanged(bool playing)`
- `void positionChanged(qint64 position)`
- `void seekableChanged(bool seekable)`
- `void sourceChanged(const QUrl &media)`
- `void tracksChanged()`
- `void videoOutputChanged()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QMediaPlayer::Error`

**作用与语义：**

定义了媒体播放器错误条件。
- `QMediaPlayer::NoError`：`0`;未发生错误。
- `QMediaPlayer::ResourceError`：`1`;媒体资源问题无法解决。
- `QMediaPlayer::FormatError`：`2`;媒体资源的格式尚未（完全）支持。播放可能仍然可能，但不包含音频或视频成分。
- `QMediaPlayer::NetworkError`：`3`;发生网络错误。
- `QMediaPlayer::AccessDeniedError`：`4`;播放媒体资源时没有合适的权限。

### `enum QMediaPlayer::Loops`

**作用与语义：**

`loops`属性的一些预定义常数。
- `QMediaPlayer::Infinite`：是`-1`;永远循环。
- `QMediaPlayer::Once`：`1`;播放一次媒体（默认播放）。

### `enum QMediaPlayer::MediaStatus`

**作用与语义：**

定义媒体播放器当前媒体的状态。
- `QMediaPlayer::NoMedia`：`0`;没有当前媒体。玩家在`StoppedState`中。
- `QMediaPlayer::LoadingMedia`：`1`;当前媒体正在加载中。播放器可以处于任何状态。
- `QMediaPlayer::LoadedMedia`：`2`;当前媒体已加载。播放器在`StoppedState`中。
- `QMediaPlayer::StalledMedia`：`3`;当前媒体的播放因缓冲不足或其他暂时中断而停滞。播放器处于`PlayingState`或 `PausedState`。
- `QMediaPlayer::BufferingMedia`：`4`;播放器正在缓冲数据，但已缓冲足够播放以维持近期播放。播放器处于 `PlayingState` 或 `PausedState`。
- `QMediaPlayer::BufferedMedia`：`5`;播放器已完全缓冲当前媒体。播放器处于`PlayingState`或`PausedState`。
- `QMediaPlayer::EndOfMedia`：`6`;播放已结束当前媒体。玩家处于`StoppedState`中。
- `QMediaPlayer::InvalidMedia`：`7`;当前媒体无法播放。播放器处于`StoppedState`中。

### `[since 6.10] enum class QMediaPlayer::PitchCompensationAvailability`

**作用与语义：**

音高补偿的可用性。
不同后端在改变播放速率时，关于音高补偿的行为各不相同。
- `QMediaPlayer::PitchCompensationAvailability::AlwaysOn`：`0`;媒体播放器始终在进行音高补偿。
- `QMediaPlayer::PitchCompensationAvailability::Available`：`1`;媒体播放器可以配置为使用音高补偿。如果当前平台上支持音高补偿，默认启用，但用户可按需关闭。
- `QMediaPlayer::PitchCompensationAvailability::Unavailable`：`2`;媒体播放器无法在当前平台上进行投球补偿。
这个枚举是在Qt 6.10引入的。

### `enum QMediaPlayer::PlaybackState`

**作用与语义：**

定义了媒体播放器的当前状态。
- `QMediaPlayer::StoppedState`：`0`;媒体播放器不会播放内容，播放将从当前曲目开始。
- `QMediaPlayer::PlayingState`：`1`;媒体播放器当前正在播放内容。这表示与`playing`属性相同。
- `QMediaPlayer::PausedState`：`2`;媒体播放器暂停播放，当前曲目播放将从暂停位置继续播放。

### `activeAudioTrack : int`

**作用与语义：**

返回当前活跃的音频轨道。
默认情况下，会选择第一个可用的音轨。
把`index`设为`-1`以禁用所有音轨。

**如何使用：** 调用 `activeAudioTrack()` 读取当前值；它不会修改应用状态。

### `activeSubtitleTrack : int`

**作用与语义：**

返回当前活跃的字幕轨。
将`index`设置为`-1`以禁用字幕。
字幕默认是关闭的。

**如何使用：** 调用 `activeSubtitleTrack()` 读取当前值；它不会修改应用状态。

### `activeVideoTrack : int`

**作用与语义：**

返回当前活跃的视频轨道。
默认情况下，会选择第一个可用的音轨。
把`index`设为`-1`以禁用所有视频轨道。

**如何使用：** 调用 `activeVideoTrack()` 读取当前值；它不会修改应用状态。

### `[since 6.8] audioBufferOutput : QAudioBufferOutput*`

**作用与语义：**

该属性包含媒体播放器使用的输出音频缓冲区。
设置一个音频缓冲区`output`媒体播放器。
如果指定`QAudioBufferOutput`且媒体源包含音频流，即媒体播放器，它会发出带有音频缓冲区的信号`QAudioBufferOutput::audioBufferReceived`，里面包含解码音频数据。在音频流结束时，`QMediaPlayer`会发出一个空的`QAudioBuffer`。
如果指定了音频缓冲，`QMediaPlayer`会在将匹配数据推送到音频输出的同时发出音频缓冲区。不过，由于音频缓冲，声音可以以较小的延迟播放。
发射音频缓冲区的格式取自指定`output`，或如果`output`返回无效格式，则取自匹配音频流。发射音频数据不会根据当前播放速率进行调整。
利用`QAudioBufferOutput`配合`QMediaPlayer`的潜在用例可能包括：
- 音频可视化。如果媒体播放器的播放速率不`1`，你可以根据可视化工具的需求调整输出图像尺寸或图像更新间隔。
- 任何人工智能声音处理，例如语音识别。
- 将数据发送到外部音频输出。应考虑播放速率变化、与视频同步以及停止和寻址时手动冲入。除非有充分理由，否则我们不建议使用音频缓冲输出。

**如何使用：** 调用 `audioBufferOutput()` 读取当前值；它不会修改应用状态。

### `audioOutput : QAudioOutput*`

**作用与语义：**

该属性包含媒体播放器使用的音频输出设备。
播放媒体时使用的当前音频输出。设置新的音频输出将替换当前使用的输出。
将此属性设置为`nullptr`会禁用任何音频输出。

**如何使用：** 调用 `audioOutput()` 读取当前值；它不会修改应用状态。

### `[read-only] audioTracks : QList<QMediaMetaData>`

**作用与语义：**

列出媒体中可用的音频轨道集合。
返回的`QMediaMetaData`描述了单个轨道的属性。
不同的音轨可以包含不同语言的音频。

**如何使用：** 调用 `audioTracks()` 读取当前值；它不会修改应用状态。

### `[read-only] bufferProgress : float`

**作用与语义：**

该属性保留播放开始或恢复前临时缓冲区被填满的百分比，范围从`0`。（空）到`1`。（满）。
当播放器对象缓冲时;该属性保留临时缓冲区中被填充的百分比。缓冲区需要达到100%才能开始或恢复播放，届时`mediaStatus()`返回`BufferedMedia`或`BufferingMedia`。如果值低于`100`，`mediaStatus()`返回`StalledMedia`。

**如何使用：** 调用 `bufferProgress()` 读取当前值；它不会修改应用状态。

### `[read-only] duration : qint64`

**作用与语义：**

该特性保持当前媒体的持续时间。
该值是当前媒体的总播放时间（以毫秒计）。该值可能在`QMediaPlayer`对象的生命周期内变化，且在初始播放开始时可能无法使用，连接`durationChanged()`信号以接收状态通知。

**如何使用：** 调用 `duration()` 读取当前值；它不会修改应用状态。

### `[read-only] error : Error`

**作用与语义：**

该属性包含描述最后错误条件的字符串。

**如何使用：** 调用 `error()` 读取当前值；它不会修改应用状态。

### `[read-only] errorString : QString`

**作用与语义：**

该属性包含一个字符串，详细描述当前错误状况。

**如何使用：** 调用 `errorString()` 读取当前值；它不会修改应用状态。

### `[read-only] hasAudio : bool`

**作用与语义：**

该属性决定介质是否包含音频。

**如何使用：** 调用 `hasAudio()` 读取当前值；它不会修改应用状态。

### `[read-only] hasVideo : bool`

**作用与语义：**

该属性决定介质是否包含视频。

**如何使用：** 调用 `hasVideo()` 读取当前值；它不会修改应用状态。

### `loops : int`

**作用与语义：**

决定播放器停止前媒体播放的频率。设置为`QMediaPlayer::Infinite`以永久循环当前媒体文件。
默认值是`1`。将该属性设置为`0`没有影响。

**如何使用：** 调用 `loops()` 读取当前值；它不会修改应用状态。

### `[read-only] mediaStatus : MediaStatus`

**作用与语义：**

该属性表示当前媒体流的状态。
流状态描述当前流的播放进展。
默认情况下，该属性`QMediaPlayer::NoMedia`。

**如何使用：** 调用 `mediaStatus()` 读取当前值；它不会修改应用状态。

### `[read-only] metaData : QMediaMetaData`

**作用与语义：**

返回当前媒体播放器使用的元数据。
元数据可以包含视频标题或创建日期等信息。
注意：Windows 实现仅提供位于本地文件系统的媒体元数据。

**如何使用：** 调用 `metaData()` 读取当前值；它不会修改应用状态。

### `[since 6.10] pitchCompensation : bool`

**作用与语义：**

该属性具有媒体播放器的投球补偿状态。
表示是否启用了音高补偿。启用后，改变播放速率不会影响音频信号的音高。
注意：音高补偿会增加`QMediaPlayer`的CPU负载。
默认情况下，如果有投球补偿，`true`，否则`false`。

**如何使用：** 调用 `pitchCompensation()` 读取当前值；它不会修改应用状态。

### `[read-only, since 6.10] pitchCompensationAvailability : const PitchCompensationAvailability`

**作用与语义：**

该特性保留了当前`QtMultimedia`后端的俯仰补偿可用性。
表示当前后端`QMediaPlayer`具备音高补偿功能。
注意：不同的后端可能有不同的行为。
更多信息请参见`QMediaPlayer::PitchCompensationAvailability`。

**如何使用：** 调用 `pitchCompensationAvailability()` 读取当前值；它不会修改应用状态。

### `[since 6.10] playbackOptions : QPlaybackOptions`

**作用与语义：**

用于配置媒体播放和解码的高级播放选项。
该特性揭示了`QPlaybackOptions` API，提供对媒体播放选项的低层控制。虽然我们强烈建议依赖`QMediaPlayer`的默认设置，但该API可用于针对默认选项不理想的特定场景优化媒体播放。
播放选项在下次`QMediaPlayer::setSource()`被调用时生效。

**如何使用：** 调用 `playbackOptions()` 读取当前值；它不会修改应用状态。

### `playbackRate : qreal`

**作用与语义：**

该属性表示当前媒体的播放速率。
该值是加诸于媒体标准播放速率的乘数。默认情况下，该值为1.0，表示媒体以标准速度播放。高于1.0的数值会提高播放速度，而0.0到1.0之间的数值则播放速度变慢。不支持负播放率。
并非所有播放服务都支持播放速率的变更。这是一个框架，用于快速或倒带时音频和视频的状态和质量。

**如何使用：** 调用 `playbackRate()` 读取当前值；它不会修改应用状态。

### `[read-only] playbackState : PlaybackState`

**作用与语义：**

还给`PlaybackState`。

**如何使用：** 调用 `playbackState()` 读取当前值；它不会修改应用状态。

### `[read-only, since 6.5] playing : bool`

**作用与语义：**

该属性决定媒体是否在播放。

**如何使用：** 调用 `playing()` 读取当前值；它不会修改应用状态。

### `position : qint64`

**作用与语义：**

该属性表示当前媒体的播放位置。
该值为当前播放位置，单位为毫秒，自媒体开始以来。位置的变化会定期用`positionChanged()`信号显示。
如果`seekable`属性为真，则该属性可设置为毫秒级。

**如何使用：** 调用 `position()` 读取当前值；它不会修改应用状态。

### `[read-only] seekable : bool`

**作用与语义：**

该属性具有当前媒体的是否可跳转的状态。
如果支持寻址，该属性为真;否则为假。该属性的状态在`QMediaPlayer`对象的生命周期内可能会变化，请使用`seekableChanged`信号监控变化。

**如何使用：** 调用 `seekable()` 读取当前值；它不会修改应用状态。

### `source : QUrl`

**作用与语义：**

该属性包含播放器对象正在使用的活动媒体源。
玩家对象会使用`QUrl`来选择要播放的内容。
默认情况下，该属性具有空的 `QUrl`。
将该属性设置为空`QUrl`会使播放器丢弃所有与当前媒体源相关的信息，并停止所有与该媒体相关的I/O操作。

**如何使用：** 调用 `source()` 读取当前值；它不会修改应用状态。

### `[read-only] subtitleTracks : QList<QMediaMetaData>`

**作用与语义：**

列出媒体中可用的字幕轨道集合。
返回的 `QMediaMetaData` 描述了单个轨道的属性。

**如何使用：** 调用 `subtitleTracks()` 读取当前值；它不会修改应用状态。

### `videoOutput : QObject*`

**作用与语义：**

该属性包含媒体播放器将使用的视频输出。
媒体播放器只能连接一个视频输出，因此设置该属性将取代之前连接的视频输出。
将该属性设置为`nullptr`会禁用视频输出。

**如何使用：** 调用 `videoOutput()` 读取当前值；它不会修改应用状态。

### `[read-only] videoTracks : QList<QMediaMetaData>`

**作用与语义：**

列出媒体中可用的视频轨道集合。
返回的`QMediaMetaData`描述了单个轨道的特性。

**如何使用：** 调用 `videoTracks()` 读取当前值；它不会修改应用状态。

### `[explicit] QMediaPlayer::QMediaPlayer(QObject *parent = nullptr)`

**作用与语义：**

构建一个QMediaPlayer实例，作为`parent`的子实例。

### `[override virtual noexcept] QMediaPlayer::~QMediaPlayer()`

**作用与语义：**

摧毁玩家的物品。

### `float QMediaPlayer::bufferProgress() const`

**作用与语义：**

缓冲数据时返回0到1之间的数字。
0表示没有缓冲数据可用，此时播放通常会被暂停。当缓冲区达到1时播放会继续，表示缓冲区已缓冲足够，可以继续播放。
bufferProgress() 对本地文件总是返回 1。
注意：属性缓冲区的获取函数。

### `[signal] void QMediaPlayer::bufferProgressChanged(float filled)`

**作用与语义：**

该属性保留播放开始或恢复前临时缓冲区被填满的百分比，范围从`0`。（空）到`1`。（满）。
当播放器对象缓冲时;该属性保留临时缓冲区中被填充的百分比。缓冲区需要达到100%才能开始或恢复播放，届时`mediaStatus()`返回`BufferedMedia`或`BufferingMedia`。如果值低于`100`，`mediaStatus()`返回`StalledMedia`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `bufferProgress` 的变化，不要把它当作普通函数主动调用。

### `QMediaTimeRange QMediaPlayer::bufferedTimeRange() const`

**作用与语义：**

返回描述当前缓冲数据的`QMediaTimeRange`。
当从远程源流媒体时，媒体文件的不同部分可以在本地获取。返回的 `QMediaTimeRange` 对象描述了缓冲并可立即播放的时间范围。

### `qint64 QMediaPlayer::duration() const`

**作用与语义：**

返回当前媒体的时长（毫秒）。
如果媒体播放器没有有效的媒体文件或流，则返回0。对于直播流，随着更多数据的增加，播放时长通常会变化。
注意：属性持续时间的获取函数。

### `[signal] void QMediaPlayer::durationChanged(qint64 duration)`

**作用与语义：**

该特性保持当前媒体的持续时间。
该值是当前媒体的总播放时间（以毫秒计）。该值可能在`QMediaPlayer`对象的生命周期内变化，且在初始播放开始时可能无法使用，连接`durationChanged()`信号以接收状态通知。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `duration` 的变化，不要把它当作普通函数主动调用。

### `QMediaPlayer::Error QMediaPlayer::error() const`

**作用与语义：**

返回当前错误状态。
注意：属性错误时使用获取函数。

### `[signal] void QMediaPlayer::errorOccurred(QMediaPlayer::Error error, const QString &errorString)`

**作用与语义：**

表示发生了`error`条件，`errorString`包含错误的描述。

### `[signal] void QMediaPlayer::hasAudioChanged(bool available)`

**作用与语义：**

该属性决定介质是否包含音频。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `hasAudio` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QMediaPlayer::hasVideoChanged(bool videoAvailable)`

**作用与语义：**

该属性决定介质是否包含视频。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `hasVideo` 的变化，不要把它当作普通函数主动调用。

### `bool QMediaPlayer::isAvailable() const`

**作用与语义：**

如果媒体播放器支持该平台，则返回为真。

### `bool QMediaPlayer::isSeekable() const`

**作用与语义：**

该属性具有当前媒体的是否可跳转的状态。
如果支持寻址，该属性为真;否则为假。该属性的状态在`QMediaPlayer`对象的生命周期内可能会变化，请使用`seekableChanged`信号监控变化。

**如何使用：** 调用 `isSeekable()` 读取当前值；它不会修改应用状态。

### `[signal] void QMediaPlayer::mediaStatusChanged(QMediaPlayer::MediaStatus status)`

**作用与语义：**

该属性表示当前媒体流的状态。
流状态描述当前流的播放进展。
默认情况下，该属性`QMediaPlayer::NoMedia`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `mediaStatus` 的变化，不要把它当作普通函数主动调用。

### `[slot] void QMediaPlayer::pause()`

**作用与语义：**

暂停播放当前的源头。

### `[since 6.10] bool QMediaPlayer::pitchCompensation() const`

**作用与语义：**

返回音高补偿状态。
注意：属性 pitchCompensation 的 getter 函数。

### `[since 6.10] QMediaPlayer::PitchCompensationAvailability QMediaPlayer::pitchCompensationAvailability() const`

**作用与语义：**

当前后端的投高补偿的回报。
注意：房产投球的获取功能薪酬可用性。

### `[slot] void QMediaPlayer::play()`

**作用与语义：**

开始或继续播放当前的源代码。

### `qreal QMediaPlayer::playbackRate() const`

**作用与语义：**

返回当前播放速率。
注意：属性播放速率的获取函数。

### `[signal] void QMediaPlayer::playbackRateChanged(qreal rate)`

**作用与语义：**

该属性表示当前媒体的播放速率。
该值是加诸于媒体标准播放速率的乘数。默认情况下，该值为1.0，表示媒体以标准速度播放。高于1.0的数值会提高播放速度，而0.0到1.0之间的数值则播放速度变慢。不支持负播放率。
并非所有播放服务都支持播放速率的变更。这是一个框架，用于快速或倒带时音频和视频的状态和质量。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `playbackRate` 的变化，不要把它当作普通函数主动调用。

### `qint64 QMediaPlayer::position() const`

**作用与语义：**

返回正在播放的媒体的当前位置（以毫秒为单位）。
如果媒体播放器没有有效的媒体文件或流，则返回0。对于直播流，随着更多数据可用，播放期间持续时间通常会发生变化。
注意：属性 position 的获取函数。

### `[signal] void QMediaPlayer::positionChanged(qint64 position)`

**作用与语义：**

该属性表示当前媒体的播放位置。
该值为当前播放位置，单位为毫秒，自媒体开始以来。位置的变化会定期用`positionChanged()`信号显示。
如果`seekable`属性为真，则该属性可设置为毫秒级。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `position` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QMediaPlayer::seekableChanged(bool seekable)`

**作用与语义：**

该属性具有当前媒体的是否可跳转的状态。
如果支持寻址，该属性为真;否则为假。该属性的状态在`QMediaPlayer`对象的生命周期内可能会变化，请使用`seekableChanged`信号监控变化。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `seekable` 的变化，不要把它当作普通函数主动调用。

### `[slot, since 6.10] void QMediaPlayer::setPitchCompensation(bool enabled) const`

**作用与语义：**

该属性具有媒体播放器的投球补偿状态。
表示是否启用了音高补偿。启用后，改变播放速率不会影响音频信号的音高。
注意：音高补偿会增加`QMediaPlayer`的CPU负载。
默认情况下，如果有投球补偿，`true`，否则`false`。

**如何使用：** 调用 `setPitchCompensation(...)` 修改 `pitchCompensation`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `[slot] void QMediaPlayer::setSource(const QUrl &source)`

**作用与语义：**

该属性包含播放器对象正在使用的活动媒体源。
玩家对象会使用`QUrl`来选择要播放的内容。
默认情况下，该属性具有空的 `QUrl`。
将该属性设置为空`QUrl`会使播放器丢弃所有与当前媒体源相关的信息，并停止所有与该媒体相关的I/O操作。

**如何使用：** 调用 `setSource(...)` 修改 `source`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `[slot] void QMediaPlayer::setSourceDevice(QIODevice *device, const QUrl &sourceUrl = QUrl())`

**作用与语义：**

设定电流源`device`。
媒体数据将从`device`读取。`sourceUrl`可用于解析媒体、哑剧类型等额外信息。`device`必须开放且可读。
对于macOS，`device`也应该是可寻的。
注意：该功能在录制指定媒体源后立即返回。它不会等待媒体加载完成，也不会检查错误。在媒体加载时，请监听`mediaStatusChanged()`和`error()`信号，以便在加载过程中出现错误时通知。

### `void QMediaPlayer::setVideoSink(QVideoSink *sink)`

**作用与语义：**

将`sink`设置为`QVideoSink`实例来获取视频数据。

### `[signal] void QMediaPlayer::sourceChanged(const QUrl &media)`

**作用与语义：**

该属性包含播放器对象正在使用的活动媒体源。
玩家对象会使用`QUrl`来选择要播放的内容。
默认情况下，该属性具有空的 `QUrl`。
将该属性设置为空`QUrl`会使播放器丢弃所有与当前媒体源相关的信息，并停止所有与该媒体相关的I/O操作。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `source` 的变化，不要把它当作普通函数主动调用。

### `const QIODevice *QMediaPlayer::sourceDevice() const`

**作用与语义：**

返回媒体数据的流源。
这仅在流传递给`setSource()`时有效。

### `[slot] void QMediaPlayer::stop()`

**作用与语义：**

停止演奏，重置游戏位置到起点。

### `QVideoSink *QMediaPlayer::videoSink() const`

**作用与语义：**

返回`QVideoSink`实例。

### `int activeAudioTrack() const`

**作用与语义：**

返回当前活跃的音频轨道。
默认情况下，会选择第一个可用的音轨。
把`index`设为`-1`以禁用所有音轨。

**如何使用：** 调用 `activeAudioTrack()` 读取当前值；它不会修改应用状态。

### `int activeSubtitleTrack() const`

**作用与语义：**

返回当前活跃的字幕轨。
将`index`设置为`-1`以禁用字幕。
字幕默认是关闭的。

**如何使用：** 调用 `activeSubtitleTrack()` 读取当前值；它不会修改应用状态。

### `int activeVideoTrack() const`

**作用与语义：**

返回当前活跃的视频轨道。
默认情况下，会选择第一个可用的音轨。
把`index`设为`-1`以禁用所有视频轨道。

**如何使用：** 调用 `activeVideoTrack()` 读取当前值；它不会修改应用状态。

### `QAudioBufferOutput * audioBufferOutput() const`

**作用与语义：**

该属性包含媒体播放器使用的输出音频缓冲区。
设置一个音频缓冲区`output`媒体播放器。
如果指定`QAudioBufferOutput`且媒体源包含音频流，即媒体播放器，它会发出带有音频缓冲区的信号`QAudioBufferOutput::audioBufferReceived`，里面包含解码音频数据。在音频流结束时，`QMediaPlayer`会发出一个空的`QAudioBuffer`。
如果指定了音频缓冲，`QMediaPlayer`会在将匹配数据推送到音频输出的同时发出音频缓冲区。不过，由于音频缓冲，声音可以以较小的延迟播放。
发射音频缓冲区的格式取自指定`output`，或如果`output`返回无效格式，则取自匹配音频流。发射音频数据不会根据当前播放速率进行调整。
利用`QAudioBufferOutput`配合`QMediaPlayer`的潜在用例可能包括：
- 音频可视化。如果媒体播放器的播放速率不`1`，你可以根据可视化工具的需求调整输出图像尺寸或图像更新间隔。
- 任何人工智能声音处理，例如语音识别。
- 将数据发送到外部音频输出。应考虑播放速率变化、与视频同步以及停止和寻址时手动冲入。除非有充分理由，否则我们不建议使用音频缓冲输出。

**如何使用：** 调用 `audioBufferOutput()` 读取当前值；它不会修改应用状态。

### `QAudioOutput * audioOutput() const`

**作用与语义：**

该属性包含媒体播放器使用的音频输出设备。
播放媒体时使用的当前音频输出。设置新的音频输出将替换当前使用的输出。
将此属性设置为`nullptr`会禁用任何音频输出。

**如何使用：** 调用 `audioOutput()` 读取当前值；它不会修改应用状态。

### `QList<QMediaMetaData> audioTracks() const`

**作用与语义：**

列出媒体中可用的音频轨道集合。
返回的`QMediaMetaData`描述了单个轨道的属性。
不同的音轨可以包含不同语言的音频。

**如何使用：** 调用 `audioTracks()` 读取当前值；它不会修改应用状态。

### `QString errorString() const`

**作用与语义：**

该属性包含一个字符串，详细描述当前错误状况。

**如何使用：** 调用 `errorString()` 读取当前值；它不会修改应用状态。

### `bool hasAudio() const`

**作用与语义：**

该属性决定介质是否包含音频。

**如何使用：** 调用 `hasAudio()` 读取当前值；它不会修改应用状态。

### `bool hasVideo() const`

**作用与语义：**

该属性决定介质是否包含视频。

**如何使用：** 调用 `hasVideo()` 读取当前值；它不会修改应用状态。

### `bool isPlaying() const`

**作用与语义：**

该属性决定媒体是否在播放。

**如何使用：** 调用 `isPlaying()` 读取当前值；它不会修改应用状态。

### `int loops() const`

**作用与语义：**

决定播放器停止前媒体播放的频率。设置为`QMediaPlayer::Infinite`以永久循环当前媒体文件。
默认值是`1`。将该属性设置为`0`没有影响。

**如何使用：** 调用 `loops()` 读取当前值；它不会修改应用状态。

### `QMediaPlayer::MediaStatus mediaStatus() const`

**作用与语义：**

该属性表示当前媒体流的状态。
流状态描述当前流的播放进展。
默认情况下，该属性`QMediaPlayer::NoMedia`。

**如何使用：** 调用 `mediaStatus()` 读取当前值；它不会修改应用状态。

### `QMediaMetaData metaData() const`

**作用与语义：**

返回当前媒体播放器使用的元数据。
元数据可以包含视频标题或创建日期等信息。
注意：Windows 实现仅提供位于本地文件系统的媒体元数据。

**如何使用：** 调用 `metaData()` 读取当前值；它不会修改应用状态。

### `QPlaybackOptions playbackOptions() const`

**作用与语义：**

用于配置媒体播放和解码的高级播放选项。
该特性揭示了`QPlaybackOptions` API，提供对媒体播放选项的低层控制。虽然我们强烈建议依赖`QMediaPlayer`的默认设置，但该API可用于针对默认选项不理想的特定场景优化媒体播放。
播放选项在下次`QMediaPlayer::setSource()`被调用时生效。

**如何使用：** 调用 `playbackOptions()` 读取当前值；它不会修改应用状态。

### `QMediaPlayer::PlaybackState playbackState() const`

**作用与语义：**

还给`PlaybackState`。

**如何使用：** 调用 `playbackState()` 读取当前值；它不会修改应用状态。

### `void setActiveAudioTrack(int index)`

**作用与语义：**

返回当前活跃的音频轨道。
默认情况下，会选择第一个可用的音轨。
把`index`设为`-1`以禁用所有音轨。

**如何使用：** 调用 `setActiveAudioTrack(...)` 修改 `activeAudioTrack`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setActiveSubtitleTrack(int index)`

**作用与语义：**

返回当前活跃的字幕轨。
将`index`设置为`-1`以禁用字幕。
字幕默认是关闭的。

**如何使用：** 调用 `setActiveSubtitleTrack(...)` 修改 `activeSubtitleTrack`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setActiveVideoTrack(int index)`

**作用与语义：**

返回当前活跃的视频轨道。
默认情况下，会选择第一个可用的音轨。
把`index`设为`-1`以禁用所有视频轨道。

**如何使用：** 调用 `setActiveVideoTrack(...)` 修改 `activeVideoTrack`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setAudioBufferOutput(QAudioBufferOutput *output)`

**作用与语义：**

该属性包含媒体播放器使用的输出音频缓冲区。
设置一个音频缓冲区`output`媒体播放器。
如果指定`QAudioBufferOutput`且媒体源包含音频流，即媒体播放器，它会发出带有音频缓冲区的信号`QAudioBufferOutput::audioBufferReceived`，里面包含解码音频数据。在音频流结束时，`QMediaPlayer`会发出一个空的`QAudioBuffer`。
如果指定了音频缓冲，`QMediaPlayer`会在将匹配数据推送到音频输出的同时发出音频缓冲区。不过，由于音频缓冲，声音可以以较小的延迟播放。
发射音频缓冲区的格式取自指定`output`，或如果`output`返回无效格式，则取自匹配音频流。发射音频数据不会根据当前播放速率进行调整。
利用`QAudioBufferOutput`配合`QMediaPlayer`的潜在用例可能包括：
- 音频可视化。如果媒体播放器的播放速率不`1`，你可以根据可视化工具的需求调整输出图像尺寸或图像更新间隔。
- 任何人工智能声音处理，例如语音识别。
- 将数据发送到外部音频输出。应考虑播放速率变化、与视频同步以及停止和寻址时手动冲入。除非有充分理由，否则我们不建议使用音频缓冲输出。

**如何使用：** 调用 `setAudioBufferOutput(...)` 修改 `audioBufferOutput`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setAudioOutput(QAudioOutput *output)`

**作用与语义：**

该属性包含媒体播放器使用的音频输出设备。
播放媒体时使用的当前音频输出。设置新的音频输出将替换当前使用的输出。
将此属性设置为`nullptr`会禁用任何音频输出。

**如何使用：** 调用 `setAudioOutput(...)` 修改 `audioOutput`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLoops(int loops)`

**作用与语义：**

决定播放器停止前媒体播放的频率。设置为`QMediaPlayer::Infinite`以永久循环当前媒体文件。
默认值是`1`。将该属性设置为`0`没有影响。

**如何使用：** 调用 `setLoops(...)` 修改 `loops`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setVideoOutput(QObject *)`

**作用与语义：**

该属性包含媒体播放器将使用的视频输出。
媒体播放器只能连接一个视频输出，因此设置该属性将取代之前连接的视频输出。
将该属性设置为`nullptr`会禁用视频输出。

**如何使用：** 调用 `setVideoOutput(...)` 修改 `videoOutput`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QUrl source() const`

**作用与语义：**

该属性包含播放器对象正在使用的活动媒体源。
玩家对象会使用`QUrl`来选择要播放的内容。
默认情况下，该属性具有空的 `QUrl`。
将该属性设置为空`QUrl`会使播放器丢弃所有与当前媒体源相关的信息，并停止所有与该媒体相关的I/O操作。

**如何使用：** 调用 `source()` 读取当前值；它不会修改应用状态。

### `QList<QMediaMetaData> subtitleTracks() const`

**作用与语义：**

列出媒体中可用的字幕轨道集合。
返回的 `QMediaMetaData` 描述了单个轨道的属性。

**如何使用：** 调用 `subtitleTracks()` 读取当前值；它不会修改应用状态。

### `QObject * videoOutput() const`

**作用与语义：**

该属性包含媒体播放器将使用的视频输出。
媒体播放器只能连接一个视频输出，因此设置该属性将取代之前连接的视频输出。
将该属性设置为`nullptr`会禁用视频输出。

**如何使用：** 调用 `videoOutput()` 读取当前值；它不会修改应用状态。

### `QList<QMediaMetaData> videoTracks() const`

**作用与语义：**

列出媒体中可用的视频轨道集合。
返回的`QMediaMetaData`描述了单个轨道的特性。

**如何使用：** 调用 `videoTracks()` 读取当前值；它不会修改应用状态。

### `void resetPlaybackOptions()`

**作用与语义：**

用于配置媒体播放和解码的高级播放选项。
该特性揭示了`QPlaybackOptions` API，提供对媒体播放选项的低层控制。虽然我们强烈建议依赖`QMediaPlayer`的默认设置，但该API可用于针对默认选项不理想的特定场景优化媒体播放。
播放选项在下次`QMediaPlayer::setSource()`被调用时生效。

**如何使用：** 调用 `resetPlaybackOptions()` 撤销对 `playbackOptions` 的显式覆盖，让它重新采用继承值或默认值。

### `void setPlaybackOptions(const QPlaybackOptions &options)`

**作用与语义：**

用于配置媒体播放和解码的高级播放选项。
该特性揭示了`QPlaybackOptions` API，提供对媒体播放选项的低层控制。虽然我们强烈建议依赖`QMediaPlayer`的默认设置，但该API可用于针对默认选项不理想的特定场景优化媒体播放。
播放选项在下次`QMediaPlayer::setSource()`被调用时生效。

**如何使用：** 调用 `setPlaybackOptions(...)` 修改 `playbackOptions`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPlaybackRate(qreal rate)`

**作用与语义：**

该属性表示当前媒体的播放速率。
该值是加诸于媒体标准播放速率的乘数。默认情况下，该值为1.0，表示媒体以标准速度播放。高于1.0的数值会提高播放速度，而0.0到1.0之间的数值则播放速度变慢。不支持负播放率。
并非所有播放服务都支持播放速率的变更。这是一个框架，用于快速或倒带时音频和视频的状态和质量。

**如何使用：** 调用 `setPlaybackRate(...)` 修改 `playbackRate`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPosition(qint64 position)`

**作用与语义：**

该属性表示当前媒体的播放位置。
该值为当前播放位置，单位为毫秒，自媒体开始以来。位置的变化会定期用`positionChanged()`信号显示。
如果`seekable`属性为真，则该属性可设置为毫秒级。

**如何使用：** 调用 `setPosition(...)` 修改 `position`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void activeTracksChanged()`

**作用与语义：**

返回当前活跃的音频轨道。
默认情况下，会选择第一个可用的音轨。
把`index`设为`-1`以禁用所有音轨。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `activeAudioTrack` 的变化，不要把它当作普通函数主动调用。

### `void audioBufferOutputChanged()`

**作用与语义：**

该属性包含媒体播放器使用的输出音频缓冲区。
设置一个音频缓冲区`output`媒体播放器。
如果指定`QAudioBufferOutput`且媒体源包含音频流，即媒体播放器，它会发出带有音频缓冲区的信号`QAudioBufferOutput::audioBufferReceived`，里面包含解码音频数据。在音频流结束时，`QMediaPlayer`会发出一个空的`QAudioBuffer`。
如果指定了音频缓冲，`QMediaPlayer`会在将匹配数据推送到音频输出的同时发出音频缓冲区。不过，由于音频缓冲，声音可以以较小的延迟播放。
发射音频缓冲区的格式取自指定`output`，或如果`output`返回无效格式，则取自匹配音频流。发射音频数据不会根据当前播放速率进行调整。
利用`QAudioBufferOutput`配合`QMediaPlayer`的潜在用例可能包括：
- 音频可视化。如果媒体播放器的播放速率不`1`，你可以根据可视化工具的需求调整输出图像尺寸或图像更新间隔。
- 任何人工智能声音处理，例如语音识别。
- 将数据发送到外部音频输出。应考虑播放速率变化、与视频同步以及停止和寻址时手动冲入。除非有充分理由，否则我们不建议使用音频缓冲输出。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `audioBufferOutput` 的变化，不要把它当作普通函数主动调用。

### `void audioOutputChanged()`

**作用与语义：**

该属性包含媒体播放器使用的音频输出设备。
播放媒体时使用的当前音频输出。设置新的音频输出将替换当前使用的输出。
将此属性设置为`nullptr`会禁用任何音频输出。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `audioOutput` 的变化，不要把它当作普通函数主动调用。

### `void errorChanged()`

**作用与语义：**

该属性包含描述最后错误条件的字符串。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `error` 的变化，不要把它当作普通函数主动调用。

### `void loopsChanged()`

**作用与语义：**

决定播放器停止前媒体播放的频率。设置为`QMediaPlayer::Infinite`以永久循环当前媒体文件。
默认值是`1`。将该属性设置为`0`没有影响。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `loops` 的变化，不要把它当作普通函数主动调用。

### `void metaDataChanged()`

**作用与语义：**

返回当前媒体播放器使用的元数据。
元数据可以包含视频标题或创建日期等信息。
注意：Windows 实现仅提供位于本地文件系统的媒体元数据。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `metaData` 的变化，不要把它当作普通函数主动调用。

### `void pitchCompensationChanged(bool)`

**作用与语义：**

该属性具有媒体播放器的投球补偿状态。
表示是否启用了音高补偿。启用后，改变播放速率不会影响音频信号的音高。
注意：音高补偿会增加`QMediaPlayer`的CPU负载。
默认情况下，如果有投球补偿，`true`，否则`false`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `pitchCompensation` 的变化，不要把它当作普通函数主动调用。

### `void playbackOptionsChanged()`

**作用与语义：**

用于配置媒体播放和解码的高级播放选项。
该特性揭示了`QPlaybackOptions` API，提供对媒体播放选项的低层控制。虽然我们强烈建议依赖`QMediaPlayer`的默认设置，但该API可用于针对默认选项不理想的特定场景优化媒体播放。
播放选项在下次`QMediaPlayer::setSource()`被调用时生效。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `playbackOptions` 的变化，不要把它当作普通函数主动调用。

### `void playbackStateChanged(QMediaPlayer::PlaybackState newState)`

**作用与语义：**

还给`PlaybackState`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `playbackState` 的变化，不要把它当作普通函数主动调用。

### `void playingChanged(bool playing)`

**作用与语义：**

该属性决定媒体是否在播放。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `playing` 的变化，不要把它当作普通函数主动调用。

### `void tracksChanged()`

**作用与语义：**

列出媒体中可用的音频轨道集合。
返回的`QMediaMetaData`描述了单个轨道的属性。
不同的音轨可以包含不同语言的音频。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `audioTracks` 的变化，不要把它当作普通函数主动调用。

### `void videoOutputChanged()`

**作用与语义：**

该属性包含媒体播放器将使用的视频输出。
媒体播放器只能连接一个视频输出，因此设置该属性将取代之前连接的视频输出。
将该属性设置为`nullptr`会禁用视频输出。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `videoOutput` 的变化，不要把它当作普通函数主动调用。

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

`QMediaPlayer` 所属机制类型：多媒体设备与会话机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
