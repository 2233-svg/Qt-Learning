# QQmlComponent

> Qt 6.11.1 · Qt Qml

## 1. 先建立直觉

**一句话定位：** `QQmlComponent` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** 这是 Qt Qml 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QQmlComponent` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQmlComponent>`
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

- `enum CompilationMode { PreferSynchronous, Asynchronous }`
- `enum Status { Null, Ready, Loading, Error }`

### 属性

- `progress : qreal`
- `status : Status`
- `url : const QUrl`

### 公有函数

- `QQmlComponent(QQmlEngine *engine, QObject *parent = nullptr)`
- `QQmlComponent(QQmlEngine *engine, const QString &fileName, QObject *parent = nullptr)`
- `QQmlComponent(QQmlEngine *engine, const QUrl &url, QObject *parent = nullptr)`
- `QQmlComponent(QQmlEngine *engine, const QString &fileName, QQmlComponent::CompilationMode mode, QObject *parent = nullptr)`
- `QQmlComponent(QQmlEngine *engine, const QUrl &url, QQmlComponent::CompilationMode mode, QObject *parent = nullptr)`
- `(since 6.5) QQmlComponent(QQmlEngine *engine, QAnyStringView uri, QAnyStringView typeName, QObject *parent = nullptr)`
- `(since 6.5) QQmlComponent(QQmlEngine *engine, QAnyStringView uri, QAnyStringView typeName, QQmlComponent::CompilationMode mode, QObject *parent = nullptr)`
- `virtual ~QQmlComponent() override`
- `virtual QObject * beginCreate(QQmlContext *context)`
- `virtual void completeCreate()`
- `virtual QObject * create(QQmlContext *context = nullptr)`
- `void create(QQmlIncubator &incubator, QQmlContext *context = nullptr, QQmlContext *forContext = nullptr)`
- `QObject * createWithInitialProperties(const QVariantMap &initialProperties, QQmlContext *context = nullptr)`
- `QQmlContext * creationContext() const`
- `QQmlEngine * engine() const`
- `QList<QQmlError> errors() const`
- `(since 6.5) bool isBound() const`
- `bool isError() const`
- `bool isLoading() const`
- `bool isNull() const`
- `bool isReady() const`
- `qreal progress() const`
- `void setInitialProperties(QObject *object, const QVariantMap &properties)`
- `QQmlComponent::Status status() const`
- `QUrl url() const`

### 公有槽函数

- `(since 6.5) void loadFromModule(QAnyStringView uri, QAnyStringView typeName, QQmlComponent::CompilationMode mode = PreferSynchronous)`
- `void loadUrl(const QUrl &url)`
- `void loadUrl(const QUrl &url, QQmlComponent::CompilationMode mode)`
- `void setData(const QByteArray &data, const QUrl &url)`

### 信号

- `void progressChanged(qreal progress)`
- `void statusChanged(QQmlComponent::Status status)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QQmlComponent::CompilationMode`

**作用与语义：**

指定`QQmlComponent`应立即加载组件还是异步加载。
- `QQmlComponent::PreferSynchronous`：`0`;倾向于立即加载/编译组件，阻断线程。这并非总是可行;例如，远程 URL 总是异步加载。
- `QQmlComponent::Asynchronous`：`1`;在后台线程中加载/编译组件。

### `enum QQmlComponent::Status`

**作用与语义：**

指定`QQmlComponent`的加载状态。
- `QQmlComponent::Null`：`0`;该`QQmlComponent`没有数据。调用`loadUrl()`或 `setData()` 以添加量子ML内容。
- `QQmlComponent::Ready`：`1`;本 `QQmlComponent` 已准备好，`create()`可被召唤。
- `QQmlComponent::Loading`：`2`;该`QQmlComponent`正在加载网络数据。
- `QQmlComponent::Error`：`3`;发生错误。调用`errors()`获取`errors`列表。

### `[read-only] progress : qreal`

**作用与语义：**

加载组件的进度，从0.0（未加载）到1.0（完成）。

**如何使用：** 调用 `progress()` 读取当前值；它不会修改应用状态。

### `[read-only] status : Status`

**作用与语义：**

该组件当前的 `status`。

**如何使用：** 调用 `status()` 读取当前值；它不会修改应用状态。

