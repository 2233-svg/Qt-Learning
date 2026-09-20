# QRhiSampler

> Qt 6.11.1 · Qt GUI Private · 来自 `QRhiSampler`

## 1. 先建立直觉

`QRhiSampler` 描述 shader 采样纹理时的规则：纹理坐标超出范围时怎么包裹，放大/缩小时用最近邻还是线性过滤，是否使用 mipmap，以及采样深度纹理时是否做比较。

纹理保存数据，sampler 决定怎样读数据。同一张纹理可以配不同 sampler 得到不同视觉效果：像素风用 nearest，普通图片缩放用 linear，重复平铺用 repeat，UI 图标常用 clamp-to-edge。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`Qt6::GuiPrivate`
- 继承自：`QRhiResource`
- 创建入口：`QRhi::newSampler(...)`
- 使用入口：`QRhiShaderResourceBinding::sampledTexture(...)`

sampler 创建后通常长期复用。大量材质共享同样过滤和包裹规则时，不要为每个对象重复创建完全相同的 sampler。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `Filter::Nearest` | 最近邻采样，适合像素风、数据纹理。 |
| `Filter::Linear` | 线性过滤，适合图片平滑缩放。 |
| `Filter::None` | 仅用于 mipmap mode，表示不使用 mipmap。 |
| `AddressMode::Repeat` | 纹理坐标重复平铺。 |
| `AddressMode::ClampToEdge` | 超出范围时夹到边缘，常用于 UI/图集。 |
| `AddressMode::Mirror` | 镜像重复。 |
| `CompareOp` | 深度比较采样使用的比较函数。 |
| `setMagFilter()` / `magFilter()` | 设置/读取放大过滤。 |
| `setMinFilter()` / `minFilter()` | 设置/读取缩小过滤。 |
| `setMipmapMode()` / `mipmapMode()` | 设置/读取 mipmap 过滤。 |
| `setAddressU/V/W()` | 设置 U/V/W 坐标包裹模式。 |
| `setTextureCompareOp()` | 设置深度纹理比较操作。 |
| `resourceType()` | 返回 `QRhiResource::Sampler`。 |

## 4. 关键用法

### 普通图片采样

```cpp
QRhiSampler *sampler = rhi->newSampler(QRhiSampler::Linear,
                                       QRhiSampler::Linear,
                                       QRhiSampler::Linear,
                                       QRhiSampler::ClampToEdge,
                                       QRhiSampler::ClampToEdge);
sampler->create();
```

这适合 UI 图片或普通纹理缩放。使用 mipmap mode 为 `Linear` 前，纹理本身需要有 mip levels。

### 像素风或数据纹理

```cpp
QRhiSampler *nearest = rhi->newSampler(QRhiSampler::Nearest,
                                       QRhiSampler::Nearest,
                                       QRhiSampler::None,
                                       QRhiSampler::ClampToEdge,
                                       QRhiSampler::ClampToEdge);
```

nearest 避免插值，适合颜色表、mask、整数编码纹理、像素艺术。

### 阴影深度比较

```cpp
sampler->setTextureCompareOp(QRhiSampler::LessOrEqual);
```

比较采样用于 shadow map 一类深度纹理场景。shader、纹理格式和资源绑定也要按比较采样语义准备。

## 5. 使用场景

- UI 纹理、图集、材质贴图采样。
- 平铺背景或 repeat 纹理。
- 像素风 nearest 采样。
- mipmapped 远距离纹理过滤。
- shadow map 深度比较采样。
- 3D 纹理或 cubemap 的 U/V/W 包裹控制。

## 6. 常见坑与经验

- **sampler 不保存纹理数据。** 它只描述采样规则。
- **mipmap mode 要和纹理 mip levels 配套。** 没有 mipmap 的纹理不要随便设置 mipmap filtering。
- **ClampToEdge 可避免图集边缘串色。** 图集采样常配合 padding 和 clamp。
- **Repeat 对 NPOT 纹理可能有后端限制。** 旧 GLES 场景要查 `NPOTTextureRepeat`。
- **比较采样不是普通颜色采样。** 需要深度纹理、合适 shader 声明和 compare op。
- **创建后改参数通常要重新创建。** 把 sampler 当不可变状态对象缓存更自然。

## 7. 知识点覆盖

- 纹理数据与采样状态的分离
- min/mag/mipmap filter 的区别
- U/V/W address mode 和图集边缘问题
- mipmap、NPOT、深度比较采样
- sampler 复用和材质系统设计
