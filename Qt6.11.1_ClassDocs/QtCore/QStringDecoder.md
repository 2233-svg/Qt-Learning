# QStringDecoder

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“StringDecoder”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QStringDecoder` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QStringDecoder>`
- 继承自：QStringConverter
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

- `FinalizeResult`
- `FinalizeResultQChar`

### 公有函数

- `QStringDecoder()`
- `QStringDecoder(QAnyStringView name, QStringConverter::Flags flags = Flag::Default)`
- `QStringDecoder(QStringConverter::Encoding encoding, QStringConverter::Flags flags = Flag::Default)`
- `QChar * appendToBuffer(QChar *out, QByteArrayView in)`
- `(since 6.6) char16_t * appendToBuffer(char16_t *out, QByteArrayView in)`
- `QStringDecoder::EncodedData<QByteArrayView> decode(QByteArrayView ba)`
- `QStringDecoder::EncodedData<const QByteArray &> decode(const QByteArray &ba)`
- `(since 6.11) QStringDecoder::FinalizeResult finalize()`
- `(since 6.11) QStringDecoder::FinalizeResultQChar finalize(QChar *out, qsizetype maxlen)`
- `(since 6.11) QStringDecoder::FinalizeResult finalize(char16_t *out, qsizetype maxlen)`
- `qsizetype requiredSpace(qsizetype inputLength) const`
- `QStringDecoder::EncodedData<QByteArrayView> operator()(QByteArrayView ba)`
- `QStringDecoder::EncodedData<const QByteArray &> operator()(const QByteArray &ba)`

### 静态公有成员

- `QStringDecoder decoderForHtml(QByteArrayView data)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[alias] QStringDecoder::FinalizeResult`

**作用与语义：**

这是`QStringConverter::FinalizeResultChar`的化名<char16_t>。

### `[alias] QStringDecoder::FinalizeResultQChar`

**作用与语义：**

这是`QStringConverter::FinalizeResultChar`的化名<`QChar`>。

### `[constexpr noexcept] QStringDecoder::QStringDecoder()`

**作用与语义：**

默认构建解码器。默认解码器无效，不能用于转换文本。

### `[explicit] QStringDecoder::QStringDecoder(QAnyStringView name, QStringConverter::Flags flags = Flag::Default)`

**作用与语义：**

使用 `name` 和 `flags` 创建解码器对象。如果 的 不是已知编码的名称`name`，将生成一个无效的转换器。
注意：在6.8之前的Qt版本中，该功能只需一个`const char *`，预计该功能将采用UTF-8编码。

### `[explicit constexpr] QStringDecoder::QStringDecoder(QStringConverter::Encoding encoding, QStringConverter::Flags flags = Flag::Default)`

**作用与语义：**

利用`encoding`和 `flags` 创建解码器对象。

### `QChar *QStringDecoder::appendToBuffer(QChar *out, QByteArrayView in)`

**作用与语义：**

解码`in`看到的字节序列，并将解码结果写入从`out`开始的缓冲区。返回写入数据末尾的指针。
`out`需要足够大，能够容纳所有解码数据。利用`requiredSpace`确定解码`in.size()`字节编码数据缓冲区的最大大小要求。该函数可以写入介于`out`到`out + requiredSpace()`之间的任意字节，包括返回端点以外的字节。

### `[since 6.6] char16_t *QStringDecoder::appendToBuffer(char16_t *out, QByteArrayView in)`

**作用与语义：**

解码`in`看到的字节序列，并将解码结果写入从`out`开始的缓冲区。返回写入数据末尾的指针。
`out`需要足够大，能够容纳所有解码数据。利用`requiredSpace`确定解码`in.size()`字节编码数据缓冲区的最大大小要求。该函数可以写入介于`out`到`out + requiredSpace()`之间的任意字节，包括返回端点以外的字节。

### `[static] QStringDecoder QStringDecoder::decoderForHtml(QByteArrayView data)`

**作用与语义：**

尝试通过查看 HTML 元标签中的字节序标记或字元集指定符来确定 `data` HTML 的编码，并返回与编码匹配的`QStringDecoder`。如果返回的译码器无效，`QStringConverter`不支持该编码。如果检测不到编码，方法返回 Utf8 的译码器。

### `[since 6.11] QStringDecoder::FinalizeResult QStringDecoder::finalize()`

**作用与语义：**

