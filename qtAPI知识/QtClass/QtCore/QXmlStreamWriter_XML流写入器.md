# Qt QXmlStreamWriter 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QXmlStreamWriter>`  
> 所属模块：`Qt6::Core`  
> 线程属性：所有函数可重入；一个 writer 不应被多个线程同时修改  
> 定位：XML 1.0 流式写入器

## 1. 它解决什么问题

`QXmlStreamWriter` 用一组与 XML token 对应的成员函数，把结构化数据连续写入 `QIODevice`、`QByteArray` 或 `QString`。它负责 XML 标签、属性、命名空间、字符转义和部分格式化细节，调用方只需要按正确的文档顺序发出写入操作。

它适合：

- 生成配置文件、项目文件和导出文件；
- 将数据库或业务对象逐条写成 XML，避免先构造完整 DOM；
- 把 `QXmlStreamReader` 读取到的 token 链接到另一个输出；
- 向文件、内存缓冲区、压缩/网络设备等 `QIODevice` 连续输出。

它不是 DOM builder，也不会为你维护一棵可随机修改的 XML 树。调用顺序本身就是结构约束：先开始元素，再写属性和命名空间，随后写内容，最后关闭元素。

Writer 遵循 XML 1.0 的语法、转义和字符合法性规则，并且始终使用 UTF-8 编码。XML 1.1 不受支持；`writeStartDocument()` 虽然允许手工传入其它版本字符串，但这不会改变实际的 XML 1.0 转义和字符约束。

## 2. 输出目标、所有权与生命周期

### 2.1 输出到 `QIODevice`

```cpp
QFile file("bookmarks.xml");
if (!file.open(QIODevice::WriteOnly | QIODevice::Truncate)) {
    return;
}

QXmlStreamWriter xml(&file);
xml.setAutoFormatting(true);
xml.writeStartDocument();
xml.writeStartElement("bookmarks");
xml.writeTextElement("title", "Qt Project");
xml.writeEndElement();
xml.writeEndDocument();

if (xml.hasError()) {
    qWarning().noquote() << xml.errorString();
}
```

writer 只保存外部 `QIODevice *`，不拥有、不开启也不关闭设备。设备必须在整个写入过程有效，并且具有可写状态。设备的 I/O 错误会进入 writer 的错误状态；调用方仍应检查设备自身的错误信息和 writer 的 `hasError()`。

### 2.2 输出到 `QByteArray` 或 `QString`

```cpp
QByteArray bytes;
QXmlStreamWriter byteWriter(&bytes);
byteWriter.writeStartDocument();
byteWriter.writeTextElement("message", "hello");
byteWriter.writeEndDocument();

QString string;
QXmlStreamWriter stringWriter(&string);
stringWriter.writeStartElement("root");
stringWriter.writeCharacters("a < b");
stringWriter.writeEndElement();
```

这两个构造函数把输出写入调用方提供的对象。writer 不接管对象所有权，对象必须活到 writer 不再使用为止。需要注意：

- `QByteArray *` 和 `QString *` 不能是 `nullptr`；
- 输出目标必须保持有效，不能在 writer 使用期间移动、销毁或替换；
- 这类目标适合一次性生成内存 XML，不适合无限增长的网络流；
- 写入结束后，读取目标对象即可获得内容，不需要从 writer 再导出。

也可以先默认构造，再用 `setDevice()` 绑定 `QIODevice`。切换设备前应先完成或放弃当前文档；writer 不会把旧目标中的未闭合结构迁移到新目标。

## 3. 最小写入模型

```cpp
QByteArray output;
QXmlStreamWriter xml(&output);

xml.writeStartDocument();
xml.writeStartElement("book");
xml.writeAttribute("id", "42");
xml.writeTextElement("title", "Qt");
xml.writeEndElement();
xml.writeEndDocument();

if (xml.hasError()) {
    // output 可能已经包含部分内容，不能把它当作完整 XML 使用
}
```

最重要的调用顺序是：

