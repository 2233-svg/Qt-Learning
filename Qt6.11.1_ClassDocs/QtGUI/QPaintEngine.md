# QPaintEngine

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QPaintEngine` 是 Qt GUI 绘制体系中的类型，负责画笔、画刷、字体、图像、绘制设备或绘制状态。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QPaintEngine` 是 二维绘制状态机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 绘制对象维护一组状态：画笔、画刷、字体、变换、裁剪、合成模式和渲染提示。每次 draw 调用都会使用当前状态；坐标通常经过当前 transform 映射到目标设备。

**适用场景：** 开始绘制后配置必要状态，使用 save/restore 包围局部变换，按设备坐标绘制，结束时让上下文析构或调用 end。绘制文本和图片时同时考虑字体度量、devicePixelRatio、裁剪和性能。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要直接调用 paintEvent；不要在绘制函数里修改会再次触发绘制的状态；不要假定所有图像都是四字节像素；不要忘记 transform 会影响坐标和 boundingRect。

## 2. 依赖与对象关系

- 头文件：`#include <QPaintEngine>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

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

- `enum DirtyFlag { DirtyPen, DirtyBrush, DirtyBrushOrigin, DirtyFont, DirtyBackground, …, AllDirty }`
- `flags DirtyFlags`
- `enum PaintEngineFeature { AlphaBlend, Antialiasing, BlendModes, BrushStroke, ConicalGradientFill, …, AllFeatures }`
- `flags PaintEngineFeatures`
- `enum PolygonDrawMode { OddEvenMode, WindingMode, ConvexMode, PolylineMode }`
- `enum Type { X11, Windows, MacPrinter, CoreGraphics, QuickDraw, …, Direct2D }`

### 公有函数

- `QPaintEngine(QPaintEngine::PaintEngineFeatures caps = PaintEngineFeatures())`
- `virtual ~QPaintEngine()`
- `virtual bool begin(QPaintDevice *pdev) = 0`
- `virtual void drawEllipse(const QRectF &rect)`
- `virtual void drawEllipse(const QRect &rect)`
- `virtual void drawImage(const QRectF &rectangle, const QImage &image, const QRectF &sr, Qt::ImageConversionFlags flags = Qt::AutoColor)`
- `virtual void drawLines(const QLineF *lines, int lineCount)`
- `virtual void drawLines(const QLine *lines, int lineCount)`
- `virtual void drawPath(const QPainterPath &path)`
- `virtual void drawPixmap(const QRectF &r, const QPixmap &pm, const QRectF &sr) = 0`
- `virtual void drawPoints(const QPoint *points, int pointCount)`
- `virtual void drawPoints(const QPointF *points, int pointCount)`
- `virtual void drawPolygon(const QPointF *points, int pointCount, QPaintEngine::PolygonDrawMode mode)`
- `virtual void drawPolygon(const QPoint *points, int pointCount, QPaintEngine::PolygonDrawMode mode)`
- `virtual void drawRects(const QRectF *rects, int rectCount)`
- `virtual void drawRects(const QRect *rects, int rectCount)`
- `virtual void drawTextItem(const QPointF &p, const QTextItem &textItem)`
- `virtual void drawTiledPixmap(const QRectF &rect, const QPixmap &pixmap, const QPointF &p)`
- `virtual bool end() = 0`
- `bool hasFeature(QPaintEngine::PaintEngineFeatures feature) const`
- `bool isActive() const`
- `QPaintDevice * paintDevice() const`
- `QPainter * painter() const`
- `void setActive(bool state)`
- `virtual QPaintEngine::Type type() const = 0`
- `virtual void updateState(const QPaintEngineState &state) = 0`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QPaintEngine::DirtyFlagflags QPaintEngine::DirtyFlags`

**作用与语义：**

