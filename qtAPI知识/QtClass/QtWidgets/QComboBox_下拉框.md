# Qt QComboBox 深入笔记

> 适用版本：Qt 6.11 Widgets  
> 头文件：`#include <QComboBox>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QWidget -> QComboBox`  
> 定位：下拉框

## 1. 先建立整体认识：它解决什么问题

`QComboBox` 的本质，是让用户在一个紧凑的控件里完成“从已有选项里选一个，必要时还可以输入一个”的操作。

它解决的不是“显示一串文本”这么简单，而是这些实际问题：

- 选项很多，但界面不能太占地方；
- 选项要能和模型数据联动；
- 当前值要能被程序读取和修改；
- 有时用户只能选，有时用户还可以输入；
- 下拉列表要支持图标、用户数据、验证、补全和自定义视图。

可以把它理解成：

```text
QWidget
  └─ QComboBox
```

它表面上是一个下拉框，底层却是一个小型的“选择器 + 可选编辑器 + 模型视图入口”。

## 2. 什么时候该用它

| 场景 | 建议 |
| --- | --- |
| 让用户从一组选项里选一个 | 用 `QComboBox` |
| 选项数量不多，但又不想占太多空间 | 用 `QComboBox` |
| 选项来自模型、数据库或业务数据 | 用 `QComboBox` |
| 用户可以从已有项里选，也可以输入新值 | 用可编辑 `QComboBox` |
| 想做大表格、层级树、复杂筛选器 | 不要只靠它，考虑 `QTableView` / `QTreeView` / 专门控件 |

一句话：**它适合“选择”这个任务，不适合承载复杂交互。**

## 3. 先把几个核心概念分开

### 3.1 `currentIndex`

当前选中的项目索引。  
空组合框或未选中时通常是 `-1`。

### 3.2 `currentText`

当前显示的文本。

- 非可编辑时，通常就是当前条目的文本；
- 可编辑时，就是行编辑里的文本。

### 3.3 `currentData`

当前条目的附加数据，默认读的是 `Qt::UserRole`。

### 3.4 `editable`

是否允许用户直接输入。

- `false`：更像标准下拉选择；
- `true`：更像“下拉 + 输入框”。

### 3.5 `insertPolicy`

用户输入的新值要插到哪里。  
这只有在可编辑并允许插入时才有意义。

## 4. 模型/视图：它不是简单数组

`QComboBox` 内部遵循模型/视图思路：

- `model()` 决定数据从哪来；
- `view()` 决定下拉列表怎么显示；
- `itemDelegate()` 决定条目怎么画；
- `rootModelIndex()` 和 `modelColumn()` 决定看模型的哪一部分。

这意味着 `QComboBox` 不只是 `addItem()` 那么简单。  
你可以直接喂它字符串，也可以接一个外部模型。

## 5. 最小可用代码

### 5.1 最简单的下拉框

```cpp
QComboBox combo;
combo.addItem(tr("中文"));
combo.addItem(tr("English"));
combo.addItem(tr("日本語"));
```

### 5.2 带用户数据

```cpp
combo.addItem(tr("管理员"), 1);
combo.addItem(tr("普通用户"), 2);

int role = combo.currentData().toInt();
```

### 5.3 可编辑下拉框

```cpp
combo.setEditable(true);
combo.setInsertPolicy(QComboBox::InsertAtBottom);
combo.setPlaceholderText(tr("请选择或输入"));
```

### 5.4 绑定模型

```cpp
combo.setModel(model);
combo.setModelColumn(1);
```

## 6. 构造与默认状态

`QComboBox(QWidget *parent = nullptr)` 构造一个下拉框，默认使用 `QStandardItemModel`。

它的几个常见默认值要记住：

- `editable = false`
- `currentIndex = -1`
- `count = 0`
- `duplicatesEnabled = false`
- `frame = true`
- `insertPolicy = InsertAtBottom`
- `maxVisibleItems = 10`
- `minimumContentsLength = 0`
- `modelColumn = 0`
- `sizeAdjustPolicy = AdjustToContentsOnFirstShow`
- `labelDrawingMode = UseStyle`

这些默认值基本决定了它最常见的样子：一个带边框、默认不可编辑、显示第一列的标准下拉框。

