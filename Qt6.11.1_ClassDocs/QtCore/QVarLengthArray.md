# QVarLengthArray

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QVarLengthArray` 是 Qt 容器类型，负责保存一组元素，并提供插入、删除、查找、遍历和容量管理。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QVarLengthArray` 是 Qt 容器与隐式共享机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt 容器负责元素的存储、访问、遍历和修改。部分容器使用隐式共享，复制容器时可能共享数据，写操作时发生 detach；这会降低按值传递成本，但也会影响迭代器、引用、指针和修改时的性能。

**适用场景：** 先选择连续序列、关联映射、哈希表还是队列，再决定按索引、迭代器或范围遍历；批量修改时预留容量并注意 detach，跨 API 传值时确认元素类型和所有权。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要在容器修改后继续使用旧迭代器；不要在范围 for 中改变会导致迭代器失效的容器；不要误以为隐式共享等于线程安全；不要忽略 QHash/QMap/QList 的顺序和复杂度差异。

## 2. 依赖与对象关系

- 头文件：`#include <QVarLengthArray>`
- 继承自：QVLABase、QVLAStorage
- 直接派生类：未在类页中列出

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

- `const_iterator`
- `const_pointer`
- `const_reference`
- `const_reverse_iterator`
- `difference_type`
- `iterator`
- `pointer`
- `reference`
- `reverse_iterator`
- `size_type`
- `value_type`

### 公有函数

- `QVarLengthArray()`
- `QVarLengthArray(qsizetype size)`
- `QVarLengthArray(std::initializer_list<T> args)`
- `QVarLengthArray(InputIterator first, InputIterator last)`
- `(since 6.4) QVarLengthArray(qsizetype size, const T &v)`
- `QVarLengthArray(const QVarLengthArray<T, Prealloc> &other)`
- `(since 6.0) QVarLengthArray(QVarLengthArray<T, Prealloc> &&other)`
- `~QVarLengthArray()`
- `void append(const T &t)`
- `void append(const T *buf, qsizetype size)`
- `void append(T &&t)`
- `(since 6.6) QVarLengthArray<T, Prealloc> & assign(std::initializer_list<T> list)`
- `(since 6.6) QVarLengthArray<T, Prealloc> & assign(InputIterator first, InputIterator last)`
- `(since 6.6) QVarLengthArray<T, Prealloc> & assign(qsizetype n, const T &t)`
- `const T & at(qsizetype i) const`
- `T & back()`
- `const T & back() const`
- `QVarLengthArray<T, Prealloc>::iterator begin()`
- `QVarLengthArray<T, Prealloc>::const_iterator begin() const`
- `qsizetype capacity() const`
- `QVarLengthArray<T, Prealloc>::const_iterator cbegin() const`
- `QVarLengthArray<T, Prealloc>::const_iterator cend() const`
- `void clear()`
- `QVarLengthArray<T, Prealloc>::const_iterator constBegin() const`
- `const T * constData() const`
- `QVarLengthArray<T, Prealloc>::const_iterator constEnd() const`
- `bool contains(const AT &value) const`
- `qsizetype count() const`
- `QVarLengthArray<T, Prealloc>::const_reverse_iterator crbegin() const`
- `QVarLengthArray<T, Prealloc>::const_reverse_iterator crend() const`
- `T * data()`
- `const T * data() const`
- `(since 6.3) QVarLengthArray<T, Prealloc>::iterator emplace(QVarLengthArray<T, Prealloc>::const_iterator pos, Args &&... args)`
- `(since 6.3) T & emplace_back(Args &&... args)`
- `bool empty() const`
- `QVarLengthArray<T, Prealloc>::iterator end()`
- `QVarLengthArray<T, Prealloc>::const_iterator end() const`
- `QVarLengthArray<T, Prealloc>::iterator erase(QVarLengthArray<T, Prealloc>::const_iterator pos)`
- `QVarLengthArray<T, Prealloc>::iterator erase(QVarLengthArray<T, Prealloc>::const_iterator begin, QVarLengthArray<T, Prealloc>::const_iterator end)`
- `T & first()`
- `const T & first() const`
- `T & front()`
- `const T & front() const`
- `qsizetype indexOf(const AT &value, qsizetype from = 0) const`
- `void insert(qsizetype i, T &&value)`
- `void insert(qsizetype i, const T &value)`
- `QVarLengthArray<T, Prealloc>::iterator insert(QVarLengthArray<T, Prealloc>::const_iterator before, qsizetype count, const T &value)`
- `QVarLengthArray<T, Prealloc>::iterator insert(QVarLengthArray<T, Prealloc>::const_iterator before, T &&value)`
- `QVarLengthArray<T, Prealloc>::iterator insert(QVarLengthArray<T, Prealloc>::const_iterator before, const T &value)`
- `void insert(qsizetype i, qsizetype count, const T &value)`
- `bool isEmpty() const`
- `T & last()`
- `const T & last() const`
- `qsizetype lastIndexOf(const AT &value, qsizetype from = -1) const`
- `qsizetype length() const`
- `(since 6.8) qsizetype max_size() const`
- `void pop_back()`
- `void push_back(const T &t)`
- `void push_back(T &&t)`
- `QVarLengthArray<T, Prealloc>::reverse_iterator rbegin()`
- `QVarLengthArray<T, Prealloc>::const_reverse_iterator rbegin() const`
- `void remove(qsizetype i, qsizetype count = 1)`
- `(since 6.1) qsizetype removeAll(const AT &t)`
- `(since 6.1) qsizetype removeIf(Predicate pred)`
- `void removeLast()`
- `(since 6.1) bool removeOne(const AT &t)`
- `QVarLengthArray<T, Prealloc>::reverse_iterator rend()`
- `QVarLengthArray<T, Prealloc>::const_reverse_iterator rend() const`
- `void replace(qsizetype i, const T &value)`
- `void reserve(qsizetype size)`
- `void resize(qsizetype size)`
- `(since 6.4) void resize(qsizetype size, const T &v)`
- `void shrink_to_fit()`
- `qsizetype size() const`
- `void squeeze()`
- `T value(qsizetype i) const`
- `T value(qsizetype i, const T &defaultValue) const`
- `QVarLengthArray<T, Prealloc> & operator+=(const T &value)`
- `QVarLengthArray<T, Prealloc> & operator+=(T &&value)`
- `QVarLengthArray<T, Prealloc> & operator<<(const T &value)`
- `QVarLengthArray<T, Prealloc> & operator<<(T &&value)`
- `(since 6.0) QVarLengthArray<T, Prealloc> & operator=(QVarLengthArray<T, Prealloc> &&other)`
- `QVarLengthArray<T, Prealloc> & operator=(const QVarLengthArray<T, Prealloc> &other)`
- `QVarLengthArray<T, Prealloc> & operator=(std::initializer_list<T> list)`
- `T & operator[](qsizetype i)`
- `const T & operator[](qsizetype i) const`

