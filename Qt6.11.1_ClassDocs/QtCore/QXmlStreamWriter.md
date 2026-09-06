# QXmlStreamWriter

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** XML 流式写入器，按开始元素、属性、文本和结束元素顺序生成 XML。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QXmlStreamWriter`：XML 流式写入器，按开始元素、属性、文本和结束元素顺序生成 XML。

**内部模型：** JSON 通常表示为 value/object/array 树，XML 则包含元素、属性、文本和层级。文档容器负责解析和序列化，具体字段/节点访问由 object、array、value 或 DOM/流式读取对象完成。

**适用场景：** 接收字节数据后显式指定编码和解析选项，检查错误对象，再按类型访问节点，校验业务字段，最后序列化或转换成领域对象。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要只检查 parse 成功；不要假设字段一定存在且类型固定；不要把用户输入直接当作可信结构；大文件不要无条件 readAll 和构造整棵树。

## 2. 依赖与对象关系

- 头文件：`#include <QXmlStreamWriter>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

JSON 通常表示为 value/object/array 树，XML 则包含元素、属性、文本和层级。文档容器负责解析和序列化，具体字段/节点访问由 object、array、value 或 DOM/流式读取对象完成。

### 状态、生命周期和线程

**生命周期：** 解析结果通常是值对象，可在作用域内传递；流式解析器则依赖输入设备和读取顺序。解析错误、结构合法和业务字段合法是三个不同层次，必须分别检查。

**状态与结果：** 先判断文档是否为空、根节点类型和解析错误，再访问字段；字段缺失、类型不匹配、空值和默认值要分开处理。序列化时要明确紧凑/格式化输出和编码。

**线程与事件循环：** 值形式的解析结果可以复制后跨线程处理；共享设备、流对象和可变 DOM 不应无保护地跨线程使用。大文档要评估一次性树结构的内存成本，必要时用流式 API。

## 3. 直接使用

接收字节数据后显式指定编码和解析选项，检查错误对象，再按类型访问节点，校验业务字段，最后序列化或转换成领域对象。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `(since 6.10) enum class Error { None, IO, Encoding, InvalidCharacter, Custom }`

### 属性

- `autoFormatting : bool`
- `autoFormattingIndent : int`
- `(since 6.10) stopWritingOnError : bool`

### 公有函数

- `QXmlStreamWriter()`
- `QXmlStreamWriter(QByteArray *array)`
- `QXmlStreamWriter(QIODevice *device)`
- `QXmlStreamWriter(QString *string)`
- `~QXmlStreamWriter()`
- `bool autoFormatting() const`
- `int autoFormattingIndent() const`
- `QIODevice * device() const`
- `(since 6.10) QXmlStreamWriter::Error error() const`
- `(since 6.10) QString errorString() const`
- `bool hasError() const`
- `(since 6.10) void raiseError(QAnyStringView message)`
- `void setAutoFormatting(bool enable)`
- `void setAutoFormattingIndent(int spacesOrTabs)`
- `void setDevice(QIODevice *device)`
- `void setStopWritingOnError(bool stop)`
- `bool stopWritingOnError() const`
- `void writeAttribute(QAnyStringView namespaceUri, QAnyStringView name, QAnyStringView value)`
- `void writeAttribute(const QXmlStreamAttribute &attribute)`
- `void writeAttribute(QAnyStringView qualifiedName, QAnyStringView value)`
- `void writeAttributes(const QXmlStreamAttributes &attributes)`
- `void writeCDATA(QAnyStringView text)`
- `void writeCharacters(QAnyStringView text)`
- `void writeComment(QAnyStringView text)`
- `void writeCurrentToken(const QXmlStreamReader &reader)`
- `void writeDTD(QAnyStringView dtd)`
- `void writeDefaultNamespace(QAnyStringView namespaceUri)`
- `void writeEmptyElement(QAnyStringView namespaceUri, QAnyStringView name)`
- `void writeEmptyElement(QAnyStringView qualifiedName)`
- `void writeEndDocument()`
- `void writeEndElement()`
- `void writeEntityReference(QAnyStringView name)`
- `void writeNamespace(QAnyStringView namespaceUri, QAnyStringView prefix = {})`
- `void writeProcessingInstruction(QAnyStringView target, QAnyStringView data = {})`
- `void writeStartDocument(QAnyStringView version)`
- `void writeStartDocument(QAnyStringView version, bool standalone)`
- `void writeStartDocument()`
- `void writeStartElement(QAnyStringView namespaceUri, QAnyStringView name)`
- `void writeStartElement(QAnyStringView qualifiedName)`
- `void writeTextElement(QAnyStringView namespaceUri, QAnyStringView name, QAnyStringView text)`
- `void writeTextElement(QAnyStringView qualifiedName, QAnyStringView text)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[since 6.10] enum class QXmlStreamWriter::Error`

