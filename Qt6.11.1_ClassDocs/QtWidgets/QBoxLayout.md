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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 36 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QBoxLayout::Direction`

**API 类别：** 成员类型说明

**中文解读：** `QBoxLayout::Direction` 决定项目排列方向：`LeftToRight`、`RightToLeft`、`TopToBottom`、`BottomToTop`。水平和垂直方向不仅改变视觉顺序，也决定 stretch 沿宽度还是高度分配。

**签名拆解：**

- 属性类型：`:Direction`。
- 属性名：`QBoxLayout`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QBoxLayout::QBoxLayout(QBoxLayout::Direction dir, QWidget *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** `QBoxLayout(QBoxLayout::Direction dir, QWidget *parent = nullptr)` 中，`dir` 决定排列方向：`LeftToRight` 从左到右，`RightToLeft` 从右到左，`TopToBottom` 从上到下，`BottomToTop` 从下到上。`parent` 只有在这个布局直接作为某个 QWidget 的顶层布局时才传入；嵌套布局通常先无父对象创建，再用父布局的 `addLayout()` 接管它。实际开发优先写 `QHBoxLayout` 或 `QVBoxLayout`，因为它们已经固定了方向。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `dir`：类型为 `QBoxLayout::Direction`。没有默认值，调用时必须提供。传入 `QBoxLayout::Direction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `parent`：类型为 `QWidget *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QBoxLayout::~QBoxLayout()`

**API 类别：** 成员函数说明

**中文解读：** 析构布局时，布局项目和子布局会按 Qt 的所有权规则释放；布局管理的普通 `QWidget` 不会因为布局析构而自动销毁。若只是移除布局，不要误以为控件也被删除；控件的新父对象和生命周期仍需明确。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QBoxLayout::addItem(QLayoutItem *item)`

**API 类别：** 成员函数说明

**中文解读：** `addItem(QLayoutItem *item)` 把一个底层布局项目追加到末尾，项目可以包着 widget、子布局或 spacer。普通业务代码通常使用 `addWidget()`、`addLayout()`、`addSpacing()` 或 `addStretch()`，因为这些函数会明确表达项目类型和参数。传入的 item 所有权交给布局。

**签名拆解：**

- 返回值：`void`。
- 参数 `item`：类型为 `QLayoutItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QBoxLayout::addLayout(QLayout *layout, int stretch = 0)`

**API 类别：** 成员函数说明

**中文解读：** `addLayout(QLayout *layout, int stretch = 0)` 把另一个布局作为一个项目追加。子布局的所有控件仍由子布局管理，而父布局只分配这个子布局整体的矩形。`stretch` 作用在子布局整体上。例如外层垂直布局中，上方工具栏布局设为 0、下方编辑区布局设为 1，就能让编辑区吸收多余高度。添加后所有权交给父布局，不要重复把同一个布局加入多个父布局。

**签名拆解：**

- 返回值：`void`。
- 参数 `layout`：类型为 `QLayout *`。没有默认值，调用时必须提供。参与操作的布局对象。通常表示整个子布局的几何区域和所有权，不等于子布局里的某一个控件。
- 参数 `stretch`：类型为 `int`。默认值为 `0`。伸展比例或权重，不是像素值。它通常只影响剩余空间如何分配，并受最小/最大尺寸和 size policy 限制。

**正确调用组合：** 通常与嵌套布局和父布局 stretch 一起使用；父布局分配子布局整体空间，子布局再管理自己的项目。

### `void QBoxLayout::addSpacerItem(QSpacerItem *spacerItem)`

**API 类别：** 成员函数说明

**中文解读：** `addSpacerItem(QSpacerItem *spacerItem)` 添加自定义 spacer。与 `addStretch()` 和 `addSpacing()` 相比，`QSpacerItem` 可以分别指定宽度、最小高度、最大尺寸和 `QSizePolicy`。添加后所有权交给布局；除非确实需要复杂 size policy，否则优先使用语义更清楚的 `addStretch()` 或 `addSpacing()`。

**签名拆解：**

- 返回值：`void`。
- 参数 `spacerItem`：类型为 `QSpacerItem *`。没有默认值，调用时必须提供。传入 `QSpacerItem *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QBoxLayout::addSpacing(int size)`

**API 类别：** 成员函数说明

**中文解读：** `addSpacing(int size)` 添加固定大小的空白，`size` 是沿布局主方向的像素数。它不会随着窗口变大而吸收剩余空间，也不会代替 `setSpacing()` 设置所有相邻项目的间隔。它适合表达某一个位置需要额外留白的关系。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `int`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QBoxLayout::addStretch(int stretch = 0)`

