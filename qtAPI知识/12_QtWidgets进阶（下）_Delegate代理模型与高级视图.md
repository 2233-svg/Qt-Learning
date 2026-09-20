# Qt Widgets 进阶（下）：Delegate、代理模型与高级视图

> 适用版本：Qt 6.11.1  
> 核心类型：`QStyledItemDelegate`、`QSortFilterProxyModel`、`QItemSelectionModel`、`QMimeData`、`QAbstractItemView`

中篇完成了“模型如何遵守协议”。本篇把这些模型接入真实界面：

```text
Source Model
    ↓
Proxy Model（排序、过滤、映射）
    ↓
View ── SelectionModel（选择和当前项）
    ↓
Delegate（绘制和编辑）
```

最重要的边界是：

- Model 决定数据和能力；
- Proxy 改变观察到的顺序或可见集合；
- View 决定滚动、导航和交互；
- Delegate 决定单元格如何绘制、如何编辑；
- SelectionModel 独立保存选择状态。

## 1. 构建配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

`QStyledItemDelegate` 和 `QAbstractItemView` 属于 Widgets；`QSortFilterProxyModel`、`QItemSelectionModel` 属于 Core。

## 2. Delegate 到底负责什么

标准 View 不会为每个单元格永久创建一个 Widget。它只为正在编辑的项临时创建编辑器，普通显示则通过 Delegate 绘制。

### 2.1 绘制和编辑的生命周期

```text
View 需要显示 Item
    → delegate::paint()

用户触发编辑
    → createEditor()
    → setEditorData()
    → updateEditorGeometry()

用户提交
    → setModelData()
    → Model::setData(EditRole)
    → Model::dataChanged()
    → destroyEditor()
```

标准 `QStyledItemDelegate` 会按当前 `QStyle` 绘制，并根据数据类型选择编辑器。只有默认行为不满足需求时，才覆写 Delegate。

### 2.2 自定义编辑器：分数使用 QSpinBox

```cpp
#include <QSpinBox>
#include <QStyledItemDelegate>

class ScoreDelegate : public QStyledItemDelegate
{
public:
    using QStyledItemDelegate::QStyledItemDelegate;

    QWidget *createEditor(QWidget *parent,
                          const QStyleOptionViewItem &option,
                          const QModelIndex &index) const override
    {
        Q_UNUSED(option);
        if (index.column() != 1)
            return QStyledItemDelegate::createEditor(parent, option, index);

        auto *editor = new QSpinBox(parent);
        editor->setRange(0, 100);
        editor->setFrame(false);
        return editor;
    }

    void setEditorData(QWidget *editor,
                       const QModelIndex &index) const override
    {
        if (auto *spin = qobject_cast<QSpinBox *>(editor)) {
            spin->setValue(index.data(Qt::EditRole).toInt());
            return;
        }
        QStyledItemDelegate::setEditorData(editor, index);
    }

    void setModelData(QWidget *editor, QAbstractItemModel *model,
                      const QModelIndex &index) const override
    {
        if (auto *spin = qobject_cast<QSpinBox *>(editor)) {
            model->setData(index, spin->value(), Qt::EditRole);
            return;
        }
        QStyledItemDelegate::setModelData(editor, model, index);
    }

    void updateEditorGeometry(QWidget *editor,
                              const QStyleOptionViewItem &option,
                              const QModelIndex &index) const override
    {
        Q_UNUSED(index);
        editor->setGeometry(option.rect);
    }
};
```

安装到视图：

```cpp
auto *delegate = new ScoreDelegate(&view);
view.setItemDelegateForColumn(1, delegate);
```

View 不拥有通过 `setItemDelegate()` 设置的 Delegate。给 Delegate 设置合适的 parent，或者由控制器明确管理其生命周期。不要在多个 View 间共享同一个 Delegate 实例，否则一个 View 可能响应另一个 View 的 `closeEditor()` 信号。

### 2.3 Delegate 只负责编辑器，不负责业务校验

Delegate 可以用 `QIntValidator`、`QSpinBox` 提供即时输入约束，但最终合法性仍由 Model 的 `setData()` 决定。因为数据也可能由工具栏命令、批量导入或其他 View 写入。

### 2.4 自定义绘制：优先调用父类

```cpp
void StatusDelegate::paint(QPainter *painter,
                           const QStyleOptionViewItem &option,
                           const QModelIndex &index) const
{
    QStyleOptionViewItem opt(option);
    initStyleOption(&opt, index);

    if (index.data(PassedRole).toBool())
        opt.palette.setColor(QPalette::Text, QColor("#16794a"));

    QStyledItemDelegate::paint(painter, opt, index);
}
```

