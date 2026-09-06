# QJSManagedValue

> Qt 6.11.1 · Qt Qml

## 1. 先建立直觉

**一句话定位：** `QJSManagedValue` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** 这是 Qt Qml 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QJSManagedValue` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QJSManagedValue>`
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
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum Type { Undefined, Boolean, Number, String, Object, …, Function }`

### 公有函数

- `QJSManagedValue()`
- `QJSManagedValue(QJSValue value, QJSEngine *engine)`
- `QJSManagedValue(const QJSPrimitiveValue &value, QJSEngine *engine)`
- `QJSManagedValue(const QString &string, QJSEngine *engine)`
- `QJSManagedValue(const QVariant &variant, QJSEngine *engine)`
- `QJSManagedValue(QJSManagedValue &&other)`
- `~QJSManagedValue()`
- `QJSValue call(const QJSValueList &arguments = {}) const`
- `QJSValue callAsConstructor(const QJSValueList &arguments = {}) const`
- `QJSValue callWithInstance(const QJSValue &instance, const QJSValueList &arguments = {}) const`
- `bool deleteProperty(const QString &name)`
- `bool deleteProperty(quint32 arrayIndex)`
- `QJSEngine * engine() const`
- `bool equals(const QJSManagedValue &other) const`
- `bool hasOwnProperty(const QString &name) const`
- `bool hasOwnProperty(quint32 arrayIndex) const`
- `bool hasProperty(const QString &name) const`
- `bool hasProperty(quint32 arrayIndex) const`
- `bool isArray() const`
- `bool isBoolean() const`
- `bool isDate() const`
- `bool isError() const`
- `bool isFunction() const`
- `bool isInteger() const`
- `bool isNull() const`
- `bool isNumber() const`
- `bool isObject() const`
- `bool isQMetaObject() const`
- `bool isQObject() const`
- `bool isRegularExpression() const`
- `bool isString() const`
- `bool isSymbol() const`
- `bool isUndefined() const`
- `bool isUrl() const`
- `bool isVariant() const`
- `QJSValue property(const QString &name) const`
- `QJSValue property(quint32 arrayIndex) const`
- `QJSManagedValue prototype() const`
- `void setProperty(const QString &name, const QJSValue &value)`
- `void setProperty(quint32 arrayIndex, const QJSValue &value)`
- `void setPrototype(const QJSManagedValue &prototype)`
- `bool strictlyEquals(const QJSManagedValue &other) const`
- `bool toBoolean() const`
- `QDateTime toDateTime() const`
- `int toInteger() const`
- `QJSValue toJSValue() const`
- `double toNumber() const`
- `QJSPrimitiveValue toPrimitive() const`
- `const QMetaObject * toQMetaObject() const`
- `QObject * toQObject() const`
- `QRegularExpression toRegularExpression() const`
- `QString toString() const`
- `QUrl toUrl() const`
- `QVariant toVariant() const`
- `QJSManagedValue::Type type() const`
- `QJSManagedValue & operator=(QJSManagedValue &&other)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QJSManagedValue::Type`

**作用与语义：**

该枚举代表了 ECMA-262 规定的 JavaScript 原生类型。
- `QJSManagedValue::Undefined`：`0`;`undefined`类型
- `QJSManagedValue::Boolean`：`1`;`boolean`型
- `QJSManagedValue::Number`：`2`;`number`类型
- `QJSManagedValue::String`：`3`;`string`类型
- `QJSManagedValue::Object`：`4`;`object`类型
- `QJSManagedValue::Symbol`：`5`;`symbol`类型
- `QJSManagedValue::Function`：`6`;`function`类型
注意，`null`值不是自身的类型，而是一种特殊类型的对象。你可以用`isNull()`方法查询`QJSManagedValue`来获取该条件。此外，JavaScript没有整数类型，但它知道对数字的特殊处理，以准备纯整数操作。你可以查询`QJSManagedValue`，看看它是否包含这种处理的结果，方法是用`isInteger()`方法。

### `[constexpr noexcept] QJSManagedValue::QJSManagedValue()`

**作用与语义：**

创建一个 QJSManagedValue，表示 JavaScript `undefined` 值。这是唯一不存储在 JavaScript 堆中的值。调用默认构造的 QJSManagedValue `engine()` 会返回 nullptr。

### `QJSManagedValue::QJSManagedValue(QJSValue value, QJSEngine *engine)`

**作用与语义：**

利用`engine`堆从`value`创建QJSManagedValue。如果`value`本身被管理且其所属引擎未`engine`，结果为`undefined`值，并生成警告。

### `QJSManagedValue::QJSManagedValue(const QJSPrimitiveValue &value, QJSEngine *engine)`

**作用与语义：**

利用`engine`堆从`value`生成QJSManagedValue。

### `QJSManagedValue::QJSManagedValue(const QString &string, QJSEngine *engine)`

**作用与语义：**

利用`engine`堆从`string`创建QJSManagedValue。

### `QJSManagedValue::QJSManagedValue(const QVariant &variant, QJSEngine *engine)`

**作用与语义：**

利用`engine`堆从`variant`创建QJSManagedValue。

### `QJSManagedValue::QJSManagedValue(QJSManagedValue &&other)`

**作用与语义：**

Move从`other`构造一个QJSManagedValue。这使得`other`处于默认构造状态，表示未定义，不属于任何引擎。

### `[noexcept] QJSManagedValue::~QJSManagedValue()`

**作用与语义：**

毁掉`QJSManagedValue`。
注意：这会释放它在 JavaScript 堆上的内存槽。你不得销毁与该 `QJSEngine` 所在线程不同的线程`QJSManagedValue`。

### `QJSValue QJSManagedValue::call(const QJSValueList &arguments = {}) const`

**作用与语义：**

如果`QJSManagedValue`代表 JavaScript FunctionObject，则用给定的`arguments`调用，返回结果。否则返回 JavaScript 的 `undefined` 值。
`arguments`必须是原始值或与该`QJSManagedValue`属于同一`QJSEngine`。否则调用不执行，返回JavaScript `undefined`值。

### `QJSValue QJSManagedValue::callAsConstructor(const QJSValueList &arguments = {}) const`

**作用与语义：**

如果`QJSManagedValue`代表一个JavaScript函数对象，则以构造函数的方式调用它并返回给定`arguments`，返回结果。否则返回JavaScript `undefined`值。
`arguments`必须是原始值或与该`QJSManagedValue`属于同一`QJSEngine`。否则调用不执行，返回JavaScript `undefined`值。

### `QJSValue QJSManagedValue::callWithInstance(const QJSValue &instance, const QJSValueList &arguments = {}) const`

**作用与语义：**

如果该`QJSManagedValue`代表 JavaScript FunctionObject，则在 FunctionObject `instance` 调用并返回给定`arguments`，返回结果。否则返回 JavaScript 的 `undefined` 值。
`arguments`和`instance`必须是原始值或与该`QJSManagedValue`属于同一`QJSEngine`。否则调用不执行，返回JavaScript `undefined`值。

### `bool QJSManagedValue::deleteProperty(const QString &name)`

**作用与语义：**

删除该`QJSManagedValue` `name`的属性。如果删除成功，返回`true`，否则`false`。

### `bool QJSManagedValue::deleteProperty(quint32 arrayIndex)`

**作用与语义：**

删除该`QJSManagedValue`中存储的`arrayIndex`值。如果删除成功，返回`true`，否则返回`false`。

### `QJSEngine *QJSManagedValue::engine() const`

**作用与语义：**

返回该`QJSManagedValue`所属的`QJSEngine`。请注意，除非`QJSManagedValue`被默认构造或移出，否则引擎始终有效。在后者情况下，返回一个nullptr。

### `bool QJSManagedValue::equals(const QJSManagedValue &other) const`

**作用与语义：**

调用JavaScript的“==”操作符，`QJSManagedValue`和`other`，返回结果。

### `bool QJSManagedValue::hasOwnProperty(const QString &name) const`

**作用与语义：**

如果该 `QJSManagedValue` 具有属性 `name`，返回`true`，否则返回 `false`。不考虑原型链的属性。

### `bool QJSManagedValue::hasOwnProperty(quint32 arrayIndex) const`

**作用与语义：**

如果该`QJSManagedValue`有数组索引`arrayIndex`，返回`true`，否则返回`false`。不考虑原型链的属性。

### `bool QJSManagedValue::hasProperty(const QString &name) const`

**作用与语义：**

如果该`QJSManagedValue`具有属性`name`，则返回`true`，否则返回`false`。考虑原型链的属性。

### `bool QJSManagedValue::hasProperty(quint32 arrayIndex) const`

**作用与语义：**

如果该`QJSManagedValue`具有数组索引`arrayIndex`，返回`true`，否则返回 `false`。考虑原型链的属性。

### `bool QJSManagedValue::isArray() const`

**作用与语义：**

如果该值表示一个 JavaScript 数组对象，则返回 `true`，否则返回 `false`。

### `bool QJSManagedValue::isBoolean() const`

**作用与语义：**

如果该`QJSManagedValue`类型为`boolean`，则返回`true`，否则`false`。

### `bool QJSManagedValue::isDate() const`

**作用与语义：**

如果该值表示一个 JavaScript 日期对象，则返回 `true`，否则返回 `false`。

### `bool QJSManagedValue::isError() const`

**作用与语义：**

如果该值代表JavaScript错误对象，则返回`true`，否则`false`。

### `bool QJSManagedValue::isFunction() const`

**作用与语义：**

如果该`QJSManagedValue`类型为`function`，返回 `true`，否则`false`。

### `bool QJSManagedValue::isInteger() const`

**作用与语义：**

如果该`QJSManagedValue`保持整数值，返回`true`，否则`false`。数字的存储格式不会影响对其执行的任何操作结果，但如果存储整数，许多操作会更快。

### `bool QJSManagedValue::isNull() const`

**作用与语义：**

如果该`QJSManagedValue`持有JavaScript `null`值，则返回`true`，否则`false`。

### `bool QJSManagedValue::isNumber() const`

**作用与语义：**

如果该`QJSManagedValue`类型为`number`，则返回`true`，否则`false`。

### `bool QJSManagedValue::isObject() const`

**作用与语义：**

如果该`QJSManagedValue`类型为`object`，则返回`true`，否则`false`。

### `bool QJSManagedValue::isQMetaObject() const`

**作用与语义：**

如果该值代表在JavaScript堆上管理的`QMetaObject`指针，`false`返回`true`。

### `bool QJSManagedValue::isQObject() const`

**作用与语义：**

如果该值代表在 JavaScript 堆上管理的 `QObject` 指针，`false` 返回 `true`。

### `bool QJSManagedValue::isRegularExpression() const`

**作用与语义：**

返回`true`该值是否代表JavaScript正则表达式对象，否则`false`返回。

### `bool QJSManagedValue::isString() const`

**作用与语义：**

如果该`QJSManagedValue`类型为`string`，则返回`true`，否则`false`。

### `bool QJSManagedValue::isSymbol() const`

**作用与语义：**

如果该`QJSManagedValue`类型为`symbol`，则返回`true`，否则`false`。

### `bool QJSManagedValue::isUndefined() const`

**作用与语义：**

如果该`QJSManagedValue`类型为`undefined`，则返回`true`，否则`false`。

### `bool QJSManagedValue::isUrl() const`

**作用与语义：**

如果该值代表 JavaScript URL 对象，则返回`true`，否则`false`。

### `bool QJSManagedValue::isVariant() const`

**作用与语义：**

如果该值代表在 JavaScript 堆上管理的`QVariant`，则返回`true`，否则`false`返回。

### `QJSValue QJSManagedValue::property(const QString &name) const`

**作用与语义：**

返回该`QJSManagedValue` `name`的属性。如果在实际对象上找不到该属性，则会搜索原型链。

### `QJSValue QJSManagedValue::property(quint32 arrayIndex) const`

**作用与语义：**

返回该`QJSManagedValue` `arrayIndex`存储的属性。如果在实际对象上找不到该属性，则搜索原型链。

### `QJSManagedValue QJSManagedValue::prototype() const`

**作用与语义：**

返回该`QJSManagedValue`的原型。这适用于任意值。例如，你可以从 `boolean` 值中检索 JavaScript `boolean` 原型。

### `void QJSManagedValue::setProperty(const QString &name, const QJSValue &value)`

**作用与语义：**

将属性 `name` 设置为该`QJSManagedValue`上的 `value`。这只能在类型为 `object` 的 JavaScript 值上实现。此外，`value`必须是原语或属于与该值相同的引擎。

### `void QJSManagedValue::setProperty(quint32 arrayIndex, const QJSValue &value)`

**作用与语义：**

在该`QJSManagedValue`中存储`value` `arrayIndex`。这只能在类型为`object`的JavaScript值上实现，且如果值不是数组，不推荐这样做。此外，`value`必须是原语，或者与该值属于同一引擎。

### `void QJSManagedValue::setPrototype(const QJSManagedValue &prototype)`

**作用与语义：**

将该`QJSManagedValue`的原型设置为`prototype`。前提条件是`prototype`与该`QJSManagedValue`属于同一`QJSEngine`，并且是对象（包括空）。此外，该`QJSManagedValue`也必须是对象（排除零），且不能创建原型循环。

### `bool QJSManagedValue::strictlyEquals(const QJSManagedValue &other) const`

**作用与语义：**

调用JavaScript '==='操作符，`QJSManagedValue`和`other`，返回结果。

### `bool QJSManagedValue::toBoolean() const`

**作用与语义：**

将管理值转换为布尔值。如果管理值包含布尔值，则返回该布尔值。否则，将执行JavaScript规则的布尔强制。

### `QDateTime QJSManagedValue::toDateTime() const`

**作用与语义：**

如果该`QJSManagedValue`包含 JavaScript 日期对象，返回等效的 `QDateTime`。否则返回无效的。

### `int QJSManagedValue::toInteger() const`

**作用与语义：**

将管理值转换为整数。首先根据`toNumber()`规则将数值转换为数值，然后根据将参数强制转换为32位整数的规则将其夹入整数范围。
内部，值可能已经存储为整数，这时会选择快速路径。
注意：将管理值转换为数字时可能会抛出异常。特别是，符号不能被强制转换为数字，或者自定义的 valueOf() 方法可能会抛出异常。此时结果为 0，转换后引擎会携带错误。
注意：JavaScript 强制将数字输入 32 位整数的规则不直观。

### `QJSValue QJSManagedValue::toJSValue() const`

**作用与语义：**

将此`QJSManagedValue`复制到新的`QJSValue`中。这比从`QJSManagedValue`构造`QJSValue`效率低，但保留了`QJSManagedValue`。

### `double QJSManagedValue::toNumber() const`

**作用与语义：**

将管理值转换为数字。如果管理值包含数字，则返回该数字。否则，将通过JavaScript规则执行数字强制执行。
注意：将管理值转换为数字时可能会抛出异常。特别是，符号不能被强制转换为数字，或者自定义的 valueOf() 方法可能会抛出异常。此时结果为 0，转换后引擎会携带错误。

### `QJSPrimitiveValue QJSManagedValue::toPrimitive() const`

**作用与语义：**

将管理值转换为`QJSPrimitiveValue`。如果管理值包含由`QJSPrimitiveValue`支持的类型，则复制该值。否则，值被转换为字符串，并存储在`QJSPrimitiveValue`中。
注意：将管理值转换为字符串可能会抛出异常。特别是，符号不能强制生成字符串，或者自定义`toString()`方法可能会抛出异常。在这种情况下，结果是未定义的值，转换后引擎会携带错误。

### `const QMetaObject *QJSManagedValue::toQMetaObject() const`

**作用与语义：**

如果该`QJSManagedValue`包含`QMetaObject`指针，则返回该指针。否则返回 nullptr。

### `QObject *QJSManagedValue::toQObject() const`

**作用与语义：**

如果该`QJSManagedValue`包含`QObject`指针，则返回该指针。否则返回 nullptr。

### `QRegularExpression QJSManagedValue::toRegularExpression() const`

**作用与语义：**

如果该`QJSManagedValue`包含JavaScript正则表达式对象，则返回等价的`QRegularExpression`。否则返回无效的。

### `QString QJSManagedValue::toString() const`

**作用与语义：**

将管理值转换为字符串。如果管理值包含字符串，则返回该字符串。否则，将执行 JavaScript 规则的字符串强制执行。
注意：将管理值转换为字符串时可能会抛出异常。特别是，符号无法强制生成字符串，或者自定义的 toString() 方法可能会抛出异常。在这种情况下，结果是空字符串，转换后引擎会携带错误。

### `QUrl QJSManagedValue::toUrl() const`

**作用与语义：**

如果该`QJSManagedValue`包含JavaScript URL对象，则返回等效`QUrl`。否则返回无效的。

### `QVariant QJSManagedValue::toVariant() const`

**作用与语义：**

将该`QJSManagedValue`复制到新的`QVariant`中。如果 `QJSManagedValue::isVariant()`返回 false，这也创造了一个有用的`QVariant`。`QVariant` 可以存储所有由 `QJSManagedValue` 支持的类型。

### `QJSManagedValue::Type QJSManagedValue::type() const`

**作用与语义：**

返回该`QJSManagedValue`的JavaScript类型。

### `QJSManagedValue &QJSManagedValue::operator=(QJSManagedValue &&other)`

**作用与语义：**

Move从`other`中分配一个`QJSManagedValue`。这使得`other`处于默认构造状态，表示未定义，不属于任何引擎。
注意：这会释放该`QJSManagedValue`在JavaScript堆中占用的内存槽。你不能在与该`QJSEngine`存在的线程不同的线程上移动分配`QJSManagedValue`。

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

`QJSManagedValue` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
