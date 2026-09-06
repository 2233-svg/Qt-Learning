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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 29 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QAudioFormat::AudioChannelPosition`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QAudioFormat` 暴露的类型声明 `Audio、Channel、Position`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:AudioChannelPosition`。
- 属性名：`QAudioFormat`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QAudioFormat::ChannelConfig`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QAudioFormat` 暴露的类型声明 `Channel、Config`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ChannelConfig`。
- 属性名：`QAudioFormat`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QAudioFormat::SampleFormat`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QAudioFormat` 暴露的类型声明 `Sample、格式化`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:SampleFormat`。
- 属性名：`QAudioFormat`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[default] QAudioFormat::QAudioFormat()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAudioFormat` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[default] QAudioFormat::QAudioFormat(const QAudioFormat &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAudioFormat` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QAudioFormat &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept default] QAudioFormat::~QAudioFormat()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAudioFormat` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint32 QAudioFormat::bytesForDuration(qint64 microseconds) const`

**API 类别：** 成员函数说明

**中文解读：** `QAudioFormat::bytesForDuration` 用于计算、查询或取得与“字节、For、持续时间”相关的操作。调用时要先确认当前状态和 `microseconds` 的有效范围；返回类型是 `qint32`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint32`。
- 参数 `microseconds`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint32 QAudioFormat::bytesForFrames(qint32 frameCount) const`

**API 类别：** 成员函数说明

**中文解读：** `QAudioFormat::bytesForFrames` 用于计算、查询或取得与“字节、For、Frames”相关的操作。调用时要先确认当前状态和 `frameCount` 的有效范围；返回类型是 `qint32`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint32`。
- 参数 `frameCount`：类型为 `qint32`。没有默认值，调用时必须提供。传入 `qint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr] int QAudioFormat::bytesPerFrame() const`

**API 类别：** 成员函数说明

**中文解读：** `QAudioFormat::bytesPerFrame` 用于计算、查询或取得与“字节、Per、Frame”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] int QAudioFormat::bytesPerSample() const`

**API 类别：** 成员函数说明

**中文解读：** `QAudioFormat::bytesPerSample` 用于计算、查询或取得与“字节、Per、Sample”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QAudioFormat::ChannelConfig QAudioFormat::channelConfig() const`

**API 类别：** 成员函数说明

**中文解读：** `QAudioFormat::channelConfig` 用于计算、查询或取得与“channel、Config”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAudioFormat::ChannelConfig`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAudioFormat::ChannelConfig`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static constexpr] template <typename... Args> QAudioFormat::ChannelConfig QAudioFormat::channelConfig(Args... channels)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `channelConfig`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename... Args> QAudioFormat::ChannelConfig`。
- 参数 `channels`：类型为 `Args...`。没有默认值，调用时必须提供。传入 `Args...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] int QAudioFormat::channelCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QAudioFormat::channelCount` 用于计算、查询或取得与“channel、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] int QAudioFormat::channelOffset(QAudioFormat::AudioChannelPosition channel) const`

**API 类别：** 成员函数说明

**中文解读：** `QAudioFormat::channelOffset` 用于计算、查询或取得与“channel、Offset”相关的操作。调用时要先确认当前状态和 `channel` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `channel`：类型为 `QAudioFormat::AudioChannelPosition`。没有默认值，调用时必须提供。传入 `QAudioFormat::AudioChannelPosition` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QAudioFormat::ChannelConfig QAudioFormat::defaultChannelConfigForChannelCount(int channelCount)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `defaultChannelConfigForChannelCount`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QAudioFormat::ChannelConfig`。
- 参数 `channelCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QAudioFormat::durationForBytes(qint32 bytes) const`

**API 类别：** 成员函数说明

**中文解读：** `QAudioFormat::durationForBytes` 用于计算、查询或取得与“持续时间、For、字节”相关的操作。调用时要先确认当前状态和 `bytes` 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `bytes`：类型为 `qint32`。没有默认值，调用时必须提供。传入 `qint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QAudioFormat::durationForFrames(qint32 frameCount) const`

**API 类别：** 成员函数说明

**中文解读：** `QAudioFormat::durationForFrames` 用于计算、查询或取得与“持续时间、For、Frames”相关的操作。调用时要先确认当前状态和 `frameCount` 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `frameCount`：类型为 `qint32`。没有默认值，调用时必须提供。传入 `qint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint32 QAudioFormat::framesForBytes(qint32 byteCount) const`

**API 类别：** 成员函数说明

**中文解读：** `QAudioFormat::framesForBytes` 用于计算、查询或取得与“frames、For、字节”相关的操作。调用时要先确认当前状态和 `byteCount` 的有效范围；返回类型是 `qint32`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint32`。
- 参数 `byteCount`：类型为 `qint32`。没有默认值，调用时必须提供。传入 `qint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint32 QAudioFormat::framesForDuration(qint64 microseconds) const`

**API 类别：** 成员函数说明

**中文解读：** `QAudioFormat::framesForDuration` 用于计算、查询或取得与“frames、For、持续时间”相关的操作。调用时要先确认当前状态和 `microseconds` 的有效范围；返回类型是 `qint32`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint32`。
- 参数 `microseconds`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] bool QAudioFormat::isValid() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isValid`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `float QAudioFormat::normalizedSampleValue(const void *sample) const`

**API 类别：** 成员函数说明

**中文解读：** `QAudioFormat::normalizedSampleValue` 用于计算、查询或取得与“normalized、Sample、值访问”相关的操作。调用时要先确认当前状态和 `sample` 的有效范围；返回类型是 `float`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`float`。
- 参数 `sample`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QAudioFormat::SampleFormat QAudioFormat::sampleFormat() const`

**API 类别：** 成员函数说明

**中文解读：** `QAudioFormat::sampleFormat` 用于计算、查询或取得与“sample、格式化”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAudioFormat::SampleFormat`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAudioFormat::SampleFormat`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] int QAudioFormat::sampleRate() const`

**API 类别：** 成员函数说明

**中文解读：** `QAudioFormat::sampleRate` 用于计算、查询或取得与“sample、Rate”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QAudioFormat::setChannelConfig(QAudioFormat::ChannelConfig config)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setChannelConfig`。调用它会改变 `QAudioFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `config`：类型为 `QAudioFormat::ChannelConfig`。没有默认值，调用时必须提供。传入 `QAudioFormat::ChannelConfig` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] void QAudioFormat::setChannelCount(int channels)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setChannelCount`。调用它会改变 `QAudioFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `channels`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] void QAudioFormat::setSampleFormat(QAudioFormat::SampleFormat format)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSampleFormat`。调用它会改变 `QAudioFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `format`：类型为 `QAudioFormat::SampleFormat`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] void QAudioFormat::setSampleRate(int samplerate)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSampleRate`。调用它会改变 `QAudioFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `samplerate`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool operator!=(const QAudioFormat &a, const QAudioFormat &b)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QAudioFormat` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `a`：类型为 `const QAudioFormat &`。没有默认值，调用时必须提供。传入 `const QAudioFormat &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `b`：类型为 `const QAudioFormat &`。没有默认值，调用时必须提供。传入 `const QAudioFormat &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool operator==(const QAudioFormat &a, const QAudioFormat &b)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QAudioFormat` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `a`：类型为 `const QAudioFormat &`。没有默认值，调用时必须提供。传入 `const QAudioFormat &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `b`：类型为 `const QAudioFormat &`。没有默认值，调用时必须提供。传入 `const QAudioFormat &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

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

`QAudioFormat` 所属机制类型：多媒体设备与会话机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
