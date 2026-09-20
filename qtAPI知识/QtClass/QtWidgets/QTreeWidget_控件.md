# Qt QTreeWidget 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QTreeWidget>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QTreeView -> QTreeWidget`  
> 直接搭档：`QTreeWidgetItem`

## 1. QTreeWidget 解决什么问题

`QTreeWidget` 是 Qt 提供的“内置 item 模型的树控件”。它把树的可视部分和一个默认的 item 管理机制打包在一起，因此不需要先编写 `QAbstractItemModel`，就可以直接创建父节点、子节点、列文本和勾选状态。

它适合以下场景：

- 文件夹、项目、设备、分类等层级数据；
- 数据量中小、结构由界面代码直接组装；
- 需要快速完成展开、折叠、选择、排序和编辑；
- 节点数量有限，开发效率比极致性能更重要。

它不适合以下场景：

- 数十万节点或频繁增删的大型数据树；
- 数据来自数据库、远程服务或多个业务源，需要独立于界面复用；
- 需要虚拟化、懒加载、复杂代理绘制和精细模型控制。

这些情况通常应该使用 `QTreeView + 自定义 QAbstractItemModel`。两者的选择可以这样理解：

| 类 | 负责什么 | 适合什么 |
| --- | --- | --- |
| `QTreeView` | 只负责树形视图，数据来自外部 model。 | 大数据、复杂数据源、可复用模型。 |
| `QTreeWidget` | 视图和 item 管理一起提供。 | 快速开发、中小型树、直接操作节点。 |
| `QTreeWidgetItem` | 一个节点的数据、状态和父子关系。 | `QTreeWidget` 中的实际树项。 |

`QTreeWidget` 不是“存数据的节点类”。树节点的数据主要放在 `QTreeWidgetItem` 中，`QTreeWidget` 负责把这些节点显示出来并处理用户交互。

## 2. 最小可用代码

```cpp
#include <QTreeWidget>
#include <QTreeWidgetItem>

auto *tree = new QTreeWidget;
tree->setColumnCount(2);
tree->setHeaderLabels({tr("Name"), tr("Value")});

auto *root = new QTreeWidgetItem(tree, {tr("Root"), tr("1")});
new QTreeWidgetItem(root, {tr("Child"), tr("2")});

tree->expandAll();
tree->show();
```

构造 `QTreeWidgetItem(tree, ...)` 时，item 会直接成为树的顶层节点；构造 `QTreeWidgetItem(root, ...)` 时，item 会成为 `root` 的子节点。两种构造方式都会把 item 加入相应的树结构，后续由树或父 item 负责其生命周期。

## 3. 三层对象关系：树、视图索引和树项

使用 `QTreeWidget` 时，最好先分清三个层次：

1. **`QTreeWidget`**：窗口中的控件，负责列、表头、当前项、选择、展开折叠、滚动和拖放。
2. **`QTreeWidgetItem`**：一个节点对象，负责文本、图标、勾选、角色数据和父子关系。
3. **`QModelIndex`**：视图层访问 model 的索引，可以通过 `indexFromItem()` 和 `itemFromIndex()` 与 item 互转。

```text
QTreeWidget
  ├─ 顶层 QTreeWidgetItem
  │    ├─ 子 QTreeWidgetItem
  │    └─ 子 QTreeWidgetItem
  └─ 另一个顶层 QTreeWidgetItem
```

`QModelIndex` 不是 item 的所有权句柄。它只是一个访问位置；对应 item 被移除或销毁后，之前缓存的普通 `QModelIndex` 不能继续使用。需要重新从当前 item 获取索引，或者重新从当前索引取 item。

## 4. 列数、表头和顶层 item

### 4.1 先设置列数

```cpp
tree->setColumnCount(3);
int count = tree->columnCount();
```

列数决定 item 可以显示多少列数据。通常应在批量创建 item 前设置好列数，这样代码中的列含义稳定，也便于设置表头。

### 4.2 设置表头

最简单的方式是设置表头文本：

```cpp
tree->setHeaderLabels({tr("Name"), tr("Type"), tr("Value")});
```

如果需要为表头设置图标、字体、对齐方式或角色数据，可以直接创建表头 item：

```cpp
auto *header = new QTreeWidgetItem({tr("Name"), tr("Value")});
header->setFont(0, QFont({}, 10, QFont::Bold));
tree->setHeaderItem(header);
```

设置为表头后，`header` 由树负责管理。不要再把同一个 item 同时当作普通顶层 item 使用，也不要手动删除仍被树管理的表头 item。

### 4.3 顶层 item 的所有权

```cpp
auto *item = new QTreeWidgetItem({tr("Project"), tr("Enabled")});
tree->addTopLevelItem(item);       // 树接管 item

auto *taken = tree->takeTopLevelItem(0); // 从树中移出
delete taken;                            // 不再使用时由调用方删除
```

