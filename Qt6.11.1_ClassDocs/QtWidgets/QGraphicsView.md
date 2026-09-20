# QGraphicsView

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsView`

## 1. 先建立直觉

`QGraphicsView` 是 `QGraphicsScene` 的可视窗口。场景里有什么、item 在哪里，由 scene 管；用户看到哪一块、缩放多少、如何滚动、如何把坐标从屏幕映射到场景，由 view 管。

一个 scene 可以同时挂多个 view：一个主编辑视图、一个缩略导航视图、一个只读预览视图。每个 view 都能有自己的 transform、滚动条和渲染设置。

## 2. 类说明

`QGraphicsView` 继承自 `QAbstractScrollArea`，内部有 viewport。它把场景渲染到 viewport 上，并把鼠标键盘事件转发给 scene 和 item。

它的核心能力有三类：视图变换（缩放、旋转、平移）、交互模式（拖拽滚屏、框选）、渲染优化（抗锯齿、缓存、更新模式、优化标志）。做复杂画布时，view 的配置往往决定体验是否顺手。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `setScene()` / `scene()` | 绑定或读取要显示的场景。 |
| `mapToScene()` / `mapFromScene()` | 在视图/viewport 坐标和场景坐标之间转换。 |
| `centerOn()` | 让某个场景点或 item 居中显示。 |
| `ensureVisible()` | 滚动到让某个区域或 item 可见。 |
| `fitInView()` | 调整变换使指定区域适配视口。 |
| `scale()` / `rotate()` / `translate()` | 修改视图变换。 |
| `setTransform()` / `transform()` | 设置或读取完整变换矩阵。 |
| `resetTransform()` | 重置缩放/旋转等视图变换。 |
| `setDragMode()` | 设置无拖拽、滚屏拖拽或橡皮筋选择。 |
| `setRenderHint()` / `renderHints()` | 控制抗锯齿、平滑 pixmap 等绘制提示。 |
| `setViewportUpdateMode()` | 控制局部/全量更新策略，影响性能和正确性。 |
| `setCacheMode()` | 缓存背景，适合复杂静态背景。 |
| `setOptimizationFlag()` | 调整绘制优化行为，高级性能调优用。 |
| `items()` / `itemAt()` | 从视图坐标查询当前可见或命中的 item。 |
| `render(QPainter *)` | 把视图内容渲染到打印机、图片或其他 paint device。 |

## 4. 关键用法

```cpp
auto *scene = new QGraphicsScene(this);
auto *view = new QGraphicsView(scene, this);

view->setRenderHint(QPainter::Antialiasing, true);
view->setDragMode(QGraphicsView::RubberBandDrag);
view->setTransformationAnchor(QGraphicsView::AnchorUnderMouse);
```

滚轮缩放通常写在子类里：

```cpp
void DiagramView::wheelEvent(QWheelEvent *event)
{
    const qreal factor = event->angleDelta().y() > 0 ? 1.15 : 1.0 / 1.15;
    scale(factor, factor);
}
```

命中测试时使用 view 坐标：

```cpp
if (auto *item = itemAt(event->pos()))
    selectOrOpen(item);
```

## 5. 使用场景

适合图形编辑器、节点画布、流程图、地图/平面图、图片标注、机器人路径可视化、网络拓扑和任何需要平移缩放交互的 2D 场景。

如果只需要显示固定数量普通控件，不要用 Graphics View 装 QWidget；普通布局更自然。Graphics View 的优势在 item 数量、坐标变换和图元交互。

## 6. 常见坑与经验

视图坐标、场景坐标、item 坐标是三套体系。很多“点击不准”“缩放后拖动错位”都来自坐标没映射。

`fitInView()` 不适合在每次 resize 中无脑调用而不控制条件，否则用户手动缩放会被窗口变化重置。

性能问题先看 item 的 `boundingRect()` 和 scene 索引，再看 view 更新模式。错误的 item 边界会让局部重绘失效，比关抗锯齿更致命。
