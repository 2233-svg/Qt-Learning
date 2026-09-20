# Qt QGridLayout 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QGridLayout>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QLayout -> QGridLayout`  
> 定位：把可用矩形按行列切分的二维布局

## 1. QGridLayout 解决什么问题

`QBoxLayout` 擅长把项目排成一行或一列；当界面同时存在标题、内容区、侧栏、跨列按钮栏、占位列或需要严格列对齐的多组控件时，一维嵌套会很快变得难读。`QGridLayout` 直接使用 `(row, column)` 描述位置，把父布局给出的区域切成网格后再分配给项目。

```text
             column 0       column 1        column 2
row 0      [ 标题 ---------------------------------- ]
row 1      [ 工具栏 ]       [ 主内容区 ------------ ]
row 2      [ 状态 ]         [ 操作按钮 ------------ ]
```

它解决的不是“固定像素坐标”，而是这些约束：

- 某个项目从第几行、第几列开始；
- 它跨几行、几列；
- 哪些行列不能小于某个尺寸；
- 多余宽高应按什么比例给各行列；
- 项目是填满单元格还是按 size hint 局部对齐。

常见场景：

- 对齐要求强的属性编辑器、参数面板；
- 带图标、标题、预览区和操作区的对话框；
- 计算器键盘、控制台按钮矩阵；
- 中间内容区随窗口扩展、侧边栏保持较窄的主界面；
- 与 `QFormLayout` 不完全匹配的复杂表单，例如某些字段需要跨两列。

若界面就是标准“标签 - 字段”对，优先 `QFormLayout`；若只是单行或单列，优先 `QHBoxLayout` / `QVBoxLayout`。`QGridLayout` 更自由，也意味着行列语义需要你自己保持清晰。

## 2. 最小可用示例：有侧栏和主内容区的网格

```cpp
#include <QApplication>
#include <QGridLayout>
#include <QLabel>
#include <QListWidget>
#include <QPlainTextEdit>
#include <QPushButton>
#include <QWidget>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QWidget window;
    auto *grid = new QGridLayout(&window);

    auto *title = new QLabel("项目说明");
    auto *sidebar = new QListWidget;
    sidebar->addItems({"概览", "构建", "运行"});
    auto *editor = new QPlainTextEdit;
    auto *saveButton = new QPushButton("保存");
    auto *closeButton = new QPushButton("关闭");

    grid->addWidget(title, 0, 0, 1, 3);      // 从 (0, 0) 起，跨 1 行 3 列
    grid->addWidget(sidebar, 1, 0);
    grid->addWidget(editor, 1, 1, 1, 2);     // 主内容跨两列
    grid->addWidget(saveButton, 2, 1);
    grid->addWidget(closeButton, 2, 2);

    grid->setColumnMinimumWidth(0, 120);     // 侧栏不小于 120 px
    grid->setColumnStretch(0, 0);
    grid->setColumnStretch(1, 1);
    grid->setColumnStretch(2, 0);
    grid->setRowStretch(1, 1);               // 多余高度优先给中间内容行

    window.resize(640, 420);
    window.show();
    return app.exec();
}
```

这里真正控制窗口拉大后编辑器区域变大的，是第 1 行和第 1 列的 stretch；`editor` 跨列只是让它覆盖多个单元格，不会自动让那些列平均或等比扩展。

构造 `QGridLayout(&window)` 时，它立即成为 `window` 的顶层布局。若传入 `nullptr`，创建后要么通过父布局的 `addLayout()` 嵌入它，要么调用 `window.setLayout(grid)`。一个 `QWidget` 只能有一个顶层布局。

## 3. 坐标、跨度和对齐

网格坐标从 `(0, 0)` 开始。默认情况下它是左上角，但可以用 `setOriginCorner()` 改变逻辑原点所在角。

```cpp
grid->addWidget(widget, 2, 3);          // 第 2 行、第 3 列，跨度默认 1 x 1
grid->addWidget(header, 0, 0, 1, 4);    // 1 行 x 4 列
grid->addWidget(preview, 1, 0, 2, 2);   // 2 行 x 2 列
```

带跨度的重载中：

- `fromRow` / `fromColumn` 是左上起始单元格的逻辑坐标；
- `rowSpan` / `columnSpan` 是占用的行数、列数；
- 对 `addWidget()`、`addLayout()`、`addItem()`，跨度传 `-1` 表示延伸到网格的底边或右边；
- `alignment` 默认为空，即项目填充整个分配区域；非零对齐意味着项目按 `sizeHint()` 放在分配区域内，而不是继续拉大。

