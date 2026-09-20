# QSqlQueryModel
> Qt 6.11.1 · Qt SQL · 来自 `QSqlQueryModel`

## 1. 先建立直觉

`QSqlQueryModel` 把一条 SELECT 查询结果包装成 Qt Model/View 可显示的表格模型。它适合只读展示：报表、搜索结果、复杂 JOIN 查询、仪表盘表格。

如果你要直接编辑单表数据，用 `QSqlTableModel`；如果要外键显示和下拉编辑，用 `QSqlRelationalTableModel`。

## 2. 类说明

保留类说明：这些 API 来自 `QSqlQueryModel`，属于 Qt SQL 模块，用于把 SQL 查询结果暴露为 `QAbstractTableModel`。

它继承 `QAbstractTableModel`。默认情况下结果是只读的；要可编辑，需要派生类重写 `setData()`、`flags()`，并自己提交 SQL。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QSqlQueryModel(parent)` | 创建查询模型。 |
| `setQuery(QString, db)` | 执行 SQL 并把结果设为模型数据。 |
| `setQuery(QSqlQuery &&query)` | 使用已执行且活跃的 query 作为数据源。 |
| `query()` | 返回当前查询对象。 |
| `lastError()` / `setLastError()` | 读取或设置模型查询错误。 |
| `record()` / `record(row)` | 获取字段结构或某行记录。 |
| `indexInQuery(index)` | 把模型索引映射到底层查询索引。 |
| `data()`、`headerData()`、`setHeaderData()` | 提供单元格和表头数据。 |
| `rowCount()`、`columnCount()` | 行列数量。 |
| `canFetchMore()`、`fetchMore()` | 渐进获取更多结果行。 |
| `clear()` | 清空模型结果。 |
| `refresh()` | Qt 6.9 起重新执行当前查询。 |
| `roleNames()` | 为 QML/角色访问提供列名角色。 |
| `removeColumns()` | 从模型视图中移除列。 |

## 4. 典型流程

```cpp
auto *model = new QSqlQueryModel(this);
model->setQuery("SELECT id, name, total FROM customer_summary", db);
if (model->lastError().isValid())
    qWarning() << model->lastError();

view->setModel(model);
model->setHeaderData(1, Qt::Horizontal, "客户");
```

预准备查询：

```cpp
QSqlQuery q(db);
q.prepare("SELECT * FROM log WHERE level = ?");
q.addBindValue(level);
q.exec();
model->setQuery(std::move(q));
```

## 5. 使用场景

| 场景 | 为什么适合 |
| --- | --- |
| 复杂 JOIN 或聚合报表 | SQL 自由，模型只负责展示。 |
| 只读搜索结果 | `setQuery()` 后交给 `QTableView`。 |
| QML 表格读取 SQL | `roleNames()` 可暴露列角色。 |
| 大结果集 | `fetchMore()` 支持渐进加载，取决于驱动。 |

## 6. 常见坑与经验

`setQuery(QString)` 直接执行字符串，不会帮你绑定用户输入。涉及用户输入时先用 `QSqlQuery::prepare()` 和绑定参数，再 `setQuery(std::move(query))`。

传给 `setQuery(QSqlQuery&&)` 的 query 必须是 active，且不能是 forward-only。否则模型无法随机访问行列。

`refresh()` 会重新执行查询，当前选择、滚动位置和未保存的视图状态可能需要外层保存恢复。

只读不是缺点。很多报表模型强行做编辑，最后会陷入“SQL 查询结果行如何映射回真实表”的问题；可编辑场景优先考虑 table model 或自定义模型。

## 7. 知识点覆盖

- SQL 查询结果到 Model/View 的桥接。
- 只读查询模型与可编辑表模型的区别。
- 查询错误、字段记录、表头、角色名。
- 渐进获取和查询刷新。
- 参数绑定与 `setQuery(QSqlQuery&&)` 的正确使用。
