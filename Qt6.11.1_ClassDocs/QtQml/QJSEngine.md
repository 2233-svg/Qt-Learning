# QJSEngine

> Qt 6.11.1 · Qt Qml

## 1. 先建立直觉

**一句话定位：** `QJSEngine` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** 这是 Qt Qml 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QJSEngine` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QJSEngine>`
- 继承自：QObject
- 直接派生类：QQmlEngine

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
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum Extension { TranslationExtension, ConsoleExtension, GarbageCollectionExtension, AllExtensions }`
- `flags Extensions`
- `enum ObjectOwnership { CppOwnership, JavaScriptOwnership }`

### 属性

- `uiLanguage : QString`

### 公有函数

- `QJSEngine()`
- `QJSEngine(QObject *parent)`
- `virtual ~QJSEngine() override`
- `(since Qt 6.1) QJSValue catchError()`
- `To coerceValue(const From &from)`
- `void collectGarbage()`
- `QJSValue evaluate(const QString &program, const QString &fileName = QString(), int lineNumber = 1, QStringList *exceptionStackTrace = nullptr)`
- `T fromManagedValue(const QJSManagedValue &value)`
- `T fromPrimitiveValue(const QJSPrimitiveValue &value)`
- `T fromScriptValue(const QJSValue &value)`
- `T fromVariant(const QVariant &value)`
- `QJSValue globalObject() const`
- `(since Qt 6.1) bool hasError() const`
- `QJSValue importModule(const QString &fileName)`
- `void installExtensions(QJSEngine::Extensions extensions, const QJSValue &object = QJSValue())`
- `bool isInterrupted() const`
- `QJSValue newArray(uint length = 0)`
- `QJSValue newErrorObject(QJSValue::ErrorType errorType, const QString &message = QString())`
- `QJSValue newObject()`
- `QJSValue newQMetaObject()`
- `QJSValue newQMetaObject(const QMetaObject *metaObject)`
- `QJSValue newQObject(QObject *object)`
- `(since 6.2) QJSValue newSymbol(const QString &name)`
- `bool registerModule(const QString &moduleName, const QJSValue &value)`
- `void setInterrupted(bool interrupted)`
- `void setUiLanguage(const QString &language)`
- `(since Qt 5.12) void throwError(const QString &message)`
- `(since 6.1) void throwError(const QJSValue &error)`
- `(since Qt 5.12) void throwError(QJSValue::ErrorType errorType, const QString &message = QString())`
- `QJSManagedValue toManagedValue(const T &value)`
- `QJSPrimitiveValue toPrimitiveValue(const T &value)`
- `QJSValue toScriptValue(const T &value)`
- `QString uiLanguage() const`

### 信号

- `void uiLanguageChanged()`

### 静态公有成员

- `QJSEngine::ObjectOwnership objectOwnership(QObject *object)`
- `void setObjectOwnership(QObject *object, QJSEngine::ObjectOwnership ownership)`

### 相关非成员函数

- `QJSEngine * qjsEngine(const QObject *object)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 42 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QJSEngine::Extensionflags QJSEngine::Extensions`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QJSEngine` 暴露的类型声明 `Extensionflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Extensionflags QJSEngine::Extensions`。
- 属性名：`QJSEngine`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QJSEngine::ObjectOwnership`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QJSEngine` 暴露的类型声明 `Object、Ownership`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ObjectOwnership`。
- 属性名：`QJSEngine`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `uiLanguage : QString`

**API 类别：** 属性说明

**中文解读：** 这是 `QJSEngine` 的配置属性。初始化或状态切换时通过 `setUiLanguage(...)` 设置，之后用 `uiLanguage()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QString`。
- 属性名：`uiLanguage`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJSEngine::QJSEngine()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJSEngine` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QJSEngine::QJSEngine(QObject *parent)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJSEngine` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QObject *`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual noexcept] QJSEngine::~QJSEngine()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJSEngine` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since Qt 6.1] QJSValue QJSEngine::catchError()`

**API 类别：** 成员函数说明

**中文解读：** `QJSEngine::catchError` 用于计算、查询或取得与“catch、错误”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QJSValue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QJSValue`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename From, typename To> To QJSEngine::coerceValue(const From &from)`

**API 类别：** 成员函数说明

