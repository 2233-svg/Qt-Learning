# QVideoFrameFormat：描述视频帧的像素布局与呈现规则

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QVideoFrameFormat>`  
> 所属模块：`Qt6::Multimedia`  
> 继承：无  
> 类型性质：显式共享值类型

## 它解决什么问题

`QVideoFrameFormat` 描述一条视频流中“帧是什么样，以及应该怎样呈现”。它定义的不只是宽高，还包括：

- 像素格式和底层平面布局；
- 实际显示区域 `viewport`；
- 扫描线方向；
- 流帧率；
- 色彩空间、传递函数和色彩范围；
- 旋转、镜像；
- 面向底层 RHI 渲染的 shader 和亮度信息。

它与 `QVideoFrame` 的关系是：`QVideoFrameFormat` 描述格式，`QVideoFrame` 携带一帧具体数据并可以拥有或引用视频缓冲。格式对象本身不保存视频像素。

## 实际使用场景

- 创建 `QVideoFrame` 或 `QVideoFrameInput` 时声明视频帧尺寸和像素格式；
- 检查摄像头实际输出与算法或编码器要求是否匹配；
- 解释 `QVideoFrame` 映射出来的 RGB、YUV 多平面数据；
- 保留视频的色彩元数据，避免把 HDR 或 limited range 视频错误当成普通 SDR；
- 自定义视频渲染时读取 viewport、旋转、镜像和 RHI shader 配置；
- 在 `QImage` 与视频像素格式之间做可行性判断。

## 创建和有效性

```cpp
QVideoFrameFormat format(
        QSize(1920, 1080),
        QVideoFrameFormat::Format_NV12);

if (format.isValid()) {
    qDebug() << format.frameSize()
             << format.planeCount()
             << format.streamFrameRate();
}
```

默认构造产生无效格式。`QVideoFrameFormat(const QSize &, PixelFormat)` 至少需要有效尺寸和有效像素格式，`isValid()` 才会返回 `true`。

这是显式共享值类型。复制格式对象通常共享内部描述数据，不复制任何视频像素。`detach()` 可将当前对象与共享数据分离，适合需要独立修改格式描述的场景；它不会复制视频帧缓冲。

```cpp
QVideoFrameFormat a(QSize(1280, 720),
                    QVideoFrameFormat::Format_ARGB8888);
