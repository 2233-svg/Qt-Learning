# QXmlStreamReader

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** XML 流式读取器，按令牌顺序读取 XML，适合大文件和低内存解析。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QXmlStreamReader`：XML 流式读取器，按令牌顺序读取 XML，适合大文件和低内存解析。

**内部模型：** JSON 通常表示为 value/object/array 树，XML 则包含元素、属性、文本和层级。文档容器负责解析和序列化，具体字段/节点访问由 object、array、value 或 DOM/流式读取对象完成。

**适用场景：** 接收字节数据后显式指定编码和解析选项，检查错误对象，再按类型访问节点，校验业务字段，最后序列化或转换成领域对象。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要只检查 parse 成功；不要假设字段一定存在且类型固定；不要把用户输入直接当作可信结构；大文件不要无条件 readAll 和构造整棵树。

## 2. 依赖与对象关系

- 头文件：`#include <QXmlStreamReader>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

JSON 通常表示为 value/object/array 树，XML 则包含元素、属性、文本和层级。文档容器负责解析和序列化，具体字段/节点访问由 object、array、value 或 DOM/流式读取对象完成。

### 状态、生命周期和线程

**生命周期：** 解析结果通常是值对象，可在作用域内传递；流式解析器则依赖输入设备和读取顺序。解析错误、结构合法和业务字段合法是三个不同层次，必须分别检查。

**状态与结果：** 先判断文档是否为空、根节点类型和解析错误，再访问字段；字段缺失、类型不匹配、空值和默认值要分开处理。序列化时要明确紧凑/格式化输出和编码。

**线程与事件循环：** 值形式的解析结果可以复制后跨线程处理；共享设备、流对象和可变 DOM 不应无保护地跨线程使用。大文档要评估一次性树结构的内存成本，必要时用流式 API。

## 3. 直接使用

