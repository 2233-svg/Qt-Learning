# QPixmap

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 面向屏幕显示优化的像素图，负责控件图标、窗口显示和与平台绘制资源的交互。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QPixmap`：面向屏幕显示优化的像素图，负责控件图标、窗口显示和与平台绘制资源的交互。

**内部模型：** 绘制对象维护一组状态：画笔、画刷、字体、变换、裁剪、合成模式和渲染提示。每次 draw 调用都会使用当前状态；坐标通常经过当前 transform 映射到目标设备。

**适用场景：** 开始绘制后配置必要状态，使用 save/restore 包围局部变换，按设备坐标绘制，结束时让上下文析构或调用 end。绘制文本和图片时同时考虑字体度量、devicePixelRatio、裁剪和性能。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要直接调用 paintEvent；不要在绘制函数里修改会再次触发绘制的状态；不要假定所有图像都是四字节像素；不要忘记 transform 会影响坐标和 boundingRect。

## 2. 依赖与对象关系

- 头文件：`#include <QPixmap>`
- 继承自：QPaintDevice
- 直接派生类：QBitmap

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

绘制对象维护一组状态：画笔、画刷、字体、变换、裁剪、合成模式和渲染提示。每次 draw 调用都会使用当前状态；坐标通常经过当前 transform 映射到目标设备。

### 状态、生命周期和线程

**生命周期：** 绘制上下文必须绑定有效的 paint device，并在合法的绘制阶段使用。QWidget 上通常只在 `paintEvent()` 内创建 painter；离屏图像、打印设备和 pixmap 则有各自的设备生命周期。

**状态与结果：** `save()`/`restore()` 用于隔离局部状态；改变坐标系、画笔或合成模式后要么恢复，要么明确后续绘制也需要该状态。重绘请求和真正绘制是两个阶段，业务状态变化应调用 `update()`。

**线程与事件循环：** 同一个 GUI 控件的绘制在 GUI 线程完成；离屏 QImage 可以按数据所有权在后台处理，但不要让后台线程直接绘制或访问正在显示的 QWidget/QPixmap 资源。

## 3. 直接使用

开始绘制后配置必要状态，使用 save/restore 包围局部变换，按设备坐标绘制，结束时让上下文析构或调用 end。绘制文本和图片时同时考虑字体度量、devicePixelRatio、裁剪和性能。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

```cpp
void Widget::paintEvent(QPaintEvent *)
{
    QPainter painter(this);
    painter.save();
    // 设置画笔、画刷、字体或变换后进行绘制
    painter.restore();
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QPixmap()`
- `QPixmap(const char *const[] xpm)`
- `QPixmap(int width, int height)`
- `QPixmap(const QString &fileName, const char *format = nullptr, Qt::ImageConversionFlags flags = Qt::AutoColor)`
- `QPixmap(const QSize &size)`
- `QPixmap(const QPixmap &pixmap)`
- `QPixmap(QPixmap &&other)`
- `virtual ~QPixmap()`
- `qint64 cacheKey() const`
- `bool convertFromImage(const QImage &image, Qt::ImageConversionFlags flags = Qt::AutoColor)`
- `QPixmap copy(const QRect &rectangle = QRect()) const`
- `QPixmap copy(int x, int y, int width, int height) const`
- `QBitmap createHeuristicMask(bool clipTight = true) const`
- `QBitmap createMaskFromColor(const QColor &maskColor, Qt::MaskMode mode = Qt::MaskInColor) const`
- `int depth() const`
- `void detach()`
- `(since 6.2) QSizeF deviceIndependentSize() const`
- `qreal devicePixelRatio() const`
- `void fill(const QColor &color = Qt::white)`
- `bool hasAlpha() const`
- `bool hasAlphaChannel() const`
- `int height() const`
- `bool isNull() const`
- `bool isQBitmap() const`
- `bool load(const QString &fileName, const char *format = nullptr, Qt::ImageConversionFlags flags = Qt::AutoColor)`
- `bool loadFromData(const uchar *data, uint len, const char *format = nullptr, Qt::ImageConversionFlags flags = Qt::AutoColor)`
- `bool loadFromData(const QByteArray &data, const char *format = nullptr, Qt::ImageConversionFlags flags = Qt::AutoColor)`
- `QBitmap mask() const`
- `QRect rect() const`
- `bool save(const QString &fileName, const char *format = nullptr, int quality = -1) const`
- `bool save(QIODevice *device, const char *format = nullptr, int quality = -1) const`
- `QPixmap scaled(const QSize &size, Qt::AspectRatioMode aspectRatioMode = Qt::IgnoreAspectRatio, Qt::TransformationMode transformMode = Qt::FastTransformation) const`
- `QPixmap scaled(int width, int height, Qt::AspectRatioMode aspectRatioMode = Qt::IgnoreAspectRatio, Qt::TransformationMode transformMode = Qt::FastTransformation) const`
- `QPixmap scaledToHeight(int height, Qt::TransformationMode mode = Qt::FastTransformation) const`
- `QPixmap scaledToWidth(int width, Qt::TransformationMode mode = Qt::FastTransformation) const`
- `void scroll(int dx, int dy, const QRect &rect, QRegion *exposed = nullptr)`
- `void scroll(int dx, int dy, int x, int y, int width, int height, QRegion *exposed = nullptr)`
- `void setDevicePixelRatio(qreal scaleFactor)`
- `void setMask(const QBitmap &mask)`
- `QSize size() const`
- `void swap(QPixmap &other)`
- `QImage toImage() const`
- `QPixmap transformed(const QTransform &transform, Qt::TransformationMode mode = Qt::FastTransformation) const`
- `int width() const`
- `operator QVariant() const`
- `bool operator!() const`
- `QPixmap & operator=(QPixmap &&other)`
- `QPixmap & operator=(const QPixmap &pixmap)`