### 静态公有成员

- `(since 6.8) qsizetype maxSize()`

### 相关非成员函数

- `(since 6.1) qsizetype erase(QVarLengthArray<T, Prealloc> &array, const AT &t)`
- `(since 6.1) qsizetype erase_if(QVarLengthArray<T, Prealloc> &array, Predicate pred)`
- `size_t qHash(const QVarLengthArray<T, Prealloc> &key, size_t seed = 0)`
- `bool operator!=(const QVarLengthArray<T, Prealloc1> &left, const QVarLengthArray<T, Prealloc2> &right)`
- `bool operator<(const QVarLengthArray<T, Prealloc1> &lhs, const QVarLengthArray<T, Prealloc2> &rhs)`
- `bool operator<=(const QVarLengthArray<T, Prealloc1> &lhs, const QVarLengthArray<T, Prealloc2> &rhs)`
- `bool operator==(const QVarLengthArray<T, Prealloc1> &left, const QVarLengthArray<T, Prealloc2> &right)`
- `bool operator>(const QVarLengthArray<T, Prealloc1> &lhs, const QVarLengthArray<T, Prealloc2> &rhs)`
- `bool operator>=(const QVarLengthArray<T, Prealloc1> &lhs, const QVarLengthArray<T, Prealloc2> &rhs)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 118 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[alias] QVarLengthArray::const_iterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QVarLengthArray` 的配置属性。初始化或状态切换时通过 `setConst_iterator(...)` 设置，之后用 `const_iterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:const_iterator`。
- 属性名：`QVarLengthArray`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QVarLengthArray::const_pointer`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QVarLengthArray` 的配置属性。初始化或状态切换时通过 `setConst_pointer(...)` 设置，之后用 `const_pointer()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:const_pointer`。
- 属性名：`QVarLengthArray`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QVarLengthArray::const_reference`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QVarLengthArray` 的配置属性。初始化或状态切换时通过 `setConst_reference(...)` 设置，之后用 `const_reference()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:const_reference`。
- 属性名：`QVarLengthArray`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QVarLengthArray::const_reverse_iterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QVarLengthArray` 的配置属性。初始化或状态切换时通过 `setConst_reverse_iterator(...)` 设置，之后用 `const_reverse_iterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:const_reverse_iterator`。
- 属性名：`QVarLengthArray`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QVarLengthArray::difference_type`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QVarLengthArray` 的配置属性。初始化或状态切换时通过 `setDifference_type(...)` 设置，之后用 `difference_type()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:difference_type`。
- 属性名：`QVarLengthArray`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QVarLengthArray::iterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QVarLengthArray` 的配置属性。初始化或状态切换时通过 `setIterator(...)` 设置，之后用 `iterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:iterator`。
- 属性名：`QVarLengthArray`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QVarLengthArray::pointer`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QVarLengthArray` 的配置属性。初始化或状态切换时通过 `setPointer(...)` 设置，之后用 `pointer()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:pointer`。
- 属性名：`QVarLengthArray`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QVarLengthArray::reference`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QVarLengthArray` 的配置属性。初始化或状态切换时通过 `setReference(...)` 设置，之后用 `reference()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:reference`。
- 属性名：`QVarLengthArray`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QVarLengthArray::reverse_iterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QVarLengthArray` 的配置属性。初始化或状态切换时通过 `setReverse_iterator(...)` 设置，之后用 `reverse_iterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:reverse_iterator`。
- 属性名：`QVarLengthArray`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QVarLengthArray::size_type`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QVarLengthArray` 的配置属性。初始化或状态切换时通过 `setSize_type(...)` 设置，之后用 `size_type()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:size_type`。
- 属性名：`QVarLengthArray`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QVarLengthArray::value_type`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QVarLengthArray` 的配置属性。初始化或状态切换时通过 `setValue_type(...)` 设置，之后用 `value_type()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:value_type`。
- 属性名：`QVarLengthArray`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QVarLengthArray::QVarLengthArray()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVarLengthArray` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QVarLengthArray::QVarLengthArray(qsizetype size)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVarLengthArray` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVarLengthArray::QVarLengthArray(std::initializer_list<T> args)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVarLengthArray` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `args`：类型为 `std::initializer_list<T>`。没有默认值，调用时必须提供。传入 `std::initializer_list<T>` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename InputIterator, QVarLengthArray<T, Prealloc>::if_input_iterator<InputIterator> = true> QVarLengthArray::QVarLengthArray(InputIterator first, InputIterator last)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVarLengthArray` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `first`：类型为 `InputIterator`。没有默认值，调用时必须提供。传入 `InputIterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `last`：类型为 `InputIterator`。没有默认值，调用时必须提供。传入 `InputIterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit, since 6.4] QVarLengthArray::QVarLengthArray(qsizetype size, const T &v)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVarLengthArray` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。
- 参数 `v`：类型为 `const T &`。没有默认值，调用时必须提供。传入 `const T &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVarLengthArray::QVarLengthArray(const QVarLengthArray<T, Prealloc> &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVarLengthArray` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QVarLengthArray<T, Prealloc> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept(...), since 6.0] QVarLengthArray::QVarLengthArray(QVarLengthArray<T, Prealloc> &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVarLengthArray` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `QVarLengthArray<T, Prealloc> &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVarLengthArray::~QVarLengthArray()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVarLengthArray` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVarLengthArray::append(const T &t)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QVarLengthArray` 添加依赖、数据或子对象的 API `append`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `t`：类型为 `const T &`。没有默认值，调用时必须提供。传入 `const T &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVarLengthArray::append(const T *buf, qsizetype size)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QVarLengthArray` 添加依赖、数据或子对象的 API `append`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `buf`：类型为 `const T *`。没有默认值，调用时必须提供。传入 `const T *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVarLengthArray::append(T &&t)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QVarLengthArray` 添加依赖、数据或子对象的 API `append`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `t`：类型为 `T &&`。没有默认值，调用时必须提供。传入 `T &&` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] QVarLengthArray<T, Prealloc> &QVarLengthArray::assign(std::initializer_list<T> list)`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::assign` 用于计算、查询或取得与“assign”相关的操作。调用时要先确认当前状态和 `list` 的有效范围；返回类型是 `QVarLengthArray<T, Prealloc> &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVarLengthArray<T, Prealloc> &`。
- 参数 `list`：类型为 `std::initializer_list<T>`。没有默认值，调用时必须提供。传入 `std::initializer_list<T>` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] template <typename InputIterator, QVarLengthArray<T, Prealloc>::if_input_iterator<InputIterator> = true> QVarLengthArray<T, Prealloc> &QVarLengthArray::assign(InputIterator first, InputIterator last)`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::assign` 用于计算、查询或取得与“assign”相关的操作。调用时要先确认当前状态和 `first`、`last` 的有效范围；返回类型是 `template <typename InputIterator, QVarLengthArray<T, Prealloc>::if_input_iterator<InputIterator> = true> QVarLengthArray<T, Prealloc> &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename InputIterator, QVarLengthArray<T, Prealloc>::if_input_iterator<InputIterator> = true> QVarLengthArray<T, Prealloc> &`。
- 参数 `first`：类型为 `InputIterator`。没有默认值，调用时必须提供。传入 `InputIterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `last`：类型为 `InputIterator`。没有默认值，调用时必须提供。传入 `InputIterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] QVarLengthArray<T, Prealloc> &QVarLengthArray::assign(qsizetype n, const T &t)`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::assign` 用于计算、查询或取得与“assign”相关的操作。调用时要先确认当前状态和 `n`、`t` 的有效范围；返回类型是 `QVarLengthArray<T, Prealloc> &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVarLengthArray<T, Prealloc> &`。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `t`：类型为 `const T &`。没有默认值，调用时必须提供。传入 `const T &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const T &QVarLengthArray::at(qsizetype i) const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `at`，用于取得 `QVarLengthArray` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`const T &`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T &QVarLengthArray::back()`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::back` 用于计算、查询或取得与“末尾”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `T &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`T &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const T &QVarLengthArray::back() const`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::back` 用于计算、查询或取得与“末尾”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const T &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const T &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVarLengthArray<T, Prealloc>::iterator QVarLengthArray::begin()`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `begin`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QVarLengthArray<T, Prealloc>::iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVarLengthArray<T, Prealloc>::const_iterator QVarLengthArray::begin() const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `begin`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QVarLengthArray<T, Prealloc>::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QVarLengthArray::capacity() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `capacity`，返回 `QVarLengthArray` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVarLengthArray<T, Prealloc>::const_iterator QVarLengthArray::cbegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::cbegin` 用于计算、查询或取得与“cbegin”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVarLengthArray<T, Prealloc>::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVarLengthArray<T, Prealloc>::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVarLengthArray<T, Prealloc>::const_iterator QVarLengthArray::cend() const`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::cend` 用于计算、查询或取得与“cend”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVarLengthArray<T, Prealloc>::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVarLengthArray<T, Prealloc>::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVarLengthArray::clear()`

