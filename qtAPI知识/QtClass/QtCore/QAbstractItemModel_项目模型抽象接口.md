# QAbstractItemModel 项目模型抽象接口深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAbstractItemModel>`  
> 所属模块：`Qt6::Core`  
> 继承关系：`QObject -> QAbstractItemModel`  
> 相关框架：Qt Model/View，Qt Widgets item views，QML item views

## 1. 先建立整体认识：它解决什么问题

`QAbstractItemModel` 是 Qt model/view 框架里最核心的抽象接口。它解决的问题不是“怎么显示控件”，而是“如何把任意数据结构，包装成视图能理解的行、列、父子层级和角色数据”。

视图并不关心你的真实数据是数据库、JSON、文件系统、树、数组、网络分页结果，还是内存对象集合。视图只通过模型问几个问题：

```text
某个父节点下面有多少行？
某个父节点下面有多少列？
第 row 行第 column 列对应哪个 QModelIndex？
这个 QModelIndex 的父节点是谁？
这个 QModelIndex 在 DisplayRole、EditRole 等角色下返回什么数据？
数据或结构变了，模型有没有通知我？
```

`QAbstractItemModel` 就是这些问题的统一协议。只要你的类遵守这套协议，`QTreeView`、`QTableView`、`QListView`、代理模型、选择模型、委托和 QML 视图都能用同一套方式访问它。

## 2. 什么时候选它，什么时候别选它

如果数据天然是一维列表，优先继承 `QAbstractListModel`。如果数据天然是二维表格，优先继承 `QAbstractTableModel`。这两个类已经替你处理了很多层级相关细节。

直接继承 `QAbstractItemModel` 通常是因为你需要表达树形或混合层级结构，例如：

- 文件系统目录树；
- 组织架构树；
- JSON 或 XML 节点；
- 工程资源树；
- 带子任务的任务列表；
- 左侧导航树；
- 每个节点下面列数相同或列语义一致的树表。

如果你只是要把 `QStringList` 显示到列表里，直接继承 `QAbstractItemModel` 反而会让代码更复杂。它的灵活性来自五个基础函数都交给你实现，因此也要求你非常准确地维护索引、父子关系和变更通知。

## 3. 模型不是数据本身，而是数据的访问协议

一个模型经常包着真实数据结构：

```text
你的真实数据结构
    Node / QVector / 数据库记录 / 网络分页缓存
            ↓
QAbstractItemModel 子类
            ↓
QModelIndex + role + begin/end 通知
            ↓
QTreeView / QTableView / QListView / QML View / Proxy Model
```

模型的职责是把真实数据翻译成 Qt 视图协议：

- `rowCount()` 和 `columnCount()` 告诉视图某个父节点下有多大。
- `index()` 把行列坐标转成 `QModelIndex`。
- `parent()` 把一个 `QModelIndex` 反向映射回父节点。
- `data()` 按角色返回显示、编辑、图标、提示等数据。
- `flags()` 告诉视图某项是否可选、可编辑、可拖拽、可勾选。
- `beginInsertRows()`、`endInsertRows()` 等函数通知视图结构变更。

也就是说，模型不是“存储容器”的同义词。它可以真的拥有数据，也可以只是访问数据库或远程数据源的适配层。

## 4. 最小只读模型必须实现的 5 个函数

直接继承 `QAbstractItemModel` 时，至少要实现：

```cpp
QModelIndex index(int row, int column,
                  const QModelIndex &parent) const override;

QModelIndex parent(const QModelIndex &child) const override;

int rowCount(const QModelIndex &parent) const override;

int columnCount(const QModelIndex &parent) const override;

QVariant data(const QModelIndex &index, int role) const override;
```

这五个函数共同维护一个模型拓扑：

```text
parent QModelIndex
        ↓ rowCount(parent), columnCount(parent)
row + column
        ↓ index(row, column, parent)
child QModelIndex
        ↓ parent(child)
parent QModelIndex
```

如果 `index()` 和 `parent()` 不能互相对应，视图会出现展开错误、重复节点、死递归、选择错乱或崩溃。写树模型时，最先要保证的不是 `data()` 多漂亮，而是索引拓扑正确。

## 5. `QModelIndex`：视图拿到的是索引，不是你的对象

`QModelIndex` 里面主要包含四类信息：

- `row()`：它在父节点下面的行号。
- `column()`：它在父节点下面的列号。
- `model()`：它属于哪个模型。
- `internalPointer()` 或 `internalId()`：模型实现者放进去的内部标识。

自定义模型一般用 `createIndex()` 创建索引：

```cpp
return createIndex(row, column, nodePointer);
```

或者：

