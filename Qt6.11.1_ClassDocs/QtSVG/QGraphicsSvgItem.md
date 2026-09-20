# QGraphicsSvgItem
> Qt 6.11.1 · Qt SVG · 来自 `QGraphicsSvgItem`

## 1. 先建立直觉

`QGraphicsSvgItem` 是 Graphics View 场景里的 SVG 图元。它让 SVG 像普通 `QGraphicsItem` 一样进入 `QGraphicsScene`：可以移动、缩放、旋转、参与层级和碰撞区域，也能只显示 SVG 文件中的某个 `id` 元素。

它适合老牌 Graphics View 架构的地图、编辑器、流程图、组态画面。Qt Quick 场景里不要强行用它，应该看 Quick 侧的图像或自定义渲染方案。

## 2. 类说明

保留类说明：这些 API 来自 `QGraphicsSvgItem`，属于 Qt SVG 模块，用于在 `QGraphicsScene` 中显示 SVG 内容。

每个 item 可以拥有自己的 renderer，也可以通过 `setSharedRenderer()` 多个 item 共用同一个 `QSvgRenderer`。共享能省解析成本，但 renderer 的生命周期要由你保证。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QGraphicsSvgItem(parent = nullptr)` | 创建空 SVG 图元。 |
| `QGraphicsSvgItem(fileName, parent = nullptr)` | 创建并加载 SVG 文件。 |
| `setSharedRenderer(QSvgRenderer *)` | 使用外部共享 renderer，避免重复解析。 |
| `renderer() const` | 取得当前 renderer。 |
| `setElementId(id)` / `elementId()` | 只显示 SVG 中指定 `id` 的元素。 |
| `setMaximumCacheSize(QSize)` / `maximumCacheSize()` | 设置图元缓存的最大尺寸。 |
| `boundingRect() const` | 返回图元边界，供场景索引和重绘使用。 |
| `paint(QPainter *, option, widget)` | 图形视图框架调用的绘制函数。 |
| `type() const` | 返回图元类型，便于自定义 item 判断。 |

## 4. 典型流程

```cpp
auto *renderer = new QSvgRenderer(QStringLiteral(":/symbols/factory.svg"), scene);

auto *pump = new QGraphicsSvgItem;
pump->setSharedRenderer(renderer);
pump->setElementId("pump");
pump->setPos(40, 80);
scene->addItem(pump);

auto *valve = new QGraphicsSvgItem;
valve->setSharedRenderer(renderer);
valve->setElementId("valve");
valve->setPos(140, 80);
scene->addItem(valve);
```

这种写法的好处是一个 SVG 文件可包含多个符号，解析一次，场景里按元素复用。

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 工业组态/流程图符号库 | 一个 SVG 文件存多个符号，用 `elementId` 拆出。 |
| 地图或平面图标注 | item 可缩放、旋转、选择、拖拽。 |
| 可视化编辑器 | SVG 图元和其它 `QGraphicsItem` 混排。 |
| 大量重复图标 | `setSharedRenderer()` 降低解析和内存成本。 |

## 6. 常见坑与经验

`setSharedRenderer()` 不接管 renderer 所有权。只要 item 还在绘制，renderer 就必须活着。最省心的做法是把 renderer 的 QObject parent 设成 scene、view 或更长寿的资源管理器。

`elementId` 只对可渲染元素有意义。设计 SVG 资源时要给目标元素设置稳定 `id`，不要依赖设计工具自动生成的临时名字。

缓存尺寸不是越大越好。大缓存能减少重复渲染，但会吃内存；item 经常缩放或内容很简单时，过大的 cache 反而不划算。

`boundingRect()` 影响场景索引、重绘区域和鼠标命中。切换 elementId 或 renderer 后，如果边界变化，要确保场景能正确更新，避免残影或命中区域不对。

## 7. 知识点覆盖

- Graphics View 中 SVG 图元的角色。
- `QSvgRenderer` 共享和生命周期管理。
- `elementId` 级别的符号复用。
- item 缓存大小、边界和绘制流程。
- SVG 资源制作与场景交互设计。
