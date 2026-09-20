# QPixmap：面向屏幕显示的像素图

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPixmap>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QPaintDevice`

`QPixmap` 表示一份适合交给 GUI 绘制后端显示的像素图。它和 `QImage` 都能保存图像，但职责不同：`QImage` 面向文件 I/O、像素访问和 CPU 端处理；`QPixmap` 面向屏幕显示，内部可能使用平台相关资源，因此不能简单当成后台线程里的通用像素缓冲。

典型用途包括：

- 给 `QLabel` 设置图片或缩略图。
- 给 `QAbstractButton`、`QToolButton` 或 `QIcon` 提供按钮图标。
- 在 `QWidget::paintEvent()` 中由 `QPainter::drawPixmap()` 绘制。
- 保存经过加载、缩放或绘制后的屏幕资源。
- 在高 DPI 界面中保存带设备像素比的图片。

## 它解决的问题

程序最终要把图像显示到屏幕上时，直接使用 `QPixmap` 通常比先把图像当作普通 CPU 像素数组处理更贴合 Qt 的绘制路径。`QPixmap` 可以由文件、资源系统、内存数据或 `QImage` 创建，也可以通过 `QPainter` 绘制后再交给控件显示。

它不负责以下事情：

- 不提供像 `QImage::bits()` 那样的通用逐像素访问接口。
- 不适合作为解码线程与工作线程之间的主要像素交换格式。
- 不等于一个文件格式；`save()` 输出的是编码后的图片文件，数据流运算符则有自己的序列化格式。
- 不表示绘制命令序列；需要记录和重放绘制命令时使用 `QPicture`。

### `QPixmap`、`QImage`、`QBitmap`、`QPicture` 怎么选

| 类型 | 主要职责 | 适合场景 |
| --- | --- | --- |
| `QImage` | 可访问、可修改的 CPU 端图像数据 | 解码、像素算法、图像处理、后台线程 |
| `QPixmap` | 面向屏幕显示的像素图 | 控件图标、窗口绘制、屏幕缓存 |
| `QBitmap` | 深度为 1 的 `QPixmap` 便利类型 | 单色位图、旧式 mask |
| `QPicture` | 记录并重放 `QPainter` 命令 | 可重复绘制的命令序列 |

常见工作流是：工作线程读取或生成 `QImage`，在 GUI 线程中转换成 `QPixmap`，然后交给控件或 `QPainter`。如果应用使用的是 OpenGL、QRhi 或其他平台绘制路径，还要结合具体绘制后端的线程和资源规则。

## 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Gui Qt6::Widgets)
```

只使用 `QPixmap`、`QPainter` 等 GUI 类型时链接 `Qt6::Gui` 即可；示例中的 `QLabel`、`QPushButton` 等控件还需要 `Qt6::Widgets`。

```cpp
#include <QPixmap>
#include <QPainter>
#include <QWidget>
```

## 最小可用代码

### 从资源加载并显示

```cpp
QPixmap pixmap(":/images/logo.png");
if (pixmap.isNull()) {
    // 文件不存在、格式不受支持或图片解码失败
    return;
}

label->setPixmap(pixmap);
```

构造函数会调用加载逻辑。相对路径相对于运行时工作目录，而 `:/` 路径来自 Qt 资源系统。加载失败时对象成为 null pixmap，必须用 `isNull()` 或返回值检查。

### 在绘制事件中绘制

```cpp
void ImageWidget::paintEvent(QPaintEvent *)
{
    QPainter painter(this);
    painter.drawPixmap(QPoint(10, 10), m_pixmap);
}
```

`QPixmap` 只描述要绘制的图像资源；缩放、裁剪、合成和坐标变换通常由 `QPainter` 或返回新对象的变换 API 完成。

### 生成并绘制一张空白像素图

```cpp
QPixmap pixmap(QSize(320, 200));
pixmap.fill(Qt::transparent); // 构造后数据未初始化，先填充

QPainter painter(&pixmap);
painter.setPen(Qt::white);
painter.drawText(pixmap.rect(), Qt::AlignCenter, "Preview");
```

`QPixmap(int, int)` 和 `QPixmap(QSize)` 创建的像素数据未初始化。开始绘制前应调用 `fill()`，否则未覆盖区域的内容不确定。

## 使用边界

### GUI 资源与线程

`QPixmap` 依赖 GUI 平台实现。应在 GUI 线程创建和使用它，尤其是加载、转换、绘制和与窗口系统交互的操作。后台线程更适合使用 `QImage`，完成处理后把 `QImage` 传回 GUI 线程，再调用 `QPixmap::fromImage()`。

