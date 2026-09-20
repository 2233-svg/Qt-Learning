# QAudioDevice：描述一个输入或输出音频设备

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAudioDevice>`  
> 所属模块：`Qt6::Multimedia`  
> 继承：无  
> 类型性质：值类型、设备信息快照

## 它解决什么问题

`QAudioDevice` 描述系统中的一个音频输入或输出设备。它把设备标识、显示名称、方向以及可接受的音频格式能力提供给：

- `QAudioSource`：从输入设备采集原始音频；
- `QAudioSink`：向输出设备播放原始音频；
- `QMediaCaptureSession`：选择录音输入；
- `QMediaPlayer`：选择播放输出。

它是设备信息，不是打开的硬件句柄。构造或复制 `QAudioDevice` 不会启动采集或占用扬声器。

## 实际使用场景：设备从哪里取得

设备列表和默认设备由 `QMediaDevices` 提供：

```cpp
const QAudioDevice output = QMediaDevices::defaultAudioOutput();
if (output.isNull())
    return;

QAudioFormat format = output.preferredFormat();
if (!output.isFormatSupported(format))
    return;

auto *sink = new QAudioSink(output, format, this);
```

也可以遍历 `QMediaDevices::audioInputs()` 或 `audioOutputs()`，用 `description()` 呈现给用户，用 `id()` 作为稳定选择依据。

## 快照语义和设备热插拔

`QAudioDevice` 会在其生命周期内保留创建时的属性，即使物理设备断开、重命名或设置改变，已有对象也不会自动刷新。要跟踪变化，应在 `QMediaDevices` 的设备变化信号发出后重新获取设备实例。

因此不要长期缓存一个设备对象并假定它永远代表当前硬件。设备被移除后，基于旧对象创建的新 `QAudioSink`/`QAudioSource` 可能失败或表现为设备不可用；应用应重新选择设备并重建相关 I/O 对象。

## 格式能力不是独立区间的笛卡尔积

设备会分别提供最小/最大采样率、最小/最大声道数和支持的采样格式，但这些信息只是能力概览。实际支持的是“采样率、声道数、样本格式组成的完整组合”。

例如设备可能支持 44100 Hz 立体声和 48000 Hz 单声道，却不支持把任意采样率与任意声道数自由组合。需要准确判断时直接调用 `isFormatSupported()`。

## 方向、空设备与所有权

`mode()` 表示 `Null`、`Input` 或 `Output`。默认构造得到 null device，使用任何能力属性前都应先检查 `isNull()`。

`QAudioDevice` 是可复制和可移动的值类型。它不拥有实际硬件，也不替 `QAudioSink` 或 `QAudioSource` 管理资源。设备的 `description()` 适合显示给用户，`id()` 适合持久化用户选择，但仍应处理设备后来消失的情况。

## 逐项 API 说明

### `enum QAudioDevice::Mode`

描述设备方向：

| 枚举值 | 含义 |
| --- | --- |
| `Null` | 无效或空设备。 |
| `Input` | 音频输入设备，例如麦克风。 |
| `Output` | 音频输出设备，例如扬声器。 |

### `[read-only] QString description() const`

返回设备的人类可读名称，适合显示在设备选择界面。它是展示文本，不应作为跨平台稳定 ID 使用。

### `[read-only] QByteArray id() const`

返回设备标识。设备名称可能随平台或插件变化，而 ID 用来区分设备。持久化后仍要验证当前列表是否包含它，因为设备可能已拔出或重新枚举。

### `[read-only] bool isDefault() const`

判断该快照是否代表系统默认音频设备。默认设备可能因系统设置变化而改变，旧对象的结果不会自动更新。

### `[read-only] QAudioDevice::Mode mode() const`

返回设备方向。默认构造对象返回 `Null`。

### `QAudioDevice()`

构造 null device。它不对应可用硬件，通常只用于声明变量或表示“尚未选择设备”。

### `QAudioDevice(const QAudioDevice &other)`

复制设备信息快照。复制不打开或复制硬件资源。

### `QAudioDevice(QAudioDevice &&other) noexcept`

移动设备信息到当前对象。移动后的源对象只应视为可析构、可重新赋值的对象，不要继续依赖其原快照内容。

### `~QAudioDevice() noexcept`

销毁设备信息对象，不会关闭或释放音频硬件，因为该类本身不拥有硬件会话。

### `QAudioFormat::ChannelConfig channelConfiguration() const`

返回设备报告的声道配置。它补充 `minimumChannelCount()` 和 `maximumChannelCount()`，可用于了解默认或标准声道布局。

### `bool isFormatSupported(const QAudioFormat &settings) const`

判断完整的 `QAudioFormat` 组合是否受设备支持。它会综合采样率、声道数和采样格式，不能用三个独立范围的判断替代。

传入无效格式时不要把结果当作“设备支持所有格式”；先构造完整有效格式，再查询。

### `bool isNull() const`

判断当前对象是否没有有效设备定义。默认构造对象返回 `true`。

### `int maximumChannelCount() const`

返回设备支持的最大声道数。它是能力边界，不保证每个采样率和样本格式下都能达到该数量。

### `int maximumSampleRate() const`

返回设备支持的最大采样率，单位 Hz。它不是一个保证所有声道配置都可用的独立上限。

### `int minimumChannelCount() const`

返回设备支持的最小声道数。常见单声道设备为 1，立体声设备为 2，但具体值以设备报告为准。

### `int minimumSampleRate() const`

返回设备支持的最小采样率，单位 Hz。实际可用组合仍应通过 `isFormatSupported()` 验证。

### `QAudioFormat preferredFormat() const`

返回平台或音频插件为该设备提供的默认格式。输入设备和输出设备可能有不同默认值，例如输入偏向单声道、输出偏向立体声。

它适合用作初始配置，不等于所有应用都必须使用的格式；需要固定格式时仍要检查支持情况。

### `QList<QAudioFormat::SampleFormat> supportedSampleFormats() const`

返回设备支持的样本格式列表。它只列样本类型，不能单独证明某个采样率和声道数组合也受支持。

### `void swap(QAudioDevice &other) noexcept`

交换两个设备信息快照。不会改变系统硬件，也不会打开或关闭设备。

### `bool operator==(const QAudioDevice &other) const`

判断两个对象是否表示同一个音频设备。可用于比较用户选择是否仍对应同一设备。

### `bool operator!=(const QAudioDevice &other) const`

判断两个对象是否表示不同音频设备。

### `QAudioDevice &operator=(const QAudioDevice &other)`

复制赋值设备快照。赋值只更新当前值对象，不影响硬件。

### `QAudioDevice &operator=(QAudioDevice &&other) noexcept`

移动赋值设备快照。移动后源对象不再保证保留原快照内容。

## 常见误区

- 把 `QAudioDevice` 当成已打开的设备；实际 I/O 由 `QAudioSink`/`QAudioSource` 完成。
- 把 `description()` 当稳定 ID；跨平台选择应保存 `id()`，并处理设备消失。
- 缓存对象后不响应 `QMediaDevices` 变化，导致使用过期能力信息。
- 把最小/最大范围和样本格式列表拼成任意组合；最终组合必须 `isFormatSupported()`。
- 对默认构造对象直接读取能力，忘记先检查 `isNull()`。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `Mode { Null, Input, Output }` | 表示设备方向或空设备。 | 默认构造为 `Null`。 |
| 属性 | `description()` | 返回用户可读设备名称。 | 只用于展示，不是稳定 ID。 |
| 属性 | `id()` | 返回设备标识。 | 可用于持久化选择，但需处理设备消失。 |
| 属性 | `isDefault()` | 判断是否为默认设备。 | 旧快照不会随系统默认设备变化自动更新。 |
| 属性 | `mode()` | 返回输入、输出或空方向。 | 空设备先检查 `isNull()`。 |
| 构造 | `QAudioDevice()` | 创建 null device。 | 不对应硬件。 |
| 构造 | `QAudioDevice(const QAudioDevice &)` | 复制设备快照。 | 不打开硬件。 |
| 构造 | `QAudioDevice(QAudioDevice &&)` | 移动设备快照。 | 源对象不再保证原内容。 |
| 析构 | `~QAudioDevice()` | 销毁设备信息对象。 | 不负责释放硬件会话。 |
| 能力 | `channelConfiguration()` | 返回设备声道配置。 | 与声道数范围互补。 |
| 能力 | `minimumChannelCount()` / `maximumChannelCount()` | 返回声道数范围。 | 不代表每个组合都支持。 |
| 能力 | `minimumSampleRate()` / `maximumSampleRate()` | 返回采样率范围，单位 Hz。 | 仍需验证完整格式组合。 |
| 能力 | `supportedSampleFormats()` | 返回支持的样本类型。 | 不能独立代表完整格式支持。 |
| 能力 | `preferredFormat()` | 返回平台推荐默认格式。 | 适合初始配置，仍可检查。 |
| 能力 | `isFormatSupported(const QAudioFormat &)` | 判断完整格式是否支持。 | 这是最终组合检查。 |
| 状态 | `isNull()` | 判断是否为空设备。 | 默认对象为 `true`。 |
| 工具 | `swap(QAudioDevice &)` | 交换两个设备快照。 | 不影响系统设备。 |
| 比较 | `operator==` / `operator!=` | 比较是否代表同一设备。 | 用于选择和缓存判断。 |
| 赋值 | `operator=(const QAudioDevice &)` | 复制赋值快照。 | 不改变硬件。 |
| 赋值 | `operator=(QAudioDevice &&)` | 移动赋值快照。 | 源对象不再保证原内容。 |

---

### 一句话总结

`QAudioDevice` 是音频硬件的能力快照，不是硬件句柄；设备变化后重新从 `QMediaDevices` 获取，格式组合用 `isFormatSupported()` 做最终确认。
