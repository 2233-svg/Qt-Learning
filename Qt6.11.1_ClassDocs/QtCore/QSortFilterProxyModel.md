# QSortFilterProxyModel

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QSortFilterProxyModel` 是 模型/视图协议 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QSortFilterProxyModel` 是模型/视图体系中的数据模型类型，向视图提供索引、角色数据和结构变化通知。

**内部模型：** 视图不应该直接操作底层容器；它通过 QModelIndex 和 data roles 查询模型。模型必须准确维护索引有效性以及插入、删除、移动时的通知顺序。

**适用场景：** 需要把自定义数据接入 QListView、QTableView、QTreeView 或代理模型时使用。

**典型调用链：** 准备数据源 -> 实现/配置模型 -> 连接 view -> 通过 data/flags/setData 读写 -> 发出 dataChanged 或 begin/end 结构通知。

**先记住的坑：** 不要在 data() 中修改数据；不要返回过期索引；不要用全量 reset 代替精确结构通知，除非确实无法描述变化。

## 2. 依赖与对象关系

- 头文件：`#include <QSortFilterProxyModel>`
- 继承自：QAbstractProxyModel
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

- `(since 6.10) enum class Direction { Rows, Columns, Both }`
- `flags Directions`

### 属性

- `(since 6.0) autoAcceptChildRows : bool`
- `dynamicSortFilter : bool`
- `filterCaseSensitivity : Qt::CaseSensitivity`
- `filterKeyColumn : int`
- `filterRegularExpression : QRegularExpression`
- `filterRole : int`
- `isSortLocaleAware : bool`
- `recursiveFilteringEnabled : bool`
- `sortCaseSensitivity : Qt::CaseSensitivity`
- `sortRole : int`

### 公有函数

- `QSortFilterProxyModel(QObject *parent = nullptr)`
- `virtual ~QSortFilterProxyModel()`
- `bool autoAcceptChildRows() const`
- `QBindable<bool> bindableAutoAcceptChildRows()`
- `QBindable<bool> bindableDynamicSortFilter()`
- `QBindable<Qt::CaseSensitivity> bindableFilterCaseSensitivity()`
- `QBindable<int> bindableFilterKeyColumn()`
- `QBindable<QRegularExpression> bindableFilterRegularExpression()`
- `QBindable<int> bindableFilterRole()`
- `QBindable<bool> bindableIsSortLocaleAware()`
- `QBindable<bool> bindableRecursiveFilteringEnabled()`
- `QBindable<Qt::CaseSensitivity> bindableSortCaseSensitivity()`
- `QBindable<int> bindableSortRole()`
- `bool dynamicSortFilter() const`
- `Qt::CaseSensitivity filterCaseSensitivity() const`
- `int filterKeyColumn() const`
- `QRegularExpression filterRegularExpression() const`
- `int filterRole() const`
- `bool isRecursiveFilteringEnabled() const`
- `bool isSortLocaleAware() const`
- `void setAutoAcceptChildRows(bool accept)`
- `void setDynamicSortFilter(bool enable)`
- `void setFilterCaseSensitivity(Qt::CaseSensitivity cs)`
- `void setFilterKeyColumn(int column)`
- `void setFilterRole(int role)`
- `void setRecursiveFilteringEnabled(bool recursive)`
- `void setSortCaseSensitivity(Qt::CaseSensitivity cs)`
- `void setSortLocaleAware(bool on)`
- `void setSortRole(int role)`
- `Qt::CaseSensitivity sortCaseSensitivity() const`
- `int sortColumn() const`
- `Qt::SortOrder sortOrder() const`
- `int sortRole() const`

### 重实现的公有函数

