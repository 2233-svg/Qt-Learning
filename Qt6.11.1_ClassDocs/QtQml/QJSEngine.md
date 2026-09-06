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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QJSEngine::Extensionflags QJSEngine::Extensions`

**作用与语义：**

该枚举用于指定通过`installExtensions()`安装的扩展。
- `QJSEngine::TranslationExtension`：`0x1`;表示应安装翻译函数（例如，像 `qsTr()`）。这也会安装 Qt.`uiLanguage` 属性。
- `QJSEngine::ConsoleExtension`：`0x2`;表示应安装控制台功能（例如`console.log()`）。
- `QJSEngine::GarbageCollectionExtension`：`0x4`;表示应安装垃圾回收功能（例如`gc()`）。
- `QJSEngine::AllExtensions`：`0xffffffff`;表示所有延长部分都应安装。
翻译扩展。
脚本翻译函数与C翻译函数之间的关系如下表描述：
- `Script Function`：对应的C函数
- `qsTr()`：`QObject::tr()`
- `QT_TR_NOOP()`：`QT_TR_NOOP()`
- `qsTranslate()`：`QCoreApplication::translate()`
- `QT_TRANSLATE_NOOP()`：`QT_TRANSLATE_NOOP()`
- `qsTrId()`：`qtTrId()`
- `QT_TRID_NOOP()`：`QT_TRID_NOOP()`
该标志还为字符串原型添加了一个`arg()`函数。
更多信息请参见Qt国际化文档。
控制台扩展。
控制台对象实现了控制台API的一个子集，该API提供了熟悉的日志功能，如`console.log()`。
新增的功能列表如下：
- `console.assert()`
- `console.debug()`
- `console.exception()`
- `console.info()`
- `console.log()`（相当于`console.debug()`）
- `console.error()`
- `console.time()`
- `console.timeEnd()`
- `console.trace()`
- `console.count()`
- `console.warn()`
- `print()`（相当于`console.debug()`）
欲了解更多信息，请参阅控制台API文档。
垃圾回收扩展。
`gc()`函数等价于调用`collectGarbage()`。
扩展类型是QFlag的typedef<Extension>。它存储扩展值的或组合。

### `enum QJSEngine::ObjectOwnership`

**作用与语义：**

ObjectOwnership 控制 JavaScript 内存管理器是否在对应的 JavaScript 对象被引擎垃圾回收时自动销毁`QObject`。两种所有权选项为：
- `QJSEngine::CppOwnership`：`0`;该对象由 C 代码拥有，JavaScript 内存管理器永远不会删除它。JavaScript 的 destroy() 方法不能用于这些对象。该选项类似于 QScriptEngine：：QtOwnership。
- `QJSEngine::JavaScriptOwnership`：`1`;该对象归 JavaScript 所有。当该对象作为方法调用的返回值返回到 JavaScript 内存管理器时，JavaScript 内存管理器会跟踪该对象，并在没有剩余 JavaScript 引用且无`QObject::parent()`时删除它。一个`QJSEngine`跟踪的对象将在该`QJSEngine`的解构器过程中被删除。因此，如果删除其中一个引擎，两个不同引擎中具有 JavaScriptOwnership 的对象之间的 JavaScript 引用将无效。该选项类似于 QScriptEngine：：ScriptOwnership。
通常应用程序不需要显式设置对象的所有权。JavaScript内存管理器使用启发式方法设置默认所有权。默认情况下，JavaScript内存管理器创建的对象具有JavaScriptOwnership。例外是调用`QQmlComponent::create()`或`QQmlComponent::beginCreate()`创建的根对象，默认拥有CppOwnership。这些根级对象的所有权被视为已转移给C调用者。
未由 JavaScript 内存管理器创建的对象默认具有 CppOwnership。例外是从 C 方法调用返回的对象;它们的所有权将设置为 JavaScriptOwnership。这仅适用于显式调用`Q_INVOKABLE`方法或槽函数，但不适用于属性获取调用。
调用`setObjectOwnership()`会覆盖默认所有权。

### `uiLanguage : QString`

**作用与语义：**

此属性保存用于翻译用户界面字符串的语言。
此属性保存用于用户界面字符串翻译的语言名称。当 `QJSEngine::TranslationExtension` 安装到引擎中时，可作为 `Qt.uiLanguage` 进行读写。在 `QQmlEngine` 的实例中始终可用。
您可以自由设置其值并在绑定中使用。建议在应用程序中安装翻译器后设置。按约定，空字符串表示不打算对源代码使用的语言进行翻译。

**如何使用：** 调用 `uiLanguage()` 读取当前值；它不会修改应用状态。

### `QJSEngine::QJSEngine()`

**作用与语义：**

构造一个QJSEngine对象。
`globalObject()`初始化为具有ECMA-262第15.1节描述的属性。

### `[explicit] QJSEngine::QJSEngine(QObject *parent)`

**作用与语义：**

构造一个具有给定`parent`的QJSEngine对象。
`globalObject()`初始化为具有ECMA-262第15.1节描述的属性。

### `[override virtual noexcept] QJSEngine::~QJSEngine()`

**作用与语义：**

毁了这个`QJSEngine`。
在`QJSEngine`销毁期间，垃圾不会从持久的JS堆中收集。如果你需要释放所有内存，在销毁`QJSEngine`前手动调用`collectGarbage()`。

### `[since Qt 6.1] QJSValue QJSEngine::catchError()`

**作用与语义：**

如果异常当前待处理，则捕获该异常并返回为`QJSValue`。否则返回未定义的 `QJSValue`。调用该方法后，`hasError()`返回`false`。

### `template <typename From, typename To> To QJSEngine::coerceValue(const From &from)`

**作用与语义：**

返回给定的`from`转换为模板类型 `To`。转换采用 JavaScript 语义完成。这些语义与 `qvariant_cast` 语义不同。JavaScript 等价类型之间存在许多默认不执行的隐式转换`qvariant_cast`。该方法是该类中所有转换方法的推广。

### `void QJSEngine::collectGarbage()`

**作用与语义：**

负责垃圾收集。
垃圾回收器会通过寻找并丢弃脚本环境中无法访问的对象来尝试回收内存。
通常你不需要调用这个函数;当`QJSEngine`认为有必要时（即新对象已创建一定数量时），垃圾回收器会自动被调用。不过，你可以调用这个函数，明确请求尽快执行垃圾回收。

### `QJSValue QJSEngine::evaluate(const QString &program, const QString &fileName = QString(), int lineNumber = 1, QStringList *exceptionStackTrace = nullptr)`

**作用与语义：**

以`lineNumber`为基线编号，计算`program`，并返回评估结果。
脚本代码将在全局对象的上下文中进行评估。
注意：如果你需要在QML上下文中进行评估，请使用`QQmlExpression`。
`program`的求值可能导致引擎出现`exception`;此时返回值将是被抛出的异常（通常是`Error`对象;参见`QJSValue::isError()`）。
`lineNumber`用于指定`program`的起始行号;引擎报告的与此评估相关的行号信息将基于该参数。例如，如果`program`由两行代码组成，且第二行的语句引发脚本异常，例外行号为`lineNumber`加一。当未指定起始行号时，行号基于1。
`fileName`用于错误报告。例如，在错误对象中，如果文件名带有该功能，可以通过“fileName”属性访问文件名。
`exceptionStackTrace`用于报告是否投掷了未捕获的异常。如果你将非空指针传递给该指针的`QStringList`，如果脚本抛出未处理异常，它会将其设置为“栈框消息列表”，否则设置为空列表。堆栈框架消息的格式函数为 name：line number：column：file name。
注意：在某些情况下，例如原生函数，函数名和文件名可以为空，行号和列可以为-1。
注意：如果抛出异常且异常值不是错误实例（即返回`QJSValue::isError()`返回`false`），异常值仍会返回。使用`exceptionStackTrace->isEmpty()`区分该值是正常返回值还是例外返回值。

### `template <typename T> T QJSEngine::fromManagedValue(const QJSManagedValue &value)`

**作用与语义：**

返回已转换成模板类型`value` `T`。

### `template <typename T> T QJSEngine::fromPrimitiveValue(const QJSPrimitiveValue &value)`

**作用与语义：**

返回给定的`value`转换为模板类型`T`。
由于`QJSPrimitiveValue`只能保留int、bool、double、`QString`以及JavaScript的等价物，`null`和`undefined`，如果你请求任何其他类型，这个值会被强行强制。

### `template <typename T> T QJSEngine::fromScriptValue(const QJSValue &value)`

**作用与语义：**

返回已转换成模板类型`value` `T`。

### `template <typename T> T QJSEngine::fromVariant(const QVariant &value)`

**作用与语义：**

返回给定的 `value`转换为模板类型 `T`。转换采用 JavaScript 语义。这些语义与 `qvariant_cast` 的语义不同。JavaScript 等价类型之间存在许多隐式转换，默认情况下`qvariant_cast`不会执行。

### `QJSValue QJSEngine::globalObject() const`

**作用与语义：**

返回该引擎的全局对象。
默认情况下，全局对象包含 ECMA-262 内建的对象，如数学、日期和字符串。此外，你可以设置全局对象的属性，使所有脚本代码都能使用自己的扩展。脚本代码中的非本地变量将作为全局对象的属性创建，全局代码中的本地变量也会被创建。

### `[since Qt 6.1] bool QJSEngine::hasError() const`

**作用与语义：**

如果最后一次 JavaScript 执行出现异常，或者调用了 `throwError()`，返回 `true`。否则返回 `false`。请注意，`evaluate()` 会捕捉评估代码中抛出的任何异常。

### `QJSValue QJSEngine::importModule(const QString &fileName)`

**作用与语义：**

导入位于 `fileName` 的模块，并返回一个模块命名空间对象，其中包含所有导出的变量、常量和函数作为属性。
如果这是引擎中第一次导入该模块，则会从本地文件系统或 Qt 资源系统的指定位置加载文件，并作为 ECMAScript 模块进行评估。文件应以 UTF-8 文本编码。
随后对同一模块的导入将返回先前导入的实例。模块为单例，直至引擎被销毁。
指定的 `fileName` 将使用 `QFileInfo::canonicalFilePath()` 内部规范化。这意味着使用不同相对路径多次导入同一磁盘文件将只加载一次。
注意：如果在加载模块期间抛出异常，返回值将为异常（通常为 `Error` 对象；参见 `QJSValue::isError()`）。

### `void QJSEngine::installExtensions(QJSEngine::Extensions extensions, const QJSValue &object = QJSValue())`

**作用与语义：**

安装JavaScript `extensions`以添加标准ECMAScript实现中不具备的功能。
扩展安装在给定的`object`上，或者如果没有指定对象，则安装在全局对象上。
通过`OR`枚举值，可以同时安装多个扩展：

**官方示例：**

```cpp
 installExtensions(QJSEngine::TranslationExtension | QJSEngine::ConsoleExtension);
