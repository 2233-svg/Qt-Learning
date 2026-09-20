# QAnimationGroup 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAnimationGroup>`  
> 模块：`Qt6::Core`  
> 继承：`QObject -> QAbstractAnimation -> QAnimationGroup`  
> 直接派生类：`QParallelAnimationGroup`、`QSequentialAnimationGroup`

## 它解决什么问题

真实界面中的动画往往不是一个属性从 A 变到 B 这么简单：一个面板进入时可能同时移动、改变透明度、缩放；一整段引导流程又可能要先淡入、停顿、再滑出。若每个动画都单独 `start()`、单独暂停和清理，状态很快失控。

`QAnimationGroup` 是一组 `QAbstractAnimation` 的抽象容器基类。它统一管理子动画的开始、暂停、恢复和停止，并允许多个动画组继续嵌套，构成动画树：

```text
QAbstractAnimation
  └─ QAnimationGroup
       ├─ QParallelAnimationGroup    同时推进所有子动画
       └─ QSequentialAnimationGroup  按顺序推进子动画
```

它本身仍是抽象类。日常代码不要直接创建 `QAnimationGroup`，而是选择：

- `QParallelAnimationGroup`：多个效果同时发生，例如窗口移动和淡入同步完成。
- `QSequentialAnimationGroup`：多个效果依次发生，例如“展开 -> 等待 -> 收起”。

`QAnimationGroup` 解决的是动画的**编排、统一控制和子动画所有权**问题；属性插值本身通常仍由 `QPropertyAnimation`，数值插值由 `QVariantAnimation` 完成。

## 最小可用代码：并行动画组

下面让一个控件同时移动并变得不透明。两个子动画的裸指针一旦传给 `addAnimation()`，就由组负责销毁。

```cpp
#include <QParallelAnimationGroup>
#include <QPropertyAnimation>
#include <QWidget>

void playEnterAnimation(QWidget *panel)
{
    auto *group = new QParallelAnimationGroup(panel);

    auto *move = new QPropertyAnimation(panel, "pos");
    move->setDuration(240);
    move->setStartValue(panel->pos() + QPoint(0, 24));
    move->setEndValue(panel->pos());

    auto *fade = new QPropertyAnimation(panel, "windowOpacity");
    fade->setDuration(240);
    fade->setStartValue(0.0);
    fade->setEndValue(1.0);

    group->addAnimation(move);
    group->addAnimation(fade);
    group->start(QAbstractAnimation::DeleteWhenStopped);
}
```

这里的 `group` 是顶层动画组，直接调用 `start()` 是正确的。`DeleteWhenStopped` 让组完成后删除自己；析构组时也会删除仍在其中的子动画。采用这个策略后，外部不要再保存并使用 `group`、`move` 或 `fade` 的裸指针。

实际项目中常把组作为窗口或控制器的成员，以便反复播放、暂停或取消；那种情况下通常使用默认的 `KeepWhenStopped`，并明确由 QObject 父子关系或成员对象负责组的生命周期。

## 动画树：只有顶层组负责启动

由于 `QAnimationGroup` 继承 `QAbstractAnimation`，组可以放入另一个组：

```cpp
auto *parallel = new QParallelAnimationGroup;
parallel->addAnimation(new QPropertyAnimation(target, "pos"));
parallel->addAnimation(new QPropertyAnimation(target, "size"));

auto *sequence = new QSequentialAnimationGroup(parent);
sequence->addAnimation(parallel);
sequence->addAnimation(new QPauseAnimation(150));
sequence->start();
```

此时 `parallel` 是 `sequence` 的子动画。应当启动 `sequence`，而不是再直接调用 `parallel->start()`。Qt 明确把“直接启动已包含在另一个组中的子组”视为不受支持的用法，容易得到意外状态。

子动画可通过继承自 `QAbstractAnimation` 的 `group()` 查询直接所属组：

```cpp
QAnimationGroup *owner = animation->group(); // 不属于任何组时为 nullptr
```

这个返回值适合调试动画树和避免重复加入，但不要据此绕过组的控制逻辑。

## 最关键的规则：谁拥有子动画

`QAnimationGroup` 对它管理的子动画采用明确的所有权规则：