**API 类别：** 成员函数说明

**中文解读：** 这是状态清理或重置 API `clear`。调用后原有数据、索引、缓存或绑定可能失效；使用前先确认它影响的是当前对象、子对象还是底层共享资源，之后重新检查状态。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVarLengthArray<T, Prealloc>::const_iterator QVarLengthArray::constBegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::constBegin` 用于计算、查询或取得与“const、起始位置”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVarLengthArray<T, Prealloc>::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVarLengthArray<T, Prealloc>::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const T *QVarLengthArray::constData() const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `constData`，用于取得 `QVarLengthArray` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`const T *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVarLengthArray<T, Prealloc>::const_iterator QVarLengthArray::constEnd() const`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::constEnd` 用于计算、查询或取得与“const、结束”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVarLengthArray<T, Prealloc>::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVarLengthArray<T, Prealloc>::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename AT = T> bool QVarLengthArray::contains(const AT &value) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `contains`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`template <typename AT = T> bool`。
- 参数 `value`：类型为 `const AT &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QVarLengthArray::count() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `count`，返回 `QVarLengthArray` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVarLengthArray<T, Prealloc>::const_reverse_iterator QVarLengthArray::crbegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::crbegin` 用于计算、查询或取得与“crbegin”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVarLengthArray<T, Prealloc>::const_reverse_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVarLengthArray<T, Prealloc>::const_reverse_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVarLengthArray<T, Prealloc>::const_reverse_iterator QVarLengthArray::crend() const`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::crend` 用于计算、查询或取得与“crend”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVarLengthArray<T, Prealloc>::const_reverse_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVarLengthArray<T, Prealloc>::const_reverse_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T *QVarLengthArray::data()`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `data`，用于取得 `QVarLengthArray` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`T *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const T *QVarLengthArray::data() const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `data`，用于取得 `QVarLengthArray` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`const T *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.3] template <typename... Args> QVarLengthArray<T, Prealloc>::iterator QVarLengthArray::emplace(QVarLengthArray<T, Prealloc>::const_iterator pos, Args &&... args)`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::emplace` 用于计算、查询或取得与“emplace”相关的操作。调用时要先确认当前状态和 `pos`、`args` 的有效范围；返回类型是 `template <typename... Args> QVarLengthArray<T, Prealloc>::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename... Args> QVarLengthArray<T, Prealloc>::iterator`。
- 参数 `pos`：类型为 `QVarLengthArray<T, Prealloc>::const_iterator`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。
- 参数 `args`：类型为 `Args &&...`。没有默认值，调用时必须提供。传入 `Args &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.3] template <typename... Args> T &QVarLengthArray::emplace_back(Args &&... args)`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::emplace_back` 用于计算、查询或取得与“emplace、末尾”相关的操作。调用时要先确认当前状态和 `args` 的有效范围；返回类型是 `template <typename... Args> T &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename... Args> T &`。
- 参数 `args`：类型为 `Args &&...`。没有默认值，调用时必须提供。传入 `Args &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QVarLengthArray::empty() const`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::empty` 用于计算、查询或取得与“空状态”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVarLengthArray<T, Prealloc>::iterator QVarLengthArray::end()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `end`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QVarLengthArray<T, Prealloc>::iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVarLengthArray<T, Prealloc>::const_iterator QVarLengthArray::end() const`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `end`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QVarLengthArray<T, Prealloc>::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVarLengthArray<T, Prealloc>::iterator QVarLengthArray::erase(QVarLengthArray<T, Prealloc>::const_iterator pos)`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::erase` 用于计算、查询或取得与“erase”相关的操作。调用时要先确认当前状态和 `pos` 的有效范围；返回类型是 `QVarLengthArray<T, Prealloc>::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVarLengthArray<T, Prealloc>::iterator`。
- 参数 `pos`：类型为 `QVarLengthArray<T, Prealloc>::const_iterator`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVarLengthArray<T, Prealloc>::iterator QVarLengthArray::erase(QVarLengthArray<T, Prealloc>::const_iterator begin, QVarLengthArray<T, Prealloc>::const_iterator end)`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::erase` 用于计算、查询或取得与“erase”相关的操作。调用时要先确认当前状态和 `begin`、`end` 的有效范围；返回类型是 `QVarLengthArray<T, Prealloc>::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVarLengthArray<T, Prealloc>::iterator`。
- 参数 `begin`：类型为 `QVarLengthArray<T, Prealloc>::const_iterator`。没有默认值，调用时必须提供。传入 `QVarLengthArray<T, Prealloc>::const_iterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `end`：类型为 `QVarLengthArray<T, Prealloc>::const_iterator`。没有默认值，调用时必须提供。传入 `QVarLengthArray<T, Prealloc>::const_iterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T &QVarLengthArray::first()`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::first` 用于计算、查询或取得与“首项”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `T &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`T &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const T &QVarLengthArray::first() const`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::first` 用于计算、查询或取得与“首项”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const T &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const T &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T &QVarLengthArray::front()`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::front` 用于计算、查询或取得与“开头”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `T &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`T &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const T &QVarLengthArray::front() const`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::front` 用于计算、查询或取得与“开头”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const T &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const T &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename AT = T> qsizetype QVarLengthArray::indexOf(const AT &value, qsizetype from = 0) const`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::indexOf` 用于计算、查询或取得与“索引、Of”相关的操作。调用时要先确认当前状态和 `value`、`from` 的有效范围；返回类型是 `template <typename AT = T> qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename AT = T> qsizetype`。
- 参数 `value`：类型为 `const AT &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。
- 参数 `from`：类型为 `qsizetype`。默认值为 `0`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVarLengthArray::insert(qsizetype i, T &&value)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QVarLengthArray` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `T &&`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVarLengthArray<T, Prealloc>::iterator QVarLengthArray::insert(QVarLengthArray<T, Prealloc>::const_iterator before, qsizetype count, const T &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QVarLengthArray` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QVarLengthArray<T, Prealloc>::iterator`。
- 参数 `before`：类型为 `QVarLengthArray<T, Prealloc>::const_iterator`。没有默认值，调用时必须提供。传入 `QVarLengthArray<T, Prealloc>::const_iterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVarLengthArray<T, Prealloc>::iterator QVarLengthArray::insert(QVarLengthArray<T, Prealloc>::const_iterator before, T &&value)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QVarLengthArray` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QVarLengthArray<T, Prealloc>::iterator`。
- 参数 `before`：类型为 `QVarLengthArray<T, Prealloc>::const_iterator`。没有默认值，调用时必须提供。传入 `QVarLengthArray<T, Prealloc>::const_iterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `T &&`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVarLengthArray::insert(qsizetype i, qsizetype count, const T &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QVarLengthArray` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QVarLengthArray::isEmpty() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isEmpty`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T &QVarLengthArray::last()`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::last` 用于计算、查询或取得与“末项”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `T &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`T &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const T &QVarLengthArray::last() const`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::last` 用于计算、查询或取得与“末项”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const T &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const T &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename AT = T> qsizetype QVarLengthArray::lastIndexOf(const AT &value, qsizetype from = -1) const`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::lastIndexOf` 用于计算、查询或取得与“末项、索引、Of”相关的操作。调用时要先确认当前状态和 `value`、`from` 的有效范围；返回类型是 `template <typename AT = T> qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename AT = T> qsizetype`。
- 参数 `value`：类型为 `const AT &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。
- 参数 `from`：类型为 `qsizetype`。默认值为 `-1`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QVarLengthArray::length() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `length`，返回 `QVarLengthArray` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static constexpr noexcept, since 6.8] qsizetype QVarLengthArray::maxSize()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `maxSize`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVarLengthArray::pop_back()`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::pop_back` 用于执行与“pop、末尾”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVarLengthArray::push_back(const T &t)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QVarLengthArray` 添加依赖、数据或子对象的 API `push_back`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `t`：类型为 `const T &`。没有默认值，调用时必须提供。传入 `const T &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVarLengthArray::push_back(T &&t)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QVarLengthArray` 添加依赖、数据或子对象的 API `push_back`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `t`：类型为 `T &&`。没有默认值，调用时必须提供。传入 `T &&` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVarLengthArray<T, Prealloc>::reverse_iterator QVarLengthArray::rbegin()`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::rbegin` 用于计算、查询或取得与“rbegin”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVarLengthArray<T, Prealloc>::reverse_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVarLengthArray<T, Prealloc>::reverse_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVarLengthArray<T, Prealloc>::const_reverse_iterator QVarLengthArray::rbegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::rbegin` 用于计算、查询或取得与“rbegin”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVarLengthArray<T, Prealloc>::const_reverse_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVarLengthArray<T, Prealloc>::const_reverse_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVarLengthArray::remove(qsizetype i, qsizetype count = 1)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `remove`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `qsizetype`。默认值为 `1`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] template <typename AT = T> qsizetype QVarLengthArray::removeAll(const AT &t)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeAll`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`template <typename AT = T> qsizetype`。
- 参数 `t`：类型为 `const AT &`。没有默认值，调用时必须提供。传入 `const AT &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] template <typename Predicate> qsizetype QVarLengthArray::removeIf(Predicate pred)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeIf`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`template <typename Predicate> qsizetype`。
- 参数 `pred`：类型为 `Predicate`。没有默认值，调用时必须提供。传入 `Predicate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVarLengthArray::removeLast()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeLast`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] template <typename AT = T> bool QVarLengthArray::removeOne(const AT &t)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeOne`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`template <typename AT = T> bool`。
- 参数 `t`：类型为 `const AT &`。没有默认值，调用时必须提供。传入 `const AT &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVarLengthArray<T, Prealloc>::reverse_iterator QVarLengthArray::rend()`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::rend` 用于计算、查询或取得与“rend”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVarLengthArray<T, Prealloc>::reverse_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVarLengthArray<T, Prealloc>::reverse_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVarLengthArray<T, Prealloc>::const_reverse_iterator QVarLengthArray::rend() const`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::rend` 用于计算、查询或取得与“rend”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVarLengthArray<T, Prealloc>::const_reverse_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVarLengthArray<T, Prealloc>::const_reverse_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVarLengthArray::replace(qsizetype i, const T &value)`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::replace` 用于执行与“替换”相关的操作。调用时要先确认当前状态和 `i`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVarLengthArray::reserve(qsizetype size)`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::reserve` 用于执行与“reserve”相关的操作。调用时要先确认当前状态和 `size` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVarLengthArray::resize(qsizetype size)`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::resize` 用于执行与“调整尺寸”相关的操作。调用时要先确认当前状态和 `size` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.4] void QVarLengthArray::resize(qsizetype size, const T &v)`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::resize` 用于执行与“调整尺寸”相关的操作。调用时要先确认当前状态和 `size`、`v` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。
- 参数 `v`：类型为 `const T &`。没有默认值，调用时必须提供。传入 `const T &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVarLengthArray::shrink_to_fit()`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::shrink_to_fit` 用于执行与“shrink、转换输出、fit”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QVarLengthArray::size() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `size`，返回 `QVarLengthArray` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVarLengthArray::squeeze()`

