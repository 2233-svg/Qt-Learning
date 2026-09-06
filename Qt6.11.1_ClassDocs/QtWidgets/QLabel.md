# QLabel

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QLabel` 是用于显示文本、富文本、图片或链接的轻量控件，通常不负责复杂交互。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QLabel` 是用于显示文本、富文本、图片或链接的轻量控件，通常不负责复杂交互。

**内部模型：** QLabel 的内容由 text/pixmap/movie 等模式决定；尺寸提示和 wordWrap 会影响布局，文本格式还会影响安全性和显示结果。

**适用场景：** 表单标签、状态提示、图标、说明文字和简单链接使用；需要编辑文本应使用 QLineEdit/QTextEdit，需要按钮行为应使用按钮类。

**典型调用链：** 创建 -> setText/setPixmap -> 设置 wordWrap/alignment/openExternalLinks -> 放入 layout -> 按业务状态更新。

**先记住的坑：** 富文本来自外部输入时注意安全和性能；图片显示要考虑 devicePixelRatio；不要用大量 QLabel 替代真正的数据视图。

## 2. 依赖与对象关系

- 头文件：`#include <QLabel>`
- 继承自：QFrame
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

QLabel 的内容由 text/pixmap/movie 等模式决定；尺寸提示和 wordWrap 会影响布局，文本格式还会影响安全性和显示结果。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

表单标签、状态提示、图标、说明文字和简单链接使用；需要编辑文本应使用 QLineEdit/QTextEdit，需要按钮行为应使用按钮类。 使用时通常按这个过程组织：创建 -> setText/setPixmap -> 设置 wordWrap/alignment/openExternalLinks -> 放入 layout -> 按业务状态更新。

```cpp
auto *label = new QLabel(QStringLiteral("Ready"), parent);
label->setWordWrap(true);
label->setAlignment(Qt::AlignCenter);
connect(worker, &Worker::statusChanged, label, &QLabel::setText);
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 属性

- `alignment : Qt::Alignment`
- `hasSelectedText : bool`
- `indent : int`
- `margin : int`
- `openExternalLinks : bool`
- `pixmap : QPixmap`
- `scaledContents : bool`
- `selectedText : QString`
- `text : QString`
- `textFormat : Qt::TextFormat`
- `textInteractionFlags : Qt::TextInteractionFlags`
- `wordWrap : bool`

### 公有函数

- `QLabel(QWidget *parent = nullptr, Qt::WindowFlags f = Qt::WindowFlags())`
- `QLabel(const QString &text, QWidget *parent = nullptr, Qt::WindowFlags f = Qt::WindowFlags())`
- `virtual ~QLabel()`
- `Qt::Alignment alignment() const`
- `QWidget * buddy() const`
- `bool hasScaledContents() const`
- `bool hasSelectedText() const`
- `int indent() const`
- `int margin() const`
- `QMovie * movie() const`
- `bool openExternalLinks() const`
- `(since 6.0) QPicture picture() const`
- `QPixmap pixmap() const`
- `(since 6.1) QTextDocument::ResourceProvider resourceProvider() const`
- `QString selectedText() const`
- `int selectionStart() const`
- `void setAlignment(Qt::Alignment)`
- `void setBuddy(QWidget *buddy)`
- `void setIndent(int)`
- `void setMargin(int)`
- `void setOpenExternalLinks(bool open)`
- `(since 6.1) void setResourceProvider(const QTextDocument::ResourceProvider &provider)`
- `void setScaledContents(bool)`
- `void setSelection(int start, int length)`
- `void setTextFormat(Qt::TextFormat)`
- `void setTextInteractionFlags(Qt::TextInteractionFlags flags)`
- `void setWordWrap(bool on)`
- `QString text() const`
- `Qt::TextFormat textFormat() const`
- `Qt::TextInteractionFlags textInteractionFlags() const`
- `bool wordWrap() const`

### 重实现的公有函数

- `virtual int heightForWidth(int w) const override`
- `virtual QSize minimumSizeHint() const override`
- `virtual QSize sizeHint() const override`

### 公有槽函数

- `void clear()`
- `void setMovie(QMovie *movie)`
- `void setNum(int num)`
- `void setNum(double num)`
- `void setPicture(const QPicture &picture)`
- `void setPixmap(const QPixmap &)`
- `void setText(const QString &)`

### 信号

- `void linkActivated(const QString &link)`
- `void linkHovered(const QString &link)`

### 重实现的保护函数

- `virtual void changeEvent(QEvent *ev) override`
- `virtual void contextMenuEvent(QContextMenuEvent *ev) override`
- `virtual bool event(QEvent *e) override`
- `virtual void focusInEvent(QFocusEvent *ev) override`
- `virtual bool focusNextPrevChild(bool next) override`
- `virtual void focusOutEvent(QFocusEvent *ev) override`
- `virtual void keyPressEvent(QKeyEvent *ev) override`
- `virtual void mouseMoveEvent(QMouseEvent *ev) override`
- `virtual void mousePressEvent(QMouseEvent *ev) override`
- `virtual void mouseReleaseEvent(QMouseEvent *ev) override`
- `virtual void paintEvent(QPaintEvent *) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `alignment : Qt::Alignment`