**API 类别：** 成员函数说明

**中文解读：** `addStretch(int stretch = 0)` 添加一个可伸缩空白。参数是这个空白项目的 stretch factor，默认 0；当布局中没有其他正 stretch 时，Qt 还会结合 spacer 的 size policy 分配空间。为了明确表达“这个空白按比例吸收剩余空间”，通常写 `addStretch(1)`。`addStretch(1); addWidget(button);` 把按钮推到末端；两侧各加一个相同 stretch 则可以居中。

**签名拆解：**

- 返回值：`void`。
- 参数 `stretch`：类型为 `int`。默认值为 `0`。伸展比例或权重，不是像素值。它通常只影响剩余空间如何分配，并受最小/最大尺寸和 size policy 限制。

**正确调用组合：** 通常用来吸收剩余空间、推开项目或配合两侧相同 stretch 实现居中。

### `void QBoxLayout::addStrut(int size)`

**API 类别：** 成员函数说明

**中文解读：** `addStrut(int size)` 设置一条不可见的最小尺寸约束，作用在布局的交叉方向：水平盒式布局影响最小高度，垂直盒式布局影响最小宽度。它不是主方向上的空白，也不是设置控件固定尺寸；只有需要让一行/一列至少达到某个交叉方向尺寸时才使用。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `int`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QBoxLayout::addWidget(QWidget *widget, int stretch = 0, Qt::Alignment alignment = Qt::Alignment())`

**API 类别：** 成员函数说明

**中文解读：** `addWidget(QWidget *widget, int stretch = 0, Qt::Alignment alignment = {})` 把控件追加到末尾。`widget` 是要管理的控件；`stretch` 是主方向的相对伸展比例，默认 0；`alignment` 是控件在分配单元格内的对齐方式，默认空 alignment，通常表示允许控件填满单元格。常用写法是 `addWidget(edit, 1)` 让输入框吸收剩余宽度，按钮使用默认 0 保持接近推荐尺寸。控件会成为布局父控件中的子控件，不要再手动管理同一几何区域。

**签名拆解：**

- 返回值：`void`。
- 参数 `widget`：类型为 `QWidget *`。没有默认值，调用时必须提供。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。
- 参数 `stretch`：类型为 `int`。默认值为 `0`。伸展比例或权重，不是像素值。它通常只影响剩余空间如何分配，并受最小/最大尺寸和 size policy 限制。
- 参数 `alignment`：类型为 `Qt::Alignment`。默认值为 `Qt::Alignment()`。对齐标志的组合，例如 `Qt::AlignLeft | Qt::AlignVCenter`；它描述内容在已分配区域中的位置，不负责分配剩余空间。

**正确调用组合：** 通常与 `setContentsMargins()`、`setSpacing()` 和 stretch 一起使用；stretch 分配主方向剩余空间，alignment 控制控件在自身区域中的位置。

### `[override virtual] int QBoxLayout::count() const`

**API 类别：** 成员函数说明

**中文解读：** `count()` 返回当前布局项目数量。这里的项目不仅是可见控件，还包括子布局、固定空白和 stretch；因此它是遍历 `itemAt(index)`、`takeAt(index)` 或判断 `setStretch(index, ...)` 索引范围的依据。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBoxLayout::Direction QBoxLayout::direction() const`

**API 类别：** 成员函数说明

**中文解读：** `setDirection(Direction direction)` 运行时改变排列方向，`direction()` 读取当前方向。方向改变后，项目仍是同一批项目，但视觉顺序和 stretch 的作用轴会改变；例如从 `LeftToRight` 切到 `TopToBottom` 后，同样的 stretch 会从分配宽度变成分配高度。