QVideoFrameFormat b = a;
b.detach();
b.setFrameSize(640, 480);
```

## `PixelFormat`：像素格式不是颜色空间

`PixelFormat` 描述字节或纹理的存储布局；它不单独决定 BT.601、BT.709、HDR 或 limited/full range。解释 YUV 数据时，还必须结合 `colorSpace()`、`colorTransfer()` 和 `colorRange()`。

### RGB 和带 alpha 格式

| 枚举 | 含义和使用重点 |
| --- | --- |
| `Format_ARGB8888` | 每个分量 8 位的 ARGB 格式。 |
| `Format_ARGB8888_Premultiplied` | 预乘 alpha 的 8 位 ARGB；混合时应按预乘规则处理。 |
| `Format_XRGB8888` | 32 位 RGB，最高字节为不透明占位值 `0xff`。 |
| `Format_BGRA8888` | 32 位 BGRA，内存/数值布局为 `0xBBGGRRAA`。 |
| `Format_BGRA8888_Premultiplied` | 预乘 alpha 的 BGRA。 |
| `Format_BGRX8888` | 32 位 BGRx，x 为不使用的占位分量。 |
| `Format_ABGR8888` | 32 位 ABGR，布局为 `0xAABBGGRR`。 |
| `Format_XBGR8888` | 32 位 BGR，最高分量为不透明占位值。 |
| `Format_RGBA8888` | 内存中按 R、G、B、A/X 字节顺序存储。 |
| `Format_RGBX8888` | 内存中按 R、G、B、X 字节顺序存储。 |

`ARGB8888`、`BGRA8888` 等名称容易被误读为“内存中一定按名称从低地址到高地址排列”。实际解释还涉及平台字节序、Qt 对格式的定义以及底层后端，不能仅凭变量名做指针强转。需要逐字节处理时，应根据 Qt 文档和实际平台验证布局。

### AYUV、packed YUV、planar YUV

| 枚举 | 布局和边界 |
| --- | --- |
| `Format_AYUV` | packed 32 位 AYUV，布局 `0xAAYYUUVV`。 |
| `Format_AYUV_Premultiplied` | 预乘 alpha 的 packed AYUV。 |
| `Format_YUV420P` | 8 位 planar YUV；U、V 平面宽高均为 Y 平面的一半。 |
| `Format_YUV422P` | 8 位 planar YUV；U、V 平面宽度为 Y 的一半，高度与 Y 相同。 |
| `Format_YV12` | 8 位 planar YVU；平面顺序是 V、U，宽高均为 Y 的一半。 |
| `Format_UYVY` | packed 8 位 YUV；两个横向相邻像素组成 `U-Y-V-Y` 的 32 位宏像素。 |
| `Format_YUYV` | packed 8 位 YUV；两个横向相邻像素组成 `Y-U-Y-V` 的 32 位宏像素。 |

`YUV420P` 和 `YV12` 都是三平面 4:2:0，但 U/V 顺序不同。`UYVY` 和 `YUYV` 都是 packed 格式，也不能按三个独立平面访问。

### 半平面和 IMC 格式

| 枚举 | 布局和边界 |
| --- | --- |
| `Format_NV12` | Y 平面后接 4:2:0 采样的 packed UV 平面，顺序 U-V。 |
| `Format_NV21` | Y 平面后接 4:2:0 采样的 packed VU 平面，顺序 V-U。 |
| `Format_IMC1` | 类似 `YUV420P`，但 U/V 行跨度填充到与 Y 相同。 |
| `Format_IMC2` | 类似 `YUV420P`，但 U/V 行交错，每行 U 后跟一行 V，共用 Y 的跨度。 |
| `Format_IMC3` | 类似 `YV12`，但 V/U 行跨度填充到与 Y 相同。 |
| `Format_IMC4` | 类似 `YV12`，但 V/U 行交错，每行 V 后跟一行 U，共用 Y 的跨度。 |

这些格式名字相似但内存组织不同。正确代码应读取 `QVideoFrame::planeCount()`、`bytesPerLine(plane)` 和实际平面地址，不能只根据宽高计算连续内存偏移。

### 灰度、高位深度和特殊格式

| 枚举 | 含义和使用重点 |
| --- | --- |
| `Format_Y8` | 8 位灰度。 |
| `Format_Y16` | 16 位线性灰度，小端序。 |
| `Format_P010` | 16 位分量的半平面 YUV，只有每个分量最高 10 位有效，Y 后接 UV。 |
| `Format_P016` | 16 位分量的半平面 YUV，Y 后接 UV。 |
| `Format_SamplerExternalOES` | 外部 OES 纹理格式，目前主要用于 Android。 |
| `Format_Jpeg` | 压缩 JPEG 帧，不是可直接按未压缩像素行访问的 RGB。 |
| `Format_SamplerRect` | 矩形纹理格式，目前仅用于 macOS 的 OpenGL RHI；纹理底层像素格式为 `Format_BGRA8888`。 |
| `Format_YUV420P10` | 类似 `YUV420`，但每个分量占 16 位，其中 10 位有效。 |
| `Format_Invalid` | 无效格式。 |

高位深度格式不应简单地按 8 位数组读取；还要确认有效位的位置、端序、平面跨度和色彩范围。`Format_Jpeg` 的 `map()` 数据是压缩码流语义，不能套用普通 YUV 行数公式。纹理格式则可能根本没有可用的 CPU 平面。

## 尺寸、viewport 和平面数

`frameSize()` 是底层帧的尺寸，`frameWidth()` 和 `frameHeight()` 是便捷查询。`viewport()` 是真正要显示的区域，默认覆盖整个帧。

底层帧有时为了行对齐或后端最优尺寸而比有效视频区域更大，例如宽度被扩展到满足字节对齐。此时可以让 `frameSize()` 保留底层尺寸，用 `viewport()` 表示实际画面区域。

```cpp
QVideoFrameFormat format(
        QSize(1928, 1080),
        QVideoFrameFormat::Format_NV12);