**API 类别：** 成员函数说明

**中文解读：** `QVarLengthArray::squeeze` 用于执行与“squeeze”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QVarLengthArray::value(qsizetype i) const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `value`，用于取得 `QVarLengthArray` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`T`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QVarLengthArray::value(qsizetype i, const T &defaultValue) const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `value`，用于取得 `QVarLengthArray` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`T`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `defaultValue`：类型为 `const T &`。没有默认值，调用时必须提供。传入 `const T &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVarLengthArray<T, Prealloc> &QVarLengthArray::operator+=(const T &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVarLengthArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QVarLengthArray<T, Prealloc> &`。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVarLengthArray<T, Prealloc> &QVarLengthArray::operator+=(T &&value)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVarLengthArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QVarLengthArray<T, Prealloc> &`。
- 参数 `value`：类型为 `T &&`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVarLengthArray<T, Prealloc> &QVarLengthArray::operator<<(const T &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVarLengthArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QVarLengthArray<T, Prealloc> &`。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVarLengthArray<T, Prealloc> &QVarLengthArray::operator<<(T &&value)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVarLengthArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QVarLengthArray<T, Prealloc> &`。
- 参数 `value`：类型为 `T &&`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept(...), since 6.0] QVarLengthArray<T, Prealloc> &QVarLengthArray::operator=(QVarLengthArray<T, Prealloc> &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVarLengthArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QVarLengthArray<T, Prealloc> &`。
- 参数 `other`：类型为 `QVarLengthArray<T, Prealloc> &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVarLengthArray<T, Prealloc> &QVarLengthArray::operator=(const QVarLengthArray<T, Prealloc> &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVarLengthArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QVarLengthArray<T, Prealloc> &`。
- 参数 `other`：类型为 `const QVarLengthArray<T, Prealloc> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVarLengthArray<T, Prealloc> &QVarLengthArray::operator=(std::initializer_list<T> list)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVarLengthArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QVarLengthArray<T, Prealloc> &`。
- 参数 `list`：类型为 `std::initializer_list<T>`。没有默认值，调用时必须提供。传入 `std::initializer_list<T>` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T &QVarLengthArray::operator[](qsizetype i)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVarLengthArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`T &`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const T &QVarLengthArray::operator[](qsizetype i) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVarLengthArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`const T &`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] template < typename T, qsizetype Prealloc, typename AT > qsizetype erase(QVarLengthArray<T, Prealloc> &array, const AT &t)`

**API 类别：** 相关非成员函数

**中文解读：** `QVarLengthArray::erase` 用于计算、查询或取得与“erase”相关的操作。调用时要先确认当前状态和 `array`、`t` 的有效范围；返回类型是 `template < typename T, qsizetype Prealloc, typename AT > qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template < typename T, qsizetype Prealloc, typename AT > qsizetype`。
- 参数 `array`：类型为 `QVarLengthArray<T, Prealloc> &`。没有默认值，调用时必须提供。传入 `QVarLengthArray<T, Prealloc> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `t`：类型为 `const AT &`。没有默认值，调用时必须提供。传入 `const AT &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] template < typename T, qsizetype Prealloc, typename Predicate > qsizetype erase_if(QVarLengthArray<T, Prealloc> &array, Predicate pred)`

