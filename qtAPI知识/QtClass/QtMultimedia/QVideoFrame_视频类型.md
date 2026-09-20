# QVideoFrame：承载一帧视频数据及其显示元数据

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QVideoFrame>`  
> 所属模块：`Qt6::Multimedia`  
> 继承：无  
> 类型性质：显式共享值类型

## 它解决什么问题

`QVideoFrame` 表示“某一帧视频”本身。它不仅可以引用像素数据，还携带这帧的像素格式、尺寸、时间戳、帧率、旋转、镜像和字幕文本等信息。

视频帧可能来自不同的存储位置：

- `QMediaPlayer` 解码得到的系统内存或 GPU 资源；
- `QCamera`、`QScreenCapture`、`QWindowCapture` 产生的采集帧；
- `QVideoFrameInput` 要送入录制器的应用自定义帧；
- 通过 `QAbstractVideoBuffer` 包装的第三方或硬件视频缓冲。

`QVideoFrame` 解决的是“统一描述并传递这些帧”，而不是“保证每一帧都能直接当作 `QImage` 使用”。底层可能是多平面 YUV、压缩 JPEG、RHI 纹理或无法被 CPU 直接访问的硬件缓冲。

## 实际使用场景

- 在 `QVideoSink::videoFrameChanged()` 中逐帧分析摄像头画面；
- 将自定义渲染结果送入 `QVideoFrameInput` 录制；
- 在需要 CPU 像素时映射视频缓冲，读取 Y、U、V 或 RGB 平面；
- 把可转换的帧转成 `QImage`，用于截图、算法或保存；
- 根据时间戳做音视频同步，根据旋转和镜像做正确显示；
- 在自定义绘制代码中用 `paint()` 把帧画到 `QPainter` 目标上。

## 值语义不等于深拷贝

`QVideoFrame` 是显式共享类型。复制一个帧通常只复制共享的帧对象，不会立即复制底层像素：

```cpp
QVideoFrame a = sink->videoFrame();
QVideoFrame b = a; // 浅复制；a 和 b 仍然表示同一帧资源
```

因此，复制后的两个对象会反映同一帧；对一个副本进行修改，可能影响其他副本。这个设计避免了视频帧复制的高成本，但也意味着不能把复制当作写时自动隔离。

帧可能持有较大的系统内存、GPU 纹理或平台缓冲。处理完成后应尽快释放不再需要的副本。要跨较长时间保存内容，通常应将需要的像素转换成应用拥有的 `QImage` 或字节数据，而不是无限累积 `QVideoFrame`。

## 创建帧

### 默认构造和格式构造

```cpp
QVideoFrame invalid;

QVideoFrameFormat format(
        QSize(1280, 720),
        QVideoFrameFormat::Format_ARGB8888);
QVideoFrame frame(format);
```

默认构造产生无效帧。用 `QVideoFrameFormat` 构造时，格式必须有有效像素格式和帧尺寸，否则得到的帧也不能用于正常的视频处理。

格式构造主要建立帧的格式描述；它不等同于为任意格式自动分配一个可写的 CPU 像素缓冲。自定义缓冲应使用 Qt 6.8 起的 `std::unique_ptr<QAbstractVideoBuffer>` 构造方式。

### 从 `QImage` 构造

Qt 6.8 起可以显式从 `QImage` 构造：

```cpp
QImage image(640, 480, QImage::Format_ARGB32_Premultiplied);
QVideoFrame frame(image);
```

如果 `QImage::Format` 与某个 `QVideoFrameFormat::PixelFormat` 对应，帧可以直接持有该图像并复用其格式，不必先做格式转换。若没有对应格式，Qt 会把图像转换为支持的 RGB/ARGB 格式，这可能产生额外开销。

传入空的 `QImage` 会生成无效 `QVideoFrame`。另外，即使构造阶段没有复制像素，后续以 `WriteOnly` 映射并保留原图像时也可能触发复制，以保护图像的共享数据。

### 从自定义视频缓冲构造

Qt 6.8 起推荐通过拥有式智能指针传入自定义缓冲：

```cpp
std::unique_ptr<QAbstractVideoBuffer> buffer =
        std::make_unique<ExternalVideoBuffer>(format);
