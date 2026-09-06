# QFormLayout

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QFormLayout` 是 布局管理机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QFormLayout` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QFormLayout>`
- 继承自：QLayout
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

**生命周期：** 顶层布局可以在构造时绑定到 QWidget，也可以通过 `setLayout()` 安装；嵌套布局加入父布局后所有权交给父布局。布局析构不会自动销毁普通 QWidget，动态移除项目时要分别处理控件、子布局和 spacer。

**状态与结果：** 布局的项目索引会随着 add、insert、remove 和 takeAt 改变；索引既包括控件，也包括子布局、固定空白和 stretch。修改项目或尺寸参数后 Qt 会使布局失效并重新计算。

**线程与事件循环：** 布局只应在 GUI 线程操作，因为它直接改变 QWidget 几何和可见界面。布局系统不负责业务线程同步，也不会把手动的跨线程控件访问变安全。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `struct TakeRowResult`
- `enum FieldGrowthPolicy { FieldsStayAtSizeHint, ExpandingFieldsGrow, AllNonFixedFieldsGrow }`
- `enum ItemRole { LabelRole, FieldRole, SpanningRole }`
- `enum RowWrapPolicy { DontWrapRows, WrapLongRows, WrapAllRows }`

### 属性

- `fieldGrowthPolicy : FieldGrowthPolicy`
- `formAlignment : Qt::Alignment`
- `horizontalSpacing : int`
- `labelAlignment : Qt::Alignment`
- `rowWrapPolicy : RowWrapPolicy`
- `verticalSpacing : int`

### 公有函数

- `QFormLayout(QWidget *parent = nullptr)`
- `virtual ~QFormLayout()`
- `void addRow(QWidget *label, QWidget *field)`
- `void addRow(QLayout *layout)`
- `void addRow(QWidget *widget)`
- `void addRow(QWidget *label, QLayout *field)`
- `void addRow(const QString &labelText, QLayout *field)`
- `void addRow(const QString &labelText, QWidget *field)`
- `QFormLayout::FieldGrowthPolicy fieldGrowthPolicy() const`
- `Qt::Alignment formAlignment() const`
- `void getItemPosition(int index, int *rowPtr, QFormLayout::ItemRole *rolePtr) const`
- `void getLayoutPosition(QLayout *layout, int *rowPtr, QFormLayout::ItemRole *rolePtr) const`
- `void getWidgetPosition(QWidget *widget, int *rowPtr, QFormLayout::ItemRole *rolePtr) const`
- `int horizontalSpacing() const`
- `void insertRow(int row, QWidget *label, QWidget *field)`
- `void insertRow(int row, QLayout *layout)`
- `void insertRow(int row, QWidget *widget)`
- `void insertRow(int row, QWidget *label, QLayout *field)`
- `void insertRow(int row, const QString &labelText, QLayout *field)`
- `void insertRow(int row, const QString &labelText, QWidget *field)`
- `(since 6.4) bool isRowVisible(int row) const`
- `(since 6.4) bool isRowVisible(QLayout *layout) const`
- `(since 6.4) bool isRowVisible(QWidget *widget) const`
- `QLayoutItem * itemAt(int row, QFormLayout::ItemRole role) const`
- `Qt::Alignment labelAlignment() const`
- `QWidget * labelForField(QWidget *field) const`
- `QWidget * labelForField(QLayout *field) const`
- `void removeRow(int row)`
- `void removeRow(QLayout *layout)`
- `void removeRow(QWidget *widget)`
- `int rowCount() const`
- `QFormLayout::RowWrapPolicy rowWrapPolicy() const`
- `void setFieldGrowthPolicy(QFormLayout::FieldGrowthPolicy policy)`
- `void setFormAlignment(Qt::Alignment alignment)`
- `void setHorizontalSpacing(int spacing)`
- `void setItem(int row, QFormLayout::ItemRole role, QLayoutItem *item)`
- `void setLabelAlignment(Qt::Alignment alignment)`
- `void setLayout(int row, QFormLayout::ItemRole role, QLayout *layout)`
- `(since 6.4) void setRowVisible(int row, bool on)`
- `(since 6.4) void setRowVisible(QLayout *layout, bool on)`
- `(since 6.4) void setRowVisible(QWidget *widget, bool on)`
- `void setRowWrapPolicy(QFormLayout::RowWrapPolicy policy)`
- `void setVerticalSpacing(int spacing)`
- `void setWidget(int row, QFormLayout::ItemRole role, QWidget *widget)`
- `QFormLayout::TakeRowResult takeRow(int row)`
- `QFormLayout::TakeRowResult takeRow(QLayout *layout)`
- `QFormLayout::TakeRowResult takeRow(QWidget *widget)`
- `int verticalSpacing() const`

### 重实现的公有函数

- `virtual void addItem(QLayoutItem *item) override`
- `virtual int count() const override`
- `virtual Qt::Orientations expandingDirections() const override`
- `virtual bool hasHeightForWidth() const override`
- `virtual int heightForWidth(int width) const override`
- `virtual void invalidate() override`
- `virtual QLayoutItem * itemAt(int index) const override`
- `virtual QSize minimumSize() const override`
- `virtual void setGeometry(const QRect &rect) override`
- `virtual void setSpacing(int spacing) override`
- `virtual QSize sizeHint() const override`
- `virtual int spacing() const override`
- `virtual QLayoutItem * takeAt(int index) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QFormLayout::FieldGrowthPolicy`

**作用与语义：**

该枚举规定了可用于控制表单字段增长方式的不同策略。
- `QFormLayout::FieldsStayAtSizeHint`：`0`;字段从未超过其有效大小提示。这是QMacStyle的默认设置。
- `QFormLayout::ExpandingFieldsGrow`：`1`;具有水平大小策略为`Expanding`或`MinimumExpanding`的场将增长以填满可用空间。其他场不会超出其有效尺寸提示。这是塑性模型的默认策略。
- `QFormLayout::AllNonFixedFieldsGrow`：`2`;所有允许增长的大小策略字段都会增长以填满可用空间。这是大多数样式的默认策略。

### `enum QFormLayout::ItemRole`

**作用与语义：**

该枚举指定了可以出现在一行中的控件类型（或其他布局项）。
- `QFormLayout::LabelRole`：`0`;一个标签控件。
- `QFormLayout::FieldRole`：`1`;一个字段控件。
- `QFormLayout::SpanningRole`：`2`;一个跨标签列和字段列的小部件。

### `enum QFormLayout::RowWrapPolicy`

**作用与语义：**

该枚举规定了可用于控制表单行包裹方式的不同策略。
- `QFormLayout::DontWrapRows`：`0`;字段总是排在标签旁边。这是除 Qt 扩展样式外所有样式的默认策略。
- `QFormLayout::WrapLongRows`：`1`;标签会被分配足够的水平空间以容纳最宽的标签，其余空间分配给字段。如果字段对的最小大小大于可用空间，字段会被包裹到下一行。这是Qt扩展样式的默认策略。
- `QFormLayout::WrapAllRows`：`2`;字段总是在其标签下方排列。

### `fieldGrowthPolicy : FieldGrowthPolicy`

**作用与语义：**

该属性决定了形式场的增长方式。
默认值取决于控件或应用样式。对于 QMacStyle，默认值为 `FieldsStayAtSizeHint`;对于`QCommonStyle`派生样式（如 Plastique 和 Windows），默认值为 `ExpandingFieldsGrow`;对于 Qt 扩展样式，默认值为 `AllNonFixedFieldsGrow`。
如果所有字段都无法增长且表单被调整大小，则根据当前表单的对齐分配额外空间。

**如何使用：** 调用 `fieldGrowthPolicy()` 读取当前值；它不会修改应用状态。

### `formAlignment : Qt::Alignment`

**作用与语义：**

该属性表示表单布局内容在布局几何中的对齐。
默认值取决于控件或应用样式。对于 QMacStyle，默认值为 `Qt::AlignHCenter` |`Qt::AlignTop`;对于其他样式，默认值为 `Qt::AlignLeft` |`Qt::AlignTop`。

**如何使用：** 调用 `formAlignment()` 读取当前值；它不会修改应用状态。

### `horizontalSpacing : int`

**作用与语义：**

该属性决定了并排排列的元件之间的间距。
默认情况下，如果没有明确设置值，布局的水平间距会继承自父布局，或父控件的样式设置。

**如何使用：** 调用 `horizontalSpacing()` 读取当前值；它不会修改应用状态。

### `labelAlignment : Qt::Alignment`

**作用与语义：**

该属性表示标签的水平对齐。
默认值取决于控件或应用样式。对于`QCommonStyle`派生样式（除 QPlastiqueStyle）默认为 `Qt::AlignLeft`;其他样式的默认值为 `Qt::AlignRight`。

**如何使用：** 调用 `labelAlignment()` 读取当前值；它不会修改应用状态。

### `rowWrapPolicy : RowWrapPolicy`

**作用与语义：**

该属性决定了表单行的包裹方式。
默认值取决于小部件或应用样式。对于 Qt 扩展样式，默认值为 `WrapLongRows`;对于其他样式，默认值为 `DontWrapRows`。
如果你想把每个标签显示在其关联字段上方（而不是旁边），可以将该属性设置为`WrapAllRows`。

**如何使用：** 调用 `rowWrapPolicy()` 读取当前值；它不会修改应用状态。

### `verticalSpacing : int`

**作用与语义：**

该属性表示垂直布局的控件之间的间距。
默认情况下，如果没有显式设置值，布局的垂直间距会继承自父布局或父控件的样式设置。

**如何使用：** 调用 `verticalSpacing()` 读取当前值；它不会修改应用状态。

### `[explicit] QFormLayout::QFormLayout(QWidget *parent = nullptr)`

**作用与语义：**

用给定的`parent`小部件构建一个新的表单布局。
布局直接设置为`parent`的顶层布局。一个小部件只能有一个顶层布局。它由`QWidget::layout()`返回。

### `[virtual noexcept] QFormLayout::~QFormLayout()`

**作用与语义：**

这会破坏表单布局。

### `[override virtual] void QFormLayout::addItem(QLayoutItem *item)`

**作用与语义：**

重实现自：`QLayout::addItem`（QLayoutItem *item）。
在子职业中实现以添加`item`。添加方式因子职业而异。
该函数通常不会在应用代码中调用。要向布局添加小部件，使用`addWidget()`函数;要添加子布局，使用相关`QLayout`子类提供的addLayout()函数。
注意：`item`的所有权转移到了布局上，删除它由布局负责。

### `void QFormLayout::addRow(QWidget *label, QWidget *field)`

**作用与语义：**

在该表单布局底部添加一行，包含给定的`label`和`field`。

### `void QFormLayout::addRow(QLayout *layout)`

**作用与语义：**

在表单布局末尾添加指定的`layout`。`layout`跨越了两列。

### `void QFormLayout::addRow(QWidget *widget)`

**作用与语义：**

在表单布局末尾添加指定的`widget`。`widget`跨越了两列。

### `void QFormLayout::addRow(QWidget *label, QLayout *field)`

**作用与语义：**

在该表单布局底部添加一行，包含给定的`label`和`field`。

### `void QFormLayout::addRow(const QString &labelText, QLayout *field)`

**作用与语义：**

此重载会在幕后自动创建一个 `QLabel`，并以 `labelText` 作为其文本。

### `void QFormLayout::addRow(const QString &labelText, QWidget *field)`

**作用与语义：**

此重载会在幕后自动创建一个 `QLabel`，并以 `labelText` 作为其文本。`field` 被设置为新的 `QLabel` 的 `buddy`。

### `[override virtual] int QFormLayout::count() const`

**作用与语义：**

重装：`QLayout::count()` const.
必须在子类中实现，以返回布局中的物品数量。

### `[override virtual] Qt::Orientations QFormLayout::expandingDirections() const`

**作用与语义：**

重装：`QLayout::expandingDirections()` const.

### `void QFormLayout::getItemPosition(int index, int *rowPtr, QFormLayout::ItemRole *rolePtr) const`

**作用与语义：**

检索指定`index`处的行和角色（列）。如果`index`超出边界，*`rowPtr`设为-1;否则该行存储在*`rowPtr`，角色存储在*`rolePtr`。

### `void QFormLayout::getLayoutPosition(QLayout *layout, int *rowPtr, QFormLayout::ItemRole *rolePtr) const`

**作用与语义：**

检索指定子`layout`的行和角色（列）。如果`layout`不在表单布局中，则将*`rowPtr`设置为-1;否则该行存储在*`rowPtr`，角色存储在*`rolePtr`。

### `void QFormLayout::getWidgetPosition(QWidget *widget, int *rowPtr, QFormLayout::ItemRole *rolePtr) const`

**作用与语义：**

检索指定`widget`的行和角色（列）。如果`widget`不在布局中，*`rowPtr`设置为-1;否则该行存储在*`rowPtr`，角色存储在*`rolePtr`。

### `[override virtual] bool QFormLayout::hasHeightForWidth() const`

**作用与语义：**

重装：`QLayoutItem::hasHeightForWidth()` const.
如果该布局的首选高度取决于宽度，则返回`true`;否则返回`false`。默认实现返回false。
在支持宽度高度的布局管理器中重新实现这个功能。

### `[override virtual] int QFormLayout::heightForWidth(int width) const`

**作用与语义：**

重装：`QLayoutItem::heightForWidth`（int） const.
返回该布局项的首选高度，基于宽度，但默认实现中未使用宽度。
默认实现返回 -1，表示首选高度与项目宽度无关。使用函数 `hasHeightForWidth()` 通常比调用该函数并测试 -1 快得多。
在支持宽度高度的布局管理器中重新实现该函数。典型的实现如下：
强烈建议缓存;没有缓存，布局将耗费指数级时间。

### `void QFormLayout::insertRow(int row, QWidget *label, QWidget *field)`

**作用与语义：**

在该表单布局中，在位置`row`插入一行，`label`和`field`。如果`row`越界，则在末尾添加新行。

### `void QFormLayout::insertRow(int row, QLayout *layout)`

**作用与语义：**

在此表单布局中，将指定`layout`插入位置`row`。`layout`跨越两列。如果`row`超出边界，则在末尾添加该小部件。

### `void QFormLayout::insertRow(int row, QWidget *widget)`

**作用与语义：**

在此表单布局中，将指定`widget`插入位置`row`。`widget`跨越两列。如果`row`超出边界，则将小部件添加到末尾。

### `void QFormLayout::insertRow(int row, QWidget *label, QLayout *field)`

**作用与语义：**

在该表单布局中，在位置`row`插入一行，`label`和`field`。如果`row`越界，则在末尾添加新行。

### `void QFormLayout::insertRow(int row, const QString &labelText, QLayout *field)`

**作用与语义：**

此重载会在幕后自动创建一个 `QLabel`，并以 `labelText` 作为其文本。

### `void QFormLayout::insertRow(int row, const QString &labelText, QWidget *field)`

**作用与语义：**

此重载会在幕后自动创建一个 `QLabel`，并以 `labelText` 作为其文本。`field` 被设置为新的 `QLabel` 的 `buddy`。

### `[override virtual] void QFormLayout::invalidate()`

**作用与语义：**

重装：`QLayout::invalidate()`。

### `[since 6.4] bool QFormLayout::isRowVisible(int row) const`

**作用与语义：**

如果行中有部分`row`可见，则返回 true;否则返回 false。

### `[since 6.4] bool QFormLayout::isRowVisible(QLayout *layout) const`

**作用与语义：**

如果对应`layout`行中的某些项可见，则返回真;否则返回假。

### `[since 6.4] bool QFormLayout::isRowVisible(QWidget *widget) const`

**作用与语义：**

如果对应`widget`的行中某些项可见，则返回真;否则返回假。

### `[override virtual] QLayoutItem *QFormLayout::itemAt(int index) const`

**作用与语义：**

重实现自：`QLayout::itemAt`（int index）const.
必须在子类中实现以返回`index`的布局项。如果没有这样的项，函数必须返回`nullptr`。项编号从0依次排列。如果一个项被删除，其他项将被重新编号。
该函数可用于遍历布局。以下代码将为小部件布局结构中的每个布局项绘制一个矩形。

### `QLayoutItem *QFormLayout::itemAt(int row, QFormLayout::ItemRole role) const`

**作用与语义：**

返回给定`row`中的布局项，并返回指定`role`（列）。如果没有该项，则返回`nullptr`。

### `QWidget *QFormLayout::labelForField(QWidget *field) const`

**作用与语义：**

返回与给定`field`关联的标签。

### `QWidget *QFormLayout::labelForField(QLayout *field) const`

**作用与语义：**

返回与给定`field`关联的标签。

### `[override virtual] QSize QFormLayout::minimumSize() const`

**作用与语义：**

重装：`QLayout::minimumSize()` const.

### `void QFormLayout::removeRow(int row)`

**作用与语义：**

删除表单布局中的`row`行。
`row`必须是非负数且小于`rowCount()`。
调用后，`rowCount()`减少一。所有占据该行的控件和嵌套布局都会被删除。这包括字段控件和标签（如有）。后续所有行向上移动一行，释放的垂直空间重新分配到剩余的行。
你可以用这个函数来撤销之前的`addRow()`或`insertRow()`：
如果你想在不删除控件的情况下移除该行，可以用`takeRow()`。

**官方示例：**

```cpp
 QFormLayout *flay = ...;
 QPointer<QLineEdit> le = new QLineEdit;
 flay->insertRow(2, "User:", le);
 // later:
 flay->removeRow(2); // le == nullptr at this point
