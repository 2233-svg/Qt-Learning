# QAudioBuffer

> Qt 6.11.1 · Qt Multimedia

## 1. 先建立直觉

**一句话定位：** `QAudioBuffer` 是 Qt Multimedia 的“音频缓冲区”类型，参与媒体源、设备、格式、播放/采集状态或音视频数据处理。

**模块背景：** Qt Multimedia 提供音频、视频、摄像头、媒体会话和设备访问能力。

### 这是什么

`QAudioBuffer` 是 多媒体设备与会话机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

**适用场景：** 先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

## 2. 依赖与对象关系

- 头文件：`#include <QAudioBuffer>`
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

- `F32M`
- `F32S`
- `S16M`
- `S16S`
- `S32M`
- `S32S`
- `U8M`
- `U8S`

### 公有函数

- `QAudioBuffer()`
- `QAudioBuffer(const QByteArray &data, const QAudioFormat &format, qint64 startTime = -1)`
- `QAudioBuffer(int numFrames, const QAudioFormat &format, qint64 startTime = -1)`
- `QAudioBuffer(const QAudioBuffer &other)`
- `QAudioBuffer(QAudioBuffer &&other)`
- `~QAudioBuffer()`
- `qsizetype byteCount() const`
- `const T * constData() const`
- `T * data()`
- `const T * data() const`
- `void detach()`
- `qint64 duration() const`
- `QAudioFormat format() const`
- `qsizetype frameCount() const`
- `bool isValid() const`
- `qsizetype sampleCount() const`
- `qint64 startTime() const`
- `void swap(QAudioBuffer &other)`
- `QAudioBuffer & operator=(QAudioBuffer &&other)`
- `QAudioBuffer & operator=(const QAudioBuffer &other)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QAudioBuffer::F32M`

**作用与语义：**

这是32位浮点单声采样的预定义专用。

### `QAudioBuffer::F32S`

**作用与语义：**

这是针对32位浮点立体声采样的预设专用化。

### `QAudioBuffer::S16M`

**作用与语义：**

这是预定义的16位单声道采样专用。i。

### `QAudioBuffer::S16S`

**作用与语义：**

这是为带号立体声16位采样预定义的专用化。每个通道都是带符号短路。

### `QAudioBuffer::S32M`

**作用与语义：**

这是对带号32位单声道采样的预定义专用化。

### `QAudioBuffer::S32S`

**作用与语义：**

这是针对有符号32位立体声采样的预先确定的专用化。

### `QAudioBuffer::U8M`

**作用与语义：**

这是对无符号8位单声道采样的预定义专用化。

### `QAudioBuffer::U8S`

**作用与语义：**

这是对无符号8位立体声采样的预先定义专用。

### `[noexcept] QAudioBuffer::QAudioBuffer()`

**作用与语义：**

创建一个新的、空的、无效的缓冲区。

### `QAudioBuffer::QAudioBuffer(const QByteArray &data, const QAudioFormat &format, qint64 startTime = -1)`

**作用与语义：**

在给定`format`中，从提供的`data`创建新的音频缓冲区。格式决定了采样的数量和大小如何从`data`中解读。
如果提供的`data`不是计算帧大小的整数倍，则多余的数据将不被使用。
这个音频缓冲区会复制`data`的内容。
`startTime`（以微秒计）表示该缓冲区在流中的起始时间。如果该缓冲区不属于流，则将其设置为-1。

### `QAudioBuffer::QAudioBuffer(int numFrames, const QAudioFormat &format, qint64 startTime = -1)`

**作用与语义：**

创建一个新的音频缓冲区，为给定`format`的`numFrames`帧留出空间。每个采样将初始化为该格式的默认格式。
`startTime`（以微秒计）表示该缓冲区在流中的起始时间。如果该缓冲区不属于流，则将其设置为-1。

### `[noexcept] QAudioBuffer::QAudioBuffer(const QAudioBuffer &other)`

**作用与语义：**

从`other`创建一个新的音频缓冲区。音频缓冲区是明确共享的，你应该调用缓冲区上的`detach()`来复制一个可以修改的副本。

### `[constexpr noexcept] QAudioBuffer::QAudioBuffer(QAudioBuffer &&other)`

**作用与语义：**

通过从`other`移动构建QAudio缓冲区。

### `[noexcept] QAudioBuffer::~QAudioBuffer()`

**作用与语义：**

