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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 112 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QComboBox::InsertPolicy`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QComboBox` 暴露的类型声明 `插入、Policy`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:InsertPolicy`。
- 属性名：`QComboBox`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] enum class QComboBox::LabelDrawingMode`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QComboBox` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:LabelDrawingMode`。
- 属性名：`QComboBox`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QComboBox::SizeAdjustPolicy`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QComboBox` 暴露的类型声明 `尺寸或数量、Adjust、Policy`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:SizeAdjustPolicy`。
- 属性名：`QComboBox`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] count : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QComboBox` 的状态/能力属性。通常通过 `count()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`count`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] currentData : QVariant`

**API 类别：** 属性说明

**中文解读：** 这是 `QComboBox` 的状态/能力属性。通常通过 `currentData()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`QVariant`。
- 属性名：`currentData`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `currentIndex : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QComboBox` 的配置属性。初始化或状态切换时通过 `setCurrentIndex(...)` 设置，之后用 `currentIndex()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`currentIndex`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `currentText : QString`

**API 类别：** 属性说明

**中文解读：** 这是 `QComboBox` 的配置属性。初始化或状态切换时通过 `setCurrentText(...)` 设置，之后用 `currentText()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QString`。
- 属性名：`currentText`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `duplicatesEnabled : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QComboBox` 的配置属性。初始化或状态切换时通过 `setDuplicatesEnabled(...)` 设置，之后用 `duplicatesEnabled()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`duplicatesEnabled`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `editable : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QComboBox` 的配置属性。初始化或状态切换时通过 `setEditable(...)` 设置，之后用 `editable()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`editable`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `frame : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QComboBox` 的配置属性。初始化或状态切换时通过 `setFrame(...)` 设置，之后用 `frame()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`frame`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `iconSize : QSize`

**API 类别：** 属性说明

**中文解读：** 这是 `QComboBox` 的配置属性。初始化或状态切换时通过 `setIconSize(...)` 设置，之后用 `iconSize()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QSize`。
- 属性名：`iconSize`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `insertPolicy : InsertPolicy`

**API 类别：** 属性说明

**中文解读：** 这是 `QComboBox` 的配置属性。初始化或状态切换时通过 `setInsertPolicy(...)` 设置，之后用 `insertPolicy()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`InsertPolicy`。
- 属性名：`insertPolicy`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] labelDrawingMode : LabelDrawingMode`

**API 类别：** 属性说明

**中文解读：** 这是 `QComboBox` 的配置属性。初始化或状态切换时通过 `setLabelDrawingMode(...)` 设置，之后用 `labelDrawingMode()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`LabelDrawingMode`。
- 属性名：`labelDrawingMode`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `maxCount : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QComboBox` 的配置属性。初始化或状态切换时通过 `setMaxCount(...)` 设置，之后用 `maxCount()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`maxCount`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `maxVisibleItems : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QComboBox` 的配置属性。初始化或状态切换时通过 `setMaxVisibleItems(...)` 设置，之后用 `maxVisibleItems()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`maxVisibleItems`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `minimumContentsLength : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QComboBox` 的配置属性。初始化或状态切换时通过 `setMinimumContentsLength(...)` 设置，之后用 `minimumContentsLength()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`minimumContentsLength`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `modelColumn : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QComboBox` 的配置属性。初始化或状态切换时通过 `setModelColumn(...)` 设置，之后用 `modelColumn()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`modelColumn`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `placeholderText : QString`

**API 类别：** 属性说明

**中文解读：** 这是 `QComboBox` 的配置属性。初始化或状态切换时通过 `setPlaceholderText(...)` 设置，之后用 `placeholderText()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QString`。
- 属性名：`placeholderText`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `sizeAdjustPolicy : SizeAdjustPolicy`

**API 类别：** 属性说明

