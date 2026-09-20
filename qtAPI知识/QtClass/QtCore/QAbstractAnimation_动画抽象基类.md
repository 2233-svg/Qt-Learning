# QAbstractAnimation 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAbstractAnimation>`  
> 模块：`Qt6::Core`  
> 继承：`QObject -> QAbstractAnimation`  
> 常见派生类：`QVariantAnimation`、`QPropertyAnimation`、`QPauseAnimation`、`QAnimationGroup`

## 它解决什么问题

`QAbstractAnimation` 是 Qt 动画框架的共同基类。它本身不负责“把哪个属性从 A 变到 B”，而是统一解决动画都绕不开的几个问题：什么时候开始、什么时候暂停、当前跑到第几毫秒、循环几次、向前还是向后播放、结束后是否自动销毁。

换句话说，它是动画的时间线和状态机。你平时更常用 `QPropertyAnimation` 或 `QVariantAnimation`；只有在默认动画类不够用时，才派生 `QAbstractAnimation`，把自己的数据更新逻辑接进 Qt 的统一计时器。

典型场景包括：

- 做一个不直接绑定 QObject 属性的自定义动画，例如驱动游戏对象、图表采样点或音频进度。
- 把多个动画放进 `QAnimationGroup`，统一控制开始、暂停、停止。
- 只关心时间推进事件，不需要 `QVariantAnimation` 的插值系统。
- 实现非线性、事件驱动或无法提前知道时长的动画。

## 最小使用思路

`QAbstractAnimation` 是抽象类，不能直接实例化。最小派生类至少实现两个函数：

```cpp
class MeterAnimation : public QAbstractAnimation
{
public:
    using QAbstractAnimation::QAbstractAnimation;

    int duration() const override
    {
        return 1000;
    }

protected:
    void updateCurrentTime(int currentTime) override
    {
        const double progress = currentTime / double(duration());
        setMeterValue(progress);
    }
};
```

框架会在动画运行时周期性调用 `updateCurrentTime()`。调用间隔和次数没有严格保证，不能把它当成固定帧率定时器；代码应该根据传入的 `currentTime` 计算状态，而不是依赖“这次比上次多了固定毫秒”。

## 时间线、循环和方向

一个动画有两个时间概念：

- `currentTime()`：从整个动画开始算起的总进度，范围通常是 `0` 到 `totalDuration()`。
- `currentLoopTime()`：当前这一轮内部的进度，范围是 `0` 到 `duration()`。

如果 `duration()` 返回 `1000`，`loopCount()` 是 `3`，那么 `totalDuration()` 是三轮合计的时长。动画跑过第一秒后会回到本轮时间 `0`，但 `currentLoop()` 会从 `0` 变为 `1`。

`duration()` 返回 `-1` 表示时长未知或无限运行。此时动画会一直跑到你调用 `stop()`，并且多轮循环没有意义，`loopCount` 不会按有限时长那样生效。

`direction()` 控制时间推进方向：

- `Forward`：从 `0` 向 `duration()` 推进。
- `Backward`：从末尾向 `0` 推进。

改变方向时，框架会调用 `updateDirection()`，并发出 `directionChanged()`。如果你的派生类维护了方向相关的外部状态，例如音频播放方向、粒子重置策略，可以在这个钩子里同步。

## 状态机怎么工作

动画只有三种状态：

- `Stopped`：未运行，也是初始状态和自然结束后的状态。
- `Running`：正在由事件循环驱动更新时间。
- `Paused`：暂停在当前时间，之后可 `resume()`。

`start()` 会重新开始动画。动画已经停止或已经到达末尾时，再次 `start()` 会倒回开头；如果动画已经在运行，调用 `start()` 不做事。`pause()` 只暂停运行中的动画；`resume()` 只恢复暂停状态。`stop()` 会进入 `Stopped`，但不会把 `currentTime()` 清零，下一次 `start()` 才会重新从开始运行。

需要注意信号顺序：状态变化时先调用虚函数 `updateState(newState, oldState)`，然后发出 `stateChanged()`。如果动画是自然运行到最后一轮结束，会在进入 `Stopped` 后发出 `finished()`；手动 `stop()` 不代表一定有 `finished()`。

动画依赖目标线程的事件循环。没有事件循环，`start()` 后不会有持续的时间推进。GUI 程序里这通常不是问题；控制台程序或工作线程里要确认线程确实在跑事件循环。

## 删除策略和对象所有权

`start(DeleteWhenStopped)` 会让动画停止后自动删除自己。这个模式适合“一次性动画”，例如短暂提示、过渡效果或临时对象。使用时不要再用栈对象或智能指针管理同一个实例，也不要在 `finished()` 之后继续访问裸指针。

如果动画被加入 `QAnimationGroup`，销毁动画时会自动从组中移除。反过来，组通常也会管理子动画生命周期，具体所有权以 `QAnimationGroup::addAnimation()` 的约定为准。