是否允许跨线程传递一个已经存在的 `QPixmap`，还取决于平台和具体操作；即使 C++ 对象可复制，也不应把“可复制”误解成“可以在任意线程安全使用”。不要在工作线程中把 `QPixmap` 当作共享的可变缓存。

### 隐式共享与修改分离

复制 `QPixmap` 通常只复制共享数据的引用，真正修改时 Qt 才分离数据：

```cpp
QPixmap original(":/images/photo.png");
QPixmap copy = original; // 通常是廉价的隐式共享

copy.fill(Qt::black);    // 修改 copy 时分离，original 不变
```

`copy()` 明确返回深拷贝；`detach()` 可显式解除共享。通过 `handle()` 直接调用平台系统函数绕过 Qt 修改数据时，必须先 `detach()`，否则可能修改到多个对象共享的数据。

### 正在绘制时不要修改或滚动

一个 `QPixmap` 上存在活动的 `QPainter` 时，不要调用 `fill()`、`setMask()` 或 `scroll()` 等会改变底层数据的操作。先结束 painter，再进行这些调用：

```cpp
{
    QPainter painter(&pixmap);
    painter.drawLine(0, 0, 20, 20);
} // painter 析构，结束绘制

pixmap.scroll(10, 10, pixmap.rect());
```

## 高 DPI：像素尺寸不等于布局尺寸

`size()`、`width()` 和 `height()` 返回的是底层设备像素数量。例如一张 `200 x 200`、`devicePixelRatio() == 2.0` 的像素图，在界面布局中通常代表 `100 x 100` 个设备无关像素。

```cpp
QPixmap pixmap(":/images/icon@2x.png");
pixmap.setDevicePixelRatio(2.0);

QSizeF logicalSize = pixmap.deviceIndependentSize();
// logicalSize == QSizeF(底层像素宽 / 2, 底层像素高 / 2)
```

`deviceIndependentSize()` 从 Qt 6.2 起提供，语义等价于：

```cpp
QSizeF logicalSize = QSizeF(pixmap.size()) / pixmap.devicePixelRatio();
```

需要注意三件事：

1. `setDevicePixelRatio()` 不会重新采样像素，也不会改变 `size()`；它修改的是解释这些像素的比例。
2. 用 pixmap 尺寸计算控件布局时，应使用 `deviceIndependentSize()`。
3. 如果只是想让绘制内容缩放，通常应设置 painter 的变换或让绘制后端缩放，而不是反复生成缩放后的 pixmap。

## 加载、保存与格式

### 加载来源

可以通过构造函数、`load()` 或 `loadFromData()` 加载。`format == nullptr` 时，Qt 会根据文件名后缀或数据头尝试识别格式；也可以显式传入 `"PNG"`、`"JPG"` 等格式名。

```cpp
QPixmap pixmap;
if (!pixmap.load(":/images/photo.png")) {
    qWarning("load failed");
}

QByteArray encoded = reply->readAll();
QPixmap fromNetwork;
if (!fromNetwork.loadFromData(encoded, "PNG")) {
    qWarning("decode failed");
}
```

`loadFromData(const uchar *, uint, ...)` 只读取给定长度的前 `len` 个字节，调用方必须保证指针在调用期间有效。`QByteArray` 重载更不容易传错长度。

从文件在主线程加载的 pixmap 会自动加入 `QPixmapCache`，但 Qt 使用的内部键不会返回给调用方。需要显式控制缓存键时，应使用 `QPixmapCache`。

### 保存和质量

```cpp
QPixmap pixmap(":/images/photo.png");
pixmap.save("preview.jpg", "JPG", 85);

QByteArray bytes;
QBuffer buffer(&bytes);
buffer.open(QIODevice::WriteOnly);
pixmap.save(&buffer, "PNG");
```

`quality` 为 `-1` 时使用格式默认值；否则应在 `[0, 100]` 范围内。`0` 通常偏向更小的压缩文件，`100` 偏向更高质量。`format == nullptr` 时，文件名重载通常根据后缀选择格式；设备重载没有文件名后缀，最好显式指定格式。

数据流运算符用于 Qt 类型序列化。`operator<<` 把 pixmap 写成 PNG 图像数据，但把该流直接保存成文件并不会得到一个可被图片查看器直接打开的 PNG 文件；要生成图片文件应调用 `save()`。

## 转换、裁剪与变换

### `QImage` 与 `QPixmap`

```cpp
QImage image(":/images/photo.png");
QPixmap pixmap = QPixmap::fromImage(image);

QImage editable = pixmap.toImage();
```

