# QRangeModelAdapter

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“Range模型Adapter”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QRangeModelAdapter` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QRangeModelAdapter>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `(preliminary) struct ColumnIterator`
- `(preliminary) struct ConstColumnIterator`
- `(preliminary) struct ConstRowIterator`
- `(preliminary) struct ConstRowReference`
- `(preliminary) struct DataReference`
- `(preliminary) struct RowIterator`
- `(preliminary) struct RowReference`
- `(preliminary) struct RowReferenceBase`

### 公有函数

- `QRangeModelAdapter(Range &&range)`
- `QRangeModelAdapter(Range &&range, Protocol &&protocol)`
- `void assign(NewRange &&newRange)`
- `void assign(std::initializer_list<Row> newRange)`
- `void assign(InputIterator first, Sentinel last)`
- `auto at(QSpan<const int> path)`
- `auto at(int listRow)`
- `auto at(int tableRow)`
- `auto at(int treeRow)`
- `decltype(auto) at(QSpan<const int> path) const`
- `auto at(int listRow) const`
- `decltype(auto) at(int tableRow) const`
- `auto at(QSpan<const int> path, int column)`
- `auto at(int tableRow, int column)`
- `auto at(QSpan<const int> path, int column) const`
- `auto at(int tableRow, int column) const`
- `int columnCount() const`
- `QVariant data(int listRow) const`
- `QVariant data(QSpan<const int> path, int column) const`
- `QVariant data(int listRow, int role) const`
- `QVariant data(int tableRow, int column) const`
- `QVariant data(QSpan<const int> path, int column, int role) const`
- `QVariant data(int tableRow, int column, int role) const`
- `bool hasChildren(QSpan<const int> row) const`
- `bool hasChildren(int row) const`
- `QModelIndex index(int listRow) const`
- `QModelIndex index(QSpan<const int> path, int column) const`
- `QModelIndex index(int tableRow, int column) const`
- `bool insertColumn(int before)`
- `bool insertColumn(int before, D &&data)`
- `bool insertColumns(int before, C &&data)`
- `bool insertRow(QSpan<const int> before)`
- `bool insertRow(int before)`
- `bool insertRow(QSpan<const int> before, D &&data)`
- `bool insertRow(int before, D &&data)`
- `bool insertRows(QSpan<const int> before, C &&data)`
- `bool insertRows(int before, C &&data)`
- `Model * model() const`
- `bool moveColumn(int from, int to)`
- `bool moveColumns(int from, int count, int to)`
- `bool moveRow(QSpan<const int> source, QSpan<const int> destination)`
- `bool moveRow(int source, int destination)`
- `bool moveRows(QSpan<const int> source, int count, QSpan<const int> destination)`
- `bool moveRows(int source, int count, int destination)`
- `const QRangeModelAdapter<Range, Protocol, Model>::range_type & range() const`
- `bool removeColumn(int column)`
- `bool removeColumns(int column, int count)`
- `bool removeRow(QSpan<const int> path)`
- `bool removeRow(int row)`
- `bool removeRows(QSpan<const int> path, int count)`
- `bool removeRows(int row, int count)`
- `int rowCount() const`
- `int rowCount(QSpan<const int> row) const`
- `int rowCount(int row) const`
- `bool setData(int listRow, const QVariant &value, int role = Qt::EditRole)`
- `bool setData(QSpan<const int> path, int column, const QVariant &value, int role = Qt::EditRole)`
- `bool setData(int tableRow, int column, const QVariant &value, int role = Qt::EditRole)`
- `QRangeModelAdapter<Range, Protocol, Model> & operator=(NewRange &&newRange)`
- `QRangeModelAdapter<Range, Protocol, Model> & operator=(std::initializer_list<Row> newRange)`
- `auto operator[](QSpan<const int> path)`
- `auto operator[](int listRow)`
- `auto operator[](int tableRow)`
- `auto operator[](int treeRow)`
- `decltype(auto) operator[](QSpan<const int> path) const`
- `auto operator[](int listRow) const`
- `decltype(auto) operator[](int tableRow) const`

### 相关非成员函数

- `bool operator!=(const QRangeModelAdapter<Range, Protocol, Model> &lhs, const QRangeModelAdapter<Range, Protocol, Model> &rhs)`
- `bool operator==(const QRangeModelAdapter<Range, Protocol, Model> &lhs, const QRangeModelAdapter<Range, Protocol, Model> &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[default] QRangeModelAdapter::QRangeModelAdapter(Range &&range)`

**作用与语义：**

构造一个在`range`上操作的`QRangeModelAdapter`。对于树范围，可选`protocol`将用于树的遍历。
请参阅`QRangeModel`构造器文档，了解`Range`需求详情，以及`range`的值类别如何改变适配器、型号和范围之间的相互作用。

### `template < typename NewRange = QRangeModelAdapter<Range, Protocol, Model>::range_type, QRangeModelAdapter<Range, Protocol, Model>::if_assignable_range<NewRange> = true, QRangeModelAdapter<Range, Protocol, Model>::unless_adapter<NewRange> = true > QRangeModelAdapter<Range, Protocol, Model> &QRangeModelAdapter::operator=(NewRange &&newRange)`

**作用与语义：**

用`newRange`中的行替换模型内容，可能使用移动语义。
该功能使`model()`发出`modelAboutToBeReset()`信号，`modelReset()`信号。
仅在`Range`可变且`newRange`可分配给`Range`但不能分配给`QRangeModelAdapter`时参与超载解析。

### `template <typename Row, QRangeModelAdapter<Range, Protocol, Model>::if_assignable_range<std::initializer_list<Row>> = true> QRangeModelAdapter<Range, Protocol, Model> &QRangeModelAdapter::operator=(std::initializer_list<Row> newRange)`

**作用与语义：**

用`newRange`中的行替换模型内容。
仅在`Range`可变且`newRange`可分配给`Range`时才参与超载解析。

### `template < typename InputIterator, typename Sentinel, typename I, QRangeModelAdapter<Range, Protocol, Model>::if_writable<I> = true > void QRangeModelAdapter::assign(InputIterator first, Sentinel last)`

**作用与语义：**

用`newRange`中的行替换模型内容，可能使用移动语义。
该功能使`model()`发出`modelAboutToBeReset()`信号，`modelReset()`信号。
仅在`Range`可变且`newRange`可分配给`Range`但不能分配给`QRangeModelAdapter`时参与超载解析。

### `template < typename I, QRangeModelAdapter<Range, Protocol, Model>::if_tree<I> = true, QRangeModelAdapter<Range, Protocol, Model>::if_writable<I> = true > auto QRangeModelAdapter::operator[](QSpan<const int> path)`

**作用与语义：**

返回一个可变的包装器，包含对 `path` 指定的树行的引用。
要修改树行，需赋值为其。赋入新树行会将新树行的父节点设置为旧树行的父节点。但旧树行和新树行都必须没有子行。访问树行时，使用`operator*()`取消引用包装器，或使用`operator->()`访问树行成员。
注意：对范围进行修改将使包装器失效。
只有当`Range`是树时才参与超载解析。

### `template < typename I, QRangeModelAdapter<Range, Protocol, Model>::if_list<I> = true, QRangeModelAdapter<Range, Protocol, Model>::if_writable<I> = true > auto QRangeModelAdapter::operator[](int listRow)`

**作用与语义：**

返回一个可变的 `Range` 存储值的引用。
注意：对该范围的修改将使该引用失效。要修改该引用，需为其分配一个新值。除非`Range`中存储的值是指针，否则无法访问存储值中的单个成员。
只有当`Range`是可变列表时才参与超载解析。

### `template < typename I, QRangeModelAdapter<Range, Protocol, Model>::if_table<I> = true, QRangeModelAdapter<Range, Protocol, Model>::if_writable<I> = true > auto QRangeModelAdapter::operator[](int tableRow)`

**作用与语义：**

返回 `tableRow` 处行的引用封装器，存储在 `Range` 中。
仅当 是可变表时`Range` 才参与超载解析，但不是树。

### `template < typename I, QRangeModelAdapter<Range, Protocol, Model>::if_tree<I> = true, QRangeModelAdapter<Range, Protocol, Model>::if_writable<I> = true > auto QRangeModelAdapter::operator[](int treeRow)`

**作用与语义：**

返回 `treeRow` 行的引用包装器，存储在 `Range` 中。
要修改树行，给它赋值。赋入新树行会将新树行的父节点设置为旧树行的父节点。但旧树行和新树行都必须没有子行。访问树行时，使用`operator*()`反引用包装器，或使用`operator->()`访问树行成员。
注意：对范围进行修改将使包装器失效。
只有当`Range`是树时才参与超载解析。

### `template <typename I, QRangeModelAdapter<Range, Protocol, Model>::if_tree<I> = true> decltype(auto) QRangeModelAdapter::operator[](QSpan<const int> path) const`

**作用与语义：**

返回`path`指定的行的常量引用，存储在`Range`中。
只有当`Range`是树时才参与超载解析。

### `template <typename I, QRangeModelAdapter<Range, Protocol, Model>::if_list<I> = true> auto QRangeModelAdapter::operator[](int listRow) const`

**作用与语义：**

返回`listRow`的值，作为存储在`Range`中的类型。
只有当`Range`是列表时才参与超载解析。

### `template <typename I, QRangeModelAdapter<Range, Protocol, Model>::unless_list<I> = true> decltype(auto) QRangeModelAdapter::operator[](int tableRow) const`

**作用与语义：**

返回对`tableRow`行的常量引用，存储在`Range`中。
仅在`Range`为表或树时参与超载解析。

### `template < typename I, QRangeModelAdapter<Range, Protocol, Model>::if_tree<I> = true, QRangeModelAdapter<Range, Protocol, Model>::if_writable<I> = true > auto QRangeModelAdapter::at(QSpan<const int> path, int column)`

**作用与语义：**

返回一个可变的包装器，包含对 `path` 指定的树行的引用。
要修改树行，需赋值为其。赋入新树行会将新树行的父节点设置为旧树行的父节点。但旧树行和新树行都必须没有子行。访问树行时，使用`operator*()`取消引用包装器，或使用`operator->()`访问树行成员。
注意：对范围进行修改将使包装器失效。
只有当`Range`是树时才参与超载解析。

### `template < typename I, QRangeModelAdapter<Range, Protocol, Model>::unless_list<I> = true, QRangeModelAdapter<Range, Protocol, Model>::if_writable<I> = true > auto QRangeModelAdapter::at(int tableRow, int column)`

**作用与语义：**

返回一个可变的 `Range` 存储值的引用。
注意：对该范围的修改将使该引用失效。要修改该引用，需为其分配一个新值。除非`Range`中存储的值是指针，否则无法访问存储值中的单个成员。
只有当`Range`是可变列表时才参与超载解析。

### `template <typename I, QRangeModelAdapter<Range, Protocol, Model>::if_tree<I> = true> auto QRangeModelAdapter::at(QSpan<const int> path, int column) const`

**作用与语义：**

返回 `tableRow` 处行的引用封装器，存储在 `Range` 中。
仅当 是可变表时`Range` 才参与超载解析，但不是树。

### `template <typename I, QRangeModelAdapter<Range, Protocol, Model>::unless_list<I> = true> auto QRangeModelAdapter::at(int tableRow, int column) const`

**作用与语义：**

返回 `treeRow` 行的引用包装器，存储在 `Range` 中。
要修改树行，给它赋值。赋入新树行会将新树行的父节点设置为旧树行的父节点。但旧树行和新树行都必须没有子行。访问树行时，使用`operator*()`反引用包装器，或使用`operator->()`访问树行成员。
注意：对范围进行修改将使包装器失效。
只有当`Range`是树时才参与超载解析。

### `int QRangeModelAdapter::columnCount() const`

**作用与语义：**

返回列数。如果`Range`代表列表，则返回列数，否则返回每行的元素数。

### `template <typename I, QRangeModelAdapter<Range, Protocol, Model>::if_list<I> = true> QVariant QRangeModelAdapter::data(int listRow, int role) const`

**作用与语义：**

返回`listRow`时该项在给定`role`下存储的数据的`QVariant`，若无项则返回无效`QVariant`。如果未指定`role`，则返回包含完整项的`QVariant`。
只有当`Range`是列表时才参与超载解析。

### `template <typename I, QRangeModelAdapter<Range, Protocol, Model>::if_tree<I> = true> QVariant QRangeModelAdapter::data(QSpan<const int> path, int column, int role) const`

**作用与语义：**

返回`listRow`时该项在给定`role`下存储的数据的`QVariant`，若无项则返回无效`QVariant`。如果未指定`role`，则返回包含完整项的`QVariant`。
只有当`Range`是列表时才参与超载解析。

### `template <typename I, QRangeModelAdapter<Range, Protocol, Model>::unless_list<I> = true> QVariant QRangeModelAdapter::data(int tableRow, int column, int role) const`

**作用与语义：**

返回一个`QVariant`，存储`path`和`column`所指项目在给定`role`下存储的数据;如果该位置或角色没有数据存储，则返回无效`QVariant`。如果未指定`role`，则返回一个包含完整项目的`QVariant`。
只有当`Range`是树时才参与重载决议。

### `[constexpr] template <typename I, QRangeModelAdapter<Range, Protocol, Model>::if_tree<I> = true> bool QRangeModelAdapter::hasChildren(QSpan<const int> row) const`

**作用与语义：**

返回是否有行在`row`下。
只有当`Range`是树时才参与超载解析。

### `template <typename I, QRangeModelAdapter<Range, Protocol, Model>::if_list<I> = true> QModelIndex QRangeModelAdapter::index(int listRow) const`

**作用与语义：**

`listRow`还了`QModelIndex`。
只有当`Range`是一维列表时，才参与超载解析。

### `template <typename I, QRangeModelAdapter<Range, Protocol, Model>::if_tree<I> = true> QModelIndex QRangeModelAdapter::index(QSpan<const int> path, int column) const`

**作用与语义：**

返回树中`path`指定的行的 位于 `column` 项的 `QModelIndex`。
只有当`Range`是树时才参与重载决议。

### `template <typename I, QRangeModelAdapter<Range, Protocol, Model>::unless_list<I> = true> QModelIndex QRangeModelAdapter::index(int tableRow, int column) const`

**作用与语义：**

`tableRow`，`column`时退还该物品的 `QModelIndex`。
只有当`Range`是表或树时才参与超载解析。

### `template <typename I, QRangeModelAdapter<Range, Protocol, Model>::if_canInsertColumns<I> = true> bool QRangeModelAdapter::insertColumn(int before)`

**作用与语义：**

在所有行中插入一个空列`before`，并返回插入是否成功。如果`before`与`columnCount()`值相同，则该列将附加到每行。
只有当`Range`有支持插入元素的行时，才参与重载决议。

### `template < typename D, typename I, QRangeModelAdapter<Range, Protocol, Model>::if_canInsertColumns<I> = true, QRangeModelAdapter<Range, Protocol, Model>::if_compatible_column_data<D> = true > bool QRangeModelAdapter::insertColumn(int before, D &&data)`

**作用与语义：**

在`before`指定的列之前，从`data`构成的单一列插入到所有行中，并返回插入是否成功。如果`before`与`columnCount()`值相同，则该列将附加到每一行。
如果 `data` 是一个单一值，那么所有行的新条目都将由该单一值构造出来。
如果`data`是容器，则该容器中的元素将依次用于构造后续行的列。如果`data`中的元素少于行数，函数会绕行并从第一个元素重新开始。
只有当`Range`有支持插入元素的行，且元素可以从`data`中的元素构成时，才参与超载解析。

### `template < typename C, typename I, QRangeModelAdapter<Range, Protocol, Model>::if_canInsertColumns<I> = true, QRangeModelAdapter<Range, Protocol, Model>::if_compatible_column_range<C> = true > bool QRangeModelAdapter::insertColumns(int before, C &&data)`

**作用与语义：**

将由`before` `data`中元素构成的列插入所有行，并返回插入是否成功。如果`before`与`columnCount()`值相同，则该列将附加到每行。
如果`data`中的元素是值，那么所有行的新条目都会由这些值构造出来。
如果`data`中的元素是容器，那么外层容器中的元素将依次用于构造每一行的新元素。如果`data`中的元素少于行数，则函数会绕行并从第一个元素重新开始。
只有当`Range`有支持插入元素的行，并且可以从`data`中的元素构造时，才参与超载解析。

### `template < typename I, QRangeModelAdapter<Range, Protocol, Model>::if_canInsertRows<I> = true, QRangeModelAdapter<Range, Protocol, Model>::if_tree<I> = true > bool QRangeModelAdapter::insertRow(QSpan<const int> before)`

**作用与语义：**

在`before`指定路径的行前插入一行空行，返回插入是否成功。如果`before`与`rowCount()`值相同，则会附加新行。
只有当`Range`是支持元素插入的树时，才参与超载解析。

### `template <typename I, QRangeModelAdapter<Range, Protocol, Model>::if_canInsertRows<I> = true> bool QRangeModelAdapter::insertRow(int before)`

**作用与语义：**

在`before`行前插入一行空行，返回插入是否成功。如果`before`与`rowCount()`值相同，则将添加新行。
仅在支持元素插入`Range`参与超载解析。

### `template < typename D, typename I, QRangeModelAdapter<Range, Protocol, Model>::if_canInsertRows<I> = true, QRangeModelAdapter<Range, Protocol, Model>::if_compatible_row<D> = true, QRangeModelAdapter<Range, Protocol, Model>::if_tree<I> = true > bool QRangeModelAdapter::insertRow(QSpan<const int> before, D &&data)`

**作用与语义：**

在`before`的行之前插入一行由`data`构造的单行，并返回插入是否成功。如果`before`与`rowCount()`值相同，则将附加新行。
只有当`Range`是支持元素插入的树，并且可以由`data`构造行时，才参与超载解析。

### `template < typename D, typename I, QRangeModelAdapter<Range, Protocol, Model>::if_canInsertRows<I> = true, QRangeModelAdapter<Range, Protocol, Model>::if_compatible_row<D> = true > bool QRangeModelAdapter::insertRow(int before, D &&data)`

**作用与语义：**

在`before`的行之前插入由`data`构造的单行，并返回插入是否成功。如果`before`与`rowCount()`值相同，则将添加新行。
只有当`Range`支持元素插入且行可以由`data`构造时，才参与超载解析。

### `template < typename C, typename I, QRangeModelAdapter<Range, Protocol, Model>::if_canInsertRows<I> = true, QRangeModelAdapter<Range, Protocol, Model>::if_compatible_row_range<C> = true, QRangeModelAdapter<Range, Protocol, Model>::if_tree<I> = true > bool QRangeModelAdapter::insertRows(QSpan<const int> before, C &&data)`

**作用与语义：**

插入由`before` `data`中元素构成的行，并返回插入是否成功。如果`before`与`rowCount()`值相同，则将添加新行。
只有当`Range`是支持元素插入的树状结构，并且可以从`data`中的元素构造行时，才参与超载解析。

### `template < typename C, typename I, QRangeModelAdapter<Range, Protocol, Model>::if_canInsertRows<I> = true, QRangeModelAdapter<Range, Protocol, Model>::if_compatible_row_range<C> = true > bool QRangeModelAdapter::insertRows(int before, C &&data)`

**作用与语义：**

插入由`before` `data`中元素构成的行，并返回插入是否成功。如果`before`与`rowCount()`值相同，则将附加新行。
仅在`Range`支持元素插入且能从`data`中的元素构成行时，才参与超载解析。

### `Model *QRangeModelAdapter::model() const`

**作用与语义：**

返回由该适配器创建的`QRangeModel`实例。

### `template <typename F, QRangeModelAdapter<Range, Protocol, Model>::if_canMoveItems<F> = true> bool QRangeModelAdapter::moveColumn(int from, int to)`

**作用与语义：**

将`from`的列移动到`to`的列，并返回该列是否成功移动。
只有当`Range`有支持元素移动的行时，才参与超载解析。

### `template <typename F, QRangeModelAdapter<Range, Protocol, Model>::if_canMoveItems<F> = true> bool QRangeModelAdapter::moveColumns(int from, int count, int to)`

**作用与语义：**

`count`从`from`开始的列移动到`to`的位置，并返回列是否成功移动。
只有当`Range`有支持元素移动的行时，才参与重载决议。

### `template < typename I, typename F, QRangeModelAdapter<Range, Protocol, Model>::if_canMoveItems<F> = true, QRangeModelAdapter<Range, Protocol, Model>::if_tree<I> = true > bool QRangeModelAdapter::moveRow(QSpan<const int> source, QSpan<const int> destination)`

**作用与语义：**

将树枝移至树枝`source`至`destination`位置，并返回枝条是否成功移动。
只有当`Range`是支持元素移动的树时，才参与超载解析。

### `template <typename F, QRangeModelAdapter<Range, Protocol, Model>::if_canMoveItems<F> = true> bool QRangeModelAdapter::moveRow(int source, int destination)`

**作用与语义：**

将`source`行移动到`destination`的位置，并返回是否成功移动该行。
只有在`Range`支持元素移动时才参与超载解析。

### `template < typename I, typename F, QRangeModelAdapter<Range, Protocol, Model>::if_canMoveItems<F> = true, QRangeModelAdapter<Range, Protocol, Model>::if_tree<I> = true > bool QRangeModelAdapter::moveRows(QSpan<const int> source, int count, QSpan<const int> destination)`

**作用与语义：**

`count`从`source`开始的树枝移动到`destination`的位置，并返回是否成功移动了这些行。
仅当`Range`是支持元素移动的树时，才参与超载解析。

### `template <typename F, QRangeModelAdapter<Range, Protocol, Model>::if_canMoveItems<F> = true> bool QRangeModelAdapter::moveRows(int source, int count, int destination)`

**作用与语义：**

`count`从`source`开始的行移动到`destination`的位置，并返回是否成功移动了这些行。
只有在`Range`支持元素移动时才参与重载决议。

### `const QRangeModelAdapter<Range, Protocol, Model>::range_type &QRangeModelAdapter::range() const`

**作用与语义：**

返回模型适配器所工作的范围的const引用。

### `template <typename I, QRangeModelAdapter<Range, Protocol, Model>::if_canRemoveColumns<I> = true> bool QRangeModelAdapter::removeColumn(int column)`

**作用与语义：**

从每行中移除给定`column`，并返回移除是否成功。
只有当`Range`行支持移除元素时，才参与超载解析。

### `template <typename I, QRangeModelAdapter<Range, Protocol, Model>::if_canRemoveColumns<I> = true> bool QRangeModelAdapter::removeColumns(int column, int count)`

**作用与语义：**

从每行移除以给定`column`为起始的`count`列，并返回移除是否成功。
只有当`Range`行支持移除元素时，才参与超载解析。

### `template < typename I, QRangeModelAdapter<Range, Protocol, Model>::if_canRemoveRows<I> = true, QRangeModelAdapter<Range, Protocol, Model>::if_tree<I> = true > bool QRangeModelAdapter::removeRow(QSpan<const int> path)`

**作用与语义：**

删除给定`path`的行，包括该行的所有子节点，并返回移除是否成功。
只有当`Range`树支持元素移除时，才参与超载解析。

### `template <typename I, QRangeModelAdapter<Range, Protocol, Model>::if_canRemoveRows<I> = true> bool QRangeModelAdapter::removeRow(int row)`

**作用与语义：**

移除给定的`row`并返回移除是否成功。
只有在`Range`支持移除元素时才参与超载解析。

### `template < typename I, QRangeModelAdapter<Range, Protocol, Model>::if_canRemoveRows<I> = true, QRangeModelAdapter<Range, Protocol, Model>::if_tree<I> = true > bool QRangeModelAdapter::removeRows(QSpan<const int> path, int count)`

**作用与语义：**

移除`path`指定行起始的`count`行，并返回移除是否成功。
只有当`Range`树支持元素移除时，才参与超载解析。

### `template <typename I, QRangeModelAdapter<Range, Protocol, Model>::if_canRemoveRows<I> = true> bool QRangeModelAdapter::removeRows(int row, int count)`

**作用与语义：**

从`row`开始移除`count`行，并返回移除是否成功。
只有在`Range`支持移除元素时才参与超载解析。

### `int QRangeModelAdapter::rowCount() const`

**作用与语义：**

返回行数。如果`Range`代表列表或表，则为行数。对于树，这是顶层行数。

### `template <typename I, QRangeModelAdapter<Range, Protocol, Model>::if_tree<I> = true> int QRangeModelAdapter::rowCount(QSpan<const int> row) const`

**作用与语义：**

返回`row`下的行数。
只有当`Range`是树时才参与超载解析。

### `template < typename I, QRangeModelAdapter<Range, Protocol, Model>::if_list<I> = true, QRangeModelAdapter<Range, Protocol, Model>::if_writable<I> = true > bool QRangeModelAdapter::setData(int listRow, const QVariant &value, int role = Qt::EditRole)`

**作用与语义：**

将`listRow`项的`role`数据设置为`value`。
成功时返回`true`;否则返回`false`。
只有当`Range`为可变列表时才参与超载解析。

### `template < typename I, QRangeModelAdapter<Range, Protocol, Model>::if_tree<I> = true, QRangeModelAdapter<Range, Protocol, Model>::if_writable<I> = true > bool QRangeModelAdapter::setData(QSpan<const int> path, int column, const QVariant &value, int role = Qt::EditRole)`

**作用与语义：**

将`path`和`column`所提及项目的 `role` 数据设置为 `value`。
成功时返回`true`;否则返回`false`。
只有当 是可变树时`Range`才参与重载决议。

### `template < typename I, QRangeModelAdapter<Range, Protocol, Model>::unless_list<I> = true, QRangeModelAdapter<Range, Protocol, Model>::if_writable<I> = true > bool QRangeModelAdapter::setData(int tableRow, int column, const QVariant &value, int role = Qt::EditRole)`

**作用与语义：**

将`tableRow`和`column`所提及项目的 `role` 数据设置为 `value`。
成功时返回`true`;否则返回`false`。
只有当`Range`可变时才参与超载解析，而非列表。

### `[noexcept] bool operator!=(const QRangeModelAdapter<Range, Protocol, Model> &lhs, const QRangeModelAdapter<Range, Protocol, Model> &rhs)`

**作用与语义：**

返回`lhs`是否等于`rhs`。如果两个适配器都承载相同的 `model`实例，则它们相等。

### `[noexcept] bool operator==(const QRangeModelAdapter<Range, Protocol, Model> &lhs, const QRangeModelAdapter<Range, Protocol, Model> &rhs)`

**作用与语义：**

返回`lhs`是否等于`rhs`。如果两个适配器都承载同一个`model`实例，则称它们相等。

### `(preliminary) struct ColumnIterator`

**作用与语义：**

在模型行的列上提供一个STL风格的非const迭代器。
迭代器模型`std::random_access_iterator`。反引用迭代器返回模型中指向项处的值的 `DataReference` 封装器。

### `(preliminary) struct ConstColumnIterator`

**作用与语义：**

在模型行的列上提供一个STL风格的非const迭代器。
迭代器模型`std::random_access_iterator`。反参照迭代器返回模型中指向项的const值。

### `(preliminary) struct ConstRowIterator`

**作用与语义：**

提供一个STL风格的const迭代器，覆盖模型的各行。
迭代器建模时`std::random_access_iterator`。如果模型是一个列表，那么反参照迭代器会返回模型中指向的项。
对于表和树，迭代器取消引用会返回指向行的`ConstRowReference`。

### `(preliminary) struct ConstRowReference`

**作用与语义：**

ConstRowReference 是 QRangeModel 中 const 行的引用包装器。
对于表或树的范围，使用`at()`或下标算符[]的const重载访问`QRangeModelAdapter`行，或通过反引用`ConstRowIterator`，返回指定行的ConstRowReference。

### `(preliminary) struct DataReference`

**作用与语义：**

DataReference 是 QRangeModel 中环绕项目的引用包装器。
使用`at()`、下标运算符[]等非const超载访问模型中的项目，或取消引用非const `iterator`，都会返回模型中该项目的DataReference包装器。
赋值到该引用包装器会通过`QAbstractItemModel` API改变模型中的数据。
该值本身的const版本可以通过`get()`或算符>()访问。
与`std::reference_wrapper`不同，将一个DataReference分配给另一个DataReference并不会重新绑定引用，而是通过复制语义设置值。

**官方示例：**

```cpp
 adapter[0] = newValue;
```

### `(preliminary) struct RowIterator`

**作用与语义：**

提供一个STL风格的非const迭代器，覆盖模型的各行。
迭代器模型`std::random_access_iterator`。如果模型是一个列表，那么去引用迭代器会返回模型中指向项的 `DataReference` 包装器。
对于表和树，迭代子取消引用会返回指向行的`RowReference`。

### `(preliminary) struct RowReference`

**作用与语义：**

RowReference 是 QRangeModel 中环绕行的引用包装器。
对于表或树的范围，使用`at()`或下标算子[]的非const超载访问`QRangeModelAdapter`行，或通过反引用`RowIterator`，返回指定行的行引用。

### `(preliminary) struct RowReferenceBase`

**作用与语义：**

RowReferenceBase 为 RowReference 和 ConstRowReference 提供了通用的 API。
对于表或树模型，使用`at()`、下标算子[]或取消`RowIterator`引用该行访问适配器的行，会返回指定行的`RowReference`或`ConstRowReference`。

### `QRangeModelAdapter(Range &&range, Protocol &&protocol)`

**作用与语义：**

构造一个在`range`上操作的`QRangeModelAdapter`。对于树范围，可选`protocol`将用于树的遍历。
请参阅`QRangeModel`构造器文档，了解`Range`需求详情，以及`range`的值类别如何改变适配器、型号和范围之间的相互作用。

### `void assign(NewRange &&newRange)`

**作用与语义：**

用`newRange`中的行替换模型内容。
仅在`Range`可变且`newRange`可分配给`Range`时才参与超载解析。

### `void assign(std::initializer_list<Row> newRange)`

**作用与语义：**

用 [`first`， `last` ] 中的行替换模型的内容。

### `auto at(QSpan<const int> path)`

**作用与语义：**

返回`path`指定的行的常量引用，存储在`Range`中。
只有当`Range`是树时才参与超载解析。

### `auto at(int listRow)`

**作用与语义：**

返回`listRow`的值，作为存储在`Range`中的类型。
只有当`Range`是列表时才参与超载解析。

### `auto at(int tableRow)`

**作用与语义：**

返回对`tableRow`行的常量引用，存储在`Range`中。
仅在`Range`为表或树时参与超载解析。

### `auto at(int treeRow)`

**作用与语义：**

返回一个可变的引用，指向由`path`和`column`指定为物品的值。如果该项是多功能项，则该项将引用整个项。如果`Range`中的行在不同列存储不同类型，则返回类型为`QVariant`。
注意：对该范围的修改将使该引用失效。要修改该引用，需为其分配一个新值。除非`Range`中存储的值是指针，否则无法访问存储值中的单个成员。
仅当 是可变树时`Range`才参与超载解析。

### `decltype(auto) at(QSpan<const int> path) const`

**作用与语义：**

返回一个可变的引用，即`tableRow`和`column`指定为物品的值。如果该物品是多功能物品，则该引用将指向整个物品。
注意：对该范围的修改将使该引用失效。要修改该引用，需赋值一个新值。除非`Range`中存储的值是指针，否则无法访问存储值中的单个成员。
只有当 `Range` 是可变表时，才参与超载解析。

### `auto at(int listRow) const`

**作用与语义：**

返回`path`和`column`指定为物品的值副本。如果该物品是多功能物品，则返回整个物品的副本。如果`Range`中的行在不同列存储不同类型，则返回类型为`QVariant`。
只有当`Range`是树时才参与超载解析。

### `decltype(auto) at(int tableRow) const`

**作用与语义：**

返回由`tableRow`和`column`指定为物品的值副本。如果该物品是多功能物品，则返回整个物品的副本。如果`Range`中的行在不同列存储不同类型，则返回类型为`QVariant`。
只有当`Range`是表或树时才参与超载解析。

### `QVariant data(int listRow) const`

**作用与语义：**

返回一个`QVariant`，存储`path`和`column`所指项目在给定`role`下存储的数据;如果该位置或角色没有数据存储，则返回无效`QVariant`。如果未指定`role`，则返回一个包含完整项目的`QVariant`。
只有当`Range`是树时才参与重载决议。

### `QVariant data(QSpan<const int> path, int column) const`

**作用与语义：**

返回一个`QVariant`，存储`tableRow`和`column`所指项目的指定`role`下的数据;如果该位置或角色没有数据，则返回无效`QVariant`。如果未指定`role`，则返回一个包含完整项目的`QVariant`。
仅在`Range`为表或树时参与超载解析。

### `QVariant data(int tableRow, int column) const`

**作用与语义：**

返回一个`QVariant`，存储`tableRow`和`column`所指项目的指定`role`下的数据;如果该位置或角色没有数据，则返回无效`QVariant`。如果未指定`role`，则返回一个包含完整项目的`QVariant`。
仅在`Range`为表或树时参与超载解析。

### `bool hasChildren(int row) const`

**作用与语义：**

返回是否有行在`row`下。
只有当`Range`是树时才参与超载解析。

### `int rowCount(int row) const`

**作用与语义：**

返回`row`下的行数。
只有当`Range`是树时才参与超载解析。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QRangeModelAdapter` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
