# QItemSelection

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QItemSelection` 是 模型/视图协议 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QItemSelection` 是 模型/视图协议 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 视图不直接读取业务容器，而是通过 `QModelIndex`、行列坐标和数据角色向模型查询。模型必须维护索引、父子层级、角色数据以及插入/删除/移动/重置通知；代理模型则在索引映射、排序和过滤之间维护另一层关系。

**适用场景：** 先确定数据层级和角色，再实现/配置模型，连接视图和选择模型；编辑时同时实现 flags、setData 和对应通知；结构变化严格成对调用 begin/end。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要在 `data()` 中修改数据或做长时间阻塞操作；不要混用 DisplayRole、EditRole 和 UserRole；不要保存没有稳定生命周期保证的索引；不要用 reset 掩盖本可以精确描述的局部变化。

## 2. 依赖与对象关系

- 头文件：`#include <QItemSelection>`
- 继承自：QList
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

- `QItemSelection()`
- `QItemSelection(const QModelIndex &topLeft, const QModelIndex &bottomRight)`
- `bool contains(const QModelIndex &index) const`
- `QModelIndexList indexes() const`
- `void merge(const QItemSelection &other, QItemSelectionModel::SelectionFlags command)`
- `void select(const QModelIndex &topLeft, const QModelIndex &bottomRight)`

### 静态公有成员

- `void split(const QItemSelectionRange &range, const QItemSelectionRange &other, QItemSelection *result)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[default] QItemSelection::QItemSelection()`

**作用与语义：**

构造一个空选择。

### `QItemSelection::QItemSelection(const QModelIndex &topLeft, const QModelIndex &bottomRight)`

**作用与语义：**

构建一个从左上角模型项（由`topLeft`索引指定）延伸到右下角（由`bottomRight`指定）的项选择。

### `bool QItemSelection::contains(const QModelIndex &index) const`

**作用与语义：**

如果选择包含给定`index`，返回`true`;否则返回`false`。

### `QModelIndexList QItemSelection::indexes() const`

**作用与语义：**

返回对应所选项目的模型索引列表。

### `void QItemSelection::merge(const QItemSelection &other, QItemSelectionModel::SelectionFlags command)`

**作用与语义：**

利用给定的 `command`将`other`选择与该 `QItemSelection`合并。该方法保证没有范围重叠。
请注意，仅支持`QItemSelectionModel::Select`、`QItemSelectionModel::Deselect`和`QItemSelectionModel::Toggle`。

### `void QItemSelection::select(const QModelIndex &topLeft, const QModelIndex &bottomRight)`

**作用与语义：**

将从左上角的模型项（由`topLeft`索引指定）到右下角的项（由`bottomRight`指定）添加到列表中。
注意：`topLeft`和`bottomRight`必须有同一个父母。

### `[static] void QItemSelection::split(const QItemSelectionRange &range, const QItemSelectionRange &other, QItemSelection *result)`

**作用与语义：**

利用选择`other`范围将选择区间`range`拆分。从`range`中移除`other`中的所有项，并将结果归入`result`。这可以与集合的减法运算语义进行比较。

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

`QItemSelection` 所属机制类型：模型/视图协议。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
