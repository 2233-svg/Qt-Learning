# QTapAndHoldGesture：长按手势的数据对象

> Qt 6.11.1 · `#include <QTapAndHoldGesture>` · 模块：`Qt6::Widgets` · 继承：`QGesture`

`QTapAndHoldGesture` 表示用户按住一段时间后触发的长按手势，也常叫 long tap。它常用于触摸界面的上下文菜单、拖拽准备、显示辅助操作等。

## 触发语义

recognizer 在触点按下后开始计时；如果到达超时时间时触点仍保持按下，就触发长按。默认超时是 700 ms，可通过静态 `setTimeout()` 修改。这个值是全局手势识别参数，不是某个对象的局部属性。

`position()` 给出长按位置。若同时启用 tap、tap-and-hold 和 context menu，要清楚哪个动作接受事件，避免重复弹菜单或重复选中。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QTapAndHoldGesture(QObject *parent = nullptr)` | 构造长按手势；通常由 Qt 创建。 |
| `position() const` | 返回长按位置。 |
| `setPosition(const QPointF &)` | 设置位置，主要供 recognizer 使用。 |
| `setTimeout(int msecs)` | 设置全局长按触发时间；默认 700 ms。 |
| `timeout()` | 返回当前长按触发时间。 |
| 超时范围 | 太短容易误触发，太长会让触摸界面显得迟钝。 |
