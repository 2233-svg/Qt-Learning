# QImageWriter：可控的格式无关图像编码器

> Qt 版本：6.11.1  
> 模块：`Qt6::Gui`  
> 头文件：`#include <QImageWriter>`

## 它解决什么问题

`QImageWriter` 把 `QImage` 编码到文件或 `QIODevice`，并在写出前提供质量、压缩、子格式、渐进扫描、优化写入、文字元数据和方向元数据等格式相关选项。

只需按默认策略保存一张图时，`QImage::save()` 更短；需要选择编码参数、写入 `QBuffer`/网络设备、检查具体错误或根据运行时插件能力降级时，使用 `QImageWriter`。

它是可重入类，但一个 writer 假定独占其 file/device。在 writer 存活期间，其他代码修改同一个设备的读写位置、内容或打开状态，结果未定义。要立即重新打开、移动或提交目标文件，使用一个清晰的局部作用域结束 writer 会话。

## 实际使用场景

- 导出 JPEG 时设置质量，在体积与视觉质量之间取舍。
- 向 `QBuffer` 写 PNG，随后把 `QByteArray` 发到网络或存进数据库。
- 使用 `QSaveFile` 原子替换导出文件，避免写到一半留下损坏目标。
- 将标题、作者、版权等文本嵌入支持 metadata 的格式。
- 对支持的格式选择 subtype，例如同一容器格式中的编码变体。
- 将方向作为 metadata 写入，或在不支持 metadata 时让 Qt 在写出前实际变换像素。
- 用 `supportedImageFormats()` 和 MIME 查询构建导出菜单。

## 最小可靠写入

目标路径能决定格式时可以省略 format；没有扩展名或想避免后缀歧义时，显式传 `"png"`、`"jpeg"` 等格式名。`write()` 的返回值是最终成功判断，失败后读取 `error()` 和 `errorString()`。

```cpp
QImage image = renderPreview();
QImageWriter writer("export/preview.jpg", "jpeg");
writer.setQuality(88);

if (!writer.write(image)) {
    qWarning() << writer.error() << writer.errorString();
}
```

需要原子落盘时，将 writer 限制在 `QSaveFile` 的作用域内，再调用 `commit()`：

```cpp
QSaveFile file("export/report.png");
if (!file.open(QIODevice::WriteOnly)) {
    return;
}

bool encoded = false;
{
    QImageWriter writer(&file, "png");
    encoded = writer.write(image);
    if (!encoded) {
        qWarning() << writer.errorString();
    }
}

if (!encoded || !file.commit()) {
    return;
}
```

`write()` 成功只表示编码数据成功写入该设备；文件路径场景还应考虑磁盘权限、完整路径和类似 `QSaveFile::commit()` 的最终提交结果。

## 文件、设备和格式

默认构造得到空 writer。开始写入前必须先设置 format，再设置 device 或 file name。文件名构造器在 format 为空时根据文件扩展名识别格式；设备构造器没有可靠的后缀可用，因此必须显式提供 format。

`setDevice()` 可替换已设置的旧设备，旧设备本身不会被关闭或销毁。若新设备尚未打开，writer 会尝试以 `WriteOnly` 打开；`QProcess`、`QTcpSocket`、`QUdpSocket` 等需要更复杂打开流程的设备应由调用方先准备好。`setFileName()` 内部创建并以只写模式打开 `QFile`。

`setFormat()` 的格式字符串大小写不敏感，但运行时是否真的有相应编码器取决于 Qt 内建支持和已部署的图像插件。先用 `canWrite()` 做预检，真正写入仍必须检查 `write()`。

## 选项并非每种格式都支持

`QImageWriter` 将许多配置转交给当前 format 的 `QImageIOHandler`。因此在设置或依赖一个选项前，先用 `supportsOption()` 查询：

```cpp
QImageWriter writer("out.png", "png");

if (writer.supportsOption(QImageIOHandler::Description)) {
    writer.setText("Author", "Qt application");
}

if (writer.supportsOption(QImageIOHandler::OptimizedWrite)) {
    writer.setOptimizedWrite(true);
}
```

