# QAudioSink

> Qt 6.11.1 · Qt Multimedia

## 1. 先建立直觉

**一句话定位：** `QAudioSink` 是 Qt Multimedia 的“音频Sink”类型，参与媒体源、设备、格式、播放/采集状态或音视频数据处理。

**模块背景：** Qt Multimedia 提供音频、视频、摄像头、媒体会话和设备访问能力。

### 这是什么

`QAudioSink` 是 多媒体设备与会话机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

**适用场景：** 先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

## 2. 依赖与对象关系

- 头文件：`#include <QAudioSink>`
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

### 公有函数

- `QAudioSink(const QAudioFormat &format = QAudioFormat(), QObject *parent = nullptr)`
- `QAudioSink(const QAudioDevice &audioDevice, const QAudioFormat &format = QAudioFormat(), QObject *parent = nullptr)`
- `virtual ~QAudioSink() override`
- `(since 6.10) qsizetype bufferFrameCount() const`
- `qsizetype bufferSize() const`
- `qsizetype bytesFree() const`
- `qint64 elapsedUSecs() const`
- `QtAudio::Error error() const`
- `QAudioFormat format() const`
- `(since 6.10) qsizetype framesFree() const`
- `bool isNull() const`
- `qint64 processedUSecs() const`
- `void reset()`
- `void resume()`
- `(since 6.10) void setBufferFrameCount(qsizetype value)`
- `void setBufferSize(qsizetype value)`
- `void setVolume(qreal volume)`
- `QIODevice * start()`
- `(since 6.11) void start(Callback &&cb)`
- `void start(QIODevice *device)`
- `QtAudio::State state() const`
- `void stop()`
- `void suspend()`
- `qreal volume() const`

### 信号

- `void stateChanged(QtAudio::State state)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QAudioSink::QAudioSink(const QAudioFormat &format = QAudioFormat(), QObject *parent = nullptr)`

**作用与语义：**

构建一个新的音频输出并将其连接到`parent`。默认音频输出设备与输出`format`参数一起使用。如果`format`为默认初始化，格式将设置为音频设备的首选格式。

### `[explicit] QAudioSink::QAudioSink(const QAudioDevice &audioDevice, const QAudioFormat &format = QAudioFormat(), QObject *parent = nullptr)`

**作用与语义：**

构建一个新的音频输出并将其连接到`parent`。`audioDevice`引用的设备与输出`format`参数一起使用。如果`format`为默认初始化，格式将设置为`audioDevice`的首选格式。

### `[override virtual noexcept] QAudioSink::~QAudioSink()`

**作用与语义：**

这会破坏音频输出。
这样可以释放所有系统资源并释放所有缓冲区。

### `[since 6.10] qsizetype QAudioSink::bufferFrameCount() const`

**作用与语义：**

返回音频缓冲区大小（帧数）。
如果在`start()`之前调用，返回平台默认值。如果在`start()`之前调用，但`setBufferSize()`或`setBufferFrameCount()`先被调用，返回由`setBufferSize()`或`setBufferFrameCount()`设定的值。如果在`start()`之后调用，返回实际使用的缓冲区大小。这可能不是之前由`setBufferSize()`或`setBufferFrameCount()`设定的。

### `qsizetype QAudioSink::bufferSize() const`

**作用与语义：**

返回音频缓冲区大小（字节单位）。
如果在`start()`之前调用，返回平台默认值。如果在`start()`之前调用，但之前调用了`setBufferSize()`或`setBufferFrameCount()`，返回由`setBufferSize()`或`setBufferFrameCount()`设定的值。如果在`start()`之后调用，返回实际使用的缓冲区大小。这可能不是之前`setBufferSize()`或`setBufferFrameCount()`设置的。

### `qsizetype QAudioSink::bytesFree() const`

**作用与语义：**

返回音频缓冲区中可用的可用字节数。
注意：返回的值仅在`QtAudio::ActiveState`或`QtAudio::IdleState`状态时有效，否则返回零。

### `qint64 QAudioSink::elapsedUSecs() const`

**作用与语义：**

返回自调用`start()`以来的微秒，包括闲置和暂停状态的时间。

### `QtAudio::Error QAudioSink::error() const`

**作用与语义：**

返回错误状态。

### `QAudioFormat QAudioSink::format() const`

**作用与语义：**

退还正在使用的`QAudioFormat`。

### `[since 6.10] qsizetype QAudioSink::framesFree() const`

**作用与语义：**

返回音频缓冲区中可用的空闲帧数。
注意：返回的值仅在`QtAudio::ActiveState`或`QtAudio::IdleState`状态时有效，否则返回零。

### `bool QAudioSink::isNull() const`

**作用与语义：**

返回`true`是实例被`null` `QAudioSink`，否则返回`false`。

### `qint64 QAudioSink::processedUSecs() const`

**作用与语义：**

返回自调用`start()`以来处理的音频数据量（以微秒计）。

### `void QAudioSink::reset()`

**作用与语义：**

立即停止音频输出，并丢弃缓冲区中当前所有的音频数据。所有推送到`QIODevice`的待处理音频数据都被忽略。

### `void QAudioSink::resume()`

**作用与语义：**

