# Qt QAccessibleTableModelChangeEvent 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAccessibleTableModelChangeEvent>`  
> 所属模块：`Qt6::Gui`  
> 基类：`QAccessibleEvent`  
> 定位：报告表、树或列表模型数据/结构范围变化的无障碍事件

## 1. 它解决什么问题

`QAccessibleTableModelChangeEvent` 把“表格模型发生什么变化、影响了哪片行列范围”传给辅助技术。它可用于 table、tree 和 list 的可访问对象，使平台后端和读屏能够失效旧缓存、重新读取 cell、更新可导航范围。

它不是 `QAbstractItemModel` 信号的替代品。模型仍要正确发 `beginInsertRows()`/`endInsertRows()`、`dataChanged()` 等 Qt 模型通知；此 event 是向辅助技术报告同一变化的语义层补充。

## 2. 变更类型

### `enum ModelChangeType`

| 枚举值 | 含义 | 范围解释 |
| --- | --- | --- |
| `ModelReset` | 模型已重置，之前关于行、列、cell 的知识都失效。 | 通常不依赖局部范围，默认 `-1` 可保留。 |
| `DataChanged` | cell 没有新增/删除，但指定矩形范围的数据已失效或改变。 | 使用 first/last row、column 描述范围。 |
| `RowsInserted` | 插入新行。 | 指定受影响首末行；列 getter 返回 `-1`。 |
| `ColumnsInserted` | 插入新列。 | 指定受影响首末列；行 getter 返回 `-1`。 |
| `RowsRemoved` | 删除行。 | 指定删除前/后约定下的受影响首末行；列 getter 返回 `-1`。 |
| `ColumnsRemoved` | 删除列。 | 指定受影响首末列；行 getter 返回 `-1`。 |

不要依赖枚举整数值。`DataChanged` 不应伪装成 `ModelReset`，否则辅助技术需要无谓地重建整个对象树。

## 3. 范围与 `-1` 语义

事件构造后，`firstRow`、`firstColumn`、`lastRow`、`lastColumn` 初值都是 `-1`。

- 行插入/删除影响若干行时：填写 `firstRow` 和 `lastRow`，`firstColumn`、`lastColumn` 应保持 `-1`；
- 列插入/删除影响若干列时：填写 `firstColumn` 和 `lastColumn`，行范围应保持 `-1`；
- 矩形数据变化：填写四个边界，表示包含端点的行列范围；
- 模型重置：通常保持范围未指定，让客户端放弃此前完整缓存。

`-1` 不表示“第 0 行/列”，也不表示空范围；它表示该维度不适用或未知。`first` 不能大于 `last`。范围索引必须与 table interface 的 `cellAt()`、`rowCount()`、`columnCount()` 使用同一逻辑坐标。

## 4. 基本用法

```cpp
void GridAccessible::announceRowsInserted(int first, int last)
{
    QAccessibleTableModelChangeEvent event(
        this, QAccessibleTableModelChangeEvent::RowsInserted);
    event.setFirstRow(first);
    event.setLastRow(last);

    QAccessible::updateAccessibility(&event);
}
```

事件应在模型已经完成插入/删除/数据修改之后发送，此时 `rowCount()`、`columnCount()` 和 `cellAt()` 已能反映新结构。event 是短生命周期对象，通常栈上创建；`updateAccessibility()` 不取得所有权。

## 5. 与 `QAccessibleTableInterface::modelChange()` 的关系

table interface 的 `modelChange(QAccessibleTableModelChangeEvent *)` 接收这类事件详情，用于更新自身 cell、header、跨度与选择缓存。实现不能保存 event 指针到异步任务中，因为它只在调用期间有效。

当模型变化影响大量虚拟 cell 时，优先根据 event 的类型和范围局部失效 cache；只有 `ModelReset` 才应整体丢弃此前模型映射。

## 6. 逐项 API 说明

### `QAccessibleTableModelChangeEvent(QObject *object, ModelChangeType type)`

构造针对 QObject 的 table model change event。目标只借用，变更类型在构造时设定，范围字段初始为 `-1`。

### `QAccessibleTableModelChangeEvent(QAccessibleInterface *iface, ModelChangeType type)`

构造针对已知 accessible interface 的事件。interface 必须在提交期间有效，且不转移所有权。

### `~QAccessibleTableModelChangeEvent()`

虚析构由基类提供。销毁事件不删除 table、model 或 interface。

### `ModelChangeType modelChangeType() const` / `void setModelChangeType(ModelChangeType)`

读取或修改变化类型。若在构造后修改类型，必须同步重设范围字段，避免留下与新类型矛盾的 row/column 范围。

### `int firstRow() const`、`lastRow() const`、`firstColumn() const`、`lastColumn() const`

读取受影响范围的包含端点。返回 `-1` 表示该维度对当前变化不适用或未提供。

### `setFirstRow(int)`、`setLastRow(int)`、`setFirstColumn(int)`、`setLastColumn(int)`

设置受影响范围的端点。调用者负责保证 `first <= last`、索引符合变化类型，并在行/列结构变化中对不适用维度保留 `-1`。

## API 速查表

| 类别 | API | 作用 | 使用边界 |
| --- | --- | --- | --- |
| 类型 | `ModelChangeType` | 指定 reset、数据变更、行列插入或删除。 | 用最精确类型；不要依赖整数值。 |
| 构造 | `QAccessibleTableModelChangeEvent(QObject *, ModelChangeType)` | 为 QObject 创建模型变更事件。 | 目标只借用，范围默认 `-1`。 |
| 构造 | `QAccessibleTableModelChangeEvent(QAccessibleInterface *, ModelChangeType)` | 为 interface 创建事件。 | interface 必须有效，不转移所有权。 |
| 生命周期 | `~QAccessibleTableModelChangeEvent()` | 销毁 event。 | 不删除 table/model/interface。 |
| 类型 | `modelChangeType()` | 查询变更类型。 | 与范围字段保持一致。 |
| 类型 | `setModelChangeType(...)` | 设置变更类型。 | 修改类型后同步重设范围。 |
| 行范围 | `firstRow()` / `lastRow()` | 读取行范围。 | 行变更时填；列变更时通常为 `-1`。 |
| 列范围 | `firstColumn()` / `lastColumn()` | 读取列范围。 | 列变更时填；行变更时通常为 `-1`。 |
| 行范围 | `setFirstRow()` / `setLastRow()` | 设置行端点。 | 包含端点，`first <= last`。 |
| 列范围 | `setFirstColumn()` / `setLastColumn()` | 设置列端点。 | 包含端点，`first <= last`。 |
| 提交 | `QAccessible::updateAccessibility(&event)` | 通知无障碍后端。 | 模型已改变后提交，event 仅在调用期间有效。 |

### 一句话总结

`QAccessibleTableModelChangeEvent` 用类型加范围告诉辅助技术表格结构哪里变了：行变化让列范围为 `-1`，列变化让行范围为 `-1`，数据矩形填满四个端点，模型重置则让旧缓存整体失效。
