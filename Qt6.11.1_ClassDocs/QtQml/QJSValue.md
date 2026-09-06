# QJSValue

> Qt 6.11.1 · Qt Qml

## 1. 先建立直觉

**一句话定位：** `QJSValue` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** 这是 Qt Qml 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QJSValue` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QJSValue>`
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

- `enum ErrorType { GenericError, RangeError, ReferenceError, SyntaxError, TypeError, URIError }`
- `enum ObjectConversionBehavior { ConvertJSObjects, RetainJSObjects }`
- `enum SpecialValue { UndefinedValue, NullValue }`

### 公有函数

- `QJSValue(QJSValue::SpecialValue value = UndefinedValue)`
- `QJSValue(bool value)`
- `QJSValue(const QLatin1String &value)`
- `QJSValue(const QString &value)`
- `QJSValue(const char *value)`
- `QJSValue(double value)`
- `QJSValue(int value)`
- `QJSValue(uint value)`
- `QJSValue(const QJSValue &other)`
- `QJSValue(QJSValue &&other)`
- `~QJSValue()`
- `QJSValue call(const QJSValueList &args = QJSValueList()) const`
- `QJSValue callAsConstructor(const QJSValueList &args = QJSValueList()) const`
- `QJSValue callWithInstance(const QJSValue &instance, const QJSValueList &args = QJSValueList()) const`
- `bool deleteProperty(const QString &name)`
- `bool equals(const QJSValue &other) const`
- `QJSValue::ErrorType errorType() const`
- `bool hasOwnProperty(const QString &name) const`
- `bool hasProperty(const QString &name) const`
- `bool isArray() const`
- `bool isBool() const`
- `bool isCallable() const`
- `bool isDate() const`
- `bool isError() const`
- `bool isNull() const`
- `bool isNumber() const`
- `bool isObject() const`
- `bool isQMetaObject() const`
- `bool isQObject() const`
- `bool isRegExp() const`
- `bool isString() const`
- `bool isUndefined() const`
- `bool isUrl() const`
- `QJSValue property(const QString &name) const`
- `QJSValue property(quint32 arrayIndex) const`
- `QJSValue prototype() const`
- `void setProperty(const QString &name, const QJSValue &value)`
- `void setProperty(quint32 arrayIndex, const QJSValue &value)`
- `void setPrototype(const QJSValue &prototype)`
- `bool strictlyEquals(const QJSValue &other) const`
- `bool toBool() const`
- `QDateTime toDateTime() const`
- `qint32 toInt() const`
- `double toNumber() const`
- `QJSPrimitiveValue toPrimitive() const`
- `const QMetaObject * toQMetaObject() const`
- `QObject * toQObject() const`
- `QString toString() const`
- `quint32 toUInt() const`
- `QVariant toVariant(QJSValue::ObjectConversionBehavior behavior) const`
- `QVariant toVariant() const`
- `QJSValue & operator=(QJSValue &&other)`
- `QJSValue & operator=(const QJSValue &other)`

### 相关非成员函数