- `virtual QModelIndex buddy(const QModelIndex &index) const override`
- `virtual bool canFetchMore(const QModelIndex &parent) const override`
- `virtual int columnCount(const QModelIndex &parent = QModelIndex()) const override`
- `virtual QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override`
- `virtual bool dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent) override`
- `virtual void fetchMore(const QModelIndex &parent) override`
- `virtual Qt::ItemFlags flags(const QModelIndex &index) const override`
- `virtual bool hasChildren(const QModelIndex &parent = QModelIndex()) const override`
- `virtual QVariant headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const override`
- `virtual QModelIndex index(int row, int column, const QModelIndex &parent = QModelIndex()) const override`
- `virtual bool insertColumns(int column, int count, const QModelIndex &parent = QModelIndex()) override`
- `virtual bool insertRows(int row, int count, const QModelIndex &parent = QModelIndex()) override`
- `virtual QModelIndex mapFromSource(const QModelIndex &sourceIndex) const override`
- `virtual QItemSelection mapSelectionFromSource(const QItemSelection &sourceSelection) const override`
- `virtual QItemSelection mapSelectionToSource(const QItemSelection &proxySelection) const override`
- `virtual QModelIndex mapToSource(const QModelIndex &proxyIndex) const override`
- `virtual QModelIndexList match(const QModelIndex &start, int role, const QVariant &value, int hits = 1, Qt::MatchFlags flags = Qt::MatchFlags(Qt::MatchStartsWith|Qt::MatchWrap)) const override`
- `virtual QMimeData * mimeData(const QModelIndexList &indexes) const override`
- `virtual QStringList mimeTypes() const override`
- `virtual QModelIndex parent(const QModelIndex &child) const override`
- `virtual bool removeColumns(int column, int count, const QModelIndex &parent = QModelIndex()) override`
- `virtual bool removeRows(int row, int count, const QModelIndex &parent = QModelIndex()) override`
- `virtual int rowCount(const QModelIndex &parent = QModelIndex()) const override`
- `virtual bool setData(const QModelIndex &index, const QVariant &value, int role = Qt::EditRole) override`
- `virtual bool setHeaderData(int section, Qt::Orientation orientation, const QVariant &value, int role = Qt::EditRole) override`
- `virtual void setSourceModel(QAbstractItemModel *sourceModel) override`
- `virtual QModelIndex sibling(int row, int column, const QModelIndex &idx) const override`
- `virtual void sort(int column, Qt::SortOrder order = Qt::AscendingOrder) override`
- `virtual QSize span(const QModelIndex &index) const override`
- `virtual Qt::DropActions supportedDropActions() const override`

### 公有槽函数

- `void invalidate()`
- `void setFilterFixedString(const QString &pattern)`
- `void setFilterRegularExpression(const QString &pattern)`
- `void setFilterRegularExpression(const QRegularExpression &regularExpression)`
- `void setFilterWildcard(const QString &pattern)`

### 信号

- `(since 6.0) void autoAcceptChildRowsChanged(bool autoAcceptChildRows)`
- `void filterCaseSensitivityChanged(Qt::CaseSensitivity filterCaseSensitivity)`
- `void filterRoleChanged(int filterRole)`
- `void recursiveFilteringEnabledChanged(bool recursiveFilteringEnabled)`
- `void sortCaseSensitivityChanged(Qt::CaseSensitivity sortCaseSensitivity)`
- `void sortLocaleAwareChanged(bool sortLocaleAware)`
- `void sortRoleChanged(int sortRole)`

### 保护函数

- `(since 6.9) void beginFilterChange()`
- `(since 6.10) void endFilterChange(QSortFilterProxyModel::Directions directions = Direction::Both)`
- `virtual bool filterAcceptsColumn(int source_column, const QModelIndex &source_parent) const`
- `virtual bool filterAcceptsRow(int source_row, const QModelIndex &source_parent) const`
- `(since 6.0, until 6.13) void invalidateColumnsFilter()`
- `(until 6.13) void invalidateFilter()`
- `(since 6.0, until 6.13) void invalidateRowsFilter()`
- `virtual bool lessThan(const QModelIndex &source_left, const QModelIndex &source_right) const`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 96 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[since 6.10] enum class QSortFilterProxyModel::Directionflags QSortFilterProxyModel::Directions`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QSortFilterProxyModel` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Directionflags QSortFilterProxyModel::Directions`。
- 属性名：`QSortFilterProxyModel`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[bindable, since 6.0] autoAcceptChildRows : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QSortFilterProxyModel` 的配置属性。初始化或状态切换时通过 `setAutoAcceptChildRows(...)` 设置，之后用 `autoAcceptChildRows()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`autoAcceptChildRows`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[bindable] dynamicSortFilter : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QSortFilterProxyModel` 的配置属性。初始化或状态切换时通过 `setDynamicSortFilter(...)` 设置，之后用 `dynamicSortFilter()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`dynamicSortFilter`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[bindable] filterCaseSensitivity : Qt::CaseSensitivity`

