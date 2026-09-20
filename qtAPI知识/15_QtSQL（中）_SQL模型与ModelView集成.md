# Qt SQL（中）：SQL 模型与 Model/View 集成

> 适用版本：Qt 6.11.1  
> 核心类型：`QSqlQueryModel`、`QSqlTableModel`、`QSqlRelationalTableModel`、`QSqlRelationalDelegate`、`QDataWidgetMapper`

Qt SQL 提供三层现成模型：

```text
QSqlQueryModel：任意查询结果，只读
       └─ QSqlTableModel：单表，可编辑
              └─ QSqlRelationalTableModel：单表 + 外键显示和编辑
```

它们适合快速把关系数据接到 Item View，但不替代业务层、权限校验和复杂领域事务。

## 1. 构建配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets Sql)
target_link_libraries(mytarget PRIVATE Qt6::Widgets Qt6::Sql)
```

## 2. QSqlQueryModel：查询结果直接进 View

```cpp
auto *model = new QSqlQueryModel(&window);

QSqlQuery query(QSqlDatabase::database("main"));
query.prepare(R"SQL(
    SELECT id, title, created_at
    FROM note
    WHERE archived = :archived
    ORDER BY created_at DESC
)SQL");
query.bindValue(":archived", false);

if (!query.exec()) {
    qWarning() << query.lastError();
    return;
}

model->setQuery(std::move(query));
model->setHeaderData(0, Qt::Horizontal, QStringLiteral("编号"));
model->setHeaderData(1, Qt::Horizontal, QStringLiteral("标题"));
model->setHeaderData(2, Qt::Horizontal, QStringLiteral("创建时间"));

auto *view = new QTableView(&window);
view->setModel(model);
view->hideColumn(0);
```

Qt 6.2+ 的右值 `setQuery(QSqlQuery &&)` 允许先 prepare/bind，再把查询交给模型。设置后仍要检查：

```cpp
if (model->lastError().isValid())
    qWarning() << model->lastError();
```

### 2.1 它为什么只读

任意 SELECT 可能包含 JOIN、聚合、表达式和别名，Qt 无法普遍推断一个单元格应更新哪张表的哪一行。需要编辑时：

- 简单单表使用 `QSqlTableModel`；
- 复杂查询提供明确业务命令；
- 或继承 `QSqlQueryModel`，自行实现 flags/setData 和可靠主键映射。

不要直接按 View 行号拼 UPDATE；排序、过滤和刷新后行号不是业务身份。

### 2.2 增量获取

部分驱动不会一次返回所有记录。模型通过 `canFetchMore()` / `fetchMore()` 增量获取：

```cpp
while (model->canFetchMore())
    model->fetchMore();
```

UI 通常让 View 按需触发，不应为了显示首屏就强制拉完百万行。需要稳定分页、总数和任意跳页时，应在 SQL 层设计分页 API。

### 2.3 refresh

Qt 6.9+ 可调用：

```cpp
model->refresh();
```

它重新运行当前查询。刷新可能改变行集合和选择；需要保留用户上下文时，用主键记录当前业务对象，刷新后按主键重新定位。

## 3. QSqlTableModel：单表编辑

```cpp
auto *model = new QSqlTableModel(
    &window, QSqlDatabase::database("main"));
model->setTable("note");
model->setEditStrategy(QSqlTableModel::OnManualSubmit);
model->setSort(model->fieldIndex("created_at"), Qt::DescendingOrder);

if (!model->select()) {
    qWarning() << model->lastError();
    return;
}

view->setModel(model);
```

`setTable()` 只读取字段信息；`select()` 才真正填充数据。调用 `select()` 会放弃未提交修改，因此刷新按钮不能在用户有草稿时无条件调用它。

### 3.1 三种编辑策略

| 策略 | 何时写数据库 | 适用场景 |
|---|---|---|
| `OnFieldChange` | 字段编辑结束后 | 独立、立即保存字段 |
| `OnRowChange` | 当前行切换时 | 一行构成提交单元 |
| `OnManualSubmit` | 调用 `submitAll()` | 有保存/取消按钮的表格 |

注意：新插入行无论设置 `OnFieldChange` 还是 `OnRowChange`，行为都会类似按行提交，以免部分新行写入。

改变 edit strategy 会回滚模型中尚未提交的修改。

## 4. 手动提交的正确流程

```cpp
connect(saveButton, &QPushButton::clicked, &window, [model] {
    QSqlDatabase db = model->database();
    if (!db.transaction()) {
        showError(db.lastError());
        return;
    }

    if (model->submitAll() && db.commit()) {
        return;
    }

    const QSqlError modelError = model->lastError();
    db.rollback();
    showError(modelError.isValid() ? modelError : db.lastError());
});

connect(cancelButton, &QPushButton::clicked,
        model, &QSqlTableModel::revertAll);
