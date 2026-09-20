# QMediaFormat：描述媒体容器与音视频编解码组合

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMediaFormat>`  
> 所属模块：`Qt6::Multimedia`  
> 继承：无  
> 类型性质：隐式共享值类型

## 它解决什么问题

`QMediaFormat` 描述一组媒体文件格式和编解码器选择，回答的是“文件应该用什么容器保存、音频和视频分别用什么编码”：

- 文件格式，也就是容器或音频文件格式，例如 MP4、Matroska、WebM、MP3、FLAC、WAV；
- 音频编解码器，例如 AAC、MP3、Opus、FLAC；
- 视频编解码器，例如 H.264、H.265、VP9、AV1。

它不负责真正编码或解码，也不包含媒体数据。`QMediaRecorder` 使用它决定录制输出格式，播放器和后端也可以用它查询当前构建支持哪些编码/解码组合。

```text
QMediaFormat
   |
   +-- FileFormat   容器/文件格式
   +-- AudioCodec   音频编码
   +-- VideoCodec   视频编码
            |
            v
      QMediaRecorder / 后端能力检查
```

## 真实使用场景

- 录屏设置中让用户选择 MP4、WebM 或 Matroska；
- 根据当前平台可用能力填充音频和视频编码器下拉框；
- 录制前验证“容器 + 音频编码 + 视频编码”组合是否能编码；
- 让用户偏好保持为空，由 Qt 为未指定项解析出可用默认组合；
- 播放器或转换工具查询某个容器能否被解码。

## 基本使用流程

```cpp
QMediaFormat format;
format.setFileFormat(QMediaFormat::MPEG4);
format.setVideoCodec(QMediaFormat::VideoCodec::H264);
format.setAudioCodec(QMediaFormat::AudioCodec::AAC);

if (!format.isSupported(QMediaFormat::Encode)) {
    qWarning() << "recording format is not supported";
    return;
}

recorder->setMediaFormat(format);
```

格式能力是平台和后端相关的，不能只凭枚举名称判断。UI 一般应先查询支持列表，再设置用户选择，最后用 `isSupported(Encode)` 检查完整组合。

## 容器、编码器和文件扩展名不是一回事

`MPEG4` 是文件格式/容器，`H264` 是视频编解码器，`AAC` 是音频编解码器。一个容器通常只能承载部分编码组合，因此三者需要作为整体检查。

文件名扩展名也不能替代 `QMediaFormat`。扩展名只是路径文本或后端的提示；它不保证容器和编码器实际匹配。需要跨平台输出时，应显式配置并验证格式，再由 `QMediaRecorder` 报告最终状态。

## 枚举类型

### `FileFormat`

| 枚举值 | 典型含义 |
| --- | --- |
| `UnspecifiedFormat` | 不指定文件格式，由后端/配置流程决定。 |
| `WMV` | Windows Media Video 文件格式。 |
| `AVI` | AVI 容器。 |
| `Matroska` | Matroska，常见扩展名为 MKV。 |
| `MPEG4` | MPEG-4 容器，常见扩展名为 MP4。 |
| `Ogg` | Ogg 容器。 |
| `QuickTime` | QuickTime 容器，常见扩展名为 MOV。 |
| `WebM` | WebM 容器。 |
| `Mpeg4Audio` | MPEG-4 音频文件格式。 |
| `AAC` | AAC 音频文件格式。 |
| `WMA` | Windows Media Audio 文件格式。 |
| `MP3` | MP3 文件格式。 |
| `FLAC` | FLAC 文件格式。 |
| `Wave` | Wave/WAV 文件格式。 |

### `AudioCodec`

包括 `MP3`、`AAC`、`AC3`、`EAC3`、`FLAC`、`DolbyTrueHD`、`Opus`、`Vorbis`、`Wave`、`WMA` 和 `ALAC`。`Unspecified` 表示不指定音频编码器。

### `VideoCodec`

包括 `MPEG1`、`MPEG2`、`MPEG4`、`H264`、`H265`、`VP8`、`VP9`、`AV1`、`Theora`、`WMV` 和 `MotionJPEG`。`Unspecified` 表示不指定视频编码器。

枚举中的值代表 Qt 能表达的标准选项，不保证当前平台后端真的安装或启用了对应能力。`Last...` 只用于标记枚举范围，不是实际格式选项。

### `ConversionMode`

- `Encode`：检查当前组合能否编码，典型用于录制；
- `Decode`：检查当前组合能否解码，典型用于播放或媒体读取。

编码和解码能力可能不同。例如某平台能解码某编码，却不能用它录制；查询时必须使用正确的模式。

### `ResolveFlags`

- `NoFlags`：按普通规则解析未指定项；
- `RequiresVideo`：解析时要求结果包含视频编码，适合明确要生成视频的录制场景。

## 支持列表是有上下文的

三个 `supported...()` 函数不是单纯返回全局枚举，而是会根据当前对象中已经设置的其他字段进行筛选：

```cpp
QMediaFormat format;
const auto containers =
        format.supportedFileFormats(QMediaFormat::Encode);

