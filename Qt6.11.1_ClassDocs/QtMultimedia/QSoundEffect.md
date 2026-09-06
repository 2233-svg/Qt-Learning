# QSoundEffect

> Qt 6.11.1 · Qt Multimedia

## 1. 先建立直觉

**一句话定位：** `QSoundEffect` 是 Qt Multimedia 的“声音效果”类型，参与媒体源、设备、格式、播放/采集状态或音视频数据处理。

**模块背景：** Qt Multimedia 提供音频、视频、摄像头、媒体会话和设备访问能力。

### 这是什么

`QSoundEffect` 是 多媒体设备与会话机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

**适用场景：** 先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

## 2. 依赖与对象关系

- 头文件：`#include <QSoundEffect>`
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

- `enum Loop { Infinite }`
- `enum Status { Null, Loading, Ready, Error }`

### 属性

- `audioDevice : QAudioDevice`
- `loops : int`
- `loopsRemaining : int`
- `muted : bool`
- `playing : bool`
- `source : QUrl`
- `status : Status`
- `volume : float`

### 公有函数

- `QSoundEffect(QObject *parent = nullptr)`
- `QSoundEffect(const QAudioDevice &audioDevice, QObject *parent = nullptr)`
- `virtual ~QSoundEffect() override`
- `QAudioDevice audioDevice()`
- `bool isLoaded() const`
- `bool isMuted() const`
- `bool isPlaying() const`
- `int loopCount() const`
- `int loopsRemaining() const`
- `void setAudioDevice(const QAudioDevice &device)`
- `void setLoopCount(int loopCount)`
- `void setMuted(bool muted)`
- `void setSource(const QUrl &url)`
- `void setVolume(float volume)`
- `QUrl source() const`
- `QSoundEffect::Status status() const`
- `float volume() const`

### 公有槽函数

- `void play()`
- `void stop()`

### 信号

- `void audioDeviceChanged()`
- `void loadedChanged()`
- `void loopCountChanged()`
- `void loopsRemainingChanged()`
- `void mutedChanged()`
- `void playingChanged()`
- `void sourceChanged()`
- `void statusChanged()`
- `void volumeChanged()`

### 静态公有成员

- `QStringList supportedMimeTypes()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `audioDevice : QAudioDevice`

**作用与语义：**

返回`QAudioDevice`实例。

**如何使用：** 调用 `audioDevice()` 读取当前值；它不会修改应用状态。

### `loops : int`

**作用与语义：**

该属性表示声音被播放的次数。值为0或1时，声音只会播放一次;设置为`SoundEffect`。无限以实现无限循环。
音效播放时可以更改数值，此时剩余循环会更新为新值。

**如何使用：** 调用 `loops()` 读取当前值；它不会修改应用状态。

### `[read-only] loopsRemaining : int`

**作用与语义：**

该属性包含音效停止前剩余的循环数，或者如果`loops`设置了，则为`QSoundEffect::Infinite`。

**如何使用：** 调用 `loopsRemaining()` 读取当前值；它不会修改应用状态。

### `muted : bool`

**作用与语义：**

该特性提供了控制静音的方法。值为`true`时，可以静音该效果。

**如何使用：** 调用 `muted()` 读取当前值；它不会修改应用状态。

### `[read-only] playing : bool`

**作用与语义：**

该特性指示音效是否在播放。

**如何使用：** 调用 `playing()` 读取当前值；它不会修改应用状态。

### `source : QUrl`

**作用与语义：**

此属性保存要播放的声音的 URL。要让 `SoundEffect` 尝试加载该源，URL 必须存在，并且应用程序必须在指定目录中具有读取权限。

**如何使用：** 调用 `source()` 读取当前值；它不会修改应用状态。

### `[read-only] status : Status`

**作用与语义：**

该属性表示`QSoundEffect::Status`枚举中音效的当前状态。

**如何使用：** 调用 `status()` 读取当前值；它不会修改应用状态。

### `volume : float`

**作用与语义：**

该特性保持音效播放的音量，范围从0.0（静音）到1.0（全音量）。

**如何使用：** 调用 `volume()` 读取当前值；它不会修改应用状态。

### `[explicit] QSoundEffect::QSoundEffect(QObject *parent = nullptr)`

**作用与语义：**

与给定`parent`创建QSoundEffect。

### `[explicit] QSoundEffect::QSoundEffect(const QAudioDevice &audioDevice, QObject *parent = nullptr)`

**作用与语义：**

生成带有给定`audioDevice`和`parent`的QSoundEffect。

### `[override virtual noexcept] QSoundEffect::~QSoundEffect()`

**作用与语义：**

破坏了这个音效。

### `bool QSoundEffect::isLoaded() const`

**作用与语义：**

返回音效是否加载完成`source()`。

### `bool QSoundEffect::isMuted() const`

**作用与语义：**

该特性提供了控制静音的方法。值为`true`时，可以静音该效果。

**如何使用：** 调用 `isMuted()` 读取当前值；它不会修改应用状态。

### `bool QSoundEffect::isPlaying() const`

**作用与语义：**

该特性指示音效是否在播放。

**如何使用：** 调用 `isPlaying()` 读取当前值；它不会修改应用状态。

### `[signal] void QSoundEffect::loadedChanged()`

**作用与语义：**

当加载状态发生变化时，`loadedChanged`信号会发出。

### `int QSoundEffect::loopCount() const`

**作用与语义：**

该属性表示声音被播放的次数。值为0或1时，声音只会播放一次;设置为`SoundEffect`。无限以实现无限循环。
音效播放时可以更改数值，此时剩余循环会更新为新值。

**如何使用：** 调用 `loopCount()` 读取当前值；它不会修改应用状态。

### `[signal] void QSoundEffect::loopCountChanged()`

**作用与语义：**

该属性表示声音被播放的次数。值为0或1时，声音只会播放一次;设置为`SoundEffect`。无限以实现无限循环。
音效播放时可以更改数值，此时剩余循环会更新为新值。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `loops` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QSoundEffect::loopsRemainingChanged()`