QVideoFrame frame(std::move(buffer));
```

帧会在其共享对象的最后一个副本销毁时销毁该缓冲。若帧已经送入录制器或渲染管线，帧资源的最终释放线程和时间可能由下游决定，外部代码不能假设一定在当前线程销毁。

旧的 `QVideoFrame(QAbstractVideoBuffer *, ...)` 内部构造函数在 Qt 6.8 已弃用，新代码不要使用。

## 判断帧和查询存储类型

`isValid()` 只表示帧具有关联的视频缓冲；无效帧没有可用的底层数据。它不保证该帧能被 CPU 映射，也不保证格式是应用想要的格式。

`pixelFormat()` 返回帧的像素格式；`surfaceFormat()` 返回帧的格式描述副本；`size()`、`width()`、`height()` 返回帧尺寸。`planeCount()` 返回实际使用的平面数量，处理 YUV 时不能假设一定只有一个平面。

`handleType()` 可区分：

- `NoHandle`：没有可用的外部句柄，通常需要通过 `map()` 访问数据；
- `RhiTextureHandle`：底层句柄由 Qt Rendering Hardware Interface 定义，适合底层 RHI 视频渲染。

`handleType()` 并不意味着应用可以把 `QVideoFrame` 任意转换成某个 OpenGL、Vulkan 或 Direct3D 句柄。只有在对应 RHI 管线和上下文契约成立时，底层句柄才有意义。

## 映射 CPU 内存

当帧在 GPU 或平台视频内存中时，必须先映射才能通过 `bits()` 等接口访问：

```cpp
QVideoFrame frame = sink->videoFrame();
if (!frame.isValid())
    return;

if (!frame.map(QVideoFrame::ReadOnly))
    return;

for (int plane = 0; plane < frame.planeCount(); ++plane) {
    const uchar *data = frame.bits(plane);
    const int stride = frame.bytesPerLine(plane);
    const int size = frame.mappedBytes(plane);
    // 依据 pixelFormat() 解释 data、stride 和 size。
    Q_UNUSED(data);
    Q_UNUSED(stride);
    Q_UNUSED(size);
}

