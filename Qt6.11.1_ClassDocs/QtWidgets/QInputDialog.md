# QInputDialog

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QInputDialog` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QInputDialog` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QInputDialog>`
- 继承自：QDialog
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum InputDialogOption { NoButtons, UseListViewForComboBoxItems, UsePlainTextEditForTextInput }`
- `flags InputDialogOptions`
- `enum InputMode { TextInput, IntInput, DoubleInput }`

### 属性

- `cancelButtonText : QString`
- `comboBoxEditable : bool`
- `comboBoxItems : QStringList`
- `doubleDecimals : int`
- `doubleMaximum : double`
- `doubleMinimum : double`
- `doubleStep : double`
- `doubleValue : int`
- `inputMode : InputMode`
- `intMaximum : int`
- `intMinimum : int`
- `intStep : int`
- `intValue : int`
- `labelText : QString`
- `okButtonText : QString`
- `options : InputDialogOptions`
- `textEchoMode : QLineEdit::EchoMode`
- `textValue : QString`

### 公有函数

- `QInputDialog(QWidget *parent = nullptr, Qt::WindowFlags flags = Qt::WindowFlags())`
- `virtual ~QInputDialog()`
- `QString cancelButtonText() const`
- `QStringList comboBoxItems() const`
- `int doubleDecimals() const`
- `double doubleMaximum() const`
- `double doubleMinimum() const`
- `double doubleStep() const`
- `double doubleValue() const`
- `QInputDialog::InputMode inputMode() const`
- `int intMaximum() const`
- `int intMinimum() const`
- `int intStep() const`
- `int intValue() const`
- `bool isComboBoxEditable() const`
- `QString labelText() const`
- `QString okButtonText() const`
- `void open(QObject *receiver, const char *member)`
- `QInputDialog::InputDialogOptions options() const`
- `void setCancelButtonText(const QString &text)`
- `void setComboBoxEditable(bool editable)`
- `void setComboBoxItems(const QStringList &items)`
- `void setDoubleDecimals(int decimals)`
- `void setDoubleMaximum(double max)`
- `void setDoubleMinimum(double min)`
- `void setDoubleRange(double min, double max)`
- `void setDoubleStep(double step)`
- `void setDoubleValue(double value)`
- `void setInputMode(QInputDialog::InputMode mode)`
- `void setIntMaximum(int max)`
- `void setIntMinimum(int min)`
- `void setIntRange(int min, int max)`
- `void setIntStep(int step)`
- `void setIntValue(int value)`
- `void setLabelText(const QString &text)`
- `void setOkButtonText(const QString &text)`
- `void setOption(QInputDialog::InputDialogOption option, bool on = true)`
- `void setOptions(QInputDialog::InputDialogOptions options)`
- `void setTextEchoMode(QLineEdit::EchoMode mode)`
- `void setTextValue(const QString &text)`
- `bool testOption(QInputDialog::InputDialogOption option) const`
- `QLineEdit::EchoMode textEchoMode() const`
- `QString textValue() const`

### 重实现的公有函数

- `virtual void done(int result) override`
- `virtual QSize minimumSizeHint() const override`
- `virtual void setVisible(bool visible) override`
- `virtual QSize sizeHint() const override`

### 信号

- `void doubleValueChanged(double value)`
- `void doubleValueSelected(double value)`
- `void intValueChanged(int value)`
- `void intValueSelected(int value)`
- `void textValueChanged(const QString &text)`
- `void textValueSelected(const QString &text)`

### 静态公有成员

