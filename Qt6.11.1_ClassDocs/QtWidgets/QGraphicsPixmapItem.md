# QGraphicsPixmapItem

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsPixmapItem`

## 1. 先建立直觉

`QGraphicsPixmapItem` 是场景中的图片图元。它把 `QPixmap` 放进 `QGraphicsScene`，让图片可以像其他 item 一样移动、缩放、旋转、选择和参与命中检测。

它适合显示图标、截图、地图瓦片、背景图、纹理预览、图片标注底图。图像内容本身由 `QPixmap` 提供，item 负责在场景中摆放和绘制它。

## 2. 类说明

`QGraphicsPixmapItem` 继承自 `QGraphicsItem`。`offset()` 决定 pixmap 左上角相对于 item 原点的位置，`transformationMode()` 决定缩放时是快速还是平滑。

`shapeMode()` 决定透明区域是否参与命中：按 mask 精确命中更符合视觉，但成本更高；按 bounding rect 命中更快但可能点到透明区域也算命中。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QGraphicsPixmapItem(parent)` | 创建空图片图元。 |
| `QGraphicsPixmapItem(QPixmap, parent)` | 创建带图片的图元。 |
| `setPixmap(const QPixmap &)` / `pixmap()` | 设置或读取图片。 |
| `setOffset(QPointF)` / `offset()` | 设置图片相对 item 原点的偏移。 |
| `setOffset(x, y)` | 坐标参数版本。 |
| `setTransformationMode(Qt::TransformationMode)` | 设置缩放绘制质量：快速或平滑。 |
| `transformationMode()` | 读取缩放绘制模式。 |
| `setShapeMode(ShapeMode)` / `shapeMode()` | 设置透明区域命中策略。 |
| `MaskShape` | 根据 pixmap mask 精确命中。 |
| `BoundingRectShape` | 按外接矩形命中，速度快。 |
| `HeuristicMaskShape` | 使用启发式 mask，折中方案。 |
| `boundingRect()` / `shape()` | 返回边界和命中形状。 |
| `paint()` | 绘制 pixmap。 |

## 4. 关键用法

```cpp
auto *image = scene->addPixmap(QPixmap(":/images/photo.png"));
image->setTransformationMode(Qt::SmoothTransformation);
image->setFlag(QGraphicsItem::ItemIsMovable);
```

让图片以中心为 item 原点：

```cpp
const QPixmap pm(":/icons/node.png");
auto *item = new QGraphicsPixmapItem(pm);
item->setOffset(-pm.width() / 2.0, -pm.height() / 2.0);
```

透明图片需要精确点击时：

```cpp
item->setShapeMode(QGraphicsPixmapItem::MaskShape);
```

## 5. 使用场景

适合图片查看器、标注底图、节点图标、纹理预览、地图瓦片、缩略图画布、流程图图形素材。

如果要处理像素数据，用 `QImage` 更方便；如果要在场景中高效显示并利用 GPU/窗口系统资源，`QPixmap` + pixmap item 更贴近 GUI 显示。

## 6. 常见坑与经验

大量大图会吃内存。不要把未缩放的超大图片随意铺满场景；可以用瓦片、缩略图或按需加载。

`SmoothTransformation` 质量更好但更慢。静态预览可以开，频繁缩放拖动时要评估性能。

透明区域命中策略会影响用户体验。图标类通常精确命中更自然，图片底图通常外接矩形命中更简单。
