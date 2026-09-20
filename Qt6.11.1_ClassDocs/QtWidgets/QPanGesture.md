# QPanGesture

> Qt 6.11.1 · Qt Widgets · 来自 `QPanGesture`

## 1. 先建立直觉

`QPanGesture` 表示平移手势：手指或触控板拖动内容，让视图跟着移动。图片查看器拖动画布、地图平移、图形场景移动视口，都属于 pan 的典型语义。

它不是滚动条本身，也不是惯性滚动引擎。它只描述一次平移动作的位移、上一帧位移和加速度；你要把这些数据应用到自己的视图、变换或滚动位置上。

## 2. 类说明

`QPanGesture` 继承自 `QGesture`。它提供 `offset`、`lastOffset`、`delta`、`acceleration` 等属性，用来描述从手势开始到当前的累计位移、上一状态和本次变化。

实践中通常读取 `delta()` 做增量移动，而不是每帧根据 `offset()` 重新推导全部状态。这样代码更接近“当前帧移动了多少”的交互模型。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `offset()` | 手势开始以来的累计偏移。 |
| `setOffset(const QPointF &)` | 设置累计偏移，通常由识别器使用。 |
| `lastOffset()` | 上一次事件时的累计偏移。 |
| `setLastOffset(const QPointF &)` | 设置上一次偏移，通常由识别器使用。 |
| `delta()` | 当前偏移与上一次偏移的差值，最适合驱动视图移动。 |
| `acceleration()` | 平移动作的加速度估计，可用于惯性或响应强度判断。 |
| `setAcceleration(qreal)` | 设置加速度，通常由识别器使用。 |
| `state()` | 继承自 `QGesture`，判断手势开始、更新、结束或取消。 |

## 4. 关键用法

```cpp
if (auto *pan = static_cast<QPanGesture *>(event->gesture(Qt::PanGesture))) {
    const QPointF d = pan->delta();
    translateView(d.x(), d.y());
    event->accept(pan);
}
```

如果你的坐标系里“拖动内容”方向和“移动视口”方向相反，要明确取反：

```cpp
scrollBarH->setValue(scrollBarH->value() - int(pan->delta().x()));
scrollBarV->setValue(scrollBarV->value() - int(pan->delta().y()));
```

## 5. 使用场景

适合地图、图片查看器、PDF/图纸视图、图形场景、时间轴、数据可视化画布、触控屏上的大面板平移。

如果目标是标准滚动区域的触摸惯性滚动，优先看 `QScroller`；如果只是鼠标拖拽某个对象，普通 mouse move 事件可能更直观。

## 6. 常见坑与经验

`offset()` 是累计量，`delta()` 是增量。混用会导致移动速度越来越奇怪，尤其在缩放后的坐标系中更明显。

平移手势和点击手势可能竞争。处理 pan 时要只在确实进入拖动后接受它，避免轻点被误吞。

对可缩放画布应用 pan 时，要考虑当前缩放比例。屏幕像素位移不一定等于场景坐标位移。
