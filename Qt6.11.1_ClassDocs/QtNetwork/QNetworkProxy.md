# QNetworkProxy
> Qt 6.11.1 · Qt Network · 来自 `QNetworkProxy`

## 作用定位
`QNetworkProxy` 是代理服务器的值类型描述，包含代理类型、主机、端口和认证信息。

## API 速查
| API | 是做什么的 |
|---|---|
| `setType()` | 选择 HTTP、SOCKS5 等代理类型。|
| `setHostName()` / `setPort()` | 设置代理端点。|
| `setUser()` / `setPassword()` | 设置代理凭据。|
| `applicationProxy()` | 读取全局应用代理。|
| `setApplicationProxy()` | 设置全局代理。|

## 使用场景
企业网络代理、测试流量转发或 SOCKS 隧道。

## 常见坑与经验
- 代理密码也是凭据，避免硬编码。
- 全局代理影响所有使用 Qt 网络栈的组件；局部需求优先在具体 manager/socket 配置。

## 知识点覆盖
HTTP 代理、SOCKS、凭据、全局配置、网络隔离。
