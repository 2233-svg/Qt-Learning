# QListWidget

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QListWidget` 是 Qt 容器类型，负责保存一组元素，并提供插入、删除、查找、遍历和容量管理。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QListWidget` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QListWidget>`
- 继承自：QListView
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

**生命周期：** 容器自己管理元素存储，容器销毁后由它提供的迭代器、引用和 data 指针通常失效。修改容器可能重新分配或 detach，不能把元素地址和迭代器当成长期句柄。

**状态与结果：** 要区分空容器、容量、元素数量、查找失败和默认构造值。插入/删除可能改变索引和迭代器；关联容器还要考虑键唯一性、排序和查找复杂度。

**线程与事件循环：** 不同线程使用各自的容器副本通常安全；同一个容器一边读一边写仍需要同步，即使底层采用隐式共享也不会自动解决数据竞争。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

```cpp
#include <QList>

QList<int> values{1, 2, 3};
values.append(4);
for (const int value : values) {
    // 使用 value
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 属性

- `count : int`
- `currentRow : int`
- `sortingEnabled : bool`
- `(since 6.10) supportedDragActions : Qt::DropActions`

### 公有函数

- `QListWidget(QWidget *parent = nullptr)`
- `virtual ~QListWidget()`
- `void addItem(QListWidgetItem *item)`
- `void addItem(const QString &label)`
- `void addItems(const QStringList &labels)`
- `void closePersistentEditor(QListWidgetItem *item)`
- `int count() const`
- `QListWidgetItem * currentItem() const`
- `int currentRow() const`
- `void editItem(QListWidgetItem *item)`
- `QList<QListWidgetItem *> findItems(const QString &text, Qt::MatchFlags flags) const`
- `QModelIndex indexFromItem(const QListWidgetItem *item) const`
- `void insertItem(int row, QListWidgetItem *item)`
- `void insertItem(int row, const QString &label)`
- `void insertItems(int row, const QStringList &labels)`
- `bool isPersistentEditorOpen(QListWidgetItem *item) const`
- `bool isSortingEnabled() const`
- `QListWidgetItem * item(int row) const`
- `QListWidgetItem * itemAt(const QPoint &p) const`
- `QListWidgetItem * itemAt(int x, int y) const`
- `QListWidgetItem * itemFromIndex(const QModelIndex &index) const`
- `QWidget * itemWidget(QListWidgetItem *item) const`
- `QList<QListWidgetItem *> items(const QMimeData *data) const`
- `void openPersistentEditor(QListWidgetItem *item)`
- `void removeItemWidget(QListWidgetItem *item)`
- `int row(const QListWidgetItem *item) const`
- `QList<QListWidgetItem *> selectedItems() const`
- `void setCurrentItem(QListWidgetItem *item)`
- `void setCurrentItem(QListWidgetItem *item, QItemSelectionModel::SelectionFlags command)`
- `void setCurrentRow(int row)`
- `void setCurrentRow(int row, QItemSelectionModel::SelectionFlags command)`
- `void setItemWidget(QListWidgetItem *item, QWidget *widget)`
- `void setSortingEnabled(bool enable)`
- `void setSupportedDragActions(Qt::DropActions actions)`
- `void sortItems(Qt::SortOrder order = Qt::AscendingOrder)`
- `Qt::DropActions supportedDragActions() const`
- `QListWidgetItem * takeItem(int row)`
- `QRect visualItemRect(const QListWidgetItem *item) const`

### 重实现的公有函数

- `virtual void setSelectionModel(QItemSelectionModel *selectionModel) override`

### 公有槽函数

- `void clear()`
- `void scrollToItem(const QListWidgetItem *item, QAbstractItemView::ScrollHint hint = EnsureVisible)`

### 信号

- `void currentItemChanged(QListWidgetItem *current, QListWidgetItem *previous)`
- `void currentRowChanged(int currentRow)`
- `void currentTextChanged(const QString &currentText)`
- `void itemActivated(QListWidgetItem *item)`
- `void itemChanged(QListWidgetItem *item)`
- `void itemClicked(QListWidgetItem *item)`
- `void itemDoubleClicked(QListWidgetItem *item)`
- `void itemEntered(QListWidgetItem *item)`
- `void itemPressed(QListWidgetItem *item)`
- `void itemSelectionChanged()`

### 保护函数

- `virtual bool dropMimeData(int index, const QMimeData *data, Qt::DropAction action)`
- `virtual QMimeData * mimeData(const QList<QListWidgetItem *> &items) const`
- `virtual QStringList mimeTypes() const`
- `virtual Qt::DropActions supportedDropActions() const`

### 重实现的保护函数

- `virtual void dropEvent(QDropEvent *event) override`
- `virtual bool event(QEvent *e) override`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 61 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[read-only] count : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QListWidget` 的状态/能力属性。通常通过 `count()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`count`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `currentRow : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QListWidget` 的配置属性。初始化或状态切换时通过 `setCurrentRow(...)` 设置，之后用 `currentRow()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`currentRow`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `sortingEnabled : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QListWidget` 的配置属性。初始化或状态切换时通过 `setSortingEnabled(...)` 设置，之后用 `sortingEnabled()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`sortingEnabled`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.10] supportedDragActions : Qt::DropActions`

**API 类别：** 属性说明

**中文解读：** 这是 `QListWidget` 的配置属性。初始化或状态切换时通过 `setDropActions(...)` 设置，之后用 `DropActions()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`Qt::DropActions`。
- 属性名：`supportedDragActions`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QListWidget::QListWidget(QWidget *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QListWidget` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QWidget *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QListWidget::~QListWidget()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QListWidget` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QListWidget::addItem(QListWidgetItem *item)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QListWidget` 添加依赖、数据或子对象的 API `addItem`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `item`：类型为 `QListWidgetItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QListWidget::addItem(const QString &label)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QListWidget` 添加依赖、数据或子对象的 API `addItem`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `label`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QListWidget::addItems(const QStringList &labels)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QListWidget` 添加依赖、数据或子对象的 API `addItems`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `labels`：类型为 `const QStringList &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QListWidget::clear()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `clear`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QListWidget::closePersistentEditor(QListWidgetItem *item)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `closePersistentEditor`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `item`：类型为 `QListWidgetItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QListWidgetItem *QListWidget::currentItem() const`

**API 类别：** 成员函数说明

**中文解读：** `QListWidget::currentItem` 用于计算、查询或取得与“当前、项目访问”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QListWidgetItem *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QListWidgetItem *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QListWidget::currentItemChanged(QListWidgetItem *current, QListWidgetItem *previous)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QListWidget` 发出的通知信号 `currentItemChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `current`：类型为 `QListWidgetItem *`。没有默认值，调用时必须提供。传入 `QListWidgetItem *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `previous`：类型为 `QListWidgetItem *`。没有默认值，调用时必须提供。传入 `QListWidgetItem *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QListWidget::currentRowChanged(int currentRow)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QListWidget` 发出的通知信号 `currentRowChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `currentRow`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QListWidget::currentTextChanged(const QString &currentText)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QListWidget` 发出的通知信号 `currentTextChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `currentText`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QListWidget::dropEvent(QDropEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QListWidget::dropEvent` 用于执行与“drop、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QDropEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] bool QListWidget::dropMimeData(int index, const QMimeData *data, Qt::DropAction action)`

**API 类别：** 成员函数说明

**中文解读：** `QListWidget::dropMimeData` 用于计算、查询或取得与“drop、Mime、数据访问”相关的操作。调用时要先确认当前状态和 `index`、`data`、`action` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `data`：类型为 `const QMimeData *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `action`：类型为 `Qt::DropAction`。没有默认值，调用时必须提供。传入 `Qt::DropAction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QListWidget::editItem(QListWidgetItem *item)`

