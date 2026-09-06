# QComboBox

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QComboBox` 把一组候选项压缩成一个下拉选择控件，既可以直接管理项目，也可以连接模型/视图数据。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QComboBox` 把一组候选项压缩成一个下拉选择控件，既可以直接管理项目，也可以连接模型/视图数据。

**内部模型：** 当前索引 currentIndex、当前文本 currentText 和用户选择信号是三个不同概念；可编辑组合框还增加了编辑器和验证问题。

**适用场景：** 模式、类型、排序方式等有限选项使用；选项很多、需要搜索或多选时应考虑 QListView/QCompleter 等方案。

**典型调用链：** 添加项目或设置 model -> 设置 currentIndex -> 连接 currentIndexChanged/activated -> 根据 itemData 取得稳定业务值。

**先记住的坑：** 不要用显示文本作为唯一业务 ID；区分程序设置 currentIndex 和用户 activated；批量填充时可暂时 blockSignals。

## 2. 依赖与对象关系

- 头文件：`#include <QComboBox>`
- 继承自：QWidget
- 直接派生类：QFontComboBox

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

当前索引 currentIndex、当前文本 currentText 和用户选择信号是三个不同概念；可编辑组合框还增加了编辑器和验证问题。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

模式、类型、排序方式等有限选项使用；选项很多、需要搜索或多选时应考虑 QListView/QCompleter 等方案。 使用时通常按这个过程组织：添加项目或设置 model -> 设置 currentIndex -> 连接 currentIndexChanged/activated -> 根据 itemData 取得稳定业务值。

```cpp
auto *combo = new QComboBox(parent);
combo->addItem(QStringLiteral("Low"), 1);
combo->addItem(QStringLiteral("High"), 2);
connect(combo, &QComboBox::currentIndexChanged, this, [combo](int index) {
    const QVariant id = combo->itemData(index);
});
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum InsertPolicy { NoInsert, InsertAtTop, InsertAtCurrent, InsertAtBottom, InsertAfterCurrent, …, InsertAlphabetically }`
- `(since 6.9) enum class LabelDrawingMode { UseStyle, UseDelegate }`
- `enum SizeAdjustPolicy { AdjustToContents, AdjustToContentsOnFirstShow, AdjustToMinimumContentsLengthWithIcon }`

### 属性

- `count : int`
- `currentData : QVariant`
- `currentIndex : int`
- `currentText : QString`
- `duplicatesEnabled : bool`
- `editable : bool`
- `frame : bool`
- `iconSize : QSize`
- `insertPolicy : InsertPolicy`
- `(since 6.9) labelDrawingMode : LabelDrawingMode`
- `maxCount : int`
- `maxVisibleItems : int`
- `minimumContentsLength : int`
- `modelColumn : int`
- `placeholderText : QString`
- `sizeAdjustPolicy : SizeAdjustPolicy`

### 公有函数

- `QComboBox(QWidget *parent = nullptr)`
- `virtual ~QComboBox()`
- `void addItem(const QString &text, const QVariant &userData = QVariant())`
- `void addItem(const QIcon &icon, const QString &text, const QVariant &userData = QVariant())`
- `void addItems(const QStringList &texts)`
- `QCompleter * completer() const`
- `int count() const`
- `QVariant currentData(int role = Qt::UserRole) const`
- `int currentIndex() const`
- `QString currentText() const`
- `bool duplicatesEnabled() const`
- `int findData(const QVariant &data, int role = Qt::UserRole, Qt::MatchFlags flags = static_cast<Qt::MatchFlags>(Qt::MatchExactly|Qt::MatchCaseSensitive)) const`
- `int findText(const QString &text, Qt::MatchFlags flags = Qt::MatchExactly|Qt::MatchCaseSensitive) const`
- `bool hasFrame() const`
- `virtual void hidePopup()`
- `QSize iconSize() const`
- `void insertItem(int index, const QString &text, const QVariant &userData = QVariant())`
- `void insertItem(int index, const QIcon &icon, const QString &text, const QVariant &userData = QVariant())`
- `void insertItems(int index, const QStringList &list)`
- `QComboBox::InsertPolicy insertPolicy() const`
- `void insertSeparator(int index)`
- `bool isEditable() const`
- `QVariant itemData(int index, int role = Qt::UserRole) const`
- `QAbstractItemDelegate * itemDelegate() const`
- `QIcon itemIcon(int index) const`
- `QString itemText(int index) const`
- `QComboBox::LabelDrawingMode labelDrawingMode() const`
- `QLineEdit * lineEdit() const`
- `int maxCount() const`
- `int maxVisibleItems() const`
- `int minimumContentsLength() const`
- `QAbstractItemModel * model() const`
- `int modelColumn() const`
- `QString placeholderText() const`
- `void removeItem(int index)`
- `QModelIndex rootModelIndex() const`
- `void setCompleter(QCompleter *completer)`
- `void setDuplicatesEnabled(bool enable)`
- `void setEditable(bool editable)`
- `void setFrame(bool)`
- `void setIconSize(const QSize &size)`
- `void setInsertPolicy(QComboBox::InsertPolicy policy)`
- `void setItemData(int index, const QVariant &value, int role = Qt::UserRole)`
- `void setItemDelegate(QAbstractItemDelegate *delegate)`
- `void setItemIcon(int index, const QIcon &icon)`
- `void setItemText(int index, const QString &text)`
- `void setLabelDrawingMode(QComboBox::LabelDrawingMode labelDrawing)`
- `void setLineEdit(QLineEdit *edit)`
- `void setMaxCount(int max)`
- `void setMaxVisibleItems(int maxItems)`
- `void setMinimumContentsLength(int characters)`
- `virtual void setModel(QAbstractItemModel *model)`
- `void setModelColumn(int visibleColumn)`
- `void setPlaceholderText(const QString &placeholderText)`
- `void setRootModelIndex(const QModelIndex &index)`
- `void setSizeAdjustPolicy(QComboBox::SizeAdjustPolicy policy)`
- `void setValidator(const QValidator *validator)`
- `void setView(QAbstractItemView *itemView)`
- `virtual void showPopup()`
- `QComboBox::SizeAdjustPolicy sizeAdjustPolicy() const`
- `const QValidator * validator() const`
- `QAbstractItemView * view() const`

