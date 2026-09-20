# QAudioFormat：定义原始音频的采样、声道和布局

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAudioFormat>`  
> 所属模块：`Qt6::Multimedia`  
> 继承：无  
> 类型性质：值类型

## 它解决什么问题

`QAudioFormat` 描述原始音频字节应如何解释。一个完整有效的格式由三部分组成：

- 采样率 `sampleRate()`，单位 Hz；
- 声道数/声道配置 `channelCount()`、`channelConfig()`；
- 每个样本的存储类型 `sampleFormat()`。

没有它，一串 PCM 字节只能被视为无意义的二进制数据。`QAudioBuffer`、`QAudioSink`、`QAudioSource`、`QAudioDecoder` 和 `QAudioDevice` 都依赖它来计算帧大小、持续时间和设备兼容性。

Qt 的原始音频样本按主机端字节序处理，声道通常按交错方式排列：一帧包含同一时刻每个声道各一个样本。

## 实际使用场景：创建有效格式

```cpp
QAudioFormat format;
format.setSampleRate(48000);
format.setChannelConfig(QAudioFormat::ChannelConfigStereo);
format.setSampleFormat(QAudioFormat::Int16);

Q_ASSERT(format.isValid());
qDebug() << format.bytesPerSample()
         << format.bytesPerFrame()
         << format.durationForFrames(480);