**作用与语义：**

该属性表示标签内容的对齐。
默认情况下，标签内容为左对齐且垂直居中。

**如何使用：** 调用 `alignment()` 读取当前值；它不会修改应用状态。

### `[read-only] hasSelectedText : bool`

**作用与语义：**

该属性决定是否存在任何文本被选中。
hasSelectedText() 如果用户选择了部分或全部文本，则返回 `true`;否则返回 `false`。
默认情况下，该属性为`false`。
注意：标签上的 `textInteractionFlags` 集需要包含 TextSelectableByMouse 或 TextSelectableByKeyboard。

**如何使用：** 调用 `hasSelectedText()` 读取当前值；它不会修改应用状态。

### `indent : int`

**作用与语义：**

此属性保存标签的文本缩进（以像素为单位）。
如果标签显示文本，当 `alignment()` 为 `Qt::AlignLeft` 时，缩进应用于左边缘；当 `alignment()` 为 `Qt::AlignRight` 时，缩进应用于右边缘；当 `alignment()` 为 `Qt::AlignTop` 时，缩进应用于上边缘；当 `alignment()` 为 `Qt::AlignBottom` 时，缩进应用于下边缘。
如果缩进为负值，或者没有设置缩进，标签按以下方式计算有效缩进：如果 `frameWidth()` 为 0，则有效缩进为 0。如果 `frameWidth()` 大于 0，则有效缩进为该控件当前 `font()` 的“x”字符宽度的一半。
默认情况下，缩进为 -1，这意味着有效缩进按上述方式计算。

**如何使用：** 调用 `indent()` 读取当前值；它不会修改应用状态。

### `margin : int`

**作用与语义：**

该属性表示边际宽度。
边距是画面最内层像素与内容最外层像素之间的距离。
默认保证金为0。

**如何使用：** 调用 `margin()` 读取当前值；它不会修改应用状态。

### `openExternalLinks : bool`

**作用与语义：**

规定`QLabel`是否应使用`QDesktopServices::openUrl()`自动开启链路，而不是发出`linkActivated()`信号。
注意：标签上的 `textInteractionFlags` 集需要包含 LinksAccessibleByMouse 或 LinksAccessibleByKeyboard。
默认值为假。

**如何使用：** 调用 `openExternalLinks()` 读取当前值；它不会修改应用状态。

### `pixmap : QPixmap`

**作用与语义：**

该属性包含标签的像素映射。
设置像素映射会清除之前的所有内容。如果有好友快捷方式，则禁用。

**如何使用：** 调用 `pixmap()` 读取当前值；它不会修改应用状态。

### `scaledContents : bool`

**作用与语义：**

该属性决定标签是否会按内容放大填满所有可用空间。
启用后标签显示像素图，它会放大像素图以填满可用空间。
该属性的默认值为假。

