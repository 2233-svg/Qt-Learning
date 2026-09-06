# QQuickFramebufferObject::Renderer

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QQuickFramebufferObject::Renderer` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QQuickFramebufferObject::Renderer` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQuickFramebufferObject>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

### 状态、生命周期和线程

**生命周期：** QML 引擎、上下文和对象所有权必须明确。由 QML 创建的对象通常由引擎管理；通过 context property 或 C++ 暴露的对象要决定由 C++ 持有还是转移给 QML，不能让绑定指向悬空对象。

**状态与结果：** 属性绑定和直接赋值不是一回事：直接给被绑定属性赋值通常会打破原有绑定。C++ 属性要有正确的 notify signal，QML 才能在数据变化时更新；信号参数和属性当前值要保持一致。

**线程与事件循环：** 大多数 QML 对象和 GUI 操作在 GUI 线程，场景图渲染还可能在 render thread。不要在渲染阶段调用 GUI 对象 API；后台数据通过线程安全的信号/槽边界送入 QML。

## 3. 直接使用

需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。 使用时通常按这个过程组织：注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

```cpp
// C++ 侧暴露属性/信号后，在 QML 中建立绑定。
// 变化时发出 notify signal，避免在绑定表达式中直接修改状态。
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 保护函数

- `Renderer()`
- `virtual ~Renderer()`
- `virtual QOpenGLFramebufferObject * createFramebufferObject(const QSize &size)`
- `QOpenGLFramebufferObject * framebufferObject() const`
- `void invalidateFramebufferObject()`
- `virtual void render() = 0`
- `virtual void synchronize(QQuickFramebufferObject *item)`
- `void update()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[protected] Renderer::Renderer()`

**作用与语义：**

构建一个新的渲染器。
该函数在场景图同步阶段调用，当图形线程被阻塞时。

### `[virtual noexcept protected] Renderer::~Renderer()`

**作用与语义：**

当`QQuickFramebufferObject`项目的场景图资源被清理时，渲染器会自动被删除。
该函数在渲染线程中被调用。

### `[virtual protected] QOpenGLFramebufferObject *Renderer::createFramebufferObject(const QSize &size)`

**作用与语义：**

当需要新的 FBO 时调用该函数。此过程发生在初始帧。如果 `QQuickFramebufferObject::textureFollowsItemSize` 设置为 true，每次项目尺寸变化时都会再次调用。
返回的 FBO 可以有任何附件。如果`QOpenGLFramebufferObjectFormat`指示 FBO 需要多重采样，渲染器内部实现会分配第二个 FBO，并将多采样后的 FBO 漂白到用于显示纹理的 FBO 中。
注意：有些硬件对小FBO尺寸存在问题。`size`考虑了这一点，所以在用固定尺寸覆盖尺寸时要小心。最小尺寸64x64应该总是可行。
注意：`size`考虑了设备像素比，意味着它已经乘以正确的比例因子。当将包含`QQuickFramebufferObject`物品的窗口移动到设置不同的屏幕时，FBO会自动重建，并以正确的大小调用此功能。

### `[protected] QOpenGLFramebufferObject *Renderer::framebufferObject() const`

**作用与语义：**

返回当前正在渲染的帧缓冲对象。

### `[protected] void Renderer::invalidateFramebufferObject()`

**作用与语义：**

在 `synchronize()` 期间调用该函数以使当前 FBO 失效。这会导致创建一个新的 FBO 并带有 `createFramebufferObject()`。

### `[pure virtual protected] void Renderer::render()`

**作用与语义：**

当 FBO 渲染到该 时调用这个函数。此时帧缓冲区被绑定，`glViewport` 也设置为匹配 FBO 大小。
函数返回后，FBO会自动解除绑定。
注意：不要假设调用该函数时 OpenGL 状态已全部设置为默认值，或调用间保持状态。Qt Quick 渲染器和自定义渲染代码都使用相同的 OpenGL 上下文。这意味着状态可能在调用该函数之前被 Quick 修改过。
注意：建议在返回前调用`QQuickOpenGLUtils::resetOpenGLState()`。这会重置 Qt Quick 渲染器使用的 OpenGL 状态，从而避免渲染代码在该函数中所做的状态变化干扰。

### `[virtual protected] void Renderer::synchronize(QQuickFramebufferObject *item)`

**作用与语义：**

该函数是`QQuickFramebufferObject::update()`的结果。
使用该函数更新渲染器中发生的变更。`item` 是实例化该渲染器的项目。在创建 FBO 之前，该函数只调用一次。
例如，如果该项目有由QML控制的颜色属性，应调用`QQuickFramebufferObject::update()`并使用同步化（synchronize）将新颜色复制到渲染器中，以便用于渲染下一帧。
这个函数是渲染器和物品之间唯一安全读取和写入彼此成员的地方。

### `[protected] void Renderer::update()`

**作用与语义：**

当 FBO 需要重新渲染时调用此函数。可以在 `render()` 中调用，以在下一帧之前强制 FBO 重新渲染。注意：此函数应在渲染器内部使用。要在 GUI 线程上更新项，请使用 `QQuickFramebufferObject::update()`。

## 6. 深入实践与常见坑

### 生命周期和资源边界

QML 引擎、上下文和对象所有权必须明确。由 QML 创建的对象通常由引擎管理；通过 context property 或 C++ 暴露的对象要决定由 C++ 持有还是转移给 QML，不能让绑定指向悬空对象。

### 状态和错误边界

属性绑定和直接赋值不是一回事：直接给被绑定属性赋值通常会打破原有绑定。C++ 属性要有正确的 notify signal，QML 才能在数据变化时更新；信号参数和属性当前值要保持一致。

### 线程边界

大多数 QML 对象和 GUI 操作在 GUI 线程，场景图渲染还可能在 render thread。不要在渲染阶段调用 GUI 对象 API；后台数据通过线程安全的信号/槽边界送入 QML。

### 最容易出现的错误

不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QQuickFramebufferObject::Renderer` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