**API 类别：** 属性说明

**中文解读：** 这是 `QSortFilterProxyModel` 的配置属性。初始化或状态切换时通过 `setCaseSensitivity(...)` 设置，之后用 `CaseSensitivity()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`Qt::CaseSensitivity`。
- 属性名：`filterCaseSensitivity`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[bindable] filterKeyColumn : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QSortFilterProxyModel` 的配置属性。初始化或状态切换时通过 `setFilterKeyColumn(...)` 设置，之后用 `filterKeyColumn()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`filterKeyColumn`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[bindable] filterRegularExpression : QRegularExpression`

**API 类别：** 属性说明

**中文解读：** 这是 `QSortFilterProxyModel` 的配置属性。初始化或状态切换时通过 `setFilterRegularExpression(...)` 设置，之后用 `filterRegularExpression()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QRegularExpression`。
- 属性名：`filterRegularExpression`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[bindable] filterRole : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QSortFilterProxyModel` 的配置属性。初始化或状态切换时通过 `setFilterRole(...)` 设置，之后用 `filterRole()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`filterRole`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[bindable] isSortLocaleAware : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QSortFilterProxyModel` 的状态/能力属性。通常通过 `isSortLocaleAware()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`isSortLocaleAware`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[bindable] recursiveFilteringEnabled : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QSortFilterProxyModel` 的配置属性。初始化或状态切换时通过 `setRecursiveFilteringEnabled(...)` 设置，之后用 `recursiveFilteringEnabled()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`recursiveFilteringEnabled`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[bindable] sortCaseSensitivity : Qt::CaseSensitivity`

**API 类别：** 属性说明

**中文解读：** 这是 `QSortFilterProxyModel` 的配置属性。初始化或状态切换时通过 `setCaseSensitivity(...)` 设置，之后用 `CaseSensitivity()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`Qt::CaseSensitivity`。
- 属性名：`sortCaseSensitivity`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[bindable] sortRole : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QSortFilterProxyModel` 的配置属性。初始化或状态切换时通过 `setSortRole(...)` 设置，之后用 `sortRole()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`sortRole`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QSortFilterProxyModel::QSortFilterProxyModel(QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSortFilterProxyModel` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QSortFilterProxyModel::~QSortFilterProxyModel()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSortFilterProxyModel` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal, since 6.0] void QSortFilterProxyModel::autoAcceptChildRowsChanged(bool autoAcceptChildRows)`

**API 类别：** 成员函数说明

**中文解读：** 这是状态变化通知 `autoAcceptChildRowsChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `autoAcceptChildRows`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected, since 6.9] void QSortFilterProxyModel::beginFilterChange()`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `beginFilterChange`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QModelIndex QSortFilterProxyModel::buddy(const QModelIndex &index) const`

**API 类别：** 成员函数说明

**中文解读：** `QSortFilterProxyModel::buddy` 用于计算、查询或取得与“buddy”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `QModelIndex`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QModelIndex`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QSortFilterProxyModel::canFetchMore(const QModelIndex &parent) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `canFetchMore`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `parent`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] int QSortFilterProxyModel::columnCount(const QModelIndex &parent = QModelIndex()) const`

**API 类别：** 成员函数说明

**中文解读：** `QSortFilterProxyModel::columnCount` 用于计算、查询或取得与“列、数量统计”相关的操作。调用时要先确认当前状态和 `parent` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `parent`：类型为 `const QModelIndex &`。默认值为 `QModelIndex()`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QVariant QSortFilterProxyModel::data(const QModelIndex &index, int role = Qt::DisplayRole) const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `data`，用于取得 `QSortFilterProxyModel` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `role`：类型为 `int`。默认值为 `Qt::DisplayRole`。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。