- `double getDouble(QWidget *parent, const QString &title, const QString &label, double value = 0, double min = -2147483647, double max = 2147483647, int decimals = 1, bool *ok = nullptr, Qt::WindowFlags flags = Qt::WindowFlags(), double step = 1)`
- `int getInt(QWidget *parent, const QString &title, const QString &label, int value = 0, int min = -2147483647, int max = 2147483647, int step = 1, bool *ok = nullptr, Qt::WindowFlags flags = Qt::WindowFlags())`
- `QString getItem(QWidget *parent, const QString &title, const QString &label, const QStringList &items, int current = 0, bool editable = true, bool *ok = nullptr, Qt::WindowFlags flags = Qt::WindowFlags(), Qt::InputMethodHints inputMethodHints = Qt::ImhNone)`
- `QString getMultiLineText(QWidget *parent, const QString &title, const QString &label, const QString &text = QString(), bool *ok = nullptr, Qt::WindowFlags flags = Qt::WindowFlags(), Qt::InputMethodHints inputMethodHints = Qt::ImhNone)`
- `QString getText(QWidget *parent, const QString &title, const QString &label, QLineEdit::EchoMode mode = QLineEdit::Normal, const QString &text = QString(), bool *ok = nullptr, Qt::WindowFlags flags = Qt::WindowFlags(), Qt::InputMethodHints inputMethodHints = Qt::ImhNone)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QInputDialog::InputDialogOptionflags QInputDialog::InputDialogOptions`

**作用与语义：**

该枚举指定了影响输入对话框外观和感受的各种选项。
- `QInputDialog::NoButtons`：`0x00000001`;不显示确定和取消按钮（对“实时对话”非常有用）。
- `QInputDialog::UseListViewForComboBoxItems`：`0x00000002`;使用`QListView`而非不可编辑的`QComboBox`来显示与`setComboBoxItems()`相符的项目。
- `QInputDialog::UsePlainTextEditForTextInput`：`0x00000004`;多行文本输入使用`QPlainTextEdit`。该值在5.2版本中引入。
InputDialogOptions 类型是 QFlags 的 typedef<InputDialogOption>。它存储 InputDialogOption 值的 OR 组合。

### `enum QInputDialog::InputMode`

**作用与语义：**

该枚举描述了对话中可以选择的不同输入模式。
- `QInputDialog::TextInput`：`0`;用于输入文本字符串。
- `QInputDialog::IntInput`：`1`;用于输入整数。
- `QInputDialog::DoubleInput`：`2`;用于以双精度输入浮点数。

### `cancelButtonText : QString`

**作用与语义：**

该属性包含取消对话所用按钮的文本。

**如何使用：** 调用 `cancelButtonText()` 读取当前值；它不会修改应用状态。

### `comboBoxEditable : bool`

**作用与语义：**

该属性适用于输入对话框中的组合框是否可编辑。

**如何使用：** 调用 `comboBoxEditable()` 读取当前值；它不会修改应用状态。

### `comboBoxItems : QStringList`

**作用与语义：**

该属性包含输入对话框中使用的物品。

**如何使用：** 调用 `comboBoxItems()` 读取当前值；它不会修改应用状态。

### `doubleDecimals : int`

**作用与语义：**

将双自旋盒的精度设定为小数点。

**如何使用：** 调用 `doubleDecimals()` 读取当前值；它不会修改应用状态。

### `doubleMaximum : double`

**作用与语义：**

该属性表示了被接受为输入的最大双精度浮点值。
该特性仅在输入对话以`DoubleInput`模式使用时相关。

**如何使用：** 调用 `doubleMaximum()` 读取当前值；它不会修改应用状态。

### `doubleMinimum : double`

**作用与语义：**

该属性表示被接受为输入的最小双精度浮点值。
该属性仅在输入对话以`DoubleInput`模式使用时相关。

**如何使用：** 调用 `doubleMinimum()` 读取当前值；它不会修改应用状态。

### `doubleStep : double`

**作用与语义：**

该属性表示了加倍值的增减步骤。
该特性仅在输入对话以`DoubleInput`模式使用时相关。

**如何使用：** 调用 `doubleStep()` 读取当前值；它不会修改应用状态。

### `doubleValue : int`

**作用与语义：**

该属性保留当前接受的双精度浮点值。
该特性仅在输入对话以`DoubleInput`模式使用时相关。

**如何使用：** 调用 `doubleValue()` 读取当前值；它不会修改应用状态。

### `inputMode : InputMode`

**作用与语义：**

该属性表示输入所用的模态。
该属性有助于确定用于输入对话的控件。

