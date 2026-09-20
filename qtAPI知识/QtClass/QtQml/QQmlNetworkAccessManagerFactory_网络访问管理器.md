# QQmlNetworkAccessManagerFactory：为 QML 网络请求注入统一策略

> Qt 6.11.1 | `#include <QQmlNetworkAccessManagerFactory>` | CMake: `Qt6::Qml`

`QQmlNetworkAccessManagerFactory` 让应用替换 QML 引擎创建的 `QNetworkAccessManager`。它解决的是跨越所有 QML 网络访问的统一配置问题：缓存目录、代理、Cookie、证书策略或测试替身不应散落在每个 `Image`、XMLHttpRequest 或 QML 网络消费者里。

它是抽象工厂，只要求实现一个 `create()`。QML 引擎负责在需要时调用它，网络管理器的 parent 由引擎传入。

## 实际用法：给 QML 图片和请求增加磁盘缓存

```cpp
#include <QQmlNetworkAccessManagerFactory>
#include <QNetworkAccessManager>
#include <QNetworkDiskCache>

class CachedNetworkFactory final : public QQmlNetworkAccessManagerFactory
{
public:
    QNetworkAccessManager *create(QObject *parent) override
    {
        auto *manager = new QNetworkAccessManager(parent);
        auto *cache = new QNetworkDiskCache(manager);
        cache->setCacheDirectory(u"C:/app-cache/network"_s);
        manager->setCache(cache);
        return manager;
    }
};
```

安装发生在引擎真正加载和执行 QML 之前：

```cpp
QQmlApplicationEngine engine;
CachedNetworkFactory factory;
engine.setNetworkAccessManagerFactory(&factory);
engine.loadFromModule("Dashboard", "Main");
```

`QQmlEngine` 不接管 factory 的所有权，因此上例中 `factory` 必须活得比 `engine` 久。将局部 factory 放进一个提前返回的初始化函数是常见悬空错误。

## 每次都要造一个新的 manager

`create(QObject *parent)` 每次调用都必须返回新建的 `QNetworkAccessManager`，并以给定 `parent` 为父对象。不要缓存一个全局 manager 并反复返回，也不要无视 parent；网络访问管理器有线程亲和性，QML 引擎可能在多个线程中请求实例。

因此 `create()` 必须可重入：同时进入该函数的两个调用不能破坏共享状态。最稳妥的做法是在函数内部仅创建独立对象；若要读取全局配置，配置读取本身也要并发安全。

## 信号跨线程时的两个陷阱

引擎会处理自己发起的请求，并清理相应的 `QNetworkReply`。若把 `QNetworkAccessManager::finished` 跨线程连接到接收者，槽函数执行时 reply 可能已经被删除，不能把该信号当作跨线程持久结果通道。

`QNetworkAccessManager::authenticationRequired` 更严格：认证信息必须立刻提供。它不能使用 `Qt::QueuedConnection`，而当收发双方属于不同线程时，默认的 `Qt::AutoConnection` 也会排队，因而同样不适合。认证策略要留在 manager 所在线程内同步完成。

## 不适合用它的情况

- 只想给某一个 C++ 发起的请求加 header：直接配置该 `QNetworkAccessManager` 即可。
- 需要逐 URL 重写、拦截 QML 资源定位：考虑 `QQmlAbstractUrlInterceptor`。
- 需要给 QML 暴露一个明确的业务 HTTP 客户端：封装一个 QObject 服务通常比隐式改写全局 QML 网络栈更可维护。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `virtual ~QQmlNetworkAccessManagerFactory()` | 虚析构，允许以基类指针销毁派生 factory | engine 不拥有 factory；销毁时序由应用负责 |
| `create(QObject *parent)` | 创建并返回一个 QML 专用网络管理器 | 每次必须返回新的 `QNetworkAccessManager` |
| `parent` 参数 | manager 的 QObject 父对象 | 传给 manager 构造函数，避免脱离引擎的生命周期 |
| `QQmlEngine::setNetworkAccessManagerFactory()` | 将 factory 安装到一个 engine | 必须在 engine 执行/加载相关 QML 前设置 |
| `QNetworkAccessManager::finished` | 网络请求完成通知 | 跨线程接收时 reply 可能已被引擎删除 |
| `QNetworkAccessManager::authenticationRequired` | 需要立即填写认证信息的同步通知 | 不可跨线程 queued 连接 |

## 相关类型

- `QQmlEngine` / `QQmlApplicationEngine`：安装并使用 factory 的引擎。
- `QNetworkAccessManager`：factory 生成的实际请求执行者。
- `QNetworkDiskCache`、`QNetworkProxy`：常见的缓存和代理定制点。
