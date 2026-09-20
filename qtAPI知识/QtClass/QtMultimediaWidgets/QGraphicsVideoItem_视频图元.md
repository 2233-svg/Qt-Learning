# QGraphicsVideoItem：在 Graphics View 场景中显示视频

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QGraphicsVideoItem>`  
> 所属模块：`Qt6::MultimediaWidgets`  
> 继承：`QGraphicsObject`  
> 类型性质：Graphics View 视频图元

## 它解决什么问题

`QGraphicsVideoItem` 把 `QMediaPlayer` 或 `QCamera` 的视频输出嵌入 `QGraphicsScene`。它不像 `QVideoWidget` 那样受 QWidget 布局管理，而是一个可放进场景、参与坐标变换和父子图元关系的视频图元。

它不负责解码或播放媒体，只负责在 Graphics View 绘制链路中展示视频帧。媒体源仍由 `QMediaPlayer`、`QCamera` 和 `QMediaCaptureSession` 等对象管理。

## 实际使用场景

- 在 `QGraphicsView` 的画布中显示播放器视频。
- 在视频上叠加文本、框选、轨迹、控件或可交互标注。
- 监控墙、视频编辑器和带缩放/平移的可视化应用。
- 直接把自定义 `QVideoFrame` 送给图元显示。

```cpp
auto *item = new QGraphicsVideoItem;
scene->addItem(item);

player->setVideoOutput(item);
player->setSource(QUrl::fromLocalFile(filePath));
player->play();
```

一个媒体对象同一时刻只能有一个显示输出。将播放器改连 `QVideoWidget`、另一个图元或 `QVideoSink`，会替换当前图元输出。

## 图元尺寸、偏移和原始尺寸

### `size`

`size` 是绘制视频时使用的目标矩形尺寸。视频在这个区域内依照 `aspectRatioMode` 进行缩放，不一定逐像素等于原始帧。

### `offset`

`offset` 是视频左上角在图元局部坐标中的偏移。可用它给边框、标题、控件叠层预留位置，也会影响视频实际绘制位置。

### `nativeSize`

`nativeSize` 表示当前视频的自然尺寸，而不是图元的当前 `size`。媒体尚未输出帧时它可能为空或未确定；应监听 `nativeSizeChanged()` 后再据此初始化比例布局。

## 宽高比模式

`setAspectRatioMode()` 控制视频适配 `size` 的方式：

| 模式 | 显示效果 | 代价 |
| --- | --- | --- |
| `Qt::KeepAspectRatio` | 保持比例完整显示 | 可能有空白区域 |
| `Qt::KeepAspectRatioByExpanding` | 保持比例填满区域 | 可能裁剪边缘 |
| `Qt::IgnoreAspectRatio` | 拉伸到目标区域 | 画面可能变形 |

它不修改 `nativeSize`、视频帧像素或播放器输出格式，只决定图元的呈现方式。

## `videoSink()` 与自定义帧

图元内部始终有一个 `QVideoSink`，`videoSink()` 不会返回空指针。除了把图元传给 `QMediaPlayer::setVideoOutput()`，也可以直接向它提交帧：

```cpp
QImage image(":/images/preview.png");
item->videoSink()->setVideoFrame(QVideoFrame(image));
```

这种方式适合测试、算法处理后的画面或自定义采集源。提交者仍要负责帧产生节奏、线程边界和内容正确性；图元不会替应用做编码、限帧或缓冲队列管理。

## 几何、绘制和图元类型

### `boundingRect()`

返回图元边界，供场景索引、碰撞检测和重绘区域计算使用。不要在自定义代码中只改绘制结果却不让几何信息与之对应。

### `paint()`

由 Graphics View 在 GUI 线程中调用，用于绘制当前视频帧。通常不需要重写；若需要完整自定义渲染，直接使用独立 `QVideoSink` 接收帧往往更清晰。

### `type()`

返回固定值 `14`，使 `qgraphicsitem_cast<QGraphicsVideoItem *>()` 可用。它不是视频格式、媒体类型或业务分类编号。

## 生命周期、线程和性能边界

`QGraphicsVideoItem` 是 Graphics View 对象，创建、加入场景、移动、调整大小和绘制都应发生在 GUI 线程。不要从解码、摄像头或算法后台线程直接修改图元。

高分辨率视频、缩放、复杂场景变换和多个并行视频图元都会增加 GUI 绘制压力。需要低延迟或大量并发视频时，应在目标平台实测帧率、CPU/GPU 占用和事件队列积压情况。

## 常见误区

- 把 `QGraphicsVideoItem` 当成播放器，忘记调用 `setVideoOutput()`。
- 将 `nativeSize` 误认为当前 `size`。
- 只设置 `size` 却忽略宽高比模式，导致画面变形或裁剪。
- 在后台线程直接修改场景或图元。
- 同时把一个播放器接到图元和另一个显示输出。
- 把 `type() == 14` 当成可自定义扩展的媒体类型。
- 在收到首帧前就把未确定的 `nativeSize` 用作最终布局。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QGraphicsVideoItem(QGraphicsItem *parent = nullptr)` | 创建场景视频图元。 | `parent` 是图元父节点。 |
| 析构 | `~QGraphicsVideoItem()` | 销毁图元。 | 不代替播放器生命周期管理。 |
| 输出 | `QVideoSink *videoSink() const` | 取得内部视频 sink。 | 永不为空，受图元生命周期约束。 |
| 属性 | `Qt::AspectRatioMode aspectRatioMode() const` | 查询视频适配策略。 | 影响留白、裁剪和变形。 |
| 属性 | `void setAspectRatioMode(Qt::AspectRatioMode)` | 设置视频适配策略。 | 不改写底层像素。 |
| 属性 | `QPointF offset() const` | 查询视频绘制偏移。 | 使用图元局部坐标。 |
| 属性 | `void setOffset(const QPointF &)` | 设置视频绘制偏移。 | 影响视频位置和图元边界。 |
| 属性 | `QSizeF size() const` | 查询绘制目标尺寸。 | 不是 `nativeSize`。 |
| 属性 | `void setSize(const QSizeF &)` | 设置视频区域尺寸。 | 显示仍受宽高比策略影响。 |
| 属性 | `QSizeF nativeSize() const` | 查询视频自然尺寸。 | 出帧前可能未确定。 |
| 信号 | `nativeSizeChanged(const QSizeF &)` | 通知自然尺寸变化。 | 用于响应式布局。 |
| 几何 | `QRectF boundingRect() const` | 返回图元边界。 | 参与场景重绘和索引。 |
| 绘制 | `paint(QPainter *, const QStyleOptionGraphicsItem *, QWidget *)` | 绘制当前视频帧。 | 通常不应替换内部实现。 |
| 类型 | `int type() const` | 返回图元类型。 | 固定值 14，用于图元转换。 |

### 一句话总结

`QGraphicsVideoItem` 是 Graphics View 中的视频输出端：用 `size`、`offset` 和宽高比控制呈现，用 `videoSink()` 接收媒体或自定义帧。
