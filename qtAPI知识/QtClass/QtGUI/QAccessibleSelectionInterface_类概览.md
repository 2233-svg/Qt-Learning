# Qt QAccessibleSelectionInterface 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAccessibleSelectionInterface>`  
> 所属模块：`Qt6::Gui`  
> 自 Qt 6.5 引入  
> 定位：查询和修改可访问对象直接子项选择的纯虚接口

## 1. 它解决什么问题

`QAccessibleSelectionInterface` 让辅助技术读取或修改集合对象的选择状态。它适合列表、图标网格、树的当前层、标签栏或其他有可选直接子项的对象。

最重要的限制是：**只支持直接 child 的选择**。它不是跨整棵 accessible 树的通用查询接口，也不是文本选区接口：

- 选择对象必须是实现者的直接 accessible child；
- 文本范围选择由 `QAccessibleTextInterface` 负责；
- `selectedItem(index)` 的 index 是“选中项目列表”里的序号，不是 `child(index)` 的 child 序号；
- 实际选择规则仍由控件决定，单选实现允许 `select()` 替换旧选择。

## 2. 实际使用场景

自定义图标选择器可实现该接口，并通过 `QAccessibleInterface::interface_cast(QAccessible::SelectionInterface)` 暴露：

```cpp
bool IconGridAccessible::select(QAccessibleInterface *item)
{
    const int row = indexOfChild(item);
    if (row < 0 || !grid()->isEnabled())
        return false;

    grid()->setCurrentIndex(row); // 单选时替换原选择
    return true;
}
```

成功修改选择后，控件还应发送合适的无障碍事件，例如 `QAccessible::Selection`、`SelectionAdd`、`SelectionRemove` 或 `SelectionWithin`。接口方法返回 `true` 只说明请求确实改变/完成了选择，不能代替事件通知。

## 3. 选择模型、返回值和性能

接口中的 bool 返回值应严格表示结果：

- `select()`：该 item 是否实际进入选择；
- `unselect()`：该 item 是否实际从选择中移除；
- `clear()`：调用后是否真的已无选中项；
- `selectAll()`：调用后是否所有直接 child 都已选中。

对于单选控件，`select()` 成功时可以替换当前选择；`selectAll()` 是否支持取决于真实控件能力，不能为了实现接口强制改变单选语义。

`selectedItems()` 返回的每个 interface pointer 都是借用。大集合中构造完整 QList 可能昂贵；`selectedItem()` 的默认实现会从列表取第 N 项，若选中项很多，派生类应覆盖它实现更高效的按序访问。

## 4. 有效性与线程边界

传入的 `childItem` 必须属于当前对象的直接 accessible child，并且仍有效。传入 `nullptr`、后代、兄弟、来自别的容器或已失效的 interface 时，应返回 `false`，而不是尝试跨对象修改状态。

选择通常会修改 GUI 控件或模型，因此必须在对象所属线程执行；后台线程只能通过 queued 调用请求 UI 线程完成操作。禁用、只读或过滤导致不可选的 child 也应按实际控件语义拒绝。

## 5. 逐项 API 说明

### `virtual ~QAccessibleSelectionInterface()`

虚析构函数。接口通常由同一 accessible object 实现并通过 `interface_cast()` 暴露；调用方获得的是借用指针，不能删除。

### `virtual int selectedItemCount() const = 0`

返回当前选中的直接 accessible child 总数。应与 `selectedItems().size()` 一致。

### `virtual QList<QAccessibleInterface *> selectedItems() const = 0`

返回当前选中的直接 child 接口列表。列表可以为空；其中的指针不转移所有权，调用方必须处理 child 在后续时刻失效的可能。

### `virtual QAccessibleInterface *selectedItem(int selectionIndex) const`

返回选择列表中第 `selectionIndex` 个 item。默认实现基于 `selectedItems()`；越界时返回 `nullptr`。

该 index 通常不同于 `child(index)` 的 child index。大量选中项时可以覆盖该函数避免每次都构造整个列表。

### `virtual bool isSelected(QAccessibleInterface *childItem) const`

判断指定直接 child 是否已选中。默认实现搜索 `selectedItems()`；对于大选择集可覆盖为模型/哈希查询。

### `virtual bool select(QAccessibleInterface *childItem) = 0`

把直接 child 加入选择，实际加入后返回 `true`。单选实现可以替换当前 selection；不可选、已失效或不属于当前容器的 item 返回 `false`。

### `virtual bool unselect(QAccessibleInterface *childItem) = 0`

从选择中移除直接 child，实际移除后返回 `true`。未选中 item 或不支持取消的选择模型应返回 `false`。

### `virtual bool clear() = 0`

取消所有直接 child 的选择。调用后 selection 真为空时返回 `true`；控件因强制至少选择一项等规则无法清空时返回 `false`。

### `virtual bool selectAll() = 0`

选择所有直接 accessible child。调用后全部实际已选时返回 `true`。单选控件或带不可选 child 的容器不应声称成功选择了全部。

## API 速查表

| 类别 | API | 作用 | 使用边界 |
| --- | --- | --- | --- |
| 生命周期 | `~QAccessibleSelectionInterface()` | 虚析构接口。 | 指针由 accessible object/Qt 管理。 |
| 查询 | `selectedItemCount()` | 返回选中直接 child 数。 | 与 `selectedItems()` 一致。 |
| 查询 | `selectedItems()` | 返回选中直接 child 列表。 | 结果是借用指针，列表可为空。 |
| 查询 | `selectedItem(int)` | 按选中列表序号取 item。 | 不是 child index；越界为 `nullptr`。 |
| 查询 | `isSelected(QAccessibleInterface *)` | 判断 direct child 是否选中。 | 非直接 child 或失效项返回 false。 |
| 修改 | `select(QAccessibleInterface *)` | 选中直接 child。 | 单选可替换原选择；成功才返回 true。 |
| 修改 | `unselect(QAccessibleInterface *)` | 取消选中 child。 | 未选中/不可取消时返回 false。 |
| 修改 | `clear()` | 清空选择。 | 强制至少选一项的模型可能失败。 |
| 修改 | `selectAll()` | 选中全部直接 child。 | 单选或不可选项存在时不应虚报成功。 |

### 一句话总结

`QAccessibleSelectionInterface` 是直接 child 选择的读写契约：区分 selected-list index 与 child index，严格反映实际单选/多选规则，返回的 interface 不转移所有权，并在选择真正改变后发送无障碍事件。