- `QJSValueList`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QJSValue::ErrorType`

**作用与语义：**

使用此枚举表示JavaScript语言特定的错误对象类型。
当用 C 语言模拟语言特性需要使用专用异常类型时，它们可能非常有用。此外，它们还可能帮助更清晰地传达某些典型条件，而不是抛出通用的 JavaScript 异常。例如，处理网络和资源定位器的代码可能会发现，使用 URIError 类型传播与格式错误定位符相关的错误很有用。
- `QJSValue::GenericError`：`1`;一个通用的错误对象，但不是特定子类型。
- `QJSValue::RangeError`：`3`;某个值与预期集合或范围不匹配。
- `QJSValue::ReferenceError`：`4`;一个不存在的变量被引用。
- `QJSValue::SyntaxError`：`5`;遇到了不符合语言语法的无效令牌或令牌序列。
- `QJSValue::TypeError`：`6`;操作数或参数与预期类型不兼容。
- `QJSValue::URIError`：`7`;URI 处理函数使用错误或提供的 URI 形状异常。

### `enum QJSValue::ObjectConversionBehavior`

**作用与语义：**

该枚举用于指定没有对应本地 Qt 类型的 JavaScript 对象和符号在转换为 `QVariant` 时应如何处理。
- `QJSValue::ConvertJSObjects`：`0`;尝试尽力而为，可能有损的转换。符号转换为`QString`。
- `QJSValue::RetainJSObjects`：`1`;价值以`QJSValue`包裹`QVariant`保持。

### `enum QJSValue::SpecialValue`

**作用与语义：**

该枚举用于指定单值类型。
- `QJSValue::UndefinedValue`：`1`;一个未定义的值。
- `QJSValue::NullValue`：`0`;一个空值。

### `QJSValue::QJSValue(QJSValue::SpecialValue value = UndefinedValue)`

**作用与语义：**

建造了一辆带有特殊`value`的新QJS车。

### `QJSValue::QJSValue(bool value)`

**作用与语义：**

构造一个带有布尔`value`的新QJSValue。

### `QJSValue::QJSValue(const QLatin1String &value)`

**作用与语义：**

构建一个新的QJSValue，带有字符串`value`。

### `QJSValue::QJSValue(const QString &value)`

**作用与语义：**

构建一个新的QJSValue，带有字符串`value`。

### `QJSValue::QJSValue(const char *value)`

**作用与语义：**

构建一个新的QJSValue，带有字符串`value`。

### `QJSValue::QJSValue(double value)`

**作用与语义：**

构建了一个编号为`value`的新QJSValue。

### `QJSValue::QJSValue(int value)`

**作用与语义：**

构建了一个编号为`value`的新QJSValue。

### `QJSValue::QJSValue(uint value)`

**作用与语义：**

构建了一个编号为`value`的新QJSValue。

### `QJSValue::QJSValue(const QJSValue &other)`

**作用与语义：**

构建了一个新的QJSValue，复制了`other`。
注意，如果`other`是对象（即 `isObject()` 返回 true），则只有对底层对象的引用会被复制到新的脚本值中（即对象本身不会被复制）。

### `QJSValue::QJSValue(QJSValue &&other)`

**作用与语义：**

移动构造函数。从`other`移动到这个QJSValue对象。

### `[noexcept] QJSValue::~QJSValue()`

**作用与语义：**

毁了这个`QJSValue`。

### `QJSValue QJSValue::call(const QJSValueList &args = QJSValueList()) const`

**作用与语义：**

调用该`QJSValue`作为函数，将`args`作为参数传递给函数，并使用globalObject()作为“this”对象。返回函数返回的值。
如果该`QJSValue`不可调用，call() 不做任何操作，返回一个未定义的 `QJSValue`。
调用 call() 可能会导致脚本引擎出现异常;此时，call() 返回抛出的值（通常是 `Error` 对象）。你可以调用返回值的 `isError()` 来判断是否发生异常。

### `QJSValue QJSValue::callAsConstructor(const QJSValueList &args = QJSValueList()) const`

**作用与语义：**

创建一个新`Object`，并调用该`QJSValue`作为构造函数，使用所创建对象作为 `this' object and passing `args 的参数。如果构造调用的返回值是对象，则返回该对象;否则返回默认构造对象。
如果该`QJSValue`不是函数，callAsConstructor() 不做任何操作，返回一个未定义的`QJSValue`。
调用该函数可能会导致脚本引擎出现异常;此时返回抛出的值（通常是`Error`对象）。你可以调用返回值的`isError()`来判断是否发生异常。

### `QJSValue QJSValue::callWithInstance(const QJSValue &instance, const QJSValueList &args = QJSValueList()) const`

**作用与语义：**

调用该`QJSValue`作为函数，`instance` 作为 `this' object in the function call, and passing `args 作为函数的参数。返回函数返回的值。
如果该`QJSValue`不是函数，`call()`则不做任何操作，返回一个未定义的`QJSValue`。
注意，如果`instance`不是对象，则全局对象（见`QJSEngine::globalObject()`）将被用作“这个”对象。
调用 `call()` 可能会导致脚本引擎出现异常;此时， `call()` 返回抛出的值（通常是 `Error` 对象）。你可以调用返回值的 `isError()` 来判断是否发生异常。

### `bool QJSValue::deleteProperty(const QString &name)`

**作用与语义：**

尝试删除该对象在给定`name`中的属性。如果该属性被删除，则返回 true，否则返回 false。
该函数的行为与JavaScript删除操作符一致。具体来说：
- 不可配置属性不可删除。
- 即使该对象不具有给定`name`的属性（即不存在的属性“平凡可去”），该函数仍返回为真。
- 如果该对象没有给定`name`的自身属性，但`prototype()`链中的某个对象有，则原型对象的属性不会被删除，该函数返回为真。

### `bool QJSValue::equals(const QJSValue &other) const`

**作用与语义：**

