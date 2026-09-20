# QQmlApplicationEngine：加载应用入口 QML 的便捷引擎

> Qt 6.11.1 · `#include <QQmlApplicationEngine>` · 模块：`Qt6::Qml` · 基类：`QQmlEngine`

`QQmlApplicationEngine` 把 `QQmlEngine` 与一个用于实例化根组件的 `QQmlComponent` 组合起来，解决了混合 C++/QML 应用“加载入口、拿到根对象、处理加载失败”的常见启动流程。

它适合大多数应用的 `main.qml` 启动。相比 `QQuickView`，它不会自动创建根窗口：根 QML 若使用 Qt Quick，自己必须包含 `Window` 或 `ApplicationWindow`。

## 推荐的启动路径

```cpp
#include <QGuiApplication>
#include <QQmlApplicationEngine>

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);
    QQmlApplicationEngine engine;

    QObject::connect(&engine, &QQmlApplicationEngine::objectCreationFailed,
                     &app, [] { QCoreApplication::exit(-1); },
                     Qt::QueuedConnection);

    engine.setInitialProperties({{u"launchMode"_s, u"normal"_s}});
    engine.loadFromModule(u"MyApp"_s, u"Main"_s);
    return app.exec();
}
```

工程链接 `Qt6::Qml`；qmake 使用 `QT += qml`。只使用非 GUI QML 模块时可以配合 `QCoreApplication`；使用 `QtQuick` 通常需要 `QGuiApplication`。

## 它额外替你配置了什么

在普通 `QQmlEngine` 基础上，它会连接 `Qt.quit()` 到 `QCoreApplication::quit()`，从主 QML 文件相邻的 `i18n` 目录自动加载 `qml_*.qm` 翻译文件，并在 `uiLanguage` 变化时重载翻译。

若场景有 `QQuickWindow`，它会自动设置 incubation controller；还会安装 `QQmlFileSelector` 处理 QML 和资源的文件选择器。因此它是“应用入口加载器”，不是一个完全中性的 `QQmlEngine` 替身。

## 加载方式和完成时机

`load(QString)` 仅接受本地文件或 qrc 路径；相对路径相对于进程工作目录。`load(QUrl)` 可加载远程 URL，远程加载是异步的，必须监听 `objectCreated()`，不能紧接着读取 `rootObjects()` 就假定有根对象。

`loadData()` 从字节数据创建组件；传入的 `url` 作为基准 URL，影响数据内部相对路径和错误信息。`loadFromModule(uri, typeName)`（Qt 6.5 起）按 QML import path 查找模块中的入口类型，也可能异步。

无论加载失败还是成功都会发出 `objectCreated()`；失败时其对象参数为 `nullptr`。Qt 6.4 起另有更明确的 `objectCreationFailed()`，并且失败时两者都会发出。连接信号必须在调用 load 前完成。

## 常见边界

- `rootObjects()` 只包含此类通过 `load()` 或便利构造函数创建的根对象；不是 engine 中所有 QObject 的列表。
- engine 析构会销毁它加载的 QML 对象。因此从 `rootObjects()` 缓存裸指针时，确保 engine 存活。
- `setInitialProperties()` 应在加载前调用，用于根组件顶层初始属性；不能把它当作任意嵌套属性注入器。
- `setExtraFileSelectors()` 必须在加载第一个 QML 文件前设置，之后调用没有效果。
- 翻译资源有命名和资源路径约束，自动加载不会修复不正确的 `qml_` 前缀或资源前缀。

## API 速查表

| API | 用途 | 语义与边界 |
| --- | --- | --- |
| `QQmlApplicationEngine(parent)` | 创建空应用引擎 | 之后调用一种 `load...()` 方法。 |
| `QQmlApplicationEngine(QString/QUrl)` | 构造并加载入口 | 等价于默认构造后立即加载。 |
| `QQmlApplicationEngine(uri, typeName)` | 构造并按模块类型加载 | Qt 6.5 起；按 import path 查找模块。 |
| `load(QString)` | 加载本地/qrc 文件 | 相对路径相对工作目录，同步实例化。 |
| `load(QUrl)` | 从 URL 加载根组件 | 远程 URL 可能异步；监听 `objectCreated()`。 |
| `loadData(data, baseUrl)` | 从内存 QML 加载 | `baseUrl` 决定相对引用和诊断中的位置。 |
| `loadFromModule(uri, typeName)` | 加载模块中的 QML 类型 | Qt 6.5 起；找不到模块会失败。 |
| `rootObjects()` | 取得已加载根对象 | 仅限本 engine 的 load 路径创建的根对象。 |
| `setInitialProperties(map)` | 设置根组件初始顶层属性 | 在 load 前调用；必需属性未满足时创建失败。 |
| `setExtraFileSelectors(list)` | 增加文件选择器 | 必须早于第一次 QML 加载。 |
| `objectCreated(object, url)` | 通知一次对象创建结束 | 失败时 `object == nullptr`。 |
| `objectCreationFailed(url)` | 通知创建失败 | Qt 6.4 起；失败时也会额外收到 `objectCreated(nullptr, ...)`。 |

当应用只是“加载一个入口组件并开始运行”时，它是正确的默认选择；需要细粒度组件编译与手工创建时，改用 `QQmlComponent`。
