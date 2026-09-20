# QSqlQueryModel：把只读 SQL 结果交给模型/视图

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSqlQueryModel>`  
> 模块：`Qt6::Sql`  
> 继承：`QAbstractTableModel`  
> 相关类：`QSqlQuery`、`QSqlTableModel`、`QTableView`

## 它解决什么问题

`QSqlQueryModel` 把一条 SQL 查询的结果包装成 Qt 的表格模型，使 `QTableView`、代理、选择模型和 QML 等模型消费者可以按 `QModelIndex`、角色和模型信号访问数据。

它站在两层抽象之间：

```text
QSqlQuery 负责执行 SQL 和移动结果游标
        ->
QSqlQueryModel 负责 model/view 数据接口
        ->
QTableView 或其他视图负责呈现与交互
```

它的默认职责是**只读展示**。调用 `setHeaderData()` 只能修改视图标题，不能修改数据库字段值。要编辑单张表，应改用 `QSqlTableModel`；要编辑多表查询结果，应继承本类并自行实现写回协议，或设计专用命令。

## 适用场景

- 把统计查询、报表查询、JOIN 结果直接显示在 `QTableView`。
- 需要自定义 `data()` 的展示格式、额外角色或计算列，但不需要自动写回数据库。
- 在不绑定视图的情况下，按行通过 `record(row)` 读取查询结果。

不适合：

- 让用户直接编辑查询结果后期待它自动更新数据库。
- 把前向模式的 `QSqlQuery` 直接交给模型。
- 假定 `rowCount()` 在任何驱动上都立即等于总行数。

## 最小示例

```cpp
#include <QSqlQueryModel>
#include <QTableView>

auto *model = new QSqlQueryModel(parent);
model->setQuery(
    "SELECT name, salary "
    "FROM employee "
    "ORDER BY salary DESC",
    QSqlDatabase::database("hr"));

if (model->lastError().isValid())
    qWarning() << model->lastError().text();

