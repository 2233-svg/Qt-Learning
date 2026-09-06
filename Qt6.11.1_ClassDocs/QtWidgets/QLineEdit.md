# QLineEdit

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QLineEdit` 是单行文本编辑控件，提供输入、选择、验证、占位提示和编辑完成信号。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QLineEdit` 是单行文本编辑控件，提供输入、选择、验证、占位提示和编辑完成信号。

**内部模型：** 编辑中的 text 和用户确认后的 editingFinished 是不同阶段；validator、inputMask 和 echoMode 分别控制合法性、格式和显示方式。

**适用场景：** 用户名、路径、搜索框、数值和短文本输入使用；多行文本使用 QTextEdit/QPlainTextEdit。

**典型调用链：** 创建 -> 设置 placeholder/validator/echoMode -> 连接 textChanged 或 editingFinished -> 读取 text -> 业务校验和提交。

**先记住的坑：** textChanged 可能高频触发；不能只依赖 validator 当作业务校验；密码框不要记录日志；提交前仍要检查空值和业务约束。

## 2. 依赖与对象关系

- 头文件：`#include <QLineEdit>`
- 继承自：QWidget
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

编辑中的 text 和用户确认后的 editingFinished 是不同阶段；validator、inputMask 和 echoMode 分别控制合法性、格式和显示方式。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

用户名、路径、搜索框、数值和短文本输入使用；多行文本使用 QTextEdit/QPlainTextEdit。 使用时通常按这个过程组织：创建 -> 设置 placeholder/validator/echoMode -> 连接 textChanged 或 editingFinished -> 读取 text -> 业务校验和提交。

```cpp
auto *edit = new QLineEdit(parent);
edit->setPlaceholderText(QStringLiteral("Search..."));
connect(edit, &QLineEdit::returnPressed, this, [this, edit] {
    search(edit->text());
});
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum ActionPosition { LeadingPosition, TrailingPosition }`
- `enum EchoMode { Normal, NoEcho, Password, PasswordEchoOnEdit }`

### 属性

- `acceptableInput : bool`
- `alignment : Qt::Alignment`
- `clearButtonEnabled : bool`
- `cursorMoveStyle : Qt::CursorMoveStyle`
- `cursorPosition : int`
- `displayText : QString`
- `dragEnabled : bool`
- `echoMode : EchoMode`
- `frame : bool`
- `hasSelectedText : bool`
- `inputMask : QString`
- `maxLength : int`
- `modified : bool`
- `placeholderText : QString`
- `readOnly : bool`
- `redoAvailable : bool`
- `selectedText : QString`
- `text : QString`
- `undoAvailable : bool`

### 公有函数

- `QLineEdit(QWidget *parent = nullptr)`
- `QLineEdit(const QString &contents, QWidget *parent = nullptr)`
- `virtual ~QLineEdit()`
- `void addAction(QAction *action, QLineEdit::ActionPosition position)`
- `QAction * addAction(const QIcon &icon, QLineEdit::ActionPosition position)`
- `Qt::Alignment alignment() const`
- `void backspace()`
- `QCompleter * completer() const`
- `QMenu * createStandardContextMenu()`
- `void cursorBackward(bool mark, int steps = 1)`
- `void cursorForward(bool mark, int steps = 1)`
- `Qt::CursorMoveStyle cursorMoveStyle() const`
- `int cursorPosition() const`
- `int cursorPositionAt(const QPoint &pos)`
- `void cursorWordBackward(bool mark)`
- `void cursorWordForward(bool mark)`
- `void del()`
- `void deselect()`
- `QString displayText() const`
- `bool dragEnabled() const`
- `QLineEdit::EchoMode echoMode() const`
- `void end(bool mark)`
- `bool hasAcceptableInput() const`
- `bool hasFrame() const`
- `bool hasSelectedText() const`
- `void home(bool mark)`
- `QString inputMask() const`
- `void insert(const QString &newText)`
- `bool isClearButtonEnabled() const`
- `bool isModified() const`
- `bool isReadOnly() const`
- `bool isRedoAvailable() const`
- `bool isUndoAvailable() const`
- `int maxLength() const`
- `QString placeholderText() const`
- `QString selectedText() const`
- `int selectionEnd() const`
- `int selectionLength() const`
- `int selectionStart() const`
- `void setAlignment(Qt::Alignment flag)`
- `void setClearButtonEnabled(bool enable)`
- `void setCompleter(QCompleter *c)`
- `void setCursorMoveStyle(Qt::CursorMoveStyle style)`
- `void setCursorPosition(int)`
- `void setDragEnabled(bool b)`
- `void setEchoMode(QLineEdit::EchoMode)`
- `void setFrame(bool)`
- `void setInputMask(const QString &inputMask)`
- `void setMaxLength(int)`
- `void setModified(bool)`
- `void setPlaceholderText(const QString &)`
- `void setReadOnly(bool)`
- `void setSelection(int start, int length)`
- `void setTextMargins(const QMargins &margins)`
- `void setTextMargins(int left, int top, int right, int bottom)`
- `void setValidator(const QValidator *v)`
- `QString text() const`
- `QMargins textMargins() const`
- `const QValidator * validator() const`

### 重实现的公有函数

- `virtual bool event(QEvent *e) override`
- `virtual QVariant inputMethodQuery(Qt::InputMethodQuery property) const override`
- `virtual QSize minimumSizeHint() const override`
- `virtual QSize sizeHint() const override`
- `virtual void timerEvent(QTimerEvent *e) override`

### 公有槽函数

- `void clear()`
- `void copy() const`
- `void cut()`
- `void paste()`
- `void redo()`
- `void selectAll()`
- `void setText(const QString &)`
- `void undo()`

### 信号

- `void cursorPositionChanged(int oldPos, int newPos)`
- `void editingFinished()`
- `void inputRejected()`
- `void returnPressed()`
- `void selectionChanged()`
- `void textChanged(const QString &text)`
- `void textEdited(const QString &text)`

### 保护函数

- `QRect cursorRect() const`
- `virtual void initStyleOption(QStyleOptionFrame *option) const`

### 重实现的保护函数

- `virtual void changeEvent(QEvent *ev) override`
- `virtual void contextMenuEvent(QContextMenuEvent *event) override`
- `virtual void dragEnterEvent(QDragEnterEvent *e) override`
- `virtual void dragLeaveEvent(QDragLeaveEvent *e) override`
- `virtual void dragMoveEvent(QDragMoveEvent *e) override`
- `virtual void dropEvent(QDropEvent *e) override`
- `virtual void focusInEvent(QFocusEvent *e) override`
- `virtual void focusOutEvent(QFocusEvent *e) override`
- `virtual void inputMethodEvent(QInputMethodEvent *e) override`
- `virtual void keyPressEvent(QKeyEvent *event) override`
- `virtual void keyReleaseEvent(QKeyEvent *e) override`
- `virtual void mouseDoubleClickEvent(QMouseEvent *e) override`
- `virtual void mouseMoveEvent(QMouseEvent *e) override`
- `virtual void mousePressEvent(QMouseEvent *e) override`
- `virtual void mouseReleaseEvent(QMouseEvent *e) override`
- `virtual void paintEvent(QPaintEvent *) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QLineEdit::ActionPosition`

**作用与语义：**

