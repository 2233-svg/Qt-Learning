# QWindowCapture：把指定窗口作为 Qt Multimedia 视频源

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QWindowCapture>`  
> 所属模块：`Qt6::Multimedia`  
> 继承：`QObject`  
> 类型性质：窗口采集源

## 它解决什么问题

`QWindowCapture` 只采集一个窗口，而不是整个屏幕。它把用户选择的 `QCapturableWindow` 送入 `QMediaCaptureSession`，之后可以交给预览、`QVideoSink` 或 `QMediaRecorder`。

它解决的是“录制目标选择和采集状态”问题，不解决：

- 窗口列表界面；
- 视频编码和文件封装；
- 音频采集；
- 采集后的视频绘制；
- 窗口关闭后的业务替代策略。

典型关系如下：

```text
QWindowCapture::capturableWindows()
                |
                v
         QCapturableWindow
                |
                v
          QWindowCapture
                |
                v
       QMediaCaptureSession
          /              \
     QVideoSink       QMediaRecorder
```

## 实际使用场景

- 只录制 IDE、浏览器或演示软件窗口；
- 教程软件把目标应用窗口嵌入预览；
- 自动化测试采集某个测试窗口；
- 远程协助时共享单个应用而不是整个桌面；
- 用户从窗口列表中选择要直播或录制的对象。

如果业务目标是整块显示器，应使用 `QScreenCapture`。窗口采集不一定覆盖窗口的阴影、弹出菜单、系统级浮层或其它不属于窗口本身的内容。

## 枚举窗口并开始采集

```cpp
auto *session = new QMediaCaptureSession(this);
auto *capture = new QWindowCapture(this);
auto *recorder = new QMediaRecorder(this);

session->setWindowCapture(capture);
session->setRecorder(recorder);

const QList<QCapturableWindow> windows =
        QWindowCapture::capturableWindows();

for (const QCapturableWindow &window : windows) {
    if (window.isValid())
        qDebug() << window.description();
}

if (!windows.isEmpty()) {
    capture->setWindow(windows.first());
    capture->start();
}
```

`capturableWindows()` 返回的是一次枚举结果，不是持续更新的模型。窗口打开、关闭、标题变化或平台桌面变化后，应在需要时重新枚举。保存旧的 `QCapturableWindow` 值并不保证它一直有效。

## QCapturableWindow 的边界

`window` 属性是一个显式共享值类型，不是 `QWindow *`。它描述一个可采集目标，默认构造对象无效，也不拥有底层窗口。

```cpp
QCapturableWindow selected = ...;

if (!selected.isValid()) {
    // 目标可能已经关闭或不再允许采集
    return;
}

