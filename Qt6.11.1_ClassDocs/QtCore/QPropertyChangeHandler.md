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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 4 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QPropertyChangeHandler<Functor>::QPropertyChangeHandler(Functor handler)`

**API 类别：** 配套与继承 API

**中文解读：** `QPropertyChangeHandler` 用于创建或取得属性变化监听器。必须把返回的 handler/notifier 保存到足够长的作用域；对象析构会自动解除监听，回调通常应重新读取属性当前值。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `handler`：类型为 `Functor`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPropertyChangeHandler<Functor>::QPropertyChangeHandler(const Property &property, Functor handler)`

**API 类别：** 配套与继承 API

**中文解读：** `QPropertyChangeHandler` 用于创建或取得属性变化监听器。必须把返回的 handler/notifier 保存到足够长的作用域；对象析构会自动解除监听，回调通常应重新读取属性当前值。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `property`：类型为 `const Property &`。没有默认值，调用时必须提供。传入 `const Property &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `handler`：类型为 `Functor`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPropertyChangeHandler<Functor> QProperty<T>::onValueChanged(Functor handler)`

**API 类别：** 配套与继承 API

**中文解读：** `onValueChanged` 用于创建或取得属性变化监听器。必须把返回的 handler/notifier 保存到足够长的作用域；对象析构会自动解除监听，回调通常应重新读取属性当前值。

**签名拆解：**

- 返回值：`QPropertyChangeHandler<Functor> QProperty<T>::`。
- 参数 `handler`：类型为 `Functor`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPropertyChangeHandler<Functor> QProperty<T>::subscribe(Functor handler)`

**API 类别：** 配套与继承 API

**中文解读：** `subscribe` 用于创建或取得属性变化监听器。必须把返回的 handler/notifier 保存到足够长的作用域；对象析构会自动解除监听，回调通常应重新读取属性当前值。

**签名拆解：**

- 返回值：`QPropertyChangeHandler<Functor> QProperty<T>::`。
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

最常见错误是没有保存返回值；回调捕获的对象必须比 handler 活得久；不要在回调中制造循环绑定或跨线程访问。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QPropertyChangeHandler` 所属机制类型：Qt 属性绑定机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
