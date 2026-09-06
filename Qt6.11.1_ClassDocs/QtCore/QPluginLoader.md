# QPluginLoader

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QPluginLoader` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QPluginLoader` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QPluginLoader>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

### 状态、生命周期和线程

**生命周期：** 先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

**状态与结果：** QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

**线程与事件循环：** QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

## 3. 直接使用

使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 属性

- `fileName : QString`
- `loadHints : QLibrary::LoadHints`

### 公有函数

- `QPluginLoader(QObject *parent = nullptr)`
- `QPluginLoader(const QString &fileName, QObject *parent = nullptr)`
- `virtual ~QPluginLoader()`
- `QString errorString() const`
- `QString fileName() const`
- `QObject * instance()`
- `bool isLoaded() const`
- `bool load()`
- `QLibrary::LoadHints loadHints() const`
- `QJsonObject metaData() const`
- `void setFileName(const QString &fileName)`
- `void setLoadHints(QLibrary::LoadHints loadHints)`
- `bool unload()`

### 静态公有成员

- `QObjectList staticInstances()`
- `QList<QStaticPlugin> staticPlugins()`

### 相关非成员函数

- `void qRegisterStaticPluginFunction(QStaticPlugin plugin)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `fileName : QString`

**作用与语义：**

该属性包含插件的文件名。
我们建议在文件名中省略文件后缀，因为`QPluginLoader`会自动查找带有相应后缀的文件（见 `QLibrary::isLibrary()`）。
加载插件时，`QPluginLoader`会搜索`QCoreApplication::libraryPaths()`指定的所有插件位置，除非文件名有绝对路径。成功加载插件后，fileName() 返回插件的完全限定文件名，包括构造函数中给出或传递给 setFileName()的插件完整路径。
如果文件名不存在，则不会设置。该属性将包含空字符串。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `fileName()` 读取当前值；它不会修改应用状态。

### `loadHints : QLibrary::LoadHints`

**作用与语义：**

给`load()`函数一些提示，告诉它应该如何表现。
你可以给插件中符号解析的提示。从Qt 5.7开始默认设置`QLibrary::PreventUnloadHint`。
请参阅`QLibrary::loadHints`文件以了解该物业的完整运作方式。

**如何使用：** 调用 `loadHints()` 读取当前值；它不会修改应用状态。

### `[explicit] QPluginLoader::QPluginLoader(QObject *parent = nullptr)`

**作用与语义：**

用给定的`parent`构建插件加载器。

### `[explicit] QPluginLoader::QPluginLoader(const QString &fileName, QObject *parent = nullptr)`

**作用与语义：**

构建一个插件加载器，包含给定的`parent`，加载`fileName`指定的插件。
要实现可加载，文件的后缀必须是可加载库的有效后缀，符合平台要求，例如Unix上的`.so`，macOS和iOS上的`.dylib`，Windows上的`.dll`。后缀可以通过`QLibrary::isLibrary()`验证。

### `[virtual noexcept] QPluginLoader::~QPluginLoader()`

**作用与语义：**

摧毁`QPluginLoader`物体。
除非`unload()`被明确调用，否则该插件会一直留在内存中，直到应用程序终止。

### `QString QPluginLoader::errorString() const`

**作用与语义：**

返回一个包含最后错误描述的文本字符串。

### `QObject *QPluginLoader::instance()`

**作用与语义：**

返回插件的根组件对象。必要时加载插件。如果插件无法加载或根组件对象无法实例化，函数返回`nullptr`。
如果根组件对象被销毁，调用该函数会创建一个新的实例。
该函数返回的根组件在`QPluginLoader`被销毁时不会被删除。如果你想确保根组件被删除，应该在不需要访问核心组件时尽快调用`unload()`。当库最终卸载时，根组件将被自动删除。
组件对象是一个`QObject`。使用`qobject_cast()`访问你感兴趣的接口。

### `bool QPluginLoader::isLoaded() const`

**作用与语义：**

如果插件已加载，返回`true`;否则返回`false`。

### `bool QPluginLoader::load()`

**作用与语义：**

加载插件并返回 `true` 如果插件成功加载;否则返回 `false`。由于 `instance()` 总是在解析任何符号前调用该函数，因此无需显式调用。在某些情况下，你可能希望插件提前加载，这时你会使用该函数。

### `QJsonObject QPluginLoader::metaData() const`

**作用与语义：**

返回该插件的元数据。元数据是通过编译插件时使用`Q_PLUGIN_METADATA()`宏以json格式指定的数据。
元数据可以快速且廉价地查询，而无需实际加载插件。这使得例如可以将插件的功能存储其中，并根据这些元数据决定是否加载插件。

### `[static] QObjectList QPluginLoader::staticInstances()`

**作用与语义：**

返回插件加载器持有的静态插件实例（根组件）列表。

### `[static] QList<QStaticPlugin> QPluginLoader::staticPlugins()`

**作用与语义：**

返回插件加载器持有的 QStaticPlugins 列表。该函数类似于 `staticInstances()`，但增加了一个`QStaticPlugin`还包含元数据信息。

### `bool QPluginLoader::unload()`

**作用与语义：**

卸载插件并返回`true`如果插件可以卸载;否则返回`false`。
这在应用终止时会自动发生，所以通常不需要调用这个函数。
如果其他`QPluginLoader`实例使用同一插件，调用将失败，卸载只有在每个实例都调用过 unload() 时才会发生。
不要试图删除根组件。相反，依赖 unload() 在需要时会自动删除它。

### `void qRegisterStaticPluginFunction(QStaticPlugin plugin)`

**作用与语义：**

注册插件加载器指定的`plugin`，`Q_IMPORT_PLUGIN()` 使用。

### `QString fileName() const`

**作用与语义：**

该属性包含插件的文件名。
我们建议在文件名中省略文件后缀，因为`QPluginLoader`会自动查找带有相应后缀的文件（见 `QLibrary::isLibrary()`）。
加载插件时，`QPluginLoader`会搜索`QCoreApplication::libraryPaths()`指定的所有插件位置，除非文件名有绝对路径。成功加载插件后，fileName() 返回插件的完全限定文件名，包括构造函数中给出或传递给 setFileName()的插件完整路径。
如果文件名不存在，则不会设置。该属性将包含空字符串。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `fileName()` 读取当前值；它不会修改应用状态。

### `QLibrary::LoadHints loadHints() const`

**作用与语义：**

给`load()`函数一些提示，告诉它应该如何表现。
你可以给插件中符号解析的提示。从Qt 5.7开始默认设置`QLibrary::PreventUnloadHint`。
请参阅`QLibrary::loadHints`文件以了解该物业的完整运作方式。

**如何使用：** 调用 `loadHints()` 读取当前值；它不会修改应用状态。

### `void setFileName(const QString &fileName)`

**作用与语义：**

该属性包含插件的文件名。
我们建议在文件名中省略文件后缀，因为`QPluginLoader`会自动查找带有相应后缀的文件（见 `QLibrary::isLibrary()`）。
加载插件时，`QPluginLoader`会搜索`QCoreApplication::libraryPaths()`指定的所有插件位置，除非文件名有绝对路径。成功加载插件后，fileName() 返回插件的完全限定文件名，包括构造函数中给出或传递给 setFileName()的插件完整路径。
如果文件名不存在，则不会设置。该属性将包含空字符串。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `setFileName(...)` 修改 `fileName`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLoadHints(QLibrary::LoadHints loadHints)`

**作用与语义：**

给`load()`函数一些提示，告诉它应该如何表现。
你可以给插件中符号解析的提示。从Qt 5.7开始默认设置`QLibrary::PreventUnloadHint`。
请参阅`QLibrary::loadHints`文件以了解该物业的完整运作方式。

**如何使用：** 调用 `setLoadHints(...)` 修改 `loadHints`；传入的新值会成为后续查询和相关界面行为所使用的值。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

### 状态和错误边界

QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

### 线程边界

QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

### 最容易出现的错误

不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QPluginLoader` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
