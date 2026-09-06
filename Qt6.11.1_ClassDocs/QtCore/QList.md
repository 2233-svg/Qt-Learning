# QList

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QList` 是 Qt 容器类型，负责保存一组元素，并提供插入、删除、查找、遍历和容量管理。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QList` 是 Qt 容器与隐式共享机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt 容器负责元素的存储、访问、遍历和修改。部分容器使用隐式共享，复制容器时可能共享数据，写操作时发生 detach；这会降低按值传递成本，但也会影响迭代器、引用、指针和修改时的性能。

**适用场景：** 先选择连续序列、关联映射、哈希表还是队列，再决定按索引、迭代器或范围遍历；批量修改时预留容量并注意 detach，跨 API 传值时确认元素类型和所有权。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要在容器修改后继续使用旧迭代器；不要在范围 for 中改变会导致迭代器失效的容器；不要误以为隐式共享等于线程安全；不要忽略 QHash/QMap/QList 的顺序和复杂度差异。

## 2. 依赖与对象关系

- 头文件：`#include <QList>`
- 继承自：未在类页中列出
- 直接派生类：QBluetoothServiceInfo::Alternative、QBluetoothServiceInfo::Sequence、QByteArrayList、QItemSelection、QMqttUserProperties、QNdefMessage、QPolygon、QPolygonF、QQueue、QSignalSpy、QStack、QStringList、QTestEventList、QVector、QVulkanInfoVector,、QXmlStreamAttributes

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

Qt 容器负责元素的存储、访问、遍历和修改。部分容器使用隐式共享，复制容器时可能共享数据，写操作时发生 detach；这会降低按值传递成本，但也会影响迭代器、引用、指针和修改时的性能。

### 状态、生命周期和线程

**生命周期：** 容器自己管理元素存储，容器销毁后由它提供的迭代器、引用和 data 指针通常失效。修改容器可能重新分配或 detach，不能把元素地址和迭代器当成长期句柄。

**状态与结果：** 要区分空容器、容量、元素数量、查找失败和默认构造值。插入/删除可能改变索引和迭代器；关联容器还要考虑键唯一性、排序和查找复杂度。

**线程与事件循环：** 不同线程使用各自的容器副本通常安全；同一个容器一边读一边写仍需要同步，即使底层采用隐式共享也不会自动解决数据竞争。

## 3. 直接使用

先选择连续序列、关联映射、哈希表还是队列，再决定按索引、迭代器或范围遍历；批量修改时预留容量并注意 detach，跨 API 传值时确认元素类型和所有权。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

