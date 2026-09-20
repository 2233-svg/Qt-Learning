# QImageReader：可控、安全的格式无关图像读取器

> Qt 版本：6.11.1  
> 模块：`Qt6::Gui`  
> 头文件：`#include <QImageReader>`

## 它解决什么问题

`QImageReader` 从文件或 `QIODevice` 解码图像，并在读取前提供格式探测、尺寸查询、解码期裁剪、解码期缩放、方向元数据、动画帧和错误诊断。

只需“加载一张本地图”的场景，`QImage::load()` 足够；需要降低大图内存峰值、读动图、得到清晰错误信息、控制格式识别或处理不可信数据时，应使用 `QImageReader`。

它是可重入类，但一个 reader 假定对其 file/device 有**独占控制**。在 reader 的生命周期内，其他代码修改同一个文件或设备的位置、内容、打开状态，结果未定义。不要用同一个 `QBuffer` 或 socket 同时交给两套读取逻辑。

## 实际使用场景

- 图片浏览器在读取超大照片时先查询 `size()`，然后只解码需要显示的缩略图。
- 地图、相册或医学影像程序只读取巨大源图中的 ROI。
- 文件选择器按 `supportedMimeTypes()` 构造可用格式过滤器。
- 网络或用户上传图片在解码前使用 `allocationLimit()` 防御畸形尺寸声明。
- 读取 JPEG 的 EXIF 方向，并选择让 `read()` 自动旋转，或由应用自己处理。
- 逐帧读取 GIF、WebP 等动画图像，获取帧延迟、循环次数和局部更新矩形。
- 对文件后缀不可信的输入强制按内容识别真实格式。

## 常用读取链

设置裁剪、缩放、背景色和方向策略应发生在第一次 `read()` 前。

```cpp
QImageReader reader("photos/large-photo.jpg");
reader.setAutoTransform(true);
reader.setScaledSize(QSize(1600, 0)); // 只给一边时保持纵横比

if (!reader.canRead()) {
    qWarning() << reader.errorString();
    return;
}

const QImage image = reader.read();
if (image.isNull()) {
    qWarning() << reader.error() << reader.errorString();
    return;
}
```

`canRead()` 只是轻量的头部检查。它返回 `true` 后，`read()` 仍可能因截断流、损坏压缩数据、内存分配失败等原因失败；最终成功判断仍是 `read()` 的结果。

想复用已有图像内存时，使用输出参数重载。若 `image` 的尺寸和格式恰好匹配即将解码的数据，Qt 可能避免一次新的图像分配。

```cpp
QImage reusable(256, 256, QImage::Format_ARGB32);
QImageReader reader("frame.bmp");

if (!reader.read(&reusable)) {
    qWarning() << reader.errorString();
}
```

## 文件、设备与格式判定

构造或 `setFileName()` 后，reader 内部创建 `QFile` 并以只读方式打开；如果文件名不带扩展名，Qt 会依次尝试受支持的扩展名。构造或 `setDevice()` 后，若设备尚未打开，reader 会尝试以 `ReadOnly` 打开它；某些设备如 `QProcess`、`QTcpSocket`、`QUdpSocket` 还需要调用方自行完成连接或打开逻辑。

`setFormat("png")` 指定希望使用的格式，格式字符串不区分大小写。默认启用的自动探测会综合可选 format、文件后缀和设备内容选择 handler：

1. 先按显式 format 或文件后缀询问插件。
2. 再按同一信息检查 Qt 内建 handler。
3. 若未找到，遍历插件并基于内容探测。
4. 最后遍历内建 handler 并基于内容探测。

关闭 `setAutoDetectImageFormat(false)` 后，只按显式 format 查找，不再尝试文件后缀。`setDecideFormatFromContent(true)` 更严格：忽略 format 与后缀，只看设备内容；它会加载所有图像插件并同时关闭自动格式探测。该模式适合不信任扩展名的输入，但启动和探测成本更高。

