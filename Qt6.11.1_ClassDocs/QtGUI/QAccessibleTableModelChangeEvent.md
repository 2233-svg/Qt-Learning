# QAccessibleTableModelChangeEvent

> Qt 6.11.1 · Qt GUI · 来自 `QAccessibleTableModelChangeEvent`

## 1. 先建立直觉

`QAccessibleTableModelChangeEvent` 用来通知辅助技术：表格的模型结构或指定单元格数据发生了变化。它面向 `QAccessibleTableInterface`，让屏幕阅读器能够丢弃旧的行列缓存、重新查询受影响区域，并避免继续朗读已经不存在的单元格。

它描述的是表格语义层的变化，不是普通视图重绘。排序、过滤、插入行、删除列、数据更新和模型重置都可能需要对应事件，但鼠标悬停或 repaint 不需要。

## 2. 类说明

- 头文件：`#include <QAccessibleTableModelChangeEvent>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QAccessibleEvent`
- 协作接口：`QAccessibleTableInterface::modelChange()`、`QAccessible::updateAccessibility()`

事件可绑定到 `QObject` 或已存在的 `QAccessibleInterface`。范围使用行列索引描述，通常与用户当前看到的表格坐标一致。

## 3. API 速查

| API | 用途 |
|---|---|
| `QAccessibleTableModelChangeEvent(object, type)` | 为表格对象构造模型变化事件。 |
| `QAccessibleTableModelChangeEvent(iface, type)` | 为表格可访问接口构造模型变化事件。 |
| `modelChangeType()` / `setModelChangeType()` | 读取或修改变化类型。 |
| `firstRow()` / `setFirstRow()` | 变化范围起始行。 |
| `lastRow()` / `setLastRow()` | 变化范围结束行。 |
| `firstColumn()` / `setFirstColumn()` | 变化范围起始列。 |
| `lastColumn()` / `setLastColumn()` | 变化范围结束列。 |
| `ModelReset` | 表格模型整体重置，旧缓存全部无效。 |
| `DataChanged` | 单元格仍存在，但内容或状态变化。 |
| `RowsInserted` / `RowsRemoved` | 行插入或删除。 |
| `ColumnsInserted` / `ColumnsRemoved` | 列插入或删除。 |

## 4. 关键用法

```cpp
QAccessibleTableModelChangeEvent event(
    tableView, QAccessibleTableModelChangeEvent::RowsInserted);
event.setFirstRow(first);
event.setLastRow(last);
event.setFirstColumn(0);
event.setLastColumn(tableModel->columnCount() - 1);

QAccessible::updateAccessibility(&event);
```

插入或删除行列时，范围应指向发生结构变化的位置。对于整行变化，列范围通常覆盖当前可见列；对于整列变化，行范围通常覆盖当前可见行。

```cpp
QAccessibleTableModelChangeEvent event(
    tableView, QAccessibleTableModelChangeEvent::DataChanged);
event.setFirstRow(topLeft.row());
event.setLastRow(bottomRight.row());
event.setFirstColumn(topLeft.column());
event.setLastColumn(bottomRight.column());
QAccessible::updateAccessibility(&event);
```

`DataChanged` 表示单元格没有新增或移除，只是文字、值、状态、格式或可访问说明需要重新查询。不要把纯数据变化报告成 `ModelReset`，否则辅助技术会丢弃过多上下文。

## 5. 变化类型选择

| 场景 | 类型 |
|---|---|
| 模型被重新设置、排序后无法保留旧索引、代理模型整体变化 | `ModelReset`。 |
| 单元格文本、数值、勾选状态或可访问描述变化 | `DataChanged`。 |
| 新增连续行 | `RowsInserted`。 |
| 删除连续行 | `RowsRemoved`。 |
| 新增连续列 | `ColumnsInserted`。 |
| 删除连续列 | `ColumnsRemoved`。 |

如果一次操作涉及多个不连续范围，优先发送多个精确事件；只有旧结构无法可靠映射时才用 `ModelReset`。

## 6. 常见坑与经验

- 事件范围应和 `QAccessibleTableInterface::rowCount()`、`columnCount()`、`cellAt()` 使用同一坐标体系。代理模型、隐藏列和排序会让源模型坐标不再适合直接发送。
- 删除行列后不要让辅助技术继续访问旧单元格接口。先让内部缓存失效，再发送变化通知。
- `ModelReset` 是最强烈的通知，会让读屏丢失上下文；能用插入、删除或数据变化表达时不要滥用。
- 对大量连续更新，可以合并为一个范围事件；对每个单元格发送一条事件会造成明显噪声。
- 事件对象可放在栈上，`updateAccessibility()` 返回后不再保存它。

## 7. 知识点覆盖

- 表格结构变化与数据变化的区别
- 行列范围、可见坐标和代理模型
- 表格接口缓存失效策略
- 插入、删除、重置事件的粒度取舍
- 与 `QAccessibleTableInterface` 和单元格接口的一致性
