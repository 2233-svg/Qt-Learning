# QRangeModel

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QRangeModel` 是 模型/视图协议 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QRangeModel` 是模型/视图体系中的数据模型类型，向视图提供索引、角色数据和结构变化通知。

**内部模型：** 视图不应该直接操作底层容器；它通过 QModelIndex 和 data roles 查询模型。模型必须准确维护索引有效性以及插入、删除、移动时的通知顺序。

**适用场景：** 需要把自定义数据接入 QListView、QTableView、QTreeView 或代理模型时使用。

**典型调用链：** 准备数据源 -> 实现/配置模型 -> 连接 view -> 通过 data/flags/setData 读写 -> 发出 dataChanged 或 begin/end 结构通知。

**先记住的坑：** 不要在 data() 中修改数据；不要返回过期索引；不要用全量 reset 代替精确结构通知，除非确实无法描述变化。

## 2. 依赖与对象关系

- 头文件：`#include <QRangeModel>`
- 继承自：QAbstractItemModel
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

视图不应该直接操作底层容器；它通过 QModelIndex 和 data roles 查询模型。模型必须准确维护索引有效性以及插入、删除、移动时的通知顺序。

### 状态、生命周期和线程

**生命周期：** 模型应比视图活得足够久，视图销毁时不会自动替业务容器释放资源。模型变化必须使用对应的 begin/end 协议或精确通知，不能只改容器后期待视图自行发现。取到的 QModelIndex 只在模型允许的生命周期内有效。

**状态与结果：** 区分当前索引、选择模型、编辑状态、数据角色和模型结构变化。`dataChanged` 表示已有项目的数据变化，行列插入/删除表示结构变化，`modelReset` 会让旧索引整体失效。

**线程与事件循环：** 模型通常在 GUI 线程被视图访问。后台线程不要直接修改正在显示的模型；应在正确线程汇总数据，再通过通知协议更新，或使用线程安全的数据交换层。

## 3. 直接使用

需要把自定义数据接入 QListView、QTableView、QTreeView 或代理模型时使用。 使用时通常按这个过程组织：准备数据源 -> 实现/配置模型 -> 连接 view -> 通过 data/flags/setData 读写 -> 发出 dataChanged 或 begin/end 结构通知。

```cpp
// 视图通过 QModelIndex 和 role 查询模型。
const QVariant value = model->data(index, Qt::DisplayRole);
// 数据变化时由模型发出 dataChanged 或 begin/end 结构通知。
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `(since 6.11) struct ItemAccess`
- `(since 6.10) struct RowOptions`
- `(since 6.11) enum class AutoConnectPolicy { None, Full, OnRead }`
- `enum class RowCategory { Default, MultiRoleItem }`

### 属性

- `(since 6.11) autoConnectPolicy : AutoConnectPolicy`
- `roleNames : QHash<int, QByteArray>`

### 公有函数

- `QRangeModel(Range &&range, QObject *parent = nullptr)`
- `QRangeModel(Range &&range, Protocol &&protocol, QObject *parent = nullptr)`
- `virtual ~QRangeModel() override`
- `QRangeModel::AutoConnectPolicy autoConnectPolicy() const`
- `void resetRoleNames()`
- `void setAutoConnectPolicy(QRangeModel::AutoConnectPolicy policy)`
- `void setRoleNames(const QHash<int, QByteArray> &names)`

### 重实现的公有函数

- `virtual QModelIndex buddy(const QModelIndex &index) const override`
- `virtual bool canDropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent) const override`
- `virtual bool canFetchMore(const QModelIndex &parent) const override`
- `virtual bool clearItemData(const QModelIndex &index) override`
- `virtual int columnCount(const QModelIndex &parent = {}) const override`
- `virtual QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override`
- `virtual bool dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent) override`
- `virtual void fetchMore(const QModelIndex &parent) override`
- `virtual Qt::ItemFlags flags(const QModelIndex &index) const override`
- `virtual bool hasChildren(const QModelIndex &parent = QModelIndex()) const override`
- `virtual QVariant headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const override`
- `virtual QModelIndex index(int row, int column, const QModelIndex &parent = {}) const override`
- `virtual bool insertColumns(int column, int count, const QModelIndex &parent = {}) override`
- `virtual bool insertRows(int row, int count, const QModelIndex &parent = {}) override`
- `virtual QMap<int, QVariant> itemData(const QModelIndex &index) const override`
- `virtual QModelIndexList match(const QModelIndex &start, int role, const QVariant &value, int hits, Qt::MatchFlags flags) const override`
- `virtual QMimeData * mimeData(const QModelIndexList &indexes) const override`
- `virtual QStringList mimeTypes() const override`
- `virtual bool moveColumns(const QModelIndex &sourceParent, int sourceColumn, int count, const QModelIndex &destinationParent, int destinationColumn) override`
- `virtual bool moveRows(const QModelIndex &sourceParent, int sourceRow, int count, const QModelIndex &destinationParent, int destinationRow) override`
- `virtual void multiData(const QModelIndex &index, QModelRoleDataSpan roleDataSpan) const override`
- `virtual QModelIndex parent(const QModelIndex &child) const override`
- `virtual bool removeColumns(int column, int count, const QModelIndex &parent = {}) override`
- `virtual bool removeRows(int row, int count, const QModelIndex &parent = {}) override`
- `virtual QHash<int, QByteArray> roleNames() const override`
- `virtual int rowCount(const QModelIndex &parent = {}) const override`
- `virtual bool setData(const QModelIndex &index, const QVariant &data, int role = Qt::EditRole) override`
- `virtual bool setHeaderData(int section, Qt::Orientation orientation, const QVariant &data, int role = Qt::EditRole) override`
- `virtual bool setItemData(const QModelIndex &index, const QMap<int, QVariant> &data) override`
- `virtual QModelIndex sibling(int row, int column, const QModelIndex &index) const override`
- `virtual void sort(int column, Qt::SortOrder order = Qt::AscendingOrder) override`
- `virtual QSize span(const QModelIndex &index) const override`
- `virtual Qt::DropActions supportedDragActions() const override`
- `virtual Qt::DropActions supportedDropActions() const override`

### 信号

- `void autoConnectPolicyChanged(QRangeModel::AutoConnectPolicy policy)`
- `void roleNamesChanged()`

### 重实现的保护函数

- `virtual bool event(QEvent *event) override`
- `virtual bool eventFilter(QObject *object, QEvent *event) override`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 52 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[since 6.11] enum class QRangeModel::AutoConnectPolicy`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRangeModel` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:AutoConnectPolicy`。
- 属性名：`QRangeModel`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum class QRangeModel::RowCategory`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRangeModel` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:RowCategory`。
- 属性名：`QRangeModel`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.11] autoConnectPolicy : AutoConnectPolicy`

