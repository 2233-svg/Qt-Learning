# QGestureRecognizer：自定义手势识别器基类

> Qt 6.11.1 · `#include <QGestureRecognizer>` · 模块：`Qt6::Widgets`

`QGestureRecognizer` 是 Qt 手势识别流程的扩展点。它负责观察目标对象收到的输入事件，更新对应的 `QGesture` 对象，并返回当前识别状态，让 Qt 决定是否投递 `QGestureEvent`。

## 什么时候需要它

标准手势如 pan、pinch、swipe、tap 通常不需要手写 recognizer，只要在 widget 或 graphics object 上 grab 对应手势即可。只有当你要识别应用特有的输入序列，例如三指特定轨迹、压感笔组合动作、复杂鼠标拖拽模式时，才需要派生 `QGestureRecognizer`。

自定义 recognizer 需要注册到应用，注册后 Qt 接管 recognizer 所有权，并返回一个 gesture type。

## 识别流程

Qt 为每个目标对象调用 `create()` 创建 `QGesture`。之后每个相关输入事件都会进入 `recognize(gesture, watched, event)`；recognizer 在这里更新 gesture 属性，并返回 `Ignore`、`MayBeGesture`、`TriggerGesture`、`FinishGesture` 或 `CancelGesture` 等结果。取消时 Qt 调用 `reset()`，给 recognizer 清理或重置属性的机会。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QGestureRecognizer()` | 构造识别器；注册后由 `QApplication` 管理。 |
| `~QGestureRecognizer()` | 虚析构。 |
| `create(QObject *target)` | 为目标创建手势对象；默认创建 `QGesture`，可重写返回派生类。 |
| `recognize(QGesture *, QObject *watched, QEvent *)` | 纯虚函数；根据输入事件更新手势并返回识别结果。 |
| `reset(QGesture *)` | 手势取消或复用前调用；可重置自定义属性。 |
| `registerRecognizer(QGestureRecognizer *)` | 注册识别器并返回 gesture type；应用程序取得该类型后可 grab。 |
| `unregisterRecognizer(Qt::GestureType)` | 注销指定类型的识别器。 |
| `Ignore` | 当前事件不属于该手势。 |
| `MayBeGesture` | 可能是手势，但还未确认。 |
| `TriggerGesture` | 手势已触发，应投递事件。 |
| `FinishGesture` | 手势完成。 |
| `CancelGesture` | 手势取消。 |
| `ConsumeEventHint` | 提示 Qt 消费当前输入事件，避免继续被普通控件处理。 |
