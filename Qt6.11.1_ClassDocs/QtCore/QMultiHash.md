# QMultiHash

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QMultiHash` 是 Qt 容器类型，负责保存一组元素，并提供插入、删除、查找、遍历和容量管理。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QMultiHash` 是 Qt 容器与隐式共享机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt 容器负责元素的存储、访问、遍历和修改。部分容器使用隐式共享，复制容器时可能共享数据，写操作时发生 detach；这会降低按值传递成本，但也会影响迭代器、引用、指针和修改时的性能。

**适用场景：** 先选择连续序列、关联映射、哈希表还是队列，再决定按索引、迭代器或范围遍历；批量修改时预留容量并注意 detach，跨 API 传值时确认元素类型和所有权。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要在容器修改后继续使用旧迭代器；不要在范围 for 中改变会导致迭代器失效的容器；不要误以为隐式共享等于线程安全；不要忽略 QHash/QMap/QList 的顺序和复杂度差异。

## 2. 依赖与对象关系

- 头文件：`#include <QMultiHash>`
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
- `const_key_value_iterator`
- `key_value_iterator`

### 公有函数

- `QMultiHash()`
- `QMultiHash(const QHash<Key, T> &other)`
- `QMultiHash(std::initializer_list<std::pair<Key, T>> list)`
- `QMultiHash(InputIterator begin, InputIterator end)`
- `(since 6.4) auto asKeyValueRange() &&`
- `(since 6.4) auto asKeyValueRange() &`
- `(since 6.4) auto asKeyValueRange() const &&`
- `(since 6.4) auto asKeyValueRange() const &`
- `QMultiHash<Key, T>::iterator begin()`
- `QMultiHash<Key, T>::const_iterator begin() const`
- `QMultiHash<Key, T>::const_iterator cbegin() const`
- `QMultiHash<Key, T>::const_iterator cend() const`
- `void clear()`
- `QMultiHash<Key, T>::const_iterator constBegin() const`
- `QMultiHash<Key, T>::const_iterator constEnd() const`
- `QMultiHash<Key, T>::const_iterator constFind(const Key &key, const T &value) const`
- `QMultiHash<Key, T>::const_key_value_iterator constKeyValueBegin() const`
- `QMultiHash<Key, T>::const_key_value_iterator constKeyValueEnd() const`
- `bool contains(const Key &key, const T &value) const`
- `qsizetype count(const Key &key, const T &value) const`
- `QMultiHash<Key, T>::iterator emplace(Key &&key, Args &&... args)`
- `QMultiHash<Key, T>::iterator emplace(const Key &key, Args &&... args)`
- `QMultiHash<Key, T>::iterator emplaceReplace(Key &&key, Args &&... args)`
- `QMultiHash<Key, T>::iterator emplaceReplace(const Key &key, Args &&... args)`
- `QMultiHash<Key, T>::iterator end()`
- `QMultiHash<Key, T>::const_iterator end() const`
- `std::pair<QMultiHash<Key, T>::iterator, QMultiHash<Key, T>::iterator> equal_range(const Key &key)`
- `std::pair<QMultiHash<Key, T>::const_iterator, QMultiHash<Key, T>::const_iterator> equal_range(const Key &key) const`
- `QMultiHash<Key, T>::iterator erase(QMultiHash<Key, T>::const_iterator pos)`
- `QMultiHash<Key, T>::iterator find(const Key &key, const T &value)`
- `QMultiHash<Key, T>::const_iterator find(const Key &key, const T &value) const`
- `QMultiHash<Key, T>::iterator insert(const Key &key, const T &value)`
- `(since 6.11) QMultiHash<Key, T>::iterator insert(Key &&key, T &&value)`
- `(since 6.11) QMultiHash<Key, T>::iterator insert(Key &&key, const T &value)`
- `(since 6.11) QMultiHash<Key, T>::iterator insert(const Key &key, T &&value)`
- `Key key(const T &value) const`
- `Key key(const T &value, const Key &defaultKey) const`
- `QMultiHash<Key, T>::key_iterator keyBegin() const`
- `QMultiHash<Key, T>::key_iterator keyEnd() const`
- `QMultiHash<Key, T>::key_value_iterator keyValueBegin()`
- `QMultiHash<Key, T>::const_key_value_iterator keyValueBegin() const`
- `QMultiHash<Key, T>::key_value_iterator keyValueEnd()`
- `QMultiHash<Key, T>::const_key_value_iterator keyValueEnd() const`
- `QList<Key> keys() const`
- `qsizetype remove(const Key &key)`
- `qsizetype remove(const Key &key, const T &value)`
- `(since 6.1) qsizetype removeIf(Predicate pred)`
- `QMultiHash<Key, T>::iterator replace(const Key &key, const T &value)`
- `void swap(QMultiHash<Key, T> &other)`
- `T take(const Key &key)`
- `QList<Key> uniqueKeys() const`
- `(since 6.0) QMultiHash<Key, T> & unite(const QHash<Key, T> &other)`
- `QMultiHash<Key, T> & unite(const QMultiHash<Key, T> &other)`
- `T value(const Key &key) const`
- `T value(const Key &key, const T &defaultValue) const`
- `QList<T> values() const`
- `QList<T> values(const Key &key) const`
- `QMultiHash<Key, T> operator+(const QMultiHash<Key, T> &other) const`
- `QMultiHash<Key, T> & operator+=(const QMultiHash<Key, T> &other)`
- `T & operator[](const Key &key)`

