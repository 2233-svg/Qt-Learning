# QRhiTextureSubresourceUploadDescription
> Qt 6.11.1 · Qt GUI [Private] · 来自 `QRhiTextureSubresourceUploadDescription`

## 1. 先建立直觉

`QRhiTextureSubresourceUploadDescription` 描述“一小块要上传到纹理的数据”。这里的 subresource 指某个 layer、某个 mip level 里的内容；它只关心像素数据从哪里来、取多大、写到目标的哪个左上角。

它通常不会单独提交，而是放进 `QRhiTextureUploadEntry`，再由 `QRhiTextureUploadDescription` 交给 `QRhiResourceUpdateBatch::uploadTexture()`。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::GuiPrivate)`
- 类型：值类型，保存 `QImage` 或原始字节数据
- 归属：RHI 私有接口，来自 `QRhiTextureSubresourceUploadDescription`

这个类把“数据内容”和“局部上传范围”放在一起。它不表达 layer 和 mip level，layer/level 由外层 `QRhiTextureUploadEntry` 表达。

## 3. API 速查

| API | 作用 |
| --- | --- |
| 默认构造 | 空描述；提交前必须设置 image 或 data |
| `QRhiTextureSubresourceUploadDescription(QImage)` | 用 `QImage` 作为像素来源 |
| `QRhiTextureSubresourceUploadDescription(QByteArray)` | 用字节数组作为像素或压缩块数据 |
| `QRhiTextureSubresourceUploadDescription(const void *, quint32)` | 从内存复制指定字节数 |
| `setImage()` / `image()` | 设置或读取图像来源 |
| `setData()` / `data()` | 设置或读取原始数据来源 |
| `setDataStride()` / `dataStride()` | 设置原始数据每行字节跨度 |
| `setSourceTopLeft()` / `sourceTopLeft()` | 从源图像或数据的哪个左上角开始取 |
| `setSourceSize()` / `sourceSize()` | 取源数据的多大区域；空尺寸表示整个子资源 |
| `setDestinationTopLeft()` / `destinationTopLeft()` | 写入目标 subresource 的哪个位置 |

## 4. 关键用法

整张图片上传最简单：

```cpp
QRhiTextureSubresourceUploadDescription sub(image);
QRhiTextureUploadEntry entry(0, 0, sub);
batch->uploadTexture(texture, QRhiTextureUploadDescription(entry));
```

局部更新时要同时想清楚源矩形和目标点：

```cpp
QRhiTextureSubresourceUploadDescription sub(atlasPatch);
sub.setSourceTopLeft(QPoint(0, 0));
sub.setSourceSize(QSize(64, 64));
sub.setDestinationTopLeft(QPoint(128, 256));
```

原始数据适合压缩纹理、浮点纹理或你已经有自定义排布的像素缓冲：

```cpp
QRhiTextureSubresourceUploadDescription sub(bytes);
sub.setDataStride(rowPitch);
```

`QImage` 路径会自动理解 `bytesPerLine()`；只有使用原始 `data()` 且行之间有 padding 时，才需要 `setDataStride()`。

## 5. 使用场景

- 把 `QImage` 加载的普通贴图传入 GPU。
- 更新纹理图集中的一个小块，避免整张 atlas 重新上传。
- 上传 cubemap 某个面、数组纹理某层、或 mip chain 的某一级。
- 上传压缩纹理块数据或浮点纹理数据。
- 动态视频帧、字体 glyph atlas、粒子贴图等频繁局部更新。

## 6. 常见坑与经验

- `image()` 和 `data()` 不能同时作为有效来源。换来源时要明确覆盖，不要以为它会合并。
- `QImage` 不会自动转成纹理格式匹配的最佳格式；位深和通道排布要与 `QRhiTexture::Format` 兼容。
- `const void *` 构造会复制数据，函数返回后原始内存可以释放；这点适合临时缓冲。
- `setDataStride()` 依赖 `QRhi::ImageDataStride` 功能支持；不支持时应改成紧密排列数据。
- 目标区域越界时 Qt 可能为了避免底层 API 崩溃而裁剪并输出警告，但真正可靠的做法是自己先算好 mip 尺寸和更新矩形。
- 设置 source top-left 或 source size 可能触发内部 `QImage` 副本，频繁更新路径要注意成本。

## 7. 知识点覆盖

本页覆盖：纹理 subresource、layer/mip 分工、完整上传与局部上传、`QImage` 与原始字节数据差异、row pitch/stride、压缩纹理上传、图集更新、GPU 验证层排错。
