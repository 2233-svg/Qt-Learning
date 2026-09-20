# QAudioDecoder：异步取得解码后的原始音频

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAudioDecoder>`  
> 所属模块：`Qt6::Multimedia`  
> 继承：`QObject`

## 它解决什么问题

`QAudioDecoder` 是面向应用层的音频解码器。它读取音频文件或一个 `QIODevice`，把压缩格式解码成一块一块的 `QAudioBuffer`，由应用自行处理。

它与 `QMediaPlayer` 的关键区别是：`QMediaPlayer` 通常把音频继续送往播放设备，而 `QAudioDecoder` 把解码结果交给应用。适合：

- 读取 MP3、AAC、WAV 等媒体中的 PCM 数据；
- 做波形、频谱、响度和语音特征分析；
- 转换或导出音频；
- 在测试中逐块验证解码结果。

它不负责播放，也不提供随机访问的任意样本接口。输出以异步 `QAudioBuffer` 块为单位。

## 实际使用场景和解码状态机

一个稳定的使用顺序是：

1. 创建解码器并确认 `isSupported()`。
2. 用 `setSource()` 指定 URL，或用 `setSourceDevice()` 指定设备，二者只能选一个。
3. 连接 `bufferReady()`、`finished()` 和错误信号。
4. 调用 `start()`。
5. 每次收到 `bufferReady()`，调用 `read()` 取走当前缓冲；也可以在读取前检查 `bufferAvailable()`。
6. `finished()` 表示成功完成；失败时处理 `error(QAudioDecoder::Error)` 和 `errorString()`。

`read()` 不会阻塞。如果当前没有可用缓冲或发生失败，它返回无效的 `QAudioBuffer`。因此不要在启动后立即用一次 `read()` 期待拿到数据，也不要用定时器忙等；应由信号驱动读取。

```cpp
auto *decoder = new QAudioDecoder(this);

connect(decoder, &QAudioDecoder::bufferReady, this, [decoder] {
    while (decoder->bufferAvailable()) {
        const QAudioBuffer buffer = decoder->read();
        if (buffer.isValid())
            consume(buffer);
    }
});

connect(decoder, &QAudioDecoder::finished, this, [] {
    qDebug() << "decode finished";
});

connect(decoder,
        qOverload<QAudioDecoder::Error>(&QAudioDecoder::error),
        this,
        [decoder](QAudioDecoder::Error error) {
            qWarning() << error << decoder->errorString();
        });

