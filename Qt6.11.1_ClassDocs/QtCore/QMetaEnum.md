# QMetaEnum

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“MetaEnum”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QMetaEnum` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QMetaEnum>`
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

- `const char * enumName() const`
- `(since 6.9) bool is64Bit() const`
- `bool isFlag() const`
- `bool isScoped() const`
- `bool isValid() const`
- `const char * key(int index) const`
- `int keyCount() const`
- `(since 6.9) std::optional<quint64> keyToValue64(const char *key) const`
- `int keyToValue(const char *key, bool *ok = nullptr) const`
- `std::optional<quint64> keysToValue64(const char *keys) const`
- `int keysToValue(const char *keys, bool *ok = nullptr) const`
- `(since 6.6) QMetaType metaType() const`
- `const char * name() const`
- `const char * scope() const`
- `(since 6.9) std::optional<quint64> value64(int index) const`
- `int value(int index) const`
- `const char * valueToKey(quint64 value) const`
- `QByteArray valueToKeys(quint64 value) const`

### 静态公有成员

- `QMetaEnum fromType()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `const char *QMetaEnum::enumName() const`

**作用与语义：**

返回标志的枚举名称（不含作用域）。
例如，`Qt::AlignmentFlag` 标志的枚举名是 `AlignmentFlag`，但类型名是 `Alignment`。非标志枚举的枚举名称和枚举名相同。
枚举名称与类型名称具有相同的作用域。

### `[static] template <typename T> QMetaEnum QMetaEnum::fromType()`

**作用与语义：**

返回模板参数中对应类型的`QMetaEnum`。枚举需要声明为 `Q_ENUM`。

### `[since 6.9] bool QMetaEnum::is64Bit() const`

**作用与语义：**

如果该枚举的底层类型宽度为64位，返回`true`。

### `bool QMetaEnum::isFlag() const`

**作用与语义：**

如果将该枚举器用作标志，返回`true`;否则返回 false。
作为标志使用时，枚举器可以通过 OR 操作符组合。

### `bool QMetaEnum::isScoped() const`

**作用与语义：**

如果该枚举器被声明为 C 11 枚举类，返回 `true`;否则返回 false。

### `bool QMetaEnum::isValid() const`

**作用与语义：**

如果该枚举有效（有名称），返回`true`;否则返回 false。

### `const char *QMetaEnum::key(int index) const`

**作用与语义：**

返回带有给定`index`的密钥，若无该密钥则返回 `nullptr`。

### `int QMetaEnum::keyCount() const`

**作用与语义：**

返回密钥数量。

### `[since 6.9] std::optional<quint64> QMetaEnum::keyToValue64(const char *key) const`

**作用与语义：**

返回给定枚举的整数值，`key`，若未定义`key`则返回`std::nullopt`。
对于标志类型，使用`keysToValue64()`。
如果32位枚举的底层类型有符号（例如`int`、`short`），该函数总是将32位枚举的值进行符号扩展到64位。在大多数情况下，这是预期的行为。
一个显著的例外是标志值设置为第31位，如0x8000'0000，因为某些编译器（如Microsoft Visual Studio）不会自动切换到未签名的底层类型。为避免此问题，应在`enum`声明中明确指定底层类型。
注意：对于Qt 6.6之前编译的QMetaObjects，该函数始终是符号扩展的。

### `int QMetaEnum::keyToValue(const char *key, bool *ok = nullptr) const`

**作用与语义：**

返回给定枚举`key`的整数值，若未定义`key`则返回-1。
如果`key`未定义，则*`ok`设为假;否则*`ok`设为真。
对于标志类型，使用`keysToValue()`。
如果这是64位枚举（见`is64Bit()`），该函数返回最低32位部分。使用`keyToValue64()`来获得完整值。

### `std::optional<quint64> QMetaEnum::keysToValue64(const char *keys) const`

**作用与语义：**

返回通过OR算子将`keys`值组合得出的值，若未定义`keys`则返回`std::nullopt`。注意，`keys`中的字符串必须是'|'-分离的。
如果32位枚举的底层类型有符号（例如`int`、`short`），该函数总是将32位枚举的值符号扩展到64位。在大多数情况下，这是预期的行为。
一个显著的例外是标志值设置为第31位，如0x8000'0000，因为某些编译器（如Microsoft Visual Studio）不会自动切换到未签名的底层类型。为避免此问题，应在`enum`声明中明确指定底层类型。
注意：对于Qt 6.6之前编译的QMetaObjects，该函数始终是符号扩展的。

### `int QMetaEnum::keysToValue(const char *keys, bool *ok = nullptr) const`

**作用与语义：**

返回通过OR算子将`keys`值合并得出的值，若未定义`keys`则返回-1。注意，`keys`中的字符串必须是“|'-分离。
如果`keys`未定义，则 *`ok` 设为假;否则 *`ok` 设为真。
如果这是64位枚举（见`is64Bit()`），该函数返回低32位部分。使用`keyToValue64()`以获得完整值。

### `[since 6.6] QMetaType QMetaEnum::metaType() const`

**作用与语义：**

返回枚举的元类型。
如果该枚举所属的`QMetaObject`是在Qt 6.5或更早生成的，则该元类型将无效。
注意：这是枚举本身的元类型，而非其底层整数类型。您可以使用`QMetaType::underlyingType()`检索枚举底层类型的元类型。

### `const char *QMetaEnum::name() const`

**作用与语义：**

返回类型名称（不含作用域）。
例如，`Qt::Key`枚举中类型名为`Key` `Qt`，作用域为范畴。
对于标志，这返回的是标志类型的名称，而不是枚举类型的名称。

### `const char *QMetaEnum::scope() const`

**作用与语义：**

返回该枚举器所声明的范围。
例如，`Qt::AlignmentFlag`枚举的范围是`Qt`，名称是`AlignmentFlag`。

### `[since 6.9] std::optional<quint64> QMetaEnum::value64(int index) const`

**作用与语义：**

如果存在该`index`，返回该值;如果不存在，返回`std::nullopt`。
如果32位枚举的底层类型有符号（例如`int`、`short`），该函数总是将其值符号扩展到64位。在大多数情况下，这是预期的行为。
一个显著的例外是标志值设置为第31位，如0x8000'0000，因为某些编译器（如Microsoft Visual Studio）不会自动切换到未签名的底层类型。为避免此问题，应在`enum`声明中明确指定底层类型。
注意：对于Qt 6.6之前编译的QMetaObjects，该函数始终是符号扩展的。

### `int QMetaEnum::value(int index) const`

**作用与语义：**

返回带有给定`index`的值;如果没有该值，则返回-1。
如果这是一个带有64位底层类型的枚举（见`is64Bit()`），该函数返回值的最低32位部分。使用`value64()`以获得完整值。

### `const char *QMetaEnum::valueToKey(quint64 value) const`

**作用与语义：**

返回用作给定枚举名称的字符串，`value`，若未定义`value`则返回`nullptr`。
对于标志类型，使用`valueToKeys()`。

### `QByteArray QMetaEnum::valueToKeys(quint64 value) const`

**作用与语义：**

返回一个由 '|' 组成的字节数组-分离键，代表给定的`value`。
注意：将64位`value`传递给底层类型为32位的枚举（即`is64Bit()`返回`false`时），返回的字符串为空。

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

`QMetaEnum` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
