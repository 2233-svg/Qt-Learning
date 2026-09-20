# QUndoView

> Qt 6.11.1 · Qt Widgets · 来自 `QUndoView`

## 1. 先建立直觉

`QUndoView` 是撤销栈的可视化列表。它把 `QUndoStack` 里的命令历史显示出来，让用户看到“我做过什么、当前停在哪一步、保存点在哪里”。

它不是撤销系统本身。真正记录操作的是 `QUndoCommand` 和 `QUndoStack`；多个文档之间切换当前撤销栈时用 `QUndoGroup`；`QUndoView` 只是给这套系统一个可浏览、可点击的界面。

## 2. 类说明

`QUndoView` 继承自 `QListView`。它内部使用 undo stack/group 提供的模型，显示命令文本、当前位置和 clean 状态。用户在视图中选择某一项时，可以把栈移动到对应命令位置，从而批量撤销或重做到那一步。

这让它特别适合创作类软件：图像编辑器、文档编辑器、CAD、流程编排器、设计器都需要让用户理解操作历史，而不只是按 `Ctrl+Z` 盲退。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QUndoView(QWidget *)` | 创建空的撤销历史视图，之后用 `setStack()` 或 `setGroup()` 绑定。 |
| `QUndoView(QUndoStack *, QWidget *)` | 直接观察一个撤销栈，适合单文档应用。 |
| `QUndoView(QUndoGroup *, QWidget *)` | 观察一个撤销组，适合多文档应用随当前文档切换。 |
| `setStack(QUndoStack *)` / `stack()` | 绑定或读取当前观察的撤销栈。 |
| `setGroup(QUndoGroup *)` / `group()` | 绑定或读取当前观察的撤销组。 |
| `setCleanIcon(const QIcon &)` / `cleanIcon()` | 设置保存点图标，用来标记 clean state。 |
| `setEmptyLabel(const QString &)` / `emptyLabel()` | 设置栈为空时顶部项文本，例如“初始状态”。 |
| `QListView` 相关 API | 可继续配置选择模式、委托、滚动条和尺寸策略。 |

## 4. 关键用法

单文档应用：

```cpp
auto *stack = new QUndoStack(this);
auto *view = new QUndoView(stack, this);
view->setEmptyLabel(tr("Initial state"));
view->setCleanIcon(QIcon(":/icons/saved.svg"));
```

多文档应用更适合用 `QUndoGroup`：

```cpp
auto *group = new QUndoGroup(this);
auto *history = new QUndoView(group, this);

connect(tabWidget, &QTabWidget::currentChanged, this, [=](int index) {
    group->setActiveStack(documentAt(index)->undoStack());
});
```

这样历史视图会跟随当前文档切换，不需要每个文档单独维护一个可见列表。

## 5. 使用场景

适合图形编辑器、富文本编辑器、节点编辑器、表单设计器、乐谱/时间轴工具、地图编辑器、工程配置器，以及任何需要让用户审视历史步骤的复杂编辑界面。

如果应用只有少量简单撤销操作，菜单里的 Undo/Redo 动作可能就足够。`QUndoView` 的意义在于把历史暴露出来，而不是为了实现撤销。

## 6. 常见坑与经验

命令文本质量会直接决定 `QUndoView` 是否有用。`QUndoCommand::setText()` 不要写成“Changed”，而应写“Move rectangle”、“Rename layer”、“Delete node”这类用户能理解的动作。

clean 状态通常对应“已保存”。保存文件后调用 `QUndoStack::setClean()`，`QUndoView` 才能用 `cleanIcon` 给用户一个明确标记。

不要把 `QUndoView` 当日志。撤销栈应该记录可撤销的用户操作，不应塞入后台同步、自动刷新、网络状态变化等不可撤销事件。