1. 可选：`writeStartDocument()`；
2. `writeStartElement()` 或 `writeEmptyElement()`；
3. 紧跟着写 `writeAttribute()`、`writeAttributes()` 和命名空间声明；
4. 写字符、CDATA、实体引用或嵌套元素；
5. 对普通开始元素调用 `writeEndElement()`；
6. 最后调用 `writeEndDocument()`。

`writeEndDocument()` 会关闭所有仍然打开的元素并写出换行，因此它可以兜底收尾，但不应掩盖业务代码中元素层级不清的问题。

## 4. 元素、属性与内容边界

### 4.1 属性只能紧跟开始元素

```cpp
xml.writeStartElement("item");
xml.writeAttribute("id", "42");
xml.writeAttribute("kind", "note");
xml.writeCharacters("content");
xml.writeEndElement();
```

`writeAttribute()` 和 `writeAttributes()` 只能在开始元素已经写出、元素内容尚未开始时调用。属性不是普通内容，以下顺序是错误的：

```cpp
xml.writeStartElement("item");
xml.writeCharacters("content");
xml.writeAttribute("id", "42"); // 太晚
```

`writeEmptyElement()` 也允许随后追加属性。它表达一个空元素的开始，writer 会在后续结构确定时输出自闭合形式；不要把它当成已经完全结束、无法再添加属性的字符串写入操作。

### 4.2 普通开始元素与空元素

```cpp
xml.writeStartElement("parent");
xml.writeEmptyElement("child");
xml.writeAttribute("enabled", "true");
xml.writeEndElement();
```

`writeStartElement()` 开启一个需要内容或结束标签的元素，后续用 `writeEndElement()` 关闭。`writeEmptyElement()` 用于没有子内容的元素，后续仍可补属性；如果元素需要内容，应使用普通开始元素。

### 4.3 `writeTextElement()`

`writeTextElement()` 是便捷函数，等价于：

```cpp
xml.writeStartElement("title");
xml.writeCharacters("A < B");
xml.writeEndElement();
```

它只适合终端文本元素。需要属性、CDATA、实体引用或嵌套元素时，应拆开调用。

## 5. 命名空间

### 5.1 使用 URI 重载

```cpp
constexpr QAnyStringView ns = "https://example.com/book";

xml.writeStartElement(ns, "book");
xml.writeAttribute(ns, "id", "42");
xml.writeTextElement(ns, "title", "Qt");
xml.writeEndElement();
```

使用 `(namespaceUri, name)` 重载时，writer 根据 URI 选择或生成 prefix；如果该 URI 尚未声明，它会自动写出命名空间声明。业务代码因此应优先传 namespace URI，而不是自行拼接 prefix。

属性与元素有一个重要 XML 边界：默认命名空间只影响元素，不影响无 prefix 的属性。需要让属性属于某个命名空间，应使用带 URI 的 `writeAttribute(namespaceUri, name, value)`，writer 会使用合适的 prefix。

### 5.2 `writeNamespace()` 和 `writeDefaultNamespace()`

```cpp
xml.writeStartElement("book");
xml.writeNamespace("https://example.com/book", "bk");
xml.writeDefaultNamespace("https://example.com/default");
```

如果已经调用了 `writeStartElement()` 或 `writeEmptyElement()`，声明作用于当前元素；否则作用于下一个子元素。显式声明适合协议要求固定 prefix 的场景。

`writeNamespace(uri, prefix)` 的规则：

- prefix 为空时，writer 自动生成唯一 prefix，形如 `n0`、`n1`；
- `xml` 是保留 prefix，只能绑定 `http://www.w3.org/XML/1998/namespace`；
- `xmlns` 及其命名空间 URI `http://www.w3.org/2000/xmlns/` 属于命名空间机制本身，不能作为普通声明使用。

`writeDefaultNamespace(uri)` 写默认命名空间。XML 规范规定 `xml` 和 `xmlns` 对应的保留命名空间不能作为默认命名空间。

### 5.3 qualified name 重载

```cpp
xml.writeStartElement("bk:book");
xml.writeAttribute("bk:id", "42");
```