format.setFileFormat(QMediaFormat::MPEG4);
const auto videoCodecs =
        format.supportedVideoCodecs(QMediaFormat::Encode);

format.setVideoCodec(QMediaFormat::VideoCodec::H264);
const auto audioCodecs =
        format.supportedAudioCodecs(QMediaFormat::Encode);
```

对默认构造的 `QMediaFormat` 查询，可以取得该模式下较完整的支持列表。设置了容器后再查询编码器，得到的是与该容器相关的候选项；设置了一个不匹配的编码器，列表可能为空。

这些列表是查询时的值快照。后端、驱动、系统组件和权限状态改变后，应重新查询，不要长期缓存为跨平台能力表。

## `isSupported()` 与 `resolveForEncoding()`

`isSupported(mode)` 检查当前容器、音频编码器和视频编码器组合是否能按指定模式工作。它是整体组合检查，不是分别检查三个枚举值是否存在。

`resolveForEncoding(flags)` 会就地修改对象，把未指定或当前录制器不支持的设置调整为接近且可用的组合。Qt 的解析优先级是：

1. 文件格式；
2. 视频编解码器；
3. 音频编解码器。

因此它不是“保留用户每一项设置”的函数。调用后必须重新读取 `fileFormat()`、`videoCodec()` 和 `audioCodec()`，并把解析后的对象交给录制器。若业务必须严格遵守用户选择，应先调用 `isSupported()`，失败时提示用户，而不是静默解析成另一个格式。

```cpp
QMediaFormat format;
format.setFileFormat(QMediaFormat::MPEG4);
format.resolveForEncoding(QMediaFormat::RequiresVideo);

qDebug() << format.fileFormat()
         << format.videoCodec()
         << format.audioCodec();
