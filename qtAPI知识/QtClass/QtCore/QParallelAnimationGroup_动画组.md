# Qt QParallelAnimationGroup：让多条动画以同一时间轴并行运行

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QParallelAnimationGroup>`  
> 所属模块：`Qt6::Core`  
> 继承链：`QObject -> QAbstractAnimation -> QAnimationGroup -> QParallelAnimationGroup`  
> 类型性质：不可复制的 `QObject` 容器；拥有加入其中的子动画

## 1. 它解决什么问题

界面过渡经常由多条动画同时组成：窗口淡入、位置移动、尺寸变化和背景色变化应在同一段时间内发生。若分别启动每个 `QPropertyAnimation`，就需要手工处理它们的暂停、停止、完成时机和所有权。

`QParallelAnimationGroup` 将多个 `QAbstractAnimation` 放在一条共享时间轴上：

```text
group start
  0 ms  -> child A、child B、child C 一起开始
  ...   -> 每个 child 按自己的时长、缓动曲线和循环规则推进
  end   -> 最长的有效 child 结束，group 才结束
```

它是动画容器，不是属性动画本身。通常与下列类型组合：

- `QPropertyAnimation`：动画化 `QObject` 属性；
- `QVariantAnimation`：得到插值值后自行应用；
- `QPauseAnimation`：在并行时间轴中提供固定时长的占位；
- 另一 `QParallelAnimationGroup` 或 `QSequentialAnimationGroup`：构建更复杂的动画图。

## 2. 最小可用模式

以下示例假定 `panel` 是仍然存活的 `QWidget *`，代码位于一个 `QObject` 派生控制器中：

```cpp
#include <QParallelAnimationGroup>
#include <QPropertyAnimation>
#include <QWidget>

void PanelController::showPanel(QWidget *panel)
{
    auto *group = new QParallelAnimationGroup(this);

    auto *fade = new QPropertyAnimation(panel, "windowOpacity");
    fade->setDuration(180);
    fade->setStartValue(0.0);
    fade->setEndValue(1.0);

    auto *move = new QPropertyAnimation(panel, "pos");
    move->setDuration(260);
    move->setStartValue(panel->pos() + QPoint(0, 12));
    move->setEndValue(panel->pos());
    move->setEasingCurve(QEasingCurve::OutCubic);

    group->addAnimation(fade);
    group->addAnimation(move);

    connect(group, &QAbstractAnimation::finished,
            this, &PanelController::panelShown);

    group->start();
}
```

关键点：

- `group` 由控制器这个 `QObject` 父对象管理；
- `addAnimation()` 后，group 接管 `fade` 和 `move` 的所有权；
- 两条动画在 group 启动时一起开始；
- group 在 260 ms 的移动动画结束后才完成，180 ms 的淡入会先停在终值；
- group 不拥有 `panel`，目标控件必须在动画期间保持有效。

## 3. 时间模型：并行不等于时长相同

### 3.1 子动画共享 group 的当前时间

并行组把自身的时间推进映射给每个子动画。子动画可以有不同的局部时长：

```text
group current time: 0 ------- 180 ----------- 260 ms
fade:               [========= finished =====]
move:               [=========================]
group:              [=========================] -> finished
```

短动画完成后会停在其终点，较长动画继续；组不会因为第一个子动画结束而结束。

### 3.2 `duration()` 是最长子动画的有效时长

`QParallelAnimationGroup::duration()` 返回子动画中最长的有效时长。对子动画而言，循环会影响其有效总运行时间，因此实际设计时应把 child 的 `duration()`、`loopCount()` 和 `totalDuration()` 一起考虑。

```cpp
auto *pulse = new QPropertyAnimation(button, "windowOpacity");
pulse->setDuration(200);
pulse->setLoopCount(3); // 有效运行时间为 600 ms

auto *move = new QPropertyAnimation(button, "pos");
move->setDuration(400);

group->addAnimation(pulse);
group->addAnimation(move);