### 静态公有成员

- `int defaultDepth()`
- `QPixmap fromImage(const QImage &image, Qt::ImageConversionFlags flags = Qt::AutoColor)`
- `QPixmap fromImage(QImage &&image, Qt::ImageConversionFlags flags = Qt::AutoColor)`
- `QPixmap fromImageReader(QImageReader *imageReader, Qt::ImageConversionFlags flags = Qt::AutoColor)`
- `QTransform trueMatrix(const QTransform &matrix, int width, int height)`

### 相关非成员函数

- `QDataStream & operator<<(QDataStream &stream, const QPixmap &pixmap)`
- `QDataStream & operator>>(QDataStream &stream, QPixmap &pixmap)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QPixmap::QPixmap()`

**作用与语义：**

构建一个空像素映射。

### `[explicit] QPixmap::QPixmap(const char *const[] xpm)`

**作用与语义：**

从给定的`xpm`数据构建像素映射，该数据必须是有效的XPM图像。
错误被默默忽略。
请注意，可以通过使用一个不寻常的声明来稍微压缩 XPM 变量：
额外的`const`使整个定义变成只读，这在代码共享库中时效率略高，且在应用需要存储在ROM中时可以实现ROM。

**官方示例：**

```cpp
 static const char * const start_xpm[] = {
     "16 15 8 1",
     "a c #cec6bd",
     // etc.
 };
```

### `QPixmap::QPixmap(int width, int height)`

**作用与语义：**

构造一个像素映射，其`width`和`height`。如果`width`或`height`为零，则构造一个空像素映射。
警告：这将生成一个包含未初始化数据的QPixmap。请先调用`fill()`，先用合适的颜色填充像素地图，然后再用`QPainter`绘制。

### `QPixmap::QPixmap(const QString &fileName, const char *format = nullptr, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**作用与语义：**

从给定`fileName`的文件构建像素映射。如果文件不存在或格式未知，像素映射将成为空像素映射。
加载器尝试使用指定的`format`读取像素映射。如果未指定`format`（这是默认），加载器会探测文件头部以猜测文件格式。
文件名可以指磁盘上的实际文件，也可以指应用程序的嵌入式资源之一。有关如何将镜像和其他资源文件嵌入应用程序可执行文件的详细信息，请参见资源系统概述。
如果图像需要修改以适应较低分辨率的结果（例如从32位转换为8位），使用`flags`来控制转换。
`fileName`、`format`和`flags`参数会传递给`load()`。这意味着`fileName`中的数据不会被编译成二进制。如果`fileName`包含相对路径（例如仅文件名），相关文件必须相对于运行时工作目录找到。

### `[explicit] QPixmap::QPixmap(const QSize &size)`

**作用与语义：**

构建给定`size`的像素图。
警告：这将创建一个包含未初始化数据的QPixmap。请调用`fill()`，在用`QPainter`绘制前填充像素图的颜色。

### `QPixmap::QPixmap(const QPixmap &pixmap)`