```

### `void QFormLayout::removeRow(QLayout *layout)`

**作用与语义：**

删除表单布局中对应`layout`的行。
调用后，`rowCount()` 减少一。所有占据该行的控件和嵌套布局都会被删除。这包括字段控件和标签（如有）。后续所有行向上移动一行，释放的垂直空间重新分配给剩余的行。
你可以用这个函数来撤销之前的`addRow()`或`insertRow()`：
如果你想在不删除插入的布局的情况下移除该行，可以用`takeRow()`。

**官方示例：**

```cpp
 QFormLayout *flay = ...;
 QPointer<QVBoxLayout> vbl = new QVBoxLayout;
 flay->insertRow(2, "User:", vbl);
 // later:
 flay->removeRow(layout); // vbl == nullptr at this point
```

### `void QFormLayout::removeRow(QWidget *widget)`

**作用与语义：**

删除表单布局中对应`widget`的行。
调用后，`rowCount()` 减少一。所有占据该行的控件和嵌套布局均被删除。包括字段控件和标签（如有）。后续所有行向上移动一行，释放的垂直空间重新分配给剩余行。
你可以用这个函数来撤销之前的`addRow()`或`insertRow()`：
如果你想在不删除小部件的情况下移除该行，可以用`takeRow()`。

**官方示例：**

```cpp
 QFormLayout *flay = ...;
 QPointer<QLineEdit> le = new QLineEdit;
 flay->insertRow(2, "User:", le);
 // later:
 flay->removeRow(le); // le == nullptr at this point