- `addAnimation(animation)`：追加到末尾，动画组取得并负责销毁该动画。
- `insertAnimation(index, animation)`：插入到指定位置，动画组取得并负责销毁该动画。
- `clear()`：移除全部动画，并立即删除全部子动画。
- 析构动画组：销毁尚在组内的全部子动画。
- `removeAnimation(animation)`：从组中移除，所有权转回调用者。
- `takeAnimation(index)`：取出并从组中移除，所有权转回调用者。

因此，以下两种代码的后半段含义完全不同：

```cpp
group->removeAnimation(animation);
delete animation; // remove 后调用者已经拿回所有权
```

```cpp
QAbstractAnimation *animation = group->takeAnimation(0);
if (animation)
    animation->deleteLater(); // take 后也需要调用者安排销毁
```

反过来，动画一旦已经交给组，就不要再用 `std::unique_ptr`、栈对象或另一套手动 `delete` 同时管理它，否则会造成重复释放。`QObject` 的 parent 关系也不能替代这一约定：把一个动画交给组后，生命周期应以组的 API 契约为准。

## 添加、查询和调整顺序

### `addAnimation()`：追加

```cpp
group->addAnimation(animation);
```

它等价于：

```cpp
group->insertAnimation(group->animationCount(), animation);
```

适合构建时按自然顺序把动画放进组。组取得所有权。

### `insertAnimation()`：在指定位置插入

```cpp
group->insertAnimation(0, animation); // 成为第一个子动画
```

索引 `0` 插到开头，索引等于 `animationCount()` 插到末尾。对顺序组而言，索引会直接改变播放先后；对并行组而言，它通常不改变“同时播放”的语义，但仍会影响枚举、调试和组内结构。

### 查询：`animationCount()`、`animationAt()`、`indexOfAnimation()`

```cpp
for (int i = 0; i < group->animationCount(); ++i) {
    QAbstractAnimation *animation = group->animationAt(i);
    // 这里只是借用指针；不要 delete。
}
```

`animationAt(i)` 的有效区间是 `0` 到 `animationCount() - 1`。遍历时必须以 `animationCount()` 为边界，不要凭记忆写死索引。`indexOfAnimation(animation)` 返回该动画的索引，常用于先查询位置，再传给 `takeAnimation()`；动画不在组中时应把返回值当作“未找到”处理，而不是直接用于按索引访问。

## 清空、移除、取出：语义不能混

### `clear()`：彻底清空并删除

```cpp
group->clear();
```

它会移除并删除所有子动画，同时把组的 `currentTime` 重置为 `0`。适合关闭页面、重建整套动画流程或需要释放所有旧动画的场景。调用后，之前保存的子动画指针全部失效。

### `removeAnimation()`：按指针摘下，所有权交回调用者

```cpp
group->removeAnimation(animation);
animation->setParent(controller);
```

当你已持有某个动画指针，想把它改放到其他组或保留下来复用时使用。移除后组不再删它，调用者必须立刻让新的所有者接管，或在合适时机销毁。

### `takeAnimation()`：按索引摘下并返回

```cpp
QAbstractAnimation *animation = group->takeAnimation(index);
if (!animation)
    return;

otherGroup->addAnimation(animation); // 所有权转给 otherGroup
```

它适合按位置重排、在两个组之间移动或取出未知的第 N 个动画。返回指针后，组不再拥有对象；把它加入另一个组会再次转移所有权。

## 状态控制由组向下传播

动画组通常负责决定子动画何时 `start()`、`stop()`、`pause()` 和 `resume()`。你通过从 `QAbstractAnimation` 继承来的 API 控制顶层组，具体派生组再按自己的策略分发时间：

- 并行组：多个子动画在同一时间轴上推进，整体时长由最长的子动画决定。
- 顺序组：当前子动画结束后再切换到下一个，整体时长通常是各子动画时长之和。

不要一边让组运行，一边对其某个子动画独立执行 `start()` 或 `stop()` 来“手动纠正”状态；这会让组内部状态和子动画状态脱节。需要改动流程时，先停止顶层组，再调整其成员，最后重新启动。

动画依赖所在线程的事件循环推进。`start()` 只会使顶层组进入运行状态；若线程没有运行事件循环，时间不会持续流动。

## 观察组成员变化

子动画是 `QObject`。组内增加或移除子动画时，可以在自定义派生类或事件过滤逻辑中关注 `QEvent::ChildAdded` 和 `QEvent::ChildRemoved`，用于维护调试面板、日志或额外的业务映射。