### 重实现的公有函数

- `virtual bool event(QEvent *event) override`
- `virtual QVariant inputMethodQuery(Qt::InputMethodQuery query) const override`
- `virtual QSize minimumSizeHint() const override`
- `virtual QSize sizeHint() const override`

### 公有槽函数

- `void clear()`
- `void clearEditText()`
- `void setCurrentIndex(int index)`
- `void setCurrentText(const QString &text)`
- `void setEditText(const QString &text)`

### 信号

- `void activated(int index)`
- `void currentIndexChanged(int index)`
- `void currentTextChanged(const QString &text)`
- `void editTextChanged(const QString &text)`
- `void highlighted(int index)`
- `void textActivated(const QString &text)`
- `void textHighlighted(const QString &text)`

### 保护函数

- `virtual void initStyleOption(QStyleOptionComboBox *option) const`

### 重实现的保护函数

- `virtual void changeEvent(QEvent *e) override`
- `virtual void contextMenuEvent(QContextMenuEvent *e) override`
- `virtual void focusInEvent(QFocusEvent *e) override`
- `virtual void focusOutEvent(QFocusEvent *e) override`
- `virtual void hideEvent(QHideEvent *e) override`
- `virtual void inputMethodEvent(QInputMethodEvent *e) override`
- `virtual void keyPressEvent(QKeyEvent *e) override`
- `virtual void keyReleaseEvent(QKeyEvent *e) override`
- `virtual void mousePressEvent(QMouseEvent *e) override`
- `virtual void mouseReleaseEvent(QMouseEvent *e) override`
- `virtual void paintEvent(QPaintEvent *e) override`
- `virtual void resizeEvent(QResizeEvent *e) override`
- `virtual void showEvent(QShowEvent *e) override`
- `virtual void wheelEvent(QWheelEvent *e) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QComboBox::InsertPolicy`

**作用与语义：**

该枚举规定了用户输入新字符串时`QComboBox`应采取的操作。
- `QComboBox::NoInsert`：`0`;该弦不会插入组合盒。
- `QComboBox::InsertAtTop`：`1`;该字符串将作为组合盒的第一个物品插入。
- `QComboBox::InsertAtCurrent`：`2`;当前项将被字符串替换。
- `QComboBox::InsertAtBottom`：`3`;该字符串会在组合盒的最后一个物品之后插入。
- `QComboBox::InsertAfterCurrent`：`4`;字符串插入在组合盒当前物品之后。
- `QComboBox::InsertBeforeCurrent`：`5`;字符串插入在组合盒当前物品之前。
- `QComboBox::InsertAlphabetically`：`6`;字符串按字母顺序插入组合盒中。

### `[since 6.9] enum class QComboBox::LabelDrawingMode`

**作用与语义：**

这个枚举指定了组合盒如何绘制其标签。
- `QComboBox::LabelDrawingMode::UseStyle`：`0`;组合盒利用`style`绘制标签。
- `QComboBox::LabelDrawingMode::UseDelegate`：`1`;组合盒使用物品代理绘制标签。使用此模式时设置合适的物品代理。
这个枚举是在Qt 6.9引入的。

### `enum QComboBox::SizeAdjustPolicy`

**作用与语义：**

该枚举规定了当新增内容或内容变更时，`QComboBox`的提示大小应如何调整。
- `QComboBox::AdjustToContents`：`0`;组合盒始终会根据内容进行调整
- `QComboBox::AdjustToContentsOnFirstShow`：`1`;组合盒将在首次显示时调整为其内容。
- `QComboBox::AdjustToMinimumContentsLengthWithIcon`：`2`;组合盒将调整到图标的额外空间`minimumContentsLength`。出于性能考虑，大型模型使用此策略。

### `[read-only] count : int`

**作用与语义：**

此属性保存组合框中的项目数量。
默认情况下，对于空组合框，该属性的值为 0。

**如何使用：** 调用 `count()` 读取当前值；它不会修改应用状态。

### `[read-only] currentData : QVariant`

**作用与语义：**

该属性包含当前项目的数据。
默认情况下，对于空的组合盒或当前没有设置物品的组合盒，该属性包含无效的 `QVariant`。

**如何使用：** 调用 `currentData()` 读取当前值；它不会修改应用状态。

### `currentIndex : int`

**作用与语义：**

该属性包含组合框中当前项目的索引。
当前索引在插入或移除物品时可能会变化。
默认情况下，对于空的连击盒或当前未设置任何物品的连击盒，该属性的值为-1。

**如何使用：** 调用 `currentIndex()` 读取当前值；它不会修改应用状态。

### `currentText : QString`

**作用与语义：**

该属性包含当前文本。
如果组合框可编辑，当前文本即为行编辑显示的值。否则，当前文本为当前物品值，或当组合框为空或当前未设置时为空字符串。
如果组合框可编辑，setter则调用`setEditText()`。否则，如果列表中有匹配文本，`currentIndex`会被设置为对应的索引。

**如何使用：** 调用 `currentText()` 读取当前值；它不会修改应用状态。

### `duplicatesEnabled : bool`

**作用与语义：**

该属性决定用户是否可以将重复物品输入组合框。
请注意，总可以程序化地将重复物品插入组合盒中。
默认情况下，该属性是`false`的（不允许重复）。

**如何使用：** 调用 `duplicatesEnabled()` 读取当前值；它不会修改应用状态。

### `editable : bool`

**作用与语义：**