**如何使用：** 调用 `inputMode()` 读取当前值；它不会修改应用状态。

### `intMaximum : int`

**作用与语义：**

该属性包含被接受为输入的最大整数值。
该特性仅在输入对话在`IntInput`模式下使用时相关。

**如何使用：** 调用 `intMaximum()` 读取当前值；它不会修改应用状态。

### `intMinimum : int`

**作用与语义：**

该属性包含被接受为输入的最小整数值。
该特性仅在输入对话以`IntInput`模式使用时相关。

**如何使用：** 调用 `intMinimum()` 读取当前值；它不会修改应用状态。

### `intStep : int`

**作用与语义：**

该属性表示整数值的增减步骤。
该特性仅在输入对话以`IntInput`模式使用时相关。

**如何使用：** 调用 `intStep()` 读取当前值；它不会修改应用状态。

### `intValue : int`

**作用与语义：**

该属性表示当前被接受为输入的整数值。
该特性仅在输入对话以`IntInput`模式使用时相关。

**如何使用：** 调用 `intValue()` 读取当前值；它不会修改应用状态。

### `labelText : QString`

**作用与语义：**

此属性保存标签的文本，用于描述需要输入的内容。

**如何使用：** 调用 `labelText()` 读取当前值；它不会修改应用状态。

### `okButtonText : QString`

**作用与语义：**

该属性包含用于接受对话中输入的按钮文本。

**如何使用：** 调用 `okButtonText()` 读取当前值；它不会修改应用状态。

### `options : InputDialogOptions`

**作用与语义：**

该属性包含影响对话视觉和感觉的各种选项。
默认情况下，所有选项都是被禁用的。

**如何使用：** 调用 `options()` 读取当前值；它不会修改应用状态。

### `textEchoMode : QLineEdit::EchoMode`

**作用与语义：**

该属性表示文本值的回声模式。
该特性仅在输入对话框在`TextInput`模式下使用时相关。

**如何使用：** 调用 `textEchoMode()` 读取当前值；它不会修改应用状态。

### `textValue : QString`

**作用与语义：**

该属性包含输入对话框的文本值。
该特性仅在输入对话框以`TextInput`模式使用时相关。

**如何使用：** 调用 `textValue()` 读取当前值；它不会修改应用状态。

### `QInputDialog::QInputDialog(QWidget *parent = nullptr, Qt::WindowFlags flags = Qt::WindowFlags())`

**作用与语义：**

构建一个包含给定`parent`和窗口`flags`的新输入对话。

### `[virtual noexcept] QInputDialog::~QInputDialog()`

**作用与语义：**

会破坏输入对话框。

### `[override virtual] void QInputDialog::done(int result)`

**作用与语义：**

重实现自：`QDialog::done`（int r）。
关闭对话并将其结果代码设置为`result`。如果该对话显示为`exec()`，done() 会导致本地事件循环结束，`exec()`返回`result`。
关闭对话并将结果码设置为`r`。`finished()`信号会发出`r`;如果`r`是`QDialog::Accepted`或`QDialog::Rejected`，则分别会发出`accepted()`或`rejected()`信号。
如果该对话显示为`exec()`，done() 也会使本地事件循环结束，`exec()`返回`r`。
与`QWidget::close()`一样，如果设置了`Qt::WA_DeleteOnClose`标志，done() 会删除对话。如果对话框是应用程序的主控件，应用程序会终止。如果对话框是最后关闭的窗口，则发出`QGuiApplication::lastWindowClosed()`信号。

### `[signal] void QInputDialog::doubleValueChanged(double value)`

**作用与语义：**