传入 qualified name 的重载直接使用调用方给出的原始名称，绕过 writer 的 URI 到 prefix 解析。它适合必须保留既有 prefix 的输出，但 writer 不会因为看到 `bk:` 就替你验证或声明 `bk` 的 URI。需要命名空间一致性时，优先使用 URI 重载并显式声明需要的 prefix。

## 6. 字符、CDATA、注释和处理指令

### 6.1 `writeCharacters()`

`writeCharacters()` 写普通文本并自动转义 XML 特殊字符。至少需要关注：

- `<` 写成 `&lt;`；
- `&` 写成 `&amp;`；
- `"` 写成 `&quot;`；
- 为避免形成禁止的 `]]>` 序列，`>` 也可能被写成 `&gt;`。

因此，业务字符串不要手工预先写成 `&lt;`，否则 `&` 会再次被转义为 `&amp;lt;`。把原始文本交给 writer 是正确做法。

### 6.2 `writeCDATA()`

`writeCDATA()` 输出 CDATA 段，适合希望保留大量 `<`、`&` 文本表示形式的场景。但 XML 不允许 CDATA 内容直接包含 `]]>`。writer 会把该序列拆分成多个 CDATA 段，使最终 XML 保持合法。

CDATA 仍然受到 XML 1.0 字符合法性限制；它不是绕过非法控制字符检查的通道。

### 6.3 注释与处理指令

```cpp
xml.writeComment("generated file");
xml.writeProcessingInstruction("xml-stylesheet",
                               "type=\"text/xsl\" href=\"style.xsl\"");
```

`writeComment()` 的文本不能包含 `--`，也不能以 `-` 结尾；XML 没有可用于转义注释中连字符的机制，调用方必须在写入前修正内容。

`writeProcessingInstruction()` 的 data 不能包含 `?>`。target 和 data 应符合 XML 处理指令语法；writer 不会把任意字符串变成合法的处理指令。

### 6.4 实体引用

`writeEntityReference(name)` 原样写出 `&name;`。它不会检查该实体是否在 DTD 中声明，也不会把它当普通文本自动转义。要写用户输入中的 `&name;` 字面量，应使用 `writeCharacters()`。

## 7. 文档声明、DTD 和 token 链接

### 7.1 文档声明

```cpp
xml.writeStartDocument();                 // <?xml version="1.0"?>
xml.writeStartDocument("1.0", true);      // 带 standalone="yes"
xml.writeEndDocument();
```

无参数重载写出版本 `1.0`。版本重载允许调用方提供版本字符串，但不会验证，也不会让 writer 获得 XML 1.1 能力。实际输出应保持声明、内容和解析器能力一致，通常直接使用 `"1.0"`。

`standalone` 参数控制 XML 声明中的 standalone 属性。它描述文档是否依赖外部声明，不等于是否使用了命名空间。

### 7.2 `writeDTD()`

`writeDTD()` 的参数应是 XML 1.0 规范中完整的 `doctypedecl`，而不是只传一个根元素名称或任意内部片段。DTD 内容的合法性和与文档主体的匹配由调用方负责。

### 7.3 `writeCurrentToken()`

`writeCurrentToken(reader)` 把 `QXmlStreamReader` 当前 token 写到输出，支持把一个 XML 流链到另一个 XML 流。例如可以读取源设备、过滤部分 token 后写入目标设备。它处理所有有效 token 状态；业务代码仍需保证 reader 当前 token 和输出文档上下文兼容。

## 8. 自动格式化

`autoFormatting` 默认关闭。开启后，writer 会在元素之间的空白区域自动插入换行和缩进，以提高人工可读性。它添加的是可忽略空白，不应依赖其具体换行位置作为数据协议。

`autoFormattingIndent` 的默认值为 `4`：

- 正数表示每层使用对应数量的空格；
- 负数表示每层使用对应数量的 tab，绝对值表示 tab 数；
- 只有开启 `autoFormatting` 后，这个设置才会影响输出。

如果 XML 内容本身包含混合文本，自动格式化不会把它变成适合人工阅读的 DOM 排版；格式化空白可能改变某些对空白敏感的消费方语义，因此要根据协议决定是否开启。

