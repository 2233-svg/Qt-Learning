# QBoxLayout

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QBoxLayout` 是按一个方向排列控件和子布局的布局管理器。它接管子项的几何位置和尺寸，不需要你在窗口 resize 时手动计算每个控件的 `setGeometry()`。水平排列使用一行，垂直排列使用一列。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QBoxLayout` 是按一个方向排列控件和子布局的布局管理器。它接管子项的几何位置和尺寸，不需要你在窗口 resize 时手动计算每个控件的 `setGeometry()`。水平排列使用一行，垂直排列使用一列。

**内部模型：** 把布局想成一个会重新计算矩形的分配器：先从父控件的矩形中扣除 contents margins，再给相邻项目之间留下 spacing，剩余空间沿布局方向分配给控件、子布局和 spacer。每个项目还受到 minimumSize、sizeHint、maximumSize 和 sizePolicy 的限制。

**适用场景：** 一组控件需要横向排列、纵向排列，或者需要在一个方向上按比例占用空间时使用。实际代码中通常直接用 `QHBoxLayout` 或 `QVBoxLayout`，只有需要运行时切换方向或明确指定 `Direction` 时才直接构造 `QBoxLayout`。

**典型调用链：** 创建布局并挂到父控件 -> 按顺序添加 widget、layout、spacing 或 stretch -> 设置 margins、spacing、alignment 和 stretch -> 父控件尺寸变化时由 Qt 自动重新分配 -> 用 add/remove/takeAt 动态修改内容。

**先记住的坑：** `stretch` 是比例，不是像素；`setStretch()` 的 index 是布局项目索引，不是控件编号；`setStretchFactor()` 只查找当前这一层；spacing 不等于外边距；不要给已经交给布局管理的控件反复调用 `setGeometry()`。

## 2. 依赖与对象关系

- 头文件：`#include <QBoxLayout>`
- 继承自：QLayout
- 直接派生类：QHBoxLayout、QVBoxLayout

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

把布局想成一个会重新计算矩形的分配器：先从父控件的矩形中扣除 contents margins，再给相邻项目之间留下 spacing，剩余空间沿布局方向分配给控件、子布局和 spacer。每个项目还受到 minimumSize、sizeHint、maximumSize 和 sizePolicy 的限制。

### 状态、生命周期和线程

**生命周期：** 顶层布局可以在构造时绑定到 QWidget，也可以通过 `setLayout()` 安装；嵌套布局加入父布局后所有权交给父布局。布局析构不会自动销毁普通 QWidget，动态移除项目时要分别处理控件、子布局和 spacer。

**状态与结果：** 布局的项目索引会随着 add、insert、remove 和 takeAt 改变；索引既包括控件，也包括子布局、固定空白和 stretch。修改项目或尺寸参数后 Qt 会使布局失效并重新计算。

**线程与事件循环：** 布局只应在 GUI 线程操作，因为它直接改变 QWidget 几何和可见界面。布局系统不负责业务线程同步，也不会把手动的跨线程控件访问变安全。

## 3. 直接使用

### 布局究竟解决什么问题

窗口大小会变化，字体和平台风格也会变化。把控件的坐标写死，只能在某一个尺寸下看起来正确；布局管理器会根据父控件当前的可用矩形，持续计算每个子项的新矩形。

`QBoxLayout` 只沿一个主方向排列项目：水平布局的主方向是 X 轴，垂直布局的主方向是 Y 轴。项目可以是普通 `QWidget`、另一个 `QLayout`，也可以是固定空白或可伸缩空白。布局本身不绘制背景，也不是一个可见控件，它只是管理几何关系。

### 四个数字决定最终位置

1. **contents margins**：布局外边缘到第一个/最后一个项目之间的距离，分别由 left、top、right、bottom 指定。
2. **spacing**：相邻项目之间的距离。三个项目通常有两个内部间隔，不会自动变成四个外边距。
3. **项目的最小、推荐和最大尺寸**：控件的 `minimumSizeHint()`、`sizeHint()`、`maximumSize()` 和 `QSizePolicy` 会参与分配。
4. **stretch factor**：当主方向还有多余空间时，正的 stretch factor 按比例获得多余空间。例如 1:2:1 表示三项分别分到四等份中的一份、两份、一份。