该属性保留当前接受的双精度浮点值。
该特性仅在输入对话以`DoubleInput`模式使用时相关。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `doubleValue` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QInputDialog::doubleValueSelected(double value)`

**作用与语义：**

每当用户通过接受对话选择双倍值时，该信号就会发出;例如，点击确定按钮。选中的值由`value`指定。
该信号仅在输入对话以`DoubleInput`模式使用时才相关。

### `[static] double QInputDialog::getDouble(QWidget *parent, const QString &title, const QString &label, double value = 0, double min = -2147483647, double max = 2147483647, int decimals = 1, bool *ok = nullptr, Qt::WindowFlags flags = Qt::WindowFlags(), double step = 1)`

**作用与语义：**

静态便利功能，用于从用户那里获取浮点数。
`title` 是对话框标题栏中显示的文本。`label` 是显示给用户的文本（应说明应输入的内容）。`value` 是行编辑设置的默认浮点数。`min` 和 `max` 分别是用户可选择的最小值和最大值。`decimals` 是该数字可拥有的最大小数位数。`step` 是用户按箭头按钮以增加或减少数值时，值的变化幅度。
如果`ok`非空，用户按 OK 时 *`ok` 设为 true，按下取消则设为 false。对话的父节点是 `parent`。对话框将是模态的，并使用 widget `flags`。
该函数返回用户输入的浮点数。
像这样使用这个静态函数：

**官方示例：**

```cpp
     bool ok{};
     double d = QInputDialog::getDouble(this, tr("QInputDialog::getDouble()"),
                                        tr("Amount:"), 37.56, -10000, 10000, 2, &ok,
                                        Qt::WindowFlags(), 1);
     if (ok)
         doubleLabel->setText(QStringLiteral("$%1").arg(d));
```

### `[static] int QInputDialog::getInt(QWidget *parent, const QString &title, const QString &label, int value = 0, int min = -2147483647, int max = 2147483647, int step = 1, bool *ok = nullptr, Qt::WindowFlags flags = Qt::WindowFlags())`

**作用与语义：**

静态便利函数，用于从用户那里获得整数输入。
`title` 是对话框标题栏中显示的文本。`label` 是显示给用户的文本（应说明应输入的内容）。`value` 是旋转盒将被设置的默认整数。`min` 和 `max` 分别是用户可选择的最小值和最大值。`step` 是用户按键递增或减值时，值的变化幅度。
如果`ok`非空，*`ok` 如果用户按了 OK，则设置为 true，按下 Cancel 则设为 false。该对话框的父节点是`parent`。该对话框将是模态的，并使用 widget `flags`。
成功时，该函数返回用户输入的整数;失败时返回初始的 `value`。
像这样使用这个静态函数：

**官方示例：**

```cpp
     bool ok;
     int i = QInputDialog::getInt(this, tr("QInputDialog::getInt()"),
                                  tr("Percentage:"), 25, 0, 100, 1, &ok);
     if (ok)
         integerLabel->setText(tr("%1%").arg(i));
```

### `[static] QString QInputDialog::getItem(QWidget *parent, const QString &title, const QString &label, const QStringList &items, int current = 0, bool editable = true, bool *ok = nullptr, Qt::WindowFlags flags = Qt::WindowFlags(), Qt::InputMethodHints inputMethodHints = Qt::ImhNone)`

**作用与语义：**

静态便利功能，允许用户从字符串列表中选择项目。
`title` 是对话框标题栏中显示的文本。`label` 是显示给用户的文本（应说明应输入的内容）。`items` 是插入组合框中的字符串列表。`current` 是当前项目的编号。`inputMethodHints` 是组合框可编辑且输入法激活时将使用的输入法提示。
如果`editable`为真，用户可以输入自己的文本;否则，用户只能选择现有项目中的一个。
如果 `ok` 非空，*ok 将设置为 true（如果用户按下 OK）;如果用户按下 Cancel，则设置为 false。对话的父节点是 `parent`。该对话框将是模态的，并使用 widget 的 `flags`。
该函数返回当前项目的文本，或者如果`editable`为真，则返回组合框当前的文本。
像这样使用这个静态函数：

**官方示例：**

```cpp
     const QStringList items{tr("Spring"), tr("Summer"), tr("Fall"), tr("Winter")};

     bool ok{};
     QString item = QInputDialog::getItem(this, tr("QInputDialog::getItem()"),
                                          tr("Season:"), items, 0, false, &ok);
     if (ok && !item.isEmpty())
         itemLabel->setText(item);
