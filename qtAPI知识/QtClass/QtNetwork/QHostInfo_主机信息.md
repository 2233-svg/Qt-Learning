# QHostInfo：主机名正反向解析结果

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QHostInfo>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Network)`，并链接 `Qt6::Network`  
> 类型：可复制、可移动、可重入的结果值类型

## 它解决什么问题

`QHostInfo` 使用操作系统的名称解析机制，在主机名与 IP 地址之间做正向或反向查询。它既是异步 `lookupHost()` 回调收到的结果类型，也可由阻塞式 `fromName()` 返回。

它适合“把服务域名解析为地址列表”或“把数值 IP 反查为名称”。它不查询 MX、SRV、TXT、TLSA 等 DNS 记录，也不控制具体 DNS 服务器；这些需求应使用 `QDnsLookup`。

## 实际使用场景

- 客户端在后台异步解析 API 主机名，然后依据 IPv4/IPv6 列表发起连接。
- 日志或诊断工具对远端 IP 做 PTR 反向解析。
- 仅在工作线程或命令行短任务中使用 `fromName()` 进行同步解析。
- 获取机器 host name 与 DNS domain，作为诊断信息或默认标识。

`QHostInfo` 依赖操作系统解析器、hosts 文件、DNS 缓存和平台策略。它不保证返回域名登记的全部地址，地址顺序也不应被当作可靠优先级或负载均衡策略。

## 优先使用异步 lookup

```cpp
const int lookupId = QHostInfo::lookupHost(
    u"api.example.com"_qs, this,
    [this](const QHostInfo &info) {
        if (info.error() != QHostInfo::NoError) {
            reportResolveError(info.errorString());
            return;
        }

        for (const QHostAddress &address : info.addresses())
            tryConnect(address);
    });
```

带 `context` 的 functor 重载最安全：如果 context 在查询完成前销毁，callback 不会执行；callback 在 context 所在线程运行，且该线程必须有运行中的 Qt 事件循环。

不带 context 的 functor 会在发起 `lookupHost()` 的线程回调，同样要求该线程有事件循环。它更容易在对象销毁后捕获悬垂指针，除非 lambda 不引用任何短生命周期状态，否则不建议在 UI/对象代码中使用。

多个 lookup 并发时，完成顺序不保证与发起顺序一致。业务代码必须以 `lookupId()`、请求自身的 token 或 captured context 匹配结果，而不能按“第 N 个完成对应第 N 个请求”处理。

## 取消与阻塞查询

`lookupHost()` 返回 lookup ID，可传给 `abortHostLookup(id)` 取消。取消是尽力取消：调用后不要假定旧回调一定不会在竞态中到达；带 context 的 callback 仍应确认当前请求 token，避免旧结果覆盖新 UI 状态。

`fromName()` 会阻塞当前线程直到解析完成。绝不能在 GUI 线程、主要事件循环线程或持有关键锁时调用，否则会冻结界面或放大死锁风险。若必须同步解析，将它放到明确管理的工作线程中。

传入字面 IP 地址时，`lookupHost()` / `fromName()` 执行反向查找。成功结果包含解析出的主机名和关联 IP 地址；PTR 记录缺失或不可信都很常见，不能把反向名称当作身份认证。

## 结果与错误

| `HostInfoError` | 含义 |
| --- | --- |
| `NoError` | 查询成功；地址列表仍可能为空，业务应按实际需求判断。 |
| `HostNotFound` | 找不到主机的 IP 地址。 |
| `UnknownError` | 其他解析器/平台错误。 |

先检查 `error()`，再消费 `addresses()`。`errorString()` 是可读诊断文本，程序分支应使用枚举值。系统解析器按 RFC 6724 等策略工作，不保证返回所有注册地址，因此不能基于“没有返回某地址族”推断 DNS 中一定不存在它。

`QHostInfo` 支持 IDN（IDNA/Punycode）。仍应将域名输入按业务安全策略规范化和验证；解析成功不等于它属于受信任的 origin。

## 本机名称的边界

`localHostName()` 返回本机配置的主机名，未必全局唯一，也不保证是 FQDN。若确实需要从它推导可解析全名，需再进行名称解析并处理失败。

`localDomainName()` 返回机器的 DNS domain；它与 Windows 网络域（如 AD 域）不是同一个概念，不能混用来做身份或组织归属判断。

## API 速查表

| 类别 | API | 语义与使用重点 |
| --- | --- | --- |
| 枚举 | `HostInfoError` | `NoError`、`HostNotFound`、`UnknownError`；先检查它再读取地址。 |
| 构造 | `QHostInfo(int lookupId = -1)` | 构造空结果，附带可选 lookup ID。 |
| 构造与赋值 | 复制/移动构造、复制/移动 `operator=`、`swap()` | 复制或转移结果值；移动后原对象只应销毁或重新赋值。 |
| 结果 | `hostName()` / `setHostName()` | 读写主机名字段；反向解析成功时可得到名称。 |
| 结果 | `addresses()` / `setAddresses()` | 读写 `QHostAddress` 列表；系统不保证完整列表或排序。 |
| 结果 | `error()` / `setError(HostInfoError)` | 读写错误枚举；正常结果为 `NoError`。 |
| 结果 | `errorString()` / `setErrorString(const QString &)` | 读写可读错误文本；只用于诊断，不作为稳定逻辑条件。 |
| 关联 ID | `lookupId()` / `setLookupId(int)` | 读取/设置 lookup ID；异步请求取消和结果匹配使用。 |
| 异步解析 | `lookupHost(const QString &, const QObject *receiver, const char *member)` | 以成员函数/槽接收 `QHostInfo`；返回可取消的 ID。 |
| 异步解析 | `lookupHost(const QString &, const QObject *context, Functor)` | 推荐重载；context 销毁时不调用 callback，在 context 线程回调，线程必须有事件循环。 |
| 异步解析 | `lookupHost(const QString &, Functor)` | 无 context 回调，运行在发起线程；需自行保证捕获对象生命周期。 |
| 取消 | `abortHostLookup(int id)` | 请求取消；仍应使用 token/context 防范已经排队的旧结果竞争。 |
| 同步解析 | `fromName(const QString &)` | 阻塞查询；只用于非 UI、非关键事件线程。传 IP 文本时执行反向解析。 |
| 本机信息 | `localHostName()` | 返回本机主机名，不保证 FQDN 或全局唯一。 |
| 本机信息 | `localDomainName()` | 返回 DNS domain，不等于 Windows 网络域。 |

## 一句话总结

`QHostInfo` 是系统 DNS 名称解析的异步结果接口：优先使用带 context 的 `lookupHost()`，按错误和请求 token 消费不保证顺序的地址列表，把同步 `fromName()` 留在工作线程。
