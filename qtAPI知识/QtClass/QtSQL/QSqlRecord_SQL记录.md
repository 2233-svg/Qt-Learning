# QSqlRecord 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSqlRecord>`  
> 所属模块：`Qt6::Sql`  
> 继承：无

## 它解决什么问题

`QSqlRecord` 是一条 SQL 记录的值对象，通常对应数据库表或视图的一行。它保存有序的 `QSqlField` 集合，因此既携带每列的当前值，也携带字段名称、类型、是否生成 SQL 等元数据。

它常出现在三类地方：

- `QSqlQuery::record()`：取得查询结果列的结构；
- `QSqlQueryModel::record(row)` 或 `QSqlTableModel::record(row)`：取得模型某行快照；
- `QSqlDatabase::record(table)`：取得表字段结构。

```cpp
QSqlRecord record = model->record(row);
const int amountColumn = record.indexOf("amount");

if (amountColumn >= 0 && !record.isNull(amountColumn))
    qDebug() << record.value(amountColumn);
```

## 它不是可更新的数据库行

修改 `QSqlRecord` 只改内存中的字段值，不会自动执行 `UPDATE`。要保存修改：

- 使用 `QSqlTableModel::setRecord()` 配合 `submitAll()`；
- 或用 `QSqlQuery` 写参数化 `UPDATE`；
- 或按所在模型提供的编辑策略提交。

把 record 当作“待提交的数据快照”很准确；把它当成“数据库中的活行对象”则会造成保存遗漏。

## 字段查找与重名

`indexOf(name)` 不区分大小写；找不到返回 `-1`。若有多个同名字段，返回第一个。这在 `SELECT a.id, b.id ...` 中尤其危险，应该在 SQL 中使用别名，如 `a.id AS order_id`、`b.id AS customer_id`。

按名称获取 `field()`、`value()`、`isNull()` 时，字段不存在通常返回默认字段、无效 QVariant 或 true。不要把这些“兜底返回”当作真实数据库 NULL；先用 `contains()` 或 `indexOf()` 判断字段是否存在。

## `generated` 的含义

`setGenerated()` 控制字段是否参与 `QSqlQueryModel`、`QSqlTableModel` 等生成 SQL。设为 false 适合排除计算列、只读视图列或不想提交的字段。

它不是“字段有没有值”，也不等价于 `QSqlField::isAutoValue()`：

- `generated = false`：Qt 自动生成的 SQL 忽略此字段；
- `autoValue = true`：数据库会自动产生字段值，例如自增 ID。

## 结构操作与值操作

- `append()`、`insert()`、`replace()`、`remove()`、`clear()` 操作字段结构；
- `setValue()`、`setNull()`、`clearValues()` 操作字段当前值；
- `clear()` 移除所有字段，`clearValues()` 保留字段定义但把每个值设为 NULL。