### `[read-only] url : const QUrl`

**作用与语义：**

组件 URL。 这是传递给构造函数、`loadUrl()` 或 `setData()` 方法的 URL。

**如何使用：** 调用 `url()` 读取当前值；它不会修改应用状态。

### `QQmlComponent::QQmlComponent(QQmlEngine *engine, QObject *parent = nullptr)`

**作用与语义：**

创建一个没有数据的 QQmlComponent，给它指定的`engine`和`parent`。用 `setData()` 设置数据。

### `QQmlComponent::QQmlComponent(QQmlEngine *engine, const QString &fileName, QObject *parent = nullptr)`

**作用与语义：**

从给定的`fileName`创建一个QQmlComponent，并赋予它指定的`parent`和`engine`。

### `QQmlComponent::QQmlComponent(QQmlEngine *engine, const QUrl &url, QObject *parent = nullptr)`

**作用与语义：**

从给定的`url`创建一个QQmlComponent，并赋予它指定的`parent`和`engine`。
确保提供的URL完整且正确，特别是在从本地文件系统加载文件时使用`QUrl::fromLocalFile()`。
相对路径将以`QQmlEngine::baseUrl()`解析，除非特别说明，否则这是当前的工作目录。

### `QQmlComponent::QQmlComponent(QQmlEngine *engine, const QString &fileName, QQmlComponent::CompilationMode mode, QObject *parent = nullptr)`

**作用与语义：**

从给定的`fileName`创建一个QQmlComponent，并赋予其指定的`parent`和`engine`。如果`mode` `Asynchronous`，该组件将被异步加载和编译。

### `QQmlComponent::QQmlComponent(QQmlEngine *engine, const QUrl &url, QQmlComponent::CompilationMode mode, QObject *parent = nullptr)`

**作用与语义：**

从给定的`url`创建一个QQmlComponent，并赋予其指定的`parent`和 `engine`。如果`mode` `Asynchronous`，该组件将被异步加载和编译。
确保提供的URL完整且正确，特别是在从本地文件系统加载文件时使用`QUrl::fromLocalFile()`。
相对路径将以`QQmlEngine::baseUrl()`解析，除非特别说明，否则这是当前的工作目录。

### `[explicit, since 6.5] QQmlComponent::QQmlComponent(QQmlEngine *engine, QAnyStringView uri, QAnyStringView typeName, QObject *parent = nullptr)`

**作用与语义：**

从给定的 `uri` 创建 QQmlComponent，`typeName`并赋予其指定的`parent`和`engine`。如果可能，组件将同步加载。

### `[explicit, since 6.5] QQmlComponent::QQmlComponent(QQmlEngine *engine, QAnyStringView uri, QAnyStringView typeName, QQmlComponent::CompilationMode mode, QObject *parent = nullptr)`

**作用与语义：**

从给定的`uri`和`typeName`创建一个QQmlComponent，并赋予其指定的 `parent` 和`engine`。如果`mode` `Asynchronous`，该组件将被异步加载和编译。

### `[override virtual noexcept] QQmlComponent::~QQmlComponent()`

**作用与语义：**

摧毁`QQmlComponent`。

### `[virtual] QObject *QQmlComponent::beginCreate(QQmlContext *context)`

**作用与语义：**

在指定的`context`内，从该组件创建一个对象实例。如果创建失败，返回`nullptr`。
注意：该方法提供了对组件实例创建的高级控制。一般来说，程序员应使用`QQmlComponent::create()`来创建对象实例。
`QQmlComponent`构造实例时，分为三个步骤：
- 创建对象层级，并赋予常数值。
- 首次评估属性绑定。
- 如适用，`QQmlParserStatus::componentComplete()` 在对象上被调用。
QQmlComponent：：beginCreate() 与 `QQmlComponent::create()` 不同，它只执行第 1 步。`QQmlComponent::completeCreate()` 必须被调用才能完成第 2 和第 3 步。
当使用附加属性向实例化组件传递信息时，这个断点有时非常有用，因为它允许在属性绑定生效前配置其初始值。
返回对象实例的所有权转移给调用者。
注意：绑定的分类为常值和实际绑定，是有意未具体说明的，且可能因Qt版本及你是否以及如何使用qmlcachegen而有所变化。你不应依赖任何特定绑定在bestartCreate()返回前后被评估。例如，像MyType.EnumValue这样的常数表达式在编译时可能被识别为此类，或被推迟执行为绑定。常量表达式如-（5）或“a”常量字符串“也是如此。

