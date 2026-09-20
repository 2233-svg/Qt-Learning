# QBitmap

> Qt 6.11.1 · Qt GUI · 来自 `QBitmap`

## 1. 先建立直觉

`QBitmap` 是 1-bit 深度的 `QPixmap`。每个像素只有两种状态，通常用于“有或没有”“遮挡或透明”“选中或未选中”这样的二值图形，而不是保存普通彩色图片。

它最常见的价值是掩码：自定义光标 mask、图像透明区域、旧式单色资源、区域化绘制。若把彩色图片强行转成 `QBitmap`，Qt 必须做二值化或抖动，细节与颜色信息都会丢失。

## 2. 类说明

`QBitmap` 继承自 `QPixmap`，所以可作为 GUI 侧的像素图资源使用，但其像素格式固定为单色。它是值类型，支持复制与交换。

类说明只用于表明这些 API 来自 `QBitmap`：加载、转换、清空与变换由本类提供；一般图像读取、编辑和多像素格式处理应优先使用 `QImage`，最终显示再按需转为 `QPixmap`。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QBitmap()` | 构造空位图。 |
| `QBitmap(size)` / `QBitmap(width, height)` | 构造指定尺寸的未初始化单色位图。 |
| `QBitmap(fileName, format)` | 从文件加载并转换为 1-bit 位图，彩色源会二值化。 |
| `fromData(size, bits, monoFormat)` | 从原始 1-bit 数据构造位图。 |
| `fromImage(image, flags)` | 将 `QImage` 转换为位图，可指定转换策略。 |
| `fromPixmap(pixmap)` | 将 `QPixmap` 转换为位图，必要时进行抖动。 |
| `clear()` | 将全部位设置为 `Qt::color0`。 |
| `transformed(transform)` | 返回几何变换后的位图副本。 |
| `swap(other)` | 高效交换两个位图。 |
| `operator QVariant()` | 转换为 `QVariant`，便于属性或通用容器传递。 |

## 4. 关键用法

### 从 1-bit 原始数据构造掩码

```cpp
static const uchar bits[] = {
    0b11110000,
    0b10010000,
    0b10010000,
    0b11110000
};

QBitmap mask = QBitmap::fromData(
    QSize(8, 4), bits, QImage::Format_MonoLSB);
```

位序必须与 `QImage::Format_Mono` 或 `QImage::Format_MonoLSB` 匹配。XBM 风格数据通常使用 `Format_Mono`；传错位序会导致图形左右镜像或花屏。

### 用作自定义光标 mask

```cpp
QBitmap bitmap(":/cursor/shape.xbm");
QBitmap mask(":/cursor/mask.xbm");
QCursor cursor(bitmap, mask, 2, 2);
```

bitmap 决定前景位，mask 决定透明/不透明区域。单色光标的组合规则具有平台差异，因此除非需要复古或极简资源，彩色 `QPixmap` 光标通常更直观。

### 从图像生成二值遮罩

```cpp
QImage source(":/icons/logo.png");
QBitmap silhouette = QBitmap::fromImage(
    source.convertToFormat(QImage::Format_Grayscale8),
    Qt::ThresholdDither);
```

显式控制灰度化和抖动，比把任意彩色图直接交给默认转换更可预测。

## 5. 使用场景

`QBitmap` 适合自定义单色光标、透明遮罩、二值打印图形、像素风工具图标、legacy XBM 资源和只需命中/遮挡信息的辅助数据。

它也适合与 `QRegion`、`QPixmap::setMask()` 等旧式图形 API 协作，但现代应用在需要 alpha 透明度时通常更倾向 `QImage` / `QPixmap` 的 alpha 通道。

## 6. 常见坑与经验

不要把 `QBitmap` 当作一般图片容器。它只有 1-bit 深度，不能表达半透明、抗锯齿和完整颜色。

不要假设新建 bitmap 已清零。指定尺寸构造后像素未初始化，需要先 `clear()` 或立即完整绘制。

不要忽略转换成本。把大彩色图片反复转换成 bitmap 会产生抖动与 CPU 开销，应缓存结果。

不要在后台线程随意操作 GUI 资源。需要大规模图像处理时，先在后台处理 `QImage`，回到 GUI 线程后再转换成 `QBitmap` / `QPixmap`。

不要忘记高 DPI。作为光标或 UI mask 使用时，资源的 device pixel ratio 和目标显示比例仍需匹配。

## 7. 知识点覆盖

学习 `QBitmap` 应覆盖 1-bit 像素、bitmap/mask、`QImage::Format_Mono`、位序、二值化、抖动、自定义光标、透明遮罩、`QPixmap` 区别、高 DPI 和 GUI 线程资源管理。
