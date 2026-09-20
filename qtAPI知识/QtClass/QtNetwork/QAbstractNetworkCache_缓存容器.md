# QAbstractNetworkCache：给网络管理器实现缓存后端

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAbstractNetworkCache>`  
> CMake：`Qt6::Network`  
> 继承：`QObject`  
> 类型：抽象基类

## 它解决什么问题

`QAbstractNetworkCache` 定义 `QNetworkAccessManager` 使用缓存后端的统一协议。它不提供存储实现，而是规定缓存如何：

- 依据 URL 查找元数据和响应内容；
- 为即将写入的内容准备临时 `QIODevice`；
- 将准备好的内容提交、更新或撤销；
- 报告并清空缓存容量。

大多数应用直接使用 `QNetworkDiskCache`。只有需要自定义内存缓存、加密缓存、数据库缓存或业务特定淘汰策略时，才应派生这个类。

## 实际使用场景

- 将 HTTP 响应存入自定义加密文件格式或数据库。
- 对缓存条目按租户、账号、网络环境或业务优先级淘汰。
- 在测试中提供可控的内存缓存，验证请求缓存策略。
- 替换默认磁盘缓存，但仍让 `QNetworkAccessManager` 按标准请求属性决定读写时机。

它不是“给任意 `QIODevice` 加缓存”的通用容器。该接口围绕 URL、HTTP 元数据和 `QNetworkAccessManager` 的请求生命周期设计。

## 核心流程与所有权

缓存写入有明确的两阶段协议：

```text
metaData(url) -> prepare(metaData) -> 向返回设备写响应体 -> insert(device)
                                                \-> remove(metaData.url()) 取消
```

`prepare()` 成功时返回一个由**缓存拥有**的 `QIODevice`。调用者填充设备后必须调用 `insert(device)` 提交；若决定放弃，调用 `remove(metaData.url())` 取消。不要手动删除 prepare 返回的设备，缓存会在插入或移除时回收它。

读取方向相反：`data(url)` 返回已缓存内容的 `QIODevice`，其所有权归**请求数据的应用方**。用完后必须删除该 device。找不到条目、URL 无效或内部出错时返回 `nullptr`。

这是自定义实现最关键的边界：把两种 device 的所有权写反，通常会导致泄漏、重复释放或缓存内容无法提交。

## 与 QNetworkAccessManager 协作

通常将一个已配置好的派生缓存交给网络管理器：

```cpp
#include <QNetworkAccessManager>
#include <QNetworkDiskCache>
#include <QStandardPaths>

auto *manager = new QNetworkAccessManager(this);
auto *cache = new QNetworkDiskCache;
cache->setCacheDirectory(
    QStandardPaths::writableLocation(QStandardPaths::CacheLocation)
    + QStringLiteral("/http-cache"));

manager->setCache(cache); // manager 取得 cache 的所有权
```

`QNetworkAccessManager::setCache()` 会取得缓存对象所有权。把它交给 manager 后，不要再由独立智能指针或其他 owner 销毁它；缓存的读写也应和 manager 一样限定在同一 QObject 线程中。

请求是否优先读缓存由 `QNetworkRequest` 的缓存加载属性决定，不能仅凭“设置了 cache”推断每个请求一定命中缓存。自定义后端只负责正确实现该协议，不应绕过请求的缓存控制语义。

## 实现派生类时的契约

### 查找、更新和删除

- `metaData(url)`：命中时返回有效的 `QNetworkCacheMetaData`，否则返回无效元数据。
- `data(url)`：返回可供读取的内容 device；调用者随后删除它。
- `updateMetaData(metaData)`：仅更新 `metaData.url()` 对应的已存在条目；不存在时不应凭空创建内容。
- `remove(url)`：删除该 URL 的条目，成功返回 `true`。
- `clear()`：删除所有条目；无失败时随后 `cacheSize()` 应为 0。

缓存 key 的规范化策略必须稳定。`QNetworkCacheMetaData::setUrl()` 会去掉密码和 fragment，派生实现若又使用未规范化 URL 建 key，很容易制造“写入后读不到”的幽灵未命中。

### 容量报告

`cacheSize()` 返回当前占用的大小，单位是字节。它可以是磁盘或内存大小，取决于实现。若后台清理是延迟的，应确保该值和实际可用空间策略一致，避免网络管理器和诊断工具看到误导性数字。

### 生命周期和失败路径

基类析构时，尚未 `insert()` 的准备操作会被丢弃。实现中应保证临时文件、事务或内存缓冲随之清理。所有纯虚函数都可能被 manager 在网络活动期间调用，不应在其中执行长时间阻塞 I/O 或回调同一个 manager 形成重入链。

## 常见误区

- **把 `data()` 返回的 device 当成 cache 所有**：它由请求数据的一方删除。
- **手动删除 `prepare()` 的返回值**：该 device 属于 cache；提交后 `insert()`，取消时 `remove()`。
- **调用 `prepare()` 后什么也不做**：未提交操作会在销毁时丢弃，应显式 insert 或 remove。
- **`updateMetaData()` 被当作创建接口**：它只更新已有 cache item。
- **把抽象接口直接实例化**：该类含纯虚函数，实际使用 `QNetworkDiskCache` 或自定义子类。

## API 速查表

| 类别 | API | 语义与注意点 |
| --- | --- | --- |
| 构造 | `QAbstractNetworkCache(parent)` | 受保护构造；仅供派生类初始化 QObject 基类。 |
| 析构 | `~QAbstractNetworkCache()` | 虚析构；未提交的 prepare 操作会被丢弃。 |
| 查询 | `metaData(url)` | 取 URL 的元数据；命中返回有效值，未命中或异常返回无效元数据。 |
| 查询 | `data(url)` | 取缓存内容 device；未命中、无效 URL 或内部错误返回 `nullptr`，调用方负责删除成功返回的 device。 |
| 写入 | `prepare(metaData)` | 为条目准备可写 device；元数据或其中 URL 无效时返回 `nullptr`。返回设备归缓存所有。 |
| 写入 | `insert(device)` | 提交通过 `prepare()` 填充的内容和元数据，使后续 `data()` / `metaData()` 可读取。 |
| 更新 | `updateMetaData(metaData)` | 更新该 URL 已有条目的元数据；没有该条目时不做事。 |
| 删除 | `remove(url)` | 删除 URL 对应条目；返回是否成功，同时也可取消尚未提交的 prepare。 |
| 容量 | `cacheSize() const` | 返回当前缓存占用字节数；具体是内存还是磁盘由实现定义。 |
| 清空 | `clear()` | 槽函数，移除全部项目；无失败时容量应归零。 |

## 相关类型

- `QNetworkDiskCache`：Qt 提供的基础磁盘实现。
- `QNetworkCacheMetaData`：URL、HTTP 头和缓存存储策略等条目元数据。
- `QNetworkAccessManager`：缓存协议的主要调用方。
- `QIODevice`：缓存内容的读取和临时写入通道。