该属性决定用户是否可以编辑组合框。
默认情况下，该属性为`false`。编辑效果取决于插入策略。
注意：禁用`editable`状态时，验证者和补全器会被移除。

**如何使用：** 调用 `editable()` 读取当前值；它不会修改应用状态。

### `frame : bool`

**作用与语义：**

该属性决定组合盒是否用框架绘制。
如果启用（默认），连击盒会在一个框架内绘制自己，否则组合框会在没有任何帧的情况下绘制自己。

**如何使用：** 调用 `frame()` 读取当前值；它不会修改应用状态。

### `iconSize : QSize`

**作用与语义：**

该属性表示组合框中图标的大小。
除非明确设置，否则返回当前样式的默认值。该大小是图标的最大尺寸;较小的图标不会被放大。

**如何使用：** 调用 `iconSize()` 读取当前值；它不会修改应用状态。

### `insertPolicy : InsertPolicy`

**作用与语义：**

此属性保存用于确定用户插入项在组合框中应显示位置的策略。
默认值是 `InsertAtBottom`，表示新项将出现在项目列表的底部。

**如何使用：** 调用 `insertPolicy()` 读取当前值；它不会修改应用状态。

### `[since 6.9] labelDrawingMode : LabelDrawingMode`

**作用与语义：**

该属性代表组合盒绘制标签的模式。
默认值为`UseStyle`。在将该属性改为`UseDelegate`时，确保也设置合适的项目代理。默认代理取决于样式，可能不适合绘制标签。

**如何使用：** 调用 `labelDrawingMode()` 读取当前值；它不会修改应用状态。

### `maxCount : int`

**作用与语义：**

该属性包含组合箱中允许的最大物品数量。
注意：如果你把组合盒中最大物品数量设置为小于当前数量，额外的物品会被截断。如果你在组合盒上设置了外部模型，这同样适用。
默认情况下，该属性的值是从可用的最大有符号整数（通常是2147483647）推导出来的。

**如何使用：** 调用 `maxCount()` 读取当前值；它不会修改应用状态。

### `maxVisibleItems : int`

**作用与语义：**

该属性能显示组合盒屏幕上的最大允许尺寸，单位为物品。
默认情况下，该属性的值为10。
注意：对于某些样式（如Mac样式或Gtk样式）`QStyle::SH_ComboBox_Popup`中，不可编辑组合框（如Mac样式或Gtk样式）则忽略此特性。

**如何使用：** 调用 `maxVisibleItems()` 读取当前值；它不会修改应用状态。

### `minimumContentsLength : int`

**作用与语义：**

该属性包含组合框中应容纳的最少字符数。
默认值是0。
如果该属性被设定为正值，`minimumSizeHint()`和`sizeHint()`会考虑它。

**如何使用：** 调用 `minimumContentsLength()` 读取当前值；它不会修改应用状态。

### `modelColumn : int`

**作用与语义：**

该属性保存模型中可见的列。
如果在填充组合框之前设置，弹出视图将不受影响，并将显示第一列（使用此属性的默认值）。
默认情况下，此属性的值为0。
注意：在可编辑的组合框中，可见列也将成为补全列。

**如何使用：** 调用 `modelColumn()` 读取当前值；它不会修改应用状态。

### `placeholderText : QString`

**作用与语义：**

设置一个`placeholderText`文本，当没有有效索引时显示。
当设置了无效索引时，`placeholderText`会显示出来。该文本在下拉列表中无法访问。当在添加项目前调用该函数时，会显示占位符文本，否则你必须程序调用 `setCurrentIndex`（-1）才能显示占位符文本。设置一个空的占位符文本以重置设置。
当`QComboBox`可编辑时，使用该`QLineEdit::setPlaceholderText()`。

**如何使用：** 调用 `placeholderText()` 读取当前值；它不会修改应用状态。

### `sizeAdjustPolicy : SizeAdjustPolicy`

**作用与语义：**

此属性保存描述当内容更改时组合框大小变化的策略。
默认值是 `AdjustToContentsOnFirstShow`。

**如何使用：** 调用 `sizeAdjustPolicy()` 读取当前值；它不会修改应用状态。

### `[explicit] QComboBox::QComboBox(QWidget *parent = nullptr)`

**作用与语义：**

使用默认模型`QStandardItemModel`，构建与给定`parent`的组合盒。

### `[virtual noexcept] QComboBox::~QComboBox()`

**作用与语义：**

会破坏连击盒。

### `[signal] void QComboBox::activated(int index)`

**作用与语义：**

当用户在组合盒中选择物品时，该信号会被发送。物品的 `index` 会被传递。请注意，即使选择未被更改，这个信号也会被发送。如果你需要知道选择实际变化的时间，可以使用信号 `currentIndexChanged()` 或 `currentTextChanged()`。

### `void QComboBox::addItem(const QString &text, const QVariant &userData = QVariant())`

**作用与语义：**

将一个物品添加到组合盒中，包含指定`text`且包含指定`userData`（存储在`Qt::UserRole`中）。该物品会附加到现有物品列表中。

### `void QComboBox::addItem(const QIcon &icon, const QString &text, const QVariant &userData = QVariant())`

**作用与语义：**

将一个物品添加到组合盒中，包含指定`icon`和`text`，并包含指定`userData`（存储在`Qt::UserRole`中）。该物品会附加到现有物品列表中。

### `void QComboBox::addItems(const QStringList &texts)`

**作用与语义：**

将给定`texts`中的每个字符串加入组合盒。每个物品依次附加到现有物品列表中。

### `[override virtual protected] void QComboBox::changeEvent(QEvent *e)`

**作用与语义：**