二者不可混用。想复用表结构并插入一条空记录时，应该 `clearValues()`，不是 `clear()`。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QSqlRecord()` | 创建不含字段的空记录。 | `isEmpty()` 为 true；可用 append 或 insert 添加字段。 |
| 构造 | `QSqlRecord(const QSqlRecord &other)` | 拷贝记录。 | 隐式共享，复制开销通常很低；修改后发生分离。 |
| 构造 | `QSqlRecord(QSqlRecord &&other)` | 移动构造记录。 | 移动后源对象只应销毁或重新赋值。 |
| 析构 | `~QSqlRecord()` | 销毁记录对象。 | 值类型，不会影响数据库记录。 |
| 追加字段 | `append(const QSqlField &field)` | 在记录末尾添加字段副本。 | 改的是字段结构，不会修改数据库 schema。 |
| 清空字段 | `clear()` | 移除记录中全部字段。 | 与 clearValues 不同；之后不再保留表结构。 |
| 清空值 | `clearValues()` | 保留字段结构，将所有字段值设为 SQL NULL。 | 适合基于既有 record 创建待插入空行。 |
| 按名存在 | `contains(QAnyStringView name) const` | 判断是否有给定名称的字段。 | Qt 6.8 起参数为 QAnyStringView；重名字段只说明至少存在一个。 |
| 字段数量 | `count() const` | 返回字段数量。 | 有效索引范围为 0 到 count 减 1。 |
| 取字段 | `field(int index) const` | 返回指定位置的字段副本。 | 越界返回默认字段，先检查索引。 |
| 取字段 | `field(QAnyStringView name) const` | 返回指定名称的字段副本。 | 找不到返回默认字段；同名字段只取第一个。 |
| 字段名 | `fieldName(int index) const` | 返回指定位置字段名。 | 越界返回空字符串；查询重名列时应使用别名。 |
| 按名索引 | `indexOf(QAnyStringView name) const` | 返回字段名的位置，找不到为 -1。 | 名称不区分大小写；重名时返回第一个。 |
| 插入字段 | `insert(int pos, const QSqlField &field)` | 在指定位置插入字段。 | pos 与字段顺序有关，复合键或模型映射时要保持稳定。 |
| 是否为空记录 | `isEmpty() const` | 判断记录是否没有字段。 | 不表示所有字段值是否为 NULL。 |
| 是否参与 SQL | `isGenerated(int index) const` | 判断指定位置字段是否参与自动 SQL 生成。 | 越界返回 false；与字段是否有值无关。 |
| 是否参与 SQL | `isGenerated(QAnyStringView name) const` | 判断指定名称字段是否参与自动 SQL 生成。 | 不存在或重名时要先确认实际字段。 |
| 是否 NULL | `isNull(int index) const` | 判断指定位置字段是否为 NULL，越界也返回 true。 | 先确认索引有效，避免把“字段不存在”误判为 NULL。 |
| 是否 NULL | `isNull(QAnyStringView name) const` | 判断指定名称字段是否为 NULL，不存在也返回 true。 | 先用 contains 或 indexOf 区分缺列与 SQL NULL。 |
| 键值提取 | `keyValues(const QSqlRecord &keyFields) const` | 返回与 keyFields 同名字段构成的记录，并填入当前值。 | 常用于构造键条件；字段匹配按名称，不按位置。 |
| 移除字段 | `remove(int pos)` | 移除指定位置字段。 | 越界无操作；会改变后续字段索引。 |
| 替换字段 | `replace(int pos, const QSqlField &field)` | 用新字段替换指定位置字段。 | 越界无操作；会连同原字段元数据和值一起替换。 |
| 设置生成状态 | `setGenerated(QAnyStringView name, bool generated)` | 按名设置字段是否参与自动 SQL。 | 字段不存在时无操作；重名时应避免依赖第一个匹配。 |
| 设置生成状态 | `setGenerated(int index, bool generated)` | 按位置设置字段是否参与自动 SQL。 | 适合字段顺序可控的模型记录。 |
| 设 NULL | `setNull(int index)` | 将指定位置字段设为 SQL NULL。 | 越界无操作；不要用空字符串代替 NULL。 |
| 设 NULL | `setNull(QAnyStringView name)` | 将指定名称字段设为 SQL NULL。 | 不存在时无操作；按名操作要处理重名。 |
| 设置值 | `setValue(int index, const QVariant &val)` | 设置指定位置字段的当前值。 | 越界无操作；只改内存，不提交数据库。 |
| 设置值 | `setValue(QAnyStringView name, const QVariant &val)` | 设置指定名称字段的当前值。 | 字段不存在时无操作；必要时检查字段类型转换。 |
| 交换 | `swap(QSqlRecord &other)` | 高效交换两条记录。 | Qt 6.6 起可用；适用于值对象暂存和重排。 |
| 取值 | `value(int index) const` | 返回指定位置字段的 QVariant 值。 | 越界返回无效 QVariant，先判断索引。 |
| 取值 | `value(QAnyStringView name) const` | 返回指定名称字段的 QVariant 值。 | 不存在返回无效 QVariant，不等于 SQL NULL。 |
| 不等比较 | `operator!=(const QSqlRecord &other) const` | 判断两条记录的字段或顺序是否不同。 | 比较内存快照，不会查询数据库。 |
| 移动赋值 | `operator=(QSqlRecord &&other)` | 以移动方式替换当前记录。 | 源对象移动后只可销毁或重新赋值。 |
| 拷贝赋值 | `operator=(const QSqlRecord &other)` | 以另一记录替换当前记录。 | 是值复制，不会同步数据库。 |
| 相等比较 | `operator==(const QSqlRecord &other) const` | 判断字段及其顺序是否完全相同。 | 字段顺序不同即不相等，即使名称和值相同。 |

## 易错点

1. 修改 `QSqlRecord` 不会自动更新数据库。
2. `clear()` 删除字段结构，`clearValues()` 仅把字段值设为 NULL。
3. 按名称访问遇到重名列只会命中第一个，复杂查询务必使用别名。
4. `isNull(name)` 在字段不存在时也可能为 true，先用 `contains()` 区分。
5. `generated` 只控制 Qt 自动 SQL，和数据库自动生成字段不是同一个概念。

### 一句话总结

`QSqlRecord` 是一行 SQL 数据及字段元数据的可复制快照：它负责字段结构和值的内存操作，提交到数据库必须通过 query 或 model 的保存流程。
