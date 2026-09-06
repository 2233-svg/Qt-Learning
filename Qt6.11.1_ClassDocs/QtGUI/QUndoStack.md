# QUndoStack

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QUndoStack` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QUndoStack` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QUndoStack>`
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

### 属性

- `active : bool`
- `canRedo : bool`
- `canUndo : bool`
- `clean : bool`
- `redoText : QString`
- `undoLimit : int`
- `undoText : QString`

### 公有函数

- `QUndoStack(QObject *parent = nullptr)`
- `virtual ~QUndoStack()`
- `void beginMacro(const QString &text)`
- `bool canRedo() const`
- `bool canUndo() const`
- `int cleanIndex() const`
- `void clear()`
- `const QUndoCommand * command(int index) const`
- `int count() const`
- `QAction * createRedoAction(QObject *parent, const QString &prefix = QString()) const`
- `QAction * createUndoAction(QObject *parent, const QString &prefix = QString()) const`
- `void endMacro()`
- `int index() const`
- `bool isActive() const`
- `bool isClean() const`
- `void push(QUndoCommand *cmd)`
- `QString redoText() const`
- `void setUndoLimit(int limit)`
- `QString text(int idx) const`
- `int undoLimit() const`
- `QString undoText() const`

### 公有槽函数

- `void redo()`
- `void resetClean()`
- `void setActive(bool active = true)`
- `void setClean()`
- `void setIndex(int idx)`
- `void undo()`

### 信号

- `void canRedoChanged(bool canRedo)`
- `void canUndoChanged(bool canUndo)`
- `void cleanChanged(bool clean)`
- `void indexChanged(int idx)`
- `void redoTextChanged(const QString &redoText)`
- `void undoTextChanged(const QString &undoText)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `active : bool`

**作用与语义：**

该属性表示该堆栈的活跃状态。
应用程序通常有多个撤销栈，每个打开的文档对应一个。活跃栈是与当前活跃文档关联的栈。如果栈属于某个`QUndoGroup`，调用`QUndoGroup::undo()`或`QUndoGroup::redo()`的调用会在该栈活跃时被转发到该栈。如果`QUndoGroup`被`QUndoView`监控，视图会显示该栈在激活时的内容。如果栈不属于`QUndoGroup`，激活无效。
程序员负责通过调用 setActive() 指定哪个栈处于激活状态，通常是在相关文档窗口获得焦点时。

**如何使用：** 调用 `active()` 读取当前值；它不会修改应用状态。

### `[read-only] canRedo : bool`

**作用与语义：**

该属性决定了该堆栈是否可以重做。
该属性表明是否存在可重执行的命令。

**如何使用：** 调用 `canRedo()` 读取当前值；它不会修改应用状态。

### `[read-only] canUndo : bool`

**作用与语义：**

该属性决定该堆栈是否能撤销。
该属性表明是否存在可撤销的命令。

**如何使用：** 调用 `canUndo()` 读取当前值；它不会修改应用状态。

### `[read-only] clean : bool`

**作用与语义：**

该属性表示该堆栈的清洁状态。
该属性表示栈是否干净。例如，当文档被保存时，栈是干净的。

**如何使用：** 调用 `clean()` 读取当前值；它不会修改应用状态。

### `[read-only] redoText : QString`

**作用与语义：**

该属性包含下一个重新执行命令的重做文本。
该属性包含命令文本，下一次调用`redo()`时将重新执行。

**如何使用：** 调用 `redoText()` 读取当前值；它不会修改应用状态。

### `undoLimit : int`

**作用与语义：**

该属性包含该栈中最大命令数量。
当一个栈上的命令数量超过栈的 undoLimit 时，命令会从栈底部删除。宏命令（带有子命令的命令）被视为一个命令。默认值为 0，意味着没有限制。
该属性仅在撤销栈为空时设置，因为将其设置为非空栈可能会删除当前索引的命令。在非空栈上调用 setUndoLimit() 会打印警告，但无反应。

**如何使用：** 调用 `undoLimit()` 读取当前值；它不会修改应用状态。

### `[read-only] undoText : QString`

**作用与语义：**

此属性保存下一个将被撤销的命令的撤销文本。
此属性保存将在下一次调用 `undo()` 时被撤销的命令文本。

**如何使用：** 调用 `undoText()` 读取当前值；它不会修改应用状态。