**作用与语义：**

该枚举规定了在编写带有`QXmlStreamWriter`的XML时可能出现的不同错误情况。
- `QXmlStreamWriter::Error::None`：`0`;未发生错误。
- `QXmlStreamWriter::Error::IO`：`1`;写入设备时发生I/O错误。
- `QXmlStreamWriter::Error::Encoding`：`2`;在将字符转换为输出格式时发生编码错误。
- `QXmlStreamWriter::Error::InvalidCharacter`：`3`;在写入过程中遇到了XML 1.0中不允许的字符。
- `QXmlStreamWriter::Error::Custom`：`4`;`raiseError()` 时出现了自定义错误。
这个枚举是在Qt 6.10引入的。

### `autoFormatting : bool`

**作用与语义：**

该属性包含流写器的自动格式化标志。
该属性控制流写入器是否自动格式化生成的XML数据。启用后，写入者会自动在元素间的空部分添加换行和缩进（可忽略的空白）。自动格式化的主要目的是将数据拆分为多行，并提高人类阅读者的可读性。缩进深度可以通过`autoFormattingIndent`属性控制。
默认情况下，自动格式化是被禁用的。

**如何使用：** 调用 `autoFormatting()` 读取当前值；它不会修改应用状态。

### `autoFormattingIndent : int`

**作用与语义：**

该属性表示启用自动格式时用于缩进的空格或制表符数。正数表示空格，负数表示制表表。
默认缩进是4。

**如何使用：** 调用 `autoFormattingIndent()` 读取当前值；它不会修改应用状态。

### `[since 6.10] stopWritingOnError : bool`

**作用与语义：**

该特性允许在遇到错误后停止写入设备。
如果该属性设置为`true`，写入者在遇到任何错误时立即停止写入，并忽略所有后续写入操作。当该属性设为`false`时，写入者可以在错误后继续写入，跳过无效写入但允许继续输出。
注意这包括`Error::InvalidCharacter`、`Error::Encoding`和`Error::Custom`。无论设置如何，`Error::IO`始终被视为终端，停止写入。
默认值是`false`。

**如何使用：** 调用 `stopWritingOnError()` 读取当前值；它不会修改应用状态。

### `QXmlStreamWriter::QXmlStreamWriter()`

**作用与语义：**

构建一个流媒体写手。

### `[explicit] QXmlStreamWriter::QXmlStreamWriter(QByteArray *array)`

**作用与语义：**

构建一个流写入`array`。这与创建一个运行在`QBuffer`设备上的XML写入器是相同的，而该设备又运行于`array`。

### `[explicit] QXmlStreamWriter::QXmlStreamWriter(QIODevice *device)`

**作用与语义：**

构建一个流写入器，写入`device`;

### `[explicit] QXmlStreamWriter::QXmlStreamWriter(QString *string)`

**作用与语义：**

构建一个流写入器，写入`string`。

### `[noexcept] QXmlStreamWriter::~QXmlStreamWriter()`

**作用与语义：**

毁灭者。

### `bool QXmlStreamWriter::autoFormatting() const`

**作用与语义：**

如果启用了自动格式化，返回`true`，否则会`false`。
注意：属性自动格式化的获取函数。

### `QIODevice *QXmlStreamWriter::device() const`

**作用与语义：**

返回与`QXmlStreamWriter`关联的当前设备，若未分配设备则返回`nullptr`。

### `[since 6.10] QXmlStreamWriter::Error QXmlStreamWriter::error() const`

**作用与语义：**

返回写入者的当前错误状态。
如果没有发生错误，该函数返回`QXmlStreamWriter::Error::None`。

### `[since 6.10] QString QXmlStreamWriter::errorString() const`

**作用与语义：**

如果发生错误，返回其相关的错误信息。
错误消息要么由`QXmlStreamWriter`内部设置，要么由用户通过`raiseError()`提供。如果没有发生错误，该函数返回一个空字符串。

### `bool QXmlStreamWriter::hasError() const`

**作用与语义：**

如果在尝试写入数据时发生错误，返回`true`。
如果错误`Error::IO`，后续对底层`QIODevice`的写入将失败。在其他情况下，数据可能会写入文档，数据形式错误。
错误状态永远不会被重置。错误发生后发生的写入可以被忽略，即使错误条件已被清除。

