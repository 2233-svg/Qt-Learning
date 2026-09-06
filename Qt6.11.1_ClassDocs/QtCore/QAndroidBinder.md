# QAndroidBinder

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“AndroidBinder”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QAndroidBinder` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QtCore/private/qandroidextras_p.h>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS CorePrivate)
target_link_libraries(mytarget PRIVATE Qt6::CorePrivate)
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

- `enum class CallType { Normal, OneWay }`

### 公有函数

- `QAndroidBinder()`
- `QAndroidBinder(const QJniObject &binder)`
- `QJniObject handle() const`
- `virtual bool onTransact(int code, const QAndroidParcel &data, const QAndroidParcel &reply, QAndroidBinder::CallType flags)`
- `bool transact(int code, const QAndroidParcel &data, QAndroidParcel *reply = nullptr, QAndroidBinder::CallType flags = CallType::Normal) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum class QAndroidBinder::CallType`

**作用与语义：**

该枚举与`QAndroidBinder::transact()`一起使用，描述IPC调用的执行模式。
- `QAndroidBinder::CallType::Normal`：`0`;正常IPC，意味着调用者等待被叫方的结果
- `QAndroidBinder::CallType::OneWay`：`1`;单向IPC，意味着来电者立即返回，无需等待被叫方的结果

### `[explicit] QAndroidBinder::QAndroidBinder()`

**作用与语义：**

创建一个新的对象，可用于执行IPC。

### `QAndroidBinder::QAndroidBinder(const QJniObject &binder)`

**作用与语义：**

从`binder` Java 对象创建一个新对象。

### `QJniObject QAndroidBinder::handle() const`

**作用与语义：**

返回值对于调用未被该封装器覆盖的其他 Java API 非常有用。

### `[virtual] bool QAndroidBinder::onTransact(int code, const QAndroidParcel &data, const QAndroidParcel &reply, QAndroidBinder::CallType flags)`

**作用与语义：**

默认实现是一个返回false的存根。用户应覆盖此方法以获取调用方的交易数据。
`code`是要执行的动作。`data`是调用者发送的集结数据。

`reply`是发送给来电者的集管数据。

`flags`是额外的操作标志。
警告：此方法调用自Binder的线程，该线程与该对象创建的线程不同。

### `bool QAndroidBinder::transact(int code, const QAndroidParcel &data, QAndroidParcel *reply = nullptr, QAndroidBinder::CallType flags = CallType::Normal) const`

**作用与语义：**

执行IPC调用。
`code`是要执行的动作。应该介于FIRST_CALL_TRANSACTION和LAST_CALL_TRANSACTION之间。

`data`是发送给目标的汇编数据。

`reply`（如果指定）是目标接收的编组数据。如果你不关心返回值，可能是nullptr。

`flags`是额外的操作标志。
成功时的回报为真。

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

`QAndroidBinder` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
