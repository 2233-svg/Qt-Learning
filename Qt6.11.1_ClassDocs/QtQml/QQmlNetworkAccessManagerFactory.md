# QQmlNetworkAccessManagerFactory
> Qt 6.11.1 · Qt QML · 来自 `QQmlNetworkAccessManagerFactory`

## 作用定位

`QQmlNetworkAccessManagerFactory` 用来自定义 QML 引擎加载网络资源时使用的 `QNetworkAccessManager`。你可以在这里设置代理、缓存、证书策略、请求头、cookie、认证或统一监控。

## 类说明

- 头文件：`#include <QQmlNetworkAccessManagerFactory>`
- CMake：链接 `Qt6::Qml`
- 接口类，必须实现 `create(QObject *parent)`
- 设置入口：`QQmlEngine::setNetworkAccessManagerFactory()`

## API 速查

| API | 说明 |
| --- | --- |
| `create(parent)` | 为 QML 引擎创建一个 `QNetworkAccessManager`，parent 通常应传给 NAM。 |
| `~QQmlNetworkAccessManagerFactory()` | 虚析构，允许通过接口管理派生类。 |

## 使用场景

- QML 加载远程图片、QML、JS 时需要统一网络策略。
- 设置 HTTP cache、proxy、cookie jar、认证。
- 在企业环境中注入证书和安全策略。
- 记录 QML 网络请求用于诊断。

## 常见坑与经验

| 点 | 说明 |
| --- | --- |
| 设置时机 | 必须在任何网络资源加载前设置 factory。 |
| 线程 | `QNetworkAccessManager` 有线程归属，不要跨线程随意复用同一个实例。 |
| parent | `create()` 应尊重传入 parent，便于引擎管理生命周期。 |
| 范围 | 它影响 QML 引擎的网络访问，不一定影响你应用里其他手写的 NAM。 |

## 知识点覆盖

- QML 网络资源加载
- 自定义 QNetworkAccessManager
- 缓存、代理、cookie、证书策略
- 引擎级网络诊断
