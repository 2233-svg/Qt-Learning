# Qt XML（下）：QDomDocument 节点树、命名空间与安全

`QDomDocument` 把整个 XML 文档加载为 DOM（Document Object Model）节点树。它可以随机查找、插入、删除和重排节点，代码直观；代价是内存通常远高于源文件大小，并且大文档解析和遍历更慢。

选择原则：需要顺序读写时用 `QXmlStreamReader/Writer`；需要保留并修改小型文档结构时用 DOM。

## 1. CMake 配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core Xml)

target_link_libraries(mytarget PRIVATE
    Qt6::Core
    Qt6::Xml
)
```

```cpp
#include <QDomDocument>
#include <QDomElement>
#include <QDomNodeList>
```

## 2. 解析文档与错误定位

Qt 6.5 以后，`setContent()` 返回 `QDomDocument::ParseResult`：

```cpp
QFile file("catalog.xml");
if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    return;

QDomDocument document;
const QDomDocument::ParseResult result = document.setContent(&file);

if (!result) {
    qWarning() << "XML parse error:"
               << result.errorMessage
               << "line" << result.errorLine
               << "column" << result.errorColumn;
    return;
}
```

旧代码常使用 `bool setContent(..., &message, &line, &column)` 重载。新代码优先保存 `ParseResult`，错误信息更集中。

## 3. 根节点和子元素遍历

```cpp
const QDomElement root = document.documentElement();
if (root.tagName() != "catalog") {
    qWarning() << "Unexpected root element:" << root.tagName();
    return;
}

for (QDomElement book = root.firstChildElement("book");
     !book.isNull();
     book = book.nextSiblingElement("book")) {
    const QString id = book.attribute("id");
    const QString title = book.firstChildElement("title").text();
    qDebug() << id << title;
}
```

`firstChildElement()` 跳过注释和空白文本节点，比 `firstChild()` 更适合只关心元素的业务代码。

## 4. 节点类型与转换

所有 DOM 节点都可以用 `QDomNode` 表示，再转换为具体类型：

```cpp
for (QDomNode node = root.firstChild();
     !node.isNull();
     node = node.nextSibling()) {
    if (node.isElement()) {
        const QDomElement element = node.toElement();
        qDebug() << element.tagName();
    } else if (node.isComment()) {
        qDebug() << "comment:" << node.nodeValue();
    } else if (node.isText()) {
        qDebug() << "text:" << node.nodeValue();
    }
}
```

`toElement()` 转换失败会返回空元素，不会抛异常。调用 `tagName()` 前可用 `isNull()` 或 `isElement()` 检查。

## 5. 创建文档

```cpp
QDomDocument document("catalog");

QDomElement root = document.createElement("catalog");
root.setAttribute("version", 1);
document.appendChild(root);

QDomElement book = document.createElement("book");
book.setAttribute("id", "qt6");

QDomElement title = document.createElement("title");
title.appendChild(document.createTextNode("Qt 6 Guide"));

book.appendChild(title);
root.appendChild(book);
```

节点必须由目标 `QDomDocument` 创建。不要从另一个文档直接追加节点；跨文档需要 `importNode()` 或重新创建。

## 6. 修改、替换和删除

```cpp
QDomElement title = book.firstChildElement("title");
if (!title.isNull()) {
    while (!title.firstChild().isNull())
        title.removeChild(title.firstChild());
    title.appendChild(document.createTextNode("Modern Qt Guide"));
}

QDomElement obsolete = book.firstChildElement("obsolete");
if (!obsolete.isNull())
    book.removeChild(obsolete);
```

`QDomElement::text()` 读取所有后代文本，但没有对应的简单 `setText()`。更新时删除旧文本子节点并追加新节点，或封装辅助函数。

替换节点：

```cpp
QDomElement replacement = document.createElement("name");
replacement.appendChild(document.createTextNode("Qt 6 Guide"));
book.replaceChild(replacement, title);
```

## 7. `QDomDocumentFragment` 批量插入

文档片段可以暂存多个节点，再一次插入到目标位置：

```cpp
QDomDocumentFragment fragment = document.createDocumentFragment();

for (const Book &value : books) {
    QDomElement element = document.createElement("book");
    element.setAttribute("id", value.id);
    fragment.appendChild(element);
}

root.appendChild(fragment);
```

追加 fragment 后，其子节点被移动到目标父节点，fragment 自身不会出现在输出 XML 中。

## 8. 查找节点

```cpp
const QDomNodeList books = root.elementsByTagName("book");
for (qsizetype i = 0; i < books.count(); ++i) {
    const QDomElement book = books.at(i).toElement();
    qDebug() << book.attribute("id");
}
```

`elementsByTagName()` 会递归查找所有后代，而不只是直接子元素。结构较大时可能返回意外的嵌套结果；只查直接孩子时使用 sibling 遍历。

频繁按 ID 查找时，应在业务层构建哈希索引，不要反复扫描整棵 DOM。

## 9. 命名空间

### 9.1 为什么前缀不是身份

以下两个元素语义相同：

```xml
<a:item xmlns:a="urn:example:catalog"/>
<b:item xmlns:b="urn:example:catalog"/>
```

元素身份由命名空间 URI `urn:example:catalog` 和本地名 `item` 组成，前缀 `a`/`b` 只是文档中的别名。

### 9.2 启用命名空间解析

```cpp
QDomDocument document;
const auto result = document.setContent(
    &file,
    QDomDocument::ParseOption::UseNamespaceProcessing);

