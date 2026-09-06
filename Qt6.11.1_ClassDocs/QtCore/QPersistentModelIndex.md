# QPersistentModelIndex

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QPersistentModelIndex` 是 模型/视图协议 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QPersistentModelIndex` 是 模型/视图协议 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 视图不直接读取业务容器，而是通过 `QModelIndex`、行列坐标和数据角色向模型查询。模型必须维护索引、父子层级、角色数据以及插入/删除/移动/重置通知；代理模型则在索引映射、排序和过滤之间维护另一层关系。

**适用场景：** 先确定数据层级和角色，再实现/配置模型，连接视图和选择模型；编辑时同时实现 flags、setData 和对应通知；结构变化严格成对调用 begin/end。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要在 `data()` 中修改数据或做长时间阻塞操作；不要混用 DisplayRole、EditRole 和 UserRole；不要保存没有稳定生命周期保证的索引；不要用 reset 掩盖本可以精确描述的局部变化。

## 2. 依赖与对象关系

- 头文件：`#include <QPersistentModelIndex>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

视图不直接读取业务容器，而是通过 `QModelIndex`、行列坐标和数据角色向模型查询。模型必须维护索引、父子层级、角色数据以及插入/删除/移动/重置通知；代理模型则在索引映射、排序和过滤之间维护另一层关系。

### 状态、生命周期和线程

**生命周期：** 模型应比视图活得足够久，视图销毁时不会自动替业务容器释放资源。模型变化必须使用对应的 begin/end 协议或精确通知，不能只改容器后期待视图自行发现。取到的 QModelIndex 只在模型允许的生命周期内有效。

**状态与结果：** 区分当前索引、选择模型、编辑状态、数据角色和模型结构变化。`dataChanged` 表示已有项目的数据变化，行列插入/删除表示结构变化，`modelReset` 会让旧索引整体失效。

**线程与事件循环：** 模型通常在 GUI 线程被视图访问。后台线程不要直接修改正在显示的模型；应在正确线程汇总数据，再通过通知协议更新，或使用线程安全的数据交换层。

## 3. 直接使用

先确定数据层级和角色，再实现/配置模型，连接视图和选择模型；编辑时同时实现 flags、setData 和对应通知；结构变化严格成对调用 begin/end。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

```cpp
// 视图通过 QModelIndex 和 role 查询模型。
const QVariant value = model->data(index, Qt::DisplayRole);
// 数据变化时由模型发出 dataChanged 或 begin/end 结构通知。
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QPersistentModelIndex(const QModelIndex &index)`
- `QPersistentModelIndex(const QPersistentModelIndex &other)`
- `QPersistentModelIndex(QPersistentModelIndex &&other)`
- `int column() const`
- `QVariant data(int role = Qt::DisplayRole) const`
- `Qt::ItemFlags flags() const`
- `bool isValid() const`
- `const QAbstractItemModel * model() const`
- `(since 6.0) void multiData(QModelRoleDataSpan roleDataSpan) const`
- `QModelIndex parent() const`
- `int row() const`
- `QModelIndex sibling(int row, int column) const`
- `void swap(QPersistentModelIndex &other)`
- `operator QModelIndex() const`
- `QPersistentModelIndex & operator=(QPersistentModelIndex &&other)`
- `QPersistentModelIndex & operator=(const QModelIndex &other)`
- `QPersistentModelIndex & operator=(const QPersistentModelIndex &other)`

### 相关非成员函数

- `size_t qHash(const QPersistentModelIndex &key, size_t seed = 0)`
- `bool operator!=(const QPersistentModelIndex &lhs, const QModelIndex &rhs)`
- `bool operator!=(const QPersistentModelIndex &lhs, const QPersistentModelIndex &rhs)`
- `bool operator<(const QPersistentModelIndex &lhs, const QPersistentModelIndex &rhs)`
- `bool operator==(const QPersistentModelIndex &lhs, const QModelIndex &rhs)`
- `bool operator==(const QPersistentModelIndex &lhs, const QPersistentModelIndex &rhs)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 23 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QPersistentModelIndex::QPersistentModelIndex(const QModelIndex &index)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPersistentModelIndex` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `index`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPersistentModelIndex::QPersistentModelIndex(const QPersistentModelIndex &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPersistentModelIndex` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QPersistentModelIndex &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QPersistentModelIndex::QPersistentModelIndex(QPersistentModelIndex &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPersistentModelIndex` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `QPersistentModelIndex &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QPersistentModelIndex::column() const`

**API 类别：** 成员函数说明

**中文解读：** `QPersistentModelIndex::column` 用于计算、查询或取得与“列”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVariant QPersistentModelIndex::data(int role = Qt::DisplayRole) const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `data`，用于取得 `QPersistentModelIndex` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `role`：类型为 `int`。默认值为 `Qt::DisplayRole`。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。

**正确调用组合：** 通常与 role、QModelIndex 有关；数据变化后发 `dataChanged`，不要在 data() 中修改模型。

### `Qt::ItemFlags QPersistentModelIndex::flags() const`

**API 类别：** 成员函数说明

**中文解读：** `QPersistentModelIndex::flags` 用于计算、查询或取得与“标志”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::ItemFlags`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::ItemFlags`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPersistentModelIndex::isValid() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isValid`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QAbstractItemModel *QPersistentModelIndex::model() const`

**API 类别：** 成员函数说明

**中文解读：** `QPersistentModelIndex::model` 用于计算、查询或取得与“model”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QAbstractItemModel *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QAbstractItemModel *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] void QPersistentModelIndex::multiData(QModelRoleDataSpan roleDataSpan) const`

**API 类别：** 成员函数说明

**中文解读：** `QPersistentModelIndex::multiData` 用于执行与“multi、数据访问”相关的操作。调用时要先确认当前状态和 `roleDataSpan` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `roleDataSpan`：类型为 `QModelRoleDataSpan`。没有默认值，调用时必须提供。传入 `QModelRoleDataSpan` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QModelIndex QPersistentModelIndex::parent() const`

**API 类别：** 成员函数说明

**中文解读：** `QPersistentModelIndex::parent` 用于计算、查询或取得与“父对象”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QModelIndex`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QModelIndex`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QPersistentModelIndex::row() const`

**API 类别：** 成员函数说明

**中文解读：** `QPersistentModelIndex::row` 用于计算、查询或取得与“行”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QModelIndex QPersistentModelIndex::sibling(int row, int column) const`

**API 类别：** 成员函数说明

**中文解读：** `QPersistentModelIndex::sibling` 用于计算、查询或取得与“sibling”相关的操作。调用时要先确认当前状态和 `row`、`column` 的有效范围；返回类型是 `QModelIndex`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QModelIndex`。
- 参数 `row`：类型为 `int`。没有默认值，调用时必须提供。行号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。
- 参数 `column`：类型为 `int`。没有默认值，调用时必须提供。列号，通常从 0 开始；要确认它属于当前模型、表格或矩形范围。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QPersistentModelIndex::swap(QPersistentModelIndex &other)`

**API 类别：** 成员函数说明

**中文解读：** `QPersistentModelIndex::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QPersistentModelIndex &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPersistentModelIndex::operator QModelIndex() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPersistentModelIndex` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`由运算符声明决定`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QPersistentModelIndex &QPersistentModelIndex::operator=(QPersistentModelIndex &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPersistentModelIndex` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QPersistentModelIndex &`。
- 参数 `other`：类型为 `QPersistentModelIndex &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPersistentModelIndex &QPersistentModelIndex::operator=(const QModelIndex &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPersistentModelIndex` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QPersistentModelIndex &`。
- 参数 `other`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPersistentModelIndex &QPersistentModelIndex::operator=(const QPersistentModelIndex &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPersistentModelIndex` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QPersistentModelIndex &`。
- 参数 `other`：类型为 `const QPersistentModelIndex &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] size_t qHash(const QPersistentModelIndex &key, size_t seed = 0)`

**API 类别：** 相关非成员函数

**中文解读：** `QPersistentModelIndex::qHash` 用于计算、查询或取得与“q、Hash”相关的操作。调用时要先确认当前状态和 `key`、`seed` 的有效范围；返回类型是 `size_t`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`size_t`。
- 参数 `key`：类型为 `const QPersistentModelIndex &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `seed`：类型为 `size_t`。默认值为 `0`。传入 `size_t` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator!=(const QPersistentModelIndex &lhs, const QModelIndex &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QPersistentModelIndex` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QPersistentModelIndex &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator!=(const QPersistentModelIndex &lhs, const QPersistentModelIndex &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QPersistentModelIndex` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QPersistentModelIndex &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QPersistentModelIndex &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator<(const QPersistentModelIndex &lhs, const QPersistentModelIndex &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QPersistentModelIndex` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QPersistentModelIndex &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QPersistentModelIndex &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator==(const QPersistentModelIndex &lhs, const QModelIndex &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QPersistentModelIndex` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QPersistentModelIndex &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QModelIndex &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator==(const QPersistentModelIndex &lhs, const QPersistentModelIndex &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QPersistentModelIndex` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QPersistentModelIndex &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QPersistentModelIndex &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

模型应比视图活得足够久，视图销毁时不会自动替业务容器释放资源。模型变化必须使用对应的 begin/end 协议或精确通知，不能只改容器后期待视图自行发现。取到的 QModelIndex 只在模型允许的生命周期内有效。

### 状态和错误边界

区分当前索引、选择模型、编辑状态、数据角色和模型结构变化。`dataChanged` 表示已有项目的数据变化，行列插入/删除表示结构变化，`modelReset` 会让旧索引整体失效。

### 线程边界

模型通常在 GUI 线程被视图访问。后台线程不要直接修改正在显示的模型；应在正确线程汇总数据，再通过通知协议更新，或使用线程安全的数据交换层。

### 最容易出现的错误

不要在 `data()` 中修改数据或做长时间阻塞操作；不要混用 DisplayRole、EditRole 和 UserRole；不要保存没有稳定生命周期保证的索引；不要用 reset 掩盖本可以精确描述的局部变化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QPersistentModelIndex` 所属机制类型：模型/视图协议。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