会破坏这个音频缓冲区。

### `[noexcept] qsizetype QAudioBuffer::byteCount() const`

**作用与语义：**

返回缓冲区的大小，单位为字节。

### `template <typename T> const T *QAudioBuffer::constData() const`

**作用与语义：**

返回指向该缓冲区数据的指针。你只能读取它。
这种方法比const版本的`data()`更受青睐，以防止不必要的复制。
请注意，音频缓冲区的格式并未进行检查——这只是方便的功能。

**官方示例：**

```cpp
 // With a 16bit sample buffer:
 const quint16 *data = buffer->constData<quint16>();
```

### `template <typename T> T *QAudioBuffer::data()`

**作用与语义：**

返回该缓冲区数据的指针。你可以通过返回的指针修改数据。
由于`QAudioBuffer`对象是显式共享的，通常在通过该函数修改数据前应先调用`detach()`。
请注意，音频缓冲区的格式并未进行检查——这只是方便的功能。

**官方示例：**

```cpp
 // With a 16bit sample buffer:
 quint16 *data = buffer->data<quint16>(); // May cause deep copy
```

### `template <typename T> const T *QAudioBuffer::data() const`

**作用与语义：**

返回指向该缓冲区数据的指针。你只能读取它。
你应该用`constData()`功能来防止意外深度复制。
请注意，音频缓冲区的格式并未进行检查——这只是方便的功能。

**官方示例：**

```cpp
 // With a 16bit sample const buffer:
 const quint16 *data = buffer->data<quint16>();
```

### `void QAudioBuffer::detach()`

**作用与语义：**

将这些音频缓冲区从可能共享数据的其他副本中分离出来。

### `[noexcept] qint64 QAudioBuffer::duration() const`

**作用与语义：**

返回该缓冲区内音频的时长，单位为微秒。
这取决于`format()`和`frameCount()`。

### `[noexcept] QAudioFormat QAudioBuffer::format() const`

**作用与语义：**

返回该缓冲区的 `format`。
该格式的若干特性影响`duration()`或`byteCount()`如何从`frameCount()`计算。

### `[noexcept] qsizetype QAudioBuffer::frameCount() const`

**作用与语义：**

返回该缓冲区中完整音频帧的数量。
音频帧是同一时间点每个通道交错出现一个采样的集合。

### `[noexcept] bool QAudioBuffer::isValid() const`

**作用与语义：**

如果缓冲区有效，则返回为真。有效的缓冲区包含超过零的帧数且格式有效。

### `[noexcept] qsizetype QAudioBuffer::sampleCount() const`

**作用与语义：**

返回缓冲区中的采样数量。
如果缓冲区格式包含多个通道，那么这个计数包括所有通道。这意味着一个总共1000个采样的立体声缓冲区会有500个左采样和500个右采样（交错），这个函数会返回1000个采样。

### `[noexcept] qint64 QAudioBuffer::startTime() const`

**作用与语义：**

返回该缓冲区在流中起始的时间（以微秒计）。
如果该缓冲区不属于流，则返回 -1。

### `[noexcept] void QAudioBuffer::swap(QAudioBuffer &other)`

**作用与语义：**

把音频缓冲区换成`other`。

### `[noexcept] QAudioBuffer &QAudioBuffer::operator=(QAudioBuffer &&other)`

**作用与语义：**

这`other`进入了这个`QAudioBuffer`。

### `QAudioBuffer &QAudioBuffer::operator=(const QAudioBuffer &other)`

**作用与语义：**

将`other`缓冲区分配给该缓冲区。

### `F32M`

**作用与语义：**

这是32位浮点单声采样的预定义专用。

### `F32S`

**作用与语义：**

这是针对32位浮点立体声采样的预设专用化。

### `S16M`

**作用与语义：**

这是预定义的16位单声道采样专用。i。

### `S16S`

**作用与语义：**

这是为带号立体声16位采样预定义的专用化。每个通道都是带符号短路。

### `S32M`

**作用与语义：**

这是对带号32位单声道采样的预定义专用化。

### `S32S`

**作用与语义：**

这是针对有符号32位立体声采样的预先确定的专用化。

### `U8M`

**作用与语义：**

这是对无符号8位单声道采样的预定义专用化。

### `U8S`

**作用与语义：**

这是对无符号8位立体声采样的预先定义专用。

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

`QAudioBuffer` 所属机制类型：多媒体设备与会话机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
