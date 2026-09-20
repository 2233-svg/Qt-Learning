# QQuickRenderControl
> Qt 6.11.1 · Qt Quick · 来自 `QQuickRenderControl`

## 作用定位
`QQuickRenderControl` 将 Qt Quick 的渲染循环从窗口中拆出来，由宿主决定何时 polish、同步、渲染和呈现。它用于离屏目标、外部交换链或把 QML 画进非 Qt 的引擎。

## API 速查
| API | 是做什么的 |
|---|---|
| `initialize()` | 用当前图形上下文/RHI 初始化渲染控制。|
| `beginFrame()` / `endFrame()` | 包围一次受控帧。|
| `polishItems()` | 执行 GUI 线程的 polish 阶段。|
| `sync()` | 将 GUI 线程状态同步到 Scene Graph。|
| `render()` | 录制 Qt Quick 场景渲染命令。|
| `invalidate()` | 场景图失效时释放相关资源。|
| `setRenderWindow()` | 指定关联的 `QQuickWindow`。|
| `renderRequested()` | Qt Quick 请求宿主安排渲染。|
| `sceneChanged()` | 场景内容变化，通常需要安排一帧。|

## 使用场景
一帧的典型顺序是：GUI 线程 `polishItems()`，在正确同步点 `sync()`，再在渲染目标可写时 `render()`。宿主负责表面取得、提交和帧节流。

## 常见坑与经验
- 不要从任意线程随意调用这些阶段；`sync()` 的线程切换和互斥关系是这个类最容易出错的部分。
- `renderRequested()` 不是“马上 render”；它只说明场景希望有一帧。
- 图形设备丢失或目标重建后必须按生命周期调用 `invalidate()` 和 `initialize()`。

## 知识点覆盖
自定义渲染循环、离屏渲染、帧阶段、Scene Graph 同步、交换链、线程协作。
