# QGraphicsScene

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsScene`

## 1. 先建立直觉

`QGraphicsScene` 是 Graphics View 框架里的“场景世界”。它保存 item、管理坐标、选择、焦点、碰撞检测、事件分发和索引；真正把场景显示到屏幕上的是 `QGraphicsView`。

可以把三者分清：`QGraphicsScene` 管数据和交互世界，`QGraphicsView` 管视口显示和滚动缩放，`QGraphicsItem` 是场景里的对象。写复杂画布时，这个分层比 API 名字本身更重要。

## 2. 类说明

`QGraphicsScene` 继承自 `QObject`。它本身不是 widget，可以被多个 view 同时观察。一个场景可显示在主视图、缩略图视图、打印视图中，每个 view 可以有不同缩放和变换。

场景负责把鼠标、键盘、拖放、上下文菜单等事件路由给合适的 item，也负责维护选择集合、焦点 item、scene rect 和绘制背景/前景。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `addItem(QGraphicsItem *)` | 把已有 item 加入场景，场景接管其场景归属。 |
| `addRect/addEllipse/addLine/addPath/addPixmap/addText` | 快速创建常见图元并加入场景。 |
| `removeItem(QGraphicsItem *)` | 从场景移除 item，但不删除对象。 |
| `clear()` | 清空场景并删除场景拥有的 item。 |
| `items()` / `itemAt()` | 查询全部 item 或指定位置 item。 |
| `selectedItems()` | 返回当前选中 item 列表。 |
| `setSceneRect()` / `sceneRect()` | 设置场景逻辑边界，影响 view 滚动范围。 |
| `setItemIndexMethod()` | 配置 item 索引方式，大量 item 时影响查询性能。 |
| `setFocusItem()` / `focusItem()` | 设置或读取键盘焦点 item。 |
| `setBackgroundBrush()` / `drawBackground()` | 设置或自定义背景绘制。 |
| `setForegroundBrush()` / `drawForeground()` | 设置或自定义前景绘制。 |
| `invalidate()` / `update()` | 请求重绘指定区域。 |
| `collidingItems()` | 查询与某 item 碰撞的其他 item。 |
| `views()` | 返回观察该场景的所有 `QGraphicsView`。 |
| `changed()` | 场景区域变化时发出。 |
| `selectionChanged()` | 选择集合变化时发出。 |

## 4. 关键用法

```cpp
auto *scene = new QGraphicsScene(this);
scene->setSceneRect(-500, -500, 1000, 1000);

auto *item = scene->addRect(QRectF(-40, -20, 80, 40),
                            QPen(Qt::black), QBrush(Qt::yellow));
item->setFlags(QGraphicsItem::ItemIsMovable | QGraphicsItem::ItemIsSelectable);

auto *view = new QGraphicsView(scene, this);
```

场景坐标和视图坐标要分清。鼠标事件进入 item 时通常已经是 item/scene 相关坐标；从 view 手动查询场景对象时常用：

```cpp
const QPointF scenePos = view->mapToScene(mousePos);
auto *hit = scene->itemAt(scenePos, view->transform());
```

## 5. 使用场景

适合节点编辑器、流程图、图形标注、CAD 简化视图、图片批注、拓扑图、时间轴、2D 游戏编辑器、可拖拽设计器，以及需要大量独立图元交互的界面。

如果只是画一张静态图，重写 `QWidget::paintEvent()` 可能更简单；如果需要上万图元、选择、拖动、碰撞和缩放，`QGraphicsScene` 的结构更划算。

## 6. 常见坑与经验

`removeItem()` 不删除 item。移除后如果没有其他所有者，需要你自己 `delete`，否则会泄漏。

`sceneRect` 不是 item 的自动包围盒。未设置或设置不当会影响滚动条范围、fitInView 效果和大场景导航。

大量动态 item 时索引方式要测试。`BspTreeIndex` 查询快但维护有成本；频繁移动海量 item 时 `NoIndex` 反而可能更合适。
