# QMultiMap

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QMultiMap` 是 Qt 容器类型，负责保存一组元素，并提供插入、删除、查找、遍历和容量管理。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QMultiMap` 是 Qt 容器与隐式共享机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt 容器负责元素的存储、访问、遍历和修改。部分容器使用隐式共享，复制容器时可能共享数据，写操作时发生 detach；这会降低按值传递成本，但也会影响迭代器、引用、指针和修改时的性能。

**适用场景：** 先选择连续序列、关联映射、哈希表还是队列，再决定按索引、迭代器或范围遍历；批量修改时预留容量并注意 detach，跨 API 传值时确认元素类型和所有权。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要在容器修改后继续使用旧迭代器；不要在范围 for 中改变会导致迭代器失效的容器；不要误以为隐式共享等于线程安全；不要忽略 QHash/QMap/QList 的顺序和复杂度差异。

## 2. 依赖与对象关系

- 头文件：`#include <QMultiMap>`
- 继承自：未在类页中列出
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

- `class const_iterator`
- `class iterator`
- `class key_iterator`
- `ConstIterator`
- `Iterator`
- `const_key_value_iterator`
- `difference_type`
- `key_type`
- `key_value_iterator`
- `mapped_type`
- `size_type`

### 公有函数

- `QMultiMap()`
- `(since 6.0) QMultiMap(QMap<Key, T> &&other)`
- `(since 6.0) QMultiMap(const QMap<Key, T> &other)`
- `QMultiMap(const std::multimap<Key, T> &other)`
- `QMultiMap(std::initializer_list<std::pair<Key, T>> list)`
- `QMultiMap(std::multimap<Key, T> &&other)`
- `QMultiMap(const QMultiMap<Key, T> &other)`
- `QMultiMap(QMultiMap<Key, T> &&other)`
- `~QMultiMap()`
- `(since 6.4) auto asKeyValueRange() &&`
- `(since 6.4) auto asKeyValueRange() &`
- `(since 6.4) auto asKeyValueRange() const &&`
- `(since 6.4) auto asKeyValueRange() const &`
- `QMultiMap<Key, T>::iterator begin()`
- `QMultiMap<Key, T>::const_iterator begin() const`
- `QMultiMap<Key, T>::const_iterator cbegin() const`
- `QMultiMap<Key, T>::const_iterator cend() const`
- `void clear()`
- `QMultiMap<Key, T>::const_iterator constBegin() const`
- `QMultiMap<Key, T>::const_iterator constEnd() const`
- `QMultiMap<Key, T>::const_iterator constFind(const Key &key) const`
- `QMultiMap<Key, T>::const_iterator constFind(const Key &key, const T &value) const`
- `QMultiMap<Key, T>::const_key_value_iterator constKeyValueBegin() const`
- `QMultiMap<Key, T>::const_key_value_iterator constKeyValueEnd() const`
- `bool contains(const Key &key) const`
- `bool contains(const Key &key, const T &value) const`
- `QMultiMap<Key, T>::size_type count(const Key &key) const`
- `QMultiMap<Key, T>::size_type count(const Key &key, const T &value) const`
- `QMultiMap<Key, T>::size_type count() const`
- `bool empty() const`
- `QMultiMap<Key, T>::iterator end()`
- `QMultiMap<Key, T>::const_iterator end() const`
- `std::pair<QMultiMap<Key, T>::iterator, QMultiMap<Key, T>::iterator> equal_range(const Key &key)`
- `std::pair<QMultiMap<Key, T>::const_iterator, QMultiMap<Key, T>::const_iterator> equal_range(const Key &key) const`
- `QMultiMap<Key, T>::iterator erase(QMultiMap<Key, T>::const_iterator pos)`
- `(since 6.0) QMultiMap<Key, T>::iterator erase(QMultiMap<Key, T>::const_iterator first, QMultiMap<Key, T>::const_iterator last)`
- `QMultiMap<Key, T>::iterator find(const Key &key)`
- `QMultiMap<Key, T>::const_iterator find(const Key &key) const`
- `QMultiMap<Key, T>::const_iterator find(const Key &key, const T &value) const`
- `T & first()`
- `const T & first() const`
- `const Key & firstKey() const`
- `QMultiMap<Key, T>::iterator insert(const Key &key, const T &value)`
- `QMultiMap<Key, T>::iterator insert(QMultiMap<Key, T>::const_iterator pos, const Key &key, const T &value)`
- `bool isEmpty() const`
- `Key key(const T &value, const Key &defaultKey = Key()) const`
- `QMultiMap<Key, T>::key_iterator keyBegin() const`
- `QMultiMap<Key, T>::key_iterator keyEnd() const`
- `QMultiMap<Key, T>::key_value_iterator keyValueBegin()`
- `QMultiMap<Key, T>::const_key_value_iterator keyValueBegin() const`
- `QMultiMap<Key, T>::key_value_iterator keyValueEnd()`
- `QMultiMap<Key, T>::const_key_value_iterator keyValueEnd() const`
- `QList<Key> keys() const`
- `QList<Key> keys(const T &value) const`
- `T & last()`
- `const T & last() const`
- `const Key & lastKey() const`
- `QMultiMap<Key, T>::iterator lowerBound(const Key &key)`
- `QMultiMap<Key, T>::const_iterator lowerBound(const Key &key) const`
- `QMultiMap<Key, T>::size_type remove(const Key &key)`
- `QMultiMap<Key, T>::size_type remove(const Key &key, const T &value)`
- `(since 6.1) QMultiMap<Key, T>::size_type removeIf(Predicate pred)`
- `QMultiMap<Key, T>::iterator replace(const Key &key, const T &value)`
- `QMultiMap<Key, T>::size_type size() const`
- `void swap(QMultiMap<Key, T> &other)`
- `T take(const Key &key)`
- `std::multimap<Key, T> toStdMultiMap() const &`
- `QList<Key> uniqueKeys() const`
- `QMultiMap<Key, T> & unite(QMultiMap<Key, T> &&other)`
- `QMultiMap<Key, T> & unite(const QMultiMap<Key, T> &other)`
- `QMultiMap<Key, T>::iterator upperBound(const Key &key)`
- `QMultiMap<Key, T>::const_iterator upperBound(const Key &key) const`
- `T value(const Key &key, const T &defaultValue = T()) const`
- `QList<T> values() const`
- `QList<T> values(const Key &key) const`
- `QMultiMap<Key, T> & operator=(QMultiMap<Key, T> &&other)`
- `QMultiMap<Key, T> & operator=(const QMultiMap<Key, T> &other)`