**API 类别：** 属性说明

**中文解读：** 这是 `QRangeModel` 的配置属性。初始化或状态切换时通过 `setAutoConnectPolicy(...)` 设置，之后用 `autoConnectPolicy()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`AutoConnectPolicy`。
- 属性名：`autoConnectPolicy`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `roleNames : QHash<int, QByteArray>`

**API 类别：** 属性说明

**中文解读：** 这是 `QRangeModel` 的配置属性。初始化或状态切换时通过 `setRoleNames(...)` 设置，之后用 `roleNames()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QHash<int, QByteArray>`。
- 属性名：`roleNames`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] template < typename Range, typename Protocol, int = true > QRangeModel::QRangeModel(Range &&range, Protocol &&protocol, QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRangeModel` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `range`：类型为 `Range &&`。没有默认值，调用时必须提供。传入 `Range &&` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `protocol`：类型为 `Protocol &&`。没有默认值，调用时必须提供。传入 `Protocol &&` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual noexcept] QRangeModel::~QRangeModel()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRangeModel` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QModelIndex QRangeModel::buddy(const QModelIndex &index) const`

**API 类别：** 成员函数说明

**中文解读：** `QRangeModel::buddy` 用于计算、查询或取得与“buddy”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `QModelIndex`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QModelIndex`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QRangeModel::canDropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `canDropMimeData`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `data`：类型为 `const QMimeData *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `action`：类型为 `Qt::DropAction`。没有默认值，调用时必须提供。传入 `Qt::DropAction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `column`：类型为 `int`。没有默认值，调用时必须提供。列号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `parent`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QRangeModel::canFetchMore(const QModelIndex &parent) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `canFetchMore`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `parent`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QRangeModel::clearItemData(const QModelIndex &index)`

**API 类别：** 成员函数说明

