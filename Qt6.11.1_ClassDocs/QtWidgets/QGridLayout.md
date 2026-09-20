# QGridLayout

> Qt 6.11.1 · Qt Widgets · 来自 `QGridLayout`

## 1. 先建立直觉

### 这是什么

`QGridLayout` 是 Qt Widgets 的二维网格布局。它把控件、子布局和底层布局项放到行列坐标中，可以让某个项目跨多行或多列，并分别控制每一行、每一列的最小尺寸和伸缩比例。

和 `QBoxLayout` 的“一条轴线”不同，`QGridLayout` 关心的是表格状空间分配。它适合做结构稳定的二维界面：参数面板、计算器键盘、仪表盘网格、复杂对话框中的字段矩阵。

### 适合使用的场景

- 多个控件需要按行列对齐，而不是简单横排或竖排。
- 某些控件需要跨行或跨列，例如标题跨整行、预览区跨多列。
- 不同列需要不同 stretch，比如标签列固定、输入列扩展、按钮列保持窄。
- 需要通过 `itemAtPosition()` 或 `getItemPosition()` 查询布局项位置。

### 不适合的场景

- 典型“标签 + 字段”表单优先用 `QFormLayout`，它更懂平台表单风格和标签伙伴关系。
- 简单一行或一列用 `QHBoxLayout` / `QVBoxLayout` 更清楚。
- 数据表格展示不是布局问题，应使用 `QTableView`、`QTableWidget` 或模型/视图。

### 最小示例

```cpp
auto *grid = new QGridLayout(parent);
grid->addWidget(new QLabel(tr("Host:")), 0, 0);
grid->addWidget(hostEdit, 0, 1);
grid->addWidget(new QLabel(tr("Port:")), 1, 0);
grid->addWidget(portSpinBox, 1, 1);
grid->addWidget(testButton, 0, 2, 2, 1);
grid->setColumnStretch(1, 1);
```

这里第 1 列是输入区，获得额外宽度；按钮跨两行，占据右侧一列。

## 2. 依赖与对象关系

