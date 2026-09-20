# QSqlIndex 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSqlIndex>`  
> 所属模块：`Qt6::Sql`  
> 继承：`QSqlRecord`

## 它解决什么问题

`QSqlIndex` 用值对象描述数据库表或视图的一个索引：它继承 `QSqlRecord` 保存参与索引的字段，并额外保存索引名、关联 cursor 名和每个字段的升降序。

它主要用于读取数据库元数据或协助 Qt SQL 生成 SQL。它不是执行 `CREATE INDEX` 的命令，也不会自动修改数据库中的真实索引。

```cpp
QSqlIndex primary = db.primaryIndex("orders");
for (int i = 0; i < primary.count(); ++i) {
    qDebug() << primary.fieldName(i)
             << (primary.isDescending(i) ? "DESC" : "ASC");
}
```

上例读取的是数据库 driver 返回的主键索引描述。应用可据此识别键列、构造查询条件或辅助排序 UI。

## 它与 `QSqlRecord` 的关系

`QSqlIndex` 是 `QSqlRecord` 的特化：字段增删、按序号读取、字段名和值等记录能力来自基类；`append()` 的额外 `desc` 参数和 `isDescending()` 则提供索引排序方向。

`cursorName` 与 `name` 都是描述性元数据。不要把 `cursorName` 当成数据库游标对象，也不要把 `name` 当成可直接用于 SQL 拼接的可信输入；若动态选择索引名，仍需要验证来源和数据库标识规则。

## 排序方向

`append(field)` 默认将字段按升序加入索引。`append(field, true)` 或 `setDescending(i, true)` 标记为降序。若索引中不存在指定位置，`setDescending()` 不做任何事，因此修改前应确认索引范围。

不同数据库对复合索引排序方向、表达式索引和特殊索引类型的支持不同；`QSqlIndex` 只描述 Qt driver 能提供的信息。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 属性 | `cursorName : QString` | 保存该索引关联的 cursor 名。 | 是元数据名称，不是可操作的数据库游标。 |
| 属性 | `name : QString` | 保存索引名称。 | 不要把外部输入直接当作可信 SQL 标识符使用。 |
| 构造 | `QSqlIndex(const QString &cursorname = {}, const QString &name = {})` | 创建空索引描述并设置 cursor 与索引名。 | 只创建内存描述，不在数据库中创建真实索引。 |
| 构造 | `QSqlIndex(const QSqlIndex &other)` | 复制索引描述。 | 值类型复制；底层数据库 schema 仍可能后来变化。 |
| 构造 | `QSqlIndex(QSqlIndex &&other)` | 移动构造索引描述。 | 被移动对象只能销毁或重新赋值。 |
| 析构 | `~QSqlIndex()` | 销毁索引描述。 | 不影响数据库 schema。 |
| 添加字段 | `append(const QSqlField &field)` | 将字段以升序加入索引字段列表。 | 字段顺序决定复合索引顺序，不能随意调整。 |
| 添加字段 | `append(const QSqlField &field, bool desc)` | 将字段按指定升降序加入索引字段列表。 | `desc = true` 表示降序；支持程度依赖具体数据库。 |
| cursor 名 | `cursorName() const` | 返回关联 cursor 名。 | 仅描述用途，不创建或定位真实 cursor。 |
| 降序查询 | `isDescending(int i) const` | 判断第 `i` 个索引字段是否为降序。 | 先确保索引有效；索引范围来自 `count()`。 |
| 索引名 | `name() const` | 返回索引名称。 | 可能为空，或受 driver 元数据能力限制。 |
| 设置 cursor 名 | `setCursorName(const QString &cursorName)` | 设置关联 cursor 名。 | 只改内存描述，不影响数据库。 |
| 设置方向 | `setDescending(int i, bool desc)` | 设置第 `i` 个字段的升降序标记。 | 越界时无操作；字段顺序应先通过 `append()` 或基类 API 建好。 |
| 设置索引名 | `setName(const QString &name)` | 设置索引名称。 | 不会重命名数据库中的真实索引。 |
| 移动赋值 | `operator=(QSqlIndex &&other)` | 以移动方式替换当前索引描述。 | 源对象移动后不要再读取。 |
| 拷贝赋值 | `operator=(const QSqlIndex &other)` | 以另一索引描述替换当前对象。 | 值复制不反映后续 schema 变化。 |

## 易错点

1. `QSqlIndex` 是元数据描述，不会创建、删除或修改数据库真实索引。
2. 它继承 `QSqlRecord`，字段相关 API 来自基类；本类新增的是索引名称和排序方向。
3. 复合索引中字段顺序很重要，`append()` 的次序不可随意看待。
4. 排序方向与索引元数据的可用性依赖 driver 和数据库能力。

### 一句话总结

`QSqlIndex` 是带排序方向的索引字段描述，适合读取或传递数据库索引元数据，而不是执行 schema 变更。
