# QRhiResource

> Qt 6.11.1 · Qt GUI Private · 来自 `QRhiResource`

## 1. 先建立直觉

`QRhiResource` 是 RHI 资源的共同基类。buffer、texture、sampler、render target、pipeline、swapchain、command buffer 等都属于它的派生类型。它统一提供所属 `QRhi`、资源类型、调试名称、全局 id、销毁和延迟删除等基础能力。

RHI 资源有两层生命周期：C++ 对象生命周期，以及底层 native GPU 资源生命周期。`destroy()` 释放或安排释放 native 资源，但对象本身还可以继续存在并重新 `create()`；析构则会把对象一起销毁。帧录制期间还被命令引用的资源不能立刻消失，`deleteLater()` 就是为这个边界服务的。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`Qt6::GuiPrivate`
- API 层级：Qt GUI 私有 API
- 派生类：`QRhiBuffer`、`QRhiTexture`、`QRhiSampler`、`QRhiRenderTarget`、`QRhiGraphicsPipeline` 等
- 所属关系：每个资源属于创建它的 `QRhi`

`QRhiResource` 不是 `QObject`。`deleteLater()` 的含义也不是 QObject 事件循环延迟删除，而是 RHI 帧生命周期感知的安全删除。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `Type` | 标识资源类型，如 Buffer、Texture、Sampler、GraphicsPipeline、CommandBuffer。 |
| `resourceType()` | 返回具体资源类型，便于调试或资源管理。 |
| `rhi()` | 返回创建该资源的 `QRhi`；若 RHI 已销毁可能为 `nullptr`。 |
| `destroy()` | 释放或安排释放底层 native 图形资源；对象可稍后重新创建。 |
| `deleteLater()` | 在当前帧结束后安全删除资源对象；帧外调用近似立即删除。 |
| `setName()` / `name()` | 设置调试名称，可在 RenderDoc、Xcode 等工具中显示。 |
| `globalResourceId()` | 返回全局唯一资源 id，主要用于内部跟踪和诊断。 |

## 4. 关键用法

### 帧内临时资源安全释放

```cpp
rhi->beginFrame(swapChain);

QRhiBuffer *scratch = rhi->newBuffer(QRhiBuffer::Immutable,
                                     QRhiBuffer::VertexBuffer,
                                     256);
scratch->create();
scratch->deleteLater();

// 本帧命令仍可引用 scratch

rhi->endFrame(swapChain);
```

`deleteLater()` 保证资源对象不会在当前帧命令提交前消失。底层 native 对象也会按后端策略延迟到 GPU 安全时释放。

### 资源重建

```cpp
texture->destroy();
texture->setPixelSize(newSize);
texture->create();
```

`destroy()` 后对象仍然存在，适合窗口大小变化、格式变化、swapchain 重建时复用 C++ 资源包装对象。

### 调试命名

```cpp
vertexBuffer->setName("mesh.vertices");
diffuseTexture->setName("material.diffuse");
```

开启 debug markers 且后端支持时，名字会传给底层图形 API，外部 GPU 调试工具里更容易定位资源。

## 5. 使用场景

- 统一管理 RHI 资源生命周期。
- 在资源缓存中注册 `QRhi` cleanup callback，并销毁派生资源。
- 帧内创建临时 buffer/texture 后安全释放。
- swapchain 或设备丢失后批量重建资源。
- 为 GPU 调试工具命名资源。

## 6. 常见坑与经验

- **`deleteLater()` 不是 QObject 语义。** 它按 RHI 帧录制状态工作，不依赖事件循环。
- **`destroy()` 不等于 `delete`。** 它释放 native 资源，对象仍可重新 `create()`。
- **当前帧引用的资源不要立刻删。** 命令还没提交前销毁对象会破坏录制命令的引用。
- **资源不能跨 `QRhi` 混用。** buffer、texture、pipeline 都绑定创建它的 RHI。
- **调试名不是功能逻辑。** 后端可能忽略名称，应用逻辑不能依赖它。
- **`rhi()` 可能为 null。** 所属 RHI 已销毁后，不要再尝试访问 native 资源。

## 7. 知识点覆盖

- RHI 资源的统一基类和资源类型枚举
- C++ 包装对象与 native GPU 资源的双层生命周期
- `destroy()`、析构、`deleteLater()` 的区别
- 帧内引用、延迟释放和 GPU 安全回收
- 调试名称、全局资源 id 和资源缓存管理
