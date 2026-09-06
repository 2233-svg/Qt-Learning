# QJsonDocument

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QJsonDocument` 是 JSON 文档根容器，负责 JSON 文本与 QJsonObject/QJsonArray 之间的解析和序列化。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QJsonDocument` 是 JSON 文档根容器，负责 JSON 文本与 QJsonObject/QJsonArray 之间的解析和序列化。

**内部模型：** JSON 数据结构是 value -> object/array -> value 的树；QJsonDocument 只负责文档边界，字段访问要通过 QJsonObject/QJsonArray/QJsonValue。解析必须检查 QJsonParseError。

**适用场景：** 配置文件、网络响应、进程间数据交换和序列化轻量对象时使用。复杂二进制或高性能连续数据不应强行使用 JSON。

**典型调用链：** fromJson/fromJson(json, error) -> isObject/isArray -> object/array -> value/type conversion -> toJson。

**先记住的坑：** 缺字段与类型错误要分别处理；toObject/toArray 可能得到空结构；数字在 JSON 中是 double 语义；不要把 parse 成功等同于业务数据有效。

## 2. 依赖与对象关系

- 头文件：`#include <QJsonDocument>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

JSON 数据结构是 value -> object/array -> value 的树；QJsonDocument 只负责文档边界，字段访问要通过 QJsonObject/QJsonArray/QJsonValue。解析必须检查 QJsonParseError。

### 状态、生命周期和线程

**生命周期：** 解析结果通常是值对象，可在作用域内传递；流式解析器则依赖输入设备和读取顺序。解析错误、结构合法和业务字段合法是三个不同层次，必须分别检查。

**状态与结果：** 先判断文档是否为空、根节点类型和解析错误，再访问字段；字段缺失、类型不匹配、空值和默认值要分开处理。序列化时要明确紧凑/格式化输出和编码。

**线程与事件循环：** 值形式的解析结果可以复制后跨线程处理；共享设备、流对象和可变 DOM 不应无保护地跨线程使用。大文档要评估一次性树结构的内存成本，必要时用流式 API。

## 3. 直接使用

配置文件、网络响应、进程间数据交换和序列化轻量对象时使用。复杂二进制或高性能连续数据不应强行使用 JSON。 使用时通常按这个过程组织：fromJson/fromJson(json, error) -> isObject/isArray -> object/array -> value/type conversion -> toJson。

```cpp
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonParseError>

