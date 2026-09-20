# Qt Widgets 进阶（中）：自定义 Item Model

> 适用版本：Qt 6.11.1  
> 所属模块：Qt Core、Qt Widgets；模型测试还会用到 Qt Test  
> 核心类型：`QAbstractListModel`、`QAbstractTableModel`、`QAbstractItemModel`、`QModelIndex`、`QPersistentModelIndex`、`QAbstractItemModelTester`

上篇解决了“Model/View 各部分是什么”。本篇解决更容易出错的问题：**怎样把自己的业务数据包装成一个符合 Qt 协议的模型**。

自定义模型的本质不是把容器换个名字，而是履行两类契约：

1. **查询契约**：View 给出 `QModelIndex` 和 Role，Model 必须稳定、准确地回答结构和数据。
2. **变更契约**：数据或结构变化时，Model 必须在正确时间通知 View、SelectionModel 和代理模型。

第二类契约尤其重要。界面不刷新、选择错位、代理模型崩溃，通常不是 View 的问题，而是模型漏发信号或发信号的时机错误。

## 1. 应该继承哪一个抽象模型

| 数据结构 | 推荐基类 | 最少需要实现 |
|---|---|---|
| 单列平面列表 | `QAbstractListModel` | `rowCount()`、`data()` |
| 多列平面表格 | `QAbstractTableModel` | `rowCount()`、`columnCount()`、`data()` |
| 有父子层级的树 | `QAbstractItemModel` | 上述三个，再加 `index()`、`parent()` |

若需要编辑，再实现 `setData()` 和 `flags()`；若需要表头，实现 `headerData()`；若需要动态增删，再实现对应的 `insertRows()`、`removeRows()` 等函数。

原则是选择**能准确表达数据的最具体基类**。平面表格没有必要直接继承 `QAbstractItemModel`，因为 `QAbstractTableModel` 已替你正确实现了平面结构的 `index()` 和 `parent()`。

## 2. 构建配置

普通自定义模型和 Widgets 视图：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

若使用本篇后面的 `QAbstractItemModelTester`：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets Test)
target_link_libraries(mytarget PRIVATE Qt6::Widgets Qt6::Test)
```

模型基类属于 Qt Core。链接 `Qt6::Widgets` 时会传递所需的 Core、Gui 依赖。

## 3. 从最小只读列表开始

一个只读字符串列表模型只需要回答两个问题：根下面有多少行，每行显示什么。

```cpp
#include <QAbstractListModel>
#include <QStringList>

class NameModel : public QAbstractListModel
{
public:
    explicit NameModel(QStringList names, QObject *parent = nullptr)
        : QAbstractListModel(parent), m_names(std::move(names))
    {
    }

    int rowCount(const QModelIndex &parent = {}) const override
    {
        if (parent.isValid())
            return 0; // 平面列表中的项没有子项
        return m_names.size();
    }

    QVariant data(const QModelIndex &index,
                  int role = Qt::DisplayRole) const override
    {
        if (!index.isValid() || index.row() >= m_names.size())
            return {};

        if (role == Qt::DisplayRole || role == Qt::EditRole)
            return m_names.at(index.row());

        return {};
    }

private:
    QStringList m_names;
};
```

使用方式：

```cpp
auto *model = new NameModel({"Alice", "Bob", "Carol"}, &window);
auto *view = new QListView(&window);
view->setModel(model);
```

这里没有 `Q_OBJECT`，因为类没有声明自己的信号、槽或属性。它仍然继承了 `QObject` 和 `QAbstractItemModel` 的元对象能力。

### 3.1 为什么 parent 有效时返回 0

所有 Item Model 都用“某个父项下面的二维表”描述结构。平面列表只有根表：

```text
无效 QModelIndex（根）
├─ row 0
├─ row 1
└─ row 2
```

当 View 询问 `row 0` 下面有多少行时，`parent` 是有效索引。列表没有子节点，因此必须返回 0。若不检查，View 会误以为每一项下面又有同样多的子项。

### 3.2 为什么越界返回无效 QVariant

模型函数会被 View、Delegate、代理模型频繁调用。无效索引或不支持的 Role 应返回 `{}`，而不是越界访问容器，也不要为“不支持的 Role”制造伪数据。

调试期可以再加入：

```cpp
Q_ASSERT(checkIndex(index,
    QAbstractItemModel::CheckIndexOption::IndexIsValid |
    QAbstractItemModel::CheckIndexOption::ParentIsInvalid));
