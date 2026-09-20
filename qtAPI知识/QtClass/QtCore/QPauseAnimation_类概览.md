# Qt QPauseAnimation：在动画时间线中插入不改变属性的停顿

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPauseAnimation>`  
> 所属模块：`Qt6::Core`  
> 继承链：`QObject -> QAbstractAnimation -> QPauseAnimation`  
> 类型性质：不可复制的 `QObject` 动画节点；不拥有任何动画目标

## 1. 它解决什么问题

有些界面过渡需要“先动，再停一会儿，再继续”：

```text
淡入 180 ms -> 停留 600 ms -> 淡出 180 ms
```

`QPauseAnimation` 是动画框架中的“时间占位节点”。它：

- 从开始起等待指定毫秒数；
- 不写入任何属性，不绘制任何内容；
- 到期后正常结束；
- 最常用于 `QSequentialAnimationGroup` 的两个动画之间。

它不是“冻结已经在运行的其他动画”的命令。若将一个 `QPauseAnimation` 放入 `QParallelAnimationGroup`，它只是在并行组中等待自己的时长，其他 child 仍照常运行。

## 2. 首选用法：让顺序组提供 pause

通常无需自行 `new QPauseAnimation`。`QSequentialAnimationGroup` 已提供语义更直接的便利函数：

```cpp
#include <QPropertyAnimation>
#include <QSequentialAnimationGroup>
#include <QWidget>

void NotificationController::showThenHide(QWidget *banner)
{
    auto *sequence = new QSequentialAnimationGroup(this);

    auto *fadeIn = new QPropertyAnimation(banner, "windowOpacity");
    fadeIn->setDuration(160);
    fadeIn->setStartValue(0.0);
    fadeIn->setEndValue(1.0);

    auto *fadeOut = new QPropertyAnimation(banner, "windowOpacity");
    fadeOut->setDuration(160);
    fadeOut->setStartValue(1.0);
    fadeOut->setEndValue(0.0);

    sequence->addAnimation(fadeIn);
    sequence->addPause(800);
    sequence->addAnimation(fadeOut);

    sequence->start();
}
```

`addPause(800)` 等价于创建一个 800 ms 的 `QPauseAnimation` 并加入 sequence。sequence 会接管它和其它 child 的所有权。

若要插到指定位置，使用：

```cpp
sequence->insertPause(1, 800);
```

顺序组决定 pause 什么时候开始、暂停、恢复和停止；不要单独对已经属于 sequence 的 pause 调用 `start()`。

## 3. 它实际怎样运行

### 3.1 没有视觉副作用，只有时间推进

`QPauseAnimation` 重写 `updateCurrentTime()`，但不会根据当前时间更新目标属性。它仍是一个完整的 `QAbstractAnimation`，因此有：

- `Running`、`Paused`、`Stopped` 状态；
- `currentTime`、`currentLoop`、`loopCount`；
- `finished()` 和 `stateChanged()` 信号；
- 正向和反向方向；
- `start()`、`pause()`、`resume()`、`stop()` 等控制 API。

它的效果是延后 sequence 进入下一个节点，而不是让 CPU 线程 `sleep`，更不会阻塞 Qt 事件循环。

### 3.2 必须让事件循环继续运行

动画时间由事件循环推进。下面这种写法会让 pause 和其它动画一起卡住：

```cpp
sequence->start();
doExpensiveSynchronousWork(); // 阻塞 GUI 线程，动画不会正常推进
```

如果业务只是“过 N ms 执行一次回调”，而不是动画编排的一部分，通常用 `QTimer::singleShot()` 更清楚：

```cpp
QTimer::singleShot(800, this, &NotificationController::hideBanner);
```

使用选择：

| 需求 | 优先工具 |
| --- | --- |
| 动画 A 与动画 B 之间插入停顿 | `QSequentialAnimationGroup::addPause()` |
| 仅在稍后执行槽或 lambda | `QTimer::singleShot()` |
| 阻塞当前工作线程等待 | 业务同步原语；不要用 GUI 动画或 `sleep` |

### 3.3 单独启动可以延后 `finished()`，但通常不推荐

```cpp
auto *pause = new QPauseAnimation(500, this);
connect(pause, &QAbstractAnimation::finished, this, [] {
    qDebug() << "500 ms elapsed";
});
pause->start();
```

这在技术上可行，但它把纯计时写成动画对象。没有要组合进动画时间线时，`QTimer::singleShot()` 的意图、取消和对象上下文通常更清楚。

## 4. 时长、默认值与负数边界

### 4.1 `duration` 的单位和默认值

`duration` 单位是毫秒，必须为非负数。

```cpp
auto *pause = new QPauseAnimation(600, this);
Q_ASSERT(pause->duration() == 600);

