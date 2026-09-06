# QDomDocument

> Qt 6.11.1 · Qt XML

## 1. 先建立直觉

**一句话定位：** `QDomDocument` 是结构化文档类型，负责 JSON/XML 节点、值、解析状态或流式读写。

**模块背景：** Qt XML 提供 XML 文档和 DOM 风格 XML 数据处理能力。

### 这是什么

`QDomDocument` 是 结构化文本解析机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** JSON 通常表示为 value/object/array 树，XML 则包含元素、属性、文本和层级。文档容器负责解析和序列化，具体字段/节点访问由 object、array、value 或 DOM/流式读取对象完成。

**适用场景：** 接收字节数据后显式指定编码和解析选项，检查错误对象，再按类型访问节点，校验业务字段，最后序列化或转换成领域对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要只检查 parse 成功；不要假设字段一定存在且类型固定；不要把用户输入直接当作可信结构；大文件不要无条件 readAll 和构造整棵树。

## 2. 依赖与对象关系

- 头文件：`#include <QDomDocument>`
- 继承自：QDomNode
- 直接派生类：未在类页中列出

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

- `(since 6.5) struct ParseResult`
- `(since 6.5) enum class ParseOption { Default, UseNamespaceProcessing, PreserveSpacingOnlyNodes }`
- `flags ParseOptions`

### 公有函数

- `QDomDocument()`
- `QDomDocument(const QDomDocumentType &doctype)`
- `QDomDocument(const QString &name)`
- `QDomDocument(const QDomDocument &document)`
- `~QDomDocument()`
- `QDomAttr createAttribute(const QString &name)`
- `QDomAttr createAttributeNS(const QString &nsURI, const QString &qName)`
- `QDomCDATASection createCDATASection(const QString &value)`
- `QDomComment createComment(const QString &value)`
- `QDomDocumentFragment createDocumentFragment()`
- `QDomElement createElement(const QString &tagName)`
- `QDomElement createElementNS(const QString &nsURI, const QString &qName)`
- `QDomEntityReference createEntityReference(const QString &name)`
- `QDomProcessingInstruction createProcessingInstruction(const QString &target, const QString &data)`
- `QDomText createTextNode(const QString &value)`
- `QDomDocumentType doctype() const`
- `QDomElement documentElement() const`
- `QDomElement elementById(const QString &elementId)`
- `QDomNodeList elementsByTagName(const QString &tagname) const`
- `QDomNodeList elementsByTagNameNS(const QString &nsURI, const QString &localName)`
- `QDomImplementation implementation() const`
- `QDomNode importNode(const QDomNode &importedNode, bool deep)`
- `QDomNode::NodeType nodeType() const`
- `(since 6.5) QDomDocument::ParseResult setContent(QAnyStringView text, QDomDocument::ParseOptions options = ParseOption::Default)`
- `(since 6.5) QDomDocument::ParseResult setContent(QIODevice *device, QDomDocument::ParseOptions options = ParseOption::Default)`
- `(since 6.5) QDomDocument::ParseResult setContent(QXmlStreamReader *reader, QDomDocument::ParseOptions options = ParseOption::Default)`
- `(since 6.5) QDomDocument::ParseResult setContent(const QByteArray &data, QDomDocument::ParseOptions options = ParseOption::Default)`
- `QByteArray toByteArray(int indent = 1) const`
- `QString toString(int indent = 1) const`
- `QDomDocument & operator=(const QDomDocument &other)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[since 6.5] enum class QDomDocument::ParseOptionflags QDomDocument::ParseOptions`

**作用与语义：**

该枚举描述了使用`setContent()`方法解析XML文档时可能使用的选项。
- `QDomDocument::ParseOption::Default`：`0x00`;不设置解析选项。
- `QDomDocument::ParseOption::UseNamespaceProcessing`：`0x01`;启用命名空间处理。
- `QDomDocument::ParseOption::PreserveSpacingOnlyNodes`：`0x02`;仅包含间隔字符的文本节点被保留。
这个枚举是在Qt 6.5引入的。
ParseOptions 类型是 QFlags 的 typedef<ParseOption>。它存储 ParseOption 值的 OR 组合。