```cpp
#include <QList>

QList<int> values{1, 2, 3};
values.append(4);
for (const int value : values) {
    // 使用 value
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `class const_iterator`
- `class iterator`
- `ConstIterator`
- `Iterator`
- `const_pointer`
- `const_reference`
- `const_reverse_iterator`
- `difference_type`
- `parameter_type`
- `pointer`
- `reference`
- `reverse_iterator`
- `rvalue_ref`
- `size_type`
- `value_type`

### 公有函数

- `QList()`
- `QList(qsizetype size)`
- `QList(std::initializer_list<T> args)`
- `QList(InputIterator first, InputIterator last)`
- `QList(qsizetype size, QList<T>::parameter_type value)`
- `(since 6.8) QList(qsizetype size, Qt::Initialization)`
- `QList(const QList<T> &other)`
- `QList(QList<T> &&other)`
- `~QList()`
- `void append(QList<T>::parameter_type value)`
- `(since 6.0) void append(QList<T> &&value)`
- `void append(QList<T>::rvalue_ref value)`
- `void append(const QList<T> &value)`
- `(since 6.6) QList<T> & assign(std::initializer_list<T> l)`
- `(since 6.6) QList<T> & assign(InputIterator first, InputIterator last)`
- `(since 6.6) QList<T> & assign(qsizetype n, QList<T>::parameter_type t)`
- `QList<T>::const_reference at(qsizetype i) const`
- `QList<T>::reference back()`
- `QList<T>::const_reference back() const`
- `QList<T>::iterator begin()`
- `QList<T>::const_iterator begin() const`
- `qsizetype capacity() const`
- `QList<T>::const_iterator cbegin() const`
- `QList<T>::const_iterator cend() const`
- `void clear()`
- `QList<T>::const_iterator constBegin() const`
- `QList<T>::const_pointer constData() const`
- `QList<T>::const_iterator constEnd() const`
- `const T & constFirst() const`
- `const T & constLast() const`
- `bool contains(const AT &value) const`
- `qsizetype count(const AT &value) const`
- `qsizetype count() const`
- `QList<T>::const_reverse_iterator crbegin() const`
- `QList<T>::const_reverse_iterator crend() const`
- `QList<T>::pointer data()`
- `QList<T>::const_pointer data() const`
- `QList<T>::iterator emplace(qsizetype i, Args &&... args)`
- `QList<T>::iterator emplace(QList<T>::const_iterator before, Args &&... args)`
- `QList<T>::reference emplaceBack(Args &&... args)`
- `QList<T>::reference emplace_back(Args &&... args)`
- `bool empty() const`
- `QList<T>::iterator end()`
- `QList<T>::const_iterator end() const`
- `bool endsWith(QList<T>::parameter_type value) const`
- `QList<T>::iterator erase(QList<T>::const_iterator pos)`
- `QList<T>::iterator erase(QList<T>::const_iterator begin, QList<T>::const_iterator end)`
- `QList<T> & fill(QList<T>::parameter_type value, qsizetype size = -1)`
- `T & first()`
- `(since 6.0) QList<T> first(qsizetype n) const`
- `const T & first() const`
- `QList<T>::reference front()`
- `QList<T>::const_reference front() const`
- `qsizetype indexOf(const AT &value, qsizetype from = 0) const`
- `QList<T>::iterator insert(qsizetype i, QList<T>::parameter_type value)`
- `QList<T>::iterator insert(qsizetype i, QList<T>::rvalue_ref value)`
- `QList<T>::iterator insert(QList<T>::const_iterator before, qsizetype count, QList<T>::parameter_type value)`
- `QList<T>::iterator insert(QList<T>::const_iterator before, QList<T>::parameter_type value)`
- `QList<T>::iterator insert(QList<T>::const_iterator before, QList<T>::rvalue_ref value)`
- `QList<T>::iterator insert(qsizetype i, qsizetype count, QList<T>::parameter_type value)`
- `bool isEmpty() const`
- `T & last()`
- `(since 6.0) QList<T> last(qsizetype n) const`
- `const T & last() const`
- `qsizetype lastIndexOf(const AT &value, qsizetype from = -1) const`
- `qsizetype length() const`
- `(since 6.8) qsizetype max_size() const`
- `QList<T> mid(qsizetype pos, qsizetype length = -1) const`
- `void move(qsizetype from, qsizetype to)`
- `void pop_back()`
- `void pop_front()`
- `void prepend(QList<T>::parameter_type value)`
- `void prepend(QList<T>::rvalue_ref value)`
- `void push_back(QList<T>::parameter_type value)`
- `void push_back(QList<T>::rvalue_ref value)`
- `void push_front(QList<T>::parameter_type value)`
- `void push_front(QList<T>::rvalue_ref value)`
- `QList<T>::reverse_iterator rbegin()`
- `QList<T>::const_reverse_iterator rbegin() const`
- `void remove(qsizetype i, qsizetype n = 1)`
- `qsizetype removeAll(const AT &t)`
- `void removeAt(qsizetype i)`
- `void removeFirst()`
- `(since 6.1) qsizetype removeIf(Predicate pred)`
- `void removeLast()`
- `bool removeOne(const AT &t)`
- `QList<T>::reverse_iterator rend()`
- `QList<T>::const_reverse_iterator rend() const`
- `void replace(qsizetype i, QList<T>::parameter_type value)`
- `void replace(qsizetype i, QList<T>::rvalue_ref value)`
- `void reserve(qsizetype size)`
- `(since 6.0) void resize(qsizetype size)`
- `(since 6.0) void resize(qsizetype size, QList<T>::parameter_type c)`
- `(since 6.8) void resizeForOverwrite(qsizetype size)`
- `void shrink_to_fit()`
- `qsizetype size() const`
- `(since 6.0) QList<T> sliced(qsizetype pos, qsizetype n) const`
- `(since 6.0) QList<T> sliced(qsizetype pos) const`
- `void squeeze()`
- `bool startsWith(QList<T>::parameter_type value) const`
- `void swap(QList<T> &other)`
- `void swapItemsAt(qsizetype i, qsizetype j)`
- `T takeAt(qsizetype i)`
- `QList<T>::value_type takeFirst()`
- `QList<T>::value_type takeLast()`
- `T value(qsizetype i) const`
- `T value(qsizetype i, QList<T>::parameter_type defaultValue) const`
- `bool operator!=(const QList<T> &other) const`
- `QList<T> operator+(QList<T> &&other) &&`
- `QList<T> operator+(const QList<T> &other) &&`
- `QList<T> operator+(QList<T> &&other) const &`
- `QList<T> operator+(const QList<T> &other) const &`
- `QList<T> & operator+=(const QList<T> &other)`
- `(since 6.0) QList<T> & operator+=(QList<T> &&other)`
- `QList<T> & operator+=(QList<T>::parameter_type value)`
- `QList<T> & operator+=(QList<T>::rvalue_ref value)`
- `bool operator<(const QList<T> &other) const`
- `QList<T> & operator<<(QList<T>::parameter_type value)`
- `QList<T> & operator<<(const QList<T> &other)`
- `(since 6.0) QList<T> & operator<<(QList<T> &&other)`
- `QList<T> & operator<<(QList<T>::rvalue_ref value)`
- `bool operator<=(const QList<T> &other) const`
- `QList<T> & operator=(QList<T> &&other)`
- `QList<T> & operator=(const QList<T> &other)`
- `QList<T> & operator=(std::initializer_list<T> args)`
- `bool operator==(const QList<T> &other) const`
- `bool operator>(const QList<T> &other) const`
- `bool operator>=(const QList<T> &other) const`
- `QList<T>::reference operator[](qsizetype i)`
- `QList<T>::const_reference operator[](qsizetype i) const`

### 静态公有成员

- `(since 6.8) qsizetype maxSize()`

### 相关非成员函数

- `(since 6.1) qsizetype erase(QList<T> &list, const AT &t)`
- `(since 6.1) qsizetype erase_if(QList<T> &list, Predicate pred)`
- `size_t qHash(const QList<T> &key, size_t seed = 0)`
- `QDataStream & operator<<(QDataStream &out, const QList<T> &list)`
- `(since 6.9) auto operator<=>(const QList<T> &lhs, const QList<T> &rhs)`
- `QDataStream & operator>>(QDataStream &in, QList<T> &list)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 163 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[alias] QList::ConstIterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QList` 的配置属性。初始化或状态切换时通过 `setConstIterator(...)` 设置，之后用 `ConstIterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:ConstIterator`。
- 属性名：`QList`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QList::Iterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QList` 的配置属性。初始化或状态切换时通过 `setIterator(...)` 设置，之后用 `Iterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:Iterator`。
- 属性名：`QList`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QList::const_pointer`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QList` 的配置属性。初始化或状态切换时通过 `setConst_pointer(...)` 设置，之后用 `const_pointer()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:const_pointer`。
- 属性名：`QList`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QList::const_reference`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QList` 的配置属性。初始化或状态切换时通过 `setConst_reference(...)` 设置，之后用 `const_reference()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:const_reference`。
- 属性名：`QList`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QList::const_reverse_iterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QList` 的配置属性。初始化或状态切换时通过 `setConst_reverse_iterator(...)` 设置，之后用 `const_reverse_iterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:const_reverse_iterator`。
- 属性名：`QList`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QList::difference_type`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QList` 的配置属性。初始化或状态切换时通过 `setDifference_type(...)` 设置，之后用 `difference_type()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:difference_type`。
- 属性名：`QList`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QList::pointer`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QList` 的配置属性。初始化或状态切换时通过 `setPointer(...)` 设置，之后用 `pointer()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:pointer`。
- 属性名：`QList`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QList::reference`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QList` 的配置属性。初始化或状态切换时通过 `setReference(...)` 设置，之后用 `reference()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:reference`。
- 属性名：`QList`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QList::reverse_iterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QList` 的配置属性。初始化或状态切换时通过 `setReverse_iterator(...)` 设置，之后用 `reverse_iterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:reverse_iterator`。
- 属性名：`QList`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QList::size_type`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QList` 的配置属性。初始化或状态切换时通过 `setSize_type(...)` 设置，之后用 `size_type()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:size_type`。
- 属性名：`QList`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QList::value_type`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QList` 的配置属性。初始化或状态切换时通过 `setValue_type(...)` 设置，之后用 `value_type()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:value_type`。
- 属性名：`QList`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QList::QList()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QList` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QList::QList(qsizetype size)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QList` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList::QList(std::initializer_list<T> args)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QList` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `args`：类型为 `std::initializer_list<T>`。没有默认值，调用时必须提供。传入 `std::initializer_list<T>` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename InputIterator, QList<T>::if_input_iterator<InputIterator> = true> QList::QList(InputIterator first, InputIterator last)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QList` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `first`：类型为 `InputIterator`。没有默认值，调用时必须提供。传入 `InputIterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `last`：类型为 `InputIterator`。没有默认值，调用时必须提供。传入 `InputIterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList::QList(qsizetype size, QList<T>::parameter_type value)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QList` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。
- 参数 `value`：类型为 `QList<T>::parameter_type`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] QList::QList(qsizetype size, Qt::Initialization)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QList` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。
- 参数 `Initialization`：类型为 `Qt::`。没有默认值，调用时必须提供。传入 `Qt::` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[default] QList::QList(const QList<T> &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QList` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QList<T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[default] QList::QList(QList<T> &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QList` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `QList<T> &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[default] QList::~QList()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QList` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QList::append(QList<T>::parameter_type value)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QList` 添加依赖、数据或子对象的 API `append`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `value`：类型为 `QList<T>::parameter_type`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] void QList::append(QList<T> &&value)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QList` 添加依赖、数据或子对象的 API `append`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `value`：类型为 `QList<T> &&`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QList::append(QList<T>::rvalue_ref value)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QList` 添加依赖、数据或子对象的 API `append`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `value`：类型为 `QList<T>::rvalue_ref`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QList::append(const QList<T> &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QList` 添加依赖、数据或子对象的 API `append`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `value`：类型为 `const QList<T> &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] QList<T> &QList::assign(std::initializer_list<T> l)`

**API 类别：** 成员函数说明

**中文解读：** `QList::assign` 用于计算、查询或取得与“assign”相关的操作。调用时要先确认当前状态和 `l` 的有效范围；返回类型是 `QList<T> &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T> &`。
- 参数 `l`：类型为 `std::initializer_list<T>`。没有默认值，调用时必须提供。传入 `std::initializer_list<T>` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] template <typename InputIterator, QList<T>::if_input_iterator<InputIterator> = true> QList<T> &QList::assign(InputIterator first, InputIterator last)`

**API 类别：** 成员函数说明

**中文解读：** `QList::assign` 用于计算、查询或取得与“assign”相关的操作。调用时要先确认当前状态和 `first`、`last` 的有效范围；返回类型是 `template <typename InputIterator, QList<T>::if_input_iterator<InputIterator> = true> QList<T> &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename InputIterator, QList<T>::if_input_iterator<InputIterator> = true> QList<T> &`。
- 参数 `first`：类型为 `InputIterator`。没有默认值，调用时必须提供。传入 `InputIterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `last`：类型为 `InputIterator`。没有默认值，调用时必须提供。传入 `InputIterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] QList<T> &QList::assign(qsizetype n, QList<T>::parameter_type t)`

