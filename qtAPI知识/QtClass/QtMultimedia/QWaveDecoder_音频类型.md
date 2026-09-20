# QWaveDecoder：把 WAV 输入暴露为可读的 PCM 设备

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QWaveDecoder>`  
> 所属模块：`Qt6::Multimedia`  
> 继承：`QIODevice`  
> 类型性质：WAV 解析和 PCM 读取设备  
> 状态：Qt 6.11 已弃用

## 先看结论

`QWaveDecoder` 接受一个 `QIODevice` 形式的 WAV 输入，解析 RIFF/WAVE 头部，并把音频数据作为一个可读取的 `QIODevice` 暴露出来。它还提供解析出的 `QAudioFormat`、时长和格式就绪信号。

但是，Qt 6.11 的头文件已经明确将 `QWaveDecoder` 标记为弃用，并建议使用 `QAudioDecoder`。新项目不应围绕它设计公共接口；只有维护旧代码、需要兼容一个只支持 WAV 的旧读取路径时，才有必要理解它。

## 它解决什么问题

WAV 文件通常包含 RIFF/WAVE 容器头、格式块和数据块。业务代码如果直接读取文件，需要自己：

- 识别 RIFF/WAVE 标识；
- 读取采样率、声道数、位深和块对齐；
- 跳过 `JUNK` 或其它未知块；
- 找到 `data` 块；
- 处理数据还未完整到达的异步输入。

`QWaveDecoder` 把这些步骤包装成一个 `QIODevice`。应用可以等格式已知后读取解码后的 PCM 字节，而不必手工解析 WAV 头。

它不是通用媒体播放器，也不会把数据送到声卡。它的输出仍是原始音频字节，需要应用交给 `QAudioSink`、分析器或其它处理组件。

## 实际使用场景

- 旧版桌面程序从 `QFile` 读取 WAV 并直接送入音频输出。
- 从网络或自定义 `QIODevice` 逐步接收 WAV 数据。
- 在不引入完整媒体播放流程的情况下读取一个简单 WAV 文件。
- 维护 Qt 旧代码中依赖 `formatKnown()` 和 `parsingError()` 的路径。

新代码更适合使用：

```cpp
auto *decoder = new QAudioDecoder(this);
decoder->setSource(QUrl::fromLocalFile(filePath));
connect(decoder, &QAudioDecoder::bufferReady, this, [decoder] {
    const QAudioBuffer buffer = decoder->read();
    if (buffer.isValid())
        consume(buffer);
});
decoder->start();
```

`QAudioDecoder` 返回的是带格式、帧数和时间信息的 `QAudioBuffer`，而 `QWaveDecoder` 暴露的是 `QIODevice` 字节流，两者的处理模型不同。

## 输入设备和所有权

两个构造函数都接收 `QIODevice *`：

```cpp
QWaveDecoder decoder(&file);
```

输入设备由调用方管理。不要因为 decoder 持有一个指针就假设它取得了设备所有权；输入设备必须在 decoder 使用期间保持有效。

`setIODevice()` 可以替换当前输入设备。替换后应重新处理格式解析状态，不要继续使用旧输入对应的 `audioFormat()`、`duration()` 或当前位置假设。

输入设备可以是文件、内存设备或顺序设备。对于顺序设备，解析和读取通常依赖数据逐步到达，因此必须响应 `formatKnown()`、`parsingError()` 等异步信号，而不能假定构造完成后头信息已经可用。

## 两种构造方式

### `QWaveDecoder(QIODevice *device, QObject *parent = nullptr)`

从 WAV 输入设备解析原始格式。解析出的 WAV 格式成为 `audioFormat()` 的结果。

### `QWaveDecoder(QIODevice *device, const QAudioFormat &format, QObject *parent = nullptr)`

除了解析输入，还提供一个期望输出格式。具体格式转换能力受实现限制；它不是任意 PCM 重采样器。应检查实际 `audioFormat()` 和读取结果，不要只根据请求格式推断输出。

两个构造函数在 Qt 6.11 都已弃用。

## 解析和读取流程

典型的旧式流程如下：

```cpp
QFile file(path);
if (!file.open(QIODevice::ReadOnly))
    return;

auto *decoder = new QWaveDecoder(&file, this);

connect(decoder, &QWaveDecoder::formatKnown, this, [decoder] {
    const QAudioFormat format = decoder->audioFormat();
    if (!format.isValid())
        return;

    decoder->open(QIODevice::ReadOnly);
    QByteArray pcm = decoder->readAll();
    consumePcm(pcm, format);
});