静态 `imageFormat(fileName)` 和 `imageFormat(device)` 只用于探测编码格式名称，如 `"jpeg"`；实例 `imageFormat()` 返回的是解码后图像的 `QImage::Format`。两者同名但问题不同。

## 解码期裁剪、缩放与质量

如果底层格式 handler 支持，`QImageReader` 可以让解码器直接少读像素，而不是先解整图再处理。操作顺序固定：

1. `setClipRect()`：相对于**未变换原图** `size()` 的 ROI。
2. `setScaledSize()`：对裁剪结果缩放。
3. `setScaledClipRect()`：对缩放结果再次裁剪。

```cpp
QImageReader reader("slide.tiff");
reader.setClipRect(QRect(4000, 2000, 3000, 2000));
reader.setScaledSize(QSize(1200, 800));

QImage tile = reader.read();
```

支持与否取决于格式。先用 `supportsOption()` 查询 `Size`、`ClipRect`、`ScaledSize`、`ScaledClipRect` 等选项；不支持时，`QImageReader` 会在读完整图后尽力完成回退处理，结果正确但节省不了峰值内存。

`setScaledSize()` 只设宽或高时，会根据原始自然尺寸推导另一边以保持比例。`setQuality()` 对支持它的格式控制“视觉质量与解码/缩放速度”的权衡，数值范围由编码器决定，例如 JPEG 常见为 0 到 100；它不是所有格式都有意义的通用画质保证。

## 方向、高 DPI 与图像文本

`transformation()` 返回文件中记录的方向变换，例如 EXIF 的旋转或镜像。默认 `autoTransform()` 为关闭状态时，`read()` 返回原始像素方向；启用 `setAutoTransform(true)` 后，reader 在返回图像前应用该元数据。二者只能选择一种策略：若应用层还会按 `transformation()` 手动旋转，就不要再开启自动变换。

高分辨率资源名为 `logo@2x.png` 时，Qt 读取后会把返回 `QImage` 的 device pixel ratio 标为 2。实际存储仍是高分辨率像素，布局应使用设备无关尺寸。环境变量 `QT_HIGHDPI_DISABLE_2X_IMAGE_LOADING` 可禁用这项 `@2x` 约定。

`textKeys()` 和 `text(key)` 读取格式支持的文字元数据；调用前也应以 `supportsOption(QImageIOHandler::Description)` 判断支持情况。不要把图片 metadata 当成可信配置或命令输入。

## 动画和多帧图像

`supportsAnimation()` 只说明格式有动画能力，不保证当前文件一定有多个可读帧。每次调用 `read()` 取得下一帧，全部帧读完后得到空图；这时 `canRead()` 对动画会返回 `false`。

- `imageCount()` 查询帧数；未知或不支持时不要假设其一定大于 0。
- `currentImageNumber()` 查询当前帧；出错返回 `-1`。
- `jumpToImage(n)` 将下一次读取定位到指定帧。
- `jumpToNextImage()` 跳过当前帧；默认实现可能实际解码并丢弃一帧，所以不一定便宜。
- `nextImageDelay()` 返回播放下一帧前的毫秒数；错误时为 `-1`，非动画为 0。
- `loopCount()` 返回建议循环次数；`-1` 既可能表示无限循环，也可能表示错误，必须再检查 `canRead()` / `error()`。
- `currentImageRect()` 返回动画当前帧在逻辑画布中的更新区域，非动画得到空矩形。

需要直接播放动图时 `QMovie` 往往更合适；需要把每一帧送进自定义处理管线时再驱动 `QImageReader`。

## 分配上限与错误处理

`setAllocationLimit(int mbLimit)` 是进程级静态限制，限制单次解码所需 `QImage` 内存。超限图像会被拒绝；传入 0 会关闭检查。默认值足以覆盖常见尺寸，通常不应为了“兼容所有图片”直接设为 0。

对网络、拖放或用户上传内容，更合理的策略是保留上限，并在 `size()` 可用时同时设置业务维度上限。内存限制不能防止所有资源消耗问题，例如高度压缩的文件仍可能耗费大量 CPU。