### 相关非成员函数

- `(since 6.1) qsizetype erase_if(QMultiMap<Key, T> &map, Predicate pred)`
- `bool operator!=(const QMultiMap<Key, T> &lhs, const QMultiMap<Key, T> &rhs)`
- `QMultiMap<Key, T> operator+(const QMultiMap<Key, T> &lhs, const QMultiMap<Key, T> &rhs)`
- `QMultiMap<Key, T> operator+=(QMultiMap<Key, T> &lhs, const QMultiMap<Key, T> &rhs)`
- `QDataStream & operator<<(QDataStream &out, const QMultiMap<Key, T> &map)`
- `bool operator==(const QMultiMap<Key, T> &lhs, const QMultiMap<Key, T> &rhs)`
- `QDataStream & operator>>(QDataStream &in, QMultiMap<Key, T> &map)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 101 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QMultiMap::ConstIterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QMultiMap` 的配置属性。初始化或状态切换时通过 `setConstIterator(...)` 设置，之后用 `ConstIterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:ConstIterator`。
- 属性名：`QMultiMap`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap::Iterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QMultiMap` 的配置属性。初始化或状态切换时通过 `setIterator(...)` 设置，之后用 `Iterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:Iterator`。
- 属性名：`QMultiMap`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap::const_key_value_iterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QMultiMap` 的配置属性。初始化或状态切换时通过 `setConst_key_value_iterator(...)` 设置，之后用 `const_key_value_iterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:const_key_value_iterator`。
- 属性名：`QMultiMap`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QMultiMap::difference_type`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QMultiMap` 的配置属性。初始化或状态切换时通过 `setDifference_type(...)` 设置，之后用 `difference_type()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:difference_type`。
- 属性名：`QMultiMap`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QMultiMap::key_type`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QMultiMap` 的配置属性。初始化或状态切换时通过 `setKey_type(...)` 设置，之后用 `key_type()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:key_type`。
- 属性名：`QMultiMap`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap::key_value_iterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QMultiMap` 的配置属性。初始化或状态切换时通过 `setKey_value_iterator(...)` 设置，之后用 `key_value_iterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:key_value_iterator`。
- 属性名：`QMultiMap`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QMultiMap::mapped_type`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QMultiMap` 的配置属性。初始化或状态切换时通过 `setMapped_type(...)` 设置，之后用 `mapped_type()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:mapped_type`。
- 属性名：`QMultiMap`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QMultiMap::size_type`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QMultiMap` 的配置属性。初始化或状态切换时通过 `setSize_type(...)` 设置，之后用 `size_type()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:size_type`。
- 属性名：`QMultiMap`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap::QMultiMap()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMultiMap` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit, since 6.0] QMultiMap::QMultiMap(QMap<Key, T> &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMultiMap` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `QMap<Key, T> &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit, since 6.0] QMultiMap::QMultiMap(const QMap<Key, T> &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMultiMap` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QMap<Key, T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QMultiMap::QMultiMap(const std::multimap<Key, T> &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMultiMap` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const std::multimap<Key, T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap::QMultiMap(std::initializer_list<std::pair<Key, T>> list)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMultiMap` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `list`：类型为 `std::initializer_list<std::pair<Key, T>>`。没有默认值，调用时必须提供。传入 `std::initializer_list<std::pair<Key, T>>` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QMultiMap::QMultiMap(std::multimap<Key, T> &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMultiMap` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `std::multimap<Key, T> &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[default] QMultiMap::QMultiMap(const QMultiMap<Key, T> &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMultiMap` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QMultiMap<Key, T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[default] QMultiMap::QMultiMap(QMultiMap<Key, T> &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMultiMap` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `QMultiMap<Key, T> &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[default] QMultiMap::~QMultiMap()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMultiMap` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.4] auto QMultiMap::asKeyValueRange() const &&`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::asKeyValueRange` 用于计算、查询或取得与“as、Key、值访问、Range”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `auto`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`auto`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::iterator QMultiMap::begin()`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `begin`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::const_iterator QMultiMap::begin() const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `begin`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::const_iterator QMultiMap::cbegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::cbegin` 用于计算、查询或取得与“cbegin”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMultiMap<Key, T>::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::const_iterator QMultiMap::cend() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::cend` 用于计算、查询或取得与“cend”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMultiMap<Key, T>::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMultiMap::clear()`

**API 类别：** 成员函数说明

**中文解读：** 这是状态清理或重置 API `clear`。调用后原有数据、索引、缓存或绑定可能失效；使用前先确认它影响的是当前对象、子对象还是底层共享资源，之后重新检查状态。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::const_iterator QMultiMap::constBegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::constBegin` 用于计算、查询或取得与“const、起始位置”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMultiMap<Key, T>::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::const_iterator QMultiMap::constEnd() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::constEnd` 用于计算、查询或取得与“const、结束”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMultiMap<Key, T>::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::const_iterator QMultiMap::constFind(const Key &key) const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::constFind` 用于计算、查询或取得与“const、查找”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `QMultiMap<Key, T>::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::const_iterator`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::const_iterator QMultiMap::constFind(const Key &key, const T &value) const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::constFind` 用于计算、查询或取得与“const、查找”相关的操作。调用时要先确认当前状态和 `key`、`value` 的有效范围；返回类型是 `QMultiMap<Key, T>::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::const_iterator`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::const_key_value_iterator QMultiMap::constKeyValueBegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::constKeyValueBegin` 用于计算、查询或取得与“const、Key、值访问、起始位置”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMultiMap<Key, T>::const_key_value_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::const_key_value_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::const_key_value_iterator QMultiMap::constKeyValueEnd() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::constKeyValueEnd` 用于计算、查询或取得与“const、Key、值访问、结束”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMultiMap<Key, T>::const_key_value_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::const_key_value_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMultiMap::contains(const Key &key) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `contains`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMultiMap::contains(const Key &key, const T &value) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `contains`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::size_type QMultiMap::count(const Key &key) const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `count`，返回 `QMultiMap` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::size_type`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::size_type QMultiMap::count(const Key &key, const T &value) const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `count`，返回 `QMultiMap` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::size_type`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::size_type QMultiMap::count() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `count`，返回 `QMultiMap` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::size_type`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMultiMap::empty() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::empty` 用于计算、查询或取得与“空状态”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::iterator QMultiMap::end()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `end`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::const_iterator QMultiMap::end() const`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `end`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `std::pair<QMultiMap<Key, T>::iterator, QMultiMap<Key, T>::iterator> QMultiMap::equal_range(const Key &key)`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::equal_range` 用于计算、查询或取得与“equal、range”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `std::pair<QMultiMap<Key, T>::iterator, QMultiMap<Key, T>::iterator>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`std::pair<QMultiMap<Key, T>::iterator, QMultiMap<Key, T>::iterator>`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `std::pair<QMultiMap<Key, T>::const_iterator, QMultiMap<Key, T>::const_iterator> QMultiMap::equal_range(const Key &key) const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::equal_range` 用于计算、查询或取得与“equal、range”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `std::pair<QMultiMap<Key, T>::const_iterator, QMultiMap<Key, T>::const_iterator>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`std::pair<QMultiMap<Key, T>::const_iterator, QMultiMap<Key, T>::const_iterator>`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::iterator QMultiMap::erase(QMultiMap<Key, T>::const_iterator pos)`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::erase` 用于计算、查询或取得与“erase”相关的操作。调用时要先确认当前状态和 `pos` 的有效范围；返回类型是 `QMultiMap<Key, T>::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::iterator`。
- 参数 `pos`：类型为 `QMultiMap<Key, T>::const_iterator`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QMultiMap<Key, T>::iterator QMultiMap::erase(QMultiMap<Key, T>::const_iterator first, QMultiMap<Key, T>::const_iterator last)`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::erase` 用于计算、查询或取得与“erase”相关的操作。调用时要先确认当前状态和 `first`、`last` 的有效范围；返回类型是 `QMultiMap<Key, T>::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::iterator`。
- 参数 `first`：类型为 `QMultiMap<Key, T>::const_iterator`。没有默认值，调用时必须提供。传入 `QMultiMap<Key, T>::const_iterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `last`：类型为 `QMultiMap<Key, T>::const_iterator`。没有默认值，调用时必须提供。传入 `QMultiMap<Key, T>::const_iterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::iterator QMultiMap::find(const Key &key)`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::find` 用于计算、查询或取得与“查找”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `QMultiMap<Key, T>::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::iterator`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::const_iterator QMultiMap::find(const Key &key) const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::find` 用于计算、查询或取得与“查找”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `QMultiMap<Key, T>::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::const_iterator`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::const_iterator QMultiMap::find(const Key &key, const T &value) const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::find` 用于计算、查询或取得与“查找”相关的操作。调用时要先确认当前状态和 `key`、`value` 的有效范围；返回类型是 `QMultiMap<Key, T>::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::const_iterator`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T &QMultiMap::first()`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::first` 用于计算、查询或取得与“首项”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `T &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`T &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const T &QMultiMap::first() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::first` 用于计算、查询或取得与“首项”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const T &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const T &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const Key &QMultiMap::firstKey() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::firstKey` 用于计算、查询或取得与“首项、Key”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const Key &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const Key &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::iterator QMultiMap::insert(const Key &key, const T &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QMultiMap` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::iterator`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::iterator QMultiMap::insert(QMultiMap<Key, T>::const_iterator pos, const Key &key, const T &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QMultiMap` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::iterator`。
- 参数 `pos`：类型为 `QMultiMap<Key, T>::const_iterator`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMultiMap::isEmpty() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isEmpty`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Key QMultiMap::key(const T &value, const Key &defaultKey = Key()) const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::key` 用于计算、查询或取得与“key”相关的操作。调用时要先确认当前状态和 `value`、`defaultKey` 的有效范围；返回类型是 `Key`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Key`。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。
- 参数 `defaultKey`：类型为 `const Key &`。默认值为 `Key()`。传入 `const Key &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::key_iterator QMultiMap::keyBegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::keyBegin` 用于计算、查询或取得与“key、起始位置”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMultiMap<Key, T>::key_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::key_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::key_iterator QMultiMap::keyEnd() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::keyEnd` 用于计算、查询或取得与“key、结束”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMultiMap<Key, T>::key_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::key_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::key_value_iterator QMultiMap::keyValueBegin()`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::keyValueBegin` 用于计算、查询或取得与“key、值访问、起始位置”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMultiMap<Key, T>::key_value_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::key_value_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::const_key_value_iterator QMultiMap::keyValueBegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::keyValueBegin` 用于计算、查询或取得与“key、值访问、起始位置”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMultiMap<Key, T>::const_key_value_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::const_key_value_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::key_value_iterator QMultiMap::keyValueEnd()`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::keyValueEnd` 用于计算、查询或取得与“key、值访问、结束”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMultiMap<Key, T>::key_value_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::key_value_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::const_key_value_iterator QMultiMap::keyValueEnd() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::keyValueEnd` 用于计算、查询或取得与“key、值访问、结束”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMultiMap<Key, T>::const_key_value_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::const_key_value_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<Key> QMultiMap::keys() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::keys` 用于计算、查询或取得与“keys”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<Key>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<Key>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<Key> QMultiMap::keys(const T &value) const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::keys` 用于计算、查询或取得与“keys”相关的操作。调用时要先确认当前状态和 `value` 的有效范围；返回类型是 `QList<Key>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<Key>`。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T &QMultiMap::last()`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::last` 用于计算、查询或取得与“末项”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `T &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`T &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const T &QMultiMap::last() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::last` 用于计算、查询或取得与“末项”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const T &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const T &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const Key &QMultiMap::lastKey() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::lastKey` 用于计算、查询或取得与“末项、Key”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const Key &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const Key &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::iterator QMultiMap::lowerBound(const Key &key)`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::lowerBound` 用于计算、查询或取得与“lower、Bound”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `QMultiMap<Key, T>::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::iterator`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::const_iterator QMultiMap::lowerBound(const Key &key) const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::lowerBound` 用于计算、查询或取得与“lower、Bound”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `QMultiMap<Key, T>::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::const_iterator`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::size_type QMultiMap::remove(const Key &key)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `remove`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::size_type`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::size_type QMultiMap::remove(const Key &key, const T &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `remove`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::size_type`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] template <typename Predicate> QMultiMap<Key, T>::size_type QMultiMap::removeIf(Predicate pred)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeIf`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`template <typename Predicate> QMultiMap<Key, T>::size_type`。
- 参数 `pred`：类型为 `Predicate`。没有默认值，调用时必须提供。传入 `Predicate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::iterator QMultiMap::replace(const Key &key, const T &value)`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::replace` 用于计算、查询或取得与“替换”相关的操作。调用时要先确认当前状态和 `key`、`value` 的有效范围；返回类型是 `QMultiMap<Key, T>::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::iterator`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::size_type QMultiMap::size() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `size`，返回 `QMultiMap` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::size_type`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QMultiMap::swap(QMultiMap<Key, T> &other)`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QMultiMap<Key, T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QMultiMap::take(const Key &key)`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::take` 用于计算、查询或取得与“取出”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `T`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`T`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `std::multimap<Key, T> QMultiMap::toStdMultiMap() const &`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toStdMultiMap`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`std::multimap<Key, T>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<Key> QMultiMap::uniqueKeys() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::uniqueKeys` 用于计算、查询或取得与“unique、Keys”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<Key>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<Key>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T> &QMultiMap::unite(QMultiMap<Key, T> &&other)`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::unite` 用于计算、查询或取得与“unite”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `QMultiMap<Key, T> &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiMap<Key, T> &`。
- 参数 `other`：类型为 `QMultiMap<Key, T> &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T> &QMultiMap::unite(const QMultiMap<Key, T> &other)`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::unite` 用于计算、查询或取得与“unite”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `QMultiMap<Key, T> &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiMap<Key, T> &`。
- 参数 `other`：类型为 `const QMultiMap<Key, T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::iterator QMultiMap::upperBound(const Key &key)`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::upperBound` 用于计算、查询或取得与“upper、Bound”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `QMultiMap<Key, T>::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::iterator`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<Key, T>::const_iterator QMultiMap::upperBound(const Key &key) const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::upperBound` 用于计算、查询或取得与“upper、Bound”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `QMultiMap<Key, T>::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiMap<Key, T>::const_iterator`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QMultiMap::value(const Key &key, const T &defaultValue = T()) const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `value`，用于取得 `QMultiMap` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`T`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `defaultValue`：类型为 `const T &`。默认值为 `T()`。传入 `const T &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T> QMultiMap::values() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::values` 用于计算、查询或取得与“values”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<T>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T> QMultiMap::values(const Key &key) const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiMap::values` 用于计算、查询或取得与“values”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `QList<T>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T>`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[default] QMultiMap<Key, T> &QMultiMap::operator=(QMultiMap<Key, T> &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMultiMap` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMultiMap<Key, T> &`。
- 参数 `other`：类型为 `QMultiMap<Key, T> &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[default] QMultiMap<Key, T> &QMultiMap::operator=(const QMultiMap<Key, T> &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMultiMap` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMultiMap<Key, T> &`。
- 参数 `other`：类型为 `const QMultiMap<Key, T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] template < typename Key, typename T, typename Predicate > qsizetype erase_if(QMultiMap<Key, T> &map, Predicate pred)`

**API 类别：** 相关非成员函数

**中文解读：** `QMultiMap::erase_if` 用于计算、查询或取得与“erase、if”相关的操作。调用时要先确认当前状态和 `map`、`pred` 的有效范围；返回类型是 `template < typename Key, typename T, typename Predicate > qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template < typename Key, typename T, typename Predicate > qsizetype`。
- 参数 `map`：类型为 `QMultiMap<Key, T> &`。没有默认值，调用时必须提供。传入 `QMultiMap<Key, T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pred`：类型为 `Predicate`。没有默认值，调用时必须提供。传入 `Predicate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool operator!=(const QMultiMap<Key, T> &lhs, const QMultiMap<Key, T> &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMultiMap` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QMultiMap<Key, T> &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QMultiMap<Key, T> &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Key, typename T> QMultiMap<Key, T> operator+(const QMultiMap<Key, T> &lhs, const QMultiMap<Key, T> &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMultiMap` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template <typename Key, typename T> QMultiMap<Key, T>`。
- 参数 `lhs`：类型为 `const QMultiMap<Key, T> &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QMultiMap<Key, T> &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Key, typename T> QMultiMap<Key, T> operator+=(QMultiMap<Key, T> &lhs, const QMultiMap<Key, T> &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMultiMap` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template <typename Key, typename T> QMultiMap<Key, T>`。
- 参数 `lhs`：类型为 `QMultiMap<Key, T> &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QMultiMap<Key, T> &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Key, typename T> QDataStream &operator<<(QDataStream &out, const QMultiMap<Key, T> &map)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMultiMap` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template <typename Key, typename T> QDataStream &`。
- 参数 `out`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `map`：类型为 `const QMultiMap<Key, T> &`。没有默认值，调用时必须提供。传入 `const QMultiMap<Key, T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool operator==(const QMultiMap<Key, T> &lhs, const QMultiMap<Key, T> &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMultiMap` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QMultiMap<Key, T> &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QMultiMap<Key, T> &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Key, typename T> QDataStream &operator>>(QDataStream &in, QMultiMap<Key, T> &map)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMultiMap` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template <typename Key, typename T> QDataStream &`。
- 参数 `in`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `map`：类型为 `QMultiMap<Key, T> &`。没有默认值，调用时必须提供。传入 `QMultiMap<Key, T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `class const_iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QMultiMap` 暴露的类型声明 `const、iterator`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `class iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QMultiMap` 暴露的类型声明 `iterator`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `class key_iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QMultiMap` 暴露的类型声明 `key、iterator`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `ConstIterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QMultiMap` 的 `Const、Iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QMultiMap` 的 `Iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const_key_value_iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QMultiMap` 的 `const、key、值访问、iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `difference_type`

**API 类别：** 公有类型

**中文解读：** 这是 `QMultiMap` 的 `difference、类型` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `key_type`

**API 类别：** 公有类型

**中文解读：** 这是 `QMultiMap` 的 `key、类型` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `key_value_iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QMultiMap` 的 `key、值访问、iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `mapped_type`

**API 类别：** 公有类型

**中文解读：** 这是转换/映射 API `mapped_type`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `size_type`

**API 类别：** 公有类型

**中文解读：** 这是 `QMultiMap` 的 `尺寸或数量、类型` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.4) auto asKeyValueRange() &&`

**API 类别：** 公有函数

**中文解读：** `QMultiMap::asKeyValueRange` 用于计算、查询或取得与“as、Key、值访问、Range”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `auto`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`auto`。
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

`QMultiMap` 所属机制类型：Qt 容器与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