**API 类别：** 成员函数说明

**中文解读：** `QList::assign` 用于计算、查询或取得与“assign”相关的操作。调用时要先确认当前状态和 `n`、`t` 的有效范围；返回类型是 `QList<T> &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T> &`。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `t`：类型为 `QList<T>::parameter_type`。没有默认值，调用时必须提供。传入 `QList<T>::parameter_type` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QList<T>::const_reference QList::at(qsizetype i) const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `at`，用于取得 `QList` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`QList<T>::const_reference`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T>::reference QList::back()`

**API 类别：** 成员函数说明

**中文解读：** `QList::back` 用于计算、查询或取得与“末尾”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<T>::reference`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T>::reference`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QList<T>::const_reference QList::back() const`

**API 类别：** 成员函数说明

**中文解读：** `QList::back` 用于计算、查询或取得与“末尾”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<T>::const_reference`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T>::const_reference`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T>::iterator QList::begin()`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `begin`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QList<T>::iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QList<T>::const_iterator QList::begin() const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `begin`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QList<T>::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QList::capacity() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `capacity`，返回 `QList` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QList<T>::const_iterator QList::cbegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QList::cbegin` 用于计算、查询或取得与“cbegin”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<T>::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T>::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QList<T>::const_iterator QList::cend() const`

**API 类别：** 成员函数说明

**中文解读：** `QList::cend` 用于计算、查询或取得与“cend”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<T>::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T>::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QList::clear()`