**签名拆解：**

- 返回值：`QBoxLayout::Direction`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] Qt::Orientations QBoxLayout::expandingDirections() const`

**API 类别：** 成员函数说明

**中文解读：** `expandingDirections()` 告诉 Qt 这个布局愿意在哪些方向扩展。盒式布局的主方向通常可以扩展，具体结果还会综合子项目的 size policy；它主要供布局系统计算尺寸，不是设置控件大小的业务 API。

**签名拆解：**

- 返回值：`Qt::Orientations`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QBoxLayout::hasHeightForWidth() const`

**API 类别：** 成员函数说明

**中文解读：** `hasHeightForWidth()` 用于判断布局中的项目是否需要根据宽度计算高度，例如自动换行文本。它由布局系统在尺寸计算时使用，应用代码通常不需要手动调用；不要把它当成普通控件是否可见的判断。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] int QBoxLayout::heightForWidth(int w) const`

**API 类别：** 成员函数说明

**中文解读：** `heightForWidth(int w)` 根据给定宽度计算布局需要的高度，`w` 是布局宽度。它通常由 Qt 在布局计算过程中调用，用来支持 word wrap 等高度依赖宽度的控件；不要在普通业务代码中用它替代设置布局。

**签名拆解：**

- 返回值：`int`。
- 参数 `w`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QBoxLayout::insertItem(int index, QLayoutItem *item)`

**API 类别：** 成员函数说明

**中文解读：** `insertItem(int index, QLayoutItem *item)` 在指定位置插入一个布局项目。`index` 是包括控件、子布局和 spacer 在内的项目索引；所有权转交给布局。普通代码优先使用 `insertWidget()`、`insertLayout()`、`insertSpacing()` 或 `insertStretch()`，因为这些函数的参数更明确。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `item`：类型为 `QLayoutItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QBoxLayout::insertLayout(int index, QLayout *layout, int stretch = 0)`

**API 类别：** 成员函数说明

**中文解读：** 插入版本的第一个参数 `index` 是项目位置，项目包括控件、子布局、固定空白和 stretch，不能只按可见控件计数。负数或等于 `count()` 会追加到末尾。插入控件时后两个参数仍分别是 stretch 和 alignment；插入布局时最后一个参数是子布局整体的 stretch。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `layout`：类型为 `QLayout *`。没有默认值，调用时必须提供。参与操作的布局对象。通常表示整个子布局的几何区域和所有权，不等于子布局里的某一个控件。
- 参数 `stretch`：类型为 `int`。默认值为 `0`。伸展比例或权重，不是像素值。它通常只影响剩余空间如何分配，并受最小/最大尺寸和 size policy 限制。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QBoxLayout::insertSpacerItem(int index, QSpacerItem *spacerItem)`

**API 类别：** 成员函数说明

**中文解读：** `insertSpacerItem(int index, QSpacerItem *spacerItem)` 在指定位置插入自定义 spacer。`index` 负数或等于 `count()` 时追加到末尾；添加后 spacer 的所有权交给布局。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `spacerItem`：类型为 `QSpacerItem *`。没有默认值，调用时必须提供。传入 `QSpacerItem *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QBoxLayout::insertSpacing(int index, int size)`

**API 类别：** 成员函数说明

**中文解读：** `insertSpacing(int index, int size)` 在指定位置插入固定空白。`size` 是沿布局主方向的像素大小；它不会吸收窗口变大后产生的剩余空间。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `size`：类型为 `int`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QBoxLayout::insertStretch(int index, int stretch = 0)`

**API 类别：** 成员函数说明