如果该`QJSValue`等于`other`，则返回真;否则返回假。比较遵循ECMA-262第11.9.3节“抽象等式比较算法”中描述的行为。
即使该`QJSValue`的类型与`other`值类型不同，该函数仍可返回真;即比较不严格。例如，将数字9与字符串“9”比较返回为真;将未定义值与空值比较返回为真;将原始值为6的`Number`对象与原始值为“6”的对象比较`String`对象返回真;将数字1与布尔值比较`true`返回为真。如果你想进行不进行隐式值转换的比较，可以使用`strictlyEquals()`。
注意，如果该`QJSValue`或`other`值是对象，调用该函数对脚本引擎有副作用，因为引擎会调用对象的valueOf()函数（可能还有`toString()`），试图将对象转换为原始值（可能导致未捕获的脚本异常）。

### `QJSValue::ErrorType QJSValue::errorType() const`

**作用与语义：**

如果`QJSValue`是错误对象，则返回该所代表的错误类型。否则，返回`NoError."`。

### `bool QJSValue::hasOwnProperty(const QString &name) const`

**作用与语义：**

如果该对象具有给定`name`自身（非原型继承的）属性，则返回真;否则返回假。

### `bool QJSValue::hasProperty(const QString &name) const`

**作用与语义：**

如果该对象具有给定`name`的属性，则返回真;否则返回假。

### `bool QJSValue::isArray() const`

**作用与语义：**

如果该`QJSValue`是数组类的对象，则返回真;否则返回假。
注意：该方法相当于 JavaScript 中的 Array.isArray()。你可以用它来识别 JavaScript 数组，但它会返回任何非 JavaScript 数组的类数组对象的 `false`。这包括 QML 列表对象（值类型或对象类型）、JavaScript 类型数组、JavaScript ArrayBuffer 对象，以及你自己创建的任何自定义类数组对象。不过，这些都类似于 JavaScript 数组：它们通常暴露相同的方法，并且可以使用下标操作符。因此，使用该方法来判断一个对象是否可以作为数组使用是不建议的。

### `bool QJSValue::isBool() const`

**作用与语义：**

如果该`QJSValue`是布尔原始类型，则返回真;否则返回假。

### `bool QJSValue::isCallable() const`

**作用与语义：**

如果该`QJSValue`是函数，则返回真;否则返回假。

### `bool QJSValue::isDate() const`

**作用与语义：**

如果该`QJSValue`是Date类的对象，则返回true;否则返回false。

### `bool QJSValue::isError() const`

**作用与语义：**

如果该`QJSValue`是错误类的对象，则返回真;否则返回假。

### `bool QJSValue::isNull() const`

**作用与语义：**

如果该`QJSValue`为 Null 原始类型，则返回 true;否则返回 false。

### `bool QJSValue::isNumber() const`

**作用与语义：**

如果该`QJSValue`是原始类型 Number，则返回为真;否则返回为假。

### `bool QJSValue::isObject() const`

**作用与语义：**

如果该`QJSValue`对象类型为 ，则返回 true;否则返回 false。
注意函数值、变体值和`QObject`值都是对象，因此该函数对这些值返回为真。

### `bool QJSValue::isQMetaObject() const`

**作用与语义：**

如果该`QJSValue`是`QMetaObject`，则返回真;否则返回假。

### `bool QJSValue::isQObject() const`

**作用与语义：**

如果该`QJSValue`是`QObject`，则返回真;否则返回假。
注意：即使该`QJSValue`包裹的`QObject`已被删除，该函数仍返回为真。

### `bool QJSValue::isRegExp() const`

**作用与语义：**

如果该`QJSValue`是 RegExp 类的对象，则返回 true;否则返回 false。

### `bool QJSValue::isString() const`

**作用与语义：**

如果该`QJSValue`是原始类型 String，则返回 true;否则返回 false。

### `bool QJSValue::isUndefined() const`

**作用与语义：**

如果该`QJSValue`为原始类型未定义，或已清除管理值（通过删除引擎），则返回为真。否则返回为假。

### `bool QJSValue::isUrl() const`

**作用与语义：**

如果该`QJSValue`是 URL JavaScript 类的对象，则返回 true;否则返回 false。
注意：对于包含`QUrl`的`QJSValue`，该函数返回为假。不过，`toVariant().value<QUrl>()`在两种情况下都有效。

### `QJSValue QJSValue::property(const QString &name) const`

**作用与语义：**

返回该`QJSValue`属性的值，并返回给定`name`。如果不存在此类属性，则返回未定义的`QJSValue`。
如果该属性是用 getter 函数实现的（即 PropertyGetter 标志已设置），调用 property() 会对脚本引擎产生副作用，因为 getter 函数会被调用（可能导致未捕获的脚本异常）。如果发生异常，property() 返回抛出的值（通常是 `Error` 对象）。
要访问数组元素，请使用 `setProperty`（quint32 arrayIndex， const QJSValue &value） overload。

