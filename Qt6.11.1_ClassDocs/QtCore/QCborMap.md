# QCborMap

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“Cbor映射”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QCborMap` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QCborMap>`
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

- `class ConstIterator`
- `class Iterator`
- `const_iterator`
- `(since 6.10) const_key_value_iterator`
- `iterator`
- `key_type`
- `(since 6.10) key_value_iterator`
- `mapped_type`
- `size_type`
- `value_type`

### 公有函数

- `QCborMap()`
- `QCborMap(std::initializer_list<QCborMap::value_type> args)`
- `QCborMap(const QCborMap &other)`
- `(since 6.10) QCborMap(QCborMap &&other)`
- `~QCborMap()`
- `(since 6.10) auto asKeyValueRange() &&`
- `(since 6.10) auto asKeyValueRange() &`
- `(since 6.10) auto asKeyValueRange() const &&`
- `(since 6.10) auto asKeyValueRange() const &`
- `QCborMap::iterator begin()`
- `QCborMap::const_iterator begin() const`
- `QCborMap::const_iterator cbegin() const`
- `QCborMap::const_iterator cend() const`
- `void clear()`
- `int compare(const QCborMap &other) const`
- `QCborMap::const_iterator constBegin() const`
- `QCborMap::const_iterator constEnd() const`
- `QCborMap::const_iterator constFind(qint64 key) const`
- `QCborMap::const_iterator constFind(QLatin1StringView key) const`
- `QCborMap::const_iterator constFind(const QCborValue &key) const`
- `QCborMap::const_iterator constFind(const QString &key) const`
- `(since 6.10) QCborMap::const_key_value_iterator constKeyValueBegin() const`
- `(since 6.10) QCborMap::const_key_value_iterator constKeyValueEnd() const`
- `bool contains(const QCborValue &key) const`
- `bool contains(qint64 key) const`
- `bool contains(QLatin1StringView key) const`
- `bool contains(const QString &key) const`
- `bool empty() const`
- `QCborMap::iterator end()`
- `QCborMap::const_iterator end() const`
- `QCborMap::iterator erase(QCborMap::const_iterator it)`
- `QCborMap::iterator erase(QCborMap::iterator it)`
- `QCborValue extract(QCborMap::const_iterator it)`
- `QCborValue extract(QCborMap::iterator it)`
- `QCborMap::iterator find(qint64 key)`
- `QCborMap::const_iterator find(qint64 key) const`
- `QCborMap::iterator find(QLatin1StringView key)`
- `QCborMap::iterator find(const QCborValue &key)`
- `QCborMap::iterator find(const QString &key)`
- `QCborMap::const_iterator find(QLatin1StringView key) const`
- `QCborMap::const_iterator find(const QCborValue &key) const`
- `QCborMap::const_iterator find(const QString &key) const`
- `QCborMap::iterator insert(QCborMap::value_type v)`
- `QCborMap::iterator insert(QLatin1StringView key, const QCborValue &value)`
- `QCborMap::iterator insert(const QCborValue &key, const QCborValue &value)`
- `QCborMap::iterator insert(const QString &key, const QCborValue &value)`
- `QCborMap::iterator insert(qint64 key, const QCborValue &value)`
- `bool isEmpty() const`
- `(since 6.10) QCborMap::key_value_iterator keyValueBegin()`
- `(since 6.10) QCborMap::const_key_value_iterator keyValueBegin() const`
- `(since 6.10) QCborMap::key_value_iterator keyValueEnd()`
- `(since 6.10) QCborMap::const_key_value_iterator keyValueEnd() const`
- `QList<QCborValue> keys() const`
- `void remove(const QCborValue &key)`
- `void remove(qint64 key)`
- `void remove(QLatin1StringView key)`
- `void remove(const QString &key)`
- `qsizetype size() const`
- `void swap(QCborMap &other)`
- `QCborValue take(QLatin1StringView key)`
- `QCborValue take(const QCborValue &key)`
- `QCborValue take(const QString &key)`
- `QCborValue take(qint64 key)`
- `QCborValue toCborValue() const`
- `QJsonObject toJsonObject() const`
- `QVariantHash toVariantHash() const`
- `QVariantMap toVariantMap() const`
- `QCborValue value(const QCborValue &key) const`
- `QCborValue value(qint64 key) const`
- `QCborValue value(QLatin1StringView key) const`
- `QCborValue value(const QString &key) const`
- `(since 6.10) QCborMap & operator=(QCborMap &&other)`
- `QCborMap & operator=(const QCborMap &other)`
- `QCborValueRef operator[](qint64 key)`
- `const QCborValue operator[](const QCborValue &key) const`
- `const QCborValue operator[](qint64 key) const`
- `QCborValueRef operator[](QLatin1StringView key)`
- `QCborValueRef operator[](const QCborValue &key)`
- `QCborValueRef operator[](const QString &key)`
- `const QCborValue operator[](QLatin1StringView key) const`
- `const QCborValue operator[](const QString &key) const`

