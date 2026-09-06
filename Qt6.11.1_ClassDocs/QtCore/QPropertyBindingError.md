# QPropertyBindingError

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QPropertyBindingError` 是 Qt 属性绑定体系中的类型，负责保存属性值、建立依赖关系或监听变化。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QPropertyBindingError` 是 Qt 属性绑定机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt 的属性系统把当前值、依赖关系和变化通知分开。`QProperty` 可以保存值并建立绑定，绑定会记录读取过的依赖；依赖变化时重新计算。`QPropertyNotifier` 和 `QPropertyChangeHandler` 则用对象生命周期控制通知回调。

**适用场景：** 先定义属性及其默认值，再用绑定表达式连接依赖；用 notify/subscribe/onValueChanged 观察变化，保存返回的 handler 直到监听结束。需要一次性赋值时明确接受它会替换绑定。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要让绑定表达式产生副作用；不要立即销毁通知器；不要把绑定系统当线程同步工具；循环绑定、隐式转换和直接赋值都可能让结果与直觉不同。

## 2. 依赖与对象关系

- 头文件：`#include <QPropertyBindingError>`
- 继承自：未在类页中列出
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

### 公有类型

- `enum Type { NoError, BindingLoop, EvaluationError, UnknownError }`

### 公有函数

- `QPropertyBindingError()`
- `QPropertyBindingError(QPropertyBindingError::Type type, const QString &description = QString())`
- `QPropertyBindingError(const QPropertyBindingError &other)`
- `QPropertyBindingError(QPropertyBindingError &&other)`
- `~QPropertyBindingError()`
- `QString description() const`
- `QPropertyBindingError::Type type() const`
- `QPropertyBindingError & operator=(QPropertyBindingError &&other)`
- `QPropertyBindingError & operator=(const QPropertyBindingError &other)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QPropertyBindingError::Type`

**作用与语义：**

该枚举具体说明了发生了哪些错误。
- `QPropertyBindingError::NoError`：`0`;在评估绑定过程中未发生错误。
- `QPropertyBindingError::BindingLoop`：`1`;约束性评估被停止，因为属性依赖于其自身价值。
- `QPropertyBindingError::EvaluationError`：`2`;绑定评估被停止的原因不是绑定环。例如，当QML引擎在评估绑定时发生异常时，会使用该值。
- `QPropertyBindingError::UnknownError`：`3`;当其他两个值都不适用时使用的通用错误类型。调用`description()`可能提供详细信息。

### `QPropertyBindingError::QPropertyBindingError()`

**作用与语义：**

默认构造为 QPropertyBindingError。hasError() 返回 false，类型返回 `NoError`，`description()` 返回空字符串。

### `QPropertyBindingError::QPropertyBindingError(QPropertyBindingError::Type type, const QString &description = QString())`

**作用与语义：**

构造一个类型为`type`的QPropertyBindingError，描述为`description`。

### `QPropertyBindingError::QPropertyBindingError(const QPropertyBindingError &other)`

**作用与语义：**

从 `other` 复制构造 QPropertyBindingError。

### `QPropertyBindingError::QPropertyBindingError(QPropertyBindingError &&other)`

**作用与语义：**

Move-构造 QPropertyBindingError，从`other`。`other` 将保持默认状态。

### `[noexcept] QPropertyBindingError::~QPropertyBindingError()`

**作用与语义：**

摧毁了`QPropertyBindingError`。

### `QString QPropertyBindingError::description() const`

**作用与语义：**

如果`QPropertyBindingError`已被设置，会返回描述性错误信息。

### `QPropertyBindingError::Type QPropertyBindingError::type() const`

**作用与语义：**

返回`QPropertyBindingError`类型。

### `QPropertyBindingError &QPropertyBindingError::operator=(QPropertyBindingError &&other)`

**作用与语义：**

Move-assign `other`到这个`QPropertyBindingError`。`other`会保持默认状态。

### `QPropertyBindingError &QPropertyBindingError::operator=(const QPropertyBindingError &other)`

**作用与语义：**

本`QPropertyBindingError` `other`副本。

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

`QPropertyBindingError` 所属机制类型：Qt 属性绑定机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
