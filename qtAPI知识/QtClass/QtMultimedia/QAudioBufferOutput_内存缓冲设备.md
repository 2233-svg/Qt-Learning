# QAudioBufferOutput：接收 QMediaPlayer 解码出的原始音频

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAudioBufferOutput>`  
> 所属模块：`Qt6::Multimedia`  
> 继承：`QObject`

## 它解决什么问题

`QAudioBufferOutput` 是 `QMediaPlayer` 的原始音频观察端。播放器解码媒体时，可以把解码得到的 `QAudioBuffer` 通过 `audioBufferReceived()` 发给应用，用于：

- 实时音量表和峰值检测；
- 波形或频谱可视化；
- 音频特征分析；
- 将解码 PCM 交给自定义 DSP 或其他处理管线。

它不是音频输出设备，不会替代扬声器播放。它只提供播放器解码阶段的数据旁路。

## 实际使用场景与连接方式

```cpp
QMediaPlayer player;
QAudioBufferOutput output;

player.setAudioBufferOutput(&output);

connect(&output, &QAudioBufferOutput::audioBufferReceived,
        this, &Analyzer::processBuffer);

player.setSource(QUrl("file:///path/to/audio.mp3"));
player.play();
```

`QAudioBufferOutput` 只由应用持有的 `QMediaPlayer` 使用，不拥有播放器。两者在播放和信号处理期间必须同时存活。解除输出时调用 `QMediaPlayer::setAudioBufferOutput(nullptr)` 或设置其他输出对象，避免播放器继续向已销毁对象发送数据。

该类目前只支持 FFmpeg backend。运行时是否能收到缓冲取决于后端、媒体是否含音频轨、播放器是否实际解码以及输出对象是否仍连接。

## 输出格式选择

无参构造时，输出缓冲的格式由媒体文件和播放器内部音频解码器决定。带有效 `QAudioFormat` 构造时，要求输出缓冲使用该格式；传入无效格式则回到由媒体和解码器决定的行为。

格式一旦确定，处理器应依据每个缓冲的 `format()` 读取样本。不要仅依据构造时的期望格式把所有输入强制解释成同一种 C++ 样本类型，因为具体后端可能产生与预期不同的格式，尤其是在使用无效格式或不同媒体源时。

## 信号处理与性能

`audioBufferReceived()` 在播放器产生新的解码块时发出。处理器应尽量快速完成工作；频谱、波形等重计算可以把数据复制或转移到工作线程，但要明确 `QAudioBuffer` 的共享语义和线程同步。

信号参数是 `const QAudioBuffer &`。如果要异步保存，按值复制 `QAudioBuffer`，不要保存引用或底层 `constData()` 指针。复制通常是显式共享的，真正修改副本前仍需 `detach()`。

信号不是“文件全部解码完成”的通知，也不保证每次缓冲大小固定。播放暂停、跳转、后端缓冲和媒体格式都会影响回调节奏。

## 逐项 API 说明

### `explicit QAudioBufferOutput(QObject *parent = nullptr)`

创建不指定输出格式的对象。收到的缓冲格式由媒体源和播放器内部解码器决定。

### `explicit QAudioBufferOutput(const QAudioFormat &format, QObject *parent = nullptr)`

创建带输出格式要求的对象。传入有效格式时，输出缓冲应使用该格式；传入无效格式时，格式仍由媒体和内部解码器决定。

### `~QAudioBufferOutput() override noexcept`

销毁输出对象。销毁前应从 `QMediaPlayer` 解除连接，或确保播放器先于输出对象停止并清除该输出指针。

### `[signal] void audioBufferReceived(const QAudioBuffer &buffer)`

通知应用收到播放器解码的一块音频缓冲。缓冲可能是无效或空数据的边界结果时，处理代码应检查 `buffer.isValid()`，并依据 `buffer.format()` 解释样本。

如果要跨越信号调用保存数据，复制整个 `QAudioBuffer`；不要保存信号参数引用。

### `QAudioFormat format() const`

返回构造时指定的输出格式。有效格式表示输出缓冲的目标格式；无效格式表示不预先指定，由媒体和解码器决定。

它不是对最近一次 `audioBufferReceived()` 缓冲格式的查询。要知道实际收到的格式，读取信号参数的 `buffer.format()`。

## 常见误区

- 把 `QAudioBufferOutput` 当作扬声器输出或播放控制类。
- 忘记只支持 FFmpeg backend，部署到其他环境后没有备用路径。
- 保存 `audioBufferReceived()` 的引用或内部指针到槽函数返回之后。
- 不检查实际 `buffer.format()` 就按固定样本类型读取。
- 把信号当作固定周期回调，或在槽函数中执行长时间阻塞操作。
- 只设置输出对象却没有启动播放器、设置媒体源或确认媒体包含音频轨。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `explicit QAudioBufferOutput(QObject *parent = nullptr)` | 创建由媒体决定输出格式的对象。 | 实际格式读取每个 `QAudioBuffer`。 |
| 构造 | `explicit QAudioBufferOutput(const QAudioFormat &, QObject *parent = nullptr)` | 创建带目标格式的输出对象。 | 无效格式表示交给媒体和解码器决定。 |
| 析构 | `~QAudioBufferOutput()` | 销毁输出对象。 | 先解除播放器连接。 |
| 查询 | `QAudioFormat format() const` | 返回构造时指定的输出格式。 | 不是最近缓冲的实际格式查询。 |
| 信号 | `void audioBufferReceived(const QAudioBuffer &buffer)` | 收到播放器解码缓冲。 | 依据 `buffer.format()` 读取；异步保存需按值复制。 |

---

### 一句话总结

`QAudioBufferOutput` 为 `QMediaPlayer` 提供一条原始 PCM 旁路，适合做音频分析和可视化；它只负责接收解码缓冲，实际格式与生命周期都要按每个 `QAudioBuffer` 检查。
