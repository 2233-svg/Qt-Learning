# QScreenCapture：把整个屏幕作为 Qt Multimedia 视频源

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QScreenCapture>`  
> 所属模块：`Qt6::Multimedia`  
> 继承：`QObject`  
> 类型性质：屏幕采集源

## 它解决什么问题

`QScreenCapture` 把一个 `QScreen` 的画面转换成 Qt Multimedia 视频输入。它只负责“从哪块屏幕采集”，不负责预览窗口、文件编码或音频录制。采集到的帧要通过 `QMediaCaptureSession` 路由给 `QVideoSink`、视频 widget 或 `QMediaRecorder`。

典型管线是：

```text
QScreen
   |
   v
QScreenCapture -- setScreen()/setActive() -->
QMediaCaptureSession
   |                         |
   v                         v
QVideoSink / VideoOutput    QMediaRecorder
```

## 实际使用场景

- 录制桌面教学视频或产品演示；
- 录屏工具把桌面显示到预览窗口；
- 远程协助或监控程序采集某个显示器；
- 将屏幕帧送入自定义分析、截图或编码管线；
- 与 `QAudioInput` 组合录制“桌面画面 + 麦克风”。

它不是窗口采集器。如果只希望录制一个应用窗口，应使用 `QWindowCapture`，否则会把同一屏幕上的其它窗口、面板和通知一起采集。

## 最小连接示例

```cpp
#include <QMediaCaptureSession>
#include <QMediaRecorder>
#include <QScreenCapture>

auto *session = new QMediaCaptureSession(this);
auto *capture = new QScreenCapture(this);
auto *recorder = new QMediaRecorder(this);

session->setScreenCapture(capture);
session->setRecorder(recorder);

capture->setScreen(QGuiApplication::primaryScreen());
recorder->setOutputLocation(
        QUrl::fromLocalFile("desktop.mp4"));

connect(capture, &QScreenCapture::errorOccurred,
        this, [](QScreenCapture::Error error,
                 const QString &message) {
    qWarning() << error << message;
});