重装：`QWidget::changeEvent`（QEvent *事件）。
该事件处理程序可以重新实现以处理状态变化。
该事件中被更改的状态可以通过提供的`event`检索。
变更事件包括：`QEvent::ToolBarChange`、`QEvent::ActivationChange`、`QEvent::EnabledChange`、`QEvent::FontChange`、`QEvent::StyleChange`、`QEvent::PaletteChange`、`QEvent::WindowTitleChange`、`QEvent::IconTextChange`、`QEvent::ModifiedChange`、`QEvent::MouseTrackingChange`、`QEvent::ParentChange`、`QEvent::WindowStateChange`、`QEvent::LanguageChange`、`QEvent::LocaleChange`、`QEvent::LayoutDirectionChange`、`QEvent::ReadOnlyChange`。

### `[slot] void QComboBox::clear()`

**作用与语义：**

清除组合框，移除所有条目。
注意：如果您在组合框上设置了外部模型，调用此函数时该模型仍将被清除。

### `[slot] void QComboBox::clearEditText()`

**作用与语义：**

清除用于组合框编辑的行编辑内容。

### `QCompleter *QComboBox::completer() const`

**作用与语义：**

返回用于自动补全组合盒文本输入的补全器。

### `[override virtual protected] void QComboBox::contextMenuEvent(QContextMenuEvent *e)`

**作用与语义：**

重实现自：`QWidget::contextMenuEvent`（QContextMenuEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收控件上下文菜单事件。
当控件的 `contextMenuPolicy` `Qt::DefaultContextMenu`时调用处理器。
默认实现忽略上下文事件。详情请参见`QContextMenuEvent`文档。

### `[signal] void QComboBox::currentIndexChanged(int index)`

**作用与语义：**

该属性包含组合框中当前项目的索引。
当前索引在插入或移除物品时可能会变化。
默认情况下，对于空的连击盒或当前未设置任何物品的连击盒，该属性的值为-1。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `currentIndex` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QComboBox::currentTextChanged(const QString &text)`

**作用与语义：**

该属性包含当前文本。
如果组合框可编辑，当前文本即为行编辑显示的值。否则，当前文本为当前物品值，或当组合框为空或当前未设置时为空字符串。
如果组合框可编辑，setter则调用`setEditText()`。否则，如果列表中有匹配文本，`currentIndex`会被设置为对应的索引。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `currentText` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QComboBox::editTextChanged(const QString &text)`

**作用与语义：**

当组合盒的行编辑小部件中的文本被更改时，会发出该信号。新文本由`text`指定。

### `[override virtual] bool QComboBox::event(QEvent *event)`

**作用与语义：**

重实现自：`QWidget::event`（QEvent *事件）。

### `int QComboBox::findData(const QVariant &data, int role = Qt::UserRole, Qt::MatchFlags flags = static_cast<Qt::MatchFlags>(Qt::MatchExactly|Qt::MatchCaseSensitive)) const`

**作用与语义：**

返回包含给定`role` `data`项的索引;否则返回 -1。
`flags`会指定组合框中物品的搜索方式。

### `int QComboBox::findText(const QString &text, Qt::MatchFlags flags = Qt::MatchExactly|Qt::MatchCaseSensitive) const`

**作用与语义：**

返回包含给定`text`项的索引;否则返回 -1。
`flags`会指定组合框中的物品如何被搜索。

### `[override virtual protected] void QComboBox::focusInEvent(QFocusEvent *e)`

**作用与语义：**

重实现自：`QWidget::focusInEvent`（QFocusEvent *event）。
该事件处理程序可以在子类中重新实现，以接收控件的键盘焦点事件（焦点接收）。事件通过`event`参数传递。
小部件通常必须`setFocusPolicy()`到非`Qt::NoFocus`的对象才能接收焦点事件。（注意，应用程序员可以调用任何小部件`setFocus()`，即使是那些通常不接受焦点的小部件。）。
默认实现会更新小部件（除非是没有指定`focusPolicy()`的窗口）。

### `[override virtual protected] void QComboBox::focusOutEvent(QFocusEvent *e)`

**作用与语义：**

重现：`QWidget::focusOutEvent`（QFocusEvent *event）。
该事件处理程序可以在子类中重新实现，以接收控件的键盘焦点事件（焦点丢失）。事件通过`event`参数传递。
小部件通常必须`setFocusPolicy()`到非`Qt::NoFocus`的对象才能接收焦点事件。（注意，应用程序员可以调用任何小部件`setFocus()`，即使是那些通常不接受焦点的小部件。）。
默认实现会更新小部件（除非是没有指定`focusPolicy()`的窗口）。

### `[override virtual protected] void QComboBox::hideEvent(QHideEvent *e)`

**作用与语义：**

重实现自：`QWidget::hideEvent`（QHideEvent *event）。
该事件处理程序可以在子类中重新实现，以接收控件隐藏事件。事件通过`event`参数传递。
隐藏事件会在小部件被隐藏后立即发送。
注意：当窗口系统改变其映射状态时，小部件会接收自发显示和隐藏事件，例如用户最小化窗口时自发隐藏事件，恢复窗口时自发显示事件。收到自发隐藏事件后，小部件仍被视为可见，意义`isVisible()`。

### `[virtual] void QComboBox::hidePopup()`

**作用与语义：**

如果组合框当前可见，它会隐藏该列表并重置内部状态，这样如果自定义弹窗显示在重新实现的 `showPopup()` 里，那么你还需要重新实现 hidePopup() 函数来隐藏你的自定义弹窗，并在自定义弹出窗口被隐藏时调用基类实现重置内部状态。

### `[signal] void QComboBox::highlighted(int index)`

**作用与语义：**

当用户高亮组合框弹出列表中的某个物品时，会发送该信号。该物品的`index`会被传递。

### `[virtual protected] void QComboBox::initStyleOption(QStyleOptionComboBox *option) const`

**作用与语义：**

用这个`QComboBox`的值初始化`option`。这种方法适用于需要`QStyleOptionComboBox`但不想自己填满所有信息的子类。

