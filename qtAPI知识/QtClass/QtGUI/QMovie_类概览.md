# QMovie：逐帧播放动画图像

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMovie>`  
> 模块：`Qt6::Gui`  
> 继承：`QObject`  
> 常用协作类型：`QLabel`、`QIODevice`、`QImageReader`、`QImage`、`QPixmap`

`QMovie` 是基于 `QImageReader` 的动画图像播放便利类。它解码并按帧推进 GIF 等动画图像，发出状态和帧更新信号，但不处理声音、视频轨、字幕、网络缓冲策略或完整媒体播放控制。需要多媒体文件播放时，应使用 Qt Multimedia 的相关类型。

## 它解决的问题

对“加载一个动画图片，按原始帧时序显示出来”这类 UI 需求，`QMovie` 省去了手动解析图像帧、读取帧延迟、安排定时器和管理循环的工作。

它适合：

- `QLabel` 中显示加载指示、空状态动画、表情或简短 GIF。
- 用 `updated()` 触发自定义 widget 的局部重绘。
- 从 `QFile`、内存缓冲区或其他 `QIODevice` 读取动画图像。
- 用 `jumpToFrame()` 实现简单的帧预览或调试。

它不适合：

- 有声音的视频或音视频同步。
- 大尺寸、高帧率、长时间的动画内容。
- 需要可靠随机访问且动画帧占用很大的资源。
- 在工作线程中直接驱动 `QPixmap` 或 `QWidget` 绘制。

## 最小可用示例：交给 QLabel 显示

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui Widgets)
target_link_libraries(my_app PRIVATE Qt6::Gui Qt6::Widgets)
```

```cpp
#include <QLabel>
#include <QMovie>

auto *label = new QLabel(this);
auto *movie = new QMovie(QStringLiteral(":/animations/loading.gif"), {}, label);

label->setMovie(movie);

connect(movie, &QMovie::error, label,
        [movie](QImageReader::ImageReaderError) {
            qWarning() << movie->lastErrorString();
        });

if (movie->isValid())
    movie->start();
```

`QMovie` 是不可复制的 `QObject`。上例将 `movie` 的 parent 设为 `label`，由 label 的析构统一销毁它。`QLabel::setMovie()` 负责显示当前帧，不应把它当作 movie 的所有权转移；显式 parent 关系更清楚。

## 生命周期与状态机

`QMovie::MovieState` 有三个状态：

| 状态 | 含义 | 关键行为 |
| --- | --- | --- |
| `NotRunning` | 未开始、已停止或播放失败后停止。 | 不继续发出 `updated()`/`resized()`；之后 `start()` 从开头重新播放。 |
| `Running` | 正在按帧推进。 | 每帧更新可能发出 `updated()`、`frameChanged()`，尺寸变化时发出 `resized()`。 |
| `Paused` | 暂停在当前帧。 | 保留当前帧号；不继续发出更新，`setPaused(false)` 从下一帧继续。 |

```cpp
connect(movie, &QMovie::stateChanged, this,
        [this](QMovie::MovieState state) {
            m_playButton->setText(
                state == QMovie::Running ? tr("Pause") : tr("Play"));
        });

movie->setPaused(true);   // Running -> Paused
movie->setPaused(false);  // Paused -> Running
movie->stop();            // -> NotRunning；下次 start() 从头开始
```

`start()` 在 `Paused` 状态等价于恢复播放；若已经 `Running` 则不做事。`stop()` 不是暂停：它进入 `NotRunning`，下一次 `start()` 会从第一帧重新开始。

播放错误会发出 `error(QImageReader::ImageReaderError)`，停止 movie 并进入 `NotRunning`。错误处理应读取 `lastError()` 和 `lastErrorString()`，而非仅依赖 `isValid()` 的一次检查，因为数据也可能在播放过程中出错。

## 输入来源：文件、设备与格式

`QMovie` 可从文件名或 `QIODevice` 读取：

