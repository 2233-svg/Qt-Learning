# QCompleter

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QCompleter` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QCompleter` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QCompleter>`
- 继承自：QObject
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

- `enum CompletionMode { PopupCompletion, InlineCompletion, UnfilteredPopupCompletion }`
- `enum ModelSorting { UnsortedModel, CaseSensitivelySortedModel, CaseInsensitivelySortedModel }`

### 属性

- `caseSensitivity : Qt::CaseSensitivity`
- `completionColumn : int`
- `completionMode : CompletionMode`
- `completionPrefix : QString`
- `completionRole : int`
- `filterMode : Qt::MatchFlags`
- `maxVisibleItems : int`
- `modelSorting : ModelSorting`
- `wrapAround : bool`

### 公有函数

- `QCompleter(QObject *parent = nullptr)`
- `QCompleter(QAbstractItemModel *model, QObject *parent = nullptr)`
- `QCompleter(const QStringList &list, QObject *parent = nullptr)`
- `virtual ~QCompleter() override`
- `Qt::CaseSensitivity caseSensitivity() const`
- `int completionColumn() const`
- `int completionCount() const`
- `QCompleter::CompletionMode completionMode() const`
- `QAbstractItemModel * completionModel() const`
- `QString completionPrefix() const`
- `int completionRole() const`
- `QString currentCompletion() const`
- `QModelIndex currentIndex() const`
- `int currentRow() const`
- `Qt::MatchFlags filterMode() const`
- `int maxVisibleItems() const`
- `QAbstractItemModel * model() const`
- `QCompleter::ModelSorting modelSorting() const`
- `virtual QString pathFromIndex(const QModelIndex &index) const`
- `QAbstractItemView * popup() const`
- `void setCaseSensitivity(Qt::CaseSensitivity caseSensitivity)`
- `void setCompletionColumn(int column)`
- `void setCompletionMode(QCompleter::CompletionMode mode)`
- `void setCompletionRole(int role)`
- `bool setCurrentRow(int row)`
- `void setFilterMode(Qt::MatchFlags filterMode)`
- `void setMaxVisibleItems(int maxItems)`
- `void setModel(QAbstractItemModel *model)`
- `void setModelSorting(QCompleter::ModelSorting sorting)`
- `void setPopup(QAbstractItemView *popup)`
- `void setWidget(QWidget *widget)`
- `virtual QStringList splitPath(const QString &path) const`
- `QWidget * widget() const`
- `bool wrapAround() const`

### 公有槽函数

- `void complete(const QRect &rect = QRect())`
- `void setCompletionPrefix(const QString &prefix)`
- `void setWrapAround(bool wrap)`

### 信号

- `void activated(const QModelIndex &index)`
- `void activated(const QString &text)`
- `void highlighted(const QModelIndex &index)`
- `void highlighted(const QString &text)`

### 重实现的保护函数

- `virtual bool event(QEvent *ev) override`
- `virtual bool eventFilter(QObject *o, QEvent *e) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QCompleter::CompletionMode`

**作用与语义：**

该枚举规定了如何向用户提供补全。
- `QCompleter::PopupCompletion`：`0`;当前完成项目会以弹出窗口显示。
- `QCompleter::InlineCompletion`：`2`;补足词以内联形式出现（作为选定文本）。
- `QCompleter::UnfilteredPopupCompletion`：`1`;所有可能的完成项目都会在弹窗中显示，最有可能的建议被标注为当前。

### `enum QCompleter::ModelSorting`

**作用与语义：**

该枚举规定了模型中项的排序方式。
- `QCompleter::UnsortedModel`：`0`;模型未排序。
- `QCompleter::CaseSensitivelySortedModel`：`1`;模型按大小写分类。
- `QCompleter::CaseInsensitivelySortedModel`：`2`;模型对大小写排序不敏感。

### `caseSensitivity : Qt::CaseSensitivity`

**作用与语义：**

该属性表示匹配的大小写敏感性。
默认值是`Qt::CaseSensitive`。

**如何使用：** 调用 `caseSensitivity()` 读取当前值；它不会修改应用状态。

### `completionColumn : int`

**作用与语义：**

该属性包含模型中搜索完备化的列。
如果`popup()`是`QListView`，会自动设置显示该列。
默认情况下，匹配列为0。

**如何使用：** 调用 `completionColumn()` 读取当前值；它不会修改应用状态。

### `completionMode : CompletionMode`

**作用与语义：**

完成项如何提供给用户。
默认值是`QCompleter::PopupCompletion`。

**如何使用：** 调用 `completionMode()` 读取当前值；它不会修改应用状态。

### `completionPrefix : QString`

**作用与语义：**

该属性保存用于提供补全的补全前缀。
`completionModel()` 会更新以反映可能匹配 `prefix` 的列表。

**如何使用：** 调用 `completionPrefix()` 读取当前值；它不会修改应用状态。

### `completionRole : int`

**作用与语义：**

该属性包含用于查询内容以匹配的项目角色。
默认角色是`Qt::EditRole`。

**如何使用：** 调用 `completionRole()` 读取当前值；它不会修改应用状态。

### `filterMode : Qt::MatchFlags`

**作用与语义：**

该特性控制过滤的执行方式。
如果filterMode设置为`Qt::MatchStartsWith`，只有以类型字符开头的条目才会显示。`Qt::MatchContains`会显示包含类型字符的条目，并`Qt::MatchEndsWith`以类型字符结尾的条目。
将 filterMode 设置为其他`Qt::MatchFlag`会发出警告，且不会执行任何操作。因此，`Qt::MatchCaseSensitive` 标志没有效果。使用 `caseSensitivity` 属性来控制大小写敏感性。
默认模式是`Qt::MatchStartsWith`。

**如何使用：** 调用 `filterMode()` 读取当前值；它不会修改应用状态。

### `maxVisibleItems : int`

**作用与语义：**

该属性能显示完成器屏幕上的最大允许尺寸，单位为项目。
默认情况下，该属性的值为7。

**如何使用：** 调用 `maxVisibleItems()` 读取当前值；它不会修改应用状态。

### `modelSorting : ModelSorting`

**作用与语义：**

该属性决定了模型的排序方式。
默认情况下，模型中不假设完成化的项目顺序。
如果模型中`completionColumn()`和`completionRole()`的数据按升序排序，你可以将该属性设置为`CaseSensitivelySortedModel`或`CaseInsensitivelySortedModel`。在大型模型中，这能带来显著的性能提升，因为更完整的对象可以使用二分搜索算法而非线性搜索算法。
模型的排序顺序（即升序或降序）通过动态检查模型内容来确定。
注意：上述性能提升无法实现，当完成者的 `caseSensitivity` 与模型排序时使用的大小写敏感性不同。

**如何使用：** 调用 `modelSorting()` 读取当前值；它不会修改应用状态。

### `wrapAround : bool`

**作用与语义：**

该属性保存导航项目时补全是否循环。
默认值为true。

**如何使用：** 调用 `wrapAround()` 读取当前值；它不会修改应用状态。

### `QCompleter::QCompleter(QObject *parent = nullptr)`

**作用与语义：**

构造一个具有给定`parent`的完备对象。

### `QCompleter::QCompleter(QAbstractItemModel *model, QObject *parent = nullptr)`

**作用与语义：**

构造一个包含给定`parent`的完备对象，提供指定`model`的完备化。

### `QCompleter::QCompleter(const QStringList &list, QObject *parent = nullptr)`

**作用与语义：**

构造一个带有给定`parent`的QCompleter对象，使用指定`list`作为可能完备化的源。

### `[override virtual noexcept] QCompleter::~QCompleter()`

**作用与语义：**

摧毁完备对象。

### `[signal] void QCompleter::activated(const QModelIndex &index)`

**作用与语义：**

当用户激活`popup()`中的某个物品时，会发送该信号。（通过点击或按回车键）该物品在`completionModel()`中的`index`会被显示。
注意：该信号重载。连接此信号：


使用 qOverload 连接：
connect（completer， qOverload（&QCompleter：：activated），。
receiver， &ReceiverClass：：slot）;

或者用λ：
connect（completer， qOverload（&QCompleter：：activated），。
this， []（const QModelIndex & index） { /* handle activated */ }）;


更多示例和方法，请参见连接重载信号。

### `[signal] void QCompleter::activated(const QString &text)`

**作用与语义：**

当用户通过点击或按回车激活`popup()`中的某个物品时，会发送该信号。该物品的`text`会被显示出来。
注意：该信号重载。连接此信号：


使用 qOverload 连接：
connect（completer， qOverload（&QCompleter：：activated），。
receiver， &ReceiverClass：：slot）;

或者用λ：
connect（completer， qOverload（&QCompleter：：activated），。
this， []（const QString &text） { /* handle activated */ }）;


更多示例和方法，请参见连接重载信号。

### `[slot] void QCompleter::complete(const QRect &rect = QRect())`

**作用与语义：**

对于`QCompleter::PopupCompletion`和QCompletion：：UnfilteredPopupCompletion模式，调用该函数会显示当前补全的弹窗。默认情况下，如果未指定`rect`，弹窗会显示在`widget()`底部。如果指定`rect`，弹窗会显示在矩形的左侧边缘。
对于`QCompleter::InlineCompletion`模式，`highlighted()`信号与当前完成信号一起发射。

### `int QCompleter::completionCount() const`

**作用与语义：**

返回当前前缀的完成次数。对于未排序且项目数量众多的模型，这可能成本较高。使用`setCurrentRow()`和`currentCompletion()`遍历所有补全。

### `QAbstractItemModel *QCompleter::completionModel() const`

**作用与语义：**

返回完备化模型。完备模型是一个只读列表模型，包含当前完备前缀的所有可能匹配。完备模型会自动更新以反映当前完备化。
注意：该函数的返回值被定义为`QAbstractItemModel`，纯粹是为了一般性。这种实际返回的模型是`QAbstractProxyModel`子类的一个实例。

### `QString QCompleter::currentCompletion() const`

**作用与语义：**

返回当前的补全字符串。这包括 `completionPrefix`。与 `setCurrentRow()` 一起使用时，可以用来遍历所有匹配。

### `QModelIndex QCompleter::currentIndex() const`

**作用与语义：**

返回当前完备化的模型索引`completionModel()`。

### `int QCompleter::currentRow() const`

**作用与语义：**

返回当前行。

### `[override virtual protected] bool QCompleter::event(QEvent *ev)`

**作用与语义：**

重实现自：`QObject::event`（QEvent *e）。

### `[override virtual protected] bool QCompleter::eventFilter(QObject *o, QEvent *e)`

**作用与语义：**

重装：`QObject::eventFilter`（QObject *已观看，QEvent *事件）。

### `[signal] void QCompleter::highlighted(const QModelIndex &index)`

**作用与语义：**

当用户在`popup()`中选中某个项目时，会发送该信号。如果`complete()`被调用且`completionMode()`设置为`QCompleter::InlineCompletion`，也会发送该信号。该物品在`completionModel()`中的`index`会被给出。
注意：该信号重载。连接此信号：


使用 qOverload 连接：
connect（completer， qOverload（&QCompleter：：highlighted），。
receiver， &ReceiverClass：：slot）;

或者用λ：
connect（completer， qOverload（&QCompleter：：highlighted），。
this， []（const QModelIndex &index） { /* handle highlighted */ }）;


更多示例和方法，请参见连接重载信号。

### `[signal] void QCompleter::highlighted(const QString &text)`

**作用与语义：**

当用户在`popup()`中选中某个物品时，会发送该信号。如果`completionMode()`设置为`QCompleter::InlineCompletion`，`complete()`也会发送。该物品的`text`会被给出。
注意：该信号重载。连接此信号：


使用 qOverload 连接：
connect（completer， qOverload（&QCompleter：：highlighted），。
receiver， &ReceiverClass：：slot）;

或者用λ：
connect（completer， qOverload（&QCompleter：：highlighted），。
this， []（const QString &text） { /* handle highlighted */ }）;


更多示例和方法，请参见连接重载信号。

### `QAbstractItemModel *QCompleter::model() const`

**作用与语义：**

返回提供完备性字符串的模型。

### `[virtual] QString QCompleter::pathFromIndex(const QModelIndex &index) const`

**作用与语义：**

返回给定`index`的路径。完备对象利用此方法从底层模型获取补全文本。
默认实现会返回列表模型的编辑角色。如果模型是`QFileSystemModel`，则返回绝对文件路径。

### `QAbstractItemView *QCompleter::popup() const`

**作用与语义：**

返回用于显示完成信息的弹窗。

### `bool QCompleter::setCurrentRow(int row)`

**作用与语义：**

将当前行设置为指定的`row`。成功时返回`true`;否则返回`false`。
该函数可与`currentCompletion()`结合使用，遍历所有可能的完备化。

### `void QCompleter::setModel(QAbstractItemModel *model)`

**作用与语义：**

设置模型，提供完备化到`model`。`model`可以是列表模型或树模型。如果模型已经被设置过，且其父`QCompleter`为父模型，则被删除。
为了方便，如果`model`是`QFileSystemModel`，`QCompleter` `caseSensitivity`会切换到Windows上的`Qt::CaseInsensitive`，`Qt::CaseSensitive`其他平台。

### `void QCompleter::setPopup(QAbstractItemView *popup)`

**作用与语义：**

将用于显示完成的弹窗设置为`popup`。`QCompleter`拥有视图的所有权。
当`completionMode()`设置为`QCompleter::PopupCompletion`或`QCompleter::UnfilteredPopupCompletion`时，会自动生成`QListView`。默认弹窗显示`completionColumn()`。
确保在修改视图设置前调用该函数。这是必要的，因为视图的属性可能要求视图上已设置模型（例如，隐藏视图中的列需要在视图上设置模型）。

### `void QCompleter::setWidget(QWidget *widget)`

**作用与语义：**

将提供完成的控件设置为`widget`。当使用 `QLineEdit::setCompleter()` 在`QLineEdit`上设置`QCompleter`或使用 `QComboBox::setCompleter()` 在`QComboBox`上设置时，该函数会自动调用。在为自定义控件提供完成时，需要显式设置该控件。

### `[virtual] QStringList QCompleter::splitPath(const QString &path) const`

**作用与语义：**

将给定`path`拆分为字符串，用于在`model()`的每个层级匹配。
splitPath() 的默认实现是基于 sourceModel() `QDir::separator()` 分割文件系统路径，当 sourceModel() 是`QFileSystemModel`时。
当用于列表模型时，返回列表中的第一个项用于匹配。

### `QWidget *QCompleter::widget() const`

**作用与语义：**

返回完备器对象提供完备的小部件。

### `Qt::CaseSensitivity caseSensitivity() const`

**作用与语义：**

该属性表示匹配的大小写敏感性。
默认值是`Qt::CaseSensitive`。

**如何使用：** 调用 `caseSensitivity()` 读取当前值；它不会修改应用状态。

### `int completionColumn() const`

**作用与语义：**

该属性包含模型中搜索完备化的列。
如果`popup()`是`QListView`，会自动设置显示该列。
默认情况下，匹配列为0。

**如何使用：** 调用 `completionColumn()` 读取当前值；它不会修改应用状态。

### `QCompleter::CompletionMode completionMode() const`

**作用与语义：**

完成项如何提供给用户。
默认值是`QCompleter::PopupCompletion`。

**如何使用：** 调用 `completionMode()` 读取当前值；它不会修改应用状态。

### `QString completionPrefix() const`

**作用与语义：**

该属性保存用于提供补全的补全前缀。
`completionModel()` 会更新以反映可能匹配 `prefix` 的列表。

**如何使用：** 调用 `completionPrefix()` 读取当前值；它不会修改应用状态。

### `int completionRole() const`

**作用与语义：**

该属性包含用于查询内容以匹配的项目角色。
默认角色是`Qt::EditRole`。

**如何使用：** 调用 `completionRole()` 读取当前值；它不会修改应用状态。

### `Qt::MatchFlags filterMode() const`

**作用与语义：**

该特性控制过滤的执行方式。
如果filterMode设置为`Qt::MatchStartsWith`，只有以类型字符开头的条目才会显示。`Qt::MatchContains`会显示包含类型字符的条目，并`Qt::MatchEndsWith`以类型字符结尾的条目。
将 filterMode 设置为其他`Qt::MatchFlag`会发出警告，且不会执行任何操作。因此，`Qt::MatchCaseSensitive` 标志没有效果。使用 `caseSensitivity` 属性来控制大小写敏感性。
默认模式是`Qt::MatchStartsWith`。

**如何使用：** 调用 `filterMode()` 读取当前值；它不会修改应用状态。

### `int maxVisibleItems() const`

**作用与语义：**

该属性能显示完成器屏幕上的最大允许尺寸，单位为项目。
默认情况下，该属性的值为7。

**如何使用：** 调用 `maxVisibleItems()` 读取当前值；它不会修改应用状态。

### `QCompleter::ModelSorting modelSorting() const`

**作用与语义：**

该属性决定了模型的排序方式。
默认情况下，模型中不假设完成化的项目顺序。
如果模型中`completionColumn()`和`completionRole()`的数据按升序排序，你可以将该属性设置为`CaseSensitivelySortedModel`或`CaseInsensitivelySortedModel`。在大型模型中，这能带来显著的性能提升，因为更完整的对象可以使用二分搜索算法而非线性搜索算法。
模型的排序顺序（即升序或降序）通过动态检查模型内容来确定。
注意：上述性能提升无法实现，当完成者的 `caseSensitivity` 与模型排序时使用的大小写敏感性不同。

**如何使用：** 调用 `modelSorting()` 读取当前值；它不会修改应用状态。

### `void setCaseSensitivity(Qt::CaseSensitivity caseSensitivity)`

**作用与语义：**

该属性表示匹配的大小写敏感性。
默认值是`Qt::CaseSensitive`。

**如何使用：** 调用 `setCaseSensitivity(...)` 修改 `caseSensitivity`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setCompletionColumn(int column)`

