# QScroller

> Qt 6.11.1 · Qt Widgets · 来自 `QScroller`

## 1. 先建立直觉

`QScroller` 给 QObject/Widget 目标添加“手指一拨还能继续滑”的动力学滚动。它把按下、拖动、释放转换成带速度、减速、吸附和越界效果的滚动过程。

它不是滚动区域本身，也不保存内容。目标对象仍然需要能响应滚动准备和滚动事件，或者本身是 Qt 支持的可滚动控件。`QScroller` 负责手势识别和滚动动画，内容如何移动由目标配合完成。

## 2. 类说明

`QScroller` 继承自 `QObject`。通常通过 `QScroller::grabGesture(target, gestureType)` 给目标对象安装滚动手势，再用 `QScroller::scroller(target)` 取得对应 scroller 调整属性或控制滚动。

它有状态机：Inactive、Pressed、Dragging、Scrolling。应用可以监听状态变化，做滚动中隐藏复杂装饰、停止视频缩略图加载、或在滚动结束后恢复细节绘制。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `grabGesture(QObject *, ScrollerGestureType)` | 给目标安装触摸或鼠标拖拽滚动手势。 |
| `ungrabGesture(QObject *)` | 移除目标上的 scroller 手势。 |
| `grabbedGesture(QObject *)` | 查询目标当前被安装的滚动手势类型。 |
| `scroller(QObject *)` | 获取目标对应的 scroller。 |
| `hasScroller(QObject *)` | 判断目标是否已有 scroller。 |
| `activeScrollers()` | 返回当前活动的 scroller 列表。 |
| `state()` | 读取滚动状态：Inactive、Pressed、Dragging、Scrolling。 |
| `velocity()` | 当前滚动速度。 |
| `finalPosition()` | 按当前速度和属性预估最终位置。 |
| `scrollTo(QPointF, int)` | 程序化滚动到指定位置，可带动画时间。 |
| `ensureVisible(QRectF, margins, time)` | 滚动到让某个区域可见。 |
| `stop()` | 停止当前滚动。 |
| `handleInput(Input, QPointF, timestamp)` | 手动喂输入事件，适合自定义目标。 |
| `setSnapPositionsX/Y(...)` | 设置吸附位置，适合分页或卡片列表。 |
| `setScrollerProperties()` / `scrollerProperties()` | 设置或读取滚动手感参数。 |
| `stateChanged(State)` | 滚动状态变化时发出。 |

## 4. 关键用法

给滚动区域 viewport 启用触摸滚动：

```cpp
QScroller::grabGesture(scrollArea->viewport(), QScroller::TouchGesture);
```

允许鼠标左键拖动滚动，常用于触屏风格桌面界面：

```cpp
QScroller::grabGesture(listView->viewport(), QScroller::LeftMouseButtonGesture);
```

调整属性：

```cpp
auto *scroller = QScroller::scroller(listView->viewport());
QScrollerProperties props = scroller->scrollerProperties();
props.setScrollMetric(QScrollerProperties::OvershootDragDistanceFactor, 0.15);
scroller->setScrollerProperties(props);
```

## 5. 使用场景

适合触摸屏列表、平板上的设置页、图片缩略图网格、触控大屏时间线、可拖动滚动的文件浏览器，以及需要更自然滚动手感的 kiosk 或嵌入式界面。

如果应用主要是鼠标滚轮和键盘操作，标准滚动条已经足够。强行启用左键拖动滚动可能会和选择文本、拖拽 item、框选冲突。

## 6. 常见坑与经验

安装目标常常应该是 viewport，而不是外层 view。比如 `QListView`、`QScrollArea` 这类控件真正接收内容输入的是 viewport。

左键拖动滚动会改变鼠标交互语义。列表项点击、拖拽排序、文本选择都可能受影响，要按场景测试。

`QScroller` 的手感由 `QScrollerProperties` 决定。不要靠定时器手搓惯性滚动；先调属性，必要时再手动处理输入。