- `QPaintEngine::DirtyPen`：`0x0001`;笔脏了，需要更新。
- `QPaintEngine::DirtyBrush`：`0x0002`;画刷脏了，需要更新。
- `QPaintEngine::DirtyBrushOrigin`：`0x0004`;画刷原点脏，需要更新。
- `QPaintEngine::DirtyFont`：`0x0008`;字体脏了，需要更新。
- `QPaintEngine::DirtyBackground`：`0x0010`;背景脏了，需要更新。
- `QPaintEngine::DirtyBackgroundMode`：`0x0020`;后台模式很脏，需要更新。
- `QPaintEngine::DirtyTransform`：`0x0040`;变换是脏的，需要更新。
- `QPaintEngine::DirtyClipRegion`：`0x0080`;剪辑区域脏了，需要更新。
- `QPaintEngine::DirtyClipPath`：`0x0100`;剪辑路径是脏的，需要更新。
- `QPaintEngine::DirtyHints`：`0x0200`;渲染提示是脏的，需要更新。
- `QPaintEngine::DirtyCompositionMode`：`0x0400`;合成模式很脏，需要更新。
- `QPaintEngine::DirtyClipEnabled`：`0x0800`;是否启用裁剪是不规则的，需要更新。
- `QPaintEngine::DirtyOpacity`：`0x1000`;常数不透明度发生变化，需要作为状态变化的一部分进行更新`QPaintEngine::updateState()`。
- `QPaintEngine::AllDirty`：`0xffff`;内部使用的便利枚举。
这些类型被`QPainter`用来触发`QPaintEngine`中各状态的懒惰更新，使用`QPaintEngine::updateState()`。
喷漆引擎必须更新所有脏状态。
DirtyFlags 类型是 QFlags 的 typedef<DirtyFlag>。它存储 DirtyFlag 值的 OR 组合。

### `enum QPaintEngine::PaintEngineFeatureflags QPaintEngine::PaintEngineFeatures`

**作用与语义：**

该枚举用于描述绘图引擎的特性或能力。如果某个功能不被引擎支持，`QPainter`系统会尽力通过其他方式模拟该功能，并将 alpha 混合`QImage`与模拟结果传递给引擎。有些功能无法被模拟：AlphaBlend 和 PorterDuff。
- `QPaintEngine::AlphaBlend`：`0x00000080`;该引擎可以alpha混合原语。
- `QPaintEngine::Antialiasing`：`0x00000400`;该引擎可以使用抗锯齿来改善渲染图元的外观。
- `QPaintEngine::BlendModes`：`0x00008000`;引擎支持混合模式。
- `QPaintEngine::BrushStroke`：`0x00000800`;引擎支持以笔刷为填充的绘画笔画，而不仅仅是纯色（例如宽度为2的虚线渐变线）。
- `QPaintEngine::ConicalGradientFill`：`0x00000040`;发动机支持锥形梯度填充。
- `QPaintEngine::ConstantOpacity`：`0x00001000`;该发动机支持`QPainter::setOpacity()`提供的特性。
- `QPaintEngine::LinearGradientFill`：`0x00000010`;发动机支持线性梯度填充。
- `QPaintEngine::MaskedBrush`：`0x00002000`;该引擎能够渲染带有 alpha 通道或遮罩的纹理笔刷。
- `QPaintEngine::ObjectBoundingModeGradients`：`0x00010000`;引擎原生支持坐标模式`QGradient::ObjectBoundingMode`的梯度。否则，如果支持 QPaintEngine：:P atternTransform，则物体边界模式梯度会转换为坐标模式为 `QGradient::LogicalMode` 的梯度，并带有坐标映射的画刷变换。
- `QPaintEngine::PainterPaths`：`0x00000200`;发动机有路径支撑。
- `QPaintEngine::PaintOutsidePaintEvent`：`0x20000000`;该引擎能够在喷漆事件之外进行喷漆。
- `QPaintEngine::PatternBrush`：`0x00000008`;该引擎能够渲染`Qt::BrushStyle`中指定的画刷图案。
- `QPaintEngine::PatternTransform`：`0x00000002`;引擎支持笔刷图案的转换。
- `QPaintEngine::PerspectiveTransform`：`0x00004000`;该引擎支持对原件进行透视变换。
- `QPaintEngine::PixmapTransform`：`0x00000004`;引擎可以转换像素贴图，包括旋转和剪切。
- `QPaintEngine::PorterDuff`：`0x00000100`;该发动机支持波特-达夫的运营
- `QPaintEngine::PrimitiveTransform`：`0x00000001`;该引擎支持绘图原语的变换。
- `QPaintEngine::RadialGradientFill`：`0x00000020`;发动机支持径向梯度填充。
- `QPaintEngine::RasterOpModes`：`0x00020000`;该引擎支持位形扫描。
- `QPaintEngine::AllFeatures`：`0xffffffff`;上述所有特征。该枚举值通常用作位遮罩。
PaintEngineFeatures 类型是 QFlags 的 typedef<PaintEngineFeature>。它存储 PaintEngineFeature 值的 OR 组合。

