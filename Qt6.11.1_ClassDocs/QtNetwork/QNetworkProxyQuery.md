# QNetworkProxyQuery
> Qt 6.11.1 · Qt Network · 来自 `QNetworkProxyQuery`

## 作用定位
`QNetworkProxyQuery` 把一次网络访问的目标协议、主机、端口和查询类型传给 `QNetworkProxyFactory`。

## API 速查
| API | 是做什么的 |
|---|---|
| `setUrl()` | 用 URL 描述请求目标。|
| `setPeerHostName()` / `setPeerPort()` | 设置 socket 目标。|
| `setProtocolTag()` | 设置协议标签。|
| `queryType()` | 查询访问类型。|

## 使用场景
代理工厂根据 HTTP URL、TCP 主机或 UDP 目标制定规则。

## 常见坑与经验
- URL 代理与 socket 代理的可用字段不同，工厂实现应看 query type。
- 不能假设 peer host 已经解析成数值 IP。

## 知识点覆盖
代理查询、协议类型、URL 与 socket、目标路由。
