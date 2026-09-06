# QMediaDevices

> Qt 6.11.1 · Qt Multimedia

## 1. 先建立直觉

**一句话定位：** `QMediaDevices` 是 Qt Multimedia 的“媒体Devices”类型，参与媒体源、设备、格式、播放/采集状态或音视频数据处理。

**模块背景：** Qt Multimedia 提供音频、视频、摄像头、媒体会话和设备访问能力。

### 这是什么

`QMediaDevices` 是 多媒体设备与会话机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

**适用场景：** 先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

## 2. 依赖与对象关系

- 头文件：`#include <QMediaDevices>`
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

### 属性

- `audioInputs : QList<QAudioDevice>`
- `audioOutputs : QList<QAudioDevice>`
- `defaultAudioInput : QAudioDevice`
- `defaultAudioOutput : QAudioDevice`
- `defaultVideoInput : QCameraDevice`
- `videoInputs : QList<QCameraDevice>`

### 信号

- `void audioInputsChanged()`
- `void audioOutputsChanged()`
- `void videoInputsChanged()`

### 静态公有成员

- `QList<QAudioDevice> audioInputs()`
- `QList<QAudioDevice> audioOutputs()`
- `QAudioDevice defaultAudioInput()`
- `QAudioDevice defaultAudioOutput()`
- `QCameraDevice defaultVideoInput()`
- `QList<QCameraDevice> videoInputs()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[read-only] audioInputs : QList<QAudioDevice>`

**作用与语义：**

返回系统中可用的音频输入设备列表。
这些设备通常是麦克风。设备可以是内置的，或者通过USB或蓝牙连接。

**如何使用：** 调用 `audioInputs()` 读取当前值；它不会修改应用状态。

### `[read-only] audioOutputs : QList<QAudioDevice>`

**作用与语义：**

返回系统中可用的音频输出设备列表。
这些设备通常是扬声器或耳机。设备可以是内置的，也可以通过USB或蓝牙连接。

**如何使用：** 调用 `audioOutputs()` 读取当前值；它不会修改应用状态。

### `[read-only] defaultAudioInput : QAudioDevice`

**作用与语义：**

返回默认音频输入设备。
默认设备可以在应用运行期间更换。此时会发出`audioInputsChanged()`信号。

**如何使用：** 调用 `defaultAudioInput()` 读取当前值；它不会修改应用状态。

### `[read-only] defaultAudioOutput : QAudioDevice`

**作用与语义：**

返回默认音频输出设备。
默认设备在应用运行期间可以更换。此时发出`audioOutputsChanged()`信号。

**如何使用：** 调用 `defaultAudioOutput()` 读取当前值；它不会修改应用状态。

### `[read-only] defaultVideoInput : QCameraDevice`

**作用与语义：**

系统会返回默认摄像头。
注意：返回对象在使用前应使用isNull()检查，以防没有默认相机或根本没有相机。
默认设备可以在应用运行时更换。在这种情况下，`videoInputsChanged()`信号会被发射。

**如何使用：** 调用 `defaultVideoInput()` 读取当前值；它不会修改应用状态。

### `[read-only] videoInputs : QList<QCameraDevice>`

**作用与语义：**

返回系统中可用摄像头列表。

**如何使用：** 调用 `videoInputs()` 读取当前值；它不会修改应用状态。

### `void audioInputsChanged()`

**作用与语义：**

返回系统中可用的音频输入设备列表。
这些设备通常是麦克风。设备可以是内置的，或者通过USB或蓝牙连接。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `audioInputs` 的变化，不要把它当作普通函数主动调用。

### `void audioOutputsChanged()`

**作用与语义：**

返回系统中可用的音频输出设备列表。
这些设备通常是扬声器或耳机。设备可以是内置的，也可以通过USB或蓝牙连接。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `audioOutputs` 的变化，不要把它当作普通函数主动调用。

### `void videoInputsChanged()`

**作用与语义：**

系统会返回默认摄像头。
注意：返回对象在使用前应使用isNull()检查，以防没有默认相机或根本没有相机。
默认设备可以在应用运行时更换。在这种情况下，`videoInputsChanged()`信号会被发射。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `defaultVideoInput` 的变化，不要把它当作普通函数主动调用。

### `QList<QAudioDevice> audioInputs()`

**作用与语义：**

返回系统中可用的音频输入设备列表。
这些设备通常是麦克风。设备可以是内置的，或者通过USB或蓝牙连接。

**如何使用：** 调用 `audioInputs()` 读取当前值；它不会修改应用状态。

### `QList<QAudioDevice> audioOutputs()`

**作用与语义：**

返回系统中可用的音频输出设备列表。
这些设备通常是扬声器或耳机。设备可以是内置的，也可以通过USB或蓝牙连接。

**如何使用：** 调用 `audioOutputs()` 读取当前值；它不会修改应用状态。

### `QAudioDevice defaultAudioInput()`

**作用与语义：**

返回默认音频输入设备。
默认设备可以在应用运行期间更换。此时会发出`audioInputsChanged()`信号。

**如何使用：** 调用 `defaultAudioInput()` 读取当前值；它不会修改应用状态。

### `QAudioDevice defaultAudioOutput()`

**作用与语义：**

返回默认音频输出设备。
默认设备在应用运行期间可以更换。此时发出`audioOutputsChanged()`信号。

**如何使用：** 调用 `defaultAudioOutput()` 读取当前值；它不会修改应用状态。

### `QCameraDevice defaultVideoInput()`

**作用与语义：**

系统会返回默认摄像头。
注意：返回对象在使用前应使用isNull()检查，以防没有默认相机或根本没有相机。
默认设备可以在应用运行时更换。在这种情况下，`videoInputsChanged()`信号会被发射。

**如何使用：** 调用 `defaultVideoInput()` 读取当前值；它不会修改应用状态。

### `QList<QCameraDevice> videoInputs()`

**作用与语义：**

返回系统中可用摄像头列表。

**如何使用：** 调用 `videoInputs()` 读取当前值；它不会修改应用状态。

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

`QMediaDevices` 所属机制类型：多媒体设备与会话机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
