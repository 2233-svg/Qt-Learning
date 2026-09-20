# QNetworkCookie：一条 HTTP Cookie 的值对象

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QNetworkCookie>`  
> CMake：`Qt6::Network`  
> 类型：隐式共享值类型

## 它解决什么问题

`QNetworkCookie` 描述一条 HTTP Cookie：名字和值、适用的 domain/path、过期时间，以及 `Secure`、`HttpOnly`、`SameSite` 等属性。它是 `QNetworkCookieJar` 存放和 `QNetworkAccessManager` 在请求/响应过程中传递的基本数据单元。

Cookie 用于让 HTTP 这类无状态协议在多次请求间携带少量状态。`QNetworkCookie` 本身不维护全局会话，不会自动落盘，也不会直接发送网络请求；它只是一个可复制的 Cookie 值。

## 实际使用场景

- 从 `QNetworkReply` 的 Cookie 相关头读取服务端返回的会话信息。
- 在测试、受控内部服务或迁移工具中构造 Cookie 并放入 `QNetworkCookieJar`。
- 解析原始 `Set-Cookie` 值，检查服务端实际下发的属性。
- 为自定义持久化 Cookie Jar 序列化和恢复 Cookie 数据。

不要把 Cookie 的 `value()` 当作应用可自由解释的业务字段。Qt 将 name/value 视为不透明字节；它们的含义、编码和保密要求由服务端协议决定。

## 创建、规范化与放入 Cookie Jar

手工创建 Cookie 时，应该给出名字，并让 jar 用来源 URL 补全未指定的 domain/path：

```cpp
#include <QNetworkCookie>
#include <QNetworkCookieJar>
#include <QUrl>

QNetworkCookie session("session", "opaque-token");
session.setSecure(true);
session.setHttpOnly(true);
session.setSameSitePolicy(QNetworkCookie::SameSite::Lax);

