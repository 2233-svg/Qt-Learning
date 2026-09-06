# QPalette

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QPalette` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QPalette>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum ColorGroup { Disabled, Active, Inactive, Normal }`
- `enum ColorRole { Window, WindowText, Base, AlternateBase, ToolTipBase, …, NoRole }`

### 公有函数

- `QPalette()`
- `QPalette(Qt::GlobalColor button)`
- `QPalette(const QColor &button)`
- `QPalette(const QColor &button, const QColor &window)`
- `QPalette(const QBrush &windowText, const QBrush &button, const QBrush &light, const QBrush &dark, const QBrush &mid, const QBrush &text, const QBrush &bright_text, const QBrush &base, const QBrush &window)`
- `QPalette(const QPalette &p)`
- `QPalette(QPalette &&other)`
- `~QPalette()`
- `(since 6.6) const QBrush & accent() const`
- `const QBrush & alternateBase() const`
- `const QBrush & base() const`
- `const QBrush & brightText() const`
- `const QBrush & brush(QPalette::ColorGroup group, QPalette::ColorRole role) const`
- `const QBrush & brush(QPalette::ColorRole role) const`
- `const QBrush & button() const`
- `const QBrush & buttonText() const`
- `qint64 cacheKey() const`
- `const QColor & color(QPalette::ColorGroup group, QPalette::ColorRole role) const`
- `const QColor & color(QPalette::ColorRole role) const`
- `QPalette::ColorGroup currentColorGroup() const`
- `const QBrush & dark() const`
- `const QBrush & highlight() const`
- `const QBrush & highlightedText() const`
- `bool isBrushSet(QPalette::ColorGroup cg, QPalette::ColorRole cr) const`
- `bool isCopyOf(const QPalette &p) const`
- `bool isEqual(QPalette::ColorGroup cg1, QPalette::ColorGroup cg2) const`
- `const QBrush & light() const`
- `const QBrush & link() const`
- `const QBrush & linkVisited() const`
- `const QBrush & mid() const`
- `const QBrush & midlight() const`
- `const QBrush & placeholderText() const`
- `QPalette resolve(const QPalette &other) const`
- `void setBrush(QPalette::ColorRole role, const QBrush &brush)`
- `void setBrush(QPalette::ColorGroup group, QPalette::ColorRole role, const QBrush &brush)`
- `void setColor(QPalette::ColorGroup group, QPalette::ColorRole role, const QColor &color)`
- `void setColor(QPalette::ColorRole role, const QColor &color)`
- `void setColorGroup(QPalette::ColorGroup cg, const QBrush &windowText, const QBrush &button, const QBrush &light, const QBrush &dark, const QBrush &mid, const QBrush &text, const QBrush &bright_text, const QBrush &base, const QBrush &window)`
- `void setCurrentColorGroup(QPalette::ColorGroup cg)`
- `const QBrush & shadow() const`
- `void swap(QPalette &other)`
- `const QBrush & text() const`
- `const QBrush & toolTipBase() const`
- `const QBrush & toolTipText() const`
- `const QBrush & window() const`
- `const QBrush & windowText() const`
- `operator QVariant() const`
- `bool operator!=(const QPalette &p) const`
- `QPalette & operator=(QPalette &&other)`
- `QPalette & operator=(const QPalette &p)`
- `(since 6.6) bool operator==(const QPalette &p) const`

### 相关非成员函数

- `QDataStream & operator<<(QDataStream &s, const QPalette &p)`
- `QDataStream & operator>>(QDataStream &s, QPalette &p)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QPalette::ColorRole`

**作用与语义：**

