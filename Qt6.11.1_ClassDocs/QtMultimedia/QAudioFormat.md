# QAudioFormat

> Qt 6.11.1 · Qt Multimedia

## 1. 先建立直觉

**一句话定位：** `QAudioFormat` 是 Qt Multimedia 的“音频格式”类型，参与媒体源、设备、格式、播放/采集状态或音视频数据处理。

**模块背景：** Qt Multimedia 提供音频、视频、摄像头、媒体会话和设备访问能力。

### 这是什么

`QAudioFormat` 是 多媒体设备与会话机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

**适用场景：** 先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

## 2. 依赖与对象关系

- 头文件：`#include <QAudioFormat>`
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

- `enum AudioChannelPosition { UnknownPosition, FrontLeft, FrontRight, FrontCenter, LFE, …, BottomFrontRight }`
- `enum ChannelConfig { ChannelConfigUnknown, ChannelConfigMono, ChannelConfigStereo, ChannelConfig2Dot1, ChannelConfig3Dot0, …, ChannelConfigSurround7Dot1 }`
- `enum SampleFormat { Unknown, UInt8, Int16, Int32, Float }`

### 公有函数

- `QAudioFormat()`
- `QAudioFormat(const QAudioFormat &other)`
- `~QAudioFormat()`
- `qint32 bytesForDuration(qint64 microseconds) const`
- `qint32 bytesForFrames(qint32 frameCount) const`
- `int bytesPerFrame() const`
- `int bytesPerSample() const`
- `QAudioFormat::ChannelConfig channelConfig() const`
- `int channelCount() const`
- `int channelOffset(QAudioFormat::AudioChannelPosition channel) const`
- `qint64 durationForBytes(qint32 bytes) const`
- `qint64 durationForFrames(qint32 frameCount) const`
- `qint32 framesForBytes(qint32 byteCount) const`
- `qint32 framesForDuration(qint64 microseconds) const`
- `bool isValid() const`
- `float normalizedSampleValue(const void *sample) const`
- `QAudioFormat::SampleFormat sampleFormat() const`
- `int sampleRate() const`
- `void setChannelConfig(QAudioFormat::ChannelConfig config)`
- `void setChannelCount(int channels)`
- `void setSampleFormat(QAudioFormat::SampleFormat format)`
- `void setSampleRate(int samplerate)`

### 静态公有成员

- `QAudioFormat::ChannelConfig channelConfig(Args... channels)`
- `QAudioFormat::ChannelConfig defaultChannelConfigForChannelCount(int channelCount)`

### 相关非成员函数

- `bool operator!=(const QAudioFormat &a, const QAudioFormat &b)`
- `bool operator==(const QAudioFormat &a, const QAudioFormat &b)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QAudioFormat::AudioChannelPosition`

**作用与语义：**

描述可能的音频通道位置。这些通道遵循22.2环绕声配置中使用的标清。
- `QAudioFormat::UnknownPosition`：`0`;位置不明
- `QAudioFormat::FrontLeft`：`1`
- `QAudioFormat::FrontRight`：`2`
- `QAudioFormat::FrontCenter`：`3`
- `QAudioFormat::LFE`：`4`;低频效果通道（低音炮）
- `QAudioFormat::BackLeft`：`5`
- `QAudioFormat::BackRight`：`6`
- `QAudioFormat::FrontLeftOfCenter`：`7`
- `QAudioFormat::FrontRightOfCenter`：`8`
- `QAudioFormat::BackCenter`：`9`
- `QAudioFormat::LFE2`：`19`
- `QAudioFormat::SideLeft`：`10`
- `QAudioFormat::SideRight`：`11`
- `QAudioFormat::TopFrontLeft`：`13`
- `QAudioFormat::TopFrontRight`：`15`
- `QAudioFormat::TopFrontCenter`：`14`
- `QAudioFormat::TopCenter`：`12`
- `QAudioFormat::TopBackLeft`：`16`
- `QAudioFormat::TopBackRight`：`18`
- `QAudioFormat::TopSideLeft`：`20`
- `QAudioFormat::TopSideRight`：`21`
- `QAudioFormat::TopBackCenter`：`17`
- `QAudioFormat::BottomFrontCenter`：`22`
- `QAudioFormat::BottomFrontLeft`：`23`
- `QAudioFormat::BottomFrontRight`：`24`

### `enum QAudioFormat::ChannelConfig`

