# QAudioEngine

> Qt 6.11.1 · Qt Spatial Audio

## 1. 先建立直觉

**一句话定位：** `QAudioEngine` 是 Qt Multimedia 的“音频引擎”类型，参与媒体源、设备、格式、播放/采集状态或音视频数据处理。

**模块背景：** 这是 Qt Spatial Audio 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QAudioEngine` 是 多媒体设备与会话机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

**适用场景：** 先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

## 2. 依赖与对象关系

- 头文件：`#include <QAudioEngine>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS SpatialAudio)
target_link_libraries(mytarget PRIVATE Qt6::SpatialAudio)
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

- `enum OutputMode { Surround, Stereo, Headphone }`

### 属性

- `distanceScale : float`
- `masterVolume : float`
- `outputDevice : QAudioDevice`
- `outputMode : OutputMode`
- `paused : bool`

### 公有函数

- `QAudioEngine()`
- `QAudioEngine(QObject *parent)`
- `QAudioEngine(int sampleRate, QObject *parent = nullptr)`
- `virtual ~QAudioEngine() override`
- `float distanceScale() const`
- `float masterVolume() const`
- `QAudioDevice outputDevice() const`
- `QAudioEngine::OutputMode outputMode() const`
- `bool paused() const`
- `bool roomEffectsEnabled() const`
- `int sampleRate() const`
- `void setDistanceScale(float scale)`
- `void setMasterVolume(float volume)`
- `void setOutputDevice(const QAudioDevice &device)`
- `void setOutputMode(QAudioEngine::OutputMode mode)`
- `void setPaused(bool paused)`
- `void setRoomEffectsEnabled(bool enabled)`

### 公有槽函数

- `void pause()`
- `void resume()`
- `void start()`
- `void stop()`

### 信号

- `void distanceScaleChanged()`
- `void masterVolumeChanged()`
- `void outputDeviceChanged()`
- `void outputModeChanged()`
- `void pausedChanged()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `distanceScale : float`

**作用与语义：**

定义空间音频引擎所使用的坐标系的比例尺。默认情况下，所有单位均以厘米为单位，与 Qt Quick 3D 默认单位一致。
将距离刻度设置为QAudioEngine：:D istanceScaleMeter，以获得单位单位（米）。

**如何使用：** 调用 `distanceScale()` 读取当前值；它不会修改应用状态。

### `masterVolume : float`

**作用与语义：**

设置或返回用于渲染声场的音量。

**如何使用：** 调用 `masterVolume()` 读取当前值；它不会修改应用状态。

### `outputDevice : QAudioDevice`

**作用与语义：**

设置或返回用于播放声场的设备。

**如何使用：** 调用 `outputDevice()` 读取当前值；它不会修改应用状态。

### `outputMode : OutputMode`

**作用与语义：**

设置或取回发动机的电流输出模式。

**如何使用：** 调用 `outputMode()` 读取当前值；它不会修改应用状态。

### `paused : bool`

**作用与语义：**

暂停空间音频引擎。

**如何使用：** 调用 `paused()` 读取当前值；它不会修改应用状态。

### `[explicit] QAudioEngine::QAudioEngine(int sampleRate, QObject *parent = nullptr)`

**作用与语义：**

构建一个包含`parent`（如果有的话）的空间音频引擎。
发动机将以`sampleRate`给出的采样率运行。如果没有采样率，默认采样率为44100（44.1kHz）。
未以该采样率提供的声音内容，在引擎处理时会自动重新采样为`sampleRate`。默认采样率在大多数情况下是可以的，但如果大多数声音文件采样率不同，你可以自定义不同的采样率，避免重采样时的CPU开销。

### `[override virtual noexcept] QAudioEngine::~QAudioEngine()`

**作用与语义：**

摧毁了空间音频引擎。

### `[slot] void QAudioEngine::pause()`

**作用与语义：**

暂停播放。

### `[slot] void QAudioEngine::resume()`

**作用与语义：**

恢复播放。

### `bool QAudioEngine::roomEffectsEnabled() const`

**作用与语义：**

如果启用了房间效果，则返回为真。

### `int QAudioEngine::sampleRate() const`

**作用与语义：**

返回引擎配置时的采样率。

### `void QAudioEngine::setRoomEffectsEnabled(bool enabled)`

**作用与语义：**

启用回声和混响等房间效果。
如果`enabled`为真，则启用房间效果。房间效果只有在你创建了一个或多个`QAudioRoom`对象且监听者至少在其中一个房间时才适用。如果监听者在多个房间内，则使用音量最小的房间。

### `[slot] void QAudioEngine::start()`

**作用与语义：**

启动引擎。

### `[slot] void QAudioEngine::stop()`

**作用与语义：**

发动机停了。

### `enum OutputMode { Surround, Stereo, Headphone }`

**作用与语义：**

- `QAudioEngine::Surround`：`0`;将声音映射到输出设备的扬声器配置。这通常是立体声或环绕扬声器的设置。
- `QAudioEngine::Stereo`：`1`;将声音映射到输出设备的立体声扬声器配置。这样可以忽略任何额外的扬声器，只使用左右声道来创建声场的强烈渲染。
- `QAudioEngine::Headphone`：`2`;使用耳机空间化在通过耳机听声场时创造3D音频效果

### `QAudioEngine()`

**作用与语义：**

构建一个包含`parent`（如果有的话）的空间音频引擎。
发动机将以`sampleRate`给出的采样率运行。如果没有采样率，默认采样率为44100（44.1kHz）。
未以该采样率提供的声音内容，在引擎处理时会自动重新采样为`sampleRate`。默认采样率在大多数情况下是可以的，但如果大多数声音文件采样率不同，你可以自定义不同的采样率，避免重采样时的CPU开销。

### `QAudioEngine(QObject *parent)`

**作用与语义：**

构建一个包含`parent`（如果有的话）的空间音频引擎。
发动机将以`sampleRate`给出的采样率运行。如果没有采样率，默认采样率为44100（44.1kHz）。
未以该采样率提供的声音内容，在引擎处理时会自动重新采样为`sampleRate`。默认采样率在大多数情况下是可以的，但如果大多数声音文件采样率不同，你可以自定义不同的采样率，避免重采样时的CPU开销。

### `float distanceScale() const`

**作用与语义：**

定义空间音频引擎所使用的坐标系的比例尺。默认情况下，所有单位均以厘米为单位，与 Qt Quick 3D 默认单位一致。
将距离刻度设置为QAudioEngine：:D istanceScaleMeter，以获得单位单位（米）。

**如何使用：** 调用 `distanceScale()` 读取当前值；它不会修改应用状态。

### `float masterVolume() const`

**作用与语义：**

设置或返回用于渲染声场的音量。

**如何使用：** 调用 `masterVolume()` 读取当前值；它不会修改应用状态。

### `QAudioDevice outputDevice() const`

**作用与语义：**

设置或返回用于播放声场的设备。

**如何使用：** 调用 `outputDevice()` 读取当前值；它不会修改应用状态。

### `QAudioEngine::OutputMode outputMode() const`

**作用与语义：**

设置或取回发动机的电流输出模式。

**如何使用：** 调用 `outputMode()` 读取当前值；它不会修改应用状态。

### `bool paused() const`

**作用与语义：**

暂停空间音频引擎。

**如何使用：** 调用 `paused()` 读取当前值；它不会修改应用状态。

### `void setDistanceScale(float scale)`

**作用与语义：**

定义空间音频引擎所使用的坐标系的比例尺。默认情况下，所有单位均以厘米为单位，与 Qt Quick 3D 默认单位一致。
将距离刻度设置为QAudioEngine：:D istanceScaleMeter，以获得单位单位（米）。

**如何使用：** 调用 `setDistanceScale(...)` 修改 `distanceScale`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMasterVolume(float volume)`

