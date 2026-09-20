# Qt QTimeLine：用时间轴驱动离散动画

`QTimeLine` 是一个面向 `QObject` 的时间轴对象。它在指定的毫秒时长内推进一个“当前时间”，再把这个时间映射成 `0.0..1.0` 的动画值，或者映射成起止帧之间的整数帧。外部对象通过连接 `valueChanged(qreal)` 或 `frameChanged(int)`，把时间轴变成进度条变化、控件位置变化、颜色过渡或其它动画效果。

它适合“我只需要一个时间进度源，然后自己决定每一帧做什么”的场景。若要直接动画化 Qt 属性，通常优先考虑 `QPropertyAnimation`；若要组合并行、串行动画，使用 Qt Animation Framework 中的 `QAbstractAnimation`、`QParallelAnimationGroup` 等类型更自然。

```cpp
#include <QProgressBar>
#include <QTimeLine>

auto *line = new QTimeLine(1000, this);
line->setFrameRange(0, 100);

connect(line, &QTimeLine::frameChanged,
        progressBar, &QProgressBar::setValue);
connect(startButton, &QPushButton::clicked,
        line, &QTimeLine::start);
```

## 它解决什么问题

动画通常需要三个独立概念：

1. 动画运行多久。
2. 当前进行到哪一步。
3. 如何把这一步转换成业务值。

`QTimeLine` 把前两项和常见的插值策略封装起来，并通过信号把变化送给业务对象。默认情况下，它以 `QEasingCurve::InOutSine` 计算从 `0` 到 `1` 的平滑值；你可以把这个值直接用于自定义动画，也可以配置帧范围，让它输出整数帧。

它不是绘图引擎，也不会自动修改任意控件。`QTimeLine` 只负责产生时间、值和帧，真正的 UI 更新发生在你连接的槽或回调中。

## 生命周期与事件循环

`QTimeLine` 继承 `QObject`。通常给它设置一个合适的 parent，让父对象负责销毁；也可以把它作为成员对象保存。对象销毁时，时间轴会停止并清理自身的内部定时器。

时间轴依靠所属线程的事件循环推进。调用 `start()` 只会把状态切换为 `Running`，后续的时间更新要等事件循环继续运行。如果在线程中创建时间轴却没有运行事件循环，就不会得到正常的周期更新。跨线程使用时，不要直接从其它线程读写同一个对象，应通过 queued signal/slot 或 `QMetaObject::invokeMethod()` 把操作投递到对象所属线程。

```cpp
auto *line = new QTimeLine(600, owner);
line->setFrameRange(0, 30);
line->setUpdateInterval(16);
line->start();
```

默认更新间隔是 40 ms，大约每秒 25 次。它只是更新请求的间隔，不是“每次一定精确经过多少毫秒”，也不保证固定帧率。系统调度、主线程阻塞和槽函数执行时间都会影响实际回调时刻。需要平滑动画时可以把间隔设置为接近显示刷新周期，但不要在槽里做长时间阻塞工作。

## 状态机：启动、暂停、恢复、停止

`State` 有三个值：

| 状态 | 含义 |
| --- | --- |
| `NotRunning` | 初始或停止状态，不再自动更新 |
| `Paused` | 暂停自动更新，当前位置保留 |
| `Running` | 时间轴在事件循环中持续推进 |

`start()` 总是重新开始：正向时从时间 `0` 开始，反向时从时长末尾开始。想从当前位置继续，应使用 `resume()` 或 `setPaused(false)`。`stop()` 进入 `NotRunning`，保留停止时的当前时间、帧和值；再次 `start()` 会重新起步。

```cpp
line->start();             // 从起点或终点重新开始
line->setPaused(true);     // 保留当前位置
line->setPaused(false);    // 从当前位置继续
line->stop();              // 停止并保留当前位置
line->resume();            // 从停止时的位置继续
```

`finished()` 只在时间轴真正到达终点并结束时发出。循环播放时，中间的每次回绕都不是完成，只有最后一次播放结束才会发出 `finished()`。

## 时间、值与帧的三层关系

### `currentTime`

`currentTime` 是从 `0` 到 `duration()` 的时间位置，单位是毫秒。运行中它会自动变化；停止或暂停时，它保持最近位置，除非你调用 `setCurrentTime()`。

可以把其它属性绑定到 `currentTime`，但不建议给 `currentTime` 设置持续性的绑定。动画推进会主动写入当前时间，从而取消该绑定。