对于不支持的格式，`setQuality()`、`setCompression()`、`setOptimizedWrite()`、`setProgressiveScanWrite()` 等设置可以被忽略。调用 setter 不等于生成的文件一定使用了该选项。

| 选项 | 含义与边界 |
| --- | --- |
| `quality` | 多用于有损编码，在视觉质量、压缩率和编码时间之间权衡；范围由格式定义，例如 JPEG 常见 0 到 100。 |
| `compression` | 编码器私有的压缩级别/方案，不是统一的“压缩百分比”；例如某些 TIFF handler 用枚举式整数。 |
| `optimizedWrite` | 请求格式的优化写出策略，默认关闭；可能增加编码时间或只在少数编码器中有效。 |
| `progressiveScanWrite` | 请求渐进扫描输出，默认关闭；不是每个格式都支持。 |
| `subType` | 容器或格式族中的具体变体。先查看 `supportedSubTypes()`，再设置。 |
| `text` | 以键值形式写入描述/版权等 metadata；格式不支持时不会神奇地保留它。 |
| `transformation` | 方向 metadata；若格式不能存该 metadata，Qt 会在写前把变换实际应用于像素。 |

## 方向：metadata 与像素不是同一件事

`setTransformation()` 接受 `QImageIOHandler::Transformations`，例如旋转、水平镜像及组合。若输出格式支持方向 metadata，文件可以保留原始像素并写入方向标记；若不支持，Qt 会在写出前实际变换图像。

这意味着相同的 writer 设置可能在两种格式里产生不同的原始像素排列，却在支持方向的查看器中显示一致。若后续系统会忽略 EXIF/方向 metadata，应用应显式在 `QImage` 上完成变换，而不是只依赖 `setTransformation()`。

## 文本与子格式

`setText(key, text)` 在下一次 `write()` 时尝试嵌入元数据。要写一个单独的注释块，可以使用空 key 或 `"Description"`。文本会进入图像文件，可能被任何获得文件的人看到；不要写入密码、访问令牌或仅限内部的业务数据。

`setSubType()` 不是 MIME type，也不是文件扩展名；它是 handler 用来选择格式变体的格式私有名称。用 `supportedSubTypes()` 取得候选值，并先检查 `QImageIOHandler::SupportedSubTypes` / `SubType` 相关 option 是否真的得到支持。

## 错误与运行时格式清单

| 错误 | 含义与排查方向 |
| --- | --- |
| `DeviceError` | 设备打开、写入、磁盘、网络或提交失败；检查 `QIODevice` 自身状态。 |
| `UnsupportedFormatError` | 当前 Qt 运行时不能编码该格式；检查 format、插件目录、部署依赖。 |
| `InvalidImageError` | 传入了无效图像，例如 null `QImage`。 |
| `UnknownError` | 无法归类的失败；若在 `write()` 后出现，可能是 Qt 或插件实现问题。 |

静态 `supportedImageFormats()`、`supportedMimeTypes()` 和 `imageFormatsForMimeType()` 反映**当前运行时**可用编码器，包括能被发现的写入插件。它们需要在 `QGuiApplication` 创建后调用；不要用开发机上的固定列表替代部署环境检测。

## 常见错误

- 只调用 `canWrite()`，却不检查 `write()` 的返回值。
- 在 writer 使用期间从别处读写同一个 `QIODevice`。
- 对 device 输出忘记显式指定 format，期待 Qt 从字节流反推输出格式。
- 把 JPEG 的 quality 数字当成所有格式都共享的统一质量尺度。
- 以为 setter 调用必定生效，没有先调用 `supportsOption()`。
- 用 `setTransformation()` 后又手动旋转同一图像，或反过来在 metadata 不被消费者支持时只写方向标记。
- 将私人数据写入 `setText()`，忽略图片 metadata 会随文件传播。
- 把 `subType` 当作扩展名或 MIME type。
- 忘记在 `QSaveFile` 写入成功后调用 `commit()`。
- 将运行时可写格式列表硬编码，导致部署后插件缺失时才暴露问题。

## API 速查表

