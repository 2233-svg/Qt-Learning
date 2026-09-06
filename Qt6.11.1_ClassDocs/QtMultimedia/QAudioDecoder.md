# QAudioDecoder

> Qt 6.11.1 · Qt Multimedia

## 1. 先建立直觉

**一句话定位：** `QAudioDecoder` 是 Qt Multimedia 的“音频Decoder”类型，参与媒体源、设备、格式、播放/采集状态或音视频数据处理。

**模块背景：** Qt Multimedia 提供音频、视频、摄像头、媒体会话和设备访问能力。

### 这是什么

`QAudioDecoder` 是 多媒体设备与会话机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

**适用场景：** 先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

## 2. 依赖与对象关系

- 头文件：`#include <QAudioDecoder>`
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

- `enum Error { NoError, ResourceError, FormatError, AccessDeniedError, NotSupportedError }`

### 属性

- `bufferAvailable : bool`
- `error : QString`
- `isDecoding : bool`
- `source : QUrl`

### 公有函数

- `QAudioDecoder(QObject *parent = nullptr)`
- `virtual ~QAudioDecoder() override`
- `QAudioFormat audioFormat() const`
- `bool bufferAvailable() const`
- `qint64 duration() const`
- `QAudioDecoder::Error error() const`
- `QString errorString() const`
- `bool isDecoding() const`
- `bool isSupported() const`
- `qint64 position() const`
- `QAudioBuffer read() const`
- `void setAudioFormat(const QAudioFormat &format)`
- `void setSource(const QUrl &fileName)`
- `void setSourceDevice(QIODevice *device)`
- `QUrl source() const`
- `QIODevice * sourceDevice() const`

### 公有槽函数

- `void start()`
- `void stop()`

### 信号

- `void bufferAvailableChanged(bool available)`
- `void bufferReady()`
- `void durationChanged(qint64 duration)`
- `void error(QAudioDecoder::Error error)`
- `void finished()`
- `void formatChanged(const QAudioFormat &format)`
- `void isDecodingChanged(bool)`
- `void positionChanged(qint64 position)`
- `void sourceChanged()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QAudioDecoder::Error`

**作用与语义：**

定义了媒体播放器错误条件。
- `QAudioDecoder::NoError`：`0`;未发生错误。
- `QAudioDecoder::ResourceError`：`1`;媒体资源无法解决。
- `QAudioDecoder::FormatError`：`2`;不支持媒体资源的格式。
- `QAudioDecoder::AccessDeniedError`：`3`;播放媒体资源时没有合适的权限。
- `QAudioDecoder::NotSupportedError`：`4`;`QAudioDecoder` 不支持本平台

### `[read-only] bufferAvailable : bool`

**作用与语义：**

该属性适用于是否存在解码音频缓冲区。

**如何使用：** 调用 `bufferAvailable()` 读取当前值；它不会修改应用状态。

### `[read-only] error : QString`

**作用与语义：**

返回当前错误的人类可读描述，或者如果没有错误则返回空字符串。

**如何使用：** 调用 `error()` 读取当前值；它不会修改应用状态。

### `[read-only] isDecoding : bool`

**作用与语义：**

`true`解码器当前是否正在运行并解码音频数据。

**如何使用：** 调用 `isDecoding()` 读取当前值；它不会修改应用状态。

### `source : QUrl`

**作用与语义：**

该属性包含解码器对象正在解码的活跃文件名。

**如何使用：** 调用 `source()` 读取当前值；它不会修改应用状态。

### `[explicit] QAudioDecoder::QAudioDecoder(QObject *parent = nullptr)`

**作用与语义：**

构建一个带有`parent`的QAudioDecoder实例。

### `[override virtual noexcept] QAudioDecoder::~QAudioDecoder()`

**作用与语义：**

会破坏音频解码器对象。

### `QAudioFormat QAudioDecoder::audioFormat() const`

**作用与语义：**

返回解码器设置的音频格式。
注意：如果音频格式设置为无效，这可能与解码采样的格式不同。

### `bool QAudioDecoder::bufferAvailable() const`

**作用与语义：**

如果有缓冲区可供读取，返回真，否则返回假。如果没有缓冲区可用，调用`read()`函数会返回无效缓冲区。
注意：属性缓冲区的获取函数可用。

### `[signal] void QAudioDecoder::bufferAvailableChanged(bool available)`

**作用与语义：**

