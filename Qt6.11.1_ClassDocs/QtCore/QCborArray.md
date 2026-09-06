# QCborArray

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“Cbor数组”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QCborArray` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QCborArray>`
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
- `const_pointer`
- `const_reference`
- `difference_type`
- `iterator`
- `pointer`
- `reference`
- `size_type`
- `value_type`

### 公有函数

- `QCborArray()`
- `QCborArray(std::initializer_list<QCborValue> args)`
- `QCborArray(const QCborArray &other)`
- `(since 6.10) QCborArray(QCborArray &&other)`
- `~QCborArray()`
- `void append(QCborValue &&value)`
- `void append(const QCborValue &value)`
- `QCborValue at(qsizetype i) const`
- `QCborArray::iterator begin()`
- `QCborArray::const_iterator begin() const`
- `QCborArray::const_iterator cbegin() const`
- `QCborArray::const_iterator cend() const`
- `void clear()`
- `int compare(const QCborArray &other) const`
- `QCborArray::const_iterator constBegin() const`
- `QCborArray::const_iterator constEnd() const`
- `bool contains(const QCborValue &value) const`
- `bool empty() const`
- `QCborArray::iterator end()`
- `QCborArray::const_iterator end() const`
- `QCborArray::iterator erase(QCborArray::const_iterator it)`
- `QCborArray::iterator erase(QCborArray::iterator it)`
- `QCborValue extract(QCborArray::ConstIterator it)`
- `QCborValue extract(QCborArray::Iterator it)`
- `QCborValueRef first()`
- `QCborValue first() const`
- `void insert(qsizetype i, QCborValue &&value)`
- `void insert(qsizetype i, const QCborValue &value)`
- `QCborArray::iterator insert(QCborArray::const_iterator before, const QCborValue &value)`
- `QCborArray::iterator insert(QCborArray::iterator before, const QCborValue &value)`
- `bool isEmpty() const`
- `QCborValueRef last()`
- `QCborValue last() const`
- `void pop_back()`
- `void pop_front()`
- `void prepend(QCborValue &&value)`
- `void prepend(const QCborValue &value)`
- `void push_back(const QCborValue &t)`
- `void push_front(const QCborValue &t)`
- `void removeAt(qsizetype i)`
- `void removeFirst()`
- `void removeLast()`
- `qsizetype size() const`
- `void swap(QCborArray &other)`
- `QCborValue takeAt(qsizetype i)`
- `QCborValue takeFirst()`
- `QCborValue takeLast()`
- `QCborValue toCborValue() const`
- `QJsonArray toJsonArray() const`
- `QVariantList toVariantList() const`
- `QCborArray operator+(const QCborValue &v) const`
- `QCborArray & operator+=(const QCborValue &v)`
- `QCborArray & operator<<(const QCborValue &v)`
- `(since 6.10) QCborArray & operator=(QCborArray &&other)`
- `QCborArray & operator=(const QCborArray &other)`
- `QCborValueRef operator[](qsizetype i)`
- `const QCborValue operator[](qsizetype i) const`

### 静态公有成员

- `QCborArray fromJsonArray(const QJsonArray &array)`
- `(since 6.3) QCborArray fromJsonArray(QJsonArray &&array)`
- `QCborArray fromStringList(const QStringList &list)`
- `QCborArray fromVariantList(const QVariantList &list)`

### 相关非成员函数