```

### `int QFormLayout::rowCount() const`

**作用与语义：**

返回表单中的行数。

### `[override virtual] void QFormLayout::setGeometry(const QRect &rect)`

**作用与语义：**

重装：`QLayout::setGeometry`（const QRect & r）。

### `void QFormLayout::setItem(int row, QFormLayout::ItemRole role, QLayoutItem *item)`

**作用与语义：**

将给定`row`中该`role`的物品设置为`item`，必要时用空行扩展布局。
如果该单元格已被占用，则不插入`item`，错误信息发送到控制台。`item`跨越两列。
警告：请勿使用此功能添加子布局或子控件项。请使用`setLayout()`或`setWidget()`。

### `void QFormLayout::setLayout(int row, QFormLayout::ItemRole role, QLayout *layout)`

**作用与语义：**

将给定`row`中对应`role`子布局设置为`layout`，必要时扩展表单布局并保留空行。
如果小区已被占用，`layout`不会入，错误信息会发送到控制台。
注意：对于大多数应用，应使用`addRow()`或`insertRow()`代替 setLayout()。

### `[since 6.4] void QFormLayout::setRowVisible(int row, bool on)`

**作用与语义：**

如果`on`为真，显示`row`行，否则隐藏该行。
`row`必须是非负数且小于`rowCount()`。

### `[since 6.4] void QFormLayout::setRowVisible(QLayout *layout, bool on)`

**作用与语义：**

如果 `on` 为真，则显示对应于 `layout` 的行，否则隐藏该行。

### `[since 6.4] void QFormLayout::setRowVisible(QWidget *widget, bool on)`

**作用与语义：**

如果 `on` 为真，则显示对应于 `widget` 的行，否则隐藏该行。

### `[override virtual] void QFormLayout::setSpacing(int spacing)`

**作用与语义：**

重新实现了属性的访问函数：`QLayout::spacing`。
该函数将垂直和水平间距设置为`spacing`。

### `void QFormLayout::setWidget(int row, QFormLayout::ItemRole role, QWidget *widget)`

**作用与语义：**

将该`role`的给定`row`中的小部件设置为`widget`，必要时扩展布局并保留空行。
如果该单元已被占用，`widget`不会插入，错误信息会发送到控制台。
注意：对于大多数应用，应使用`addRow()`或`insertRow()`代替 setWidget()。

### `[override virtual] QSize QFormLayout::sizeHint() const`

**作用与语义：**

重装：`QLayoutItem::sizeHint()` const.
在子类中实现，以返回该物品的首选大小。

### `[override virtual] int QFormLayout::spacing() const`

**作用与语义：**

重新实现了属性的访问函数：`QLayout::spacing`。
如果垂直间距等于水平间距，该函数返回该值;否则返回-1。

### `[override virtual] QLayoutItem *QFormLayout::takeAt(int index)`

**作用与语义：**

重实现自：`QLayout::takeAt`（整数索引）。
必须在子类中实现，以从布局中移除`index`的布局项并返回该项。如果没有这样的项，函数必须什么都不做，返回0。项编号从0开始依次编号。如果一个项被移除，其他项将被重新编号。
以下代码片段展示了一种安全移除所有布局物品的方法：

### `QFormLayout::TakeRowResult QFormLayout::takeRow(int row)`

**作用与语义：**

从表单布局中移除指定的`row`。
`row`必须是非负数且小于`rowCount()`。
注意：这个功能不会删除任何东西。
调用后，`rowCount()`减少一。后续所有行向上移动一行，释放的垂直空间重新分配到剩余行。
你可以用这个函数来撤销之前的`addRow()`或`insertRow()`：
如果你想从布局中移除该行并删除小部件，可以改用`removeRow()`。
返回包含小部件及其相应标签布局项的结构。

**官方示例：**

```cpp
 QFormLayout *flay = ...;
 QPointer<QLineEdit> le = new QLineEdit;
 flay->insertRow(2, "User:", le);
 // later:
 QFormLayout::TakeRowResult result = flay->takeRow(2);
