# QUndoGroup 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QUndoGroup>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QObject`

## 1. 它解决什么问题

`QUndoGroup` 把多个 `QUndoStack` 组织成“当前活动文档的撤销栈”。在多文档编辑器、MDI 程序、标签页编辑器或多个独立画布同时存在的应用里，用户界面通常只有一组 Undo/Redo 菜单和工具栏按钮，但每个文档都有自己的撤销历史。`QUndoGroup` 负责把这组全局动作转发到当前活动的那个栈。

它不替代 `QUndoStack` 保存命令，也不保存文档内容；它只维护栈集合、活动栈和相关状态信号。

## 2. 活动栈模型

一个组里同一时刻最多有一个活动栈。调用 `undo()` 或 `redo()` 时，组会转发给 `activeStack()`；没有活动栈时这些槽什么也不做。`canUndo()`、`canRedo()`、`undoText()`、`redoText()`、`isClean()` 等查询也都来自活动栈；没有活动栈时返回安全的空状态。

常见用法是在文档窗口获得焦点时切换活动栈：

```cpp
void DocumentWindow::focusInEvent(QFocusEvent *event)
{
    m_undoStack->setActive(true);
    QWidget::focusInEvent(event);
}
```

也可以直接调用 `group->setActiveStack(stack)`，但目标栈必须已经属于这个组，否则调用无效。

## 3. 所有权和多组边界

`addStack()` 不取得栈的所有权。栈需要由文档对象、窗口对象或普通 QObject parent 关系管理。若把 `QUndoGroup` 作为 `QUndoStack` 的 QObject parent 创建栈，栈会按 QObject 规则随组销毁，同时也会隐式加入组。

一个 `QUndoStack` 只能属于一个 `QUndoGroup`。把同一个栈加入另一个组，会先从旧组移除。栈析构时会自动从所属组移除；如果它正是活动栈，组的活动栈会变为空并发出相应状态信号。

## 4. 和 QAction、QUndoView 协作

`createUndoAction()` 与 `createRedoAction()` 创建的 `QAction` 始终跟随活动栈：可用状态、显示文本和触发行为都会随着活动栈变化而更新。这样菜单栏只需要持有一对 action，而不必在切换文档时手动重连每个栈。

`QUndoView` 也可以观察 `QUndoGroup`。当活动栈变化时，视图显示对应文档的命令历史，适合多文档编辑器的“历史”面板。

## API 速查表

| API | 用途与关键语义 | 边界、默认值或注意事项 |
| --- | --- | --- |
| `QUndoGroup(QObject *parent = nullptr)` | 创建空的撤销栈组。 | 是 `QObject`；可用 parent 管理组自身生命周期。 |
| `~QUndoGroup()` | 销毁组。 | 不会删除通过 `addStack()` 加入且无 QObject parent 关系的栈。 |
| `addStack(QUndoStack *stack)` | 把栈加入组。 | 组不取得所有权；同一栈加入新组会脱离旧组。 |
| `removeStack(QUndoStack *stack)` | 从组中移除栈。 | 若移除的是活动栈，活动栈变为 `nullptr`。 |
| `stacks() const` | 返回组内栈列表。 | 返回的是指针列表，不代表调用方拥有这些栈。 |
| `activeStack() const` | 返回当前活动栈。 | 组为空或没有活动栈时返回 `nullptr`。 |
| `setActiveStack(QUndoStack *stack)` | 将组内某个栈设为活动栈。 | `stack` 不属于当前组时调用无效；等价于对栈调用 `setActive(true)`。 |
| `undo()` | 对活动栈调用 `QUndoStack::undo()`。 | 没有活动栈时什么也不做。 |
| `redo()` | 对活动栈调用 `QUndoStack::redo()`。 | 没有活动栈时什么也不做。 |
| `canUndo() const` | 返回活动栈是否可撤销。 | 没有活动栈时返回 `false`。 |
| `canRedo() const` | 返回活动栈是否可重做。 | 没有活动栈时返回 `false`。 |
| `undoText() const` | 返回活动栈下一次 undo 的命令文本。 | 没有活动栈时返回空字符串。 |
| `redoText() const` | 返回活动栈下一次 redo 的命令文本。 | 没有活动栈时返回空字符串。 |
| `isClean() const` | 查询活动栈是否处于 clean 状态。 | 没有活动栈时返回 `true`，便于禁用保存提示。 |
| `createUndoAction(QObject *, const QString &prefix = QString())` | 创建跟随活动栈的 Undo action。 | 无可撤销命令、组为空或无活动栈时 action 会禁用。 |
| `createRedoAction(QObject *, const QString &prefix = QString())` | 创建跟随活动栈的 Redo action。 | `prefix` 为空时使用 Qt 默认 “Redo %1” 文案。 |
| `activeStackChanged(QUndoStack *)` | 活动栈变化时发出。 | 参数可为 `nullptr`。 |
| `indexChanged(int)` | 活动栈 index 变化或活动栈切换时发出。 | 无活动栈时状态按 0 表示。 |
| `cleanChanged(bool)` | 活动栈 clean 状态变化或活动栈切换时发出。 | 无活动栈时参数为 `true`。 |
| `canUndoChanged(bool)` / `canRedoChanged(bool)` | 活动栈可撤销/可重做状态变化时发出。 | 活动栈切换也会触发。 |
| `undoTextChanged(const QString &)` / `redoTextChanged(const QString &)` | 活动栈动作文本变化时发出。 | 无活动栈时文本为空。 |

## 5. 记忆重点

`QUndoGroup` 是多文档 Undo/Redo 的路由器。它不拥有通过 `addStack()` 加入的栈，也不存命令；所有查询、action 和槽调用都以当前活动栈为准。
