# QSignalSpy

> Qt 6.11.1 · Qt Test

## 1. 先建立直觉

**一句话定位：** 这是 Qt Test 中围绕“信号Spy”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Test 提供单元测试、数据驱动测试、基准测试和 GUI 测试支持。

### 这是什么

`QSignalSpy` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QSignalSpy>`
- 继承自：QList
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Test)
target_link_libraries(mytarget PRIVATE Qt6::Test)
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

- `QSignalSpy(const QObject *object, PointerToMemberFunction signal)`
- `QSignalSpy(const QObject *obj, QMetaMethod signal)`
- `QSignalSpy(const QObject *object, const char *signal)`
- `~QSignalSpy()`
- `bool isValid() const`
- `QByteArray signal() const`
- `bool wait(int timeout)`
- `(since 6.6) bool wait(std::chrono::milliseconds timeout = std::chrono::seconds{5})`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `template <typename PointerToMemberFunction> QSignalSpy::QSignalSpy(const QObject *object, PointerToMemberFunction signal)`

**作用与语义：**

构建一个新的QSignalSpy，监听`QObject` `object` `signal`的发射。如果QSignalSpy无法监听有效信号（例如，`object` `nullptr`或`signal`不表示有效信号`object`），将使用`qWarning()`输出解释性警告消息，后续调用`isValid()`将返回false。

**官方示例：**

```cpp
 QSignalSpy spy(myPushButton, &QPushButton::clicked);
```

### `QSignalSpy::QSignalSpy(const QObject *obj, QMetaMethod signal)`

**作用与语义：**

构建一个新的QSignalSpy，监听`QObject` `obj` `signal`的发射。如果QSignalSpy无法监听有效信号（例如，`obj` `nullptr`或`signal`不表示有效信号为`obj`），将输出一个解释性警告消息，使用`qWarning()`，后续调用`isValid()`将返回false。
当 Qt 的元对象系统在测试中被大量使用时，该构造器非常方便。
基本使用示例：
假设我们需要检查代表最小维和最大维度的`QWindow`类所有属性是否都正确可写。以下示例展示了其中一种方法：

**官方示例：**

```cpp
 QObject object;
 auto mo = object.metaObject();
 auto signalIndex = mo->indexOfSignal("objectNameChanged(QString)");
 auto signal = mo->method(signalIndex);

 QSignalSpy spy(&object, signal);
 object.setObjectName("A new object name");
 QCOMPARE(spy.count(), 1);
```

### `[explicit] QSignalSpy::QSignalSpy(const QObject *object, const char *signal)`

**作用与语义：**

构建一个新的QSignalSpy，监听`QObject` `object` `signal`的发射。如果QSignalSpy无法监听有效信号（例如，`object` `nullptr`或`signal`不表示有效信号`object`），将使用`qWarning()`输出解释性警告消息，后续调用`isValid()`将返回false。

**官方示例：**

```cpp
 QSignalSpy spy(myPushButton, SIGNAL(clicked(bool)));
```

### `[noexcept] QSignalSpy::~QSignalSpy()`

**作用与语义：**

毁灭者。

### `[noexcept] bool QSignalSpy::isValid() const`

**作用与语义：**

如果信号间谍听到有效信号，则返回`true`，否则返回假。

### `QByteArray QSignalSpy::signal() const`

**作用与语义：**

返回间谍当前正在收听的归一化信号。

### `bool QSignalSpy::wait(int timeout)`

**作用与语义：**

这是一个重载函数，等效地传递`timeout`时间超载：
如果信号在`timeout`中至少发射过一次，返回`true`，否则返回`false`。

**官方示例：**

```cpp
 wait(std::chrono::milliseconds{timeout});
```

### `[since 6.6] bool QSignalSpy::wait(std::chrono::milliseconds timeout = std::chrono::seconds{5})`

**作用与语义：**

启动一个事件循环，直到收到给定信号或`timeout`过去，以先发生者为准。
`timeout`有有效的标准：：:d uration（标准：：时间：：秒，标准：：时间：毫秒......等等）。
如果信号在 `timeout` 中至少发出一次，则返回`true`，否则返回 `false`。

**官方示例：**

```cpp
 using namespace std::chrono_literals;
 QSignalSpy spy(object, signal);
 spy.wait(2s);
```

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

`QSignalSpy` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
