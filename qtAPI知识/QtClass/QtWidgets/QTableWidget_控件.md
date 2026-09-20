# Qt QTableWidget 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QTableWidget>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QTableView -> QTableWidget`  
> 常见搭档：`QTableWidgetItem`

## 1. QTableWidget 解决什么问题

`QTableWidget` 是“带内置 item 的表格控件”。它把模型和视图的复杂性包了一层，让你可以直接按行列创建 `QTableWidgetItem`，不用先自己写模型。

适合的场景：

- 小型数据表；
- 原型开发；
- 配置表格；
- 直接手写单元格内容和样式；
- 不想先写 `QAbstractTableModel` 的工具类界面。

它的代价也很清楚：数据量大、模型逻辑复杂、排序筛选重度定制时，`QTableView + 自定义模型` 更合适。

## 2. 最小可用代码

```cpp
#include <QTableWidget>
#include <QTableWidgetItem>

auto *table = new QTableWidget(2, 3);
table->setHorizontalHeaderLabels({tr("Name"), tr("Age"), tr("City")});
table->setItem(0, 0, new QTableWidgetItem(tr("Alice")));
table->setItem(0, 1, new QTableWidgetItem("18"));
table->setItem(0, 2, new QTableWidgetItem(tr("Shanghai")));
table->show();
```

`QTableWidgetItem` 才是单元格真正存文本、图标、对齐、颜色、检查状态等数据的地方。

## 3. 行列数量和表头

```cpp
table->setRowCount(10);
table->setColumnCount(5);
```

先定行列，再填 item，是最常见的顺序。  
设置表头最简单的方法是直接给字符串列表：

```cpp
table->setHorizontalHeaderLabels({tr("A"), tr("B"), tr("C")});
table->setVerticalHeaderLabels({tr("1"), tr("2"), tr("3")});
```

如果你想给表头更复杂的外观，可以直接设置 `QTableWidgetItem` 作为 header item：

```cpp
auto *header = new QTableWidgetItem(QIcon(":/icons/flag.svg"), tr("Status"));
table->setHorizontalHeaderItem(0, header);
```

`setHeaderLabels()` 不会删除现有列，只是给已有列设置标题。

## 4. item 的所有权和取出

### 4.1 setItem

```cpp
table->setItem(row, column, new QTableWidgetItem(tr("Hello")));
```

`setItem()` 会把 `QTableWidgetItem` 交给表格管理。  
你不应该在插入后再手动 delete 这个 item。

### 4.2 item 和 takeItem

```cpp
QTableWidgetItem *item = table->item(0, 0);
QTableWidgetItem *taken = table->takeItem(0, 0);
```

- `item()`：只查看，不转移所有权；
- `takeItem()`：从表格里取出 item，并把所有权交还给你。

如果 `takeItem()` 后你不再用它，就自己删除；如果要复用，可以重新插入别处。

### 4.3 行列取值

```cpp
int r = table->row(item);
int c = table->column(item);
```

`QTableWidgetItem` 也能反查自己所在的行列。这个能力来自内置 table model。

## 5. 单元格 widget 和 item 的区别

```cpp
table->setCellWidget(0, 0, new QLineEdit);
```

`setCellWidget()` 是把真实 `QWidget` 塞进单元格里。  
它和 `QTableWidgetItem` 不是一回事：

| 方式 | 适合什么 |
| --- | --- |
| `QTableWidgetItem` | 显示文本、图标、对齐、颜色、勾选状态。 |
| `setCellWidget()` | 需要真正交互控件，比如下拉框、按钮、输入框。 |

`setCellWidget()` 适合少量交互控件。大量使用会让表格变重，滚动和布局也更复杂。

要移除单元格 widget，调用：

```cpp
table->removeCellWidget(row, column);
```

它本质上等价于把单元格 widget 设为 `nullptr`。

## 6. 选择、范围和当前单元格

```cpp
table->setCurrentCell(1, 2);
table->setCurrentItem(table->item(1, 2));
table->selectRow(3);
table->selectColumn(1);
```

常见查询：

```cpp
int row = table->currentRow();
int column = table->currentColumn();
QTableWidgetItem *current = table->currentItem();
```

如果你需要整块区域选择，可以用 `QTableWidgetSelectionRange`：

```cpp
table->setRangeSelected(QTableWidgetSelectionRange(0, 0, 2, 2), true);
auto ranges = table->selectedRanges();
```

`selectedItems()` 返回当前所有被选中的 item，`itemSelectionChanged()` 是统一的选择变化信号。

## 7. 排序和自动移动行

```cpp
table->setSortingEnabled(true);
table->sortItems(1, Qt::AscendingOrder);
```