pause->setDuration(1000);
```

Qt 6.11.1 的实现将默认 duration 初始化为 **250 ms**。本机离线文档存在冲突：属性说明写默认 250 ms，但无参构造函数段落写默认 0 ms。实际使用应以实现的 250 ms 为准；更稳妥的工程习惯是始终显式传入或设置 duration，不依赖默认值：

```cpp
auto *pause = new QPauseAnimation(this);
pause->setDuration(400);
```

### 4.2 负 duration 无效

```cpp
pause->setDuration(-1);
```

负值不是“无限暂停”。Qt 会发出警告并保留原 duration；不会把它转换为 0，也不会接受 `QAbstractAnimation` 中 `-1` 所代表的未定义时长语义。

若需要等待外部事件或无限期停留，不要滥用 pause：

- 用状态机、信号或 `QEventLoop` 之外的明确业务流程等待条件；
- 或让相应的动画/页面保持状态，直到外部事件决定进入下一阶段；
- 不要让 sequence 卡在伪造的无限 duration 节点上。

### 4.3 duration 为 0

0 ms 是合法的。它不会产生可见停顿，通常很快完成：

```cpp
sequence->addPause(0);
```

它偶尔可用于按条件构建统一的 sequence，但若没有结构需求，直接不加入该节点更易读。

## 5. 所有权、父对象和删除

`QPauseAnimation` 没有 target object，也不拥有前后动画。它本身只是一个 `QObject`：

```cpp
auto *pause = new QPauseAnimation(400, this);
```

此处 `this` 管理 pause 的生命周期。

放入动画组后遵循 `QAnimationGroup` 所有权规则：

```cpp
auto *pause = new QPauseAnimation(400);
sequence->addAnimation(pause); // sequence 接管 pause
```

加入后不要再次手工 `delete pause`。需要取回时：

```cpp
QAbstractAnimation *taken = sequence->takeAnimation(index);
if (taken)
    taken->setParent(this);
