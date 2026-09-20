# Qt QGraphicsView 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）
> 头文件：`#include <QGraphicsView>`
> 所属模块：`Qt6::Widgets`
> 继承：`QAbstractScrollArea -> QGraphicsView`
> 常见搭档：`QGraphicsScene`

## 1. QGraphicsView 解决什么问题

`QGraphicsView` 是图形视图架构里的“观察窗口”。它负责把 `QGraphicsScene` 里的内容显示出来，并把鼠标、键盘、滚轮等输入转成场景事件。

它解决的是“如何看、如何缩放、如何拖动、如何把场景导出”的问题，不负责保存图元数据。

适合场景：

- 大画布浏览；
- 缩放和平移；
- 节点图/流程图视图；
- 场景导出到图片或打印；
- 需要做橡皮筋选择和命中测试的画布。

## 2. 最小可用代码

```cpp
#include <QApplication>
#include <QGraphicsScene>
#include <QGraphicsView>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    auto *scene = new QGraphicsScene;
    scene->addText("Hello, graphics view");
    scene->setSceneRect(-100, -100, 400, 300);

    QGraphicsView view(scene);
    view.show();

    return app.exec();
}
```

`QGraphicsView` 不拥有 scene。  
你把 scene 换掉，旧 scene 也不会因为 `setScene()` 自动删除。

## 3. 视图和场景的边界

```cpp
view.setScene(scene);
QGraphicsScene *current = view.scene();
```

`setScene()` 只是接入一个场景，不会接管它的所有权。  
这点和 `QGraphicsScene::addItem()` 接管 item 的语义不同，别混。

场景内容怎么显示，由这些属性控制：

- `backgroundBrush`
- `foregroundBrush`
- `renderHints`
- `viewportUpdateMode`
- `cacheMode`
- `dragMode`
- `interactive`

## 4. 缩放、定位和可见性

```cpp
view.centerOn(point);
view.ensureVisible(rect);
view.fitInView(rect, Qt::KeepAspectRatio);
view.scale(1.25, 1.25);
view.rotate(15);
view.resetTransform();
```

### 4.1 centerOn

把目标点或 item 放到视口中央。  
适合定位当前对象。

### 4.2 ensureVisible

只保证目标进入视口，不要求居中。  
比 `centerOn()` 更温和。

### 4.3 fitInView

把场景区域缩放到刚好塞进视口。  
常用于打开文件时自动适配全图。

注意：在 `resizeEvent()` 里直接反复调用 `fitInView()` 可能引起滚动条状态变化和递归，要小心。

## 5. 交互模式

```cpp
view.setInteractive(true);
view.setDragMode(QGraphicsView::ScrollHandDrag);
view.setRubberBandSelectionMode(Qt::IntersectsItemShape);
```

- `interactive`：是否允许 item 接收交互；
- `dragMode`：拖动方式；
- `ScrollHandDrag`：手型拖动画布；
- `RubberBandDrag`：橡皮筋选择；
- `NoDrag`：不启用拖动。

`rubberBandChanged` 信号能拿到框选矩形和场景坐标，做自定义框选提示很方便。

## 6. 坐标映射

```cpp
QPointF scenePos = view.mapToScene(viewPos);
QPoint viewPos2 = view.mapFromScene(scenePos);
QList<QGraphicsItem *> hits = view.items(viewPos);
QGraphicsItem *item = view.itemAt(viewPos);
```

这是 `QGraphicsView` 的真正强项之一：  
把视口坐标和场景坐标来回转换，做命中测试、工具提示和定位都靠它。

## 7. 绘制和性能

```cpp
view.setRenderHints(QPainter::Antialiasing | QPainter::SmoothPixmapTransform);
view.setCacheMode(QGraphicsView::CacheBackground);
view.setViewportUpdateMode(QGraphicsView::MinimalViewportUpdate);
view.setOptimizationFlag(QGraphicsView::DontSavePainterState, true);
```

`drawBackground()` 和 `drawForeground()` 是自定义背景/前景的主要重写点。  
如果只是想设背景色或纹理，优先用 `setBackgroundBrush()`。

`viewportUpdateMode` 和 `optimizationFlags` 直接影响大场景性能，尤其是图元很多时。

