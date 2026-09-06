# QPainterPathStroker

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QPainterPathStroker` 是 Qt GUI 绘制体系中的类型，负责画笔、画刷、字体、图像、绘制设备或绘制状态。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QPainterPathStroker` 是 二维绘制状态机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 绘制对象维护一组状态：画笔、画刷、字体、变换、裁剪、合成模式和渲染提示。每次 draw 调用都会使用当前状态；坐标通常经过当前 transform 映射到目标设备。

**适用场景：** 开始绘制后配置必要状态，使用 save/restore 包围局部变换，按设备坐标绘制，结束时让上下文析构或调用 end。绘制文本和图片时同时考虑字体度量、devicePixelRatio、裁剪和性能。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要直接调用 paintEvent；不要在绘制函数里修改会再次触发绘制的状态；不要假定所有图像都是四字节像素；不要忘记 transform 会影响坐标和 boundingRect。

## 2. 依赖与对象关系

- 头文件：`#include <QPainterPathStroker>`
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

### 公有函数

- `QPainterPathStroker()`
- `QPainterPathStroker(const QPen &pen)`
- `~QPainterPathStroker()`
- `Qt::PenCapStyle capStyle() const`
- `QPainterPath createStroke(const QPainterPath &path) const`
- `qreal curveThreshold() const`
- `qreal dashOffset() const`
- `QList<qreal> dashPattern() const`
- `Qt::PenJoinStyle joinStyle() const`
- `qreal miterLimit() const`
- `void setCapStyle(Qt::PenCapStyle style)`
- `void setCurveThreshold(qreal threshold)`
- `void setDashOffset(qreal offset)`
- `void setDashPattern(Qt::PenStyle style)`
- `void setDashPattern(const QList<qreal> &dashPattern)`
- `void setJoinStyle(Qt::PenJoinStyle style)`
- `void setMiterLimit(qreal limit)`
- `void setWidth(qreal width)`
- `qreal width() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QPainterPathStroker::QPainterPathStroker()`

**作用与语义：**

会创造一个新的行程器。

### `[explicit] QPainterPathStroker::QPainterPathStroker(const QPen &pen)`

**作用与语义：**

基于`pen`创建新的划弦器。

### `[noexcept] QPainterPathStroker::~QPainterPathStroker()`

**作用与语义：**

摧毁了行程器。

### `Qt::PenCapStyle QPainterPathStroker::capStyle() const`

**作用与语义：**

返回生成轮廓的顶部样式。

### `QPainterPath QPainterPathStroker::createStroke(const QPainterPath &path) const`

**作用与语义：**

生成一条新路径，该路径是表示给定`path`轮廓的可填充区域。
轮廓的各个设计方面基于划弦者的特性：`width()`、`capStyle()`、`joinStyle()`、`dashPattern()`、`curveThreshold()`和`miterLimit()`。
生成的路径应仅用于绘制给定的画家路径的轮廓。否则可能会导致意外行为。生成的轮廓还需要默认设置的`Qt::WindingFill`规则。

### `qreal QPainterPathStroker::curveThreshold() const`

**作用与语义：**

返回生成轮廓的曲线平整阈值。

### `qreal QPainterPathStroker::dashOffset() const`

**作用与语义：**

返回生成轮廓的破折号偏移量。

### `QList<qreal> QPainterPathStroker::dashPattern() const`

**作用与语义：**

返回生成轮廓的破折号图案。

### `Qt::PenJoinStyle QPainterPathStroker::joinStyle() const`

**作用与语义：**

返回生成轮廓的连接样式。

### `qreal QPainterPathStroker::miterLimit() const`

**作用与语义：**

返回生成轮廓的斜切限制。

### `void QPainterPathStroker::setCapStyle(Qt::PenCapStyle style)`

**作用与语义：**

将生成轮廓的顶部样式设置为`style`。如果设置了破折号图案，图案的每个段都受顶部`style`影响。

### `void QPainterPathStroker::setCurveThreshold(qreal threshold)`

**作用与语义：**

指定曲线拓平`threshold`，控制生成轮廓曲线绘制的粒度。
默认阈值是调整良好的值（0.25），通常不需要修改。不过，你可以通过降低曲线值来使曲线看起来更平滑。

### `void QPainterPathStroker::setDashOffset(qreal offset)`

**作用与语义：**

将生成轮廓的破折号偏移设置为`offset`。
关于破边偏移的描述，请参见`QPen::setDashOffset()`文档。

### `void QPainterPathStroker::setDashPattern(Qt::PenStyle style)`

**作用与语义：**

将生成轮廓的破折号模式设置为`style`。

### `void QPainterPathStroker::setDashPattern(const QList<qreal> &dashPattern)`

**作用与语义：**

将生成轮廓的破折线模式设置为`dashPattern`。该函数允许自定义破折线模式。
列表中的每个元素包含划线中划线中划号和空格的长度，从第一个元素的第一个破折号开始，第二个元素的第一个空格，之后的每对元素在破折号和空格之间交替出现。
列表可以包含奇数个元素，此时当模式重复时，最后一个元素的长度会延长至第一个元素的长度。

### `void QPainterPathStroker::setJoinStyle(Qt::PenJoinStyle style)`

**作用与语义：**

将生成轮廓的连接样式设置为`style`。

### `void QPainterPathStroker::setMiterLimit(qreal limit)`

**作用与语义：**

将生成轮廓的斜切极限设为`limit`。
斜口极限描述了斜接连接从每个连接处延伸的距离。该极限以当前设定宽度为单位表示。因此，像素级斜接极限将为`miterlimit * width`。
该值仅在连接风格为`Qt::MiterJoin`时使用。

### `void QPainterPathStroker::setWidth(qreal width)`

**作用与语义：**

将生成的轮廓画家路径宽度设置为`width`。
生成的轮廓会将`width`的约50%延伸到给定输入路径原始轮廓的两侧。

### `qreal QPainterPathStroker::width() const`

**作用与语义：**

返回生成轮廓的宽度。

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

`QPainterPathStroker` 所属机制类型：二维绘制状态机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
