# QQmlApplicationEngine

> Qt 6.11.1 · Qt Qml

## 1. 先建立直觉

**一句话定位：** `QQmlApplicationEngine` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** 这是 Qt Qml 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QQmlApplicationEngine` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQmlApplicationEngine>`
- 继承自：QQmlEngine
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

### 公有函数

- `QQmlApplicationEngine(QObject *parent = nullptr)`
- `QQmlApplicationEngine(const QString &filePath, QObject *parent = nullptr)`
- `QQmlApplicationEngine(const QUrl &url, QObject *parent = nullptr)`
- `(since 6.5) QQmlApplicationEngine(QAnyStringView uri, QAnyStringView typeName, QObject *parent = nullptr)`
- `virtual ~QQmlApplicationEngine() override`
- `QList<QObject *> rootObjects() const`

### 公有槽函数

- `void load(const QString &filePath)`
- `void load(const QUrl &url)`
- `void loadData(const QByteArray &data, const QUrl &url = QUrl())`
- `(since 6.5) void loadFromModule(QAnyStringView uri, QAnyStringView typeName)`
- `(since 6.0) void setExtraFileSelectors(const QStringList &extraFileSelectors)`
- `void setInitialProperties(const QVariantMap &initialProperties)`

### 信号

- `void objectCreated(QObject *object, const QUrl &url)`
- `(since 6.4) void objectCreationFailed(const QUrl &url)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QQmlApplicationEngine::QQmlApplicationEngine(QObject *parent = nullptr)`

**作用与语义：**

用给定的 `parent`创建一个新的 QQmlApplicationEngine。你之后需要调用 `load()` 才能加载 QML 文件。

### `QQmlApplicationEngine::QQmlApplicationEngine(const QString &filePath, QObject *parent = nullptr)`

**作用与语义：**

创建一个新的 QQmlApplicationEngine，并在给定的 `filePath` 加载 QML 文件，该文件必须是本地文件或 qrc 路径。如果给出了相对路径，则该路径将被解释为相对于应用的工作目录。
这是出于方便而提供的，类似于使用空构造函数后再调用加载。

### `QQmlApplicationEngine::QQmlApplicationEngine(const QUrl &url, QObject *parent = nullptr)`

**作用与语义：**

创建一个新的 QQmlApplicationEngine，并在给定的 `url` 加载 QML 文件。这是出于方便，类似于使用空构造函数后调用加载。

### `[explicit, since 6.5] QQmlApplicationEngine::QQmlApplicationEngine(QAnyStringView uri, QAnyStringView typeName, QObject *parent = nullptr)`

**作用与语义：**

创建一个新的 QQmlApplicationEngine，加载由 `uri` 和 `typeName` 指定的 QML 类型。这是方便提供，与使用空构造函数后调用 `loadFromModule` 相同。

### `[override virtual noexcept] QQmlApplicationEngine::~QQmlApplicationEngine()`

**作用与语义：**

销毁`QQmlApplicationEngine`及其加载的所有QML对象。

### `[slot] void QQmlApplicationEngine::load(const QString &filePath)`

**作用与语义：**

加载位于 `filePath` 的根 QML 文件。`filePath` 必须是指向本地文件的路径，或资源文件系统中文件的路径。如果 `filePath` 是相对路径，则视为相对于应用程序的工作目录。文件定义的对象树会立即实例化。
如果发生错误，错误消息会与`qWarning`一起打印。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
qmlApplicationEngine， qOverload（&QQmlApplicationEngine：：load））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
qmlApplicationEngine， [receiver = qmlApplicationEngine]（const QString &filePath） { receiver->load（filePath）; }）;


更多示例和方法，请参见连接超载槽位。

### `[slot] void QQmlApplicationEngine::load(const QUrl &url)`

**作用与语义：**