## API 速查表
### 8.1 构造、场景和视口基础属性

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `ViewportAnchor` | 指定缩放或视图尺寸变化时，哪个位置保持稳定。 | `AnchorUnderMouse` 适合鼠标滚轮缩放；`AnchorViewCenter` 适合程序化缩放。 |
| 类型 | `DragMode` | 指定鼠标拖动是禁用、手型滚动画布还是橡皮筋框选。 | `RubberBandDrag` 主要负责选择框，图元自身拖动仍由 item 交互处理。 |
| 类型 | `ViewportUpdateMode` | 指定视口重绘区域的计算策略。 | 更新越精细不一定越快，大量动态 item 要结合实际场景测试。 |
| 类型 | `CacheMode` | 指定视图是否缓存背景。 | `CacheBackground` 适合背景复杂且变化少的视图；动态背景缓存反而会增加开销。 |
| 类型 | `OptimizationFlags` | 控制保存 painter 状态、抗锯齿调整等绘制优化。 | 只有确认所有 item 都能适应该假设时才开启激进优化。 |
| 构造 | `QGraphicsView(QWidget *parent = nullptr)` | 创建没有绑定场景的视图。 | 后续通过 `setScene()` 连接场景；视图本身仍然可以先配置。 |
| 构造 | `QGraphicsView(QGraphicsScene *, QWidget *parent = nullptr)` | 创建视图并立即绑定场景。 | 最常用写法；场景所有权仍不转移给视图。 |
| 析构 | `~QGraphicsView()` | 销毁视图和其 viewport。 | 不会删除 `QGraphicsScene`，场景的生命周期要由父对象或调用方管理。 |
| 尺寸 | `sizeHint()` | 向外层布局提供视图推荐尺寸。 | 视图太小时滚动条和场景可见区域会受限。 |
| 场景 | `scene()` / `setScene(QGraphicsScene *)` | 读取或替换视图正在显示的场景。 | `setScene()` 不接管场景所有权；替换前要确认旧场景是否还被其他视图使用。 |
| 范围 | `sceneRect()` / `setSceneRect(...)` | 指定视图滚动和显示时采用的场景范围。 | 未设置时可能使用场景的范围；它不等同于 viewport 的像素矩形。 |
| 对齐 | `alignment()` / `setAlignment(...)` | 控制场景内容小于视口时如何对齐。 | 常用于让小场景居中、靠左上或保持特定阅读方向。 |

### 8.2 绘制、缓存和交互

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 绘制提示 | `renderHints()` / `setRenderHint(...)` / `setRenderHints(...)` | 读取或设置抗锯齿、平滑变换等 `QPainter` 绘制提示。 | 抗锯齿会增加绘制成本；像素编辑器通常不希望打开它。 |
| 背景 | `backgroundBrush()` / `setBackgroundBrush(...)` | 设置视图绘制在场景后面的背景画刷。 | 简单纯色、纹理背景优先用它；复杂背景重写 `drawBackground()`。 |
| 前景 | `foregroundBrush()` / `setForegroundBrush(...)` | 设置覆盖在场景内容上方的前景画刷。 | 可用于统一遮罩或简单辅助层；复杂辅助线更适合重写 `drawForeground()`。 |
| 交互 | `isInteractive()` / `setInteractive(bool)` | 开关视图把鼠标、键盘等事件交给场景 item 处理的能力。 | 关闭后仍可浏览、缩放和映射坐标，但 item 不再按正常方式交互。 |
| 拖动 | `dragMode()` / `setDragMode(...)` | 读取或设置滚动画布、框选等视图级拖动模式。 | 手型拖动与 item 的 `ItemIsMovable` 是两套机制，不要混为一谈。 |
| 框选 | `rubberBandSelectionMode()` / `setRubberBandSelectionMode(...)` | 设置橡皮筋框选采用相交、完全包含等命中规则。 | 只有启用 `RubberBandDrag` 时才会直接影响用户框选。 |
| 框选 | `rubberBandRect()` | 读取当前橡皮筋框的 viewport 矩形。 | 需要把它换算成场景坐标时使用 `mapToScene()`。 |
| 缓存 | `cacheMode()` / `setCacheMode(...)` | 读取或设置视图缓存策略。 | 改变场景背景后必要时调用 `resetCachedContent()`。 |
| 缓存 | `resetCachedContent()` | 清空视图缓存并要求重新生成。 | 只在缓存内容确实已经过期时调用，频繁调用会抵消缓存收益。 |
| 更新 | `viewportUpdateMode()` / `setViewportUpdateMode(...)` | 控制 viewport 发生变化时重绘哪些区域。 | 动态图元、半透明效果和 OpenGL viewport 下的最佳值可能不同。 |
| 优化 | `optimizationFlags()` / `setOptimizationFlag(...)` / `setOptimizationFlags(...)` | 读取或设置绘制优化标志。 | `DontSavePainterState` 要求 item 自己正确恢复 painter 状态。 |