## 9. Qt 6.10 错误模型

### 9.1 `Error`

| 枚举值 | 含义 |
| --- | --- |
| `QXmlStreamWriter::Error::None` | 没有错误。 |
| `IO` | 向设备写入时发生 I/O 错误。 |
| `Encoding` | 把字符转换为输出格式时发生编码错误。 |
| `InvalidCharacter` | 遇到 XML 1.0 不允许的字符。 |
| `Custom` | `raiseError()` 主动报告的自定义错误。 |

`Error`、`error()`、`errorString()`、`raiseError()` 从 Qt 6.10 起提供。需要兼容更早 Qt 版本时，不应直接使用这些 API。

### 9.2 `stopWritingOnError`

该属性从 Qt 6.10 起提供，默认值为 `false`：

- `false`：遇到 `Encoding`、`InvalidCharacter` 或 `Custom` 后，writer 可能继续处理后续写入；错误操作之前已经缓冲的数据或同一次操作的部分数据也可能已经写出；
- `true`：第一次错误后立即停止写入，并忽略后续写操作；
- `IO` 错误始终是终止性的，不论该属性取值如何。

实际工程中应把 `hasError()` 视为当前文档不可继续信任的信号。即使选择默认的继续模式，也不应把错误后拼接出来的部分输出当成完整 XML。

`raiseError(message)` 设置自定义错误，不抛 C++ 异常。writer 的错误状态不会自动重置；需要新的独立文档时，重新创建 writer 通常比在错误对象上继续写更清楚。

## 10. 逐项 API 说明

### 成员类型

#### `[since 6.10] enum class QXmlStreamWriter::Error`

表示写入过程中的错误类别：`None`、`IO`、`Encoding`、`InvalidCharacter`、`Custom`。使用枚举名判断，不要依赖底层整数值。

### 属性

#### `autoFormatting : bool`

读取或设置自动换行和缩进。默认关闭；开启后只在元素间可插入的空白区域进行格式化。

#### `autoFormattingIndent : int`

读取或设置每级缩进宽度。默认 `4`；正数为空格数，负数为 tab 数。它只影响开启了 `autoFormatting` 的输出。

#### `[since 6.10] stopWritingOnError : bool`

读取或设置错误后是否立即停止写入。默认 `false`，但 I/O 错误始终终止。

### 构造、目标与状态

#### `QXmlStreamWriter::QXmlStreamWriter()`

构造未绑定输出目标的 writer。之后可用 `setDevice()` 绑定设备。

#### `[explicit] QXmlStreamWriter::QXmlStreamWriter(QByteArray *array)`

把输出写入外部 `QByteArray`。writer 不拥有该数组，数组在使用期间必须有效。

#### `[explicit] QXmlStreamWriter::QXmlStreamWriter(QIODevice *device)`

把输出写入外部设备。writer 不打开、不关闭、不拥有该设备。

#### `[explicit] QXmlStreamWriter::QXmlStreamWriter(QString *string)`

把输出写入外部 `QString`。writer 不拥有该字符串，字符串在使用期间必须有效。

#### `QXmlStreamWriter::~QXmlStreamWriter()`

销毁 writer，不销毁外部输出设备、字节数组或字符串。析构不会替代显式的 `writeEndDocument()`；需要完整 XML 时应主动收尾并检查错误。

#### `void QXmlStreamWriter::setDevice(QIODevice *device)`

设置当前输出设备。设备指针不转移所有权；切换设备时不应假设当前元素栈能安全迁移到新目标。

#### `QIODevice *QXmlStreamWriter::device() const`

返回当前设备指针。使用 `QByteArray *` 或 `QString *` 构造时，内部目标是 Qt 管理的适配设备，调用方不应依赖其具体实现；没有设备时返回 `nullptr`。

#### `void QXmlStreamWriter::setAutoFormatting(bool enable)`

设置自动格式化开关。

#### `bool QXmlStreamWriter::autoFormatting() const`

返回自动格式化是否启用。

#### `void QXmlStreamWriter::setAutoFormattingIndent(int spacesOrTabs)`