## 7. 增删改查：items 这一层怎么用

### 7.1 `addItem()` / `addItems()`

`addItem()` 向末尾追加一个项目，`addItems()` 批量追加字符串。

适合：

- 固定选项；
- 少量枚举；
- 小型配置项。

### 7.2 `insertItem()` / `insertItems()`

插入到指定位置。  
如果索引超范围，会自动追加或前插。

### 7.3 `removeItem()`

移除某个位置的条目。  
如果移除的是当前项，`currentIndex` 会随之更新。

### 7.4 `clear()`

清空全部条目。  
如果你接的是外部模型，也会把模型内容清掉，所以要特别小心。

### 7.5 `setItemText()` / `setItemIcon()` / `setItemData()`

这三个函数分别改：

- 显示文本；
- 图标；
- 角色数据。

这是比重新插入更稳的做法，适合“只改某一项”的场景。

## 8. 查找：别只盯着文本

### 8.1 `findText()`

按显示文本查找条目索引。

### 8.2 `findData()`

按附加数据查找条目索引。

这在“UI 选项和业务枚举对应”时特别好用。  
比如你存的是角色值、ID、状态码，查找时就不用靠显示文字。

## 9. 可编辑下拉框：它已经不只是选择框了

当 `editable` 打开后，`QComboBox` 变成“可输入的下拉框”。

这时会多出几样东西：

- `lineEdit()`
- `setLineEdit()`
- `validator()`
- `setValidator()`
- `completer()`
- `setCompleter()`
- `setEditText()`
- `clearEditText()`

这套组合解决的是“用户可以输入，但输入要受控”的问题。

### 9.1 `validator`

约束用户输入合法性。  
当 `editable` 变成 `false` 时，验证器会被移除。

### 9.2 `completer`

自动补全输入。  
可编辑下拉框默认会自动创建一个大小写不敏感的内联补全器。

### 9.3 `setEditText()`

直接改编辑区里的文本，不一定等于选中某个现有项。

### 9.4 `placeholderText`

只有在当前没有有效索引时才会显示。  
如果是可编辑框，真正的占位文本通常该设在线编辑器上。

## 10. 模型和视图替换：这是它真正强的地方

### 10.1 `setModel()`

把组合框的数据源换成外部模型。

### 10.2 `setView()`

替换弹出列表的视图。

### 10.3 `setItemDelegate()`

替换条目绘制方式。

### 10.4 `setRootModelIndex()` / `setModelColumn()`

控制从模型的哪一层、哪一列来显示内容。

这几个函数合起来，说明 `QComboBox` 其实是一个可以挂上复杂模型的轻量选择器，不只是“字符串数组下拉框”。

## 11. 下拉弹出与隐藏

### 11.1 `showPopup()`

显示选项列表。  
如果列表为空，就不会显示条目。

### 11.2 `hidePopup()`

隐藏列表，并重置内部状态。  
如果你重写了 `showPopup()` 做自定义弹层，也要重写 `hidePopup()` 去收尾。

这两个函数是自定义弹出交互的入口。

## 12. 信号：选中变化和用户操作不是一回事

`QComboBox` 的信号要分清：

| 信号 | 含义 |
| --- | --- |
| `activated(int)` | 用户选择了某项 |
| `textActivated(const QString &)` | 用户选择了某个文本 |
| `highlighted(int)` | 下拉列表中某项被高亮 |
| `textHighlighted(const QString &)` | 高亮项的文本 |
| `currentIndexChanged(int)` | 当前索引变化 |
| `currentTextChanged(const QString &)` | 当前文本变化 |
| `editTextChanged(const QString &)` | 编辑框里的文本变化 |

这里最容易混的是：

- `activated` 关注“用户选了什么”；
- `currentIndexChanged` 关注“当前索引是否真的变了”；
- `currentTextChanged` 关注“当前文本是否真的变了”。

它们不是同一个时机。

## 13. 常见使用场景

### 13.1 枚举选择

把枚举名显示给用户，内部存枚举值。

### 13.2 数据字典选择

显示中文名称，内部存 ID。

### 13.3 可输入历史值

用户可从历史项里选，也可输入新值。

### 13.4 模型驱动的层级选择

