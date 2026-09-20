# QQmlAbstractUrlInterceptor：在 QML 使用 URL 前改写它

> Qt 6.11.1 · `#include <QQmlAbstractUrlInterceptor>` · 模块：`Qt6::Qml`

`QQmlAbstractUrlInterceptor` 是一个抽象策略接口，用来在 QML 引擎实际使用 URL 前改写 URL。它解决的典型问题是：同一份 QML 逻辑要根据平台、主题、渠道或运行环境选择不同资源，而不想把选择条件散落到所有 QML 文件中。

例如，把 `qrc:/assets/logo.png` 改到当前平台资源目录，把 QML 文件映射到替代实现，或将本地 URL 改为由自定义网络方案处理的 URL。

## 接入方式

```cpp
#include <QQmlAbstractUrlInterceptor>
#include <QQmlEngine>

class ThemeInterceptor final : public QQmlAbstractUrlInterceptor
{
public:
    QUrl intercept(const QUrl &url, DataType type) override
    {
        if (type == UrlString && url.path().startsWith(u"/assets/"_s))
            return QUrl(u"qrc:/assets/dark/"_s + url.fileName());
        return url;
    }
};

QQmlEngine engine;
ThemeInterceptor interceptor;
engine.setUrlInterceptor(&interceptor);
```

工程链接 `Qt6::Qml`；qmake 使用 `QT += qml`。

引擎不拥有这个 interceptor。它必须在 `QQmlEngine` 停止使用它之前持续存活，通常将它放在与 engine 相同或更长的作用域中。

## 拦截发生在哪个阶段

相对 URL 会先相对于当前 QML 上下文的文件路径解析，再传给 `intercept()`。但被替换内容内部的相对路径仍按**拦截前**的原始 URL 作为基准解析。这使“替换整个 QML 文件”不必同时重写文件内部的每个相对资源路径。

`DataType` 不是装饰信息，决定了改写的影响范围：

- `QmlFile`：QML 文件本身。拦截它而不改 `QmldirFile`，更接近“用另一个文件替换该组件实现”。
- `QmldirFile`：类型定位用的 `qmldir`。只改它可以替换整个模块子树。
- `JavaScriptFile`：QML 导入的 JavaScript 文件。
- `UrlString`：QML 的 `url` 属性值，不代表引擎正加载一个文件。

同一 QML 类型涉及 `qmldir` 和定义类型的 QML 文件；不分 `DataType` 地统一替换，容易得到双重替换或无法定位类型。

## 同步与线程边界

`intercept()` 是同步回调，并且 Qt 要求其实现**线程安全**，因为它可被多个线程同时调用。实现中不要读写未经保护的可变成员、依赖 GUI 线程对象，或做会等待事件循环的工作。

若需要异步资源，拦截器本身不能等待下载完成；应返回具有异步 scheme 的 URL，例如 `https` 或由自定义 `QNetworkAccessManager` 处理的 scheme。它拦截所有 URL，包含本地文件和资源系统 URL；若仅要控制网络请求，`setNetworkAccessManagerFactory()` 更聚焦。

## API 速查表

| API | 用途 | 语义与边界 |
| --- | --- | --- |
| `QQmlAbstractUrlInterceptor` | URL 改写策略基类 | 抽象类型，不直接实例化。 |
| `intercept(url, type)` | 返回替代后的 URL | 纯虚函数；同步调用且必须线程安全。 |
| `DataType::QmlFile` | 指明加载 QML 文件 | 适合替换单个组件实现。 |
| `DataType::QmldirFile` | 指明加载 qmldir | 适合切换整个类型/模块子树。 |
| `DataType::JavaScriptFile` | 指明导入 JS 文件 | 仅在 JavaScript 导入路径上改写。 |
| `DataType::UrlString` | 指明 QML `url` 属性 | 不等于引擎正在加载组件文件。 |
| `QQmlEngine::setUrlInterceptor()` | 将策略装入 engine | engine 不接管 interceptor 生命周期。 |

它适合做“URL 到 URL”的确定性映射。把认证、下载、阻塞 I/O 或状态机塞进 `intercept()`，会把 QML 加载路径变得脆弱而难以调试。
