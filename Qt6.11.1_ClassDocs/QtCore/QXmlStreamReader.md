# QXmlStreamReader

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** XML 流式读取器，按令牌顺序读取 XML，适合大文件和低内存解析。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QXmlStreamReader`：XML 流式读取器，按令牌顺序读取 XML，适合大文件和低内存解析。

**内部模型：** JSON 通常表示为 value/object/array 树，XML 则包含元素、属性、文本和层级。文档容器负责解析和序列化，具体字段/节点访问由 object、array、value 或 DOM/流式读取对象完成。

**适用场景：** 接收字节数据后显式指定编码和解析选项，检查错误对象，再按类型访问节点，校验业务字段，最后序列化或转换成领域对象。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要只检查 parse 成功；不要假设字段一定存在且类型固定；不要把用户输入直接当作可信结构；大文件不要无条件 readAll 和构造整棵树。

## 2. 依赖与对象关系

- 头文件：`#include <QXmlStreamReader>`
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

- `enum Error { NoError, CustomError, NotWellFormedError, PrematureEndOfDocumentError, UnexpectedElementError }`
- `enum ReadElementTextBehaviour { ErrorOnUnexpectedElement, IncludeChildElements, SkipChildElements }`
- `enum TokenType { NoToken, Invalid, StartDocument, EndDocument, StartElement, …, ProcessingInstruction }`

### 属性

- `namespaceProcessing : bool`

### 公有函数

- `QXmlStreamReader()`
- `QXmlStreamReader(QAnyStringView data)`
- `QXmlStreamReader(QIODevice *device)`
- `QXmlStreamReader(const QByteArray &data)`
- `~QXmlStreamReader()`
- `void addData(QAnyStringView data)`
- `void addData(const QByteArray &data)`
- `void addExtraNamespaceDeclaration(const QXmlStreamNamespaceDeclaration &extraNamespaceDeclaration)`
- `void addExtraNamespaceDeclarations(const QXmlStreamNamespaceDeclarations &extraNamespaceDeclarations)`
- `bool atEnd() const`
- `QXmlStreamAttributes attributes() const`
- `qint64 characterOffset() const`
- `void clear()`
- `qint64 columnNumber() const`
- `QIODevice * device() const`
- `QStringView documentEncoding() const`
- `QStringView documentVersion() const`
- `QStringView dtdName() const`
- `QStringView dtdPublicId() const`
- `QStringView dtdSystemId() const`
- `QXmlStreamEntityDeclarations entityDeclarations() const`
- `int entityExpansionLimit() const`
- `QXmlStreamEntityResolver * entityResolver() const`
- `QXmlStreamReader::Error error() const`
- `QString errorString() const`
- `bool hasError() const`
- `(since 6.6) bool hasStandaloneDeclaration() const`
- `bool isCDATA() const`
- `bool isCharacters() const`
- `bool isComment() const`
- `bool isDTD() const`
- `bool isEndDocument() const`
- `bool isEndElement() const`
- `bool isEntityReference() const`
- `bool isProcessingInstruction() const`
- `bool isStandaloneDocument() const`
- `bool isStartDocument() const`
- `bool isStartElement() const`
- `bool isWhitespace() const`
- `qint64 lineNumber() const`
- `QStringView name() const`
- `QXmlStreamNamespaceDeclarations namespaceDeclarations() const`
- `bool namespaceProcessing() const`
- `QStringView namespaceUri() const`
- `QXmlStreamNotationDeclarations notationDeclarations() const`
- `QStringView prefix() const`
- `QStringView processingInstructionData() const`
- `QStringView processingInstructionTarget() const`
- `QStringView qualifiedName() const`
- `void raiseError(const QString &message = QString())`
- `QString readElementText(QXmlStreamReader::ReadElementTextBehaviour behaviour = ErrorOnUnexpectedElement)`
- `QXmlStreamReader::TokenType readNext()`
- `bool readNextStartElement()`
- `(since 6.10) QString readRawInnerData()`
- `void setDevice(QIODevice *device)`
- `void setEntityExpansionLimit(int limit)`
- `void setEntityResolver(QXmlStreamEntityResolver *resolver)`
- `void setNamespaceProcessing(bool)`
- `void skipCurrentElement()`
- `QStringView text() const`
- `QString tokenString() const`
- `QXmlStreamReader::TokenType tokenType() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QXmlStreamReader::Error`

