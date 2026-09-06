# QQmlIncubator

> Qt 6.11.1 · Qt Qml

## 1. 先建立直觉

**一句话定位：** `QQmlIncubator` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** 这是 Qt Qml 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QQmlIncubator` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQmlIncubator>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Qml)
target_link_libraries(mytarget PRIVATE Qt6::Qml)
```

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

### 公有类型

- `enum IncubationMode { Asynchronous, AsynchronousIfNested, Synchronous }`
- `enum Status { Null, Ready, Loading, Error }`

### 公有函数

- `QQmlIncubator(QQmlIncubator::IncubationMode mode = Asynchronous)`
- `void clear()`
- `QList<QQmlError> errors() const`
- `void forceCompletion()`
- `QQmlIncubator::IncubationMode incubationMode() const`
- `bool isError() const`
- `bool isLoading() const`
- `bool isNull() const`
- `bool isReady() const`
- `QObject * object() const`
- `void setInitialProperties(const QVariantMap &initialProperties)`
- `QQmlIncubator::Status status() const`

### 保护函数

- `virtual void setInitialState(QObject *object)`
- `virtual void statusChanged(QQmlIncubator::Status status)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QQmlIncubator::IncubationMode`

**作用与语义：**

指定孵化器运行的模式。无论孵化模式如何，如果`QQmlEngine`没有`QQmlIncubationController`集，`QQmlIncubator`都会同步运行。
- `QQmlIncubator::Asynchronous`：`0`;该对象将异步创建。
- `QQmlIncubator::AsynchronousIfNested`：`1`;如果该对象是在已经是异步创建的一部分的上下文中创建的，该孵化器将加入该现有孵化并异步执行。现有孵化器在它和该孵化都完成后才会进入“就绪”状态。否则，孵化将同步执行。
- `QQmlIncubator::Synchronous`：`2`;该对象将同步生成。

### `enum QQmlIncubator::Status`

**作用与语义：**

指定 `QQmlIncubator` 的状态。
- `QQmlIncubator::Null`: `0`；孵化尚未进行。调用 `QQmlComponent::create()` 开始孵化。
- `QQmlIncubator::Ready`: `1`；对象已完全创建，可以通过调用 `object()` 访问。
- `QQmlIncubator::Loading`: `2`；对象正在创建过程中。
- `QQmlIncubator::Error`: `3`；发生错误。可以通过调用 `errors()` 访问错误。

### `QQmlIncubator::QQmlIncubator(QQmlIncubator::IncubationMode mode = Asynchronous)`

**作用与语义：**

创建一个带有指定条件的新孵化器`mode`。

### `void QQmlIncubator::clear()`

**作用与语义：**

清除孵化器。任何进行中的孵化都会被中止。如果孵化器处于准备状态，创建的对象不会被删除。

### `QList<QQmlError> QQmlIncubator::errors() const`

**作用与语义：**

返回孵化过程中遇到的错误列表。

### `void QQmlIncubator::forceCompletion()`

**作用与语义：**

强制任何进行中的孵化同步完成。一旦调用返回，孵化器将不再处于加载状态。

### `QQmlIncubator::IncubationMode QQmlIncubator::incubationMode() const`

**作用与语义：**

返回传递给`QQmlIncubator`构造器的孵化模式。

### `bool QQmlIncubator::isError() const`

**作用与语义：**

如果孵化器的`status()`为错误，则返回为真。

### `bool QQmlIncubator::isLoading() const`

**作用与语义：**

如果孵化器的`status()`处于加载中，则返回为true。

### `bool QQmlIncubator::isNull() const`

**作用与语义：**

如果孵化器的`status()`为Null，则返回为真。

### `bool QQmlIncubator::isReady() const`

**作用与语义：**

如果孵化器的 `status()` 已准备好，则返回为真。

### `QObject *QQmlIncubator::object() const`

**作用与语义：**

如果状态是 Ready，则返回孵化对象，否则返回 0。

### `void QQmlIncubator::setInitialProperties(const QVariantMap &initialProperties)`

**作用与语义：**

存储从属性名称到初始值的映射，包含在`initialProperties`中，孵化组件将用以初始化。

### `[virtual protected] void QQmlIncubator::setInitialState(QObject *object)`

**作用与语义：**

在`object`首次创建后调用，但在复杂属性绑定被评估之前，如果适用，调用`QQmlParserStatus::componentComplete()`。这相当于`QQmlComponent::beginCreate()`和`QQmlComponent::completeCreate()`之间的点，可以用来为对象属性赋予初始值。
默认实现什么都不做。
注意：简单的绑定，如数值文字，是在调用 setInitialState() 之前先评估的。绑定的简单和复杂绑定是有意未明确区分的，且可能因 Qt 版本之间以及你是否以及如何使用 qmlcachegen 而有所变化。你不应依赖于在调用 setInitialState() 之前或之后被评估任何特定绑定。例如，像 MyType.EnumValue 这样的常数表达式在编译时可能被识别为 MyType.EnumValue，或者被推迟执行为绑定。同样适用于常量表达式，如 -（5） 或 “a” “常量字符串”。

### `QQmlIncubator::Status QQmlIncubator::status() const`

**作用与语义：**

返回孵化器的当前状态。

### `[virtual protected] void QQmlIncubator::statusChanged(QQmlIncubator::Status status)`

**作用与语义：**

当孵化器状态发生变化时调用。`status` 是新的状态。 默认实现不执行任何操作。

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

`QQmlIncubator` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
