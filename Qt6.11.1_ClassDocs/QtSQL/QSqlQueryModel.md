# QSqlQueryModel

> Qt 6.11.1 · Qt SQL

## 1. 先建立直觉

**一句话定位：** `QSqlQueryModel` 是 Qt SQL 的“Sql查询模型”类型，参与数据库连接、SQL 执行、事务或结果模型。

**模块背景：** Qt SQL 提供数据库连接、查询、事务和 SQL 模型/视图集成。

### 这是什么

`QSqlQueryModel` 是模型/视图体系中的数据模型类型，向视图提供索引、角色数据和结构变化通知。

**内部模型：** 视图不应该直接操作底层容器；它通过 QModelIndex 和 data roles 查询模型。模型必须准确维护索引有效性以及插入、删除、移动时的通知顺序。

**适用场景：** 需要把自定义数据接入 QListView、QTableView、QTreeView 或代理模型时使用。

**典型调用链：** 准备数据源 -> 实现/配置模型 -> 连接 view -> 通过 data/flags/setData 读写 -> 发出 dataChanged 或 begin/end 结构通知。

**先记住的坑：** 不要在 data() 中修改数据；不要返回过期索引；不要用全量 reset 代替精确结构通知，除非确实无法描述变化。

## 2. 依赖与对象关系

- 头文件：`#include <QSqlQueryModel>`
- 继承自：QAbstractTableModel
- 直接派生类：QSqlTableModel

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Sql)
target_link_libraries(mytarget PRIVATE Qt6::Sql)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

视图不应该直接操作底层容器；它通过 QModelIndex 和 data roles 查询模型。模型必须准确维护索引有效性以及插入、删除、移动时的通知顺序。

### 状态、生命周期和线程

**生命周期：** 连接由连接名识别，查询和模型引用连接。关闭或移除连接前必须销毁仍引用它的 query、model 和 database 句柄；不同线程不要共用连接。

**状态与结果：** 区分连接是否打开、语句是否执行成功、游标是否定位在有效行、字段是否存在以及事务是否提交成功。`exec()` 成功不代表有结果行，`next()` 成功后才可以安全读取当前行。

**线程与事件循环：** Qt SQL 连接有线程归属，每个线程应建立自己的连接并使用唯一连接名；不要把一个线程创建的 QSqlDatabase 或 QSqlQuery 传到另一个线程继续使用。

## 3. 直接使用

需要把自定义数据接入 QListView、QTableView、QTreeView 或代理模型时使用。 使用时通常按这个过程组织：准备数据源 -> 实现/配置模型 -> 连接 view -> 通过 data/flags/setData 读写 -> 发出 dataChanged 或 begin/end 结构通知。

```cpp
QSqlQuery query(database);
query.prepare(QStringLiteral("SELECT name FROM users WHERE id = :id"));
query.bindValue(QStringLiteral(":id"), id);
if (query.exec()) {
    while (query.next()) {
        const QVariant value = query.value(0);
    }
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QSqlQueryModel(QObject *parent = nullptr)`
- `virtual ~QSqlQueryModel()`
- `virtual void clear()`
- `QSqlError lastError() const`
- `const QSqlQuery & query() const`
- `QSqlRecord record(int row) const`
- `QSqlRecord record() const`
- `(since 6.9) void refresh()`
- `(since 6.2) void setQuery(QSqlQuery &&query)`
- `void setQuery(const QString &query, const QSqlDatabase &db = QSqlDatabase())`

### 重实现的公有函数

- `virtual bool canFetchMore(const QModelIndex &parent = QModelIndex()) const override`
- `virtual int columnCount(const QModelIndex &index = QModelIndex()) const override`
- `virtual QVariant data(const QModelIndex &item, int role = Qt::DisplayRole) const override`
- `virtual void fetchMore(const QModelIndex &parent = QModelIndex()) override`
- `virtual QVariant headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const override`
- `virtual bool insertColumns(int column, int count, const QModelIndex &parent = QModelIndex()) override`
- `virtual bool removeColumns(int column, int count, const QModelIndex &parent = QModelIndex()) override`
- `virtual QHash<int, QByteArray> roleNames() const override`
- `virtual int rowCount(const QModelIndex &parent = QModelIndex()) const override`
- `virtual bool setHeaderData(int section, Qt::Orientation orientation, const QVariant &value, int role = Qt::EditRole) override`

### 保护函数

- `virtual QModelIndex indexInQuery(const QModelIndex &item) const`
- `virtual void queryChange()`
- `void setLastError(const QSqlError &error)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 23 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[explicit] QSqlQueryModel::QSqlQueryModel(QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSqlQueryModel` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QSqlQueryModel::~QSqlQueryModel()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSqlQueryModel` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QSqlQueryModel::canFetchMore(const QModelIndex &parent = QModelIndex()) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `canFetchMore`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `parent`：类型为 `const QModelIndex &`。默认值为 `QModelIndex()`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] void QSqlQueryModel::clear()`

**API 类别：** 成员函数说明

