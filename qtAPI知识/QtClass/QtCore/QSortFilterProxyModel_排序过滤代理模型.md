# QSortFilterProxyModel：在不改源模型的前提下提供排序与筛选

> Qt 6.11.1 | `#include <QSortFilterProxyModel>` | 模块：`Qt6::Core`

`QSortFilterProxyModel` 把一个已有的 `QAbstractItemModel` 包在外面，向视图提供“已经过滤、已经排序”的另一套模型索引。它不复制业务数据，也不要求源模型为了某个视图的筛选条件而改变数据结构。

这很适合文件列表、商品表、日志检索、联系人树等场景：同一份源数据可以同时被多个代理以不同条件展示，例如一个视图只显示“未完成”任务，另一个按更新时间倒序显示全部任务。

## 它解决的核心问题

直接在源模型中删除不匹配的行会污染真实数据；直接重排源模型又会影响其他视图。代理模型把“展示策略”从“数据事实”中拆开：

```text
sourceModel()  --源索引-->  QSortFilterProxyModel  --代理索引-->  QTreeView / QTableView
```

因此，所有跨边界的索引都必须明确转换。把源索引直接交给代理视图，或把代理索引交给源模型，都是逻辑错误，即使两者的行列号碰巧相同。

## 基本用法

```cpp
auto *proxy = new QSortFilterProxyModel(this);
proxy->setSourceModel(taskModel);
proxy->setFilterKeyColumn(-1); // 所有列都参与默认过滤
proxy->setFilterRole(Qt::DisplayRole);
proxy->setFilterCaseSensitivity(Qt::CaseInsensitive);
proxy->setFilterFixedString(searchText);
proxy->sort(2, Qt::DescendingOrder);

tableView->setModel(proxy);
```

`setFilterFixedString()` 将用户文本按普通字面量处理；`setFilterWildcard()` 接受通配符；`setFilterRegularExpression()` 才是正则表达式。搜索框的输入若不是用户明确在写正则，通常应优先用固定字符串，避免意外的正则元字符和额外开销。

## 真实场景中的选择

### 搜索结果表

把 `QLineEdit::textChanged` 连接到 `setFilterFixedString()`，源模型只负责数据，代理负责“此刻要显示什么”。当筛选字段不是显示文本时，设置 `filterRole`，不要在视图层手动隐藏行。

### 层级树中的命中路径

`recursiveFilteringEnabled` 为 `true` 时，子项命中会让其父项保留，从而让用户能看到命中项所在的路径。它与 `autoAcceptChildRows` 的方向不同：后者表示父项一旦通过筛选，其所有子项也保留，即使子项自身并不匹配。

### 自定义日期、数值或多列规则

派生类重写 `filterAcceptsRow()`、`filterAcceptsColumn()` 或 `lessThan()`。这三个函数收到的都是**源模型索引**或源行号；在实现内应从 `sourceModel()` 读取角色数据，不能把参数当作代理索引。

```cpp
class DateProxy final : public QSortFilterProxyModel
{
public:
    void setEarliest(const QDate &date)
    {
        beginFilterChange();
        earliest_ = date;
        endFilterChange(Direction::Rows);
    }

protected:
    bool filterAcceptsRow(int sourceRow,
                          const QModelIndex &sourceParent) const override
    {
        const QModelIndex index = sourceModel()->index(sourceRow, 1, sourceParent);
        return sourceModel()->data(index, Qt::UserRole).toDate() >= earliest_;
    }

private:
    QDate earliest_;
};
```

`beginFilterChange()` 自 Qt 6.9 提供，`endFilterChange()` 自 Qt 6.10 提供。参数改变前后必须成对调用；只影响行时传 `Direction::Rows`，只影响列时传 `Direction::Columns`。旧的 `invalidateFilter()`、`invalidateRowsFilter()`、`invalidateColumnsFilter()` 在 Qt 6.13 计划弃用，新代码应使用这一对 API。

## 关键语义与边界

### 索引、选择和持久索引

- `mapToSource()`：代理索引转源索引，适用于提交编辑、打开真实对象等操作。
- `mapFromSource()`：源索引转代理索引；若该项目被过滤，结果可能是无效索引。
- `mapSelectionToSource()` / `mapSelectionFromSource()`：转换整段选择，不能用单个行号猜测。
- 排序或筛选变化会改变代理行号。业务代码不要把代理行号当成稳定 ID；使用源模型中的 ID 角色或 `QPersistentModelIndex`，并仍处理失效。

