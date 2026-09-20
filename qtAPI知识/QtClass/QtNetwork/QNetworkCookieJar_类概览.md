# QNetworkCookieJar：按 URL 管理 HTTP Cookie 的容器

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QNetworkCookieJar>`  
> CMake：`Qt6::Network`  
> 继承：`QObject`

## 它解决什么问题

`QNetworkCookieJar` 保存多条 `QNetworkCookie`，并回答两个核心问题：

1. 即将向某个 URL 发请求时，哪些 Cookie 应附加到请求中？
2. 某个 URL 的响应返回了 Cookie 时，哪些应被接收并怎样更新现有记录？

`QNetworkAccessManager` 会在发送请求前调用 `cookiesForUrl()`，收到响应 Cookie 时调用 `setCookiesFromUrl()`。因此它是 Qt HTTP 会话状态的集中策略点，而不是单纯的 `QList<QNetworkCookie>`。

## 实际使用场景

- 一个 `QNetworkAccessManager` 维持登录会话、语言偏好或服务端下发的状态。
- 为桌面应用实现持久化 Cookie：派生 jar，在适当时机用 `allCookies()` 写入自己的存储，并在启动时用 `setAllCookies()` 恢复。
- 为隐私、租户隔离或测试环境定制 Cookie 接收/发送策略。
- 测试请求是否携带了正确的 domain/path 范围 Cookie。

默认 jar 不是浏览器级隐私策略，也不会自动保存到磁盘。它只在内存中保存，并接受来自请求的 Cookie，再做基础的 domain/path 匹配。

## 与 QNetworkAccessManager 的正确组合

Cookie Jar 应在交给网络管理器前完成配置：

```cpp
#include <QNetworkAccessManager>
#include <QNetworkCookieJar>

auto *manager = new QNetworkAccessManager(this);
auto *jar = new QNetworkCookieJar;