**如何使用：** 调用 `scaledContents()` 读取当前值；它不会修改应用状态。

### `[read-only] selectedText : QString`

**作用与语义：**

该属性包含所选文本。
如果没有被选中的文本，该属性的值是空字符串。
默认情况下，该属性包含空字符串。
注意：标签上的 `textInteractionFlags` 集需要包含 TextSelectableByMouse 或 TextSelectableByKeyboard。

**如何使用：** 调用 `selectedText()` 读取当前值；它不会修改应用状态。

### `text : QString`

**作用与语义：**

该属性包含标签的文本。
如果没有设置文本，则返回一个空字符串。设置文本会清除之前的所有内容。
文本将根据文本格式设置被解释为纯文本或富文本;参见 `setTextFormat()`。默认设置为`Qt::AutoText`;即`QLabel`会尝试自动检测文本集的格式。关于富文本的定义，请参见支持 HTML 子集。
如果设置了伙伴，伙伴助记键会根据新文本更新。
请注意，`QLabel` 非常适合显示小型富文本文档，比如通过标签调色板和字体属性获得文档专属设置（字体、文本颜色、链接颜色）的小文档。对于大型文档，请使用只读模式的 `QTextEdit`。`QTextEdit` 也可以在需要时提供滚动条。
注意：如果`text`包含富文本，此功能可启用鼠标追踪。

**如何使用：** 调用 `text()` 读取当前值；它不会修改应用状态。

### `textFormat : Qt::TextFormat`

**作用与语义：**

该属性表示标签的文本格式。
请参阅`Qt::TextFormat`枚举，了解可能选项的说明。
默认格式是`Qt::AutoText`。

**如何使用：** 调用 `textFormat()` 读取当前值；它不会修改应用状态。

### `textInteractionFlags : Qt::TextInteractionFlags`

**作用与语义：**

规定标签在显示文本时应如何与用户输入交互。
如果旗标包含`Qt::LinksAccessibleByKeyboard`焦点策略也会自动设置为`Qt::StrongFocus`。如果设置`Qt::TextSelectableByKeyboard`，焦点策略也设置为`Qt::ClickFocus`。
默认值是`Qt::LinksAccessibleByMouse`。

**如何使用：** 调用 `textInteractionFlags()` 读取当前值；它不会修改应用状态。

### `wordWrap : bool`

**作用与语义：**

此属性保存标签的自动换行策略。
如果此属性为 `true`，则标签文本在必要时按照断词处换行；否则完全不换行。
默认情况下，自动换行被禁用。

**如何使用：** 调用 `wordWrap()` 读取当前值；它不会修改应用状态。

### `[explicit] QLabel::QLabel(QWidget *parent = nullptr, Qt::WindowFlags f = Qt::WindowFlags())`

**作用与语义：**

构造一个空标签。
`parent`和控件标志`f`，参数传递给`QFrame`构造器。

### `[explicit] QLabel::QLabel(const QString &text, QWidget *parent = nullptr, Qt::WindowFlags f = Qt::WindowFlags())`

**作用与语义：**

构建一个标签来显示文本，`text`。
`parent`和控件标志`f`，参数传递给`QFrame`构造器。

### `[virtual noexcept] QLabel::~QLabel()`

**作用与语义：**

毁掉了这个标签。

### `QWidget *QLabel::buddy() const`

**作用与语义：**

返回该标签的伙伴，或者如果当前没有伙伴设置，则返回nullptr。

### `[override virtual protected] void QLabel::changeEvent(QEvent *ev)`

**作用与语义：**

重实现自：`QFrame::changeEvent`（QEvent *ev）。

### `[slot] void QLabel::clear()`

**作用与语义：**

清除标签内容。

### `[override virtual protected] void QLabel::contextMenuEvent(QContextMenuEvent *ev)`

**作用与语义：**

重实现自：`QWidget::contextMenuEvent`（QContextMenuEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收控件上下文菜单事件。
当控件的 `contextMenuPolicy` `Qt::DefaultContextMenu`时调用处理器。
默认实现忽略上下文事件。详情请参见`QContextMenuEvent`文档。