**中文解读：** `insertStretch(int index, int stretch = 0)` 在指定位置插入可伸缩空白。`stretch` 是相对权重；想让它吸收剩余空间通常传入正数，例如 `insertStretch(1, 1)`。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `stretch`：类型为 `int`。默认值为 `0`。伸展比例或权重，不是像素值。它通常只影响剩余空间如何分配，并受最小/最大尺寸和 size policy 限制。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QBoxLayout::insertWidget(int index, QWidget *widget, int stretch = 0, Qt::Alignment alignment = Qt::Alignment())`

**API 类别：** 成员函数说明

**中文解读：** 插入版本的第一个参数 `index` 是项目位置，项目包括控件、子布局、固定空白和 stretch，不能只按可见控件计数。负数或等于 `count()` 会追加到末尾。插入控件时后两个参数仍分别是 stretch 和 alignment；插入布局时最后一个参数是子布局整体的 stretch。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `widget`：类型为 `QWidget *`。没有默认值，调用时必须提供。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。
- 参数 `stretch`：类型为 `int`。默认值为 `0`。伸展比例或权重，不是像素值。它通常只影响剩余空间如何分配，并受最小/最大尺寸和 size policy 限制。
- 参数 `alignment`：类型为 `Qt::Alignment`。默认值为 `Qt::Alignment()`。对齐标志的组合，例如 `Qt::AlignLeft | Qt::AlignVCenter`；它描述内容在已分配区域中的位置，不负责分配剩余空间。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QBoxLayout::invalidate()`

**API 类别：** 成员函数说明

**中文解读：** `invalidate()` 清除布局缓存，让 Qt 在下一次布局更新时重新计算尺寸和几何位置。改变项目、margin、spacing、stretch 或子控件尺寸提示后 Qt 通常会自动触发更新，只有自定义布局或特殊缓存场景才需要关注它。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QLayoutItem *QBoxLayout::itemAt(int index) const`

**API 类别：** 成员函数说明

**中文解读：** `itemAt(int index)` 按索引读取布局项目，但不移除它。返回的 `QLayoutItem` 可能代表 widget、子 layout 或 spacer，读取前先判断 `item->widget()`、`item->layout()` 和 `item->spacerItem()` 哪一个有效；索引越界返回空指针。

**签名拆解：**

- 返回值：`QLayoutItem *`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QSize QBoxLayout::maximumSize() const`

**API 类别：** 成员函数说明

**中文解读：** `maximumSize()` 返回布局综合子项目最大尺寸后允许的最大尺寸。某个控件达到 maximumSize 后，即使它的 stretch 很大也不会继续变大，多余空间会由其他可扩展项目处理。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] int QBoxLayout::minimumHeightForWidth(int w) const`

**API 类别：** 成员函数说明

**中文解读：** `minimumHeightForWidth(int w)` 根据宽度 `w` 计算布局所需的最小高度，主要用于布局中存在自动换行或其他宽度影响高度的控件时。它是 Qt 尺寸计算过程的一部分，普通代码不应拿它代替 `setMinimumHeight()`。

**签名拆解：**

- 返回值：`int`。
- 参数 `w`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QSize QBoxLayout::minimumSize() const`

**API 类别：** 成员函数说明

**中文解读：** `minimumSize()` 返回布局根据 margins、spacing、子项目最小尺寸和 size policy 计算出的最小尺寸。窗口被缩小时，这个结果会影响窗口还能缩到多小；它不是单独设置某个控件最小尺寸的接口。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QBoxLayout::setDirection(QBoxLayout::Direction direction)`

**API 类别：** 成员函数说明

**中文解读：** `setDirection(Direction direction)` 运行时改变排列方向，`direction()` 读取当前方向。方向改变后，项目仍是同一批项目，但视觉顺序和 stretch 的作用轴会改变；例如从 `LeftToRight` 切到 `TopToBottom` 后，同样的 stretch 会从分配宽度变成分配高度。

**签名拆解：**

- 返回值：`void`。
- 参数 `direction`：类型为 `QBoxLayout::Direction`。没有默认值，调用时必须提供。方向枚举，决定排列、遍历或坐标增长方向；要结合该类定义的枚举值判断实际方向。

**正确调用组合：** 改变方向后 stretch 的作用轴也会改变；水平变垂直时，同一比例从分配宽度变为分配高度。

### `[override virtual] void QBoxLayout::setGeometry(const QRect &r)`

**API 类别：** 成员函数说明

**中文解读：** `setGeometry(const QRect &r)` 是布局系统用来分配自身矩形的虚函数。`r` 是 Qt 计算出的布局区域；普通代码不要手动调用它，也不要在窗口 resize 中自己调用它来摆放子控件，应该修改布局参数或控件的尺寸策略。

**签名拆解：**

- 返回值：`void`。
- 参数 `r`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QBoxLayout::setSpacing(int spacing)`

