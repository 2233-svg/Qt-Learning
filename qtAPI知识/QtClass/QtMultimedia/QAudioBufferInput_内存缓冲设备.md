# QAudioBufferInput：把自定义原始音频送入录制管线

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAudioBufferInput>`  
> 所属模块：`Qt6::Multimedia`  
> 继承：`QObject`

## 它解决什么问题

`QAudioBufferInput` 是 `QMediaCaptureSession` 的自定义音频输入端。它允许应用不依赖麦克风设备，而是把自己生成或从其他来源取得的 `QAudioBuffer` 送入 `QMediaRecorder`。

典型来源包括：

- 游戏或合成器生成的 PCM；
- 网络接收到并转换后的音频帧；
- 第三方音频解码器或 DSP 输出；
- 测试程序中的确定性音频样本。

它只负责把缓冲交给录制管线，不负责把数据编码成文件，也不负责播放。真正的编码和文件写入由连接到同一 `QMediaCaptureSession` 的 `QMediaRecorder` 完成。

## 实际使用场景、后端和连接关系

该类目前只由 FFmpeg backend 支持。部署到其他后端或平台时，不能仅凭编译成功就认为运行时可用，应按目标环境验证。

基本连接关系是：

```cpp
QMediaCaptureSession session;
QMediaRecorder recorder;
QAudioBufferInput input(format);

session.setRecorder(&recorder);
session.setAudioBufferInput(&input);

connect(&input, &QAudioBufferInput::readyToSendAudioBuffer,
        &generator, &Generator::produceNext);

