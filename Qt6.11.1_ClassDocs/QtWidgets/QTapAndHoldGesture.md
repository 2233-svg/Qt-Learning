# QTapAndHoldGesture

> Qt 6.11.1 · Qt Widgets · 来自 `QTapAndHoldGesture`

## 1. 先建立直觉

`QTapAndHoldGesture` 表示“点住不放”的长按手势。它通常承担触摸设备上的右键语义：打开上下文菜单、进入选择模式、显示更多操作。

它和 `QTapGesture` 的区别在时间：tap 是快速轻点，tap-and-hold 要按住超过阈值。这个阈值由类的静态 timeout 控制。

## 2. 类说明

`QTapAndHoldGesture` 继承自 `QGesture`。它提供长按位置，并提供静态 `setTimeout()` / `timeout()` 控制识别长按所需时间。

长按通常应该触发“可取消、可解释”的操作，例如弹出菜单，而不是直接执行高风险命令。因为用户在触摸屏上的长按精度和意图有时不如鼠标右键清晰。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `position()` | 返回长按位置。 |
| `setPosition(const QPointF &)` | 设置长按位置，通常由识别器使用。 |
| `setTimeout(int msecs)` | 设置全局长按识别时间。影响 `QTapAndHoldGesture` 的识别阈值。 |
| `timeout()` | 读取当前全局长按超时时间。 |
| `state()` | 继承自 `QGesture`，可判断长按是否触发、完成或取消。 |
| `gestureType()` | 返回 `Qt::TapAndHoldGesture`。 |

## 4. 关键用法

```cpp
if (auto *hold = static_cast<QTapAndHoldGesture *>(event->gesture(Qt::TapAndHoldGesture))) {
    if (hold->state() == Qt::GestureFinished) {
        showContextMenu(hold->position().toPoint());
    }
    event->accept(hold);
}
```

如需调整长按识别时间：

```cpp
QTapAndHoldGesture::setTimeout(700);
```

这是全局设置，适合应用启动时统一配置，不适合每个控件随意改。

## 5. 使用场景

适合触摸上下文菜单、列表项更多操作、画布对象进入选择模式、地图标记详情、平板应用中的辅助命令入口。

不适合高频操作，也不适合必须快速完成的动作。长按天然比点击慢，应留给不那么常用但需要可发现性的功能。

## 6. 常见坑与经验

全局 timeout 改得太短，会让普通 tap 容易被误判；改得太长，用户会觉得长按不灵敏。

长按和拖动会竞争。用户手指按住后轻微移动是常见现象，交互设计上要允许一定容错，不要一点移动就让体验断裂。

在桌面端同时支持鼠标右键和触摸长按时，两者应打开同一套上下文菜单，避免功能分裂。
