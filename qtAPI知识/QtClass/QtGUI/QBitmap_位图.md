# QBitmap：用于掩码和图案的 1-bit QPixmap

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QBitmap>`  
> 模块：Qt GUI，链接 `Qt6::Gui`  
> 继承：`QPixmap`

## 它解决什么问题

`QBitmap` 是深度固定为 1 的单色离屏绘制设备。每个像素只有一个 bit，适合表达“有或没有”的形状，而非真实彩色图像。它主要用于自定义光标和画刷、构造 `QRegion`，以及为 pixmap、widget 设置遮罩。

非空 `QBitmap` 的深度必为 `1`，空对象的深度为 `0`。从深度大于 1 的 `QPixmap` 转换时，Qt 会自动抖动成单色位图，因此它不是保存原图颜色信息的格式。

## 何时使用，何时不要使用

适合：

- 做透明遮罩或命中区域。
- 构造重复的黑白纹理，交给 `QBrush` 使用。
- 创建传统风格的单色光标。
- 需要用一位数据表达前景与背景的场景。

不适合：

- 保存照片、图标原色、灰阶或 alpha 通道细节，此时用 `QImage` 或 `QPixmap`。
- 在工作线程中加载、修改或频繁处理显示资源。`QBitmap` 继承 `QPixmap`，应遵守其 GUI 资源与线程约束；后台图像处理优先使用 `QImage`，回到 GUI 线程再转换。

## 最关键的颜色语义

在 `QBitmap` 上绘制必须使用 `Qt::color0` 与 `Qt::color1`：

| 绘制颜色 | 写入 bit | 常见含义 |
| --- | --- | --- |
| `Qt::color0` | `0` | 背景或透明像素 |
| `Qt::color1` | `1` | 前景或不透明像素 |

`Qt::black` 与 `Qt::white` 不是这两个 bit 值的可靠替代品。它们的 `QColor::pixel()` 并不保证分别为 `0` 和 `1`，用于 1-bit 位图会导致含义不明确。

```cpp
QBitmap mask(QSize(32, 32));
mask.clear(); // 全部置为 Qt::color0

QPainter painter(&mask);
painter.setPen(Qt::NoPen);
painter.setBrush(Qt::color1);
painter.drawEllipse(mask.rect());
```

尺寸构造函数创建的像素内容是未初始化的。若希望从透明背景开始，必须调用 `clear()` 或先用 `Qt::color0` 填充，不能依赖内存恰好为零。

## 创建方式和数据格式

文件构造函数委托给 `QPixmap::load()`；文件不存在或格式未知时，结果为 null bitmap。若文件不是 1-bit，结果会被抖动。

`fromImage()` 和 `fromPixmap()` 都返回转换后的副本。后者自 Qt 6.0 提供，深度大于 1 的输入会抖动。

`fromData()` 适合嵌入静态位图字节数据，但要求最严格：

- 数据必须按字节对齐。
- `monoFormat` 只能是 `QImage::Format_Mono` 或 `QImage::Format_MonoLSB`。
- 位序必须与实际字节数据一致。
- XBM 格式数据应指定 `QImage::Format_Mono`。

错误的位序通常不会报错，而是表现为图案左右翻转、杂乱或透明区域相反，因此这是排查掩码问题的首要检查项。

## 共享与变换

和 `QPixmap` 一样，`QBitmap` 使用隐式共享。拷贝通常很便宜，首次修改某个副本时才会分离数据。需要高效交换两个位图时用 `swap()`，它快速且不会失败。

`transformed()` 根据 `QTransform` 返回新的位图，可进行平移、缩放、错切和旋转。它不会原地修改原位图；变换后的单色边缘可能因转换规则与原始像素网格不同而发生形状变化。

## API 速查表

| API | 含义 | 重点边界 |
| --- | --- | --- |
| `QBitmap()` | 创建 null bitmap。 | 深度为 `0`，使用前可用 `isNull()` 判断。 |
| `QBitmap(int width, int height)` | 创建指定宽高的 1-bit 位图。 | 像素未初始化，需先 `clear()` 或显式填充。 |
| `QBitmap(const QSize &size)` | 创建指定尺寸的 1-bit 位图。 | 像素未初始化。 |
| `QBitmap(const QString &fileName, const char *format = nullptr)` | 从文件加载并转换为位图。 | 文件无效或未知格式时结果为 null；非 1-bit 输入会抖动。 |
| `~QBitmap()` | 销毁位图。 | 采用隐式共享，值对象可正常拷贝和析构。 |
| `void clear()` | 将所有 bit 置为 `Qt::color0`。 | 表示背景或透明，适合初始化掩码。 |
| `static QBitmap fromData(const QSize &size, const uchar *bits, QImage::Format monoFormat = QImage::Format_MonoLSB)` | 从原始单色字节数据构造位图。 | 数据需字节对齐；格式只能为 `Format_Mono` 或 `Format_MonoLSB`。 |
| `static QBitmap fromImage(const QImage &image, Qt::ImageConversionFlags flags = Qt::AutoColor)` | 从图像副本转换为位图。 | 转换会丢失颜色信息。 |
| `static QBitmap fromImage(QImage &&image, Qt::ImageConversionFlags flags = Qt::AutoColor)` | 从右值图像转换为位图。 | 仍返回转换后的位图，重载用于减少不必要拷贝的机会。 |
| `static QBitmap fromPixmap(const QPixmap &pixmap)` | 从 pixmap 副本转换为位图。 | Qt 6.0 起可用；深度大于 1 时自动抖动。 |
| `void swap(QBitmap &other)` | 与另一位图交换数据。 | 速度快且不会失败；只交换同类对象。 |
| `QBitmap transformed(const QTransform &matrix) const` | 返回经矩阵变换的新位图。 | 不修改原对象，结果可能改变像素边缘。 |
| `operator QVariant() const` | 将位图包装为 `QVariant`。 | 适合 QVariant 传递或属性存储，不等于图像序列化。 |
| 继承的 `QPixmap::depth()` | 查询位图深度。 | 非空对象应为 `1`，null 对象为 `0`。 |