`QTableWidget` 的排序是直接对内置 item 排序。  
这意味着当你逐个 `setItem()` 填充数据时，如果已经启用了排序，行可能会在插入过程中移动。

这就是为什么官方文档也提醒：批量填充同一行时，最好先关掉排序，填完再开回去。

## 8. 清空和删除

### 8.1 clearContents

```cpp
table->clearContents();
```

只清掉单元格内容，表头和行列尺寸一般还保留。

### 8.2 clear

```cpp
table->clear();
```

它会清掉视图中的所有 item、选择和表头。  
如果你只想清数据不想动表头，用 `clearContents()`。

### 8.3 行列增删

```cpp
table->insertRow(1);
table->insertColumn(2);
table->removeRow(3);
table->removeColumn(1);
```

行列变化后，item 的位置和有效性都要重新检查。

## 9. 查找和读取

```cpp
auto found = table->findItems(tr("Alice"), Qt::MatchExactly);
```

`findItems()` 可以按文本和匹配规则查找 item。  
如果你要从鼠标坐标找当前单元格，使用：

```cpp
QTableWidgetItem *item = table->itemAt(QPoint(20, 20));
```

或者：

```cpp
QRect rect = table->visualItemRect(item);
```

## 10. QTableWidgetItem 的作用

`QTableWidgetItem` 承载每个单元格的数据和外观：

- `text() / setText()`
- `icon() / setIcon()`
- `font() / setFont()`
- `background() / setBackground()`
- `foreground() / setForeground()`
- `checkState() / setCheckState()`
- `sizeHint() / setSizeHint()`

它还能自定义比较和序列化：

- `operator<()`：用于排序；
- `clone()`：复制 item；
- `read()/write()`：数据流读写。

如果你只用 `QTableWidget` 做表格展示，大部分情况下只需要操作这些 item API，不必碰模型层。