```

`checkIndex()` 会验证索引是否属于此模型、行列是否合法，并可按选项验证 parent。它适合尽早暴露模型实现错误。

## 4. 完整可编辑表格模型

下面用业务结构 `Student` 演示查询、编辑、表头、插入和删除。它是可以直接摘入项目的最小完整实现，但仍只作为 Markdown 示例存在。

```cpp
#include <QAbstractTableModel>
#include <QVector>

struct Student
{
    QString name;
    int score = 0;
};

class StudentModel : public QAbstractTableModel
{
public:
    explicit StudentModel(QObject *parent = nullptr)
        : QAbstractTableModel(parent)
    {
    }

    int rowCount(const QModelIndex &parent = {}) const override
    {
        return parent.isValid() ? 0 : m_students.size();
    }

    int columnCount(const QModelIndex &parent = {}) const override
    {
        return parent.isValid() ? 0 : 2;
    }

    QVariant data(const QModelIndex &index,
                  int role = Qt::DisplayRole) const override
    {
        if (!index.isValid()
            || index.row() < 0 || index.row() >= m_students.size()
            || index.column() < 0 || index.column() >= 2) {
            return {};
        }

        const Student &student = m_students.at(index.row());

        if (role == Qt::DisplayRole || role == Qt::EditRole) {
            if (index.column() == 0)
                return student.name;
            return student.score;
        }

        if (role == Qt::TextAlignmentRole && index.column() == 1)
            return Qt::AlignCenter;

        return {};
    }

    QVariant headerData(int section, Qt::Orientation orientation,
                        int role = Qt::DisplayRole) const override
    {
        if (role != Qt::DisplayRole)
            return {};

        if (orientation == Qt::Horizontal) {
            if (section == 0)
                return QStringLiteral("姓名");
            if (section == 1)
                return QStringLiteral("分数");
        }

        return section + 1; // 垂直表头显示 1、2、3……
    }

    Qt::ItemFlags flags(const QModelIndex &index) const override
    {
        if (!index.isValid())
            return Qt::NoItemFlags;
        return QAbstractTableModel::flags(index) | Qt::ItemIsEditable;
    }

    bool setData(const QModelIndex &index, const QVariant &value,
                 int role = Qt::EditRole) override
    {
        if (!index.isValid() || role != Qt::EditRole
            || index.row() < 0 || index.row() >= m_students.size()) {
            return false;
        }

        Student &student = m_students[index.row()];
        bool changed = false;

        if (index.column() == 0) {
            const QString name = value.toString().trimmed();
            if (!name.isEmpty() && name != student.name) {
                student.name = name;
                changed = true;
            }
        } else if (index.column() == 1) {
            bool ok = false;
            const int score = value.toInt(&ok);
            if (ok && score >= 0 && score <= 100
                && score != student.score) {
                student.score = score;
                changed = true;
            }
        }

        if (!changed)
            return false;

        emit dataChanged(index, index,
                         {Qt::DisplayRole, Qt::EditRole});
        return true;
    }

    bool insertRows(int row, int count,
                    const QModelIndex &parent = {}) override
    {
        if (parent.isValid() || row < 0 || row > m_students.size()
            || count <= 0) {
            return false;
        }

        beginInsertRows({}, row, row + count - 1);
        for (int i = 0; i < count; ++i)
            m_students.insert(row + i, Student{QStringLiteral("新同学"), 0});
        endInsertRows();
        return true;
    }

