# QQmlEngine

> Qt 6.11.1 · Qt Qml

## 1. 先建立直觉

**一句话定位：** `QQmlEngine` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** 这是 Qt Qml 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QQmlEngine` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQmlEngine>`
- 继承自：QJSEngine
- 直接派生类：QQmlApplicationEngine

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

### 属性

- `offlineStoragePath : QString`

### 公有函数

- `QQmlEngine(QObject *parent = nullptr)`
- `virtual ~QQmlEngine() override`
- `void addImageProvider(const QString &providerId, QQmlImageProviderBase *provider)`
- `void addImportPath(const QString &path)`
- `void addPluginPath(const QString &path)`
- `void addUrlInterceptor(QQmlAbstractUrlInterceptor *urlInterceptor)`
- `QUrl baseUrl() const`
- `void clearComponentCache()`
- `void clearSingletons()`
- `QQmlImageProviderBase * imageProvider(const QString &providerId) const`
- `QStringList importPathList() const`
- `QQmlIncubationController * incubationController() const`
- `QUrl interceptUrl(const QUrl &url, QQmlAbstractUrlInterceptor::DataType type) const`
- `(since 6.6) void markCurrentFunctionAsTranslationBinding()`
- `QNetworkAccessManager * networkAccessManager() const`
- `QQmlNetworkAccessManagerFactory * networkAccessManagerFactory() const`
- `QString offlineStorageDatabaseFilePath(const QString &databaseName) const`
- `QString offlineStoragePath() const`
- `bool outputWarningsToStandardError() const`
- `QStringList pluginPathList() const`
- `void removeImageProvider(const QString &providerId)`
- `void removeUrlInterceptor(QQmlAbstractUrlInterceptor *urlInterceptor)`
- `QQmlContext * rootContext() const`
- `void setBaseUrl(const QUrl &url)`
- `void setImportPathList(const QStringList &paths)`
- `void setIncubationController(QQmlIncubationController *controller)`
- `void setNetworkAccessManagerFactory(QQmlNetworkAccessManagerFactory *factory)`
- `void setOfflineStoragePath(const QString &dir)`
- `void setOutputWarningsToStandardError(bool enabled)`
- `void setPluginPathList(const QStringList &paths)`
- `T singletonInstance(int qmlTypeId)`
- `(since 6.5) T singletonInstance(QAnyStringView uri, QAnyStringView typeName)`
- `void trimComponentCache()`
- `QList<QQmlAbstractUrlInterceptor *> urlInterceptors() const`

### 公有槽函数

- `void retranslate()`

### 信号

- `void exit(int retCode)`
- `(since 6.5) void offlineStoragePathChanged()`
- `void quit()`
- `void warnings(const QList<QQmlError> &warnings)`

### 静态公有成员

- `QQmlContext * contextForObject(const QObject *object)`
- `void setContextForObject(QObject *object, QQmlContext *context)`

### 重实现的保护函数

- `virtual bool event(QEvent *e) override`

### 相关非成员函数

- `QQmlContext * qmlContext(const QObject *object)`
- `QQmlEngine * qmlEngine(const QObject *object)`

### 公开宏

