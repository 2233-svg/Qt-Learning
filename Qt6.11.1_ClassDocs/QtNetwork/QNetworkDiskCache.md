# QNetworkDiskCache
> Qt 6.11.1 · Qt Network · 来自 `QNetworkDiskCache`

## 作用定位
`QNetworkDiskCache` 是 Qt 提供的磁盘 HTTP 缓存实现，可挂到 `QNetworkAccessManager`。

## API 速查
| API | 是做什么的 |
|---|---|
| `setCacheDirectory()` | 设置缓存目录。|
| `setMaximumCacheSize()` | 限制最大磁盘占用。|
| `cacheDirectory()` | 读取实际目录。|
| `expire()` | 清除过期/超量条目。|
| `clear()` | 删除全部缓存。|

## 使用场景
新闻、文档、图片等允许 HTTP 缓存的客户端，降低重复下载。

## 常见坑与经验
- 缓存目录应放在应用缓存路径，不能直接使用安装目录。
- 登录态私有数据是否可缓存要由服务端头和产品安全规则共同决定。

## 知识点覆盖
磁盘缓存、缓存目录、容量、HTTP 缓存控制、隐私。
