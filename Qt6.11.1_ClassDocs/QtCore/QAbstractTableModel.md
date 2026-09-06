# QAbstractTableModel

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QAbstractTableModel` 是 模型/视图协议 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QAbstractTableModel` 是 Qt Core 中的抽象协议类型，通常通过具体子类、模型、插件或工厂来使用。

**内部模型：** 抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

**适用场景：** 当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。

**典型调用链：** 选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

**先记住的坑：** 不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

## 2. 依赖与对象关系

- 头文件：`#include <QAbstractTableModel>`
- 继承自：QAbstractItemModel
- 直接派生类：QSqlQueryModel

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

### 状态、生命周期和线程

**生命周期：** 模型应比视图活得足够久，视图销毁时不会自动替业务容器释放资源。模型变化必须使用对应的 begin/end 协议或精确通知，不能只改容器后期待视图自行发现。取到的 QModelIndex 只在模型允许的生命周期内有效。

**状态与结果：** 区分当前索引、选择模型、编辑状态、数据角色和模型结构变化。`dataChanged` 表示已有项目的数据变化，行列插入/删除表示结构变化，`modelReset` 会让旧索引整体失效。

**线程与事件循环：** 模型通常在 GUI 线程被视图访问。后台线程不要直接修改正在显示的模型；应在正确线程汇总数据，再通过通知协议更新，或使用线程安全的数据交换层。

## 3. 直接使用

当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。 使用时通常按这个过程组织：选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

```cpp
// 视图通过 QModelIndex 和 role 查询模型。
const QVariant value = model->data(index, Qt::DisplayRole);
// 数据变化时由模型发出 dataChanged 或 begin/end 结构通知。
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QAbstractTableModel(QObject *parent = nullptr)`
- `virtual ~QAbstractTableModel()`

### 重实现的公有函数

- `virtual bool dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent) override`
- `virtual Qt::ItemFlags flags(const QModelIndex &index) const override`
- `virtual QModelIndex index(int row, int column, const QModelIndex &parent = QModelIndex()) const override`
- `virtual QModelIndex sibling(int row, int column, const QModelIndex &idx) const override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QAbstractTableModel::QAbstractTableModel(QObject *parent = nullptr)`

**作用与语义：**

为给定`parent`构造一个抽象表模型。

### `[virtual noexcept] QAbstractTableModel::~QAbstractTableModel()`

**作用与语义：**

它破坏了抽象表模型。

### `[override virtual] bool QAbstractTableModel::dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent)`

**作用与语义：**

Reimplementation s： `QAbstractItemModel::dropMimeData`（const QMimeData *data， Qt：:D ropAction action， int row， int column， const QModelIndex &parent）.
处理拖放操作提供的`data`，拖拽操作以给定`action`结束。
如果数据和动作由模型处理，返回`true`;否则返回`false`。
指定的`row`、`column`和`parent`表示操作结束时该项在模型中的位置。模型有责任在正确的位置完成动作。
例如，`QTreeView`中物品的投放动作可能导致新物品入，要么作为`row`、`column`和`parent`指定的物品的子项，要么作为该物品的兄弟姐妹。
当`row`和`column`为-1时，意味着丢弃的数据应被视为直接丢弃`parent`。通常这意味着将数据作为`parent`的子项附加。如果`row`和`column`大于或等于零，则表示丢弃发生在指定`parent`中指定的`row`和`column`之前。
调用`mimeTypes()`成员以获取可接受的MIME类型列表。该默认实现假设`mimeTypes()`的默认实现，返回单一默认MIME类型。如果你在自定义模型中重新实现`mimeTypes()`以返回多个MIME类型，必须重新实现该函数以利用它们。

### `[override virtual] Qt::ItemFlags QAbstractTableModel::flags(const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractItemModel::flags`（const QModelIndex & index） const.
返回给定`index`的物品标志。
基类实现返回一组标志组合，使该项（`ItemIsEnabled`）启用并允许选择（`ItemIsSelectable`）。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] QModelIndex QAbstractTableModel::index(int row, int column, const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

重实现自：`QAbstractItemModel::index`（整数行，整数列，cont QModelIndex 和 parent） const.
返回`row`和`column`中的数据索引，并与`parent`。
返回由给定`row`、`column`和`parent`索引指定的模型中项目的索引。
在子类中重新实现该函数时，调用 `createIndex()` 生成模型索引，其他组件可以用来引用模型中的项目。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[override virtual] QModelIndex QAbstractTableModel::sibling(int row, int column, const QModelIndex &idx) const`

**作用与语义：**

重构：`QAbstractItemModel::sibling`（整数行，整数列，const QModelIndex & index）const.
`row`时退回兄弟姐妹，`index` `column`物品，或者如果该地点没有兄弟姐妹，则`QModelIndex`无效。
sibling() 只是一个方便函数，它会找到该项的父项，并用它检索指定`row`和`column`中子项的索引。
该方法可选择性地覆盖以实现特定优化。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

## 6. 深入实践与常见坑

### 生命周期和资源边界

模型应比视图活得足够久，视图销毁时不会自动替业务容器释放资源。模型变化必须使用对应的 begin/end 协议或精确通知，不能只改容器后期待视图自行发现。取到的 QModelIndex 只在模型允许的生命周期内有效。

### 状态和错误边界

区分当前索引、选择模型、编辑状态、数据角色和模型结构变化。`dataChanged` 表示已有项目的数据变化，行列插入/删除表示结构变化，`modelReset` 会让旧索引整体失效。

### 线程边界

模型通常在 GUI 线程被视图访问。后台线程不要直接修改正在显示的模型；应在正确线程汇总数据，再通过通知协议更新，或使用线程安全的数据交换层。

### 最容易出现的错误

不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QAbstractTableModel` 所属机制类型：模型/视图协议。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
