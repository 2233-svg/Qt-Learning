# QTableWidgetItem：QTableWidget 单元格的数据项

> Qt 6.11.1 · `#include <QTableWidgetItem>` · 模块：`Qt6::Widgets`

`QTableWidgetItem` 是 `QTableWidget` 的 convenience item。它用角色数据保存一个单元格的文本、图标、字体、颜色、勾选状态、提示、尺寸建议和自定义数据，并由 `QTableWidget` 内部模型展示。

## 使用场景

适合行列规模不大、数据结构简单、希望直接操作单元格对象的表格。复杂数据、大量行、虚拟加载或需要多个视图共享数据时，应使用 `QTableView + QAbstractItemModel`。

把 item 传给 `QTableWidget::setItem()` 后，表格接管所有权；`takeItem()` 会把所有权取回。复制或赋值 item 时，`type()` 和所属 `tableWidget()` 不会按普通数据一起复制。

## 数据和排序

便捷 setter 都映射到 Qt item roles：`setText()` 是 `DisplayRole`，`setIcon()` 是 `DecorationRole`，`setCheckState()` 是 `CheckStateRole`。自定义角色用 `setData(role, value)`。

排序使用虚函数 `operator<()`。自定义 item 类型应使用 `UserType` 及以上 type，并在需要时重写 `clone()` 和 `operator<()`。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QTableWidgetItem(type)` / `(text, type)` / `(icon, text, type)` | 构造单元格 item；未放入表格前无 row/column。 |
| `clone() const` | 返回副本；自定义 item 应重写。 |
| `tableWidget() const` | 返回所属表格；未插入时为 `nullptr`。 |
| `row() const` / `column() const` | 返回当前位置；未插入时为 -1。 |
| `setSelected(bool)` / `isSelected()` | 控制或查询选择状态，需已在表格中。 |
| `flags()` / `setFlags()` | 控制是否可选、可编辑、可勾选、可拖放等。 |
| `text/icon/font/background/foreground/checkState/sizeHint` | 各自对应标准 data role 的便捷访问器。 |
| `data(int role) const` / `setData(int role, QVariant)` | 通用角色数据接口。 |
| `operator<(const QTableWidgetItem &)` | 排序比较函数；默认主要按显示数据。 |
| `read(QDataStream &)` / `write(QDataStream &) const` | 序列化 item 数据。 |
| `type() const` | 返回构造时 type；自定义类型使用 `UserType` 及以上。 |
| `operator=` | 复制数据和 flags；不复制 type 和所属 table。 |
