# Qt QTransposeProxyModel：把模型的行列坐标互换

`QTransposeProxyModel` 是一个只改变模型坐标解释方式的代理模型。它不复制源模型的数据，也不负责重新排序；它把源模型的每一行看成代理模型的一列，把源模型的每一列看成代理模型的一行，然后把数据、编辑操作和结构变化转发到源模型。

它适合把“按记录排列”的模型临时改成“按字段排列”的展示方式。例如源模型有 2 行、3 列：

```text
源模型                         代理模型
       C0   C1   C2                   C0   C1
R0     a    b    c             R0     a    d
R1     d    e    f             R1     b    e
                                   R2     c    f
```

代理模型中的 `(row = 1, column = 0)` 对应源模型中的 `(row = 0, column = 1)`。视图只需要绑定代理模型，就能看到转置后的布局。

```cpp
#include <QStandardItemModel>
#include <QTableView>
#include <QTransposeProxyModel>

QStandardItemModel source(2, 3);
source.setData(source.index(0, 0), QStringLiteral("a"));
source.setData(source.index(0, 1), QStringLiteral("b"));
source.setData(source.index(0, 2), QStringLiteral("c"));
source.setData(source.index(1, 0), QStringLiteral("d"));
source.setData(source.index(1, 1), QStringLiteral("e"));
source.setData(source.index(1, 2), QStringLiteral("f"));

auto *transpose = new QTransposeProxyModel;
transpose->setSourceModel(&source);

auto *view = new QTableView;
view->setModel(transpose);
view->show();
```

## 它解决什么问题

模型和视图之间通常约定“第一个坐标是行，第二个坐标是列”。当同一份数据需要以另一种方向展示时，直接改写源模型会带来几个问题：

- 业务模型的行列含义被展示需求污染；
- 编辑、表头和结构变化需要在多个地方重复处理；
- 同一份源数据难以同时被普通视图和转置视图使用；
- 树模型中的父索引不能只交换当前索引的 `row()` 和 `column()`，否则层级关系会断裂。

`QTransposeProxyModel` 把这些坐标转换集中在代理层。源模型仍然保存真实数据，代理模型只负责提供另一套 `QAbstractItemModel` 接口。

它不是以下类型：

- 不是数据拷贝工具。调用 `mapToSource()` 得到的索引仍然指向源模型。
- 不是排序模型。它的 `sort()` 明确不执行任何操作。
- 不是把任意控件旋转 90 度的布局工具。它只改变模型索引的行列解释。
- 不是通用的二维数组转置算法。源模型的父子结构、角色数据和变更通知仍然遵守模型/视图协议。

## 构建与包含

`QTransposeProxyModel` 属于 Qt Core。使用 CMake 时链接 `Qt6::Core`：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QTransposeProxyModel>
```

qmake 工程使用：

```text
QT += core
```

头文件内部要求 `transposeproxymodel` 配置特性。官方完整 Qt 构建通常已经启用；如果使用裁剪过的 Qt，必须确认该特性没有被禁用。

## 最小使用流程

实际使用通常只有四步：

1. 创建源模型。
2. 创建 `QTransposeProxyModel`。
3. 调用 `setSourceModel()` 接入源模型。
4. 把视图或下一级代理绑定到转置代理。

```cpp
auto *transpose = new QTransposeProxyModel(this);
transpose->setSourceModel(sourceModel);
tableView->setModel(transpose);
```

代理不拥有 `sourceModel`。源模型可以是栈对象，也可以由其他 `QObject` 管理，但它必须在代理使用期间保持有效。通常让源模型和代理由同一个更长生命周期的对象管理，并在销毁顺序上保证源模型不会被提前释放。

如果没有设置源模型，或者源模型已经被销毁，基类会让代理表现为空模型。此时行数、列数和映射结果都不能按真实数据模型来假设。

## 转置规则：先记住索引公式

对于没有父索引的普通表模型，规则可以写成：

```text
proxy(row, column) <=> source(column, row)
```

因此：

```cpp
QModelIndex sourceIndex = sourceModel->index(0, 1);
QModelIndex proxyIndex = transpose->mapFromSource(sourceIndex);

