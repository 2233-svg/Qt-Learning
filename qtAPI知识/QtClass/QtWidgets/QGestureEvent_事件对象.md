# QGestureEvent：一次投递中的手势集合

> Qt 6.11.1 · `#include <QGestureEvent>` · 模块：`Qt6::Widgets` · 继承：`QEvent`

`QGestureEvent` 是 Qt 把一个或多个 `QGesture` 交给目标对象的事件。一个事件里可能同时包含平移、捏合、轻触等多个手势，也可能包含刚被取消的手势。

## 解决的问题

手势识别不是“一种输入对应一个事件”那么简单：同一串触摸可能同时被多个 recognizer 观察，某些手势成功后还可能取消另一些。`QGestureEvent` 提供统一入口，让事件处理器逐个接受或忽略手势，并决定未处理手势是否继续向父级传播。

## 接受与传播

对整个 `QEvent` 调用 `accept()` 会影响事件级别；但更常见的是对特定手势或手势类型调用 `accept()`/`ignore()`。未被接受且处于 `GestureStarted` 的手势可能沿父 widget 链继续传播，直到某个对象接受它或事件过滤器消费事件。

`QEvent::Gesture` 中的手势默认被接受；`QEvent::GestureOverride` 中的手势默认被忽略，通常用于让父级有机会抢先声明是否接管。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QGestureEvent(const QList<QGesture *> &gestures)` | 构造包含一组手势的事件；通常由 Qt 创建。 |
| `gestures() const` | 返回事件中全部手势。 |
| `gesture(Qt::GestureType type) const` | 按类型取一个手势；没有则返回 `nullptr`。 |
| `activeGestures() const` | 返回未取消、仍活动的手势。 |
| `canceledGestures() const` | 返回被取消的手势。 |
| `accept(QGesture *)` / `ignore(QGesture *)` | 接受或忽略某个具体手势。 |
| `accept(Qt::GestureType)` / `ignore(Qt::GestureType)` | 按类型接受或忽略手势。 |
| `setAccepted(..., bool)` | 设置具体手势或类型的接受标志。 |
| `isAccepted(...) const` | 查询具体手势或类型是否被接受。 |
| `widget() const` | 返回事件发生的 widget。 |
| `mapToGraphicsScene(const QPointF &)` | 把屏幕坐标手势点映射到 scene 坐标；仅 Graphics View 场景有意义。 |
