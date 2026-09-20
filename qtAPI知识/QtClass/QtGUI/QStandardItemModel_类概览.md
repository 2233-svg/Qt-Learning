# Qt QStandardItemModel：可直接连接视图的标准表格与树模型

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStandardItemModel>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QAbstractItemModel`  
> 类型定位：以 `QStandardItem` 为节点的通用 item model

## 1. 它解决什么问题

`QStandardItemModel` 为列表、表格和树提供一个开箱即用的 `QAbstractItemModel` 实现。它负责：

- 保存行列结构和父子层级；
- 管理 `QStandardItem` 的所有权；
- 通过 `QModelIndex` 向视图暴露数据；
- 转发 item 的 role 数据、flags 和检查状态；
- 生成插入、删除、数据变化等标准模型通知；
- 保存水平/垂直表头；
- 提供查找、排序、拖放 MIME 数据和自定义 role 名称。

它适合配置面板、文件树、设置列表、简单数据表和原型工具。数据量巨大、结构来自远程数据库、需要虚拟化或复杂分页时，直接实现 `QAbstractItemModel` 往往更合适。

## 2. 模型、item 和视图的关系

```text
QStandardItemModel
  -> invisibleRootItem()
     -> top-level QStandardItem
        -> child QStandardItem

QTreeView / QTableView / QListView
  -> QModelIndex
     -> model->data(index, role)
```

模型拥有 item。插入到模型的 item 不应再由调用方手动释放。需要转移所有权时使用 `takeItem()`、`takeRow()`、`takeColumn()` 或相应 header 的 `take*()`。

## 3. 构建与最小用法

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

```cpp
#include <QStandardItemModel>
#include <QTableView>

auto *model = new QStandardItemModel(0, 2, view);
model->setHorizontalHeaderLabels({
    QStringLiteral("名称"),
    QStringLiteral("状态")
});

model->appendRow({
    new QStandardItem(QStringLiteral("任务 A")),
    new QStandardItem(QStringLiteral("进行中"))
});

view->setModel(model);
```

插入 row 时，model 接管新 item 的所有权。若只想设置某个单元格，也可以：

```cpp
model->setItem(0, 0, new QStandardItem(QStringLiteral("任务 B")));
```

## 4. 顶层表格与嵌套树

### 4.1 顶层 API

`QStandardItemModel` 的 `appendRow()`、`insertRow()`、`setItem()`、`rowCount()` 等无 parent 重载操作模型的顶层区域。

### 4.2 嵌套 API

对树节点，应从 item 进入子树：

```cpp
auto *root = model->invisibleRootItem();
auto *group = new QStandardItem(QStringLiteral("分组"));
root->appendRow(group);
group->appendRow(new QStandardItem(QStringLiteral("子项")));
```

也可以使用带 parent `QModelIndex` 的模型接口，例如 `insertRows(row, count, parentIndex)`。两条路径最终都必须保持 model 的索引和 item 树一致。

### 4.3 `invisibleRootItem()`

返回模型内部的根 item。它本身不作为可见数据行展示，但可以像普通 item 一样管理顶层子项。它的 `index()` 通常是无效的根索引；不要把它当成视图中的实际行。

## 5. 索引、item 和生命周期

### 5.1 `index()` / `parent()`

模型用 `index(row, column, parent)` 创建索引，用 `parent(child)` 返回树层级的父索引。顶层索引的 parent 是无效 `QModelIndex()`。

越界 row/column 或不属于本模型的 parent 应返回无效索引或失败结果；调用方应使用 `QModelIndex::isValid()` 检查。

### 5.2 `item()` 与 `itemFromIndex()`

- `item(row, column)` 读取顶层对应 item；空单元通常返回 `nullptr`；
- `itemFromIndex(index)` 把模型索引转换为 item；
- 当索引对应位置尚未有 item 且模型设置了 item prototype 时，`itemFromIndex()` 可能通过 prototype 懒创建 item；
- `indexFromItem(item)` 把属于该模型的 item 转回索引。

不要在只想查询时无意间调用会触发懒创建的路径，也不要把其他模型的 item 传给 `indexFromItem()`。

## 6. 所有权和替换规则

### 6.1 设置/插入

`setItem()`、`setHorizontalHeaderItem()`、`setVerticalHeaderItem()` 和各种插入 API 会把新 item 纳入模型管理。若目标位置已有 item，旧 item 通常会被删除；需要保留旧 item 时先 `take*()`。

### 6.2 take 与 remove

| API 方向 | 结果 |
| --- | --- |
| `removeRows()` / `removeColumns()` | 从模型删除结构，通常销毁被删除 item |
| `clear()` | 清除整个 item 树和表头 |
| `takeItem()` / `takeRow()` / `takeColumn()` | 移除并把 item 指针交给调用方 |
| `takeHorizontalHeaderItem()` / `takeVerticalHeaderItem()` | 移除表头 item 并把指针交给调用方 |

```cpp
QStandardItem *taken = model->takeItem(0, 0);
if (taken) {
    // 重新插入其他位置，或在不需要时 delete taken
    delete taken;
}
```

## 7. 角色数据和通知

### 7.1 `data()` 与 `setData()`

模型层的 `data(index, role)` 通常转发到 index 对应 item 的 `data(role)`。默认读取 role 是 `Qt::DisplayRole`，默认写入 role 是 `Qt::EditRole`。

`setData()` 成功修改后会让 model 发出相应数据变化通知，视图据此刷新。直接修改 item 的 role 数据也应通过属于模型的 item API，让模型能够发出通知。

### 7.2 `itemData()` 与 `setItemData()`

这两个 API 以 `QMap<int, QVariant>` 批量读写一个 index 的角色集合。适合复制角色、实现自定义编辑器或一次性更新多个属性。

批量写入时应避免在循环中发出大量互相独立的更新；若业务需要事务式刷新，应考虑模型重置或合适的 layout/dataChanged 通知策略。

### 7.3 `clearItemData()`

清除指定 index 的角色数据，但不会删除 item、改变行列结构或自动清除表头。

### 7.4 `itemChanged(QStandardItem *)`

这是 `QStandardItemModel` 面向 item 的信号。它通常在 item 的数据或 flags 改变后发出。连接时应避免在槽中无条件再次修改同一 item，防止递归更新。

## 8. 自定义 role 名称和 QML

```cpp
constexpr int PriorityRole = Qt::UserRole + 1;

