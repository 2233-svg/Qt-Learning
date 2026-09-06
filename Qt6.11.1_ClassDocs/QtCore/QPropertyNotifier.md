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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 4 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QPropertyNotifier::QPropertyNotifier()`

**API 类别：** 配套与继承 API

**中文解读：** `QPropertyNotifier` 用于创建或取得属性变化监听器。必须把返回的 handler/notifier 保存到足够长的作用域；对象析构会自动解除监听，回调通常应重新读取属性当前值。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPropertyNotifier::QPropertyNotifier(Functor handler)`

**API 类别：** 配套与继承 API

**中文解读：** `QPropertyNotifier` 用于创建或取得属性变化监听器。必须把返回的 handler/notifier 保存到足够长的作用域；对象析构会自动解除监听，回调通常应重新读取属性当前值。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `handler`：类型为 `Functor`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPropertyNotifier::QPropertyNotifier(const Property &property, Functor handler)`

**API 类别：** 配套与继承 API

**中文解读：** `QPropertyNotifier` 用于创建或取得属性变化监听器。必须把返回的 handler/notifier 保存到足够长的作用域；对象析构会自动解除监听，回调通常应重新读取属性当前值。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `property`：类型为 `const Property &`。没有默认值，调用时必须提供。传入 `const Property &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `handler`：类型为 `Functor`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPropertyNotifier QProperty<T>::addNotifier(Functor handler)`

**API 类别：** 配套与继承 API

**中文解读：** `addNotifier` 用于创建或取得属性变化监听器。必须把返回的 handler/notifier 保存到足够长的作用域；对象析构会自动解除监听，回调通常应重新读取属性当前值。

**签名拆解：**

- 返回值：`QPropertyNotifier QProperty<T>::`。
- 参数 `handler`：类型为 `Functor`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
