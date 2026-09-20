# QNativeGestureEvent

> Qt 6.11.1 · Qt GUI · 来自 `QNativeGestureEvent`

## 1. 先建立直觉

`QNativeGestureEvent` 表示操作系统或触摸板驱动已经识别好的原生手势，例如缩放、旋转、平移、滑动。它不是原始多触点数据；原始触点应看 `QTouchEvent` 和 `QEventPoint`。

这一点决定了处理方式：收到原生手势时，通常不再自己从两根手指坐标推导缩放比或旋转角，而是直接根据 `gestureType()` 解释 `value()` 或 `delta()`。它更容易获得平台一致的触摸板体验，但可用手势种类和数值精度受平台影响。

## 2. 类说明

`QNativeGestureEvent` 继承自 `QSinglePointEvent`。它因此拥有位置、全局位置、修饰键和来源设备信息；本类额外提供原生手势类型、手指数、手势 value 和平移 delta。

类说明只用于表明这些 API 来自 `QNativeGestureEvent`：具体手势识别由平台完成，应用负责把事件映射成视图缩放、旋转、平移或导航行为。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QNativeGestureEvent(type, device, fingerCount, localPos, scenePos, globalPos, value, delta, sequenceId)` | 构造原生手势事件，主要用于测试、平台层或输入转发。 |
| `gestureType() const` | 返回原生手势类型，如 Begin、End、Zoom、Rotate、Pan、Swipe。 |
| `value() const` | 返回与手势类型相关的数值；缩放、旋转、滑动的解释不同。 |
| `delta() const` | 返回相对上一事件的平移量，单位为像素，主要用于 Pan。 |
| `fingerCount() const` | 返回参与手势的手指数；未知时可能为 0。 |
| `position() const` | 来自父类，手势锚点在接收对象中的局部坐标。 |
| `globalPosition() const` | 来自父类，手势锚点在屏幕中的全局坐标。 |
| `pointingDevice() const` | 来自父类，读取产生手势的指针设备。 |

## 4. 关键用法

### 缩放以手势位置为锚点

缩放手势的 `value()` 通常是一个很小的增量。常见计算方式是乘以 `1 + value`，不要把它直接当成最终缩放比例。

```cpp
bool ImageView::event(QEvent *event)
{
    if (event->type() == QEvent::NativeGesture) {
        auto *gesture = static_cast<QNativeGestureEvent *>(event);

        if (gesture->gestureType() == Qt::ZoomNativeGesture) {
            zoomAt(gesture->position(), 1.0 + gesture->value());
            gesture->accept();
            return true;
        }
    }

    return QWidget::event(event);
}
```

以 `position()` 为锚点可以让用户在图片某处捏合时，那一处保持在视觉中心附近。

### 平移使用 `delta()`

```cpp
if (gesture->gestureType() == Qt::PanNativeGesture) {
    panBy(gesture->delta());
    gesture->accept();
}
```

`delta()` 表示相对于上一原生手势事件的像素增量；不要把它与 `value()` 混合使用。

### 旋转和 swipe 的 value 语义不同

旋转手势的 `value()` 通常表示角度增量；滑动手势也可能使用角度或方向相关数值。处理前必须先看 `gestureType()`，不要写一条“所有手势都按 value 缩放”的通用逻辑。

### Begin / End 适合管理连续交互状态

在平台支持时，`BeginNativeGesture` 与 `EndNativeGesture` 可用于启动或结束临时状态，例如禁止文本选择、开始批量视图刷新、结束后做吸附动画。手指数在 begin/end 阶段可能未知，因此不应依赖它做核心判断。

## 5. 使用场景

`QNativeGestureEvent` 适合图片浏览、地图、画布、CAD、时间轴、演示视图、音频波形和触摸板优化的桌面应用。

它特别适合“系统触摸板应该有原生感觉”的功能：pinch-to-zoom、两指平移、旋转画布、三指或多指 swipe 导航。原生手势通常比自己把触摸板行为模拟成鼠标滚轮更自然。

## 6. 常见坑与经验

不要把原生手势和 `QTouchEvent` 重复处理成两次操作。先明确你的控件是消费原始触点、原生手势，还是按设备类型选择其中一个入口。

不要假设所有平台都会发送所有 gesture type。应为缺失原生手势准备鼠标滚轮、快捷键或触摸事件降级方案。

不要忽略 delta 为零的开始/结束事件。它们可能只用于标记序列边界。

不要把 `fingerCount()` 当作可靠的手势类型判断。它是辅助信息，未知时为 0；真正的判断依据是 `gestureType()`。

## 7. 知识点覆盖

学习 `QNativeGestureEvent` 应覆盖平台原生手势、缩放增量、旋转角、平移 delta、手势序列、手指数量、锚点缩放、触摸板体验、原始触点与已识别手势的选择、跨平台降级。
