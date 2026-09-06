# QTextDocumentWriter

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QTextDocumentWriter` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QTextDocumentWriter>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
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

- `QTextDocumentWriter()`
- `QTextDocumentWriter(QIODevice *device, const QByteArray &format)`
- `QTextDocumentWriter(const QString &fileName, const QByteArray &format = QByteArray())`
- `~QTextDocumentWriter()`
- `QIODevice * device() const`
- `QString fileName() const`
- `QByteArray format() const`
- `void setDevice(QIODevice *device)`
- `void setFileName(const QString &fileName)`
- `void setFormat(const QByteArray &format)`
- `bool write(const QTextDocument *document)`
- `bool write(const QTextDocumentFragment &fragment)`

### 静态公有成员

- `QList<QByteArray> supportedDocumentFormats()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QTextDocumentWriter::QTextDocumentWriter()`

**作用与语义：**

构建一个空的 QTextDocumentWriter 对象。在写入前，你必须调用 `setFormat()` 设置文档格式，然后 `setDevice()` 或 `setFileName()`。

### `QTextDocumentWriter::QTextDocumentWriter(QIODevice *device, const QByteArray &format)`

**作用与语义：**

构建一个QTextDocumentWriter对象，用`format`指定的文档格式写入给定`device`。

### `[explicit] QTextDocumentWriter::QTextDocumentWriter(const QString &fileName, const QByteArray &format = QByteArray())`

**作用与语义：**

构建一个QTextDocumentWriter对象，该对象将按照`format`指定的文档格式写入名为`fileName`的文件。如果没有提供`format`，QTextDocumentWriter将通过检查`fileName`的扩展来检测文档格式。

### `[noexcept] QTextDocumentWriter::~QTextDocumentWriter()`

**作用与语义：**

摧毁`QTextDocumentWriter`物体。

### `QIODevice *QTextDocumentWriter::device() const`

**作用与语义：**

返回当前分配的设备，或者如果没有分配设备则返回`nullptr`。

### `QString QTextDocumentWriter::fileName() const`

**作用与语义：**

如果当前分配的设备是`QFile`，或者`setFileName()`已被调用，该函数返回要写入的文件名称。在其他情况下，返回空字符串。

### `QByteArray QTextDocumentWriter::format() const`

**作用与语义：**

返回用于撰写文档的格式。

### `void QTextDocumentWriter::setDevice(QIODevice *device)`

**作用与语义：**

将写入者的设备设置为指定的`device`。如果设备已被设置，旧设备会被移除，但其他方面保持不变。
如果设备尚未打开，`QTextDocumentWriter`将尝试通过调用open()来以`WriteOnly`模式打开设备。
注意：这对某些设备不适用，如`QProcess`、`QTcpSocket`和`QUdpSocket`，因为需要某些配置才能打开设备。

### `void QTextDocumentWriter::setFileName(const QString &fileName)`

**作用与语义：**

设置要写入`fileName`的文件名称。内部，`QTextDocumentWriter`会创建一个`QFile`并以`WriteOnly`模式打开，并在写入文档时使用该文件。

### `void QTextDocumentWriter::setFormat(const QByteArray &format)`

**作用与语义：**

设置用于编写文档的格式，`format`指定。`format` 是一个不区分大小写的文本字符串。例如：
你可以致电`supportedDocumentFormats()`获取完整的格式`QTextDocumentWriter`支持列表。

**官方示例：**

```cpp
         QTextDocumentWriter writer;
         writer.setFormat("odf"); // same as writer.setFormat("ODF");
```

### `[static] QList<QByteArray> QTextDocumentWriter::supportedDocumentFormats()`

**作用与语义：**

返回`QTextDocumentWriter`支持的文档格式列表。
默认情况下，Qt 可以编写以下格式：
- `Format`：描述
- `plaintext`：纯文本
- `HTML`：超文本标记语言
- `markdown`：Markdown（CommonMark 或 GitHub 方言）
- `ODF`：OpenDocument 格式

### `bool QTextDocumentWriter::write(const QTextDocument *document)`

**作用与语义：**

将指定`document`写入指定设备或文件，成功时返回`true`;否则返回`false`。

### `bool QTextDocumentWriter::write(const QTextDocumentFragment &fragment)`

**作用与语义：**

将`fragment`指定的文档片段写入指定的设备或文件，成功时返回`true`;否则返回`false`。

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

`QTextDocumentWriter` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
