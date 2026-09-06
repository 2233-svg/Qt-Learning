# QSequentialAnimationGroup

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QSequentialAnimationGroup` 是 动画时间轴机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QSequentialAnimationGroup` 是动画框架中的类型，描述时间、状态、插值或动画组装行为。

**内部模型：** 动画通常由时间轴驱动属性变化；先确认动画对象、目标属性、持续时间和停止后的最终值，再组合 easing、loop 和 group。

**适用场景：** 界面过渡、状态变化和可视反馈需要平滑变化时使用。

**典型调用链：** 创建目标 -> 配置 duration/easing/start/end -> connect state/finished -> start/pause/stop -> 管理动画对象生命周期。

**先记住的坑：** 动画对象销毁会立即停止；重复 start 可能重置进度；不要用动画替代业务状态；跨线程动画通常不是正确方向。

## 2. 依赖与对象关系

- 头文件：`#include <QSequentialAnimationGroup>`
- 继承自：QAnimationGroup
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

**生命周期：** 动画必须保持目标和动画对象在运行期间有效。父对象、动画组或栈对象的生命周期要覆盖播放过程；删除或替换目标时先停止动画，避免回调访问旧对象。

**状态与结果：** 区分 stopped、running、paused、finished 和 loop 重启。`stop()` 后的当前值和终值取决于具体动画类型及配置，不能把停止当成完成；完成信号才表示时间轴走完。

**线程与事件循环：** 界面动画通常属于 GUI 线程并依赖事件循环；不要用动画对象承担跨线程任务或耗时计算。后台结果应先回到正确线程，再启动属性动画。

## 3. 直接使用

界面过渡、状态变化和可视反馈需要平滑变化时使用。 使用时通常按这个过程组织：创建目标 -> 配置 duration/easing/start/end -> connect state/finished -> start/pause/stop -> 管理动画对象生命周期。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 属性

- `currentAnimation : QAbstractAnimation*`

### 公有函数

- `QSequentialAnimationGroup(QObject *parent = nullptr)`
- `virtual ~QSequentialAnimationGroup()`
- `QPauseAnimation * addPause(int msecs)`
- `QBindable<QAbstractAnimation *> bindableCurrentAnimation() const`
- `QAbstractAnimation * currentAnimation() const`
- `QPauseAnimation * insertPause(int index, int msecs)`

### 重实现的公有函数

- `virtual int duration() const override`

### 信号

- `void currentAnimationChanged(QAbstractAnimation *current)`

### 重实现的保护函数

- `virtual bool event(QEvent *event) override`
- `virtual void updateCurrentTime(int currentTime) override`
- `virtual void updateDirection(QAbstractAnimation::Direction direction) override`
- `virtual void updateState(QAbstractAnimation::State newState, QAbstractAnimation::State oldState) override`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 13 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[bindable read-only] currentAnimation : QAbstractAnimation*`

**API 类别：** 属性说明

**中文解读：** 这是 `QSequentialAnimationGroup` 的状态/能力属性。通常通过 `currentAnimation()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`QAbstractAnimation*`。
- 属性名：`currentAnimation`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSequentialAnimationGroup::QSequentialAnimationGroup(QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSequentialAnimationGroup` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QSequentialAnimationGroup::~QSequentialAnimationGroup()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSequentialAnimationGroup` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPauseAnimation *QSequentialAnimationGroup::addPause(int msecs)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QSequentialAnimationGroup` 添加依赖、数据或子对象的 API `addPause`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QPauseAnimation *`。
- 参数 `msecs`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QSequentialAnimationGroup::currentAnimationChanged(QAbstractAnimation *current)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSequentialAnimationGroup` 发出的通知信号 `currentAnimationChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `current`：类型为 `QAbstractAnimation *`。没有默认值，调用时必须提供。传入 `QAbstractAnimation *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] int QSequentialAnimationGroup::duration() const`

**API 类别：** 成员函数说明

**中文解读：** `QSequentialAnimationGroup::duration` 用于计算、查询或取得与“持续时间”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] bool QSequentialAnimationGroup::event(QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QSequentialAnimationGroup::event` 用于计算、查询或取得与“event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPauseAnimation *QSequentialAnimationGroup::insertPause(int index, int msecs)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QSequentialAnimationGroup` 添加依赖、数据或子对象的 API `insertPause`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QPauseAnimation *`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `msecs`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QSequentialAnimationGroup::updateCurrentTime(int currentTime)`

**API 类别：** 成员函数说明

**中文解读：** `QSequentialAnimationGroup::updateCurrentTime` 用于执行与“更新、当前、时间”相关的操作。调用时要先确认当前状态和 `currentTime` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `currentTime`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QSequentialAnimationGroup::updateDirection(QAbstractAnimation::Direction direction)`

**API 类别：** 成员函数说明

**中文解读：** `QSequentialAnimationGroup::updateDirection` 用于执行与“更新、Direction”相关的操作。调用时要先确认当前状态和 `direction` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `direction`：类型为 `QAbstractAnimation::Direction`。没有默认值，调用时必须提供。方向枚举，决定排列、遍历或坐标增长方向；要结合该类定义的枚举值判断实际方向。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QSequentialAnimationGroup::updateState(QAbstractAnimation::State newState, QAbstractAnimation::State oldState)`

**API 类别：** 成员函数说明

**中文解读：** `QSequentialAnimationGroup::updateState` 用于执行与“更新、State”相关的操作。调用时要先确认当前状态和 `newState`、`oldState` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `newState`：类型为 `QAbstractAnimation::State`。没有默认值，调用时必须提供。传入 `QAbstractAnimation::State` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `oldState`：类型为 `QAbstractAnimation::State`。没有默认值，调用时必须提供。传入 `QAbstractAnimation::State` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<QAbstractAnimation *> bindableCurrentAnimation() const`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableCurrentAnimation`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<QAbstractAnimation *>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAbstractAnimation * currentAnimation() const`

**API 类别：** 公有函数

**中文解读：** `QSequentialAnimationGroup::currentAnimation` 用于计算、查询或取得与“当前、Animation”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAbstractAnimation *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAbstractAnimation *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

动画必须保持目标和动画对象在运行期间有效。父对象、动画组或栈对象的生命周期要覆盖播放过程；删除或替换目标时先停止动画，避免回调访问旧对象。

### 状态和错误边界

区分 stopped、running、paused、finished 和 loop 重启。`stop()` 后的当前值和终值取决于具体动画类型及配置，不能把停止当成完成；完成信号才表示时间轴走完。

### 线程边界

界面动画通常属于 GUI 线程并依赖事件循环；不要用动画对象承担跨线程任务或耗时计算。后台结果应先回到正确线程，再启动属性动画。

### 最容易出现的错误

动画对象销毁会立即停止；重复 start 可能重置进度；不要用动画替代业务状态；跨线程动画通常不是正确方向。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QSequentialAnimationGroup` 所属机制类型：动画时间轴机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
