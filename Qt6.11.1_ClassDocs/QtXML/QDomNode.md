# QDomNode
> Qt 6.11.1 · Qt XML · 来自 `QDomNode`

## 1. 先建立直觉

`QDomNode` 是所有 DOM 节点的通用句柄。元素、文本、注释、属性、文档、文档类型，都可以先当作 `QDomNode` 处理，再通过 `isElement()`、`toElement()` 等函数转成具体类型。

它的核心价值是“树操作”：父子兄弟遍历、插入、替换、删除、克隆、查询节点名和值。

## 2. 类说明

保留类说明：这些 API 来自 `QDomNode`，属于 Qt XML 模块，用于表示 DOM 树中任意节点并提供通用树操作。

`QDomNode` 是隐式共享的值对象式句柄。拷贝节点句柄很便宜，但多个句柄可能指向同一个底层节点；修改其中一个，树结构会随之变化。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `nodeType()` | 返回节点类型，如 ElementNode、TextNode、DocumentNode。 |
| `nodeName()`、`nodeValue()`、`setNodeValue()` | 读取节点名称和值。 |
| `isNull()`、`clear()` | 判断或清空句柄。 |
| `parentNode()`、`ownerDocument()` | 访问父节点和所属文档。 |
| `firstChild()`、`lastChild()`、`childNodes()` | 访问子节点。 |
| `nextSibling()`、`previousSibling()` | 兄弟节点遍历。 |
| `appendChild()`、`insertBefore()`、`insertAfter()` | 插入节点。 |
| `replaceChild()`、`removeChild()` | 替换或移除子节点。 |
| `cloneNode(deep)` | 克隆节点，可选深拷贝子树。 |
| `hasChildNodes()`、`hasAttributes()`、`attributes()` | 查询子节点和属性。 |
| `normalize()` | 合并相邻文本节点，整理文本结构。 |
| `namespaceURI()`、`prefix()`、`localName()` | 命名空间相关名称，需命名空间解析支持。 |
| `setPrefix()` | 设置命名空间前缀。 |
| `toElement()`、`toText()`、`toDocument()` 等 | 安全转换为具体 DOM 类型。 |
| `isElement()`、`isText()`、`isDocument()` 等 | 判断节点具体类型。 |
| `save(QTextStream/QXmlStreamWriter, indent)` | 输出当前节点。 |

## 4. 典型流程

```cpp
for (QDomNode n = root.firstChild(); !n.isNull(); n = n.nextSibling()) {
    if (!n.isElement())
        continue;

    QDomElement e = n.toElement();
    if (e.tagName() == "item")
        handleItem(e);
}
```

修改树：

```cpp
QDomNode oldNode = root.firstChild();
QDomElement replacement = doc.createElement("replacement");
root.replaceChild(replacement, oldNode);
```

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 通用 DOM 遍历 | 用 `nodeType()` 或 `isXxx()` 分派。 |
| 编辑 XML 树结构 | append/insert/replace/remove。 |
| 写 XML 转换工具 | clone/import/normalize/save。 |
| 命名空间文档处理 | localName/namespaceURI/prefix。 |

## 6. 常见坑与经验

`toElement()` 对非元素节点会返回空元素。转换前先 `isElement()`，或者转换后检查 `isNull()`。

文本可能被拆成多个相邻 `QDomText` 节点。需要把元素文本当整体处理时，先理解 `text()` 和 `normalize()` 的差别。

属性节点在 DOM 中很特殊：它们不是普通子节点，通常通过 `QDomElement` 的 attribute API 或 `attributes()` 访问，不要用 childNodes 查属性。

节点插入会改变原树。如果你只是想复制到另一个位置，用 `cloneNode()`；跨文档复制还要通过目标文档 `importNode()`。

## 7. 知识点覆盖

- DOM 通用节点类型和具体节点转换。
- 父子兄弟遍历、树结构增删改。
- 隐式共享句柄和节点归属。
- 命名空间字段、属性和文本节点结构。
- 节点保存、克隆和 normalize。
