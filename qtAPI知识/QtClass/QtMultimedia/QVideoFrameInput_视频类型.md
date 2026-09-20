# QVideoFrameInput：把自定义视频帧送入媒体会话

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QVideoFrameInput>`  
> 所属模块：`Qt6::Multimedia`  
> 继承：`QObject`  
> 引入版本：Qt 6.8

## 它解决什么问题

`QVideoFrameInput` 把应用自己生成或处理的视频帧接入 Qt Multimedia 管线。它可以把这些帧送给：

- `QMediaRecorder`，编码并保存为媒体文件；
- 通过 `QMediaCaptureSession` 连接的视频输出；
- 同一个会话中的其它媒体组件。

它适合自定义渲染、屏幕内容合成、游戏画面、算法处理后的帧和离线视频生成。它不是摄像头采集器，也不负责生成帧；应用必须自己创建 `QVideoFrame` 并按后端允许的节奏发送。

当前 Qt 6.11.1 文档明确说明：`QVideoFrameInput` 只有 FFmpeg 后端支持。

## 实际使用场景与基本连接方式

```cpp
QMediaCaptureSession session;
QMediaRecorder recorder;
QVideoFrameInput videoInput;

session.setRecorder(&recorder);
session.setVideoFrameInput(&videoInput);

recorder.setOutputLocation(QUrl::fromLocalFile("capture.mp4"));
recorder.record();
```

实际发送时，应用通常监听 `readyToSendVideoFrame()`：

```cpp
connect(&videoInput, &QVideoFrameInput::readyToSendVideoFrame,
        this, [this, &videoInput] {
    while (hasFrames()) {
        QVideoFrame frame = nextFrame();
        if (!videoInput.sendVideoFrame(frame))
            break;
    }
});
```

## readyToSendVideoFrame：背压信号

这个信号表示目标现在可以接受新帧。收到信号后，可以调用一次 `sendVideoFrame()`，也可以循环发送，直到：

- 没有更多帧；
- `sendVideoFrame()` 返回 `false`。

这是一种 pull/back-pressure 模型：编码器和输出端通过信号告诉输入端何时有容量。相比无条件高速发送，它可以避免应用持续把帧塞进一个无法及时编码的队列。

如果输入帧生成速度长期高于编码速度，仍可能需要应用自己建立有限大小的队列。队列过大有内存压力，队列过小会丢帧；是否丢帧应由业务明确决定。

不要把 `readyToSendVideoFrame()` 当成“上一帧已经写入文件”的通知。它只表示目标可以再接收帧，编码和封装可能仍在异步进行。

## sendVideoFrame() 的返回值

`sendVideoFrame(frame)` 返回 `true`，表示这一帧已经成功送到目标；返回 `false` 表示这一帧没有被接受。

失败可能发生在：

- 输入对象没有连接到 `QMediaCaptureSession`；
- 会话没有视频输出或录制器；
- 录制器尚未开始录制；
- 目标内部帧队列已满；
- 当前后端不能处理该输入。

返回 `false` 不是“稍后自动重试”的承诺。应用应停止当前发送循环，等待下一次 `readyToSendVideoFrame()`，而不是在同一个调用栈中忙等。

## 发送结束标记

向 `sendVideoFrame()` 发送空的 `QVideoFrame`，表示视频输入流结束：

```cpp
videoInput.sendVideoFrame(QVideoFrame());
```

当 `QMediaRecorder::autoStop` 为 `true` 且所有输入都报告了流结束，录制器可以自动停止。若同时存在音频输入，不能只结束视频输入后就假设整个录制已经完成。

空帧是协议上的结束标记，不是一个可显示或可编码的视频帧。业务代码应避免把无效帧误当成普通数据发送。

## 构造时指定格式

可以用 `QVideoFrameFormat` 构造输入对象：

```cpp
QVideoFrameFormat format(QSize(1920, 1080),
                         QVideoFrameFormat::Format_NV12);
format.setStreamFrameRate(30.0);

