# QAbstractAnimation

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QAbstractAnimation` 是 动画时间轴机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QAbstractAnimation` 是 Qt Core 中的抽象协议类型，通常通过具体子类、模型、插件或工厂来使用。

**内部模型：** 抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

**适用场景：** 当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。

**典型调用链：** 选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

**先记住的坑：** 不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

## 2. 依赖与对象关系

- 头文件：`#include <QAbstractAnimation>`
- 继承自：QObject
- 直接派生类：QAnimationGroup、QPauseAnimation,、QVariantAnimation

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

### 状态、生命周期和线程

**生命周期：** 动画必须保持目标和动画对象在运行期间有效。父对象、动画组或栈对象的生命周期要覆盖播放过程；删除或替换目标时先停止动画，避免回调访问旧对象。

**状态与结果：** 区分 stopped、running、paused、finished 和 loop 重启。`stop()` 后的当前值和终值取决于具体动画类型及配置，不能把停止当成完成；完成信号才表示时间轴走完。

**线程与事件循环：** 界面动画通常属于 GUI 线程并依赖事件循环；不要用动画对象承担跨线程任务或耗时计算。后台结果应先回到正确线程，再启动属性动画。

## 3. 直接使用

当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。 使用时通常按这个过程组织：选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum DeletionPolicy { KeepWhenStopped, DeleteWhenStopped }`
- `enum Direction { Forward, Backward }`
- `enum State { Stopped, Paused, Running }`

### 属性

- `currentLoop : int`
- `currentTime : int`
- `direction : Direction`
- `duration : int`
- `loopCount : int`
- `state : State`

### 公有函数

- `QAbstractAnimation(QObject *parent = nullptr)`
- `virtual ~QAbstractAnimation()`
- `QBindable<int> bindableCurrentLoop() const`
- `QBindable<int> bindableCurrentTime()`
- `QBindable<QAbstractAnimation::Direction> bindableDirection()`
- `QBindable<int> bindableLoopCount()`
- `QBindable<QAbstractAnimation::State> bindableState() const`
- `int currentLoop() const`
- `int currentLoopTime() const`
- `int currentTime() const`
- `QAbstractAnimation::Direction direction() const`
- `virtual int duration() const = 0`
- `QAnimationGroup * group() const`
- `int loopCount() const`
- `void setDirection(QAbstractAnimation::Direction direction)`
- `void setLoopCount(int loopCount)`
- `QAbstractAnimation::State state() const`
- `int totalDuration() const`

### 公有槽函数

- `void pause()`
- `void resume()`
- `void setCurrentTime(int msecs)`
- `void setPaused(bool paused)`
- `void start(QAbstractAnimation::DeletionPolicy policy = KeepWhenStopped)`
- `void stop()`

### 信号

- `void currentLoopChanged(int currentLoop)`
- `void directionChanged(QAbstractAnimation::Direction newDirection)`
- `void finished()`
- `void stateChanged(QAbstractAnimation::State newState, QAbstractAnimation::State oldState)`

### 保护函数

- `virtual void updateCurrentTime(int currentTime) = 0`
- `virtual void updateDirection(QAbstractAnimation::Direction direction)`
- `virtual void updateState(QAbstractAnimation::State newState, QAbstractAnimation::State oldState)`

### 重实现的保护函数

- `virtual bool event(QEvent *event) override`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 41 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QAbstractAnimation::Direction`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QAbstractAnimation` 暴露的类型声明 `Direction`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Direction`。
- 属性名：`QAbstractAnimation`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QAbstractAnimation::State`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QAbstractAnimation` 暴露的类型声明 `State`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:State`。
- 属性名：`QAbstractAnimation`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[bindable read-only] currentLoop : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QAbstractAnimation` 的状态/能力属性。通常通过 `currentLoop()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`currentLoop`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[bindable] currentTime : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QAbstractAnimation` 的配置属性。初始化或状态切换时通过 `setCurrentTime(...)` 设置，之后用 `currentTime()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`currentTime`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[bindable] direction : Direction`

**API 类别：** 属性说明

**中文解读：** 这是 `QAbstractAnimation` 的配置属性。初始化或状态切换时通过 `setDirection(...)` 设置，之后用 `direction()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`Direction`。
- 属性名：`direction`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] duration : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QAbstractAnimation` 的状态/能力属性。通常通过 `duration()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`duration`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[bindable] loopCount : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QAbstractAnimation` 的配置属性。初始化或状态切换时通过 `setLoopCount(...)` 设置，之后用 `loopCount()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`loopCount`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[bindable read-only] state : State`

**API 类别：** 属性说明

