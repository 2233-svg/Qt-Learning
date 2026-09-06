# QHelpIndexModel

> Qt 6.11.1 · Qt Help

## 1. 先建立直觉

**一句话定位：** `QHelpIndexModel` 是 模型/视图协议 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** 这是 Qt Help 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QHelpIndexModel` 是模型/视图体系中的数据模型类型，向视图提供索引、角色数据和结构变化通知。

**内部模型：** 视图不应该直接操作底层容器；它通过 QModelIndex 和 data roles 查询模型。模型必须准确维护索引有效性以及插入、删除、移动时的通知顺序。

**适用场景：** 需要把自定义数据接入 QListView、QTableView、QTreeView 或代理模型时使用。

**典型调用链：** 准备数据源 -> 实现/配置模型 -> 连接 view -> 通过 data/flags/setData 读写 -> 发出 dataChanged 或 begin/end 结构通知。

**先记住的坑：** 不要在 data() 中修改数据；不要返回过期索引；不要用全量 reset 代替精确结构通知，除非确实无法描述变化。

## 2. 依赖与对象关系

- 头文件：`#include <QHelpIndexModel>`
- 继承自：QStringListModel
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Help)
target_link_libraries(mytarget PRIVATE Qt6::Help)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

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

- `void createIndex(const QString &filter)`
- `(since 6.8) void createIndexForCurrentFilter()`
- `QModelIndex filter(const QString &filter, const QString &wildcard = {})`
- `QHelpEngineCore * helpEngine() const`
- `bool isCreatingIndex() const`

### 信号

- `void indexCreated()`
- `void indexCreationStarted()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `void QHelpIndexModel::createIndex(const QString &filter)`

**作用与语义：**

通过查询指定自定义`filter`名称的关键词，创建新的索引。

### `[since 6.8] void QHelpIndexModel::createIndexForCurrentFilter()`

**作用与语义：**

通过查询当前筛选关键词的帮助系统创建新索引。

### `QModelIndex QHelpIndexModel::filter(const QString &filter, const QString &wildcard = {})`

**作用与语义：**

过滤索引并返回最佳匹配关键词的模型索引。第一步中，只有包含`filter`的关键词保留在模型索引列表中。类似地，如果`wildcard`不空，索引列表中只剩匹配的关键词。第二步确定最佳匹配并返回其索引模型。在指定万用符表达式时，使用`filter`字符串搜索最佳匹配。

### `QHelpEngineCore *QHelpIndexModel::helpEngine() const`

**作用与语义：**

返回管理该模型的相关帮助引擎。

### `[signal] void QHelpIndexModel::indexCreated()`

**作用与语义：**

该信号是在索引创建时发出的。

### `[signal] void QHelpIndexModel::indexCreationStarted()`

**作用与语义：**

当新索引开始创建时，该信号会被发射。从此以后，当前索引在信号`indexCreated()`发出前均无效。

### `bool QHelpIndexModel::isCreatingIndex() const`

**作用与语义：**

如果索引正在建立中，则返回真，否则返回 false。

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

`QHelpIndexModel` 所属机制类型：模型/视图协议。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