```

### `QFormLayout::TakeRowResult QFormLayout::takeRow(QLayout *layout)`

**作用与语义：**

去除表单布局中的指定 `layout`。
注意：这个功能不会删除任何东西。
调用后，`rowCount()`减少一。后续所有行向上移动一行，释放的垂直空间重新分配到剩余行。
如果你想从表单布局中移除该行并删除插入的布局，可以用`removeRow()`。
返回包含小部件及其相应标签布局项的结构。

**官方示例：**

```cpp
 QFormLayout *flay = ...;
 QPointer<QVBoxLayout> vbl = new QVBoxLayout;
 flay->insertRow(2, "User:", vbl);
 // later:
 QFormLayout::TakeRowResult result = flay->takeRow(widget);
```

### `QFormLayout::TakeRowResult QFormLayout::takeRow(QWidget *widget)`

**作用与语义：**

从表单布局中移除指定的`widget`。
注意：这个功能不会删除任何东西。
调用后，`rowCount()`减少一。后续所有行向上移动一行，释放的垂直空间重新分配到剩余行。
如果你想从布局中移除该行并删除小部件，可以用`removeRow()`。
返回包含小部件及其相应标签布局项的结构。

**官方示例：**

```cpp
 QFormLayout *flay = ...;
 QPointer<QLineEdit> le = new QLineEdit;
 flay->insertRow(2, "User:", le);
 // later:
 QFormLayout::TakeRowResult result = flay->takeRow(widget);
