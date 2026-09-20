# QTapGesture

> Qt 6.11.1 · Qt Widgets · 来自 `QTapGesture`

## 1. 先建立直觉

`QTapGesture` 表示一次轻点手势。它对应触摸语义中的“点一下”，常用于选择对象、激活卡片、打开详情、在画布上放置光标。

它和鼠标点击很像，但不完全等同。触摸输入可能没有鼠标按钮、没有 hover，也可能和 pan、tap-and-hold 竞争。使用 `QTapGesture` 时，要站在触控设备的交互模型上设计。

## 2. 类说明

`QTapGesture` 继承自 `QGesture`。它主要提供 `position`，表示轻点发生的位置。这个位置用于命中测试、选择 item、定位光标或显示上下文 UI。

轻点是否触发、何时触发，由 Qt 手势识别器根据输入事件判断。你的代码通常在 `QGestureEvent` 中读取它，然后决定业务行为。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `position()` | 返回轻点位置。 |
| `setPosition(const QPointF &)` | 设置轻点位置，通常由识别器使用。 |
| `state()` | 继承自 `QGesture`，判断手势是否完成或取消。 |
| `gestureType()` | 返回 `Qt::TapGesture`。 |
| `hotSpot()` | 继承自 `QGesture`，可表达全局手势热点。 |

## 4. 关键用法

```cpp
if (auto *tap = static_cast<QTapGesture *>(event->gesture(Qt::TapGesture))) {
    if (tap->state() == Qt::GestureFinished) {
        selectItemAt(tap->position().toPoint());
    }
    event->accept(tap);
}
```

如果在 Graphics View 里使用，要把点转换到场景坐标：

```cpp
const QPointF scenePos = gestureEvent->mapToGraphicsScene(tap->position());
```

## 5. 使用场景

适合触控列表项选择、画布点选、图片查看器显示/隐藏工具栏、地图选点、平板上的属性面板激活。

如果你的界面只面向鼠标键盘，普通 `mousePressEvent()` / `clicked()` 信号更简单。`QTapGesture` 的价值在于和其他触摸手势共同工作。

## 6. 常见坑与经验

轻点和长按要区分。不要在 tap 刚开始时就执行不可逆动作，否则用户本来想长按打开菜单也可能被误触发。

坐标系要确认。`position()` 不一定就是业务对象所在坐标系，复杂视图中常需要映射。

Tap 适合轻量动作。删除、提交订单、重置配置这类高风险操作，不应该只靠一次触摸轻点直接完成。
