# Qt QXmlStreamReader 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QXmlStreamReader>`  
> 所属模块：`Qt6::Core`  
> 线程属性：所有函数可重入；对象本身不应被多个线程同时修改  
> 定位：非验证、只向前、增量式 XML 1.0 pull parser

## 1. 它解决什么问题

`QXmlStreamReader` 把 XML 文档暴露成一个按顺序产生的 token 流。调用方主动调用 `readNext()` 取下一个 token，再依据 `tokenType()`、`isStartElement()`、`name()`、`text()` 等 API 处理它。

它解决的是“我需要读取 XML，但不想先把整个文档构造成树”的问题。与 `QDomDocument` 相比，它不保留完整 DOM，因此适合大文件、网络响应、日志流、配置导入和只关心少数节点的解析任务。代价是：解析后不能任意回看，业务代码必须自己维护需要的状态。

它属于 pull parser，而不是 SAX 风格的 push parser：

- SAX 由解析器在合适时机回调应用提供的 handler；
- `QXmlStreamReader` 由应用控制读取节奏，可以把解析逻辑拆成递归下降函数；
- reader 是 forward-only 的，已经消费的 token 不会提供通用的回退操作；
- 它检查 XML 1.0 的良构性，但不做 DTD 验证，也不处理外部 parsed entity。

它只支持 XML 1.0。输入声明 `<?xml version="1.1"?>` 会产生解析错误；即使 Writer 手工写出其它版本字符串，也不代表 Qt 实际支持 XML 1.1 语义。

## 2. 输入方式、所有权与生命周期

### 2.1 从 `QIODevice` 读取

```cpp
QFile file("bookmarks.xml");
if (!file.open(QIODevice::ReadOnly)) {
    return;
}

QXmlStreamReader xml(&file);
while (!xml.atEnd()) {
    xml.readNext();
    // 处理当前 token
}
if (xml.hasError()) {
    qWarning() << xml.errorString();
}
```

`QXmlStreamReader(QIODevice *)` 和 `setDevice()` 只保存设备指针，不拥有设备。设备必须在 reader 使用期间保持有效，并且应处于适合读取的状态。`QNetworkReply`、`QFile`、`QBuffer` 等 `QIODevice` 都可以作为来源。

顺序设备可能暂时没有完整数据。网络场景应在 `readyRead()` 中继续驱动解析；不要把“当前暂时读不到更多数据”和“文档已经结束”混为一谈。

### 2.2 从内存数据读取

```cpp
QByteArray data = R"(<root><value>42</value></root>)";
QXmlStreamReader xml(data);

while (!xml.atEnd()) {
    xml.readNext();
}
```

Qt 6.5 起，字符串输入 API 以 `QAnyStringView` 为主，同时保留 `QByteArray` 重载。使用 `QAnyStringView` 时，输入视图至少要在构造函数调用期间有效；解析器会把输入纳入自己的解析缓冲。对于跨多个事件、异步追加的场景，优先使用 `QByteArray` + `addData()` 或 `QIODevice`，让数据边界和生命周期更清楚。

一个 reader 只能在当前输入模型中工作：

- 使用 `QIODevice` 后，`addData()` 不会向该设备追加数据；
- 使用无设备的 reader 时，可以反复调用 `addData()` 追加 XML 片段；
- `setDevice()` 会把 reader 重置到初始状态，已有解析位置和错误状态都会被清掉。

## 3. 最小解析循环

```cpp
QXmlStreamReader xml(input);

while (!xml.atEnd()) {
    const auto type = xml.readNext();
    if (type == QXmlStreamReader::StartElement) {
        if (xml.name() == u"item") {
            const auto id = xml.attributes().value(u"id");
            // 读取当前 item
        }
    } else if (type == QXmlStreamReader::Characters && !xml.isWhitespace()) {
        // 处理文本
    }
}

if (xml.hasError()) {
    qWarning().noquote()
        << QStringLiteral("%1:%2:%3: %4")
               .arg(xml.lineNumber())
               .arg(xml.columnNumber())
               .arg(xml.characterOffset())
               .arg(xml.errorString());
}
```

`atEnd()` 是循环条件，不是成功条件。循环结束后必须再检查 `hasError()`：

