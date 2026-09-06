# QTimer

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QTimer` 把时间间隔转换成事件循环中的 `timeout()` 通知，适合周期任务、延迟任务和 UI 刷新。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QTimer` 把时间间隔转换成事件循环中的 `timeout()` 通知，适合周期任务、延迟任务和 UI 刷新。

**内部模型：** QTimer 不会创建线程，也不会保证精确到毫秒；它只是把一个定时事件投递到所属线程的事件循环。定时器所属线程必须有事件循环，并且 start/stop 要在该线程执行。

**适用场景：** 周期刷新、重试、超时、延迟初始化和把少量工作分批执行时使用；不要用零间隔定时器长期执行重计算，也不要用它替代真正的后台线程。

**典型调用链：** 创建并设置 parent -> connect(timeout) -> setInterval/setSingleShot -> start -> 在 timeout 中执行短任务 -> stop 或自然结束。

**先记住的坑：** timeout 不能假定精确时间；超时槽不能阻塞；跨线程启动/停止是错误用法；singleShot 的 context 应覆盖回调使用的对象生命周期。

## 2. 依赖与对象关系

- 头文件：`#include <QTimer>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

QTimer 不会创建线程，也不会保证精确到毫秒；它只是把一个定时事件投递到所属线程的事件循环。定时器所属线程必须有事件循环，并且 start/stop 要在该线程执行。

### 状态、生命周期和线程

**生命周期：** 先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

**状态与结果：** `isActive()`、`remainingTime()`、`singleShot` 和 `timerType` 共同描述定时器状态。零毫秒定时器适合把少量工作分批交还事件循环，不能用来替代后台线程。

**线程与事件循环：** QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

## 3. 直接使用

周期刷新、重试、超时、延迟初始化和把少量工作分批执行时使用；不要用零间隔定时器长期执行重计算，也不要用它替代真正的后台线程。 使用时通常按这个过程组织：创建并设置 parent -> connect(timeout) -> setInterval/setSingleShot -> start -> 在 timeout 中执行短任务 -> stop 或自然结束。

```cpp
#include <QTimer>

QTimer *timer = new QTimer(this);
timer->setInterval(1000);
connect(timer, &QTimer::timeout, this, [this] {
    updateStatus();
});
timer->start();
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 属性

- `active : bool`
- `interval : int`
- `remainingTime : int`
- `singleShot : bool`
- `timerType : Qt::TimerType`

### 公有函数

- `QTimer(QObject *parent = nullptr)`
- `virtual ~QTimer()`
- `QBindable<bool> bindableActive()`
- `QBindable<int> bindableInterval()`
- `QBindable<bool> bindableSingleShot()`
- `QBindable<Qt::TimerType> bindableTimerType()`
- `QMetaObject::Connection callOnTimeout(Functor &&slot)`
- `QMetaObject::Connection callOnTimeout(const QObject *context, Functor &&slot, Qt::ConnectionType connectionType = Qt::AutoConnection)`
- `(since 6.8) Qt::TimerId id() const`
- `int interval() const`
- `std::chrono::milliseconds intervalAsDuration() const`
- `bool isActive() const`
- `bool isSingleShot() const`
- `int remainingTime() const`
- `std::chrono::milliseconds remainingTimeAsDuration() const`
- `void setInterval(int msec)`
- `void setInterval(std::chrono::milliseconds value)`
- `void setSingleShot(bool singleShot)`
- `void setTimerType(Qt::TimerType atype)`
- `void start(std::chrono::milliseconds interval)`
- `int timerId() const`
- `Qt::TimerType timerType() const`

### 公有槽函数

- `void start(int msec)`
- `void start()`
- `void stop()`

### 信号

- `void timeout()`

### 静态公有成员

- `void singleShot(Duration interval, Functor &&functor)`
- `void singleShot(Duration interval, Qt::TimerType timerType, Functor &&functor)`
- `void singleShot(Duration interval, const QObject *context, Functor &&functor)`
- `void singleShot(Duration interval, Qt::TimerType timerType, const QObject *context, Functor &&functor)`
- `void singleShot(std::chrono::nanoseconds nsec, const QObject *receiver, const char *member)`
- `void singleShot(std::chrono::nanoseconds nsec, Qt::TimerType timerType, const QObject *receiver, const char *member)`

### 重实现的保护函数

- `virtual void timerEvent(QTimerEvent *e) override`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 38 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[bindable read-only] active : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QTimer` 的状态/能力属性。通常通过 `active()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`active`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[bindable] interval : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QTimer` 的配置属性。初始化或状态切换时通过 `setInterval(...)` 设置，之后用 `interval()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`interval`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] remainingTime : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QTimer` 的状态/能力属性。通常通过 `remainingTime()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`remainingTime`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[bindable] singleShot : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QTimer` 的配置属性。初始化或状态切换时通过 `setSingleShot(...)` 设置，之后用 `singleShot()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`singleShot`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 适合一次性延迟调用；回调要绑定 context，避免对象销毁后仍访问成员。

### `[bindable] timerType : Qt::TimerType`

**API 类别：** 属性说明