Q_ASSERT(proxyIndex.row() == 1);
Q_ASSERT(proxyIndex.column() == 0);
Q_ASSERT(transpose->mapToSource(proxyIndex) == sourceIndex);
```

若源模型的根节点有 `sourceRows` 行、`sourceColumns` 列，则代理根节点有：

```text
proxy rowCount    = source columnCount
proxy columnCount = source rowCount
```

这两个数量必须按父索引分别计算。树模型中每个父节点都可能有不同的行列数，不能只在初始化时交换一次全局行数和列数。

## 树模型中的父索引

转置不仅交换当前索引的坐标，也交换父索引的坐标。源模型中某个索引的父索引如果是：

```cpp
sourceParent = sourceModel->index(2, 0, sourceGrandParent);
```

那么对应的代理父索引是：

```cpp
proxyParent = transpose->mapFromSource(sourceParent);
// proxyParent 的坐标是 (0, 2)
```

代理中的子索引再以这个转置后的父索引为父：

```cpp
QModelIndex proxyChild = transpose->index(1, 3, proxyParent);
QModelIndex sourceChild = transpose->mapToSource(proxyChild);
// sourceChild 对应 sourceModel->index(3, 1, sourceParent)
```

`parent()` 也遵守同一规则。不要只交换 `QModelIndex::row()` 和 `column()` 后自己构造一个索引，因为 `QModelIndex` 还携带模型对象、内部指针和父子关系；正确做法是使用 `mapToSource()`、`mapFromSource()` 或代理自己的 `index()`。

## 数据、角色和编辑

`QTransposeProxyModel` 没有重新声明 `data()`、`setData()` 和 `flags()`，这些能力由 `QAbstractProxyModel` 继承实现。基类会把代理索引映射到源索引，再向源模型查询或写入。

这意味着：

- `data(proxyIndex, role)` 读取的是 `data(mapToSource(proxyIndex), role)`；
- `setData(proxyIndex, value, role)` 最终修改源模型；
- `flags(proxyIndex)` 反映源模型是否允许选择、编辑、拖放等操作；
- `itemData()` 和 `setItemData()` 会转发整组角色；
- 源模型发出的 `dataChanged` 会被代理转换为对应的代理索引范围。

如果源模型没有实现编辑，或者目标索引的标志不包含 `Qt::ItemIsEditable`，在代理上调用 `setData()` 也不会凭空获得编辑能力。代理只转换坐标，不改变源模型的权限和业务校验。

```cpp
const QModelIndex proxyIndex = transpose->index(1, 0);
const bool changed = transpose->setData(
    proxyIndex, QStringLiteral("new value"), Qt::EditRole);

// 实际写入的是源模型的 (0, 1)
Q_ASSERT(transpose->mapToSource(proxyIndex) == sourceModel->index(0, 1));
```

## 表头方向也会互换

代理的水平表头描述源模型的垂直表头，代理的垂直表头描述源模型的水平表头：

```text
proxy Qt::Horizontal -> source Qt::Vertical
proxy Qt::Vertical   -> source Qt::Horizontal
```

所以 `headerData()` 和 `setHeaderData()` 不只是原样转发 `orientation`。如果源模型把字段名放在水平表头，而转置后字段变成代理的行，视图仍能通过正确的方向映射显示这些标题。

表头内容是否存在、是否可编辑，仍由源模型决定。调用 `setHeaderData()` 返回 `false` 时，应检查源模型是否实现了对应方向和角色的写入。

## 增删和移动操作

行列互换也会影响结构操作。可以按下面的对应关系理解：

| 代理操作 | 实际转发到源模型 |
| --- | --- |
| `insertRows()` | `sourceModel->insertColumns()` |
| `removeRows()` | `sourceModel->removeColumns()` |
| `moveRows()` | `sourceModel->moveColumns()` |
| `insertColumns()` | `sourceModel->insertRows()` |
| `removeColumns()` | `sourceModel->removeRows()` |
| `moveColumns()` | `sourceModel->moveRows()` |

父索引和位置参数也会随坐标系一起转换。比如在代理中插入一行，源模型看到的是在相应源父节点下插入一列。返回值直接反映源模型是否接受操作；代理不会为不支持结构修改的源模型提供模拟存储。

结构变更必须由源模型按 `beginInsertRows()`、`endInsertRows()` 等协议发出正确通知。代理会把源模型的行变化转换成代理的列变化，把源模型的列变化转换成代理的行变化。应用代码不应该为了“帮助代理刷新”而额外调用 `beginResetModel()` 或手动发射模型内部信号。

## 排序：`sort()` 故意不做任何事

这是本类最容易误用的 API。`QTransposeProxyModel::sort()` 的文档明确规定它不执行任何动作。即使视图调用了代理的 `sort()`，源模型和代理的顺序也不会改变。

需要在转置结果上排序时，把 `QSortFilterProxyModel` 放在转置代理上面：

```text
sourceModel
    -> QTransposeProxyModel
        -> QSortFilterProxyModel
            -> view
