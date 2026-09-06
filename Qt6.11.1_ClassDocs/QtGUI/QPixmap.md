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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 55 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QPixmap::QPixmap()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPixmap` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QPixmap::QPixmap(const char *const[] xpm)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPixmap` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `xpm`：类型为 `const char *const[]`。没有默认值，调用时必须提供。传入 `const char *const[]` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPixmap::QPixmap(int width, int height)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPixmap` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPixmap::QPixmap(const QString &fileName, const char *format = nullptr, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPixmap` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。
- 参数 `format`：类型为 `const char *`。默认值为 `nullptr`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `flags`：类型为 `Qt::ImageConversionFlags`。默认值为 `Qt::AutoColor`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QPixmap::QPixmap(const QSize &size)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPixmap` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `size`：类型为 `const QSize &`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPixmap::QPixmap(const QPixmap &pixmap)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPixmap` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `pixmap`：类型为 `const QPixmap &`。没有默认值，调用时必须提供。传入 `const QPixmap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QPixmap::QPixmap(QPixmap &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPixmap` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `QPixmap &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QPixmap::~QPixmap()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPixmap` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QPixmap::cacheKey() const`

**API 类别：** 成员函数说明

**中文解读：** `QPixmap::cacheKey` 用于计算、查询或取得与“cache、Key”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPixmap::convertFromImage(const QImage &image, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `convertFromImage`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`bool`。
- 参数 `image`：类型为 `const QImage &`。没有默认值，调用时必须提供。传入 `const QImage &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `Qt::ImageConversionFlags`。默认值为 `Qt::AutoColor`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPixmap QPixmap::copy(const QRect &rectangle = QRect()) const`

**API 类别：** 成员函数说明

**中文解读：** `QPixmap::copy` 用于计算、查询或取得与“copy”相关的操作。调用时要先确认当前状态和 `rectangle` 的有效范围；返回类型是 `QPixmap`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPixmap`。
- 参数 `rectangle`：类型为 `const QRect &`。默认值为 `QRect()`。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPixmap QPixmap::copy(int x, int y, int width, int height) const`

**API 类别：** 成员函数说明

**中文解读：** `QPixmap::copy` 用于计算、查询或取得与“copy”相关的操作。调用时要先确认当前状态和 `x`、`y`、`width`、`height` 的有效范围；返回类型是 `QPixmap`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPixmap`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBitmap QPixmap::createHeuristicMask(bool clipTight = true) const`

**API 类别：** 成员函数说明

**中文解读：** `QPixmap::createHeuristicMask` 用于计算、查询或取得与“创建、Heuristic、Mask”相关的操作。调用时要先确认当前状态和 `clipTight` 的有效范围；返回类型是 `QBitmap`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QBitmap`。
- 参数 `clipTight`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBitmap QPixmap::createMaskFromColor(const QColor &maskColor, Qt::MaskMode mode = Qt::MaskInColor) const`

**API 类别：** 成员函数说明

**中文解读：** `QPixmap::createMaskFromColor` 用于计算、查询或取得与“创建、Mask、转换进入、Color”相关的操作。调用时要先确认当前状态和 `maskColor`、`mode` 的有效范围；返回类型是 `QBitmap`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QBitmap`。
- 参数 `maskColor`：类型为 `const QColor &`。没有默认值，调用时必须提供。传入 `const QColor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mode`：类型为 `Qt::MaskMode`。默认值为 `Qt::MaskInColor`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] int QPixmap::defaultDepth()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `defaultDepth`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QPixmap::depth() const`

**API 类别：** 成员函数说明

**中文解读：** `QPixmap::depth` 用于计算、查询或取得与“depth”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPixmap::detach()`

**API 类别：** 成员函数说明

**中文解读：** `QPixmap::detach` 用于执行与“detach”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] QSizeF QPixmap::deviceIndependentSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QPixmap::deviceIndependentSize` 用于计算、查询或取得与“device、Independent、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSizeF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSizeF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QPixmap::devicePixelRatio() const`

**API 类别：** 成员函数说明