ColorRole 枚举定义了当前图形界面中使用的不同符号色彩角色。
核心角色包括：
- `QPalette::Window`：`10`;一种通用的背景色。
- `QPalette::WindowText`：`0`;一种通用的前景色。
- `QPalette::Base`：`9`;主要用作文本输入小部件的背景色，但也可用于其他绘画，如组合框下拉列表的背景和工具栏手柄。通常为白色或其他浅色。
- `QPalette::AlternateBase`：`16`;在行颜色交替的视图中用作备用背景色（参见 `QAbstractItemView::setAlternatingRowColors()`）。
- `QPalette::ToolTipBase`：`18`;用作`QToolTip`和`QWhatsThis`的背景色。工具提示使用`QPalette`的非活跃颜色组，因为工具提示不是活动窗口。
- `QPalette::ToolTipText`：`19`;用作`QToolTip`和`QWhatsThis`的前景色。工具提示使用`QPalette`的非激活颜色组，因为工具提示不是活动窗口。
- `QPalette::PlaceholderText`：`20`;用作各种文本输入控件的占位颜色。该枚举值在Qt 5.12中引入
- `QPalette::Text`：`6`;与`Base`一起使用的前景色。这通常与`WindowText`相同，因此必须与`Window`和`Base`提供良好的对比。
- `QPalette::Button`：`1`;按钮的背景色。由于某些风格要求按钮背景色不同，这种背景可以与`Window`不同。
- `QPalette::ButtonText`：`8`;与`Button`色搭配的前景色。
- `QPalette::BrightText`：`7`;与`WindowText`非常不同的文本颜色，与例如`Dark`形成良好对比。通常用于需要绘制的文本，比如按压按钮上，`Text`或`WindowText`会造成对比度较差的。注意，文本颜色不仅用于文字;文本颜色通常用于文本，但也相当常见地将文本颜色角色用于行、图标等。
有些颜色角色主要用于3D斜角和阴影效果。这些通常都源自`Window`，并以依赖这种关系的方式使用。例如，按钮依赖它来使斜角看起来更有吸引力，而Motif滚动条则依赖于`Mid`与`Window`略有不同。
- `QPalette::Light`：`2`;颜色比`Button`浅。
- `QPalette::Midlight`：`3`;介于`Button`至`Light`之间。
- `QPalette::Dark`：`4`;比`Button`更深。
- `QPalette::Mid`：`5`;介于`Button`和`Dark`之间。
- `QPalette::Shadow`：`11`;非常深的颜色。默认阴影颜色为`Qt::black`。
被选定（标记）的项目有两个角色：
- `QPalette::Highlight`：`12`;用来表示所选物品或当前物品的颜色。默认情况下，高亮颜色为`Qt::darkBlue`。
- `QPalette::Accent (since Qt 6.6)`：`21`;一种通常与基础色、窗口色和按钮色形成对比或互补的颜色。它通常代表用户对桌面个性化的选择。交互组件的样式是典型的使用场景。除非明确设置，否则默认为高亮。
- `QPalette::HighlightedText`：`13`;与`Highlight`对比的文本颜色。默认情况下，高亮的文本颜色为`Qt::white`。
与超链接相关的颜色角色有两种：
- `QPalette::Link`：`14`;用于未访问超链接的文本颜色。默认情况下，链接颜色为`Qt::blue`。
- `QPalette::LinkVisited`：`15`;用于已访问超链接的文本颜色。默认情况下，链接访问颜色为`Qt::magenta`。
请注意，我们在渲染 Qt 富文本时不使用 `Link` 和 `LinkVisited` 角色，建议使用 CSS 和 `QTextDocument::setDefaultStyleSheet()` 函数来更改链接的外观。例如：
- `QPalette::NoRole`：`17`;无角色;此特殊角色常用于表示尚未分配角色。

**官方示例：**

```cpp
     QTextBrowser browser;
     QColor linkColor(Qt::red);
     QString sheet = QString::fromLatin1("a { text-decoration: underline; color: %1 }").arg(linkColor.name());
     browser.document()->setDefaultStyleSheet(sheet);
```

### `QPalette::QPalette()`

**作用与语义：**

构建一个空调色板对象，没有设置任何颜色角色。
当用作`QWidget`调色板时，颜色的解析方式如`QWidget::setPalette()`所述。

### `QPalette::QPalette(Qt::GlobalColor button)`

**作用与语义：**

从`button`颜色构建调色板。其他颜色则基于该颜色自动计算。`Window`也是按钮颜色。

### `QPalette::QPalette(const QColor &button)`

**作用与语义：**

从`button`颜色构建调色板。其他颜色则基于该颜色自动计算。`Window`也是按钮颜色。

### `QPalette::QPalette(const QColor &button, const QColor &window)`

**作用与语义：**

由`button`色和`window`构建调色板。其他颜色则基于这些颜色自动计算。

### `QPalette::QPalette(const QBrush &windowText, const QBrush &button, const QBrush &light, const QBrush &dark, const QBrush &mid, const QBrush &text, const QBrush &bright_text, const QBrush &base, const QBrush &window)`

**作用与语义：**

构建调色板。你可以通过画笔、像素贴图或纯色来处理`windowText`、`button`、`light`、`dark`、`mid`、`text`、`bright_text`、`base`和`window`。

### `QPalette::QPalette(const QPalette &p)`

**作用与语义：**

复制了`p`。
由于隐式共享，这种构建器速度很快。

