# QAudioSource：从输入设备读取原始 PCM 音频

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAudioSource>`  
> 所属模块：`Qt6::Multimedia`  
> 继承：`QObject`  
> 相关类型：`QAudioDevice`、`QAudioFormat`、`QIODevice`、`QtAudio::State`、`QtAudio::Error`

## 1. 它解决什么问题

`QAudioSource` 是 Qt 的原始音频输入接口：应用从系统麦克风取得符合 `QAudioFormat` 的 PCM 数据，然后把数据写入文件、编码器、网络发送器或实时分析器。

它适合：

- 录制裸 PCM 文件或交给自己的 WAV/FLAC/Opus 编码器；
- 实时计算音量、峰值、频谱、语音活动；
- 把麦克风数据送入网络通话或自定义 DSP 管线；
- 使用低延迟回调直接处理音频线程中的采样。

它不负责生成 WAV 头、不负责压缩编码，也不会替应用自动把任意格式转换成目标格式。构造时指定的 `QAudioFormat` 决定了读取数据的采样率、通道数和样本类型。

`QAudioSource` 与 `QAudioInput` 的职责不同：`QAudioSource` 读取原始 PCM，`QAudioInput` 只是媒体采集会话中的麦克风选择和音量/静音配置。

## 2. 实际使用场景与两种数据接收方式

### 2.1 `QIODevice` 接口

将一个已经打开、可写的 `QIODevice` 传给 `start(QIODevice *)`，Qt 把采集到的 PCM 写入它。

```cpp
QFile destination("recording.raw");
destination.open(QIODevice::WriteOnly | QIODevice::Truncate);

QAudioFormat format;
format.setSampleRate(44100);
format.setChannelCount(1);
format.setSampleFormat(QAudioFormat::Int16);

QAudioSource source(format);
source.start(&destination);
```

目标设备必须以 `WriteOnly`、`Append` 或 `ReadWrite` 打开。`QAudioSource` 不接管目标设备的所有权；停止录音后由应用自行关闭文件或销毁自定义设备。

另一种方式是调用无参数 `start()`，让 Qt 返回一个已经打开的内部 `QIODevice`，应用从它 `read()`：

```cpp
QAudioSource source(format);
QIODevice *device = source.start();

const QByteArray pcm = device->readAll();
```

实际应用通常在该设备的 `readyRead` 信号中读取，或在应用事件循环中持续读取。返回指针只在当前流有效；调用 `stop()` 或再次 `start()` 后，旧指针失效。

### 2.2 6.11 的回调接口

调用 `start(callback)` 时，Qt 在软实时音频线程把一段只读的 `QSpan<const SampleType>` 交给回调。span 中包含交错的输入样本，应用可以直接计算峰值、复制到预先分配的环形缓存，或更新原子统计值。

```cpp
std::atomic<float> peakLevel = 0.0f;