```cpp
grid->addWidget(new QPushButton("小按钮"),
                3, 2, Qt::AlignRight | Qt::AlignVCenter);
```

不要把 `alignment` 和 `QSizePolicy` 当成同一个开关：`QSizePolicy` 表达控件愿不愿意伸缩，`alignment` 规定布局已分配一个大单元格后控件如何停放。设置了 `AlignRight` 的按钮不会填满单元格，即使单元格很宽。

## 4. 行列尺寸如何计算

每一列、每一行都有两个重要约束：最小尺寸和 stretch。以列为例：

```text
某列最终最小宽度
  = max( setColumnMinimumWidth() 设置的值,
         该列内项目的最小宽度约束 )

额外宽度
  -> 按各列 stretch 和项目 QSizePolicy 共同分配
```

```cpp
grid->setColumnMinimumWidth(0, 24); // 图标列或空白分隔列
grid->setColumnMinimumWidth(1, 180);

grid->setColumnStretch(0, 0);
grid->setColumnStretch(1, 2);
grid->setColumnStretch(2, 1);
```

在能扩展的前提下，后两列会以约 `2:1` 分配额外宽度。stretch 是相对权重，不是像素，也不保证控件最后尺寸严格是 2:1：最小尺寸、最大尺寸、跨格项目和 `QSizePolicy` 都会参与计算。

特别要注意：

- 所有 stretch 都为 0，不代表行列绝不会增长；如果没有其他行列能增长，Qt 仍可能让它增长。
- 想让两列等宽，必须把**最小宽度和 stretch 都设成相同**。只设相同 stretch 不能消除不同控件最小宽度带来的差异。
- 跨多列项目的最小尺寸需要分摊到涉及的列。Qt 会参考各行列 stretch 猜测分配方式；复杂跨格界面最好显式设置相关行列的 stretch。
- `setColumnMinimumWidth()` 适合保证列的下限或创建固定宽空白列；仅为了普通控件间距，优先使用 layout 的 `spacing`，不要到处塞“魔法空列”。

## 5. 空白、边距和间距

`QGridLayout` 有两层空白：

```text
contentsMargins
+-----------------------------------+
|  [cell] <- spacing -> [cell]      |
+-----------------------------------+
```

- contents margins：网格边界到父控件边缘的留白，来自 `QLayout`。
- horizontal / vertical spacing：相邻单元格之间的距离。

```cpp
grid->setContentsMargins(12, 12, 12, 12);
grid->setHorizontalSpacing(10);
grid->setVerticalSpacing(6);
```

未设置横纵间距时，Qt 会从父布局或当前 style 读取默认值。`setSpacing(8)` 会同时设置横、纵间距；若两个方向不同，`spacing()` 返回 `-1`。一般用 `QSpacerItem` 表达需要随空间伸缩的“弹性空白”，用 spacing 表达统一、固定的控件间距。

```cpp
grid->addItem(
    new QSpacerItem(0, 0, QSizePolicy::Minimum, QSizePolicy::Expanding),
    4, 0, 1, 3);
```

`addItem()` 接管这个 `QSpacerItem` 的所有权。不要使用它包装普通 `QWidget` 或子 `QLayout`；这两种对象必须分别用 `addWidget()`、`addLayout()` 加入。

## 6. originCorner：改变逻辑原点，不是 RTL 的万能开关

`originCorner` 决定逻辑坐标 `(0, 0)` 映射到网格的哪一个视觉角：

```cpp
grid->setOriginCorner(Qt::BottomRightCorner);
```

这在需要从右下向左上排列的特殊棋盘、面板或与外部坐标系统对应的界面中有用。它不改变你调用 API 时的行列编号规则，也不会自动替代应用的布局方向（如右到左语言支持）。普通界面通常保持默认原点；要做完整 RTL 适配，还应理解 `QWidget::layoutDirection()` 和 style 的布局行为。

## 7. 查询单元格与动态调整

动态界面常需要定位某个项目：

```cpp
QLayoutItem *item = grid->itemAtPosition(1, 1);
if (item && item->widget()) {
    item->widget()->setEnabled(false);
}

int row, column, rowSpan, columnSpan;
grid->getItemPosition(0, &row, &column, &rowSpan, &columnSpan);
```

