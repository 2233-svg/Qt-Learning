# QGesture

> Qt 6.11.1 · Qt Widgets · 来自 `QGesture`

## 1. 先建立直觉

`QGesture` 是 Qt 手势系统中“已识别手势”的基类。它不代表某一种具体动作，而是给 pan、pinch、swipe、tap、tap-and-hold 等手势提供共同状态：类型、生命周期状态、热点位置和取消策略。

使用手势时，应用通常不会直接 new `QGesture`。你先让控件 `grabGesture()`，然后在 `event()` 里收到 `QGestureEvent`，再取出具体派生类读取数据。

## 2. 类说明

`QGesture` 继承自 `QObject`。它由 Qt 手势识别框架创建和管理，表示一次手势从开始、更新、结束到取消的过程。

真正有业务含义的数据在派生类中：`QPanGesture` 给偏移量，`QPinchGesture` 给缩放和旋转，`QSwipeGesture` 给方向，`QTapGesture` 给点击位置。`QGesture` 本身更像所有手势共同的状态包装。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `gestureType()` | 返回手势类型，用于在事件中区分不同手势。 |
| `state()` | 返回手势状态，例如开始、更新、结束或取消。 |
| `setHotSpot(const QPointF &)` / `hotSpot()` | 设置或读取手势热点位置。 |
| `hasHotSpot()` | 判断是否存在热点位置。 |
| `unsetHotSpot()` | 清除热点。 |
| `setGestureCancelPolicy(GestureCancelPolicy)` | 设置接受当前手势后是否取消同上下文其他手势。 |
| `gestureCancelPolicy()` | 读取取消策略。 |
| `CancelNone` | 接受此手势时不自动取消其他手势。 |
| `CancelAllInContext` | 接受此手势后取消同上下文内其他活动手势。 |

## 4. 关键用法

```cpp
bool Canvas::event(QEvent *event)
{
    if (event->type() == QEvent::Gesture) {
        auto *gestureEvent = static_cast<QGestureEvent *>(event);
        if (auto *pan = static_cast<QPanGesture *>(gestureEvent->gesture(Qt::PanGesture))) {
            panBy(pan->delta());
            gestureEvent->accept(pan);
            return true;
        }
    }
    return QWidget::event(event);
}
```

通常你检查的是 `QGestureEvent`，然后把 `QGesture *` 转成具体类型。不要只看 `QGesture` 基类就试图推断 pan 或 pinch 的详细数据。

## 5. 使用场景

适合触摸屏、触控板、图形视图、地图视图、图片查看器、可缩放画布、仪表盘和需要自然输入的桌面应用。

如果只是键盘快捷键或鼠标点击，普通事件和 `QShortcut` 更清楚。手势系统适合处理“连续动作”和“多点输入”的语义。

## 6. 常见坑与经验

不要长期保存 `QGesture *`。它由 Qt 手势框架管理，应该在事件处理期间读取状态并更新你的业务对象。

接受手势和接受整个事件不是一回事。`QGestureEvent` 可以分别 accept/ignore 某个手势，复杂控件里这能避免父子控件抢同一种输入。

取消策略要谨慎。`CancelAllInContext` 很强，会影响同上下文里的其他手势，适合互斥手势，不适合所有场景默认开启。