该枚举类型描述了行编辑应如何显示待添加的动作控件。
- `QLineEdit::LeadingPosition`：`0`;使用布局方向`Qt::LeftToRight`时，控件显示在文本左侧，使用`Qt::RightToLeft`时显示在右侧。
- `QLineEdit::TrailingPosition`：`1`;使用布局方向`Qt::LeftToRight`时，控件显示在文本右侧，使用`Qt::RightToLeft`时显示在左侧。

### `enum QLineEdit::EchoMode`

**作用与语义：**

该枚举类型描述了行编辑应如何显示其内容。
- `QLineEdit::Normal`：`0`;输入字符时显示。这是默认设置。
- `QLineEdit::NoEcho`：`1`;不显示任何内容。这可能适用于连密码长度都应保密的密码。
- `QLineEdit::Password`：`2`;显示与平台相关的密码掩码字符，而非实际输入的字符。
- `QLineEdit::PasswordEchoOnEdit`：`3`;字符输入时仅显示。否则，像输入`Password`一样显示字符。

### `[read-only] acceptableInput : bool`

**作用与语义：**

该属性决定输入是否满足`inputMask`和验证者。
默认情况下，该属性为`true`。

**如何使用：** 调用 `acceptableInput()` 读取当前值；它不会修改应用状态。

### `alignment : Qt::Alignment`

**作用与语义：**

该属性表示了行编辑的对齐。
这里允许水平和垂直排列，`Qt::AlignJustify`映射到`Qt::AlignLeft`。
默认情况下，该属性包含`Qt::AlignLeft`和`Qt::AlignVCenter`的组合。

**如何使用：** 调用 `alignment()` 读取当前值；它不会修改应用状态。

### `clearButtonEnabled : bool`

**作用与语义：**

该属性适用于行编辑在未空时是否显示清除按钮。
如果启用，行编辑在包含文本时会显示一个尾部清除按钮。否则，行编辑不会显示清除按钮（默认设置）。

**如何使用：** 调用 `clearButtonEnabled()` 读取当前值；它不会修改应用状态。

### `cursorMoveStyle : Qt::CursorMoveStyle`

**作用与语义：**

该属性保留了该行编辑中光标的移动风格。
当该属性设置为`Qt::VisualMoveStyle`时，行编辑将使用视觉移动风格。使用左箭头键总是使光标向左移动，无论文本的书写方向如何。右箭头键同样适用。
当属性设置为`Qt::LogicalMoveStyle`（默认）时，在从左到右（LTR）的文本块中，使用左箭头键会增加光标位置，而使用右箭头键则会减少光标位置。如果文本块是从右到左（RTL），则相反的行为。

**如何使用：** 调用 `cursorMoveStyle()` 读取当前值；它不会修改应用状态。

### `cursorPosition : int`

**作用与语义：**

该属性表示当前该行编辑的光标位置。
设置光标位置时，需要重新涂装。
默认情况下，该属性的值为0。

**如何使用：** 调用 `cursorPosition()` 读取当前值；它不会修改应用状态。

### `[read-only] displayText : QString`

**作用与语义：**

该属性保留显示的文本。
如果`echoMode`是`Normal`，则返回与`text()`相同。如果`EchoMode`为`Password`或`PasswordEchoOnEdit`，则返回一串与平台相关的密码掩码字符（例如“******”）。如果`EchoMode`为`NoEcho`，则返回空字符串。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `displayText()` 读取当前值；它不会修改应用状态。

### `dragEnabled : bool`

**作用与语义：**

该属性是否适用于当用户在某些选定文本上按压并移动鼠标时，行编辑是否会启动拖动。
拖曳默认是被禁用的。

**如何使用：** 调用 `dragEnabled()` 读取当前值；它不会修改应用状态。

### `echoMode : EchoMode`

**作用与语义：**

该属性保留了行编辑的回声模式。
回声模式决定了在行编辑中输入的文本如何向用户显示（或回声）。
最常见的设置是`Normal`，用户输入的文本会被逐字显示。`QLineEdit`还支持可以抑制或遮挡输入文本的模式，包括`NoEcho`、`Password`和`PasswordEchoOnEdit`。
该设置会影响小部件的显示以及复制或拖拽文本的能力。
默认情况下，该属性设置为`Normal`。

**如何使用：** 调用 `echoMode()` 读取当前值；它不会修改应用状态。

### `frame : bool`

**作用与语义：**

该属性在线编辑是否用框架绘制时成立。
如果启用（默认），线编辑会在一个框架内绘制自己。否则，线编辑会在没有帧的情况下绘制自己。

**如何使用：** 调用 `frame()` 读取当前值；它不会修改应用状态。

### `[read-only] hasSelectedText : bool`

**作用与语义：**

该属性是否存在任何文本。
hasSelectedText() 返回 `true` 如果用户选择了部分或全部文本。否则返回 `false`。
默认情况下，该属性为`false`。

**如何使用：** 调用 `hasSelectedText()` 读取当前值；它不会修改应用状态。

### `inputMask : QString`

**作用与语义：**

该属性包含验证输入掩码。
设置`QLineEdit`的验证掩码。验证器可以替代或与掩码一起使用;参见`setValidator()`。默认是空字符串，意味着不使用输入掩码。
要解除遮罩并恢复正常`QLineEdit`操作，传递一个空字符串。
输入遮罩是一个输入模板字符串。它可以包含以下元素：
- `Mask Characters`：定义在此位置下被认为有效的输入字符的 `Category`。
- `Meta Characters`：各种特殊含义（详见下文）。
- `Separators`：所有其他字符都被视为不可变的分离符。
下表展示了输入掩码中可以使用的遮罩和元字符。
- `Mask Character`：含义
- `A`：字母类别的字符要求，如A-Z、a-z。
- `a`：字母类别的属性允许但非强制。
- `N`：需要字母或数字类别的字符，如A-Z、a-z、0-9。
- `n`：字母或数字类别的字符允许但非强制。
- `X`：任何非空白字符。
- `x`：允许但不强制使用任何非空白字符。
- `9`：需要数字类别的字符，如0-9。
- `0`：数字类别的属性允许但非强制。
- `D`：数字类别的特征且大于零，如1-9。
- `d`：数字类别的特征且大于零，允许但非必需，如1-9。
- `#`：数字类别的特征，或允许加减号，但非必需。
- `H`：需要十六进制字符。A-F，a-f，0-9。
- `h`：允许使用十六进制字符，但非强制。
- `B`：需要二进制字符。0-1.
- `b`：允许二进制字符，但非必需。
- `Meta Character`：含义
- `>`：后续所有字母均为大写字母。
- `<`：后续所有字母字符均为小写。
- `!`：关闭箱转换。
- `;c`：终止输入掩码，并将空白字符设置为 c。
- `[ ] { }`：预订。
- `\`：使用`\`跳脱上述特殊字符，将其用作分隔符。
创建或清除后，行编辑会填充输入蒙罩字符串的副本，其中元字符被移除，蒙罩字符被替换为空白字符（默认为`space`）。
当设置输入遮罩时，`text()`方法返回一个修改后的行编辑内容副本，其中所有空白字符都被移除。未修改的内容可以用`displayText()`读取。
如果当前行编辑内容不满足输入掩码的要求，`hasAcceptableInput()`方法返回为false。
示例：
- `Mask`：注释
- `000.000.000.000;_`：IP地址;空白部分`_`。
- `HH:HH:HH:HH:HH:HH;_`：MAC地址
- `0000-00-00`：ISO日期;空白`space`
- `>AAAAA-AAAAA-AAAAA-AAAAA-AAAAA;#`：执照号;空格为`#`，所有（字母）字符转换为大写字母。
要控制距离（例如IP地址），使用掩码和`validators`。