如果没有任何项目的 stretch 大于 0，Qt 会更多地依据各控件的 `sizePolicy` 和推荐尺寸分配空间；一旦设置了正的 stretch，额外空间主要按 stretch 比例在这些项目之间分配。无论哪种情况，最小尺寸和最大尺寸都优先于比例，比例不是强制把控件拉到任意大小。

### `QHBoxLayout`、`QVBoxLayout` 和直接使用 `QBoxLayout`

- `QHBoxLayout` 等价于方向为 `QBoxLayout::LeftToRight` 的盒式布局，适合工具栏、按钮行、标签加输入框等场景。
- `QVBoxLayout` 等价于方向为 `QBoxLayout::TopToBottom` 的盒式布局，适合表单纵向堆叠、设置页和页面内容。
- 直接使用 `QBoxLayout` 可以选择 `LeftToRight`、`RightToLeft`、`TopToBottom` 或 `BottomToTop`，也可以在运行时通过 `setDirection()` 切换。

布局的方向同时决定 `addWidget()` 的排列方向和 stretch 的作用轴。水平布局的 stretch 影响宽度，垂直布局的 stretch 影响高度；它不会直接决定另一个轴上的尺寸。

### `stretch` 的真正用法

最推荐在添加项目时直接传入 stretch：

```cpp
auto *layout = new QHBoxLayout;
layout->addWidget(leftWidget, 1);
layout->addWidget(centerWidget, 2);
layout->addWidget(rightWidget, 1);
```

这里的 `1、2、1` 只表示相对比例，不表示 1 像素、2 像素、1 像素。假设扣除 margins、spacing 和各项目必要尺寸后还有 400 像素可分配，三个项目会按照 1:2:1 争取这部分空间，大致对应 100、200、100 像素；如果某个项目达到 maximumSize，剩余空间会重新分配，实际结果可能与简单除法不同。

`addStretch(n)` 添加的是一个没有可见内容、最小尺寸为 0 的可伸缩项目。它经常用来把按钮推到右侧或把一个控件居中：

```cpp
layout->addStretch(1);
layout->addWidget(button);       // 被推到右侧
```

```cpp
layout->addStretch(1);
layout->addWidget(button);
layout->addStretch(1);           // 两侧各分到一份剩余空间，button 居中
```

`setStretch(index, n)` 修改已有项目的比例，`setStretchFactor(widget, n)` 或 `setStretchFactor(layout, n)` 则通过对象查找项目。后两者只查当前布局的直接子项，不能直接修改孙布局里的控件。

### 对齐和 stretch 的区别

stretch 决定一个项目在主方向上分到多大的“单元格”；alignment 决定项目内容在这个单元格里怎么放。没有 alignment 时，普通控件通常会填满单元格；设置 `Qt::AlignLeft | Qt::AlignVCenter` 后，控件可以保持自己的 sizeHint，靠左并垂直居中。对齐不会把一个控件推到另一个项目后面，想要推开空间应使用 stretch。

例如，下面代码让按钮靠右，但按钮自身不会被拉宽：

```cpp
layout->addWidget(button, 0, Qt::AlignRight | Qt::AlignVCenter);
```

### margins、spacing 和固定空白

`setContentsMargins(left, top, right, bottom)` 控制布局和父控件边界之间的四条边距；`setSpacing(px)` 控制相邻项目之间的间隔。`setSpacing()` 不会改变外边距，`setContentsMargins()` 也不会改变项目之间的间隔。

`addSpacing(px)` 添加一个固定大小、不会主动伸展的空白项目，适合在某两个控件之间增加额外距离；`addStretch()` 添加的是会吸收剩余空间的空白项目。需要同时控制最小值、推荐值、最大值和 size policy 时，才使用 `QSpacerItem` 和 `addSpacerItem()`。

### `setSizeConstraint()` 约束的是父窗口

