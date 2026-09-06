# QQmlContext

> Qt 6.11.1 · Qt Qml

## 1. 先建立直觉

**一句话定位：** `QQmlContext` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** 这是 Qt Qml 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QQmlContext` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQmlContext>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Qml)
target_link_libraries(mytarget PRIVATE Qt6::Qml)
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

- `struct PropertyPair`

### 公有函数

- `QQmlContext(QQmlContext *parentContext, QObject *parent = nullptr)`
- `QQmlContext(QQmlEngine *engine, QObject *parent = nullptr)`
- `virtual ~QQmlContext() override`
- `QUrl baseUrl() const`
- `(since 6.11) QList<QQmlContext *> childContexts() const`
- `QObject * contextObject() const`
- `QVariant contextProperty(const QString &name) const`
- `QQmlEngine * engine() const`
- `(since 6.11) QObject * findObjectRecursively(const QString &id) const`
- `(since 6.11) QList<QObject *> findObjectsRecursively(const QString &id) const`
- `bool isValid() const`
- `QString nameForObject(const QObject *object) const`
- `(since 6.2) QObject * objectForName(const QString &name) const`
- `QQmlContext * parentContext() const`
- `QUrl resolvedUrl(const QUrl &src) const`
- `void setBaseUrl(const QUrl &baseUrl)`
- `void setContextObject(QObject *object)`
- `void setContextProperties(const QList<QQmlContext::PropertyPair> &properties)`
- `void setContextProperty(const QString &name, QObject *value)`
- `void setContextProperty(const QString &name, const QVariant &value)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QQmlContext::QQmlContext(QQmlContext *parentContext, QObject *parent = nullptr)`

**作用与语义：**

创建一个新的QQmlContext，包含给定的`parentContext`和`QObject` `parent`。

### `QQmlContext::QQmlContext(QQmlEngine *engine, QObject *parent = nullptr)`

**作用与语义：**

创建一个新的 QQmlContext，作为 `engine` 根上下文的子节点，以及`QObject` `parent`。

### `[override virtual noexcept] QQmlContext::~QQmlContext()`

**作用与语义：**

毁掉`QQmlContext`。
任何依赖于该上下文的表达式或子上下文都会被废止，但不会被销毁（除非它们被父级到`QQmlContext`对象）。

### `QUrl QQmlContext::baseUrl() const`

**作用与语义：**

返回组件的基础URL，如果没有设置，则返回包含组件。

### `[since 6.11] QList<QQmlContext *> QQmlContext::childContexts() const`

**作用与语义：**

返回上下文的直接子 QQmlContexts。

### `QObject *QQmlContext::contextObject() const`

**作用与语义：**

返回上下文对象，如果没有上下文对象则返回`nullptr`。

### `QVariant QQmlContext::contextProperty(const QString &name) const`

**作用与语义：**

返回该上下文的`name`属性值作为`QVariant`。如果你知道你寻找的属性是当前上下文中通过QML ID分配的`QObject`，`objectForName()`更方便、更快。与`objectForName()`和`nameForObject()`不同，该方法会穿越上下文层级，如果当前上下文中找不到`name`，则在父上下文中搜索。它还考虑你可能设置的任何`contextObject()`。

### `QQmlEngine *QQmlContext::engine() const`

**作用与语义：**

返回上下文的 `QQmlEngine`，或者如果上下文没有 `QQmlEngine` 或`QQmlEngine`被销毁，则返回`nullptr`。

### `[since 6.11] QObject *QQmlContext::findObjectRecursively(const QString &id) const`

**作用与语义：**

递归地在该上下文及其子节点中搜索ID为`id`的对象。如果找到这样的对象，则返回该对象。否则返回`nullptr`。
在给定上下文中，只能有一个具有给定`id`的对象，但你可以在一个文档内创建多个上下文，例如视图和代理。每个上下文都可以包含具有给定`id`的对象。这里只返回第一个找到的对象。搜索采用广度优先搜索。

### `[since 6.11] QList<QObject *> QQmlContext::findObjectsRecursively(const QString &id) const`

**作用与语义：**

递归地在该上下文及其子节点中搜索具有 ID `id` 的对象。返回这些对象的列表。
在任何给定上下文中，只能有一个具有给定`id`的对象，但你可以在一个文档中创建多个上下文，例如视图和代理。每个上下文都可以包含一个具有给定`id`的对象。

### `bool QQmlContext::isValid() const`

**作用与语义：**

返回上下文是否有效。
要有效，上下文必须有引擎，且该引擎`contextObject()`（如果有的话）必须未被删除。

### `QString QQmlContext::nameForObject(const QObject *object) const`

**作用与语义：**

返回该上下文中的`object`名称，若上下文中未命名`object`则返回空字符串。对象由`setContextProperty()`命名，或作为上下文对象的属性命名，QML创建上下文则由ID命名。
如果对象有多个名称，返回第一个名称。
与`contextProperty()`不同，该方法不遍历上下文层级。如果当前上下文中找不到该名称，则返回空字符串。

### `[since 6.2] QObject *QQmlContext::objectForName(const QString &name) const`

**作用与语义：**

在此上下文中返回给定`name`的对象。如果上下文中`name`不可得或与`name`关联的值不是`QObject`，则返回 nullptr。对象由`setContextProperty()`命名，或作为上下文对象的属性命名，QML创建上下文则通过id命名。与`contextProperty()`不同，该方法不遍历上下文层级。如果当前上下文中找不到该名称，则返回nullptr。

### `QQmlContext *QQmlContext::parentContext() const`

**作用与语义：**

返回上下文的父 `QQmlContext`，或者如果该上下文没有父上下文或父上下文已被销毁，则返回`nullptr`。

### `QUrl QQmlContext::resolvedUrl(const QUrl &src) const`

**作用与语义：**

解析 URL `src`相对于包含组件的 URL 进行解析。

### `void QQmlContext::setBaseUrl(const QUrl &baseUrl)`

**作用与语义：**

明确设置`resolvedUrl()`用于相对引用`baseUrl`的URL。
调用该函数会覆盖默认使用的包含组件的URL。

### `void QQmlContext::setContextObject(QObject *object)`

**作用与语义：**

设定背景`object`。
注意：你不应该用上下文对象来注入 QML 组件中的值。请使用单例或普通对象属性。

### `void QQmlContext::setContextProperties(const QList<QQmlContext::PropertyPair> &properties)`

**作用与语义：**

在这个背景下设置一批`properties`。
将所有属性集中在一个批次中可以避免不必要的刷新表达式，因此建议不要为每个属性调用`setContextProperty()`。
注意：你不应该用上下文属性来注入 QML 组件中的值。应该用单例或普通对象属性来代替。

### `void QQmlContext::setContextProperty(const QString &name, QObject *value)`

**作用与语义：**

在此上下文下设置`name`属性的 `value`。
`QQmlContext`不对`value`拥有所有权。
注意：你不应该用上下文属性来注入 QML 组件中的值。应该用单例或普通对象属性来代替。

### `void QQmlContext::setContextProperty(const QString &name, const QVariant &value)`

**作用与语义：**

在此上下文下设置`name`属性的 `value`。
注意：你不应该用上下文属性来注入 QML 组件中的值。应该用单例或普通对象属性来代替。

### `struct PropertyPair`

**作用与语义：**

该结构包含属性名称和属性值。它被用作`setContextProperties`函数的参数。

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

`QQmlContext` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
