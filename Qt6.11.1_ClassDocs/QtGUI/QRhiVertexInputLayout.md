# QRhiVertexInputLayout

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QRhiVertexInputLayout` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QRhiVertexInputLayout` 是 Qt Widgets 界面机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Widgets 通过父子控件树、布局系统、事件分发和重绘请求组成界面。控件的可见区域、sizeHint、sizePolicy、字体和平台 style 共同影响最终几何；用户输入先进入 Qt 事件系统，再由控件的事件函数、信号或快捷键处理。

**适用场景：** 创建 QApplication 后创建控件，设置 parent 或把控件加入布局，连接用户操作信号，再显示顶层窗口。复合界面用布局嵌套；控件尺寸异常时同时检查 sizePolicy、minimum/maximum size、layout stretch、margins 和 spacing。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要用固定坐标拼接响应式界面；不要给已经加入布局的控件反复 `setGeometry()`；不要在 `paintEvent()` 中修改业务状态；不要忘记窗口关闭、对象销毁和应用退出是三个不同事件。

## 2. 依赖与对象关系

- 头文件：`#include <rhi/qrhi.h>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS GuiPrivate)
target_link_libraries(mytarget PRIVATE Qt6::GuiPrivate)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

Widgets 通过父子控件树、布局系统、事件分发和重绘请求组成界面。控件的可见区域、sizeHint、sizePolicy、字体和平台 style 共同影响最终几何；用户输入先进入 Qt 事件系统，再由控件的事件函数、信号或快捷键处理。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

创建 QApplication 后创建控件，设置 parent 或把控件加入布局，连接用户操作信号，再显示顶层窗口。复合界面用布局嵌套；控件尺寸异常时同时检查 sizePolicy、minimum/maximum size、layout stretch、margins 和 spacing。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QRhiVertexInputLayout()`
- `const QRhiVertexInputAttribute * attributeAt(qsizetype index) const`
- `qsizetype attributeCount() const`
- `const QRhiVertexInputBinding * bindingAt(qsizetype index) const`
- `qsizetype bindingCount() const`
- `const QRhiVertexInputAttribute * cbeginAttributes() const`
- `const QRhiVertexInputBinding * cbeginBindings() const`
- `const QRhiVertexInputAttribute * cendAttributes() const`
- `const QRhiVertexInputBinding * cendBindings() const`
- `void setAttributes(std::initializer_list<QRhiVertexInputAttribute> list)`
- `void setAttributes(InputIterator first, InputIterator last)`
- `void setBindings(std::initializer_list<QRhiVertexInputBinding> list)`
- `void setBindings(InputIterator first, InputIterator last)`

### 相关非成员函数

