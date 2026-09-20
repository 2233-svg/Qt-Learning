# QPinchGesture

> Qt 6.11.1 · Qt Widgets · 来自 `QPinchGesture`

## 1. 先建立直觉

`QPinchGesture` 表示双指捏合手势，但它不只包含缩放。一次 pinch 可以同时带来缩放、旋转和中心点移动：两指张开缩放，旋转手指改变角度，两指整体移动改变中心点。

图片查看、地图、图形编辑器和 3D/2D 画布里，pinch 往往是最自然的“以手指中心为锚点缩放”的输入方式。

## 2. 类说明

`QPinchGesture` 继承自 `QGesture`。它提供三组值：当前值、上一帧值、总变化值。例如 `scaleFactor()` 是当前变化，`lastScaleFactor()` 是上一次变化，`totalScaleFactor()` 是从手势开始累计到当前的缩放。

`changeFlags()` 告诉你本次事件哪些分量发生了变化，`totalChangeFlags()` 告诉你整个手势过程中哪些分量曾经变化。优秀的处理代码会看 flags，只更新真正变化的部分。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `scaleFactor()` | 当前缩放因子。 |
| `lastScaleFactor()` | 上一次缩放因子。 |
| `totalScaleFactor()` | 从手势开始累计的缩放因子。 |
| `rotationAngle()` | 当前旋转角度变化。 |
| `lastRotationAngle()` | 上一次旋转角度。 |
| `totalRotationAngle()` | 累计旋转角度。 |
| `centerPoint()` | 当前手势中心点。 |
| `lastCenterPoint()` | 上一次中心点。 |
| `startCenterPoint()` | 手势开始时的中心点。 |
| `changeFlags()` | 本次事件变化了缩放、旋转还是中心点。 |
| `totalChangeFlags()` | 整个手势累计涉及哪些变化。 |
| `ScaleFactorChanged` | 缩放发生变化。 |
| `RotationAngleChanged` | 旋转发生变化。 |
| `CenterPointChanged` | 中心点发生变化。 |

## 4. 关键用法

```cpp
if (auto *pinch = static_cast<QPinchGesture *>(event->gesture(Qt::PinchGesture))) {
    if (pinch->changeFlags() & QPinchGesture::ScaleFactorChanged) {
        zoomAt(pinch->centerPoint(), pinch->scaleFactor());
    }

    if (pinch->changeFlags() & QPinchGesture::RotationAngleChanged) {
        rotateBy(pinch->rotationAngle() - pinch->lastRotationAngle());
    }

    event->accept(pinch);
}
```

如果你希望整个手势结束后一次性应用结果，可以等 `pinch->state() == Qt::GestureFinished` 时读取 `totalScaleFactor()` 和 `totalRotationAngle()`。

## 5. 使用场景

适合图片缩放、地图缩放旋转、PDF/图纸查看、流程图画布、时间轴缩放、触控屏大屏编辑器、移动工作站上的自然输入。

如果只需要鼠标滚轮缩放，不必强行使用 pinch。两者可以共存：滚轮服务鼠标用户，pinch 服务触控板/触摸屏用户。

## 6. 常见坑与经验

缩放应围绕 `centerPoint()`，而不是总围绕视图中心。否则用户会觉得手指下的内容“滑走了”。

不要假设 pinch 一定有旋转。很多设备或平台只上报缩放；用 `changeFlags()` 判断，而不是硬套全部分量。

累计值和增量值要选一种模型。混合使用 `scaleFactor()` 与 `totalScaleFactor()` 很容易把缩放应用两次。