**中文解读：** `QPixmap::devicePixelRatio` 用于计算、查询或取得与“device、Pixel、Ratio”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPixmap::fill(const QColor &color = Qt::white)`

**API 类别：** 成员函数说明

**中文解读：** `QPixmap::fill` 用于执行与“fill”相关的操作。调用时要先确认当前状态和 `color` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `color`：类型为 `const QColor &`。默认值为 `Qt::white`。传入 `const QColor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QPixmap QPixmap::fromImage(const QImage &image, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromImage`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QPixmap`。
- 参数 `image`：类型为 `const QImage &`。没有默认值，调用时必须提供。传入 `const QImage &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `Qt::ImageConversionFlags`。默认值为 `Qt::AutoColor`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QPixmap QPixmap::fromImage(QImage &&image, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromImage`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QPixmap`。
- 参数 `image`：类型为 `QImage &&`。没有默认值，调用时必须提供。传入 `QImage &&` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `Qt::ImageConversionFlags`。默认值为 `Qt::AutoColor`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QPixmap QPixmap::fromImageReader(QImageReader *imageReader, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromImageReader`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QPixmap`。
- 参数 `imageReader`：类型为 `QImageReader *`。没有默认值，调用时必须提供。传入 `QImageReader *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `Qt::ImageConversionFlags`。默认值为 `Qt::AutoColor`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPixmap::hasAlpha() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasAlpha`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPixmap::hasAlphaChannel() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasAlphaChannel`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QPixmap::height() const`

**API 类别：** 成员函数说明

**中文解读：** `QPixmap::height` 用于计算、查询或取得与“高度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPixmap::isNull() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isNull`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPixmap::isQBitmap() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isQBitmap`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPixmap::load(const QString &fileName, const char *format = nullptr, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `load`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`bool`。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。
- 参数 `format`：类型为 `const char *`。默认值为 `nullptr`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `flags`：类型为 `Qt::ImageConversionFlags`。默认值为 `Qt::AutoColor`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPixmap::loadFromData(const uchar *data, uint len, const char *format = nullptr, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `loadFromData`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`bool`。
- 参数 `data`：类型为 `const uchar *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `len`：类型为 `uint`。没有默认值，调用时必须提供。传入 `uint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `const char *`。默认值为 `nullptr`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `flags`：类型为 `Qt::ImageConversionFlags`。默认值为 `Qt::AutoColor`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPixmap::loadFromData(const QByteArray &data, const char *format = nullptr, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `loadFromData`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`bool`。
- 参数 `data`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `format`：类型为 `const char *`。默认值为 `nullptr`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `flags`：类型为 `Qt::ImageConversionFlags`。默认值为 `Qt::AutoColor`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBitmap QPixmap::mask() const`

**API 类别：** 成员函数说明

**中文解读：** `QPixmap::mask` 用于计算、查询或取得与“mask”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QBitmap`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QBitmap`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRect QPixmap::rect() const`

**API 类别：** 成员函数说明

**中文解读：** `QPixmap::rect` 用于计算、查询或取得与“rect”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPixmap::save(const QString &fileName, const char *format = nullptr, int quality = -1) const`

**API 类别：** 成员函数说明

**中文解读：** `QPixmap::save` 用于计算、查询或取得与“保存”相关的操作。调用时要先确认当前状态和 `fileName`、`format`、`quality` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。
- 参数 `format`：类型为 `const char *`。默认值为 `nullptr`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `quality`：类型为 `int`。默认值为 `-1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPixmap::save(QIODevice *device, const char *format = nullptr, int quality = -1) const`

**API 类别：** 成员函数说明

**中文解读：** `QPixmap::save` 用于计算、查询或取得与“保存”相关的操作。调用时要先确认当前状态和 `device`、`format`、`quality` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `device`：类型为 `QIODevice *`。没有默认值，调用时必须提供。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。
- 参数 `format`：类型为 `const char *`。默认值为 `nullptr`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `quality`：类型为 `int`。默认值为 `-1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPixmap QPixmap::scaled(const QSize &size, Qt::AspectRatioMode aspectRatioMode = Qt::IgnoreAspectRatio, Qt::TransformationMode transformMode = Qt::FastTransformation) const`

**API 类别：** 成员函数说明

**中文解读：** `QPixmap::scaled` 用于计算、查询或取得与“scaled”相关的操作。调用时要先确认当前状态和 `size`、`aspectRatioMode`、`transformMode` 的有效范围；返回类型是 `QPixmap`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPixmap`。
- 参数 `size`：类型为 `const QSize &`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。
- 参数 `aspectRatioMode`：类型为 `Qt::AspectRatioMode`。默认值为 `Qt::IgnoreAspectRatio`。传入 `Qt::AspectRatioMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `transformMode`：类型为 `Qt::TransformationMode`。默认值为 `Qt::FastTransformation`。传入 `Qt::TransformationMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPixmap QPixmap::scaled(int width, int height, Qt::AspectRatioMode aspectRatioMode = Qt::IgnoreAspectRatio, Qt::TransformationMode transformMode = Qt::FastTransformation) const`

**API 类别：** 成员函数说明

**中文解读：** `QPixmap::scaled` 用于计算、查询或取得与“scaled”相关的操作。调用时要先确认当前状态和 `width`、`height`、`aspectRatioMode`、`transformMode` 的有效范围；返回类型是 `QPixmap`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPixmap`。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `aspectRatioMode`：类型为 `Qt::AspectRatioMode`。默认值为 `Qt::IgnoreAspectRatio`。传入 `Qt::AspectRatioMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `transformMode`：类型为 `Qt::TransformationMode`。默认值为 `Qt::FastTransformation`。传入 `Qt::TransformationMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPixmap QPixmap::scaledToHeight(int height, Qt::TransformationMode mode = Qt::FastTransformation) const`

**API 类别：** 成员函数说明

**中文解读：** `QPixmap::scaledToHeight` 用于计算、查询或取得与“scaled、转换输出、高度”相关的操作。调用时要先确认当前状态和 `height`、`mode` 的有效范围；返回类型是 `QPixmap`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPixmap`。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `mode`：类型为 `Qt::TransformationMode`。默认值为 `Qt::FastTransformation`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPixmap QPixmap::scaledToWidth(int width, Qt::TransformationMode mode = Qt::FastTransformation) const`

**API 类别：** 成员函数说明

**中文解读：** `QPixmap::scaledToWidth` 用于计算、查询或取得与“scaled、转换输出、宽度”相关的操作。调用时要先确认当前状态和 `width`、`mode` 的有效范围；返回类型是 `QPixmap`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPixmap`。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `mode`：类型为 `Qt::TransformationMode`。默认值为 `Qt::FastTransformation`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPixmap::scroll(int dx, int dy, const QRect &rect, QRegion *exposed = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** `QPixmap::scroll` 用于执行与“scroll”相关的操作。调用时要先确认当前状态和 `dx`、`dy`、`rect`、`exposed` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `dx`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `dy`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `rect`：类型为 `const QRect &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。
- 参数 `exposed`：类型为 `QRegion *`。默认值为 `nullptr`。传入 `QRegion *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPixmap::scroll(int dx, int dy, int x, int y, int width, int height, QRegion *exposed = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** `QPixmap::scroll` 用于执行与“scroll”相关的操作。调用时要先确认当前状态和 `dx`、`dy`、`x`、`y`、`width`、`height`、`exposed` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `dx`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `dy`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `exposed`：类型为 `QRegion *`。默认值为 `nullptr`。传入 `QRegion *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPixmap::setDevicePixelRatio(qreal scaleFactor)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDevicePixelRatio`。调用它会改变 `QPixmap` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `scaleFactor`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPixmap::setMask(const QBitmap &mask)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMask`。调用它会改变 `QPixmap` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mask`：类型为 `const QBitmap &`。没有默认值，调用时必须提供。传入 `const QBitmap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSize QPixmap::size() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `size`，返回 `QPixmap` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QPixmap::swap(QPixmap &other)`

**API 类别：** 成员函数说明

**中文解读：** `QPixmap::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QPixmap &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImage QPixmap::toImage() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toImage`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QImage`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPixmap QPixmap::transformed(const QTransform &transform, Qt::TransformationMode mode = Qt::FastTransformation) const`

**API 类别：** 成员函数说明

**中文解读：** `QPixmap::transformed` 用于计算、查询或取得与“transformed”相关的操作。调用时要先确认当前状态和 `transform`、`mode` 的有效范围；返回类型是 `QPixmap`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPixmap`。
- 参数 `transform`：类型为 `const QTransform &`。没有默认值，调用时必须提供。传入 `const QTransform &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mode`：类型为 `Qt::TransformationMode`。默认值为 `Qt::FastTransformation`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QTransform QPixmap::trueMatrix(const QTransform &matrix, int width, int height)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `trueMatrix`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QTransform`。
- 参数 `matrix`：类型为 `const QTransform &`。没有默认值，调用时必须提供。传入 `const QTransform &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QPixmap::width() const`

**API 类别：** 成员函数说明

**中文解读：** `QPixmap::width` 用于计算、查询或取得与“宽度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPixmap::operator QVariant() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPixmap` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`由运算符声明决定`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPixmap::operator!() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPixmap` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QPixmap &QPixmap::operator=(QPixmap &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPixmap` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QPixmap &`。
- 参数 `other`：类型为 `QPixmap &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPixmap &QPixmap::operator=(const QPixmap &pixmap)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPixmap` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QPixmap &`。
- 参数 `pixmap`：类型为 `const QPixmap &`。没有默认值，调用时必须提供。传入 `const QPixmap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDataStream &operator<<(QDataStream &stream, const QPixmap &pixmap)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QPixmap` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDataStream &`。
- 参数 `stream`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pixmap`：类型为 `const QPixmap &`。没有默认值，调用时必须提供。传入 `const QPixmap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDataStream &operator>>(QDataStream &stream, QPixmap &pixmap)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QPixmap` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDataStream &`。
- 参数 `stream`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pixmap`：类型为 `QPixmap &`。没有默认值，调用时必须提供。传入 `QPixmap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
