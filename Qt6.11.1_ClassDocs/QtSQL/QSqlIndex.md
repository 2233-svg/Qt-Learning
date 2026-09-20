# QSqlIndex
> Qt 6.11.1 · Qt SQL · 来自 `QSqlIndex`

## 1. 先建立直觉

`QSqlIndex` 是带排序方向的字段集合，继承自 `QSqlRecord`。它常用来表示表的主键、索引键或排序键：哪些字段构成键，以及每个字段是升序还是降序。

它不是数据库里真正创建索引的 API。它只是 Qt SQL 用来描述索引结构的值对象。

## 2. 类说明

保留类说明：这些 API 来自 `QSqlIndex`，属于 Qt SQL 模块，用于保存 SQL 索引字段、索引名和游标名。

`QSqlDatabase::primaryIndex(table)` 会返回 `QSqlIndex`，`QSqlTableModel::primaryKey()` 也会用它表示模型表的主键。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QSqlIndex(cursorName, name)` | 创建索引描述，带游标名和索引名。 |
| `append(field)` | 追加升序字段。 |
| `append(field, desc)` | 追加字段并指定是否降序。 |
| `isDescending(i)` / `setDescending(i, bool)` | 读取或设置第 i 个字段的排序方向。 |
| `name()` / `setName()` | 读取或设置索引名称。 |
| `cursorName()` / `setCursorName()` | 读取或设置关联游标/表名。 |
| 继承的 `QSqlRecord` API | 管理字段列表和值。 |
| 拷贝/移动/赋值 | 值类型操作。 |

## 4. 典型流程

```cpp
QSqlIndex key = db.primaryIndex("employee");
for (int i = 0; i < key.count(); ++i)
    qDebug() << key.fieldName(i) << key.isDescending(i);
```

手动构造排序键：

```cpp
QSqlIndex order;
order.append(QSqlField("created_at", QMetaType::fromType<QDateTime>()), true);
```

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 查询表主键 | `QSqlDatabase::primaryIndex()`。 |
| SQL model 定位行 | 主键值和 `primaryValues()` 配合。 |
| 自定义 SQL 生成 | 用字段和方向拼 ORDER BY 或 WHERE 键。 |
| 展示数据库结构 | 显示索引名、字段和排序方向。 |

## 6. 常见坑与经验

`QSqlIndex` 不会在数据库里创建索引。要创建物理索引仍要执行 `CREATE INDEX` SQL 或使用数据库迁移工具。

不同数据库对索引名、主键名、大小写和 schema 的返回差异很大。读取 `primaryIndex()` 后要检查 `isEmpty()` 或 `count()`。

排序方向只在使用方生成 SQL 时有意义。单纯把字段标为 descending，不会自动改变已有查询结果顺序。

## 7. 知识点覆盖

- `QSqlIndex` 与 `QSqlRecord` 的继承关系。
- 主键、索引键、排序方向。
- `primaryIndex()`、`primaryKey()` 的返回语义。
- 描述性索引对象和数据库物理索引的区别。