```

### `struct TakeRowResult`

**作用与语义：**

包含 QFormLayout：：takeRow() 调用的结果。

### `QFormLayout::FieldGrowthPolicy fieldGrowthPolicy() const`

**作用与语义：**

该属性决定了形式场的增长方式。
默认值取决于控件或应用样式。对于 QMacStyle，默认值为 `FieldsStayAtSizeHint`;对于`QCommonStyle`派生样式（如 Plastique 和 Windows），默认值为 `ExpandingFieldsGrow`;对于 Qt 扩展样式，默认值为 `AllNonFixedFieldsGrow`。
如果所有字段都无法增长且表单被调整大小，则根据当前表单的对齐分配额外空间。

**如何使用：** 调用 `fieldGrowthPolicy()` 读取当前值；它不会修改应用状态。

### `Qt::Alignment formAlignment() const`

**作用与语义：**

该属性表示表单布局内容在布局几何中的对齐。
默认值取决于控件或应用样式。对于 QMacStyle，默认值为 `Qt::AlignHCenter` |`Qt::AlignTop`;对于其他样式，默认值为 `Qt::AlignLeft` |`Qt::AlignTop`。

**如何使用：** 调用 `formAlignment()` 读取当前值；它不会修改应用状态。

### `int horizontalSpacing() const`

**作用与语义：**

该属性决定了并排排列的元件之间的间距。
默认情况下，如果没有明确设置值，布局的水平间距会继承自父布局，或父控件的样式设置。

**如何使用：** 调用 `horizontalSpacing()` 读取当前值；它不会修改应用状态。

### `Qt::Alignment labelAlignment() const`

**作用与语义：**

该属性表示标签的水平对齐。
默认值取决于控件或应用样式。对于`QCommonStyle`派生样式（除 QPlastiqueStyle）默认为 `Qt::AlignLeft`;其他样式的默认值为 `Qt::AlignRight`。

**如何使用：** 调用 `labelAlignment()` 读取当前值；它不会修改应用状态。

### `QFormLayout::RowWrapPolicy rowWrapPolicy() const`

**作用与语义：**

该属性决定了表单行的包裹方式。
默认值取决于小部件或应用样式。对于 Qt 扩展样式，默认值为 `WrapLongRows`;对于其他样式，默认值为 `DontWrapRows`。
如果你想把每个标签显示在其关联字段上方（而不是旁边），可以将该属性设置为`WrapAllRows`。

**如何使用：** 调用 `rowWrapPolicy()` 读取当前值；它不会修改应用状态。

### `void setFieldGrowthPolicy(QFormLayout::FieldGrowthPolicy policy)`

**作用与语义：**

该属性决定了形式场的增长方式。
默认值取决于控件或应用样式。对于 QMacStyle，默认值为 `FieldsStayAtSizeHint`;对于`QCommonStyle`派生样式（如 Plastique 和 Windows），默认值为 `ExpandingFieldsGrow`;对于 Qt 扩展样式，默认值为 `AllNonFixedFieldsGrow`。
如果所有字段都无法增长且表单被调整大小，则根据当前表单的对齐分配额外空间。

**如何使用：** 调用 `setFieldGrowthPolicy(...)` 修改 `fieldGrowthPolicy`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFormAlignment(Qt::Alignment alignment)`

