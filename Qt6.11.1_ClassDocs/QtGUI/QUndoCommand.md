# QUndoCommand
> Qt 6.11.1 · Qt GUI · 来自 `QUndoCommand`

## 1. 先建立直觉

`QUndoCommand` 是撤销系统里的一个操作节点。一次用户动作对应一个 command，里面实现 `redo()` 和 `undo()`。`QUndoStack` 负责按顺序执行、撤销、重做这些 command。

它适合把“修改模型数据”包装成可回退的业务动作，而不是把界面按钮点击本身塞进去。

## 2. 类说明

- 头文件：`#include <QUndoCommand>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 类型：可继承普通 C++ 类
- 协作类：`QUndoStack`、`QUndoGroup`

command 被 push 到 stack 后，所有权交给 stack。不要把同一个 command 放进多个 stack。

## 3. API 速查

| API | 作用 |
| --- | --- |
| 构造函数 | 可设置文本和父 command |
| `redo()` | 执行或重做操作，子类重写 |
| `undo()` | 撤销操作，子类重写 |
| `text()` / `setText()` | 菜单和 action 显示文本 |
| `actionText()` | 适合 undo/redo action 的文本 |
| `id()` | 命令合并类别，默认不合并 |
| `mergeWith()` | 与后续同类命令合并 |
| `isObsolete()` / `setObsolete()` | 标记无意义命令可被丢弃 |
| `child()` / `childCount()` | 宏命令的子命令 |

## 4. 关键用法

```cpp
class RenameCommand : public QUndoCommand {
public:
    void redo() override { item->setName(newName); }
    void undo() override { item->setName(oldName); }
};

stack->push(new RenameCommand(item, oldName, newName));
```

`push()` 会立即调用 `redo()`，所以构造函数只保存状态，不要在构造函数里真正改数据。

## 5. 使用场景

- 文档编辑、图形编辑器、节点编辑器的操作历史。
- 属性面板修改对象属性。
- 鼠标拖动产生的连续移动命令合并。
- 多个子操作组成一个宏命令。

## 6. 常见坑与经验

- `undo()` 和 `redo()` 必须只修改模型，不要依赖当前 UI 焦点或选择。
- 连续输入文字或拖动时实现 `id()` 与 `mergeWith()`，否则撤销栈会爆炸。
- 空操作或最终无变化的命令应 `setObsolete(true)`。
- command 中保存指针时，要确保目标对象生命周期比命令长，或使用稳定 id 重新查找。

## 7. 知识点覆盖

撤销命令、redo/undo 协议、命令合并、宏命令、所有权、obsolete 命令、业务模型回滚。
