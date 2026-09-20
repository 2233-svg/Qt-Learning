# QQmlEngineExtensionPlugin：为每台 QML 引擎安装扩展能力

> Qt 6.11.1 · `#include <QQmlEngineExtensionPlugin>` · 模块：`Qt6::Qml`

`QQmlEngineExtensionPlugin` 是现代 QML 扩展插件的抽象基类。它解决的是：当一个 QML 模块被导入到某台 `QQmlEngine` 时，模块除了声明类型外，还需要针对该 engine 安装资源提供者、定制运行环境或执行初始化。

大部分模块根本不需要手写插件。使用 `QML_ELEMENT`、`QML_NAMED_ELEMENT` 等宏声明类型，并让 CMake 的 `qt_add_qml_module()` 生成插件和类型注册代码，通常就是正确路线。只有图像 provider 等确有每 engine 初始化需求时才手写。

## 典型结构

```cpp
#include <QQmlEngineExtensionPlugin>
#include <QQmlEngine>

class MyModulePlugin final : public QQmlEngineExtensionPlugin
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID QQmlEngineExtensionInterface_iid)

public:
    void initializeEngine(QQmlEngine *engine, const char *uri) override
    {
        Q_UNUSED(uri);
        // 例如：engine->addImageProvider(...);
    }
};
```

插件实例由 Qt 插件系统创建，正常情况下不由业务代码显式构造。工程链接 `Qt6::Qml`；CMake 项目优先用 `qt_add_qml_module()` 声明模块。

## 它解决的问题与边界

`initializeEngine(engine, uri)` 在某个 engine 加载模块时调用。初始化内容应当是该模块真正拥有且每台 engine 都需要的一小段配置，例如注册模块专用 image provider，或设置模块内部的受控服务。

库型插件不要随意修改 `engine->rootContext()`。根上下文属于应用整体，模块向其中注入名称可能和使用者冲突，也使依赖无法从 QML import 看出来。应用私有插件偶尔可以这样做，但 singleton 或显式对象属性通常仍更易维护。

静态构建不会自动把插件二进制“动态发现”进来，使用 `Q_IMPORT_QML_PLUGIN(PluginName)`（Qt 6.2 起）确保插件链接进入最终程序。`PluginName` 是声明 `Q_PLUGIN_METADATA` 的插件扩展类名，不一定等于模块 URI。

## API 速查表

| API | 用途 | 语义与边界 |
| --- | --- | --- |
| `QQmlEngineExtensionPlugin(parent)` | 构造插件基类 | 一般由 Qt 插件系统自动构造。 |
| `initializeEngine(QQmlEngine *, uri)` | 为加载模块的 engine 初始化扩展 | 适合每 engine 资源；避免污染库使用者的 root context。 |
| `Q_PLUGIN_METADATA(...)` | 向 Qt 元对象系统声明插件 | 没有它，插件不能被正常发现和加载。 |
| `QML_ELEMENT` / `QML_NAMED_ELEMENT` | 声明模块导出的 QML 类型 | 现代类型注册首选，交给构建系统生成注册代码。 |
| `qt_add_qml_module()` | 描述模块并生成默认插件 | 默认处理 `qmldir` 与类型注册；特殊需要才加 `NO_GENERATE_PLUGIN_SOURCE`。 |
| `Q_IMPORT_QML_PLUGIN(PluginName)` | 静态构建时强制链接插件 | Qt 6.2 起；参数为插件扩展类名。 |

把它理解为“模块被装到一台 engine 时的钩子”，而不是每个 QML 模块都必须自己维护的一套注册样板。