### 相关非成员函数

- `(since 6.1) qsizetype erase_if(QMultiHash<Key, T> &hash, Predicate pred)`
- `size_t qHash(const QMultiHash<Key, T> &key, size_t seed = 0)`
- `bool operator!=(const QMultiHash<Key, T> &lhs, const QMultiHash<Key, T> &rhs)`
- `QDataStream & operator<<(QDataStream &out, const QMultiHash<Key, T> &hash)`
- `bool operator==(const QMultiHash<Key, T> &lhs, const QMultiHash<Key, T> &rhs)`
- `QDataStream & operator>>(QDataStream &in, QMultiHash<Key, T> &hash)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 71 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QMultiHash::const_key_value_iterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QMultiHash` 的配置属性。初始化或状态切换时通过 `setConst_key_value_iterator(...)` 设置，之后用 `const_key_value_iterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:const_key_value_iterator`。
- 属性名：`QMultiHash`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiHash::key_value_iterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QMultiHash` 的配置属性。初始化或状态切换时通过 `setKey_value_iterator(...)` 设置，之后用 `key_value_iterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:key_value_iterator`。
- 属性名：`QMultiHash`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QMultiHash::QMultiHash()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMultiHash` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QMultiHash::QMultiHash(const QHash<Key, T> &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMultiHash` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QHash<Key, T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiHash::QMultiHash(std::initializer_list<std::pair<Key, T>> list)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMultiHash` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `list`：类型为 `std::initializer_list<std::pair<Key, T>>`。没有默认值，调用时必须提供。传入 `std::initializer_list<std::pair<Key, T>>` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename InputIterator> QMultiHash::QMultiHash(InputIterator begin, InputIterator end)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMultiHash` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `begin`：类型为 `InputIterator`。没有默认值，调用时必须提供。传入 `InputIterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `end`：类型为 `InputIterator`。没有默认值，调用时必须提供。传入 `InputIterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.4] auto QMultiHash::asKeyValueRange() const &&`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::asKeyValueRange` 用于计算、查询或取得与“as、Key、值访问、Range”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `auto`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`auto`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiHash<Key, T>::iterator QMultiHash::begin()`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `begin`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QMultiHash<Key, T>::iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QMultiHash<Key, T>::const_iterator QMultiHash::begin() const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `begin`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QMultiHash<Key, T>::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QMultiHash<Key, T>::const_iterator QMultiHash::cbegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::cbegin` 用于计算、查询或取得与“cbegin”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMultiHash<Key, T>::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiHash<Key, T>::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QMultiHash<Key, T>::const_iterator QMultiHash::cend() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::cend` 用于计算、查询或取得与“cend”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMultiHash<Key, T>::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiHash<Key, T>::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept(...)] void QMultiHash::clear()`

**API 类别：** 成员函数说明

**中文解读：** 这是状态清理或重置 API `clear`。调用后原有数据、索引、缓存或绑定可能失效；使用前先确认它影响的是当前对象、子对象还是底层共享资源，之后重新检查状态。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QMultiHash<Key, T>::const_iterator QMultiHash::constBegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::constBegin` 用于计算、查询或取得与“const、起始位置”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMultiHash<Key, T>::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiHash<Key, T>::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QMultiHash<Key, T>::const_iterator QMultiHash::constEnd() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::constEnd` 用于计算、查询或取得与“const、结束”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMultiHash<Key, T>::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiHash<Key, T>::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QMultiHash<Key, T>::const_iterator QMultiHash::constFind(const Key &key, const T &value) const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::constFind` 用于计算、查询或取得与“const、查找”相关的操作。调用时要先确认当前状态和 `key`、`value` 的有效范围；返回类型是 `QMultiHash<Key, T>::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiHash<Key, T>::const_iterator`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QMultiHash<Key, T>::const_key_value_iterator QMultiHash::constKeyValueBegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::constKeyValueBegin` 用于计算、查询或取得与“const、Key、值访问、起始位置”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMultiHash<Key, T>::const_key_value_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiHash<Key, T>::const_key_value_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QMultiHash<Key, T>::const_key_value_iterator QMultiHash::constKeyValueEnd() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::constKeyValueEnd` 用于计算、查询或取得与“const、Key、值访问、结束”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMultiHash<Key, T>::const_key_value_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiHash<Key, T>::const_key_value_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool QMultiHash::contains(const Key &key, const T &value) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `contains`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] qsizetype QMultiHash::count(const Key &key, const T &value) const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `count`，返回 `QMultiHash` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename... Args> QMultiHash<Key, T>::iterator QMultiHash::emplace(Key &&key, Args &&... args)`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::emplace` 用于计算、查询或取得与“emplace”相关的操作。调用时要先确认当前状态和 `key`、`args` 的有效范围；返回类型是 `template <typename... Args> QMultiHash<Key, T>::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename... Args> QMultiHash<Key, T>::iterator`。
- 参数 `key`：类型为 `Key &&`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `args`：类型为 `Args &&...`。没有默认值，调用时必须提供。传入 `Args &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename... Args> QMultiHash<Key, T>::iterator QMultiHash::emplaceReplace(Key &&key, Args &&... args)`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::emplaceReplace` 用于计算、查询或取得与“emplace、替换”相关的操作。调用时要先确认当前状态和 `key`、`args` 的有效范围；返回类型是 `template <typename... Args> QMultiHash<Key, T>::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename... Args> QMultiHash<Key, T>::iterator`。
- 参数 `key`：类型为 `Key &&`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `args`：类型为 `Args &&...`。没有默认值，调用时必须提供。传入 `Args &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QMultiHash<Key, T>::iterator QMultiHash::end()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `end`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QMultiHash<Key, T>::iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QMultiHash<Key, T>::const_iterator QMultiHash::end() const`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `end`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QMultiHash<Key, T>::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `std::pair<QMultiHash<Key, T>::iterator, QMultiHash<Key, T>::iterator> QMultiHash::equal_range(const Key &key)`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::equal_range` 用于计算、查询或取得与“equal、range”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `std::pair<QMultiHash<Key, T>::iterator, QMultiHash<Key, T>::iterator>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`std::pair<QMultiHash<Key, T>::iterator, QMultiHash<Key, T>::iterator>`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] std::pair<QMultiHash<Key, T>::const_iterator, QMultiHash<Key, T>::const_iterator> QMultiHash::equal_range(const Key &key) const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::equal_range` 用于计算、查询或取得与“equal、range”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `std::pair<QMultiHash<Key, T>::const_iterator, QMultiHash<Key, T>::const_iterator>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`std::pair<QMultiHash<Key, T>::const_iterator, QMultiHash<Key, T>::const_iterator>`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiHash<Key, T>::iterator QMultiHash::erase(QMultiHash<Key, T>::const_iterator pos)`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::erase` 用于计算、查询或取得与“erase”相关的操作。调用时要先确认当前状态和 `pos` 的有效范围；返回类型是 `QMultiHash<Key, T>::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiHash<Key, T>::iterator`。
- 参数 `pos`：类型为 `QMultiHash<Key, T>::const_iterator`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiHash<Key, T>::iterator QMultiHash::find(const Key &key, const T &value)`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::find` 用于计算、查询或取得与“查找”相关的操作。调用时要先确认当前状态和 `key`、`value` 的有效范围；返回类型是 `QMultiHash<Key, T>::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiHash<Key, T>::iterator`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QMultiHash<Key, T>::const_iterator QMultiHash::find(const Key &key, const T &value) const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::find` 用于计算、查询或取得与“查找”相关的操作。调用时要先确认当前状态和 `key`、`value` 的有效范围；返回类型是 `QMultiHash<Key, T>::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiHash<Key, T>::const_iterator`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiHash<Key, T>::iterator QMultiHash::insert(const Key &key, const T &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QMultiHash` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QMultiHash<Key, T>::iterator`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.11] QMultiHash<Key, T>::iterator QMultiHash::insert(Key &&key, T &&value)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QMultiHash` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QMultiHash<Key, T>::iterator`。
- 参数 `key`：类型为 `Key &&`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `value`：类型为 `T &&`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] Key QMultiHash::key(const T &value, const Key &defaultKey) const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::key` 用于计算、查询或取得与“key”相关的操作。调用时要先确认当前状态和 `value`、`defaultKey` 的有效范围；返回类型是 `Key`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Key`。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。
- 参数 `defaultKey`：类型为 `const Key &`。没有默认值，调用时必须提供。传入 `const Key &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QMultiHash<Key, T>::key_iterator QMultiHash::keyBegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::keyBegin` 用于计算、查询或取得与“key、起始位置”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMultiHash<Key, T>::key_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiHash<Key, T>::key_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QMultiHash<Key, T>::key_iterator QMultiHash::keyEnd() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::keyEnd` 用于计算、查询或取得与“key、结束”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMultiHash<Key, T>::key_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiHash<Key, T>::key_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QMultiHash<Key, T>::key_value_iterator QMultiHash::keyValueBegin()`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::keyValueBegin` 用于计算、查询或取得与“key、值访问、起始位置”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMultiHash<Key, T>::key_value_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiHash<Key, T>::key_value_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QMultiHash<Key, T>::const_key_value_iterator QMultiHash::keyValueBegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::keyValueBegin` 用于计算、查询或取得与“key、值访问、起始位置”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMultiHash<Key, T>::const_key_value_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiHash<Key, T>::const_key_value_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QMultiHash<Key, T>::key_value_iterator QMultiHash::keyValueEnd()`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::keyValueEnd` 用于计算、查询或取得与“key、值访问、结束”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMultiHash<Key, T>::key_value_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiHash<Key, T>::key_value_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QMultiHash<Key, T>::const_key_value_iterator QMultiHash::keyValueEnd() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::keyValueEnd` 用于计算、查询或取得与“key、值访问、结束”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMultiHash<Key, T>::const_key_value_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiHash<Key, T>::const_key_value_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<Key> QMultiHash::keys() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::keys` 用于计算、查询或取得与“keys”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<Key>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<Key>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QMultiHash::remove(const Key &key)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `remove`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QMultiHash::remove(const Key &key, const T &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `remove`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] template <typename Predicate> qsizetype QMultiHash::removeIf(Predicate pred)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeIf`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`template <typename Predicate> qsizetype`。
- 参数 `pred`：类型为 `Predicate`。没有默认值，调用时必须提供。传入 `Predicate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiHash<Key, T>::iterator QMultiHash::replace(const Key &key, const T &value)`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::replace` 用于计算、查询或取得与“替换”相关的操作。调用时要先确认当前状态和 `key`、`value` 的有效范围；返回类型是 `QMultiHash<Key, T>::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiHash<Key, T>::iterator`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QMultiHash::swap(QMultiHash<Key, T> &other)`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QMultiHash<Key, T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QMultiHash::take(const Key &key)`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::take` 用于计算、查询或取得与“取出”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `T`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`T`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<Key> QMultiHash::uniqueKeys() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::uniqueKeys` 用于计算、查询或取得与“unique、Keys”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<Key>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<Key>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QMultiHash<Key, T> &QMultiHash::unite(const QHash<Key, T> &other)`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::unite` 用于计算、查询或取得与“unite”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `QMultiHash<Key, T> &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiHash<Key, T> &`。
- 参数 `other`：类型为 `const QHash<Key, T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiHash<Key, T> &QMultiHash::unite(const QMultiHash<Key, T> &other)`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::unite` 用于计算、查询或取得与“unite”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `QMultiHash<Key, T> &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiHash<Key, T> &`。
- 参数 `other`：类型为 `const QMultiHash<Key, T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] T QMultiHash::value(const Key &key, const T &defaultValue) const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `value`，用于取得 `QMultiHash` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`T`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `defaultValue`：类型为 `const T &`。没有默认值，调用时必须提供。传入 `const T &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T> QMultiHash::values() const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::values` 用于计算、查询或取得与“values”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<T>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<T> QMultiHash::values(const Key &key) const`

**API 类别：** 成员函数说明

**中文解读：** `QMultiHash::values` 用于计算、查询或取得与“values”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `QList<T>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<T>`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiHash<Key, T> QMultiHash::operator+(const QMultiHash<Key, T> &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMultiHash` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMultiHash<Key, T>`。
- 参数 `other`：类型为 `const QMultiHash<Key, T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiHash<Key, T> &QMultiHash::operator+=(const QMultiHash<Key, T> &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMultiHash` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMultiHash<Key, T> &`。
- 参数 `other`：类型为 `const QMultiHash<Key, T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T &QMultiHash::operator[](const Key &key)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMultiHash` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`T &`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] template < typename Key, typename T, typename Predicate > qsizetype erase_if(QMultiHash<Key, T> &hash, Predicate pred)`

**API 类别：** 相关非成员函数

**中文解读：** `QMultiHash::erase_if` 用于计算、查询或取得与“erase、if”相关的操作。调用时要先确认当前状态和 `hash`、`pred` 的有效范围；返回类型是 `template < typename Key, typename T, typename Predicate > qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template < typename Key, typename T, typename Predicate > qsizetype`。
- 参数 `hash`：类型为 `QMultiHash<Key, T> &`。没有默认值，调用时必须提供。传入 `QMultiHash<Key, T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pred`：类型为 `Predicate`。没有默认值，调用时必须提供。传入 `Predicate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept(...)] template <typename Key, typename T> size_t qHash(const QMultiHash<Key, T> &key, size_t seed = 0)`

**API 类别：** 相关非成员函数

**中文解读：** `QMultiHash::qHash` 用于计算、查询或取得与“q、Hash”相关的操作。调用时要先确认当前状态和 `key`、`seed` 的有效范围；返回类型是 `template <typename Key, typename T> size_t`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Key, typename T> size_t`。
- 参数 `key`：类型为 `const QMultiHash<Key, T> &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `seed`：类型为 `size_t`。默认值为 `0`。传入 `size_t` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator!=(const QMultiHash<Key, T> &lhs, const QMultiHash<Key, T> &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMultiHash` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QMultiHash<Key, T> &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QMultiHash<Key, T> &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Key, typename T> QDataStream &operator<<(QDataStream &out, const QMultiHash<Key, T> &hash)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMultiHash` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template <typename Key, typename T> QDataStream &`。
- 参数 `out`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `hash`：类型为 `const QMultiHash<Key, T> &`。没有默认值，调用时必须提供。传入 `const QMultiHash<Key, T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator==(const QMultiHash<Key, T> &lhs, const QMultiHash<Key, T> &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMultiHash` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QMultiHash<Key, T> &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QMultiHash<Key, T> &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Key, typename T> QDataStream &operator>>(QDataStream &in, QMultiHash<Key, T> &hash)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMultiHash` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template <typename Key, typename T> QDataStream &`。
- 参数 `in`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `hash`：类型为 `QMultiHash<Key, T> &`。没有默认值，调用时必须提供。传入 `QMultiHash<Key, T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `class const_iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QMultiHash` 暴露的类型声明 `const、iterator`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `class iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QMultiHash` 暴露的类型声明 `iterator`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `class key_iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QMultiHash` 暴露的类型声明 `key、iterator`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const_key_value_iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QMultiHash` 的 `const、key、值访问、iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `key_value_iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QMultiHash` 的 `key、值访问、iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.4) auto asKeyValueRange() &&`

**API 类别：** 公有函数

**中文解读：** `QMultiHash::asKeyValueRange` 用于计算、查询或取得与“as、Key、值访问、Range”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `auto`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`auto`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiHash<Key, T>::iterator emplace(const Key &key, Args &&... args)`

