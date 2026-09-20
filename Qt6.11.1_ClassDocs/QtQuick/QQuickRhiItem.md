# QQuickRhiItem
> Qt 6.11.1 · Qt Quick · 来自 `QQuickRhiItem`

## 作用定位
`QQuickRhiItem` 是在 Qt Quick 场景中嵌入自定义 QRhi 渲染的可视项。它把绘制生命周期交给配套的 `QQuickRhiItemRenderer`，比直接插入平台专属图形命令更符合 Qt 6 的后端无关渲染模型。

## API 速查
| API | 是做什么的 |
|---|---|
| `createRenderer()` | 必须重实现，创建渲染器。|
| `setColorBufferFormat()` | 选择离屏颜色纹理格式。|
| `setDepthStencilBuffer()` | 请求深度模板附件。|
| `setAutoRenderTarget()` | 控制是否自动创建内部目标。|
| `setFixedColorBufferWidth/Height()` | 固定渲染缓冲尺寸。|
| `setMirrorVertically()` | 调整输出纹理的垂直方向。|
| `setSampleCount()` | 请求多重采样。|
| `setTextureProvider()` | 暴露输出纹理给 QML/Scene Graph。|

## 使用场景
实现一块 CAD 预览、粒子图或专用图表：`QQuickRhiItem` 负责 Qt Quick 项属性和尺寸，renderer 负责 GPU 资源与渲染通道。

## 常见坑与经验
- item 在 GUI 线程，renderer 生命周期及 `render()` 通常在渲染线程；不要共享未同步的容器。
- 改变尺寸、MSAA 或颜色格式会导致资源重建，应避免在动画中反复切换。
- 这是 QRhi API，不能把 OpenGL 特定调用混进来。

## 知识点覆盖
自定义 GPU 绘制、QRhi、纹理提供者、多重采样、渲染线程、资源重建。