**中文解读：** 这是 `QTimer` 的配置属性。初始化或状态切换时通过 `setTimerType(...)` 设置，之后用 `TimerType()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`Qt::TimerType`。
- 属性名：`timerType`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QTimer::QTimer(QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTimer` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QTimer::~QTimer()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTimer` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Functor> QMetaObject::Connection QTimer::callOnTimeout(Functor &&slot)`

**API 类别：** 成员函数说明

**中文解读：** `QTimer::callOnTimeout` 用于计算、查询或取得与“call、On、超时”相关的操作。调用时要先确认当前状态和 `slot` 的有效范围；返回类型是 `template <typename Functor> QMetaObject::Connection`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Functor> QMetaObject::Connection`。
- 参数 `slot`：类型为 `Functor &&`。没有默认值，调用时必须提供。槽函数或回调。要确认签名、执行线程、上下文生命周期和是否可能阻塞。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Functor> QMetaObject::Connection QTimer::callOnTimeout(const QObject *context, Functor &&slot, Qt::ConnectionType connectionType = Qt::AutoConnection)`

**API 类别：** 成员函数说明

**中文解读：** `QTimer::callOnTimeout` 用于计算、查询或取得与“call、On、超时”相关的操作。调用时要先确认当前状态和 `context`、`slot`、`connectionType` 的有效范围；返回类型是 `template <typename Functor> QMetaObject::Connection`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Functor> QMetaObject::Connection`。
- 参数 `context`：类型为 `const QObject *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。
- 参数 `slot`：类型为 `Functor &&`。没有默认值，调用时必须提供。槽函数或回调。要确认签名、执行线程、上下文生命周期和是否可能阻塞。
- 参数 `connectionType`：类型为 `Qt::ConnectionType`。默认值为 `Qt::AutoConnection`。传入 `Qt::ConnectionType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] Qt::TimerId QTimer::id() const`

**API 类别：** 成员函数说明

**中文解读：** `QTimer::id` 用于计算、查询或取得与“id”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::TimerId`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::TimerId`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `std::chrono::milliseconds QTimer::intervalAsDuration() const`

**API 类别：** 成员函数说明

**中文解读：** `QTimer::intervalAsDuration` 用于计算、查询或取得与“间隔、As、持续时间”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `std::chrono::milliseconds`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`std::chrono::milliseconds`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTimer::isActive() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isActive`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `std::chrono::milliseconds QTimer::remainingTimeAsDuration() const`

**API 类别：** 成员函数说明

**中文解读：** `QTimer::remainingTimeAsDuration` 用于计算、查询或取得与“剩余、时间、As、持续时间”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `std::chrono::milliseconds`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`std::chrono::milliseconds`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] template <typename Duration, typename Functor> void QTimer::singleShot(Duration interval, Qt::TimerType timerType, Functor &&functor)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `singleShot`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename Duration, typename Functor> void`。
- 参数 `interval`：类型为 `Duration`。没有默认值，调用时必须提供。时间间隔，Qt 定时器通常使用毫秒；要检查 0、负数和超出范围时的语义。
- 参数 `timerType`：类型为 `Qt::TimerType`。没有默认值，调用时必须提供。传入 `Qt::TimerType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `functor`：类型为 `Functor &&`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 适合一次性延迟调用；回调要绑定 context，避免对象销毁后仍访问成员。

### `[static] void QTimer::singleShot(std::chrono::nanoseconds nsec, const QObject *receiver, const char *member)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `singleShot`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `nsec`：类型为 `std::chrono::nanoseconds`。没有默认值，调用时必须提供。传入 `std::chrono::nanoseconds` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `receiver`：类型为 `const QObject *`。没有默认值，调用时必须提供。接收者对象。它决定槽函数所属线程和连接生命周期，必须在回调使用期间有效。
- 参数 `member`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 适合一次性延迟调用；回调要绑定 context，避免对象销毁后仍访问成员。

### `[static] void QTimer::singleShot(std::chrono::nanoseconds nsec, Qt::TimerType timerType, const QObject *receiver, const char *member)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `singleShot`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `nsec`：类型为 `std::chrono::nanoseconds`。没有默认值，调用时必须提供。传入 `std::chrono::nanoseconds` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `timerType`：类型为 `Qt::TimerType`。没有默认值，调用时必须提供。传入 `Qt::TimerType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `receiver`：类型为 `const QObject *`。没有默认值，调用时必须提供。接收者对象。它决定槽函数所属线程和连接生命周期，必须在回调使用期间有效。
- 参数 `member`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 适合一次性延迟调用；回调要绑定 context，避免对象销毁后仍访问成员。

### `[slot] void QTimer::start(int msec)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `start`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `msec`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 通常与 `timeout()`、`setInterval()`、`setSingleShot()` 和 `stop()` 一起使用；启动成功只表示定时器已注册到事件循环。

### `[slot] void QTimer::start()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `start`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 通常与 `timeout()`、`setInterval()`、`setSingleShot()` 和 `stop()` 一起使用；启动成功只表示定时器已注册到事件循环。