- `bool operator!=(const QCborArray &lhs, const QCborArray &rhs)`
- `bool operator<(const QCborArray &lhs, const QCborArray &rhs)`
- `bool operator<=(const QCborArray &lhs, const QCborArray &rhs)`
- `bool operator==(const QCborArray &lhs, const QCborArray &rhs)`
- `bool operator>(const QCborArray &lhs, const QCborArray &rhs)`
- `bool operator>=(const QCborArray &lhs, const QCborArray &rhs)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 87 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QCborArray::const_iterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QCborArray` 的配置属性。初始化或状态切换时通过 `setConst_iterator(...)` 设置，之后用 `const_iterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:const_iterator`。
- 属性名：`QCborArray`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborArray::const_pointer`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QCborArray` 的配置属性。初始化或状态切换时通过 `setConst_pointer(...)` 设置，之后用 `const_pointer()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:const_pointer`。
- 属性名：`QCborArray`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborArray::const_reference`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QCborArray` 的配置属性。初始化或状态切换时通过 `setConst_reference(...)` 设置，之后用 `const_reference()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:const_reference`。
- 属性名：`QCborArray`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborArray::difference_type`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QCborArray` 的配置属性。初始化或状态切换时通过 `setDifference_type(...)` 设置，之后用 `difference_type()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:difference_type`。
- 属性名：`QCborArray`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborArray::iterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QCborArray` 的配置属性。初始化或状态切换时通过 `setIterator(...)` 设置，之后用 `iterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:iterator`。
- 属性名：`QCborArray`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborArray::pointer`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QCborArray` 的配置属性。初始化或状态切换时通过 `setPointer(...)` 设置，之后用 `pointer()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:pointer`。
- 属性名：`QCborArray`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborArray::reference`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QCborArray` 的配置属性。初始化或状态切换时通过 `setReference(...)` 设置，之后用 `reference()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:reference`。
- 属性名：`QCborArray`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborArray::size_type`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QCborArray` 的配置属性。初始化或状态切换时通过 `setSize_type(...)` 设置，之后用 `size_type()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:size_type`。
- 属性名：`QCborArray`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborArray::value_type`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QCborArray` 的配置属性。初始化或状态切换时通过 `setValue_type(...)` 设置，之后用 `value_type()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:value_type`。
- 属性名：`QCborArray`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QCborArray::QCborArray()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCborArray` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborArray::QCborArray(std::initializer_list<QCborValue> args)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCborArray` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `args`：类型为 `std::initializer_list<QCborValue>`。没有默认值，调用时必须提供。传入 `std::initializer_list<QCborValue>` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QCborArray::QCborArray(const QCborArray &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCborArray` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QCborArray &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept, since 6.10] QCborArray::QCborArray(QCborArray &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCborArray` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `QCborArray &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QCborArray::~QCborArray()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCborArray` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QCborArray::append(QCborValue &&value)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QCborArray` 添加依赖、数据或子对象的 API `append`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `value`：类型为 `QCborValue &&`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborValue QCborArray::at(qsizetype i) const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `at`，用于取得 `QCborArray` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`QCborValue`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborArray::iterator QCborArray::begin()`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `begin`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QCborArray::iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborArray::const_iterator QCborArray::begin() const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `begin`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QCborArray::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborArray::const_iterator QCborArray::cbegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QCborArray::cbegin` 用于计算、查询或取得与“cbegin”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QCborArray::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborArray::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborArray::const_iterator QCborArray::cend() const`

**API 类别：** 成员函数说明

**中文解读：** `QCborArray::cend` 用于计算、查询或取得与“cend”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QCborArray::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborArray::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QCborArray::clear()`

**API 类别：** 成员函数说明

**中文解读：** 这是状态清理或重置 API `clear`。调用后原有数据、索引、缓存或绑定可能失效；使用前先确认它影响的是当前对象、子对象还是底层共享资源，之后重新检查状态。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] int QCborArray::compare(const QCborArray &other) const`

**API 类别：** 成员函数说明

**中文解读：** `QCborArray::compare` 用于计算、查询或取得与“比较”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `other`：类型为 `const QCborArray &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborArray::const_iterator QCborArray::constBegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QCborArray::constBegin` 用于计算、查询或取得与“const、起始位置”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QCborArray::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborArray::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborArray::const_iterator QCborArray::constEnd() const`

**API 类别：** 成员函数说明

**中文解读：** `QCborArray::constEnd` 用于计算、查询或取得与“const、结束”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QCborArray::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborArray::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QCborArray::contains(const QCborValue &value) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `contains`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `value`：类型为 `const QCborValue &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QCborArray::empty() const`

**API 类别：** 成员函数说明

**中文解读：** `QCborArray::empty` 用于计算、查询或取得与“空状态”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborArray::iterator QCborArray::end()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `end`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QCborArray::iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborArray::const_iterator QCborArray::end() const`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `end`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QCborArray::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborArray::iterator QCborArray::erase(QCborArray::const_iterator it)`

**API 类别：** 成员函数说明

**中文解读：** `QCborArray::erase` 用于计算、查询或取得与“erase”相关的操作。调用时要先确认当前状态和 `it` 的有效范围；返回类型是 `QCborArray::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborArray::iterator`。
- 参数 `it`：类型为 `QCborArray::const_iterator`。没有默认值，调用时必须提供。传入 `QCborArray::const_iterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborValue QCborArray::extract(QCborArray::ConstIterator it)`

**API 类别：** 成员函数说明

**中文解读：** `QCborArray::extract` 用于计算、查询或取得与“extract”相关的操作。调用时要先确认当前状态和 `it` 的有效范围；返回类型是 `QCborValue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborValue`。
- 参数 `it`：类型为 `QCborArray::ConstIterator`。没有默认值，调用时必须提供。传入 `QCborArray::ConstIterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborValueRef QCborArray::first()`