- `size_t qHash(const QRhiVertexInputLayout &key, size_t seed = 0)`
- `bool operator!=(const QRhiVertexInputLayout &a, const QRhiVertexInputLayout &b)`
- `bool operator==(const QRhiVertexInputLayout &a, const QRhiVertexInputLayout &b)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 16 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[constexpr noexcept] QRhiVertexInputLayout::QRhiVertexInputLayout()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRhiVertexInputLayout` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QRhiVertexInputAttribute *QRhiVertexInputLayout::attributeAt(qsizetype index) const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiVertexInputLayout::attributeAt` 用于计算、查询或取得与“attribute、按位置访问”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `const QRhiVertexInputAttribute *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QRhiVertexInputAttribute *`。
- 参数 `index`：类型为 `qsizetype`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QRhiVertexInputLayout::attributeCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiVertexInputLayout::attributeCount` 用于计算、查询或取得与“attribute、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QRhiVertexInputBinding *QRhiVertexInputLayout::bindingAt(qsizetype index) const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `bindingAt`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`const QRhiVertexInputBinding *`。
- 参数 `index`：类型为 `qsizetype`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QRhiVertexInputLayout::bindingCount() const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `bindingCount`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QRhiVertexInputAttribute *QRhiVertexInputLayout::cbeginAttributes() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiVertexInputLayout::cbeginAttributes` 用于计算、查询或取得与“cbegin、Attributes”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QRhiVertexInputAttribute *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QRhiVertexInputAttribute *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QRhiVertexInputBinding *QRhiVertexInputLayout::cbeginBindings() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiVertexInputLayout::cbeginBindings` 用于计算、查询或取得与“cbegin、Bindings”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QRhiVertexInputBinding *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QRhiVertexInputBinding *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QRhiVertexInputAttribute *QRhiVertexInputLayout::cendAttributes() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiVertexInputLayout::cendAttributes` 用于计算、查询或取得与“cend、Attributes”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QRhiVertexInputAttribute *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QRhiVertexInputAttribute *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QRhiVertexInputBinding *QRhiVertexInputLayout::cendBindings() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiVertexInputLayout::cendBindings` 用于计算、查询或取得与“cend、Bindings”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QRhiVertexInputBinding *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QRhiVertexInputBinding *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiVertexInputLayout::setAttributes(std::initializer_list<QRhiVertexInputAttribute> list)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAttributes`。调用它会改变 `QRhiVertexInputLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `list`：类型为 `std::initializer_list<QRhiVertexInputAttribute>`。没有默认值，调用时必须提供。传入 `std::initializer_list<QRhiVertexInputAttribute>` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename InputIterator> void QRhiVertexInputLayout::setAttributes(InputIterator first, InputIterator last)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAttributes`。调用它会改变 `QRhiVertexInputLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`template <typename InputIterator> void`。
- 参数 `first`：类型为 `InputIterator`。没有默认值，调用时必须提供。传入 `InputIterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `last`：类型为 `InputIterator`。没有默认值，调用时必须提供。传入 `InputIterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiVertexInputLayout::setBindings(std::initializer_list<QRhiVertexInputBinding> list)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBindings`。调用它会改变 `QRhiVertexInputLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `list`：类型为 `std::initializer_list<QRhiVertexInputBinding>`。没有默认值，调用时必须提供。传入 `std::initializer_list<QRhiVertexInputBinding>` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename InputIterator> void QRhiVertexInputLayout::setBindings(InputIterator first, InputIterator last)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBindings`。调用它会改变 `QRhiVertexInputLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`template <typename InputIterator> void`。
- 参数 `first`：类型为 `InputIterator`。没有默认值，调用时必须提供。传入 `InputIterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `last`：类型为 `InputIterator`。没有默认值，调用时必须提供。传入 `InputIterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] size_t qHash(const QRhiVertexInputLayout &key, size_t seed = 0)`

**API 类别：** 相关非成员函数

**中文解读：** `QRhiVertexInputLayout::qHash` 用于计算、查询或取得与“q、Hash”相关的操作。调用时要先确认当前状态和 `key`、`seed` 的有效范围；返回类型是 `size_t`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`size_t`。
- 参数 `key`：类型为 `const QRhiVertexInputLayout &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `seed`：类型为 `size_t`。默认值为 `0`。传入 `size_t` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator!=(const QRhiVertexInputLayout &a, const QRhiVertexInputLayout &b)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QRhiVertexInputLayout` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `a`：类型为 `const QRhiVertexInputLayout &`。没有默认值，调用时必须提供。传入 `const QRhiVertexInputLayout &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `b`：类型为 `const QRhiVertexInputLayout &`。没有默认值，调用时必须提供。传入 `const QRhiVertexInputLayout &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator==(const QRhiVertexInputLayout &a, const QRhiVertexInputLayout &b)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QRhiVertexInputLayout` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `a`：类型为 `const QRhiVertexInputLayout &`。没有默认值，调用时必须提供。传入 `const QRhiVertexInputLayout &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `b`：类型为 `const QRhiVertexInputLayout &`。没有默认值，调用时必须提供。传入 `const QRhiVertexInputLayout &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

不要用固定坐标拼接响应式界面；不要给已经加入布局的控件反复 `setGeometry()`；不要在 `paintEvent()` 中修改业务状态；不要忘记窗口关闭、对象销毁和应用退出是三个不同事件。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QRhiVertexInputLayout` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