**如何使用：** 调用 `inputMask()` 读取当前值；它不会修改应用状态。

### `maxLength : int`

**作用与语义：**

该属性包含文本的最大允许长度。
如果文本过长，则在极限处截断。
如果发生截断，任何选中的文本都会被取消选择，光标位置设为0，并显示字符串的第一部分。
如果行编辑有输入遮罩，遮罩定义了最大字符串长度。
默认情况下，该属性的值为32767。

**如何使用：** 调用 `maxLength()` 读取当前值；它不会修改应用状态。

### `modified : bool`

**作用与语义：**

该属性决定了用户是否修改了行编辑的内容。
修改后的标志从不被`QLineEdit`读取;默认值为false，每当用户更改行编辑内容时，标记就会改为true。
这对于需要提供默认值但一开始就不知道默认值（例如，它依赖于表单中的其他字段）的情况非常有用。在没有最佳默认值的情况下开始行编辑，当已知默认值时，如果 modified() 返回 `false`（用户未输入任何文本），则插入默认值。
调用`setText()`会将修改后的标志重置为false。

**如何使用：** 调用 `modified()` 读取当前值；它不会修改应用状态。

### `placeholderText : QString`

**作用与语义：**

该属性包含行编辑的占位文本。
设置该属性后，行编辑显示的是一个灰色的占位文本，只要行编辑是空的。
通常，空行编辑即使有焦点也会显示占位符文本。然而，如果内容水平居中，当行编辑有焦点时，占位符文本不会显示在光标下方。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `placeholderText()` 读取当前值；它不会修改应用状态。

### `readOnly : bool`

**作用与语义：**

该属性决定了行编辑是否为只读。
在只读模式下，用户仍可将文本复制到剪贴板，或拖放文本（如果有`Normal` `echoMode()`），但无法编辑。
`QLineEdit` 在只读模式下不会显示光标。
默认情况下，该属性为`false`。

**如何使用：** 调用 `readOnly()` 读取当前值；它不会修改应用状态。

### `[read-only] redoAvailable : bool`

**作用与语义：**

该属性决定是否可重做。
当用户对行编辑中的文本执行一次或多次撤销操作后，重做才可重新启用。
默认情况下，该属性为`false`。

**如何使用：** 调用 `redoAvailable()` 读取当前值；它不会修改应用状态。

### `[read-only] selectedText : QString`

**作用与语义：**

该属性包含所选文本。
如果没有被选中的文本，则该属性的值为空字符串。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `selectedText()` 读取当前值；它不会修改应用状态。

### `text : QString`

**作用与语义：**

该属性包含行编辑的文本。
设置该属性会清除选择，清除撤销/重做历史，将光标移动到行尾，并将`modified`属性重置为false。当用 setText() 插入文本时，文本不会被验证。
文本被截断为`maxLength()`长度。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `text()` 读取当前值；它不会修改应用状态。

### `[read-only] undoAvailable : bool`

**作用与语义：**

该属性决定是否可撤销。
一旦用户修改了行编辑中的文本，撤销功能就会开放。
默认情况下，该属性为`false`。

**如何使用：** 调用 `undoAvailable()` 读取当前值；它不会修改应用状态。

### `[explicit] QLineEdit::QLineEdit(QWidget *parent = nullptr)`

**作用与语义：**

构造一个无文本的行编辑。
最大文本长度设置为32767个字符。
`parent`参数被发送给`QWidget`构造器。

### `[explicit] QLineEdit::QLineEdit(const QString &contents, QWidget *parent = nullptr)`

**作用与语义：**

构建包含文本 `contents` 作为 `parent` 子的行编辑。
光标位置设在行尾，文本最大长度为32767字符。

### `[virtual noexcept] QLineEdit::~QLineEdit()`

**作用与语义：**

这会破坏台词编辑。

### `void QLineEdit::addAction(QAction *action, QLineEdit::ActionPosition position)`

**作用与语义：**

将`action`添加到`position`的操作列表中。

### `QAction *QLineEdit::addAction(const QIcon &icon, QLineEdit::ActionPosition position)`

**作用与语义：**

创建一个新的动作，`position`处有给定的`icon`。

### `void QLineEdit::backspace()`

**作用与语义：**

如果未选择文本，则删除光标左侧的字符，并将光标向左移动一个位置。如果选择任何文本，光标移动到所选文本的开头，所选文本被删除。

### `[override virtual protected] void QLineEdit::changeEvent(QEvent *ev)`

**作用与语义：**

重装：`QWidget::changeEvent`（QEvent *事件）。
该事件处理程序可以重新实现以处理状态变化。
该事件中被更改的状态可以通过提供的`event`检索。
变更事件包括：`QEvent::ToolBarChange`、`QEvent::ActivationChange`、`QEvent::EnabledChange`、`QEvent::FontChange`、`QEvent::StyleChange`、`QEvent::PaletteChange`、`QEvent::WindowTitleChange`、`QEvent::IconTextChange`、`QEvent::ModifiedChange`、`QEvent::MouseTrackingChange`、`QEvent::ParentChange`、`QEvent::WindowStateChange`、`QEvent::LanguageChange`、`QEvent::LocaleChange`、`QEvent::LayoutDirectionChange`、`QEvent::ReadOnlyChange`。

### `[slot] void QLineEdit::clear()`

**作用与语义：**

清除行编辑内容。

### `QCompleter *QLineEdit::completer() const`

**作用与语义：**

返回当前提供完备的`QCompleter`。

### `[override virtual protected] void QLineEdit::contextMenuEvent(QContextMenuEvent *event)`

**作用与语义：**

重实现自：`QWidget::contextMenuEvent`（QContextMenuEvent *event）。
显示用`createStandardContextMenu()`创建的标准右键菜单。
如果你不希望行编辑带有右键菜单，可以将其`contextMenuPolicy`设置为`Qt::NoContextMenu`。要自定义右键菜单，请重新实现该函数。要扩展标准右键菜单，重新实现该功能，调用`createStandardContextMenu()`，并扩展返回的菜单。
`event`参数用于获取事件生成时鼠标光标的位置。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收控件上下文菜单事件。
当控件的 `contextMenuPolicy` 被`Qt::DefaultContextMenu`时调用处理器。
默认实现忽略上下文事件。详情请参见 `QContextMenuEvent` 文档。

**官方示例：**

```cpp
 void LineEdit::contextMenuEvent(QContextMenuEvent *event)
 {
     QMenu *menu = createStandardContextMenu();
     menu->addAction(tr("My Menu Item"));
     //...
     menu->exec(event->globalPos());
     delete menu;
 }
```

### `[slot] void QLineEdit::copy() const`

**作用与语义：**

如果有，`echoMode()` `Normal`，则将选中的文本复制到剪贴板上。

### `QMenu *QLineEdit::createStandardContextMenu()`