### `[since 6.10] void QXmlStreamWriter::raiseError(QAnyStringView message)`

**作用与语义：**

在给定`message`下会引发自定义错误。
此功能用于手动指示写入过程中发生错误，例如应用层验证失败。

### `void QXmlStreamWriter::setAutoFormatting(bool enable)`

**作用与语义：**

该属性包含流写器的自动格式化标志。
该属性控制流写入器是否自动格式化生成的XML数据。启用后，写入者会自动在元素间的空部分添加换行和缩进（可忽略的空白）。自动格式化的主要目的是将数据拆分为多行，并提高人类阅读者的可读性。缩进深度可以通过`autoFormattingIndent`属性控制。
默认情况下，自动格式化是被禁用的。

**如何使用：** 调用 `setAutoFormatting(...)` 修改 `autoFormatting`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QXmlStreamWriter::setDevice(QIODevice *device)`

**作用与语义：**

将当前设备设置为`device`。如果你想让流写入`QByteArray`，可以创建一个`QBuffer`设备。

### `void QXmlStreamWriter::writeAttribute(QAnyStringView namespaceUri, QAnyStringView name, QAnyStringView value)`

**作用与语义：**

编写带有 `name` 和 `value` 的属性，并在指定`namespaceUri`前缀。如果命名空间尚未声明，`QXmlStreamWriter` 会为其生成命名空间声明。
该函数只能在内容写入前`writeStartElement()`之后或内容写入后调用`writeEmptyElement()`。
注意：在6.5之前的Qt版本中，该功能需要的是`QString`，而不是`QAnyStringView`。

### `void QXmlStreamWriter::writeAttribute(const QXmlStreamAttribute &attribute)`

**作用与语义：**

`attribute`写道。
该函数只能在内容写入前`writeStartElement()`之后或`writeEmptyElement()`之后调用。

### `void QXmlStreamWriter::writeAttribute(QAnyStringView qualifiedName, QAnyStringView value)`

**作用与语义：**

写一个带有`qualifiedName`和`value`属性的。
该函数只能在内容写入前`writeStartElement()`或内容写入后调用`writeEmptyElement()`。
注意：在6.5之前的Qt版本中，该功能采用`QString`，而非取`QAnyStringView`。

### `void QXmlStreamWriter::writeAttributes(const QXmlStreamAttributes &attributes)`

**作用与语义：**

写入属性向量 `attributes`。如果属性中引用的命名空间尚未声明，`QXmlStreamWriter` 将为其生成命名空间声明。此函数只能在 `writeStartElement()` 之后且在写入任何内容之前调用，或在 `writeEmptyElement()` 之后调用。

### `void QXmlStreamWriter::writeCDATA(QAnyStringView text)`

**作用与语义：**

将`text`写入为 CDATA 部分。如果`text`包含禁用字符序列“]]>”，则被拆分为不同的 CDATA 部分。
这个函数主要是为了完整性。通常你不需要使用它，因为`writeCharacters()`会自动转义出所有非内容字符。
注意：在6.5之前的Qt版本中，该函数采用了`QString`，而非`QAnyStringView`。

### `void QXmlStreamWriter::writeCharacters(QAnyStringView text)`

**作用与语义：**

写入`text`。字符“<”、“&”和“”“作为实体引用”<“、”&“和”“”逃逸。为避免禁用序列“]]>”，“>”也被转为“>”。
注意：在6.5之前的Qt版本中，这个功能是用了`QString`，而不是用`QAnyStringView`。

### `void QXmlStreamWriter::writeComment(QAnyStringView text)`

**作用与语义：**

将`text`写成XML注释，其中`text`不得包含禁止的序列`--`或以`-`结尾。注意，XML不提供任何在注释中逃逸`-`的方法。
注意：在 6.5 之前的 Qt 版本中，这个功能是用 `QString` 而不是 `QAnyStringView`。

### `void QXmlStreamWriter::writeCurrentToken(const QXmlStreamReader &reader)`

**作用与语义：**

写入当前`reader`状态。支持所有可能的有效状态。
该函数的目的是支持XML数据的链式处理。

### `void QXmlStreamWriter::writeDTD(QAnyStringView dtd)`

**作用与语义：**

编写DTD部分。`dtd`代表XML 1.0规范中完整的doctypedecl生成。
注意：在 6.5 之前的 Qt 版本中，该功能采用了 `QString` 的使用，而非 `QAnyStringView`。

### `void QXmlStreamWriter::writeDefaultNamespace(QAnyStringView namespaceUri)`

**作用与语义：**

为`namespaceUri`写一个默认命名空间声明。
如果调用了`writeStartElement()`或`writeEmptyElement()`，声明适用于当前元素;否则则适用于下一个子元素。
请注意，命名空间 http://www.w3.org/XML/1998/namespace（绑定于 xmlns）和 http://www.w3.org/2000/xmlns/（绑定于 xml）按定义不能被默认声明。
注意：在6.5之前的Qt版本中，该功能采用了`QString`，而非`QAnyStringView`。

### `void QXmlStreamWriter::writeEmptyElement(QAnyStringView namespaceUri, QAnyStringView name)`

**作用与语义：**

写入一个空元素，前缀为`name`，前缀为指定`namespaceUri`。如果命名空间尚未声明，`QXmlStreamWriter`将为其生成命名空间声明。后续调用`writeAttribute()`会为该元素添加属性。
注意：在6.5之前的Qt版本中，该功能需要`QString`，而非 `QAnyStringView`。

### `void QXmlStreamWriter::writeEmptyElement(QAnyStringView qualifiedName)`

**作用与语义：**

写一个带有限定名称 `qualifiedName` 的空元素。后续调用 `writeAttribute()` 会为该元素添加属性。
注意：在6.5之前的Qt版本中，该函数采用`QString`，而非取`QAnyStringView`。

### `void QXmlStreamWriter::writeEndDocument()`

**作用与语义：**

关闭所有剩余的开起始元素并写入换行。

### `void QXmlStreamWriter::writeEndElement()`

**作用与语义：**

关闭之前的起始元素。

### `void QXmlStreamWriter::writeEntityReference(QAnyStringView name)`

**作用与语义：**

将实体引用写成“&`name`;”，对流`name`。
注意：在6.5之前的Qt版本中，该功能采用了`QString`，而非被`QAnyStringView`。

### `void QXmlStreamWriter::writeNamespace(QAnyStringView namespaceUri, QAnyStringView prefix = {})`

**作用与语义：**

为`namespaceUri`写入命名空间声明，`prefix`。如果`prefix`空，`QXmlStreamWriter`赋予一个唯一前缀，由字母“n”和数字组成。
如果调用了`writeStartElement()`或`writeEmptyElement()`，声明适用于当前元素;否则则适用于下一个子元素。
注意，前缀 xml 既预定义又保留给 http://www.w3.org/XML/1998/namespace，而  又不能绑定到任何其他前缀。前缀 xmlns 及其 URI http://www.w3.org/2000/xmlns/ 用于命名空间机制本身，因此在声明中完全禁止。
注意：在6.5之前的Qt版本中，该功能采用`QString`，而非`QAnyStringView`。

### `void QXmlStreamWriter::writeProcessingInstruction(QAnyStringView target, QAnyStringView data = {})`

**作用与语义：**

编写带有 `target` 和 `data` 的 XML 处理指令，其中 `data` 中不得包含序列“？>”。
注意：在6.5之前的Qt版本中，这个功能是`QString`的，而不是`QAnyStringView`。

### `void QXmlStreamWriter::writeStartDocument(QAnyStringView version)`

**作用与语义：**

编写以XML版本号开端的文档`version`。
注意：该函数不验证版本字符串，允许手动设置。然而，`QXmlStreamWriter`仅支持 XML 1.0。设置非“1.0”版本字符串不会改变写入者的行为或转义规则。确保声明版本与实际内容之间的一致性是调用者的责任。
注意：在6.5之前的Qt版本中，该功能采用了`QString`，而非`QAnyStringView`。

### `void QXmlStreamWriter::writeStartDocument(QAnyStringView version, bool standalone)`

**作用与语义：**

编写以XML版本号`version`和独立属性`standalone`开头的文档。
注意：该函数不验证版本字符串，允许手动设置。然而，`QXmlStreamWriter`仅支持 XML 1.0。设置非“1.0”版本字符串不会改变写作者的行为或逃逸规则。确保声明版本与实际内容之间的一致性是调用者的责任。
注意：在6.5之前的Qt版本中，该功能采用了`QString`，而非`QAnyStringView`。

### `void QXmlStreamWriter::writeStartDocument()`

**作用与语义：**

编写以XML版本号“1.0”开头的文档。

### `void QXmlStreamWriter::writeStartElement(QAnyStringView namespaceUri, QAnyStringView name)`

**作用与语义：**

写入带有 `name` 的起始元素，前缀为指定`namespaceUri`。如果命名空间尚未声明，`QXmlStreamWriter` 会为其生成命名空间声明。后续调用 `writeAttribute()` 会为该元素添加属性。
注意：在6.5之前的Qt版本中，该功能采用`QString`，而非取`QAnyStringView`。

### `void QXmlStreamWriter::writeStartElement(QAnyStringView qualifiedName)`

**作用与语义：**

写一个带有`qualifiedName`的起始元素。后续调用`writeAttribute()`会为该元素添加属性。
注意：在6.5之前的Qt版本中，该功能采用了`QString`，而非`QAnyStringView`。

### `void QXmlStreamWriter::writeTextElement(QAnyStringView namespaceUri, QAnyStringView name, QAnyStringView text)`

**作用与语义：**

编写一个带有`name`的文本元素，前缀为指定`namespaceUri`，`text`。如果命名空间尚未声明，`QXmlStreamWriter`将为其生成命名空间声明。
这是一个便利函数，等价于：
注意：在6.5之前的Qt版本中，该功能采用了`QString`，而非`QAnyStringView`。

**官方示例：**

```cpp
 stream.writeStartElement(namespaceUri, name);
 stream.writeCharacters(text);
 stream.writeEndElement();
