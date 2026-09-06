# QJniObject

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“Jni对象”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QJniObject` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QJniObject>`
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

### 公有函数

- `QJniObject()`
- `QJniObject(const char *className)`
- `QJniObject(jclass clazz)`
- `QJniObject(jobject object)`
- `(since 6.4) QJniObject(const char *className, Args &&... args)`
- `(since 6.4) QJniObject(jclass clazz, Args &&... args)`
- `QJniObject(const char *className, const char *signature, ...)`
- `QJniObject(jclass clazz, const char *signature, ...)`
- `~QJniObject()`
- `(since 6.4) auto callMethod(const char *methodName, Args &&... args) const`
- `(since 6.4) auto callMethod(const char *methodName, const char *signature, Args &&... args) const`
- `(since 6.4) QJniObject callObjectMethod(const char *methodName, Args &&... args) const`
- `QJniObject callObjectMethod(const char *methodName, const char *signature, ...) const`
- `(since 6.2) QByteArray className() const`
- `auto getField(const char *fieldName) const`
- `QJniObject getObjectField(const char *fieldName) const`
- `QJniObject getObjectField(const char *fieldName, const char *signature) const`
- `bool isValid() const`
- `jobject object() const`
- `T object() const`
- `(since 6.2) jclass objectClass() const`
- `auto setField(const char *fieldName, Type value)`
- `auto setField(const char *fieldName, const char *signature, Type value)`
- `(since 6.8) void swap(QJniObject &other)`
- `QString toString() const`
- `QJniObject & operator=(T object)`

### 静态公有成员

- `(since 6.7) auto callStaticMethod(const char *methodName, Args &&... args)`
- `(since 6.4) auto callStaticMethod(const char *className, const char *methodName, Args &&... args)`
- `(since 6.4) auto callStaticMethod(jclass clazz, const char *methodName, Args &&... args)`
- `(since 6.4) auto callStaticMethod(jclass clazz, jmethodID methodId, Args &&... args)`
- `(since 6.4) auto callStaticMethod(const char *className, const char *methodName, const char *signature, Args &&... args)`
- `auto callStaticMethod(jclass clazz, const char *methodName, const char *signature, Args &&... args)`
- `(since 6.4) QJniObject callStaticObjectMethod(const char *className, const char *methodName, Args &&... args)`
- `(since 6.4) QJniObject callStaticObjectMethod(jclass clazz, const char *methodName, Args &&... args)`
- `QJniObject callStaticObjectMethod(jclass clazz, jmethodID methodId, ...)`
- `QJniObject callStaticObjectMethod(const char *className, const char *methodName, const char *signature, ...)`
- `QJniObject callStaticObjectMethod(jclass clazz, const char *methodName, const char *signature, ...)`
- `(since 6.4) auto construct(Args &&... args)`
- `QJniObject fromLocalRef(jobject localRef)`
- `QJniObject fromString(const QString &string)`
- `auto getStaticField(const char *fieldName)`
- `auto getStaticField(const char *className, const char *fieldName)`
- `auto getStaticField(jclass clazz, const char *fieldName)`
- `QJniObject getStaticObjectField(const char *className, const char *fieldName)`
- `QJniObject getStaticObjectField(jclass clazz, const char *fieldName)`
- `QJniObject getStaticObjectField(const char *className, const char *fieldName, const char *signature)`
- `QJniObject getStaticObjectField(jclass clazz, const char *fieldName, const char *signature)`
- `bool isClassAvailable(const char *className)`
- `auto setStaticField(const char *fieldName, Type value)`
- `auto setStaticField(const char *className, const char *fieldName, Type value)`
- `auto setStaticField(jclass clazz, const char *fieldName, Type value)`
- `auto setStaticField(const char *className, const char *fieldName, const char *signature, Type value)`
- `auto setStaticField(jclass clazz, const char *fieldName, const char *signature, Type value)`

### 相关非成员函数

