# QNetworkProxyFactory
> Qt 6.11.1 · Qt Network · 来自 `QNetworkProxyFactory`

## 作用定位
`QNetworkProxyFactory` 按请求目标动态选择代理，适合 PAC、内网直连与外网代理并存的环境。

## API 速查
| API | 是做什么的 |
|---|---|
| `queryProxy()` | 必须重实现，返回候选代理列表。|
| `setUseSystemConfiguration()` | 使用系统代理设置。|
| `usesSystemConfiguration()` | 查询是否启用系统配置。|
| `setApplicationProxyFactory()` | 安装全局工厂。|

## 使用场景
企业网络中内网域名直连、公共网络经代理，按主机规则返回不同配置。

## 常见坑与经验
- `queryProxy()` 不应执行阻塞 DNS 或网络 I/O。
- 代理选择失败要有 `NoProxy` 或回退策略，避免所有请求卡死。

## 知识点覆盖
动态代理、系统代理、PAC 思路、请求路由、回退。
