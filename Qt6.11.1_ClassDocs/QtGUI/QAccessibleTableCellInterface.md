# QAccessibleTableCellInterface

> Qt 6.11.1 · Qt GUI · 来自 `QAccessibleTableCellInterface`

## 1. 先建立直觉

`QAccessibleTableCellInterface` 描述表格、树表或网格中的一个单元格。它让辅助技术知道“这个单元格在第几行第几列、跨多少行列、对应哪些表头、是否被选中、属于哪张表”。

没有这个接口时，读屏可能只能读出一串项目文本，却无法告诉用户它在第几列、列标题是什么，或合并单元格覆盖了哪些位置。

## 2. 类说明

- 头文件：`#include <QAccessibleTableCellInterface>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 来源类：可访问子接口；通过单元格主接口的 `tableCellInterface()` 获取。
- 协作接口：所属表应实现 `QAccessibleTableInterface`。

行列索引通常从 0 开始，与 Qt 模型索引风格一致。展示给用户时，辅助技术可自行转换为 1 基编号。

## 3. API 速查

| API | 用途 |
|---|---|
| `rowIndex()` | 返回单元格起始行索引。 |
| `columnIndex()` | 返回单元格起始列索引。 |
| `rowExtent()` | 返回单元格跨越的行数。 |
| `columnExtent()` | 返回单元格跨越的列数。 |
| `rowHeaderCells()` | 返回描述该行的表头接口列表。 |
| `columnHeaderCells()` | 返回描述该列的表头接口列表。 |
| `isSelected()` | 当前单元格是否被选中。 |
| `table()` | 返回所属表格的可访问接口。 |

## 4. 关键用法

```cpp
int AccessibleCell::rowIndex() const
{
    return index().row();
}

int AccessibleCell::columnIndex() const
{
    return index().column();
}

QAccessibleInterface *AccessibleCell::table() const
{
    return QAccessible::queryAccessibleInterface(view());
}
```

单元格接口应直接反映当前模型状态。排序、过滤、隐藏列或代理模型会改变可见行列时，应使用用户当前感知到的表格坐标，而不是源模型的原始坐标。

## 5. 使用场景

| 场景 | 实现重点 |
|---|---|
| `QTableView` 风格数据网格 | 行列索引、表头、选中状态必须准确。 |
| 合并单元格 | `rowExtent()` / `columnExtent()` 返回跨度，不能总是 1。 |
| 树表 | 单元格角色与层级/展开状态要配合主接口表达。 |
| 电子表格 | 表头、坐标、编辑状态和公式/值说明需分清。 |
| 虚拟大表 | 单元格接口应按需创建，不长期缓存海量对象。 |

## 6. 常见坑与经验

- `rowHeaderCells()` 和 `columnHeaderCells()` 返回的是可访问接口，不是纯文本。没有表头时可返回空列表。
- `isSelected()` 应与表格/视图的选择模型一致。行选中、列选中、单元格选中要按实际规则判断。
- 对隐藏行列，通常不应把不可见单元格暴露为普通可导航单元格，除非应用语义明确需要。
- `table()` 返回的接口由 Qt 管理，调用者不删除；实现也不应返回临时栈对象。
- 模型重置后旧单元格接口可能失效。`rowIndex()` / `columnIndex()` 应防御无效索引。
- 合并单元格的起始索引和跨度要与 `QAccessibleTableInterface::cellAt()` 保持一致。

## 7. 知识点覆盖

- 表格单元格的行列坐标和跨度
- 单元格、表、表头之间的接口关系
- 选择模型与无障碍选中状态
- 代理模型、排序过滤和可见坐标
- 大表虚拟化与接口生命周期