**中文解读：** `QJSEngine::coerceValue` 用于计算、查询或取得与“coerce、值访问”相关的操作。调用时要先确认当前状态和 `from` 的有效范围；返回类型是 `template <typename From, typename To> To`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename From, typename To> To`。
- 参数 `from`：类型为 `const From &`。没有默认值，调用时必须提供。传入 `const From &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QJSEngine::collectGarbage()`

**API 类别：** 成员函数说明

**中文解读：** `QJSEngine::collectGarbage` 用于执行与“collect、Garbage”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJSValue QJSEngine::evaluate(const QString &program, const QString &fileName = QString(), int lineNumber = 1, QStringList *exceptionStackTrace = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** `QJSEngine::evaluate` 用于计算、查询或取得与“evaluate”相关的操作。调用时要先确认当前状态和 `program`、`fileName`、`lineNumber`、`exceptionStackTrace` 的有效范围；返回类型是 `QJSValue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QJSValue`。
- 参数 `program`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `fileName`：类型为 `const QString &`。默认值为 `QString()`。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。
- 参数 `lineNumber`：类型为 `int`。默认值为 `1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `exceptionStackTrace`：类型为 `QStringList *`。默认值为 `nullptr`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename T> T QJSEngine::fromManagedValue(const QJSManagedValue &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `fromManagedValue`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`template <typename T> T`。
- 参数 `value`：类型为 `const QJSManagedValue &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename T> T QJSEngine::fromPrimitiveValue(const QJSPrimitiveValue &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `fromPrimitiveValue`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`template <typename T> T`。
- 参数 `value`：类型为 `const QJSPrimitiveValue &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename T> T QJSEngine::fromScriptValue(const QJSValue &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `fromScriptValue`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`template <typename T> T`。
- 参数 `value`：类型为 `const QJSValue &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename T> T QJSEngine::fromVariant(const QVariant &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `fromVariant`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`template <typename T> T`。
- 参数 `value`：类型为 `const QVariant &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJSValue QJSEngine::globalObject() const`

**API 类别：** 成员函数说明

**中文解读：** `QJSEngine::globalObject` 用于计算、查询或取得与“global、Object”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QJSValue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QJSValue`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since Qt 6.1] bool QJSEngine::hasError() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasError`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJSValue QJSEngine::importModule(const QString &fileName)`

**API 类别：** 成员函数说明

**中文解读：** `QJSEngine::importModule` 用于计算、查询或取得与“import、Module”相关的操作。调用时要先确认当前状态和 `fileName` 的有效范围；返回类型是 `QJSValue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QJSValue`。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QJSEngine::installExtensions(QJSEngine::Extensions extensions, const QJSValue &object = QJSValue())`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QJSEngine` 添加依赖、数据或子对象的 API `installExtensions`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `extensions`：类型为 `QJSEngine::Extensions`。没有默认值，调用时必须提供。传入 `QJSEngine::Extensions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `object`：类型为 `const QJSValue &`。默认值为 `QJSValue()`。传入 `const QJSValue &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJSEngine::isInterrupted() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isInterrupted`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJSValue QJSEngine::newArray(uint length = 0)`

**API 类别：** 成员函数说明

**中文解读：** `QJSEngine::newArray` 用于计算、查询或取得与“new、Array”相关的操作。调用时要先确认当前状态和 `length` 的有效范围；返回类型是 `QJSValue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QJSValue`。
- 参数 `length`：类型为 `uint`。默认值为 `0`。传入 `uint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJSValue QJSEngine::newErrorObject(QJSValue::ErrorType errorType, const QString &message = QString())`

**API 类别：** 成员函数说明

**中文解读：** `QJSEngine::newErrorObject` 用于计算、查询或取得与“new、错误、Object”相关的操作。调用时要先确认当前状态和 `errorType`、`message` 的有效范围；返回类型是 `QJSValue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QJSValue`。
- 参数 `errorType`：类型为 `QJSValue::ErrorType`。没有默认值，调用时必须提供。传入 `QJSValue::ErrorType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `message`：类型为 `const QString &`。默认值为 `QString()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJSValue QJSEngine::newObject()`

**API 类别：** 成员函数说明

**中文解读：** `QJSEngine::newObject` 用于计算、查询或取得与“new、Object”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QJSValue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QJSValue`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename T> QJSValue QJSEngine::newQMetaObject()`

**API 类别：** 成员函数说明

**中文解读：** `QJSEngine::newQMetaObject` 用于计算、查询或取得与“new、Q、Meta、Object”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `template <typename T> QJSValue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename T> QJSValue`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJSValue QJSEngine::newQMetaObject(const QMetaObject *metaObject)`

**API 类别：** 成员函数说明

**中文解读：** `QJSEngine::newQMetaObject` 用于计算、查询或取得与“new、Q、Meta、Object”相关的操作。调用时要先确认当前状态和 `metaObject` 的有效范围；返回类型是 `QJSValue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QJSValue`。
- 参数 `metaObject`：类型为 `const QMetaObject *`。没有默认值，调用时必须提供。传入 `const QMetaObject *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJSValue QJSEngine::newQObject(QObject *object)`

**API 类别：** 成员函数说明

**中文解读：** `QJSEngine::newQObject` 用于计算、查询或取得与“new、Q、Object”相关的操作。调用时要先确认当前状态和 `object` 的有效范围；返回类型是 `QJSValue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QJSValue`。
- 参数 `object`：类型为 `QObject *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] QJSValue QJSEngine::newSymbol(const QString &name)`

**API 类别：** 成员函数说明

**中文解读：** `QJSEngine::newSymbol` 用于计算、查询或取得与“new、Symbol”相关的操作。调用时要先确认当前状态和 `name` 的有效范围；返回类型是 `QJSValue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QJSValue`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QJSEngine::ObjectOwnership QJSEngine::objectOwnership(QObject *object)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `objectOwnership`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QJSEngine::ObjectOwnership`。
- 参数 `object`：类型为 `QObject *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJSEngine::registerModule(const QString &moduleName, const QJSValue &value)`

**API 类别：** 成员函数说明

**中文解读：** `QJSEngine::registerModule` 用于计算、查询或取得与“注册、Module”相关的操作。调用时要先确认当前状态和 `moduleName`、`value` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `moduleName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `value`：类型为 `const QJSValue &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QJSEngine::setInterrupted(bool interrupted)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setInterrupted`。调用它会改变 `QJSEngine` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `interrupted`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QJSEngine::setObjectOwnership(QObject *object, QJSEngine::ObjectOwnership ownership)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `setObjectOwnership`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `object`：类型为 `QObject *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。
- 参数 `ownership`：类型为 `QJSEngine::ObjectOwnership`。没有默认值，调用时必须提供。传入 `QJSEngine::ObjectOwnership` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since Qt 5.12] void QJSEngine::throwError(const QString &message)`

**API 类别：** 成员函数说明

**中文解读：** `QJSEngine::throwError` 用于执行与“throw、错误”相关的操作。调用时要先确认当前状态和 `message` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `message`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] void QJSEngine::throwError(const QJSValue &error)`

**API 类别：** 成员函数说明

**中文解读：** `QJSEngine::throwError` 用于执行与“throw、错误”相关的操作。调用时要先确认当前状态和 `error` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `error`：类型为 `const QJSValue &`。没有默认值，调用时必须提供。错误输出对象或错误状态。解析/执行后要检查它，而不能只看主返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since Qt 5.12] void QJSEngine::throwError(QJSValue::ErrorType errorType, const QString &message = QString())`