**API 类别：** 成员函数说明

**中文解读：** 这是状态清理或重置 API `clear`。调用后原有数据、索引、缓存或绑定可能失效；使用前先确认它影响的是当前对象、子对象还是底层共享资源，之后重新检查状态。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QList<T>::const_iterator QList::constBegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QList::constBegin` 用于计算、查询或取得与“const、起始位置”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<T>::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T>::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QList<T>::const_pointer QList::constData() const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `constData`，用于取得 `QList` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`QList<T>::const_pointer`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QList<T>::const_iterator QList::constEnd() const`

**API 类别：** 成员函数说明

**中文解读：** `QList::constEnd` 用于计算、查询或取得与“const、结束”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<T>::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T>::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] const T &QList::constFirst() const`

**API 类别：** 成员函数说明

**中文解读：** `QList::constFirst` 用于计算、查询或取得与“const、首项”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const T &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const T &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] const T &QList::constLast() const`

**API 类别：** 成员函数说明

**中文解读：** `QList::constLast` 用于计算、查询或取得与“const、末项”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const T &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const T &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] template <typename AT> bool QList::contains(const AT &value) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `contains`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`template <typename AT> bool`。
- 参数 `value`：类型为 `const AT &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] template <typename AT = T> qsizetype QList::count(const AT &value) const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `count`，返回 `QList` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`template <typename AT = T> qsizetype`。
- 参数 `value`：类型为 `const AT &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] qsizetype QList::count() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `count`，返回 `QList` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QList<T>::const_reverse_iterator QList::crbegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QList::crbegin` 用于计算、查询或取得与“crbegin”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<T>::const_reverse_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T>::const_reverse_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QList<T>::const_reverse_iterator QList::crend() const`

**API 类别：** 成员函数说明

**中文解读：** `QList::crend` 用于计算、查询或取得与“crend”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<T>::const_reverse_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T>::const_reverse_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T>::pointer QList::data()`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `data`，用于取得 `QList` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`QList<T>::pointer`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QList<T>::const_pointer QList::data() const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `data`，用于取得 `QList` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`QList<T>::const_pointer`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename... Args> QList<T>::iterator QList::emplace(qsizetype i, Args &&... args)`

**API 类别：** 成员函数说明

**中文解读：** `QList::emplace` 用于计算、查询或取得与“emplace”相关的操作。调用时要先确认当前状态和 `i`、`args` 的有效范围；返回类型是 `template <typename... Args> QList<T>::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename... Args> QList<T>::iterator`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `args`：类型为 `Args &&...`。没有默认值，调用时必须提供。传入 `Args &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename... Args> QList<T>::iterator QList::emplace(QList<T>::const_iterator before, Args &&... args)`

**API 类别：** 成员函数说明

**中文解读：** `QList::emplace` 用于计算、查询或取得与“emplace”相关的操作。调用时要先确认当前状态和 `before`、`args` 的有效范围；返回类型是 `template <typename... Args> QList<T>::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename... Args> QList<T>::iterator`。
- 参数 `before`：类型为 `QList<T>::const_iterator`。没有默认值，调用时必须提供。传入 `QList<T>::const_iterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `args`：类型为 `Args &&...`。没有默认值，调用时必须提供。传入 `Args &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename... Args> QList<T>::reference QList::emplace_back(Args &&... args)`

**API 类别：** 成员函数说明

**中文解读：** `QList::emplace_back` 用于计算、查询或取得与“emplace、末尾”相关的操作。调用时要先确认当前状态和 `args` 的有效范围；返回类型是 `template <typename... Args> QList<T>::reference`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename... Args> QList<T>::reference`。
- 参数 `args`：类型为 `Args &&...`。没有默认值，调用时必须提供。传入 `Args &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool QList::empty() const`

**API 类别：** 成员函数说明

**中文解读：** `QList::empty` 用于计算、查询或取得与“空状态”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T>::iterator QList::end()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `end`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QList<T>::iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QList<T>::const_iterator QList::end() const`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `end`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QList<T>::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QList::endsWith(QList<T>::parameter_type value) const`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `endsWith`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`bool`。
- 参数 `value`：类型为 `QList<T>::parameter_type`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T>::iterator QList::erase(QList<T>::const_iterator pos)`

**API 类别：** 成员函数说明

**中文解读：** `QList::erase` 用于计算、查询或取得与“erase”相关的操作。调用时要先确认当前状态和 `pos` 的有效范围；返回类型是 `QList<T>::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T>::iterator`。
- 参数 `pos`：类型为 `QList<T>::const_iterator`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T>::iterator QList::erase(QList<T>::const_iterator begin, QList<T>::const_iterator end)`

