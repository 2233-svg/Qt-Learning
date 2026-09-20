# QEventPoint

> Qt 6.11.1 · Qt GUI · 来自 `QEventPoint`

## 1. 先建立直觉

`QEventPoint` 是 `QPointerEvent` 中的一个“指针点快照”。鼠标事件通常只有一个点，触摸事件可以有多个点，平板笔事件也会把笔尖当作一个点。每个点独立保存自己的 ID、状态、当前位置、按下位置、上一位置、压力、速度、时间戳和接受状态。

把它理解为“某一根手指或某一个笔尖，在这一帧输入事件中的完整观测结果”最合适。复杂交互不应该只看当前坐标：拖动要看 press position，甩动要看 velocity，长按要看 time held，多指操作要用 point ID 跟踪各点。

## 2. 类说明

`QEventPoint` 是值类型，主要从 `QPointerEvent::points()` 获取。它不拥有设备，也不控制事件分发；它描述一个点在当前事件中的数据。点级接受状态主要服务于 Qt Quick 和高级多点路由，Widgets 常规代码通常以整个 `QPointerEvent` 的接受状态为主。

类说明只用于表明这些 API 来自 `QEventPoint`：设备类型、事件级 modifiers、grabber 列表在 `QPointerEvent` 或更高层类中；单个点的轨迹和物理输入属性在 `QEventPoint`。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `enum State` / `States` | 描述点状态：Unknown、Stationary、Pressed、Updated、Released。 |
| `QEventPoint(id, state, scenePosition, globalPosition)` | 构造一个事件点，主要用于测试、模拟或平台层。 |
| `id() const` | 返回点 ID，用于在一次多点交互期间持续跟踪同一根手指。 |
| `state() const` | 返回当前点状态，决定开始、更新、结束处理。 |
| `position() const` | 返回相对接收对象的当前局部坐标。 |
| `scenePosition() const` | 返回相对窗口或场景的当前坐标。 |
| `globalPosition() const` | 返回当前全局屏幕坐标。 |
| `pressPosition()` / `scenePressPosition()` / `globalPressPosition()` | 返回该点初始按下时的三套坐标。 |
| `lastPosition()` / `sceneLastPosition()` / `globalLastPosition()` | 返回前一个事件中的三套坐标。 |
| `grabPosition()` / `sceneGrabPosition()` / `globalGrabPosition()` | 返回该点被 grab 时的三套坐标。 |
| `timestamp()` | 返回当前事件点时间戳。 |
| `lastTimestamp()` | 返回前一个 pointer 事件对应的时间戳。 |
| `pressTimestamp()` | 返回该点首次按下时的时间戳。 |
| `timeHeld()` | 返回从按下至当前点的持续时间。 |
| `velocity() const` | 返回由 Qt 估算的二维速度向量。 |
| `pressure() const` | 返回压力，通常为 0.0 到 1.0，设备不支持时可能是默认值。 |
| `rotation() const` | 返回工具旋转角度，设备支持时才有意义。 |
| `ellipseDiameters() const` | 返回接触区域椭圆直径，通常仅少数触摸设备提供。 |
| `normalizedPosition() const` | 返回映射到设备可用区域的归一化位置。 |
| `device() const` | 返回产生这个点的 `QPointingDevice`。 |
| `uniqueId() const` | 返回指针设备或工具唯一 ID。 |
| `isAccepted() const` | 查询该点是否被接受。 |
| `setAccepted(bool)` | 设置点级接受状态。 |
| `operator==` / `operator!=` | 比较两个事件点是否相等。 |

## 4. 关键用法

### 用 ID 跟踪多触点，不依赖列表顺序

```cpp
void Whiteboard::handleTouch(QTouchEvent *event)
{
    for (const QEventPoint &point : event->points()) {
        switch (point.state()) {
        case QEventPoint::State::Pressed:
            m_strokes.insert(point.id(), Stroke(point.position()));
            break;
        case QEventPoint::State::Updated:
            m_strokes[point.id()].append(point.position());
            break;
        case QEventPoint::State::Released:
            finishStroke(point.id());
            m_strokes.remove(point.id());
            break;
        default:
            break;
        }
    }
}
```

不要假设 ID 从 0 开始、连续递增，或 `points()` 内的索引永远代表同一个手指。设备驱动与事件合并都可能让这些假设失效。