### `[noexcept] QPalette::QPalette(QPalette &&other)`

**作用与语义：**

Move构造一个QPalette实例，使其指向`other`指向的同一个对象。
被移出后，你只能对`other`分配或销毁。其他操作都会导致行为未定义。

### `[noexcept] QPalette::~QPalette()`

**作用与语义：**

会破坏调色板。

### `[since 6.6] const QBrush &QPalette::accent() const`

**作用与语义：**

返回当前颜色组的重音刷。

### `const QBrush &QPalette::alternateBase() const`

**作用与语义：**

返回当前颜色组的备用基刷。

### `const QBrush &QPalette::base() const`

**作用与语义：**

返回当前颜色组的基础画笔。

### `const QBrush &QPalette::brightText() const`

**作用与语义：**

返回当前颜色组的明亮文本前景画笔。

### `const QBrush &QPalette::brush(QPalette::ColorGroup group, QPalette::ColorRole role) const`

**作用与语义：**

以指定颜色`group`返回画笔，该颜色`role`使用。

### `const QBrush &QPalette::brush(QPalette::ColorRole role) const`

**作用与语义：**

返回当前`ColorGroup`中为指定颜色设置的画笔`role`。

### `const QBrush &QPalette::button() const`

**作用与语义：**

返回当前颜色组的按钮画刷。

### `const QBrush &QPalette::buttonText() const`

**作用与语义：**

返回当前颜色组的按钮文本前景笔刷。

### `qint64 QPalette::cacheKey() const`

**作用与语义：**

返回一个编号，用于识别该`QPalette`对象的内容。如果不同`QPalette`对象引用相同的内容，则可以拥有相同的密钥。
当调色板被更改时，cacheKey() 会发生变化。

### `const QColor &QPalette::color(QPalette::ColorGroup group, QPalette::ColorRole role) const`

**作用与语义：**

返回指定颜色`group`中的颜色，用于指定颜色`role`。

### `const QColor &QPalette::color(QPalette::ColorRole role) const`

**作用与语义：**

返回当前`ColorGroup`中为给定颜色`role`设置的颜色。

### `QPalette::ColorGroup QPalette::currentColorGroup() const`

**作用与语义：**

返回调色板当前的色组。

### `const QBrush &QPalette::dark() const`

**作用与语义：**

返回当前色组的深色刷。

### `const QBrush &QPalette::highlight() const`

**作用与语义：**

返回当前颜色组的高亮刷。

### `const QBrush &QPalette::highlightedText() const`

**作用与语义：**

返回当前颜色组的高亮文本刷。

### `bool QPalette::isBrushSet(QPalette::ColorGroup cg, QPalette::ColorRole cr) const`

**作用与语义：**

如果`ColorGroup` `cg`和`ColorRole` `cr`之前已在该调色板上设置过，返回`true`;否则返回`false`。
`ColorGroup` `cg`应该小于`QPalette::NColorGroups`，但你可以用`QPalette::Current`。在这种情况下，将使用之前设置的当前颜色组。
`ColorRole` `cr`应该低于`QPalette::NColorRoles`。

### `bool QPalette::isCopyOf(const QPalette &p) const`

**作用与语义：**

如果该调色板和`p`彼此是复制品，即其中一个作为另一个的复制品创建且未被修改，返回`true`;否则返回`false`。这比等式更严格。

### `bool QPalette::isEqual(QPalette::ColorGroup cg1, QPalette::ColorGroup cg2) const`

**作用与语义：**

如果颜色群`cg1`等于`cg2`，则返回`true`（通常很快）;否则返回`false`。

### `const QBrush &QPalette::light() const`

**作用与语义：**

返回当前色组的轻刷。

### `const QBrush &QPalette::link() const`

**作用与语义：**

返回当前颜色组未访问的链接文本刷。

### `const QBrush &QPalette::linkVisited() const`

**作用与语义：**

返回当前颜色组的访问链接文本画刷。

### `const QBrush &QPalette::mid() const`

**作用与语义：**

返回当前颜色组的中间画刷。

### `const QBrush &QPalette::midlight() const`

**作用与语义：**

返回当前颜色组的中光刷。

### `const QBrush &QPalette::placeholderText() const`

**作用与语义：**

返回当前颜色组的占位文本画刷。
注意：在Qt 5.12之前，占位符的文本颜色被硬编码为`QPalette::text()`。`color()`应用了alpha 128。在Qt 6中，占位符颜色是独立的。

### `QPalette QPalette::resolve(const QPalette &other) const`

**作用与语义：**