```cpp
auto *file = new QFile(QStringLiteral(":/animations/status.gif"), this);
auto *movie = new QMovie(file, QByteArrayLiteral("gif"), this);

if (!file->open(QIODevice::ReadOnly)) {
    qWarning() << file->errorString();
} else if (movie->isValid()) {
    movie->start();
}
```

`setDevice()` 传入的是原始 `QIODevice *`。应由调用方保证设备在 movie 的整个读取期间存活、保持可读并且遵守线程归属；最简单的方式是让 device 和 movie 拥有同一 parent，或让 device 的寿命更长。切换 `setDevice()`、`setFileName()`、`setFormat()` 前，实践上先 `stop()`，再重新校验并启动，避免把正在工作的解码器切到另一来源。

| API | 含义 | 边界 |
| --- | --- | --- |
| `setFileName()` | 以文件作为来源。 | 由 Qt 打开并读取；`fileName()` 在当前来源不是文件时返回空字符串。 |
| `setDevice()` | 以任意可读 `QIODevice` 作为来源。 | 设备必须保持有效；顺序设备不能回退读取。 |
| `setFormat()` | 指定格式名称，例如 `"gif"`。 | 空格式时 Qt 尝试猜测；明确格式可减少探测歧义。 |
| `supportedFormats()` | 查询当前 Qt 安装支持的动画格式。 | 受图像插件部署影响，不能假定每个平台都一样。 |

## 缓存与顺序设备

`CacheMode` 决定是否保留已经解码的帧：

| 模式 | 行为 | 代价与用途 |
| --- | --- | --- |
| `CacheNone` | 默认值，不缓存所有帧。 | 内存占用低；某些格式/设备不支持跳帧或回到开头。 |
| `CacheAll` | 将所有帧保留到内存。 | 可辅助跳帧、回退和循环；长动画或高分辨率内容会显著占用内存。 |

当动画来自 socket、管道等顺序设备时，底层解码器无法回到已经读过的帧。如果需要循环播放，这种来源必须使用 `CacheAll`；否则即使文件本身声明循环，数据也无法重新读取。

```cpp
movie->setCacheMode(QMovie::CacheAll);
movie->start();
```

不要把 `CacheAll` 当成默认优化。先估算帧数量、每帧尺寸和像素格式；一个看似短小的高分辨率动画仍可能占用大量内存。

## 帧更新与显示方式

`QLabel::setMovie()` 是最省事的显示路径。若由自定义 widget 绘制，可监听 `updated()`，再通过 `currentImage()` 或 `currentPixmap()` 取得当前帧：

```cpp
connect(movie, &QMovie::updated, this,
        [this](const QRect &changedRect) {
            update(changedRect);
        });

void AnimatedBadge::paintEvent(QPaintEvent *)
{
    QPainter painter(this);
    painter.drawPixmap(rect(), m_movie->currentPixmap());
}
```

| API/信号 | 适用场景 | 注意 |
| --- | --- | --- |
| `updated(const QRect &rect)` | 只重绘当前帧中变动的区域。 | 获取当前帧后按 `rect` 调用 `update()`，避免不必要的整块刷新。 |
| `frameChanged(int)` | 需要帧号、逐帧统计或精确逻辑。 | 可在槽中读 `currentImage()`/`currentPixmap()`。 |
| `resized(const QSize &size)` | 动画帧尺寸随内容变化。 | 调整控件布局或缓存时监听它。 |
| `currentImage()` | 图像处理、像素访问或后台算法的输入。 | 返回当前帧的 `QImage` 值；仍不要跨线程直接操作 `QMovie` 本体。 |
| `currentPixmap()` | GUI 绘制、`QLabel` 外的 widget 绘制。 | `QPixmap` 属于 GUI 资源，应在 GUI 线程使用。 |

`frameRect()` 在尚未更新任何帧时返回无效矩形。不要在刚构造 movie 后用它决定控件大小；等到首个 `updated()`/`resized()`，或先准备固定占位尺寸。

## 速度、缩放、循环与帧跳转