这样保留了选中、禁用、焦点、图标和平台样式，只改变文字颜色。完全自己画时必须处理高 DPI、RTL、选中状态、焦点框和可访问性，维护成本更高。

### 2.5 `sizeHint()` 与换行

```cpp
QSize sizeHint(const QStyleOptionViewItem &option,
               const QModelIndex &index) const override
{
    QSize size = QStyledItemDelegate::sizeHint(option, index);
    size.setHeight(qMax(size.height(), 28));
    return size;
}
```

如果 Delegate 的高度取决于宽度，启用 `wordWrap` 后要注意 View 的行高计算成本。大数据列表尽量保持统一行高。

### 2.6 为什么不在每个索引上放 Widget

```cpp
view.setIndexWidget(index, new QPushButton(QStringLiteral("操作")));
```

`setIndexWidget()` 适合可见区域内的静态内容，不适合动态、大量或可滚动数据。它会为每个索引创建真实 Widget，带来对象、布局、事件和内存开销。动态单元格内容应该使用 Delegate。

## 3. QSortFilterProxyModel：不复制源数据的排序过滤

Proxy Model 通过索引映射观察 Source Model：

```cpp
auto *proxy = new QSortFilterProxyModel(&view);
proxy->setSourceModel(&sourceModel);
proxy->setFilterCaseSensitivity(Qt::CaseInsensitive);
proxy->setFilterKeyColumn(0);
proxy->setFilterRegularExpression(QStringLiteral("张"));
view.setModel(proxy);
```

View 看到的是 proxy 索引，不是 source 索引。需要访问源模型时显式映射：

```cpp
const QModelIndex proxyIndex = view.currentIndex();
const QModelIndex sourceIndex = proxy->mapToSource(proxyIndex);

const QModelIndex anotherProxyIndex = proxy->mapFromSource(sourceIndex);
```

不要把 `proxyIndex.row()` 直接当作源容器的行号。过滤或排序后它几乎肯定不同。

### 3.1 自定义过滤

```cpp
class StudentProxy : public QSortFilterProxyModel
{
public:
    using QSortFilterProxyModel::QSortFilterProxyModel;

    void setMinimumScore(int score)
    {
        beginFilterChange();
        m_minimumScore = score;
        endFilterChange(QSortFilterProxyModel::Direction::Rows);
    }

protected:
    bool filterAcceptsRow(int sourceRow,
                          const QModelIndex &sourceParent) const override
    {
        const QModelIndex scoreIndex = sourceModel()->index(
            sourceRow, 1, sourceParent);
        return scoreIndex.data(Qt::DisplayRole).toInt() >= m_minimumScore;
    }

private:
    int m_minimumScore = 0;
};
```

Qt 6.9 引入 `beginFilterChange()`，Qt 6.10 的 `endFilterChange(Direction)` 能准确说明行过滤、列过滤或两者都过滤。参数改变前调用 begin，改变后立即调用 end。

旧代码中常见的 `invalidateFilter()` 在 Qt 6.13 计划弃用，面向 Qt 6.11 的新代码优先使用 begin/end 过滤变更协议。

### 3.2 自定义排序

```cpp
class ScoreSortProxy : public QSortFilterProxyModel
{
protected:
    bool lessThan(const QModelIndex &left,
                  const QModelIndex &right) const override
    {
        if (left.column() == 1)
            return left.data(Qt::EditRole).toInt()
                 < right.data(Qt::EditRole).toInt();
        return QSortFilterProxyModel::lessThan(left, right);
    }
};
```

打开排序：

```cpp
proxy->setSortRole(Qt::EditRole);
proxy->setDynamicSortFilter(true);
view.setSortingEnabled(true);
```

`lessThan()` 应是纯函数，不能在比较时修改 Model。若排序依据是数字、日期等，优先让源 Model 在 `EditRole` 或自定义 Role 返回原始类型。

### 3.3 过滤树模型

树过滤涉及父子关系：一个孩子匹配时，是否保留其祖先？相关属性包括：

```cpp
proxy->setRecursiveFilteringEnabled(true);
proxy->setAutoAcceptChildRows(true);
```

两者语义不同：递归过滤会沿层级查找后代匹配，自动接受子行则可能因父项被接受而显示其子项。树过滤前先写清楚“匹配父节点是否显示全部子节点”的产品规则。

## 4. 代理索引、选择与编辑的完整链路

```text
用户点击 View 中的 proxy index
    ↓
QItemSelectionModel 保存 proxy index
    ↓
Delegate 调用 proxy->setData(proxyIndex, value)
    ↓
Proxy 映射到 source index
    ↓
Source Model::setData()
```