### `currentValue`

`currentValue()` 返回当前时间对应的动画值，通常在 `0.0..1.0` 之间。`valueChanged()` 只在值发生变化时发出，信号参数就是当前值。

```cpp
connect(line, &QTimeLine::valueChanged, this, [this](qreal value) {
    const int width = qRound(value * maximumWidth);
    panel->setFixedWidth(width);
});
```

### 帧范围

`setFrameRange(startFrame, endFrame)` 建立一个线性帧范围。`frameForTime(msec)` 先计算 `valueForTime(msec)`，再用该值在起止帧之间插值；因此使用 easing curve 时，帧速度也会随曲线变化。`frameChanged()` 只在整数帧真正变化时发出，更新间隔过小并不意味着每个定时器 tick 都会收到新帧。

起始帧可以大于结束帧，具体业务上可以用它表达反向数值范围；方向属性则控制时间如何前进。不要把“负向帧范围”和 `Backward` 方向混成同一件事，它们分别影响帧映射和时间推进。

## 方向、循环和修改配置

`Direction::Forward` 让时间从 `0` 向 `duration` 增长，`Backward` 让时间从 `duration` 向 `0` 减少。`toggleDirection()` 反转方向，而且会移除 `direction` 属性上已有的绑定；如果依赖绑定关系，改用 `setDirection()` 前也要意识到显式 setter 同样会覆盖该属性的绑定。

`loopCount` 默认是 `1`，表示只运行一次；设置为 `0` 表示无限循环。循环只在时长有效且大于 0 时有实际意义。每次循环从另一端重新开始当前时间，外部只会看到值/帧继续变化；要区分第几圈，应自行监听状态和记录业务计数。

改变 `duration` 不会自动把 `currentTime` 重置到零或裁剪到新时长。修改时长后，如果当前时间可能越界，应显式调用 `setCurrentTime()` 设到你希望的位置。运行中的配置变更也可能导致下一次更新立即反映新规则，关键交互中应在停止或暂停时调整配置。

## easing 与自定义曲线

`setEasingCurve()` 选择 `QEasingCurve` 提供的预设或自定义曲线。曲线接收归一化时间，输出通常位于 `0..1`，决定动画快慢而不是动画对象的具体单位。

```cpp
line->setEasingCurve(QEasingCurve::OutCubic);
```

需要完全自定义映射时，可以继承 `QTimeLine` 并重写 `valueForTime(int msec) const`。重写后，`easingCurve` 属性会被忽略。实现应当根据 `msec` 和 `duration()` 产生稳定、可预测的值；通常保持 `0..1` 范围，避免让下游帧计算得到意外结果。

```cpp
class PulseLine final : public QTimeLine
{
public:
    using QTimeLine::QTimeLine;

protected:
    qreal valueForTime(int msec) const override
    {
        const qreal progress = qreal(msec) / duration();
        return 0.5 + 0.5 * qSin(progress * 2.0 * M_PI);
    }
};
```

自定义实现要注意 `duration()` 不能为零，并根据项目的数学常量和浮点精度要求选择实现。对于普通的缓入缓出，不必继承，直接配置 `QEasingCurve` 更易维护。

## 信号的使用方式

`valueChanged`、`frameChanged`、`stateChanged` 和 `finished` 在文档中标记为 private signal。这表示用户不能手动发射它们，但可以正常连接。

- 需要连续的归一化进度：连接 `valueChanged`。
- 需要整数进度或控件值：设置帧范围后连接 `frameChanged`。
- 需要知道暂停、运行、停止：连接 `stateChanged`。
- 需要在最后一圈结束后执行动作：连接 `finished`。

这些信号只会在时间轴实际更新时发出，不是同步调用 `start()` 就立即发出完整序列。测试时要启动事件循环，不能只构造对象后立即断言动画已经结束。

## 常见错误

