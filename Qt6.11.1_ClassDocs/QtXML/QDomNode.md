# QDomNode

> Qt 6.11.1 · Qt XML

## 1. 先建立直觉

**一句话定位：** `QDomNode` 是结构化文档类型，负责 JSON/XML 节点、值、解析状态或流式读写。

**模块背景：** Qt XML 提供 XML 文档和 DOM 风格 XML 数据处理能力。

### 这是什么

`QDomNode` 是 结构化文本解析机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** JSON 通常表示为 value/object/array 树，XML 则包含元素、属性、文本和层级。文档容器负责解析和序列化，具体字段/节点访问由 object、array、value 或 DOM/流式读取对象完成。

**适用场景：** 接收字节数据后显式指定编码和解析选项，检查错误对象，再按类型访问节点，校验业务字段，最后序列化或转换成领域对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要只检查 parse 成功；不要假设字段一定存在且类型固定；不要把用户输入直接当作可信结构；大文件不要无条件 readAll 和构造整棵树。

## 2. 依赖与对象关系

- 头文件：`#include <QDomNode>`
- 继承自：未在类页中列出
- 直接派生类：QDomAttr、QDomCharacterData、QDomDocument、QDomDocumentFragment、QDomDocumentType、QDomElement、QDomEntity、QDomEntityReference、QDomNotation,、QDomProcessingInstruction

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Xml)
target_link_libraries(mytarget PRIVATE Qt6::Xml)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

JSON 通常表示为 value/object/array 树，XML 则包含元素、属性、文本和层级。文档容器负责解析和序列化，具体字段/节点访问由 object、array、value 或 DOM/流式读取对象完成。

### 状态、生命周期和线程

**生命周期：** 解析结果通常是值对象，可在作用域内传递；流式解析器则依赖输入设备和读取顺序。解析错误、结构合法和业务字段合法是三个不同层次，必须分别检查。

**状态与结果：** 先判断文档是否为空、根节点类型和解析错误，再访问字段；字段缺失、类型不匹配、空值和默认值要分开处理。序列化时要明确紧凑/格式化输出和编码。

**线程与事件循环：** 值形式的解析结果可以复制后跨线程处理；共享设备、流对象和可变 DOM 不应无保护地跨线程使用。大文档要评估一次性树结构的内存成本，必要时用流式 API。

## 3. 直接使用