**中文解读：** 这是状态清理或重置 API `clear`。调用后原有数据、索引、缓存或绑定可能失效；使用前先确认它影响的是当前对象、子对象还是底层共享资源，之后重新检查状态。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] int QSqlQueryModel::columnCount(const QModelIndex &index = QModelIndex()) const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQueryModel::columnCount` 用于计算、查询或取得与“列、数量统计”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `index`：类型为 `const QModelIndex &`。默认值为 `QModelIndex()`。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QVariant QSqlQueryModel::data(const QModelIndex &item, int role = Qt::DisplayRole) const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `data`，用于取得 `QSqlQueryModel` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `item`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。
- 参数 `role`：类型为 `int`。默认值为 `Qt::DisplayRole`。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QSqlQueryModel::fetchMore(const QModelIndex &parent = QModelIndex())`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSqlQueryModel` 的核心操作 `fetchMore`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `parent`：类型为 `const QModelIndex &`。默认值为 `QModelIndex()`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QVariant QSqlQueryModel::headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQueryModel::headerData` 用于计算、查询或取得与“header、数据访问”相关的操作。调用时要先确认当前状态和 `section`、`orientation`、`role` 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `section`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `orientation`：类型为 `Qt::Orientation`。没有默认值，调用时必须提供。传入 `Qt::Orientation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `role`：类型为 `int`。默认值为 `Qt::DisplayRole`。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] QModelIndex QSqlQueryModel::indexInQuery(const QModelIndex &item) const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQueryModel::indexInQuery` 用于计算、查询或取得与“索引、In、查询”相关的操作。调用时要先确认当前状态和 `item` 的有效范围；返回类型是 `QModelIndex`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QModelIndex`。
- 参数 `item`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QSqlQueryModel::insertColumns(int column, int count, const QModelIndex &parent = QModelIndex())`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QSqlQueryModel` 添加依赖、数据或子对象的 API `insertColumns`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `column`：类型为 `int`。没有默认值，调用时必须提供。列号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `count`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `parent`：类型为 `const QModelIndex &`。默认值为 `QModelIndex()`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSqlError QSqlQueryModel::lastError() const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQueryModel::lastError` 用于计算、查询或取得与“末项、错误”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSqlError`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSqlError`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QSqlQuery &QSqlQueryModel::query() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSqlQueryModel` 的核心操作 `query`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`const QSqlQuery &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QSqlQueryModel::queryChange()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSqlQueryModel` 的核心操作 `queryChange`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSqlRecord QSqlQueryModel::record(int row) const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQueryModel::record` 用于计算、查询或取得与“record”相关的操作。调用时要先确认当前状态和 `row` 的有效范围；返回类型是 `QSqlRecord`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSqlRecord`。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSqlRecord QSqlQueryModel::record() const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQueryModel::record` 用于计算、查询或取得与“record”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSqlRecord`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSqlRecord`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] void QSqlQueryModel::refresh()`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQueryModel::refresh` 用于执行与“refresh”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QSqlQueryModel::removeColumns(int column, int count, const QModelIndex &parent = QModelIndex())`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeColumns`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`bool`。
- 参数 `column`：类型为 `int`。没有默认值，调用时必须提供。列号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `count`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `parent`：类型为 `const QModelIndex &`。默认值为 `QModelIndex()`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QHash<int, QByteArray> QSqlQueryModel::roleNames() const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQueryModel::roleNames` 用于计算、查询或取得与“角色、Names”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QHash<int, QByteArray>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QHash<int, QByteArray>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] int QSqlQueryModel::rowCount(const QModelIndex &parent = QModelIndex()) const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQueryModel::rowCount` 用于计算、查询或取得与“行、数量统计”相关的操作。调用时要先确认当前状态和 `parent` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `parent`：类型为 `const QModelIndex &`。默认值为 `QModelIndex()`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QSqlQueryModel::setHeaderData(int section, Qt::Orientation orientation, const QVariant &value, int role = Qt::EditRole)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setHeaderData`。调用它会改变 `QSqlQueryModel` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`bool`。
- 参数 `section`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `orientation`：类型为 `Qt::Orientation`。没有默认值，调用时必须提供。传入 `Qt::Orientation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const QVariant &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。
- 参数 `role`：类型为 `int`。默认值为 `Qt::EditRole`。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QSqlQueryModel::setLastError(const QSqlError &error)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setLastError`。调用它会改变 `QSqlQueryModel` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `error`：类型为 `const QSqlError &`。没有默认值，调用时必须提供。错误输出对象或错误状态。解析/执行后要检查它，而不能只看主返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] void QSqlQueryModel::setQuery(QSqlQuery &&query)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setQuery`。调用它会改变 `QSqlQueryModel` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `query`：类型为 `QSqlQuery &&`。没有默认值，调用时必须提供。传入 `QSqlQuery &&` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSqlQueryModel::setQuery(const QString &query, const QSqlDatabase &db = QSqlDatabase())`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setQuery`。调用它会改变 `QSqlQueryModel` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `query`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `db`：类型为 `const QSqlDatabase &`。默认值为 `QSqlDatabase()`。传入 `const QSqlDatabase &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

连接由连接名识别，查询和模型引用连接。关闭或移除连接前必须销毁仍引用它的 query、model 和 database 句柄；不同线程不要共用连接。

### 状态和错误边界

区分连接是否打开、语句是否执行成功、游标是否定位在有效行、字段是否存在以及事务是否提交成功。`exec()` 成功不代表有结果行，`next()` 成功后才可以安全读取当前行。

### 线程边界

Qt SQL 连接有线程归属，每个线程应建立自己的连接并使用唯一连接名；不要把一个线程创建的 QSqlDatabase 或 QSqlQuery 传到另一个线程继续使用。

### 最容易出现的错误

不要在 data() 中修改数据；不要返回过期索引；不要用全量 reset 代替精确结构通知，除非确实无法描述变化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QSqlQueryModel` 所属机制类型：Qt SQL 连接、查询与事务机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