```

也可以先设置声道数：

```cpp
format.setChannelCount(2);
```

但 `setChannelCount()` 会把 `channelConfig()` 重置为 `ChannelConfigUnknown`。如果需要知道具体的前左、前右、LFE 等位置，应最后调用 `setChannelConfig()`。

## 三个计数维度

假设 48 kHz、立体声、16 位整数：

- 一个样本 2 字节；
- 一个帧包含两个声道样本，所以 4 字节；
- 480 帧对应 10 ms；
- 480 帧对应 1920 字节。

通常有以下关系：

```text
bytesPerFrame = bytesPerSample * channelCount
duration(us) ~= frameCount * 1,000,000 / sampleRate
```

以帧为单位处理，才能正确计算多声道音频的时长和设备缓冲大小。`framesForBytes()`、`bytesForDuration()` 等函数会执行整数换算，输入不能精确表示整帧或整采样周期时会发生舍入。

## 有效性与声道配置

默认构造的格式为 `sampleRate == 0`、`channelCount == 0`、`sampleFormat == Unknown`，因此无效。`isValid()` 只有在所有必要参数有效时才返回 `true`。

`channelConfig()` 是声道位置的配置，而 `channelCount()` 是数量；两者有关但不是同一概念。未知配置仍可能有一个有效的声道数，例如通过 `setChannelCount(2)` 设置的立体声数量，但这时不能用 `channelOffset()` 推断左/右声道位置。

`channelOffset()` 找不到指定位置，或配置未知时返回 `-1`。不要把未知配置当作隐含的标准立体声。

## 样本格式和归一化

`SampleFormat` 支持：

- `UInt8`：8 位无符号整数；
- `Int16`：16 位有符号整数；
- `Int32`：32 位有符号整数；
- `Float`：浮点样本；
- `Unknown`：未指定。

`normalizedSampleValue()` 根据当前格式把一个样本映射到约 `-1` 到 `1` 的浮点范围。传入的指针必须指向与 `sampleFormat()` 匹配的样本对象，并且在调用期间有效；函数不会替你验证指针或样本类型。

## 成员类型

### `enum AudioChannelPosition`

定义声道在声场中的位置：

| 枚举值 | 语义 |
| --- | --- |
| `UnknownPosition` | 位置未知。 |
| `FrontLeft` / `FrontRight` | 前左 / 前右。 |
| `FrontCenter` | 前中。 |
| `LFE` / `LFE2` | 低频效果声道 1 / 2。 |
| `BackLeft` / `BackRight` | 后左 / 后右。 |
| `BackCenter` | 后中。 |
| `SideLeft` / `SideRight` | 侧左 / 侧右。 |
| `FrontLeftOfCenter` / `FrontRightOfCenter` | 前中左 / 前中右。 |
| `TopFrontLeft` / `TopFrontRight` / `TopFrontCenter` | 顶部前左 / 前右 / 前中。 |
| `TopCenter` | 顶部中。 |
| `TopBackLeft` / `TopBackRight` / `TopBackCenter` | 顶部后左 / 后右 / 后中。 |
| `TopSideLeft` / `TopSideRight` | 顶部侧左 / 侧右。 |
| `BottomFrontCenter` / `BottomFrontLeft` / `BottomFrontRight` | 底部前中 / 前左 / 前右。 |

### `enum ChannelConfig`

标准配置包括：

| 枚举值 | 声道位置顺序 |
| --- | --- |
| `ChannelConfigUnknown` | 位置未知。 |
| `ChannelConfigMono` | `FrontCenter`。 |
| `ChannelConfigStereo` | `FrontLeft, FrontRight`。 |
| `ChannelConfig2Dot1` | `FrontLeft, FrontRight, LFE`。 |
| `ChannelConfig3Dot0` | `FrontLeft, FrontRight, FrontCenter`。 |
| `ChannelConfig3Dot1` | `FrontLeft, FrontRight, FrontCenter, LFE`。 |
| `ChannelConfigSurround5Dot0` | 前左、前右、前中、后左、后右。 |
| `ChannelConfigSurround5Dot1` | 前左、前右、前中、LFE、后左、后右。 |
| `ChannelConfigSurround7Dot0` | 前左、前右、前中、后左、后右、侧左、侧右。 |
| `ChannelConfigSurround7Dot1` | 前左、前右、前中、LFE、后左、后右、侧左、侧右。 |

### `enum SampleFormat`

| 枚举值 | 含义 | 每样本字节数 |
| --- | --- | --- |
| `Unknown` | 未指定。 | 0 |
| `UInt8` | 8 位无符号整数。 | 1 |
| `Int16` | 16 位有符号整数。 | 2 |
| `Int32` | 32 位有符号整数。 | 4 |
| `Float` | 浮点样本。 | 4 |

## 逐项 API 说明

### `QAudioFormat()`

创建无效格式：采样率和声道数为 0，样本格式为 `Unknown`。

### `QAudioFormat(const QAudioFormat &other)`

复制格式值。它只复制描述信息，不涉及音频数据或设备资源。

### `~QAudioFormat() noexcept`

销毁格式值对象。

### `qint32 bytesForDuration(qint64 microseconds) const`

计算当前格式表示指定微秒数所需的字节数。格式无效时返回 `0`；微秒数不能精确对应整帧时会发生舍入。

### `qint32 bytesForFrames(qint32 frameCount) const`

计算指定完整帧数所需字节数。格式无效时返回 `0`。每帧大小由样本大小和声道数共同决定。

### `int bytesPerFrame() const`

返回一帧的字节数，即每个声道一个样本的总大小。格式无效时返回 `0`。

### `int bytesPerSample() const`

返回一个样本的字节数。格式无效时返回 `0`；`UInt8`、`Int16`、`Int32` 和 `Float` 分别对应 1、2、4、4 字节。

### `QAudioFormat::ChannelConfig channelConfig() const`

返回当前声道位置配置。若仅设置了 `channelCount()`，配置通常为 `ChannelConfigUnknown`。

### `static constexpr QAudioFormat::ChannelConfig channelConfig(Args... channels)`

根据一组 `AudioChannelPosition` 生成声道配置。它适合表达标准枚举中没有直接命名的布局，例如按指定顺序组合若干声道位置。

参数应是有效的声道位置枚举；该函数只构造布局描述，不改变任何 `QAudioFormat` 对象。

### `int channelCount() const`

返回当前声道数量。它表示每帧包含多少个样本，不表示这些样本的空间位置。

### `int channelOffset(QAudioFormat::AudioChannelPosition channel) const`

返回指定声道位置在一帧中的索引。找不到该声道，或当前声道配置未知时返回 `-1`。

### `static QAudioFormat::ChannelConfig defaultChannelConfigForChannelCount(int channelCount)`

根据声道数量返回默认配置。标准配置定义到 8 声道；更高数量会使用 `AudioChannelPosition` 中前面的声道位置填充，不代表真实硬件一定采用该布局。

### `qint64 durationForBytes(qint32 bytes) const`

计算指定字节数代表的时长，单位微秒。格式无效时返回 `0`；字节数不是完整帧整数倍时会舍入。

### `qint64 durationForFrames(qint32 frameCount) const`

计算指定帧数的时长，单位微秒。结果由采样率决定，不能把它当作毫秒。

### `qint32 framesForBytes(qint32 byteCount) const`

计算指定字节数包含的帧数。每帧含所有声道各一个样本；字节数不是完整帧整数倍时会舍入。

### `qint32 framesForDuration(qint64 microseconds) const`

计算表示指定时长所需的帧数。微秒数不是采样周期的整数倍时会舍入。

### `bool isValid() const`

判断采样率、声道数和样本格式是否都有效。默认构造格式返回 `false`。

### `float normalizedSampleValue(const void *sample) const`

将一个与当前样本格式匹配的样本转换到约 `-1` 到 `1` 的浮点范围。调用者必须传入有效、正确类型且正确对齐的样本地址；该 API 不执行类型检查。

### `QAudioFormat::SampleFormat sampleFormat() const`

返回样本存储类型。

### `int sampleRate() const`

返回采样率，单位 Hz。

### `void setChannelConfig(QAudioFormat::ChannelConfig config)`

设置标准或自定义声道配置，同时更新声道数。它会让 `channelCount()` 与配置中的位置数量一致。

### `void setChannelCount(int channels)`

设置声道数，并把声道配置重置为 `ChannelConfigUnknown`。如果应用还需要精确的声道位置，应在之后调用 `setChannelConfig()`。

### `void setSampleFormat(QAudioFormat::SampleFormat format)`

设置样本格式。它决定一个样本的字节数以及原始数据应按哪种 C++ 数值类型解释。

### `void setSampleRate(int samplerate)`

设置采样率，单位 Hz。采样率参与所有帧、字节和时长之间的换算。

### `bool operator==(const QAudioFormat &a, const QAudioFormat &b)`

判断两个格式的采样率、声道信息和样本格式是否相同。

### `bool operator!=(const QAudioFormat &a, const QAudioFormat &b)`

判断两个格式是否不同。

## 常见误区

- 只设置采样率就把格式传给设备；还需要有效声道数和样本格式。
- 把 `channelCount()` 当成有明确左右位置；使用 `setChannelCount()` 后配置是未知的。
- 设置 `channelConfig()` 后又调用 `setChannelCount()`，导致配置被重置。
- 把 `bytesPerSample()` 当作一帧大小；多声道必须使用 `bytesPerFrame()`。
- 用错误的 C++ 类型调用 `normalizedSampleValue()` 或读取 PCM。
- 把微秒 API 的结果当毫秒；`durationForBytes()` 和 `durationForFrames()` 返回微秒。
- 认为最小/最大采样率可以推导设备全部组合；设备兼容性由 `QAudioDevice::isFormatSupported()` 最终判断。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QAudioFormat()` | 创建默认无效格式。 | 采样率、声道数为 0，样本格式为 `Unknown`。 |
| 构造 | `QAudioFormat(const QAudioFormat &)` | 复制格式值。 | 不复制音频数据或设备。 |
| 析构 | `~QAudioFormat()` | 销毁格式值。 | 无外部资源。 |
| 枚举 | `AudioChannelPosition` | 描述声道空间位置。 | 未知位置不能用于可靠偏移计算。 |
| 枚举 | `ChannelConfig` | 描述声道位置组合。 | `setChannelConfig()` 会同步改变声道数。 |
| 枚举 | `SampleFormat` | 描述样本数值类型。 | `Unknown` 使格式无效。 |
| 设置 | `setSampleRate(int)` | 设置采样率，单位 Hz。 | 参与帧/字节/时长换算。 |
| 设置 | `setChannelCount(int)` | 设置声道数量。 | 会重置 `channelConfig()` 为未知。 |
| 设置 | `setChannelConfig(ChannelConfig)` | 设置标准声道布局。 | 同时更新 `channelCount()`。 |
| 设置 | `setSampleFormat(SampleFormat)` | 设置样本存储类型。 | 决定每样本字节数。 |
| 查询 | `sampleRate()` | 读取采样率。 | 单位 Hz。 |
| 查询 | `channelCount()` | 读取声道数。 | 每帧样本数量，不等于位置布局。 |
| 查询 | `channelConfig()` | 读取声道布局。 | 可能为 `ChannelConfigUnknown`。 |
| 查询 | `sampleFormat()` | 读取样本格式。 | 用于选择正确 C++ 类型。 |
| 查询 | `isValid()` | 判断格式是否完整有效。 | 默认格式无效。 |
| 计数 | `bytesPerSample()` | 返回每样本字节数。 | 无效格式返回 `0`。 |
| 计数 | `bytesPerFrame()` | 返回每帧字节数。 | 包含全部声道。 |
| 计数 | `bytesForFrames(qint32)` | 计算帧数所需字节。 | 无效格式返回 `0`。 |
| 计数 | `framesForBytes(qint32)` | 计算字节对应帧数。 | 非整帧会舍入。 |
| 计时 | `bytesForDuration(qint64)` | 计算时长所需字节。 | 参数/结果单位分别是微秒/字节。 |
| 计时 | `durationForBytes(qint32)` | 计算字节代表时长。 | 返回微秒；非整帧会舍入。 |
| 计时 | `framesForDuration(qint64)` | 计算时长所需帧数。 | 非整采样周期会舍入。 |
| 计时 | `durationForFrames(qint32)` | 计算帧数代表时长。 | 返回微秒。 |
| 声道 | `channelOffset(AudioChannelPosition)` | 查找声道在一帧中的索引。 | 未知配置或不存在时返回 `-1`。 |
| 静态辅助 | `channelConfig(Args...)` | 从声道位置生成布局。 | 只生成值，不修改对象。 |
| 静态辅助 | `defaultChannelConfigForChannelCount(int)` | 按数量生成默认布局。 | 高于 8 声道是顺序填充的默认值。 |
| 样本 | `normalizedSampleValue(const void *)` | 将样本归一化为浮点值。 | 指针类型必须匹配当前格式。 |
| 比较 | `operator==` / `operator!=` | 比较两个格式值。 | 比较格式描述，不比较数据。 |

---

### 一句话总结

`QAudioFormat` 是原始音频的解释合同：先让采样率、声道和样本格式完整有效，再用帧作为基本单位计算字节、时长和设备兼容性。
