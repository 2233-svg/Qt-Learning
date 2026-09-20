# QJSEngine：在 C++ 中承载一套 JavaScript 运行环境

> Qt 6.11.1 · `#include <QJSEngine>` · 模块：`Qt6::Qml` · 基类：`QObject`

`QJSEngine` 是不依赖 QML 界面的 JavaScript 引擎。它维护一套独立的全局对象、JavaScript 堆、模块缓存、异常状态和 QObject 桥接规则。它适合规则表达式、可配置脚本、自动化扩展和脚本化测试；若要加载 `.qml`、创建 QML 对象，应使用在它之上扩展的 `QQmlEngine` 或 `QQmlApplicationEngine`。

## 构建

```cmake
find_package(Qt6 REQUIRED COMPONENTS Qml)
target_link_libraries(app PRIVATE Qt6::Qml)
```

qmake：`QT += qml`。

## 执行脚本时先设计异常路径

```cpp
#include <QJSEngine>
#include <QDebug>

QJSEngine engine;
QStringList stack;
const QJSValue result = engine.evaluate(
    u"function divide(a, b) { if (!b) throw new Error('zero'); return a / b; }"
    u"divide(6, 0);"_s, u"rules.js"_s, 1, &stack);

if (result.isError())
    qWarning() << result.toString() << stack;
else
    qDebug() << result.toNumber();
```

`fileName` 和 `lineNumber` 只影响错误定位。也不要只依赖 `isError()`：JavaScript 可以执行 `throw 42`，这时异常值不一定是 Error 对象；传入 `exceptionStackTrace` 才能可靠地知道本次 `evaluate()` 是否异常结束。

## 解决的问题与实际场景

### 提供可控的全局脚本环境

`globalObject()` 包含 ECMAScript 内建对象。写入它的属性会成为随后脚本可见的全局变量：

```cpp
engine.globalObject().setProperty(u"taxRate"_s, 0.13);
const QJSValue total = engine.evaluate(u"100 * (1 + taxRate)"_s);
```

同一 engine 中的全局变量、原型改动和模块状态会持续存在。多租户规则、相互隔离的测试或不可信插件不能共用同一台 engine。

### 暴露 C++ 对象和类型

`newQObject()` 将 `QObject` 包装为 JavaScript 对象，脚本可使用元对象系统公开的属性、信号和方法。包装器不保证 QObject 永远存活：目标被 C++ 删除后，后续脚本访问会抛异常。

`newQObject()` 的默认 JS 所有权尤其需要小心。通过 `setObjectOwnership()` 明确 C++ 或 JavaScript 谁负责销毁，并让它与 QObject parent、智能指针策略保持一致。不要让三套所有权同时接管同一对象。

`newQMetaObject()` 用来暴露元对象能力；`newObject()`、`newArray()`、`newErrorObject()` 和 `newSymbol()` 用于在当前 engine 内创建对应脚本值。

### 模块、转换和宿主扩展

`importModule()` 加载 UTF-8 ECMAScript 模块，路径会规范化；同一模块在同一 engine 的生命周期内只实例化一次，模块顶层状态因而是“每台 engine 一份”。`registerModule()` 可以把 C++ 创建的 `QJSValue` 注册为可导入模块。

`toScriptValue()` / `fromScriptValue()` 处理通用值，`toPrimitiveValue()` / `fromPrimitiveValue()` 处理无 engine 依赖的标量，`toManagedValue()` / `fromManagedValue()` 处理与当前 engine 绑定的局部值。`coerceValue<From, To>()` 遵循 QML/JavaScript 转换规则，不是简单 C++ cast。

## 关键边界

- `evaluate()` 与 `QJSValue` 的调用路径会把异常作为结果值返回；`QJSManagedValue` 的失败则写入 engine 错误状态，之后调用 `hasError()` / `catchError()`。
- `setInterrupted(true)` 是协作式中断：它不能回滚已发生的 C++ 副作用，也不能取消阻塞的原生函数。
- `collectGarbage()` 通常不必手动调用；解除全局引用、闭包引用和缓存引用才是资源治理重点。
- JavaScript 对象、函数、模块都属于创建它们的 engine，不能直接混进另一台 engine 的对象图。
- `uiLanguage` 表示 UI 区域语言并发出 `uiLanguageChanged()`；它不会自动翻译任意 C++ 字符串。

## API 速查表

| API | 用途 | 语义与边界 |
| --- | --- | --- |
| `QJSEngine(parent)` | 创建 JavaScript 环境 | 是 QObject；在所属线程中使用和销毁。 |
| `evaluate(program, fileName, lineNumber, stack)` | 执行脚本文本 | 返回结果或被抛出的值；`stack` 用于诊断异常。 |
| `globalObject()` | 访问全局对象 | 写入的是该 engine 持续存在的全局状态。 |
| `newObject()` / `newArray(length)` | 创建对象或数组 | 结果只能在当前 engine 的对象图中使用。 |
| `newErrorObject(type, message)` | 创建 Error 对象 | 可作为结构化脚本异常抛出。 |
| `newSymbol(name)` | 创建 `Symbol` | Qt 6.2 起；无法用普通 primitive 完整替代。 |
| `newQObject(object)` | 包装 QObject | 包装不延长对象生命；明确对象所有权。 |
| `newQMetaObject(metaObject)` | 暴露元对象 | 不代替 QML 类型注册流程。 |
| `toScriptValue()` / `fromScriptValue()` | 通用 C++/JS 转换 | 确认对象是复制、包装还是脚本引用。 |
| `toPrimitiveValue()` / `fromPrimitiveValue()` | primitive 转换 | 只适用于 undefined、null、布尔、整数、双精度、字符串。 |
| `toManagedValue()` / `fromManagedValue()` | managed value 转换 | 值绑定当前 engine 与线程，适合局部操作。 |
| `coerceValue<From, To>()` | JS/QML 规则强制转换 | 不等价于 C++ 强制转换。 |
| `importModule(fileName)` | 导入 ECMAScript 模块 | UTF-8；同一 engine 内模块只初始化一次。 |
| `registerModule(name, value)` | 注册宿主模块 | `value` 应来自当前 engine。 |
| `installExtensions(...)` | 安装 console、翻译、GC 扩展 | 方便开发，不构成安全沙箱。 |
| `throwError(...)` | 从 C++ 向脚本抛错 | 立即结束当前 C++ 路径并返回合适默认值。 |
| `hasError()` / `catchError()` | 查询/取走 engine 错误 | 主要配合 `QJSManagedValue`；`catchError()` 会消费错误。 |
| `setInterrupted()` / `isInterrupted()` | 请求/查询中断 | 不回滚副作用。 |
| `collectGarbage()` | 请求 GC | 不应用作常规内存管理手段。 |
| `setObjectOwnership()` / `objectOwnership()` | 设置/查询 QObject 所有权 | parent、智能指针和 JS 所有权须有唯一主导规则。 |
| `uiLanguage` / `uiLanguageChanged()` | 设置 UI 区域语言 | 只影响支持该概念的翻译路径。 |
| `qjsEngine(QObject *)` | 查当前 JS 调用关联的 engine | 只在从 JS/QML 进入 QObject 的上下文有意义。 |

`QJSEngine` 的关键不是执行字符串，而是守住 C++ 与脚本之间的边界：全局状态归谁、对象归谁、异常从哪里取，以及值属于哪台 engine。
