# QNetworkRequestFactory：批量生成共享配置的网络请求

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QNetworkRequestFactory>`  
> CMake：`Qt6::Network`  
> 自 Qt 6.7 起提供  
> 类型：隐式共享值类型

## 它解决什么问题

`QNetworkRequestFactory` 将一组稳定的远程 API 配置集中起来：base URL、公共头、Bearer token、认证用户名密码、查询参数、SSL 配置、传输超时、优先级和 request attributes。每次只提供变化的 path 或 query，即可得到独立的 `QNetworkRequest`。

它解决的不是发请求，而是避免 API 客户端在每个端点手写重复 URL 拼接、认证头和安全策略。最终仍由 `QNetworkAccessManager` 或 `QRestAccessManager` 执行返回的 request。

## 实际使用场景

- 一个 REST API 的所有端点共享 `https://api.example.com/v2`、Accept 头、Bearer token 和超时。
- token 刷新后，后续请求自动使用最新 token，不必逐个修改端点函数。
- 所有请求统一设置 TLS 配置、缓存属性或后台优先级。
- 测试中建立可复制的 factory，为不同测试只覆盖 path/query。

它适合“同一远端服务的一族请求”。不同账号、不同安全域或不同代理策略应使用不同 factory，避免凭据和公共头交叉污染。

## 基本使用

```cpp
#include <QNetworkAccessManager>
#include <QNetworkRequestFactory>
#include <QUrl>
#include <QUrlQuery>

QNetworkRequestFactory api(
    QUrl(QStringLiteral("https://api.example.com/v2")));
api.setBearerToken("access-token");
api.setTransferTimeout(std::chrono::seconds(15));

QUrlQuery query;
query.addQueryItem(QStringLiteral("page"), QStringLiteral("1"));

const QNetworkRequest request =
    api.createRequest(QStringLiteral("models"), query);
QNetworkReply *reply = manager.get(request);
```

上例生成 `https://api.example.com/v2/models?page=1`。base URL 自带的路径会成为前缀；传入 `"models"` 和 `"/models"` 都会追加到这个前缀，而不是把路径重置到站点根目录。

## 关键语义与边界

### factory 是模板配置，生成结果是独立快照

调用 `createRequest()` 时，factory 的当前配置被写入一个独立 `QNetworkRequest`。之后修改 token、公共头或查询参数，只影响**未来**生成的 request；已经生成或已经交给 manager 的 request 不会回写更新。

这种边界很适合 token 刷新：刷新完成后 `setBearerToken(newToken)`，后续请求自动变更；不应期待飞行中的请求被替换凭据。

### URL 拼接和查询参数合并

base URL 可以包含路径，如 `https://example.com/v2`，这个路径会成为后续 path 的前缀。`createRequest(path, query)` 会合并：

1. base URL 中已有的 query；
2. factory 的 `queryParameters()`；
3. path 中自带的 query；
4. 本次传入的 `QUrlQuery`。

重复 query key 是否有业务意义由服务器定义，不能假设后出现的项目总会覆盖早出现的项目。涉及签名、分页或 API key 时，应在生成前检查最终 URL。

### Bearer token 的优先级

设置 bearer token 后，生成 request 会带 `Authorization: Bearer <token>`。它不会显示在 `commonHeaders()` 的返回值里；若公共头中也有 `Authorization`，Bearer token 会覆盖该公共头。

token 通常会过期，刷新后应立即再次调用 `setBearerToken()`。不要在 factory 的 `QDebug` 输出、崩溃日志或可导出的配置中泄露 token。

### 用户名与密码会进入 URL

`setUserName()` 和 `setPassword()` 会在 `createRequest()` 时写入请求 URL 的 user-info，随后 `QNetworkAccessManager` / `QRestAccessManager` 会在服务器要求认证时尝试使用这些凭据。

URL 很容易进入日志、浏览器历史、调试输出和错误报告。优先使用认证挑战回调与受保护凭据来源；只有在明确受控且能防止 URL 泄露的场景下才在 factory 中保存 user/password。用完后调用相应 `clear...()`，但这不是安全擦除保证。

### 公共 headers、SSL、超时与 attributes

`setCommonHeaders()` 为每个生成请求复制结构化 `QHttpHeaders`。用 `clearCommonHeaders()` 整体清除，不能把它当成每次请求的动态 header 容器；会变化的 request-id、时间戳和幂等键应在 `createRequest()` 后写到那一个 request。