### `[override virtual protected] void QComboBox::inputMethodEvent(QInputMethodEvent *e)`

**作用与语义：**

重实现自：`QWidget::inputMethodEvent`（QInputMethodEvent *event）。
对于事件`event`，该事件处理程序可以被重新实现到子类中以接收输入法组合事件。当输入方法的状态发生变化时，调用该处理程序。
注意，在创建自定义文本编辑小部件时，必须明确设置`Qt::WA_InputMethodEnabled`窗口属性（使用`setAttribute()`函数），才能接收输入法事件。
默认实现调用 event->ignore()，拒绝输入法事件。详情请参见 `QInputMethodEvent` 文档。

### `[override virtual] QVariant QComboBox::inputMethodQuery(Qt::InputMethodQuery query) const`

**作用与语义：**

重实现自：`QWidget::inputMethodQuery`（Qt：：InputMethodQuery query） const.
该方法仅适用于输入控件。输入方法用于查询控件的一组属性，以支持复杂的输入法操作，以支持周围文本和重新转换。
`query` 指定查询的属性。

### `void QComboBox::insertItem(int index, const QString &text, const QVariant &userData = QVariant())`

**作用与语义：**

在指定`index`将`text`和`userData`（存储在`Qt::UserRole`）插入组合盒。
如果索引等于或大于总项目数，则新项目会附加到现有项目列表中。如果索引为零或负数，则新项目会在现有项目列表前加。

### `void QComboBox::insertItem(int index, const QIcon &icon, const QString &text, const QVariant &userData = QVariant())`

**作用与语义：**

在指定`index`将`icon`、`text`和`userData`（存储在`Qt::UserRole`中）插入组合盒。
如果索引等于或大于总项目数，则新项目会附加到现有项目列表中。如果索引为零或负数，则新项目会在现有项目列表前加。

### `void QComboBox::insertItems(int index, const QStringList &list)`

**作用与语义：**

将`list`中的弦作为独立物品插入组合盒，从指定的`index`开始。
如果索引等于或大于总项数，则新项目会附加到现有项目列表中。如果索引为零或负数，则新项目会加在现有项目列表之前。

### `void QComboBox::insertSeparator(int index)`

**作用与语义：**

在指定`index`插入一个分隔物品进入组合盒。
如果索引等于或大于总项目数，则新项目会附加到现有项目列表中。如果索引为零或负数，则新项目会在现有项目列表前加。

### `QVariant QComboBox::itemData(int index, int role = Qt::UserRole) const`

**作用与语义：**

返回组合盒中给定`index`中给定`role`的数据，若无该角色数据则返回无效`QVariant`。

### `QAbstractItemDelegate *QComboBox::itemDelegate() const`

**作用与语义：**

返回弹出列表视图中使用的项目代理。

### `QIcon QComboBox::itemIcon(int index) const`

**作用与语义：**

在组合框中返回该`index`的图标。

### `QString QComboBox::itemText(int index) const`

**作用与语义：**

返回组合框中给定`index`的文本。

### `[override virtual protected] void QComboBox::keyPressEvent(QKeyEvent *e)`

**作用与语义：**

重实现自：`QWidget::keyPressEvent`（QKeyEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该控件的按键事件。
一个小部件必须调用`setFocusPolicy()`先接受焦点，并且必须有焦点才能接收按键事件。
如果你重新实现这个处理器，如果你不对密钥进行操作，务必调用基类实现。
默认实现会关闭弹出小部件，如果用户按下`QKeySequence::Cancel`的按键序列（通常是 Escape 键）。否则事件会被忽略，以便小部件的父节点能够解释。
注意`QKeyEvent`以 isAccepted() == true 开头，所以你不需要调用 `QKeyEvent::accept()`——只要你对该键执行时不要调用基类实现即可。

### `[override virtual protected] void QComboBox::keyReleaseEvent(QKeyEvent *e)`

**作用与语义：**

重实现自：`QWidget::keyReleaseEvent`（QKeyEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该小部件的密钥释放事件。
小部件必须先接受焦点并拥有焦点，才能接收密钥释放事件。
如果你重新实现这个处理器，如果你不对密钥进行操作，务必调用基类实现。
默认实现忽略事件，以便小部件的父节点能够解释事件。
注意`QKeyEvent`以 isAccepted() == true开头，所以你不需要调用`QKeyEvent::accept()`——只要你对密钥操作时不要调用基类实现即可。

### `QLineEdit *QComboBox::lineEdit() const`

**作用与语义：**

返回用于编辑组合框中物品的行编辑，或者如果没有行编辑则返回`nullptr`。
只有可编辑的组合盒才有行编辑功能。

### `[override virtual] QSize QComboBox::minimumSizeHint() const`

**作用与语义：**

重新实现属性的访问函数：`QWidget::minimumSizeHint`。

### `QAbstractItemModel *QComboBox::model() const`

**作用与语义：**

返回组合盒使用的型号。

### `[override virtual protected] void QComboBox::mousePressEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QWidget::mousePressEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标按键事件。
如果你在 mousePressEvent() 创建新控件，`mouseReleaseEvent()`可能不会出现在你预期的位置，这取决于底层窗口系统（或 X11 窗口管理器）、控件的位置，甚至可能还有其他因素。
默认实现实现了当你点击窗口外时关闭弹出小部件的功能。对于其他小部件类型，它没有任何作用。

### `[override virtual protected] void QComboBox::mouseReleaseEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QWidget::mouseReleaseEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标释放事件。

### `[override virtual protected] void QComboBox::paintEvent(QPaintEvent *e)`

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

### `void QComboBox::removeItem(int index)`

**作用与语义：**

从组合框中移除给定`index`的物品。如果索引被移除，当前索引会更新。
如果超出`index`范围，这个功能就不会做任何事。

### `[override virtual protected] void QComboBox::resizeEvent(QResizeEvent *e)`