```

### `bool QJSEngine::isInterrupted() const`

**作用与语义：**

返回JavaScript执行是否当前中断。

### `QJSValue QJSEngine::newArray(uint length = 0)`

**作用与语义：**

创建一个带有给定`length`的 Java 对象 Array 类。

### `QJSValue QJSEngine::newErrorObject(QJSValue::ErrorType errorType, const QString &message = QString())`

**作用与语义：**

创建一个 Error 类的 JavaScript 对象，错误消息为 `message`。
所创建对象的原型将`errorType`。

### `QJSValue QJSEngine::newObject()`

**作用与语义：**

创建类为 Object 的 JavaScript 对象。
创建对象的原型将是对象原型对象。

### `template <typename T> QJSValue QJSEngine::newQMetaObject()`

**作用与语义：**

创建一个 JavaScript 对象，包裹与类 `T` 关联的静态`QMetaObject`。

### `QJSValue QJSEngine::newQMetaObject(const QMetaObject *metaObject)`

**作用与语义：**

创建一个包裹给定`QMetaObject`元对象的JavaScript对象`metaObject`必须比脚本引擎更持久。建议仅在静态元对象时使用此方法。
当被调用为构造函数时，会创建一个新的类实例。只有`Q_INVOKABLE`暴露的构造器才会从脚本引擎中可见。

### `QJSValue QJSEngine::newQObject(QObject *object)`

**作用与语义：**

创建一个JavaScript对象，用`JavaScriptOwnership`包裹给定的`QObject` `object`。
信号和槽函数、`object`的属性和子节点作为创建`QJSValue`的属性可用。
如果`object`是空指针，该函数返回空值。
如果为`object`的类（或递归地）注册了默认原型，那么新脚本对象的原型将被设置为该默认原型。
如果给定`object`在引擎控制之外被删除，任何通过JavaScript封装对象（无论是脚本代码还是C语言）访问已删除`QObject`成员的任何尝试都会导致脚本异常。

### `[since 6.2] QJSValue QJSEngine::newSymbol(const QString &name)`

**作用与语义：**

创建一个类为 Symbol 的 JavaScript 对象，值为 `name`。
创建对象的原型将是符号原型对象。

### `[static] QJSEngine::ObjectOwnership QJSEngine::objectOwnership(QObject *object)`

**作用与语义：**

归还`object`的所有权。

### `bool QJSEngine::registerModule(const QString &moduleName, const QJSValue &value)`

**作用与语义：**

注册一个`QJSValue`作为模块。调用该函数后，所有导入`moduleName`的模块将导入`value`值，而不是从文件系统加载`moduleName`。
任何有效的`QJSValue`都可以注册，但命名导出（即`import { name } from "info"`被视为对象的成员，因此默认导出必须使用newXYZ的某个`QJSEngine`方法之一创建。
由于这允许导入文件系统中不存在的模块，脚本应用程序可以利用这一点提供内置模块，类似于 Node.js。
成功时`true`回报，`false`其他情况。
注意：`QJSValue` `value`在被其他模块使用之前不会被调用或读取。这意味着没有代码可评估，因此在另一个模块尝试加载该模块时抛出异常之前，不会看到错误。
警告：尝试访问非对象`QJSValue`的命名导出将触发`exception`。

### `void QJSEngine::setInterrupted(bool interrupted)`

**作用与语义：**

中断或重新启用JavaScript执行。
如果`interrupted` `true`，该引擎执行的任何JavaScript都会立即中止并返回错误对象，直到该函数再次被调用，`interrupted`值为`false`。
该函数对线程是安全的。你可以从另一个线程调用它来中断，例如JavaScript中的无限循环。

### `[static] void QJSEngine::setObjectOwnership(QObject *object, QJSEngine::ObjectOwnership ownership)`

**作用与语义：**

设定`object`的`ownership`。
带有 `JavaScriptOwnership` 的对象只要仍有父对象，即使没有引用，也不会被垃圾回收。

### `[since Qt 5.12] void QJSEngine::throwError(const QString &message)`

**作用与语义：**

在给定`message`时抛出运行时错误（例外）。
该方法是 JavaScript 中 `throw()` 表达式的 C 对应。它使 C 代码能够向 `QJSEngine` 报告运行时错误。因此，它应仅从通过 `QJSEngine` 由 JavaScript 函数调用的 C 代码调用。
当从C返回时，引擎会中断正常的执行流程，并调用下一个预注册的异常处理程序，并使用包含该`message`的错误对象。错误对象将指向JavaScript调用栈中最顶端的上下文位置;具体来说，它将具有属性`lineNumber`、`fileName`和`stack`。这些属性在脚本异常中有描述。
在以下示例中，FileAccess.cpp 中的一个 C 方法在 qmlFile.qml 中，在调用 `readFileAsText()` 的位置抛出错误：
也可以在 JavaScript 中检测抛出错误：
如果你需要更具体的运行时错误来描述异常，可以使用 `throwError`（QJSValue：：ErrorType errorType， const QString &message） 重载。

**官方示例：**

```cpp
 // qmlFile.qml
 function someFunction() {
   ...
   var text = FileAccess.readFileAsText("/path/to/file.txt");
 }
