# Qt QVariantAnimation：在两个 QVariant 值之间产生动画帧

`QVariantAnimation` 是 Qt 动画框架中负责“计算中间值”的基类。它按时间、缓动曲线和关键帧，在两个 `QVariant` 之间不断插值，更新 `currentValue` 并发射 `valueChanged()`；至于这个值最终写到哪里，由调用者或子类决定。

它适合动画并非 Qt 属性的状态，例如让自绘图表的刻度、音频参数、渲染器状态或业务模型中的数值平滑变化。若目标就是某个 `QObject` 的 Qt 属性，通常应直接使用它的子类 `QPropertyAnimation`，少写一层“收到值后再 setProperty”的胶水代码。

```cpp
#include <QVariantAnimation>

auto *animation = new QVariantAnimation(this);
animation->setDuration(300);
animation->setStartValue(0.0);
animation->setEndValue(1.0);
animation->setEasingCurve(QEasingCurve::OutCubic);

connect(animation, &QVariantAnimation::valueChanged, this,
        [this](const QVariant &value) {
            m_opacity = value.toReal();
            update();
        });

animation->start(QAbstractAnimation::DeleteWhenStopped);
```

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QVariantAnimation>`  
> CMake：`Qt6::Core`  
> 继承：`QObject -> QAbstractAnimation -> QVariantAnimation`

## 它解决什么问题

“从 `a` 变到 `b`”听起来只是一个公式，但 UI、绘制和状态动画还需要处理持续时间、暂停、重启、循环、反向播放、缓动、关键帧和对象寿命。`QVariantAnimation` 把这些时间轴工作交给 `QAbstractAnimation`，把某一时刻的结果交给 `QVariant` 插值机制。

它**不会自动修改任意对象**。动画运行时的默认结果是：

1. 根据 `currentTime()`、`duration()` 和 `QEasingCurve` 得到有效进度；
2. 在起点、终点和可选关键帧之间求出 `currentValue`；
3. 调用虚函数 `updateCurrentValue(value)`；
4. 发射 `valueChanged(value)`。

基类的 `updateCurrentValue()` 什么也不做，所以使用者至少要二选一：

- 连接 `valueChanged()`，将 `QVariant` 转换后应用到自己的状态；
- 派生 `QVariantAnimation` 并重写 `updateCurrentValue()`。

`QPropertyAnimation` 选择第二条路，把每一帧写入指定 `QObject` 属性。因此，常规控件属性动画优先选它；`QVariantAnimation` 的价值在于不要求目标是 Qt 属性。

## 一个合适的实际场景：驱动自绘状态

下面让一个自绘部件的数值从当前值滑到目标值。动画对象有 `this` 作为父对象，部件销毁时会一并销毁；每一帧由信号改变绘制状态。

```cpp
void MeterWidget::animateTo(qreal target)
{
    auto *animation = new QVariantAnimation(this);
    animation->setDuration(220);
    animation->setStartValue(m_displayValue);
    animation->setEndValue(target);
    animation->setEasingCurve(QEasingCurve::OutQuart);

    connect(animation, &QVariantAnimation::valueChanged, this,
            [this](const QVariant &value) {
                m_displayValue = value.toReal();
                update();
            });

    animation->start(QAbstractAnimation::DeleteWhenStopped);
}
```

这里 `DeleteWhenStopped` 很实用，但也改变了生命周期：动画停止后 Qt 会删除它。启动后不要再把裸指针当作可长期访问的对象保存；若外部确实要观察寿命，使用带 context 的信号连接、`QPointer`，或由明确所有者在合适时机销毁。

## 起点、终点、时间和缓动

### `startValue` 是可选的

`setStartValue()` / `setEndValue()` 接受 `QVariant`。终点通常必须明确设置；起点可以省略，也可以设置 null `QVariant`。这时动画在**启动时**采用终点当前所在的位置作为起点。这个语义主要服务于属性动画：例如目标属性已经是 40，就从 40 动到设定的终点。

对裸 `QVariantAnimation` 而言，没有目标属性可读取时，不应把“未设置起点”当作会自动读取你的业务变量。要得到确定行为，应显式设置起点。

### 默认动画是 250 ms 的线性变化

`duration` 单位是毫秒，默认值为 250；`easingCurve` 默认是线性曲线。它们都是 `QProperty` 可绑定属性，普通动画代码仍以 setter 最直接：

```cpp
animation.setDuration(500);
animation.setEasingCurve(QEasingCurve::InOutCubic);
```

动画的原始进度大致来自“本轮已过时间 / 持续时间”。`QEasingCurve::valueForProgress()` 会把它转换为**有效进度**，而这个有效进度才传给关键帧选择和 `interpolated()`。因此关键帧步长并不总是等间隔时间点：`OutCubic` 之类会让变化前快后慢。

部分曲线，例如 `QEasingCurve::InBack`，可能产生小于 0 或大于 1 的有效进度。自定义 `interpolated()` 不能武断地把 `progress` 当作必然位于 `[0, 1]`；应支持外推，或在数据类型不能外推时做合理钳制。

### 运行依赖事件循环

`start()`、`pause()`、`resume()`、`stop()`、循环、方向和删除策略来自 `QAbstractAnimation`。调用 `start()` 后，只有对象线程的 Qt 事件循环在运行，框架才会继续推进时间并产生后续帧。动画通常应创建、配置和启动在同一个有事件循环的线程中；不要跨线程直接修改动画或让工作线程直接触碰 GUI 状态。

`start()` 会在已停止或已播完时从头开始；暂停后用 `resume()` 从原时间继续；手动 `stop()` 不等同自然播放完成，是否发射基类的 `finished()` 取决于停止原因。高频帧回调中也不要执行阻塞 I/O 或昂贵计算。

## 关键帧：进度位置不是毫秒

关键帧用 `KeyValue` 表示：

```cpp
using KeyValue = std::pair<qreal, QVariant>;
using KeyValues = QList<KeyValue>;
```

其中第一个值是 `step`，范围必须是 `0.0` 到 `1.0`；第二个值是该步长的值。`0.0` 和 `1.0` 分别就是起点和终点。

```cpp
animation.setKeyValueAt(0.0, 0);
animation.setKeyValueAt(0.55, 90);
animation.setKeyValueAt(1.0, 100);
```

`keyValueAt(step)` 只查询**恰好存在**的关键帧，若该位置没有帧则返回无效 `QVariant`，它不会替你计算邻近插值值。`setKeyValues()` 会整体替换已有关键帧；其每个 step 都必须在闭区间 `[0, 1]`。外部配置数据应在调用前验证范围，而不是依赖调试断言暴露输入错误。

特别注意：这里的 step 对应的是经过缓动后的有效进度，不是 `duration * step` 的裸时间点。若产品要求“第 250 ms 必须碰到某个值”，需要考虑缓动曲线，或自行控制 `currentTime`。

## 哪些 QVariant 能被 Qt 默认插值

Qt 6.11.1 默认支持以下 `QVariant` 元类型：

- `Int`、`UInt`、`Double`、`Float`
- `QLine`、`QLineF`
- `QPoint`、`QPointF`
- `QSize`、`QSizeF`
- `QRect`、`QRectF`
- `QColor`

起点、终点和关键帧应使用相容的类型。无法插值的类型不会凭空产生合理中间值；在连接槽中盲目 `toInt()` 或 `value<T>()` 也可能掩盖类型配置错误。

## 自定义插值：全局注册和局部重写

对自定义元类型，可以在构造任何此类动画**之前**注册全局插值器：

```cpp
struct Gain {
    qreal db = 0;
};
Q_DECLARE_METATYPE(Gain)

