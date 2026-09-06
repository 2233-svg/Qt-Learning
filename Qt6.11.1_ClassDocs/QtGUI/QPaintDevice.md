# QPaintDevice

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QPaintDevice` 是 Qt GUI 绘制体系中的类型，负责画笔、画刷、字体、图像、绘制设备或绘制状态。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QPaintDevice` 是 二维绘制状态机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 绘制对象维护一组状态：画笔、画刷、字体、变换、裁剪、合成模式和渲染提示。每次 draw 调用都会使用当前状态；坐标通常经过当前 transform 映射到目标设备。

**适用场景：** 开始绘制后配置必要状态，使用 save/restore 包围局部变换，按设备坐标绘制，结束时让上下文析构或调用 end。绘制文本和图片时同时考虑字体度量、devicePixelRatio、裁剪和性能。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要直接调用 paintEvent；不要在绘制函数里修改会再次触发绘制的状态；不要假定所有图像都是四字节像素；不要忘记 transform 会影响坐标和 boundingRect。

## 2. 依赖与对象关系

- 头文件：`#include <QPaintDevice>`
- 继承自：未在类页中列出
- 直接派生类：QImage、QOpenGLPaintDevice、QPagedPaintDevice、QPaintDeviceWindow、QPicture、QPixmap、QSvgGenerator,、QWidget

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

开始绘制后配置必要状态，使用 save/restore 包围局部变换，按设备坐标绘制，结束时让上下文析构或调用 end。绘制文本和图片时同时考虑字体度量、devicePixelRatio、裁剪和性能。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

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

### 公有类型

- `enum PaintDeviceMetric { PdmWidth, PdmHeight, PdmWidthMM, PdmHeightMM, PdmNumColors, …, PdmDevicePixelRatioF_EncodedB }`

### 公有函数

- `virtual ~QPaintDevice()`
- `int colorCount() const`
- `int depth() const`
- `qreal devicePixelRatio() const`
- `qreal devicePixelRatioF() const`
- `int height() const`
- `int heightMM() const`
- `int logicalDpiX() const`
- `int logicalDpiY() const`
- `virtual QPaintEngine * paintEngine() const = 0`
- `bool paintingActive() const`
- `int physicalDpiX() const`
- `int physicalDpiY() const`
- `int width() const`
- `int widthMM() const`

### 静态公有成员

- `(since 6.8) int encodeMetricF(QPaintDevice::PaintDeviceMetric metric, double value)`

### 保护函数

- `QPaintDevice()`
- `virtual int metric(QPaintDevice::PaintDeviceMetric metric) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QPaintDevice::PaintDeviceMetric`

**作用与语义：**

描述了油漆设备的各种指标。
- `QPaintDevice::PdmWidth`：`1`;涂装装置在默认坐标系单位中的宽度（例如像素数为`QPixmap`和`QWidget`）。另见`width()`。
- `QPaintDevice::PdmHeight`：`2`;涂装装置在默认坐标系单位中的高度（例如像素数为`QPixmap`和`QWidget`）。另见`height()`。
- `QPaintDevice::PdmWidthMM`：`3`;涂料装置的宽度（毫米）。参见`widthMM()`。
- `QPaintDevice::PdmHeightMM`：`4`;涂料装置的高度（毫米）。另见`heightMM()`。
- `QPaintDevice::PdmNumColors`：`5`;涂装装置可用的不同颜色数量。另见`colorCount()`。
- `QPaintDevice::PdmDepth`：`6`;绘画装置的位深（位面数）。参见`depth()`。
- `QPaintDevice::PdmDpiX`：`7`;设备的水平分辨率，单位为每英寸点数。参见`logicalDpiX()`。
- `QPaintDevice::PdmDpiY`：`8`;设备的垂直分辨率，单位为每英寸点数。参见`logicalDpiY()`。
- `QPaintDevice::PdmPhysicalDpiX`：`9`;设备的水平分辨率（每英寸点数）。参见`physicalDpiX()`。
- `QPaintDevice::PdmPhysicalDpiY`：`10`;设备的垂直分辨率，单位为每英寸点数。参见`physicalDpiY()`。
- `QPaintDevice::PdmDevicePixelRatio`：`11`;设备像素比。常见值为1用于正常DPI显示器，2用于高DPI“视网膜”显示器。
- `QPaintDevice::PdmDevicePixelRatioScaled`：`12`;设备的缩放后设备像素比。这与PdmDevicePixelRatio相同，但值被常数因子放大，以支持分数缩放因子的绘画设备。所使用的恒定缩放因子为devicePixelRatioFScale()。该枚举值在Qt 5.6中引入。
- `QPaintDevice::PdmDevicePixelRatioF_EncodedA (since Qt 6.8)`：`13`;该枚举项与对应的 `B` 项一起用于设备的像素比，作为编码`double`浮点值。支持分数 DPR 值的`QPaintDevice`子类应在覆盖 `metric()` 函数时实现对这两个枚举项的支持。返回值预期为 `encodeMetricF()` 函数的结果。
- `QPaintDevice::PdmDevicePixelRatioF_EncodedB (since Qt 6.8)`：`14`;参见PdmDevicePixelRatioF_EncodedA。