### `[override virtual protected] bool QLabel::event(QEvent *e)`

**作用与语义：**

重实现自：`QFrame::event`（QEvent *e）。

### `[override virtual protected] void QLabel::focusInEvent(QFocusEvent *ev)`

**作用与语义：**

重实现自：`QWidget::focusInEvent`（QFocusEvent *event）。
该事件处理程序可以在子类中重新实现，以接收控件的键盘焦点事件（焦点接收）。事件通过`event`参数传递。
小部件通常必须`setFocusPolicy()`到非`Qt::NoFocus`的对象才能接收焦点事件。（注意，应用程序员可以调用任何小部件`setFocus()`，即使是那些通常不接受焦点的小部件。）。
默认实现会更新小部件（除非是没有指定`focusPolicy()`的窗口）。

### `[override virtual protected] bool QLabel::focusNextPrevChild(bool next)`

**作用与语义：**

重构：`QWidget::focusNextPrevChild`（下一个布尔）。
根据 Tab 和 Shift Tab 找到一个新的控件来给键盘焦点，如果能找到新控件，则返回 `true`，找不到则返回 false。
如果`next`为真，该函数向前搜索;如果`next`为假，则向后搜索。
有时，你会想重新实现这个函数。例如，浏览器可能会重新实现它，将“当前活跃链接”向前或向后移动，只有当它到达“页面”的最后或第一个链接时才调用 focusNextPrevChild()。
子控件调用其父控件的 focusNextPrevChild()，但只有包含子控件的窗口决定将焦点重定向到哪里。通过重新实现该函数，你就能控制所有子控件的焦点遍历。

### `[override virtual protected] void QLabel::focusOutEvent(QFocusEvent *ev)`

**作用与语义：**

重现：`QWidget::focusOutEvent`（QFocusEvent *event）。
该事件处理程序可以在子类中重新实现，以接收控件的键盘焦点事件（焦点丢失）。事件通过`event`参数传递。
小部件通常必须`setFocusPolicy()`到非`Qt::NoFocus`的对象才能接收焦点事件。（注意，应用程序员可以调用任何小部件`setFocus()`，即使是那些通常不接受焦点的小部件。）。
默认实现会更新小部件（除非是没有指定`focusPolicy()`的窗口）。

### `[override virtual] int QLabel::heightForWidth(int w) const`

**作用与语义：**

重实现自：`QWidget::heightForWidth`（内性 w） const.
返回该小部件的首选高度，基于宽度`w`。
如果该控件有布局，默认实现返回该布局的首选高度。如果没有布局，默认实现返回 -1，表示首选高度不依赖于宽度。

### `[override virtual protected] void QLabel::keyPressEvent(QKeyEvent *ev)`

**作用与语义：**

重实现自：`QWidget::keyPressEvent`（QKeyEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该控件的按键事件。
一个小部件必须调用`setFocusPolicy()`先接受焦点，并且必须有焦点才能接收按键事件。
如果你重新实现这个处理器，如果你不对密钥进行操作，务必调用基类实现。
默认实现会关闭弹出小部件，如果用户按下`QKeySequence::Cancel`的按键序列（通常是 Escape 键）。否则事件会被忽略，以便小部件的父节点能够解释。
注意`QKeyEvent`以 isAccepted() == true 开头，所以你不需要调用 `QKeyEvent::accept()`——只要你对该键执行时不要调用基类实现即可。

### `[signal] void QLabel::linkActivated(const QString &link)`

**作用与语义：**

当用户点击链接时，该信号会发出。锚点所引用的URL会以`link`传递。

### `[signal] void QLabel::linkHovered(const QString &link)`

**作用与语义：**

当用户将鼠标悬停在链接上时，该信号会发出。锚点所引用的URL会以`link`传递。

### `[override virtual] QSize QLabel::minimumSizeHint() const`

**作用与语义：**

重新实现属性的访问函数：`QWidget::minimumSizeHint`。

