# QQuickWindow：Qt Quick 场景、原生窗口和 scene graph 的交汇点

> Qt 6.11.1 | `#include <QQuickWindow>` | CMake: `Qt6::Quick`

`QQuickWindow` 是 Qt Quick 的窗口宿主。它继承 `QWindow`，提供原生窗口、事件和屏幕生命周期；同时拥有一个 `contentItem`，使 QML item tree 能被 scene graph 同步并绘制。`QQuickView` 是它的便捷子类，而需要自行构造 QML 对象、接入原生 GPU 命令或控制离屏输出时，直接使用 `QQuickWindow`。

它要解决的不是“画一个窗口”这么简单，而是三个世界的边界：GUI 线程维护 QML 状态，scene graph 可能在独立渲染线程工作，GPU 命令又受图形 API 的 frame/pass 状态约束。绝大多数稳定性问题都来自跨越这些边界时用了错误的时机或线程。

## 常规窗口与离屏窗口

最普通的路径是把根 item 挂到 `contentItem()`：

```cpp
auto *window = new QQuickWindow;
auto *root = qobject_cast<QQuickItem *>(component.create());
root->setParentItem(window->contentItem());
window->show();
```

当只需从一个 QML 文件启动窗口，`QQuickView` 更省事。若需要把 Qt Quick 渲染到应用自管纹理而非屏幕，使用 `QQuickRenderControl` 创建本类，并配合 `setGraphicsDevice()`、`setGraphicsConfiguration()` 与 `setRenderTarget()`；这种窗口不能 `show()`，帧循环由应用驱动。

默认 scene graph 会为普通可见窗口自动创建图形设备/上下文。需要与 Vulkan、D3D、Metal、OpenGL 引擎共享设备时，应在 scene graph 初始化前设置 `QQuickGraphicsDevice`。配置设备扩展等初始化选项则使用 `QQuickGraphicsConfiguration`；一旦采用外部设备，配置对象不会再参与设备创建。

## 一帧中信号处在什么位置

这组信号通常从**scene graph 渲染线程**发出。需要同步完成的槽必须使用 `Qt::DirectConnection`，且槽内只能接触该线程允许的 scene graph/GPU 对象。

| 时机 | 适合做什么 | 不能误解为 |
|---|---|---|
| `beforeFrameBegin` | 最早的渲染线程帧起点，例如低层资源清理 | 此时并未开始录制当前 frame |
| `beforeSynchronizing` / `afterSynchronizing` | 和 QML 状态同步边界协作 | 常规 GUI 状态的随意并发读写窗口 |
| `beforeRendering` | command buffer 已开始录制，可提交 upload/copy 等非 render-pass 命令 | 主 render pass 已激活；此时直接画 underlay 会被之后清屏覆盖 |
| `beforeRenderPassRecording` | 主 render pass 活跃，插入 Qt Quick 之前的绘制命令 | 可以随意提交资源 upload/copy |
| `afterRenderPassRecording` | 主 pass 的 Quick 命令已录入但 pass 尚未结束，插入 overlay 命令 | frame 已提交或可安全销毁 GPU 资源 |
| `afterRendering` | Quick 已录制命令但尚未提交到队列 | 仍能追加到 Quick 的主 pass |
| `afterFrameEnd` | Qt Quick 已提交 frame 的最后一个渲染线程信号 | 画面一定已显示；重定向渲染也会发出 |
| `frameSwapped` | 一帧已排队呈现 | 离屏 `QQuickRenderControl` 路径的可靠完成通知 |

在 `beforeRendering`、`beforeRenderPassRecording`、`afterRenderPassRecording` 中混入原生命令时，原生 API 必须与 Qt Quick 使用同一后端。原生 device/context/command list 从 `rendererInterface()` 的资源查询中取得，不要凭平台假设缓存句柄。

## 原生命令的正确包围方式

对 scene graph 正在使用的 command buffer 或 encoder 录制原生命令时，使用：

```cpp
connect(window, &QQuickWindow::beforeRenderPassRecording,
        window, [window] {
    window->beginExternalCommands();
    // 重新查询 QSGRendererInterface::CommandListResource，
    // 然后在当前 pass 录制兼容的原生命令。
    window->endExternalCommands();
}, Qt::DirectConnection);
```

