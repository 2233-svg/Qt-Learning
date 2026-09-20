# QIODeviceBase
> Qt 6.11.1 · Qt Core · 来自 `QIODeviceBase`

## 作用定位
`QIODeviceBase` 提供所有 Qt I/O 设备共享的打开模式、错误类型和文本模式等基础定义；`QIODevice` 在此基础上加入实际读写接口。

## API 速查
| API | 是做什么的 |
|---|---|
| `OpenMode` | 组合读、写、追加、截断、文本、未缓冲等打开方式。|
| `ReadOnly` / `WriteOnly` | 声明读或写权限。|
| `ReadWrite` | 同时读写。|
| `Append` | 写入从设备末尾开始。|
| `Truncate` | 打开时清空已有内容。|
| `Text` | 启用平台文本换行转换。|
| `OpenModeFlag` | 单个打开模式位。|

## 使用场景
打开 `QFile`、`QBuffer`、`QTcpSocket` 等设备时指定需要的读写语义。

## 常见坑与经验
- `Append` 与 `Truncate` 表意相反，组合前先确认底层设备支持的语义。
- 二进制协议和哈希计算不应使用 `Text`，否则换行转换会改变字节内容。

## 知识点覆盖
I/O 打开模式、文本与二进制、追加、截断、设备抽象、位标志。