**API 类别：** 成员函数说明

**中文解读：** `QList::erase` 用于计算、查询或取得与“erase”相关的操作。调用时要先确认当前状态和 `begin`、`end` 的有效范围；返回类型是 `QList<T>::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T>::iterator`。
- 参数 `begin`：类型为 `QList<T>::const_iterator`。没有默认值，调用时必须提供。传入 `QList<T>::const_iterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `end`：类型为 `QList<T>::const_iterator`。没有默认值，调用时必须提供。传入 `QList<T>::const_iterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T> &QList::fill(QList<T>::parameter_type value, qsizetype size = -1)`

**API 类别：** 成员函数说明

**中文解读：** `QList::fill` 用于计算、查询或取得与“fill”相关的操作。调用时要先确认当前状态和 `value`、`size` 的有效范围；返回类型是 `QList<T> &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T> &`。
- 参数 `value`：类型为 `QList<T>::parameter_type`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。
- 参数 `size`：类型为 `qsizetype`。默认值为 `-1`。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T &QList::first()`

**API 类别：** 成员函数说明

**中文解读：** `QList::first` 用于计算、查询或取得与“首项”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `T &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`T &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QList<T> QList::first(qsizetype n) const`

**API 类别：** 成员函数说明

**中文解读：** `QList::first` 用于计算、查询或取得与“首项”相关的操作。调用时要先确认当前状态和 `n` 的有效范围；返回类型是 `QList<T>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T>`。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] const T &QList::first() const`

**API 类别：** 成员函数说明

**中文解读：** `QList::first` 用于计算、查询或取得与“首项”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const T &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const T &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T>::reference QList::front()`

**API 类别：** 成员函数说明

**中文解读：** `QList::front` 用于计算、查询或取得与“开头”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<T>::reference`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T>::reference`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QList<T>::const_reference QList::front() const`

**API 类别：** 成员函数说明

**中文解读：** `QList::front` 用于计算、查询或取得与“开头”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<T>::const_reference`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T>::const_reference`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] template <typename AT> qsizetype QList::indexOf(const AT &value, qsizetype from = 0) const`

**API 类别：** 成员函数说明

**中文解读：** `QList::indexOf` 用于计算、查询或取得与“索引、Of”相关的操作。调用时要先确认当前状态和 `value`、`from` 的有效范围；返回类型是 `template <typename AT> qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename AT> qsizetype`。
- 参数 `value`：类型为 `const AT &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。
- 参数 `from`：类型为 `qsizetype`。默认值为 `0`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T>::iterator QList::insert(qsizetype i, QList<T>::rvalue_ref value)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QList` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QList<T>::iterator`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `QList<T>::rvalue_ref`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T>::iterator QList::insert(QList<T>::const_iterator before, qsizetype count, QList<T>::parameter_type value)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QList` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QList<T>::iterator`。
- 参数 `before`：类型为 `QList<T>::const_iterator`。没有默认值，调用时必须提供。传入 `QList<T>::const_iterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `QList<T>::parameter_type`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T>::iterator QList::insert(QList<T>::const_iterator before, QList<T>::rvalue_ref value)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QList` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QList<T>::iterator`。
- 参数 `before`：类型为 `QList<T>::const_iterator`。没有默认值，调用时必须提供。传入 `QList<T>::const_iterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `QList<T>::rvalue_ref`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T>::iterator QList::insert(qsizetype i, qsizetype count, QList<T>::parameter_type value)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QList` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QList<T>::iterator`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `QList<T>::parameter_type`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] bool QList::isEmpty() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isEmpty`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T &QList::last()`

**API 类别：** 成员函数说明

**中文解读：** `QList::last` 用于计算、查询或取得与“末项”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `T &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`T &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QList<T> QList::last(qsizetype n) const`

**API 类别：** 成员函数说明

**中文解读：** `QList::last` 用于计算、查询或取得与“末项”相关的操作。调用时要先确认当前状态和 `n` 的有效范围；返回类型是 `QList<T>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T>`。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] const T &QList::last() const`

**API 类别：** 成员函数说明

**中文解读：** `QList::last` 用于计算、查询或取得与“末项”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const T &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const T &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] template <typename AT> qsizetype QList::lastIndexOf(const AT &value, qsizetype from = -1) const`

**API 类别：** 成员函数说明

**中文解读：** `QList::lastIndexOf` 用于计算、查询或取得与“末项、索引、Of”相关的操作。调用时要先确认当前状态和 `value`、`from` 的有效范围；返回类型是 `template <typename AT> qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename AT> qsizetype`。
- 参数 `value`：类型为 `const AT &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。
- 参数 `from`：类型为 `qsizetype`。默认值为 `-1`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] qsizetype QList::length() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `length`，返回 `QList` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static constexpr, since 6.8] qsizetype QList::maxSize()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `maxSize`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T> QList::mid(qsizetype pos, qsizetype length = -1) const`

**API 类别：** 成员函数说明

**中文解读：** `QList::mid` 用于计算、查询或取得与“mid”相关的操作。调用时要先确认当前状态和 `pos`、`length` 的有效范围；返回类型是 `QList<T>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T>`。
- 参数 `pos`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。
- 参数 `length`：类型为 `qsizetype`。默认值为 `-1`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QList::move(qsizetype from, qsizetype to)`

