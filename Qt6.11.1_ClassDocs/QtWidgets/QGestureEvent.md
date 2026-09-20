# QGestureEvent

> Qt 6.11.1 · Qt Widgets · 来自 `QGestureEvent`

## 1. 先建立直觉

`QGestureEvent` 是 Qt 把手势送到控件时使用的事件对象。一次事件里可能包含多个手势，比如同一段触摸输入既可能被识别为 pan，也可能同时带有 pinch 状态。

它的重点不是“事件发生了”这么简单，而是你要决定每个手势是否由当前控件处理。手势可以被当前控件接受，也可以被忽略后交给父控件或其他处理路径。

## 2. 类说明

`QGestureEvent` 继承自 `QEvent`。控件通常在 `QWidget::event()` 或事件过滤器中检测 `QEvent::Gesture`，再把事件转换成 `QGestureEvent`。

事件对象只在处理期间有效，不应该保存指针。业务层应该读取手势数据，立即更新视图状态、滚动位置、缩放比例或命令状态。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `gestures()` | 返回事件携带的全部手势。 |
| `activeGestures()` | 返回正在活动且未取消的手势。 |
| `canceledGestures()` | 返回已取消手势，适合回滚临时交互状态。 |
| `gesture(Qt::GestureType)` | 按类型取某个手势，例如 `Qt::PinchGesture`。 |
| `accept(QGesture *)` | 接受指定手势，表示当前对象处理它。 |
| `ignore(QGesture *)` | 忽略指定手势，让它有机会继续传播。 |
| `accept(Qt::GestureType)` / `ignore(Qt::GestureType)` | 按手势类型接受或忽略。 |
| `setAccepted(..., bool)` | 程序化设置某个手势接受状态。 |
| `isAccepted(...)` | 查询某个手势是否已接受。 |
| `widget()` | 返回接收事件的 widget。 |
| `mapToGraphicsScene(const QPointF &)` | 把手势点映射到 Graphics View 场景坐标。 |

## 4. 关键用法

```cpp
bool ImageView::event(QEvent *event)
{
    if (event->type() == QEvent::Gesture) {
        auto *ge = static_cast<QGestureEvent *>(event);

        if (auto *pinch = static_cast<QPinchGesture *>(ge->gesture(Qt::PinchGesture))) {
            applyPinch(pinch);
            ge->accept(pinch);
        }

        if (auto *pan = static_cast<QPanGesture *>(ge->gesture(Qt::PanGesture))) {
            scrollBy(pan->delta());
            ge->accept(pan);
        }

        return true;
    }
    return QWidget::event(event);
}
```

如果只处理 pinch，不处理 pan，就只接受 pinch。不要无条件接受全部手势，否则父控件可能收不到它本该处理的滚动或导航手势。

## 5. 使用场景

适合触摸画布、图片查看器、地图控件、图形场景、仪表盘、可缩放编辑器、平板设备上的 Widgets 应用。

如果控件只需要普通鼠标事件，直接处理 `mousePressEvent()` / `mouseMoveEvent()` 更直观。手势事件适合抽象出“滑动、捏合、轻点”这样的高级输入。

## 6. 常见坑与经验

一个 `QGestureEvent` 可以包含多个手势。不要写成 `if/else` 后只处理第一个，除非你明确要互斥。

被取消的手势也很重要。比如 pinch 取消时，要清理临时缩放中心、撤销视觉反馈或停止惯性计算。

Graphics View 场景里注意坐标转换。手势位置可能来自 viewport/widget 坐标，真正操作 item 时通常需要映射到 scene。
