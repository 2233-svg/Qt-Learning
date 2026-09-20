# QNativeInterface::QSGVulkanTexture：把 VkImage 和布局状态接入 Qt Quick

> Qt 6.11.1 | `#include <QSGTexture>` | CMake: `Qt6::Quick` | Vulkan 后端

`QNativeInterface::QSGVulkanTexture` 用于把现有 `VkImage` 包装为 `QSGTexture`，或从 Quick 的纹理取得 `VkImage` 与当前 `VkImageLayout`。它让计算、视频或外部 Vulkan 渲染链输出能够在 QML 场景中直接显示。

Vulkan 的关键不只是 image handle，而是 layout 和同步。Qt 无法从裸 `VkImage` 猜到它目前是否适合采样，因此调用方必须明确交接状态。

## 从原生 image 创建 QSGTexture

```cpp
QSGTexture *texture = QNativeInterface::QSGVulkanTexture::fromNative(
    image,
    VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL,
    window,
    imageSize,
    QQuickWindow::TextureHasAlphaChannel);
```

`layout` 必须是 `VkImage` 的当前布局，不是下一帧希望转换到的布局。函数当前只适用于二维 RGBA 图像，scene graph 尚未初始化时返回 `nullptr`。

返回的 `QSGTexture` 不拥有 `VkImage`。销毁 wrapper 不会执行 `vkDestroyImage`；原生 image、allocation、fence/semaphore 和 queue ownership 的生命周期仍由调用方负责。它们必须覆盖 Qt Quick 读取纹理的整个时段。

## 反向获取 image 和 layout

```cpp
auto *native = texture->nativeInterface<
    QNativeInterface::QSGVulkanTexture>();
if (native) {
    VkImage image = native->nativeImage();
    VkImageLayout layout = native->nativeImageLayout();
    Q_UNUSED(image);
    Q_UNUSED(layout);
}
```

`nativeImageLayout()` 是互操作时必需的信息。拿到 image 后就自行发 barrier、却不和 Quick 的资源使用和渲染线程协作，会造成 layout mismatch 或数据竞争。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `fromNative(VkImage, VkImageLayout, window, size, options)` | 包装已有 Vulkan 图像 | layout 必须是当前布局；仅支持 2D RGBA |
| `nativeImage()` | 返回底层 `VkImage` | 不转移 image、memory 或同步对象的所有权 |
| `nativeImageLayout()` | 返回 image 的当前 layout | 与外部 barrier/采样协作时必须读取它 |
| `QSGTexture::nativeInterface<QSGVulkanTexture>()` | 查询 Vulkan 接口 | 非 Vulkan 后端或纹理不支持时返回空 |
| `TextureHasAlphaChannel` / `TextureHasMipmaps` | 指定可识别的纹理特性 | 不替代创建 image 时的真实 usage/format 设置 |

## 使用边界

- 不要把错误 layout 交给 `fromNative()`；这不是可由 Qt 自动修复的提示信息。
- GPU 完成顺序需要应用自行通过 Vulkan 同步原语与渲染阶段衔接。
- 仅在 Quick 实际使用 Vulkan scene graph 后端时走此接口，跨后端代码需有降级路径。
