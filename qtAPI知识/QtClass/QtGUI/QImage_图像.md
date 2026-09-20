# QImage：可直接访问像素的图像数据容器

> Qt 版本：6.11.1  
> 模块：`Qt6::Gui`  
> 头文件：`#include <QImage>`  
> 继承：`QPaintDevice`

## 它解决什么问题

`QImage` 管理一块有明确像素格式、行跨度和元数据的图像内存。它面向文件 I/O、解码后的像素处理、格式转换和离屏绘制；调用者可以逐像素访问，也可以一次取得整行连续内存。

它与 `QPixmap` 的分工很重要：

- `QImage` 以 CPU 可访问的图像数据为中心，适合解码、算法、序列化和工作线程处理。
- `QPixmap` 以屏幕显示和平台图形资源为中心，适合 GUI 线程中的显示。

`QImage` 是 `QPaintDevice`，因此可让 `QPainter` 直接画到它上面；这项离屏绘制可以在非 GUI 线程进行。类中所有函数都是可重入的，但这不等于同一个实例可被多个线程同时读写。共享实例仍要由调用方同步，通常做法是在线程间传递副本，并只让一个线程修改某个副本。

## 实际使用场景

- 在工作线程读取照片、缩放、加水印或逐像素处理，再把结果交给 GUI 线程显示。
- 从相机、网络帧或第三方库拿到原始缓冲区，以零拷贝方式暂时包装为图像。
- 生成 PNG、JPEG、WebP 等格式，写入文件、`QBuffer` 或网络响应。
- 用 `QPainter` 生成缩略图、验证码、导出图或报表中的位图。
- 处理 RGBA、灰度、索引色、浮点 HDR 和 CMYK 图像，显式控制格式和色彩空间。
- 在高 DPI 资源中保存像素尺寸，同时指定正确的设备像素比。

## 从文件到可处理像素

读取失败必须检查返回值或 `isNull()`；文件名后缀只是提示，实际可读格式还取决于已部署的图像格式插件。

```cpp
QImage image;
if (!image.load("input.png")) {
    return;
}

QImage working = image.convertToFormat(QImage::Format_ARGB32_Premultiplied);
working.invertPixels();
working.save("output.png");
```

新建图像的像素**未初始化**。它不是透明黑或白底，分配后应先 `fill()`，再交给绘制或读取代码。

```cpp
QImage canvas(QSize(1200, 630), QImage::Format_ARGB32_Premultiplied);
if (canvas.isNull()) {
    return; // 例如内存分配失败
}

canvas.fill(Qt::transparent);
QPainter painter(&canvas);
painter.setPen(Qt::white);
painter.drawText(canvas.rect(), Qt::AlignCenter, "Qt");
```

`Format_ARGB32_Premultiplied` 是带透明度的常用绘制格式：预乘 alpha 能减少合成成本。它要求每个 RGB 分量不大于 alpha；把普通 RGBA 原始字节误标为预乘格式会出现边缘发黑、颜色错误等未定义结果。

## 格式不是只看“有无 alpha”

`Format` 同时表达位深、通道顺序、是否预乘、是否索引色和数据解释方式。常见选择如下：

| 目的 | 常用格式 | 注意点 |
| --- | --- | --- |
| 不透明 32 位绘制或通用 RGB | `Format_RGB32` | 内存值按 `0xffRRGGBB` 解释。 |
| 带透明度的绘制和合成 | `Format_ARGB32_Premultiplied` | 推荐的通用 alpha 绘制格式；数据必须已预乘。 |
| 直接对接按字节排列的 RGBA 缓冲 | `Format_RGBA8888` | 是 byte-ordered 格式；不能把它在所有端序上都当作一个 `QRgb *`。 |
| 灰度算法 | `Format_Grayscale8` / `Format_Grayscale16` | 先确认算法需要 8 位还是 16 位精度。 |
| 调色板图 | `Format_Indexed8` | 像素是颜色表索引，创建后必须设置足够的 color table。 |
| 单色 mask | `Format_Mono` / `Format_MonoLSB` | 两者的位打包顺序不同。 |
| 高精度线性工作流 | `Format_RGBA16FPx4` 等 | 需让后续绘制、编码器和颜色管理链确实支持。 |
| 印刷输入 | `Format_CMYK8888` | 不能作为 `QPainter` 的绘制目标。 |

不要对 `Format_Indexed8` 或 `Format_CMYK8888` 建立 `QPainter`。Qt 对绘制最优化的是 `Format_RGB32` 和 `Format_ARGB32_Premultiplied`，其次才是 `RGB16`、`RGBX8888`、`RGBA8888_Premultiplied`、64 位 RGB/RGBA 等格式。若来源格式不适合绘制，先 `convertToFormat()`。