### `[explicit] QPaintEngine::QPaintEngine(QPaintEngine::PaintEngineFeatures caps = PaintEngineFeatures())`

**作用与语义：**

创建一个带有`caps`指定特征集的绘画引擎。

### `[virtual noexcept] QPaintEngine::~QPaintEngine()`

**作用与语义：**

会毁掉喷漆引擎。

### `[pure virtual] bool QPaintEngine::begin(QPaintDevice *pdev)`

**作用与语义：**

重新实现该函数，在绘制设备开始绘制时初始化绘图引擎`pdev`。如果初始化成功，则返回 true;否则返回 false。

### `[virtual] void QPaintEngine::drawEllipse(const QRectF &rect)`

**作用与语义：**

重新实现该函数，绘制出矩形`rect`内能包含的最大椭圆。
默认实现调用`drawPolygon()`。

### `[virtual] void QPaintEngine::drawEllipse(const QRect &rect)`

**作用与语义：**

该函数的默认实现调用该函数的浮点版本。

### `[virtual] void QPaintEngine::drawImage(const QRectF &rectangle, const QImage &image, const QRectF &sr, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**作用与语义：**

重新实现这个函数，用给定的转换旗标绘制给定`rectangle`中`sr`矩形指定的`image`部分，`flags`，并将其转换为像素映射。

### `[virtual] void QPaintEngine::drawLines(const QLineF *lines, int lineCount)`

**作用与语义：**

默认实现将 `lines` 中的行列表拆分为 `lineCount` 个独立调用 `drawPath()` 或 `drawPolygon()`，具体取决于绘图引擎的特性集。

### `[virtual] void QPaintEngine::drawLines(const QLine *lines, int lineCount)`

**作用与语义：**

默认实现将 `lines` 中的前 `lineCount` 行转换为 `QLineF`，并调用该函数的浮点版本。

### `[virtual] void QPaintEngine::drawPath(const QPainterPath &path)`

**作用与语义：**

默认实现忽略 `path`，不执行任何操作。

### `[pure virtual] void QPaintEngine::drawPixmap(const QRectF &r, const QPixmap &pm, const QRectF &sr)`

**作用与语义：**

重新实现该函数，绘制给定`r`中`sr`矩形指定的`pm`部分。

### `[virtual] void QPaintEngine::drawPoints(const QPoint *points, int pointCount)`

**作用与语义：**

绘制缓冲区中的前`pointCount`点`points`。
默认实现会将`points`中的前`pointCount` QPoint转换为QPointF，并调用drawPoint的浮点版本。

### `[virtual] void QPaintEngine::drawPoints(const QPointF *points, int pointCount)`

**作用与语义：**

绘制缓冲区的前`pointCount`点`points`。

### `[virtual] void QPaintEngine::drawPolygon(const QPointF *points, int pointCount, QPaintEngine::PolygonDrawMode mode)`

**作用与语义：**