### 静态公有成员

- `QCborMap fromJsonObject(const QJsonObject &obj)`
- `(since 6.3) QCborMap fromJsonObject(QJsonObject &&obj)`
- `QCborMap fromVariantHash(const QVariantHash &hash)`
- `QCborMap fromVariantMap(const QVariantMap &map)`

### 相关非成员函数

- `bool operator!=(const QCborMap &lhs, const QCborMap &rhs)`
- `bool operator<(const QCborMap &lhs, const QCborMap &rhs)`
- `bool operator<=(const QCborMap &lhs, const QCborMap &rhs)`
- `bool operator==(const QCborMap &lhs, const QCborMap &rhs)`
- `bool operator>(const QCborMap &lhs, const QCborMap &rhs)`
- `bool operator>=(const QCborMap &lhs, const QCborMap &rhs)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 107 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QCborMap::const_iterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QCborMap` 的配置属性。初始化或状态切换时通过 `setConst_iterator(...)` 设置，之后用 `const_iterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:const_iterator`。
- 属性名：`QCborMap`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.10] QCborMap::const_key_value_iterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QCborMap` 的配置属性。初始化或状态切换时通过 `setConst_key_value_iterator(...)` 设置，之后用 `const_key_value_iterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:const_key_value_iterator`。
- 属性名：`QCborMap`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::iterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QCborMap` 的配置属性。初始化或状态切换时通过 `setIterator(...)` 设置，之后用 `iterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:iterator`。
- 属性名：`QCborMap`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::key_type`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QCborMap` 的配置属性。初始化或状态切换时通过 `setKey_type(...)` 设置，之后用 `key_type()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:key_type`。
- 属性名：`QCborMap`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.10] QCborMap::key_value_iterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QCborMap` 的配置属性。初始化或状态切换时通过 `setKey_value_iterator(...)` 设置，之后用 `key_value_iterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:key_value_iterator`。
- 属性名：`QCborMap`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::mapped_type`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QCborMap` 的配置属性。初始化或状态切换时通过 `setMapped_type(...)` 设置，之后用 `mapped_type()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:mapped_type`。
- 属性名：`QCborMap`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::size_type`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QCborMap` 的配置属性。初始化或状态切换时通过 `setSize_type(...)` 设置，之后用 `size_type()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:size_type`。
- 属性名：`QCborMap`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::value_type`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QCborMap` 的配置属性。初始化或状态切换时通过 `setValue_type(...)` 设置，之后用 `value_type()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:value_type`。
- 属性名：`QCborMap`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QCborMap::QCborMap()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCborMap` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::QCborMap(std::initializer_list<QCborMap::value_type> args)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCborMap` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `args`：类型为 `std::initializer_list<QCborMap::value_type>`。没有默认值，调用时必须提供。传入 `std::initializer_list<QCborMap::value_type>` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QCborMap::QCborMap(const QCborMap &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCborMap` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QCborMap &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept, since 6.10] QCborMap::QCborMap(QCborMap &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCborMap` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `QCborMap &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QCborMap::~QCborMap()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCborMap` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.10] auto QCborMap::asKeyValueRange() const &&`

**API 类别：** 成员函数说明

**中文解读：** `QCborMap::asKeyValueRange` 用于计算、查询或取得与“as、Key、值访问、Range”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `auto`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`auto`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::iterator QCborMap::begin()`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `begin`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QCborMap::iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::const_iterator QCborMap::begin() const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `begin`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QCborMap::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::const_iterator QCborMap::cbegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QCborMap::cbegin` 用于计算、查询或取得与“cbegin”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QCborMap::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborMap::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::const_iterator QCborMap::cend() const`

**API 类别：** 成员函数说明

**中文解读：** `QCborMap::cend` 用于计算、查询或取得与“cend”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QCborMap::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborMap::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QCborMap::clear()`

**API 类别：** 成员函数说明

**中文解读：** 这是状态清理或重置 API `clear`。调用后原有数据、索引、缓存或绑定可能失效；使用前先确认它影响的是当前对象、子对象还是底层共享资源，之后重新检查状态。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] int QCborMap::compare(const QCborMap &other) const`

**API 类别：** 成员函数说明

**中文解读：** `QCborMap::compare` 用于计算、查询或取得与“比较”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `other`：类型为 `const QCborMap &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::const_iterator QCborMap::constBegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QCborMap::constBegin` 用于计算、查询或取得与“const、起始位置”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QCborMap::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborMap::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::const_iterator QCborMap::constEnd() const`