**作用与语义：**

该属性表示表单布局内容在布局几何中的对齐。
默认值取决于控件或应用样式。对于 QMacStyle，默认值为 `Qt::AlignHCenter` |`Qt::AlignTop`;对于其他样式，默认值为 `Qt::AlignLeft` |`Qt::AlignTop`。

**如何使用：** 调用 `setFormAlignment(...)` 修改 `formAlignment`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setHorizontalSpacing(int spacing)`

**作用与语义：**

该属性决定了并排排列的元件之间的间距。
默认情况下，如果没有明确设置值，布局的水平间距会继承自父布局，或父控件的样式设置。

**如何使用：** 调用 `setHorizontalSpacing(...)` 修改 `horizontalSpacing`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLabelAlignment(Qt::Alignment alignment)`

**作用与语义：**

该属性表示标签的水平对齐。
默认值取决于控件或应用样式。对于`QCommonStyle`派生样式（除 QPlastiqueStyle）默认为 `Qt::AlignLeft`;其他样式的默认值为 `Qt::AlignRight`。

**如何使用：** 调用 `setLabelAlignment(...)` 修改 `labelAlignment`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setRowWrapPolicy(QFormLayout::RowWrapPolicy policy)`

**作用与语义：**

该属性决定了表单行的包裹方式。
默认值取决于小部件或应用样式。对于 Qt 扩展样式，默认值为 `WrapLongRows`;对于其他样式，默认值为 `DontWrapRows`。
如果你想把每个标签显示在其关联字段上方（而不是旁边），可以将该属性设置为`WrapAllRows`。

**如何使用：** 调用 `setRowWrapPolicy(...)` 修改 `rowWrapPolicy`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setVerticalSpacing(int spacing)`

