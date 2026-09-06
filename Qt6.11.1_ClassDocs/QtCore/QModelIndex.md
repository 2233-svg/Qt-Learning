# QModelIndex

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 模型/视图中定位一个数据项的轻量索引。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QModelIndex`：模型/视图中定位一个数据项的轻量索引。

**内部模型：** 视图不直接读取业务容器，而是通过 `QModelIndex`、行列坐标和数据角色向模型查询。模型必须维护索引、父子层级、角色数据以及插入/删除/移动/重置通知；代理模型则在索引映射、排序和过滤之间维护另一层关系。

**适用场景：** 先确定数据层级和角色，再实现/配置模型，连接视图和选择模型；编辑时同时实现 flags、setData 和对应通知；结构变化严格成对调用 begin/end。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要在 `data()` 中修改数据或做长时间阻塞操作；不要混用 DisplayRole、EditRole 和 UserRole；不要保存没有稳定生命周期保证的索引；不要用 reset 掩盖本可以精确描述的局部变化。

## 2. 依赖与对象关系

- 头文件：`#include <QModelIndex>`
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

先确定数据层级和角色，再实现/配置模型，连接视图和选择模型；编辑时同时实现 flags、setData 和对应通知；结构变化严格成对调用 begin/end。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

```cpp
// 视图通过 QModelIndex 和 role 查询模型。
const QVariant value = model->data(index, Qt::DisplayRole);
// 数据变化时由模型发出 dataChanged 或 begin/end 结构通知。
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QModelIndex()`
- `int column() const`
- `const void * constInternalPointer() const`
- `QVariant data(int role = Qt::DisplayRole) const`
- `Qt::ItemFlags flags() const`
- `quintptr internalId() const`
- `void * internalPointer() const`
- `bool isValid() const`
- `const QAbstractItemModel * model() const`
- `(since 6.0) void multiData(QModelRoleDataSpan roleDataSpan) const`
- `QModelIndex parent() const`
- `int row() const`
- `QModelIndex sibling(int row, int column) const`
- `QModelIndex siblingAtColumn(int column) const`
- `QModelIndex siblingAtRow(int row) const`

### 相关非成员函数

- `QModelIndexList`
- `bool operator!=(const QModelIndex &lhs, const QModelIndex &rhs)`
- `bool operator<(const QModelIndex &lhs, const QModelIndex &rhs)`
- `bool operator==(const QModelIndex &lhs, const QModelIndex &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[constexpr noexcept] QModelIndex::QModelIndex()`

**作用与语义：**

创建一个新的空模型索引。这种类型的模型索引用于表示模型中的位置无效。

### `[constexpr noexcept] int QModelIndex::column() const`

**作用与语义：**

返回该模型索引所指的列。

### `[noexcept] const void *QModelIndex::constInternalPointer() const`

**作用与语义：**

返回模型用来关联索引与内部数据结构的`const void` `*`指针。

### `QVariant QModelIndex::data(int role = Qt::DisplayRole) const`

**作用与语义：**

返回索引所指项目的给定`role`数据，或如果该模型索引`invalid`，则返回默认构造的`QVariant`。

### `Qt::ItemFlags QModelIndex::flags() const`

**作用与语义：**

返回索引所指项的标志。

### `[constexpr noexcept] quintptr QModelIndex::internalId() const`

**作用与语义：**

返回模型用来关联索引与内部数据结构的`quintptr`。

### `[noexcept] void *QModelIndex::internalPointer() const`

**作用与语义：**

返回模型用于将索引与内部数据结构关联的`void` `*`指针。

### `[constexpr noexcept] bool QModelIndex::isValid() const`

**作用与语义：**

如果该模型索引有效，则返回`true`;否则返回`false`。
有效的索引属于模型，且行号和列号均为非负数。

### `[constexpr noexcept] const QAbstractItemModel *QModelIndex::model() const`

**作用与语义：**

返回一个指向该索引所指项的模型的指针。
返回模型的const指针是因为调用模型的非const函数可能会导致模型索引失效，甚至导致应用崩溃。

### `[since 6.0] void QModelIndex::multiData(QModelRoleDataSpan roleDataSpan) const`

**作用与语义：**

填充索引所指项目的给定`roleDataSpan`。

### `QModelIndex QModelIndex::parent() const`

**作用与语义：**

返回模型索引的父级，若无父级则返回`QModelIndex()`。

### `[constexpr noexcept] int QModelIndex::row() const`

**作用与语义：**

返回该模型索引所指的行。

### `QModelIndex QModelIndex::sibling(int row, int column) const`

**作用与语义：**

返回`row`和 `column` 的兄弟姐妹。如果该位置没有兄弟姐妹，则返回无效`QModelIndex`。

### `QModelIndex QModelIndex::siblingAtColumn(int column) const`

**作用与语义：**

返回当前行`column`的兄弟节点。如果该位置没有兄弟节点，则返回无效`QModelIndex`。

### `QModelIndex QModelIndex::siblingAtRow(int row) const`

**作用与语义：**

返回当前列`row`的兄弟节点。如果该位置没有兄弟节点，则返回无效`QModelIndex`。

### `QModelIndexList`

**作用与语义：**

`QList`的同义词<`QModelIndex`>。

### `[constexpr noexcept] bool operator!=(const QModelIndex &lhs, const QModelIndex &rhs)`

**作用与语义：**

如果 `lhs` 模型索引不指向与 `rhs` 模型索引相同的位置，则返回 `true`；否则返回 `false`。

### `[constexpr noexcept] bool operator<(const QModelIndex &lhs, const QModelIndex &rhs)`

**作用与语义：**

返回`true`如果`lhs`模型索引小于`rhs`模型索引；否则返回`false`小于计算对开发者没有直接用处——不同父类的索引之间的比较方式未定义。这个运算符仅存在，以便该类可以用于`QMap`.

### `[constexpr noexcept] bool operator==(const QModelIndex &lhs, const QModelIndex &rhs)`

**作用与语义：**

如果 `lhs` 模型索引引用与 `rhs` 模型索引相同的位置，则返回 `true`；否则返回 `false`。 内部数据指针、行、列和模型值在与另一个模型索引比较时使用。

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

`QModelIndex` 所属机制类型：模型/视图协议。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
