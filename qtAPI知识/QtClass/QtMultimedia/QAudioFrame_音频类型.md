# QAudioFrame：按编译期声道布局访问单个音频帧

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAudioBuffer>`  
> 所属模块：`Qt6::Multimedia`  
> 类型性质：公开类模板，定义在 `qaudiobuffer.h` 中

## 它解决什么问题

原始音频通常是交错存储的：一个音频帧包含同一时刻所有声道各一个样本。直接用 `float *` 或 `qint16 *` 访问时，代码必须自己记住声道顺序；多声道布局变化后，索引很容易写错。

`QAudioFrame<ChannelConfig, SampleFormat>` 用两个编译期参数描述：

- `ChannelConfig`：这一帧有哪些声道位置；
- `SampleFormat`：每个样本的 C++ 存储类型。

模板内部提供 `channels[]`、按声道位置读取的 `value()`、写入的 `setValue()`、下标运算符和 `clear()`，适合在已经确认格式的音频处理代码中表示一个完整帧。

它不是 `QAudioBuffer`，也不负责分配音频流、转换格式或连接设备。它只是一个轻量的帧形状描述和存储结构。

## 实际使用场景

- 在 `QAudioBuffer::data<QAudioBuffer::S16S>()` 得到的交错数据上逐帧访问左右声道。
- 写入一个固定声道布局的合成器或测试信号。
- 处理单声道、立体声、5.1 等已知布局，避免把声道位置硬编码成数组下标。
- 用同一套模板代码支持 `UInt8`、`Int16`、`Int32` 和 `Float` 样本格式。

使用前必须确认 `QAudioFormat::channelConfig()` 和 `sampleFormat()` 与模板参数一致。模板不会读取运行时 `QAudioFormat`，也不会验证指针指向的内存。

## 模板参数和内存布局

```cpp
using Stereo16 = QAudioFrameStereo<QAudioFormat::Int16>;

