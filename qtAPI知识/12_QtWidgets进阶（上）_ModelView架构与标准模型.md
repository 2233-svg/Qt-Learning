# Qt Widgets 进阶（上）：Model/View 架构与标准模型

> 适用版本：Qt 6.11.1  
> 所属模块：Qt Core、Qt GUI、Qt Widgets  
> 核心类型：`QAbstractItemModel`、`QModelIndex`、`QPersistentModelIndex`、`QStandardItemModel`、`QStringListModel`、`QAbstractItemView`、`QListView`、`QTableView`、`QTreeView`、`QItemSelectionModel`

## 1. 为什么需要 Model/View

如果每条业务数据都对应一个独立 Widget，会出现：

- 大量 QObject 和事件处理成本；
- 数据与显示逻辑互相缠绕；
- 同一数据难以同时显示为列表、表格和树；
- 排序筛选需要复制数据；
- 选中、编辑、拖放各写一套逻辑；
- 几万条数据几乎无法流畅布局。

Model/View 把数据访问、显示和编辑拆开：

```text
数据源（容器、数据库、文件、服务）
                ↕
             Model
       标准化索引、数据和变更信号
          ↙             ↘
       View            Delegate
 展示/滚动/选择       绘制单元格/创建编辑器
          ↘             ↙
        SelectionModel
        当前项和选中范围
```

Qt 把传统 MVC 的 View 和 Controller 合并在 Item View 中，因此称 Model/View。

## 2. 三个核心角色

### 2.1 Model

回答：

- 有多少行、多少列；
- 某个父节点下面有哪些子项；
- 某索引在某 Role 下是什么数据；
- 项是否可选、可编辑、可拖放；
- 如何修改、插入和删除数据；
- 数据变化时如何通知观察者。

模型不一定拥有数据。它可以只是现有业务仓库的适配器。

### 2.2 View

负责：

- 只绘制可见 Item；
- 滚动；
- 选择和当前项交互；
- 编辑触发；
- 展开/折叠树；
- 列宽和表头；
- 键盘鼠标导航。

### 2.3 Delegate

负责每个 Item 的绘制和编辑器。标准 View 默认使用 `QStyledItemDelegate`，它遵循当前 QStyle。自定义 Delegate 放在本章下篇讲解。

## 3. 构建配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

`QAbstractItemModel` 属于 Core，`QStandardItemModel` 属于 Gui，视图属于 Widgets；链接 Widgets 会带入所需基础模块。

## 4. 最小可用代码：标准模型与表格视图

```cpp
#include <QApplication>
#include <QHeaderView>
#include <QStandardItemModel>
#include <QTableView>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QStandardItemModel model(3, 2);
    model.setHorizontalHeaderLabels({"姓名", "分数"});

    model.setItem(0, 0, new QStandardItem("张三"));
    model.setItem(0, 1, new QStandardItem("92"));
    model.setItem(1, 0, new QStandardItem("李四"));
    model.setItem(1, 1, new QStandardItem("85"));
    model.setItem(2, 0, new QStandardItem("王五"));
    model.setItem(2, 1, new QStandardItem("96"));

    QTableView view;
    view.setModel(&model);
    view.setSelectionBehavior(QAbstractItemView::SelectRows);
    view.setSelectionMode(QAbstractItemView::SingleSelection);
    view.horizontalHeader()->setStretchLastSection(true);
    view.resize(480, 260);
    view.show();

    return app.exec();
}
```

这里 model 在 view 之后析构吗？局部对象按逆序析构：view 后创建，因此 view 先析构，model 后析构，顺序安全。`setModel()` 不会把外部 Model 所有权转移给 View，实际项目应给 Model 合适 parent 或由 Controller 持有。

## 5. 表格是统一的数据抽象

所有 Item Model 都以“父索引下的二维表”表达数据：

```text
root（无效 QModelIndex）
  ├─ row 0: [column 0] [column 1] ...
  ├─ row 1: [column 0] [column 1] ...
  └─ row 2: ...
```

树只是每个 Item 还可以成为另一个二维表的 parent：

```text
root
  ├─ 项目 A
  │    ├─ 文件 A1
  │    └─ 文件 A2
  └─ 项目 B
       └─ 文件 B1
```

List 是一列表格，Table 是根下二维表，Tree 是递归表。