比如选择分类、仓库、区域、字段。

## 14. 常见误区

### 14.1 “我改了文本，数据没变”

文本和数据是两回事。  
要同步业务值，应该改 `currentData` 对应的条目数据。

### 14.2 “editable 打开后补全没了”

检查你是否替换了 `lineEdit`，或者把 `editable` 关掉了。  
这两个动作都会影响 `completer`。

### 14.3 “setModel 后原来的 addItem 没反应”

因为数据源已经换成外部模型了。  
这时应该操作模型，而不是继续把它当内部列表。

### 14.4 “placeholderText 不显示”

检查当前是否还有有效索引。  
可编辑时还要看是不是该设在线编辑器上。

### 14.5 “按钮按下去后 currentIndexChanged 没发”

`activated` 和 `currentIndexChanged` 不是一回事。  
一个偏用户动作，一个偏状态变化。

## 15. 逐项 API 说明

### 成员类型

#### `enum QComboBox::InsertPolicy`

**作用：** 决定用户输入的新项插入哪里。

#### `enum class QComboBox::LabelDrawingMode`

**作用：** 决定组合框标签如何绘制。

#### `enum QComboBox::SizeAdjustPolicy`

**作用：** 决定尺寸提示如何随内容变化。

### 属性

#### `count : int`

**作用：** 当前项数量。  
**默认值：** `0`

#### `currentData : QVariant`

**作用：** 当前项的数据。  
**默认值：** 无效 `QVariant`

#### `currentIndex : int`

**作用：** 当前项索引。  
**默认值：** `-1`

#### `currentText : QString`

**作用：** 当前显示文本。

#### `duplicatesEnabled : bool`

**作用：** 是否允许用户输入重复项。  
**默认值：** `false`

#### `editable : bool`

**作用：** 是否允许编辑。  
**默认值：** `false`

#### `frame : bool`

**作用：** 是否绘制边框。  
**默认值：** `true`

#### `iconSize : QSize`

**作用：** 项图标显示尺寸。  
**默认值：** 由样式决定

#### `insertPolicy : InsertPolicy`

**作用：** 用户输入新项时的插入策略。  
**默认值：** `InsertAtBottom`

#### `[since 6.9] labelDrawingMode : LabelDrawingMode`

**作用：** 标签绘制模式。  
**默认值：** `UseStyle`

#### `maxCount : int`

**作用：** 最大条目数。  
**默认值：** 平台整数上限

#### `maxVisibleItems : int`

**作用：** 下拉时最多可见多少项。  
**默认值：** `10`

#### `minimumContentsLength : int`

**作用：** 预留最小字符宽度。  
**默认值：** `0`

#### `modelColumn : int`

**作用：** 可见列。  
**默认值：** `0`

#### `placeholderText : QString`

**作用：** 无有效索引时显示的占位文本。

#### `sizeAdjustPolicy : SizeAdjustPolicy`

**作用：** 内容变化时如何调整尺寸。  
**默认值：** `AdjustToContentsOnFirstShow`

### 成员函数

#### `[explicit] QComboBox::QComboBox(QWidget *parent = nullptr)`

**作用：** 构造一个下拉框，默认使用 `QStandardItemModel`。

#### `[virtual noexcept] QComboBox::~QComboBox()`

**作用：** 销毁下拉框。

#### `int QComboBox::count() const`

**作用：** 返回条目数量。

#### `void QComboBox::setMaxCount(int max)`

**作用：** 设置最大条目数。

#### `int QComboBox::maxCount() const`

**作用：** 查询最大条目数。

#### `int QComboBox::maxVisibleItems() const`

**作用：** 查询最大可见项数。

#### `void QComboBox::setMaxVisibleItems(int maxItems)`

**作用：** 设置最大可见项数。

#### `bool QComboBox::duplicatesEnabled() const`

**作用：** 查询是否允许重复项。

#### `void QComboBox::setDuplicatesEnabled(bool enable)`

**作用：** 设置是否允许重复项。

#### `bool QComboBox::hasFrame() const`

**作用：** 查询是否有边框。

#### `void QComboBox::setFrame(bool)`

**作用：** 设置是否绘制边框。

#### `QComboBox::InsertPolicy QComboBox::insertPolicy() const`