QJsonParseError error;
const QJsonDocument document = QJsonDocument::fromJson(data, &error);
if (error.error == QJsonParseError::NoError && document.isObject()) {
    const QString name = document.object().value("name").toString();
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum JsonFormat { Indented, Compact }`

### 公有函数

- `QJsonDocument()`
- `QJsonDocument(const QJsonArray &array)`
- `QJsonDocument(const QJsonObject &object)`
- `QJsonDocument(const QJsonDocument &other)`
- `QJsonDocument(QJsonDocument &&other)`
- `~QJsonDocument()`
- `QJsonArray array() const`
- `bool isArray() const`
- `bool isEmpty() const`
- `bool isNull() const`
- `bool isObject() const`
- `QJsonObject object() const`
- `void setArray(const QJsonArray &array)`
- `void setObject(const QJsonObject &object)`
- `void swap(QJsonDocument &other)`
- `QByteArray toJson(QJsonDocument::JsonFormat format = JsonFormat::Indented) const`
- `QVariant toVariant() const`
- `QJsonDocument & operator=(QJsonDocument &&other)`
- `QJsonDocument & operator=(const QJsonDocument &other)`
- `const QJsonValue operator[](const QString &key) const`
- `const QJsonValue operator[](qsizetype i) const`
- `const QJsonValue operator[](QLatin1StringView key) const`
- `const QJsonValue operator[](QStringView key) const`

### 静态公有成员

- `QJsonDocument fromJson(const QByteArray &json, QJsonParseError *error = nullptr)`
- `QJsonDocument fromVariant(const QVariant &variant)`

### 相关非成员函数

- `bool operator!=(const QJsonDocument &lhs, const QJsonDocument &rhs)`
- `bool operator==(const QJsonDocument &lhs, const QJsonDocument &rhs)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 28 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QJsonDocument::JsonFormat`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QJsonDocument` 暴露的类型声明 `Json、格式化`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:JsonFormat`。
- 属性名：`QJsonDocument`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJsonDocument::QJsonDocument()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJsonDocument` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QJsonDocument::QJsonDocument(const QJsonArray &array)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJsonDocument` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `array`：类型为 `const QJsonArray &`。没有默认值，调用时必须提供。传入 `const QJsonArray &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QJsonDocument::QJsonDocument(const QJsonObject &object)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJsonDocument` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `object`：类型为 `const QJsonObject &`。没有默认值，调用时必须提供。传入 `const QJsonObject &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJsonDocument::QJsonDocument(const QJsonDocument &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJsonDocument` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QJsonDocument &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QJsonDocument::QJsonDocument(QJsonDocument &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJsonDocument` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `QJsonDocument &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QJsonDocument::~QJsonDocument()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJsonDocument` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJsonArray QJsonDocument::array() const`

**API 类别：** 成员函数说明

**中文解读：** `QJsonDocument::array` 用于计算、查询或取得与“array”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QJsonArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QJsonArray`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QJsonDocument QJsonDocument::fromJson(const QByteArray &json, QJsonParseError *error = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromJson`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QJsonDocument`。
- 参数 `json`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `error`：类型为 `QJsonParseError *`。默认值为 `nullptr`。错误输出对象或错误状态。解析/执行后要检查它，而不能只看主返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QJsonDocument QJsonDocument::fromVariant(const QVariant &variant)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromVariant`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QJsonDocument`。
- 参数 `variant`：类型为 `const QVariant &`。没有默认值，调用时必须提供。传入 `const QVariant &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJsonDocument::isArray() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isArray`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJsonDocument::isEmpty() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isEmpty`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJsonDocument::isNull() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isNull`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJsonDocument::isObject() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isObject`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJsonObject QJsonDocument::object() const`

**API 类别：** 成员函数说明

**中文解读：** `QJsonDocument::object` 用于计算、查询或取得与“object”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QJsonObject`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QJsonObject`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QJsonDocument::setArray(const QJsonArray &array)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setArray`。调用它会改变 `QJsonDocument` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `array`：类型为 `const QJsonArray &`。没有默认值，调用时必须提供。传入 `const QJsonArray &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QJsonDocument::setObject(const QJsonObject &object)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setObject`。调用它会改变 `QJsonDocument` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `object`：类型为 `const QJsonObject &`。没有默认值，调用时必须提供。传入 `const QJsonObject &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QJsonDocument::swap(QJsonDocument &other)`

**API 类别：** 成员函数说明

**中文解读：** `QJsonDocument::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QJsonDocument &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QJsonDocument::toJson(QJsonDocument::JsonFormat format = JsonFormat::Indented) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toJson`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `format`：类型为 `QJsonDocument::JsonFormat`。默认值为 `JsonFormat::Indented`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVariant QJsonDocument::toVariant() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toVariant`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QVariant`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QJsonDocument &QJsonDocument::operator=(QJsonDocument &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJsonDocument` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QJsonDocument &`。
- 参数 `other`：类型为 `QJsonDocument &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJsonDocument &QJsonDocument::operator=(const QJsonDocument &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJsonDocument` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QJsonDocument &`。
- 参数 `other`：类型为 `const QJsonDocument &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QJsonValue QJsonDocument::operator[](const QString &key) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJsonDocument` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`const QJsonValue`。
- 参数 `key`：类型为 `const QString &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QJsonValue QJsonDocument::operator[](qsizetype i) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJsonDocument` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`const QJsonValue`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QJsonValue QJsonDocument::operator[](QLatin1StringView key) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJsonDocument` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`const QJsonValue`。
- 参数 `key`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QJsonValue QJsonDocument::operator[](QStringView key) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJsonDocument` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`const QJsonValue`。
- 参数 `key`：类型为 `QStringView`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator!=(const QJsonDocument &lhs, const QJsonDocument &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QJsonDocument` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QJsonDocument &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QJsonDocument &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator==(const QJsonDocument &lhs, const QJsonDocument &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QJsonDocument` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QJsonDocument &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QJsonDocument &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

解析结果通常是值对象，可在作用域内传递；流式解析器则依赖输入设备和读取顺序。解析错误、结构合法和业务字段合法是三个不同层次，必须分别检查。

### 状态和错误边界

先判断文档是否为空、根节点类型和解析错误，再访问字段；字段缺失、类型不匹配、空值和默认值要分开处理。序列化时要明确紧凑/格式化输出和编码。

### 线程边界

值形式的解析结果可以复制后跨线程处理；共享设备、流对象和可变 DOM 不应无保护地跨线程使用。大文档要评估一次性树结构的内存成本，必要时用流式 API。

### 最容易出现的错误

缺字段与类型错误要分别处理；toObject/toArray 可能得到空结构；数字在 JSON 中是 double 语义；不要把 parse 成功等同于业务数据有效。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QJsonDocument` 所属机制类型：结构化文本解析机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
