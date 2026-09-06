# QObjectBindableProperty

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“对象BindableProperty”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QObjectBindableProperty` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QObjectBindableProperty>`
- 继承自：QPropertyData
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

- `QObjectBindableProperty()`
- `QObjectBindableProperty(Functor &&f)`
- `QObjectBindableProperty(T &&initialValue)`
- `QObjectBindableProperty(const T &initialValue)`
- `QObjectBindableProperty(Class *owner, QPropertyBinding<T> &&binding)`
- `QObjectBindableProperty(Class *owner, const QPropertyBinding<T> &binding)`
- `~QObjectBindableProperty()`
- `QPropertyNotifier addNotifier(Functor f)`
- `QPropertyBinding<T> binding() const`
- `bool hasBinding() const`
- `void notify()`
- `QPropertyChangeHandler<Functor> onValueChanged(Functor f)`
- `QPropertyBinding<T> setBinding(const QPropertyBinding<T> &newBinding)`
- `QPropertyBinding<T> setBinding(Functor f)`
- `bool setBinding(const QUntypedPropertyBinding &newBinding)`
- `void setValue(QObjectBindableProperty<Class, T, Offset, Signal>::parameter_type newValue)`
- `void setValue(QObjectBindableProperty<Class, T, Offset, Signal>::rvalue_ref newValue)`
- `QPropertyChangeHandler<Functor> subscribe(Functor f)`
- `QPropertyBinding<T> takeBinding()`
- `QObjectBindableProperty<Class, T, Offset, Signal>::parameter_type value() const`

### 公开宏

- `(since 6.0) Q_OBJECT_BINDABLE_PROPERTY(containingClass, type, name, signal)`
- `(since 6.0) Q_OBJECT_BINDABLE_PROPERTY_WITH_ARGS(containingClass, type, name, initialvalue, signal)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QObjectBindableProperty::QObjectBindableProperty()`

**作用与语义：**

构造一个带有默认构造实例T的属性。

### `[explicit] template <typename Functor> QObjectBindableProperty::QObjectBindableProperty(Functor &&f)`

**作用与语义：**

构造一个与所给绑定表达式绑定的属性`f`。该属性的值被设置为评估新绑定的结果。每当绑定的依赖发生变化时，绑定将被重新评估，属性值也会相应更新。

### `[explicit] QObjectBindableProperty::QObjectBindableProperty(T &&initialValue)`

**作用与语义：**

用提供的 Move-Constructs 一个属性`initialValue`。

### `[explicit] QObjectBindableProperty::QObjectBindableProperty(const T &initialValue)`

**作用与语义：**

用提供的`initialValue`构造一个物业。

### `[default] QObjectBindableProperty::QObjectBindableProperty(Class *owner, QPropertyBinding<T> &&binding)`

**作用与语义：**

构造一个与所给`binding`表达式绑定的属性。该属性的值被设置为评估新绑定的结果。每当绑定的依赖发生变化时，绑定将被重新评估，属性值也会相应更新。
当属性值发生变化时，`owner`会通过回调函数通知。

### `[default] QObjectBindableProperty::QObjectBindableProperty(Class *owner, const QPropertyBinding<T> &binding)`

**作用与语义：**

构造一个与所给`binding`表达式绑定的属性。该属性的值被设置为评估新绑定的结果。每当绑定的依赖发生变化时，绑定将被重新评估，属性值也会相应更新。
当属性值发生变化时，`owner`会通过回调函数通知。

### `[default] QObjectBindableProperty::~QObjectBindableProperty()`

**作用与语义：**

毁坏了属性。

### `template <typename Functor> QPropertyNotifier QObjectBindableProperty::addNotifier(Functor f)`

**作用与语义：**

将给定函子`f`作为回调，每当该属性的值发生变化时调用。
回调`f`应是一个类型，带有一个普通调用运算符()''，没有任何参数。这意味着你可以提供C lambda表达式、std：：函数，甚至带有调用运算符的自定义结构体。
返回的属性变更处理对象负责跟踪订阅情况。当订阅超出范围时，回调会被取消订阅。
在某些情况下，这种方法比 `onValueChanged()` 更易使用，因为返回的对象不是模板。因此它可以更容易存储，例如作为类中的成员。

### `QPropertyBinding<T> QObjectBindableProperty::binding() const`

**作用与语义：**

返回与该属性相关的绑定表达式。<T>如果不存在此类关联，将返回默认构造的QPropertyBinding。

### `bool QObjectBindableProperty::hasBinding() const`

**作用与语义：**

如果该属性与绑定相关，则返回真;否则返回为假。

### `void QObjectBindableProperty::notify()`

**作用与语义：**

