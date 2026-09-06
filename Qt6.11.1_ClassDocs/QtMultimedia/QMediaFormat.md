# QMediaFormat

> Qt 6.11.1 · Qt Multimedia

## 1. 先建立直觉

**一句话定位：** `QMediaFormat` 是 Qt Multimedia 的“媒体格式”类型，参与媒体源、设备、格式、播放/采集状态或音视频数据处理。

**模块背景：** Qt Multimedia 提供音频、视频、摄像头、媒体会话和设备访问能力。

### 这是什么

`QMediaFormat` 是 多媒体设备与会话机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

**适用场景：** 先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

## 2. 依赖与对象关系

- 头文件：`#include <QMediaFormat>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Multimedia)
target_link_libraries(mytarget PRIVATE Qt6::Multimedia)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

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

- `enum class AudioCodec { WMA, AC3, AAC, ALAC, DolbyTrueHD, …, Unspecified }`
- `enum ConversionMode { Encode, Decode }`
- `enum FileFormat { WMA, AAC, Matroska, WMV, MP3, …, UnspecifiedFormat }`
- `enum ResolveFlags { NoFlags, RequiresVideo }`
- `enum class VideoCodec { VP8, MPEG2, MPEG1, WMV, H265, …, Unspecified }`

### 属性

- `audioCodec : AudioCodec`
- `fileFormat : FileFormat`
- `videoCodec : VideoCodec`

### 公有函数

- `QMediaFormat(QMediaFormat::FileFormat format = UnspecifiedFormat)`
- `QMediaFormat(const QMediaFormat &other)`
- `QMediaFormat(QMediaFormat &&other)`
- `~QMediaFormat()`
- `QMediaFormat::AudioCodec audioCodec() const`
- `QMediaFormat::FileFormat fileFormat() const`
- `bool isSupported(QMediaFormat::ConversionMode mode) const`
- `QMimeType mimeType() const`
- `void resolveForEncoding(QMediaFormat::ResolveFlags flags)`
- `void setAudioCodec(QMediaFormat::AudioCodec codec)`
- `void setFileFormat(QMediaFormat::FileFormat f)`
- `void setVideoCodec(QMediaFormat::VideoCodec codec)`
- `QList<QMediaFormat::AudioCodec> supportedAudioCodecs(QMediaFormat::ConversionMode m)`
- `QList<QMediaFormat::FileFormat> supportedFileFormats(QMediaFormat::ConversionMode m)`
- `QList<QMediaFormat::VideoCodec> supportedVideoCodecs(QMediaFormat::ConversionMode m)`
- `void swap(QMediaFormat &other)`
- `QMediaFormat::VideoCodec videoCodec() const`
- `bool operator!=(const QMediaFormat &other) const`
- `QMediaFormat & operator=(QMediaFormat &&other)`
- `QMediaFormat & operator=(const QMediaFormat &other)`
- `bool operator==(const QMediaFormat &other) const`

### 静态公有成员

- `QString audioCodecDescription(QMediaFormat::AudioCodec codec)`
- `QString audioCodecName(QMediaFormat::AudioCodec codec)`
- `QString fileFormatDescription(QMediaFormat::FileFormat fileFormat)`
- `QString fileFormatName(QMediaFormat::FileFormat fileFormat)`
- `QString videoCodecDescription(QMediaFormat::VideoCodec codec)`
- `QString videoCodecName(QMediaFormat::VideoCodec codec)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum class QMediaFormat::AudioCodec`

**作用与语义：**

描述多媒体文件或流中使用的音频编解码器。
- `QMediaFormat::AudioCodec::WMA`：`9`;Windows Media 音频
- `QMediaFormat::AudioCodec::AC3`：`2`;杜比数字
- `QMediaFormat::AudioCodec::AAC`：`1`;高级音频编码
- `QMediaFormat::AudioCodec::ALAC`：`10`;苹果无损音频编解码器
- `QMediaFormat::AudioCodec::DolbyTrueHD`：`5`;杜比TrueHD
- `QMediaFormat::AudioCodec::EAC3`：`3`;杜比数字加（EAC3）
- `QMediaFormat::AudioCodec::MP3`：`0`;MPEG-1 音频层 III 或 MPEG-2 音频层 III
- `QMediaFormat::AudioCodec::Wave`：`8`;波形音频文件格式
- `QMediaFormat::AudioCodec::Vorbis`：`7`;奥格·沃比斯
- `QMediaFormat::AudioCodec::FLAC`：`4`;免费无损音频编解码器
- `QMediaFormat::AudioCodec::Opus`：`6`;Opus 音频格式
- `QMediaFormat::AudioCodec::Unspecified`：`-1`;未指定编解码器

### `enum QMediaFormat::ConversionMode`

**作用与语义：**

在许多情况下，系统具备非对称能力，且通常能解码比可编码更多的格式或编解码器。该枚举描述了在检查某种文件格式或编解码器是否支持时所请求的转换模式。
- `QMediaFormat::Encode`：`0`;用于检查某种文件格式或编解码器是否可以编码。
- `QMediaFormat::Decode`：`1`;用于检查某种文件格式或编解码器是否可以解码。

### `enum QMediaFormat::FileFormat`

**作用与语义：**

描述多媒体文件或流中使用的容器格式。
- `QMediaFormat::WMA`：`9`;Windows Media 音频
- `QMediaFormat::AAC`：`8`;高级音频编码
- `QMediaFormat::Matroska`：`2`;马特罗斯卡（MKV）
- `QMediaFormat::WMV`：`0`;Windows Media 视频
- `QMediaFormat::MP3`：`10`;MPEG-1 音频层 III 或 MPEG-2 音频层 III
- `QMediaFormat::Wave`：`12`;波形音频文件格式
- `QMediaFormat::Ogg`：`4`;奥格
- `QMediaFormat::MPEG4`：`3`;MPEG-4
- `QMediaFormat::AVI`：`1`;音视频交错
- `QMediaFormat::QuickTime`：`5`;QuickTime
- `QMediaFormat::WebM`：`6`;WebM
- `QMediaFormat::Mpeg4Audio`：`7`;MPEG-4 第三部分或 MPEG-4 音频（正式名称为 ISO/IEC 14496-3）
- `QMediaFormat::FLAC`：`11`;免费无损音频编解码器
- `QMediaFormat::UnspecifiedFormat`：`-1`;格式未明确说明。

### `enum QMediaFormat::ResolveFlags`

**作用与语义：**

描述解析 `QMediaRecorder` 的合适格式的要求。
- `QMediaFormat::NoFlags`: `0`; 无要求
- `QMediaFormat::RequiresVideo`: `1`; 需要视频编码器

### `enum class QMediaFormat::VideoCodec`

**作用与语义：**

描述用于多媒体文件或流媒体的视频编码。
- `QMediaFormat::VideoCodec::VP8`：`5`;VP8
- `QMediaFormat::VideoCodec::MPEG2`：`1`;MPEG-2
- `QMediaFormat::VideoCodec::MPEG1`：`0`;MPEG-1
- `QMediaFormat::VideoCodec::WMV`：`9`;Windows Media 视频
- `QMediaFormat::VideoCodec::H265`：`4`;高效视频编码（HEVC）
- `QMediaFormat::VideoCodec::H264`：`3`;高级视频编码
- `QMediaFormat::VideoCodec::MPEG4`：`2`;MPEG-4
- `QMediaFormat::VideoCodec::AV1`：`7`;AOMedia 视频1
- `QMediaFormat::VideoCodec::MotionJPEG`：`10`;MotionJPEG
- `QMediaFormat::VideoCodec::VP9`：`6`;VP9
- `QMediaFormat::VideoCodec::Theora`：`8`;西奥拉
- `QMediaFormat::VideoCodec::Unspecified`：`-1`;视频编码未指定

### `audioCodec : AudioCodec`

**作用与语义：**

该属性包含媒体的音频编解码器。

**如何使用：** 调用 `audioCodec()` 读取当前值；它不会修改应用状态。

### `fileFormat : FileFormat`

**作用与语义：**

该属性包含介质的文件（容器）格式。

**如何使用：** 调用 `fileFormat()` 读取当前值；它不会修改应用状态。

### `videoCodec : VideoCodec`

**作用与语义：**

该特性承载了媒体的视频编解码器。

**如何使用：** 调用 `videoCodec()` 读取当前值；它不会修改应用状态。

### `QMediaFormat::QMediaFormat(QMediaFormat::FileFormat format = UnspecifiedFormat)`

**作用与语义：**

为`format`构建一个QMediaFormat对象。

### `[noexcept] QMediaFormat::QMediaFormat(const QMediaFormat &other)`

**作用与语义：**

通过从`other`复制构建QMediaFormat对象。

### `[constexpr noexcept] QMediaFormat::QMediaFormat(QMediaFormat &&other)`

**作用与语义：**

通过从 `other` 构建 QMediaFormat 对象。

### `[noexcept] QMediaFormat::~QMediaFormat()`

**作用与语义：**

摧毁`QMediaFormat`物体。

### `QMediaFormat::AudioCodec QMediaFormat::audioCodec() const`

**作用与语义：**

返回该格式中使用的音频编解码器。
注意：property audioCodec的获取函数。

### `[static invokable] QString QMediaFormat::audioCodecDescription(QMediaFormat::AudioCodec codec)`

**作用与语义：**

返回描述以供`codec`。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[static invokable] QString QMediaFormat::audioCodecName(QMediaFormat::AudioCodec codec)`