## 6. QModelIndex：数据位置的临时句柄

```cpp
QModelIndex index = model->index(row, column, parent);
if (index.isValid()) {
    qDebug() << index.row()
             << index.column()
             << index.data(Qt::DisplayRole);
}
```

Index 通常包含：

- 所属 Model；
- row；
- column；
- Model 内部定位信息；
- 隐含的层级关系。

它不是数据对象，也不拥有数据。

### 6.1 无效 QModelIndex 表示根

```cpp
model->rowCount(QModelIndex());
model->index(0, 0, QModelIndex());
```

对平面模型，parent 参数通常必须无效；对树模型，它指定查询哪个节点的子表。

### 6.2 不要长期保存普通 Index

模型插入、删除、移动或重置后，普通 QModelIndex 可能失效：

```cpp
QModelIndex saved = view->currentIndex(); // 不适合作长期业务引用
```

短期函数调用中使用；长期 UI 引用使用 `QPersistentModelIndex`，业务身份最好使用稳定 ID。

```cpp
QPersistentModelIndex persistent(index);
```

Persistent Index 会由正确实现的模型在结构变化时维护，但模型 reset 后仍可能失效，也不替代业务 ID。

## 7. Role：一个 Item 的多种语义

同一个 Index 可按 Role 提供不同数据：

```cpp
QVariant display = model->data(index, Qt::DisplayRole);
QVariant edit = model->data(index, Qt::EditRole);
QVariant icon = model->data(index, Qt::DecorationRole);
```

常用 Role：

| Role | 用途 |
|---|---|
| `DisplayRole` | 显示文本 |
| `EditRole` | 编辑器中的原始值 |
| `DecorationRole` | 图标、颜色装饰 |
| `ToolTipRole` | 悬停提示 |
| `StatusTipRole` | 状态栏提示 |
| `FontRole` | 字体 |
| `TextAlignmentRole` | 对齐 |
| `BackgroundRole` | 背景 Brush |
| `ForegroundRole` | 前景 Brush |
| `CheckStateRole` | 复选状态 |
| `SizeHintRole` | Item 尺寸建议 |
| `UserRole` 起 | 应用自定义数据 |

### 7.1 显示值和原始值分开

日期显示为本地化字符串，但编辑和排序应使用 QDateTime：

```cpp
item->setData(dateTime.toString("yyyy-MM-dd"), Qt::DisplayRole);
item->setData(dateTime, Qt::UserRole);
```

更理想的自定义模型可在 DisplayRole 返回字符串、EditRole 返回结构化值。不要把格式化文本当唯一数据。

### 7.2 自定义 Role

```cpp
enum Roles {
    IdRole = Qt::UserRole + 1,
    SortRole,
    ErrorRole
};
```

Role 值应稳定，特别是模型还暴露给 QML、插件或序列化逻辑时。

## 8. ItemFlags：一个 Item 能做什么

```cpp
Qt::ItemFlags flags = model->flags(index);
```

常见标志：

- `ItemIsEnabled`；
- `ItemIsSelectable`；
- `ItemIsEditable`；
- `ItemIsUserCheckable`；
- `ItemIsDragEnabled`；
- `ItemIsDropEnabled`。

只有 data 提供值但 flags 不含 Editable，View 不会启动标准编辑。CheckStateRole 通常还要配 `ItemIsUserCheckable`。

## 9. 标准 Model 怎么选

| Model | 用途 |
|---|---|
| `QStringListModel` | 一列字符串 |
| `QStandardItemModel` | 通用 Item 树/表，快速搭建 |
| `QFileSystemModel` | 文件系统异步模型 |
| `QSortFilterProxyModel` | 排序筛选代理 |
| `QSqlQueryModel` | SQL 查询只读结果 |
| `QSqlTableModel` | 单表可编辑模型 |
| 自定义 `QAbstractListModel` | 领域列表、高效且强语义 |
| 自定义 `QAbstractTableModel` | 领域表格 |
| 自定义 `QAbstractItemModel` | 任意树结构 |

先用最窄的基类。平面列表不要直接继承最复杂的 QAbstractItemModel。

## 10. QStringListModel

```cpp
auto *model = new QStringListModel(this);
model->setStringList({"北京", "上海", "深圳"});

auto *view = new QListView;
view->setModel(model);
```

适合简单字符串；需要多个 Role、图标、复杂业务对象时会很快到达边界。