- 头文件：`#include <QGridLayout>`
- 模块：Qt Widgets
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QLayout`
- 直接派生类：类页未列出

### 坐标与跨度

网格坐标从 `(0, 0)` 开始。默认情况下左上角是原点，但可以用 `setOriginCorner()` 改成其他角。`rowSpan` 和 `columnSpan` 表示占据几行几列；传 `-1` 表示延伸到底部或最右侧。

同一个单元格不要重复放多个项目。Qt 不会把重叠项变成层叠控件；布局结果会变得难以预测。

### 行列尺寸模型

每一行和每一列都有三类影响因素：内部项目的尺寸提示、显式设置的最小尺寸、显式设置的 stretch。列宽不是平均分配的；额外空间会优先给能扩展且 stretch 更高的列。

### 所有权

加入网格的子布局、spacer item 和底层 item 所有权交给布局。控件的 parent 会调整到布局所属的父控件；从布局移除控件并不删除控件。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `horizontalSpacing : int` | 控制相邻列之间的水平间距。 |
| `verticalSpacing : int` | 控制相邻行之间的垂直间距。 |
| `QGridLayout(QWidget *parent)` | 创建网格布局，可直接安装到父控件。 |
| `~QGridLayout()` | 销毁布局对象；普通控件生命周期仍需单独处理。 |
| `addWidget(widget, row, column, alignment)` | 把控件放入单个单元格。 |
| `addWidget(widget, row, column, rowSpan, columnSpan, alignment)` | 把控件放入跨行跨列区域。 |
| `addLayout(layout, row, column, alignment)` | 把子布局放入单个单元格。 |
| `addLayout(layout, row, column, rowSpan, columnSpan, alignment)` | 把子布局放入跨行跨列区域。 |
| `addItem(item, row, column, rowSpan, columnSpan, alignment)` | 放入底层布局项，通常用于 spacer 或自定义 item。 |
| `cellRect(row, column) const` | 获取某单元格最终几何；显示并布局后才可靠。 |
| `rowCount() const` / `columnCount() const` | 返回网格当前行数和列数。 |
| `setRowMinimumHeight(row, minSize)` / `rowMinimumHeight(row)` | 设置或读取某行最小高度。 |
| `setColumnMinimumWidth(column, minSize)` / `columnMinimumWidth(column)` | 设置或读取某列最小宽度。 |
| `setRowStretch(row, stretch)` / `rowStretch(row)` | 设置或读取某行伸缩比例。 |
| `setColumnStretch(column, stretch)` / `columnStretch(column)` | 设置或读取某列伸缩比例。 |
| `setHorizontalSpacing(int)` / `horizontalSpacing() const` | 设置或读取列间距。 |
| `setVerticalSpacing(int)` / `verticalSpacing() const` | 设置或读取行间距。 |
| `setSpacing(int)` / `spacing() const` | 同时设置或读取两个方向的间距。 |
| `setOriginCorner(Qt::Corner)` / `originCorner() const` | 设置或读取 `(0, 0)` 所在角。 |
| `itemAtPosition(row, column) const` | 查询占用某单元格的布局项。 |
| `getItemPosition(index, row, column, rowSpan, columnSpan)` | 按 item 索引反查网格位置和跨度。 |
| `count()` / `itemAt(index)` / `takeAt(index)` | 遍历、查看和移除布局项。 |
| `setGeometry(const QRect &rect)` | 执行实际行列几何分配。 |
| `sizeHint()` / `minimumSize()` / `maximumSize()` | 汇总网格推荐、最小和最大尺寸。 |
| `hasHeightForWidth()` / `heightForWidth(int)` / `minimumHeightForWidth(int)` | 支持宽度影响高度的子项。 |
| `expandingDirections()` | 返回网格整体愿意扩展的方向。 |
| `invalidate()` | 使布局缓存失效，等待重新计算。 |

## 4. API 逐项说明

### `horizontalSpacing` / `verticalSpacing`

网格布局允许水平和垂直间距分开设置。字段密集的表单可能需要较小的垂直间距和较大的水平间距；按钮矩阵可能需要两个方向一致。

如果两个方向间距不同，继承自 `QLayout` 的通用 `spacing()` 可能返回 `-1`，这不是错误，而是表示无法用一个整数描述两个方向。

### `QGridLayout(QWidget *parent = nullptr)`

创建网格布局。传入 `parent` 时直接成为父控件的顶层布局；不传 parent 时，应加入其他布局或通过 `setLayout()` 安装。

网格会随着放入项目自动扩展行列数，不需要先声明尺寸。

### `~QGridLayout()`

销毁布局对象并结束几何管理。控件对象是否销毁由 QObject 父子关系和你的代码决定。

动态清空网格时，优先使用 `takeAt()` 循环，明确处理每个 item 中的 widget、layout 或 spacer。

### `addWidget(...)`

把控件放到网格坐标。单格重载适合普通字段，跨行跨列重载适合大控件或标题。

`alignment` 非空时，控件不一定填满单元格，而是按照自己的推荐尺寸在单元格内对齐。若希望输入框随列宽扩展，通常不要给它设置会阻止填充的 alignment。

### `addLayout(...)`

把子布局放到网格中。它是组织复杂单元格的常用方式，例如某个单元格里再横向排列多个小按钮。

子布局加入后成为网格的一部分。不要再把同一个子布局加入其他父布局。

### `addItem(QLayoutItem *item, int row, int column, int rowSpan, int columnSpan, Qt::Alignment alignment)`

底层插入入口，常用于自定义 `QLayoutItem` 或 `QSpacerItem`。普通控件和子布局应优先使用 `addWidget()`、`addLayout()`，语义更清楚，也能正确登记关系。

传入 item 后所有权交给布局。

### `cellRect(int row, int column) const`

返回某个单元格的最终矩形。这个值只有布局执行过 `setGeometry()` 后才可靠；通常意味着父控件已经显示或至少完成一次布局。

不要在构造函数里依赖 `cellRect()` 做初始化计算。需要显示后计算时，可以在 `showEvent()` 后或通过零延迟 `QTimer::singleShot(0, ...)` 读取。

### `rowCount()` / `columnCount()`

返回当前网格的行列数量。它们反映布局已知的最大坐标范围，不表示每个单元格都有内容。

删除项目后，行列数量可能仍受其他项目、跨度或内部结构影响，不应把它当作紧凑数据表的行数。

### `setRowMinimumHeight()` / `setColumnMinimumWidth()`

给某一行或某一列设置最小尺寸。它适合保证按钮行、图标列、预览列有底线空间。

不要用很大的最小尺寸硬推布局。若目的是让某列占更多剩余空间，应使用 stretch；若目的是让控件本身有自然尺寸，应调整控件的 size hint 或 size policy。

### `setRowStretch()` / `setColumnStretch()`

设置行列对额外空间的分配比例。典型设置是标签列 `0`、输入列 `1`，或左右两个内容区 `1:2`。

stretch 只分配剩余空间，不会让行列小于内部项目最小尺寸，也不会强迫超过最大尺寸的控件继续变大。

### `setHorizontalSpacing()` / `setVerticalSpacing()` / `setSpacing()`

分别设置列间距、行间距，或一次设置两个方向。未显式设置时，间距通常来自父布局或平台 style。

网格中不要靠空白列模拟间距；优先使用 spacing。空白列更适合表达真实结构，例如固定图标槽或可伸缩分隔区。

### `setOriginCorner(Qt::Corner corner)` / `originCorner() const`

控制 `(0, 0)` 从哪个角开始解释。默认常见为左上角。改变原点会影响视觉排列方向，但你在代码中写的 row/column 坐标仍是逻辑坐标。

这个功能在镜像界面、特殊仪表面板或从右侧开始填充的布局中有用。普通表单不要为了对齐标签而改 origin corner。

### `itemAtPosition(int row, int column) const`

返回占用指定单元格的布局项。跨行跨列项目占据其覆盖区域内的多个单元格，所以查询其中任意被覆盖位置都可能返回同一 item。

它适合调试布局、做动态替换，或避免重复往同一格塞控件。

### `getItemPosition(int index, ...) const`

按布局项索引反查 row、column、rowSpan、columnSpan。它和 `itemAt(index)` 搭配用于遍历整个网格并了解每项位置。

index 是布局项顺序，不是二维坐标编码。动态插入删除后 index 会变化。

### `count()` / `itemAt(int)` / `takeAt(int)`

继承自 `QLayout` 的遍历与移除接口。`itemAt()` 不转移所有权，`takeAt()` 移除并交出 item。

清空网格时，要处理 item 中可能包含的 widget、layout 或 spacer。仅删除 item 可能不会删除 widget。

### `setGeometry(const QRect &rect)`

网格布局在这里完成实际几何计算：先扣边距和间距，再根据行列最小尺寸、stretch、跨度和子项尺寸提示分配空间。

应用层不应直接调用。需要触发布局更新时，改变布局参数或调用 `update()` / `invalidate()`。

### `sizeHint()` / `minimumSize()` / `maximumSize()`

这些函数汇总网格内容的推荐尺寸、最小尺寸和最大尺寸。跨行跨列项目会参与多个行列的尺寸推导，因此结果不总是简单相加。

布局尺寸异常时，检查跨列控件的最小尺寸和 size policy 往往比检查网格本身更有效。

### `hasHeightForWidth()` / `heightForWidth(int)` / `minimumHeightForWidth(int)`

当网格中有依赖宽度计算高度的项目时，这组函数用于把这种关系向上层布局报告。自动换行文本、富文本标签、某些自定义控件会触发这种模型。

复杂网格中 height-for-width 计算可能较昂贵，所以不要在高频路径反复查询。

### `expandingDirections()` / `invalidate()`

`expandingDirections()` 汇总网格是否愿意在水平或垂直方向扩展。`invalidate()` 清理缓存，让下一轮布局重新计算。

通常这些由 Qt 自动调用。只有写自定义容器或进行复杂动态重组时，才需要主动干预。

## 5. 深入实践与常见坑

### QGridLayout 不是表格控件

它只负责摆放固定数量的界面控件，不负责滚动、选择、单元格编辑、模型数据或大规模行列渲染。展示数据表请用模型/视图。

### 标签表单优先考虑 QFormLayout

`QGridLayout` 可以写表单，但你需要自己处理标签对齐、伙伴关系、换行策略和平台风格。`QFormLayout` 已经把这些规则封装好了。

### 跨行跨列会影响整张网格

一个跨多列的大控件可能抬高多个列的最小宽度，也可能改变额外空间分配。遇到“某列莫名变宽”，先找跨列项目。

### `cellRect()` 不适合构造期使用

构造函数里布局还没拿到最终几何，`cellRect()` 可能无效。需要真实坐标时，等窗口显示并完成布局。