// group 的本轮时长由 pulse 的有效时长主导。
```

如果任一子动画的 duration 为 `-1`，它没有可预测的结束时间；并行组也就不应期待按有限时长自然结束。此时应由业务代码显式 `stop()`，或先移除/停止该无限动画。

空 group 的时长为 0，启动后会很快完成；这通常说明子动画还没有正确加入。

### 3.3 group 自身也可以循环

并行组本身继承 `QAbstractAnimation::setLoopCount()`。group 的一轮是“所有子动画共享时间轴从本轮起点推进到本轮终点”；group 设置多轮时，整组按该轮重复。

不要同时随意给 group 和所有 child 都设置循环次数，否则总时长和视觉节奏很难推断。常见的两种清晰建模方式是：

- 子动画自己循环，group 只运行一轮；
- 子动画各运行一轮，group 负责整套过渡的循环。

## 4. 所有权、层级与删除策略

### 4.1 加入即转移所有权

`QAnimationGroup::addAnimation()` 和 `insertAnimation()` 都会让 group 取得 child 的所有权：

```cpp
auto *group = new QParallelAnimationGroup(this);
auto *animation = new QPropertyAnimation(target, "opacity");

group->addAnimation(animation);
// 此后不要再手工 delete animation。
```

group 析构时会析构所有仍在组内的动画。`QParallelAnimationGroup` 本身被其 `QObject` 父对象删除时，效果相同。

### 4.2 移除后由调用方负责

```cpp
QAbstractAnimation *animation = group->takeAnimation(0);
if (animation) {
    // 现在 group 不再拥有它。
    animation->setParent(this);
}
```

`removeAnimation(animation)` 也会将所有权转回调用方，只是没有返回指针。`clear()` 则不同：它会移除并**删除**所有 child，且将 group 的当前时间重置为 0。

| 操作 | child 是否仍在组中 | child 后续所有者 |
| --- | --- | --- |
| `addAnimation()` / `insertAnimation()` | 是 | group |
| `removeAnimation()` | 否 | 调用方 |
| `takeAnimation()` | 否 | 调用方 |
| `clear()` | 否 | 已删除 |
| group 析构 | 否 | 已删除 |

不要在 `clear()` 或 group 析构后继续使用之前保存的 child 裸指针。

### 4.3 `DeleteWhenStopped` 删除的是 group

顶层组可以这样启动：

```cpp
group->start(QAbstractAnimation::DeleteWhenStopped);
```

group 停止后会自动删除自身，因而也会删除所有仍属于它的子动画。这适合一次性过渡，但要注意：

- `finished` 槽内不要把 group 指针保存到后续异步任务；
- 不要让其他代码持有未保护的 group/child 裸指针；
- 若需要观察对象是否仍在，使用 `QPointer<QParallelAnimationGroup>`；
- 对已有 `QObject` 父对象的 group，通常保留默认 `KeepWhenStopped` 更容易管理生命周期。

## 5. 启动、暂停、停止与方向

`QParallelAnimationGroup` 可像普通 `QAbstractAnimation` 一样控制，但只有**顶层 group** 应直接启动。直接 `start()` 已经属于另一个 group 的子组不受支持，可能出现不可预期行为。

```cpp
group->start();                  // 从本轮起点启动，重置 currentTime
group->pause();                  // 暂停所有受 group 管理的进度
group->resume();                 // 从暂停位置继续
group->stop();                   // 停止，保留当前时间
group->setCurrentTime(120);      // 跳到 group 时间轴 120 ms
group->setDirection(QAbstractAnimation::Backward);
```

状态机来自 `QAbstractAnimation`：

```text
Stopped -- start() --> Running
Running -- pause() --> Paused
Paused  -- resume() -> Running
Running/Paused -- stop() --> Stopped
```

- `start()` 总会重置 group 的 current time；
- `pause()` 保留当前位置，`resume()` 从该位置继续；
- `stop()` 后不能 `resume()`；想重新运行应 `start()`；
- 正常到达最后一轮时进入 `Stopped` 并发出 `finished()`；
- `direction` 为 `Backward` 时，时间从当前轮终点向 0 方向推进，并由 group 同步给子动画。

`setCurrentTime()` 很适合预览、拖动进度或测试，但它会立即驱动 child 到对应位置。若某些 property 有其他绑定或业务代码同时修改，最终视觉值取决于最后一次写入，容易产生跳变。

## 6. 线程与事件循环边界

动画由 Qt 事件循环推进。阻塞 group 所在线程会让时间更新、属性写入和绘制一起停住。

常见 GUI 动画应遵守：

- 在目标 UI 对象所属线程创建和控制 group 及其 child，通常就是 GUI 线程；
- 不要从工作线程直接 `start()`、`stop()` 或修改 GUI 目标的属性；
- 重计算、网络和磁盘 I/O 放到工作线程，完成后仅把短小的 UI 动画操作投递回 GUI 线程；
- group 和 child 都是 `QObject`，不要跨线程随意移动其中一个，而让其余对象仍留在原线程。

`QParallelAnimationGroup` 所在模块是 Qt Core，并不表示它可无视 GUI 对象的线程规则；动画目标决定实际的线程约束。

## 7. 组合模式

### 7.1 在顺序组中作为一个阶段

```cpp
auto *parallel = new QParallelAnimationGroup;
parallel->addAnimation(makeFadeIn(panel));
parallel->addAnimation(makeMoveIn(panel));