### `[explicit] QUndoStack::QUndoStack(QObject *parent = nullptr)`

**作用与语义：**

构造一个空的撤销栈，包含父`parent`。栈初始处于清洁状态。如果`parent`是`QUndoGroup`对象，堆栈会自动添加到组中。

### `[virtual noexcept] QUndoStack::~QUndoStack()`

**作用与语义：**

销毁撤销堆栈，删除其上的所有命令。如果堆栈处于`QUndoGroup`中，该堆叠会自动从组中移除。

### `void QUndoStack::beginMacro(const QString &text)`

**作用与语义：**

开始以给定`text`描述组成宏命令。
由指定`text`描述的空命令会被推送到堆栈中。后续推送到堆栈的命令会被附加到空命令的子命令中，直到调用`endMacro()`。
对 beginMacro() 和 `endMacro()` 的调用可以嵌套，但每个调用 beginMacro() 的调用都必须有对应的 `endMacro()` 调用。
在宏编写过程中，栈会被禁用。这意味着：
- `indexChanged()`和`cleanChanged()`不被发射，
- `canUndo()` 和 `canRedo()` 返回为假，
- 调用`undo()`或`redo()`无效，
- 撤销/重做操作被禁用。
当最外层宏调用`endMacro()`时，堆栈被启用并发出相应信号。
该代码等价于：

**官方示例：**

```cpp
 stack.beginMacro("insert red text");
 stack.push(new InsertText(document, idx, text));
 stack.push(new SetColor(document, idx, text.length(), Qt::red));
 stack.endMacro(); // indexChanged() is emitted
```

### `bool QUndoStack::canRedo() const`

**作用与语义：**

如果有可重做的命令，返回`true`;否则返回`false`。
该函数返回`false`栈是否空或栈顶命令已被重执行。
与`index()`同义词 == `count()`。
注意：属性的获取函数可以重做。

### `[signal] void QUndoStack::canRedoChanged(bool canRedo)`

**作用与语义：**

该属性决定了该堆栈是否可以重做。
该属性表明是否存在可重执行的命令。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `canRedo` 的变化，不要把它当作普通函数主动调用。

### `bool QUndoStack::canUndo() const`

**作用与语义：**

如果有可撤销的命令，返回`true`;否则返回`false`。
该函数返回 Stack 是否空，或栈底命令已被撤销时返回 `false`。
与`index()`同义词 == 0。
注意：属性的getter函数canUndo。

### `[signal] void QUndoStack::canUndoChanged(bool canUndo)`

**作用与语义：**

