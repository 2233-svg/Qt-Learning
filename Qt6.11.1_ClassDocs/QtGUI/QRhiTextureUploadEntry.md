# QRhiTextureUploadEntry
> Qt 6.11.1 · Qt GUI [Private] · 来自 `QRhiTextureUploadEntry`

## 1. 先建立直觉

`QRhiTextureUploadEntry` 是“把这份子资源数据写到纹理的哪一层、哪一级 mip”的三元组：`layer`、`level`、`description`。它不关心整个上传批次，也不关心目标纹理对象；这些由外层的 `QRhiTextureUploadDescription` 和 `uploadTexture()` 负责。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::GuiPrivate)`
- 类型：值类型
- 归属：RHI 私有接口，来自 `QRhiTextureUploadEntry`

默认构造的 entry 指向 layer 0、level 0，但没有有效数据描述。实际提交前必须设置 `QRhiTextureSubresourceUploadDescription`。

## 3. API 速查

| API | 作用 |
| --- | --- |
| 默认构造 | layer 和 level 默认为 0，description 为空 |
| `QRhiTextureUploadEntry(layer, level, desc)` | 一次性指定目标层级和上传内容 |
| `setLayer()` / `layer()` | 设置或读取数组层、cubemap 面等 layer 索引 |
| `setLevel()` / `level()` | 设置或读取 mip level |
| `setDescription()` / `description()` | 设置或读取该 layer/level 的实际上传数据 |

## 4. 关键用法

把 `QImage` 上传到普通 2D 纹理：

```cpp
QRhiTextureSubresourceUploadDescription sub(image);
QRhiTextureUploadEntry entry(0, 0, sub);
```

上传 mip level 2：

```cpp
entry.setLevel(2);
entry.setDescription(QRhiTextureSubresourceUploadDescription(mip2Image));
```

上传数组纹理第 3 层：

```cpp
QRhiTextureUploadEntry layerEntry(3, 0, QRhiTextureSubresourceUploadDescription(layerImage));
```

这里的 layer 语义由目标纹理类型决定：2D 纹理通常只有 0；纹理数组表示数组层；cubemap 通常对应不同面。

## 5. 使用场景

- 普通贴图的一次 level 0 上传。
- cubemap 的每个面分别构造一个 entry。
- 数组纹理批量填充多层图片。
- 自己生成 mip chain，然后逐级 entry 上传。
- atlas 局部更新时，同一 layer/level 下放多个 entry。

## 6. 常见坑与经验

- 不要把 `level` 当成缩放比例，它是 mip 索引；level 1 的尺寸通常是 level 0 的一半，但边界要按纹理实际规则计算。
- `layer` 越界不会因为 entry 是值类型就变安全，错误会在上传或后端验证时暴露。
- 默认构造 entry 只是占位。没有 description 的 entry 不该被提交。
- description 里的 source/destination 矩形描述的是该 layer/level 内部的位置，不会改变 entry 的 layer/level。
- cubemap 面顺序要和 Qt/RHI 对该纹理类型的约定保持一致，最好集中封装，不要在多处硬编码数字。

## 7. 知识点覆盖

本页覆盖：纹理层与 mip level、entry 与 subresource 的边界、普通 2D/数组/cubemap 上传差异、局部更新、越界与格式兼容检查。
