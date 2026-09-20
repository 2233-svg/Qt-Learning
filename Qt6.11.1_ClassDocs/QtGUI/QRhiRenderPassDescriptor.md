# QRhiRenderPassDescriptor

> Qt 6.11.1 · Qt GUI Private · 来自 `QRhiRenderPassDescriptor`

## 1. 先建立直觉

`QRhiRenderPassDescriptor` 描述 render pass 的附件格式/布局等与 pipeline 兼容性相关的信息。`QRhiGraphicsPipeline` 创建时需要它，因为现代图形 API 通常要求 pipeline 知道将要渲染到什么样的 render pass。

它不是 render target 本身，也不保存颜色/深度资源。它更像“这类 render target 的 pass 形状签名”。如果两个 descriptor 兼容，同一个 graphics pipeline 就可以复用到它们上面。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`Qt6::GuiPrivate`
- 继承自：`QRhiResource`
- 获取来源：通常来自 `QRhiRenderTarget::renderPassDescriptor()`
- 使用入口：`QRhiGraphicsPipeline::setRenderPassDescriptor()`

descriptor 的具体内容是后端相关的，所以 API 只暴露兼容性测试、克隆、序列化格式和 native handles。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `isCompatible(other)` | 判断两个 render pass descriptor 是否可被同一 graphics pipeline 兼容使用。 |
| `serializedFormat()` | 返回可比较的不透明格式签名，用于缓存键。 |
| `newCompatibleRenderPassDescriptor()` | 克隆一个兼容 descriptor，调用方获得所有权。 |
| `nativeHandles()` | 获取后端原生 render pass 句柄，可能为空。 |
| `resourceType()` | 返回 `QRhiResource::RenderPassDescriptor`。 |

## 4. 关键用法

### pipeline 缓存中检查 render pass 变化

```cpp
QRhiRenderPassDescriptor *rp = rt->renderPassDescriptor();
if (!pipeline || rp->serializedFormat() != cachedRenderPassFormat) {
    pipeline->setRenderPassDescriptor(rp);
    cachedRenderPassFormat = rp->serializedFormat();
    pipeline->create();
}
```

不要只比较 descriptor 指针。窗口 resize、swapchain 重建、离屏目标替换后，指针可能变化；也可能不同对象仍然兼容。

### 克隆保存兼容信息

```cpp
std::unique_ptr<QRhiRenderPassDescriptor> saved(
    rt->renderPassDescriptor()->newCompatibleRenderPassDescriptor());
```

当 render target 生命周期短于 pipeline cache 时，克隆 descriptor 可以让 cache 仍然保留创建 pipeline 所需的兼容信息。

## 5. 使用场景

- graphics pipeline 创建与缓存。
- swapchain resize 或 render target 替换后的 pipeline 兼容性判断。
- 可复用渲染组件接入外部提供的 render target。
- Vulkan/Metal/D3D 后端 native render pass 互操作。

## 6. 常见坑与经验

- **它不是附件资源。** 颜色/深度 texture 或 render buffer 在 render target 中。
- **兼容性不等于完全相同对象。** 使用 `isCompatible()` 或 `serializedFormat()` 做缓存判断。
- **serialized format 只在所属 RHI 生命周期内比较。** 不要跨进程、跨后端、跨 RHI 实例持久化。
- **pipeline 依赖 descriptor。** render pass 格式变化后旧 pipeline 可能不再可用。
- **native handles 后端相关。** 不能写成跨后端必有逻辑。

## 7. 知识点覆盖

- render pass descriptor 与 render target 的分工
- graphics pipeline render pass 兼容性
- pipeline cache 键设计
- descriptor 克隆、序列化签名和 native handle
- 后端相关 render pass 模型的抽象边界