`speed` 以原始速度的百分比表示，默认是 `100`：

```cpp
movie->setSpeed(150); // 1.5 倍速
movie->setScaledSize(QSize(96, 96)); // 在解码流程中缩放帧
```

`setScaledSize()` 在 movie 输出帧前缩放，通常比每次 `paintEvent()` 里重复缩放更合适；但不同显示区域需要不同尺寸时，应选择一个明确的缩放策略，避免两层重复缩放导致模糊和额外开销。

`loopCount()` 的结果含义如下：

- `0`：只播放一次，不循环。
- 正整数：完成指定循环次数后结束。
- `-1`：无限循环。

`frameCount()` 仅在格式支持总帧数时才可靠；不支持时返回 `0`，不能把 `0` 一概解释为“没有动画帧”。`currentFrameNumber()` 的第一帧为 `0`。

`jumpToFrame()` 与 `jumpToNextFrame()` 返回 `bool`，必须检查。随机跳帧是否成功取决于格式、底层 handler 和缓存状态；顺序设备、未缓存帧和不支持跳转的格式可能失败。

## 线程、事件循环与性能

`QMovie` 依赖其线程的事件循环安排下一帧，且它通常与 `QLabel`、`QPixmap` 等 GUI 类型协作。因此最常见、最稳妥的用法是：创建、连接、启动、停止和销毁都在 GUI 线程完成。

- 不要从工作线程直接调用 GUI 线程中 `QMovie` 的方法；通过 queued signal/slot 或 `QMetaObject::invokeMethod()` 转回对象所属线程。
- 只做图像分析时，复制 `currentImage()` 的结果后交给工作线程处理；不要把 movie 或 `QPixmap` 直接移交。
- `nextFrameDelay()` 是解码器建议的下一帧等待毫秒数，不是应用逻辑的精准时钟，也不应据此另起一个竞争定时器驱动同一 movie。
- 多个大型动画同时播放会带来解码、缩放、绘制和内存压力。对不可见标签调用 `stop()`，或共享更合适的动画资源策略。

## 常见错误

1. **把 QMovie 当视频播放器。** 它只播放无声音的动画图像。
2. **movie 没有 parent，label 销毁后仍在播放。** 显式管理 QObject 所有权，例如将 movie 设为 label 的子对象。
3. **顺序设备上循环却保持 `CacheNone`。** 无法回读已消费帧；循环需要 `CacheAll`。
4. **以为 `stop()` 能继续播放。** `stop()` 后 `start()` 从头开始；临时停住使用 `setPaused(true)`。
5. **在首帧出现前读取有效 `frameRect()`。** 会得到无效矩形。
6. **不检查 `jumpToFrame()` 返回值。** 格式、设备与缓存都可能令跳帧失败。
7. **在自定义绘制中每帧做昂贵缩放。** 优先 `setScaledSize()` 或缓存适配尺寸。
8. **忽略运行时 `error()`。** 资源可在播放中损坏或读取失败，应显示或记录 `lastErrorString()`。

## API 速查表