    bool removeRows(int row, int count,
                    const QModelIndex &parent = {}) override
    {
        if (parent.isValid() || row < 0 || count <= 0
            || row + count > m_students.size()) {
            return false;
        }

        beginRemoveRows({}, row, row + count - 1);
        m_students.remove(row, count);
        endRemoveRows();
        return true;
    }

private:
    QVector<Student> m_students {
        {QStringLiteral("张三"), 92},
        {QStringLiteral("李四"), 85}
    };
};
```

接到视图：

```cpp
StudentModel model;
QTableView view;
view.setModel(&model);
view.setEditTriggers(QAbstractItemView::DoubleClicked
                     | QAbstractItemView::EditKeyPressed);
view.show();
```

这个实现体现了六条核心规则：

1. 平面模型只接受无效 parent。
2. 所有传入索引都先检查有效性和边界。
3. `data()` 按 Role 返回数据，不混淆显示值和编辑值。
4. 可编辑项同时需要 `ItemIsEditable` 和 `setData()`。
5. 修改成功后发送 `dataChanged()`。
6. 改变行数时用 `begin.../end...` 包住真实容器操作。

## 5. `data()`：同一单元格的多种表示

一个索引不是只对应一个字符串。Role 表示调用者想要这个 Item 的哪种信息。

| Role | 常见返回值 | 用途 |
|---|---|---|
| `Qt::DisplayRole` | `QString`、数字、日期 | 常规显示 |
| `Qt::EditRole` | 原始可编辑值 | 编辑器读写 |
| `Qt::DecorationRole` | `QIcon`、`QPixmap`、颜色 | 图标或装饰 |
| `Qt::ToolTipRole` | `QString` | 鼠标悬停提示 |
| `Qt::CheckStateRole` | `Qt::CheckState` | 复选状态 |
| `Qt::TextAlignmentRole` | `Qt::Alignment` | 对齐方式 |
| `Qt::ForegroundRole` | `QBrush`、`QColor` | 前景色 |
| `Qt::BackgroundRole` | `QBrush`、`QColor` | 背景色 |
| `Qt::UserRole + n` | 任意 `QVariant` 可承载值 | 业务数据 |

不要把所有逻辑塞入 `DisplayRole`。例如日期可在显示时格式化，在编辑时返回 `QDate`：

```cpp
if (role == Qt::DisplayRole)
    return date.toString(QStringLiteral("yyyy-MM-dd"));
if (role == Qt::EditRole)
    return date;
```

这样 Delegate 可以创建 `QDateEdit`，排序也能针对真正日期而不是格式化字符串。

### 5.1 自定义 Role

```cpp
enum Roles {
    StudentIdRole = Qt::UserRole + 1,
    PassedRole
};

if (role == StudentIdRole)
    return student.id;
if (role == PassedRole)
    return student.score >= 60;
```

Role 适合把同一记录的不同视图数据暴露给 Delegate、代理模型或 QML。不要用行号当业务 ID，插入、排序后行号会变化。

## 6. 编辑协议：`flags()`、`setData()`、`dataChanged()`

三者缺一不可：

```text
flags() 含 ItemIsEditable
        ↓
View 允许启动编辑器
        ↓
Delegate 调用 setData(EditRole)
        ↓
Model 校验并写入业务数据
        ↓
emit dataChanged(...)
        ↓
View、Delegate、Proxy 重新读取数据
```

### 6.1 `setData()` 返回值的含义

- 写入成功并产生变化：返回 `true`。
- 输入非法、Role 不支持、索引非法：返回 `false`。
- 新值与旧值相同：通常返回 `false`，避免无意义刷新。

业务校验应尽量放在模型或更底层业务层，而不是只放在 Delegate。因为数据还可能从命令、脚本或其他 View 被修改。

### 6.2 `dataChanged()` 的范围和 Roles

```cpp
emit dataChanged(index(3, 0), index(3, 2),
                 {Qt::DisplayRole, Qt::EditRole});
