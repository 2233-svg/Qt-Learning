# QDomElement

> Qt 6.11.1 · Qt XML

## 1. 先建立直觉

**一句话定位：** `QDomElement` 是结构化文档类型，负责 JSON/XML 节点、值、解析状态或流式读写。

**模块背景：** Qt XML 提供 XML 文档和 DOM 风格 XML 数据处理能力。

### 这是什么

`QDomElement` 是 结构化文本解析机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** JSON 通常表示为 value/object/array 树，XML 则包含元素、属性、文本和层级。文档容器负责解析和序列化，具体字段/节点访问由 object、array、value 或 DOM/流式读取对象完成。

**适用场景：** 接收字节数据后显式指定编码和解析选项，检查错误对象，再按类型访问节点，校验业务字段，最后序列化或转换成领域对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要只检查 parse 成功；不要假设字段一定存在且类型固定；不要把用户输入直接当作可信结构；大文件不要无条件 readAll 和构造整棵树。

## 2. 依赖与对象关系

- 头文件：`#include <QDomElement>`
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

### 公有函数

- `QDomElement()`
- `QDomElement(const QDomElement &element)`
- `QString attribute(const QString &name, const QString &defValue = QString()) const`
- `QString attributeNS(const QString &nsURI, const QString &localName, const QString &defValue = QString()) const`
- `QDomAttr attributeNode(const QString &name)`
- `QDomAttr attributeNodeNS(const QString &nsURI, const QString &localName)`
- `QDomNamedNodeMap attributes() const`
- `QDomNodeList elementsByTagName(const QString &tagname) const`
- `QDomNodeList elementsByTagNameNS(const QString &nsURI, const QString &localName) const`
- `bool hasAttribute(const QString &name) const`
- `bool hasAttributeNS(const QString &nsURI, const QString &localName) const`
- `QDomNode::NodeType nodeType() const`
- `void removeAttribute(const QString &name)`
- `void removeAttributeNS(const QString &nsURI, const QString &localName)`
- `QDomAttr removeAttributeNode(const QDomAttr &oldAttr)`
- `void setAttribute(const QString &name, const QString &value)`
- `void setAttribute(const QString &name, double value)`
- `void setAttribute(const QString &name, float value)`
- `void setAttribute(const QString &name, int value)`
- `void setAttribute(const QString &name, qlonglong value)`
- `void setAttribute(const QString &name, qulonglong value)`
- `void setAttribute(const QString &name, uint value)`
- `void setAttributeNS(const QString &nsURI, const QString &qName, const QString &value)`
- `void setAttributeNS(const QString &nsURI, const QString &qName, double value)`
- `void setAttributeNS(const QString &nsURI, const QString &qName, int value)`
- `void setAttributeNS(const QString &nsURI, const QString &qName, qlonglong value)`
- `void setAttributeNS(const QString &nsURI, const QString &qName, qulonglong value)`
- `void setAttributeNS(const QString &nsURI, const QString &qName, uint value)`
- `QDomAttr setAttributeNode(const QDomAttr &newAttr)`
- `QDomAttr setAttributeNodeNS(const QDomAttr &newAttr)`
- `void setTagName(const QString &name)`
- `QString tagName() const`
- `QString text() const`
- `QDomElement & operator=(const QDomElement &other)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QDomElement::QDomElement()`

**作用与语义：**

构造一个空元素。使用`QDomDocument::createElement()`函数构造包含内容的元素。

### `QDomElement::QDomElement(const QDomElement &element)`

**作用与语义：**

构建了一份`element`的副本。
复制的数据是共享的（浅副本）：修改一个节点也会改变另一个节点。如果你想做深度复制，可以用`cloneNode()`。

### `QString QDomElement::attribute(const QString &name, const QString &defValue = QString()) const`

**作用与语义：**

返回称为`name`的属性。如果该属性不存在，返回`defValue`。

### `QString QDomElement::attributeNS(const QString &nsURI, const QString &localName, const QString &defValue = QString()) const`

**作用与语义：**

