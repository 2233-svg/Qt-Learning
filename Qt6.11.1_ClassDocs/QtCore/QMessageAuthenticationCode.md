# QMessageAuthenticationCode

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“MessageAuthenticationCode”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QMessageAuthenticationCode` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QMessageAuthenticationCode>`
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

- `QMessageAuthenticationCode(QCryptographicHash::Algorithm method, QByteArrayView key = {})`
- `(since 6.6) QMessageAuthenticationCode(QMessageAuthenticationCode &&other)`
- `~QMessageAuthenticationCode()`
- `void addData(QByteArrayView data)`
- `bool addData(QIODevice *device)`
- `void addData(const char *data, qsizetype length)`
- `void reset()`
- `QByteArray result() const`
- `(since 6.6) QByteArrayView resultView() const`
- `void setKey(QByteArrayView key)`
- `(since 6.6) void swap(QMessageAuthenticationCode &other)`
- `(since 6.6) QMessageAuthenticationCode & operator=(QMessageAuthenticationCode &&other)`

### 静态公有成员

- `QByteArray hash(QByteArrayView message, QByteArrayView key, QCryptographicHash::Algorithm method)`
- `(since 6.8) QByteArrayView hashInto(QSpan<char> buffer, QByteArrayView message, QByteArrayView key, QCryptographicHash::Algorithm method)`
- `(since 6.8) QByteArrayView hashInto(QSpan<char> buffer, QSpan<const QByteArrayView> messageParts, QByteArrayView key, QCryptographicHash::Algorithm method)`
- `(since 6.8) QByteArrayView hashInto(QSpan<std::byte> buffer, QByteArrayView message, QByteArrayView key, QCryptographicHash::Algorithm method)`
- `(since 6.8) QByteArrayView hashInto(QSpan<std::byte> buffer, QSpan<const QByteArrayView> messageParts, QByteArrayView key, QCryptographicHash::Algorithm method)`
- `(since 6.8) QByteArrayView hashInto(QSpan<uchar> buffer, QByteArrayView message, QByteArrayView key, QCryptographicHash::Algorithm method)`
- `(since 6.8) QByteArrayView hashInto(QSpan<uchar> buffer, QSpan<const QByteArrayView> messageParts, QByteArrayView key, QCryptographicHash::Algorithm method)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 19 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[explicit] QMessageAuthenticationCode::QMessageAuthenticationCode(QCryptographicHash::Algorithm method, QByteArrayView key = {})`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMessageAuthenticationCode` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `method`：类型为 `QCryptographicHash::Algorithm`。没有默认值，调用时必须提供。传入 `QCryptographicHash::Algorithm` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `key`：类型为 `QByteArrayView`。默认值为 `{}`。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.6] QMessageAuthenticationCode::QMessageAuthenticationCode(QMessageAuthenticationCode &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMessageAuthenticationCode` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `QMessageAuthenticationCode &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QMessageAuthenticationCode::~QMessageAuthenticationCode()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMessageAuthenticationCode` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QMessageAuthenticationCode::addData(QByteArrayView data)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QMessageAuthenticationCode` 添加依赖、数据或子对象的 API `addData`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `data`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMessageAuthenticationCode::addData(QIODevice *device)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QMessageAuthenticationCode` 添加依赖、数据或子对象的 API `addData`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `device`：类型为 `QIODevice *`。没有默认值，调用时必须提供。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMessageAuthenticationCode::addData(const char *data, qsizetype length)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QMessageAuthenticationCode` 添加依赖、数据或子对象的 API `addData`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `data`：类型为 `const char *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `length`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QByteArray QMessageAuthenticationCode::hash(QByteArrayView message, QByteArrayView key, QCryptographicHash::Algorithm method)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `hash`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `message`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `key`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `method`：类型为 `QCryptographicHash::Algorithm`。没有默认值，调用时必须提供。传入 `QCryptographicHash::Algorithm` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static noexcept, since 6.8] QByteArrayView QMessageAuthenticationCode::hashInto(QSpan<std::byte> buffer, QByteArrayView message, QByteArrayView key, QCryptographicHash::Algorithm method)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `hashInto`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QByteArrayView`。
- 参数 `buffer`：类型为 `QSpan<std::byte>`。没有默认值，调用时必须提供。传入 `QSpan<std::byte>` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `message`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `key`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `method`：类型为 `QCryptographicHash::Algorithm`。没有默认值，调用时必须提供。传入 `QCryptographicHash::Algorithm` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QMessageAuthenticationCode::reset()`