该属性决定该堆栈是否能撤销。
该属性表明是否存在可撤销的命令。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `canUndo` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QUndoStack::cleanChanged(bool clean)`

**作用与语义：**

该属性表示该堆栈的清洁状态。
该属性表示栈是否干净。例如，当文档被保存时，栈是干净的。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `clean` 的变化，不要把它当作普通函数主动调用。

### `int QUndoStack::cleanIndex() const`

**作用与语义：**

返回干净的索引。这是调用`setClean()`的索引。
栈可能没有干净的索引。这种情况发生在保存文档后，部分命令被撤销后推送新命令。由于`push()`在推送新命令前删除所有未完成命令，栈无法再次返回清洁状态。此时，该函数返回 -1。-1 也可以在显式调用 `resetClean()` 后返回。

### `void QUndoStack::clear()`

**作用与语义：**

通过删除命令栈上的所有命令来清除命令栈，并将栈重置为干净状态。
命令不会被撤销或重做；已编辑对象的状态保持不变。
此函数通常在文档内容被放弃时使用。

### `const QUndoCommand *QUndoStack::command(int index) const`

**作用与语义：**

返回一个命令指向`index`的const指针。
该函数返回一个const指针，因为修改命令一旦推送到栈并执行，几乎总会导致文档状态损坏，如果命令后来被撤销或重做。

### `int QUndoStack::count() const`

**作用与语义：**

返回堆栈中的命令数量。宏命令计入一个命令。

### `QAction *QUndoStack::createRedoAction(QObject *parent, const QString &prefix = QString()) const`

**作用与语义：**

用给定`parent`创建`QAction`对象的重做。
触发该动作将导致调用`redo()`。该动作的文本是下一次调用`redo()`时将重新执行的命令文本，前缀为指定`prefix`。如果没有可重做的命令，该动作将被禁用。
如果`prefix`为空，则使用默认模板“Redo %1”代替前缀。Qt 4.8之前，默认使用前缀“Redo”。

### `QAction *QUndoStack::createUndoAction(QObject *parent, const QString &prefix = QString()) const`

**作用与语义：**

用给定`parent`创建一个撤销对象`QAction`。
触发该动作将导致调用`undo()`。该动作的文本是下一次调用`undo()`时将被撤销的命令文本，前缀为指定的`prefix`。如果没有可用的撤销命令，该动作将被禁用。
如果`prefix`为空，则使用默认模板“Undo %1”代替前缀。Qt 4.8之前，默认使用前缀“Undo”。

### `void QUndoStack::endMacro()`

**作用与语义：**

结束宏命令的组合。
如果这是一组嵌套宏中最外层的宏，该函数在整个宏命令中只发出一次`indexChanged()`。

### `int QUndoStack::index() const`

**作用与语义：**

返回当前命令的索引。这是下一次调用`redo()`时执行的命令。它不总是堆栈中最顶的命令，因为可能有部分命令被撤销。

### `[signal] void QUndoStack::indexChanged(int idx)`

**作用与语义：**

每当命令修改文档状态时，该信号都会发出。当命令被撤销或重执行时，就会发生这种情况。当宏命令被撤销或重执行，或调用`setIndex()`时，该信号只发出一次。
`idx` 指定当前命令的索引，即下一次调用 `redo()` 时执行的命令。

### `bool QUndoStack::isClean() const`

**作用与语义：**

该属性表示该堆栈的清洁状态。
该属性表示栈是否干净。例如，当文档被保存时，栈是干净的。

**如何使用：** 调用 `isClean()` 读取当前值；它不会修改应用状态。

### `void QUndoStack::push(QUndoCommand *cmd)`

**作用与语义：**

将`cmd`推送到栈上，或将其与最近执行的命令合并。无论哪种情况，都通过调用其`redo()`函数执行`cmd`。
如果`cmd`的ID不是-1，且ID与最近执行的命令相同，`QUndoStack`会尝试通过调用最近执行命令的`QUndoCommand::mergeWith()`来合并这两个命令。如果`QUndoCommand::mergeWith()`返回`true`，`cmd`将被删除。
调用`QUndoCommand::redo()`，如果适用，调用`QUndoCommand::mergeWith()`后，`QUndoCommand::isObsolete()`将被调用`cmd`或合并命令。如果`QUndoCommand::isObsolete()`返回`true`，那么`cmd`或合并命令将从栈中删除。
在其他情况下`cmd`只是直接推送到堆栈上。
如果在推送`cmd`前撤销了命令，当前命令及其上方的所有命令都会被删除。因此`cmd`总是堆栈中最顶端的命令。
一旦命令被推送，栈就会对它拥有。没有获取者来返回命令，因为执行后修改命令几乎总会导致文档状态损坏。

### `[slot] void QUndoStack::redo()`

**作用与语义：**

通过调用`QUndoCommand::redo()`重新执行当前命令。递增当前命令索引。
如果栈是空的，或者栈顶命令已经被重做，这个函数就不会有任何作用。
如果当前命令的`QUndoCommand::isObsolete()`返回为真，则该命令将从栈中删除。此外，如果干净的索引大于或等于当前命令索引，则干净的索引会被重置。

### `QString QUndoStack::redoText() const`

**作用与语义：**

返回命令文本，下次调用`redo()`时会重新执行。
注意：属性重做文本的获取函数。

### `[signal] void QUndoStack::redoTextChanged(const QString &redoText)`

**作用与语义：**

该属性包含下一个重新执行命令的重做文本。
该属性包含命令文本，下一次调用`redo()`时将重新执行。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `redoText` 的变化，不要把它当作普通函数主动调用。

### `[slot] void QUndoStack::resetClean()`

**作用与语义：**

如果栈是干净的，则保持干净状态并发出`cleanChanged()`。该方法将干净索引重置为 -1。
通常在以下情况下称为，当一份文件已经经过：
- 基于某个模板创建且尚未保存，因此该文档尚未关联任何文件名。
- 从备份文件恢复。
- 在编辑器之外发生更改，且用户未重新加载。

### `[slot] void QUndoStack::setClean()`

**作用与语义：**

将堆栈标记为干净，如果堆栈本身还不干净，则发出`cleanChanged()`。
这通常在保存文档时调用。
每当堆栈通过撤销/重做命令回到该状态时，就会发出信号`cleanChanged()`。当栈离开干净状态时，也会发出该信号。

### `[slot] void QUndoStack::setIndex(int idx)`

**作用与语义：**

反复调用`undo()`或`redo()`，直到当前命令索引达到`idx`。该函数可用于向前或向后滚动文档状态。`indexChanged()`只发出一次。

### `QString QUndoStack::text(int idx) const`

**作用与语义：**

返回命令文本，索引为`idx`。

### `[slot] void QUndoStack::undo()`

**作用与语义：**

通过调用`QUndoCommand::undo()`，撤销当前命令下方的命令。递减当前命令索引。
如果堆栈是空的，或者栈底命令已经被撤销，这个函数就不会有任何作用。
命令撤销后，如果返回`QUndoCommand::isObsolete()`返回`true`，则该命令将从栈中删除。此外，如果干净索引大于或等于当前命令索引，则清理索引会被重置。

### `QString QUndoStack::undoText() const`

**作用与语义：**

返回命令文本，下一次调用`undo()`时会被撤销。
注意：属性的获取函数可撤销文本。

### `[signal] void QUndoStack::undoTextChanged(const QString &undoText)`

**作用与语义：**

此属性保存下一个将被撤销的命令的撤销文本。
此属性保存将在下一次调用 `undo()` 时被撤销的命令文本。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `undoText` 的变化，不要把它当作普通函数主动调用。

### `bool isActive() const`

**作用与语义：**

该属性表示该堆栈的活跃状态。
应用程序通常有多个撤销栈，每个打开的文档对应一个。活跃栈是与当前活跃文档关联的栈。如果栈属于某个`QUndoGroup`，调用`QUndoGroup::undo()`或`QUndoGroup::redo()`的调用会在该栈活跃时被转发到该栈。如果`QUndoGroup`被`QUndoView`监控，视图会显示该栈在激活时的内容。如果栈不属于`QUndoGroup`，激活无效。
程序员负责通过调用 setActive() 指定哪个栈处于激活状态，通常是在相关文档窗口获得焦点时。

**如何使用：** 调用 `isActive()` 读取当前值；它不会修改应用状态。

### `void setUndoLimit(int limit)`

**作用与语义：**

该属性包含该栈中最大命令数量。
当一个栈上的命令数量超过栈的 undoLimit 时，命令会从栈底部删除。宏命令（带有子命令的命令）被视为一个命令。默认值为 0，意味着没有限制。
该属性仅在撤销栈为空时设置，因为将其设置为非空栈可能会删除当前索引的命令。在非空栈上调用 setUndoLimit() 会打印警告，但无反应。

**如何使用：** 调用 `setUndoLimit(...)` 修改 `undoLimit`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `int undoLimit() const`

**作用与语义：**

该属性包含该栈中最大命令数量。
当一个栈上的命令数量超过栈的 undoLimit 时，命令会从栈底部删除。宏命令（带有子命令的命令）被视为一个命令。默认值为 0，意味着没有限制。
该属性仅在撤销栈为空时设置，因为将其设置为非空栈可能会删除当前索引的命令。在非空栈上调用 setUndoLimit() 会打印警告，但无反应。

**如何使用：** 调用 `undoLimit()` 读取当前值；它不会修改应用状态。

### `void setActive(bool active = true)`

**作用与语义：**

该属性表示该堆栈的活跃状态。
应用程序通常有多个撤销栈，每个打开的文档对应一个。活跃栈是与当前活跃文档关联的栈。如果栈属于某个`QUndoGroup`，调用`QUndoGroup::undo()`或`QUndoGroup::redo()`的调用会在该栈活跃时被转发到该栈。如果`QUndoGroup`被`QUndoView`监控，视图会显示该栈在激活时的内容。如果栈不属于`QUndoGroup`，激活无效。
程序员负责通过调用 setActive() 指定哪个栈处于激活状态，通常是在相关文档窗口获得焦点时。

**如何使用：** 调用 `setActive(...)` 修改 `active`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QUndoStack` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
