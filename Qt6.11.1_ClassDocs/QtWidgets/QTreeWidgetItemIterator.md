# QTreeWidgetItemIterator

> Qt 6.11.1 · Qt Widgets · 来自 `QTreeWidgetItemIterator`

## 1. 先建立直觉

`QTreeWidgetItemIterator` 是 `QTreeWidget` 的项目遍历器。它让你从整棵树或某个节点开始，按树结构依次访问 `QTreeWidgetItem`，并且可以只遍历满足条件的项，比如选中项、隐藏项、可编辑项、已勾选项。

它服务的是 item-based 树控件。如果你的树来自 `QTreeView` + `QAbstractItemModel`，应使用模型索引递归遍历，而不是这个迭代器。

## 2. 类说明

`QTreeWidgetItemIterator` 是轻量迭代器类型，不是 `QObject`，也不是控件。它持有对树项目结构的遍历状态，解引用得到当前 `QTreeWidgetItem *`。

遍历期间要谨慎修改树结构。读取、改文本、改勾选状态通常没问题；删除当前项、移动节点、清空树可能让迭代状态失效。需要删除时，先收集指针或路径，再统一处理会更稳。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QTreeWidgetItemIterator(QTreeWidget *, flags)` | 从整个树控件开始遍历。 |
| `QTreeWidgetItemIterator(QTreeWidgetItem *, flags)` | 从某个项目子树开始遍历。 |
| `IteratorFlag::All` | 遍历所有项目。 |
| `Hidden` / `NotHidden` | 只遍历隐藏或非隐藏项目。 |
| `Selected` / `Unselected` | 只遍历选中或未选中项目。 |
| `Checked` / `NotChecked` | 按勾选状态过滤。 |
| `Enabled` / `Disabled` | 按是否启用过滤。 |
| `Editable` / `NotEditable` | 按是否可编辑过滤。 |
| `HasChildren` / `NoChildren` | 按是否有子项过滤。 |
| `operator*()` | 取得当前 `QTreeWidgetItem *`；为空表示遍历结束。 |
| `operator++()` / `operator++(int)` | 前进到下一个匹配项。 |
| `operator--()` / `operator--(int)` | 后退到上一个匹配项。 |
| `operator+=(int)` / `operator-=(int)` | 一次移动多个匹配项。 |

## 4. 关键用法

遍历所有已选项目：

```cpp
QTreeWidgetItemIterator it(tree, QTreeWidgetItemIterator::Selected);
while (*it) {
    processSelectedItem(*it);
    ++it;
}
```

批量勾选可见项目：

```cpp
QTreeWidgetItemIterator it(tree, QTreeWidgetItemIterator::NotHidden);
while (*it) {
    (*it)->setCheckState(0, Qt::Checked);
    ++it;
}
```

从某个节点开始只处理子树：

```cpp
QTreeWidgetItemIterator it(rootItem, QTreeWidgetItemIterator::Editable);
while (*it) {
    validateEditableItem(*it);
    ++it;
}
```

## 5. 使用场景

适合设置树、权限树、文件分类树、测试用例树、检查项树中做批量读取或批量更新，尤其是“只处理选中/勾选/可见项目”的操作。

如果数据规模很大，或者树只是模型数据的一个视图，优先考虑模型层遍历。`QTreeWidgetItemIterator` 方便，但它和 `QTreeWidgetItem` 体系绑定较紧。

## 6. 常见坑与经验

循环条件应写 `while (*it)`，不要先解引用再判断。尾后状态没有有效 item。

过滤标志是遍历时筛选，不是结果快照。遍历过程中修改某些状态，例如隐藏或勾选，可能影响后续匹配结果；复杂批量操作建议先收集目标列表。

不要在遍历中直接删除当前 item 后继续 `++it`。删除会改变树结构，最稳的做法是先把要删的项存到 `QList<QTreeWidgetItem *>`，遍历结束后再删除。