修改应通过 Model API：

```cpp
QModelIndex index = model->index(1, 0);
model->setData(index, "广州", Qt::EditRole);
```

取出 stringList 修改副本后忘记 set 回去，不会改变模型。

## 11. QStandardItemModel

```cpp
auto *model = new QStandardItemModel(this);
auto *item = new QStandardItem("服务器 A");
item->setIcon(QIcon::fromTheme("network-server"));
item->setData("server-a", IdRole);
item->setCheckable(true);
model->appendRow(item);
```

树结构：

```cpp
auto *group = new QStandardItem("生产环境");
group->appendRow(new QStandardItem("服务器 A"));
group->appendRow(new QStandardItem("服务器 B"));
model->appendRow(group);
```

Model 接管插入的 QStandardItem。`takeItem()` / `takeRow()` 则把所有权交给调用者。

### 11.1 优点与边界

优点：灵活、无需写 Model 子类、支持树和多 Role。

边界：每个 Item 都是独立对象，大数据内存较高；业务数据容易被复制进 Item；同步外部仓库较麻烦。稳定领域模型通常应直接适配业务数据。

## 12. Convenience Widget 何时使用

`QListWidget`、`QTableWidget`、`QTreeWidget` 把 Model 隐藏在 Item API 后面。

适合：

- 数据很少；
- 单一界面使用；
- 原型和简单工具；
- 不需要代理模型和多个共享 View。

不适合：

- 大数据；
- 多视图共享；
- 外部业务数据源；
- 复杂排序筛选；
- 希望单元测试数据逻辑；
- 后续要迁移到 QML。

Qt 文档总体推荐优先 Model/View。若还想使用 Item API，可先用 View + QStandardItemModel。

## 13. QListView、QTableView、QTreeView

### 13.1 QListView

展示一列 Model，也可用 IconMode：

```cpp
view->setViewMode(QListView::IconMode);
view->setFlow(QListView::LeftToRight);
view->setWrapping(true);
```

### 13.2 QTableView

展示二维表：

```cpp
table->horizontalHeader()->setSectionResizeMode(
    QHeaderView::Interactive);
table->verticalHeader()->setVisible(false);
table->setAlternatingRowColors(true);
table->setSortingEnabled(true);
```

启用 sorting 前确认 Model 或 Proxy 正确支持排序。对 QStandardItemModel，排序数据 Role 和类型会影响顺序。

### 13.3 QTreeView

展示层级：

```cpp
tree->setRootIsDecorated(true);
tree->setUniformRowHeights(true);
tree->expandToDepth(1);
```

只有所有行高度确实相同时才启用 uniformRowHeights，它能减少重复 size hint 查询。

## 14. View 不拥有外部 Model

```cpp
auto *model = new MyModel(view); // 可把 parent 设为 view
view->setModel(model);
```

`setModel()` 本身不转移外部 Model 所有权。一个 Model 可被多个 View 共享，所以所有者应是 Controller、窗口或一个明确的 QObject。

View 会创建/管理自己的 SelectionModel。更换 Model 后，旧 SelectionModel 的处理也要注意，尤其是手动共享 SelectionModel 时。

## 15. Root Index

Tree View 可只展示某个子树：

```cpp
QModelIndex projectIndex = model->index(projectRow, 0);
tree->setRootIndex(projectIndex);
```

Root Index 本身不显示，只显示它的孩子。Model 没变，只是 View 的观察入口改变。

## 16. SelectionBehavior 与 SelectionMode

```cpp
view->setSelectionBehavior(QAbstractItemView::SelectRows);
view->setSelectionMode(QAbstractItemView::ExtendedSelection);
```

Behavior：

- `SelectItems`；
- `SelectRows`；
- `SelectColumns`。

Mode：

- `NoSelection`；
- `SingleSelection`；
- `MultiSelection`；
- `ExtendedSelection`；
- `ContiguousSelection`。

表格业务常按行操作，应显式设 SelectRows，避免只选中一个单元格却删除整行造成意外。

## 17. 当前项不等于选中项

SelectionModel 同时维护：

- current index：键盘导航和编辑焦点所在项；
- selected indexes/ranges：一个或多个选中区域。

Current 可以未被选中；选区也可以包含多个 Item。