重新实现这个虚拟函数，用模式`mode`绘制`points`中`pointCount`点定义的多边形。
注意：至少有一个 drawPolygon() 函数必须重新实现。

### `[virtual] void QPaintEngine::drawPolygon(const QPoint *points, int pointCount, QPaintEngine::PolygonDrawMode mode)`

**作用与语义：**

重新实现这个虚拟函数，用模式`mode`绘制`points`中`pointCount`点定义的多边形。
注意：至少有一个 drawPolygon() 函数必须重新实现。

### `[virtual] void QPaintEngine::drawRects(const QRectF *rects, int rectCount)`

**作用与语义：**

在缓冲区`rects`绘制前`rectCount`矩形。该函数的默认实现调用 `drawPath()` 或 `drawPolygon()`，具体取决于绘图引擎的功能集。

### `[virtual] void QPaintEngine::drawRects(const QRect *rects, int rectCount)`

**作用与语义：**

默认实现将缓冲区 `rects` 中的前 `rectCount` 矩形转换为 `QRectF`，并调用该函数的浮点版本。

### `[virtual] void QPaintEngine::drawTextItem(const QPointF &p, const QTextItem &textItem)`

**作用与语义：**

该函数绘制位于位置`p`的文本项`textItem`。该函数的默认实现是将文本转换为`QPainterPath`并绘制生成路径。

### `[virtual] void QPaintEngine::drawTiledPixmap(const QRectF &rect, const QPixmap &pixmap, const QPointF &p)`

**作用与语义：**

重新实现该函数，从给定`p`开始绘制给定`rect`的`pixmap`。像素映射将反复绘制，直到`rect`填满。

### `[pure virtual] bool QPaintEngine::end()`

**作用与语义：**

重新实现该函数以完成当前绘画设备上的绘画。如果绘画成功完成，则返回 true;否则返回 false。

### `bool QPaintEngine::hasFeature(QPaintEngine::PaintEngineFeatures feature) const`

**作用与语义：**

如果涂装引擎支持指定`feature`，返回`true`;否则返回`false`。

### `bool QPaintEngine::isActive() const`

**作用与语义：**

如果油漆引擎正在绘制，返回`true`;否则返回`false`。

### `QPaintDevice *QPaintEngine::paintDevice() const`

**作用与语义：**

如果正在绘制，返回该引擎正在绘制的装置;否则返回`nullptr`。

### `QPainter *QPaintEngine::painter() const`

**作用与语义：**

还原喷漆引擎的油漆工。

### `void QPaintEngine::setActive(bool state)`

**作用与语义：**

将涂装引擎的激活状态设置为`state`。

### `[pure virtual] QPaintEngine::Type QPaintEngine::type() const`

**作用与语义：**

重新实现这个函数，返回绘画引擎`Type`。

### `[pure virtual] void QPaintEngine::updateState(const QPaintEngineState &state)`

**作用与语义：**

重新实现这个函数以更新绘图引擎的状态。
实现后，该函数负责检查绘图引擎当前`state`并更新被更改的属性。使用`QPaintEngineState::state()`函数找出需要更新的属性，然后使用相应的get函数获取当前属性的值。

### `enum DirtyFlag { DirtyPen, DirtyBrush, DirtyBrushOrigin, DirtyFont, DirtyBackground, …, AllDirty }`

**作用与语义：**

