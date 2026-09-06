# QProperty

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QProperty` 是 Qt 属性绑定体系中的类型，负责保存属性值、建立依赖关系或监听变化。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QProperty` 是 Qt 属性绑定机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt 的属性系统把当前值、依赖关系和变化通知分开。`QProperty` 可以保存值并建立绑定，绑定会记录读取过的依赖；依赖变化时重新计算。`QPropertyNotifier` 和 `QPropertyChangeHandler` 则用对象生命周期控制通知回调。

**适用场景：** 先定义属性及其默认值，再用绑定表达式连接依赖；用 notify/subscribe/onValueChanged 观察变化，保存返回的 handler 直到监听结束。需要一次性赋值时明确接受它会替换绑定。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要让绑定表达式产生副作用；不要立即销毁通知器；不要把绑定系统当线程同步工具；循环绑定、隐式转换和直接赋值都可能让结果与直觉不同。

## 2. 依赖与对象关系

- 头文件：`#include <QProperty>`
- 继承自：QPropertyData
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

Qt 的属性系统把当前值、依赖关系和变化通知分开。`QProperty` 可以保存值并建立绑定，绑定会记录读取过的依赖；依赖变化时重新计算。`QPropertyNotifier` 和 `QPropertyChangeHandler` 则用对象生命周期控制通知回调。

### 状态、生命周期和线程

**生命周期：** 绑定、通知器和 change handler 都必须活到你希望回调持续工作的时间。移动 handler 可以转移回调责任，销毁 handler 会解除监听；绑定表达式引用的对象必须比绑定更长寿。

**状态与结果：** 区分没有绑定、绑定有效、绑定被直接赋值打破、值发生变化和回调已解除。直接写入绑定属性往往会覆盖绑定关系，读取属性时要确认当前值是否来自预期依赖。

**线程与事件循环：** 属性绑定通常在创建它的线程计算，依赖对象的读写要遵守线程规则。不要让绑定表达式跨线程访问无锁共享状态，也不要在回调中修改会形成循环依赖的属性。

## 3. 直接使用

先定义属性及其默认值，再用绑定表达式连接依赖；用 notify/subscribe/onValueChanged 观察变化，保存返回的 handler 直到监听结束。需要一次性赋值时明确接受它会替换绑定。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

```cpp
QProperty<int> source{1};
QProperty<int> result{[&source] { return source.value() * 2; }};
auto notifier = result.onValueChanged([] {
    // 依赖变化后执行轻量通知逻辑
});
source = 2; // result 会重新计算
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QProperty()`
- `QProperty(Functor &&f)`
- `QProperty(T &&initialValue)`
- `QProperty(const QPropertyBinding<T> &binding)`
- `QProperty(const T &initialValue)`
- `~QProperty()`
- `(since 6.2) QPropertyNotifier addNotifier(Functor f)`
- `QPropertyBinding<T> binding() const`
- `QPropertyChangeHandler<Functor> onValueChanged(Functor f)`
- `QPropertyBinding<T> setBinding(const QPropertyBinding<T> &newBinding)`
- `(since 6.0) QPropertyBinding<T> setBinding(Functor f)`
- `bool setBinding(const QUntypedPropertyBinding &newBinding)`
- `void setValue(QProperty<T>::parameter_type newValue)`
- `void setValue(QProperty<T>::rvalue_ref newValue)`
- `(since 6.0) QPropertyChangeHandler<Functor> subscribe(Functor f)`
- `QPropertyBinding<T> takeBinding()`
- `QProperty<T>::parameter_type value() const`
- `QProperty<T> & operator=(QProperty<T>::parameter_type newValue)`
- `QProperty<T> & operator=(QProperty<T>::rvalue_ref newValue)`

### 相关非成员函数

- `(since 6.2) void beginPropertyUpdateGroup()`
- `(since 6.2) void endPropertyUpdateGroup()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QProperty::QProperty()`

**作用与语义：**

构造一个带有默认构造实例T的属性。

### `[explicit] template <typename Functor> QProperty::QProperty(Functor &&f)`

**作用与语义：**

构造一个与所给绑定表达式绑定的属性`f`。该属性的值被设置为评估新绑定的结果。每当绑定的依赖发生变化时，绑定将被重新评估，属性值也会相应更新。

### `[explicit default] QProperty::QProperty(T &&initialValue)`

**作用与语义：**

用提供的 Move-Constructs 一个属性`initialValue`。

### `[explicit] QProperty::QProperty(const QPropertyBinding<T> &binding)`

**作用与语义：**

构造一个与所提供`binding`表达式绑定的属性。该属性的值被设置为评估新绑定的结果。每当绑定的依赖发生变化时，绑定将被重新评估，属性值也会相应更新。

### `[explicit default] QProperty::QProperty(const T &initialValue)`

**作用与语义：**

用提供的`initialValue`构造一个物业。

### `QProperty::~QProperty()`

**作用与语义：**

毁坏了属性。

### `[since 6.2] template <typename Functor> QPropertyNotifier QProperty::addNotifier(Functor f)`

**作用与语义：**

将给定函子`f`作为回调，每当该属性的值发生变化时调用。
回调`f`应是一个类型，带有一个普通调用运算符()''，没有任何参数。这意味着你可以提供C lambda表达式、std：：函数，甚至带有调用运算符的自定义结构体。
返回的属性变更处理对象负责跟踪订阅情况。当订阅超出范围时，回调会被取消订阅。
在某些情况下，这种方法比 `onValueChanged()` 更易使用，因为返回的对象不是模板。因此它可以更容易存储，例如作为类中的成员。

