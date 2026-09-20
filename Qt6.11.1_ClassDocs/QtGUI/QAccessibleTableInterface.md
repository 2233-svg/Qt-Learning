# QAccessibleTableInterface

> Qt 6.11.1 · Qt GUI · 来自 `QAccessibleTableInterface`

## 1. 先建立直觉

`QAccessibleTableInterface` 描述一个可按行列导航的数据区域。它让辅助技术知道表格有多少行列、某个坐标对应哪个单元格、行列标题是什么、哪些行列或单元格被选中，以及模型结构何时发生变化。

它适合表格、树表、电子表格、属性网格和二维数据视图。若只是普通列表，使用选择接口和子节点语义即可，不必伪装成表格。

## 2. 类说明

- 头文件：`#include <QAccessibleTableInterface>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 来源类：可访问子接口；通过表格主接口的 `tableInterface()` 获取。
- 协作接口：单元格应提供 `QAccessibleTableCellInterface`。

行列索引采用 0 基语义。实现应反映用户当前看到的表格，而不是仅反映底层源模型。

## 3. API 速查

| API | 用途 |
|---|---|
| `rowCount()` / `columnCount()` | 返回当前行列数。 |
| `cellAt(row, column)` | 返回指定坐标的单元格接口。 |
| `rowDescription(row)` / `columnDescription(column)` | 返回行/列描述，常来自表头。 |
| `caption()` / `summary()` | 返回表格标题或摘要对象，可为空。 |
| `isRowSelected(row)` / `isColumnSelected(column)` | 判断整行/整列是否完全选中。 |
| `selectRow(row)` / `selectColumn(column)` | 选择整行/整列。 |
| `unselectRow(row)` / `unselectColumn(column)` | 取消整行/整列选择。 |
| `selectedCells()` / `selectedCellCount()` | 返回当前选中单元格。 |
| `selectedRows()` / `selectedRowCount()` | 返回当前选中行。 |
| `selectedColumns()` / `selectedColumnCount()` | 返回当前选中列。 |
| `modelChange(event)` | 响应模型结构变化事件，刷新表格语义缓存。 |

## 4. 关键用法

```cpp
QAccessibleInterface *AccessibleTable::cellAt(int row, int column) const
{
    if (row < 0 || column < 0 ||
        row >= rowCount() || column >= columnCount())
        return nullptr;

    return accessibleCellForVisibleIndex(row, column);
}
```

`cellAt()` 应按可见表格坐标工作。若视图使用代理模型、隐藏列或排序，辅助技术关心的是用户听到和看到的第几行第几列，而不是源数据表的原始位置。

```cpp
void AccessibleTable::modelChange(QAccessibleTableModelChangeEvent *event)
{
    clearCellCacheAffectedBy(event);
    QAccessible::updateAccessibility(event);
}
```

模型插入、删除、移动或重置后，旧单元格接口、行列计数和选择缓存都可能失效。`modelChange()` 是同步内部缓存与通知辅助技术的关键点。

## 5. 使用场景

| 场景 | 实现重点 |
|---|---|
| 数据表/属性表 | 准确行列数、表头文本、单元格值。 |
| 树表 | 行列语义外，还要表达层级、展开状态和当前项。 |
| 电子表格 | 坐标、合并单元格、选区和编辑状态要可查询。 |
| 大型虚拟表 | 按需创建单元格接口，避免一次暴露百万子节点。 |
| 行选择列表 | 若没有真正列结构，不要强行实现表格接口。 |

## 6. 常见坑与经验

- `selectedCells()` 返回的是接口列表；大量选择时可能成本很高，应与计数和行列选择 API 配合优化。
- `selectRow()` / `selectColumn()` 可能清除旧选择，这取决于真实选择模型；返回值要反映实际结果。
- `rowDescription()` / `columnDescription()` 是文本描述，不等于表头单元格接口。单元格接口仍可通过 `rowHeaderCells()` / `columnHeaderCells()` 关联表头。
- `caption()` 和 `summary()` 可以返回 `nullptr`，但数据密集表格最好提供可理解标题或概要。
- 模型结构变化后必须发送 `QAccessibleTableModelChangeEvent`，否则读屏可能继续使用旧行列数量。
- 表格接口和单元格接口必须互相一致：`cellAt(r,c)` 返回的单元格应报告同样的行列和所属表。

## 7. 知识点覆盖

- 二维可访问表格模型
- 行列计数、单元格定位、表头描述
- 行/列/单元格选择语义
- 表格模型变化与缓存失效
- 可见坐标、代理模型和虚拟化性能