auto *sequence = new QSequentialAnimationGroup(this);
sequence->addAnimation(parallel);              // sequence 接管 parallel
sequence->addPause(500);
sequence->addAnimation(makeFadeOut(panel));

sequence->start();
```

这里不能再单独启动 `parallel`。它已经是 `sequence` 的 child，由 sequence 决定何时启动、暂停和停止。

### 7.2 动画完成后再做业务动作

```cpp
connect(group, &QAbstractAnimation::finished, this, [this] {
    commitNavigation();
});
```

`finished()` 只在动画到达末尾并停止后发出。手工在中途 `stop()` 不是“成功完成”的同义词；若业务需要区分取消与自然结束，应自己保存状态或使用单独的完成条件。

### 7.3 可复用的一次性 factory

```cpp
QParallelAnimationGroup *makeShowAnimation(QWidget *target, QObject *owner)
{
    auto *group = new QParallelAnimationGroup(owner);

    auto *opacity = new QPropertyAnimation(target, "windowOpacity");
    opacity->setDuration(150);
    opacity->setStartValue(0.0);
    opacity->setEndValue(1.0);

    auto *position = new QPropertyAnimation(target, "pos");
    position->setDuration(220);
    position->setEndValue(target->pos());

    group->addAnimation(opacity);
    group->addAnimation(position);
    return group;
}
```

factory 返回的是 group 的非空所有权指针；`owner` 不为空时最终由 QObject 父子关系回收。若调用方改为 `start(DeleteWhenStopped)`，就不应在动画结束后再访问返回的指针。

## 8. 常见错误

### 8.1 将 child 同时交给两个 group

动画实例只能有一个所属 group。不要把同一个 `QPropertyAnimation *` 当作可共享轨道加入多个组；为每个编排创建独立 child，或用 `takeAnimation()` 明确转移。

### 8.2 自己删除已经加入的 child

group 已拥有 child。手工 `delete` 容易留下悬空指针和中途被破坏的时间线。想单独管理时先 `removeAnimation()` 或 `takeAnimation()`。

### 8.3 认为最短 child 结束时 group 会结束

并行组等最长有效 child。需要“任一动画结束就继续”时，不是并行组的默认语义，应连接相应 child 信号并显式决定后续动作。

### 8.4 在已有父组的子组上调用 `start()`

嵌套动画应由最外层 group 驱动。直接启动 child group 会绕开父组的状态调度。

### 8.5 忽略无限 duration 的 child

一个 duration 为 `-1` 的 child 可以让整个编排不自然结束。需要停止条件时自己调用 `stop()`，并避免等待其 `finished()`。

### 8.6 使用 `DeleteWhenStopped` 后仍访问指针

自动删除会同时释放 group 和其 child。finished 槽、定时器回调和 lambda 捕获中都应避免延后解引用。

### 8.7 动画期间销毁目标对象

group 只拥有动画，不拥有 `QPropertyAnimation` 的 target object。目标 UI 生命周期应覆盖动画，销毁页面前先停止/销毁其相关动画，或让二者受同一个上层 `QObject` 管理。

### 8.8 阻塞 GUI 线程等待动画

不要用忙等、长循环或同步 I/O “等待动画跑完”。事件循环被阻塞时，动画本身不会推进；连接 `finished()` 继续流程。

## 9. 逐项 API 说明

### 9.1 `QParallelAnimationGroup(QObject *parent = nullptr)`

构造空并行组；`parent` 是 QObject 父对象，不是动画 child。

- 初始没有动画，`animationCount()` 为 0；
- group 自身的 QObject 生命周期可由 `parent` 管理；
- child 在稍后通过 `addAnimation()` / `insertAnimation()` 加入；
- 类不可复制。

### 9.2 `~QParallelAnimationGroup()`

析构 group 并销毁其仍拥有的全部子动画。

- 运行中析构会终止相关动画对象；
- `takeAnimation()` 或 `removeAnimation()` 过的 child 不在析构范围内；
- 任何保存的 child 裸指针都随之失效。

### 9.3 `duration() const`

```cpp
int duration() const override;
```

返回当前 child 集合中最长的有效时长。

- 是本轮局部 duration，不是 group 额外 loop 后的总时长；
- 用 `totalDuration()` 读取包含 group `loopCount()` 的有效总时长；
- 子动画集合、其 duration 或 loopCount 改变后，结果也会改变；
- 存在未定义 duration 的 child 时，不要把 group 当作必然自然结束的有限动画。

### 9.4 `event(QEvent *event)`

```cpp
bool event(QEvent *event) override;
```

受保护的 QObject 事件处理重写。Qt 用它处理 child 加入、移除等内部容器同步。

- 普通使用者不应直接调用；
- 子类重写时应理解并保留基类事件处理语义；
- 若只是观察 child 结构变化，可关注 `QEvent::ChildAdded` / `QEvent::ChildRemoved`，不必派生重写。

### 9.5 `updateCurrentTime(int currentTime)`

```cpp
void updateCurrentTime(int currentTime) override;
```

受保护回调。Qt 时间驱动更新 group current time 时，用它把进度同步到子动画。

- 不由应用代码手工调用；
- 用公开的 `setCurrentTime()` 进行跳转；
- 子类覆盖时必须维护所有 child 的时间映射，否则暂停、反向播放、循环和完成时机都会失真。

### 9.6 `updateState(State newState, State oldState)`

```cpp
void updateState(QAbstractAnimation::State newState,
                 QAbstractAnimation::State oldState) override;
