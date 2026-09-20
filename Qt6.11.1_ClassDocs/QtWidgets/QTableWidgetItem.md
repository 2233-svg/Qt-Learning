# QTableWidgetItem

> Qt 6.11.1 · Qt Widgets · 来自 `QTableWidgetItem`

## 1. 先建立直觉

`QTableWidgetItem` 是 `QTableWidget` 中一个单元格或表头格子的 item。它不是 QWidget，而是保存显示数据、编辑数据、图标、字体、颜色、勾选状态、对齐方式和自定义 role 的轻量对象。

它适合小型表格和原型工具。若你的单元格数据来自业务模型，或者需要大规模更新、排序过滤、懒加载，应该把数据放进 `QAbstractTableModel`，而不是让每个格子都成为一个 item 对象。

## 2. 类说明

- 头文件：`#include <QTableWidgetItem>`
- 模块：`Qt6::Widgets`
- 继承自：无
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

item 放进 `QTableWidget` 后由表格管理；用 `takeItem()` 或取走表头 item 后，所有权回到调用者。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QTableWidgetItem(type)` | 创建空单元格 item。 |
| `QTableWidgetItem(text, type)` | 创建带文本的 item。 |
| `QTableWidgetItem(icon, text, type)` | 创建带图标和文本的 item。 |
| `QTableWidgetItem(other)` / `operator=()` | 复制 item 数据；不会复制所属表格。 |
| `clone()` | 创建副本，配合 item prototype 或子类使用。 |
| `type()` | item 类型；自定义类型从 `UserType` 起。 |
| `tableWidget()` | 返回所属表格，未插入时为空。 |
| `row()` / `column()` | 返回当前所在行列；未插入时为 `-1`。 |
| `text()` / `setText()` | 显示文本。 |
| `icon()` / `setIcon()` | 显示图标。 |
| `data(role)` / `setData(role, value)` | 按数据角色读写值。 |
| `checkState()` / `setCheckState()` | 勾选状态。 |
| `flags()` / `setFlags()` | 控制可选、可编辑、可勾选、可拖拽等行为。 |
| `font()` / `setFont()` | 字体。 |
| `foreground()` / `setForeground()` | 前景画刷。 |
| `background()` / `setBackground()` | 背景画刷。 |
| `sizeHint()` / `setSizeHint()` | 单元格推荐尺寸。 |
| `textAlignment()` / `setTextAlignment()` | 文本对齐；`setTextAlignment` 自 Qt 6.4 起可用。 |
| `toolTip()` / `setToolTip()` | 鼠标提示。 |
| `statusTip()` / `setStatusTip()` | 状态栏提示。 |
| `whatsThis()` / `setWhatsThis()` | What's This 帮助。 |
| `isSelected()` / `setSelected()` | 查询或设置选择状态。 |
| `read()` / `write()` | 用 `QDataStream` 序列化。 |
| `operator<()` | 排序比较逻辑，子类可重写。 |
| `operator<<` / `operator>>` | 非成员流操作符。 |

## 4. 关键用法

### 显示值和排序值可以分开

表格里经常显示 `"1,234.50"`、`"2026-09-17"`、`"12 ms"` 这类字符串，但排序需要数字或日期。把展示文本放在 `DisplayRole`，把原始值放在 `UserRole`，然后重写 `operator<()` 使用原始值，能避免字符串排序把 `100` 排在 `20` 前面。

### 空单元格不是空 item

`QTableWidget` 中未设置过的单元格，`item(row, column)` 返回空指针。要改文字、颜色或 flags，必须先创建 `QTableWidgetItem` 并 `setItem()`。这也是 `selectedItems()` 可能少于选中单元格数量的原因：空单元格没有 item 可返回。

### 表头也可以是 item

水平和垂直表头可以使用 `QTableWidgetItem`，因此也能设置图标、对齐、提示和自定义数据。不要把表头 item 和普通单元格混在同一套业务遍历里，表头不属于表格内容矩阵。

### flags 决定交互能力

只设置显示数据不会自动允许编辑或勾选。可编辑要包含 `Qt::ItemIsEditable`，可勾选要包含 `Qt::ItemIsUserCheckable`，禁用可以移除 `Qt::ItemIsEnabled`。flags 是 item 行为的第一道开关。

## 5. 常见坑与经验

- item 的 `row()`、`column()` 会随排序、插入、删除改变，不要当长期业务 id。
- `setSelected()` 依赖 item 已经在表格里；未插入 item 没有可视选择状态。
- 批量填充时 `itemChanged()` 会被程序修改触发，必要时阻断信号。
- 大量 `setBackground()`、`setFont()` 能工作，但复杂条件样式更适合 delegate。
- 从表格取走 item 后要自己删除或重新插入，否则会泄漏。