**中文解读：** `QRangeModel::clearItemData` 用于计算、查询或取得与“清空、项目访问、数据访问”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] int QRangeModel::columnCount(const QModelIndex &parent = {}) const`

**API 类别：** 成员函数说明

**中文解读：** `QRangeModel::columnCount` 用于计算、查询或取得与“列、数量统计”相关的操作。调用时要先确认当前状态和 `parent` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `parent`：类型为 `const QModelIndex &`。默认值为 `{}`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QVariant QRangeModel::data(const QModelIndex &index, int role = Qt::DisplayRole) const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `data`，用于取得 `QRangeModel` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `role`：类型为 `int`。默认值为 `Qt::DisplayRole`。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。

**正确调用组合：** 通常与 role、QModelIndex 有关；数据变化后发 `dataChanged`，不要在 data() 中修改模型。

### `[override virtual] bool QRangeModel::dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent)`

**API 类别：** 成员函数说明

**中文解读：** `QRangeModel::dropMimeData` 用于计算、查询或取得与“drop、Mime、数据访问”相关的操作。调用时要先确认当前状态和 `data`、`action`、`row`、`column`、`parent` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `data`：类型为 `const QMimeData *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `action`：类型为 `Qt::DropAction`。没有默认值，调用时必须提供。传入 `Qt::DropAction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `column`：类型为 `int`。没有默认值，调用时必须提供。列号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `parent`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] bool QRangeModel::event(QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QRangeModel::event` 用于计算、查询或取得与“event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] bool QRangeModel::eventFilter(QObject *object, QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QRangeModel::eventFilter` 用于计算、查询或取得与“event、Filter”相关的操作。调用时要先确认当前状态和 `object`、`event` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `object`：类型为 `QObject *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QRangeModel::fetchMore(const QModelIndex &parent)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRangeModel` 的核心操作 `fetchMore`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `parent`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] Qt::ItemFlags QRangeModel::flags(const QModelIndex &index) const`

**API 类别：** 成员函数说明

**中文解读：** `QRangeModel::flags` 用于计算、查询或取得与“标志”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `Qt::ItemFlags`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::ItemFlags`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QRangeModel::hasChildren(const QModelIndex &parent = QModelIndex()) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasChildren`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `parent`：类型为 `const QModelIndex &`。默认值为 `QModelIndex()`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QVariant QRangeModel::headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const`

**API 类别：** 成员函数说明

**中文解读：** `QRangeModel::headerData` 用于计算、查询或取得与“header、数据访问”相关的操作。调用时要先确认当前状态和 `section`、`orientation`、`role` 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `section`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `orientation`：类型为 `Qt::Orientation`。没有默认值，调用时必须提供。传入 `Qt::Orientation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `role`：类型为 `int`。默认值为 `Qt::DisplayRole`。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QModelIndex QRangeModel::index(int row, int column, const QModelIndex &parent = {}) const`

**API 类别：** 成员函数说明

**中文解读：** `QRangeModel::index` 用于计算、查询或取得与“索引”相关的操作。调用时要先确认当前状态和 `row`、`column`、`parent` 的有效范围；返回类型是 `QModelIndex`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QModelIndex`。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `column`：类型为 `int`。没有默认值，调用时必须提供。列号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `parent`：类型为 `const QModelIndex &`。默认值为 `{}`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QRangeModel::insertColumns(int column, int count, const QModelIndex &parent = {})`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QRangeModel` 添加依赖、数据或子对象的 API `insertColumns`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `column`：类型为 `int`。没有默认值，调用时必须提供。列号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `count`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `parent`：类型为 `const QModelIndex &`。默认值为 `{}`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QRangeModel::insertRows(int row, int count, const QModelIndex &parent = {})`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QRangeModel` 添加依赖、数据或子对象的 API `insertRows`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `count`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `parent`：类型为 `const QModelIndex &`。默认值为 `{}`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QMap<int, QVariant> QRangeModel::itemData(const QModelIndex &index) const`

**API 类别：** 成员函数说明

**中文解读：** `QRangeModel::itemData` 用于计算、查询或取得与“项目访问、数据访问”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `QMap<int, QVariant>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMap<int, QVariant>`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QModelIndexList QRangeModel::match(const QModelIndex &start, int role, const QVariant &value, int hits, Qt::MatchFlags flags) const`

**API 类别：** 成员函数说明

**中文解读：** `QRangeModel::match` 用于计算、查询或取得与“匹配”相关的操作。调用时要先确认当前状态和 `start`、`role`、`value`、`hits`、`flags` 的有效范围；返回类型是 `QModelIndexList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QModelIndexList`。
- 参数 `start`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。模型索引。调用前确认索引有效、属于正确模型，并注意模型结构变化后它可能失效。
- 参数 `role`：类型为 `int`。没有默认值，调用时必须提供。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。
- 参数 `value`：类型为 `const QVariant &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。
- 参数 `hits`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `Qt::MatchFlags`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QMimeData *QRangeModel::mimeData(const QModelIndexList &indexes) const`

**API 类别：** 成员函数说明

**中文解读：** `QRangeModel::mimeData` 用于计算、查询或取得与“mime、数据访问”相关的操作。调用时要先确认当前状态和 `indexes` 的有效范围；返回类型是 `QMimeData *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMimeData *`。
- 参数 `indexes`：类型为 `const QModelIndexList &`。没有默认值，调用时必须提供。模型索引。调用前确认索引有效、属于正确模型，并注意模型结构变化后它可能失效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QStringList QRangeModel::mimeTypes() const`

**API 类别：** 成员函数说明

**中文解读：** `QRangeModel::mimeTypes` 用于计算、查询或取得与“mime、Types”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QRangeModel::moveColumns(const QModelIndex &sourceParent, int sourceColumn, int count, const QModelIndex &destinationParent, int destinationColumn)`

**API 类别：** 成员函数说明

**中文解读：** `QRangeModel::moveColumns` 用于计算、查询或取得与“移动、列”相关的操作。调用时要先确认当前状态和 `sourceParent`、`sourceColumn`、`count`、`destinationParent`、`destinationColumn` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `sourceParent`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `sourceColumn`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `destinationParent`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `destinationColumn`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QRangeModel::moveRows(const QModelIndex &sourceParent, int sourceRow, int count, const QModelIndex &destinationParent, int destinationRow)`

**API 类别：** 成员函数说明

**中文解读：** `QRangeModel::moveRows` 用于计算、查询或取得与“移动、行”相关的操作。调用时要先确认当前状态和 `sourceParent`、`sourceRow`、`count`、`destinationParent`、`destinationRow` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `sourceParent`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `sourceRow`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `destinationParent`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `destinationRow`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QRangeModel::multiData(const QModelIndex &index, QModelRoleDataSpan roleDataSpan) const`

**API 类别：** 成员函数说明

**中文解读：** `QRangeModel::multiData` 用于执行与“multi、数据访问”相关的操作。调用时要先确认当前状态和 `index`、`roleDataSpan` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `roleDataSpan`：类型为 `QModelRoleDataSpan`。没有默认值，调用时必须提供。传入 `QModelRoleDataSpan` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QModelIndex QRangeModel::parent(const QModelIndex &child) const`

**API 类别：** 成员函数说明

**中文解读：** `QRangeModel::parent` 用于计算、查询或取得与“父对象”相关的操作。调用时要先确认当前状态和 `child` 的有效范围；返回类型是 `QModelIndex`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QModelIndex`。
- 参数 `child`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。子对象或子节点；要确认它是否由父对象接管，以及调用后原指针是否仍有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QRangeModel::removeColumns(int column, int count, const QModelIndex &parent = {})`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeColumns`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`bool`。
- 参数 `column`：类型为 `int`。没有默认值，调用时必须提供。列号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `count`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `parent`：类型为 `const QModelIndex &`。默认值为 `{}`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QRangeModel::removeRows(int row, int count, const QModelIndex &parent = {})`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeRows`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`bool`。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `count`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `parent`：类型为 `const QModelIndex &`。默认值为 `{}`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected slot] void QRangeModel::resetInternalData()`

**API 类别：** 成员函数说明

**中文解读：** `QRangeModel::resetInternalData` 用于执行与“重置、Internal、数据访问”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QHash<int, QByteArray> QRangeModel::roleNames() const`

