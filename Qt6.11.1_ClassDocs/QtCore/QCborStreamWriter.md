# QCborStreamWriter
> Qt 6.11.1 · Qt Core · 来自 `QCborStreamWriter`

## 作用定位
`QCborStreamWriter` 将 CBOR token 直接写入 `QIODevice` 或字节数组，避免先构造完整对象树。

## API 速查
| API | 是做什么的 |
|---|---|
| `startArray()` / `endArray()` | 写入数组边界。|
| `startMap()` / `endMap()` | 写入 map 边界。|
| `append()` | 写入整数、文本、字节或值。|
| `appendNull()` / `appendUndefined()` | 写入简单值。|
| `appendTag()` | 写入 CBOR tag。|

## 使用场景
持续生成大消息、边采集边写文件或按协议顺序编码字段。

## 常见坑与经验
- map 的键和值必须成对写入；数组/map 的嵌套开始与结束必须平衡。
- 写入错误通常来自目标 device，结束后仍要检查 device 状态。

## 知识点覆盖
流式编码、QIODevice、CBOR 容器、嵌套平衡、内存控制。
