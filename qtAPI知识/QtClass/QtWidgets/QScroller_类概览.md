# QScroller：给任意目标增加动量滚动

> Qt 6.11.1 · `#include <QScroller>` · 模块：`Qt6::Widgets` · 继承：`QObject`

`QScroller` 为 widget 或 graphics item 提供 kinetic scrolling：用户拖动后内容会按速度和摩擦继续滚动，直到停止或被新输入打断。它保存滚动状态、速度、目标位置，并向目标发送滚动准备和滚动事件。

## 使用场景

触摸界面的列表、画布、图片视图、自定义滚动区域都可以使用 `QScroller`。常见做法是 `QScroller::grabGesture(target, QScroller::TouchGesture)`，让 Qt 的 flick recognizer 自动把触摸输入交给 scroller。更底层的控件或自定义 recognizer 可以直接调用 `handleInput()`。

目标对象需要响应 `QScrollPrepareEvent` 提供内容范围、当前位置和 viewport 尺寸，并响应 `QScrollEvent` 实际移动内容。

## 状态与坐标

状态包括 `Inactive`、`Pressed`、`Dragging`、`Scrolling`。`velocity()` 以米/秒返回速度；`pixelPerMeter()` 用于物理单位与像素转换。`scrollTo()` 和 `ensureVisible()` 使用像素坐标，滚到合法范围之外时行为未定义或取决于 overshoot 设置。

`scroller(target)` 会为目标隐式创建并返回唯一 scroller；不要手动 delete。

## API 速查表

| API | 语义与边界 |
|---|---|
| `hasScroller(QObject *target)` | 查询目标是否已有 scroller。 |
| `scroller(QObject *target)` | 返回目标唯一 scroller；没有则创建。 |
| `grabGesture(target, type)` | 为目标安装 flick 手势；同一目标同一时间只能有一个滚动手势。 |
| `grabbedGesture(target)` | 查询目标当前抓取的滚动手势类型。 |
| `ungrabGesture(target)` | 移除目标上的滚动手势。 |
| `activeScrollers()` | 返回应用中非 `Inactive` 的 scroller 列表。 |
| `target() const` | 返回被滚动的目标对象。 |
| `state() const` | 查询当前状态。 |
| `handleInput(input, position, timestamp)` | 手动喂入 press/move/release；返回是否应消费事件。 |
| `stop()` | 停止滚动并回到 `Inactive`。 |
| `velocity() const` | Dragging/Scrolling 时返回当前速度，否则通常为零。 |
| `finalPosition() const` | 返回估计最终位置；Inactive 时结果未定义。 |
| `pixelPerMeter() const` | 返回当前目标的像素/米换算。 |
| `scrollerProperties() const` | 返回滚动物理参数。 |
| `setScrollerProperties(const QScrollerProperties &)` | 设置滚动物理参数。 |
| `scrollTo(pos)` / `scrollTo(pos, ms)` | 滚到指定 viewport 坐标，可指定耗时。 |
| `ensureVisible(rect, xmargin, ymargin)` | 滚动使矩形尽量可见。 |
| `resendPrepareEvent()` | 重新发送 prepare 事件；Inactive 时通常无意义。 |
| `setSnapPositionsX/Y(...)` | 设置水平或垂直吸附位置；空列表或 0 间隔可关闭对应吸附。 |
| `stateChanged(State)` | 状态变化信号。 |
| `scrollerPropertiesChanged(...)` | 属性变化信号。 |