### `QDomDocument::QDomDocument()`

**作用与语义：**

构建一个空白文档。

### `[explicit] QDomDocument::QDomDocument(const QDomDocumentType &doctype)`

**作用与语义：**

创建一个具有文档类型`doctype`的文档。

### `[explicit] QDomDocument::QDomDocument(const QString &name)`

**作用与语义：**

创建一个文档并将文档类型名称设置为`name`。

### `QDomDocument::QDomDocument(const QDomDocument &document)`

**作用与语义：**

复制了`document`。
复制的数据是共享的（浅层复制）：修改一个节点也会改变另一个节点。如果你想做深度复制，可以用`cloneNode()`。

### `[noexcept] QDomDocument::~QDomDocument()`

**作用与语义：**

摧毁该物体并释放其资源。

### `QDomAttr QDomDocument::createAttribute(const QString &name)`

**作用与语义：**

创建一个称为`name`的新属性，可以插入元素中，例如使用`QDomElement::setAttributeNode()`。
如果 `name` 不是有效的 XML 名称，该函数的行为将由 `QDomImplementation::InvalidDataPolicy` 控制。

### `QDomAttr QDomDocument::createAttributeNS(const QString &nsURI, const QString &qName)`

**作用与语义：**

创建一个支持命名空间的新属性，可以插入元素中。属性名称为`qName`，命名空间URI为`nsURI`。该函数还将`QDomNode::prefix()`和`QDomNode::localName()`设置为适当的值（取决于`qName`）。
如果 `qName` 不是有效的 XML 名称，该函数的行为将由 `QDomImplementation::InvalidDataPolicy` 控制。

### `QDomCDATASection QDomDocument::createCDATASection(const QString &value)`

**作用与语义：**

为字符串`value`创建新的 CDATA 部分，可插入文档，例如使用 `QDomNode::appendChild()`。
如果`value`包含无法存储在 CDATA 部分的字符，该函数的行为由 `QDomImplementation::InvalidDataPolicy` 控制。

### `QDomComment QDomDocument::createComment(const QString &value)`

**作用与语义：**

为字符串`value`创建一个新的注释，可以插入到文档中，例如使用`QDomNode::appendChild()`。
如果`value`包含无法存储在XML注释中的字符，该函数的行为由`QDomImplementation::InvalidDataPolicy`控制。

### `QDomDocumentFragment QDomDocument::createDocumentFragment()`

**作用与语义：**

创建一个新的文档片段，可用于保存文档的部分，例如在对文档树进行复杂操作时。

### `QDomElement QDomDocument::createElement(const QString &tagName)`

**作用与语义：**

创建一个称为`tagName`的新元素，可以插入到DOM树中，例如使用`QDomNode::appendChild()`。
如果`tagName`不是有效的XML名称，该函数的行为将受`QDomImplementation::InvalidDataPolicy`控制。

### `QDomElement QDomDocument::createElementNS(const QString &nsURI, const QString &qName)`

**作用与语义：**

创建一个支持命名空间的新元素，可以插入到 DOM 树中。元素的名称为 `qName`，命名空间 URI 为 `nsURI`。该函数还将 `QDomNode::prefix()` 和 `QDomNode::localName()` 设定为合适的值（取决于`qName`）。
如果`qName`是空字符串，无论无效的数据策略是否被设置，都返回一个空元素。

### `QDomEntityReference QDomDocument::createEntityReference(const QString &name)`

**作用与语义：**

创建一个名为 `name` 的新实体引用，可以插入文档中，例如使用 `QDomNode::appendChild()`。
如果`name`不是有效的 XML 名称，该函数的行为将由 `QDomImplementation::InvalidDataPolicy` 控制。

### `QDomProcessingInstruction QDomDocument::createProcessingInstruction(const QString &target, const QString &data)`