**作用与语义：**

创建标准的上下文菜单，用户用鼠标右键点击行编辑时会显示。它从默认的`contextMenuEvent()`处理程序中调用。弹出菜单的所有权会转移给调用者。

### `void QLineEdit::cursorBackward(bool mark, int steps = 1)`

**作用与语义：**

将光标往后移动`steps`字符。如果`mark`为真，则每移动一个字符都会加入选择中。如果`mark`为假，则该选择被清除。

### `void QLineEdit::cursorForward(bool mark, int steps = 1)`

**作用与语义：**

将光标向前移动字符`steps`。如果`mark`为真，则每个移过的字符都加入到选择中。如果`mark`为假，则该选择被清除。

### `int QLineEdit::cursorPositionAt(const QPoint &pos)`

**作用与语义：**

返回点`pos`下方的光标位置。

### `[signal] void QLineEdit::cursorPositionChanged(int oldPos, int newPos)`

**作用与语义：**

该信号在光标移动时发出。之前的位置由`oldPos`表示，新位置由`newPos`表示。

### `[protected] QRect QLineEdit::cursorRect() const`

**作用与语义：**

返回一个包含行编辑光标的矩形。

### `void QLineEdit::cursorWordBackward(bool mark)`

**作用与语义：**

将光标向后移动一个单词。如果`mark`为真，该单词也会被选中。

### `void QLineEdit::cursorWordForward(bool mark)`

**作用与语义：**

将光标向前移动一个单词。如果`mark`为真，则该单词也被选中。

### `[slot] void QLineEdit::cut()`

**作用与语义：**

将选中的文本复制到剪贴板，如果有的话删除，且`Normal` `echoMode()`。
如果当前验证者不允许删除所选文本，cut() 将复制但不删除。

### `void QLineEdit::del()`

**作用与语义：**

如果未选择文本，则删除光标右侧的字符。如果选择任何文本，光标会移动到所选文本的开头，并删除所选文本。

### `void QLineEdit::deselect()`

**作用与语义：**

取消选择任何选中的文本。

### `[override virtual protected] void QLineEdit::dragEnterEvent(QDragEnterEvent *e)`

**作用与语义：**

重实现自：`QWidget::dragEnterEvent`（QDragEnterEvent *event）。
当拖拽进行中且鼠标进入该控件时，调用该事件处理程序。事件通过`event`参数传递。
如果事件被忽略，小部件将不会接收任何拖动动作事件。
请参阅拖放文档，了解如何在申请中提供拖放功能的概览。

### `[override virtual protected] void QLineEdit::dragLeaveEvent(QDragLeaveEvent *e)`

**作用与语义：**

重实现自：`QWidget::dragLeaveEvent`（QDragLeaveEvent *event）。
当拖拽进行且鼠标离开该控件时，调用该事件处理程序。事件通过`event`参数传递。
请参阅拖放文档，了解如何在申请中提供拖放功能的概览。

### `[override virtual protected] void QLineEdit::dragMoveEvent(QDragMoveEvent *e)`

**作用与语义：**

重实现自：`QWidget::dragMoveEvent`（QDragMoveEvent *event）。
当拖拽正在进行中，且发生以下任一条件时，会调用该事件处理程序：光标进入该控件、光标在控件内移动，或在该控件拥有焦点时按下键盘上的修饰键。事件通过 `event` 参数传递。
请参阅拖放文档，了解如何在申请中提供拖放功能的概览。

### `[override virtual protected] void QLineEdit::dropEvent(QDropEvent *e)`

**作用与语义：**

重实现自：`QWidget::dropEvent`（QDropEvent *event）。
当拖拽该控件时调用该事件处理程序。事件通过`event`参数传递。
请参阅拖放文档，了解如何在申请中提供拖放功能的概览。

### `[signal] void QLineEdit::editingFinished()`

**作用与语义：**

当使用回车键或回车键，或行编辑失去焦点且内容自上次发出以来发生变化时，会发出该信号。
注意：如果在编辑和回车线上设置了`validator()`或`inputMask()`，只有当输入跟随`inputMask()`且`validator()`返回`QValidator::Acceptable`时才会发出editingFinished()信号。

### `void QLineEdit::end(bool mark)`

**作用与语义：**

将文本光标移动到行尾，除非已经在那里。如果`mark`为真，文本会被选中到最后一个位置。否则，只要光标移动，任何被选中的文本都会取消。

### `[override virtual] bool QLineEdit::event(QEvent *e)`

**作用与语义：**

重实现自：`QWidget::event`（QEvent *事件）。

### `[override virtual protected] void QLineEdit::focusInEvent(QFocusEvent *e)`

**作用与语义：**

重实现自：`QWidget::focusInEvent`（QFocusEvent *event）。
该事件处理程序可以在子类中重新实现，以接收控件的键盘焦点事件（焦点接收）。事件通过`event`参数传递。
小部件通常必须`setFocusPolicy()`到非`Qt::NoFocus`的对象才能接收焦点事件。（注意，应用程序员可以调用任何小部件`setFocus()`，即使是那些通常不接受焦点的小部件。）。
默认实现会更新小部件（除非是没有指定`focusPolicy()`的窗口）。

### `[override virtual protected] void QLineEdit::focusOutEvent(QFocusEvent *e)`

**作用与语义：**

重现：`QWidget::focusOutEvent`（QFocusEvent *event）。
该事件处理程序可以在子类中重新实现，以接收控件的键盘焦点事件（焦点丢失）。事件通过`event`参数传递。
小部件通常必须`setFocusPolicy()`到非`Qt::NoFocus`的对象才能接收焦点事件。（注意，应用程序员可以调用任何小部件`setFocus()`，即使是那些通常不接受焦点的小部件。）。
默认实现会更新小部件（除非是没有指定`focusPolicy()`的窗口）。

### `void QLineEdit::home(bool mark)`

**作用与语义：**

将文本光标移动到行的开头，除非它已经存在。如果`mark`为真，文本会被选中到第一个位置。否则，只要光标移动，任何被选中的文本都会被取消选择。

### `[virtual protected] void QLineEdit::initStyleOption(QStyleOptionFrame *option) const`

**作用与语义：**

用这个`QLineEdit`的值初始化`option`。这种方法适用于需要`QStyleOptionFrame`但不想自己填满所有信息的子类。

### `[override virtual protected] void QLineEdit::inputMethodEvent(QInputMethodEvent *e)`

**作用与语义：**

重实现自：`QWidget::inputMethodEvent`（QInputMethodEvent *event）。
对于事件`event`，该事件处理程序可以被重新实现到子类中以接收输入法组合事件。当输入方法的状态发生变化时，调用该处理程序。
注意，在创建自定义文本编辑小部件时，必须明确设置`Qt::WA_InputMethodEnabled`窗口属性（使用`setAttribute()`函数），才能接收输入法事件。
默认实现调用 event->ignore()，拒绝输入法事件。详情请参见 `QInputMethodEvent` 文档。

### `[override virtual] QVariant QLineEdit::inputMethodQuery(Qt::InputMethodQuery property) const`

**作用与语义：**

重实现自：`QWidget::inputMethodQuery`（Qt：：InputMethodQuery query） const.
该方法仅适用于输入控件。输入方法用于查询控件的一组属性，以支持复杂的输入法操作，以支持周围文本和重新转换。
`query` 指定查询的属性。