程序化地表示属性的变化。任何依赖该属性的绑定都会被通知，如果属性有信号，则会被发出。
这与 setValueBypassingBindings 结合使用时非常有用，可以推迟到类不变恢复后才发出变更信号。
注意：如果该属性具有绑定（即`hasBinding()`返回为真），当调用notify()时该绑定不会被重新评估。任何依赖该属性的绑定仍会像往常一样重新评估。

### `template <typename Functor> QPropertyChangeHandler<Functor> QObjectBindableProperty::onValueChanged(Functor f)`

**作用与语义：**

将给定函子`f`注册为回调，每当属性值变化时应调用。每次值变更时，处理程序要么立即调用，要么延迟调用，具体取决于上下文。
回调`f`预期是一个带有普通调用运算符()''的类型，没有任何参数。这意味着你可以提供C λ表达式、std：：函数，甚至带有调用运算符的自定义结构。
返回的属性变更处理对象负责跟踪注册情况。当它超出作用域时，回调会被取消注册。

### `QPropertyBinding<T> QObjectBindableProperty::setBinding(const QPropertyBinding<T> &newBinding)`

**作用与语义：**

将该属性的值与提供的`newBinding`表达式关联，并返回之前关联的绑定。该属性的值被设置为评估新绑定的结果。每当绑定的依赖发生变化，绑定将被重新评估，属性值相应更新。当属性值发生变化时，所有者通过回调函数收到通知。

### `template <typename Functor> QPropertyBinding<T> QObjectBindableProperty::setBinding(Functor f)`

**作用与语义：**

将该属性的值与所提供的函子 `f` 关联，并返回之前关联的绑定。该属性的值被设置为通过调用运算符 ()'` of `f' 计算新绑定的结果。每当绑定的依赖发生变化时，绑定将被重新评估，属性值相应更新。
当房产价值发生变化时，业主会通过回调函数收到通知。

### `bool QObjectBindableProperty::setBinding(const QUntypedPropertyBinding &newBinding)`

**作用与语义：**

将该属性的值与提供的`newBinding`表达式关联起来。属性的值被设置为评估新绑定的结果。每当绑定的依赖发生变化时，绑定会被重新评估，属性的值也会相应更新。
返回 `true` 如果该属性的类型与绑定函数返回的类型相同;否则`false`。

### `void QObjectBindableProperty::setValue(QObjectBindableProperty<Class, T, Offset, Signal>::rvalue_ref newValue)`

**作用与语义：**

将`newValue`赋入该属性，并移除该属性相关的绑定（如存在）。如果属性值因此发生变化，则调用回调函数`owner`。

### `template <typename Functor> QPropertyChangeHandler<Functor> QObjectBindableProperty::subscribe(Functor f)`

**作用与语义：**

将给定函子`f`作为回调，立即调用，且每当属性值未来发生变化时。每次值变更时，处理程序要么立即调用，要么延迟调用，具体取决于上下文。
回调`f`预期是一个类型，带有一个普通调用运算符()''，没有任何参数。这意味着你可以提供一个C λ表达式、一个std：：函数，甚至一个带有调用运算符的自定义结构体。
返回的属性变更处理对象负责跟踪订阅情况。当订阅超出范围时，回调会被取消订阅。

### `QPropertyBinding<T> QObjectBindableProperty::takeBinding()`

**作用与语义：**

将绑定表达式与该属性分离并返回。调用该函数后，只有当你赋予它新的值或设置新的绑定时，属性的值才会发生变化。

### `QObjectBindableProperty<Class, T, Offset, Signal>::parameter_type QObjectBindableProperty::value() const`

**作用与语义：**

返回该属性的值。这可能会在返回值之前，评估与该属性相关的绑定表达式。

### `[since 6.0] Q_OBJECT_BINDABLE_PROPERTY(containingClass, type, name, signal)`

**作用与语义：**

在类型为`type`的`containingClass`中声明一个名为`name`的`QObjectBindableProperty`。如果给出可选参数`signal`，当该属性被标记为脏时，该信号将被发出。
该宏在Qt 6.0中引入。

### `[since 6.0] Q_OBJECT_BINDABLE_PROPERTY_WITH_ARGS(containingClass, type, name, initialvalue, signal)`

**作用与语义：**

在类型为`type`的`containingClass`中声明一个`QObjectBindableProperty`，名为`name`，初始化为`initialvalue`。如果给出可选参数`signal`，当该属性被标记为脏时，该信号将被发射。
该宏在Qt 6.0中引入。

### `void setValue(QObjectBindableProperty<Class, T, Offset, Signal>::parameter_type newValue)`

**作用与语义：**

将`newValue`赋入该属性，并移除该属性相关的绑定（如存在）。如果属性值因此发生变化，则调用回调函数`owner`。

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

`QObjectBindableProperty` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