**API 类别：** 相关非成员函数

**中文解读：** `QVarLengthArray::erase_if` 用于计算、查询或取得与“erase、if”相关的操作。调用时要先确认当前状态和 `array`、`pred` 的有效范围；返回类型是 `template < typename T, qsizetype Prealloc, typename Predicate > qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template < typename T, qsizetype Prealloc, typename Predicate > qsizetype`。
- 参数 `array`：类型为 `QVarLengthArray<T, Prealloc> &`。没有默认值，调用时必须提供。传入 `QVarLengthArray<T, Prealloc> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pred`：类型为 `Predicate`。没有默认值，调用时必须提供。传入 `Predicate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept(...)] template <typename T, qsizetype Prealloc> size_t qHash(const QVarLengthArray<T, Prealloc> &key, size_t seed = 0)`

**API 类别：** 相关非成员函数

**中文解读：** `QVarLengthArray::qHash` 用于计算、查询或取得与“q、Hash”相关的操作。调用时要先确认当前状态和 `key`、`seed` 的有效范围；返回类型是 `template <typename T, qsizetype Prealloc> size_t`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename T, qsizetype Prealloc> size_t`。
- 参数 `key`：类型为 `const QVarLengthArray<T, Prealloc> &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `seed`：类型为 `size_t`。默认值为 `0`。传入 `size_t` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template < typename T, qsizetype Prealloc1, qsizetype Prealloc2 > bool operator!=(const QVarLengthArray<T, Prealloc1> &left, const QVarLengthArray<T, Prealloc2> &right)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QVarLengthArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template < typename T, qsizetype Prealloc1, qsizetype Prealloc2 > bool`。
- 参数 `left`：类型为 `const QVarLengthArray<T, Prealloc1> &`。没有默认值，调用时必须提供。传入 `const QVarLengthArray<T, Prealloc1> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `right`：类型为 `const QVarLengthArray<T, Prealloc2> &`。没有默认值，调用时必须提供。传入 `const QVarLengthArray<T, Prealloc2> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template < typename T, qsizetype Prealloc1, qsizetype Prealloc2 > bool operator<(const QVarLengthArray<T, Prealloc1> &lhs, const QVarLengthArray<T, Prealloc2> &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QVarLengthArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template < typename T, qsizetype Prealloc1, qsizetype Prealloc2 > bool`。
- 参数 `lhs`：类型为 `const QVarLengthArray<T, Prealloc1> &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QVarLengthArray<T, Prealloc2> &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template < typename T, qsizetype Prealloc1, qsizetype Prealloc2 > bool operator<=(const QVarLengthArray<T, Prealloc1> &lhs, const QVarLengthArray<T, Prealloc2> &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QVarLengthArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template < typename T, qsizetype Prealloc1, qsizetype Prealloc2 > bool`。
- 参数 `lhs`：类型为 `const QVarLengthArray<T, Prealloc1> &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QVarLengthArray<T, Prealloc2> &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template < typename T, qsizetype Prealloc1, qsizetype Prealloc2 > bool operator==(const QVarLengthArray<T, Prealloc1> &left, const QVarLengthArray<T, Prealloc2> &right)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QVarLengthArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template < typename T, qsizetype Prealloc1, qsizetype Prealloc2 > bool`。
- 参数 `left`：类型为 `const QVarLengthArray<T, Prealloc1> &`。没有默认值，调用时必须提供。传入 `const QVarLengthArray<T, Prealloc1> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `right`：类型为 `const QVarLengthArray<T, Prealloc2> &`。没有默认值，调用时必须提供。传入 `const QVarLengthArray<T, Prealloc2> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template < typename T, qsizetype Prealloc1, qsizetype Prealloc2 > bool operator>(const QVarLengthArray<T, Prealloc1> &lhs, const QVarLengthArray<T, Prealloc2> &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QVarLengthArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template < typename T, qsizetype Prealloc1, qsizetype Prealloc2 > bool`。
- 参数 `lhs`：类型为 `const QVarLengthArray<T, Prealloc1> &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QVarLengthArray<T, Prealloc2> &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template < typename T, qsizetype Prealloc1, qsizetype Prealloc2 > bool operator>=(const QVarLengthArray<T, Prealloc1> &lhs, const QVarLengthArray<T, Prealloc2> &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QVarLengthArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template < typename T, qsizetype Prealloc1, qsizetype Prealloc2 > bool`。
- 参数 `lhs`：类型为 `const QVarLengthArray<T, Prealloc1> &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QVarLengthArray<T, Prealloc2> &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const_iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QVarLengthArray` 的 `const、iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const_pointer`

**API 类别：** 公有类型

**中文解读：** 这是 `QVarLengthArray` 的 `const、pointer` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const_reference`

**API 类别：** 公有类型

**中文解读：** 这是 `QVarLengthArray` 的 `const、reference` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const_reverse_iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QVarLengthArray` 的 `const、reverse、iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `difference_type`

**API 类别：** 公有类型

**中文解读：** 这是 `QVarLengthArray` 的 `difference、类型` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QVarLengthArray` 的 `iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `pointer`

**API 类别：** 公有类型

**中文解读：** 这是 `QVarLengthArray` 的 `pointer` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `reference`

**API 类别：** 公有类型

**中文解读：** 这是 `QVarLengthArray` 的 `reference` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `reverse_iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QVarLengthArray` 的 `reverse、iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `size_type`

**API 类别：** 公有类型

**中文解读：** 这是 `QVarLengthArray` 的 `尺寸或数量、类型` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `value_type`

**API 类别：** 公有类型

**中文解读：** 这是 `QVarLengthArray` 的 `值访问、类型` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void insert(qsizetype i, const T &value)`

**API 类别：** 公有函数

**中文解读：** 这是向 `QVarLengthArray` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVarLengthArray<T, Prealloc>::iterator insert(QVarLengthArray<T, Prealloc>::const_iterator before, const T &value)`

**API 类别：** 公有函数

**中文解读：** 这是向 `QVarLengthArray` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QVarLengthArray<T, Prealloc>::iterator`。
- 参数 `before`：类型为 `QVarLengthArray<T, Prealloc>::const_iterator`。没有默认值，调用时必须提供。传入 `QVarLengthArray<T, Prealloc>::const_iterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.8) qsizetype max_size() const`

**API 类别：** 公有函数

**中文解读：** `QVarLengthArray::max_size` 用于计算、查询或取得与“max、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

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

`QVarLengthArray` 所属机制类型：Qt 容器与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