**API 类别：** 成员函数说明

**中文解读：** `QList::move` 用于执行与“移动”相关的操作。调用时要先确认当前状态和 `from`、`to` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `from`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `to`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QList::pop_back()`

**API 类别：** 成员函数说明

**中文解读：** `QList::pop_back` 用于执行与“pop、末尾”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QList::pop_front()`

**API 类别：** 成员函数说明

**中文解读：** `QList::pop_front` 用于执行与“pop、开头”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QList::prepend(QList<T>::rvalue_ref value)`

**API 类别：** 成员函数说明

**中文解读：** `QList::prepend` 用于执行与“前置追加”相关的操作。调用时要先确认当前状态和 `value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `value`：类型为 `QList<T>::rvalue_ref`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QList::push_back(QList<T>::parameter_type value)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QList` 添加依赖、数据或子对象的 API `push_back`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `value`：类型为 `QList<T>::parameter_type`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QList::push_back(QList<T>::rvalue_ref value)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QList` 添加依赖、数据或子对象的 API `push_back`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `value`：类型为 `QList<T>::rvalue_ref`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QList::push_front(QList<T>::rvalue_ref value)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QList` 添加依赖、数据或子对象的 API `push_front`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `value`：类型为 `QList<T>::rvalue_ref`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T>::reverse_iterator QList::rbegin()`

**API 类别：** 成员函数说明

**中文解读：** `QList::rbegin` 用于计算、查询或取得与“rbegin”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<T>::reverse_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T>::reverse_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QList<T>::const_reverse_iterator QList::rbegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QList::rbegin` 用于计算、查询或取得与“rbegin”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<T>::const_reverse_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T>::const_reverse_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QList::remove(qsizetype i, qsizetype n = 1)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `remove`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `n`：类型为 `qsizetype`。默认值为 `1`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename AT = T> qsizetype QList::removeAll(const AT &t)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeAll`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`template <typename AT = T> qsizetype`。
- 参数 `t`：类型为 `const AT &`。没有默认值，调用时必须提供。传入 `const AT &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QList::removeAt(qsizetype i)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeAt`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QList::removeFirst()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeFirst`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] template <typename Predicate> qsizetype QList::removeIf(Predicate pred)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeIf`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`template <typename Predicate> qsizetype`。
- 参数 `pred`：类型为 `Predicate`。没有默认值，调用时必须提供。传入 `Predicate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QList::removeLast()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeLast`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename AT = T> bool QList::removeOne(const AT &t)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeOne`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`template <typename AT = T> bool`。
- 参数 `t`：类型为 `const AT &`。没有默认值，调用时必须提供。传入 `const AT &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T>::reverse_iterator QList::rend()`

**API 类别：** 成员函数说明

**中文解读：** `QList::rend` 用于计算、查询或取得与“rend”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<T>::reverse_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T>::reverse_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QList<T>::const_reverse_iterator QList::rend() const`

**API 类别：** 成员函数说明

**中文解读：** `QList::rend` 用于计算、查询或取得与“rend”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<T>::const_reverse_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T>::const_reverse_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QList::replace(qsizetype i, QList<T>::rvalue_ref value)`

**API 类别：** 成员函数说明

**中文解读：** `QList::replace` 用于执行与“替换”相关的操作。调用时要先确认当前状态和 `i`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `QList<T>::rvalue_ref`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QList::reserve(qsizetype size)`

**API 类别：** 成员函数说明

**中文解读：** `QList::reserve` 用于执行与“reserve”相关的操作。调用时要先确认当前状态和 `size` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] void QList::resize(qsizetype size, QList<T>::parameter_type c)`

**API 类别：** 成员函数说明

**中文解读：** `QList::resize` 用于执行与“调整尺寸”相关的操作。调用时要先确认当前状态和 `size`、`c` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。
- 参数 `c`：类型为 `QList<T>::parameter_type`。没有默认值，调用时必须提供。传入 `QList<T>::parameter_type` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] void QList::resizeForOverwrite(qsizetype size)`

**API 类别：** 成员函数说明

**中文解读：** `QList::resizeForOverwrite` 用于执行与“调整尺寸、For、Overwrite”相关的操作。调用时要先确认当前状态和 `size` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QList::shrink_to_fit()`

**API 类别：** 成员函数说明

**中文解读：** `QList::shrink_to_fit` 用于执行与“shrink、转换输出、fit”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] qsizetype QList::size() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `size`，返回 `QList` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QList<T> QList::sliced(qsizetype pos, qsizetype n) const`

**API 类别：** 成员函数说明

**中文解读：** `QList::sliced` 用于计算、查询或取得与“sliced”相关的操作。调用时要先确认当前状态和 `pos`、`n` 的有效范围；返回类型是 `QList<T>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T>`。
- 参数 `pos`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QList<T> QList::sliced(qsizetype pos) const`

**API 类别：** 成员函数说明

**中文解读：** `QList::sliced` 用于计算、查询或取得与“sliced”相关的操作。调用时要先确认当前状态和 `pos` 的有效范围；返回类型是 `QList<T>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T>`。
- 参数 `pos`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QList::squeeze()`

**API 类别：** 成员函数说明