**API 类别：** 成员函数说明

**中文解读：** `QRangeModel::roleNames` 用于计算、查询或取得与“角色、Names”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QHash<int, QByteArray>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QHash<int, QByteArray>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] int QRangeModel::rowCount(const QModelIndex &parent = {}) const`

**API 类别：** 成员函数说明

**中文解读：** `QRangeModel::rowCount` 用于计算、查询或取得与“行、数量统计”相关的操作。调用时要先确认当前状态和 `parent` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `parent`：类型为 `const QModelIndex &`。默认值为 `{}`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QRangeModel::setData(const QModelIndex &index, const QVariant &data, int role = Qt::EditRole)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setData`。调用它会改变 `QRangeModel` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`bool`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `data`：类型为 `const QVariant &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `role`：类型为 `int`。默认值为 `Qt::EditRole`。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。

**正确调用组合：** 成功修改后要发出对应 dataChanged；同时确认 flags 包含可编辑能力。

### `[override virtual] bool QRangeModel::setHeaderData(int section, Qt::Orientation orientation, const QVariant &data, int role = Qt::EditRole)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setHeaderData`。调用它会改变 `QRangeModel` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`bool`。
- 参数 `section`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `orientation`：类型为 `Qt::Orientation`。没有默认值，调用时必须提供。传入 `Qt::Orientation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `data`：类型为 `const QVariant &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `role`：类型为 `int`。默认值为 `Qt::EditRole`。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QRangeModel::setItemData(const QModelIndex &index, const QMap<int, QVariant> &data)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setItemData`。调用它会改变 `QRangeModel` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`bool`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `data`：类型为 `const QMap<int, QVariant> &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QModelIndex QRangeModel::sibling(int row, int column, const QModelIndex &index) const`

