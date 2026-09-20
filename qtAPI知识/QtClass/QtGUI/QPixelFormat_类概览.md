# QPixelFormat：描述图形缓冲区中的像素布局

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPixelFormat>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Gui)`，并链接 `Qt6::Gui`

`QPixelFormat` 是一个轻量值对象，用来说明图形缓冲区中一个像素的颜色模型、各通道位数、alpha 规则、数据单元类型、字节序和 YUV 布局。`QImage::pixelFormat()`、视频帧和平台图像接口会用它报告或协商格式。

它**不持有像素数据**，不包含行跨度、平面偏移、内存对齐、图像尺寸或颜色空间转换信息。它能回答“每个像素按什么规则解释”，不能单独回答“第 n 个像素在内存的哪个字节”。

## 它解决的问题

只看“32 位”无法判断像素该怎么读：它可能是 ARGB、RGBA、RGBX，可能是预乘 alpha，也可能按 `uint32` 或四个字节处理。`QPixelFormat` 把这些描述拆开，使代码可在格式不同的图像、视频或 surface 之间进行选择和检查。

```cpp
QImage image("logo.png");
const QPixelFormat format = image.pixelFormat();

if (format.alphaUsage() == QPixelFormat::UsesAlpha
    && format.premultiplied() == QPixelFormat::Premultiplied) {
    // 选择与预乘 alpha 相容的处理路径。
}
```

实际图像处理通常以 `QImage::format()`、`QImage::pixelFormat()`、`bytesPerLine()` 和 `constScanLine()` 等 API 共同决定访问方式。不要只根据 `QPixelFormat` 直接转换裸指针类型。

## 描述的四个层面

### 1. 颜色模型与通道位数

`ColorModel` 表示通道的语义：`RGB`、`BGR`、`Indexed`、`Grayscale`、`CMYK`、`HSL`、`HSV`、`YUV` 或仅 alpha。最多可描述五个颜色通道和一个 alpha 通道。

对 RGB 模型，`redSize()`、`greenSize()`、`blueSize()` 返回对应位数；对 CMYK，前四个位置以 `cyanSize()`、`magentaSize()`、`yellowSize()`、`blackSize()` 命名；对 HSL/HSV，则同一组位置以 hue、saturation、lightness/brightness 命名。

这些访问器只是同一字段在不同色彩模型下的语义别名。对 CMYK 格式调用 `redSize()` 虽可能返回第一通道宽度，但没有“红色位数”的业务含义。先检查 `colorModel()` 再选择正确的访问器。

### 2. Alpha 的存在、位置与预乘

alpha 有三个彼此独立的维度：

| 属性 | 要回答的问题 |
| --- | --- |
| `alphaSize()` | alpha 字段占多少 bit。 |
| `alphaUsage()` | 该字段是否参与透明度计算。 |
| `alphaPosition()` | alpha 在颜色通道之前（如 ARGB）还是之后（如 RGBA）。 |
| `premultiplied()` | 颜色分量是否已经乘过 alpha。 |

“有 8 个 alpha bit”不等价于“使用透明度”：可以构造 32 位 RGBX 一类格式，其中 alpha 位存在但 `IgnoresAlpha`。预乘格式则要求颜色通道已按 alpha 缩放；把预乘数据当作直 alpha，或反过来处理，常造成半透明边缘发黑、发白或颜色过亮。

### 3. 类型解释和字节序

`typeInterpretation()` 说明每个像素单元应作为什么类型读取：

- `UnsignedByte`：按一个或多个 `uchar` 单元读取，例如常见的三字节 RGB。
- `UnsignedShort`：按一个或多个 16 位无符号单元读取。
- `UnsignedInteger`：按一个或多个无符号整型单元读取，许多 32 位 `QImage` 格式属于此类。
- `FloatingPoint`：依据通道大小解释为半精度或单精度浮点等浮点格式。

`byteOrder()` 影响**每个读取单元内**的字节顺序，不改变多个单元彼此的相对顺序。`CurrentSystemEndian` 只是构造参数便利值，构造时会转换并存储成当前系统实际的 `LittleEndian` 或 `BigEndian`，不会作为“动态跟随系统”的值保留下来。

例如 `QImage::Format_ARGB32` 按 `UnsignedInteger` 解释时可用 `0xFF000000` 掩码读取 alpha，而不必因主机字节序改变掩码；但如果把同一内存粗暴视为连续 R/G/B/A 字节，结果会随字节序而变化。格式与主机字节序不匹配时，`QImage` 不会为了迎合主机而自动交换内部 bit。

### 4. YUV 不按普通通道模型描述

YUV 的子采样与宏像素会跨越多个像素或平面，无法用“本像素有几个 R/G/B 通道”完整表达。对于 `ColorModel::YUV`，`QPixelFormat` 用 `YUVLayout` 标识布局，`bitsPerPixel()` 由布局推导。

这仍不足以替代实际视频帧的平面信息：YUV420P、NV12 等格式通常涉及多个平面、行对齐和步长。访问视频缓冲应使用对应帧/平面 API，而不是假设 `bitsPerPixel() / 8` 就是每个像素的可用内存跨度。

## 用辅助构造函数表达意图

直接使用完整构造器时，`firstSize` 到 `fifthSize` 的含义随颜色模型变化，容易传错。优先使用语义化辅助函数：

```cpp
const QPixelFormat rgba8 =
    qPixelFormatRgba(8, 8, 8, 8,
                     QPixelFormat::UsesAlpha,
                     QPixelFormat::AtEnd,
                     QPixelFormat::NotPremultiplied,
                     QPixelFormat::UnsignedByte);

