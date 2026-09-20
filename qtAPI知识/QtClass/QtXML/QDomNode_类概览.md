# QDomNode 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDomNode>`  
> 所属模块：`Qt6::Xml`  
> 继承：无

## 它解决什么问题

`QDomNode` 是 Qt DOM 树里所有节点的通用访问句柄。元素、属性、文本、注释、CDATA、文档、DTD、实体引用等具体类型都可以先作为 `QDomNode` 处理，再根据节点类型转换成更具体的类。

它解决的是“在不知道节点具体类型时，仍然能遍历、改动、序列化 XML 树”的问题。解析 XML 后，你通常会从 `QDomDocument` 取出一个根节点或子节点，然后用 `firstChild()`、`nextSibling()` 这类 API 遍历；遇到元素节点时再 `toElement()`，遇到文本节点时再 `toText()`。

`QDomNode` 不是 `QObject`，也不拥有独立生命周期。它是指向 `QDomDocument` 内部 DOM 数据的轻量值对象。复制一个节点不会复制 XML 子树，而是让两个 `QDomNode` 句柄指向同一份底层数据；修改其中一个，另一个也能看到变化。要做独立拷贝，使用 `cloneNode(true)`。

## 最小使用路径

```cpp
#include <QDomDocument>
#include <QDomElement>
#include <QDomNode>

QDomDocument document;
const auto parsed = document.setContent("<ui><widget name=\"main\"/></ui>");
if (!parsed)
    return;

for (QDomNode node = document.documentElement().firstChild();
     !node.isNull();
     node = node.nextSibling()) {
    if (!node.isElement())
        continue;

    QDomElement element = node.toElement();
    qDebug() << element.tagName() << element.attribute("name");
}
```

这段代码体现了 `QDomNode` 的典型角色：先用通用节点 API 遍历树，再用 `isElement()` 和 `toElement()` 进入元素专用 API。

## 核心模型

### 空节点

默认构造的 `QDomNode` 是空节点。很多查询失败也会返回空节点，例如没有子节点、类型转换不匹配、插入失败。对返回节点继续操作前，应先用 `isNull()` 判断。

`clear()` 会把当前句柄变成空节点。它不是“清空 XML 文件”的工具，而是让这个句柄不再引用原来的 DOM 节点。

### 浅复制和深复制

拷贝构造、赋值和大多数返回值都只是复制句柄。`firstChild()` 返回的节点没有被克隆，修改它就是修改文档树里的真实子节点。只有 `cloneNode()` 才会创建新的节点数据。

```cpp
QDomNode original = document.documentElement().firstChild();
QDomNode alias = original;
alias.toElement().setAttribute("dirty", true); // original 指向的同一节点也被修改

QDomNode copy = original.cloneNode(true);       // copy 是独立子树
```

### 插入不是复制，而是移动

`appendChild()`、`insertBefore()`、`insertAfter()`、`replaceChild()` 会把已有节点重新挂到新位置。如果 `newChild` 原本属于别的父节点，它会被移走；如果已经是当前节点的孩子，则改变它在子节点列表中的位置。

`QDomDocumentFragment` 是特殊情况：插入片段时，插入的是片段的孩子们，片段自身会被清空。

## 遍历时怎么选 API

- 想处理所有直接孩子，包括文本、注释、空白文本：用 `firstChild()` 加 `nextSibling()`，或 `childNodes()`。
- 只想处理直接子元素：用 `firstChildElement()` 加 `nextSiblingElement()`。
- 想按名字找第一个直接孩子：用 `namedItem()`。
- 想递归查找后代元素：用 `QDomElement::elementsByTagName()`，它不属于 `QDomNode` 的直接子节点遍历模型。

XML 缩进产生的换行和空格通常会成为文本节点。遍历 UI 文件、配置文件时，如果你发现“第一个孩子不是元素”，大多是因为先遇到了空白文本节点。

## 节点类型与转换