接收字节数据后显式指定编码和解析选项，检查错误对象，再按类型访问节点，校验业务字段，最后序列化或转换成领域对象。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum EncodingPolicy { EncodingFromDocument, EncodingFromTextStream }`
- `enum NodeType { ElementNode, AttributeNode, TextNode, CDATASectionNode, EntityReferenceNode, …, CharacterDataNode }`

### 公有函数

- `QDomNode()`
- `QDomNode(const QDomNode &node)`
- `~QDomNode()`
- `QDomNode appendChild(const QDomNode &newChild)`
- `QDomNamedNodeMap attributes() const`
- `QDomNodeList childNodes() const`
- `void clear()`
- `QDomNode cloneNode(bool deep = true) const`
- `int columnNumber() const`
- `QDomNode firstChild() const`
- `QDomElement firstChildElement(const QString &tagName = QString(), const QString &namespaceURI = QString()) const`
- `bool hasAttributes() const`
- `bool hasChildNodes() const`
- `QDomNode insertAfter(const QDomNode &newChild, const QDomNode &refChild)`
- `QDomNode insertBefore(const QDomNode &newChild, const QDomNode &refChild)`
- `bool isAttr() const`
- `bool isCDATASection() const`
- `bool isCharacterData() const`
- `bool isComment() const`
- `bool isDocument() const`
- `bool isDocumentFragment() const`
- `bool isDocumentType() const`
- `bool isElement() const`
- `bool isEntity() const`
- `bool isEntityReference() const`
- `bool isNotation() const`
- `bool isNull() const`
- `bool isProcessingInstruction() const`
- `bool isSupported(const QString &feature, const QString &version) const`
- `bool isText() const`
- `QDomNode lastChild() const`
- `QDomElement lastChildElement(const QString &tagName = QString(), const QString &namespaceURI = QString()) const`
- `int lineNumber() const`
- `QString localName() const`
- `QDomNode namedItem(const QString &name) const`
- `QString namespaceURI() const`
- `QDomNode nextSibling() const`
- `QDomElement nextSiblingElement(const QString &tagName = QString(), const QString &namespaceURI = QString()) const`
- `QString nodeName() const`
- `QDomNode::NodeType nodeType() const`
- `QString nodeValue() const`
- `void normalize()`
- `QDomDocument ownerDocument() const`
- `QDomNode parentNode() const`
- `QString prefix() const`
- `QDomNode previousSibling() const`
- `QDomElement previousSiblingElement(const QString &tagName = QString(), const QString &namespaceURI = QString()) const`
- `QDomNode removeChild(const QDomNode &oldChild)`
- `QDomNode replaceChild(const QDomNode &newChild, const QDomNode &oldChild)`
- `void save(QTextStream &stream, int indent, QDomNode::EncodingPolicy encodingPolicy = QDomNode::EncodingFromDocument) const`
- `void setNodeValue(const QString &value)`
- `void setPrefix(const QString &pre)`
- `QDomAttr toAttr() const`
- `QDomCDATASection toCDATASection() const`
- `QDomCharacterData toCharacterData() const`
- `QDomComment toComment() const`
- `QDomDocument toDocument() const`
- `QDomDocumentFragment toDocumentFragment() const`
- `QDomDocumentType toDocumentType() const`
- `QDomElement toElement() const`
- `QDomEntity toEntity() const`
- `QDomEntityReference toEntityReference() const`
- `QDomNotation toNotation() const`
- `QDomProcessingInstruction toProcessingInstruction() const`
- `QDomText toText() const`
- `bool operator!=(const QDomNode &other) const`
- `QDomNode & operator=(const QDomNode &other)`
- `bool operator==(const QDomNode &other) const`

### 相关非成员函数

- `QTextStream & operator<<(QTextStream &str, const QDomNode &node)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QDomNode::EncodingPolicy`

**作用与语义：**

该枚举规定了`QDomNode::save()`在序列化时如何决定使用哪种编码方式。
- `QDomNode::EncodingFromDocument`：`1`;编码从文档中获取。
- `QDomNode::EncodingFromTextStream`：`2`;编码从`QTextStream`取出。

### `enum QDomNode::NodeType`

**作用与语义：**

该枚举定义了节点的类型：
- `QDomNode::ElementNode`：`1`
- `QDomNode::AttributeNode`：`2`
- `QDomNode::TextNode`：`3`
- `QDomNode::CDATASectionNode`：`4`
- `QDomNode::EntityReferenceNode`：`5`
- `QDomNode::EntityNode`：`6`
- `QDomNode::ProcessingInstructionNode`：`7`
- `QDomNode::CommentNode`：`8`
- `QDomNode::DocumentNode`：`9`
- `QDomNode::DocumentTypeNode`：`10`
- `QDomNode::DocumentFragmentNode`：`11`
- `QDomNode::NotationNode`：`12`
- `QDomNode::BaseNode`：`21`;一个`QDomNode`对象，即非`QDomNode`子类。
- `QDomNode::CharacterDataNode`：`22`

### `QDomNode::QDomNode()`

**作用与语义：**

构建一个`null`节点。

### `QDomNode::QDomNode(const QDomNode &node)`

**作用与语义：**

构建了`node`的复制品。
复制的数据是共享的（浅层复制）：修改一个节点也会改变另一个节点。如果你想做深度复制，可以用`cloneNode()`。

### `[noexcept] QDomNode::~QDomNode()`

**作用与语义：**

摧毁该物体并释放其资源。

### `QDomNode QDomNode::appendChild(const QDomNode &newChild)`

**作用与语义：**

作为节点的最后一个子节点，`newChild` 附着。
如果`newChild`是另一个节点的子节点，则它会被重新父级到该节点。如果`newChild`是该节点的子节点，那么它在子节点列表中的位置会发生变化。
如果`newChild`是`QDomDocumentFragment`，则该片段的子节点会从片段中移除并附加。
如果`newChild`是`QDomElement`，且该节点是一个`QDomDocument`，且该节点已经有一个元素节点作为子节点，则`newChild`不会被添加为子节点，而是返回一个空节点。
成功时返回新的`newChild`引用，失败时返回空节点。
在空节点（例如用默认构造函数创建）上调用该函数无效，返回空节点。
DOM规范禁止插入属性节点，但出于历史原因，QDom仍然接受它们。

### `QDomNamedNodeMap QDomNode::attributes() const`

**作用与语义：**

返回所有属性的命名节点映射。属性仅为`QDomElement`提供。
更改地图中的属性也会改变该`QDomNode`的属性。

### `QDomNodeList QDomNode::childNodes() const`

**作用与语义：**

返回所有直接子节点的列表。
通常你会调用`QDomElement`对象上的这个函数。
例如，如果XML文档看起来如下：
那么“body”元素的子节点列表将包含由标签创建的节点<h1>和由标签创建的节点<p>。
列表中的节点不会被复制;因此，更改列表中的节点也会改变该节点的子节点。

**官方示例：**

```cpp
 <body>
 <h1>Heading</h1>
 <p>Hello <b>you</b></p>
 </body>
