# QQmlEngine
> Qt 6.11.1 · Qt QML · 来自 `QQmlEngine`

## 作用定位

`QQmlEngine` 是 QML 运行时核心：它继承 `QJSEngine`，额外负责 QML 类型加载、import/plugin 路径、组件缓存、图片 provider、URL 拦截、网络访问、根上下文、单例、异步孵化和 QML 警告输出。

如果 `QJSEngine` 是 JS 虚拟机，`QQmlEngine` 就是能理解 QML 模块、组件和绑定的运行时。

## 类说明

- 头文件：`#include <QQmlEngine>`
- CMake：链接 `Qt6::Qml`
- 继承：`QJSEngine`
- 直接派生：`QQmlApplicationEngine`

## API 速查

| API | 说明 |
| --- | --- |
| `rootContext()` | 获取全局根上下文，用来设置应用级上下文属性。 |
| `addImportPath()` / `setImportPathList()` | 配置 QML import 搜索路径。 |
| `addPluginPath()` / `setPluginPathList()` | 配置插件搜索路径。 |
| `addImageProvider()` / `removeImageProvider()` / `imageProvider()` | 注册和访问 `image://provider/...` 图片源。 |
| `addUrlInterceptor()` / `removeUrlInterceptor()` / `interceptUrl()` | 拦截 QML 资源 URL，常用于重定向、打包资源、文件选择。 |
| `networkAccessManager()` / `setNetworkAccessManagerFactory()` | 定制 QML 网络加载使用的 NAM。 |
| `baseUrl()` / `setBaseUrl()` | 影响相对 URL 解析。 |
| `offlineStoragePath` / `setOfflineStoragePath()` | 配置 QML Local Storage 路径。 |
| `clearComponentCache()` / `trimComponentCache()` | 清理或收缩组件缓存。 |
| `clearSingletons()` / `singletonInstance()` | 管理 QML 单例实例。 |
| `setIncubationController()` / `incubationController()` | 定制异步创建对象的孵化节奏。 |
| `setOutputWarningsToStandardError()` | 控制 QML warning 是否直接输出到 stderr。 |
| `warnings()` | 捕获 QML 警告列表。 |
| `quit()` / `exit(retCode)` | QML 侧请求退出应用时的信号。 |
| `retranslate()` / `markCurrentFunctionAsTranslationBinding()` | 触发翻译绑定刷新。 |
| `contextForObject()` / `setContextForObject()` | 查询或设置 QObject 关联的 QML 上下文。 |
| `qmlContext()` / `qmlEngine()` | 便捷查询对象所在上下文和引擎。 |

## 使用场景

- 构建自定义 QML 加载框架，而不是直接用 `QQmlApplicationEngine`。
- 给 QML 注入全局 C++ 对象、图片源、网络工厂。
- 插件式应用需要动态调整 import/plugin 路径。
- 需要控制组件缓存、单例缓存或对象异步创建节奏。

## 常见坑与经验

- `rootContext()->setContextProperty()` 应在加载 QML 前完成；加载后再改会让已创建绑定重新评估，成本和行为都更难控。
- `clearComponentCache()` 会影响之后创建的组件，不会让已经存在的对象自动换类定义。
- 图片 provider 的 providerId 大小写、路径和 URL 写法要一致，`image://icons/foo` 对应 providerId `icons`。
- 自定义 `QQmlNetworkAccessManagerFactory` 要在加载任何网络资源前设置。
- `QQmlEngine` 管对象生命周期时，QObject ownership 仍然和 `QJSEngine` 规则相关。

## 知识点覆盖

- QML import 与 plugin 路径
- 根上下文和 context property
- 组件缓存与单例缓存
- 图片 provider、URL interceptor、网络工厂
- 异步孵化控制
- QML 警告、退出、翻译刷新