- 正常读到 `EndDocument`：`atEnd()` 为 `true`，`hasError()` 为 `false`；
- 语法错误、意外元素或自定义错误：`atEnd()` 也可能为 `true`，但 `hasError()` 为 `true`；
- 增量输入暂时结束：可能是 `PrematureEndOfDocumentError`，这类错误可以在追加数据后恢复。

## 4. Token 状态机

一次 `readNext()` 返回一个 token。当前 token 的附加信息必须在读取下一个 token 前使用，因为许多访问器返回的是当前解析缓冲区的 `QStringView`。

### 4.1 `TokenType`

| 枚举值 | 数值 | 含义 |
| --- | ---: | --- |
| `NoToken` | 0 | reader 尚未读取任何内容。 |
| `Invalid` | 1 | 发生错误；详情看 `error()` 与 `errorString()`。 |
| `StartDocument` | 2 | XML 声明被读取；版本、编码和 standalone 信息可查询。 |
| `EndDocument` | 3 | 文档结束。 |
| `StartElement` | 4 | 开始元素；元素名、属性、命名空间声明可查询。空元素也先报告 `StartElement`，随后报告 `EndElement`。 |
| `EndElement` | 5 | 结束元素。 |
| `Characters` | 6 | 普通文本或 CDATA 文本；内容由 `text()` 返回。 |
| `Comment` | 7 | XML 注释；内容由 `text()` 返回。 |
| `DTD` | 8 | DOCTYPE/DTD；DTD 文本、实体声明、notation 声明可查询。 |
| `EntityReference` | 9 | 未能解析的实体引用；名称由 `name()` 返回，替换文本由 `text()` 返回。 |
| `ProcessingInstruction` | 10 | 处理指令；目标和数据分别由对应 API 返回。 |

XML 声明和 DTD 的顺序受 XML 规则约束。出现元素、字符、实体引用或 `EndDocument` 后，不会再合法地产生 `StartDocument` 或 `DTD`；注释和处理指令可以出现在流中的多个位置。

### 4.2 三个常用读取策略

只关心所有 token 时使用 `readNext()`：

```cpp
while (!xml.atEnd()) {
    switch (xml.readNext()) {
    case QXmlStreamReader::StartElement:
        // ...
        break;
    case QXmlStreamReader::Characters:
        // ...
        break;
    default:
        break;
    }
}
```

只关心元素层级时使用 `readNextStartElement()`。它会跳过当前元素中的非元素 token，遇到子元素返回 `true`，遇到当前元素的结束标签或错误返回 `false`。常见递归写法如下：

```cpp
void readRoot(QXmlStreamReader &xml)
{
    while (xml.readNextStartElement()) {
        if (xml.name() == u"item") {
            readItem(xml);
        } else {
            xml.skipCurrentElement();
        }
    }
}
```

`skipCurrentElement()` 从当前 `StartElement` 读到匹配的 `EndElement`，跳过所有子节点，适合未知扩展节点。调用前应确认当前 token 是开始元素；调用后当前元素变为父元素。

## 5. `readElementText()` 的边界

该函数应在当前 token 是 `StartElement` 时调用。它读取到对应 `EndElement`，返回中间的文本，并在成功时把当前 token 留在该结束元素。它会拼接 `Characters` 和 `EntityReference` 的 `text()`，跳过注释和处理指令。

| 行为 | 子元素出现时的处理 |
| --- | --- |
| `ErrorOnUnexpectedElement` | 默认值。设置 `UnexpectedElementError`，返回到目前为止收集的文本。适合元素按协议只能包含纯文本的场景。 |
| `IncludeChildElements` | 递归包含子元素中的文本。适合需要提取混合内容文本的场景。 |
| `SkipChildElements` | 跳过子元素及其内容，只保留当前层直接读到的文本。 |

如果当前 token 不是 `StartElement`，返回空字符串。它返回的是拥有数据的 `QString`，适合立即保存；不要把它和零拷贝的 `text()` 混淆。

## 6. 增量解析与 `PrematureEndOfDocumentError`

reader 支持输入分块到达。当当前块在 XML 文档完成前结束时，reader 报告 `PrematureEndOfDocumentError`。这不等价于永久失败：