### `QPropertyBinding<T> QProperty::binding() const`

**作用与语义：**

返回与该属性相关的绑定表达式。<T>如果不存在此类关联，将返回默认构造的QPropertyBinding。

### `template <typename Functor> QPropertyChangeHandler<Functor> QProperty::onValueChanged(Functor f)`

**作用与语义：**

将给定函子`f`注册为回调，每当属性值变化时应调用。每次值变更时，处理程序要么立即调用，要么延迟调用，具体取决于上下文。
回调`f`预期是一个带有普通调用运算符()''的类型，没有任何参数。这意味着你可以提供C λ表达式、std：：函数，甚至带有调用运算符的自定义结构。
返回的属性变更处理对象负责跟踪注册情况。当它超出作用域时，回调会被取消注册。

### `QPropertyBinding<T> QProperty::setBinding(const QPropertyBinding<T> &newBinding)`

**作用与语义：**

将该属性的值与提供的`newBinding`表达式关联，并返回之前关联的绑定。该属性的值被设置为新绑定的结果。每当绑定的依赖发生变化时，绑定将被重新评估，属性值相应更新。

### `[since 6.0] template <typename Functor> QPropertyBinding<T> QProperty::setBinding(Functor f)`

**作用与语义：**

将该属性的值与所提供的函子 `f` 关联，并返回之前关联的绑定。该属性的值被设置为评估新绑定的结果。每当绑定的依赖发生变化时，绑定将被重新评估，属性的值也会相应更新。

### `bool QProperty::setBinding(const QUntypedPropertyBinding &newBinding)`

**作用与语义：**

将该属性的值与提供的`newBinding`表达式关联起来。该属性的值被设置为评估新绑定的结果。每当绑定的依赖发生变化时，绑定会被重新评估，属性的值也会相应更新。
如果该属性的类型与绑定函数返回的类型相同，则返回真;否则返回为假。

### `void QProperty::setValue(QProperty<T>::parameter_type newValue)`

**作用与语义：**

将`newValue`赋入该属性，并移除该属性相关的绑定（如存在）。

### `[since 6.0] template <typename Functor> QPropertyChangeHandler<Functor> QProperty::subscribe(Functor f)`

**作用与语义：**

将给定函子`f`作为回调，立即调用，且每当属性值未来变化时即可调用。每次值变更时，处理程序要么立即调用，要么延迟调用，具体取决于上下文。
回调`f`应是一个可复制的类型，并且有一个没有参数的普通调用操作符()。这意味着你可以提供一个 C λ 表达式、一个 std：：函数，甚至一个带有调用操作符的自定义结构。
返回的属性变更处理对象负责跟踪订阅情况。当订阅超出范围时，回调会被取消订阅。

### `QPropertyBinding<T> QProperty::takeBinding()`

**作用与语义：**

将绑定表达式与该属性分离并返回。调用该函数后，只有当你赋予它新的值或设置新的绑定时，属性的值才会发生变化。

### `QProperty<T>::parameter_type QProperty::value() const`

**作用与语义：**

返回该属性的值。这可能会在返回值之前，评估与该属性相关的绑定表达式。

### `QProperty<T> &QProperty::operator=(QProperty<T>::parameter_type newValue)`

**作用与语义：**

将`newValue`赋予该属性，并返回该`QProperty`的引用。

### `[since 6.2] void beginPropertyUpdateGroup()`

**作用与语义：**

标志着属性更新组的开始。在该组内，更改属性既不会立即更新任何依赖属性，也不会触发变更通知。这些通知会被推迟，直到通过调用`endPropertyUpdateGroup`结束该组。
群可以嵌套。在这种情况下，延迟只有在最外层的组结束后才结束。
注意：只有在所有受影响的属性值都更新为新值后，才会发送变更通知。这允许在需要更新多个属性时重新建立类不变量，防止任何外部观察者察觉到状态不一致。

### `[since 6.2] void endPropertyUpdateGroup()`

**作用与语义：**

结束属性更新组。如果最外层组已经结束，延迟绑定的评估和通知现在就会发生。
警告：未先调用 `beginPropertyUpdateGroup` 的 endPropertyUpdateGroup 会导致行为未定义。

### `void setValue(QProperty<T>::rvalue_ref newValue)`

**作用与语义：**

将`newValue`赋入该属性，并移除该属性相关的绑定（如存在）。

### `QProperty<T> & operator=(QProperty<T>::rvalue_ref newValue)`

**作用与语义：**

将`newValue`赋予该属性，并返回该`QProperty`的引用。

## 6. 深入实践与常见坑

### 生命周期和资源边界

绑定、通知器和 change handler 都必须活到你希望回调持续工作的时间。移动 handler 可以转移回调责任，销毁 handler 会解除监听；绑定表达式引用的对象必须比绑定更长寿。

### 状态和错误边界

区分没有绑定、绑定有效、绑定被直接赋值打破、值发生变化和回调已解除。直接写入绑定属性往往会覆盖绑定关系，读取属性时要确认当前值是否来自预期依赖。

### 线程边界

属性绑定通常在创建它的线程计算，依赖对象的读写要遵守线程规则。不要让绑定表达式跨线程访问无锁共享状态，也不要在回调中修改会形成循环依赖的属性。

### 最容易出现的错误

不要让绑定表达式产生副作用；不要立即销毁通知器；不要把绑定系统当线程同步工具；循环绑定、隐式转换和直接赋值都可能让结果与直觉不同。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QProperty` 所属机制类型：Qt 属性绑定机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