connect(decoder, &QWaveDecoder::parsingError, this, [decoder] {
    decoder->close();
    reportWaveError();
});
```

实际项目中应根据输入设备是否顺序、数据是否分段到达以及旧代码的读取方式调整流程。`formatKnown()` 只表示格式已经解析出来，不等于全部 PCM 数据已经读取完。

## `QIODevice` 语义

### `open()` / `close()`

以 `QIODevice` 方式开始或结束读取。调用 `open(QIODevice::ReadOnly)` 前应确保头部已解析或当前实现允许延迟解析。`close()` 会关闭 decoder 的读取状态，不负责销毁输入设备。

### `read()` / `readAll()`

继承自 `QIODevice` 的读取函数取得解码后的 PCM 字节。可读取字节数受 WAV 数据块、当前位置和底层输入数据可用性影响。

### `seek()` / `pos()` / `size()`

用于在解码后的数据流中定位。是否可成功定位取决于输入设备和解析状态；顺序输入通常不能任意回退。

### `bytesAvailable()`

返回当前可读的解码数据量。对于正在到达的数据，它是动态值，不应在一次查询后长期缓存。

### `isSequential()`

反映当前设备是否只能顺序读取。对顺序输入返回 `true` 时，不要调用依赖随机访问的 `seek()` 逻辑。

## 元数据和信号

### `audioFormat()`

返回已解析或配置的 `QAudioFormat`。在格式尚未确定、解析失败或输入无效时，不能把它当成有效格式。

### `duration()`

返回 WAV 音频时长，接口类型为 `int`。在大文件、未知数据长度或解析尚未完成时，不要依赖它代表完整且高精度的时间轴；需要现代异步解码和时间信息时优先使用 `QAudioDecoder`。

### `getDevice()`

返回当前被包装的输入 `QIODevice *`。这是借用指针，不改变所有权，也不应在设备销毁后继续使用。

### `headerLength()`

返回实现定义的组合头长度常量，供旧式 WAV 解析代码参考。它不是所有 WAV 文件头的通用长度：WAV 允许出现可变长度和附加块，不能用它跳过任意文件的全部元数据。

### `formatKnown()`

格式解析完成后发出。此时可以读取 `audioFormat()`，但不表示整个音频已经解码完。

### `parsingError()`

输入不是可处理的 WAV、头部不完整且无法继续、块结构非法或读取失败时发出。应停止读取并向上层报告，而不是继续把未知字节当作 PCM。

## 线程和生命周期边界

`QWaveDecoder` 是 `QIODevice`/`QObject`，应在所属线程中使用。输入 `QIODevice`、decoder 和接收信号的对象需要遵守 Qt 的线程亲和性规则。

异步输入场景下，底层设备产生数据的线程不能直接并发修改 decoder 依赖的设备状态；应通过信号、事件队列或线程安全的自定义设备传递数据。

## 常见误区

- 在 Qt 6.11 新代码中继续选择它，而没有先评估 `QAudioDecoder`。
- 认为 `formatKnown()` 表示所有 PCM 数据都已准备好。
- 把 `headerLength()` 当成任意 WAV 文件都可跳过的固定头长度。
- 关闭或销毁输入 `QIODevice` 后仍继续读取 decoder。
- 把 `QWaveDecoder` 的 PCM 输出误认为已经连接到扬声器。
- 认为请求 `QAudioFormat` 就一定会完成重采样或样本格式转换。
- 在顺序设备上假设 `seek()` 一定成功。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QWaveDecoder(QIODevice *, QObject *parent = nullptr)` | 从输入设备解析 WAV 格式。 | Qt 6.11 已弃用。 |
| 构造 | `QWaveDecoder(QIODevice *, const QAudioFormat &, QObject *parent = nullptr)` | 解析 WAV 并请求输出格式。 | 转换能力受实现限制；已弃用。 |
| 生命周期 | `~QWaveDecoder()` | 销毁 decoder。 | 不要据此假设输入设备归它所有。 |
| 信息 | `QAudioFormat audioFormat() const` | 返回当前音频格式。 | 格式未知或失败时不可用。 |
| 信息 | `QIODevice *getDevice()` | 返回被包装的输入设备。 | 借用指针，不转移所有权。 |
| 信息 | `int duration() const` | 返回音频时长。 | 大文件或未知长度时不要过度依赖。 |
| 静态 | `static qint64 headerLength()` | 返回实现的组合头长度参考值。 | 不是任意 WAV 的通用跳过长度。 |
| 输入 | `void setIODevice(QIODevice *)` | 替换输入设备。 | 替换后重新等待解析状态。 |
| 设备 | `bool open(QIODevice::OpenMode)` | 打开 decoder 设备。 | 常用 `ReadOnly`。 |
| 设备 | `void close()` | 关闭读取。 | 不负责销毁输入设备。 |
| 定位 | `bool seek(qint64)` | 尝试定位解码数据流。 | 顺序设备可能不支持。 |
| 定位 | `qint64 pos() const` | 返回当前读取位置。 | 单位为输出字节流位置。 |
| 容量 | `qint64 size() const` | 返回可知的输出大小。 | 输入未完成时可能不完整。 |
| 读取 | `qint64 bytesAvailable() const` | 查询当前可读字节数。 | 动态值，不应长期缓存。 |
| 读取 | `bool isSequential() const` | 判断是否只能顺序读取。 | 顺序设备不能任意回退。 |
| 信号 | `void formatKnown()` | 通知格式已经解析。 | 不表示全部数据就绪。 |
| 信号 | `void parsingError()` | 通知 WAV 解析失败。 | 停止读取并报告错误。 |

### 一句话总结

`QWaveDecoder` 是旧式的 WAV 到 PCM `QIODevice` 适配器；在 Qt 6.11 它已弃用，新代码应优先采用返回 `QAudioBuffer` 的 `QAudioDecoder`。
