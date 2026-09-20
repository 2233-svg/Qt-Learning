# QByteArrayView
> Qt 6.11.1 · Qt Core · 来自 `QByteArrayView`

## 作用定位
`QByteArrayView` 是不拥有数据的只读字节视图，适合作为二进制 API 参数而避免复制。

## API 速查
| API | 是做什么的 |
|---|---|
| `data()` / `size()` | 访问原始字节和长度。|
| `sliced()` / `first()` / `last()` | 创建子视图。|
| `indexOf()` | 查找字节或子序列。|
| `toByteArray()` | 显式复制为拥有数据。|

## 使用场景
解析器、哈希函数、协议编码器接收 `QByteArray`、原始 buffer 或字面量。

## 常见坑与经验
- 不拥有数据，异步任务或长期缓存前必须复制。

## 知识点覆盖
零拷贝、字节视图、生命周期、切片、二进制 API。