### `[noexcept protected] QPaintDevice::QPaintDevice()`

**作用与语义：**

构造一个绘图装置。该构造器只能从QPaintDevice的子类调用。

### `[virtual noexcept] QPaintDevice::~QPaintDevice()`

**作用与语义：**

会摧毁绘画装置并释放窗户系统资源。

### `int QPaintDevice::colorCount() const`

**作用与语义：**

返回绘画设备可用的颜色数量。如果可用颜色数量过多，无法用整数数据类型表示，则返回INT_MAX。

### `int QPaintDevice::depth() const`

**作用与语义：**

返回绘图设备的位深（位面数）。

### `qreal QPaintDevice::devicePixelRatio() const`

**作用与语义：**

返回设备各单元的像素比例。
常见的数值是1用于正常DPI显示器，2用于高DPI“视网膜”显示器。

### `qreal QPaintDevice::devicePixelRatioF() const`

**作用与语义：**

返回设备的像素比，作为浮点数。

### `[static, since 6.8] int QPaintDevice::encodeMetricF(QPaintDevice::PaintDeviceMetric metric, double value)`

**作用与语义：**

返回`value`为度量`metric`编码。实现`metric()`的子类应使用该函数进行编码。
- `as`：当查询度量指定编码浮点数值时，为整数返回值。

### `int QPaintDevice::height() const`

**作用与语义：**

返回涂装设备的高度，使用默认坐标系单位（例如`QPixmap`和`QWidget`的像素数）。

### `int QPaintDevice::heightMM() const`

**作用与语义：**

返回绘图设备的高度（毫米单位）。由于平台限制，可能无法使用此功能来确定屏幕上小部件的实际物理大小。

### `int QPaintDevice::logicalDpiX() const`

**作用与语义：**

返回设备的水平分辨率（每英寸点数），用于计算字体大小。对于X11，通常与`widthMM()`计算相同。
注意，如果逻辑DpiX()不等于`physicalDpiX()`，则相应的`QPaintEngine`必须处理分辨率映射。

### `int QPaintDevice::logicalDpiY() const`

**作用与语义：**

返回设备的垂直分辨率（每英寸点数），用于计算字体大小。对于X11，这通常与`heightMM()`计算的相同。
注意，如果逻辑DpiY()不等于`physicalDpiY()`，则相应的`QPaintEngine`必须处理分辨率映射。

### `[virtual protected] int QPaintDevice::metric(QPaintDevice::PaintDeviceMetric metric) const`

**作用与语义：**

返回给定绘画设备`metric`的度规信息。

### `[pure virtual] QPaintEngine *QPaintDevice::paintEngine() const`

**作用与语义：**

返回一个指向用于在设备上绘画的绘画引擎的指针。

### `bool QPaintDevice::paintingActive() const`

**作用与语义：**

如果设备正在被涂装，即有人已调用`QPainter::begin()`但尚未为该设备调用`QPainter::end()`，则返回`true`;否则返回`false`。

### `int QPaintDevice::physicalDpiX() const`

**作用与语义：**

返回设备的水平分辨率，单位为每英寸点数。例如，在打印时，该分辨率指的是物理打印机的分辨率。而逻辑DPI则指实际绘图引擎使用的分辨率。
注意，如果物理DpiX()不等于`logicalDpiX()`，对应的`QPaintEngine`必须处理分辨率映射。

### `int QPaintDevice::physicalDpiY() const`

**作用与语义：**

返回设备的水平分辨率，单位为每英寸点数。例如，在打印时，该分辨率指的是物理打印机的分辨率。而逻辑DPI则指实际绘图引擎使用的分辨率。
注意，如果物理DpiY()不等于`logicalDpiY()`，对应的`QPaintEngine`必须处理分辨率映射。

### `int QPaintDevice::width() const`

**作用与语义：**

返回涂装设备的宽度，以默认坐标系单位（例如`QPixmap`和像素`QWidget`）。

### `int QPaintDevice::widthMM() const`

**作用与语义：**

返回绘图设备的宽度（毫米）。由于平台限制，可能无法用该函数确定屏幕上小部件的实际物理大小。

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

`QPaintDevice` 所属机制类型：二维绘制状态机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
