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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QMessageAuthenticationCode::QMessageAuthenticationCode(QCryptographicHash::Algorithm method, QByteArrayView key = {})`

**作用与语义：**

构建一个对象，可用于利用方法`method`和密钥`key`从数据中创建密码学哈希。
注意：在 6.6 之前的 Qt 版本中，这个函数的参数是 `QByteArray`，而不是 `QByteArrayView`。如果你遇到编译错误，那是因为你的代码传递的对象是隐式可转换为 `QByteArray`，但不能`QByteArrayView`。将相应的参数包裹在 `QByteArray{~~~}` 中，使 cast 显式化。这与旧版 Qt 版本兼容。

### `[noexcept, since 6.6] QMessageAuthenticationCode::QMessageAuthenticationCode(QMessageAuthenticationCode &&other)`

**作用与语义：**

从`other`中构建一个新的QMessageAuthenticationCode。
注意：移出对象`other`处于部分成形状态，唯一有效的操作是销毁和新对象的赋值。

### `[noexcept] QMessageAuthenticationCode::~QMessageAuthenticationCode()`

**作用与语义：**

摧毁了该物体。

### `[noexcept] void QMessageAuthenticationCode::addData(QByteArrayView data)`

**作用与语义：**

这让信息更有深度`data`。
注意：在 6.6 之前的 Qt 版本中，这个函数的参数是 `QByteArray`，而不是 `QByteArrayView`。如果你遇到编译错误，那是因为你的代码传递的对象是隐式可转换为 `QByteArray`，但不能`QByteArrayView`。将相应的参数包裹在 `QByteArray{~~~}` 中，使 cast 显式化。这与旧的 Qt 版本是向后兼容的。

### `bool QMessageAuthenticationCode::addData(QIODevice *device)`

**作用与语义：**

读取打开`QIODevice` `device`的数据直到它结束并添加到消息中。如果读取成功，返回`true`。
注意：`device`必须已经开封。

### `void QMessageAuthenticationCode::addData(const char *data, qsizetype length)`

**作用与语义：**

给消息添加前`length`字`data`字。

### `[static] QByteArray QMessageAuthenticationCode::hash(QByteArrayView message, QByteArrayView key, QCryptographicHash::Algorithm method)`

**作用与语义：**

返回消息的认证码`message`使用密钥`key`和方法的`method`。
注意：在 6.6 之前的 Qt 版本中，这个函数的参数是 `QByteArray`，而不是 `QByteArrayView`。如果你遇到编译错误，那是因为你的代码传递的对象是隐式可转换为 `QByteArray`，但不能`QByteArrayView`。将对应参数包裹在 `QByteArray{~~~}` 中，使 cast 显式化。这与旧版 Qt 版本向后兼容。

### `[static noexcept, since 6.8] QByteArrayView QMessageAuthenticationCode::hashInto(QSpan<std::byte> buffer, QByteArrayView message, QByteArrayView key, QCryptographicHash::Algorithm method)`

**作用与语义：**

返回消息的认证码（`message`，或在`QSpan`重载时，`messageParts`的连接），使用密钥`key`和方法返回`method`。
返回值将是`buffer`的子张成，除非`buffer`大小不足，此时返回空`QByteArrayView`。

### `[noexcept] void QMessageAuthenticationCode::reset()`

**作用与语义：**

重置消息数据。调用这个函数不会影响密钥。

### `QByteArray QMessageAuthenticationCode::result() const`

**作用与语义：**

返回最终认证码。

### `[noexcept, since 6.6] QByteArrayView QMessageAuthenticationCode::resultView() const`

**作用与语义：**

返回最终哈希值。
注意，返回的视图只有在`QMessageAuthenticationCode`对象未被其他方式修改时才有效。

### `[noexcept] void QMessageAuthenticationCode::setKey(QByteArrayView key)`

**作用与语义：**

设置秘密`key`。调用该函数会自动重置对象状态。
为了最佳性能，只需调用该函数来更改激活键，而不是设置初始键，如。
倾向于将初始密钥作为构造函数参数传递：
你可以用std：：optional来延迟`QMessageAuthenticationCode`的建造，直到你知道密钥：
注意：在 6.6 之前的 Qt 版本中，这个函数的参数是 `QByteArray`，而不是 `QByteArrayView`。如果你遇到编译错误，那是因为你的代码传递的对象是隐式可转换为 `QByteArray`，但不能`QByteArrayView`。将对应的参数包裹在 `QByteArray{~~~}` 中，使 cast 显式化。这与旧版 Qt 版本兼容。

**官方示例：**

```cpp
 QMessageAuthenticationCode mac(method);
 mac.setKey(key); // does extra work
 use(mac);
```

### `[noexcept, since 6.6] void QMessageAuthenticationCode::swap(QMessageAuthenticationCode &other)`

**作用与语义：**

将该消息认证码与`other`交换。该操作非常快且从未失败。

### `[noexcept, since 6.6] QMessageAuthenticationCode &QMessageAuthenticationCode::operator=(QMessageAuthenticationCode &&other)`

**作用与语义：**

Move-assign `other`到该`QMessageAuthenticationCode`实例。
注意：移出对象`other`处于部分成形状态，唯一有效的操作是销毁和新对象的赋值。

### `(since 6.8) QByteArrayView hashInto(QSpan<char> buffer, QByteArrayView message, QByteArrayView key, QCryptographicHash::Algorithm method)`

**作用与语义：**

返回消息的认证码（`message`，或在`QSpan`重载时，`messageParts`的连接），使用密钥`key`和方法返回`method`。
返回值将是`buffer`的子张成，除非`buffer`大小不足，此时返回空`QByteArrayView`。

### `(since 6.8) QByteArrayView hashInto(QSpan<char> buffer, QSpan<const QByteArrayView> messageParts, QByteArrayView key, QCryptographicHash::Algorithm method)`

**作用与语义：**

返回消息的认证码（`message`，或在`QSpan`重载时，`messageParts`的连接），使用密钥`key`和方法返回`method`。
返回值将是`buffer`的子张成，除非`buffer`大小不足，此时返回空`QByteArrayView`。

### `(since 6.8) QByteArrayView hashInto(QSpan<std::byte> buffer, QSpan<const QByteArrayView> messageParts, QByteArrayView key, QCryptographicHash::Algorithm method)`

**作用与语义：**

返回消息的认证码（`message`，或在`QSpan`重载时，`messageParts`的连接），使用密钥`key`和方法返回`method`。
返回值将是`buffer`的子张成，除非`buffer`大小不足，此时返回空`QByteArrayView`。

### `(since 6.8) QByteArrayView hashInto(QSpan<uchar> buffer, QByteArrayView message, QByteArrayView key, QCryptographicHash::Algorithm method)`

**作用与语义：**

返回消息的认证码（`message`，或在`QSpan`重载时，`messageParts`的连接），使用密钥`key`和方法返回`method`。
返回值将是`buffer`的子张成，除非`buffer`大小不足，此时返回空`QByteArrayView`。

### `(since 6.8) QByteArrayView hashInto(QSpan<uchar> buffer, QSpan<const QByteArrayView> messageParts, QByteArrayView key, QCryptographicHash::Algorithm method)`

**作用与语义：**

返回消息的认证码（`message`，或在`QSpan`重载时，`messageParts`的连接），使用密钥`key`和方法返回`method`。
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

`QMessageAuthenticationCode` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