`fromImage(const QImage &)` 将图像转换为适合显示的 pixmap；右值重载在可能时避免额外复制。`convertFromImage()` 则替换当前 pixmap 的数据，并返回转换后是否为非 null。

`toImage()` 可能发生格式转换和数据复制，失败时返回 null `QImage`。返回图像的格式接近底层平台格式，不应假设一定是某个固定的 `QImage::Format`。如果需要稳定的像素格式，应在得到 `QImage` 后显式调用 `convertToFormat()`。

`fromImageReader()` 允许从 `QImageReader` 直接创建 pixmap；某些系统上这样可以比“先读成 `QImage` 再转换”使用更少内存。

### 裁剪和复制

```cpp
QPixmap tile = pixmap.copy(QRect(0, 0, 64, 64));
QPixmap wholeCopy = pixmap.copy(); // 空矩形表示整张图
```

`copy()` 返回深拷贝，不会因为隐式共享而与原对象共同受后续修改影响。矩形超出边界时，实际结果由 Qt 的矩形裁剪语义决定；生产代码应先检查或裁剪输入矩形，避免把无效尺寸误当成业务结果。

### 缩放

```cpp
QPixmap fitted = pixmap.scaled(
    QSize(320, 200),
    Qt::KeepAspectRatio,
    Qt::SmoothTransformation);
```

- `Qt::IgnoreAspectRatio` 允许拉伸到目标宽高。
- `Qt::KeepAspectRatio` 保持比例并放入目标矩形，可能留下空白。
- `Qt::KeepAspectRatioByExpanding` 保持比例并覆盖目标矩形，可能超出目标边界。
- `Qt::FastTransformation` 速度优先。
- `Qt::SmoothTransformation` 质量优先，通常更耗时。

`scaled()` 的空尺寸、零宽或零高会返回 null pixmap；`scaledToWidth()` 和 `scaledToHeight()` 的目标值为零或负数时也会返回 null pixmap。缩放操作返回新对象，不会修改原 pixmap。

如果同一 pixmap 要在 OpenGL 等 painter 上以不断变化的比例绘制，反复调用 `scaled()` 往往不划算，直接对 painter 设置缩放更合适。固定尺寸的列表缩略图则适合预先缩放并缓存。

### 仿射变换

```cpp
QTransform transform;
transform.rotate(30);
QPixmap rotated = pixmap.transformed(transform, Qt::SmoothTransformation);
```

`transformed()` 返回包含全部变换后像素的最小 pixmap，Qt 会内部调整平移部分以避免结果出现不必要的负坐标。`trueMatrix()` 可取得这份实际调整后的矩阵。该操作较慢，因为通常涉及 `QImage` 转换、几何计算和转回 `QPixmap`。

## Alpha、mask 与深度

`hasAlphaChannel()` 只回答像素格式是否支持 alpha 通道；`hasAlpha()` 更宽，它在有 alpha 通道或存在 mask 时都返回 `true`。这两个函数不是“当前是否有任何半透明像素”的逐像素扫描结果。

`QBitmap` 是深度为 1 的 `QPixmap`。`createMaskFromColor()` 根据颜色创建 mask，`Qt::MaskInColor` 会把匹配颜色设为透明，`Qt::MaskOutColor` 会把匹配颜色设为不透明。`createHeuristicMask()` 从边缘颜色推断背景，结果只是启发式的，且会发生 `QImage` 转换和额外计算。

```cpp
QBitmap mask = pixmap.createMaskFromColor(Qt::white, Qt::MaskInColor);
pixmap.setMask(mask);
```

`setMask()` 要求 mask 与 pixmap 尺寸相同；mask 中值为 1 的像素保持原样，值为 0 的像素变透明。传入 null mask 会重置 mask，但此前透明区域会变黑。`mask()` 会从 alpha 数据动态提取 `QBitmap`，可能很昂贵；现代代码优先直接使用 alpha 通道，只有需要旧式位图 mask 或平台兼容时才使用这些 API。

## 状态查询与平台信息

- `isNull()` 表示没有内容、宽高均为零；null pixmap 不能绘制。
- `size()`、`rect()`、`width()`、`height()` 描述底层像素范围。
- `depth()` 返回 bits per pixel；null pixmap 的深度是 0。
- `defaultDepth()` 返回应用默认 pixmap 深度，要求先创建 `QGuiApplication`。
- `isQBitmap()` 判断对象是否实际是 `QBitmap`。
- `cacheKey()` 用于识别当前内容；pixmap 内容改变时 key 会改变。
- `isDetached()` 判断是否已经脱离共享数据；它是低层优化和平台句柄操作辅助，不是业务层对象身份判断。

