# QSequentialAnimationGroup：按时间顺序编排 Qt 动画

> 适用版本：Qt 6.11.1  
> 所属头文件：`#include <QSequentialAnimationGroup>`  
> 所属模块：Qt Core  
> 继承关系：`QAbstractAnimation -> QAnimationGroup -> QSequentialAnimationGroup`

`QSequentialAnimationGroup` 把多个 `QAbstractAnimation` 排成一条时间线：前一个完成后，下一个才开始。任何时刻组内至多有一个活动子动画；最后一个结束后，整个组结束。

它适合表达“先淡入，再移动，再停顿，再淡出”这类有明确先后依赖的交互。若动画应该同时运行，应使用 `QParallelAnimationGroup`，不要靠多个顺序组互相手工同步。

## 它解决的问题

没有动画组时，业务代码往往要在每个子动画的 `finished()` 信号里手工启动下一个动画。这样会很快出现重入、取消、反向播放、暂停、循环和对象销毁的边界问题。

顺序组把这些步骤变成一个可作为整体控制的动画：

```cpp
auto *group = new QSequentialAnimationGroup(this);

auto *fadeIn = new QPropertyAnimation(panel, "opacity");
fadeIn->setDuration(150);
fadeIn->setStartValue(0.0);
fadeIn->setEndValue(1.0);

auto *move = new QPropertyAnimation(panel, "pos");
move->setDuration(220);
move->setEndValue(QPoint(120, 80));

group->addAnimation(fadeIn);
group->addPause(80);
group->addAnimation(move);
group->start();
```

这里调用者启动的是组，不是 `fadeIn` 或 `move`。组负责在正确时刻切换子动画、传播状态和方向，并在结束时发出从 `QAbstractAnimation` 继承的 `finished()`。

## 顺序、当前动画与时长

子动画按加入顺序运行，`addAnimation()` 追加到末尾，`insertAnimation(index, ...)` 插入指定位置。每一段的局部时长由子动画的 `duration()` 与其 `loopCount` 共同影响；顺序组的 `duration()` 是各子动画局部时长之和，而组的 `totalDuration()` 还会纳入组自身的循环次数。

若某个子动画的 `duration()` 为 `-1`，它表示无固定时长、需要显式停止。将这种动画放在顺序组中，后续动画不能按正常时间线自然开始；设计流程时应避免把“不知道何时结束”的动画放在必须继续推进的步骤之前。

`currentAnimation()` 返回当前时间点的活动子动画。空组返回 `nullptr`。它是只读属性，不应通过保存其裸指针来猜测未来时间线；组可能在暂停、反向播放、跳转当前时间、停止或子动画重排时改变当前项。

```cpp
connect(group, &QSequentialAnimationGroup::currentAnimationChanged,
        this, [this](QAbstractAnimation *current) {
    if (current == m_moveAnimation)
        showMoveHint();
});
```

信号的参数可能是 `nullptr`，特别是在空组或没有可用当前动画的状态边界。槽函数应检查指针，不要假定它一定是某个 `QPropertyAnimation`。

## 所有权：加入即交给动画组

`QSequentialAnimationGroup` 继承 `QAnimationGroup`，而 `QAnimationGroup` 接管其子动画的所有权。组销毁时会销毁仍在其中的所有子动画：

```cpp
auto *animation = new QPropertyAnimation(target, "geometry");
group->addAnimation(animation);  // group 现在拥有 animation
```

因此不要在 `addAnimation()` 后再手动 `delete animation`，也不要把同一个动画对象同时放入两个组。若要收回所有权：

```cpp
QAbstractAnimation *ownedByCaller = group->takeAnimation(index);
// 调用方现在负责删除或加入另一个组
```

`removeAnimation(animation)` 同样把所有权移交给调用方。`clear()` 则删除组内所有动画。父子 QObject 所有权和动画组所有权要按一个来源管理，避免让外部父对象、`DeleteWhenStopped` 和组析构同时竞争同一子动画的销毁责任。