```

`topLeft` 和 `bottomRight` 必须属于同一 parent。Roles 为空表示所有 Role 都可能变化；提供准确 Roles 可减少代理和视图的不必要工作。

若表头变化，发送的不是 `dataChanged()`，而是：

```cpp
emit headerDataChanged(Qt::Horizontal, firstColumn, lastColumn);
```

## 7. 结构变更协议是模型正确性的核心

### 7.1 插入

正确顺序：

```cpp
beginInsertRows(parent, first, last); // 此时旧数据仍完整
// 真正插入底层数据
endInsertRows();                      // 此时新数据已经可查询
```

`first`、`last` 是插入完成后新行占据的闭区间。追加 2 行到原有 4 行之后：

```cpp
beginInsertRows(parent, 4, 5);
```

常见错误是先修改容器，再调用 `beginInsertRows()`。此时 Qt 在“即将插入”阶段查询到的已经是新结构，内部索引和选择维护会失去一致性。

### 7.2 删除

```cpp
beginRemoveRows(parent, first, last); // 被删对象仍然存在
// 真正删除底层数据
endRemoveRows();                      // 被删对象已经不存在
```

这让 View 和 `QPersistentModelIndex` 有机会在数据消失前处理状态。

### 7.3 移动

```cpp
if (!beginMoveRows(sourceParent, sourceFirst, sourceLast,
                   destinationParent, destinationChild)) {
    return false;
}
// 移动底层数据
endMoveRows();
```

`destinationChild` 表示移动前目标 parent 中的插入位置。它不是移动完成后的最终行号。同一 parent 内向下移动时尤其容易差一个区间长度。

例如把行 `[1, 2]` 移到原行 5 之前：

```text
移动前：0 [1 2] 3 4 |5| 6
参数：sourceFirst=1, sourceLast=2, destinationChild=5
移动后：0 3 4 [1 2] 5 6
```

若目标落在被移动区间内部或紧邻其结束位置，移动无效，`beginMoveRows()` 会返回 `false`。只有它返回 `true` 后才能修改底层数据并调用 `endMoveRows()`。

### 7.4 不要手动发私有结构信号

不要自己 `emit rowsInserted(...)` 或 `rowsRemoved(...)`。调用 `begin.../end...` 会按正确顺序发送相关信号，并维护持久索引。子类代码应使用受保护的 begin/end API。

## 8. `dataChanged`、结构信号、layout 和 reset 怎么选

| 实际变化 | 应使用的通知 |
|---|---|
| 行列数量和层级不变，只是值改变 | `dataChanged()` |
| 插入或删除连续行列 | `begin/endInsert...`、`begin/endRemove...` |
| 一段行列被移动 | `begin/endMove...` |
| 相同 Item 重新排列，结构规模不变 | `layoutAboutToBeChanged()` / `layoutChanged()`，并维护持久索引 |
| 整个数据集语义上被替换，难以描述差异 | `beginResetModel()` / `endResetModel()` |

### 8.1 reset 为什么应作为最后手段

```cpp
beginResetModel();
m_students = std::move(newStudents);
endResetModel();
```

reset 简单，但会使现有索引失效，并通常丢失选择、当前项、展开状态和滚动上下文。局部变化能用精确信号表达时，不要偷懒 reset。

### 8.2 重新排序与持久索引

若自己用 layout 信号实现排序，应在排列前记录旧持久索引，在排列后计算它们的新索引，并调用：

```cpp
changePersistentIndexList(oldIndexes, newIndexes);
```

然后再发 `layoutChanged()`。简单项目更常见的做法是在下篇使用 `QSortFilterProxyModel`，让源模型保持原顺序。

## 9. 从平面模型进入树模型

树模型必须回答两个互逆问题：

```text
index(row, column, parent) -> parent 的第 row 个孩子
parent(index)              -> index 对应节点的父节点
```

一个常见内部节点结构：

```cpp
#include <memory>
#include <vector>

struct TreeNode
{
    QString text;
    TreeNode *parent = nullptr; // 非拥有指针
    std::vector<std::unique_ptr<TreeNode>> children;