```

### `[static] QString QInputDialog::getMultiLineText(QWidget *parent, const QString &title, const QString &label, const QString &text = QString(), bool *ok = nullptr, Qt::WindowFlags flags = Qt::WindowFlags(), Qt::InputMethodHints inputMethodHints = Qt::ImhNone)`

**作用与语义：**

静态便利函数，用于从用户那里获取多行字符串。
`title` 是对话框标题栏中显示的文本。`label` 是显示给用户的文本（应说明应输入内容）。`text` 是默认文本，放置在纯文本编辑中。`inputMethodHints` 是输入法提示，如果某个输入法激活，编辑小部件中将使用。
如果 `ok` 非空，*ok 设置为 true（用户按 OK）;如果用户按 Cancel，*ok 设为 false。对话框的父节点是`parent`。对话框将是模态的，并使用指定的控件`flags`。
如果对话被接受，该函数返回对话的纯文本编辑。如果对话被拒绝，则返回空`QString`。
像这样使用这个静态函数：

**官方示例：**

```cpp
     bool ok{};
     QString text = QInputDialog::getMultiLineText(this, tr("QInputDialog::getMultiLineText()"),
                                                   tr("Address:"), "John Doe\nFreedom Street"_L1, &ok);
     if (ok && !text.isEmpty())
         multiLineTextLabel->setText(text);
```

### `[static] QString QInputDialog::getText(QWidget *parent, const QString &title, const QString &label, QLineEdit::EchoMode mode = QLineEdit::Normal, const QString &text = QString(), bool *ok = nullptr, Qt::WindowFlags flags = Qt::WindowFlags(), Qt::InputMethodHints inputMethodHints = Qt::ImhNone)`

**作用与语义：**

静态便利函数，用于从用户那里获取字符串。
`title` 是对话框标题栏中显示的文本。`label` 是显示给用户的文本（应说明应输入什么）。`text` 是放置在行编辑中的默认文本。`mode` 是行编辑使用的回声模式。`inputMethodHints` 是如果输入方法激活时，编辑小部件中将使用的输入法提示。
如果`ok`非空，*ok 将设置为 true（如果用户按下 OK）;如果用户按下 Cancel，则设置为 false。该对话框的父节点是`parent`。该对话框将是模态的，并使用指定的控件`flags`。
如果对话被接受，该函数返回对话行编辑中的文本。如果对话被拒绝，则返回空 `QString`。
像这样使用这个静态函数：

**官方示例：**

```cpp
     bool ok{};
     QString text = QInputDialog::getText(this, tr("QInputDialog::getText()"),
                                          tr("User name:"), QLineEdit::Normal,
                                          QDir::home().dirName(), &ok);
     if (ok && !text.isEmpty())
         textLabel->setText(text);
```

### `[signal] void QInputDialog::intValueChanged(int value)`

**作用与语义：**

该属性表示当前被接受为输入的整数值。
该特性仅在输入对话以`IntInput`模式使用时相关。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `intValue` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QInputDialog::intValueSelected(int value)`

**作用与语义：**

每当用户通过接受对话选择整数值时，该信号都会发出;例如，点击确定按钮。选中的值由`value`指定。
该信号仅在输入对话以`IntInput`模式使用时相关。

### `[override virtual] QSize QInputDialog::minimumSizeHint() const`

**作用与语义：**

重装：`QDialog::minimumSizeHint()` const.
重新实现属性访问函数：`QWidget::minimumSizeHint`。

### `void QInputDialog::open(QObject *receiver, const char *member)`

**作用与语义：**

该函数将其中一个信号连接到由`receiver`和`member`指定的槽函数。具体信号取决于`member`中指定的参数。这些参数包括：
- `textValueSelected()` `member` 的第一个参数有 `QString`。
- `intValueSelected()` `member` 的第一个参数有 int。
- `doubleValueSelected()` 如果`member`第一个参数有双重变量。
- `accepted()`如果`member`没有任何论点。
当对话关闭时，信号会从槽函数中断开。