`cacheKey()` 不是永久对象 ID，也不能用它判断两个 pixmap 是否像素完全相同到任何时刻。由于 `QPixmap` 在 Qt 6.11.1 中明确删除了 `operator==` 和 `operator!=`，需要比较图像内容时通常转为 `QImage` 后按业务规则比较，或比较稳定的文件/资源标识。

## API 逐项说明

### 构造、赋值与共享

#### `QPixmap::QPixmap()`

构造 null pixmap。它没有像素内容，`isNull()` 返回 `true`。

#### `QPixmap::QPixmap(int width, int height)`

按底层像素尺寸构造 pixmap。任一尺寸为 0 时得到 null pixmap；构造出的非 null 像素数据未初始化，绘制前先调用 `fill()`。

#### `explicit QPixmap::QPixmap(const QSize &size)`

`int` 尺寸构造函数的 `QSize` 版本。尺寸为零时得到 null pixmap，像素数据同样未初始化。

#### `QPixmap::QPixmap(const QString &fileName, const char *format = nullptr, Qt::ImageConversionFlags flags = Qt::AutoColor)`

从文件或 Qt 资源路径加载。文件不存在、格式未知或解码失败时得到 null pixmap；相对路径依赖运行时工作目录。

#### `explicit QPixmap::QPixmap(const char *const xpm[])`

从有效的 XPM 数组构造。XPM 无效时错误会被静默忽略，因此仍应检查 `isNull()`。该构造受 `QT_NO_IMAGEFORMAT_XPM` 配置影响。

#### `QPixmap::QPixmap(const QPixmap &pixmap)`

复制 pixmap。通常采用隐式共享，复制本身廉价；后续修改会触发写时分离。

#### `QPixmap::QPixmap(QPixmap &&other) noexcept`

移动构造，转移内部共享数据。移动后的 `other` 仍是有效对象，但不应依赖它保留原来的图像内容。

#### `QPixmap::~QPixmap()`

销毁 pixmap 对象并释放其对共享平台资源的引用。

#### `QPixmap &QPixmap::operator=(const QPixmap &pixmap)`

复制赋值，采用隐式共享。赋值后目标引用与源相同的内容，任一方后续修改会适时分离。

#### `QPixmap &QPixmap::operator=(QPixmap &&other) noexcept`

移动赋值，转移内部数据，适合把函数返回的临时 pixmap 高效交给已有对象。

#### `void QPixmap::swap(QPixmap &other) noexcept`

交换两个 pixmap 的内部数据。操作很快且不会失败，适合实现高效替换。

#### `bool QPixmap::operator!() const`

等价于 `isNull()`，对象为 null pixmap 时返回 `true`。

#### `operator QVariant() const`

把 pixmap 包装成 `QVariant`，适合与属性系统、模型数据或通用 Qt 容器协作。

#### `bool QPixmap::operator==(const QPixmap &) const = delete`

Qt 6.11.1 中明确删除相等比较运算符，不能直接写 `pixmap1 == pixmap2`。

#### `bool QPixmap::operator!=(const QPixmap &) const = delete`

Qt 6.11.1 中明确删除不等比较运算符，不能直接写 `pixmap1 != pixmap2`。

### 尺寸、格式与状态

#### `bool QPixmap::isNull() const`

返回 pixmap 是否没有内容。null pixmap 的宽、高为 0，不能作为绘制源。

#### `int QPixmap::width() const`

返回底层像素宽度，不是高 DPI 下的设备无关宽度。

#### `int QPixmap::height() const`

返回底层像素高度，不是高 DPI 下的设备无关高度。

#### `QSize QPixmap::size() const`

返回底层像素尺寸。用于 UI 布局时要结合 `devicePixelRatio()` 或直接使用 `deviceIndependentSize()`。

#### `QRect QPixmap::rect() const`

返回包围 pixmap 的矩形，通常是从 `(0, 0)` 开始、尺寸为 `size()` 的矩形。

#### `int QPixmap::depth() const`

返回每像素位数；null pixmap 返回 0。

#### `int QPixmap::defaultDepth()`

返回应用默认 pixmap 深度，实际取主屏幕深度。调用前必须已经创建 `QGuiApplication`。

#### `bool QPixmap::hasAlpha() const`

如果 pixmap 有 alpha 通道或 mask，返回 `true`。它不保证存在非 0 且非 255 的半透明像素。

#### `bool QPixmap::hasAlphaChannel() const`

