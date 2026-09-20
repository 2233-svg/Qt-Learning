# QScrollEvent

> Qt 6.11.1 · Qt GUI · 来自 `QScrollEvent`

## 1. 先建立直觉

`QScrollEvent` 是 `QScroller` 在滚动过程中发送的位置更新事件。它不报告“这次手指移动了多少”，而是报告“内容现在应该处于什么位置”，并附带超出合法边界的 overshoot 距离。

这使得控件可以把内容位置设置为确定值，而不是自己累计 delta。确定位置在触控、惯性、回弹和帧率变化下更稳定，避免累计误差。

## 2. 类说明

`QScrollEvent` 继承自 `QEvent`，通常在 `event()` 中处理 `QEvent::Scroll`。它由 `QScroller` 基于此前的 `QScrollPrepareEvent` 配置生成。

类说明只用于表明这些 API 来自 `QScrollEvent`：滚动状态机、速度曲线和回弹动画由 `QScroller` 管理；控件负责把 content position 映射为自己的视图偏移并绘制 overshoot 效果。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `enum ScrollState` | 表示一次滚动序列的开始、更新、结束。 |
| `QScrollEvent(contentPos, overshootDistance, state)` | 构造滚动位置更新事件。 |
| `contentPos() const` | 返回当前建议设置的内容位置。 |
| `overshootDistance() const` | 返回超出内容边界的距离，可用于弹性视觉。 |
| `scrollState() const` | 返回滚动阶段：Started、Updated、Finished。 |

## 4. 关键用法

### 用绝对内容位置更新视图

```cpp
bool CanvasView::event(QEvent *event)
{
    if (event->type() == QEvent::Scroll) {
        auto *scroll = static_cast<QScrollEvent *>(event);

        m_contentOffset = scroll->contentPos();
        m_overshoot = scroll->overshootDistance();
        update();

        if (scroll->scrollState() == QScrollEvent::ScrollFinished)
            settleAtBoundary();

        scroll->accept();
        return true;
    }

    return QWidget::event(event);
}
```

不要再把 `contentPos()` 加到旧偏移上。它已经是新位置，重复累加会让内容飞出范围。

### overshoot 只用于视觉，不应修改真实范围

```cpp
const QPointF visualOffset = m_contentOffset - m_overshoot * 0.35;
drawContent(painter, visualOffset);
```

真实内容位置应保持在合法范围；overshoot 是为了做弹性拉伸、阴影或边缘反馈。把它写入真实滚动位置会让边界计算越来越复杂。

### 正确处理滚动序列边界

`ScrollStarted` 可用于隐藏文本选择、暂停昂贵布局或开始记录手势；`ScrollFinished` 可用于恢复选择、吸附到刻度、保存位置。一次序列若只有一个事件，开始与结束语义可能同时成立，代码不能假设它们永远是不同事件。

## 5. 使用场景

`QScrollEvent` 适合触控照片浏览器、地图、时间轴、画布、长列表、工业面板和需要惯性/回弹效果的自定义滚动区域。

对于 `QAbstractScrollArea` 系列，滚动条和 viewport 已经处理大部分场景；只有自己接入 `QScroller` 或做特殊触控交互时才需要直接消费该事件。

## 6. 常见坑与经验

不要把 `contentPos()` 与 `QWheelEvent::pixelDelta()` 混淆。前者是内容的绝对目标位置，后者是本次设备输入的相对增量。

不要忽略 `ScrollFinished`。惯性结束后常需要停止临时渲染策略、吸附刻度或恢复被隐藏的 UI。

不要把 overshoot 当作错误。它是正常的弹性边界信息，尤其在触控滚动中很常见。

不要在收到滚动事件时重新配置 content range。范围应该在 `QScrollPrepareEvent` 中协商；滚动中只有内容尺寸真的改变时才需要重新处理。

## 7. 知识点覆盖

学习 `QScrollEvent` 应覆盖绝对内容坐标、滚动序列、惯性滚动、overshoot、边界回弹、`QScroller`、触控视图更新、吸附逻辑和 wheel delta 区别。