### `[signal] void QLineEdit::inputRejected()`

**作用与语义：**

当用户使用不被视为有效输入的密钥时，会发出该信号。例如，如果使用密钥导致验证者`validate()`返回`Invalid`。另一种情况是尝试输入超过行编辑最大长度的字符。
注意：当仅接受部分文本时，该信号仍会发出。例如，如果设定了最大长度，且剪贴板文本长度超过粘贴时的最大长度。

### `void QLineEdit::insert(const QString &newText)`

**作用与语义：**

删除任何选中的文本，插入`newText`，并验证结果。如果有效，则将新文本设置为行编辑的新内容。

### `[override virtual protected] void QLineEdit::keyPressEvent(QKeyEvent *event)`

**作用与语义：**

重实现自：`QWidget::keyPressEvent`（QKeyEvent *event）。
将给定的按键`event`转换为行编辑动作。
如果使用返回或回车，且当前文本有效（或验证者可以使文本有效），则发出信号`returnPressed()`。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收小部件的按键事件。
一个小部件必须先调用`setFocusPolicy()`接受焦点，并且拥有焦点才能接收按键事件。
如果你重新实现这个处理器，如果你不对密钥进行操作，务必调用基类实现。
默认实现会关闭弹出小部件，如果用户按下`QKeySequence::Cancel`的按键序列（通常是Escape键）。否则该事件会被忽略，以便小部件的父节点能够解释。
注意`QKeyEvent`以 isAccepted() == true 开头，所以你不需要调用 `QKeyEvent::accept()`——只要你对密钥操作时不要调用基类实现即可。

### `[override virtual protected] void QLineEdit::keyReleaseEvent(QKeyEvent *e)`

**作用与语义：**

重实现自：`QWidget::keyReleaseEvent`（QKeyEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该小部件的密钥释放事件。
小部件必须先接受焦点并拥有焦点，才能接收密钥释放事件。
如果你重新实现这个处理器，如果你不对密钥进行操作，务必调用基类实现。
默认实现忽略事件，以便小部件的父节点能够解释事件。
注意`QKeyEvent`以 isAccepted() == true开头，所以你不需要调用`QKeyEvent::accept()`——只要你对密钥操作时不要调用基类实现即可。

### `[override virtual] QSize QLineEdit::minimumSizeHint() const`

**作用与语义：**

重新实现了属性的访问函数：`QWidget::minimumSizeHint`。
返回行编辑的最小尺寸。
返回的宽度通常足够至少一个字符使用。

### `[override virtual protected] void QLineEdit::mouseDoubleClickEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QWidget::mouseDoubleClickEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收小部件的鼠标双击事件。
默认实现调用`mousePressEvent()`。
注意：该小部件除了双击事件外，还会接收鼠标按键和鼠标释放事件。如果与该小部件重叠的其他小部件在新闻发布事件后消失，则该小部件只会接收双击事件。开发者有责任确保应用程序正确解读这些事件。

### `[override virtual protected] void QLineEdit::mouseMoveEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QWidget::mouseMoveEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标移动事件。
如果关闭鼠标追踪，只有在鼠标移动过程中按下鼠标按钮时才会发生鼠标移动事件。如果开启鼠标追踪，即使未按键，鼠标移动事件也会发生。
`QMouseEvent::position()`报告鼠标光标相对于该小部件的位置。对于按下和释放事件，位置通常与最后一次鼠标移动事件的位置相同，但如果用户的手握手，可能会有所不同。这是底层窗口系统的功能，而非Qt。
如果你想在鼠标移动时立即显示提示（例如，获取鼠标坐标与`QMouseEvent::position()`并显示为提示），你必须先启用上述的鼠标追踪功能。然后，为了确保提示立即更新，你必须在鼠标移动事件（mouseMoveEvent）实现中调用`QToolTip::showText()`而不是`setToolTip()`。

### `[override virtual protected] void QLineEdit::mousePressEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QWidget::mousePressEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标按键事件。
如果你在 mousePressEvent() 创建新控件，`mouseReleaseEvent()`可能不会出现在你预期的位置，这取决于底层窗口系统（或 X11 窗口管理器）、控件的位置，甚至可能还有其他因素。
默认实现实现了当你点击窗口外时关闭弹出小部件的功能。对于其他小部件类型，它没有任何作用。

### `[override virtual protected] void QLineEdit::mouseReleaseEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QWidget::mouseReleaseEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标释放事件。

### `[override virtual protected] void QLineEdit::paintEvent(QPaintEvent *)`

**作用与语义：**

重实现自：`QWidget::paintEvent`（QPaintEvent *event）。
该事件处理程序可以在子类中重新实现，以接收 `event` 传递的绘画事件。
绘图事件是请求重新绘制一个小部件的全部或部分。它可能由以下原因之一发生：
- `repaint()`或`update()`被援引，
- 小部件被遮挡，现已被发现，或
- 还有很多其他原因。
许多控件可以在被要求时重新绘制整个表面，但一些慢速控件需要通过仅绘制请求的区域来优化：`QPaintEvent::region()`。这种速度优化不会改变结果，因为在事件处理过程中绘制会被裁剪到该区域。例如，`QListView`和`QTableView`就是这样做的。
Qt 还试图通过将多个绘画事件合并为一个来加快绘画速度。当 `update()` 被多次调用或窗口系统发送多个绘画事件时，Qt 会将这些事件合并为一个区域更大的事件（参见 `QRegion::united()`）。`repaint()` 函数不支持这种优化，因此我们建议尽可能使用 `update()`。
当绘制事件发生时，更新区域通常已经被擦除，所以你是在小部件的背景上作画。
背景可以用`setBackgroundRole()`和`setPalette()`设置。
自 Qt 4.0 起，`QWidget` 会自动双缓冲绘制，因此无需在 paintEvent() 中编写双缓冲代码以避免闪烁。
注意：通常，你应避免在paintEvent()中调用`update()`或`repaint()`。例如，在paintEvent()中调用`update()`或`repaint()`会导致行为未定义;孩子可能会或不会获得绘画事件。
警告：如果你使用没有 Qt backingstore 的自定义绘图引擎，`Qt::WA_PaintOnScreen`必须设置。否则，`QWidget::paintEngine()` 永远不会被调用;Backingstore 将被使用。

### `[slot] void QLineEdit::paste()`

**作用与语义：**

在光标位置插入剪贴板文本，删除任何选中的文本，前提是行编辑未`read-only`。
如果最终结果对当前`validator`无效，则什么都不会发生。

### `[slot] void QLineEdit::redo()`

**作用与语义：**

如果重做是`available`，就重新做上一次操作。

### `[signal] void QLineEdit::returnPressed()`

**作用与语义：**

当使用返回键或回车键时，会发出该信号。
注意：如果线编辑设置了`validator()`或`inputMask()`，returnPressed() 信号只有在输入跟随`inputMask()`且 `validator()` 返回`QValidator::Acceptable`时才会发出。

### `[slot] void QLineEdit::selectAll()`

**作用与语义：**

选择所有文本（高亮显示），并将光标移动到末尾。
注意：当默认值已插入时，这很有用，因为如果用户在点击小部件前输入，所选文本将被删除。

