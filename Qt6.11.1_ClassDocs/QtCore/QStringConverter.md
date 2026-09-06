# QStringConverter

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“StringConverter”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QStringConverter` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QStringConverter>`
- 继承自：未在类页中列出
- 直接派生类：QStringDecoder、QStringEncoder

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

- `(since 6.11) struct FinalizeResultChar`
- `enum Encoding { Utf8, Utf16, Utf16BE, Utf16LE, Utf32, …, System }`
- `enum class FinalizeResultError { NoError, InvalidCharacters, NotEnoughSpace }`
- `enum class Flag { Default, ConvertInvalidToNull, WriteBom, ConvertInitialBom, Stateless }`
- `flags Flags`

### 公有函数

- `bool hasError() const`
- `bool isValid() const`
- `const char * name() const`
- `void resetState()`

### 静态公有成员

- `QStringList availableCodecs()`
- `std::optional<QStringConverter::Encoding> encodingForData(QByteArrayView data, char16_t expectedFirstCharacter = 0)`
- `std::optional<QStringConverter::Encoding> encodingForHtml(QByteArrayView data)`
- `std::optional<QStringConverter::Encoding> encodingForName(QAnyStringView name)`
- `const char * nameForEncoding(QStringConverter::Encoding e)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum class QStringConverter::Flagflags QStringConverter::Flags`

**作用与语义：**

- `QStringConverter::Flag::Default`：`0`;适用默认转换规则。
- `QStringConverter::Flag::ConvertInvalidToNull`：`0x2`;如果设置了该标志，每个无效输入字符作为空字符输出。如果未设置，若输出编码能表示该字符，则无效输入字符表示为`QChar::ReplacementCharacter`，否则表示为问号。
- `QStringConverter::Flag::WriteBom`：`0x4`;从`QString`转换为输出编码时，如果输出编码支持，请将`QChar::ByteOrderMark`写为第一个字符。UTF-8、UTF-16 和 UTF-32 编码均为此类。
- `QStringConverter::Flag::ConvertInitialBom`：`0x8`;从输入编码转换为`QString`时，`QStringDecoder`通常会跳过一个前`QChar::ByteOrderMark`。当该标志被设置时，字节顺序标记不会被跳过，而是转换为 utf-16，并插入在创建的 `QString` 开头。
- `QStringConverter::Flag::Stateless`：`0x1`;忽略不同函数调用之间可能的转换状态，用于编码或解码字符串。如果遇到不完整的数据序列，这也会导致`QStringConverter`报错。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `[static] QStringList QStringConverter::availableCodecs()`

**作用与语义：**

返回支持编解码器的名称列表。该函数返回的名称可以传递给`QStringEncoder`和`QStringDecoder`的构造器，以创建该编解码器的解码器或解码器。
该函数可用于获取标准编解码器之外的额外编解码器列表。支持额外编解码器需要在 Qt 编译时支持 ICU 库。
注意：编解码器的顺序是内部实现细节，不保证稳定。

### `[static noexcept] std::optional<QStringConverter::Encoding> QStringConverter::encodingForData(QByteArrayView data, char16_t expectedFirstCharacter = 0)`

**作用与语义：**

如果能确定`data`的内容，返回编码。`expectedFirstCharacter`可以作为额外提示传递，帮助确定编码。
如果编码不清晰，返回的可选选项为空。

### `[static] std::optional<QStringConverter::Encoding> QStringConverter::encodingForHtml(QByteArrayView data)`

**作用与语义：**

尝试通过查看 HTML 元标签中的字节序标记或字元集指定符来确定 HTML 的编码`data`。如果可选为空，表示该编码不被 `QStringConverter` 支持。如果检测不到编码，方法返回 Utf8。

### `[static noexcept] std::optional<QStringConverter::Encoding> QStringConverter::encodingForName(QAnyStringView name)`

**作用与语义：**

如果有相应的 `Encoding` 成员，`name`转换。
如果`name`不是编码枚举中列出的编解码器名称，则返回`std::nullopt`。尽管如此，当Qt与ICU一起构建时，`QStringConverter`构造器可能会接受这样的名称，前提是ICU提供了带有该名称的转换器。
注意：在 6.8 之前的 Qt 版本中，该函数只需一个 `const char *`，预计该功能将采用 UTF-8 编码。

### `[noexcept] bool QStringConverter::hasError() const`

**作用与语义：**

如果转换无法正确转换字符，则返回为true。例如，这可能因无效的UTF-8序列或因目标编码限制无法转换字符而触发。

### `[noexcept] bool QStringConverter::isValid() const`

**作用与语义：**

如果这是一个可用于编码或解码文本的字符串转换器，则返回为真。
默认构造字符串转换器或带有不支持名称的转换器不有效。

### `[noexcept] const char *QStringConverter::name() const`

**作用与语义：**

返回该`QStringConverter`可编码或解码的编码规范名称。如果转换器无效，返回 nullptr。返回名称为 UTF-8 编码。

### `[static noexcept] const char *QStringConverter::nameForEncoding(QStringConverter::Encoding e)`

**作用与语义：**