该属性适用于是否存在解码音频缓冲区。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `bufferAvailable` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QAudioDecoder::bufferReady()`

**作用与语义：**

新的解码音频缓冲区可以读取的信号。

### `qint64 QAudioDecoder::duration() const`

**作用与语义：**

返回音频流的总时长（以毫秒为单位），如果无法使用则返回-1。

### `[signal] void QAudioDecoder::durationChanged(qint64 duration)`

**作用与语义：**

这表明解码数据的估计`duration`发生了变化。

### `QAudioDecoder::Error QAudioDecoder::error() const`

**作用与语义：**

返回`QAudioDecoder`当前的错误状态。

### `[signal] void QAudioDecoder::error(QAudioDecoder::Error error)`

**作用与语义：**

表示出现了`error`状态。
注意：该信号重载。连接此信号：


使用 qOverload 连接：
connect（audioDecoder， qOverload（&QAudioDecoder：：error），。
receiver， &ReceiverClass：：slot）;

或者用λ：
connect（audioDecoder， qOverload（&QAudioDecoder：：error），。
this， []（QAudioDecoder：：Error error） { /* handle error */ }）;


更多示例和方法，请参见连接重载信号。

### `[signal] void QAudioDecoder::finished()`

**作用与语义：**

解码成功完成的信号。如果解码失败，则会发出错误信号。

### `[signal] void QAudioDecoder::formatChanged(const QAudioFormat &format)`

**作用与语义：**

解码器的当前音频格式已变为`format`信号。

### `bool QAudioDecoder::isSupported() const`

**作用与语义：**

回归真值：该平台支持音频解码。

### `qint64 QAudioDecoder::position() const`

**作用与语义：**

返回解码器最后读取缓冲区的位置（以毫秒为单位），如果没有读取缓冲区，则返回-1。

### `[signal] void QAudioDecoder::positionChanged(qint64 position)`

**作用与语义：**

提示解码器的当前`position`发生了变化。

### `QAudioBuffer QAudioDecoder::read() const`

**作用与语义：**

如果解码器有缓冲区，则读取该缓冲区。如果当前没有解码缓冲区可用，或失败时返回无效缓冲区。在这两种情况下，该函数都不会阻塞。
你应该在调用read()前先响应`bufferReady()`信号，或者检查`bufferAvailable()`函数，以确保获得有用数据。

### `void QAudioDecoder::setAudioFormat(const QAudioFormat &format)`

**作用与语义：**

将解码采样的音频格式设置为`format`。
该属性只能在解码器停止时设置。在其他时间设置该属性将被忽略。
如果解码器不支持此格式，`error()`将设置为`FormatError`。
如果不指定格式，则会使用解码音频本身的格式。否则，将进行某种格式转换。
如果你想将解码后的格式重置为原始音频文件格式，可以指定无效`format`。
警告：Android 后端尚未支持设置所需音频格式。它在默认的 FFMPEG 后端上是可使用的。

### `void QAudioDecoder::setSource(const QUrl &fileName)`

**作用与语义：**

该属性包含解码器对象正在解码的活跃文件名。

**如何使用：** 调用 `setSource(...)` 修改 `source`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QAudioDecoder::setSourceDevice(QIODevice *device)`

**作用与语义：**

将当前音频`QIODevice`设置为`device`。
当该属性被设置时，所有当前解码都会停止，所有音频缓冲区也会被丢弃。
你只能指定源文件名或源`QIODevice`。设置其中一个会重置另一个。

### `QUrl QAudioDecoder::source() const`

**作用与语义：**

返回当前文件名进行解码。如果调用了`setSourceDevice`，则该文件为空。
注意：属性来源的获取函数。

### `[signal] void QAudioDecoder::sourceChanged()`

**作用与语义：**

该属性包含解码器对象正在解码的活跃文件名。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `source` 的变化，不要把它当作普通函数主动调用。

### `QIODevice *QAudioDecoder::sourceDevice() const`

**作用与语义：**

如果设置了当前源 `QIODevice`，返回。如果调用了 `setSource()`，则为 nullptr。

### `[slot] void QAudioDecoder::start()`

**作用与语义：**

开始解码音频资源。
随着数据解码，当解码足够多时，`bufferReady()`信号会被发出。调用`read()`会返回一个音频缓冲区，且不会被阻塞。
如果你在缓冲区准备好之前调用`read()`，会返回一个无效缓冲区，同样不会被阻塞。

### `[slot] void QAudioDecoder::stop()`

**作用与语义：**

停止解码音频。再次调用`start()`会从头开始解码。

### `QString errorString() const`

**作用与语义：**

返回当前错误的人类可读描述，或者如果没有错误则返回空字符串。

**如何使用：** 调用 `errorString()` 读取当前值；它不会修改应用状态。

### `bool isDecoding() const`

**作用与语义：**

`true`解码器当前是否正在运行并解码音频数据。

**如何使用：** 调用 `isDecoding()` 读取当前值；它不会修改应用状态。

### `void isDecodingChanged(bool)`

**作用与语义：**

`true`解码器当前是否正在运行并解码音频数据。

**如何使用：** 调用 `isDecodingChanged()` 读取当前值；它不会修改应用状态。

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

`QAudioDecoder` 所属机制类型：多媒体设备与会话机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