因此通常应把 SelectionModel 连接在 View 当前使用的 Proxy 上，而不是源模型上：

```cpp
auto *selection = new QItemSelectionModel(proxy, &view);
view.setSelectionModel(selection);
```

若业务层需要源索引，则在槽中映射：

```cpp
connect(selection, &QItemSelectionModel::currentChanged,
        &window, [&proxy](const QModelIndex &current,
                          const QModelIndex &) {
    const QModelIndex source = proxy->mapToSource(current);
    qDebug() << source.data(Qt::DisplayRole);
});
```

## 5. QItemSelectionModel：当前项和选中项是两件事

`QItemSelectionModel` 可被多个 View 共享，用于统一选择状态。它同时跟踪：

- **current index**：键盘焦点和当前操作位置；
- **selected indexes**：明确选中的一个或多个范围。

当前项可以不在选区中，选区也可以包含多个项。

### 5.1 常用选择命令

```cpp
selection->select(index,
    QItemSelectionModel::ClearAndSelect
    | QItemSelectionModel::Rows);

selection->setCurrentIndex(index,
    QItemSelectionModel::NoUpdate);
```

| Flag | 作用 |
|---|---|
| `Clear` | 清除旧选区 |
| `Select` | 加入选区 |
| `Deselect` | 移出选区 |
| `Toggle` | 已选则取消，未选则加入 |
| `Current` | 同时更新 current 层 |
| `Rows` | 将整行纳入操作 |
| `Columns` | 将整列纳入操作 |
| `ClearAndSelect` | `Clear | Select` 的组合 |

### 5.2 监听选择变化

```cpp
connect(selection, &QItemSelectionModel::selectionChanged,
        &window, [](const QItemSelection &selected,
                    const QItemSelection &deselected) {
    qDebug() << "新增范围" << selected.indexes().size()
             << "移除范围" << deselected.indexes().size();
});

connect(selection, &QItemSelectionModel::currentChanged,
        &window, [](const QModelIndex &current,
                    const QModelIndex &previous) {
    qDebug() << "当前行" << current.row()
             << "之前行" << previous.row();
});
```

大块选区以范围存储，不要在每个鼠标移动事件中把所有 `selectedIndexes()` 转成复杂业务对象。需要批量操作时，在用户提交动作时一次性读取。

### 5.3 多个 View 共享选择模型

```cpp
auto *selection = new QItemSelectionModel(proxy, &window);
tableView.setSelectionModel(selection);
listView.setSelectionModel(selection);
```

两个 View 必须使用同一个 Model，且通常也要使用同一个 Proxy 实例。若每个 View 有不同代理，选择映射需要额外同步，不能直接共享同一 SelectionModel。

## 6. 拖放：MIME 是模型与外界的协议

拖放支持分三层：

1. View 开启拖放交互；
2. Model 声明动作和 MIME 类型；
3. Model 编码、解析并应用数据。

### 6.1 View 端设置

```cpp
view.setDragEnabled(true);
view.setAcceptDrops(true);
view.setDropIndicatorShown(true);
view.setDragDropMode(QAbstractItemView::InternalMove);
view.setDefaultDropAction(Qt::MoveAction);
```

`InternalMove` 只接受来自自身的移动操作，不等于 Model 自动支持移动。Model 仍需要实现对应的 flags、动作或 `dropMimeData()`。

### 6.2 Model 声明可拖放能力

```cpp
Qt::ItemFlags flags(const QModelIndex &index) const override
{
    if (!index.isValid())
        return Qt::NoItemFlags;
    return QAbstractListModel::flags(index)
         | Qt::ItemIsDragEnabled
         | Qt::ItemIsDropEnabled;
}

Qt::DropActions supportedDropActions() const override
{
    return Qt::CopyAction | Qt::MoveAction;
}

QStringList mimeTypes() const override
{
    return {QStringLiteral("application/vnd.myapp.student")};
}
```

### 6.3 编码和解析的最小轮廓

