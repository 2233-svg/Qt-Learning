# QTransposeProxyModel

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QTransposeProxyModel` 是 模型/视图协议 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QTransposeProxyModel` 是模型/视图体系中的数据模型类型，向视图提供索引、角色数据和结构变化通知。

**内部模型：** 视图不应该直接操作底层容器；它通过 QModelIndex 和 data roles 查询模型。模型必须准确维护索引有效性以及插入、删除、移动时的通知顺序。

**适用场景：** 需要把自定义数据接入 QListView、QTableView、QTreeView 或代理模型时使用。

**典型调用链：** 准备数据源 -> 实现/配置模型 -> 连接 view -> 通过 data/flags/setData 读写 -> 发出 dataChanged 或 begin/end 结构通知。

**先记住的坑：** 不要在 data() 中修改数据；不要返回过期索引；不要用全量 reset 代替精确结构通知，除非确实无法描述变化。

## 2. 依赖与对象关系

- 头文件：`#include <QTransposeProxyModel>`
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

### 公有函数

- `QTransposeProxyModel(QObject *parent = nullptr)`
- `virtual ~QTransposeProxyModel()`

### 重实现的公有函数

- `virtual int columnCount(const QModelIndex &parent = QModelIndex()) const override`
- `virtual QVariant headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const override`
- `virtual QModelIndex index(int row, int column, const QModelIndex &parent = QModelIndex()) const override`
- `virtual bool insertColumns(int column, int count, const QModelIndex &parent = QModelIndex()) override`
- `virtual bool insertRows(int row, int count, const QModelIndex &parent = QModelIndex()) override`
- `virtual QMap<int, QVariant> itemData(const QModelIndex &index) const override`
- `virtual QModelIndex mapFromSource(const QModelIndex &sourceIndex) const override`
- `virtual QModelIndex mapToSource(const QModelIndex &proxyIndex) const override`
- `virtual bool moveColumns(const QModelIndex &sourceParent, int sourceRow, int count, const QModelIndex &destinationParent, int destinationChild) override`
- `virtual bool moveRows(const QModelIndex &sourceParent, int sourceRow, int count, const QModelIndex &destinationParent, int destinationChild) override`
- `virtual QModelIndex parent(const QModelIndex &index) const override`
- `virtual bool removeColumns(int column, int count, const QModelIndex &parent = QModelIndex()) override`
- `virtual bool removeRows(int row, int count, const QModelIndex &parent = QModelIndex()) override`
- `virtual int rowCount(const QModelIndex &parent = QModelIndex()) const override`
- `virtual bool setHeaderData(int section, Qt::Orientation orientation, const QVariant &value, int role = Qt::EditRole) override`
- `virtual bool setItemData(const QModelIndex &index, const QMap<int, QVariant> &roles) override`
- `virtual void setSourceModel(QAbstractItemModel *newSourceModel) override`
- `virtual void sort(int column, Qt::SortOrder order = Qt::AscendingOrder) override`
- `virtual QSize span(const QModelIndex &index) const override`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 21 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[explicit] QTransposeProxyModel::QTransposeProxyModel(QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTransposeProxyModel` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QTransposeProxyModel::~QTransposeProxyModel()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTransposeProxyModel` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] int QTransposeProxyModel::columnCount(const QModelIndex &parent = QModelIndex()) const`

**API 类别：** 成员函数说明

**中文解读：** `QTransposeProxyModel::columnCount` 用于计算、查询或取得与“列、数量统计”相关的操作。调用时要先确认当前状态和 `parent` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `parent`：类型为 `const QModelIndex &`。默认值为 `QModelIndex()`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QVariant QTransposeProxyModel::headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const`

**API 类别：** 成员函数说明

**中文解读：** `QTransposeProxyModel::headerData` 用于计算、查询或取得与“header、数据访问”相关的操作。调用时要先确认当前状态和 `section`、`orientation`、`role` 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `section`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `orientation`：类型为 `Qt::Orientation`。没有默认值，调用时必须提供。传入 `Qt::Orientation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `role`：类型为 `int`。默认值为 `Qt::DisplayRole`。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QModelIndex QTransposeProxyModel::index(int row, int column, const QModelIndex &parent = QModelIndex()) const`

**API 类别：** 成员函数说明

**中文解读：** `QTransposeProxyModel::index` 用于计算、查询或取得与“索引”相关的操作。调用时要先确认当前状态和 `row`、`column`、`parent` 的有效范围；返回类型是 `QModelIndex`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QModelIndex`。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `column`：类型为 `int`。没有默认值，调用时必须提供。列号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `parent`：类型为 `const QModelIndex &`。默认值为 `QModelIndex()`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QTransposeProxyModel::insertColumns(int column, int count, const QModelIndex &parent = QModelIndex())`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QTransposeProxyModel` 添加依赖、数据或子对象的 API `insertColumns`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `column`：类型为 `int`。没有默认值，调用时必须提供。列号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `count`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `parent`：类型为 `const QModelIndex &`。默认值为 `QModelIndex()`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QTransposeProxyModel::insertRows(int row, int count, const QModelIndex &parent = QModelIndex())`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QTransposeProxyModel` 添加依赖、数据或子对象的 API `insertRows`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `count`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `parent`：类型为 `const QModelIndex &`。默认值为 `QModelIndex()`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QMap<int, QVariant> QTransposeProxyModel::itemData(const QModelIndex &index) const`

