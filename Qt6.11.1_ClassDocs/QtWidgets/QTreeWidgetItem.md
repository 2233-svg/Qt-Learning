# QTreeWidgetItem

> Qt 6.11.1 · Qt Widgets · 来自 `QTreeWidgetItem`

## 1. 先建立直觉

`QTreeWidgetItem` 是 `QTreeWidget` 里的一个树节点。它不是 QWidget，也不是 QObject；它保存多列文本、图标、勾选状态、字体、颜色、提示、自定义数据，以及一组子节点。

它适合中小规模树形 UI：分类、权限、项目导航、简单对象层级。真正的大树、懒加载树或业务对象树，应该考虑 `QTreeView` + 自定义模型。

最关键的心智模型是所有权：节点插入 `QTreeWidget` 或另一个 `QTreeWidgetItem` 后，由它的父节点/树控件管理；用 `takeChild()`、`takeChildren()` 或 `takeTopLevelItem()` 取出后，调用者重新获得所有权。

## 2. 类说明

- 头文件：`#include <QTreeWidgetItem>`
- 模块：`Qt6::Widgets`
- 继承自：无
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

它与 `QTreeWidget` 配套使用，通过 item API 映射到底层模型。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QTreeWidgetItem(type)` | 创建未插入的节点。 |
| `QTreeWidgetItem(parentTree, type)` | 创建并作为顶层节点加入树。 |
| `QTreeWidgetItem(parentItem, type)` | 创建并加入父节点。 |
| `QTreeWidgetItem(strings, type)` | 创建多列文本节点。 |
| `QTreeWidgetItem(parent, preceding, type)` | 插入到指定兄弟节点之后。 |
| `QTreeWidgetItem(other)` / `operator=()` | 复制节点数据；不会复制所属树。 |
| `clone()` | 复制节点，子类保留自定义数据时应重写。 |
| `type()` | 节点类型，自定义类型从 `UserType` 起。 |
| `treeWidget()` | 返回所属树控件，未插入时为空。 |
| `parent()` | 返回父节点，顶层节点为空。 |
| `addChild()` / `addChildren()` | 追加子节点。 |
| `insertChild()` / `insertChildren()` | 在指定位置插入子节点。 |
| `takeChild()` / `takeChildren()` | 移除并返回子节点，调用者接手所有权。 |
| `removeChild()` | 从子列表移除节点。 |
| `child(index)` / `childCount()` / `indexOfChild()` | 访问和定位子节点。 |
| `columnCount()` | 节点可用列数。 |
| `text(column)` / `setText()` | 指定列文本。 |
| `icon(column)` / `setIcon()` | 指定列图标。 |
| `data(column, role)` / `setData()` | 指定列和角色的数据。 |
| `checkState(column)` / `setCheckState()` | 指定列勾选状态。 |
| `flags()` / `setFlags()` | 控制可选、可编辑、可勾选、拖放等能力。 |
| `font()` / `setFont()` | 指定列字体。 |
| `foreground()` / `setForeground()` | 指定列前景画刷。 |
| `background()` / `setBackground()` | 指定列背景画刷。 |
| `sizeHint()` / `setSizeHint()` | 指定列推荐尺寸。 |
| `textAlignment()` / `setTextAlignment()` | 指定列文本对齐；`setTextAlignment` 自 Qt 6.4 起可用。 |
| `toolTip()` / `setToolTip()` | 指定列鼠标提示。 |
| `statusTip()` / `setStatusTip()` | 指定列状态栏提示。 |
| `whatsThis()` / `setWhatsThis()` | 指定列 What's This 帮助。 |
| `isExpanded()` / `setExpanded()` | 展开或折叠节点。 |
| `isHidden()` / `setHidden()` | 隐藏或显示节点。 |
| `isDisabled()` / `setDisabled()` | 禁用或启用节点。 |
| `isSelected()` / `setSelected()` | 查询或设置选中状态。 |
| `isFirstColumnSpanned()` / `setFirstColumnSpanned()` | 第一列是否横跨整行。 |
| `childIndicatorPolicy()` / `setChildIndicatorPolicy()` | 控制是否显示展开指示器。 |
| `sortChildren(column, order)` | 对直接子节点按列排序。 |
| `read()` / `write()` | 用 `QDataStream` 序列化。 |
| `operator<()` | 排序比较逻辑，子类可重写。 |
| `emitDataChanged()` | 子类内部数据变化后通知视图刷新。 |

## 4. 关键用法

### 多列数据按 column 分开存

每一列都有自己的文本、图标、字体、颜色、提示和 role 数据。不要把所有信息拼到第一列里；例如文件树可以第 0 列放名称，第 1 列放大小，第 2 列放修改时间，同时在 `UserRole` 保存完整路径。

### 子节点所有权要清楚

`addChild()` 后父节点负责销毁 child。`takeChild()` 会把 child 从树中移除并返回，之后你需要 delete 或重新插入。`removeChild()` 只是移除关系，实际所有权处理要格外小心；实际项目里更常用 `takeChild()`，因为语义更明确。

### 勾选树要防递归信号

权限树经常需要父节点半选、子节点全选联动。实现时通常响应 `itemChanged()`，更新子孙和祖先状态。程序更新状态也会再次触发 `itemChanged()`，所以需要 `QSignalBlocker` 或内部标志位防止递归。

`Qt::PartiallyChecked` 只是状态，不会自动计算。你要自己根据子节点状态维护父节点。

### 懒加载提示

`setChildIndicatorPolicy(ShowIndicator)` 可以在尚未真正加载子节点时显示展开箭头。用户展开时再插入真实子节点，是便捷树里模拟懒加载的常见方法。数据特别大时，自定义 model 仍然更稳。

### 排序比较

`sortChildren()` 和 `QTreeWidget::sortItems()` 会使用 item 的 `operator<()`。数字、日期、版本号等不要依赖字符串默认比较；把原始值放在 role 中并重写比较逻辑，排序才会符合用户直觉。

## 5. 常见坑与经验

- 顶层节点的 `parent()` 为空，但它仍属于 `QTreeWidget`。
- `setExpanded()` 只有节点已经在树中时才有可视意义。
- `columnCount()` 可能受节点文本列表和树列数共同影响，访问列前确认树的列数。
- 复制节点不会复制它所属的树控件。
- 大量真实 QWidget 不应放到节点上；用 item 数据和 delegate 更轻。
