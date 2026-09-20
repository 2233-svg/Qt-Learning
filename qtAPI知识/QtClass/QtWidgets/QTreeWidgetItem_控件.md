# QTreeWidgetItem：QTreeWidget 的树节点数据项

> Qt 6.11.1 · `#include <QTreeWidgetItem>` · 模块：`Qt6::Widgets`

`QTreeWidgetItem` 是 `QTreeWidget` 的 convenience item。它表示树中的一行，可有多列数据、图标、勾选状态、字体、前景/背景、tooltip、子节点和排序行为。

## 使用场景

适合层级数据规模适中、直接操作节点对象最方便的界面，例如设置页、资源树、小型分类树。若数据量大、来自业务模型、需要懒加载或多视图共享，应使用 `QTreeView + QAbstractItemModel`。

构造时可指定 `QTreeWidget` 作为顶层父对象，或指定另一个 `QTreeWidgetItem` 作为子节点父对象。树/父节点会管理 item 生命周期；`takeChild()`、`takeChildren()`、`takeTopLevelItem()` 会把所有权取回。

## 数据、状态和排序

每列都有独立角色数据，便捷函数映射到标准 roles。默认 flags 使 item 可选、可勾选、启用、可拖、可放。`operator<()` 决定排序；自定义子类应使用 `UserType` 及以上 type，必要时重写 `clone()` 和排序。

`setHidden()`、`setExpanded()`、`setSelected()` 等状态通常只有 item 已放入 `QTreeWidget` 后才有实际 UI 效果。

## API 速查表

| API | 语义与边界 |
|---|---|
| 多组构造函数 | 可创建未插入 item、顶层 item、子 item，或插入到指定 preceding 后。 |
| `clone() const` | 克隆节点；自定义 item 应重写以保留派生类型。 |
| `treeWidget() const` | 返回所属树；未插入时为 `nullptr`。 |
| `parent() const` / `child(index)` / `childCount()` | 访问父子关系。 |
| `addChild/insertChild/removeChild/takeChild` | 管理子节点；take 会转移所有权。 |
| `addChildren/insertChildren/takeChildren` | 批量管理子节点。 |
| `text/icon/font/background/foreground/checkState` | 按列访问标准 role 数据。 |
| `data(column, role)` / `setData(column, role, value)` | 通用角色数据接口。 |
| `flags()` / `setFlags()` | 控制可选、可编辑、可勾选、可拖放等。 |
| `setHidden/setExpanded/setSelected` | 控制 UI 状态；通常需已在树中。 |
| `setFirstColumnSpanned(bool)` | 第一列跨越所有列，常用于分组标题。 |
| `ChildIndicatorPolicy` | 控制是否显示展开指示器。 |
| `sortChildren(column, order)` | 对直接子项排序。 |
| `operator<` | 树排序比较函数。 |
| `type() const` | 返回 item 类型；自定义类型使用 `UserType` 及以上。 |
| `emitDataChanged()` | 受保护函数；派生类变更数据后通知视图。 |