### `[virtual] void QQmlComponent::completeCreate()`

**作用与语义：**

该方法提供了对组件实例创建的高级控制。一般来说，程序员应使用`QQmlComponent::create()`来创建组件。
该函数完成了以 `QQmlComponent::beginCreate()` 开始的组件创建，之后必须调用。

### `[virtual] QObject *QQmlComponent::create(QQmlContext *context = nullptr)`

**作用与语义：**

在指定的`context`内，从该组件创建一个对象实例。如果创建失败，返回`nullptr`。
如果`context`是`nullptr`（默认），它会在引擎的根上下文中创建实例。
返回对象实例的所有权转移给调用者。
如果从该组件创建的对象是视觉项，则必须有视觉父，可通过调用`QQuickItem::setParentItem()`设置。详情请参见Qt Quick中的概念 - 视觉父。

### `void QQmlComponent::create(QQmlIncubator &incubator, QQmlContext *context = nullptr, QQmlContext *forContext = nullptr)`

**作用与语义：**

利用提供的`incubator`从该组件创建对象实例。`context`指定创建该对象实例的上下文。
如果`context`是`nullptr`（默认），它会在引擎的根上下文中创建实例。
`forContext` 指定了该对象创建依赖的上下文。如果`forContext`是异步创建，且`QQmlIncubator::IncubationMode`是`QQmlIncubator::AsynchronousIfNested`，则该对象也会异步创建。如果`forContext`是`nullptr`（默认），则该`context`将用于此决策。
创建的对象及其创建状态可以通过`incubator`获取。

### `QObject *QQmlComponent::createWithInitialProperties(const QVariantMap &initialProperties, QQmlContext *context = nullptr)`

**作用与语义：**

在指定`context`内创建该组件的对象实例，并用`initialProperties`初始化其顶层属性。
如果无法设置任何`initialProperties`，会发出警告。如果有未设置的必需属性，创建对象失败并返回`nullptr`，此时`isError()`返回`true`。
如果`context`是`nullptr`（默认），它会在引擎的根上下文中创建实例。
返回对象实例的所有权转移给调用者。

### `QQmlContext *QQmlComponent::creationContext() const`

**作用与语义：**

返回组件创建的 `QQmlContext`。这仅适用于直接从 QML 创建的组件。

### `QQmlEngine *QQmlComponent::engine() const`

**作用与语义：**

返回该组件的`QQmlEngine`。

### `QList<QQmlError> QQmlComponent::errors() const`

**作用与语义：**

返回上次编译或创建操作中发生的错误列表。如果没有设置`isError()`，则返回一个空列表。

### `[since 6.5] bool QQmlComponent::isBound() const`

**作用与语义：**

如果组件是在指定`pragma ComponentBehavior: Bound`的QML文件中创建的，则返回true;否则返回false。

### `bool QQmlComponent::isError() const`

**作用与语义：**

如果`status()` 则返回为真 == `QQmlComponent::Error`。

### `bool QQmlComponent::isLoading() const`

**作用与语义：**

如果`status()` 则返回为真 == `QQmlComponent::Loading`。

### `bool QQmlComponent::isNull() const`

**作用与语义：**

如果`status()` 则返回为真 == `QQmlComponent::Null`。

### `bool QQmlComponent::isReady() const`

**作用与语义：**

如果`status()` 则返回为真 == `QQmlComponent::Ready`。

### `[slot, since 6.5] void QQmlComponent::loadFromModule(QAnyStringView uri, QAnyStringView typeName, QQmlComponent::CompilationMode mode = PreferSynchronous)`

**作用与语义：**

在模块 `uri` 中加载 `typeName` 对应的 `QQmlComponent`。如果类型是通过 QML 文件实现的，则使用 `mode` 来加载它。由 C 支持的类型总是同步加载。

**官方示例：**

