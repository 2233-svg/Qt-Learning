# QMimeDatabase

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“Mime数据库”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QMimeDatabase` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QMimeDatabase>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum MatchMode { MatchDefault, MatchExtension, MatchContent }`

### 公有函数

- `QMimeDatabase()`
- `~QMimeDatabase()`
- `QList<QMimeType> allMimeTypes() const`
- `QMimeType mimeTypeForData(QIODevice *device) const`
- `QMimeType mimeTypeForData(const QByteArray &data) const`
- `QMimeType mimeTypeForFile(const QFileInfo &fileInfo, QMimeDatabase::MatchMode mode = MatchDefault) const`
- `QMimeType mimeTypeForFile(const QString &fileName, QMimeDatabase::MatchMode mode = MatchDefault) const`
- `QMimeType mimeTypeForFileNameAndData(const QString &fileName, QIODevice *device) const`
- `QMimeType mimeTypeForFileNameAndData(const QString &fileName, const QByteArray &data) const`
- `QMimeType mimeTypeForName(const QString &nameOrAlias) const`
- `QMimeType mimeTypeForUrl(const QUrl &url) const`
- `QList<QMimeType> mimeTypesForFileName(const QString &fileName) const`
- `QString suffixForFileName(const QString &fileName) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QMimeDatabase::MatchMode`

**作用与语义：**

该枚举规定了如何将文件匹配到MIME类型。
- `QMimeDatabase::MatchDefault`：`0x0`;文件名和内容均用于匹配
- `QMimeDatabase::MatchExtension`：`0x1`;仅使用文件名来查找匹配
- `QMimeDatabase::MatchContent`：`0x2`;文件内容用于寻找匹配

### `QMimeDatabase::QMimeDatabase()`

**作用与语义：**

构建一个QMimeDatabase对象。
每次需要查找时创建 QMimeDatabase 实例完全没问题。mimetypes 的解析可以按需进行（安装共享 mime-info 时），或者在构建第一个实例时（直接解析 XML 文件时）。

### `[noexcept] QMimeDatabase::~QMimeDatabase()`

**作用与语义：**

摧毁`QMimeDatabase`物体。

### `QList<QMimeType> QMimeDatabase::allMimeTypes() const`

**作用与语义：**

返回所有可用的MIME类型列表。
这对于向用户展示所有 MIME 类型非常有用，例如在 MIME 类型编辑器中。除非非常必要，否则不要使用，出于性能考虑，优先使用`mimeTypeForXxx()`方法。

### `QMimeType QMimeDatabase::mimeTypeForData(QIODevice *device) const`

**作用与语义：**

返回数据的MIME类型`device`。
总是返回一个有效的 MIME 类型。如果 `device` 中的数据与已知的 MIME 类型数据不匹配，则返回默认的 MIME 类型（应用程序/八位元组流）。

### `QMimeType QMimeDatabase::mimeTypeForData(const QByteArray &data) const`

**作用与语义：**

退回一台MIME类型`data`。
总是返回一个有效的 MIME 类型。如果 `data` 与已知的 MIME 类型数据不匹配，则返回默认的 MIME 类型（应用程序/八位元组流）。

### `QMimeType QMimeDatabase::mimeTypeForFile(const QFileInfo &fileInfo, QMimeDatabase::MatchMode mode = MatchDefault) const`

**作用与语义：**

退回一台MIME类型`fileInfo`。
总是返回有效的 MIME 类型。
默认匹配算法会同时查看文件名和文件内容（如有必要）。文件扩展名优先于内容，但如果文件扩展名未知或匹配多个 MIME 类型，则使用内容。如果 `fileInfo` 是 Unix 符号链接，则使用其所引用的文件。如果文件与已知模式或数据不匹配，则返回默认 MIME 类型（application/octet-stream）。
当`mode`设置为`MatchExtension`时，只使用文件名，而非文件内容。文件甚至不必存在。如果文件名与已知模式不匹配，返回默认MIME类型（application/octet-stream）。如果多个MIME类型匹配该文件，返回第一个类型（按字母顺序）。
当`mode`设置为`MatchContent`且文件可读时，仅使用文件内容来确定MIME类型。这相当于调用`mimeTypeForData`，输入设备为`QFile`。
`fileInfo`可以指绝对路径或相对路径。

### `QMimeType QMimeDatabase::mimeTypeForFile(const QString &fileName, QMimeDatabase::MatchMode mode = MatchDefault) const`

**作用与语义：**

返回名为`fileName`的文件的MIME类型，使用`mode`。

### `QMimeType QMimeDatabase::mimeTypeForFileNameAndData(const QString &fileName, QIODevice *device) const`

**作用与语义：**

返回给定`fileName`和`device`数据的MIME类型。
这种重载在文件处于远程状态时非常有用，我们开始在设备中下载部分数据。这也允许对远程文件进行完整的MIME类型匹配。
如果设备未打开，该功能将被打开，完成MIME类型检测后关闭设备。
总是返回一个有效的MIME类型。如果`device`数据与任何已知的MIME类型数据不匹配，则返回默认MIME类型（应用程序/八位元组流）。
该方法会同时查看文件名和文件内容（如有必要）。文件扩展名优先于内容，但如果文件扩展名未知或匹配多个 MIME 类型，则会使用内容。

### `QMimeType QMimeDatabase::mimeTypeForFileNameAndData(const QString &fileName, const QByteArray &data) const`

**作用与语义：**

返回给定`fileName`和设备`data`的MIME类型。
这种重载在文件处于远程时非常有用，我们开始下载部分数据。这也允许对远程文件进行完整的MIME类型匹配。
总是返回一个有效的 MIME 类型。如果`data`与已知的 MIME 类型数据不匹配，则返回默认的 MIME 类型（应用/八元组流）。
该方法会同时查看文件名和文件内容（如有必要）。文件扩展名优先于内容，但如果文件扩展名未知或匹配多个 MIME 类型，则会使用内容。

### `QMimeType QMimeDatabase::mimeTypeForName(const QString &nameOrAlias) const`

**作用与语义：**

如果没有找到，则返回一个MIME类型`nameOrAlias`或返回无效类型。

### `QMimeType QMimeDatabase::mimeTypeForUrl(const QUrl &url) const`

**作用与语义：**

退回一辆MIME类型`url`。
如果URL是本地文件，则调用`mimeTypeForFile`。
否则匹配仅基于文件名，除非文件名意义不大，比如 HTTP。该方法总是返回 HTTP URL 的默认 mimetype，使用 `QNetworkAccessManager` 正确处理 HTTP URL。
总是返回有效的 MIME 类型。如果 `url` 与已知的 MIME 类型数据不匹配，则返回默认的 MIME 类型（应用程序/八位元组流）。

### `QList<QMimeType> QMimeDatabase::mimeTypesForFileName(const QString &fileName) const`

**作用与语义：**

返回文件名 `fileName` 的 MIME 类型。
如果文件名与已知模式不匹配，则返回一个空列表。如果多个 MIME 类型匹配该文件，则全部返回。
该函数不会尝试打开文件。为了在确定MIME类型时也使用内容，请使用`mimeTypeForFile()`或`mimeTypeForFileNameAndData()`。

### `QString QMimeDatabase::suffixForFileName(const QString &fileName) const`

**作用与语义：**

返回文件`fileName`的后缀，符合MIME数据库的认知。
这允许预选“tar.bz2”作为 foo.tar.bz2，但仅为 my.file.with.dots.txt 选择“txt”。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QMimeDatabase` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
