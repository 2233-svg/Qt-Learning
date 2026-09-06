# QCryptographicHash

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“CryptographicHash”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QCryptographicHash` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QCryptographicHash>`
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

- `enum Algorithm { Md4, Md5, Sha1, Sha224, Sha256, …, Blake2s_256 }`

### 公有函数

- `QCryptographicHash(QCryptographicHash::Algorithm method)`
- `(since 6.5) QCryptographicHash(QCryptographicHash &&other)`
- `~QCryptographicHash()`
- `void addData(QByteArrayView bytes)`
- `bool addData(QIODevice *device)`
- `(since 6.5) QCryptographicHash::Algorithm algorithm() const`
- `void reset()`
- `QByteArray result() const`
- `(since 6.3) QByteArrayView resultView() const`
- `(since 6.5) void swap(QCryptographicHash &other)`
- `(since 6.5) QCryptographicHash & operator=(QCryptographicHash &&other)`

### 静态公有成员

- `QByteArray hash(QByteArrayView data, QCryptographicHash::Algorithm method)`
- `(since 6.8) QByteArrayView hashInto(QSpan<char> buffer, QByteArrayView data, QCryptographicHash::Algorithm method)`
- `(since 6.8) QByteArrayView hashInto(QSpan<char> buffer, QSpan<const QByteArrayView> data, QCryptographicHash::Algorithm method)`
- `(since 6.8) QByteArrayView hashInto(QSpan<std::byte> buffer, QByteArrayView data, QCryptographicHash::Algorithm method)`
- `(since 6.8) QByteArrayView hashInto(QSpan<std::byte> buffer, QSpan<const QByteArrayView> data, QCryptographicHash::Algorithm method)`
- `(since 6.8) QByteArrayView hashInto(QSpan<uchar> buffer, QByteArrayView data, QCryptographicHash::Algorithm method)`
- `(since 6.8) QByteArrayView hashInto(QSpan<uchar> buffer, QSpan<const QByteArrayView> data, QCryptographicHash::Algorithm method)`
- `int hashLength(QCryptographicHash::Algorithm method)`
- `(since 6.5) bool supportsAlgorithm(QCryptographicHash::Algorithm method)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QCryptographicHash::Algorithm`

**作用与语义：**

注意：在5.9之前的Qt版本中，当被要求生成SHA3哈希和时，`QCryptographicHash`实际上计算了Keccak。如果你需要与这些Qt版本产生的SHA-3哈希兼容，可以使用`Keccak_`枚举器。或者，如果需要源兼容性，可以定义宏`QT_SHA3_KECCAK_COMPAT`。
- `QCryptographicHash::Md4`：`0`;生成MD4哈希和
- `QCryptographicHash::Md5`：`1`;生成MD5哈希和
- `QCryptographicHash::Sha1`：`2`;生成SHA-1哈希和
- `QCryptographicHash::Sha224`：`3`;生成SHA-224哈希和（SHA-2）。引入于Qt 5.0
- `QCryptographicHash::Sha256`：`4`;生成SHA-256哈希和（SHA-2）。引入于Qt 5.0
- `QCryptographicHash::Sha384`：`5`;生成SHA-384哈希和（SHA-2）。Qt 5.0引入
- `QCryptographicHash::Sha512`：`6`;生成SHA-512哈希和（SHA-2）。引入于Qt 5.0
- `QCryptographicHash::Sha3_224`：`RealSha3_224`;生成SHA3-224哈希和。引入于Qt 5.1
- `QCryptographicHash::Sha3_256`：`RealSha3_256`;生成SHA3-256哈希和。引入于Qt 5.1
- `QCryptographicHash::Sha3_384`：`RealSha3_384`;生成SHA3-384哈希和。引入于Qt 5.1
- `QCryptographicHash::Sha3_512`：`RealSha3_512`;生成SHA3-512哈希和。引入于Qt 5.1
- `QCryptographicHash::Keccak_224`：`7`;生成 Keccak-224 哈希和。引入于 Qt 5.9.2
- `QCryptographicHash::Keccak_256`：`8`;生成一个 Keccak-256 哈希和。引入于 Qt 5.9.2
- `QCryptographicHash::Keccak_384`：`9`;生成 Keccak-384 哈希和。引入于 Qt 5.9.2
- `QCryptographicHash::Keccak_512`：`10`;生成 Keccak-512 哈希和。Qt 5.9.2 引入
- `QCryptographicHash::Blake2b_160`：`15`;生成BLAKE2b-160哈希和。在Qt 6.0中引入
- `QCryptographicHash::Blake2b_256`：`16`;生成BLAKE2b-256哈希和。Qt 6.0引入
- `QCryptographicHash::Blake2b_384`：`17`;生成BLAKE2b-384哈希和。Qt 6.0引入
- `QCryptographicHash::Blake2b_512`：`18`;生成BLAKE2b-512哈希和。Qt 6.0引入
- `QCryptographicHash::Blake2s_128`：`19`;生成一个BLAKE2s-128哈希和。在Qt 6.0中引入
- `QCryptographicHash::Blake2s_160`：`20`;生成BLAKE2s-160哈希和。引入于Qt 6.0
- `QCryptographicHash::Blake2s_224`：`21`;生成一个BLAKE2s-224哈希和。在Qt 6.0中引入
- `QCryptographicHash::Blake2s_256`：`22`;生成BLAKE2s-256哈希和。引入于Qt 6.0

### `[explicit] QCryptographicHash::QCryptographicHash(QCryptographicHash::Algorithm method)`

**作用与语义：**

构建一个对象，可用于利用`method`从数据中创建密码学哈希。

