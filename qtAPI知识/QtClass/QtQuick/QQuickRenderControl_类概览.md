# QQuickRenderControl：把 Qt Quick 场景渲染进应用管理的目标

> Qt 6.11.1 | `#include <QQuickRenderControl>` | CMake: `Qt6::Quick`

`QQuickRenderControl` 用于把 Qt Quick 的 scene graph 从普通窗口渲染循环中取出来，交给应用驱动，并输出到外部的纹理、图像或 RHI render target。它解决的是“已有渲染引擎、合成器或 XR runtime，但仍希望把 QML 界面作为一层 GPU 内容嵌进去”的问题。

典型场景是游戏或工业可视化引擎把 QML HUD 渲染到自身纹理、VR/AR 提交 Qt Quick 画面到双眼目标、第三方 D3D/Vulkan/Metal 渲染器与 Qt Quick 共享设备。它不是截屏 API：相比 `QQuickWindow::grabWindow()`，这里的结果保持在 GPU 路径中。

## 离屏窗口仍是场景的宿主

先创建 `QQuickRenderControl`，再用接受它的 `QQuickWindow` 构造函数创建窗口：

```cpp
auto *control = new QQuickRenderControl(this);
auto *quickWindow = new QQuickWindow(control);

quickWindow->setGraphicsDevice(
    QQuickGraphicsDevice::fromDeviceAndContext(device, context));
```

这个 `QQuickWindow` 负责 QML 场景、输入事件、焦点和 scene graph，但**不能调用 `show()`**；它没有对应的原生可见窗口。将 QML 根对象挂到 `quickWindow->contentItem()`，并通过 `quickWindow->setRenderTarget()` 指定输出位置。

设备、上下文以及目标纹理由应用创建并维持生命期。必须先完成 `setGraphicsApi()`、`setGraphicsDevice()`、`setGraphicsConfiguration()` 等配置，再调用 `initialize()`。若使用 Vulkan，应用还必须自行创建 `QVulkanInstance`，设置 Qt Quick 所需 instance extension 后，通过 `QWindow::setVulkanInstance()` 关联到该窗口。

## 一帧的责任归应用

常见的硬件后端帧循环如下：

```cpp
control->polishItems();

control->beginFrame();
const bool changed = control->sync();
if (changed)
    control->render();
control->endFrame();
```

`polishItems()` 应尽量靠近 `sync()` 调用。`beginFrame()` 与 `endFrame()` 包住 `sync()`、`render()`，它们对应 QRhi 的离屏帧开始和结束；同一 `QRhi` 此时不能已有另一个 offscreen 或 swapchain frame 正在录制。`endFrame()` 才会提交 scene graph 已录入的 GPU 命令。

软件 scene graph adaptation 不适用这套 `beginFrame()`/`endFrame()`/`initialize()` 调用约定；相关 `QRhi` 和 command buffer 查询也会得到空指针。

## 信号告诉你该做哪种更新

`renderRequested()` 表示现有 scene graph 只需再次 `render()`；`sceneChanged()` 表示 QML 状态已经改变，需要先 `polishItems()`、`sync()`，再根据 `sync()` 的返回值决定是否 `render()`。这两个信号中都不要直接同步重入整套渲染流程，延后到计时器、引擎 tick 或下一次渲染调度中处理，吞吐和重入安全性都会更好。

初始化成功后会在某个时机收到 `QQuickWindow::sceneGraphInitialized()`，适合创建外部目标并设置到窗口；收到 `sceneGraphInvalidated()` 后则应释放依赖该 scene graph/设备的目标资源。向场景发送鼠标、键盘等输入时，以 `quickWindow` 为接收者调用 `QCoreApplication::sendEvent()`；键盘场景通常还需要对根 item 或目标 item 调用 `forceActiveFocus()`。

## 线程与销毁

单线程使用不需要额外设置。若同步和渲染发生在 GUI 线程外，开始前调用 `prepareThread(targetThread)` 声明目标线程。不要把它当成通用线程迁移函数：QML 对象仍遵守其 GUI 线程归属，跨线程数据需要遵循 scene graph 同步边界。

`invalidate()` 停止渲染并释放 scene graph 资源，等价于真实窗口隐藏时的清理。析构会自动调用它；手工调用之后可再次 `initialize()`。它不理会 `persistentSceneGraph` 和 `persistentGraphics`，上下文相关资源仍会被释放。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `QQuickRenderControl(parent)` | 创建离屏渲染控制器 | 用它创建关联的 `QQuickWindow`；窗口不能显示 |
| `initialize()` | 初始化 scene graph 与 Qt Quick 图形基础设施 | 图形 API、设备、配置要预先设好；失败返回 `false` |
| `invalidate()` | 停止渲染并释放资源 | 可随后重新 `initialize()`；持久化 scene graph 设置不生效 |
| `setSamples(count)` / `samples()` | 设置和读取 MSAA 样本数 | `0`/`1` 禁用；必须与目标资源和 `QQuickRenderTarget` 的样本数一致 |
| `polishItems()` | 执行 QML item 的 polish 阶段 | 尽量紧邻 `sync()`；不是 GPU 绘制 |
| `beginFrame()` | 开始一次 QRhi 离屏帧 | `sync()`、`render()` 必须位于其与 `endFrame()` 之间；软件后端不要调用 |
| `sync()` | 把 QML/GUI 状态同步到 scene graph | 返回 `true` 表示随后需要 `render()` |
| `render()` | 以当前图形上下文绘制 scene graph | 应答 `renderRequested()` 时通常无需先 `sync()` |
| `endFrame()` | 结束离屏帧并提交已录制命令 | 必须与 `beginFrame()` 成对；软件后端不要调用 |
| `renderRequested()` | 请求重新绘制 | 延后调度 `render()`，避免在信号槽中立即重入 |
| `sceneChanged()` | QML 场景改变 | 延后执行 `polishItems()`、`sync()`，必要时再 `render()` |
| `prepareThread(thread)` | 指定同步和渲染发生的线程 | 仅多线程渲染使用；不改变 QML 对象的线程规则 |
| `rhi()` | 返回初始化后的 `QRhi` | Qt 6.6 起；初始化前和软件后端均为 `nullptr` |
| `commandBuffer()` | 返回本离屏帧的 command buffer | Qt 6.6 起；通常仅在 `beginFrame()` 到 `endFrame()` 之间使用 |
| `window()` | 返回关联的离屏 `QQuickWindow` | 它是场景宿主，不是可显示窗口 |
| `renderWindow(offset)` | 供子类报告实际承载输出的窗口与偏移 | 多屏 DPI、QML popup 定位时强烈建议重写 |
| `renderWindowFor(win, offset)` | 查询某个离屏窗口对应的真实窗口 | 无关联真实窗口时返回空 |
