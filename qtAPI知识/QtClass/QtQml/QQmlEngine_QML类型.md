# QQmlEngine：管理 QML 组件、上下文、导入和运行时资源

> Qt 6.11.1 · `#include <QQmlEngine>` · 模块：`Qt6::Qml` · 基类：`QJSEngine`

`QQmlEngine` 是 QML 运行环境：它加载模块和组件、创建 QML 上下文和对象、执行绑定与 JavaScript，并管理图像提供者、网络访问、离线存储、URL 拦截和组件缓存。

当你需要手工加载/创建多个 QML 组件、动态建立 context 或嵌入 QML 子系统时使用它。只加载一个应用入口时，`QQmlApplicationEngine` 往往更省心。

## 最小的动态组件环境

```cpp
#include <QQmlComponent>
#include <QQmlEngine>

QQmlEngine engine;
engine.addImportPath(u":/qt/qml"_s);

QQmlComponent component(&engine, QUrl(u"qrc:/ui/Panel.qml"_s));
if (component.isReady())
    QObject *panel = component.create(engine.rootContext());
```

工程链接 `Qt6::Qml`；qmake 使用 `QT += qml`。

每个 QML 组件在 `QQmlContext` 中创建；未指定 context 时通常使用 `rootContext()`。root context 适合所有组件都应看见的少量全局数据，局部数据应放到它的子 context。context property 的工具可见性很差，新设计仍优先 QML singleton 或组件显式属性。

## 运行环境的关键组成

### 导入、插件与基准 URL

`addImportPath()` 将规范化后的路径放到 import path **首位**，可用于应用私有模块覆盖或测试模块；`setImportPathList()` 则完全替换列表，**不会保留默认 import path**。插件路径只影响 `qmldir` 引用的原生插件查找，不等于 QML 模块路径。

`baseUrl()` 只用于 `QQmlComponent` 接到相对 URL 时的解析；未显式设置时为应用工作目录。把本地路径转换为 `QUrl::fromLocalFile()` 通常比依赖工作目录更稳。

### 外部资源所有权并不一致

| 接口 | engine 是否取得所有权 | 配置时机 |
| --- | --- | --- |
| `addImageProvider()` | 是 | 在加载任意 QML 源前添加。 |
| `addUrlInterceptor()` | 否 | 加载文件期间不得修改列表；按添加顺序执行。 |
| `setNetworkAccessManagerFactory()` | 否 | 执行 engine 前设置，首次创建网络管理器前必须就绪。 |
| `setIncubationController()` | 否 | 每台 engine 同时只能有一个 active controller。 |

`removeImageProvider()` 只是按 id 移除 provider；由 engine 管理过的 provider 生命周期应按该所有权关系审视。`removeUrlInterceptor()` 不删除 interceptor，可以转给其他 engine 再用。

`interceptUrl()` 让你手工运行当前所有 URL interceptor，调试资源路径时很有用。多个 interceptor 在每个 URL 上按添加顺序执行；加载过程中增删会导致资源选择不一致。

### 网络、缓存、单例与本地存储

QML 的网络访问共享 `networkAccessManager()`。若首次创建前已设置 `QQmlNetworkAccessManagerFactory`，它可统一定制代理、cookie 和缓存；之后再设置太晚。`offlineStoragePath` 是 SQL 等离线数据目录，`offlineStorageDatabaseFilePath(name)` 返回某个 Local Storage 数据库实际或预计位置。

`trimComponentCache()` 只释放当前未使用组件的元数据，适合作为温和的回收。`clearComponentCache()` 更激进：会丢弃未引用组件的属性元数据；官方建议调用前确保没有由 QML 组件创建的对象仍活着。要重置 engine 拥有的 singleton，可先 `clearSingletons()`；它会删除 engine 拥有的 QObject singleton，现有 QML 对象中的对应属性可能变为 null，且不会因为访问而自动创建，只有新组件实例化时才重新生成。

## 翻译、警告和对象关联

安装新 `QTranslator` 后调用 `retranslate()`，可刷新使用翻译字符串的绑定。C++ 实现自定义翻译辅助函数时，若它处于 QML binding 中可调用 `markCurrentFunctionAsTranslationBinding()`（Qt 6.6 起）；普通 QObject 的动态语言支持通常更适合处理 `LanguageChange` 事件。

