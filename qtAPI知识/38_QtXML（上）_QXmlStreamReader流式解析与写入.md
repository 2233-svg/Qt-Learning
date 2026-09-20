# Qt XML（上）：QXmlStreamReader 流式解析与写入

Qt 处理 XML 有两条主路线：

- `QXmlStreamReader` / `QXmlStreamWriter`：位于 Qt Core，顺序读写、内存小，推荐用于大多数新代码。
- `QDomDocument`：位于 Qt XML，把整份文档构造成可随机访问的节点树，适合小型配置和需要频繁修改结构的场景。

本文先讲流式 API；DOM、命名空间、错误定位和安全边界放在下篇。

## 1. CMake 配置

流式 API 只需要 Qt Core：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

头文件：

```cpp
#include <QXmlStreamReader>
#include <QXmlStreamWriter>
```

只有使用 `QDomDocument` 时才需要 `Qt6::Xml`。

## 2. XML 基础结构

```xml
<?xml version="1.0" encoding="UTF-8"?>
<catalog version="1">
    <book id="qt6">
        <title>Qt 6 Guide</title>
        <price currency="CNY">98.00</price>
    </book>
</catalog>
```

要区分：

- 元素：`<book>...</book>`。
- 属性：`id="qt6"`。
- 文本节点：`Qt 6 Guide`。
- XML 声明、注释、CDATA、处理指令。
- 命名空间 URI 与前缀。

XML 标签区分大小写，且必须正确嵌套。

## 3. 最小流式读取

```cpp
QFile file("catalog.xml");
if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    return;

QXmlStreamReader xml(&file);

while (!xml.atEnd()) {
    xml.readNext();

    if (xml.isStartElement())
        qDebug() << "开始:" << xml.name();
    else if (xml.isCharacters() && !xml.isWhitespace())
        qDebug() << "文本:" << xml.text();
    else if (xml.isEndElement())
        qDebug() << "结束:" << xml.name();
}

if (xml.hasError())
    qWarning() << xml.errorString();
```

`readNext()` 每次前进到下一个 token。`atEnd()` 既可能表示正常文档结束，也可能表示解析错误，所以循环后必须检查 `hasError()`。

## 4. 面向业务结构解析

### 4.1 数据类型

```cpp
struct Book
{
    QString id;
    QString title;
    double price = 0.0;
    QString currency;
};
```

### 4.2 解析单个元素

```cpp
Book readBook(QXmlStreamReader &xml)
{
    Book book;
    book.id = xml.attributes().value("id").toString();

    while (xml.readNextStartElement()) {
        if (xml.name() == u"title") {
            book.title = xml.readElementText();
        } else if (xml.name() == u"price") {
            book.currency =
                xml.attributes().value("currency").toString();

            bool ok = false;
            const QString text = xml.readElementText();
            book.price = QLocale::c().toDouble(text, &ok);
            if (!ok)
                xml.raiseError("Invalid price value");
        } else {
            xml.skipCurrentElement();
        }
    }

    return book;
}
```

`readNextStartElement()` 会跳过空白并在遇到下一个开始元素时返回 `true`。`skipCurrentElement()` 是向前兼容的关键：新版本增加未知元素时，旧程序可以跳过而不是错乱。

### 4.3 解析根元素

```cpp
QList<Book> readCatalog(QIODevice *device)
{
    QXmlStreamReader xml(device);
    QList<Book> books;

    if (!xml.readNextStartElement() || xml.name() != u"catalog") {
        xml.raiseError("Expected <catalog> root element");
        return {};
    }

    while (xml.readNextStartElement()) {
        if (xml.name() == u"book")
            books.append(readBook(xml));
        else
            xml.skipCurrentElement();
    }

    if (xml.hasError()) {
        qWarning() << "XML error at"
                   << xml.lineNumber() << xml.columnNumber()
                   << xml.errorString();
        return {};
    }

    return books;
}
```

解析函数应在失败时返回清晰错误，不能把“空文档”和“合法但没有书籍”都默认为同一个空列表。工程代码可返回 `std::optional`、`std::expected` 或自己的结果结构。

## 5. 属性读取与验证

```cpp
const auto attrs = xml.attributes();
const QStringView id = attrs.value("id");

if (id.isEmpty())
    xml.raiseError("Missing required book id");
```

`value()` 返回视图，通常只在当前 reader 状态有效；需要长期保存时转换为 `QString`。属性存在但值为空与属性缺失可能有不同业务含义，应使用 `hasAttribute()` 区分。

数值解析要检查 `ok`：

```cpp
bool ok = false;
const int version = attrs.value("version").toInt(&ok);
if (!ok || version < 1)
    xml.raiseError("Invalid catalog version");
```

## 6. `readElementText()` 的边界

```xml
<title>Qt <b>Advanced</b> Guide</title>
```

元素包含子元素时，默认 `readElementText()` 可能报告意外子元素。根据数据格式选择行为：

```cpp
const QString text = xml.readElementText(
    QXmlStreamReader::IncludeChildElements);
```