```cpp
return createIndex(row, column, numericId);
```

这些内部标识必须能稳定地帮你找回真实数据项。它们不要求全局唯一，但对于同一个模型里的活动索引来说，组合出来的身份必须能区分不同项。

`QModelIndex` 是轻量临时对象。模型结构变化后，旧的普通 `QModelIndex` 很可能不再可靠。需要跨结构变化保存索引时，应使用 `QPersistentModelIndex`，并且模型在移动或重排时要正确维护 persistent index。

## 6. 根节点和无效索引

在 Qt 模型里，无效 `QModelIndex()` 通常表示根层级：

```cpp
int MyModel::rowCount(const QModelIndex &parent) const
{
    if (!parent.isValid())
        return rootItem->childCount();

    auto *node = static_cast<Node *>(parent.internalPointer());
    return node->childCount();
}
```

对树模型来说：

- `parent` 无效：询问根下面有多少顶层项。
- `parent` 有效：询问某个节点下面有多少子项。
- 顶层项的 `parent()` 应返回无效索引。
- 常见树表模型通常只让第 0 列节点拥有子项，其它列的 `rowCount()` 返回 0。

这一点特别容易错：`QModelIndex()` 不是“错误索引”那么简单，它在很多 API 里表示根。

## 7. 一个树模型骨架

下面是一个典型树模型的核心形状。它不是完整工程，但能看出 `index()`、`parent()`、`rowCount()`、`data()` 如何互相配合。

```cpp
struct Node
{
    QString name;
    Node *parent = nullptr;
    QVector<std::unique_ptr<Node>> children;

    int rowInParent() const
    {
        if (!parent)
            return 0;

        for (int i = 0; i < parent->children.size(); ++i) {
            if (parent->children[i].get() == this)
                return i;
        }
        return -1;
    }
};

QModelIndex TreeModel::index(int row, int column,
                             const QModelIndex &parent) const
{
    if (!hasIndex(row, column, parent))
        return {};

    Node *parentNode = parent.isValid()
        ? static_cast<Node *>(parent.internalPointer())
        : m_root.get();

    Node *childNode = parentNode->children.at(row).get();
    return createIndex(row, column, childNode);
}

QModelIndex TreeModel::parent(const QModelIndex &child) const
{
    if (!child.isValid())
        return {};

    auto *node = static_cast<Node *>(child.internalPointer());
    Node *parentNode = node->parent;

    if (!parentNode || parentNode == m_root.get())
        return {};

    return createIndex(parentNode->rowInParent(), 0, parentNode);
}

int TreeModel::rowCount(const QModelIndex &parent) const
{
    Node *node = parent.isValid()
        ? static_cast<Node *>(parent.internalPointer())
        : m_root.get();

    return node->children.size();
}

int TreeModel::columnCount(const QModelIndex &) const
{
    return 1;
}

QVariant TreeModel::data(const QModelIndex &index, int role) const
{
    if (!index.isValid() || role != Qt::DisplayRole)
        return {};

    auto *node = static_cast<Node *>(index.internalPointer());
    return node->name;
}
```

这段代码最关键的点：

- `index()` 先用 `hasIndex()` 防止越界。
- `createIndex()` 里放的是能找回真实节点的指针。
- `parent()` 不能调用 `child.parent()` 这种 `QModelIndex` 成员函数来找父级，否则会回到自己的 `parent()` 实现，形成递归。
- 顶层节点的父索引返回无效索引。
- `rowInParent()` 必须反映当前节点在父节点 children 中的真实位置。

## 8. 角色：同一个索引可以返回多种数据

模型的 `data(index, role)` 不是只返回“显示文字”。同一个 `QModelIndex` 在不同 role 下可以返回不同内容：

- `Qt::DisplayRole`：显示文本或主要显示值。
- `Qt::EditRole`：编辑器使用的原始值。
- `Qt::DecorationRole`：图标、颜色或装饰数据。
- `Qt::ToolTipRole`：鼠标悬停提示。
- `Qt::CheckStateRole`：复选状态。
- `Qt::UserRole` 起：业务自定义角色，QML 中尤其常用。

示例：

```cpp
QVariant TaskModel::data(const QModelIndex &index, int role) const
{
    if (!index.isValid())
        return {};

    const Task &task = taskFor(index);

    switch (role) {
    case Qt::DisplayRole:
        return task.title;
    case Qt::CheckStateRole:
        return task.done ? Qt::Checked : Qt::Unchecked;
    case PriorityRole:
        return task.priority;
    default:
        return {};
    }
}
```

如果模型给 QML 用，通常还要重写 `roleNames()`：

