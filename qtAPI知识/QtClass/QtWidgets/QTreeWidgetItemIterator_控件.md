# QTreeWidgetItemIterator：按前序遍历 QTreeWidgetItem

> Qt 6.11.1 · `#include <QTreeWidgetItemIterator>` · 模块：`Qt6::Widgets`

`QTreeWidgetItemIterator` 用来遍历 `QTreeWidget` 或某个 `QTreeWidgetItem` 子树中的节点。遍历顺序是前序：先访问父节点，再访问其子节点。

## 使用场景

适合在 convenience tree 中查找、批量设置可见性、选中状态、勾选状态或收集节点。构造时可传过滤 flags，只遍历隐藏/未隐藏、选中/未选中、可编辑、已勾选、有子节点等节点。

遍历时不要随意删除当前 item 或大幅重排树结构；需要修改结构时，先收集指针或数据，再进行修改。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QTreeWidgetItemIterator(QTreeWidget *widget, flags = All)` | 从树的第一个顶层匹配项开始遍历。 |
| `QTreeWidgetItemIterator(QTreeWidgetItem *item, flags = All)` | 从指定 item 或下一个匹配项开始遍历其所在序列。 |
| 拷贝构造 / `operator=` | 复制迭代器当前位置和过滤规则。 |
| `operator*() const` | 返回当前 item；到末尾时为 `nullptr`。 |
| `operator++()` / `operator++(int)` | 前进到下一个匹配项。 |
| `operator--()` / `operator--(int)` | 后退到上一个匹配项。 |
| `operator+=(int n)` / `operator-=(int n)` | 向前或向后跳过 n 个匹配项；负数反向。 |
| `All` | 不过滤，遍历所有项。 |
| `Hidden` / `NotHidden` | 按隐藏状态过滤。 |
| `Selected` / `Unselected` | 按选择状态过滤。 |
| `Checked` / `NotChecked` | 按勾选状态过滤。 |
| `Enabled` / `Disabled` | 按启用状态过滤。 |
| `Editable` / `NotEditable` | 按可编辑状态过滤。 |
| `HasChildren` / `NoChildren` | 按是否有子项过滤。 |
| `UserFlag` | 用户自定义过滤标志的起始位。 |