- `QPaintEngine::DirtyPen`：`0x0001`;笔脏了，需要更新。
- `QPaintEngine::DirtyBrush`：`0x0002`;画刷脏了，需要更新。
- `QPaintEngine::DirtyBrushOrigin`：`0x0004`;画刷原点脏，需要更新。
- `QPaintEngine::DirtyFont`：`0x0008`;字体脏了，需要更新。
- `QPaintEngine::DirtyBackground`：`0x0010`;背景脏了，需要更新。
- `QPaintEngine::DirtyBackgroundMode`：`0x0020`;后台模式很脏，需要更新。
- `QPaintEngine::DirtyTransform`：`0x0040`;变换是脏的，需要更新。
- `QPaintEngine::DirtyClipRegion`：`0x0080`;剪辑区域脏了，需要更新。
- `QPaintEngine::DirtyClipPath`：`0x0100`;剪辑路径是脏的，需要更新。
- `QPaintEngine::DirtyHints`：`0x0200`;渲染提示是脏的，需要更新。
- `QPaintEngine::DirtyCompositionMode`：`0x0400`;合成模式很脏，需要更新。
- `QPaintEngine::DirtyClipEnabled`：`0x0800`;是否启用裁剪是不规则的，需要更新。
- `QPaintEngine::DirtyOpacity`：`0x1000`;常数不透明度发生变化，需要作为状态变化的一部分进行更新`QPaintEngine::updateState()`。
- `QPaintEngine::AllDirty`：`0xffff`;内部使用的便利枚举。
这些类型被`QPainter`用来触发`QPaintEngine`中各状态的懒惰更新，使用`QPaintEngine::updateState()`。
喷漆引擎必须更新所有脏状态。
DirtyFlags 类型是 QFlags 的 typedef<DirtyFlag>。它存储 DirtyFlag 值的 OR 组合。

### `flags DirtyFlags`

**作用与语义：**

- `QPaintEngine::DirtyPen`：`0x0001`;笔脏了，需要更新。
- `QPaintEngine::DirtyBrush`：`0x0002`;画刷脏了，需要更新。
- `QPaintEngine::DirtyBrushOrigin`：`0x0004`;画刷原点脏，需要更新。
- `QPaintEngine::DirtyFont`：`0x0008`;字体脏了，需要更新。
- `QPaintEngine::DirtyBackground`：`0x0010`;背景脏了，需要更新。
- `QPaintEngine::DirtyBackgroundMode`：`0x0020`;后台模式很脏，需要更新。
- `QPaintEngine::DirtyTransform`：`0x0040`;变换是脏的，需要更新。
- `QPaintEngine::DirtyClipRegion`：`0x0080`;剪辑区域脏了，需要更新。
- `QPaintEngine::DirtyClipPath`：`0x0100`;剪辑路径是脏的，需要更新。
- `QPaintEngine::DirtyHints`：`0x0200`;渲染提示是脏的，需要更新。
- `QPaintEngine::DirtyCompositionMode`：`0x0400`;合成模式很脏，需要更新。
- `QPaintEngine::DirtyClipEnabled`：`0x0800`;是否启用裁剪是不规则的，需要更新。
- `QPaintEngine::DirtyOpacity`：`0x1000`;常数不透明度发生变化，需要作为状态变化的一部分进行更新`QPaintEngine::updateState()`。
- `QPaintEngine::AllDirty`：`0xffff`;内部使用的便利枚举。
这些类型被`QPainter`用来触发`QPaintEngine`中各状态的懒惰更新，使用`QPaintEngine::updateState()`。
喷漆引擎必须更新所有脏状态。
DirtyFlags 类型是 QFlags 的 typedef<DirtyFlag>。它存储 DirtyFlag 值的 OR 组合。

### `enum PaintEngineFeature { AlphaBlend, Antialiasing, BlendModes, BrushStroke, ConicalGradientFill, …, AllFeatures }`

**作用与语义：**

