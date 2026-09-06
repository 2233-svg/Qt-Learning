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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 21 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QProperty::QProperty()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QProperty` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] template <typename Functor> QProperty::QProperty(Functor &&f)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QProperty` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `f`：类型为 `Functor &&`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit default] QProperty::QProperty(T &&initialValue)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QProperty` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `initialValue`：类型为 `T &&`。没有默认值，调用时必须提供。传入 `T &&` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QProperty::QProperty(const QPropertyBinding<T> &binding)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QProperty` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `binding`：类型为 `const QPropertyBinding<T> &`。没有默认值，调用时必须提供。传入 `const QPropertyBinding<T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit default] QProperty::QProperty(const T &initialValue)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QProperty` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `initialValue`：类型为 `const T &`。没有默认值，调用时必须提供。传入 `const T &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QProperty::~QProperty()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QProperty` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] template <typename Functor> QPropertyNotifier QProperty::addNotifier(Functor f)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QProperty` 添加依赖、数据或子对象的 API `addNotifier`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`template <typename Functor> QPropertyNotifier`。
- 参数 `f`：类型为 `Functor`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPropertyBinding<T> QProperty::binding() const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `binding`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QPropertyBinding<T>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Functor> QPropertyChangeHandler<Functor> QProperty::onValueChanged(Functor f)`

**API 类别：** 成员函数说明

**中文解读：** 这是状态变化通知 `onValueChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`template <typename Functor> QPropertyChangeHandler<Functor>`。
- 参数 `f`：类型为 `Functor`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPropertyBinding<T> QProperty::setBinding(const QPropertyBinding<T> &newBinding)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBinding`。调用它会改变 `QProperty` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`QPropertyBinding<T>`。
- 参数 `newBinding`：类型为 `const QPropertyBinding<T> &`。没有默认值，调用时必须提供。传入 `const QPropertyBinding<T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] template <typename Functor> QPropertyBinding<T> QProperty::setBinding(Functor f)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBinding`。调用它会改变 `QProperty` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`template <typename Functor> QPropertyBinding<T>`。
- 参数 `f`：类型为 `Functor`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QProperty::setBinding(const QUntypedPropertyBinding &newBinding)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBinding`。调用它会改变 `QProperty` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`bool`。
- 参数 `newBinding`：类型为 `const QUntypedPropertyBinding &`。没有默认值，调用时必须提供。传入 `const QUntypedPropertyBinding &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QProperty::setValue(QProperty<T>::parameter_type newValue)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setValue`。调用它会改变 `QProperty` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `newValue`：类型为 `QProperty<T>::parameter_type`。没有默认值，调用时必须提供。传入 `QProperty<T>::parameter_type` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] template <typename Functor> QPropertyChangeHandler<Functor> QProperty::subscribe(Functor f)`

**API 类别：** 成员函数说明

**中文解读：** `QProperty::subscribe` 用于计算、查询或取得与“subscribe”相关的操作。调用时要先确认当前状态和 `f` 的有效范围；返回类型是 `template <typename Functor> QPropertyChangeHandler<Functor>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Functor> QPropertyChangeHandler<Functor>`。
- 参数 `f`：类型为 `Functor`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPropertyBinding<T> QProperty::takeBinding()`

**API 类别：** 成员函数说明

**中文解读：** `QProperty::takeBinding` 用于计算、查询或取得与“取出、Binding”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPropertyBinding<T>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPropertyBinding<T>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QProperty<T>::parameter_type QProperty::value() const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `value`，用于取得 `QProperty` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`QProperty<T>::parameter_type`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QProperty<T> &QProperty::operator=(QProperty<T>::parameter_type newValue)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QProperty` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QProperty<T> &`。
- 参数 `newValue`：类型为 `QProperty<T>::parameter_type`。没有默认值，调用时必须提供。传入 `QProperty<T>::parameter_type` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] void beginPropertyUpdateGroup()`

**API 类别：** 相关非成员函数

**中文解读：** 这是启动/建立资源的 API `beginPropertyUpdateGroup`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] void endPropertyUpdateGroup()`

**API 类别：** 相关非成员函数

**中文解读：** 这是结束/释放/取消 API `endPropertyUpdateGroup`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setValue(QProperty<T>::rvalue_ref newValue)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setValue`。调用它会改变 `QProperty` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `newValue`：类型为 `QProperty<T>::rvalue_ref`。没有默认值，调用时必须提供。传入 `QProperty<T>::rvalue_ref` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QProperty<T> & operator=(QProperty<T>::rvalue_ref newValue)`

**API 类别：** 公有函数

**中文解读：** 这是 `QProperty` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QProperty<T> &`。
- 参数 `newValue`：类型为 `QProperty<T>::rvalue_ref`。没有默认值，调用时必须提供。传入 `QProperty<T>::rvalue_ref` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