在一`suspend()`后恢复音频数据处理。
将`state()`设置为调用时的状态`suspend()`。如果音频接收器的状态不`QtAudio::SuspendedState`，这个函数就没有任何作用。

### `[since 6.10] void QAudioSink::setBufferFrameCount(qsizetype value)`

**作用与语义：**

将音频缓冲区大小设置为帧数`value`。
注意：该函数可以在 `start()` 之前的任何时候调用。`start()` 后对该函数的调用将被忽略。不应假设缓冲区大小设置是实际使用的缓冲区大小——在 `start()` 之后随时调用 `bufferFrameCount()` 以返回实际使用的缓冲区大小。

### `void QAudioSink::setBufferSize(qsizetype value)`

**作用与语义：**

将音频缓冲区大小设置为`value`字节。
注意：该函数可以在`start()`之前的任何时间调用。调用该函数的调用在`start()`后被忽略。不应假设缓冲区大小设置为实际使用的缓冲区大小——在`start()`之后随时调用`bufferSize()`以返回实际使用的缓冲区大小。

### `void QAudioSink::setVolume(qreal volume)`

**作用与语义：**

输出音量设置为`volume`。
音量按线性比例从`0.0`（静音）到`1.0`（满音量）进行调整。超出该范围的数值将被夹紧。
默认音量是`1.0`。
注意：音量调整会改变该音频流的音量，而非全局音量。
UI音量控制通常应非线性缩放。例如，使用对数刻度会产生感知响度的线性变化，这也是用户通常对音量控制的预期。更多详情请参见 `QtAudio::convertVolume()`。

### `QIODevice *QAudioSink::start()`

**作用与语义：**

返回指向用于传输数据到系统音频输出的内部`QIODevice`的指针。设备已经打开，`write()`可以直接写入数据。
注意：当直播被停止或你开始另一个直播时，指针将失效。
如果`QAudioSink`能够访问系统的音频设备，`state()`返回`QtAudio::IdleState`，`error()`返回`QtAudio::NoError`，`stateChanged()`信号发出。
如果在此过程中出现问题，返回`error()` `QtAudio::OpenError`，返回`state()`返回 `QtAudio::StoppedState`，`stateChanged()`信号被发射。

### `[since 6.11] template <typename Callback, QtAudio::if_audio_sink_callback<Callback> = true> void QAudioSink::start(Callback &&cb)`

**作用与语义：**

以一个回调函数开始`QAudioSink`，调用在软实时音频线程上。回调是一个可调用的，参数为<SampleType>`QSpan`，SampleType必须匹配`QAudioSink`格式的 `QAudioFormat::SampleFormat`。该区间需要填充交错音频数据。
如果`QAudioSink`成功启动，`error()`返回`QtAudio::NoError`。
如果在此过程中出现问题，`error()`返回`QtAudio::OpenError`，`state()`返回`QtAudio::StoppedState`，`stateChanged()`信号被发射。
注意：该 API 仅支持回调 API 的平台：苹果的 CoreAudio（macOS、iOS 等）、Windows、Linux（使用 PulseAudio 或 PipeWire 后端）和 Android。
注意：回调将在软实时音频线程中调用。确保回调不会阻塞非常重要，因为这可能导致音频故障或断线。这包括执行阻塞IO、锁定互斥、分配内存或其他可能阻塞的操作。最佳实践请参阅Ross Bencina的文章《实时音频编程101：时间等待无效》。还可考虑使用clang的实时净化工具来验证音频回调。

### `void QAudioSink::start(QIODevice *device)`

**作用与语义：**

开始将音频数据从`device`传输到系统的音频输出。`device`必须在`ReadOnly`或`ReadWrite`模式下打开。
如果`QAudioSink`能够成功输出音频数据，`state()`返回`QtAudio::ActiveState`，`error()`返回`QtAudio::NoError`，`stateChanged()`信号被发射。
如果在此过程中出现问题，`error()`返回`QtAudio::OpenError`，`state()`返回`QtAudio::StoppedState`，`stateChanged()`信号被发射。

### `QtAudio::State QAudioSink::state() const`

**作用与语义：**

返回音频处理状态。

### `[signal] void QAudioSink::stateChanged(QtAudio::State state)`

**作用与语义：**

当设备`state`发生变化时，该信号会发出。这是音频输出的当前状态。
注意：`QtAudio`命名空间在Qt 6.6之前称为QAudio。基于字符串的连接必须使用`QAudio::State`作为参数类型：`connect(source, SIGNAL(stateChanged(QAudio::State)), ...);`。

### `void QAudioSink::stop()`

**作用与语义：**

停止音频输出，脱离系统资源。
将`error()`设为`QtAudio::NoError`，`state()`转为`QtAudio::StoppedState`并发出`stateChanged()`信号。
注意：在Linux和Darwin上，此操作会同步耗尽底层音频缓冲区，可能导致缓冲区负载相应延迟。要立即重置所有缓冲区，请使用`reset`方法。

### `void QAudioSink::suspend()`

**作用与语义：**

停止处理音频数据，保留缓冲音频数据。
将`state()`设为`QtAudio::SuspendedState`并发出`stateChanged()`信号。

### `qreal QAudioSink::volume() const`

**作用与语义：**

返回0.0到1.0之间的体积。

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

`QAudioSink` 所属机制类型：多媒体设备与会话机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