接收字节数据后显式指定编码和解析选项，检查错误对象，再按类型访问节点，校验业务字段，最后序列化或转换成领域对象。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum Error { NoError, CustomError, NotWellFormedError, PrematureEndOfDocumentError, UnexpectedElementError }`
- `enum ReadElementTextBehaviour { ErrorOnUnexpectedElement, IncludeChildElements, SkipChildElements }`
- `enum TokenType { NoToken, Invalid, StartDocument, EndDocument, StartElement, …, ProcessingInstruction }`

### 属性

- `namespaceProcessing : bool`

### 公有函数

- `QXmlStreamReader()`
- `QXmlStreamReader(QAnyStringView data)`
- `QXmlStreamReader(QIODevice *device)`
- `QXmlStreamReader(const QByteArray &data)`
- `~QXmlStreamReader()`
- `void addData(QAnyStringView data)`
- `void addData(const QByteArray &data)`
- `void addExtraNamespaceDeclaration(const QXmlStreamNamespaceDeclaration &extraNamespaceDeclaration)`
- `void addExtraNamespaceDeclarations(const QXmlStreamNamespaceDeclarations &extraNamespaceDeclarations)`
- `bool atEnd() const`
- `QXmlStreamAttributes attributes() const`
- `qint64 characterOffset() const`
- `void clear()`
- `qint64 columnNumber() const`
- `QIODevice * device() const`
- `QStringView documentEncoding() const`
- `QStringView documentVersion() const`
- `QStringView dtdName() const`
- `QStringView dtdPublicId() const`
- `QStringView dtdSystemId() const`
- `QXmlStreamEntityDeclarations entityDeclarations() const`
- `int entityExpansionLimit() const`
- `QXmlStreamEntityResolver * entityResolver() const`
- `QXmlStreamReader::Error error() const`
- `QString errorString() const`
- `bool hasError() const`
- `(since 6.6) bool hasStandaloneDeclaration() const`
- `bool isCDATA() const`
- `bool isCharacters() const`
- `bool isComment() const`
- `bool isDTD() const`
- `bool isEndDocument() const`
- `bool isEndElement() const`
- `bool isEntityReference() const`
- `bool isProcessingInstruction() const`
- `bool isStandaloneDocument() const`
- `bool isStartDocument() const`
- `bool isStartElement() const`
- `bool isWhitespace() const`
- `qint64 lineNumber() const`
- `QStringView name() const`
- `QXmlStreamNamespaceDeclarations namespaceDeclarations() const`
- `bool namespaceProcessing() const`
- `QStringView namespaceUri() const`
- `QXmlStreamNotationDeclarations notationDeclarations() const`
- `QStringView prefix() const`
- `QStringView processingInstructionData() const`
- `QStringView processingInstructionTarget() const`
- `QStringView qualifiedName() const`
- `void raiseError(const QString &message = QString())`
- `QString readElementText(QXmlStreamReader::ReadElementTextBehaviour behaviour = ErrorOnUnexpectedElement)`
- `QXmlStreamReader::TokenType readNext()`
- `bool readNextStartElement()`
- `(since 6.10) QString readRawInnerData()`
- `void setDevice(QIODevice *device)`
- `void setEntityExpansionLimit(int limit)`
- `void setEntityResolver(QXmlStreamEntityResolver *resolver)`
- `void setNamespaceProcessing(bool)`
- `void skipCurrentElement()`
- `QStringView text() const`
- `QString tokenString() const`
- `QXmlStreamReader::TokenType tokenType() const`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 66 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QXmlStreamReader::Error`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QXmlStreamReader` 暴露的类型声明 `错误`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Error`。
- 属性名：`QXmlStreamReader`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QXmlStreamReader::ReadElementTextBehaviour`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QXmlStreamReader` 暴露的类型声明 `读取、Element、文本、Behaviour`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ReadElementTextBehaviour`。
- 属性名：`QXmlStreamReader`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QXmlStreamReader::TokenType`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QXmlStreamReader` 暴露的类型声明 `Token、类型`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:TokenType`。
- 属性名：`QXmlStreamReader`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `namespaceProcessing : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QXmlStreamReader` 的配置属性。初始化或状态切换时通过 `setNamespaceProcessing(...)` 设置，之后用 `namespaceProcessing()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`namespaceProcessing`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QXmlStreamReader::QXmlStreamReader()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamReader` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QXmlStreamReader::QXmlStreamReader(QAnyStringView data)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamReader` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `data`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QXmlStreamReader::QXmlStreamReader(QIODevice *device)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamReader` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `device`：类型为 `QIODevice *`。没有默认值，调用时必须提供。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QXmlStreamReader::QXmlStreamReader(const QByteArray &data)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamReader` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `data`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QXmlStreamReader::~QXmlStreamReader()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamReader` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamReader::addData(QAnyStringView data)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QXmlStreamReader` 添加依赖、数据或子对象的 API `addData`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `data`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamReader::addData(const QByteArray &data)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QXmlStreamReader` 添加依赖、数据或子对象的 API `addData`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `data`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamReader::addExtraNamespaceDeclaration(const QXmlStreamNamespaceDeclaration &extraNamespaceDeclaration)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QXmlStreamReader` 添加依赖、数据或子对象的 API `addExtraNamespaceDeclaration`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `extraNamespaceDeclaration`：类型为 `const QXmlStreamNamespaceDeclaration &`。没有默认值，调用时必须提供。传入 `const QXmlStreamNamespaceDeclaration &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamReader::addExtraNamespaceDeclarations(const QXmlStreamNamespaceDeclarations &extraNamespaceDeclarations)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QXmlStreamReader` 添加依赖、数据或子对象的 API `addExtraNamespaceDeclarations`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `extraNamespaceDeclarations`：类型为 `const QXmlStreamNamespaceDeclarations &`。没有默认值，调用时必须提供。传入 `const QXmlStreamNamespaceDeclarations &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QXmlStreamReader::atEnd() const`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamReader::atEnd` 用于计算、查询或取得与“按位置访问、结束”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QXmlStreamAttributes QXmlStreamReader::attributes() const`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamReader::attributes` 用于计算、查询或取得与“attributes”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QXmlStreamAttributes`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QXmlStreamAttributes`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QXmlStreamReader::characterOffset() const`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamReader::characterOffset` 用于计算、查询或取得与“character、Offset”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamReader::clear()`

**API 类别：** 成员函数说明

**中文解读：** 这是状态清理或重置 API `clear`。调用后原有数据、索引、缓存或绑定可能失效；使用前先确认它影响的是当前对象、子对象还是底层共享资源，之后重新检查状态。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QXmlStreamReader::columnNumber() const`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamReader::columnNumber` 用于计算、查询或取得与“列、Number”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QIODevice *QXmlStreamReader::device() const`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamReader::device` 用于计算、查询或取得与“device”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QIODevice *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QIODevice *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringView QXmlStreamReader::documentEncoding() const`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamReader::documentEncoding` 用于计算、查询或取得与“document、Encoding”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStringView`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringView`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringView QXmlStreamReader::documentVersion() const`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamReader::documentVersion` 用于计算、查询或取得与“document、Version”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStringView`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringView`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringView QXmlStreamReader::dtdName() const`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamReader::dtdName` 用于计算、查询或取得与“dtd、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStringView`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringView`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringView QXmlStreamReader::dtdPublicId() const`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamReader::dtdPublicId` 用于计算、查询或取得与“dtd、Public、Id”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStringView`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringView`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringView QXmlStreamReader::dtdSystemId() const`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamReader::dtdSystemId` 用于计算、查询或取得与“dtd、System、Id”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStringView`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringView`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QXmlStreamEntityDeclarations QXmlStreamReader::entityDeclarations() const`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamReader::entityDeclarations` 用于计算、查询或取得与“entity、Declarations”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QXmlStreamEntityDeclarations`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QXmlStreamEntityDeclarations`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QXmlStreamReader::entityExpansionLimit() const`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamReader::entityExpansionLimit` 用于计算、查询或取得与“entity、Expansion、Limit”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QXmlStreamEntityResolver *QXmlStreamReader::entityResolver() const`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamReader::entityResolver` 用于计算、查询或取得与“entity、Resolver”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QXmlStreamEntityResolver *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QXmlStreamEntityResolver *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QXmlStreamReader::Error QXmlStreamReader::error() const`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamReader::error` 用于计算、查询或取得与“错误”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QXmlStreamReader::Error`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QXmlStreamReader::Error`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QXmlStreamReader::errorString() const`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamReader::errorString` 用于计算、查询或取得与“错误、字符串”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QXmlStreamReader::hasError() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasError`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] bool QXmlStreamReader::hasStandaloneDeclaration() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasStandaloneDeclaration`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QXmlStreamReader::isCDATA() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isCDATA`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QXmlStreamReader::isCharacters() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isCharacters`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QXmlStreamReader::isComment() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isComment`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QXmlStreamReader::isDTD() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isDTD`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QXmlStreamReader::isEndDocument() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isEndDocument`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QXmlStreamReader::isEndElement() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isEndElement`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QXmlStreamReader::isEntityReference() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isEntityReference`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QXmlStreamReader::isProcessingInstruction() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isProcessingInstruction`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QXmlStreamReader::isStandaloneDocument() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isStandaloneDocument`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QXmlStreamReader::isStartDocument() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isStartDocument`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QXmlStreamReader::isStartElement() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isStartElement`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QXmlStreamReader::isWhitespace() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isWhitespace`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QXmlStreamReader::lineNumber() const`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamReader::lineNumber` 用于计算、查询或取得与“行、Number”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringView QXmlStreamReader::name() const`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamReader::name` 用于计算、查询或取得与“名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStringView`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringView`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QXmlStreamNamespaceDeclarations QXmlStreamReader::namespaceDeclarations() const`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamReader::namespaceDeclarations` 用于计算、查询或取得与“namespace、Declarations”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QXmlStreamNamespaceDeclarations`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QXmlStreamNamespaceDeclarations`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringView QXmlStreamReader::namespaceUri() const`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamReader::namespaceUri` 用于计算、查询或取得与“namespace、Uri”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStringView`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringView`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QXmlStreamNotationDeclarations QXmlStreamReader::notationDeclarations() const`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamReader::notationDeclarations` 用于计算、查询或取得与“notation、Declarations”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QXmlStreamNotationDeclarations`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QXmlStreamNotationDeclarations`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringView QXmlStreamReader::prefix() const`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamReader::prefix` 用于计算、查询或取得与“prefix”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStringView`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringView`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringView QXmlStreamReader::processingInstructionData() const`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamReader::processingInstructionData` 用于计算、查询或取得与“processing、Instruction、数据访问”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStringView`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringView`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringView QXmlStreamReader::processingInstructionTarget() const`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamReader::processingInstructionTarget` 用于计算、查询或取得与“processing、Instruction、目标”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStringView`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringView`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringView QXmlStreamReader::qualifiedName() const`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamReader::qualifiedName` 用于计算、查询或取得与“qualified、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStringView`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringView`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamReader::raiseError(const QString &message = QString())`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamReader::raiseError` 用于执行与“raise、错误”相关的操作。调用时要先确认当前状态和 `message` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `message`：类型为 `const QString &`。默认值为 `QString()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QXmlStreamReader::readElementText(QXmlStreamReader::ReadElementTextBehaviour behaviour = ErrorOnUnexpectedElement)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamReader` 的核心操作 `readElementText`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QString`。
- 参数 `behaviour`：类型为 `QXmlStreamReader::ReadElementTextBehaviour`。默认值为 `ErrorOnUnexpectedElement`。传入 `QXmlStreamReader::ReadElementTextBehaviour` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QXmlStreamReader::TokenType QXmlStreamReader::readNext()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamReader` 的核心操作 `readNext`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QXmlStreamReader::TokenType`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QXmlStreamReader::readNextStartElement()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamReader` 的核心操作 `readNextStartElement`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.10] QString QXmlStreamReader::readRawInnerData()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamReader` 的核心操作 `readRawInnerData`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamReader::setDevice(QIODevice *device)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDevice`。调用它会改变 `QXmlStreamReader` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `device`：类型为 `QIODevice *`。没有默认值，调用时必须提供。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamReader::setEntityExpansionLimit(int limit)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setEntityExpansionLimit`。调用它会改变 `QXmlStreamReader` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `limit`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamReader::setEntityResolver(QXmlStreamEntityResolver *resolver)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setEntityResolver`。调用它会改变 `QXmlStreamReader` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `resolver`：类型为 `QXmlStreamEntityResolver *`。没有默认值，调用时必须提供。传入 `QXmlStreamEntityResolver *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamReader::skipCurrentElement()`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamReader::skipCurrentElement` 用于执行与“skip、当前、Element”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringView QXmlStreamReader::text() const`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamReader::text` 用于计算、查询或取得与“文本”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStringView`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringView`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QXmlStreamReader::tokenString() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `tokenString`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QXmlStreamReader::TokenType QXmlStreamReader::tokenType() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `tokenType`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QXmlStreamReader::TokenType`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool namespaceProcessing() const`

**API 类别：** 公有函数

**中文解读：** `QXmlStreamReader::namespaceProcessing` 用于计算、查询或取得与“namespace、Processing”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setNamespaceProcessing(bool)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setNamespaceProcessing`。调用它会改变 `QXmlStreamReader` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `bool`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

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

`QXmlStreamReader` 所属机制类型：结构化文本解析机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