如果底层像素格式支持 alpha 通道，返回 `true`。仅有 mask 也不一定使该函数返回 `true`。

#### `bool QPixmap::isQBitmap() const`

判断当前对象是否实际表示 `QBitmap`，而不是普通深度 pixmap。

#### `qreal QPixmap::devicePixelRatio() const`

返回设备像素与设备无关像素的比例，默认值为 `1.0`。

#### `void QPixmap::setDevicePixelRatio(qreal scaleFactor)`

设置设备像素比。它不重新缩放像素；会影响在该 pixmap 上打开的 `QPainter` 的有效坐标范围，也会影响 Qt 根据 pixmap 尺寸进行的布局计算。业务代码应传入正的、有效的比例值。

#### `QSizeF QPixmap::deviceIndependentSize() const`

返回设备无关尺寸，等价于 `size() / devicePixelRatio()`。该 API 从 Qt 6.2 起提供，适合 UI 尺寸计算。

#### `qint64 QPixmap::cacheKey() const`

返回标识当前内容的 key。内容发生改变时 key 会改变；它适合检测缓存内容变化，不是跨进程持久化键。

#### `bool QPixmap::isDetached() const`

返回是否已经脱离共享平台数据。普通业务代码通常不需要主动判断它。

#### `void QPixmap::detach()`

主动脱离共享数据。Qt 在大多数修改操作和 `QPainter::begin()` 时会自动分离；如果通过平台句柄或系统调用直接修改底层资源，则应先显式调用。

#### `QPlatformPixmap *QPixmap::handle() const`

返回平台 pixmap 句柄。它属于低层平台集成接口，依赖平台实现，不应作为普通业务 API 使用。通过句柄修改底层内容前要先 `detach()`，并确认当前平台和线程规则。

#### `int QPixmap::devType() const`

返回 `QPaintDevice` 类型标识，通常用于 Qt 内部绘制后端识别。应用层通常不需要根据该值分支。

#### `QPaintEngine *QPixmap::paintEngine() const`

返回用于在 pixmap 上绘制的 `QPaintEngine`。通常由 `QPainter` 间接使用，不建议业务代码直接操纵。

### 填充、转换与裁剪

#### `void QPixmap::fill(const QColor &color = Qt::white)`

用颜色填充整张 pixmap。pixmap 正由 painter 绘制时调用的效果未定义；应先结束 painter。

#### `QPixmap QPixmap::fromImage(const QImage &image, Qt::ImageConversionFlags flags = Qt::AutoColor)`

把 `QImage` 转成面向显示的 pixmap。`flags` 控制颜色和格式转换；单色或 8 位图可能先转为 32 位 pixmap，若只需要 1 位 bitmap 可考虑 `QBitmap::fromImage()`。

#### `QPixmap QPixmap::fromImage(QImage &&image, Qt::ImageConversionFlags flags = Qt::AutoColor)`

右值版本，在可能时直接复用 `QImage` 的数据，减少复制。它仍可能因为平台格式要求而进行转换。

#### `QPixmap QPixmap::fromImageReader(QImageReader *imageReader, Qt::ImageConversionFlags flags = Qt::AutoColor)`

从 `QImageReader` 直接读取并创建 pixmap。指针必须指向有效的 reader；reader 的打开状态、格式插件和错误状态由调用方负责。

#### `bool QPixmap::convertFromImage(const QImage &image, Qt::ImageConversionFlags flags = Qt::AutoColor)`

用转换后的 `image` 替换当前 pixmap 数据。返回转换结果是否为非 null pixmap；失败后不要继续假设旧内容仍然存在。

#### `QImage QPixmap::toImage() const`

把 pixmap 转为 `QImage`。转换失败返回 null image；结果格式接近底层系统格式，不能假定固定为某个 `QImage::Format`。当前文档还指出，单色图的 alpha mask 不纳入转换结果。

#### `QPixmap QPixmap::copy(const QRect &rectangle = QRect()) const`

返回指定矩形的深拷贝。传入空矩形表示复制整张 pixmap。需要独立内容时使用它，而不是只做普通复制赋值。

#### `QPixmap QPixmap::copy(int x, int y, int width, int height) const`

按坐标和尺寸裁剪并返回深拷贝，等价于传入 `QRect(x, y, width, height)`。

### 文件与内存 I/O

#### `bool QPixmap::load(const QString &fileName, const char *format = nullptr, Qt::ImageConversionFlags flags = Qt::AutoColor)`

加载文件或资源中的 pixmap。成功返回 `true`；失败时会使对象失效并返回 `false`。主线程从文件加载时 Qt 可能自动加入 `QPixmapCache`。

