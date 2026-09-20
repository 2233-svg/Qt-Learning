# QSqlField 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSqlField>`  
> 所属模块：`Qt6::Sql`  
> 继承：无

## 它解决什么问题

`QSqlField` 描述 SQL 表或视图中的单个字段，并同时保存字段元数据与当前字段值。它是 `QSqlRecord` 的基本单元；应用通常从 query、model 或 record 中取得它，而不是手工构造。

一个字段至少有两层含义：

- **元数据**：字段名、所属表、数据库类型、长度、小数精度、是否必填、是否只读；
- **当前值状态**：`QVariant` 值、是否为 SQL `NULL`、是否是数据库自动生成值、是否应参与自动生成 SQL。

```cpp
QSqlRecord record = query.record();
QSqlField field = record.field("amount");

if (!field.isNull())
    qDebug() << field.metaType() << field.value();
```

## `NULL`、无效 QVariant 与默认值

`clear()` 会把字段值设为 SQL `NULL`；不要用空字符串或数值 0 来代替数据库 NULL。`isNull()` 判断的正是这个状态。

`defaultValue()` 是数据库 schema 中的默认值元数据，不等于字段当前 `value()`。驱动不支持时默认值信息可能不可用。`isAutoValue()` 表示数据库会自动生成该值，例如自增主键；插入新记录后，只有提交到数据库并由 driver 回填，字段才可能拿到真实生成值。

## `generated` 与 `readOnly` 的边界

`isGenerated()`/`setGenerated()` 决定此字段是否参与 Qt SQL 模型生成的 SQL。设为 false 不会删除数据库列，也不会让字段不可读，只是让模型生成 INSERT 或 UPDATE 时忽略该字段。

`isReadOnly()`/`setReadOnly()` 则禁止通过本 `QSqlField` 的 `setValue()` 和 `clear()` 修改值。二者没有必然关系：一个字段可以不参与 SQL 生成但仍可在内存中修改，也可以参与生成但在当前对象中被设为只读。

## 类型转换

