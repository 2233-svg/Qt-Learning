# QBoxLayout

> Qt 6.11.1 · Qt Widgets · 来自 `QBoxLayout`

## 1. 先建立直觉

### 这是什么

`QBoxLayout` 是“一条轴线上的布局”：它把控件、子布局和空白项按水平或垂直方向排成一排，然后在窗口尺寸变化时重新计算每一项的位置和大小。

实际项目里你更多会直接用 `QHBoxLayout` 和 `QVBoxLayout`，它们只是把方向预设好的 `QBoxLayout`。直接使用 `QBoxLayout` 的典型理由，是你希望运行时切换方向，或明确需要 `RightToLeft`、`BottomToTop` 这样的反向排列。

### 适合使用的场景

- 一行按钮、一列设置项、标题加工具按钮、侧边栏加内容区。
- 需要用 stretch 把剩余空间按比例分给几个区域。
- 需要用可伸缩空白把按钮推到一侧，或把某个控件居中。
- 需要嵌套横向和纵向布局，快速搭出大多数传统桌面界面。

### 不适合的场景

- 二维表格式排列用 `QGridLayout` 或 `QFormLayout` 更清楚。
- 多页切换用 `QStackedLayout` 或 `QStackedWidget`，不要靠一堆控件 hide/show 堆在盒布局里。
- 需要自动换行的标签云、按钮流，标准 `QBoxLayout` 不会折行，应考虑自定义流式布局。

### 最小示例

```cpp
auto *layout = new QHBoxLayout(parent);
layout->setContentsMargins(12, 12, 12, 12);
layout->setSpacing(8);
layout->addWidget(new QLabel(tr("Name")), 0);
layout->addWidget(new QLineEdit, 1);
layout->addWidget(new QPushButton(tr("Search")), 0);
```

这里 `QLineEdit` 的 stretch 是 `1`，因此主方向上的额外宽度会优先给输入框；标签和按钮保持接近自己的推荐宽度。

## 2. 依赖与对象关系