```cpp
QModelIndex current = view->currentIndex();
QModelIndexList selected = view->selectionModel()->selectedRows();
```

执行批量操作用 selectedRows；显示详情通常跟随 currentChanged。不要混用。

## 18. QItemSelectionModel 信号

```cpp
connect(view->selectionModel(),
        &QItemSelectionModel::currentChanged,
        this, &Panel::showCurrentDetails);

connect(view->selectionModel(),
        &QItemSelectionModel::selectionChanged,
        this, &Panel::updateBatchActions);
```

`selectionChanged` 给出新增选区和取消选区，不是每次都给出完整当前选区。需要完整结果时再调用 selectedRows/selectedIndexes。

### 18.1 程序选择

```cpp
selectionModel->select(
    index,
    QItemSelectionModel::ClearAndSelect |
    QItemSelectionModel::Rows);
selectionModel->setCurrentIndex(
    index,
    QItemSelectionModel::NoUpdate);
```

SelectionFlag 可组合 Clear、Select、Deselect、Toggle、Current、Rows、Columns。`setCurrentIndex` 是否同时选择取决于传入命令，不要假定 current 自动加入 selection。

## 19. 多个 View 共享选择

同一个 Model 的多个 View 可共享 SelectionModel：

```cpp
auto *selection = new QItemSelectionModel(model, this);
listView->setSelectionModel(selection);
tableView->setSelectionModel(selection);
```

只有当两个 View 的索引语义完全相同才可直接共享。若其中一个使用 Proxy Model，索引所属 Model 不同，必须映射或使用独立选择同步逻辑。

## 20. 表头

模型提供表头数据：

```cpp
model->setHeaderData(0, Qt::Horizontal, "姓名");
```

View 控制呈现和尺寸：

```cpp
header->setSectionResizeMode(0, QHeaderView::ResizeToContents);
header->setSectionResizeMode(1, QHeaderView::Stretch);
header->setSectionsMovable(true);
```

`ResizeToContents` 在大量行上可能昂贵，因为需测量内容。可只用于少量列、设置 resizeContentsPrecision，或使用 Interactive + 合理初始宽度。

## 21. 编辑触发

```cpp
view->setEditTriggers(
    QAbstractItemView::DoubleClicked |
    QAbstractItemView::EditKeyPressed);
```

即使 View 允许触发，Model flags 还必须包含 ItemIsEditable，Model `setData()` 也必须接受 EditRole 并发出 dataChanged。

```text
用户触发编辑
  → View 检查 EditTriggers
  → Model flags 是否 Editable
  → Delegate 创建 Editor
  → Delegate 写回 Model::setData(EditRole)
  → Model 发 dataChanged
  → 所有 View 重绘
```

## 22. Index 和业务 ID

删除操作不要先收集 row 数字再从小到大删除：索引会移动。

策略：

- 使用稳定业务 ID 找数据；
- 平面模型按 row 从大到小删除；
- 使用 Persistent Index，并理解 reset 会失效；
- 通过 Model 的领域 API 批量删除；
- Proxy View 的 Index 先映射到 source。

## 23. Model 的通知契约

View 不会轮询数据变化。Model 必须发信号：

| 变化 | 通知 |
|---|---|
| 某些 Role 数据变化 | `dataChanged` |
| 表头变化 | `headerDataChanged` |
| 插入行列 | begin/endInsertRows/Columns |
| 删除行列 | begin/endRemoveRows/Columns |
| 移动行列 | begin/endMoveRows/Columns |
| 布局重排 | `layoutAboutToBeChanged` / `layoutChanged` |
| 整体重建 | begin/endResetModel |

缺少通知会导致 View 显示旧数据、选区错位或 Persistent Index 损坏。详细实现放在中篇。

## 24. 线程规则

`QAbstractItemModel` 不是线程安全对象。连接到 View 的 Model 应在 GUI 线程访问和修改。

后台线程流程：

```text
工作线程读取/计算普通数据
          ↓ 信号按值传回
GUI 线程调用 Model API 插入/更新
          ↓ 正确 begin/end 或 dataChanged
View 更新
```

不要从工作线程直接调用 `beginInsertRows()` 或修改 View 正在读取的底层容器。

## 25. 性能基础

