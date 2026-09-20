# QImageIOHandler：图像编解码器的统一底层接口

> Qt 版本：6.11.1  
> 模块：`Qt6::Gui`  
> 头文件：`#include <QImageIOHandler>`

## 它解决什么问题

`QImageIOHandler` 是 Qt 图像格式处理器的抽象接口。`QImageReader` 和 `QImageWriter` 负责面向应用的文件、设备、格式选择和错误报告；真正认识某种编码格式、从字节流读出 `QImage`、或把 `QImage` 写成字节流的工作，由具体 handler 完成。

通常应用代码不直接创建它，而是使用 `QImageReader` / `QImageWriter`。需要支持私有图片格式、为特殊硬件数据接入 Qt 图像 I/O 管线，或实现图像格式插件时，才派生 `QImageIOHandler`。

它是可重入类，但 handler 内部关联的 `QIODevice` 位置、当前动画帧和选项状态都是可变的会话状态。一个 handler 实例应由一个执行流串行使用，不能因为“可重入”就同时在多个线程上对同一实例 `read()`。

## 实际使用场景

- 实现公司内部纹理、医学影像、卫星图块或设备专有帧格式。
- 为 Qt 不自带的格式编写 `QImageIOPlugin`，让 `QImageReader` 自动发现它。
- 利用 `Size`、`ClipRect`、`ScaledSize` 做解码时裁剪和缩放，避免先解出超大整图。
- 实现 GIF、WebP 动画或多页图像的逐帧读取和定位。
- 暴露 JPEG quality、压缩级别、渐进式写入、EXIF 方向等格式能力。
- 在不可信输入上用 `allocateImage()` 遵守 `QImageReader` 的内存分配限制。

## 使用模型：handler 是插件后端，不是文件读取捷径

一个读取 handler 至少要实现两个纯虚函数：

1. `canRead()`：判断当前设备能否读出本格式，并保持设备读位置不变。
2. `read(QImage *image)`：从设备读取当前图像或当前帧，成功时填充 `*image`。

写出能力由 `write()` 提供；基类默认返回 `false`，所以只读格式不必实现写入。

```cpp
class FooImageHandler final : public QImageIOHandler
{
public:
    bool canRead() const override
    {
        const QByteArray header = device()->peek(8);
        if (header != QByteArray("FOOIMG\0", 7)) {
            return false;
        }

        setFormat("foo"); // const 重载专为 canRead() 提供
        return true;
    }

    bool read(QImage *image) override
    {
        if (!image || !canRead()) {
            return false;
        }

        // 解析头部、验证尺寸，并调用 allocateImage() 后填充像素。
        return decodeInto(image);
    }
};
```

`canRead()` 不能通过 `read()` 消耗文件头后直接返回结果。使用 `QIODevice::peek()`，或在可寻址设备上保存并恢复位置；否则后续 `read()` 会从错误偏移开始。

## 设备与格式的边界

调用 `setDevice()` 后，handler 使用该 `QIODevice` 进行探测、读取和写入。设备必须在这些调用期间保持有效并处于相应的打开状态。一个 handler 的 device 只能设置一次，并且必须先于 `canRead()`、`read()`、`write()` 等操作设置；需要处理多个文件时创建多个 handler。

`setFormat()` 设置的是格式标识，例如 `"png"` 或 `"foo"`，主要用于同一个 handler 能处理多种近亲格式时。它并不转换设备内容，也不保证格式一定能读。其 const 重载允许 `canRead() const` 在探测成功后记录识别出的实际格式。

## 选项协商：先声明支持，再读写

`ImageOption` 既有读取信息，也有读写策略。调用链的正确模式是：

```cpp
if (handler.supportsOption(QImageIOHandler::ScaledSize)) {
    handler.setOption(QImageIOHandler::ScaledSize, QSize(640, 360));
}

QVariant nativeSize;
if (handler.supportsOption(QImageIOHandler::Size)) {
    nativeSize = handler.option(QImageIOHandler::Size);
}
```

派生类对不支持的选项应让 `supportsOption()` 返回 `false`，而不是静默假装生效。`option()` 返回的 `QVariant` 类型由选项决定，调用方和 handler 必须一致，例如 `Size` 是 `QSize`，ROI 选项是 `QRect`，质量与压缩比通常是 `int`，`BackgroundColor` 是 `QColor`。

解码优化有明确的执行顺序：

1. `ClipRect`：先在原始图中裁剪。
2. `ScaledSize`：再缩放。
3. `ScaledClipRect`：最后对缩放结果裁剪。