model->setHeaderData(0, Qt::Horizontal, tr("姓名"));
model->setHeaderData(1, Qt::Horizontal, tr("薪资"));
view->setModel(model);
```

`setQuery(QString, db)` 会执行 SQL。传入无效 `db` 或不传连接时，会使用默认连接；实际工程中建议显式传入具名连接。

## 它与 `QSqlQuery` 的差别

`QSqlQuery` 是面向过程的游标接口，你自己决定何时 `next()`。`QSqlQueryModel` 是面向模型/视图的接口，视图通过 `rowCount()`、`data()`、`canFetchMore()` 等函数驱动它取数。

模型内部要支持任意行的索引访问，因此交给 `setQuery(QSqlQuery &&)` 的查询必须：

1. 已成功执行且处于 active 状态。
2. 不是 `isForwardOnly()`。

否则模型无法可靠地提供表格随机访问。

## 延迟取数：为什么行数会慢慢增加

部分驱动无法报告查询结果总行数。当 `QSqlDriver::QuerySize` 不支持时，模型不会立即取完全部记录，而是按批次缓存；视图继续滚动或主动调用 `fetchMore()` 时，模型再从数据库读取下一批。

因此：

- `rowCount()` 可能只是当前已缓存行数。
- `canFetchMore()` 只应对无父项的表格根索引判断。
- 不要把“当前 `rowCount()`”误当最终总记录数。

这个机制让大查询在 UI 中可逐步显示，但不等于给任意巨量结果集提供无限滚动的性能保证；SQL 本身仍应分页、筛选和建立合适索引。

## 刷新、列隐藏与扩展

### `refresh()` 不是通用重新执行按钮

Qt 6.9 的 `refresh()` 会在同一连接上重新执行当前查询，但**不适用于包含绑定值的查询**。有参数的查询应重新准备、重新绑定并用 `setQuery()` 交给模型。

### 移除列只影响模型视图

`removeColumns()` 只是从模型可见列中移除，不会改变底层 SQL，也不会 ALTER TABLE。适合隐藏原始主键等展示列；`setQuery()` 会清除通过 `insertColumns()` 添加的列。

### 子类扩展从模型协议入手

覆盖 `data()` 时，先对特殊角色返回自定义内容，其余角色交给基类；需要把模型索引映射回查询列时使用 `indexInQuery()`。`queryChange()` 在查询替换后调用，适合重建派生缓存，不应在其中假设旧查询仍存在。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QSqlQueryModel(QObject *parent)` | 创建空的 SQL 查询模型。 | 指定 `parent` 以便随界面或控制器释放。 |
| 生命周期 | `~QSqlQueryModel()` | 销毁模型及其当前查询状态。 | 视图仍在使用时不要提前删除模型。 |
| 设置查询 | `setQuery(const QString &query, const QSqlDatabase &db)` | 在指定连接上执行 SQL 并重置模型。 | 失败后通过 `lastError()` 获取原因；建议显式传具名连接。 |
| 设置查询 | `setQuery(QSqlQuery &&query)` | 把已执行的查询移动给模型作为数据源。 | 查询必须 active 且不能是 forward-only；Qt 6.2 引入。 |
| 查询访问 | `query()` | 返回模型当前持有的查询。 | 返回 const 引用，不要试图用它修改模型内部状态。 |
| 查询访问 | `lastError()` | 返回设置查询或读取期间的最近错误。 | `setQuery()` 后立即检查；驱动延迟报错时也要关注。 |
| 查询访问 | `clear()` | 清空查询、错误和当前模型内容。 | 视图会看到空模型；不是数据库删除操作。 |
| 查询访问 | `refresh()` | 在同一连接上重新执行当前查询。 | Qt 6.9 引入；查询含绑定值时不能使用。 |
| 行访问 | `record(int row)` | 返回指定模型行对应的字段和值。 | 行尚未缓存或越界时会返回空记录。 |
| 行访问 | `record()` | 返回当前查询的字段结构。 | 模型未初始化时返回空记录，不包含某一行的值。 |
| 模型数据 | `rowCount(const QModelIndex &parent)` | 返回当前模型中已可见的行数。 | `parent` 必须无效；延迟取数时不一定是最终总数。 |
| 模型数据 | `columnCount(const QModelIndex &parent)` | 返回当前可见列数。 | `parent` 必须无效；隐藏列会影响返回值。 |
| 模型数据 | `data(const QModelIndex &item, int role)` | 为索引和角色提供数据。 | 子类重写时保留基类的标准显示和编辑角色行为。 |
| 模型数据 | `headerData(int section, Qt::Orientation orientation, int role)` | 返回表头数据。 | 本类主要维护水平表头；数据库内容不在这里修改。 |
| 模型数据 | `setHeaderData(int section, Qt::Orientation orientation, const QVariant &value, int role)` | 设置表头显示数据。 | 只改变模型标题，不能更新数据库字段。 |
| 模型数据 | `roleNames()` | 返回角色编号到名称的映射。 | QML 或自定义角色场景才需要关注。 |
| 延迟取数 | `canFetchMore(const QModelIndex &parent)` | 判断是否还有未缓存的结果行。 | 只对无效根索引调用；依赖驱动无法报告总行数的情形。 |
| 延迟取数 | `fetchMore(const QModelIndex &parent)` | 从结果集继续读取一批行。 | 一般由视图自动调用；不要在递归模型通知中滥用。 |
| 可见列 | `insertColumns(int column, int count, const QModelIndex &parent)` | 在模型中插入额外空列。 | 不改变 SQL 查询或数据库；下一次 `setQuery()` 会清除它们。 |
| 可见列 | `removeColumns(int column, int count, const QModelIndex &parent)` | 从模型可见结果中移除列。 | 只隐藏结果列，不会修改底层查询和表结构。 |
| 子类钩子 | `indexInQuery(const QModelIndex &item)` | 把模型索引映射为底层查询索引。 | 重写 `data()` 或增加列时用于正确定位原始字段。 |
| 子类钩子 | `queryChange()` | 在当前查询变化后调用的虚函数。 | 默认无动作；用于刷新派生缓存或字段映射。 |
| 子类钩子 | `setLastError(const QSqlError &error)` | 让派生类设置模型最近错误。 | 仅在自定义数据源或写回逻辑中使用。 |

## 常见错误

- 用 `QSqlQueryModel` 做可编辑表格：它默认只读，换 `QSqlTableModel` 或显式重写写入逻辑。
- 把 `setForwardOnly(true)` 的查询交给 `setQuery(QSqlQuery &&)`：模型需要可随机访问的结果。
- 只看一次 `rowCount()` 就计算总页数：驱动可能在增量读取。
- 带绑定值的查询调用 `refresh()`：重新构造、绑定并设置查询。
- `removeColumns()` 后以为数据库字段也消失：它只是 UI 模型层的可见性变化。