### `void QInputDialog::setDoubleRange(double min, double max)`

**作用与语义：**

设置对话在`DoubleInput`模式下接受的双精度浮点值范围，最小值和最大值分别由`min`和`max`指定。

### `void QInputDialog::setIntRange(int min, int max)`

**作用与语义：**

设置对话在`IntInput`模式下可接受的整数值范围，最小值和最大值分别由 `min` 和 `max` 指定。

### `void QInputDialog::setOption(QInputDialog::InputDialogOption option, bool on = true)`

**作用与语义：**

将给定`option`设为启用，`on`为真;否则，清除给定`option`。

### `[override virtual] void QInputDialog::setVisible(bool visible)`

**作用与语义：**

重实现自：`QDialog::setVisible`（bool可见）。
重新实现了属性的访问函数：`QWidget::visible`。

### `[override virtual] QSize QInputDialog::sizeHint() const`

**作用与语义：**

重装：`QDialog::sizeHint()` const.
重新实现了属性的访问函数：`QWidget::sizeHint`。

### `bool QInputDialog::testOption(QInputDialog::InputDialogOption option) const`

**作用与语义：**

如果启用给定`option`，返回 `true`;否则返回 false。

### `[signal] void QInputDialog::textValueChanged(const QString &text)`

**作用与语义：**

