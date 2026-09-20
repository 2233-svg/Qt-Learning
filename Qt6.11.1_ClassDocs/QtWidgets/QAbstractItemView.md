# QAbstractItemView

> Qt 6.11.1 · Qt Widgets · 来自 `QAbstractItemView`

## 1. 先建立直觉

`QAbstractItemView` 是 Qt 模型/视图体系里“视图端”的共同基类。`QListView`、`QTableView`、`QTreeView` 都靠它处理选择、当前项、滚动、编辑、拖放、委托绘制、键盘导航和用户信号。

它本身通常不直接实例化。你学习它，是为了掌握所有 item view 的共同规则：数据来自 `QAbstractItemModel`，选择由 `QItemSelectionModel` 管，单元格显示和编辑交给 `QAbstractItemDelegate`，视图只负责把这些拼成可交互的界面。

最重要的使用判断：数据量小、结构简单，可以用 `QListWidget`、`QTableWidget`、`QTreeWidget`；数据来自业务模型、数据库、远程分页、需要排序过滤或多视图共享时，应该用 `QAbstractItemView` 的派生视图加 model。

## 2. 类说明

- 头文件：`#include <QAbstractItemView>`
- 模块：`Qt6::Widgets`
- 继承自：`QAbstractScrollArea`
- 直接派生类：`QColumnView`、`QHeaderView`、`QListView`、`QTableView`、`QTreeView`

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

它是抽象类。派生类必须实现 `indexAt()`、`visualRect()`、`scrollTo()`、`moveCursor()`、`setSelection()`、`visualRegionForSelection()` 以及偏移/隐藏判断等几何相关函数。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `setModel()` / `model()` | 绑定或读取数据模型。 |
| `setSelectionModel()` / `selectionModel()` | 绑定或读取选择模型，用于多视图共享选择。 |
| `setRootIndex()` / `rootIndex()` | 只显示模型中的某个子树或子区域。 |
| `currentIndex()` / `setCurrentIndex()` | 当前焦点项，不等同于选中项。 |
| `clearSelection()` / `selectAll()` | 清除或全选。 |
| `selectedIndexes()` | 读取当前选中的模型索引。 |
| `setSelectionMode()` | 单选、多选、连续多选、无选择。 |
| `setSelectionBehavior()` | 按单元格、整行或整列选择。 |
| `setEditTriggers()` / `edit()` | 控制双击、按键、选中点击等何时进入编辑。 |
| `openPersistentEditor()` / `closePersistentEditor()` | 让某个索引的编辑器长期显示。 |
| `setItemDelegate()` | 设置全局绘制/编辑委托。 |
| `setItemDelegateForRow()` / `setItemDelegateForColumn()` | 为特定行列设置委托。 |
| `itemDelegateForIndex()` | 查询最终用于某个索引的委托。 |
| `setIndexWidget()` / `indexWidget()` | 在索引位置嵌入真实 QWidget；少量静态控件可用，大量数据慎用。 |
| `scrollTo()` | 滚动到指定索引。 |
| `scrollToTop()` / `scrollToBottom()` | 滚到开头或末尾。 |
| `indexAt()` / `visualRect()` | 在视口坐标和模型索引之间转换。 |
| `sizeHintForIndex()` / `sizeHintForRow()` / `sizeHintForColumn()` | 查询项目、行、列推荐尺寸。 |
| `setIconSize()` / `iconSize()` | 控制装饰图标大小。 |
| `setTextElideMode()` | 控制文本过长时省略方式。 |
| `setAlternatingRowColors()` | 开启交替行底色。 |
| `setHorizontalScrollMode()` / `setVerticalScrollMode()` | 按项滚动或按像素滚动。 |
| `setTabKeyNavigation()` | Tab 是否在项目间导航。 |
| `keyboardSearch()` / `setKeyboardSearchFlags()` | 用户键入字符时按显示文本定位匹配项。 |
| `setDragEnabled()` / `setDragDropMode()` | 开启拖拽或拖放。 |
| `setDefaultDropAction()` | 设置默认 drop 行为，如复制或移动。 |
| `setDropIndicatorShown()` | 是否显示拖放位置提示。 |
| `setAutoScroll()` / `setAutoScrollMargin()` | 拖拽到边缘时自动滚动。 |
| `setDragDropOverwriteMode()` | drop 到已有项时覆盖还是插入，具体还取决于视图和模型。 |
| `setUpdateThreshold()` | Qt 6.9 起的数据变化更新阈值，影响大范围刷新策略。 |
| `activated()` | 用户“激活”某项，通常是回车或双击语义。 |
| `clicked()` / `doubleClicked()` / `pressed()` | 鼠标交互信号。 |
| `entered()` / `viewportEntered()` | 鼠标悬停到项目或离开项目区域。 |
| `update(index)` / `reset()` | 刷新某项或重置视图状态。 |
| `startDrag()` | 子类化自定义拖拽启动。 |
| `selectionCommand()` | 子类化改变鼠标/键盘事件对应的选择策略。 |
| `initViewItemOption()` | 子类化时初始化委托绘制选项。 |

