# QGesture：手势识别结果的公共基类

> Qt 6.11.1 · `#include <QGesture>` · 模块：`Qt6::Widgets` · 继承：`QObject`

`QGesture` 表示一次被 Qt 手势系统识别出来的手势。它不是原始触摸/鼠标事件，也不是识别器本身；识别器更新 `QGesture` 的状态和属性，Qt 再把它放进 `QGestureEvent` 交给目标 widget 或 graphics item。

## 使用场景

应用层通常不会直接创建 `QGesture`，而是在 widget 上 `grabGesture()`，然后在 `QEvent::Gesture` 中读取 `QPanGesture`、`QPinchGesture`、`QTapGesture` 等派生对象。自定义手势时，`QGesture` 可以作为承载识别结果的基类，也可以通过动态属性扩展信息。

手势对象由 Qt 创建和管理，不适合从事件里取出后长期缓存裸指针。

## 状态和位置

`state()` 描述手势生命周期：开始、更新、完成或取消。连续手势通常在 `GestureUpdated` 中实时更新 UI，而不是等到 `GestureFinished` 才处理。

`hotSpot()` 是全局坐标中的关注点，可能不存在；先检查 `hasHotSpot()`。在 widget 中要映射到本地坐标，在 Graphics View 中可结合 `QGestureEvent::mapToGraphicsScene()`。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QGesture(QObject *parent = nullptr)` | 构造手势对象；通常由 recognizer 或 Qt 框架调用。 |
| `~QGesture()` | 虚析构；应用层不要手动销毁事件中的手势对象。 |
| `gestureType() const` | 返回 `Qt::GestureType`，如 `Qt::PanGesture`。 |
| `state() const` | 返回当前识别状态，用于区分 started/updated/finished/canceled。 |
| `hotSpot() const` | 返回全局 hot spot；不保证每种手势都有。 |
| `setHotSpot(const QPointF &)` | 设置 hot spot；主要供 recognizer 使用。 |
| `hasHotSpot() const` | 判断 hot spot 是否有效。 |
| `unsetHotSpot()` | 清除 hot spot。 |
| `setGestureCancelPolicy(policy)` | 设置接受本手势时是否取消同上下文其他手势。 |
| `gestureCancelPolicy() const` | 查询取消策略。 |
| `CancelNone` | 接受本手势不主动取消其他手势。 |
| `CancelAllInContext` | 接受本手势时取消同上下文的其他活动手势。 |