### 动态更新

`dynamicSortFilter` 默认是 `true`：源模型的内容变化会触发代理重排和重新过滤。它很适合普通展示，但有一个重要限制：开启时，不要通过代理所绑定的编辑控件间接修改源模型。例如 `QComboBox` 使用该代理模型后再调用 `addItem()`，行为可能不符合预期。批量编辑时可暂时关闭动态排序/过滤，完成后再调用 `sort()`。

### 属性绑定

十个公开属性都提供 `QBindable` 访问器。`filterCaseSensitivity` 与 `filterRegularExpression` 会彼此影响：显式设置其中一个会更新另一个的相关状态，并可能打断其属性绑定。对响应式代码而言，应选择一个作为单一真相来源，而不是同时双向绑定。

### 线程与生命周期

- 代理不拥有 `sourceModel()`；源模型必须在代理使用期间存活。
- 模型和连接它的视图应在同一线程中访问。工作线程应产出纯数据，再通过所属线程更新模型，不能从后台线程直接修改正在被视图使用的源模型或代理。
- `QSortFilterProxyModel` 是 `QObject`；给它设置合适的父对象，或在同一线程中按所有权销毁。

## 常见错误

1. **混用两套索引。** 在代理视图的 `activated()` 回调中，先 `mapToSource()`，再查询源模型。
2. **重写过滤函数后没有触发重新过滤。** 自定义条件成员变化时，使用 `beginFilterChange()` / `endFilterChange()`。
3. **对树模型误解递归过滤。** 默认情况下父项不匹配会遮住其子树；需要保留命中路径时启用 `recursiveFilteringEnabled`。
4. **比较函数不满足严格弱序。** `lessThan()` 必须稳定、一致，且不要在其中修改模型；否则排序结果会混乱。
5. **以为代理替源模型保管数据。** 代理只是投影；源模型重置、销毁或换源后，旧索引和选择都需要重新处理。

## API 速查表