### `QJSValue QJSValue::property(quint32 arrayIndex) const`

**作用与语义：**

在给定的 `arrayIndex` 归还该属性。
可以通过两种方式访问数组中的元素。第一种是将数组索引作为属性名称：
第二种是使用取索引的超载：
这两种方法都达到了相同的结果，只是后者：
- 更易使用（可直接使用整数）
- 速度更快（不转换为整数）
如果该`QJSValue`不是数组对象，该函数的行为就像用 Properties 的字符串表示调用了 property（`arrayIndex`。

**官方示例：**

```cpp
 qDebug() << jsValueArray.property(QLatin1String("4")).toString();
```

### `QJSValue QJSValue::prototype() const`

**作用与语义：**

如果该`QJSValue`是对象，返回该对象的内部原型（`__proto__`属性）;否则返回未定义的`QJSValue`。

### `void QJSValue::setProperty(const QString &name, const QJSValue &value)`

**作用与语义：**

将该`QJSValue`属性的值与给定`name`定于给定`value`。
如果该`QJSValue`不是对象，这个函数就不做任何事。
如果该`QJSValue`还没有带有`name`的物业，则会创建一个新的物业。
要修改数组元素，请使用 `setProperty`（quint32 arrayIndex， const QJSValue &value） overload。

### `void QJSValue::setProperty(quint32 arrayIndex, const QJSValue &value)`

**作用与语义：**

将给定`arrayIndex`的属性映射到给定`value`。
可以通过两种方式修改数组中的元素。第一种是将数组索引作为属性名称：
第二种是使用取索引的超载：
这两种方法都达到了相同的结果，只是后者：
- 更易使用（可直接使用整数）
- 速度更快（不转换为整数）
如果该`QJSValue`不是数组对象，该函数的行为就像用 `arrayIndex` 的字符串表示调用了 setProperty() 一样。

**官方示例：**

```cpp
 jsValueArray.setProperty(QLatin1String("4"), value);
```

### `void QJSValue::setPrototype(const QJSValue &prototype)`

**作用与语义：**

如果该`QJSValue`是一个对象，则将该对象的内部原型（`__proto__`属性）设置为`prototype`;如果`QJSValue`为空，则将原型设为空;否则不做任何操作。
内部原型不应与名为“prototype”的公共属性混淆;公共原型通常只设置在作为构造函数的函数上。

### `bool QJSValue::strictlyEquals(const QJSValue &other) const`

**作用与语义：**

如果该`QJSValue`等于严格比较（无转换）时的`other`，则返回为真;否则返回为假。比较遵循ECMA-262第11.9.6节“严格等价比较算法”中描述的行为。
如果该`QJSValue`的类型与`other`值的类型不同，该函数返回为假。如果两者相等，结果取决于类型，如下表所示：
- `Type`：结果
- `Undefined`：真
- `Null`：真
- `Boolean`：当值都为真或为假时为真，否则为假
- `Number`：当任一值为NaN（非数）时为假;当值相等时为真，否则为假
- `String`：当两个值的字符序列完全相同时为真，否则为假
- `Object`：当两个值都指向同一对象时为真，否则为假

### `bool QJSValue::toBool() const`

**作用与语义：**

返回该`QJSValue`的布尔值，使用ECMA-262第9.2节“ToBoolean”中描述的转换规则。
注意，如果该`QJSValue`是一个对象，调用该函数对脚本引擎有副作用，因为引擎会调用对象的 valueOf() 函数（可能还会调用 `toString()`），试图将对象转换为原始值（可能导致未捕获的脚本异常）。

### `QDateTime QJSValue::toDateTime() const`

**作用与语义：**

返回该值的`QDateTime`表示，以当地时间计算。如果该`QJSValue`不是日期，或者日期的值是NaN（非数字），则返回无效`QDateTime`。

### `qint32 QJSValue::toInt() const`

**作用与语义：**

返回该`QJSValue`的带符号32位整数值，使用ECMA-262第9.5节“ToInt32”中描述的转换规则。
注意，如果该`QJSValue`是一个对象，调用该函数对脚本引擎有副作用，因为引擎会调用对象的valueOf()函数（可能还会调用`toString()`），试图将对象转换为原始值（可能导致未捕获的脚本异常）。

### `double QJSValue::toNumber() const`

**作用与语义：**

返回该`QJSValue`的编号值，定义见ECMA-262第9.3节，“ToNumber”。
注意，如果该`QJSValue`是一个对象，调用该函数对脚本引擎有副作用，因为引擎会调用对象的valueOf()函数（可能还会调用`toString()`），试图将对象转换为原始值（可能导致未捕获的脚本异常）。

