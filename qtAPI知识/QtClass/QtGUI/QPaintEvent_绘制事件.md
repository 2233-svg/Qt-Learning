# QPaintEvent：一次控件重绘实际需要更新的区域

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPaintEvent>`  
> 模块：`Qt6::Gui`；通常由 `Qt6::Widgets` 中的 `QWidget::paintEvent()` 接收

`QPaintEvent` 是 Qt 发送给需要重绘的 widget 的事件参数。它说明“这次哪些区域失效并需要更新”，而不是让应用程序随意在任何时机启动绘制。覆盖在控件上的窗口移开、控件显示、大小变化、调用 `update()` 等都可能最终合并成一次 `QPaintEvent`。

这个对象由 Qt 的事件分发系统创建并在 `paintEvent()` 调用期间借给处理函数使用。不要保存事件指针、手工删除它，或把它当作可跨线程传递的绘图命令。

## 正确的使用位置

```cpp
void WaveformWidget::paintEvent(QPaintEvent *event)
{
    QPainter painter(this);

    // 复杂内容可先按这次失效区域做粗略过滤。
    const QRect dirtyBounds = event->rect();
    drawGrid(painter, dirtyBounds);

    // 若数据分块与非矩形失效区紧密对应，再使用精确区域。
    for (const QRect &tile : event->region())
        drawWaveformTile(painter, tile);
}
```

`QPainter(this)` 只能在 `paintEvent()` 或其调用链中使用。外部状态改变时，更新数据并调用 `update()`；Qt 会合并更新请求、选择合适时机并投递 `QPaintEvent`。`repaint()` 会尝试立刻同步重绘，可能破坏事件合并和响应性，应仅在确有同步需求时使用。

## `region()` 与 `rect()`：精度和成本的取舍

`region()` 返回实际要刷新的 `QRegion`，它可以由多个互不相连的矩形组成。`rect()` 是该区域的包围矩形。两者同时存在是为了让绘制代码按复杂度选择：

- 只需一次背景填充、路径绘制或大多数普通控件时，直接使用 `rect()`；它通常比每次从区域计算包围盒更快。
- 内容按块缓存、绘制开销很高且失效区很稀疏时，遍历 `region()` 可避免重绘中间没有失效的部分。
- 不要把 `rect()` 当成精确失效形状。它可能包括两个分离失效块之间本不必重绘的区域。

Qt 的绘制系统在处理 `QPaintEvent` 时已经将绘制设备裁剪到 `region()`。这层裁剪独立于你对 `QPainter` 再调用的 `setClipRect()`、`setClipRegion()` 或 `setClipPath()`；添加自己的裁剪只会进一步收窄输出，不能扩大本次允许绘制的区域。

## 事件合并与性能

`update(rect)` 不是立刻调用 `paintEvent()`。多个更新请求常被合并为更少的事件，因此应让 `paintEvent()` 能正确绘制任意传入区域，而不是假设每个 `update()` 都对应一次单独回调。

最实用的策略通常是：

1. 保持完整、可重建的控件状态。
2. 在状态改变时调用 `update()` 或 `update(dirtyRect)`。
3. 在 `paintEvent()` 中只读取状态并绘制，不在这里改变会再次触发更新的业务状态。
4. 当性能测量显示确有收益时，使用 `event->rect()` 或 `event->region()` 过滤昂贵图层。

许多小控件完整重绘比维护复杂的脏矩形逻辑更快、更不容易漏画。只有缓存、海量项目视图或大画布等明确瓶颈，才值得围绕 `region()` 做细粒度绘制。

## 构造器适用范围

应用代码很少直接构造 `QPaintEvent`。两个构造器主要用于 Qt 内部、事件测试或需要人工发送事件的极少数框架代码：

- 用 `QRect` 构造时，事件区域就是该矩形。
- 用 `QRegion` 构造时，可以表达多个不连续的失效矩形。

手动 `sendEvent()` 并不能替代 widget 的正常更新流程，也不会自动完成窗口系统和 backing store 的所有协调。常规控件刷新应使用 `update()`。

## 常见错误

- 在非 `paintEvent()` 中创建 `QPainter(this)`：改为更新状态后 `update()`。
- 只根据 `event->rect()` 绘制一小块，却没有保证这块能覆盖控件的所有可见内容：会遗留旧像素。
- 认为 `region()` 是自己设置的 `QPainter` clip：两者不同，事件区域由 Qt 的更新系统决定。
- 保存 `QPaintEvent *` 到成员中以后使用：事件生命周期只覆盖当前事件处理。
- 为每个很小的变化调用 `repaint()`：会失去 Qt 的更新合并，滚动和动画容易卡顿。

## API 速查表

| API | 语义与使用边界 |
| --- | --- |
| `QPaintEvent(const QRect &paintRect)` | 构造一个矩形失效区域的绘制事件；常规 widget 代码几乎不需手动构造。 |
| `QPaintEvent(const QRegion &paintRegion)` | 构造一个可由多个矩形组成的失效区域事件；用于测试/框架场景。 |
| `rect()` | 返回 `region()` 的包围矩形，适合快速粗略过滤；它可能大于实际失效区域。 |
| `region()` | 返回实际待更新的 `QRegion`；处理事件时 Qt 已据此裁剪绘制。 |
| 继承的 `type()` | 返回事件类型 `QEvent::Paint`，仅在通用事件分发中需要检查。 |
