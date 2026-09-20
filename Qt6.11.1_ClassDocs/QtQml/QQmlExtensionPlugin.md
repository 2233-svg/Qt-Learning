# QQmlExtensionPlugin
> Qt 6.11.1 · Qt QML · 来自 `QQmlExtensionPlugin`

## 作用定位

`QQmlExtensionPlugin` 是传统 QML 扩展插件基类。插件被 QML import 机制加载后，负责在 `registerTypes()` 中注册 C++ 类型，并可在 `initializeEngine()` 中对引擎做额外初始化。

Qt 6 的现代 QML 模块更多依赖 CMake/qmltyperegistrar 自动生成注册代码，但理解这个类仍有助于维护旧插件和手写插件。

## 类说明

- 头文件：`#include <QQmlExtensionPlugin>`
- CMake：链接 `Qt6::Qml`
- 继承：`QObject`
- 必须实现：`registerTypes(const char *uri)`

## API 速查

| API | 说明 |
| --- | --- |
| `registerTypes(uri)` | 注册该 import URI 下暴露的 QML 类型、单例、不可创建类型等。 |
| `initializeEngine(engine, uri)` | 插件加载到某个 engine 后调用，可设置 image provider、context 或单例状态。 |
| `unregisterTypes()` | Qt 6 起可用于撤销/清理类型注册场景。 |

## 使用场景

- 维护手写 QML 插件。
- import 某 URI 时动态注册 C++ 类型。
- 插件加载时配置引擎资源，例如 image provider。

## 常见坑与经验

- `uri` 必须和 qmldir/import 中的模块 URI 一致；不一致会导致类型找不到。
- `registerTypes()` 做类型注册，不要依赖某个具体 engine 实例。
- `initializeEngine()` 可以访问 engine，但可能被多个 engine 调用，避免保存单例式全局可变状态。
- 现代 Qt 项目优先用 QML_ELEMENT、QML_SINGLETON 和 CMake QML module；手写插件只在确有需要时使用。

## 知识点覆盖

- QML import 插件机制
- 类型注册与 engine 初始化分离
- 旧式插件和现代 QML 模块的关系
- URI/qmldir 一致性
