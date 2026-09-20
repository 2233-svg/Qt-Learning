# QSwipeGesture

> Qt 6.11.1 · Qt Widgets · 来自 `QSwipeGesture`

## 1. 先建立直觉

`QSwipeGesture` 表示快速扫动手势。它关心的是“方向和角度”，适合翻页、切换面板、前进后退、打开侧栏这类离散动作。

它和 `QPanGesture` 的区别在于：pan 是连续位移，视图跟着手指走；swipe 是一次快速方向命令，手势完成后触发一个动作。

## 2. 类说明

`QSwipeGesture` 继承自 `QGesture`。它提供水平和垂直方向，以及扫动角度。方向可能是 `Left`、`Right`、`Up`、`Down` 或 `NoDirection`。

实践中一般在手势结束时处理 swipe，避免用户还在移动时就多次翻页。方向判断也要尊重界面语义：左右扫动可能代表切换文档，也可能代表时间轴移动。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `horizontalDirection()` | 返回水平扫动方向：左、右或无。 |
| `verticalDirection()` | 返回垂直扫动方向：上、下或无。 |
| `swipeAngle()` | 返回扫动角度，可用于更细的方向判断。 |
| `setSwipeAngle(qreal)` | 设置角度，通常由识别器使用。 |
| `SwipeDirection::Left` | 向左扫。 |
| `SwipeDirection::Right` | 向右扫。 |
| `SwipeDirection::Up` | 向上扫。 |
| `SwipeDirection::Down` | 向下扫。 |
| `SwipeDirection::NoDirection` | 没有明确方向。 |
| `state()` | 继承自 `QGesture`，通常在 `GestureFinished` 时执行命令。 |

## 4. 关键用法

```cpp
if (auto *swipe = static_cast<QSwipeGesture *>(event->gesture(Qt::SwipeGesture))) {
    if (swipe->state() == Qt::GestureFinished) {
        if (swipe->horizontalDirection() == QSwipeGesture::Left)
            goToNextPage();
        else if (swipe->horizontalDirection() == QSwipeGesture::Right)
            goToPreviousPage();
    }
    event->accept(swipe);
}
```

如果水平和垂直方向都可能存在，先定义业务优先级。比如图片浏览器可能只处理左右扫动，忽略上下扫动。

## 5. 使用场景

适合页面切换、图册上一张/下一张、仪表盘左右切面板、历史前进后退、卡片堆切换、触控大屏上的快速导航。

不适合精确拖动、画布移动、滑块调整或滚动内容。那些动作需要连续反馈，应使用 pan、scroll 或普通拖动事件。

## 6. 常见坑与经验

不要在 `GestureUpdated` 阶段反复执行离散命令。swipe 一般等完成后触发一次。

方向语义在 RTL 语言环境中可能要重新考虑。比如“上一页/下一页”和“左/右”不总是同一个概念。

如果同一控件也支持 pan，swipe 与 pan 可能竞争。明确哪个动作接受手势，避免一次输入既平移又翻页。