QNetworkCookieJar jar;
const QUrl source(QStringLiteral("https://api.example.com/v1/login"));
jar.setCookiesFromUrl({session}, source);
```

空名字会使 Cookie 无效；空 value 仍然有效，且可能具有服务端定义的特殊含义。`setCookiesFromUrl()` 会先对 Cookie 规范化：仅当 domain 或 path 原先为空时，才依据来源 URL 补齐它们。

## 关键语义与边界

### domain、path 与“同一个 Cookie”

Cookie 的标识符是 **name、domain、path** 三元组。`hasSameIdentifier()` 只比较这个三元组；`operator==` 则要求所有字段都相等。因此更新 jar 中的 Cookie 时，不能只按 name 判断。

`domain()` 可能以 `.` 开头。这样的文本本身不是合法主机名，但表达“匹配以该后缀结尾的主机”。不要把它直接交给 DNS 或主机校验 API。

`normalize(url)` 只补全之前为空的 domain/path，不会替你修正已经设置但不正确的显式值。对于从响应接收的 Cookie，优先交给 `QNetworkCookieJar::setCookiesFromUrl()`，让 jar 在来源 URL 上执行它的标准流程。

### 会话 Cookie、持久 Cookie 与过期

没有有效到期时间的 Cookie 是会话 Cookie：`isSessionCookie()` 返回 `true`，`expirationDate()` 返回无效的 `QDateTime`。调用 `setExpirationDate()` 传入无效日期也会把 Cookie 变成会话 Cookie。

返回过去时间的 `expirationDate()` 表示它已经过期，不应再发给远端。Cookie 是否跨应用重启保留不是 `QNetworkCookie` 决定的：默认 `QNetworkCookieJar` 只在内存中保存，进程结束时所有内容都会丢弃。

### Secure、HttpOnly、SameSite 不是同一种安全机制

- `Secure`：Cookie 不应通过未加密连接重新发送。它不是对 TLS 证书的验证，也不会使一个 HTTP URL 自动变成 HTTPS。
- `HttpOnly`：在浏览器中限制脚本读取该 Cookie。对于 C++ 程序，调用 `value()` 仍能读到数据；因此它不是保护本进程内存的访问控制。
- `SameSite`：Qt 6.1 起可保存 `Default`、`None`、`Lax`、`Strict`。这是浏览器生态的跨站发送策略属性；不要假定通用网络客户端会替应用实现浏览器完整的站点上下文模型。

现代浏览器通常要求 `SameSite=None` 同时标记 `Secure`；即使目标是非浏览器客户端，服务端兼容策略也值得遵守。

### 原始表单与解析

`toRawForm(NameAndValueOnly)` 只产生 `NAME=VALUE`，适合组织请求的 `Cookie` 头。`toRawForm(Full)` 产生完整属性，适合 `Set-Cookie` 形式，且只有完整形式可以无损再解析。

`parseCookies(QByteArrayView)` 解析来自响应 `Set-Cookie` 的原始值，成功时可返回多条 Cookie，解析出错时返回空列表。在 `QNetworkReply` 中收到的 Cookie 已经由 Qt 解析，通常无需重复解析原始头文本。

Qt 的实现基于较早的 Netscape Cookie 规范及 `HttpOnly` 扩展；`Set-Cookie2` 对应的 RFC 2965 不受支持。需要严格复现现代浏览器的全套 Cookie 策略时，必须自行验证目标行为。

### 值语义

该类是隐式共享值类型，可安全复制、赋值、交换并存储在 Qt 容器中。它没有 QObject 父子关系，也不绑定事件循环。`swap()` 是无异常且高效的值交换。

## 常见误区

- **认为空 value 就无效**：只有空 name 使 Cookie 无效。
- **用 `operator==` 判断“是否应覆盖”**：覆盖身份应使用 name/domain/path，也就是 `hasSameIdentifier()`。
- **把 `HttpOnly` 当成 C++ 代码不可访问**：它是浏览器脚本模型中的属性。
- **保存 Cookie 时忽略 session 和过期状态**：持久化前应按应用会话规则丢弃会话 Cookie，并过滤过期 Cookie。
- **把 `NameAndValueOnly` 输出再当作完整 Cookie 解析**：该形式没有 domain、path、过期时间等属性，不能无损恢复。

## API 速查表

| 类别 | API | 语义与注意点 |
| --- | --- | --- |
| 枚举 | `RawForm::NameAndValueOnly` | 只输出 `NAME=VALUE`，适合客户端 `Cookie` 头；多个 Cookie 由调用方按分号组织。 |
| 枚举 | `RawForm::Full` | 输出完整 Cookie 属性，适合 `Set-Cookie` 形式，也是可无损再解析的形式。 |
| 枚举 | `SameSite::Default` | Qt 6.1 起；未设置 SameSite，外部客户端可能按 None 或 Lax 解释。 |
| 枚举 | `SameSite::None` | 可在所有上下文发送；现代浏览器通常要求同时为 Secure。 |
| 枚举 | `SameSite::Lax` | 第一方请求及第三方发起的 GET 等较宽松场景。 |
| 枚举 | `SameSite::Strict` | 仅第一方上下文发送。 |
| 构造 | `QNetworkCookie(name, value)` | 创建 Cookie；name 不能为空才有效，value 可为空。 |
| 值语义 | 拷贝构造、拷贝/移动赋值、`swap(other)` | 隐式共享值操作；不涉及网络 I/O 或 QObject 所有权。 |
| 生命周期 | `~QNetworkCookie()` | 普通值类型析构。 |
| 名值 | `name()` / `setName(name)` | 读取/设置名字；设置为空字节数组会使 Cookie 无效。 |
| 名值 | `value()` / `setValue(value)` | 读取/设置不透明值；空值仍可能是有效 Cookie。 |
| 作用域 | `domain()` / `setDomain(domain)` | 读取/设置 domain；前导点表示后缀匹配语义，不能当普通主机名。 |
| 作用域 | `path()` / `setPath(path)` | 读取/设置 URL 路径匹配范围。 |
| 作用域 | `normalize(url)` | 仅补全原本为空的 domain/path；不会修复显式设置的错误范围。 |
| 身份 | `hasSameIdentifier(other)` | 比较 name、domain、path 三元组；用于更新、删除和去重。 |
| 生命周期 | `expirationDate()` | 返回到期时间；会话 Cookie 返回无效 `QDateTime`，过去时间表示已过期。 |
| 生命周期 | `setExpirationDate(date)` | 设置到期时间；无效日期表示会话 Cookie。 |
| 生命周期 | `isSessionCookie()` | 是否没有有效到期时间。 |
| 安全属性 | `isSecure()` / `setSecure(enable)` | 查询/设置 Secure；它表达不应走未加密连接，不替代 TLS 证书验证。 |
| 安全属性 | `isHttpOnly()` / `setHttpOnly(enable)` | 查询/设置 HttpOnly；限制浏览器脚本，不限制 C++ 调用 `value()`。 |
| 安全属性 | `sameSitePolicy()` / `setSameSitePolicy(policy)` | Qt 6.1 起读取/设置 SameSite 属性。 |
| 序列化 | `toRawForm(form)` | 转为 HTTP 头适用的字节形式；按需求选名称值或完整形式。 |
| 解析 | `parseCookies(QByteArrayView)` | 静态解析 `Set-Cookie` 文本；错误返回空列表。Qt 6.7 前参数为 `QByteArray`。 |
| 比较 | `operator==(other)` / `operator!=(other)` | 比较所有 Cookie 字段；不等同于“同一标识符”。 |
| 调试 | `operator<<(QDebug, cookie)` | 非禁用 debug stream 的构建下可输出调试表示；日志中避免泄露 Cookie value。 |

## 相关类型

- `QNetworkCookieJar`：按 URL 选择、接收和存放多条 Cookie。
- `QNetworkAccessManager`：使用 jar 自动将 Cookie 加入请求并接收响应 Cookie。
- `QNetworkReply`：网络响应中的 Cookie 已由 Qt 解析，可直接读取相关头信息。
