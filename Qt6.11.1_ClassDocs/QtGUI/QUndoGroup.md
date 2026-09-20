# QUndoGroup
> Qt 6.11.1 · Qt GUI · 来自 `QUndoGroup`

## 1. 先建立直觉

`QUndoGroup` 管理多个 `QUndoStack`，并把菜单上的 Undo/Redo 动作路由到当前激活的 stack。多文档应用里，每个文档一个 stack，主窗口只需要一组撤销重做 action。

## 2. 类说明

- 头文件：`#include <QUndoGroup>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QObject`
- 协作类：`QUndoStack`

group 不替文档保存数据，它只负责选择“当前哪个 stack 接收撤销重做”。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `addStack()` / `removeStack()` | 管理栈集合 |
| `stacks()` | 返回所有栈 |
| `activeStack()` / `setActiveStack()` | 当前活动栈 |
| `undo()` / `redo()` | 转发到 active stack |
| `canUndo()` / `canRedo()` | 查询 active stack 状态 |
| `undoText()` / `redoText()` | active stack 的动作文本 |
| `createUndoAction()` / `createRedoAction()` | 创建全局 action |
| `activeStackChanged` 等信号 | 活动栈或状态变化通知 |

## 4. 关键用法

```cpp
undoGroup->addStack(doc->undoStack());
connect(mdiArea, &QMdiArea::subWindowActivated, this, [=](QMdiSubWindow *w) {
    undoGroup->setActiveStack(w ? documentFor(w)->undoStack() : nullptr);
});
```

菜单 action 绑定 group，而不是绑定某个文档。

## 5. 使用场景

- MDI 多文档编辑器。
- 多个 dock/panel 各有独立撤销历史。
- 主窗口全局 Undo/Redo action 自动跟随焦点文档。

## 6. 常见坑与经验

- 文档关闭时记得 `removeStack()` 或让 stack 析构自动脱离。
- 没有 active stack 时 action 应自动 disabled，业务代码也要能处理 nullptr。
- active stack 切换不是保存点切换，clean 状态仍在各自 stack 内。

## 7. 知识点覆盖

多文档撤销、active stack、全局 action 路由、状态信号、stack 生命周期。