**作用与语义：**

设置或返回用于渲染声场的音量。

**如何使用：** 调用 `setMasterVolume(...)` 修改 `masterVolume`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setOutputDevice(const QAudioDevice &device)`

**作用与语义：**

设置或返回用于播放声场的设备。

**如何使用：** 调用 `setOutputDevice(...)` 修改 `outputDevice`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setOutputMode(QAudioEngine::OutputMode mode)`

**作用与语义：**

设置或取回发动机的电流输出模式。

**如何使用：** 调用 `setOutputMode(...)` 修改 `outputMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPaused(bool paused)`

**作用与语义：**

暂停空间音频引擎。

**如何使用：** 调用 `setPaused(...)` 修改 `paused`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void distanceScaleChanged()`

**作用与语义：**

定义空间音频引擎所使用的坐标系的比例尺。默认情况下，所有单位均以厘米为单位，与 Qt Quick 3D 默认单位一致。
将距离刻度设置为QAudioEngine：:D istanceScaleMeter，以获得单位单位（米）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `distanceScale` 的变化，不要把它当作普通函数主动调用。

### `void masterVolumeChanged()`

**作用与语义：**

设置或返回用于渲染声场的音量。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `masterVolume` 的变化，不要把它当作普通函数主动调用。

### `void outputDeviceChanged()`

**作用与语义：**

设置或返回用于播放声场的设备。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `outputDevice` 的变化，不要把它当作普通函数主动调用。

### `void outputModeChanged()`

**作用与语义：**

设置或取回发动机的电流输出模式。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `outputMode` 的变化，不要把它当作普通函数主动调用。

### `void pausedChanged()`

**作用与语义：**

暂停空间音频引擎。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `paused` 的变化，不要把它当作普通函数主动调用。

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

`QAudioEngine` 所属机制类型：多媒体设备与会话机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