**作用与语义：**

创建一条新的处理指令，可以插入文档中，例如使用`QDomNode::appendChild()`。该函数将处理指令的目标设置为`target`，数据设置为`data`。
如果 `target` 不是有效的 XML 名称，或者数据中不包含无法出现在处理指令中的字符，该函数的行为由 `QDomImplementation::InvalidDataPolicy` 控制。

### `QDomText QDomDocument::createTextNode(const QString &value)`

**作用与语义：**

为字符串`value`创建文本节点，可插入文档树，例如使用`QDomNode::appendChild()`。
如果`value`包含无法作为XML文档字符数据存储的字符（即使是字符引用形式），该函数的行为由`QDomImplementation::InvalidDataPolicy`控制。

### `QDomDocumentType QDomDocument::doctype() const`

**作用与语义：**

返回该文档的文档类型。

### `QDomElement QDomDocument::documentElement() const`

**作用与语义：**

返回文档的根元素。

### `QDomElement QDomDocument::elementById(const QString &elementId)`

**作用与语义：**

返回ID等于`elementId`的元素。如果未找到带有该ID的元素，该函数返回一个空元素。
由于QDomClasses不知道哪些属性是元素ID，该函数总是返回一个空元素。未来版本可能会改变这一点。

### `QDomNodeList QDomDocument::elementsByTagName(const QString &tagname) const`

**作用与语义：**

返回一个`QDomNodeList`，包含文档中所有名为 `tagname` 的元素。节点列表的顺序是它们在元素树预排序遍历中遇到的顺序。

### `QDomNodeList QDomDocument::elementsByTagNameNS(const QString &nsURI, const QString &localName)`

**作用与语义：**

返回一个包含文档中所有元素的 `QDomNodeList`，其本地名为 `localName`，命名空间 URI 为 `nsURI`。节点列表的顺序是它们在元素树预序遍历中遇到的顺序。

### `QDomImplementation QDomDocument::implementation() const`

**作用与语义：**

返回一个`QDomImplementation`对象。

### `QDomNode QDomDocument::importNode(const QDomNode &importedNode, bool deep)`

**作用与语义：**

将节点`importedNode`从另一个文档导入到该文档。`importedNode` 仍然保留在原始文档中;该函数创建一个可以在该文档中使用的副本。
该函数返回属于本文档的导入节点。返回的节点没有父节点。无法导入`QDomDocument`节点和`QDomDocumentType`节点。在这种情况下，该函数返回一个空节点。
如果`importedNode`是空节点，则返回空节点。
如果`deep`为真，该函数不仅导入节点`importedNode`，还导入整个子树;如果为假，则仅导入`importedNode`。`deep` 参数对`QDomAttr`和`QDomEntityReference`节点无影响，因为`QDomAttr`节点的后代总是被导入，`QDomEntityReference`节点的后代永远不会被导入。
该函数的行为会根据节点类型略有不同：
- `Node Type`：行为
- `QDomAttr`：所有者元素设置为0，生成属性中指定的标志为真。属性节点的整个子树`importedNode`始终导入：`deep`无影响。
- `QDomDocument`：文档节点无法导入。
- `QDomDocumentFragment`：如果`deep`为真，该函数导入整个文档片段;否则只生成一个空文档片段。
- `QDomDocumentType`：文档类型的节点无法导入。
- `QDomElement`：`QDomAttr::specified()`为真的属性也会被导入，其他属性则不导入。如果`deep`为真，该函数还会导入`importedNode`的子树;否则只导入元素节点（以及部分属性，见上文）。
- `QDomEntity`：实体节点可以导入，但目前无法使用，因为DOM级别中文档类型为只读。
- `QDomEntityReference`：实体引用节点的后代永远不会导入：`deep` 没有影响。
- `QDomNotation`：符号节点可以导入，但目前无法使用，因为DOM级别2的文档类型是只读的。
- `QDomProcessingInstruction`：处理指令的目标和值被复制到新节点。
- `QDomText`：文本被复制到新节点。
- `QDomCDATASection`：文本被复制到新节点。
- `QDomComment`：文本被复制到新节点。