```cpp
QXmlStreamReader xml;

void feed(QByteArray chunk, bool finalChunk)
{
    xml.addData(chunk);

    while (!xml.atEnd()) {
        xml.readNext();
        // 处理已经完成的 token
    }

    if (xml.error() == QXmlStreamReader::PrematureEndOfDocumentError
        && !finalChunk) {
        // 等下一块；追加数据后会恢复
        return;
    }

    if (xml.hasError()) {
        // finalChunk 或真正的解析错误
    }
}
```

使用 `QIODevice` 时，不要在第一次 `readNext()` 返回暂时没有完整文档后立即当成损坏文件。对顺序设备应等待更多数据；网络设备通常在 `readyRead()` 中再次调用解析逻辑。

恢复边界：

- 只有 `PrematureEndOfDocumentError` 允许通过更多 XML 恢复；
- `NotWellFormedError`、`UnexpectedElementError`、`CustomError` 通常是终止性错误；
- `addData()` 已经无设备的 reader 使用时有效；已有 device 时调用无效；
- 最后一个块到达后应确认确实产生了 `EndDocument` 或至少没有错误。

## 7. 命名空间

默认 `namespaceProcessing` 为 `true`。开启时，reader 解析 `prefix:name` 与 `xmlns` 声明，并通过 `namespaceUri()`、`name()`、`prefix()` 提供解析后的结果。识别业务节点时优先比较 URI + local name，因为 prefix 不是稳定标识：

```cpp
if (xml.isStartElement()
    && xml.namespaceUri() == u"https://example.com/book"
    && xml.name() == u"entry") {
    // ...
}
```

关闭命名空间处理后，reader 不解析命名空间，可用 `qualifiedName()` 获取原始的带前缀名称。这适合处理不符合命名空间规则但仍需要读取的独立 XML；关闭后不要再把 `namespaceUri()` 当成可信的解析结果。

`namespaceDeclarations()` 只在当前 token 是 `StartElement` 时有意义，否则返回空列表。它返回当前元素直接声明的命名空间，不是把祖先作用域全部展开后的完整映射。

`addExtraNamespaceDeclaration(s)` 用于为 reader 增加额外的命名空间声明，适合解析 XML 片段时补充片段外部原本存在的上下文。它们不修改输入文本，而是影响后续命名空间解析。

## 8. 字符串视图与位置

`name()`、`namespaceUri()`、`qualifiedName()`、`prefix()`、`text()`、文档信息和 DTD 信息大多返回 `QStringView`。它们通常指向 reader 当前解析缓冲区，生命周期短于拥有型 `QString`；在调用下一个会推进解析的 API、追加数据或清理 reader 后，不要继续保存这些 view。需要长期保存时调用 `.toString()`。

位置 API 从 1 开始计数：

- `lineNumber()`：当前行号；
- `columnNumber()`：当前列号；
- `characterOffset()`：当前字符在输入中的偏移。

它们主要用于构造诊断信息。错误发生后仍可读取它们，但不要把具体偏移当作字节偏移，尤其不要在多字节 UTF-8 输入上直接用它索引 `QByteArray`。

## 9. DTD、实体与安全边界

reader 是非验证解析器。它会处理内部实体的替换文本和内部 DTD 子集中的属性规范化，但不做 DTD 验证，也不处理外部 parsed entity。

当当前 token 是 `DTD` 时：

- `text()` 返回 DTD 文本；
- `dtdName()` 返回文档类型名称；
- `dtdPublicId()`、`dtdSystemId()` 返回对应标识；
- `entityDeclarations()` 返回实体声明；
- `notationDeclarations()` 返回 notation 声明。

`entityExpansionLimit()` 默认是 4096，表示单个实体允许展开到的最大字符数。该限制用于降低递归实体扩展造成内存耗尽或拒绝服务的风险。对于确实需要较大内部实体的受控输入，可以显式设置更高值；面对未知来源 XML 时不要为了“让文件能读”而盲目取消或无限放大限制。

`QXmlStreamEntityResolver` 是非拥有指针。设置 resolver 后，reader 不负责销毁它；resolver 必须在 reader 整个使用期间有效，或者在销毁 resolver 前先设置为另一个 resolver 或 `nullptr`。resolver 的实现也应明确是否允许网络访问，避免解析不可信文档时产生隐式外部请求。

## 10. 错误模型