## 隐式共享、分离与原始指针

`QImage` 是隐式共享值类型。复制构造、复制赋值和按值传参通常只增加共享引用，不立即复制像素；任一副本发生可写操作时，Qt 可能复制数据并使其分离。

```cpp
QImage source("photo.jpg");
QImage preview = source;                 // 通常只共享数据
preview.setPixelColor(0, 0, Qt::red);    // preview 需要写入，可能深拷贝
```

这影响低层 API：

- `constBits()`、常量 `bits()` 和常量 `scanLine()` 只读访问，不触发可写分离。
- 非 const `bits()` 与非 const `scanLine()` 要返回可写指针，必要时会分离。
- `detach()` 可主动分离，`isDetached()` 查询是否独占；一般业务代码不应为了“保险”而频繁调用它。
- `cacheKey()` 是当前内容的缓存身份；像素或相关数据变更后 key 会变，不能存为跨进程、跨版本的永久 ID。

小面积检查可用 `pixel()` 或 `pixelColor()`，但在百万像素循环中它们有坐标和格式转换开销。批处理应按 `scanLine(y)`、`bytesPerLine()` 与实际 `format()` 遍历；只有在调用方已明确约束格式时才将行指针转换为对应像素类型。

## 借用外部缓冲区时，生命周期比指针更重要

带 `uchar *data` 或 `const uchar *data` 的构造函数不复制缓冲区。`data` 必须从图像创建开始，一直有效到该图像及所有仍未分离的副本全部销毁为止。默认情况下 `QImage` 不会释放这块内存。

不提供 `bytesPerLine` 的重载要求缓冲起始地址和每条扫描线均为 32 位对齐；有 stride 的重载由 `bytesPerLine` 明确每行字节数，更适合相机帧和第三方库的 padded row。

```cpp
auto *pixels = acquireFrame(); // 假设其寿命由 frameOwner 管理
const int stride = frameStride();

QImage view(pixels, 1920, 1080, stride, QImage::Format_RGBA8888);
consumeSynchronously(view);    // frameOwner 在此之前不能销毁或复用 pixels
```

若缓冲归 `QImage` 的最后一个共享副本负责回收，可传入 `QImageCleanupFunction` 和 `cleanupInfo`；回调只在最后一个尚引用该外部数据的副本销毁时执行。它不适合捕获局部对象的 lambda，也不能掩盖调用方过早复用缓冲区的问题。

以 `const uchar *` 创建的图像承诺不修改原缓冲。若对它调用可写 `bits()`，Qt 会先深拷贝，再返回新内存；这非常适合把只读解码缓存安全地包装成 `QImage`。

## 色彩空间、像素转换与元数据

`setColorSpace()` 仅修改“这些数值属于哪个色彩空间”的标签，不改变任何像素。把 sRGB 数据标成 Display P3 并不是转换，会导致之后显示颜色错误。

真正转换像素用 `convertToColorSpace()` 或 `convertedToColorSpace()`；如果源图没有有效色彩空间，前者什么也不做，后者返回空图像。需要指定目标格式时使用 Qt 6.8 引入的带 `Format` 重载。`QColorTransform` 的 `colorTransformed()` / `applyColorTransform()` 适合已准备好的变换；来源或目标与图像格式不兼容时，返回式 API 可得到空图像。

```cpp
QImage displayReady = decoded.convertedToColorSpace(
    QColorSpace::SRgb,
    QImage::Format_ARGB32_Premultiplied);

if (displayReady.isNull()) {
    // decoded 缺少有效色彩空间，或转换不能完成
}
```

`setDotsPerMeterX/Y()`、`setOffset()`、`setText()` 和 `setDevicePixelRatio()` 是元数据接口。它们不会重采样存储像素。特别是 `setDevicePixelRatio(2.0)` 会使 200x200 像素图在以设备无关单位绘制和布局时表现为 100x100，而不是把图像缩小为 100x100 个物理像素。

## 变换、掩码与格式重解释

