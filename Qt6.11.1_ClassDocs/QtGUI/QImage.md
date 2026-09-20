# QImage

> Qt 6.11.1 · Qt GUI · 来自 `QImage`

## 1. 先建立直觉

`QImage` 是 CPU 可寻址的像素缓冲区，也是一个 `QPaintDevice`。它适合解码、逐像素处理、离屏绘制、颜色管理和后台图像工作。与偏向窗口系统显示资源的 `QPixmap` 相比，`QImage` 的 `bits()`、`scanLine()` 和明确的 `Format` 使它能被算法直接处理。

一张图的“大小”并不只是一组宽高：还包括像素格式、每行跨度、alpha 表示方式、颜色空间、DPR、DPI 元数据和文本元数据。代码如果只盯着 `width() * height() * 4`，迟早会在 24 位、16 位、灰度、浮点或外部缓冲区图像上出错。

## 2. 类说明

- 头文件：`#include <QImage>`
- CMake：`target_link_libraries(app PRIVATE Qt6::Gui)`
- 类型：隐式共享值类型，适合按值传递；写访问会触发 detach。
- 继承：`QPaintDevice`，可用 `QPainter painter(&image)` 离屏绘制。
- 线程：不同线程可以各自操作独立 `QImage`；共享实例被写入时要明确所有权和 detach 成本。不要把同一实例并发读写。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QImage(size, format)` | 分配未初始化的图像缓冲区 |
| `QImage(fileName)` / `load()` / `fromData()` | 直接解码文件、设备或内存数据 |
| 外部数据构造函数 | 包装现有像素内存；调用者负责内存和行跨度生命周期 |
| `isNull()` / `valid()` / `size()` / `rect()` | 检查解码/分配与边界 |
| `format()` / `pixelFormat()` / `depth()` | 查询像素布局和每像素位数 |
| `bits()` / `constBits()` | 获得整块首地址；非 const 访问可能 detach |
| `scanLine()` / `constScanLine()` / `bytesPerLine()` | 按行安全遍历像素数据 |
| `pixel()` / `pixelColor()` / `setPixelColor()` | 便利单像素访问，适合少量像素而非热循环 |
| `fill()` / `invertPixels()` / `rgbSwap()` / `flip()` | 常用原地像素变换 |
| `copy()` / `scaled()` / `transformed()` / `flipped()` | 创建裁剪、缩放、变换、翻转后的新图 |
| `convertTo()` / `convertedTo()` | 原地或返回式格式转换 |
| `reinterpretAsFormat()` | 仅在内存解释兼容时更换 format 标签，不转换数据 |
| `colorSpace()` / `setColorSpace()` | 读取/附加颜色空间元数据，不转换颜色值 |
| `convertToColorSpace()` / `convertedToColorSpace()` | 真正转换颜色值到目标色彩空间 |
| `applyColorTransform()` / `colorTransformed()` | 应用预先构造的 `QColorTransform` |
| `hasAlphaChannel()` / `createAlphaMask()` / `setAlphaChannel()` | 查询、生成或替换 alpha |
| `colorTable()` / `setColorTable()` | 管理索引色格式的颜色表 |
| `devicePixelRatio()` / `deviceIndependentSize()` | 管理高 DPI 显示尺寸 |
| `dotsPerMeterX/Y()` | 管理打印/文件分辨率元数据 |
| `textKeys()` / `text()` / `setText()` | 访问可用格式支持的图像文本元数据 |
| `cacheKey()` | 判断共享数据/内容改变，适合内部缓存失效判断 |
| `save()` | 编码到文件或 `QIODevice` |
| `toPixelFormat()` / `toImageFormat()` | 在 `QImage::Format` 与 `QPixelFormat` 间转换 |
| `trueMatrix()` | 获取 `transformed()` 实际使用的平移补偿矩阵 |

## 4. 格式选择

| 格式族 | 适用场景 | 要点 |
| --- | --- | --- |
| `Format_ARGB32_Premultiplied` | 常规带透明绘制、合成、离屏 UI | Qt 绘制性能常最佳；RGB 已乘 alpha |
| `Format_RGBA8888` | 需要确定的内存字节顺序、与外部 RGBA 协议交换 | 按单字节通道访问，勿把端序与 `QRgb` 混为一谈 |
| `Format_RGB32` / `Format_RGBX8888` | 无透明背景、截图、普通离屏绘制 | alpha 恒为不透明 |
| `Format_RGB888` / `Format_BGR888` | 图像交换或相机数据 | 一行常有填充，不能假设 `width * 3` |
| `Format_Grayscale8/16` | 灰度处理、医学/工业图像 | 适合单通道算法，不适合直接当 ARGB 绘制 |
| `Format_RGBA64`、`16FPx4`、`32FPx4` | 高精度/HDR/线性处理 | 内存与带宽成本高，选择前确认后端支持 |
| `Format_Indexed8` | 调色板图像兼容 | 使用 `colorTable()`；不适合直接 `QPainter` 绘制 |
| `Format_CMYK8888` | Qt 6.8 起 CMYK 数据交换 | 不支持直接用 `QPainter` 渲染 |

预乘格式中应始终满足 `R <= A`、`G <= A`、`B <= A`。把普通 RGBA 字节直接当预乘 ARGB 写入，会在半透明边缘形成黑边或脏色。

## 5. 关键用法

### 建立可绘制的离屏画布

```cpp
QImage canvas(1280, 720, QImage::Format_ARGB32_Premultiplied);
if (canvas.isNull())
    return;

