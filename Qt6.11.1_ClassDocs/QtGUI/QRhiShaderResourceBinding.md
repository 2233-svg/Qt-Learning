# QRhiShaderResourceBinding

> Qt 6.11.1 · Qt GUI Private · 来自 `QRhiShaderResourceBinding`

## 1. 先建立直觉

`QRhiShaderResourceBinding` 描述 shader 某个 binding 点上放什么资源：uniform buffer、sampled texture、独立 texture、独立 sampler、storage image、storage buffer 等。它是单个 binding；多个 binding 组合起来才是 `QRhiShaderResourceBindings`。

关键思想是：binding 既包含“布局信息”，也可以包含“实际资源”。布局信息包括 binding 编号、stage 可见性、资源类型；实际资源则是具体 buffer、texture、sampler、offset、size。创建 pipeline 时可以用空资源的 binding 只表达 layout，draw/dispatch 时再绑定 layout-compatible 的实际资源集合。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`Qt6::GuiPrivate`
- 类型性质：值类型，可比较、可哈希
- 所属集合：`QRhiShaderResourceBindings`
- 主要协作：`QRhiBuffer`、`QRhiTexture`、`QRhiSampler`、`QShader`

binding 编号必须和 shader 里的 `layout(binding = N)` 或经 `QShader` 反射/翻译后的绑定约定一致。stage flags 要覆盖 shader 实际访问该资源的阶段。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `StageFlags` | 指定资源在哪些 shader stage 可见：Vertex、Fragment、Compute、Geometry、Tessellation 等。 |
| `Type` | 指定资源类型：UniformBuffer、SampledTexture、Texture、Sampler、ImageLoad/Store、BufferLoad/Store。 |
| `uniformBuffer()` | 绑定 uniform/constant buffer，可指定 offset/size。 |
| `uniformBufferWithDynamicOffset()` | 使用动态 offset 的 uniform buffer。 |
| `sampledTexture()` / `sampledTextures()` | 绑定组合 texture+sampler，支持数组。 |
| `texture()` / `textures()` | 绑定独立纹理对象。 |
| `sampler()` | 绑定独立 sampler。 |
| `imageLoad()` / `imageStore()` / `imageLoadStore()` | 绑定 storage image，用于 image load/store。 |
| `bufferLoad()` / `bufferStore()` / `bufferLoadStore()` | 绑定 storage buffer。 |
| `isLayoutCompatible()` | 判断两个单 binding 的布局是否兼容，不比较具体资源对象。 |

## 4. 关键用法

### uniform + texture

```cpp
auto ub = QRhiShaderResourceBinding::uniformBuffer(
    0, QRhiShaderResourceBinding::VertexStage, uniformBuffer);

auto tex = QRhiShaderResourceBinding::sampledTexture(
    1, QRhiShaderResourceBinding::FragmentStage, texture, sampler);
```

这对应常见 shader：顶点阶段读 binding 0 的 uniform，片段阶段读 binding 1 的 sampler2D。

### 只创建 layout，不指定资源

```cpp
auto layoutOnly = QRhiShaderResourceBinding::uniformBuffer(
    0, QRhiShaderResourceBinding::VertexStage, nullptr);
```

这种 binding 不能直接用于 `setShaderResources()`，但可以放进 pipeline 使用的 SRB 来声明布局。实际绘制时换成 layout-compatible 且资源非空的 SRB。

### storage buffer 用于 compute

```cpp
auto data = QRhiShaderResourceBinding::bufferLoadStore(
    0, QRhiShaderResourceBinding::ComputeStage, storageBuffer);
```

storage buffer 主要保证在 compute pipeline 中可用。图形阶段使用 storage buffer 的可移植性更差，要谨慎。

## 5. 使用场景

- 为 graphics/compute pipeline 描述资源 layout。
- 每个 draw 或 dispatch 绑定不同材质/对象 uniform。
- 绑定贴图、sampler、texture array。
- compute shader 读写 storage buffer 或 storage image。
- pipeline cache 中比较 shader resource layout 是否兼容。

## 6. 常见坑与经验

- **binding 编号必须匹配 shader。** 编号错了不是编译错误，往往是运行结果错误。
- **stage flags 要覆盖实际访问阶段。** 片段 shader 使用却只声明 VertexStage 会出问题。
- **空资源只适合 layout。** 含空 buffer/texture/sampler 的 SRB 不应用于实际 `setShaderResources()`。
- **layout-compatible 不等于资源相同。** 它只比较 binding、stage、type 等布局信息。
- **数组 binding 每个元素都要有效。** 某些后端要求描述符数组所有元素都有真实资源。
- **storage 资源需要正确 usage flag。** buffer 要有 `StorageBuffer`，texture 要有 `UsedWithLoadStore`。
- **dynamic offset 要按 binding 提供。** 使用动态 uniform 时，command buffer 设置的 offset 必须对齐且对应正确 binding。

## 7. 知识点覆盖

- shader binding 编号、stage visibility 和资源类型
- uniform buffer、sampled texture、独立 texture/sampler
- storage image、storage buffer 与 compute 工作流
- layout-only binding 与实际资源 binding
- layout compatibility 与 pipeline/SRB 复用