### `QJSPrimitiveValue QJSValue::toPrimitive() const`

**作用与语义：**

将值转换为`QJSPrimitiveValue`。如果该值包含由`QJSPrimitiveValue`支持的类型，则该值被复制。否则，该值被转换为字符串，并存储在`QJSPrimitiveValue`中。
注意：将管理值转换为字符串可能会抛出异常。特别是，符号不能强制转换为字符串，或者自定义`toString()`方法可能会抛出异常。在这种情况下，结果是未定义的值，转换后引擎会携带错误。

### `const QMetaObject *QJSValue::toQMetaObject() const`

**作用与语义：**

* 如果此 `QJSValue` 是一个 `QMetaObject`，返回 `QJSValue` 表示的 `QMetaObject` 指针；否则返回 `nullptr`。* *。

### `QObject *QJSValue::toQObject() const`

**作用与语义：**

如果该`QJSValue`是`QObject`，则返回`QJSValue`所代表的`QObject`指针;否则返回`nullptr`。
如果该`QJSValue`包裹的`QObject`被删除，该函数返回 `nullptr`（即即使 返回 `isQObject()` 真，toQObject() 也可能返回 `nullptr`）。

### `QString QJSValue::toString() const`

**作用与语义：**

返回该`QJSValue`的字符串值，定义见ECMA-262第9.8节“ToString”。
注意，如果`QJSValue`是对象，调用该函数对脚本引擎有副作用，因为引擎会调用对象的 toString() 函数（可能还有 valueOf()），试图将对象转换为原始值（可能导致未捕获的脚本异常）。

### `quint32 QJSValue::toUInt() const`

**作用与语义：**

返回该`QJSValue`的无符号32位整数值，使用ECMA-262第9.6节“ToUint32”中描述的转换规则。
注意，如果该`QJSValue`是一个对象，调用该函数对脚本引擎有副作用，因为引擎会调用对象的valueOf()函数（可能还有`toString()`），试图将对象转换为原始值（可能导致脚本未捕获异常）。

### `QVariant QJSValue::toVariant(QJSValue::ObjectConversionBehavior behavior) const`

**作用与语义：**

如果该`QJSValue`可以转换为`QVariant`，则返回`QVariant`值;否则返回无效`QVariant`。一些JavaScript类型和对象在Qt中有原生表达式。这些表达式会被转换为其原生表达式。例如：
- `Input Type`：结果
- `Undefined`：一名病弱`QVariant`。
- `Null`：包含空指针（`QMetaType::Nullptr`）的`QVariant`。
- `Boolean`：包含布尔值的`QVariant`。
- `Number`：包含数字值的`QVariant`。
- `String`：包含字符串值的`QVariant`。
- `QVariant` 对象`: The result is the `QVariant'的对象值（无转换）。
- `QVariantMap` Object`: A `QVariantZXQQCODE 0000X0020ZXQQVariantMap 存储在对象中（无转换）。
- `QVariantHash` Object`: A `QVariantZXQQVariantZXQQCODE 0000X0023ZXQQVariantHash' 存储在对象中（无转换）。
- `QObject` Object`: A `QVariant` containing a pointer to the `QObject'。
- `Date Object`：包含日期值（`toDateTime()`）的`QVariant`。
- `RegularExpression` 包含正则表达式值的 Object`: A `QVariant'。
对于其他类型，`behavior`参数是相关的。如果给出`ConvertJSObjects`，则尝试尽力但可能有损的转换。通用的JavaScript对象被转换为`QVariantMap`。JavaScript数组被转换为`QVariantList`。每个属性或元素递归地转换为`QVariant`;不遵循循环引用。JavaScript函数对象被丢弃。如果给出`RetainJSObjects`，则`QJSValue`通过`QVariant::fromValue()`包裹成`QVariant`。由此产生的转换是无损的，但对象的内部结构无法立即被访问。

### `QVariant QJSValue::toVariant() const`

**作用与语义：**

返回Variant（`ConvertJSObjects`）。

### `QJSValue &QJSValue::operator=(QJSValue &&other)`

**作用与语义：**

移动为该`QJSValue`对象分配`other`。

### `QJSValue &QJSValue::operator=(const QJSValue &other)`

**作用与语义：**

赋予该`QJSValue`的`other`值。
注意，如果`other`是对象（`isObject()`返回true），只会被赋值到底层对象的引用;对象本身不会被复制。

### `QJSValueList`

**作用与语义：**

这是`QList`的typedef<`QJSValue`>。

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

`QJSValue` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