**作用与语义：**

构建一个像素映射，该映射是给定`pixmap`的副本。

### `[noexcept] QPixmap::QPixmap(QPixmap &&other)`

**作用与语义：**

Move-构造一个QPixmap实例，`other`。

### `[virtual noexcept] QPixmap::~QPixmap()`

**作用与语义：**

毁掉像素地图。

### `qint64 QPixmap::cacheKey() const`

**作用与语义：**

返回一个识别该`QPixmap`的数字。不同的`QPixmap`对象只有在引用相同内容时，才能拥有相同的缓存键。
当pixmap被修改时，cacheKey()也会改变。

### `bool QPixmap::convertFromImage(const QImage &image, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**作用与语义：**

用指定`flags`控制转换，将该像素映射的数据替换为给定的 `image`。`flags` 参数是 `Qt::ImageConversionFlags` 的逐位或。传递 0 表示 `flags` 会设置所有默认选项。如果结果是该像素映射不是空的，则返回 `true`。

### `QPixmap QPixmap::copy(const QRect &rectangle = QRect()) const`

**作用与语义：**

返回由给定`rectangle`指定的像素映射子集的深度副本。有关深度副本的更多信息，请参见隐式数据共享文档。
如果给定的`rectangle`为空，则复制整个图像。

### `QPixmap QPixmap::copy(int x, int y, int width, int height) const`

**作用与语义：**

返回由矩形`QRect`（`x`， `y`， `width`， `height`）指定的像素映射子集的深度副本。

### `QBitmap QPixmap::createHeuristicMask(bool clipTight = true) const`

**作用与语义：**

为该像素图创建并返回启发式遮罩。
该函数的工作原理是从某个角落选择颜色，然后从所有边缘开始逐个削减该颜色的像素。如果`clipTight`为真（默认），遮罩的大小刚好足够覆盖这些像素;否则，遮罩会大于数据像素。
面罩可能不完美，但应该合理，所以你可以做以下事情：
该函数较慢，因为它涉及与`QImage`的转换和非平凡的计算。

**官方示例：**

```cpp
 QPixmap myPixmap;
 myPixmap.setMask(myPixmap.createHeuristicMask());
```

### `QBitmap QPixmap::createMaskFromColor(const QColor &maskColor, Qt::MaskMode mode = Qt::MaskInColor) const`

**作用与语义：**

根据给定的 `maskColor` 创建并返回该像素映射的遮罩。如果`mode`是`Qt::MaskInColor`，所有匹配 maskColor 的像素都是透明的。如果 `mode` `Qt::MaskOutColor`，所有匹配 maskColor 的像素都是不透明的。
这个功能比较慢，因为它涉及从`QImage`转换或转换。

### `[static] int QPixmap::defaultDepth()`

**作用与语义：**

返回应用程序默认使用的像素映射深度。
所有平台上，主屏幕的深度都会恢复。
注意：必须在调用此函数前创建`QGuiApplication`。

### `int QPixmap::depth() const`

**作用与语义：**

返回像素地图的深度。
像素图深度也称为像素比特数（bpp）或像素图的位平面数。空像素图的深度为0。

### `void QPixmap::detach()`

**作用与语义：**

将像素地图与共享像素地图数据分离。
每当像素映射内容即将发生变化时，Qt会自动将其分离。几乎所有修改像素映射的`QPixmap`成员函数（`fill()`、`fromImage()`、`load()`等）都实现了这一点，像素映射`QPainter::begin()`也实现了这一点。
有两个例外情况，必须显式调用 detach() ，即调用 handle() 或 x11PictureHandle() 函数（仅在 X11 上可用）。否则，任何通过系统调用进行的修改都会对共享数据进行。
如果只有一个引用或像素映射尚未初始化，detach() 函数会立即返回。

### `[since 6.2] QSizeF QPixmap::deviceIndependentSize() const`

**作用与语义：**

返回像素图的大小（设备无关像素）。
在使用像素地图大小计算用户界面尺寸时，应使用该值。
返回值等同于像素地图。`size()` / 像素地图。`devicePixelRatio()`。

### `qreal QPixmap::devicePixelRatio() const`

**作用与语义：**

返回pixmap的设备像素比。这是设备像素与设备无关像素之间的比值。
在基于像素地图大小计算布局几何时使用该函数：`QSize` layoutSize = 图像。`size()` / image.devicePixelRatio()。
默认值是1.0。

