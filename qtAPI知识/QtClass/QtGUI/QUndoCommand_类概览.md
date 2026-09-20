# QUndoCommand 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QUndoCommand>`  
> 所属模块：`Qt6::Gui`

## 1. 它解决什么问题

`QUndoCommand` 是 Qt Undo Framework 中的“一个可撤销操作”。它把一次编辑动作拆成两段：`redo()` 负责应用动作，`undo()` 负责撤回动作。`QUndoStack` 只负责调度、合并、删除和暴露状态；真正如何修改文档、场景、模型或业务对象，由具体的 `QUndoCommand` 派生类实现。

适合封装插入文字、移动图元、改变颜色、重命名节点、调整属性、批量操作等用户可理解的编辑动作。它不是 `QObject`，没有信号槽和父子对象树；它自己的 parent 是“宏命令父子关系”，不是 QObject parent。

## 2. 基本实现方式

命令对象通常在构造时记录足够的上下文，在 `redo()` 中执行修改，在 `undo()` 中根据保存的数据恢复原状态。重要边界是：`QUndoStack::push()` 会立即调用命令的 `redo()`，因此不要在 push 前先手动把同一修改应用一遍。

```cpp
class RenameItemCommand : public QUndoCommand
{
public:
    RenameItemCommand(Item *item, QString after)
        : m_item(item), m_before(item->name()), m_after(std::move(after))
    {
        setText("rename item");
    }

    void redo() override { m_item->setName(m_after); }
    void undo() override { m_item->setName(m_before); }

private:
    Item *m_item;
    QString m_before;
    QString m_after;
};
```

`redo()` 和 `undo()` 内部不能再调用同一个栈的 `push()`、`undo()` 或 `redo()`，否则会破坏栈的状态机。命令执行期间应只修改自己的目标对象。

## 3. 所有权、宏命令和压缩

命令被 `QUndoStack::push()` 接收后，栈取得所有权。栈在清空、析构、丢弃 redo 分支、合并命令或删除 obsolete 命令时会释放它。命令压栈后不应再通过外部裸指针修改命令内容；如果命令持有业务对象指针，业务对象的生命周期要由应用自己保证。

构造命令时传入另一个 `QUndoCommand *parent`，当前命令会成为父命令的子命令，并由父命令释放。父命令可作为宏命令：默认 `redo()` 会按子命令顺序调用，默认 `undo()` 会按反序调用。`QUndoStack::beginMacro()`/`endMacro()` 是创建这种父子命令的便利方式。

压缩用于把连续的小命令合成一个命令，例如连续输入字符合成一个“输入单词”。派生类通过重写 `id()` 和 `mergeWith()` 支持压缩：`id()` 默认是 `-1`，表示不参与合并；只有最近已执行命令与新命令 `id()` 相同且不为 `-1` 时，栈才尝试调用 `mergeWith()`。

## 4. 文本、动作和 obsolete

`text()` 是显示在 `QUndoView` 中的命令名称，也会用于 undo/redo action 的文字。`actionText()` 面向 action 文案；如果需要给视图和动作使用不同翻译文本，可在 `setText()` 传入的字符串中用换行分隔两段。

`setObsolete(true)` 表示命令已经没有实际意义，可以从栈中移除。常见例子是移动后又回到原位、网络型命令执行失败且无法撤销/重做。栈会在 `push()`、`undo()`、`redo()`、`setIndex()` 等过程中检查 obsolete 状态并删除命令。

## API 速查表

| API | 用途与关键语义 | 边界、默认值或注意事项 |
| --- | --- | --- |
| `QUndoCommand(QUndoCommand *parent = nullptr)` | 创建无文本命令，可独立压栈或作为子命令。 | `parent` 是命令宏父子关系；不是 QObject parent。 |
| `QUndoCommand(const QString &text, QUndoCommand *parent = nullptr)` | 创建命令并设置用户可见文本。 | 文本应短而能描述用户动作。 |
| `~QUndoCommand()` | 销毁命令并销毁所有子命令。 | 压入栈后通常由 `QUndoStack` 删除，不要手工重复释放。 |
| `redo()` | 应用命令代表的修改。 | `push()` 会立即调用；内部不要调用栈的 `push()`/`undo()`/`redo()`。 |
| `undo()` | 撤销 `redo()` 做过的修改。 | 必须让目标回到 redo 前状态；默认实现会反序撤销子命令。 |
| `text() const` | 返回命令名称，常用于 `QUndoView`。 | 可以与 `actionText()` 不同。 |
| `actionText() const` | 返回 undo/redo action 使用的动作文本。 | `setText()` 中用换行可提供单独 action 文案。 |
| `setText(const QString &)` | 设置命令文本。 | 压栈后再改变文本会影响视图和动作显示，通常在构造时设置。 |
| `id() const` | 返回命令压缩 id。 | 默认 `-1` 表示不参与压缩；可压缩命令应返回同类唯一 id。 |
| `mergeWith(const QUndoCommand *)` | 尝试把新命令合并进当前命令。 | 只有 id 相同且非 `-1` 时才会被栈尝试调用；成功后新命令会被删除。 |
| `isObsolete() const` | 查询命令是否已无实际意义。 | 栈会在若干操作后检查并删除 obsolete 命令。 |
| `setObsolete(bool)` | 标记命令是否 obsolete。 | 删除 obsolete 命令可能导致 clean index 被重置。 |
| `childCount() const` | 返回宏命令的子命令数量。 | 普通命令通常为 0。 |
| `child(int index) const` | 返回指定子命令。 | 返回 const 指针；不要在压栈后修改命令破坏文档状态一致性。 |

## 5. 记忆重点

`QUndoCommand` 的核心契约是“`redo()` 可重做，`undo()` 可恢复”。命令被压栈后归栈或父命令所有；压缩靠 `id()`/`mergeWith()`，宏命令靠子命令，空操作靠 obsolete 移除。