### `[signal] void QLineEdit::selectionChanged()`

**作用与语义：**

每当选择发生变化时，该信号都会发出。

### `int QLineEdit::selectionEnd() const`

**作用与语义：**

在行编辑中返回字符的索引，直接返回选中后面的索引（如果没有选择文本，则返回-1）。

### `int QLineEdit::selectionLength() const`

**作用与语义：**

返回选择长度。

### `int QLineEdit::selectionStart() const`

**作用与语义：**

返回行编辑中第一个被选中的字符索引（如果未选择文本则返回-1）。

### `void QLineEdit::setCompleter(QCompleter *c)`

**作用与语义：**

将该行编辑设置为从补全器中自动补全，`c`。补全模式通过`QCompleter::setCompletionMode()`设置。
要使用带有`QValidator`或`QLineEdit::inputMask`的`QCompleter`，你需要确保提供给`QCompleter`的模型包含有效的条目。你可以用`QSortFilterProxyModel`确保`QCompleter`的模型只包含有效的条目。
要移除补全器并禁用自动补全，请传递一个`nullptr`。

### `void QLineEdit::setSelection(int start, int length)`

**作用与语义：**

从`start`和`length`字符的位置选择文本。允许负长度。

### `void QLineEdit::setTextMargins(const QMargins &margins)`

**作用与语义：**

在框架内的文字周围设置`margins`。

### `void QLineEdit::setTextMargins(int left, int top, int right, int bottom)`

**作用与语义：**

将框内文本的边距设置为大小为`left`、`top`、`right`和`bottom`。

### `void QLineEdit::setValidator(const QValidator *v)`

**作用与语义：**

将行编辑值的验证器设置为`v`。
行编辑的`returnPressed()`和`editingFinished()`信号只有在`v`验证行编辑内容为`Acceptable`时才会发出。用户在编辑过程中可以将内容更改为任意`Intermediate`值，但将被禁止编辑到`v`验证为`Invalid`值。
这允许你限制编辑时存储的文本，同时保留用户足够的自由度将文本从一个有效状态编辑到另一个有效状态。
要移除当前输入验证器，通过`nullptr`。初始设置是没有输入验证器（任何输入都接受，最高可达`maxLength()`）。

### `[override virtual] QSize QLineEdit::sizeHint() const`

**作用与语义：**

重新实现属性的访问函数：`QWidget::sizeHint`。
返回小部件的推荐尺寸。
返回的宽度（以像素计）通常足够支持大约15到20个字符。

### `[signal] void QLineEdit::textChanged(const QString &text)`

**作用与语义：**

该属性包含行编辑的文本。
设置该属性会清除选择，清除撤销/重做历史，将光标移动到行尾，并将`modified`属性重置为false。当用 setText() 插入文本时，文本不会被验证。
文本被截断为`maxLength()`长度。
默认情况下，该属性包含空字符串。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `text` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QLineEdit::textEdited(const QString &text)`

**作用与语义：**

该信号在文本编辑时发出。`text`论元是新文本。
与`textChanged()`不同，当文本程序性更改时，例如调用`setText()`，不会发出该信号。

### `QMargins QLineEdit::textMargins() const`

**作用与语义：**

返回小部件的文本边距。

### `[override virtual] void QLineEdit::timerEvent(QTimerEvent *e)`

**作用与语义：**

重实现自：`QObject::timerEvent`（QTimerEvent *event）。

### `[slot] void QLineEdit::undo()`

**作用与语义：**

如果撤销`available`，则撤销上一次操作。取消当前选择，并将选择开始更新为当前光标位置。

### `const QValidator *QLineEdit::validator() const`

**作用与语义：**

返回当前输入验证器的指针，若未设置验证器则返回`nullptr`。

### `Qt::Alignment alignment() const`

**作用与语义：**

该属性表示了行编辑的对齐。
这里允许水平和垂直排列，`Qt::AlignJustify`映射到`Qt::AlignLeft`。
默认情况下，该属性包含`Qt::AlignLeft`和`Qt::AlignVCenter`的组合。

**如何使用：** 调用 `alignment()` 读取当前值；它不会修改应用状态。

### `Qt::CursorMoveStyle cursorMoveStyle() const`

**作用与语义：**

该属性保留了该行编辑中光标的移动风格。
当该属性设置为`Qt::VisualMoveStyle`时，行编辑将使用视觉移动风格。使用左箭头键总是使光标向左移动，无论文本的书写方向如何。右箭头键同样适用。
当属性设置为`Qt::LogicalMoveStyle`（默认）时，在从左到右（LTR）的文本块中，使用左箭头键会增加光标位置，而使用右箭头键则会减少光标位置。如果文本块是从右到左（RTL），则相反的行为。

**如何使用：** 调用 `cursorMoveStyle()` 读取当前值；它不会修改应用状态。

### `int cursorPosition() const`

**作用与语义：**

该属性表示当前该行编辑的光标位置。
设置光标位置时，需要重新涂装。
默认情况下，该属性的值为0。

**如何使用：** 调用 `cursorPosition()` 读取当前值；它不会修改应用状态。

### `QString displayText() const`

**作用与语义：**

该属性保留显示的文本。
如果`echoMode`是`Normal`，则返回与`text()`相同。如果`EchoMode`为`Password`或`PasswordEchoOnEdit`，则返回一串与平台相关的密码掩码字符（例如“******”）。如果`EchoMode`为`NoEcho`，则返回空字符串。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `displayText()` 读取当前值；它不会修改应用状态。

### `bool dragEnabled() const`

**作用与语义：**

该属性是否适用于当用户在某些选定文本上按压并移动鼠标时，行编辑是否会启动拖动。
拖曳默认是被禁用的。

**如何使用：** 调用 `dragEnabled()` 读取当前值；它不会修改应用状态。

### `QLineEdit::EchoMode echoMode() const`

**作用与语义：**

该属性保留了行编辑的回声模式。
回声模式决定了在行编辑中输入的文本如何向用户显示（或回声）。
最常见的设置是`Normal`，用户输入的文本会被逐字显示。`QLineEdit`还支持可以抑制或遮挡输入文本的模式，包括`NoEcho`、`Password`和`PasswordEchoOnEdit`。
该设置会影响小部件的显示以及复制或拖拽文本的能力。
默认情况下，该属性设置为`Normal`。

**如何使用：** 调用 `echoMode()` 读取当前值；它不会修改应用状态。

### `bool hasAcceptableInput() const`

**作用与语义：**

该属性决定输入是否满足`inputMask`和验证者。
默认情况下，该属性为`true`。

**如何使用：** 调用 `hasAcceptableInput()` 读取当前值；它不会修改应用状态。

### `bool hasFrame() const`

**作用与语义：**

该属性在线编辑是否用框架绘制时成立。
如果启用（默认），线编辑会在一个框架内绘制自己。否则，线编辑会在没有帧的情况下绘制自己。

**如何使用：** 调用 `hasFrame()` 读取当前值；它不会修改应用状态。

### `bool hasSelectedText() const`

**作用与语义：**

该属性是否存在任何文本。
hasSelectedText() 返回 `true` 如果用户选择了部分或全部文本。否则返回 `false`。
默认情况下，该属性为`false`。

**如何使用：** 调用 `hasSelectedText()` 读取当前值；它不会修改应用状态。

### `QString inputMask() const`

**作用与语义：**

该属性包含验证输入掩码。
设置`QLineEdit`的验证掩码。验证器可以替代或与掩码一起使用;参见`setValidator()`。默认是空字符串，意味着不使用输入掩码。
要解除遮罩并恢复正常`QLineEdit`操作，传递一个空字符串。
输入遮罩是一个输入模板字符串。它可以包含以下元素：
- `Mask Characters`：定义在此位置下被认为有效的输入字符的 `Category`。
- `Meta Characters`：各种特殊含义（详见下文）。
- `Separators`：所有其他字符都被视为不可变的分离符。
下表展示了输入掩码中可以使用的遮罩和元字符。
- `Mask Character`：含义
- `A`：字母类别的字符要求，如A-Z、a-z。
- `a`：字母类别的属性允许但非强制。
- `N`：需要字母或数字类别的字符，如A-Z、a-z、0-9。
- `n`：字母或数字类别的字符允许但非强制。
- `X`：任何非空白字符。
- `x`：允许但不强制使用任何非空白字符。
- `9`：需要数字类别的字符，如0-9。
- `0`：数字类别的属性允许但非强制。
- `D`：数字类别的特征且大于零，如1-9。
- `d`：数字类别的特征且大于零，允许但非必需，如1-9。
- `#`：数字类别的特征，或允许加减号，但非必需。
- `H`：需要十六进制字符。A-F，a-f，0-9。
- `h`：允许使用十六进制字符，但非强制。
- `B`：需要二进制字符。0-1.
- `b`：允许二进制字符，但非必需。
- `Meta Character`：含义
- `>`：后续所有字母均为大写字母。
- `<`：后续所有字母字符均为小写。
- `!`：关闭箱转换。
- `;c`：终止输入掩码，并将空白字符设置为 c。
- `[ ] { }`：预订。
- `\`：使用`\`跳脱上述特殊字符，将其用作分隔符。
创建或清除后，行编辑会填充输入蒙罩字符串的副本，其中元字符被移除，蒙罩字符被替换为空白字符（默认为`space`）。
当设置输入遮罩时，`text()`方法返回一个修改后的行编辑内容副本，其中所有空白字符都被移除。未修改的内容可以用`displayText()`读取。
如果当前行编辑内容不满足输入掩码的要求，`hasAcceptableInput()`方法返回为false。
示例：
- `Mask`：注释
- `000.000.000.000;_`：IP地址;空白部分`_`。
- `HH:HH:HH:HH:HH:HH;_`：MAC地址
- `0000-00-00`：ISO日期;空白`space`
- `>AAAAA-AAAAA-AAAAA-AAAAA-AAAAA;#`：执照号;空格为`#`，所有（字母）字符转换为大写字母。
要控制距离（例如IP地址），使用掩码和`validators`。

