# QQmlEngineExtensionPlugin
> Qt 6.11.1 · Qt QML · 来自 `QQmlEngineExtensionPlugin`

## 作用定位

`QQmlEngineExtensionPlugin` 是面向“扩展 QML 引擎行为”的插件基类。它的重点不在手动注册一堆类型，而是在插件加载时通过 `initializeEngine()` 配置引擎；类型注册通常由 QML 模块生成机制处理。

## 类说明

- 头文件：`#include <QQmlEngineExtensionPlugin>`
- CMake：链接 `Qt6::Qml`
- 继承：`QObject`
- 构造：`QQmlEngineExtensionPlugin(QObject *parent = nullptr)`

## API 速查

| API | 说明 |
| --- | --- |
| `QQmlEngineExtensionPlugin(parent)` | 创建插件对象。 |
| `initializeEngine(engine, uri)` | 插件被引擎加载时进行初始化。 |
| `Q_IMPORT_QML_PLUGIN(PluginName)` | Qt 6.2 起静态导入 QML 插件的宏。 |

## 使用场景

- QML 模块需要在 import 时给 engine 加 image provider、URL interceptor 或单例初始化。
- 静态链接 QML 插件，需要用 `Q_IMPORT_QML_PLUGIN` 拉入插件。
- 现代 QML 模块中把类型注册交给工具链，插件只做 engine 级初始化。

## 常见坑与经验

- `initializeEngine()` 可能对不同 engine 多次调用，代码要可重复、可隔离。
- 静态插件忘记 `Q_IMPORT_QML_PLUGIN` 时，链接进了二进制也未必会被 QML import 找到。
- 不要在插件初始化里过早加载 QML 文件，容易造成递归 import 或路径尚未稳定。
- 与 `QQmlExtensionPlugin` 相比，它更适合 Qt 6 模块化工程的 engine 扩展。

## 知识点覆盖

- QML engine 扩展插件
- 静态 QML 插件导入
- 模块初始化与类型注册分工
- 多 engine 场景下的初始化约束