**中文解读：** 这是 `QAbstractAnimation` 的状态/能力属性。通常通过 `state()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`State`。
- 属性名：`state`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAbstractAnimation::QAbstractAnimation(QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAbstractAnimation` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QAbstractAnimation::~QAbstractAnimation()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAbstractAnimation` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QAbstractAnimation::currentLoopChanged(int currentLoop)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAbstractAnimation` 发出的通知信号 `currentLoopChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `currentLoop`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QAbstractAnimation::currentLoopTime() const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractAnimation::currentLoopTime` 用于计算、查询或取得与“当前、Loop、时间”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QAbstractAnimation::directionChanged(QAbstractAnimation::Direction newDirection)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAbstractAnimation` 发出的通知信号 `directionChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `newDirection`：类型为 `QAbstractAnimation::Direction`。没有默认值，调用时必须提供。传入 `QAbstractAnimation::Direction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] int QAbstractAnimation::duration() const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractAnimation::duration` 用于计算、查询或取得与“持续时间”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] bool QAbstractAnimation::event(QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractAnimation::event` 用于计算、查询或取得与“event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QAbstractAnimation::finished()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAbstractAnimation` 发出的通知信号 `finished`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAnimationGroup *QAbstractAnimation::group() const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractAnimation::group` 用于计算、查询或取得与“group”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAnimationGroup *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAnimationGroup *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QAbstractAnimation::pause()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `pause`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QAbstractAnimation::resume()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `resume`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QAbstractAnimation::setPaused(bool paused)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `setPaused`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `paused`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QAbstractAnimation::start(QAbstractAnimation::DeletionPolicy policy = KeepWhenStopped)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `start`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `policy`：类型为 `QAbstractAnimation::DeletionPolicy`。默认值为 `KeepWhenStopped`。传入 `QAbstractAnimation::DeletionPolicy` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QAbstractAnimation::stateChanged(QAbstractAnimation::State newState, QAbstractAnimation::State oldState)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAbstractAnimation` 发出的通知信号 `stateChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `newState`：类型为 `QAbstractAnimation::State`。没有默认值，调用时必须提供。传入 `QAbstractAnimation::State` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `oldState`：类型为 `QAbstractAnimation::State`。没有默认值，调用时必须提供。传入 `QAbstractAnimation::State` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QAbstractAnimation::stop()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `stop`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QAbstractAnimation::totalDuration() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `totalDuration`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual protected] void QAbstractAnimation::updateCurrentTime(int currentTime)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractAnimation::updateCurrentTime` 用于执行与“更新、当前、时间”相关的操作。调用时要先确认当前状态和 `currentTime` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `currentTime`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QAbstractAnimation::updateDirection(QAbstractAnimation::Direction direction)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractAnimation::updateDirection` 用于执行与“更新、Direction”相关的操作。调用时要先确认当前状态和 `direction` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `direction`：类型为 `QAbstractAnimation::Direction`。没有默认值，调用时必须提供。方向枚举，决定排列、遍历或坐标增长方向；要结合该类定义的枚举值判断实际方向。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QAbstractAnimation::updateState(QAbstractAnimation::State newState, QAbstractAnimation::State oldState)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractAnimation::updateState` 用于执行与“更新、State”相关的操作。调用时要先确认当前状态和 `newState`、`oldState` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `newState`：类型为 `QAbstractAnimation::State`。没有默认值，调用时必须提供。传入 `QAbstractAnimation::State` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `oldState`：类型为 `QAbstractAnimation::State`。没有默认值，调用时必须提供。传入 `QAbstractAnimation::State` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum DeletionPolicy { KeepWhenStopped, DeleteWhenStopped }`

**API 类别：** 公有类型

**中文解读：** 这是 `QAbstractAnimation` 暴露的类型声明 `Deletion、Policy`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<int> bindableCurrentLoop() const`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableCurrentLoop`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<int>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<int> bindableCurrentTime()`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableCurrentTime`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<int>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<QAbstractAnimation::Direction> bindableDirection()`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableDirection`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<QAbstractAnimation::Direction>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<int> bindableLoopCount()`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableLoopCount`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<int>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<QAbstractAnimation::State> bindableState() const`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableState`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<QAbstractAnimation::State>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int currentLoop() const`

**API 类别：** 公有函数

**中文解读：** `QAbstractAnimation::currentLoop` 用于计算、查询或取得与“当前、Loop”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int currentTime() const`

**API 类别：** 公有函数

**中文解读：** `QAbstractAnimation::currentTime` 用于计算、查询或取得与“当前、时间”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAbstractAnimation::Direction direction() const`

**API 类别：** 公有函数

**中文解读：** `QAbstractAnimation::direction` 用于计算、查询或取得与“direction”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAbstractAnimation::Direction`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAbstractAnimation::Direction`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int loopCount() const`

**API 类别：** 公有函数

**中文解读：** `QAbstractAnimation::loopCount` 用于计算、查询或取得与“loop、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setDirection(QAbstractAnimation::Direction direction)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setDirection`。调用它会改变 `QAbstractAnimation` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `direction`：类型为 `QAbstractAnimation::Direction`。没有默认值，调用时必须提供。方向枚举，决定排列、遍历或坐标增长方向；要结合该类定义的枚举值判断实际方向。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setLoopCount(int loopCount)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setLoopCount`。调用它会改变 `QAbstractAnimation` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `loopCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAbstractAnimation::State state() const`

**API 类别：** 公有函数

**中文解读：** `QAbstractAnimation::state` 用于计算、查询或取得与“state”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAbstractAnimation::State`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAbstractAnimation::State`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setCurrentTime(int msecs)`

**API 类别：** 公有槽函数

**中文解读：** 这是可被信号连接或元对象调用的槽 `setCurrentTime`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `msecs`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

动画必须保持目标和动画对象在运行期间有效。父对象、动画组或栈对象的生命周期要覆盖播放过程；删除或替换目标时先停止动画，避免回调访问旧对象。

### 状态和错误边界

区分 stopped、running、paused、finished 和 loop 重启。`stop()` 后的当前值和终值取决于具体动画类型及配置，不能把停止当成完成；完成信号才表示时间轴走完。

### 线程边界

界面动画通常属于 GUI 线程并依赖事件循环；不要用动画对象承担跨线程任务或耗时计算。后台结果应先回到正确线程，再启动属性动画。

### 最容易出现的错误

不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QAbstractAnimation` 所属机制类型：动画时间轴机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