### `[override virtual protected] void QLabel::mouseMoveEvent(QMouseEvent *ev)`

**作用与语义：**

重实现自：`QWidget::mouseMoveEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标移动事件。
如果关闭鼠标追踪，只有在鼠标移动过程中按下鼠标按钮时才会发生鼠标移动事件。如果开启鼠标追踪，即使未按键，鼠标移动事件也会发生。
`QMouseEvent::position()`报告鼠标光标相对于该小部件的位置。对于按下和释放事件，位置通常与最后一次鼠标移动事件的位置相同，但如果用户的手握手，可能会有所不同。这是底层窗口系统的功能，而非Qt。
如果你想在鼠标移动时立即显示提示（例如，获取鼠标坐标与`QMouseEvent::position()`并显示为提示），你必须先启用上述的鼠标追踪功能。然后，为了确保提示立即更新，你必须在鼠标移动事件（mouseMoveEvent）实现中调用`QToolTip::showText()`而不是`setToolTip()`。

### `[override virtual protected] void QLabel::mousePressEvent(QMouseEvent *ev)`

**作用与语义：**

重实现自：`QWidget::mousePressEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标按键事件。
如果你在 mousePressEvent() 创建新控件，`mouseReleaseEvent()`可能不会出现在你预期的位置，这取决于底层窗口系统（或 X11 窗口管理器）、控件的位置，甚至可能还有其他因素。
默认实现实现了当你点击窗口外时关闭弹出小部件的功能。对于其他小部件类型，它没有任何作用。

### `[override virtual protected] void QLabel::mouseReleaseEvent(QMouseEvent *ev)`

**作用与语义：**

重实现自：`QWidget::mouseReleaseEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标释放事件。

### `QMovie *QLabel::movie() const`

**作用与语义：**

返回标签的电影指针，如果没有设置电影则返回nullptr。

### `[override virtual protected] void QLabel::paintEvent(QPaintEvent *)`

**作用与语义：**

重实现自：`QFrame::paintEvent`（QPaintEvent *）。

### `[since 6.0] QPicture QLabel::picture() const`

**作用与语义：**

还给标签上的照片。

### `[since 6.1] QTextDocument::ResourceProvider QLabel::resourceProvider() const`

**作用与语义：**

返回该标签的富文本资源提供者。

### `int QLabel::selectionStart() const`

**作用与语义：**

selectionStart() 返回标签中第一个被选中字符的索引，若未选择文本则返回 -1。
注意：标签上的 `textInteractionFlags` 集需要包含 TextSelectableByMouse 或 TextSelectableByKeyboard。

### `void QLabel::setBuddy(QWidget *buddy)`

**作用与语义：**

让这个标签的伙伴变成`buddy`。
当用户按下该标签指示的快捷键时，键盘焦点会转移到标签的伙伴小部件上。
伙伴机制仅适用于包含一个字符前缀为“&”的文本的QLabel。该字符被设置为快捷键。详情请参见`QKeySequence::mnemonic()`文档（如需显示实际的&符号，请使用“&&”）。
在对话框中，你可以创建两个数据输入小部件和每个小部件的标签，并设置几何布局，使每个标签都位于其数据输入小部件（它的“伙伴”）左侧，例如：
使用上述代码，用户按Alt N时焦点跳转到Name字段，按下Alt P时跳转到Phone字段。
要撤销之前设置的伙伴，调用该函数，`buddy`设置为 nullptr。

**官方示例：**

```cpp
 QLineEdit *nameEdit  = new QLineEdit(this);
 QLabel    *nameLabel = new QLabel("&Name:", this);
 nameLabel->setBuddy(nameEdit);
 QLineEdit *phoneEdit  = new QLineEdit(this);
 QLabel    *phoneLabel = new QLabel("&Phone:", this);
 phoneLabel->setBuddy(phoneEdit);
 // (layout setup not shown)