**API 类别：** 成员函数说明

**中文解读：** `QCborMap::constEnd` 用于计算、查询或取得与“const、结束”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QCborMap::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborMap::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::const_iterator QCborMap::constFind(qint64 key) const`

**API 类别：** 成员函数说明

**中文解读：** `QCborMap::constFind` 用于计算、查询或取得与“const、查找”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `QCborMap::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborMap::const_iterator`。
- 参数 `key`：类型为 `qint64`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::const_iterator QCborMap::constFind(QLatin1StringView key) const`

**API 类别：** 成员函数说明

**中文解读：** `QCborMap::constFind` 用于计算、查询或取得与“const、查找”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `QCborMap::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborMap::const_iterator`。
- 参数 `key`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::const_iterator QCborMap::constFind(const QCborValue &key) const`

**API 类别：** 成员函数说明

**中文解读：** `QCborMap::constFind` 用于计算、查询或取得与“const、查找”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `QCborMap::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborMap::const_iterator`。
- 参数 `key`：类型为 `const QCborValue &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::const_iterator QCborMap::constFind(const QString &key) const`

**API 类别：** 成员函数说明

**中文解读：** `QCborMap::constFind` 用于计算、查询或取得与“const、查找”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `QCborMap::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborMap::const_iterator`。
- 参数 `key`：类型为 `const QString &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.10] QCborMap::const_key_value_iterator QCborMap::constKeyValueBegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QCborMap::constKeyValueBegin` 用于计算、查询或取得与“const、Key、值访问、起始位置”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QCborMap::const_key_value_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborMap::const_key_value_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.10] QCborMap::const_key_value_iterator QCborMap::constKeyValueEnd() const`

**API 类别：** 成员函数说明

**中文解读：** `QCborMap::constKeyValueEnd` 用于计算、查询或取得与“const、Key、值访问、结束”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QCborMap::const_key_value_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborMap::const_key_value_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QCborMap::contains(const QCborValue &key) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `contains`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `key`：类型为 `const QCborValue &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QCborMap::contains(qint64 key) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `contains`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `key`：类型为 `qint64`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QCborMap::contains(QLatin1StringView key) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `contains`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `key`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QCborMap::contains(const QString &key) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `contains`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `key`：类型为 `const QString &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QCborMap::empty() const`

**API 类别：** 成员函数说明

**中文解读：** `QCborMap::empty` 用于计算、查询或取得与“空状态”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::iterator QCborMap::end()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `end`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QCborMap::iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::const_iterator QCborMap::end() const`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `end`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QCborMap::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::iterator QCborMap::erase(QCborMap::const_iterator it)`

**API 类别：** 成员函数说明

**中文解读：** `QCborMap::erase` 用于计算、查询或取得与“erase”相关的操作。调用时要先确认当前状态和 `it` 的有效范围；返回类型是 `QCborMap::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborMap::iterator`。
- 参数 `it`：类型为 `QCborMap::const_iterator`。没有默认值，调用时必须提供。传入 `QCborMap::const_iterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::iterator QCborMap::erase(QCborMap::iterator it)`

**API 类别：** 成员函数说明

**中文解读：** `QCborMap::erase` 用于计算、查询或取得与“erase”相关的操作。调用时要先确认当前状态和 `it` 的有效范围；返回类型是 `QCborMap::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborMap::iterator`。
- 参数 `it`：类型为 `QCborMap::iterator`。没有默认值，调用时必须提供。传入 `QCborMap::iterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborValue QCborMap::extract(QCborMap::const_iterator it)`

**API 类别：** 成员函数说明

**中文解读：** `QCborMap::extract` 用于计算、查询或取得与“extract”相关的操作。调用时要先确认当前状态和 `it` 的有效范围；返回类型是 `QCborValue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborValue`。
- 参数 `it`：类型为 `QCborMap::const_iterator`。没有默认值，调用时必须提供。传入 `QCborMap::const_iterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::const_iterator QCborMap::find(qint64 key) const`

**API 类别：** 成员函数说明

**中文解读：** `QCborMap::find` 用于计算、查询或取得与“查找”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `QCborMap::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborMap::const_iterator`。
- 参数 `key`：类型为 `qint64`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::const_iterator QCborMap::find(QLatin1StringView key) const`