QAudioSource source(format);
source.start([&peakLevel](QSpan<const qint16> samples) {
    qint16 peak = 0;
    for (qint16 sample : samples)
        peak = std::max(peak, qAbs(sample));

    peakLevel.store(float(peak) / 32768.0f, std::memory_order_relaxed);
});
```

回调的样本类型必须与 `format().sampleFormat()` 匹配，例如 `UInt8` 使用 `quint8`，`Int16` 使用 `qint16`，`Int32` 使用 `qint32`，`Float` 使用 `float`。多通道数据按交错方式排列，例如双声道为 `L, R, L, R`；span 长度是样本数，不是帧数。

回调运行在软实时音频线程。不要在其中做文件/网络 I/O、等待、互斥锁、动态内存分配、可能阻塞的系统调用或 UI 操作。若应用线程需要拿到数据，应使用预分配的无锁环形缓冲、原子变量或平台提供的实时安全通知机制。

回调模式下，回调参数大小由音频后端决定，不能用 `setBufferSize()` 预先规定每次回调的样本数。该 API 只在支持回调的后端可用，启动失败时检查 `error()` 和 `state()`。

## 3. 格式、设备和生命周期

### 3.1 默认设备和指定设备

默认构造使用系统默认音频输入设备。也可以传入具体的 `QAudioDevice`，例如从 `QMediaDevices::audioInputs()` 选择 USB 麦克风。

如果 `QAudioFormat` 是默认构造值，Qt 使用设备的首选格式。指定格式时，启动前应调用 `QAudioDevice::isFormatSupported()` 检查。对于录音应用，格式不支持时应选择设备支持的格式或使用自己的重采样器，而不是直接假定后端会转换。

### 3.2 QObject 所有权

`QAudioSource` 是 `QObject`，不可复制。给它设置 parent 后，父对象负责销毁它，析构会释放平台音频输入资源和内部缓冲。

传给 `start(QIODevice *)` 的设备由调用方拥有。它必须在录音期间保持有效，并且不能在其他线程中未经同步地关闭、移动或销毁。

### 3.3 采集权限和线程

访问麦克风可能需要操作系统权限。创建 `QAudioSource` 成功不代表设备已获准打开；真正打开通常发生在 `start()`，因此应在启动后检查状态和错误。

普通 `QIODevice` 模式面向应用线程，Qt 通过内部环形缓冲与音频线程通信。回调模式直接运行在音频线程，捕获的引用必须保证在停止回调前一直有效。

## 4. 状态、缓冲和丢帧

### 4.1 状态

`QtAudio::State` 常见状态如下：

- `ActiveState`：正在采集并向目标设备提供数据；
- `SuspendedState`：暂停采集处理，但保留已缓冲数据；
- `StoppedState`：停止或发生错误；
- `IdleState`：应用没有及时从内部 `QIODevice` 读取，输入环形缓冲已经满，或当前没有可继续交付的数据。

对于 `QIODevice` 模式，输入缓冲被读空和被写满都可能导致状态变化，具体表现依后端而定。最重要的边界是：如果应用读取不及时，缓冲会满，音频数据会被丢弃；回到 `ActiveState` 后丢失的数据也不会补回来。

回调模式没有 `IdleState`，音频后端按回调节奏直接交付数据。

### 4.2 错误处理

启动成功时通常是 `ActiveState` 或 `IdleState` 且 `error()` 为 `NoError`。启动失败时通常是 `OpenError` 加 `StoppedState`。

错误类型属于 `QtAudio::Error`，常见值包括 `NoError`、`OpenError`、`IOError`、`UnderrunError` 和 `FatalError`。调用 `stop()` 或 `reset()` 会清除错误状态，但如果设备、权限或格式问题未解决，重新启动仍会失败。

### 4.3 输入缓冲

普通 `QIODevice` 模式默认使用约 250 ms 的内部环形缓冲。启动前可以设置：

- `setBufferSize(bytes)`：按字节设置；
- `setBufferFrameCount(frames)`：按音频帧设置。

这些设置必须在 `start()` 前完成，启动后调用会被忽略。后端可能将请求值调整为实际值，因此启动后用 `bufferSize()` 和 `bufferFrameCount()` 读取实际缓冲大小。

一个音频帧包含所有通道各一个样本。单声道 16 位音频一帧是 2 字节，双声道 16 位音频一帧是 4 字节。

`bytesAvailable()` 和 `framesAvailable()` 只在 `ActiveState` 或 `IdleState` 有效，其他状态返回 0。它们表示应用当前可以从内部设备读取的数据量；若长期不读取，缓冲满后会产生丢帧。

## 5. 停止、暂停和时间统计

### 5.1 `stop()` 与 `reset()`

`stop()` 停止采集并解除系统资源连接，将状态设为 `StoppedState`，同时清除错误。调用后 `start()` 返回的内部 `QIODevice *` 不能继续使用。

`reset()` 丢弃缓冲中的所有音频并把缓冲重置为空。需要放弃当前未处理的录音数据、切换输入管线或快速清除延迟时使用它。

### 5.2 `suspend()` 与 `resume()`

`suspend()` 暂停音频处理并保留已经缓冲的数据，状态变为 `SuspendedState`。`resume()` 只对暂停状态有意义，并恢复到暂停前的状态；其他状态调用不会启动新的采集。

如果业务要求“暂停期间绝不产生新的数据”，应使用 `suspend()`；如果业务要求“丢弃已有数据并重新开始”，应使用 `reset()` 后再 `start()`。

### 5.3 两种时间

- `processedUSecs()`：从 `start()` 起实际处理的音频时长；
- `elapsedUSecs()`：从 `start()` 起经过的墙上时间，包括 `IdleState` 和 `SuspendedState`。

例如应用因读取不及时进入 idle，`elapsedUSecs()` 仍会继续增长，但 `processedUSecs()` 只代表真正处理的音频量。统计录音文件对应的音频时长时，优先参考 `processedUSecs()` 和实际写入字节数。

## 6. API 逐项说明

### 构造、析构和查询

#### `QAudioSource(const QAudioFormat &format = QAudioFormat(), QObject *parent = nullptr)`

使用系统默认输入设备创建音频源。默认格式表示采用设备首选格式。

#### `QAudioSource(const QAudioDevice &audioDevice, const QAudioFormat &format = QAudioFormat(), QObject *parent = nullptr)`

使用 `audioDevice` 指定的输入设备创建音频源。默认格式表示采用该设备首选格式。

#### `~QAudioSource()`

销毁音频源，释放系统输入资源和内部缓冲。不会销毁应用传入的 `QIODevice`。

#### `bool isNull() const`

返回平台音频源实现是否为空。它适合用于早期防御性检查，但不替代启动后的格式、权限和设备错误检查。

#### `QAudioFormat format() const`

返回正在使用的音频格式。应用读取的每个样本都必须按该格式解释。

### 缓冲查询和设置

#### `void setBufferSize(qsizetype bytes)`（Qt 6.10）

在启动前按字节请求内部输入缓冲大小。启动后调用会被忽略，实际缓冲大小可能由后端调整。

#### `qsizetype bufferSize() const`（Qt 6.10）

返回内部缓冲字节数。启动前可能返回平台默认值或预设值，启动后返回实际使用值。

#### `void setBufferFrameCount(qsizetype frames)`

在启动前按音频帧数请求内部输入缓冲大小。启动后调用会被忽略，实际值通过 `bufferFrameCount()` 查询。

#### `qsizetype bufferFrameCount() const`

返回内部缓冲的帧数。启动后更能反映后端最终采用的大小。

#### `qsizetype bytesAvailable() const`

返回当前可从内部设备读取的字节数。仅在 `ActiveState` 或 `IdleState` 有效，否则返回 0。

#### `qsizetype framesAvailable() const`

返回当前可读取的音频帧数。仅在 `ActiveState` 或 `IdleState` 有效，否则返回 0。

### 音量

#### `void setVolume(qreal volume)`

设置输入流音量，按线性范围 `0.0` 到 `1.0` 解释，越界值会被钳制。它只影响当前输入流，不修改系统全局麦克风音量。

如果设备不支持输入音量调节，参数会被忽略，输入音量保持为 `1.0`。

#### `qreal volume() const`

返回输入流线性音量。设备不支持调节时返回 `1.0`。

### 启动和读取接口

#### `void start(QIODevice *device)`

开始从系统输入采集，并把 PCM 数据写到 `device`。目标设备必须已经以 `WriteOnly`、`Append` 或 `ReadWrite` 打开，且由调用方保证其生命周期。

成功时通常进入 `ActiveState` 或 `IdleState`；失败时通常进入 `StoppedState` 并报告 `OpenError`。

#### `QIODevice *start()`

启动并返回 Qt 内部的已打开设备，应用从它 `read()` 获取 PCM 数据。通常应在 `readyRead` 时尽快读取。

返回指针在 `stop()` 或再次 `start()` 后失效；Qt 不要求应用关闭或删除它。

#### `template <typename Callback> void start(Callback &&cb)`（Qt 6.11）

使用软实时回调启动。回调接收 `QSpan<const SampleType>`，其中 `SampleType` 必须匹配 `format().sampleFormat()`，span 内是交错音频样本。

回调不能做阻塞 I/O、锁竞争、动态内存分配或 UI 调用。回调签名不匹配、后端不支持回调或设备打开失败时，检查 `error()` 和 `state()`。

### 状态控制和计时

#### `void stop()`

停止采集、解除系统输入资源连接、清除错误并进入 `StoppedState`。

#### `void reset()`

丢弃当前输入缓冲中的所有音频并将缓冲清空。适合主动放弃未处理数据。

#### `void suspend()`

暂停采集处理并保留缓冲数据，进入 `SuspendedState`。

#### `void resume()`

从暂停状态恢复处理。当前不是 `SuspendedState` 时不会启动新的采集。

#### `qint64 processedUSecs() const`

返回从 `start()` 起已处理音频的时长，单位为微秒。

#### `qint64 elapsedUSecs() const`

返回从 `start()` 起经过的时间，单位为微秒，包括 idle 和 suspend 时段。

#### `QtAudio::Error error() const`

返回当前错误状态。启动失败或 I/O 异常时与 `state()` 一起检查。

#### `QtAudio::State state() const`

返回当前输入处理状态。

### 信号

#### `void stateChanged(QtAudio::State state)`

输入状态改变时发出。可用于更新录音按钮、检测启动失败、记录 idle/暂停状态。

Qt 6.6 及以前命名空间名为 `QAudio`。使用旧式字符串连接时，参数类型仍应写作 `QAudio::State`；新式函数指针连接使用当前的 `QtAudio::State`。

## 7. 常见误区与排查顺序

1. 先检查 `QAudioDevice::isFormatSupported()`，再启动录音。
2. 读取 `QIODevice` 模式的内部设备时要足够及时，否则环形缓冲满后会丢帧。
3. `IdleState` 不一定是设备故障，但输入模式下它意味着应用读取链路需要重点检查。
4. 不要缓存内部 `QIODevice *` 跨过 `stop()` 或下一次 `start()`。
5. `processedUSecs()` 与 `elapsedUSecs()` 含义不同，暂停或丢帧期间不能混用。
6. 使用回调时，将数据复制到预分配缓存即可；不要直接在音频线程写文件或发复杂 Qt 信号链。
7. 设备、权限和格式问题要分别排查；`reset()` 只能清理当前状态，不能修复外部条件。

## API 速查表

| 类别 | API | 语义 | 边界与注意 |
| --- | --- | --- | --- |
| 构造 | `QAudioSource(const QAudioFormat &format = QAudioFormat(), QObject *parent = nullptr)` | 用默认输入设备和指定/首选格式创建 source。 | 格式不自动转换。 |
| 构造 | `QAudioSource(const QAudioDevice &audioDevice, const QAudioFormat &format = QAudioFormat(), QObject *parent = nullptr)` | 用指定输入设备创建 source。 | 默认格式使用设备首选格式。 |
| 析构 | `~QAudioSource()` | 释放输入资源和内部缓冲。 | 不销毁应用传入的 `QIODevice`。 |
| 查询 | `bool isNull() const` | 查询平台实现是否为空。 | 不代替 start 后的错误检查。 |
| 查询 | `QAudioFormat format() const` | 返回 PCM 格式。 | 读取数据必须按此格式解释。 |
| 缓冲 | `void setBufferSize(qsizetype bytes)`（Qt 6.10） | 启动前按字节请求缓冲大小。 | 启动后忽略；实际值可能不同。 |
| 缓冲 | `qsizetype bufferSize() const`（Qt 6.10） | 返回缓冲字节数。 | 启动后查询实际值。 |
| 缓冲 | `void setBufferFrameCount(qsizetype frames)` | 启动前按帧请求缓冲大小。 | 启动后忽略。 |
| 缓冲 | `qsizetype bufferFrameCount() const` | 返回缓冲帧数。 | 启动后更接近后端实际值。 |
| 缓冲 | `qsizetype bytesAvailable() const` | 查询可读取字节数。 | 仅 Active/Idle 有效，否则为 0。 |
| 缓冲 | `qsizetype framesAvailable() const` | 查询可读取帧数。 | 仅 Active/Idle 有效，否则为 0。 |
| 音量 | `void setVolume(qreal volume)` | 设置输入流线性音量。 | `[0, 1]`，越界钳制；设备不支持时忽略。 |
| 音量 | `qreal volume() const` | 返回输入流音量。 | 不支持调节时返回 `1.0`。 |
| 启动 | `void start(QIODevice *device)` | 把采集 PCM 写入外部设备。 | 设备需 WriteOnly/Append/ReadWrite；不接管所有权。 |
| 启动 | `QIODevice *start()` | 返回 Qt 内部设备供应用 `read()`。 | stop 或再次 start 后指针失效。 |
| 启动 | `void start(Callback &&cb)`（Qt 6.11） | 在音频线程回调中读取交错 PCM。 | span 为 const；类型须匹配 sampleFormat；禁止阻塞。 |
| 控制 | `void stop()` | 停止采集并解除系统输入。 | 清除错误，内部设备不再有效。 |
| 控制 | `void reset()` | 丢弃所有输入缓冲。 | 适合快速放弃未处理数据。 |
| 控制 | `void suspend()` | 暂停并保留缓冲。 | 进入 SuspendedState。 |
| 控制 | `void resume()` | 从暂停恢复。 | 非暂停状态调用无效。 |
| 计时 | `qint64 processedUSecs() const` | 返回已处理音频时长。 | 与实际处理量相关。 |
| 计时 | `qint64 elapsedUSecs() const` | 返回 start 后经过时间。 | 包含 idle/suspend。 |
| 状态 | `QtAudio::Error error() const` | 查询错误状态。 | 与 state 一起检查。 |
| 状态 | `QtAudio::State state() const` | 查询输入状态机。 | 输入不及时可能 Idle 并丢帧。 |
| 信号 | `void stateChanged(QtAudio::State state)` | 通知状态变化。 | 用于 UI 和录音流程控制。 |
