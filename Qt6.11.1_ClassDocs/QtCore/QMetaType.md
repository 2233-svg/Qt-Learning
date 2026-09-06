# QMetaType

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“MetaType”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QMetaType` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QMetaType>`
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

- `enum Type { Void, Bool, Int, UInt, Double, …, UnknownType }`
- `enum TypeFlag { NeedsConstruction, NeedsCopyConstruction, NeedsMoveConstruction, NeedsDestruction, RelocatableType, …, IsConst }`
- `flags TypeFlags`

### 公有函数

- `(since 6.0) QMetaType()`
- `QMetaType(int typeId)`
- `(since 6.0) qsizetype alignOf() const`
- `(since 6.0) QPartialOrdering compare(const void *lhs, const void *rhs) const`
- `void * construct(void *where, const void *copy = nullptr) const`
- `void * create(const void *copy = nullptr) const`
- `bool debugStream(QDebug &dbg, const void *rhs)`
- `void destroy(void *data) const`
- `void destruct(void *data) const`
- `(since 6.0) bool equals(const void *lhs, const void *rhs) const`
- `QMetaType::TypeFlags flags() const`
- `(since 6.1) bool hasRegisteredDataStreamOperators() const`
- `(since 6.0) bool hasRegisteredDebugStreamOperator() const`
- `int id() const`
- `(since 6.5) bool isCopyConstructible() const`
- `(since 6.5) bool isDefaultConstructible() const`
- `(since 6.5) bool isDestructible() const`
- `bool isEqualityComparable() const`
- `(since 6.5) bool isMoveConstructible() const`
- `bool isOrdered() const`
- `bool isRegistered() const`
- `bool isValid() const`
- `bool load(QDataStream &stream, void *data) const`
- `const QMetaObject * metaObject() const`
- `const char * name() const`
- `(since 6.5) void registerType() const`
- `bool save(QDataStream &stream, const void *data) const`
- `qsizetype sizeOf() const`
- `(since 6.6) QMetaType underlyingType() const`

### 静态公有成员

- `bool canConvert(QMetaType fromType, QMetaType toType)`
- `bool canView(QMetaType fromType, QMetaType toType)`
- `bool convert(QMetaType fromType, const void *from, QMetaType toType, void *to)`
- `QMetaType fromName(QByteArrayView typeName)`
- `QMetaType fromType()`
- `bool hasRegisteredConverterFunction(QMetaType fromType, QMetaType toType)`
- `bool hasRegisteredConverterFunction()`
- `bool hasRegisteredMutableViewFunction(QMetaType fromType, QMetaType toType)`
- `(since 6.0) bool hasRegisteredMutableViewFunction()`
- `bool isRegistered(int type)`
- `bool registerConverter()`
- `bool registerConverter(To (From::*)() const function)`
- `bool registerConverter(To (From::*)(bool *) const function)`
- `bool registerConverter(UnaryFunction function)`
- `(since 6.0) bool registerMutableView(To (From::*)() function)`
- `(since 6.0) bool registerMutableView(UnaryFunction function)`
- `(since 6.0) bool view(QMetaType fromType, void *from, QMetaType toType, void *to)`

### 相关非成员函数

- `(since 6.4) size_t qHash(QMetaType key, size_t seed = 0)`
- `int qMetaTypeId()`
- `int qRegisterMetaType()`
- `(since 6.5) int qRegisterMetaType(QMetaType meta)`
- `bool operator!=(const QMetaType &lhs, const QMetaType &rhs)`
- `(since 6.5) QDebug operator<<(QDebug d, QMetaType m)`
- `bool operator==(const QMetaType &lhs, const QMetaType &rhs)`

### 公开宏

- `Q_DECLARE_ASSOCIATIVE_CONTAINER_METATYPE(Container)`
- `Q_DECLARE_METATYPE(Type)`
- `Q_DECLARE_OPAQUE_POINTER(PointerType)`
- `Q_DECLARE_SEQUENTIAL_CONTAINER_METATYPE(Container)`
- `Q_DECLARE_SMART_POINTER_METATYPE(SmartPointer)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 62 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QMetaType::Type`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QMetaType` 暴露的类型声明 `类型`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Type`。
- 属性名：`QMetaType`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QMetaType::TypeFlagflags QMetaType::TypeFlags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QMetaType` 暴露的类型声明 `类型、Flagflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:TypeFlagflags QMetaType::TypeFlags`。
- 属性名：`QMetaType`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept, since 6.0] QMetaType::QMetaType()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMetaType` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QMetaType::QMetaType(int typeId)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMetaType` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `typeId`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr, since 6.0] qsizetype QMetaType::alignOf() const`