```cpp
QMimeData *mimeData(const QModelIndexList &indexes) const override
{
    auto *mime = new QMimeData;
    QByteArray bytes;
    QDataStream stream(&bytes, QIODevice::WriteOnly);

    for (const QModelIndex &index : indexes) {
        if (index.column() == 0)
            stream << index.data(Qt::EditRole).toString();
    }
    mime->setData(QStringLiteral("application/vnd.myapp.student"), bytes);
    return mime;
}

bool dropMimeData(const QMimeData *data, Qt::DropAction action,
                  int row, int column,
                  const QModelIndex &parent) override
{
    Q_UNUSED(column);
    if (action == Qt::IgnoreAction
        || !data->hasFormat(QStringLiteral("application/vnd.myapp.student")))
        return false;

    const QByteArray bytes = data->data(
        QStringLiteral("application/vnd.myapp.student"));
    QDataStream stream(bytes);
    QString name;
    QVector<QString> names;
    while (!stream.atEnd()) {
        stream >> name;
        names.push_back(name);
    }

    const int insertRow = row >= 0 ? row : rowCount(parent);
    beginInsertRows(parent, insertRow,
                    insertRow + names.size() - 1);
    // 将 names 写入自己的底层容器
    endInsertRows();
    return !names.isEmpty();
}
```

实际项目还要校验版本、来源、数据数量和权限，避免把任意 MIME 内容直接反序列化到业务对象。

## 7. 代理模型中的增删改

通过 Proxy 调用 `insertRows()`、`removeRows()`、`setData()` 通常会转发到 Source Model，但行号是 Proxy 坐标。自定义批量操作时：

```cpp
QModelIndexList proxyIndexes = selection->selectedRows();
for (const QModelIndex &proxyIndex : proxyIndexes) {
    const QModelIndex sourceIndex = proxy->mapToSource(proxyIndex);
    // 使用 sourceIndex 的稳定 ID 执行业务删除
}
```

从多个选中行删除时，若按源行号直接从小到大删除，会导致后续行号左移。可按源行号降序处理，或提供一个由 Model/Repository 批量删除的业务 API，并让模型发出一段连续的 remove 协议。

## 8. 大数据视图性能

### 8.1 保持 `data()` 轻量

Delegate 绘制多少个可见项，Model 就可能被查询多少次。不要在 `data()` 中做网络、磁盘或阻塞 SQL。

### 8.2 统一行高

树中所有行高度确定相同才设置：

```cpp
treeView.setUniformRowHeights(true);
```

Qt 可以跳过昂贵的逐项高度计算。若某些项会换行或有不同字体，不要强行开启。

### 8.3 避免 `setIndexWidget()` 和过多持久索引

Delegate 绘制比真实 Widget 更节省资源。`QPersistentModelIndex` 有维护成本，只在确实需要跨结构变化跟踪 UI 项时使用。

### 8.4 精确刷新

优先：

```cpp
emit dataChanged(topLeft, bottomRight, {Qt::DisplayRole});
```

其次是局部结构信号；最后才是 reset。Proxy 也会因源模型信号重新映射，过宽的刷新会放大成本。

### 8.5 批量更新策略

大量连续插入时一次 `beginInsertRows()` 包住整批，比循环插入每行一次更高效。批量更新期间不要让用户同时触发依赖中间状态的命令；完成后再发送一次业务完成信号。

## 9. 高级 View 配置

```cpp
tableView.setSelectionBehavior(QAbstractItemView::SelectRows);
tableView.setSelectionMode(QAbstractItemView::ExtendedSelection);
tableView.setAlternatingRowColors(true);
tableView.setSortingEnabled(true);
tableView.setEditTriggers(QAbstractItemView::DoubleClicked
                          | QAbstractItemView::EditKeyPressed);
```

常见视图选择：

| View | 适合数据 |
|---|---|
| `QListView` | 单列列表、图标网格 |
| `QTableView` | 固定列的二维数据 |
| `QTreeView` | 层级目录、资源树、多级数据 |

不要因为数据来自数据库就选择 `QTableView`，也不要因为数据有多列就为每个单元格创建 Widget。View 只表达呈现方式，真正的结构由 Model 决定。

## 10. 可访问性与键盘交互

Delegate 至少要保证：

- 文本、图标和复选状态有对应的标准 Role；
- 编辑器具有合理的 Tab 顺序和键盘提交行为；
- 选中状态不只靠颜色表达；
- `ToolTipRole` 或辅助文本能补充截断信息；
- 自定义绘制不覆盖焦点框和禁用状态。

View 的 `EditKeyPressed`、`Tab` 导航和 `CurrentChanged` 编辑触发都依赖正确的 `flags()` 与 Delegate 生命周期。只在鼠标双击路径上测试，容易漏掉键盘用户的行为。

## 11. 常见错误排查顺序

### 11.1 代理后点击了错误记录

检查是否把 Proxy 行号当成 Source 行号；先 `mapToSource()`，再读取稳定业务 ID。

### 11.2 编辑器显示了旧值

检查 Model 是否在 `EditRole` 返回原始值，Delegate 是否调用 `setEditorData()`；不要只实现 `DisplayRole`。

