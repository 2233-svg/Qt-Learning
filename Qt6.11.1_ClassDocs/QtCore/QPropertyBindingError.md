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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 10 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QPropertyBindingError::Type`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QPropertyBindingError` 暴露的类型声明 `类型`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Type`。
- 属性名：`QPropertyBindingError`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPropertyBindingError::QPropertyBindingError()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPropertyBindingError` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPropertyBindingError::QPropertyBindingError(QPropertyBindingError::Type type, const QString &description = QString())`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPropertyBindingError` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `type`：类型为 `QPropertyBindingError::Type`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `description`：类型为 `const QString &`。默认值为 `QString()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPropertyBindingError::QPropertyBindingError(const QPropertyBindingError &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPropertyBindingError` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QPropertyBindingError &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPropertyBindingError::QPropertyBindingError(QPropertyBindingError &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPropertyBindingError` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `QPropertyBindingError &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QPropertyBindingError::~QPropertyBindingError()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPropertyBindingError` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QPropertyBindingError::description() const`

**API 类别：** 成员函数说明

**中文解读：** `QPropertyBindingError::description` 用于计算、查询或取得与“description”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPropertyBindingError::Type QPropertyBindingError::type() const`

**API 类别：** 成员函数说明

**中文解读：** `QPropertyBindingError::type` 用于计算、查询或取得与“类型”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPropertyBindingError::Type`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPropertyBindingError::Type`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPropertyBindingError &QPropertyBindingError::operator=(QPropertyBindingError &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPropertyBindingError` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QPropertyBindingError &`。
- 参数 `other`：类型为 `QPropertyBindingError &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPropertyBindingError &QPropertyBindingError::operator=(const QPropertyBindingError &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPropertyBindingError` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QPropertyBindingError &`。
- 参数 `other`：类型为 `const QPropertyBindingError &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

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

`QPropertyBindingError` 所属机制类型：Qt 属性绑定机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