- `bool operator!=(const QJniObject &o1, const QJniObject &o2)`
- `bool operator==(const QJniObject &o1, const QJniObject &o2)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 54 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QJniObject::QJniObject()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJniObject` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QJniObject::QJniObject(const char *className)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJniObject` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `className`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QJniObject::QJniObject(jclass clazz)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJniObject` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `clazz`：类型为 `jclass`。没有默认值，调用时必须提供。传入 `jclass` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJniObject::QJniObject(jobject object)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJniObject` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `object`：类型为 `jobject`。没有默认值，调用时必须提供。传入 `jobject` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit, since 6.4] template <typename... Args> QJniObject::QJniObject(const char *className, Args &&... args)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJniObject` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `className`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `args`：类型为 `Args &&...`。没有默认值，调用时必须提供。传入 `Args &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit, since 6.4] template <typename... Args> QJniObject::QJniObject(jclass clazz, Args &&... args)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJniObject` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `clazz`：类型为 `jclass`。没有默认值，调用时必须提供。传入 `jclass` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `args`：类型为 `Args &&...`。没有默认值，调用时必须提供。传入 `Args &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QJniObject::QJniObject(const char *className, const char *signature, ...)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJniObject` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `className`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `signature`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `...`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QJniObject::QJniObject(jclass clazz, const char *signature, ...)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJniObject` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `clazz`：类型为 `jclass`。没有默认值，调用时必须提供。传入 `jclass` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `signature`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `...`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QJniObject::~QJniObject()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJniObject` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.4] template <typename ReturnType = void, typename... Args> auto QJniObject::callMethod(const char *methodName, Args &&... args) const`

**API 类别：** 成员函数说明

**中文解读：** `QJniObject::callMethod` 用于计算、查询或取得与“call、Method”相关的操作。调用时要先确认当前状态和 `methodName`、`args` 的有效范围；返回类型是 `template <typename ReturnType = void, typename... Args> auto`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename ReturnType = void, typename... Args> auto`。
- 参数 `methodName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `args`：类型为 `Args &&...`。没有默认值，调用时必须提供。传入 `Args &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.4] template <typename ReturnType = void, typename... Args> auto QJniObject::callMethod(const char *methodName, const char *signature, Args &&... args) const`

**API 类别：** 成员函数说明

**中文解读：** `QJniObject::callMethod` 用于计算、查询或取得与“call、Method”相关的操作。调用时要先确认当前状态和 `methodName`、`signature`、`args` 的有效范围；返回类型是 `template <typename ReturnType = void, typename... Args> auto`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename ReturnType = void, typename... Args> auto`。
- 参数 `methodName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `signature`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `args`：类型为 `Args &&...`。没有默认值，调用时必须提供。传入 `Args &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.4] template <typename Ret, typename... Args> QJniObject QJniObject::callObjectMethod(const char *methodName, Args &&... args) const`

**API 类别：** 成员函数说明

**中文解读：** `QJniObject::callObjectMethod` 用于计算、查询或取得与“call、Object、Method”相关的操作。调用时要先确认当前状态和 `methodName`、`args` 的有效范围；返回类型是 `template <typename Ret, typename... Args> QJniObject`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Ret, typename... Args> QJniObject`。
- 参数 `methodName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `args`：类型为 `Args &&...`。没有默认值，调用时必须提供。传入 `Args &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJniObject QJniObject::callObjectMethod(const char *methodName, const char *signature, ...) const`

**API 类别：** 成员函数说明

**中文解读：** `QJniObject::callObjectMethod` 用于计算、查询或取得与“call、Object、Method”相关的操作。调用时要先确认当前状态和 `methodName`、`signature`、`...` 的有效范围；返回类型是 `QJniObject`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QJniObject`。
- 参数 `methodName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `signature`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `...`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.7] template < typename Klass, typename ReturnType = void, typename... Args > auto QJniObject::callStaticMethod(const char *methodName, Args &&... args)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `callStaticMethod`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template < typename Klass, typename ReturnType = void, typename... Args > auto`。
- 参数 `methodName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `args`：类型为 `Args &&...`。没有默认值，调用时必须提供。传入 `Args &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.4] template <typename ReturnType = void, typename... Args> auto QJniObject::callStaticMethod(const char *className, const char *methodName, Args &&... args)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `callStaticMethod`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename ReturnType = void, typename... Args> auto`。
- 参数 `className`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `methodName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `args`：类型为 `Args &&...`。没有默认值，调用时必须提供。传入 `Args &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.4] template <typename ReturnType = void, typename... Args> auto QJniObject::callStaticMethod(jclass clazz, const char *methodName, Args &&... args)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `callStaticMethod`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename ReturnType = void, typename... Args> auto`。
- 参数 `clazz`：类型为 `jclass`。没有默认值，调用时必须提供。传入 `jclass` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `methodName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `args`：类型为 `Args &&...`。没有默认值，调用时必须提供。传入 `Args &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.4] template <typename ReturnType = void, typename... Args> auto QJniObject::callStaticMethod(jclass clazz, jmethodID methodId, Args &&... args)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `callStaticMethod`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename ReturnType = void, typename... Args> auto`。
- 参数 `clazz`：类型为 `jclass`。没有默认值，调用时必须提供。传入 `jclass` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `methodId`：类型为 `jmethodID`。没有默认值，调用时必须提供。传入 `jmethodID` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `args`：类型为 `Args &&...`。没有默认值，调用时必须提供。传入 `Args &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.4] template <typename Ret = void, typename... Args> auto QJniObject::callStaticMethod(const char *className, const char *methodName, const char *signature, Args &&... args)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `callStaticMethod`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename Ret = void, typename... Args> auto`。
- 参数 `className`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `methodName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `signature`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `args`：类型为 `Args &&...`。没有默认值，调用时必须提供。传入 `Args &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] template <typename Ret = void, typename... Args> auto QJniObject::callStaticMethod(jclass clazz, const char *methodName, const char *signature, Args &&... args)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `callStaticMethod`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename Ret = void, typename... Args> auto`。
- 参数 `clazz`：类型为 `jclass`。没有默认值，调用时必须提供。传入 `jclass` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `methodName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `signature`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `args`：类型为 `Args &&...`。没有默认值，调用时必须提供。传入 `Args &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.4] template <typename Ret, typename... Args> QJniObject QJniObject::callStaticObjectMethod(const char *className, const char *methodName, Args &&... args)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `callStaticObjectMethod`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename Ret, typename... Args> QJniObject`。
- 参数 `className`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `methodName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `args`：类型为 `Args &&...`。没有默认值，调用时必须提供。传入 `Args &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.4] template <typename Ret, typename... Args> QJniObject QJniObject::callStaticObjectMethod(jclass clazz, const char *methodName, Args &&... args)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `callStaticObjectMethod`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename Ret, typename... Args> QJniObject`。
- 参数 `clazz`：类型为 `jclass`。没有默认值，调用时必须提供。传入 `jclass` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `methodName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `args`：类型为 `Args &&...`。没有默认值，调用时必须提供。传入 `Args &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QJniObject QJniObject::callStaticObjectMethod(jclass clazz, jmethodID methodId, ...)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `callStaticObjectMethod`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QJniObject`。
- 参数 `clazz`：类型为 `jclass`。没有默认值，调用时必须提供。传入 `jclass` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `methodId`：类型为 `jmethodID`。没有默认值，调用时必须提供。传入 `jmethodID` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `...`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QJniObject QJniObject::callStaticObjectMethod(const char *className, const char *methodName, const char *signature, ...)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `callStaticObjectMethod`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QJniObject`。
- 参数 `className`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `methodName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `signature`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `...`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QJniObject QJniObject::callStaticObjectMethod(jclass clazz, const char *methodName, const char *signature, ...)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `callStaticObjectMethod`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QJniObject`。
- 参数 `clazz`：类型为 `jclass`。没有默认值，调用时必须提供。传入 `jclass` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `methodName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `signature`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `...`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] QByteArray QJniObject::className() const`