**作用与语义：**

重实现自：`QWidget::resizeEvent`（QResizeEvent *event）。
该事件处理程序可以在子类中重新实现，以接收通过 `event` 参数传递的控件调整大小事件。当调用 resizeEvent() 时，控件已经拥有新的几何体。旧的大小可以通过 `QResizeEvent::oldSize()` 访问。
控件会被擦除，并在处理调整尺寸事件后立即接收绘图事件。不需要（也不应该）在这个处理程序中进行绘图。

### `QModelIndex QComboBox::rootModelIndex() const`

**作用与语义：**

返回组合盒中物品的根模型物品索引。

### `void QComboBox::setCompleter(QCompleter *completer)`

**作用与语义：**

将`completer`设置为替代当前补全器。如果`completer` `nullptr`，自动补全将被禁用。
默认情况下，对于可编辑组合框，会自动创建一个执行大小写不区分内联补全的 `QCompleter`。
注意：当`editable`属性变`false`，或将行编辑替换为调用`setLineEdit()`时，补全器将被移除。在不可编辑的`QComboBox`上设置补全器将被忽略。

### `[slot] void QComboBox::setEditText(const QString &text)`

**作用与语义：**

在组合框的文本编辑中设置 `text`。

### `void QComboBox::setItemData(int index, const QVariant &value, int role = Qt::UserRole)`

**作用与语义：**

将组合盒中给定`index`物品的数据`role`设置为指定的 `value`。

### `void QComboBox::setItemDelegate(QAbstractItemDelegate *delegate)`

**作用与语义：**

为弹出列表视图设置项目`delegate`。组合盒会拥有代理。
任何现有代表都会被移除，但不会被删除。`QComboBox`不承担`delegate`的所有权。
警告：你不应在组合框、控件映射器或视图之间共享同一个代理实例。这样做可能导致错误或不直观的编辑行为，因为连接到某代理的每个视图都可能收到`closeEditor()`信号，并试图访问、修改或关闭已关闭的编辑器。

### `void QComboBox::setItemIcon(int index, const QIcon &icon)`

**作用与语义：**

在组合盒中设定该物品的`icon`，`index`上。

### `void QComboBox::setItemText(int index, const QString &text)`

**作用与语义：**

在组合盒中设定该物品的`text` `index`。

### `void QComboBox::setLineEdit(QLineEdit *edit)`

**作用与语义：**

设置行`edit`用来代替当前的行编辑控件。
组合盒拥有对行编辑的所有权。
注意：由于组合盒的行编辑拥有`QCompleter`，之前对`setCompleter()`的任何调用将不再生效。

### `[virtual] void QComboBox::setModel(QAbstractItemModel *model)`

**作用与语义：**

将模型设置为`model`。`model`不能被`nullptr`。如果你想清除模型的内容，请调用`clear()`。
注意：如果组合框可编辑，那么`model`也会被设置为该行编辑的完整版本。

### `void QComboBox::setRootModelIndex(const QModelIndex &index)`

**作用与语义：**

为组合盒中的物品设置根模型的物品`index`。

### `void QComboBox::setValidator(const QValidator *validator)`

**作用与语义：**

将`validator`设置为替代当前验证器。
注意：当`editable`属性变`false`时，验证者将被移除。

### `void QComboBox::setView(QAbstractItemView *itemView)`

**作用与语义：**

将组合框弹窗中的视图设置为给定的 `itemView`。组合盒拥有视图的所有权。
注意：如果你想使用便利视图（如`QListWidget`、`QTableWidget`或`QTreeWidget`），请务必在组合框中调用便利小部件模型中的`setModel()`，再调用该函数。

### `[override virtual protected] void QComboBox::showEvent(QShowEvent *e)`

**作用与语义：**

重实现自：`QWidget::showEvent`（QShowEvent *event）。
该事件处理程序可以在子类中重新实现，以接收传递给 `event` 参数的控件显示事件。
非自发的展示事件会在展示前立即发送到小部件。窗口的自发展示事件则在展示之后交付。
注意：当窗口系统改变其映射状态时，小部件会接收自发显示和隐藏事件，例如用户最小化窗口时自发隐藏事件，窗口恢复时自发显示事件。收到自发隐藏事件后，小部件仍被视为`isVisible()`可见。

### `[virtual] void QComboBox::showPopup()`

**作用与语义：**

显示组合框中的物品列表。如果列表为空，则不会显示任何物品。
如果你重新实现这个函数来显示自定义弹窗，务必调用`hidePopup()`来重置内部状态。

### `[override virtual] QSize QComboBox::sizeHint() const`

**作用与语义：**

重新实现了属性的访问函数：`QWidget::sizeHint`。
该实现缓存大小提示，以避免内容动态变化时的大小调整。要使缓存值失效，请更改`sizeAdjustPolicy`。

### `[signal] void QComboBox::textActivated(const QString &text)`

**作用与语义：**

当用户在组合盒中选择物品时，该信号会被发送。物品的`text`会被传递。请注意，即使选择未被更改，这个信号也会被发送。如果你需要知道选择实际发生变化的时间，可以使用信号`currentIndexChanged()`或`currentTextChanged()`。

### `[signal] void QComboBox::textHighlighted(const QString &text)`

**作用与语义：**

当用户高亮组合框弹出列表中的某个物品时，会发送该信号。该物品的 `text` 会被传递。

### `const QValidator *QComboBox::validator() const`

**作用与语义：**

返回用于限制组合盒文本输入的验证器。

### `QAbstractItemView *QComboBox::view() const`

**作用与语义：**

返回用于组合盒弹窗的列表视图。

### `[override virtual protected] void QComboBox::wheelEvent(QWheelEvent *e)`

**作用与语义：**

重实现自：`QWidget::wheelEvent`（QWheelEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该控件的轮事件。
如果你重新实现了这个处理程序，非常重要的是，如果你不处理事件，必须`ignore()`事件，这样小部件的父节点才能解释它。
默认实现会忽略该事件。

