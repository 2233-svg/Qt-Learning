# QQuickRhiItem：将跨后端自定义渲染包装成 QML Item

> Qt 6.11.1 | `#include <QQuickRhiItem>` | CMake: `Qt6::Quick`

`QQuickRhiItem` 是自定义 GPU 渲染嵌入 Qt Quick 的抽象 item。它以 QRhi 为基础，因此同一渲染器可以运行在 Vulkan、Metal、Direct3D 11/12、OpenGL/OpenGL ES 上；它是仅能走 OpenGL 的 `QQuickFramebufferObject` 的现代替代品。

实际用途包括在 QML 中显示体渲染、频谱仪、地图或游戏画面，把自定义渲染的结果继续交给 `ShaderEffect` 采样，或在标准 Qt Quick UI 内保留一块跨平台 3D 画布。软件 scene graph adaptation 下该类不能工作。

## 需要实现 Item 和 Renderer 两个类

`QQuickRhiItem` 只放 GUI/QML 状态，真正的 GPU 资源和命令属于 `QQuickRhiItemRenderer`。最小结构如下：

```cpp
class MeterItem final : public QQuickRhiItem
{
    Q_OBJECT
    Q_PROPERTY(float level READ level WRITE setLevel NOTIFY levelChanged)
public:
    QQuickRhiItemRenderer *createRenderer() override;
    float level() const { return m_level; }
    void setLevel(float value) { m_level = value; emit levelChanged(); update(); }
private:
    float m_level = 0.0f;
};
```

`createRenderer()` 在渲染线程、GUI 线程被阻塞时调用，返回一个新 renderer。Renderer 的 `synchronize(item)` 也处在这一安全交接点：把 `level` 等 GUI 状态复制进 renderer 的私有成员。两端平时不应共同读写同一个变量；排队信号或事件也可传递数据，但不能绕过 GPU 资源的线程边界。

所有 `QQuickRhiItem` 使用所属 `QQuickWindow` 的同一个 `QRhi`、设备和后端。要选择图形 API，应在 scene graph 初始化前配置窗口；初始化后不能改，且同一窗口中的 RHI item 必须使用同一后端。

## 颜色缓冲与采样策略

item 自动维护用于最终合成的颜色 texture。默认大小为 item 的逻辑尺寸乘有效设备像素比，尺寸变化会重建底层资源。把 `fixedColorBufferWidth` 和 `fixedColorBufferHeight` 都设置为非零，可固定为像素尺寸：大于显示像素是 supersampling，小于显示像素是降分辨率渲染再放大。固定缓冲不会改变 item 本身几何尺寸。

`sampleCount` 默认 `1`。常用请求是 `1`、`4`、`8`，但可用值仍要以 `QRhi::supportedSampleCounts()` 为准。动态切换样本数或 `colorBufferFormat` 会使旧 graphics pipeline 的 render-pass 兼容性失效；Qt 会重建其附件并再次调用 renderer 的 `initialize()`，而 renderer 必须丢弃并重建依赖旧格式/样本数的 pipeline。

`TextureFormat` 可选 `RGBA8`、`RGBA16F`、`RGBA32F`、`RGB10A2`。只应选择运行时由 `QRhi::isTextureFormatSupported()` 报告支持的格式。

## 合成结果与自动目标

`alphaBlending` 默认 false，是对不透明内容的性能优化。renderer 输出任何半透明像素时必须设为 true，且 Qt Quick 要求预乘 alpha：清屏 alpha 为 `0.5` 时，RGB 也应先乘 `0.5`。否则与周围 QML 内容混合会出现暗边或错误颜色。

`mirrorVertically` 只翻转最终纹理四边形的 UV，不改变离屏 color buffer 中的像素，也不改变 renderer 内部的投影或坐标系。

默认自动模式会创建匹配颜色附件的 depth-stencil buffer 和 `QRhiTextureRenderTarget`。派生 item 可以在构造期用 `setAutoRenderTarget(false)` 关闭它，以处理多个 color attachment、特殊深度资源或自定义 resolve；这之后 renderer 必须自行维护深度缓冲和 render target，且附件尺寸、样本数必须始终跟随 item 的颜色缓冲。

该 item 是 texture provider，可被 `ShaderEffect` 等 Qt Quick 内容消费；它不等于可从任意线程安全读取的图像。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `createRenderer()` | 创建对应的 `QQuickRhiItemRenderer` | 纯虚；渲染线程调用且 GUI 线程被阻塞 |
| `sampleCount` / `setSampleCount()` | 控制 MSAA 样本数 | 默认 `1`；改动后旧 pipeline 不可继续使用 |
| `colorBufferFormat` / `setColorBufferFormat()` | 设置离屏颜色纹理格式 | 仅可用 `QRhi::isTextureFormatSupported()` 验证的格式 |
| `TextureFormat::{RGBA8, RGBA16F, RGBA32F, RGB10A2}` | 可选颜色格式 | `RGBA8` 默认；高精度格式可能不受当前后端支持 |
| `fixedColorBufferWidth` / `fixedColorBufferHeight` | 指定固定的物理像素缓冲尺寸 | 两者为 `0` 时跟随 item 与 DPI；不会改变 item 几何 |
| `effectiveColorBufferSize` | 读取实际颜色缓冲的像素尺寸 | 面向 GUI/QML；renderer 应从 `renderTarget()` 查询 |
| `alphaBlending` / `setAlphaBlending()` | 是否为最终纹理 quad 启用混合 | 半透明输出要启用，并使用预乘 alpha |
| `mirrorVertically` / `setMirrorVertically()` | 翻转最终合成时的纹理 UV | 只影响显示，不改变渲染出的 color buffer |
| `isTextureProvider()` / `textureProvider()` | 将结果暴露为 Quick 纹理源 | 可供 `ShaderEffect` 等消费，遵守 scene graph 线程规则 |
| `isAutoRenderTargetEnabled()` | 查询自动 depth/render target 管理开关 | 默认 true |
| `setAutoRenderTarget(false)` | 改为自行创建深度附件和 render target | 应在派生类构造期调用；之后 `renderTarget()` 与 `depthStencilBuffer()` 为 `nullptr` |
| `sampleCountChanged()` 等属性信号 | 通知 QML/GUI 侧属性变化 | 不替代 renderer 的 `synchronize()` 状态交接 |