```cpp
QHash<int, QByteArray> TaskModel::roleNames() const
{
    auto roles = QAbstractItemModel::roleNames();
    roles[PriorityRole] = "priority";
    roles[DoneRole] = "done";
    return roles;
}
```

## 9. 可编辑模型：`setData()` 和 `flags()` 必须配套

仅仅重写 `setData()` 不一定能让视图进入编辑状态。视图会先询问 `flags(index)`，确认这个索引是否包含 `Qt::ItemIsEditable`。

```cpp
Qt::ItemFlags TaskModel::flags(const QModelIndex &index) const
{
    if (!index.isValid())
        return Qt::NoItemFlags;

    return QAbstractItemModel::flags(index)
        | Qt::ItemIsEditable
        | Qt::ItemIsUserCheckable;
}

bool TaskModel::setData(const QModelIndex &index,
                        const QVariant &value,
                        int role)
{
    if (!index.isValid())
        return false;

    Task &task = taskFor(index);

    if (role == Qt::EditRole) {
        task.title = value.toString();
        emit dataChanged(index, index, { Qt::DisplayRole, Qt::EditRole });
        return true;
    }

    if (role == Qt::CheckStateRole) {
        task.done = value.toInt() == Qt::Checked;
        emit dataChanged(index, index, { Qt::CheckStateRole });
        return true;
    }

    return false;
}
```

重点是：只要数据真的改成功，就要发出 `dataChanged()`。没有这个信号，视图、代理模型、选择模型和 QML 绑定都可能继续使用旧数据。

## 10. 结构变更必须走 begin/end

模型有两种变化：

- **数据变化**：行列结构不变，只是某些 index 的某些 role 值变了，用 `dataChanged()`。
- **结构变化**：行、列、父子层级、顺序发生变化，必须使用 begin/end 函数组合。

插入行的顺序是：

```cpp
bool TreeModel::insertRows(int row, int count, const QModelIndex &parent)
{
    Node *node = nodeFor(parent);

    beginInsertRows(parent, row, row + count - 1);
    node->insertChildren(row, count);
    endInsertRows();

    return true;
}
```

删除行的顺序是：

```cpp
bool TreeModel::removeRows(int row, int count, const QModelIndex &parent)
{
    Node *node = nodeFor(parent);

    beginRemoveRows(parent, row, row + count - 1);
    node->removeChildren(row, count);
    endRemoveRows();

    return true;
}
```

这两个顺序不能反：

- 插入：先 `beginInsertRows()`，再改底层数据，最后 `endInsertRows()`。
- 删除：先 `beginRemoveRows()`，再删底层数据，最后 `endRemoveRows()`。

原因是视图和 `QItemSelectionModel` 需要在变更前后各看到一次一致状态，才能正确更新选择、滚动位置和 persistent index。

## 11. 移动行列比插入删除更讲究

移动不是“先 remove 后 insert”的简单替代。Qt 提供 `beginMoveRows()`、`endMoveRows()` 是为了正确维护 persistent index 和选择状态。

```cpp
bool TreeModel::moveRows(const QModelIndex &sourceParent,
                         int sourceRow,
                         int count,
                         const QModelIndex &destinationParent,
                         int destinationChild)
{
    const int sourceLast = sourceRow + count - 1;

    if (!beginMoveRows(sourceParent,
                       sourceRow,
                       sourceLast,
                       destinationParent,
                       destinationChild)) {
        return false;
    }

    moveNodesInStorage(sourceParent,
                       sourceRow,
                       count,
                       destinationParent,
                       destinationChild);

    endMoveRows();
    return true;
}
```

同一个父节点内向下移动时，`destinationChild` 表示“移动后放到哪个原始位置之前”。例如要把第 0、1 行移动到原来的第 3 行之后，`destinationChild` 往往不是 2，而要按 Qt 的移动语义传入正确的目标边界。`beginMoveRows()` 会检查明显非法的移动，例如移动到自身范围内部，返回 `false` 时必须放弃底层移动。

## 12. 重置模型是重锤

当模型结构大幅变化，逐个发 `dataChanged()` 或 begin/end 很难表达时，可以使用：

```cpp
beginResetModel();
reloadEverything();
endResetModel();
```

重置意味着：

- 视图需要重新查询所有数据。
- 旧选择、当前项、展开状态可能失效。
- 普通 `QModelIndex` 和许多缓存都不再可信。
- `modelAboutToBeReset()` 和 `modelReset()` 会由 begin/end 触发。

不要因为省事就频繁 reset。小范围数据变化用 `dataChanged()`，结构插入删除移动用对应 begin/end，真的全量换数据再 reset。

## 13. layoutChanged 不是插入删除的替代品

