# QPropertyChangeHandler

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QPropertyChangeHandler<Functor>` 用对象生命周期控制 QProperty 变化回调：handler 存活时监听，析构或移动走后解除监听。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QPropertyChangeHandler<Functor>` 用对象生命周期控制 QProperty 变化回调：handler 存活时监听，析构或移动走后解除监听。

**内部模型：** `onValueChanged()` 返回的就是 handler。回调通常不带参数，需要主动读取属性当前值；`subscribe()` 与之类似，但会先立即调用一次回调。把返回值写成临时对象会在语句结束时立刻解除监听。

**适用场景：** 希望用 RAII 管理属性变化订阅，而不是手动 connect/disconnect 时使用。

**典型调用链：** 在属性上调用 onValueChanged/subscribe -> 把返回的 handler 保存为长期变量或成员 -> 回调中读取新值 -> 销毁 handler 自动取消。

**先记住的坑：** 最常见错误是没有保存返回值；回调捕获的对象必须比 handler 活得久；不要在回调中制造循环绑定或跨线程访问。

## 2. 依赖与对象关系

- 头文件：`#include <QPropertyChangeHandler>`
- 继承自：QPropertyObserver
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

`onValueChanged()` 返回的就是 handler。回调通常不带参数，需要主动读取属性当前值；`subscribe()` 与之类似，但会先立即调用一次回调。把返回值写成临时对象会在语句结束时立刻解除监听。

### 状态、生命周期和线程

**生命周期：** 绑定、通知器和 change handler 都必须活到你希望回调持续工作的时间。移动 handler 可以转移回调责任，销毁 handler 会解除监听；绑定表达式引用的对象必须比绑定更长寿。

**状态与结果：** 区分没有绑定、绑定有效、绑定被直接赋值打破、值发生变化和回调已解除。直接写入绑定属性往往会覆盖绑定关系，读取属性时要确认当前值是否来自预期依赖。

**线程与事件循环：** 属性绑定通常在创建它的线程计算，依赖对象的读写要遵守线程规则。不要让绑定表达式跨线程访问无锁共享状态，也不要在回调中修改会形成循环依赖的属性。

## 3. 直接使用

希望用 RAII 管理属性变化订阅，而不是手动 connect/disconnect 时使用。 使用时通常按这个过程组织：在属性上调用 onValueChanged/subscribe -> 把返回的 handler 保存为长期变量或成员 -> 回调中读取新值 -> 销毁 handler 自动取消。

```cpp
QProperty<int> count{0};
auto handler = count.onValueChanged([&count] {
    qInfo() << count.value();
});
count = 1; // handler 仍存活，因此执行回调
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 配套与继承 API

- `QPropertyChangeHandler<Functor>::QPropertyChangeHandler(Functor handler)`
- `QPropertyChangeHandler<Functor>::QPropertyChangeHandler(const Property &property, Functor handler)`
- `QPropertyChangeHandler<Functor> QProperty<T>::onValueChanged(Functor handler)`
- `QPropertyChangeHandler<Functor> QProperty<T>::subscribe(Functor handler)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QPropertyChangeHandler<Functor>::QPropertyChangeHandler(Functor handler)`

**作用与语义：**

保存无参数回调 `handler`，但这个重载本身没有指定要观察的属性。它主要供稍后关联属性的低层用法；常规代码应优先使用同时传入 `property` 的构造函数或 `addNotifier()`。

### `QPropertyChangeHandler<Functor>::QPropertyChangeHandler(const Property &property, Functor handler)`

**作用与语义：**

保存无参数回调 `handler` 并立即订阅 `property`；属性值变化时调用该回调。必须保存返回的 `QPropertyChangeHandler` 对象，它销毁后订阅会自动解除。

### `QPropertyChangeHandler<Functor> QProperty<T>::onValueChanged(Functor handler)`

**作用与语义：**

将给定函子`f`注册为回调，每当属性值变化时应调用。每次值变更时，处理程序要么立即调用，要么延迟调用，具体取决于上下文。
回调`f`预期是一个带有普通调用运算符()''的类型，没有任何参数。这意味着你可以提供C λ表达式、std：：函数，甚至带有调用运算符的自定义结构。
返回的属性变更处理对象负责跟踪注册情况。当它超出作用域时，回调会被取消注册。

### `QPropertyChangeHandler<Functor> QProperty<T>::subscribe(Functor handler)`

**作用与语义：**

将给定函子`f`作为回调，立即调用，且每当属性值未来变化时即可调用。每次值变更时，处理程序要么立即调用，要么延迟调用，具体取决于上下文。
回调`f`应是一个可复制的类型，并且有一个没有参数的普通调用操作符()。这意味着你可以提供一个 C λ 表达式、一个 std：：函数，甚至一个带有调用操作符的自定义结构。
返回的属性变更处理对象负责跟踪订阅情况。当订阅超出范围时，回调会被取消订阅。

## 6. 深入实践与常见坑

### 生命周期和资源边界

绑定、通知器和 change handler 都必须活到你希望回调持续工作的时间。移动 handler 可以转移回调责任，销毁 handler 会解除监听；绑定表达式引用的对象必须比绑定更长寿。

### 状态和错误边界

区分没有绑定、绑定有效、绑定被直接赋值打破、值发生变化和回调已解除。直接写入绑定属性往往会覆盖绑定关系，读取属性时要确认当前值是否来自预期依赖。

### 线程边界

属性绑定通常在创建它的线程计算，依赖对象的读写要遵守线程规则。不要让绑定表达式跨线程访问无锁共享状态，也不要在回调中修改会形成循环依赖的属性。

### 最容易出现的错误

最常见错误是没有保存返回值；回调捕获的对象必须比 handler 活得久；不要在回调中制造循环绑定或跨线程访问。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QPropertyChangeHandler` 所属机制类型：Qt 属性绑定机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