- `QML_NAMESPACE_EXTENDED(EXTENSION_NAMESPACE)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `offlineStoragePath : QString`

**作用与语义：**

该属性包含用于存储离线用户数据的目录。
返回放置 SQL 和其他离线存储的目录。
用`openDatabaseSync()`创建的SQL数据库存储在这里。
默认设置为平台标准用户应用数据目录中的 QML/OfflineStorage。
请注意，该路径可能目前不存在于文件系统中，因此希望在该位置创建新文件的调用者应先创建路径——详见`QDir::mkpath()`。

**如何使用：** 调用 `offlineStoragePath()` 读取当前值；它不会修改应用状态。

### `[explicit] QQmlEngine::QQmlEngine(QObject *parent = nullptr)`

**作用与语义：**

创建一个新的QQmlEngine，使用给定的`parent`。

### `[override virtual noexcept] QQmlEngine::~QQmlEngine()`

**作用与语义：**

摧毁了`QQmlEngine`。
该引擎上创建的任何`QQmlContext`都会被无效，但不会被销毁（除非它们被父级到`QQmlEngine`对象）。
关于清理 JS 引擎的详细信息，请参见 ~`QJSEngine()`。

### `void QQmlEngine::addImageProvider(const QString &providerId, QQmlImageProviderBase *provider)`

**作用与语义：**

设置通过 image： url scheme 请求的图片的`provider`，并带有主机 `providerId`。`QQmlEngine` 拥有 `provider`。
图像提供者支持pixmap和线程图像请求。有关实现和使用图像提供者的详细信息，请参见`QQuickImageProvider`文档。
所有必要的图像提供者应在加载任何QML源文件之前加入引擎。

### `void QQmlEngine::addImportPath(const QString &path)`

**作用与语义：**

添加`path`作为一个目录，引擎在基于URL的目录结构中搜索已安装模块。
`path`可以是本地文件系统目录、Qt 资源路径（`:/imports`）、Qt 资源 URL（`qrc:/imports`）或 URL。
`path`会在加入导入路径列表之前被转换为规范形式。
新加入的`path`将率先进入`importPathList()`。

### `void QQmlEngine::addPluginPath(const QString &path)`

**作用与语义：**

添加`path`作为一个目录，引擎在该目录中搜索导入模块的本地插件（在`qmldir`文件中引用）。
默认情况下，列表只包含`.`，即引擎在`qmldir`文件本身的目录中进行搜索。
新加入的`path`将率先进入`pluginPathList()`。

### `void QQmlEngine::addUrlInterceptor(QQmlAbstractUrlInterceptor *urlInterceptor)`

**作用与语义：**

增加了用于解析 QML URL 的`urlInterceptor`。这同样适用于用于加载脚本文件和 QML 类型的 URL。在加载文件时，不应修改 URL 拦截器，否则 URL 选择可能不一致。多个 URL 拦截器（如有）将按添加顺序调用。
`QQmlEngine`不拥有拦截者，也不会删除它。

### `QUrl QQmlEngine::baseUrl() const`

**作用与语义：**

返回该引擎的基础URL。基础URL仅在向`QQmlComponent`构造函数传递相对URL时用于解析组件。
如果没有显式设置基础 URL，该方法返回应用当前的工作目录。

### `void QQmlEngine::clearComponentCache()`

**作用与语义：**

清除发动机内部组件缓存。
该函数会摧毁引擎之前加载的大多数组件的属性元数据。它通过从引擎的组件缓存中丢弃未被引用的组件来实现。它不会丢弃仍然被引用的组件，因为这几乎肯定会导致后续崩溃。
如果没有引用任何组件，该函数将引擎返回到不包含任何已加载组件数据的状态。这对于重新加载前一个组件集的较小子集，或加载先前加载组件的新版本时可能非常有用。
组件缓存清除后，必须先加载组件，才能创建任何新对象。
注意：由 QML 组件创建的任何现有对象都会保留其类型，即使你清除了组件缓存。这包括单例对象。如果你在清除缓存后从同一 QML 代码创建了更多对象，新的对象类型会与旧的不同。将这样的新对象分配给其声明类型中属于该对象的属性，而该属性属于清除缓存前创建的对象，是行不通的。
一般来说，清除组件缓存时，确保没有由QML组件创建的对象处于活体状态。

### `void QQmlEngine::clearSingletons()`

**作用与语义：**

清除发动机所有单条。
该函数会丢弃所有单例实例，删除引擎在其中拥有的任何 QObject。这有助于确保调用 `clearComponentCache()` 前没有剩余 QML 创建的对象。
如果引擎拥有基于`QObject`的单例实例，QML属性将变为空，若引擎不拥有则保留其值。访问现有QML创建对象时，这些单例不会被自动重建。只有当新组件实例化时，这些单例才会被重新创建。

### `[static] QQmlContext *QQmlEngine::contextForObject(const QObject *object)`

**作用与语义：**

返回`object`的`QQmlContext`，若未设置上下文则返回 nullptr。
当`QQmlEngine`实例化`QObject`时，内部上下文会自动分配给它。此类内部上下文是只读的。你无法在它们上设置上下文属性。

### `[override virtual protected] bool QQmlEngine::event(QEvent *e)`

**作用与语义：**

重实现自：`QObject::event`（QEvent *e）。

### `[signal] void QQmlEngine::exit(int retCode)`

**作用与语义：**

当引擎加载的QML希望以指定返回码`retCode`退出事件循环时，会发出该信号。

### `QQmlImageProviderBase *QQmlEngine::imageProvider(const QString &providerId) const`

**作用与语义：**

如果找到，返回设置为`providerId`的图像提供者;否则返回`nullptr`。

### `QStringList QQmlEngine::importPathList() const`

**作用与语义：**

返回引擎在基于URL的目录结构中搜索已安装模块的目录列表。
例如，如果路径中有`/opt/MyApp/lib/imports`，导入`com.mycompany.Feature`的QML会使`QQmlEngine`在`/opt/MyApp/lib/imports/com/mycompany/Feature/`中查找该模块提供的组件。定义版本映射类型以及可能的QML扩展插件需要`qmldir`文件。
默认情况下，此列表包含QML导入路径中提到的路径。

### `QQmlIncubationController *QQmlEngine::incubationController() const`

**作用与语义：**

返回当前设定的孵化控制器，若未设置控制器则返回0。

### `QUrl QQmlEngine::interceptUrl(const QUrl &url, QQmlAbstractUrlInterceptor::DataType type) const`

**作用与语义：**

在给定`type`的`url`上运行当前的URL拦截器并返回结果。

### `[since 6.6] void QQmlEngine::markCurrentFunctionAsTranslationBinding()`

**作用与语义：**

如果该方法被调用在QML中绑定的一部分函数内，则该绑定将被视为平移绑定。
注意：该函数主要适用于你想提供 qsTr 函数的替代方案。为了确保 C 类暴露的属性在语言变更时更新，建议对 `LanguageChange` 事件进行反应。这是一种更通用的机制，在非 QML 环境中使用该类时也能有效，且开销略小。然而，当类已经与 QML 引擎紧密关联时，使用 `markCurrentFunctionAsTranslationBinding` 也可以接受。更多细节请参见“为动态语言变更做准备”。

**官方示例：**

```cpp
 class I18nAwareClass : public QObject {

   //...

    QString text() const
    {
         if (auto engine = qmlEngine(this))
             engine->markCurrentFunctionAsTranslationBinding();
         return tr("Hello, world!");
    }
 };
