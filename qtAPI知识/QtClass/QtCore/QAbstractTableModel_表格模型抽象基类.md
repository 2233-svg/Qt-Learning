# QAbstractTableModel 表格模型抽象基类深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAbstractTableModel>`  
> 所属模块：`Qt6::Core`  
> 继承关系：`QObject -> QAbstractItemModel -> QAbstractTableModel`

## 1. 它解决什么问题

`QAbstractTableModel` 是专门给二维表格数据准备的模型基类。它把 `QAbstractItemModel` 的通用树形接口压扁成一个表格：顶层有多行多列，但每个单元格下面没有子节点。

典型数据长这样：

```text
row 0: name, age, city
row 1: name, age, city
row 2: name, age, city
```

或者：

```text
QVector<Record>
    Record { name, age, city }
```

在这种结构里，行表示记录，列表示字段。你不需要手写 `parent()` 来维护树结构，`QAbstractTableModel` 已经帮你提供了非层级模型的默认实现。

## 2. 它和 `QAbstractItemModel`、`QAbstractListModel` 的区别

`QAbstractItemModel` 是最通用的树形接口；`QAbstractListModel` 是一维列表；`QAbstractTableModel` 是二维表格。

如果你需要这些能力，适合用 `QAbstractTableModel`：

- `QTableView` 显示多列数据；
- `QListView` 临时显示表格的某一列或默认列；
- 每一行是一条记录，每一列是字段；
- 需要表头；
- 需要按列编辑、排序、拖放或导出。

如果每一行是对象，字段主要给 QML delegate 用，优先考虑 `QAbstractListModel` 加自定义 role。如果每个节点还有孩子，使用 `QAbstractItemModel`。

## 3. 最小只读表格模型

继承 `QAbstractTableModel` 时，最小只读模型通常实现：

```cpp
int rowCount(const QModelIndex &parent = QModelIndex()) const override;
int columnCount(const QModelIndex &parent = QModelIndex()) const override;
QVariant data(const QModelIndex &index,
              int role = Qt::DisplayRole) const override;
```

示例：

```cpp
class PersonTableModel : public QAbstractTableModel
{
    Q_OBJECT

public:
    explicit PersonTableModel(QObject *parent = nullptr)
        : QAbstractTableModel(parent)
    {
    }

    int rowCount(const QModelIndex &parent = QModelIndex()) const override
    {
        return parent.isValid() ? 0 : m_people.size();
    }

    int columnCount(const QModelIndex &parent = QModelIndex()) const override
    {
        return parent.isValid() ? 0 : 3;
    }

    QVariant data(const QModelIndex &index,
                  int role = Qt::DisplayRole) const override
    {
        if (!index.isValid() || role != Qt::DisplayRole)
            return {};

        const Person &person = m_people.at(index.row());

        switch (index.column()) {
        case 0:
            return person.name;
        case 1:
            return person.age;
        case 2:
            return person.city;
        default:
            return {};
        }
    }

private:
    QVector<Person> m_people;
};
```

这里仍然检查 `parent.isValid()`。表格模型没有层级，所以当视图问“某个单元格下面有多少行列”时，应该返回 0。

## 4. 表头：表格模型通常应该实现

表格没有表头也能显示，但可读性会很差。常见写法是重写 `headerData()`：

```cpp
QVariant PersonTableModel::headerData(int section,
                                      Qt::Orientation orientation,
                                      int role) const
{
    if (role != Qt::DisplayRole)
        return {};

    if (orientation == Qt::Horizontal) {
        switch (section) {
        case 0:
            return tr("Name");
        case 1:
            return tr("Age");
        case 2:
            return tr("City");
        default:
            return {};
        }
    }

    return section + 1;
}
```

如果表头也能编辑，就重写 `setHeaderData()`。成功修改后必须发 `headerDataChanged()`，否则视图不会更新表头。

## 5. 可编辑表格模型

表格编辑和列表编辑一样，需要 `flags()` 与 `setData()` 配套。

```cpp
Qt::ItemFlags PersonTableModel::flags(const QModelIndex &index) const
{
    if (!index.isValid())
        return Qt::NoItemFlags;

    return QAbstractTableModel::flags(index)
        | Qt::ItemIsEditable;
}

bool PersonTableModel::setData(const QModelIndex &index,
                               const QVariant &value,
                               int role)
{
    if (!index.isValid() || role != Qt::EditRole)
        return false;

    Person &person = m_people[index.row()];

    switch (index.column()) {
    case 0:
        person.name = value.toString();
        break;
    case 1:
        person.age = value.toInt();
        break;
    case 2:
        person.city = value.toString();
        break;
    default:
        return false;
    }

    emit dataChanged(index, index, { Qt::DisplayRole, Qt::EditRole });
    return true;
}
```