**正确调用组合：** 通常与 role、QModelIndex 有关；数据变化后发 `dataChanged`，不要在 data() 中修改模型。

### `[override virtual] bool QSortFilterProxyModel::dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent)`

**API 类别：** 成员函数说明

**中文解读：** `QSortFilterProxyModel::dropMimeData` 用于计算、查询或取得与“drop、Mime、数据访问”相关的操作。调用时要先确认当前状态和 `data`、`action`、`row`、`column`、`parent` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `data`：类型为 `const QMimeData *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `action`：类型为 `Qt::DropAction`。没有默认值，调用时必须提供。传入 `Qt::DropAction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `column`：类型为 `int`。没有默认值，调用时必须提供。列号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `parent`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected, since 6.10] void QSortFilterProxyModel::endFilterChange(QSortFilterProxyModel::Directions directions = Direction::Both)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `endFilterChange`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `directions`：类型为 `QSortFilterProxyModel::Directions`。默认值为 `Direction::Both`。传入 `QSortFilterProxyModel::Directions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QSortFilterProxyModel::fetchMore(const QModelIndex &parent)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSortFilterProxyModel` 的核心操作 `fetchMore`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `parent`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] bool QSortFilterProxyModel::filterAcceptsColumn(int source_column, const QModelIndex &source_parent) const`

**API 类别：** 成员函数说明

**中文解读：** `QSortFilterProxyModel::filterAcceptsColumn` 用于计算、查询或取得与“filter、Accepts、列”相关的操作。调用时要先确认当前状态和 `source_column`、`source_parent` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `source_column`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `source_parent`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] bool QSortFilterProxyModel::filterAcceptsRow(int source_row, const QModelIndex &source_parent) const`

**API 类别：** 成员函数说明

**中文解读：** `QSortFilterProxyModel::filterAcceptsRow` 用于计算、查询或取得与“filter、Accepts、行”相关的操作。调用时要先确认当前状态和 `source_row`、`source_parent` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `source_row`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `source_parent`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QSortFilterProxyModel::filterCaseSensitivityChanged(Qt::CaseSensitivity filterCaseSensitivity)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSortFilterProxyModel` 发出的通知信号 `filterCaseSensitivityChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `filterCaseSensitivity`：类型为 `Qt::CaseSensitivity`。没有默认值，调用时必须提供。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QSortFilterProxyModel::filterRoleChanged(int filterRole)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSortFilterProxyModel` 发出的通知信号 `filterRoleChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `filterRole`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] Qt::ItemFlags QSortFilterProxyModel::flags(const QModelIndex &index) const`

**API 类别：** 成员函数说明

**中文解读：** `QSortFilterProxyModel::flags` 用于计算、查询或取得与“标志”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `Qt::ItemFlags`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::ItemFlags`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QSortFilterProxyModel::hasChildren(const QModelIndex &parent = QModelIndex()) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasChildren`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `parent`：类型为 `const QModelIndex &`。默认值为 `QModelIndex()`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QVariant QSortFilterProxyModel::headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const`

**API 类别：** 成员函数说明

**中文解读：** `QSortFilterProxyModel::headerData` 用于计算、查询或取得与“header、数据访问”相关的操作。调用时要先确认当前状态和 `section`、`orientation`、`role` 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `section`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `orientation`：类型为 `Qt::Orientation`。没有默认值，调用时必须提供。传入 `Qt::Orientation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `role`：类型为 `int`。默认值为 `Qt::DisplayRole`。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QModelIndex QSortFilterProxyModel::index(int row, int column, const QModelIndex &parent = QModelIndex()) const`

**API 类别：** 成员函数说明