#### `bool QPixmap::loadFromData(const uchar *data, uint len, const char *format = nullptr, Qt::ImageConversionFlags flags = Qt::AutoColor)`

从内存中前 `len` 个字节加载。指针和长度必须匹配，数据在函数返回前保持有效；失败会使 pixmap 失效。

#### `bool QPixmap::loadFromData(const QByteArray &data, const char *format = nullptr, Qt::ImageConversionFlags flags = Qt::AutoColor)`

从 `QByteArray` 加载，Qt 根据其长度读取数据。相比裸指针重载更不容易出现长度错误；失败同样会使 pixmap 失效。

#### `bool QPixmap::save(const QString &fileName, const char *format = nullptr, int quality = -1) const`

按指定格式保存到文件。`format == nullptr` 时根据文件名后缀选择格式；`quality` 应为 `-1` 或 `[0, 100]`；成功返回 `true`。

#### `bool QPixmap::save(QIODevice *device, const char *format = nullptr, int quality = -1) const`

把 pixmap 编码写入已准备好的 `QIODevice`。没有文件名后缀可供推断时，建议显式给出 `format`；设备的打开模式和写入错误由调用方检查。

### 缩放与几何变换

#### `QPixmap QPixmap::scaled(const QSize &size, Qt::AspectRatioMode aspectRatioMode = Qt::IgnoreAspectRatio, Qt::TransformationMode transformMode = Qt::FastTransformation) const`

按目标尺寸返回缩放副本。空尺寸返回 null pixmap；宽高比由 `aspectRatioMode` 控制，采样质量由 `transformMode` 控制。

#### `QPixmap QPixmap::scaled(int width, int height, Qt::AspectRatioMode aspectRatioMode = Qt::IgnoreAspectRatio, Qt::TransformationMode transformMode = Qt::FastTransformation) const`

按整数宽高缩放，任一参数为零或负数时返回 null pixmap。它是 `QSize` 重载的便捷形式。

#### `QPixmap QPixmap::scaledToWidth(int width, Qt::TransformationMode mode = Qt::FastTransformation) const`

固定宽度并按原比例计算高度。宽度为零或负数时返回 null pixmap。

#### `QPixmap QPixmap::scaledToHeight(int height, Qt::TransformationMode mode = Qt::FastTransformation) const`

固定高度并按原比例计算宽度。高度为零或负数时返回 null pixmap。

#### `QPixmap QPixmap::transformed(const QTransform &transform, Qt::TransformationMode mode = Qt::FastTransformation) const`

返回应用矩阵后的新 pixmap，原对象不变。Qt 会平移结果以得到包含所有变换后点的最小图像；该操作较慢，适合低频或预处理。

#### `QTransform QPixmap::trueMatrix(const QTransform &matrix, int width, int height)`

返回 `transformed()` 实际使用的、已经补偿平移的矩阵。需要把原坐标映射到变换后 pixmap 坐标时使用它。

### mask 与滚动

#### `QBitmap QPixmap::mask() const`

从 alpha 通道动态提取 bitmap mask。可能很昂贵；不要在高频绘制循环中反复调用。

#### `void QPixmap::setMask(const QBitmap &mask)`

把 mask 与 pixmap alpha 合并。mask 必须与 pixmap 尺寸相同；传入 null mask 会重置 mask。pixmap 正在被 painter 使用时调用效果未定义，而且该操作可能昂贵。

#### `QBitmap QPixmap::createHeuristicMask(bool clipTight = true) const`

根据边缘颜色推断背景并生成启发式 mask。结果不保证完美；函数涉及图像转换和计算，`clipTight` 决定 mask 是否紧贴数据像素。

#### `QBitmap QPixmap::createMaskFromColor(const QColor &maskColor, Qt::MaskMode mode = Qt::MaskInColor) const`

按颜色创建 mask。`MaskInColor` 使匹配颜色透明，`MaskOutColor` 使匹配颜色不透明；该操作可能因转换为 `QImage` 而较慢。

#### `void QPixmap::scroll(int dx, int dy, const QRect &rect, QRegion *exposed = nullptr)`

把 `rect` 区域内的内容平移 `(dx, dy)`，被移出后留下的 exposed 区域保持不变。`exposed` 若指向空的 `QRegion`，Qt 会把受影响的空白区域写入其中。pixmap 上有活动 painter 时不能调用。

#### `void QPixmap::scroll(int dx, int dy, int x, int y, int width, int height, QRegion *exposed = nullptr)`

`scroll(QRect(...))` 的坐标便捷重载，其他语义和活动 painter 限制相同。