`layoutAboutToBeChanged()` 和 `layoutChanged()` 适合“同一批项还在，但布局或顺序变了”的场景，例如排序、重排、代理模型映射变化。

如果你真的新增或删除了行列，应使用 `beginInsertRows()`、`beginRemoveRows()`、`beginInsertColumns()`、`beginRemoveColumns()`。如果你真的移动了连续行列，应优先使用 `beginMoveRows()`、`beginMoveColumns()`。

layout 信号常和 `QPersistentModelIndex` 配合使用。重排之前记录旧索引，重排底层数据后调用 `changePersistentIndex()` 或 `changePersistentIndexList()`，再发出布局变化完成信号。否则用户选中的项可能在排序后指向错误数据。

## 14. lazy loading：`canFetchMore()` 和 `fetchMore()`

模型可以只先暴露一部分数据，视图需要时再继续加载。典型例子是大目录、数据库分页、网络搜索结果。

```cpp
bool ResultModel::canFetchMore(const QModelIndex &parent) const
{
    return !parent.isValid() && m_loadedCount < m_allRows.size();
}

void ResultModel::fetchMore(const QModelIndex &parent)
{
    if (parent.isValid())
        return;

    const int remaining = m_allRows.size() - m_loadedCount;
    const int count = qMin(remaining, 100);

    beginInsertRows({}, m_loadedCount, m_loadedCount + count - 1);
    m_loadedCount += count;
    endInsertRows();
}
```

如果 `fetchMore()` 增加了行或列，仍然必须走 begin/end。不能在 `fetchMore()` 里偷偷改底层数量，然后指望视图自己发现。

## 15. 拖放、排序和匹配

拖放支持由几类函数共同决定：

- `mimeTypes()`：模型支持哪些 MIME 格式。
- `mimeData()`：把被拖拽的索引编码成 `QMimeData`。
- `canDropMimeData()`：判断某个 drop 位置是否能接受数据。
- `dropMimeData()`：真正修改模型数据。
- `supportedDragActions()` 和 `supportedDropActions()`：声明支持复制、移动等动作。
- `flags()`：每个 index 是否可拖拽、可接收 drop。

排序可以重写 `sort(column, order)`。如果排序改变了现有项的排列顺序，应使用 layout 变化信号并正确维护 persistent index。只改变显示顺序但不想改源模型时，很多时候应该用 `QSortFilterProxyModel`。

`match()` 用来从某个起点开始按 role 查找数据。它方便，但不是数据库查询引擎；大模型里频繁全量 match 可能很贵，应考虑建立业务索引或代理模型过滤。

## 16. 线程安全

`QAbstractItemModel` 是 `QObject` 子类，模型相关 API 不应从模型所属线程之外直接调用。视图也通常和模型在 GUI 线程中协作。

正确做法是：

- 后台线程加载或计算原始数据。
- 通过 queued signal 或 `QMetaObject::invokeMethod()` 把结果投递到模型所属线程。
- 在模型所属线程里调用 `beginInsertRows()`、修改底层数据、`endInsertRows()`。

不要在工作线程里直接调用模型的 `insertRows()`、`setData()`、`dataChanged()` 或 `beginResetModel()`。这些调用会让视图在另一个线程收到模型变化，轻则断言，重则随机崩溃。

## 17. `checkIndex()`：调试模型拓扑的好工具

`checkIndex(index, options)` 用来检查某个 `QModelIndex` 是否属于当前模型，行列是否在父节点范围内，以及父子关系是否满足指定约束。

常见用法：

```cpp
Q_ASSERT(checkIndex(index,
                    CheckIndexOption::IndexIsValid));
```

在 `parent()` 里要特别小心，因为 `checkIndex()` 默认可能需要调用 `parent()` 来验证索引，错误使用会触发递归。此时可以加 `CheckIndexOption::DoNotUseParent`。

```cpp
Q_ASSERT(checkIndex(child,
                    CheckIndexOption::IndexIsValid
                    | CheckIndexOption::DoNotUseParent));
```

如果你确认某个索引应该是顶层项，也可以用 `ParentIsInvalid` 约束父索引必须无效。

## 18. 常见误区

### 18.1 `rowCount()` 对所有 parent 都返回顶层数量

这会让树视图以为每个节点都有同样数量的孩子，轻则显示重复数据，重则无限展开。

### 18.2 在 `parent()` 里调用 `QModelIndex::parent()`

`QModelIndex::parent()` 会回调模型的 `parent()`。在模型自己的 `parent()` 实现里这么写，基本就是递归陷阱。

### 18.3 改了底层数据但忘记通知视图