`nodeType()` 给出底层节点类型；`isElement()`、`isText()` 等是更好读的判断函数。判断成功后，再使用对应的 `toElement()`、`toText()` 等转换函数。转换失败不会抛异常，而是返回空的具体类型对象。

`isElement()` 返回 `true` 并不意味着当前 C++ 静态类型已经是 `QDomElement`；它只说明底层节点是元素。要使用元素的属性 API，仍要调用 `toElement()`。

## 命名空间与名字

`nodeName()` 是节点展示层面的名字，具体含义随节点类型变化。元素通常返回标签名，属性返回属性名，文本和注释会返回固定的节点名。

`namespaceURI()`、`localName()`、`prefix()` 只对命名空间感知的元素和属性真正有意义。解析已有 XML 时，如果没有在 `QDomDocument::setContent()` 中启用命名空间处理，这些值可能不是你想要的结构化结果。

`setPrefix()` 只能修改已经拥有命名空间前缀的元素或属性节点，不能给一个普通无命名空间节点“补上命名空间”。需要命名空间节点时，应从 `QDomDocument::createElementNS()` 或 `createAttributeNS()` 开始创建。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 成员类型 | `enum EncodingPolicy` | 控制 `save()` 序列化文档节点时从哪里决定文本编码。 | 只影响文档节点的编码选择；普通子节点序列化通常沿用传入 `QTextStream`。 |
| 枚举值 | `EncodingFromDocument` | 让 `save()` 从文档的 XML 声明推断编码，缺省为 UTF-8。 | Qt 因历史原因把名为 `xml` 的处理指令当作声明处理。 |
| 枚举值 | `EncodingFromTextStream` | 让 `save()` 使用 `QTextStream` 当前编码。 | 适合调用方已经明确控制输出流编码的场景。 |
| 成员类型 | `enum NodeType` | 表示底层 DOM 节点种类。 | 类型值常用于通用遍历；日常代码更常用 `is...()` 加 `to...()`。 |
| 枚举值 | `ElementNode` | 元素节点，例如 `<item>`。 | 对应 `QDomElement`。 |
| 枚举值 | `AttributeNode` | 属性节点，例如 `id="1"`。 | 对应 `QDomAttr`；属性通常通过元素 API 管理。 |
| 枚举值 | `TextNode` | 普通文本节点。 | XML 缩进空白也可能生成文本节点。 |
| 枚举值 | `CDATASectionNode` | CDATA 节点。 | 不会被 `normalize()` 与普通文本节点合并。 |
| 枚举值 | `EntityReferenceNode` | 实体引用节点。 | 对应 `QDomEntityReference`。 |
| 枚举值 | `EntityNode` | DTD 中的实体声明节点。 | 对应 `QDomEntity`，多数应用只读。 |
| 枚举值 | `ProcessingInstructionNode` | 处理指令节点，例如 `<?xml-stylesheet ...?>`。 | 对应 `QDomProcessingInstruction`。 |
| 枚举值 | `CommentNode` | 注释节点。 | 对应 `QDomComment`。 |
| 枚举值 | `DocumentNode` | 整个文档节点。 | 对应 `QDomDocument`。 |
| 枚举值 | `DocumentTypeNode` | 文档类型声明节点。 | 对应 `QDomDocumentType`。 |
| 枚举值 | `DocumentFragmentNode` | 文档片段节点。 | 插入时会展开其子节点。 |
| 枚举值 | `NotationNode` | DTD notation 节点。 | 对应 `QDomNotation`，通常只读。 |
| 枚举值 | `BaseNode` | 普通 `QDomNode` 基础节点类型。 | 不是某个具体 DOM 子类。 |
| 枚举值 | `CharacterDataNode` | 字符数据类节点的基础类型。 | Qt 扩展值，不是标准 DOM 节点种类之一。 |
| 构造 | `QDomNode()` | 构造空节点句柄。 | 空节点没有类型或内容，修改操作通常无效。 |
| 构造 | `QDomNode(const QDomNode &node)` | 复制节点句柄。 | 浅复制，共享底层节点。 |
| 析构 | `~QDomNode()` | 销毁当前句柄。 | 不等于删除文档树里的节点；DOM 数据由文档和共享引用管理。 |
| 赋值 | `operator=(const QDomNode &other)` | 让当前句柄指向另一个节点。 | 浅赋值；不会复制子树。 |
| 比较 | `operator==(const QDomNode &other)` | 判断两个句柄是否指向同一底层节点。 | 不是比较 XML 文本内容是否相同。 |
| 比较 | `operator!=(const QDomNode &other)` | 判断两个句柄是否不是同一底层节点。 | 两个内容相同但来自不同树的节点通常也不相等。 |
| 子节点编辑 | `appendChild(const QDomNode &newChild)` | 把节点追加为最后一个孩子。 | 会移动已有节点；文档节点已有根元素时不能再追加第二个元素根。 |
| 子节点编辑 | `insertBefore(const QDomNode &newChild, const QDomNode &refChild)` | 在直接孩子 `refChild` 前插入节点。 | `refChild` 为空时插到最前；`refChild` 必须是当前节点的直接孩子。 |
| 子节点编辑 | `insertAfter(const QDomNode &newChild, const QDomNode &refChild)` | 在直接孩子 `refChild` 后插入节点。 | `refChild` 为空时追加到最后。 |
| 子节点编辑 | `replaceChild(const QDomNode &newChild, const QDomNode &oldChild)` | 用新节点替换直接孩子 `oldChild`。 | 返回被替换节点；`newChild` 若是文档片段，会用片段孩子替换。 |
| 子节点编辑 | `removeChild(const QDomNode &oldChild)` | 从当前节点移除直接孩子。 | 只接受直接孩子；成功时返回被移除节点，失败返回空节点。 |
| 子节点状态 | `hasChildNodes() const` | 判断是否至少有一个子节点。 | 子节点可能是文本、注释、空白，不一定是元素。 |
| 子树复制 | `cloneNode(bool deep = true) const` | 创建独立的节点副本。 | `deep=false` 只复制节点本身，不复制子节点；`deep=true` 递归复制子树。 |
| 文本整理 | `normalize()` | 合并相邻的普通 `QDomText` 子节点。 | 不合并 `QDomCDATASection`；常用于整理多次拼接后的文本节点。 |
| 功能查询 | `isSupported(const QString &feature, const QString &version) const` | 查询实现是否支持某个 DOM 功能和版本。 | 多数业务代码很少需要；不要用它代替节点类型判断。 |
| 名称 | `nodeName() const` | 返回节点名称。 | 含义随类型变化；元素是标签名，属性是属性名，文本类节点常是固定名称。 |
| 类型 | `nodeType() const` | 返回 `NodeType`。 | 通用调试和分派时有用。 |
| 父节点 | `parentNode() const` | 返回父节点。 | 无父节点时返回空节点；属性节点通常不按普通父子树遍历。 |
| 子节点列表 | `childNodes() const` | 返回全部直接子节点列表。 | 列表中的节点不是副本，修改会影响文档树。 |
| 子节点 | `firstChild() const` | 返回第一个直接子节点。 | 没有孩子时返回空节点。 |
| 子节点 | `lastChild() const` | 返回最后一个直接子节点。 | 返回句柄仍指向树中真实节点。 |
| 兄弟节点 | `previousSibling() const` | 返回前一个兄弟节点。 | 可能是文本或注释，不一定是元素。 |
| 兄弟节点 | `nextSibling() const` | 返回后一个兄弟节点。 | 遍历元素时常改用 `nextSiblingElement()`。 |
| 属性集合 | `attributes() const` | 返回节点属性映射。 | 只有元素节点真正提供属性；修改映射会影响元素属性。 |
| 所属文档 | `ownerDocument() const` | 返回节点所属的 `QDomDocument`。 | 创建新子节点时最好从同一文档创建，避免跨文档混用。 |
| 命名空间 | `namespaceURI() const` | 返回节点命名空间 URI。 | 无命名空间时为空；解析时需启用命名空间处理。 |
| 命名空间 | `localName() const` | 返回去掉前缀后的本地名。 | 只有命名空间节点才有意义；否则返回空字符串。 |
| 属性状态 | `hasAttributes() const` | 判断节点是否有属性。 | 通常只对元素节点为真。 |
| 值 | `nodeValue() const` | 返回节点值。 | 文本、注释、CDATA、属性等有值；元素和文档等通常返回空字符串。 |
| 值 | `setNodeValue(const QString &value)` | 设置节点值。 | 只对有节点值的类型有实际意义；元素文本应操作文本子节点或用元素 API。 |
| 命名空间 | `prefix() const` | 返回命名空间前缀。 | 前缀不是命名空间身份；身份应看 URI。 |
| 命名空间 | `setPrefix(const QString &pre)` | 修改已有命名空间节点的前缀。 | 不能给无命名空间节点新增前缀；只适用于元素和属性节点。 |
| 类型判断 | `isAttr() const` | 判断底层节点是否是属性。 | 为真后用 `toAttr()` 取得属性对象。 |
| 类型判断 | `isCDATASection() const` | 判断是否是 CDATA 节点。 | 为真后用 `toCDATASection()`。 |
| 类型判断 | `isDocumentFragment() const` | 判断是否是文档片段。 | 插入片段时行为与普通节点不同。 |
| 类型判断 | `isDocument() const` | 判断是否是文档节点。 | 为真后用 `toDocument()`。 |
| 类型判断 | `isDocumentType() const` | 判断是否是 DTD 文档类型节点。 | 为真后用 `toDocumentType()`。 |
| 类型判断 | `isElement() const` | 判断是否是元素节点。 | 为真后仍需 `toElement()` 才能使用元素 API。 |
| 类型判断 | `isEntityReference() const` | 判断是否是实体引用节点。 | 为真后用 `toEntityReference()`。 |
| 类型判断 | `isText() const` | 判断是否是普通文本节点。 | 缩进空白也常是文本节点。 |
| 类型判断 | `isEntity() const` | 判断是否是实体声明节点。 | 常见于 DTD 相关读取。 |
| 类型判断 | `isNotation() const` | 判断是否是 notation 节点。 | 常见于 DTD 相关读取。 |
| 类型判断 | `isProcessingInstruction() const` | 判断是否是处理指令节点。 | 为真后用 `toProcessingInstruction()`。 |
| 类型判断 | `isCharacterData() const` | 判断是否是字符数据类节点。 | 文本、注释、CDATA 等都属于字符数据方向。 |
| 类型判断 | `isComment() const` | 判断是否是注释节点。 | 为真后用 `toComment()`。 |
| 查找 | `namedItem(const QString &name) const` | 返回第一个 `nodeName()` 等于指定名称的直接子节点。 | 不是递归查找；也不专门筛选元素。 |
| 空状态 | `isNull() const` | 判断句柄是否为空。 | 查询失败、转换失败、默认构造都会得到空节点。 |
| 空状态 | `clear()` | 把当前句柄转为空节点。 | 只是清除当前引用，不是删除整棵 DOM 文档。 |
| 类型转换 | `toAttr() const` | 转为 `QDomAttr`。 | 类型不匹配时返回空属性。 |
| 类型转换 | `toCDATASection() const` | 转为 `QDomCDATASection`。 | 类型不匹配时返回空对象。 |
| 类型转换 | `toDocumentFragment() const` | 转为 `QDomDocumentFragment`。 | 类型不匹配时返回空片段。 |
| 类型转换 | `toDocument() const` | 转为 `QDomDocument`。 | 类型不匹配时返回空文档。 |
| 类型转换 | `toDocumentType() const` | 转为 `QDomDocumentType`。 | 类型不匹配时返回空对象。 |
| 类型转换 | `toElement() const` | 转为 `QDomElement`。 | 最常用的转换；先判断 `isElement()` 可让代码更清楚。 |
| 类型转换 | `toEntityReference() const` | 转为 `QDomEntityReference`。 | 类型不匹配时返回空对象。 |
| 类型转换 | `toText() const` | 转为 `QDomText`。 | 只匹配普通文本节点，不等同于元素的 `text()`。 |
| 类型转换 | `toEntity() const` | 转为 `QDomEntity`。 | 多用于 DTD 实体声明读取。 |
| 类型转换 | `toNotation() const` | 转为 `QDomNotation`。 | 多用于 DTD notation 读取。 |
| 类型转换 | `toProcessingInstruction() const` | 转为 `QDomProcessingInstruction`。 | 可读取或修改处理指令数据。 |
| 类型转换 | `toCharacterData() const` | 转为 `QDomCharacterData`。 | 适合统一处理文本、注释、CDATA 一类数据节点。 |
| 类型转换 | `toComment() const` | 转为 `QDomComment`。 | 类型不匹配时返回空注释。 |
| 序列化 | `save(QTextStream &stream, int indent, EncodingPolicy encodingPolicy = EncodingFromDocument) const` | 把当前节点及其子节点写成 XML。 | 文档含非法 XML 字符或目标编码无法表示的字符时行为未定义；编码策略主要影响文档节点。 |
| 元素遍历 | `firstChildElement(const QString &tagName = {}, const QString &namespaceURI = {}) const` | 返回第一个匹配的直接子元素。 | 两个过滤参数都空时返回第一个子元素；找不到时返回空元素。 |
| 元素遍历 | `lastChildElement(const QString &tagName = {}, const QString &namespaceURI = {}) const` | 返回最后一个匹配的直接子元素。 | 只查直接孩子，不递归。 |
| 元素遍历 | `previousSiblingElement(const QString &tagName = {}, const QString &namespaceURI = {}) const` | 返回前一个匹配的兄弟元素。 | 会跳过非元素兄弟节点。 |
| 元素遍历 | `nextSiblingElement(const QString &tagName = {}, const QString &namespaceURI = {}) const` | 返回后一个匹配的兄弟元素。 | 遍历同级元素时比 `nextSibling()` 更顺手。 |
| 定位 | `lineNumber() const` | 返回解析得到该节点时所在的行号。 | 只有来自 `QDomDocument::setContent()` 的节点才有值；其他节点返回 `-1`。 |
| 定位 | `columnNumber() const` | 返回解析得到该节点时所在的列号。 | 手动创建或克隆出的节点通常返回 `-1`。 |
| 非成员 | `operator<<(QTextStream &stream, const QDomNode &node)` | 将节点 XML 表示写入文本流。 | 适合快速输出；需要缩进和编码策略时使用 `save()` 更明确。 |

## 易错点

1. `QDomNode a = b;` 不是复制 XML 子树。它只是又拿了一个指向同一节点的句柄。
2. `appendChild(existingNode)` 会把原节点从旧父节点移动过来，不会留下原位置副本。
3. 遍历 XML 时经常遇到空白文本节点。只关心元素时优先用 `firstChildElement()`、`nextSiblingElement()`。
4. `operator==` 比较的是是否同一个底层节点，不是 XML 内容是否一样。
5. `setPrefix()` 不能给普通节点强行添加命名空间；命名空间应在创建或解析阶段正确建立。

### 一句话总结

`QDomNode` 是 Qt DOM 的通用节点句柄：用它遍历和改动树，用类型判断进入具体节点类，并牢记复制、返回值和比较都围绕“同一个底层节点引用”工作。
