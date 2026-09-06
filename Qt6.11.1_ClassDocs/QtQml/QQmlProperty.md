# QQmlProperty

> Qt 6.11.1 · Qt Qml

## 1. 先建立直觉

**一句话定位：** `QQmlProperty` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** 这是 Qt Qml 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QQmlProperty` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQmlProperty>`
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

### 公有类型

- `enum PropertyTypeCategory { InvalidCategory, List, Object, Normal }`
- `enum Type { Invalid, Property, SignalProperty }`

### 属性

- `name : const QString`
- `object : QObject* const`

### 公有函数

- `QQmlProperty()`
- `QQmlProperty(QObject *obj)`
- `QQmlProperty(QObject *obj, QQmlContext *ctxt)`
- `QQmlProperty(QObject *obj, QQmlEngine *engine)`
- `QQmlProperty(QObject *obj, const QString &name)`
- `QQmlProperty(QObject *obj, const QString &name, QQmlContext *ctxt)`
- `QQmlProperty(QObject *obj, const QString &name, QQmlEngine *engine)`
- `QQmlProperty(const QQmlProperty &other)`
- `bool connectNotifySignal(QObject *dest, const char *slot) const`
- `bool connectNotifySignal(QObject *dest, int method) const`
- `bool hasNotifySignal() const`
- `int index() const`
- `bool isDesignable() const`
- `bool isProperty() const`
- `bool isResettable() const`
- `bool isSignalProperty() const`
- `bool isValid() const`
- `bool isWritable() const`
- `QMetaMethod method() const`
- `QString name() const`
- `bool needsNotifySignal() const`
- `QObject * object() const`
- `QMetaProperty property() const`
- `QMetaType propertyMetaType() const`
- `int propertyType() const`
- `QQmlProperty::PropertyTypeCategory propertyTypeCategory() const`
- `const char * propertyTypeName() const`
- `QVariant read() const`
- `bool reset() const`
- `QQmlProperty::Type type() const`
- `bool write(const QVariant &value) const`
- `QQmlProperty & operator=(const QQmlProperty &other)`
- `bool operator==(const QQmlProperty &other) const`

### 静态公有成员

- `QVariant read(const QObject *object, const QString &name)`
- `QVariant read(const QObject *object, const QString &name, QQmlContext *ctxt)`
- `QVariant read(const QObject *object, const QString &name, QQmlEngine *engine)`
- `bool write(QObject *object, const QString &name, const QVariant &value)`
- `bool write(QObject *object, const QString &name, const QVariant &value, QQmlContext *ctxt)`
- `bool write(QObject *object, const QString &name, const QVariant &value, QQmlEngine *engine)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QQmlProperty::PropertyTypeCategory`

**作用与语义：**

该枚举指定了一个QML属性的范畴。
- `QQmlProperty::InvalidCategory`：`0`;该属性无效，或为信号属性。
- `QQmlProperty::List`：`1`;该属性属于`QQmlListProperty`列表属性
- `QQmlProperty::Object`：`2`;该属性是一个 `QObject` 派生类型指针
- `QQmlProperty::Normal`：`3`;该属性是一个正规值属性。

### `enum QQmlProperty::Type`

**作用与语义：**

该枚举指定了一种QML属性。
- `QQmlProperty::Invalid`：`0`;该属性无效。
- `QQmlProperty::Property`：`1`;该属性是一个正则Qt属性。
- `QQmlProperty::SignalProperty`：`2`;该属性是一个信号属性。

### `[read-only] name : const QString`

**作用与语义：**

该属性即为QML属性的名称。

**如何使用：** 调用 `name()` 读取当前值；它不会修改应用状态。

### `[read-only] object : QObject* const`

**作用与语义：**

该属性包含QML属性所表示的`QObject`。

**如何使用：** 调用 `object()` 读取当前值；它不会修改应用状态。

### `QQmlProperty::QQmlProperty()`

**作用与语义：**