model->setItemRoleNames({
    {PriorityRole, "priority"}
});
```

`roleNames()` 返回 role 到名称的映射，便于 QML 或调试工具理解自定义字段。角色编号应在应用中稳定，不能因为插入新角色而随意重排已有编号。

`QStandardItem` 负责保存 role 数据；模型负责把 role 名称告诉视图/QQml 访问层。设置 role 名称不会自动给已有 item 填值。

## 9. 行列和结构 API

### `rowCount()` / `columnCount()`

带 parent 的重载查询指定层级；默认无效 parent 查询顶层。`rowCount(parent)` 和 `columnCount(parent)` 的返回值可能因树节点不同而不同。

### `setRowCount()` / `setColumnCount()`

调整模型顶层的行列数量。缩小尺寸会移除超出区域的 item，因此需要保留对象时先 `take*()`。嵌套节点可通过 item 的对应函数调整。

### insert/remove

模型重写的 `insertRows()`、`insertColumns()`、`removeRows()`、`removeColumns()` 带 parent index，适合让视图/代理使用标准模型操作。无 parent 的 item-list 重载适合直接插入 `QStandardItem`。

结构变化必须走模型 API，使 begin/end 通知和索引维护由模型完成。不要直接修改 private item 链接。

## 10. 表头

```cpp
model->setHorizontalHeaderLabels({
    QStringLiteral("名称"),
    QStringLiteral("大小")
});
model->setVerticalHeaderLabels({
    QStringLiteral("1"),
    QStringLiteral("2")
});
```

表头也是 `QStandardItem`，可以通过：

- `horizontalHeaderItem()` / `setHorizontalHeaderItem()` / `takeHorizontalHeaderItem()`；
- `verticalHeaderItem()` / `setVerticalHeaderItem()` / `takeVerticalHeaderItem()`。

替换表头 item 时同样要遵守所有权规则。设置 header label 是方便函数，不会把 header 变成独立的 QObject。

## 11. 排序

### `sortRole`

`sortRole` 属性决定 `sort()` 使用哪个 role，默认通常是 `Qt::DisplayRole`。设置它后再排序：

```cpp
model->setSortRole(Qt::UserRole + 1);
model->sort(0, Qt::AscendingOrder);
```

`sortRole` 支持 `QBindable<int>`，适合 Qt Property 绑定。绑定只管理 role 值，不替你执行排序事务。

### `sort(int column, Qt::SortOrder order)`

排序指定层级的 item 行。模型级排序会改变行顺序，依赖旧行号的临时索引需要重新获取。复杂排序可以在 `QStandardItem::operator<` 或自定义 item 中实现。

排序列必须存在；排序规则使用的 role、类型和空值策略应在业务中统一，否则字符串数字可能出现字典序而非数值序。

## 12. 查找、拖放和 MIME

### `findItems()`

```cpp
const auto matches = model->findItems(
    QStringLiteral("任务"),
    Qt::MatchContains | Qt::MatchRecursive,
    0);