decoder->setSource(QUrl::fromLocalFile("/path/to/audio.wav"));
decoder->start();
```

## 输入源和输出格式

`setSource()` 与 `setSourceDevice()` 互斥。设置其中一个会停止当前解码、丢弃已有音频缓冲，并清除另一个来源。切换文件时不要继续处理切换前排队的结果。

`setAudioFormat()` 只能在 stopped 状态调用；运行中调用会被忽略。传入有效格式表示希望解码器转换输出，传入无效格式表示使用原始解码格式。如果请求格式不受支持，错误状态会变成 `FormatError`。

Qt 6.11.1 文档特别说明：指定目标格式在默认 FFmpeg backend 上可用，但 Android backend 尚不支持。跨平台代码应准备好使用原始格式并在应用侧转换。

`audioFormat()` 返回解码器当前设置的格式；如果设置的是无效格式，它可能与实际输出样本的格式不同。处理每个缓冲时，最终应以 `buffer.format()` 为准。

## 时间和生命周期

`duration()` 和 `position()` 的单位是毫秒。尚不可用时返回 `-1`；`position()` 表示最近一次读取的缓冲位置，而不是当前后台线程已经解码到的精确游标。

对象属于 QObject 模型，父对象可以管理其销毁。解码任务由对象和事件循环协作完成，通常不要在工作过程中跨线程直接操作它；如需放入专用线程，应在线程归属确定后创建并通过 queued signal/slot 驱动。

连接到 `bufferReady()` 的处理器应及时取走数据。如果要异步处理，按值保存 `QAudioBuffer`，不要保存信号回调期间的引用或裸数据指针。

## 错误类型

- `NoError`：没有发生错误。
- `ResourceError`：无法解析或打开媒体资源。
- `FormatError`：媒体格式或请求的目标格式不受支持。
- `AccessDeniedError`：缺少访问资源所需的权限。
- `NotSupportedError`：当前平台不支持该解码器。

错误枚举说明“发生了哪类问题”，`errorString()` 提供可展示或记录的文字描述。失败时不要等待 `finished()`；文档定义成功完成走 `finished()`，失败走错误信号。

## 逐项 API 说明

### `enum QAudioDecoder::Error`

表示解码器错误状态：

| 枚举值 | 含义 |
| --- | --- |
| `NoError` | 没有错误。 |
| `ResourceError` | 媒体资源无法解析或访问。 |
| `FormatError` | 资源格式或目标解码格式不支持。 |
| `AccessDeniedError` | 没有足够权限访问媒体资源。 |
| `NotSupportedError` | 当前平台不支持 `QAudioDecoder`。 |

### `[read-only] bool bufferAvailable() const`

判断当前是否有已解码且可以通过 `read()` 取得的缓冲。为 `false` 时调用 `read()` 仍然安全，但会返回无效缓冲且不会阻塞。

### `[read-only] QString errorString() const`

返回当前错误的人类可读描述；没有错误时返回空字符串。它对应属性 `error` 的访问函数，通常与错误枚举一起记录。

### `[read-only] bool isDecoding() const`

返回解码器当前是否正在运行。它适合显示忙碌状态，但异步状态变化应优先连接 `isDecodingChanged(bool)`，不要靠高频轮询。

### `QUrl source() const`

返回当前文件来源。如果最近调用的是 `setSourceDevice()`，这里返回空 URL。它不代表当前 `QIODevice` 来源。

### `void setSource(const QUrl &fileName)`

设置待解码的文件 URL。设置时会停止当前解码并丢弃排队缓冲，同时取消设备来源。可使用本地文件 URL、远程 URL 或后端支持的其他 URL。

设置源只完成配置，不会自动开始解码；仍需调用 `start()`。

### `void setSourceDevice(QIODevice *device)`

设置待解码的 `QIODevice`。解码器使用该设备作为输入，不拥有设备；设备的生命周期必须覆盖解码过程。设置时会停止当前解码并丢弃已有缓冲，同时清除文件 URL。

设备应处于适合读取的状态，并满足目标 backend 对顺序读取、可寻址性或打开模式的要求。

### `QIODevice *sourceDevice() const`

返回当前设备来源；如果当前使用 `setSource()`，返回 `nullptr`。返回指针不转移所有权。

### `explicit QAudioDecoder(QObject *parent = nullptr)`

创建解码器对象。可传入父对象由 QObject 父子关系管理。

### `~QAudioDecoder() override noexcept`

销毁解码器。销毁前会结束对象拥有的解码状态；应用仍应先停止或解除外部处理逻辑，避免在析构后使用其指针。

### `QAudioFormat audioFormat() const`

返回解码器设置的目标格式。设置无效格式时，它表示“使用原始格式”的意图，可能不同于最终解码样本格式；实际输出应检查 `QAudioBuffer::format()`。

### `qint64 duration() const`

返回音频流总时长，单位毫秒；元数据尚不可用时返回 `-1`。它可能是估算值，并通过 `durationChanged()` 更新。

### `QAudioDecoder::Error error() const`

返回当前错误枚举。没有错误时为 `NoError`。

### `bool isSupported() const`

返回当前平台是否支持音频解码。它是能力查询，不表示当前 URL 一定存在、权限一定足够或具体格式一定可解码。

### `qint64 position() const`

返回最近一次从解码器读取的缓冲在流中的位置，单位毫秒；尚未读取缓冲时返回 `-1`。位置变化通过 `positionChanged()` 通知。

### `QAudioBuffer read() const`

读取当前可用的一块解码音频。没有可用缓冲或读取失败时返回无效 `QAudioBuffer`，并且不会阻塞。

应在 `bufferReady()` 或确认 `bufferAvailable()` 后调用。读取后要根据 `QAudioBuffer::format()`、`isValid()` 和数据计数处理结果。

### `void setAudioFormat(const QAudioFormat &format)`

设置解码目标格式，只在 stopped 状态有效。有效格式会请求转换；无效格式会恢复原始音频格式。若 backend 不支持该目标格式，会设置 `FormatError`。

### `void start()`

开始异步解码。解码出足够数据后发出 `bufferReady()`，应用再调用 `read()`。没有源或源不可读时，错误会通过错误状态和信号报告。

再次 `start()` 通常从当前配置的源开始新的解码流程；需要从头开始时，按文档语义先 `stop()`，再重新 `start()`。

### `void stop()`

停止解码并结束当前处理。之后再次 `start()` 会从源开头恢复解码；停止过程中不要继续把旧缓冲当成新一轮结果。

### `[signal] void bufferAvailableChanged(bool available)`

通知是否存在可读的解码缓冲。`available == true` 表示可以尝试 `read()`；`false` 表示当前没有缓冲。

### `[signal] void bufferReady()`

通知新解码缓冲可供读取。通常在槽中循环 `read()` 或在循环条件中检查 `bufferAvailable()`。

### `[signal] void durationChanged(qint64 duration)`

通知估算的总时长发生变化，单位毫秒。媒体元数据可能在解码过程中才可用。

### `[signal] void error(QAudioDecoder::Error error)`

通知发生解码错误。该信号与无参数同名属性接口可能造成连接歧义，连接带枚举参数的重载时使用 `qOverload<QAudioDecoder::Error>()`。

### `[signal] void finished()`

通知解码成功完成。失败时走错误信号，不应把没有收到 `finished()` 简单解释为“仍有数据”。

### `[signal] void formatChanged(const QAudioFormat &format)`

通知当前音频格式改变。输出转换、源格式识别或后端初始化可能触发它。

### `[signal] void isDecodingChanged(bool decoding)`

通知 `isDecoding()` 状态改变。适合启用或禁用界面控制。

### `[signal] void positionChanged(qint64 position)`

通知最近读取位置改变，单位毫秒。

### `[signal] void sourceChanged()`

通知文件来源属性改变。设置设备来源后，`source()` 为空，但仍会发出来源状态变化通知。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `Error` | 表示解码错误类别。 | `finished()` 只表示成功；失败处理错误信号。 |
| 属性 | `bufferAvailable` | 表示是否有可读缓冲。 | `false` 时 `read()` 返回无效缓冲且不阻塞。 |
| 属性 | `error` / `errorString()` | 提供错误枚举和文字描述。 | 无错误时文字为空；枚举信号有重载歧义。 |
| 属性 | `isDecoding` | 表示当前是否正在解码。 | 用 `isDecodingChanged()` 观察变化。 |
| 属性 | `source` | 返回当前文件 URL。 | 使用设备来源时为空。 |
| 构造/析构 | `QAudioDecoder(QObject *)`、`~QAudioDecoder()` | 创建和销毁异步解码器。 | 遵守 QObject 父子关系和线程归属。 |
| 查询 | `QAudioFormat audioFormat() const` | 返回目标或设置的音频格式。 | 无效设置可能不同于实际输出格式。 |
| 查询 | `bool isSupported() const` | 查询平台解码能力。 | 不保证具体资源可访问或格式可解码。 |
| 查询 | `qint64 duration() const` | 返回总时长，单位毫秒。 | 不可用时 `-1`，可能后续更新。 |
| 查询 | `qint64 position() const` | 返回最近读取位置，单位毫秒。 | 未读缓冲时 `-1`。 |
| 查询 | `QAudioDecoder::Error error() const` | 返回错误枚举。 | 与同名信号连接时明确重载。 |
| 输入 | `void setSource(const QUrl &)` | 设置文件来源。 | 会停止解码、丢弃缓冲并清除设备来源。 |
| 输入 | `void setSourceDevice(QIODevice *)` | 设置设备来源。 | 不拥有设备；会清除文件来源。 |
| 输入 | `QUrl source() const` | 读取文件来源。 | 使用设备来源时返回空 URL。 |
| 输入 | `QIODevice *sourceDevice() const` | 读取设备来源。 | 文件来源时返回 `nullptr`，不转移所有权。 |
| 格式 | `void setAudioFormat(const QAudioFormat &)` | 设置解码目标格式。 | 只能 stopped 时设置；无效格式表示原始格式。 |
| 读取 | `QAudioBuffer read() const` | 取出一块已解码音频。 | 在 `bufferReady()` 后调用；不阻塞。 |
| 控制 | `void start()` | 开始异步解码。 | 通过信号获取数据和完成状态。 |
| 控制 | `void stop()` | 停止并重置当前解码流程。 | 再次开始从源开头解码。 |
| 信号 | `bufferAvailableChanged(bool)` | 通知缓冲可用性变化。 | `true` 时读取，`false` 时不要忙等。 |
| 信号 | `bufferReady()` | 通知新缓冲可读。 | 槽中及时取走，重处理放到其他线程。 |
| 信号 | `durationChanged(qint64)` | 通知总时长更新。 | 单位毫秒。 |
| 信号 | `error(QAudioDecoder::Error)` | 通知解码失败。 | 用 `qOverload` 选择该重载。 |
| 信号 | `finished()` | 通知成功完成。 | 失败不会以此信号报告。 |
| 信号 | `formatChanged(const QAudioFormat &)` | 通知当前格式变化。 | 以每个输出 buffer 的格式为最终依据。 |
| 信号 | `isDecodingChanged(bool)` | 通知运行状态变化。 | 适合更新界面状态。 |
| 信号 | `positionChanged(qint64)` | 通知读取位置变化。 | 单位毫秒，反映最近读取位置。 |
| 信号 | `sourceChanged()` | 通知文件来源变化。 | 文件/设备来源互斥切换时触发。 |

---

### 一句话总结

`QAudioDecoder` 是异步的“压缩音频到 `QAudioBuffer`”转换器：设置一种输入源，启动后在 `bufferReady()` 中非阻塞读取，成功看 `finished()`，失败看错误信号。
