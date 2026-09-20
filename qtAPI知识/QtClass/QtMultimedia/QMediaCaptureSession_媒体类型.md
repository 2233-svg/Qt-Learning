# QMediaCaptureSession：把媒体源、预览、录制和音频输出接成一条管线

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMediaCaptureSession>`  
> 所属模块：`Qt6::Multimedia`  
> 继承：`QObject`

## 它解决什么问题

`QMediaCaptureSession` 是 Qt Multimedia 采集架构中的连接枢纽。它把媒体输入源与输出功能组合到同一个会话中，让应用可以用统一的方式组织：

- 摄像头、屏幕、窗口或自定义视频帧作为视频输入；
- 麦克风或自定义音频缓冲作为音频输入；
- `QVideoWidget`、`QGraphicsVideoItem` 或 `QVideoSink` 接收视频；
- `QAudioOutput` 播放监听音频；
- `QImageCapture` 拍照；
- `QMediaRecorder` 录制音视频。

它不负责枚举设备、不负责产生摄像头帧，也不等同于“正在录制”的状态对象。它维护的是对象之间的路由关系：

```text
视频源: QCamera / QScreenCapture / QWindowCapture / QVideoFrameInput
                                      |
                                      v
                             QMediaCaptureSession
                              /      |       \
                       视频输出   拍照      录制
                     QVideoSink QImageCapture QMediaRecorder

音频源: QAudioInput / QAudioBufferInput ----> session ----> QAudioOutput
```

## 真实使用场景

- 相机预览、拍照和录像共用一个摄像头会话；
- 录屏工具把屏幕或窗口送到视频预览和文件录制；
- 视频会议把摄像头送给界面，把麦克风送给录制或网络层；
- 测试程序用 `QVideoFrameInput` 注入合成帧，复用同一套预览/录制管线；
- 播放或采集时把音频路由到扬声器，同时保留录音输入。

## 基本组装

```cpp
auto *session = new QMediaCaptureSession(this);
auto *camera = new QCamera(QMediaDevices::defaultVideoInput(), this);
auto *imageCapture = new QImageCapture(this);
auto *recorder = new QMediaRecorder(this);
auto *sink = new QVideoSink(this);

session->setCamera(camera);
session->setImageCapture(imageCapture);
session->setRecorder(recorder);
session->setVideoSink(sink);

camera->start();
```

音频链路可以单独接入：

```cpp
auto *audioInput = new QAudioInput(
        QMediaDevices::defaultAudioInput(), this);
auto *audioOutput = new QAudioOutput(
        QMediaDevices::defaultAudioOutput(), this);