**API 类别：** 成员函数说明

**中文解读：** `setSpacing(int spacing)` 设置相邻项目之间的统一间隔，`spacing()` 读取实际值。它只影响相邻项目之间的距离，不影响布局外边距；嵌套布局未显式设置时，间距可能继承父布局或由 style 决定。`addSpacing()` 是某一个位置的额外固定空白，两者不要混为一谈。

**签名拆解：**

- 返回值：`void`。
- 参数 `spacing`：类型为 `int`。没有默认值，调用时必须提供。相邻项目之间的间隔，通常以像素表示；它通常不等于外边距。

**正确调用组合：** 与 `setContentsMargins()` 配合控制内部间隔和外部边距，不能用一个替代另一个。

### `void QBoxLayout::setStretch(int index, int stretch)`

**API 类别：** 成员函数说明

**中文解读：** `setStretch(int index, int stretch)` 修改指定项目的 stretch。`index` 必须对应当前布局中的项目索引，`stretch` 是非负的相对权重。布局中有三个控件时，只有控件项目恰好位于 0、1、2 才能这样写；如果中间插入了 `addSpacing()` 或 `addStretch()`，索引会随项目改变。对于不容易维护的索引，使用 `setStretchFactor(widget, stretch)` 更安全。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `stretch`：类型为 `int`。没有默认值，调用时必须提供。伸展比例或权重，不是像素值。它通常只影响剩余空间如何分配，并受最小/最大尺寸和 size policy 限制。

**正确调用组合：** 要结合 `count()` 和 `stretch(index)` 使用，注意 index 包括 spacer 和子布局。

### `bool QBoxLayout::setStretchFactor(QWidget *widget, int stretch)`

**API 类别：** 成员函数说明

**中文解读：** `setStretchFactor(QWidget *widget, int stretch)` 和 `setStretchFactor(QLayout *layout, int stretch)` 通过对象设置直接子项的 stretch，并返回是否找到该对象。返回 `false` 通常表示对象不在当前布局这一层，或者已经被移除；它不会递归搜索子布局。`stretch` 仍是比例，不是宽度。

**签名拆解：**

- 返回值：`bool`。
- 参数 `widget`：类型为 `QWidget *`。没有默认值，调用时必须提供。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。
- 参数 `stretch`：类型为 `int`。没有默认值，调用时必须提供。伸展比例或权重，不是像素值。它通常只影响剩余空间如何分配，并受最小/最大尺寸和 size policy 限制。

**正确调用组合：** 要结合 `count()` 和 `stretch(index)` 使用，注意 index 包括 spacer 和子布局。

### `bool QBoxLayout::setStretchFactor(QLayout *layout, int stretch)`

**API 类别：** 成员函数说明

**中文解读：** `setStretchFactor(QWidget *widget, int stretch)` 和 `setStretchFactor(QLayout *layout, int stretch)` 通过对象设置直接子项的 stretch，并返回是否找到该对象。返回 `false` 通常表示对象不在当前布局这一层，或者已经被移除；它不会递归搜索子布局。`stretch` 仍是比例，不是宽度。

**签名拆解：**

- 返回值：`bool`。
- 参数 `layout`：类型为 `QLayout *`。没有默认值，调用时必须提供。参与操作的布局对象。通常表示整个子布局的几何区域和所有权，不等于子布局里的某一个控件。
- 参数 `stretch`：类型为 `int`。没有默认值，调用时必须提供。伸展比例或权重，不是像素值。它通常只影响剩余空间如何分配，并受最小/最大尺寸和 size policy 限制。

**正确调用组合：** 要结合 `count()` 和 `stretch(index)` 使用，注意 index 包括 spacer 和子布局。

