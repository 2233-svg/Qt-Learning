# QIODevice
> Qt 6.11.1 · Qt Core · 来自 `QIODevice`

## 作用定位
`QIODevice` 是 Qt 顺序或随机访问 I/O 的抽象基类，统一文件、内存缓冲、网络 socket、进程管道和自定义数据源的读写协议。

## API 速查
| API | 是做什么的 |
|---|---|
| `open()` / `close()` | 打开或关闭设备。|
| `read()` / `readAll()` | 读取可用字节。|
| `write()` | 写入字节。|
| `bytesAvailable()` | 查询当前可读缓冲量。|
| `bytesToWrite()` | 查询待写缓冲量。|
| `readyRead()` | 有新字节可读时通知。|
| `bytesWritten()` | 已写入底层设备时通知。|
| `canReadLine()` / `readLine()` | 按行读取文本。|
| `seek()` / `pos()` | 在随机访问设备中定位。|
| `startTransaction()` / `commitTransaction()` | 对不完整流数据执行可回滚读取。|

## 使用场景
让序列化器、解码器或协议解析器面向 `QIODevice*` 编写，从而同时支持文件、内存和网络输入。

## 常见坑与经验
- `readyRead()` 表示“有字节”，不是“有完整消息”；网络协议必须自行分帧。
- 顺序设备不能 `seek()`；调用前检查 `isSequential()`。
- `readAll()` 会复制当前全部缓冲，大数据流应分块读取并设定最大包长。
- 事务读取非常适合长度未知的半包，但提交失败后必须等待更多数据而不是丢弃缓冲。

## 知识点覆盖
设备抽象、顺序与随机访问、异步 I/O、缓冲、协议分帧、读取事务、内存控制。
