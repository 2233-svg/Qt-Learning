# QImageIOHandler

> Qt 6.11.1 · Qt GUI · 来自 `QImageIOHandler`

## 1. 先建立直觉

`QImageIOHandler` 是 Qt 图像格式插件的编解码实现接口。`QImageReader` 和 `QImageWriter` 把公共 API 转成这里的 `canRead()`、`read()`、`write()`、`option()` 和动画帧操作；应用程序正常读取 PNG/JPEG 时不需要直接继承它。

只有在实现私有图像格式、硬件相机格式、行业容器或自定义流媒体图片插件时，才直接接触它。此时最重要的不是“能否把字节转成像素”，而是遵守流位置、内存限制、可选能力和方向元数据的契约。

## 2. 类说明

- 头文件：`#include <QImageIOHandler>`
- CMake：`target_link_libraries(app PRIVATE Qt6::Gui)`
- 类型：非 QObject 的多态基类；由 `QImageIOPlugin::create()` 创建，通常交给 Qt reader/writer 管理。
- 必须实现：`canRead() const` 与 `read(QImage *)`；若支持写入，重载 `write(const QImage &)`.
- `QIODevice*` 不归 handler 所有；handler 只使用由 Qt 设置的 device。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `canRead()` | 快速判断当前 device 是否像此格式；必须尽量不消费数据 |
| `read(QImage *)` | 解码当前图像/帧到输出 `QImage` |
| `write(image)` | 编码图像到 device；默认返回 `false` |
| `device()` / `setDevice()` | 读取或一次性设定输入输出设备 |
| `format()` / `setFormat()` | 读取或设定格式标识；`const setFormat()` 允许在 `canRead()` 中修正 |
| `supportsOption(option)` | 声明 handler 支持哪些能力 |
| `option(option)` | 读取能力参数，如尺寸、帧数、描述、方向 |
| `setOption(option, value)` | 接收 reader/writer 的缩放、裁剪、质量等配置 |
| `ImageOption::Size` | 不完整解码即可获得原始尺寸 |
| `ClipRect` / `ScaledSize` / `ScaledClipRect` | 声明支持 ROI、解码时缩放和缩放后 ROI |
| `Description` / `Name` | 图片文本或名称元数据 |
| `CompressionRatio` / `Gamma` / `Quality` | 格式特有的编码配置 |
| `SubType` / `SupportedSubTypes` | 同格式的存储变体能力 |
| `Animation` / `IncrementalReading` | 声明多帧或渐进读取能力 |
| `ImageFormat` | 声明 `read()` 输出的 `QImage::Format` |
| `ImageTransformation` | 读取/写入方向元数据，通常不直接改像素 |
| `currentImageNumber()` / `imageCount()` | 报告多帧序号和总数 |
| `jumpToImage()` / `jumpToNextImage()` | 支持随机或顺序跳帧 |
| `currentImageRect()` | 报告当前动画帧更新的区域 |
| `loopCount()` / `nextImageDelay()` | 报告动画循环次数和下帧等待时间 |
| `allocateImage(size, format, image)` | Qt 6 起按全局 allocation limit 安全分配输出图像 |
| `Transformations` | 表达镜像、翻转、90/180/270 度方向组合 |

## 4. 实现关键

### 正确实现非破坏性格式探测

```cpp
bool AcmeHandler::canRead() const
{
    QIODevice *dev = device();
    if (!dev)
        return false;

    const QByteArray header = dev->peek(8);
    if (header != "ACMEIMG\0")
        return false;

    setFormat("acme");
    return true;
}
```

`canRead()` 可能被 Qt 调用多次，也可能与其他 handler 竞争同一个 device。必须用 `peek()` 或保存/恢复位置，不能用不可逆 `read()` 吃掉头字节；否则真正 `read()` 会从错误偏移开始。

### 分配前先验证尺寸和限制

```cpp
bool AcmeHandler::read(QImage *image)
{
    const Header h = parseHeader(device());
    if (!h.valid() || h.width > 16384 || h.height > 16384)
        return false;

    if (!allocateImage({h.width, h.height},
                       QImage::Format_RGBA8888, image))
        return false;

    return decodePixels(device(), image);
}
```

不要直接 `*image = QImage(size, format)`。`allocateImage()` 会同时检查参数与 `QImageReader` 的全局内存上限，令你的插件与 Qt 的解压炸弹防护保持一致。格式文件里的宽高、帧数和压缩长度全部是不可信输入。

### 将可选能力声明和实现保持一致

```cpp
bool AcmeHandler::supportsOption(ImageOption option) const
{
    return option == Size
        || option == ScaledSize
        || option == ImageTransformation;
}

QVariant AcmeHandler::option(ImageOption option) const
{
    if (option == Size)
        return headerSizeWithoutFullDecode();
    if (option == ImageTransformation)
        return int(TransformationRotate90);
    return {};
}
```

只有真的实现了选项语义才返回 `true`。虚报 `ScaledSize` 会让 `QImageReader` 假定你已在解码阶段缩小图，导致额外内存或尺寸不一致；虚报方向却已经旋转像素，会在 `setAutoTransform(true)` 时二次变换。

## 5. 方向与动画契约

| 能力 | handler 应做什么 |
| --- | --- |
| `ImageTransformation` | 返回/写入元数据，不主动把像素旋转；由 `QImageReader` 决定是否自动应用 |
| `Animation` | 支持多帧时报告帧序号、延迟、循环和当前帧区域 |
| `IncrementalReading` | 允许在连续输入上逐步更新，并正确复用上一次输出图像语义 |
| `ClipRect` + `ScaledSize` | 明确处理顺序：原图 ROI，缩放，再缩放后 ROI |

## 6. 常见坑与经验

- **这是插件接口，不是应用 API。** 应用要读图时使用 `QImageReader`，它会处理 handler 选择、回退和公共错误路径。
- **不要持有已失效的 device。** 设备由外部创建；handler 生命周期内它必须有效并处于正确读写模式。
- **返回 `QVariant` 时类型必须准确。** `Size` 是 `QSize`，`Quality` 常为整数，方向通常是枚举/整型值；错类型会让上层安静失效。
- **默认跳帧实现什么也不做。** 只有确实支持定位时才重载 `jumpToImage()`；否则要让调用者知道随机访问不可用。
- **分块解码也要考虑部分失败。** `read()` 失败时不要把半初始化、看似有效的图像交给调用者。
- **线程安全由实现决定。** 不要让静态解码缓存因多个 reader 并发调用而无锁共享。

## 7. 知识点覆盖

图像格式插件、设备流契约、非破坏性探测、安全内存分配、ROI/缩放、动画帧、EXIF 方向、QVariant 选项、插件线程安全、输入校验。