**中文解读：** `QList::squeeze` 用于执行与“squeeze”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QList::startsWith(QList<T>::parameter_type value) const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `startsWith`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`bool`。
- 参数 `value`：类型为 `QList<T>::parameter_type`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QList::swap(QList<T> &other)`

**API 类别：** 成员函数说明

**中文解读：** `QList::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QList<T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QList::swapItemsAt(qsizetype i, qsizetype j)`

**API 类别：** 成员函数说明

**中文解读：** `QList::swapItemsAt` 用于执行与“swap、Items、按位置访问”相关的操作。调用时要先确认当前状态和 `i`、`j` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `j`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QList::takeAt(qsizetype i)`

**API 类别：** 成员函数说明

**中文解读：** `QList::takeAt` 用于计算、查询或取得与“取出、按位置访问”相关的操作。调用时要先确认当前状态和 `i` 的有效范围；返回类型是 `T`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`T`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T>::value_type QList::takeFirst()`

**API 类别：** 成员函数说明

**中文解读：** `QList::takeFirst` 用于计算、查询或取得与“取出、首项”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<T>::value_type`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T>::value_type`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T>::value_type QList::takeLast()`

**API 类别：** 成员函数说明

**中文解读：** `QList::takeLast` 用于计算、查询或取得与“取出、末项”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<T>::value_type`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T>::value_type`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QList::value(qsizetype i) const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `value`，用于取得 `QList` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`T`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QList::value(qsizetype i, QList<T>::parameter_type defaultValue) const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `value`，用于取得 `QList` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`T`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `defaultValue`：类型为 `QList<T>::parameter_type`。没有默认值，调用时必须提供。传入 `QList<T>::parameter_type` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QList::operator!=(const QList<T> &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QList<T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T> QList::operator+(QList<T> &&other) &&`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QList<T>`。
- 参数 `other`：类型为 `QList<T> &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T> &QList::operator+=(const QList<T> &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QList<T> &`。
- 参数 `other`：类型为 `const QList<T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QList<T> &QList::operator+=(QList<T> &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QList<T> &`。
- 参数 `other`：类型为 `QList<T> &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T> &QList::operator+=(QList<T>::parameter_type value)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QList<T> &`。
- 参数 `value`：类型为 `QList<T>::parameter_type`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T> &QList::operator+=(QList<T>::rvalue_ref value)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QList<T> &`。
- 参数 `value`：类型为 `QList<T>::rvalue_ref`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QList::operator<(const QList<T> &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QList<T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T> &QList::operator<<(QList<T>::parameter_type value)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QList<T> &`。
- 参数 `value`：类型为 `QList<T>::parameter_type`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T> &QList::operator<<(const QList<T> &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QList<T> &`。
- 参数 `other`：类型为 `const QList<T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QList<T> &QList::operator<<(QList<T> &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QList<T> &`。
- 参数 `other`：类型为 `QList<T> &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T> &QList::operator<<(QList<T>::rvalue_ref value)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QList<T> &`。
- 参数 `value`：类型为 `QList<T>::rvalue_ref`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QList::operator<=(const QList<T> &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QList<T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[default] QList<T> &QList::operator=(QList<T> &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QList<T> &`。
- 参数 `other`：类型为 `QList<T> &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[default] QList<T> &QList::operator=(const QList<T> &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QList<T> &`。
- 参数 `other`：类型为 `const QList<T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T> &QList::operator=(std::initializer_list<T> args)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QList<T> &`。
- 参数 `args`：类型为 `std::initializer_list<T>`。没有默认值，调用时必须提供。传入 `std::initializer_list<T>` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QList::operator==(const QList<T> &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QList<T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QList::operator>(const QList<T> &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QList<T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QList::operator>=(const QList<T> &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QList<T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T>::reference QList::operator[](qsizetype i)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QList<T>::reference`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QList<T>::const_reference QList::operator[](qsizetype i) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QList<T>::const_reference`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] template <typename T, typename AT> qsizetype erase(QList<T> &list, const AT &t)`

**API 类别：** 相关非成员函数

**中文解读：** `QList::erase` 用于计算、查询或取得与“erase”相关的操作。调用时要先确认当前状态和 `list`、`t` 的有效范围；返回类型是 `template <typename T, typename AT> qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename T, typename AT> qsizetype`。
- 参数 `list`：类型为 `QList<T> &`。没有默认值，调用时必须提供。传入 `QList<T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `t`：类型为 `const AT &`。没有默认值，调用时必须提供。传入 `const AT &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] template <typename T, typename Predicate> qsizetype erase_if(QList<T> &list, Predicate pred)`

**API 类别：** 相关非成员函数

**中文解读：** `QList::erase_if` 用于计算、查询或取得与“erase、if”相关的操作。调用时要先确认当前状态和 `list`、`pred` 的有效范围；返回类型是 `template <typename T, typename Predicate> qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename T, typename Predicate> qsizetype`。
- 参数 `list`：类型为 `QList<T> &`。没有默认值，调用时必须提供。传入 `QList<T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pred`：类型为 `Predicate`。没有默认值，调用时必须提供。传入 `Predicate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept(...)] template <typename T> size_t qHash(const QList<T> &key, size_t seed = 0)`

**API 类别：** 相关非成员函数

**中文解读：** `QList::qHash` 用于计算、查询或取得与“q、Hash”相关的操作。调用时要先确认当前状态和 `key`、`seed` 的有效范围；返回类型是 `template <typename T> size_t`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename T> size_t`。
- 参数 `key`：类型为 `const QList<T> &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `seed`：类型为 `size_t`。默认值为 `0`。传入 `size_t` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename T> QDataStream &operator<<(QDataStream &out, const QList<T> &list)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template <typename T> QDataStream &`。
- 参数 `out`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `list`：类型为 `const QList<T> &`。没有默认值，调用时必须提供。传入 `const QList<T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] auto operator<=>(const QList<T> &lhs, const QList<T> &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`auto`。
- 参数 `lhs`：类型为 `const QList<T> &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QList<T> &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename T> QDataStream &operator>>(QDataStream &in, QList<T> &list)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template <typename T> QDataStream &`。
- 参数 `in`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `list`：类型为 `QList<T> &`。没有默认值，调用时必须提供。传入 `QList<T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `class const_iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QList` 暴露的类型声明 `const、iterator`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `class iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QList` 暴露的类型声明 `iterator`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `ConstIterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QList` 的 `Const、Iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QList` 的 `Iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const_pointer`

**API 类别：** 公有类型

**中文解读：** 这是 `QList` 的 `const、pointer` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const_reference`

**API 类别：** 公有类型

**中文解读：** 这是 `QList` 的 `const、reference` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const_reverse_iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QList` 的 `const、reverse、iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `difference_type`

**API 类别：** 公有类型

**中文解读：** 这是 `QList` 的 `difference、类型` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `parameter_type`

**API 类别：** 公有类型

**中文解读：** 这是 `QList` 的 `parameter、类型` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `pointer`

**API 类别：** 公有类型

**中文解读：** 这是 `QList` 的 `pointer` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `reference`

**API 类别：** 公有类型

**中文解读：** 这是 `QList` 的 `reference` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `reverse_iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QList` 的 `reverse、iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `rvalue_ref`

**API 类别：** 公有类型

**中文解读：** 这是 `QList` 的 `rvalue、ref` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `size_type`

**API 类别：** 公有类型

**中文解读：** 这是 `QList` 的 `尺寸或数量、类型` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `value_type`

**API 类别：** 公有类型

**中文解读：** 这是 `QList` 的 `值访问、类型` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T>::reference emplaceBack(Args &&... args)`

**API 类别：** 公有函数

**中文解读：** `QList::emplaceBack` 用于计算、查询或取得与“emplace、末尾”相关的操作。调用时要先确认当前状态和 `args` 的有效范围；返回类型是 `QList<T>::reference`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T>::reference`。
- 参数 `args`：类型为 `Args &&...`。没有默认值，调用时必须提供。传入 `Args &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T>::iterator insert(qsizetype i, QList<T>::parameter_type value)`

**API 类别：** 公有函数

**中文解读：** 这是向 `QList` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QList<T>::iterator`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `QList<T>::parameter_type`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T>::iterator insert(QList<T>::const_iterator before, QList<T>::parameter_type value)`

**API 类别：** 公有函数

**中文解读：** 这是向 `QList` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QList<T>::iterator`。
- 参数 `before`：类型为 `QList<T>::const_iterator`。没有默认值，调用时必须提供。传入 `QList<T>::const_iterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `QList<T>::parameter_type`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.8) qsizetype max_size() const`

**API 类别：** 公有函数

**中文解读：** `QList::max_size` 用于计算、查询或取得与“max、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void prepend(QList<T>::parameter_type value)`

**API 类别：** 公有函数

**中文解读：** `QList::prepend` 用于执行与“前置追加”相关的操作。调用时要先确认当前状态和 `value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `value`：类型为 `QList<T>::parameter_type`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void push_front(QList<T>::parameter_type value)`

**API 类别：** 公有函数

**中文解读：** 这是向 `QList` 添加依赖、数据或子对象的 API `push_front`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `value`：类型为 `QList<T>::parameter_type`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void replace(qsizetype i, QList<T>::parameter_type value)`

**API 类别：** 公有函数

**中文解读：** `QList::replace` 用于执行与“替换”相关的操作。调用时要先确认当前状态和 `i`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `QList<T>::parameter_type`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.0) void resize(qsizetype size)`

**API 类别：** 公有函数

**中文解读：** `QList::resize` 用于执行与“调整尺寸”相关的操作。调用时要先确认当前状态和 `size` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T> operator+(const QList<T> &other) &&`

**API 类别：** 公有函数

**中文解读：** 这是 `QList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QList<T>`。
- 参数 `other`：类型为 `const QList<T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T> operator+(QList<T> &&other) const &`

**API 类别：** 公有函数

**中文解读：** 这是 `QList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QList<T>`。
- 参数 `other`：类型为 `QList<T> &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T> operator+(const QList<T> &other) const &`

**API 类别：** 公有函数

**中文解读：** 这是 `QList` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QList<T>`。
- 参数 `other`：类型为 `const QList<T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

容器自己管理元素存储，容器销毁后由它提供的迭代器、引用和 data 指针通常失效。修改容器可能重新分配或 detach，不能把元素地址和迭代器当成长期句柄。

### 状态和错误边界

要区分空容器、容量、元素数量、查找失败和默认构造值。插入/删除可能改变索引和迭代器；关联容器还要考虑键唯一性、排序和查找复杂度。

### 线程边界

不同线程使用各自的容器副本通常安全；同一个容器一边读一边写仍需要同步，即使底层采用隐式共享也不会自动解决数据竞争。

### 最容易出现的错误

不要在容器修改后继续使用旧迭代器；不要在范围 for 中改变会导致迭代器失效的容器；不要误以为隐式共享等于线程安全；不要忽略 QHash/QMap/QList 的顺序和复杂度差异。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QList` 所属机制类型：Qt 容器与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