返回一个新`QPalette`，该  是该实例与 `other` 的并集。该实例中设置的颜色角色优先。未在此实例中设置的角色将从`other`中取用。

### `void QPalette::setBrush(QPalette::ColorRole role, const QBrush &brush)`

**作用与语义：**

将给定颜色的画笔设置为调色板中所有组的指定`brush` `role`。

### `void QPalette::setBrush(QPalette::ColorGroup group, QPalette::ColorRole role, const QBrush &brush)`

**作用与语义：**

将画笔设置为指定颜色`group`，用于指定颜色`role`，设置为`brush`。

### `void QPalette::setColor(QPalette::ColorGroup group, QPalette::ColorRole role, const QColor &color)`

**作用与语义：**

将指定颜色`group`中的颜色设置为指定的实色`color`，该颜色用于指定颜色`role`。

### `void QPalette::setColor(QPalette::ColorRole role, const QColor &color)`

**作用与语义：**

将给定颜色的颜色在所有颜色组中`role`指定为指定的实色`color`。

### `void QPalette::setColorGroup(QPalette::ColorGroup cg, const QBrush &windowText, const QBrush &button, const QBrush &light, const QBrush &dark, const QBrush &mid, const QBrush &text, const QBrush &bright_text, const QBrush &base, const QBrush &window)`

**作用与语义：**

将组设置为`cg`。你可以通过画笔、像素贴图或纯色传递给`windowText`、`button`、`light`、`dark`、`mid`、`text`、`bright_text`、`base`和`window`。

### `void QPalette::setCurrentColorGroup(QPalette::ColorGroup cg)`

**作用与语义：**

将调色板当前的色彩组设置为`cg`。

### `const QBrush &QPalette::shadow() const`

**作用与语义：**

返回当前颜色组的阴影刷。

### `[noexcept] void QPalette::swap(QPalette &other)`

**作用与语义：**

将该调色板实例与`other`交换。此操作非常快且从未失败。

### `const QBrush &QPalette::text() const`

**作用与语义：**

返回当前颜色组的文本前景笔刷。

### `const QBrush &QPalette::toolTipBase() const`

**作用与语义：**

返回当前颜色组的工具提示基础画笔。该画笔被`QToolTip`和`QWhatsThis`使用。
注意：工具提示使用`QPalette`的“非活跃颜色组”，因为工具提示不是活动窗口。

### `const QBrush &QPalette::toolTipText() const`

**作用与语义：**

返回当前颜色组的工具提示文本刷。该画刷被`QToolTip`和`QWhatsThis`使用。
注意：工具提示使用`QPalette`的“非活跃颜色组”，因为工具提示不是活动窗口。

### `const QBrush &QPalette::window() const`

**作用与语义：**

返回当前颜色组的窗口（通用背景）画刷。

### `const QBrush &QPalette::windowText() const`

**作用与语义：**

返回当前颜色组的窗口文本（前景）笔刷。

### `QPalette::operator QVariant() const`

**作用与语义：**

将调色板作为`QVariant`返回。

### `bool QPalette::operator!=(const QPalette &p) const`

**作用与语义：**

如果调色板与`p`不同，则返回`true`（缓慢）;否则返回`false`（通常很快）。
注意：比较调色板时不考虑当前`ColorGroup`。

### `[noexcept] QPalette &QPalette::operator=(QPalette &&other)`

**作用与语义：**

Move-assign `other`到这个`QPalette`实例。

### `QPalette &QPalette::operator=(const QPalette &p)`

**作用与语义：**

将`p`分配到该调色板，并返回对该调色板的引用。
由于隐式共享，这一操作速度很快。

### `[since 6.6] bool QPalette::operator==(const QPalette &p) const`

**作用与语义：**

如果调色板等于`p`，则返回`true`（通常很快）;否则返回`false`（缓慢）。
注意：比较调色板时未考虑以下因素：
- `current` `ColorGroup`
- `ColorRole` `NoRole`

### `QDataStream &operator<<(QDataStream &s, const QPalette &p)`

**作用与语义：**

写入调色板，`p`流`s`并返回流的引用。

### `QDataStream &operator>>(QDataStream &s, QPalette &p)`

**作用与语义：**

读取流中的调色板，`s`调色板`p`，并返回流的引用。

### `enum ColorGroup { Disabled, Active, Inactive, Normal }`

**作用与语义：**

- `QPalette::Disabled`：`1`
- `QPalette::Active`：`0`
- `QPalette::Inactive`：`2`
- `QPalette::Normal`：`Active`;主动的同义词

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QPalette` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