把 item 加入树后，树拥有这个 item；树销毁时会销毁仍在树中的顶层 item 及其子孙节点。

`takeTopLevelItem()` 是“移出并返回”，不是“删除”。调用后：

- item 不再属于这棵树；
- 子节点仍跟随该 item；
- 调用方获得 item 的管理责任；
- 如果不打算复用，应该 `delete`。`QTreeWidgetItem` 不是 `QObject`，不能调用 `deleteLater()`。

## 5. QTreeWidgetItem：树真正的数据载体

`QTreeWidgetItem` 可以保存：

- 每列的文本、图标和提示文字；
- 字体、前景色、背景色和对齐方式；
- 勾选状态、可编辑/可选/可拖放等 item flags；
- 自定义角色数据；
- 子节点、父节点和展开状态；
- 用于排序的比较逻辑。

常用写法：

```cpp
auto *item = new QTreeWidgetItem({tr("Project"), tr("Enabled")});
item->setCheckState(1, Qt::Checked);
item->setExpanded(true);
item->setFirstColumnSpanned(true);
tree->addTopLevelItem(item);
```

父子关系可以通过构造函数直接建立，也可以在创建后再添加：

```cpp
auto *parent = new QTreeWidgetItem;
auto *child = new QTreeWidgetItem;

parent->addChild(child);
tree->addTopLevelItem(parent);
```

不要让同一个 item 同时属于两个父节点。一个 item 被加入新父节点时，必须先从旧父节点或旧树中移除。

## 6. 选择、当前项和查找

“当前项”和“选中项”不是一个概念：

- **当前项**：键盘焦点所在的主要 item，只有一个当前位置；
- **选中项**：用户选择的 item 集合，是否允许多个由选择模式决定。

```cpp
QTreeWidgetItem *current = tree->currentItem();
tree->setCurrentItem(item);
tree->setCurrentItem(item, 1);

const QList<QTreeWidgetItem *> selected = tree->selectedItems();
```

常见定位方式：

- `itemAt(QPoint)`：根据控件坐标命中 item；
- `visualItemRect(item)`：得到 item 当前可视行的矩形；
- `findItems(text, flags, column)`：按某列文本查找；
- `itemAbove(item)` / `itemBelow(item)`：查找相邻可见 item；
- `scrollToItem(item)`：把 item 滚动到可视区域。

`itemAt()` 使用的是 `QTreeWidget` 自身的坐标，不是窗口坐标，也不是屏幕坐标。若坐标来自鼠标事件，通常可以直接使用事件提供的局部坐标。

## 7. 展开、折叠和懒加载

```cpp
tree->expandItem(item);
tree->collapseItem(item);
tree->expandAll();
tree->collapseAll();
```

如果节点有大量后代，不要无条件调用 `expandAll()`。它会递归展开整棵树，可能导致大量布局、绘制和滚动区域计算。

需要“点击展开时才加载子节点”时，可以使用 `itemExpanded()` 信号；如果希望没有真实子节点的 item 也显示展开指示器，可以使用 `QTreeWidgetItem::setChildIndicatorPolicy()`：

```cpp
item->setChildIndicatorPolicy(QTreeWidgetItem::ShowIndicator);

connect(tree, &QTreeWidget::itemExpanded,
        tree, [tree](QTreeWidgetItem *item) {
    if (item->childCount() == 0) {
        // 根据业务数据加载子节点
        new QTreeWidgetItem(item, {QObject::tr("Loaded child")});
    }
});
```

这只是轻量懒加载方案。数据量很大或需要异步模型时，仍应优先使用 `QTreeView` 和自定义 model。

## 8. 单元格 widget 和 item 数据

```cpp
tree->setItemWidget(item, 1, new QLineEdit);
QWidget *editor = tree->itemWidget(item, 1);
tree->removeItemWidget(item, 1);
```

这里有两个完全不同的存储层次：

| 方式 | 存储的是什么 | 适合什么 |
| --- | --- | --- |
| `QTreeWidgetItem::setText()`、`setData()` 等 | item 数据和显示角色。 | 文本、图标、勾选、颜色、排序。 |
| `QTreeWidget::setItemWidget()` | 真实的 `QWidget` 子控件。 | 少量静态或简单交互控件。 |

`setItemWidget()` 会让树管理这个 widget。它适合少量、基本不变化的单元格控件；大量 item 都放真实 widget 会明显增加对象、布局和绘制开销。

如果只是为了自定义显示或编辑，不要优先给每个 item 塞一个 `QLineEdit`、`QComboBox`。对于大量节点，应该使用 `QTreeView` 的 delegate，在需要编辑时临时创建编辑器。

`removeItemWidget()` 只是把控件从该 item 的单元格显示关系中移除。不要把它当成 item 数据清理 API，也不要在不确认所有权的情况下继续持有已经移除的 widget。

