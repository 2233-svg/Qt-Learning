# QDomDocument
> Qt 6.11.1 · Qt XML · 来自 `QDomDocument`

## 1. 先建立直觉

`QDomDocument` 是一整份 XML 文档的 DOM 树。它既负责把 XML 解析成节点树，也负责创建新节点、导入外部节点、找到根元素，并把树重新输出成字符串或字节数组。

DOM 的特点是“整棵树在内存里”。这让随机访问、修改节点很方便，但不适合超大 XML。大文件、流式导入、只扫一遍的场景，应优先考虑 `QXmlStreamReader`，而不是把全部内容放进 `QDomDocument`。

## 2. 类说明

保留类说明：这些 API 来自 `QDomDocument`，属于 Qt XML 模块，用于表示、解析、创建和序列化 XML DOM 文档。

`QDomDocument` 继承 `QDomNode`，但它是文档级节点：根元素由 `documentElement()` 返回，节点创建应通过文档的工厂函数完成，跨文档移动节点时要用 `importNode()`。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QDomDocument(name)` | 创建空 DOM 文档，可指定文档类型名称。 |
| `setContent(...)` | 从字符串、字节数组、设备或 `QXmlStreamReader` 解析 XML。 |
| `ParseResult` | Qt 6.5 起返回解析成功状态、错误文本、行号、列号。 |
| `ParseOption::UseNamespaceProcessing` | 解析时填充 prefix/localName/namespaceURI。 |
| `ParseOption::PreserveSpacingOnlyNodes` | 保留只包含空白的文本节点。 |
| `documentElement()` | 返回根元素。 |
| `doctype()` | 返回文档类型节点。 |
| `implementation()` | 返回 DOM implementation，用于创建 doctype 等。 |
| `createElement()` / `createElementNS()` | 创建元素节点。 |
| `createAttribute()` / `createAttributeNS()` | 创建属性节点。 |
| `createTextNode()` | 创建普通文本节点。 |
| `createCDATASection()` | 创建 CDATA 节点。 |
| `createComment()` | 创建注释节点。 |
| `createProcessingInstruction()` | 创建处理指令节点。 |
| `createDocumentFragment()` | 创建文档片段。 |
| `createEntityReference()` | 创建实体引用节点。 |
| `elementsByTagName()` / `elementsByTagNameNS()` | 全文查找元素列表。 |
| `elementById()` | 按 ID 查找元素，依赖文档 ID 信息。 |
| `importNode(node, deep)` | 把另一个文档的节点复制到当前文档。 |
| `toString(indent)` / `toByteArray(indent)` | 序列化 DOM 树。 |
| `nodeType()` | 对文档节点返回 `DocumentNode`。 |

## 4. 典型流程

```cpp
QDomDocument doc;
auto result = doc.setContent(xmlBytes, QDomDocument::ParseOption::UseNamespaceProcessing);
if (!result) {
    qWarning() << result.errorMessage << result.errorLine << result.errorColumn;
    return;
}

QDomElement root = doc.documentElement();
QDomElement item = doc.createElement("item");
item.setAttribute("id", "42");
item.appendChild(doc.createTextNode("hello"));
root.appendChild(item);
```

输出：

```cpp
QByteArray xml = doc.toByteArray(2);
```

## 5. 使用场景

| 场景 | 为什么适合 |
| --- | --- |
| 配置文件体量较小且结构复杂 | DOM 便于按节点增删改查。 |
| 需要修改后重新保存 XML | 节点工厂和序列化 API 完整。 |
| 需要跨节点随机访问 | 比流式解析更直接。 |
| 构造 XML 文档 | 通过 create 系列函数保证节点归属同一文档。 |

## 6. 常见坑与经验

跨文档节点不能直接随便 append。一个节点属于创建它的 document；要放入另一个 document，先 `importNode()`，否则会遇到空节点、失败或结构不符合预期。

命名空间默认不处理。需要 `prefix()`、`localName()`、`namespaceURI()` 有意义时，解析时必须启用 `UseNamespaceProcessing`，创建时也要使用 `createElementNS()`、`setAttributeNS()`。

只检查解析成功还不够。还要检查根元素名称、版本、必需属性和业务约束。XML 格式正确不代表语义正确。

DOM 会保留树结构和许多节点对象。对不可信或很大的 XML，要考虑内存、实体展开、输入限制和超时策略。

## 7. 知识点覆盖

- DOM 文档树、根元素、文档类型。
- XML 解析结果、命名空间和空白节点策略。
- 文档工厂函数、节点归属和 `importNode()`。
- DOM 修改和序列化。
- DOM 与流式 XML 解析的取舍。
