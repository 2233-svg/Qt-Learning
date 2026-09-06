# QUndoGroup

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QUndoGroup` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QUndoGroup` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QUndoGroup>`
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

### 公有函数

- `QUndoGroup(QObject *parent = nullptr)`
- `virtual ~QUndoGroup()`
- `QUndoStack * activeStack() const`
- `void addStack(QUndoStack *stack)`
- `bool canRedo() const`
- `bool canUndo() const`
- `QAction * createRedoAction(QObject *parent, const QString &prefix = QString()) const`
- `QAction * createUndoAction(QObject *parent, const QString &prefix = QString()) const`
- `bool isClean() const`
- `QString redoText() const`
- `void removeStack(QUndoStack *stack)`
- `QList<QUndoStack *> stacks() const`
- `QString undoText() const`

### 公有槽函数

- `void redo()`
- `void setActiveStack(QUndoStack *stack)`
- `void undo()`

### 信号

- `void activeStackChanged(QUndoStack *stack)`
- `void canRedoChanged(bool canRedo)`
- `void canUndoChanged(bool canUndo)`
- `void cleanChanged(bool clean)`
- `void indexChanged(int idx)`
- `void redoTextChanged(const QString &redoText)`
- `void undoTextChanged(const QString &undoText)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QUndoGroup::QUndoGroup(QObject *parent = nullptr)`

**作用与语义：**

创建一个带有父`parent`的空 QUndoGroup 对象。

### `[virtual noexcept] QUndoGroup::~QUndoGroup()`

**作用与语义：**

毁了`QUndoGroup`。

### `QUndoStack *QUndoGroup::activeStack() const`

**作用与语义：**

返回该组的活跃堆栈。
如果堆栈都不活跃，或者组为空，该函数返回`nullptr`。

### `[signal] void QUndoGroup::activeStackChanged(QUndoStack *stack)`

**作用与语义：**

每当组的活跃栈发生变化时，该信号都会发出。这可能发生在调用`setActiveStack()`或`QUndoStack::setActive()`，或当活动堆栈从组中移除时。`stack` 是新的活跃栈。如果没有激活的栈，`stack`为0。

### `void QUndoGroup::addStack(QUndoStack *stack)`

**作用与语义：**

向该组添加`stack`。该组不拥有该堆栈的所有权。另一种向组添加栈的方法是在 `QUndoStack::QUndoStack()` 中指定该组作为栈的父 `QObject`。在这种情况下，当组被删除时，栈也会被删除，方式类似于 QObjects。

### `bool QUndoGroup::canRedo() const`

**作用与语义：**

返回活跃堆栈`QUndoStack::canRedo()`的值。
如果堆栈都不活跃，或者组为空，该函数返回`false`。

### `[signal] void QUndoGroup::canRedoChanged(bool canRedo)`

**作用与语义：**

当活动堆栈发出`QUndoStack::canRedoChanged()`或激活堆栈发生变化时，该信号都会被发射。
`canRedo` 是新状态，或者如果激活栈为 0，则为假。

### `bool QUndoGroup::canUndo() const`

**作用与语义：**

返回活跃堆栈`QUndoStack::canUndo()`的值。
如果堆栈都不活跃，或者组为空，该函数返回`false`。

### `[signal] void QUndoGroup::canUndoChanged(bool canUndo)`

**作用与语义：**

当活跃堆栈发出`QUndoStack::canUndoChanged()`或激活堆栈发生变化时，该信号就会发出。
`canUndo` 是新状态，若活跃栈为 0，则为假。

### `[signal] void QUndoGroup::cleanChanged(bool clean)`

**作用与语义：**

当活动堆栈发出`QUndoStack::cleanChanged()`或激活堆栈发生变化时，该信号就会发出。
`clean` 是新状态，或者如果激活栈为0，则为真。

### `QAction *QUndoGroup::createRedoAction(QObject *parent, const QString &prefix = QString()) const`

**作用与语义：**

创建一个带有父`parent`的对象重做`QAction`。
触发该动作会对激活栈进行调用 `QUndoStack::redo()`。该动作的文本始终是下一次调用 `redo()` 时将重新执行的命令文本，前缀为 `prefix`。如果没有可重做的命令，组为空，或堆栈均未激活，该动作将被禁用。
如果`prefix`为空，则使用默认模板“Redo %1”代替前缀。在Qt 4.8之前，默认使用前缀“Redo”。

### `QAction *QUndoGroup::createUndoAction(QObject *parent, const QString &prefix = QString()) const`

**作用与语义：**

创建一个带有父`parent`的撤销对象`QAction`。
触发该操作会调用激活栈的 `QUndoStack::undo()`。该动作的文本始终是下一次调用 `undo()` 时会被撤销的命令文本，前缀为 `prefix`。如果没有可撤销的命令，组为空，或堆栈均未激活，该动作将被禁用。
如果`prefix`为空，默认模板“Undo %1”代替前缀。Qt 4.8之前，默认使用前缀“Undo”。

### `[signal] void QUndoGroup::indexChanged(int idx)`

**作用与语义：**

每当活动堆栈发出`QUndoStack::indexChanged()`或激活堆栈发生变化时，该信号都会被发射。
`idx` 是新的当前索引，或者如果活跃栈为 0，则为 0。

### `bool QUndoGroup::isClean() const`

**作用与语义：**

返回激活堆栈的值`QUndoStack::isClean()`。
如果堆栈都不活跃，或者组为空，该函数返回`true`。

### `[slot] void QUndoGroup::redo()`

**作用与语义：**

调用会`QUndoStack::redo()`在活跃堆栈上。
如果堆栈都不活跃，或者组为空，该函数不做任何事。

### `QString QUndoGroup::redoText() const`

**作用与语义：**

返回激活堆栈`QUndoStack::redoText()`的值。
如果没有任何堆栈处于活动状态，或者该组为空，该函数返回空字符串。

### `[signal] void QUndoGroup::redoTextChanged(const QString &redoText)`

**作用与语义：**

当活跃堆栈发出`QUndoStack::redoTextChanged()`或活跃堆栈发生变化时，该信号就会发出。
`redoText` 是新状态，或者如果激活栈为 0，则为空字符串。

### `void QUndoGroup::removeStack(QUndoStack *stack)`

**作用与语义：**

从该组中移除`stack`。如果堆栈是组中活跃的，活跃堆栈为0。

### `[slot] void QUndoGroup::setActiveStack(QUndoStack *stack)`

**作用与语义：**

将该组的活跃栈设置为`stack`。
如果堆栈不是该组的成员，这个函数就不做任何事。
这就像在打电话`QUndoStack::setActive()` `stack`。
`createUndoAction()`和`createRedoAction()`返回的动作将与`stack` `QUndoStack::createUndoAction()`和`QUndoStack::createRedoAction()`返回的行为相同。

### `QList<QUndoStack *> QUndoGroup::stacks() const`

**作用与语义：**

返回该组中的堆叠列表。

### `[slot] void QUndoGroup::undo()`

**作用与语义：**

调用`QUndoStack::undo()`在活跃堆栈上。
如果堆栈都不活跃，或者组为空，该函数不做任何事。

### `QString QUndoGroup::undoText() const`

**作用与语义：**

返回活跃堆栈`QUndoStack::undoText()`的值。
如果没有任何堆栈处于活动状态，或者该组为空，该函数返回空字符串。

### `[signal] void QUndoGroup::undoTextChanged(const QString &undoText)`

**作用与语义：**

当活动栈发射`QUndoStack::undoTextChanged()`或活动堆栈发生变化时，该信号都会被发射。
`undoText` 是新状态，或者如果激活栈为 0，则表示空字符串。

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

`QUndoGroup` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
