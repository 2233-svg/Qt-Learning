# QQuickGraphicsConfiguration：在 scene graph 初始化前确定底层图形策略

> Qt 6.11.1 | `#include <QQuickGraphicsConfiguration>` | CMake: `Qt6::Quick`

`QQuickGraphicsConfiguration` 是传给 `QQuickWindow` 的低层图形初始化配置。它解决的不是每帧渲染设置，而是窗口首次创建 scene graph、图形 instance/device 和 pipeline cache 时的策略选择：调试层、Vulkan 扩展、2D 深度缓冲、软件设备偏好、时间戳和缓存文件。

## 配置必须早于首次初始化

```cpp
QQuickGraphicsConfiguration config;
config.setDebugLayer(true);
config.setDebugMarkers(true);

QQuickView view;
view.setGraphicsConfiguration(config);
view.setSource(u"qrc:/Main.qml"_s);
view.show();
```

对屏幕窗口，必须在 `show()` 前调用 `setGraphicsConfiguration()`；对 `QQuickRenderControl`，必须在 `initialize()` 前最终确定。scene graph 已初始化后再改 configuration 不会重建既有 device，也不应期待新设置生效。

## 主要配置维度

- `setDeviceExtensions()` 与 `preferredInstanceExtensions()`：外部 Vulkan/XR 系统参与 instance 创建时，补充或查询 Qt Quick 所需扩展。
- `setDepthBufferFor2D()`：让纯 2D scene graph 请求 depth buffer；只有确有自定义 3D/depth 需求才打开。
- `setDebugLayer()`、`setDebugMarkers()`、`setTimestamps()`：便于图形调试和性能分析，但可能带来额外开销；timestamps 自 Qt 6.6 起。
- `setPreferSoftwareDevice()`：偏向软件 renderer，用于兼容/诊断，不代表所有系统一定能提供。
- pipeline cache 读写：可缩短后续启动时着色器或 pipeline 创建，效果取决于运行时后端和驱动。

```cpp
config.setPipelineCacheLoadFile(cacheFile);
config.setPipelineCacheSaveFile(cacheFile);
config.setAutomaticPipelineCache(true);
```

缓存数据通常与设备和驱动版本绑定。Qt 会附加元数据，不匹配时静默忽略；不能把“有缓存文件”当作必然的性能收益或跨设备一致性的保证。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `QQuickWindow::setGraphicsConfiguration()` | 将配置应用到一个窗口 | 在首次 scene graph 初始化前调用 |
| `preferredInstanceExtensions()` | 返回 Qt Quick 偏好的 Vulkan instance 扩展 | 供应用自己创建 `QVulkanInstance` 时参考 |
| `setDeviceExtensions()` | 请求额外 device extensions | 只提供真正由所选后端支持且需要的扩展 |
| `setDepthBufferFor2D()` | 控制 2D 渲染是否请求 depth buffer | 增加资源需求，非默认的通用优化手段 |
| `setDebugLayer()` / `setDebugMarkers()` | 启用图形 API 调试层与标记 | 开发期工具，可能影响性能 |
| `setTimestamps()` | 请求 GPU 时间戳 | Qt 6.6 起；依赖后端和驱动能力 |
| `setPreferSoftwareDevice()` | 偏向选择软件图形设备 | 适合诊断/兼容，不保证强制成功 |
| pipeline cache setters | 指定读取、保存或自动管理 pipeline cache | 后端不支持时无效，驱动不匹配的缓存会被忽略 |

## 使用边界

- 这不是 `QQuickGraphicsDevice`：前者描述策略，后者引用一个既有图形设备。
- 用配置 API 替换环境变量时，仍需留意部署环境可能设置的 legacy 图形变量。
- 应用自行管理 Vulkan instance / XR 系统时，要协调 extension、instance、device 与窗口的完整创建链。