**API 类别：** 成员函数说明

**中文解读：** `QJSEngine::throwError` 用于执行与“throw、错误”相关的操作。调用时要先确认当前状态和 `errorType`、`message` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `errorType`：类型为 `QJSValue::ErrorType`。没有默认值，调用时必须提供。传入 `QJSValue::ErrorType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `message`：类型为 `const QString &`。默认值为 `QString()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename T> QJSManagedValue QJSEngine::toManagedValue(const T &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toManagedValue`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`template <typename T> QJSManagedValue`。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename T> QJSPrimitiveValue QJSEngine::toPrimitiveValue(const T &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toPrimitiveValue`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`template <typename T> QJSPrimitiveValue`。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename T> QJSValue QJSEngine::toScriptValue(const T &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toScriptValue`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`template <typename T> QJSValue`。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJSEngine *qjsEngine(const QObject *object)`

**API 类别：** 相关非成员函数

**中文解读：** `QJSEngine::qjsEngine` 用于计算、查询或取得与“qjs、Engine”相关的操作。调用时要先确认当前状态和 `object` 的有效范围；返回类型是 `QJSEngine *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QJSEngine *`。
- 参数 `object`：类型为 `const QObject *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum Extension { TranslationExtension, ConsoleExtension, GarbageCollectionExtension, AllExtensions }`

**API 类别：** 公有类型

**中文解读：** 这是 `QJSEngine` 暴露的类型声明 `Extension`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags Extensions`

**API 类别：** 公有类型

**中文解读：** 这是 `QJSEngine` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setUiLanguage(const QString &language)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setUiLanguage`。调用它会改变 `QJSEngine` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `language`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString uiLanguage() const`

**API 类别：** 公有函数

**中文解读：** `QJSEngine::uiLanguage` 用于计算、查询或取得与“ui、Language”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void uiLanguageChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `uiLanguageChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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

`QJSEngine` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
