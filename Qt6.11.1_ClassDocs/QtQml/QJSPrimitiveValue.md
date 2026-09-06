# QJSPrimitiveValue

> Qt 6.11.1 · Qt Qml

## 1. 先建立直觉

**一句话定位：** `QJSPrimitiveValue` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** 这是 Qt Qml 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QJSPrimitiveValue` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QJSPrimitiveValue>`
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

- `enum Type { Undefined, Null, Boolean, Integer, Double, String }`

### 公有函数

- `QJSPrimitiveValue()`
- `QJSPrimitiveValue(QJSPrimitiveNull null)`
- `QJSPrimitiveValue(QJSPrimitiveUndefined undefined)`
- `QJSPrimitiveValue(QString value)`
- `QJSPrimitiveValue(bool value)`
- `QJSPrimitiveValue(const QVariant &value)`
- `QJSPrimitiveValue(double value)`
- `QJSPrimitiveValue(int value)`
- `(since 6.4) QJSPrimitiveValue(QMetaType type, const void *value)`
- `(since 6.6) const void * constData() const`
- `(since 6.6) void * data()`
- `(since 6.6) const void * data() const`
- `bool equals(const QJSPrimitiveValue &other) const`
- `(since 6.6) QMetaType metaType() const`
- `bool strictlyEquals(const QJSPrimitiveValue &other) const`
- `(since 6.6) QJSPrimitiveValue to() const`
- `bool toBoolean() const`
- `double toDouble() const`
- `int toInteger() const`
- `QString toString() const`
- `QJSPrimitiveValue::Type type() const`

### 相关非成员函数

- `(since 6.1) bool operator!=(const QJSPrimitiveValue &lhs, const QJSPrimitiveValue &rhs)`
- `(since 6.1) QJSPrimitiveValue operator*(const QJSPrimitiveValue &lhs, const QJSPrimitiveValue &rhs)`
- `(since 6.1) QJSPrimitiveValue operator+(const QJSPrimitiveValue &lhs, const QJSPrimitiveValue &rhs)`
- `(since 6.1) QJSPrimitiveValue operator-(const QJSPrimitiveValue &lhs, const QJSPrimitiveValue &rhs)`
- `(since 6.1) QJSPrimitiveValue operator/(const QJSPrimitiveValue &lhs, const QJSPrimitiveValue &rhs)`
- `(since 6.1) bool operator<(const QJSPrimitiveValue &lhs, const QJSPrimitiveValue &rhs)`
- `(since 6.1) bool operator<=(const QJSPrimitiveValue &lhs, const QJSPrimitiveValue &rhs)`
- `(since 6.1) bool operator==(const QJSPrimitiveValue &lhs, const QJSPrimitiveValue &rhs)`
- `(since 6.1) bool operator>(const QJSPrimitiveValue &lhs, const QJSPrimitiveValue &rhs)`
- `(since 6.1) bool operator>=(const QJSPrimitiveValue &lhs, const QJSPrimitiveValue &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QJSPrimitiveValue::Type`

**作用与语义：**

这个枚举指定了 `QJSPrimitiveValue` 可能包含的类型。
- `QJSPrimitiveValue::Undefined`: `0`; JavaScript 的 Undefined 值。
- `QJSPrimitiveValue::Null`: `1`; JavaScript 的 null 值。事实上，这并不是一个独立的 JavaScript 类型，而是 Object 类型的一个特殊值。由于它非常常见且无需 JavaScript 引擎即可存储，因此仍然被支持。
- `QJSPrimitiveValue::Boolean`: `2`; JavaScript 的 Boolean 值。
- `QJSPrimitiveValue::Integer`: `3`; 一个整数。这是 JavaScript Number 类型的一个特殊情况。JavaScript 并没有实际的整数类型，但 ECMA-262 标准包含了一些规则，用于将一个 Number 转换，以便为某些只适用于整数的运算符做准备，特别是位移运算符。`QJSPrimitiveValue` 的 Integer 类型表示这种转换后的结果。
- `QJSPrimitiveValue::Double`: `4`; 一个 JavaScript Number 值。
- `QJSPrimitiveValue::String`: `5`; 一个 JavaScript String 值。

### `[constexpr noexcept] QJSPrimitiveValue::QJSPrimitiveValue()`

**作用与语义：**

创建 QJSPrimitiveValue 类型为 Undefined。

### `[constexpr noexcept] QJSPrimitiveValue::QJSPrimitiveValue(QJSPrimitiveNull null)`

**作用与语义：**

创建 QJSPrimitiveValue 值为 `null`，类型为 Null。

### `[constexpr noexcept] QJSPrimitiveValue::QJSPrimitiveValue(QJSPrimitiveUndefined undefined)`

**作用与语义：**

创建价值`undefined`的QJSPrimitiveValue，类型为Undefined。

### `[noexcept] QJSPrimitiveValue::QJSPrimitiveValue(QString value)`

**作用与语义：**

创建 QJSPrimitiveValue 值 `value` 和类型 String。

### `[constexpr noexcept] QJSPrimitiveValue::QJSPrimitiveValue(bool value)`

**作用与语义：**

创建一个 QJSPrimitiveValue，值为 和 类型为 Boolean `value`。

### `[explicit noexcept] QJSPrimitiveValue::QJSPrimitiveValue(const QVariant &value)`

**作用与语义：**

如果`value`的内容可以存储在 QJSPrimtiveValue 中，则从 QJSPrimitiveValue 创建 QJSPrimitiveValue。否则，这会导致 QJSPrimitiveValue 类型为 Undefined。

### `[constexpr noexcept] QJSPrimitiveValue::QJSPrimitiveValue(double value)`

**作用与语义：**

