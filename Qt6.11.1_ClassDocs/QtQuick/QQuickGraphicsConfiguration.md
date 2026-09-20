# QQuickGraphicsConfiguration
> Qt 6.11.1 · Qt Quick · 来自 `QQuickGraphicsConfiguration`

## 作用定位
`QQuickGraphicsConfiguration` 是配置 Qt Quick 图形后端行为的值类型，例如调试层、首选适配器、纹理图集或深度模板缓冲策略。它不创建图形设备，而是把窗口创建 Scene Graph 前的策略集中起来。

## API 速查
| API | 是做什么的 |
|---|---|
| `setDebugLayer()` | 请求底层图形 API 调试层。|
| `setDebugMarkers()` | 让 Qt Quick 写入便于 GPU 调试器识别的标记。|
| `setPreferredAdapter()` | 选择默认/高性能/低功耗图形适配器偏好。|
| `setDepthBufferFor2D()` | 为 2D 场景请求深度缓冲。|
| `setStencilBuffer()` | 为裁剪等功能请求模板缓冲。|
| `setTextureAtlasEnabled()` | 控制小纹理图集优化。|
| `setAutomaticPipelineCache()` | 控制管线缓存使用。|

## 使用场景
在 `QQuickWindow` 创建并初始化 Scene Graph 前调用 `setGraphicsConfiguration()`。GPU 调试时开启调试标记；混合 3D、自定义深度操作时才考虑深度缓冲。

## 常见坑与经验
- 配置必须足够早设置；窗口已经创建图形资源后再修改通常无效。
- 调试层和标记会损失性能，只用于开发诊断。
- 强制关闭纹理图集会改变内存与批处理特性，先用 RenderDoc 或性能数据证明需要。

## 知识点覆盖
RHI、图形适配器、GPU 调试、纹理图集、深度/模板缓冲、初始化时机。
