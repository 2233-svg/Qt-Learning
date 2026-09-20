# QNetworkRequestFactory
> Qt 6.11.1 · Qt Network · 来自 `QNetworkRequestFactory`

## 作用定位
`QNetworkRequestFactory` 用统一基地址、公共请求头和认证信息构建多个 `QNetworkRequest`，避免 REST 客户端把 token、版本头和 URL 拼接散落到各处。

## API 速查
| API | 是做什么的 |
|---|---|
| `setBaseUrl()` | 设置 API 根地址。|
| `setCommonHeaders()` | 设置每个请求共有头。|
| `setBearerToken()` | 设置 Bearer 认证令牌。|
| `createRequest()` | 从相对路径创建完整请求。|
| `setTransferTimeout()` | 设置默认传输超时。|

## 使用场景
应用启动时建立一个 factory，所有 `/v1/...` 请求从它派生，令牌刷新时仅更新一处。

## 常见坑与经验
- 基地址末尾斜杠与相对路径开头斜杠会影响 URL 合并结果；测试一条真实 URL。
- token 更换后旧 request 不会自动更新；它们已是独立值对象。

## 知识点覆盖
客户端配置、基 URL、认证头、请求复用、URL 解析。
