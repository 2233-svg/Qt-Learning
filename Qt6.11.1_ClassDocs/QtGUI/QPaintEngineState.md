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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 18 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QBrush QPaintEngineState::backgroundBrush() const`

**API 类别：** 成员函数说明

**中文解读：** `QPaintEngineState::backgroundBrush` 用于计算、查询或取得与“background、Brush”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QBrush`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QBrush`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::BGMode QPaintEngineState::backgroundMode() const`

**API 类别：** 成员函数说明

**中文解读：** `QPaintEngineState::backgroundMode` 用于计算、查询或取得与“background、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::BGMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::BGMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBrush QPaintEngineState::brush() const`

**API 类别：** 成员函数说明

**中文解读：** `QPaintEngineState::brush` 用于计算、查询或取得与“brush”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QBrush`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QBrush`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPaintEngineState::brushNeedsResolving() const`

**API 类别：** 成员函数说明

**中文解读：** `QPaintEngineState::brushNeedsResolving` 用于计算、查询或取得与“brush、Needs、Resolving”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPointF QPaintEngineState::brushOrigin() const`

**API 类别：** 成员函数说明

**中文解读：** `QPaintEngineState::brushOrigin` 用于计算、查询或取得与“brush、Origin”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPointF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPointF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::ClipOperation QPaintEngineState::clipOperation() const`

**API 类别：** 成员函数说明

**中文解读：** `QPaintEngineState::clipOperation` 用于计算、查询或取得与“clip、Operation”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::ClipOperation`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::ClipOperation`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPainterPath QPaintEngineState::clipPath() const`

**API 类别：** 成员函数说明

**中文解读：** `QPaintEngineState::clipPath` 用于计算、查询或取得与“clip、Path”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPainterPath`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPainterPath`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRegion QPaintEngineState::clipRegion() const`

**API 类别：** 成员函数说明

**中文解读：** `QPaintEngineState::clipRegion` 用于计算、查询或取得与“clip、Region”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRegion`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRegion`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPainter::CompositionMode QPaintEngineState::compositionMode() const`

**API 类别：** 成员函数说明

**中文解读：** `QPaintEngineState::compositionMode` 用于计算、查询或取得与“composition、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPainter::CompositionMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPainter::CompositionMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFont QPaintEngineState::font() const`

**API 类别：** 成员函数说明

**中文解读：** `QPaintEngineState::font` 用于计算、查询或取得与“字体”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFont`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFont`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPaintEngineState::isClipEnabled() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isClipEnabled`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QPaintEngineState::opacity() const`

**API 类别：** 成员函数说明

**中文解读：** `QPaintEngineState::opacity` 用于计算、查询或取得与“opacity”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPainter *QPaintEngineState::painter() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPaintEngineState` 的核心操作 `painter`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QPainter *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPen QPaintEngineState::pen() const`

**API 类别：** 成员函数说明

**中文解读：** `QPaintEngineState::pen` 用于计算、查询或取得与“pen”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPen`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPen`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPaintEngineState::penNeedsResolving() const`

**API 类别：** 成员函数说明

**中文解读：** `QPaintEngineState::penNeedsResolving` 用于计算、查询或取得与“pen、Needs、Resolving”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPainter::RenderHints QPaintEngineState::renderHints() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPaintEngineState` 的核心操作 `renderHints`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QPainter::RenderHints`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPaintEngine::DirtyFlags QPaintEngineState::state() const`

**API 类别：** 成员函数说明

**中文解读：** `QPaintEngineState::state` 用于计算、查询或取得与“state”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPaintEngine::DirtyFlags`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPaintEngine::DirtyFlags`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTransform QPaintEngineState::transform() const`

**API 类别：** 成员函数说明

**中文解读：** `QPaintEngineState::transform` 用于计算、查询或取得与“transform”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTransform`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTransform`。
- 参数：无。

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

`QPaintEngineState` 所属机制类型：二维绘制状态机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