特别注意：顶层组可调用 `start()`；已作为另一个组子项的组不应被直接启动，否则行为可能出乎预期。嵌套动画应从最外层组统一启动、暂停、停止和设定方向。

## 暂停不是定时器，而是一个子动画

`addPause(msecs)` 与 `insertPause(index, msecs)` 创建并加入 `QPauseAnimation`，返回其指针。暂停会占用时间线，也会计入 `animationCount()`：

```cpp
group->addAnimation(fadeOut);
QPauseAnimation *hold = group->addPause(500);
group->addAnimation(fadeIn);
```

这意味着 pause 可像其他子动画一样被检索、移除或替换。需要根据运行状态动态修改暂停长度时，保存返回的 `QPauseAnimation *`，并与其组所有权一致地管理生命周期。

`insertPause()` 的 `index` 应使用当前组的有效插入位置，通常是 `0` 到 `animationCount()`。由用户输入或异步逻辑计算出的索引应在调用前校验；不要把无效索引当作会自动追加的容错接口。

## 状态、事件循环与反向播放

顺序组本身是 `QAbstractAnimation`，因此可使用：

- `start()`、`stop()`、`pause()`、`resume()`；
- `setCurrentTime()` 跳到时间线指定位置；
- `setLoopCount()` 控制整个序列循环次数；
- `setDirection(Forward/Backward)` 正向或反向播放；
- `finished()`、`stateChanged()` 等继承信号观察整体状态。

调用 `start()` 后，动画依赖对象所属线程的事件循环自动推进。`start()` 会从起点重新开始已停止或已经走到终点的动画；已经运行时再次 `start()` 不会重启它。暂停后 `resume()` 从原时间继续；`stop()` 不改变当前时间，但之后再次 `start()` 会从开头启动。

框架不会承诺 `updateCurrentTime()` 的精确调用间隔或调用次数。不要把动画回调当作固定帧率计时器，也不要把“每次 update”当作必须发生的离散业务事件。若业务逻辑需要可靠的状态转换，应由明确的信号、状态机或完成回调驱动。

逆向播放时，时间线按相反方向经过子动画。子动画自身必须支持你期望的 backward 视觉语义；仅仅把组改成 `Backward` 并不能修复错误的起止值或依赖前一段副作用的动画设计。

## 运行时修改与线程边界

组、子动画和它们通常驱动的 `QObject` 属性都应在同一对象线程中操作。对 `QWidget`、`QQuickItem` 等 GUI 对象，实际就是 GUI 线程。不要从工作线程直接调用 `addAnimation()`、`clear()`、`start()` 或改动目标对象属性；通过 queued signal 把请求交回对象线程。

虽然基类提供增删动画接口，运行中的时间线会有当前项、已过时间和所有权状态。实际产品代码应在组停止或暂停并明确处理当前位置后再改动顺序、移除当前动画或清空组。这样可避免业务逻辑仍持有刚被删除的子动画指针，也能让视觉状态的切换可预测。

若使用 `start(QAbstractAnimation::DeleteWhenStopped)` 启动组，组结束后会自动删除。此时不要在 `finished()` 的异步后续逻辑中继续解引用 group 指针；使用 QObject context 连接、`QPointer` 或让外部对象重新创建下一次动画。

## 常见错误

1. **直接启动已嵌套的子组。** 只启动最外层动画组。
2. **加入子动画后仍手动 delete。** 组已经拥有它。
3. **把同一个动画加入多个组。** 一个动画同一时刻只能由一个动画组管理。
4. **把 `addPause()` 当不计数的延时。** 它是实际的 `QPauseAnimation`，占一个组位置。
5. **假设 `currentAnimation()` 永不为空。** 空组及状态边界都可能没有当前项。
6. **用 `duration()` 估算总循环耗时。** 总时长用 `totalDuration()`；`duration()` 不包含组的 loopCount。
7. **依赖每帧回调做关键业务步骤。** 更新频率与次数不受保证。
8. **从工作线程控制 UI 动画。** 动画组和目标 QObject 应留在同一对象线程。