**作用与语义：**

该属性包含模型中搜索完备化的列。
如果`popup()`是`QListView`，会自动设置显示该列。
默认情况下，匹配列为0。

**如何使用：** 调用 `setCompletionColumn(...)` 修改 `completionColumn`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setCompletionMode(QCompleter::CompletionMode mode)`

**作用与语义：**

完成项如何提供给用户。
默认值是`QCompleter::PopupCompletion`。

**如何使用：** 调用 `setCompletionMode(...)` 修改 `completionMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setCompletionRole(int role)`

**作用与语义：**

该属性包含用于查询内容以匹配的项目角色。
默认角色是`Qt::EditRole`。

**如何使用：** 调用 `setCompletionRole(...)` 修改 `completionRole`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFilterMode(Qt::MatchFlags filterMode)`

**作用与语义：**

该特性控制过滤的执行方式。
如果filterMode设置为`Qt::MatchStartsWith`，只有以类型字符开头的条目才会显示。`Qt::MatchContains`会显示包含类型字符的条目，并`Qt::MatchEndsWith`以类型字符结尾的条目。
将 filterMode 设置为其他`Qt::MatchFlag`会发出警告，且不会执行任何操作。因此，`Qt::MatchCaseSensitive` 标志没有效果。使用 `caseSensitivity` 属性来控制大小写敏感性。
默认模式是`Qt::MatchStartsWith`。