- `scaled()`、`scaledToWidth()`、`scaledToHeight()` 和 `transformed()` 返回新图像；`FastTransformation` 较快，`SmoothTransformation` 质量更高但耗时更多。
- `trueMatrix()` 返回已修正平移量的矩阵，适合预先计算旋转、错切后包围盒的实际变换。
- `flipped()` 返回翻转副本，`flip()` 原地翻转；默认是垂直方向。旧的 `mirrored()` 和 `mirror()` 自 Qt 6.13 起弃用。
- `rgbSwapped()` 返回副本，`rgbSwap()` 原地交换红蓝通道；不能把它当成任意颜色空间转换。
- `invertPixels(InvertRgb)` 默认保留 alpha，`InvertRgba` 连 alpha 一并反相。
- `createAlphaMask()` 根据 alpha 建 1 bpp mask；`Format_RGB32` 没有 alpha，会得到空图像。`createHeuristicMask()` 不看 alpha，而是从边缘角落颜色推断背景。

`reinterpretAsFormat()` 只改格式标签，不改变数据，且仅在原格式和目标格式位深相同才成功。它不校验字节是否真的符合新格式，错误使用后再读取或绘制属于未定义行为。它只适用于调用方已经证明数据解释可变的情况，例如已知所有 alpha 都为 255 时把 ARGB 数据标成对应的不透明格式；一般格式迁移应使用 `convertToFormat()`。

## 常见错误

- 新建 `QImage` 后未 `fill()`，就把未初始化内存显示或保存。
- 在工作线程处理 `QPixmap`，而不是处理 `QImage` 并把结果送回 GUI 线程。
- 误以为“可重入”允许多个线程同时写同一个 `QImage`。
- 给 `Format_Indexed8` 设置像素却没有先建立足够大的颜色表。
- 把 `RGBA8888` 的原始字节当作平台相关的 `QRgb` 整数数组。
- 把普通 alpha 数据标为 `ARGB32_Premultiplied`，造成透明边缘色彩异常。
- 外部帧缓冲已经复用或释放，`QImage` 或其浅拷贝仍在访问它。
- 用 `setColorSpace()` 代替实际颜色转换。
- 以为 `setDevicePixelRatio()` 会改变像素缓冲的宽高或重新采样。
- 用 `reinterpretAsFormat()` 逃避真正的格式转换。
- 对每个像素调用 `pixelColor()` / `setPixelColor()`，导致不必要的格式转换和性能损耗。
- 只检查 `isNull()`，却不检查 `load()`、`save()` 的布尔返回值。

## API 速查表

