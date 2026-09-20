# QMediaPlayer：异步播放音频和视频媒体

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMediaPlayer>`  
> 所属模块：`Qt6::Multimedia`  
> 继承：`QObject -> QMediaPlayer`  
> 类型性质：异步媒体播放器

## 它解决什么问题

`QMediaPlayer` 把“找到媒体资源、交给后端解码、按时间推进、把音频/视频送到输出设备”整合成一个高层播放器。应用不需要自己解析 MP4、MP3、HLS 等容器，也不需要手写解码线程和时钟同步。

它适合：

- 播放本地文件、网络 URL 或自定义 `QIODevice`；
- 播放音频并连接 `QAudioOutput`；
- 播放视频并连接 `QVideoWidget`、`QVideoSink` 或其它 Qt 视频输出；
- 获取当前位置、时长、缓冲范围、元数据和轨道列表；
- 做暂停、拖动、倍速、循环、语言轨道切换和字幕选择。

它不是一个“同步读取文件”的类。`setSource()` 和 `setSourceDevice()` 只提交新的媒体源，加载、探测、解码和错误报告在之后异步发生，必须通过信号观察进展。

## 最小播放骨架

```cpp
#include <QAudioOutput>
#include <QMediaPlayer>
#include <QUrl>

QMediaPlayer *player = new QMediaPlayer(this);
QAudioOutput *audioOutput = new QAudioOutput(this);

player->setAudioOutput(audioOutput);
connect(player, &QMediaPlayer::errorOccurred,
        this, [](QMediaPlayer::Error error, const QString &message) {
    qWarning() << error << message;
});
connect(player, &QMediaPlayer::mediaStatusChanged,
        this, [](QMediaPlayer::MediaStatus status) {
    qDebug() << status;
});

