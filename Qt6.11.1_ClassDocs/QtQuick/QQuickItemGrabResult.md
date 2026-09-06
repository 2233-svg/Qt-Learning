# QQuickItemGrabResult

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QQuickItemGrabResult` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QQuickItemGrabResult` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQuickItemGrabResult>`
- 继承自：QObject
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

### 属性

- `image : const QImage`
- `url : const QUrl`

### 公有函数

- `QImage image() const`
- `bool saveToFile(const QString &fileName) const`
- `(since 6.2) bool saveToFile(const QUrl &filePath) const`
- `QUrl url() const`

### 信号

- `void ready()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[read-only] image : const QImage`

**作用与语义：**

该属性包含抓取的像素结果。
如果抓取尚未完成或失败，则返回空图像（`image.isNull()`返回`true`）。

**如何使用：** 调用 `image()` 读取当前值；它不会修改应用状态。

### `[read-only] url : const QUrl`

**作用与语义：**

该属性包含一个可与基于 URL 的图像消费者（如 QtQuick：：Image 类型）一起使用的 URL。
该URL在`QQuickItemGrabResult`对象被删除前有效。
该URL不代表有效的文件或读取位置，主要作为通过Qt Quick基于图像类型访问图像的密钥。

**如何使用：** 调用 `url()` 读取当前值；它不会修改应用状态。

### `[signal] void QQuickItemGrabResult::ready()`

**作用与语义：**

抓取完成后发出该信号。

### `[invokable] bool QQuickItemGrabResult::saveToFile(const QString &fileName) const`

**作用与语义：**

将抓取结果保存为图像以图像形式保存到`fileName`。成功时返回`true`;否则返回`false`。
注意：在5.9之前的Qt版本中，该功能被标记为非 `const`。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[invokable, since 6.2] bool QQuickItemGrabResult::saveToFile(const QUrl &filePath) const`

**作用与语义：**

将抓取结果保存为图像，`filePath` 必须指向本地文件名且支持的图像格式扩展名。成功时返回`true`;否则返回`false`。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `QImage image() const`

**作用与语义：**

该属性包含抓取的像素结果。
如果抓取尚未完成或失败，则返回空图像（`image.isNull()`返回`true`）。

**如何使用：** 调用 `image()` 读取当前值；它不会修改应用状态。

### `QUrl url() const`

**作用与语义：**

该属性包含一个可与基于 URL 的图像消费者（如 QtQuick：：Image 类型）一起使用的 URL。
该URL在`QQuickItemGrabResult`对象被删除前有效。
该URL不代表有效的文件或读取位置，主要作为通过Qt Quick基于图像类型访问图像的密钥。

**如何使用：** 调用 `url()` 读取当前值；它不会修改应用状态。

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

`QQuickItemGrabResult` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
