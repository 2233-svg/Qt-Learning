# QAudioSink：将原始 PCM 音频送往输出设备

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAudioSink>`  
> 所属模块：`Qt6::Multimedia`  
> 继承：`QObject`  
> 相关类型：`QAudioDevice`、`QAudioFormat`、`QIODevice`、`QtAudio::State`、`QtAudio::Error`

## 1. 它解决什么问题

`QAudioSink` 是 Qt 的原始音频输出接口：应用提供一段符合 `QAudioFormat` 的 PCM 数据，`QAudioSink` 负责把数据送到指定的系统音频输出设备。

它适合以下场景：

- 播放 WAV 头之后的裸 PCM 数据；
- 播放网络解码器、语音引擎或游戏音频混音器产生的实时采样；
- 低延迟播放，需要在音频线程中直接生成正弦波、合成器或提示音；
- 不想依赖 `QMediaPlayer` 的文件/媒体容器流程，而是自行管理采样格式和数据流。

它不负责解析 WAV、MP3 或 AAC，也不负责把任意字节自动转换成目标格式。应用必须确保输入数据的采样率、通道数、样本格式和交错布局与 `format()` 一致。格式不匹配时，听到噪声并不意味着 Qt 做错了，通常是数据解释方式与设备格式不同。

## 2. 两种数据供给方式

`QAudioSink` 有两套互斥的数据接口。

### 2.1 `QIODevice` 接口

把一个已经打开的 `QIODevice` 交给 `start(QIODevice *)`，Qt 从该设备读取数据。这种方式适合文件、环形缓存或已有的流式设备。应用设备接口主要运行在应用线程，Qt 内部使用无锁环形缓冲把数据交给音频线程。

```cpp
QFile source(":/audio/voice.raw");
source.open(QIODevice::ReadOnly);

QAudioFormat format;
format.setSampleRate(44100);
format.setChannelCount(2);
format.setSampleFormat(QAudioFormat::Int16);

QAudioSink sink(format);
sink.start(&source);
```

`source` 必须以 `QIODevice::ReadOnly` 或 `QIODevice::ReadWrite` 打开。文件结束或应用供数不及时，输出会进入 `IdleState`，后端可能输出静音；有新数据可读后可以回到 `ActiveState`。

也可以调用无参数 `start()`，让 Qt 返回一个已经打开的内部 `QIODevice`，应用向它 `write()`：

```cpp
QAudioSink sink(format);
QIODevice *device = sink.start();
device->write(pcmBytes);
```

这个内部指针只在当前流有效。调用 `stop()` 或再次 `start()` 后，指针失效，不能缓存后继续写。

### 2.2 6.11 的回调接口

调用 `start(callback)` 时，Qt 在软实时音频线程中向回调提供一个 `QSpan<SampleType>`。应用必须把交错 PCM 样本填满这个 span。

```cpp
QAudioSink sink(format);
float phase = 0.0f;
const float step = 2.0f * float(M_PI) * 440.0f / format.sampleRate();