**中文解读：** 这是 `QComboBox` 的配置属性。初始化或状态切换时通过 `setSizeAdjustPolicy(...)` 设置，之后用 `sizeAdjustPolicy()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`SizeAdjustPolicy`。
- 属性名：`sizeAdjustPolicy`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QComboBox::QComboBox(QWidget *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QComboBox` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QWidget *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QComboBox::~QComboBox()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QComboBox` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QComboBox::activated(int index)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QComboBox` 发出的通知信号 `activated`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QComboBox::addItem(const QString &text, const QVariant &userData = QVariant())`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QComboBox` 添加依赖、数据或子对象的 API `addItem`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `userData`：类型为 `const QVariant &`。默认值为 `QVariant()`。传入 `const QVariant &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QComboBox::addItem(const QIcon &icon, const QString &text, const QVariant &userData = QVariant())`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QComboBox` 添加依赖、数据或子对象的 API `addItem`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `icon`：类型为 `const QIcon &`。没有默认值，调用时必须提供。传入 `const QIcon &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `userData`：类型为 `const QVariant &`。默认值为 `QVariant()`。传入 `const QVariant &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QComboBox::addItems(const QStringList &texts)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QComboBox` 添加依赖、数据或子对象的 API `addItems`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `texts`：类型为 `const QStringList &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QComboBox::changeEvent(QEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QComboBox::changeEvent` 用于执行与“change、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QEvent *`。没有默认值，调用时必须提供。传入 `QEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QComboBox::clear()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `clear`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QComboBox::clearEditText()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `clearEditText`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCompleter *QComboBox::completer() const`

**API 类别：** 成员函数说明

**中文解读：** `QComboBox::completer` 用于计算、查询或取得与“completer”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QCompleter *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCompleter *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QComboBox::contextMenuEvent(QContextMenuEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QComboBox::contextMenuEvent` 用于执行与“context、Menu、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QContextMenuEvent *`。没有默认值，调用时必须提供。传入 `QContextMenuEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QComboBox::currentIndexChanged(int index)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QComboBox` 发出的通知信号 `currentIndexChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QComboBox::currentTextChanged(const QString &text)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QComboBox` 发出的通知信号 `currentTextChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QComboBox::editTextChanged(const QString &text)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QComboBox` 发出的通知信号 `editTextChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QComboBox::event(QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QComboBox::event` 用于计算、查询或取得与“event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QComboBox::findData(const QVariant &data, int role = Qt::UserRole, Qt::MatchFlags flags = static_cast<Qt::MatchFlags>(Qt::MatchExactly|Qt::MatchCaseSensitive)) const`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `findData`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`int`。
- 参数 `data`：类型为 `const QVariant &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `role`：类型为 `int`。默认值为 `Qt::UserRole`。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。
- 参数 `flags`：类型为 `Qt::MatchFlags`。默认值为 `static_cast<Qt::MatchFlags>(Qt::MatchExactly|Qt::MatchCaseSensitive)`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QComboBox::findText(const QString &text, Qt::MatchFlags flags = Qt::MatchExactly|Qt::MatchCaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** `QComboBox::findText` 用于计算、查询或取得与“查找、文本”相关的操作。调用时要先确认当前状态和 `text`、`flags` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `flags`：类型为 `Qt::MatchFlags`。默认值为 `Qt::MatchExactly|Qt::MatchCaseSensitive`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QComboBox::focusInEvent(QFocusEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QComboBox::focusInEvent` 用于执行与“focus、In、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QFocusEvent *`。没有默认值，调用时必须提供。传入 `QFocusEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QComboBox::focusOutEvent(QFocusEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QComboBox::focusOutEvent` 用于执行与“focus、Out、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QFocusEvent *`。没有默认值，调用时必须提供。传入 `QFocusEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QComboBox::hideEvent(QHideEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QComboBox::hideEvent` 用于执行与“隐藏、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QHideEvent *`。没有默认值，调用时必须提供。传入 `QHideEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] void QComboBox::hidePopup()`

**API 类别：** 成员函数说明

**中文解读：** `QComboBox::hidePopup` 用于执行与“隐藏、Popup”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QComboBox::highlighted(int index)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QComboBox` 发出的通知信号 `highlighted`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QComboBox::initStyleOption(QStyleOptionComboBox *option) const`

**API 类别：** 成员函数说明

**中文解读：** `QComboBox::initStyleOption` 用于执行与“init、Style、Option”相关的操作。调用时要先确认当前状态和 `option` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `option`：类型为 `QStyleOptionComboBox *`。没有默认值，调用时必须提供。选项或绘制/行为配置对象；调用前确认其中的状态、矩形和样式信息已经初始化。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QComboBox::inputMethodEvent(QInputMethodEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QComboBox::inputMethodEvent` 用于执行与“input、Method、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QInputMethodEvent *`。没有默认值，调用时必须提供。传入 `QInputMethodEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QVariant QComboBox::inputMethodQuery(Qt::InputMethodQuery query) const`

**API 类别：** 成员函数说明

**中文解读：** `QComboBox::inputMethodQuery` 用于计算、查询或取得与“input、Method、查询”相关的操作。调用时要先确认当前状态和 `query` 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `query`：类型为 `Qt::InputMethodQuery`。没有默认值，调用时必须提供。传入 `Qt::InputMethodQuery` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QComboBox::insertItem(int index, const QString &text, const QVariant &userData = QVariant())`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QComboBox` 添加依赖、数据或子对象的 API `insertItem`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `userData`：类型为 `const QVariant &`。默认值为 `QVariant()`。传入 `const QVariant &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QComboBox::insertItem(int index, const QIcon &icon, const QString &text, const QVariant &userData = QVariant())`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QComboBox` 添加依赖、数据或子对象的 API `insertItem`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `icon`：类型为 `const QIcon &`。没有默认值，调用时必须提供。传入 `const QIcon &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `userData`：类型为 `const QVariant &`。默认值为 `QVariant()`。传入 `const QVariant &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QComboBox::insertItems(int index, const QStringList &list)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QComboBox` 添加依赖、数据或子对象的 API `insertItems`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `list`：类型为 `const QStringList &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QComboBox::insertSeparator(int index)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QComboBox` 添加依赖、数据或子对象的 API `insertSeparator`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVariant QComboBox::itemData(int index, int role = Qt::UserRole) const`

**API 类别：** 成员函数说明

**中文解读：** `QComboBox::itemData` 用于计算、查询或取得与“项目访问、数据访问”相关的操作。调用时要先确认当前状态和 `index`、`role` 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `role`：类型为 `int`。默认值为 `Qt::UserRole`。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAbstractItemDelegate *QComboBox::itemDelegate() const`

**API 类别：** 成员函数说明

**中文解读：** `QComboBox::itemDelegate` 用于计算、查询或取得与“项目访问、Delegate”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAbstractItemDelegate *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAbstractItemDelegate *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QIcon QComboBox::itemIcon(int index) const`

**API 类别：** 成员函数说明

**中文解读：** `QComboBox::itemIcon` 用于计算、查询或取得与“项目访问、Icon”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `QIcon`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QIcon`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QComboBox::itemText(int index) const`

**API 类别：** 成员函数说明

**中文解读：** `QComboBox::itemText` 用于计算、查询或取得与“项目访问、文本”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QComboBox::keyPressEvent(QKeyEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QComboBox::keyPressEvent` 用于执行与“key、Press、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QKeyEvent *`。没有默认值，调用时必须提供。传入 `QKeyEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QComboBox::keyReleaseEvent(QKeyEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QComboBox::keyReleaseEvent` 用于执行与“key、释放、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QKeyEvent *`。没有默认值，调用时必须提供。传入 `QKeyEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QLineEdit *QComboBox::lineEdit() const`

**API 类别：** 成员函数说明

**中文解读：** `QComboBox::lineEdit` 用于计算、查询或取得与“行、Edit”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QLineEdit *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QLineEdit *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QSize QComboBox::minimumSizeHint() const`

**API 类别：** 成员函数说明

**中文解读：** `QComboBox::minimumSizeHint` 用于计算、查询或取得与“最小值、尺寸或数量、Hint”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAbstractItemModel *QComboBox::model() const`

**API 类别：** 成员函数说明

**中文解读：** `QComboBox::model` 用于计算、查询或取得与“model”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAbstractItemModel *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAbstractItemModel *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QComboBox::mousePressEvent(QMouseEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QComboBox::mousePressEvent` 用于执行与“mouse、Press、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QMouseEvent *`。没有默认值，调用时必须提供。传入 `QMouseEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QComboBox::mouseReleaseEvent(QMouseEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QComboBox::mouseReleaseEvent` 用于执行与“mouse、释放、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QMouseEvent *`。没有默认值，调用时必须提供。传入 `QMouseEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QComboBox::paintEvent(QPaintEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QComboBox` 的核心操作 `paintEvent`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QPaintEvent *`。没有默认值，调用时必须提供。传入 `QPaintEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QComboBox::removeItem(int index)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeItem`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QComboBox::resizeEvent(QResizeEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QComboBox::resizeEvent` 用于执行与“调整尺寸、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QResizeEvent *`。没有默认值，调用时必须提供。传入 `QResizeEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QModelIndex QComboBox::rootModelIndex() const`

**API 类别：** 成员函数说明

**中文解读：** `QComboBox::rootModelIndex` 用于计算、查询或取得与“root、Model、索引”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QModelIndex`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QModelIndex`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QComboBox::setCompleter(QCompleter *completer)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setCompleter`。调用它会改变 `QComboBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `completer`：类型为 `QCompleter *`。没有默认值，调用时必须提供。传入 `QCompleter *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QComboBox::setEditText(const QString &text)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `setEditText`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QComboBox::setItemData(int index, const QVariant &value, int role = Qt::UserRole)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setItemData`。调用它会改变 `QComboBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `value`：类型为 `const QVariant &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。
- 参数 `role`：类型为 `int`。默认值为 `Qt::UserRole`。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QComboBox::setItemDelegate(QAbstractItemDelegate *delegate)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setItemDelegate`。调用它会改变 `QComboBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `delegate`：类型为 `QAbstractItemDelegate *`。没有默认值，调用时必须提供。传入 `QAbstractItemDelegate *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QComboBox::setItemIcon(int index, const QIcon &icon)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setItemIcon`。调用它会改变 `QComboBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `icon`：类型为 `const QIcon &`。没有默认值，调用时必须提供。传入 `const QIcon &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QComboBox::setItemText(int index, const QString &text)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setItemText`。调用它会改变 `QComboBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QComboBox::setLineEdit(QLineEdit *edit)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setLineEdit`。调用它会改变 `QComboBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `edit`：类型为 `QLineEdit *`。没有默认值，调用时必须提供。传入 `QLineEdit *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] void QComboBox::setModel(QAbstractItemModel *model)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setModel`。调用它会改变 `QComboBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `model`：类型为 `QAbstractItemModel *`。没有默认值，调用时必须提供。数据模型对象。要确认模型生命周期、线程归属、索引有效期和变化通知协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QComboBox::setRootModelIndex(const QModelIndex &index)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setRootModelIndex`。调用它会改变 `QComboBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QComboBox::setValidator(const QValidator *validator)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setValidator`。调用它会改变 `QComboBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `validator`：类型为 `const QValidator *`。没有默认值，调用时必须提供。传入 `const QValidator *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QComboBox::setView(QAbstractItemView *itemView)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setView`。调用它会改变 `QComboBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `itemView`：类型为 `QAbstractItemView *`。没有默认值，调用时必须提供。传入 `QAbstractItemView *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QComboBox::showEvent(QShowEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QComboBox::showEvent` 用于执行与“显示、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QShowEvent *`。没有默认值，调用时必须提供。传入 `QShowEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 通常在控件完成 parent、layout、属性和信号连接后调用；顶层窗口显示后由事件循环处理绘制和输入。

### `[virtual] void QComboBox::showPopup()`

**API 类别：** 成员函数说明

**中文解读：** `QComboBox::showPopup` 用于执行与“显示、Popup”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 通常在控件完成 parent、layout、属性和信号连接后调用；顶层窗口显示后由事件循环处理绘制和输入。

### `[override virtual] QSize QComboBox::sizeHint() const`

**API 类别：** 成员函数说明

**中文解读：** `QComboBox::sizeHint` 用于计算、查询或取得与“尺寸或数量、Hint”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QComboBox::textActivated(const QString &text)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QComboBox` 发出的通知信号 `textActivated`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QComboBox::textHighlighted(const QString &text)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QComboBox` 发出的通知信号 `textHighlighted`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QValidator *QComboBox::validator() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `validator`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`const QValidator *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAbstractItemView *QComboBox::view() const`

**API 类别：** 成员函数说明

**中文解读：** `QComboBox::view` 用于计算、查询或取得与“view”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAbstractItemView *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAbstractItemView *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QComboBox::wheelEvent(QWheelEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QComboBox::wheelEvent` 用于执行与“wheel、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QWheelEvent *`。没有默认值，调用时必须提供。传入 `QWheelEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int count() const`

**API 类别：** 公有函数

**中文解读：** 这是尺寸/数量查询 API `count`，返回 `QComboBox` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVariant currentData(int role = Qt::UserRole) const`

**API 类别：** 公有函数

**中文解读：** `QComboBox::currentData` 用于计算、查询或取得与“当前、数据访问”相关的操作。调用时要先确认当前状态和 `role` 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `role`：类型为 `int`。默认值为 `Qt::UserRole`。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int currentIndex() const`

**API 类别：** 公有函数

**中文解读：** `QComboBox::currentIndex` 用于计算、查询或取得与“当前、索引”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString currentText() const`

**API 类别：** 公有函数

**中文解读：** `QComboBox::currentText` 用于计算、查询或取得与“当前、文本”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool duplicatesEnabled() const`

**API 类别：** 公有函数

**中文解读：** `QComboBox::duplicatesEnabled` 用于计算、查询或取得与“duplicates、启用状态”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool hasFrame() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `hasFrame`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSize iconSize() const`

**API 类别：** 公有函数

**中文解读：** `QComboBox::iconSize` 用于计算、查询或取得与“icon、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QComboBox::InsertPolicy insertPolicy() const`

**API 类别：** 公有函数

**中文解读：** 这是向 `QComboBox` 添加依赖、数据或子对象的 API `insertPolicy`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QComboBox::InsertPolicy`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool isEditable() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `isEditable`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QComboBox::LabelDrawingMode labelDrawingMode() const`

**API 类别：** 公有函数

**中文解读：** `QComboBox::labelDrawingMode` 用于计算、查询或取得与“label、Drawing、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QComboBox::LabelDrawingMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QComboBox::LabelDrawingMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int maxCount() const`

**API 类别：** 公有函数

**中文解读：** `QComboBox::maxCount` 用于计算、查询或取得与“max、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int maxVisibleItems() const`

**API 类别：** 公有函数

**中文解读：** `QComboBox::maxVisibleItems` 用于计算、查询或取得与“max、可见状态、Items”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int minimumContentsLength() const`

**API 类别：** 公有函数

**中文解读：** `QComboBox::minimumContentsLength` 用于计算、查询或取得与“最小值、Contents、Length”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int modelColumn() const`

**API 类别：** 公有函数

**中文解读：** `QComboBox::modelColumn` 用于计算、查询或取得与“model、列”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString placeholderText() const`

**API 类别：** 公有函数

**中文解读：** `QComboBox::placeholderText` 用于计算、查询或取得与“placeholder、文本”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setDuplicatesEnabled(bool enable)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setDuplicatesEnabled`。调用它会改变 `QComboBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setEditable(bool editable)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setEditable`。调用它会改变 `QComboBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `editable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setFrame(bool)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setFrame`。调用它会改变 `QComboBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `bool`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setIconSize(const QSize &size)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setIconSize`。调用它会改变 `QComboBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `const QSize &`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setInsertPolicy(QComboBox::InsertPolicy policy)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setInsertPolicy`。调用它会改变 `QComboBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `policy`：类型为 `QComboBox::InsertPolicy`。没有默认值，调用时必须提供。传入 `QComboBox::InsertPolicy` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setLabelDrawingMode(QComboBox::LabelDrawingMode labelDrawing)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setLabelDrawingMode`。调用它会改变 `QComboBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `labelDrawing`：类型为 `QComboBox::LabelDrawingMode`。没有默认值，调用时必须提供。传入 `QComboBox::LabelDrawingMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setMaxCount(int max)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setMaxCount`。调用它会改变 `QComboBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `max`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setMaxVisibleItems(int maxItems)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setMaxVisibleItems`。调用它会改变 `QComboBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `maxItems`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setMinimumContentsLength(int characters)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setMinimumContentsLength`。调用它会改变 `QComboBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `characters`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setModelColumn(int visibleColumn)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setModelColumn`。调用它会改变 `QComboBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `visibleColumn`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setPlaceholderText(const QString &placeholderText)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setPlaceholderText`。调用它会改变 `QComboBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `placeholderText`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setSizeAdjustPolicy(QComboBox::SizeAdjustPolicy policy)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setSizeAdjustPolicy`。调用它会改变 `QComboBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `policy`：类型为 `QComboBox::SizeAdjustPolicy`。没有默认值，调用时必须提供。传入 `QComboBox::SizeAdjustPolicy` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QComboBox::SizeAdjustPolicy sizeAdjustPolicy() const`

**API 类别：** 公有函数

**中文解读：** `QComboBox::sizeAdjustPolicy` 用于计算、查询或取得与“尺寸或数量、Adjust、Policy”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QComboBox::SizeAdjustPolicy`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QComboBox::SizeAdjustPolicy`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setCurrentIndex(int index)`

**API 类别：** 公有槽函数

**中文解读：** 这是可被信号连接或元对象调用的槽 `setCurrentIndex`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setCurrentText(const QString &text)`

**API 类别：** 公有槽函数

**中文解读：** 这是可被信号连接或元对象调用的槽 `setCurrentText`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