`beginExternalCommands()` 和 `endExternalCommands()` 让 Qt Quick 隔离必要状态；在 OpenGL/D3D11 等没有暴露 native command buffer 的后端，它们承担 Qt 5 `resetOpenGLState()` 的相近职责，但不会把 OpenGL 状态重置为默认值。调用 `beginExternalCommands()` 后必须重新查询 `CommandListResource`，因为 Qt 可能为外部命令换成 secondary command buffer。`QSGRenderNode::render()` 中无需显式包围，scene graph 已做此处理。

## scene graph 资源的生死

`sceneGraphInitialized()` 在渲染线程首次可用时发出，适合创建依赖图形上下文的自定义资源。`sceneGraphInvalidated()` 表示上下文/设备已失效，所有绑定它的用户资源都必须释放；窗口再次可渲染时会重新初始化，不能继续使用旧 GPU 对象。

`releaseResources()` 请求释放图像缓存、pipeline、shader 等可重建资源，并且有些 render loop 会进一步释放整套 scene graph。`setPersistentGraphics()` 和 `setPersistentSceneGraph()` 默认都是 true，可作为降低重建频率的提示；它们不是保留全部缓存的保证，调用 `releaseResources()` 后廉价缓存仍会释放。窗口隐藏或失去 expose 后也可能触发同样的资源收缩。

## 纹理、截图与渲染配置

`createTextureFromImage()` 可从 GUI 或渲染线程调用，但 scene graph 尚未初始化时返回空；调用方负责删除返回的 `QSGTexture`。设置 `TextureCanUseAtlas` 后应使用 `normalizedTextureSubRect()`，且不支持 `Repeat`。`TextureIsOpaque` 可避免混合并常带来更快合成，`TextureHasMipmaps` 与 atlas 不能并用。

`createTextureFromRhiTexture()` 仅能在 scene graph 渲染线程调用，返回的 `QSGTexture` 会拥有传入的 `QRhiTexture`。它和传入 native resource 的所有权不同，后者仍由创建 `QRhiTexture` 的方式决定。

`grabWindow()` 是 GUI 线程阻塞式读回，更适合测试或偶发截图。窗口不可见时也可工作，但须已 `create()`、有有效大小且进程中没有别的 `QQuickWindow` 在渲染；通过 `QQuickRenderControl` 重定向时通常返回空图，应由应用直接 readback 自己管理的目标。

