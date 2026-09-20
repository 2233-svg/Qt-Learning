# QRgba64

> Qt 6.11.1 · Qt GUI · 来自 `QRgba64`

## 1. 先建立直觉

`QRgba64` 是一个 64 位 RGBA 颜色值：红、绿、蓝、alpha 各 16 bit。它比传统 32 位 ARGB/RGBA 每通道 8 bit 的颜色能保留更多精度，适合高位深图像、颜色转换、中间计算和避免渐变/混合时的量化损失。

它不是 `QColor` 那种带颜色空间和多种模型语义的高层颜色对象，而是紧凑的 RGBA 通道容器。你通常在图像像素处理、`QImage` 高位深格式、颜色转换底层代码里遇到它。

## 2. 类说明

- 头文件：`#include <QRgba64>`
- CMake：`Qt6::Gui`
- 类型性质：小型值类型，很多函数为 `constexpr`
- 通道精度：R/G/B/A 各 16 bit
- 可转换格式：32 位 ARGB、16 位 RGB、64 位打包值

`QRgba64` 的 16 位通道范围是 `0..65535`。`red8()` / `green8()` 等 8 位访问器会降精度，适合与旧 8 位 API 交互，不适合做高精度处理中间值。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `fromRgba64(quint16 r,g,b,a)` | 从四个 16 位通道创建颜色。 |
| `fromRgba64(quint64 c)` | 从 64 位打包值创建。 |
| `fromRgba(quint8 r,g,b,a)` | 从 8 位通道创建，内部扩展到 16 位。 |
| `fromArgb32(uint rgb)` | 从 32 位 ARGB 创建。 |
| `red()` / `green()` / `blue()` / `alpha()` | 读取 16 位通道。 |
| `red8()` / `green8()` / `blue8()` / `alpha8()` | 读取降采样后的 8 位通道。 |
| `setRed()` / `setGreen()` / `setBlue()` / `setAlpha()` | 设置 16 位通道。 |
| `isOpaque()` | alpha 是否为最大值。 |
| `isTransparent()` | alpha 是否为 0。 |
| `premultiplied()` | 返回 RGB 已按 alpha 预乘后的颜色。 |
| `unpremultiplied()` | 从预乘形式还原为非预乘颜色。 |
| `toArgb32()` | 转成 32 位 ARGB，会损失通道精度。 |
| `toRgb16()` | 转成 16 位 RGB565。 |
| `operator quint64()` | 取得底层 64 位打包值。 |
| `qHash(QRgba64)` | Qt 6.11.1 起支持哈希，可用于哈希容器键。 |

## 4. 关键用法

### 高位深通道处理

```cpp
QRgba64 c = QRgba64::fromRgba64(50000, 32000, 12000, 65535);

const quint16 r = c.red();
const quint8 r8 = c.red8();
```

`r` 保留 16 位精度；`r8` 是为了兼容 8 位路径的结果。做颜色计算时尽量留在 16 位，最后输出时再降采样。

### 预乘 alpha

```cpp
QRgba64 src = QRgba64::fromRgba64(40000, 20000, 10000, 32768);
QRgba64 pm = src.premultiplied();
```

预乘格式常用于图像合成，因为混合计算更高效，也更符合许多 raster 引擎的内部表示。不要把预乘后的 RGB 当作原始颜色显示或再次预乘。

### 转成传统 32 位 ARGB

```cpp
uint argb = color.toArgb32();
```

这一步会把每个 16 位通道压到 8 位。用于旧 API 或低位深输出可以，若后续还要继续处理颜色，最好保留 `QRgba64`。

## 5. 使用场景

- 高位深 `QImage` 像素处理。
- 颜色渐变、合成、滤镜的中间计算。
- 从 8 位颜色升级到 16 位内部精度。
- 需要显式控制 premultiplied alpha 的 raster 管线。
- 哈希颜色值或把颜色作为轻量键值保存。

## 6. 常见坑与经验

- **16 位通道不是 0..255。** 直接把 `255` 当最大值会得到很暗的颜色；最大值是 `65535`。
- **8 位访问器会丢精度。** `red8()` 是输出/兼容工具，不是高精度处理入口。
- **预乘和非预乘不能混用。** 混用会导致半透明边缘发暗或颜色错误。
- **`toArgb32()` 是降采样。** 转换后无法恢复 16 位细节。
- **`isTransparent()` 只看 alpha。** RGB 即使有值，只要 alpha 为 0，视觉上就是完全透明。
- **`QColor` 语义更丰富。** 需要颜色空间、HSL/HSV/CMYK 等模型时，用 `QColor` 或 `QColorSpace` 配合。

## 7. 知识点覆盖

- 每通道 16 位 RGBA 与 8 位 ARGB 的区别
- 高位深图像处理和量化损失
- premultiplied alpha 与 unpremultiplied alpha
- 64 位打包、32 位 ARGB、RGB565 转换
- 透明、不透明和 alpha 通道判断
- `QRgba64` 与 `QColor`、`QImage` 像素格式的关系