## API 速查表
### 11.1 构造和尺寸

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QTableWidget(QWidget *parent = nullptr)` | 创建一个空的 item 表格。 | 行列数默认为 0，后续用 `setRowCount/setColumnCount` 设置。 |
| 构造 | `QTableWidget(int rows, int columns, QWidget *parent = nullptr)` | 创建指定行列数量的 item 表格。 | 只创建网格，不会自动填充 `QTableWidgetItem`。 |
| 析构 | `~QTableWidget()` | 销毁表格以及仍由表格管理的 item。 | 已经 `takeItem()` 取出的 item 不再由表格负责。 |
| 尺寸 | `setRowCount(int rows)` / `rowCount() const` | 设置或查询行数。 | 增加行只扩大网格，不会自动创建 item。 |
| 尺寸 | `setColumnCount(int columns)` / `columnCount() const` | 设置或查询列数。 | 删除行列会改变已有 item 的坐标和所有权。 |

### 11.2 Item 和单元格

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 读取 | `item(int row, int column) const` | 取得指定单元格的 item。 | 没有 item 时返回空指针；只观察，不转移所有权。 |
| 写入 | `setItem(int row, int column, QTableWidgetItem *item)` | 把 item 放入指定单元格。 | 所有权转给表格，插入后不要再手动 delete。 |
| 所有权 | `takeItem(int row, int column)` | 从单元格取出 item 并交还所有权。 | 取出后由调用者负责复用或删除。 |
| 拖放 | `items(const QMimeData *data) const` | 从拖放数据解析出 item 列表。 | 只有在自定义拖放流程时才常用。 |
| 索引转换 | `indexFromItem(const QTableWidgetItem *item) const` | 把便捷 item 转成模型索引。 | 适合与继承自 `QTableView` 的接口衔接。 |
| 索引转换 | `itemFromIndex(const QModelIndex &index) const` | 把模型索引转回 `QTableWidgetItem`。 | 索引必须来自该表格的内部模型。 |
| 当前项 | `currentItem() const` | 返回当前焦点 item。 | 没有当前项时返回空指针。 |
| 当前项 | `setCurrentItem(QTableWidgetItem *item)` | 设置当前焦点 item。 | 可选用带 selection command 的重载同步选择状态。 |
| 当前单元格 | `setCurrentCell(int row, int column)` | 按行列设置当前单元格。 | 行列无效时不会产生有效当前项。 |
| 编辑 | `editItem(QTableWidgetItem *item)` | 请求打开某个 item 的编辑器。 | 是否可编辑还受 item flags、delegate 和视图编辑触发器影响。 |
| 持久编辑 | `openPersistentEditor(QTableWidgetItem *item)` / `closePersistentEditor(QTableWidgetItem *item)` | 打开或关闭始终显示的编辑器。 | 大量持久编辑器会显著增加控件数量和布局成本。 |

### 11.3 行列、表头和 widget

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 行表头 | `verticalHeaderItem(int row) const` / `setVerticalHeaderItem(int row, QTableWidgetItem *item)` | 读取或设置某行的复杂表头 item。 | 设置后所有权转给表格。 |
| 列表头 | `horizontalHeaderItem(int column) const` / `setHorizontalHeaderItem(int column, QTableWidgetItem *item)` | 读取或设置某列的复杂表头 item。 | 需要图标、勾选或特殊字体时使用。 |
| 行表头 | `setVerticalHeaderLabels(const QStringList &labels)` | 批量设置行表头文本。 | 只设置标题，不改变行数。 |
| 列表头 | `setHorizontalHeaderLabels(const QStringList &labels)` | 批量设置列表头文本。 | 最常用的简单表头初始化方式。 |
| 单元格控件 | `setCellWidget(int row, int column, QWidget *widget)` | 把真实 QWidget 放进单元格。 | 适合少量按钮、下拉框、输入框；大量使用会变重。 |
| 单元格控件 | `cellWidget(int row, int column) const` | 取出某个单元格里的 widget。 | 没有时返回空指针。 |
| 单元格控件 | `removeCellWidget(int row, int column)` | 移除单元格里的 widget。 | 它只是解除单元格关联，旧 widget 的生命周期要明确。 |
| 行操作 | `insertRow(int row)` / `removeRow(int row)` | 插入或删除整行。 | 现有 item 坐标会变化；删除行会释放仍由表格管理的 item。 |
| 列操作 | `insertColumn(int column)` / `removeColumn(int column)` | 插入或删除整列。 | 同样会影响 item 坐标和所有权。 |

### 11.4 选择、查找和排序

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 区域选择 | `setRangeSelected(const QTableWidgetSelectionRange &range, bool select)` | 选中或取消选中一个矩形范围。 | 最终结果受当前 selection mode 和 item flags 影响。 |
| 区域查询 | `selectedRanges() const` | 返回当前选中的矩形范围列表。 | 多段选择时可能返回多个范围。 |
| Item 查询 | `selectedItems() const` | 返回当前选中的 item 列表。 | 只返回有 item 的单元格，不代表每个选中格都有对象。 |
| 查找 | `findItems(const QString &text, Qt::MatchFlags flags) const` | 按 item 文本和匹配规则搜索。 | 搜索的是 item 的显示文本，不是任意角色数据。 |
| 排序 | `sortItems(int column, Qt::SortOrder order = Qt::AscendingOrder)` | 按指定列对内置 item 排序。 | 比较规则来自 `QTableWidgetItem::operator<()`。 |
| 排序 | `setSortingEnabled(bool enable)` / `isSortingEnabled() const` | 控制用户排序和表格排序状态。 | 批量填充时先关闭，避免插入过程中行自动移动。 |
| Item 信号 | `itemPressed(...)` / `itemClicked(...)` / `itemDoubleClicked(...)` | 按 item 对象报告鼠标交互。 | 没有 item 的空单元格不会提供有效 item。 |
| Cell 信号 | `cellPressed(...)` / `cellClicked(...)` / `cellDoubleClicked(...)` | 按行列坐标报告鼠标交互。 | 需要处理空单元格时，cell 信号更直接。 |
| 修改信号 | `itemChanged(QTableWidgetItem *item)` / `cellChanged(int row, int column)` | item 内容或单元格数据变化时通知。 | 初始化批量填充时可用 `QSignalBlocker` 避免触发业务更新。 |
| 选择信号 | `itemSelectionChanged()` | 选择范围发生变化时通知。 | 适合刷新工具栏按钮和详情面板。 |
| 当前项信号 | `currentItemChanged(...)` / `currentCellChanged(...)` | 当前焦点 item 或坐标变化时通知。 | 和“被选中”不是同一个概念。 |

### 11.5 清空、显示和拖放

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 清空 | `clear()` | 清除 item、表头和选择状态。 | 适合完全重置表格。 |
| 清空 | `clearContents()` | 清除单元格内容但保留表头和行列结构。 | 刷新数据时通常比 `clear()` 更合适。 |
| 定位 | `scrollToItem(const QTableWidgetItem *item, ScrollHint hint = EnsureVisible)` | 把指定 item 滚动到可见区域。 | item 必须仍属于该表格。 |
| 定位 | `visualItemRect(const QTableWidgetItem *item) const` | 返回 item 的可视矩形。 | item 无效或不可见时可能返回空矩形。 |
| 命中测试 | `itemAt(const QPoint &p) const` / `itemAt(int x, int y) const` | 从 viewport 坐标找 item。 | 空单元格或空白区域返回空指针。 |
| 拖放 | `supportedDragActions() const` / `setSupportedDragActions(Qt::DropActions actions)` | 查询或设置拖出时支持的动作。 | 需要启用 Qt drag-and-drop 配置。 |
| 拖放扩展 | `mimeTypes() const` / `mimeData(...) const` / `dropMimeData(...)` / `supportedDropActions() const` | 定义 item 如何编码、解析和接收拖放数据。 | 这是高级拖放接口，重写时要和 `QTableWidgetItem` 类型保持一致。 |

### 11.6 QTableWidgetItem 的常用 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QTableWidgetItem(...)` | 创建承载单元格数据和外观的 item。 | item 不等于真实 QWidget；大多数普通表格只需要 item。 |
| 复制 | `clone() const` | 创建当前 item 的副本。 | 自定义 item 类型时应重写，保证自定义字段也被复制。 |
| 所属关系 | `tableWidget() const` / `row() const` / `column() const` | 查询 item 所属表格和当前坐标。 | item 未插入表格时表格为空、行列通常为 -1。 |
| 选择 | `setSelected(bool select)` / `isSelected() const` | 读取或设置 item 的选中状态。 | 复杂选择优先通过 table 的 selection model 处理。 |
| 标志 | `flags() const` / `setFlags(Qt::ItemFlags flags)` | 控制 item 是否可选、可编辑、可拖拽等。 | 关闭 `ItemIsEditable` 会影响双击编辑。 |
| 文本 | `text() const` / `setText(const QString &text)` | 读取或设置显示文本。 | 最常用的 item 数据入口。 |
| 图标 | `icon() const` / `setIcon(const QIcon &icon)` | 读取或设置装饰图标。 | 图标显示仍受 delegate 和列宽影响。 |
| 提示 | `statusTip()` / `setStatusTip()`、`toolTip()` / `setToolTip()`、`whatsThis()` / `setWhatsThis()` | 设置状态栏、悬停和 What's This 说明。 | 这些值通过不同 Qt item role 保存。 |
| 字体 | `font() const` / `setFont(const QFont &font)` | 设置该 item 的字体。 | 大量单元格设置独立字体会增加数据和绘制成本。 |
| 对齐 | `textAlignment() const` / `setTextAlignment(Qt::Alignment alignment)` | 设置文本在单元格内的对齐方式。 | Qt 6.4 前的 int 重载已不推荐使用。 |
| 背景 | `background() const` / `setBackground(const QBrush &brush)` | 设置单元格背景画刷。 | 传 `NoBrush` 可清除自定义背景。 |
| 前景 | `foreground() const` / `setForeground(const QBrush &brush)` | 设置文本或前景画刷。 | 颜色状态要和主题、选中态协调。 |
| 勾选 | `checkState() const` / `setCheckState(Qt::CheckState state)` | 读取或设置 item 勾选状态。 | 还要确保 flags 包含可勾选能力。 |
| 尺寸 | `sizeHint() const` / `setSizeHint(const QSize &size)` | 读取或设置 item 推荐尺寸。 | 会影响视图的内容适配和行列尺寸计算。 |
| 角色数据 | `data(int role) const` / `setData(int role, const QVariant &value)` | 按 Qt item role 读写任意数据。 | 需要自定义业务数据时优先使用自定义 role。 |
| 排序 | `operator<(const QTableWidgetItem &other) const` | 定义两个 item 的排序比较。 | `sortItems()` 会使用它；自定义 item 必须保证比较规则稳定。 |
| 序列化 | `read(QDataStream &in)` / `write(QDataStream &out) const` | 从数据流读取或写入 item。 | 需要启用 Qt DataStream；自定义字段要自行序列化。 |
| 类型 | `type() const` | 返回 item 类型编号。 | 自定义类型通常从 `UserType` 起步。 |

## 12. 常见误区

### 12.1 把 QTableWidget 当成大数据表

它很方便，但不是高性能大数据模型的最佳选择。数据大、逻辑复杂时，用 `QTableView` + 自定义模型。

### 12.2 setItem 后还自己 delete

不要。表格接管了 item 所有权。`takeItem()` 才是把所有权拿回来。

### 12.3 开了排序再批量填数据

排序会让行在插入过程中移动，导致你原来按行号写入的数据错位。批量填充前先关排序。

### 12.4 混淆 item 和 cell widget

`QTableWidgetItem` 是数据项，`setCellWidget()` 是放真实控件。两者不是一个层级。

---

### 一句话总结

`QTableWidget` 是便捷表格：你直接操作 `QTableWidgetItem`、行列数和单元格 widget，就能快速得到一个可编辑、可排序的表格，但它更适合小中型数据界面，不适合复杂模型场景。