创建一个无效的QQmlProperty。

### `QQmlProperty::QQmlProperty(QObject *obj)`

**作用与语义：**

为默认属性`obj`创建QQmlProperty。如果没有默认属性，将创建一个无效的QQmlProperty。

### `QQmlProperty::QQmlProperty(QObject *obj, QQmlContext *ctxt)`

**作用与语义：**

使用 `context` `ctxt` 为 `obj` 的默认属性创建 QQmlProperty。如果没有默认属性，将创建一个无效的 QQmlProperty。

### `QQmlProperty::QQmlProperty(QObject *obj, QQmlEngine *engine)`

**作用与语义：**

利用`engine`提供的 QML 组件实例化环境，为 `obj` 的默认属性创建 QQmlProperty。如果没有默认属性，将生成一个无效的 QQmlProperty。

### `QQmlProperty::QQmlProperty(QObject *obj, const QString &name)`

**作用与语义：**

为`obj`的属性`name`创建QQmlProperty。

### `QQmlProperty::QQmlProperty(QObject *obj, const QString &name, QQmlContext *ctxt)`

**作用与语义：**

利用`context` `ctxt`为`obj`的`name`创建QQmlProperty。
没有上下文创建 QQmlProperty 会使某些属性——比如附加属性——无法访问。

### `QQmlProperty::QQmlProperty(QObject *obj, const QString &name, QQmlEngine *engine)`

**作用与语义：**

为`obj`的属性创建QQmlProperty，`name`用于实例化QML组件，该环境由`engine`提供的。

### `QQmlProperty::QQmlProperty(const QQmlProperty &other)`

**作用与语义：**

制作一份`other`副本。

### `bool QQmlProperty::connectNotifySignal(QObject *dest, const char *slot) const`

**作用与语义：**

将该属性的变化通知信号连接到`dest`对象指定的`slot`，并返回true。如果该元属性不代表常规Qt属性，或者没有变更通知信号，或者`dest`对象没有指定的`slot`，则返回false。
注意：`slot`应使用SLOT()宏传递，以确保正确识别。

### `bool QQmlProperty::connectNotifySignal(QObject *dest, int method) const`

**作用与语义：**

将该属性的变更通知信号与`dest`对象指定的`method`连接起来，并返回true。如果该元属性不代表常规的Qt属性，或者没有变更通知信号，或者`dest`对象没有指定的`method`，则返回false。

### `bool QQmlProperty::hasNotifySignal() const`

**作用与语义：**

如果属性具有变更通知信号，则返回真，否则返回为真。

### `int QQmlProperty::index() const`

**作用与语义：**

返回该属性的 Qt 元对象索引。

### `bool QQmlProperty::isDesignable() const`

**作用与语义：**

如果该属性是可设计的，则返回真，否则返回假。

### `bool QQmlProperty::isProperty() const`

**作用与语义：**

如果该`QQmlProperty`表示正则Qt属性，则返回为真。

### `bool QQmlProperty::isResettable() const`

**作用与语义：**

如果属性可重置，则返回真，否则返回为真。

### `bool QQmlProperty::isSignalProperty() const`

**作用与语义：**

如果该`QQmlProperty`代表QML信号属性，则返回为真。

### `bool QQmlProperty::isValid() const`

**作用与语义：**

如果`QQmlProperty`涉及有效属性，则返回真，否则返回真。

### `bool QQmlProperty::isWritable() const`

**作用与语义：**

如果属性可写，则返回真，否则返回为真。

### `QMetaMethod QQmlProperty::method() const`

**作用与语义：**

如果该属性是`SignalProperty`，则返回该属性的`QMetaMethod`，否则返回无效`QMetaMethod`。

### `QString QQmlProperty::name() const`

**作用与语义：**

返回该QML属性的名称。
注意：物业名称的获取函数。

### `bool QQmlProperty::needsNotifySignal() const`

**作用与语义：**