### 用 press position 判断拖动阈值

```cpp
bool DragRecognizer::hasMovedFarEnough(const QEventPoint &point) const
{
    const qreal distance = QLineF(point.pressPosition(), point.position()).length();
    return distance >= QApplication::startDragDistance();
}
```

`pressPosition()` 比自己缓存第一帧位置更稳，因为它属于 Qt 对该点整个生命周期的统一记录。

### 用 last position 计算增量，用 velocity 处理甩动

```cpp
void MapView::updatePan(const QEventPoint &point)
{
    panBy(point.position() - point.lastPosition());

    if (point.state() == QEventPoint::State::Released
        && point.velocity().length() > 900.0f) {
        startFlick(point.velocity());
    }
}
```

局部增量适合移动内容；速度适合惯性滚动。不要把 `globalPosition() - globalPressPosition()` 误用成单帧位移。

### 多点事件要按状态混合处理

一个 `QTouchEvent` 可能同时包含一个点 `Released`、另一个点 `Updated`。因此 `QPointerEvent::isBeginEvent()` / `isEndEvent()` 只能做粗分流；复杂手势仍要遍历每个 `QEventPoint` 的 `state()`。

### 点级接受主要面向高级路由

```cpp
for (QEventPoint &point : event->points()) {
    if (ownsPoint(point.id()))
        point.setAccepted();
}
```

这个模式主要在 Qt Quick 或自定义输入框架中有意义。纯 Widgets 控件更常见的做法是接受或忽略整个事件，避免混乱地部分接收多个点。

## 5. 坐标、时间与物理量的关系

`position()` 是相对事件接收对象的局部坐标，适合绘制和命中测试；`scenePosition()` 是窗口或场景层坐标，适合跨对象协作；`globalPosition()` 是屏幕坐标，适合移动顶层窗口、弹出原生菜单和跨窗口拖动。

每套坐标又有 current、last、press、grab 四个时刻。current 表示现在，last 表示上一帧，press 表示交互开始，grab 表示分发目标获得该点时。只要先确定“相对哪个对象”和“哪个时刻”，就不容易选错 API。

时间戳与 `timeHeld()` 用于长按、采样率和速度判断。它们适合计算相对时间，不应解释为现实世界日期时间。`velocity()` 是 Qt 基于事件序列估算的结果，适合交互动画，不应被当作精密物理传感器读数。

压力、旋转、接触椭圆、归一化位置等属于可选硬件能力。使用前应结合 `device()->hasCapability()` 判断，并给不支持设备准备合理默认值。

## 6. 使用场景

`QEventPoint` 是多指绘制、双指缩放旋转、地图平移、画布框选、触控白板、平板笔笔刷、签名、惯性列表和游戏手势的基础。

它也适合手势识别器。用 `pressPosition()` 判断点击或拖动，用 `timeHeld()` 判断长按，用 `velocity()` 判断 flick，用两个或多个点的 current/last 坐标计算缩放、旋转和平移。

在调试输入异常时，记录 ID、state、position、press position、pressure 和 device 是非常高效的方式。它能揭示问题是点状态转移错、坐标系错，还是设备本身没有报告预期能力。

## 7. 常见坑与经验

不要保存对事件中 `QEventPoint` 的引用、指针或迭代器到事件处理函数之外。需要长期轨迹时，复制所需的数据到自己的模型。

不要把 `Stationary` 当成无意义数据。多点触摸事件中，静止点仍然是当前手势的一部分，计算双指中心或缩放比例时可能需要它。

不要假设压力为 0 就表示事件无效。鼠标与不支持压力的设备可能给默认值；应先看 capability 和状态。

不要混淆 `id()` 与 `uniqueId()`。前者识别一次交互中的一个点，后者识别设备或工具来源。

不要只以点级 accepted 判断 Widgets 事件是否处理完成。在 Widgets 中，优先观察整个 pointer event 的接受策略。

## 8. 知识点覆盖

学习 `QEventPoint` 应覆盖多触点 ID、点状态机、局部/场景/全局坐标、按下/上一帧/grab 坐标、时间戳、长按、速度、压力、旋转、接触面积、归一化位置、点级接受、设备能力、手势识别与 Qt 6 指针事件模型。