| 类别 | API | 语义 | 使用边界 |
| --- | --- | --- | --- |
| 构造 | `QSortFilterProxyModel(QObject *parent = nullptr)` | 创建代理。 | 之后调用 `setSourceModel()`；父对象管理代理寿命，不管理源模型。 |
| 源模型 | `setSourceModel()` / `sourceModel()` | 设置或取得被包装的模型。 | 切换源模型会让旧代理索引失去意义。 |
| 索引映射 | `mapToSource()` / `mapFromSource()` | 在代理与源索引之间转换。 | 过滤掉的源项映射到代理时得到无效索引。 |
| 选择映射 | `mapSelectionToSource()` / `mapSelectionFromSource()` | 在两套模型间转换 `QItemSelection`。 | 批量选择不要靠行号逐项猜测。 |
| 排序 | `sort(int, Qt::SortOrder)` | 以 `sortRole` 排序指定列。 | 树模型会递归排序子项。 |
| 排序状态 | `sortColumn()` / `sortOrder()` | 读取当前排序列和方向。 | 返回的是代理当前状态，不是源模型固有顺序。 |
| 排序规则 | `sortRole`、`setSortRole()`、`sortRoleChanged()` | 选择比较使用的角色，默认 `Qt::DisplayRole`。 | 角色数据类型应可比较；复杂逻辑重写 `lessThan()`。 |
| 字符串排序 | `sortCaseSensitivity`、`setSortCaseSensitivity()`、`sortCaseSensitivityChanged()` | 控制字符串排序的大小写敏感性。 | 只影响默认比较及依赖它的实现。 |
| 本地化排序 | `isSortLocaleAware`、`setSortLocaleAware()`、`sortLocaleAwareChanged()` | 使用 locale-aware 字符串比较。 | 结果可能随区域设置变化，需考虑可复现排序。 |
| 动态策略 | `dynamicSortFilter`、`setDynamicSortFilter()`、`bindableDynamicSortFilter()` | 源模型变化时自动重新排序和过滤，默认开启。 | 开启时不要经代理间接编辑源模型。 |
| 过滤列 | `filterKeyColumn`、`setFilterKeyColumn()` | 指定默认行过滤读取的列；`-1` 表示全部列。 | 多列或跨列逻辑更适合重写 `filterAcceptsRow()`。 |
| 过滤角色 | `filterRole`、`setFilterRole()`、`filterRoleChanged()` | 选择过滤时读取哪个角色。 | 角色不存在时通常无法匹配。 |
| 过滤表达式 | `filterRegularExpression()`、`setFilterRegularExpression(QString/QRegularExpression)` | 设置默认过滤正则。 | 设置大小写属性和正则会互相影响并可能打断绑定。 |
| 固定字符串 | `setFilterFixedString(QString)` | 用字面文本生成过滤条件。 | 用户普通搜索优先用它，避免把输入当正则。 |
| 通配符 | `setFilterWildcard(QString)` | 用 wildcard 生成过滤条件。 | 与正则不是同一语法。 |
| 过滤大小写 | `filterCaseSensitivity`、`setFilterCaseSensitivity()`、`filterCaseSensitivityChanged()` | 控制默认过滤的大小写规则。 | 会传播到过滤正则的相关选项。 |
| 递归过滤 | `recursiveFilteringEnabled`、`isRecursiveFilteringEnabled()`、`setRecursiveFilteringEnabled()` | 子项命中时保留其祖先。 | 仅影响层级模型的呈现策略。 |
| 接受子项 | `autoAcceptChildRows`、`setAutoAcceptChildRows()`、`autoAcceptChildRowsChanged()` | 父项命中时不再过滤其子项。 | 自 Qt 6.0；含义与递归过滤不同。 |
| 属性绑定 | 十个 `bindable...()` 访问器 | 为对应属性提供 `QBindable<T>`。 | 避免相互绑定的属性形成循环或被 setter 打断。 |
| 自定义行规则 | `filterAcceptsRow(int, const QModelIndex &)` | 返回源模型某行是否可见。 | 参数属于源模型；保持无副作用并尽量低成本。 |
| 自定义列规则 | `filterAcceptsColumn(int, const QModelIndex &)` | 返回源模型某列是否可见。 | 参数属于源模型；列规则变化使用 `Direction::Columns`。 |
| 自定义比较 | `lessThan(const QModelIndex &, const QModelIndex &)` | 定义排序的“小于”。 | 两个索引属于源模型；必须满足严格弱序。 |
| 过滤变更 | `beginFilterChange()` | 标记自定义过滤参数即将变化。 | 自 Qt 6.9，必须在修改参数前调用。 |
| 过滤变更 | `endFilterChange(Directions)` | 失效化受影响方向的过滤结果。 | 自 Qt 6.10，和 `beginFilterChange()` 成对使用。 |
| 失效化 | `invalidate()` | 重新计算当前排序与过滤。 | 适合通用刷新；大量变更时评估模型重置的代价。 |
| 旧失效 API | `invalidateFilter()`、`invalidateRowsFilter()`、`invalidateColumnsFilter()` | 旧的细分重新过滤接口。 | Qt 6.13 计划弃用；新代码改用 begin/end。 |
| 模型转发 | `data()`、`setData()`、`headerData()`、`setHeaderData()`、`flags()`、`buddy()`、`span()` | 在映射后转发常见模型请求。 | 若源模型有非常规语义，代理可能需要对应重写。 |
| 结构转发 | `rowCount()`、`columnCount()`、`index()`、`parent()`、`hasChildren()` | 暴露筛选后的树或表结构。 | 行列号属于代理模型。 |
| 增删转发 | `insertRows()`、`removeRows()`、`insertColumns()`、`removeColumns()` | 将结构修改映射至源模型。 | 动态排序过滤开启时，避免经代理进行复杂批量修改。 |
| 拖放与查找 | `mimeData()`、`dropMimeData()`、`mimeTypes()`、`supportedDropActions()`、`match()` | 映射并转发 MIME、拖放、查找操作。 | 所有输入输出索引均按代理侧解释。 |
| 延迟加载 | `canFetchMore()` / `fetchMore()` | 转发源模型的按需加载。 | 自定义源模型需正确发送插行通知。 |
| 属性信号 | `autoAcceptChildRowsChanged()`、`filterCaseSensitivityChanged()`、`filterRoleChanged()`、`recursiveFilteringEnabledChanged()`、`sortCaseSensitivityChanged()`、`sortLocaleAwareChanged()`、`sortRoleChanged()` | 对应属性发生改变时通知。 | 连接 lambda 时提供 context，避免悬空回调。 |

`QSortFilterProxyModel` 的价值不在“把表格排一下序”，而在于它把展示规则做成可组合、可替换的模型层。只要始终分清源索引与代理索引，并正确通知自定义条件的变化，它能让复杂视图保持干净。