**作用：** 查询插入策略。

#### `void QComboBox::setInsertPolicy(QComboBox::InsertPolicy policy)`

**作用：** 设置插入策略。

#### `QComboBox::SizeAdjustPolicy QComboBox::sizeAdjustPolicy() const`

**作用：** 查询尺寸调整策略。

#### `void QComboBox::setSizeAdjustPolicy(QComboBox::SizeAdjustPolicy policy)`

**作用：** 设置尺寸调整策略。

#### `int QComboBox::minimumContentsLength() const`

**作用：** 查询最小内容长度。

#### `void QComboBox::setMinimumContentsLength(int characters)`

**作用：** 设置最小内容长度。

#### `QSize QComboBox::iconSize() const`

**作用：** 查询图标尺寸。

#### `void QComboBox::setIconSize(const QSize &size)`

**作用：** 设置图标尺寸。

#### `QString QComboBox::placeholderText() const`

**作用：** 查询占位文本。

#### `void QComboBox::setPlaceholderText(const QString &placeholderText)`

**作用：** 设置占位文本。

#### `bool QComboBox::isEditable() const`

**作用：** 查询是否可编辑。

#### `void QComboBox::setEditable(bool editable)`

**作用：** 设置是否可编辑。

#### `void QComboBox::setLineEdit(QLineEdit *edit)`

**作用：** 替换内部行编辑器。

#### `QLineEdit *QComboBox::lineEdit() const`

**作用：** 返回当前行编辑器。

#### `void QComboBox::setValidator(const QValidator *v)`

**作用：** 设置输入校验器。

#### `const QValidator *QComboBox::validator() const`

**作用：** 返回当前校验器。

#### `void QComboBox::setCompleter(QCompleter *c)`

**作用：** 设置自动补全器。

#### `QCompleter *QComboBox::completer() const`

**作用：** 返回自动补全器。

#### `QAbstractItemDelegate *QComboBox::itemDelegate() const`

**作用：** 返回弹出列表的委托。

#### `void QComboBox::setItemDelegate(QAbstractItemDelegate *delegate)`

**作用：** 设置弹出列表的委托。

#### `QAbstractItemModel *QComboBox::model() const`

**作用：** 返回当前模型。

#### `void QComboBox::setModel(QAbstractItemModel *model)`

**作用：** 设置当前模型。

#### `QModelIndex QComboBox::rootModelIndex() const`

**作用：** 返回根索引。

#### `void QComboBox::setRootModelIndex(const QModelIndex &index)`

**作用：** 设置根索引。

#### `int QComboBox::modelColumn() const`

**作用：** 返回可见列。

#### `void QComboBox::setModelColumn(int visibleColumn)`

**作用：** 设置可见列。

#### `QComboBox::LabelDrawingMode QComboBox::labelDrawingMode() const`

**作用：** 返回标签绘制模式。

#### `void QComboBox::setLabelDrawingMode(QComboBox::LabelDrawingMode labelDrawing)`

**作用：** 设置标签绘制模式。

#### `int QComboBox::currentIndex() const`

**作用：** 查询当前索引。

#### `void QComboBox::setCurrentIndex(int index)`

**作用：** 设置当前索引。

#### `QString QComboBox::currentText() const`

**作用：** 查询当前文本。

#### `void QComboBox::setCurrentText(const QString &text)`

**作用：** 设置当前文本。

#### `QVariant QComboBox::currentData(int role = Qt::UserRole) const`

**作用：** 查询当前项数据。

#### `QString QComboBox::itemText(int index) const`

**作用：** 查询指定项文本。

#### `QIcon QComboBox::itemIcon(int index) const`

**作用：** 查询指定项图标。

#### `QVariant QComboBox::itemData(int index, int role = Qt::UserRole) const`

**作用：** 查询指定项数据。

#### `void QComboBox::addItem(const QString &text, const QVariant &userData = QVariant())`

**作用：** 追加文本项。

#### `void QComboBox::addItem(const QIcon &icon, const QString &text, const QVariant &userData = QVariant())`

**作用：** 追加图标文本项。

#### `void QComboBox::addItems(const QStringList &texts)`

**作用：** 批量追加文本项。

