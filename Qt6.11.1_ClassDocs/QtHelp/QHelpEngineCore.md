# QHelpEngineCore

> Qt 6.11.1 · Qt Help

## 1. 先建立直觉

**一句话定位：** `QHelpEngineCore` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** 这是 Qt Help 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QHelpEngineCore` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QHelpEngineCore>`
- 继承自：QObject
- 直接派生类：QHelpEngine

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Help)
target_link_libraries(mytarget PRIVATE Qt6::Help)
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

- `autoSaveFilter : bool`
- `collectionFile : QString`
- `(since 6.0) readOnly : bool`

### 公有函数

- `QHelpEngineCore(const QString &collectionFile, QObject *parent = nullptr)`
- `virtual ~QHelpEngineCore()`
- `bool autoSaveFilter() const`
- `QString collectionFile() const`
- `bool copyCollectionFile(const QString &fileName)`
- `QVariant customValue(const QString &key, const QVariant &defaultValue = {}) const`
- `QString documentationFileName(const QString &namespaceName)`
- `QList<QHelpLink> documentsForIdentifier(const QString &id) const`
- `QList<QHelpLink> documentsForIdentifier(const QString &id, const QString &filterName) const`
- `QList<QHelpLink> documentsForKeyword(const QString &keyword) const`
- `QList<QHelpLink> documentsForKeyword(const QString &keyword, const QString &filterName) const`
- `QString error() const`
- `QByteArray fileData(const QUrl &url) const`
- `QList<QUrl> files(const QString namespaceName, const QString &filterName, const QString &extensionFilter = {})`
- `QHelpFilterEngine * filterEngine() const`
- `QUrl findFile(const QUrl &url) const`
- `bool isReadOnly() const`
- `bool registerDocumentation(const QString &documentationFileName)`
- `QStringList registeredDocumentations() const`
- `bool removeCustomValue(const QString &key)`
- `void setAutoSaveFilter(bool save)`
- `void setCollectionFile(const QString &fileName)`
- `bool setCustomValue(const QString &key, const QVariant &value)`
- `void setReadOnly(bool enable)`
- `void setUsesFilterEngine(bool uses)`
- `bool setupData()`
- `bool unregisterDocumentation(const QString &namespaceName)`
- `bool usesFilterEngine() const`

### 信号

- `void setupFinished()`
- `void setupStarted()`
- `void warning(const QString &msg)`

### 静态公有成员

