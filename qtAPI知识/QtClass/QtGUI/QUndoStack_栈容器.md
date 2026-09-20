# QUndoStack 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QUndoStack>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QObject`

## 1. 它解决什么问题

`QUndoStack` 保存一串已经应用到文档上的 `QUndoCommand`，并维护“当前 index”。index 下方是已经执行、可撤销的命令；index 及其上方是已经撤销、可重做的命令。它解决的是编辑器中最经典的状态管理问题：用户连续修改内容后，可以一步步撤回，也可以再重做，并且菜单、工具栏、历史视图和“是否已保存”状态都能自动跟随。

典型场景是文本编辑器、绘图软件、节点编辑器、表格编辑器、地图标注工具和任何需要可逆用户操作的业务配置界面。

## 2. push、index 和命令所有权

新命令通过 `push(QUndoCommand *)` 加入栈。`push()` 会立即调用命令的 `redo()`，然后根据 `id()`/`mergeWith()` 尝试和最近命令压缩，并根据 `isObsolete()` 决定是否删除。命令一旦被 push，栈取得所有权；外部不应再删除或修改它。

如果用户已经 undo 到历史中间，再 push 新命令，当前 index 之上的 redo 分支会被删除，新命令成为栈顶。这和多数编辑器一致：回到过去后做新修改，旧的“未来”不再可重做。

```cpp
auto *stack = new QUndoStack(this);
stack->push(new RenameItemCommand(item, "Layer 1"));

connect(stack, &QUndoStack::canUndoChanged, undoButton, &QWidget::setEnabled);
connect(stack, &QUndoStack::cleanChanged, this, &DocumentWindow::setSavedState);
```

## 3. 撤销、重做、宏和压缩

`undo()` 会撤销 index 下方的命令并让 index 减一；`redo()` 会重做 index 指向的命令并让 index 加一。`setIndex(idx)` 会重复调用 undo 或 redo，直到到达目标 index，并且 `indexChanged()` 对这次跳转只发出一次。

`beginMacro(text)` 与 `endMacro()` 用来把多条命令合成一个用户动作。宏内部 push 的命令会成为父命令的子命令；外层宏结束时，栈把整个宏看作一个命令。宏可以嵌套，最外层 `endMacro()` 才会恢复整体状态通知。

命令压缩由 `QUndoCommand::id()` 和 `mergeWith()` 决定，适合把连续输入、连续拖动这类细碎变化合并成一次撤销。宏和压缩效果相似，但语义不同：宏保留子命令结构，压缩会把多个同类命令折叠进一个命令对象。

## 4. clean 状态和 UI 动作

clean 状态表示“当前文档状态等同于已保存状态”。保存成功后调用 `setClean()`，之后只要 undo/redo 回到这个 index，`isClean()` 会再次为 true 并发出 `cleanChanged(true)`。如果清洁点所在的命令被新分支或 obsolete 删除，`cleanIndex()` 会变为 `-1`。

`createUndoAction()` 和 `createRedoAction()` 创建可直接放进菜单或工具栏的 `QAction`。这些 action 会自动跟随 `canUndo`、`canRedo`、`undoText`、`redoText` 变化，无命令可执行时禁用。多文档应用里通常配合 `QUndoGroup` 创建全局 action。

## 5. 边界和排查

`clear()` 会删除栈内所有命令并回到 clean 状态，但不会对文档执行 undo/redo。它适合“放弃当前历史，从此刻重新开始记录”，不适合“撤销所有修改”。

`command(index)` 返回 const 指针，因为命令已经执行后再修改内部数据很容易让后续 undo/redo 与文档状态不一致。需要检查历史时只读即可；要改变历史，应通过新的命令、清空栈或业务层重建。

`undoLimit` 必须在栈为空时设置才可靠；它限制栈保存的命令数量，适合防止大文档或图形操作占用过多内存。宏命令按一个命令计数。

## API 速查表