**API 类别：** 成员函数说明

**中文解读：** `QMetaType::alignOf` 用于计算、查询或取得与“align、Of”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QMetaType::canConvert(QMetaType fromType, QMetaType toType)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `canConvert`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `fromType`：类型为 `QMetaType`。没有默认值，调用时必须提供。传入 `QMetaType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `toType`：类型为 `QMetaType`。没有默认值，调用时必须提供。传入 `QMetaType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QMetaType::canView(QMetaType fromType, QMetaType toType)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `canView`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `fromType`：类型为 `QMetaType`。没有默认值，调用时必须提供。传入 `QMetaType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `toType`：类型为 `QMetaType`。没有默认值，调用时必须提供。传入 `QMetaType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QPartialOrdering QMetaType::compare(const void *lhs, const void *rhs) const`

**API 类别：** 成员函数说明

**中文解读：** `QMetaType::compare` 用于计算、查询或取得与“比较”相关的操作。调用时要先确认当前状态和 `lhs`、`rhs` 的有效范围；返回类型是 `QPartialOrdering`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPartialOrdering`。
- 参数 `lhs`：类型为 `const void *`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const void *`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void *QMetaType::construct(void *where, const void *copy = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** `QMetaType::construct` 用于计算、查询或取得与“construct”相关的操作。调用时要先确认当前状态和 `where`、`copy` 的有效范围；返回类型是 `void *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void *`。
- 参数 `where`：类型为 `void *`。没有默认值，调用时必须提供。传入 `void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `copy`：类型为 `const void *`。默认值为 `nullptr`。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QMetaType::convert(QMetaType fromType, const void *from, QMetaType toType, void *to)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `convert`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `fromType`：类型为 `QMetaType`。没有默认值，调用时必须提供。传入 `QMetaType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `from`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `toType`：类型为 `QMetaType`。没有默认值，调用时必须提供。传入 `QMetaType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `to`：类型为 `void *`。没有默认值，调用时必须提供。传入 `void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void *QMetaType::create(const void *copy = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** `QMetaType::create` 用于计算、查询或取得与“创建”相关的操作。调用时要先确认当前状态和 `copy` 的有效范围；返回类型是 `void *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void *`。
- 参数 `copy`：类型为 `const void *`。默认值为 `nullptr`。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMetaType::debugStream(QDebug &dbg, const void *rhs)`

**API 类别：** 成员函数说明

**中文解读：** `QMetaType::debugStream` 用于计算、查询或取得与“调试输出、Stream”相关的操作。调用时要先确认当前状态和 `dbg`、`rhs` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `dbg`：类型为 `QDebug &`。没有默认值，调用时必须提供。传入 `QDebug &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `rhs`：类型为 `const void *`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMetaType::destroy(void *data) const`

**API 类别：** 成员函数说明

**中文解读：** `QMetaType::destroy` 用于执行与“destroy”相关的操作。调用时要先确认当前状态和 `data` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `data`：类型为 `void *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMetaType::destruct(void *data) const`

**API 类别：** 成员函数说明

**中文解读：** `QMetaType::destruct` 用于执行与“destruct”相关的操作。调用时要先确认当前状态和 `data` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `data`：类型为 `void *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] bool QMetaType::equals(const void *lhs, const void *rhs) const`

**API 类别：** 成员函数说明

**中文解读：** `QMetaType::equals` 用于计算、查询或取得与“equals”相关的操作。调用时要先确认当前状态和 `lhs`、`rhs` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const void *`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const void *`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr] QMetaType::TypeFlags QMetaType::flags() const`

**API 类别：** 成员函数说明

**中文解读：** `QMetaType::flags` 用于计算、查询或取得与“标志”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMetaType::TypeFlags`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMetaType::TypeFlags`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QMetaType QMetaType::fromName(QByteArrayView typeName)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromName`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QMetaType`。
- 参数 `typeName`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static constexpr] template <typename T> QMetaType QMetaType::fromType()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromType`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename T> QMetaType`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QMetaType::hasRegisteredConverterFunction(QMetaType fromType, QMetaType toType)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `hasRegisteredConverterFunction`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `fromType`：类型为 `QMetaType`。没有默认值，调用时必须提供。传入 `QMetaType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `toType`：类型为 `QMetaType`。没有默认值，调用时必须提供。传入 `QMetaType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] template <typename From, typename To> bool QMetaType::hasRegisteredConverterFunction()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `hasRegisteredConverterFunction`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename From, typename To> bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] bool QMetaType::hasRegisteredDataStreamOperators() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasRegisteredDataStreamOperators`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] bool QMetaType::hasRegisteredDebugStreamOperator() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasRegisteredDebugStreamOperator`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QMetaType::hasRegisteredMutableViewFunction(QMetaType fromType, QMetaType toType)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `hasRegisteredMutableViewFunction`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `fromType`：类型为 `QMetaType`。没有默认值，调用时必须提供。传入 `QMetaType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `toType`：类型为 `QMetaType`。没有默认值，调用时必须提供。传入 `QMetaType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.0] template <typename From, typename To> bool QMetaType::hasRegisteredMutableViewFunction()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `hasRegisteredMutableViewFunction`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename From, typename To> bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QMetaType::id() const`

