# QUrlQuery

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** URL 查询参数类型，负责键值对的添加、编码、查找和序列化。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QUrlQuery`：URL 查询参数类型，负责键值对的添加、编码、查找和序列化。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QUrlQuery>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

### 状态、生命周期和线程

**生命周期：** manager 必须在线程事件循环中存活到 reply 完成；reply 完成后读取结果并调用 `deleteLater()`，不能在信号触发前直接释放。请求对象是值类型，reply 才是带有异步状态和资源的对象。

**状态与结果：** 请求成功发出不等于 HTTP 成功，HTTP 状态码成功也不等于业务 JSON 有效。至少分别处理网络错误、HTTP 状态码、响应头、响应体解析和业务字段校验。上传/下载还要处理进度、分段读取和取消。

**线程与事件循环：** QNetworkAccessManager、QNetworkReply 和相关请求应在同一个有事件循环的线程使用。跨线程时把网络对象整体放到目标线程，通过信号传递结果，不要跨线程直接读写 reply。

## 3. 直接使用

创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

```cpp
// manager、reply 和事件循环必须在正确线程中存活。
QNetworkReply *reply = manager->get(request);
connect(reply, &QNetworkReply::finished, this, [reply] {
    const QByteArray body = reply->readAll();
    reply->deleteLater();
});
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QUrlQuery()`
- `QUrlQuery(const QString &queryString)`
- `QUrlQuery(const QUrl &url)`
- `QUrlQuery(std::initializer_list<std::pair<QString, QString>> list)`
- `QUrlQuery(const QUrlQuery &other)`
- `(since 6.5) QUrlQuery(QUrlQuery &&other)`
- `~QUrlQuery()`
- `void addQueryItem(const QString &key, const QString &value)`
- `QStringList allQueryItemValues(const QString &key, QUrl::ComponentFormattingOptions encoding = QUrl::PrettyDecoded) const`
- `void clear()`
- `bool hasQueryItem(const QString &key) const`
- `bool isEmpty() const`
- `QString query(QUrl::ComponentFormattingOptions encoding = QUrl::PrettyDecoded) const`
- `QString queryItemValue(const QString &key, QUrl::ComponentFormattingOptions encoding = QUrl::PrettyDecoded) const`
- `QList<std::pair<QString, QString>> queryItems(QUrl::ComponentFormattingOptions encoding = QUrl::PrettyDecoded) const`
- `QChar queryPairDelimiter() const`
- `QChar queryValueDelimiter() const`
- `void removeAllQueryItems(const QString &key)`
- `void removeQueryItem(const QString &key)`
- `void setQuery(const QString &queryString)`
- `void setQueryDelimiters(QChar valueDelimiter, QChar pairDelimiter)`
- `void setQueryItems(const QList<std::pair<QString, QString>> &query)`
- `void swap(QUrlQuery &other)`
- `QString toString(QUrl::ComponentFormattingOptions encoding = QUrl::PrettyDecoded) const`
- `QUrlQuery & operator=(QUrlQuery &&other)`
- `QUrlQuery & operator=(const QUrlQuery &other)`

### 静态公有成员

- `char16_t defaultQueryPairDelimiter()`
- `char16_t defaultQueryValueDelimiter()`

### 相关非成员函数

- `size_t qHash(const QUrlQuery &key, size_t seed = 0)`
- `bool operator!=(const QUrlQuery &lhs, const QUrlQuery &rhs)`
- `bool operator==(const QUrlQuery &lhs, const QUrlQuery &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QUrlQuery::QUrlQuery()`

**作用与语义：**

构造一个空的QUrlQuery对象。查询可以通过调用`setQuery()`设置，或通过使用`addQueryItem()`添加项。

### `[explicit] QUrlQuery::QUrlQuery(const QString &queryString)`

**作用与语义：**

构建一个QUrlQuery对象，并用默认的查询分隔符解析`queryString`查询字符串。要解析使用其他分隔符的查询字符串，你应该先用`setQueryDelimiters()`设置它们，然后用`setQuery()`设置查询。

### `[explicit] QUrlQuery::QUrlQuery(const QUrl &url)`

**作用与语义：**

构建一个QUrlQuery对象，并用默认的查询分隔符解析`url` URL中的查询字符串。要解析使用其他分隔符的查询字符串，你应该先用`setQueryDelimiters()`设置它们，然后用`setQuery()`设置查询。

### `QUrlQuery::QUrlQuery(std::initializer_list<std::pair<QString, QString>> list)`

**作用与语义：**

从键值对的`list`构造一个QUrlQuery对象。

### `QUrlQuery::QUrlQuery(const QUrlQuery &other)`

**作用与语义：**

复制`other` QUrlQuery 对象的内容，包括查询分隔符。

### `[noexcept, since 6.5] QUrlQuery::QUrlQuery(QUrlQuery &&other)`

**作用与语义：**

移动`other` QUrlQuery 对象的内容，包括查询分隔符。

### `[noexcept] QUrlQuery::~QUrlQuery()`

**作用与语义：**

摧毁了这个`QUrlQuery`物体。

### `void QUrlQuery::addQueryItem(const QString &key, const QString &value)`

**作用与语义：**

在查询字符串末尾附加对 `key` = `value`。该方法不会覆盖可能存在的相同键的现有项目。
注意：该方法不像HTML表单那样将空格（ASCII 0x20）和加号（“”）视为同一符号。如果你需要用加号表示空格，请使用实际的加号。
注意：键和值字符串应为百分比编码形式。如果输入编码不当，该函数会尝试恢复，但这可能导致数据丢失。更多信息请参见QUrlQuery#编码。

### `QStringList QUrlQuery::allQueryItemValues(const QString &key, QUrl::ComponentFormattingOptions encoding = QUrl::PrettyDecoded) const`

**作用与语义：**

返回一个查询字符串的值列表，其键等于URL的`key`，使用`encoding`中指定的选项编码返回值。如果找不到键`key`，该函数返回一个空列表。
注意：密钥应为百分比编码形式。该函数会尝试恢复，但可能导致数据丢失。更多信息请参见QUrlQuery#编码。

### `void QUrlQuery::clear()`

**作用与语义：**

通过移除当前存储的所有键值对来清除该`QUrlQuery`对象。如果查询分隔符被更改，该函数会保留其更改后的值。

### `[static constexpr noexcept] char16_t QUrlQuery::defaultQueryPairDelimiter()`

**作用与语义：**

返回用于分隔键值对的默认字符，即一个&符号（“&”）。
注：在第6题之前，该函数返回`QChar`。

### `[static constexpr noexcept] char16_t QUrlQuery::defaultQueryValueDelimiter()`

**作用与语义：**

返回查询中分隔键与值的默认字符，等号（“=”）。
注：在Qt 6之前，该函数返回`QChar`。

### `bool QUrlQuery::hasQueryItem(const QString &key) const`

**作用与语义：**

如果存在一对查询字符串，其键等于 URL 的 `key`，则返回 `true`。
注意：密钥预计为百分比编码形式。如果输入编码不当，该函数会尝试恢复，但这可能导致数据丢失。更多信息请参见 QUrlQuery#Encoding 。

### `bool QUrlQuery::isEmpty() const`

**作用与语义：**

如果该`QUrlQuery`对象没有键值对，例如默认构造后或解析空查询字符串后，返回`true`。

### `QString QUrlQuery::query(QUrl::ComponentFormattingOptions encoding = QUrl::PrettyDecoded) const`

**作用与语义：**

返回由当前存储在该`QUrlQuery`对象中的键值对组成的重构查询字符串，并由该对象所选的查询分隔符分隔。键和值通过`encoding`参数给出的选项进行编码。
对于该功能，唯一歧义的分隔符是哈希（“#”），在URL中用来区分查询字符串与后续片段。
返回字符串中键值对的顺序与原始查询完全相同。

### `QString QUrlQuery::queryItemValue(const QString &key, QUrl::ComponentFormattingOptions encoding = QUrl::PrettyDecoded) const`

**作用与语义：**

从URL返回与键`key`关联的查询值，使用`encoding`中指定的选项编码返回值。如果找不到键`key`，该函数返回空字符串。如果你需要区分空值和不存在的键，应先用`hasQueryItem()`检查键的存在。
如果键`key`是乘法定义的，该函数将返回第一个找到的键，顺序是查询字符串中出现的或通过`addQueryItem()`添加的顺序。
注意：密钥应为百分比编码形式。该函数会尝试恢复，但可能导致数据丢失。更多信息请参见QUrlQuery#编码。

### `QList<std::pair<QString, QString>> QUrlQuery::queryItems(QUrl::ComponentFormattingOptions encoding = QUrl::PrettyDecoded) const`

**作用与语义：**

返回URL的查询字符串，作为键和值的映射，使用`encoding`中指定的选项编码这些项。元素的顺序与查询字符串中或带有`setQueryItems()`的集合相同。

### `QChar QUrlQuery::queryPairDelimiter() const`

**作用与语义：**

在`query()`中重建查询字符串或在`setQuery()`中解析时，返回用于分隔键值对的字符。

### `QChar QUrlQuery::queryValueDelimiter() const`

**作用与语义：**

在`query()`中重建查询字符串或在`setQuery()`中解析时，返回用于分隔键和值的字符。

### `void QUrlQuery::removeAllQueryItems(const QString &key)`

**作用与语义：**

移除所有键为 `key` 的查询字符串对从 URL 中移除。
注意：密钥应为百分比编码形式。该函数会尝试恢复，但可能导致数据丢失。更多信息请参见QUrlQuery#编码。

### `void QUrlQuery::removeQueryItem(const QString &key)`

**作用与语义：**

从URL中移除键为`key`的查询字符串对。如果有多个键为`key`的项，则移除查询字符串中出现顺序中的第一个项，顺序是它们在查询字符串中出现或与`addQueryItem()`相连的。
注意：密钥应为百分比编码形式。该函数会尝试恢复，但可能导致数据丢失。更多信息请参见QUrlQuery#编码。

### `void QUrlQuery::setQuery(const QString &queryString)`

**作用与语义：**

解析查询字符串，`queryString`并将内部项设置为其中的值。如果用`setQueryDelimiters()`指定了任何分隔符，该函数将使用它们代替默认分隔符来解析字符串。

### `void QUrlQuery::setQueryDelimiters(QChar valueDelimiter, QChar pairDelimiter)`

**作用与语义：**

设置用于分隔键和值之间，以及 URL 查询字符串中键值对之间的字符。默认值分隔符为 '='，默认对分隔符为 '&'。
`valueDelimiter`用于分隔键与值，`pairDelimiter`用于分隔键值对。在查询字符串的键和值编码表示中出现的任何分隔字符，返回`query()`时均为百分比编码。
如果`valueDelimiter`设置为“，`pairDelimiter`为”;“，则上述查询字符串将改为如下表示：
注意：非标准分隔符应从RFC 3986所称的“子分隔符”中选择。它们包括：
不支持使用其他字符，可能导致意外行为。此方法无法验证你是否通过了有效的分隔符。

**官方示例：**

```cpp
  http://www.example.com/cgi-bin/drawgraph.cgi?type,pie;color,green
```

### `void QUrlQuery::setQueryItems(const QList<std::pair<QString, QString>> &query)`

**作用与语义：**

将该`QUrlQuery`对象中的元素设置为`query`。`query`中元素的顺序保持不变。
注意：该方法不像HTML表单那样将空格（ASCII 0x20）和加号（“”）视为同一符号。如果你需要用加号表示空格，请使用实际的加号。
注意：键和值应为百分比编码形式。如果输入编码不当，该函数会尝试恢复，但这可能导致数据丢失。更多信息请参见 QUrlQuery#Encoding 。

### `[noexcept] void QUrlQuery::swap(QUrlQuery &other)`

**作用与语义：**

将该URL查询实例与`other`交换。该操作非常快速且从未失败。

### `QString QUrlQuery::toString(QUrl::ComponentFormattingOptions encoding = QUrl::PrettyDecoded) const`

**作用与语义：**

返回该`QUrlQuery`作为`QString`。`encoding`可用于指定返回值的URL字符串编码。

### `[noexcept] QUrlQuery &QUrlQuery::operator=(QUrlQuery &&other)`

**作用与语义：**

移动分配`other`到该`QUrlQuery`实例。

### `QUrlQuery &QUrlQuery::operator=(const QUrlQuery &other)`

**作用与语义：**

复制`other` `QUrlQuery`对象的内容，包括查询分隔符。

### `[noexcept] size_t qHash(const QUrlQuery &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[noexcept] bool operator!=(const QUrlQuery &lhs, const QUrlQuery &rhs)`

**作用与语义：**

如果 `QUrlQuery` 对象 `rhs` 不等于 `lhs`，则返回 `true`。否则，返回 `false`。

### `[noexcept] bool operator==(const QUrlQuery &lhs, const QUrlQuery &rhs)`

**作用与语义：**

如果 `QUrlQuery` 对象和 `rhs` 包含相同内容、顺序相同，并使用相同的查询分隔符，则返回 `lhs`。

## 6. 深入实践与常见坑

### 生命周期和资源边界

manager 必须在线程事件循环中存活到 reply 完成；reply 完成后读取结果并调用 `deleteLater()`，不能在信号触发前直接释放。请求对象是值类型，reply 才是带有异步状态和资源的对象。

### 状态和错误边界

请求成功发出不等于 HTTP 成功，HTTP 状态码成功也不等于业务 JSON 有效。至少分别处理网络错误、HTTP 状态码、响应头、响应体解析和业务字段校验。上传/下载还要处理进度、分段读取和取消。

### 线程边界

QNetworkAccessManager、QNetworkReply 和相关请求应在同一个有事件循环的线程使用。跨线程时把网络对象整体放到目标线程，通过信号传递结果，不要跨线程直接读写 reply。

### 最容易出现的错误

不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QUrlQuery` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