```

### `[slot] void QLabel::setMovie(QMovie *movie)`

**作用与语义：**

将标签内容设置为`movie`。之前的内容会被清除。标签不会拥有电影的所有权。
如果有好友快捷方式，则是禁用的。

### `[slot] void QLabel::setNum(int num)`

**作用与语义：**

将标签内容设置为纯文本，包含整数 `num` 的文本表示。之前的所有内容被清除。如果整数的字符串表示与标签当前内容相同，则无效。
如果有好友快捷方式，则是禁用的。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
label， qOverload（&QLabel：：setNum））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
label， [receiver = label]（int num） { receiver->setNum（num）; }）;


更多示例和方法，请参见连接超载槽位。

### `[slot] void QLabel::setNum(double num)`

**作用与语义：**

将标签内容设置为包含双重 `num` 文本表示的纯文本。之前的所有内容都被清除。如果双重的字符串表示与当前标签内容相同，则无效。
如果有好友快捷方式，则是禁用的。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
label， qOverload（&QLabel：：setNum））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
label， [receiver = label]（double num） { receiver->setNum（num）; }）;


更多示例和方法，请参见连接超载槽位。

### `[slot] void QLabel::setPicture(const QPicture &picture)`

**作用与语义：**

将标签内容设置为`picture`。之前的内容会被清除。
如果有好友快捷方式，则是禁用的。

### `[since 6.1] void QLabel::setResourceProvider(const QTextDocument::ResourceProvider &provider)`

**作用与语义：**

设置该标签富文本资源的资源`provider`。
注意：唱片公司不对`provider`拥有所有权。

### `void QLabel::setSelection(int start, int length)`

**作用与语义：**

从位置`start`和`length`字符中选择文本。
注意：标签上的`textInteractionFlags`集需要包含TextSelectableByMouse或TextSelectableByKeyboard之一。

### `[override virtual] QSize QLabel::sizeHint() const`

**作用与语义：**

重实现自：`QFrame::sizeHint()` const.
重新实现了属性的访问函数：`QWidget::sizeHint`。

### `Qt::Alignment alignment() const`

**作用与语义：**

该属性表示标签内容的对齐。
默认情况下，标签内容为左对齐且垂直居中。

**如何使用：** 调用 `alignment()` 读取当前值；它不会修改应用状态。

### `bool hasScaledContents() const`

**作用与语义：**

该属性决定标签是否会按内容放大填满所有可用空间。
启用后标签显示像素图，它会放大像素图以填满可用空间。
该属性的默认值为假。

**如何使用：** 调用 `hasScaledContents()` 读取当前值；它不会修改应用状态。

### `bool hasSelectedText() const`

**作用与语义：**

该属性决定是否存在任何文本被选中。
hasSelectedText() 如果用户选择了部分或全部文本，则返回 `true`;否则返回 `false`。
默认情况下，该属性为`false`。
注意：标签上的 `textInteractionFlags` 集需要包含 TextSelectableByMouse 或 TextSelectableByKeyboard。

**如何使用：** 调用 `hasSelectedText()` 读取当前值；它不会修改应用状态。

### `int indent() const`

**作用与语义：**

此属性保存标签的文本缩进（以像素为单位）。
如果标签显示文本，当 `alignment()` 为 `Qt::AlignLeft` 时，缩进应用于左边缘；当 `alignment()` 为 `Qt::AlignRight` 时，缩进应用于右边缘；当 `alignment()` 为 `Qt::AlignTop` 时，缩进应用于上边缘；当 `alignment()` 为 `Qt::AlignBottom` 时，缩进应用于下边缘。
如果缩进为负值，或者没有设置缩进，标签按以下方式计算有效缩进：如果 `frameWidth()` 为 0，则有效缩进为 0。如果 `frameWidth()` 大于 0，则有效缩进为该控件当前 `font()` 的“x”字符宽度的一半。
默认情况下，缩进为 -1，这意味着有效缩进按上述方式计算。

**如何使用：** 调用 `indent()` 读取当前值；它不会修改应用状态。

### `int margin() const`

**作用与语义：**

该属性表示边际宽度。
边距是画面最内层像素与内容最外层像素之间的距离。
默认保证金为0。

**如何使用：** 调用 `margin()` 读取当前值；它不会修改应用状态。

### `bool openExternalLinks() const`

**作用与语义：**

规定`QLabel`是否应使用`QDesktopServices::openUrl()`自动开启链路，而不是发出`linkActivated()`信号。
注意：标签上的 `textInteractionFlags` 集需要包含 LinksAccessibleByMouse 或 LinksAccessibleByKeyboard。
默认值为假。

**如何使用：** 调用 `openExternalLinks()` 读取当前值；它不会修改应用状态。

### `QPixmap pixmap() const`

**作用与语义：**

该属性包含标签的像素映射。
设置像素映射会清除之前的所有内容。如果有好友快捷方式，则禁用。

**如何使用：** 调用 `pixmap()` 读取当前值；它不会修改应用状态。

### `QString selectedText() const`

**作用与语义：**

该属性包含所选文本。
如果没有被选中的文本，该属性的值是空字符串。
默认情况下，该属性包含空字符串。
注意：标签上的 `textInteractionFlags` 集需要包含 TextSelectableByMouse 或 TextSelectableByKeyboard。

**如何使用：** 调用 `selectedText()` 读取当前值；它不会修改应用状态。

### `void setAlignment(Qt::Alignment)`

**作用与语义：**

该属性表示标签内容的对齐。
默认情况下，标签内容为左对齐且垂直居中。

**如何使用：** 调用 `setAlignment(...)` 修改 `alignment`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setIndent(int)`

