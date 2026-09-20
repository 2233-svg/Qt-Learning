# QRhiShaderResourceBindings

> Qt 6.11.1 · Qt GUI Private · 来自 `QRhiShaderResourceBindings`

## 1. 先建立直觉

`QRhiShaderResourceBindings` 是一组 `QRhiShaderResourceBinding` 的集合。它既可以作为 pipeline 创建时的资源布局，也可以作为 draw/dispatch 时真正绑定的资源集合。一个 pipeline 不关心你这次具体用哪张纹理，但它必须知道 binding 0 是 uniform、binding 1 是 sampled texture、哪些 shader stage 能访问。

RHI 允许用 layout-compatible 的不同 SRB 互换：pipeline 创建时用 A，绘制时绑定 B，只要二者布局兼容。这是材质系统和 pipeline cache 的重要基础。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`Qt6::GuiPrivate`
- 继承自：`QRhiResource`
- 创建入口：`QRhi::newShaderResourceBindings()`
- 使用入口：`QRhiGraphicsPipeline::setShaderResourceBindings()`、`QRhiCommandBuffer::setShaderResources()`

`create()` 可能创建底层描述符集/布局相关对象，因此不要把它当普通 vector 操作。资源变化频繁时，设计可复用的 SRB cache 更重要。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `setBindings(list/iterators)` | 设置 binding 列表。 |
| `create()` | 创建底层资源绑定对象；失败返回 `false`。 |
| `bindingCount()` | 返回 binding 数量。 |
| `bindingAt(index)` | 读取指定 binding。 |
| `cbeginBindings()` / `cendBindings()` | 遍历 binding 列表。 |
| `isLayoutCompatible(other)` | 判断两个 SRB 是否可在同一 pipeline layout 下互换。 |
| `serializedLayoutDescription()` | 返回布局签名，用作内存中的 cache key。 |
| `resourceType()` | 返回 `QRhiResource::ShaderResourceBindings`。 |

## 4. 关键用法

### 创建材质 SRB

```cpp
QRhiShaderResourceBindings *srb = rhi->newShaderResourceBindings();
srb->setBindings({
    QRhiShaderResourceBinding::uniformBuffer(0, QRhiShaderResourceBinding::VertexStage, ubuf),
    QRhiShaderResourceBinding::sampledTexture(1, QRhiShaderResourceBinding::FragmentStage, tex, sampler)
});
srb->create();
```

这个 SRB 可被 pipeline 用作 layout，也可在 command buffer 中作为实际资源绑定。

### layout-compatible 替换

```cpp
if (pipelineLayoutSrb->isLayoutCompatible(materialSrb))
    cb->setShaderResources(materialSrb);
```

只要 binding 数量、顺序、编号、stage 和资源类型兼容，具体 buffer/texture 可以不同。

## 5. 使用场景

- pipeline 的资源 layout 描述。
- 每个材质/对象的实际资源绑定。
- 多 draw 之间切换 uniform、texture、sampler。
- compute dispatch 绑定 storage buffer/image。
- pipeline/SRB cache 中做 layout 签名比较。

## 6. 常见坑与经验

- **创建后再比较 layout。** `isLayoutCompatible()` 依赖 create 后的底层布局数据。
- **binding 顺序也要匹配。** 不只是 binding 编号一样，数量和顺序也影响兼容性。
- **serialized layout 不能持久化。** 只在所属 RHI 生命周期内用于内存比较。
- **空资源 SRB 不能用于实际绑定。** 它适合 pipeline layout，不适合 `setShaderResources()`。
- **SRB 改了要重新 create。** 改 binding 列表后旧底层资源不再代表新布局。
- **频繁创建会有成本。** 材质系统应缓存常用 layout 和资源组合。

## 7. 知识点覆盖

- SRB 集合与单个 binding 的关系
- pipeline layout 与实际资源绑定的分离
- layout compatibility、serialized layout 和 cache
- graphics/compute pipeline 的资源绑定流程
- 描述符/绑定对象创建成本与复用策略