### `int count() const`

**作用与语义：**

此属性保存组合框中的项目数量。
默认情况下，对于空组合框，该属性的值为 0。

**如何使用：** 调用 `count()` 读取当前值；它不会修改应用状态。

### `QVariant currentData(int role = Qt::UserRole) const`

**作用与语义：**

该属性包含当前项目的数据。
默认情况下，对于空的组合盒或当前没有设置物品的组合盒，该属性包含无效的 `QVariant`。

**如何使用：** 调用 `currentData()` 读取当前值；它不会修改应用状态。

### `int currentIndex() const`

**作用与语义：**

该属性包含组合框中当前项目的索引。
当前索引在插入或移除物品时可能会变化。
默认情况下，对于空的连击盒或当前未设置任何物品的连击盒，该属性的值为-1。

**如何使用：** 调用 `currentIndex()` 读取当前值；它不会修改应用状态。

### `QString currentText() const`

**作用与语义：**

该属性包含当前文本。
如果组合框可编辑，当前文本即为行编辑显示的值。否则，当前文本为当前物品值，或当组合框为空或当前未设置时为空字符串。
如果组合框可编辑，setter则调用`setEditText()`。否则，如果列表中有匹配文本，`currentIndex`会被设置为对应的索引。

**如何使用：** 调用 `currentText()` 读取当前值；它不会修改应用状态。

### `bool duplicatesEnabled() const`

**作用与语义：**

该属性决定用户是否可以将重复物品输入组合框。
请注意，总可以程序化地将重复物品插入组合盒中。
默认情况下，该属性是`false`的（不允许重复）。

**如何使用：** 调用 `duplicatesEnabled()` 读取当前值；它不会修改应用状态。

### `bool hasFrame() const`

**作用与语义：**

该属性决定组合盒是否用框架绘制。
如果启用（默认），连击盒会在一个框架内绘制自己，否则组合框会在没有任何帧的情况下绘制自己。

**如何使用：** 调用 `hasFrame()` 读取当前值；它不会修改应用状态。

### `QSize iconSize() const`

**作用与语义：**

该属性表示组合框中图标的大小。
除非明确设置，否则返回当前样式的默认值。该大小是图标的最大尺寸;较小的图标不会被放大。

**如何使用：** 调用 `iconSize()` 读取当前值；它不会修改应用状态。

### `QComboBox::InsertPolicy insertPolicy() const`

**作用与语义：**

此属性保存用于确定用户插入项在组合框中应显示位置的策略。
默认值是 `InsertAtBottom`，表示新项将出现在项目列表的底部。

**如何使用：** 调用 `insertPolicy()` 读取当前值；它不会修改应用状态。

### `bool isEditable() const`

**作用与语义：**

该属性决定用户是否可以编辑组合框。
默认情况下，该属性为`false`。编辑效果取决于插入策略。
注意：禁用`editable`状态时，验证者和补全器会被移除。

**如何使用：** 调用 `isEditable()` 读取当前值；它不会修改应用状态。

### `QComboBox::LabelDrawingMode labelDrawingMode() const`

**作用与语义：**

该属性代表组合盒绘制标签的模式。
默认值为`UseStyle`。在将该属性改为`UseDelegate`时，确保也设置合适的项目代理。默认代理取决于样式，可能不适合绘制标签。

**如何使用：** 调用 `labelDrawingMode()` 读取当前值；它不会修改应用状态。

### `int maxCount() const`

**作用与语义：**

该属性包含组合箱中允许的最大物品数量。
注意：如果你把组合盒中最大物品数量设置为小于当前数量，额外的物品会被截断。如果你在组合盒上设置了外部模型，这同样适用。
默认情况下，该属性的值是从可用的最大有符号整数（通常是2147483647）推导出来的。

**如何使用：** 调用 `maxCount()` 读取当前值；它不会修改应用状态。

### `int maxVisibleItems() const`

**作用与语义：**

该属性能显示组合盒屏幕上的最大允许尺寸，单位为物品。
默认情况下，该属性的值为10。
注意：对于某些样式（如Mac样式或Gtk样式）`QStyle::SH_ComboBox_Popup`中，不可编辑组合框（如Mac样式或Gtk样式）则忽略此特性。

**如何使用：** 调用 `maxVisibleItems()` 读取当前值；它不会修改应用状态。

### `int minimumContentsLength() const`

**作用与语义：**

该属性包含组合框中应容纳的最少字符数。
默认值是0。
如果该属性被设定为正值，`minimumSizeHint()`和`sizeHint()`会考虑它。

**如何使用：** 调用 `minimumContentsLength()` 读取当前值；它不会修改应用状态。

### `int modelColumn() const`

**作用与语义：**

该属性保存模型中可见的列。
如果在填充组合框之前设置，弹出视图将不受影响，并将显示第一列（使用此属性的默认值）。
默认情况下，此属性的值为0。
注意：在可编辑的组合框中，可见列也将成为补全列。

**如何使用：** 调用 `modelColumn()` 读取当前值；它不会修改应用状态。

### `QString placeholderText() const`

**作用与语义：**

设置一个`placeholderText`文本，当没有有效索引时显示。
当设置了无效索引时，`placeholderText`会显示出来。该文本在下拉列表中无法访问。当在添加项目前调用该函数时，会显示占位符文本，否则你必须程序调用 `setCurrentIndex`（-1）才能显示占位符文本。设置一个空的占位符文本以重置设置。
当`QComboBox`可编辑时，使用该`QLineEdit::setPlaceholderText()`。

**如何使用：** 调用 `placeholderText()` 读取当前值；它不会修改应用状态。

### `void setDuplicatesEnabled(bool enable)`

**作用与语义：**

