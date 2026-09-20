# QTest::QTouchEventWidgetSequence
> Qt 6.11.1 · Qt Test · 来自 `QTest::QTouchEventWidgetSequence`

## 1. 先建立直觉

`QTouchEventWidgetSequence` 是面向 `QWidget` 的触摸事件序列。它继承自 `QTouchEventSequence`，但把目标从 `QWindow *` 换成更适合传统 Widgets 测试的 `QWidget *`。

## 2. 类说明

保留类说明：这些 API 来自 `QTest::QTouchEventWidgetSequence`，属于 Qt Test 模块，用于在 QWidget 测试中模拟触摸 press/move/release。

如果你的被测对象是 QWidget 或其子类，用这个类比窗口级序列更直接；如果是 QWindow/Quick 场景，则使用基类窗口版本。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `press(touchId, pt, widget)` | 在 widget 坐标中添加触点按下。 |
| `move(touchId, pt, widget)` | 在 widget 坐标中添加触点移动。 |
| `release(touchId, pt, widget)` | 在 widget 坐标中添加触点释放。 |
| 继承的 `stationary(touchId)` | 保持触点不动。 |
| 继承的 `commit(processEvents)` | 提交当前触摸事件序列。 |

## 4. 典型流程

```cpp
QTest::touchEvent(widget, device)
    .press(0, QPoint(30, 30), widget)
    .move(0, QPoint(90, 30), widget)
    .release(0, QPoint(90, 30), widget)
    .commit();
```

坐标按 widget 本地坐标理解，不是全局屏幕坐标。

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 自定义 QWidget 触摸交互 | 测试滑动、拖拽、长按的状态变化。 |
| 触控版桌面控件 | 验证鼠标和触摸路径是否都可用。 |
| 多点 widget 手势 | 配合 `stationary()` 和多个 touchId。 |

## 6. 常见坑与经验

widget 必须能接收触摸事件，通常需要相关属性或平台支持。测试事件发出去了，不代表控件一定订阅了触摸输入。

不要把 QWidget 坐标和窗口坐标混用。控件嵌套较深时，传给序列的位置应对应目标 widget 的本地坐标。

如果控件内部把触摸转换成鼠标事件，也要明确测试的是触摸路径还是兼容鼠标路径，避免同一个行为被重复触发。

## 7. 知识点覆盖

- QWidget 触摸测试入口。
- widget 本地坐标和触点生命周期。
- 与 `QTouchEventSequence` 的继承关系。
- 触摸订阅、事件转换和平台差异。