这是 `QLayout` 的 API，但使用盒式布局时经常一起出现。它控制布局所属的顶层/父控件在调整尺寸时采用什么约束：`SetFixedSize` 会让窗口适配布局的 sizeHint 后不能随意改变，`SetMinimumSize` 只限制最小尺寸，`SetMaximumSize` 只限制最大尺寸，`SetMinAndMaxSize` 同时限制两者。它不是把每个子控件固定成同一个大小；单个控件的大小应通过 size policy、minimum/maximum size 或 alignment 控制。

### 可运行示例

#### 完整示例：按比例分配一行控件

```cpp
#include <QApplication>
#include <QHBoxLayout>
#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include <QWidget>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QWidget window;
    auto *layout = new QHBoxLayout(&window);
    layout->setContentsMargins(16, 12, 16, 12);
    layout->setSpacing(8);

    auto *label = new QLabel(QStringLiteral("Name:"));
    auto *edit = new QLineEdit;
    auto *button = new QPushButton(QStringLiteral("Search"));

    layout->addWidget(label, 0, Qt::AlignVCenter);
    layout->addWidget(edit, 1);
    layout->addWidget(button, 0);

    window.resize(520, 80);
    window.show();
    return app.exec();
}
```

#### 完整示例：用 stretch 把按钮推到右侧

```cpp
#include <QApplication>
#include <QHBoxLayout>
#include <QPushButton>
#include <QWidget>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    QWidget window;
    auto *layout = new QHBoxLayout(&window);

    layout->addWidget(new QPushButton(QStringLiteral("Back")));
    layout->addStretch(1);
    layout->addWidget(new QPushButton(QStringLiteral("Cancel")));
    layout->addWidget(new QPushButton(QStringLiteral("OK")));

    window.show();
    return app.exec();
}
```

#### 完整示例：嵌套布局和运行时修改 stretch

```cpp
#include <QApplication>
#include <QHBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QVBoxLayout>
#include <QWidget>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    QWidget window;

    auto *root = new QVBoxLayout(&window);
    auto *top = new QHBoxLayout;
    auto *content = new QHBoxLayout;
    auto *left = new QLabel(QStringLiteral("Navigation"));
    auto *right = new QLabel(QStringLiteral("Content"));

    top->addWidget(new QLabel(QStringLiteral("Title")));
    top->addStretch(1);
    top->addWidget(new QPushButton(QStringLiteral("Settings")));

    content->addWidget(left, 1);
    content->addWidget(right, 3);
    content->setAlignment(left, Qt::AlignTop | Qt::AlignLeft);

    root->addLayout(top, 0);
    root->addLayout(content, 1);
    root->setContentsMargins(12, 12, 12, 12);

    window.resize(640, 360);
    window.show();
    return app.exec();
}
```

## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum Direction { LeftToRight, RightToLeft, TopToBottom, BottomToTop }`

### 公有函数

- `QBoxLayout(QBoxLayout::Direction dir, QWidget *parent = nullptr)`
- `virtual ~QBoxLayout()`
- `void addLayout(QLayout *layout, int stretch = 0)`
- `void addSpacerItem(QSpacerItem *spacerItem)`
- `void addSpacing(int size)`
- `void addStretch(int stretch = 0)`
- `void addStrut(int size)`
- `void addWidget(QWidget *widget, int stretch = 0, Qt::Alignment alignment = Qt::Alignment())`
- `QBoxLayout::Direction direction() const`
- `void insertItem(int index, QLayoutItem *item)`
- `void insertLayout(int index, QLayout *layout, int stretch = 0)`
- `void insertSpacerItem(int index, QSpacerItem *spacerItem)`
- `void insertSpacing(int index, int size)`
- `void insertStretch(int index, int stretch = 0)`
- `void insertWidget(int index, QWidget *widget, int stretch = 0, Qt::Alignment alignment = Qt::Alignment())`
- `void setDirection(QBoxLayout::Direction direction)`
- `void setStretch(int index, int stretch)`
- `bool setStretchFactor(QWidget *widget, int stretch)`
- `bool setStretchFactor(QLayout *layout, int stretch)`
- `int stretch(int index) const`

### 重实现的公有函数