recorder.record();
```

`QAudioBufferInput` 不拥有 `QMediaCaptureSession`。会话、录音器和输入对象必须在录制期间同时存活，通常让它们拥有共同的父对象或由同一个控制器管理。

## 推送节奏与背压

`readyToSendAudioBuffer()` 是输入端可以接受新数据的通知。收到后，可以调用一次或循环调用 `sendAudioBuffer()`，直到它返回 `false`：

```cpp
void Generator::produceNext()
{
    while (true) {
        const QAudioBuffer buffer = nextBuffer();
        if (!input->sendAudioBuffer(buffer))
            break;
        if (buffer.isValid() == false)
            break;
    }
}
```

实际代码应把“没有更多数据”和“队列暂时已满”区分开来。`false` 表示本次没有发送成功，可能是未连接会话、会话没有录音器、录音器尚未启动或内部队列已满。队列满时不要忙等，应等待下一次 `readyToSendAudioBuffer()`。

发送空的 `QAudioBuffer` 表示输入流结束。若 `QMediaRecorder::autoStop` 为 `true`，且所有输入都报告结束，录音器可以自动停止。

## 格式和生命周期

构造函数可以带一个 `QAudioFormat`。有效格式会作为录音器初始化匹配音频编码器的提示；如果没有指定格式或格式无效，编码器会在第一个音频缓冲发送时根据其格式初始化。

如果应用预先知道所有缓冲格式，建议在构造时提供有效格式。这样编码器可以更早确定配置，也能更早暴露不兼容问题。发送的缓冲应保持与这个格式一致，不要在录音中途无提示地切换采样率、声道数或采样格式。

对象应在录音停止、待发送数据排空或输入流结束后再销毁。信号槽默认遵守 QObject 线程归属；生成数据的线程若不同，应通过合适的跨线程信号连接或事件投递进入输入对象所属线程。

## 逐项 API 说明

### `explicit QAudioBufferInput(QObject *parent = nullptr)`

创建未预先指定格式的输入对象。录音器会在发送第一个有效音频缓冲时确定编码器所需格式。

适合运行时才知道音频格式的生成器，但第一个缓冲必须及时且格式有效。

### `explicit QAudioBufferInput(const QAudioFormat &format, QObject *parent = nullptr)`

创建带格式提示的输入对象。有效格式会用于初始化匹配的音频编码器；无效格式表示延迟到第一个输入缓冲再决定。

这个格式是输入对象构造时指定的格式，不是一个会随着每个缓冲自动更新的属性。

### `~QAudioBufferInput() override noexcept`

销毁输入对象。销毁前应解除它与捕获会话的使用关系，并确保录音管线不会再向它发送或等待它发送数据。

### `QMediaCaptureSession *captureSession() const`

返回当前连接的捕获会话；未连接时返回 `nullptr`。连接由 `QMediaCaptureSession::setAudioBufferInput()` 完成。

返回的是非拥有指针，不能据此延长会话生命周期。

### `QAudioFormat format() const`

返回构造时指定的音频格式。如果使用无参构造或传入无效格式，返回值可能是无效格式；这不表示之后发送的第一个缓冲一定无效，而是表示没有预先提供格式提示。

### `bool sendAudioBuffer(const QAudioBuffer &audioBuffer)`

尝试把音频缓冲送入捕获会话中的 `QMediaRecorder`，成功接收时返回 `true`。

返回 `false` 的常见原因：

- 输入尚未连接到 `QMediaCaptureSession`；
- 会话没有设置 `QMediaRecorder`；
- 录音器尚未启动；
- 录音器的输入队列已满。

队列满并不要求丢弃数据；应保留待发送数据，等下一次 `readyToSendAudioBuffer()`。发送空缓冲表示输入结束，不要把它当作普通的零长度音频块。

### `[signal] void readyToSendAudioBuffer()`

通知应用输入端可以接受新的音频缓冲。收到信号后，可调用 `sendAudioBuffer()` 一次或循环调用直到返回 `false`。

该信号是背压协议的一部分，不是“录音已经写入文件”的确认。不要在信号处理器里无限生成数据，也不要忽略 `sendAudioBuffer()` 的返回值。

## 常见误区

- 忘记该类只支持 FFmpeg backend，换平台后直接假定可用。
- 把 `sendAudioBuffer()` 当作永远成功的队列追加接口。
- 在录音器未 `record()` 时发送，并把 `false` 误判成格式错误。
- 没有连接 `QMediaCaptureSession` 就发送。
- 把 `readyToSendAudioBuffer()` 当作“每次只允许发送一个 buffer”；实际可发送到 `false`。
- 发送空缓冲后还继续发送普通数据。
- 在录音过程中改变缓冲格式，却没有重新建立编码配置。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `explicit QAudioBufferInput(QObject *parent = nullptr)` | 创建未指定格式的自定义音频输入。 | 编码器在第一个输入缓冲时确定格式。 |
| 构造 | `explicit QAudioBufferInput(const QAudioFormat &, QObject *parent = nullptr)` | 创建带格式提示的输入。 | 有效格式帮助编码器提前初始化。 |
| 析构 | `~QAudioBufferInput()` | 销毁输入对象。 | 停止录音并解除管线使用后再销毁。 |
| 查询 | `QMediaCaptureSession *captureSession() const` | 返回连接的捕获会话。 | 未连接返回 `nullptr`；不转移所有权。 |
| 查询 | `QAudioFormat format() const` | 返回构造时指定的格式。 | 不是随输入缓冲自动更新的检测结果。 |
| 发送 | `bool sendAudioBuffer(const QAudioBuffer &)` | 尝试向录制器发送一块音频。 | `false` 可能是队列满或管线未启动。 |
| 流结束 | `sendAudioBuffer(QAudioBuffer{})` | 报告自定义输入流结束。 | `autoStop` 条件满足时录音器可自动停止。 |
| 信号 | `void readyToSendAudioBuffer()` | 通知可以继续发送。 | 发送到返回 `false`，再等待下一次信号。 |

---

### 一句话总结

`QAudioBufferInput` 是连接自定义 PCM 生成器与 `QMediaRecorder` 的背压输入端：先接入捕获会话并启动录音，再按 `readyToSendAudioBuffer()` 推送，空缓冲用于结束输入流。