```

### `QNetworkAccessManager *QQmlEngine::networkAccessManager() const`

**作用与语义：**

返回一个通用`QNetworkAccessManager`，可被该引擎实例化的任何QML类型使用。
如果`QQmlNetworkAccessManagerFactory`已设置且尚未创建`QNetworkAccessManager`，则使用该`QQmlNetworkAccessManagerFactory`来创建`QNetworkAccessManager`;否则返回的`QNetworkAccessManager`将没有代理或缓存设置。

### `QQmlNetworkAccessManagerFactory *QQmlEngine::networkAccessManagerFactory() const`

**作用与语义：**

返回当前`QQmlNetworkAccessManagerFactory`。

### `QString QQmlEngine::offlineStorageDatabaseFilePath(const QString &databaseName) const`

**作用与语义：**

返回带有标识符`databaseName`的本地存储数据库所在（或将会被定位）的文件路径。

### `[signal, since 6.5] void QQmlEngine::offlineStoragePathChanged()`

**作用与语义：**

该属性包含用于存储离线用户数据的目录。
返回放置 SQL 和其他离线存储的目录。
用`openDatabaseSync()`创建的SQL数据库存储在这里。
默认设置为平台标准用户应用数据目录中的 QML/OfflineStorage。
请注意，该路径可能目前不存在于文件系统中，因此希望在该位置创建新文件的调用者应先创建路径——详见`QDir::mkpath()`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `offlineStoragePath` 的变化，不要把它当作普通函数主动调用。

### `bool QQmlEngine::outputWarningsToStandardError() const`

**作用与语义：**

如果警告消息除了`warnings()`信号发出外还会输出到stderr，则返回true;否则返回false。
默认值为真。

### `QStringList QQmlEngine::pluginPathList() const`

**作用与语义：**

返回引擎搜索导入模块本地插件的目录列表（`qmldir`文件中引用）。
默认情况下，列表只包含`.`，即引擎在`qmldir`文件本身的目录中进行搜索。

### `[signal] void QQmlEngine::quit()`

**作用与语义：**

当引擎加载的QML想要退出时，会发出这个信号。

### `void QQmlEngine::removeImageProvider(const QString &providerId)`

**作用与语义：**

`providerId`时移除了图像提供商。

### `void QQmlEngine::removeUrlInterceptor(QQmlAbstractUrlInterceptor *urlInterceptor)`

**作用与语义：**

移除之前用 `addUrlInterceptor` 添加的 `urlInterceptor`。在引擎加载文件时不应修改 URL 拦截器，否则 URL 选择可能不一致。
这不会删除拦截器，只是将其从发动机中移除。之后你可以在同一台或不同的发动机上重复使用它。

### `[slot] void QQmlEngine::retranslate()`

**作用与语义：**

刷新所有使用标记为翻译字符串的绑定表达式。
安装带`QCoreApplication::installTranslator`的新译文后调用此功能，确保用户界面显示最新的翻译内容。

### `QQmlContext *QQmlEngine::rootContext() const`

**作用与语义：**

返回引擎的根上下文。
根上下文由`QQmlEngine`自动创建。所有由引擎实例实例化的QML组件实例应可用的数据应放在根上下文中。
应将仅部分组件实例可用的额外数据添加到根上下文的子上下文中。

### `void QQmlEngine::setBaseUrl(const QUrl &url)`

**作用与语义：**

将该引擎的基础URL设置为`url`。

### `[static] void QQmlEngine::setContextForObject(QObject *object, QQmlContext *context)`

**作用与语义：**

将`object`的 `QQmlContext` 设置为 `context`。如果`object`已经有上下文，则会输出警告，但上下文不会被更改。
当`QQmlEngine`实例化`QObject`时，上下文会自动设置。

### `void QQmlEngine::setImportPathList(const QStringList &paths)`

**作用与语义：**

将 `paths` 设置为搜索引擎在基于 URL 的目录结构中搜索已安装模块的目录列表。
默认情况下，此列表包含QML导入路径中提到的路径。
警告：调用 setImportPathList 不会保留默认导入路径。

### `void QQmlEngine::setIncubationController(QQmlIncubationController *controller)`

**作用与语义：**

设定发动机的孵化时间`controller`。发动机只能有一个主动控制器，且不拥有该控制器。

### `void QQmlEngine::setNetworkAccessManagerFactory(QQmlNetworkAccessManagerFactory *factory)`

**作用与语义：**

设置用于创建`QNetworkAccessManager`的`factory`。
`QNetworkAccessManager` 用于 QML 的所有网络访问。通过实现工厂，可以创建带有专门缓存、代理和 cookie 支持的自定义`QNetworkAccessManager`。
必须在发动机运行前设置好工厂设置。
注意：`QQmlEngine`不对工厂拥有所有权。

### `void QQmlEngine::setOutputWarningsToStandardError(bool enabled)`

**作用与语义：**

设置警告消息是否输出到 stderr 到 `enabled`。
如果`enabled`为真，QML生成的任何警告消息都会输出到stderr并由`warnings()`信号发出。如果`enabled`为假，则只发出`warnings()`信号。这使得应用程序能够自行处理警告输出。
默认值为真。

### `void QQmlEngine::setPluginPathList(const QStringList &paths)`

**作用与语义：**

将引擎用于搜索导入模块本地插件的目录列表（在`qmldir`文件中引用）设置为`paths`。
默认情况下，列表只包含`.`，即引擎在`qmldir`文件本身的目录中进行搜索。

### `template <typename T> T QQmlEngine::singletonInstance(int qmlTypeId)`

**作用与语义：**

返回注册在`qmlTypeId`下的单例类型实例。
模板参数 T 可以是`QJSValue`或指向 `QObject` 派生类型的指针，具体取决于单例的注册方式。如果尚未创建 T 实例，则现在创建。如果 `qmlTypeId` 不代表有效的单例类型，则返回默认构造 `QJSValue` 或返回 `nullptr`。
`QObject`* 示例：
`QJSValue`例：
建议将QML类型ID（例如作为单例类中的静态成员）存储。通过`qmlTypeId()`查找成本较高。

**官方示例：**

```cpp
 class MySingleton : public QObject {
     Q_OBJECT

     // Register as default constructed singleton.
     QML_ELEMENT
     QML_SINGLETON

     static int typeId;
     // ...
 };

     MySingleton::typeId = qmlTypeId(...);

     // Retrieve as QObject*
     QQmlEngine engine;
     MySingleton* instance = engine.singletonInstance<MySingleton*>(MySingleton::typeId);
