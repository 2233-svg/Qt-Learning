# QVideoWidget：在 QWidget 界面显示媒体视频

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QVideoWidget>`  
> 所属模块：`Qt6::MultimediaWidgets`  
> 继承：`QWidget`  
> 类型性质：视频显示控件

## 它解决什么问题

`QVideoWidget` 把 `QMediaPlayer` 或 `QCamera` 产生的视频显示到传统 Qt Widgets 界面中。它接收视频帧、按控件大小绘制，并提供宽高比和全屏显示控制。

它是显示端，不负责打开媒体文件、解码视频、启动摄像头或播放音频。这些职责仍属于 `QMediaPlayer`、`QCamera`、`QMediaCaptureSession` 和音频输出对象。

## 实际使用场景

- 播放器窗口中的视频区域。
- 摄像头取景或拍照界面。
- 监控、会议、教学软件的主视频画面。
- 需要放进 `QLayout` 的传统 Widgets 视频输出。

```cpp
auto *player = new QMediaPlayer(this);
auto *video = new QVideoWidget;

layout()->addWidget(video);
player->setVideoOutput(video);
player->setSource(QUrl::fromLocalFile(filePath));

video->show();
player->play();
```

同一个媒体对象一次只能连接一个视频显示输出。再次调用 `setVideoOutput()` 连接另一个 `QVideoWidget`、`QGraphicsVideoItem` 或 `QVideoSink` 时，旧输出会被替换。

## 宽高比与缩放

`aspectRatioMode` 决定视频如何适配控件矩形：

| 模式 | 显示效果 | 代价 |
| --- | --- | --- |
| `Qt::KeepAspectRatio` | 保持原比例完整显示 | 可能出现黑边或空白 |
| `Qt::KeepAspectRatioByExpanding` | 保持比例并填满控件 | 可能裁剪边缘 |
| `Qt::IgnoreAspectRatio` | 拉伸填满控件 | 人物和画面可能变形 |

控件尺寸通常不等于视频原始尺寸。展示监控画面、影片或人像时，通常优先用 `KeepAspectRatio`；需要作为背景填满区域时再评估裁剪模式。

## 全屏语义

`setFullScreen(true)` 让这个视频控件进入全屏显示，`isFullScreen()` 查询当前状态。它改变的是控件的窗口显示方式：

- 不改变视频文件、摄像头分辨率或播放器状态；
- 不等价于“媒体流全屏”；
- 不会自动提供退出全屏的业务交互。

应用应自行连接快捷键、双击或工具栏动作，并监听 `fullScreenChanged()` 同步窗口控制状态。

## `videoSink()`：内部的视频接收器

`videoSink()` 返回控件内部用于呈现帧的 `QVideoSink`。它适合在显示的同时观察 `videoFrameChanged()`、读取帧元数据或为调试提供帧入口。

```cpp
connect(video->videoSink(), &QVideoSink::videoFrameChanged,
        this, [](const QVideoFrame &frame) {
            inspectFrame(frame);
        });
```

这个 sink 受 `QVideoWidget` 生命周期控制。不要在控件销毁后保留并使用其指针；如果目的只是让播放器显示视频，直接把控件传给 `setVideoOutput()` 即可。

## 尺寸提示、平台和线程边界

`sizeHint()` 返回当前视频后端能给出的建议大小，否则回退到 `QWidget` 的默认尺寸提示。布局、父控件约束、最小/最大尺寸仍能改变最终显示区域。

Qt 6.11 文档说明 `QVideoWidget` 不支持 `eglfs` 平台插件。其它平台是否可用、是否使用硬件解码或特定渲染路径，仍应在目标设备上实际验证。

作为 QWidget，它必须在 GUI 线程创建和操作。不要从解码工作线程直接调整控件属性、调用 `show()`，或把 GUI 事件和媒体后台回调混用。

## 逐项 API 说明

### `QVideoWidget(QWidget *parent = nullptr)`

创建视频显示控件。`parent` 按 QWidget 所有权规则管理控件生命周期。

### `QVideoSink *videoSink() const`

取得内部视频接收器。它可被元对象系统调用，也可用于访问当前显示链路的帧通知；返回指针并不把所有权交给调用方。

### `Qt::AspectRatioMode aspectRatioMode() const`

读取当前缩放策略。它只描述视频如何适配控件，不修改视频源或帧像素。

### `void setAspectRatioMode(Qt::AspectRatioMode mode)`

设置缩放策略。切换到裁剪或拉伸模式前，应确认业务是否允许丢失边缘内容或改变画面比例。

### `bool isFullScreen() const` / `void setFullScreen(bool)`

查询或修改控件全屏显示状态。窗口系统可能受平台策略、父子控件关系和当前窗口状态影响。

### `QSize sizeHint() const`

返回布局建议尺寸。它不能保证控件最终会按此尺寸显示。

### `event()`、`showEvent()`、`hideEvent()`、`resizeEvent()`、`moveEvent()`

这些保护函数用于内部呈现和窗口状态同步。子类重写时要保持 QWidget 事件链，通常应在适当时机调用基类实现；隐藏控件不等于停止播放器。

## 常见误区

- 认为控件会自行打开媒体文件或启动摄像头。
- 试图让一个 `QMediaPlayer` 同时显示到多个输出对象。
- 使用 `IgnoreAspectRatio` 后把画面变形当作解码问题。
- 把控件全屏当成视频源或播放器属性。
- 在非 GUI 线程创建、销毁或操作控件。
- 将 `videoSink()` 的返回指针当成由调用者拥有的独立对象。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QVideoWidget(QWidget *parent = nullptr)` | 创建视频显示控件。 | 必须在 GUI 线程使用。 |
| 析构 | `~QVideoWidget()` | 销毁控件。 | 不代替播放器生命周期管理。 |
| 输出 | `QVideoSink *videoSink() const` | 取得内部视频接收器。 | 返回对象受控件生命周期约束。 |
| 属性 | `Qt::AspectRatioMode aspectRatioMode() const` | 查询缩放宽高比策略。 | 决定留白、裁剪或变形。 |
| 属性 | `void setAspectRatioMode(Qt::AspectRatioMode)` | 设置视频适配策略。 | `IgnoreAspectRatio` 可能变形。 |
| 信号 | `aspectRatioModeChanged(Qt::AspectRatioMode)` | 通知宽高比策略改变。 | 可用于同步设置面板。 |
| 属性 | `bool isFullScreen() const` | 查询控件是否全屏。 | 只描述控件显示状态。 |
| 属性 | `void setFullScreen(bool)` | 切换控件全屏显示。 | 需要配合退出逻辑。 |
| 信号 | `fullScreenChanged(bool)` | 通知全屏状态改变。 | 不代表媒体流改变。 |
| 布局 | `QSize sizeHint() const` | 返回建议尺寸。 | 最终尺寸由布局决定。 |
| 事件 | `event(QEvent *)` | 处理控件事件。 | 重写时保持基类事件链。 |
| 事件 | `showEvent(QShowEvent *)` | 响应显示事件。 | 适合处理显示时机。 |
| 事件 | `hideEvent(QHideEvent *)` | 响应隐藏事件。 | 不等于停止播放器。 |
| 事件 | `resizeEvent(QResizeEvent *)` | 响应控件尺寸变化。 | 视频缩放由控件后端处理。 |
| 事件 | `moveEvent(QMoveEvent *)` | 响应控件移动。 | 通常用于后端窗口更新。 |

### 一句话总结

`QVideoWidget` 是 Widgets 界面的视频输出端：它负责显示和适配，不负责播放、采集或解码。
