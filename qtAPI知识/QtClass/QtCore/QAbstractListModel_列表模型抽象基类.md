# QAbstractListModel 列表模型抽象基类深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAbstractListModel>`  
> 所属模块：`Qt6::Core`  
> 继承关系：`QObject -> QAbstractItemModel -> QAbstractListModel`

## 1. 它解决什么问题

`QAbstractListModel` 是专门给“一维列表数据”准备的模型基类。它仍然属于 Qt model/view 框架，但比 `QAbstractItemModel` 少了树模型和多列模型的负担。

如果你的数据天然长这样：

```text
0  Alice
1  Bob
2  Carol
3  David
```

或者每一行是一个对象：

```text
0  Task { title, done, priority }
1  Task { title, done, priority }
2  Task { title, done, priority }
```

就应该优先考虑 `QAbstractListModel`。它帮你固定了列表模型的基本拓扑：没有子节点，默认只有一列，索引通常只关心 row。

## 2. 它和 `QAbstractItemModel` 的关系

`QAbstractItemModel` 是万能接口，要自己回答行、列、父子、索引和数据。`QAbstractListModel` 在它之上做了简化：

- `parent()` 被处理为无层级模型语义。
- `columnCount()` 默认表示只有一列。
- `index(row, column, parent)` 已经按列表模型做了默认实现。
- `sibling()` 已经按同一列表里的行列关系做了默认实现。

所以直接继承 `QAbstractListModel` 时，最小只读模型通常只需要实现：

```cpp
int rowCount(const QModelIndex &parent = QModelIndex()) const override;
QVariant data(const QModelIndex &index,
              int role = Qt::DisplayRole) const override;
```

这正是它的价值：你把精力放在“列表有多少行”和“某一行在某个 role 下显示什么”，不必重复写列表模型永远无父子的样板代码。

## 3. 什么时候不用它

不要因为它名字里有 Model 就什么都继承它。

- 数据有树形层级：用 `QAbstractItemModel`。
- 数据是常规二维表格：用 `QAbstractTableModel`。
- 数据只是字符串列表：优先用 `QStringListModel`。
- 数据已经来自 SQL 查询：考虑 `QSqlQueryModel` 或相关 SQL 模型。
- 只想过滤或排序另一个模型：用 `QSortFilterProxyModel`。

`QAbstractListModel` 最适合“多行、每行一个逻辑对象、通过不同 role 暴露字段”的场景，尤其适合 QML 的 `ListView`、`Repeater`、`ComboBox` 等。

## 4. 最小只读列表模型

```cpp
class TaskListModel : public QAbstractListModel
{
    Q_OBJECT

public:
    enum Role {
        TitleRole = Qt::UserRole + 1,
        DoneRole,
        PriorityRole
    };

    explicit TaskListModel(QObject *parent = nullptr)
        : QAbstractListModel(parent)
    {
    }

    int rowCount(const QModelIndex &parent = QModelIndex()) const override
    {
        if (parent.isValid())
            return 0;

        return m_tasks.size();
    }

    QVariant data(const QModelIndex &index,
                  int role = Qt::DisplayRole) const override
    {
        if (!index.isValid())
            return {};

        const Task &task = m_tasks.at(index.row());

        switch (role) {
        case Qt::DisplayRole:
        case TitleRole:
            return task.title;
        case DoneRole:
            return task.done;
        case PriorityRole:
            return task.priority;
        default:
            return {};
        }
    }

    QHash<int, QByteArray> roleNames() const override
    {
        auto roles = QAbstractListModel::roleNames();
        roles[TitleRole] = "title";
        roles[DoneRole] = "done";
        roles[PriorityRole] = "priority";
        return roles;
    }

private:
    QVector<Task> m_tasks;
};
```

这里 `rowCount()` 先检查 `parent.isValid()`，这是列表模型非常重要的习惯。列表没有子节点，所以视图问“某个有效 index 下面有多少孩子”时，应该返回 0。

`data()` 只处理有效 index 和支持的 role。不要为了省事让无效 index 返回第一条数据，也不要对未知 role 返回显示文本；role 混乱会让代理模型、QML 绑定和委托行为变得很难排查。

## 5. 可编辑列表模型

可编辑模型需要两件事同时成立：

