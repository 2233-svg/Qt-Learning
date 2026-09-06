# QFormDataBuilder

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QFormDataBuilder` 是 Qt Network 的“Form数据Builder”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QFormDataBuilder` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QFormDataBuilder>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Network)
target_link_libraries(mytarget PRIVATE Qt6::Network)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

### 状态、生命周期和线程

**生命周期：** manager 必须在线程事件循环中存活到 reply 完成；reply 完成后读取结果并调用 `deleteLater()`，不能在信号触发前直接释放。请求对象是值类型，reply 才是带有异步状态和资源的对象。

**状态与结果：** 请求成功发出不等于 HTTP 成功，HTTP 状态码成功也不等于业务 JSON 有效。至少分别处理网络错误、HTTP 状态码、响应头、响应体解析和业务字段校验。上传/下载还要处理进度、分段读取和取消。

**线程与事件循环：** QNetworkAccessManager、QNetworkReply 和相关请求应在同一个有事件循环的线程使用。跨线程时把网络对象整体放到目标线程，通过信号传递结果，不要跨线程直接读写 reply。

## 3. 直接使用

创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum class Option { Default, OmitRfc8187EncodedFilename, UseRfc7578PercentEncodedFilename, PreferLatin1EncodedFilename, StrictRfc7578 }`
- `flags Options`

### 公有函数

- `QFormDataBuilder()`
- `QFormDataBuilder(QFormDataBuilder &&other)`
- `~QFormDataBuilder()`
- `std::unique_ptr<QHttpMultiPart> buildMultiPart(QFormDataBuilder::Options options = {})`
- `QFormDataPartBuilder part(QAnyStringView name)`
- `QFormDataBuilder & operator=(QFormDataBuilder &&other)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum class QFormDataBuilder::Optionflags QFormDataBuilder::Options`

**作用与语义：**

控制 `buildMultiPart()` 的选项。
当前有几个 RFC 对如何精确格式化 `multipart/form-data` 存在分歧。为了避免硬编码任何单一 RFC，这些选项允许您控制遵循哪个 RFC。
- `QFormDataBuilder::Option::Default`: `0x00`；默认值，旨在最大化常规互操作性。下面列出的所有选项都是关闭的。
- `QFormDataBuilder::Option::OmitRfc8187EncodedFilename`: `0x01`；当一个主体部分的文件名包含非 US-ASCII 字符时，RFC 6266 第 4.3 节建议使用 RFC 8187 风格的编码 (`filename*=utf-8''...`)。然而，更近期的 RFC 7578 第 4.2 节禁止使用该机制。截至本文撰写时，这两个 RFC 都是当前有效的，因此此选项允许您选择遵循哪一个。默认情况下，将包含 RFC 8187 编码的 `filename*` 以及未编码的 `filename`，如 RFC 6266 所建议。
- `QFormDataBuilder::Option::UseRfc7578PercentEncodedFilename`: `0x02`；当一个主体部分的文件名包含非 US-ASCII 字符时，RFC 7578 第 4.2 节建议对 UTF-8 编码的文件名的八位字节进行百分比编码。它还指出，许多实现实际上并不对 UTF-8 编码的文件名进行百分比编码，而只是输出“原始” UTF-8（`"` 和 `\` 使用 `\` 转义）。这也是 `QFormDataBuilder` 的默认设置。
- `QFormDataBuilder::Option::PreferLatin1EncodedFilename`: `0x04`；RFC 5987 第 3.2 节要求接收者支持 ISO-8859-1（"Latin-1"）编码。当一个主体部分的文件名包含非 US-ASCII 字符，但可以归入 Latin-1 时，此选项优先使用 ISO-8859-1 编码而不是 UTF-8。更近期的 {https://datatracker.ietf.org/doc/html/rfc8187#appendix-A}{RFC 8187} 不再要求支持 ISO-8859-1，因此默认情况下所有非 US-ASCII 文件名都以 UTF-8 编码发送。
- `QFormDataBuilder::Option::StrictRfc7578`: `OmitRfc8187EncodedFilename | UseRfc7578PercentEncodedFilename`；此选项组合其他选项以选择严格的 RFC 7578 合规性。
Options 类型是 QFlags<Option> 的 typedef。它存储 Option 值的 OR 组合。

### `QFormDataBuilder::QFormDataBuilder()`

**作用与语义：**

构造一个空的 QFormDataBuilder 对象。

### `[noexcept] QFormDataBuilder::QFormDataBuilder(QFormDataBuilder &&other)`

**作用与语义：**

Move构造一个QFormDataBuilder实例，使其指向`other`指向的同一个对象。

### `[noexcept] QFormDataBuilder::~QFormDataBuilder()`

**作用与语义：**

摧毁`QFormDataBuilder`物体。

### `std::unique_ptr<QHttpMultiPart> QFormDataBuilder::buildMultiPart(QFormDataBuilder::Options options = {})`

**作用与语义：**

构造并返回指向根据`options`构造的QHttpMultipart对象的指针。

### `QFormDataPartBuilder QFormDataBuilder::part(QAnyStringView name)`

**作用与语义：**

返回一个新构建的`QFormDataPartBuilder`对象，使用`name`作为表单数据的`name`参数。只要关联的 `QFormDataBuilder` 未被销毁，该对象有效。
出于互操作性，强烈建议将`name`字符限制为 US-ASCII。

### `[noexcept] QFormDataBuilder &QFormDataBuilder::operator=(QFormDataBuilder &&other)`

**作用与语义：**

Move-assign `other`到该`QFormDataBuilder`实例。

### `enum class Option { Default, OmitRfc8187EncodedFilename, UseRfc7578PercentEncodedFilename, PreferLatin1EncodedFilename, StrictRfc7578 }`

**作用与语义：**

控制 `buildMultiPart()` 的选项。
当前有几个 RFC 对如何精确格式化 `multipart/form-data` 存在分歧。为了避免硬编码任何单一 RFC，这些选项允许您控制遵循哪个 RFC。
- `QFormDataBuilder::Option::Default`: `0x00`；默认值，旨在最大化常规互操作性。下面列出的所有选项都是关闭的。
- `QFormDataBuilder::Option::OmitRfc8187EncodedFilename`: `0x01`；当一个主体部分的文件名包含非 US-ASCII 字符时，RFC 6266 第 4.3 节建议使用 RFC 8187 风格的编码 (`filename*=utf-8''...`)。然而，更近期的 RFC 7578 第 4.2 节禁止使用该机制。截至本文撰写时，这两个 RFC 都是当前有效的，因此此选项允许您选择遵循哪一个。默认情况下，将包含 RFC 8187 编码的 `filename*` 以及未编码的 `filename`，如 RFC 6266 所建议。
- `QFormDataBuilder::Option::UseRfc7578PercentEncodedFilename`: `0x02`；当一个主体部分的文件名包含非 US-ASCII 字符时，RFC 7578 第 4.2 节建议对 UTF-8 编码的文件名的八位字节进行百分比编码。它还指出，许多实现实际上并不对 UTF-8 编码的文件名进行百分比编码，而只是输出“原始” UTF-8（`"` 和 `\` 使用 `\` 转义）。这也是 `QFormDataBuilder` 的默认设置。
- `QFormDataBuilder::Option::PreferLatin1EncodedFilename`: `0x04`；RFC 5987 第 3.2 节要求接收者支持 ISO-8859-1（"Latin-1"）编码。当一个主体部分的文件名包含非 US-ASCII 字符，但可以归入 Latin-1 时，此选项优先使用 ISO-8859-1 编码而不是 UTF-8。更近期的 {https://datatracker.ietf.org/doc/html/rfc8187#appendix-A}{RFC 8187} 不再要求支持 ISO-8859-1，因此默认情况下所有非 US-ASCII 文件名都以 UTF-8 编码发送。
- `QFormDataBuilder::Option::StrictRfc7578`: `OmitRfc8187EncodedFilename | UseRfc7578PercentEncodedFilename`；此选项组合其他选项以选择严格的 RFC 7578 合规性。
Options 类型是 QFlags<Option> 的 typedef。它存储 Option 值的 OR 组合。

### `flags Options`

**作用与语义：**

控制 `buildMultiPart()` 的选项。
当前有几个 RFC 对如何精确格式化 `multipart/form-data` 存在分歧。为了避免硬编码任何单一 RFC，这些选项允许您控制遵循哪个 RFC。
- `QFormDataBuilder::Option::Default`: `0x00`；默认值，旨在最大化常规互操作性。下面列出的所有选项都是关闭的。
- `QFormDataBuilder::Option::OmitRfc8187EncodedFilename`: `0x01`；当一个主体部分的文件名包含非 US-ASCII 字符时，RFC 6266 第 4.3 节建议使用 RFC 8187 风格的编码 (`filename*=utf-8''...`)。然而，更近期的 RFC 7578 第 4.2 节禁止使用该机制。截至本文撰写时，这两个 RFC 都是当前有效的，因此此选项允许您选择遵循哪一个。默认情况下，将包含 RFC 8187 编码的 `filename*` 以及未编码的 `filename`，如 RFC 6266 所建议。
- `QFormDataBuilder::Option::UseRfc7578PercentEncodedFilename`: `0x02`；当一个主体部分的文件名包含非 US-ASCII 字符时，RFC 7578 第 4.2 节建议对 UTF-8 编码的文件名的八位字节进行百分比编码。它还指出，许多实现实际上并不对 UTF-8 编码的文件名进行百分比编码，而只是输出“原始” UTF-8（`"` 和 `\` 使用 `\` 转义）。这也是 `QFormDataBuilder` 的默认设置。
- `QFormDataBuilder::Option::PreferLatin1EncodedFilename`: `0x04`；RFC 5987 第 3.2 节要求接收者支持 ISO-8859-1（"Latin-1"）编码。当一个主体部分的文件名包含非 US-ASCII 字符，但可以归入 Latin-1 时，此选项优先使用 ISO-8859-1 编码而不是 UTF-8。更近期的 {https://datatracker.ietf.org/doc/html/rfc8187#appendix-A}{RFC 8187} 不再要求支持 ISO-8859-1，因此默认情况下所有非 US-ASCII 文件名都以 UTF-8 编码发送。
- `QFormDataBuilder::Option::StrictRfc7578`: `OmitRfc8187EncodedFilename | UseRfc7578PercentEncodedFilename`；此选项组合其他选项以选择严格的 RFC 7578 合规性。
Options 类型是 QFlags<Option> 的 typedef。它存储 Option 值的 OR 组合。

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

`QFormDataBuilder` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