| 错误 | 含义 | 是否可恢复 |
| --- | --- | --- |
| `NoError` | 没有错误。 | 不适用。 |
| `UnexpectedElementError` | 读取流程遇到调用方不接受的元素或 token，常由 `readElementText()` 默认行为触发。 | 通常不可恢复。 |
| `CustomError` | 调用 `raiseError()` 主动报告的业务错误。 | 通常不可恢复，除非重新 `clear()` 或 `setDevice()` 开始新的解析。 |
| `NotWellFormedError` | 输入不是良构 XML 1.0。 | 通常不可恢复。 |
| `PrematureEndOfDocumentError` | 当前输入块结束，但文档尚未完成。 | 追加数据或等待 device 更多数据后可恢复。 |

`raiseError()` 不抛 C++ 异常，而是把 reader 置于错误状态。错误后 `readNext()` 返回 `Invalid`，`atEnd()` 和 `hasError()` 都可能为 `true`。业务代码应把 `error()`、`errorString()` 和位置一起记录。

## 11. 逐项 API 说明

### 成员类型

#### `enum QXmlStreamReader::Error`

解析错误类型：`NoError`、`UnexpectedElementError`、`CustomError`、`NotWellFormedError`、`PrematureEndOfDocumentError`。枚举值的实际数值应使用枚举名，不要依赖数值硬编码。

#### `enum QXmlStreamReader::ReadElementTextBehaviour`

`ErrorOnUnexpectedElement`、`IncludeChildElements`、`SkipChildElements`，控制 `readElementText()` 遇到嵌套元素时的策略。

#### `enum QXmlStreamReader::TokenType`

`NoToken`、`Invalid`、`StartDocument`、`EndDocument`、`StartElement`、`EndElement`、`Characters`、`Comment`、`DTD`、`EntityReference`、`ProcessingInstruction`。

### 属性

#### `namespaceProcessing : bool`

读取或设置命名空间处理开关，默认开启。关闭后按原始 qualified name 使用 XML，适合非标准片段；开启后优先使用解析后的 namespace URI 与 local name。

### 构造、输入和重置

#### `QXmlStreamReader::QXmlStreamReader()`

构造一个尚未绑定输入的 reader。之后可用 `setDevice()` 或 `addData()` 提供输入。

#### `[explicit] QXmlStreamReader::QXmlStreamReader(QAnyStringView data)`

用字符串视图初始化内存输入。适合已有一段完整或初始 XML 的场景；不要把它当作可增量追加的 device。

#### `[explicit] QXmlStreamReader::QXmlStreamReader(QIODevice *device)`

绑定非拥有的 `QIODevice`。设备的打开状态、读权限和生命周期由调用方负责。

#### `[explicit] QXmlStreamReader::QXmlStreamReader(const QByteArray &data)`

用 `QByteArray` 初始化内存输入，适合一次性解析已有 XML 数据。

#### `QXmlStreamReader::~QXmlStreamReader()`

销毁 reader，不销毁外部 `QIODevice` 或 `QXmlStreamEntityResolver`。

#### `void QXmlStreamReader::setDevice(QIODevice *device)`

设置当前设备并把 reader 重置到初始状态。设备指针不转移所有权；调用后此前 token、位置、错误和输入状态不再保留。

#### `QIODevice *QXmlStreamReader::device() const`

返回当前绑定的设备指针；没有设备时返回 `nullptr`。

#### `void QXmlStreamReader::addData(QAnyStringView data)`

向无设备的 reader 追加 XML 数据，常用于网络分块或多次读取。已有 `QIODevice` 时无效。追加新数据后，`PrematureEndOfDocumentError` 可以恢复。

#### `void QXmlStreamReader::addData(const QByteArray &data)`

`addData(QAnyStringView)` 的 `QByteArray` 重载，适合直接追加 `readAll()` 或网络 chunk。

#### `void QXmlStreamReader::clear()`

清空 reader 的解析状态、错误和当前输入状态，使其回到初始状态。它不会替代重新设置设备；需要新输入时通常配合 `setDevice()` 或随后 `addData()`。

### 读取和状态

#### `bool QXmlStreamReader::atEnd() const`

返回是否不能再读取。正常文档结束和错误结束都可能为 `true`，因此必须与 `hasError()` 一起判断。

