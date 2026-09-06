# QPauseAnimation

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QPauseAnimation` 是 动画时间轴机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QPauseAnimation` 是动画框架中的类型，描述时间、状态、插值或动画组装行为。

**内部模型：** 动画通常由时间轴驱动属性变化；先确认动画对象、目标属性、持续时间和停止后的最终值，再组合 easing、loop 和 group。

**适用场景：** 界面过渡、状态变化和可视反馈需要平滑变化时使用。

**典型调用链：** 创建目标 -> 配置 duration/easing/start/end -> connect state/finished -> start/pause/stop -> 管理动画对象生命周期。

**先记住的坑：** 动画对象销毁会立即停止；重复 start 可能重置进度；不要用动画替代业务状态；跨线程动画通常不是正确方向。

## 2. 依赖与对象关系

- 头文件：`#include <QPauseAnimation>`
- 继承自：QAbstractAnimation
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

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

- `duration : int`

### 公有函数

- `QPauseAnimation(QObject *parent = nullptr)`
- `QPauseAnimation(int msecs, QObject *parent = nullptr)`
- `virtual ~QPauseAnimation()`
- `QBindable<int> bindableDuration()`
- `virtual int duration() const override`
- `void setDuration(int msecs)`

### 重实现的保护函数

- `virtual bool event(QEvent *e) override`
- `virtual void updateCurrentTime(int) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[bindable] duration : int`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示暂停的持续时间。
暂停的持续时间。持续时间不应为负。默认持续时间为250毫秒。

**如何使用：** 调用 `duration()` 读取当前值；它不会修改应用状态。

### `QPauseAnimation::QPauseAnimation(QObject *parent = nullptr)`

**作用与语义：**

构造一个QPauseAnimation。`parent`传递给`QObject`的构造器。默认时长为0。

### `QPauseAnimation::QPauseAnimation(int msecs, QObject *parent = nullptr)`

**作用与语义：**

构建一个QPauseAnimation。`msecs` 是暂停的持续时间。`parent`传递给`QObject`的构造器。

### `[virtual noexcept] QPauseAnimation::~QPauseAnimation()`

**作用与语义：**

会破坏暂停动画。

### `[override virtual protected] bool QPauseAnimation::event(QEvent *e)`

**作用与语义：**

重装：`QAbstractAnimation::event`（QEvent *事件）。

### `[override virtual protected] void QPauseAnimation::updateCurrentTime(int)`

**作用与语义：**

重实现自：`QAbstractAnimation::updateCurrentTime`（int currentTime）。
每次动画`currentTime`变化时都会调用这个纯虚拟函数。

### `QBindable<int> bindableDuration()`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示暂停的持续时间。
暂停的持续时间。持续时间不应为负。默认持续时间为250毫秒。

**如何使用：** 调用 `bindableDuration()` 取得 `duration` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `virtual int duration() const override`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示暂停的持续时间。
暂停的持续时间。持续时间不应为负。默认持续时间为250毫秒。

**如何使用：** 调用 `duration()` 读取当前值；它不会修改应用状态。

### `void setDuration(int msecs)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示暂停的持续时间。
暂停的持续时间。持续时间不应为负。默认持续时间为250毫秒。

**如何使用：** 调用 `setDuration(...)` 修改 `duration`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QPauseAnimation` 所属机制类型：动画时间轴机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
