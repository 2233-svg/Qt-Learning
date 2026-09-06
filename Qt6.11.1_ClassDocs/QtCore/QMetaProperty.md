# QMetaProperty

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“MetaProperty”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QMetaProperty` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QMetaProperty>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `(since 6.0) QUntypedBindable bindable(QObject *object) const`
- `QMetaEnum enumerator() const`
- `bool hasNotifySignal() const`
- `(since 6.0) bool isBindable() const`
- `bool isConstant() const`
- `bool isDesignable() const`
- `bool isEnumType() const`
- `bool isFinal() const`
- `bool isFlagType() const`
- `(since 6.11) bool isOverride() const`
- `bool isReadable() const`
- `bool isRequired() const`
- `bool isResettable() const`
- `bool isScriptable() const`
- `bool isStored() const`
- `bool isUser() const`
- `bool isValid() const`
- `(since 6.11) bool isVirtual() const`
- `bool isWritable() const`
- `(since 6.0) QMetaType metaType() const`
- `const char * name() const`
- `QMetaMethod notifySignal() const`
- `int notifySignalIndex() const`
- `int propertyIndex() const`
- `QVariant read(const QObject *object) const`
- `QVariant readOnGadget(const void *gadget) const`
- `int relativePropertyIndex() const`
- `bool reset(QObject *object) const`
- `bool resetOnGadget(void *gadget) const`
- `int revision() const`
- `(since 6.0) int typeId() const`
- `const char * typeName() const`
- `int userType() const`
- `bool write(QObject *object, const QVariant &value) const`
- `(since 6.6) bool write(QObject *object, QVariant &&v) const`
- `bool writeOnGadget(void *gadget, const QVariant &value) const`
- `(since 6.6) bool writeOnGadget(void *gadget, QVariant &&value) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[since 6.0] QUntypedBindable QMetaProperty::bindable(QObject *object) const`

**作用与语义：**

返回给定`object`属性的可绑定接口。
如果该属性不支持绑定，返回的接口将无效。

### `QMetaEnum QMetaProperty::enumerator() const`

**作用与语义：**

如果该属性的类型是枚举类型，则返回枚举子;否则返回的值未定义。

### `bool QMetaProperty::hasNotifySignal() const`

**作用与语义：**

如果该属性具有相应的变化通知信号，则返回`true`;否则返回`false`。

### `[since 6.0] bool QMetaProperty::isBindable() const`

**作用与语义：**

如果 `Q_PROPERTY()` 暴露绑定功能，则返回 `true`；否则返回 false。 这意味着您可以创建使用此属性作为依赖项的绑定，或者在此属性上安装 QPropertyObserver 对象。除非该属性为只读，否则您还可以在此属性上设置绑定。

### `bool QMetaProperty::isConstant() const`

**作用与语义：**

如果属性是常数，则返回`true`;否则返回`false`。
如果`Q_PROPERTY()`的`CONSTANT`属性被设置，则该属性是常数的。

### `bool QMetaProperty::isDesignable() const`

**作用与语义：**

如果`Q_PROPERTY()`的`DESIGNABLE`属性为假，返回`false`;否则返回`true`。

### `bool QMetaProperty::isEnumType() const`

**作用与语义：**

如果属性类型是枚举值，返回`true`;否则返回`false`。

### `bool QMetaProperty::isFinal() const`

**作用与语义：**

如果属性是最终的，则返回`true`;否则返回`false`。
如果`Q_PROPERTY()`的`FINAL`属性被设置，则该属性为最终属性。

### `bool QMetaProperty::isFlagType() const`

**作用与语义：**

如果属性类型是枚举值并用作标志，返回`true`;否则返回`false`。
标志可以通过OR操作符组合。标志类型隐含地也是枚举类型。

### `[since 6.11] bool QMetaProperty::isOverride() const`

**作用与语义：**

如果属性覆盖，返回`true`;否则返回`false`。
如果`Q_PROPERTY()`的`OVERRIDE`属性被设置，属性确实会覆盖。

### `bool QMetaProperty::isReadable() const`

**作用与语义：**

如果该属性可读，返回`true`;否则返回`false`。

### `bool QMetaProperty::isRequired() const`

**作用与语义：**

如果需要该属性，则返回`true`;否则返回`false`。
如果`Q_PROPERTY()`的`REQUIRED`属性被设置，则该属性为终结属性。

### `bool QMetaProperty::isResettable() const`

**作用与语义：**

如果该属性可以重置为默认值，返回`true`;否则返回`false`。

### `bool QMetaProperty::isScriptable() const`

**作用与语义：**

如果`Q_PROPERTY()`的`SCRIPTABLE`属性为假，返回`false`;否则返回真。

### `bool QMetaProperty::isStored() const`

**作用与语义：**

如果该属性被存储，返回`true`;否则返回false。
如果`Q_PROPERTY()`的`STORED`属性为假，函数返回`false`;否则返回为真。

### `bool QMetaProperty::isUser() const`

**作用与语义：**

如果`Q_PROPERTY()`的`USER`属性为假，返回`false`。否则返回真，表示该属性被指定为`USER`属性，即用户可编辑或以其他方式具有重要意义的属性。

### `bool QMetaProperty::isValid() const`

**作用与语义：**

如果该属性有效（可读），返回`true`;否则返回 `false`。

### `[since 6.11] bool QMetaProperty::isVirtual() const`

**作用与语义：**

如果属性是虚的，则返回`true`;否则返回`false`。
如果`Q_PROPERTY()`的`VIRTUAL`属性被设置，则该属性是虚的。

### `bool QMetaProperty::isWritable() const`

**作用与语义：**

如果该属性可写，返回`true`;否则返回false。

### `[since 6.0] QMetaType QMetaProperty::metaType() const`

**作用与语义：**

归还该房产的`QMetaType`。

### `const char *QMetaProperty::name() const`

**作用与语义：**

返回该物业的名称。

### `QMetaMethod QMetaProperty::notifySignal() const`

**作用与语义：**

如果指定了属性变更信号，返回`QMetaMethod`实例，否则返回无效`QMetaMethod`。

### `int QMetaProperty::notifySignalIndex() const`

**作用与语义：**

如果指定了属性变更信号，返回该索引，否则返回-1。

### `int QMetaProperty::propertyIndex() const`

**作用与语义：**

返回该属性的索引。

### `QVariant QMetaProperty::read(const QObject *object) const`

**作用与语义：**

从给定`object`读取该属性的值。如果能够读取，则返回该值;否则返回无效变体。

### `QVariant QMetaProperty::readOnGadget(const void *gadget) const`

**作用与语义：**

从给定`gadget`读取该属性的值。如果能读取，则返回该值;否则返回无效变体。
只有当该函数属于`Q_GADGET`属性时才应使用。

### `int QMetaProperty::relativePropertyIndex() const`

**作用与语义：**

返回该属性在包围元对象内的索引相对关系。

### `bool QMetaProperty::reset(QObject *object) const`

**作用与语义：**

用复位方法重置给定`object`的属性。如果复位成功，返回`true`;否则返回`false`。
重置方法是可选的;只有少数属性支持。

### `bool QMetaProperty::resetOnGadget(void *gadget) const`

**作用与语义：**

用重置方法重置给定`gadget`的属性。如果复位成功，返回`true`;否则返回`false`。
重置方法是可选的;只有少数属性支持。
只有当该函数属于`Q_GADGET`属性时才应使用。

### `int QMetaProperty::revision() const`

**作用与语义：**

如果`Q_REVISION`指定了属性修订版本，返回该修正版本，否则返回0。自Qt 6.0起，非零值被编码，并可用`QTypeRevision::fromEncodedVersion()`解码。

### `[since 6.0] int QMetaProperty::typeId() const`

**作用与语义：**

返回属性的存储类型。这与 `metaType()`.id() 相同。

### `const char *QMetaProperty::typeName() const`

**作用与语义：**

返回该属性类型的名称。

### `int QMetaProperty::userType() const`

**作用与语义：**

返回该属性的用户类型。返回值是注册在`QMetaType`中的值之一。
这等价于 `metaType()`.id()。

### `bool QMetaProperty::write(QObject *object, const QVariant &value) const`

**作用与语义：**

将`value`写为该属性对给定`object`的值。如果写入成功，则返回真;否则返回`false`。
如果`value`与该属性类型不同，则尝试转换。如果该属性可重置，空QVariant()等同于调用`reset()`;否则设置默认构造对象。
注意：该函数内部复制`value`。尽量使用r值重载。

### `[since 6.6] bool QMetaProperty::write(QObject *object, QVariant &&v) const`

**作用与语义：**

将`value`写为该属性对给定`object`的值。如果写入成功，则返回真;否则返回`false`。
如果`value`与该属性类型不同，则尝试转换。如果该属性可重置，空QVariant()等同于调用`reset()`;否则设置默认构造对象。
注意：该函数内部复制`value`。尽量使用r值重载。

### `bool QMetaProperty::writeOnGadget(void *gadget, const QVariant &value) const`

**作用与语义：**

将`value`写为该属性对给定`gadget`的值。如果写入成功，则返回真;否则返回`false`。
该函数仅在该属性属于`Q_GADGET`时使用。

### `[since 6.6] bool QMetaProperty::writeOnGadget(void *gadget, QVariant &&value) const`

**作用与语义：**

将`value`写为该属性对给定`gadget`的值。如果写入成功，则返回真;否则返回`false`。
该函数仅在该属性属于`Q_GADGET`时使用。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QMetaProperty` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
