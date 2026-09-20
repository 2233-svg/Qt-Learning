# QNetworkCacheMetaData
> Qt 6.11.1 · Qt Network · 来自 `QNetworkCacheMetaData`

## 作用定位
`QNetworkCacheMetaData` 是缓存条目的值类型，保存 URL、保存日期、过期日期、原始响应头和自定义属性。

## API 速查
| API | 是做什么的 |
|---|---|
| `setUrl()` / `url()` | 设置或读取缓存键 URL。|
| `setSaveToDisk()` | 标记是否允许落盘。|
| `setRawHeaders()` | 保存响应头。|
| `setExpirationDate()` | 设置过期时间。|
| `setLastModified()` | 设置最后修改时间。|
| `setAttributes()` | 保存额外属性。|

## 使用场景
自定义 cache 实现保存验证器、响应头和过期策略。

## 常见坑与经验
- 过期时间只是缓存判定的一部分；ETag/Last-Modified 再验证同样重要。
- 缓存元数据可能含敏感 URL/头，日志需脱敏。

## 知识点覆盖
缓存键、HTTP 验证、过期、ETag、隐私、值对象。