capture->setWindow(selected);
```

Qt 6.10 起，应用也可以从本进程的顶层 `QWindow *` 构造 `QCapturableWindow`。传入 `nullptr`、非顶层窗口或尚未建立平台资源的窗口，可能得到永远无效或暂时无效的描述。`description()` 适合展示标题，不适合充当稳定的窗口 ID。

窗口关闭、桌面切换和平台权限变化都可能使旧描述失效。因此开始采集前、采集中收到错误后、窗口选择界面重新显示时，都应再次调用 `isValid()` 或重新枚举。

## active、start 和 stop

`active` 表示当前是否请求并维持窗口采集。`start()` 是 `setActive(true)` 的便捷形式，`stop()` 是 `setActive(false)` 的便捷形式。

启动行为是异步的，调用返回不代表：

- 目标窗口仍然存在；
- 后端已经建立采集；
- 第一帧已经到达；
- 录制器已经成功写入文件。

应用应同时监听 `activeChanged`、`errorOccurred` 以及下游输出的状态信号。需要切换目标窗口时，通常先停止当前采集，再设置新的 `QCapturableWindow`，最后重新启动；这样更容易区分旧目标的错误和新目标的初始化过程。

## X11 上的可见区域限制

Qt 文档对 X11 有几项重要限制：

- 窗口部分移出可见屏幕区域时，可能只采集当前可见部分；
- 采集帧尺寸可能因此小于窗口的 `geometry()`；
- 完全位于可见区域之外的窗口可能无法采集，并发出错误；
- 最小化窗口或位于不可见虚拟工作区的行为取决于窗口管理器。

因此，不能用窗口几何尺寸推断每一帧的实际尺寸。下游处理应以 `QVideoFrame` 或视频输出报告的实际尺寸为准。窗口移动、最大化、最小化和跨屏切换时，也要准备处理格式变化或错误。

## 后端支持和权限

Qt 6.11.1 文档明确指出 `QWindowCapture` 只支持 FFmpeg 后端。系统的窗口分享策略、桌面权限和窗口管理器仍可能拒绝采集。

窗口出现在枚举列表中，只说明它被发现，不代表一定可以持续抓取。真正启动时还会受到目标可见性、平台安全策略、窗口状态和后端实现的影响。

## 线程、所有权和重建策略

`QWindowCapture` 是不可复制的 `QObject`。`QMediaCaptureSession` 通过 setter 建立关联，但不应把它理解为自动接管对象生命周期。通常让 session、capture、recorder 和 sink 使用同一个父对象，并在同一线程中运行。

窗口采集失败后，最稳妥的恢复流程通常是：

1. 停止采集并读取 `errorString()`；
2. 重新调用 `capturableWindows()`；
3. 过滤 `isValid()` 的对象；
4. 让用户重新选择或按业务规则选择替代窗口；
5. 设置新窗口并重新启动。

不要只对旧对象反复调用 `start()`，因为旧对象可能已经指向一个平台上不存在的窗口。

## 常见误区

- 把 `QWindowCapture` 当成整个桌面录制器；
- 把 `description()` 当成稳定窗口 ID；
- 只在列表展示时检查 `isValid()`，启动前不再检查；
- 以为 `capturableWindows()` 返回的是自动更新列表；
- 用窗口 `geometry()` 作为每帧实际大小；
- 在 X11 上假定最小化窗口和不可见工作区窗口都能采集；
- 设置窗口后以为录制已经开始；
- 忽略 FFmpeg 后端和操作系统窗口分享权限。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `enum Error` | 描述窗口采集错误。 | 详细原因从 `errorString()` 读取。 |
| 枚举值 | `NoError = 0` | 表示没有错误。 | 不代表窗口当前一定可见或有帧。 |
| 枚举值 | `InternalError = 1` | 表示底层窗口采集驱动错误。 | 记录平台和后端信息。 |
| 枚举值 | `CapturingNotSupported = 2` | 表示窗口采集不受支持。 | Qt 6.11.1 要求 FFmpeg 后端。 |
| 枚举值 | `CaptureFailed = 4` | 表示抓取窗口失败。 | 检查窗口状态和可见区域。 |
| 枚举值 | `NotFound = 5` | 表示目标窗口已找不到。 | 重新枚举窗口列表。 |
| 构造 | `QWindowCapture(QObject *parent = nullptr)` | 创建窗口采集对象。 | 不自动选择窗口或启动采集。 |
| 析构 | `~QWindowCapture() override` | 销毁窗口采集对象。 | 销毁前应停止或解除 session 关联。 |
| 静态枚举 | `static QList<QCapturableWindow> capturableWindows()` | 返回当前可采集窗口列表。 | 是一次快照；窗口变化后需重新枚举。 |
| 连接 | `QMediaCaptureSession *captureSession() const` | 返回当前连接的媒体采集会话。 | 可能为空；不转移所有权。 |
| 目标 | `void setWindow(QCapturableWindow window)` | 设置窗口采集目标。 | 传入无效对象不会自动修复。 |
| 目标 | `QCapturableWindow window() const` | 返回当前窗口描述。 | 返回值可能随后因窗口关闭而失效。 |
| 状态 | `bool isActive() const` | 查询采集是否活动。 | 活动状态不等于采集已成功。 |
| 错误 | `Error error() const` | 返回最近一次错误码。 | 与 `errorString()` 一起读取。 |
| 错误 | `QString errorString() const` | 返回最近一次错误说明。 | 适合日志和用户提示。 |
| 控制 | `void setActive(bool active)` | 开始或停止窗口采集。 | 资源创建通常异步完成。 |
| 控制 | `void start()` | 启动窗口采集。 | 等价于 `setActive(true)`。 |
| 控制 | `void stop()` | 停止窗口采集。 | 等价于 `setActive(false)`。 |
| 信号 | `void activeChanged(bool)` | 采集活动状态变化时通知。 | 还要监听错误和下游帧状态。 |
| 信号 | `void windowChanged(QCapturableWindow)` | 目标窗口描述变化时通知。 | 不表示目标已成功采集。 |
| 信号 | `void errorChanged()` | 最近错误或错误文字变化时通知。 | 重新读取两个错误属性。 |
| 信号 | `void errorOccurred(Error, const QString &)` | 采集发生错误时通知。 | 适合触发重新枚举和恢复流程。 |

## 一句话总结

`QWindowCapture` 是“指定窗口到 Multimedia 管线”的输入端：它用 `QCapturableWindow` 表示目标，用 `active` 控制采集，并要求应用持续面对窗口失效、可见区域、窗口管理器和平台后端差异。