返回带有本地名称`localName`的属性和命名空间URI的属性`nsURI`。如果该属性不存在，则返回`defValue`。

### `QDomAttr QDomElement::attributeNode(const QString &name)`

**作用与语义：**

返回对应于称为`name`的属性的 `QDomAttr` 对象。如果不存在此类属性，则返回空属性。

### `QDomAttr QDomElement::attributeNodeNS(const QString &nsURI, const QString &localName)`

**作用与语义：**

返回对应本地名称为`localName`的属性和命名空间URI `nsURI`的`QDomAttr`对象。如果不存在此类属性，则返回一个空属性。

### `QDomNamedNodeMap QDomElement::attributes() const`

**作用与语义：**

返回包含该元素所有属性的`QDomNamedNodeMap`。

### `QDomNodeList QDomElement::elementsByTagName(const QString &tagname) const`

**作用与语义：**

返回一个包含该元素所有后代的`QDomNodeList`，这些元素在以该元素为根的预序遍历中遇到的，这些元素名为`tagname`。返回列表中元素的顺序即为预序遍历过程中遇到的顺序。

### `QDomNodeList QDomElement::elementsByTagNameNS(const QString &nsURI, const QString &localName) const`

**作用与语义：**

返回一个包含该元素所有后代的`QDomNodeList`，其本地名称`localName`和命名空间URI `nsURI`在以该元素为根的预序遍历中遇到。返回列表中元素的顺序即为预序遍历过程中遇到的顺序。

### `bool QDomElement::hasAttribute(const QString &name) const`

**作用与语义：**

如果该元素有称为`name`的属性，则返回`true`;否则返回`false`。
注意：该函数不考虑命名空间的存在。因此，指定名称将与包含任何可能存在的命名空间前缀的完全限定属性名称进行测试。
用`hasAttributeNS()`明确测试具有特定命名空间和名称的属性。

### `bool QDomElement::hasAttributeNS(const QString &nsURI, const QString &localName) const`

**作用与语义：**

如果该元素具有本地名称为`localName`且命名空间为`nsURI` URI的属性，则返回`true`;否则返回false。

### `QDomNode::NodeType QDomElement::nodeType() const`

**作用与语义：**

退货 `ElementNode`。

### `void QDomElement::removeAttribute(const QString &name)`

**作用与语义：**

从该元素中移除名为name `name`的属性。

### `void QDomElement::removeAttributeNS(const QString &nsURI, const QString &localName)`

**作用与语义：**

从该元素中移除带有本地名称`localName`的属性和URI `nsURI`命名空间。

### `QDomAttr QDomElement::removeAttributeNode(const QDomAttr &oldAttr)`

**作用与语义：**

从元素中移除属性`oldAttr`并返回。

### `void QDomElement::setAttribute(const QString &name, const QString &value)`

**作用与语义：**

添加一个名为`name`的属性，值为`value`。如果存在同名属性，其值被替换为`value`。

### `void QDomElement::setAttribute(const QString &name, double value)`

**作用与语义：**

格式总是用`QLocale::C`。

### `void QDomElement::setAttribute(const QString &name, float value)`

**作用与语义：**

格式总是用`QLocale::C`。

### `void QDomElement::setAttribute(const QString &name, int value)`

**作用与语义：**

格式总是用`QLocale::C`。

### `void QDomElement::setAttribute(const QString &name, qlonglong value)`

**作用与语义：**

格式总是用`QLocale::C`。

### `void QDomElement::setAttribute(const QString &name, qulonglong value)`

**作用与语义：**

格式总是用`QLocale::C`。

### `void QDomElement::setAttribute(const QString &name, uint value)`

**作用与语义：**

格式总是用`QLocale::C`。

### `void QDomElement::setAttributeNS(const QString &nsURI, const QString &qName, const QString &value)`

**作用与语义：**

添加一个带有限定名称`qName`的属性，以及以 `value` 值的命名空间 URI `nsURI`。如果存在具有相同本地名称和命名空间 URI 的属性，其前缀被 `qName` 前缀替换，其值被 `value` 替换。
虽然`qName`是限定名称，但本地名称用于决定是否替换现有属性的值。