向解码器发出信号，表示不会再有更多数据到达。
也可能提供待解码的残余内容数据。当没有剩余数据需要考虑时，返回的`error`字段将设置为`NoError`。
如果`out`被提供且非空，则必须有空间，最多可写入`maxlen`个字符。在该空间写入最多剩余输出字符，末尾由返回值的`next`字段表示。通常，这些残差数据应由每个未转换输入字符的替换字符组成。
如果所有残留内容都已通过`out`传递，`out` `nullptr`，或没有残留数据，解码器在返回时`finalize()`重置。否则，剩余数据可以通过进一步调用`finalize()`来检索或丢弃。

### `qsizetype QStringDecoder::requiredSpace(qsizetype inputLength) const`

**作用与语义：**

返回处理`inputLength`编码数据所需的最大UTF-16编码单元数量。

### `QStringDecoder::EncodedData<QByteArrayView> QStringDecoder::decode(QByteArrayView ba)`

**作用与语义：**

转换`ba`并返回一个可隐式转换为`QString`的结构体。

**官方示例：**

```cpp
 QByteArray encodedString = "...";
 auto toUtf16 = QStringDecoder(QStringDecoder::Utf8);
 auto data = toUtf16(encodedString); // data's type is QStringDecoder::EncodedData<const QByteArray &>
 QString string = toUtf16(encodedString); // Implicit conversion to QString

 // Here you have to cast "data" to QString
 auto func = [&]() { return !toUtf16.hasError() ? QString(data) : u"foo"_s; };
```

### `FinalizeResult`

**作用与语义：**

这是`QStringConverter::FinalizeResultChar`的化名<char16_t>。

### `FinalizeResultQChar`

**作用与语义：**

这是`QStringConverter::FinalizeResultChar`的化名<`QChar`>。

### `QStringDecoder::EncodedData<const QByteArray &> decode(const QByteArray &ba)`

**作用与语义：**

转换`ba`并返回一个可隐式转换为`QString`的结构体。

**官方示例：**

```cpp
 QByteArray encodedString = "...";
 auto toUtf16 = QStringDecoder(QStringDecoder::Utf8);
 auto data = toUtf16(encodedString); // data's type is QStringDecoder::EncodedData<const QByteArray &>
 QString string = toUtf16(encodedString); // Implicit conversion to QString

 // Here you have to cast "data" to QString
 auto func = [&]() { return !toUtf16.hasError() ? QString(data) : u"foo"_s; };
```

### `(since 6.11) QStringDecoder::FinalizeResultQChar finalize(QChar *out, qsizetype maxlen)`

**作用与语义：**

向解码器发出信号，表示不会再有更多数据到达。
也可能提供待解码的残余内容数据。当没有剩余数据需要考虑时，返回的`error`字段将设置为`NoError`。
如果`out`被提供且非空，则必须有空间，最多可写入`maxlen`个字符。在该空间写入最多剩余输出字符，末尾由返回值的`next`字段表示。通常，这些残差数据应由每个未转换输入字符的替换字符组成。
如果所有残留内容都已通过`out`传递，`out` `nullptr`，或没有残留数据，解码器在返回时`finalize()`重置。否则，剩余数据可以通过进一步调用`finalize()`来检索或丢弃。

### `(since 6.11) QStringDecoder::FinalizeResult finalize(char16_t *out, qsizetype maxlen)`

**作用与语义：**

向解码器发出信号，表示不会再有更多数据到达。
也可能提供待解码的残余内容数据。当没有剩余数据需要考虑时，返回的`error`字段将设置为`NoError`。
如果`out`被提供且非空，则必须有空间，最多可写入`maxlen`个字符。在该空间写入最多剩余输出字符，末尾由返回值的`next`字段表示。通常，这些残差数据应由每个未转换输入字符的替换字符组成。
如果所有残留内容都已通过`out`传递，`out` `nullptr`，或没有残留数据，解码器在返回时`finalize()`重置。否则，剩余数据可以通过进一步调用`finalize()`来检索或丢弃。

### `QStringDecoder::EncodedData<QByteArrayView> operator()(QByteArrayView ba)`

**作用与语义：**

转换`ba`并返回一个可隐式转换为`QString`的结构体。

**官方示例：**

```cpp
 QByteArray encodedString = "...";
 auto toUtf16 = QStringDecoder(QStringDecoder::Utf8);
 auto data = toUtf16(encodedString); // data's type is QStringDecoder::EncodedData<const QByteArray &>
 QString string = toUtf16(encodedString); // Implicit conversion to QString

 // Here you have to cast "data" to QString
 auto func = [&]() { return !toUtf16.hasError() ? QString(data) : u"foo"_s; };
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

`QStringDecoder` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
