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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 35 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum class QMediaFormat::AudioCodec`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QMediaFormat` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:AudioCodec`。
- 属性名：`QMediaFormat`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QMediaFormat::ConversionMode`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QMediaFormat` 暴露的类型声明 `Conversion、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ConversionMode`。
- 属性名：`QMediaFormat`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QMediaFormat::FileFormat`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QMediaFormat` 暴露的类型声明 `File、格式化`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:FileFormat`。
- 属性名：`QMediaFormat`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QMediaFormat::ResolveFlags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QMediaFormat` 暴露的类型声明 `Resolve、标志`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ResolveFlags`。
- 属性名：`QMediaFormat`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum class QMediaFormat::VideoCodec`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QMediaFormat` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:VideoCodec`。
- 属性名：`QMediaFormat`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `audioCodec : AudioCodec`

**API 类别：** 属性说明

**中文解读：** 这是 `QMediaFormat` 的配置属性。初始化或状态切换时通过 `setAudioCodec(...)` 设置，之后用 `audioCodec()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`AudioCodec`。
- 属性名：`audioCodec`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `fileFormat : FileFormat`

**API 类别：** 属性说明

**中文解读：** 这是 `QMediaFormat` 的配置属性。初始化或状态切换时通过 `setFileFormat(...)` 设置，之后用 `fileFormat()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`FileFormat`。
- 属性名：`fileFormat`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `videoCodec : VideoCodec`

**API 类别：** 属性说明

**中文解读：** 这是 `QMediaFormat` 的配置属性。初始化或状态切换时通过 `setVideoCodec(...)` 设置，之后用 `videoCodec()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`VideoCodec`。
- 属性名：`videoCodec`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMediaFormat::QMediaFormat(QMediaFormat::FileFormat format = UnspecifiedFormat)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaFormat` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `format`：类型为 `QMediaFormat::FileFormat`。默认值为 `UnspecifiedFormat`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QMediaFormat::QMediaFormat(const QMediaFormat &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaFormat` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QMediaFormat &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QMediaFormat::QMediaFormat(QMediaFormat &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaFormat` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `QMediaFormat &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QMediaFormat::~QMediaFormat()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaFormat` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMediaFormat::AudioCodec QMediaFormat::audioCodec() const`

**API 类别：** 成员函数说明

**中文解读：** `QMediaFormat::audioCodec` 用于计算、查询或取得与“audio、Codec”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMediaFormat::AudioCodec`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMediaFormat::AudioCodec`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static invokable] QString QMediaFormat::audioCodecDescription(QMediaFormat::AudioCodec codec)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `audioCodecDescription`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `codec`：类型为 `QMediaFormat::AudioCodec`。没有默认值，调用时必须提供。传入 `QMediaFormat::AudioCodec` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static invokable] QString QMediaFormat::audioCodecName(QMediaFormat::AudioCodec codec)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `audioCodecName`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `codec`：类型为 `QMediaFormat::AudioCodec`。没有默认值，调用时必须提供。传入 `QMediaFormat::AudioCodec` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static invokable] QString QMediaFormat::fileFormatDescription(QMediaFormat::FileFormat fileFormat)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fileFormatDescription`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `fileFormat`：类型为 `QMediaFormat::FileFormat`。没有默认值，调用时必须提供。传入 `QMediaFormat::FileFormat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static invokable] QString QMediaFormat::fileFormatName(QMediaFormat::FileFormat fileFormat)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fileFormatName`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `fileFormat`：类型为 `QMediaFormat::FileFormat`。没有默认值，调用时必须提供。传入 `QMediaFormat::FileFormat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[invokable] bool QMediaFormat::isSupported(QMediaFormat::ConversionMode mode) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isSupported`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `mode`：类型为 `QMediaFormat::ConversionMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMimeType QMediaFormat::mimeType() const`

**API 类别：** 成员函数说明

**中文解读：** `QMediaFormat::mimeType` 用于计算、查询或取得与“mime、类型”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMimeType`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMimeType`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMediaFormat::resolveForEncoding(QMediaFormat::ResolveFlags flags)`

**API 类别：** 成员函数说明

