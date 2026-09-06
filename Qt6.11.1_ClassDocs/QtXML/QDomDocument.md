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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 34 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[since 6.5] enum class QDomDocument::ParseOptionflags QDomDocument::ParseOptions`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QDomDocument` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ParseOptionflags QDomDocument::ParseOptions`。
- 属性名：`QDomDocument`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDomDocument::QDomDocument()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDomDocument` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QDomDocument::QDomDocument(const QDomDocumentType &doctype)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDomDocument` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `doctype`：类型为 `const QDomDocumentType &`。没有默认值，调用时必须提供。传入 `const QDomDocumentType &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QDomDocument::QDomDocument(const QString &name)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDomDocument` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDomDocument::QDomDocument(const QDomDocument &document)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDomDocument` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `document`：类型为 `const QDomDocument &`。没有默认值，调用时必须提供。传入 `const QDomDocument &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QDomDocument::~QDomDocument()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDomDocument` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDomAttr QDomDocument::createAttribute(const QString &name)`

**API 类别：** 成员函数说明

**中文解读：** `QDomDocument::createAttribute` 用于计算、查询或取得与“创建、Attribute”相关的操作。调用时要先确认当前状态和 `name` 的有效范围；返回类型是 `QDomAttr`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDomAttr`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDomAttr QDomDocument::createAttributeNS(const QString &nsURI, const QString &qName)`

**API 类别：** 成员函数说明

**中文解读：** `QDomDocument::createAttributeNS` 用于计算、查询或取得与“创建、Attribute、NS”相关的操作。调用时要先确认当前状态和 `nsURI`、`qName` 的有效范围；返回类型是 `QDomAttr`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDomAttr`。
- 参数 `nsURI`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `qName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDomCDATASection QDomDocument::createCDATASection(const QString &value)`

**API 类别：** 成员函数说明

**中文解读：** `QDomDocument::createCDATASection` 用于计算、查询或取得与“创建、CDATA、Section”相关的操作。调用时要先确认当前状态和 `value` 的有效范围；返回类型是 `QDomCDATASection`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDomCDATASection`。
- 参数 `value`：类型为 `const QString &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDomComment QDomDocument::createComment(const QString &value)`

**API 类别：** 成员函数说明

**中文解读：** `QDomDocument::createComment` 用于计算、查询或取得与“创建、Comment”相关的操作。调用时要先确认当前状态和 `value` 的有效范围；返回类型是 `QDomComment`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDomComment`。
- 参数 `value`：类型为 `const QString &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDomDocumentFragment QDomDocument::createDocumentFragment()`

**API 类别：** 成员函数说明

**中文解读：** `QDomDocument::createDocumentFragment` 用于计算、查询或取得与“创建、Document、Fragment”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDomDocumentFragment`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDomDocumentFragment`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDomElement QDomDocument::createElement(const QString &tagName)`

**API 类别：** 成员函数说明

**中文解读：** `QDomDocument::createElement` 用于计算、查询或取得与“创建、Element”相关的操作。调用时要先确认当前状态和 `tagName` 的有效范围；返回类型是 `QDomElement`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDomElement`。
- 参数 `tagName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDomElement QDomDocument::createElementNS(const QString &nsURI, const QString &qName)`

**API 类别：** 成员函数说明

**中文解读：** `QDomDocument::createElementNS` 用于计算、查询或取得与“创建、Element、NS”相关的操作。调用时要先确认当前状态和 `nsURI`、`qName` 的有效范围；返回类型是 `QDomElement`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDomElement`。
- 参数 `nsURI`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `qName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDomEntityReference QDomDocument::createEntityReference(const QString &name)`

**API 类别：** 成员函数说明

**中文解读：** `QDomDocument::createEntityReference` 用于计算、查询或取得与“创建、Entity、Reference”相关的操作。调用时要先确认当前状态和 `name` 的有效范围；返回类型是 `QDomEntityReference`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDomEntityReference`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDomProcessingInstruction QDomDocument::createProcessingInstruction(const QString &target, const QString &data)`

**API 类别：** 成员函数说明

**中文解读：** `QDomDocument::createProcessingInstruction` 用于计算、查询或取得与“创建、Processing、Instruction”相关的操作。调用时要先确认当前状态和 `target`、`data` 的有效范围；返回类型是 `QDomProcessingInstruction`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDomProcessingInstruction`。
- 参数 `target`：类型为 `const QString &`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `data`：类型为 `const QString &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDomText QDomDocument::createTextNode(const QString &value)`

**API 类别：** 成员函数说明

**中文解读：** `QDomDocument::createTextNode` 用于计算、查询或取得与“创建、文本、Node”相关的操作。调用时要先确认当前状态和 `value` 的有效范围；返回类型是 `QDomText`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDomText`。
- 参数 `value`：类型为 `const QString &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDomDocumentType QDomDocument::doctype() const`

**API 类别：** 成员函数说明

**中文解读：** `QDomDocument::doctype` 用于计算、查询或取得与“doctype”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDomDocumentType`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDomDocumentType`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDomElement QDomDocument::documentElement() const`

