# QAccessibleSelectionInterface

> Qt 6.11.1 · Qt GUI · 来自 `QAccessibleSelectionInterface`

## 1. 先建立直觉

`QAccessibleSelectionInterface` 描述一个对象内部“可选择子项”的选择状态和选择操作。它适合列表、图标网格、标签集合、缩略图墙、绘图画布中的对象等非文本选择；文本选择应使用 `QAccessibleTextInterface`。

这个接口让辅助技术能查询当前选中了哪些项目，并通过语音、键盘或自动化命令改变选择。它不负责表格行列语义；表格应同时考虑 `QAccessibleTableInterface` 和单元格接口。

## 2. 类说明

- 头文件：`#include <QAccessibleSelectionInterface>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 来源类：可访问子接口；Qt 6.5 起可通过 `QAccessibleInterface::selectionInterface()` 获取。
- 适用对象：支持子项选择的容器，不是单个复选框或文本编辑器。

接口返回和接收的是 `QAccessibleInterface *` 子项。实现必须能把这些接口映射回真实模型项，并在模型变化后避免使用失效指针。

## 3. API 速查

| API | 用途 |
|---|---|
| `selectedItemCount()` | 返回当前选中项目数。 |
| `selectedItems()` | 返回所有选中项目接口。 |
| `selectedItem(selectionIndex)` | 返回选择列表中的第 n 项。 |
| `isSelected(childItem)` | 判断给定子项是否选中。 |
| `select(childItem)` | 选择某子项；单选模型可替换现有选择。 |
| `unselect(childItem)` | 取消某子项选择。 |
| `clear()` | 清空选择。 |
| `selectAll()` | 选择所有可选择子项。 |

## 4. 关键用法

```cpp
bool AccessibleTagList::select(QAccessibleInterface *childItem)
{
    const int index = indexOfAccessibleTag(childItem);
    if (index < 0 || !tagModel()->isSelectable(index))
        return false;

    tagModel()->select(index);
    QAccessibleEvent event(object(), QAccessible::Selection);
    QAccessible::updateAccessibility(&event);
    return tagModel()->isSelected(index);
}
```

操作应走真实选择模型，而不是只改无障碍层缓存。这样键盘焦点、视觉高亮、信号、撤销和无障碍通知才能保持同一套状态。

`selectedItem(selectionIndex)` 中的 `selectionIndex` 是“当前选择列表里的第几个”，不等同于 `QAccessibleInterface::child(index)` 的子索引。比如第 2、7、9 个子项被选中时，`selectedItem(1)` 应返回第 7 个子项，而不是容器的第 1 个孩子。

## 5. 使用场景

| 场景 | 实现建议 |
|---|---|
| 单选列表或标签栏 | `select()` 替换当前选择，`clear()` 可能受业务限制。 |
| 多选网格或缩略图视图 | 支持 `selectAll()`、`clear()` 和增量选择。 |
| 图形编辑画布 | 为可选择图元暴露虚拟子项，返回稳定接口。 |
| 文本编辑器中的文字选区 | 不用此接口，改用文本接口的选择 API。 |
| 表格行列/单元格选择 | 同时实现表格接口，保持行列查询一致。 |

## 6. 常见坑与经验

- `selectedItems()` 返回大量项目可能很贵；如果选择量很大，应高效重写 `selectedItem()`，避免每次都构造完整列表。
- 只读或不可选择项不应被 `selectAll()` 选中。
- 返回值表示操作是否成功达到目标状态。不要无条件返回 true。
- 模型重置、过滤或排序后，旧子项接口可能失效；查询时要基于当前模型重新解析。
- 选择变化后应发送适当的 `Selection`、`SelectionAdd`、`SelectionRemove` 或 `SelectionWithin` 事件。
- 单选容器也可以实现该接口，但必须清楚说明 `select()` 会替换旧选择。

## 7. 知识点覆盖

- 非文本子项选择的无障碍协议
- 选择列表索引与可访问子索引的区别
- 单选、多选、全选和清空的语义
- 虚拟子项、模型变化与接口有效期
- 选择事件与视觉/业务状态同步
