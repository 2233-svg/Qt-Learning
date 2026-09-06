# QParallelAnimationGroup

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QParallelAnimationGroup` 是 动画时间轴机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QParallelAnimationGroup` 是动画框架中的类型，描述时间、状态、插值或动画组装行为。

**内部模型：** 动画通常由时间轴驱动属性变化；先确认动画对象、目标属性、持续时间和停止后的最终值，再组合 easing、loop 和 group。

**适用场景：** 界面过渡、状态变化和可视反馈需要平滑变化时使用。

**典型调用链：** 创建目标 -> 配置 duration/easing/start/end -> connect state/finished -> start/pause/stop -> 管理动画对象生命周期。

**先记住的坑：** 动画对象销毁会立即停止；重复 start 可能重置进度；不要用动画替代业务状态；跨线程动画通常不是正确方向。

## 2. 依赖与对象关系

- 头文件：`#include <QParallelAnimationGroup>`
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

### 公有函数

- `QParallelAnimationGroup(QObject *parent = nullptr)`
- `virtual ~QParallelAnimationGroup()`

### 重实现的公有函数

- `virtual int duration() const override`

### 重实现的保护函数

- `virtual bool event(QEvent *event) override`
- `virtual void updateCurrentTime(int currentTime) override`
- `virtual void updateDirection(QAbstractAnimation::Direction direction) override`
- `virtual void updateState(QAbstractAnimation::State newState, QAbstractAnimation::State oldState) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QParallelAnimationGroup::QParallelAnimationGroup(QObject *parent = nullptr)`

**作用与语义：**

构建一个QParallelAnimationGroup。`parent`传递给`QObject`的构造器。

### `[virtual noexcept] QParallelAnimationGroup::~QParallelAnimationGroup()`

**作用与语义：**

会破坏动画组。它也会破坏所有动画。

### `[override virtual] int QParallelAnimationGroup::duration() const`

**作用与语义：**

重实现自：`QAbstractAnimation::duration()` const.
该属性表示动画的持续时间。
如果持续时间为-1，表示持续时间未定义。在这种情况下，`loopCount`被忽略。

### `[override virtual protected] bool QParallelAnimationGroup::event(QEvent *event)`

**作用与语义：**

重现：`QAnimationGroup::event`（QEvent *事件）。

### `[override virtual protected] void QParallelAnimationGroup::updateCurrentTime(int currentTime)`

**作用与语义：**

重实现自：`QAbstractAnimation::updateCurrentTime`（int currentTime）。
每次动画`currentTime`变化时都会调用这个纯虚拟函数。

### `[override virtual protected] void QParallelAnimationGroup::updateDirection(QAbstractAnimation::Direction direction)`

**作用与语义：**

重实现自：`QAbstractAnimation::updateDirection`（QAbstractAnimation：:D制作方向）。
当动画方向改变时，`QAbstractAnimation`调用了这个虚拟函数。`direction`参数是新的方向。

### `[override virtual protected] void QParallelAnimationGroup::updateState(QAbstractAnimation::State newState, QAbstractAnimation::State oldState)`

**作用与语义：**

重实现自：`QAbstractAnimation::updateState`（QAbstractAnimation：：State newState， QAbstractAnimation：：State oldState）。
当动画状态从`oldState`变为`newState`时，`QAbstractAnimation`调用了这个虚拟函数。

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

`QParallelAnimationGroup` 所属机制类型：动画时间轴机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
