# QHostInfo
> Qt 6.11.1 · Qt Network · 来自 `QHostInfo`

## 作用定位
`QHostInfo` 表示一次主机名 DNS 解析结果，含规范名、地址列表、错误和查找 ID。

## API 速查
| API | 是做什么的 |
|---|---|
| `lookupHost()` | 异步解析域名。|
| `abortHostLookup()` | 取消未完成查找。|
| `addresses()` | 读取解析到的地址。|
| `error()` / `errorString()` | 查询解析失败原因。|
| `hostName()` | 读取请求主机名。|

## 使用场景
在连接前解析域名，并让 `QTcpSocket` 按结果或直接按主机名连接。

## 常见坑与经验
- DNS 成功只说明名称解析成功，不说明任一地址或端口可连接。
- 回调中应处理空地址、IPv6 优先和请求已过期的情况。

## 知识点覆盖
异步 DNS、地址列表、取消、IPv4/IPv6、连接前置条件。