QVariant interpolateGain(const Gain &from, const Gain &to, qreal progress)
{
    return QVariant::fromValue(
        Gain { from.db + (to.db - from.db) * progress });
}

qRegisterAnimationInterpolator<Gain>(interpolateGain);
```

`qRegisterAnimationInterpolator<T>()` 的函数签名固定为 `QVariant (*)(const T &, const T &, qreal)`。传入 `nullptr` 可取消该类型的自定义注册并恢复默认插值器；注册函数本身是线程安全的，但不要因此推断正在运行的动画可以跨线程操作。由于注册会影响该类型之后构造的动画，应在应用初始化阶段完成，并避免让模块彼此覆盖同一类型的插值策略。

另一种方式是派生并重写 `interpolated(from, to, progress)`。这适合某一个动画实例或某一类动画需要不同策略，例如角度取最短路径、逻辑状态分段跳变或对进度进行钳制。若派生类还希望保留 Qt 支持类型的默认能力，未知类型分支应调用 `QVariantAnimation::interpolated()`。

```cpp
QVariant AngleAnimation::interpolated(
    const QVariant &from, const QVariant &to, qreal progress) const
{
    if (from.canConvert<qreal>() && to.canConvert<qreal>()) {
        const qreal a = from.toReal();
        const qreal b = to.toReal();
        const qreal delta = std::remainder(b - a, 360.0);
        return a + delta * progress;
    }
    return QVariantAnimation::interpolated(from, to, progress);
}
```

## 生命周期、线程与常见错误

`QVariantAnimation` 是 `QObject`，不可拷贝，有线程归属。父对象销毁会销毁它；析构时基类会停止运行中的动画。动画属于 `QAnimationGroup` 时，销毁前也会自动从组中移除。

- 把 `QVariantAnimation` 当成属性动画使用，却没有连接 `valueChanged()` 或重写 `updateCurrentValue()`，因此看不到任何变化。
- 未显式设置 `startValue`，却期望裸动画读取某个普通成员变量。
- 使用 `DeleteWhenStopped` 后继续访问动画指针。
- 把关键帧的 step 当作毫秒，或传入不在 `[0, 1]` 内的值。
- 用支持过冲的缓动曲线，却让自定义插值器只能处理 `[0, 1]`。
- 在动画构造后才注册自定义插值器。
- 在没有运行事件循环的线程中启动动画，或在帧回调里阻塞线程。
- 对未受支持或类型不一致的 `QVariant` 假定 Qt 会自动转换并插值。

## API 速查表

下表列出 `QVariantAnimation` 自身公开 API；`start()`、`stop()`、循环、方向、状态和删除策略等继承 API 见 `QAbstractAnimation`。

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QVariantAnimation(QObject *parent = nullptr)` | 创建动画 | `parent` 管理 QObject 生命周期；默认时长 250 ms、线性缓动。 |
| `~QVariantAnimation()` | 销毁动画 | 运行中销毁会停止动画；不要保存悬空指针。 |
| `KeyValue` | 一个关键帧类型 | 即 `std::pair<qreal, QVariant>`；前者是 `[0, 1]` 的有效进度位置。 |
| `KeyValues` | 关键帧列表类型 | 即 `QList<KeyValue>`；可整体传给 `setKeyValues()`。 |
| `startValue()` | 读取起点 | 起点可为无效/null；裸动画最好显式设置。 |
| `setStartValue(value)` | 设置起点 | null 或省略时，启动时使用终点当前值的语义主要面向属性动画。 |
| `endValue()` | 读取终点 | 通常应在启动前明确设置。 |
| `setEndValue(value)` | 设置终点 | 与起点、关键帧必须能够按所选插值器处理。 |
| `currentValue()` | 读取当前插值值 | 只读；值变化时同步调用 hook 并发射 `valueChanged()`。 |
| `duration()` | 读取本轮持续时间 | 单位毫秒；循环总时长由基类的 `totalDuration()` 计算。 |
| `setDuration(msecs)` | 设置持续时间 | 普通有限动画应使用非负毫秒值；它是可绑定属性。 |
| `bindableDuration()` | 获取 `duration` 的绑定接口 | 用于 `QProperty` 绑定；状态改变时需理解绑定所有权。 |
| `easingCurve()` | 读取缓动曲线 | 默认线性；它改变有效进度，而不只是视觉效果。 |
| `setEasingCurve(easing)` | 设置缓动曲线 | 可能产生小于 0 或大于 1 的有效进度。 |
| `bindableEasingCurve()` | 获取 `easingCurve` 绑定接口 | 用于 `QProperty` 绑定。 |
| `keyValueAt(step)` | 查询某一步的关键帧值 | `step` 必须在 `[0, 1]`；没有精确匹配的关键帧时返回无效 `QVariant`。 |
| `setKeyValueAt(step, value)` | 新建或修改一个关键帧 | `0.0` 和 `1.0` 分别定义起点和终点；step 不是毫秒。 |
| `keyValues()` | 取得当前全部关键帧 | 返回列表副本，用于检查或整体修改。 |
| `setKeyValues(values)` | 替换全部关键帧 | 列表中的每个 step 都必须在 `[0, 1]`。 |
| `valueChanged(const QVariant &value)` | 通知当前值改变 | 可连接到槽/lambda 应用结果；连接时提供接收 context 以避免悬空回调。 |
| `qRegisterAnimationInterpolator<T>(func)` | 为类型注册全局插值器 | 必须在动画构造前注册；`nullptr` 取消注册；该函数线程安全。 |

### 受保护扩展点

| API | 用途 | 重写时注意 |
| --- | --- | --- |
| `updateCurrentValue(value)` | 每次当前值变化时接收新值 | 基类无操作；适合将结果写到非属性目标。不要做阻塞工作。 |
| `interpolated(from, to, progress)` | 返回两值之间的中间值 | `progress` 可能越过 `[0, 1]`；希望保留内置类型支持时调用基类实现。 |
| `updateCurrentTime(int)` | 框架推进时间时计算帧 | 框架内部调用，通常不要从外部手工调用。 |
| `updateState(newState, oldState)` | 处理动画状态转换 | 处理启动、暂停、停止等内部状态；保持基类契约。 |
| `event(QEvent *)` | 处理 Qt 事件 | 框架实现细节；除非确有事件扩展需求，一般不重写。 |

---

### 一句话总结

`QVariantAnimation` 管理“随时间计算 QVariant 中间值”，但不决定“把值写到哪里”；非属性状态用信号或 `updateCurrentValue()` 消费每一帧，普通 QObject 属性则优先选择 `QPropertyAnimation`。