## 9. 父子节点操作和所有权

```cpp
auto *child = new QTreeWidgetItem(item, {tr("Child"), tr("42")});

QTreeWidgetItem *taken = item->takeChild(0);
delete taken;
```

需要区分三类操作：

| 操作 | 结果 | 调用方要注意什么 |
| --- | --- | --- |
| `addChild()` / `insertChild()` | 把 item 加入父节点。 | 父节点接管 item。 |
| `removeChild(child)` | 从父节点移除 item，但不返回它。 | item 已不再由父节点管理，调用方应保存指针并负责后续处理。 |
| `takeChild(index)` | 移除并返回 item。 | 调用方获得 item，复用或删除都由调用方决定。 |
| `takeChildren()` | 移除并返回所有子节点。 | 返回的 item 列表由调用方管理。 |

`removeChild()` 适合你已经持有 item 指针的场景；`takeChild()` 适合按索引取出并继续处理的场景。无论哪一种，移出后都不能再假设父节点会替你删除它。

## 10. 排序

```cpp
tree->sortItems(0, Qt::AscendingOrder);
item->sortChildren(0, Qt::DescendingOrder);
```

排序只改变同一父节点下的兄弟节点顺序，不会把子节点提升到顶层，也不会改变父子关系。

批量构建时，建议暂时关闭排序：

```cpp
tree->setSortingEnabled(false);
// 批量添加和修改 item
tree->setSortingEnabled(true);
tree->sortItems(0, Qt::AscendingOrder);
```

自定义 `QTreeWidgetItem` 时可以重写 `operator<()`，让排序使用数值、时间或业务优先级，而不是简单按显示文本比较。排序比较函数应保持稳定、可重复，不要在比较过程中修改 item。

## API 速查表
### 11.1 QTreeWidget：创建、列和表头

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 生命周期 | `QTreeWidget(QWidget *parent = nullptr)` | 创建树控件。 | `parent` 是 QObject 父对象；顶层窗口通常再调用 `show()`。 |
| 生命周期 | `~QTreeWidget()` | 销毁树控件及仍由它管理的 item。 | 不要再访问已被树销毁的 item 指针。 |
| 列 | `columnCount()` | 返回当前列数。 | 只返回列数量，不代表任何 item 已经有数据。 |
| 列 | `setColumnCount(int columns)` | 设置树显示的列数。 | 批量创建 item 前先设置，列索引从 0 开始。 |
| 顶层节点 | `topLevelItemCount()` | 返回顶层 item 数量。 | 不包含子孙节点。 |
| 顶层节点 | `topLevelItem(int index)` | 按索引读取顶层 item。 | 索引无效时返回 `nullptr`；返回指针不转移所有权。 |
| 顶层节点 | `addTopLevelItem(QTreeWidgetItem *item)` | 把 item 追加为顶层节点。 | 树接管 item；item 不能同时属于别的树或父节点。 |
| 顶层节点 | `addTopLevelItems(const QList<QTreeWidgetItem *> &items)` | 批量追加顶层 item。 | 加入后由树管理；批量操作时注意排序和信号开销。 |
| 顶层节点 | `insertTopLevelItem(int index, QTreeWidgetItem *item)` | 在指定位置插入顶层 item。 | 插入后后续顶层索引可能全部变化。 |
| 顶层节点 | `insertTopLevelItems(int index, const QList<QTreeWidgetItem *> &items)` | 在指定位置批量插入顶层 item。 | 不要把旧索引当成稳定身份。 |
| 顶层节点 | `takeTopLevelItem(int index)` | 移出并返回一个顶层 item。 | 不会删除 item；移出后由调用方负责复用或 `delete`。 |
| 隐藏根节点 | `invisibleRootItem()` | 返回代表整棵树的隐藏根 item。 | 适合统一遍历顶层节点；它不是用户可见节点，不要把它当普通业务 item 删除。 |
| 表头 | `headerItem()` | 返回当前表头 item。 | 返回的是树管理的对象，不要手动删除。 |
| 表头 | `setHeaderItem(QTreeWidgetItem *item)` | 用 item 设置复杂表头。 | item 所有权交给树；不能再把它用作普通树节点。 |
| 表头 | `setHeaderLabels(const QStringList &labels)` | 设置各列表头文本。 | 只设置文本；需要图标、字体或角色数据时使用 `setHeaderItem()`。 |
| 表头 | `setHeaderLabel(const QString &label)` | 设置单列表头文本的便捷函数。 | 本质上是设置一个字符串列表。 |