format.setViewport(QRect(0, 0, 1920, 1080));
```

调用任一 `setFrameSize()` 重置 `viewport()`，使其重新覆盖整个帧。因此如果改变尺寸后仍需要裁剪区域，必须重新设置 viewport。

`planeCount()` 由像素格式决定：RGB 通常是 1；YUV 通常是 1 到 3。它是格式层面的平面数量提示，实际映射时仍应以 `QVideoFrame` 的实际结果和后端能力为准。

## 扫描方向

`scanLineDirection()` 描述扫描线从上到下还是从下到上：

- `TopToBottom`：第一行是画面顶部，随后向底部排列；
- `BottomToTop`：第一行是画面底部，随后向顶部排列。

它不是旋转属性，也不是镜像属性。改变扫描线方向不会自动重排 `bits()` 返回的内存；自定义 CPU 处理器必须在解释行地址时考虑该元数据。

## 帧率与三类色彩元数据

### 帧率

`streamFrameRate()` 和 `setStreamFrameRate()` 使用帧/秒。Qt 6.8 起，旧的 `frameRate()` 和 `setFrameRate()` 已弃用，应使用带 `stream` 前缀的新 API。

帧率是流描述或编码初始化信息，不是“每隔多少毫秒调用一次槽”的保证。可变帧率视频不能只靠一个固定 `streamFrameRate()` 推断每帧的真实呈现时间，应优先使用帧时间戳。

### 色彩空间、传递函数、范围

这三个属性表达不同层次的语义：

| 属性 | 说明 |
| --- | --- |
| `colorSpace()` | 原色、矩阵等颜色空间语义，如 BT.601、BT.709、BT.2020。 |
| `colorTransfer()` | 数值如何通过传递曲线编码，如 BT.709、线性、Gamma 2.2、PQ/ST2084、HLG/STD B67。 |
| `colorRange()` | 使用视频 limited range 还是 full range。 |

常见值包括：

- `ColorSpace_Undefined`、`ColorSpace_BT601`、`ColorSpace_BT709`、`ColorSpace_AdobeRgb`、`ColorSpace_BT2020`；
- `ColorTransfer_Unknown`、`ColorTransfer_BT709`、`ColorTransfer_BT601`、`ColorTransfer_Linear`、`ColorTransfer_Gamma22`、`ColorTransfer_Gamma28`、`ColorTransfer_ST2084`、`ColorTransfer_STD_B67`；
- `ColorRange_Unknown`、`ColorRange_Video`、`ColorRange_Full`。

`ColorRange_Video` 对 8 位传统 YUV 通常表示 Y 为 16 到 235、色度为 16 到 240；高位深度按位深缩放。`ColorRange_Full` 表示使用从 0 到 `2^depth - 1` 的完整范围。

`Unknown` 或 `Undefined` 表示元数据缺失，不能擅自当成 BT.709、sRGB 或 full range。尤其在 HDR 场景中，BT.2020、ST2084、HLG 和亮度信息需要一起处理；只设置一个枚举不等于完成 HDR tone mapping。

## 旋转与镜像

`rotation()` / `setRotation()` 使用 `QtVideo::Rotation`：

- `None`
- `Clockwise90`
- `Clockwise180`
- `Clockwise270`

`isMirrored()` / `setMirrored()` 表示是否围绕垂直轴镜像。旋转先于镜像。这个“垂直轴镜像”与 `QImage::mirrored()` 中按参数命名的轴容易混淆，不能直接把两个 API 的布尔或方向含义互换。

旋转和镜像是表面呈现元数据，不会自动改写已经映射的像素排列。若转换成 `QImage` 后需要得到最终朝向，应用应显式执行相应图像变换。

## RHI/Shader 和最大亮度

`vertexShaderFileName()`、`fragmentShaderFileName()` 和 `updateUniformData()` 面向 Qt Multimedia 的底层视频渲染路径。它们用于 shader 文件和 uniform 数据契约，不是普通的图像滤镜 API。

```cpp
QByteArray uniforms;
QMatrix4x4 transform;
const float opacity = 1.0f;
format.updateUniformData(&uniforms, frame, transform, opacity);
```

调用者必须传入有效的目标 `QByteArray` 指针，并理解当前渲染后端约定的数据布局。普通 `QImage` 处理、`QVideoSink` 取帧或 QWidget 业务通常不需要调用这些函数。它们与 Qt 的内部渲染实现、shader 资源和 RHI 上下文密切相关，不能把返回的文件名或字节数组当作稳定的跨后端业务协议。

`maxLuminance()` / `setMaxLuminance()` 描述或设置最大亮度，主要服务于 HDR 和显示亮度映射。它不是简单的“把视频变亮/变暗”的用户音视频控制，也不替代色彩传递函数和 tone mapping。

## 静态转换 API

```cpp
const auto pixelFormat =
        QVideoFrameFormat::pixelFormatFromImageFormat(
                QImage::Format_ARGB32_Premultiplied);