**API 类别：** 成员函数说明

**中文解读：** `QDomDocument::documentElement` 用于计算、查询或取得与“document、Element”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDomElement`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDomElement`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDomElement QDomDocument::elementById(const QString &elementId)`

**API 类别：** 成员函数说明

**中文解读：** `QDomDocument::elementById` 用于计算、查询或取得与“element、By、Id”相关的操作。调用时要先确认当前状态和 `elementId` 的有效范围；返回类型是 `QDomElement`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDomElement`。
- 参数 `elementId`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDomNodeList QDomDocument::elementsByTagName(const QString &tagname) const`

**API 类别：** 成员函数说明

**中文解读：** `QDomDocument::elementsByTagName` 用于计算、查询或取得与“elements、By、Tag、名称”相关的操作。调用时要先确认当前状态和 `tagname` 的有效范围；返回类型是 `QDomNodeList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDomNodeList`。
- 参数 `tagname`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDomNodeList QDomDocument::elementsByTagNameNS(const QString &nsURI, const QString &localName)`

**API 类别：** 成员函数说明

**中文解读：** `QDomDocument::elementsByTagNameNS` 用于计算、查询或取得与“elements、By、Tag、名称、NS”相关的操作。调用时要先确认当前状态和 `nsURI`、`localName` 的有效范围；返回类型是 `QDomNodeList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDomNodeList`。
- 参数 `nsURI`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `localName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDomImplementation QDomDocument::implementation() const`

**API 类别：** 成员函数说明

**中文解读：** `QDomDocument::implementation` 用于计算、查询或取得与“implementation”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDomImplementation`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDomImplementation`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDomNode QDomDocument::importNode(const QDomNode &importedNode, bool deep)`

**API 类别：** 成员函数说明

**中文解读：** `QDomDocument::importNode` 用于计算、查询或取得与“import、Node”相关的操作。调用时要先确认当前状态和 `importedNode`、`deep` 的有效范围；返回类型是 `QDomNode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDomNode`。
- 参数 `importedNode`：类型为 `const QDomNode &`。没有默认值，调用时必须提供。传入 `const QDomNode &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `deep`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDomNode::NodeType QDomDocument::nodeType() const`

**API 类别：** 成员函数说明

**中文解读：** `QDomDocument::nodeType` 用于计算、查询或取得与“node、类型”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDomNode::NodeType`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDomNode::NodeType`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] QDomDocument::ParseResult QDomDocument::setContent(QXmlStreamReader *reader, QDomDocument::ParseOptions options = ParseOption::Default)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setContent`。调用它会改变 `QDomDocument` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`QDomDocument::ParseResult`。
- 参数 `reader`：类型为 `QXmlStreamReader *`。没有默认值，调用时必须提供。传入 `QXmlStreamReader *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `options`：类型为 `QDomDocument::ParseOptions`。默认值为 `ParseOption::Default`。传入 `QDomDocument::ParseOptions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QDomDocument::toByteArray(int indent = 1) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toByteArray`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `indent`：类型为 `int`。默认值为 `1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QDomDocument::toString(int indent = 1) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toString`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QString`。
- 参数 `indent`：类型为 `int`。默认值为 `1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDomDocument &QDomDocument::operator=(const QDomDocument &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDomDocument` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDomDocument &`。
- 参数 `other`：类型为 `const QDomDocument &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.5) struct ParseResult`

**API 类别：** 公有类型

**中文解读：** 这是 `QDomDocument` 的 `Parse、结果` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.5) enum class ParseOption { Default, UseNamespaceProcessing, PreserveSpacingOnlyNodes }`

**API 类别：** 公有类型

**中文解读：** 这是 `QDomDocument` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags ParseOptions`

**API 类别：** 公有类型

**中文解读：** 这是 `QDomDocument` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.5) QDomDocument::ParseResult setContent(QAnyStringView text, QDomDocument::ParseOptions options = ParseOption::Default)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setContent`。调用它会改变 `QDomDocument` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`QDomDocument::ParseResult`。
- 参数 `text`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `options`：类型为 `QDomDocument::ParseOptions`。默认值为 `ParseOption::Default`。传入 `QDomDocument::ParseOptions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.5) QDomDocument::ParseResult setContent(QIODevice *device, QDomDocument::ParseOptions options = ParseOption::Default)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setContent`。调用它会改变 `QDomDocument` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`QDomDocument::ParseResult`。
- 参数 `device`：类型为 `QIODevice *`。没有默认值，调用时必须提供。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。
- 参数 `options`：类型为 `QDomDocument::ParseOptions`。默认值为 `ParseOption::Default`。传入 `QDomDocument::ParseOptions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.5) QDomDocument::ParseResult setContent(const QByteArray &data, QDomDocument::ParseOptions options = ParseOption::Default)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setContent`。调用它会改变 `QDomDocument` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`QDomDocument::ParseResult`。
- 参数 `data`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `options`：类型为 `QDomDocument::ParseOptions`。默认值为 `ParseOption::Default`。传入 `QDomDocument::ParseOptions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