**作用与语义：**

本枚举描述了标准化的音频通道布局。最常见的配置包括单声道、立体声、2.1声道（立体声加低频）、5.1环绕和7.1环绕配置。
- `QAudioFormat::ChannelConfigUnknown`：`0`;信道配置尚不清楚。
- `QAudioFormat::ChannelConfigMono`：`QtPrivate::channelConfig(FrontCenter)`;音频有一个中置声道。
- `QAudioFormat::ChannelConfigStereo`：`QtPrivate::channelConfig(FrontLeft, FrontRight)`;音频有两个声道，分别是左声道和右声道。
- `QAudioFormat::ChannelConfig2Dot1`：`QtPrivate::channelConfig(FrontLeft, FrontRight, LFE)`;音频有三个声道，分别是左声道、右声道和低频效果（LFE）。
- `QAudioFormat::ChannelConfig3Dot0`：`QtPrivate::channelConfig(FrontLeft, FrontRight, FrontCenter)`;音频有三个声道，分别是左声道、右声道和中声道。
- `QAudioFormat::ChannelConfig3Dot1`：`QtPrivate::channelConfig(FrontLeft, FrontRight, FrontCenter, LFE)`;音频有四个声道，分别是左声道、右声道、中声道和低频效果（LFE）。
- `QAudioFormat::ChannelConfigSurround5Dot0`：`QtPrivate::channelConfig(FrontLeft, FrontRight, FrontCenter, BackLeft, BackRight)`;音频有五个声道，分别是左声道、右声道、中声道、正声道`BackLeft`声道和声道`BackRight`。
- `QAudioFormat::ChannelConfigSurround5Dot1`：`QtPrivate::channelConfig(FrontLeft, FrontRight, FrontCenter, LFE, BackLeft, BackRight)`;音频有6个声道，分别是左声道、右声道、中声道、低频效果器（LFE）、`BackLeft`声道和`BackRight`声道。
- `QAudioFormat::ChannelConfigSurround7Dot0`：`QtPrivate::channelConfig(FrontLeft, FrontRight, FrontCenter, BackLeft, BackRight, SideLeft, SideRight)`;音频有7个声道，分别是左、右、中、`BackLeft`、`BackRight`、`SideLeft`和`SideRight`。
- `QAudioFormat::ChannelConfigSurround7Dot1`：`QtPrivate::channelConfig(FrontLeft, FrontRight, FrontCenter, LFE, BackLeft, BackRight, SideLeft, SideRight)`;音频有8个声道，分别是左声道、右声道、中声道、低频效果器、`BackLeft`声道、`BackRight`声道、正`SideLeft`声道和`SideRight`声道。

### `enum QAudioFormat::SampleFormat`

**作用与语义：**

Qt始终期望并使用主平台的字节音。在自己处理外部音频数据时，确保在写入`QAudioSink`或音`QAudioBuffer`前将其转换为正确的字节。
- `QAudioFormat::Unknown`：`0`;未设定
- `QAudioFormat::UInt8`：`1`;采样是8位无符号整数
- `QAudioFormat::Int16`：`2`;采样是16位符号整数
- `QAudioFormat::Int32`：`3`;采样是32位符号整数
- `QAudioFormat::Float`：`4`;样本是浮点

### `[default] QAudioFormat::QAudioFormat()`

**作用与语义：**

构建了一种新的音频格式。
数值初始化如下：
- `sampleRate()` = 0
- `channelCount()` = 0
- `sampleFormat()` = `QAudioFormat::Unknown`

### `[default] QAudioFormat::QAudioFormat(const QAudioFormat &other)`

**作用与语义：**

用`other`构建一种新的音频格式。

### `[noexcept default] QAudioFormat::~QAudioFormat()`

**作用与语义：**

销毁这个音频格式。

### `qint32 QAudioFormat::bytesForDuration(qint64 microseconds) const`

**作用与语义：**

返回该音频格式所需的字节数，`microseconds`。
如果该格式不成立，则返回 0。
注意，如果 `microseconds` 不是`sampleRate()`的精确分数，可能会出现一些四舍五入。

### `qint32 QAudioFormat::bytesForFrames(qint32 frameCount) const`

**作用与语义：**

返回该格式`frameCount`帧所需的字节数。
如果该格式不成立，则返回 0。

### `[constexpr] int QAudioFormat::bytesPerFrame() const`