**中文解读：** `QSortFilterProxyModel::index` 用于计算、查询或取得与“索引”相关的操作。调用时要先确认当前状态和 `row`、`column`、`parent` 的有效范围；返回类型是 `QModelIndex`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QModelIndex`。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `column`：类型为 `int`。没有默认值，调用时必须提供。列号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `parent`：类型为 `const QModelIndex &`。默认值为 `QModelIndex()`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QSortFilterProxyModel::insertColumns(int column, int count, const QModelIndex &parent = QModelIndex())`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QSortFilterProxyModel` 添加依赖、数据或子对象的 API `insertColumns`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `column`：类型为 `int`。没有默认值，调用时必须提供。列号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `count`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `parent`：类型为 `const QModelIndex &`。默认值为 `QModelIndex()`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QSortFilterProxyModel::insertRows(int row, int count, const QModelIndex &parent = QModelIndex())`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QSortFilterProxyModel` 添加依赖、数据或子对象的 API `insertRows`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `count`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `parent`：类型为 `const QModelIndex &`。默认值为 `QModelIndex()`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QSortFilterProxyModel::invalidate()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `invalidate`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected, since 6.0, until 6.13] void QSortFilterProxyModel::invalidateColumnsFilter()`

**API 类别：** 成员函数说明

**中文解读：** `QSortFilterProxyModel::invalidateColumnsFilter` 用于执行与“invalidate、列、Filter”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected, until 6.13] void QSortFilterProxyModel::invalidateFilter()`

**API 类别：** 成员函数说明

**中文解读：** `QSortFilterProxyModel::invalidateFilter` 用于执行与“invalidate、Filter”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected, since 6.0, until 6.13] void QSortFilterProxyModel::invalidateRowsFilter()`

**API 类别：** 成员函数说明

**中文解读：** `QSortFilterProxyModel::invalidateRowsFilter` 用于执行与“invalidate、行、Filter”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] bool QSortFilterProxyModel::lessThan(const QModelIndex &source_left, const QModelIndex &source_right) const`

**API 类别：** 成员函数说明

**中文解读：** `QSortFilterProxyModel::lessThan` 用于计算、查询或取得与“less、Than”相关的操作。调用时要先确认当前状态和 `source_left`、`source_right` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `source_left`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。模型索引。调用前确认索引有效、属于正确模型，并注意模型结构变化后它可能失效。
- 参数 `source_right`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。模型索引。调用前确认索引有效、属于正确模型，并注意模型结构变化后它可能失效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QModelIndex QSortFilterProxyModel::mapFromSource(const QModelIndex &sourceIndex) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapFromSource`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QModelIndex`。
- 参数 `sourceIndex`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。模型索引。调用前确认索引有效、属于正确模型，并注意模型结构变化后它可能失效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QItemSelection QSortFilterProxyModel::mapSelectionFromSource(const QItemSelection &sourceSelection) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapSelectionFromSource`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QItemSelection`。
- 参数 `sourceSelection`：类型为 `const QItemSelection &`。没有默认值，调用时必须提供。传入 `const QItemSelection &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QItemSelection QSortFilterProxyModel::mapSelectionToSource(const QItemSelection &proxySelection) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapSelectionToSource`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QItemSelection`。
- 参数 `proxySelection`：类型为 `const QItemSelection &`。没有默认值，调用时必须提供。传入 `const QItemSelection &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QModelIndex QSortFilterProxyModel::mapToSource(const QModelIndex &proxyIndex) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapToSource`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QModelIndex`。
- 参数 `proxyIndex`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。模型索引。调用前确认索引有效、属于正确模型，并注意模型结构变化后它可能失效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QModelIndexList QSortFilterProxyModel::match(const QModelIndex &start, int role, const QVariant &value, int hits = 1, Qt::MatchFlags flags = Qt::MatchFlags(Qt::MatchStartsWith|Qt::MatchWrap)) const`

**API 类别：** 成员函数说明

**中文解读：** `QSortFilterProxyModel::match` 用于计算、查询或取得与“匹配”相关的操作。调用时要先确认当前状态和 `start`、`role`、`value`、`hits`、`flags` 的有效范围；返回类型是 `QModelIndexList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QModelIndexList`。
- 参数 `start`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。模型索引。调用前确认索引有效、属于正确模型，并注意模型结构变化后它可能失效。
- 参数 `role`：类型为 `int`。没有默认值，调用时必须提供。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。
- 参数 `value`：类型为 `const QVariant &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。
- 参数 `hits`：类型为 `int`。默认值为 `1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `Qt::MatchFlags`。默认值为 `Qt::MatchFlags(Qt::MatchStartsWith|Qt::MatchWrap)`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QMimeData *QSortFilterProxyModel::mimeData(const QModelIndexList &indexes) const`

**API 类别：** 成员函数说明

**中文解读：** `QSortFilterProxyModel::mimeData` 用于计算、查询或取得与“mime、数据访问”相关的操作。调用时要先确认当前状态和 `indexes` 的有效范围；返回类型是 `QMimeData *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMimeData *`。
- 参数 `indexes`：类型为 `const QModelIndexList &`。没有默认值，调用时必须提供。模型索引。调用前确认索引有效、属于正确模型，并注意模型结构变化后它可能失效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QStringList QSortFilterProxyModel::mimeTypes() const`

