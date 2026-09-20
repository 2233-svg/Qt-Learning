# QQmlIncubator
> Qt 6.11.1 · Qt QML · 来自 `QQmlIncubator`

## 作用定位

`QQmlIncubator` 用来异步或分批创建 QML 对象，避免重组件一次性同步创建导致界面卡顿。它和 `QQmlComponent::create(incubator, ...)` 配合使用，负责跟踪创建状态、错误、初始属性和最终对象。

## 类说明

- 头文件：`#include <QQmlIncubator>`
- CMake：链接 `Qt6::Qml`
- 继承：无公开 QObject 继承
- 可继承并重写 `statusChanged()`、`setInitialState()`

## API 速查

| API | 说明 |
| --- | --- |
| `IncubationMode` | `Asynchronous`、`AsynchronousIfNested`、`Synchronous`。 |
| `Status` | `Null`、`Loading`、`Ready`、`Error`。 |
| `QQmlIncubator(mode)` | 创建指定孵化模式。 |
| `setInitialProperties()` | 创建前设置初始属性。 |
| `setInitialState(object)` | 保护虚函数，可在对象完成前设置初始状态。 |
| `status()` / `isReady()` / `isLoading()` / `isError()` / `isNull()` | 查询孵化状态。 |
| `object()` | Ready 后取得创建出的对象。 |
| `errors()` | Error 后取得错误列表。 |
| `forceCompletion()` | 强制同步完成剩余创建工作。 |
| `clear()` | 清除当前孵化任务和结果。 |
| `incubationMode()` | 查询模式。 |
| `statusChanged()` | 状态变化时的保护回调。 |

## 使用场景

- 列表、页面、复杂弹窗等 QML 对象较重，想分帧创建。
- 自定义对象池或懒加载系统。
- 在创建过程中设置一些 C++ 初始状态。
- 需要在对象 ready/error 时统一处理结果。

## 常见坑与经验

- `object()` 只有 Ready 后才可靠；Loading 状态下读取没有意义。
- `forceCompletion()` 会把剩余工作同步做完，可能造成卡顿，适合收尾或测试。
- incubator 本身不是 QObject，生命周期要由外部 C++ 对象管理。
- `AsynchronousIfNested` 适合组件内部再创建组件时避免破坏外层异步节奏。
- 创建出的对象生命周期仍要自己管理，孵化器不等于 owner。

## 知识点覆盖

- QML 对象异步创建
- 孵化状态机
- 初始属性和初始状态
- 分帧创建与强制完成
- 与 `QQmlComponent` 协作
