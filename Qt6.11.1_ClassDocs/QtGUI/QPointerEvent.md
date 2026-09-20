# QPointerEvent

> Qt 6.11.1 · Qt GUI · 来自 `QPointerEvent`

## 1. 先建立直觉

`QPointerEvent` 是 Qt 6 统一指针输入模型的核心类。这里的“pointer”不是 C++ 指针，而是“能指向屏幕上某个位置的输入设备”：鼠标、触摸点、触摸板、手写笔、橡皮擦端等都属于这个范围。

它解决的问题是：过去鼠标事件、触摸事件、平板笔事件各有一套坐标和状态字段，复杂应用很难用一套逻辑处理。`QPointerEvent` 把这些事件抽象成“一个设备产生了一个或多个 `QEventPoint`”，再由 `QMouseEvent`、`QTouchEvent`、`QTabletEvent` 等子类提供更具体的语义。

## 2. 类说明

`QPointerEvent` 继承自 `QInputEvent`，直接派生类包括 `QSinglePointEvent` 和 `QTouchEvent`。它主要暴露触点列表、设备信息、指针类型以及事件点的 grabber 关系。

对 Widgets 应用来说，你多数时候会直接处理 `QMouseEvent`、`QWheelEvent` 或 `QTouchEvent`；但一旦要做跨设备绘制、手势识别、多触点编辑、Qt Quick 与 Widgets 混合输入分析，`QPointerEvent` 的模型就非常重要。

最值得建立的概念是：一个 pointer 事件可以包含多个点，每个点可以有自己的位置、状态、接受情况和抓取对象。不要把它想成“只有一个坐标的鼠标事件”。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `points() const` | 取得本次事件包含的所有 `QEventPoint`。 |
| `point(qsizetype i)` | 按索引取得可修改的事件点引用，适合底层输入处理器使用。 |
| `pointById(int id)` | 按触点 ID 查找事件点，常用于多触点跟踪。 |
| `pointCount() const` | 返回事件点数量，鼠标通常是 1，触摸可能大于 1。 |
| `pointingDevice() const` | 取得更具体的 `QPointingDevice`，比 `QInputDevice` 更适合指针设备分析。 |
| `pointerType() const` | 判断指针形态，例如普通指针、手写笔、橡皮擦等。 |
| `allPointsAccepted() const` | 判断所有事件点是否都已被接受。 |
| `setAccepted(bool)` | 设置整个事件的接受状态，并影响点级接受逻辑。 |
| `allPointsGrabbed() const` | 判断所有点是否都已被独占或被动抓取。 |
| `exclusiveGrabber(point) const` | 查询某个点当前的独占抓取对象。 |
| `setExclusiveGrabber(point, object)` | 为某个点设置后续事件的独占接收者。 |
| `passiveGrabbers(point) const` | 查询某个点的被动抓取对象列表。 |
| `addPassiveGrabber(point, object)` | 为某个点添加被动抓取对象。 |
| `removePassiveGrabber(point, object)` | 移除某个点的被动抓取对象。 |
| `clearPassiveGrabbers(point)` | 清空某个点的被动抓取对象。 |

## 4. 关键用法

### 用 `points()` 建立多触点逻辑

触摸事件最自然的处理方式不是只读第一个点，而是根据点数量决定交互模式。

```cpp
bool Canvas::handlePointerEvent(QPointerEvent *event)
{
    if (event->pointCount() == 1) {
        const QEventPoint &p = event->points().first();
        updateStroke(p.position(), p.pressure());
        event->accept();
        return true;
    }

    if (event->pointCount() == 2) {
        updatePinchGesture(event->points());
        event->accept();
        return true;
    }

    return false;
}
```

鼠标事件也可以进入这个模型，只是点数量通常为 1。这个统一性是 Qt 6 输入模型相比 Qt 5 更值得利用的地方。

### 用 `pointingDevice()` 和 `pointerType()` 区分笔、鼠标和橡皮擦

绘图、批注、白板应用里，手写笔的笔尖和橡皮擦端往往需要进入完全不同的工具。

```cpp
void PaintTool::handlePointer(QPointerEvent *event)
{
    if (event->pointerType() == QPointingDevice::PointerType::Eraser) {
        eraseAt(event->points().first().position());
        event->accept();
        return;
    }

    drawWithDevice(event->pointingDevice(), event->points().first());
}
```

如果只按鼠标按钮判断，平板笔的一些能力会被浪费；如果只按设备类型判断，又可能漏掉同一设备上的不同端。

### 理解 grabber：谁能继续收到这个点的后续事件

`exclusiveGrabber()` 和 passive grabber 主要服务 Qt 的输入分发机制，尤其是 Qt Quick。它们描述“某个事件点后续更新应该继续送给谁”。独占抓取者像是拖拽过程中锁定的目标；被动抓取者则像旁听者，可以继续收到相关更新但不阻止正常分发。

Widgets 业务代码一般不需要主动设置这些 grabber。除非你在写输入框架、嵌入 Qt Quick、或实现非常底层的触点路由，否则把它们当成诊断和高级机制理解即可。

## 5. 使用场景

`QPointerEvent` 适合做跨设备交互抽象：画布、地图、CAD 视图、时间轴编辑器、音乐控制面板、触控大屏应用，都可以把鼠标、触摸和笔输入汇总到同一套处理逻辑里。

它也适合做多点手势的前置分析。比如一个控件既支持单指绘制，又支持双指缩放旋转，就可以先读取 `pointCount()` 和每个 `QEventPoint` 的状态，再决定交给绘制工具还是手势工具。

在调试输入问题时，`QPointerEvent` 能帮助你确认事件到底来自哪个 `QPointingDevice`、包含几个点、是不是已经被某个对象抓取。这比只看 `event->type()` 更接近真实原因。

## 6. 常见坑与经验

不要假设 pointer 事件只有一个点。`QSinglePointEvent` 的子类可以这样理解，但 `QTouchEvent` 明确可能包含多个点。

不要把事件级 `accepted` 和点级接受状态混为一谈。多触点事件里，一个点被某个对象处理，另一个点可能仍需要继续分发；这也是 `allPointsAccepted()` 存在的意义。

不要随意调用 grabber 修改函数。它们看起来像普通公开 API，但实际更偏向 Qt 内部和高级输入分发场景。常规控件只要正确 `accept()` / `ignore()` 即可。

不要长期保存 `QEventPoint &` 或 `QEventPoint *`。事件对象生命周期结束后，这些引用和指针也就失效了；需要记录轨迹时，复制坐标、压力、ID 和状态等数据。

## 7. 知识点覆盖

学习 `QPointerEvent` 应覆盖 Qt 6 指针输入统一模型、`QEventPoint`、多触点状态、输入设备能力、指针类型、事件接受策略、事件抓取机制、Qt Quick 输入路由、Widgets 触摸支持以及鼠标事件与触摸事件的关系。它是理解现代 Qt 输入系统的关键节点。