```

```cpp
auto *transpose = new QTransposeProxyModel(this);
transpose->setSourceModel(sourceModel);

auto *sorted = new QSortFilterProxyModel(this);
sorted->setSourceModel(transpose);
sorted->setSortRole(Qt::DisplayRole);
sorted->sort(0, Qt::AscendingOrder);

tableView->setModel(sorted);
```

这种链路的排序列是转置后模型的列。若需求是改变源模型本身的业务顺序，应直接调用源模型提供的排序接口，或者在转置代理之前安排一个适合的排序代理，不能把 `QTransposeProxyModel::sort()` 当成排序入口。

## span 和选择映射

`span()` 会把源索引的行列跨度转成代理坐标中的跨度。通常可以把返回的 `QSize` 宽高理解为互换后的结果。源模型不支持单元格合并时，结果一般就是默认的 `QSize(1, 1)`。

选择映射由 `QAbstractProxyModel` 的通用实现提供。需要在源模型和代理模型之间同步选择时，使用 `mapSelectionToSource()` 和 `mapSelectionFromSource()`，不要遍历选区后只交换每个索引的整数坐标。对树模型、多范围选区和结构变化频繁的模型，应在实际视图中验证选区边界。

## 生命周期、线程与索引有效性

`QTransposeProxyModel` 是 `QObject`，不能拷贝。构造函数的 `parent` 只管理代理自身的生命周期，不会自动接管源模型。

模型/代理链通常应位于同一个线程，并由该线程的事件循环处理模型通知。Qt 的模型接口不是一个可以从任意线程并发读写的通用容器。后台线程准备数据时，应通过受控的数据交换或信号把变更交给模型所属线程；不要让视图线程和工作线程同时调用同一个模型的结构修改接口。

源模型发生重置、插入、删除、移动或布局变化后，之前保存的 `QModelIndex` 可能失效。需要跨变化保存索引时，使用 `QPersistentModelIndex`，并仍然遵守源模型发出的变更通知边界。映射函数也只能接收属于相应模型的索引：

- `mapFromSource()` 需要源模型的索引；
- `mapToSource()` 需要该代理的索引；
- 把另一个模型的索引传入属于逻辑错误，不能依赖返回值“自动修正”。

## 常见使用场景

### 属性表或参数检查器

源模型可以按对象排列，每一行是一个对象、每一列是一个属性。转置后，每一列对应一个对象，适合在屏幕较窄但对象较少时横向比较。

### 日志或实验结果的方向切换

数据导出和内部计算常按记录存储，用户却可能希望按指标浏览。转置代理能提供一个只读的浏览视图，而不改变导出模型的列定义。

### 复用编辑模型

同一源模型可以连接到普通表格视图和转置视图。只要源模型的角色、编辑权限和结构通知实现正确，两个视图都能通过代理访问同一份数据。

### 作为代理链中的一个几何变换

它可以与筛选、排序代理组合。要注意每一层代理都有自己的坐标系，调用 `mapToSource()` 时要逐层映射，不能把最终视图索引直接拿给最底层源模型。

## 常见错误与排查顺序

- 把 `QTransposeProxyModel` 当成排序器。先确认是否需要在它上面叠加 `QSortFilterProxyModel`。
- 只交换当前索引的行列，却忽略 `parent()`。树模型必须连父索引一起转置。
- 手工构造代理索引或源索引。应调用 `mapToSource()` 和 `mapFromSource()`。
- 把代理的行操作直接当成源模型的行操作。代理行对应源模型列，增删移动方向是反的。
- 忘记表头方向也要交换，导致字段名显示在错误的表头。
- 以为代理会复制数据。源模型释放后代理只剩空模型，代理不会保留数据快照。
- 源模型更新后继续使用普通 `QModelIndex`。检查模型通知和索引生命周期。
- 从错误线程直接修改模型。把操作投递到模型所属线程，并让事件循环处理通知。
- 在源模型不支持编辑或结构修改时期待代理“补齐能力”。代理只转发，不改变源模型契约。
- 把不属于该代理或源模型的 `QModelIndex` 传给映射函数。

## 逐项 API 说明

### 构造与源模型

#### `QTransposeProxyModel::QTransposeProxyModel(QObject *parent = nullptr)`

创建一个转置代理。构造后尚未连接源模型，代理表现为空模型；`parent` 只用于 QObject 父子关系。

#### `QTransposeProxyModel::~QTransposeProxyModel()`

销毁代理并断开其与源模型的连接。代理不负责销毁源模型。

#### `void QTransposeProxyModel::setSourceModel(QAbstractItemModel *newSourceModel)`

设置要被转置的源模型。设置新源模型后，代理会重新建立内部连接并以新模型的结构为准。传入 `nullptr` 等价于让代理回到空模型状态。

这是继承的 `sourceModel` 属性的 setter。调用方不应同时手工连接源模型的所有结构信号来刷新代理，因为代理已经负责坐标转换和通知转发。

### 尺寸与索引

#### `int QTransposeProxyModel::rowCount(const QModelIndex &parent = QModelIndex()) const`

返回代理父节点下的行数，实质上查询对应源父节点下的列数。对根节点而言，代理行数等于源模型列数。

#### `int QTransposeProxyModel::columnCount(const QModelIndex &parent = QModelIndex()) const`

返回代理父节点下的列数，实质上查询对应源父节点下的行数。对根节点而言，代理列数等于源模型行数。

#### `QModelIndex QTransposeProxyModel::index(int row, int column, const QModelIndex &parent = QModelIndex()) const`

创建代理索引，并把坐标映射为源模型中的 `(column, row)`。越界位置、错误父索引或没有源模型时，结果可能是无效索引。

#### `QModelIndex QTransposeProxyModel::parent(const QModelIndex &index) const`

返回代理索引的转置父索引。树模型中不能用简单的 `row()`、`column()` 交换替代它。

#### `QModelIndex QTransposeProxyModel::mapFromSource(const QModelIndex &sourceIndex) const`

把属于源模型的索引转换为代理索引。源坐标 `(sourceRow, sourceColumn)` 变成代理坐标 `(sourceColumn, sourceRow)`，父索引也递归转换。

#### `QModelIndex QTransposeProxyModel::mapToSource(const QModelIndex &proxyIndex) const`

把属于该代理的索引转换回源模型索引。它是 `mapFromSource()` 的逆方向；对有效索引进行往返映射时，应回到同一个源位置。

### 数据与表头

#### `QVariant QTransposeProxyModel::headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const`

查询转置后的表头数据。代理水平表头查询源垂直表头，代理垂直表头查询源水平表头；`role` 原样参与查询。

#### `bool QTransposeProxyModel::setHeaderData(int section, Qt::Orientation orientation, const QVariant &value, int role = Qt::EditRole)`

设置转置后的表头数据，并把方向转换后交给源模型。返回值表示源模型是否接受了修改。

#### `QMap<int, QVariant> QTransposeProxyModel::itemData(const QModelIndex &index) const`

查询代理索引的全部角色数据。索引会先映射到源模型，返回的角色和值来自源模型。

#### `bool QTransposeProxyModel::setItemData(const QModelIndex &index, const QMap<int, QVariant> &roles)`

一次设置代理索引的多个角色。只有 `roles` 中出现的角色会被请求修改，最终结果由源模型决定。

#### `QSize QTransposeProxyModel::span(const QModelIndex &index) const`

查询索引的行列跨度，并转换为代理坐标。通常表现为把源跨度的宽高互换；源模型不支持跨度时使用其默认结果。

### 结构修改

#### `bool QTransposeProxyModel::insertRows(int row, int count, const QModelIndex &parent = QModelIndex())`

在代理中插入行，实际请求源模型在对应位置插入列。`count` 必须符合源模型结构操作的约束，失败时返回 `false`。

#### `bool QTransposeProxyModel::removeRows(int row, int count, const QModelIndex &parent = QModelIndex())`

从代理中移除行，实际请求源模型移除列。不要把它理解为删除源模型的行。

#### `bool QTransposeProxyModel::moveRows(const QModelIndex &sourceParent, int sourceRow, int count, const QModelIndex &destinationParent, int destinationChild)`

移动代理中的行，实际转发为源模型中的列移动。两个父索引和位置参数都要按转置关系解释，最终能否移动由源模型决定。

#### `bool QTransposeProxyModel::insertColumns(int column, int count, const QModelIndex &parent = QModelIndex())`

在代理中插入列，实际请求源模型在对应位置插入行。

#### `bool QTransposeProxyModel::removeColumns(int column, int count, const QModelIndex &parent = QModelIndex())`

从代理中移除列，实际请求源模型移除行。

#### `bool QTransposeProxyModel::moveColumns(const QModelIndex &sourceParent, int sourceColumn, int count, const QModelIndex &destinationParent, int destinationChild)`

移动代理中的列，实际转发为源模型中的行移动。它与 `moveRows()` 的方向相反。

### 排序

#### `void QTransposeProxyModel::sort(int column, Qt::SortOrder order = Qt::AscendingOrder)`

故意不执行任何操作。需要排序时，在转置代理上方使用 `QSortFilterProxyModel`，或者直接让源模型执行明确的业务排序。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QTransposeProxyModel(QObject *parent = nullptr)` | 创建转置代理 | 初始没有源模型；`parent` 只管理代理生命周期 |
| `~QTransposeProxyModel()` | 销毁代理 | 断开内部连接；不销毁源模型 |
| `setSourceModel(QAbstractItemModel *newSourceModel)` | 设置源模型 | 代理不取得源模型所有权；设置 `nullptr` 后表现为空模型 |
| `rowCount(const QModelIndex &parent = {}) const` | 查询代理行数 | 等于对应源父节点的列数 |
| `columnCount(const QModelIndex &parent = {}) const` | 查询代理列数 | 等于对应源父节点的行数 |
| `index(int row, int column, const QModelIndex &parent = {}) const` | 创建代理索引 | 代理 `(row, column)` 对应源 `(column, row)` |
| `parent(const QModelIndex &index) const` | 查询代理父索引 | 父索引也必须转置，树模型尤其重要 |
| `mapFromSource(const QModelIndex &sourceIndex) const` | 源索引转代理索引 | 需要传入属于源模型的索引；父链递归转换 |
| `mapToSource(const QModelIndex &proxyIndex) const` | 代理索引转源索引 | 需要传入属于该代理的索引；可与 `mapFromSource()` 往返 |
| `headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const` | 查询代理表头 | 水平/垂直方向映射到源模型的相反方向 |
| `setHeaderData(int section, Qt::Orientation orientation, const QVariant &value, int role = Qt::EditRole)` | 设置代理表头 | 转发到源模型；返回源模型是否接受 |
| `itemData(const QModelIndex &index) const` | 查询全部角色 | 先映射索引，再读取源模型角色数据 |
| `setItemData(const QModelIndex &index, const QMap<int, QVariant> &roles)` | 批量设置角色 | 只修改传入的角色；能力取决于源模型 |
| `span(const QModelIndex &index) const` | 查询单元格跨度 | 通常交换源跨度的宽高 |
| `insertRows(int row, int count, const QModelIndex &parent = {})` | 插入代理行 | 实际插入源模型列 |
| `removeRows(int row, int count, const QModelIndex &parent = {})` | 删除代理行 | 实际删除源模型列 |
| `moveRows(const QModelIndex &, int sourceRow, int count, const QModelIndex &, int destinationChild)` | 移动代理行 | 实际移动源模型列 |
| `insertColumns(int column, int count, const QModelIndex &parent = {})` | 插入代理列 | 实际插入源模型行 |
| `removeColumns(int column, int count, const QModelIndex &parent = {})` | 删除代理列 | 实际删除源模型行 |
| `moveColumns(const QModelIndex &, int sourceColumn, int count, const QModelIndex &, int destinationChild)` | 移动代理列 | 实际移动源模型行 |
| `sort(int column, Qt::SortOrder order = Qt::AscendingOrder)` | 响应排序请求 | 本类明确不做任何事；用上层 `QSortFilterProxyModel` 排序 |
| `sourceModel() const` | 读取当前源模型 | 从 `QAbstractProxyModel` 继承；源模型为空或已销毁时不可按真实数据使用 |
| `data(const QModelIndex &, int role = Qt::DisplayRole) const` | 读取代理单元格 | 从 `QAbstractProxyModel` 继承；通过 `mapToSource()` 读取源模型 |
| `setData(const QModelIndex &, const QVariant &, int role = Qt::EditRole)` | 修改代理单元格 | 从 `QAbstractProxyModel` 继承；不会增加源模型的编辑能力 |
| `flags(const QModelIndex &) const` | 查询代理索引能力 | 从源模型转发选择、编辑和拖放等标志 |
| `mapSelectionToSource(const QItemSelection &) const` | 代理选区转源选区 | 从 `QAbstractProxyModel` 继承；复杂树和多范围选区应实测 |
| `mapSelectionFromSource(const QItemSelection &) const` | 源选区转代理选区 | 从 `QAbstractProxyModel` 继承；不要只交换整数坐标 |

---

### 一句话总结

`QTransposeProxyModel` 是模型坐标的转置层：代理行对应源列，代理列对应源行，父索引、表头、编辑和结构操作都必须沿着这条规则转换，而 `sort()` 则明确保持无动作。