`setSslConfiguration()`、`setTransferTimeout()`、`setPriority()` 和 `setAttribute()` 都只影响以后创建的 request。请求级 transfer timeout 是“无字节传输进展”的超时，0 表示禁用；其具体行为见 `QNetworkRequest`。

### 复制与移动

factory 是隐式共享值类型，拷贝后按值使用。移动构造或移动赋值后的源对象处于部分形成状态，只能析构或重新赋值，不能继续调用 `createRequest()` 或读取其配置。

## 常见误区

- **以为 `/path` 会覆盖 base URL 的 `/v2`**：两种前导斜杠写法都会追加。
- **更新 token 后期待旧 request 自动更新**：只影响之后 `createRequest()` 的结果。
- **把 `Authorization` 放在 common headers 又设置 bearer token**：Bearer 会覆盖它。
- **忽略 username/password 会进 URL**：这容易造成凭据日志泄露。
- **将 factory 用作并发可变全局对象**：它是值类型，但并发读写同一个实例仍需自行同步。

## API 速查表

| 类别 | API | 语义与注意点 |
| --- | --- | --- |
| 构造 | `QNetworkRequestFactory()` | 创建空 factory；先设置有效 base URL。 |
| 构造 | `QNetworkRequestFactory(baseUrl)` | 设置 base URL；其中 path 成为以后 path 的前缀。 |
| 值语义 | 拷贝构造、拷贝/移动赋值、`swap(other)` | 复制配置；移动后的源对象只可析构或重新赋值。 |
| 析构 | `~QNetworkRequestFactory()` | 普通值类型析构。 |
| base URL | `baseUrl()` / `setBaseUrl(url)` | 读取/设置生成 request 的基础 URL。 |
| 生成 | `createRequest()` | 用当前 base URL、公共配置生成 request。 |
| 生成 | `createRequest(path)` | 将 path 追加到 base URL 的路径前缀。 |
| 生成 | `createRequest(query)` | 为 base URL 附加 query。 |
| 生成 | `createRequest(path, query)` | 合并 base、factory、path 和本次 query，生成完整 request。 |
| 公共头 | `commonHeaders()` / `setCommonHeaders(headers)` | 读取/设置要复制到每个请求的 `QHttpHeaders`。 |
| 公共头 | `clearCommonHeaders()` | 清空所有公共头。 |
| Bearer | `bearerToken()` / `setBearerToken(token)` | 读取/设置 token；生成 `Authorization: Bearer` 并覆盖同名公共头。 |
| Bearer | `clearBearerToken()` | 移除未来请求的 Bearer token。 |
| 用户名 | `userName()` / `setUserName(name)` / `clearUserName()` | 管理 URL user-info 中的用户名；注意敏感信息泄露面。 |
| 密码 | `password()` / `setPassword(password)` / `clearPassword()` | 管理 URL user-info 中的密码；注意敏感信息泄露面。 |
| 超时 | `transferTimeout()` / `setTransferTimeout(milliseconds)` | 读取/设置以后请求的无进展 transfer timeout。 |
| 查询参数 | `queryParameters()` / `setQueryParameters(query)` / `clearQueryParameters()` | 管理每个请求追加的 query 参数。 |
| 优先级 | `priority()` / `setPriority(priority)` | Qt 6.8 起管理未来请求优先级；默认 `NormalPriority`。 |
| 属性 | `attribute(attribute)` / `attribute(attribute, defaultValue)` | Qt 6.8 起读取 factory 保存的 request attribute。 |
| 属性 | `setAttribute(attribute, value)` | Qt 6.8 起设置要复制到未来 request 的 attribute，重复设置覆盖旧值。 |
| 属性 | `clearAttribute(attribute)` / `clearAttributes()` | Qt 6.8 起清除一个 / 全部保存的 attributes。 |
| SSL | `sslConfiguration()` / `setSslConfiguration(config)` | 读取/设置会复制给每个生成 request 的 TLS 配置；仅 SSL 构建可用。 |
| 调试 | `operator<<(QDebug, factory)` | 输出 factory 调试信息；避免在敏感日志中使用。 |

## 相关类型

- `QNetworkRequest`：factory 的创建结果。
- `QNetworkAccessManager` / `QRestAccessManager`：执行创建出的 request。
- `QUrlQuery`：合并常驻与单次 query 参数。
- `QHttpHeaders`：公共结构化 HTTP 头。