**API 类别：** 成员函数说明

**中文解读：** `QListWidget::editItem` 用于执行与“edit、项目访问”相关的操作。调用时要先确认当前状态和 `item` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `item`：类型为 `QListWidgetItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] bool QListWidget::event(QEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QListWidget::event` 用于计算、查询或取得与“event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `e`：类型为 `QEvent *`。没有默认值，调用时必须提供。传入 `QEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QListWidgetItem *> QListWidget::findItems(const QString &text, Qt::MatchFlags flags) const`

**API 类别：** 成员函数说明

**中文解读：** `QListWidget::findItems` 用于计算、查询或取得与“查找、Items”相关的操作。调用时要先确认当前状态和 `text`、`flags` 的有效范围；返回类型是 `QList<QListWidgetItem *>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QListWidgetItem *>`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `flags`：类型为 `Qt::MatchFlags`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QModelIndex QListWidget::indexFromItem(const QListWidgetItem *item) const`

**API 类别：** 成员函数说明

**中文解读：** `QListWidget::indexFromItem` 用于计算、查询或取得与“索引、转换进入、项目访问”相关的操作。调用时要先确认当前状态和 `item` 的有效范围；返回类型是 `QModelIndex`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QModelIndex`。
- 参数 `item`：类型为 `const QListWidgetItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QListWidget::insertItem(int row, QListWidgetItem *item)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QListWidget` 添加依赖、数据或子对象的 API `insertItem`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `item`：类型为 `QListWidgetItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QListWidget::insertItem(int row, const QString &label)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QListWidget` 添加依赖、数据或子对象的 API `insertItem`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `label`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QListWidget::insertItems(int row, const QStringList &labels)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QListWidget` 添加依赖、数据或子对象的 API `insertItems`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `labels`：类型为 `const QStringList &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QListWidget::isPersistentEditorOpen(QListWidgetItem *item) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isPersistentEditorOpen`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `item`：类型为 `QListWidgetItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QListWidgetItem *QListWidget::item(int row) const`

**API 类别：** 成员函数说明

**中文解读：** `QListWidget::item` 用于计算、查询或取得与“项目访问”相关的操作。调用时要先确认当前状态和 `row` 的有效范围；返回类型是 `QListWidgetItem *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QListWidgetItem *`。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QListWidget::itemActivated(QListWidgetItem *item)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QListWidget` 发出的通知信号 `itemActivated`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `item`：类型为 `QListWidgetItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QListWidgetItem *QListWidget::itemAt(const QPoint &p) const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `itemAt`，用于取得 `QListWidget` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`QListWidgetItem *`。
- 参数 `p`：类型为 `const QPoint &`。没有默认值，调用时必须提供。传入 `const QPoint &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QListWidgetItem *QListWidget::itemAt(int x, int y) const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `itemAt`，用于取得 `QListWidget` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`QListWidgetItem *`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QListWidget::itemChanged(QListWidgetItem *item)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QListWidget` 发出的通知信号 `itemChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `item`：类型为 `QListWidgetItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QListWidget::itemClicked(QListWidgetItem *item)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QListWidget` 发出的通知信号 `itemClicked`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `item`：类型为 `QListWidgetItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QListWidget::itemDoubleClicked(QListWidgetItem *item)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QListWidget` 发出的通知信号 `itemDoubleClicked`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `item`：类型为 `QListWidgetItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QListWidget::itemEntered(QListWidgetItem *item)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QListWidget` 发出的通知信号 `itemEntered`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `item`：类型为 `QListWidgetItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QListWidgetItem *QListWidget::itemFromIndex(const QModelIndex &index) const`

