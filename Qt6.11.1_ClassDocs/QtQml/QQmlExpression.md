# QQmlExpression

> Qt 6.11.1 · Qt Qml

## 1. 先建立直觉

**一句话定位：** `QQmlExpression` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** 这是 Qt Qml 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QQmlExpression` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQmlExpression>`
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

### 公有函数

- `QQmlExpression()`
- `QQmlExpression(QQmlContext *ctxt, QObject *scope, const QString &expression, QObject *parent = nullptr)`
- `QQmlExpression(const QQmlScriptString &script, QQmlContext *ctxt = nullptr, QObject *scope = nullptr, QObject *parent = nullptr)`
- `virtual ~QQmlExpression() override`
- `void clearError()`
- `int columnNumber() const`
- `QQmlContext * context() const`
- `QQmlEngine * engine() const`
- `QQmlError error() const`
- `QVariant evaluate(bool *valueIsUndefined = nullptr)`
- `QString expression() const`
- `bool hasError() const`
- `int lineNumber() const`
- `bool notifyOnValueChanged() const`
- `QObject * scopeObject() const`
- `void setExpression(const QString &expression)`
- `void setNotifyOnValueChanged(bool notifyOnChange)`
- `void setSourceLocation(const QString &url, int line, int column = 0)`
- `QString sourceFile() const`

### 信号

- `void valueChanged()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QQmlExpression::QQmlExpression()`

**作用与语义：**

创建一个无效的QQml表达式。
由于表达式没有关联的`QQmlContext`，这将是一个空表达式对象，其值始终是无效的`QVariant`。

### `QQmlExpression::QQmlExpression(QQmlContext *ctxt, QObject *scope, const QString &expression, QObject *parent = nullptr)`

**作用与语义：**

创建一个 QQmlExpression 对象，它是 `parent` 的子对象。
`expression` JavaScript 将在`ctxt` `QQmlContext`中执行。如果指定，`scope`对象的属性也会在表达式执行时处于作用域内。

### `[explicit] QQmlExpression::QQmlExpression(const QQmlScriptString &script, QQmlContext *ctxt = nullptr, QObject *scope = nullptr, QObject *parent = nullptr)`

**作用与语义：**

创建一个 QQmlExpression 对象，它是 `parent` 的子对象。
`script`提供了要评估的表达式、用于评估的上下文以及用于评估的范围对象。如果提供了，`ctxt`和`scope`将覆盖`script`提供的上下文和范围对象。

### `[override virtual noexcept] QQmlExpression::~QQmlExpression()`

**作用与语义：**

摧毁`QQmlExpression`实例。

### `void QQmlExpression::clearError()`

**作用与语义：**

清除所有表达式错误。之后调用`hasError()`将返回false。

### `int QQmlExpression::columnNumber() const`

**作用与语义：**

返回该表达式的源文件列号。源位置必须事先通过调用`setSourceLocation()`设置。

### `QQmlContext *QQmlExpression::context() const`

**作用与语义：**

返回该表达式所关联的`QQmlContext`，若无关联或`QQmlContext`被破坏则返回`nullptr`。

### `QQmlEngine *QQmlExpression::engine() const`

**作用与语义：**

返回该表达式关联的`QQmlEngine`，若无关联或`QQmlEngine`被破坏则返回`nullptr`。

### `QQmlError QQmlExpression::error() const`

**作用与语义：**

返回上次调用`evaluate()`的错误。如果没有错误，则返回无效的`QQmlError`实例。

### `QVariant QQmlExpression::evaluate(bool *valueIsUndefined = nullptr)`

**作用与语义：**

评估表达式，返回求值结果;如果表达式无效或有错误，则返回无效`QVariant`。
如果表达式得到未定义的值，`valueIsUndefined` 将设置为 true。

### `QString QQmlExpression::expression() const`

**作用与语义：**

返回表达式字符串。

### `bool QQmlExpression::hasError() const`

**作用与语义：**

如果最后一次调用`evaluate()`出现错误，则返回 true，否则返回 false。

### `int QQmlExpression::lineNumber() const`

**作用与语义：**

返回该表达式的源文件行号。源位置必须事先通过调用`setSourceLocation()`设置。

### `bool QQmlExpression::notifyOnValueChanged() const`

**作用与语义：**

如果当表达式的求值变化时发出`valueChanged()`信号，则返回为真。

### `QObject *QQmlExpression::scopeObject() const`

**作用与语义：**

如果提供，返回表达式的范围对象，否则返回0。
除了表达式`QQmlContext`提供的数据外，作用域对象的属性在表达式评估时也在作用域内。

### `void QQmlExpression::setExpression(const QString &expression)`

**作用与语义：**

将表达式设置为`expression`。

### `void QQmlExpression::setNotifyOnValueChanged(bool notifyOnChange)`

**作用与语义：**

设置当求值表达式值变化时是否发出`valueChanged()`信号。
如果`notifyOnChange`为真，`QQmlExpression`会监控表达式评估相关的属性，并在属性发生变化时发出`QQmlExpression::valueChanged()`。这使应用程序能够确保与表达式结果相关的任何值保持最新。
如果`notifyOnChange`为假（默认），`QQmlExpression`不会蒙提托与表达式评估相关的属性，`QQmlExpression::valueChanged()`也永远不会被输出。如果应用程序希望对表达式进行一次“一次性”的评估，这样做更高效。

### `void QQmlExpression::setSourceLocation(const QString &url, int line, int column = 0)`

**作用与语义：**

将该表达式的位置设置为`line`，`column` of `url`。这些信息被脚本引擎使用。

### `QString QQmlExpression::sourceFile() const`

**作用与语义：**

返回该表达式的源文件URL。源位置必须事先通过调用`setSourceLocation()`设置。

### `[signal] void QQmlExpression::valueChanged()`

**作用与语义：**

每次表达式值相较于上次计算时都会发出。表达式必须至少被计算一次（通过调用`QQmlExpression::evaluate()`），才能发射该信号。

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

`QQmlExpression` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