- `flags()` 返回 `Qt::ItemIsEditable`。
- `setData()` 真正修改数据，并在成功后发 `dataChanged()`。

```cpp
Qt::ItemFlags TaskListModel::flags(const QModelIndex &index) const
{
    if (!index.isValid())
        return Qt::NoItemFlags;

    return QAbstractListModel::flags(index)
        | Qt::ItemIsEditable;
}

bool TaskListModel::setData(const QModelIndex &index,
                            const QVariant &value,
                            int role)
{
    if (!index.isValid())
        return false;

    Task &task = m_tasks[index.row()];

    if (role == TitleRole || role == Qt::EditRole) {
        task.title = value.toString();
        emit dataChanged(index, index, { TitleRole, Qt::DisplayRole, Qt::EditRole });
        return true;
    }

    return false;
}
```

`dataChanged()` 的范围在列表中通常是同一个 index 到同一个 index。一次修改多行时，可以用从第一行到最后一行的范围，但要确保这些行在同一个父节点下；列表模型的父节点通常就是无效索引。

## 6. 插入和删除行

列表模型的结构变化基本就是行变化。插入时：

```cpp
void TaskListModel::appendTask(const Task &task)
{
    const int row = m_tasks.size();

    beginInsertRows(QModelIndex(), row, row);
    m_tasks.append(task);
    endInsertRows();
}
```

删除时：

```cpp
bool TaskListModel::removeRows(int row,
                               int count,
                               const QModelIndex &parent)
{
    if (parent.isValid() || row < 0 || count < 0)
        return false;

    if (row + count > m_tasks.size())
        return false;

    beginRemoveRows(parent, row, row + count - 1);
    m_tasks.erase(m_tasks.begin() + row,
                  m_tasks.begin() + row + count);
    endRemoveRows();

    return true;
}
```

顺序必须是 begin、修改底层容器、end。视图、选择模型和代理模型依靠这组通知维护内部状态。直接 `m_tasks.append()` 后只发 `layoutChanged()` 是不对的。

## 7. `index()`、`sibling()` 和默认一列

`QAbstractListModel` 提供了 `index()` 和 `sibling()` 的实现。它们的行为符合普通一维列表：

- 顶层第 `row` 行、第 0 列可以形成有效 index。
- 有效 parent 下面没有子项。
- 默认列数是 1。
- 同一列表里的 sibling 可以通过 row 和 column 查到。

虽然函数签名里仍然有 `column` 和 `parent`，那是因为它要兼容 `QAbstractItemModel` 的通用接口。对于真正的一维列表，业务代码应把 row 作为主要坐标，column 通常保持 0。

## 8. QML 场景里的 roleNames

QML 不会直接使用 C++ enum 名字，它依赖 `roleNames()` 返回的字节串名称。

```qml
ListView {
    model: taskModel

    delegate: Text {
        text: title + " / " + priority
    }
}
```

这里的 `title` 和 `priority` 就来自：

```cpp
roles[TitleRole] = "title";
roles[PriorityRole] = "priority";
```

如果忘记重写 `roleNames()`，C++ 侧的 `data()` 可能能返回自定义 role，但 QML delegate 里就是访问不到对应名字。

## 9. 拖放在列表模型里的语义

列表拖放通常是“把若干行拖到某个行位置”。你需要组合这些函数：

- `flags()`：给可拖拽项加 `Qt::ItemIsDragEnabled`，给可接收位置加 `Qt::ItemIsDropEnabled`。
- `mimeTypes()`：声明支持的 MIME 类型。
- `mimeData()`：把选中行编码成 `QMimeData`。
- `canDropMimeData()`：检查目标 row 是否可接收。
- `dropMimeData()`：修改底层列表。
- `supportedDragActions()` 和 `supportedDropActions()`：声明复制或移动能力。

`QAbstractListModel` 自己重写了 `dropMimeData()`，用于在列表模型的行语义下接入基类默认逻辑。但只要你有自定义数据格式或真正需要移动业务对象，仍然应按自己的存储结构重写拖放相关函数，并在结构变化时使用 begin/end。

## 10. 线程边界

和所有 `QAbstractItemModel` 子类一样，模型 API 应在模型所属线程调用。GUI 视图使用的列表模型通常就在 GUI 线程。