**API 类别：** 成员函数说明

**中文解读：** `QListWidget::itemFromIndex` 用于计算、查询或取得与“项目访问、转换进入、索引”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `QListWidgetItem *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QListWidgetItem *`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QListWidget::itemPressed(QListWidgetItem *item)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QListWidget` 发出的通知信号 `itemPressed`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `item`：类型为 `QListWidgetItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QListWidget::itemSelectionChanged()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QListWidget` 发出的通知信号 `itemSelectionChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QWidget *QListWidget::itemWidget(QListWidgetItem *item) const`

**API 类别：** 成员函数说明

**中文解读：** `QListWidget::itemWidget` 用于计算、查询或取得与“项目访问、Widget”相关的操作。调用时要先确认当前状态和 `item` 的有效范围；返回类型是 `QWidget *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数 `item`：类型为 `QListWidgetItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QListWidgetItem *> QListWidget::items(const QMimeData *data) const`

**API 类别：** 成员函数说明

**中文解读：** `QListWidget::items` 用于计算、查询或取得与“items”相关的操作。调用时要先确认当前状态和 `data` 的有效范围；返回类型是 `QList<QListWidgetItem *>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QListWidgetItem *>`。
- 参数 `data`：类型为 `const QMimeData *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] QMimeData *QListWidget::mimeData(const QList<QListWidgetItem *> &items) const`

**API 类别：** 成员函数说明

**中文解读：** `QListWidget::mimeData` 用于计算、查询或取得与“mime、数据访问”相关的操作。调用时要先确认当前状态和 `items` 的有效范围；返回类型是 `QMimeData *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMimeData *`。
- 参数 `items`：类型为 `const QList<QListWidgetItem *> &`。没有默认值，调用时必须提供。传入 `const QList<QListWidgetItem *> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] QStringList QListWidget::mimeTypes() const`

**API 类别：** 成员函数说明

**中文解读：** `QListWidget::mimeTypes` 用于计算、查询或取得与“mime、Types”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QListWidget::openPersistentEditor(QListWidgetItem *item)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `openPersistentEditor`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数 `item`：类型为 `QListWidgetItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QListWidget::removeItemWidget(QListWidgetItem *item)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeItemWidget`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `item`：类型为 `QListWidgetItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QListWidget::row(const QListWidgetItem *item) const`

**API 类别：** 成员函数说明