设置缩进宽度。正数使用空格，负数使用 tab，默认值为 `4`。

#### `int QXmlStreamWriter::autoFormattingIndent() const`

返回当前自动格式化缩进设置。

#### `[since 6.10] void QXmlStreamWriter::setStopWritingOnError(bool stop)`

设置错误后是否停止所有后续写入。I/O 错误不受该选项放宽。

#### `[since 6.10] bool QXmlStreamWriter::stopWritingOnError() const`

返回错误后停止写入选项。

### 错误

#### `[since 6.10] QXmlStreamWriter::Error QXmlStreamWriter::error() const`

返回当前错误类别。`None` 表示尚未记录错误。

#### `[since 6.10] QString QXmlStreamWriter::errorString() const`

返回当前错误的人类可读描述。日志中应同时记录输出对象和生成阶段。

#### `bool QXmlStreamWriter::hasError() const`

判断 writer 是否进入错误状态。它不表示输出为空；错误前可能已经有部分合法 XML 写入目标。

#### `[since 6.10] void QXmlStreamWriter::raiseError(QAnyStringView message)`

设置 `Custom` 错误并记录消息。它不抛异常，错误状态不会自动清除。

### 属性和元素

#### `void QXmlStreamWriter::writeAttribute(QAnyStringView namespaceUri, QAnyStringView name, QAnyStringView value)`

在当前开始元素上写入带命名空间 URI 的属性。只能在开始元素后、元素内容前调用；URI 重载会参与 prefix 选择和声明。

#### `void QXmlStreamWriter::writeAttribute(const QXmlStreamAttribute &attribute)`

写入一个 `QXmlStreamAttribute`。仍受“必须处于属性阶段”的调用顺序限制。

#### `void QXmlStreamWriter::writeAttribute(QAnyStringView qualifiedName, QAnyStringView value)`

按调用方给出的 qualified name 写入属性，绕过 URI 到 prefix 的解析。需要固定 prefix 时使用，但声明一致性由调用方负责。

#### `void QXmlStreamWriter::writeAttributes(const QXmlStreamAttributes &attributes)`

批量写入属性列表。列表中的每个属性都必须满足当前元素和命名空间上下文的约束。

#### `void QXmlStreamWriter::writeStartElement(QAnyStringView namespaceUri, QAnyStringView name)`

按 namespace URI 写开始元素；未声明的 URI 会触发自动命名空间声明。

#### `void QXmlStreamWriter::writeStartElement(QAnyStringView qualifiedName)`

按原始 qualified name 写开始元素，不解析其 prefix 与 URI 的对应关系。

#### `void QXmlStreamWriter::writeEmptyElement(QAnyStringView namespaceUri, QAnyStringView name)`

按 namespace URI 写空元素；未声明的 URI 会自动声明。随后仍可写属性。

#### `void QXmlStreamWriter::writeEmptyElement(QAnyStringView qualifiedName)`

按 qualified name 写空元素，绕过 namespace URI 解析。随后仍可写属性。

#### `void QXmlStreamWriter::writeEndElement()`

关闭最近一个开始元素。元素嵌套必须按后进先出顺序结束。

#### `void QXmlStreamWriter::writeTextElement(QAnyStringView namespaceUri, QAnyStringView name, QAnyStringView text)`

写入带 namespace URI 的文本元素，等价于开始元素、`writeCharacters()`、结束元素。

#### `void QXmlStreamWriter::writeTextElement(QAnyStringView qualifiedName, QAnyStringView text)`

写入带 qualified name 的文本元素，等价于对应的开始元素、`writeCharacters()`、结束元素。

### 内容和声明

#### `void QXmlStreamWriter::writeCDATA(QAnyStringView text)`

写 CDATA 内容，并处理其中的 `]]>` 拆分；仍拒绝 XML 1.0 非法字符。

#### `void QXmlStreamWriter::writeCharacters(QAnyStringView text)`

写普通文本并自动进行 XML 转义。传入原始文本，不要提前手工转义。

#### `void QXmlStreamWriter::writeComment(QAnyStringView text)`

