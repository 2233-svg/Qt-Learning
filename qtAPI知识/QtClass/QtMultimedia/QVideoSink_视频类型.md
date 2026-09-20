# QVideoSink：逐帧接收并处理 Qt Multimedia 视频

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QVideoSink>`  
> 所属模块：`Qt6::Multimedia`  
> 继承：`QObject`  
> 类型性质：视频帧接收器

## 它解决什么问题

`QVideoSink` 把 Qt Multimedia 输出的视频逐帧交给应用。它是一个通用接收端，不负责播放控制、摄像头采集或视频编码。

连接播放器或采集会话后，应用可以在 `videoFrameChanged()` 中取得每个 `QVideoFrame`，然后：

- 映射到 CPU 内存做图像分析；
- 转换成 `QImage` 进行处理；
- 交给自定义渲染器；
- 使用 `QVideoFrame::paint()` 绘制；
- 读取字幕文本或当前视频尺寸。

## 实际使用场景

- 摄像头预览中的二维码、条码、目标检测；
- 播放器的视频帧截图、取样和波形同步分析；
- 自定义 `QWidget`、`QGraphicsItem` 或 OpenGL/RHI 视频渲染；
- 录制前对视频帧加水印、裁剪或检测；
- 在不使用 `QVideoWidget` 的情况下构建自己的视频输出。

## 连接 QMediaPlayer

```cpp
auto *sink = new QVideoSink(this);
player->setVideoSink(sink);