### `void QPixmap::fill(const QColor &color = Qt::white)`

**作用与语义：**

用给定的 `color` 填充像素图。
当绘制像素地图时，该函数的效果是未定义的。

### `[static] QPixmap QPixmap::fromImage(const QImage &image, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**作用与语义：**

利用指定的`flags`将给定`image`转换为像素映射以控制转换。`flags`参数是`Qt::ImageConversionFlags`的位或。传递0作为`flags`设置所有默认选项。
对于单色和8位图像，图像首先转换为32位像素图，然后填充颜色表中的颜色。如果这操作成本过高，你可以用`QBitmap::fromImage()`代替。

### `[static] QPixmap QPixmap::fromImage(QImage &&image, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**作用与语义：**

如果可能的话，将给定`image`转换为像素图，避免复制。

### `[static] QPixmap QPixmap::fromImageReader(QImageReader *imageReader, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**作用与语义：**

从直接从`imageReader`读取的图像创建一个`QPixmap`。`flags`参数是`Qt::ImageConversionFlags`的位或。传递0作为`flags`会设置所有默认选项。
在某些系统上，直接将图像读取到`QPixmap`比读取`QImage`转换为`QPixmap`更节省内存。

### `bool QPixmap::hasAlpha() const`

**作用与语义：**

如果该像素图有alpha通道或有掩码，返回`true`，否则返回`false`。

### `bool QPixmap::hasAlphaChannel() const`

**作用与语义：**

如果像素图格式尊重阿尔法通道，返回`true`;否则返回`false`。

### `int QPixmap::height() const`

**作用与语义：**

返回像素地图的高度。

### `bool QPixmap::isNull() const`

**作用与语义：**

如果是空像素映射，则返回`true`;否则返回 `false`。
空像素图没有宽度、高度为零且没有内容。你不能在空像素图中绘制。

### `bool QPixmap::isQBitmap() const`

**作用与语义：**

如果是`QBitmap`，返回`true`;否则返回`false`。

### `bool QPixmap::load(const QString &fileName, const char *format = nullptr, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**作用与语义：**

从带有指定 `fileName` 的文件加载像素映射。如果像素映射成功加载，则返回 true;否则 返回像素映射并返回 `false`。
加载器尝试使用指定的 `format` 读取像素映射。如果未指定`format`（这是默认），加载器会探测文件的头部以猜测文件格式。
文件名可以指磁盘上的实际文件，也可以指应用程序的嵌入式资源之一。有关如何将像素映射和其他资源文件嵌入应用程序可执行文件的详细信息，请参见资源系统概述。
如果需要修改数据以适应较低分辨率的结果（例如从32位转换为8位），使用`flags`来控制转换。
注意，QPixmaps 在主线程文件加载时会自动添加到`QPixmapCache`中;所使用的密钥是内部的，无法获取。

### `bool QPixmap::loadFromData(const uchar *data, uint len, const char *format = nullptr, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**作用与语义：**

从给定二进制`data`的`len`前字节加载像素映射。如果像素映射成功加载，返回`true`;否则使像素映射失效并返回`false`。
加载器尝试使用指定的`format`读取像素映射。如果未指定`format`（这是默认），加载器会探测文件的头部以猜测文件格式。
如果数据需要修改以适应较低分辨率的结果（例如从32位转换为8位），使用`flags`来控制转换。

### `bool QPixmap::loadFromData(const QByteArray &data, const char *format = nullptr, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**作用与语义：**

使用指定的`format`和转换`flags`从二进制 `data`加载像素映射。

### `QBitmap QPixmap::mask() const`

**作用与语义：**

从像素图的 alpha 通道中提取位图遮罩。
警告：这可能是一项代价较高的操作。像素图的遮罩是从像素数据中动态提取的。

### `QRect QPixmap::rect() const`

**作用与语义：**

返回像素图的包围矩形。

### `bool QPixmap::save(const QString &fileName, const char *format = nullptr, int quality = -1) const`

**作用与语义：**

使用指定的图像文件 `format` 和 `quality` 因子，将像素映射保存到具有指定`fileName`的文件中。成功时返回 `true`;否则返回 `false`。
`quality`因子必须在 [0,100] 或 -1 范围内。指定 0 以获取小型压缩文件，指定 100 用于大型未压缩文件，-1 表示使用默认设置。
如果`format` `nullptr`，则从`fileName`的后缀中选择图像格式。

