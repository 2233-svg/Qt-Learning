# QXmlStreamWriter

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** XML 流式写入器，按开始元素、属性、文本和结束元素顺序生成 XML。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QXmlStreamWriter`：XML 流式写入器，按开始元素、属性、文本和结束元素顺序生成 XML。

**内部模型：** JSON 通常表示为 value/object/array 树，XML 则包含元素、属性、文本和层级。文档容器负责解析和序列化，具体字段/节点访问由 object、array、value 或 DOM/流式读取对象完成。

**适用场景：** 接收字节数据后显式指定编码和解析选项，检查错误对象，再按类型访问节点，校验业务字段，最后序列化或转换成领域对象。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要只检查 parse 成功；不要假设字段一定存在且类型固定；不要把用户输入直接当作可信结构；大文件不要无条件 readAll 和构造整棵树。

## 2. 依赖与对象关系

- 头文件：`#include <QXmlStreamWriter>`
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

- `(since 6.10) enum class Error { None, IO, Encoding, InvalidCharacter, Custom }`

### 属性

- `autoFormatting : bool`
- `autoFormattingIndent : int`
- `(since 6.10) stopWritingOnError : bool`

### 公有函数

- `QXmlStreamWriter()`
- `QXmlStreamWriter(QByteArray *array)`
- `QXmlStreamWriter(QIODevice *device)`
- `QXmlStreamWriter(QString *string)`
- `~QXmlStreamWriter()`
- `bool autoFormatting() const`
- `int autoFormattingIndent() const`
- `QIODevice * device() const`
- `(since 6.10) QXmlStreamWriter::Error error() const`
- `(since 6.10) QString errorString() const`
- `bool hasError() const`
- `(since 6.10) void raiseError(QAnyStringView message)`
- `void setAutoFormatting(bool enable)`
- `void setAutoFormattingIndent(int spacesOrTabs)`
- `void setDevice(QIODevice *device)`
- `void setStopWritingOnError(bool stop)`
- `bool stopWritingOnError() const`
- `void writeAttribute(QAnyStringView namespaceUri, QAnyStringView name, QAnyStringView value)`
- `void writeAttribute(const QXmlStreamAttribute &attribute)`
- `void writeAttribute(QAnyStringView qualifiedName, QAnyStringView value)`
- `void writeAttributes(const QXmlStreamAttributes &attributes)`
- `void writeCDATA(QAnyStringView text)`
- `void writeCharacters(QAnyStringView text)`
- `void writeComment(QAnyStringView text)`
- `void writeCurrentToken(const QXmlStreamReader &reader)`
- `void writeDTD(QAnyStringView dtd)`
- `void writeDefaultNamespace(QAnyStringView namespaceUri)`
- `void writeEmptyElement(QAnyStringView namespaceUri, QAnyStringView name)`
- `void writeEmptyElement(QAnyStringView qualifiedName)`
- `void writeEndDocument()`
- `void writeEndElement()`
- `void writeEntityReference(QAnyStringView name)`
- `void writeNamespace(QAnyStringView namespaceUri, QAnyStringView prefix = {})`
- `void writeProcessingInstruction(QAnyStringView target, QAnyStringView data = {})`
- `void writeStartDocument(QAnyStringView version)`
- `void writeStartDocument(QAnyStringView version, bool standalone)`
- `void writeStartDocument()`
- `void writeStartElement(QAnyStringView namespaceUri, QAnyStringView name)`
- `void writeStartElement(QAnyStringView qualifiedName)`
- `void writeTextElement(QAnyStringView namespaceUri, QAnyStringView name, QAnyStringView text)`
- `void writeTextElement(QAnyStringView qualifiedName, QAnyStringView text)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 45 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[since 6.10] enum class QXmlStreamWriter::Error`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QXmlStreamWriter` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Error`。
- 属性名：`QXmlStreamWriter`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `autoFormatting : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QXmlStreamWriter` 的配置属性。初始化或状态切换时通过 `setAutoFormatting(...)` 设置，之后用 `autoFormatting()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`autoFormatting`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `autoFormattingIndent : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QXmlStreamWriter` 的配置属性。初始化或状态切换时通过 `setAutoFormattingIndent(...)` 设置，之后用 `autoFormattingIndent()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`autoFormattingIndent`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.10] stopWritingOnError : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QXmlStreamWriter` 的配置属性。初始化或状态切换时通过 `setStopWritingOnError(...)` 设置，之后用 `stopWritingOnError()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`stopWritingOnError`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QXmlStreamWriter::QXmlStreamWriter()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamWriter` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QXmlStreamWriter::QXmlStreamWriter(QByteArray *array)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamWriter` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `array`：类型为 `QByteArray *`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QXmlStreamWriter::QXmlStreamWriter(QIODevice *device)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamWriter` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `device`：类型为 `QIODevice *`。没有默认值，调用时必须提供。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QXmlStreamWriter::QXmlStreamWriter(QString *string)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamWriter` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `string`：类型为 `QString *`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QXmlStreamWriter::~QXmlStreamWriter()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamWriter` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QXmlStreamWriter::autoFormatting() const`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamWriter::autoFormatting` 用于计算、查询或取得与“auto、Formatting”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QIODevice *QXmlStreamWriter::device() const`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamWriter::device` 用于计算、查询或取得与“device”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QIODevice *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QIODevice *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.10] QXmlStreamWriter::Error QXmlStreamWriter::error() const`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamWriter::error` 用于计算、查询或取得与“错误”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QXmlStreamWriter::Error`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QXmlStreamWriter::Error`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.10] QString QXmlStreamWriter::errorString() const`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamWriter::errorString` 用于计算、查询或取得与“错误、字符串”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QXmlStreamWriter::hasError() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasError`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.10] void QXmlStreamWriter::raiseError(QAnyStringView message)`

**API 类别：** 成员函数说明

**中文解读：** `QXmlStreamWriter::raiseError` 用于执行与“raise、错误”相关的操作。调用时要先确认当前状态和 `message` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `message`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。传入 `QAnyStringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamWriter::setAutoFormatting(bool enable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAutoFormatting`。调用它会改变 `QXmlStreamWriter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamWriter::setDevice(QIODevice *device)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDevice`。调用它会改变 `QXmlStreamWriter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `device`：类型为 `QIODevice *`。没有默认值，调用时必须提供。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamWriter::writeAttribute(QAnyStringView namespaceUri, QAnyStringView name, QAnyStringView value)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamWriter` 的核心操作 `writeAttribute`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `namespaceUri`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。传入 `QAnyStringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `name`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。
- 参数 `value`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamWriter::writeAttribute(const QXmlStreamAttribute &attribute)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamWriter` 的核心操作 `writeAttribute`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `attribute`：类型为 `const QXmlStreamAttribute &`。没有默认值，调用时必须提供。传入 `const QXmlStreamAttribute &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamWriter::writeAttribute(QAnyStringView qualifiedName, QAnyStringView value)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamWriter` 的核心操作 `writeAttribute`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `qualifiedName`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。传入 `QAnyStringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamWriter::writeAttributes(const QXmlStreamAttributes &attributes)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamWriter` 的核心操作 `writeAttributes`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `attributes`：类型为 `const QXmlStreamAttributes &`。没有默认值，调用时必须提供。传入 `const QXmlStreamAttributes &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamWriter::writeCDATA(QAnyStringView text)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamWriter` 的核心操作 `writeCDATA`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `text`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamWriter::writeCharacters(QAnyStringView text)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamWriter` 的核心操作 `writeCharacters`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `text`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamWriter::writeComment(QAnyStringView text)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamWriter` 的核心操作 `writeComment`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `text`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamWriter::writeCurrentToken(const QXmlStreamReader &reader)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamWriter` 的核心操作 `writeCurrentToken`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `reader`：类型为 `const QXmlStreamReader &`。没有默认值，调用时必须提供。传入 `const QXmlStreamReader &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamWriter::writeDTD(QAnyStringView dtd)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamWriter` 的核心操作 `writeDTD`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `dtd`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。传入 `QAnyStringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamWriter::writeDefaultNamespace(QAnyStringView namespaceUri)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamWriter` 的核心操作 `writeDefaultNamespace`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `namespaceUri`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。传入 `QAnyStringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamWriter::writeEmptyElement(QAnyStringView namespaceUri, QAnyStringView name)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamWriter` 的核心操作 `writeEmptyElement`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `namespaceUri`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。传入 `QAnyStringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `name`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamWriter::writeEmptyElement(QAnyStringView qualifiedName)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamWriter` 的核心操作 `writeEmptyElement`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `qualifiedName`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。传入 `QAnyStringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamWriter::writeEndDocument()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamWriter` 的核心操作 `writeEndDocument`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamWriter::writeEndElement()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamWriter` 的核心操作 `writeEndElement`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamWriter::writeEntityReference(QAnyStringView name)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamWriter` 的核心操作 `writeEntityReference`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `name`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamWriter::writeNamespace(QAnyStringView namespaceUri, QAnyStringView prefix = {})`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamWriter` 的核心操作 `writeNamespace`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `namespaceUri`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。传入 `QAnyStringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `prefix`：类型为 `QAnyStringView`。默认值为 `{}`。传入 `QAnyStringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamWriter::writeProcessingInstruction(QAnyStringView target, QAnyStringView data = {})`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamWriter` 的核心操作 `writeProcessingInstruction`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `data`：类型为 `QAnyStringView`。默认值为 `{}`。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamWriter::writeStartDocument(QAnyStringView version)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamWriter` 的核心操作 `writeStartDocument`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `version`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。传入 `QAnyStringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamWriter::writeStartDocument(QAnyStringView version, bool standalone)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamWriter` 的核心操作 `writeStartDocument`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `version`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。传入 `QAnyStringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `standalone`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamWriter::writeStartDocument()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamWriter` 的核心操作 `writeStartDocument`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamWriter::writeStartElement(QAnyStringView namespaceUri, QAnyStringView name)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamWriter` 的核心操作 `writeStartElement`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `namespaceUri`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。传入 `QAnyStringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `name`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamWriter::writeStartElement(QAnyStringView qualifiedName)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamWriter` 的核心操作 `writeStartElement`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `qualifiedName`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。传入 `QAnyStringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamWriter::writeTextElement(QAnyStringView namespaceUri, QAnyStringView name, QAnyStringView text)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamWriter` 的核心操作 `writeTextElement`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `namespaceUri`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。传入 `QAnyStringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `name`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。
- 参数 `text`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXmlStreamWriter::writeTextElement(QAnyStringView qualifiedName, QAnyStringView text)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXmlStreamWriter` 的核心操作 `writeTextElement`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `qualifiedName`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。传入 `QAnyStringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `text`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int autoFormattingIndent() const`

**API 类别：** 公有函数

**中文解读：** `QXmlStreamWriter::autoFormattingIndent` 用于计算、查询或取得与“auto、Formatting、Indent”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setAutoFormattingIndent(int spacesOrTabs)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setAutoFormattingIndent`。调用它会改变 `QXmlStreamWriter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `spacesOrTabs`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setStopWritingOnError(bool stop)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setStopWritingOnError`。调用它会改变 `QXmlStreamWriter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `stop`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool stopWritingOnError() const`

**API 类别：** 公有函数

**中文解读：** 这是结束/释放/取消 API `stopWritingOnError`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

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

`QXmlStreamWriter` 所属机制类型：结构化文本解析机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
