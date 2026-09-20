# Qt QStandardItem：标准项模型中的数据、角色和树形节点

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStandardItemModel>`  
> 所属模块：`Qt6::Gui`  
> 继承：无  
> 类型定位：由 `QStandardItemModel` 管理的表格/树节点对象

## 1. 它解决什么问题

`QStandardItem` 是 Qt 标准项模型中的一个节点。它把以下内容放在同一个可插入模型的对象里：

- `Qt::ItemDataRole` 对应的数据，如显示文本、图标、提示和自定义角色；
- 可编辑、可选中、可拖放、可勾选等 `Qt::ItemFlags`；
- 行列位置和父子关系；
- 子项表格，既可以表示二维表格，也可以表示树；
- 可供视图排序和委托读取的标准角色。

它适合快速搭建中小型树、表格和列表模型。对于数据量很大、数据来自数据库或需要严格控制内存的场景，通常应直接派生 `QAbstractItemModel`，避免把所有业务对象都复制成 item 节点。

## 2. 所有权是核心契约

`QStandardItem` 不是 `QObject`，没有 QObject parent。它的所有权由 item/model 树管理：

```text
QStandardItemModel
  -> invisibleRootItem()
     -> top-level QStandardItem
        -> child QStandardItem
```

当 item 通过 `setItem()`、`setChild()`、`appendRow()` 等函数插入模型或父 item 后，容器接管它。相反：

- `removeRow()`、`removeChild` 类操作会移除并通常销毁项；
- `takeRow()`、`takeColumn()`、`takeChild()` 会移除并把指针交还调用方；
- 一个 item 指针不应同时插入两个父项或两个位置；
- 要移动 item，先使用 `take*()` 取出，再插入目标位置。

```cpp
auto *model = new QStandardItemModel(parent);
auto *root = model->invisibleRootItem();

auto *folder = new QStandardItem(QStringLiteral("文档"));
root->appendRow(folder); // root/model 接管 folder

auto *file = new QStandardItem(QStringLiteral("说明.txt"));
folder->appendRow(file); // folder 接管 file
```

## 3. 构建与最小用法

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

```cpp
#include <QStandardItemModel>