### `[override virtual] QSize QBoxLayout::sizeHint() const`

**API 类别：** 成员函数说明

**中文解读：** `sizeHint()` 返回布局希望占用的推荐尺寸，它来自子项目的 sizeHint、spacing 和 margins。它是窗口初始大小和 `SetFixedSize` 等约束的重要输入，但不是强制尺寸；窗口仍可在约束允许时调整。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] int QBoxLayout::spacing() const`

**API 类别：** 成员函数说明

**中文解读：** `setSpacing(int spacing)` 设置相邻项目之间的统一间隔，`spacing()` 读取实际值。它只影响相邻项目之间的距离，不影响布局外边距；嵌套布局未显式设置时，间距可能继承父布局或由 style 决定。`addSpacing()` 是某一个位置的额外固定空白，两者不要混为一谈。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QBoxLayout::stretch(int index) const`

**API 类别：** 成员函数说明

**中文解读：** `stretch(int index) const` 返回项目当前的 stretch factor，可用来检查动态调整是否生效。`index` 与 `setStretch()` 使用同一套项目索引，访问前先确认 `0 <= index < count()`。

**签名拆解：**

- 返回值：`int`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QLayoutItem *QBoxLayout::takeAt(int index)`

**API 类别：** 成员函数说明

**中文解读：** `removeWidget(widget)` 只把控件从布局关系中移除，通常不会销毁控件；移除后要自己决定它的新父对象和生命周期。`takeAt(index)` 取出项目并把所有权交还给调用者，取出的 `QLayoutItem` 可能包着 widget、子布局或 spacer，需要分别通过 `widget()`、`layout()`、`spacerItem()` 处理。

**签名拆解：**

- 返回值：`QLayoutItem *`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### 常用继承 API

#### `QLayout::setContentsMargins`

`setContentsMargins(int left, int top, int right, int bottom)` 的四个参数分别是左、上、右、下边距，单位是像素。它作用在布局外框，不会改变控件之间的 spacing。传入 0 可以让内容贴近父控件边缘，但通常要考虑平台风格和可读性；不手动设置时，Qt 可能使用 style 提供的默认值。

#### `QLayout::setSpacing / spacing`

`setSpacing(int spacing)` 设置相邻项目之间的统一间隔，`spacing()` 读取实际值。它只影响相邻项目之间的距离，不影响布局外边距；嵌套布局未显式设置时，间距可能继承父布局或由 style 决定。`addSpacing()` 是某一个位置的额外固定空白，两者不要混为一谈。

#### `QLayout::setAlignment`

`setAlignment(QWidget *widget, Qt::Alignment alignment)` 或 `setAlignment(QLayout *layout, Qt::Alignment alignment)` 设置直接子项目在其分配单元格中的对齐方式。常用组合是 `Qt::AlignLeft | Qt::AlignVCenter`、`Qt::AlignHCenter`、`Qt::AlignRight`。alignment 解决“项目在自己的格子里怎么放”，stretch 解决“项目的格子分多大”，需要两者配合时先分配空间再控制内容对齐。

#### `QLayout::setSizeConstraint`

`setSizeConstraint(QLayout::SizeConstraint constraint)` 控制布局所属窗口的尺寸约束。`SetDefaultConstraint` 使用默认行为；`SetFixedSize` 让窗口按布局推荐尺寸固定；`SetMinimumSize` 只设置最小尺寸；`SetMaximumSize` 只设置最大尺寸；`SetMinAndMaxSize` 同时设置最小和最大尺寸；`SetNoConstraint` 不由布局施加约束。它不替代 `QWidget::setMinimumSize()`，也不改变 stretch 比例。

#### `removeWidget / takeAt`

`removeWidget(widget)` 只把控件从布局关系中移除，通常不会销毁控件；移除后要自己决定它的新父对象和生命周期。`takeAt(index)` 取出项目并把所有权交还给调用者，取出的 `QLayoutItem` 可能包着 widget、子布局或 spacer，需要分别通过 `widget()`、`layout()`、`spacerItem()` 处理。

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
