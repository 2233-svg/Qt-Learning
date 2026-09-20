# QDomElement
> Qt 6.11.1 · Qt XML · 来自 `QDomElement`

## 1. 先建立直觉

`QDomElement` 表示 XML 标签元素，例如 `<book id="1">Title</book>` 里的 `book`。它是 DOM 中最常用的节点类型：有标签名、属性、子节点、文本内容，也能按标签名查找后代元素。

如果 `QDomNode` 是通用树节点，`QDomElement` 就是“标签 + 属性 + 子内容”的专用接口。

## 2. 类说明

保留类说明：这些 API 来自 `QDomElement`，属于 Qt XML 模块，用于操作 XML 元素节点及其属性。

元素应通过 `QDomDocument::createElement()` 或 `createElementNS()` 创建，然后插入到文档树中。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `tagName()` / `setTagName()` | 读取或修改标签名。 |
| `attribute(name, default)` | 读取属性字符串，不存在时返回默认值。 |
| `setAttribute(name, value)` | 设置普通属性，支持多种数值重载。 |
| `removeAttribute(name)` | 删除属性。 |
| `hasAttribute(name)` | 判断属性是否存在。 |
| `attributeNode(name)` | 获取属性节点 `QDomAttr`。 |
| `setAttributeNode(attr)` / `removeAttributeNode(attr)` | 用属性节点设置或移除属性。 |
| `attributeNS()`、`setAttributeNS()`、`removeAttributeNS()` | 命名空间属性操作。 |
| `attributeNodeNS()`、`setAttributeNodeNS()` | 命名空间属性节点操作。 |
| `hasAttributeNS()` | 判断命名空间属性是否存在。 |
| `text()` | 返回元素及其后代文本拼接。 |
| `elementsByTagName()` / `elementsByTagNameNS()` | 查找后代元素列表。 |
| `nodeType()` | 返回 `ElementNode`。 |

## 4. 典型流程

```cpp
QDomElement book = doc.createElement("book");
book.setAttribute("id", 42);
book.appendChild(doc.createTextNode("Designing with Qt"));
root.appendChild(book);
```

读取：

```cpp
QDomElement book = node.toElement();
const int id = book.attribute("id").toInt();
const QString title = book.text();
```

命名空间：

```cpp
QDomElement e = doc.createElementNS("urn:demo", "d:item");
e.setAttributeNS("urn:demo", "d:id", "42");
```

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 读取配置节点 | 检查 `tagName()`，读取属性和文本。 |
| 构造 XML 输出 | createElement + setAttribute + appendChild。 |
| 处理命名空间 XML | 使用 NS 版本 API，不只看冒号前缀。 |
| 查找子结构 | 小文档可用 `elementsByTagName()`，大/复杂文档手动遍历更可控。 |

## 6. 常见坑与经验

`attribute()` 不区分“不存在”和“存在但为空字符串”，除非你先用 `hasAttribute()` 判断。需要严格校验配置时不要只读默认值。

`text()` 会拼接后代文本，不只是一层直接文本。对混合内容 XML（文本夹元素）要小心，它可能比你想象的更“宽”。

命名空间不能靠字符串切冒号处理。前缀可以变，namespace URI 才是语义身份；解析时要启用 namespace processing。

`elementsByTagName()` 返回所有后代，不只是直接子元素。只想遍历直接子节点时，用 `firstChild()`/`nextSibling()` 并判断元素。

## 7. 知识点覆盖

- XML 元素、标签名、属性和文本内容。
- 普通属性与命名空间属性。
- 直接子节点与后代元素查询。
- XML 构造、读取和业务校验。