- `itemAtPosition(row, column)` 按单元格找占用该格的项目；空格返回 `nullptr`。
- `itemAt(index)` / `getItemPosition(index, ...)` 使用的是内部项目线性索引，插入顺序与视觉位置不是一回事。
- `cellRect(row, column)` 返回单元格最终几何。父控件尚未显示、布局尚未执行 `setGeometry()` 时，这个矩形可能无效；不要在构造函数里用它做坐标计算。
- 移除一个 widget 可调用继承自 `QLayout` 的 `removeWidget()`；它只是解除布局管理，不删除控件。调用 `widget->hide()` 也会让布局暂时不把该 widget 计入可见几何，`show()` 后重新参与。
- `takeAt(index)` 取出一个 `QLayoutItem` 也不会删除它；调用者需处理 item 及其 widget/layout 的后续所有权。

## 8. 常见误区

### 8.1 以为网格天然等宽等高

它不会。行列最终大小取决于项目尺寸约束、最小尺寸、stretch、span 和 style。需要相等时，逐行逐列明确设置：

```cpp
grid->setColumnMinimumWidth(0, 100);
grid->setColumnMinimumWidth(1, 100);
grid->setColumnStretch(0, 1);
grid->setColumnStretch(1, 1);
```

### 8.2 跨格之后不再设置相关行列权重

一个跨两列的编辑器可能看起来“不够宽”，原因往往是被跨越的两列 stretch 都为 0，或其中一列被固定控件限制。跨度描述覆盖范围，不代替尺寸策略。

### 8.3 手动设 geometry 与布局争夺控制权

加入 `QGridLayout` 的控件几何由布局在 resize、字体变化、显示/隐藏后重新计算。对这类控件反复 `move()`、`resize()` 或 `setGeometry()`，结果会在下一次布局时被覆盖。

### 8.4 把布局的析构理解成会删除所有 widget

`QGridLayout` 析构时不会直接删除它管理的 widgets；实际 widget 生命周期通常由父 `QWidget` 的对象树负责。相反，`QLayoutItem` 是布局管理的一部分，`addItem()` 传入的 item 所有权交给布局。动态拆除时先明确自己取出的是 widget、layout 还是 item。