如果一次修改整行，可以发从该行第 0 列到最后一列的 `dataChanged()`。如果一次修改整列，也可以发从第一行到最后一行的范围。范围必须是同一个父节点下的矩形区域，表格模型里通常就是根层级。

## 6. 插入、删除行列

表格模型的结构变化分两类：行变化和列变化。行通常对应记录，列通常对应字段。

插入行：

```cpp
bool PersonTableModel::insertRows(int row,
                                  int count,
                                  const QModelIndex &parent)
{
    if (parent.isValid() || row < 0 || count < 0)
        return false;

    if (row > m_people.size())
        return false;

    beginInsertRows(parent, row, row + count - 1);
    insertEmptyPeople(row, count);
    endInsertRows();

    return true;
}
```

删除列：

```cpp
bool MatrixModel::removeColumns(int column,
                                int count,
                                const QModelIndex &parent)
{
    if (parent.isValid() || column < 0 || count < 0)
        return false;

    if (column + count > m_columnCount)
        return false;

    beginRemoveColumns(parent, column, column + count - 1);
    removeColumnsFromStorage(column, count);
    endRemoveColumns();

    return true;
}
```

只要改变 `rowCount()` 或 `columnCount()` 的结果，就必须用对应 begin/end。修改某个单元格内容才用 `dataChanged()`。

## 7. 默认 `index()` 和无父子层级

`QAbstractTableModel` 已经实现了：

- `index(row, column, parent)`；
- `sibling(row, column, idx)`；
- `parent(child)` 的非层级语义；
- `hasChildren(parent)` 的表格语义。

这意味着你通常不需要自己创建 `QModelIndex`。视图调用 `index(row, column)` 时，默认实现会为顶层表格单元创建索引；当 parent 有效时，它不会继续创建子节点。

如果你的“表格单元”下面还有子行，说明这不是普通表格模型，而是树表模型，应该回到 `QAbstractItemModel`。

## 8. 排序：源模型排序还是代理排序

`QAbstractTableModel` 继承了 `sort(column, order)`。如果你想让源模型自己改变行顺序，可以重写它：

```cpp
void PersonTableModel::sort(int column, Qt::SortOrder order)
{
    emit layoutAboutToBeChanged();

    sortStorageByColumn(column, order);

    emit layoutChanged();
}
```

真实项目里还要考虑 `QPersistentModelIndex`，否则排序后用户选择的行可能指向错误记录。很多场景更适合把源模型保持原顺序，再用 `QSortFilterProxyModel` 做排序和过滤，这样源数据模型更干净。

## 9. 拖放在表格模型里的语义

表格拖放要明确目标位置是行、列还是单元格：

- 拖整行：drop 到某个 row，通常改变记录顺序。
- 拖整列：drop 到某个 column，通常改变字段顺序。
- 拖单元格：只修改一个或多个 index 的数据。

相关函数来自 `QAbstractItemModel`：

- `mimeTypes()`；
- `mimeData()`；
- `canDropMimeData()`；
- `dropMimeData()`；
- `supportedDragActions()`；
- `supportedDropActions()`；
- `flags()`。

`QAbstractTableModel` 重写了 `dropMimeData()` 以适配表格坐标，但如果业务拖放要修改存储结构，仍要自己重写并使用 begin/end 或 `dataChanged()`。

## 10. 线程安全

`QAbstractTableModel` 文档明确提醒：它是 `QObject` 子类，模型相关 API 不线程安全。和视图连接的表格模型通常属于 GUI 线程。

后台线程可以读取数据库或计算结果，但不要直接调用模型 API。正确方式是把结果投递到模型线程，然后在模型线程里：

```cpp
beginInsertRows({}, first, last);
appendRowsOnModelThread(rows);
endInsertRows();
```

同理，`dataChanged()`、`beginResetModel()`、`layoutChanged()` 都应该在模型所属线程发出。

## 11. 常见误区

### 11.1 忘记有效 parent 返回 0

表格没有子节点。`rowCount(validParent)` 和 `columnCount(validParent)` 通常应返回 0。

