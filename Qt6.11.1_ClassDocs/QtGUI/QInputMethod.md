# QInputMethod

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QInputMethod` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QInputMethod` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QInputMethod>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

### 状态、生命周期和线程

**生命周期：** 先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

**状态与结果：** QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

**线程与事件循环：** QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

## 3. 直接使用

使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum Action { Click, ContextMenu }`

### 属性

- `anchorRectangle : QRectF`
- `animating : bool`
- `cursorRectangle : QRectF`
- `inputDirection : Qt::LayoutDirection`
- `inputItemClipRectangle : QRectF`
- `keyboardRectangle : QRectF`
- `locale : QLocale`
- `visible : bool`

### 公有函数

- `QRectF anchorRectangle() const`
- `QRectF cursorRectangle() const`
- `Qt::LayoutDirection inputDirection() const`
- `QRectF inputItemClipRectangle() const`
- `QRectF inputItemRectangle() const`
- `QTransform inputItemTransform() const`
- `bool isAnimating() const`
- `bool isVisible() const`
- `QRectF keyboardRectangle() const`
- `QLocale locale() const`
- `void setInputItemRectangle(const QRectF &rect)`
- `void setInputItemTransform(const QTransform &transform)`
- `void setVisible(bool visible)`

### 公有槽函数

- `void commit()`
- `void hide()`
- `void invokeAction(QInputMethod::Action a, int cursorPosition)`
- `void reset()`
- `void show()`
- `void update(Qt::InputMethodQueries queries)`

### 信号

- `void anchorRectangleChanged()`
- `void animatingChanged()`
- `void cursorRectangleChanged()`
- `void inputDirectionChanged(Qt::LayoutDirection newDirection)`
- `void inputItemClipRectangleChanged()`
- `void keyboardRectangleChanged()`
- `void localeChanged()`
- `void visibleChanged()`

### 静态公有成员

- `QVariant queryFocusObject(Qt::InputMethodQuery query, const QVariant &argument)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 37 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QInputMethod::Action`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QInputMethod` 暴露的类型声明 `Action`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Action`。
- 属性名：`QInputMethod`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] anchorRectangle : QRectF`

**API 类别：** 属性说明

**中文解读：** 这是 `QInputMethod` 的状态/能力属性。通常通过 `anchorRectangle()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`QRectF`。
- 属性名：`anchorRectangle`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] animating : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QInputMethod` 的状态/能力属性。通常通过 `animating()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`animating`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] cursorRectangle : QRectF`

**API 类别：** 属性说明

**中文解读：** 这是 `QInputMethod` 的状态/能力属性。通常通过 `cursorRectangle()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`QRectF`。
- 属性名：`cursorRectangle`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] inputDirection : Qt::LayoutDirection`

**API 类别：** 属性说明

**中文解读：** 这是 `QInputMethod` 的状态/能力属性。通常通过 `LayoutDirection()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`Qt::LayoutDirection`。
- 属性名：`inputDirection`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] inputItemClipRectangle : QRectF`

**API 类别：** 属性说明

**中文解读：** 这是 `QInputMethod` 的状态/能力属性。通常通过 `inputItemClipRectangle()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`QRectF`。
- 属性名：`inputItemClipRectangle`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] keyboardRectangle : QRectF`

**API 类别：** 属性说明

**中文解读：** 这是 `QInputMethod` 的状态/能力属性。通常通过 `keyboardRectangle()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`QRectF`。
- 属性名：`keyboardRectangle`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] locale : QLocale`

**API 类别：** 属性说明

**中文解读：** 这是 `QInputMethod` 的状态/能力属性。通常通过 `locale()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`QLocale`。
- 属性名：`locale`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] visible : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QInputMethod` 的状态/能力属性。通常通过 `visible()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`visible`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QInputMethod::commit()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `commit`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QInputMethod::hide()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `hide`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRectF QInputMethod::inputItemRectangle() const`

**API 类别：** 成员函数说明

**中文解读：** `QInputMethod::inputItemRectangle` 用于计算、查询或取得与“input、项目访问、Rectangle”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTransform QInputMethod::inputItemTransform() const`

**API 类别：** 成员函数说明

**中文解读：** `QInputMethod::inputItemTransform` 用于计算、查询或取得与“input、项目访问、Transform”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTransform`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTransform`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QInputMethod::invokeAction(QInputMethod::Action a, int cursorPosition)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `invokeAction`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `a`：类型为 `QInputMethod::Action`。没有默认值，调用时必须提供。传入 `QInputMethod::Action` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cursorPosition`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QVariant QInputMethod::queryFocusObject(Qt::InputMethodQuery query, const QVariant &argument)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `queryFocusObject`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `query`：类型为 `Qt::InputMethodQuery`。没有默认值，调用时必须提供。传入 `Qt::InputMethodQuery` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `argument`：类型为 `const QVariant &`。没有默认值，调用时必须提供。传入 `const QVariant &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QInputMethod::reset()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `reset`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QInputMethod::setInputItemRectangle(const QRectF &rect)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setInputItemRectangle`。调用它会改变 `QInputMethod` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `rect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QInputMethod::setInputItemTransform(const QTransform &transform)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setInputItemTransform`。调用它会改变 `QInputMethod` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `transform`：类型为 `const QTransform &`。没有默认值，调用时必须提供。传入 `const QTransform &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QInputMethod::setVisible(bool visible)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setVisible`。调用它会改变 `QInputMethod` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `visible`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QInputMethod::show()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `show`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QInputMethod::update(Qt::InputMethodQueries queries)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `update`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `queries`：类型为 `Qt::InputMethodQueries`。没有默认值，调用时必须提供。传入 `Qt::InputMethodQueries` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRectF anchorRectangle() const`

**API 类别：** 公有函数

**中文解读：** `QInputMethod::anchorRectangle` 用于计算、查询或取得与“anchor、Rectangle”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRectF cursorRectangle() const`

**API 类别：** 公有函数

**中文解读：** `QInputMethod::cursorRectangle` 用于计算、查询或取得与“cursor、Rectangle”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::LayoutDirection inputDirection() const`

**API 类别：** 公有函数

**中文解读：** `QInputMethod::inputDirection` 用于计算、查询或取得与“input、Direction”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::LayoutDirection`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::LayoutDirection`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRectF inputItemClipRectangle() const`

**API 类别：** 公有函数

**中文解读：** `QInputMethod::inputItemClipRectangle` 用于计算、查询或取得与“input、项目访问、Clip、Rectangle”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool isAnimating() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `isAnimating`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool isVisible() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `isVisible`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRectF keyboardRectangle() const`

**API 类别：** 公有函数

**中文解读：** `QInputMethod::keyboardRectangle` 用于计算、查询或取得与“keyboard、Rectangle”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QLocale locale() const`

**API 类别：** 公有函数

**中文解读：** `QInputMethod::locale` 用于计算、查询或取得与“locale”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QLocale`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QLocale`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void anchorRectangleChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `anchorRectangleChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void animatingChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `animatingChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void cursorRectangleChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `cursorRectangleChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void inputDirectionChanged(Qt::LayoutDirection newDirection)`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `inputDirectionChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `newDirection`：类型为 `Qt::LayoutDirection`。没有默认值，调用时必须提供。传入 `Qt::LayoutDirection` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void inputItemClipRectangleChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `inputItemClipRectangleChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void keyboardRectangleChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `keyboardRectangleChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void localeChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `localeChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void visibleChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `visibleChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

### 状态和错误边界

QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

### 线程边界

QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

### 最容易出现的错误

不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QInputMethod` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