#### `QXmlStreamReader::TokenType QXmlStreamReader::readNext()`

读取并返回下一个 token。正常结束返回 `EndDocument`；终止性错误后返回 `Invalid`。`PrematureEndOfDocumentError` 是例外，追加数据或设备出现更多数据后可以继续。

#### `bool QXmlStreamReader::readNextStartElement()`

在当前元素范围内读到下一个开始元素时返回 `true`；遇到当前元素结束或错误返回 `false`。它简化了按元素递归解析。

#### `void QXmlStreamReader::skipCurrentElement()`

从当前开始元素跳到匹配的结束元素，忽略所有子节点。适合忽略未知扩展元素。

#### `[since 6.10] QString QXmlStreamReader::readRawInnerData()`

读取当前元素内部的原始 XML 内容，包括嵌套标签、文本、注释、处理指令、CDATA 等，并在成功后把当前 token 推进到对应 `EndElement`。DTD 中定义的实体在解析阶段已展开为普通文本，只有五个预定义 XML 实体会在返回文本中重新转义。只应在当前元素尚未结束时使用。

#### `QXmlStreamReader::TokenType QXmlStreamReader::tokenType() const`

返回当前 token 类型。reader 尚未读取时是 `NoToken`，错误状态通常是 `Invalid`。

#### `QString QXmlStreamReader::tokenString() const`

把当前 token 表示为字符串，主要用于调试、日志和诊断。它不是适合业务判断的稳定协议值，业务判断应使用 `tokenType()`。

#### `void QXmlStreamReader::setNamespaceProcessing(bool)`

开启或关闭命名空间解析。默认值为 `true`；应在开始解析前设置，避免同一文档前后采用两套名称语义。

#### `bool QXmlStreamReader::namespaceProcessing() const`

返回当前命名空间解析开关。

### 当前文档信息和位置

#### `bool QXmlStreamReader::isStartDocument() const`

当前 token 是否为 `StartDocument`。

#### `bool QXmlStreamReader::isEndDocument() const`

当前 token 是否为 `EndDocument`。

#### `bool QXmlStreamReader::isStartElement() const`

当前 token 是否为 `StartElement`。

#### `bool QXmlStreamReader::isEndElement() const`

当前 token 是否为 `EndElement`。

#### `bool QXmlStreamReader::isCharacters() const`

当前 token 是否为 `Characters`。

#### `bool QXmlStreamReader::isWhitespace() const`

当前 `Characters` token 是否全部由 XML 空白字符组成。常用于忽略元素之间的缩进换行；只有在 `Characters` token 上使用才有实际意义。

#### `bool QXmlStreamReader::isCDATA() const`

当前 `Characters` token 是否来自 CDATA 段。CDATA 的内容仍可通过 `text()` 读取，但该 API 可用于区分原始表示形式。

#### `bool QXmlStreamReader::isComment() const`

当前 token 是否为 `Comment`。

#### `bool QXmlStreamReader::isDTD() const`

当前 token 是否为 `DTD`。

#### `bool QXmlStreamReader::isEntityReference() const`

当前 token 是否为 `EntityReference`。

#### `bool QXmlStreamReader::isProcessingInstruction() const`

当前 token 是否为 `ProcessingInstruction`。

#### `bool QXmlStreamReader::isStandaloneDocument() const`

当前文档声明是否带有 `standalone="yes"`。通常在 `StartDocument` token 上查询。

#### `[since 6.6] bool QXmlStreamReader::hasStandaloneDeclaration() const`

返回 XML 声明是否明确提供了 standalone 属性。它和 `isStandaloneDocument()` 不同：后者表示值是否为 `yes`，前者表示该属性是否存在。未声明时，`isStandaloneDocument()` 为 `false`，不能据此断言文档明确声明了 `no`。

#### `QStringView QXmlStreamReader::documentVersion() const`

返回 `StartDocument` token 中的 XML 版本字符串。XML 1.0 reader 不接受 XML 1.1 文档。

#### `QStringView QXmlStreamReader::documentEncoding() const`

返回 XML 声明中的编码名称。对于无 XML 声明的输入，不要把空 view 当成业务编码结论。

#### `qint64 QXmlStreamReader::lineNumber() const`

返回当前行号，从 1 开始。

