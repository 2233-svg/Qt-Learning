# QHstsPolicy：描述一条 HSTS 主机策略

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QHstsPolicy>`  
> CMake：`Qt6::Network`  
> 类型：可复制的值类型

## 它解决什么问题

`QHstsPolicy` 表示一条 HTTP Strict Transport Security（HSTS，RFC 6797）策略：某个主机在一段有效期内只能被安全地访问，以及这条约束是否扩展到其子域名。

它**不发请求、不解析 DNS、也不自行升级 URL**。它只是策略数据；`QNetworkAccessManager` 才是保存并执行 HSTS 策略的一方。把它交给网络管理器后，管理器会在策略有效期内避免以不安全方式访问相应主机。

一条策略由三个互相独立的字段构成：

- `host`：适用的主机名；
- `expiry`：UTC 到期时刻；
- `IncludeSubDomains`：是否连同子域名一起适用。

## 实际使用场景

- 内部 HTTPS 服务需要预置 HSTS，而不想等待服务端第一次返回 `Strict-Transport-Security` 响应头。
- 程序从受信任的配置或持久化存储恢复 HSTS 白名单，然后通过 `QNetworkAccessManager` 导入。
- 管理器导出已有策略后，在 UI 或诊断日志中检查某个域名的安全访问约束。

不要把它当作证书校验或网络访问权限控制工具。HSTS 只约束 HTTP/HTTPS 的访问方式；TLS 证书是否可信仍由 SSL 配置和证书验证流程决定。

## 使用模型

通常先生成值对象，再将其设置到网络管理器：

```cpp
#include <QDateTime>
#include <QHstsPolicy>
#include <QNetworkAccessManager>

QNetworkAccessManager manager;

const QDateTime expiry = QDateTime::currentDateTimeUtc().addDays(30);
QHstsPolicy policy(expiry, QHstsPolicy::IncludeSubDomains,
                   QStringLiteral("api.example.com"));

manager.addStrictTransportSecurityHosts({policy});
manager.setStrictTransportSecurityEnabled(true);
```

这里的到期时间必须按 UTC 理解。若策略来自服务器响应头，通常无需手动构造；手动创建更适合“预加载”或从可信存储恢复的场景。

## 关键语义与边界

### 主机名不是任意 URL

`setHost()` 和带主机参数的构造函数只接收主机组成部分，例如 `api.example.com`，而不是 `https://api.example.com/path`。其解析规则由 `QUrl::ParsingMode` 决定，读取时可用 `QUrl::ComponentFormattingOptions` 指定输出形式。

默认的 `QUrl::DecodedMode` 适合已经按解码文本处理的输入；若主机来自 URL 的原始编码内容，应先明确编码边界，避免把百分号编码又当作普通文本解释。

### 过期策略只是数据，导入时应过滤

`isExpired()` 仅根据当前时间判断 `expiry()` 是否已经过去。它不清理任何管理器中的记录，也不替应用删除持久化数据。导入或恢复列表前应丢弃已过期条目：

```cpp
QList<QHstsPolicy> usable;
for (const QHstsPolicy &policy : storedPolicies) {
    if (!policy.isExpired())
        usable.append(policy);
}
manager.addStrictTransportSecurityHosts(usable);
```

### 子域名标记不能替代域名边界判断

`IncludeSubDomains` 的含义是策略还适用于该主机的子域名；它不是字符串前缀匹配。例如 `example.com` 与 `notexample.com` 没有父子域关系。不要在应用层用 `startsWith()` 复刻这个规则，交给 HSTS 实现处理。

### 值对象的比较与共享

该类是隐式共享的值类型，可复制、赋值和放入 Qt 容器。`swap()` 和移动赋值适合高效调换对象内容；`operator==` / `operator!=` 比较的是策略值本身。它不持有 `QNetworkAccessManager`，也没有事件循环或线程亲和性要求。

## 常见误区

- **把 HSTS 当作“能否联网”的判断条件**：HSTS 只影响安全访问策略，不代表域名可达。
- **传入完整 URL 作为 host**：应只传主机部分；协议、端口、路径不属于策略主机名。
- **使用本地时间构造 expiry**：接口和 HSTS 语义按 UTC，使用 `currentDateTimeUtc()`。
- **以为 `setIncludesSubDomains()` 会立即影响请求**：只有把策略交给启用 HSTS 的 `QNetworkAccessManager` 后，网络访问才会受影响。

## API 速查表

| 类别 | API | 语义与注意点 |
| --- | --- | --- |
| 枚举 | `PolicyFlag::IncludeSubDomains` | 表示策略同时适用于子域名；可组成 `PolicyFlags`。 |
| 构造 | `QHstsPolicy()` | 创建默认策略；在填入有效 host 和 expiry 前不应将其视作可用 HSTS 记录。 |
| 构造 | `QHstsPolicy(expiry, flags, host, mode)` | 以 UTC 到期时间、子域名标记和主机名构造；`mode` 决定如何解释主机文本。 |
| 值语义 | 拷贝构造、`operator=(const QHstsPolicy &)`, 移动赋值 | 复制或转移策略值，不与任何网络管理器建立所有权关系。 |
| 生命周期 | `~QHstsPolicy()` | 普通值类型析构，无 I/O 或异步收尾。 |
| 主机 | `setHost(host, mode)` | 设置目标主机；只给 host，不给完整 URL。 |
| 主机 | `host(options) const` | 按指定 URL 组件格式选项返回主机文本，默认完全解码。 |
| 有效期 | `setExpiry(expiry)` | 设置 UTC 到期时刻。 |
| 有效期 | `expiry() const` | 返回当前记录的 UTC 到期时间。 |
| 有效期 | `isExpired() const` | 根据当前时间判断是否过期；不自动移除外部存储或管理器中的记录。 |
| 子域名 | `setIncludesSubDomains(include)` | 设置是否覆盖子域名。 |
| 子域名 | `includesSubDomains() const` | 查询子域名覆盖标志。 |
| 值操作 | `swap(other)` | 无异常交换两条策略，适合实现移动或批量整理。 |
| 比较 | `operator==(lhs, rhs)` | 比较两条策略的值是否相等。 |
| 比较 | `operator!=(lhs, rhs)` | 相等比较的否定。 |

## 相关类型

- `QNetworkAccessManager`：通过其 HSTS 相关接口导入、启用和查询策略。
- `QUrl`：主机输入和输出格式的解析规则来源。
- `QDateTime`：策略到期时间；应使用 UTC。
