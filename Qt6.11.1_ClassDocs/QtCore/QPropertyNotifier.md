# QPropertyNotifier

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QPropertyNotifier` 是类型擦除的属性变化监听器，用 RAII 保存一个无参数回调及其属性来源。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QPropertyNotifier` 是类型擦除的属性变化监听器，用 RAII 保存一个无参数回调及其属性来源。

**内部模型：** 它和模板化的 QPropertyChangeHandler 作用相近，但回调存入 std::function。可先构造回调再绑定 source，也可由 `QProperty::addNotifier()` 创建；对象销毁时自动停止监听。

**适用场景：** 需要把不同回调类型放入同一成员、容器或非模板接口时使用。

**典型调用链：** 构造 notifier/调用 addNotifier -> 绑定属性来源 -> 保存 notifier -> 属性变化时执行回调 -> 析构自动解除。

**先记住的坑：** 不要丢弃临时 notifier；回调必须可无参数调用；捕获对象的生命周期和线程必须安全。

## 2. 依赖与对象关系

- 头文件：`#include <QPropertyNotifier>`
- 继承自：QPropertyObserver
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

它和模板化的 QPropertyChangeHandler 作用相近，但回调存入 std::function。可先构造回调再绑定 source，也可由 `QProperty::addNotifier()` 创建；对象销毁时自动停止监听。

### 状态、生命周期和线程

**生命周期：** 绑定、通知器和 change handler 都必须活到你希望回调持续工作的时间。移动 handler 可以转移回调责任，销毁 handler 会解除监听；绑定表达式引用的对象必须比绑定更长寿。

**状态与结果：** 区分没有绑定、绑定有效、绑定被直接赋值打破、值发生变化和回调已解除。直接写入绑定属性往往会覆盖绑定关系，读取属性时要确认当前值是否来自预期依赖。

**线程与事件循环：** 属性绑定通常在创建它的线程计算，依赖对象的读写要遵守线程规则。不要让绑定表达式跨线程访问无锁共享状态，也不要在回调中修改会形成循环依赖的属性。

## 3. 直接使用

需要把不同回调类型放入同一成员、容器或非模板接口时使用。 使用时通常按这个过程组织：构造 notifier/调用 addNotifier -> 绑定属性来源 -> 保存 notifier -> 属性变化时执行回调 -> 析构自动解除。

```cpp
QProperty<int> count{0};
QPropertyNotifier notifier = count.addNotifier([&count] {
    qInfo() << count.value();
});
count = 1;
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 配套与继承 API

- `QPropertyNotifier::QPropertyNotifier()`
- `QPropertyNotifier::QPropertyNotifier(Functor handler)`
- `QPropertyNotifier::QPropertyNotifier(const Property &property, Functor handler)`
- `QPropertyNotifier QProperty<T>::addNotifier(Functor handler)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QPropertyNotifier::QPropertyNotifier()`

**作用与语义：**

构造一个尚未关联属性、也没有回调的通知器；在设置有效来源和处理函数前，属性变化不会触发任何操作。

### `QPropertyNotifier::QPropertyNotifier(Functor handler)`

**作用与语义：**

保存无参数回调 `handler`，但这个重载本身没有指定要观察的属性。它主要供稍后关联属性的低层用法；常规代码应优先使用同时传入 `property` 的构造函数或 `addNotifier()`。

### `QPropertyNotifier::QPropertyNotifier(const Property &property, Functor handler)`

**作用与语义：**

保存无参数回调 `handler` 并立即订阅 `property`；属性值变化时调用该回调。必须保存返回的 `QPropertyNotifier` 对象，它销毁后订阅会自动解除。

### `QPropertyNotifier QProperty<T>::addNotifier(Functor handler)`

**作用与语义：**

将给定函子`f`作为回调，每当该属性的值发生变化时调用。
回调`f`应是一个类型，带有一个普通调用运算符()''，没有任何参数。这意味着你可以提供C lambda表达式、std：：函数，甚至带有调用运算符的自定义结构体。
返回的属性变更处理对象负责跟踪订阅情况。当订阅超出范围时，回调会被取消订阅。
在某些情况下，这种方法比 `onValueChanged()` 更易使用，因为返回的对象不是模板。因此它可以更容易存储，例如作为类中的成员。

## 6. 深入实践与常见坑

### 生命周期和资源边界

绑定、通知器和 change handler 都必须活到你希望回调持续工作的时间。移动 handler 可以转移回调责任，销毁 handler 会解除监听；绑定表达式引用的对象必须比绑定更长寿。

### 状态和错误边界

区分没有绑定、绑定有效、绑定被直接赋值打破、值发生变化和回调已解除。直接写入绑定属性往往会覆盖绑定关系，读取属性时要确认当前值是否来自预期依赖。

### 线程边界

属性绑定通常在创建它的线程计算，依赖对象的读写要遵守线程规则。不要让绑定表达式跨线程访问无锁共享状态，也不要在回调中修改会形成循环依赖的属性。

### 最容易出现的错误

不要丢弃临时 notifier；回调必须可无参数调用；捕获对象的生命周期和线程必须安全。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QPropertyNotifier` 所属机制类型：Qt 属性绑定机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
