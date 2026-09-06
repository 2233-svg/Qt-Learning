# QAbstractNetworkCache

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QAbstractNetworkCache` 是 Qt Network 的“抽象网络缓存”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QAbstractNetworkCache` 是 Qt Network 中的抽象协议类型，通常通过具体子类、模型、插件或工厂来使用。

**内部模型：** 抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

**适用场景：** 当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。

**典型调用链：** 选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

**先记住的坑：** 不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

## 2. 依赖与对象关系

- 头文件：`#include <QAbstractNetworkCache>`
- 继承自：QObject
- 直接派生类：QNetworkDiskCache

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Network)
target_link_libraries(mytarget PRIVATE Qt6::Network)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

### 状态、生命周期和线程

**生命周期：** manager 必须在线程事件循环中存活到 reply 完成；reply 完成后读取结果并调用 `deleteLater()`，不能在信号触发前直接释放。请求对象是值类型，reply 才是带有异步状态和资源的对象。

**状态与结果：** 请求成功发出不等于 HTTP 成功，HTTP 状态码成功也不等于业务 JSON 有效。至少分别处理网络错误、HTTP 状态码、响应头、响应体解析和业务字段校验。上传/下载还要处理进度、分段读取和取消。

**线程与事件循环：** QNetworkAccessManager、QNetworkReply 和相关请求应在同一个有事件循环的线程使用。跨线程时把网络对象整体放到目标线程，通过信号传递结果，不要跨线程直接读写 reply。

## 3. 直接使用

当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。 使用时通常按这个过程组织：选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

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

- `virtual ~QAbstractNetworkCache()`
- `virtual qint64 cacheSize() const = 0`
- `virtual QIODevice * data(const QUrl &url) = 0`
- `virtual void insert(QIODevice *device) = 0`
- `virtual QNetworkCacheMetaData metaData(const QUrl &url) = 0`
- `virtual QIODevice * prepare(const QNetworkCacheMetaData &metaData) = 0`
- `virtual bool remove(const QUrl &url) = 0`
- `virtual void updateMetaData(const QNetworkCacheMetaData &metaData) = 0`

### 公有槽函数

- `virtual void clear() = 0`

### 保护函数

- `QAbstractNetworkCache(QObject *parent = nullptr)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit protected] QAbstractNetworkCache::QAbstractNetworkCache(QObject *parent = nullptr)`

**作用与语义：**

构造一个包含给定`parent`的抽象网络缓存。

### `[virtual noexcept] QAbstractNetworkCache::~QAbstractNetworkCache()`

**作用与语义：**

摧毁缓存。
未插入的操作被丢弃。

### `[pure virtual] qint64 QAbstractNetworkCache::cacheSize() const`

**作用与语义：**

返回缓存当前占用的大小。根据缓存实现，可能是磁盘大小或内存大小。
在基类中，这是一个纯虚拟函数。

### `[pure virtual slot] void QAbstractNetworkCache::clear()`

**作用与语义：**

移除缓存中的所有项目。除非清除缓存失败，否则调用清除后`cacheSize()`应该返回0。
在基类中，这是一个纯虚拟函数。

### `[pure virtual] QIODevice *QAbstractNetworkCache::data(const QUrl &url)`

**作用与语义：**

返回与`url`相关的数据。
请求数据的应用程序在完成`QIODevice`后是否删除。
如果没有缓存，`url` 的 URL 无效;如果内存内部缓存错误，`nullptr`返回。
在基类中，这是一个纯虚拟函数。

### `[pure virtual] void QAbstractNetworkCache::insert(QIODevice *device)`

**作用与语义：**

将数据插入`device`并将准备好的元数据插入缓存。调用该函数后，数据和元数据应可通过`data()`和`metaData()`检索。
取消预先插入的调用`remove()`元数据的 URL。
在基类中，这是一个纯虚拟函数。

### `[pure virtual] QNetworkCacheMetaData QAbstractNetworkCache::metaData(const QUrl &url)`

**作用与语义：**

返回URL的元数据`url`。
如果URL有效且缓存包含URL数据，则返回有效`QNetworkCacheMetaData`。
在基类中，这是一个纯虚拟函数。

### `[pure virtual] QIODevice *QAbstractNetworkCache::prepare(const QNetworkCacheMetaData &metaData)`

**作用与语义：**

返回应填充缓存项数据的设备`metaData`。当所有数据写入后，应调用`insert()`。如果`metaData`无效或元数据中的URL无效，返回`nullptr`。
缓存拥有设备，并在插入或移除时负责删除。
取消预设插入的调用`remove()`元数据 URL 上的调用。
在基类中，这是一个纯虚拟函数。

### `[pure virtual] bool QAbstractNetworkCache::remove(const QUrl &url)`

**作用与语义：**

移除`url`的缓存条目，如果成功或为false则返回true。
在基类中，这是一个纯虚拟函数。

### `[pure virtual] void QAbstractNetworkCache::updateMetaData(const QNetworkCacheMetaData &metaData)`

**作用与语义：**

更新`metaData`网址的缓存元日期为`metaData`。
如果缓存中没有该URL的缓存项，则不会采取任何操作。
在基类中，这是一个纯虚拟函数。

## 6. 深入实践与常见坑

### 生命周期和资源边界

manager 必须在线程事件循环中存活到 reply 完成；reply 完成后读取结果并调用 `deleteLater()`，不能在信号触发前直接释放。请求对象是值类型，reply 才是带有异步状态和资源的对象。

### 状态和错误边界

请求成功发出不等于 HTTP 成功，HTTP 状态码成功也不等于业务 JSON 有效。至少分别处理网络错误、HTTP 状态码、响应头、响应体解析和业务字段校验。上传/下载还要处理进度、分段读取和取消。

### 线程边界

QNetworkAccessManager、QNetworkReply 和相关请求应在同一个有事件循环的线程使用。跨线程时把网络对象整体放到目标线程，通过信号传递结果，不要跨线程直接读写 reply。

### 最容易出现的错误

不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QAbstractNetworkCache` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
