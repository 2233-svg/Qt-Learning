# QGestureRecognizer

> Qt 6.11.1 · Qt Widgets · 来自 `QGestureRecognizer`

## 1. 先建立直觉

`QGestureRecognizer` 是自定义手势识别器。Qt 内置了 tap、pan、pinch、swipe 等常见手势；当你需要“画一个特定路径”“三指特定动作”“业务专属输入模式”时，就需要编写 recognizer。

它本质上是一个状态机：Qt 把输入事件交给你，你根据已有状态和新事件判断当前是忽略、可能是手势、已经触发、完成还是取消。

## 2. 类说明

`QGestureRecognizer` 不是 `QObject`，也不是 widget。你继承它，重写 `recognize()`，必要时重写 `create()` 创建自定义 `QGesture` 子类保存额外数据。

注册后，Qt 返回一个自定义 `Qt::GestureType`。控件通过 `grabGesture(type)` 订阅，之后就能在 `QGestureEvent` 中收到你的自定义手势。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `recognize(QGesture *, QObject *, QEvent *)` | 核心识别函数，根据输入事件更新手势状态并返回结果。 |
| `create(QObject *target)` | 创建手势对象。默认创建 `QGesture`，需要额外字段时返回自定义子类。 |
| `reset(QGesture *)` | 重置手势对象状态，取消或结束后清理临时数据。 |
| `registerRecognizer(QGestureRecognizer *)` | 注册识别器并获得新的手势类型。Qt 接管 recognizer 生命周期。 |
| `unregisterRecognizer(Qt::GestureType)` | 注销自定义手势类型。 |
| `Ignore` | 当前事件不影响识别。 |
| `MayBeGesture` | 事件可能属于手势，但还需要更多输入确认。 |
| `TriggerGesture` | 手势已经触发，会发送给目标。 |
| `FinishGesture` | 手势成功结束。 |
| `CancelGesture` | 手势应取消。 |
| `ConsumeEventHint` | 提示框架消耗原始事件，避免继续传给目标。 |

## 4. 关键用法

识别器的大致结构：

```cpp
class MyGestureRecognizer : public QGestureRecognizer {
public:
    Result recognize(QGesture *gesture, QObject *watched, QEvent *event) override
    {
        Q_UNUSED(watched);

        switch (event->type()) {
        case QEvent::MouseButtonPress:
            rememberStart(gesture, event);
            return MayBeGesture | ConsumeEventHint;
        case QEvent::MouseMove:
            return updateAndDecide(gesture, event);
        case QEvent::MouseButtonRelease:
            return FinishGesture;
        default:
            return Ignore;
        }
    }
};
```

注册并订阅：

```cpp
const Qt::GestureType myGestureType =
    QGestureRecognizer::registerRecognizer(new MyGestureRecognizer);

widget->grabGesture(myGestureType);
```

## 5. 使用场景

适合专业图形软件里的手势命令、触控大屏操作、绘图板输入、业务专用路径识别、复杂触摸板手势，以及需要统一处理 mouse/touch/graphics scene 输入的高级控件。

如果只是识别一次拖动距离、双击或右键菜单，不必上自定义 recognizer。普通事件处理更易懂，也更容易维护。

## 6. 常见坑与经验

`MayBeGesture` 不能卡太久。用户输入不能被无限期悬挂，否则点击、拖动等普通事件会显得延迟或丢失。

`ConsumeEventHint` 要谨慎使用。它会影响原始事件是否继续传递，错误使用会让控件看起来“不响应鼠标”。

自定义手势数据最好放在自定义 `QGesture` 子类里，而不是 recognizer 的全局成员里。一个 recognizer 可能服务多个目标，状态混在一起会出问题。
