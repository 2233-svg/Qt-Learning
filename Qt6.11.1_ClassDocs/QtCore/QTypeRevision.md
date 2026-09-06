# QTypeRevision

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“TypeRevision”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QTypeRevision` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QTypeRevision>`
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

- `QTypeRevision()`
- `bool hasMajorVersion() const`
- `bool hasMinorVersion() const`
- `bool isValid() const`
- `quint8 majorVersion() const`
- `quint8 minorVersion() const`
- `Integer toEncodedVersion() const`

### 静态公有成员

- `QTypeRevision fromEncodedVersion(Integer value)`
- `QTypeRevision fromMajorVersion(Major majorVersion)`
- `QTypeRevision fromMinorVersion(Minor minorVersion)`
- `QTypeRevision fromVersion(Major majorVersion, Minor minorVersion)`
- `bool isValidSegment(Integer segment)`
- `QTypeRevision zero()`

### 相关非成员函数

- `(since 6.0) QDataStream & operator<<(QDataStream &out, const QTypeRevision &revision)`
- `(since 6.0) QDataStream & operator>>(QDataStream &in, QTypeRevision &revision)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[constexpr noexcept] QTypeRevision::QTypeRevision()`

**作用与语义：**

产生无效的修订。

### `[static constexpr] template <typename Integer, QTypeRevision::if_valid_value_type<Integer> = true> QTypeRevision QTypeRevision::fromEncodedVersion(Integer value)`

**作用与语义：**

从给定的`value`生成一个`QTypeRevision`。`value` 分别以最低有效字节和第二低有效字节编码小版本和大字节。
`value`不能有位超出最低有效两个字节设置。`Integer`宽度至少为16位，且最低有效16位内不得有符号位。

### `[static constexpr] template <typename Major, QTypeRevision::if_valid_segment_type<Major> = true> QTypeRevision QTypeRevision::fromMajorVersion(Major majorVersion)`

**作用与语义：**

从给定`majorVersion`生成一个带有无效小版本的`QTypeRevision`。`majorVersion`需要是有效的段。

### `[static constexpr] template <typename Minor, QTypeRevision::if_valid_segment_type<Minor> = true> QTypeRevision QTypeRevision::fromMinorVersion(Minor minorVersion)`

**作用与语义：**

从给定`minorVersion`生成一个无效的主要版本的`QTypeRevision`。`minorVersion`段必须是有效的。

### `[static constexpr] template < typename Major, typename Minor, QTypeRevision::if_valid_segment_type<Major> = true, QTypeRevision::if_valid_segment_type<Minor> = true > QTypeRevision QTypeRevision::fromVersion(Major majorVersion, Minor minorVersion)`

**作用与语义：**

从给定的 `majorVersion` 和 `minorVersion` 产生`QTypeRevision`，这两者都需要是有效的段。

### `[constexpr] bool QTypeRevision::hasMajorVersion() const`

**作用与语义：**

如果已知主要版本，则返回真，否则返回为假。

### `[constexpr] bool QTypeRevision::hasMinorVersion() const`

**作用与语义：**

如果已知次要版本，则返回为真，否则为假。

### `[constexpr] bool QTypeRevision::isValid() const`

**作用与语义：**

如果已知主要版本或次要版本，则返回真，否则返回为假。

### `[static constexpr] template <typename Integer, QTypeRevision::if_valid_segment_type<Integer> = true> bool QTypeRevision::isValidSegment(Integer segment)`

**作用与语义：**

如果给定数字可以作为`QTypeRevision`中的大调或小调使用，则返回真值。`segment`的有效范围为`>= 0`和`< 255`。

### `[constexpr] quint8 QTypeRevision::majorVersion() const`

**作用与语义：**

返回版本中编码的主版本。

### `[constexpr] quint8 QTypeRevision::minorVersion() const`

**作用与语义：**

返回版本中编码的次要版本。

### `[constexpr] template <typename Integer, QTypeRevision::if_valid_value_type<Integer> = true> Integer QTypeRevision::toEncodedVersion() const`

**作用与语义：**

将修订值转换为整数值，将次要版本编码为最低有效字节，将主要版本编码为第二低有效字节。
`Integer`宽度至少为16位，且符号位不得处于最低有效16位。

### `[static constexpr] QTypeRevision QTypeRevision::zero()`

**作用与语义：**

产生带有大调和小调`0`的`QTypeRevision`。

### `[since 6.0] QDataStream &operator<<(QDataStream &out, const QTypeRevision &revision)`

**作用与语义：**

写修订版，播放`out` `revision`。

### `[since 6.0] QDataStream &operator>>(QDataStream &in, QTypeRevision &revision)`

**作用与语义：**

读取流`in`的修订并存储在`revision`。

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

`QTypeRevision` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