capture->start();
recorder->record();
```

设置到 session 只是建立媒体路由，不等于已经开始采集。`start()` 或 `setActive(true)` 才会请求后端启动采集；录制是否开始还由 `QMediaRecorder::record()` 决定。

## screen 的语义

`screen` 是目标 `QScreen *`。它是 Qt GUI 对象的非拥有指针，`QScreenCapture` 不会销毁屏幕。

当 `screen` 为 `nullptr` 时，Qt 会在采集对象被激活时选择 `QGuiApplication::primaryScreen()`。因此，下面两种写法在常见桌面环境中通常等价：

```cpp
capture->setScreen(QGuiApplication::primaryScreen());
capture->start();
```

```cpp
capture->setScreen(nullptr);
capture->start(); // 激活时选择 primary screen
```

但第二种写法不是“永远跟随主屏幕”。如果主屏幕后来变化，应用仍应根据 `screenChanged`、屏幕插拔通知和业务需要重新设置目标。

屏幕对象可能在显示器断开后失效或被替换。开始采集前应检查指针，并处理采集错误；不要把启动时拿到的 `QScreen *` 当成长期稳定的硬件 ID。

## active、start 和 stop

`active` 表示采集是否处于活动状态。`start()` 等价于 `setActive(true)`，`stop()` 等价于 `setActive(false)`。

启动是异步资源操作：

- `start()` 返回时不保证已经收到第一帧；
- 后端可能还在申请权限、创建捕获对象或协商像素格式；
- 应通过 `activeChanged`、输出对象的帧信号和 `errorOccurred` 判断实际进展；
- 重复设置相同状态不应被当作重新初始化请求。

停止采集后，session 仍可保留这个对象和视频路由关系；再次 `start()` 可以复用同一对象。若要切换到窗口采集，应显式调整 session 的视频输入，避免同时依赖两个源的后端选择。

## 错误处理

`error()` 保存最近一次错误，`errorString()` 提供可显示的文字说明。`errorOccurred()` 在错误发生时同时给出枚举和说明。

| 错误 | 含义 |
| --- | --- |
| `NoError` | 没有错误。 |
| `InternalError` | 底层屏幕采集驱动或实现发生内部错误。 |
| `CapturingNotSupported` | 当前平台或后端不支持屏幕采集。 |
| `CaptureFailed` | 已请求采集，但实际抓取失败。 |
| `NotFound` | 目标屏幕不存在或已经失效。 |

错误枚举适合做程序分支，`errorString()` 适合日志和界面提示。错误发生后不要只清空提示就继续使用旧的目标屏幕，先重新检查屏幕列表和权限。

## 平台边界

### FFmpeg 后端

Qt 6.11.1 文档明确将 `QScreenCapture` 限定为 FFmpeg 后端能力。其它后端即使类可以构造，激活时也可能报告 `CapturingNotSupported`。

### Wayland

Wayland 协议不允许应用通过 `QScreenCapture` API 可靠地设置和读取目标屏幕。调用 `setActive(true)` 时，系统可能弹出 XDG Desktop Portal 的屏幕选择器，由用户完成授权和选择。

该路径通常还要求：

- 已安装并启用 ScreenCast  portal；
- 使用 PipeWire 0.3 或兼容实现；
- 应用准备好面对“用户取消选择”或选择结果与 `screen()` 不完全对应的情况。

因此，在 Wayland 上不要把 `screen()` 当成可靠的用户最终选择结果，也不要假定 `setScreen()` 一定能控制系统选择器。

### Android

Android 屏幕捕获需要 MediaProjection 相关的前台服务权限，并在应用清单中配置 Qt 的屏幕捕获服务。仅调用 C++ API 不足以完成系统授权。权限或服务配置缺失时，应通过错误信号诊断，而不是反复调用 `start()`。

### EGLFS 和性能

EGLFS 上功能受限；Qt Quick 场景可能通过 `QQuickWindow::grabWindow()` 实现，存在额外的抓屏和拷贝成本。

多数平台的采集帧率接近屏幕刷新率。75 Hz、120 Hz 或 4K 屏幕会显著增加 CPU、GPU、内存带宽和编码压力。EGLFS 当前约束为 30 FPS。录制器编码跟不上时可能丢帧，因此应结合实际设备测试分辨率、刷新率和编码器组合。

## 线程和生命周期

`QScreenCapture` 是不可复制的 `QObject`，通常与 `QMediaCaptureSession` 在同一控制线程创建和使用。它不拥有 session，也不拥有目标 `QScreen`。

不要在工作线程直接操作 GUI 屏幕对象或媒体 QObject。帧分析应在收到 `QVideoSink::videoFrameChanged()` 后复制必要数据，再将轻量数据交给工作线程；不要把整个采集对象跨线程搬运来规避性能问题。

## 常见误区

- 把 `QScreenCapture` 当成录制器；它只产生视频输入。
- 设置 `screen` 后以为已经开始采集；还必须激活对象。
- 把 `start()` 返回当成“第一帧已经到达”。
- 在 Wayland 上假定 `setScreen()` 一定有效。
- 忽略 Android 的 MediaProjection 前台服务配置。
- 以为 `screen == nullptr` 会永久跟随主屏幕变化。
- 在高刷 4K 屏幕上按普通摄像头的性能估算 CPU 和编码压力。
- 只读取 `error()`，却不记录 `errorString()` 的具体原因。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `enum Error` | 描述屏幕采集错误。 | 具体原因还要结合 `errorString()`。 |
| 枚举值 | `NoError = 0` | 表示没有错误。 | 不代表当前一定已经有视频帧。 |
| 枚举值 | `InternalError = 1` | 表示底层采集驱动内部错误。 | 记录日志并考虑重建采集管线。 |
| 枚举值 | `CapturingNotSupported = 2` | 表示当前平台或后端不支持。 | Qt 6.11.1 主要要求 FFmpeg 后端。 |
| 枚举值 | `CaptureFailed = 4` | 表示抓取过程失败。 | 检查权限、目标屏幕和后端状态。 |
| 枚举值 | `NotFound = 5` | 表示目标屏幕不存在。 | 显示器断开后需要重新选择。 |
| 构造 | `QScreenCapture(QObject *parent = nullptr)` | 创建屏幕采集对象。 | 不自动连接 session，也不自动启动。 |
| 析构 | `~QScreenCapture() override` | 销毁屏幕采集对象。 | 销毁前应停止或解除 session 关联。 |
| 连接 | `QMediaCaptureSession *captureSession() const` | 返回当前连接的媒体采集会话。 | 可能为空；不转移所有权。 |
| 目标 | `void setScreen(QScreen *screen)` | 设置要采集的屏幕。 | 不拥有 `QScreen`；`nullptr` 在激活时选择主屏幕。 |
| 目标 | `QScreen *screen() const` | 返回当前目标屏幕。 | Wayland 下不能把它当成可靠选择结果。 |
| 状态 | `bool isActive() const` | 查询采集是否活动。 | 活动不等于第一帧已经到达。 |
| 错误 | `Error error() const` | 返回最近一次错误码。 | 和 `errorString()` 配合使用。 |
| 错误 | `QString errorString() const` | 返回最近一次错误的可读说明。 | 适合日志和界面提示。 |
| 控制 | `void setActive(bool active)` | 开始或停止屏幕采集。 | 操作通常异步完成。 |
| 控制 | `void start()` | 启动采集。 | 等价于 `setActive(true)`。 |
| 控制 | `void stop()` | 停止采集。 | 等价于 `setActive(false)`。 |
| 信号 | `void activeChanged(bool)` | 活动状态变化时通知。 | 不替代帧到达信号或错误信号。 |
| 信号 | `void screenChanged(QScreen *)` | 目标屏幕变化时通知。 | 监听显示器插拔和目标切换。 |
| 信号 | `void errorChanged()` | 最近错误或错误文字变化时通知。 | 重新读取 `error()` 和 `errorString()`。 |
| 信号 | `void errorOccurred(Error, const QString &)` | 采集发生错误时通知。 | 适合集中处理启动失败和运行中失败。 |

## 一句话总结

`QScreenCapture` 是“屏幕到 Multimedia 管线”的输入端：它负责选择和启动屏幕采集，真正的预览、录制和逐帧处理交给 `QMediaCaptureSession` 及其输出对象，同时必须把平台权限、Wayland 选择器和高分辨率性能当成实现的一部分。