QVideoFrameInput videoInput(format);
```

这个格式会作为编码器初始化时的提示。如果构造时没有指定有效格式，编码器可能等到第一帧到达后才初始化。

已知将要发送的帧格式时，建议提前指定。编码器初始化后，如果后续帧频繁改变尺寸或像素格式，可能产生转换和重新配置开销，具体行为依赖后端。

`format()` 返回构造时指定的格式。这个类没有公开的格式 setter，因此它不是运行时动态格式协商接口。

## 帧的所有权和生命周期

`sendVideoFrame()` 参数是 `const QVideoFrame &`，调用方仍应把帧当作值传递给后端。不要在发送后立即修改底层共享资源，也不要依赖局部对象销毁后后端一定不会再访问其资源。

`QVideoFrame` 可能引用 GPU 纹理、系统内存或其它昂贵资源。帧生成器应控制缓存数量，并在不需要时及时释放自己的副本。

## 生命周期、所有权和线程

`QVideoFrameInput` 是不可复制的 `QObject`。通常由父对象管理生命周期，也可以作为控制器成员使用。把它连接到 `QMediaCaptureSession` 不应被理解为会话接管了它的生命周期；输入对象必须在会话使用期间保持有效。

输入对象、会话和录制器通常应在同一个线程中创建和操作。`readyToSendVideoFrame()` 通过 Qt 事件循环发出，阻塞所属线程会阻止背压通知和录制状态推进。

如果视频帧生成在工作线程，建议在线程间传递帧值或自定义的有限队列，再在输入对象所属线程调用 `sendVideoFrame()`。不要直接跨线程操作同一个 `QVideoFrameInput`。

## 与摄像头输入的区别

摄像头由 `QCamera` 自动产生视频帧，应用主要消费或显示它们；`QVideoFrameInput` 则要求应用负责产生每一帧。

因此它适合：

- 已经有渲染结果的应用；
- 将多路画面合成一路视频；
- 对帧做算法处理后再录制；
- 生成测试视频或离线动画。

如果只是录制摄像头或屏幕，不需要手动创建帧，应优先使用 `QCamera`、`QScreenCapture` 或 `QWindowCapture`。

## 常见误区

- 未连接会话或未开始录制就把 `false` 当作编码错误；
- 忽略 `readyToSendVideoFrame()`，持续高速调用导致队列满；
- 把 `readyToSendVideoFrame()` 当成写盘完成通知；
- 把空 `QVideoFrame` 当作普通视频帧；
- 只结束视频输入，却忘记音频输入也必须结束；
- 发送的帧尺寸和像素格式不断变化，却期待没有转换开销；
- 以为构造时的格式会自动转换所有后续不匹配的帧；
- 在工作线程直接调用属于另一个线程的输入对象。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `explicit QVideoFrameInput(QObject *parent = nullptr)` | 创建未指定格式的输入对象。 | 编码器可能等第一帧到达后才初始化。 |
| 构造 | `explicit QVideoFrameInput(const QVideoFrameFormat &format, QObject *parent = nullptr)` | 创建带格式提示的输入对象。 | 已知帧格式时优先使用；格式只是初始化提示。 |
| 析构 | `~QVideoFrameInput() override` | 销毁输入对象。 | 销毁前应停止依赖它的媒体流程。 |
| 发送 | `bool sendVideoFrame(const QVideoFrame &frame)` | 向会话中的录制器或视频输出发送一帧。 | `false` 表示当前没有接受；队列满时应等待 ready 信号。 |
| 查询 | `QVideoFrameFormat format() const` | 返回构造时指定的格式。 | 没有 setter；不表示每一帧都一定符合该格式。 |
| 查询 | `QMediaCaptureSession *captureSession() const` | 返回当前连接的媒体会话。 | 未连接时返回 `nullptr`；指针不表示输入拥有会话。 |
| 信号 | `void readyToSendVideoFrame()` | 通知目标可以接受新帧。 | 可发送一帧或循环发送到 `false`；这是背压信号。 |

## 一句话总结

`QVideoFrameInput` 是自定义视频帧进入 Qt Multimedia 的入口：先接入 `QMediaCaptureSession`，再响应 `readyToSendVideoFrame()` 发送，`false` 代表当前背压，空帧代表输入结束。