写注释。文本不能含 `--`，也不能以 `-` 结尾。

#### `void QXmlStreamWriter::writeEntityReference(QAnyStringView name)`

原样写出 `&name;`。不会替你声明或验证实体。

#### `void QXmlStreamWriter::writeProcessingInstruction(QAnyStringView target, QAnyStringView data = {})`

写处理指令。data 不能包含 `?>`。

#### `void QXmlStreamWriter::writeDTD(QAnyStringView dtd)`

写完整 XML 1.0 `doctypedecl`。DTD 内容的合法性由调用方负责。

#### `void QXmlStreamWriter::writeNamespace(QAnyStringView namespaceUri, QAnyStringView prefix = {})`

为 URI 写命名空间声明。prefix 为空时自动生成唯一 prefix；声明作用于当前元素或下一个子元素。

#### `void QXmlStreamWriter::writeDefaultNamespace(QAnyStringView namespaceUri)`

写默认命名空间声明。默认命名空间只影响元素，不会让无 prefix 属性自动属于该 URI。

#### `void QXmlStreamWriter::writeStartDocument()`

写出 `<?xml version="1.0"?>`。

#### `void QXmlStreamWriter::writeStartDocument(QAnyStringView version)`

写出指定版本字符串。不会验证版本，也不会启用 XML 1.1；实际项目通常传 `"1.0"`。

#### `void QXmlStreamWriter::writeStartDocument(QAnyStringView version, bool standalone)`

写出版本和 standalone 属性。版本字符串仍不改变 writer 的 XML 1.0 语义。

#### `void QXmlStreamWriter::writeEndDocument()`

关闭所有尚未关闭的开始元素并写出换行。调用后应检查 `hasError()`。

#### `void QXmlStreamWriter::writeCurrentToken(const QXmlStreamReader &reader)`

把 reader 当前有效 token 写到输出，适合 XML 流过滤、转发和链式处理。输出上下文仍须满足 XML 结构顺序。

## API 速查表

