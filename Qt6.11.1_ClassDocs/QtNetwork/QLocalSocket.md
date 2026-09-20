# QLocalSocket
> Qt 6.11.1 · Qt Network · 来自 `QLocalSocket`

## 作用定位
`QLocalSocket` 是同一机器进程之间的流式 IPC 客户端。Unix 常使用 domain socket，Windows 使用本地命名管道等实现。

## API 速查
| API | 是做什么的 |
|---|---|
| `connectToServer()` | 连接命名本地服务。|
| `serverName()` / `fullServerName()` | 查询逻辑名和平台实际名。|
| `readyRead()` | 接收 IPC 字节流。|
| `errorOccurred()` | 查询连接和访问错误。|
| `disconnectFromServer()` | 关闭连接。|

## 使用场景
单实例应用将打开文件命令转发给主进程、桌面程序与本机辅助服务通信。

## 常见坑与经验
- 它仍是字节流，同样需要协议分帧。
- 本地不等于可信；其他用户或恶意本机进程可能尝试连接，需设置权限和握手认证。

## 知识点覆盖
本地 IPC、命名服务、字节流、单实例应用、访问控制。
