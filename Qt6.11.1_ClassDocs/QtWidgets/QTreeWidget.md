# QTreeWidget

> Qt 6.11.1 · Qt Widgets · 来自 `QTreeWidget`

## 1. 先建立直觉

`QTreeWidget` 是 `QTreeView` 的便捷版本：它内置 item-based 模型，让你直接用 `QTreeWidgetItem` 搭层级节点。它适合设置树、分类树、简单导航、权限勾选树、对象层级检查器等中小规模场景。

它的好处是不用写 model；代价是节点数据和界面绑得比较近。数据来自真实对象树、文件系统、数据库、远程懒加载，或者需要多个视图共享时，应使用 `QTreeView` + 自定义模型。

最重要的直觉是：顶层节点挂在 `QTreeWidget` 上，子节点挂在 `QTreeWidgetItem` 上；`invisibleRootItem()` 是所有顶层节点的隐藏父节点，很多统一遍历和批量插入都可以从它开始。

## 2. 类说明

- 头文件：`#include <QTreeWidget>`
- 模块：`Qt6::Widgets`
- 继承自：`QTreeView`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

它继承 `QTreeView` 的展开折叠、表头、选择、排序、拖放和 delegate 能力，同时提供基于 `QTreeWidgetItem` 的节点 API。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QTreeWidget(parent)` | 创建树控件。 |
| `setColumnCount()` / `columnCount()` | 设置或读取列数。 |
| `addTopLevelItem()` / `addTopLevelItems()` | 添加顶层节点。 |
| `insertTopLevelItem()` / `insertTopLevelItems()` | 在指定位置插入顶层节点。 |
| `takeTopLevelItem()` | 移除并返回顶层节点，调用者获得所有权。 |
| `topLevelItem()` / `topLevelItemCount()` | 访问顶层节点和数量。 |
| `indexOfTopLevelItem()` | 查询顶层节点位置。 |
| `invisibleRootItem()` | 获取隐藏根节点，便于统一处理整棵树。 |
| `headerItem()` / `setHeaderItem()` | 读取或设置表头 item。 |
| `setHeaderLabel()` / `setHeaderLabels()` | 设置单列表头或多列表头文字。 |
| `currentItem()` / `currentColumn()` | 当前节点和列。 |
| `setCurrentItem()` | 设置当前节点，可指定列和选择命令。 |
| `selectedItems()` | 获取选中节点。 |
| `findItems(text, flags, column)` | 在指定列查找节点。 |
| `itemAt(point)` | 根据视口坐标找节点。 |
| `itemAbove()` / `itemBelow()` | 获取视觉上相邻节点。 |
| `visualItemRect()` | 获取节点可视矩形。 |
| `expandItem()` / `collapseItem()` | 展开或折叠指定节点。 |
| `scrollToItem()` | 滚动到指定节点。 |
| `editItem()` | 让节点某列进入编辑。 |
| `openPersistentEditor()` / `closePersistentEditor()` | 长期开启或关闭节点某列编辑器。 |
| `setItemWidget()` / `itemWidget()` | 在节点某列放真实 QWidget；少量使用。 |
| `removeItemWidget()` | 移除节点控件。 |
| `sortItems(column, order)` / `sortColumn()` | 按列排序或读取当前排序列。 |
| `indexFromItem()` / `itemFromIndex()` | 与模型索引互转。 |
| `setSupportedDragActions()` / `supportedDragActions()` | Qt 6.10 起设置可发起的拖拽动作。 |
| `clear()` | 清空并删除所有节点。 |
| `mimeData()` / `dropMimeData()` | 子类化自定义拖放数据。 |
| `currentItemChanged()` | 当前节点变化。 |
| `itemClicked()` / `itemDoubleClicked()` / `itemActivated()` | 用户操作节点。 |
| `itemExpanded()` / `itemCollapsed()` | 节点展开折叠。 |
| `itemChanged()` | 节点数据变化。 |
| `itemSelectionChanged()` | 选择集合变化。 |

## 4. 关键用法

### 建树：列数和表头先定下来

多列树应先 `setColumnCount()` 和 `setHeaderLabels()`，再创建节点并为各列设置文本、图标、勾选状态或用户数据。后续增加列当然可以，但早定结构能避免大量节点缺列或表头错位。

顶层节点由 `QTreeWidget` 接管所有权，子节点由父 `QTreeWidgetItem` 接管。`clear()` 会删除整棵树；`takeTopLevelItem()` 只取走顶层节点及其子树，之后需要你自己管理。

### `invisibleRootItem()` 是统一遍历入口

当你要递归遍历所有节点、批量设置勾选状态、导出树结构时，从 `invisibleRootItem()` 开始可以把顶层节点和普通子节点统一处理。它不会显示在界面上，但行为上像所有顶层节点的父节点。

### 多列节点：信号里的 column 很重要

`itemClicked(item, column)`、`itemChanged(item, column)` 会告诉你用户操作的是哪一列。权限树常常第一列是名称，第二列是读权限，第三列是写权限；如果忽略 column，很容易把用户在某一列的勾选误处理成整行状态。

### 排序会改变同级节点顺序

`sortItems()` 对树中同一父节点下的子项排序，而不是把整棵树拉平成列表排序。排序后不要继续保存旧的 child index；要通过 item 指针、业务 id 或重新查找定位。

### item widget 和持久编辑器要克制

树节点上可以放 QWidget，也可以打开持久编辑器，但大树里大量真实控件会拖慢滚动和展开。勾选框、图标、文本、颜色通常直接用 `QTreeWidgetItem` 数据角色就够了。

## 5. 常见坑与经验

- `takeTopLevelItem()` 只适用于顶层节点；子节点要用 `QTreeWidgetItem` 自己的 child API。
- `selectedItems()` 返回节点，不包含列信息；需要列级选择时结合 current column 或底层 selection model。
- `itemChanged()` 对程序修改也会触发，做父子勾选联动时要防递归。
- `findItems()` 默认只查指定列，不会自动查所有列。
- 大型或懒加载树不要用 `QTreeWidget` 硬撑，自定义模型更清晰。