该枚举用于描述绘图引擎的特性或能力。如果某个功能不被引擎支持，`QPainter`系统会尽力通过其他方式模拟该功能，并将 alpha 混合`QImage`与模拟结果传递给引擎。有些功能无法被模拟：AlphaBlend 和 PorterDuff。
- `QPaintEngine::AlphaBlend`：`0x00000080`;该引擎可以alpha混合原语。
- `QPaintEngine::Antialiasing`：`0x00000400`;该引擎可以使用抗锯齿来改善渲染图元的外观。
- `QPaintEngine::BlendModes`：`0x00008000`;引擎支持混合模式。
- `QPaintEngine::BrushStroke`：`0x00000800`;引擎支持以笔刷为填充的绘画笔画，而不仅仅是纯色（例如宽度为2的虚线渐变线）。
- `QPaintEngine::ConicalGradientFill`：`0x00000040`;发动机支持锥形梯度填充。
- `QPaintEngine::ConstantOpacity`：`0x00001000`;该发动机支持`QPainter::setOpacity()`提供的特性。
- `QPaintEngine::LinearGradientFill`：`0x00000010`;发动机支持线性梯度填充。
- `QPaintEngine::MaskedBrush`：`0x00002000`;该引擎能够渲染带有 alpha 通道或遮罩的纹理笔刷。
- `QPaintEngine::ObjectBoundingModeGradients`：`0x00010000`;引擎原生支持坐标模式`QGradient::ObjectBoundingMode`的梯度。否则，如果支持 QPaintEngine：:P atternTransform，则物体边界模式梯度会转换为坐标模式为 `QGradient::LogicalMode` 的梯度，并带有坐标映射的画刷变换。
- `QPaintEngine::PainterPaths`：`0x00000200`;发动机有路径支撑。
- `QPaintEngine::PaintOutsidePaintEvent`：`0x20000000`;该引擎能够在喷漆事件之外进行喷漆。
- `QPaintEngine::PatternBrush`：`0x00000008`;该引擎能够渲染`Qt::BrushStyle`中指定的画刷图案。
- `QPaintEngine::PatternTransform`：`0x00000002`;引擎支持笔刷图案的转换。
- `QPaintEngine::PerspectiveTransform`：`0x00004000`;该引擎支持对原件进行透视变换。
- `QPaintEngine::PixmapTransform`：`0x00000004`;引擎可以转换像素贴图，包括旋转和剪切。
- `QPaintEngine::PorterDuff`：`0x00000100`;该发动机支持波特-达夫的运营
- `QPaintEngine::PrimitiveTransform`：`0x00000001`;该引擎支持绘图原语的变换。
- `QPaintEngine::RadialGradientFill`：`0x00000020`;发动机支持径向梯度填充。
- `QPaintEngine::RasterOpModes`：`0x00020000`;该引擎支持位形扫描。
- `QPaintEngine::AllFeatures`：`0xffffffff`;上述所有特征。该枚举值通常用作位遮罩。
PaintEngineFeatures 类型是 QFlags 的 typedef<PaintEngineFeature>。它存储 PaintEngineFeature 值的 OR 组合。

### `flags PaintEngineFeatures`

**作用与语义：**

