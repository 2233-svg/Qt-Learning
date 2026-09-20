# QTreeView

> Qt 6.11.1 · Qt Widgets · 来自 `QTreeView`

## 1. 先建立直觉

`QTreeView` 用层级模型展示父子结构：文件树、项目导航、对象检查器、分类目录、组织架构、带多列属性的节点列表都属于它的地盘。它不是把缩进画出来的 `QTableView`，而是围绕 `QModelIndex` 的 parent/child 关系工作。

它可以显示多列。第一列通常承载展开箭头和树结构，其他列显示同一节点的属性。`treePosition`、`rootIsDecorated`、`indentation` 和 header 设置决定树看起来是“目录树”还是“层级表格”。

小型手工节点可以用 `QTreeWidget`；数据来自真实业务对象、文件系统、数据库、懒加载或代理模型时，使用 `QTreeView` 加自定义 model 更可靠。

## 2. 类说明

- 头文件：`#include <QTreeView>`
- 模块：`Qt6::Widgets`
- 继承自：`QAbstractItemView`
- 直接派生类：`QTreeWidget`，以及 Qt Help 中的内容控件

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

它继承 item view 的选择、编辑、委托和拖放机制；本类新增的重点是展开折叠、缩进、树枝绘制、层级导航和树表头。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QTreeView(parent)` | 创建树视图。 |
| `setModel()` | 绑定层级模型。 |
| `expand()` / `collapse()` | 展开或折叠指定节点。 |
| `setExpanded()` / `isExpanded()` | 设置或查询节点展开状态。 |
| `expandAll()` / `collapseAll()` | 展开或折叠整棵可见树。 |
| `expandRecursively(index, depth)` | 从某节点开始递归展开，可限制深度。 |
| `expandToDepth(depth)` | 展开到指定层级。 |
| `expanded(index)` / `collapsed(index)` | 节点展开状态变化信号。 |
| `indexAbove()` / `indexBelow()` | 获取视觉上相邻的上一项或下一项。 |
| `setIndentation()` / `indentation()` | 设置层级缩进宽度。 |
| `resetIndentation()` | 恢复默认缩进。 |
| `setRootIsDecorated()` / `rootIsDecorated()` | 根层节点是否显示展开装饰。 |
| `setItemsExpandable()` / `itemsExpandable()` | 用户是否可以展开有子节点的项目。 |
| `setExpandsOnDoubleClick()` / `expandsOnDoubleClick()` | 双击是否展开折叠。 |
| `setAnimated()` / `isAnimated()` | 展开折叠是否带动画。 |
| `setAutoExpandDelay()` / `autoExpandDelay()` | 拖放悬停时自动展开的延迟。 |
| `setUniformRowHeights()` / `uniformRowHeights()` | 告诉视图每行高度一致，提高大树性能。 |
| `setHeaderHidden()` / `isHeaderHidden()` | 隐藏或显示表头。 |
| `header()` / `setHeader()` | 获取或替换 `QHeaderView`。 |
| `setColumnWidth()` / `columnWidth()` | 设置或读取列宽。 |
| `hideColumn()` / `showColumn()` | 隐藏或显示列。 |
| `setColumnHidden()` / `isColumnHidden()` | 程序化控制列隐藏。 |
| `resizeColumnToContents()` | 按内容调整列宽。 |
| `setSortingEnabled()` / `sortByColumn()` | 开启或执行按列排序。 |
| `setAllColumnsShowFocus()` | 焦点高亮是否覆盖整行所有列。 |
| `setFirstColumnSpanned()` / `isFirstColumnSpanned()` | 某行第一列是否横跨所有列，常用于分组标题。 |
| `setTreePosition()` / `treePosition()` | 指定哪一列显示树结构。 |
| `setRowHidden()` / `isRowHidden()` | 隐藏指定父节点下的子行。 |
| `setWordWrap()` / `wordWrap()` | 节点文本是否换行。 |
| `drawBranches()` / `drawRow()` | 子类化自定义树枝或整行绘制。 |
| `rowHeight()` / `indexRowSizeHint()` | 查询行高相关信息。 |

## 4. 关键用法

### 树的根可以移动

`setRootIndex()` 可以让视图只显示某个节点之下的子树，非常适合文件浏览器进入某个目录、项目面板只看一个模块、或权限限制下隐藏上层结构。它不会改变模型，只改变视图观察模型的位置。

如果你需要面包屑、返回上级、当前目录这些概念，通常组合 `rootIndex()`、模型的 `parent()` 和外部导航状态，而不是重新构建模型。

### 展开状态不是模型数据

`expand()`、`collapse()`、`isExpanded()` 管的是视图状态。模型 reset、代理过滤、根索引改变后，展开状态可能丢失或不再对应同一节点。需要记忆展开状态时，用业务 id 或 `QPersistentModelIndex` 谨慎保存，再在模型稳定后恢复。

`expandAll()` 对大树和懒加载模型很危险。它可能触发大量 `rowCount()`、`fetchMore()` 和布局计算。更友好的方式是 `expandToDepth()` 或对用户展开的路径逐步加载。

### 多列树要设计焦点和表头

树结构默认在第一列，但 `setTreePosition()` 可以改变。属性检查器常把第一列作为属性名、第二列作为值；文件树可能第一列是名称，后面是大小、修改时间。是否显示 header、焦点是否跨所有列，都会影响它像“导航树”还是“树形表格”。

`setFirstColumnSpanned()` 可做分组行，但它只影响显示。排序、选择和数据访问仍然按模型索引工作。

### 性能来自稳定的行高和懒加载

如果每一行高度一致，`setUniformRowHeights(true)` 对大树非常有价值。文件系统树、对象树通常可以打开；含多行文本、不同大小图标或自定义高度 delegate 时不要撒谎。

层级数据很大时，应让 model 实现 `canFetchMore()` / `fetchMore()` 懒加载。视图负责在展开时询问模型，模型负责按需补数据。

## 5. 常见坑与经验

- `setRowHidden(row, parent, true)` 的 row 是某个 parent 下的子行，不是全局行号。
- `indexAbove()` 和 `indexBelow()` 按当前视觉展开状态走，不等同于模型里的前后兄弟。
- `sortingEnabled` 会通过模型或代理模型排序；树排序要考虑每个父节点下的子节点分别排序。
- 自定义 `drawBranches()` 时要保留平台 style 的基本语义，否则展开箭头、hover、RTL 布局可能不自然。
- 大树不要随手 `expandAll()`；用户体验和性能都通常更差。
