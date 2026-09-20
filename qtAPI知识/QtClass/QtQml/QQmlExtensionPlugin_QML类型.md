# QQmlExtensionPlugin：旧式手工类型注册插件基类

> Qt 6.11.1 · `#include <QQmlExtensionPlugin>` · 模块：`Qt6::Qml`

`QQmlExtensionPlugin` 是较旧的 QML 扩展插件基类，额外提供 `registerTypes()` 和 `unregisterTypes()`，让插件手工调用 `qmlRegisterType()` 等函数注册类型。

它解决的是早期或特殊构建系统下的手工注册需求，但 Qt 6 文档的明确建议是：手写插件很少需要，若确实需要插件，应优先使用 `QQmlEngineExtensionPlugin`；类型声明使用 `QML_ELEMENT` 等宏，再让构建系统处理注册。

## 仍会遇到它的场景

- 维护 Qt 5/早期 Qt 6 的既有 QML 模块。
- 旧 qmake 项目中，插件需要按 URI 手工注册 C++ 类型。
- 有极特殊的动态注册/卸载需求，无法交给 `qt_add_qml_module()`。

```cpp
class LegacyPlugin final : public QQmlExtensionPlugin
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID QQmlExtensionInterface_iid)

public:
    void registerTypes(const char *uri) override
    {
        Q_ASSERT(QLatin1StringView(uri) == u"Example.Legacy"_s);
        qmlRegisterType<Backend>(uri, 1, 0, "Backend");
    }
};
```

工程链接 `Qt6::Qml`。新模块应优先选择 `QML_ELEMENT` 与 `qt_add_qml_module()`，避免维护插件元数据、`qmldir` 与手工注册代码三份并行事实。

## 注册、初始化与反注册不是一回事

`registerTypes(uri)` 是纯虚函数，负责将插件提供的 QML 类型注册到该 URI。URI 是引擎根据插件库名和路径识别出的模块标识，注册时应只处理属于本模块的类型。

`initializeEngine(engine, uri)` 在 engine 加载扩展时执行，适合每 engine 初始化。`unregisterTypes()`（Qt 6.0 起）仅在你确实于 `registerTypes()` 手工注册了可反注册类型时覆写；常规模块不应该将它当作运行期“热卸载 QML 模块”的工具。

旧的 `baseUrl()` 在 Qt 6.3 起废弃。应通过 `qmldir` 和规范模块布局描述资源位置，而不是在插件里猜路径。

## API 速查表

| API | 用途 | 语义与边界 |
| --- | --- | --- |
| `QQmlExtensionPlugin(parent)` | 构造旧式插件基类 | 通常由插件系统创建。 |
| `registerTypes(uri)` | 手工注册模块类型 | 纯虚函数；仅注册该 URI 对应的类型。 |
| `unregisterTypes()` | 撤销手工注册 | Qt 6.0 起；仅配合确有需要的手工注册。 |
| `initializeEngine(engine, uri)` | 按 engine 初始化扩展 | 不应把库插件的全局状态强塞进 root context。 |
| `qmlRegisterType()` 等 | 注册 C++ 类型 | 旧式注册 API；新模块优先宏和构建系统。 |
| `baseUrl()` | 旧插件资源基准接口 | Qt 6.3 起废弃，使用 `qmldir` 替代。 |
| `Q_PLUGIN_METADATA(...)` | 声明插件元数据 | 没有它插件无法按 Qt 插件机制发现。 |

它仍是理解历史模块的重要接口，但对新代码而言，最好的使用方式往往是不要再引入它。
