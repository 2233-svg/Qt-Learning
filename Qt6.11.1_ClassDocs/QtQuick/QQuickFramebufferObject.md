# QQuickFramebufferObject

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QQuickFramebufferObject` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QQuickFramebufferObject` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQuickFramebufferObject>`
- 继承自：QQuickItem
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Quick)
target_link_libraries(mytarget PRIVATE Qt6::Quick)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

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

### 公有类型

- `class Renderer`

### 属性

- `mirrorVertically : bool`
- `textureFollowsItemSize : bool`

### 公有函数

- `QQuickFramebufferObject(QQuickItem *parent = nullptr)`
- `virtual QQuickFramebufferObject::Renderer * createRenderer() const = 0`
- `bool mirrorVertically() const`
- `void setMirrorVertically(bool enable)`
- `void setTextureFollowsItemSize(bool follows)`
- `bool textureFollowsItemSize() const`

### 重实现的公有函数

- `virtual bool isTextureProvider() const override`
- `virtual void releaseResources() override`
- `virtual QSGTextureProvider * textureProvider() const override`

### 信号

- `void mirrorVerticallyChanged(bool)`
- `void textureFollowsItemSizeChanged(bool)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `mirrorVertically : bool`

**作用与语义：**

该属性控制绘制时 FBO 内容大小是否应垂直镜像。这使得不符合标准期望的第三方渲染代码易于集成。
默认值是`false`。

**如何使用：** 调用 `mirrorVertically()` 读取当前值；它不会修改应用状态。

### `textureFollowsItemSize : bool`

**作用与语义：**

该属性控制 FBO 纹理尺寸是否应与`QQuickFramebufferObject`物品的尺寸相符。当该属性为假时，FBO 将在首次显示时创建一次。如果设置为 true，则每次物品尺寸变化时都会重新创建。
默认值是`true`。

**如何使用：** 调用 `textureFollowsItemSize()` 读取当前值；它不会修改应用状态。

### `QQuickFramebufferObject::QQuickFramebufferObject(QQuickItem *parent = nullptr)`

**作用与语义：**

构建一个带有父 `parent` 的新 QQuickFrameBufferObject。

### `[pure virtual] QQuickFramebufferObject::Renderer *QQuickFramebufferObject::createRenderer() const`

**作用与语义：**

重新实现这个函数，创建一个用于渲染到 FBO 的渲染器。
在GUI线程被阻塞时，该函数会在渲染线程上被调用。

### `[override virtual] bool QQuickFramebufferObject::isTextureProvider() const`

**作用与语义：**

重装：`QQuickItem::isTextureProvider()` const.
如果该项是纹理提供者，则返回 true。默认实现返回 false。
该函数可以从任何线程调用。

### `[override virtual] void QQuickFramebufferObject::releaseResources()`

**作用与语义：**

重装：`QQuickItem::releaseResources()`。
当某个项目需要释放尚未由`QQuickItem::updatePaintNode()`返回节点管理的图形资源时，调用该函数。
当该项即将从之前渲染的窗口中移除时，就会发生这种情况。当调用该函数时，该项必定会有`window`。
该函数在图形界面线程中被调用，渲染线程的状态（使用时）未知。对象不应直接删除，而应通过`QQuickWindow::scheduleRenderJob()`调度进行清理。

### `[override virtual] QSGTextureProvider *QQuickFramebufferObject::textureProvider() const`

**作用与语义：**

重实现自：`QQuickItem::textureProvider()` const.
返回某个物品的纹理提供者。默认实现返回`nullptr`。
该函数只能在渲染线程中调用。

### `class Renderer`

**作用与语义：**

`QQuickFramebufferObject::Renderer`类用于实现`QQuickFramebufferObject`的渲染逻辑。

### `bool mirrorVertically() const`

**作用与语义：**

该属性控制绘制时 FBO 内容大小是否应垂直镜像。这使得不符合标准期望的第三方渲染代码易于集成。
默认值是`false`。

**如何使用：** 调用 `mirrorVertically()` 读取当前值；它不会修改应用状态。

### `void setMirrorVertically(bool enable)`

**作用与语义：**

该属性控制绘制时 FBO 内容大小是否应垂直镜像。这使得不符合标准期望的第三方渲染代码易于集成。
默认值是`false`。

**如何使用：** 调用 `setMirrorVertically(...)` 修改 `mirrorVertically`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTextureFollowsItemSize(bool follows)`

**作用与语义：**

该属性控制 FBO 纹理尺寸是否应与`QQuickFramebufferObject`物品的尺寸相符。当该属性为假时，FBO 将在首次显示时创建一次。如果设置为 true，则每次物品尺寸变化时都会重新创建。
默认值是`true`。

**如何使用：** 调用 `setTextureFollowsItemSize(...)` 修改 `textureFollowsItemSize`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `bool textureFollowsItemSize() const`

**作用与语义：**

该属性控制 FBO 纹理尺寸是否应与`QQuickFramebufferObject`物品的尺寸相符。当该属性为假时，FBO 将在首次显示时创建一次。如果设置为 true，则每次物品尺寸变化时都会重新创建。
默认值是`true`。

**如何使用：** 调用 `textureFollowsItemSize()` 读取当前值；它不会修改应用状态。

### `void mirrorVerticallyChanged(bool)`

**作用与语义：**

该属性控制绘制时 FBO 内容大小是否应垂直镜像。这使得不符合标准期望的第三方渲染代码易于集成。
默认值是`false`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `mirrorVertically` 的变化，不要把它当作普通函数主动调用。

### `void textureFollowsItemSizeChanged(bool)`

**作用与语义：**

该属性控制 FBO 纹理尺寸是否应与`QQuickFramebufferObject`物品的尺寸相符。当该属性为假时，FBO 将在首次显示时创建一次。如果设置为 true，则每次物品尺寸变化时都会重新创建。
默认值是`true`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `textureFollowsItemSize` 的变化，不要把它当作普通函数主动调用。

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

`QQuickFramebufferObject` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