### 11.2 QTreeWidget：当前项、选择和查找

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 当前项 | `currentItem()` | 返回当前拥有键盘焦点语义的 item。 | 没有当前项时返回 `nullptr`；当前项不等于所有选中项。 |
| 当前项 | `currentColumn()` | 返回当前项所在列。 | 没有当前项时通常为无效列值；与 `currentItem()` 一起使用。 |
| 当前项 | `setCurrentItem(QTreeWidgetItem *item)` | 设置当前 item。 | item 必须属于这棵树；传 `nullptr` 可清除当前项。 |
| 当前项 | `setCurrentItem(QTreeWidgetItem *item, int column)` | 设置当前 item 和当前列。 | 列索引必须有效；设置当前项可能触发当前项变化信号。 |
| 当前项 | `setCurrentItem(QTreeWidgetItem *item, int column, QItemSelectionModel::SelectionFlags command)` | 设置当前 item、当前列以及选择模型要执行的选择命令。 | 适合在设置当前项的同时控制选中/取消选中；传入的 item 仍必须属于此树。 |
| 坐标命中 | `itemAt(const QPoint &point)` | 根据树控件局部坐标找 item。 | 坐标不是屏幕坐标；没有命中时返回 `nullptr`。 |
| 坐标命中 | `itemAt(int x, int y)` | 以横纵坐标调用 `itemAt(QPoint)` 的便捷重载。 | 同样使用控件局部坐标。 |
| 可视区域 | `visualItemRect(const QTreeWidgetItem *item)` | 返回 item 当前可见行的矩形。 | item 不可见或不属于此树时可能得到无效矩形；矩形会随滚动和布局变化。 |
| 查找 | `findItems(const QString &text, Qt::MatchFlags flags, int column)` | 在指定列按匹配规则查找 item。 | 返回的是当前 item 指针列表；移除或销毁 item 后旧指针不能继续使用。 |
| 选择 | `selectedItems()` | 返回当前所有被选中的 item。 | 结果是列表副本；多选需要配合合适的 selection mode。 |
| 单元格控件 | `itemWidget(QTreeWidgetItem *item, int column)` | 取得 item 某列上的真实 widget。 | 没有控件时返回 `nullptr`；返回指针由树管理。 |
| 单元格控件 | `setItemWidget(QTreeWidgetItem *item, int column, QWidget *widget)` | 把真实 QWidget 放入 item 的某列。 | 树接管 widget；适合少量静态控件，不适合大规模动态单元格。 |
| 单元格控件 | `removeItemWidget(QTreeWidgetItem *item, int column)` | 移除 item 某列的 widget 显示关系。 | 不等同于清除 item 数据；移除后的 widget 生命周期不要想当然。 |

### 11.3 QTreeWidget：展开、滚动、排序和索引

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 展开 | `expandItem(const QTreeWidgetItem *item)` | 展开指定 item。 | 只改变该节点的展开状态，不会自动加载业务数据。 |
| 折叠 | `collapseItem(const QTreeWidgetItem *item)` | 折叠指定 item。 | 子节点仍存在，只是暂时不可见。 |
| 滚动 | `scrollToItem(const QTreeWidgetItem *item, ScrollHint hint = EnsureVisible)` | 把 item 滚动到可见区域。 | item 必须仍属于此树；滚动只改变视口位置。 |
| 相邻项 | `itemAbove(const QTreeWidgetItem *item)` | 返回视觉上方的相邻可见 item。 | 不是按内存顺序；没有相邻项时返回 `nullptr`。 |
| 相邻项 | `itemBelow(const QTreeWidgetItem *item)` | 返回视觉下方的相邻可见 item。 | 折叠的子节点不会作为可见相邻项返回。 |
| 顶层索引 | `indexOfTopLevelItem(QTreeWidgetItem *item)` | 查询 item 在顶层节点列表中的索引。 | item 不属于这棵树时返回 `-1`；插入、删除和排序后索引可能变化。 |
| 排序 | `sortColumn()` | 返回当前排序列。 | 只表示排序状态，不会执行排序。 |
| 排序 | `sortItems(int column, Qt::SortOrder order)` | 按指定列对各层级的兄弟 item 排序。 | 不改变父子关系；批量插入时可先关闭 sorting。 |
| 索引转换 | `indexFromItem(const QTreeWidgetItem *item, int column = 0)` | 把 item 和列转换成 `QModelIndex`。 | 索引不是所有权；item 被移除/销毁或 model 结构变化后不要继续缓存普通索引。 |
| 索引转换 | `itemFromIndex(const QModelIndex &index)` | 把属于此树 model 的索引转换回 item。 | 传入无效索引或其他 model 的索引时返回 `nullptr`。 |
| 拖放 | `supportedDragActions()` | 读取树允许的拖放动作。 | 只描述支持的动作，实际拖放还受视图属性和事件处理影响。 |
| 拖放 | `setSupportedDragActions(Qt::DropActions actions)` | 设置树支持的拖放动作。 | 需要同时配置拖放模式、flags 和 MIME 数据处理。 |
| 编辑 | `editItem(QTreeWidgetItem *item, int column = 0)` | 请求对指定 item 的某列开始编辑。 | item 必须允许编辑；真正的编辑器由视图 delegate 创建。 |
| 持久编辑 | `openPersistentEditor(QTreeWidgetItem *item, int column = 0)` | 打开并保持某列的编辑器。 | 会长期占用编辑器资源；不用时调用 `closePersistentEditor()`。 |
| 持久编辑 | `closePersistentEditor(QTreeWidgetItem *item, int column = 0)` | 关闭指定 item 某列的持久编辑器。 | 只关闭编辑器，不删除 item 数据。 |
| 持久编辑 | `isPersistentEditorOpen(QTreeWidgetItem *item, int column = 0)` | 查询某列是否有持久编辑器。 | 编辑器状态不等于 item 是否可编辑。 |
| 清空 | `clear()` | 删除树中所有顶层 item 及其子孙节点，并清理选择和视图状态。 | 调用后原有 item 指针全部失效；不要在清空后继续使用。 |