#### `void QComboBox::insertItem(int index, const QString &text, const QVariant &userData = QVariant())`

**作用：** 插入文本项。

#### `void QComboBox::insertItem(int index, const QIcon &icon, const QString &text, const QVariant &userData = QVariant())`

**作用：** 插入图标文本项。

#### `void QComboBox::insertItems(int index, const QStringList &list)`

**作用：** 批量插入文本项。

#### `void QComboBox::insertSeparator(int index)`

**作用：** 插入分隔项。

#### `void QComboBox::removeItem(int index)`

**作用：** 删除指定条目。

#### `void QComboBox::setItemText(int index, const QString &text)`

**作用：** 修改条目文本。

#### `void QComboBox::setItemIcon(int index, const QIcon &icon)`

**作用：** 修改条目图标。

#### `void QComboBox::setItemData(int index, const QVariant &value, int role = Qt::UserRole)`

**作用：** 修改条目数据。

#### `void QComboBox::clear()`

**作用：** 清空所有条目。

#### `void QComboBox::clearEditText()`

**作用：** 清空编辑框文本。

#### `void QComboBox::setEditText(const QString &text)`

**作用：** 设置编辑框文本。

#### `int QComboBox::findText(const QString &text, Qt::MatchFlags flags = Qt::MatchExactly|Qt::MatchCaseSensitive) const`

**作用：** 按文本查找索引。

#### `int QComboBox::findData(const QVariant &data, int role = Qt::UserRole, Qt::MatchFlags flags = static_cast<Qt::MatchFlags>(Qt::MatchExactly|Qt::MatchCaseSensitive)) const`

**作用：** 按数据查找索引。

#### `void QComboBox::showPopup()`

**作用：** 显示下拉列表。

#### `void QComboBox::hidePopup()`

**作用：** 隐藏下拉列表。

#### `QSize QComboBox::sizeHint() const`

**作用：** 返回推荐尺寸。

#### `QSize QComboBox::minimumSizeHint() const`

**作用：** 返回最小推荐尺寸。

#### `bool QComboBox::event(QEvent *event)`

**作用：** 统一事件入口。

#### `QVariant QComboBox::inputMethodQuery(Qt::InputMethodQuery query) const`

**作用：** 支持输入法查询。

#### `QVariant QComboBox::inputMethodQuery(Qt::InputMethodQuery query, const QVariant &argument) const`

**作用：** 额外输入法查询接口。

### 信号

#### `[signal] void QComboBox::activated(int index)`

**作用：** 用户激活某项时发出。

#### `[signal] void QComboBox::textActivated(const QString &text)`

**作用：** 用户激活某文本时发出。

#### `[signal] void QComboBox::highlighted(int index)`

**作用：** 高亮项变化时发出。

#### `[signal] void QComboBox::textHighlighted(const QString &text)`

**作用：** 高亮文本变化时发出。

#### `[signal] void QComboBox::currentIndexChanged(int index)`

**作用：** 当前索引变化时发出。

#### `[signal] void QComboBox::currentTextChanged(const QString &text)`

**作用：** 当前文本变化时发出。

#### `[signal] void QComboBox::editTextChanged(const QString &text)`

**作用：** 编辑框文本变化时发出。

### 受保护函数

#### `[override virtual protected] void QComboBox::focusInEvent(QFocusEvent *e)`

**作用：** 获得焦点时处理。

#### `[override virtual protected] void QComboBox::focusOutEvent(QFocusEvent *e)`

**作用：** 失去焦点时处理。

#### `[override virtual protected] void QComboBox::changeEvent(QEvent *e)`

**作用：** 响应变化事件。

#### `[override virtual protected] void QComboBox::resizeEvent(QResizeEvent *e)`

**作用：** 处理尺寸变化。

#### `[override virtual protected] void QComboBox::paintEvent(QPaintEvent *e)`

**作用：** 绘制控件。

#### `[override virtual protected] void QComboBox::showEvent(QShowEvent *e)`

**作用：** 处理显示事件。

#### `[override virtual protected] void QComboBox::hideEvent(QHideEvent *e)`

**作用：** 处理隐藏事件。

#### `[override virtual protected] void QComboBox::mousePressEvent(QMouseEvent *e)`