### 相关非成员

#### `QDataStream &operator<<(QDataStream &, const QPixmap &)`

把 pixmap 以 PNG 图像形式写入数据流。流文件不是普通图片文件；需要生成独立图片时使用 `save()`。

#### `QDataStream &operator>>(QDataStream &, QPixmap &)`

从数据流读取图像并写入目标 pixmap。数据流版本、格式和读写错误应由调用方统一管理。

#### `QDebug operator<<(QDebug, const QPixmap &)`

在启用 debug stream 时输出 pixmap 的调试表示，适合日志和诊断，不是图片编码接口。

## 常见错误排查

1. **图片显示为空**：先检查 `isNull()`，再检查资源路径、运行时工作目录、图片插件和 `load()` 返回值。
2. **后台线程崩溃或平台警告**：后台线程用 `QImage`，在 GUI 线程转换为 `QPixmap`。
3. **生成的空白图出现随机内容**：尺寸构造后忘记 `fill()`，导致使用未初始化像素。
4. **高 DPI 图标变得过大**：把底层 `size()` 当作布局尺寸，改用 `deviceIndependentSize()` 并正确设置设备像素比。
5. **缩放结果变形或模糊**：检查 `KeepAspectRatio`、`SmoothTransformation` 和是否应该由 painter 直接缩放。
6. **调用 `scroll()` 或 `fill()` 后结果异常**：确认没有活动 `QPainter`，并在必要时先结束绘制作用域。
7. **mask 操作很慢**：`mask()`、`setMask()` 和颜色 mask 可能触发图像转换；优先使用 alpha 通道并缓存结果。
8. **尝试比较两个 pixmap**：Qt 6.11.1 删除了 `operator==`/`operator!=`；按业务选择资源 key、`cacheKey()` 或转换为 `QImage` 后比较。

## API 速查表