`QAnimationGroup::event(QEvent *)` 是保护重写函数，Qt 用它处理对象子节点等框架事件。普通应用无需调用或重写它。确实需要派生动画组时，重写后应让不由自己完全处理的事件继续交给基类，避免破坏 QObject 的父子对象管理。

## 常见误区

- 直接实例化 `QAnimationGroup`。它从 `QAbstractAnimation` 继承抽象契约，应创建并行组或顺序组。
- 直接启动嵌套在另一个组里的子组。只启动最外层动画组。
- `addAnimation()` 后继续手动 `delete` 子动画。加入和插入都会把所有权交给组。
- 以为 `removeAnimation()` 会删除动画。它恰恰会把所有权交还调用者。
- 以为 `clear()` 只是从列表移除。它会删除所有子动画并重置组时间。
- 用 `animationAt()` 返回的指针做长期所有权保存。它只是组内部对象的借用指针，组 `clear()` 或析构后立即失效。
- 对运行中的组动态大幅增删子动画，却没有确认当前播放状态。复杂修改应先停止顶层组，完成重组后再播放。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QAnimationGroup(QObject *parent = nullptr)` | 构造动画组基类并设置 QObject 父对象。 | 本类仍是抽象类，实际应构造 `QParallelAnimationGroup` 或 `QSequentialAnimationGroup`。 |
| 析构 | `~QAnimationGroup()` | 销毁动画组及其尚在组内的全部子动画。 | 组拥有由 `addAnimation()` 或 `insertAnimation()` 加入的动画；外部保存的借用指针会失效。 |
| 添加 | `addAnimation(QAbstractAnimation *animation)` | 将动画追加到组末尾。 | 等价于在 `animationCount()` 位置插入；调用后组取得 `animation` 的所有权。 |
| 查询 | `animationAt(int index) const` | 返回指定位置的子动画指针。 | 有效索引是 `0` 到 `animationCount() - 1`；返回的是借用指针，不要删除。 |
| 查询 | `animationCount() const` | 返回当前由组管理的子动画数量。 | 遍历或传索引前先用它检查边界。 |
| 清空 | `clear()` | 移除并删除全部子动画，并将当前时间重置为 `0`。 | 调用后所有原子动画的指针都可能悬挂；不能把它当成只移除不删除。 |
| 查询 | `indexOfAnimation(QAbstractAnimation *animation) const` | 返回指定动画在组内的位置。 | 未找到时不要把返回值直接传给 `animationAt()` 或 `takeAnimation()`。 |
| 插入 | `insertAnimation(int index, QAbstractAnimation *animation)` | 在指定位置加入子动画。 | `0` 是开头，`animationCount()` 是末尾；组取得动画所有权。 |
| 移除 | `removeAnimation(QAbstractAnimation *animation)` | 将指定动画从组中移除。 | 所有权转给调用者；应尽快交给其他组、父对象或显式销毁。 |
| 取出 | `takeAnimation(int index)` | 取出指定位置的动画并将其从组中移除。 | 所有权转给调用者；适合转移到另一组或重排。 |
| 保护函数 | `event(QEvent *event)` | 处理组作为 QObject 收到的框架事件。 | 一般不直接调用或重写；派生时保留基类事件处理，特别是子对象事件。 |
| 继承控制 | `start(DeletionPolicy policy = KeepWhenStopped)` | 启动顶层动画组。 | 仅对不属于其他组的顶层组直接调用；`DeleteWhenStopped` 后不要再访问组或其子动画。 |
| 继承控制 | `pause()`、`resume()`、`stop()` | 暂停、恢复或停止顶层组，从而由组协调子动画状态。 | 不要通过单独启动或停止运行中组的子动画来对抗组的状态管理。 |
| 继承查询 | `group() const` | 从任意子动画查询其直接所属动画组。 | 返回 `nullptr` 表示该动画没有被组管理；可用于检查动画树，不用于接管所有权。 |

## 一句话总结

`QAnimationGroup` 是动画树的容器和指挥者：顶层组负责启动，组负责子动画状态与销毁；要保留子动画用 `removeAnimation()` 或 `takeAnimation()` 先把所有权拿回来，真正要删除整组则用 `clear()`。