## 4. 关键用法

### 模型、选择、委托是三条线

`setModel()` 只解决“显示什么”。用户选中了什么，要通过 `selectionModel()` 看；每个项怎么画、怎么编辑，要通过 delegate 控制。把颜色、按钮、编辑器状态都硬塞进 view 子类，短期能跑，长期会让排序、代理模型和多视图共享非常难维护。

当前项和选中项也要分开。`currentIndex()` 是键盘焦点或编辑目标；选择可能为空、一个或多个。很多表格 bug 来自只看 current index，却以为它代表全部选择。

### 编辑不是数据修改本身

`editTriggers` 只决定何时打开编辑器。真正写回数据靠模型的 `setData()` 和 flags 中的 `Qt::ItemIsEditable`。如果双击不能编辑，检查顺序是：模型 index 是否有效、模型 flags 是否可编辑、视图 edit trigger 是否允许、delegate 是否能创建 editor。

持久编辑器适合少量开关、进度、状态控件。大量使用 `openPersistentEditor()` 会创建很多 QWidget，性能和滚动体验会下降；这种场景通常应该写 delegate 绘制。

### `setIndexWidget()` 是方便工具，不是高性能单元格方案

`setIndexWidget()` 可以把一个按钮、进度条或小控件放进某个 index，但它绕开了 delegate 的轻量绘制模型。几十个静态控件可以接受，成百上千行的表格应使用 delegate，否则内存、布局和滚动都会变重。

### 拖放需要模型配合

视图属性只能打开交互入口；能拖出什么、能放到哪里、放下后如何改数据，要看模型实现的 `mimeData()`、`dropMimeData()`、`supportedDropActions()` 和 flags。只设置 `setDragDropMode(InternalMove)` 而模型不支持移动，界面会看似允许但数据不会正确改变。

### 继承时先尊重 viewport 坐标

`QAbstractItemView` 继承自 `QAbstractScrollArea`，鼠标位置、绘制区域、`indexAt()`、`visualRect()` 主要都以 viewport 为参照。自定义视图时，滚动偏移、dirty region、visual region 必须一致，否则会出现点击命中和绘制位置不一致的诡异问题。

## 5. 常见坑与经验

- `QModelIndex` 不是长期稳定句柄；模型 reset、删除行、排序过滤后，旧 index 可能失效。需要长期引用时看 `QPersistentModelIndex`。
- 排序过滤一般放在 `QSortFilterProxyModel`，不要在 view 里手动重排显示。
- `reset()` 是视图状态重置，不是让模型丢数据；模型重大变化应由模型发出正确信号。
- 大范围 `dataChanged()` 会触发大量可见性判断；Qt 6.9 的 `updateThreshold` 可用于调节刷新策略。
- 所有模型通知都应在 GUI 线程与视图配合。后台线程可以准备数据，但不要直接改已绑定到视图的模型内部结构。