- `virtual void addItem(QLayoutItem *item) override`
- `virtual int count() const override`
- `virtual Qt::Orientations expandingDirections() const override`
- `virtual bool hasHeightForWidth() const override`
- `virtual int heightForWidth(int w) const override`
- `virtual void invalidate() override`
- `virtual QLayoutItem * itemAt(int index) const override`
- `virtual QSize maximumSize() const override`
- `virtual int minimumHeightForWidth(int w) const override`
- `virtual QSize minimumSize() const override`
- `virtual void setGeometry(const QRect &r) override`
- `virtual void setSpacing(int spacing) override`
- `virtual QSize sizeHint() const override`
- `virtual int spacing() const override`
- `virtual QLayoutItem * takeAt(int index) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QBoxLayout::Direction`

**作用与语义：**

这种类型用于确定方块布局的方向。
- `QBoxLayout::LeftToRight`：`0`;从左到右水平排列。
- `QBoxLayout::RightToLeft`：`1`;从右向左水平排列。
- `QBoxLayout::TopToBottom`：`2`;从上到下垂直排列。
- `QBoxLayout::BottomToTop`：`3`;从下到上垂直排列。

### `[explicit] QBoxLayout::QBoxLayout(QBoxLayout::Direction dir, QWidget *parent = nullptr)`

**作用与语义：**

构建一个新的QBoxLayout，带有方向`dir`和父控件`parent`。
布局直接设置为`parent`的顶层布局。一个小部件只能有一个顶层布局。它由`QWidget::layout()`返回。

### `[virtual noexcept] QBoxLayout::~QBoxLayout()`

**作用与语义：**

破坏了这个盒子布局。
布局中的控件没有被破坏。

### `[override virtual] void QBoxLayout::addItem(QLayoutItem *item)`

**作用与语义：**

重实现自：`QLayout::addItem`（QLayoutItem *item）。
在子职业中实现以添加`item`。添加方式因子职业而异。
该函数通常不会在应用代码中调用。要向布局添加小部件，使用`addWidget()`函数;要添加子布局，使用相关`QLayout`子类提供的addLayout()函数。
注意：`item`的所有权转移到了布局上，删除它由布局负责。

### `void QBoxLayout::addLayout(QLayout *layout, int stretch = 0)`

**作用与语义：**

在盒子末端增加`layout`，并实现串行拉伸因子`stretch`。
`layout`成为盒子布局的子体。

### `void QBoxLayout::addSpacerItem(QSpacerItem *spacerItem)`

**作用与语义：**

这为这个盒子布局的结尾增加了一些`spacerItem`。
`spacerItem`的所有权转移到了这种布局。

### `void QBoxLayout::addSpacing(int size)`

**作用与语义：**

在这个框布局的末端添加一个不可拉伸的空间（`QSpacerItem`），大小为`size`。`QBoxLayout`提供默认的边距和间距。这个功能增加了额外的空间。

### `void QBoxLayout::addStretch(int stretch = 0)`

**作用与语义：**

在这个盒子布局的末端增加了一个可拉伸空间（`QSpacerItem`），最小尺寸和拉伸因子`stretch`为零。

### `void QBoxLayout::addStrut(int size)`

**作用与语义：**

限制盒子的垂直尺寸（例如箱体`LeftToRight`时高度）最小`size`。其他约束可能会增加限制。

### `void QBoxLayout::addWidget(QWidget *widget, int stretch = 0, Qt::Alignment alignment = Qt::Alignment())`

**作用与语义：**

为该盒式布局末端增加了`widget`，并增加了`stretch`的拉伸因子和对齐`alignment`。
拉伸因子仅适用于`QBoxLayout` `direction`，且相对于本`QBoxLayout`中其他箱子和小部件。伸缩因子较高的小部件和盒子增长更多。
如果拉伸因子为0，且`QBoxLayout`中没有其他元素的拉伸因子大于0，则空间根据涉及的每个控件的`QWidget::sizePolicy()`分布。
对齐方式由 `alignment` 指定。默认对齐为 0，这意味着小部件会填满整个单元格。
`widget`成为了`QLayout::parentWidget()`的孩子。

### `[override virtual] int QBoxLayout::count() const`

**作用与语义：**

重装：`QLayout::count()` const.
必须在子类中实现，以返回布局中的物品数量。