**API 类别：** 成员函数说明

**中文解读：** `QCborArray::first` 用于计算、查询或取得与“首项”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QCborValueRef`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborValueRef`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborValue QCborArray::first() const`

**API 类别：** 成员函数说明

**中文解读：** `QCborArray::first` 用于计算、查询或取得与“首项”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QCborValue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborValue`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QCborArray QCborArray::fromJsonArray(const QJsonArray &array)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromJsonArray`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QCborArray`。
- 参数 `array`：类型为 `const QJsonArray &`。没有默认值，调用时必须提供。传入 `const QJsonArray &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static noexcept, since 6.3] QCborArray QCborArray::fromJsonArray(QJsonArray &&array)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromJsonArray`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QCborArray`。
- 参数 `array`：类型为 `QJsonArray &&`。没有默认值，调用时必须提供。传入 `QJsonArray &&` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QCborArray QCborArray::fromStringList(const QStringList &list)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromStringList`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QCborArray`。
- 参数 `list`：类型为 `const QStringList &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QCborArray QCborArray::fromVariantList(const QVariantList &list)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromVariantList`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QCborArray`。
- 参数 `list`：类型为 `const QVariantList &`。没有默认值，调用时必须提供。传入 `const QVariantList &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QCborArray::insert(qsizetype i, QCborValue &&value)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QCborArray` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `QCborValue &&`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborArray::iterator QCborArray::insert(QCborArray::const_iterator before, const QCborValue &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QCborArray` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QCborArray::iterator`。
- 参数 `before`：类型为 `QCborArray::const_iterator`。没有默认值，调用时必须提供。传入 `QCborArray::const_iterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const QCborValue &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QCborArray::isEmpty() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isEmpty`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborValueRef QCborArray::last()`

**API 类别：** 成员函数说明

**中文解读：** `QCborArray::last` 用于计算、查询或取得与“末项”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QCborValueRef`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborValueRef`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborValue QCborArray::last() const`

**API 类别：** 成员函数说明

**中文解读：** `QCborArray::last` 用于计算、查询或取得与“末项”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QCborValue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborValue`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QCborArray::pop_back()`

**API 类别：** 成员函数说明

**中文解读：** `QCborArray::pop_back` 用于执行与“pop、末尾”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QCborArray::pop_front()`

**API 类别：** 成员函数说明

**中文解读：** `QCborArray::pop_front` 用于执行与“pop、开头”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QCborArray::prepend(QCborValue &&value)`

**API 类别：** 成员函数说明

**中文解读：** `QCborArray::prepend` 用于执行与“前置追加”相关的操作。调用时要先确认当前状态和 `value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `value`：类型为 `QCborValue &&`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QCborArray::push_back(const QCborValue &t)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QCborArray` 添加依赖、数据或子对象的 API `push_back`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `t`：类型为 `const QCborValue &`。没有默认值，调用时必须提供。传入 `const QCborValue &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QCborArray::push_front(const QCborValue &t)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QCborArray` 添加依赖、数据或子对象的 API `push_front`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `t`：类型为 `const QCborValue &`。没有默认值，调用时必须提供。传入 `const QCborValue &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QCborArray::removeAt(qsizetype i)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeAt`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QCborArray::removeFirst()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeFirst`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QCborArray::removeLast()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeLast`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] qsizetype QCborArray::size() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `size`，返回 `QCborArray` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QCborArray::swap(QCborArray &other)`

**API 类别：** 成员函数说明

**中文解读：** `QCborArray::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QCborArray &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborValue QCborArray::takeAt(qsizetype i)`

**API 类别：** 成员函数说明

**中文解读：** `QCborArray::takeAt` 用于计算、查询或取得与“取出、按位置访问”相关的操作。调用时要先确认当前状态和 `i` 的有效范围；返回类型是 `QCborValue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborValue`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborValue QCborArray::takeFirst()`

**API 类别：** 成员函数说明

**中文解读：** `QCborArray::takeFirst` 用于计算、查询或取得与“取出、首项”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QCborValue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborValue`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborValue QCborArray::takeLast()`

**API 类别：** 成员函数说明

