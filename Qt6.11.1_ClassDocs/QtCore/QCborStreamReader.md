# QCborStreamReader
> Qt 6.11.1 · Qt Core · 来自 `QCborStreamReader`

## 作用定位
`QCborStreamReader` 以流式方式解析 CBOR，适合输入很大、来自 `QIODevice` 或不能一次性载入内存的场景。

## API 速查
| API | 是做什么的 |
|---|---|
| `currentType()` | 查询当前 token 类型。|
| `isArray()` / `isMap()` | 判断容器开始。|
| `enterContainer()` / `leaveContainer()` | 进入或离开嵌套容器。|
| `next()` | 前进到下一个 token。|
| `readString()` / `readByteArray()` | 读取标量内容。|
| `lastError()` | 查询解析或 I/O 错误。|

## 使用场景
处理大型 CBOR 日志、设备数据流或受内存限制的消息。

## 常见坑与经验
- 读取逻辑必须严格与 CBOR 嵌套结构匹配；遗漏 `leaveContainer()` 会使后续解析失位。
- 输入不可信时设置消息大小、嵌套深度和字段长度限制。

## 知识点覆盖
流式解析、QIODevice、嵌套容器、错误恢复、资源限制。
