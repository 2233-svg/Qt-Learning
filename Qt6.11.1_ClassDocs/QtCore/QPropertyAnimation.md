# QPropertyAnimation

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QPropertyAnimation` 是 Qt 属性绑定体系中的类型，负责保存属性值、建立依赖关系或监听变化。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QPropertyAnimation` 是动画框架中的类型，描述时间、状态、插值或动画组装行为。

**内部模型：** 动画通常由时间轴驱动属性变化；先确认动画对象、目标属性、持续时间和停止后的最终值，再组合 easing、loop 和 group。

**适用场景：** 界面过渡、状态变化和可视反馈需要平滑变化时使用。

**典型调用链：** 创建目标 -> 配置 duration/easing/start/end -> connect state/finished -> start/pause/stop -> 管理动画对象生命周期。

**先记住的坑：** 动画对象销毁会立即停止；重复 start 可能重置进度；不要用动画替代业务状态；跨线程动画通常不是正确方向。

## 2. 依赖与对象关系

- 头文件：`#include <QPropertyAnimation>`
- 继承自：QVariantAnimation
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

动画通常由时间轴驱动属性变化；先确认动画对象、目标属性、持续时间和停止后的最终值，再组合 easing、loop 和 group。

### 状态、生命周期和线程

**生命周期：** 绑定、通知器和 change handler 都必须活到你希望回调持续工作的时间。移动 handler 可以转移回调责任，销毁 handler 会解除监听；绑定表达式引用的对象必须比绑定更长寿。

**状态与结果：** 区分没有绑定、绑定有效、绑定被直接赋值打破、值发生变化和回调已解除。直接写入绑定属性往往会覆盖绑定关系，读取属性时要确认当前值是否来自预期依赖。

**线程与事件循环：** 属性绑定通常在创建它的线程计算，依赖对象的读写要遵守线程规则。不要让绑定表达式跨线程访问无锁共享状态，也不要在回调中修改会形成循环依赖的属性。

## 3. 直接使用

界面过渡、状态变化和可视反馈需要平滑变化时使用。 使用时通常按这个过程组织：创建目标 -> 配置 duration/easing/start/end -> connect state/finished -> start/pause/stop -> 管理动画对象生命周期。

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

### 属性

- `propertyName : QByteArray`
- `targetObject : QObject*`

### 公有函数

- `QPropertyAnimation(QObject *parent = nullptr)`
- `QPropertyAnimation(QObject *target, const QByteArray &propertyName, QObject *parent = nullptr)`
- `virtual ~QPropertyAnimation()`
- `QBindable<QByteArray> bindablePropertyName()`
- `QBindable<QObject *> bindableTargetObject()`
- `QByteArray propertyName() const`
- `void setPropertyName(const QByteArray &propertyName)`
- `void setTargetObject(QObject *target)`
- `QObject * targetObject() const`

### 重实现的保护函数

- `virtual bool event(QEvent *event) override`
- `virtual void updateCurrentValue(const QVariant &value) override`
- `virtual void updateState(QAbstractAnimation::State newState, QAbstractAnimation::State oldState) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[bindable] propertyName : QByteArray`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含了该动画的目标属性名称。
该属性定义了该动画的目标属性名称。该属性名称是动画运行所必需的。

**如何使用：** 调用 `propertyName()` 读取当前值；它不会修改应用状态。

### `[bindable] targetObject : QObject*`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含了该动画的目标`QObject`。
该属性定义了该动画的目标`QObject`。

**如何使用：** 调用 `targetObject()` 读取当前值；它不会修改应用状态。

### `QPropertyAnimation::QPropertyAnimation(QObject *parent = nullptr)`

**作用与语义：**

构造一个QPropertyAnimation对象。`parent`传递给`QObject`的构造器。

### `QPropertyAnimation::QPropertyAnimation(QObject *target, const QByteArray &propertyName, QObject *parent = nullptr)`

**作用与语义：**

构造一个QPropertyAnimation对象。`parent`传递给`QObject`的构造器。动画会改变`target`上的属性`propertyName`。默认持续时间为250毫秒。

### `[virtual noexcept] QPropertyAnimation::~QPropertyAnimation()`

**作用与语义：**

会摧毁`QPropertyAnimation`实例。

### `[override virtual protected] bool QPropertyAnimation::event(QEvent *event)`

**作用与语义：**

重实现自：`QVariantAnimation::event`（QEvent *事件）。

### `[override virtual protected] void QPropertyAnimation::updateCurrentValue(const QVariant &value)`

**作用与语义：**

重装：`QVariantAnimation::updateCurrentValue`（const QVariant & value）。
每当当前值发生变化时，`QVariantAnimation`都会调用这个虚拟函数。`value` 是新的、更新后的值。它会更新目标对象属性的当前值，除非动画停止。
每次动画当前值变化时，都会调用这个虚拟函数。`value`参数是新的当前值。
基础类实现什么都不做。

### `[override virtual protected] void QPropertyAnimation::updateState(QAbstractAnimation::State newState, QAbstractAnimation::State oldState)`

**作用与语义：**

重实现自：`QVariantAnimation::updateState`（QAbstractAnimation：：State newState， QAbstractAnimation：：State oldState）。
如果动画状态从停止变为运行时未定义`startValue`，则使用当前属性值作为动画的初始值。

### `QBindable<QByteArray> bindablePropertyName()`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含了该动画的目标属性名称。
该属性定义了该动画的目标属性名称。该属性名称是动画运行所必需的。

**如何使用：** 调用 `bindablePropertyName()` 取得 `propertyName` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<QObject *> bindableTargetObject()`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含了该动画的目标`QObject`。
该属性定义了该动画的目标`QObject`。

**如何使用：** 调用 `bindableTargetObject()` 取得 `targetObject` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QByteArray propertyName() const`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含了该动画的目标属性名称。
该属性定义了该动画的目标属性名称。该属性名称是动画运行所必需的。

**如何使用：** 调用 `propertyName()` 读取当前值；它不会修改应用状态。

### `void setPropertyName(const QByteArray &propertyName)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含了该动画的目标属性名称。
该属性定义了该动画的目标属性名称。该属性名称是动画运行所必需的。

**如何使用：** 调用 `setPropertyName(...)` 修改 `propertyName`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTargetObject(QObject *target)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含了该动画的目标`QObject`。
该属性定义了该动画的目标`QObject`。

**如何使用：** 调用 `setTargetObject(...)` 修改 `targetObject`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QObject * targetObject() const`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含了该动画的目标`QObject`。
该属性定义了该动画的目标`QObject`。

**如何使用：** 调用 `targetObject()` 读取当前值；它不会修改应用状态。

## 6. 深入实践与常见坑

### 生命周期和资源边界

绑定、通知器和 change handler 都必须活到你希望回调持续工作的时间。移动 handler 可以转移回调责任，销毁 handler 会解除监听；绑定表达式引用的对象必须比绑定更长寿。

### 状态和错误边界

区分没有绑定、绑定有效、绑定被直接赋值打破、值发生变化和回调已解除。直接写入绑定属性往往会覆盖绑定关系，读取属性时要确认当前值是否来自预期依赖。

### 线程边界

属性绑定通常在创建它的线程计算，依赖对象的读写要遵守线程规则。不要让绑定表达式跨线程访问无锁共享状态，也不要在回调中修改会形成循环依赖的属性。

### 最容易出现的错误

动画对象销毁会立即停止；重复 start 可能重置进度；不要用动画替代业务状态；跨线程动画通常不是正确方向。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QPropertyAnimation` 所属机制类型：Qt 属性绑定机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