**作用与语义：**

返回表示该格式中一帧（每个通道中的一个采样）所需的字节数。
如果该格式无效，则返回0。

### `[constexpr noexcept] int QAudioFormat::bytesPerSample() const`

**作用与语义：**

返回表示该格式中一个样本所需的字节数。
如果该格式无效，则返回0。

### `[constexpr noexcept] QAudioFormat::ChannelConfig QAudioFormat::channelConfig() const`

**作用与语义：**

返回当前频道配置。

### `[static constexpr] template <typename... Args> QAudioFormat::ChannelConfig QAudioFormat::channelConfig(Args... channels)`

**作用与语义：**

返回给定`channels`当前的信道配置。

### `[constexpr noexcept] int QAudioFormat::channelCount() const`

**作用与语义：**

返回当前频道计数值。

### `[noexcept] int QAudioFormat::channelOffset(QAudioFormat::AudioChannelPosition channel) const`

**作用与语义：**

返回某一音频`channel`在给定格式中音频帧内的位置。如果该格式的通道不存在或通道配置未知，返回-1。

### `[static] QAudioFormat::ChannelConfig QAudioFormat::defaultChannelConfigForChannelCount(int channelCount)`

**作用与语义：**

`channelCount`返回默认频道配置。
默认配置最多支持8个声道，对应标准的单声道、立体声和环绕声配置。对于更高声道数量，只需使用`QAudioFormat::AudioChannelPosition`中定义的前`channelCount`音频声道。

### `qint64 QAudioFormat::durationForBytes(qint32 bytes) const`

**作用与语义：**

返回该格式中由`bytes`表示的微秒数。
如果该格式不成立，则返回 0。
注意，如果`bytes`不是每帧字节数的正好倍数，可能会进行一些舍入处理。

### `qint64 QAudioFormat::durationForFrames(qint32 frameCount) const`

**作用与语义：**

返回以`frameCount`帧表示的微秒数。

### `qint32 QAudioFormat::framesForBytes(qint32 byteCount) const`

**作用与语义：**

返回该格式中由`byteCount`表示的帧数。
注意，如果`byteCount`不是每帧字节数的正好倍数，可能会出现一些四舍五入。
每帧每个通道有一个采样。

### `qint32 QAudioFormat::framesForDuration(qint64 microseconds) const`

**作用与语义：**

返回表示该格式`microseconds`所需的帧数。
注意，如果`microseconds`不是`sampleRate()`的精确分数，可能会出现一定的舍入。

### `[constexpr noexcept] bool QAudioFormat::isValid() const`

**作用与语义：**

如果所有参数都有效，返回`true`。

### `float QAudioFormat::normalizedSampleValue(const void *sample) const`

**作用与语义：**

将`sample`值归一化为-1到1之间的数值。该方法依赖于QaudioFormat。

### `[constexpr noexcept] QAudioFormat::SampleFormat QAudioFormat::sampleFormat() const`

**作用与语义：**

返回当前的采样格式。

### `[constexpr noexcept] int QAudioFormat::sampleRate() const`

**作用与语义：**

返回当前的采样率（赫兹）。

### `[noexcept] void QAudioFormat::setChannelConfig(QAudioFormat::ChannelConfig config)`

**作用与语义：**

将通道配置设置为`config`。
将音频格式的通道配置设置为标准音频通道配置之一。
注意：这也会改变频道数量。

### `[constexpr noexcept] void QAudioFormat::setChannelCount(int channels)`

**作用与语义：**

将频道计数设置为`channels`。设置后频道配置也设为`ChannelConfigUnknown`。

### `[constexpr noexcept] void QAudioFormat::setSampleFormat(QAudioFormat::SampleFormat format)`

**作用与语义：**

将采样格式设置为`format`。

### `[constexpr noexcept] void QAudioFormat::setSampleRate(int samplerate)`

**作用与语义：**

采样率设置为`samplerate`赫兹。

### `bool operator!=(const QAudioFormat &a, const QAudioFormat &b)`

**作用与语义：**

如果音频格式`a`不等于`b`，返回`true`，否则返回`false`。

### `bool operator==(const QAudioFormat &a, const QAudioFormat &b)`

**作用与语义：**

如果音频格式`a`等于`b`，返回`true`，否则返回`false`。

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

`QAudioFormat` 所属机制类型：多媒体设备与会话机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