const QPixelFormat mask =
    qPixelFormatAlpha(1, QPixelFormat::UnsignedByte);
```

`qPixelFormatRgba()` 把 RGB 通道大小、alpha 使用方式、位置和预乘规则显式列出；`qPixelFormatGrayscale()`、`qPixelFormatAlpha()`、`qPixelFormatCmyk()`、`qPixelFormatHsl()`、`qPixelFormatHsv()`、`qPixelFormatYuv()` 分别避免调用方手工映射通道字段。

默认构造对象的所有字段为零，不应把它当作“默认 RGB 图像格式”。要描述实际数据，始终从产生数据的 `QImage` / 视频帧读取格式，或用明确构造函数创建。

## 常见使用场景

- 在图像导入或处理管线中检查 alpha 是否可用、是否预乘，决定走哪个转换或合成分支。
- 在自定义图像缓存中按 `colorModel()` 和通道精度选择 SIMD 或颜色转换实现。
- 在视频输出代码中识别 NV12、YUYV、Y8 等 YUV layout，并转交给对应的平台/图形后端。
- 在调试中打印 `QImage::pixelFormat()`，解释“同样是 32 位”为何颜色顺序或透明边缘不同。

它不是颜色管理 API。`QPixelFormat` 描述样本布局，不描述 sRGB、Display P3、ICC profile 或 gamma；这些属于 `QColorSpace` 和具体图像/媒体对象的颜色空间信息。

## 常见错误

- 将 `bitsPerPixel() / 8` 当作 `bytesPerLine()` 或所有格式的单像素寻址步长：有行填充、位打包和多平面 YUV 时都不成立。
- 把 `AtBeginning` / `AtEnd` 当作内存中永远固定的“第一个字节/最后一个字节”：还必须结合 `typeInterpretation()` 与 `byteOrder()`。
- 看见 `alphaSize() > 0` 就进行 alpha 混合：还要检查 `alphaUsage()`。
- 把 `Premultiplied` 数据按直 alpha 写入：会破坏半透明颜色。
- 对任何颜色模型都读取 `redSize()`：先检查颜色模型并使用语义相符的通道访问器。
- 试图用 `QPixelFormat` 单独推导 YUV 平面地址：必须用帧实际的 plane、stride 和映射信息。

## API 速查表

### 构造与整体属性

| API | 语义与使用边界 |
| --- | --- |
| `QPixelFormat()` | 构造所有字段为零的空描述；不是常用图像格式。 |
| 完整构造器 | 直接指定模型、五个颜色通道、alpha、类型、字节序和子枚举；仅在确实了解目标布局时使用。 |
| `colorModel()` | 返回颜色模型，决定各通道尺寸访问器的语义。 |
| `channelCount()` | 返回非零颜色通道与 alpha 通道的数量；不是 YUV 平面数。 |
| `bitsPerPixel()` | 返回描述的每像素 bit 数；不能替代行跨度、像素地址或 YUV plane 布局。 |
| `operator==` / `operator!=` | 比较整个格式描述是否完全相同。 |
| `QDebug <<` | 输出调试格式描述；仅在启用调试流时可用。 |

### 通道大小

| API | 适用模型与含义 |
| --- | --- |
| `redSize()` / `greenSize()` / `blueSize()` | RGB/BGR 的 R、G、B 通道位数。 |
| `cyanSize()` / `magentaSize()` / `yellowSize()` / `blackSize()` | CMYK 的 C、M、Y、K 通道位数。 |
| `hueSize()` / `saturationSize()` / `lightnessSize()` | HSL 的 H、S、L 通道位数。 |
| `hueSize()` / `saturationSize()` / `brightnessSize()` | HSV 的 H、S、V 通道位数。 |
| `alphaSize()` | alpha 字段位数；是否真正参与混合还要看 `alphaUsage()`。 |

### Alpha、类型与字节序

| API | 语义与使用边界 |
| --- | --- |
| `alphaUsage()` | 返回 `UsesAlpha` 或 `IgnoresAlpha`。 |
| `alphaPosition()` | 返回 alpha 在颜色通道前的 `AtBeginning` 或后的 `AtEnd`。 |
| `premultiplied()` | 返回 `Premultiplied` 或 `NotPremultiplied`。 |
| `typeInterpretation()` | 返回像素单元按无符号整数、短整数、字节或浮点解释的方式。 |
| `byteOrder()` | 返回每个读取单元的字节序；不改变多个单元的相对顺序。 |
| `yuvLayout()` | 返回 YUV 宏像素/平面布局枚举；仅在 YUV 模型时有意义。 |
| `subEnum()` | 返回内部子枚举值；常规代码应优先使用 `yuvLayout()` 等有语义的访问器。 |

### 非成员辅助构造函数

| API | 语义与使用边界 |
| --- | --- |
| `qPixelFormatRgba(...)` | 构造 RGB/RGBA 描述，显式给出每个颜色通道和 alpha 规则。 |
| `qPixelFormatGrayscale(channelSize, type)` | 构造灰度格式；通道大小为 `1` 可表示单色格式。 |
| `qPixelFormatAlpha(channelSize, type)` | 构造仅 alpha 格式；通道大小为 `1` 可表示掩码。 |
| `qPixelFormatCmyk(...)` | 构造四个同位数 CMYK 通道及可选 alpha 的格式。 |
| `qPixelFormatHsl(...)` | 构造 HSL 格式，H/S/L 使用相同通道大小。 |
| `qPixelFormatHsv(...)` | 构造 HSV 格式，H/S/V 使用相同通道大小。 |
| `qPixelFormatYuv(layout, ...)` | 构造指定 YUV layout 的格式；真实 plane 与 stride 仍由图像/视频帧提供。 |

### 枚举

| 枚举 | 取值与含义 |
| --- | --- |
| `ColorModel` | `RGB`、`BGR`、`Indexed`、`Grayscale`、`CMYK`、`HSL`、`HSV`、`YUV`、`Alpha`。 |
| `AlphaUsage` | `UsesAlpha` 表示 alpha 参与透明度；`IgnoresAlpha` 表示忽略其值。 |
| `AlphaPosition` | `AtBeginning` 如 ARGB；`AtEnd` 如 RGBA。 |
| `AlphaPremultiplied` | `NotPremultiplied` 为直 alpha；`Premultiplied` 为颜色已乘 alpha。 |
| `TypeInterpretation` | `UnsignedInteger`、`UnsignedShort`、`UnsignedByte`、`FloatingPoint`。 |
| `ByteOrder` | `LittleEndian`、`BigEndian`、构造时解析为实际字节序的 `CurrentSystemEndian`。 |
| `YUVLayout` | `YUV444`、`YUV422`、`YUV411`、`YUV420P`、`YUV420SP`、`YV12`、`UYVY`、`YUYV`、`NV12`、`NV21`、`IMC1` 至 `IMC4`、`Y8`、`Y16`。 |