该属性包含输入对话框的文本值。
该特性仅在输入对话框以`TextInput`模式使用时相关。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `textValue` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QInputDialog::textValueSelected(const QString &text)`

**作用与语义：**

每当用户通过接受对话选择文本字符串时，都会发出该信号;例如，点击确定按钮。选中的字符串由`text` 指定。
该信号仅在输入对话以`TextInput`模式使用时相关。

### `enum InputDialogOption { NoButtons, UseListViewForComboBoxItems, UsePlainTextEditForTextInput }`

**作用与语义：**

该枚举指定了影响输入对话框外观和感受的各种选项。
- `QInputDialog::NoButtons`：`0x00000001`;不显示确定和取消按钮（对“实时对话”非常有用）。
- `QInputDialog::UseListViewForComboBoxItems`：`0x00000002`;使用`QListView`而非不可编辑的`QComboBox`来显示与`setComboBoxItems()`相符的项目。
- `QInputDialog::UsePlainTextEditForTextInput`：`0x00000004`;多行文本输入使用`QPlainTextEdit`。该值在5.2版本中引入。
InputDialogOptions 类型是 QFlags 的 typedef<InputDialogOption>。它存储 InputDialogOption 值的 OR 组合。

### `flags InputDialogOptions`

**作用与语义：**

该枚举指定了影响输入对话框外观和感受的各种选项。
- `QInputDialog::NoButtons`：`0x00000001`;不显示确定和取消按钮（对“实时对话”非常有用）。
- `QInputDialog::UseListViewForComboBoxItems`：`0x00000002`;使用`QListView`而非不可编辑的`QComboBox`来显示与`setComboBoxItems()`相符的项目。
- `QInputDialog::UsePlainTextEditForTextInput`：`0x00000004`;多行文本输入使用`QPlainTextEdit`。该值在5.2版本中引入。
InputDialogOptions 类型是 QFlags 的 typedef<InputDialogOption>。它存储 InputDialogOption 值的 OR 组合。

### `QString cancelButtonText() const`

**作用与语义：**

该属性包含取消对话所用按钮的文本。

**如何使用：** 调用 `cancelButtonText()` 读取当前值；它不会修改应用状态。

### `QStringList comboBoxItems() const`

**作用与语义：**

该属性包含输入对话框中使用的物品。

**如何使用：** 调用 `comboBoxItems()` 读取当前值；它不会修改应用状态。

### `int doubleDecimals() const`

**作用与语义：**

将双自旋盒的精度设定为小数点。

**如何使用：** 调用 `doubleDecimals()` 读取当前值；它不会修改应用状态。

### `double doubleMaximum() const`

**作用与语义：**

该属性表示了被接受为输入的最大双精度浮点值。
该特性仅在输入对话以`DoubleInput`模式使用时相关。

**如何使用：** 调用 `doubleMaximum()` 读取当前值；它不会修改应用状态。

### `double doubleMinimum() const`

**作用与语义：**

该属性表示被接受为输入的最小双精度浮点值。
该属性仅在输入对话以`DoubleInput`模式使用时相关。

**如何使用：** 调用 `doubleMinimum()` 读取当前值；它不会修改应用状态。

### `double doubleStep() const`

**作用与语义：**

该属性表示了加倍值的增减步骤。
该特性仅在输入对话以`DoubleInput`模式使用时相关。

**如何使用：** 调用 `doubleStep()` 读取当前值；它不会修改应用状态。

### `double doubleValue() const`

**作用与语义：**

该属性保留当前接受的双精度浮点值。
该特性仅在输入对话以`DoubleInput`模式使用时相关。

**如何使用：** 调用 `doubleValue()` 读取当前值；它不会修改应用状态。

### `QInputDialog::InputMode inputMode() const`

**作用与语义：**

该属性表示输入所用的模态。
该属性有助于确定用于输入对话的控件。

**如何使用：** 调用 `inputMode()` 读取当前值；它不会修改应用状态。

### `int intMaximum() const`

**作用与语义：**

该属性包含被接受为输入的最大整数值。
该特性仅在输入对话在`IntInput`模式下使用时相关。

**如何使用：** 调用 `intMaximum()` 读取当前值；它不会修改应用状态。

### `int intMinimum() const`

**作用与语义：**

该属性包含被接受为输入的最小整数值。
该特性仅在输入对话以`IntInput`模式使用时相关。

**如何使用：** 调用 `intMinimum()` 读取当前值；它不会修改应用状态。

### `int intStep() const`

**作用与语义：**

该属性表示整数值的增减步骤。
该特性仅在输入对话以`IntInput`模式使用时相关。

**如何使用：** 调用 `intStep()` 读取当前值；它不会修改应用状态。

### `int intValue() const`

**作用与语义：**

该属性表示当前被接受为输入的整数值。
该特性仅在输入对话以`IntInput`模式使用时相关。

**如何使用：** 调用 `intValue()` 读取当前值；它不会修改应用状态。

### `bool isComboBoxEditable() const`

**作用与语义：**

该属性适用于输入对话框中的组合框是否可编辑。

**如何使用：** 调用 `isComboBoxEditable()` 读取当前值；它不会修改应用状态。

### `QString labelText() const`

**作用与语义：**

此属性保存标签的文本，用于描述需要输入的内容。

**如何使用：** 调用 `labelText()` 读取当前值；它不会修改应用状态。

### `QString okButtonText() const`

**作用与语义：**

该属性包含用于接受对话中输入的按钮文本。

**如何使用：** 调用 `okButtonText()` 读取当前值；它不会修改应用状态。

### `QInputDialog::InputDialogOptions options() const`

**作用与语义：**

该属性包含影响对话视觉和感觉的各种选项。
默认情况下，所有选项都是被禁用的。

**如何使用：** 调用 `options()` 读取当前值；它不会修改应用状态。

### `void setCancelButtonText(const QString &text)`

**作用与语义：**

该属性包含取消对话所用按钮的文本。

**如何使用：** 调用 `setCancelButtonText(...)` 修改 `cancelButtonText`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setComboBoxEditable(bool editable)`

**作用与语义：**

该属性适用于输入对话框中的组合框是否可编辑。

**如何使用：** 调用 `setComboBoxEditable(...)` 修改 `comboBoxEditable`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setComboBoxItems(const QStringList &items)`

**作用与语义：**

该属性包含输入对话框中使用的物品。

**如何使用：** 调用 `setComboBoxItems(...)` 修改 `comboBoxItems`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDoubleDecimals(int decimals)`

**作用与语义：**

将双自旋盒的精度设定为小数点。

