# Qt QRhiWidget 深入笔记

> 适用版本：Qt 6.11.1
> 头文件：`#include <QRhiWidget>`
> 所属模块：`Qt6::Widgets`
> 继承：`QWidget`

## 它解决什么问题

`QRhiWidget` 把 Qt RHI 的低层图形渲染嵌入 QWidget 界面。它适合在传统 Widgets 程序中放入一个 GPU 渲染区域，同时避免直接绑定到单一图形 API。根据平台和设置，它可以使用 OpenGL、Metal、Vulkan、Direct3D 11、Direct3D 12 或 Null 后端。

可以把它理解为跨后端版本的“GPU 视口控件”。它不是 `QPainter` 控件，也不是 Qt Quick 场景。你需要派生它，在 `initialize()` 中创建 QRhi 资源，在 `render()` 中录制渲染命令，在 `releaseResources()` 中释放 GPU 资源。

## 实际使用场景

- 在 QWidget 软件中嵌入实时 2D/3D 预览。
- 做 shader、材质、图像处理结果预览。
- 在 CAD、医学影像、可视化工具中显示 GPU 加速画面。
- 希望同一套渲染代码跨不同图形后端运行。
- 从 `QOpenGLWidget` 迁移到 QRhi 抽象层。

如果只是普通控件绘制、图标绘制或轻量自定义 UI，`paintEvent()` 加 `QPainter` 更简单。`QRhiWidget` 的成本在于你要自己管理 GPU 资源和渲染命令。

## 基本生命周期

派生类通常关注三个虚函数：

| 阶段 | 函数 | 该做什么 |
| --- | --- | --- |
| 资源准备 | `initialize(QRhiCommandBuffer *cb)` | 创建或重建 pipeline、buffer、texture、sampler 等 QRhi 资源。 |
| 每帧绘制 | `render(QRhiCommandBuffer *cb)` | 使用命令缓冲录制当前帧绘制命令。 |
| 资源释放 | `releaseResources()` | 释放自己持有的 QRhi 资源，并清空悬空指针。 |

`initialize()` 会在第一次渲染前调用，也会在渲染环境变化时再次调用。例如控件尺寸、采样数、颜色格式、RHI 后端、重新父子化、离屏抓图再回到屏幕等，都可能导致底层资源重建。凡是依赖 `QRhi`、渲染目标尺寸或格式的资源，都要准备好在 `initialize()` 中重建。

`render()` 前一定已经有一次匹配当前资源状态的 `initialize()`。动画或持续刷新通常在 `render()` 中再次调用 `update()`，Qt 会把重绘节奏限制在合适的提交节奏上。

## 渲染目标管理

默认 `autoRenderTarget` 为 true，控件自动管理颜色缓冲、MSAA 缓冲、深度模板缓冲和 render target。大多数派生类应该使用默认模式，然后在 `render()` 中通过 `renderTarget()` 取得目标。

只有在你非常清楚 QRhi attachment 生命周期，并且需要完全自定义渲染目标时，才考虑在派生类中调用 `setAutoRenderTarget(false)`。关闭后，自己创建的纹理、render buffer 和 render target 必须匹配当前尺寸、采样数和颜色格式，否则渲染失败很难排查。

受保护的 `rhi()`、`colorTexture()`、`msaaColorBuffer()`、`resolveTexture()`、`depthStencilBuffer()`、`renderTarget()` 只应在 `initialize()` 和 `render()` 这类受控阶段使用。不要把这些指针长期当成稳定资源保存；底层 RHI 资源可能因窗口和格式变化被替换。

## 属性与后端选择

`setApi()` 选择图形后端。一般应在控件开始渲染前设置；运行中切换会引发资源重建，派生类必须能释放并重建所有 QRhi 资源。后端不可用时可能触发 `renderFailed()`。

`sampleCount` 控制多重采样。修改它会影响颜色缓冲和渲染目标，通常导致重新初始化。

`colorBufferFormat` 控制颜色缓冲格式，例如 `RGBA8`、`RGBA16F`、`RGBA32F`、`RGB10A2`。高精度格式更适合 HDR 或科学可视化，但也更消耗带宽和显存。

`fixedColorBufferSize` 非空时，颜色缓冲使用固定像素尺寸，而不是随 widget 的设备像素尺寸变化。这适合固定分辨率渲染或性能控制，但需要接受缩放显示带来的清晰度变化。

`mirrorVertically` 用来处理最终图像垂直方向。不同图形 API 和纹理坐标约定可能导致上下方向差异，这个属性提供一个控件级调整。

## 抓图与信号

`grabFramebuffer()` 会渲染一帧并读回为 `QImage`。读回 GPU 内容通常是同步成本较高的操作，不适合每帧调用。失败时返回 null image。返回格式取决于颜色缓冲格式，但不会返回 premultiplied 格式。

`frameSubmitted()` 表示一帧已经提交；适合统计帧率或触发轻量状态更新。`renderFailed()` 表示渲染流程失败，常见原因包括后端不可用、资源创建失败、目标格式不匹配。

## 常见误区