**中文解读：** `QMediaFormat::resolveForEncoding` 用于执行与“resolve、For、Encoding”相关的操作。调用时要先确认当前状态和 `flags` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `flags`：类型为 `QMediaFormat::ResolveFlags`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMediaFormat::setAudioCodec(QMediaFormat::AudioCodec codec)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAudioCodec`。调用它会改变 `QMediaFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `codec`：类型为 `QMediaFormat::AudioCodec`。没有默认值，调用时必须提供。传入 `QMediaFormat::AudioCodec` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMediaFormat::setVideoCodec(QMediaFormat::VideoCodec codec)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setVideoCodec`。调用它会改变 `QMediaFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `codec`：类型为 `QMediaFormat::VideoCodec`。没有默认值，调用时必须提供。传入 `QMediaFormat::VideoCodec` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[invokable] QList<QMediaFormat::AudioCodec> QMediaFormat::supportedAudioCodecs(QMediaFormat::ConversionMode m)`

**API 类别：** 成员函数说明

**中文解读：** `QMediaFormat::supportedAudioCodecs` 用于计算、查询或取得与“supported、Audio、Codecs”相关的操作。调用时要先确认当前状态和 `m` 的有效范围；返回类型是 `QList<QMediaFormat::AudioCodec>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QMediaFormat::AudioCodec>`。
- 参数 `m`：类型为 `QMediaFormat::ConversionMode`。没有默认值，调用时必须提供。传入 `QMediaFormat::ConversionMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[invokable] QList<QMediaFormat::FileFormat> QMediaFormat::supportedFileFormats(QMediaFormat::ConversionMode m)`

**API 类别：** 成员函数说明

**中文解读：** `QMediaFormat::supportedFileFormats` 用于计算、查询或取得与“supported、File、Formats”相关的操作。调用时要先确认当前状态和 `m` 的有效范围；返回类型是 `QList<QMediaFormat::FileFormat>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QMediaFormat::FileFormat>`。
- 参数 `m`：类型为 `QMediaFormat::ConversionMode`。没有默认值，调用时必须提供。传入 `QMediaFormat::ConversionMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[invokable] QList<QMediaFormat::VideoCodec> QMediaFormat::supportedVideoCodecs(QMediaFormat::ConversionMode m)`

**API 类别：** 成员函数说明

**中文解读：** `QMediaFormat::supportedVideoCodecs` 用于计算、查询或取得与“supported、Video、Codecs”相关的操作。调用时要先确认当前状态和 `m` 的有效范围；返回类型是 `QList<QMediaFormat::VideoCodec>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QMediaFormat::VideoCodec>`。
- 参数 `m`：类型为 `QMediaFormat::ConversionMode`。没有默认值，调用时必须提供。传入 `QMediaFormat::ConversionMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QMediaFormat::swap(QMediaFormat &other)`

**API 类别：** 成员函数说明

**中文解读：** `QMediaFormat::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QMediaFormat &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMediaFormat::VideoCodec QMediaFormat::videoCodec() const`

**API 类别：** 成员函数说明

**中文解读：** `QMediaFormat::videoCodec` 用于计算、查询或取得与“video、Codec”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMediaFormat::VideoCodec`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMediaFormat::VideoCodec`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static invokable] QString QMediaFormat::videoCodecDescription(QMediaFormat::VideoCodec codec)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `videoCodecDescription`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `codec`：类型为 `QMediaFormat::VideoCodec`。没有默认值，调用时必须提供。传入 `QMediaFormat::VideoCodec` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static invokable] QString QMediaFormat::videoCodecName(QMediaFormat::VideoCodec codec)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `videoCodecName`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `codec`：类型为 `QMediaFormat::VideoCodec`。没有默认值，调用时必须提供。传入 `QMediaFormat::VideoCodec` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMediaFormat::operator!=(const QMediaFormat &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaFormat` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QMediaFormat &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QMediaFormat &QMediaFormat::operator=(QMediaFormat &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaFormat` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMediaFormat &`。
- 参数 `other`：类型为 `QMediaFormat &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QMediaFormat &QMediaFormat::operator=(const QMediaFormat &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaFormat` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMediaFormat &`。
- 参数 `other`：类型为 `const QMediaFormat &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMediaFormat::operator==(const QMediaFormat &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMediaFormat` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QMediaFormat &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMediaFormat::FileFormat fileFormat() const`

**API 类别：** 公有函数

**中文解读：** `QMediaFormat::fileFormat` 用于计算、查询或取得与“file、格式化”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMediaFormat::FileFormat`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMediaFormat::FileFormat`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setFileFormat(QMediaFormat::FileFormat f)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setFileFormat`。调用它会改变 `QMediaFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `f`：类型为 `QMediaFormat::FileFormat`。没有默认值，调用时必须提供。传入 `QMediaFormat::FileFormat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

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

`QMediaFormat` 所属机制类型：多媒体设备与会话机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