```

### `[since 6.5] template <typename T> T QQmlEngine::singletonInstance(QAnyStringView uri, QAnyStringView typeName)`

**作用与语义：**

返回由`uri`指定的模块中名为`typeName`的单例类型实例。
该方法可作为调用`qmlTypeId`随后基于id的singletonInstance超载的替代方案。当只需一次性设置单例时，这非常方便;如果需要多次访问单例，缓存其typeId将允许通过基于类型ID的超载更快地访问。
模板参数 T 可以是`QJSValue`或指向 `QObject` 派生类型的指针，具体取决于单例的注册方式。如果尚未创建 T 实例，则现在进行创建。如果 `typeName`不代表有效的单例类型，则返回默认构造`QJSValue`或`nullptr`。

**官方示例：**

```cpp
     QQmlEngine engine;
     MySingleton *singleton = engine.singletonInstance<MySingleton *>("mymodule", "MySingleton");
```

### `void QQmlEngine::trimComponentCache()`

**作用与语义：**

修剪发动机内部组件缓存。
该函数会删除当前未被使用的加载组件的属性元数据。
如果该组件存在任何现存的组件实例、使用该组件的其他组件实例，或由这些组件实例化的任何对象，则该组件被视为正在使用中。

### `QList<QQmlAbstractUrlInterceptor *> QQmlEngine::urlInterceptors() const`

**作用与语义：**

返回当前活跃的URL拦截器列表。

### `[signal] void QQmlEngine::warnings(const QList<QQmlError> &warnings)`

**作用与语义：**

当QML生成`warnings`消息时，该信号会被发射。

### `QQmlContext *qmlContext(const QObject *object)`

**作用与语义：**

返回与`object`相关的`QQmlContext`（如果有的话）。这等价于`QQmlEngine::contextForObject`（对象）。
注意：添加`#include <QtQml>`以使用此功能。

