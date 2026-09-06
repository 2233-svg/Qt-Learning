# QQmlError

> Qt 6.11.1 · Qt Qml

## 1. 先建立直觉

**一句话定位：** `QQmlError` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** 这是 Qt Qml 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QQmlError` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQmlError>`
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

```cpp
// C++ 侧暴露属性/信号后，在 QML 中建立绑定。
// 变化时发出 notify signal，避免在绑定表达式中直接修改状态。
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QQmlError()`
- `QQmlError(const QQmlError &other)`
- `int column() const`
- `QString description() const`
- `bool isValid() const`
- `int line() const`
- `QtMsgType messageType() const`
- `QObject * object() const`
- `void setColumn(int column)`
- `void setDescription(const QString &description)`
- `void setLine(int line)`
- `void setMessageType(QtMsgType messageType)`
- `void setObject(QObject *object)`
- `void setUrl(const QUrl &url)`
- `QString toString() const`
- `QUrl url() const`
- `QQmlError & operator=(const QQmlError &other)`

### 相关非成员函数

- `QDebug operator<<(QDebug debug, const QQmlError &error)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QQmlError::QQmlError()`

**作用与语义：**

生成一个空的错误对象。

### `QQmlError::QQmlError(const QQmlError &other)`

**作用与语义：**

创建`other`副本。

### `int QQmlError::column() const`

**作用与语义：**

返回错误列编号。

### `QString QQmlError::description() const`

**作用与语义：**

返回错误描述。

### `bool QQmlError::isValid() const`

**作用与语义：**

如果该错误有效，则返回真，否则返回为真。

### `int QQmlError::line() const`

**作用与语义：**

返回错误行号。

### `QtMsgType QQmlError::messageType() const`

**作用与语义：**

返回消息类型。

### `QObject *QQmlError::object() const`

**作用与语义：**

返回该错误发生的最近对象。绑定属性表达式中的异常将该属性归属于对象。其他异常则为0。

### `void QQmlError::setColumn(int column)`

**作用与语义：**

设置误差`column`数值。

### `void QQmlError::setDescription(const QString &description)`

**作用与语义：**

设置错误`description`。

### `void QQmlError::setLine(int line)`

**作用与语义：**

设置误差`line`数值。

### `void QQmlError::setMessageType(QtMsgType messageType)`

**作用与语义：**

设置该消息的`messageType`。消息类型决定了哪些`QDebug`处理器负责接收消息。

### `void QQmlError::setObject(QObject *object)`

**作用与语义：**

设置最接近该错误发生`object`。

### `void QQmlError::setUrl(const QUrl &url)`

**作用与语义：**

为导致该错误的文件设置`url`。

### `QString QQmlError::toString() const`

**作用与语义：**

返回错误为人类可读字符串。

### `QUrl QQmlError::url() const`

**作用与语义：**

返回导致该错误的文件的URL。

### `QQmlError &QQmlError::operator=(const QQmlError &other)`

**作用与语义：**

将`other`分配到该错误对象。

### `QDebug operator<<(QDebug debug, const QQmlError &error)`

**作用与语义：**

输出一个人类可读的版本`error`给`debug`。

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

`QQmlError` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