**作用与语义：**

该属性表示垂直布局的控件之间的间距。
默认情况下，如果没有显式设置值，布局的垂直间距会继承自父布局或父控件的样式设置。

**如何使用：** 调用 `setVerticalSpacing(...)` 修改 `verticalSpacing`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `int verticalSpacing() const`

**作用与语义：**

该属性表示垂直布局的控件之间的间距。
默认情况下，如果没有显式设置值，布局的垂直间距会继承自父布局或父控件的样式设置。

**如何使用：** 调用 `verticalSpacing()` 读取当前值；它不会修改应用状态。

## 6. 深入实践与常见坑

### 生命周期和资源边界

顶层布局可以在构造时绑定到 QWidget，也可以通过 `setLayout()` 安装；嵌套布局加入父布局后所有权交给父布局。布局析构不会自动销毁普通 QWidget，动态移除项目时要分别处理控件、子布局和 spacer。

### 状态和错误边界

布局的项目索引会随着 add、insert、remove 和 takeAt 改变；索引既包括控件，也包括子布局、固定空白和 stretch。修改项目或尺寸参数后 Qt 会使布局失效并重新计算。

### 线程边界

布局只应在 GUI 线程操作，因为它直接改变 QWidget 几何和可见界面。布局系统不负责业务线程同步，也不会把手动的跨线程控件访问变安全。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QFormLayout` 所属机制类型：布局管理机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