```

### `void QDomNode::clear()`

**作用与语义：**

将该节点转换为空节点;如果之前不是空节点，其类型和内容将被删除。

### `QDomNode QDomNode::cloneNode(bool deep = true) const`

**作用与语义：**

这样可以建立一个深层（而非浅层）的`QDomNode`复制品。
如果`deep`为真，则克隆是递归完成的，这意味着节点的所有子节点也都被深度复制。如果`deep`为假，则只有节点本身被复制，且复制中没有子节点。

### `int QDomNode::columnNumber() const`

**作用与语义：**

对于`QDomDocument::setContent()`创建的节点，该函数返回解析节点所在的XML文档列号。否则返回-1。

### `QDomNode QDomNode::firstChild() const`

**作用与语义：**

返回该节点的第一个子节点。如果没有子节点，则返回一个空节点。更改返回的节点也会改变文档树中的该节点。

### `QDomElement QDomNode::firstChildElement(const QString &tagName = QString(), const QString &namespaceURI = QString()) const`

**作用与语义：**

返回第一个子元素，标签名为`tagName`，命名空间为URI `namespaceURI`。如果`tagName`为空，返回第一个子元素，`namespaceURI`;如果为空，返回第一个子元素，`namespaceURI`返回第一个子元素，`tagName`。如果两个参数均为空，返回第一个子元素。如果不存在空子元素，返回空元素。

### `bool QDomNode::hasAttributes() const`

**作用与语义：**

如果节点有属性，返回`true`;否则返回`false`。

### `bool QDomNode::hasChildNodes() const`

**作用与语义：**

如果节点有一个或多个子节点，返回`true`;否则返回`false`。

### `QDomNode QDomNode::insertAfter(const QDomNode &newChild, const QDomNode &refChild)`

**作用与语义：**

在子节点 `refChild` 之后插入节点 `newChild`。`refChild` 必须是该节点的直接子节点。如果 `refChild` 被`null`，则`newChild` 作为该节点的最后一个子节点被附加。
如果`newChild`是另一个节点的子节点，则它会被重新父级到该节点。如果`newChild`是该节点的子节点，那么它在子节点列表中的位置会发生变化。
如果`newChild`是`QDomDocumentFragment`，则片段的子节点会从片段中移除，并在`refChild`后插入。
成功时返回新的 `newChild` 引用，失败时返回空节点。
DOM规范不允许插入属性节点，但由于历史原因，QDom仍然接受它们。

### `QDomNode QDomNode::insertBefore(const QDomNode &newChild, const QDomNode &refChild)`

**作用与语义：**

在子节点`refChild`之前插入节点 `newChild`。`refChild` 必须是该节点的直接子节点。如果`refChild` 被`null`，则插入`newChild`作为该节点的第一个子节点。
如果`newChild`是另一个节点的子节点，则它会被重新父级到该节点。如果`newChild`是该节点的子节点，那么它在子节点列表中的位置会被改变。
如果`newChild`是`QDomDocumentFragment`，则片段的子节点会从片段中移除，并在`refChild`之前插入。
成功时返回新的 `newChild` 引用，失败时返回空节点。
DOM规范不允许插入属性节点，但由于历史原因，QDom仍然接受它们。

### `bool QDomNode::isAttr() const`

**作用与语义：**

如果节点是属性，则返回 `true`；否则返回 `false`。
如果此函数返回 `true`，则不意味着此对象是 QDomAttribute；你可以使用 toAttribute() 获取 QDomAttribute。

### `bool QDomNode::isCDATASection() const`

**作用与语义：**

如果节点是 CDATA 部分，返回 `true`;否则返回 false。
如果该函数返回`true`，并不意味着该对象是`QDomCDATASection`;你可以用`toCDATASection()`得到`QDomCDATASection`。

### `bool QDomNode::isCharacterData() const`

**作用与语义：**

如果节点是字符数据节点，返回`true`;否则返回`false`。
如果该函数返回`true`，并不意味着该对象是`QDomCharacterData`;你可以用`toCharacterData()`得到`QDomCharacterData`。

### `bool QDomNode::isComment() const`

**作用与语义：**

如果节点是注释，则返回 `true`；否则返回 `false`。如果此函数返回 `true`，并不意味着该对象是 `QDomComment`；您可以使用 `toComment()` 获取 `QDomComment`。

### `bool QDomNode::isDocument() const`

**作用与语义：**

如果节点是文档，则返回 `true`；否则返回 `false`。如果此函数返回 `true`，并不意味着该对象是 `QDomDocument`；您可以使用 `toDocument()` 获取 `QDomDocument`。

### `bool QDomNode::isDocumentFragment() const`

**作用与语义：**

如果节点是文档片段，则返回 `true`；否则返回 false。
如果此函数返回 `true`，并不意味着此对象是 `QDomDocumentFragment`；你可以通过 `toDocumentFragment()` 获取 `QDomDocumentFragment`。

### `bool QDomNode::isDocumentType() const`

**作用与语义：**

如果节点是文档类型，则返回 `true`；否则返回 false。如果此函数返回 `true`，则不意味着该对象是 `QDomDocumentType`；你可以使用 `toDocumentType()` 获取 `QDomDocumentType`。

### `bool QDomNode::isElement() const`

**作用与语义：**

如果节点是元素，则返回 `true`；否则返回 `false`。 如果此函数返回 `true`，并不意味着该对象是 `QDomElement`；您可以使用 `toElement()` 获取 `QDomElement`。

### `bool QDomNode::isEntity() const`

**作用与语义：**

如果节点是实体，则返回 `true`；否则返回 `false`。 如果此函数返回 `true`，并不意味着该对象是 `QDomEntity`；您可以使用 `toEntity()` 获取 `QDomEntity`。

### `bool QDomNode::isEntityReference() const`

**作用与语义：**

如果节点是实体引用，则返回 `true`；否则返回 false。 如果此函数返回 `true`，则不意味着该对象是 `QDomEntityReference`；你可以使用 `toEntityReference()` 获取 `QDomEntityReference`。

### `bool QDomNode::isNotation() const`

**作用与语义：**

如果节点是记号，则返回 `true`；否则返回 `false`。如果此函数返回 `true`，并不意味着该对象是 `QDomNotation`；您可以使用 `toNotation()` 获取 `QDomNotation`。

### `bool QDomNode::isNull() const`

**作用与语义：**

如果该节点为空（即没有类型或内容），返回`true`;否则返回`false`。

### `bool QDomNode::isProcessingInstruction() const`

**作用与语义：**

如果节点是处理指令，则返回 `true`；否则返回 `false`。
如果此函数返回 `true`，并不意味着该对象是 `QDomProcessingInstruction`；你可以通过 `toProcessingInstruction()` 获取 QProcessingInstruction。

### `bool QDomNode::isSupported(const QString &feature, const QString &version) const`

**作用与语义：**

如果DOM实现了该功能`feature`且该节点在版本`version`中支持该功能，则返回`true`;否则返回`false`。

### `bool QDomNode::isText() const`

**作用与语义：**

如果节点是文本节点，则返回 `true`；否则返回 `false`。
如果此函数返回 `true`，并不意味着此对象是 `QDomText`；你可以通过 `toText()` 获取 `QDomText`。

### `QDomNode QDomNode::lastChild() const`

**作用与语义：**

返回该节点的最后一个子节点。如果没有子节点，则返回一个空节点。更改返回的节点也会改变文档树中的该节点。

### `QDomElement QDomNode::lastChildElement(const QString &tagName = QString(), const QString &namespaceURI = QString()) const`

**作用与语义：**

返回标签名为`tagName`的最后一个子元素，命名空间为URI `namespaceURI`。如果`tagName`为空，返回最后一个子元素，`namespaceURI`;如果是空的，返回`namespaceURI`，返回最后一个子元素，`tagName`。如果两个参数均为空，返回最后一个子元素。如果没有空子元素，返回一个空元素。

### `int QDomNode::lineNumber() const`

**作用与语义：**

对于`QDomDocument::setContent()`创建的节点，该函数返回解析节点所在的XML文档行号。否则返回-1。

### `QString QDomNode::localName() const`

**作用与语义：**

如果节点使用命名空间，该函数返回节点的本地名称;否则返回空字符串。
只有类型为`ElementNode`或`AttributeNode`的节点才能拥有命名空间。命名空间必须在创建时被指定;之后无法添加命名空间。

### `QDomNode QDomNode::namedItem(const QString &name) const`

**作用与语义：**

返回第一个 `nodeName()` 等于 `name` 的直接子节点。
如果不存在这样的直接子节点，则返回一个空节点。

### `QString QDomNode::namespaceURI() const`

**作用与语义：**

返回该节点的命名空间URI，或如果没有命名空间URI，则返回空字符串。
只有类型为`ElementNode`或`AttributeNode`的节点才能拥有命名空间。命名空间URI必须在创建时指定，且之后不能更改。

### `QDomNode QDomNode::nextSibling() const`

**作用与语义：**

返回文档树中的下一个兄弟节点。更改返回节点也会改变文档树中的节点。
如果你有类似这样的 XML：
而这个`QDomNode`代表<p>该标签，nextSibling() 将返回代表<h2>该标签的节点。

**官方示例：**

```cpp
 <h1>Heading</h1>
 <p>The text...</p>
 <h2>Next heading</h2>
