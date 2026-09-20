# QQuickRenderTarget：把原生图形资源交给 Qt Quick 的描述对象

> Qt 6.11.1 | `#include <QQuickRenderTarget>` | CMake: `Qt6::Quick`

`QQuickRenderTarget` 是 `QQuickWindow::setRenderTarget()` 的参数类型。它把“哪个原生纹理、尺寸是多少、样本数、格式、当前状态如何”打包成 Qt Quick 可理解的目标描述，使 `QQuickRenderControl` 能把 scene graph 渲染进应用已有的 GPU 资源。

它尤其适合 Vulkan/D3D/Metal/OpenGL 引擎向 Qt Quick 提供一张可写纹理、XR runtime 提供 swapchain image、或已有 `QRhiTextureRenderTarget` 的场景。对象本身不创建、不销毁任何原生 texture、image 或 render target；资源的生命期、同步与状态转换始终由调用方负责。

## 选择与后端匹配的工厂

原生资源必须使用对应后端的工厂函数：

```cpp
QQuickRenderTarget target =
    QQuickRenderTarget::fromD3D12Texture(texture,
                                          D3D12_RESOURCE_STATE_RENDER_TARGET,
                                          DXGI_FORMAT_R8G8B8A8_UNORM,
                                          QSize(1920, 1080));
quickWindow->setRenderTarget(target);
```

OpenGL 使用 `fromOpenGLTexture()` 或 `fromOpenGLRenderBuffer()`；D3D11/12 使用相应 `fromD3D*Texture()`；Metal 使用 `fromMetalTexture()`；Vulkan 使用 `fromVulkanImage()`；应用已在 QRhi 层构建目标时使用 `fromRhiRenderTarget()`。`fromPaintDevice()` 只服务于兼容路径，不能把它和 GPU 目标的同步模型混为一谈。

所有 `pixelSize` 都是物理像素。普通重载默认某些格式，例如 Vulkan 简写重载假设 `VK_FORMAT_R8G8B8A8_UNORM`；实际格式并非默认值时应使用含 `format` 的重载。仅支持文档列出的 2D 纹理或 2D 纹理数组场景。

## 状态、样本数和所有权不能猜

D3D12 的 `resourceState` 必须准确反映资源当前的 `D3D12_RESOURCE_STATES`；Vulkan 的 `layout` 必须是传入 image 的真实当前布局。它们不是提示信息，填错可能触发验证层错误、渲染异常或设备问题。

`sampleCount` 为 `0` 或 `1` 时无 MSAA。未设置 `MultisampleResolve` 时，大于 `1` 意味着传入的资源本身就是 multisample 资源；设置 `Flag::MultisampleResolve` 后，传入的是普通纹理，Qt Quick 创建中间 MSAA 附件并在 render pass 结束时 resolve 到该纹理。这是已有单采样输出纹理时开启 MSAA 的推荐方式。

即使复制、赋值 `QQuickRenderTarget`，底层资源也没有被复制或托管。窗口、render control 和 GPU 尚可能使用该目标时，原生资源必须保持有效；先销毁资源再让 Qt Quick 绘制是未定义的集成顺序。

## DPI、镜像与深度附件

`devicePixelRatio` 默认 `1.0`，供没有真实窗口的离屏目标把逻辑尺寸映射为物理像素。若 `QQuickRenderControl::renderWindow()` 被重写并返回有效窗口，则此值会被真实窗口的 DPI 覆盖。

`setMirrorVertically(true)` 让 Qt Quick 绘制目标时做垂直镜像，常用于纠正第三方坐标原点约定。它不改变源纹理数据，也不应在软件后端使用。

Qt 6.8 起可通过 `setDepthTexture()` 指定一个外部 `QRhiTexture` 作为深度或深度模板附件，例如把 OpenXR 交换链中的深度纹理提交给 runtime。该对象不接管所有权，只接受非 multisample 的 2D texture 或 texture array；若请求的 MSAA 组合不被后端支持，Qt Quick 会警告且不会写入该纹理。`fromRhiRenderTarget()`、`fromPaintDevice()` 和 `fromOpenGLRenderBuffer()` 路径会忽略该请求。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `QQuickRenderTarget()` / `isNull()` | 创建或判断空目标 | 空目标没有引用任何原生资源 |
| `fromOpenGLTexture(...)` | 引用 OpenGL 2D texture 或 texture array | 名称必须在 Qt Quick 所用上下文中有效 |
| `fromOpenGLRenderBuffer(...)` | 引用 OpenGL renderbuffer | 不能配合 `setDepthTexture()` 自定义深度纹理 |
| `fromD3D11Texture(...)` | 引用 D3D11 texture | `format` 应为 Qt 图形基础设施支持的 `DXGI_FORMAT` |
| `fromD3D12Texture(texture, state, ...)` | 引用 D3D12 texture | `state` 必须是资源此刻的真实 `D3D12_RESOURCE_STATES` 位掩码 |
| `fromMetalTexture(...)` | 引用 `MTLTexture` | 资源和像素格式必须在 Qt Quick 绘制期间存活且兼容 |
| `fromVulkanImage(image, layout, ...)` | 引用 Vulkan image | 必须提供真实当前 `VkImageLayout`；格式不默认时显式传入 |
| `fromRhiRenderTarget(target)` | 引用现有 `QRhiRenderTarget` | 不取得 `target` 或其底层资源的所有权 |
| `fromPaintDevice(device)` | 从 `QPaintDevice` 创建目标 | 面向兼容路径，不等同于原生 GPU 目标 |
| `Flag::MultisampleResolve` | 让 Qt 为普通输出纹理创建中间 MSAA 附件并 resolve | Qt 6.8 起；`sampleCount == 1` 时无效果 |
| `setDevicePixelRatio(ratio)` / `devicePixelRatio()` | 指定离屏目标的物理像素比例 | 真实窗口由 `renderWindow()` 返回时，此值会被忽略 |
| `setMirrorVertically(enable)` / `mirrorVertically()` | 使绘制结果垂直镜像 | 不改变资源内容；软件后端不要使用 |
| `setDepthTexture(texture)` / `depthTexture()` | 请求使用外部深度或深度模板纹理 | Qt 6.8 起；不接管所有权，且仅部分工厂路径生效 |
| `operator==` / `operator!=` | 比较目标描述 | 比较的是封装状态，不表示原生资源内容相同 |
