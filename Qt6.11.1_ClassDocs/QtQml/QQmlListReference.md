# QQmlListReference

> Qt 6.11.1 · Qt Qml

## 1. 先建立直觉

**一句话定位：** `QQmlListReference` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** 这是 Qt Qml 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QQmlListReference` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQmlListReference>`
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

- `QQmlListReference()`
- `(since 6.1) QQmlListReference(const QVariant &variant)`
- `QQmlListReference(QObject *object, const char *property)`
- `bool append(QObject *object) const`
- `QObject * at(qsizetype index) const`
- `bool canAppend() const`
- `bool canAt() const`
- `bool canClear() const`
- `bool canCount() const`
- `bool canRemoveLast() const`
- `bool canReplace() const`
- `bool clear() const`
- `qsizetype count() const`
- `bool isManipulable() const`
- `bool isReadable() const`
- `bool isValid() const`
- `const QMetaObject * listElementType() const`
- `QObject * object() const`
- `bool removeLast() const`
- `bool replace(qsizetype index, QObject *object) const`
- `(since 6.2) qsizetype size() const`
- `bool operator==(const QQmlListReference &other) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QQmlListReference::QQmlListReference()`

**作用与语义：**

构造一个无效实例。

### `[explicit, since 6.1] QQmlListReference::QQmlListReference(const QVariant &variant)`

**作用与语义：**

从包含`QQmlListProperty`的`QVariant` `variant`构造 QQmlListReference。如果`variant`不包含列表属性，则创建无效的 QQmlListReference。如果在引用构建后，拥有列表属性的对象被销毁，则该对象将自动失效。也就是说，即使对象被删除，仍可安全地保留 QQmlListReference 实例。

### `QQmlListReference::QQmlListReference(QObject *object, const char *property)`

**作用与语义：**

为`object`的`property`构造一个QQmlListReference。如果`property`不是列表属性，则创建一个无效的QQmlListReference。如果`object`在引用构建后被销毁，它将自动变为无效。也就是说，即使`object`被删除，仍然可以安全保留QQmlListReference实例。

### `bool QQmlListReference::append(QObject *object) const`

**作用与语义：**

将`object`附加到列表中。如果操作成功，返回为真，否则返回为假。

### `QObject *QQmlListReference::at(qsizetype index) const`

**作用与语义：**

返回列表元素，`index` 返回，操作失败时返回 `nullptr`。

### `bool QQmlListReference::canAppend() const`

**作用与语义：**

如果列表属性可以附加，则返回真，否则返回 false。如果引用无效，则返回 false。

### `bool QQmlListReference::canAt() const`

**作用与语义：**

如果列表属性可以通过索引查询，则返回真，否则返回 false。如果引用无效，则返回 false。

### `bool QQmlListReference::canClear() const`

**作用与语义：**

如果列表属性可以清除，则返回真，否则返回 false。如果引用无效，则返回 false。

### `bool QQmlListReference::canCount() const`

**作用与语义：**

如果列表属性可以查询其元素计数，则返回真;否则返回为假。如果引用无效，则返回假。

### `bool QQmlListReference::canRemoveLast() const`

**作用与语义：**

如果最后一个项可以从列表属性中移除，则返回 true，否则返回 false。如果引用无效，则返回 false。

### `bool QQmlListReference::canReplace() const`

**作用与语义：**

如果列表属性中的项可以被替换，则返回 true，否则返回 false。如果引用无效，则返回 false。

### `bool QQmlListReference::clear() const`

**作用与语义：**

清除列表。如果操作成功，返回真，否则返回false。

### `qsizetype QQmlListReference::count() const`

**作用与语义：**

返回列表中的项目数量，若操作失败则返回0。

### `bool QQmlListReference::isManipulable() const`

**作用与语义：**

如果实现了`at()`、`count()`、`append()`，以及`clear()`或`removeLast()`，则返回真，以便操作列表。
请注意，`replace()`和`removeLast()`可以通过存放所有物品并用`clear()`和 `append()`重建列表来模拟。因此，操作列表并非必须有这些。此外，`clear()`可以通过`removeLast()`来模拟。

### `bool QQmlListReference::isReadable() const`

**作用与语义：**

如果实现了`at()`和`count()`，则返回真，这样你就能访问这些元素。

### `bool QQmlListReference::isValid() const`

**作用与语义：**

如果实例引用有效的列表属性，则返回真，否则返回为假。

### `const QMetaObject *QQmlListReference::listElementType() const`

**作用与语义：**

返回列表属性中存储元素的`QMetaObject`，若引用无效则返回`nullptr`。
`QMetaObject`可以提前判断某个实例是否可以添加到列表中。如果你在构建时没有通过引擎，可能会返回 nullptr。

### `QObject *QQmlListReference::object() const`

**作用与语义：**

返回列表属性的对象。如果引用无效，返回`nullptr`。

### `bool QQmlListReference::removeLast() const`

**作用与语义：**

删除列表中的最后一项。如果操作成功，返回 true，否则返回 false。

### `bool QQmlListReference::replace(qsizetype index, QObject *object) const`

**作用与语义：**

将列表中`index`项替换为 `object`。如果操作成功，返回 true，否则返回 false。

### `[since 6.2] qsizetype QQmlListReference::size() const`

**作用与语义：**

返回列表中的项目数量，若操作失败则返回0。

### `bool QQmlListReference::operator==(const QQmlListReference &other) const`

**作用与语义：**

将此`QQmlListReference`与 `other` 比较，若相等则返回`true`。只有当其中一个通过复制赋值或复制构造从另一个生成时，才被视为相等。
注意：对同一对象的独立创建引用不被视为相等。

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

`QQmlListReference` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
