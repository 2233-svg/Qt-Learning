# QPlaybackOptions

> Qt 6.11.1 · Qt Multimedia

## 1. 先建立直觉

**一句话定位：** `QPlaybackOptions` 是 Qt Multimedia 的“PlaybackOptions”类型，参与媒体源、设备、格式、播放/采集状态或音视频数据处理。

**模块背景：** Qt Multimedia 提供音频、视频、摄像头、媒体会话和设备访问能力。

### 这是什么

`QPlaybackOptions` 是 多媒体设备与会话机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

**适用场景：** 先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

## 2. 依赖与对象关系

- 头文件：`#include <QPlaybackOptions>`
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

- `(since 6.10) enum class PlaybackIntent { Playback, LowLatencyStreaming }`

### 属性

- `(since 6.10) networkTimeout : std::chrono::milliseconds`
- `(since 6.10) playbackIntent : PlaybackIntent`
- `(since 6.10) probeSize : qsizetype`

### 公有函数

- `std::chrono::milliseconds networkTimeout() const`
- `QPlaybackOptions::PlaybackIntent playbackIntent() const`
- `qsizetype probeSize() const`
- `void resetNetworkTimeout()`
- `void resetPlaybackIntent()`
- `void resetProbeSize()`
- `void setNetworkTimeout(std::chrono::milliseconds timeout)`
- `void setPlaybackIntent(QPlaybackOptions::PlaybackIntent intent)`
- `void setProbeSize(qsizetype probeSizeBytes)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[since 6.10] enum class QPlaybackOptions::PlaybackIntent`

**作用与语义：**

配置媒体播放的意图，使其专注于高质量播放或低延迟媒体流。
- `QPlaybackOptions::PlaybackIntent::Playback`：`0`;其意图是稳健且高质量的媒体播放，允许足够的缓冲以防止播放过程中出现故障。
- `QPlaybackOptions::PlaybackIntent::LowLatencyStreaming`：`1`;缓冲减少以优化低延迟流媒体，但播放过程中更可能出现帧丢失或其他故障。
这个枚举是在Qt 6.10引入的。

### `[since 6.10] networkTimeout : std::chrono::milliseconds`

**作用与语义：**

确定某些网络格式下用于套接字I/O操作的网络超时。
该选项仅支持FFmpeg媒体后端。

**如何使用：** 调用 `networkTimeout()` 读取当前值；它不会修改应用状态。

### `[since 6.10] playbackIntent : PlaybackIntent`

**作用与语义：**

判断`QMediaPlayer`应优化为强健的高质量视频播放（默认）还是低延迟流媒体。
该选项仅支持FFmpeg媒体后端。

**如何使用：** 调用 `playbackIntent()` 读取当前值；它不会修改应用状态。

### `[since 6.10] probeSize : qsizetype`

**作用与语义：**

Probesize 定义了在媒体播放开始前需要分析的数据量（以字节为单位），以便收集流信息。
较大的探针大小可以提供更稳健的播放，但可能会增加延迟。相反，较小的探针大小可以降低延迟，但可能会遗漏一些流的细节。默认探针大小为-1，实际探测大小由媒体后端决定。
该选项仅支持FFmpeg媒体后端。

**如何使用：** 调用 `probeSize()` 读取当前值；它不会修改应用状态。

### `std::chrono::milliseconds networkTimeout() const`

**作用与语义：**

确定某些网络格式下用于套接字I/O操作的网络超时。
该选项仅支持FFmpeg媒体后端。

**如何使用：** 调用 `networkTimeout()` 读取当前值；它不会修改应用状态。

### `QPlaybackOptions::PlaybackIntent playbackIntent() const`

**作用与语义：**

判断`QMediaPlayer`应优化为强健的高质量视频播放（默认）还是低延迟流媒体。
该选项仅支持FFmpeg媒体后端。

**如何使用：** 调用 `playbackIntent()` 读取当前值；它不会修改应用状态。

### `qsizetype probeSize() const`

**作用与语义：**

Probesize 定义了在媒体播放开始前需要分析的数据量（以字节为单位），以便收集流信息。
较大的探针大小可以提供更稳健的播放，但可能会增加延迟。相反，较小的探针大小可以降低延迟，但可能会遗漏一些流的细节。默认探针大小为-1，实际探测大小由媒体后端决定。
该选项仅支持FFmpeg媒体后端。

**如何使用：** 调用 `probeSize()` 读取当前值；它不会修改应用状态。

### `void resetNetworkTimeout()`

**作用与语义：**

确定某些网络格式下用于套接字I/O操作的网络超时。
该选项仅支持FFmpeg媒体后端。

**如何使用：** 调用 `resetNetworkTimeout()` 撤销对 `networkTimeout` 的显式覆盖，让它重新采用继承值或默认值。

### `void resetPlaybackIntent()`

**作用与语义：**

判断`QMediaPlayer`应优化为强健的高质量视频播放（默认）还是低延迟流媒体。
该选项仅支持FFmpeg媒体后端。

**如何使用：** 调用 `resetPlaybackIntent()` 撤销对 `playbackIntent` 的显式覆盖，让它重新采用继承值或默认值。

### `void resetProbeSize()`

**作用与语义：**

Probesize 定义了在媒体播放开始前需要分析的数据量（以字节为单位），以便收集流信息。
较大的探针大小可以提供更稳健的播放，但可能会增加延迟。相反，较小的探针大小可以降低延迟，但可能会遗漏一些流的细节。默认探针大小为-1，实际探测大小由媒体后端决定。
该选项仅支持FFmpeg媒体后端。

**如何使用：** 调用 `resetProbeSize()` 撤销对 `probeSize` 的显式覆盖，让它重新采用继承值或默认值。

### `void setNetworkTimeout(std::chrono::milliseconds timeout)`

**作用与语义：**

确定某些网络格式下用于套接字I/O操作的网络超时。
该选项仅支持FFmpeg媒体后端。

**如何使用：** 调用 `setNetworkTimeout(...)` 修改 `networkTimeout`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPlaybackIntent(QPlaybackOptions::PlaybackIntent intent)`

**作用与语义：**

判断`QMediaPlayer`应优化为强健的高质量视频播放（默认）还是低延迟流媒体。
该选项仅支持FFmpeg媒体后端。

**如何使用：** 调用 `setPlaybackIntent(...)` 修改 `playbackIntent`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setProbeSize(qsizetype probeSizeBytes)`

**作用与语义：**

Probesize 定义了在媒体播放开始前需要分析的数据量（以字节为单位），以便收集流信息。
较大的探针大小可以提供更稳健的播放，但可能会增加延迟。相反，较小的探针大小可以降低延迟，但可能会遗漏一些流的细节。默认探针大小为-1，实际探测大小由媒体后端决定。
该选项仅支持FFmpeg媒体后端。

**如何使用：** 调用 `setProbeSize(...)` 修改 `probeSize`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QPlaybackOptions` 所属机制类型：多媒体设备与会话机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