    int rowInParent() const
    {
        if (!parent)
            return 0;
        const auto &siblings = parent->children;
        for (int row = 0; row < static_cast<int>(siblings.size()); ++row) {
            if (siblings[row].get() == this)
                return row;
        }
        return -1;
    }
};
```

所有权由 `unique_ptr` 从根向下拥有，`parent` 只用于向上导航，不负责销毁。

### 9.1 用 `internalPointer()` 定位节点

```cpp
class TreeModel : public QAbstractItemModel
{
public:
    using QAbstractItemModel::QAbstractItemModel;

    QModelIndex index(int row, int column,
                      const QModelIndex &parent = {}) const override
    {
        if (!hasIndex(row, column, parent))
            return {};

        TreeNode *parentNode = parent.isValid()
            ? static_cast<TreeNode *>(parent.internalPointer())
            : m_root.get();

        TreeNode *child = parentNode->children.at(row).get();
        return createIndex(row, column, child);
    }

    QModelIndex parent(const QModelIndex &childIndex) const override
    {
        if (!childIndex.isValid())
            return {};

        auto *child = static_cast<TreeNode *>(childIndex.internalPointer());
        TreeNode *parentNode = child->parent;

        if (!parentNode || parentNode == m_root.get())
            return {}; // 顶层节点的 parent 是无效根索引

        return createIndex(parentNode->rowInParent(), 0, parentNode);
    }

    int rowCount(const QModelIndex &parent = {}) const override
    {
        if (parent.isValid() && parent.column() != 0)
            return 0;

        TreeNode *node = parent.isValid()
            ? static_cast<TreeNode *>(parent.internalPointer())
            : m_root.get();
        return static_cast<int>(node->children.size());
    }

    int columnCount(const QModelIndex & = {}) const override
    {
        return 1;
    }

    QVariant data(const QModelIndex &index,
                  int role = Qt::DisplayRole) const override
    {
        if (!index.isValid() || role != Qt::DisplayRole)
            return {};
        auto *node = static_cast<TreeNode *>(index.internalPointer());
        return node->text;
    }

private:
    std::unique_ptr<TreeNode> m_root = std::make_unique<TreeNode>();
};
```

根节点只是内部哨兵，不对应一个有效 `QModelIndex`。它的 children 才是 View 看到的顶层节点。

### 9.2 为什么 `parent()` 总返回第 0 列

在典型树表中，只有第 0 列承载层级和 children。某节点第 2 列对应索引的 parent，仍应是父节点的第 0 列索引。若不同列各自拥有孩子，结构会变得异常复杂，多数 View 也不按这种模型工作。

### 9.3 内部指针的稳定性

`createIndex()` 存入的指针在索引有效期间必须指向同一节点。危险写法：

```cpp
QVector<TreeNode> children; // 扩容可能整体搬迁，旧指针悬空
```

较稳妥的方案：

- 用 `std::unique_ptr<TreeNode>` 单独分配节点；容器移动的是智能指针，节点地址不变。
- 使用稳定 ID 作为 `internalId()`，每次通过仓库查找节点。
- 在结构变更时严格使用 begin/end 协议，让普通和持久索引得到正确处理。

“地址稳定”不等于“生命周期永远有效”。删除节点时仍必须先 `beginRemoveRows()`，再销毁节点。

### 9.4 `index()` 与 `parent()` 的一致性

对任意有效索引，应满足这种关系：

```cpp
QModelIndex child = model.index(row, column, parent);
Q_ASSERT(model.parent(child) == parent);
```

还应保证同一 parent 下：

```text
0 <= index.row() < rowCount(parent)
0 <= index.column() < columnCount(parent)
```

树只显示一部分、随机崩溃或无限展开，首先检查这组双向关系。

## 10. 懒加载：`canFetchMore()` 与 `fetchMore()`

数据很多或来自远端时，不必一次暴露全部行。模型可以先报告已加载数量，View 需要更多内容时再取下一批。

```cpp
bool canFetchMore(const QModelIndex &parent) const override
{
    return !parent.isValid() && m_loaded < m_allItems.size();
}