### `QDomNode::NodeType QDomDocument::nodeType() const`

**作用与语义：**

返回`DocumentNode`。

### `[since 6.5] QDomDocument::ParseResult QDomDocument::setContent(QXmlStreamReader *reader, QDomDocument::ParseOptions options = ParseOption::Default)`

**作用与语义：**

该函数从字节数组`data`、字符串视图`text`、输入输出（IO）`device`或流`reader`中解析XML文档，并将其设置为文档内容。它尝试检测文档的编码，符合XML规范。返回解析结果，并以`ParseResult`形式显式转换为`bool`。
你可以用`options`参数指定不同的解析选项，比如启用命名空间处理等。
默认情况下，命名空间处理是被禁用的。如果禁用了命名空间处理，解析器在读取XML文件时就不会进行命名空间处理。函数`QDomNode::prefix()`、`QDomNode::localName()`和`QDomNode::namespaceURI()`返回一个空字符串。
如果通过解析`options`启用命名空间处理，解析器会识别XML文件中的命名空间，并将前缀名、本地名和命名空间URI设置为合适的值。函数`QDomNode::prefix()`、`QDomNode::localName()`和`QDomNode::namespaceURI()`为所有元素和属性返回字符串，如果元素或属性没有前缀则返回空字符串。
仅由空白组成的文本节点会被剥离，不会出现在`QDomDocument`中。自Qt 6.5起，可以将`QDomDocument::ParseOption::PreserveSpacingOnlyNodes`作为解析选项，指定必须保留仅间距的文本节点。
实体引用的处理方式如下：
- 包含内容中对内部通用实体和字符实体的引用。结果是一个`QDomText`节点，引用被对应的实体值替换。
- 包含对内部子集中中参数实体的引用。结果是一个包含实体声明和符号声明的`QDomDocumentType`节点，引用被对应的实体值替换。
- 任何未在内部子集中定义且出现在内容中的一般解析实体引用，都表示为`QDomEntityReference`节点。
- 任何未在内部子集定义且出现在内容之外的解析实体引用，都被替换为空字符串。
- 任何未解析的实体引用都被替换为空字符串。
注意：重载的 IO 接管 `device` 会尝试以只读模式打开，前提是设备尚未打开。在这种情况下，调用者负责调用关闭。这种情况将在Qt 7 发生变化，届时不再打开 IO `device`。因此，应用程序应在调用 `setContent()` 前自行打开设备。

### `QByteArray QDomDocument::toByteArray(int indent = 1) const`

**作用与语义：**

将解析后的文档转换回文本表示，并返回包含 UTF-8 编码数据的 `QByteArray`。
该函数使用 `indent` 作为缩进子元素的空间量。

### `QString QDomDocument::toString(int indent = 1) const`

**作用与语义：**

将解析后的文档转换回文本表示。
该函数使用 `indent` 作为缩进子元素的空间。
如果`indent`为-1，则不添加任何空白。

### `QDomDocument &QDomDocument::operator=(const QDomDocument &other)`

**作用与语义：**

将`other`分配到此DOM文档中。
复制的数据是共享的（浅层复制）：修改一个节点也会改变另一个节点。如果你想做深度复制，可以用`cloneNode()`。

### `(since 6.5) struct ParseResult`

**作用与语义：**

该结构用于存储QDomDocument::setContent()的结果。
`QDomDocument::ParseResult`结构用于存储`QDomDocument::setContent()`的结果。如果在解析XML文档时发现错误，错误的消息、行号和列号将存储在`ParseResult`中。

### `(since 6.5) enum class ParseOption { Default, UseNamespaceProcessing, PreserveSpacingOnlyNodes }`

**作用与语义：**