| 错误 | 含义与排查方向 |
| --- | --- |
| `FileNotFoundError` | 文件路径不存在，或无扩展名时没有找到受支持的实际文件。 |
| `DeviceError` | 读取设备失败；检查打开模式、网络流状态和设备错误字符串。 |
| `UnsupportedFormatError` | 没有可用 handler；检查 format、插件部署和支持格式列表。 |
| `InvalidDataError` | 数据损坏、截断或不是有效的目标图像格式。 |
| `UnknownError` | 以上无法归类的失败；保留 `errorString()` 与输入样本进一步诊断。 |

## 常见错误

- `canRead()` 成功后不检查 `read()`，把损坏数据误当为正常图像。
- 在 reader 存活时从另一个地方读写同一个 `QIODevice`。
- 以为 `setScaledSize()` 总能避免整图解码；插件不支持时仍可能先读完整图。
- 混淆静态 `imageFormat()` 的编码格式名与实例 `imageFormat()` 的像素格式。
- 同时开启 `autoTransform` 又按 `transformation()` 手动旋转，导致图像旋转两次。
- 不信任扩展名却只依赖默认检测，没有使用内容判定或 MIME 检查。
- 将 `setDecideFormatFromContent()` 误认为普通“自动检测开关”；它会忽略 format/后缀并加载所有插件。
- 为未知来源图像禁用 allocation limit。
- 把 `loopCount() == -1` 一律当无限循环，而不检查是否发生错误。
- 在 `read()` 之后才设置 clip、缩放、背景色或自动方向。

## API 速查表