```

`QSequentialAnimationGroup::addPause()` 生成的对象同样归 sequence 所有；对 sequence 执行 `clear()` 或销毁 sequence，会删除 pause。

若顶层 sequence 以 `DeleteWhenStopped` 启动，sequence 结束时 pause 和其它 child 一并销毁。finished 槽或延后 lambda 中不应继续持有这些裸指针。

## 6. 状态、循环与方向

### 6.1 pause 自身可以被暂停

名称中的 Pause 指“它提供一个时间间隔”，不是对象不能 `pause()`。作为 `QAbstractAnimation`，它可以暂停和恢复：

```cpp
pause->start();
pause->pause();  // 当前计时冻结
pause->resume(); // 从冻结位置继续
```

当 pause 位于 sequence 中，应操作顶层 sequence，由父组统一传播状态。直接控制 child 会破坏父组对时间线的管理。

### 6.2 循环规则

pause 默认 `loopCount()` 为 1。将其设置为多轮，会重复等待：

```cpp
pause->setDuration(100);
pause->setLoopCount(3); // 有效总等待约 300 ms
```

但在 sequence 中，重复纯停顿通常不如直接写一个总时长清楚：

```cpp
sequence->addPause(300);
```

仅在每一轮都需要观察 `currentLoopChanged()`，或要让 loop 规则与相邻动画保持一致时，才考虑给 pause 自身设置 loop count。

### 6.3 反向播放

QPauseAnimation 不改变属性，所以反向不会带来可见“倒放”。它仍遵守抽象动画的时间方向和状态规则，主要在嵌套 group 反向播放时保证时间线一致。

## 7. 线程边界

pause 是 `QObject`，应从其线程亲和性所在的线程使用。实际 UI 动画通常在 GUI 线程创建和控制：

- 不从工作线程直接操作 GUI sequence；
- 不要阻塞 group 所在线程；
- 若异步工作完成后要继续/启动时间线，用 queued signal 或线程安全的事件投递回拥有者线程；
- 不要只把某一个 child `moveToThread()`，而其父 group 和其它 child 仍在原线程。

Qt Core 提供该类型并不意味着它能脱离 `QObject` 和事件循环的线程规则。

## 8. 常见错误

### 8.1 用 `QPauseAnimation` 停止其它并行动画

它只等待自己。要暂停整套动画，调用顶层 group 的 `pause()`。

### 8.2 用它替代 `QTimer`

纯延迟回调优先 `QTimer::singleShot()`；pause 的语义是动画序列中的一个时间节点。

### 8.3 依赖无参构造的默认时长

Qt 6.11.1 离线参考页对默认值有冲突。显式设置毫秒数，避免版本和文档差异。

### 8.4 传负数希望无限等待

负 duration 无效，保留旧值。使用外部事件或明确状态控制。

### 8.5 加入 sequence 后单独 `start()`

子动画应由顶层 group 驱动。直接启动被管理 child 的行为不受支持，可能导致状态不同步。

### 8.6 在事件循环被阻塞时等待它完成

忙等、长计算或同步 I/O 会阻止动画计时。用 `finished()` 继续流程，不要堵住 GUI 线程。

### 8.7 忘记所有权已经转移

`addAnimation()`、`addPause()` 之后 group 拥有 pause；`clear()` 和 group 析构会删除它。

## 9. 逐项 API 说明

### 9.1 `duration` 属性

```cpp
Q_PROPERTY(int duration READ duration WRITE setDuration
           BINDABLE bindableDuration)