- 以为 `start()` 会从暂停位置继续。`start()` 会重新开始；继续播放用 `resume()`。
- 把 `updateInterval` 当成精确帧率。它是更新请求间隔，实际回调受事件循环和系统调度影响。
- 在线程没有事件循环的 worker 中使用时间轴。时间轴不会正常推进。
- 连接了 `valueChanged` 却忘了真正修改目标对象。`QTimeLine` 不会自动驱动控件属性。
- 修改 `duration` 后假设当前位置自动归零或自动裁剪。应主动调用 `setCurrentTime()`。
- 用 `frameChanged` 做精细浮点动画。整数帧会丢失中间值，应使用 `valueChanged`。
- 重写 `valueForTime()` 后还期待 `setEasingCurve()` 生效。自定义函数会覆盖默认 easing。
- 把无限循环的 `loopCount(0)` 当作“循环零次”。在 `QTimeLine` 中它表示一直循环。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QTimeLine(int duration = 1000, QObject *parent = nullptr)` | 创建时间轴 | 默认时长 1000 ms；时长应大于 0；遵守 QObject parent 生命周期 |
| `~QTimeLine()` | 销毁时间轴 | QObject 析构时停止并释放内部资源 |
| `state()` | 查询当前状态 | 返回 `NotRunning`、`Paused` 或 `Running` |
| `start()` | 从头启动 | 正向从 0 开始，反向从 duration 开始；不会从停止位置续播 |
| `resume()` | 从当前时间继续 | 与 `start()` 不同，不重置当前时间 |
| `stop()` | 停止时间轴 | 进入 `NotRunning`，保留当前时间、帧和值 |
| `setPaused(bool paused)` | 暂停或恢复 | `true` 保留位置并暂停；`false` 从当前位置继续 |
| `setCurrentTime(int msec)` | 直接设置时间位置 | 会更新对应值和帧；运行中主动写入会影响自动推进 |
| `currentTime()` | 查询当前时间 | 单位毫秒；默认是 0 |
| `setDuration(int duration)` | 设置总时长 | 时长必须大于 0；不会自动重置当前时间 |
| `duration()` | 查询总时长 | 单位毫秒；默认 1000 |
| `setDirection(Direction)` | 设置时间推进方向 | `Forward` 从 0 到 duration，`Backward` 反向 |
| `direction()` | 查询方向 | 默认 `Forward` |
| `toggleDirection()` | 反转方向 | 会移除 direction 属性上的绑定 |
| `setLoopCount(int count)` | 设置循环次数 | 默认 1；`0` 表示无限循环 |
| `loopCount()` | 查询循环次数 | 只在有限时长下有正常循环语义 |
| `setUpdateInterval(int interval)` | 设置更新请求间隔 | 默认 40 ms；不是精确帧率，受事件循环调度影响 |
| `updateInterval()` | 查询更新间隔 | 单位毫秒 |
| `setEasingCurve(const QEasingCurve &curve)` | 设置插值曲线 | 自定义重写 `valueForTime()` 后该属性被忽略 |
| `easingCurve()` | 查询插值曲线 | 默认是 `QEasingCurve::InOutSine` |
| `currentValue()` | 查询当前归一化值 | 通常在 `0.0..1.0`，由 easing 或重写函数决定 |
| `valueForTime(int msec) const` | 把时间映射为值 | 可重写；通常应返回稳定的 `0..1` 值 |
| `setStartFrame(int frame)` | 设置起始帧 | 该帧对应值 0 |
| `startFrame()` | 查询起始帧 | 由帧范围配置决定 |
| `setEndFrame(int frame)` | 设置结束帧 | 该帧对应值 1 |
| `endFrame()` | 查询结束帧 | 由帧范围配置决定 |
| `setFrameRange(int startFrame, int endFrame)` | 设置帧范围 | 帧通过 `valueForTime()` 在两端之间插值 |
| `currentFrame()` | 查询当前帧 | 当前时间映射到帧范围后的整数结果 |
| `frameForTime(int msec)` | 查询任意时间对应帧 | 使用当前 value/easing 计算，不会改变当前时间 |
| `valueChanged(qreal value)` | 监听归一化值变化 | private signal，只能连接不能手动发射 |
| `frameChanged(int frame)` | 监听整数帧变化 | 只有帧实际改变时发出 |
| `stateChanged(QTimeLine::State newState)` | 监听状态切换 | private signal；可用于观察运行、暂停、停止 |
| `finished()` | 监听最终完成 | 循环播放时只在最后一圈结束后发出 |
| `bindableCurrentTime()` 等 `bindable...()` | 接入 QProperty 绑定 | `currentTime` 适合被读取和被其它属性依赖，不适合设置持续绑定 |
| `timerEvent(QTimerEvent *)` | 内部定时器处理 | protected 重写点；通常不应从业务代码直接调用 |