QStandardItemModel *createModel(QObject *parent)
{
    auto *model = new QStandardItemModel(parent);
    model->setHorizontalHeaderLabels({QStringLiteral("名称"),
                                      QStringLiteral("状态")});

    auto *name = new QStandardItem(QStringLiteral("任务 A"));
    auto *state = new QStandardItem(QStringLiteral("进行中"));
    model->appendRow({name, state});

    return model;
}
```

视图使用：

```cpp
QTreeView *view = new QTreeView;
view->setModel(createModel(view));
```

## 4. 角色数据：`data()` 是统一存储通道

### 4.1 `data(int role) const`

默认参数是 `Qt::UserRole + 1`，不是 `Qt::DisplayRole`。但标准便捷函数有自己的角色：

| 便捷 API | 使用的 role |
| --- | --- |
| `text()` / `setText()` | `Qt::DisplayRole` |
| `icon()` / `setIcon()` | `Qt::DecorationRole` |
| `toolTip()` / `setToolTip()` | `Qt::ToolTipRole` |
| `statusTip()` / `setStatusTip()` | `Qt::StatusTipRole` |
| `whatsThis()` / `setWhatsThis()` | `Qt::WhatsThisRole` |
| `sizeHint()` / `setSizeHint()` | `Qt::SizeHintRole` |
| `font()` / `setFont()` | `Qt::FontRole` |
| `textAlignment()` / `setTextAlignment()` | `Qt::TextAlignmentRole` |
| `background()` / `setBackground()` | `Qt::BackgroundRole` |
| `foreground()` / `setForeground()` | `Qt::ForegroundRole` |
| `checkState()` / `setCheckState()` | `Qt::CheckStateRole` |
| `accessibleText()` / `setAccessibleText()` | `Qt::AccessibleTextRole` |
| `accessibleDescription()` / `setAccessibleDescription()` | `Qt::AccessibleDescriptionRole` |

`setText()` 本质上是 `setData(text, Qt::DisplayRole)`。业务自定义字段应使用大于 `Qt::UserRole` 的稳定角色编号，并在模型的 `roleNames()` 中提供名称（尤其是 QML 场景）。

### 4.2 `DisplayRole` 和 `EditRole`

标准 item 对显示和编辑数据通常把 `Qt::DisplayRole` 与 `Qt::EditRole` 视为同一文本/值通道。自定义 `QStandardItem` 时，如果重写 `data()` 或 `setData()`，应明确决定这两个 role 是否共享，避免视图显示值和编辑器初始值不一致。

### 4.3 `multiData()`

Qt 6.0 起，`multiData(QModelRoleDataSpan)` 可批量填充多个 role，减少视图或代理逐个调用 `data()` 的开销。自定义 item 重写它时，应为 span 中请求的每个 role 写入对应值，并保留未处理 role 的基类行为。

## 5. 外观、可访问性和状态

`QStandardItem` 的外观 setter 大多只是向对应 role 写入数据：

```cpp
item->setFont(QFont(QStringLiteral("Segoe UI"), 10));
item->setForeground(QBrush(Qt::darkGreen));
item->setTextAlignment(Qt::AlignCenter);
item->setToolTip(QStringLiteral("双击编辑"));
```

视图是否使用这些 role 还取决于 delegate。设置背景或字体不会强制所有视图采用相同绘制方式。

可访问性字段 `accessibleText()` 和 `accessibleDescription()` 供辅助技术/可访问性接口读取，不是普通 tooltip 的替代品。

## 6. flags 和复选状态

### 6.1 `flags()`

`flags()` 返回 item 的 `Qt::ItemFlags`。常见能力包括：

- `Qt::ItemIsEnabled`；
- `Qt::ItemIsSelectable`；
- `Qt::ItemIsEditable`；
- `Qt::ItemIsUserCheckable`；
- `Qt::ItemIsDragEnabled`；
- `Qt::ItemIsDropEnabled`；
- `Qt::ItemIsAutoTristate`；
- `Qt::ItemIsUserTristate`。

便捷函数如 `setEditable(bool)`、`setCheckable(bool)` 都是在修改对应 flag。直接 `setFlags()` 会整体替换 flags，不是增量添加。

### 6.2 checkable、auto tristate、user tristate

一个可勾选项通常需要：

```cpp
item->setCheckable(true);
item->setCheckState(Qt::Unchecked);
```

`ItemIsAutoTristate` 与 `ItemIsUserTristate` 是不同能力：

- auto tristate 通常用于父项根据子项状态呈现部分选中；
- user tristate 允许用户循环或设置 `PartiallyChecked`；
- 是否如何传播还取决于模型、视图和使用的标准项行为。

不要只设置 `CheckStateRole` 而忘记 `ItemIsUserCheckable`，否则视图可能不提供复选交互。

## 7. 行列、树关系和索引

### 7.1 位置查询

- `parent()`：返回父 item；顶层 item 没有 item parent；
- `row()`、`column()`：返回在父 item 中的位置；
- `model()`：返回所属 `QStandardItemModel`；
- `index()`：返回对应 `QModelIndex`。

未插入模型的 item 通常没有有效 `model()` 和 `index()`，位置也可能是 `-1`。不要在 item 脱离模型后缓存其旧 `QModelIndex`。

### 7.2 `rowCount()` 和 `columnCount()`

子项是二维表格。树节点常用一列多行；表格 item 可以有多列。改变行列数会改变子项矩阵，缩小尺寸可能移除超出范围的 item。若要保留被移除对象，应先 `takeRow()` 或 `takeColumn()`。

### 7.3 `child()` 与 `setChild()`

`child(row, column)` 读取子项，越界或空单元通常返回 `nullptr`。`setChild()` 把 item 放入指定位置并接管其所有权，替换旧 item 时要考虑旧项的销毁。

## 8. 插入、追加、移除和取出

### 插入/追加

- `insertRow()`：在指定行插入一个 item 列表；
- `insertRows()`：插入 item 列表或若干空行；
- `insertColumn()`、`insertColumns()`：对应列操作；
- `appendRow()`、`appendRows()`、`appendColumn()`：在末尾追加。

列表长度和目标列数不一致时，空单元可能以 `nullptr` 表示。构造二维表格时应明确列数，避免视图看到不完整的行。

### 移除

`removeRow()`、`removeRows()`、`removeColumn()`、`removeColumns()` 从树中移除指定区域，并通常销毁其中的 item。它们适合“删除数据”的语义。

### 取出

`takeChild()`、`takeRow()`、`takeColumn()` 从树中移除对象但把所有权交还调用方：

```cpp
QStandardItem *item = parentItem->takeChild(row, column);
if (item) {
    // 现在由调用方负责重新插入或 delete
    targetItem->appendRow(item);
}
```

取出后若不再使用，必须 `delete`，否则会泄漏。

## 9. 自定义 item 类型

### 9.1 `ItemType` 和 `type()`

```cpp
enum ItemType {
    Type = 0,
    UserType = 1000
};
```

基类类型是 `Type`。自定义 item 应返回不小于 `UserType` 的值，以便在反序列化、工厂或调试中识别：

```cpp
class TaskItem : public QStandardItem
{
public:
    enum { Type = QStandardItem::UserType + 1 };
    int type() const override { return Type; }
    QStandardItem *clone() const override { return new TaskItem(*this); }
};
```

### 9.2 `clone()`

`clone()` 创建当前 item 的副本，适合 `QStandardItemModel::itemPrototype()` 机制。通常应复制 item 的角色数据和 flags；它不是把整个子树自动深拷贝到新对象的通用保证，业务需要复制子项时应显式遍历。

### 9.3 重写 `data()`、`setData()` 和 `multiData()`

自定义角色时：

```cpp
QVariant TaskItem::data(int role) const
{
    if (role == TaskRole)
        return taskId;
    return QStandardItem::data(role);
}