**如何使用：** 调用 `inputMask()` 读取当前值；它不会修改应用状态。

### `bool isClearButtonEnabled() const`

**作用与语义：**

该属性适用于行编辑在未空时是否显示清除按钮。
如果启用，行编辑在包含文本时会显示一个尾部清除按钮。否则，行编辑不会显示清除按钮（默认设置）。

**如何使用：** 调用 `isClearButtonEnabled()` 读取当前值；它不会修改应用状态。

### `bool isModified() const`

**作用与语义：**

该属性决定了用户是否修改了行编辑的内容。
修改后的标志从不被`QLineEdit`读取;默认值为false，每当用户更改行编辑内容时，标记就会改为true。
这对于需要提供默认值但一开始就不知道默认值（例如，它依赖于表单中的其他字段）的情况非常有用。在没有最佳默认值的情况下开始行编辑，当已知默认值时，如果 modified() 返回 `false`（用户未输入任何文本），则插入默认值。
调用`setText()`会将修改后的标志重置为false。

**如何使用：** 调用 `isModified()` 读取当前值；它不会修改应用状态。

### `bool isReadOnly() const`

**作用与语义：**

该属性决定了行编辑是否为只读。
在只读模式下，用户仍可将文本复制到剪贴板，或拖放文本（如果有`Normal` `echoMode()`），但无法编辑。
`QLineEdit` 在只读模式下不会显示光标。
默认情况下，该属性为`false`。

**如何使用：** 调用 `isReadOnly()` 读取当前值；它不会修改应用状态。

### `bool isRedoAvailable() const`

**作用与语义：**

该属性决定是否可重做。
当用户对行编辑中的文本执行一次或多次撤销操作后，重做才可重新启用。
默认情况下，该属性为`false`。

**如何使用：** 调用 `isRedoAvailable()` 读取当前值；它不会修改应用状态。

### `bool isUndoAvailable() const`

**作用与语义：**

该属性决定是否可撤销。
一旦用户修改了行编辑中的文本，撤销功能就会开放。
默认情况下，该属性为`false`。

**如何使用：** 调用 `isUndoAvailable()` 读取当前值；它不会修改应用状态。

### `int maxLength() const`

**作用与语义：**

该属性包含文本的最大允许长度。
如果文本过长，则在极限处截断。
如果发生截断，任何选中的文本都会被取消选择，光标位置设为0，并显示字符串的第一部分。
如果行编辑有输入遮罩，遮罩定义了最大字符串长度。
默认情况下，该属性的值为32767。

**如何使用：** 调用 `maxLength()` 读取当前值；它不会修改应用状态。

### `QString placeholderText() const`

**作用与语义：**

该属性包含行编辑的占位文本。
设置该属性后，行编辑显示的是一个灰色的占位文本，只要行编辑是空的。
通常，空行编辑即使有焦点也会显示占位符文本。然而，如果内容水平居中，当行编辑有焦点时，占位符文本不会显示在光标下方。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `placeholderText()` 读取当前值；它不会修改应用状态。

### `QString selectedText() const`

**作用与语义：**

该属性包含所选文本。
如果没有被选中的文本，则该属性的值为空字符串。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `selectedText()` 读取当前值；它不会修改应用状态。

### `void setAlignment(Qt::Alignment flag)`

**作用与语义：**

该属性表示了行编辑的对齐。
这里允许水平和垂直排列，`Qt::AlignJustify`映射到`Qt::AlignLeft`。
默认情况下，该属性包含`Qt::AlignLeft`和`Qt::AlignVCenter`的组合。

**如何使用：** 调用 `setAlignment(...)` 修改 `alignment`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setClearButtonEnabled(bool enable)`

**作用与语义：**

该属性适用于行编辑在未空时是否显示清除按钮。
如果启用，行编辑在包含文本时会显示一个尾部清除按钮。否则，行编辑不会显示清除按钮（默认设置）。

**如何使用：** 调用 `setClearButtonEnabled(...)` 修改 `clearButtonEnabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setCursorMoveStyle(Qt::CursorMoveStyle style)`

**作用与语义：**

该属性保留了该行编辑中光标的移动风格。
当该属性设置为`Qt::VisualMoveStyle`时，行编辑将使用视觉移动风格。使用左箭头键总是使光标向左移动，无论文本的书写方向如何。右箭头键同样适用。
当属性设置为`Qt::LogicalMoveStyle`（默认）时，在从左到右（LTR）的文本块中，使用左箭头键会增加光标位置，而使用右箭头键则会减少光标位置。如果文本块是从右到左（RTL），则相反的行为。

**如何使用：** 调用 `setCursorMoveStyle(...)` 修改 `cursorMoveStyle`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setCursorPosition(int)`