加载位于`url`的根QML文件。文件定义的对象树立即为本地文件URL创建。远程URL异步加载，监听`objectCreated`信号以确定对象树何时准备好。
如果发生错误，`objectCreated`信号会以空指针作为参数发射，错误消息随`qWarning`打印。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
qmlApplicationEngine， qOverload（&QQmlApplicationEngine：：load））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
qmlApplicationEngine， [receiver = qmlApplicationEngine]（const QUrl &url） { receiver->load（url）; }）;


更多示例和方法，请参见连接超载槽位。

### `[slot] void QQmlApplicationEngine::loadData(const QByteArray &data, const QUrl &url = QUrl())`

**作用与语义：**

加载`data`中给出的QML。由`data`定义的对象树会立即实例化。
如果指定了`url`，则该地址作为组件的基础URL。这会影响数据和错误消息中的相对路径。
如果发生错误，错误消息会与`qWarning`一起打印。

### `[slot, since 6.5] void QQmlApplicationEngine::loadFromModule(QAnyStringView uri, QAnyStringView typeName)`

**作用与语义：**

从`uri`指定的模块加载QML类型`typeName`。如果类型来源于位于远程URL的QML文件，则该类型将异步加载。监听`objectCreated`信号以确定对象树何时准备好。
如果发生错误，`objectCreated`信号会以空指针作为参数发射，错误消息随`qWarning`打印。
注意：`uri`识别的模块会在导入路径中被搜索，方式与在QML文件中进行`import uri`搜索相同。如果模块无法在该路径中定位，该函数将失败。

**官方示例：**

```cpp
 QQmlApplicationEngine engine;
 engine.loadFromModule("QtQuick", "Rectangle");
```

### `[signal] void QQmlApplicationEngine::objectCreated(QObject *object, const QUrl &url)`

**作用与语义：**

当对象完成加载时，该信号会发出。如果加载成功，`object`包含指向已加载对象的指针，否则指针为NULL。
同时也提供了`object`所来自组件的`url`。
注意：如果组件路径作为包含相对路径的 `QString` 提供，则`url`将包含文件的完全解析路径。

### `[signal, since 6.4] void QQmlApplicationEngine::objectCreationFailed(const QUrl &url)`

**作用与语义：**

该信号在加载结束时发出，因为发生了错误。
未能加载的组件`url`作为参数提供。
注意：如果组件路径作为包含相对路径的 `QString` 提供，`url` 将包含文件的完全解析路径。

**官方示例：**

```cpp
 QGuiApplication app(argc, argv);
 QQmlApplicationEngine engine;

 // exit on error
 QObject::connect(&engine, &QQmlApplicationEngine::objectCreationFailed,
     &app, []() { QCoreApplication::exit(-1); }, Qt::QueuedConnection);
 engine.load(QUrl());
 return app.exec();
```

### `QList<QObject *> QQmlApplicationEngine::rootObjects() const`

**作用与语义：**

返回由`QQmlApplicationEngine`实例化的所有根对象列表。该列表只包含通过`load()`或便利构造器加载的对象。
注意：在5.9之前的Qt版本中，该功能被标记为非 `const`。

### `[slot, since 6.0] void QQmlApplicationEngine::setExtraFileSelectors(const QStringList &extraFileSelectors)`

**作用与语义：**

设置将 `extraFileSelectors`传递给用于将 URL 解析为本地文件的内部 `QQmlFileSelector`。`extraFileSelectors`在加载第一个 QML 文件时应用。之后设置 QML 文件则无效。

### `[slot] void QQmlApplicationEngine::setInitialProperties(const QVariantMap &initialProperties)`

**作用与语义：**

设置 QML 组件加载后初始化的`initialProperties`。

**官方示例：**

```cpp
 QQmlApplicationEngine engine;

 EventDatabase eventDatabase;
 EventMonitor eventMonitor;

 engine.setInitialProperties({
     { "eventDatabase", QVariant::fromValue(&eventDatabase) },
     { "eventMonitor", QVariant::fromValue(&eventMonitor) }
 });
```

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

`QQmlApplicationEngine` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