## API 速查表
### 9.1 创建、加入项目与坐标

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QGridLayout(QWidget *parent = nullptr)` | 创建网格布局，传 `parent` 时成为其顶层布局 | 无 parent 时要嵌入父布局或调用 `setLayout()` |
| 生命周期 | `~QGridLayout()` | 销毁布局并停止几何管理 | 不直接销毁其管理的 widgets；widgets 通常由父对象树销毁 |
| 添加控件 | `addWidget(QWidget *widget)` | 使用默认定位规则加入控件 | 来自公开 inline 重载；具体行列由 `setDefaultPositioning()` 规则决定，普通网格更建议显式写坐标 |
| 添加控件 | `addWidget(QWidget *widget, int row, int column, Qt::Alignment alignment = {})` | 把控件放到一个单元格 | 默认填满单元格；非零 alignment 会按 size hint 局部停放 |
| 添加控件 | `addWidget(QWidget *widget, int fromRow, int fromColumn, int rowSpan, int columnSpan, Qt::Alignment alignment = {})` | 把控件放入并跨越多个单元格 | `rowSpan` / `columnSpan` 为 `-1` 时延伸至底边或右边 |
| 添加布局 | `addLayout(QLayout *layout, int row, int column, Qt::Alignment alignment = {})` | 把子布局放到一个单元格 | 子布局成为 grid 的子布局，不能再属于其他父布局 |
| 添加布局 | `addLayout(QLayout *layout, int row, int column, int rowSpan, int columnSpan, Qt::Alignment alignment = {})` | 把子布局放入并跨越多个单元格 | span 为 `-1` 时延伸至边缘 |
| 添加项目 | `addItem(QLayoutItem *item, int row, int column, int rowSpan = 1, int columnSpan = 1, Qt::Alignment alignment = {})` | 把原始布局项放入网格 | grid 接管 item；适合 `QSpacerItem`，不要用它添加 widget 或 child layout |
| 底层添加 | `addItem(QLayoutItem *item)` | 对 `QLayout::addItem()` 的保护重实现 | 自定义派生布局的框架入口，应用代码不能直接调用 |
| 自动定位 | `setDefaultPositioning(int n, Qt::Orientation orient)` | 设置无坐标添加项目时的自动换行/换列规则 | 很少用于普通手写界面；显式 `(row, column)` 更清楚 |
| 行列数量 | `rowCount() const` | 返回当前网格行数 | 行数会随新项目扩展，不等于项目数量 |
| 行列数量 | `columnCount() const` | 返回当前网格列数 | 列数会随新项目扩展，不等于项目数量 |
| 原点 | `originCorner() const` | 读取逻辑 `(0, 0)` 对应的视觉角 | 特殊坐标映射时检查 |
| 原点 | `setOriginCorner(Qt::Corner corner)` | 设置逻辑网格原点 | 不应拿它替代完整 RTL 支持 |

### 9.2 行列大小、权重与间距

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 列尺寸 | `columnMinimumWidth(int column) const` | 读取某列显式设置的最小宽度 | 实际列下限还受该列项目最小尺寸影响 |
| 列尺寸 | `setColumnMinimumWidth(int column, int minSize)` | 为列设置最小宽度 | 适合图标列、侧栏下限或等宽列约束；单位是像素 |
| 行尺寸 | `rowMinimumHeight(int row) const` | 读取某行显式设置的最小高度 | 实际行下限还受该行项目最小尺寸影响 |
| 行尺寸 | `setRowMinimumHeight(int row, int minSize)` | 为行设置最小高度 | 适合工具行、预览行或保留空间；单位是像素 |
| 列权重 | `columnStretch(int column) const` | 读取列的额外宽度权重 | 0 不一定意味着永不增长，还要看其他列和 size policy |
| 列权重 | `setColumnStretch(int column, int stretch)` | 设置列的额外宽度权重 | 是相对值，不是像素；如 2 和 1 表示优先比例 |
| 行权重 | `rowStretch(int row) const` | 读取行的额外高度权重 | 内容区行通常比工具行大 |
| 行权重 | `setRowStretch(int row, int stretch)` | 设置行的额外高度权重 | 与 `QSizePolicy`、最小/最大尺寸一起决定最终高度 |
| 间距 | `horizontalSpacing() const` | 读取同一行相邻单元格间距 | 未显式设置时可能从父布局或 style 获取 |
| 间距 | `setHorizontalSpacing(int spacing)` | 设置横向间距 | 只影响列间距离 |
| 间距 | `verticalSpacing() const` | 读取上下相邻单元格间距 | 未显式设置时可能从父布局或 style 获取 |
| 间距 | `setVerticalSpacing(int spacing)` | 设置纵向间距 | 只影响行间距离 |
| 间距 | `spacing() const` | 读取统一间距 | 横纵间距不相等时返回 `-1` |
| 间距 | `setSpacing(int spacing)` | 同时设置横纵间距 | 需要统一网格节奏时使用 |

### 9.3 查找项目与实际几何

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 几何 | `cellRect(int row, int column) const` | 返回某单元格的最终矩形 | 越界为无效矩形；父控件可见且布局执行后才可靠 |
| 查询 | `itemAtPosition(int row, int column) const` | 返回占据某逻辑单元格的项目 | 空单元格返回 `nullptr`；span 覆盖范围内也可命中该项目 |
| 查询 | `itemAt(int index) const` | 按内部线性索引返回项目 | 与单元格坐标不同；越界返回 `nullptr` |
| 定位 | `getItemPosition(int index, int *row, int *column, int *rowSpan, int *columnSpan) const` | 反查内部项目的起点和跨行跨列范围 | 适合遍历、序列化或动态重排 |
| 项数 | `count() const` | 返回布局项数 | 按 item 数统计，不是已占单元格数 |
| 接管 | `takeAt(int index)` | 按内部索引取出一个项目 | 不删除 item；调用者负责后续所有权 |

### 9.4 布局引擎重实现接口

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 尺寸协商 | `expandingDirections() const` | 报告网格可有效利用额外空间的方向 | 父布局的尺寸协商使用 |
| 高宽相关 | `hasHeightForWidth() const` | 查询高度是否依赖宽度 | 内含可换行项目时可能为真 |
| 高宽相关 | `heightForWidth(int w) const` | 计算给定宽度下所需高度 | 由父布局和 Qt 几何过程调用 |
| 高宽相关 | `minimumHeightForWidth(int w) const` | 计算给定宽度下的最小高度 | 用于更严格的尺寸协商 |
| 尺寸协商 | `minimumSize() const` | 返回满足内容约束的最小尺寸 | 窗口最小尺寸计算使用 |
| 尺寸协商 | `sizeHint() const` | 返回推荐尺寸 | 受行列、项目、span、边距和间距共同影响 |
| 尺寸协商 | `maximumSize() const` | 返回允许的最大尺寸 | 综合子项目最大约束 |
| 几何分配 | `setGeometry(const QRect &rect)` | 将分配矩形拆成行列并写入项目 geometry | Qt 自动调用；应用代码不应手动分配子项 |
| 缓存 | `invalidate()` | 让已缓存的尺寸计算失效 | 内容、约束或可见性变动后由 Qt 流程处理 |