**API 类别：** 成员函数说明

**中文解读：** `QSortFilterProxyModel::mimeTypes` 用于计算、查询或取得与“mime、Types”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QModelIndex QSortFilterProxyModel::parent(const QModelIndex &child) const`

**API 类别：** 成员函数说明

**中文解读：** `QSortFilterProxyModel::parent` 用于计算、查询或取得与“父对象”相关的操作。调用时要先确认当前状态和 `child` 的有效范围；返回类型是 `QModelIndex`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QModelIndex`。
- 参数 `child`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。子对象或子节点；要确认它是否由父对象接管，以及调用后原指针是否仍有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QSortFilterProxyModel::recursiveFilteringEnabledChanged(bool recursiveFilteringEnabled)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSortFilterProxyModel` 发出的通知信号 `recursiveFilteringEnabledChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `recursiveFilteringEnabled`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QSortFilterProxyModel::removeColumns(int column, int count, const QModelIndex &parent = QModelIndex())`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeColumns`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`bool`。
- 参数 `column`：类型为 `int`。没有默认值，调用时必须提供。列号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `count`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `parent`：类型为 `const QModelIndex &`。默认值为 `QModelIndex()`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QSortFilterProxyModel::removeRows(int row, int count, const QModelIndex &parent = QModelIndex())`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeRows`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`bool`。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `count`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `parent`：类型为 `const QModelIndex &`。默认值为 `QModelIndex()`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] int QSortFilterProxyModel::rowCount(const QModelIndex &parent = QModelIndex()) const`

**API 类别：** 成员函数说明

**中文解读：** `QSortFilterProxyModel::rowCount` 用于计算、查询或取得与“行、数量统计”相关的操作。调用时要先确认当前状态和 `parent` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `parent`：类型为 `const QModelIndex &`。默认值为 `QModelIndex()`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QSortFilterProxyModel::setData(const QModelIndex &index, const QVariant &value, int role = Qt::EditRole)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setData`。调用它会改变 `QSortFilterProxyModel` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`bool`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `value`：类型为 `const QVariant &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。
- 参数 `role`：类型为 `int`。默认值为 `Qt::EditRole`。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。

**正确调用组合：** 成功修改后要发出对应 dataChanged；同时确认 flags 包含可编辑能力。

### `[slot] void QSortFilterProxyModel::setFilterFixedString(const QString &pattern)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `setFilterFixedString`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `pattern`：类型为 `const QString &`。没有默认值，调用时必须提供。匹配模式或格式模板；要确认转义规则、大小写策略和编译失败时的状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QSortFilterProxyModel::setFilterRegularExpression(const QString &pattern)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `setFilterRegularExpression`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `pattern`：类型为 `const QString &`。没有默认值，调用时必须提供。匹配模式或格式模板；要确认转义规则、大小写策略和编译失败时的状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QSortFilterProxyModel::setFilterWildcard(const QString &pattern)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `setFilterWildcard`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `pattern`：类型为 `const QString &`。没有默认值，调用时必须提供。匹配模式或格式模板；要确认转义规则、大小写策略和编译失败时的状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QSortFilterProxyModel::setHeaderData(int section, Qt::Orientation orientation, const QVariant &value, int role = Qt::EditRole)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setHeaderData`。调用它会改变 `QSortFilterProxyModel` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`bool`。
- 参数 `section`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `orientation`：类型为 `Qt::Orientation`。没有默认值，调用时必须提供。传入 `Qt::Orientation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const QVariant &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。
- 参数 `role`：类型为 `int`。默认值为 `Qt::EditRole`。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QSortFilterProxyModel::setSourceModel(QAbstractItemModel *sourceModel)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSourceModel`。调用它会改变 `QSortFilterProxyModel` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `sourceModel`：类型为 `QAbstractItemModel *`。没有默认值，调用时必须提供。传入 `QAbstractItemModel *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QModelIndex QSortFilterProxyModel::sibling(int row, int column, const QModelIndex &idx) const`

**API 类别：** 成员函数说明

**中文解读：** `QSortFilterProxyModel::sibling` 用于计算、查询或取得与“sibling”相关的操作。调用时要先确认当前状态和 `row`、`column`、`idx` 的有效范围；返回类型是 `QModelIndex`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QModelIndex`。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `column`：类型为 `int`。没有默认值，调用时必须提供。列号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `idx`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。模型索引。调用前确认索引有效、属于正确模型，并注意模型结构变化后它可能失效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QSortFilterProxyModel::sort(int column, Qt::SortOrder order = Qt::AscendingOrder)`

**API 类别：** 成员函数说明

**中文解读：** `QSortFilterProxyModel::sort` 用于执行与“sort”相关的操作。调用时要先确认当前状态和 `column`、`order` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `column`：类型为 `int`。没有默认值，调用时必须提供。列号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `order`：类型为 `Qt::SortOrder`。默认值为 `Qt::AscendingOrder`。传入 `Qt::SortOrder` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QSortFilterProxyModel::sortCaseSensitivityChanged(Qt::CaseSensitivity sortCaseSensitivity)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSortFilterProxyModel` 发出的通知信号 `sortCaseSensitivityChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `sortCaseSensitivity`：类型为 `Qt::CaseSensitivity`。没有默认值，调用时必须提供。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QSortFilterProxyModel::sortColumn() const`

