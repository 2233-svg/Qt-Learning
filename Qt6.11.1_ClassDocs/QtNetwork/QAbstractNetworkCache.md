# QAbstractNetworkCache
> Qt 6.11.1 · Qt Network · 来自 `QAbstractNetworkCache`

## 作用定位
`QAbstractNetworkCache` 定义网络响应缓存接口。`QNetworkAccessManager` 可通过它读取、写入和删除可缓存资源。

## API 速查
| API | 是做什么的 |
|---|---|
| `metaData()` | 查询 URL 的缓存元数据。|
| `data()` | 打开缓存响应体供读取。|
| `insert()` | 开始写入一个缓存条目。|
| `updateMetaData()` | 更新缓存头与属性。|
| `remove()` | 删除 URL 缓存。|
| `clear()` | 清空缓存。|
| `cacheSize()` | 查询占用大小。|
| `expire()` | 清理过期条目。|

## 使用场景
实现加密缓存、内存 LRU 或公司统一缓存策略。

## 常见坑与经验
- 必须尊重 HTTP cache-control、Vary 和认证语义；缓存层不应随意复用私有响应。
- 读写设备的所有权和关闭责任需按接口约定处理。

## 知识点覆盖
HTTP 缓存、缓存元数据、LRU、过期、隐私响应、设备所有权。
