# QActionGroup

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QActionGroup` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QActionGroup` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QActionGroup>`
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

- `enum class ExclusionPolicy { None, Exclusive, ExclusiveOptional }`

### 属性

- `enabled : bool`
- `exclusionPolicy : QActionGroup::ExclusionPolicy`
- `visible : bool`

### 公有函数

- `QActionGroup(QObject *parent)`
- `virtual ~QActionGroup()`
- `QList<QAction *> actions() const`
- `QAction * addAction(QAction *action)`
- `QAction * addAction(const QString &text)`
- `QAction * addAction(const QIcon &icon, const QString &text)`
- `QAction * checkedAction() const`
- `QActionGroup::ExclusionPolicy exclusionPolicy() const`
- `bool isEnabled() const`
- `bool isExclusive() const`
- `bool isVisible() const`
- `void removeAction(QAction *action)`

### 公有槽函数

- `void setDisabled(bool b)`
- `void setEnabled(bool)`
- `void setExclusionPolicy(QActionGroup::ExclusionPolicy policy)`
- `void setExclusive(bool b)`
- `void setVisible(bool)`

### 信号

- `void hovered(QAction *action)`
- `void triggered(QAction *action)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum class QActionGroup::ExclusionPolicy`

**作用与语义：**

该枚举规定了可用于控制小组对可检查动作进行独占检查的不同策略。
- `QActionGroup::ExclusionPolicy::None`：`0`;组内的动作可以相互独立检查。
- `QActionGroup::ExclusionPolicy::Exclusive`：`1`;任何时候只能检查一个操作。这是默认策略。
- `QActionGroup::ExclusionPolicy::ExclusiveOptional`：`2`;每次最多可检查一个动作。这些动作也可以全部未被检查。

### `enabled : bool`

**作用与语义：**

该属性是否允许作用群。
组中的每个动作都会被启用或禁用，除非它被明确禁用。

**如何使用：** 调用 `enabled()` 读取当前值；它不会修改应用状态。

### `exclusionPolicy : QActionGroup::ExclusionPolicy`

**作用与语义：**

该属性包含组排他检查策略。
如果 exclusionPolicy 设置为 Exclusive，则动作组中任何时候只能有一个可检查动作处于激活状态。如果用户在组中选择另一个可检查动作，所选动作将变为激活，原本活跃的动作变为非活跃。如果 exclusionPolicy 设置为 ExclusionOptional，该组是排他的，但组中可检查的激活操作可以取消勾选，导致组内没有任何动作被勾选。

**如何使用：** 调用 `exclusionPolicy()` 读取当前值；它不会修改应用状态。

### `visible : bool`

**作用与语义：**

该属性表示作用群是否可见。
动作组中的每个动作都会与该组的可见状态匹配，除非它被明确隐藏。

**如何使用：** 调用 `visible()` 读取当前值；它不会修改应用状态。

### `[explicit] QActionGroup::QActionGroup(QObject *parent)`

**作用与语义：**

为`parent`对象构造一个动作群。
动作组默认是异他。调用 `setExclusive`（false） 使动作组非异。使组为异，但允许取消勾选激活动作调用 `setExclusionPolicy`（`QActionGroup::ExclusionPolicy::ExclusiveOptional`）。

### `[virtual noexcept] QActionGroup::~QActionGroup()`

**作用与语义：**

摧毁了行动小组。

### `QList<QAction *> QActionGroup::actions() const`

**作用与语义：**

返回该组的行动列表。这可能是空的。

### `QAction *QActionGroup::addAction(QAction *action)`

**作用与语义：**

将`action`加入该组，并返回。
通常，动作是通过创建以该组为父的组来添加，因此通常不使用该函数。

### `QAction *QActionGroup::addAction(const QString &text)`

**作用与语义：**

创建并返回带有`text`的动作。新创建的动作是该动作组的子。
通常，动作是通过创建以该组为父的组来添加，因此通常不使用该函数。

### `QAction *QActionGroup::addAction(const QIcon &icon, const QString &text)`

**作用与语义：**

创建并返回一个动作，`text` 和 `icon`。新创建的动作是该动作组的子节点。
通常，动作是通过创建以该组为父的组来添加，因此通常不使用该函数。

### `QAction *QActionGroup::checkedAction() const`

**作用与语义：**

返回组中当前已勾选的动作，若未勾选则返回`nullptr`。

### `[signal] void QActionGroup::hovered(QAction *action)`

**作用与语义：**

当用户高亮动作组中的指定`action`时，会发出该信号;例如，当用户在菜单选项或工具栏按钮上停留光标，或按下动作快捷键组合时。

### `bool QActionGroup::isExclusive() const`

**作用与语义：**

如果群是异的，则返回为真。
如果`ExclusionPolicy`是排他或排除可选，则该组是排他。

### `void QActionGroup::removeAction(QAction *action)`

**作用与语义：**

移除该组中的`action`。因此该动作将没有父。

### `[slot] void QActionGroup::setDisabled(bool b)`

**作用与语义：**

这是`enabled`属性的一个便利函数，对信号-槽连接非常有用。如果`b`为真，则该动作组被禁用;否则则被启用。

### `[slot] void QActionGroup::setExclusive(bool b)`

**作用与语义：**

启用或禁用组排除检查。
这是一种方便方法，当`b`为真时调用`setExclusionPolicy`（`ExclusionPolicy::Exclusive`），否则调用`setExclusionPolicy`（`QActionGroup::ExclusionPolicy::None`）。

### `[signal] void QActionGroup::triggered(QAction *action)`

**作用与语义：**

当用户激活动作组中的指定`action`时，会发出该信号;例如，当用户点击菜单选项或工具栏按钮，或按下动作快捷键组合时。
连接这个信号进行指令操作。

### `QActionGroup::ExclusionPolicy exclusionPolicy() const`

**作用与语义：**

该属性包含组排他检查策略。
如果 exclusionPolicy 设置为 Exclusive，则动作组中任何时候只能有一个可检查动作处于激活状态。如果用户在组中选择另一个可检查动作，所选动作将变为激活，原本活跃的动作变为非活跃。如果 exclusionPolicy 设置为 ExclusionOptional，该组是排他的，但组中可检查的激活操作可以取消勾选，导致组内没有任何动作被勾选。

**如何使用：** 调用 `exclusionPolicy()` 读取当前值；它不会修改应用状态。

### `bool isEnabled() const`

**作用与语义：**

该属性是否允许作用群。
组中的每个动作都会被启用或禁用，除非它被明确禁用。

**如何使用：** 调用 `isEnabled()` 读取当前值；它不会修改应用状态。

### `bool isVisible() const`

**作用与语义：**

该属性表示作用群是否可见。
动作组中的每个动作都会与该组的可见状态匹配，除非它被明确隐藏。

**如何使用：** 调用 `isVisible()` 读取当前值；它不会修改应用状态。

### `void setEnabled(bool)`

**作用与语义：**

该属性是否允许作用群。
组中的每个动作都会被启用或禁用，除非它被明确禁用。

**如何使用：** 调用 `setEnabled(...)` 修改 `enabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setExclusionPolicy(QActionGroup::ExclusionPolicy policy)`

**作用与语义：**

该属性包含组排他检查策略。
如果 exclusionPolicy 设置为 Exclusive，则动作组中任何时候只能有一个可检查动作处于激活状态。如果用户在组中选择另一个可检查动作，所选动作将变为激活，原本活跃的动作变为非活跃。如果 exclusionPolicy 设置为 ExclusionOptional，该组是排他的，但组中可检查的激活操作可以取消勾选，导致组内没有任何动作被勾选。

**如何使用：** 调用 `setExclusionPolicy(...)` 修改 `exclusionPolicy`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setVisible(bool)`

**作用与语义：**

该属性表示作用群是否可见。
动作组中的每个动作都会与该组的可见状态匹配，除非它被明确隐藏。

**如何使用：** 调用 `setVisible(...)` 修改 `visible`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QActionGroup` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