**API 类别：** 成员函数说明

**中文解读：** `QTransposeProxyModel::itemData` 用于计算、查询或取得与“项目访问、数据访问”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `QMap<int, QVariant>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMap<int, QVariant>`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QModelIndex QTransposeProxyModel::mapFromSource(const QModelIndex &sourceIndex) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapFromSource`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QModelIndex`。
- 参数 `sourceIndex`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。模型索引。调用前确认索引有效、属于正确模型，并注意模型结构变化后它可能失效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QModelIndex QTransposeProxyModel::mapToSource(const QModelIndex &proxyIndex) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapToSource`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QModelIndex`。
- 参数 `proxyIndex`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。模型索引。调用前确认索引有效、属于正确模型，并注意模型结构变化后它可能失效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QTransposeProxyModel::moveColumns(const QModelIndex &sourceParent, int sourceRow, int count, const QModelIndex &destinationParent, int destinationChild)`

**API 类别：** 成员函数说明

**中文解读：** `QTransposeProxyModel::moveColumns` 用于计算、查询或取得与“移动、列”相关的操作。调用时要先确认当前状态和 `sourceParent`、`sourceRow`、`count`、`destinationParent`、`destinationChild` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `sourceParent`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `sourceRow`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `destinationParent`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `destinationChild`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QTransposeProxyModel::moveRows(const QModelIndex &sourceParent, int sourceRow, int count, const QModelIndex &destinationParent, int destinationChild)`

**API 类别：** 成员函数说明

**中文解读：** `QTransposeProxyModel::moveRows` 用于计算、查询或取得与“移动、行”相关的操作。调用时要先确认当前状态和 `sourceParent`、`sourceRow`、`count`、`destinationParent`、`destinationChild` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `sourceParent`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `sourceRow`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `destinationParent`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `destinationChild`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QModelIndex QTransposeProxyModel::parent(const QModelIndex &index) const`

**API 类别：** 成员函数说明

**中文解读：** `QTransposeProxyModel::parent` 用于计算、查询或取得与“父对象”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `QModelIndex`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QModelIndex`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QTransposeProxyModel::removeColumns(int column, int count, const QModelIndex &parent = QModelIndex())`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeColumns`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`bool`。
- 参数 `column`：类型为 `int`。没有默认值，调用时必须提供。列号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `count`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `parent`：类型为 `const QModelIndex &`。默认值为 `QModelIndex()`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QTransposeProxyModel::removeRows(int row, int count, const QModelIndex &parent = QModelIndex())`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeRows`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`bool`。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `count`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `parent`：类型为 `const QModelIndex &`。默认值为 `QModelIndex()`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] int QTransposeProxyModel::rowCount(const QModelIndex &parent = QModelIndex()) const`

**API 类别：** 成员函数说明

**中文解读：** `QTransposeProxyModel::rowCount` 用于计算、查询或取得与“行、数量统计”相关的操作。调用时要先确认当前状态和 `parent` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `parent`：类型为 `const QModelIndex &`。默认值为 `QModelIndex()`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QTransposeProxyModel::setHeaderData(int section, Qt::Orientation orientation, const QVariant &value, int role = Qt::EditRole)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setHeaderData`。调用它会改变 `QTransposeProxyModel` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`bool`。
- 参数 `section`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `orientation`：类型为 `Qt::Orientation`。没有默认值，调用时必须提供。传入 `Qt::Orientation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const QVariant &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。
- 参数 `role`：类型为 `int`。默认值为 `Qt::EditRole`。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QTransposeProxyModel::setItemData(const QModelIndex &index, const QMap<int, QVariant> &roles)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setItemData`。调用它会改变 `QTransposeProxyModel` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`bool`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `roles`：类型为 `const QMap<int, QVariant> &`。没有默认值，调用时必须提供。传入 `const QMap<int, QVariant> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QTransposeProxyModel::setSourceModel(QAbstractItemModel *newSourceModel)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSourceModel`。调用它会改变 `QTransposeProxyModel` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `newSourceModel`：类型为 `QAbstractItemModel *`。没有默认值，调用时必须提供。传入 `QAbstractItemModel *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QTransposeProxyModel::sort(int column, Qt::SortOrder order = Qt::AscendingOrder)`

**API 类别：** 成员函数说明

**中文解读：** `QTransposeProxyModel::sort` 用于执行与“sort”相关的操作。调用时要先确认当前状态和 `column`、`order` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `column`：类型为 `int`。没有默认值，调用时必须提供。列号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `order`：类型为 `Qt::SortOrder`。默认值为 `Qt::AscendingOrder`。传入 `Qt::SortOrder` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QSize QTransposeProxyModel::span(const QModelIndex &index) const`

**API 类别：** 成员函数说明

**中文解读：** `QTransposeProxyModel::span` 用于计算、查询或取得与“span”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

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

`QTransposeProxyModel` 所属机制类型：模型/视图协议。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