**API 类别：** 成员函数说明

**中文解读：** `QMetaType::id` 用于计算、查询或取得与“id”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.5] bool QMetaType::isCopyConstructible() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isCopyConstructible`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.5] bool QMetaType::isDefaultConstructible() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isDefaultConstructible`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.5] bool QMetaType::isDestructible() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isDestructible`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMetaType::isEqualityComparable() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isEqualityComparable`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.5] bool QMetaType::isMoveConstructible() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isMoveConstructible`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMetaType::isOrdered() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isOrdered`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool QMetaType::isRegistered() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isRegistered`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QMetaType::isRegistered(int type)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `isRegistered`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `type`：类型为 `int`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] bool QMetaType::isValid() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isValid`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMetaType::load(QDataStream &stream, void *data) const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `load`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`bool`。
- 参数 `stream`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `data`：类型为 `void *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr] const QMetaObject *QMetaType::metaObject() const`

**API 类别：** 成员函数说明

**中文解读：** `QMetaType::metaObject` 用于计算、查询或取得与“meta、Object”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QMetaObject *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QMetaObject *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr] const char *QMetaType::name() const`

**API 类别：** 成员函数说明

**中文解读：** `QMetaType::name` 用于计算、查询或取得与“名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const char *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const char *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] template <typename From, typename To> bool QMetaType::registerConverter()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `registerConverter`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename From, typename To> bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] template <typename From, typename To> bool QMetaType::registerConverter(To (From::*)() const function)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `registerConverter`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename From, typename To> bool`。
- 参数 `function`：类型为 `To (From::*)() const`。没有默认值，调用时必须提供。传入 `To (From::*)() const` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] template <typename From, typename To> bool QMetaType::registerConverter(To (From::*)(bool *) const function)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `registerConverter`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename From, typename To> bool`。
- 参数 `function`：类型为 `To (From::*)(bool *) const`。没有默认值，调用时必须提供。传入 `To (From::*)(bool *) const` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] template < typename From, typename To, typename UnaryFunction > bool QMetaType::registerConverter(UnaryFunction function)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `registerConverter`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template < typename From, typename To, typename UnaryFunction > bool`。
- 参数 `function`：类型为 `UnaryFunction`。没有默认值，调用时必须提供。传入 `UnaryFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.0] template <typename From, typename To> bool QMetaType::registerMutableView(To (From::*)() function)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `registerMutableView`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename From, typename To> bool`。
- 参数 `function`：类型为 `To (From::*)()`。没有默认值，调用时必须提供。传入 `To (From::*)()` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.0] template < typename From, typename To, typename UnaryFunction > bool QMetaType::registerMutableView(UnaryFunction function)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `registerMutableView`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template < typename From, typename To, typename UnaryFunction > bool`。
- 参数 `function`：类型为 `UnaryFunction`。没有默认值，调用时必须提供。传入 `UnaryFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] void QMetaType::registerType() const`

**API 类别：** 成员函数说明

**中文解读：** `QMetaType::registerType` 用于执行与“注册、类型”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMetaType::save(QDataStream &stream, const void *data) const`

**API 类别：** 成员函数说明

**中文解读：** `QMetaType::save` 用于计算、查询或取得与“保存”相关的操作。调用时要先确认当前状态和 `stream`、`data` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `stream`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `data`：类型为 `const void *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr] qsizetype QMetaType::sizeOf() const`

**API 类别：** 成员函数说明

**中文解读：** `QMetaType::sizeOf` 用于计算、查询或取得与“尺寸或数量、Of”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] QMetaType QMetaType::underlyingType() const`

**API 类别：** 成员函数说明

**中文解读：** `QMetaType::underlyingType` 用于计算、查询或取得与“underlying、类型”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMetaType`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMetaType`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.0] bool QMetaType::view(QMetaType fromType, void *from, QMetaType toType, void *to)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `view`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `fromType`：类型为 `QMetaType`。没有默认值，调用时必须提供。传入 `QMetaType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `from`：类型为 `void *`。没有默认值，调用时必须提供。传入 `void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `toType`：类型为 `QMetaType`。没有默认值，调用时必须提供。传入 `QMetaType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `to`：类型为 `void *`。没有默认值，调用时必须提供。传入 `void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.4] size_t qHash(QMetaType key, size_t seed = 0)`

