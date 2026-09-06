# QHelpContentModel

> Qt 6.11.1 · Qt Help

## 1. 先建立直觉

**一句话定位：** `QHelpContentModel` 是 模型/视图协议 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** 这是 Qt Help 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QHelpContentModel` 是模型/视图体系中的数据模型类型，向视图提供索引、角色数据和结构变化通知。

**内部模型：** 视图不应该直接操作底层容器；它通过 QModelIndex 和 data roles 查询模型。模型必须准确维护索引有效性以及插入、删除、移动时的通知顺序。

**适用场景：** 需要把自定义数据接入 QListView、QTableView、QTreeView 或代理模型时使用。

**典型调用链：** 准备数据源 -> 实现/配置模型 -> 连接 view -> 通过 data/flags/setData 读写 -> 发出 dataChanged 或 begin/end 结构通知。

**先记住的坑：** 不要在 data() 中修改数据；不要返回过期索引；不要用全量 reset 代替精确结构通知，除非确实无法描述变化。

## 2. 依赖与对象关系

- 头文件：`#include <QHelpContentModel>`
- 继承自：QAbstractItemModel
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Help)
target_link_libraries(mytarget PRIVATE Qt6::Help)
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

- `virtual ~QHelpContentModel() override`
- `QHelpContentItem * contentItemAt(const QModelIndex &index) const`
- `void createContents(const QString &filter)`
- `(since 6.8) void createContentsForCurrentFilter()`
- `bool isCreatingContents() const`

### 重实现的公有函数

- `virtual int columnCount(const QModelIndex &parent = {}) const override`
- `virtual QVariant data(const QModelIndex &index, int role) const override`
- `virtual QModelIndex index(int row, int column, const QModelIndex &parent = {}) const override`
- `virtual QModelIndex parent(const QModelIndex &index) const override`
- `virtual int rowCount(const QModelIndex &parent = {}) const override`

### 信号

- `void contentsCreated()`
- `void contentsCreationStarted()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[override virtual noexcept] QHelpContentModel::~QHelpContentModel()`

**作用与语义：**

这破坏了帮助内容的模式。

### `[override virtual] int QHelpContentModel::columnCount(const QModelIndex &parent = {}) const`

**作用与语义：**

重实现自：Const QModelIndex 和 parent const. `QAbstractItemModel::columnCount`（const QModelIndex & parent） const.
返回给定`parent`下的列数。目前总是返回1。

### `QHelpContentItem *QHelpContentModel::contentItemAt(const QModelIndex &index) const`

**作用与语义：**

返回模型索引位置的帮助内容项 `index`。

### `[signal] void QHelpContentModel::contentsCreated()`

**作用与语义：**

当内容被创建时，该信号会发出。

### `[signal] void QHelpContentModel::contentsCreationStarted()`

**作用与语义：**

当内容开始创建时，该信号会被发射。从此以后，当前内容在信号`contentsCreated()`发出前均无效。

### `void QHelpContentModel::createContents(const QString &filter)`

**作用与语义：**

通过查询帮助系统中为自定义`filter`名称指定的内容创建新内容。

### `[since 6.8] void QHelpContentModel::createContentsForCurrentFilter()`

**作用与语义：**

通过查询当前筛选器指定的内容帮助系统创建新内容。

### `[override virtual] QVariant QHelpContentModel::data(const QModelIndex &index, int role) const`

**作用与语义：**

重实现自：`QAbstractItemModel::data`（const QModelIndex & index， int role） const.
返回`index`所指项在指定`role`下存储的数据。

### `[override virtual] QModelIndex QHelpContentModel::index(int row, int column, const QModelIndex &parent = {}) const`

**作用与语义：**

重实现自：`QAbstractItemModel::index`（整数行，整数列，cont QModelIndex 和parent）const.
返回由给定`row`、`column`和`parent`索引指定模型中项目的索引。

### `bool QHelpContentModel::isCreatingContents() const`

**作用与语义：**

如果内容正在重建，则返回真，否则返回 false。

### `[override virtual] QModelIndex QHelpContentModel::parent(const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractItemModel::parent`（const QModelIndex & index） const.
返回带有给定 `index` 的模型项目的父项，若无父项则返回 QModelIndex()。

### `[override virtual] int QHelpContentModel::rowCount(const QModelIndex &parent = {}) const`

**作用与语义：**

重实现自：`QAbstractItemModel::rowCount`（const QModelIndex & parent） const.
返回给定`parent`下的行数。

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

`QHelpContentModel` 所属机制类型：模型/视图协议。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
