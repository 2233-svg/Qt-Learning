# QSqlRelationalDelegate 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSqlRelationalDelegate>`  
> 所属模块：`Qt6::Sql`  
> 继承：`QStyledItemDelegate`

## 它解决什么问题

`QSqlRelationalDelegate` 是为 `QSqlRelationalTableModel` 准备的 item delegate。它解决外键列在表格视图中的编辑问题：数据库存储的是 ID，但用户应该看到并选择关联表中的名称。

假设订单表保存 `customer_id`，客户表保存 `id` 和 `name`。`QSqlRelationalTableModel` 通过 `QSqlRelation` 显示客户名称，而本 delegate 会为该外键列创建组合框，让用户选择名称，最终写回对应的 ID。

```cpp
auto *model = new QSqlRelationalTableModel(this, db);
model->setTable("orders");
model->setRelation(customerColumn, QSqlRelation("customers", "id", "name"));
model->select();

view->setModel(model);
view->setItemDelegate(new QSqlRelationalDelegate(view));
```

如果不安装这个 delegate，视图仍可显示关系模型的数据，但编辑外键时常常只会得到普通文本编辑器，无法安全地把显示值映射回关联键。

## 它不替代关系模型

`QSqlRelationalDelegate` 不定义 relation，也不执行 join；relation 仍由 `QSqlRelationalTableModel::setRelation()` 设置。它只负责 View 层编辑器创建和编辑结果回写。

也不要把它用于普通 `QSqlTableModel` 来期待自动外键支持。普通表模型不知道关联表、键列和显示列，delegate 没有足够信息建立组合框。

## `createEditor()` 与 `setModelData()`

`createEditor()` 检测当前索引是否属于已配置关系的列。是关系列时创建并配置 `QComboBox`，否则沿用普通 delegate 的默认编辑器行为。

`setModelData()` 把组合框当前选项转换为关系模型需要的实际键值并写回 model。重写时不能只把 `comboBox->currentText()` 写入模型，否则数据库外键列可能被错误写成显示文本。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QSqlRelationalDelegate(QObject *parent = nullptr)` | 创建关系模型专用 delegate。 | 设置给 view 后，parent 通常设为 view 以便自动释放。 |
| 析构 | `~QSqlRelationalDelegate()` | 销毁 delegate。 | view 可能在销毁时清理它；避免重复所有权管理。 |
| 创建编辑器 | `createEditor(QWidget *parent, const QStyleOptionViewItem &option, const QModelIndex &index) const` | 为关系外键列创建组合框，为普通列创建默认编辑器。 | 重写时应保留关系列判断，不能对所有列都强行返回同一编辑器。 |
| 写回模型 | `setModelData(QWidget *editor, QAbstractItemModel *model, const QModelIndex &index) const` | 将编辑器结果写回模型，关系列会从显示项映射回实际键值。 | 不要直接写入组合框显示文本，否则可能破坏外键数据。 |

## 易错点

1. 必须先在 `QSqlRelationalTableModel` 上设置 relation，再安装此 delegate。
2. delegate 负责编辑器映射，不会创建数据库外键或执行关系查询。
3. 外键列保存 ID，组合框显示名称；两者不能混写。
4. 模型编辑策略决定何时提交到数据库，delegate 写回 model 不代表已经提交。

### 一句话总结

`QSqlRelationalDelegate` 把关系表模型中的外键编辑变成关联表的下拉选择，并负责把用户选择的显示项安全映射回实际键值。