if (!result)
    return;

const QDomNodeList items = document.elementsByTagNameNS(
    "urn:example:catalog", "item");
```

不启用 namespace processing 时，`tagName()` 可能保留带前缀名称，`namespaceURI()` 和 `localName()` 无法按预期使用。

### 9.3 创建带命名空间节点

```cpp
QDomElement item = document.createElementNS(
    "urn:example:catalog", "c:item");
item.setAttributeNS("urn:example:meta", "m:id", "42");
root.appendChild(item);
```

命名空间声明和前缀应保持一致。业务比较使用 URI 和 local name，不要把 `c:item` 整体作为稳定键。

## 10. 空白文本节点

Qt 6.5 默认移除只包含空白的文本节点。若编辑器需要尽量保留原始排版，可启用：

```cpp
const auto options =
    QDomDocument::ParseOption::UseNamespaceProcessing |
    QDomDocument::ParseOption::PreserveSpacingOnlyNodes;

const auto result = document.setContent(&file, options);
```

即便保留空白，重新序列化也不保证字节级一致：属性顺序、实体表示和声明格式可能变化。DOM 适合保持语义，不适合无损 XML 编辑。

## 11. 隐式共享与节点句柄

Qt DOM 类是轻量句柄，多个 `QDomNode` 可能指向同一底层树。复制节点变量不等于深拷贝：

```cpp
QDomElement a = root.firstChildElement("book");
QDomElement b = a;
b.setAttribute("state", "updated");
// a 看到同一个底层节点的修改
```

需要独立节点时使用 `cloneNode(true)`，再插入合适文档；跨文档还需 `importNode()`。

不要让节点句柄活得比其 `QDomDocument` 更久。虽然实现可能通过共享数据延长部分存储寿命，工程上仍应把文档作为节点树的明确拥有者。

## 12. 序列化和原子保存

```cpp
QSaveFile file("catalog.xml");
if (!file.open(QIODevice::WriteOnly | QIODevice::Text))
    return false;

QTextStream stream(&file);
document.save(stream, 2);

if (stream.status() != QTextStream::Ok)
    return false;

return file.commit();
```

缩进值 `2` 只影响可读性。保存后如格式是外部协议，可再用 reader 解析一次进行结构验证。

## 13. DOM 的性能边界

DOM 会为元素、属性、文本和关系创建对象，100 MB XML 可能占用数倍内存。以下情况应改用流式解析：

- 文档可能来自用户且大小不可控。
- 只需读取一遍或提取少量字段。
- 需要边下载边解析。
- 记录数量达到数十万。
- 运行在内存有限设备。

若必须用 DOM，先限制输入字节数，再解析；不要解析后才检查大小。

## 14. 不可信 XML 的安全边界

### 14.1 实体和外部资源

不要配置自定义实体解析器去任意读取本地文件或网络 URL。若业务不需要 DTD/实体，拒绝带相关声明的文档，或使用默认不会访问外部资源的受限解析路径。

### 14.2 资源耗尽

为输入建立限制：

- 最大文件字节数。
- 最大元素数量和嵌套深度。
- 单个文本和属性最大长度。
- 解析总耗时或可取消机制。

仅仅“XML 语法合法”不代表可以安全接受。

### 14.3 模式验证

Qt Core/Qt XML 不提供完整的 XSD 业务验证管线。需要 XML Schema 时可使用独立验证组件或第三方库，并把验证错误映射为明确的业务错误。无论是否有 XSD，关键字段仍应在程序中做范围和语义校验。

## 15. DOM 与 Stream 的组合

可以用 `QXmlStreamReader` 扫描大文档，仅对一个小子树构建 `QDomDocument`；也可用 DOM 修改模板，再用 stream writer 生成大量重复记录。组合时明确编码、命名空间和节点边界，避免先转字符串造成额外内存复制。

## 16. 工程检查表

1. 小且需随机修改的文档才使用 DOM。
2. 检查 `ParseResult` 的消息、行号和列号。
3. 用 `firstChildElement` 避免误处理空白节点。
4. 节点由正确的 `QDomDocument` 创建或导入。
5. 命名空间比较 URI，而不是前缀。
6. 保存使用 `QSaveFile`，并检查流状态和 commit。
7. 不可信输入在解析前限制大小，解析中限制复杂度。
8. 不依赖 DOM 序列化保持原始字节格式。

掌握流式 API 与 DOM 的选择边界，比记住每个节点函数更重要：数据规模、修改需求和安全约束决定了正确工具。