#### `qint64 QXmlStreamReader::columnNumber() const`

返回当前列号，用于诊断当前 token 或错误位置。

#### `qint64 QXmlStreamReader::characterOffset() const`

返回当前字符偏移。它是字符位置语义，不等同于 UTF-8 `QByteArray` 的字节下标。

### 当前元素、属性和文本

#### `QXmlStreamAttributes QXmlStreamReader::attributes() const`

当前 token 是 `StartElement` 时返回该元素的属性列表；其它 token 返回空列表。属性列表是值类型容器，可使用 `value()`、`hasAttribute()` 或遍历查询。命名空间声明不属于普通属性列表，应使用 `namespaceDeclarations()`。

#### `QStringView QXmlStreamReader::name() const`

返回当前开始元素、结束元素或实体引用的 local name。开启命名空间处理后，它不包含 prefix。

#### `QStringView QXmlStreamReader::namespaceUri() const`

返回当前开始元素或结束元素的解析后 namespace URI。未声明或关闭 namespace processing 时可能为空。

#### `QStringView QXmlStreamReader::qualifiedName() const`

返回输入中出现的原始 qualified name，也就是可包含 prefix 的名称。命名空间合规业务不应依赖它，因为同一 prefix 可指向不同 URI。

#### `QStringView QXmlStreamReader::prefix() const`

返回当前开始元素或结束元素的 prefix。

#### `QStringView QXmlStreamReader::text() const`

返回当前 `Characters`、`Comment`、`DTD` 或 `EntityReference` token 的文本。结果是 `QStringView`，需要跨越后续读取保存时调用 `.toString()`。

#### `QString QXmlStreamReader::readElementText(QXmlStreamReader::ReadElementTextBehaviour behaviour = ErrorOnUnexpectedElement)`

在当前开始元素内读取文本直到匹配结束元素。默认遇到子元素时报 `UnexpectedElementError`；另外两种行为分别包含或跳过子元素。当前 token 不是开始元素时返回空字符串。

### 命名空间、DTD 和实体

#### `QXmlStreamNamespaceDeclarations QXmlStreamReader::namespaceDeclarations() const`

当前 token 是 `StartElement` 时返回该元素直接出现的命名空间声明，否则返回空列表。返回类型是 `QList<QXmlStreamNamespaceDeclaration>`。

#### `void QXmlStreamReader::addExtraNamespaceDeclaration(const QXmlStreamNamespaceDeclaration &extraNamespaceDeclaration)`

为后续解析增加一条外部命名空间上下文，不修改原始输入。适合 XML 片段脱离原文档根元素后单独解析的情况。

#### `void QXmlStreamReader::addExtraNamespaceDeclarations(const QXmlStreamNamespaceDeclarations &extraNamespaceDeclarations)`

批量增加额外命名空间声明。

#### `QXmlStreamNotationDeclarations QXmlStreamReader::notationDeclarations() const`

当前 token 是 `DTD` 时返回 notation 声明，否则返回空列表。

#### `QXmlStreamEntityDeclarations QXmlStreamReader::entityDeclarations() const`

当前 token 是 `DTD` 时返回实体声明，否则返回空列表。外部 parsed entity 不会被 reader 处理成可验证的外部资源。

#### `QStringView QXmlStreamReader::dtdName() const`

返回当前 DTD 的名称，通常在 `DTD` token 上查询。

#### `QStringView QXmlStreamReader::dtdPublicId() const`

返回当前 DTD 的 public identifier。

#### `QStringView QXmlStreamReader::dtdSystemId() const`

返回当前 DTD 的 system identifier。

#### `int QXmlStreamReader::entityExpansionLimit() const`

返回单个实体允许展开的最大字符数，默认 4096。

#### `void QXmlStreamReader::setEntityExpansionLimit(int limit)`

设置单个实体的展开上限。输入超过上限会被视为非良构；该参数应结合输入可信度和实际协议需求设置。

#### `void QXmlStreamReader::setEntityResolver(QXmlStreamEntityResolver *resolver)`

设置非拥有的实体解析器。resolver 必须比 reader 活得更久，或在销毁前先解绑。

#### `QXmlStreamEntityResolver *QXmlStreamReader::entityResolver() const`

返回当前实体解析器指针；没有设置时返回 `nullptr`。