**作用与语义：**

该属性包含音效停止前剩余的循环数，或者如果`loops`设置了，则为`QSoundEffect::Infinite`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `loopsRemaining` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QSoundEffect::mutedChanged()`

**作用与语义：**

该特性提供了控制静音的方法。值为`true`时，可以静音该效果。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `muted` 的变化，不要把它当作普通函数主动调用。

### `[slot] void QSoundEffect::play()`

**作用与语义：**

开始播放音效，循环播放效果，按照循环属性指定次数。

### `[signal] void QSoundEffect::playingChanged()`

**作用与语义：**

该特性指示音效是否在播放。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `playing` 的变化，不要把它当作普通函数主动调用。

### `void QSoundEffect::setLoopCount(int loopCount)`

**作用与语义：**

该属性表示声音被播放的次数。值为0或1时，声音只会播放一次;设置为`SoundEffect`。无限以实现无限循环。
音效播放时可以更改数值，此时剩余循环会更新为新值。

**如何使用：** 调用 `setLoopCount(...)` 修改 `loops`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QSoundEffect::setMuted(bool muted)`

**作用与语义：**

该特性提供了控制静音的方法。值为`true`时，可以静音该效果。

**如何使用：** 调用 `setMuted(...)` 修改 `muted`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QSoundEffect::setSource(const QUrl &url)`

**作用与语义：**

此属性保存要播放的声音的 URL。要让 `SoundEffect` 尝试加载该源，URL 必须存在，并且应用程序必须在指定目录中具有读取权限。

**如何使用：** 调用 `setSource(...)` 修改 `source`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QSoundEffect::setVolume(float volume)`

**作用与语义：**

该特性保持音效播放的音量，范围从0.0（静音）到1.0（全音量）。

**如何使用：** 调用 `setVolume(...)` 修改 `volume`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QUrl QSoundEffect::source() const`

**作用与语义：**

返回当前播放源的URL。
注意：属性来源的获取函数。

### `[signal] void QSoundEffect::sourceChanged()`

**作用与语义：**

此属性保存要播放的声音的 URL。要让 `SoundEffect` 尝试加载该源，URL 必须存在，并且应用程序必须在指定目录中具有读取权限。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `source` 的变化，不要把它当作普通函数主动调用。

### `QSoundEffect::Status QSoundEffect::status() const`

**作用与语义：**

返回该音效的当前状态。
注意：物业状态的获取函数。

### `[signal] void QSoundEffect::statusChanged()`

**作用与语义：**

该属性表示`QSoundEffect::Status`枚举中音效的当前状态。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `status` 的变化，不要把它当作普通函数主动调用。

### `[slot] void QSoundEffect::stop()`

**作用与语义：**

停止当前播放。

### `[static] QStringList QSoundEffect::supportedMimeTypes()`

**作用与语义：**

返回该平台支持的哑剧类型列表。

### `float QSoundEffect::volume() const`

**作用与语义：**

返回该音效当前音量，从0.0（静音）到1.0（最大音量）。
注意：属性体积的获取函数。

### `[signal] void QSoundEffect::volumeChanged()`

**作用与语义：**

该特性保持音效播放的音量，范围从0.0（静音）到1.0（全音量）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `volume` 的变化，不要把它当作普通函数主动调用。

### `enum Loop { Infinite }`

**作用与语义：**

- `QSoundEffect::Infinite`：`-2`;用作`setLoopCount()`无限循环的参数

### `enum Status { Null, Loading, Ready, Error }`

**作用与语义：**

- `QSoundEffect::Null`：`0`;未设置任何源或源为空。
- `QSoundEffect::Loading`：`1`;`SoundEffect`正在尝试加载源代码。
- `QSoundEffect::Ready`：`2`;源代码已加载并准备播放。
- `QSoundEffect::Error`：`3`;运行过程中发生错误，例如源加载失败。

### `QAudioDevice audioDevice()`

**作用与语义：**

返回`QAudioDevice`实例。

**如何使用：** 调用 `audioDevice()` 读取当前值；它不会修改应用状态。

### `int loopsRemaining() const`

**作用与语义：**

该属性包含音效停止前剩余的循环数，或者如果`loops`设置了，则为`QSoundEffect::Infinite`。

**如何使用：** 调用 `loopsRemaining()` 读取当前值；它不会修改应用状态。

### `void setAudioDevice(const QAudioDevice &device)`

**作用与语义：**

返回`QAudioDevice`实例。

**如何使用：** 调用 `setAudioDevice(...)` 修改 `audioDevice`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void audioDeviceChanged()`

**作用与语义：**

返回`QAudioDevice`实例。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `audioDevice` 的变化，不要把它当作普通函数主动调用。

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

`QSoundEffect` 所属机制类型：多媒体设备与会话机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