若 handler 不支持这些选项，`QImageReader` 可以在读完整图后代为处理，但那会消耗更多内存和 CPU。

## 多帧、动画与增量读取

动画格式中，`read()` 每次读取一个当前帧。对于增量格式和动画格式，传入的 `QImage *` 可以指向上一帧，handler 可以据此只更新变化区域或做帧合成。

- `imageCount()` 返回总帧数；未知或非动画格式可返回 0。基类在可读时默认返回 1。
- `currentImageNumber()` 在尚未读取任何帧时返回 `-1`；动画第一帧是 0；非动画格式返回 0。
- `jumpToImage(n)` 和 `jumpToNextImage()` 只移动下一次 `read()` 的目标帧，默认实现返回 `false`。
- `nextImageDelay()` 返回下一帧前应等待的毫秒数；不支持动画时为 0。
- `loopCount()` 返回建议循环次数；不支持动画时为 0。不要将 0 擅自解释为“无限循环”，应按具体格式及上层 API 约定处理。
- `currentImageRect()` 返回当前帧在画布内应更新的区域；没有局部更新区域时返回空 `QRect`。

`ImageTransformation` 表示读取到的方向元数据，例如 EXIF 镜像或旋转。handler 应报告元数据，而不是自行把像素旋转；是否自动应用由上层 `QImageReader::setAutoTransform()` 决定。

## 安全分配与不可信图像

格式头里声明的宽高不能直接拿来构造 `QImage`。恶意输入可以宣称极大的尺寸并触发内存耗尽。Qt 6 的 `allocateImage(size, format, image)` 会验证参数、检查当前 `QImageReader` 分配上限，并在成功时保证 `*image` 是已分离的指定尺寸和格式图像。

```cpp
if (!QImageIOHandler::allocateImage(size, QImage::Format_RGBA8888, image)) {
    return false;
}

for (int y = 0; y < size.height(); ++y) {
    uchar *line = image->scanLine(y);
    if (!decodeRow(line, image->bytesPerLine())) {
        return false;
    }
}
```

`allocateImage()` 只负责安全分配，不验证你的像素数据、行长度、压缩流完整性或颜色解释。解析器仍须检查整数溢出、每行输入量、帧边界和 `QIODevice` 的实际返回值。

## ImageOption 语义

| 选项 | 读取或写入时的含义 |
| --- | --- |
| `Size` | 读取原始图像尺寸，`option()` 返回 `QSize`。 |
| `ClipRect` | 原图 ROI；应在缩放前应用。 |
| `ScaledSize` | 目标解码尺寸，`ClipRect` 之后应用。 |
| `ScaledClipRect` | 缩放后的 ROI；最后应用。 |
| `Description` | 图像文字。键值文本采用 `Key: Value`、条目之间空行的约定；单块文本可使用 `Description` 作为键。 |
| `CompressionRatio` | 写入压缩比例，通常为 `int`；实际范围由编码器决定。 |
| `Gamma` | 写入 gamma，通常为浮点数；不是通用 ICC 色彩空间替代品。 |
| `Quality` | 写入质量，通常为 `int`；不同编码器的范围和效果不同。 |
| `Name` | 读取或写入图像名称元数据，通常为 `QString`。 |
| `SubType` | 同一族格式的子类型，例如 PPM 的变体，通常为 `QByteArray`。 |
| `IncrementalReading` | 声明可分多次读取，`QImageReader` 会按动画式方式处理。 |
| `Endianness` | 请求特定大端或小端存储；仅对格式确有此概念时支持。 |
| `Animation` | `supportsOption()` 是否为 `true` 表示格式支持动画。 |
| `BackgroundColor` | 读取时的背景色，值为 `QColor`。 |
| `ImageFormat` | handler 返回图像所使用的 `QImage::Format`。 |
| `SupportedSubTypes` | 写入时可用的子类型列表，值为 `QList<QByteArray>`。 |
| `OptimizedWrite` | 请求编码器启用面向体积或编码的优化策略。 |
| `ProgressiveScanWrite` | 请求写成渐进扫描图像；并非每种格式都有对应能力。 |
| `ImageTransformation` | 读取方向元数据，值为 `Transformations`；handler 不应自行应用它。 |

## 常见错误