对于结构化 XML，更推荐显式处理子元素，而不是把嵌套标记压平成文本。

## 7. 增量输入和网络数据

`QXmlStreamReader` 可以逐块接收数据：

```cpp
QXmlStreamReader xml;

connect(reply, &QNetworkReply::readyRead, this, [&] {
    xml.addData(reply->readAll());

    while (!xml.atEnd()) {
        const auto token = xml.readNext();
        if (token == QXmlStreamReader::StartElement)
            consumeStartElement(xml);
    }

    if (xml.hasError()
        && xml.error() != QXmlStreamReader::PrematureEndOfDocumentError) {
        abortWithError(xml.errorString());
    }
});
```

数据尚未收完时出现 `PrematureEndOfDocumentError` 不一定是永久错误。新数据到来后继续 `addData()`，解析器可以恢复。网络请求结束时若仍是提前结束，才应判定文档不完整。

## 8. 写入 XML

### 8.1 最小写入

```cpp
QFile file("catalog.xml");
if (!file.open(QIODevice::WriteOnly | QIODevice::Text))
    return;

QXmlStreamWriter xml(&file);
xml.setAutoFormatting(true);
xml.writeStartDocument();
xml.writeStartElement("catalog");
xml.writeAttribute("version", "1");

xml.writeStartElement("book");
xml.writeAttribute("id", "qt6");
xml.writeTextElement("title", "Qt 6 Guide");
xml.writeStartElement("price");
xml.writeAttribute("currency", "CNY");
xml.writeCharacters("98.00");
xml.writeEndElement(); // price
xml.writeEndElement(); // book

xml.writeEndElement(); // catalog
xml.writeEndDocument();
```

Writer 会转义文本和属性中的 `&`、`<`、引号等字符。不要手工拼 XML 字符串，否则容易产生非法转义和注入问题。

### 8.2 写入函数封装

```cpp
void writeBook(QXmlStreamWriter &xml, const Book &book)
{
    xml.writeStartElement("book");
    xml.writeAttribute("id", book.id);
    xml.writeTextElement("title", book.title);

    xml.writeStartElement("price");
    xml.writeAttribute("currency", book.currency);
    xml.writeCharacters(QLocale::c().toString(book.price, 'f', 2));
    xml.writeEndElement();

    xml.writeEndElement();
}
```

持久化协议中的数字应使用 `QLocale::c()`，不要依赖用户区域设置把小数点写成逗号。

## 9. 原子保存

直接覆盖配置文件时，程序崩溃或磁盘写满会留下半个 XML。使用 `QSaveFile`：

```cpp
QSaveFile file("settings.xml");
if (!file.open(QIODevice::WriteOnly | QIODevice::Text))
    return false;

QXmlStreamWriter xml(&file);
writeSettings(xml, settings);

if (xml.hasError())
    return false;

return file.commit();
```

`commit()` 成功后才替换目标文件。还应检查 writer 错误和设备错误，不要只看 `open()`。

## 10. CDATA、注释与处理指令

```cpp
xml.writeComment("Generated file; do not edit manually");
xml.writeCDATA(rawScript);
xml.writeProcessingInstruction("xml-stylesheet",
                               "type=\"text/xsl\" href=\"view.xsl\"");
```

CDATA 不能包含字面量 `]]>`，Writer 会按其能力处理或报错。业务数据通常使用普通 `writeCharacters()` 更简单安全。

## 11. 编码

XML 输出默认使用 UTF-8。`QXmlStreamReader` 会根据 XML 声明或 BOM 识别编码。不要先用错误编码把文件转换为 `QString` 再交给 reader；直接传 `QIODevice` 或原始 `QByteArray`，让解析器处理声明。

## 12. 大文件策略

流式解析的内存主要与当前元素和业务缓存有关，而不是文档总大小。要保持这一优势：

- 读到一条记录就处理或入库，不要全部保存。
- 为文本长度、元素数量和嵌套深度设置业务上限。
- 批量写数据库时按固定数量提交事务。
- 解析中定期检查取消请求。

## 13. 常见错误

### 忘记消费当前元素

分支处理后既不调用 `readElementText()` 也不 `skipCurrentElement()`，循环会停在错误层级。每个开始元素分支都必须明确消费完整元素。

### 混用用户区域格式

XML 协议数字应使用稳定格式；用户界面显示才使用当前 `QLocale`。

### 把空字符串当作所有失败

空元素可能合法。应通过 `hasError()`、必填字段验证和显式结果类型区分。

## 14. 测试清单

1. 正常文档、空集合、单条和多条记录。
2. 缺少必填属性、非法数值和未知元素。
3. 标签未闭合、错误嵌套和截断输入。
4. 非 ASCII 文本、实体转义和 CDATA。
5. 超长文本、深层嵌套和大文件取消。
6. 写入后重新读取，验证语义往返一致。

下一篇将介绍 `QDomDocument` 的节点树操作、命名空间、解析选项、文档修改，以及处理不可信 XML 时的安全与性能限制。