```

保存 pause 的时长，单位毫秒。

- 必须非负；
- Qt 6.11.1 实现默认值为 250 ms，工程代码应显式设置；
- `0` 合法且无可见等待；
- 直接 `setDuration()` 会更新值；有活动 QProperty binding 时，普通 setter 调用会解除该绑定；
- duration 改变不会给 pause 自动增加通知信号，但 `bindableDuration()` 可用于 QProperty 绑定。

### 9.2 `QPauseAnimation(QObject *parent = nullptr)`

构造 pause，并可指定 QObject 父对象。

- 不提供 animation target；
- duration 默认实现值为 250 ms；不要依赖离线构造函数页中的 0 ms 说法；
- `parent` 管理 pause 本身，加入 group 后则由 group 管理 child 所有权；
- 无参构造后通常立即 `setDuration()`。

### 9.3 `QPauseAnimation(int msecs, QObject *parent = nullptr)`

构造指定时长的 pause。

- `msecs` 单位为毫秒；
- 应传入 `>= 0` 的值；
- `parent` 只管理该 QObject，不代表将它加入 sequence；
- 最适合直接交给 `QSequentialAnimationGroup::addAnimation()`。

### 9.4 `duration() const`

```cpp
int duration() const override;
```

返回当前 pause 的单轮时长。

- 不包含 `loopCount()` 产生的重复；
- 完整运行时长用继承的 `totalDuration()` 查询；
- 返回值不应为负；
- 是 `QAbstractAnimation::duration()` 的实现。

### 9.5 `setDuration(int msecs)`

```cpp
void setDuration(int msecs);
```

修改单轮 pause 时长。

- 接受 0 和正整数；
- 负值会警告并保持当前值；
- 动画时间线运行中修改时长会改变后续的时长判断，应在 stopped 状态配置编排以避免难以预期的交互；
- 对已建立的 duration binding，直接 setter 会解除该 binding。

### 9.6 `bindableDuration()`

```cpp
QBindable<int> bindableDuration();
```

返回 duration 的 QProperty 绑定入口。

- 用于依赖属性的响应式同步；
- 若直接调用 `setDuration()`，绑定可能被解除；
- 大多数普通动画编排只需 `setDuration()`，不需要引入绑定。

### 9.7 `event(QEvent *e)`

```cpp
bool event(QEvent *e) override;
```

受保护的 QObject 事件处理重写。

- Qt 内部用它维护动画对象行为；
- 普通代码不应直接调用；
- 自定义派生类极少需要覆盖，覆盖时应保留基类事件语义。

### 9.8 `updateCurrentTime(int)`

```cpp
void updateCurrentTime(int) override;
```

受保护的时间更新回调。

- pause 的实现不根据时间写入目标属性；
- 不由应用代码手工调用；
- 用 `setCurrentTime()`、`start()` 和 group 时间线驱动它；
- 自定义派生类若需要可见进度，应考虑自定义动画，而不是改变 pause 的语义。

### 9.9 继承的关键 `QAbstractAnimation` API

| API | 作用 | 在 pause 中的含义 |
| --- | --- | --- |
| `start(policy)` | 开始计时 | 顶层 pause 可独立计时；group child 由父组启动 |
| `pause()` / `resume()` | 冻结/继续 current time | 暂停的是 pause 自己的计时 |
| `stop()` | 停止动画 | 不代表自然等待结束 |
| `setCurrentTime(msecs)` | 跳转计时位置 | 不产生视觉更新，只改变进度 |
| `setLoopCount(count)` | 设置重复次数 | 一般不如直接设置总 pause 时长清晰 |
| `state()` / `currentTime()` | 读取状态和已过时间 | 适合调试/测试 |
| `finished()` | 自然到达末尾后发出 | 用于继续异步流程；不应阻塞等待 |

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 顺序组 | `QSequentialAnimationGroup::addPause(msecs)` | 创建并加入 pause | 首选方式；sequence 接管所有权 |
| 顺序组 | `insertPause(index, msecs)` | 在指定节点前插入 pause | 适合动态编排 |
| 构造 | `QPauseAnimation(msecs, parent)` | 创建指定时长 pause | 单位毫秒；优先显式时长 |
| 属性 | `duration` / `duration()` | 读取单轮等待时长 | Qt 6.11.1 实现默认 250 ms；负值无效 |
| 设置 | `setDuration(msecs)` | 修改等待时长 | 负值保留旧值并警告；可能解除 binding |
| 绑定 | `bindableDuration()` | 获取 QProperty 绑定入口 | 普通编排通常不用 |
| 状态 | `start()` / `pause()` / `resume()` / `stop()` | 控制计时 | group child 由顶层 group 控制 |
| 进度 | `setCurrentTime()` / `currentTime()` | 跳转或读取计时进度 | 不产生视觉属性变化 |
| 循环 | `setLoopCount()` / `totalDuration()` | 重复 pause、读取总时长 | 避免无意义地与总时长叠加 |
| 生命周期 | `parent` / group 所有权 | 管理 pause 对象 | 加入 group 后不要手工 delete |
| 扩展 | `event()` / `updateCurrentTime()` | 内部 protected 钩子 | 普通代码不要调用 |
| 替代 | `QTimer::singleShot()` | 仅做延迟回调 | 不属于动画编排时更合适 |

## 11. 一句话总结

`QPauseAnimation` 是不会改动任何属性的动画时间节点：把它放在 `QSequentialAnimationGroup` 中就能让前后动画之间保留指定节拍；显式设置非负时长、交给顶层 group 管理，并在单纯延迟回调时改用 `QTimer`，是最稳妥的使用方式。