- 在 `canRead()` 中调用会推进设备位置的 `read()`，导致真正解码从错误位置开始。
- 未先调用 `supportsOption()` 就假设 `setOption()` 一定有效。
- 将上层希望的 ROI/缩放当作必须由 handler 完成的约束；不支持时要让 `QImageReader` 回退。
- 无视 `QImageReader` 分配限制，按攻击者提供的尺寸直接分配图像。
- 把动画帧当成独立完整画布，忽略上一帧和 `currentImageRect()` 的增量语义。
- 读取 EXIF 方向后既由 handler 旋转，又让 `QImageReader` 自动旋转一次。
- 使用一个 handler 不断 `setDevice()` 切换文件；该 setter 只能使用一次。
- 忘记为只读 handler 明确接受 `write()` 的默认 `false`，却在插件能力声明中声称可写。
- 将 `setFormat()` 当作强制解码格式转换；它只是 handler 的格式选择/识别状态。

## API 速查表

| 类别 | API | 语义与边界 |
| --- | --- | --- |
| 类型 | `ImageOption` | 图像元数据、解码策略和编码选项枚举；每项是否可用必须由 `supportsOption()` 声明。 |
| 类型 | `Transformation` | 方向元数据原子标志：无变换、水平镜像、垂直镜像、90 度旋转及其组合。 |
| 类型 | `Transformations` | `QFlags<Transformation>`；可 OR 组合，用于 EXIF 等方向信息。 |
| 构造 | `QImageIOHandler()` | 创建无设备、无格式的 handler。通常仅在派生类构造时使用。 |
| 析构 | `virtual ~QImageIOHandler()` | 虚析构，允许经基类指针删除派生 handler。 |
| 设备 | `setDevice(QIODevice *)` | 设置 I/O 设备；只能调用一次，且必须早于读写调用。设备需在 handler 使用期间保持有效和打开。 |
| 设备 | `device() const` | 返回当前设备，未设置时为 `nullptr`。 |
| 格式 | `setFormat(const QByteArray &)` | 设置格式标识，适合多格式 handler；不验证或转换输入数据。 |
| 格式 | `setFormat(const QByteArray &) const` | 同上，但可在 `canRead() const` 中记录探测到的格式。 |
| 格式 | `format() const` | 返回已设置/识别出的格式；未设置时为空 `QByteArray`。 |
| 读取 | `virtual canRead() const = 0` | 必须实现。判断设备、格式和初始头是否支持；不得改变设备当前位置。 |
| 读取 | `virtual read(QImage *) = 0` | 必须实现。读取当前图或帧并写入输出参数，成功返回 `true`。动画/增量读取时输出可能承载上一帧。 |
| 写入 | `virtual write(const QImage &)` | 将图像编码到设备；基类默认返回 `false`，可写格式需要重写。 |
| 选项 | `option(ImageOption) const` | 返回当前选项的 `QVariant`；返回类型由具体选项约定。 |
| 选项 | `setOption(ImageOption, const QVariant &)` | 设置解码或编码选项；派生类应只接受它实际支持且类型正确的值。 |
| 选项 | `supportsOption(ImageOption) const` | 明确声明选项能力；调用方先查询再设置/读取。 |
| 动画 | `jumpToNextImage()` | 将下一次 `read()` 定位到下一帧；基类默认返回 `false`。 |
| 动画 | `jumpToImage(int)` | 将下一次 `read()` 定位到指定帧；基类默认返回 `false`。 |
| 动画 | `imageCount() const` | 返回总帧数；未知或非动画可为 0，基类可读时默认 1。 |
| 动画 | `currentImageNumber() const` | 当前帧序号；读前为 `-1`，非动画为 0。 |
| 动画 | `currentImageRect() const` | 当前帧的更新矩形；无局部区域时为空矩形。 |
| 动画 | `nextImageDelay() const` | 下一帧建议延迟，单位毫秒；非动画为 0。 |
| 动画 | `loopCount() const` | 建议循环次数；非动画为 0，具体 0 的播放解释交给格式和上层。 |
| 安全 | `static allocateImage(QSize, QImage::Format, QImage *)` | Qt 6 起。检查尺寸和分配上限后构造已分离图像；读取不可信输入时优先使用。 |
| 派生 | 受保护构造 `QImageIOHandler(QImageIOHandlerPrivate &)` | 供 Qt 内部私有实现使用；普通插件派生类使用默认公共构造。 |

## 相关类

- `QImageReader`：应用层读取入口，负责插件选择、错误信息、自动方向和分配上限。
- `QImageWriter`：应用层写入入口，负责格式、质量和输出设备。
- `QImageIOPlugin`：把 handler 注册为可自动发现的图像格式插件。
- `QImage`：handler 的解码结果和编码输入。
- `QIODevice`：字节流的来源或目标。

`QImageIOHandler` 的价值在于把“一个格式如何解码”与“应用想读取什么”分开。实现时最要紧的是维护设备位置、如实报告能力、严格验证输入，并让上层掌握格式策略。