### `QBoxLayout::Direction QBoxLayout::direction() const`

**作用与语义：**

返回盒子的方向。`addWidget()`和`addSpacing()`朝这个方向工作;拉伸方向向此延伸。

### `[override virtual] Qt::Orientations QBoxLayout::expandingDirections() const`

**作用与语义：**

重装：`QLayout::expandingDirections()` const.

### `[override virtual] bool QBoxLayout::hasHeightForWidth() const`

**作用与语义：**

重装：`QLayoutItem::hasHeightForWidth()` const.
如果该布局的首选高度取决于宽度，则返回`true`;否则返回`false`。默认实现返回false。
在支持宽度高度的布局管理器中重新实现这个功能。

### `[override virtual] int QBoxLayout::heightForWidth(int w) const`

**作用与语义：**

重装：`QLayoutItem::heightForWidth`（int） const.
返回该布局项的首选高度，基于宽度，但默认实现中未使用宽度。
默认实现返回 -1，表示首选高度与项目宽度无关。使用函数 `hasHeightForWidth()` 通常比调用该函数并测试 -1 快得多。
在支持宽度高度的布局管理器中重新实现该函数。典型的实现如下：
强烈建议缓存;没有缓存，布局将耗费指数级时间。

### `void QBoxLayout::insertItem(int index, QLayoutItem *item)`

**作用与语义：**

在该框布局中插入`item`，位置`index`。索引必须为负或范围在0到`count()`之间，包括。如果`index`为负或`count()`，则该项会加在末尾。
`item`的所有权转移到了这种布局。

### `void QBoxLayout::insertLayout(int index, QLayout *layout, int stretch = 0)`

**作用与语义：**

插入物在位置`index` `layout`，拉伸因子为`stretch`。如果`index`为负，则在末尾添加布局。
`layout`成为盒子布局的子体。

### `void QBoxLayout::insertSpacerItem(int index, QSpacerItem *spacerItem)`

**作用与语义：**

插入物`spacerItem`位置为`index`，最小尺寸和拉伸因子均为零。如果`index`为负，则在末端加空间。
`spacerItem`的所有权转移到了该布局。

### `void QBoxLayout::insertSpacing(int index, int size)`

**作用与语义：**

在位置`index`插入一个不可伸缩的空间（`QSpacerItem`），大小为`size`。如果`index`为负，则在末尾加空间。
框布局默认有边距和间距。这个功能增加了额外的空间。

### `void QBoxLayout::insertStretch(int index, int stretch = 0)`

**作用与语义：**

在位置`index`插入一个可拉伸空间（`QSpacerItem`），最小大小为零，拉伸因子为`stretch`。如果`index`为负，则在末端加空间。

### `void QBoxLayout::insertWidget(int index, QWidget *widget, int stretch = 0, Qt::Alignment alignment = Qt::Alignment())`

**作用与语义：**

插入点在位置`index` `widget`，拉伸因子为`stretch`，对齐`alignment`。如果`index`为负，则在末尾添加小部件。
拉伸因子仅适用于`QBoxLayout` `direction`，且相对于该`QBoxLayout`中的其他盒子和控件。拉伸因子较高的控件和盒子增长更多。
如果拉伸因子为0，且`QBoxLayout`中没有其他物品的拉伸因子大于零，则空间根据涉及的每个控件的`QWidget::sizePolicy()`分配。
对齐由 `alignment` 指定。默认对齐为 0，这意味着小部件会填满整个单元格。
`widget`成为`QLayout::parentWidget()`的孩子。

### `[override virtual] void QBoxLayout::invalidate()`

**作用与语义：**

重装：`QLayout::invalidate()`。
重置缓存信息。

### `[override virtual] QLayoutItem *QBoxLayout::itemAt(int index) const`

**作用与语义：**

重实现自：`QLayout::itemAt`（int index）const.
必须在子类中实现以返回`index`的布局项。如果没有这样的项，函数必须返回`nullptr`。项编号从0依次排列。如果一个项被删除，其他项将被重新编号。
该函数可用于遍历布局。以下代码将为小部件布局结构中的每个布局项绘制一个矩形。