**作用与语义：**

此属性保存标签的文本缩进（以像素为单位）。
如果标签显示文本，当 `alignment()` 为 `Qt::AlignLeft` 时，缩进应用于左边缘；当 `alignment()` 为 `Qt::AlignRight` 时，缩进应用于右边缘；当 `alignment()` 为 `Qt::AlignTop` 时，缩进应用于上边缘；当 `alignment()` 为 `Qt::AlignBottom` 时，缩进应用于下边缘。
如果缩进为负值，或者没有设置缩进，标签按以下方式计算有效缩进：如果 `frameWidth()` 为 0，则有效缩进为 0。如果 `frameWidth()` 大于 0，则有效缩进为该控件当前 `font()` 的“x”字符宽度的一半。
默认情况下，缩进为 -1，这意味着有效缩进按上述方式计算。

**如何使用：** 调用 `setIndent(...)` 修改 `indent`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMargin(int)`

**作用与语义：**

该属性表示边际宽度。
边距是画面最内层像素与内容最外层像素之间的距离。
默认保证金为0。

**如何使用：** 调用 `setMargin(...)` 修改 `margin`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setOpenExternalLinks(bool open)`

**作用与语义：**

规定`QLabel`是否应使用`QDesktopServices::openUrl()`自动开启链路，而不是发出`linkActivated()`信号。
注意：标签上的 `textInteractionFlags` 集需要包含 LinksAccessibleByMouse 或 LinksAccessibleByKeyboard。
默认值为假。

**如何使用：** 调用 `setOpenExternalLinks(...)` 修改 `openExternalLinks`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setScaledContents(bool)`

**作用与语义：**

该属性决定标签是否会按内容放大填满所有可用空间。
启用后标签显示像素图，它会放大像素图以填满可用空间。
该属性的默认值为假。

**如何使用：** 调用 `setScaledContents(...)` 修改 `scaledContents`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTextFormat(Qt::TextFormat)`

**作用与语义：**

该属性表示标签的文本格式。
请参阅`Qt::TextFormat`枚举，了解可能选项的说明。
默认格式是`Qt::AutoText`。

**如何使用：** 调用 `setTextFormat(...)` 修改 `textFormat`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTextInteractionFlags(Qt::TextInteractionFlags flags)`

**作用与语义：**

规定标签在显示文本时应如何与用户输入交互。
如果旗标包含`Qt::LinksAccessibleByKeyboard`焦点策略也会自动设置为`Qt::StrongFocus`。如果设置`Qt::TextSelectableByKeyboard`，焦点策略也设置为`Qt::ClickFocus`。
默认值是`Qt::LinksAccessibleByMouse`。

**如何使用：** 调用 `setTextInteractionFlags(...)` 修改 `textInteractionFlags`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setWordWrap(bool on)`

