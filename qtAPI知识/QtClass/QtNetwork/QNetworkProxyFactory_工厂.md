# QNetworkProxyFactory：按连接上下文选择代理

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QNetworkProxyFactory>`  
> CMake：`Qt6::Network`  
> 类型：抽象策略接口

## 它解决什么问题

`QNetworkProxyFactory` 根据一份 `QNetworkProxyQuery` 返回一个按优先级排序的 `QNetworkProxy` 列表。它让应用可以针对不同 URL、协议、目标主机、端口或 socket 类型选择不同代理，而不必将整个进程锁死在一条静态代理上。

它本身不连接代理，也不实现 PAC 下载或自动认证；它只做“快速、确定地给出候选代理”这一件事。

## 实际使用场景

- 公司网络中，内部域名 `NoProxy`、Web 请求走 HTTP 代理、其他 TCP 走 SOCKS5。
- 在一个 `QNetworkAccessManager` 上按请求 URL 选择代理，而不影响应用里的其他网络模块。
- 使用系统代理设置，但在诊断工具中先对某个 URL 查询候选结果。
- 为测试注入固定且可预测的代理选择策略。

只需要一条固定代理时，直接使用 `QNetworkProxy` 更简单。factory 的价值在于“每次查询都可能不同”。

## 最小自定义 factory

`queryProxy()` 必须返回至少一项。下面的策略让内部域名直连，其他请求走一个 SOCKS5 代理：

```cpp
#include <QNetworkProxyFactory>

class RoutingProxyFactory final : public QNetworkProxyFactory
{
public:
    QList<QNetworkProxy> queryProxy(
        const QNetworkProxyQuery &query) override
    {
        if (query.peerHostName().endsWith(QStringLiteral(".corp.example")))
            return {QNetworkProxy::NoProxy};

        return {QNetworkProxy(QNetworkProxy::Socks5Proxy,
                              QStringLiteral("proxy.example.com"), 1080)};
    }
};
```

返回列表的顺序就是偏好顺序。无法做出更好判断时，返回 `DefaultProxy` 而不是空列表：若 factory 装在某个 `QNetworkAccessManager` 上，这会让它继续查询应用级配置；若 factory 本身就是应用级 factory，则 `DefaultProxy` 与 `NoProxy` 含义相同。

## 设置范围与所有权

### 应用级 factory

`setApplicationProxyFactory(factory)` 安装全局 factory，并取得该对象所有权。它会覆盖任何应用级 `QNetworkProxy::setApplicationProxy()` 设置，同时使 `usesSystemConfiguration()` 返回 `false`。

由于它影响整个进程，应用入口应集中设置一次；库代码不应擅自调用这个静态函数。交出 factory 后，不要再自行释放它。

### 某个网络管理器的 factory

`QNetworkAccessManager::setProxyFactory()` 可把策略限制在一个 manager 的请求范围内，通常比应用级静态配置更可控。对于实例级 factory，查阅 manager 的生命周期规则并使其在 manager 所属线程中工作；`queryProxy()` 不应访问同一 manager 触发嵌套请求。

### 静态代理、factory 与系统配置

`QNetworkProxy::setApplicationProxy()`、`setApplicationProxyFactory()` 和 `setUseSystemConfiguration(true)` 都是在选择应用级来源，不能简单叠加：

- 设置静态应用代理会覆盖应用 factory 并禁用系统代理选择。
- 设置应用 factory 会覆盖静态应用代理并关闭系统配置状态。
- 启用系统配置会重置已经设置的应用代理或 factory，只使用平台代理设置。

将这些操作集中在应用启动阶段，避免运行时在不同模块之间反复切换。

## 系统代理查询的边界

`systemProxyForQuery()` 直接查询当前平台的系统设置；如果没有相应平台库，返回一条 `NoProxy`。`setUseSystemConfiguration(true)` 则让应用级选择只使用系统配置。

不同平台的来源并不一致：

- Windows 使用 WinHTTP；在某些系统配置下查询可能耗时数秒。
- macOS 使用 CFNetwork，按 `ftp`、`http`、`https` 的 protocol tag 应用相应代理；若配置 SOCKS，则适用于所有 query。
- 带 libproxy 的系统委托给 libproxy，可能再读取桌面设置或环境变量。
- 其他系统回退读取 `http_proxy`，其 URL scheme 必须是 `http`、`socks5` 或 `socks5h`。

因此不要在 GUI 的高频同步路径反复调用 `systemProxyForQuery()`，特别是在 Windows。代理系统设置也可能在运行中被用户或策略更改，诊断日志应记录返回结果而不是假定固定。

## 实现约束

`queryProxy()` 位于连接建立路径，应近似纯函数：

- 不做耗时网络访问、同步磁盘扫描或阻塞锁竞争。
- 不返回空列表；至少返回 `DefaultProxy` 或 `NoProxy`。
- 按可用性/偏好顺序返回候选项。
- 对 hostname、port、protocol tag 缺失的 query 有安全的默认规则。

factory 没有 QObject 线程亲和性模型，但被 Qt 网络对象调用时仍会运行在调用路径所在的线程。若策略需要可变共享状态，应自行提供同步，或将状态变为不可变快照。

## 常见误区

- **`queryProxy()` 返回空列表**：违反 API 要求，至少给一个回退代理。
- **用应用级 factory 实现某个 manager 的特例**：会影响所有 Qt socket；优先使用实例级 factory。
- **将 `DefaultProxy` 视为无代理**：它表示继续向更高层配置回退。
- **每个请求同步查询系统代理**：Windows 上可能卡住数秒。
- **以为安装 factory 后仍会叠加静态应用代理**：它们彼此覆盖。

## API 速查表

| 类别 | API | 语义与注意点 |
| --- | --- | --- |
| 构造/析构 | `QNetworkProxyFactory()` / `~QNetworkProxyFactory()` | 抽象策略接口；不能直接实例化。 |
| 核心虚函数 | `queryProxy(query)` | 必须按优先级返回至少一条 `QNetworkProxy`；无法决策时用 `DefaultProxy` 或 `NoProxy`。 |
| 全局查询 | `proxyForQuery(query)` | 静态函数，按当前全局选择链查询候选代理。 |
| 全局安装 | `setApplicationProxyFactory(factory)` | 安装应用级 factory 并取得所有权；覆盖静态应用代理和系统配置。 |
| 系统模式 | `setUseSystemConfiguration(enable)` | 启用时只使用平台代理设置，并重置已有应用代理或 factory。 |
| 系统模式 | `usesSystemConfiguration()` | 是否启用了平台系统代理选择。 |
| 系统查询 | `systemProxyForQuery(query)` | 直接查询平台代理候选；可能受平台能力限制，Windows 可能耗时数秒。 |

## 相关类型

- `QNetworkProxyQuery`：factory 的输入，描述目标和操作类型。
- `QNetworkProxy`：factory 返回的候选配置。
- `QNetworkAccessManager`：支持为单个 manager 安装 factory。