### `[override virtual] QSize QBoxLayout::maximumSize() const`

**作用与语义：**

重装：`QLayout::maximumSize()` const.

### `[override virtual] int QBoxLayout::minimumHeightForWidth(int w) const`

**作用与语义：**

重实现自：`QLayoutItem::minimumHeightForWidth`（内性 w） const.
返回该控件在给定宽度下所需的最小高度，`w`。默认实现则返回 `heightForWidth`（`w`）。

### `[override virtual] QSize QBoxLayout::minimumSize() const`

**作用与语义：**

重装：`QLayout::minimumSize()` const.

### `void QBoxLayout::setDirection(QBoxLayout::Direction direction)`

**作用与语义：**

将布局方向设置为`direction`。

### `[override virtual] void QBoxLayout::setGeometry(const QRect &r)`

**作用与语义：**

重装：`QLayout::setGeometry`（const QRect & r）。

### `[override virtual] void QBoxLayout::setSpacing(int spacing)`

**作用与语义：**

重新实现了属性的访问函数：`QLayout::spacing`。
重新实现`QLayout::setSpacing()`。将间距属性设置为`spacing`。

### `void QBoxLayout::setStretch(int index, int stretch)`

**作用与语义：**

将拉伸因子设定在位置`index`。为`stretch`。

### `bool QBoxLayout::setStretchFactor(QWidget *widget, int stretch)`

**作用与语义：**

将 `widget` 的拉伸因子设置为 `stretch`，若在此布局中找到 `widget`则返回 true（不包括子布局）;否则返回 `false`。

### `bool QBoxLayout::setStretchFactor(QLayout *layout, int stretch)`

**作用与语义：**

将布局`layout`的拉伸因子设置为`stretch`，如果在该布局中发现`layout`（不包括子布局），返回`true`;否则返回`false`。

### `[override virtual] QSize QBoxLayout::sizeHint() const`

**作用与语义：**

重装：`QLayoutItem::sizeHint()` const.
在子类中实现，以返回该物品的首选大小。

### `[override virtual] int QBoxLayout::spacing() const`

**作用与语义：**

重新实现了属性访问函数：`QLayout::spacing`。
重新实现`QLayout::spacing()`。如果间距属性有效，则返回该值。否则，计算并返回间距属性的值。由于控件中的布局间距依赖于样式，如果父组件是控件，它会查询样式的（水平或垂直）间距。否则，父节点是布局，它会查询父布局的间距()。

### `int QBoxLayout::stretch(int index) const`

**作用与语义：**

返回位置`index`的拉伸因子。

### `[override virtual] QLayoutItem *QBoxLayout::takeAt(int index)`

**作用与语义：**

重实现自：`QLayout::takeAt`（整数索引）。
必须在子类中实现，以从布局中移除`index`的布局项并返回该项。如果没有这样的项，函数必须什么都不做，返回0。项编号从0开始依次编号。如果一个项被移除，其他项将被重新编号。
以下代码片段展示了一种安全移除所有布局物品的方法：

## 6. 深入实践与常见坑

### 生命周期和资源边界

顶层布局可以在构造时绑定到 QWidget，也可以通过 `setLayout()` 安装；嵌套布局加入父布局后所有权交给父布局。布局析构不会自动销毁普通 QWidget，动态移除项目时要分别处理控件、子布局和 spacer。

### 状态和错误边界

布局的项目索引会随着 add、insert、remove 和 takeAt 改变；索引既包括控件，也包括子布局、固定空白和 stretch。修改项目或尺寸参数后 Qt 会使布局失效并重新计算。

### 线程边界

布局只应在 GUI 线程操作，因为它直接改变 QWidget 几何和可见界面。布局系统不负责业务线程同步，也不会把手动的跨线程控件访问变安全。

### 最容易出现的错误

`stretch` 是比例，不是像素；`setStretch()` 的 index 是布局项目索引，不是控件编号；`setStretchFactor()` 只查找当前这一层；spacing 不等于外边距；不要给已经交给布局管理的控件反复调用 `setGeometry()`。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QBoxLayout` 所属机制类型：布局管理机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