**作用与语义：**

该枚举指定了不同的错误情况。
- `QXmlStreamReader::NoError`：`0`;未发生错误。
- `QXmlStreamReader::CustomError`：`2`;`raiseError()` 中出现了自定义错误
- `QXmlStreamReader::NotWellFormedError`：`3`;解析器内部因读取XML未规范而报错。
- `QXmlStreamReader::PrematureEndOfDocumentError`：`4`;输入流在解析完好的XML文档之前就已结束。如果流中出现更多XML时，可以通过调用`addData()`或等待它在`device()`上到达，从而恢复该错误。
- `QXmlStreamReader::UnexpectedElementError`：`1`;解析器遇到的元素或标记与预期不同。

### `enum QXmlStreamReader::ReadElementTextBehaviour`

**作用与语义：**

这个枚举规定了`readElementText()`的不同行为。
- `QXmlStreamReader::ErrorOnUnexpectedElement`：`0`;遇到子元素时，举起`UnexpectedElementError`并返回已读内容。
- `QXmlStreamReader::IncludeChildElements`：`1`;递归地包含子元素中的文本。
- `QXmlStreamReader::SkipChildElements`：`2`;跳过子元素。

### `enum QXmlStreamReader::TokenType`

**作用与语义：**

这个枚举指定了读者刚刚读取的代币类型。
- `QXmlStreamReader::NoToken`：`0`;读者尚未阅读任何内容。
- `QXmlStreamReader::Invalid`：`1`;发生了错误，`error()`和`errorString()`中报告。
- `QXmlStreamReader::StartDocument`：`2`;读取器以`documentVersion()`报告XML版本号，`documentEncoding()`中报告XML文档中指定的编码。如果文档声明为独立，`isStandaloneDocument()`返回`true`;否则返回`false`。
- `QXmlStreamReader::EndDocument`：`3`;读者报告文档结尾。
- `QXmlStreamReader::StartElement`：`4`;读者报告元素的起始，`namespaceUri()`和`name()`。空元素也以StartElement报告，紧接EndElement。方便函数`readElementText()`可调用，将所有内容串接至对应的EndElement。属性报告于`attributes()`，命名空间声明报告于`namespaceDeclarations()`。
- `QXmlStreamReader::EndElement`：`5`;读者报告元素结尾时，`namespaceUri()` 和 `name()`。
- `QXmlStreamReader::Characters`：`6`;读取器报告字符`text()`。如果字符全部为空白，`isWhitespace()`返回`true`。如果字符源自CDATA部分，`isCDATA()`返回`true`。
- `QXmlStreamReader::Comment`：`7`;读者报告一条评论，`text()`。
- `QXmlStreamReader::DTD`：`8`;读者以`text()`报告DTD，以`notationDeclarations()`表示，实体声明以以在`entityDeclarations()`。DTD声明的详细信息在`dtdName()`、`dtdPublicId()`和`dtdSystemId()`中报告。
- `QXmlStreamReader::EntityReference`：`9`;读者报告无法解析的实体引用。引用名称以`name()`报告，替换文本以`text()`表示。
- `QXmlStreamReader::ProcessingInstruction`：`10`;读卡器报告处理指令，表示`processingInstructionTarget()`和 `processingInstructionData()`。

### `namespaceProcessing : bool`

**作用与语义：**

此属性保存流读取器的命名空间处理标志。
此属性控制流读取器是否处理命名空间。如果启用，读取器将处理命名空间，否则不会。
默认情况下，命名空间处理是启用的。