```

### `QDomElement QDomNode::nextSiblingElement(const QString &tagName = QString(), const QString &namespaceURI = QString()) const`

**作用与语义：**

返回下一个兄弟元素，标签名为`tagName`，命名空间为URI `namespaceURI`。如果`tagName`为空，返回下一个兄弟元素，`namespaceURI`;如果`namespaceURI`为空，返回下一个兄弟子元素，`tagName`。如果两个参数均为空，返回下一个兄弟元素。如果不存在兄弟元素，返回空元素。

### `QString QDomNode::nodeName() const`

**作用与语义：**

返回节点名称。
名称的含义取决于子类：
- `Name`：含义
- `QDomAttr`：属性名称
- `QDomCDATASection`：弦“#cdata 段”
- `QDomComment`：弦“#comment”
- `QDomDocument`：弦“#document”
- `QDomDocumentFragment`：字符串“#document 片段”
- `QDomDocumentType`：文档类型的名称
- `QDomElement`：标签名称
- `QDomEntity`：实体名称
- `QDomEntityReference`：被引用实体的名称
- `QDomNotation`：符号名称
- `QDomProcessingInstruction`：处理指令的目标
- `QDomText`：弦“#text”
注意：该函数在处理元素和属性节点名称时不考虑命名空间的存在。因此，返回的名称可能包含任何可能存在的命名空间前缀。要获取元素或属性的节点名称，请使用`localName()`;获取命名空间前缀，请使用`namespaceURI()`。

### `QDomNode::NodeType QDomNode::nodeType() const`

**作用与语义：**

返回节点类型。

### `QString QDomNode::nodeValue() const`

**作用与语义：**

返回节点的值。
该值的含义取决于子类：
- `Name`：含义
- `QDomAttr`：属性值
- `QDomCDATASection`：CDATA部分的内容
- `QDomComment`：评论
- `QDomProcessingInstruction`：处理指令的数据
- `QDomText`：文本
其他所有子类都没有节点值，会返回空字符串。

### `void QDomNode::normalize()`

**作用与语义：**

调用元素的 normalize() 会将其所有子节点转换为标准形式。这意味着相邻的 `QDomText` 对象会合并成一个文本对象（`QDomCDATASection`节点不合并）。

### `QDomDocument QDomNode::ownerDocument() const`

**作用与语义：**

返回该节点所属的文档。

### `QDomNode QDomNode::parentNode() const`

**作用与语义：**

返回父节点。如果该节点没有父节点，则返回一个空节点（即`isNull()`返回`true`的节点）。

### `QString QDomNode::prefix() const`

**作用与语义：**

返回节点的命名空间前缀，若节点没有命名空间前缀则返回空字符串。
只有类型为`ElementNode`或`AttributeNode`的节点才能拥有命名空间。创建时必须指定命名空间前缀。如果节点创建时带有命名空间前缀，之后可以用`setPrefix()`更改。
如果你创建带有 `QDomDocument::createElement()` 或 `QDomDocument::createAttribute()` 的元素或属性，前缀将是空字符串。如果你使用 `QDomDocument::createElementNS()` 或 `QDomDocument::createAttributeNS()`，前缀不会是空字符串;但如果名称没有前缀，则可能是空字符串。

### `QDomNode QDomNode::previousSibling() const`

**作用与语义：**

返回文档树中的前一个兄弟节点。更改返回节点也会改变文档树中的节点。
例如，如果你有像这样的 XML 文件：
而这个`QDomNode`代表<p>该标签，前置Sibling()将返回代表<h1>该标签的节点。

**官方示例：**

```cpp
 <h1>Heading</h1>
 <p>The text...</p>
 <h2>Next heading</h2>