void fetchMore(const QModelIndex &parent) override
{
    if (parent.isValid())
        return;

    const int remaining = m_allItems.size() - m_loaded;
    const int count = qMin(100, remaining);
    if (count <= 0)
        return;

    beginInsertRows({}, m_loaded, m_loaded + count - 1);
    m_loaded += count;
    endInsertRows();
}

int rowCount(const QModelIndex &parent = {}) const override
{
    return parent.isValid() ? 0 : m_loaded;
}
```

即使完整数据已经在 `m_allItems` 中，改变“对 View 可见的行数”仍是结构变化，所以必须使用 `beginInsertRows()` / `endInsertRows()`。

真正的网络或数据库异步加载还要维护状态，避免 View 在上一次请求未完成时重复触发：

```text
canFetchMore() = 还有数据 && 当前没有请求
fetchMore()    = 标记请求中并启动异步操作
请求成功        = 在模型线程中 beginInsertRows → 追加 → endInsertRows
请求失败        = 清除请求中状态，并暴露错误或允许重试
```

## 11. 线程边界：后台取数据，主线程改模型

`QAbstractItemModel` 不是线程安全类。连接到 Widget View 的模型通常归属于 GUI 线程，因此：

- 工作线程可以读取文件、查询数据库或解析数据；
- 工作线程不应直接调用模型的 `beginInsertRows()`、`setData()` 等 API；
- 工作线程把纯数据结果通过 queued connection 发送到 GUI 线程；
- 模型在自己的线程中应用结果并发送变更通知。

典型流向：

```text
Worker 线程：读取/计算 -> 生成一批普通值对象
                         |
                         | queued signal
                         v
GUI 线程：Model::appendBatch() -> beginInsertRows -> 写容器 -> endInsertRows
```

槽函数中可用断言确认线程：

```cpp
Q_ASSERT(QThread::currentThread() == thread());
```

不要用互斥锁把“跨线程直接操作 Model”包装成看似安全。View 仍会在 GUI 线程同步查询模型，模型信号的时序也要求在所属线程保持一致。

## 12. 模型所有权与业务数据所有权

`view->setModel(model)` 通常不转移外部模型的所有权。常见做法：

```cpp
auto *model = new StudentModel(&window);
view->setModel(model);
```

但“模型拥有业务数据”不是强制的。三种设计都合理：

| 设计 | 适用场景 | 注意点 |
|---|---|---|
| Model 内部直接存容器 | 小型、单视图数据 | 简单，但业务与 UI 适配层耦合 |
| Model 引用 Repository | 多处共享业务数据 | 明确 Repository 生命周期和通知机制 |
| Model 保存不可变快照 | 异步结果、报表 | 更新常以批次或替换快照进行 |

模型不是数据库，也不一定是真正的数据源；它是 View 能理解的访问协议适配器。

## 13. 性能设计：先找真正的热路径

View 会频繁调用 `rowCount()`、`index()` 和 `data()`，因此这些函数应尽量：

- 不执行网络、磁盘和 SQL 查询；
- 不每次复制整个容器；
- 不做昂贵的格式转换；
- 不产生副作用；
- 对相同输入给出稳定结果。

### 13.1 避免在 `data()` 中查询数据库

错误思路：每次绘制单元格都执行一条 SQL。滚动一次可能触发几百次调用。

更好的思路：

- 批量查询后缓存在模型中；
- 使用分页/懒加载；
- 让数据层生成展示所需快照；
- 数据变化时精确失效缓存。

### 13.2 `multiData()` 是进阶优化点

Qt 6 中 `multiData()` 能一次请求同一索引的多个 Role。只有性能分析确认 Role 查询是热点时才值得覆盖。常规模型先保证 `data()` 正确，Qt 的默认实现会逐个 Role 调用它。

### 13.3 行号查询的复杂度

树模型示例中的 `rowInParent()` 是线性查找，适合小树。超大树可以让节点缓存 row，但每次插入、删除和移动后必须更新受影响兄弟节点的 row。空间、更新成本和查询速度需要权衡。

## 14. 用 `QAbstractItemModelTester` 自动检查契约

许多模型错误不是业务测试能立即发现的。Qt Test 提供 `QAbstractItemModelTester`，它会主动调用模型 API 并检查常见不变量。

```cpp
#include <QAbstractItemModelTester>