```

### `[since 6.1] void QJSEngine::throwError(const QJSValue &error)`

**作用与语义：**

抛出预构的运行时`error`（例外）。这样你可以用`newErrorObject()`创建错误并根据需要进行自定义。
注意：该功能会让`QJSEngine::throwError()`重载。

### `[since Qt 5.12] void QJSEngine::throwError(QJSValue::ErrorType errorType, const QString &message = QString())`

**作用与语义：**

在给定的`errorType`和 `message` 时抛出运行时错误（异常）。
注意：该功能会让`QJSEngine::throwError()`重载。

**官方示例：**

```cpp
 // Assuming that DataEntry is a QObject-derived class that has been
 // registered as a singleton type and provides an invokable method
 // setAge().

 void DataEntry::setAge(int age) {
   if (age < 0 || age > 200) {
     jsEngine->throwError(QJSValue::RangeError,
                          "Age must be between 0 and 200");
   }
   ...
 }
```

### `template <typename T> QJSManagedValue QJSEngine::toManagedValue(const T &value)`

**作用与语义：**

与给定`value`形成`QJSManagedValue`。

### `template <typename T> QJSPrimitiveValue QJSEngine::toPrimitiveValue(const T &value)`

**作用与语义：**

与给定`value`形成`QJSPrimitiveValue`。
由于`QJSPrimitiveValue`只能保留int、bool、double、`QString`，以及JavaScript的等效代码`null`和`undefined`，如果你通过其他类型，这个值会被强迫。

### `template <typename T> QJSValue QJSEngine::toScriptValue(const T &value)`

**作用与语义：**

与给定`value`形成`QJSValue`。

### `QJSEngine *qjsEngine(const QObject *object)`

**作用与语义：**

返回与`object`相关的`QJSEngine`（如果有的话）。
如果你已经将`QObject`暴露给 JavaScript 环境，并且在程序后期想要重新获得访问权限，这个函数非常有用。它不需要你保留从`QJSEngine::newQObject()`返回的包装器。

### `enum Extension { TranslationExtension, ConsoleExtension, GarbageCollectionExtension, AllExtensions }`

**作用与语义：**

该枚举用于指定通过`installExtensions()`安装的扩展。
- `QJSEngine::TranslationExtension`：`0x1`;表示应安装翻译函数（例如，像 `qsTr()`）。这也会安装 Qt.`uiLanguage` 属性。
- `QJSEngine::ConsoleExtension`：`0x2`;表示应安装控制台功能（例如`console.log()`）。
- `QJSEngine::GarbageCollectionExtension`：`0x4`;表示应安装垃圾回收功能（例如`gc()`）。
- `QJSEngine::AllExtensions`：`0xffffffff`;表示所有延长部分都应安装。
翻译扩展。
脚本翻译函数与C翻译函数之间的关系如下表描述：
- `Script Function`：对应的C函数
- `qsTr()`：`QObject::tr()`
- `QT_TR_NOOP()`：`QT_TR_NOOP()`
- `qsTranslate()`：`QCoreApplication::translate()`
- `QT_TRANSLATE_NOOP()`：`QT_TRANSLATE_NOOP()`
- `qsTrId()`：`qtTrId()`
- `QT_TRID_NOOP()`：`QT_TRID_NOOP()`
该标志还为字符串原型添加了一个`arg()`函数。
更多信息请参见Qt国际化文档。
控制台扩展。
控制台对象实现了控制台API的一个子集，该API提供了熟悉的日志功能，如`console.log()`。
新增的功能列表如下：
- `console.assert()`
- `console.debug()`
- `console.exception()`
- `console.info()`
- `console.log()`（相当于`console.debug()`）
- `console.error()`
- `console.time()`
- `console.timeEnd()`
- `console.trace()`
- `console.count()`
- `console.warn()`
- `print()`（相当于`console.debug()`）
欲了解更多信息，请参阅控制台API文档。
垃圾回收扩展。
`gc()`函数等价于调用`collectGarbage()`。
扩展类型是QFlag的typedef<Extension>。它存储扩展值的或组合。

### `flags Extensions`

**作用与语义：**

该枚举用于指定通过`installExtensions()`安装的扩展。
- `QJSEngine::TranslationExtension`：`0x1`;表示应安装翻译函数（例如，像 `qsTr()`）。这也会安装 Qt.`uiLanguage` 属性。
- `QJSEngine::ConsoleExtension`：`0x2`;表示应安装控制台功能（例如`console.log()`）。
- `QJSEngine::GarbageCollectionExtension`：`0x4`;表示应安装垃圾回收功能（例如`gc()`）。
- `QJSEngine::AllExtensions`：`0xffffffff`;表示所有延长部分都应安装。
翻译扩展。
脚本翻译函数与C翻译函数之间的关系如下表描述：
- `Script Function`：对应的C函数
- `qsTr()`：`QObject::tr()`
- `QT_TR_NOOP()`：`QT_TR_NOOP()`
- `qsTranslate()`：`QCoreApplication::translate()`
- `QT_TRANSLATE_NOOP()`：`QT_TRANSLATE_NOOP()`
- `qsTrId()`：`qtTrId()`
- `QT_TRID_NOOP()`：`QT_TRID_NOOP()`
该标志还为字符串原型添加了一个`arg()`函数。
更多信息请参见Qt国际化文档。
控制台扩展。
控制台对象实现了控制台API的一个子集，该API提供了熟悉的日志功能，如`console.log()`。
新增的功能列表如下：
- `console.assert()`
- `console.debug()`
- `console.exception()`
- `console.info()`
- `console.log()`（相当于`console.debug()`）
- `console.error()`
- `console.time()`
- `console.timeEnd()`
- `console.trace()`
- `console.count()`
- `console.warn()`
- `print()`（相当于`console.debug()`）
欲了解更多信息，请参阅控制台API文档。
垃圾回收扩展。
`gc()`函数等价于调用`collectGarbage()`。
扩展类型是QFlag的typedef<Extension>。它存储扩展值的或组合。

### `void setUiLanguage(const QString &language)`

**作用与语义：**

此属性保存用于翻译用户界面字符串的语言。
此属性保存用于用户界面字符串翻译的语言名称。当 `QJSEngine::TranslationExtension` 安装到引擎中时，可作为 `Qt.uiLanguage` 进行读写。在 `QQmlEngine` 的实例中始终可用。
您可以自由设置其值并在绑定中使用。建议在应用程序中安装翻译器后设置。按约定，空字符串表示不打算对源代码使用的语言进行翻译。

**如何使用：** 调用 `setUiLanguage(...)` 修改 `uiLanguage`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QString uiLanguage() const`

**作用与语义：**

此属性保存用于翻译用户界面字符串的语言。
此属性保存用于用户界面字符串翻译的语言名称。当 `QJSEngine::TranslationExtension` 安装到引擎中时，可作为 `Qt.uiLanguage` 进行读写。在 `QQmlEngine` 的实例中始终可用。
您可以自由设置其值并在绑定中使用。建议在应用程序中安装翻译器后设置。按约定，空字符串表示不打算对源代码使用的语言进行翻译。

**如何使用：** 调用 `uiLanguage()` 读取当前值；它不会修改应用状态。

### `void uiLanguageChanged()`

**作用与语义：**

此属性保存用于翻译用户界面字符串的语言。
此属性保存用于用户界面字符串翻译的语言名称。当 `QJSEngine::TranslationExtension` 安装到引擎中时，可作为 `Qt.uiLanguage` 进行读写。在 `QQmlEngine` 的实例中始终可用。
您可以自由设置其值并在绑定中使用。建议在应用程序中安装翻译器后设置。按约定，空字符串表示不打算对源代码使用的语言进行翻译。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `uiLanguage` 的变化，不要把它当作普通函数主动调用。

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