析构正在运行的动画时，基类会先停止动画再销毁。这能避免计时器继续回调已销毁对象，但业务资源的停止和清理仍应放在派生类析构、`updateState()` 或外部控制代码里明确处理。

## 属性绑定的边界

Qt 6 的这些属性提供 `QBindable` 接口：`state`、`loopCount`、`currentTime`、`currentLoop`、`direction`。绑定适合让 UI 或业务状态观察动画进度。

不要轻易给 `currentTime` 设置长期绑定。动画运行时会持续自动写入 `currentTime`，这些写入可能取消绑定。更自然的方式是让别的属性绑定到 `currentTime`，或者监听信号后做同步。

`state` 是只读属性，但状态变化可能间接更新 `currentTime`。如果你同时依赖状态绑定和时间绑定，要把“开始、暂停、恢复、停止会改时间”的副作用考虑进去。

## 自定义派生类应该遵守的契约

`duration()` 返回当前动画单轮时长，单位是毫秒。返回值会影响循环、总时长和自然结束判断。返回 `0` 通常表示立即完成；返回 `-1` 表示无限或未知时长。

`updateCurrentTime(int currentTime)` 是最核心的回调。它可能被 `start()`、`setCurrentTime()`、方向变化、循环切换和正常推进触发；不要假设它只在运行状态下按固定频率调用。

`updateState()` 适合接管外部资源，例如启动一个真实播放器、暂停采样、停止后台任务。重写时要把 `newState` 和 `oldState` 都纳入判断，因为 `Stopped -> Running`、`Running -> Paused`、`Paused -> Running`、`Running -> Stopped` 的业务含义不同。

`updateDirection()` 只在方向改变时调用。方向不是插值公式本身，它只是告诉框架时间应该往哪个方向走；你的派生类仍然应该依据 `currentTime` 计算当前结果。

## 常见误区

