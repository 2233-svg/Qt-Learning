# QQuickRhiItemRenderer：在 scene graph 线程实现 RHI 绘制

> Qt 6.11.1 | `#include <QQuickRhiItem>` | CMake: `Qt6::Quick`

`QQuickRhiItemRenderer` 是 `QQuickRhiItem` 的抽象渲染端。它把真正的 QRhi 资源创建、pipeline 配置和 command buffer 录制放在 scene graph 渲染线程，避免 QML/GUI 线程直接碰 GPU 对象。

它适合为 `QQuickRhiItem` 实现跨后端 2D/3D 绘制：renderer 从 item 接收已复制的业务状态，在离屏 color buffer 上绘制，随后 Qt Quick 自动把结果作为纹理合成进主场景。renderer 生命周期跟随 scene graph node；item 重新归属到另一 `QQuickWindow` 等情况会销毁旧 renderer 并创建新实例，因此不能把其地址当成长期业务对象。

## 三个回调分工

```cpp
class MeterRenderer final : public QQuickRhiItemRenderer
{
    void synchronize(QQuickRhiItem *item) override;
    void initialize(QRhiCommandBuffer *cb) override;
    void render(QRhiCommandBuffer *cb) override;
};
```

`synchronize(item)` 在渲染线程调用且 GUI 线程被阻塞，是从派生 item 复制 `Q_PROPERTY`、尺寸比例等状态的唯一常规交接点。不要把 item 成员缓存为可跨帧访问的共享状态。

`initialize(cb)` 在首次使用、颜色缓冲尺寸/格式/样本数变化、或 QRhi/底层纹理改变时调用。这里维护 renderer 自己创建的 buffer、shader resource binding、pipeline 等资源；这些资源在 renderer 析构时释放即可。传入的 `cb` 已在录制帧中但没有活跃 render pass，适合提交 resource update。

`render(cb)` 在 backing color buffer 需要更新时调用，同样处于录制帧且没有活跃 render pass。常规自动目标模式中，调用 `cb->beginPass(renderTarget(), ...)`、录制 draw、再 `endPass()`。`initialize()` 总会先于第一次 `render()` 调用。

## 自动目标和 MSAA 的返回值

默认 `QQuickRhiItem` 会自动创建 depth-stencil buffer 与 render target，此时 `renderTarget()`、`depthStencilBuffer()` 可用。若 item 关闭 `autoRenderTarget`，两者会返回空，renderer 的 `initialize()` 必须创建匹配尺寸和样本数的附件及 `QRhiTextureRenderTarget`。

无 MSAA 时 `colorTexture()` 返回最终颜色纹理，`msaaColorBuffer()` 和 `resolveTexture()` 为空。启用 MSAA 后则相反：`colorTexture()` 为空，向 `msaaColorBuffer()` 绘制，最终由 `resolveTexture()` 接收 resolve 结果。自动模式已正确连接这些附件；自管模式必须自己保证 render target 的 resolve 配置、pipeline 样本数和深度附件样本数一致。

`rhi()`、`colorTexture()`、`renderTarget()` 及相关资源 getter 只可在 `initialize()` 或 `render()` 内调用，不能在 `synchronize()`、GUI 线程或 renderer 析构后的路径使用。texture render target 的 `devicePixelRatio()` 总是 `1`；若着色器或投影需要屏幕 scale，在 `synchronize()` 中从 `item->window()->effectiveDevicePixelRatio()` 取值并复制。

## 如何请求下一帧

QML 或 GUI 线程的属性 setter 中调用 item 的 `update()`。renderer 回调内需要继续动画、异步结果到达时，则调用 renderer 自己的 `update()`。在 `render()` 每帧调用 renderer `update()` 会形成持续重绘，只有确实需要连续动画时才这样做。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `synchronize(QQuickRhiItem *item)` | 从 GUI item 拷贝渲染所需状态 | 纯虚；GUI 线程被阻塞时调用，不应保留不安全的共享读写 |
| `initialize(QRhiCommandBuffer *cb)` | 创建或重建 renderer 自有 GPU 资源 | 纯虚；尺寸、格式、样本数或 QRhi 改变都可能再次调用 |
| `render(QRhiCommandBuffer *cb)` | 向 item 的离屏目标录制绘制命令 | 纯虚；无活跃 render pass，通常自行 `beginPass()`/`endPass()` |
| `update()` | 从 renderer 请求后续更新 | 在 `render()` 中反复调用会导致连续渲染 |
| `rhi()` | 返回当前共享的 `QRhi` | 仅 `initialize()`/`render()` 中可用 |
| `colorTexture()` | 返回单采样时的颜色纹理 | 仅 `initialize()`/`render()`；MSAA 开启时为 `nullptr` |
| `msaaColorBuffer()` | 返回 MSAA 颜色 renderbuffer | 仅 MSAA 时有效；pipeline 样本数必须匹配 |
| `resolveTexture()` | 返回 MSAA resolve 后的单采样纹理 | 仅 MSAA 时有效；它不是 MSAA 绘制目标 |
| `depthStencilBuffer()` | 返回自动维护的深度/模板附件 | 仅自动 render target 模式有效 |
| `renderTarget()` | 返回应传给 `beginPass()` 的自动目标 | 仅自动模式有效；自管模式需自行建立目标 |
| 析构函数 | 释放派生类创建的 QRhi 资源 | renderer 可因窗口重归属等被重建，勿假设资源长期有效 |