```

它按文本和 `Qt::MatchFlags` 搜索指定列。是否递归搜索、是否区分大小写、是否完整匹配由 flags 决定。返回的是 item 指针列表，使用时仍要确认它们属于当前 model。

### `mimeTypes()` / `mimeData()`

这些函数为拖放或剪贴板提供 MIME 数据。默认实现面向标准 item model 的数据传输；自定义格式应覆盖对应函数，并确保 MIME payload 能安全表达选中索引。

### `dropMimeData()`

接收拖放数据并把它插入指定 parent、row 和 column。`row == -1` 或 `column == -1` 等位置语义由模型拖放协议决定，不能简单当作普通有效索引使用。自定义实现要检查 action、MIME 类型和 parent 有效性。

### `supportedDropActions()`

返回支持的拖放动作集合。它只声明能力，实际是否成功仍取决于 `dropMimeData()` 的实现和 item flags。

## 13. item prototype

```cpp
class CustomItem : public QStandardItem
{
public:
    QStandardItem *clone() const override
    {
        return new CustomItem(*this);
    }
};

model->setItemPrototype(new CustomItem);
```

prototype 由模型保存，模型销毁时负责清理。它用于在需要 item 的位置通过 `clone()` 创建自定义类型。自定义 item 必须正确实现 `clone()`，否则懒创建得到的类型或数据可能不符合预期。

## 14. 继承 API 的边界

`QStandardItemModel` 重写了 `QAbstractItemModel` 的核心虚函数：

- `index()`、`parent()`；
- `rowCount()`、`columnCount()`、`hasChildren()`；
- `data()`、`multiData()`、`setData()`、`clearItemData()`；
- `headerData()`、`setHeaderData()`；
- `flags()`；
- `insertRows()`、`insertColumns()`、`removeRows()`、`removeColumns()`；
- `itemData()`、`setItemData()`；
- `roleNames()`；
- `mimeTypes()`、`mimeData()`、`dropMimeData()`；
- `supportedDropActions()`；
- `sort()`。

视图通过这些函数工作。重写或扩展模型行为时，应保持 `QAbstractItemModel` 的 begin/end 通知、索引有效性和线程约定。

## 15. 生命周期和线程

`QStandardItemModel` 是 `QObject`，可设置 parent。它通常和视图在 GUI 线程使用。模型及其 item 树不应由多个线程同时读写；后台线程应准备普通数据，再通过 queued signal/slot 在模型所属线程更新。

模型析构会清理其拥有的 item、header item 和 prototype。视图持有的 `QModelIndex` 不应在模型销毁后继续使用。

## 16. 常见误区与排查顺序

### 16.1 新 item 被手动 delete

插入模型后由模型负责所有权。要移除并保留指针，使用 `take*()`。

### 16.2 把 `itemFromIndex()` 当成纯查询

设置了 prototype 时，某些空位置可能在转换时懒创建 item。只想判断位置是否有 item 时，先按业务需要选择 `item()` 或检查 index。

### 16.3 直接改 item 但视图不刷新

通过所属 item API 修改通常会触发模型通知；自定义 item 的 `setData()` 绕过基类时要调用 `emitDataChanged()`。

### 16.4 结构改变却没有模型通知

不要直接操作内部 child 表。使用 model/item 的插入、移除 API，让模型维护索引和发出 begin/end 信号。

### 16.5 混用 model index 和 item 行号

树节点下的 row 是相对于该 parent 的，不是全局行号。`index(row, column, parent)` 的 parent 必须传对。

### 16.6 排序后继续使用旧行号

排序、插入和删除都会改变行号。需要跨变化保存位置时使用 persistent index 或重新从 item 获取 index。

### 16.7 role 编号不稳定

自定义 role 是模型接口的一部分。尤其对 QML、代理和序列化，角色编号和名称要稳定。

## 17. 逐项 API 说明

### 构造和生命周期

- `QStandardItemModel(QObject *parent = nullptr)`：创建空模型。
- `QStandardItemModel(int rows, int columns, QObject *parent = nullptr)`：创建指定顶层尺寸的模型。
- `~QStandardItemModel()`：销毁模型及其拥有的 item、表头和 prototype。
- `QStandardItemModel(QStandardItemModelPrivate &, QObject *)`：protected 内部构造，不用于普通应用。
- 模型不可复制，不能用复制赋值共享 item 树。

### role 和属性

- `setItemRoleNames(const QHash<int, QByteArray> &)`：设置 role 名称映射。
- `roleNames() const`：读取 role 名称映射。
- `sortRole() const`：读取排序 role，通常默认 `DisplayRole`。
- `setSortRole(int)`：设置排序 role。
- `bindableSortRole()`：获取可绑定的 `QBindable<int>`。

### 标准模型虚函数

- `index(int, int, const QModelIndex &)`：创建子索引。
- `parent(const QModelIndex &)`：返回索引的父索引。
- `rowCount(const QModelIndex &)`：查询指定层级行数。
- `columnCount(const QModelIndex &)`：查询指定层级列数。
- `hasChildren(const QModelIndex &)`：判断指定层级是否有子项。
- `data(const QModelIndex &, int role)`：读取角色数据。
- `multiData(const QModelIndex &, QModelRoleDataSpan)`：批量读取角色。
- `setData(const QModelIndex &, const QVariant &, int role)`：写入角色数据。
- `clearItemData(const QModelIndex &)`：清除指定索引的角色数据。
- `headerData(int, Qt::Orientation, int)`：读取表头数据。
- `setHeaderData(int, Qt::Orientation, const QVariant &, int)`：写入表头数据。
- `flags(const QModelIndex &)`：读取 item flags。
- `insertRows(int, int, const QModelIndex &)`：在指定 parent 插入空行。
- `insertColumns(int, int, const QModelIndex &)`：插入空列。
- `removeRows(int, int, const QModelIndex &)`：移除行。
- `removeColumns(int, int, const QModelIndex &)`：移除列。
- `itemData(const QModelIndex &)`：批量读取 role map。
- `setItemData(const QModelIndex &, const QMap<int, QVariant> &)`：批量写入 role map。
- `mimeTypes() const`、`mimeData(const QModelIndexList &) const`、`dropMimeData(...)`：拖放 MIME 支持。
- `supportedDropActions() const`：声明支持的拖放动作。
- `sort(int, Qt::SortOrder)`：按列排序。

### 模型控制和 item 转换

- `clear()`：清空整个模型及表头。
- `itemFromIndex(const QModelIndex *)`：索引转 item，可能触发 prototype 懒创建。
- `indexFromItem(const QStandardItem *)`：item 转索引。
- `invisibleRootItem()`：获取不可见根 item。
- `item(int, int)`：读取顶层 item。
- `setItem(int, int, QStandardItem *)`：设置顶层 item 并接管所有权。
- `setItem(int, QStandardItem *)`：设置第 0 列 item。

### 表头

- `horizontalHeaderItem(int) const`：读取水平表头 item。
- `setHorizontalHeaderItem(int, QStandardItem *)`：设置水平表头并接管所有权。
- `verticalHeaderItem(int) const`：读取垂直表头 item。
- `setVerticalHeaderItem(int, QStandardItem *)`：设置垂直表头并接管所有权。
- `setHorizontalHeaderLabels(const QStringList &)`：批量设置水平表头文本。
- `setVerticalHeaderLabels(const QStringList &)`：批量设置垂直表头文本。

### 结构和所有权

- `setRowCount(int)`、`setColumnCount(int)`：调整顶层尺寸。
- `appendRow(const QList<QStandardItem *> &)`、`appendRow(QStandardItem *)`：追加行。
- `appendColumn(const QList<QStandardItem *> &)`：追加列。
- `insertRow(int, const QList<QStandardItem *> &)`、`insertRow(int, QStandardItem *)`：插入 item 行。
- `insertColumn(int, const QList<QStandardItem *> &)`：插入 item 列。
- `insertRow(int, const QModelIndex &)`、`insertColumn(int, const QModelIndex &)`：使用基类接口插入空结构。
- `takeItem(int, int)`：移除并交还一个 item。
- `takeRow(int)`、`takeColumn(int)`：移除并交还一行/列。
- `takeHorizontalHeaderItem(int)`、`takeVerticalHeaderItem(int)`：移除并交还表头 item。

### 查找和 prototype

- `findItems(const QString &, Qt::MatchFlags, int)`：按文本和匹配 flags 查找 item。
- `itemPrototype() const`：读取 prototype，不转移所有权。
- `setItemPrototype(const QStandardItem *)`：设置 prototype，由模型保存并使用其 clone 能力。

### 信号

- `itemChanged(QStandardItem *)`：item 数据或相关状态变化时通知。

## API 速查表

| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 构造 | `QStandardItemModel(QObject *)` | 创建空模型 | 模型是 QObject，可有 parent |
| 构造 | `QStandardItemModel(int, int, QObject *)` | 创建指定尺寸模型 | 尺寸是顶层结构 |
| 生命周期 | `~QStandardItemModel()` | 销毁模型和所有权内对象 | 视图索引不可继续使用 |
| 属性 | `sortRole` | 指定排序 role | 默认通常为 `DisplayRole` |
| 属性 | `bindableSortRole()` | 获取排序 role 绑定 | 绑定不自动替你设计刷新事务 |
| role | `setItemRoleNames()` / `roleNames()` | 设置/读取 role 名称 | 编号和名称应稳定 |
| 索引 | `index()` / `parent()` | 建立树索引关系 | parent 层级必须正确 |
| 尺寸 | `rowCount()` / `columnCount()` | 查询层级尺寸 | 默认 parent 表示顶层 |
| 数据 | `data()` / `setData()` | 读写 index role | 默认读 DisplayRole、写 EditRole |
| 数据 | `multiData()` | 批量读取角色 | Qt 6.0 起 |
| 数据 | `clearItemData()` | 清除一个索引的角色数据 | 不删除 item 和结构 |
| 数据 | `itemData()` / `setItemData()` | 批量读写角色 map | 更新仍要考虑通知数量 |
| 状态 | `flags()` | 读取 item 交互能力 | 由 item flags 决定 |
| 结构 | `insertRows()` / `insertColumns()` | 按 parent 插入空结构 | 维护模型通知和索引 |
| 结构 | `removeRows()` / `removeColumns()` | 删除结构 | 通常销毁被移除 item |
| 结构 | `setRowCount()` / `setColumnCount()` | 调整顶层尺寸 | 缩小可能删除对象 |
| item | `item()` | 查询顶层 item | 空单元可返回 nullptr |
| item | `itemFromIndex()` | index 转 item | 可能按 prototype 懒创建 |
| item | `indexFromItem()` | item 转 index | item 必须属于该模型 |
| 根节点 | `invisibleRootItem()` | 获取不可见根 | 根本身通常没有有效展示 index |
| 所有权 | `setItem()` | 放置 item | 模型接管并可能删除旧 item |
| 所有权 | `takeItem()` | 取出 item | 所有权交给调用方 |
| 所有权 | `takeRow()` / `takeColumn()` | 取出整行/列 | 不使用时调用方负责释放 |
| 表头 | `horizontalHeaderItem()` / `verticalHeaderItem()` | 查询表头 item | 表头也是 item |
| 表头 | `setHorizontalHeaderItem()` / `setVerticalHeaderItem()` | 设置表头 item | 替换旧对象时注意所有权 |
| 表头 | `setHorizontalHeaderLabels()` / `setVerticalHeaderLabels()` | 批量设置表头文本 | 不等于设置 view header 样式 |
| 追加 | `appendRow()` / `appendColumn()` | 末尾添加 item 结构 | 插入后模型拥有 item |
| 插入 | `insertRow()` / `insertColumn()` | 指定位置添加 item | 位置相对顶层 |
| 清空 | `clear()` | 清空 item 树和表头 | 所有被模型拥有的 item 会被清理 |
| 查找 | `findItems()` | 按文本查找 | MatchFlags 决定匹配范围 |
| 排序 | `sort()` | 按列排序 | 改变行序，旧行号可能失效 |
| MIME | `mimeTypes()` | 列出拖放格式 | 自定义格式需同步 drop |
| MIME | `mimeData()` | 生成拖放数据 | 需要处理选中索引 |
| MIME | `dropMimeData()` | 接收拖放数据 | 检查 action、MIME 和位置 |
| 拖放 | `supportedDropActions()` | 声明拖放动作 | 声明不等于实现成功 |
| prototype | `itemPrototype()` | 获取 item 原型 | 不转移所有权 |
| prototype | `setItemPrototype()` | 设置 item 原型 | 模型使用 clone 懒创建 |
| 信号 | `itemChanged(QStandardItem *)` | 通知 item 变化 | 避免槽中递归修改同一 item |
| 重写 | `QAbstractItemModel` 虚函数族 | 支撑视图/代理访问 | 遵守 begin/end 和索引契约 |

---

### 一句话总结

`QStandardItemModel` 是一棵由模型拥有的 item 树和表格：用 `QModelIndex` 服务视图，用 role 数据服务显示和编辑，用 `take*` 转移所有权，用 `insert/remove` 维护结构通知；`itemFromIndex()` 的 prototype 懒创建、排序后的索引变化和 role 编号稳定性是最需要记住的边界。