- 头文件：`#include <QBoxLayout>`
- 模块：Qt Widgets
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QLayout`
- 直接派生类：`QHBoxLayout`、`QVBoxLayout`

### 排列模型

`QBoxLayout` 先从自身几何中扣掉 `contentsMargins`，再在相邻项目之间放入 `spacing`，最后沿主方向分配剩余空间。每个项目仍受自己的最小尺寸、推荐尺寸、最大尺寸和 `QSizePolicy` 限制。

主方向由 `Direction` 决定：水平布局分配宽度，垂直布局分配高度。另一个方向通常由可用空间、对齐方式和项目尺寸策略共同决定。

### 项目类型

盒布局里可以放四类东西：`QWidget`、子 `QLayout`、固定空白、可伸缩空白。它们都以 `QLayoutItem` 的形式存在，所以索引计算会把不可见的 stretch 和 spacer 也算进去。

这点会影响 `setStretch(index, value)` 和 `takeAt(index)`：index 不是第几个可见控件，而是第几个布局项。

### 所有权

加入布局的子布局和 spacer 所有权交给布局。控件会被重新设置 parent 到布局所属的父控件，但从布局移除控件不会自动删除控件。动态重排时要分清“从布局移走”和“销毁对象”。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `enum Direction` | 设置排列方向：从左到右、从右到左、从上到下、从下到上。 |
| `QBoxLayout(Direction dir, QWidget *parent)` | 创建指定方向的盒布局，可直接安装到父控件。 |
| `~QBoxLayout()` | 销毁布局对象；不会因为布局析构而销毁普通控件对象。 |
| `addWidget(QWidget *widget, int stretch, Qt::Alignment alignment)` | 追加控件，设置主方向伸缩比例和对齐方式。 |
| `addLayout(QLayout *layout, int stretch)` | 追加子布局，形成横纵嵌套结构。 |
| `addSpacing(int size)` | 追加固定大小的空白。 |
| `addStretch(int stretch)` | 追加可伸缩空白，用于吸收剩余空间。 |
| `addStrut(int size)` | 给垂直于主方向的尺寸设置最小限制。 |
| `addSpacerItem(QSpacerItem *spacerItem)` | 追加自定义 spacer，表达更复杂的空白策略。 |
| `insertWidget(int index, QWidget *widget, int stretch, Qt::Alignment alignment)` | 在指定位置插入控件。 |
| `insertLayout(int index, QLayout *layout, int stretch)` | 在指定位置插入子布局。 |
| `insertSpacing(int index, int size)` | 在指定位置插入固定空白。 |
| `insertStretch(int index, int stretch)` | 在指定位置插入可伸缩空白。 |
| `insertSpacerItem(int index, QSpacerItem *spacerItem)` | 在指定位置插入自定义 spacer。 |
| `insertItem(int index, QLayoutItem *item)` | 在指定位置插入底层布局项。 |
| `direction() const` / `setDirection(Direction)` | 读取或切换排列方向。 |
| `setStretch(int index, int stretch)` / `stretch(int index) const` | 按布局项索引设置或读取伸缩因子。 |
| `setStretchFactor(QWidget *widget, int stretch)` | 按控件对象设置伸缩因子。 |
| `setStretchFactor(QLayout *layout, int stretch)` | 按子布局对象设置伸缩因子。 |
| `addItem(QLayoutItem *item)` | `QLayout` 重写；追加底层 item。 |
| `count() const` / `itemAt(int) const` / `takeAt(int)` | 遍历、查看和移除布局项。 |
| `setGeometry(const QRect &r)` | 根据给定矩形重新分配所有项目的位置。 |
| `sizeHint() const` / `minimumSize() const` / `maximumSize() const` | 汇总子项尺寸，给父布局或父窗口参考。 |
| `hasHeightForWidth() const` / `heightForWidth(int)` / `minimumHeightForWidth(int)` | 支持“宽度影响高度”的控件，例如自动换行文本。 |
| `expandingDirections() const` | 返回布局愿意扩展的方向。 |
| `setSpacing(int)` / `spacing() const` | 设置或读取相邻项目间距。 |
| `invalidate()` | 让布局尺寸缓存失效，等待重新计算。 |

## 4. API 逐项说明

### `enum QBoxLayout::Direction`

`Direction` 决定项目加入后的排列顺序，也决定 stretch 作用在哪条轴上。

- `LeftToRight`：从左向右排，等价于常见 `QHBoxLayout` 方向。
- `RightToLeft`：从右向左排，适合特殊镜像界面或反向工具区。
- `TopToBottom`：从上向下排，等价于常见 `QVBoxLayout` 方向。
- `BottomToTop`：从下向上排，适合底部优先的堆叠面板。

注意它和应用的文字方向不是一回事。国际化界面中，布局方向、文本方向、控件对齐可能需要分别考虑。

### `QBoxLayout(QBoxLayout::Direction dir, QWidget *parent = nullptr)`

创建一个指定方向的盒布局。传入 `parent` 时，它会成为该控件的顶层布局；不传 parent 时，要稍后加入另一个布局或安装到控件上。

普通应用代码通常选择 `new QHBoxLayout(parent)` 或 `new QVBoxLayout(parent)`，语义更直接。

### `~QBoxLayout()`

销毁布局。布局中的布局项会被清理，但它管理过的普通控件对象不会因为“从布局角度消失”就自动按你的业务意图删除。

如果你正在动态移除界面片段，应显式决定控件是隐藏、复用、重新加入别的布局，还是 `deleteLater()`。

### `addWidget(QWidget *widget, int stretch = 0, Qt::Alignment alignment = Qt::Alignment())`

把控件追加到末尾。`stretch` 控制主方向上额外空间的分配比例；`alignment` 控制控件在分配到的区域内如何摆放。

`stretch = 0` 不等于“不能变大”。如果没有任何项目设置正 stretch，Qt 会根据各控件 `QSizePolicy` 分配空间。一旦某些项目有正 stretch，额外空间主要按正 stretch 比例分配。

### `addLayout(QLayout *layout, int stretch = 0)`

把子布局追加到末尾。横纵嵌套是 Widgets 界面最常见的组织方式：外层纵向分区，内部横向排列字段或按钮。

子布局加入后所有权交给父布局，不要再手动把同一个布局安装到别的父控件上。

### `addSpacing(int size)`

添加固定大小空白。它不会随窗口变大主动伸展，适合表达某两个项目之间的额外距离。

固定空白要少用。若只是统一项目间隔，用 `setSpacing()` 更一致；若是推开剩余空间，用 `addStretch()` 更合适。

### `addStretch(int stretch = 0)`

添加可伸缩空白。它常用来把按钮推到右侧、把控件推到底部、或配合两侧 stretch 让内容居中。

`addStretch(1)` 是最常见写法。若多个 stretch 同时存在，剩余空间按比例分配。

### `addStrut(int size)`

给垂直于主方向的尺寸加一个最小约束。水平盒布局中，strut 影响最小高度；垂直盒布局中，strut 影响最小宽度。

它适合保证一行工具区至少有某个高度，或一列侧栏至少有某个宽度。它不是添加可见控件，也不是主方向上的间隔。

### `addSpacerItem(QSpacerItem *spacerItem)`

追加一个自定义 spacer，并把所有权交给布局。相比 `addSpacing()` 和 `addStretch()`，`QSpacerItem` 能携带更完整的尺寸策略。

只有当固定空白和 stretch 表达不了你的需求时才需要它。

### `insertWidget()` / `insertLayout()` / `insertSpacing()` / `insertStretch()` / `insertSpacerItem()` / `insertItem()`

这些函数在指定索引处插入项目。索引按布局项计数，包括控件、子布局、spacer 和 stretch。

运行时插入控件后，后面所有索引都会变化。长期维护的动态界面最好保存对象指针，通过 `indexOf()` 查找当前位置，而不是把 magic index 写死。

### `direction() const` / `setDirection(QBoxLayout::Direction direction)`

读取或改变排列方向。切换方向后，已有项目顺序不变，但它们会沿新轴重新排列。

如果切换方向后界面尺寸很怪，通常是因为控件的 horizontal/vertical size policy 原本只针对旧方向调过。

### `setStretch(int index, int stretch)` / `stretch(int index) const`

按布局项索引设置或读取伸缩因子。它适合你明确知道第几个 item 代表什么的场景。

对动态布局更推荐 `setStretchFactor(widget, stretch)` 或 `setStretchFactor(layout, stretch)`，可读性更强，也不容易被插入项打乱。

### `setStretchFactor(QWidget *widget, int stretch)`

为当前布局直接管理的某个控件设置 stretch，成功返回 `true`。如果控件不在这一层布局中，返回 `false`。

它不会递归进入子布局。若控件在子布局里，要对那个子布局调用，或调整父布局中“整个子布局”这一项的 stretch。

### `setStretchFactor(QLayout *layout, int stretch)`

为当前布局直接包含的子布局设置 stretch。常用于外层布局中控制侧栏、内容区、预览区的比例。

这不会改变子布局内部各控件的分配规则；内部分配仍由子布局自己的 stretch 和 size policy 决定。

### `addItem(QLayoutItem *item)`

`QLayout` 的重写版本，追加底层布局项。应用代码通常不直接调用，除非你手动构造了 `QSpacerItem` 或特殊 `QLayoutItem`。

传入后 item 所有权交给布局。

### `count()` / `itemAt(int)` / `takeAt(int)`

三者用于遍历和修改布局项。`itemAt()` 不转移所有权；`takeAt()` 会把 item 从布局中取出并交给调用方。

删除或移动项目时要检查 `item->widget()`、`item->layout()`、`item->spacerItem()`。盒布局里的“空白”也是 item，不要假设每一项都有 widget。

### `setGeometry(const QRect &r)`

布局被要求占据某个矩形时调用。`QBoxLayout` 会在这里按方向、边距、间距、stretch 和尺寸约束计算每个项目的矩形。

普通应用代码不需要直接调用它；父控件尺寸变化时 Qt 会自动触发布局流程。

### `sizeHint()` / `minimumSize()` / `maximumSize()`

这些函数汇总内部项目的尺寸。盒布局会沿主方向累加项目尺寸和 spacing，沿副方向取合适的最大值或约束值。

如果窗口默认尺寸不合理，通常要从子控件的 `sizeHint()`、文本长度、字体、图标尺寸和 stretch 查起。

### `hasHeightForWidth()` / `heightForWidth(int w)` / `minimumHeightForWidth(int w)`

支持“宽度影响高度”的项目，例如自动换行的 label。水平空间变化后，高度可能也要重新计算。

如果你在布局里放了大量自动换行文本，窗口缩放时高度变化看起来“不线性”是正常的，因为文本换行点在改变。

### `expandingDirections() const`

返回盒布局整体愿意扩展的方向。它由内部项目的尺寸策略和布局方向共同决定。

父布局会使用这个信息判断额外空间该给谁。一个控件为什么被拉大，常常要看它自己的 `QSizePolicy` 和所在布局的 expanding directions。

### `setSpacing(int spacing)` / `spacing() const`

设置或读取相邻项目间距。它只影响项目之间，不影响布局外圈边距。

如果没有设置，盒布局会使用父布局或平台 style 的默认间距。组件库通常应尊重这个默认值，除非你有明确的视觉规范。

### `invalidate()`

清掉布局缓存，让下一轮布局重新计算。改变项目、spacing、stretch、方向时通常会自动失效。

应用代码很少主动调用；自定义布局或复杂动态界面在手动调整内部 item 后才可能需要。

## 5. 深入实践与常见坑

### stretch 是分配剩余空间，不是像素

`1:2:1` 表示比例，不表示控件最终宽度。最小尺寸、最大尺寸、size policy 会先参与约束；某项不能继续变大时，多余空间会转给其他项。

### 对齐不会制造空白

`alignment` 控制控件在自己的分配区域里靠哪里摆，不负责把两个控件推开。想把“确定/取消”按钮推到右侧，应在它们前面加 `addStretch(1)`。

### 索引包含不可见项目

`addStretch()`、`addSpacing()`、`addSpacerItem()` 都会占一个 index。使用 `setStretch(index, ...)` 或 `takeAt(index)` 时尤其要注意。

### 横纵嵌套要有主次

复杂窗口通常外层少量大区块，内层再细分字段和按钮。不要把几十个控件都塞进一个盒布局里靠 spacing 调整；那样一旦需求变化，索引、stretch 和间距会很快难以维护。