```

### `QDomElement QDomNode::previousSiblingElement(const QString &tagName = QString(), const QString &namespaceURI = QString()) const`

**作用与语义：**

返回带有标签名`tagName`和命名空间URI `namespaceURI`的前一个兄弟元素。如果`tagName`为空，返回前一个兄弟元素（`namespaceURI`），如果`namespaceURI`为空，返回前一个兄弟元素，`tagName`。如果两个参数均为空，返回前一个兄弟元素。如果不存在此类兄弟元素，返回空元素。

### `QDomNode QDomNode::removeChild(const QDomNode &oldChild)`

**作用与语义：**

从子节点列表中移除`oldChild`。`oldChild`必须是该节点的直接子节点。
成功时返回新的 `oldChild` 引用，失败时返回空节点。

### `QDomNode QDomNode::replaceChild(const QDomNode &newChild, const QDomNode &oldChild)`

**作用与语义：**

用`newChild`替换`oldChild`。`oldChild`必须是该节点的直接子节点。
如果`newChild`是另一个节点的子节点，则它会被重新父级到该节点。如果`newChild`是该节点的子节点，那么它在子节点列表中的位置会发生变化。
如果`newChild`是`QDomDocumentFragment`，则`oldChild`被该片段的所有子节点替换。
成功时返回新的`oldChild`引用，失败时返回空节点。

### `void QDomNode::save(QTextStream &stream, int indent, QDomNode::EncodingPolicy encodingPolicy = QDomNode::EncodingFromDocument) const`

**作用与语义：**

将节点及其所有子节点的XML表示写入流 `stream`。该函数使用`indent`作为缩进节点的空间量。
如果文档包含无效的XML字符或无法用指定编码方式编码的字符，那么结果和行为将未定义。
如果`encodingPolicy` `QDomNode::EncodingFromDocument`且该节点是文档节点，文本流`stream`的编码通过将名为“xml”的处理指令视为 XML 声明（如果存在）来设定，否则默认为 UTF-8。XML 声明不是处理指令，但这种行为存在于历史原因。如果该节点不是文档节点，则使用文本流的编码。
如果`encodingPolicy`是`EncodingFromTextStream`且该节点是文档节点，该函数表现为 save（`QTextStream` &str， int 缩进），例外是使用文本流 `stream` 中指定的编码。
如果文档包含无效的XML字符或无法用指定编码方式编码的字符，那么结果和行为将未定义。

### `void QDomNode::setNodeValue(const QString &value)`

**作用与语义：**

将节点值设置为`value`。

### `void QDomNode::setPrefix(const QString &pre)`

**作用与语义：**

如果节点有命名空间前缀，该函数将该节点的命名空间前缀改为`pre`。否则该函数不做任何事。
只有类型为`ElementNode`或`AttributeNode`的节点才能拥有命名空间。创建时必须指定命名空间前缀;之后无法添加命名空间前缀。

### `QDomAttr QDomNode::toAttr() const`

**作用与语义：**

将`QDomNode`转换为`QDomAttr`。如果节点不是属性，返回的对象将被`null`。

### `QDomCDATASection QDomNode::toCDATASection() const`

**作用与语义：**

将`QDomNode`转换为`QDomCDATASection`。如果节点不是CDATA部分，返回的对象将被`null`。

### `QDomCharacterData QDomNode::toCharacterData() const`

**作用与语义：**

将`QDomNode`转换为`QDomCharacterData`。如果节点不是字符数据节点，返回的对象将被 `null`。

### `QDomComment QDomNode::toComment() const`

**作用与语义：**

将`QDomNode`转换为`QDomComment`。如果节点不是注释，返回的对象将被 `null`。

### `QDomDocument QDomNode::toDocument() const`

**作用与语义：**

将`QDomNode`转换为`QDomDocument`。如果节点不是文档，返回的对象将被`null`。

### `QDomDocumentFragment QDomNode::toDocumentFragment() const`

**作用与语义：**

将`QDomNode`转换为`QDomDocumentFragment`。如果节点不是文档片段，返回的对象将被`null`。

### `QDomDocumentType QDomNode::toDocumentType() const`

**作用与语义：**

将`QDomNode`转换为`QDomDocumentType`。如果节点不是文档类型，返回的对象将被`null`。

### `QDomElement QDomNode::toElement() const`

**作用与语义：**

将`QDomNode`转换为`QDomElement`。如果节点不是元素，返回的对象将被`null`。

### `QDomEntity QDomNode::toEntity() const`

**作用与语义：**

将`QDomNode`转换为`QDomEntity`。如果节点不是实体，返回的对象将被`null`。

### `QDomEntityReference QDomNode::toEntityReference() const`

**作用与语义：**

将`QDomNode`转换为`QDomEntityReference`。如果节点不是实体引用，返回的对象将被`null`。

### `QDomNotation QDomNode::toNotation() const`

**作用与语义：**

将`QDomNode`转换为`QDomNotation`。如果节点不是符号，返回的对象将被`null`。

### `QDomProcessingInstruction QDomNode::toProcessingInstruction() const`

**作用与语义：**

将`QDomNode`转换为`QDomProcessingInstruction`。如果节点不是处理指令，返回的对象将被`null`。

### `QDomText QDomNode::toText() const`

**作用与语义：**

将`QDomNode`转换为`QDomText`。如果节点不是文本，返回的对象将被`null`。

### `bool QDomNode::operator!=(const QDomNode &other) const`

**作用与语义：**

如果`other`和该DOM节点不相等，返回`true`;否则返回`false`。

### `QDomNode &QDomNode::operator=(const QDomNode &other)`

**作用与语义：**

将`other`的副本分配给该DOM节点。
复制的数据是共享的（浅层复制）：修改一个节点也会改变另一个节点。如果你想做深度复制，可以用`cloneNode()`。

### `bool QDomNode::operator==(const QDomNode &other) const`

**作用与语义：**

如果`other`和该DOM节点相等，返回`true`;否则返回`false`。
任何`QDomNode`实例都作为`QDomDocument`底层数据结构的引用。当两个引用指向同一底层节点时，对等性检查进行检验。例如：
这两个节点（`QDomElement` 是`QDomNode`子类）都指向文档的根元素，`element1 == element2` 返回 true。另一方面：
尽管这两个节点都是携带相同名称的空元素，`element3 == element4` 仍会返回 false，因为它们指向底层数据结构中的两个不同节点。

**官方示例：**

```cpp
 QDomDocument document;
 QDomElement element1 = document.documentElement();
 QDomElement element2 = element1;
```

### `QTextStream &operator<<(QTextStream &str, const QDomNode &node)`

**作用与语义：**

将节点`node`及其所有子节点的XML表示写入流`str`。

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

`QDomNode` 所属机制类型：结构化文本解析机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
