# QQuickGraphicsDevice：让 Qt Quick 复用已有的图形设备或适配器

> Qt 6.11.1 | `#include <QQuickGraphicsDevice>` | CMake: `Qt6::Quick`

`QQuickGraphicsDevice` 是一个可复制的描述值，用来告诉 `QQuickWindow` 选择或复用已有的 OpenGL、Direct3D、Metal、Vulkan 或 QRhi 图形对象。它解决嵌入式渲染、OpenXR 和多窗口协作中的设备一致性问题：让 Qt Quick 使用应用已经选定的 adapter、physical device、context 或 queue。

它通常**引用**原生对象而不是拥有它们。传入的 context、device、queue、RHI 或 adapter 必须至少在 scene graph 初始化所需期间保持有效。

## 按后端选择工厂函数

```cpp
QQuickGraphicsDevice device =
    QQuickGraphicsDevice::fromPhysicalDevice(vkPhysicalDevice);
window.setGraphicsDevice(device);
```

- OpenGL：`fromOpenGLContext(QOpenGLContext *)`。
- D3D：`fromAdapter(luidLow, luidHigh, featureLevel)`，或 `fromDeviceAndContext(device, context)`；D3D12 中 context 可为空。
- Metal：`fromDeviceAndCommandQueue(MTLDevice *, MTLCommandQueue *)`。
- Vulkan：`fromPhysicalDevice()` 只指定物理设备，或 `fromDeviceObjects()` 复用 logical device 和队列族。
- Qt RHI：`fromRhi(QRhi *)` 自 Qt 6.6 起，`fromRhiAdapter(QRhiAdapter *)` 自 Qt 6.10 起。

设置时机与 graphics configuration 相同：必须早于对应窗口的 scene graph 初始化。默认构造对象 `isNull()` 为 true，表示没有指定任何原生对象，Qt 将按默认策略创建。

## 共享设备不是自动线程安全

把一个 `QRhi` 或原生 graphics context 提供给多个 `QQuickWindow`，只是让它们指向相同资源基础，不代表 Qt 会替应用修复线程、pixel format、queue 或 surface 兼容性。确认底层 API 允许这种共享，再让窗口使用同一 `QQuickGraphicsDevice`。

这类 API 适合确有外部引擎/XR 约束的程序；普通 QML 应用通常无需指定，让 Qt Quick 自选设备更简单稳妥。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `isNull()` | 判断是否为默认、未引用原生对象的描述 | true 时由 Qt 自行选择设备 |
| `fromOpenGLContext()` | 引用一个既有 OpenGL context | 需遵守 context share group 与线程规则 |
| `fromAdapter()` | 指定 D3D adapter LUID 和可选 feature level | 适合 D3D11/12 与 OpenXR 场景 |
| `fromDeviceAndContext()` | 引用 D3D11 device/context 或 D3D12 device | D3D12 的 context 参数可为 null |
| `fromDeviceAndCommandQueue()` | 引用 Metal device 与 command queue | 仅 Apple/Metal 后端 |
| `fromPhysicalDevice()` | 让 Vulkan 选择给定 physical device | 常用于与外部 Vulkan/XR 设备一致 |
| `fromDeviceObjects()` | 复用 Vulkan physical device、device 与 queue | 调用方保证所有对象和队列索引有效 |
| `fromRhi()` / `fromRhiAdapter()` | 引用既有 QRhi 或 adapter | 分别自 Qt 6.6 / 6.10 起；共享前确认兼容性 |
| `QQuickWindow::setGraphicsDevice()` | 给窗口安装设备描述 | 必须在 scene graph 初始化前调用 |

## 使用边界

- 传入原生对象后仍由其原本所有者销毁，`QQuickGraphicsDevice` 不接管。
- Device 描述匹配的运行时后端才会有意义；不要把 Vulkan 描述交给被强制为 OpenGL 的窗口。
- 多窗口共享时，线程、surface 格式和设备 lifecycle 的约束来自底层图形 API，而不是该值类型。