`setData()` 成功后要发 `dataChanged()`；插入、删除、移动必须用 begin/end；全量重置用 reset。视图不是你的容器观察者，它只相信模型信号。

### 18.4 直接发 rowsInserted 等私有信号

行列插入、删除、移动相关信号是私有信号，可以连接，但子类不应该直接发。应调用对应 begin/end 函数，让 Qt 在正确时机发信号并维护内部状态。

### 18.5 复用已失效的 `QModelIndex`

普通 `QModelIndex` 适合短期使用。模型结构变化后长期保存它是不可靠的。需要跨变化保存时使用 `QPersistentModelIndex`，并保证模型正确维护 persistent index。

### 18.6 用 reset 解决所有刷新问题

reset 很方便，但会让选择、当前项和缓存整体失效。能精确通知时就精确通知，只有结构大换血时再 reset。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 成员类型 | `LayoutChangeHint` | 描述布局变化的提示类型 | 用在 layout 信号中，帮助视图理解排序方向等变化 |
| 枚举值 | `NoLayoutChangeHint` | 表示没有额外布局变化提示 | 默认值，适合一般重排 |
| 枚举值 | `VerticalSortHint` | 表示行方向排序或垂直方向顺序变化 | 常见于按列排序导致行顺序改变 |
| 枚举值 | `HorizontalSortHint` | 表示列方向排序或水平方向顺序变化 | 常见于列顺序变化 |
| 成员类型 | `CheckIndexOption` | 控制 `checkIndex()` 检查哪些约束 | 调试索引合法性时使用 |
| 枚举值 | `CheckIndexOption::NoOption` | 使用默认索引检查规则 | 无额外限制 |
| 枚举值 | `CheckIndexOption::IndexIsValid` | 要求传入索引必须有效 | 检查 `data()`、`setData()` 等必须有效的输入很有用 |
| 枚举值 | `CheckIndexOption::DoNotUseParent` | 检查时不要调用 `parent()` | 在 `parent()` 实现内部避免递归 |
| 枚举值 | `CheckIndexOption::ParentIsInvalid` | 要求索引父项为无效索引 | 用于确认顶层项 |
| 成员类型 | `CheckIndexOptions` | `CheckIndexOption` 的 flags 类型 | 可组合多个检查选项 |
| 构造函数 | `QAbstractItemModel(QObject *parent = nullptr)` | 构造模型对象 | 抽象类不能直接实例化，通常由自定义模型子类调用 |
| 析构函数 | `~QAbstractItemModel()` | 多态销毁模型对象 | 模型销毁会让视图持有的索引失效 |
| 索引检查 | `hasIndex(int row, int column, const QModelIndex &parent) const` | 判断 parent 下的 row 和 column 是否能形成合法索引 | `index()` 里常先调用它防越界 |
| 纯虚索引 | `index(int row, int column, const QModelIndex &parent) const` | 根据父索引和行列创建子索引 | 必须返回属于本模型的索引，无效输入返回无效索引 |
| 纯虚索引 | `parent(const QModelIndex &child) const` | 返回 child 的父索引 | 顶层项返回无效索引，内部不要调用 `QModelIndex::parent()` 造成递归 |
| 索引便利函数 | `sibling(int row, int column, const QModelIndex &index) const` | 返回同一父节点下指定行列的兄弟索引 | 默认通过 `parent()` 和 `index()` 实现，可按存储结构优化 |
| 纯虚尺寸 | `rowCount(const QModelIndex &parent) const` | 返回 parent 下的子行数 | 树模型要区分根、节点和列，表模型对有效 parent 通常返回 0 |
| 纯虚尺寸 | `columnCount(const QModelIndex &parent) const` | 返回 parent 下的列数 | 树表模型通常各层列数一致，但仍要保证和 `index()` 协调 |
| 子项查询 | `hasChildren(const QModelIndex &parent) const` | 判断 parent 是否可能有子项 | `rowCount()` 很贵或 lazy loading 时可重写 |
| 纯虚数据 | `data(const QModelIndex &index, int role) const` | 按 role 返回 index 的数据 | 只支持有意义的 role，无数据返回无效 `QVariant` |
| 数据写入 | `setData(const QModelIndex &index, const QVariant &value, int role)` | 修改 index 的某个 role 数据 | 成功后必须发 `dataChanged()` |
| 表头读取 | `headerData(int section, Qt::Orientation orientation, int role) const` | 返回行头或列头数据 | 常用于表头文字、对齐、提示 |
| 表头写入 | `setHeaderData(int section, Qt::Orientation orientation, const QVariant &value, int role)` | 修改表头某个 role 的数据 | 成功后必须发 `headerDataChanged()` |
| 多角色读取 | `itemData(const QModelIndex &index) const` | 返回 index 的所有可用 role 数据 | 常用于拖放、复制或一次性检查多个角色 |
| 多角色写入 | `setItemData(const QModelIndex &index, const QMap<int, QVariant> &roles)` | 一次设置多个 role 数据 | 未包含的 role 不应被修改，成功后通知变化 |
| 多角色清空 | `clearItemData(const QModelIndex &index)` | 清除 index 上所有 role 数据 | Qt 6.0 起有；成功后应发 `dataChanged()` |
| MIME 类型 | `mimeTypes() const` | 返回模型拖放支持的 MIME 格式 | 自定义格式时要和 `mimeData()`、`dropMimeData()` 配套 |
| MIME 编码 | `mimeData(const QModelIndexList &indexes) const` | 把一组索引编码成 `QMimeData` | 返回对象通常交给 Qt 拖放流程接管 |
| 拖放预检 | `canDropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent) const` | 判断指定位置是否能接受 drop | 默认只检查 MIME 类型和 drop action，自定义位置规则时重写 |
| 拖放写入 | `dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent)` | 接收 drop 并修改模型数据 | 真正改结构时仍要使用 begin/end |
| drop 能力 | `supportedDropActions() const` | 返回模型支持的 drop 动作 | 默认通常为复制动作，支持移动时还要实现数据移动 |
| drag 能力 | `supportedDragActions() const` | 返回模型支持的 drag 动作 | 默认跟随 drop actions，可按模型能力重写 |
| 插入行 | `insertRows(int row, int count, const QModelIndex &parent)` | 在 parent 下插入 count 行 | 重写时先 `beginInsertRows()`，改数据，再 `endInsertRows()` |
| 插入列 | `insertColumns(int column, int count, const QModelIndex &parent)` | 在 parent 下插入 count 列 | 重写时使用 `beginInsertColumns()` 和 `endInsertColumns()` |
| 删除行 | `removeRows(int row, int count, const QModelIndex &parent)` | 从 parent 下删除 count 行 | 重写时先 begin，再删数据，再 end |
| 删除列 | `removeColumns(int column, int count, const QModelIndex &parent)` | 从 parent 下删除 count 列 | 删除期间旧索引和选择需要 Qt 通知维护 |
| 移动行 | `moveRows(const QModelIndex &sourceParent, int sourceRow, int count, const QModelIndex &destinationParent, int destinationChild)` | 移动连续行到目标父节点 | 使用 `beginMoveRows()`，返回 `false` 时不要改底层数据 |
| 移动列 | `moveColumns(const QModelIndex &sourceParent, int sourceColumn, int count, const QModelIndex &destinationParent, int destinationChild)` | 移动连续列到目标父节点 | 使用 `beginMoveColumns()`，注意目标列语义 |
| 插入单行 | `insertRow(int row, const QModelIndex &parent)` | 插入一行的便利函数 | 内部调用 `insertRows(row, 1, parent)` |
| 插入单列 | `insertColumn(int column, const QModelIndex &parent)` | 插入一列的便利函数 | 内部调用 `insertColumns(column, 1, parent)` |
| 删除单行 | `removeRow(int row, const QModelIndex &parent)` | 删除一行的便利函数 | 内部调用 `removeRows(row, 1, parent)` |
| 删除单列 | `removeColumn(int column, const QModelIndex &parent)` | 删除一列的便利函数 | 内部调用 `removeColumns(column, 1, parent)` |
| 移动单行 | `moveRow(const QModelIndex &sourceParent, int sourceRow, const QModelIndex &destinationParent, int destinationChild)` | 移动一行的便利函数 | 内部调用 `moveRows()`，同样遵守 destinationChild 语义 |
| 移动单列 | `moveColumn(const QModelIndex &sourceParent, int sourceColumn, const QModelIndex &destinationParent, int destinationChild)` | 移动一列的便利函数 | 内部调用 `moveColumns()` |
| 增量加载 | `fetchMore(const QModelIndex &parent)` | 加载 parent 下更多数据 | 如果增加行列，必须在函数内使用 begin/end |
| 增量判断 | `canFetchMore(const QModelIndex &parent) const` | 判断 parent 是否还有可加载数据 | 返回 `true` 后视图可能调用 `fetchMore()` |
| 项能力 | `flags(const QModelIndex &index) const` | 返回 index 是否可选、可编辑、可拖拽、可勾选等 | 可编辑必须包含 `Qt::ItemIsEditable` |
| 排序 | `sort(int column, Qt::SortOrder order)` | 按列和顺序排序模型 | 默认不做事；改变顺序时要发 layout 信号并维护 persistent index |
| 编辑代理 | `buddy(const QModelIndex &index) const` | 返回实际应该编辑的 buddy 索引 | 默认每项自己的 buddy，可用于让某列触发编辑另一列 |
| 匹配查找 | `match(const QModelIndex &start, int role, const QVariant &value, int hits, Qt::MatchFlags flags) const` | 从 start 开始按 role 查找匹配项 | 大模型中可能很贵，必要时建立业务索引 |
| 跨行列显示 | `span(const QModelIndex &index) const` | 返回某项跨越的行列大小 | 文档说明当前未被使用，通常不用依赖它 |
| 角色名称 | `roleNames() const` | 返回 role 编号到名称的映射 | QML 访问自定义 role 时必须正确提供名称 |
| 索引检查 | `checkIndex(const QModelIndex &index, CheckIndexOptions options) const` | 检查 index 是否对当前模型合法 | 调试模型实现很有用，在 `parent()` 内配合 `DoNotUseParent` |
| 多角色优化 | `multiData(const QModelIndex &index, QModelRoleDataSpan roleDataSpan) const` | 一次填充多个 role 数据 | 默认逐个调用 `data()`，高性能模型可重写减少重复查找 |
| 信号 | `dataChanged(const QModelIndex &topLeft, const QModelIndex &bottomRight, const QList<int> &roles)` | 通知矩形范围内某些 role 的数据变化 | 结构不变时使用；roles 为空表示不限定角色 |
| 信号 | `headerDataChanged(Qt::Orientation orientation, int first, int last)` | 通知表头 section 范围的数据变化 | `setHeaderData()` 成功后应发出 |
| 信号 | `layoutAboutToBeChanged(const QList<QPersistentModelIndex> &parents, LayoutChangeHint hint)` | 通知布局即将变化 | 排序或重排前发，必要时配合 persistent index 更新 |
| 信号 | `layoutChanged(const QList<QPersistentModelIndex> &parents, LayoutChangeHint hint)` | 通知布局已经变化 | 排序或重排后发，不应用来代替插入删除 |
| 私有信号 | `rowsAboutToBeInserted(const QModelIndex &parent, int first, int last)` | 行即将插入时通知视图 | 由 `beginInsertRows()` 触发，子类不要直接发 |
| 私有信号 | `rowsInserted(const QModelIndex &parent, int first, int last)` | 行插入完成后通知视图 | 由 `endInsertRows()` 触发 |
| 私有信号 | `rowsAboutToBeRemoved(const QModelIndex &parent, int first, int last)` | 行即将删除时通知视图 | 由 `beginRemoveRows()` 触发 |
| 私有信号 | `rowsRemoved(const QModelIndex &parent, int first, int last)` | 行删除完成后通知视图 | 由 `endRemoveRows()` 触发 |
| 私有信号 | `columnsAboutToBeInserted(const QModelIndex &parent, int first, int last)` | 列即将插入时通知视图 | 由 `beginInsertColumns()` 触发 |
| 私有信号 | `columnsInserted(const QModelIndex &parent, int first, int last)` | 列插入完成后通知视图 | 由 `endInsertColumns()` 触发 |
| 私有信号 | `columnsAboutToBeRemoved(const QModelIndex &parent, int first, int last)` | 列即将删除时通知视图 | 由 `beginRemoveColumns()` 触发 |
| 私有信号 | `columnsRemoved(const QModelIndex &parent, int first, int last)` | 列删除完成后通知视图 | 由 `endRemoveColumns()` 触发 |
| 私有信号 | `modelAboutToBeReset()` | 模型即将 reset | 由 `beginResetModel()` 触发，旧数据即将整体失效 |
| 私有信号 | `modelReset()` | 模型 reset 完成 | 由 `endResetModel()` 触发，视图应重新查询 |
| 私有信号 | `rowsAboutToBeMoved(const QModelIndex &sourceParent, int sourceStart, int sourceEnd, const QModelIndex &destinationParent, int destinationRow)` | 行即将移动时通知视图 | 由 `beginMoveRows()` 触发 |
| 私有信号 | `rowsMoved(const QModelIndex &sourceParent, int sourceStart, int sourceEnd, const QModelIndex &destinationParent, int destinationRow)` | 行移动完成后通知视图 | 由 `endMoveRows()` 触发 |
| 私有信号 | `columnsAboutToBeMoved(const QModelIndex &sourceParent, int sourceStart, int sourceEnd, const QModelIndex &destinationParent, int destinationColumn)` | 列即将移动时通知视图 | 由 `beginMoveColumns()` 触发 |
| 私有信号 | `columnsMoved(const QModelIndex &sourceParent, int sourceStart, int sourceEnd, const QModelIndex &destinationParent, int destinationColumn)` | 列移动完成后通知视图 | 由 `endMoveColumns()` 触发 |
| 公共槽 | `submit()` | 请求模型提交缓存数据到永久存储 | 常用于行编辑或延迟提交模型，默认表示无错误 |
| 公共槽 | `revert()` | 请求模型丢弃缓存编辑数据 | 常和 `submit()` 成对用于编辑流程 |
| 保护槽 | `resetInternalData()` | 模型 reset 时清理派生类内部缓存 | 代理模型维护额外缓存时常重写 |
| 保护构造 | `QAbstractItemModel(QAbstractItemModelPrivate &dd, QObject *parent)` | 供 Qt 内部或高级派生类使用的私有数据构造入口 | 普通模型实现不会直接用 |
| 创建索引 | `createIndex(int row, int column, const void *ptr) const` | 用内部指针创建 `QModelIndex` | ptr 必须能在索引有效期内找回真实项 |
| 创建索引 | `createIndex(int row, int column, quintptr id) const` | 用整数 ID 创建 `QModelIndex` | 适合不能或不想暴露指针的模型 |
| 拖放编码 | `encodeData(const QModelIndexList &indexes, QDataStream &stream) const` | 把索引列表编码进数据流 | 主要服务默认拖放实现 |
| 拖放解码 | `decodeData(int row, int column, const QModelIndex &parent, QDataStream &stream)` | 从数据流恢复拖放数据并插入模型 | 主要服务默认 drop 处理 |
| 插入行通知 | `beginInsertRows(const QModelIndex &parent, int first, int last)` | 开始插入 parent 下 first 到 last 行 | 必须在底层插入前调用 |
| 插入行通知 | `endInsertRows()` | 完成插入行通知 | 必须在底层插入后立即调用 |
| 删除行通知 | `beginRemoveRows(const QModelIndex &parent, int first, int last)` | 开始删除 parent 下 first 到 last 行 | 必须在底层删除前调用 |
| 删除行通知 | `endRemoveRows()` | 完成删除行通知 | 必须在底层删除后立即调用 |
| 移动行通知 | `beginMoveRows(const QModelIndex &sourceParent, int sourceFirst, int sourceLast, const QModelIndex &destinationParent, int destinationRow)` | 开始移动连续行 | 返回 `false` 时不要执行底层移动 |
| 移动行通知 | `endMoveRows()` | 完成移动行通知 | 与成功的 `beginMoveRows()` 成对 |
| 插入列通知 | `beginInsertColumns(const QModelIndex &parent, int first, int last)` | 开始插入 parent 下 first 到 last 列 | 必须在底层插入前调用 |
| 插入列通知 | `endInsertColumns()` | 完成插入列通知 | 必须在底层插入后立即调用 |
| 删除列通知 | `beginRemoveColumns(const QModelIndex &parent, int first, int last)` | 开始删除 parent 下 first 到 last 列 | 必须在底层删除前调用 |
| 删除列通知 | `endRemoveColumns()` | 完成删除列通知 | 必须在底层删除后立即调用 |
| 移动列通知 | `beginMoveColumns(const QModelIndex &sourceParent, int sourceFirst, int sourceLast, const QModelIndex &destinationParent, int destinationColumn)` | 开始移动连续列 | 返回 `false` 时不要执行底层移动 |
| 移动列通知 | `endMoveColumns()` | 完成移动列通知 | 与成功的 `beginMoveColumns()` 成对 |
| 重置通知 | `beginResetModel()` | 开始模型整体重置 | 必须在重置内部数据前调用 |
| 重置通知 | `endResetModel()` | 完成模型整体重置 | 调用后视图会重新查询模型 |
| persistent index | `changePersistentIndex(const QModelIndex &from, const QModelIndex &to)` | 把一个 persistent index 从旧索引改到新索引 | 自定义重排时维护长期索引 |
| persistent index | `changePersistentIndexList(const QModelIndexList &from, const QModelIndexList &to)` | 批量更新 persistent index | from 和 to 应按位置一一对应 |
| persistent index | `persistentIndexList() const` | 返回当前模型保存的 persistent index 列表 | 排序、布局变化、复杂移动前可用来映射 |

## 20. 一句话抓住它

`QAbstractItemModel` 的核心不是“返回数据”四个字，而是维护一套稳定协议：索引能往返、父子层级一致、角色数据清楚、结构变化按 begin/end 精确通知。只要这套协议稳，Qt 的视图、代理、选择和委托就能围着你的真实数据正常工作。