**API 类别：** 成员函数说明

**中文解读：** `QJniObject::className` 用于计算、查询或取得与“class、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.4] template <typename Class, typename... Args> auto QJniObject::construct(Args &&... args)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `construct`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename Class, typename... Args> auto`。
- 参数 `args`：类型为 `Args &&...`。没有默认值，调用时必须提供。传入 `Args &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QJniObject QJniObject::fromLocalRef(jobject localRef)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromLocalRef`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QJniObject`。
- 参数 `localRef`：类型为 `jobject`。没有默认值，调用时必须提供。传入 `jobject` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QJniObject QJniObject::fromString(const QString &string)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromString`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QJniObject`。
- 参数 `string`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Type> auto QJniObject::getField(const char *fieldName) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJniObject` 的核心操作 `getField`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`template <typename Type> auto`。
- 参数 `fieldName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename T> QJniObject QJniObject::getObjectField(const char *fieldName) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJniObject` 的核心操作 `getObjectField`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`template <typename T> QJniObject`。
- 参数 `fieldName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJniObject QJniObject::getObjectField(const char *fieldName, const char *signature) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJniObject` 的核心操作 `getObjectField`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QJniObject`。
- 参数 `fieldName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `signature`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] template <typename Klass, typename T> auto QJniObject::getStaticField(const char *fieldName)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `getStaticField`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename Klass, typename T> auto`。
- 参数 `fieldName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] template <typename Type> auto QJniObject::getStaticField(const char *className, const char *fieldName)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `getStaticField`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename Type> auto`。
- 参数 `className`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `fieldName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] template <typename Type> auto QJniObject::getStaticField(jclass clazz, const char *fieldName)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `getStaticField`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename Type> auto`。
- 参数 `clazz`：类型为 `jclass`。没有默认值，调用时必须提供。传入 `jclass` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `fieldName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] template <typename T> QJniObject QJniObject::getStaticObjectField(const char *className, const char *fieldName)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `getStaticObjectField`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename T> QJniObject`。
- 参数 `className`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `fieldName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] template <typename T> QJniObject QJniObject::getStaticObjectField(jclass clazz, const char *fieldName)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `getStaticObjectField`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename T> QJniObject`。
- 参数 `clazz`：类型为 `jclass`。没有默认值，调用时必须提供。传入 `jclass` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `fieldName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QJniObject QJniObject::getStaticObjectField(const char *className, const char *fieldName, const char *signature)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `getStaticObjectField`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QJniObject`。
- 参数 `className`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `fieldName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `signature`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QJniObject QJniObject::getStaticObjectField(jclass clazz, const char *fieldName, const char *signature)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `getStaticObjectField`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QJniObject`。
- 参数 `clazz`：类型为 `jclass`。没有默认值，调用时必须提供。传入 `jclass` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `fieldName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `signature`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QJniObject::isClassAvailable(const char *className)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `isClassAvailable`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `className`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJniObject::isValid() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isValid`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename T> T QJniObject::object() const`

**API 类别：** 成员函数说明

**中文解读：** `QJniObject::object` 用于计算、查询或取得与“object”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `template <typename T> T`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename T> T`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] jclass QJniObject::objectClass() const`

**API 类别：** 成员函数说明

**中文解读：** `QJniObject::objectClass` 用于计算、查询或取得与“object、Class”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `jclass`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`jclass`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Ret = void, typename Type> auto QJniObject::setField(const char *fieldName, Type value)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setField`。调用它会改变 `QJniObject` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`template <typename Ret = void, typename Type> auto`。
- 参数 `fieldName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `Type`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Ret = void, typename Type> auto QJniObject::setField(const char *fieldName, const char *signature, Type value)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setField`。调用它会改变 `QJniObject` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`template <typename Ret = void, typename Type> auto`。
- 参数 `fieldName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `signature`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `Type`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] template < typename Klass, typename Ret = void, typename Type > auto QJniObject::setStaticField(const char *fieldName, Type value)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `setStaticField`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template < typename Klass, typename Ret = void, typename Type > auto`。
- 参数 `fieldName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `Type`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] template <typename Ret = void, typename Type> auto QJniObject::setStaticField(const char *className, const char *fieldName, Type value)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `setStaticField`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename Ret = void, typename Type> auto`。
- 参数 `className`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `fieldName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `Type`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] template <typename Ret = void, typename Type> auto QJniObject::setStaticField(jclass clazz, const char *fieldName, Type value)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `setStaticField`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename Ret = void, typename Type> auto`。
- 参数 `clazz`：类型为 `jclass`。没有默认值，调用时必须提供。传入 `jclass` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `fieldName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `Type`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] template <typename Ret = void, typename Type> auto QJniObject::setStaticField(const char *className, const char *fieldName, const char *signature, Type value)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `setStaticField`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename Ret = void, typename Type> auto`。
- 参数 `className`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `fieldName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `signature`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `Type`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] template <typename Ret = void, typename Type> auto QJniObject::setStaticField(jclass clazz, const char *fieldName, const char *signature, Type value)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `setStaticField`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename Ret = void, typename Type> auto`。
- 参数 `clazz`：类型为 `jclass`。没有默认值，调用时必须提供。传入 `jclass` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `fieldName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `signature`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `Type`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.8] void QJniObject::swap(QJniObject &other)`

**API 类别：** 成员函数说明

**中文解读：** `QJniObject::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QJniObject &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QJniObject::toString() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toString`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename T, std::enable_if_t<std::is_convertible_v<T, jobject>, bool> = true> QJniObject &QJniObject::operator=(T object)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJniObject` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template <typename T, std::enable_if_t<std::is_convertible_v<T, jobject>, bool> = true> QJniObject &`。
- 参数 `object`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool operator!=(const QJniObject &o1, const QJniObject &o2)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QJniObject` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `o1`：类型为 `const QJniObject &`。没有默认值，调用时必须提供。传入 `const QJniObject &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `o2`：类型为 `const QJniObject &`。没有默认值，调用时必须提供。传入 `const QJniObject &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool operator==(const QJniObject &o1, const QJniObject &o2)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QJniObject` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `o1`：类型为 `const QJniObject &`。没有默认值，调用时必须提供。传入 `const QJniObject &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `o2`：类型为 `const QJniObject &`。没有默认值，调用时必须提供。传入 `const QJniObject &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

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

`QJniObject` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