### 8.3 变换、定位和可见性

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 锚点 | `transformationAnchor()` / `setTransformationAnchor(...)` | 设置缩放、旋转等变换围绕 viewport 中哪个位置保持。 | 交互缩放通常选鼠标下方；否则用户会感觉内容“漂移”。 |
| 锚点 | `resizeAnchor()` / `setResizeAnchor(...)` | 设置视图尺寸变化时场景的锚定位置。 | 影响窗口拉伸后用户看到的区域，不是场景本身的坐标变化。 |
| 变换 | `transform()` / `setTransform(..., bool combine)` | 读取或整体设置视图到场景的变换矩阵。 | `combine = true` 会叠加到现有变换；需要完全重置时用 `resetTransform()`。 |
| 变换 | `viewportTransform()` | 读取包含滚动和视图变换在内的 viewport 变换矩阵。 | 需要精确理解绘制坐标时使用，普通缩放代码通常只需 `transform()`。 |
| 变换 | `isTransformed()` | 判断当前是否存在非默认变换。 | 可用于决定是否显示缩放比例或启用重置按钮。 |
| 变换 | `resetTransform()` | 把视图变换恢复为单位矩阵。 | 不会删除场景，也不会改变 item 的自身变换。 |
| 变换 | `scale(sx, sy)` | 在当前变换上叠加缩放。 | 连续调用会累积；缩放控件通常需要限制最小/最大比例。 |
| 变换 | `rotate(angle)` | 在当前变换上叠加旋转。 | 旋转的是观察方式，不是直接修改场景 item。 |
| 变换 | `shear(sh, sv)` | 在当前变换上叠加错切。 | 一般用于特殊绘制效果，普通编辑器很少需要。 |
| 变换 | `translate(dx, dy)` | 在当前变换上叠加平移。 | 视图平移与滚动条语义不同，交互画布通常优先使用滚动或拖拽。 |
| 定位 | `centerOn(const QPointF &)` / `centerOn(const QGraphicsItem *)` | 让坐标点或 item 的中心进入视口中央。 | 适合“定位到当前对象”；不需要居中时用 `ensureVisible()`。 |
| 可见性 | `ensureVisible(const QRectF &, margins)` / `ensureVisible(const QGraphicsItem *, margins)` | 确保矩形或 item 进入可见区域。 | 只保证可见，不保证居中；边距是 viewport 像素边距。 |
| 适配 | `fitInView(const QRectF &, Qt::AspectRatioMode)` / `fitInView(const QGraphicsItem *, ...)` | 缩放视图，使目标内容尽量填满 viewport。 | 在 `resizeEvent()` 中使用时要防止滚动条变化导致反复触发；目标为空或尺寸为零时也要处理。 |

### 8.4 命中测试、坐标映射和导出

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 命中 | `items()` | 返回当前视图可命中的所有图元。 | 返回顺序通常体现绘制层级；适合调试或实现自定义选择工具。 |
| 命中 | `items(const QPoint &, ...)` | 查询 viewport 某个点下的图元。 | 传入的是 viewport 坐标，不是场景坐标。 |
| 命中 | `items(const QRect &, Qt::ItemSelectionMode)` | 查询 viewport 矩形内命中的图元。 | 框选工具常用；相交和完全包含的结果不同。 |
| 命中 | `items(const QPolygon &, ...)` / `items(const QPainterPath &, ...)` | 按任意多边形或路径查找图元。 | 适合套索选择；仍要明确命中模式。 |
| 命中 | `itemAt(const QPoint &)` | 返回 viewport 指定点下最上层的图元。 | 常用于鼠标点击、工具提示和右键菜单；坐标必须是 viewport 坐标。 |
| 映射 | `mapToScene(...)` | 把 viewport 中的点、矩形、多边形或路径换算成场景坐标。 | 鼠标事件位置通常先通过它转换，再交给场景业务逻辑。 |
| 映射 | `mapFromScene(...)` | 把场景中的点、矩形、多边形或路径换算成 viewport 坐标。 | 画辅助 UI、定位浮层或判断屏幕范围时使用。 |
| 导出 | `render(QPainter *, target, source, aspectRatioMode)` | 把视图内容绘制到任意 `QPainter`。 | 与 `QGraphicsScene::render()` 不同，它包含视图的变换和可见范围语义。 |

### 8.5 场景更新、绘制钩子和信号

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 更新 | `updateScene(const QList<QRectF> &)` | 通知视图指定的场景区域需要更新。 | 场景通常会自动发起更新，手动调用多用于自定义刷新流程。 |
| 失效 | `invalidateScene(const QRectF &, QGraphicsScene::SceneLayers)` | 让场景指定区域的某些层失效并重绘。 | 自定义场景背景、前景或缓存层时使用。 |
| 范围更新 | `updateSceneRect(const QRectF &)` | 更新视图内部记录的场景范围。 | 它不等价于修改 `QGraphicsScene::sceneRect()`；要改变真实场景边界应改场景对象。 |
| 背景钩子 | `drawBackground(QPainter *, const QRectF &)` | 自定义视图背景绘制。 | 重写时只绘制给定矩形，避免每次重画整个无限画布。 |
| 前景钩子 | `drawForeground(QPainter *, const QRectF &)` | 自定义视图前景绘制。 | 适合网格、十字光标、辅助线和选择覆盖层。 |
| 图元钩子 | `drawItems(...)` | 介入视图批量绘制图元的过程。 | 这是低层定制接口，除非需要特殊渲染管线，否则优先让场景和 item 自己绘制。 |
| 信号 | `rubberBandChanged(QRect, QPointF, QPointF)` | 通知橡皮筋框变化及其起止场景坐标。 | 适合显示自定义选择信息；功能受 Qt 的 rubberband 配置影响。 |

### 一句话总结

`QGraphicsView` 是“把场景看见并操控起来”的窗口：缩放、平移、框选、映射坐标和导出，都是它的活。
