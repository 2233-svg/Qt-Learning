# QPaintDeviceWindow

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QPaintDeviceWindow` 是 Qt GUI 绘制体系中的类型，负责画笔、画刷、字体、图像、绘制设备或绘制状态。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QPaintDeviceWindow` 是 二维绘制状态机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 绘制对象维护一组状态：画笔、画刷、字体、变换、裁剪、合成模式和渲染提示。每次 draw 调用都会使用当前状态；坐标通常经过当前 transform 映射到目标设备。

**适用场景：** 开始绘制后配置必要状态，使用 save/restore 包围局部变换，按设备坐标绘制，结束时让上下文析构或调用 end。绘制文本和图片时同时考虑字体度量、devicePixelRatio、裁剪和性能。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要直接调用 paintEvent；不要在绘制函数里修改会再次触发绘制的状态；不要假定所有图像都是四字节像素；不要忘记 transform 会影响坐标和 boundingRect。

## 2. 依赖与对象关系

- 头文件：`#include <QPaintDeviceWindow>`
- 继承自：QWindow、QPaintDevice
- 直接派生类：QOpenGLWindow、QRasterWindow

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

- `void update(const QRect &rect)`
- `void update(const QRegion &region)`

### 公有槽函数

- `void update()`

### 重实现的保护函数

- `virtual void paintEvent(QPaintEvent *event) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[override virtual protected] void QPaintDeviceWindow::paintEvent(QPaintEvent *event)`

**作用与语义：**

重实现自：`QWindow::paintEvent`（QPaintEvent *ev）。
处理 `event` 参数中传递的绘画事件。
默认实现不做任何操作。重新实现这个函数以执行绘画。如有必要，脏区域可以从`event`中恢复。
每当窗口某区域需要重新绘制时，例如最初显示窗口，或移动另一窗口导致部分窗口暴露时，窗口系统都会发送绘画事件（`ev`）。
应用程序应根据绘制事件渲染到窗口，无论窗口的暴露状态如何。例如，可能会在窗口暴露前发送绘画事件，以准备向用户展示。

### `[slot] void QPaintDeviceWindow::update()`

**作用与语义：**

把整扇窗户标记为脏，并安排重新粉刷。
注意：在下一次绘制事件之前对该函数的后续调用将被忽略。
注意：对于未暴露的窗口，更新会被推迟，直到窗口再次暴露。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
paintDeviceWindow， qOverload<>（&QPaintDeviceWindow：：update））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
paintDeviceWindow， [receiver = paintDeviceWindow]() { receiver->update(); }）;


更多示例和方法，请参见连接超载槽位。

### `void QPaintDeviceWindow::update(const QRect &rect)`

**作用与语义：**

标记窗户`rect`脏，并安排重新粉刷。
注意：在下一次绘画事件之前调用该函数的后续调用将被忽略，但`rect`会添加到区域以进行更新。
注意：对于未暴露的窗口，更新会被推迟，直到窗口再次暴露。

### `void QPaintDeviceWindow::update(const QRegion &region)`

**作用与语义：**

标记窗户`region`脏，并安排重新粉刷。
注意：在下一次绘制事件之前，后续调用该函数将被忽略，但`region`会添加到区域以进行更新。
注意：对于未暴露的窗口，更新会被推迟，直到窗口再次暴露。

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

`QPaintDeviceWindow` 所属机制类型：二维绘制状态机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