**API 类别：** 公有函数

**中文解读：** `QMultiHash::emplace` 用于计算、查询或取得与“emplace”相关的操作。调用时要先确认当前状态和 `key`、`args` 的有效范围；返回类型是 `QMultiHash<Key, T>::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiHash<Key, T>::iterator`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `args`：类型为 `Args &&...`。没有默认值，调用时必须提供。传入 `Args &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiHash<Key, T>::iterator emplaceReplace(const Key &key, Args &&... args)`

**API 类别：** 公有函数

**中文解读：** `QMultiHash::emplaceReplace` 用于计算、查询或取得与“emplace、替换”相关的操作。调用时要先确认当前状态和 `key`、`args` 的有效范围；返回类型是 `QMultiHash<Key, T>::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiHash<Key, T>::iterator`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `args`：类型为 `Args &&...`。没有默认值，调用时必须提供。传入 `Args &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.11) QMultiHash<Key, T>::iterator insert(Key &&key, const T &value)`

**API 类别：** 公有函数

**中文解读：** 这是向 `QMultiHash` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QMultiHash<Key, T>::iterator`。
- 参数 `key`：类型为 `Key &&`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.11) QMultiHash<Key, T>::iterator insert(const Key &key, T &&value)`

**API 类别：** 公有函数

**中文解读：** 这是向 `QMultiHash` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QMultiHash<Key, T>::iterator`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `value`：类型为 `T &&`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Key key(const T &value) const`

**API 类别：** 公有函数

**中文解读：** `QMultiHash::key` 用于计算、查询或取得与“key”相关的操作。调用时要先确认当前状态和 `value` 的有效范围；返回类型是 `Key`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Key`。
- 参数 `value`：类型为 `const T &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T value(const Key &key) const`

**API 类别：** 公有函数

**中文解读：** 这是数据访问 API `value`，用于取得 `QMultiHash` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`T`。
- 参数 `key`：类型为 `const Key &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

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

`QMultiHash` 所属机制类型：Qt 容器与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