## API 速查表

| API | 语义 | 使用时重点 |
| --- | --- | --- |
| `QSequentialAnimationGroup(parent)` | 创建顺序动画组。 | parent 管理组本身；子动画则由组管理。 |
| `~QSequentialAnimationGroup()` | 销毁组及仍被组管理的全部子动画。 | 加入后不要重复释放子动画。 |
| `addAnimation(animation)` | 从 `QAnimationGroup` 继承，在末尾加入子动画。 | 组取得所有权；顶层组统一启动。 |
| `insertAnimation(index, animation)` | 从基类继承，在指定位置插入子动画。 | 校验插入位置；不要在无协调的运行时随意重排。 |
| `removeAnimation(animation)` | 从基类继承，移除指定子动画。 | 所有权转回调用方，须自行删除或重新托管。 |
| `takeAnimation(index)` | 从基类继承，取出并移除子动画。 | 返回值由调用方负责；无效 index 不应假定有可用对象。 |
| `clear()` | 从基类继承，删除全部子动画并将当前时间重置为 0。 | 任何缓存的子动画指针都会失效。 |
| `animationCount()` / `animationAt()` / `indexOfAnimation()` | 从基类继承，用于检查组内容。 | pause 也会计入数量和索引。 |
| `addPause(msecs)` | 在末尾创建并加入 `QPauseAnimation`。 | pause 是子动画，加入后由组拥有。 |
| `insertPause(index, msecs)` | 在指定位置创建并加入暂停。 | index 应在有效插入范围内，毫秒数应符合业务预期。 |
| `currentAnimation` / `currentAnimation()` | 返回当前时间线上的活动子动画。 | 空组或边界状态可能为 `nullptr`；只读。 |
| `bindableCurrentAnimation()` | 获取 `currentAnimation` 的绑定入口。 | 适用于 Qt 属性绑定，不取代生命周期检查。 |
| `currentAnimationChanged(current)` | 当前子动画切换时发射。 | `current` 可为空；连接需提供接收 context。 |
| `duration()` | 返回一个循环内的顺序时长。 | 通常是子动画局部时长之和，不包含组循环次数。 |
| `totalDuration()` | 从 `QAbstractAnimation` 继承，返回包含 loopCount 的有效总时长。 | 包含无限时长子动画时不能当有限计时值。 |
| `start()` / `stop()` / `pause()` / `resume()` | 从基类继承，控制整个时间线。 | 依赖对象线程事件循环；只对顶层组直接 `start()`。 |
| `setCurrentTime()` | 跳转整个序列的位置。 | 会改变当前子动画；不要依赖中间帧回调次数。 |
| `setLoopCount()` / `loopCount()` | 设置或读取整个序列循环次数。 | `duration()` 不含循环，`totalDuration()` 才包含。 |
| `setDirection()` / `direction()` | 设置或读取正向、反向播放。 | 子动画需要具备合理的反向语义。 |
| `finished()` / `stateChanged()` | 从基类继承的整体完成和状态信号。 | `DeleteWhenStopped` 时避免在异步后续中使用已删除组。 |
| `event()` | 受保护的 Qt 事件分发重实现。 | 普通业务代码不直接调用或重写它。 |
| `updateCurrentTime()` | 受保护的时间推进重实现。 | 框架调用，间隔和次数不保证。 |
| `updateDirection()` | 受保护的方向传播重实现。 | 框架调用，通常无需业务层干预。 |
| `updateState()` | 受保护的状态传播重实现。 | 框架调用；自定义动画时才需要理解。 |

## 一句话总结

`QSequentialAnimationGroup` 把子动画变成可暂停、循环、反向和嵌套的顺序时间线；把所有权交给组，只从顶层启动，别把每帧更新或 `currentAnimation()` 指针当作稳定的业务状态。
