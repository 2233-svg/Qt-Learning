# QUntypedBindable

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“UntypedBindable”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QUntypedBindable` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QUntypedBindable>`
- 继承自：未在类页中列出
- 直接派生类：QBindable

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

- `QUntypedBindable()`
- `QUntypedBindable(Property *property)`
- `QPropertyNotifier addNotifier(Functor f)`
- `QUntypedPropertyBinding binding() const`
- `bool hasBinding() const`
- `(since 6.1) bool isReadOnly() const`
- `bool isValid() const`
- `QUntypedPropertyBinding makeBinding(const QPropertyBindingSourceLocation &location = QT_PROPERTY_DEFAULT_BINDING_LOCATION) const`
- `(since 6.2) QMetaType metaType() const`
- `QPropertyChangeHandler<Functor> onValueChanged(Functor f) const`
- `bool setBinding(const QUntypedPropertyBinding &binding)`
- `QPropertyChangeHandler<Functor> subscribe(Functor f) const`
- `(since 6.1) QUntypedPropertyBinding takeBinding()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[constexpr noexcept] QUntypedBindable::QUntypedBindable()`

**作用与语义：**

默认构造一个QUntypedBindable。它处于无效状态。

### `template <typename Property> QUntypedBindable::QUntypedBindable(Property *property)`

**作用与语义：**

从属性 `property` 构造 QUntypedBindable。如果 Property 是 const，则 QUntypedBindable 将为只读。`property`如果 为空，则 QUntypedBindable 无效。

### `template <typename Functor> QPropertyNotifier QUntypedBindable::addNotifier(Functor f)`

**作用与语义：**

安装`f`作为变更处理程序。每当基础属性发生变化，只要返回的`QPropertyNotifier`和属性保持存活，就会调用`f`。
在某些情况下，这种方法比`onValueChanged()`更容易使用，因为返回的对象不是模板。因此它可以更容易地存储，例如作为类中的成员。

### `QUntypedPropertyBinding QUntypedBindable::binding() const`

**作用与语义：**

如果有基础属性的绑定，返回;否则返回默认构造`QUntypedPropertyBinding`。

### `bool QUntypedBindable::hasBinding() const`

**作用与语义：**

如果标的属性具有约束力，回报`true`。

### `[since 6.1] bool QUntypedBindable::isReadOnly() const`

**作用与语义：**

如果`QUntypedBindable`是只读，则返回真。

### `bool QUntypedBindable::isValid() const`

**作用与语义：**

如果`QUntypedBindable`有效，则返回为真。调用无效`QUntypedBindable`的方法通常无效，除非另有说明。

### `QUntypedPropertyBinding QUntypedBindable::makeBinding(const QPropertyBindingSourceLocation &location = QT_PROPERTY_DEFAULT_BINDING_LOCATION) const`

**作用与语义：**

创建绑定，返回底层属性的值，使用指定的源`location`。

### `[since 6.2] QMetaType QUntypedBindable::metaType() const`

**作用与语义：**

返回创建`QUntypedBindable`的属性元类型。如果绑定对象无效，则返回一个无效元类型。

### `template <typename Functor> QPropertyChangeHandler<Functor> QUntypedBindable::onValueChanged(Functor f) const`

**作用与语义：**

安装`f`作为变更处理程序。每当底层属性发生变化，只要返回的`QPropertyChangeHandler`和属性保持活跃，就会调用`f`。每次值变更时，处理程序要么立即调用，要么延迟调用，具体取决于上下文。

### `bool QUntypedBindable::setBinding(const QUntypedPropertyBinding &binding)`

**作用与语义：**

将底层属性的绑定设置为`binding`。如果`QUntypedBindable`是只读、空，或者`binding`的类型与底层属性类型匹配，这不会有任何影响。
绑定成功设置后返回 `true`。

### `template <typename Functor> QPropertyChangeHandler<Functor> QUntypedBindable::subscribe(Functor f) const`

**作用与语义：**

表现得像是召唤`f`然后接着`onValueChanged(f)`，。

### `[since 6.1] QUntypedPropertyBinding QUntypedBindable::takeBinding()`

**作用与语义：**

移除当前设置的绑定并返回该属性。如果没有设置绑定，返回一个默认构造的`QUntypedPropertyBinding`。

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

`QUntypedBindable` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