`warnings()` 信号提供 QML 警告列表。`setOutputWarningsToStandardError(false)` 可关闭 stderr 输出而保留信号，方便应用统一收集日志。

由 engine 创建的 QObject 会自动关联 context。对手工创建的 QObject 可在它尚未有 context 时使用 `setContextForObject()`；已有 context 时 Qt 只警告且不替换。`qmlContext()` / `qmlEngine()` 是更方便的相关查询函数。

## API 速查表

| API | 用途 | 语义与边界 |
| --- | --- | --- |
| `QQmlEngine(parent)` | 创建 QML 运行环境 | 同时继承 `QJSEngine` 的脚本环境和生命周期约束。 |
| `rootContext()` | 取得根 context | 用于全局少量数据；局部数据应创建子 context。 |
| `addImportPath(path)` | 在首位增加模块路径 | 路径会规范化，可能改变同名模块解析结果。 |
| `setImportPathList(paths)` | 替换模块路径列表 | 不保留 Qt 默认 import path。 |
| `addPluginPath()` / `setPluginPathList()` | 配置原生插件查找路径 | 面向 `qmldir` 中引用的插件。 |
| `baseUrl()` / `setBaseUrl()` | 处理相对组件 URL | 默认基准是进程工作目录。 |
| `addUrlInterceptor()` | 加入 URL 改写器 | 不取得所有权；加载途中勿修改。 |
| `removeUrlInterceptor()` / `urlInterceptors()` | 移除/列出改写器 | 移除不删除对象，可重新使用。 |
| `interceptUrl(url, type)` | 手工运行改写链 | 用于验证最终资源 URL。 |
| `addImageProvider(id, provider)` | 注册 `image://id/...` provider | engine 取得所有权；在加载 QML 前添加。 |
| `imageProvider(id)` / `removeImageProvider(id)` | 查询/移除 provider | 注意 provider 所有权已经交给 engine。 |
| `setNetworkAccessManagerFactory(factory)` | 定制 QML 网络管理器 | engine 不取得所有权，且必须在执行前设置。 |
| `networkAccessManager()` | 取得 engine 共享网络管理器 | 第一次取得可能触发 factory 创建。 |
| `setIncubationController(controller)` | 绑定孵化控制器 | 不取得所有权，每台 engine 只允许一个。 |
| `offlineStoragePath` | 设置离线用户数据目录 | 变更会发 `offlineStoragePathChanged()`（Qt 6.5 起）。 |
| `offlineStorageDatabaseFilePath(name)` | 查 Local Storage 数据库路径 | 返回实际或预计存储位置。 |
| `trimComponentCache()` | 释放未使用组件元数据 | 相比 clear 更温和。 |
| `clearSingletons()` | 丢弃 engine 拥有的 singleton | 现有 QML 对象可能看到 null；不会自动重新创建。 |
| `clearComponentCache()` | 清空未引用组件缓存 | 调用前确保 QML 创建对象不再存活。 |
| `singletonInstance<T>(id)` | 取注册 singleton 实例 | `T` 为 `QJSValue` 或 QObject 指针；重复访问缓存 type id 更快。 |
| `singletonInstance<T>(uri, type)` | 按模块名取 singleton | Qt 6.5 起；适合一次性访问。 |
| `retranslate()` | 刷新翻译 binding | 安装新翻译器后调用。 |
| `markCurrentFunctionAsTranslationBinding()` | 标记自定义翻译 helper | Qt 6.6 起；仅对紧密绑定 QML 的辅助函数适用。 |
| `warnings(errors)` | 接收 QML 警告 | 可配合 stderr 输出设置统一处理日志。 |
| `quit()` / `exit(code)` | 接收 QML 请求退出信号 | 应显式连接到应用退出策略。 |
| `contextForObject()` / `setContextForObject()` | 查询/设置 QObject context | context 一旦存在就不可被替换。 |
| `qmlContext()` / `qmlEngine()` | 便利查询关联 context/engine | 需要包含 `<QtQml>`。 |

`QQmlEngine` 是一台长期运行的 QML 子系统，而不是一次性加载器。真正容易出错的地方都在配置时机、缓存清理顺序和“engine 是否拥有这个对象”这三类边界上。