### 11.4 QTreeWidget：交互信号

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 鼠标交互 | `itemPressed(QTreeWidgetItem *item, int column)` | item 被鼠标按下时发出。 | 发生在 clicked 之前，适合记录按下状态。 |
| 鼠标交互 | `itemClicked(QTreeWidgetItem *item, int column)` | item 被单击时发出。 | 不等于双击业务；需要区分激活行为时使用 `itemActivated()`。 |
| 鼠标交互 | `itemDoubleClicked(QTreeWidgetItem *item, int column)` | item 被双击时发出。 | 不要和自动展开行为重复执行同一业务。 |
| 激活 | `itemActivated(QTreeWidgetItem *item, int column)` | item 被激活时发出，例如回车或平台定义的激活操作。 | 比单纯鼠标点击更适合“打开节点”这类语义。 |
| 鼠标悬停 | `itemEntered(QTreeWidgetItem *item, int column)` | 鼠标进入 item 时发出。 | 通常需要开启 mouse tracking 才能稳定获得悬停通知。 |
| 数据变化 | `itemChanged(QTreeWidgetItem *item, int column)` | item 某列的数据或显示角色变化时发出。 | 在槽函数中再次修改 item 可能造成递归或重复处理，必要时使用信号阻塞。 |
| 展开状态 | `itemExpanded(QTreeWidgetItem *item)` | item 展开后发出。 | 适合懒加载、恢复子节点或保存展开状态。 |
| 展开状态 | `itemCollapsed(QTreeWidgetItem *item)` | item 折叠后发出。 | 子节点没有被删除，只是不可见。 |
| 当前项 | `currentItemChanged(QTreeWidgetItem *current, QTreeWidgetItem *previous)` | 当前 item 变化时发出。 | `current` 或 `previous` 可能为 `nullptr`。 |
| 选择状态 | `itemSelectionChanged()` | 选择集合变化时发出。 | 需要读取具体项时调用 `selectedItems()`；它不直接携带 item 参数。 |

### 11.5 QTreeWidget：编辑、清理和扩展

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 选择模型 | `setSelectionModel(QItemSelectionModel *selectionModel)` | 为树设置选择模型。 | 这是对 inherited API 的重载；选择模型必须与树使用的 model 匹配。 |
| 事件 | `event(QEvent *event)` | 处理树控件自身的事件。 | 通常不需要重写；重写时应保留基类处理结果。 |
| 拖放扩展 | `mimeTypes()` | 返回树支持的 MIME 类型列表。 | 自定义拖放数据格式时重写；需要和 `mimeData()`、`dropMimeData()` 配套。 |
| 拖放扩展 | `mimeData(const QList<QTreeWidgetItem *> &items)` | 把选中的 item 编码成拖放用的 `QMimeData`。 | 返回对象由调用方/Qt 拖放流程管理；不要依赖传入 item 列表在拖放后仍有效。 |
| 拖放扩展 | `dropMimeData(QTreeWidgetItem *parent, int index, const QMimeData *data, Qt::DropAction action)` | 把拖放数据解码并插入到指定父 item 的位置。 | 自定义导入逻辑时重写；要检查数据格式、目标父节点和 action。 |
| 拖放扩展 | `supportedDropActions()` | 返回树可以接受的拖放动作。 | 和 `supportedDragActions()` 不同，一个描述接收，一个描述发起。 |