**API 类别：** 成员函数说明

**中文解读：** 这是状态清理或重置 API `reset`。调用后原有数据、索引、缓存或绑定可能失效；使用前先确认它影响的是当前对象、子对象还是底层共享资源，之后重新检查状态。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QMessageAuthenticationCode::result() const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageAuthenticationCode::result` 用于计算、查询或取得与“结果”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.6] QByteArrayView QMessageAuthenticationCode::resultView() const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageAuthenticationCode::resultView` 用于计算、查询或取得与“结果、View”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArrayView`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArrayView`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QMessageAuthenticationCode::setKey(QByteArrayView key)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setKey`。调用它会改变 `QMessageAuthenticationCode` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `key`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.6] void QMessageAuthenticationCode::swap(QMessageAuthenticationCode &other)`

**API 类别：** 成员函数说明

**中文解读：** `QMessageAuthenticationCode::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QMessageAuthenticationCode &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.6] QMessageAuthenticationCode &QMessageAuthenticationCode::operator=(QMessageAuthenticationCode &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMessageAuthenticationCode` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMessageAuthenticationCode &`。
- 参数 `other`：类型为 `QMessageAuthenticationCode &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.8) QByteArrayView hashInto(QSpan<char> buffer, QByteArrayView message, QByteArrayView key, QCryptographicHash::Algorithm method)`

**API 类别：** 静态公有成员

**中文解读：** 这是静态工具 API `hashInto`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QByteArrayView`。
- 参数 `buffer`：类型为 `QSpan<char>`。没有默认值，调用时必须提供。传入 `QSpan<char>` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `message`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `key`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `method`：类型为 `QCryptographicHash::Algorithm`。没有默认值，调用时必须提供。传入 `QCryptographicHash::Algorithm` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.8) QByteArrayView hashInto(QSpan<char> buffer, QSpan<const QByteArrayView> messageParts, QByteArrayView key, QCryptographicHash::Algorithm method)`

**API 类别：** 静态公有成员

**中文解读：** 这是静态工具 API `hashInto`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QByteArrayView`。
- 参数 `buffer`：类型为 `QSpan<char>`。没有默认值，调用时必须提供。传入 `QSpan<char>` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `messageParts`：类型为 `QSpan<const QByteArrayView>`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `key`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `method`：类型为 `QCryptographicHash::Algorithm`。没有默认值，调用时必须提供。传入 `QCryptographicHash::Algorithm` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.8) QByteArrayView hashInto(QSpan<std::byte> buffer, QSpan<const QByteArrayView> messageParts, QByteArrayView key, QCryptographicHash::Algorithm method)`

**API 类别：** 静态公有成员

**中文解读：** 这是静态工具 API `hashInto`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QByteArrayView`。
- 参数 `buffer`：类型为 `QSpan<std::byte>`。没有默认值，调用时必须提供。传入 `QSpan<std::byte>` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `messageParts`：类型为 `QSpan<const QByteArrayView>`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `key`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `method`：类型为 `QCryptographicHash::Algorithm`。没有默认值，调用时必须提供。传入 `QCryptographicHash::Algorithm` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.8) QByteArrayView hashInto(QSpan<uchar> buffer, QByteArrayView message, QByteArrayView key, QCryptographicHash::Algorithm method)`

**API 类别：** 静态公有成员

**中文解读：** 这是静态工具 API `hashInto`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QByteArrayView`。
- 参数 `buffer`：类型为 `QSpan<uchar>`。没有默认值，调用时必须提供。传入 `QSpan<uchar>` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `message`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `key`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `method`：类型为 `QCryptographicHash::Algorithm`。没有默认值，调用时必须提供。传入 `QCryptographicHash::Algorithm` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.8) QByteArrayView hashInto(QSpan<uchar> buffer, QSpan<const QByteArrayView> messageParts, QByteArrayView key, QCryptographicHash::Algorithm method)`

**API 类别：** 静态公有成员

**中文解读：** 这是静态工具 API `hashInto`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QByteArrayView`。
- 参数 `buffer`：类型为 `QSpan<uchar>`。没有默认值，调用时必须提供。传入 `QSpan<uchar>` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `messageParts`：类型为 `QSpan<const QByteArrayView>`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `key`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `method`：类型为 `QCryptographicHash::Algorithm`。没有默认值，调用时必须提供。传入 `QCryptographicHash::Algorithm` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

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

`QMessageAuthenticationCode` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
