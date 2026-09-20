# QRhiTextureUploadDescription
> Qt 6.11.1 · Qt GUI [Private] · 来自 `QRhiTextureUploadDescription`

## 1. 先建立直觉

`QRhiTextureUploadDescription` 是一次纹理上传请求的总清单。它由多个 `QRhiTextureUploadEntry` 组成，每个 entry 指向一个 layer 和 mip level，再携带对应的子资源数据。

它解决的问题是：一次 `uploadTexture()` 不一定只传一张 level 0 图片，也可能同时传 cubemap 六个面、数组纹理多层、手工 mip chain，或者同一层里的多个局部矩形。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::GuiPrivate)`
- 类型：值类型，内部保存 entry 列表
- 归属：RHI 私有接口，来自 `QRhiTextureUploadDescription`

它不直接执行上传；执行者是 `QRhiResourceUpdateBatch`。描述对象可以短生命周期，因为提交时 RHI 会按自己的规则接管或复制必要数据。

## 3. API 速查

| API | 作用 |
| --- | --- |
| 默认构造 | 创建空上传清单 |
| `QRhiTextureUploadDescription(entry)` | 创建只有一个 entry 的上传 |
| `QRhiTextureUploadDescription({ ... })` | 创建多个 entry 的上传 |
| `setEntries(initializer_list)` | 用列表替换所有 entry |
| `setEntries(first, last)` | 从迭代器范围替换所有 entry |
| `entryCount()` | 返回 entry 数量 |
| `entryAt(index)` | 读取指定 entry |
| `cbeginEntries()` / `cendEntries()` | 遍历 entry |

## 4. 关键用法

单张 2D 纹理：

```cpp
QRhiTextureUploadDescription upload(
    QRhiTextureUploadEntry(0, 0, QRhiTextureSubresourceUploadDescription(image)));
batch->uploadTexture(texture, upload);
```

手工上传多个 mip：

```cpp
QRhiTextureUploadDescription upload({
    QRhiTextureUploadEntry(0, 0, QRhiTextureSubresourceUploadDescription(level0)),
    QRhiTextureUploadEntry(0, 1, QRhiTextureSubresourceUploadDescription(level1)),
    QRhiTextureUploadEntry(0, 2, QRhiTextureSubresourceUploadDescription(level2))
});
```

同一个 layer/level 可以出现多次，适合把多个不相邻的小矩形合并进一次资源更新批次，比多次 `uploadTexture()` 更容易减少命令提交开销。

## 5. 使用场景

- 普通贴图：一个 entry，layer 0、level 0。
- Cubemap：六个 face 分别作为 layer 或特定层上传。
- 纹理数组：多层图片一次组装。
- 手工 mip chain：每个 mip level 一个 entry。
- 动态 atlas：多个局部更新 entry 合并进同一次 batch。

## 6. 常见坑与经验

- 空 description 没有意义；提交前至少要有一个有效 entry。
- entry 的 layer 和 level 必须落在目标 `QRhiTexture` 创建时声明的范围内。
- 不同 entry 的数据格式仍然要和目标纹理格式兼容；description 不会替你转换像素格式。
- 多个局部 entry 指向同一区域时，最终结果取决于执行顺序和后端行为；不要依赖重叠写入来表达逻辑。
- 上传只是资源更新请求，通常需要在正确的 frame 和 pass 边界提交，避免读写同一资源的同步问题。

## 7. 知识点覆盖

本页覆盖：资源更新批次、entry 列表、layer/mip 索引、cubemap 和数组纹理上传、手工 mip、局部更新合并、上传顺序与同步意识。