- View 只绘制可见项，不要用 setIndexWidget 为每行塞复杂 Widget；
- 大模型按需 `canFetchMore/fetchMore`；
- Table 的 ResizeToContents 谨慎使用；
- Tree 行高一致时启用 uniformRowHeights；
- dataChanged 范围和 Role 尽量准确；
- 避免用 beginResetModel 代替局部通知；
- 不要在 `data()` 中访问网络或执行重计算；
- 昂贵显示值在 Model 或业务层缓存，并正确失效。

## 26. 常见错误

### 26.1 长期保存 QModelIndex

结构变化后可能失效。短期使用，长期用业务 ID 或 Persistent Index。

### 26.2 setModel 后忘记所有权

View 不接管外部 Model。给 Model parent 或由明确拥有者保存。

### 26.3 显示文本当业务数据

翻译、格式化和重命名会破坏逻辑。用 EditRole 或 UserRole 保存结构化值和 ID。

### 26.4 currentIndex 当完整选区

当前项和选中项是两套状态。批量命令使用 selectedRows。

### 26.5 直接改底层容器不通知

View 缓存无法更新。所有结构和数据变化遵守 Model 通知契约。

### 26.6 每个 Cell 放 QWidget

对象数和布局成本急剧上升。显示用 Delegate paint，编辑时才临时创建 Editor。

### 26.7 工作线程直接更新 Model

与 GUI View 并发访问导致竞态。传普通结果回 GUI 线程再修改。

## 27. API 速查表

| API | 用途 | 注意点 |
|---|---|---|
| `model->index()` | 创建位置句柄 | 检查 isValid |
| `index.data(role)` | 按 Role 读数据 | Index 不拥有数据 |
| `QPersistentModelIndex` | 跨结构变化跟踪 Item | Reset 后可失效 |
| `QStandardItem::setData()` | 设置 Role 数据 | Model 接管 Item |
| `view->setModel()` | 绑定 Model | 不转移外部 Model 所有权 |
| `view->setRootIndex()` | 显示子树 | Root 自身不显示 |
| `setSelectionBehavior()` | 按项/行/列选择 | 与业务命令一致 |
| `selectedRows()` | 取得选中行 | 默认 column 0 Index |
| `currentChanged` | 当前项变化 | 不等于 selectionChanged |
| `selectionChanged` | 选区增删 | 参数是增量范围 |
| `setEditTriggers()` | 控制开始编辑方式 | Model flags 也要 Editable |
| `headerData()` | 提供表头语义 | 表头变化发专用信号 |

## 28. 自测题

### 题 1：Model 是否必须存数据

<details><summary>答案</summary>

不必须。Model 是标准访问和通知接口，可以适配外部容器、数据库、文件或业务仓库。
</details>

### 题 2：普通 QModelIndex 能否长期保存

<details><summary>答案</summary>

不应。插入、删除、移动、重排和 reset 可能使它失效。长期身份优先用业务 ID，需要 UI 跟踪时用 Persistent Index。
</details>

### 题 3：DisplayRole 与 EditRole 为什么分开

<details><summary>答案</summary>

显示可能是本地化格式字符串，编辑和业务需要原始结构化值。分开可避免格式化文本污染排序、编辑和存储。
</details>

### 题 4：Current 与 Selection 有何区别

<details><summary>答案</summary>

Current 是导航/编辑焦点所在的单个索引；Selection 是零到多个选中范围。它们可独立变化。
</details>

### 题 5：为什么不能在线程中直接改 Model

<details><summary>答案</summary>

Model 与 GUI View 通常在主线程交互，类本身不保证线程安全。后台线程产出普通数据，再通过排队通信让 GUI 线程调用 Model API。
</details>

## 29. 本篇总结

1. Model 标准化数据访问和变化通知，View 负责可见交互，Delegate 负责 Item 绘制编辑。
2. 所有数据以“父索引下的二维表”统一表达，树是递归二维表。
3. QModelIndex 是临时位置句柄，不是业务对象；长期身份使用稳定 ID。
4. Role 让一个 Item 同时提供显示、编辑、图标、状态和业务数据。
5. current 与 selection 是不同状态，命令必须选择正确来源。
6. View 不接管外部 Model，多个 View 可以共享同一 Model。
7. Model 必须严格通知变化，并只在所属 GUI 线程更新。

中篇将实现自定义 List/Table/Tree Model，重点讲 data、flags、setData、begin/end 结构通知、reset、Persistent Index 和延迟加载。