**作用与语义：**

该属性表示当前该行编辑的光标位置。
设置光标位置时，需要重新涂装。
默认情况下，该属性的值为0。

**如何使用：** 调用 `setCursorPosition(...)` 修改 `cursorPosition`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDragEnabled(bool b)`

**作用与语义：**

该属性是否适用于当用户在某些选定文本上按压并移动鼠标时，行编辑是否会启动拖动。
拖曳默认是被禁用的。

**如何使用：** 调用 `setDragEnabled(...)` 修改 `dragEnabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setEchoMode(QLineEdit::EchoMode)`

**作用与语义：**

该属性保留了行编辑的回声模式。
回声模式决定了在行编辑中输入的文本如何向用户显示（或回声）。
最常见的设置是`Normal`，用户输入的文本会被逐字显示。`QLineEdit`还支持可以抑制或遮挡输入文本的模式，包括`NoEcho`、`Password`和`PasswordEchoOnEdit`。
该设置会影响小部件的显示以及复制或拖拽文本的能力。
默认情况下，该属性设置为`Normal`。

**如何使用：** 调用 `setEchoMode(...)` 修改 `echoMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFrame(bool)`

**作用与语义：**

该属性在线编辑是否用框架绘制时成立。
如果启用（默认），线编辑会在一个框架内绘制自己。否则，线编辑会在没有帧的情况下绘制自己。

**如何使用：** 调用 `setFrame(...)` 修改 `frame`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setInputMask(const QString &inputMask)`

**作用与语义：**

该属性包含验证输入掩码。
设置`QLineEdit`的验证掩码。验证器可以替代或与掩码一起使用;参见`setValidator()`。默认是空字符串，意味着不使用输入掩码。
要解除遮罩并恢复正常`QLineEdit`操作，传递一个空字符串。
输入遮罩是一个输入模板字符串。它可以包含以下元素：
- `Mask Characters`：定义在此位置下被认为有效的输入字符的 `Category`。
- `Meta Characters`：各种特殊含义（详见下文）。
- `Separators`：所有其他字符都被视为不可变的分离符。
下表展示了输入掩码中可以使用的遮罩和元字符。
- `Mask Character`：含义
- `A`：字母类别的字符要求，如A-Z、a-z。
- `a`：字母类别的属性允许但非强制。
- `N`：需要字母或数字类别的字符，如A-Z、a-z、0-9。
- `n`：字母或数字类别的字符允许但非强制。
- `X`：任何非空白字符。
- `x`：允许但不强制使用任何非空白字符。
- `9`：需要数字类别的字符，如0-9。
- `0`：数字类别的属性允许但非强制。
- `D`：数字类别的特征且大于零，如1-9。
- `d`：数字类别的特征且大于零，允许但非必需，如1-9。
- `#`：数字类别的特征，或允许加减号，但非必需。
- `H`：需要十六进制字符。A-F，a-f，0-9。
- `h`：允许使用十六进制字符，但非强制。
- `B`：需要二进制字符。0-1.
- `b`：允许二进制字符，但非必需。
- `Meta Character`：含义
- `>`：后续所有字母均为大写字母。
- `<`：后续所有字母字符均为小写。
- `!`：关闭箱转换。
- `;c`：终止输入掩码，并将空白字符设置为 c。
- `[ ] { }`：预订。
- `\`：使用`\`跳脱上述特殊字符，将其用作分隔符。
创建或清除后，行编辑会填充输入蒙罩字符串的副本，其中元字符被移除，蒙罩字符被替换为空白字符（默认为`space`）。
当设置输入遮罩时，`text()`方法返回一个修改后的行编辑内容副本，其中所有空白字符都被移除。未修改的内容可以用`displayText()`读取。
如果当前行编辑内容不满足输入掩码的要求，`hasAcceptableInput()`方法返回为false。
示例：
- `Mask`：注释
- `000.000.000.000;_`：IP地址;空白部分`_`。
- `HH:HH:HH:HH:HH:HH;_`：MAC地址
- `0000-00-00`：ISO日期;空白`space`
- `>AAAAA-AAAAA-AAAAA-AAAAA-AAAAA;#`：执照号;空格为`#`，所有（字母）字符转换为大写字母。
要控制距离（例如IP地址），使用掩码和`validators`。

**如何使用：** 调用 `setInputMask(...)` 修改 `inputMask`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMaxLength(int)`

**作用与语义：**

该属性包含文本的最大允许长度。
如果文本过长，则在极限处截断。
如果发生截断，任何选中的文本都会被取消选择，光标位置设为0，并显示字符串的第一部分。
如果行编辑有输入遮罩，遮罩定义了最大字符串长度。
默认情况下，该属性的值为32767。

**如何使用：** 调用 `setMaxLength(...)` 修改 `maxLength`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setModified(bool)`

**作用与语义：**

该属性决定了用户是否修改了行编辑的内容。
修改后的标志从不被`QLineEdit`读取;默认值为false，每当用户更改行编辑内容时，标记就会改为true。
这对于需要提供默认值但一开始就不知道默认值（例如，它依赖于表单中的其他字段）的情况非常有用。在没有最佳默认值的情况下开始行编辑，当已知默认值时，如果 modified() 返回 `false`（用户未输入任何文本），则插入默认值。
调用`setText()`会将修改后的标志重置为false。

**如何使用：** 调用 `setModified(...)` 修改 `modified`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPlaceholderText(const QString &)`

**作用与语义：**

该属性包含行编辑的占位文本。
设置该属性后，行编辑显示的是一个灰色的占位文本，只要行编辑是空的。
通常，空行编辑即使有焦点也会显示占位符文本。然而，如果内容水平居中，当行编辑有焦点时，占位符文本不会显示在光标下方。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `setPlaceholderText(...)` 修改 `placeholderText`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setReadOnly(bool)`

**作用与语义：**

该属性决定了行编辑是否为只读。
在只读模式下，用户仍可将文本复制到剪贴板，或拖放文本（如果有`Normal` `echoMode()`），但无法编辑。
`QLineEdit` 在只读模式下不会显示光标。
默认情况下，该属性为`false`。

**如何使用：** 调用 `setReadOnly(...)` 修改 `readOnly`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QString text() const`

**作用与语义：**

该属性包含行编辑的文本。
设置该属性会清除选择，清除撤销/重做历史，将光标移动到行尾，并将`modified`属性重置为false。当用 setText() 插入文本时，文本不会被验证。
文本被截断为`maxLength()`长度。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `text()` 读取当前值；它不会修改应用状态。

### `void setText(const QString &)`

**作用与语义：**

该属性包含行编辑的文本。
设置该属性会清除选择，清除撤销/重做历史，将光标移动到行尾，并将`modified`属性重置为false。当用 setText() 插入文本时，文本不会被验证。
文本被截断为`maxLength()`长度。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `setText(...)` 修改 `text`；传入的新值会成为后续查询和相关界面行为所使用的值。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

textChanged 可能高频触发；不能只依赖 validator 当作业务校验；密码框不要记录日志；提交前仍要检查空值和业务约束。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QLineEdit` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