auto *frames = buffer.data<Stereo16>();
for (qsizetype i = 0; i < buffer.frameCount(); ++i) {
    const qint16 left = frames[i].value(QAudioFormat::FrontLeft);
    const qint16 right = frames[i].value(QAudioFormat::FrontRight);
    processStereo(left, right);
}
```

`QAudioFrameStereo<Format>` 是：

```cpp
QAudioFrame<QAudioFormat::ChannelConfigStereo, Format>
```

`channels[]` 的排列不是按枚举声明顺序，而是按 `ChannelConfig` 位掩码中从低位到高位的声道位置排列。`positionToIndex()` 会计算某个声道位置在数组中的索引。

例如立体声配置包含 `FrontLeft` 和 `FrontRight`，因此 `channels[0]` 对应左声道，`channels[1]` 对应右声道。对于包含 LFE 或环绕声道的配置，必须使用 `value()` 或 `setValue()`，不要凭感觉猜索引。

## 默认值和未知声道

模板为不同采样格式定义了默认样本：

- `UInt8` 的静音中心值是 `128`；
- `Int16`、`Int32` 和 `Float` 的默认值是 `0`。

因此 `clear()` 不是简单地保证字节全为零：对 `UInt8` 帧，它会把每个样本设为 `128`。

如果传入的声道位置不在 `ChannelConfig` 中：

- `value()` 返回该格式的默认值；
- `operator[]` 与 `value()` 相同；
- `setValue()` 不执行任何写入。

这使得读取一个不存在的声道不会越界，但也可能掩盖布局错误。业务代码应先确认布局，而不是把默认值当成真实音频。

## 生命周期和安全边界

`QAudioFrame` 是普通聚合式模板结构，`channels[]` 直接存储在对象内部。它不拥有 `QAudioBuffer` 的底层内存，也没有运行时格式字段。

从 `QAudioBuffer` 取得指针时要注意：

- 指针必须按完整帧类型解释；
- `QAudioBuffer` 的格式、共享状态和生命周期必须保持有效；
- 不能把不同采样格式或不同声道布局的缓冲强制转换成同一个 `QAudioFrame` 类型；
- `QAudioFrame` 的大小必须与实际音频帧步长一致，否则数组步进会错误。

对 `UInt8` 音频，样本值通常按无符号字节存储，但“静音”位于 128，不是 0。进行归一化或混音前仍需遵守 `QAudioFormat` 的数值语义。

## 成员类型别名

`QAudioBuffer` 预先提供了常用别名：

| 别名 | 展开形式 |
| --- | --- |
| `QAudioBuffer::U8M` | `QAudioFrameMono<QAudioFormat::UInt8>` |
| `QAudioBuffer::S16M` | `QAudioFrameMono<QAudioFormat::Int16>` |
| `QAudioBuffer::S32M` | `QAudioFrameMono<QAudioFormat::Int32>` |
| `QAudioBuffer::F32M` | `QAudioFrameMono<QAudioFormat::Float>` |
| `QAudioBuffer::U8S` | `QAudioFrameStereo<QAudioFormat::UInt8>` |
| `QAudioBuffer::S16S` | `QAudioFrameStereo<QAudioFormat::Int16>` |
| `QAudioBuffer::S32S` | `QAudioFrameStereo<QAudioFormat::Int32>` |
| `QAudioBuffer::F32S` | `QAudioFrameStereo<QAudioFormat::Float>` |

这些别名只是类型名，不会转换数据，也不会检查 `QAudioBuffer::format()`。

## 逐项 API 说明

### `value_type`

由 `SampleFormat` 映射得到的样本 C++ 类型：

| `SampleFormat` | `value_type` | 默认值 |
| --- | --- | --- |
| `UInt8` | `unsigned char` | `128` |
| `Int16` | `short` | `0` |
| `Int32` | `int` | `0` |
| `Float` | `float` | `0.0f` |

### `value(AudioChannelPosition pos) const`

按声道位置取得样本。如果该位置属于模板的 `ChannelConfig`，函数返回对应的 `channels[]` 元素；否则返回采样格式的默认值。

它不会抛异常，也不会报告布局错误。要判断布局是否正确，应先检查运行时 `QAudioFormat`。

### `setValue(AudioChannelPosition pos, value_type val)`

按声道位置写入样本。声道存在时更新对应元素；声道不存在时静默忽略。

### `operator[](AudioChannelPosition pos) const`

`value(pos)` 的便捷写法，只读。它不是按数组整数索引访问；传入的是 `QAudioFormat::AudioChannelPosition`。

### `clear()`

把帧中的全部声道设置为该采样格式的默认值。`UInt8` 使用 `128`，其它支持格式使用 `0`。

### `positionToIndex(AudioChannelPosition pos)`

编译期可求值的静态函数。声道存在时返回它在 `channels[]` 中的索引，不存在时返回 `-1`。

它依赖 `ChannelConfig` 的位掩码布局，不接受运行时修改后的声道集合。

## 常见误区

- 把 `QAudioFrame` 当成带运行时格式信息的对象；它没有 `sampleFormat()` 或 `channelCount()`。
- 忘记检查 `QAudioBuffer::format()` 就直接 `data<QAudioBuffer::S16S>()`。
- 把 `channels[]` 当成按 `AudioChannelPosition` 数值直接索引的数组。
- 把 `UInt8` 的静音值误认为 0。
- 在不存在的声道上调用 `value()` 后，把返回的默认值当作真实声道数据。
- 把一个 `QAudioFrame` 当作整段 `QAudioBuffer`；它只代表一帧。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 模板 | `QAudioFrame<ChannelConfig, SampleFormat>` | 描述固定声道布局和样本格式的一帧。 | 不带运行时格式检查。 |
| 数据 | `value_type` | 暴露样本的 C++ 类型。 | 必须与 `SampleFormat` 匹配。 |
| 数据 | `value_type channels[nChannels]` | 按布局顺序保存每个声道样本。 | 顺序由位掩码决定。 |
| 查询 | `static constexpr int positionToIndex(AudioChannelPosition)` | 将声道位置映射到数组索引。 | 不存在时返回 `-1`。 |
| 读取 | `value(AudioChannelPosition) const` | 按声道位置读取样本。 | 不存在的声道返回默认值。 |
| 读取 | `operator[](AudioChannelPosition) const` | `value()` 的下标语法。 | 参数是声道位置，不是整数数组下标。 |
| 写入 | `setValue(AudioChannelPosition, value_type)` | 按声道位置写入样本。 | 不存在的声道静默忽略。 |
| 清空 | `clear()` | 将所有样本恢复为格式默认值。 | `UInt8` 默认值是 128。 |
| 别名 | `QAudioFrameMono<Format>` | 单声道帧特化。 | 仍需匹配运行时格式。 |
| 别名 | `QAudioFrameStereo<Format>` | 立体声帧特化。 | 左右声道按布局排列。 |
| 别名 | `QAudioFrame2Dot1<Format>` | 2.1 声道帧特化。 | 包含 LFE。 |
| 别名 | `QAudioFrameSurround5Dot1<Format>` | 5.1 声道帧特化。 | 不要自行猜通道索引。 |
| 别名 | `QAudioFrameSurround7Dot1<Format>` | 7.1 声道帧特化。 | 结合 `AudioChannelPosition` 访问。 |

### 一句话总结

`QAudioFrame` 是“已知格式的一帧”访问工具：它能按声道位置读写样本，但不会替你验证运行时格式、管理缓冲区或转换音频。