**如何使用：** 调用 `namespaceProcessing()` 读取当前值；它不会修改应用状态。

### `QXmlStreamReader::QXmlStreamReader()`

**作用与语义：**

构建一个流读器。

### `[explicit] QXmlStreamReader::QXmlStreamReader(QAnyStringView data)`

**作用与语义：**

创建一个新的流读取器，从`data`读取。
注意：在 6.5 之前的 Qt 版本中，该构造器在 `QString` 和 `const char*` 时被超载。

### `[explicit] QXmlStreamReader::QXmlStreamReader(QIODevice *device)`

**作用与语义：**

创建一个新的流读取器，从`device`读取数据。

### `[explicit] QXmlStreamReader::QXmlStreamReader(const QByteArray &data)`

**作用与语义：**

创建一个新的流读取器，从`data`读取数据。

### `[noexcept] QXmlStreamReader::~QXmlStreamReader()`

**作用与语义：**

摧毁读者。

### `void QXmlStreamReader::addData(QAnyStringView data)`

**作用与语义：**

这会增加阅读器阅读的更多内容`data`。如果阅读器有`device()`，这个功能就没有任何作用。
注意：在 6.5 之前的 Qt 版本中，该功能对 `QString` 和 `const char*` 重载。

### `void QXmlStreamReader::addData(const QByteArray &data)`

**作用与语义：**

为读者增加了阅读`data`。如果读者有`device()`，这个功能就没有任何作用。

### `void QXmlStreamReader::addExtraNamespaceDeclaration(const QXmlStreamNamespaceDeclaration &extraNamespaceDeclaration)`

**作用与语义：**

添加一个`extraNamespaceDeclaration`。声明对当前元素的子节点有效，或者如果函数在读取任何元素之前被调用，则适用于整个 XML 文档。

### `void QXmlStreamReader::addExtraNamespaceDeclarations(const QXmlStreamNamespaceDeclarations &extraNamespaceDeclarations)`

**作用与语义：**

添加由`extraNamespaceDeclarations`指定的声明向量。

### `bool QXmlStreamReader::atEnd() const`

**作用与语义：**

如果读取者已阅读到XML文档结束，或发生`error()`且阅读中止，返回`true`。否则返回`false`。
当atEnd()和`hasError()`返回true，`error()`返回`PrematureEndOfDocumentError`时，表示XML迄今为止是良好构造的，但尚未解析完整的XML文档。如果从`QByteArray`读取XML时，可以用`addData()`添加下一块XML;如果从`QIODevice`读取，则等待更多数据到达。无论哪种方式，一旦有更多数据可用，atEnd()都会返回false。

### `QXmlStreamAttributes QXmlStreamReader::attributes() const`

**作用与语义：**

返回`StartElement`的属性。

### `qint64 QXmlStreamReader::characterOffset() const`

**作用与语义：**

返回当前字符偏移量，起始于0。

### `void QXmlStreamReader::clear()`

**作用与语义：**

移除读卡器中的所有`device()`或数据，并将其内部状态重置为初始状态。

### `qint64 QXmlStreamReader::columnNumber() const`

**作用与语义：**

返回当前列号，起始于0。

### `QIODevice *QXmlStreamReader::device() const`

**作用与语义：**

返回与`QXmlStreamReader`关联的当前设备，若未分配设备则返回`nullptr`。

### `QStringView QXmlStreamReader::documentEncoding() const`

**作用与语义：**

如果`tokenType()` `StartDocument`，该函数返回XML声明中指定的编码字符串。否则返回空字符串。

### `QStringView QXmlStreamReader::documentVersion() const`

**作用与语义：**

如果`tokenType()` `StartDocument`，该函数返回XML声明中指定的版本字符串。否则返回空字符串。

### `QStringView QXmlStreamReader::dtdName() const`

