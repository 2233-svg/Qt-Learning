# QDomImplementation

> Qt 6.11.1 · Qt XML

## 1. 先建立直觉

**一句话定位：** `QDomImplementation` 是结构化文档类型，负责 JSON/XML 节点、值、解析状态或流式读写。

**模块背景：** Qt XML 提供 XML 文档和 DOM 风格 XML 数据处理能力。

### 这是什么

`QDomImplementation` 是 结构化文本解析机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** JSON 通常表示为 value/object/array 树，XML 则包含元素、属性、文本和层级。文档容器负责解析和序列化，具体字段/节点访问由 object、array、value 或 DOM/流式读取对象完成。

**适用场景：** 接收字节数据后显式指定编码和解析选项，检查错误对象，再按类型访问节点，校验业务字段，最后序列化或转换成领域对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要只检查 parse 成功；不要假设字段一定存在且类型固定；不要把用户输入直接当作可信结构；大文件不要无条件 readAll 和构造整棵树。

## 2. 依赖与对象关系

- 头文件：`#include <QDomImplementation>`
- 继承自：未在类页中列出
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

- `enum InvalidDataPolicy { AcceptInvalidChars, DropInvalidChars, ReturnNullNode }`

### 公有函数

- `QDomImplementation()`
- `QDomImplementation(const QDomImplementation &implementation)`
- `~QDomImplementation()`
- `QDomDocument createDocument(const QString &nsURI, const QString &qName, const QDomDocumentType &doctype)`
- `QDomDocumentType createDocumentType(const QString &qName, const QString &publicId, const QString &systemId)`
- `bool hasFeature(const QString &feature, const QString &version) const`
- `bool isNull()`
- `bool operator!=(const QDomImplementation &other) const`
- `QDomImplementation & operator=(const QDomImplementation &other)`
- `bool operator==(const QDomImplementation &other) const`

### 静态公有成员

- `QDomImplementation::InvalidDataPolicy invalidDataPolicy()`
- `void setInvalidDataPolicy(QDomImplementation::InvalidDataPolicy policy)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QDomImplementation::InvalidDataPolicy`

**作用与语义：**

该枚举规定了当调用`QDomDocument`中的工厂函数时，数据无效时应采取的操作。
- `QDomImplementation::AcceptInvalidChars`：`0`;数据无论如何都应该存储在DOM对象中。在这种情况下，最终生成的XML文档可能不是良好格式的。这是Qt < 4.1中的默认值和QDom的行为。
- `QDomImplementation::DropInvalidChars`：`1`;应从数据中删除无效字符。
- `QDomImplementation::ReturnNullNode`：`2`;工厂函数应返回一个空节点。

### `QDomImplementation::QDomImplementation()`

**作用与语义：**

构建一个QDomImpliation对象。

### `QDomImplementation::QDomImplementation(const QDomImplementation &implementation)`

**作用与语义：**

复制了`implementation`。

### `[noexcept] QDomImplementation::~QDomImplementation()`

**作用与语义：**

摧毁该物体并释放其资源。

### `QDomDocument QDomImplementation::createDocument(const QString &nsURI, const QString &qName, const QDomDocumentType &doctype)`

**作用与语义：**

创建文档类型为 `doctype` 的 DOM 文档。该函数还添加一个根元素节点，包含合格名称 `qName` 和命名空间 URI `nsURI`。

### `QDomDocumentType QDomImplementation::createDocumentType(const QString &qName, const QString &publicId, const QString &systemId)`

**作用与语义：**

为名称`qName`创建文档类型节点。
`publicId`指定外部子集的公共标识符。如果将`publicId`指定为空字符串（QString()），则表示文档类型没有公共标识符。
`systemId`指定外部子集的系统标识符。如果将`systemId`指定为空字符串，则表示文档类型没有系统标识符。
由于没有系统标识符不能有公共标识符，如果没有系统标识符，则公共标识符将设置为空字符串。
DOM级别2不支持任何其他文档类型声明功能。
创建的这种文档类型的唯一使用方式，是与`createDocument()`函数结合，使用此文档类型创建`QDomDocument`。
在DOM规范中，这是创建非空文档的唯一方式。出于历史原因，Qt也允许使用默认的空构造函数创建文档。生成的文档是空的，但当调用工厂函数，例如`QDomDocument::createElement()`时，它将变为非空文档。当调用setContent()时，文档也会变为非空。

### `bool QDomImplementation::hasFeature(const QString &feature, const QString &version) const`

**作用与语义：**

如果QDom实现了请求的`version`，函数返回`true` `feature`;否则返回`false`。
目前支持的功能及其版本：
- `Feature`：版本
- `XML`：1.0

### `[static] QDomImplementation::InvalidDataPolicy QDomImplementation::invalidDataPolicy()`

**作用与语义：**

返回无效数据策略，该策略规定了当`QDomDocument`中的工厂函数传递无效数据时应采取的措施。
警告：此函数不重复使用。

### `bool QDomImplementation::isNull()`

**作用与语义：**

如果对象是由 `QDomDocument::implementation()` 创建的，则返回 `false`；否则返回 `true`。

### `[static] void QDomImplementation::setInvalidDataPolicy(QDomImplementation::InvalidDataPolicy policy)`

**作用与语义：**

设置无效数据策略，规定当`QDomDocument`中的工厂函数传递无效数据时应采取的措施。
`policy`为所有已存在且未来将被创造的`QDomDocument`实例设定。
警告：此函数不重复使用。

**官方示例：**

```cpp
 void XML_snippet_main()
 {
 QDomDocument doc;
 QDomImplementation impl;
 // This will create the element, but the resulting XML document will
 // be invalid, because '~' is not a valid character in a tag name.
 impl.setInvalidDataPolicy(QDomImplementation::AcceptInvalidChars);
 QDomElement elt1 = doc.createElement("foo~bar");

 // This will create an element with the tag name "foobar".
 impl.setInvalidDataPolicy(QDomImplementation::DropInvalidChars);
 QDomElement elt2 = doc.createElement("foo~bar");

 // This will create a null element.
 impl.setInvalidDataPolicy(QDomImplementation::ReturnNullNode);
 QDomElement elt3 = doc.createElement("foo~bar");
 }
```

### `bool QDomImplementation::operator!=(const QDomImplementation &other) const`

**作用与语义：**

如果`other`和该DOM实现对象是由不同的QDomDocuments创建的，返回`true`;否则返回`false`。

### `QDomImplementation &QDomImplementation::operator=(const QDomImplementation &other)`

**作用与语义：**

为该DOM实现分配`other`。

### `bool QDomImplementation::operator==(const QDomImplementation &other) const`

**作用与语义：**

如果`other`和该DOM实现对象是从同一`QDomDocument`创建的，则返回`true`;否则返回`false`。

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

`QDomImplementation` 所属机制类型：结构化文本解析机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