connect(sink, &QVideoSink::videoFrameChanged,
        this, [this](const QVideoFrame &frame) {
    if (!frame.isValid())
        return;

    QVideoFrame copy = frame;
    if (copy.map(QVideoFrame::ReadOnly)) {
        // 读取 bits()、bytesPerLine() 等信息
        copy.unmap();
    }
});
```

也可以把 sink 设置到 `QMediaCaptureSession`，接收摄像头、屏幕或窗口采集的视频。

一个 sink 的作用是接收和保存“当前帧”引用。它不会自动把帧转换为 `QImage`，也不会自动替应用绘制到窗口。

## QVideoFrame 的资源边界

`QVideoFrame` 可能包含系统内存、GPU 纹理或平台视频缓冲，可能消耗较多资源。`videoFrameChanged()` 槽中应尽快完成必要操作，不要无限制地把每一帧存入容器。

如果要在信号返回后继续使用帧，应复制 `QVideoFrame` 值或提取应用自己的数据。复制值对象不一定复制底层像素，仍可能共享昂贵资源；需要长期保存时，通常应尽早转换为应用可控的 `QImage`、字节数组或分析结果。

读取 CPU 像素前必须检查 `map()` 返回值：

```cpp
QVideoFrame frame = sink->videoFrame();
if (frame.map(QVideoFrame::ReadOnly)) {
    const uchar *plane = frame.bits(0);
    const int stride = frame.bytesPerLine(0);
    Q_UNUSED(plane);
    Q_UNUSED(stride);
    frame.unmap();
}
```

不是所有帧都能被 CPU 映射，也不是所有像素格式都只有一个 plane。需要根据 `QVideoFrameFormat` 和 `planeCount()` 处理。

## videoFrameChanged() 的时序

`videoFrameChanged()` 表示 sink 的当前帧发生变化。它不是固定帧率定时器，也不保证每个解码帧都能在应用侧以同样频率观察到：

- 后端可能丢帧；
- 应用线程繁忙时，处理可能跟不上输入；
- 视频输出可能只在帧真正改变时通知；
- 切换媒体时可能先收到无效帧或尺寸变化。

如果业务需要稳定采样频率，应在应用层做节流或抽帧，不要用信号次数推断媒体总帧数。

## videoFrame() 与 setVideoFrame()

`videoFrame()` 返回 sink 当前保存的帧。无视频时通常是无效帧，应通过 `QVideoFrame::isValid()` 判断。

`setVideoFrame()` 可以手动把一个帧设置为当前帧，因此 `QVideoSink` 也可以作为自定义管线的终点：

```cpp
QVideoSink sink;
QVideoFrame frame = makeFrame();
sink.setVideoFrame(frame);
```

设置帧适合测试、帧转发或自定义输出。它不会自动把帧写入 `QMediaRecorder`，也不会让播放器开始播放。

## videoSize

`videoSize()` 返回当前视频尺寸。没有视频时返回无效的 `QSize`，因此应使用 `isValid()` 或检查宽高，而不是假定永远有正尺寸。

尺寸可能在切换媒体、切换轨道或视频格式变化时改变。应连接 `videoSizeChanged()`，不要只在构造时读取一次。

这个尺寸描述视频帧的基本尺寸，不代表窗口最终显示尺寸，也不自动包含应用布局、缩放、旋转和裁剪后的结果。

## subtitleText

`subtitleText` 保存当前字幕文本。播放器或后端可以通过 sink 更新它，应用也可以使用 `setSubtitleText()` 手动设置：

```cpp
connect(sink, &QVideoSink::subtitleTextChanged,
        this, [label](const QString &text) {
    label->setText(text);
});
```

设置字幕文本不会自动把字幕绘制到视频帧像素中。自定义渲染器需要自己决定字幕位置、字体、样式和绘制时机。

字幕文本也可能为空，表示当前没有可显示字幕或字幕轨道已关闭。

## RHI 和平台接口

### `rhi()` 与 `setRhi()`

`rhi()` 返回用于创建视频帧纹理数据的 `QRhi` 实例；`setRhi()` 设置该实例。这两个 API 面向底层图形集成，适合自定义 RHI 渲染管线或平台视频输出适配。

使用时要注意：

- `QRhi` 的生命周期必须覆盖 sink 使用它的时间；
- 图形资源必须在正确的图形线程和渲染上下文中使用；
- `QRhi` 不是像素格式转换器，也不会让所有视频帧自动变成可用纹理；
- 普通 QWidget/QImage 处理通常不需要显式设置 RHI。

### `platformVideoSink()`

`platformVideoSink()` 返回平台层的视频 sink 对象，类型为 `QPlatformVideoSink *`。它是 Qt Multimedia 平台集成接口，不是稳定的跨平台业务 API。

该指针不表示应用拥有对象，也不应把平台类型的方法当作 Qt Multimedia 公共跨平台契约。只有在明确依赖某个平台后端，并能接受版本和平台差异时，才应使用它。

## 生命周期、所有权和线程

`QVideoSink` 是 `QObject`，通常通过父对象管理。设置到 `QMediaPlayer` 或 `QMediaCaptureSession` 时，应用仍应保证 sink 在使用期间有效；连接输出不等于把所有权转移给播放器或会话。

sink 应在媒体对象所属线程中使用。视频帧信号通常通过事件循环交付，阻塞该线程会延迟帧处理和状态更新。

如果处理很重，可以在槽中快速复制或映射必要数据，再把轻量结果交给工作线程。不要把播放器、采集会话或 sink 本身直接跨线程操作。

## 常见误区

- 以为 `QVideoSink` 会自动显示视频；
- 未检查 `map()` 返回值就读取 `bits()`；
- 假定所有帧都是 RGB、只有一个 plane；
- 在槽中长期保存大量 `QVideoFrame`，造成 GPU/系统资源压力；
- 把 `videoFrameChanged()` 当成固定频率定时器；
- 把 `videoSize()` 当成窗口显示尺寸；
- 以为 `setVideoFrame()` 会驱动播放器或录制器；
- 在普通业务代码中依赖 `platformVideoSink()` 的平台私有行为；
- 忽略 sink、播放器和采集会话必须遵守同一线程边界。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QVideoSink(QObject *parent = nullptr)` | 创建视频帧接收器。 | 不会自动连接播放器或采集会话。 |
| 析构 | `~QVideoSink() override` | 销毁接收器。 | 销毁后不要再让媒体对象使用它。 |
| 图形 | `QRhi *rhi() const` | 返回用于创建视频帧纹理的 RHI。 | 可能为空；属于底层图形集成接口。 |
| 图形 | `void setRhi(QRhi *rhi)` | 设置视频帧纹理使用的 RHI。 | 需要保证 RHI 生命周期和线程上下文正确。 |
| 查询 | `QSize videoSize() const` | 返回当前视频尺寸。 | 无视频时返回无效 `QSize`。 |
| 字幕 | `QString subtitleText() const` | 返回当前字幕文本。 | 空字符串可能表示没有当前字幕。 |
| 字幕 | `void setSubtitleText(const QString &subtitle)` | 设置当前字幕文本。 | 只设置文本，不自动绘制字幕。 |
| 帧 | `void setVideoFrame(const QVideoFrame &frame)` | 手动设置当前视频帧。 | 适合自定义管线和测试，不会启动播放。 |
| 帧 | `QVideoFrame videoFrame() const` | 返回当前视频帧。 | 使用后应及时释放或提取所需数据。 |
| 平台 | `QPlatformVideoSink *platformVideoSink() const` | 返回平台层 sink。 | 非通用业务接口；不拥有返回对象。 |
| 信号 | `void videoFrameChanged(const QVideoFrame &frame) const` | 当前帧变化时通知应用。 | 不是固定帧率信号；帧资源可能很重。 |
| 信号 | `void subtitleTextChanged(const QString &subtitleText) const` | 当前字幕文本变化时通知。 | 文本为空也是合法状态。 |
| 信号 | `void videoSizeChanged()` | 当前视频尺寸变化时通知。 | 切换媒体或格式时应重新读取尺寸。 |

## 一句话总结

`QVideoSink` 是 Qt Multimedia 的逐帧出口：连接播放器或采集会话后，通过 `videoFrameChanged()` 取得 `QVideoFrame`，应用负责映射、处理和绘制，并要严格控制帧资源和线程边界。