```cpp
 QQmlEngine engine;
 QQmlComponent component(&engine);
 component.loadFromModule("QtQuick", "Item");
 // once the component is ready
 std::unique_ptr<QObject> item(component.create());
 Q_ASSERT(item->metaObject() == &QQuickItem::staticMetaObject);
```

### `[slot] void QQmlComponent::loadUrl(const QUrl &url)`

**作用与语义：**

从提供的 `url` 加载 `QQmlComponent`。
确保提供的 URL 是完整且正确的，特别是从本地文件系统加载文件时，请使用 `QUrl::fromLocalFile()`。
相对路径将相对于 `QQmlEngine::baseUrl()` 解析，除非另有指定，该目录为当前工作目录。
注意：此槽函数是重载的。要连接到此槽函数：

// 使用 qOverload 连接：
connect(sender, &SenderClass::signal,。
qmlComponent, qOverload(&QQmlComponent::loadUrl));

// 或使用 lambda 作为封装：
connect(sender, &SenderClass::signal,。
qmlComponent, [receiver = qmlComponent](const QUrl &url) { receiver->loadUrl(url); });

有关更多示例和方法，请参阅连接到重载槽函数。

### `[slot] void QQmlComponent::loadUrl(const QUrl &url, QQmlComponent::CompilationMode mode)`

**作用与语义：**

从提供的 `url` 加载 `QQmlComponent`。如果 `mode` 是 `Asynchronous`，组件将异步加载和编译。
确保提供的 URL 是完整且正确的，特别是从本地文件系统加载文件时，请使用 `QUrl::fromLocalFile()`。
相对路径将相对于 `QQmlEngine::baseUrl()` 解析，除非另有指定，该目录为当前工作目录。
注意：此槽函数是重载的。要连接到此槽函数：

// 使用 qOverload 连接：
connect(sender, &SenderClass::signal,。
qmlComponent, qOverload(&QQmlComponent::loadUrl));

// 或使用 lambda 作为封装：
connect(sender, &SenderClass::signal,。
qmlComponent, [receiver = qmlComponent](const QUrl &url, QQmlComponent::CompilationMode mode) { receiver->loadUrl(url, mode); });

有关更多示例和方法，请参阅连接到重载槽函数。

### `[signal] void QQmlComponent::progressChanged(qreal progress)`

**作用与语义：**

加载组件的进度，从0.0（未加载）到1.0（完成）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `progress` 的变化，不要把它当作普通函数主动调用。

### `[slot] void QQmlComponent::setData(const QByteArray &data, const QUrl &url)`

**作用与语义：**

设置`QQmlComponent`使用给定的QML的 `data`。如果提供了`url`，则用于设置组件名称并为该组件解析的项目提供基础路径。
警告：新组件会对同一URL的现有组件进行影子。你不应传递现有组件的URL。

### `void QQmlComponent::setInitialProperties(QObject *object, const QVariantMap &properties)`

**作用与语义：**

设置由`QQmlComponent`创建的`object`的顶层`properties`。
该方法提供了对组件实例创建的高级控制。一般来说，程序员应使用`QQmlComponent::createWithInitialProperties`从组件创建对象实例。
在`beginCreate`之后、`completeCreate`被调用之前使用此方法。如果不存在所提供的属性，会发出警告。
该方法不允许直接设置初始嵌套属性。相反，可以通过创建价值类型，赋值其嵌套属性，然后将该值类型作为待构造对象的初始属性传递来实现。
例如，为了设置 fond.bold，你可以创建一个`QFont`，将其粗体设置为加粗，然后将字体作为初始属性传递。

### `[signal] void QQmlComponent::statusChanged(QQmlComponent::Status status)`

**作用与语义：**

该组件当前的 `status`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `status` 的变化，不要把它当作普通函数主动调用。

### `qreal progress() const`

**作用与语义：**

加载组件的进度，从0.0（未加载）到1.0（完成）。

**如何使用：** 调用 `progress()` 读取当前值；它不会修改应用状态。

### `QQmlComponent::Status status() const`

**作用与语义：**

该组件当前的 `status`。

**如何使用：** 调用 `status()` 读取当前值；它不会修改应用状态。

### `QUrl url() const`

**作用与语义：**

组件 URL。 这是传递给构造函数、`loadUrl()` 或 `setData()` 方法的 URL。

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

`QQmlComponent` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