- 以为 `QAbstractAnimation` 可以直接 new 出来使用；它是抽象基类。
- 在 `updateCurrentTime()` 里按固定帧率累加状态，而不是用传入时间计算状态。
- 把 `pause()` 后的动画用 `start()` 恢复，结果重新从头播放；应使用 `resume()`。
- 对 `duration() == -1` 的动画设置多轮循环，并期待它按 `loopCount` 结束。
- 使用 `DeleteWhenStopped` 后还在外部保留并访问裸指针。
- 给 `currentTime` 设置绑定后，又让动画自动推进，导致绑定被取消。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `DeletionPolicy` | 定义动画停止后的对象删除策略。 | 只影响 `start()` 启动后的停止时机，不替代 QObject 父子所有权设计。 |
| 枚举值 | `KeepWhenStopped` | 动画停止后保留对象。 | 默认策略，适合复用动画或由父对象统一管理。 |
| 枚举值 | `DeleteWhenStopped` | 动画停止后自动删除对象。 | 只能用于堆对象；停止后不要再访问原指针。 |
| 枚举 | `Direction` | 定义动画时间推进方向。 | 改方向会影响后续时间推进，并触发 `updateDirection()`。 |
| 枚举值 | `Forward` | 时间从开头向单轮结束推进。 | 默认方向。 |
| 枚举值 | `Backward` | 时间从单轮结束向开头回退。 | 派生类仍应按传入 `currentTime` 计算状态。 |
| 枚举 | `State` | 表示动画当前运行状态。 | 状态变化会先走 `updateState()`，再发 `stateChanged()`。 |
| 枚举值 | `Stopped` | 动画未运行或已结束。 | 当前时间不一定是 0；重新 `start()` 才会倒回开头。 |
| 枚举值 | `Paused` | 动画暂停在当前时间。 | 用 `resume()` 继续，不要用 `start()` 当恢复。 |
| 枚举值 | `Running` | 动画正在由事件循环驱动。 | 没有事件循环就不会持续推进。 |
| 属性 | `currentLoop` | 当前正在执行第几轮，从 0 开始。 | 默认 `loopCount` 为 1，所以通常一直是 0；变化时发 `currentLoopChanged()`。 |
| 属性 | `currentTime` | 整个动画的当前进度，单位毫秒。 | 动画推进会自动写入它，给它设置绑定可能被取消。 |
| 属性 | `direction` | 当前播放方向。 | 默认 `Forward`；改变后影响下一次时间推进。 |
| 属性 | `duration` | 单轮动画时长，单位毫秒。 | 由派生类实现；`-1` 表示未知或无限时长。 |
| 属性 | `loopCount` | 动画循环次数。 | 默认 1；0 表示不运行，-1 表示无限循环；未知时长动画不支持真正多轮。 |
| 属性 | `state` | 当前状态，只读。 | 状态变化通过命令槽触发，并可通过 `stateChanged()` 观察。 |
| 构造 | `QAbstractAnimation(QObject *parent = nullptr)` | 构造动画基类并设置 QObject 父对象。 | 不能直接实例化本类，通常由派生类构造时调用。 |
| 析构 | `~QAbstractAnimation()` | 停止仍在运行的动画并销毁对象。 | 若属于动画组，会在销毁前从组中移除。 |
| 绑定 | `bindableState()` | 返回 `state` 的绑定接口。 | 只读观察状态，不直接修改。 |
| 绑定 | `bindableCurrentLoop()` | 返回 `currentLoop` 的绑定接口。 | 适合驱动进度显示或调试状态。 |
| 绑定 | `bindableCurrentTime()` | 返回 `currentTime` 的绑定接口。 | 不建议给它设置会被动画推进覆盖的绑定。 |
| 绑定 | `bindableDirection()` | 返回 `direction` 的绑定接口。 | 可用于把播放方向与 UI 状态同步。 |
| 绑定 | `bindableLoopCount()` | 返回 `loopCount` 的绑定接口。 | 修改循环次数前确认当前动画是否正在运行。 |
| 查询 | `state()` | 返回当前 `Stopped`、`Paused` 或 `Running`。 | 不要用它代替 `finished()` 判断自然结束。 |
| 查询 | `group()` | 返回所属 `QAnimationGroup`，没有则为 `nullptr`。 | 动画加入组后，启动逻辑通常由组控制。 |
| 查询 | `direction()` | 返回当前播放方向。 | 方向为 `Backward` 时当前时间会向 0 推进。 |
| 设置 | `setDirection(Direction direction)` | 设置播放方向。 | 会触发 `updateDirection()` 和 `directionChanged()`。 |
| 查询 | `currentTime()` | 返回整个动画当前毫秒位置。 | 可能跨越多轮，不等同于当前轮内部时间。 |
| 设置 | `setCurrentTime(int msecs)` | 手动跳到指定时间位置。 | 会导致 `updateCurrentTime()` 被调用，可用于拖动进度条。 |
| 查询 | `currentLoopTime()` | 返回当前循环内部的毫秒位置。 | 范围通常是 0 到 `duration()`。 |
| 查询 | `loopCount()` | 返回循环次数。 | 1 是默认值；-1 表示一直循环直到停止。 |
| 设置 | `setLoopCount(int loopCount)` | 设置循环次数。 | `duration() == -1` 时多轮循环没有通常意义。 |
| 查询 | `currentLoop()` | 返回当前循环编号。 | 第一轮是 0，不是 1。 |
| 查询 | `duration()` | 返回单轮时长。 | 纯虚函数；自定义动画必须实现。 |
| 查询 | `totalDuration()` | 返回包含循环次数后的总时长。 | 无限或未知时长通常会反映为无法确定的持续时间。 |
| 槽 | `start(DeletionPolicy policy = KeepWhenStopped)` | 从头开始或重新开始动画。 | 已运行时调用无效果；`DeleteWhenStopped` 会自动销毁对象。 |
| 槽 | `pause()` | 暂停当前运行。 | 保留当前时间，之后可 `resume()`。 |
| 槽 | `resume()` | 从暂停位置继续运行。 | 不会改变 `currentTime()`。 |
| 槽 | `setPaused(bool paused)` | 根据布尔值暂停或恢复。 | 适合直接连接复选框、动作或状态切换。 |
| 槽 | `stop()` | 停止动画。 | 保留当前时间；手动停止不一定发 `finished()`。 |
| 信号 | `finished()` | 自然到达最后一轮末尾并停止后发出。 | 发出顺序在 `stateChanged()` 之后。 |
| 信号 | `stateChanged(State newState, State oldState)` | 状态变化通知。 | 在 `updateState()` 调用之后发出。 |
| 信号 | `currentLoopChanged(int currentLoop)` | 当前循环轮次变化通知。 | 多轮动画跨轮时触发。 |
| 信号 | `directionChanged(Direction newDirection)` | 播放方向变化通知。 | 与 `setDirection()` 和绑定变化相关。 |
| 保护函数 | `updateCurrentTime(int currentTime)` | 派生类按当前时间更新动画效果的核心回调。 | 纯虚函数；不能依赖固定调用频率。 |
| 保护函数 | `updateState(State newState, State oldState)` | 派生类观察启动、暂停、恢复、停止等状态切换。 | 适合启动或释放外部资源。 |
| 保护函数 | `updateDirection(Direction direction)` | 派生类观察播放方向改变。 | 默认实现为空，只在确有方向相关资源时重写。 |
| 保护函数 | `event(QEvent *event)` | 处理动画框架内部事件。 | 一般不重写；若重写需保留 QObject 事件处理语义。 |

## 一句话总结

`QAbstractAnimation` 是动画框架的时间线和状态机基座。自定义动画时只要牢牢抓住三件事：`duration()` 定义单轮时长，`updateCurrentTime()` 按时间计算效果，`start()`、`pause()`、`resume()`、`stop()` 负责状态切换和生命周期。