如果 `e` 是无效值，则返回编码 `e` 或 `nullptr` 的典范名称。
注意：在 6.10、6.9.1、6.8.4 或 6.5.9 之前的 Qt 版本中，使用无效参数调用该函数会导致行为未定义。自上述 Qt 版本以来，它返回的是 nullptr。

### `[noexcept] void QStringConverter::resetState()`

**作用与语义：**

重置转换器的内部状态，清除潜在的错误或部分转换。

### `(since 6.11) struct FinalizeResultChar`

**作用与语义：**

保存在QStringDecoder或QStringEncoder上调用finalize()的结果。
该类用于传递 finalize() 调用的结果或调用未成功的原因。

### `enum Encoding { Utf8, Utf16, Utf16BE, Utf16LE, Utf32, …, System }`

**作用与语义：**

- `QStringConverter::Utf8`：`0`;创建一个与 UTF-8 之间的转换器
- `QStringConverter::Utf16`：`1`;创建一个与UTF-16之间的转换器。解码时，字节顺序会自动被前置字节顺序标记检测。如果不存在字节顺序或编码时，则假设系统字节顺序。
- `QStringConverter::Utf16BE`：`3`;创建与大端UTF-16的转换器。
- `QStringConverter::Utf16LE`：`2`;创建一个小端UTF-16的转换器。
- `QStringConverter::Utf32`：`4`;创建一个UTF-32的转换器。解码时，字节顺序会自动通过前置字节顺序标记检测。如果不存在或编码时，系统字节顺序将被假定。
- `QStringConverter::Utf32BE`：`6`;创建大端UTF-32的转换器。
- `QStringConverter::Utf32LE`：`5`;创建一个小端UTF-32的转换器。
- `QStringConverter::Latin1`：`7`;创建一个转换器，或从ISO-8859-1（拉丁语1）转换。
- `QStringConverter::System`：`8`;创建一个转换器，转入或从操作系统本地的底层编码。对于基于 Unix 的系统，这总是假设为 UTF-8。在 Windows 上，这会与本地代码页进行转换和转换。

### `enum class FinalizeResultError { NoError, InvalidCharacters, NotEnoughSpace }`

**作用与语义：**

- `QStringConverter::FinalizeResultError::NoError`：`0`;无错误。
- `QStringConverter::FinalizeResultError::InvalidCharacters`：`1`;编码器成功完成了最终化，但在最终化过程中或更早一段时间遇到了无效字符。
- `QStringConverter::FinalizeResultError::NotEnoughSpace`：`2`;finalize() 未成功，你必须扩大缓冲区并再次调用 finalize()。

### `enum class Flag { Default, ConvertInvalidToNull, WriteBom, ConvertInitialBom, Stateless }`

**作用与语义：**

- `QStringConverter::Flag::Default`：`0`;适用默认转换规则。
- `QStringConverter::Flag::ConvertInvalidToNull`：`0x2`;如果设置了该标志，每个无效输入字符作为空字符输出。如果未设置，若输出编码能表示该字符，则无效输入字符表示为`QChar::ReplacementCharacter`，否则表示为问号。
- `QStringConverter::Flag::WriteBom`：`0x4`;从`QString`转换为输出编码时，如果输出编码支持，请将`QChar::ByteOrderMark`写为第一个字符。UTF-8、UTF-16 和 UTF-32 编码均为此类。
- `QStringConverter::Flag::ConvertInitialBom`：`0x8`;从输入编码转换为`QString`时，`QStringDecoder`通常会跳过一个前`QChar::ByteOrderMark`。当该标志被设置时，字节顺序标记不会被跳过，而是转换为 utf-16，并插入在创建的 `QString` 开头。
- `QStringConverter::Flag::Stateless`：`0x1`;忽略不同函数调用之间可能的转换状态，用于编码或解码字符串。如果遇到不完整的数据序列，这也会导致`QStringConverter`报错。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `flags Flags`

**作用与语义：**

- `QStringConverter::Flag::Default`：`0`;适用默认转换规则。
- `QStringConverter::Flag::ConvertInvalidToNull`：`0x2`;如果设置了该标志，每个无效输入字符作为空字符输出。如果未设置，若输出编码能表示该字符，则无效输入字符表示为`QChar::ReplacementCharacter`，否则表示为问号。
- `QStringConverter::Flag::WriteBom`：`0x4`;从`QString`转换为输出编码时，如果输出编码支持，请将`QChar::ByteOrderMark`写为第一个字符。UTF-8、UTF-16 和 UTF-32 编码均为此类。
- `QStringConverter::Flag::ConvertInitialBom`：`0x8`;从输入编码转换为`QString`时，`QStringDecoder`通常会跳过一个前`QChar::ByteOrderMark`。当该标志被设置时，字节顺序标记不会被跳过，而是转换为 utf-16，并插入在创建的 `QString` 开头。
- `QStringConverter::Flag::Stateless`：`0x1`;忽略不同函数调用之间可能的转换状态，用于编码或解码字符串。如果遇到不完整的数据序列，这也会导致`QStringConverter`报错。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

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

`QStringConverter` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
