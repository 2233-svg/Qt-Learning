# QUndoStack
> Qt 6.11.1 · Qt GUI · 来自 `QUndoStack`

## 1. 先建立直觉

`QUndoStack` 是撤销命令的时间线。你把 `QUndoCommand` push 进去，它执行 redo；用户点击撤销，它调用 undo；再点击重做，它再 redo。

它还维护 clean 状态、当前 index、undo/redo action 文本，非常适合文档类应用。

## 2. 类说明

- 头文件：`#include <QUndoStack>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QObject`
- 协作类：`QUndoCommand`、`QUndoGroup`

stack 拥有其中的 command。清空 stack 或销毁 stack 会删除命令。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `push(command)` | 加入命令并立即 redo |
| `undo()` / `redo()` | 撤销和重做 |
| `canUndo()` / `canRedo()` | 是否可撤销/重做 |
| `undoText()` / `redoText()` | 下一个撤销/重做动作文本 |
| `createUndoAction()` / `createRedoAction()` | 创建可自动更新文本和 enabled 的 QAction |
| `beginMacro()` / `endMacro()` | 合并多条命令为一个用户动作 |
| `setClean()` / `isClean()` / `cleanIndex()` | 文档保存状态 |
| `index()` / `setIndex()` | 当前历史位置 |
| `count()` / `command(i)` | 查看命令数量和指定命令 |
| `clear()` | 清空历史 |
| `setUndoLimit()` / `undoLimit()` | 限制命令数量 |
| `canUndoChanged` 等信号 | 监听动作状态和 clean 状态 |

## 4. 关键用法

```cpp
auto *undoAction = stack->createUndoAction(this, tr("&Undo"));
auto *redoAction = stack->createRedoAction(this, tr("&Redo"));
editMenu->addAction(undoAction);
editMenu->addAction(redoAction);
```

保存文件后：

```cpp
saveDocument();
stack->setClean();
```

之后 `cleanChanged(false)` 就能驱动窗口标题的 `*` 标记。

## 5. 使用场景

- 文档窗口撤销重做。
- 图形编辑器命令历史。
- 属性修改和批量操作。
- 多步宏操作，如“插入模板”。
- 保存状态追踪。

## 6. 常见坑与经验

- `push()` 后会丢弃当前 index 之后的 redo 分支，这是线性历史，不是分叉历史。
- `beginMacro()` 后到 `endMacro()` 前不要提前返回，否则栈状态会错。
- `setUndoLimit()` 应在栈为空时设置最稳。
- 不要把每次鼠标移动都作为独立命令，使用 merge 或拖动结束后生成一个命令。

## 7. 知识点覆盖

撤销栈、线性历史、clean 状态、action 自动更新、宏命令、撤销限制、信号驱动 UI。