创建 QJS 的 `value` 的 QJSPrimitiveValue ，类型为 Double。

### `[constexpr noexcept] QJSPrimitiveValue::QJSPrimitiveValue(int value)`

**作用与语义：**

创建一个 QJSPrimitiveValue 的值为 `value`，类型为整数。

### `[noexcept default, since 6.4] QJSPrimitiveValue::QJSPrimitiveValue(QMetaType type, const void *value)`

**作用与语义：**

创建类型为`type`的QJSPrimitiveValue，如果`type`可以存储在QJSPrimtiveValue中，则初始化为`value`。在这种情况下，`value`不能是nullptr。如果无法存储`type`，则生成一个类型为未定义的QJSPrimitiveValue。
注意你必须传递你想存储变量的地址。
通常你不必使用这个构造函数，而是用取`QVariant`的那个构造函数。

### `[constexpr, since 6.6] const void *QJSPrimitiveValue::data() const`

**作用与语义：**

返回指向所包含值的指针，作为一个无法写入的通用空洞*。

### `[constexpr, since 6.6] void *QJSPrimitiveValue::data()`

**作用与语义：**

返回指向所含数据的指针，作为一个可写入的通用空洞*。

### `[constexpr] bool QJSPrimitiveValue::equals(const QJSPrimitiveValue &other) const`

**作用与语义：**

对该`QJSPrimitiveValue`和`other`执行JavaScript的“==”操作，并返回结果。

### `[constexpr, since 6.6] QMetaType QJSPrimitiveValue::metaType() const`

**作用与语义：**

返回存储在`QJSPrimitiveValue`中的`QMetaType`值。

### `[constexpr] bool QJSPrimitiveValue::strictlyEquals(const QJSPrimitiveValue &other) const`

**作用与语义：**

对该`QJSPrimitiveValue`和`other`执行JavaScript的“===”操作，并返回结果。

### `[since 6.6] template <QJSPrimitiveValue::Type type> QJSPrimitiveValue QJSPrimitiveValue::to() const`

**作用与语义：**

强制将值强制到指定类型，并将结果作为新`QJSPrimitiveValue`返回。

### `[constexpr] bool QJSPrimitiveValue::toBoolean() const`

**作用与语义：**

返回由JavaScript规则强制生成的布尔值。

### `[constexpr] double QJSPrimitiveValue::toDouble() const`

**作用与语义：**

返回根据JavaScript规则强制到的JavaScript编号值。

### `[constexpr] int QJSPrimitiveValue::toInteger() const`

**作用与语义：**

返回根据JavaScript准备位移操作时应用的规则强制为整数32位数的值。

### `QString QJSPrimitiveValue::toString() const`

**作用与语义：**

返回被 JavaScript 规则强制到的 JavaScript 字符串值。

### `[constexpr] QJSPrimitiveValue::Type QJSPrimitiveValue::type() const`

**作用与语义：**

返回`QJSPrimitiveValue`类型。

### `[constexpr, since 6.1] bool operator!=(const QJSPrimitiveValue &lhs, const QJSPrimitiveValue &rhs)`

**作用与语义：**

对`lhs`和`rhs`执行JavaScript的“！==”操作，并返回结果。

### `[since 6.1] QJSPrimitiveValue operator*(const QJSPrimitiveValue &lhs, const QJSPrimitiveValue &rhs)`

**作用与语义：**

对`lhs`和`rhs`执行JavaScript的“*”操作，并返回结果。

### `[since 6.1] QJSPrimitiveValue operator+(const QJSPrimitiveValue &lhs, const QJSPrimitiveValue &rhs)`

**作用与语义：**

在`lhs`和`rhs`上执行JavaScript的“ ''操作，并返回结果。

### `[since 6.1] QJSPrimitiveValue operator-(const QJSPrimitiveValue &lhs, const QJSPrimitiveValue &rhs)`

**作用与语义：**

对`lhs`和`rhs`执行JavaScript的“-”操作，并返回结果。

### `[since 6.1] QJSPrimitiveValue operator/(const QJSPrimitiveValue &lhs, const QJSPrimitiveValue &rhs)`

**作用与语义：**

在 `lhs` 和 `rhs` 之间执行 JavaScript 的 '/' 操作，并返回结果。

### `[constexpr, since 6.1] bool operator<(const QJSPrimitiveValue &lhs, const QJSPrimitiveValue &rhs)`

**作用与语义：**

对`lhs`和`rhs`执行JavaScript的“<”操作，并返回结果。

### `[constexpr, since 6.1] bool operator<=(const QJSPrimitiveValue &lhs, const QJSPrimitiveValue &rhs)`

**作用与语义：**

对`lhs`和`rhs`执行JavaScript的“<=”操作，并返回结果。

### `[constexpr, since 6.1] bool operator==(const QJSPrimitiveValue &lhs, const QJSPrimitiveValue &rhs)`

**作用与语义：**

对 `lhs` 和 `rhs` 执行 JavaScript 的 '===' 操作，并返回结果。

### `[constexpr, since 6.1] bool operator>(const QJSPrimitiveValue &lhs, const QJSPrimitiveValue &rhs)`

**作用与语义：**

对`lhs`和`rhs`执行JavaScript的“>”操作，并返回结果。

### `[constexpr, since 6.1] bool operator>=(const QJSPrimitiveValue &lhs, const QJSPrimitiveValue &rhs)`

**作用与语义：**

对`lhs`和`rhs`执行JavaScript的“>=”操作，并返回结果。

### `(since 6.6) const void * constData() const`

**作用与语义：**

返回指向所包含值的指针，作为一个无法写入的通用空洞*。

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

`QJSPrimitiveValue` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