- 不要在普通 `paintEvent()` 里混用 `QPainter` 当作主要渲染路径；`QRhiWidget` 的绘制入口是 `render()`。
- 不要长期缓存 `renderTarget()` 等受保护 getter 返回的资源指针。
- 不要假设 resize 后资源还有效；尺寸和格式变化都可能重建。
- 不要在 GUI 线程以外直接访问 QWidget 和渲染控件。
- 不要把 `grabFramebuffer()` 当成实时视频采集接口。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QRhiWidget(QWidget *parent = nullptr, Qt::WindowFlags f = {})` | 创建 RHI 渲染控件。 | 需要派生并实现渲染逻辑；遵守 QWidget 生命周期。 |
| 析构 | `~QRhiWidget()` | 销毁控件并释放内部渲染资源。 | 派生类应在 `releaseResources()` 中释放自己创建的 QRhi 资源。 |
| 后端枚举 | `enum class Api` | 表示 RHI 后端。 | 包括 `Null`、`OpenGL`、`Metal`、`Vulkan`、`Direct3D11`、`Direct3D12`。 |
| 格式枚举 | `enum class TextureFormat` | 表示颜色缓冲纹理格式。 | 高精度格式更耗资源，需确认后端支持。 |
| 后端 | `Api api() const` | 返回当前使用或请求的后端。 | 实际可用性受平台和图形驱动影响。 |
| 后端 | `void setApi(Api api)` | 设置希望使用的图形后端。 | 尽量在首次显示前设置；运行中切换要能处理资源重建。 |
| 调试 | `bool isDebugLayerEnabled() const` | 查询是否启用后端调试层。 | 调试层依赖平台支持，通常只在开发期启用。 |
| 调试 | `void setDebugLayerEnabled(bool enable)` | 启用或关闭图形后端调试层。 | 最好在 RHI 创建前设置，避免期望落空。 |
| 采样 | `int sampleCount() const` | 返回 MSAA 采样数。 | 会影响渲染目标配置。 |
| 采样 | `void setSampleCount(int samples)` | 设置 MSAA 采样数。 | 修改后通常需要重建相关资源。 |
| 颜色格式 | `TextureFormat colorBufferFormat() const` | 返回颜色缓冲格式。 | 影响 `grabFramebuffer()` 和渲染目标。 |
| 颜色格式 | `void setColorBufferFormat(TextureFormat format)` | 设置颜色缓冲格式。 | 高精度格式需考虑显存、带宽和后端支持。 |
| 固定尺寸 | `QSize fixedColorBufferSize() const` | 返回固定颜色缓冲尺寸。 | 空尺寸表示随 widget 像素尺寸变化。 |
| 固定尺寸 | `void setFixedColorBufferSize(QSize pixelSize)` | 设置固定颜色缓冲尺寸。 | 适合性能控制；可能产生缩放显示。 |
| 固定尺寸 | `void setFixedColorBufferSize(int w, int h)` | 以宽高设置固定颜色缓冲尺寸。 | 是 `QSize` 重载的便捷形式。 |
| 翻转 | `bool isMirrorVerticallyEnabled() const` | 查询是否垂直镜像最终图像。 | 用于处理坐标约定差异。 |
| 翻转 | `void setMirrorVertically(bool enabled)` | 设置是否垂直镜像。 | 修改会影响最终呈现方向。 |
| 抓图 | `QImage grabFramebuffer() const` | 渲染并读回当前帧图像。 | 同步读回成本高；失败返回 null image。 |
| 自动目标 | `bool isAutoRenderTargetEnabled() const` | 查询是否由控件自动管理 render target。 | 受保护；默认模式适合大多数用法。 |
| 自动目标 | `void setAutoRenderTarget(bool enabled)` | 设置是否自动管理 render target。 | 关闭后必须自己创建匹配的目标资源。 |
| 初始化 | `void initialize(QRhiCommandBuffer *cb)` | 创建或重建 GPU 资源。 | 首帧前和资源条件变化后会再次调用。 |
| 渲染 | `void render(QRhiCommandBuffer *cb)` | 录制当前帧渲染命令。 | 动画可在这里调用 `update()` 请求下一帧。 |
| 释放 | `void releaseResources()` | 释放派生类持有的 QRhi 资源。 | 资源失效、控件销毁或后端变化时会用到。 |
| 资源访问 | `QRhi *rhi() const` | 返回当前 RHI 对象。 | 只在初始化和渲染阶段可靠使用。 |
| 资源访问 | `QRhiTexture *colorTexture() const` | 返回颜色纹理。 | 自动目标模式下由控件管理，不要删除。 |
| 资源访问 | `QRhiRenderBuffer *msaaColorBuffer() const` | 返回 MSAA 颜色缓冲。 | 仅在使用 MSAA 时有意义。 |
| 资源访问 | `QRhiTexture *resolveTexture() const` | 返回 MSAA resolve 后的纹理。 | 指针随资源重建而变化。 |
| 资源访问 | `QRhiRenderBuffer *depthStencilBuffer() const` | 返回深度模板缓冲。 | 自动目标模式下由控件管理。 |
| 资源访问 | `QRhiRenderTarget *renderTarget() const` | 返回当前渲染目标。 | 在 `render()` 中用于开始 render pass。 |
| 信号 | `void frameSubmitted()` | 一帧提交后发出。 | 适合统计或轻量通知，不适合做重工作。 |
| 信号 | `void renderFailed()` | 渲染失败时发出。 | 应检查后端、资源格式和目标配置。 |
| 信号 | `sampleCountChanged(int)` | 采样数变化通知。 | 修改采样数后资源可能重建。 |
| 信号 | `colorBufferFormatChanged(TextureFormat)` | 颜色格式变化通知。 | 与渲染目标配置相关。 |
| 信号 | `fixedColorBufferSizeChanged(const QSize &)` | 固定缓冲尺寸变化通知。 | UI 可用它同步设置状态。 |
| 信号 | `mirrorVerticallyChanged(bool)` | 垂直镜像状态变化通知。 | 影响最终呈现方向。 |

## 一句话总结

`QRhiWidget` 是 QWidget 世界里的跨后端 GPU 渲染视口：便利之处是能嵌入 Widgets，代价是你必须认真管理 QRhi 资源生命周期。
