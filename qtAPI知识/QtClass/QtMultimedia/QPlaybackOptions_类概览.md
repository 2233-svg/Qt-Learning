# QPlaybackOptions：向媒体后端提供播放策略提示

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPlaybackOptions>`  
> 所属模块：`Qt6::Multimedia`  
> 继承：无  
> 类型性质：`Q_GADGET` 值类型  
> 引入版本：Qt 6.10

## 它解决什么问题

`QPlaybackOptions` 为 `QMediaPlayer` 提供低层播放参数，让应用能够针对特殊媒体或特殊网络环境调整后端行为。它描述的是播放意图和探测策略，不是一个独立的播放器。

它目前包含三类选项：

- 网络 socket I/O 的超时时间；
- 偏向稳定高质量播放，还是偏向低延迟流式播放；
- 播放开始前用于探测媒体流信息的数据量。

这些设置都是后端提示。后端可能因为媒体格式、编码器、平台实现或自身限制而忽略它们。不能把设置成功理解为播放器一定按该策略运行。

## 实际使用场景

- 播放局域网摄像头或实时流时降低首帧和缓冲延迟；
- 播放网络不稳定的长视频时增加探测或缓冲倾向；
- 对连接超时有明确业务要求的网络播放器；
- 为不同播放模式保存一组可复制的策略配置；
- 在 `QMediaPlayer::setPlaybackOptions()` 前构造并验证配置。

## 与 QMediaPlayer 的关系

```cpp
QPlaybackOptions options;
options.setPlaybackIntent(
    QPlaybackOptions::PlaybackIntent::LowLatencyStreaming);
options.setNetworkTimeout(std::chrono::seconds(5));
options.setProbeSize(256 * 1024);