**API 类别：** 成员函数说明

**中文解读：** `QRangeModel::sibling` 用于计算、查询或取得与“sibling”相关的操作。调用时要先确认当前状态和 `row`、`column`、`index` 的有效范围；返回类型是 `QModelIndex`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QModelIndex`。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `column`：类型为 `int`。没有默认值，调用时必须提供。列号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QRangeModel::sort(int column, Qt::SortOrder order = Qt::AscendingOrder)`

**API 类别：** 成员函数说明

**中文解读：** `QRangeModel::sort` 用于执行与“sort”相关的操作。调用时要先确认当前状态和 `column`、`order` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `column`：类型为 `int`。没有默认值，调用时必须提供。列号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `order`：类型为 `Qt::SortOrder`。默认值为 `Qt::AscendingOrder`。传入 `Qt::SortOrder` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QSize QRangeModel::span(const QModelIndex &index) const`

**API 类别：** 成员函数说明

**中文解读：** `QRangeModel::span` 用于计算、查询或取得与“span”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] Qt::DropActions QRangeModel::supportedDragActions() const`

**API 类别：** 成员函数说明

**中文解读：** `QRangeModel::supportedDragActions` 用于计算、查询或取得与“supported、Drag、Actions”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::DropActions`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::DropActions`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] Qt::DropActions QRangeModel::supportedDropActions() const`

**API 类别：** 成员函数说明

**中文解读：** `QRangeModel::supportedDropActions` 用于计算、查询或取得与“supported、Drop、Actions”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::DropActions`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::DropActions`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.11) struct ItemAccess`

**API 类别：** 公有类型

**中文解读：** 这是 `QRangeModel` 的 `项目访问、Access` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.10) struct RowOptions`

**API 类别：** 公有类型

**中文解读：** 这是 `QRangeModel` 的 `行、Options` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRangeModel(Range &&range, QObject *parent = nullptr)`

**API 类别：** 公有函数

**中文解读：** 这是 `QRangeModel` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `range`：类型为 `Range &&`。没有默认值，调用时必须提供。传入 `Range &&` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRangeModel::AutoConnectPolicy autoConnectPolicy() const`

**API 类别：** 公有函数

**中文解读：** `QRangeModel::autoConnectPolicy` 用于计算、查询或取得与“auto、连接、Policy”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRangeModel::AutoConnectPolicy`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRangeModel::AutoConnectPolicy`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void resetRoleNames()`

**API 类别：** 公有函数

**中文解读：** `QRangeModel::resetRoleNames` 用于执行与“重置、角色、Names”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setAutoConnectPolicy(QRangeModel::AutoConnectPolicy policy)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setAutoConnectPolicy`。调用它会改变 `QRangeModel` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `policy`：类型为 `QRangeModel::AutoConnectPolicy`。没有默认值，调用时必须提供。传入 `QRangeModel::AutoConnectPolicy` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setRoleNames(const QHash<int, QByteArray> &names)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setRoleNames`。调用它会改变 `QRangeModel` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `names`：类型为 `const QHash<int, QByteArray> &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void autoConnectPolicyChanged(QRangeModel::AutoConnectPolicy policy)`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `autoConnectPolicyChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `policy`：类型为 `QRangeModel::AutoConnectPolicy`。没有默认值，调用时必须提供。传入 `QRangeModel::AutoConnectPolicy` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void roleNamesChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `roleNamesChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

模型应比视图活得足够久，视图销毁时不会自动替业务容器释放资源。模型变化必须使用对应的 begin/end 协议或精确通知，不能只改容器后期待视图自行发现。取到的 QModelIndex 只在模型允许的生命周期内有效。

### 状态和错误边界

区分当前索引、选择模型、编辑状态、数据角色和模型结构变化。`dataChanged` 表示已有项目的数据变化，行列插入/删除表示结构变化，`modelReset` 会让旧索引整体失效。

### 线程边界

模型通常在 GUI 线程被视图访问。后台线程不要直接修改正在显示的模型；应在正确线程汇总数据，再通过通知协议更新，或使用线程安全的数据交换层。

### 最容易出现的错误

不要在 data() 中修改数据；不要返回过期索引；不要用全量 reset 代替精确结构通知，除非确实无法描述变化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QRangeModel` 所属机制类型：模型/视图协议。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