### 11. 编辑成功但界面不刷新

检查 `setData()` 是否真的写入、是否返回 `true`、是否发送了准确的 `dataChanged()`。

### 11. 排序后选择跳到了别的行

检查源模型是否正确发送结构/数据信号，Proxy 是否保持动态排序设置；业务操作不要依赖旧的行号。

### 11. Delegate 偶发关闭错误编辑器

检查是否在多个 View 间共享 Delegate 实例。每个 View 建立自己的 Delegate。

### 11. 拖放有指示线但放不进去

逐项检查：View 的 accept drops、dragDropMode、Model 的 `ItemIsDropEnabled`、`supportedDropActions()`、MIME 类型和 `dropMimeData()`。

## 12. API 速查

| 类型/API | 关键职责 |
|---|---|
| `QStyledItemDelegate::paint()` | 按 Style 绘制一个 Item |
| `createEditor()` | 创建临时编辑器 |
| `setEditorData()` | 从 Model 填充编辑器 |
| `setModelData()` | 将编辑器值提交给 Model |
| `updateEditorGeometry()` | 放置编辑器 |
| `sizeHint()` | 提供 Item 尺寸建议 |
| `QSortFilterProxyModel::filterAcceptsRow()` | 自定义行过滤 |
| `lessThan()` | 自定义排序比较 |
| `beginFilterChange()` / `endFilterChange()` | Qt 6.9/6.10+ 精确刷新过滤 |
| `mapToSource()` / `mapFromSource()` | Proxy 与 Source 索引转换 |
| `QItemSelectionModel::select()` | 修改选区 |
| `setCurrentIndex()` | 修改当前项 |
| `selectedRows()` | 获取选中的行 |
| `mimeData()` / `dropMimeData()` | 拖放编码与应用 |
| `setIndexWidget()` | 少量静态可见内容，不适合大数据 |
| `setUniformRowHeights()` | 行高统一时的树视图优化 |

## 13. 自测题

1. 为什么 Delegate 通常只为正在编辑的项创建 Widget？
2. `setItemDelegate()` 后 View 是否拥有 Delegate？
3. Proxy View 的 `currentIndex().row()` 能否直接作为源容器行号？
4. 自定义过滤参数修改前后分别调用哪两个函数？
5. 为什么 `EditRole` 最好返回日期或数字的原始类型？
6. `currentIndex` 和 selected indexes 有什么区别？
7. `InternalMove` 是否自动实现了 Model 的移动逻辑？
8. 大量连续数据更新时，为什么不推荐每个索引调用 `setIndexWidget()`？
9. 如何把 Proxy 选中的行安全地交给业务层删除？
10. `setUniformRowHeights(true)` 在什么前提下才正确？

## 14. 参考答案

1. 可见 Item 数量可能很大，永久 Widget 会造成巨大的对象、布局和绘制开销；Delegate 绘制轻量，编辑时才临时创建编辑器。
2. 不拥有。需要给 Delegate 设置合适的 parent 或由外部负责销毁，且不要跨 View 共享同一实例。
3. 不能。排序过滤后坐标系不同，必须调用 `mapToSource()`。
4. `beginFilterChange()`、修改参数、`endFilterChange(Direction::Rows/Columns/Both)`。
5. Delegate、排序和过滤可以按真实数值或日期处理，避免对格式化字符串进行错误的字典序比较。
6. current 是键盘焦点和当前操作位置；selected 是选中的范围，两者可以不同。
7. 不能。View 只发起拖放，Model 仍需声明 flags、动作并实现实际插入或移动。
8. 每个真实 Widget 都有 QObject、事件、布局和内存成本，滚动和批量刷新会迅速放大开销。
9. 对每个 Proxy 索引调用 `mapToSource()`，再使用源模型的稳定业务 ID 或批量删除 API，不要依赖会移动的行号。
10. 只有当所有 Item 的高度确实相同，并且 Delegate/换行不会产生不同高度时才可开启。

## 15. 本篇结论

Model/View 的高级能力仍然遵循同一条边界：

```text
模型提供稳定数据和精确变化通知
Proxy 改变观察坐标，不拥有另一份业务数据
SelectionModel 保存交互状态
Delegate 负责绘制和临时编辑
View 负责展示、滚动和输入导航
```

当排序、过滤、编辑、选择和拖放同时出现时，先明确当前索引属于哪一个模型，再在边界处显式映射。大数据场景优先使用轻量 `data()`、Delegate、批量结构信号和懒加载；把真实业务身份放在稳定 ID，而不是行号或未经维护的普通 `QModelIndex` 中。
