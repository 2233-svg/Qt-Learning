# QScrollPrepareEvent

> Qt 6.11.1 · Qt GUI · 来自 `QScrollPrepareEvent`

## 1. 先建立直觉

`QScrollPrepareEvent` 是 `QScroller` 开始一次触控/惯性滚动前发出的协商事件。滚动器知道用户从哪里开始拖动，但不知道目标控件的内容坐标、内容边界和视口尺寸；控件必须在事件里把这些信息填回去。

可以把它看成滚动协议的“初始化握手”：`QScrollPrepareEvent` 声明可滚动范围，后续 `QScrollEvent` 才持续报告新的内容位置和越界距离。

## 2. 类说明

`QScrollPrepareEvent` 继承自 `QEvent`，常与 `QScroller` 协作。自定义滚动控件通常在 `event()` 中处理 `QEvent::ScrollPrepare`。

类说明只用于表明这些 API 来自 `QScrollPrepareEvent`：滚动动画、手势识别和惯性参数由 `QScroller` 管理；内容位置和边界由控件自己的模型决定。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QScrollPrepareEvent(startPos)` | 构造滚动协商事件，传入触摸或鼠标起始位置。 |
| `startPos() const` | 返回触发本次滚动的局部起始位置。 |
| `setViewportSize(size)` | 设置可视区域大小。 |
| `viewportSize() const` | 读取已设置的视口大小。 |
| `setContentPos(pos)` | 设置滚动开始时内容当前位置。 |
| `contentPos() const` | 读取已设置的内容当前位置。 |
| `setContentPosRange(rect)` | 设置内容位置可移动的合法范围。 |
| `contentPosRange() const` | 读取已设置的内容位置范围。 |

## 4. 关键用法

### 为自定义画布声明滚动边界

```cpp
bool CanvasView::event(QEvent *event)
{
    if (event->type() == QEvent::ScrollPrepare) {
        auto *prepare = static_cast<QScrollPrepareEvent *>(event);

        const QSizeF viewport = size();
        const QSizeF content = m_documentSize;
        const QPointF current = m_contentOffset;

        prepare->setViewportSize(viewport);
        prepare->setContentPos(current);
        prepare->setContentPosRange(QRectF(
            QPointF(0, 0),
            QSizeF(qMax<qreal>(0, content.width() - viewport.width()),
                   qMax<qreal>(0, content.height() - viewport.height()))));
        prepare->accept();
        return true;
    }

    return QWidget::event(event);
}
```

坐标定义必须一致：`contentPos` 和 `contentPosRange` 都应使用同一内容坐标系，不能一个用滚动条值、一个用场景坐标。

### 视口与内容大小变化后重新协商

控件 resize、缩放比例改变、文档内容加载完成时，下一次滚动前需要给出新的边界。不要把初始范围永久缓存为常量，否则滚动器会允许越界或无法滚到新内容。

## 5. 使用场景

`QScrollPrepareEvent` 适合自定义触控画布、照片查看器、地图、时间轴、无限或大尺寸内容视图、没有使用 `QAbstractScrollArea` 的自定义滚动控件。

普通 `QScrollArea`、`QListView`、`QTextEdit` 已有完整滚动实现，通常不需要直接处理它。

## 6. 常见坑与经验

不要只设置 viewport size 而忘记 content position range。没有边界，`QScroller` 无法正确限制或计算 overshoot。

不要把 `startPos()` 当成内容位置。它是用户指针在控件里的起点，主要用于需要按起点决定滚动行为的场景。

不要在 prepare 事件里真正移动内容。这里负责声明初始状态，实际位置变化由后续 `QScrollEvent` 处理。

不要把视口宽高和内容宽高倒置。`viewportSize` 是看得见的区域，range 是内容位置可以变化的范围。

## 7. 知识点覆盖

学习 `QScrollPrepareEvent` 应覆盖 `QScroller`、滚动协商、内容坐标、视口大小、内容边界、触控拖动、惯性滚动、overshoot 和自定义滚动控件设计。
