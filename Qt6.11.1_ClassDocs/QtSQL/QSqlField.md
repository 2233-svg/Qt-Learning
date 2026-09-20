# QSqlField
> Qt 6.11.1 · Qt SQL · 来自 `QSqlField`

## 1. 先建立直觉

`QSqlField` 描述数据库记录中的一个字段：字段名、表名、值、类型、是否只读、是否自动生成、默认值、是否需要生成到 SQL 中等。它是 `QSqlRecord` 的基本组成单元。

如果 `QSqlRecord` 是一行或一组列，`QSqlField` 就是一列的“元数据 + 当前值”。

## 2. 类说明

保留类说明：这些 API 来自 `QSqlField`，属于 Qt SQL 模块，用于保存单个 SQL 字段的名称、类型、值和生成规则。

它是值类型，不直接连接数据库。字段的行为最终要通过 `QSqlRecord`、`QSqlTableModel`、`QSqlDriver` 等对象进入 SQL 生成或结果读取流程。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QSqlField(name, type, table)` | 创建字段，指定名称、元类型和表名。 |
| `name()` / `setName()` | 读取或设置字段名。 |
| `tableName()` / `setTableName()` | 读取或设置所属表名。 |
| `metaType()` / `setMetaType()` | 读取或设置字段 Qt 元类型。 |
| `typeID()` / `setTypeID()` | 保存驱动原生类型编号。 |
| `value()` / `setValue()` | 读取或设置当前字段值。 |
| `isNull()` / `clear()` | 判断或清空为 NULL。 |
| `defaultValue()` / `setDefaultValue()` | 记录数据库默认值。 |
| `isGenerated()` / `setGenerated()` | 控制 SQL model 生成语句时是否包含该字段。 |
| `isReadOnly()` / `setReadOnly()` | 标记字段是否只读。 |
| `requiredStatus()` / `setRequiredStatus()` | 标记字段是否必填、可选或未知。 |
| `length()` / `setLength()`、`precision()` / `setPrecision()` | 记录长度和精度。 |
| `operator==`、赋值、swap | 值类型操作。 |

## 4. 典型流程

```cpp
QSqlField name("name", QMetaType::fromType<QString>());
name.setValue("Grace");
name.setGenerated(true);

QSqlRecord rec;
rec.append(name);
```

让数据库填默认值：

```cpp
QSqlField created("created_at", QMetaType::fromType<QDateTime>());
created.setGenerated(false);
rec.append(created);
```

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 手动构造 `QSqlRecord` | 用字段对象描述每列。 |
| 控制 INSERT/UPDATE 字段 | 通过 `setGenerated(false)` 排除字段。 |
| 数据库元数据展示 | 显示字段名、类型、长度、精度、必填状态。 |
| 自定义 driver/model | 按字段属性生成 SQL 或转换值。 |

## 6. 常见坑与经验

`requiredStatus()` 是元数据提示，不等于数据库约束一定会按你的预期工作。真实约束仍由数据库执行，失败通过 `QSqlError` 报告。

`metaType()` 是 Qt 侧类型，`typeID()` 是驱动/数据库侧类型编号。跨驱动写代码时不要依赖某个原生编号稳定一致。

字段值是 `QVariant`，字符串、数字、日期、二进制都可能有驱动转换。对精度敏感的数值要结合 `QSqlDatabase::numericalPrecisionPolicy` 和字段精度测试。

## 7. 知识点覆盖

- 单字段元数据和值。
- Qt 类型、数据库原生类型、长度和精度。
- NULL、默认值、只读、必填状态。
- generated 标志和 SQL model 语句生成。