### 11.2 用 role 做列，或者用列做 role

表格模型中，列通常是字段位置，role 是同一单元格的不同表现方式。例如第 1 列是年龄，`DisplayRole` 返回显示文本，`EditRole` 返回编辑值，`TextAlignmentRole` 返回对齐方式。

### 11.3 改了行列数只发 `dataChanged()`

`dataChanged()` 不会告诉视图行数或列数改变。行列插入删除必须使用 begin/end。

### 11.4 排序后不维护选择和 persistent index

源模型自己排序时，选中项、当前项、持久索引都可能需要更新。简单发 `layoutChanged()` 只能刷新显示，不能自动理解你的业务对象身份。

### 11.5 明明是树表却继承 `QAbstractTableModel`

如果每一行还能展开子行，应继承 `QAbstractItemModel`。`QAbstractTableModel` 的默认父子语义就是无层级。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造函数 | `QAbstractTableModel(QObject *parent = nullptr)` | 构造表格模型基类对象 | 抽象类不能直接完整使用，通常由派生模型调用 |
| 析构函数 | `~QAbstractTableModel()` | 多态销毁表格模型 | 模型销毁后视图持有的索引都不再可靠 |
| 默认索引实现 | `index(int row, int column, const QModelIndex &parent = QModelIndex()) const` | 返回表格中指定单元格的模型索引 | 表格模型通常只接受无效 parent |
| 默认兄弟索引 | `sibling(int row, int column, const QModelIndex &idx) const` | 返回同一表格中的兄弟单元格索引 | 主要由视图和委托调用 |
| 默认项能力 | `flags(const QModelIndex &index) const` | 返回单元格默认可选、可用等能力 | 可编辑、可拖放时通常要重写并追加对应 flag |
| 默认拖放 | `dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent)` | 在表格语义下处理 drop 数据 | 自定义拖放仍要按存储结构重写并正确通知 |
| 内置层级行为 | `parent(const QModelIndex &child) const` | 表示表格单元没有父子层级 | 由类内部实现，普通表格模型不用自己写 |
| 内置子项行为 | `hasChildren(const QModelIndex &parent) const` | 表示根可能有子项，单元格没有子项 | 有效 parent 下通常没有孩子 |
| 必须实现 | `rowCount(const QModelIndex &parent) const` | 返回根层级的行数 | 有效 parent 通常返回 0 |
| 必须实现 | `columnCount(const QModelIndex &parent) const` | 返回根层级的列数 | 有效 parent 通常返回 0 |
| 必须实现 | `data(const QModelIndex &index, int role) const` | 返回某个单元格在指定 role 下的数据 | 用 `index.row()` 和 `index.column()` 定位真实数据 |
| 常用重写 | `headerData(int section, Qt::Orientation orientation, int role) const` | 返回行头或列头内容 | 表格模型通常应提供水平表头 |
| 可编辑重写 | `setData(const QModelIndex &index, const QVariant &value, int role)` | 修改已有单元格数据 | 成功后必须发 `dataChanged()` |
| 可编辑重写 | `flags(const QModelIndex &index) const` | 声明单元格是否可编辑、可拖放、可勾选 | 和 `setData()`、拖放函数配套 |
| 结构重写 | `insertRows(int row, int count, const QModelIndex &parent)` | 插入连续行 | 使用 `beginInsertRows()` 和 `endInsertRows()` 包住底层修改 |
| 结构重写 | `removeRows(int row, int count, const QModelIndex &parent)` | 删除连续行 | 使用 `beginRemoveRows()` 和 `endRemoveRows()` 包住底层修改 |
| 结构重写 | `insertColumns(int column, int count, const QModelIndex &parent)` | 插入连续列 | 使用 `beginInsertColumns()` 和 `endInsertColumns()` 包住底层修改 |
| 结构重写 | `removeColumns(int column, int count, const QModelIndex &parent)` | 删除连续列 | 使用 `beginRemoveColumns()` 和 `endRemoveColumns()` 包住底层修改 |
| 排序重写 | `sort(int column, Qt::SortOrder order)` | 按指定列调整源模型行顺序 | 可优先考虑 `QSortFilterProxyModel`，源模型排序要维护 persistent index |

## 13. 一句话抓住它

`QAbstractTableModel` 是“根层级二维表格”的模型基类：行列表示数据坐标，role 表示同一单元格的不同表现，结构变化靠 begin/end，普通单元格下面不再有孩子。