**API 类别：** 成员函数说明

**中文解读：** `QCborMap::find` 用于计算、查询或取得与“查找”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `QCborMap::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborMap::const_iterator`。
- 参数 `key`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::const_iterator QCborMap::find(const QCborValue &key) const`

**API 类别：** 成员函数说明

**中文解读：** `QCborMap::find` 用于计算、查询或取得与“查找”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `QCborMap::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborMap::const_iterator`。
- 参数 `key`：类型为 `const QCborValue &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::const_iterator QCborMap::find(const QString &key) const`

**API 类别：** 成员函数说明

**中文解读：** `QCborMap::find` 用于计算、查询或取得与“查找”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `QCborMap::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborMap::const_iterator`。
- 参数 `key`：类型为 `const QString &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QCborMap QCborMap::fromJsonObject(const QJsonObject &obj)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromJsonObject`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QCborMap`。
- 参数 `obj`：类型为 `const QJsonObject &`。没有默认值，调用时必须提供。传入 `const QJsonObject &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static noexcept, since 6.3] QCborMap QCborMap::fromJsonObject(QJsonObject &&obj)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromJsonObject`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QCborMap`。
- 参数 `obj`：类型为 `QJsonObject &&`。没有默认值，调用时必须提供。传入 `QJsonObject &&` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QCborMap QCborMap::fromVariantHash(const QVariantHash &hash)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromVariantHash`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QCborMap`。
- 参数 `hash`：类型为 `const QVariantHash &`。没有默认值，调用时必须提供。传入 `const QVariantHash &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QCborMap QCborMap::fromVariantMap(const QVariantMap &map)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromVariantMap`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QCborMap`。
- 参数 `map`：类型为 `const QVariantMap &`。没有默认值，调用时必须提供。传入 `const QVariantMap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::iterator QCborMap::insert(QCborMap::value_type v)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QCborMap` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QCborMap::iterator`。
- 参数 `v`：类型为 `QCborMap::value_type`。没有默认值，调用时必须提供。传入 `QCborMap::value_type` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::iterator QCborMap::insert(QLatin1StringView key, const QCborValue &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QCborMap` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QCborMap::iterator`。
- 参数 `key`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `value`：类型为 `const QCborValue &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::iterator QCborMap::insert(const QCborValue &key, const QCborValue &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QCborMap` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QCborMap::iterator`。
- 参数 `key`：类型为 `const QCborValue &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `value`：类型为 `const QCborValue &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::iterator QCborMap::insert(const QString &key, const QCborValue &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QCborMap` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QCborMap::iterator`。
- 参数 `key`：类型为 `const QString &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `value`：类型为 `const QCborValue &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::iterator QCborMap::insert(qint64 key, const QCborValue &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QCborMap` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QCborMap::iterator`。
- 参数 `key`：类型为 `qint64`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `value`：类型为 `const QCborValue &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QCborMap::isEmpty() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isEmpty`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.10] QCborMap::key_value_iterator QCborMap::keyValueBegin()`

**API 类别：** 成员函数说明

**中文解读：** `QCborMap::keyValueBegin` 用于计算、查询或取得与“key、值访问、起始位置”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QCborMap::key_value_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborMap::key_value_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.10] QCborMap::const_key_value_iterator QCborMap::keyValueBegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QCborMap::keyValueBegin` 用于计算、查询或取得与“key、值访问、起始位置”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QCborMap::const_key_value_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborMap::const_key_value_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.10] QCborMap::key_value_iterator QCborMap::keyValueEnd()`

**API 类别：** 成员函数说明

**中文解读：** `QCborMap::keyValueEnd` 用于计算、查询或取得与“key、值访问、结束”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QCborMap::key_value_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborMap::key_value_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.10] QCborMap::const_key_value_iterator QCborMap::keyValueEnd() const`

**API 类别：** 成员函数说明

**中文解读：** `QCborMap::keyValueEnd` 用于计算、查询或取得与“key、值访问、结束”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QCborMap::const_key_value_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborMap::const_key_value_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QCborValue> QCborMap::keys() const`

**API 类别：** 成员函数说明

**中文解读：** `QCborMap::keys` 用于计算、查询或取得与“keys”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QCborValue>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QCborValue>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QCborMap::remove(const QCborValue &key)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `remove`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `key`：类型为 `const QCborValue &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QCborMap::remove(qint64 key)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `remove`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `key`：类型为 `qint64`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QCborMap::remove(QLatin1StringView key)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `remove`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `key`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QCborMap::remove(const QString &key)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `remove`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `key`：类型为 `const QString &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] qsizetype QCborMap::size() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `size`，返回 `QCborMap` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QCborMap::swap(QCborMap &other)`

**API 类别：** 成员函数说明

**中文解读：** `QCborMap::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QCborMap &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborValue QCborMap::take(QLatin1StringView key)`

**API 类别：** 成员函数说明

**中文解读：** `QCborMap::take` 用于计算、查询或取得与“取出”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `QCborValue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborValue`。
- 参数 `key`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborValue QCborMap::take(const QCborValue &key)`

**API 类别：** 成员函数说明

**中文解读：** `QCborMap::take` 用于计算、查询或取得与“取出”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `QCborValue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborValue`。
- 参数 `key`：类型为 `const QCborValue &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborValue QCborMap::take(const QString &key)`

**API 类别：** 成员函数说明

**中文解读：** `QCborMap::take` 用于计算、查询或取得与“取出”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `QCborValue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborValue`。
- 参数 `key`：类型为 `const QString &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborValue QCborMap::take(qint64 key)`

**API 类别：** 成员函数说明

**中文解读：** `QCborMap::take` 用于计算、查询或取得与“取出”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `QCborValue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborValue`。
- 参数 `key`：类型为 `qint64`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborValue QCborMap::toCborValue() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toCborValue`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QCborValue`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJsonObject QCborMap::toJsonObject() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toJsonObject`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QJsonObject`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVariantHash QCborMap::toVariantHash() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toVariantHash`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QVariantHash`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVariantMap QCborMap::toVariantMap() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toVariantMap`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QVariantMap`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborValue QCborMap::value(const QCborValue &key) const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `value`，用于取得 `QCborMap` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`QCborValue`。
- 参数 `key`：类型为 `const QCborValue &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborValue QCborMap::value(qint64 key) const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `value`，用于取得 `QCborMap` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`QCborValue`。
- 参数 `key`：类型为 `qint64`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborValue QCborMap::value(QLatin1StringView key) const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `value`，用于取得 `QCborMap` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`QCborValue`。
- 参数 `key`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborValue QCborMap::value(const QString &key) const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `value`，用于取得 `QCborMap` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`QCborValue`。
- 参数 `key`：类型为 `const QString &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.10] QCborMap &QCborMap::operator=(QCborMap &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCborMap` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QCborMap &`。
- 参数 `other`：类型为 `QCborMap &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QCborMap &QCborMap::operator=(const QCborMap &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCborMap` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QCborMap &`。
- 参数 `other`：类型为 `const QCborMap &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborValueRef QCborMap::operator[](qint64 key)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCborMap` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QCborValueRef`。
- 参数 `key`：类型为 `qint64`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QCborValue QCborMap::operator[](const QCborValue &key) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCborMap` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`const QCborValue`。
- 参数 `key`：类型为 `const QCborValue &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QCborValue QCborMap::operator[](qint64 key) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCborMap` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`const QCborValue`。
- 参数 `key`：类型为 `qint64`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborValueRef QCborMap::operator[](QLatin1StringView key)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCborMap` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QCborValueRef`。
- 参数 `key`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborValueRef QCborMap::operator[](const QCborValue &key)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCborMap` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QCborValueRef`。
- 参数 `key`：类型为 `const QCborValue &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborValueRef QCborMap::operator[](const QString &key)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCborMap` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QCborValueRef`。
- 参数 `key`：类型为 `const QString &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QCborValue QCborMap::operator[](QLatin1StringView key) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCborMap` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`const QCborValue`。
- 参数 `key`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QCborValue QCborMap::operator[](const QString &key) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCborMap` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`const QCborValue`。
- 参数 `key`：类型为 `const QString &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator!=(const QCborMap &lhs, const QCborMap &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QCborMap` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QCborMap &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QCborMap &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator<(const QCborMap &lhs, const QCborMap &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QCborMap` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QCborMap &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QCborMap &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator<=(const QCborMap &lhs, const QCborMap &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QCborMap` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QCborMap &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QCborMap &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator==(const QCborMap &lhs, const QCborMap &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QCborMap` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QCborMap &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QCborMap &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator>(const QCborMap &lhs, const QCborMap &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QCborMap` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QCborMap &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QCborMap &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator>=(const QCborMap &lhs, const QCborMap &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QCborMap` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QCborMap &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QCborMap &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `class ConstIterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QCborMap` 暴露的类型声明 `Const、Iterator`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `class Iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QCborMap` 暴露的类型声明 `Iterator`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const_iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QCborMap` 的 `const、iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.10) const_key_value_iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QCborMap` 的 `const、key、值访问、iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QCborMap` 的 `iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `key_type`

**API 类别：** 公有类型

**中文解读：** 这是 `QCborMap` 的 `key、类型` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.10) key_value_iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QCborMap` 的 `key、值访问、iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

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

**中文解读：** 这是 `QCborMap` 的 `尺寸或数量、类型` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `value_type`

**API 类别：** 公有类型

**中文解读：** 这是 `QCborMap` 的 `值访问、类型` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.10) auto asKeyValueRange() &&`

**API 类别：** 公有函数

**中文解读：** `QCborMap::asKeyValueRange` 用于计算、查询或取得与“as、Key、值访问、Range”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `auto`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`auto`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborValue extract(QCborMap::iterator it)`

**API 类别：** 公有函数

**中文解读：** `QCborMap::extract` 用于计算、查询或取得与“extract”相关的操作。调用时要先确认当前状态和 `it` 的有效范围；返回类型是 `QCborValue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborValue`。
- 参数 `it`：类型为 `QCborMap::iterator`。没有默认值，调用时必须提供。传入 `QCborMap::iterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::iterator find(qint64 key)`

**API 类别：** 公有函数

**中文解读：** `QCborMap::find` 用于计算、查询或取得与“查找”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `QCborMap::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborMap::iterator`。
- 参数 `key`：类型为 `qint64`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::iterator find(QLatin1StringView key)`

**API 类别：** 公有函数

**中文解读：** `QCborMap::find` 用于计算、查询或取得与“查找”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `QCborMap::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborMap::iterator`。
- 参数 `key`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::iterator find(const QCborValue &key)`

**API 类别：** 公有函数

**中文解读：** `QCborMap::find` 用于计算、查询或取得与“查找”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `QCborMap::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborMap::iterator`。
- 参数 `key`：类型为 `const QCborValue &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborMap::iterator find(const QString &key)`

**API 类别：** 公有函数

**中文解读：** `QCborMap::find` 用于计算、查询或取得与“查找”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `QCborMap::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborMap::iterator`。
- 参数 `key`：类型为 `const QString &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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

`QCborMap` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