该枚举描述了使用`setContent()`方法解析XML文档时可能使用的选项。
- `QDomDocument::ParseOption::Default`：`0x00`;不设置解析选项。
- `QDomDocument::ParseOption::UseNamespaceProcessing`：`0x01`;启用命名空间处理。
- `QDomDocument::ParseOption::PreserveSpacingOnlyNodes`：`0x02`;仅包含间隔字符的文本节点被保留。
这个枚举是在Qt 6.5引入的。
ParseOptions 类型是 QFlags 的 typedef<ParseOption>。它存储 ParseOption 值的 OR 组合。

### `flags ParseOptions`

**作用与语义：**

该枚举描述了使用`setContent()`方法解析XML文档时可能使用的选项。
- `QDomDocument::ParseOption::Default`：`0x00`;不设置解析选项。
- `QDomDocument::ParseOption::UseNamespaceProcessing`：`0x01`;启用命名空间处理。
- `QDomDocument::ParseOption::PreserveSpacingOnlyNodes`：`0x02`;仅包含间隔字符的文本节点被保留。
这个枚举是在Qt 6.5引入的。
ParseOptions 类型是 QFlags 的 typedef<ParseOption>。它存储 ParseOption 值的 OR 组合。

### `(since 6.5) QDomDocument::ParseResult setContent(QAnyStringView text, QDomDocument::ParseOptions options = ParseOption::Default)`

**作用与语义：**

该函数从字节数组`data`、字符串视图`text`、输入输出（IO）`device`或流`reader`中解析XML文档，并将其设置为文档内容。它尝试检测文档的编码，符合XML规范。返回解析结果，并以`ParseResult`形式显式转换为`bool`。
你可以用`options`参数指定不同的解析选项，比如启用命名空间处理等。
默认情况下，命名空间处理是被禁用的。如果禁用了命名空间处理，解析器在读取XML文件时就不会进行命名空间处理。函数`QDomNode::prefix()`、`QDomNode::localName()`和`QDomNode::namespaceURI()`返回一个空字符串。
如果通过解析`options`启用命名空间处理，解析器会识别XML文件中的命名空间，并将前缀名、本地名和命名空间URI设置为合适的值。函数`QDomNode::prefix()`、`QDomNode::localName()`和`QDomNode::namespaceURI()`为所有元素和属性返回字符串，如果元素或属性没有前缀则返回空字符串。
仅由空白组成的文本节点会被剥离，不会出现在`QDomDocument`中。自Qt 6.5起，可以将`QDomDocument::ParseOption::PreserveSpacingOnlyNodes`作为解析选项，指定必须保留仅间距的文本节点。
实体引用的处理方式如下：
- 包含内容中对内部通用实体和字符实体的引用。结果是一个`QDomText`节点，引用被对应的实体值替换。
- 包含对内部子集中中参数实体的引用。结果是一个包含实体声明和符号声明的`QDomDocumentType`节点，引用被对应的实体值替换。
- 任何未在内部子集中定义且出现在内容中的一般解析实体引用，都表示为`QDomEntityReference`节点。
- 任何未在内部子集定义且出现在内容之外的解析实体引用，都被替换为空字符串。
- 任何未解析的实体引用都被替换为空字符串。
注意：重载的 IO 接管 `device` 会尝试以只读模式打开，前提是设备尚未打开。在这种情况下，调用者负责调用关闭。这种情况将在Qt 7 发生变化，届时不再打开 IO `device`。因此，应用程序应在调用 `setContent()` 前自行打开设备。

### `(since 6.5) QDomDocument::ParseResult setContent(QIODevice *device, QDomDocument::ParseOptions options = ParseOption::Default)`

**作用与语义：**