值以 `QVariant` 保存。`setValue()` 会尽力把可转换的类型转换成字段 `metaType()`，但不可兼容的值不应依赖隐式转换。数值过大时某些 driver 会以字符串返回以避免精度丢失，因此处理金额、ID 或高精度数值时应依据实际 `QVariant` 类型而非只看 schema 类型。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `enum RequiredStatus` | 描述字段是否必填。 | `Required` 字段没有值时 INSERT 会失败。 |
| 枚举值 | `Unknown` | 必填状态未知。 | 不要把未知状态当作可选或必填。 |
| 枚举值 | `Optional` | 字段可选。 | 仍可能受数据库其它约束限制。 |
| 枚举值 | `Required` | 字段必须提供值。 | 插入前检查值或让数据库 default/auto value 满足要求。 |
| 属性 | `autoValue` | 表示值是否由数据库自动生成。 | Qt 6.8 起提供；插入提交前通常还没有最终生成值。 |
| 属性 | `defaultValue` | 保存数据库字段默认值元数据。 | 仅部分 driver 支持，不等于当前 value。 |
| 属性 | `generated` | 表示字段是否参与 Qt 模型自动生成 SQL。 | 不改变数据库 schema 或内存可读性。 |
| 属性 | `length` | 保存字段长度信息。 | 负数表示 driver 未提供；不同类型语义不同。 |
| 属性 | `metaType` | 保存字段数据库类型的 `QMetaType`。 | 实际 QVariant 类型可能不同，例如大数可能被返回为字符串。 |
| 属性 | `name` | 保存字段名或查询别名。 | 用于 record 按名查找，避免只依赖显示文本。 |
| 属性 | `precision` | 保存数值字段精度。 | 负数表示未知；只对数值类型有意义。 |
| 属性 | `readOnly` | 控制能否通过字段对象修改当前值。 | 只保护此字段对象的写路径，不改变数据库权限。 |
| 属性 | `requiredStatus` | 保存字段必填状态。 | 与 default/auto value 一起判断插入是否有效。 |
| 属性 | `tableName` | 保存字段所属表名。 | QPSQL forward-only 查询记录中可能无法提供。 |
| 属性 | `value` | 保存当前字段的 QVariant 值。 | 设 NULL 用 `clear()`，不要依赖无效 QVariant。 |
| 构造 | `QSqlField(const QString &fieldName = {}, QMetaType type = {}, const QString &table = {})` | 创建带名称、类型和表名的空字段。 | 手工构造时类型要与数据库实际列兼容。 |
| 构造 | `QSqlField(const QSqlField &other)` | 拷贝字段。 | 拷贝的是字段快照，不会自动同步数据库。 |
| 析构 | `~QSqlField()` | 销毁字段对象。 | 值类型，无需额外资源管理。 |
| 设为 NULL | `clear()` | 清空字段值并将其设为 SQL NULL。 | 只读字段上无效果。 |
| 默认值 | `defaultValue() const` | 返回数据库元数据中的默认值。 | 不等于当前字段值，且部分 driver 不支持。 |
| 自动值 | `isAutoValue() const` | 判断数据库是否自动生成此字段值。 | 新记录提交到数据库前，通常无法获得最终值。 |
| 是否生成 SQL | `isGenerated() const` | 判断字段是否参与模型自动生成的 SQL。 | false 不表示字段不存在或不可读。 |
| 是否 NULL | `isNull() const` | 判断当前值是否为 SQL NULL。 | 与空字符串、0、无效字段不同。 |
| 只读状态 | `isReadOnly() const` | 判断字段是否禁止 `setValue()` 和 `clear()`。 | 是对象级保护，不替代数据库权限。 |
| 有效性 | `isValid() const` | 判断字段类型是否有效。 | 用于识别不存在或默认构造的字段。 |
| 长度 | `length() const` | 返回字段长度元数据。 | 负值表示未知。 |
| 数据类型 | `metaType() const` | 返回字段的 `QMetaType`。 | 按实际 QVariant 值处理大数和 driver 特殊返回。 |
| 名称 | `name() const` | 返回字段名称或别名。 | 别名时不一定是底层数据库列名。 |
| 精度 | `precision() const` | 返回数值字段精度元数据。 | 对非数值字段通常无意义，负值表示未知。 |
| 必填状态 | `requiredStatus() const` | 返回字段必填状态。 | 插入前结合当前值、默认值和自动值判断。 |
| 设置自动值 | `setAutoValue(bool autoVal)` | 设置自动生成值标记。 | 标记不会让数据库自动创建自增行为。 |
| 设置默认值 | `setDefaultValue(const QVariant &value)` | 设置字段默认值元数据。 | 不会自动把当前 value 改成默认值。 |
| 设置生成状态 | `setGenerated(bool gen)` | 设置是否把字段放进模型生成的 SQL。 | 常用于排除计算列或只读列。 |
| 设置长度 | `setLength(int fieldLength)` | 设置字段长度元数据。 | 不会改变实际数据库列定义。 |
| 设置类型 | `setMetaType(QMetaType type)` | 设置字段类型元数据。 | 与 setValue 的转换逻辑有关，应和真实列类型一致。 |
| 设置名称 | `setName(const QString &name)` | 设置字段名称。 | 影响 record 按名访问和生成 SQL 的字段标识。 |
| 设置精度 | `setPrecision(int precision)` | 设置数值精度元数据。 | 不会自动改变当前值的小数位。 |
| 设置只读 | `setReadOnly(bool readOnly)` | 设置字段对象的读写保护。 | 不改变数据库列权限或其它字段副本。 |
| 设置必填 | `setRequired(bool required)` | 将必填状态设为 Required 或 Optional。 | 需要 Unknown 时使用 `setRequiredStatus()`。 |
| 设置必填状态 | `setRequiredStatus(RequiredStatus required)` | 设置完整必填状态。 | 不会立即验证值，只影响元数据与后续生成 SQL。 |
| 设置表名 | `setTableName(const QString &tableName)` | 设置字段所属表名。 | 不会移动字段或修改数据库 schema。 |
| 设置值 | `setValue(const QVariant &value)` | 设置字段当前值，并尝试转换到字段类型。 | 只读字段无效果；不可兼容类型不要依赖隐式转换。 |
| 交换 | `swap(QSqlField &other)` | 高效交换两个字段。 | Qt 6.6 起可用；适合值对象重排。 |
| 表名 | `tableName() const` | 返回字段所属表名。 | 查询别名、特定 driver 或 forward-only 查询可能缺失。 |
| 当前值 | `value() const` | 返回字段当前 QVariant 值。 | 先用 `isNull()` 区分 SQL NULL。 |
| 不等比较 | `operator!=(const QSqlField &other) const` | 判断两个字段是否不相等。 | 比较的是字段对象状态，不是数据库实时值。 |
| 拷贝赋值 | `operator=(const QSqlField &other)` | 用另一字段替换当前字段。 | 替换所有元数据和当前值。 |
| 相等比较 | `operator==(const QSqlField &other) const` | 判断两个字段是否相等。 | 不会查询数据库确认真实列定义。 |

## 易错点

1. `clear()` 是设 SQL NULL，空字符串与 NULL 在数据库语义上不同。
2. `defaultValue()` 是 schema 默认值，不会自动成为当前 `value()`。
3. `isGenerated()` 控制模型自动 SQL，`isReadOnly()` 控制字段对象可否改值，两者不可混用。
4. 自动生成字段的真实值通常要在 INSERT 成功后才可获得。

### 一句话总结

`QSqlField` 是 SQL 单列的元数据和值容器：它同时表达类型、约束、SQL 生成策略与当前 QVariant 值，是 `QSqlRecord` 操作字段的基础。
