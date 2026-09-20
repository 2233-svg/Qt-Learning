# QImageWriter

> Qt 6.11.1 · Qt GUI · 来自 `QImageWriter`

## 1. 先建立直觉

`QImageWriter` 是可配置的图像编码器。`QImage::save()` 足够完成“把图写成 PNG”这类简单任务；当你要控制格式、质量、压缩、渐进扫描、文本元数据、子类型、方向元数据，或必须给用户显示失败原因时，使用 `QImageWriter`。

编码能力取决于当前部署的格式插件。调用 `setQuality(90)` 并不意味着所有格式都理解 90；每一个可选项都应该先由 `supportsOption()` 确认，再用 `write()` 的返回值与错误信息作为最终结果。

## 2. 类说明

- 头文件：`#include <QImageWriter>`
- CMake：`target_link_libraries(app PRIVATE Qt6::Gui)`
- 类型：保存输出文件名或外部 `QIODevice*` 的编码配置对象；不拥有外部 device。
- 对指定的 `QIODevice`，调用方负责保持对象存活、打开为可写并处理外部 I/O 错误。
- 常见用途是后台线程把 `QImage` 编码到文件/内存；不要在 worker 里操作 `QPixmap`。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QImageWriter(fileName[, format])` | 输出到文件；未指定 format 时通常从扩展名推断 |
| `QImageWriter(device, format)` | 输出到已有 `QIODevice`，建议显式指定格式 |
| `setFileName()` / `setDevice()` / `setFormat()` | 配置输出目标和编码格式 |
| `canWrite()` | 预检格式与输出设备是否看起来可写 |
| `write(image)` | 编码图像；返回值是唯一成功依据 |
| `error()` / `errorString()` | 获取写入失败的分类与可读诊断 |
| `quality()` / `setQuality()` | 设置有损格式等支持的质量参数 |
| `compression()` / `setCompression()` | 设置格式相关压缩级别/方案 |
| `optimizedWrite()` / `setOptimizedWrite()` | 请求格式相关的优化写入 |
| `progressiveScanWrite()` / `setProgressiveScanWrite()` | 请求 JPEG 等格式的渐进扫描 |
| `subType()` / `setSubType()` | 设置 handler 支持的格式子类型 |
| `supportedSubTypes()` | 查询当前格式支持的子类型 |
| `setText(key, text)` | 写入图像文本元数据，如版权/描述 |
| `setTransformation()` / `transformation()` | 写出或查询方向变换元数据 |
| `supportsOption(option)` | 确认当前 handler 是否支持某项设置 |
| `supportedImageFormats()` / `supportedMimeTypes()` | 查询当前运行时可编码的格式与 MIME |
| `imageFormatsForMimeType()` | MIME 到格式候选的映射 |

## 4. 关键用法

### 明确保存格式并报告失败

```cpp
QImageWriter writer(outputPath, "png");
writer.setText("Author", "Qt Assistant");
writer.setText("Description", "Annotated export");

if (!writer.write(image)) {
    showExportError(writer.errorString());
    return;
}
```

明确传入 `"png"` 避免路径扩展名与业务意图不一致。即使 `canWrite()` 为真，最终仍必须检查 `write()`；磁盘满、权限、无效图像和 handler 内部错误都可能发生在真正编码时。

### 将图像编码到内存再上传

```cpp
QByteArray payload;
QBuffer buffer(&payload);
buffer.open(QIODevice::WriteOnly);

QImageWriter writer(&buffer, "jpeg");
writer.setQuality(85);
if (!writer.write(photo))
    return fail(writer.errorString());

upload(payload, "image/jpeg");
```

设备构造函数没有文件扩展名可供推断，必须指定 format。`QBuffer` 的生命周期要覆盖 `write()`；编码完成前不要把其底层 `QByteArray` 交给会重分配或并发修改的代码。

### 仅在格式支持时设置高级选项

```cpp
QImageWriter writer(fileName, "jpeg");
if (writer.supportsOption(QImageIOHandler::Quality))
    writer.setQuality(90);
if (writer.supportsOption(QImageIOHandler::ProgressiveScanWrite))
    writer.setProgressiveScanWrite(true);

if (!writer.write(image))
    qWarning() << writer.errorString();
```

“设置函数存在”不表示当前格式理解它。PNG、JPEG、TIFF、DDS 等对 quality、compression、subtype 和 progressive 的解释不同，未支持时设置可能被忽略。

### 写方向元数据而不是旋转两次

```cpp
QImageWriter writer(path, "jpeg");
writer.setTransformation(QImageIOHandler::TransformationRotate90);
writer.write(image);
```

若格式支持方向元数据，writer 可以保存它；不支持时 Qt 会在写前应用变换。不要先手工旋转 `image` 又设置同一 transformation，否则读取端启用自动方向时会二次旋转。

## 5. 错误速查

| 错误 | 常见原因与处理 |
| --- | --- |
| `DeviceError` | 路径不可写、磁盘满、网络设备失败、device 未正确打开 |
| `UnsupportedFormatError` | 未指定格式、扩展名不能推断、插件未部署、格式不可写 |
| `InvalidImageError` | 传入空 `QImage` 或 handler 不能编码当前图像 |
| `UnknownError` | 未分类编码失败；记录格式、尺寸、`format()`、`errorString()` |

## 6. 使用场景

- 导出截图、画布、报表、缩略图和用户编辑后的图片。
- 将图像编码进 HTTP 请求、数据库 blob 或自定义容器。
- 设置 JPEG 质量、渐进显示，或选择特定 DDS/TIFF 子类型。
- 向 PNG/JPEG 等支持的格式写入版权、描述、制作信息。
- 保持或指定相机图像的方向元数据。

## 7. 常见坑与经验

- **质量不是通用百分比。** JPEG 0-100 常见，但无损格式可能忽略 `quality()`；压缩值的范围和语义也随 handler 变化。
- **不要认为扩展名决定一切。** 对内存 device 必须显式 format；对文件输出也建议在格式策略明确时显式指定。
- **`canWrite()` 是预检。** 它不能代替 `write()` 的错误处理。
- **元数据支持是可选的。** `setText()` 前可检查 `Description`，否则导出成功但文本可能被丢弃。
- **方向策略只能选一个。** 像素旋转与 transformation 元数据应统一由一处负责。
- **支持列表是运行时信息。** 打包时漏掉 imageformats 插件，会导致开发机能写、发布版不能写。
- **导出前统一颜色和格式。** 目标格式可能不接受 HDR、CMYK 或复杂 alpha；明确 `convertToFormat()` 与颜色空间策略，避免隐式转换带来意外结果。

## 8. 知识点覆盖

图像编码、文件与设备输出、格式插件、质量/压缩/渐进扫描、元数据、方向变换、错误处理、内存输出、部署验证、颜色与格式兼容性。
