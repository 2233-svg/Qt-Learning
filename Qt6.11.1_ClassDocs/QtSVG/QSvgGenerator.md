# QSvgGenerator
> Qt 6.11.1 · Qt SVG · 来自 `QSvgGenerator`

## 1. 先建立直觉

`QSvgGenerator` 是一个 `QPaintDevice`：你可以把它当作“SVG 文件画布”，用普通 `QPainter` 命令往上画，最后得到 SVG 输出。也就是说，它不是读取 SVG 的类，而是把 Qt 绘图指令导出成 SVG 的类。

它适合导出图表、简单矢量图、打印替代格式或可编辑草图。它不能保证把所有 `QPainter` 效果都完美转换成简洁 SVG；复杂渐变、混合模式、位图、裁剪和字体细节要实测输出质量。

## 2. 类说明

保留类说明：这些 API 来自 `QSvgGenerator`，属于 Qt SVG 模块，用于通过 `QPainter` 生成 SVG 文档。

使用顺序通常是：设置输出目标、尺寸、viewBox、标题描述和 DPI，然后创建 `QPainter painter(&generator)` 开始绘制。绘制期间再改输出文件或尺寸，往往已经来不及。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QSvgGenerator()` | 创建默认 SVG Tiny 1.2 生成器。 |
| `QSvgGenerator(SvgVersion version)` | 指定输出 SVG 版本。 |
| `setFileName(fileName)` / `fileName()` | 设置或查询输出文件路径。 |
| `setOutputDevice(QIODevice *)` / `outputDevice()` | 输出到自定义设备，如 buffer、压缩流。 |
| `setSize(QSize)` / `size()` | 设置生成文档的像素尺寸。 |
| `setViewBox(QRect/QRectF)` / `viewBox()` / `viewBoxF()` | 设置 SVG 坐标系视框。 |
| `setResolution(int dpi)` / `resolution()` | 设置 DPI，用于物理尺寸换算。 |
| `setTitle(QString)` / `title()` | 设置 SVG 标题元数据。 |
| `setDescription(QString)` / `description()` | 设置 SVG 描述元数据。 |
| `svgVersion()` | 查询生成器输出版本。 |
| `paintEngine()` | 返回内部绘图引擎，应用通常不直接调用。 |
| `metric()` | `QPaintDevice` 指标查询，框架内部使用。 |
| `initPainter(QPainter *)` | Qt 6.11 起的绘制初始化钩子，应用正常不直接调用。 |
| `SvgVersion` | 输出规范选择：`SvgTiny12` 或 `Svg11`。 |

## 4. 典型流程

```cpp
QSvgGenerator generator(QSvgGenerator::SvgVersion::Svg11);
generator.setFileName("report-chart.svg");
generator.setSize(QSize(800, 600));
generator.setViewBox(QRectF(0, 0, 800, 600));
generator.setTitle("Monthly report chart");
generator.setDescription("Generated from the analytics view");

QPainter painter(&generator);
painter.setRenderHint(QPainter::Antialiasing);
drawChart(&painter);
```

输出到内存时使用 `QBuffer`：

```cpp
QByteArray bytes;
QBuffer buffer(&bytes);
buffer.open(QIODevice::WriteOnly);
generator.setOutputDevice(&buffer);
```

## 5. 使用场景

| 场景 | 为什么适合 |
| --- | --- |
| 图表、流程图、简单图形导出 | 原本就有 `QPainter` 绘制代码，迁移成本低。 |
| 需要可缩放报表附件 | SVG 比位图在缩放和打印时更清晰。 |
| 自动化生成图标草稿 | 程序参数化绘制，输出给设计或文档流程。 |
| 自定义输出管线 | `setOutputDevice()` 可接内存、压缩或网络缓冲。 |

## 6. 常见坑与经验

必须先设置输出目标再开始绘制。`QPainter` 一旦在 generator 上 active，很多结构性设置都应该视为冻结；绘制中途换 `fileName` 或 `outputDevice` 是危险设计。

`size` 是设备尺寸，`viewBox` 是 SVG 坐标系。想让坐标和像素一一对应，就把二者设成同样范围；想输出逻辑坐标，就用 viewBox 表达你的业务坐标系。

`resolution` 影响物理尺寸换算，不会凭空提高矢量图“清晰度”。矢量图清晰度来自路径，DPI 主要影响嵌入文档、打印和单位转换。

不是所有 `QPainter` 操作都会得到理想 SVG。特别复杂的 composition mode、平台字体差异、位图纹理和高级效果，导出后要用浏览器、Inkscape、Illustrator 或目标消费端检查。

## 7. 知识点覆盖

- `QSvgGenerator` 作为 `QPaintDevice` 的使用方式。
- 文件输出与 `QIODevice` 输出的区别。
- `size`、`viewBox`、DPI、元数据的关系。
- `QPainter` 导出 SVG 的能力边界。
- SVG Tiny 1.2 与 SVG 1.1 输出选择。
