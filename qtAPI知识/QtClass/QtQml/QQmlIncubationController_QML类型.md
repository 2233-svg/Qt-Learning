# QQmlIncubationController：把异步 QML 对象创建分配到空闲时间

> Qt 6.11.1 · `#include <QQmlIncubationController>` · 模块：`Qt6::Qml`

`QQmlIncubationController` 驱动 `QQmlIncubator` 的创建进度。它解决复杂 QML 对象、委托或页面创建会阻塞一帧的问题：应用可以只在空闲预算内推进创建，把负载分摊到多个事件循环或渲染帧。

`QQuickWindow`、`QQuickView`、`QQuickWidget` 已为各自 engine 配置更智能的 controller。只有没有这些宿主，或确实需要自定义调度预算时，才应自己实现。

## 一个简单的帧预算控制器

```cpp
class IncubationController final : public QObject, public QQmlIncubationController
{
    Q_OBJECT
protected:
    void timerEvent(QTimerEvent *) override
    {
        incubateFor(4); // 本帧最多给对象创建约 4 ms
    }
};

IncubationController controller;
engine.setIncubationController(&controller);
```

工程链接 `Qt6::Qml`；qmake 使用 `QT += qml`。`QQmlEngine` 不取得 controller 所有权，controller 必须比 engine 的使用期更长。

固定 “每 16 ms 做 5 ms” 只是教学用法。真实调度应考虑当前帧耗时、输入响应和渲染压力；预算过大仍会卡顿，预算过小则让对象出现过慢。

## 控制推进而不是后台线程化

`incubateFor(msecs)` 会处理至多指定毫秒，或在没有待孵化对象时提前结束。`incubateWhile(flag, msecs)` 在原子 flag 为真时处理，可由别的线程或 Unix 信号将 flag 设为 false 请求停止；Qt 以 acquire 内存序读取 flag。

这不表示任意 QML 创建工作可随意移动到另一个线程。controller 是安排引擎在合适时间推进它自己的 incubation 工作；QML/GUI 对象的线程归属规则仍然有效。

`incubatingObjectCountChanged()` 是受保护回调，适合更新内部调度状态或启动/停止空闲计时器。不要在回调中假定对象已 Ready，应由对应 `QQmlIncubator` 自己检查状态。

## API 速查表

| API | 用途 | 语义与边界 |
| --- | --- | --- |
| `QQmlIncubationController()` | 创建控制器 | 通常以派生类实现自己的空闲调度。 |
| `QQmlEngine::setIncubationController()` | 安装到 engine | engine 不取得所有权，且一台 engine 只有一个 active controller。 |
| `engine()` | 查询已安装的 engine | 未安装时返回空。 |
| `incubateFor(msecs)` | 推进固定时间预算 | 可能因队列清空而提前返回。 |
| `incubateWhile(flag, msecs)` | 在原子标志为真时推进 | flag 以 acquire 读取；可用于外部请求中断。 |
| `incubatingObjectCount()` | 查询待孵化对象数量 | 用于调度决策，不是 Ready 对象数量。 |
| `incubatingObjectCountChanged(count)` | 观察数量变化 | 受保护虚函数，默认什么也不做。 |

它是帧时间调度工具，而不是“只要设置就自动异步”的开关；真正异步还依赖 `QQmlIncubator` 的模式和 engine 已安装 controller。