```

### `void QXmlStreamWriter::writeTextElement(QAnyStringView qualifiedName, QAnyStringView text)`

**作用与语义：**

写一个带有`qualifiedName`和`text`的文本元素。
这是一个便利函数，等价于：
注意：在6.5之前的Qt版本中，该功能采用`QString`，而非`QAnyStringView`。

**官方示例：**

```cpp
 stream.writeStartElement(qualifiedName);
 stream.writeCharacters(text);
 stream.writeEndElement();
```

### `int autoFormattingIndent() const`

**作用与语义：**

该属性表示启用自动格式时用于缩进的空格或制表符数。正数表示空格，负数表示制表表。
默认缩进是4。

**如何使用：** 调用 `autoFormattingIndent()` 读取当前值；它不会修改应用状态。

### `void setAutoFormattingIndent(int spacesOrTabs)`

**作用与语义：**

该属性表示启用自动格式时用于缩进的空格或制表符数。正数表示空格，负数表示制表表。
默认缩进是4。

**如何使用：** 调用 `setAutoFormattingIndent(...)` 修改 `autoFormattingIndent`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setStopWritingOnError(bool stop)`

**作用与语义：**

该特性允许在遇到错误后停止写入设备。
如果该属性设置为`true`，写入者在遇到任何错误时立即停止写入，并忽略所有后续写入操作。当该属性设为`false`时，写入者可以在错误后继续写入，跳过无效写入但允许继续输出。
注意这包括`Error::InvalidCharacter`、`Error::Encoding`和`Error::Custom`。无论设置如何，`Error::IO`始终被视为终端，停止写入。
默认值是`false`。