manager->setCookieJar(jar); // manager 取得 jar 所有权
```

`QNetworkAccessManager::setCookieJar()` 取得传入对象的所有权。若 jar 与 manager 在同一线程，manager 会把它设为自己的 QObject 子对象，并随 manager 析构。不要在调用后再用智能指针或其他 owner 单独释放 jar。

网络管理器只能在它所属线程使用；jar 又会在其请求链中被调用。因此自定义 jar、读写持久化数据、修改 Cookie 的操作都应安排在 manager 所在线程，跨线程请求使用 queued signal/slot 或消息分发，而不是并发访问同一个 jar。

## 默认策略的实际含义

### 内存存储，不做持久化

默认实现初始化为空，销毁时丢弃全部 Cookie。若应用要跨启动保留 Cookie，必须派生 `QNetworkCookieJar`，选择自己的存储格式并处理加密、权限、会话 Cookie、过期 Cookie 和写入失败。

`allCookies()` / `setAllCookies()` 是给派生类的受保护接口：前者导出当前整个列表，后者批量恢复。它们绕开了“从某个 URL 接收 Cookie”的语义，不应暴露给任意业务代码作为无约束写入口。

### 接收和发送是两条不同的策略链

默认 `setCookiesFromUrl(cookieList, url)` 会在插入前规范化 Cookie，并检查其 domain/path 是否与来源 URL 合法；至少成功设置一条时返回 `true`。同一标识符（name/domain/path）的记录会被新 Cookie 覆盖。

默认 `cookiesForUrl(url)` 返回适合发送给该 URL 的 Cookie；若同名 Cookie 的 path 不同，path 更长的条目排在前面。不要自行打乱该顺序，否则可能改变服务端对同名 Cookie 的解释。

默认实现只有 Cookie 规范建议的基础安全检查，并没有独立的“接受策略”，不会替应用实现第三方 Cookie 禁用、站点隔离、同意管理或容量配额。

### 容量和清理要由扩展策略决定

默认 jar 没有最大容量。长期运行、面对不受信服务或实现持久化时，应重写 `setCookiesFromUrl()`：拒绝不需要的来源、过滤已过期项、限制总数/每 domain 数量，并按自己的淘汰策略删除旧记录。

## 直接增删改与 URL 流程的区别

`insertCookie()` 直接加入一条 Cookie；同标识符存在时覆盖。`updateCookie()` 只在同标识符已经存在时更新，找不到时返回 `false`。`deleteCookie()` 按同标识符删除。

这些 API 不带来源 URL，适合受控恢复或测试数据，但也意味着调用者自己负责 Cookie 的 domain/path、有效期和安全属性。接收服务端 Cookie 时优先用 `setCookiesFromUrl()`，让默认规范化和 `validateCookie()` 有机会执行。

## 自定义策略时应重写什么

- 重写 `cookiesForUrl()`：控制“发送什么”。可以按登录隔离、匿名模式、首方规则或额外审计筛选结果；保留正确的 path 排序。
- 重写 `setCookiesFromUrl()`：控制“接受什么”。可以施加容量上限、拒绝特定 domain、清理过期记录，并将变更持久化。
- 重写 `validateCookie()`：只改变 domain/path 是否可由来源 URL 设置的基础判定。

持久化 jar 不应在每个虚函数中同步阻塞写盘。更好的做法是内存先更新，再合并或延迟写入；关闭前再确保最后一次写入完成。这样网络请求不会因为慢磁盘而被不必要地拖住。

## 常见误区

- **以为默认 jar 会跨启动保存登录态**：不会，默认只在内存中存在。
- **把 stack 上的 jar 交给 `setCookieJar()`**：manager 会取得所有权，传入栈对象会造成生命周期错误。
- **把 `insertCookie()` 当作来自网络的接收流程**：它没有来源 URL，不能完成标准的 URL 范围处理。
- **只按 Cookie name 删除或更新**：身份由 name/domain/path 三元组定义。
- **忽略无容量上限**：不受控服务可以长期累积 Cookie，定制 jar 时应增加上限和淘汰规则。

## API 速查表

| 类别 | API | 语义与注意点 |
| --- | --- | --- |
| 构造/析构 | `QNetworkCookieJar(parent)` / `~QNetworkCookieJar()` | QObject 容器；默认空且仅内存存储，析构时所有 Cookie 丢弃。 |
| 请求选择 | `cookiesForUrl(url) const` | 返回将随请求发往 URL 的 Cookie；同名不同 path 时按 path 长度从长到短排序。可重写以实现发送策略。 |
| 响应接收 | `setCookiesFromUrl(cookieList, url)` | 以来源 URL 接收 Cookie，先规范化并做基础 domain/path 校验；至少设置一条返回 `true`。可重写以实现接受、容量和持久化策略。 |
| 直接插入 | `insertCookie(cookie)` | 插入或覆盖同标识符 Cookie；无来源 URL，调用者负责范围和合法性。 |
| 直接更新 | `updateCookie(cookie)` | 仅当同标识符已存在时更新；不存在返回 `false`。内部使用 `insertCookie()`。 |
| 删除 | `deleteCookie(cookie)` | 删除同 name/domain/path 标识符的 Cookie；删除成功返回 `true`。 |
| 派生存储 | `allCookies() const` | 受保护；取得全部条目，供持久化、过期清理或自定义策略使用。 |
| 派生恢复 | `setAllCookies(cookieList)` | 受保护；整体替换内部列表，适合从可信持久化数据恢复。 |
| 派生校验 | `validateCookie(cookie, url) const` | 受保护虚函数；判断 Cookie domain/path 是否允许由来源 URL 设置。 |

## 相关类型

- `QNetworkCookie`：单条 Cookie 的值、标识符和属性。
- `QNetworkAccessManager`：调用 jar 的 URL 选择/接收接口，并在 `setCookieJar()` 后取得所有权。
- `QNetworkReply`：响应产生 Cookie 的来源。