| 类别 | API | 作用 | 关键边界与注意事项 |
| --- | --- | --- | --- |
| 构造 | `QPixmap()` | 创建 null pixmap | `isNull()` 为 `true`，不能绘制 |
| 构造 | `QPixmap(int, int)` | 按像素尺寸创建 pixmap | 任一尺寸为 0 得到 null；数据未初始化，先 `fill()` |
| 构造 | `QPixmap(QSize)` | 按 `QSize` 创建 pixmap | 同样是底层像素尺寸，数据未初始化 |
| 构造 | `QPixmap(QString, format, flags)` | 从文件或资源加载 | 失败得到 null pixmap；相对路径依赖工作目录 |
| 构造 | `QPixmap(const char *const[])` | 从 XPM 数组加载 | XPM 无效时错误可能静默忽略；受 XPM 配置影响 |
| 构造/赋值 | 拷贝、移动构造与 `operator=` | 复制或转移 pixmap | 普通复制采用隐式共享；移动后源对象不保留原内容 |
| 构造/赋值 | `swap(QPixmap &) noexcept` | 交换底层数据 | 很快且不会失败 |
| 状态 | `isNull()` / `operator!()` | 判断是否无内容 | null pixmap 宽高为 0，不能绘制 |
| 状态 | `width()` / `height()` / `size()` / `rect()` | 查询底层像素几何 | 高 DPI 布局不要直接当设备无关尺寸 |
| 状态 | `depth()` | 查询 bits per pixel | null pixmap 返回 0 |
| 状态 | `defaultDepth()` | 查询应用默认深度 | 需先创建 `QGuiApplication` |
| 状态 | `hasAlpha()` | 判断是否有 alpha 或 mask | 不等于扫描确认存在半透明像素 |
| 状态 | `hasAlphaChannel()` | 判断格式是否支持 alpha 通道 | 只有 mask 不一定为 `true` |
| 状态 | `isQBitmap()` | 判断是否实际为 `QBitmap` | 只用于类型/平台兼容判断 |
| 状态 | `cacheKey()` | 获取当前内容标识 | 内容改变会变化；不是持久化对象 ID |
| 共享 | `isDetached()` / `detach()` | 查询或主动解除隐式共享 | 通过平台句柄直接修改前应先 `detach()` |
| 平台 | `handle()` | 获取平台 pixmap 句柄 | 低层接口，平台和线程限制强，不宜常规使用 |
| 绘制设备 | `devType()` / `paintEngine()` | 提供 `QPaintDevice` 后端信息 | 通常由 Qt 和 `QPainter` 内部使用 |
| 填充 | `fill(QColor)` | 填充整张 pixmap | 活动 painter 存在时效果未定义 |
| 转换 | `fromImage(const QImage &, flags)` | `QImage` 转 `QPixmap` | 可能发生格式转换和复制 |
| 转换 | `fromImage(QImage &&, flags)` | 右值图像转 pixmap | 在可能时减少复制，但不保证零拷贝 |
| 转换 | `fromImageReader(QImageReader *, flags)` | 从 reader 直接创建 pixmap | reader 指针和错误状态由调用方管理 |
| 转换 | `convertFromImage(QImage, flags)` | 替换当前 pixmap 数据 | 返回是否得到非 null pixmap；失败后对象可能失效 |
| 转换 | `toImage()` | 转换为 `QImage` | 可能复制；失败返回 null image，格式不固定 |
| 裁剪 | `copy(QRect)` / `copy(x, y, w, h)` | 返回区域深拷贝 | 空矩形表示整图；输入矩形应自行校验 |
| I/O | `load(fileName, format, flags)` | 从文件或资源加载 | 失败返回 `false` 并使对象失效 |
| I/O | `loadFromData(uchar *, len, ...)` | 从裸内存加载 | 指针和长度必须匹配且在调用期间有效 |
| I/O | `loadFromData(QByteArray, ...)` | 从字节数组加载 | 更不易传错长度；失败使对象失效 |
| I/O | `save(fileName, format, quality)` | 编码保存到文件 | `quality` 为 `-1` 或 `[0,100]`；默认格式按后缀 |
| I/O | `save(QIODevice *, format, quality)` | 编码写入设备 | 无后缀时显式指定格式；检查设备写入错误 |
| 缩放 | `scaled(QSize, aspect, mode)` | 返回目标尺寸缩放副本 | 空尺寸返回 null；确认宽高比和采样模式 |
| 缩放 | `scaled(w, h, aspect, mode)` | 整数尺寸缩放 | 任一尺寸非正返回 null |
| 缩放 | `scaledToWidth(w, mode)` | 固定宽度等比缩放 | 非正宽度返回 null |
| 缩放 | `scaledToHeight(h, mode)` | 固定高度等比缩放 | 非正高度返回 null |
| 变换 | `transformed(QTransform, mode)` | 返回变换后的最小包围 pixmap | 较慢；原图不变，内部会补偿平移 |
| 变换 | `trueMatrix(QTransform, w, h)` | 获取实际变换矩阵 | 用于原坐标到变换结果坐标的映射 |
| Alpha/mask | `mask()` | 从 alpha 提取 `QBitmap` | 可能昂贵，避免高频重复调用 |
| Alpha/mask | `setMask(QBitmap)` | 合并位图 mask 与 alpha | 尺寸必须相同；活动 painter 时不要调用 |
| Alpha/mask | `createHeuristicMask(clipTight)` | 启发式推断背景 mask | 不保证完美，涉及图像转换和计算 |
| Alpha/mask | `createMaskFromColor(color, mode)` | 按颜色生成 mask | `MaskInColor`/`MaskOutColor` 语义相反，操作可能较慢 |
| 滚动 | `scroll(dx, dy, QRect, exposed)` | 平移区域内容并报告暴露区 | pixmap 上有活动 painter 时不能调用 |
| 滚动 | `scroll(dx, dy, x, y, w, h, exposed)` | `QRect` 版本便捷重载 | 与矩形重载相同 |
| 高 DPI | `devicePixelRatio()` | 查询设备像素比 | 默认 1.0；用于布局计算时参与换算 |
| 高 DPI | `setDevicePixelRatio(qreal)` | 设置设备像素比 | 不重采样像素，只改变显示/布局解释 |
| 高 DPI | `deviceIndependentSize()` | 查询设备无关尺寸 | Qt 6.2 起提供，优先用于 UI 布局 |
| 序列化 | `operator<<(QDataStream &, QPixmap)` | 以 PNG 图像写入流 | 流文件本身不是直接可打开的图片文件 |
| 序列化 | `operator>>(QDataStream &, QPixmap &)` | 从流读取 pixmap | 注意流版本和读写错误 |
| 调试 | `operator<<(QDebug, QPixmap)` | 输出调试表示 | 仅用于日志，不是编码保存 |
| 比较 | `operator==` / `operator!=` | 无可用实现 | Qt 6.11.1 中明确删除，不能直接比较 |

### 一句话总结

`QPixmap` 是面向屏幕显示的像素资源：用 `QImage` 做后台处理，用 `QPixmap` 做 GUI 绘制；牢记 null、未初始化像素、隐式共享、高 DPI 和活动 painter 这几个边界，绝大多数问题都能在接口层提前避免。
