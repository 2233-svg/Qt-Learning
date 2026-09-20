# QMovie

> Qt 6.11.1 · Qt GUI · 来自 `QMovie`

## 1. 先建立直觉

`QMovie` 是 QObject 化的多帧图像播放器。它用事件循环按图片格式提供的时间间隔推进 GIF、WebP 等动画帧，并通过信号告诉界面“当前帧变了、需要更新哪块区域、动画是否结束或出错”。

它不是视频播放器，也不是任意网络流播放器。动画格式支持取决于已部署图像插件；带音频、编码率控制或时间轴剪辑的媒体应使用 Qt Multimedia。

## 2. 类说明

- 头文件：`#include <QMovie>`
- CMake：`target_link_libraries(app PRIVATE Qt6::Gui)`
- 继承：`QObject`。必须在有事件循环的线程中创建和使用，UI 常放 GUI 线程。
- 源：文件名或外部 `QIODevice*`；device 由调用者拥有，必须在 movie 使用期间保持可读有效。
- 显示：`QLabel::setMovie(movie)` 是最简用法；自绘可响应 `updated()` 后取 `currentPixmap()`。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QMovie(fileName/device[, format], parent)` | 创建动画播放器，可显式指定格式 |
| `setFileName()` / `setDevice()` / `setFormat()` | 更换动画来源和解码格式 |
| `isValid()` / `lastError()` / `lastErrorString()` | 检查格式/读取状态和错误 |
| `start()` / `stop()` | 从头启动或停止并回到 `NotRunning` |
| `setPaused(bool)` | 暂停/继续，保留当前帧 |
| `state()` | 查询 `NotRunning`、`Paused`、`Running` |
| `setSpeed(percent)` / `speed()` | 设置原始帧率的百分比，100 为正常速度 |
| `currentPixmap()` / `currentImage()` | 获取当前帧，前者便于 GUI 显示 |
| `currentFrameNumber()` / `frameCount()` | 查询当前帧号与总帧数；未知总数常为 0 |
| `jumpToFrame()` / `jumpToNextFrame()` | 定位帧；是否可用受格式/缓存/输入流限制 |
| `nextFrameDelay()` | 获取到下一帧的毫秒间隔 |
| `loopCount()` | 获取循环次数，`-1` 常表示无限 |
| `frameRect()` | 获取当前更新区域，可用于局部重绘 |
| `setScaledSize()` / `scaledSize()` | 请求按目标尺寸解码/缩放帧 |
| `setBackgroundColor()` | 为支持该格式的动画设置背景 |
| `setCacheMode(CacheNone)` | 默认不缓存，内存低但随机跳转/循环能力受限 |
| `setCacheMode(CacheAll)` | 缓存所有帧，支持顺序 device 的重复播放，内存高 |
| `started()` / `finished()` | 监听开始和自然结束 |
| `stateChanged()` | 监听运行、暂停、停止状态 |
| `frameChanged()` | 新帧号产生时更新关联逻辑 |
| `updated(rect)` | 当前帧的局部区域发生变化，适合自绘 |
| `resized(size)` | 动画帧尺寸发生变化 |
| `error(error)` | 播放读取失败后收到错误 |
| `supportedFormats()` | 查询当前部署环境可播放的动画格式 |
| `bindableCacheMode()` / `bindableSpeed()` | 用于 Qt 属性绑定的 bindable 访问器 |

## 4. 关键用法

### 交给 QLabel 自动播放

```cpp
auto *movie = new QMovie(":/media/spinner.gif", QByteArray(), this);
movie->setScaledSize(QSize(32, 32));

connect(movie, &QMovie::error, this, [movie] {
    qWarning() << movie->lastErrorString();
});

ui->spinnerLabel->setMovie(movie);
movie->start();
```

父对象应拥有 `QMovie`，而不是让它成为临时局部变量。`setScaledSize()` 要在播放前设置，能避免每帧先完整解码再由控件缩小。

### 自绘动画并只重绘变化区域

```cpp
connect(movie, &QMovie::updated, this,
        [this](const QRect &changed) {
            update(changed);
        });

void Preview::paintEvent(QPaintEvent *)
{
    QPainter p(this);
    p.drawPixmap(QPoint(), movie->currentPixmap());
}
```

某些动画帧只修改画面的一小部分，`updated(rect)` 允许减少重绘。若 widget 绘制时对当前 pixmap 施加缩放、平移或 DPR 变换，记得把 `rect` 映射到 widget 坐标再调用 `update()`。

### 用顺序输入流播放时选择缓存策略

```cpp
auto *movie = new QMovie(networkBuffer, "gif", this);
movie->setCacheMode(QMovie::CacheAll);
movie->start();
```

对不可回退的顺序 device，若希望动画可以循环或跳回前帧，需要 `CacheAll`。这会长期保留所有解码帧，帧数多、分辨率大时内存会迅速膨胀；对无限长或不可信输入不要无条件开启。

### 正确建模暂停与停止

```cpp
movie->setPaused(true);  // 停在当前帧
movie->setPaused(false); // 从下一帧继续

movie->stop();           // 进入 NotRunning，下次 start 从头
```

暂停适合窗口隐藏、用户主动暂停或暂时失焦；停止适合释放播放状态和重新开始。不要假定 `finished()` 一定代表“最后一帧永久保留”，它由格式循环设置与播放过程决定。

## 5. 状态与缓存

| 项目 | 含义 |
| --- | --- |
| `NotRunning` | 初始状态、`stop()` 后或动画自然结束后 |
| `Paused` | 保持当前帧，不继续发 `updated()`/`resized()` |
| `Running` | 定时器按帧延迟推进动画 |
| `CacheNone` | 默认，节省内存；随机跳转、回绕取决于格式与 device 能否重读 |
| `CacheAll` | 保留全部帧；适合小动画或顺序 device 回放，代价为内存 |

## 6. 使用场景

- 加载 spinner、空状态插画、循环提示和小型动图。
- 多帧格式的逐帧处理或截图式预览。
- 自绘控件中的动画贴图，使用 `updated()` 驱动局部刷新。
- 从内存 buffer 或资源系统播放一个短小、可信的动画。

## 7. 常见坑与经验

- **它依赖事件循环。** 在没有运行 event loop 的线程中 `start()` 不会按时间推进。
- **不是视频框架。** 大型、长时、带音频内容请用 Qt Multimedia，别把 `CacheAll` 当视频缓存。
- **`frameCount() == 0` 未必表示没有帧。** 有些格式/流无法提前知道总帧数；看 `isValid()`、当前帧与信号。
- **`currentPixmap()` 只在 GUI 线程使用。** 后台逐帧处理取 `currentImage()` 并设计清晰的线程交接。
- **格式推断可能失败。** 对无扩展名、内存/网络 device，传入明确的 `"gif"`、`"webp"` 等 format。
- **device 生命周期要长于 movie。** 特别是 `QBuffer` 不能在构造 `QMovie` 后立即离开作用域。
- **避免在 `frameChanged()` 做重活。** 该槽阻塞会拖慢定时器，表现为卡帧；耗时处理应丢给工作线程或减少工作量。
- **不要把网络下载和播放混为一体。** 确保数据可读、完整性和限制策略；不可信动态图还要限制尺寸、帧数与缓存。

## 8. 知识点覆盖

QObject 事件循环、动画帧、状态机、局部重绘、缓存模式、顺序设备、缩放解码、图像格式插件、错误信号、线程交接、动画与视频边界。