| API | 作用 | 使用时的语义与边界 |
| --- | --- | --- |
| `MovieState` | 播放状态枚举。 | `NotRunning`、`Paused`、`Running`；状态变化监听 `stateChanged()`。 |
| `CacheMode` | 帧缓存策略枚举。 | 默认 `CacheNone`；`CacheAll` 以内存换取跳帧、回退和顺序设备循环能力。 |
| `QMovie(parent)` | 创建无输入源的 movie。 | 后续用 `setFileName()` 或 `setDevice()` 配置来源；QObject 不可复制。 |
| `QMovie(fileName, format, parent)` | 以文件构造。 | `format` 为空时猜测格式；资源文件路径也可使用。 |
| `QMovie(device, format, parent)` | 以设备构造。 | 设备生命周期与可读状态由调用方保证。 |
| `setFileName()` / `fileName()` | 设置或查询文件来源。 | 当前来源不是文件时 `fileName()` 为空。 |
| `setDevice()` / `device()` | 设置或查询设备来源。 | 只保存设备指针语义；保持它存活且可读。 |
| `setFormat()` / `format()` | 设置或查询解码格式。 | 指定格式可减少探测歧义；空格式表示自动猜测。 |
| `supportedFormats()` | 列出当前支持的动画格式。 | 部署的 imageformat 插件会影响结果。 |
| `isValid()` | 判断数据是否可读且格式受支持。 | 启动前检查；播放期间仍应监听 `error()`。 |
| `lastError()` / `lastErrorString()` | 查询最近一次读图错误。 | `error()` 槽中用于诊断；不要只记录枚举而丢失可读文本。 |
| `start()` | 开始或恢复播放。 | Paused 时恢复；Running 时无操作；依赖对象线程事件循环。 |
| `setPaused(bool)` | 暂停或恢复。 | 暂停保留当前帧并停止帧更新；恢复继续下一帧。 |
| `stop()` | 停止播放。 | 进入 `NotRunning`；下一次 `start()` 从第一帧开始。 |
| `state()` / `stateChanged()` / `started()` | 查询或通知状态转移。 | UI 状态优先响应信号，而不是轮询。 |
| `finished()` | 动画完成循环后通知。 | 只在有限循环完成时处理收尾；无限循环不会自然触发。 |
| `error(ImageReaderError)` | 播放发生错误时通知。 | movie 会停止并进入 `NotRunning`；读取 `lastErrorString()`。 |
| `updated(rect)` | 当前帧的局部区域已更新。 | 自绘控件可 `update(rect)`；`QLabel` 使用时通常无需手动连接。 |
| `frameChanged(number)` | 当前帧号改变。 | 第一帧编号为 0；适合逐帧业务逻辑。 |
| `resized(size)` | 当前帧尺寸发生变化。 | 动画格式可让帧尺寸变化；按需更新控件或缓存。 |
| `currentImage()` / `currentPixmap()` | 取得当前帧副本。 | 像素处理用 `QImage`，GUI 绘制用 `QPixmap`；后者留在 GUI 线程。 |
| `frameRect()` | 返回最近一帧的矩形。 | 尚无首帧时为无效矩形。 |
| `currentFrameNumber()` | 返回当前帧序号。 | 第一帧为 0；在尚未就绪时不要假定为有效业务帧。 |
| `frameCount()` | 返回总帧数。 | 某些格式不支持，返回 0；不是“肯定没有帧”。 |
| `loopCount()` | 返回文件声明的循环次数。 | `0` 单次、`-1` 无限；顺序设备循环需要 `CacheAll`。 |
| `nextFrameDelay()` | 返回到下一帧的建议等待毫秒数。 | 用于观察或调试，不要再用独立定时器竞争推进 movie。 |
| `jumpToFrame()` / `jumpToNextFrame()` | 跳到指定帧或下一帧。 | 返回 `bool`；随机访问能力受格式、设备与缓存限制。 |
| `setScaledSize()` / `scaledSize()` | 配置或读取解码后的帧尺寸。 | 在解码阶段缩放可减少重复绘制成本；避免与显示层二次缩放冲突。 |
| `setSpeed()` / `speed()` | 配置或读取播放速度百分比。 | 默认 100，200 为两倍速度；可通过 `bindableSpeed()` 接入 QProperty 绑定。 |
| `setCacheMode()` / `cacheMode()` | 配置或读取缓存模式。 | 大动画开启 `CacheAll` 前评估内存；可通过 `bindableCacheMode()` 绑定。 |
| `setBackgroundColor()` / `backgroundColor()` | 设置或读取动画背景色。 | 仅对支持背景色的图像格式有效；未设置时返回无效 `QColor`。 |

## 一句话总结

`QMovie` 适合无声音动画图像：将它放入明确的 QObject 所有权树，使用信号驱动显示和状态；顺序设备要循环则缓存所有帧，暂停用 `setPaused()`，停止后重新 `start()` 会从头播放。