**如何使用：** 调用 `setStopWritingOnError(...)` 修改 `stopWritingOnError`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `bool stopWritingOnError() const`

**作用与语义：**

该特性允许在遇到错误后停止写入设备。
如果该属性设置为`true`，写入者在遇到任何错误时立即停止写入，并忽略所有后续写入操作。当该属性设为`false`时，写入者可以在错误后继续写入，跳过无效写入但允许继续输出。
注意这包括`Error::InvalidCharacter`、`Error::Encoding`和`Error::Custom`。无论设置如何，`Error::IO`始终被视为终端，停止写入。
默认值是`false`。

**如何使用：** 调用 `stopWritingOnError()` 读取当前值；它不会修改应用状态。

## 6. 深入实践与常见坑

### 生命周期和资源边界

解析结果通常是值对象，可在作用域内传递；流式解析器则依赖输入设备和读取顺序。解析错误、结构合法和业务字段合法是三个不同层次，必须分别检查。

### 状态和错误边界

先判断文档是否为空、根节点类型和解析错误，再访问字段；字段缺失、类型不匹配、空值和默认值要分开处理。序列化时要明确紧凑/格式化输出和编码。

### 线程边界

值形式的解析结果可以复制后跨线程处理；共享设备、流对象和可变 DOM 不应无保护地跨线程使用。大文档要评估一次性树结构的内存成本，必要时用流式 API。

### 最容易出现的错误

不要只检查 parse 成功；不要假设字段一定存在且类型固定；不要把用户输入直接当作可信结构；大文件不要无条件 readAll 和构造整棵树。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QXmlStreamWriter` 所属机制类型：结构化文本解析机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