player->setSource(QUrl::fromLocalFile("/path/to/music.mp3"));
player->play();
```

`play()` 可以在源刚设置后调用，后端会在资源可用后开始播放；若希望界面先显示“已加载”，监听 `mediaStatusChanged()`，不要用 `setSource()` 的返回时机判断。

## 生命周期、所有权和线程

- `QMediaPlayer` 是 `QObject`，带 `parent` 构造时由父对象负责销毁；复制被禁用。
- `QAudioOutput`、`QVideoSink` 和 `QAudioBufferOutput` 是外部对象指针。设置它们表示连接输出，不应据此推断播放器取得了对象所有权。让这些对象至少存活到播放器不再使用它们。
- 播放器及其后端依赖事件循环处理异步加载、解码和通知。通常在 GUI 线程创建并使用；不要从其它线程直接读写同一个播放器。
- `sourceDevice()` 返回的是播放器当前使用的设备指针，应用仍须保证传入的 `QIODevice` 在整个使用期间保持有效、已打开且可读。播放器不会替应用延长设备生命周期。
- 关闭或销毁播放器会终止相关 I/O。切换源时，旧源的异步通知可能在切换附近到达，界面应以当前 `source()` 和最新状态为准。

## 播放状态和媒体状态不是一回事

`playbackState()` 表示用户控制下的播放动作：`StoppedState`、`PlayingState`、`PausedState`。`mediaStatus()` 表示当前媒体加载/缓冲/结束情况：`NoMedia`、`LoadingMedia`、`LoadedMedia`、`StalledMedia`、`BufferingMedia`、`BufferedMedia`、`EndOfMedia`、`InvalidMedia`。

例如：

- 媒体正在加载时，播放状态可能已经是 `PlayingState`；
- 网络不够快时，播放状态仍可能是 `PlayingState`，媒体状态变为 `StalledMedia`；
- 已加载但尚未播放通常是 `LoadedMedia + StoppedState`；
- 到达结尾通常先出现 `EndOfMedia`，循环策略决定是否重新开始。

错误要同时看 `errorOccurred(error, errorString)` 和 `error()` / `errorString()`。`FormatError` 不一定意味着完全不能播放，某些后端可能仍能播放其中一个流。

## 关键使用边界

### 源的异步加载

`setSource(QUrl())` 会清除当前媒体信息并停止与旧源有关的 I/O。普通 `setSource()` 不直接返回加载失败，错误通过 `errorOccurred()` 报告。

`setSourceDevice()` 的设备必须已经打开并可读；在 macOS 等平台，随机访问格式通常还要求设备可 seek。若同时提供 `sourceUrl`，它主要用于帮助后端判断格式和资源信息，并不替代设备本身。

### 时间和拖动

`duration()`、`position()` 和 `setPosition()` 的单位都是毫秒。时长在初次播放时可能尚未可用，也可能因流媒体探测而变化；连接 `durationChanged()`。

只有 `isSeekable()` 为 `true` 时才应把拖动条位置写回 `setPosition()`。直播或某些网络流不可 seek，强行设置位置可能无效。`positionChanged()` 是播放时钟通知，不保证每一个媒体帧都对应一次信号。

### 缓冲

`bufferProgress()` 是 0 到 1 的临时缓冲比例；本地文件通常直接为 1。网络媒体应结合 `bufferedTimeRange()` 和 `mediaStatus()`，不能只把 `bufferProgress() == 1` 当作整个文件已下载。

### 速率、循环和停止

`playbackRate()` 默认是 `1.0`。大于 1 加速，0 到 1 之间减速，负值不支持；后端未必支持所有速率，也未必保证快进/慢放时音视频质量。

`loops()` 默认是 `1`，`QMediaPlayer::Infinite` 为 `-1`。设置为 `0` 没有效果。`stop()` 后再次 `play()` 从当前媒体的开头开始，`pause()` 后 `play()` 从当前位置恢复。

### 音频、视频和自定义输出

一个播放器只能连接一个视频输出；`setVideoOutput(nullptr)` 禁用视频输出，换成另一个输出会替换旧输出。`setVideoSink()` 是直接连接 `QVideoSink` 的便捷接口，读取时用 `videoSink()`。

`setAudioOutput(nullptr)` 可禁用音频输出。音频输出对象负责音量、静音和设备等播放端控制，播放器负责把解码后的音频送过去。

Qt 6.8 起，`setAudioBufferOutput()` 可额外接收解码后的 `QAudioBuffer`，适合波形、音量计、语音分析等。音频流结束时会发出一个空 buffer；buffer 推送的时间与送往音频输出的解码数据大致对应，但扬声器实际播放可能有缓冲延迟，且 buffer 内容不会按播放速率重新缩放。

### 轨道

`audioTracks()`、`videoTracks()`、`subtitleTracks()` 返回每条轨道的 `QMediaMetaData`。默认音频和视频通常选择第一个可用轨道，字幕默认关闭。通过 `setActiveAudioTrack(-1)`、`setActiveVideoTrack(-1)` 或 `setActiveSubtitleTrack(-1)` 可以禁用对应类型。

轨道索引属于当前媒体。切换源后必须重新读取列表和索引，不能缓存旧源的索引。

### Qt 6.10 播放选项和音调补偿

`playbackOptions()` 中的选项是后端提示，不保证每个平台或每种编码器都支持。调用 `setPlaybackOptions()` 后，设置在下一次 `setSource()` 时生效，不应假定会立即改变当前已加载源。

`pitchCompensationAvailability()` 表示当前后端是否总是启用、可配置或不可用。启用 `pitchCompensation()` 后，改变播放速率时尽量保持音高，但会增加 CPU 负载；后端为 `AlwaysOn` 时，运行时开关不一定具有可见效果。

## 典型场景：视频播放与拖动条

```cpp
connect(player, &QMediaPlayer::durationChanged,
        this, [slider](qint64 duration) {
    slider->setRange(0, duration > 0 ? int(duration) : 0);
});

connect(player, &QMediaPlayer::positionChanged,
        this, [slider](qint64 position) {
    QSignalBlocker blocker(slider);
    slider->setValue(int(position));
});