void TaskItem::setData(const QVariant &value, int role)
{
    if (role == TaskRole) {
        taskId = value.toInt();
        emitDataChanged();
        return;
    }
    QStandardItem::setData(value, role);
}
```

`emitDataChanged()` 是 protected 扩展点。自定义存储不经过基类 `setData()` 时，必须在数据变化后通知模型，否则视图不会刷新。

### 9.4 `operator<`

`sortChildren()` 会使用 item 的小于比较。默认比较适合普通数据；需要按自定义字段、数字而不是字符串或特殊 null 顺序排序时，应重写 `operator<`，并确保比较满足严格弱序。

## 10. 排序

```cpp
parentItem->sortChildren(0, Qt::AscendingOrder);
```

该调用排序的是当前 item 的子行，不是整个模型任意层级的全部节点。`QStandardItemModel::sort()` 则从模型层面排序指定列。排序会改变行顺序，依赖行号的临时索引需要重新获取。

## 11. 序列化

如果启用了 data stream，`read(QDataStream &)` 和 `write(QDataStream &) const` 可用于 item 数据序列化。它们主要处理 item 自身的数据和属性，不应假设会自动序列化整棵子树、所属模型或外部对象指针。

自定义 item 若重写序列化，应定义稳定版本号和类型处理，避免直接把 `QVariant` 中的未注册业务类型写入不可读格式。

## 12. 常见误区与排查顺序

### 12.1 item 被重复释放

插入模型后不要再手动 `delete`。需要转移时使用 `take*()`。

### 12.2 `data()` 默认 role 误解为显示文本

`data()` 的默认 role 是 `Qt::UserRole + 1`；显示文本使用 `text()` 或显式传 `Qt::DisplayRole`。

### 12.3 直接 setFlags 导致其他能力消失

`setFlags()` 是整体替换。只想增加能力时先读取并按位组合：

```cpp
item->setFlags(item->flags() | Qt::ItemIsEditable);
```

### 12.4 使用失效 QModelIndex

插入、删除、排序和移动后，旧索引的行列关系可能改变。优先使用 `QPersistentModelIndex` 或通过 item 重新调用 `index()`。

### 12.5 把 `QStandardItem` 当作 QObject

它没有 signal、slot、parent QObject 或线程亲和性。变化通知由所属 model 发出 `itemChanged` 等信号。

### 12.6 自定义数据改了但视图不刷新

重写 `setData()` 绕过基类存储时，需要调用 `emitDataChanged()`。

### 12.7 把 clone 当作深拷贝整棵树

`clone()` 的用途是创建一个 item 副本；子项树是否复制应由自定义代码明确处理。

## 13. 逐项 API 说明

### 构造和生命周期

- `QStandardItem()`：创建空 item。
- `QStandardItem(const QString &text)`：用显示文本创建 item。
- `QStandardItem(const QIcon &icon, const QString &text)`：同时设置 decoration 和 display 数据。
- `QStandardItem(int rows, int columns = 1)`：创建具有指定子表格尺寸的 item。
- `QStandardItem(const QStandardItem &other)`：protected 复制构造，供派生类或内部实现使用。
- `~QStandardItem()`：销毁 item 及其拥有的子项。

构造函数不会把 item 自动加入模型；必须通过 model/item 的插入 API 建立所有权关系。

### 数据和便捷 role API

- `data(int role = Qt::UserRole + 1) const`：读取指定 role。
- `multiData(QModelRoleDataSpan)`：批量读取 role，Qt 6.0 起。
- `setData(const QVariant &, int role = Qt::UserRole + 1)`：设置指定 role。
- `clearData()`：清除 item 保存的角色数据。
- `text()` / `setText()`：读取/设置 `DisplayRole`。
- `icon()` / `setIcon()`：读取/设置 `DecorationRole`。
- `toolTip()` / `setToolTip()`：读取/设置 `ToolTipRole`。
- `statusTip()` / `setStatusTip()`：读取/设置 `StatusTipRole`。
- `whatsThis()` / `setWhatsThis()`：读取/设置 `WhatsThisRole`。
- `sizeHint()` / `setSizeHint()`：读取/设置 `SizeHintRole`。
- `font()` / `setFont()`：读取/设置 `FontRole`。
- `textAlignment()` / `setTextAlignment()`：读取/设置 `TextAlignmentRole`。
- `background()` / `setBackground()`：读取/设置 `BackgroundRole`。
- `foreground()` / `setForeground()`：读取/设置 `ForegroundRole`。
- `checkState()` / `setCheckState()`：读取/设置 `CheckStateRole`。
- `accessibleText()` / `setAccessibleText()`：读取/设置可访问文本。
- `accessibleDescription()` / `setAccessibleDescription()`：读取/设置可访问描述。

### flags 和状态

- `flags() const`：读取全部 `Qt::ItemFlags`。
- `setFlags(Qt::ItemFlags)`：整体替换 flags。
- `isEnabled()` / `setEnabled(bool)`：读写 enabled flag。
- `isEditable()` / `setEditable(bool)`：读写 editable flag。
- `isSelectable()` / `setSelectable(bool)`：读写 selectable flag。
- `isCheckable()` / `setCheckable(bool)`：读写 user-checkable flag。
- `isAutoTristate()` / `setAutoTristate(bool)`：读写 auto-tristate flag。
- `isUserTristate()` / `setUserTristate(bool)`：读写 user-tristate flag。
- `isDragEnabled()` / `setDragEnabled(bool)`：读写 drag flag，受 drag-and-drop 配置影响。
- `isDropEnabled()` / `setDropEnabled(bool)`：读写 drop flag，受 drag-and-drop 配置影响。

### 树和表格结构

- `parent() const`：返回 item parent。
- `row() const`、`column() const`：返回 item 在父表格中的位置。
- `index() const`：返回所属 model 中的索引。
- `model() const`：返回所属 `QStandardItemModel`。
- `rowCount() const` / `setRowCount(int)`：读取/设置子表格行数。
- `columnCount() const` / `setColumnCount(int)`：读取/设置子表格列数。
- `hasChildren() const`：判断是否存在子项。
- `child(int row, int column = 0) const`：读取子项。
- `setChild(int row, int column, QStandardItem *)`：设置指定子项并接管所有权。
- `setChild(int row, QStandardItem *)`：设置第 0 列子项。

### 插入、移除和取出

- `insertRow(int, const QList<QStandardItem *> &)`：在指定行插入 item 列表。
- `insertColumn(int, const QList<QStandardItem *> &)`：在指定列插入 item 列表。
- `insertRows(int, const QList<QStandardItem *> &)`：插入一行 item 列表。
- `insertRows(int, int)`：插入指定数量的空行。
- `insertColumns(int, int)`：插入指定数量的空列。
- `removeRow(int)`：移除一行并处理其所有权。
- `removeColumn(int)`：移除一列并处理其所有权。
- `removeRows(int, int)`：移除多行。
- `removeColumns(int, int)`：移除多列。
- `appendRow(const QList<QStandardItem *> &)`：追加一行。
- `appendRows(const QList<QStandardItem *> &)`：追加多行。
- `appendColumn(const QList<QStandardItem *> &)`：追加一列。
- `insertRow(int, QStandardItem *)`：插入一个第 0 列 item。
- `appendRow(QStandardItem *)`：追加一个第 0 列 item。
- `takeChild(int, int = 0)`：移除并返回一个子项，所有权交给调用方。
- `takeRow(int)`：移除并返回一行，所有权交给调用方。
- `takeColumn(int)`：移除并返回一列，所有权交给调用方。

### 排序、类型和序列化

- `sortChildren(int, Qt::SortOrder)`：按指定列对子项排序。
- `clone() const`：创建 item 副本。
- `type() const`：返回 item 类型，基类是 `Type`。
- `read(QDataStream &)`：从流读取 item 自身数据。
- `write(QDataStream &) const`：向流写入 item 自身数据。
- `operator<(const QStandardItem &)`：提供排序比较。

### 受保护扩展点

- `QStandardItem(const QStandardItem &)`：protected 复制构造。
- `QStandardItem(QStandardItemPrivate &)`：内部/private 构造，不用于普通应用。
- `operator=(const QStandardItem &)`：protected 赋值运算符。
- `emitDataChanged()`：通知所属模型该 item 的数据发生变化。

## API 速查表

| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 构造 | `QStandardItem()` | 创建空 item | 尚未属于任何模型 |
| 构造 | `QStandardItem(const QString &)` | 设置显示文本 | 使用 `DisplayRole` |
| 构造 | `QStandardItem(const QIcon &, const QString &)` | 设置图标和文本 | 图标使用 `DecorationRole` |
| 构造 | `QStandardItem(int, int)` | 创建子表格尺寸 | 不自动填充 item 对象 |
| 生命周期 | `~QStandardItem()` | 销毁 item 和子项 | 插入模型后由所有权树管理 |
| 数据 | `data(int role)` | 读取角色数据 | 默认 role 是 `UserRole + 1` |
| 数据 | `multiData(QModelRoleDataSpan)` | 批量读取角色 | Qt 6.0 起；需正确填充 span |
| 数据 | `setData(const QVariant &, int)` | 写入角色数据 | 变化需要模型通知 |
| 数据 | `clearData()` | 清除角色数据 | 不等于删除子项 |
| 便捷 | `text()` / `setText()` | 读写显示文本 | `DisplayRole` |
| 便捷 | `icon()` / `setIcon()` | 读写图标 | `DecorationRole` |
| 便捷 | `toolTip()` / `setToolTip()` | 读写工具提示 | `ToolTipRole` |
| 便捷 | `statusTip()` / `setStatusTip()` | 读写状态提示 | `StatusTipRole` |
| 便捷 | `whatsThis()` / `setWhatsThis()` | 读写 WhatsThis | 受 whatsthis 配置影响 |
| 便捷 | `sizeHint()` / `setSizeHint()` | 读写尺寸提示 | delegate 是否采用由视图决定 |
| 便捷 | `font()` / `setFont()` | 读写字体 | `FontRole` |
| 便捷 | `textAlignment()` / `setTextAlignment()` | 读写文本对齐 | `TextAlignmentRole` |
| 便捷 | `background()` / `setBackground()` | 读写背景 | delegate 负责绘制 |
| 便捷 | `foreground()` / `setForeground()` | 读写前景 | delegate 负责绘制 |
| 便捷 | `checkState()` / `setCheckState()` | 读写复选状态 | 通常还要设置 checkable |
| 便捷 | `accessibleText()` / `setAccessibleText()` | 读写辅助文本 | 不是 tooltip |
| 便捷 | `accessibleDescription()` / `setAccessibleDescription()` | 读写辅助描述 | 供可访问性读取 |
| flags | `flags()` | 读取所有 item flags | 返回组合 flags |
| flags | `setFlags(Qt::ItemFlags)` | 整体替换 flags | 可能清除已有能力 |
| flags | `isEnabled()` / `setEnabled(bool)` | 读写 enabled | 影响交互 |
| flags | `isEditable()` / `setEditable(bool)` | 读写 editable | 影响编辑器 |
| flags | `isSelectable()` / `setSelectable(bool)` | 读写 selectable | 影响选择 |
| flags | `isCheckable()` / `setCheckable(bool)` | 读写可勾选 | 还需合理设置 CheckStateRole |
| flags | `isAutoTristate()` / `setAutoTristate(bool)` | 读写自动三态 | 父子状态传播需结合模型/视图 |
| flags | `isUserTristate()` / `setUserTristate(bool)` | 读写用户三态 | 支持 `PartiallyChecked` 交互 |
| flags | `isDragEnabled()` / `setDragEnabled(bool)` | 读写拖动能力 | 受 drag-and-drop 配置影响 |
| flags | `isDropEnabled()` / `setDropEnabled(bool)` | 读写放置能力 | 受 drag-and-drop 配置影响 |
| 关系 | `parent()` | 获取父 item | 顶层 item 可能为空 |
| 关系 | `row()` / `column()` | 获取位置 | 脱离模型后可能为 `-1` |
| 关系 | `index()` | 获取 QModelIndex | 无模型时通常无效 |
| 关系 | `model()` | 获取所属模型 | item 可独立存在，结果可能为空 |
| 结构 | `rowCount()` / `setRowCount(int)` | 读写子行数 | 缩小可能移除子项 |
| 结构 | `columnCount()` / `setColumnCount(int)` | 读写子列数 | 缩小可能移除子项 |
| 结构 | `hasChildren()` | 判断有无子项 | 不等于所有单元都非空 |
| 结构 | `child(int, int)` | 读取子项 | 越界/空单元返回空指针 |
| 结构 | `setChild(int, int, QStandardItem *)` | 设置子项 | 父项接管指针所有权 |
| 插入 | `insertRow(...)` | 插入行或单项 | 位置和所有权要明确 |
| 插入 | `insertColumn(...)` | 插入列 | 列表长度影响空单元 |
| 插入 | `insertRows(...)` | 插入多行或 item 行 | count 版本创建空结构 |
| 插入 | `insertColumns(...)` | 插入多列 | 缩放子表格 |
| 插入 | `appendRow(...)` | 末尾追加行 | 插入后不再手动释放 item |
| 插入 | `appendRows(...)` | 末尾追加多行 | 由父项接管 |
| 插入 | `appendColumn(...)` | 末尾追加列 | 可包含空指针单元 |
| 移除 | `removeRow()` / `removeRows()` | 删除行 | 通常销毁被移除 item |
| 移除 | `removeColumn()` / `removeColumns()` | 删除列 | 要保留对象请使用 take |
| 取出 | `takeChild()` | 移除并返回单项 | 调用方接管所有权 |
| 取出 | `takeRow()` | 移除并返回一行 | 不使用时要 delete |
| 取出 | `takeColumn()` | 移除并返回一列 | 不使用时要 delete |
| 排序 | `sortChildren(int, SortOrder)` | 排序当前子项 | 会改变行号和索引关系 |
| 类型 | `clone()` | 创建 item 副本 | 不要默认当作整棵树深拷贝 |
| 类型 | `type()` | 返回类型编号 | 自定义类型从 `UserType` 起 |
| 序列化 | `read(QDataStream &)` | 读取 item 数据 | 不等于自动读取整棵树 |
| 序列化 | `write(QDataStream &) const` | 写出 item 数据 | 需考虑版本和自定义 QVariant |
| 比较 | `operator<` | 提供排序比较 | 自定义时保持严格弱序 |
| 扩展 | `emitDataChanged()` | 通知模型 item 数据变化 | protected；自定义存储必须调用 |
| 比较 | `operator=(const QStandardItem &)` | protected 赋值 | 派生类复制时注意自有字段 |

---

### 一句话总结

`QStandardItem` 是标准项模型中的“数据 + 角色 + flags + 子表格节点”：插入后由模型/父项接管所有权，`take*` 才把指针交还调用方；使用时围绕 role 数据、索引失效、结构变更通知和自定义 item 扩展来理解，而不要把它当成 QObject 或普通可复制树节点。