session->setAudioInput(audioInput);
session->setAudioOutput(audioOutput);
```

设置对象本身通常不会自动开始摄像头、屏幕采集或录制。采集源是否需要显式 `start()`，由具体源类决定；录制则由 `QMediaRecorder::record()` 控制。

## 生命周期和所有权

`QMediaCaptureSession` 是 `QObject`，但它对通过 setter 接入的 `QCamera`、`QAudioInput`、`QAudioOutput`、`QImageCapture`、`QMediaRecorder`、`QScreenCapture`、`QWindowCapture`、`QVideoFrameInput`、`QVideoSink` 和视频输出对象不拥有所有权。调用 setter 只是建立或替换连接关系。

因此，应用必须保证这些对象在使用期间一直存活，并且与 session 处于可兼容的线程归属。最简单的做法是给所有对象设置同一个控制器父对象。清理时可先解除 session 连接，再销毁外部对象；如果直接销毁对象，Qt 的对象销毁通知通常会让 session 清理关联，但业务不应依赖悬空指针继续可用。

同一种输入槽位通常只应设置一个有效来源。例如在同一个 session 中同时设置 `camera` 和 `screenCapture`，哪个输入最终生效取决于后端和当前架构，不应把它当成稳定的混合视频功能。切换来源时应显式把旧源设为 `nullptr` 或替换为新源，并监听对应变化。

## 视频输入

### `setCamera()`

把 `QCamera` 作为视频输入。`QCamera` 的设备、格式、镜像和运行状态由相机对象自身管理。session 只负责把相机产生的视频路由给输出、拍照和录制对象。

### `setScreenCapture()` 与 `setWindowCapture()`

分别把屏幕或窗口采集对象作为视频输入。屏幕/窗口采集的权限、目标有效性、启动停止和错误由对应对象负责。设置到 session 后仍需按源类的 API 启动采集。

### `setVideoFrameInput()`

把应用主动提交的 `QVideoFrame` 作为视频输入。它适合测试、视频处理结果回灌和自定义帧源。帧的格式、时间戳、生命周期和提交节奏由应用负责；session 不会替应用生成或校正不合法帧。

使用 `QVideoFrameInput` 时，输入帧应符合下游后端和 `QVideoFrameFormat` 的要求。若后端无法处理某种像素格式或时间戳，可能出现丢帧、录制失败或输出不更新。

## 视频输出

### `setVideoOutput(QObject *)`

把一个支持 Qt Multimedia 视频输出接口的对象接入会话。常见对象包括 `QVideoWidget`、`QGraphicsVideoItem` 等。参数类型是 `QObject *`，因为这些输出类通过对象接口与 Multimedia 后端协作；传入普通但不兼容的 `QObject` 不会自动变成视频输出。

### `setVideoSink(QVideoSink *)`

把视频送到 `QVideoSink`，适合自定义渲染、帧分析、截图或把帧交给其他处理代码。`QVideoSink` 接收视频帧并通过自己的信号通知，session 不负责读取或保存帧。

`setVideoSink()` 和 `setVideoOutput()` 都表达视频输出关系。应用应根据使用的输出类型选择一种清晰的接法，不要把同一个 sink 和 widget 的行为当作自动复制到两个独立消费者；具体后端是否支持多个输出要以平台实现和实际测试为准。

## 音频输入和输出

### `setAudioInput()`

把物理或系统音频输入设备包装成的 `QAudioInput` 接入会话，通常用于麦克风采集。设备、音量和静音属性由 `QAudioInput` 管理；session 只把音频接入录制或其他支持的处理链。

### `setAudioBufferInput()`

Qt 6.8 起，把应用提供的 `QAudioBuffer` 作为音频输入。它适合合成音频、解码后回灌、测试和自定义采集源。音频格式、缓冲时间顺序和提交节奏必须由应用维护。它与 `QAudioInput` 是不同的输入来源，不是给物理麦克风额外加一条音轨的通用混音器。

### `setAudioOutput()`

把音频路由到 `QAudioOutput` 进行监听播放。`QAudioOutput` 选择输出设备并设置音量、静音等属性。将音频输出接入 session 不等于所有输入都一定能被同时监听，是否存在回声消除、混音和后端限制由具体媒体管线决定。

## 拍照和录制

### `setImageCapture()`

接入 `QImageCapture`，让当前视频输入支持一次性拍照。拍照请求和结果信号由 `QImageCapture` 管理；session 不提供拍照槽，也不替 capture 保存图像。

### `setRecorder()`

接入 `QMediaRecorder`，让当前媒体源可以录制。录制格式、输出位置、质量和状态由 recorder 管理；开始、暂停、停止也必须调用 recorder 的 API。session 只是提供媒体输入和输出关系。

如果 session 中没有兼容的视频或音频源，recorder 可能无法开始或只录制其中一种媒体。应用应在调用 `record()` 前核对当前源、格式和权限，并监听 `QMediaRecorder` 的错误和状态信号。

## 属性变化信号

每一个 setter 都有对应的 `...Changed()` 信号。信号只表示 session 中保存的关联对象发生了变化，不表示新对象已经启动、已经有帧到达或录制已经成功。

把对象设置为同一个指针时，是否发出变化信号应以 Qt 对象实际属性变更为准，业务不要依赖“每次 setter 都发信号”。切换对象后，应该从 getter 重新读取当前值，而不是只在槽中保存旧指针。

## 平台、线程和异步行为

媒体源的启动、设备权限、协商、格式转换和帧分发通常是异步的。设置关系完成后，预览可能仍需要等待后端初始化；不要在 setter 返回后立即假设已经有可读帧。

session 和接入的媒体对象都属于创建它们的线程。通常应在主线程创建并使用整个媒体管线，保持事件循环运行。不要从工作线程直接调用 `setCamera()`、`setVideoSink()` 或其他 setter 来“加速”媒体处理；重型帧处理应在收到帧后复制数据并转交工作线程。

后端可能限制同时使用的源、输出数量、格式组合和录制能力。Qt API 负责表达连接关系，但不能保证每个平台都支持任意拓扑。应用应监听源对象、recorder、capture 和 sink 的状态/错误信号，并在切换设备或权限变化时重新建立管线。

## 常见误区

- 认为 session 拥有通过 setter 传入的对象，导致对象被过早销毁或重复管理。
- 调用 `setCamera()` 就认为相机已经启动；启动由 `QCamera::start()` 控制。
- 把 session 当作录制控制器；开始/暂停/停止由 `QMediaRecorder` 完成。
- 把 `setVideoOutput()` 的任意 `QObject` 都当作有效视频输出。
- 同时设置摄像头和屏幕采集，却期待自动混合两路视频。
- 设置 `QVideoFrameInput` 后提交不符合格式或时间戳要求的帧。
- 以为 `setAudioOutput()` 会自动解决混音、回声消除和监听延迟。
- 只处理属性变化信号，不处理各媒体对象自己的异步错误。
- 在没有事件循环的线程中创建媒体对象并等待同步结果。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QMediaCaptureSession(QObject *parent = nullptr)` | 创建媒体路由会话。 | 不自动创建或拥有任何输入输出。 |
| 音频输入 | `QAudioInput *audioInput() const` | 返回当前物理/系统音频输入对象。 | 可能为空；session 不拥有对象。 |
| 音频输入 | `void setAudioInput(QAudioInput *input)` | 设置音频输入源。 | 不自动启动输入；替换时监听 `audioInputChanged`。 |
| 音频输入 | `QAudioBufferInput *audioBufferInput() const` | 返回当前自定义音频缓冲输入。 | Qt 6.8 起；可能为空。 |
| 音频输入 | `void setAudioBufferInput(QAudioBufferInput *input)` | 设置应用提供的音频缓冲源。 | 不与物理输入自动混音；格式和节奏由应用负责。 |
| 音频输出 | `QAudioOutput *audioOutput() const` | 返回当前音频输出对象。 | 可能为空；不代表已经有声音播放。 |
| 音频输出 | `void setAudioOutput(QAudioOutput *output)` | 设置监听播放的音频输出。 | 设备、音量和静音由 `QAudioOutput` 管理。 |
| 视频输入 | `QCamera *camera() const` | 返回当前摄像头输入。 | 可能为空；相机启动状态由 `QCamera` 管理。 |
| 视频输入 | `void setCamera(QCamera *camera)` | 设置摄像头为视频源。 | 不自动启动；通常只保留一个主视频源。 |
| 视频输入 | `QScreenCapture *screenCapture()` | 返回当前屏幕采集源。 | 可能为空；采集权限和启动由源对象管理。 |
| 视频输入 | `void setScreenCapture(QScreenCapture *screenCapture)` | 设置屏幕采集源。 | 不自动开始屏幕采集。 |
| 视频输入 | `QWindowCapture *windowCapture()` | 返回当前窗口采集源。 | 目标有效性由 `QWindowCapture` 管理。 |
| 视频输入 | `void setWindowCapture(QWindowCapture *windowCapture)` | 设置窗口采集源。 | 不自动开始采集；窗口关闭后需处理错误或失效。 |
| 视频输入 | `QVideoFrameInput *videoFrameInput() const` | 返回当前自定义视频帧输入。 | Qt 6.8 起；应用负责帧格式和生命周期。 |
| 视频输入 | `void setVideoFrameInput(QVideoFrameInput *input)` | 设置应用提交的帧为视频源。 | 不会自动生成帧或修复不合法帧。 |
| 拍照 | `QImageCapture *imageCapture()` | 返回当前拍照对象。 | 具体请求和结果由 `QImageCapture` 管理。 |
| 拍照 | `void setImageCapture(QImageCapture *imageCapture)` | 接入拍照对象。 | 不拥有对象；需有兼容视频源。 |
| 录制 | `QMediaRecorder *recorder()` | 返回当前录制对象。 | 录制状态由 recorder 管理。 |
| 录制 | `void setRecorder(QMediaRecorder *recorder)` | 接入录制对象。 | 不自动开始录制；录制配置由 recorder 管理。 |
| 视频输出 | `QObject *videoOutput() const` | 返回通用视频输出对象。 | 可能为空；返回类型不能证明对象支持视频输出。 |
| 视频输出 | `void setVideoOutput(QObject *output)` | 设置 widget 等通用视频输出。 | 传入对象必须实现兼容的媒体输出接口。 |
| 视频输出 | `QVideoSink *videoSink() const` | 返回当前帧接收器。 | 可能为空；帧处理由 sink/应用完成。 |
| 视频输出 | `void setVideoSink(QVideoSink *sink)` | 设置 `QVideoSink` 接收视频帧。 | 遵守 sink 所属线程和帧生命周期。 |
| 平台 | `QPlatformMediaCaptureSession *platformSession() const` | 返回底层平台会话接口。 | 面向 Qt 平台实现，不是普通应用层 API；不要依赖内部实现细节。 |
| 通知 | `void audioInputChanged()` | 音频输入关联变化时通知。 | 不代表输入已启动或权限已授予。 |
| 通知 | `void audioBufferInputChanged()` | 音频缓冲输入关联变化时通知。 | Qt 6.8 起；不代表缓冲已经提交。 |
| 通知 | `void audioOutputChanged()` | 音频输出关联变化时通知。 | 不代表已经有音频播放。 |
| 通知 | `void cameraChanged()` | 摄像头关联变化时通知。 | 不代表相机已经运行。 |
| 通知 | `void screenCaptureChanged()` | 屏幕采集关联变化时通知。 | 不代表已开始采集。 |
| 通知 | `void windowCaptureChanged()` | 窗口采集关联变化时通知。 | 不代表目标窗口仍然有效。 |
| 通知 | `void videoFrameInputChanged()` | 自定义视频帧输入关联变化时通知。 | Qt 6.8 起；不代表已经有帧。 |
| 通知 | `void imageCaptureChanged()` | 拍照对象关联变化时通知。 | 不代表当前会话可以拍照。 |
| 通知 | `void recorderChanged()` | 录制对象关联变化时通知。 | 不代表已经开始录制。 |
| 通知 | `void videoOutputChanged()` | 通用视频输出关联变化时通知。 | 不代表已有视频帧到达。 |

## 一句话总结

`QMediaCaptureSession` 只负责把媒体对象接成可协作的路由关系：输入源、预览、拍照、录制和音频监听各自负责自己的状态与错误，session 负责让它们处在同一条媒体管线中。