connect(slider, &QSlider::sliderMoved,
        this, [player](int position) {
    if (player->isSeekable())
        player->setPosition(position);
});
```

## 成员类型

### `enum PlaybackState`

| 值 | 含义 |
| --- | --- |
| `StoppedState` | 当前没有播放，或已停止。 |
| `PlayingState` | 播放请求已处于播放状态；媒体仍可能因缓冲暂时停顿。 |
| `PausedState` | 暂停在当前位置。 |

### `enum MediaStatus`

| 值 | 含义 |
| --- | --- |
| `NoMedia` | 没有当前媒体，播放器处于停止状态。 |
| `LoadingMedia` | 正在加载当前媒体。 |
| `LoadedMedia` | 当前媒体已加载，通常处于停止状态。 |
| `StalledMedia` | 因缓冲不足或临时中断而停滞。 |
| `BufferingMedia` | 正在缓冲，但短期内有足够数据继续播放。 |
| `BufferedMedia` | 已有足够缓冲可播放。 |
| `EndOfMedia` | 已到达媒体结尾。 |
| `InvalidMedia` | 当前媒体无效或无法使用。 |

### `enum Error`

| 值 | 含义 |
| --- | --- |
| `NoError` | 没有错误。 |
| `ResourceError` | 无法解析或取得媒体资源。 |
| `FormatError` | 格式未完全支持，可能仍能播放其中一部分。 |
| `NetworkError` | 网络错误。 |
| `AccessDeniedError` | 没有播放该媒体所需的权限。 |

### `enum Loops`

| 值 | 含义 |
| --- | --- |
| `Infinite` | `-1`，无限循环。 |
| `Once` | `1`，播放一次，也是默认值。 |

### `enum class PitchCompensationAvailability`（Qt 6.10）

| 值 | 含义 |
| --- | --- |
| `AlwaysOn` | 当前后端始终启用音调补偿。 |
| `Available` | 支持运行时配置。 |
| `Unavailable` | 当前后端不支持。 |

## 逐项 API 说明

### 构造和析构

#### `QMediaPlayer(QObject *parent = nullptr)`

创建播放器；传入父对象后由父对象管理其生命周期。创建不代表已有媒体，也不会自动创建音频或视频输出。

#### `~QMediaPlayer()`

销毁播放器并结束其媒体后端和相关 I/O。外部输出对象仍由它们自己的所有者管理。

### 轨道和输出

#### `QList<QMediaMetaData> audioTracks() const`

返回当前媒体中的音频轨道描述。没有媒体、尚未完成探测或没有音频轨道时可能为空。

#### `QList<QMediaMetaData> videoTracks() const`

返回当前媒体中的视频轨道描述。列表只属于当前源。

#### `QList<QMediaMetaData> subtitleTracks() const`

返回当前媒体中的字幕轨道描述。字幕轨道存在不等于已经启用。

#### `int activeAudioTrack() const`

返回当前音频轨道索引；默认通常是第一个可用轨道，`-1` 表示禁用。

#### `int activeVideoTrack() const`

返回当前视频轨道索引；默认通常是第一个可用轨道，`-1` 表示禁用。

#### `int activeSubtitleTrack() const`

返回当前字幕轨道索引；默认是 `-1`，表示字幕关闭。

#### `void setActiveAudioTrack(int index)`

选择当前媒体的音频轨道；传 `-1` 禁用所有音频轨道。索引应来自最新的 `audioTracks()`。

#### `void setActiveVideoTrack(int index)`

选择视频轨道；传 `-1` 禁用所有视频轨道。视频输出对象仍可连接，但不会收到被禁用的轨道内容。

#### `void setActiveSubtitleTrack(int index)`

选择字幕轨道；传 `-1` 禁用字幕。

#### `void setAudioOutput(QAudioOutput *output)`

设置音频播放输出；传 `nullptr` 禁用音频输出。播放器连接该对象，不应假定取得其所有权。

#### `QAudioOutput *audioOutput() const`

返回当前音频输出指针；未设置时为 `nullptr`。

#### `void setAudioBufferOutput(QAudioBufferOutput *output)`（Qt 6.8）

设置接收解码音频 buffer 的输出对象。输出对象格式无效时，buffer 格式由媒体和解码器决定；音频结束时会收到空 buffer。

#### `QAudioBufferOutput *audioBufferOutput() const`（Qt 6.8）

返回当前音频 buffer 输出指针；未设置时为 `nullptr`。

#### `void setVideoOutput(QObject *output)`

设置视频输出。播放器只支持一个视频输出，新的输出会替换旧输出；`nullptr` 禁用视频输出。常见对象是 `QVideoWidget` 等带视频接收能力的 Qt 类型。

#### `QObject *videoOutput() const`

返回当前视频输出对象；没有连接输出时为 `nullptr`。

#### `void setVideoSink(QVideoSink *sink)`

直接设置 `QVideoSink` 作为视频输出。它与 `setVideoOutput()` 表达同一个输出槽位。

#### `QVideoSink *videoSink() const`

返回当前连接的 `QVideoSink`；若视频输出不是 `QVideoSink`，则返回 `nullptr`。

### 源和状态

#### `QUrl source() const`

返回当前媒体源 URL。默认是空 URL；用 `setSourceDevice()` 时可返回辅助用的 URL，而实际数据来自设备。

#### `const QIODevice *sourceDevice() const`

返回当前源设备指针。它是观察用指针，不转移设备所有权；设备必须由调用方保持有效。

#### `void setSource(const QUrl &source)`

提交新的 URL 源并启动异步加载。传空 URL 会清除媒体和相关 I/O；加载错误通过 `errorOccurred()` 报告。

#### `void setSourceDevice(QIODevice *device, const QUrl &sourceUrl = QUrl())`

使用已经打开且可读的 `QIODevice` 作为媒体源。设备在播放器使用完之前不能销毁或关闭；某些平台/格式还要求可 seek。`sourceUrl` 用于提供格式或资源提示。

#### `PlaybackState playbackState() const`

返回停止、播放或暂停状态。它描述播放控制状态，不等同于媒体是否已加载或当前是否正在缓冲。

#### `MediaStatus mediaStatus() const`

返回当前媒体状态。默认是 `NoMedia`；异步加载和播放过程中可能多次变化。

#### `bool isAvailable() const`

返回媒体播放器服务是否可用。它只说明后端服务是否可使用，不保证任意 URL、编解码器或设备都支持。

#### `QMediaMetaData metaData() const`

返回当前媒体元数据。数据可能要等加载/探测完成后才完整；Windows 实现对本地文件有额外限制。

#### `Error error() const`

返回最近的播放器错误类型。错误发生后应结合 `errorString()` 记录上下文。

#### `QString errorString() const`

返回当前错误的详细描述。字符串适合日志或界面展示，不应拿来做程序逻辑判断。

### 时间、缓冲和内容

#### `qint64 duration() const`

返回当前媒体总时长，单位毫秒。尚未探测完成、无效媒体或直播等场景可能返回 0 或动态变化。

#### `qint64 position() const`

返回当前播放位置，单位毫秒。播放时通过 `positionChanged()` 观察。

#### `void setPosition(qint64 position)`

请求跳转到指定毫秒位置。仅在 `isSeekable()` 为真时有可靠语义；后端可能把位置调整到可用关键帧或其它边界。

#### `float bufferProgress() const`

返回临时缓冲比例，范围 0 到 1。本地文件通常为 1；不要把它解释为网络文件下载百分比。

#### `QMediaTimeRange bufferedTimeRange() const`

返回当前已缓冲的时间区间集合。对不连续的网络缓冲比单一比例更有信息，时间单位与播放器位置相同，通常是毫秒。

#### `bool hasAudio() const`

返回当前媒体是否包含可识别的音频内容；探测完成前结果可能尚未稳定。

#### `bool hasVideo() const`

返回当前媒体是否包含可识别的视频内容；不代表已经连接视频输出。

#### `bool isSeekable() const`

返回当前媒体是否支持 seek。直播和部分顺序网络流通常为 `false`，状态可能随源改变。

#### `bool isPlaying() const`

返回播放器是否处于播放状态，等价于播放状态为 `PlayingState` 的便捷查询。

### 速率、循环和 Qt 6.10 选项

#### `qreal playbackRate() const`

返回播放速率倍率，默认 `1.0`。

#### `void setPlaybackRate(qreal rate)`

设置播放速率。负数不支持；后端可能忽略不支持的倍率，实际变化通过 `playbackRateChanged()` 观察。

#### `int loops() const`

返回播放次数配置。默认 `1`，无限循环为 `-1`。

#### `void setLoops(int loops)`

设置播放次数；`QMediaPlayer::Infinite` 表示无限循环，`0` 无效果。设置不会改变已经结束的媒体源本身。

#### `PitchCompensationAvailability pitchCompensationAvailability() const`（Qt 6.10）

返回当前媒体后端对音调补偿的支持能力。不同后端的行为不同。

#### `bool pitchCompensation() const`（Qt 6.10）

返回是否启用音调补偿。默认在可用时通常为 `true`，不可用时为 `false`。

#### `void setPitchCompensation(bool enabled) const`（Qt 6.10）

请求启用或关闭音调补偿。启用可能增加 CPU 负载；不可用后端会忽略该请求。

#### `QPlaybackOptions playbackOptions() const`（Qt 6.10）

返回当前高级播放选项值。它是值类型，修改副本不会自动回写播放器。

#### `void setPlaybackOptions(const QPlaybackOptions &options)`（Qt 6.10）

设置解码/播放提示。选项在下一次 `setSource()` 时生效，且可能被后端忽略。

#### `void resetPlaybackOptions()`（Qt 6.10）

恢复默认播放选项；同样要在下一次设置源时才对新媒体生效。

### 播放控制槽

#### `void play()`

请求播放当前源。加载、解码和实际输出是异步的；没有有效源时不会产生正常播放。

#### `void pause()`

请求暂停并保留当前位置。后端不支持暂停的特殊媒体可能表现不同，应观察 `playbackStateChanged()`。

#### `void stop()`

停止播放并回到停止状态；之后再次 `play()` 从当前媒体开头开始。

### 信号

#### `sourceChanged(const QUrl &media)`

当前源 URL 改变时发出。

#### `playbackStateChanged(PlaybackState newState)`

播放控制状态改变时发出。

#### `mediaStatusChanged(MediaStatus status)`

媒体加载、缓冲、结束或失效状态改变时发出。

#### `durationChanged(qint64 duration)`

媒体时长可用或发生变化时发出。

#### `positionChanged(qint64 position)`

播放位置推进或跳转时发出，单位毫秒。

#### `hasAudioChanged(bool available)` / `hasVideoChanged(bool videoAvailable)`

当前媒体的音频/视频可用性发生变化时发出。

#### `bufferProgressChanged(float progress)`

临时缓冲比例变化时发出。

#### `seekableChanged(bool seekable)`

当前媒体是否可 seek 发生变化时发出。

#### `playingChanged(bool playing)`

播放布尔状态改变时发出，适合直接绑定播放按钮状态。

#### `playbackRateChanged(qreal rate)`

后端接受的播放速率改变时发出。

#### `loopsChanged()`

循环次数配置改变时发出。

#### `metaDataChanged()`

当前媒体元数据改变时发出。

#### `videoOutputChanged()` / `audioOutputChanged()`

视频或音频输出对象改变时发出。

#### `audioBufferOutputChanged()`（Qt 6.8）

音频 buffer 输出对象改变时发出。

#### `tracksChanged()`

音频、视频或字幕轨道列表改变时发出。

#### `activeTracksChanged()`

当前选中的音频、视频或字幕轨道改变时发出。

#### `errorChanged()`

错误状态或错误描述改变时发出。

#### `errorOccurred(Error error, const QString &errorString)`

发生错误时发出；这是最适合记录一次错误事件的信号。

#### `pitchCompensationChanged(bool)`（Qt 6.10）

音调补偿开关状态改变时发出。

#### `playbackOptionsChanged()`（Qt 6.10）

高级播放选项值改变时发出。

## 常见误区

- 把 `setSource()` 返回当作“媒体已加载”；应监听 `mediaStatusChanged()`。
- 只监听 `errorChanged()` 而不读取 `errorOccurred()` 的错误文本。
- 未判断 `isSeekable()` 就用拖动条反复调用 `setPosition()`。
- 把 `duration()` 的毫秒和 `QVideoFrame` 时间戳的微秒混用。
- 把 `bufferProgress()` 当作整个网络文件的下载百分比。
- 设置新的 `QVideoSink` 后仍期待旧 sink 收到帧；播放器只保留一个视频输出。
- 设置 `QPlaybackOptions` 后期待当前源立即改变；选项在下一次 `setSource()` 生效。
- 让 `QIODevice`、音频输出或视频 sink 提前析构；播放器保存的是外部对象指针。
- 只看 `playbackState()` 判断是否卡顿；网络停顿还要看 `mediaStatus()`。

## API 速查表

| 类别 | API | 作用 | 边界与重点 |
| --- | --- | --- | --- |
| 构造 | `QMediaPlayer(QObject *)` | 创建播放器。 | QObject 生命周期；默认无媒体。 |
| 源 | `setSource(QUrl)` | 设置 URL 源。 | 异步加载；空 URL 清除媒体。 |
| 源 | `setSourceDevice(QIODevice *, QUrl)` | 设置设备源。 | 设备须已打开、可读且由调用方保持有效。 |
| 源 | `source()` / `sourceDevice()` | 查询当前源。 | 设备指针不转移所有权。 |
| 控制 | `play()` / `pause()` / `stop()` | 播放、暂停、停止。 | 实际输出异步；停止后播放从开头开始。 |
| 状态 | `playbackState()` | 查询停止/播放/暂停。 | 不等于媒体加载状态。 |
| 状态 | `mediaStatus()` | 查询加载、缓冲、结束等状态。 | 网络卡顿需结合它判断。 |
| 状态 | `isPlaying()` / `isAvailable()` | 查询播放和服务可用性。 | 可用不代表 URL/编码器一定支持。 |
| 时间 | `duration()` | 总时长，毫秒。 | 可能尚未可用或动态变化。 |
| 时间 | `position()` / `setPosition()` | 查询/设置位置，毫秒。 | 先判断 `isSeekable()`。 |
| 缓冲 | `bufferProgress()` | 0 到 1 的临时缓冲比例。 | 不是整个文件下载进度。 |
| 缓冲 | `bufferedTimeRange()` | 查询已缓冲时间区间。 | 适合处理不连续网络缓冲。 |
| 内容 | `hasAudio()` / `hasVideo()` | 查询媒体流类型。 | 探测完成前可能变化。 |
| 内容 | `metaData()` | 查询媒体元数据。 | 依赖后端和平台。 |
| 速率 | `playbackRate()` / `setPlaybackRate()` | 查询/设置速率倍率。 | 负数不支持；后端支持范围不同。 |
| 循环 | `loops()` / `setLoops(int)` | 设置播放次数。 | 默认 1；`Infinite == -1`；0 无效果。 |
| 输出 | `setAudioOutput()` / `audioOutput()` | 连接音频输出。 | `nullptr` 禁用；播放器不负责外部对象生命周期。 |
| 输出 | `setVideoOutput()` / `videoOutput()` | 连接视频输出。 | 同时只能有一个。 |
| 输出 | `setVideoSink()` / `videoSink()` | 连接或读取 `QVideoSink`。 | 是视频输出槽位的便捷接口。 |
| 输出 | `setAudioBufferOutput()` / `audioBufferOutput()` | 接收解码音频 buffer。 | Qt 6.8；结尾发空 buffer；不按速率缩放。 |
| 轨道 | `audioTracks()` / `videoTracks()` / `subtitleTracks()` | 查询轨道元数据。 | 索引只对当前媒体有效。 |
| 轨道 | 三个 `active...Track()` | 查询当前轨道索引。 | 字幕默认 `-1`。 |
| 轨道 | 三个 `setActive...Track(int)` | 选择或禁用轨道。 | `-1` 禁用对应类型。 |
| 错误 | `error()` / `errorString()` | 查询最近错误。 | 程序逻辑用枚举，文本用于日志。 |
| 错误 | `errorOccurred()` / `errorChanged()` | 接收错误事件/属性变化。 | 优先连接 `errorOccurred()`。 |
| Qt 6.10 | `pitchCompensationAvailability()` | 查询音调补偿能力。 | 后端差异明显。 |
| Qt 6.10 | `pitchCompensation()` / `setPitchCompensation()` | 保持变速时音高。 | 增加 CPU 负载；不可用时忽略。 |
| Qt 6.10 | `playbackOptions()` / `setPlaybackOptions()` | 配置高级播放提示。 | 下一次 `setSource()` 生效，可能被忽略。 |
| Qt 6.10 | `resetPlaybackOptions()` | 恢复默认播放选项。 | 对新源生效。 |
| 通知 | `sourceChanged()`、`playbackStateChanged()`、`mediaStatusChanged()` | 观察源和状态机。 | 不要用同步返回值替代。 |
| 通知 | `durationChanged()`、`positionChanged()` | 更新时长和进度 UI。 | 均为毫秒。 |
| 通知 | `bufferProgressChanged()`、`seekableChanged()` | 更新缓冲/拖动能力。 | 网络媒体状态会变化。 |
| 通知 | `hasAudioChanged()`、`hasVideoChanged()`、`tracksChanged()` | 更新媒体内容和轨道 UI。 | 切源后重新读取列表。 |
| 通知 | `metaDataChanged()` | 更新标题、作者等信息。 | 元数据可能分阶段到达。 |
| 通知 | `videoOutputChanged()`、`audioOutputChanged()`、`audioBufferOutputChanged()` | 观察输出连接变化。 | audioBufferOutput 自 Qt 6.8。 |
| 通知 | `activeTracksChanged()` | 观察轨道选择变化。 | 与轨道列表变化区分。 |
| 通知 | `playingChanged()`、`playbackRateChanged()`、`loopsChanged()` | 观察播放属性。 | 适合属性绑定。 |
| 通知 | `pitchCompensationChanged()`、`playbackOptionsChanged()` | 观察 Qt 6.10 配置变化。 | 选项生效时机仍由后端决定。 |

---

### 一句话总结

`QMediaPlayer` 是一个由事件循环驱动的高层播放状态机：源、加载状态、播放状态、缓冲、输出和轨道都要通过各自的 API 与信号分别处理。