**作用与语义：**

如果`tokenType()` `DTD`，该函数返回DTD的名称。否则返回空字符串。

### `QStringView QXmlStreamReader::dtdPublicId() const`

**作用与语义：**

如果`tokenType()` `DTD`，该函数返回DTD的公共标识符。否则返回空字符串。

### `QStringView QXmlStreamReader::dtdSystemId() const`

**作用与语义：**

如果`tokenType()` `DTD`，该函数返回DTD的系统标识符。否则返回空字符串。

### `QXmlStreamEntityDeclarations QXmlStreamReader::entityDeclarations() const`

**作用与语义：**

如果`tokenType()` `DTD`，该函数返回DTD未解析的（外部）实体声明。否则返回空向量。
`QXmlStreamEntityDeclarations`类被定义为`QXmlStreamEntityDeclaration`的`QList`。

### `int QXmlStreamReader::entityExpansionLimit() const`

**作用与语义：**

返回单个实体允许扩展的最大字符数。如果单个实体扩展超过给定限制，则该文档不被视为良好格式。

### `QXmlStreamEntityResolver *QXmlStreamReader::entityResolver() const`

**作用与语义：**

返回实体解析器，若无实体解析器则返回`nullptr`。

### `QXmlStreamReader::Error QXmlStreamReader::error() const`

**作用与语义：**

返回当前错误的类型，若无错误则返回`NoError`。

### `QString QXmlStreamReader::errorString() const`

**作用与语义：**

返回与`raiseError()`设置的错误信息。

### `bool QXmlStreamReader::hasError() const`

**作用与语义：**

如果发生错误，返回`true`，否则`false`。

### `[since 6.6] bool QXmlStreamReader::hasStandaloneDeclaration() const`

**作用与语义：**

如果该文档有明确的独立声明（可以是“是”或“否”），返回`true`;否则返回`false`;
如果没有解析任何 XML 声明，该函数返回 `false`。

### `bool QXmlStreamReader::isCDATA() const`

**作用与语义：**

如果读取器报告的字符源自 CDATA 部分，返回 `true`;否则返回 `false`。

### `bool QXmlStreamReader::isCharacters() const`

**作用与语义：**

如果 `tokenType()` 等于 `Characters`，则返回 `true`；否则返回 `false`。

### `bool QXmlStreamReader::isComment() const`

**作用与语义：**

如果 `tokenType()` 等于 `Comment`，则返回 `true`；否则返回 `false`。

### `bool QXmlStreamReader::isDTD() const`

**作用与语义：**

如果 `tokenType()` 等于 `DTD`，则返回 `true`；否则返回 `false`。

### `bool QXmlStreamReader::isEndDocument() const`

**作用与语义：**

如果 `tokenType()` 等于 `EndDocument`，则返回 `true`；否则返回 `false`。

### `bool QXmlStreamReader::isEndElement() const`

**作用与语义：**

如果 `tokenType()` 等于 `EndElement`，则返回 `true`；否则返回 `false`。

### `bool QXmlStreamReader::isEntityReference() const`

**作用与语义：**

如果 `tokenType()` 等于 `EntityReference`，则返回 `true`；否则返回 `false`。

### `bool QXmlStreamReader::isProcessingInstruction() const`

**作用与语义：**

如果 `tokenType()` 等于 `ProcessingInstruction`，则返回 `true`；否则返回 `false`。

### `bool QXmlStreamReader::isStandaloneDocument() const`

**作用与语义：**

如果该文档在XML声明中被声明为独立文档，返回`true`;否则返回`false`。
如果没有解析任何 XML 声明，该函数返回 `false`。

### `bool QXmlStreamReader::isStartDocument() const`

**作用与语义：**

如果 `tokenType()` 等于 `StartDocument`，则返回 `true`；否则返回 `false`。

### `bool QXmlStreamReader::isStartElement() const`

**作用与语义：**