**API 类别：** 相关非成员函数

**中文解读：** `QMetaType::qHash` 用于计算、查询或取得与“q、Hash”相关的操作。调用时要先确认当前状态和 `key`、`seed` 的有效范围；返回类型是 `size_t`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`size_t`。
- 参数 `key`：类型为 `QMetaType`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `seed`：类型为 `size_t`。默认值为 `0`。传入 `size_t` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr] template <typename T> int qMetaTypeId()`

**API 类别：** 相关非成员函数

**中文解读：** `QMetaType::qMetaTypeId` 用于计算、查询或取得与“q、Meta、类型、Id”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `template <typename T> int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename T> int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr] template <typename T> int qRegisterMetaType()`

**API 类别：** 相关非成员函数

**中文解读：** `QMetaType::qRegisterMetaType` 用于计算、查询或取得与“q、注册、Meta、类型”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `template <typename T> int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename T> int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] int qRegisterMetaType(QMetaType meta)`

**API 类别：** 相关非成员函数

**中文解读：** `QMetaType::qRegisterMetaType` 用于计算、查询或取得与“q、注册、Meta、类型”相关的操作。调用时要先确认当前状态和 `meta` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `meta`：类型为 `QMetaType`。没有默认值，调用时必须提供。传入 `QMetaType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator!=(const QMetaType &lhs, const QMetaType &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMetaType` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QMetaType &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QMetaType &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] QDebug operator<<(QDebug d, QMetaType m)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMetaType` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug`。
- 参数 `d`：类型为 `QDebug`。没有默认值，调用时必须提供。传入 `QDebug` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `m`：类型为 `QMetaType`。没有默认值，调用时必须提供。传入 `QMetaType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator==(const QMetaType &lhs, const QMetaType &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMetaType` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QMetaType &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QMetaType &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_DECLARE_ASSOCIATIVE_CONTAINER_METATYPE(Container)`

**API 类别：** 宏说明

**中文解读：** `QMetaType::Q_DECLARE_ASSOCIATIVE_CONTAINER_METATYPE` 用于执行与“METATYPE”相关的操作。调用时要先确认当前状态和 `Container` 的有效范围；返回类型是 `未标注`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`由运算符声明决定`。
- 参数 `Container`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_DECLARE_METATYPE(Type)`

**API 类别：** 宏说明

**中文解读：** `QMetaType::Q_DECLARE_METATYPE` 用于执行与“METATYPE”相关的操作。调用时要先确认当前状态和 `Type` 的有效范围；返回类型是 `未标注`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`由运算符声明决定`。
- 参数 `Type`：类型为 `未标注`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_DECLARE_OPAQUE_POINTER(PointerType)`

**API 类别：** 宏说明

**中文解读：** `QMetaType::Q_DECLARE_OPAQUE_POINTER` 用于执行与“POINTER”相关的操作。调用时要先确认当前状态和 `PointerType` 的有效范围；返回类型是 `未标注`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`由运算符声明决定`。
- 参数 `PointerType`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_DECLARE_SEQUENTIAL_CONTAINER_METATYPE(Container)`

**API 类别：** 宏说明

**中文解读：** `QMetaType::Q_DECLARE_SEQUENTIAL_CONTAINER_METATYPE` 用于执行与“METATYPE”相关的操作。调用时要先确认当前状态和 `Container` 的有效范围；返回类型是 `未标注`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`由运算符声明决定`。
- 参数 `Container`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_DECLARE_SMART_POINTER_METATYPE(SmartPointer)`

**API 类别：** 宏说明

**中文解读：** `QMetaType::Q_DECLARE_SMART_POINTER_METATYPE` 用于执行与“METATYPE”相关的操作。调用时要先确认当前状态和 `SmartPointer` 的有效范围；返回类型是 `未标注`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`由运算符声明决定`。
- 参数 `SmartPointer`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum TypeFlag { NeedsConstruction, NeedsCopyConstruction, NeedsMoveConstruction, NeedsDestruction, RelocatableType, …, IsConst }`

**API 类别：** 公有类型

**中文解读：** 这是 `QMetaType` 暴露的类型声明 `类型、Flag`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags TypeFlags`

**API 类别：** 公有类型

**中文解读：** 这是 `QMetaType` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

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

`QMetaType` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