**中文解读：** `QCborArray::takeLast` 用于计算、查询或取得与“取出、末项”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QCborValue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborValue`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborValue QCborArray::toCborValue() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toCborValue`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QCborValue`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJsonArray QCborArray::toJsonArray() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toJsonArray`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QJsonArray`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVariantList QCborArray::toVariantList() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toVariantList`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QVariantList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborArray QCborArray::operator+(const QCborValue &v) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCborArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QCborArray`。
- 参数 `v`：类型为 `const QCborValue &`。没有默认值，调用时必须提供。传入 `const QCborValue &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborArray &QCborArray::operator+=(const QCborValue &v)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCborArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QCborArray &`。
- 参数 `v`：类型为 `const QCborValue &`。没有默认值，调用时必须提供。传入 `const QCborValue &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborArray &QCborArray::operator<<(const QCborValue &v)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCborArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QCborArray &`。
- 参数 `v`：类型为 `const QCborValue &`。没有默认值，调用时必须提供。传入 `const QCborValue &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.10] QCborArray &QCborArray::operator=(QCborArray &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCborArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QCborArray &`。
- 参数 `other`：类型为 `QCborArray &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QCborArray &QCborArray::operator=(const QCborArray &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCborArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QCborArray &`。
- 参数 `other`：类型为 `const QCborArray &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborValueRef QCborArray::operator[](qsizetype i)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCborArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QCborValueRef`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QCborValue QCborArray::operator[](qsizetype i) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCborArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`const QCborValue`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator!=(const QCborArray &lhs, const QCborArray &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QCborArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QCborArray &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QCborArray &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator<(const QCborArray &lhs, const QCborArray &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QCborArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QCborArray &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QCborArray &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator<=(const QCborArray &lhs, const QCborArray &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QCborArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QCborArray &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QCborArray &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator==(const QCborArray &lhs, const QCborArray &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QCborArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QCborArray &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QCborArray &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator>(const QCborArray &lhs, const QCborArray &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QCborArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QCborArray &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QCborArray &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator>=(const QCborArray &lhs, const QCborArray &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QCborArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QCborArray &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QCborArray &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `class ConstIterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QCborArray` 暴露的类型声明 `Const、Iterator`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `class Iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QCborArray` 暴露的类型声明 `Iterator`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const_iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QCborArray` 的 `const、iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const_pointer`

**API 类别：** 公有类型

**中文解读：** 这是 `QCborArray` 的 `const、pointer` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const_reference`

**API 类别：** 公有类型

**中文解读：** 这是 `QCborArray` 的 `const、reference` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `difference_type`

**API 类别：** 公有类型

**中文解读：** 这是 `QCborArray` 的 `difference、类型` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QCborArray` 的 `iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `pointer`

**API 类别：** 公有类型

**中文解读：** 这是 `QCborArray` 的 `pointer` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `reference`

**API 类别：** 公有类型

**中文解读：** 这是 `QCborArray` 的 `reference` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `size_type`

**API 类别：** 公有类型

**中文解读：** 这是 `QCborArray` 的 `尺寸或数量、类型` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `value_type`

**API 类别：** 公有类型

**中文解读：** 这是 `QCborArray` 的 `值访问、类型` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void append(const QCborValue &value)`

**API 类别：** 公有函数

**中文解读：** 这是向 `QCborArray` 添加依赖、数据或子对象的 API `append`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `value`：类型为 `const QCborValue &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborArray::iterator erase(QCborArray::iterator it)`

**API 类别：** 公有函数

**中文解读：** `QCborArray::erase` 用于计算、查询或取得与“erase”相关的操作。调用时要先确认当前状态和 `it` 的有效范围；返回类型是 `QCborArray::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborArray::iterator`。
- 参数 `it`：类型为 `QCborArray::iterator`。没有默认值，调用时必须提供。传入 `QCborArray::iterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborValue extract(QCborArray::Iterator it)`

**API 类别：** 公有函数

**中文解读：** `QCborArray::extract` 用于计算、查询或取得与“extract”相关的操作。调用时要先确认当前状态和 `it` 的有效范围；返回类型是 `QCborValue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCborValue`。
- 参数 `it`：类型为 `QCborArray::Iterator`。没有默认值，调用时必须提供。传入 `QCborArray::Iterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void insert(qsizetype i, const QCborValue &value)`

**API 类别：** 公有函数

**中文解读：** 这是向 `QCborArray` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const QCborValue &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCborArray::iterator insert(QCborArray::iterator before, const QCborValue &value)`

**API 类别：** 公有函数

**中文解读：** 这是向 `QCborArray` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QCborArray::iterator`。
- 参数 `before`：类型为 `QCborArray::iterator`。没有默认值，调用时必须提供。传入 `QCborArray::iterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const QCborValue &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void prepend(const QCborValue &value)`

**API 类别：** 公有函数

**中文解读：** `QCborArray::prepend` 用于执行与“前置追加”相关的操作。调用时要先确认当前状态和 `value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `value`：类型为 `const QCborValue &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

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

`QCborArray` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