**API 类别：** 成员函数说明

**中文解读：** `QSortFilterProxyModel::sortColumn` 用于计算、查询或取得与“sort、列”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QSortFilterProxyModel::sortLocaleAwareChanged(bool sortLocaleAware)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSortFilterProxyModel` 发出的通知信号 `sortLocaleAwareChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `sortLocaleAware`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::SortOrder QSortFilterProxyModel::sortOrder() const`

**API 类别：** 成员函数说明

**中文解读：** `QSortFilterProxyModel::sortOrder` 用于计算、查询或取得与“sort、Order”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::SortOrder`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::SortOrder`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QSortFilterProxyModel::sortRoleChanged(int sortRole)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSortFilterProxyModel` 发出的通知信号 `sortRoleChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `sortRole`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QSize QSortFilterProxyModel::span(const QModelIndex &index) const`

**API 类别：** 成员函数说明

**中文解读：** `QSortFilterProxyModel::span` 用于计算、查询或取得与“span”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] Qt::DropActions QSortFilterProxyModel::supportedDropActions() const`

**API 类别：** 成员函数说明

**中文解读：** `QSortFilterProxyModel::supportedDropActions` 用于计算、查询或取得与“supported、Drop、Actions”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::DropActions`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::DropActions`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.10) enum class Direction { Rows, Columns, Both }`

**API 类别：** 公有类型

**中文解读：** 这是 `QSortFilterProxyModel` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags Directions`

**API 类别：** 公有类型

**中文解读：** 这是 `QSortFilterProxyModel` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool autoAcceptChildRows() const`

**API 类别：** 公有函数