### `void QDomElement::setAttributeNS(const QString &nsURI, const QString &qName, double value)`

**作用与语义：**

添加一个带有限定名称`qName`的属性，以及以 `value` 值的命名空间 URI `nsURI`。如果存在具有相同本地名称和命名空间 URI 的属性，其前缀被 `qName` 前缀替换，其值被 `value` 替换。
虽然`qName`是限定名称，但本地名称用于决定是否替换现有属性的值。

### `void QDomElement::setAttributeNS(const QString &nsURI, const QString &qName, int value)`

**作用与语义：**

添加一个带有限定名称`qName`的属性，以及以 `value` 值的命名空间 URI `nsURI`。如果存在具有相同本地名称和命名空间 URI 的属性，其前缀被 `qName` 前缀替换，其值被 `value` 替换。
虽然`qName`是限定名称，但本地名称用于决定是否替换现有属性的值。

### `void QDomElement::setAttributeNS(const QString &nsURI, const QString &qName, qlonglong value)`

**作用与语义：**

添加一个带有限定名称`qName`的属性，以及以 `value` 值的命名空间 URI `nsURI`。如果存在具有相同本地名称和命名空间 URI 的属性，其前缀被 `qName` 前缀替换，其值被 `value` 替换。
虽然`qName`是限定名称，但本地名称用于决定是否替换现有属性的值。

### `void QDomElement::setAttributeNS(const QString &nsURI, const QString &qName, qulonglong value)`

**作用与语义：**

添加一个带有限定名称`qName`的属性，以及以 `value` 值的命名空间 URI `nsURI`。如果存在具有相同本地名称和命名空间 URI 的属性，其前缀被 `qName` 前缀替换，其值被 `value` 替换。
虽然`qName`是限定名称，但本地名称用于决定是否替换现有属性的值。

### `void QDomElement::setAttributeNS(const QString &nsURI, const QString &qName, uint value)`

**作用与语义：**

添加一个带有限定名称`qName`的属性，以及以 `value` 值的命名空间 URI `nsURI`。如果存在具有相同本地名称和命名空间 URI 的属性，其前缀被 `qName` 前缀替换，其值被 `value` 替换。
虽然`qName`是限定名称，但本地名称用于决定是否替换现有属性的值。

### `QDomAttr QDomElement::setAttributeNode(const QDomAttr &newAttr)`

**作用与语义：**

为该元素添加属性`newAttr`。
如果元素有与`newAttr`同名的另一个属性，该函数会替换该属性并返回该属性;否则函数返回空属性。

### `QDomAttr QDomElement::setAttributeNodeNS(const QDomAttr &newAttr)`

**作用与语义：**

为该元素添加属性`newAttr`。
如果元素有另一个属性，且与`newAttr`具有相同的本地名称和命名空间URI，该函数会替换该属性并返回该属性;否则该函数返回空属性。

### `void QDomElement::setTagName(const QString &name)`

**作用与语义：**

将该元素的标签名称设置为`name`。

### `QString QDomElement::tagName() const`

**作用与语义：**

返回该元素的标签名称。对于像这样的XML元素：
标签名称会返回“IMG”。

**官方示例：**

```cpp
 <img src="myimg.png">
```

### `QString QDomElement::text() const`

**作用与语义：**

返回元素的文本或空字符串。
`<h1>`标签`QDomElement`函数文本()将返回以下文本：
该函数忽略注释。它只评估`QDomText`和`QDomCDATASection`对象。

**官方示例：**

```cpp
 <h1>Hello <b>Qt</b> <![CDATA[<xml is cool>]]></h1>
```

### `QDomElement &QDomElement::operator=(const QDomElement &other)`

**作用与语义：**

为该DOM元素分配`other`。
复制的数据是共享的（浅层复制）：修改一个节点也会改变另一个节点。如果你想做深度复制，可以用`cloneNode()`。

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

`QDomElement` 所属机制类型：结构化文本解析机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
