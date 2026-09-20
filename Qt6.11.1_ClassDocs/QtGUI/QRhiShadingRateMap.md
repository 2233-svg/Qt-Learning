# QRhiShadingRateMap

> Qt 6.11.1 · Qt GUI Private · 来自 `QRhiShadingRateMap`

## 1. 先建立直觉

`QRhiShadingRateMap` 描述基于图像/原生对象的可变速率着色映射。它让渲染目标的不同 tile 使用不同 shading rate，例如中心区域 1x1、边缘区域 2x2 或 4x4，从而减少像素着色成本。它常见于 VR/XR、foveated rendering 和性能敏感的后处理。

这是高级 RHI 功能，不是所有后端都支持。使用前要检查 `QRhi::VariableRateShadingMap`，如果要用纹理作为 map，还要检查 `QRhi::VariableRateShadingMapWithTexture`。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`Qt6::GuiPrivate`
- 继承自：`QRhiResource`
- 创建入口：`QRhi::newShadingRateMap()`
- 使用入口：`QRhiSwapChain::setShadingRateMap()`
- Qt 版本：相关 API 从 Qt 6.9 起出现

RHI 提供两条路径：用 `QRhiTexture` 作为 shading rate image，或导入后端原生 shading rate map。Metal 等平台可能走 native object 路径。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `NativeShadingRateMap` | 包装后端原生着色率映射对象，例如 Metal 的 rasterization rate map。 |
| `createFrom(QRhiTexture *src)` | 用 R8UI 纹理创建 shading rate map。 |
| `createFrom(NativeShadingRateMap src)` | 用原生对象创建 shading rate map。 |
| `resourceType()` | 返回 `QRhiResource::ShadingRateMap`。 |

## 4. 关键用法

### 基于纹理的 VRS map

```cpp
if (rhi->isFeatureSupported(QRhi::VariableRateShadingMapWithTexture)) {
    QRhiShadingRateMap *map = rhi->newShadingRateMap();
    map->createFrom(rateTexture);
    swapChain->setShadingRateMap(map);
}
```

`rateTexture` 必须是 `QRhiTexture::R8UI`。尺寸不是 render target 尺寸，而是 tile 网格尺寸：大致为 `ceil(targetSize / tileSize)`。

## 5. 使用场景

- VR/XR foveated rendering。
- 大屏或高分辨率下的外围区域降采样着色。
- D3D12/Vulkan 的 image-based VRS。
- Metal 原生 rasterization rate map 接入。
- 在 swapchain 级别应用 per-tile shading rate。

## 6. 常见坑与经验

- **先查功能。** `VariableRateShadingMap` 和 `VariableRateShadingMapWithTexture` 是两回事。
- **纹理格式必须是 R8UI。** 普通 R8/RGBA8 纹理不等价。
- **尺寸按 tile 网格算。** tile size 用 `QRhi::resourceLimit(QRhi::ShadingRateImageTileSize)` 查询。
- **不是所有后端都支持纹理路径。** Metal 可能使用 native map，而不是 `QRhiTexture`。
- **map 不拥有外部 native 对象语义要看后端。** 原生对象生命周期必须和使用期匹配。
- **VRS 还需要 pipeline/command 配合。** per-draw shading rate 与 map-based shading rate 是相关但不同的控制面。

## 7. 知识点覆盖

- Variable Rate Shading 与 tile-based shading rate image
- texture-backed 和 native-backed shading rate map
- R8UI map、tile size、swapchain 集成
- VR/XR foveated rendering 的资源边界
