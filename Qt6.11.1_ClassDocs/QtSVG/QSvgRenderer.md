# QSvgRenderer
> Qt 6.11.1 · Qt SVG · 来自 `QSvgRenderer`

## 1. 先建立直觉

`QSvgRenderer` 是 Qt SVG 的核心读取和绘制对象：它把 SVG 文档解析成可渲染的内部结构，然后在你提供的 `QPainter` 上画出来。`QSvgWidget` 和 `QGraphicsSvgItem` 都可以看成对它的封装；如果你要自己控制绘制目标、缩放、裁剪、缓存或只画某个元素，就直接用它。

Qt SVG 面向的是常见图标、插画和界面资源，不是完整浏览器级 SVG 引擎。复杂滤镜、脚本、外部资源和网页 SVG 生态里的所有特性，都不能默认认为会被支持。

## 2. 类说明

保留类说明：这些 API 来自 `QSvgRenderer`，属于 Qt SVG 模块，用于加载 SVG 文档并通过 `QPainter` 渲染。

它继承 `QObject`，有动画计时和 `repaintNeeded()` 信号。非动画图标可以长期复用同一个 renderer；动画 SVG 则要把重绘信号接到目标 widget/item 的更新逻辑。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QSvgRenderer(parent)` | 创建空 renderer，稍后再 `load()`。 |
| `QSvgRenderer(filename/contents/reader, parent)` | 构造时直接加载 SVG。 |
| `load(filename)` | 从文件加载 SVG，返回是否成功。 |
| `load(QByteArray)` | 从内存字节加载 SVG。 |
| `load(QXmlStreamReader *)` | 从 XML 流读取器加载，适合自定义输入管线。 |
| `isValid()` | 判断当前是否有可渲染文档。 |
| `render(QPainter *)` | 按默认尺寸/视框渲染整个文档。 |
| `render(QPainter *, QRectF bounds)` | 把 SVG 映射到指定区域。 |
| `render(QPainter *, elementId, bounds)` | 只渲染指定 `id` 的元素。 |
| `defaultSize()` | 返回 SVG 文档声明的默认尺寸。 |
| `viewBox()` / `viewBoxF()` | 读取当前视框。 |
| `setViewBox(QRect/QRectF)` | 改变后续渲染使用的 SVG 视框。 |
| `setAspectRatioMode(mode)` | 控制渲染到 bounds 时是否保持宽高比。 |
| `boundsOnElement(id)` | 查询指定元素在 SVG 坐标系中的边界。 |
| `transformForElement(id)` | 查询元素自身变换矩阵。 |
| `elementExists(id)` | 判断某个可渲染元素是否存在。 |
| `animated()` | 文档是否包含动画。 |
| `setAnimationEnabled(bool)` | 开关动画计时。 |
| `setFramesPerSecond(int)` | 设置动画刷新频率。 |
| `setOptions(QtSvg::Options)` | 设置 SVG 解析/渲染选项，必须在加载前设置才有效。 |
| `setDefaultOptions(flags)` | 设置全局默认 SVG 选项，可被环境变量覆盖。 |
| `repaintNeeded()` | 动画帧变化时发出，接收方应触发重绘。 |

## 4. 典型流程

```cpp
QSvgRenderer renderer(QStringLiteral(":/icons/state.svg"));
if (!renderer.isValid())
    return;

QPixmap pixmap(64, 64);
pixmap.fill(Qt::transparent);

QPainter painter(&pixmap);
renderer.setAspectRatioMode(Qt::KeepAspectRatio);
renderer.render(&painter, QRectF(QPointF(0, 0), pixmap.size()));
```

只画 SVG 中某个元素时，先确认 `id` 存在：

```cpp
if (renderer.elementExists("warning-layer"))
    renderer.render(&painter, "warning-layer", targetRect);
```

## 5. 使用场景

| 场景 | 为什么直接用 renderer |
| --- | --- |
| 自定义 widget 的 `paintEvent()` | 可以精确控制目标矩形、抗锯齿、裁剪和缓存。 |
| 把 SVG 预渲染成 pixmap | 常用于图标缓存、缩略图、打印前准备。 |
| 只渲染 SVG 里的某个元素 | `elementId` 渲染比拆文件更方便。 |
| 动画 SVG | 连接 `repaintNeeded()` 到 `update()`。 |
| 多个界面对象共享同一份 SVG | 避免重复解析同一个文件。 |

## 6. 常见坑与经验

`viewBox` 是 SVG 坐标系窗口，`bounds` 是你要画到的目标区域。改 `viewBox` 相当于换“看 SVG 的哪一块”，传 `bounds` 是换“画到设备的哪一块”。这两个概念混了，缩放和裁剪就会变得很难调。

`setOptions()` 要在 `load()` 之前调用；用带文件名或内容的构造函数时，加载已经发生了，再设置 options 通常来不及。需要特殊选项时，用空构造，再 `setOptions()`，最后 `load()`。

动画 SVG 不会自动让你的 widget 重绘。`repaintNeeded()` 只是信号，必须接到 `QWidget::update()`、`QGraphicsItem::update()` 或你自己的刷新逻辑。

渲染结果仍走 `QPainter`，目标设备可能是 widget、pixmap、image、printer 或 `QSvgGenerator`。不同设备的 DPI、坐标和抗锯齿表现不同，导出和屏幕显示不要只测一种。

## 7. 知识点覆盖

- SVG 加载入口：文件、字节数组、XML 流。
- `QPainter` 渲染模型和目标设备。
- `viewBox`、`defaultSize`、`bounds`、宽高比的区别。
- 元素级渲染和元素几何查询。
- 动画刷新、FPS、`repaintNeeded()`。
- SVG 选项设置时机与 Qt SVG 支持边界。