静态 `setGraphicsApi()` 应在 `main()` 很早调用，指定 Qt 内建后端使用的 OpenGL/Vulkan/Metal/D3D 或 `Software`；`setSceneGraphBackend()` 更底层，必须在构造第一个 `QQuickWindow` 前调用。初始化后真正使用的 API 应以 `QSGRendererInterface` 为准，`graphicsApi()` 在初始化前只表示当前会选择什么。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `QQuickWindow(parent)` | 创建可显示的 Quick 原生窗口 | QML 根 item 通常设为 `contentItem()` 的子项 |
| `QQuickWindow(renderControl)` | 创建由 `QQuickRenderControl` 驱动的离屏窗口 | 不可 `show()`；帧循环由应用负责 |
| `contentItem()` | 返回 QML/item tree 的不可替换根容器 | 将 C++ 创建的视觉 item 用 `setParentItem()` 挂到这里 |
| `color` / `setColor()` | 设置窗口清屏颜色 | 不改变 QML item 本身的背景与透明语义 |
| `activeFocusItem()` / `focusObject()` | 查询当前键盘焦点目标 | 焦点在 item tree 内迁移，窗口焦点不等于某个 item 已激活 |
| `mouseGrabberItem()` | 查询当前持有鼠标 grab 的 item | 主要用于输入调试，不应作为事件路由替代机制 |
| `update()` | 请求下一帧 scene graph 更新 | 异步调度，不会在调用点立即绘制 |
| `grabWindow()` | 将窗口内容读回 `QImage` | GUI 线程调用；阻塞且重定向渲染通常为空 |
| `setRenderTarget()` / `renderTarget()` | 指定或取得离屏渲染目标 | Qt 6.0 起；目标不转移原生资源所有权，且应在渲染线程设置 |
| `setGraphicsDevice()` / `graphicsDevice()` | 采用或查询外部图形设备/上下文描述 | 必须在初始化前；常与离屏和资源共享组合 |
| `setGraphicsConfiguration()` / `graphicsConfiguration()` | 设置图形设备创建配置 | 初始化前设置；采用外部 device 时该配置被忽略 |
| `rhi()` | 返回窗口正在使用的 `QRhi` | Qt 6.6 起；仅 scene graph 初始化后有效，软件后端为空 |
| `swapChain()` | 返回窗口的 `QRhiSwapChain` | Qt 6.6 起；仅普通在屏窗口，`QQuickRenderControl` 下为空 |
| `rendererInterface()` | 访问 scene graph 的后端资源查询接口 | 用于当前 API 的 native handle/command list 查询 |
| `effectiveDevicePixelRatio()` | 返回 Quick 实际使用的 DPI 比例 | 离屏路径可由 render target/真实窗口信息决定 |
| `createTextureFromImage()` | 从 `QImage` 创建场景纹理 | 未初始化返回空；调用方删除返回纹理 |
| `createTextureFromRhiTexture()` | 用已有 `QRhiTexture` 包装 `QSGTexture` | Qt 6.6 起；只限渲染线程，返回对象接管该 `QRhiTexture` |
| `CreateTextureOptions` | 控制 image texture 的 alpha、mipmap、atlas 等策略 | `TextureOwnsGLTexture` 在 Qt 6 中被忽略；mipmap 与 atlas 不兼容 |
| `createRectangleNode()` / `createImageNode()` / `createNinePatchNode()` / `createTextNode()` | 创建由当前后端实现的基础 QSG node | 仅 scene graph 渲染线程使用 |
| `sceneGraphInitialized()` | 通知 scene graph/图形资源已可用 | 渲染线程；可在资源释放后再次发出 |
| `sceneGraphInvalidated()` | 通知图形上下文或设备已失效 | 渲染线程；必须释放所有绑定该上下文的资源 |
| `beforeRendering()` | 主 pass 之前的录制阶段 | 适合 copy/upload；不是在主 pass 内绘制的插入点 |
| `beforeRenderPassRecording()` | 主 pass 已活跃、Quick 尚未录制命令 | 适合录制 underlay；直接连接并保持 API 状态兼容 |
| `afterRenderPassRecording()` | Quick 主 pass 命令已录制但 pass 未结束 | 适合 overlay；此处通常不能上传资源 |
| `afterRendering()` / `afterFrameEnd()` | Quick 已录制 / 已提交 frame | `afterFrameEnd` 也适用于离屏重定向 |
| `beginExternalCommands()` / `endExternalCommands()` | 包围对 scene graph command list 的原生命令 | 每对调用后重查 command list；不要遗留 API 状态 |
| `scheduleRenderJob(job, stage)` | 在指定渲染阶段安排任务 | 除 `NoStage` 外不主动触发绘制，需要时配合 `update()` |
| `RenderStage` | 选择同步、绘制、swap 前后的任务时点 | 选错阶段会导致线程或 GPU 状态不满足 |
| `releaseResources()` | 请求释放缓存，并可能释放完整 scene graph | 不是 `QQuickItem::releaseResources()`；需准备重建 |
| `setPersistentGraphics()` / `setPersistentSceneGraph()` | 设置资源保留提示 | 默认 true；是 hint，不阻止可重建缓存释放 |
| `graphicsStateInfo()` | 返回当前帧槽与并发帧数 | 面向 Vulkan/Metal 等外部资源多缓冲策略 |
| `setGraphicsApi()` / `graphicsApi()` | 请求/预览 Qt 内建图形 API | 静态 API 应早于任何窗口；初始化后用 renderer interface 确认真实结果 |
| `setSceneGraphBackend()` / `sceneGraphBackend()` | 请求/查询 scene graph backend 名称 | 必须在创建第一个窗口前设置，之后不可更改 |
| `setDefaultAlphaBuffer()` / `hasDefaultAlphaBuffer()` | 配置新窗口默认是否需要 alpha buffer | 创建第一个 `QQuickWindow` 前设置；默认 false |
| `setTextRenderType()` / `textRenderType()` | 设定文字 item 的默认渲染方式 | 静态全局策略，影响后续 Quick 文本渲染 |
| `sceneGraphError(error, message)` | 报告图形初始化等致命 scene graph 问题 | GUI 线程；未连接时 Qt 可能终止应用 |