**中文解读：** `QSortFilterProxyModel::autoAcceptChildRows` 用于计算、查询或取得与“auto、接受、Child、行”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<bool> bindableAutoAcceptChildRows()`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableAutoAcceptChildRows`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<bool>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<bool> bindableDynamicSortFilter()`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableDynamicSortFilter`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<bool>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<Qt::CaseSensitivity> bindableFilterCaseSensitivity()`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableFilterCaseSensitivity`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<Qt::CaseSensitivity>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<int> bindableFilterKeyColumn()`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableFilterKeyColumn`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<int>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<QRegularExpression> bindableFilterRegularExpression()`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableFilterRegularExpression`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<QRegularExpression>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<int> bindableFilterRole()`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableFilterRole`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<int>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<bool> bindableIsSortLocaleAware()`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableIsSortLocaleAware`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<bool>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<bool> bindableRecursiveFilteringEnabled()`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableRecursiveFilteringEnabled`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<bool>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<Qt::CaseSensitivity> bindableSortCaseSensitivity()`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableSortCaseSensitivity`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<Qt::CaseSensitivity>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<int> bindableSortRole()`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableSortRole`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<int>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool dynamicSortFilter() const`

**API 类别：** 公有函数

**中文解读：** `QSortFilterProxyModel::dynamicSortFilter` 用于计算、查询或取得与“dynamic、Sort、Filter”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::CaseSensitivity filterCaseSensitivity() const`

**API 类别：** 公有函数

**中文解读：** `QSortFilterProxyModel::filterCaseSensitivity` 用于计算、查询或取得与“filter、Case、Sensitivity”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::CaseSensitivity`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::CaseSensitivity`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int filterKeyColumn() const`

**API 类别：** 公有函数

**中文解读：** `QSortFilterProxyModel::filterKeyColumn` 用于计算、查询或取得与“filter、Key、列”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRegularExpression filterRegularExpression() const`

**API 类别：** 公有函数

**中文解读：** `QSortFilterProxyModel::filterRegularExpression` 用于计算、查询或取得与“filter、Regular、Expression”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRegularExpression`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRegularExpression`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int filterRole() const`

**API 类别：** 公有函数

**中文解读：** `QSortFilterProxyModel::filterRole` 用于计算、查询或取得与“filter、角色”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool isRecursiveFilteringEnabled() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `isRecursiveFilteringEnabled`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool isSortLocaleAware() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `isSortLocaleAware`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setAutoAcceptChildRows(bool accept)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setAutoAcceptChildRows`。调用它会改变 `QSortFilterProxyModel` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `accept`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setDynamicSortFilter(bool enable)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setDynamicSortFilter`。调用它会改变 `QSortFilterProxyModel` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setFilterCaseSensitivity(Qt::CaseSensitivity cs)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setFilterCaseSensitivity`。调用它会改变 `QSortFilterProxyModel` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。没有默认值，调用时必须提供。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setFilterKeyColumn(int column)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setFilterKeyColumn`。调用它会改变 `QSortFilterProxyModel` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `column`：类型为 `int`。没有默认值，调用时必须提供。列号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setFilterRole(int role)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setFilterRole`。调用它会改变 `QSortFilterProxyModel` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `role`：类型为 `int`。没有默认值，调用时必须提供。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setRecursiveFilteringEnabled(bool recursive)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setRecursiveFilteringEnabled`。调用它会改变 `QSortFilterProxyModel` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `recursive`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setSortCaseSensitivity(Qt::CaseSensitivity cs)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setSortCaseSensitivity`。调用它会改变 `QSortFilterProxyModel` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。没有默认值，调用时必须提供。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setSortLocaleAware(bool on)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setSortLocaleAware`。调用它会改变 `QSortFilterProxyModel` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `on`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setSortRole(int role)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setSortRole`。调用它会改变 `QSortFilterProxyModel` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `role`：类型为 `int`。没有默认值，调用时必须提供。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::CaseSensitivity sortCaseSensitivity() const`

**API 类别：** 公有函数

**中文解读：** `QSortFilterProxyModel::sortCaseSensitivity` 用于计算、查询或取得与“sort、Case、Sensitivity”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::CaseSensitivity`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::CaseSensitivity`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int sortRole() const`

**API 类别：** 公有函数

**中文解读：** `QSortFilterProxyModel::sortRole` 用于计算、查询或取得与“sort、角色”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setFilterRegularExpression(const QRegularExpression &regularExpression)`

**API 类别：** 公有槽函数

**中文解读：** 这是可被信号连接或元对象调用的槽 `setFilterRegularExpression`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `regularExpression`：类型为 `const QRegularExpression &`。没有默认值，调用时必须提供。传入 `const QRegularExpression &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

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

`QSortFilterProxyModel` 所属机制类型：模型/视图协议。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