### `void QTimer::start(std::chrono::milliseconds interval)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `start`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数 `interval`：类型为 `std::chrono::milliseconds`。没有默认值，调用时必须提供。时间间隔，Qt 定时器通常使用毫秒；要检查 0、负数和超出范围时的语义。

**正确调用组合：** 通常与 `timeout()`、`setInterval()`、`setSingleShot()` 和 `stop()` 一起使用；启动成功只表示定时器已注册到事件循环。

### `[slot] void QTimer::stop()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `stop`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 停止后不会再产生新的 timeout；若回调已经进入事件循环，仍要用对象状态和生命周期保护业务逻辑。

### `[private signal] void QTimer::timeout()`

**API 类别：** 成员函数说明

**中文解读：** `QTimer::timeout` 用于执行与“超时”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 这是定时事件通知，不保证精确到 interval；槽函数应短小，耗时任务要拆分或移到 worker。

### `[override virtual protected] void QTimer::timerEvent(QTimerEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QTimer::timerEvent` 用于执行与“timer、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QTimerEvent *`。没有默认值，调用时必须提供。传入 `QTimerEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QTimer::timerId() const`

**API 类别：** 成员函数说明

**中文解读：** `QTimer::timerId` 用于计算、查询或取得与“timer、Id”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<bool> bindableActive()`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableActive`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<bool>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<int> bindableInterval()`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableInterval`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<int>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<bool> bindableSingleShot()`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableSingleShot`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<bool>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<Qt::TimerType> bindableTimerType()`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableTimerType`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<Qt::TimerType>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int interval() const`

**API 类别：** 公有函数

**中文解读：** `QTimer::interval` 用于计算、查询或取得与“间隔”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool isSingleShot() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `isSingleShot`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int remainingTime() const`

**API 类别：** 公有函数

**中文解读：** `QTimer::remainingTime` 用于计算、查询或取得与“剩余、时间”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setInterval(int msec)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setInterval`。调用它会改变 `QTimer` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `msec`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 运行中的定时器修改 interval 会重新安排定时器并获得新的 timer id；负数和 0 要按 Qt 版本语义处理。

### `void setInterval(std::chrono::milliseconds value)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setInterval`。调用它会改变 `QTimer` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `value`：类型为 `std::chrono::milliseconds`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 运行中的定时器修改 interval 会重新安排定时器并获得新的 timer id；负数和 0 要按 Qt 版本语义处理。

### `void setSingleShot(bool singleShot)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setSingleShot`。调用它会改变 `QTimer` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `singleShot`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setTimerType(Qt::TimerType atype)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setTimerType`。调用它会改变 `QTimer` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `atype`：类型为 `Qt::TimerType`。没有默认值，调用时必须提供。传入 `Qt::TimerType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::TimerType timerType() const`

**API 类别：** 公有函数

**中文解读：** `QTimer::timerType` 用于计算、查询或取得与“timer、类型”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::TimerType`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::TimerType`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void singleShot(Duration interval, Functor &&functor)`

**API 类别：** 静态公有成员

**中文解读：** 这是静态工具 API `singleShot`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `interval`：类型为 `Duration`。没有默认值，调用时必须提供。时间间隔，Qt 定时器通常使用毫秒；要检查 0、负数和超出范围时的语义。
- 参数 `functor`：类型为 `Functor &&`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 适合一次性延迟调用；回调要绑定 context，避免对象销毁后仍访问成员。

### `void singleShot(Duration interval, const QObject *context, Functor &&functor)`

**API 类别：** 静态公有成员

**中文解读：** 这是静态工具 API `singleShot`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `interval`：类型为 `Duration`。没有默认值，调用时必须提供。时间间隔，Qt 定时器通常使用毫秒；要检查 0、负数和超出范围时的语义。
- 参数 `context`：类型为 `const QObject *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。
- 参数 `functor`：类型为 `Functor &&`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 适合一次性延迟调用；回调要绑定 context，避免对象销毁后仍访问成员。

### `void singleShot(Duration interval, Qt::TimerType timerType, const QObject *context, Functor &&functor)`

**API 类别：** 静态公有成员

**中文解读：** 这是静态工具 API `singleShot`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `interval`：类型为 `Duration`。没有默认值，调用时必须提供。时间间隔，Qt 定时器通常使用毫秒；要检查 0、负数和超出范围时的语义。
- 参数 `timerType`：类型为 `Qt::TimerType`。没有默认值，调用时必须提供。传入 `Qt::TimerType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `context`：类型为 `const QObject *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。
- 参数 `functor`：类型为 `Functor &&`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 适合一次性延迟调用；回调要绑定 context，避免对象销毁后仍访问成员。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

### 状态和错误边界

`isActive()`、`remainingTime()`、`singleShot` 和 `timerType` 共同描述定时器状态。零毫秒定时器适合把少量工作分批交还事件循环，不能用来替代后台线程。

### 线程边界

QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

### 最容易出现的错误

timeout 不能假定精确时间；超时槽不能阻塞；跨线程启动/停止是错误用法；singleShot 的 context 应覆盖回调使用的对象生命周期。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QTimer` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
