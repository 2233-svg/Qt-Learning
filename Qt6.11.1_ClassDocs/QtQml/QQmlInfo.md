# QQmlInfo
> Qt 6.11.1 · Qt QML · 来自 `QQmlInfo`

## 作用定位

`QQmlInfo` 是带 QML 对象上下文的调试输出流。通过 `qmlInfo()`、`qmlWarning()`、`qmlDebug()` 输出日志时，Qt 可以附带对象所在 QML 文件、行号等上下文，让日志更像 QML 引擎自己的警告。

它继承 `QDebug` 风格，用法是流式输出。

## 类说明

- 头文件：`#include <QQmlInfo>`
- CMake：链接 `Qt6::Qml`
- 继承：`QDebug`
- 使用入口：非成员函数 `qmlInfo()`、`qmlWarning()`、`qmlDebug()`

## API 速查

| API | 说明 |
| --- | --- |
| `qmlInfo(object)` | 输出普通信息，并附带 object 的 QML 上下文。 |
| `qmlWarning(object)` | 输出 warning，适合组件配置错误、弃用提示。 |
| `qmlDebug(object)` | 输出 debug 信息，受日志规则控制。 |

## 典型用法

```cpp
if (m_source.isEmpty())
    qmlWarning(this) << "source must not be empty";
```

比 `qWarning()` 更适合 QML 类型内部，因为用户能看到是哪一个 QML 对象实例触发的问题。

## 使用场景

- 自定义 QML 类型在 C++ 中报告用法错误。
- 输出带 QML 文件/行号的诊断信息。
- 给 QML API 的弃用、配置冲突、无效状态提供友好提示。

## 常见坑与经验

- 传入的 object 应该是与 QML 实例相关的 QObject；传 nullptr 会失去定位价值。
- `qmlWarning()` 不是异常，不会阻止继续运行；严重错误仍要配合状态返回或对象创建失败。
- 高频路径不要刷大量 warning，否则会影响性能并淹没有用信息。
- 输出文本应面向 QML 使用者，而不是只写 C++ 内部术语。

## 知识点覆盖

- QML 上下文日志
- C++ 自定义 QML 类型诊断
- QDebug 流式输出
- warning 与运行控制的边界
