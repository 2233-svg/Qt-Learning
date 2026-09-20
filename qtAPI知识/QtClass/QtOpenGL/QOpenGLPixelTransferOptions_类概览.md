# QOpenGLPixelTransferOptions 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLPixelTransferOptions>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：无  
> 定位：描述纹理上传时的 OpenGL unpack 像素存储规则

## 它解决什么问题

`QOpenGLPixelTransferOptions` 是传给 `QOpenGLTexture::setData()` 等上传接口的选项对象，用来描述源像素内存如何排列。它对应 OpenGL 的 `GL_UNPACK_*` 状态，例如行对齐、跳过多少行/像素/图层、每行实际像素数、3D 纹理 image height、字节交换和位顺序。

它解决的是“CPU 内存里的图片布局和 OpenGL 默认假设不一致”这个问题。默认 OpenGL 假设每行按 4 字节对齐，且上传从指针开头连续读取；现实中图像常有行步长、子区域、纹理图集、3D 切片或紧密 RGB 数据。这个类让你把这些差异显式告诉 Qt/OpenGL，而不是手工复制一份临时连续缓冲。

## 实际使用场景

- 上传 RGB888 图像时把 `alignment` 改为 `1`，避免每行宽度不是 4 字节倍数导致错行；
- 从一张大图中上传子区域，用 `skipRows()` 和 `skipPixels()` 跳过起始偏移；
- 上传 3D texture 或 texture array 的某个切片，用 `imageHeight()`、`skipImages()` 描述层间跨度；
- 处理 bitmap 或多字节像素数据时指定 bit order 或 byte swap；
- 在资源加载器中把图像 pitch/stride 显式转换为 OpenGL unpack 参数。

## 使用示例

```cpp
#include <QOpenGLPixelTransferOptions>
#include <QOpenGLTexture>

void uploadRgb(QOpenGLTexture &texture, const void *pixels, int width)
{
    QOpenGLPixelTransferOptions options;
    options.setAlignment(1);
    options.setRowLength(width);

    texture.setData(QOpenGLTexture::RGB,
                    QOpenGLTexture::UInt8,
                    pixels,
                    &options);
}
```

选项对象是值类型，内部使用共享数据，复制成本低。它只描述上传参数，不保存像素数据，也不创建 OpenGL 资源。

## 核心语义

### 它描述的是 unpack，不是 pack

这些设置影响“从客户端内存读出像素上传到纹理”的过程，即 OpenGL `GL_UNPACK_*` 状态。它不控制 `glReadPixels()` 读回时的 `GL_PACK_*` 状态。

### 默认值就是 OpenGL 默认 unpack 状态

`alignment` 默认是 `4`；`rowLength`、`imageHeight`、`skipRows`、`skipPixels`、`skipImages` 默认是 `0`；`swapBytes` 和 `lsbFirst` 默认是 `false`。默认值适合很多 RGBA8 连续图像，但不适合所有 RGB/灰度/带 stride 的数据。

### “skip” 等价于移动源指针，但更可读

`setSkipPixels()`、`setSkipRows()`、`setSkipImages()` 等价于让 OpenGL 从源数据内部偏移处开始读。它们特别适合上传子区域，但前提是 `rowLength()`/`imageHeight()` 正确描述完整源图的跨度。

## API 速查表

| API | 对应 OpenGL 状态 | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| `QOpenGLPixelTransferOptions()` | 一组 `GL_UNPACK_*` 默认值 | 创建默认上传选项。 | 默认 `alignment` 为 4，其他偏移/跨度多为 0。 |
| `QOpenGLPixelTransferOptions(const QOpenGLPixelTransferOptions &)` / `operator=` | 值语义 | 复制选项对象。 | 内部共享数据；修改时按 Qt 隐式共享语义分离。 |
| `~QOpenGLPixelTransferOptions()` | 无 | 销毁选项对象。 | 不拥有像素数据或 OpenGL 对象。 |
| `swap(QOpenGLPixelTransferOptions &other)` | 无 | 快速交换两个选项对象的数据。 | `noexcept`，适合容器/赋值实现。 |
| `setAlignment(int alignment)` / `alignment() const` | `GL_UNPACK_ALIGNMENT` | 设置/查询每行像素起始地址的字节对齐要求。 | 常用值是 1、2、4、8；RGB888 宽度不齐时常设为 1。 |
| `setRowLength(int rowLength)` / `rowLength() const` | `GL_UNPACK_ROW_LENGTH` | 设置/查询源内存中一行实际有多少像素。 | 0 表示使用上传宽度；有 pitch/stride 时要设完整行宽。 |
| `setImageHeight(int imageHeight)` / `imageHeight() const` | `GL_UNPACK_IMAGE_HEIGHT` | 设置/查询 3D/array 数据中一张 image 的高度。 | 0 表示使用上传高度；只在分层/3D 上传时常用。 |
| `setSkipRows(int skipRows)` / `skipRows() const` | `GL_UNPACK_SKIP_ROWS` | 跳过源内存开头的若干行。 | 与 `rowLength()` 共同决定起始偏移。 |
| `setSkipPixels(int skipPixels)` / `skipPixels() const` | `GL_UNPACK_SKIP_PIXELS` | 跳过源内存开头当前行的若干像素。 | 用于子矩形上传；不要再手工偏移同一段距离。 |
| `setSkipImages(int skipImages)` / `skipImages() const` | `GL_UNPACK_SKIP_IMAGES` | 跳过源内存开头的若干 2D image/层。 | 用于 3D texture 或 array texture 的子层上传。 |
| `setLeastSignificantByteFirst(bool lsbFirst)` / `isLeastSignificantBitFirst() const` | `GL_UNPACK_LSB_FIRST` | 设置/查询字节内 bit 顺序是否从低位到高位。 | 主要影响 bitmap 数据；普通 RGBA/RGB 图像很少需要。 |
| `setSwapBytesEnabled(bool swapBytes)` / `isSwapBytesEnabled() const` | `GL_UNPACK_SWAP_BYTES` | 设置/查询多字节分量是否交换字节序。 | 只影响多字节 component；不要用它修正通道顺序问题。 |

## 常见误区

### 忘记 RGB 数据的对齐

RGB888 每像素 3 字节，宽度不是 4 的倍数时，默认 `alignment = 4` 很容易导致纹理斜线或错色。优先把 alignment 设为 1。

### 同时手动偏移指针又设置 skip

`skipRows`、`skipPixels`、`skipImages` 已经表达了源偏移。若调用方也把指针提前移动，实际偏移会重复。

### 用 byte swap 修复 BGR/RGB 顺序

`setSwapBytesEnabled()` 交换的是多字节分量内部的字节序，不是把 R 和 B 通道互换。通道顺序应通过纹理格式、像素格式或预处理解决。

## 一句话总结

`QOpenGLPixelTransferOptions` 是纹理上传的“内存布局说明书”；一旦源图像不是默认连续 RGBA 排列，就应该用它把 stride、对齐和子区域偏移说清楚。