```

## 值语义、共享和线程

`QMediaFormat` 是值类型，复制、移动、赋值和 `swap()` 只处理格式描述，不复制媒体文件、不打开编码器，也不拥有 `QMediaRecorder`。它可以安全地作为配置值在对象之间传递；真正查询后端能力和开始编码仍应在媒体对象所属线程中进行。

隐式共享只优化复制成本，不让正在使用的格式配置变成线程同步对象。一个线程修改自己的副本通常没有问题；多个线程同时修改同一个逻辑配置时，仍需由应用同步。

## MIME 类型和名称描述

`mimeType()` 根据文件格式返回 MIME 类型，但只有启用了 Qt MIME 类型支持时才有该 API。未指定或无法映射的格式可能返回无效 `QMimeType`，不能把它当作编码支持判断。

`fileFormatName()`、`audioCodecName()` 和 `videoCodecName()` 返回面向程序或界面的短名称；相应的 `...Description()` 返回更适合展示的描述。它们用于显示和日志，不是稳定的持久化协议字段，也不替代枚举值。

## 常见误区

- 把容器格式当成视频编码器，例如把 MP4 直接当成 H.264。
- 只检查容器支持，不检查容器与音视频编码器的完整组合。
- 用 `Decode` 的能力推断 `Encode` 一定可用。
- 把 `supported...()` 当作永恒不变的跨平台列表。
- 调用 `resolveForEncoding()` 后继续使用旧的格式变量或旧的 UI 选择。
- 认为 `Unspecified` 会在所有后端得到同一个默认格式。
- 只改文件扩展名，期待后端自动完成可靠的容器和编码协商。
- 把值对象的复制理解为复制底层编码器资源。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QMediaFormat(FileFormat format = UnspecifiedFormat)` | 创建格式描述，可选设置文件格式。 | 不打开编解码器；未指定时三个维度可能都是未指定。 |
| 构造/赋值 | `QMediaFormat(const QMediaFormat &other)` | 复制格式描述。 | 值语义；不复制媒体数据或录制器。 |
| 构造/赋值 | `QMediaFormat(QMediaFormat &&other) noexcept` | 移动格式描述。 | 适合临时值和容器操作。 |
| 析构 | `~QMediaFormat()` | 销毁格式值。 | 不释放后端编码资源。 |
| 交换 | `void swap(QMediaFormat &other) noexcept` | 交换两个格式值。 | 只交换描述字段。 |
| 查询/设置 | `FileFormat fileFormat() const` | 返回文件格式。 | `UnspecifiedFormat` 不是具体容器。 |
| 设置 | `void setFileFormat(FileFormat f)` | 设置文件格式。 | 设置后仍需检查编码/解码能力。 |
| 查询/设置 | `AudioCodec audioCodec() const` | 返回音频编解码器。 | `Unspecified` 表示未指定。 |
| 设置 | `void setAudioCodec(AudioCodec codec)` | 设置音频编解码器。 | 与容器组合可能不兼容。 |
| 查询/设置 | `VideoCodec videoCodec() const` | 返回视频编解码器。 | `Unspecified` 表示未指定。 |
| 设置 | `void setVideoCodec(VideoCodec codec)` | 设置视频编解码器。 | 与容器组合可能不兼容。 |
| 检查 | `bool isSupported(ConversionMode mode) const` | 检查完整格式组合能否编码或解码。 | `Encode` 和 `Decode` 能力不同。 |
| MIME | `QMimeType mimeType() const` | 返回文件格式对应的 MIME 类型。 | 需要 MIME 支持；无映射时可能无效。 |
| 查询 | `QList<FileFormat> supportedFileFormats(ConversionMode m)` | 查询与当前音视频编码设置匹配的文件格式。 | 默认构造对象可查询较完整列表。 |
| 查询 | `QList<VideoCodec> supportedVideoCodecs(ConversionMode m)` | 查询与当前容器和音频编码设置匹配的视频编码器。 | 结果依赖上下文和后端。 |
| 查询 | `QList<AudioCodec> supportedAudioCodecs(ConversionMode m)` | 查询与当前容器和视频编码设置匹配的音频编码器。 | 结果依赖上下文和后端。 |
| 展示 | `static QString fileFormatName(FileFormat fileFormat)` | 返回文件格式短名称。 | 用于界面/日志，不是能力判断。 |
| 展示 | `static QString fileFormatDescription(FileFormat fileFormat)` | 返回文件格式描述。 | 不作为持久化协议值。 |
| 展示 | `static QString audioCodecName(AudioCodec codec)` | 返回音频编码器短名称。 | 可能随翻译环境变化。 |
| 展示 | `static QString audioCodecDescription(AudioCodec codec)` | 返回音频编码器描述。 | 用于用户界面说明。 |
| 展示 | `static QString videoCodecName(VideoCodec codec)` | 返回视频编码器短名称。 | 不能替代枚举值。 |
| 展示 | `static QString videoCodecDescription(VideoCodec codec)` | 返回视频编码器描述。 | 用于用户界面说明。 |
| 调整 | `void resolveForEncoding(ResolveFlags flags)` | 就地解析成 `QMediaRecorder` 支持的组合。 | 解析会修改对象，优先保留容器。 |
| 比较 | `bool operator==(const QMediaFormat &other) const` | 比较三个格式字段。 | 只比较描述值。 |
| 比较 | `bool operator!=(const QMediaFormat &other) const` | 判断两个格式描述不同。 | 不表示后端能力不同。 |

## 一句话总结

`QMediaFormat` 是媒体输出的“格式配置值”：先按 `Encode`/`Decode` 查询与上下文匹配的能力，再检查完整组合；需要自动兜底时用 `resolveForEncoding()`，并重新读取它修改后的结果。