### `QQmlEngine *qmlEngine(const QObject *object)`

**作用与语义：**

返回与`object`相关的`QQmlEngine`（如果有的话）。这等价于`QQmlEngine::contextForObject`（对象）->engine()，但效率更高。
注意：添加`#include <QtQml>`以使用此功能。

### `QML_NAMESPACE_EXTENDED(EXTENSION_NAMESPACE)`

**作用与语义：**

行为方式与`QML_EXTENDED_NAMESPACE`相同，但被扩展的是命名空间而非类型。
声明包围命名空间使用 `EXTENSION_NAMESPACE` 作为扩展，在 QML 中提供进一步枚举。如果扩展命名空间通过 `QML_ELEMENT` 或 `QML_NAMED_ELEMENT()` 宏暴露于 QML，则该功能生效。枚举需要暴露给元对象系统才能实现。
例如，在以下C代码中，。
命名空间`NS1`通过 `NS2` 扩展，`E2`枚举在 `NS1` 内即可从QML获得。
注意：`EXTENSION_NAMESPACE`也可以是`QObject`或QGadget;在这种情况下——与同样暴露方法和属性的`QML_EXTENDED`不同——只暴露其枚举。
注意：`EXTENSION_NAMESPACE`必须有一个元对象;即它必须是包含`Q_NAMESPACE`宏的命名空间，或者是`QObject`/QGadget。
注意：类名必须完全经过限定，即使你已经在命名空间内。

**官方示例：**

```cpp
 namespace NS2 {
     Q_NAMESPACE

     enum class E2 { D = 3, E, F };
     Q_ENUM_NS(E2)
 }

 namespace NS1 {
     Q_NAMESPACE
     QML_ELEMENT

     enum class E1 { A, B, C };
     Q_ENUM_NS(E1)

     // Extends NS1 with NS2
     QML_NAMESPACE_EXTENDED(NS2)
 }
```

### `QString offlineStoragePath() const`

**作用与语义：**

该属性包含用于存储离线用户数据的目录。
返回放置 SQL 和其他离线存储的目录。
用`openDatabaseSync()`创建的SQL数据库存储在这里。
默认设置为平台标准用户应用数据目录中的 QML/OfflineStorage。
请注意，该路径可能目前不存在于文件系统中，因此希望在该位置创建新文件的调用者应先创建路径——详见`QDir::mkpath()`。

**如何使用：** 调用 `offlineStoragePath()` 读取当前值；它不会修改应用状态。

### `void setOfflineStoragePath(const QString &dir)`

**作用与语义：**

该属性包含用于存储离线用户数据的目录。
返回放置 SQL 和其他离线存储的目录。
用`openDatabaseSync()`创建的SQL数据库存储在这里。
默认设置为平台标准用户应用数据目录中的 QML/OfflineStorage。
请注意，该路径可能目前不存在于文件系统中，因此希望在该位置创建新文件的调用者应先创建路径——详见`QDir::mkpath()`。

**如何使用：** 调用 `setOfflineStoragePath(...)` 修改 `offlineStoragePath`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QQmlEngine` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