如果 `tokenType()` 等于 `StartElement`，则返回 `true`；否则返回 `false`。

### `bool QXmlStreamReader::isWhitespace() const`

**作用与语义：**

如果读取者报告的字符仅包含空白，返回`true`;否则返回`false`。

### `qint64 QXmlStreamReader::lineNumber() const`

**作用与语义：**

返回当前的行号，起始于1。

### `QStringView QXmlStreamReader::name() const`

**作用与语义：**

返回`StartElement`、`EndElement`或`EntityReference`的本地名称。

### `QXmlStreamNamespaceDeclarations QXmlStreamReader::namespaceDeclarations() const`

**作用与语义：**

如果`tokenType()`是`StartElement`，该函数返回元素的命名空间声明。否则返回空向量。
`QXmlStreamNamespaceDeclarations`类被定义为`QXmlStreamNamespaceDeclaration`的`QList`。

### `QStringView QXmlStreamReader::namespaceUri() const`

**作用与语义：**

返回`StartElement`或`EndElement`的命名 spaceUri。

### `QXmlStreamNotationDeclarations QXmlStreamReader::notationDeclarations() const`

**作用与语义：**

如果`tokenType()` `DTD`，该函数返回DTD的符号声明。否则返回空向量。
`QXmlStreamNotationDeclarations`类被定义为`QXmlStreamNotationDeclaration`的`QList`。

### `QStringView QXmlStreamReader::prefix() const`

**作用与语义：**

返回`StartElement`或`EndElement`的前缀。

### `QStringView QXmlStreamReader::processingInstructionData() const`

**作用与语义：**

返回`ProcessingInstruction`的数据。

### `QStringView QXmlStreamReader::processingInstructionTarget() const`

**作用与语义：**

返回`ProcessingInstruction`的目标。

### `QStringView QXmlStreamReader::qualifiedName() const`

**作用与语义：**

返回`StartElement`或`EndElement`的限定名称;
限定名称是XML数据中元素的原始名称。它由命名空间前缀、冒号和元素的本地名称组成。由于命名空间前缀不是唯一的（同一个前缀可以指向不同的命名空间，不同的前缀也可能指向同一个命名空间），你不应该使用qualifiedName()，而是用解析后的`namespaceUri()`和属性的本地`name()`。

### `void QXmlStreamReader::raiseError(const QString &message = QString())`

**作用与语义：**

会带可选的错误`message`提出自定义错误。

### `QString QXmlStreamReader::readElementText(QXmlStreamReader::ReadElementTextBehaviour behaviour = ErrorOnUnexpectedElement)`

**作用与语义：**

在读取`StartElement`时调用便利函数。读取至对应`EndElement`，返回中间所有文本。若无错误，调用该函数后的当前令牌（见`tokenType()`）为`EndElement`。
当函数读取`Characters`或`EntityReference`个符号时，会串接`text()`，但跳过`ProcessingInstruction`和`Comment`。如果当前符号未`StartElement`，则返回一个空字符串。
`behaviour`定义了在到达`EndElement`之前读取其他内容时会发生什么。该函数可以包含子元素的文本（例如对HTML有用）、忽略子元素，或者提出`UnexpectedElementError`返回已读内容（默认）。

### `QXmlStreamReader::TokenType QXmlStreamReader::readNext()`

**作用与语义：**

读取下一个令牌并返回其类型。
除了一个例外，一旦 readNext() 报告了`error()`，XML 流就无法进一步读取。此时 `atEnd()` 返回 `true`，`hasError()` 返回 `true`，而该函数返回 `QXmlStreamReader::Invalid`。
例外是当`error()`返回`PrematureEndOfDocumentError`时。当到达一个本应良好排列的XML块的结尾，但该块不代表完整的XML文档时，会报告该错误。在这种情况下，解析可以通过调用`addData()`添加下一个XML块来恢复，当流从`QByteArray`读取时，或者在从`device()`读取流时等待更多数据到达。

