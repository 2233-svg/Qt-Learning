# QDataStream
> Qt 6.11.1 · Qt Core · 来自 `QDataStream`

## 作用定位
`QDataStream` 在 `QIODevice` 上读写 Qt 定义的二进制数据格式，支持基本类型以及实现了流运算符的 Qt 值类型。

## API 速查
| API | 是做什么的 |
|---|---|
| `setDevice()` | 指定底层读写设备。|
| `operator<<` / `operator>>` | 编码或解码支持的值。|
| `setVersion()` | 固定 Qt 二进制格式版本。|
| `setByteOrder()` | 选择大端或小端。|
| `setFloatingPointPrecision()` | 规定浮点编码精度。|
| `status()` | 查询读写和格式错误。|
| `startTransaction()` / `commitTransaction()` | 处理可能尚未收全的流数据。|

## 使用场景
本地缓存、Qt 进程间协议、二进制文件格式；网络流分帧后用 transaction 等待完整字段。

## 常见坑与经验
- 必须在协议中固定 `setVersion()`、字节序和自定义字段顺序；Qt 版本升级不应悄悄改变持久格式。
- 不可信输入要限制字符串、容器和 blob 长度，防止恶意声明巨大大小。
- `commitTransaction()` 失败时不要消费半包数据。

## 知识点覆盖
二进制序列化、QIODevice、字节序、版本兼容、事务读取、输入安全。
