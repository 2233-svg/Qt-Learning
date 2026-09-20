# QPixelFormat

> Qt 6.11.1 · Qt GUI · 来自 `QPixelFormat`

## 1. 先建立直觉

`QPixelFormat` 是像素布局的描述对象：一个像素使用什么颜色模型，每个通道多少 bit，alpha 在前还是在后，是否预乘，数据按整数、字节、短整型还是浮点解释，字节序如何，YUV 又是哪种平面/打包布局。

它不保存像素数据，也不负责转换图片。它回答的是“这块内存里的每个像素应该怎样读”。`QImage::pixelFormat()`、图像导入导出、视频帧处理和底层渲染接口都会用到这种描述。

## 2. 类说明

- 头文件：`#include <QPixelFormat>`
- CMake：`Qt6::Gui`
- 类型性质：小型值类型，很多函数为 `constexpr noexcept`
- 典型来源：`QImage::pixelFormat()` 或 `qPixelFormat...()` 工厂函数
- 主要关注：颜色模型、通道位数、alpha、预乘、类型解释、端序、YUV 子格式

不要把 `QPixelFormat` 和 `QImage::Format` 混为一谈。`QImage::Format` 是 Qt 预定义图像格式枚举；`QPixelFormat` 是更通用的结构化描述，能表达更多底层属性。

## 3. API 速查

| API / 枚举 | 作用 |
| --- | --- |
| `ColorModel` | 颜色模型：`RGB`、`BGR`、`Indexed`、`Grayscale`、`CMYK`、`HSL`、`HSV`、`YUV`、`Alpha`。 |
| `AlphaUsage` | 是否使用 alpha：`UsesAlpha` 或 `IgnoresAlpha`。 |
| `AlphaPosition` | alpha 在颜色通道前还是后：`AtBeginning` / `AtEnd`。 |
| `AlphaPremultiplied` | 颜色通道是否已乘以 alpha。 |
| `TypeInterpretation` | 通道数据按无符号整数、short、byte 或浮点解释。 |
| `ByteOrder` | 多字节/打包像素的字节序。 |
| `YUVLayout` | YUV 的具体布局，如 `YUV420P`、`NV12`、`YUYV`、`Y8`、`Y16`。 |
| `bitsPerPixel()` | 每像素总 bit 数。 |
| `channelCount()` | 实际通道数。 |
| `redSize()` / `greenSize()` / `blueSize()` | RGB/BGR 通道位数。 |
| `cyanSize()` / `magentaSize()` / `yellowSize()` / `blackSize()` | CMYK 通道位数。 |
| `hueSize()` / `saturationSize()` / `lightnessSize()` / `brightnessSize()` | HSL/HSV 通道位数。 |
| `alphaSize()` / `alphaUsage()` / `alphaPosition()` | alpha 通道大小、是否使用以及位置。 |
| `premultiplied()` | 是否为 premultiplied alpha。 |
| `byteOrder()` | 查询端序。 |
| `typeInterpretation()` | 查询通道数据解释方式。 |
| `yuvLayout()` | 查询 YUV 子布局。 |
| `qPixelFormatRgba()` | 构造 RGBA/RGB 类格式描述。 |
| `qPixelFormatGrayscale()` / `qPixelFormatAlpha()` | 构造灰度或纯 alpha 格式。 |
| `qPixelFormatCmyk()` | 构造 CMYK 格式。 |
| `qPixelFormatHsl()` / `qPixelFormatHsv()` | 构造 HSL/HSV 格式。 |
| `qPixelFormatYuv()` | 构造指定 YUV layout 的格式。 |

## 4. 关键用法

### 检查 QImage 的 alpha 语义

```cpp
const QPixelFormat fmt = image.pixelFormat();

if (fmt.alphaUsage() == QPixelFormat::UsesAlpha &&
    fmt.premultiplied() == QPixelFormat::Premultiplied) {
    // 可按预乘 alpha 路径处理
}
```

`alphaSize() > 0` 不一定代表 alpha 被使用。例如一些 32 位 RGB 格式保留了 alpha 位，但 `alphaUsage()` 可能是 `IgnoresAlpha`。

### 构造一个 RGBA 描述

```cpp
QPixelFormat rgba8888 = qPixelFormatRgba(
    8, 8, 8, 8,
    QPixelFormat::UsesAlpha,
    QPixelFormat::AtEnd,
    QPixelFormat::NotPremultiplied,
    QPixelFormat::UnsignedByte);
```

这种描述适合告诉底层接口“我传入的数据是每通道 8 bit 的 RGBA 字节序列”。真正的数据仍然由 `QImage`、视频帧或你的内存缓冲区持有。

### 识别视频常见 YUV 格式

```cpp
if (fmt.colorModel() == QPixelFormat::YUV &&
    fmt.yuvLayout() == QPixelFormat::NV12) {
    uploadNv12Frame(frameData);
}
```

YUV 的复杂度不在“有没有 Y、U、V”，而在平面数量、采样比例和字节排列。`YUV420P`、`NV12`、`YUYV` 不能只靠通道数判断。

## 5. 使用场景

- 图像加载后检查格式，决定是否需要转换。
- 视频帧导入：识别 NV12、YUV420P、YUYV 等布局。
- 与 GPU/渲染后端交换纹理数据时描述通道布局。
- 处理 premultiplied alpha，避免边缘黑边或错误混合。
- 写图像编解码、像素转换、截图或屏幕捕获工具。

## 6. 常见坑与经验

- **格式描述不是数据。** `QPixelFormat` 不持有 pixels，也不说明每行 stride。
- **BGR 不是 RGB 加反向端序。** Qt 给 BGR 单独的 color model，别用 RGB 的 byte order 去硬凑。
- **alpha 位存在不等于使用 alpha。** 同时看 `alphaSize()` 和 `alphaUsage()`。
- **预乘 alpha 会改变颜色通道含义。** 预乘格式里 RGB 已经乘过 alpha，不能当普通 RGB 直接混合。
- **端序只在多字节/打包解释时关键。** `UnsignedByte` 连续字节格式和 32 位整数打包格式的思考方式不同。
- **YUV layout 决定内存访问。** NV12 是半平面，YUV420P 是平面，YUYV 是打包；读错会出现颜色错乱。
- **`bitsPerPixel()` 不等于有效颜色精度。** padding、未使用 alpha、索引色等都会让“总 bit”与视觉色深不是一回事。

## 7. 知识点覆盖

- 颜色模型与通道位数的结构化描述
- alpha 使用、位置和 premultiplied alpha
- `QImage::Format` 与 `QPixelFormat` 的区别
- 字节序、打包像素和类型解释
- RGB/BGR、灰度、CMYK、HSL/HSV、YUV、Alpha 格式
- 视频 YUV layout 与图像内存解释