### `bool QXmlStreamReader::readNextStartElement()`

**作用与语义：**

读取直到当前元素内的下一个起始元素。当到达起始元素时返回`true`。到达结束元素或发生错误时返回假。
当前元素是与最近解析的起始元素匹配且尚未达到匹配的末端元素的元素。当解析器到达末端元素时，当前元素即为父元素。
这是一个方便你只关心解析XML元素时的函数。QXmlStream书签示例大量使用了该函数。

### `[since 6.10] QString QXmlStreamReader::readRawInnerData()`

**作用与语义：**

读取并返回当前元素的原始内部XML内容。该功能有助于检索元素内嵌入的完整内容，包括嵌套标签、文本、注释、处理指令、CDATA部分及其他标记——保持原始XML结构。
当前元素是与最近解析的起始元素匹配且尚未达到匹配的末端元素的元素。当解析器到达末端元素时，当前元素即为父元素。
注意：DTD 中定义的实体引用在解析过程中被解析并以明文返回，因为 DTD 声明是单独处理的，不属于元素内容的一部分。输出中只有五个预定义的 XML 实体（`<`、`>`、`&`、`'`、`"`;）会被重新转义。

### `void QXmlStreamReader::setDevice(QIODevice *device)`

**作用与语义：**

将当前设备设置为`device`。设置设备会将流重置到初始状态。

### `void QXmlStreamReader::setEntityExpansionLimit(int limit)`

**作用与语义：**

将单个实体允许扩展的最大字符数设定为`limit`。如果单个实体扩展超过给定限制，则该文档不被视为良好格式。
其限制是为了防止在加载未知XML文档时遭受DoS攻击，因为递归实体扩展可能会耗尽所有可用内存。
该属性的默认值为4096字符。

### `void QXmlStreamReader::setEntityResolver(QXmlStreamEntityResolver *resolver)`

**作用与语义：**

这让`resolver`成为新的`entityResolver()`。
流读取器不拥有解析器的所有权。调用者有责任确保解析器在流读取器对象的整个生命周期内有效，或直到设置另一个解析器或`nullptr`。

### `void QXmlStreamReader::skipCurrentElement()`

**作用与语义：**

读取至当前元素结束，跳过所有子节点。该函数用于跳过未知元素。
当前元素是与最近解析的起始元素匹配且尚未达到匹配的末端元素的元素。当解析器到达末端元素时，当前元素即为父元素。

### `QStringView QXmlStreamReader::text() const`

**作用与语义：**

返回`Characters`、`Comment`、`DTD`或`EntityReference`的文本。

### `QString QXmlStreamReader::tokenString() const`

**作用与语义：**

返回读取器当前的令牌作为字符串。

### `QXmlStreamReader::TokenType QXmlStreamReader::tokenType() const`

**作用与语义：**

返回当前令牌的类型。
当前代币还可以查询便利功能`isStartDocument()`、`isEndDocument()`、`isStartElement()`、`isEndElement()`、`isCharacters()`、`isComment()`、`isDTD()`、`isEntityReference()`和`isProcessingInstruction()`。

### `bool namespaceProcessing() const`

**作用与语义：**

此属性保存流读取器的命名空间处理标志。
此属性控制流读取器是否处理命名空间。如果启用，读取器将处理命名空间，否则不会。
默认情况下，命名空间处理是启用的。

**如何使用：** 调用 `namespaceProcessing()` 读取当前值；它不会修改应用状态。

### `void setNamespaceProcessing(bool)`

**作用与语义：**

此属性保存流读取器的命名空间处理标志。
此属性控制流读取器是否处理命名空间。如果启用，读取器将处理命名空间，否则不会。
默认情况下，命名空间处理是启用的。

**如何使用：** 调用 `setNamespaceProcessing(...)` 修改 `namespaceProcessing`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QXmlStreamReader` 所属机制类型：结构化文本解析机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