### 错误

#### `void QXmlStreamReader::raiseError(const QString &message = QString())`

主动设置 `CustomError`，可附带业务错误消息。它不抛异常；之后应停止按成功路径继续消费，除非重新初始化 reader。

#### `QString QXmlStreamReader::errorString() const`

返回人类可读的错误描述。日志中通常应和 `lineNumber()`、`columnNumber()`、`characterOffset()` 一起记录。

#### `QXmlStreamReader::Error QXmlStreamReader::error() const`

返回当前错误枚举。`NoError` 表示没有错误。

#### `bool QXmlStreamReader::hasError() const`

等价于 `error() != NoError`。它是判断循环是否以错误结束的关键 API。

## API 速查表

| 类别 | API | 作用 | 使用边界 |
| --- | --- | --- | --- |
| 类型 | `Error` | 表示解析错误状态。 | 仅 `PrematureEndOfDocumentError` 支持等待/追加后恢复。 |
| 类型 | `ReadElementTextBehaviour` | 选择 `readElementText()` 遇到子元素时的行为。 | 默认值会把子元素视为错误。 |
| 类型 | `TokenType` | 表示当前 token 类型。 | 使用枚举名，不依赖数值。 |
| 属性 | `namespaceProcessing` | 开关命名空间解析，默认开启。 | 关闭后优先使用 `qualifiedName()`。 |
| 构造 | `QXmlStreamReader()` | 创建无输入 reader。 | 之后用 `setDevice()` 或 `addData()`。 |
| 构造 | `QXmlStreamReader(QAnyStringView)` | 从字符串视图初始化输入。 | 输入与异步生命周期要清楚。 |
| 构造 | `QXmlStreamReader(QIODevice *)` | 从设备读取。 | reader 不拥有设备。 |
| 构造 | `QXmlStreamReader(const QByteArray &)` | 从字节数组读取。 | 适合已有内存数据。 |
| 生命周期 | `~QXmlStreamReader()` | 销毁 reader。 | 不销毁外部设备和 resolver。 |
| 输入 | `addData(QAnyStringView)` | 追加 XML 分块。 | 已有 device 时无效。 |
| 输入 | `addData(const QByteArray &)` | 追加字节数组分块。 | 可恢复 premature end。 |
| 输入 | `setDevice(QIODevice *)` | 设置设备并重置解析状态。 | 会清除当前位置和错误。 |
| 查询 | `device()` | 返回当前设备。 | 可能为 `nullptr`。 |
| 重置 | `clear()` | 清除当前解析状态。 | 新输入仍需重新提供。 |
| 循环 | `atEnd()` | 判断读取是否结束。 | 正常结束和错误结束都可能为真。 |
| 读取 | `readNext()` | 读取下一个 token。 | 终止错误后返回 `Invalid`。 |
| 读取 | `readNextStartElement()` | 读取当前元素内下一个开始元素。 | 结束元素或错误返回 `false`。 |
| 读取 | `skipCurrentElement()` | 跳过当前元素及子节点。 | 应在 `StartElement` 上使用。 |
| 读取 | `readRawInnerData()` | 取得当前元素的原始内部 XML。 | Qt 6.10；成功后位于对应结束元素。 |
| 当前状态 | `tokenType()` | 返回当前 token 类型。 | 初始为 `NoToken`。 |
| 当前状态 | `tokenString()` | 返回当前 token 的字符串表示。 | 主要用于诊断。 |
| 判断 | `isStartDocument()` | 判断是否为文档开始。 | 当前 token 语义。 |
| 判断 | `isEndDocument()` | 判断是否为文档结束。 | 当前 token 语义。 |
| 判断 | `isStartElement()` | 判断是否为开始元素。 | 属性和命名空间声明依赖它。 |
| 判断 | `isEndElement()` | 判断是否为结束元素。 | 元素栈回退依赖它。 |
| 判断 | `isCharacters()` | 判断是否为文本 token。 | 再看 `isWhitespace()`、`isCDATA()`。 |
| 判断 | `isWhitespace()` | 判断文本是否全为空白。 | 只对 `Characters` 有意义。 |
| 判断 | `isCDATA()` | 判断文本是否来自 CDATA。 | 内容仍由 `text()` 读取。 |
| 判断 | `isComment()` | 判断是否为注释。 | 文本由 `text()` 返回。 |
| 判断 | `isDTD()` | 判断是否为 DTD。 | DTD 信息 API 依赖它。 |
| 判断 | `isEntityReference()` | 判断是否为实体引用。 | 名称看 `name()`，文本看 `text()`。 |
| 判断 | `isProcessingInstruction()` | 判断是否为处理指令。 | 目标和数据分别查询。 |
| 文档 | `isStandaloneDocument()` | 返回 standalone 值是否为 yes。 | 不等于“属性存在”。 |
| 文档 | `hasStandaloneDeclaration()` | 判断 XML 声明是否写了 standalone。 | Qt 6.6 起。 |
| 文档 | `documentVersion()` | 返回 XML 声明版本。 | Reader 只支持 XML 1.0。 |
| 文档 | `documentEncoding()` | 返回声明中的编码名。 | 返回 `QStringView`。 |
| 位置 | `lineNumber()` | 返回行号。 | 从 1 开始。 |
| 位置 | `columnNumber()` | 返回列号。 | 用于诊断。 |
| 位置 | `characterOffset()` | 返回字符偏移。 | 不等于 UTF-8 字节偏移。 |
| 元素 | `attributes()` | 返回当前开始元素属性。 | 其它 token 返回空列表。 |
| 元素 | `name()` | 返回 local name。 | 命名空间开启时不含 prefix。 |
| 元素 | `namespaceUri()` | 返回解析后的 URI。 | 仅开始/结束元素有意义。 |
| 元素 | `qualifiedName()` | 返回原始带前缀名。 | 命名空间业务不应依赖 prefix。 |
| 元素 | `prefix()` | 返回元素 prefix。 | 仅开始/结束元素有意义。 |
| 元素 | `text()` | 返回当前文本类 token 的内容。 | `QStringView` 生命周期短。 |
| 元素 | `readElementText()` | 读取当前元素内文本。 | 当前 token 必须是开始元素。 |
| 命名空间 | `namespaceDeclarations()` | 返回当前元素直接声明的 namespace。 | 仅 `StartElement` 有意义。 |
| 命名空间 | `addExtraNamespaceDeclaration()` | 增加一条外部 namespace 上下文。 | 不修改输入文本。 |
| 命名空间 | `addExtraNamespaceDeclarations()` | 批量增加外部 namespace 上下文。 | 片段解析常用。 |
| DTD | `notationDeclarations()` | 返回 DTD notation 声明。 | 非 DTD token 返回空。 |
| DTD | `entityDeclarations()` | 返回 DTD 实体声明。 | 非 DTD token 返回空。 |
| DTD | `dtdName()` | 返回 DTD 名称。 | 当前 DTD 上使用。 |
| DTD | `dtdPublicId()` | 返回 DTD public ID。 | 当前 DTD 上使用。 |
| DTD | `dtdSystemId()` | 返回 DTD system ID。 | 当前 DTD 上使用。 |
| 实体 | `entityExpansionLimit()` | 查询实体展开上限。 | 默认 4096。 |
| 实体 | `setEntityExpansionLimit(int)` | 设置实体展开上限。 | 兼顾 DoS 风险和协议需求。 |
| 实体 | `setEntityResolver(QXmlStreamEntityResolver *)` | 设置实体解析器。 | 非拥有指针，需保证生命周期。 |
| 实体 | `entityResolver()` | 返回实体解析器。 | 可能为 `nullptr`。 |
| 错误 | `raiseError()` | 报告自定义错误。 | 不抛异常，进入错误状态。 |
| 错误 | `errorString()` | 返回错误说明。 | 配合位置记录。 |
| 错误 | `error()` | 返回错误枚举。 | `NoError` 表示成功。 |
| 错误 | `hasError()` | 判断是否有错误。 | 必须与 `atEnd()` 区分。 |

### 一句话总结

`QXmlStreamReader` 是面向大数据和流式输入的 XML 1.0 pull parser：用 `readNext()` 驱动 token，用 `readNextStartElement()` 和递归函数组织结构，用 `hasError()` 区分正常结束、暂时结束和真正失败，并始终尊重 `QStringView`、设备指针、resolver 指针及实体展开限制的生命周期与安全边界。
