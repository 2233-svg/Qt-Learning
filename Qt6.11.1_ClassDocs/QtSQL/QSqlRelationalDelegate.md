# QSqlRelationalDelegate
> Qt 6.11.1 · Qt SQL · 来自 `QSqlRelationalDelegate`

## 1. 先建立直觉

`QSqlRelationalDelegate` 是给 `QSqlRelationalTableModel` 用的编辑委托。它在外键列上创建下拉编辑器，让用户选择关联表里的显示值，然后把对应外键值写回模型。

没有 delegate 时，关系列可能只显示可读文本，但编辑体验通常不好；加上它，外键编辑才像一个真正的下拉选择。

## 2. 类说明

保留类说明：这些 API 来自 `QSqlRelationalDelegate`，属于 Qt SQL 模块，用于在 item view 中编辑 relational table model 的外键列。

它继承 `QStyledItemDelegate`，主要重写 `createEditor()` 和 `setModelData()`。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QSqlRelationalDelegate(parent)` | 创建关系委托。 |
| `createEditor(parent, option, index)` | 对关系列创建合适编辑器，通常是组合框。 |
| `setModelData(editor, model, index)` | 把用户选择写回模型对应外键。 |

## 4. 典型流程

```cpp
auto *model = new QSqlRelationalTableModel(this, db);
model->setTable("employee");
model->setRelation(2, QSqlRelation("city", "id", "name"));
model->select();

view->setModel(model);
view->setItemDelegate(new QSqlRelationalDelegate(view));
```

委托依赖模型的 relation 信息；如果视图使用的不是 `QSqlRelationalTableModel`，它就没有足够信息创建关系编辑器。

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 外键列下拉编辑 | 城市、部门、分类、状态等字段。 |
| 简单管理后台 | 少写自定义 delegate 代码。 |
| 保持 ID 存储和文本显示分离 | 用户看名称，数据库存 ID。 |

## 6. 常见坑与经验

显示值重复会让下拉框看起来有歧义。关系表最好让 displayColumn 对用户可区分，必要时改成视图/查询层提供组合显示。

delegate 只解决编辑器和写回，不解决数据完整性。外键约束、级联删除、引用表同步仍要靠数据库和业务逻辑。

如果你给某列设置了自定义 delegate，它可能覆盖 relational delegate 的行为。复杂表格里要按列设置委托，避免互相踩。

## 7. 知识点覆盖

- Qt item delegate 编辑流程。
- 外键列的显示值和存储值。
- `QSqlRelationalTableModel::relationModel()` 的编辑用途。
- 下拉编辑器、重复显示值和数据完整性边界。
