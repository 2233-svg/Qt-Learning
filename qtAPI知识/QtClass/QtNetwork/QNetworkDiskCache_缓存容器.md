# QNetworkDiskCache：QNetworkAccessManager 的基础磁盘缓存

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QNetworkDiskCache>`  
> CMake：`Qt6::Network`  
> 继承：`QAbstractNetworkCache`

## 它解决什么问题

`QNetworkDiskCache` 是 Qt 提供的基础 URL 响应磁盘缓存。它把每个 URL 的缓存内容放到 `cacheDirectory()` 下的独立文件，并与 `QNetworkCacheMetaData` 一起供 `QNetworkAccessManager` 在后续请求中复用。

它的目标是减少重复网络传输和提高离线/弱网体验，不是通用文件数据库，也不提供浏览器级缓存诊断、跨进程共享或内容加密。

## 实际使用场景

- 桌面客户端缓存静态资源、GET 响应和 API 数据，降低启动或重复浏览成本。
- 在网络波动时配合 `QNetworkRequest::CacheLoadControlAttribute` 优先使用已有内容。
- 对开发工具的 HTTP 请求进行基础离线缓存。

不适合保存用户机密、需要事务一致性的数据或多个进程共享的缓存文件。缓存目录中的内容应被视为可丢失、可重建的数据。

## 正确配置方式

必须在 cache 真正工作前设置目录，再交给网络管理器：

```cpp
#include <QNetworkAccessManager>
#include <QNetworkDiskCache>
#include <QNetworkRequest>
#include <QStandardPaths>

auto *manager = new QNetworkAccessManager(this);
auto *cache = new QNetworkDiskCache;

const QString directory =
    QStandardPaths::writableLocation(QStandardPaths::CacheLocation)
    + QStringLiteral("/network-cache");
cache->setCacheDirectory(directory);
cache->setMaximumCacheSize(100LL * 1024 * 1024);

manager->setCache(cache); // manager 取得 cache 所有权

QNetworkRequest request(QUrl(QStringLiteral("https://example.com/feed")));
request.setAttribute(QNetworkRequest::CacheLoadControlAttribute,
                     QNetworkRequest::PreferCache);
manager->get(request);
```

默认最大缓存空间是 50 MB。`setCacheDirectory()` 会在目录不存在时创建它；若不先设置目录，磁盘缓存无法工作。`QNetworkAccessManager::setCache()` 取得 cache 所有权，不应再由别处释放。

## 如何判断和控制缓存使用

设置缓存并不代表每个请求都会命中。请求可通过 `QNetworkRequest::CacheLoadControlAttribute` 指定网络与缓存的偏好，例如 `PreferCache`。响应完成后，读取 `QNetworkRequest::SourceIsFromCacheAttribute` 可判断结果是否来自缓存：

```cpp
QObject::connect(manager, &QNetworkAccessManager::finished,
                 manager, [](QNetworkReply *reply) {
    const bool fromCache = reply->attribute(
        QNetworkRequest::SourceIsFromCacheAttribute).toBool();
    qDebug() << "from cache:" << fromCache;
});
```

这里的 `PreferCache` 是偏好而不是“保证离线命中”。条目可能不存在、过期、被清理，或请求/响应策略不允许使用缓存。

## 关键语义与边界

### 文件格式与共享限制

每个 URL 使用独立缓存文件，元数据使用 `QDataStream` 存储；文本 MIME 类型内容会以 `qCompress` 压缩。数据实际写盘发生在 `insert()` 和 `updateMetaData()`。

同一套缓存文件不能被多个 `QNetworkDiskCache` 实例共享。多进程或多实例同时指向同一目录会破坏这一前提；每个独立实例应使用独立目录，或自行实现带进程协调的缓存后端。

### 对象析构不会清空磁盘

析构 `QNetworkDiskCache` 只销毁对象，不删除缓存目录及其中内容。需要主动清空时调用 `clear()`；用户清理缓存、账号切换和隐私模式应明确调用它或使用独立临时目录。

### 容量不是硬边界的瞬时检查

当缓存超过 `maximumCacheSize()`，`expire()` 按文件创建时间从旧到新移除条目，直到总大小低于最大值的 90%。将最大值调小也会触发清理。`cacheSize()` 在当前大小未知时也可能调用 `expire()`。

因此一次容量查询可能伴随 I/O 和清理；不要在高频 UI 刷新路径中反复调用它。若按访问频率、优先级或账户隔离淘汰，应派生并重写 `expire()`。

### 基类 device 所有权仍然适用

通过 `data(url)` 取得的读取设备由调用方删除；`prepare(metaData)` 返回的临时写设备由 cache 所有，调用方写完后调用 `insert(device)`，取消时 `remove(metaData.url())`。即使使用具体磁盘类，这条 `QAbstractNetworkCache` 契约也不变。

## 常见误区

- **只创建 `QNetworkDiskCache` 而未设目录**：它不会正常工作。
- **让两个 manager/进程共享同一 cacheDirectory**：该实现不支持共享同一缓存文件。
- **析构对象后以为磁盘内容消失**：需要显式 `clear()`。
- **把磁盘缓存当成敏感数据仓库**：缓存内容可被清除、可能被读取；还应尊重元数据的 `saveToDisk` 策略。
- **把 `maximumCacheSize()` 当作绝不越过的实时上限**：清理由 `expire()` 执行，实际会清至最大值的 90% 以下。

## API 速查表

| 类别 | API | 语义与注意点 |
| --- | --- | --- |
| 构造/析构 | `QNetworkDiskCache(parent)` / `~QNetworkDiskCache()` | 创建/销毁磁盘缓存；析构不清空磁盘目录。 |
| 目录 | `cacheDirectory()` | 返回当前缓存目录。 |
| 目录 | `setCacheDirectory(cacheDir)` | 设置目录，不存在时创建；应在使用缓存前调用。后续 prepare 条目在插入时写入新目录。 |
| 容量 | `maximumCacheSize()` | 返回容量上限，默认 50 MB。 |
| 容量 | `setMaximumCacheSize(size)` | 设置字节上限；新值小于当前大小时触发过期清理。 |
| 容量 | `cacheSize()` | 返回当前磁盘占用；大小未知时可能触发 `expire()`。 |
| 查询 | `metaData(url)` | 重写基类，取得 URL 元数据。 |
| 查询 | `data(url)` | 重写基类，取得内容 device；调用方负责删除。 |
| 写入 | `prepare(metaData)` | 重写基类，准备 cache 所有的临时写设备。 |
| 写入 | `insert(device)` | 重写基类，提交 prepare 后写好的内容。 |
| 更新 | `updateMetaData(metaData)` | 重写基类，只将元数据变更写入磁盘。 |
| 删除 | `remove(url)` | 重写基类，删除 URL 条目；可取消尚未提交的写入。 |
| 清空 | `clear()` | 槽函数，删除全部缓存项目。 |
| 文件检查 | `fileMetaData(fileName) const` | 读取指定缓存文件的元数据；不是有效缓存文件时返回无效元数据。 |
| 淘汰 | `expire()` | 受保护虚函数；按创建时间删除最旧文件直到低于上限 90%，可重写淘汰顺序。 |

## 相关类型

- `QAbstractNetworkCache`：缓存后端协议和 device 所有权规则。
- `QNetworkCacheMetaData`：文件的 URL、头和磁盘保存许可。
- `QNetworkAccessManager`：设置 cache 并决定请求读写缓存。
- `QNetworkRequest`：通过属性控制缓存偏好并标识是否来自缓存。