该函数从字节数组`data`、字符串视图`text`、输入输出（IO）`device`或流`reader`中解析XML文档，并将其设置为文档内容。它尝试检测文档的编码，符合XML规范。返回解析结果，并以`ParseResult`形式显式转换为`bool`。
你可以用`options`参数指定不同的解析选项，比如启用命名空间处理等。
默认情况下，命名空间处理是被禁用的。如果禁用了命名空间处理，解析器在读取XML文件时就不会进行命名空间处理。函数`QDomNode::prefix()`、`QDomNode::localName()`和`QDomNode::namespaceURI()`返回一个空字符串。
如果通过解析`options`启用命名空间处理，解析器会识别XML文件中的命名空间，并将前缀名、本地名和命名空间URI设置为合适的值。函数`QDomNode::prefix()`、`QDomNode::localName()`和`QDomNode::namespaceURI()`为所有元素和属性返回字符串，如果元素或属性没有前缀则返回空字符串。
仅由空白组成的文本节点会被剥离，不会出现在`QDomDocument`中。自Qt 6.5起，可以将`QDomDocument::ParseOption::PreserveSpacingOnlyNodes`作为解析选项，指定必须保留仅间距的文本节点。
实体引用的处理方式如下：
- 包含内容中对内部通用实体和字符实体的引用。结果是一个`QDomText`节点，引用被对应的实体值替换。
- 包含对内部子集中中参数实体的引用。结果是一个包含实体声明和符号声明的`QDomDocumentType`节点，引用被对应的实体值替换。
- 任何未在内部子集中定义且出现在内容中的一般解析实体引用，都表示为`QDomEntityReference`节点。
- 任何未在内部子集定义且出现在内容之外的解析实体引用，都被替换为空字符串。
- 任何未解析的实体引用都被替换为空字符串。
注意：重载的 IO 接管 `device` 会尝试以只读模式打开，前提是设备尚未打开。在这种情况下，调用者负责调用关闭。这种情况将在Qt 7 发生变化，届时不再打开 IO `device`。因此，应用程序应在调用 `setContent()` 前自行打开设备。

### `(since 6.5) QDomDocument::ParseResult setContent(const QByteArray &data, QDomDocument::ParseOptions options = ParseOption::Default)`

**作用与语义：**

该函数从字节数组`data`、字符串视图`text`、输入输出（IO）`device`或流`reader`中解析XML文档，并将其设置为文档内容。它尝试检测文档的编码，符合XML规范。返回解析结果，并以`ParseResult`形式显式转换为`bool`。
你可以用`options`参数指定不同的解析选项，比如启用命名空间处理等。
默认情况下，命名空间处理是被禁用的。如果禁用了命名空间处理，解析器在读取XML文件时就不会进行命名空间处理。函数`QDomNode::prefix()`、`QDomNode::localName()`和`QDomNode::namespaceURI()`返回一个空字符串。
如果通过解析`options`启用命名空间处理，解析器会识别XML文件中的命名空间，并将前缀名、本地名和命名空间URI设置为合适的值。函数`QDomNode::prefix()`、`QDomNode::localName()`和`QDomNode::namespaceURI()`为所有元素和属性返回字符串，如果元素或属性没有前缀则返回空字符串。
仅由空白组成的文本节点会被剥离，不会出现在`QDomDocument`中。自Qt 6.5起，可以将`QDomDocument::ParseOption::PreserveSpacingOnlyNodes`作为解析选项，指定必须保留仅间距的文本节点。
实体引用的处理方式如下：
- 包含内容中对内部通用实体和字符实体的引用。结果是一个`QDomText`节点，引用被对应的实体值替换。
- 包含对内部子集中中参数实体的引用。结果是一个包含实体声明和符号声明的`QDomDocumentType`节点，引用被对应的实体值替换。
- 任何未在内部子集中定义且出现在内容中的一般解析实体引用，都表示为`QDomEntityReference`节点。
- 任何未在内部子集定义且出现在内容之外的解析实体引用，都被替换为空字符串。
- 任何未解析的实体引用都被替换为空字符串。
注意：重载的 IO 接管 `device` 会尝试以只读模式打开，前提是设备尚未打开。在这种情况下，调用者负责调用关闭。这种情况将在Qt 7 发生变化，届时不再打开 IO `device`。因此，应用程序应在调用 `setContent()` 前自行打开设备。

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

`QDomDocument` 所属机制类型：结构化文本解析机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
