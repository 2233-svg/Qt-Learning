# QLocalServer
> Qt 6.11.1 · Qt Network · 来自 `QLocalServer`

## 作用定位
`QLocalServer` 监听命名本地 IPC 端点，并生成 `QLocalSocket` 客户端连接。

## API 速查
| API | 是做什么的 |
|---|---|
| `listen(name)` | 开始监听本地服务名。|
| `newConnection()` | 有本地客户端连接。|
| `nextPendingConnection()` | 取出下一个本地 socket。|
| `removeServer()` | 清除遗留服务端点。|
| `setSocketOptions()` | 设置访问/权限选项。|

## 使用场景
启动时尝试监听固定服务名；若已存在则连接主实例转发参数并退出。

## 常见坑与经验
- 崩溃后 Unix socket 文件可能遗留，谨慎使用 `removeServer()`，避免删除别的活跃服务。
- 服务名应包含用户/应用隔离信息，避免不同用户或不同版本冲突。

## 知识点覆盖
本地服务、单实例、命名冲突、权限、遗留端点、进程通信。