该属性决定用户是否可以将重复物品输入组合框。
请注意，总可以程序化地将重复物品插入组合盒中。
默认情况下，该属性是`false`的（不允许重复）。

**如何使用：** 调用 `setDuplicatesEnabled(...)` 修改 `duplicatesEnabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setEditable(bool editable)`

**作用与语义：**

该属性决定用户是否可以编辑组合框。
默认情况下，该属性为`false`。编辑效果取决于插入策略。
注意：禁用`editable`状态时，验证者和补全器会被移除。

**如何使用：** 调用 `setEditable(...)` 修改 `editable`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFrame(bool)`

**作用与语义：**

该属性决定组合盒是否用框架绘制。
如果启用（默认），连击盒会在一个框架内绘制自己，否则组合框会在没有任何帧的情况下绘制自己。

**如何使用：** 调用 `setFrame(...)` 修改 `frame`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setIconSize(const QSize &size)`

**作用与语义：**

该属性表示组合框中图标的大小。
除非明确设置，否则返回当前样式的默认值。该大小是图标的最大尺寸;较小的图标不会被放大。

**如何使用：** 调用 `setIconSize(...)` 修改 `iconSize`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setInsertPolicy(QComboBox::InsertPolicy policy)`

**作用与语义：**

此属性保存用于确定用户插入项在组合框中应显示位置的策略。
默认值是 `InsertAtBottom`，表示新项将出现在项目列表的底部。

**如何使用：** 调用 `setInsertPolicy(...)` 修改 `insertPolicy`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLabelDrawingMode(QComboBox::LabelDrawingMode labelDrawing)`

**作用与语义：**

该属性代表组合盒绘制标签的模式。
默认值为`UseStyle`。在将该属性改为`UseDelegate`时，确保也设置合适的项目代理。默认代理取决于样式，可能不适合绘制标签。

**如何使用：** 调用 `setLabelDrawingMode(...)` 修改 `labelDrawingMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMaxCount(int max)`

**作用与语义：**

该属性包含组合箱中允许的最大物品数量。
注意：如果你把组合盒中最大物品数量设置为小于当前数量，额外的物品会被截断。如果你在组合盒上设置了外部模型，这同样适用。
默认情况下，该属性的值是从可用的最大有符号整数（通常是2147483647）推导出来的。

**如何使用：** 调用 `setMaxCount(...)` 修改 `maxCount`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMaxVisibleItems(int maxItems)`

**作用与语义：**

该属性能显示组合盒屏幕上的最大允许尺寸，单位为物品。
默认情况下，该属性的值为10。
注意：对于某些样式（如Mac样式或Gtk样式）`QStyle::SH_ComboBox_Popup`中，不可编辑组合框（如Mac样式或Gtk样式）则忽略此特性。

**如何使用：** 调用 `setMaxVisibleItems(...)` 修改 `maxVisibleItems`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMinimumContentsLength(int characters)`

**作用与语义：**

该属性包含组合框中应容纳的最少字符数。
默认值是0。
如果该属性被设定为正值，`minimumSizeHint()`和`sizeHint()`会考虑它。

**如何使用：** 调用 `setMinimumContentsLength(...)` 修改 `minimumContentsLength`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setModelColumn(int visibleColumn)`

**作用与语义：**

该属性保存模型中可见的列。
如果在填充组合框之前设置，弹出视图将不受影响，并将显示第一列（使用此属性的默认值）。
默认情况下，此属性的值为0。
注意：在可编辑的组合框中，可见列也将成为补全列。

**如何使用：** 调用 `setModelColumn(...)` 修改 `modelColumn`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPlaceholderText(const QString &placeholderText)`

**作用与语义：**

设置一个`placeholderText`文本，当没有有效索引时显示。
当设置了无效索引时，`placeholderText`会显示出来。该文本在下拉列表中无法访问。当在添加项目前调用该函数时，会显示占位符文本，否则你必须程序调用 `setCurrentIndex`（-1）才能显示占位符文本。设置一个空的占位符文本以重置设置。
当`QComboBox`可编辑时，使用该`QLineEdit::setPlaceholderText()`。

**如何使用：** 调用 `setPlaceholderText(...)` 修改 `placeholderText`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSizeAdjustPolicy(QComboBox::SizeAdjustPolicy policy)`

**作用与语义：**

此属性保存描述当内容更改时组合框大小变化的策略。
默认值是 `AdjustToContentsOnFirstShow`。

**如何使用：** 调用 `setSizeAdjustPolicy(...)` 修改 `sizeAdjustPolicy`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QComboBox::SizeAdjustPolicy sizeAdjustPolicy() const`

**作用与语义：**

此属性保存描述当内容更改时组合框大小变化的策略。
默认值是 `AdjustToContentsOnFirstShow`。

**如何使用：** 调用 `sizeAdjustPolicy()` 读取当前值；它不会修改应用状态。

### `void setCurrentIndex(int index)`

**作用与语义：**

该属性包含组合框中当前项目的索引。
当前索引在插入或移除物品时可能会变化。
默认情况下，对于空的连击盒或当前未设置任何物品的连击盒，该属性的值为-1。

**如何使用：** 调用 `setCurrentIndex(...)` 修改 `currentIndex`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setCurrentText(const QString &text)`

**作用与语义：**

该属性包含当前文本。
如果组合框可编辑，当前文本即为行编辑显示的值。否则，当前文本为当前物品值，或当组合框为空或当前未设置时为空字符串。
如果组合框可编辑，setter则调用`setEditText()`。否则，如果列表中有匹配文本，`currentIndex`会被设置为对应的索引。

**如何使用：** 调用 `setCurrentText(...)` 修改 `currentText`；传入的新值会成为后续查询和相关界面行为所使用的值。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

不要用显示文本作为唯一业务 ID；区分程序设置 currentIndex 和用户 activated；批量填充时可暂时 blockSignals。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QComboBox` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