sink.start([&phase, step](QSpan<float> samples) {
    for (qsizetype i = 0; i < samples.size(); ++i) {
        samples[i] = std::sin(phase);
        phase += step;
        if (phase >= 2.0f * float(M_PI))
            phase -= 2.0f * float(M_PI);
    }
});
```

回调参数的样本类型必须与 `QAudioFormat::sampleFormat()` 匹配，例如 `Int16` 对应 `qint16`，`Int32` 对应 `qint32`，`Float` 对应 `float`。span 中是交错样本，不是按通道拆开的平面数组；立体声数据通常按 `L, R, L, R` 排列。

回调运行在软实时线程中。不要在回调里做文件/网络 I/O、等待条件变量、锁互斥量、分配动态内存、调用可能阻塞的日志或复杂 UI 操作。需要和应用线程交换信息时，使用预分配的无锁结构、原子变量或专门的实时安全通信机制。

回调模式下，缓冲区大小由音频后端决定，`setBufferSize()` 和 `setBufferFrameCount()` 不用于控制回调参数大小。回调 API 目前只在支持它的后端上可用，包括 Apple CoreAudio、Windows、使用 PulseAudio/PipeWire 的 Linux 以及 Android。

## 3. 格式、设备和生命周期

### 3.1 构造时确定设备和格式

默认构造函数使用系统默认输出设备。也可以传入具体的 `QAudioDevice`。如果传入的 `QAudioFormat` 是默认构造值，Qt 使用目标设备的首选格式。

如果指定格式，启动前应使用 `QAudioDevice::isFormatSupported()` 检查。`QAudioSink` 不会把任意不支持的 PCM 自动重采样或重排为设备格式。

### 3.2 QObject 所有权和不可复制

`QAudioSink` 是 `QObject`，不可复制。给它设置 parent 后，父对象析构会销毁 sink，并释放系统音频资源和内部缓冲。销毁前不需要手动释放 `start()` 返回的内部 `QIODevice`。

`start(QIODevice *)` 使用的是调用方提供的设备指针。sink 不接管这个设备的所有权；文件或自定义设备必须活得至少和音频传输过程一样久，并在 `stop()` 后由应用自行关闭或销毁。

### 3.3 线程归属

普通 `QIODevice` 方式面向应用线程。不要一边在一个线程销毁/移动设备，一边让 sink 在另一个线程读取它。回调方式则明确在音频线程执行，回调捕获的对象必须在整个音频流期间保持有效，并且要满足实时访问约束。

## 4. 状态、错误和缓冲

### 4.1 状态

`QtAudio::State` 常见状态如下：

- `ActiveState`：正在处理并输出音频；
- `SuspendedState`：处理暂停，但缓冲数据保留；
- `StoppedState`：已停止或发生错误；
- `IdleState`：当前没有可立即输出的数据，或输出设备处于空闲等待状态。

状态通过 `stateChanged(QtAudio::State)` 异步通知。启动失败时通常是 `OpenError` 加 `StoppedState`，应同时读取 `error()`，不要只看状态。

### 4.2 错误恢复

发生错误后，sink 会进入 `StoppedState`。`error()` 返回 `QtAudio::Error`，例如 `NoError`、`OpenError`、`IOError`、`UnderrunError` 或 `FatalError`，具体取值定义在 `QtAudio` 中。

调用 `stop()` 或 `reset()` 会把错误状态恢复为 `NoError`。若设备被占用、格式不支持或权限失败，清除错误并不等于问题已经解决，通常还要重新选择设备或修正格式后再次启动。

### 4.3 缓冲大小

`QIODevice` 模式默认使用约 250 ms 的内部环形缓冲。启动前可按字节或帧设置缓冲大小：

- `setBufferSize(bytes)` 以字节为单位；
- Qt 6.10 起可用 `setBufferFrameCount(framesCount)` 以音频帧为单位。

二者都只能在第一次 `start()` 前设置；启动后调用会被忽略。后端可能把请求值调整为实际可用的大小，因此启动后应调用 `bufferSize()` 或 `bufferFrameCount()` 获取实际值。

一个音频帧包含所有通道各一个样本。对于双声道 16 位音频，一帧是 4 字节，所以 `framesFree()` 比手工用字节数换算更不容易出错。

`bytesFree()` 和 Qt 6.10 起的 `framesFree()` 只在 `ActiveState` 或 `IdleState` 有效，其他状态返回 0。它们描述的是内部缓冲还能容纳多少数据，不是声卡硬件缓冲的完整实时容量。

## 5. 停止、暂停和时间统计

### 5.1 `stop()` 与 `reset()`

`stop()` 停止输出并解除系统资源连接，将状态设为 `StoppedState`，同时清除错误。在 Linux 和 Darwin 上，停止操作可能同步排空底层音频缓冲，因此缓冲中数据较多时可能等待一段时间。

`reset()` 立即停止输出并丢弃当前缓冲中的音频数据。已经写入 `QIODevice`、但尚未播放的内容也会被忽略。需要“立刻切歌”或“立即静音并清空延迟”时应使用 `reset()`。

### 5.2 `suspend()` 与 `resume()`

`suspend()` 暂停处理，但保留已经缓冲的数据，状态变为 `SuspendedState`。`resume()` 只对 `SuspendedState` 有效，并恢复到暂停前的工作状态；在其他状态调用时不做有意义的恢复。

### 5.3 两种时间

- `processedUSecs()`：从 `start()` 起已经实际处理的音频时长；
- `elapsedUSecs()`：从 `start()` 起经过的墙上时间，包括 `IdleState` 和 `SuspendedState`。

当供数中断或暂停时，二者会产生差异。计算“已经播放了多少音频”应使用 `processedUSecs()`，计算“这次播放会话持续了多久”才使用 `elapsedUSecs()`。

## 6. API 逐项说明

### 构造、析构和查询

#### `QAudioSink(const QAudioFormat &format = QAudioFormat(), QObject *parent = nullptr)`

使用系统默认输出设备创建设备输出。默认格式表示使用该设备的首选格式；指定格式时，启动前应检查设备是否支持。

#### `QAudioSink(const QAudioDevice &audioDevice, const QAudioFormat &format = QAudioFormat(), QObject *parent = nullptr)`

使用 `audioDevice` 指定的输出设备创建 sink。默认格式表示使用该设备的首选格式。

#### `~QAudioSink()`

销毁 sink，释放系统资源和内部缓冲。不会接管或销毁应用传入的 `QIODevice`。

#### `bool isNull() const`

返回 sink 是否没有有效的平台音频实现。通常用于构造或平台初始化失败后的防御性检查；即使不为 null，格式、权限和设备打开仍可能在 `start()` 时失败。

#### `QAudioFormat format() const`

返回 sink 正在使用的音频格式，包括采样率、通道数和样本格式。应用向 `QIODevice` 写入或在回调中填充的数据必须按此格式解释。

### 缓冲查询和设置

#### `void setBufferSize(qsizetype bytes)`

在启动前请求内部缓冲区大小，单位为字节。启动后调用被忽略；后端可能调整请求值。

#### `qsizetype bufferSize() const`

返回缓冲区大小，单位为字节。启动前返回平台默认值或预设值，启动后返回实际使用值。

#### `void setBufferFrameCount(qsizetype framesCount)`（Qt 6.10）

在启动前按音频帧数请求缓冲大小。启动后调用被忽略，实际值应通过 `bufferFrameCount()` 查询。

#### `qsizetype bufferFrameCount() const`（Qt 6.10）

返回缓冲区大小，单位为音频帧。启动前可能是默认/预设值，启动后是后端实际值。

#### `qsizetype bytesFree() const`

返回内部缓冲可容纳的空闲字节数。只在 `ActiveState` 或 `IdleState` 有效，否则返回 0。

#### `qsizetype framesFree() const`（Qt 6.10）

返回内部缓冲可容纳的空闲帧数。只在 `ActiveState` 或 `IdleState` 有效，否则返回 0。

### 音量

#### `void setVolume(qreal volume)`

设置当前音频流音量。值按线性范围 `0.0` 到 `1.0` 解释，越界会钳制；默认是 `1.0`。它只影响该 sink 的流，不修改系统全局音量。

#### `qreal volume() const`

返回当前线性音量，正常范围为 `[0.0, 1.0]`。

### 启动和数据接口

#### `void start(QIODevice *device)`

从 `device` 读取 PCM 数据并输出。设备必须已经以 `ReadOnly` 或 `ReadWrite` 打开。sink 不拥有该指针，调用方必须保证其生命周期。

成功时通常进入 `ActiveState`；供数暂时不足时可能进入 `IdleState`。失败时通常是 `OpenError` 加 `StoppedState`。

#### `QIODevice *start()`

启动并返回 Qt 内部的可写 `QIODevice`。应用应向返回对象调用 `write()` 提供 PCM 数据。

返回指针在 `stop()` 或再次 `start()` 后失效；不要在异步回调中继续使用旧指针。启动失败时仍应检查 `state()` 和 `error()`。

#### `template <typename Callback> void start(Callback &&cb)`（Qt 6.11）

以软实时音频回调方式启动。回调接收 `QSpan<SampleType>`，其中 `SampleType` 必须匹配 `format().sampleFormat()`，并填充交错音频数据。

该模式不能依赖 `QIODevice`，回调线程中禁止阻塞操作。回调签名不匹配、后端不支持回调或设备无法打开时，启动失败并进入错误状态。

### 状态控制和计时

#### `void stop()`

停止输出、解除系统资源连接、清空错误并进入 `StoppedState`。Linux/Darwin 可能同步排空底层缓冲，立即丢弃数据应改用 `reset()`。

#### `void reset()`

立即停止并丢弃所有缓冲音频，包括已推送到内部 `QIODevice` 但尚未播放的内容。

#### `void suspend()`

暂停音频处理并保留缓冲数据，进入 `SuspendedState`。

#### `void resume()`

从 `SuspendedState` 恢复到暂停前状态；如果当前不是暂停状态，则不执行恢复。

#### `qint64 processedUSecs() const`

返回从 `start()` 起已处理音频的时长，单位为微秒，不把暂停或供数空闲时间当作已播放音频。

#### `qint64 elapsedUSecs() const`

返回从 `start()` 起经过的时间，单位为微秒，包括 idle 和 suspend 时段。

#### `QtAudio::Error error() const`

返回当前错误状态。启动、设备访问或 I/O 出错时读取它；`stop()` 或 `reset()` 会清除错误。

#### `QtAudio::State state() const`

返回当前音频处理状态。它反映的是状态机，不等价于“缓冲中一定有数据”。

### 信号

#### `void stateChanged(QtAudio::State state)`

音频状态改变时发出。可用来更新播放/暂停按钮、处理 underrun 或发现启动失败。

Qt 6.6 及以前命名空间名为 `QAudio`。使用旧式字符串连接时，参数类型仍应写作 `QAudio::State`；新式函数指针连接使用当前的 `QtAudio::State` 声明即可。

## 7. 常见误区与排查顺序

1. 先确认 `QAudioFormat` 与裸 PCM 数据一致，再检查 `QAudioDevice::isFormatSupported()`。
2. 启动后立即读取 `error()` 和 `state()`，不要只看 `start()` 是否返回。
3. `IdleState` 不一定是致命错误，`QIODevice` 模式下它可能只是暂时没有数据；但持续 idle 表示供数不足。
4. 需要低延迟时用回调，但不要把普通文件读取搬进回调。
5. 需要立即清空延迟时用 `reset()`，不要误用可能排空底层缓冲的 `stop()`。
6. 不要保存 `start()` 返回的内部 `QIODevice *` 跨越 stop 或下一次 start。

## API 速查表

| 类别 | API | 语义 | 边界与注意 |
| --- | --- | --- | --- |
| 构造 | `QAudioSink(const QAudioFormat &format = QAudioFormat(), QObject *parent = nullptr)` | 用默认输出设备和指定/首选格式创建 sink。 | 需要 parent 生命周期管理；格式不自动转换。 |
| 构造 | `QAudioSink(const QAudioDevice &audioDevice, const QAudioFormat &format = QAudioFormat(), QObject *parent = nullptr)` | 用指定输出设备创建 sink。 | 默认格式使用该设备首选格式。 |
| 析构 | `~QAudioSink()` | 释放音频资源和内部缓冲。 | 不销毁应用传入的 `QIODevice`。 |
| 查询 | `bool isNull() const` | 查询平台实现是否为空。 | 不代表后续 `start()` 一定成功。 |
| 查询 | `QAudioFormat format() const` | 返回实际使用的 PCM 格式。 | 写入数据必须匹配采样率、通道和样本类型。 |
| 缓冲 | `void setBufferSize(qsizetype bytes)` | 启动前按字节请求缓冲大小。 | 启动后忽略；实际值可能不同。 |
| 缓冲 | `qsizetype bufferSize() const` | 返回缓冲字节数。 | 启动后才是后端实际使用值。 |
| 缓冲 | `void setBufferFrameCount(qsizetype framesCount)` | 启动前按帧请求缓冲大小。 | Qt 6.10；启动后忽略。 |
| 缓冲 | `qsizetype bufferFrameCount() const` | 返回缓冲帧数。 | Qt 6.10；启动后查询实际值。 |
| 缓冲 | `qsizetype bytesFree() const` | 查询可写入的空闲字节数。 | 仅 Active/Idle 有效，否则为 0。 |
| 缓冲 | `qsizetype framesFree() const` | 查询可写入的空闲帧数。 | Qt 6.10；仅 Active/Idle 有效。 |
| 音量 | `void setVolume(qreal volume)` | 设置当前流线性音量。 | `[0, 1]`，越界钳制；不改全局音量。 |
| 音量 | `qreal volume() const` | 返回当前流音量。 | 线性值，正常范围 `[0, 1]`。 |
| 启动 | `void start(QIODevice *device)` | 从已打开设备读取 PCM 并输出。 | 设备需 ReadOnly/ReadWrite；sink 不接管所有权。 |
| 启动 | `QIODevice *start()` | 返回 Qt 内部可写设备供应用 `write()`。 | stop 或再次 start 后指针失效。 |
| 启动 | `void start(Callback &&cb)`（Qt 6.11） | 在音频线程回调中填充交错 PCM。 | 类型须匹配 sampleFormat；禁止阻塞和分配。 |
| 控制 | `void stop()` | 停止并解除系统输出。 | Linux/Darwin 可能同步排空；清除错误。 |
| 控制 | `void reset()` | 立即停止并丢弃所有缓冲数据。 | 适合立即切换或清空延迟。 |
| 控制 | `void suspend()` | 暂停处理并保留缓冲。 | 进入 SuspendedState。 |
| 控制 | `void resume()` | 从暂停恢复。 | 非 SuspendedState 调用无效。 |
| 计时 | `qint64 processedUSecs() const` | 返回已处理音频时长。 | 不包含 idle/suspend 时段。 |
| 计时 | `qint64 elapsedUSecs() const` | 返回 start 后经过的时间。 | 包含 idle/suspend 时段。 |
| 状态 | `QtAudio::Error error() const` | 查询错误状态。 | 启动失败时与 state 一起检查。 |
| 状态 | `QtAudio::State state() const` | 查询音频状态机状态。 | 不等价于缓冲一定非空。 |
| 信号 | `void stateChanged(QtAudio::State state)` | 通知状态变化。 | 用于 UI 和错误/underrun 响应。 |
