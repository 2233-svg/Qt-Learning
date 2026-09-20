# QAudioBuffer：带格式和时间戳的音频帧数据块

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAudioBuffer>`  
> 所属模块：`Qt6::Multimedia`  
> 继承：无  
> 类型性质：显式共享值类型

## 它解决什么问题

`QAudioBuffer` 表示一段已经按某种 `QAudioFormat` 编排好的原始音频数据。它不只是一个 `QByteArray`：除了字节数据，还记录：

- 音频格式，例如采样率、声道数和采样格式；
- 完整音频帧数；
- 音频持续时间；
- 该数据块在原始音频流中的起始时间。

`QAudioDecoder` 用它把解码后的音频交给应用；`QAudioBufferInput` 也用它接收应用准备好的原始音频。应用可以读取这些数据进行波形、音量或频谱分析，也可以在确认格式匹配后修改或转发它们。

## 实际使用场景

- 从 `QAudioDecoder::bufferReady()` 读取一块 PCM 数据，送入波形或频谱分析器。
- 将麦克风、合成器或自定义生成器产生的 PCM 数据封装成缓冲，再交给 `QAudioBufferInput` 录制。
- 在不复制音频内容的前提下把缓冲放入队列，等后台任务处理。
- 根据 `startTime()` 和 `duration()` 将解码数据放入时间轴。

它不负责播放、录音或设备 I/O。需要实际连接硬件时，应使用 `QAudioSink`、`QAudioSource`；需要编解码时，应与 `QAudioDecoder`、`QMediaRecorder` 等类配合。

## 音频帧、样本和字节

一个音频帧（frame）是在同一时刻包含所有声道各一个样本的交错集合。以立体声为例：

```text
frame 0: left sample, right sample
frame 1: left sample, right sample
```

因此：

- `frameCount()` 是完整帧数；
- `sampleCount()` 是所有声道样本总数，通常等于 `frameCount() * channelCount()`；
- `byteCount()` 是原始数据总字节数；
- `duration()` 由帧数和采样率决定，单位是微秒。

构造时若字节数不是完整帧大小的整数倍，尾部多余字节不会被计入完整帧。处理数据时应以 `frameCount()` 和格式计算出的完整范围为准，不要把尾部当作合法样本。

## 生命周期、共享与线程

`QAudioBuffer` 是显式共享值类型。复制构造或复制赋值通常只复制共享数据的引用，不立即复制全部音频字节；移动则转移内部共享状态。

通过非 const `data<T>()` 修改数据前，应调用 `detach()`，把当前对象与其他共享副本分离。这样可以避免修改一个缓冲时意外改变其他副本看到的内容。`constData<T>()` 用于只读访问，优先于 const 对象上的 `data<T>()`，因为后者可能触发不必要的深拷贝。

类本身不提供跨线程同步。把缓冲按值复制后交给另一个线程通常很方便，但底层数据在一方通过可写指针修改时，仍要自行保证没有并发读写冲突。

## 创建和读取示例

```cpp
QAudioFormat format;
format.setSampleRate(48000);
format.setChannelCount(2);
format.setSampleFormat(QAudioFormat::Int16);

QByteArray pcm = readPcmBytes();
QAudioBuffer buffer(pcm, format, 0);

if (!buffer.isValid())
    return;

const auto *samples = buffer.constData<qint16>();
for (qsizetype i = 0; i < buffer.sampleCount(); ++i)
    processSample(samples[i]);
