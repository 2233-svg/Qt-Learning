# QNetworkInformation
> Qt 6.11.1 · Qt Network · 来自 `QNetworkInformation`

## 作用定位
`QNetworkInformation` 提供平台网络状态信息，例如可达性、传输介质与当前后端，帮助应用调整重试与同步策略。

## API 速查
| API | 是做什么的 |
|---|---|
| `loadDefaultBackend()` | 加载平台默认信息后端。|
| `instance()` | 取得当前信息实例。|
| `reachability()` | 查询无网络、局域网或互联网可达性。|
| `transportMedium()` | 查询 Wi-Fi、以太网、蜂窝等介质。|
| `isBehindCaptivePortal()` | 查询是否可能在认证门户后。|
| `reachabilityChanged()` | 监听状态变化。|

## 使用场景
离线优先应用在网络恢复后排队同步；检测 captive portal 后提示用户登录网络。

## 常见坑与经验
- reachability 是系统层启发信息，不保证某个目标域名真的可访问。
- 不能因为显示 Wi-Fi 就假设成本低或稳定，用户策略仍应允许控制。

## 知识点覆盖
网络状态、离线优先、认证门户、传输介质、重试策略、平台后端。
