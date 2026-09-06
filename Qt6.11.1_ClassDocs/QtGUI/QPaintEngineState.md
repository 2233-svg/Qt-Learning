# QPaintEngineState

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QPaintEngineState` 是 Qt GUI 绘制体系中的类型，负责画笔、画刷、字体、图像、绘制设备或绘制状态。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QPaintEngineState` 是 二维绘制状态机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 绘制对象维护一组状态：画笔、画刷、字体、变换、裁剪、合成模式和渲染提示。每次 draw 调用都会使用当前状态；坐标通常经过当前 transform 映射到目标设备。

**适用场景：** 开始绘制后配置必要状态，使用 save/restore 包围局部变换，按设备坐标绘制，结束时让上下文析构或调用 end。绘制文本和图片时同时考虑字体度量、devicePixelRatio、裁剪和性能。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要直接调用 paintEvent；不要在绘制函数里修改会再次触发绘制的状态；不要假定所有图像都是四字节像素；不要忘记 transform 会影响坐标和 boundingRect。

## 2. 依赖与对象关系

- 头文件：`#include <QPaintEngineState>`
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

- `QBrush backgroundBrush() const`
- `Qt::BGMode backgroundMode() const`
- `QBrush brush() const`
- `bool brushNeedsResolving() const`
- `QPointF brushOrigin() const`
- `Qt::ClipOperation clipOperation() const`
- `QPainterPath clipPath() const`
- `QRegion clipRegion() const`
- `QPainter::CompositionMode compositionMode() const`
- `QFont font() const`
- `bool isClipEnabled() const`
- `qreal opacity() const`
- `QPainter * painter() const`
- `QPen pen() const`
- `bool penNeedsResolving() const`
- `QPainter::RenderHints renderHints() const`
- `QPaintEngine::DirtyFlags state() const`
- `QTransform transform() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QBrush QPaintEngineState::backgroundBrush() const`

**作用与语义：**

返回当前绘画引擎状态的背景画笔。
该变量仅在`state()`返回包含`QPaintEngine::DirtyBackground`标志的组合时使用。

### `Qt::BGMode QPaintEngineState::backgroundMode() const`

**作用与语义：**

返回当前绘画引擎状态的背景模式。
该变量仅在`state()`返回包含`QPaintEngine::DirtyBackgroundMode`标志的组合时使用。

### `QBrush QPaintEngineState::brush() const`

**作用与语义：**

将画笔返回当前的油漆引擎状态。
该变量仅在`state()`返回包含`QPaintEngine::DirtyBrush`标志的组合时使用。

### `bool QPaintEngineState::brushNeedsResolving() const`

**作用与语义：**

返回填充坐标是否被当前渲染操作定义为有界，并需解决（关于当前渲染的原件）。

### `QPointF QPaintEngineState::brushOrigin() const`

**作用与语义：**

将画笔原点返回当前的油漆引擎状态。
该变量仅在`state()`返回包含`QPaintEngine::DirtyBrushOrigin`标志的组合时使用。

### `Qt::ClipOperation QPaintEngineState::clipOperation() const`

**作用与语义：**

在当前的绘画引擎状态下返回剪辑操作。
该变量仅在`state()`返回包含`QPaintEngine::DirtyClipPath`或`QPaintEngine::DirtyClipRegion`标志的组合时使用。

### `QPainterPath QPaintEngineState::clipPath() const`

**作用与语义：**

返回当前绘制引擎状态下的剪辑路径。
该变量仅在`state()`返回包含`QPaintEngine::DirtyClipPath`标志的组合时使用。

### `QRegion QPaintEngineState::clipRegion() const`

**作用与语义：**

返回当前绘画引擎状态下的剪辑区域。
该变量仅在`state()`返回包含`QPaintEngine::DirtyClipRegion`标志的组合时使用。

### `QPainter::CompositionMode QPaintEngineState::compositionMode() const`

**作用与语义：**

返回当前绘图引擎状态的合成模式。
该变量仅在`state()`返回包含`QPaintEngine::DirtyCompositionMode`标志的组合时使用。

### `QFont QPaintEngineState::font() const`

**作用与语义：**

会返回当前的绘图引擎状态的字体。
该变量仅在`state()`返回包含`QPaintEngine::DirtyFont`标志的组合时使用。

### `bool QPaintEngineState::isClipEnabled() const`

**作用与语义：**

在当前绘制引擎状态下，返回是否启用裁剪。
该变量仅在`state()`返回包含`QPaintEngine::DirtyClipEnabled`标志的组合时使用。

### `qreal QPaintEngineState::opacity() const`

**作用与语义：**

返回当前涂装引擎状态下的不透明度。

### `QPainter *QPaintEngineState::painter() const`

**作用与语义：**

返回一个指向正在更新喷漆引擎的画师的指针。

### `QPen QPaintEngineState::pen() const`

**作用与语义：**

将笔返回当前的涂装引擎状态。
该变量仅在`state()`返回包含`QPaintEngine::DirtyPen`标志的组合时使用。

### `bool QPaintEngineState::penNeedsResolving() const`

**作用与语义：**

返回笔画坐标是否已被当前渲染操作指定为有界，并需围绕当前渲染的原图进行解析。

### `QPainter::RenderHints QPaintEngineState::renderHints() const`

**作用与语义：**

返回当前绘画引擎状态下的渲染提示。
该变量仅在`state()`返回包含`QPaintEngine::DirtyHints`标志的组合时使用。

### `QPaintEngine::DirtyFlags QPaintEngineState::state() const`

**作用与语义：**

返回一组标志，标识在更新绘图引擎状态时需要更新的属性集合（即调用`QPaintEngine::updateState()`函数时）。

### `QTransform QPaintEngineState::transform() const`

**作用与语义：**

返回当前涂装引擎状态的矩阵。
该变量仅在`state()`返回包含`QPaintEngine::DirtyTransform`标志的组合时使用。

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

`QPaintEngineState` 所属机制类型：二维绘制状态机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