| 类别 | API | 语义与边界 |
| --- | --- | --- |
| 类型 | `ImageWriterError` | 错误枚举：`UnknownError`、`DeviceError`、`UnsupportedFormatError`、`InvalidImageError`。 |
| 构造 | `QImageWriter()` | 创建空 writer；写入前必须设置 format，再设置 device 或 file name。 |
| 构造 | `QImageWriter(QIODevice *, QByteArray format)` | 以指定设备和格式创建 writer；设备输出必须明确 format。 |
| 构造 | `QImageWriter(QString fileName, QByteArray format = {})` | 写入指定文件；format 为空时从文件扩展名识别。 |
| 析构 | `~QImageWriter()` | 结束写入会话；若需要马上访问目标资源，使用作用域让 writer 先析构。 |
| 来源 | `setDevice(QIODevice *)` / `device()` | 设置/取得输出设备；未打开时会尝试 `WriteOnly`，旧 device 不由 writer 销毁。 |
| 来源 | `setFileName(QString)` / `fileName()` | 设置/取得输出文件；内部以只写方式使用文件。非文件设备的 `fileName()` 为空。 |
| 格式 | `setFormat(QByteArray)` / `format()` | 设置/取得编码格式，大小写不敏感；可用性仍受当前插件部署影响。 |
| 预检 | `canWrite() const` | 当前格式受支持且设备可写时返回 true；不能替代最终 `write()` 结果。 |
| 写入 | `write(const QImage &)` | 编码图像到已设置文件/设备；成功返回 true，失败后查 `error()` 与 `errorString()`。 |
| 质量 | `setQuality(int)` / `quality()` | 设置/取得有损编码或缩放质量策略；数值范围、效果和是否支持均由格式决定。 |
| 压缩 | `setCompression(int)` / `compression()` | 设置/取得格式私有压缩方式或级别；不支持时可能被忽略。 |
| 子格式 | `setSubType(QByteArray)` / `subType()` | 设置/取得格式内部变体；值应来自当前 handler 支持的候选。 |
| 子格式 | `supportedSubTypes()` | 返回当前格式的可用变体列表；空列表不一定表示写入失败。 |
| 优化 | `setOptimizedWrite(bool)` / `optimizedWrite()` | 请求/查询优化写入标志；默认 false，格式不支持时可被忽略。 |
| 渐进 | `setProgressiveScanWrite(bool)` / `progressiveScanWrite()` | 请求/查询渐进扫描；默认 false，只有部分格式支持。 |
| 方向 | `setTransformation(Transformations)` / `transformation()` | 设置/查询方向 metadata；无法存 metadata 时，写前会实际变换像素。 |
| 文本 | `setText(QString key, QString text)` | 为下一次 `write()` 设置文本 metadata；单块注释可用空 key 或 `Description`。 |
| 能力 | `supportsOption(QImageIOHandler::ImageOption)` | 查询当前 format 是否支持具体 handler option；设定格式后再检查最可靠。 |
| 错误 | `error()` | 返回最近失败的 `ImageWriterError`。 |
| 错误 | `errorString()` | 返回人类可读诊断；逻辑分支应优先使用 `error()`。 |
| 静态列表 | `static supportedImageFormats()` | 返回当前运行时可写格式，包括发现的写入插件；需在 `QGuiApplication` 创建后调用。 |
| 静态列表 | `static supportedMimeTypes()` | 返回可写 MIME 类型；同样需要应用对象已创建。 |
| 静态列表 | `static imageFormatsForMimeType(QByteArray)` | 返回一个 MIME type 对应的可写格式名。 |

## 相关类

- `QImageReader`：读取侧的格式探测、缩放、动画与错误诊断。
- `QImageIOHandler`：实际图像编码后端和格式选项契约。
- `QImageIOPlugin`：向运行时注册新的写入格式。
- `QImage`：writer 的编码输入。
- `QSaveFile`：需要“写完再替换”语义时的安全文件设备。

`QImageWriter` 的重点不是把 `save()` 写得更长，而是让输出格式、编码策略、metadata 与失败原因都成为明确可验证的选择。