### `bool QPixmap::save(QIODevice *device, const char *format = nullptr, int quality = -1) const`

**作用与语义：**

该函数使用指定的图像文件`format`和`quality`因子，为给定`device`写入`QPixmap`。例如，可以直接将像素映射保存到`QByteArray`中：

**官方示例：**

```cpp
 QPixmap pixmap;
 QByteArray bytes;
 QBuffer buffer(&bytes);
 buffer.open(QIODevice::WriteOnly);
 pixmap.save(&buffer, "PNG"); // writes pixmap into bytes in PNG format
```

### `QPixmap QPixmap::scaled(const QSize &size, Qt::AspectRatioMode aspectRatioMode = Qt::IgnoreAspectRatio, Qt::TransformationMode transformMode = Qt::FastTransformation) const`

**作用与语义：**

利用`aspectRatioMode`和 `transformMode` 规定的宽高比和变换模式，将像素映射缩放到给定的`size`。
- 如果`aspectRatioMode` `Qt::IgnoreAspectRatio`，像素映射缩放为`size`。
- 如果`aspectRatioMode` `Qt::KeepAspectRatio`，像素地图会被缩放到`size`内尽可能大的矩形，保持宽高比。
- 如果`aspectRatioMode`为`Qt::KeepAspectRatioByExpanding`，像素图在`size`外缩放为尽可能小的矩形，保持宽高比。
如果给定的`size`为空，该函数返回一个空像素映射。
在某些情况下，画一个带有缩放集的画家比缩放画图更有利。这通常是当画师基于OpenGL或缩放因子变化迅速时。

### `QPixmap QPixmap::scaled(int width, int height, Qt::AspectRatioMode aspectRatioMode = Qt::IgnoreAspectRatio, Qt::TransformationMode transformMode = Qt::FastTransformation) const`

**作用与语义：**

返回一份按矩形缩放的像素映射副本，`width`和`height`根据给定的`aspectRatioMode`和`transformMode`。
如果`width`或`height`为零或负，该函数返回一个空像素映射。

### `QPixmap QPixmap::scaledToHeight(int height, Qt::TransformationMode mode = Qt::FastTransformation) const`

**作用与语义：**

返回图像的缩放副本。返回的图像通过指定的变换`mode`缩放到给定的`height`。像素图的宽度自动计算，以确保像素图的宽高比得以保持。
如果`height`为0或负值，则返回一个空像素映射。

### `QPixmap QPixmap::scaledToWidth(int width, Qt::TransformationMode mode = Qt::FastTransformation) const`

**作用与语义：**

返回一张缩放后的图像副本。返回的图像通过指定的变换`mode`缩放到给定的`width`。像素地图的高度会自动计算，以保持像素地图的宽高比。
如果`width`为0或负数，则返回一个空像素映射。

### `void QPixmap::scroll(int dx, int dy, const QRect &rect, QRegion *exposed = nullptr)`

**作用与语义：**

将该像素图`rect`的区域滚动为（`dx`， `dy`）。暴露区域保持不变。你可以选择性地将指针传递到空的`QRegion`，以获取滚动操作`exposed`的区域。
当画家在pixmap上有活跃画家时，你不能滚动。

**官方示例：**

```cpp
 QPixmap pixmap("background.png");
 QRegion exposed;
 pixmap.scroll(10, 10, pixmap.rect(), &exposed);
```

### `void QPixmap::scroll(int dx, int dy, int x, int y, int width, int height, QRegion *exposed = nullptr)`

**作用与语义：**

该便利函数等价于调用`QPixmap::scroll`（`dx`， `dy`， `QRect`（`x`， `y`， `width`， `height`）， `exposed`）。

### `void QPixmap::setDevicePixelRatio(qreal scaleFactor)`

**作用与语义：**

设置pixmap的设备像素比。这是图像像素与设备无关像素之间的比例。
默认`scaleFactor`是1.0。设置成其他版本有两个效果：
在像素地图上打开的QPainter会被缩放。例如，如果在200x200的图片上绘制，如果比例为2.0，则有效（与设备无关的）绘画边界为100x100。
基于像素地图大小计算布局几何的Qt代码路径会考虑该比例：`QSize` layoutSize = 像素地图。`size()` / 像素地图。`devicePixelRatio()` 这的净效应是像素地图显示为高DPI像素地图，而非大型像素地图（参见绘制高分辨率像素地图和图像）。

