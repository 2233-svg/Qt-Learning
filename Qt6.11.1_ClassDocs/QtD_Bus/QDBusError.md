# QDBusError

> Qt 6.11.1 · Qt D-Bus

## 1. 先建立直觉

**一句话定位：** 这是 Qt D-Bus 中围绕“DBus错误”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** 这是 Qt D-Bus 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QDBusError` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QDBusError>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS DBus)
target_link_libraries(mytarget PRIVATE Qt6::DBus)
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

- `enum ErrorType { NoError, Other, Failed, NoMemory, ServiceUnknown, …, InvalidInterface }`

### 公有函数

- `bool isValid() const`
- `QString message() const`
- `QString name() const`
- `void swap(QDBusError &other)`
- `QDBusError::ErrorType type() const`

### 静态公有成员

- `QString errorString(QDBusError::ErrorType error)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QDBusError::ErrorType`

**作用与语义：**

为了便于验证由D总线实现和总线守护进程本身产生的最常见的D-Bus错误，`QDBusError`可以与一组预定义的值进行比较：
- `QDBusError::NoError`：`0`;`QDBusError`无效（即调用成功）
- `QDBusError::Other`：`1`;`QDBusError` 包含一个并非众所周知的错误
- `QDBusError::Failed`：`2`;调用失败（`org.freedesktop.DBus.Error.Failed`）
- `QDBusError::NoMemory`：`3`;记忆消失（`org.freedesktop.DBus.Error.NoMemory`）
- `QDBusError::ServiceUnknown`：`4`;被叫服务未知（`org.freedesktop.DBus.Error.ServiceUnknown`）
- `QDBusError::NoReply`：`5`;被调用的方法未在指定的超时（`org.freedesktop.DBus.Error.NoReply`）内回复
- `QDBusError::BadAddress`：`6`;所给地址无效（`org.freedesktop.DBus.Error.BadAddress`）
- `QDBusError::NotSupported`：`7`;不支持调用/操作（`org.freedesktop.DBus.Error.NotSupported`）
- `QDBusError::LimitsExceeded`：`8`;分配给该进程/调用/连接的限制超过了预定义的值（`org.freedesktop.DBus.Error.LimitsExceeded`）
- `QDBusError::AccessDenied`：`9`;调用/操作尝试访问不允许访问的资源（`org.freedesktop.DBus.Error.AccessDenied`）
- `QDBusError::NoServer`：`10`;文档中没有说明这是什么用途（`org.freedesktop.DBus.Error.NoServer`）
- `QDBusError::Timeout`：`11`;文档未说明其用途或用途（`org.freedesktop.DBus.Error.Timeout`）
- `QDBusError::NoNetwork`：`12`;文档未说明用途（`org.freedesktop.DBus.Error.NoNetwork`）
- `QDBusError::AddressInUse`：`13`;`QDBusServer` 尝试绑定已在使用的地址（`org.freedesktop.DBus.Error.AddressInUse`）
- `QDBusError::Disconnected`：`14`;调用/进程/消息在`QDBusConnection`断开连接后发送（`org.freedesktop.DBus.Error.Disconnected`）
- `QDBusError::InvalidArgs`：`15`;传递给该调用/操作的参数无效（`org.freedesktop.DBus.Error.InvalidArgs`）
- `QDBusError::UnknownMethod`：`16`;调用的方法未在本对象/接口中找不到，且参数如下（`org.freedesktop.DBus.Error.UnknownMethod`）
- `QDBusError::TimedOut`：`17`;文档里没有说......（`org.freedesktop.DBus.Error.TimedOut`）
- `QDBusError::InvalidSignature`：`18`;类型签名无效或不兼容（`org.freedesktop.DBus.Error.InvalidSignature`）
- `QDBusError::UnknownInterface`：`19`;该对象（`org.freedesktop.DBus.Error.UnknownInterface`）中不已知接口
- `QDBusError::UnknownObject`：`20`;对象路径指向一个不存在的对象（`org.freedesktop.DBus.Error.UnknownObject`）
- `QDBusError::UnknownProperty`：`21`;该属性在此接口中不存在（`org.freedesktop.DBus.Error.UnknownProperty`）
- `QDBusError::PropertyReadOnly`：`22`;该属性集合失败，因为该属性是只读的（`org.freedesktop.DBus.Error.PropertyReadOnly`）
- `QDBusError::InternalError`：`23`;发生内部错误
- `QDBusError::InvalidObjectPath`：`25`;所提供的对象路径无效。
- `QDBusError::InvalidService`：`24`;所请求的服务无效。
- `QDBusError::InvalidMember`：`27`;该成员无效。
- `QDBusError::InvalidInterface`：`26`;接口无效。

### `[static] QString QDBusError::errorString(QDBusError::ErrorType error)`

**作用与语义：**

返回与错误条件`error`相关的错误名称。

### `bool QDBusError::isValid() const`

**作用与语义：**

如果这是一个有效的错误条件（即存在错误），返回`true`，否则返回。

### `QString QDBusError::message() const`

**作用与语义：**

返回被叫方与该错误关联的消息。错误消息是实现定义的，通常包含人类可读的错误代码，但这并不意味着它适合终端用户。

### `QString QDBusError::name() const`

**作用与语义：**

返回该错误的名称。错误名称类似于D-Bus接口名称，如`org.freedesktop.DBus.InvalidArgs`。

### `[noexcept] void QDBusError::swap(QDBusError &other)`

**作用与语义：**

将该错误与`other`交换。该操作非常快且从未失败。

### `QDBusError::ErrorType QDBusError::type() const`

**作用与语义：**

返回该错误的`ErrorType`。

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

`QDBusError` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