- `QVariant metaData(const QString &documentationFileName, const QString &name)`
- `QString namespaceName(const QString &documentationFileName)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `autoSaveFilter : bool`

**作用与语义：**

无论`QHelpEngineCore`是否处于自动保存过滤模式，这个特性都适用。
如果`QHelpEngineCore`处于自动保存过滤器模式，当前过滤器在被`QHelpFilterEngine::setActiveFilter()`函数更改时会自动保存。过滤器会永久保存在帮助收集文件中。
默认情况下，这个模式是开启的。

**如何使用：** 调用 `autoSaveFilter()` 读取当前值；它不会修改应用状态。

### `collectionFile : QString`

**作用与语义：**

该属性包含当前使用的集合文件的绝对文件名。
设置该属性会使帮助引擎处于无效状态。重新设置帮助引擎时，调用`setupData()`或任何获取函数非常重要。

**如何使用：** 调用 `collectionFile()` 读取当前值；它不会修改应用状态。

### `[since 6.0] readOnly : bool`

**作用与语义：**

该属性决定帮助引擎是否为只读。
在只读模式下，用户可以在只读位置安装集合文件后使用帮助引擎。在这种情况下，一些功能将无法访问，比如注册额外文档、过滤编辑，或任何需要修改集合文件的操作。将其设置为`false`则可以实现帮助引擎的完整功能。
默认情况下，该属性为`true`。

**如何使用：** 调用 `readOnly()` 读取当前值；它不会修改应用状态。

### `[explicit] QHelpEngineCore::QHelpEngineCore(const QString &collectionFile, QObject *parent = nullptr)`

**作用与语义：**

构建一个带有`parent`的新核心帮助引擎。帮助引擎利用`collectionFile`中存储的信息提供帮助。如果集合文件尚未存在，将会被创建。

### `[virtual noexcept] QHelpEngineCore::~QHelpEngineCore()`

**作用与语义：**

摧毁了辅助引擎。

### `bool QHelpEngineCore::copyCollectionFile(const QString &fileName)`

**作用与语义：**

创建文件`fileName`并将当前集合文件的所有内容复制到新创建的文件中，成功时返回 true;否则返回 false。
复制过程确保与 Qt Collection 文件（`.qch`）文件的引用相应更新。

### `QVariant QHelpEngineCore::customValue(const QString &key, const QVariant &defaultValue = {}) const`

**作用与语义：**

返回分配给`key`的值。如果请求的密钥不存在，则返回指定的`defaultValue`。

### `QString QHelpEngineCore::documentationFileName(const QString &namespaceName)`

**作用与语义：**

返回由`namespaceName`标识的Qt压缩帮助文件的绝对文件名（.qch）。如果没有指定命名空间的Qt压缩帮助文件，则返回空字符串。

### `QList<QHelpLink> QHelpEngineCore::documentsForIdentifier(const QString &id) const`

**作用与语义：**

返回`id`中所有文档链接的列表。返回的列表内容取决于当前过滤器，因此只返回当前过滤器注册的关键词。

### `QList<QHelpLink> QHelpEngineCore::documentsForIdentifier(const QString &id, const QString &filterName) const`

**作用与语义：**

返回`id`中找到的文档链接列表，并按`filterName`过滤。返回的列表内容取决于已通过的过滤器，因此只返回该过滤器注册的关键词。如果你想让所有结果都无过滤，请将空字符串当作`filterName`。

### `QList<QHelpLink> QHelpEngineCore::documentsForKeyword(const QString &keyword) const`

**作用与语义：**

返回`keyword`中所有文档链接的列表。返回的列表内容取决于当前过滤器，因此只返回当前过滤器注册的关键词。

### `QList<QHelpLink> QHelpEngineCore::documentsForKeyword(const QString &keyword, const QString &filterName) const`

**作用与语义：**

返回`keyword`中找到的文档链接列表，并按`filterName`过滤。返回的列表内容取决于已通过的过滤器，因此只返回该过滤器注册的关键词。如果你想让所有结果都无过滤，请将空字符串当作`filterName`传递。

### `QString QHelpEngineCore::error() const`

**作用与语义：**

返回最后发生错误的描述。

### `QByteArray QHelpEngineCore::fileData(const QUrl &url) const`

**作用与语义：**

返回`url`指定的文件数据。如果文件不存在，则返回空`QByteArray`。

### `QList<QUrl> QHelpEngineCore::files(const QString namespaceName, const QString &filterName, const QString &extensionFilter = {})`

**作用与语义：**

返回 Qt 压缩帮助文件中的文件列表，供 `namespaceName` 使用。文件可按`filterName`或扩展名`extensionFilter`（例如“html”）进行过滤。

### `QHelpFilterEngine *QHelpEngineCore::filterEngine() const`

**作用与语义：**

返回与该辅助引擎关联的过滤引擎。过滤引擎允许添加、更改和移除该辅助引擎的现有过滤器。使用该引擎还需调用`setUsesFilterEngine()`设置为`true`。

### `QUrl QHelpEngineCore::findFile(const QUrl &url) const`

**作用与语义：**

返回修正后的`url` URL，该URL可能指向由`url`中定义的虚拟文件夹定义的不同命名空间。如果虚拟文件夹与`url`的命名空间匹配，方法仅检查文件是否存在并返回相同的`url`。当虚拟文件夹与`url`的命名空间不匹配时，尝试根据活动过滤器寻找最佳匹配命名空间。找到命名空间后，如果文件存在，则返回修正后的URL，否则返回无效URL。

### `[static] QVariant QHelpEngineCore::metaData(const QString &documentationFileName, const QString &name)`

**作用与语义：**

返回Qt压缩帮助文件的元数据`documentationFileName`。如果没有可用的`name`数据，则返回无效的QVariant()。元数据在创建Qt压缩帮助文件时定义，之后不可修改。常见元数据包括例如文档作者。

### `[static] QString QHelpEngineCore::namespaceName(const QString &documentationFileName)`

**作用与语义：**

返回由其`documentationFileName`指定的Qt压缩帮助文件（.qch）定义的命名空间名称。如果文件无效，返回空字符串。

### `bool QHelpEngineCore::registerDocumentation(const QString &documentationFileName)`

**作用与语义：**

注册文件`documentationFileName`中包含的Qt压缩帮助文件（.qch）。一个压缩帮助文件，其命名空间唯一标识，只能注册一次。如果注册成功，返回为真，否则返回为假。

### `QStringList QHelpEngineCore::registeredDocumentations() const`

**作用与语义：**

返回当前集合文件中所有注册的 Qt 压缩帮助文件列表。返回的名称是注册 Qt 压缩帮助文件（.qch）的命名空间。

### `bool QHelpEngineCore::removeCustomValue(const QString &key)`

**作用与语义：**

从集合文件中的设置部分移除`key`。如果值成功移除，则返回true，否则返回false。

### `bool QHelpEngineCore::setCustomValue(const QString &key, const QVariant &value)`

**作用与语义：**

将`value`保存在`key`下。如果键已经存在，该值将被覆盖。如果成功保存值，返回真，否则返回false。

### `void QHelpEngineCore::setUsesFilterEngine(bool uses)`

**作用与语义：**

根据传递的 `uses` 参数启用或禁用帮助引擎内的新滤波器引擎功能。

### `bool QHelpEngineCore::setupData()`

**作用与语义：**

通过处理集合文件中的信息来设置帮助引擎，成功时返回true;否则返回false。
调用该函数时，帮助引擎被迫立即初始化自身。大多数情况下，这个函数不必显式调用，因为依赖正确设置帮助引擎的获取函数会自行初始化。
注意：`qsqlite4.dll`需要随应用部署，因为帮助系统在加载帮助集合时使用了 sqlite 驱动。

### `[signal] void QHelpEngineCore::setupFinished()`

**作用与语义：**

该信号在设置完成后发出。

### `[signal] void QHelpEngineCore::setupStarted()`

**作用与语义：**

该信号在设置启动时发出。

### `bool QHelpEngineCore::unregisterDocumentation(const QString &namespaceName)`

**作用与语义：**

取消注册 Qt 压缩帮助文件（.qch），该文件由帮助集合中的`namespaceName`识别。成功时返回 true，成功时返回 false。

### `bool QHelpEngineCore::usesFilterEngine() const`

**作用与语义：**

返回帮助引擎是否使用了新的过滤功能。

### `[signal] void QHelpEngineCore::warning(const QString &msg)`

**作用与语义：**

当发生非关键错误时，该信号会发出。警告消息存储在`msg`中。

### `bool autoSaveFilter() const`

**作用与语义：**

无论`QHelpEngineCore`是否处于自动保存过滤模式，这个特性都适用。
如果`QHelpEngineCore`处于自动保存过滤器模式，当前过滤器在被`QHelpFilterEngine::setActiveFilter()`函数更改时会自动保存。过滤器会永久保存在帮助收集文件中。
默认情况下，这个模式是开启的。

**如何使用：** 调用 `autoSaveFilter()` 读取当前值；它不会修改应用状态。

### `QString collectionFile() const`

**作用与语义：**

该属性包含当前使用的集合文件的绝对文件名。
设置该属性会使帮助引擎处于无效状态。重新设置帮助引擎时，调用`setupData()`或任何获取函数非常重要。

**如何使用：** 调用 `collectionFile()` 读取当前值；它不会修改应用状态。

### `bool isReadOnly() const`

**作用与语义：**

该属性决定帮助引擎是否为只读。
在只读模式下，用户可以在只读位置安装集合文件后使用帮助引擎。在这种情况下，一些功能将无法访问，比如注册额外文档、过滤编辑，或任何需要修改集合文件的操作。将其设置为`false`则可以实现帮助引擎的完整功能。
默认情况下，该属性为`true`。

**如何使用：** 调用 `isReadOnly()` 读取当前值；它不会修改应用状态。

### `void setAutoSaveFilter(bool save)`

**作用与语义：**

无论`QHelpEngineCore`是否处于自动保存过滤模式，这个特性都适用。
如果`QHelpEngineCore`处于自动保存过滤器模式，当前过滤器在被`QHelpFilterEngine::setActiveFilter()`函数更改时会自动保存。过滤器会永久保存在帮助收集文件中。
默认情况下，这个模式是开启的。

**如何使用：** 调用 `setAutoSaveFilter(...)` 修改 `autoSaveFilter`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setCollectionFile(const QString &fileName)`

**作用与语义：**

该属性包含当前使用的集合文件的绝对文件名。
设置该属性会使帮助引擎处于无效状态。重新设置帮助引擎时，调用`setupData()`或任何获取函数非常重要。

**如何使用：** 调用 `setCollectionFile(...)` 修改 `collectionFile`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setReadOnly(bool enable)`

**作用与语义：**

该属性决定帮助引擎是否为只读。
在只读模式下，用户可以在只读位置安装集合文件后使用帮助引擎。在这种情况下，一些功能将无法访问，比如注册额外文档、过滤编辑，或任何需要修改集合文件的操作。将其设置为`false`则可以实现帮助引擎的完整功能。
默认情况下，该属性为`true`。

**如何使用：** 调用 `setReadOnly(...)` 修改 `readOnly`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QHelpEngineCore` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