后台线程可以加载数据，但应该把结果投递回模型线程：

```cpp
connect(worker, &Worker::tasksReady,
        model, &TaskListModel::replaceTasks,
        Qt::QueuedConnection);
```

然后在 `replaceTasks()` 里调用 `beginResetModel()`、替换 `m_tasks`、`endResetModel()`。不要在后台线程直接改 `m_tasks` 并发模型信号。

## 11. 常见误区

### 11.1 忘记处理有效 parent

列表模型没有层级。`rowCount(validParent)` 通常应返回 0，否则视图会以为每一行下面还有子项。

### 11.2 把列当成字段

列表模型的字段应通过 role 暴露，而不是通过多列暴露。如果你开始让 column 0 是标题、column 1 是状态、column 2 是优先级，通常说明应该改用 `QAbstractTableModel`。

### 11.3 修改列表后不发 begin/end

插入、删除、移动行都属于结构变化，必须使用对应 begin/end。`dataChanged()` 只适合已有行的数据变化。

### 11.4 QML 自定义 role 没有名字

QML delegate 只能通过 `roleNames()` 暴露的名字访问自定义 role。C++ enum 本身不够。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造函数 | `QAbstractListModel(QObject *parent = nullptr)` | 构造列表模型基类对象 | 抽象类不能直接完整使用，通常由派生模型调用 |
| 析构函数 | `~QAbstractListModel()` | 多态销毁列表模型 | 模型销毁后视图持有的索引都不再可靠 |
| 默认索引实现 | `index(int row, int column = 0, const QModelIndex &parent = QModelIndex()) const` | 返回列表中指定行列的模型索引 | 列表模型通常只接受无效 parent 和第 0 列 |
| 默认兄弟索引 | `sibling(int row, int column, const QModelIndex &idx) const` | 返回同一列表里的兄弟索引 | 主要由视图和委托调用，普通业务很少直接用 |
| 默认项能力 | `flags(const QModelIndex &index) const` | 返回列表项默认可选、可用等能力 | 可编辑、可拖放时通常要重写并追加对应 flag |
| 默认拖放 | `dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent)` | 在列表语义下处理 drop 数据 | 自定义拖放仍要按存储结构重写并发 begin/end 通知 |
| 内置层级行为 | `parent(const QModelIndex &child) const` | 表示列表项没有父子层级 | 由类内部实现，继承列表模型时通常不需要自己实现 |
| 内置列数行为 | `columnCount(const QModelIndex &parent) const` | 默认告诉视图列表只有一列 | 多字段应通过 role 暴露，不要把列表模型写成表格 |
| 内置子项行为 | `hasChildren(const QModelIndex &parent) const` | 表示有效列表项下面没有子项 | lazy loading 顶层数据时仍通过 `canFetchMore()` 和 `fetchMore()` |
| 必须实现 | `rowCount(const QModelIndex &parent) const` | 返回列表顶层行数 | 有效 parent 通常返回 0 |
| 必须实现 | `data(const QModelIndex &index, int role) const` | 返回某行在指定 role 下的数据 | 无效 index 和未知 role 返回无效 `QVariant` |
| 常用重写 | `roleNames() const` | 给自定义 role 提供 QML 可访问名称 | QML 使用列表模型时几乎总要关注 |
| 可编辑重写 | `setData(const QModelIndex &index, const QVariant &value, int role)` | 修改已有行的数据 | 成功后必须发 `dataChanged()` |
| 可编辑重写 | `flags(const QModelIndex &index) const` | 声明某行是否可编辑、可拖放、可勾选 | 和 `setData()`、拖放函数配套 |
| 结构重写 | `insertRows(int row, int count, const QModelIndex &parent)` | 插入连续行 | 使用 `beginInsertRows()` 和 `endInsertRows()` 包住底层修改 |
| 结构重写 | `removeRows(int row, int count, const QModelIndex &parent)` | 删除连续行 | 使用 `beginRemoveRows()` 和 `endRemoveRows()` 包住底层修改 |

## 13. 一句话抓住它

`QAbstractListModel` 是“只有顶层行、通常只有一列、字段靠 role 暴露”的模型基类。写它时，把重点放在 `rowCount()`、`data()`、`roleNames()` 和正确的 begin/end 通知上，就不会把简单列表写成一棵假树。