| API | 用途与关键语义 | 边界、默认值或注意事项 |
| --- | --- | --- |
| `active : bool` | 表示该栈是否是所属 `QUndoGroup` 的活动栈。 | 不属于任何 group 时设置 active 没有实际转发效果。 |
| `undoLimit : int` | 限制栈中保存的命令数量。 | 应在空栈时设置；宏命令按一个命令计数。 |
| `canUndo : bool` | 只读属性，表示当前是否有命令可撤销。 | 由 index 和命令状态决定，监听 `canUndoChanged` 更新 UI。 |
| `canRedo : bool` | 只读属性，表示当前是否有命令可重做。 | 监听 `canRedoChanged`。 |
| `undoText : QString` | 只读属性，下一次 undo 的命令文本。 | 无可撤销命令时通常为空。 |
| `redoText : QString` | 只读属性，下一次 redo 的命令文本。 | 无可重做命令时通常为空。 |
| `clean : bool` | 只读属性，表示当前 index 是否等于 clean index。 | 常用于启用保存按钮或标题星号。 |
| `QUndoStack(QObject *parent = nullptr)` | 创建空撤销栈。 | 若 parent 是 `QUndoGroup`，栈会隐式加入该组。 |
| `~QUndoStack()` | 销毁栈并删除持有的命令。 | 命令归栈所有后不要外部重复删除。 |
| `push(QUndoCommand *cmd)` | 加入命令并立即执行其 `redo()`。 | 会删除 redo 分支；可能合并或删除 obsolete 命令。 |
| `undo()` | 撤销当前 index 下方的命令。 | 空栈或已到最底部时无操作；可能删除 obsolete 命令。 |
| `redo()` | 重做 index 指向的命令。 | 已在栈顶时无操作；可能删除 obsolete 命令。 |
| `setIndex(int idx)` | 跳转到指定历史 index。 | 通过反复 undo/redo 实现；`indexChanged()` 只发一次。 |
| `index() const` | 返回当前命令 index，也就是下一次 redo 的位置。 | 栈顶已重做时 `index() == count()`。 |
| `count() const` | 返回栈中命令数。 | 宏命令算一个。 |
| `command(int index) const` | 返回指定命令的 const 指针。 | 不要修改已压栈命令；索引必须有效。 |
| `text(int idx) const` | 返回指定命令文本。 | 常用于自定义历史列表。 |
| `canUndo() const` / `canRedo() const` | 查询是否可撤销/重做。 | UI 应优先响应对应信号。 |
| `undoText() const` / `redoText() const` | 查询下一步动作文本。 | 用于按钮、菜单和状态提示。 |
| `createUndoAction(QObject *, const QString &prefix = QString())` | 创建自动跟随栈状态的 Undo action。 | 无可撤销命令时禁用；默认文案形如 `Undo %1`。 |
| `createRedoAction(QObject *, const QString &prefix = QString())` | 创建自动跟随栈状态的 Redo action。 | 无可重做命令时禁用；默认文案形如 `Redo %1`。 |
| `beginMacro(const QString &text)` | 开始组合宏命令。 | 必须与 `endMacro()` 成对；宏内命令成为子命令。 |
| `endMacro()` | 结束宏命令组合。 | 嵌套宏只有最外层结束时整体通知一次。 |
| `setClean()` | 将当前 index 标记为 clean。 | 通常在保存成功后调用。 |
| `resetClean()` | 离开 clean 状态并把 clean index 重置为 `-1`。 | 适合新建未保存、从备份恢复或外部变更未重载等情况。 |
| `isClean() const` | 返回当前是否 clean。 | 等价于 `clean` 属性 getter。 |
| `cleanIndex() const` | 返回 clean index。 | 不存在可返回的 clean 点时为 `-1`。 |
| `clear()` | 删除所有命令并回到 clean 状态。 | 不会撤销或重做文档，只清历史。 |
| `setUndoLimit(int limit)` / `undoLimit() const` | 设置或读取命令数量上限。 | 非空栈中调整限制可能不符合预期，应尽早设置。 |
| `setActive(bool active = true)` / `isActive() const` | 设置或读取该栈在 group 中是否活动。 | 多文档程序通常在窗口获得焦点时调用。 |
| `indexChanged(int)` | 当前 index 变化时发出。 | 宏或 `setIndex()` 场景中会合并通知。 |
| `cleanChanged(bool)` | clean 状态变化时发出。 | 用于保存状态 UI。 |
| `canUndoChanged(bool)` / `canRedoChanged(bool)` | 可撤销/可重做状态变化时发出。 | 直接连接到 action/button 的 enabled 状态很常见。 |
| `undoTextChanged(const QString &)` / `redoTextChanged(const QString &)` | 下一步 undo/redo 文本变化时发出。 | 创建的 action 会自动使用这些变化。 |

## 6. 记忆重点

`QUndoStack` 的状态可以用 `index` 理解：index 下方可 undo，上方可 redo。`push()` 会立刻 `redo()` 并取得命令所有权；clean 状态只是一枚 index 标记；宏、压缩和 obsolete 分别解决“组合动作”“合并细碎动作”“删除无意义动作”三个不同问题。
