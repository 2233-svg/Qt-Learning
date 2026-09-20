# QRhiTextureCopyDescription

> Qt 6.11.1 · Qt GUI Private · 来自 `QRhiTextureCopyDescription`

## 1. 先建立直觉

`QRhiTextureCopyDescription` 描述一次 GPU texture-to-texture copy 的矩形和子资源位置：从源纹理哪个 mip level、哪个 layer、哪个左上角开始，复制多大区域，到目标纹理哪个 mip level、哪个 layer、哪个左上角。

它不携带源和目标 texture 指针；指针由 `QRhiResourceUpdateBatch::copyTexture(dst, src, desc)` 单独传入。把“资源是谁”和“拷贝哪一块”拆开，便于复用描述。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`Qt6::GuiPrivate`
- 类型性质：值类型
- 使用入口：`QRhiResourceUpdateBatch::copyTexture()`
- 默认语义：level/layer 为 `0`，左上角为 `(0,0)`，空 `pixelSize()` 表示复制整个源子资源

## 3. API 速查

| API | 作用 |
| --- | --- |
| `setSourceLevel()` / `sourceLevel()` | 源 mip level。 |
| `setSourceLayer()` / `sourceLayer()` | 源 array layer / cubemap face / 3D slice。 |
| `setSourceTopLeft()` / `sourceTopLeft()` | 源区域左上角像素坐标。 |
| `setDestinationLevel()` / `destinationLevel()` | 目标 mip level。 |
| `setDestinationLayer()` / `destinationLayer()` | 目标 layer。 |
| `setDestinationTopLeft()` / `destinationTopLeft()` | 目标区域左上角像素坐标。 |
| `setPixelSize()` / `pixelSize()` | 复制区域大小；空 size 表示完整子资源。 |

## 4. 关键用法

### 复制整张 level 0 图像

```cpp
updates->copyTexture(dst, src);
```

默认构造的 description 就表示 source layer 0 / level 0 整体复制到 destination layer 0 / level 0。

### 复制图集中的局部块

```cpp
QRhiTextureCopyDescription copy;
copy.setSourceTopLeft(QPoint(64, 0));
copy.setDestinationTopLeft(QPoint(0, 0));
copy.setPixelSize(QSize(32, 32));

updates->copyTexture(dst, atlas, copy);
```

这适合 GPU 内部图集搬运、贴图更新或后处理分区复制。

## 5. 使用场景

- 在 GPU 内复制 render result 到历史纹理。
- 拷贝图集/texture array 的局部区域。
- 处理不同 mip level、cubemap face、array layer。
- 生成中间纹理缓存、ping-pong buffer。

## 6. 常见坑与经验

- **copy 不做格式转换。** 源/目标 format 应一致，尺寸和 sample count 也必须兼容。
- **源要声明 `UsedAsTransferSource`。** 否则不能保证复制可用。
- **坐标是子资源内像素坐标。** mip level 变小后坐标和尺寸要随之变化。
- **空 pixelSize 不是空复制。** 它代表复制整个子资源。
- **layer 的含义取决于纹理类型。** 对 cubemap 是 face，对 array 是数组元素，对 3D 是 slice。

## 7. 知识点覆盖

- GPU texture copy 与 CPU 上传的区别
- mip/layer/subresource 概念
- 局部矩形复制、图集搬运和 ping-pong 纹理
- source transfer flag、格式与尺寸兼容性
