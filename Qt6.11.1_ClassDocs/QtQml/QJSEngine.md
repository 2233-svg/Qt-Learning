# QJSEngine
> Qt 6.11.1 · Qt QML · 来自 `QJSEngine`

## 作用定位

`QJSEngine` 是 Qt 内嵌 JavaScript 运行时。它负责执行脚本、创建 JS 对象、在 `QVariant`/C++ 类型和 JS 值之间转换、管理暴露给脚本的 `QObject`，并提供模块、异常、扩展函数和垃圾回收控制。

`QQmlEngine` 继承自它；如果你只需要运行 JS，不需要加载 QML 组件，用 `QJSEngine` 更轻。

## 类说明

- 头文件：`#include <QJSEngine>`
- CMake：链接 `Qt6::Qml`
- 继承：`QObject`
- 直接派生：`QQmlEngine`

## API 速查

| API | 说明 |
| --- | --- |
| `evaluate(program, fileName, lineNumber, stack)` | 执行一段 JS，返回 `QJSValue`；`fileName` 和行号用于错误定位。 |
| `importModule(fileName)` / `registerModule(name, value)` | 加载或注册 ECMAScript 模块。 |
| `globalObject()` | 取得全局对象，用来挂载函数、对象或配置。 |
| `newObject()` / `newArray()` | 创建普通 JS 对象或数组。 |
| `newQObject(object)` | 把 `QObject` 包装成脚本可访问对象。 |
| `newQMetaObject<T>()` / `newQMetaObject(metaObject)` | 暴露元对象，让脚本访问枚举、构造等元信息。 |
| `newErrorObject()` / `throwError()` | 创建或抛出 JS 错误。 |
| `hasError()` / `catchError()` | Qt 6.1 起检查并取出挂起异常。 |
| `toScriptValue()` / `fromScriptValue()` | C++ 类型与 `QJSValue` 转换。 |
| `toManagedValue()` / `fromManagedValue()` | 与 `QJSManagedValue` 转换，适合需要绑定 engine 的值。 |
| `toPrimitiveValue()` / `fromPrimitiveValue()` | 与无引擎原始值转换。 |
| `coerceValue<From, To>()` | 按 JS 转换规则把一个值转换为另一个类型。 |
| `collectGarbage()` | 主动触发 JS 垃圾回收。 |
| `setInterrupted()` / `isInterrupted()` | 中断长时间运行的脚本。 |
| `installExtensions()` | 安装 `console`、翻译函数、`gc()` 等扩展。 |
| `uiLanguage` / `uiLanguageChanged()` | 翻译扩展使用的 UI 语言。 |
| `setObjectOwnership()` / `objectOwnership()` | 控制 QObject 由 C++ 还是 JS 垃圾回收拥有。 |
| `qjsEngine(object)` | 查询某 QObject 所属 JS 引擎。 |

## 枚举速查

| 类型 | 值 | 说明 |
| --- | --- | --- |
| `Extension` | `TranslationExtension` | 安装 `qsTr()`、`qsTranslate()` 等翻译函数。 |
| `Extension` | `ConsoleExtension` | 安装 `console.log()`、`console.warn()` 等调试输出。 |
| `Extension` | `GarbageCollectionExtension` | 安装脚本侧 `gc()`。 |
| `ObjectOwnership` | `CppOwnership` | C++ 负责销毁对象，JS 不会 delete。 |
| `ObjectOwnership` | `JavaScriptOwnership` | JS 引擎可在无引用且无 parent 时销毁对象。 |

## 使用场景

- 在 C++ 应用里执行用户脚本或规则表达式。
- 暴露 QObject 给脚本作为扩展 API。
- 写不依赖 QML UI 的 JS 插件系统。
- 在 QML 之外复用 JS 类型转换、模块和错误模型。

## 常见坑与经验

- `evaluate()` 返回错误对象时不一定自动抛 C++ 异常；要检查 `QJSValue::isError()` 或 `hasError()`。
- `newQObject()` 后的生命周期必须明确：有 parent 的 QObject 通常让 C++ 管；无 parent 且设为 `JavaScriptOwnership` 时可能被 GC。
- 不要把同一个 JS 值跨 engine 混用。对象、函数、QObject 包装都绑定到创建它们的 engine。
- 长脚本要设计中断点或从其他线程调用 `setInterrupted(true)`，否则会卡住事件循环。
- `collectGarbage()` 是工具，不是生命周期管理策略；C++ 对象销毁仍要靠 parent/ownership。

## 知识点覆盖

- JS 运行时与 QML 引擎关系
- JS/C++ 类型转换
- QObject 暴露与所有权
- ECMAScript 模块
- 异常、错误对象、脚本中断
- 翻译和 console 扩展
