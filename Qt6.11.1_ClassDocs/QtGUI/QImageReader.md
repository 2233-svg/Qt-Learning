# QImageReader

> Qt 6.11.1 · Qt GUI · 来自 `QImageReader`

## 1. 先建立直觉

`QImageReader` 是可配置的图像解码器。相比 `QImage(fileName)` 的一行式便利加载，它允许在真正分配整张图之前查询格式与尺寸、设置缩放/裁剪、读取动画帧、应用 EXIF 方向，并获得清晰错误原因。

处理用户上传图、网络图、超大图、相机图或 GIF/WebP 等多帧内容时，应从 `QImageReader` 开始。它是同步 API；若来源慢或图像大，放到工作线程读取，完成后将 `QImage` 传给 GUI 线程显示。

## 2. 类说明

- 头文件：`#include <QImageReader>`
- CMake：`target_link_libraries(app PRIVATE Qt6::Gui)`
- 类型：持有输入 `QIODevice*` 或文件名的解码配置对象，不拥有外部 device。
- reader 会尝试打开尚未打开的普通 device，但套接字、进程等设备通常仍须由调用者按自身协议准备好。
- 图像格式支持来自 Qt 内置处理器及已部署的 imageformat 插件；运行环境而非源代码决定最终可读格式列表。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QImageReader(fileName[, format])` | 从文件创建 reader，可显式指定格式 |
| `QImageReader(device[, format])` | 从已有 `QIODevice` 创建 reader |
| `setFileName()` / `setDevice()` / `setFormat()` | 配置图像来源和预期格式 |
| `canRead()` | 轻量预检，不保证完整解码一定成功 |
| `read()` / `read(QImage *)` | 解码当前帧；指针重载可复用兼容缓冲区 |
| `error()` / `errorString()` | 在失败后获取分类与可读错误说明 |
| `format()` / 静态 `imageFormat()` | 查询检测出的格式 |
| `supportedImageFormats()` / `supportedMimeTypes()` | 查询当前运行环境支持什么 |
| `imageFormatsForMimeType()` | 把 MIME 类型映射到候选格式 |
| `size()` / `imageFormat()` | 尽量在不读整张图前获取尺寸与输出像素格式 |
| `setScaledSize()` / `scaledSize()` | 请求解码器直接缩放，常可显著省内存 |
| `setClipRect()` / `setScaledClipRect()` | 请求只读取 ROI 或缩放后的 ROI |
| `setAutoTransform()` / `transformation()` | 自动应用或查询 EXIF 等方向元数据 |
| `setAutoDetectImageFormat()` | 控制扩展名/内容自动检测 |
| `setDecideFormatFromContent()` | 强制由内容决定 handler，可能加载所有插件 |
| `supportsAnimation()` | 查询是否支持多帧 |
| `imageCount()` / `currentImageNumber()` | 查询帧总数与当前位置 |
| `read()` 重复调用 | 顺序读取动画或多页图像的下一帧 |
| `jumpToImage()` / `jumpToNextImage()` | 在支持时跳帧 |
| `nextImageDelay()` / `loopCount()` | 获取动画播放间隔与循环信息 |
| `setBackgroundColor()` | 为支持该选项的格式设置解码背景 |
| `textKeys()` / `text()` | 读取图像文本元数据 |
| `subType()` / `supportedSubTypes()` | 查询格式子类型 |
| `supportsOption()` | 先确认格式 handler 是否支持某项功能 |
| `allocationLimit()` / `setAllocationLimit()` | Qt 6 起控制单图解码分配上限，降低解压炸弹风险 |
| `quality()` / `setQuality()` | 读取或请求格式相关的解码质量取舍 |

## 4. 关键用法

### 先查尺寸，再按目标大小解码

```cpp
QImageReader reader(filePath);
reader.setAutoTransform(true);

if (!reader.canRead()) {
    reportImageError(reader.errorString());
    return;
}