| 类别 | API | 语义与边界 |
| --- | --- | --- |
| 类型 | `Format` | 图像存储格式。按位深、通道顺序、alpha、预乘、索引色和浮点格式选择；`Format_Invalid` 表示无效，`NImageFormats` 是内部计数哨兵。 |
| 类型 | `InvertMode` | `InvertRgb` 只反相 RGB，`InvertRgba` 连 alpha 反相。 |
| 类型 | `QImageCleanupFunction` | `void (*)(void *)`；外部缓冲最后一个共享引用释放时调用。回调必须处理 `cleanupInfo` 的真实所有权。 |
| 构造 | `QImage()` | 构造空图像。 |
| 构造 | `QImage(QSize, Format)` / `QImage(int, int, Format)` | 分配指定格式的新图像；分配失败为空，像素未初始化。 |
| 构造 | `QImage(uchar *data, w, h, format, cleanup, info)` | 借用可写、32 位对齐的外部缓冲；图像及未分离副本存活期间缓冲必须有效。 |
| 构造 | `QImage(const uchar *data, w, h, format, cleanup, info)` | 借用只读、32 位对齐外部缓冲；可写访问会深拷贝，原数据不会被修改。 |
| 构造 | 四个带 `bytesPerLine` 的 data 重载 | `bytesPerLine` 是每条扫描线的 stride，可处理非紧凑行；仍要保证缓冲生命周期。 |
| 构造 | `explicit QImage(const char *const xpm[])` | 从 XPM 数组构造；受 XPM 图像格式支持开关影响。 |
| 构造 | `explicit QImage(const QString &fileName, const char *format)` | 从文件立即尝试读取；失败后为 null。`format` 是格式提示，不是文件名编码。 |
| 值语义 | 复制构造、复制赋值 | 隐式共享复制；写入时可能分离。 |
| 值语义 | 移动构造、移动赋值、`swap()` | 转移或交换内部数据；移动后源对象只保证可析构和可重新赋值。 |
| 生命周期 | `~QImage()` | 释放最后一个共享数据；若仍指向外部缓冲，会按约定调用 cleanup 回调。 |
| 状态 | `isNull()` | 是否没有可用图像数据；不能单独替代 I/O 操作的返回值检查。 |
| 比较 | `operator==` / `operator!=` | 按图像内容比较；大图比较可能昂贵，不应用作高频缓存查找。 |
| QVariant | `operator QVariant()` | 将图像包装为 `QVariant`，用于元对象和通用数据通道。 |
| 共享 | `detach()` / `isDetached()` | 强制独占或查询是否独占；通常由写操作自动处理。 |
| 复制 | `copy()` / `copy(x, y, w, h)` | 返回完整或区域副本；区域超出范围会裁剪，空/无交集结果需检查。 |
| 格式 | `format()` / `pixelFormat()` | 返回 Qt 图像格式或通用 `QPixelFormat` 描述。 |
| 格式 | `convertToFormat()` / `convertedTo()` | 返回指定格式的转换副本；带 color table 重载可为索引色结果提供调色板。 |
| 格式 | `convertTo()` | 原地转换格式；可能分配、分离并改变现有图像。 |
| 格式 | `reinterpretAsFormat()` | 只换标签且要求同位深；不验证数据，只有数据解释确定兼容时才能用。 |
| 格式 | `static toPixelFormat()` / `toImageFormat()` | 在 `Format` 与 `QPixelFormat` 间映射；无对应项时得到无效表示。 |
| 尺寸 | `width()` / `height()` / `size()` / `rect()` | 返回存储像素几何信息；不是 DPR 修正后的逻辑布局尺寸。 |
| 尺寸 | `devicePixelRatio()` / `setDevicePixelRatio()` / `deviceIndependentSize()` | 查询/设置像素与设备无关单位比例；设置只改绘制与布局解释，不改实际像素。 |
| 存储 | `depth()` / `bitPlaneCount()` | 返回每像素总位深及真正使用的位平面数。 |
| 存储 | `bytesPerLine()` / `sizeInBytes()` | 返回行跨度和总存储字节数；遍历缓冲要使用 stride，不能假设 `width * bytesPerPixel`。 |
| 缓冲 | `bits()` | 非 const 版本给出可写首地址并可能分离；const 版本只读。 |
| 缓冲 | `constBits()` | 明确获得只读首地址，不触发可写分离。 |
| 缓冲 | `scanLine()` / `constScanLine()` | 取得第 `y` 行首地址；非 const 版本可能分离，调用方须确保 `y` 有效。 |
| 坐标 | `valid(x, y)` / `valid(QPoint)` | 查询坐标是否在图像内；低层循环应先保证范围而不是依赖无效访问。 |
| 像素 | `pixelIndex()` | 返回索引色图像的颜色表索引；不适合当通用 RGBA 读取 API。 |
| 像素 | `pixel()` / `pixelColor()` | 按坐标读取 `QRgb` 或 `QColor`；方便但不适合大批量算法。 |
| 像素 | `setPixel()` / `setPixelColor()` | 按坐标写像素；参数对索引格式和直接色格式的含义不同。 |
| 调色板 | `color()` / `colorCount()` / `colorTable()` | 查询索引色的颜色表。 |
| 调色板 | `setColor()` / `setColorCount()` / `setColorTable()` | 修改索引颜色表；创建 `Indexed8` 后，应先准备足以覆盖全部索引的表。 |
| 灰度 | `allGray()` / `isGrayscale()` | 前者检查颜色是否均为灰度值，后者也会考察图像格式是否是灰度语义。 |
| 填充 | `fill(uint)` / `fill(QColor)` / `fill(Qt::GlobalColor)` | 以格式可表达的像素填满图像；新建画布、复用缓冲前的必要初始化方式。 |
| Alpha | `hasAlphaChannel()` | 查询格式是否携带 alpha 通道。 |
| Alpha | `setAlphaChannel()` | 以 8 位 alpha 或灰度强度叠乘现有 alpha；可能将图像转换为带 alpha 格式。 |
| Mask | `createAlphaMask()` | 从 alpha 生成 1 bpp `Format_MonoLSB` mask；无 alpha 的 `RGB32` 得到空图。 |
| Mask | `createHeuristicMask()` | 从边缘颜色推断背景的 1 bpp mask；忽略 alpha。 |
| Mask | `createMaskFromColor()` | 用指定颜色按 `Qt::MaskMode` 生成 1 bpp mask。 |
| 缩放 | `scaled()` | 返回目标尺寸图；`AspectRatioMode` 控制比例，`TransformationMode` 在质量与速度间权衡。 |
| 缩放 | `scaledToWidth()` / `scaledToHeight()` | 保持纵横比缩放到指定单边；非法或零尺寸结果需检查。 |
| 几何 | `transformed()` | 用 `QTransform` 返回变换后的图像，结果尺寸可变。 |
| 几何 | `static trueMatrix()` | 计算包含必要平移的实际矩阵，用于预测变换后的边界。 |
| 翻转 | `flipped(Qt::Orientations)` / `flip(Qt::Orientations)` | Qt 6.9 起分别返回副本或原地翻转，默认垂直。 |
| 弃用翻转 | `mirrored()` / `mirror()` | Qt 6.13 起弃用；迁移到 `flipped()` / `flip()`。 |
| 通道 | `rgbSwapped()` / `rgbSwap()` | 分别返回副本或原地交换 R/B 通道；不是 ICC 色彩转换。 |
| 反相 | `invertPixels(InvertMode)` | 原地反相 RGB，按模式决定是否也处理 alpha。 |
| 色彩空间 | `colorSpace()` / `setColorSpace()` | 查询/标注色彩空间；`set` 不改像素数据。 |
| 色彩空间 | `convertedToColorSpace()` | 返回已转换的副本；源色彩空间无效时返回 null。 |
| 色彩空间 | `convertToColorSpace()` | 原地转换；源色彩空间无效时不做任何事。Qt 6.8 重载可指定目标格式与 flags。 |
| 颜色变换 | `colorTransformed()` | Qt 6.4 起返回应用 `QColorTransform` 的副本；不兼容格式或变换时可能返回 null。 |
| 颜色变换 | `applyColorTransform()` | 原地应用变换；Qt 6.8 重载可同时选择结果格式。 |
| 读取 | `load(fileName, format)` | 将文件读取到当前对象，成功返回 `true`；失败后不能使用旧内容作成功结果假设。 |
| 读取 | `load(QIODevice *, format)` | 从已正确打开的设备读取；设备生命周期和读位置由调用方控制。 |
| 读取 | `loadFromData(QByteArrayView)` 及其重载 | 从编码字节解码并改写当前对象；输入是压缩/编码文件数据，不是像素缓冲包装。 |
| 读取 | `static fromData(QByteArrayView)` 及其重载 | 从编码字节解码并返回新对象；失败返回 null。 |
| 写入 | `save(fileName, format, quality)` | 编码并写文件；返回值必须检查。`quality=-1` 交给格式默认策略。 |
| 写入 | `save(QIODevice *, format, quality)` | 向已打开可写设备编码；格式名通常应显式给出。 |
| 缓存 | `cacheKey()` | 当前图像内容的进程内缓存身份；修改后变化，不是持久化主键。 |
| 元数据 | `dotsPerMeterX/Y()` / `setDotsPerMeterX/Y()` | 查询/设置物理分辨率提示；不会缩放像素数据。 |
| 元数据 | `offset()` / `setOffset()` | 查询/设置图像相对位置元数据。 |
| 元数据 | `textKeys()` / `text()` / `setText()` | 管理图像文本键值；编码器是否保存取决于目标格式。 |
| 绘制底层 | `devType()` / `paintEngine()` | `QPaintDevice` 的实现接口；普通绘制只需创建 `QPainter(&image)`，不应直接依赖绘制引擎。 |
| 平台 | `toCGImage()` | macOS 平台 API；转换失败可返回空 `CGImageRef`，无色彩空间时按 sRGB 处理。 |
| 平台 | `toHBITMAP()` / `toHICON()` | Windows 平台 API；返回的 GDI 句柄由调用方按 Windows 规则释放。 |
| 平台 | `fromHBITMAP()` / `fromHICON()` | Windows 平台 API；`HBITMAP` 通常不保留 alpha 信息，必要时由调用方确认格式和 alpha 语义。 |
| 流 | `operator<<(QDataStream &, const QImage &)` | 写入 Qt 数据流；跨版本持久化应固定 `QDataStream` 版本，并考虑体积。 |
| 流 | `operator>>(QDataStream &, QImage &)` | 从 Qt 数据流读取图像；读取不可信数据时需限制输入大小。 |
| 调试 | `operator<<(QDebug, const QImage &)` | 输出调试描述，不是稳定的序列化格式。 |

## 相关类

- `QPixmap`：用于 GUI 线程中的屏幕显示和平台 pixmap。
- `QPainter`：在 `QImage` 上离屏绘制。
- `QImageReader` / `QImageWriter`：需要逐帧、格式选项、错误字符串或增量读取时使用。
- `QColorSpace` / `QColorTransform`：处理 ICC 色彩空间及明确色彩变换。
- `QPixelFormat`：描述底层通道、字节序和数值解释。

`QImage` 的核心不是“装一张图片”，而是让像素数据的格式、所有权、可写性和色彩解释都可被明确控制。把这些边界说清楚后，它既能是稳健的图像 I/O 容器，也能是高效的离屏处理工作台。
