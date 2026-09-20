# Qt QSvgGenerator 深入笔记：把 QPainter 绘制结果写成 SVG

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSvgGenerator>`  
> 所属模块：`Qt6::Svg`  
> 继承：`QPaintDevice -> QSvgGenerator`  
> 线程说明：类成员可重入；这不表示同一个对象可以被多个线程同时配置或绘制。

`QSvgGenerator` 是一个只写的 `QPaintDevice`：你照常使用 `QPainter` 画线、路径、文字和图片，Qt 把这些绘制命令转换为 SVG XML 输出到文件或 `QIODevice`。

它解决的是“已有一套 QPainter 绘图代码，怎样导出可缩放矢量图”的问题。例如导出流程图、统计图、工程图预览或打印替代物。它不是 SVG 读取器；要读取并显示 SVG，使用 `QSvgRenderer`。

```text
绘图逻辑 -- QPainter --> QSvgGenerator -- 写出 --> .svg 文件 / QIODevice
```

## 1. 什么时候用它

- 应用中的图表、示意图已经基于 `QPainter` 实现，希望导出为可无限缩放的文件。
- 需要把图形写入 `QBuffer`，再作为网络响应、压缩包条目或数据库字段处理。
- 同一套绘制函数既要画到屏幕或 `QImage`，又要画到 SVG。

不适合的情况：

- 目标只是保存像素截图：用 `QImage::save()` 更直接。
- 已有复杂 SVG 字符串，需要修改 XML 节点：用 XML API 操作源文本更合适。
- 需要把 SVG 显示到控件或图像上：用 `QSvgRenderer` 或 `QSvgWidget`。

## 2. 最小可用示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS Svg)
target_link_libraries(mytarget PRIVATE Qt6::Svg)
```

```cpp
#include <QPainter>
#include <QSvgGenerator>

QSvgGenerator generator;
generator.setFileName("report.svg");
generator.setSize(QSize(800, 450));
generator.setViewBox(QRect(0, 0, 800, 450));
generator.setTitle("Monthly report");
generator.setDescription("Exported chart for the monthly report");

QPainter painter;
if (painter.begin(&generator)) {
    painter.setRenderHint(QPainter::Antialiasing);
    painter.setPen(QPen(Qt::darkBlue, 3));
    painter.drawLine(60, 360, 740, 80);
    painter.drawText(QRect(60, 380, 680, 40), Qt::AlignCenter, "Revenue");
    painter.end();
}
```

这里有一个很关键的顺序：**先配置 generator，再 `begin()`，最后显式 `end()`**。`QSvgGenerator` 和 `QPrinter` 一样是输出设备，绘制结束时才会完整收尾文档。

## 3. 输出目标、画布和坐标不是一回事

### 3.1 `fileName` 与 `outputDevice`

两者都能指定输出位置：

- `setFileName("chart.svg")`：最适合直接落盘。
- `setOutputDevice(&buffer)`：最适合内存、网络、压缩流等自定义输出。

如果两者同时设置，`outputDevice` 优先。`QSvgGenerator` 不拥有传入的 `QIODevice`；调用方必须保证设备在整个绘制期间仍存在，并以可写状态打开。

```cpp
QByteArray bytes;
QBuffer buffer(&bytes);
buffer.open(QIODevice::WriteOnly);

QSvgGenerator generator;
generator.setOutputDevice(&buffer);
```

### 3.2 `size`、`viewBox` 和 `resolution`

这三个量很容易混淆：

- `size`：写入 `<svg>` 的宽、高；默认 `QSize(-1, -1)`，即不输出宽高属性。
- `viewBox`：SVG 内部坐标系；默认无效矩形，即不输出 `viewBox` 属性。
- `resolution`：DPI，用于计算 SVG 的物理尺寸，不等于绘图坐标的缩放倍率。

常见的导出约定是让 `size` 和 `viewBox` 使用同样的宽高，例如 `800 x 450`。这样绘图函数里的像素式坐标正好对应 SVG 的逻辑坐标。若 SVG 要嵌入另一份文档，`viewBox` 往往比固定物理宽高更重要。

`setSize()` 和 `setViewBox()` 不能在已有活动 `QPainter` 时调用；把它们放在 `begin()` 之前。

## 4. SVG 版本和元数据

从 Qt 6.5 起，构造函数可选择输出规范：

- 默认构造使用 `SvgTiny12`。
- 目标系统明确要求 SVG 1.1 时，传入 `SvgVersion::Svg11`。

`title` 和 `description` 会成为 SVG 的元数据。它们不影响图形几何，但对文件管理、无障碍说明和后续检索很有价值。

```cpp
QSvgGenerator generator(QSvgGenerator::SvgVersion::Svg11);
generator.setTitle("Pump layout");
generator.setDescription("Blue lines show the cooling-water route.");
```

## 5. 生命周期与并发边界

`QSvgGenerator` 不是 `QObject`，没有 parent 参数，也不参与对象树。通常把它作为局部对象使用，确保 `QPainter::end()` 发生在 generator 析构前。

Qt 文档将该类标为“可重入”：不同线程可使用不同的 generator 实例。但一个 generator 同时保存输出目标、尺寸和绘制状态，不能让多个线程同时对**同一个实例**调用 setter 或启动绘制。