**如何使用：** 调用 `setFilterMode(...)` 修改 `filterMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMaxVisibleItems(int maxItems)`

**作用与语义：**

该属性能显示完成器屏幕上的最大允许尺寸，单位为项目。
默认情况下，该属性的值为7。

**如何使用：** 调用 `setMaxVisibleItems(...)` 修改 `maxVisibleItems`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setModelSorting(QCompleter::ModelSorting sorting)`

**作用与语义：**

该属性决定了模型的排序方式。
默认情况下，模型中不假设完成化的项目顺序。
如果模型中`completionColumn()`和`completionRole()`的数据按升序排序，你可以将该属性设置为`CaseSensitivelySortedModel`或`CaseInsensitivelySortedModel`。在大型模型中，这能带来显著的性能提升，因为更完整的对象可以使用二分搜索算法而非线性搜索算法。
模型的排序顺序（即升序或降序）通过动态检查模型内容来确定。
注意：上述性能提升无法实现，当完成者的 `caseSensitivity` 与模型排序时使用的大小写敏感性不同。

**如何使用：** 调用 `setModelSorting(...)` 修改 `modelSorting`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `bool wrapAround() const`

**作用与语义：**

该属性保存导航项目时补全是否循环。
默认值为true。

**如何使用：** 调用 `wrapAround()` 读取当前值；它不会修改应用状态。

### `void setCompletionPrefix(const QString &prefix)`

**作用与语义：**

该属性保存用于提供补全的补全前缀。
`completionModel()` 会更新以反映可能匹配 `prefix` 的列表。

**如何使用：** 调用 `setCompletionPrefix(...)` 修改 `completionPrefix`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setWrapAround(bool wrap)`

**作用与语义：**

该属性保存导航项目时补全是否循环。
默认值为true。

**如何使用：** 调用 `setWrapAround(...)` 修改 `wrapAround`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QCompleter` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