该枚举用于描述绘图引擎的特性或能力。如果某个功能不被引擎支持，`QPainter`系统会尽力通过其他方式模拟该功能，并将 alpha 混合`QImage`与模拟结果传递给引擎。有些功能无法被模拟：AlphaBlend 和 PorterDuff。
- `QPaintEngine::AlphaBlend`：`0x00000080`;该引擎可以alpha混合原语。
- `QPaintEngine::Antialiasing`：`0x00000400`;该引擎可以使用抗锯齿来改善渲染图元的外观。
- `QPaintEngine::BlendModes`：`0x00008000`;引擎支持混合模式。
- `QPaintEngine::BrushStroke`：`0x00000800`;引擎支持以笔刷为填充的绘画笔画，而不仅仅是纯色（例如宽度为2的虚线渐变线）。
- `QPaintEngine::ConicalGradientFill`：`0x00000040`;发动机支持锥形梯度填充。
- `QPaintEngine::ConstantOpacity`：`0x00001000`;该发动机支持`QPainter::setOpacity()`提供的特性。
- `QPaintEngine::LinearGradientFill`：`0x00000010`;发动机支持线性梯度填充。
- `QPaintEngine::MaskedBrush`：`0x00002000`;该引擎能够渲染带有 alpha 通道或遮罩的纹理笔刷。
- `QPaintEngine::ObjectBoundingModeGradients`：`0x00010000`;引擎原生支持坐标模式`QGradient::ObjectBoundingMode`的梯度。否则，如果支持 QPaintEngine：:P atternTransform，则物体边界模式梯度会转换为坐标模式为 `QGradient::LogicalMode` 的梯度，并带有坐标映射的画刷变换。
- `QPaintEngine::PainterPaths`：`0x00000200`;发动机有路径支撑。
- `QPaintEngine::PaintOutsidePaintEvent`：`0x20000000`;该引擎能够在喷漆事件之外进行喷漆。
- `QPaintEngine::PatternBrush`：`0x00000008`;该引擎能够渲染`Qt::BrushStyle`中指定的画刷图案。
- `QPaintEngine::PatternTransform`：`0x00000002`;引擎支持笔刷图案的转换。
- `QPaintEngine::PerspectiveTransform`：`0x00004000`;该引擎支持对原件进行透视变换。
- `QPaintEngine::PixmapTransform`：`0x00000004`;引擎可以转换像素贴图，包括旋转和剪切。
- `QPaintEngine::PorterDuff`：`0x00000100`;该发动机支持波特-达夫的运营
- `QPaintEngine::PrimitiveTransform`：`0x00000001`;该引擎支持绘图原语的变换。
- `QPaintEngine::RadialGradientFill`：`0x00000020`;发动机支持径向梯度填充。
- `QPaintEngine::RasterOpModes`：`0x00020000`;该引擎支持位形扫描。
- `QPaintEngine::AllFeatures`：`0xffffffff`;上述所有特征。该枚举值通常用作位遮罩。
PaintEngineFeatures 类型是 QFlags 的 typedef<PaintEngineFeature>。它存储 PaintEngineFeature 值的 OR 组合。

### `enum PolygonDrawMode { OddEvenMode, WindingMode, ConvexMode, PolylineMode }`

**作用与语义：**

- `QPaintEngine::OddEvenMode`：`0`;多边形应使用奇偶填充规则绘制。
- `QPaintEngine::WindingMode`：`1`;多边形应使用绕过填充规则绘制。
- `QPaintEngine::ConvexMode`：`2`;该多边形是一个凸多边形，可用专业算法绘制。
- `QPaintEngine::PolylineMode`：`3`;只需绘制多边形的轮廓。

### `enum Type { X11, Windows, MacPrinter, CoreGraphics, QuickDraw, …, Direct2D }`

**作用与语义：**

- `QPaintEngine::X11`: `0`
- `QPaintEngine::Windows`: `1`
- `QPaintEngine::MacPrinter`: `4`
- `QPaintEngine::CoreGraphics`: `3`；macOS 的 Quartz2D（CoreGraphics）
- `QPaintEngine::QuickDraw`: `2`；macOS 的 QuickDraw
- `QPaintEngine::QWindowSystem`: `5`；嵌入式 Linux 的 Qt
- `QPaintEngine::OpenGL`: `6`
- `QPaintEngine::Picture`: `7`；`QPicture` 格式
- `QPaintEngine::SVG`: `8`；可缩放矢量图 XML 格式
- `QPaintEngine::Raster`: `9`
- `QPaintEngine::Direct3D`: `10`；仅限 Windows，基于 Direct3D 的引擎
- `QPaintEngine::Pdf`: `11`；可移植文档格式（PDF）
- `QPaintEngine::OpenVG`: `12`
- `QPaintEngine::User`: `50`；第一个用户类型 ID
- `QPaintEngine::MaxUser`: `100`；最后一个用户类型 ID
- `QPaintEngine::OpenGL2`: `13`
- `QPaintEngine::PaintBuffer`: `14`
- `QPaintEngine::Blitter`: `15`
- `QPaintEngine::Direct2D`: `16`；仅限 Windows，基于 Direct2D 的引擎

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

`QPaintEngine` 所属机制类型：二维绘制状态机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