canvas.fill(Qt::transparent);
QPainter painter(&canvas);
painter.setRenderHint(QPainter::Antialiasing);
painter.drawEllipse(QPointF(640, 360), 160, 160);
```

刚分配的 `QImage` 含未初始化数据。无论随后是否立刻绘制，先 `fill()`；透明画布尤其要用 `Qt::transparent`，避免未定义 alpha 参与合成。

### 用扫描行写高性能像素算法

```cpp
QImage image = source.convertToFormat(QImage::Format_RGBA8888);

for (int y = 0; y < image.height(); ++y) {
    auto *row = reinterpret_cast<QRgb *>(image.scanLine(y));
    for (int x = 0; x < image.width(); ++x)
        row[x] = qRgba(255 - qRed(row[x]),
                       255 - qGreen(row[x]),
                       255 - qBlue(row[x]),
                       qAlpha(row[x]));
}
```

这里先显式转换到已知格式，才有资格按 `QRgb` 解读内存。对 `RGB888`、浮点或 16 位格式，这种转换和指针类型都不正确。行首必须来自 `scanLine(y)`，不能用 `bits() + y * width * bytesPerPixel` 替代，因为有 `bytesPerLine()` 填充。

### 包装外部图像缓冲区

```cpp
QImage view(externalData, width, height, stride,
            QImage::Format_RGBA8888,
            cleanupCallback, cleanupContext);
```

外部内存必须在 `QImage` 及其共享副本不再引用前持续有效。传入 cleanup 回调时，要明确定义谁释放 `externalData`；不传时 Qt 不拥有该内存。若后续调用非 const `bits()` 或修改像素，可能 detach 成 Qt 自己的缓冲区，不能再把它当作永远零拷贝的视图。

### 正确转换颜色空间

```cpp
if (image.colorSpace().isValid()) {
    image.convertToColorSpace(QColorSpace::SRgb,
                              QImage::Format_ARGB32_Premultiplied);
}
```

`setColorSpace(QColorSpace::SRgb)` 只贴标签，不会改像素数值。来自 Display P3 或带 ICC profile 的图片若只是改标签，颜色会错；要调用 `convertToColorSpace()` 或 `applyColorTransform()`。

### 处理高 DPI 图像

```cpp
QImage icon(":/icons/close@2x.png");
icon.setDevicePixelRatio(2.0);

const QSizeF logicalSize = icon.deviceIndependentSize();
painter.drawImage(QPointF(0, 0), icon);
```

`size()` 是物理像素尺寸；UI 布局和目标逻辑尺寸应使用 `deviceIndependentSize()` 或除以 DPR。DPR 是显示解释，不会重新采样图片。

## 6. 常见坑与经验

- **读写 `bits()` 会影响共享。** 非 const `bits()`、`scanLine()` 可能触发 detach；后台算法若只读，使用 `constBits()`/`constScanLine()`。
- **单像素 API 不适合大图热循环。** `pixelColor()` / `setPixelColor()` 处理格式转换，百万像素循环应统一格式后走 scanline。
- **`reinterpretAsFormat()` 不是转换。** 它仅改格式标签；只有通道布局和 alpha 语义真的兼容时才可用。
- **`allGray()` 与 `isGrayscale()` 不同。** 前者检查当前像素内容是否灰，后者关注图像的灰度格式/色表语义。
- **缩放先判断目的。** 缩略图用 `scaled(..., SmoothTransformation)`；动态视图连续缩放时，交给 painter 的 transform 往往更划算。
- **`setAlphaChannel()` 会覆盖旧 alpha。** 它不是“叠加遮罩”；源 alpha 的合成需要你自己选择规则。
- **不要忽略格式限制。** `QPainter` 对 `ARGB32_Premultiplied`、`RGB32` 等支持最好；索引色和 CMYK 不可直接作为一般画布。
- **资源失败只会得到空图。** 文件构造函数不抛异常，读取后立即检查 `isNull()` 或改用 `QImageReader` 获取错误详情。

## 7. 知识点覆盖

CPU 像素缓冲区、隐式共享、行跨度、外部内存生命周期、预乘 alpha、像素格式、离屏绘制、颜色空间、高 DPI、元数据、线程所有权、图像转换与性能。