如果属性需要变更通知信号以保证绑定保持最新，则返回 true;否则返回 false。
某些属性，如附加属性或值永不变化的属性，不需要变更通知器。

### `QObject *QQmlProperty::object() const`

**作用与语义：**

还给`QQmlProperty`的 `QObject`。
注意：属性对象的Getter函数。

### `QMetaProperty QQmlProperty::property() const`

**作用与语义：**

返回与该QML属性相关的Qt属性。

### `QMetaType QQmlProperty::propertyMetaType() const`

**作用与语义：**

返回该属性的元类型。

### `int QQmlProperty::propertyType() const`

**作用与语义：**

返回属性的元类型 id，若属性没有元类型则返回 `QMetaType::UnknownType`。

### `QQmlProperty::PropertyTypeCategory QQmlProperty::propertyTypeCategory() const`

**作用与语义：**

返回属性类别。

### `const char *QQmlProperty::propertyTypeName() const`

**作用与语义：**

返回属性的类型名称，若属性没有类型名称则返回 0。

### `QVariant QQmlProperty::read() const`

**作用与语义：**

返回房产价值。

### `[static] QVariant QQmlProperty::read(const QObject *object, const QString &name)`

**作用与语义：**

返回`name`属性值`object`。该方法等价于：

**官方示例：**

```cpp
 QQmlProperty p(object, name);
 p.read();
```

### `[static] QVariant QQmlProperty::read(const QObject *object, const QString &name, QQmlContext *ctxt)`

**作用与语义：**

使用`context` `ctxt`返回`object`的`name`属性值。该方法等价于：

**官方示例：**

```cpp
 QQmlProperty p(object, name, context);
 p.read();
```

### `[static] QVariant QQmlProperty::read(const QObject *object, const QString &name, QQmlEngine *engine)`

**作用与语义：**

返回`engine`提供的环境实例化QML组件时`object`的`name`属性值。.该方法等价于：

**官方示例：**

```cpp
 QQmlProperty p(object, name, engine);
 p.read();
```

### `bool QQmlProperty::reset() const`

**作用与语义：**

如果该属性可重置，则返回 true。如果属性不可重置，则不会发生任何事，返回 false。

### `QQmlProperty::Type QQmlProperty::type() const`

**作用与语义：**

返回房产类型。

### `bool QQmlProperty::write(const QVariant &value) const`

**作用与语义：**

将属性值设为`value`。成功时返回`true`，或者如果`value`类型错误而无法设置，则返回`false`。

### `[static] bool QQmlProperty::write(QObject *object, const QString &name, const QVariant &value)`

**作用与语义：**

写`value`到`object`的`name`属性。该方法等价于：
成功时回报`true`，`false`其他情况。

**官方示例：**

```cpp
 QQmlProperty p(object, name);
 p.write(value);
```

### `[static] bool QQmlProperty::write(QObject *object, const QString &name, const QVariant &value, QQmlContext *ctxt)`

**作用与语义：**

利用`context` `ctxt`写入`object`的`name`属性`value`。该方法等价于：
成功时`true`回报，`false`其他情况。

**官方示例：**

```cpp
 QQmlProperty p(object, name, ctxt);
 p.write(value);
```

### `[static] bool QQmlProperty::write(QObject *object, const QString &name, const QVariant &value, QQmlEngine *engine)`

**作用与语义：**

`value`写入`object`的`name`属性，使用`engine`提供的QML组件实例化环境。该方法等价于：
成功时`true`回报，`false`其他情况。

**官方示例：**

```cpp
 QQmlProperty p(object, name, engine);
 p.write(value);
```

### `QQmlProperty &QQmlProperty::operator=(const QQmlProperty &other)`

**作用与语义：**

把`other`分配到这个`QQmlProperty`。

### `bool QQmlProperty::operator==(const QQmlProperty &other) const`

**作用与语义：**

如果 `other` 且该`QQmlProperty`表示相同的属性，则返回为真。

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

`QQmlProperty` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
