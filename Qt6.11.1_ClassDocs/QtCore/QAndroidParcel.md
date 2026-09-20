# QAndroidParcel
> Qt 6.11.1 · Qt Core · 来自 `QAndroidParcel`

## 作用定位
`QAndroidParcel` 是 Android Binder 数据传输的序列化容器封装。

## API 速查
| API | 是做什么的 |
|---|---|
| `writeData()` | 写入基本值或可序列化内容。|
| `readData()` | 读取内容。|
| `writeInterfaceToken()` | 写入接口标识。|
| `enforceInterface()` | 验证接收接口标识。|
| `dataAvail()` | 查询剩余可读字节。|

## 使用场景
实现 Binder transaction 的参数与返回值编解码。

## 常见坑与经验
- 读写字段顺序必须严格一致，读取前要检查剩余数据与类型。

## 知识点覆盖
Parcel、IPC 编码、接口令牌、输入验证、Android。
