# QWindowStateChangeEvent：窗口状态变化事件

> 适用版本：Qt 6.11.1
> 头文件：`#include <QWindowStateChangeEvent>`
> 所属模块：`Qt6::Gui`
> 继承：`QEvent`

## 它解决什么问题

`QWindowStateChangeEvent` 在窗口状态发生变化时，把变化前的状态保存下来。当前窗口对象已经可以通过 `windowState()` 或 `windowStates()` 读到新状态，因此把 old state 和当前状态比较，就能判断窗口刚刚是最小化、最大化、全屏、恢复，还是发生了多标志组合变化。

这个事件解决的是“状态变化通知只告诉你现在是什么，却没有直接告诉你从什么状态变过来”的问题。它适合做布局切换、暂停/恢复渲染、进入全屏时调整工具栏以及恢复窗口时重新安排资源。

## 实际使用场景

- 在 `QWindow::event()` 中处理 `QEvent::WindowStateChange`。
- 比较 `oldState()` 与当前 `windowStates()`，区分最小化、最大化和全屏转换。
- 窗口最小化时暂停高成本动画，恢复暴露后重新请求更新。
- 全屏切换时保存和恢复工具栏、光标、输入模式等 UI 状态。
- 在自定义窗口容器或平台集成代码中识别 override 状态。

## 判断变化的正确方式

`Qt::WindowStates` 是标志集合，可能同时包含多个状态位；`Qt::WindowState` 则表示单个状态。不要把 `oldState()` 当作永远只有一个值，也不要只用 `== Qt::WindowMaximized` 判断所有情况。

事件处理时应同时读取：

```cpp
const auto oldStates = event->oldState();
const auto newStates = windowStates();
const bool enteredFullScreen =
    !(oldStates & Qt::WindowFullScreen) &&
    (newStates & Qt::WindowFullScreen);
```

状态变化可能由窗口管理器异步完成。事件到达时通常可以读取新状态，但不要假设紧邻调用 `setWindowState()` 后就已经完成了所有平台动画、屏幕切换和几何更新。

## `isOverride()` 与生命周期

构造函数的 `isOverride` 参数用于标记该事件是否是 override 类型变化。大多数普通窗口业务只需要 `oldState()`；只有需要区分平台 override 行为或维护自定义窗口系统时，才读取 `isOverride()`。

事件对象属于当前事件派发流程。需要异步执行时，复制 `oldState()`、当前状态和必要的几何数据，不要保存事件指针。

## 常见误区

- 只比较 `windowState()`，忽略多个状态位的组合。
- 误以为 `oldState()` 是变化前的单个 `Qt::WindowState`，从而错误处理全屏和最大化组合。
- 收到状态事件后立即假定窗口已经 exposed；可见、激活和 exposed 是不同状态。
- 在状态事件中阻塞 GUI 线程，导致平台窗口动画或后续事件无法完成。
- 通过事件指针跨线程传递状态，而不是复制标志值。

## API 速查表

| API | 作用 | 重点注意 |
| --- | --- | --- |
| `explicit QWindowStateChangeEvent(Qt::WindowStates oldState, bool isOverride = false)` | 构造一个携带旧窗口状态的事件。 | `oldState` 是 QFlags 集合；`isOverride` 只在特殊窗口管理场景有意义。 |
| `Qt::WindowStates oldState() const` | 返回变化前的窗口状态集合。 | 与窗口当前 `windowStates()` 比较，才能判断进入或离开某个状态。 |
| `bool isOverride() const` | 返回事件是否标记为 override 状态变化。 | 普通应用通常无需据此改变布局或渲染逻辑。 |
| `QEvent::type()` | 返回事件类型，通常为 `QEvent::WindowStateChange`。 | 在 `event()` 或过滤器中先判断类型。 |
| `Qt::WindowStates windowStates() const` | 从接收窗口读取当前状态集合。 | 它不是事件成员，要在处理对象上查询。 |
| `Qt::WindowState windowState() const` | 读取当前主窗口状态。 | 只能表达单一状态；组合判断使用 `windowStates()`。 |
| `Qt::WindowFullScreen` / `Qt::WindowMinimized` 等 | 用位运算测试特定状态。 | 使用 `states & flag`，不要把 QFlags 当普通整数随意覆盖。 |
| `accept()` / `ignore()` | 标记该状态变化事件是否已处理。 | 通常不需要阻止平台状态变化；未处理时保留基类行为。 |

## 一句话总结

处理 `QWindowStateChangeEvent` 的核心是保存 `oldState()`，再和窗口当前的 `windowStates()` 做位标志比较。