### 11.6 QTreeWidgetItem：构造、复制和节点状态

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QTreeWidgetItem(int type = Type)` | 创建一个暂时没有父节点的 item。 | 加入树或父节点后才会显示；未加入时由调用方负责删除。 |
| 构造 | `QTreeWidgetItem(const QStringList &strings, int type = Type)` | 创建带各列文本的 item。 | 文本顺序对应列索引。 |
| 构造 | `QTreeWidgetItem(QTreeWidget *tree, ...)` | 创建并直接加入指定树的顶层 item。 | 树接管所有权。 |
| 构造 | `QTreeWidgetItem(QTreeWidgetItem *parent, ...)` | 创建并直接加入指定父 item 的子节点。 | 父 item 接管所有权。 |
| 构造 | `QTreeWidgetItem(..., QTreeWidgetItem *after, ...)` | 创建并插入到指定兄弟节点之后。 | `after` 必须属于相同父节点/树结构。 |
| 复制 | `QTreeWidgetItem(const QTreeWidgetItem &other)` | 复制 item 的数据和子树内容。 | 复制结果不是自动加入原树的独立 item。 |
| 生命周期 | `~QTreeWidgetItem()` | 销毁 item 及其仍归它管理的子节点。 | 删除已在树中的 item 前必须先移除，避免破坏树结构。 |
| 复制 | `clone()` | 虚复制函数，创建当前 item 类型的副本。 | 自定义 item 时重写它，才能保留派生类型数据。 |
| 类型 | `type()` | 返回 item 的类型编号。 | 自定义类型通常使用 `UserType` 以上的编号。 |
| 所属树 | `treeWidget()` | 返回当前 item 所属的 `QTreeWidget`。 | 未加入树时返回 `nullptr`；item 移出树后不要继续使用旧的树指针。 |
| 选择状态 | `setSelected(bool select)` | 设置 item 是否被选中。 | 需要 item 已属于树；最终结果还受选择模式和选择模型影响。 |
| 选择状态 | `isSelected()` | 查询 item 是否被选中。 | 只反映当前选择状态，不代表它是 current item。 |
| 可见性 | `setHidden(bool hide)` | 隐藏或显示 item。 | 隐藏不会删除 item，也不会改变父子关系。 |
| 可见性 | `isHidden()` | 查询 item 是否被隐藏。 | 父节点折叠造成的不可见不等同于 item 自身 hidden。 |
| 展开状态 | `setExpanded(bool expand)` | 设置 item 展开或折叠。 | 只有有子节点或显示子节点指示器时才有明显展开效果。 |
| 展开状态 | `isExpanded()` | 查询 item 的展开状态。 | 返回的是节点状态，不是当前是否在屏幕上可见。 |
| 列显示 | `setFirstColumnSpanned(bool span)` | 让第一列内容跨过整行列区域。 | 常用于分组标题；会改变该行的列显示方式。 |
| 列显示 | `isFirstColumnSpanned()` | 查询第一列是否跨行。 | 只影响显示，不会合并数据列。 |
| 子节点指示器 | `setChildIndicatorPolicy(ChildIndicatorPolicy policy)` | 控制是否显示可展开指示器。 | `ShowIndicator` 适合在真正加载子节点前提示用户可以展开。 |
| 子节点指示器 | `childIndicatorPolicy()` | 查询子节点指示器策略。 | 与懒加载、占位子节点配合使用。 |
| 启用状态 | `setDisabled(bool disabled)` | 通过 flags 禁用或启用 item。 | 禁用状态影响交互，不等于隐藏。 |
| 启用状态 | `isDisabled()` | 查询 item 是否禁用。 | 本质上是检查 `Qt::ItemIsEnabled` 标志。 |
| 交互标志 | `setFlags(Qt::ItemFlags flags)` | 设置可选、可编辑、可拖拽、可勾选等 item 能力。 | 修改时最好在原 flags 基础上按位增删，不要无意清空默认标志。 |
| 交互标志 | `flags()` | 读取 item 的交互标志。 | 编辑、复选和拖放行为都受它影响。 |

### 11.7 QTreeWidgetItem：列数据和显示角色

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 文本 | `setText(int column, const QString &text)` | 设置指定列的显示文本。 | 列索引必须对应树的列；设置后可能触发 `itemChanged()`。 |
| 文本 | `text(int column)` | 读取指定列的显示文本。 | 它对应 `Qt::DisplayRole`，不是任意角色数据。 |
| 图标 | `setIcon(int column, const QIcon &icon)` | 设置指定列图标。 | 图标由 item 数据持有，适合小型装饰资源。 |
| 图标 | `icon(int column)` | 读取指定列图标。 | 没有图标时返回空 `QIcon`。 |
| 状态提示 | `setStatusTip(int column, const QString &statusTip)` | 设置状态栏提示文本。 | 需要界面有状态栏并由视图转发提示。 |
| 状态提示 | `statusTip(int column)` | 读取状态提示文本。 | 读不到时返回空字符串。 |
| 工具提示 | `setToolTip(int column, const QString &toolTip)` | 设置鼠标悬停提示。 | 适合补充被截断的文本或解释状态。 |
| 工具提示 | `toolTip(int column)` | 读取工具提示。 | 它对应 `Qt::ToolTipRole`。 |
| 帮助文本 | `setWhatsThis(int column, const QString &whatsThis)` | 设置 What's This 帮助文本。 | 只有进入 What's This 帮助模式时才会使用。 |
| 帮助文本 | `whatsThis(int column)` | 读取 What's This 文本。 | 它对应 `Qt::WhatsThisRole`。 |
| 字体 | `setFont(int column, const QFont &font)` | 设置指定列字体。 | 只影响该 item 的该列，过多设置会增加绘制差异。 |
| 字体 | `font(int column)` | 读取指定列字体。 | 没有显式设置时可能返回默认字体值。 |
| 对齐 | `setTextAlignment(int column, Qt::Alignment alignment)` | 设置指定列文本对齐方式。 | Qt 6 同时存在兼容的整数/标志重载；按列设置。 |
| 对齐 | `textAlignment(int column)` | 读取指定列文本对齐方式。 | 具体返回类型随 Qt 版本重载而不同，Qt 6 代码优先使用 `Qt::Alignment`。 |
| 背景 | `setBackground(int column, const QBrush &brush)` | 设置指定列背景画刷。 | 传空画刷可恢复默认；不宜用它替代 delegate 绘制大量状态。 |
| 背景 | `background(int column)` | 读取指定列背景画刷。 | 没有设置时可能返回空画刷。 |
| 前景 | `setForeground(int column, const QBrush &brush)` | 设置指定列前景画刷。 | 常用于状态颜色或警告颜色。 |
| 前景 | `foreground(int column)` | 读取指定列前景画刷。 | 没有设置时可能返回空画刷。 |
| 勾选 | `setCheckState(int column, Qt::CheckState state)` | 设置指定列复选状态。 | 还需要 `Qt::ItemIsUserCheckable` 等 flags 才适合让用户交互勾选。 |
| 勾选 | `checkState(int column)` | 读取指定列复选状态。 | 可处理 `Unchecked`、`PartiallyChecked` 和 `Checked`。 |
| 尺寸 | `setSizeHint(int column, const QSize &size)` | 为指定列提供尺寸提示。 | 它是提示，不一定覆盖视图和 style 的最终行高计算。 |
| 尺寸 | `sizeHint(int column)` | 读取指定列尺寸提示。 | 没有设置时返回无效或默认尺寸。 |
| 角色数据 | `setData(int column, int role, const QVariant &value)` | 写入指定列的任意角色数据。 | 适合保存业务 ID、排序值和自定义显示数据。 |
| 角色数据 | `data(int column, int role)` | 读取指定列指定角色的数据。 | 继承并重写它可以实现自定义数据来源或排序逻辑。 |
| 数据通知 | `emitDataChanged()` | 在自定义 item 内通知树某个 item 数据已改变。 | 这是 protected API；只有直接修改了自定义存储而没有经过 `setData()` 时才需要调用。 |

### 11.8 QTreeWidgetItem：列数、父子结构和排序

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 所属关系 | `parent()` | 返回当前 item 的父 item。 | 顶层 item 和未加入树的 item 都返回 `nullptr`；不要把 `invisibleRootItem()` 当成 `parent()` 的返回值。 |
| 子节点 | `child(int index)` | 按索引读取子 item。 | 返回指针不转移所有权；索引在插入、删除和排序后可能改变。 |
| 子节点 | `childCount()` | 返回直接子节点数量。 | 不包含更深层孙节点。 |
| 列数 | `columnCount()` | 返回 item 当前保存的列数据数量。 | 它是 item 数据列数，不一定等同于树当前的 `columnCount()`。 |
| 子节点 | `indexOfChild(QTreeWidgetItem *child)` | 查询直接子节点在父节点中的索引。 | 找不到时返回 `-1`；排序后索引可能变化。 |
| 子节点 | `addChild(QTreeWidgetItem *child)` | 在末尾添加一个子节点。 | 父 item 接管 child；child 不能同时属于其他父节点。 |
| 子节点 | `insertChild(int index, QTreeWidgetItem *child)` | 在指定索引插入子节点。 | 插入会改变后续子节点索引。 |
| 子节点 | `removeChild(QTreeWidgetItem *child)` | 从父节点移除指定子节点。 | 不返回指针；移除后调用方必须仍能取得并负责 child 的生命周期。 |
| 子节点 | `takeChild(int index)` | 移出并返回指定子节点。 | 不会删除；调用方获得管理责任。 |
| 子节点 | `addChildren(const QList<QTreeWidgetItem *> &children)` | 批量追加子节点。 | 父 item 接管所有加入的 child。 |
| 子节点 | `insertChildren(int index, const QList<QTreeWidgetItem *> &children)` | 批量插入子节点。 | 调用后旧索引和排序顺序都可能变化。 |
| 子节点 | `takeChildren()` | 移出并返回全部直接子节点。 | 返回列表中的 item 不再由父 item 管理。 |
| 排序 | `sortChildren(int column, Qt::SortOrder order)` | 按指定列对直接子节点排序。 | 只排序当前层；不会递归排序每一层。 |
| 比较 | `operator<(const QTreeWidgetItem &other)` | 定义两个 item 的排序比较关系。 | 自定义派生 item 时重写；不要在比较函数中修改数据。 |
| 赋值 | `operator=(const QTreeWidgetItem &other)` | 用另一个 item 的数据替换当前 item。 | 不会自动把当前 item 移到对方所在的树；赋值时仍要注意子树和业务身份。 |
| 序列化 | `read(QDataStream &in)` | 从数据流读取 item 数据。 | 适合自定义持久化；需和 `write()` 使用一致的数据格式。 |
| 序列化 | `write(QDataStream &out) const` | 把 item 数据写入数据流。 | 只负责 item 数据流，不等于自动保存整棵树。 |

### 11.9 QTreeWidget：常用 inherited 交互设置

下面这些 API 主要来自 `QTreeView`/`QAbstractItemView`，但在使用 `QTreeWidget` 时经常一起配置：

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 展开交互 | `setAnimated(bool)` / `isAnimated()` | 设置展开折叠是否使用动画。 | 大型树或频繁展开时动画可能增加视觉和计算开销。 |
| 行高 | `setUniformRowHeights(bool)` / `uniformRowHeights()` | 声明所有行高度一致，以优化视图计算。 | 只有确实能保证行高一致时才设为 `true`。 |
| 展开交互 | `setItemsExpandable(bool)` / `itemsExpandable()` | 控制 item 是否允许通过视图展开。 | 不会删除子节点，只限制用户展开行为。 |
| 展开交互 | `setExpandsOnDoubleClick(bool)` / `expandsOnDoubleClick()` | 控制双击是否自动展开或折叠。 | 与 `itemDoubleClicked()` 业务槽函数可能同时发生。 |
| 排序交互 | `setSortingEnabled(bool)` / `isSortingEnabled()` | 开启或关闭用户排序。 | 批量加载时通常先关闭，完成后手动排序。 |
| 表头显示 | `setHeaderHidden(bool)` / `isHeaderHidden()` | 隐藏或显示表头。 | 隐藏表头不影响列数据和列宽。 |
| 缩进 | `setIndentation(int)` / `indentation()` | 设置每层树节点的缩进像素。 | 过小会削弱层级感，过大会压缩内容列。 |
| 自动展开 | `setAutoExpandDelay(int)` / `autoExpandDelay()` | 设置拖放悬停时自动展开的延迟。 | `-1` 通常表示关闭自动展开；只影响交互行为。 |
| 选择模式 | `setSelectionMode(QAbstractItemView::SelectionMode)` / `selectionMode()` | 控制单选、多选、扩展选择等规则。 | `selectedItems()` 的结果数量取决于该设置。 |

## 12. 常见误区

### 12.1 把 QTreeWidget 当成大数据树

它把每个节点都作为对象管理，使用方便但有额外内存和对象开销。大型、频繁更新或需要虚拟化的树，应使用 `QTreeView + 自定义模型`。

### 12.2 把 QTreeWidgetItem 和 QWidget 混在一起

`QTreeWidgetItem` 是树节点数据，不是控件；`setItemWidget()` 才是在单元格里放真实 QWidget。能用 item 文本、图标、角色数据解决的问题，不要直接创建一个 QWidget。

### 12.3 `takeTopLevelItem()` 或 `takeChild()` 后仍以为树会删除 item

`take*()` 是移出并转移管理责任。需要复用就重新加入某个树或父节点，不再使用就由调用方删除。

### 12.4 用旧索引代表 item 身份

插入、删除、排序和跨层移动都会改变行号和子节点索引。业务身份应该放进 `setData(column, Qt::UserRole, id)`，需要时用 item 指针或重新建立索引，不要把整数索引当成永久 ID。

### 12.5 对每一行都放复杂单元格控件

`setItemWidget()` 会创建并维护真实 QWidget。数量一多，布局、绘制和事件处理都会变重。大量动态编辑应改用 model/delegate。

### 12.6 在 `itemChanged()` 中无条件修改 item

槽函数里再次设置文本、勾选状态或角色数据，可能再次发出 `itemChanged()`。需要程序化批量修改时，可以临时阻塞信号，或者先比较新旧值再写入。

---

### 一句话总结

`QTreeWidget` 是适合中小型层级数据的便捷树控件：`QTreeWidget` 管视图和交互，`QTreeWidgetItem` 管节点数据和父子关系，`take*()` 负责移出并转移所有权，`setItemWidget()` 负责少量真实控件，`QModelIndex` 只负责视图访问而不是永久身份。需要大规模数据、虚拟化和复杂模型时，应切换到 `QTreeView + QAbstractItemModel`。