```

受保护回调。Qt 状态机变化时，用它同步 child 的 start/pause/resume/stop 行为。

- 普通代码使用 `start()`、`pause()`、`resume()`、`stop()`；
- 不手工调用；
- 自定义派生类通常应先理解基类状态传播，避免 child 状态与 group 状态脱节。

### 9.7 `updateDirection(Direction direction)`

```cpp
void updateDirection(QAbstractAnimation::Direction direction) override;
```

受保护回调。group 方向变化时用于同步子动画方向。

- 对外使用 `setDirection(Forward)` 或 `setDirection(Backward)`；
- 反向播放依赖 child 支持相应时间方向；
- 不要直接调用回调来伪造状态变化。

### 9.8 从 `QAnimationGroup` 继承的容器 API

| API | 语义 | 所有权/边界 |
| --- | --- | --- |
| `addAnimation(animation)` | 在末尾加入 child | group 接管 child |
| `insertAnimation(index, animation)` | 在指定位置加入 child | group 接管 child；并行组中索引不决定播放先后 |
| `animationAt(index)` | 返回指定 child 的非拥有指针 | 有效索引为 `0..animationCount()-1` |
| `animationCount()` | 返回 child 数量 | 空组为 0 |
| `indexOfAnimation(animation)` | 查询 child 索引 | 不在组内通常返回 `-1` |
| `removeAnimation(animation)` | 移除指定 child | 所有权转回调用方 |
| `takeAnimation(index)` | 移除并返回指定 child | 所有权转回调用方；需检查空指针 |
| `clear()` | 删除全部 child 并把 current time 置 0 | 保存的 child 指针全部失效 |

### 9.9 从 `QAbstractAnimation` 继承的运行 API

| API | 语义 | 重点 |
| --- | --- | --- |
| `start(policy)` | 从本轮起点开始运行 | 仅启动顶层组；可选自动删除策略 |
| `pause()` / `resume()` / `setPaused()` | 暂停或恢复 | pause 保留当前时间；stop 后不能 resume |
| `stop()` | 停止 group | 不等于自然完成；不应据此触发成功业务逻辑 |
| `setCurrentTime(msecs)` | 跳转进度 | 立刻同步 child 和目标属性 |
| `setDirection(direction)` | 切换正向/反向 | group 同步方向给 child |
| `setLoopCount(count)` | 设置 group 循环次数 | `0` 不运行，`-1` 无限循环；与 child 循环叠加时要审查总时长 |
| `state()` / `currentTime()` / `currentLoop()` | 读取运行状态和进度 | 用于观察，不替代 `finished()` |
| `duration()` / `totalDuration()` | 本轮时长 / 含 loop 的总时长 | `-1` 表示未定义时长 |
| `finished()` | 正常到达最终结尾后发出 | 适合串联后续业务 |
| `stateChanged()` / `directionChanged()` / `currentLoopChanged()` | 观察状态变化 | 不要在槽中破坏组的所有权结构 |

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QParallelAnimationGroup(parent)` | 创建空并行动画容器 | `parent` 管理 group，不等于 child |
| 子动画 | `addAnimation()` / `insertAnimation()` | 加入并行播放的 child | group 取得所有权 |
| 子动画 | `removeAnimation()` / `takeAnimation()` | 从 group 取走 child | 调用方重新负责删除或设置父对象 |
| 子动画 | `clear()` | 删除所有 child | 同时重置 current time，旧指针失效 |
| 查询 | `animationAt()` / `animationCount()` / `indexOfAnimation()` | 浏览 child 列表 | 返回的 child 指针非拥有 |
| 时长 | `duration()` | 返回最长 child 的有效时长 | 无限 child 会破坏有限完成预期 |
| 控制 | `start()` | 同时启动所有 child | 只启动顶层 group |
| 控制 | `pause()` / `resume()` / `stop()` | 统一控制 child 时间线 | stop 不等于 finished |
| 时间 | `setCurrentTime()` | 跳转所有 child 的共同时间轴 | 会立即写入目标属性 |
| 循环 | `setLoopCount()` / `totalDuration()` | 重复整组、查看总时长 | 别与 child loopCount 混乱叠加 |
| 方向 | `setDirection()` | 正向或反向驱动整组 | group 会同步方向给 child |
| 生命周期 | `start(DeleteWhenStopped)` | 停止后自动删除 group | child 也随 group 删除，避免悬空指针 |
| 通知 | `finished()` | group 自然完成后发出 | 用信号继续流程，别阻塞事件循环 |
| 扩展 | `event()` / `updateCurrentTime()` / `updateState()` / `updateDirection()` | Qt 内部的 protected 同步钩子 | 普通代码不要直接调用 |

## 11. 一句话总结

`QParallelAnimationGroup` 将多个 `QAbstractAnimation` 作为自己拥有的 child 放到同一时间轴：顶层启动时全部并行运行，短动画先停在终点，最长有效动画决定 group 的完成时刻；正确使用的关键是明确所有权、只启动顶层组，并让事件循环和目标对象生命周期覆盖整个动画过程。