const auto imageFormat =
        QVideoFrameFormat::imageFormatFromPixelFormat(pixelFormat);
const QString name =
        QVideoFrameFormat::pixelFormatToString(pixelFormat);
```

`pixelFormatFromImageFormat()` 和 `imageFormatFromPixelFormat()` 只在两种格式有等价表示时成功。没有对应格式时分别返回 `Format_Invalid` 或 `QImage::Format_Invalid`。一般情况下 `QImage` 不直接处理 YUV，因此不能期待 NV12、YUV420P 等都能转换成某个 `QImage::Format`。

`pixelFormatToString()` 适合日志、调试、诊断和 UI 显示。它是单向的字符串化 API，不应把显示字符串当作稳定的反向解析格式。

## 已弃用的色彩 API

Qt 6.4 起，`YCbCrColorSpace`、`yCbCrColorSpace()` 和 `setYCbCrColorSpace()` 已弃用。新代码使用 `ColorSpace`、`colorSpace()` 和 `setColorSpace()`，并分别使用 `ColorTransfer` 与 `ColorRange` 表达旧枚举无法清楚区分的传递函数和范围信息。

旧枚举中的 `YCbCr_xvYCC601`、`YCbCr_xvYCC709` 所表达的扩展范围概念，应结合新的 `ColorRange` 理解，而不是继续把范围塞进颜色空间枚举。

## 常见误区

- 只看 `PixelFormat`，不看色彩空间、transfer 和 range；
- 把 `frameSize()` 当成实际有效显示区域，忽略 viewport；
- `setFrameSize()` 后忘记 viewport 已被重置；
- 把 `YUV420P` 和 `YV12` 的 U/V 顺序混用；
- 把 NV12/NV21 或 IMC1-4 当成同一种连续内存布局；
- 把 `planeCount()` 写死为 1 或 3；
- 把 `scanLineDirection` 当成旋转或镜像；
- 把 Unknown/Undefined 擅自当成 BT.709 和 full range；
- 把 `streamFrameRate()` 当成实际每帧时间戳；
- 把 rotation 和 mirroring 误认为会修改像素；
- 在普通 QWidget 业务中依赖 shader/uniform 内部契约；
- 把 `maxLuminance` 当成简单亮度滑块；
- 认为所有视频格式都有对应的 `QImage::Format`；
- 新代码继续使用 Qt 6.4/6.8 已弃用 API。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `enum PixelFormat` | 描述视频像素存储格式。 | 不等于颜色空间；YUV 需结合平面布局和色彩元数据。 |
| 像素格式 | `Format_Invalid` | 表示无效格式。 | 不能创建可用视频帧。 |
| 像素格式 | `Format_ARGB8888` / `Format_ARGB8888_Premultiplied` | 8 位 ARGB，含普通和预乘 alpha。 | 预乘 alpha 不能按普通 alpha 直接混合。 |
| 像素格式 | `Format_XRGB8888` | 32 位 RGB，x 为不透明占位。 | x 分量不是可用 alpha。 |
| 像素格式 | `Format_BGRA8888` / `Format_BGRA8888_Premultiplied` | 32 位 BGRA，含普通和预乘 alpha。 | 注意内存布局和预乘规则。 |
| 像素格式 | `Format_BGRX8888` | 32 位 BGRx。 | x 分量只是占位。 |
| 像素格式 | `Format_ABGR8888` | 32 位 ABGR。 | 按 Qt 定义解释，不要只凭名称强转。 |
| 像素格式 | `Format_XBGR8888` | 32 位 BGR，x 为占位。 | 没有可用 alpha。 |
| 像素格式 | `Format_RGBA8888` / `Format_RGBX8888` | 按 R、G、B、A/X 字节顺序存储。 | 与整数数值显示顺序不要混淆。 |
| 像素格式 | `Format_AYUV` / `Format_AYUV_Premultiplied` | packed 32 位 AYUV，含普通和预乘 alpha。 | 不是三平面 YUV。 |
| 像素格式 | `Format_YUV420P` | 三平面 8 位 YUV 4:2:0，U/V 宽高减半。 | 平面顺序 Y、U、V。 |
| 像素格式 | `Format_YUV422P` | 三平面 8 位 YUV 4:2:2，U/V 宽度减半。 | U/V 高度与 Y 相同。 |
| 像素格式 | `Format_YV12` | 三平面 8 位 YVU 4:2:0。 | 平面顺序 Y、V、U。 |
| 像素格式 | `Format_UYVY` | packed `U-Y-V-Y`。 | 两个像素共用 U/V。 |
| 像素格式 | `Format_YUYV` | packed `Y-U-Y-V`。 | 两个像素共用 U/V。 |
| 像素格式 | `Format_NV12` | Y 平面加 packed UV 平面。 | UV 顺序是 U-V。 |
| 像素格式 | `Format_NV21` | Y 平面加 packed VU 平面。 | VU 顺序与 NV12 相反。 |
| 像素格式 | `Format_IMC1` | 4:2:0 planar，U/V 行跨度与 Y 对齐。 | 不能按普通 YUV420P 计算偏移。 |
| 像素格式 | `Format_IMC2` | 4:2:0 planar，U/V 行交错。 | 读取时处理交错行。 |
| 像素格式 | `Format_IMC3` | 4:2:0 YVU，V/U 行跨度与 Y 对齐。 | 平面顺序和跨度都不同。 |
| 像素格式 | `Format_IMC4` | 4:2:0 YVU，V/U 行交错。 | 读取时处理交错行。 |
| 像素格式 | `Format_Y8` | 8 位灰度。 | 不要当作 RGB 三通道。 |
| 像素格式 | `Format_Y16` | 16 位小端线性灰度。 | 注意端序和每像素字节数。 |
| 像素格式 | `Format_P010` | 16 位半平面 YUV，10 位有效。 | 有效位位置和端序不能按 8 位处理。 |
| 像素格式 | `Format_P016` | 16 位半平面 YUV。 | 按 16 位分量和实际跨度读取。 |
| 像素格式 | `Format_SamplerExternalOES` | 外部 OES 纹理。 | 主要面向 Android；不一定可 CPU 映射。 |
| 像素格式 | `Format_Jpeg` | 压缩 JPEG 帧。 | 按压缩数据处理，不套用未压缩行公式。 |
| 像素格式 | `Format_SamplerRect` | 矩形纹理格式。 | 主要用于 macOS OpenGL RHI。 |
| 像素格式 | `Format_YUV420P10` | 16 位存储、10 位有效的 YUV420。 | 需要正确处理高位深度和三平面布局。 |
| 枚举 | `enum Direction` | 描述扫描线方向。 | `TopToBottom` 或 `BottomToTop`。 |
| 枚举值 | `TopToBottom` | 从顶部到下方排列扫描线。 | 第一行对应画面顶部。 |
| 枚举值 | `BottomToTop` | 从底部到上方排列扫描线。 | 处理地址和显示方向时要考虑它。 |
| 枚举 | `enum ColorSpace` | 描述颜色空间。 | `Undefined` 不能擅自猜测。 |
| 枚举值 | `ColorSpace_Undefined` | 未指定颜色空间。 | 不要默认当作 BT.709。 |
| 枚举值 | `ColorSpace_BT601` | BT.601 颜色空间。 | 常见于较旧视频或特定 SD 内容。 |
| 枚举值 | `ColorSpace_BT709` | BT.709 颜色空间。 | 不能单独决定 range 和 transfer。 |
| 枚举值 | `ColorSpace_AdobeRgb` | Qt 枚举名对应 JPEG 常见的 full-range YUV 语义。 | 名称与常见 Adobe RGB 直觉不同，按 Qt 文档和实际上下文使用。 |
| 枚举值 | `ColorSpace_BT2020` | BT.2020 颜色空间。 | 常见于 HDR，但不等于自动完成 HDR 显示。 |
| 枚举 | `enum ColorTransfer` | 描述颜色传递曲线。 | 与 color space、range 是不同维度。 |
| 枚举值 | `ColorTransfer_Unknown` | 未知传递函数。 | 不要擅自假设 gamma 2.2。 |
| 枚举值 | `ColorTransfer_BT709` / `ColorTransfer_BT601` | 按 BT.709 或 BT.601 编码。 | 与对应颜色空间相关但不是同一个属性。 |
| 枚举值 | `ColorTransfer_Linear` | 线性颜色值。 | 适合线性工作空间语义。 |
| 枚举值 | `ColorTransfer_Gamma22` / `ColorTransfer_Gamma28` | gamma 2.2 或 2.8。 | 不要和 BT.709 曲线简单画等号。 |
| 枚举值 | `ColorTransfer_ST2084` | PQ/ST 2084 HDR 传递函数。 | 需要配合 HDR 显示和 tone mapping。 |
| 枚举值 | `ColorTransfer_STD_B67` | HLG/ARIB STD-B67 传递函数。 | 与 PQ 的处理路径不同。 |
| 枚举 | `enum ColorRange` | 描述视频范围。 | `Unknown`、`Video`、`Full`。 |
| 枚举值 | `ColorRange_Unknown` | 未知范围。 | 不要默认 full。 |
| 枚举值 | `ColorRange_Video` | 传统 video/limited range。 | 8 位 Y 通常 16-235，色度 16-240。 |
| 枚举值 | `ColorRange_Full` | 使用完整数值范围。 | 不能只凭 RGB/YUV 格式名称判断。 |
| 构造 | `QVideoFrameFormat()` | 创建无效格式。 | 需要设置有效尺寸和像素格式。 |
| 构造 | `QVideoFrameFormat(const QSize &, PixelFormat)` | 按尺寸和像素格式创建格式描述。 | 不分配视频像素。 |
| 构造 | `QVideoFrameFormat(const QVideoFrameFormat &format)` | 复制格式描述。 | 值语义共享；不复制帧数据。 |
| 构造 | `QVideoFrameFormat(QVideoFrameFormat &&other)` | 移动格式描述。 | 适合转移临时对象。 |
| 析构 | `~QVideoFrameFormat()` | 释放格式对象引用。 | 不负责释放视频帧像素。 |
| 赋值 | `operator=(const QVideoFrameFormat &format)` | 复制赋值。 | 共享内部描述数据。 |
| 赋值 | `operator=(QVideoFrameFormat &&other)` | 移动赋值。 | 目标原有描述被替换。 |
| 工具 | `void swap(QVideoFrameFormat &other)` | 交换两个格式对象。 | `noexcept`；不复制像素。 |
| 分离 | `void detach()` | 分离共享的格式数据。 | 只影响格式描述，不复制视频缓冲。 |
| 比较 | `operator==` / `operator!=` | 比较格式描述是否相同。 | 不是比较视频像素内容。 |
| 有效性 | `bool isValid() const` | 判断像素格式和帧尺寸是否有效。 | 有效不代表后端一定支持该格式。 |
| 查询 | `PixelFormat pixelFormat() const` | 返回像素格式。 | 解释平面数据的起点。 |
| 尺寸 | `QSize frameSize() const` | 返回底层帧尺寸。 | 可能大于有效显示区域。 |
| 尺寸 | `void setFrameSize(const QSize &size)` | 设置帧尺寸。 | 会把 viewport 重置为整帧。 |
| 尺寸 | `void setFrameSize(int width, int height)` | 以宽高设置帧尺寸。 | 同样会重置 viewport。 |
| 尺寸 | `int frameWidth() const` | 返回帧宽度。 | 与 viewport 宽度可能不同。 |
| 尺寸 | `int frameHeight() const` | 返回帧高度。 | 与 viewport 高度可能不同。 |
| 显示区域 | `QRect viewport() const` | 返回实际显示区域。 | 默认覆盖整个 frame。 |
| 显示区域 | `void setViewport(const QRect &viewport)` | 设置实际显示区域。 | 应与底层尺寸和对齐区域匹配。 |
| 平面 | `int planeCount() const` | 返回格式需要的平面数。 | RGB 通常 1，YUV 通常 1 到 3。 |
| 扫描 | `Direction scanLineDirection() const` | 查询扫描线方向。 | 不等于旋转或镜像。 |
| 扫描 | `void setScanLineDirection(Direction direction)` | 设置扫描线方向。 | 不自动重排像素内存。 |
| 帧率 | `qreal streamFrameRate() const` | 返回流帧率，帧/秒。 | 描述元数据，不等于每帧真实时间。 |
| 帧率 | `void setStreamFrameRate(qreal rate)` | 设置流帧率。 | Qt 6.8 起替代旧 frameRate API。 |
| 弃用帧率 | `frameRate()` / `setFrameRate()` | 旧帧率 API。 | Qt 6.8 起弃用。 |
| 色彩 | `ColorSpace colorSpace() const` | 返回颜色空间。 | 不包含 transfer 和 range 全部信息。 |
| 色彩 | `void setColorSpace(ColorSpace colorSpace)` | 设置颜色空间。 | 未知时保留 Undefined。 |
| 色彩 | `ColorTransfer colorTransfer() const` | 返回传递函数。 | HDR 处理需结合其它色彩信息。 |
| 色彩 | `void setColorTransfer(ColorTransfer colorTransfer)` | 设置传递函数。 | 不等于调整显示亮度。 |
| 色彩 | `ColorRange colorRange() const` | 返回 full/video/unknown 范围。 | limited range 不能误当 full range。 |
| 色彩 | `void setColorRange(ColorRange range)` | 设置色彩范围。 | 应与来源视频编码元数据一致。 |
| 旋转 | `QtVideo::Rotation rotation() const` | 查询顺时针旋转。 | 旋转先于镜像；只影响呈现。 |
| 旋转 | `void setRotation(QtVideo::Rotation rotation)` | 设置表面旋转。 | 不改写底层像素。 |
| 镜像 | `bool isMirrored() const` | 查询是否围绕垂直轴镜像。 | 语义不同于部分 `QImage` 镜像调用。 |
| 镜像 | `void setMirrored(bool mirrored)` | 设置表面镜像。 | 镜像在旋转后应用。 |
| RHI | `QString vertexShaderFileName() const` | 返回顶点 shader 文件名。 | 面向底层渲染管线，不是普通业务 API。 |
| RHI | `QString fragmentShaderFileName() const` | 返回片段 shader 文件名。 | 依赖后端 shader 契约。 |
| RHI | `void updateUniformData(QByteArray *, const QVideoFrame &, const QMatrix4x4 &, float)` | 写入视频渲染所需 uniform 数据。 | 目标指针和 RHI/渲染契约必须有效。 |
| HDR | `float maxLuminance() const` | 返回最大亮度描述。 | 服务于 HDR/显示映射，不是普通亮度控制。 |
| HDR | `void setMaxLuminance(float lum)` | 设置最大亮度描述。 | 需结合显示管线和 tone mapping 理解。 |
| 转换 | `static PixelFormat pixelFormatFromImageFormat(QImage::Format)` | 将 `QImage::Format` 映射到视频像素格式。 | 无对应格式返回 `Format_Invalid`。 |
| 转换 | `static QImage::Format imageFormatFromPixelFormat(PixelFormat)` | 将视频像素格式映射到图像格式。 | 无对应格式返回 `QImage::Format_Invalid`；YUV 通常无对应项。 |
| 调试 | `static QString pixelFormatToString(PixelFormat)` | 返回像素格式字符串。 | 适合日志和显示，不适合反向解析。 |
| 弃用色彩 | `YCbCrColorSpace` / `yCbCrColorSpace()` / `setYCbCrColorSpace()` | 旧 Y'CbCr 颜色空间 API。 | Qt 6.4 起弃用，改用 `ColorSpace`、`ColorTransfer`、`ColorRange`。 |

## 一句话总结

`QVideoFrameFormat` 是视频帧的“布局和呈现契约”：尺寸、viewport、平面数、扫描方向、色彩三元信息以及旋转镜像都在这里描述；写处理代码时要把像素格式与色彩语义分开，并始终按实际平面和跨度解释数据。