| 类别 | API | 语义与边界 |
| --- | --- | --- |
| 类型 | `ImageReaderError` | 错误枚举：`UnknownError`、`FileNotFoundError`、`DeviceError`、`UnsupportedFormatError`、`InvalidDataError`。 |
| 构造 | `QImageReader()` | 创建无来源的 reader，随后用 `setFileName()` 或 `setDevice()` 指定输入。 |
| 构造 | `QImageReader(QIODevice *, QByteArray format = {})` | 使用设备读取；reader 对设备有独占控制，设备应在使用期间保持有效。 |
| 构造 | `QImageReader(const QString &fileName, QByteArray format = {})` | 使用文件名读取；内部以只读方式管理文件。 |
| 析构 | `~QImageReader()` | 释放 reader 资源；不应在析构后再使用其 device/file 设置。 |
| 来源 | `setDevice(QIODevice *)` / `device()` | 设置/取得输入设备。未打开时会尝试以只读打开，但特殊设备需调用方自行准备。 |
| 来源 | `setFileName(QString)` / `fileName()` | 设置/取得文件名；无扩展名时会尝试受支持的扩展。 |
| 格式 | `setFormat(QByteArray)` / `format()` | 设置/读取请求格式，大小写不敏感；不是对数据做格式转换。 |
| 格式 | `setAutoDetectImageFormat(bool)` / `autoDetectImageFormat()` | 控制默认的 format、后缀和内容回退探测；关闭后只按显式 format 查找。 |
| 格式 | `setDecideFormatFromContent(bool)` / `decideFormatFromContent()` | 设为 true 时只按数据内容选择 handler，忽略 format/后缀并关闭自动探测。 |
| 预检 | `canRead() const` | 轻量判断设备和头部是否可能可读；成功不保证完整解码一定成功，动画帧耗尽时为 false。 |
| 解码 | `read()` | 返回下一张图/下一帧；失败或帧耗尽返回 null，随后查询 `error()` 与 `errorString()`。 |
| 解码 | `read(QImage *)` | 向调用方图像写入，成功返回 bool；同尺寸同格式时可能复用存储，适合连续读取。 |
| 几何 | `size()` | 不解码完整内容地查询原始尺寸；格式不支持时返回无效 `QSize`。 |
| 几何 | `setClipRect(QRect)` / `clipRect()` | 设置/查询原图坐标系 ROI；先于缩放应用。 |
| 几何 | `setScaledSize(QSize)` / `scaledSize()` | 设置/查询缩放目标；只给一个维度时按自然比例补全。 |
| 几何 | `setScaledClipRect(QRect)` / `scaledClipRect()` | 设置/查询缩放后 ROI；最后应用。 |
| 像素格式 | `imageFormat() const` | 查询 handler 预期输出的 `QImage::Format`；不可用时可能为无效格式。 |
| 质量 | `setQuality(int)` / `quality()` | 对支持的格式设置/查询解码或缩放质量策略；合法范围由格式决定。 |
| 背景 | `setBackgroundColor(QColor)` / `backgroundColor()` | 设置/查询读取时的背景色；只有支持此 option 的格式会使用。 |
| 文本 | `textKeys()` / `text(QString)` | 查询图片文字 metadata；是否可用依赖当前格式。 |
| 方向 | `transformation()` | 返回方向元数据而不改像素；不支持时为 `TransformationNone`。 |
| 方向 | `setAutoTransform(bool)` / `autoTransform()` | 控制 `read()` 是否自动应用方向 metadata；避免与手动旋转叠加。 |
| 子类型 | `subType()` / `supportedSubTypes()` | 查询当前编码变体和可用子类型；并非所有格式有子类型。 |
| 能力 | `supportsOption(QImageIOHandler::ImageOption)` | 查询当前 handler 是否支持某项特性，设置 option 或依赖快速路径前先调用。 |
| 动画 | `supportsAnimation()` | 当前格式是否具备动画支持。 |
| 动画 | `imageCount()` | 查询总帧数；未知或不适用时按返回值和 `error()` 谨慎处理。 |
| 动画 | `currentImageNumber()` | 返回当前帧号；发生错误时为 `-1`。 |
| 动画 | `currentImageRect()` | 当前动画帧的更新矩形；非动画为 null rect。 |
| 动画 | `jumpToImage(int)` | 将下一次 `read()` 定位到指定帧，成功返回 true。 |
| 动画 | `jumpToNextImage()` | 跳过当前帧；可能通过解码并丢弃实现。 |
| 动画 | `nextImageDelay()` | 下一帧展示延迟，单位毫秒；非动画为 0，错误为 `-1`。 |
| 动画 | `loopCount()` | 建议循环次数；`-1` 可能是无限循环或错误，应再检查状态。 |
| 错误 | `error()` | 返回最近失败的 `ImageReaderError`。 |
| 错误 | `errorString()` | 返回适合诊断/显示的错误描述；不要仅靠文本做逻辑分支。 |
| 静态探测 | `static imageFormat(QString)` | 根据文件探测编码格式名称；不等同于 `QImage::Format`。 |
| 静态探测 | `static imageFormat(QIODevice *)` | 根据设备内容探测编码格式；调用方仍需管理设备位置和生命周期。 |
| 静态列表 | `static supportedImageFormats()` | 返回当前运行时可读格式，包括已发现读取插件；需在 `QCoreApplication` 创建后调用。 |
| 静态列表 | `static supportedMimeTypes()` | 返回可读 MIME 类型；需在应用对象创建后调用。 |
| 静态列表 | `static imageFormatsForMimeType(QByteArray)` | 返回某 MIME 类型可读取的格式名列表。 |
| 静态安全 | `static allocationLimit()` | 返回当前单图解码分配上限，单位 MB。 |
| 静态安全 | `static setAllocationLimit(int mbLimit)` | 设置全局分配上限；0 禁用检查，通常不推荐用于不可信输入。 |

## 相关类

- `QImageWriter`：格式无关的写出接口。
- `QImageIOHandler`：实际格式解码器接口。
- `QImageIOPlugin`：扩展格式支持的插件工厂。
- `QImage`：默认解码结果和离屏像素处理容器。
- `QMovie`：需要直接播放动画图像时的高层类。

`QImageReader` 的价值在于把“能不能读、读哪一部分、怎样读、失败原因是什么”都前置到一次可控的读取会话里。对大图、动图和外部输入，这比一句 `load()` 多出来的边界往往正是稳定性的来源。