**中文解读：** `QListWidget::row` 用于计算、查询或取得与“行”相关的操作。调用时要先确认当前状态和 `item` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `item`：类型为 `const QListWidgetItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QListWidget::scrollToItem(const QListWidgetItem *item, QAbstractItemView::ScrollHint hint = EnsureVisible)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `scrollToItem`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `item`：类型为 `const QListWidgetItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。
- 参数 `hint`：类型为 `QAbstractItemView::ScrollHint`。默认值为 `EnsureVisible`。传入 `QAbstractItemView::ScrollHint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QListWidgetItem *> QListWidget::selectedItems() const`

**API 类别：** 成员函数说明

**中文解读：** `QListWidget::selectedItems` 用于计算、查询或取得与“selected、Items”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QListWidgetItem *>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QListWidgetItem *>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QListWidget::setCurrentItem(QListWidgetItem *item)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setCurrentItem`。调用它会改变 `QListWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `item`：类型为 `QListWidgetItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QListWidget::setCurrentItem(QListWidgetItem *item, QItemSelectionModel::SelectionFlags command)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setCurrentItem`。调用它会改变 `QListWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `item`：类型为 `QListWidgetItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。
- 参数 `command`：类型为 `QItemSelectionModel::SelectionFlags`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QListWidget::setCurrentRow(int row, QItemSelectionModel::SelectionFlags command)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setCurrentRow`。调用它会改变 `QListWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `command`：类型为 `QItemSelectionModel::SelectionFlags`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QListWidget::setItemWidget(QListWidgetItem *item, QWidget *widget)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setItemWidget`。调用它会改变 `QListWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `item`：类型为 `QListWidgetItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。
- 参数 `widget`：类型为 `QWidget *`。没有默认值，调用时必须提供。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QListWidget::setSelectionModel(QItemSelectionModel *selectionModel)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSelectionModel`。调用它会改变 `QListWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `selectionModel`：类型为 `QItemSelectionModel *`。没有默认值，调用时必须提供。传入 `QItemSelectionModel *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QListWidget::sortItems(Qt::SortOrder order = Qt::AscendingOrder)`

**API 类别：** 成员函数说明

**中文解读：** `QListWidget::sortItems` 用于执行与“sort、Items”相关的操作。调用时要先确认当前状态和 `order` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `order`：类型为 `Qt::SortOrder`。默认值为 `Qt::AscendingOrder`。传入 `Qt::SortOrder` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] Qt::DropActions QListWidget::supportedDropActions() const`

**API 类别：** 成员函数说明

**中文解读：** `QListWidget::supportedDropActions` 用于计算、查询或取得与“supported、Drop、Actions”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::DropActions`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::DropActions`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QListWidgetItem *QListWidget::takeItem(int row)`

**API 类别：** 成员函数说明

**中文解读：** `QListWidget::takeItem` 用于计算、查询或取得与“取出、项目访问”相关的操作。调用时要先确认当前状态和 `row` 的有效范围；返回类型是 `QListWidgetItem *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QListWidgetItem *`。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRect QListWidget::visualItemRect(const QListWidgetItem *item) const`

**API 类别：** 成员函数说明

**中文解读：** `QListWidget::visualItemRect` 用于计算、查询或取得与“visual、项目访问、Rect”相关的操作。调用时要先确认当前状态和 `item` 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数 `item`：类型为 `const QListWidgetItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int count() const`

**API 类别：** 公有函数

**中文解读：** 这是尺寸/数量查询 API `count`，返回 `QListWidget` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int currentRow() const`

**API 类别：** 公有函数

**中文解读：** `QListWidget::currentRow` 用于计算、查询或取得与“当前、行”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool isSortingEnabled() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `isSortingEnabled`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setCurrentRow(int row)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setCurrentRow`。调用它会改变 `QListWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setSortingEnabled(bool enable)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setSortingEnabled`。调用它会改变 `QListWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setSupportedDragActions(Qt::DropActions actions)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setSupportedDragActions`。调用它会改变 `QListWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `actions`：类型为 `Qt::DropActions`。没有默认值，调用时必须提供。传入 `Qt::DropActions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::DropActions supportedDragActions() const`

**API 类别：** 公有函数

**中文解读：** `QListWidget::supportedDragActions` 用于计算、查询或取得与“supported、Drag、Actions”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::DropActions`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::DropActions`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

容器自己管理元素存储，容器销毁后由它提供的迭代器、引用和 data 指针通常失效。修改容器可能重新分配或 detach，不能把元素地址和迭代器当成长期句柄。

### 状态和错误边界

要区分空容器、容量、元素数量、查找失败和默认构造值。插入/删除可能改变索引和迭代器；关联容器还要考虑键唯一性、排序和查找复杂度。

### 线程边界

不同线程使用各自的容器副本通常安全；同一个容器一边读一边写仍需要同步，即使底层采用隐式共享也不会自动解决数据竞争。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QListWidget` 所属机制类型：Qt 容器与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