### `void QPixmap::setMask(const QBitmap &mask)`

**作用与语义：**

设置遮罩位图。
该函数将`mask`与像素图的α通道合并。遮罩上的像素值为1表示像素图的像素不变;值为0表示像素是透明的。遮罩必须与像素图大小相同。
设置空遮罩会重置遮罩，原本透明的像素保持黑色。当绘制像素贴图时，该函数的效果未定义。
警告：这可能是一项昂贵的操作。

### `QSize QPixmap::size() const`

**作用与语义：**

返回像素地图的大小。

### `[noexcept] void QPixmap::swap(QPixmap &other)`

**作用与语义：**

将像素映射与`other`交换。这个操作非常快，且从未失败。

### `QImage QPixmap::toImage() const`

**作用与语义：**

将像素映射转换为`QImage`。转换失败时返回空图。
如果像素图深度为1位，返回的图像也将是1位深度。位数较多的图像会以与底层系统紧密相符的格式返回。通常，对于带有alpha的像素图，这种格式会被`QImage::Format_ARGB32_Premultiplied`，对于没有alpha的像素图则采用`QImage::Format_RGB32`或`QImage::Format_RGB16`。
请注意，目前单色图像上的alpha遮罩被忽略。

### `QPixmap QPixmap::transformed(const QTransform &transform, Qt::TransformationMode mode = Qt::FastTransformation) const`

**作用与语义：**

返回一份通过给定变换`transform`和变换`mode`进行变换的像素映射副本。原始像素映射未被更改。
变换`transform`内部调整以补偿不必要的平移;即生成的像素映射是包含原始像素映射所有变换点的最小像素映射。使用`trueMatrix()`函数获取用于像素映射转换的实际矩阵。
该函数较慢，因为它涉及转换为`QImage`、非平凡计算以及变回 `QPixmap`。

### `[static] QTransform QPixmap::trueMatrix(const QTransform &matrix, int width, int height)`

**作用与语义：**

返回用于变换像素映射的实际矩阵，且`width`为`height`和`matrix`。
使用`transformed()`函数变换像素映射时，变换矩阵内部会调整以补偿不必要的平移，即`transformed()`返回包含原始像素映射所有变换点的最小像素映射。该函数返回修改后的矩阵，将原始像素映射的点正确映射到新的像素映射。

### `int QPixmap::width() const`

**作用与语义：**

返回像素地图的宽度。

### `QPixmap::operator QVariant() const`

**作用与语义：**

返回像素地图作为`QVariant`。

### `bool QPixmap::operator!() const`

**作用与语义：**

如果是空像素映射，返回`true`;否则返回 `false`。

### `[noexcept] QPixmap &QPixmap::operator=(QPixmap &&other)`

**作用与语义：**

Move-assign `other`到这个`QPixmap`实例。

### `QPixmap &QPixmap::operator=(const QPixmap &pixmap)`

**作用与语义：**

将给定`pixmap`分配到该像素映射，并返回对像素映射的引用。

### `QDataStream &operator<<(QDataStream &stream, const QPixmap &pixmap)`

**作用与语义：**

将给定`pixmap`写入给定`stream`，作为PNG图像。注意，将流写入文件不会生成有效的图像文件。

### `QDataStream &operator>>(QDataStream &stream, QPixmap &pixmap)`

**作用与语义：**

将给定`stream`的图像读取到给定的`pixmap`。

## 6. 深入实践与常见坑

### 生命周期和资源边界

绘制上下文必须绑定有效的 paint device，并在合法的绘制阶段使用。QWidget 上通常只在 `paintEvent()` 内创建 painter；离屏图像、打印设备和 pixmap 则有各自的设备生命周期。

### 状态和错误边界

`save()`/`restore()` 用于隔离局部状态；改变坐标系、画笔或合成模式后要么恢复，要么明确后续绘制也需要该状态。重绘请求和真正绘制是两个阶段，业务状态变化应调用 `update()`。

### 线程边界

同一个 GUI 控件的绘制在 GUI 线程完成；离屏 QImage 可以按数据所有权在后台处理，但不要让后台线程直接绘制或访问正在显示的 QWidget/QPixmap 资源。

### 最容易出现的错误

不要直接调用 paintEvent；不要在绘制函数里修改会再次触发绘制的状态；不要假定所有图像都是四字节像素；不要忘记 transform 会影响坐标和 boundingRect。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QPixmap` 所属机制类型：二维绘制状态机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
