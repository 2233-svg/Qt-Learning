# QAuthenticator：在认证挑战回调中交还凭据

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAuthenticator>`  
> CMake：`Qt6::Network`  
> 类型：可重入的认证信息值对象

## 它解决什么问题

`QAuthenticator` 是 Qt 网络层在收到服务端或代理认证挑战时传给应用的凭据载体。应用在回调中填写用户名、密码和少量认证机制相关选项，Qt 随后用这些信息继续认证流程。

它不是登录会话管理器、密码保险箱或长期凭据仓库。它的职责很窄：在一次认证挑战需要立即答复时，把认证所需信息从应用交回网络栈。

## 实际使用场景

- 服务器返回 HTTP 认证挑战时，响应 `QNetworkAccessManager::authenticationRequired()`。
- HTTP/SOCKS 等代理要求认证时，响应 `QNetworkAccessManager::proxyAuthenticationRequired()`。
- `QAbstractSocket` 使用需认证的代理时，响应其 `proxyAuthenticationRequired()`。
- 为 SPNEGO/Negotiate 设置受支持的 `spn` 选项。

不要用它持久化“记住密码”。应从操作系统凭据库、受保护的应用配置或一次性用户输入中取得凭据，只在认证回调里短暂使用。

## 正确的回调方式

认证对象必须在信号返回前被填好，因此连接必须是直接调用路径，不能使用 `Qt::QueuedConnection`：

```cpp
#include <QAuthenticator>
#include <QNetworkAccessManager>
#include <QNetworkReply>

QObject::connect(&manager, &QNetworkAccessManager::authenticationRequired,
                 &manager,
                 [](QNetworkReply *reply, QAuthenticator *authenticator) {
    Q_UNUSED(reply);
    authenticator->setUser(QStringLiteral("alice"));
    authenticator->setPassword(QStringLiteral("secret"));
});
```

`authenticator` 是 Qt 在挑战处理期间提供的借用对象。只在这个回调内读取或填写它，不要保存其指针、跨线程传递或删除它。

对代理认证使用同样原则：

```cpp
QObject::connect(&manager,
                 &QNetworkAccessManager::proxyAuthenticationRequired,
                 &manager,
                 [](const QNetworkProxy &, QAuthenticator *authenticator) {
    authenticator->setUser(QStringLiteral("proxy-user"));
    authenticator->setPassword(QStringLiteral("proxy-secret"));
});
```

## 关键语义与边界

### 不填写就是明确拒绝提供凭据

在 `QNetworkAccessManager::authenticationRequired()` 回调中，若不调用 `setUser()` 或 `setPassword()`，请求不会发送凭据，随后以 `AuthenticationRequiredError` 完成。不要为了“取消”而填空字符串，直接不设置更能表达意图。

网络管理器会缓存成功提供的服务器/代理凭据；同一方再次请求认证时，可能自动重发而不再发出认证信号。服务端拒绝这些值后，信号会再次出现。注销、账号切换或密码失效时，需要考虑 manager 的生命周期和凭据缓存影响。

### 支持的方法与选项

Qt 支持 Basic、NTLM version 2、Digest-MD5、SPNEGO/Negotiate。用户名和密码不是所有机制的全部输入：

- Basic 与 Digest-MD5 可在入站 options 中带有 `realm`，也可通过 `realm()` 读取。
- NTLM v2 当前没有额外入站/出站 options；Windows 上未设置 user 时，Qt 可尝试使用本机 `domain\user` 凭据实现单点登录。
- SPNEGO/Negotiate 目前支持出站 `spn` 选项。Windows 使用 SSPI 时，未设置它会使用默认 `HTTP/<hostname>`；其他系统使用 GSSAPI，后端默认使用 `HTTPS@<hostname>`。

`options()` / `option()` 读取服务器解析出的入站信息；`setOption()` 只设置发往认证计算的出站选项。未知出站选项不会被处理或发送，因此不要把它当作任意扩展参数通道。

### `isNull()` 不是“用户名为空”

默认构造对象尚未初始化时 `isNull()` 为 `true`。一旦调用非 const 成员、从已初始化对象构造或复制内容，该状态会改变。它用于识别对象是否进入过认证数据流程，不应用来替代 `user().isEmpty()` 或密码校验。

Qt 6.11 新增 `clear()`，用于清除所有凭据并重置为默认未初始化状态。需要尽早缩短明文凭据在内存中可达时间时可调用它，但它不是安全擦除保证。

### 值比较与复制

拷贝构造、赋值和 `operator==` / `operator!=` 比较认证对象的内容。`detach()` 是低层写时分离接口；普通应用设置 user/password/options 即可，不应为了“提高安全性”手动调用它。

## 常见误区

- **将认证信号连到 queued slot**：信号返回时认证还未填好，连接会失败。
- **保存回调传入的指针以后使用**：其有效期只覆盖当前挑战处理。
- **认为不再收到信号代表不再使用密码**：`QNetworkAccessManager` 会缓存凭据并可能自动重发。
- **把 `realm` 当成可信身份**：它是服务端提供的认证域提示，不是证书或主机校验结果。
- **用 `setOption()` 塞任意自定义字段**：只有支持的出站选项会被处理。

## API 速查表

| 类别 | API | 语义与注意点 |
| --- | --- | --- |
| 构造/析构 | `QAuthenticator()` / `~QAuthenticator()` | 创建空认证对象 / 销毁对象；通常由 Qt 在认证回调中提供实例。 |
| 值语义 | 拷贝构造、`operator=(other)` | 复制认证信息值；避免把含密码的副本扩散到长期容器。 |
| 比较 | `operator==(other)` / `operator!=(other)` | 比较认证对象内容。 |
| 凭据 | `user()` / `setUser(user)` | 读取/设置认证用户名。 |
| 凭据 | `password()` / `setPassword(password)` | 读取/设置认证密码；避免记录日志。 |
| 认证域 | `realm()` / `setRealm(realm)` | 读取/设置 realm；通常 realm 来自服务端挑战。 |
| 入站选项 | `option(name)` | 返回服务端提供的选项；不存在时为无效 `QVariant`。 |
| 入站选项 | `options()` | 返回服务器响应中解析到的全部选项。 |
| 出站选项 | `setOption(name, value)` | 设置认证计算可用的出站选项；只支持已知选项，例如 SPNEGO 的 `spn`。 |
| 状态 | `isNull()` | 是否仍是未初始化对象；不是用户名或密码是否为空的判断。 |
| 状态 | `clear()` | Qt 6.11 起清除凭据并重置为默认未初始化状态。 |
| 低层 | `detach()` | 强制内部数据分离；一般业务代码无需调用。 |

## 相关类型

- `QNetworkAccessManager::authenticationRequired`：服务器认证挑战信号。
- `QNetworkAccessManager::proxyAuthenticationRequired`：代理认证挑战信号。
- `QAbstractSocket::proxyAuthenticationRequired`：socket 代理认证信号。
- `QNetworkProxy`：代理挑战所对应的代理配置。