```

模板参数只是告诉 Qt“把地址按什么 C++ 类型返回”，不会验证它与 `format().sampleFormat()`、声道布局或字节序相匹配。调用者必须自己保证类型正确；不匹配时按错误类型读取会产生错误结果，甚至触发未对齐或越界访问。

## 有效性和时间语义

默认构造得到空的无效缓冲。`isValid()` 只有在格式有效且包含多于零个完整帧时才返回 `true`。因此一个格式正确但没有数据的缓冲仍然不是可处理的有效音频块。

`startTime()` 使用微秒。如果缓冲来自连续流并带有时间位置，返回该块起始点；如果它不是某条流的一部分，则返回 `-1`。不要把 `-1` 当成零时刻。

## 逐项 API 说明

### `QAudioBuffer() noexcept`

创建空的无效缓冲。它没有有效格式，也没有音频帧；使用前应通过 `isValid()` 检查，或先赋予有效数据。

### `QAudioBuffer(const QByteArray &data, const QAudioFormat &format, qint64 startTime = -1)`

用字节数组和格式创建音频缓冲。构造函数会复制 `data` 的内容，之后调用方修改原 `QByteArray` 不会改变缓冲中的数据。

格式决定如何解释每个样本和帧。如果字节数不是完整帧大小的整数倍，尾部多余数据被忽略。`startTime` 以微秒表示；不属于流时使用默认值 `-1`。

### `QAudioBuffer(int numFrames, const QAudioFormat &format, qint64 startTime = -1)`

创建一个能容纳指定完整帧数的缓冲，并按格式分配空间。样本会初始化为该格式的默认值。

`numFrames` 应为非负的合理数量，实际字节需求由格式决定。格式无效时不要把返回对象当作可写的有效音频块。`startTime` 仍是微秒或 `-1`。

### `QAudioBuffer(const QAudioBuffer &other) noexcept`

复制构造缓冲。音频数据采用显式共享，复制通常不会立即复制所有字节；若后续要修改当前副本，应先 `detach()`。

### `QAudioBuffer(QAudioBuffer &&other) noexcept`

从 `other` 移动构造当前缓冲。移动后 `other` 仍是可析构、可重新赋值的对象，但不应继续依赖它原来的数据状态。

### `~QAudioBuffer() noexcept`

销毁缓冲对象并释放其对共享音频存储的引用。不会影响仍由其他副本持有的共享数据。

### `qsizetype byteCount() const noexcept`

返回缓冲中音频数据的字节数。它反映可访问的原始字节总量，不等于样本数，也不一定等于调用方最初传入的字节数，因为非完整帧尾部不会作为有效帧使用。

### `template <typename T> const T *constData() const`

以只读 `T` 指针返回音频数据。函数不检查 `T` 是否匹配实际格式，只提供便捷的类型转换；调用方必须选择正确的样本类型。

只读场景优先使用它。相比 const 对象上的 `data<T>()`，它明确表达不修改数据，也可避免隐式共享实现为了提供可写接口而深拷贝。

### `template <typename T> T *data()`

返回可写的 `T` 指针。因为对象显式共享，调用它并准备修改数据前应先 `detach()`，确保当前修改不会影响其他共享副本。

返回的指针只在该缓冲及其底层存储仍有效时可用。不要让它跨越缓冲重新赋值、移动或析构后继续使用。

### `template <typename T> const T *data() const`

以只读指针返回音频数据，但在语义和性能上不如 `constData<T>()` 清晰。新代码的只读访问应直接调用 `constData<T>()`。

它同样不验证模板参数。`T` 必须与实际数据布局匹配。

### `void detach()`

将当前缓冲与其他共享副本分离，保证当前对象拥有一份可独立修改的数据。没有其他副本共享时，调用它可能不需要实际复制。

典型顺序是 `buffer.detach(); auto *p = buffer.data<Sample>();`。如果只读，不需要调用 `detach()`。

### `qint64 duration() const noexcept`

返回这段音频的持续时间，单位为微秒。结果由 `format()` 和 `frameCount()` 共同决定；格式无效或帧数为零时不应把它当作有意义的播放时长。

### `QAudioFormat format() const noexcept`

返回解释该缓冲数据所需的音频格式。格式中的采样率、声道数、采样格式等属性会影响帧数、字节数和持续时间的计算。

### `qsizetype frameCount() const noexcept`

返回完整音频帧数量。一帧包含同一时刻每个声道各一个样本。多声道交错数据不能把每个样本都当成一个帧。

### `bool isValid() const noexcept`

当缓冲格式有效且包含多于零个完整帧时返回 `true`。它是处理解码结果或外部输入的第一道检查，不代表模板类型、声道顺序或数值范围一定符合业务预期。

### `qsizetype sampleCount() const noexcept`

返回所有声道的样本总数。立体声数据中，左右声道样本都计入结果；如果总样本数为 1000，则通常每个声道各有 500 个交错样本。

### `qint64 startTime() const noexcept`

返回该缓冲在音频流中的起始时间，单位为微秒。不属于流时返回 `-1`。它是时间轴信息，不是系统时钟时间。

### `void swap(QAudioBuffer &other) noexcept`

交换两个缓冲的内部数据和元信息。适合在容器或算法中以低成本交换值对象；不会逐样本复制音频内容。

### `QAudioBuffer &operator=(QAudioBuffer &&other) noexcept`

将 `other` 移动赋值给当前对象。当前对象原先持有的共享数据引用会被替换；移动后不要依赖 `other` 的原数据状态。

### `QAudioBuffer &operator=(const QAudioBuffer &other)`

复制赋值当前缓冲。赋值采用显式共享语义；若之后通过可写 `data<T>()` 修改当前对象，应先 `detach()`。

## 常见误区

- 把 `sampleCount()` 当成 `frameCount()`；多声道时两者不同。
- 忘记检查格式就用 `constData<qint16>()`；模板参数不会自动校验。
- 修改共享数据前不调用 `detach()`，导致其他副本观察到不符合预期的改变。
- 把 `byteCount()` 直接除以单个样本大小而忽略声道数和完整帧。
- 把 `startTime() == -1` 当作“从零开始”。
- 以为 `QAudioBuffer` 会播放音频；它只是数据块，不连接设备。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QAudioBuffer()` | 创建空的无效缓冲。 | 使用前检查 `isValid()`。 |
| 构造 | `QAudioBuffer(const QByteArray &, const QAudioFormat &, qint64 startTime = -1)` | 从原始字节复制创建缓冲。 | 非完整帧尾部被忽略；格式决定解释方式。 |
| 构造 | `QAudioBuffer(int numFrames, const QAudioFormat &, qint64 startTime = -1)` | 分配指定帧数的缓冲。 | 帧数必须合理；格式无效时不要当有效音频使用。 |
| 构造 | `QAudioBuffer(const QAudioBuffer &)` | 复制缓冲。 | 显式共享；修改前 `detach()`。 |
| 构造 | `QAudioBuffer(QAudioBuffer &&)` | 移动构造缓冲。 | 源对象只保证可析构或重新赋值。 |
| 析构 | `~QAudioBuffer()` | 释放当前共享引用。 | 不影响其他副本。 |
| 数据 | `qsizetype byteCount() const` | 返回原始数据字节数。 | 不等于样本数；只关注完整帧范围。 |
| 数据 | `const T *constData() const` | 只读取得指定类型的数据指针。 | 不检查 `T`；只读优先使用。 |
| 数据 | `T *data()` | 取得可写数据指针。 | 修改前调用 `detach()`。 |
| 数据 | `const T *data() const` | const 对象上取得只读指针。 | 新代码优先 `constData<T>()`。 |
| 共享 | `void detach()` | 分离共享存储。 | 为当前对象准备独立可写副本。 |
| 元信息 | `qint64 duration() const` | 返回持续时间，单位微秒。 | 依赖格式和完整帧数。 |
| 元信息 | `QAudioFormat format() const` | 返回数据格式。 | 决定样本、帧和时长的解释。 |
| 元信息 | `qsizetype frameCount() const` | 返回完整音频帧数。 | 一帧包含所有声道各一个样本。 |
| 元信息 | `qsizetype sampleCount() const` | 返回所有声道样本总数。 | 多声道会包含全部声道。 |
| 元信息 | `qint64 startTime() const` | 返回流中起始时间，单位微秒。 | 非流数据返回 `-1`。 |
| 状态 | `bool isValid() const` | 判断格式有效且有完整帧。 | 不代表模板类型已匹配。 |
| 工具 | `void swap(QAudioBuffer &other)` | 交换两个缓冲。 | 适合低成本交换值对象。 |
| 运算符 | `operator=(const QAudioBuffer &)` | 复制赋值。 | 仍是显式共享语义。 |
| 运算符 | `operator=(QAudioBuffer &&)` | 移动赋值。 | 源对象不再保留原数据保证。 |
| 类型别名 | `F32M`、`F32S` | 32 位浮点单声道/立体声样本特化名。 | 只表达预期样本形态，仍需匹配格式。 |
| 类型别名 | `S16M`、`S16S` | 16 位有符号单声道/立体声样本特化名。 | 不会替你转换数据。 |
| 类型别名 | `S32M`、`S32S` | 32 位有符号单声道/立体声样本特化名。 | 使用前确认采样格式和声道数。 |
| 类型别名 | `U8M`、`U8S` | 8 位无符号单声道/立体声样本特化名。 | 只读写类型别名不改变底层格式。 |

---

### 一句话总结

`QAudioBuffer` 是带格式、帧数、持续时间和流时间的原始音频数据块；处理它时先确认格式，再区分 frame、sample、byte，并在修改显式共享数据前调用 `detach()`。