```

`submitAll()` 失败时，OnManualSubmit 的缓存修改仍可保留，以便回滚事务后修正并重试。不要在失败后立即 `select()`，否则用户输入会被清掉。

提交成功后模型会重新填充，View 选择可能丢失。保存前记录主键，成功后重新定位，而不是保存旧 `QModelIndex`。

### 4.1 Delegate 的提交时机

用户仍在单元格编辑器里输入时，值可能尚未写入模型缓存。保存按钮处理前可让 View 提交/关闭当前编辑器，或把编辑流程设计为明确离开单元格后才能保存。测试必须覆盖“光标仍在编辑器中直接点保存”。

## 5. 新增和删除

```cpp
const int row = model->rowCount();
if (model->insertRow(row)) {
    model->setData(model->index(row, model->fieldIndex("title")),
                   QStringLiteral("新笔记"));
    view->setCurrentIndex(model->index(row, 0));
}
```

删除选中行时先取得业务主键，再按行号降序调用 `removeRow()`，避免前一行删除使后续行号变化。OnManualSubmit 下调用 `submitAll()` 才真正提交。

数据库外键和权限错误可能到提交时才出现，UI 要允许用户理解并恢复。

## 6. 字段名优于硬编码列号

```cpp
const int titleColumn = model->fieldIndex("title");
if (titleColumn < 0) {
    qWarning() << "schema 中没有 title";
    return;
}
view->setColumnHidden(model->fieldIndex("id"), true);
```

列号会随 SELECT 或 schema 改变。字段查找也应验证结果，因为 `-1` 传入 index/hideColumn 会隐藏真正错误。

`record()` 可读取字段元信息：

```cpp
const QSqlRecord schema = model->record();
for (int i = 0; i < schema.count(); ++i)
    qDebug() << schema.fieldName(i) << schema.field(i).metaType();
```

## 7. setFilter 的注入风险

```cpp
model->setFilter("archived = 0");
model->select();
```

`setFilter()` 接收的是原始 WHERE 条件片段，没有 bind API。不能这样写：

```cpp
model->setFilter("title = '" + userText + "'"); // 危险
```

安全选择：

- 只从固定白名单组合过滤条件；
- 用户值用驱动的 `formatValue()` 谨慎生成字面量；
- 复杂/安全敏感查询改用 prepared `QSqlQueryModel`；
- 在业务仓库中执行参数化查询，再交给自定义 Model。

## 8. 排序发生在哪里

```cpp
model->setSort(titleColumn, Qt::AscendingOrder);
model->select();
```

`setSort()` 配置 ORDER BY，之后 `select()` 执行；`sort()` 会立即重新 select。大表优先让数据库排序，并为过滤/排序列建立合适索引。

`QSortFilterProxyModel` 是客户端已加载数据上的排序过滤，不等价于数据库 WHERE/ORDER BY。数据量大时 Proxy 不会减少数据库读取。

## 9. QSqlRelationalTableModel：外键显示值

假设 employee.city_id 引用 city.id，而界面应显示 city.name：

```cpp
auto *model = new QSqlRelationalTableModel(
    &window, QSqlDatabase::database("main"));
model->setTable("employee");

const int cityColumn = model->fieldIndex("city_id");
model->setRelation(cityColumn,
                   QSqlRelation("city", "id", "name"));
model->setEditStrategy(QSqlTableModel::OnManualSubmit);
model->setJoinMode(QSqlRelationalTableModel::LeftJoin);

if (!model->select())
    qWarning() << model->lastError();

view->setModel(model);
view->setItemDelegate(new QSqlRelationalDelegate(view));
```

三个 relation 参数依次是：引用表、键字段、显示字段。Delegate 会为外键列创建组合框，显示名称并向模型提交键值。

### 9.1 InnerJoin 与 LeftJoin

- 默认 `InnerJoin`：外键为 NULL 或找不到引用行时，主表该行可能不显示。
- `LeftJoin`：仍显示主表行，外键显示可为空。

若业务允许空外键，通常应显式考虑 LeftJoin。

### 9.2 限制

- 主表主键不能被设置为 relation；
- 多张表的同名显示列可能被重命名以避免冲突；
- 复杂多级关系、权限过滤和计算字段更适合明确 SQL/自定义模型；
- `setData()` 给关系列提交的是外键，而不是显示文本。

## 10. relationModel

```cpp
QSqlTableModel *cities = model->relationModel(cityColumn);
if (cities)
    qDebug() << cities->rowCount();
```

可用于定制外键选择器，但不要假设它与主模型行号一致。显示列、主键列都应从 relation 元信息确定。

## 11. QDataWidgetMapper：表单映射

一条记录由多个独立 Widget 编辑时：

```cpp
auto *mapper = new QDataWidgetMapper(&window);
mapper->setModel(model);
mapper->setSubmitPolicy(QDataWidgetMapper::ManualSubmit);
mapper->addMapping(titleEdit, model->fieldIndex("title"));
mapper->addMapping(bodyEdit, model->fieldIndex("body"), "plainText");
mapper->toFirst();