**作用与语义：**

返回基于字符串的`codec`名称。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[static invokable] QString QMediaFormat::fileFormatDescription(QMediaFormat::FileFormat fileFormat)`

**作用与语义：**

返回描述以供`fileFormat`。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[static invokable] QString QMediaFormat::fileFormatName(QMediaFormat::FileFormat fileFormat)`

**作用与语义：**

返回基于字符串的 `fileFormat` 名称。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[invokable] bool QMediaFormat::isSupported(QMediaFormat::ConversionMode mode) const`

**作用与语义：**

如果 Qt 多媒体可以根据 `mode` 对此格式进行编码或解码，则返回 `true`。
注意：此函数可以通过元对象系统和 QML 调用。参见 `Q_INVOKABLE`。

### `QMimeType QMediaFormat::mimeType() const`

**作用与语义：**

返回该媒体格式中使用的文件格式的MIME类型。

### `void QMediaFormat::resolveForEncoding(QMediaFormat::ResolveFlags flags)`

**作用与语义：**

根据`flags`将格式解析为`QMediaRecorder`支持的格式。
该方法尝试为未指定设置找到最佳匹配。录音机不支持的设置将被修改为最接近的匹配。
在解析时，优先级按以下顺序确定：
- 文件格式
- 视频编解码器
- 音频编解码器

### `void QMediaFormat::setAudioCodec(QMediaFormat::AudioCodec codec)`

**作用与语义：**

该属性包含媒体的音频编解码器。

**如何使用：** 调用 `setAudioCodec(...)` 修改 `audioCodec`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QMediaFormat::setVideoCodec(QMediaFormat::VideoCodec codec)`