**作用：** 处理鼠标按下。

#### `[override virtual protected] void QComboBox::mouseReleaseEvent(QMouseEvent *e)`

**作用：** 处理鼠标释放。

#### `[override virtual protected] void QComboBox::keyPressEvent(QKeyEvent *e)`

**作用：** 处理按键按下。

#### `[override virtual protected] void QComboBox::keyReleaseEvent(QKeyEvent *e)`

**作用：** 处理按键释放。

#### `[override virtual protected] void QComboBox::wheelEvent(QWheelEvent *e)`

**作用：** 处理鼠轮。

#### `[override virtual protected] void QComboBox::contextMenuEvent(QContextMenuEvent *e)`

**作用：** 处理上下文菜单。

#### `[override virtual protected] void QComboBox::inputMethodEvent(QInputMethodEvent *)`

**作用：** 处理输入法事件。

#### `[virtual protected] void QComboBox::initStyleOption(QStyleOptionComboBox *option) const`

**作用：** 初始化样式选项。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 成员类型 | `enum QComboBox::InsertPolicy` | 决定新项插入位置 | 只在可编辑场景重要 |
| 成员类型 | `enum class QComboBox::LabelDrawingMode` | 决定标签绘制方式 | Qt 6.9 起提供 |
| 成员类型 | `enum QComboBox::SizeAdjustPolicy` | 决定尺寸如何随内容变化 | 影响 `sizeHint()` |
| 属性 | `count : int` | 项目数量 | 只读 |
| 属性 | `currentData : QVariant` | 当前项数据 | 默认读 `Qt::UserRole` |
| 属性 | `currentIndex : int` | 当前索引 | 空框时是 `-1` |
| 属性 | `currentText : QString` | 当前文本 | 可编辑时来自行编辑 |
| 属性 | `duplicatesEnabled : bool` | 允许重复项 | 只约束用户输入 |
| 属性 | `editable : bool` | 是否可编辑 | 会影响验证器和补全器 |
| 属性 | `frame : bool` | 是否绘制边框 | 默认 `true` |
| 属性 | `iconSize : QSize` | 图标尺寸 | 小图不会自动放大 |
| 属性 | `insertPolicy : InsertPolicy` | 新项插入策略 | 默认 `InsertAtBottom` |
| 属性 | `[since 6.9] labelDrawingMode : LabelDrawingMode` | 标签绘制方式 | 设成 `UseDelegate` 时要配委托 |
| 属性 | `maxCount : int` | 最大条目数 | 超过会截断 |
| 属性 | `maxVisibleItems : int` | 下拉可见项数 | 默认 `10` |
| 属性 | `minimumContentsLength : int` | 最小内容长度 | 影响尺寸提示 |
| 属性 | `modelColumn : int` | 可见列 | 可编辑时也影响补全列 |
| 属性 | `placeholderText : QString` | 占位文本 | 只有无有效索引时才显示 |
| 属性 | `sizeAdjustPolicy : SizeAdjustPolicy` | 尺寸调整策略 | 默认 `AdjustToContentsOnFirstShow` |
| 成员函数 | `[explicit] QComboBox::QComboBox(QWidget *parent = nullptr)` | 构造下拉框 | 默认使用内部模型 |
| 成员函数 | `[virtual noexcept] QComboBox::~QComboBox()` | 销毁下拉框 | 释放内部对象 |
| 成员函数 | `void QComboBox::addItem(...)` | 追加条目 | 最常用 |
| 成员函数 | `void QComboBox::addItems(...)` | 批量追加 | 适合简单列表 |
| 成员函数 | `void QComboBox::insertItem(...)` | 插入条目 | 按位置控制 |
| 成员函数 | `void QComboBox::insertItems(...)` | 批量插入 | 按位置控制 |
| 成员函数 | `void QComboBox::insertSeparator(int index)` | 插入分隔符 | 弹出列表分组 |
| 成员函数 | `void QComboBox::removeItem(int index)` | 删除条目 | 会影响 currentIndex |
| 成员函数 | `void QComboBox::clear()` | 清空条目 | 外部模型也会被清 |
| 成员函数 | `int QComboBox::findText(...) const` | 按文本找索引 | 返回 `-1` 代表没找到 |
| 成员函数 | `int QComboBox::findData(...) const` | 按数据找索引 | 业务 ID 查找更稳 |
| 成员函数 | `void QComboBox::setCurrentIndex(int index)` | 设置当前索引 | 触发索引变化信号 |
| 成员函数 | `void QComboBox::setCurrentText(const QString &text)` | 设置当前文本 | 可编辑和非可编辑语义不同 |
| 成员函数 | `QString QComboBox::currentText() const` | 查询当前文本 | 看显示值 |
| 成员函数 | `QVariant QComboBox::currentData(...) const` | 查询当前数据 | 看业务值 |
| 成员函数 | `void QComboBox::setModel(QAbstractItemModel *model)` | 设置模型 | 不能传空指针 |
| 成员函数 | `QAbstractItemModel *QComboBox::model() const` | 查询模型 | 看当前数据源 |
| 成员函数 | `void QComboBox::setView(QAbstractItemView *itemView)` | 设置弹出视图 | 视图对象会被接管 |
| 成员函数 | `QAbstractItemView *QComboBox::view() const` | 查询弹出视图 | 调试弹层时常看它 |
| 成员函数 | `void QComboBox::setItemDelegate(QAbstractItemDelegate *delegate)` | 设置条目委托 | 会影响弹出列表绘制 |
| 成员函数 | `QAbstractItemDelegate *QComboBox::itemDelegate() const` | 查询条目委托 | 列表绘制入口 |
| 成员函数 | `void QComboBox::setEditable(bool editable)` | 设置可编辑 | 会影响行编辑器 |
| 成员函数 | `QLineEdit *QComboBox::lineEdit() const` | 查询行编辑器 | 只有可编辑时才有 |
| 成员函数 | `void QComboBox::setLineEdit(QLineEdit *edit)` | 设置行编辑器 | 接管所有权 |
| 成员函数 | `void QComboBox::setValidator(const QValidator *v)` | 设置校验器 | 仅可编辑时有效 |
| 成员函数 | `const QValidator *QComboBox::validator() const` | 查询校验器 | 编辑约束 |
| 成员函数 | `void QComboBox::setCompleter(QCompleter *c)` | 设置补全器 | 不可编辑时会被忽略 |
| 成员函数 | `QCompleter *QComboBox::completer() const` | 查询补全器 | 自动补全入口 |
| 成员函数 | `void QComboBox::setPlaceholderText(const QString &placeholderText)` | 设置占位文本 | 无有效索引时显示 |
| 成员函数 | `QSize QComboBox::sizeHint() const` | 查询推荐尺寸 | 会缓存 |
| 成员函数 | `QSize QComboBox::minimumSizeHint() const` | 查询最小推荐尺寸 | 与内容长度有关 |
| 成员函数 | `void QComboBox::showPopup()` | 显示下拉列表 | 自定义弹层入口 |
| 成员函数 | `void QComboBox::hidePopup()` | 隐藏下拉列表 | 重写时要恢复内部状态 |
| 成员函数 | `QVariant QComboBox::inputMethodQuery(...) const` | 输入法查询 | 处理输入法支持 |
| 信号 | `activated(int)` | 用户激活项 | 不等于真正的状态变化 |
| 信号 | `textActivated(const QString &)` | 用户激活文本 | 只看文本 |
| 信号 | `highlighted(int)` | 高亮项变化 | 悬停/移动时常见 |
| 信号 | `textHighlighted(const QString &)` | 高亮文本变化 | 只看文本 |
| 信号 | `currentIndexChanged(int)` | 当前索引变化 | 真正状态变化 |
| 信号 | `currentTextChanged(const QString &)` | 当前文本变化 | 真正状态变化 |
| 信号 | `editTextChanged(const QString &)` | 编辑文本变化 | 可编辑时常用 |
| 受保护函数 | `initStyleOption(QStyleOptionComboBox *option) const` | 初始化样式选项 | 子类绘制时常用 |

---

### 一句话总结

`QComboBox` 不是一个简单的字符串下拉列表，它是一个可以接模型、接委托、接补全、接验证器的选择控件。选项少时可以直接 `addItem()`，数据复杂时就应该把它当成一个小型模型视图入口来用。