**如何使用：** 调用 `setDoubleDecimals(...)` 修改 `doubleDecimals`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDoubleMaximum(double max)`

**作用与语义：**

该属性表示了被接受为输入的最大双精度浮点值。
该特性仅在输入对话以`DoubleInput`模式使用时相关。

**如何使用：** 调用 `setDoubleMaximum(...)` 修改 `doubleMaximum`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDoubleMinimum(double min)`

**作用与语义：**

该属性表示被接受为输入的最小双精度浮点值。
该属性仅在输入对话以`DoubleInput`模式使用时相关。

**如何使用：** 调用 `setDoubleMinimum(...)` 修改 `doubleMinimum`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDoubleStep(double step)`

**作用与语义：**

该属性表示了加倍值的增减步骤。
该特性仅在输入对话以`DoubleInput`模式使用时相关。

**如何使用：** 调用 `setDoubleStep(...)` 修改 `doubleStep`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDoubleValue(double value)`

**作用与语义：**

该属性保留当前接受的双精度浮点值。
该特性仅在输入对话以`DoubleInput`模式使用时相关。

**如何使用：** 调用 `setDoubleValue(...)` 修改 `doubleValue`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setInputMode(QInputDialog::InputMode mode)`

**作用与语义：**

该属性表示输入所用的模态。
该属性有助于确定用于输入对话的控件。

**如何使用：** 调用 `setInputMode(...)` 修改 `inputMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setIntMaximum(int max)`

**作用与语义：**

该属性包含被接受为输入的最大整数值。
该特性仅在输入对话在`IntInput`模式下使用时相关。

**如何使用：** 调用 `setIntMaximum(...)` 修改 `intMaximum`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setIntMinimum(int min)`

**作用与语义：**

该属性包含被接受为输入的最小整数值。
该特性仅在输入对话以`IntInput`模式使用时相关。

**如何使用：** 调用 `setIntMinimum(...)` 修改 `intMinimum`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setIntStep(int step)`

**作用与语义：**

该属性表示整数值的增减步骤。
该特性仅在输入对话以`IntInput`模式使用时相关。

**如何使用：** 调用 `setIntStep(...)` 修改 `intStep`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setIntValue(int value)`

**作用与语义：**

该属性表示当前被接受为输入的整数值。
该特性仅在输入对话以`IntInput`模式使用时相关。

**如何使用：** 调用 `setIntValue(...)` 修改 `intValue`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLabelText(const QString &text)`

**作用与语义：**

此属性保存标签的文本，用于描述需要输入的内容。

**如何使用：** 调用 `setLabelText(...)` 修改 `labelText`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setOkButtonText(const QString &text)`

**作用与语义：**

该属性包含用于接受对话中输入的按钮文本。

**如何使用：** 调用 `setOkButtonText(...)` 修改 `okButtonText`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setOptions(QInputDialog::InputDialogOptions options)`

**作用与语义：**

该属性包含影响对话视觉和感觉的各种选项。
默认情况下，所有选项都是被禁用的。

**如何使用：** 调用 `setOptions(...)` 修改 `options`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTextEchoMode(QLineEdit::EchoMode mode)`

**作用与语义：**

该属性表示文本值的回声模式。
该特性仅在输入对话框在`TextInput`模式下使用时相关。

**如何使用：** 调用 `setTextEchoMode(...)` 修改 `textEchoMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTextValue(const QString &text)`

**作用与语义：**

该属性包含输入对话框的文本值。
该特性仅在输入对话框以`TextInput`模式使用时相关。

**如何使用：** 调用 `setTextValue(...)` 修改 `textValue`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QLineEdit::EchoMode textEchoMode() const`

**作用与语义：**

该属性表示文本值的回声模式。
该特性仅在输入对话框在`TextInput`模式下使用时相关。

**如何使用：** 调用 `textEchoMode()` 读取当前值；它不会修改应用状态。

### `QString textValue() const`

**作用与语义：**

该属性包含输入对话框的文本值。
该特性仅在输入对话框以`TextInput`模式使用时相关。

**如何使用：** 调用 `textValue()` 读取当前值；它不会修改应用状态。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QInputDialog` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
