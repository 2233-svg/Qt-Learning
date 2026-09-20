# QQmlIncubationController
> Qt 6.11.1 · Qt QML · 来自 `QQmlIncubationController`

## 作用定位

`QQmlIncubationController` 控制 QML 异步孵化工作的推进节奏。把它设置到 `QQmlEngine` 后，你可以决定每帧、每段时间或某个条件满足前推进多少对象创建工作。

它是性能调度工具，常见于自定义渲染循环、游戏式 UI 或需要严格控制帧预算的应用。

## 类说明

- 头文件：`#include <QQmlIncubationController>`
- CMake：链接 `Qt6::Qml`
- 继承：无公开 QObject 继承
- 设置入口：`QQmlEngine::setIncubationController()`

## API 速查

| API | 说明 |
| --- | --- |
| `engine()` | 返回当前关联的 QML 引擎。 |
| `incubateFor(msecs)` | 在指定时间预算内推进孵化任务。 |
| `incubateWhile(flag, msecs)` | 在原子标志为 true 时推进，`msecs` 可限制时间。 |
| `incubatingObjectCount()` | 当前正在孵化的对象数量。 |
| `incubatingObjectCountChanged(count)` | 保护虚函数，对象数量变化时可响应。 |

## 使用场景

- 每帧只给 QML 对象创建几毫秒预算。
- 大量动态对象创建时保持动画流畅。
- 自定义事件循环或渲染循环中手动推进 QML 孵化。
- 监控当前异步创建积压数量。

## 常见坑与经验

- 设置 controller 后，异步孵化是否推进取决于你是否按节奏调用 `incubateFor()` 等函数。
- 时间预算太小会让界面对象迟迟不 ready，太大又会带来卡顿。
- `incubateWhile()` 使用原子 flag，适合跨线程/循环控制，但仍要理解实际调用线程。
- controller 不创建对象，它只是调度由 `QQmlIncubator` 发起的工作。

## 知识点覆盖

- QML 孵化调度
- 帧预算与对象创建
- 自定义渲染循环集成
- 异步创建积压监控
