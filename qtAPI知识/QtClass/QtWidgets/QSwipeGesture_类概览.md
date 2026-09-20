# QSwipeGesture：快速划动手势的数据对象

> Qt 6.11.1 · `#include <QSwipeGesture>` · 模块：`Qt6::Widgets` · 继承：`QGesture`

`QSwipeGesture` 描述一次快速划动。它适合触发离散动作：翻页、切换面板、返回上一层、在照片之间切换，而不是连续拖动物体。

## 使用方式

目标 widget grab `Qt::SwipeGesture` 后，在 `QGestureEvent` 中读取 `QSwipeGesture`。通常在 `GestureFinished` 或触发后处理一次动作；如果要跟随手指连续移动，应使用 `QPanGesture`。

方向由 `swipeAngle()` 推导成水平和垂直方向。一次斜向 swipe 可能同时有水平和垂直分量；没有对应分量时方向为 `NoDirection`。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QSwipeGesture(QObject *parent = nullptr)` | 构造 swipe 手势；通常由 Qt 创建。 |
| `SwipeDirection` | `NoDirection`、`Left`、`Right`、`Up`、`Down`。 |
| `horizontalDirection() const` | 返回水平分量方向；无水平分量时为 `NoDirection`。 |
| `verticalDirection() const` | 返回垂直分量方向；无垂直分量时为 `NoDirection`。 |
| `swipeAngle() const` | 返回相对 x 轴的运动角度。 |
| `setSwipeAngle(qreal)` | 设置角度，主要供 recognizer 使用。 |
| `state() const` | 继承自 `QGesture`；离散动作通常避免重复触发。 |