StudentModel model;
auto *tester = new QAbstractItemModelTester(
    &model,
    QAbstractItemModelTester::FailureReportingMode::Warning,
    &model);
Q_UNUSED(tester);
```

常见模式：

| 模式 | 行为 |
|---|---|
| `QtTest` | 通过 Qt Test 报告失败，适合测试用例 |
| `Warning` | 输出警告，适合开发期挂到真实模型 |
| `Fatal` | 发现错误后终止，适合强约束调试 |

它能发现大量结构和索引错误，但不能证明业务数据正确，也不能替代对插入、删除、移动和编辑结果的单元测试。

### 14.1 建议测试的行为

```text
初始结构：rowCount / columnCount / headerData
读取：每个 Role 的类型和值
编辑：合法值成功、非法值失败、dataChanged 范围正确
插入：新行位置、内容、rowsInserted 参数
删除：删除后数据和选择是否正确
移动：同 parent 与跨 parent 的边界
重置：旧 PersistentIndex 是否按预期失效
树结构：index(parent(child)) 的互逆关系
懒加载：批次边界、重复请求、最后一批
```

可用 `QSignalSpy` 验证信号：

```cpp
QSignalSpy spy(&model, &QAbstractItemModel::dataChanged);

const QModelIndex score = model.index(0, 1);
QVERIFY(model.setData(score, 95));
QCOMPARE(spy.count(), 1);
QCOMPARE(model.data(score, Qt::DisplayRole).toInt(), 95);
```

## 15. 常见错误与直接后果

### 15.1 修改容器后不通知

后果：View 显示旧内容，代理缓存错误，选中项与真实数据不一致。

### 15.2 先改容器，再 begin

后果：Qt 在 about-to-change 阶段看到错误结构，问题可能延迟到滚动、选择或代理排序时才爆发。

### 15.3 用 `dataChanged()` 通知新增行

`dataChanged()` 只表示已有索引的数据变了，不能改变 `rowCount()` 的结构语义。新增行必须用 insert 协议。

### 15.4 每次刷新都 reset

后果：选择、展开、滚动和持久索引频繁丢失，视图重建成本高。

### 15.5 `setData()` 改了数据却返回 false

调用方会认为提交失败；Delegate 可能保持编辑状态，业务层也无法判断结果。

### 15.6 Role 返回类型漂移

同一 Role 有时返回字符串，有时返回整数，会让 Delegate、排序筛选和 QML 难以稳定处理。Role 的语义和类型应形成固定契约。

### 15.7 保存普通 `QModelIndex` 作为长期业务引用

结构变化后索引可能失效或指向别的行。长期业务引用用稳定 ID；UI 的短期跟踪可用 `QPersistentModelIndex`。

### 15.8 从工作线程直接追加模型行

后果可能从偶发警告到崩溃不等。后台线程只生产纯数据，模型变更排队回模型所属线程。

## 16. API 速查与实现时机

| API | 何时必须/适合覆盖 |
|---|---|
| `rowCount()` | 所有自定义模型 |
| `columnCount()` | 表格和树；List 默认一列 |
| `data()` | 所有自定义模型 |
| `headerData()` | 需要有意义的行列表头 |
| `flags()` | 可编辑、可勾选、拖放等能力 |
| `setData()` | 修改 Item 数据 |
| `index()` / `parent()` | 自定义树模型 |
| `insertRows()` / `removeRows()` | 调用者需要通过标准模型 API 增删 |
| `moveRows()` | 需要保留 Item 身份的重排 |
| `canFetchMore()` / `fetchMore()` | 分批暴露大量数据 |
| `roleNames()` | 主要用于向 QML 暴露自定义命名 Role |
| `sort()` | 源模型自己承担排序；多数场景可用 Proxy |
| `multiData()` | 性能测量证明多 Role 查询是热点 |

注意：业务方法也可以执行结构变更，例如 `appendStudents()` 内部调用 begin/end。只有希望调用方使用通用的 `insertRows()` 接口时，才必须覆盖它。

## 17. 从需求到实现的推荐顺序

1. 画出真实数据结构：列表、表格还是树。
2. 明确 Model 是否拥有数据，业务对象如何保持稳定身份。
3. 先实现只读的 row/column/data，并接到最简单 View。
4. 定义每个 Role 的语义和返回类型。
5. 加 `headerData()` 和显示细节。
6. 加 `flags()`、`setData()` 与精确的 `dataChanged()`。
7. 加插入、删除、移动，并逐一测试边界。
8. 树模型验证 `index()` / `parent()` 互逆和节点地址稳定性。
9. 加 `QAbstractItemModelTester`，尽早暴露协议错误。
10. 最后才做懒加载、缓存和 `multiData()` 等性能优化。

## 18. 自测题

1. 为什么 `QAbstractTableModel` 通常比直接继承 `QAbstractItemModel` 更适合平面表格？
2. 只实现 `setData()` 而不在 `flags()` 中加入 `ItemIsEditable` 会怎样？
3. 插入底层容器和 `beginInsertRows()` 谁先发生？
4. 新值只影响已有单元格内容时，应该 reset 还是发 `dataChanged()`？
5. 树模型中无效 `QModelIndex` 表示什么？
6. `internalPointer()` 指向 `QVector<TreeNode>` 中的元素有什么风险？
7. `fetchMore()` 增加可见行数时为什么也要发送插入协议？
8. 工作线程完成查询后，可以直接调用 GUI 模型的 `beginInsertRows()` 吗？
9. 为什么稳定业务 ID 通常比长期保存 `QModelIndex` 更可靠？
10. `QAbstractItemModelTester` 能否替代业务测试？

## 19. 参考答案

1. 它已经正确实现了平面结构的 `index()` 和 `parent()`，需要自行维护的协议更少。
2. View 会认为该项不可编辑，通常不会启动编辑器，`setData()` 也就不会从正常编辑流程被调用。
3. 先调用 `beginInsertRows()`，再修改容器，最后立即调用 `endInsertRows()`。
4. 发覆盖准确范围和 Role 的 `dataChanged()`；reset 代价过大且会丢失界面状态。
5. 表示不可见的根节点；顶层 Item 都是它的孩子。
6. 容器扩容或搬迁可能改变元素地址，使已保存到 Index 的内部指针悬空。
7. 从 View 看，模型结构由 `m_loaded` 行增长了；结构变化必须让 View、选择和代理同步更新。
8. 不可以。后台线程应传递纯数据，让模型在自身所属的 GUI 线程中应用变更。
9. 行号和普通 Index 会随插入、删除、排序或 reset 改变；稳定 ID 表示业务实体本身。
10. 不能。它检查通用模型不变量，业务规则、实际值和完整交互仍需要专门测试。

## 20. 本篇结论

自定义 Model 最重要的不是覆写多少函数，而是始终维持三个一致性：

```text
模型报告的结构 == 底层数据的真实结构
QModelIndex 的父子关系 == 业务数据的父子关系
变更通知描述的范围和时机 == 实际发生的变化
```

平面数据优先从 `QAbstractListModel` 或 `QAbstractTableModel` 开始；只有树形数据才承担 `index()` / `parent()` 的额外复杂度。所有结构修改都遵循 begin/end 协议，所有跨线程结果都回到模型所属线程应用，再用 `QAbstractItemModelTester` 和针对性单元测试验证行为。

下一篇将继续讲 Delegate、自定义编辑器、`QSortFilterProxyModel`、高级选择、拖放以及大数据视图性能。
