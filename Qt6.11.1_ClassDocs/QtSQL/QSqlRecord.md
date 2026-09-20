# QSqlRecord
> Qt 6.11.1 · Qt SQL · 来自 `QSqlRecord`

## 1. 先建立直觉

`QSqlRecord` 是一组数据库字段的容器，既能描述表/查询结果有哪些列，也能保存一行记录的字段值。`QSqlQuery::record()` 返回结果集结构，`QSqlTableModel::record(row)` 返回模型某行的字段和值。

它不执行 SQL，只负责字段集合、字段值、NULL 状态和 generated 标志。

## 2. 类说明

保留类说明：这些 API 来自 `QSqlRecord`，属于 Qt SQL 模块，用于保存 SQL 字段列表和值。

`generated` 标志非常重要：在 SQL model 提交 INSERT/UPDATE 时，未生成的字段不会参与 SQL 语句。它常用于让数据库默认值、自增主键或计算列由数据库自己处理。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `append()`、`insert()`、`replace()`、`remove()` | 管理字段列表。 |
| `clear()` | 清空字段和值。 |
| `clearValues()` | 保留字段结构，只清空值。 |
| `count()`、`isEmpty()` | 查询字段数量。 |
| `field(index/name)`、`fieldName(index)` | 读取字段元数据。 |
| `contains(name)`、`indexOf(name)` | 按字段名查找。 |
| `value(index/name)`、`setValue(index/name, val)` | 读取或设置字段值。 |
| `isNull(index/name)`、`setNull(index/name)` | 判断或设置 SQL NULL。 |
| `isGenerated(index/name)`、`setGenerated(index/name, bool)` | 控制字段是否参与生成 SQL。 |
| `keyValues(keyFields)` | 从当前记录中提取与 keyFields 同名的键值记录。 |
| `swap()`、拷贝/移动/比较操作 | 值类型操作。 |

## 4. 典型流程

```cpp
QSqlRecord rec = model.record();
rec.setValue("name", "Ada");
rec.setValue("email", "ada@example.com");
rec.setGenerated("id", false); // 让数据库自增
model.insertRecord(-1, rec);
```

从查询结果读取结构：

```cpp
QSqlRecord rec = query.record();
const int nameColumn = rec.indexOf("name");
while (query.next())
    qDebug() << query.value(nameColumn);
```

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 表单保存到 `QSqlTableModel` | 用 record 填字段，再 `insertRecord()` 或 `setRecord()`。 |
| 动态处理查询结果 | 用 `record()` 查字段名到列号的映射。 |
| 自增主键/默认值 | 对这些字段 `setGenerated(false)`。 |
| 构造 where key | 用 `keyValues()` 从完整记录提取主键字段。 |

## 6. 常见坑与经验

字段名查找可能受数据库大小写、别名和驱动规则影响。复杂查询里建议给列明确 alias，并用 alias 读取。

`isNull()` 和无效字段要区分。字段不存在时相关访问通常返回默认值或 true，看似像 NULL，但真实原因是列名/索引错了。

`clearValues()` 不会删除字段，只清值；`clear()` 才会把结构一起清掉。编辑表单时两者差异很大。

generated 标志只影响 Qt 生成的 SQL。你手写 `QSqlQuery` 时，它不会自动读取 `QSqlRecord` 的 generated 状态。

## 7. 知识点覆盖

- 字段结构和值的统一容器。
- 字段名/索引查找、NULL、QVariant 类型。
- generated 标志和 SQL model 提交行为。
- 查询结果元数据和表记录编辑。