## 6. 常见问题

### 6.1 生成了空文件或尾部不完整

先查是否遗漏 `painter.end()`，以及 `QIODevice` 是否仍处于打开、可写状态。使用文件名时也检查目标目录是否存在、是否有写权限。

### 6.2 导出的图形在浏览器里比例不对

检查是否只设了 `size` 却没有设 `viewBox`，或二者采用了不一致的坐标体系。不要把 DPI 当成内部坐标的缩放工具。

### 6.3 想在绘制中途改尺寸

这不是安全用法。结束当前 painter，重新配置 generator，再开始新的 SVG 文档。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `SvgVersion::SvgTiny12` | 选择 SVG Tiny 1.2 输出规范 | 默认构造函数使用它；兼容性要求特殊时再改版本 |
| 枚举 | `SvgVersion::Svg11` | 选择 SVG 1.1 输出规范 | Qt 6.5 起可用；只在下游明确要求 SVG 1.1 时选择 |
| 构造 | `QSvgGenerator()` | 创建使用 SVG Tiny 1.2 的输出设备 | 先设置输出目标和画布，再让 `QPainter` 开始绘制 |
| 构造 | `QSvgGenerator(SvgVersion version)` | 按指定规范创建输出设备 | Qt 6.5 起可用；版本一经构造确定，不能随后切换 |
| 析构 | `~QSvgGenerator()` | 销毁 SVG 输出设备 | 析构前必须结束所有在它上面活动的 `QPainter` |
| 元数据 | `description() const` | 读取 SVG 描述 | 用于检查当前导出元数据 |
| 元数据 | `setDescription(const QString &description)` | 设置 SVG 描述 | 不改变图形内容；适合补充文件含义和无障碍文本 |
| 输出目标 | `fileName() const` | 读取文件输出路径 | 如果设置了 `outputDevice`，文件名不会成为实际优先输出目标 |
| 输出目标 | `setFileName(const QString &fileName)` | 把 SVG 输出目标设为文件 | 目录必须存在且可写；与 `outputDevice` 同时设置时会被后者覆盖 |
| 输出目标 | `outputDevice() const` | 读取当前自定义输出设备指针 | 返回的是非拥有指针，不能据此假定 generator 管理其生命周期 |
| 输出目标 | `setOutputDevice(QIODevice *outputDevice)` | 把 SVG 写入指定设备 | 调用方负责设备存活和可写打开；它优先于 `fileName` |
| 物理尺寸 | `resolution() const` | 读取输出 DPI | DPI 用于物理尺寸换算，不是内部绘图坐标的缩放比例 |
| 物理尺寸 | `setResolution(int dpi)` | 设置输出 DPI | 在开始绘制前设置；与 `size`、`viewBox` 配合理解 |
| 画布尺寸 | `size() const` | 读取 SVG 宽高属性对应的尺寸 | 默认是 `QSize(-1, -1)`，表示不输出 width/height 属性 |
| 画布尺寸 | `setSize(const QSize &size)` | 设置 SVG 画布宽高 | 必须在 painter 活动前设置；常与 `viewBox` 使用同一宽高 |
| 元数据 | `title() const` | 读取 SVG 标题 | 仅元数据，不影响画出的图元 |
| 元数据 | `setTitle(const QString &title)` | 设置 SVG 标题 | 可用于文档标题和辅助信息 |
| 坐标系 | `viewBox() const` | 以整数矩形读取 `viewBoxF()` | 返回值会丢失小数部分；需要浮点坐标时用 `viewBoxF()` |
| 坐标系 | `viewBoxF() const` | 以浮点矩形读取 SVG 内部坐标系 | 默认是无效矩形，表示不输出 SVG 的 `viewBox` 属性 |
| 坐标系 | `setViewBox(const QRect &viewBox)` | 用整数矩形设置内部坐标系 | 必须在 painter 活动前设置 |
| 坐标系 | `setViewBox(const QRectF &viewBox)` | 用浮点矩形设置内部坐标系 | 适合需要小数坐标的图形；同样不能在绘制中修改 |
| SVG 版本 | `svgVersion() const` | 读取当前生成器要输出的 SVG 规范 | Qt 6.5 起可用；可据此核对导出兼容性 |
| 受保护实现 | `initPainter(QPainter *painter) const` | 初始化绑定到该设备的 painter | Qt 6.11 起的框架扩展点；普通调用方不应直接调用 |
| 受保护实现 | `metric(PaintDeviceMetric metric) const` | 向绘图系统报告设备尺寸、DPI 等度量值 | `QPaintDevice` 的重写；由 Qt 绘图框架调用 |
| 受保护实现 | `paintEngine() const` | 返回把绘图命令转为 SVG 的绘图引擎 | `QPaintDevice` 的重写；不需要在业务代码中手动使用 |

---

### 一句话总结

`QSvgGenerator` 让 `QPainter` 的绘制命令落成 SVG；真正要掌握的是先确定输出目标、`size` 与 `viewBox`，在绘制结束时显式 `end()`，并让外部 `QIODevice` 在整个过程内保持有效。
