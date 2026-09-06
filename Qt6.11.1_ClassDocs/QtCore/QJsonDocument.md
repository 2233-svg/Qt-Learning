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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QJsonDocument::JsonFormat`

**作用与语义：**

该值定义了使用 `toJson()` 转换为`QJsonDocument`时产生的 JSON 字节数组格式。
- `QJsonDocument::Indented`：`0`;定义人类可读输出如下：
{。
“阵列”： [。
确实，。
999,。
“弦”。
],。
“密钥”：“价值”。
“null”：null。
}。
- `QJsonDocument::Compact`：`1`;定义紧致输出如下：
{“Array”：[true，999，“string”]，“Key”：“Value”，“null”：null}。

### `QJsonDocument::QJsonDocument()`

**作用与语义：**

构造一个空且无效的文档。

### `[explicit] QJsonDocument::QJsonDocument(const QJsonArray &array)`

**作用与语义：**

从`array`构建QJson文档。

### `[explicit] QJsonDocument::QJsonDocument(const QJsonObject &object)`

**作用与语义：**

从`object`创建QJson文档。

### `QJsonDocument::QJsonDocument(const QJsonDocument &other)`

**作用与语义：**

创建`other`文档的副本。

### `[noexcept] QJsonDocument::QJsonDocument(QJsonDocument &&other)`

**作用与语义：**

从`other`移动构造QJson文档。

### `[noexcept] QJsonDocument::~QJsonDocument()`

**作用与语义：**

删除了文档。
带有fromRawData的二进制数据集未被释放。

### `QJsonArray QJsonDocument::array() const`

**作用与语义：**

返回文档中包含的`QJsonArray`。
如果文档包含对象，则返回空数组。

### `[static] QJsonDocument QJsonDocument::fromJson(const QByteArray &json, QJsonParseError *error = nullptr)`

**作用与语义：**

解析`json`为UTF-8编码的JSON文档，并从中生成`QJsonDocument`。
如果解析成功，返回有效（非空）的`QJsonDocument`。如果失败，返回的文档为空，可选的`error`变量将包含关于错误的更多细节。

### `[static] QJsonDocument QJsonDocument::fromVariant(const QVariant &variant)`

**作用与语义：**

从`QVariant` `variant`中产生`QJsonDocument`。
如果`variant`包含除`QVariantMap`、`QVariantHash`、`QVariantList`或`QStringList`以外的任何类型，返回的文档无效。

### `bool QJsonDocument::isArray() const`

**作用与语义：**

如果文档包含数组，返回`true`。

### `bool QJsonDocument::isEmpty() const`

**作用与语义：**

如果文档中没有任何数据，返回`true`。

### `bool QJsonDocument::isNull() const`

**作用与语义：**

如果该文档为空，则返回`true`。
空文档是通过默认构造函数创建的文档。
由UTF-8编码文本或二进制格式创建的文档在解析过程中进行验证。如果验证失败，返回的文档也将为空。

### `bool QJsonDocument::isObject() const`

**作用与语义：**

如果文档包含对象，返回`true`。

### `QJsonObject QJsonDocument::object() const`

**作用与语义：**

返回文档中包含的`QJsonObject`。
如果文档包含数组，则返回空对象。

### `void QJsonDocument::setArray(const QJsonArray &array)`

**作用与语义：**

将`array`设定为本文档的主要对象。

### `void QJsonDocument::setObject(const QJsonObject &object)`

**作用与语义：**

将`object`设定为本文档的主要对象。

### `[noexcept] void QJsonDocument::swap(QJsonDocument &other)`

**作用与语义：**

将此文档与`other`交换。此操作非常快且从未失败。

### `QByteArray QJsonDocument::toJson(QJsonDocument::JsonFormat format = JsonFormat::Indented) const`

**作用与语义：**

将`QJsonDocument`转换为提供的 `format` 中的 UTF-8 编码 JSON 文档。

### `QVariant QJsonDocument::toVariant() const`

**作用与语义：**

返回代表 Json 文档的`QVariant`。
如果文档是`QJsonArray`，返回的变体是`QVariantList`;如果是`QJsonObject`，则是`QVariantMap`。

### `[noexcept] QJsonDocument &QJsonDocument::operator=(QJsonDocument &&other)`

**作用与语义：**

移动-分配 `other` 到该文档。

### `QJsonDocument &QJsonDocument::operator=(const QJsonDocument &other)`

**作用与语义：**

将`other`文档分配给该`QJsonDocument`。返回对该对象的引用。

### `const QJsonValue QJsonDocument::operator[](const QString &key) const`

**作用与语义：**

返回一个表示密钥`key`值的`QJsonValue`。
相当于调用 `object()`.value（key）。
如果密钥不存在，或者`isObject()`为假，返回的`QJsonValue`将被`QJsonValue::Undefined`。

### `const QJsonValue QJsonDocument::operator[](qsizetype i) const`

**作用与语义：**

返回一个`QJsonValue`，表示索引`i`的值。
相当于调用 `array()`.at（i）。
如果`i`出界，或者`isArray()`为假，返回的`QJsonValue`为`QJsonValue::Undefined`。

### `const QJsonValue QJsonDocument::operator[](QLatin1StringView key) const`

**作用与语义：**

返回一个表示密钥`key`值的`QJsonValue`。
相当于调用 `object()`.value（key）。
如果密钥不存在，或者`isObject()`为假，返回的`QJsonValue`将被`QJsonValue::Undefined`。

### `const QJsonValue QJsonDocument::operator[](QStringView key) const`

**作用与语义：**

返回一个表示密钥`key`值的`QJsonValue`。
相当于调用 `object()`.value（key）。
如果密钥不存在，或者`isObject()`为假，返回的`QJsonValue`将被`QJsonValue::Undefined`。

### `[noexcept] bool operator!=(const QJsonDocument &lhs, const QJsonDocument &rhs)`

**作用与语义：**

如果`lhs`文档与`rhs`文档不相等，`false`否则返回`true`。

### `[noexcept] bool operator==(const QJsonDocument &lhs, const QJsonDocument &rhs)`

**作用与语义：**

返回`true`如果`lhs`文档等于`rhs`文件`false`否则。

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
