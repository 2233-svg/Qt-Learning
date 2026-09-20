# Qt QListWidget 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）
> 头文件：`#include <QListWidget>`
> 所属模块：`Qt6::Widgets`
> 继承：`QListView -> QListWidget`
> 常见搭档：`QListWidgetItem`、`QItemSelectionModel`、`QModelIndex`

## 1. QListWidget 解决什么问题

`QListWidget` 是“开箱即用”的列表控件。它把 `QListView` 的模型/视图机制包装成更容易上手的 item-based 接口，让你可以直接操作 `QListWidgetItem`，而不用先单独搭一个模型类。

它适合放在：

- 设置面板里的简单条目列表；
- 通讯录、文件夹、收藏夹类的小型列表；
- 需要快速原型验证的列表界面；
- 以 item 为单位增删改查的界面。

它的核心价值是“省事”，不是“最强”。如果你的数据来源复杂、需要自定义模型层、或者希望把业务数据和视图彻底分离，应该回到 `QListView + QAbstractListModel` 那套更标准的模型/视图方案。

你可以先把它理解成：

```text
QListView
  └─ QListWidget
       └─ 内部维护一个 item 模型
```

## 2. 最小可用代码

### 2.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

### 2.2 一个最简单的列表

```cpp
#include <QApplication>
#include <QListWidget>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QListWidget list;
    list.addItem("Apple");
    list.addItem("Banana");
    list.addItem("Cherry");
    list.show();

    return app.exec();
}
```

### 2.3 用 item 承载更完整的信息

```cpp
auto *item = new QListWidgetItem(QIcon(":/icons/user.png"), "Alice");
item->setData(Qt::UserRole, 42);
list->addItem(item);
```

`QListWidgetItem` 不只是文字，它还能带图标、角色数据、勾选状态、排序信息等。

## 3. QListWidget 的真正使用模型

### 3.1 item 才是列表的中心

和 `QListView` 直接操作模型不同，`QListWidget` 直接围绕 item 工作。常见操作都是：

- `addItem()`：追加；
- `insertItem()`：插入；
- `takeItem()`：取走；
- `currentItem()` / `setCurrentItem()`：当前项；
- `selectedItems()`：当前选中项。

### 3.2 所有权很重要

```cpp
auto *item = new QListWidgetItem("Temp");
list->addItem(item);   // QListWidget 接管 item
```

一旦 item 被加入列表，列表就会管理它的生命周期。反过来，`takeItem()` 会把 item 从列表中移除，并把所有权还给调用方。

这点是写动态列表时最容易出错的地方。

### 3.3 item widget 不是普通 item

```cpp
list->setItemWidget(item, new QPushButton("Action"));
```

`setItemWidget()` 是把真正的 `QWidget` 嵌到某个 item 上。它适合少量特殊条目，但不适合把整张列表都做成复杂控件树。数量一多，性能和维护都会变差。

## 4. 常用操作怎么理解

### 4.1 增删改查

```cpp
list->addItem("One");
list->insertItem(0, "Zero");
QListWidgetItem *item = list->item(0);
int row = list->row(item);
QListWidgetItem *taken = list->takeItem(0);
```

`item(row)` 和 `row(item)` 是成对使用的：一个由行找项，一个由项找行。

### 4.2 当前项和选择

```cpp
list->setCurrentRow(1);
list->setCurrentItem(item);
auto current = list->currentItem();
auto selected = list->selectedItems();
```

当前项不等于全部选中项。单选模式下两者接近，多选模式下差别就会明显。

### 4.3 排序

```cpp
list->setSortingEnabled(true);
list->sortItems(Qt::AscendingOrder);
```

开启排序后，插入顺序不再等于显示顺序。这个时候要避免在业务层死记“第几个插入的就一定显示在第几个”。

### 4.4 拖放和持久编辑器

`QListWidget` 直接继承自视图类，所以拖放、编辑器和索引映射这些功能都在：

- `openPersistentEditor()`
- `closePersistentEditor()`
- `isPersistentEditorOpen()`
- `setSupportedDragActions()`

这些 API 说明它不仅仅是“静态列表”，也能做可编辑、可拖拽的列表。