**作用与语义：**

该特性承载了媒体的视频编解码器。

**如何使用：** 调用 `setVideoCodec(...)` 修改 `videoCodec`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `[invokable] QList<QMediaFormat::AudioCodec> QMediaFormat::supportedAudioCodecs(QMediaFormat::ConversionMode m)`

**作用与语义：**

返回所选文件格式和视频编解码器（`m`）的音频编解码器列表。
要获取所有支持的音频编解码器，请在默认构造的编解码器上运行此查询`QMediaFormat`。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[invokable] QList<QMediaFormat::FileFormat> QMediaFormat::supportedFileFormats(QMediaFormat::ConversionMode m)`

**作用与语义：**

返回由`m`指示的音频和视频编解码器文件格式列表。
要获取所有支持的文件格式，请在默认构造`QMediaFormat`上运行此查询。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[invokable] QList<QMediaFormat::VideoCodec> QMediaFormat::supportedVideoCodecs(QMediaFormat::ConversionMode m)`

**作用与语义：**

返回所选文件格式和音频编解码器（`m`）的视频编解码器列表。
要获取所有支持的视频编码器，请在默认构造的MediaFormat上运行此查询。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[noexcept] void QMediaFormat::swap(QMediaFormat &other)`

**作用与语义：**

将媒体格式与`other`互换。

### `QMediaFormat::VideoCodec QMediaFormat::videoCodec() const`

**作用与语义：**

返回该格式中使用的视频编码器。
注意：property videoCodec的获取函数。

### `[static invokable] QString QMediaFormat::videoCodecDescription(QMediaFormat::VideoCodec codec)`

**作用与语义：**

返回描述以供`codec`。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[static invokable] QString QMediaFormat::videoCodecName(QMediaFormat::VideoCodec codec)`

**作用与语义：**

返回基于字符串的`codec`名称。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `bool QMediaFormat::operator!=(const QMediaFormat &other) const`

**作用与语义：**

如果`other`不等于当前媒体格式，返回`true`，否则返回`false`。

### `[noexcept] QMediaFormat &QMediaFormat::operator=(QMediaFormat &&other)`

**作用与语义：**

`other` `QMediaFormat`物体。

### `[noexcept] QMediaFormat &QMediaFormat::operator=(const QMediaFormat &other)`

**作用与语义：**

复制`other`到这个`QMediaFormat`对象里。

### `bool QMediaFormat::operator==(const QMediaFormat &other) const`

**作用与语义：**

如果`other`等于当前媒体格式，返回`true`;否则返回`false`。

### `QMediaFormat::FileFormat fileFormat() const`

**作用与语义：**

该属性包含介质的文件（容器）格式。

**如何使用：** 调用 `fileFormat()` 读取当前值；它不会修改应用状态。

### `void setFileFormat(QMediaFormat::FileFormat f)`

**作用与语义：**

该属性包含介质的文件（容器）格式。

**如何使用：** 调用 `setFileFormat(...)` 修改 `fileFormat`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QMediaFormat` 所属机制类型：多媒体设备与会话机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