### `[noexcept, since 6.5] QCryptographicHash::QCryptographicHash(QCryptographicHash &&other)`

**作用与语义：**

从`other`中移动构造一个新的QCryptographicHash。
注意：移出对象`other`处于部分成形状态，唯一有效的操作是销毁和赋予新值。

### `[noexcept] QCryptographicHash::~QCryptographicHash()`

**作用与语义：**

摧毁了该物体。

### `[noexcept] void QCryptographicHash::addData(QByteArrayView bytes)`

**作用与语义：**

将`bytes`中的字符添加到密码学哈希中。
注意：在6.3之前的Qt版本中，该函数采用`QByteArray`，而非取`QByteArrayView`。

### `bool QCryptographicHash::addData(QIODevice *device)`

**作用与语义：**

读取打开`QIODevice` `device`的数据直到结束并进行哈希。如果读取成功，返回`true`。

### `[noexcept, since 6.5] QCryptographicHash::Algorithm QCryptographicHash::algorithm() const`

**作用与语义：**

返回用于生成密码学哈希的算法。

### `[static] QByteArray QCryptographicHash::hash(QByteArrayView data, QCryptographicHash::Algorithm method)`

**作用与语义：**

返回`data`的哈希值，使用`method`。
注意：在6.3之前的Qt版本中，该功能采用了`QByteArray`，而非被`QByteArrayView`。

### `[static noexcept, since 6.8] QByteArrayView QCryptographicHash::hashInto(QSpan<std::byte> buffer, QByteArrayView data, QCryptographicHash::Algorithm method)`

**作用与语义：**

返回`data`的哈希值，使用`method`，`buffer`存储结果。
如果 `data` 是张成，则按给定顺序将所有字节数组视图添加到哈希中。
返回值将是`buffer`的子张成，除非`buffer`大小不足，此时返回空`QByteArrayView`。

### `[static] int QCryptographicHash::hashLength(QCryptographicHash::Algorithm method)`

**作用与语义：**

返回所选哈希`method`输出的大小（字节单位）。

### `[noexcept] void QCryptographicHash::reset()`

**作用与语义：**

重置对象。

### `QByteArray QCryptographicHash::result() const`

**作用与语义：**

返回最终哈希值。

### `[noexcept, since 6.3] QByteArrayView QCryptographicHash::resultView() const`

**作用与语义：**

返回最终哈希值。
注意，返回的视图只有在`QCryptographicHash`对象未被其他方式修改时才有效。

### `[static, since 6.5] bool QCryptographicHash::supportsAlgorithm(QCryptographicHash::Algorithm method)`

**作用与语义：**

返回所选算法`method`是否支持，以及`result()`在使用该`method`时是否返回一个值。
注意：OpenSSL作为提供者时将负责提供这些信息，否则`true`将返回，因为非OpenSSL实现没有任何限制。如果我们未能查询OpenSSL，我们会返回`false`。

### `[noexcept, since 6.5] void QCryptographicHash::swap(QCryptographicHash &other)`

**作用与语义：**

将该密码学哈希与`other`交换。该操作非常快且从未失败。

### `[noexcept, since 6.5] QCryptographicHash &QCryptographicHash::operator=(QCryptographicHash &&other)`

**作用与语义：**

Move-assign `other` 到这个`QCryptographicHash`实例。
注意：移出对象 `other` 处于部分成形状态，唯一有效的操作是销毁和赋予新值。

### `(since 6.8) QByteArrayView hashInto(QSpan<char> buffer, QByteArrayView data, QCryptographicHash::Algorithm method)`

**作用与语义：**

返回`data`的哈希值，使用`method`，`buffer`存储结果。
如果 `data` 是张成，则按给定顺序将所有字节数组视图添加到哈希中。
返回值将是`buffer`的子张成，除非`buffer`大小不足，此时返回空`QByteArrayView`。

### `(since 6.8) QByteArrayView hashInto(QSpan<char> buffer, QSpan<const QByteArrayView> data, QCryptographicHash::Algorithm method)`

**作用与语义：**

返回`data`的哈希值，使用`method`，`buffer`存储结果。
如果 `data` 是张成，则按给定顺序将所有字节数组视图添加到哈希中。
返回值将是`buffer`的子张成，除非`buffer`大小不足，此时返回空`QByteArrayView`。

### `(since 6.8) QByteArrayView hashInto(QSpan<std::byte> buffer, QSpan<const QByteArrayView> data, QCryptographicHash::Algorithm method)`

**作用与语义：**

返回`data`的哈希值，使用`method`，`buffer`存储结果。
如果 `data` 是张成，则按给定顺序将所有字节数组视图添加到哈希中。
返回值将是`buffer`的子张成，除非`buffer`大小不足，此时返回空`QByteArrayView`。

### `(since 6.8) QByteArrayView hashInto(QSpan<uchar> buffer, QByteArrayView data, QCryptographicHash::Algorithm method)`

**作用与语义：**

返回`data`的哈希值，使用`method`，`buffer`存储结果。
如果 `data` 是张成，则按给定顺序将所有字节数组视图添加到哈希中。
返回值将是`buffer`的子张成，除非`buffer`大小不足，此时返回空`QByteArrayView`。

### `(since 6.8) QByteArrayView hashInto(QSpan<uchar> buffer, QSpan<const QByteArrayView> data, QCryptographicHash::Algorithm method)`

**作用与语义：**

返回`data`的哈希值，使用`method`，`buffer`存储结果。
如果 `data` 是张成，则按给定顺序将所有字节数组视图添加到哈希中。
返回值将是`buffer`的子张成，除非`buffer`大小不足，此时返回空`QByteArrayView`。

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

`QCryptographicHash` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