frame.unmap();
```

映射可能触发 GPU 到 CPU 的复制或其它昂贵同步，因此只在确实需要 CPU 数据时调用，并在访问结束后立即 `unmap()`。

### `MapMode` 的语义

| 模式 | 映射时的内容 | `unmap()` 时的行为 | 适用方向 |
| --- | --- | --- | --- |
| `NotMapped` | 没有映射 | 不适用 | 查询当前状态 |
| `ReadOnly` | 从视频缓冲填充，可读取 | 修改内容可能被丢弃 | 分析、取样、转换 |
| `WriteOnly` | 初始内容未初始化 | 可能修改的内容写回帧 | 完整覆盖写入 |
| `ReadWrite` | 从视频缓冲填充 | 修改内容写回帧 | 需要读旧值再改写 |

写入只读映射的内存属于未定义行为，可能修改共享数据，甚至导致崩溃。要写帧，至少使用 `WriteOnly` 或 `ReadWrite`。

`ReadOnly` 映射可以嵌套，但每次成功的 `map(ReadOnly)` 都必须对应一次 `unmap()`。其它映射模式再次 `map()` 前必须先解除已有映射。映射失败时不要调用 `unmap()`。

### 映射指针和行跨度的边界

`bits(plane)` 返回指定平面的起始地址，只在映射有效期间可用。`mappedBytes(plane)` 是该平面映射区域的字节数，`bytesPerLine(plane)` 是每行占用的字节数；它们都不是“像素宽度”。

平面参数必须满足 `0 <= plane < planeCount()`。对于 `NV12`、`NV21`、`YUV420P` 等格式，必须按实际平面数量和格式解释每个地址、行跨度以及平面尺寸。不能把所有 YUV 都当作一块连续的 RGB 内存。

## 时间戳、帧率和显示元数据

`startTime()` 和 `endTime()` 是帧的呈现时间，单位为微秒。无效时间用 `-1` 表示：

```cpp
frame.setStartTime(2'000'000); // 2 秒
frame.setEndTime(2'033'333);   // 约 33.333 ms 后
```

它们描述应何时开始和停止显示，不是 `QMediaPlayer::position()` 那样的毫秒单位。跨 API 计算时必须显式换算，避免把微秒当毫秒。

`streamFrameRate()` 是视频流的帧率，单位是帧每秒。它是描述信息，不是让帧自动按该频率播放的计时器，也不一定等于实际每一帧到达应用的频率。

`rotation()` / `setRotation()` 使用 `QtVideo::Rotation`，支持 `None`、`Clockwise90`、`Clockwise180` 和 `Clockwise270`。`mirrored()` / `setMirrored()` 表示显示前是否围绕垂直轴镜像。旋转先应用，镜像后应用；这类属性改变的是呈现方式，不是底层像素排列。

前置摄像头常需要镜像。若应用已经自行旋转或镜像像素，又把这些元数据交给渲染器，可能造成双重变换。

`subtitleText()` 是随帧携带的、应与该帧一起呈现的字幕文本。设置文本不会把文字直接烧录进像素；绘制逻辑仍由 `paint()` 或应用自己的渲染器决定。

## 转换和绘制

`toImage()` 根据当前像素数据和 `surfaceFormat()` 转换为 `QImage`。它只反映当前帧的像素内容，不应用 `QVideoFrame` 的 rotation 和 mirroring，因为这些是仅用于呈现的变换。若需要得到最终方向的图像，应用应在转换后自行处理，或使用适合的渲染路径。

`paint()` 使用 `QPainter` 将帧绘制到给定矩形，可通过 `PaintOptions` 指定背景色、宽高比模式和是否绘制字幕：

```cpp
void VideoWidget::paintEvent(QPaintEvent *)
{
    QPainter painter(this);
    QVideoFrame frame = m_sink->videoFrame();
    if (!frame.isValid())
        return;

    QVideoFrame::PaintOptions options;
    options.aspectRatioMode = Qt::KeepAspectRatio;
    frame.paint(&painter, rect(), options);
}
```

`paint()` 通常不会使用硬件加速，适合简单的 QWidget 绘制或调试，不适合作为高吞吐 GPU 视频渲染的默认方案。调用者必须提供有效的 `QPainter` 和目标矩形，并保证绘制发生在正确的绘制阶段。

## 常见误区

- 认为复制 `QVideoFrame` 一定会复制像素，结果多个对象修改同一底层资源；
- 未检查 `isValid()` 或 `map()` 返回值就读取数据；
- 在 `ReadOnly` 映射内写入；
- 忘记 `unmap()`，导致硬件缓冲或临时 CPU 映射长期占用；
- 认为每个视频帧只有一个 plane；
- 把 `bytesPerLine()` 当成紧密像素宽度；
- 把 `startTime()`/`endTime()` 的微秒与播放器毫秒直接比较；
- 以为 rotation、mirrored 会改写 `bits()` 中的像素；
- 以为 `toImage()` 会自动应用旋转、镜像和字幕；
- 把 `paint()` 当作硬件加速视频渲染器；
- 在下游仍可能使用帧时立即修改或释放自定义缓冲；
- 新代码继续使用已弃用的 `RotationAngle` 或内部 `videoBuffer()`。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `enum HandleType` | 描述视频缓冲句柄类型。 | 不是任意图形 API 句柄的通用转换接口。 |
| 枚举值 | `NoHandle` | 表示没有可用句柄。 | 通常需要 `map()` 后访问 CPU 数据。 |
| 枚举值 | `RhiTextureHandle` | 表示句柄由 Qt RHI 定义。 | 依赖 RHI 管线、线程和上下文契约。 |
| 枚举 | `enum MapMode` | 描述映射的读写意图。 | `NotMapped`、`ReadOnly`、`WriteOnly`、`ReadWrite`。 |
| 枚举值 | `NotMapped` | 表示当前未映射。 | `mapMode()` 的初始状态通常是它。 |
| 枚举值 | `ReadOnly` | 映射时读取帧内容。 | 只读映射可嵌套；写入属于未定义行为。 |
| 枚举值 | `WriteOnly` | 映射后写入帧内容。 | 初始内存未初始化，适合完整覆盖。 |
| 枚举值 | `ReadWrite` | 先读取再写回帧。 | 可能产生读回和写回开销。 |
| 弃用枚举 | `RotationAngle` | 旧式旋转角度枚举。 | Qt 6.7 起弃用，改用 `QtVideo::Rotation`。 |
| 构造 | `QVideoFrame()` | 创建无效帧。 | `isValid()` 返回 `false`。 |
| 构造 | `QVideoFrame(const QVideoFrameFormat &format)` | 按格式创建视频帧。 | 格式无效时不能得到可用帧；不等于自动提供任意 CPU 缓冲。 |
| 构造 | `explicit QVideoFrame(const QImage &image)` | 从图像创建视频帧。 | Qt 6.8 起；不匹配的图像格式可能被转换。 |
| 构造 | `explicit QVideoFrame(std::unique_ptr<QAbstractVideoBuffer> videoBuffer)` | 从自定义视频缓冲创建帧。 | Qt 6.8 起；帧负责共享持有缓冲的生命周期。 |
| 构造 | `QVideoFrame(const QVideoFrame &other)` | 浅复制帧。 | 与原对象共享同一帧资源。 |
| 构造 | `QVideoFrame(QVideoFrame &&other)` | 移动构造帧。 | 源对象进入可析构、可重新赋值状态。 |
| 析构 | `~QVideoFrame()` | 释放当前帧引用。 | 最后一个副本销毁时才可能释放底层缓冲。 |
| 赋值 | `operator=(const QVideoFrame &other)` | 共享赋值。 | 不进行深拷贝。 |
| 赋值 | `operator=(QVideoFrame &&other)` | 移动赋值。 | 目标原有引用被替换。 |
| 比较 | `operator==` / `operator!=` | 判断是否反映同一帧。 | 比较的是帧对象身份，不是逐像素内容。 |
| 工具 | `void swap(QVideoFrame &other)` | 交换两个帧对象。 | `noexcept`；不复制像素。 |
| 有效性 | `bool isValid() const` | 判断是否有关联视频缓冲。 | 有效不代表可映射或格式符合业务要求。 |
| 格式 | `QVideoFrameFormat::PixelFormat pixelFormat() const` | 返回帧像素格式。 | 处理数据前应读取实际格式。 |
| 格式 | `QVideoFrameFormat surfaceFormat() const` | 返回帧表面格式描述。 | 返回值是格式对象副本，不是底层数据。 |
| 存储 | `HandleType handleType() const` | 返回缓冲句柄类型。 | `NoHandle` 和 `RhiTextureHandle` 的访问路径不同。 |
| 尺寸 | `QSize size() const` | 返回帧尺寸。 | 不一定等于 viewport 或窗口显示尺寸。 |
| 尺寸 | `int width() const` | 返回帧宽度。 | 应与实际格式和 viewport 一起理解。 |
| 尺寸 | `int height() const` | 返回帧高度。 | 旋转只改变呈现方向，不直接交换底层尺寸。 |
| 映射状态 | `bool isMapped() const` | 判断是否已映射到系统内存。 | 只表示映射状态，不保证数据内容正确。 |
| 映射状态 | `bool isReadable() const` | 判断映射时是否从帧读取了内容。 | `WriteOnly` 映射通常为 `false`。 |
| 映射状态 | `bool isWritable() const` | 判断解除映射时是否会写回帧。 | 只读映射上写入仍是未定义行为。 |
| 映射状态 | `MapMode mapMode() const` | 返回当前映射模式。 | 用于调试和判断读写权限。 |
| 映射 | `bool map(MapMode mode)` | 将帧内容映射到 CPU 可访问内存。 | 可能触发复制或同步；成功后才能访问像素。 |
| 映射 | `void unmap()` | 释放映射并按需写回内容。 | 成功映射才调用；写映射的提交点。 |
| 像素 | `uchar *bits(int plane)` | 返回可写的平面起始地址。 | 只在映射期间有效；平面索引必须合法。 |
| 像素 | `const uchar *bits(int plane) const` | 返回只读的平面起始地址。 | 只在映射期间有效；未读映射时内容可能未初始化。 |
| 像素 | `int mappedBytes(int plane) const` | 返回平面映射区域的字节数。 | 只在映射期间有效；不是像素数。 |
| 像素 | `int bytesPerLine(int plane) const` | 返回平面每行字节数。 | 可能包含对齐填充，不等于宽度乘每像素字节数。 |
| 平面 | `int planeCount() const` | 返回实际平面数量。 | YUV 需按该值遍历，不能写死一个平面。 |
| 时间 | `qint64 startTime() const` | 返回开始呈现时间，微秒。 | 无效值为 `-1`。 |
| 时间 | `void setStartTime(qint64 time)` | 设置开始呈现时间。 | 使用微秒；不要直接传播放器毫秒位置。 |
| 时间 | `qint64 endTime() const` | 返回停止呈现时间，微秒。 | 无效值为 `-1`。 |
| 时间 | `void setEndTime(qint64 time)` | 设置停止呈现时间。 | 应与 start time 使用同一时间基准。 |
| 帧率 | `qreal streamFrameRate() const` | 返回视频流帧率，帧/秒。 | 描述元数据，不是自动播放调度器。 |
| 帧率 | `void setStreamFrameRate(qreal rate)` | 设置视频流帧率。 | 下游是否采用它取决于媒体管线。 |
| 旋转 | `QtVideo::Rotation rotation() const` | 返回显示前顺时针旋转角度。 | 旋转先于镜像；只影响呈现。 |
| 旋转 | `void setRotation(QtVideo::Rotation angle)` | 设置显示旋转。 | 不改写底层像素。 |
| 镜像 | `bool mirrored() const` | 查询是否显示前镜像。 | 围绕垂直轴；镜像在旋转后应用。 |
| 镜像 | `void setMirrored(bool)` | 设置显示镜像。 | 常用于前置摄像头；不改写像素。 |
| 字幕 | `QString subtitleText() const` | 返回随帧携带的字幕文本。 | 只是元数据，不等于已经绘制。 |
| 字幕 | `void setSubtitleText(const QString &text)` | 设置随帧呈现的字幕文本。 | 实际位置、字体和绘制由渲染器决定。 |
| 转换 | `QImage toImage() const` | 将当前帧转换为 `QImage`。 | 不应用 rotation/mirrored；不保证所有格式都能成功转换。 |
| 绘制 | `void paint(QPainter *, const QRectF &, const PaintOptions &)` | 用 `QPainter` 绘制帧。 | 通常无硬件加速；需有效 painter 和绘制阶段。 |
| 绘制类型 | `struct PaintOptions` | 配置背景色、宽高比和绘制标志。 | `DontDrawSubtitles` 可禁止绘制随帧字幕。 |
| 弃用函数 | `rotationAngle()` / `setRotationAngle()` | 旧式旋转 API。 | Qt 6.7 起弃用，使用 `rotation()` / `setRotation()`。 |
| 弃用函数 | `videoBuffer()` | 返回内部视频缓冲。 | Qt 6.8 起弃用；新代码使用 `std::unique_ptr` 构造和公开帧 API。 |

## 一句话总结

`QVideoFrame` 是 Qt Multimedia 中“一帧视频资源加呈现元数据”的共享值对象：先确认有效性和实际格式，再按映射契约访问平面；时间戳用微秒，旋转和镜像只影响显示，长期保存则应尽早提取应用自己的数据。