| 类别 | API | 作用 | 使用边界 |
| --- | --- | --- | --- |
| 类型 | `[since 6.10] Error` | 表示写入错误类别。 | I/O 错误始终终止。 |
| 属性 | `autoFormatting` | 开关自动换行和缩进。 | 默认关闭，只插入可忽略空白。 |
| 属性 | `autoFormattingIndent` | 设置缩进宽度。 | 正数为空格，负数为 tab，默认 4。 |
| 属性 | `[since 6.10] stopWritingOnError` | 控制非 I/O 错误后是否停止。 | 默认 false；I/O 错误不受其放宽。 |
| 构造 | `QXmlStreamWriter()` | 创建未绑定目标的 writer。 | 之后需要 `setDevice()`。 |
| 构造 | `QXmlStreamWriter(QByteArray *)` | 输出到外部字节数组。 | 非拥有，指针必须有效。 |
| 构造 | `QXmlStreamWriter(QIODevice *)` | 输出到外部设备。 | 不打开、不关闭、不拥有设备。 |
| 构造 | `QXmlStreamWriter(QString *)` | 输出到外部字符串。 | 非拥有，指针必须有效。 |
| 生命周期 | `~QXmlStreamWriter()` | 销毁 writer。 | 不替代 `writeEndDocument()`。 |
| 目标 | `setDevice(QIODevice *)` | 设置输出设备。 | 切换前应结束或放弃当前文档。 |
| 目标 | `device()` | 返回当前设备。 | 具体适配设备不应依赖。 |
| 格式 | `setAutoFormatting(bool)` | 设置格式化开关。 | 只影响可插入空白区域。 |
| 格式 | `autoFormatting()` | 查询格式化开关。 | 默认 false。 |
| 格式 | `setAutoFormattingIndent(int)` | 设置缩进宽度。 | 正空格、负 tab。 |
| 格式 | `autoFormattingIndent()` | 查询缩进宽度。 | 默认 4。 |
| 错误 | `[since 6.10] setStopWritingOnError(bool)` | 设置错误后停止选项。 | 错误状态不会因此清除。 |
| 错误 | `[since 6.10] stopWritingOnError()` | 查询错误后停止选项。 | 默认 false。 |
| 错误 | `[since 6.10] error()` | 返回错误枚举。 | `None` 表示没有错误。 |
| 错误 | `[since 6.10] errorString()` | 返回错误描述。 | 配合 `hasError()` 使用。 |
| 错误 | `hasError()` | 判断是否出错。 | 输出可能已有部分数据。 |
| 错误 | `[since 6.10] raiseError()` | 设置自定义错误。 | 不抛异常，状态不会自动重置。 |
| 属性 | `writeAttribute(namespaceUri, name, value)` | 写带 URI 的属性。 | 必须在属性阶段；会参与命名空间处理。 |
| 属性 | `writeAttribute(attribute)` | 写一个属性对象。 | 必须在属性阶段。 |
| 属性 | `writeAttribute(qualifiedName, value)` | 按原始 qualified name 写属性。 | 绕过 URI/prefix 解析。 |
| 属性 | `writeAttributes(attributes)` | 批量写属性。 | 列表内容仍受当前上下文约束。 |
| 元素 | `writeStartElement(namespaceUri, name)` | 写带 URI 的开始元素。 | 未声明 URI 会自动声明。 |
| 元素 | `writeStartElement(qualifiedName)` | 写原始 qualified name 开始元素。 | prefix 声明由调用方保证。 |
| 元素 | `writeEmptyElement(namespaceUri, name)` | 写带 URI 的空元素。 | 随后仍可添加属性。 |
| 元素 | `writeEmptyElement(qualifiedName)` | 写 qualified name 空元素。 | 随后仍可添加属性。 |
| 元素 | `writeEndElement()` | 关闭最近开始元素。 | 必须按嵌套顺序。 |
| 元素 | `writeTextElement(namespaceUri, name, text)` | 写带 URI 的文本元素。 | 等价于 start + characters + end。 |
| 元素 | `writeTextElement(qualifiedName, text)` | 写 qualified name 文本元素。 | 同上，绕过 URI 解析。 |
| 文本 | `writeCharacters(text)` | 写并转义普通文本。 | 传原文，不要预转义。 |
| 文本 | `writeCDATA(text)` | 写 CDATA 内容。 | `]]>` 会被拆分，非法字符仍不允许。 |
| 文本 | `writeEntityReference(name)` | 写 `&name;`。 | 不声明、不验证实体。 |
| 声明 | `writeComment(text)` | 写 XML 注释。 | 禁止 `--` 和尾部 `-`。 |
| 声明 | `writeProcessingInstruction(target, data)` | 写处理指令。 | data 禁止 `?>`。 |
| 声明 | `writeDTD(dtd)` | 写完整 DTD。 | 参数应是完整 `doctypedecl`。 |
| 命名空间 | `writeNamespace(uri, prefix)` | 写普通 namespace 声明。 | 空 prefix 时自动分配；保留 prefix 受限制。 |
| 命名空间 | `writeDefaultNamespace(uri)` | 写默认 namespace 声明。 | 只影响元素，不影响无 prefix 属性。 |
| 文档 | `writeStartDocument()` | 写 XML 1.0 声明。 | 推荐的默认入口。 |
| 文档 | `writeStartDocument(version)` | 写指定版本字符串。 | 不启用 XML 1.1。 |
| 文档 | `writeStartDocument(version, standalone)` | 写版本和 standalone。 | 版本仍需与 XML 1.0 内容一致。 |
| 文档 | `writeEndDocument()` | 关闭剩余元素并写换行。 | 结束后检查错误。 |
| 链接 | `writeCurrentToken(reader)` | 转写 reader 当前 token。 | 需保证输出上下文合法。 |

### 一句话总结

`QXmlStreamWriter` 是按 XML 语法顺序工作的 UTF-8 流式写入器：先元素、再属性和命名空间、再内容、最后结束元素；文本交给 writer 转义，命名空间优先使用 URI，任何错误后都把当前输出视为需要重新验证的部分结果。