const QSize sourceSize = reader.size();
reader.setScaledSize(sourceSize.scaled(512, 512, Qt::KeepAspectRatio));

QImage preview = reader.read();
if (preview.isNull())
    reportImageError(reader.errorString());
```

不要总是“解码原图再缩小”。数千万像素图片会先占用巨量内存和 CPU；如果 handler 支持缩放，`setScaledSize()` 让它在解码阶段完成。缩放尺寸必须在 `read()` 前设置。

### 读取相机照片时尊重方向

```cpp
QImageReader reader(filePath);
reader.setAutoTransform(true);
const QImage image = reader.read();
```

很多手机照片像素本身是横向的，依靠 EXIF Orientation 指示显示旋转。默认不一定自动应用；显示导入照片时通常应显式 `setAutoTransform(true)`。若业务要保留原始像素与元数据，关闭它并自行读取 `transformation()`。

### 防止异常输入占满内存

```cpp
QImageReader::setAllocationLimit(256); // MiB，进程级限制

QImageReader reader(device);
if (!reader.canRead())
    return reject(reader.errorString());

const QSize size = reader.size();
if (size.width() > 12000 || size.height() > 12000)
    return reject("Image dimensions are too large");
```

allocation limit 是全局防线，不是完整的内容安全方案。像素维度、文件大小、解码时间、动画帧数与总帧内存都应根据产品限制额外控制。把 limit 设为 `0` 会禁用这项保护，除非处理受信任的专业图像，否则不建议。

### 读取动画帧

```cpp
QImageReader reader(":/media/loading.gif");
if (!reader.supportsAnimation())
    return;

while (reader.canRead()) {
    const QImage frame = reader.read();
    const int delayMs = reader.nextImageDelay();
    enqueueFrame(frame, delayMs);
}
```

`read()` 对多帧格式会推进到下一帧，读取结束后返回空图。实际播放器通常应使用 `QMovie`，它封装定时和缓存；`QImageReader` 更适合你需要手动帧处理或导出时。

## 5. 错误速查

| 错误 | 常见原因与处理 |
| --- | --- |
| `FileNotFoundError` | 路径错误、资源不存在，或无扩展名时找不到可支持的文件 |
| `DeviceError` | 流不可读、I/O 中断、网络/文件设备问题 |
| `UnsupportedFormatError` | 格式/插件未部署，或指定的 format 不可读 |
| `InvalidDataError` | 文件损坏、截断、恶意数据或不是对应格式 |
| `UnknownError` | 未分类失败；记录 `errorString()`、格式、文件大小后再诊断 |

## 6. 常见坑与经验

- **`canRead()` 不是最终验证。** 它只做快速检查；真正成功条件仍是 `read()` 返回非空或 `read(&image)` 为真。
- **不要依赖扩展名。** 用户上传的 `.jpg` 可能是别的内容；需要内容优先检测时用 `imageFormat(device)` 或配置 `setDecideFormatFromContent()`，但要考虑插件探测成本。
- **设置顺序重要。** device/file、format、ROI、缩放、自动方向等都应在第一次 `read()` 前完成。
- **device 不归 reader 所有。** `QBuffer`、`QFile`、网络流必须由调用方维持到读取完成；也要保证读位置正确。
- **`size()` 可能不被所有 handler 支持。** 调用前后用 `supportsOption(QImageIOHandler::Size)` 判断，不能将无效大小视为安全。
- **支持格式不是编译期常量。** 部署 imageformat 插件后列表会改变；诊断时记录 `supportedImageFormats()`。
- **reader 不会自动异步。** 网络下载完成、文件读取和解码都可能阻塞，放到恰当的工作线程。

## 7. 知识点覆盖

同步解码、解码前缩放与 ROI、EXIF 方向、图像格式探测、插件部署、动画帧、输入验证、解压炸弹防护、设备生命周期、错误分类、后台图像管线。