**作用与语义：**

此属性保存标签的自动换行策略。
如果此属性为 `true`，则标签文本在必要时按照断词处换行；否则完全不换行。
默认情况下，自动换行被禁用。

**如何使用：** 调用 `setWordWrap(...)` 修改 `wordWrap`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QString text() const`

**作用与语义：**

该属性包含标签的文本。
如果没有设置文本，则返回一个空字符串。设置文本会清除之前的所有内容。
文本将根据文本格式设置被解释为纯文本或富文本;参见 `setTextFormat()`。默认设置为`Qt::AutoText`;即`QLabel`会尝试自动检测文本集的格式。关于富文本的定义，请参见支持 HTML 子集。
如果设置了伙伴，伙伴助记键会根据新文本更新。
请注意，`QLabel` 非常适合显示小型富文本文档，比如通过标签调色板和字体属性获得文档专属设置（字体、文本颜色、链接颜色）的小文档。对于大型文档，请使用只读模式的 `QTextEdit`。`QTextEdit` 也可以在需要时提供滚动条。
注意：如果`text`包含富文本，此功能可启用鼠标追踪。

**如何使用：** 调用 `text()` 读取当前值；它不会修改应用状态。

### `Qt::TextFormat textFormat() const`

**作用与语义：**

该属性表示标签的文本格式。
请参阅`Qt::TextFormat`枚举，了解可能选项的说明。
默认格式是`Qt::AutoText`。

**如何使用：** 调用 `textFormat()` 读取当前值；它不会修改应用状态。

### `Qt::TextInteractionFlags textInteractionFlags() const`

**作用与语义：**

规定标签在显示文本时应如何与用户输入交互。
如果旗标包含`Qt::LinksAccessibleByKeyboard`焦点策略也会自动设置为`Qt::StrongFocus`。如果设置`Qt::TextSelectableByKeyboard`，焦点策略也设置为`Qt::ClickFocus`。
默认值是`Qt::LinksAccessibleByMouse`。

**如何使用：** 调用 `textInteractionFlags()` 读取当前值；它不会修改应用状态。

### `bool wordWrap() const`

**作用与语义：**

此属性保存标签的自动换行策略。
如果此属性为 `true`，则标签文本在必要时按照断词处换行；否则完全不换行。
默认情况下，自动换行被禁用。

**如何使用：** 调用 `wordWrap()` 读取当前值；它不会修改应用状态。

### `void setPixmap(const QPixmap &)`

**作用与语义：**

该属性包含标签的像素映射。
设置像素映射会清除之前的所有内容。如果有好友快捷方式，则禁用。

**如何使用：** 调用 `setPixmap(...)` 修改 `pixmap`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setText(const QString &)`

**作用与语义：**

该属性包含标签的文本。
如果没有设置文本，则返回一个空字符串。设置文本会清除之前的所有内容。
文本将根据文本格式设置被解释为纯文本或富文本;参见 `setTextFormat()`。默认设置为`Qt::AutoText`;即`QLabel`会尝试自动检测文本集的格式。关于富文本的定义，请参见支持 HTML 子集。
如果设置了伙伴，伙伴助记键会根据新文本更新。
请注意，`QLabel` 非常适合显示小型富文本文档，比如通过标签调色板和字体属性获得文档专属设置（字体、文本颜色、链接颜色）的小文档。对于大型文档，请使用只读模式的 `QTextEdit`。`QTextEdit` 也可以在需要时提供滚动条。
注意：如果`text`包含富文本，此功能可启用鼠标追踪。

**如何使用：** 调用 `setText(...)` 修改 `text`；传入的新值会成为后续查询和相关界面行为所使用的值。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

富文本来自外部输入时注意安全和性能；图片显示要考虑 devicePixelRatio；不要用大量 QLabel 替代真正的数据视图。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QLabel` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