connect(saveButton, &QPushButton::clicked,
        mapper, &QDataWidgetMapper::submit);
connect(cancelButton, &QPushButton::clicked,
        mapper, &QDataWidgetMapper::revert);
```

Mapper 把 Model 列映射到 Widget 的 user property，或显式属性名。它只解决展示/提交映射，不自动提供跨字段业务校验和数据库事务。

## 12. 什么时候不要使用 SQL Model

以下情况通常采用 Repository + 自定义 ItemModel：

- 一个界面编辑多个聚合对象；
- 保存需要调用远端服务或写多张表；
- 有复杂权限与审计；
- 需要撤销/重做；
- 需要离线草稿、冲突合并；
- UI Role 与表字段不是简单一一对应；
- 查询必须异步且结果需跨线程传递为值对象。

SQL Model 的便捷不应把数据库 schema 直接变成整个应用的公共业务 API。

## 13. 性能

- SELECT 只取界面真正需要的列，避免 `SELECT *`。
- 为 WHERE、JOIN、ORDER BY 字段设计索引，并用数据库 EXPLAIN 验证。
- 大数据用服务器分页，不要只依靠 View 虚拟绘制。
- 不在 Delegate 的 `paint()`/`data()` 中发 SQL。
- 避免每行单独查关联数据的 N+1 查询，使用 JOIN 或批量查询。
- 编辑提交使用事务，减少往返并保证原子性。

## 14. 常见错误

### 14.1 setTable 后忘记 select

只获得字段信息，View 没有数据。

### 14.2 刷新时丢失未提交修改

`select()` 会 revert 待提交内容。刷新前检查 dirty 状态或明确让用户保存/放弃。

### 14.3 submitAll 成功就假设选择仍在

模型可能重新填充。用业务主键恢复上下文。

### 14.4 把用户输入拼给 setFilter

造成 SQL 注入或引号错误。它不是 prepared statement。

### 14.5 外键关系使用默认 InnerJoin

可空或失效外键对应的主表行会消失。按业务决定 LeftJoin。

### 14.6 用 SQL Model 承担复杂业务事务

它擅长单表 CRUD，不擅长表达跨聚合命令、审计和冲突解决。

## 15. API 速查

| API | 用途 |
|---|---|
| `QSqlQueryModel::setQuery()` | 将查询结果设为只读模型 |
| `refresh()` | Qt 6.9+ 重跑当前查询 |
| `canFetchMore()` / `fetchMore()` | 增量取得结果 |
| `QSqlTableModel::setTable()` | 指定单表 |
| `select()` | 按 filter/sort 重新查询 |
| `setEditStrategy()` | 选择提交时机 |
| `submitAll()` / `revertAll()` | 保存/放弃缓存修改 |
| `fieldIndex()` | 按字段名取得列号 |
| `setFilter()` | 设置原始 WHERE 片段 |
| `setSort()` | 配置数据库排序 |
| `setRelation()` | 配置外键显示映射 |
| `QSqlRelationalDelegate` | 用组合框编辑外键 |
| `QDataWidgetMapper` | 将一行字段映射到表单 Widget |

## 16. 自测题

1. 为什么 QSqlQueryModel 默认只读？
2. setTable 后为何还要 select？
3. OnManualSubmit 适合什么交互？
4. submitAll 失败后是否应立即 select？
5. 为什么应按字段名取得列号？
6. setFilter 能否直接拼用户文本？
7. QSortFilterProxyModel 能否减少数据库读取？
8. 可空外键为何常考虑 LeftJoin？
9. 关系列 setData 应提交名称还是键？
10. 何时应从 SQL Model 转向自定义 Model？

## 17. 参考答案

1. 任意查询可能包含 JOIN、聚合和表达式，无法普遍映射回可更新表行。
2. setTable 只读取 schema，select 才执行查询并填充记录。
3. 有明确保存/取消按钮、需要批量检查并统一提交的界面。
4. 不应；会清掉用户修改，应保留缓存供修正或重试。
5. schema/SELECT 列顺序可能变化，硬编码列号脆弱。
6. 不能，它接受原始 SQL 片段且不提供绑定。
7. 不能；它只过滤已经由源模型取得的数据。
8. 默认 InnerJoin 会隐藏 NULL 或无匹配外键的主表行。
9. 外键值。
10. 当业务跨表、跨服务、有复杂校验、审计、离线或自定义 Role 时。

## 18. 本篇结论

```text
任意只读报表 → QSqlQueryModel
简单单表 CRUD → QSqlTableModel
简单外键单表 → QSqlRelationalTableModel + RelationalDelegate
表单式单行编辑 → 可加 QDataWidgetMapper
复杂业务工作流 → Repository + 自定义 Model
```

使用现成 SQL Model 时，仍须显式处理 edit strategy、事务、未提交修改、主键身份、过滤注入和刷新后的选择恢复。