## 5. 适合用 QListWidget 的场景

- 条目数量不大；
- 数据结构简单；
- 需要快速开发；
- 需要 item 级别的视觉定制，但不想先设计完整模型。

如果你已经开始频繁使用 `Qt::UserRole` 存业务对象 ID，或者需要跨多个视图复用数据，通常就该考虑切换到模型/视图方案了。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QListWidget(QWidget *parent = nullptr)` | 创建一个空列表控件。 | 最常见的初始化方式。 |
| 析构 | `~QListWidget()` | 销毁列表控件。 | QWidget 父子对象规则负责生命周期。 |
| 属性 | `count : int` | 当前列表项数量。 | 只读，随增删项变化。 |
| 属性 | `currentRow : int` | 当前选中项的行号。 | 和 `currentItem()` 配合看。 |
| 属性 | `sortingEnabled : bool` | 是否启用自动排序。 | 开启后插入顺序不一定等于显示顺序。 |
| 属性 | `supportedDragActions : Qt::DropActions` | 支持的拖拽动作集合。 | Qt 6.10 起可用。 |
| 修改 | `addItem(QListWidgetItem *item)` | 追加一个 item。 | 加入后通常由列表接管所有权。 |
| 修改 | `addItem(const QString &label)` | 追加一个纯文本条目。 | 适合快速构建简单列表。 |
| 修改 | `addItems(const QStringList &labels)` | 一次追加多个条目。 | 适合批量导入。 |
| 修改 | `insertItem(int row, QListWidgetItem *item)` | 在指定行插入 item。 | 行号越界时要看 Qt 的插入规则。 |
| 修改 | `insertItem(int row, const QString &label)` | 在指定行插入文本项。 | 适合按位置构建列表。 |
| 修改 | `insertItems(int row, const QStringList &labels)` | 从指定行批量插入。 | 适合导入数组。 |
| 修改 | `takeItem(int row)` | 从列表取出 item。 | 取出后所有权回到调用方。 |
| 查询 | `item(int row) const` | 按行取 item。 | 无效行返回空指针。 |
| 查询 | `row(const QListWidgetItem *item) const` | 按 item 查行号。 | 找不到时返回 `-1`。 |
| 查询 | `count() const` | 返回当前条目数。 | 和 `model()->rowCount()` 近似对应。 |
| 查询 | `currentItem() const` | 返回当前项。 | 为空时要判空。 |
| 修改 | `setCurrentItem(QListWidgetItem *item)` | 设置当前项。 | item 必须属于当前列表。 |
| 修改 | `setCurrentItem(QListWidgetItem *item, QItemSelectionModel::SelectionFlags command)` | 带选择命令设置当前项。 | 适合更细的选择控制。 |
| 查询 | `currentRow() const` | 返回当前行号。 | 常和 `currentRowChanged` 联动。 |
| 修改 | `setCurrentRow(int row)` | 设置当前行。 | 常用于程序化切换。 |
| 修改 | `setCurrentRow(int row, QItemSelectionModel::SelectionFlags command)` | 带选择命令设置当前行。 | 更细粒度地控制选择状态。 |
| 查询 | `itemAt(const QPoint &p) const` | 按视图坐标找 item。 | 用于鼠标命中测试。 |
| 查询 | `itemAt(int x, int y) const` | 按坐标找 item。 | `itemAt(QPoint)` 的便捷重载。 |
| 查询 | `visualItemRect(const QListWidgetItem *item) const` | 返回 item 的可视矩形。 | 做自定义定位时常用。 |
| 修改 | `sortItems(Qt::SortOrder order = Qt::AscendingOrder)` | 按顺序排序条目。 | 排序后行号会重排。 |
| 修改 | `setSortingEnabled(bool enable)` | 开关自动排序。 | 和 `sortItems()` 配合。 |
| 查询 | `isSortingEnabled() const` | 查询是否启用自动排序。 | 只反映当前设置。 |
| 修改 | `editItem(QListWidgetItem *item)` | 启动 item 编辑。 | 依赖编辑模式和 delegate。 |
| 修改 | `openPersistentEditor(QListWidgetItem *item)` | 打开持久编辑器。 | 适合少量需要常驻编辑的 item。 |
| 修改 | `closePersistentEditor(QListWidgetItem *item)` | 关闭持久编辑器。 | 与上一个函数配对。 |
| 查询 | `isPersistentEditorOpen(QListWidgetItem *item) const` | 查询编辑器是否打开。 | 常用于状态检查。 |
| 查询 | `itemWidget(QListWidgetItem *item) const` | 返回 item 上绑定的 widget。 | 只在 `setItemWidget()` 后有意义。 |
| 修改 | `setItemWidget(QListWidgetItem *item, QWidget *widget)` | 给某个 item 绑定 widget。 | 适合少量特殊条目。 |
| 修改 | `removeItemWidget(QListWidgetItem *item)` | 移除 item 绑定的 widget。 | 只是解绑，不等于删 item。 |
| 查询 | `selectedItems() const` | 返回当前所有选中项。 | 多选模式最常用。 |
| 查询 | `findItems(const QString &text, Qt::MatchFlags flags) const` | 按文本匹配查找 item。 | 可做搜索定位。 |
| 查询 | `items(const QMimeData *data) const` | 从拖放数据解析 item。 | 和拖放格式相关。 |
| 查询 | `indexFromItem(const QListWidgetItem *item) const` | item 转 QModelIndex。 | 和模型/视图接口打通时常用。 |
| 查询 | `itemFromIndex(const QModelIndex &index) const` | QModelIndex 转 item。 | 反向映射。 |
| 槽 | `scrollToItem(const QListWidgetItem *item, QAbstractItemView::ScrollHint hint = EnsureVisible)` | 滚动到指定 item。 | 做定位跳转时很实用。 |
| 槽 | `clear()` | 清空列表。 | 会移除所有条目。 |
| 信号 | `currentItemChanged(QListWidgetItem *current, QListWidgetItem *previous)` | 当前项变化。 | 做详情面板联动。 |
| 信号 | `currentRowChanged(int currentRow)` | 当前行变化。 | 简单联动很方便。 |
| 信号 | `currentTextChanged(const QString &currentText)` | 当前文本变化。 | 适合状态栏或预览。 |
| 信号 | `itemActivated(QListWidgetItem *item)` | 条目被激活。 | 双击或回车触发。 |
| 信号 | `itemChanged(QListWidgetItem *item)` | 条目内容变化。 | 适合同步业务数据。 |
| 信号 | `itemClicked(QListWidgetItem *item)` | 条目被点击。 | 最基础的交互信号。 |
| 信号 | `itemDoubleClicked(QListWidgetItem *item)` | 条目被双击。 | 常用于打开详情。 |
| 信号 | `itemEntered(QListWidgetItem *item)` | 鼠标进入条目。 | 需要鼠标跟踪时才明显。 |
| 信号 | `itemPressed(QListWidgetItem *item)` | 条目被按下。 | 早于 clicked。 |
| 信号 | `itemSelectionChanged()` | 选择集合变化。 | 比当前项更通用。 |
| 受保护函数 | `event(QEvent *e)` | 处理通用事件。 | 影响视图级行为。 |
| 受保护函数 | `mimeTypes() const` | 返回支持的拖放 MIME 类型。 | 做拖放时要和 `mimeData()` 对称。 |
| 受保护函数 | `mimeData(const QList<QListWidgetItem *> &items) const` | 把 item 序列打包成拖放数据。 | 自定义拖放时常重写。 |
| 受保护函数 | `dropMimeData(int index, const QMimeData *data, Qt::DropAction action)` | 接收拖放数据。 | 控制拖放插入方式。 |
| 受保护函数 | `supportedDropActions() const` | 返回允许的拖放动作。 | 控制能拖进来什么。 |
| 受保护函数 | `dropEvent(QDropEvent *event)` | 处理放下事件。 | 拖放流程入口。 |
| 受保护函数 | `setModel(QAbstractItemModel *model)` | 替换内部模型。 | 很少直接调用；通常说明你开始走更底层方案。 |

### 一句话总结

`QListWidget` 是 item 直控型列表控件，适合简单列表和快速开发；它省去模型编写，但也把你绑得更近视图层。