player->setPlaybackOptions(options);
player->setSource(url);
```

播放选项应在设置媒体源前配置。`QMediaPlayer` 文档将它定位为低层播放控制，实际生效时机和支持程度由后端决定；工程上不要假设修改后会立即重建当前媒体的网络连接或解码器。

当前 Qt 6.11.1 文档明确说明，这些选项只有 FFmpeg 媒体后端支持。使用其它后端时，getter 仍然可以读写值对象，但播放器可能完全不采用这些值。

## PlaybackIntent：稳定播放与低延迟的取舍

### `Playback`

默认意图，偏向稳定、高质量播放。后端可以使用更充分的缓冲来降低卡顿和丢帧概率，适合点播文件、长视频和对连续性要求高的场景。

### `LowLatencyStreaming`

偏向低延迟流式播放。后端会减少缓冲倾向，但更容易出现丢帧、短暂卡顿或其它播放瑕疵。它适合实时监控、交互式视频和延迟比完整性更重要的场景。

它不是“保证实时”的开关。网络链路、编码端、解码端、音视频时钟和输出设备仍然会决定最终延迟。

## networkTimeout：网络 I/O 超时

`networkTimeout` 的类型是 `std::chrono::milliseconds`，表示某些网络格式进行 socket I/O 时使用的超时时间。

```cpp
options.setNetworkTimeout(std::chrono::milliseconds(3000));
```

边界要点：

- 该选项只有 FFmpeg 后端支持；
- 它作用于后端网络 I/O，不等于整个 `QMediaPlayer` 的总播放超时；
- 超时发生后，具体错误类型和恢复行为由后端决定；
- Qt API 没有为负数定义可移植的业务语义，应用应使用非负时长；
- `resetNetworkTimeout()` 恢复默认配置，而不是保证使用某个固定毫秒值。

## probeSize：启动前探测字节数

`probeSize` 表示播放开始前，后端用于分析媒体流信息的数据量，单位是字节。

- 默认值是 `-1`，表示由媒体后端决定实际探测大小；
- 设置得太小，可能无法识别完整的流信息，甚至导致媒体无法播放；
- 设置得太大，可能增加启动延迟；
- 它是探测阶段的输入量，不是下载缓存大小，也不是解码缓冲大小；
- 只有 FFmpeg 后端支持。

```cpp
options.setProbeSize(512 * 1024);
```

对于格式固定、流信息靠近文件开头的媒体，较小值可能足够；对于封装复杂或元数据较晚出现的媒体，过小值会增加失败风险。跨平台程序应把它作为可调策略，而不是写死成所有媒体都适用的常量。

## 值语义、比较和 Q_GADGET

`QPlaybackOptions` 使用 `Q_GADGET`，不是 `QObject`：

- 没有父对象；
- 没有信号和槽；
- 可以复制、移动和放入 Qt 容器；
- 不需要事件循环；
- 不拥有播放器、网络连接或解码器。

它使用显式共享数据，复制配置通常很轻量。多个线程持有各自的副本可以安全地传递；如果多个线程同时修改同一个逻辑对象，仍需要同步。

头文件中的 `Q_DECLARE_STRONGLY_ORDERED(QPlaybackOptions)` 提供强排序相关的比较语义。比较的是配置值本身，不是“哪个播放效果更好”，也不表示当前后端对某个配置的支持程度。

## reset 的意义

三个 `reset...()` 函数将属性恢复为 Qt/后端的默认状态：

```cpp
options.setProbeSize(128 * 1024);
options.resetProbeSize();
```

恢复后的 `probeSize()` 会回到 `-1`。对于其它属性，应把 reset 理解为“取消应用层覆盖”，而不是把它解释成某个跨平台固定值。

## 生命周期和线程

这是一个纯配置值，不参与异步操作。可以在任意线程构造和修改自己的实例。

真正把它交给 `QMediaPlayer` 后，播放器及其后端仍应在播放器所属线程使用。配置对象的线程安全不能扩大播放器、网络设备或解码器的线程边界。

## 常见误区

- 认为所有媒体后端都支持这些选项；
- 把低延迟意图理解为“不会卡顿且一定实时”；
- 把 `networkTimeout` 当成整个播放流程的总超时；
- 把 `probeSize` 当成下载缓存或预读缓存大小；
- 把默认 `-1` 当成负数错误；
- 修改选项后期待当前已加载媒体立即重建；
- 通过比较两个选项对象来判断哪个播放质量更高；
- 把 `Q_GADGET` 值类型当成带信号的 `QObject`。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `enum class PlaybackIntent` | 描述播放策略意图。 | Qt 6.10 引入；实际效果依赖后端。 |
| 枚举值 | `PlaybackIntent::Playback` | 偏向稳定、高质量播放。 | 允许后端使用更多缓冲。 |
| 枚举值 | `PlaybackIntent::LowLatencyStreaming` | 偏向低延迟流式播放。 | 丢帧和卡顿概率可能提高。 |
| 构造 | `QPlaybackOptions()` | 创建默认播放选项。 | 默认探测大小为 `-1`；其它值为默认策略。 |
| 构造 | `QPlaybackOptions(const QPlaybackOptions &other)` | 复制选项对象。 | 值语义；不复制播放器资源。 |
| 构造 | `QPlaybackOptions(QPlaybackOptions &&other)` | 移动选项对象。 | 适合返回临时配置。 |
| 析构 | `~QPlaybackOptions()` | 销毁配置对象。 | 不影响任何播放器。 |
| 赋值 | `operator=(const QPlaybackOptions &other)` | 复制选项。 | 会替换当前配置。 |
| 赋值 | `operator=(QPlaybackOptions &&other)` | 移动选项。 | 适合容器和临时值。 |
| 交换 | `void swap(QPlaybackOptions &other)` | 交换两个配置对象。 | `noexcept`；只交换配置数据。 |
| 网络 | `std::chrono::milliseconds networkTimeout() const` | 读取网络 I/O 超时时间。 | 只有 FFmpeg 后端支持。 |
| 网络 | `void setNetworkTimeout(std::chrono::milliseconds timeout)` | 设置网络 I/O 超时时间。 | 使用非负时长；不等于总播放超时。 |
| 网络 | `void resetNetworkTimeout()` | 恢复网络超时默认配置。 | 不保证恢复到固定的跨平台数值。 |
| 策略 | `PlaybackIntent playbackIntent() const` | 读取播放意图。 | 只反映配置值，不反映后端是否采纳。 |
| 策略 | `void setPlaybackIntent(PlaybackIntent intent)` | 设置稳定播放或低延迟意图。 | 只有 FFmpeg 后端支持。 |
| 策略 | `void resetPlaybackIntent()` | 恢复默认播放意图。 | 默认是 `Playback`。 |
| 探测 | `qsizetype probeSize() const` | 读取探测字节数。 | `-1` 表示由后端决定。 |
| 探测 | `void setProbeSize(qsizetype probeSizeBytes)` | 设置启动前探测字节数。 | 太小可能播放失败，太大可能增加延迟。 |
| 探测 | `void resetProbeSize()` | 恢复默认探测策略。 | 恢复为 `-1`。 |
| 比较 | `comparesEqual(lhs, rhs)` / 强排序运算 | 比较两个配置对象。 | 比较配置值，不比较播放效果或后端能力。 |

## 一句话总结

`QPlaybackOptions` 是给 `QMediaPlayer` 的后端策略提示值：它能表达网络超时、播放意图和探测大小，但所有选项都受 FFmpeg 后端和媒体格式支持情况限制，不能当作强制行为开关。
