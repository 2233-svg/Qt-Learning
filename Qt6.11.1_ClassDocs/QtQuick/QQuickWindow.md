# QQuickWindow
> Qt 6.11.1 · Qt Quick · 来自 `QQuickWindow`

## 作用定位
`QQuickWindow` 是承载 Qt Quick 场景的顶层 `QWindow`。它拥有 `contentItem()` 根视觉项、驱动渲染帧，并把 QML 视觉树转换为 Scene Graph。需要把原生渲染、RHI 资源或帧生命周期接到 Qt Quick 时，它是关键入口。

## 类说明
普通应用通常由 `QQuickView` 或 QML 的 `ApplicationWindow` 间接使用它；直接操作 `QQuickWindow` 主要发生在自定义渲染、截图、诊断图形后端和资源生命周期管理中。

## API 速查
| API | 是做什么的 |
|---|---|
| `contentItem()` | 取得窗口的根 `QQuickItem`，可向其中挂接 C++ 创建的视觉项。|
| `setColor()` | 设置场景未覆盖区域的清屏色。|
| `update()` | 请求渲染一帧。|
| `grabWindow()` | 同步截取窗口图像；适合测试或低频导出。|
| `createTextureFromImage()` | 将 `QImage` 包装为当前窗口可用的 `QSGTexture`。|
| `createImageNode()` / `createRectangleNode()` | 创建匹配当前渲染后端的场景图节点。|
| `rendererInterface()` / `rhi()` | 查询底层图形接口和 `QRhi`；不要假定 OpenGL。|
| `scheduleRenderJob()` | 在指定帧阶段执行 `QRunnable`。|
| `beginExternalCommands()` / `endExternalCommands()` | 在 Qt Quick 的命令录制间插入原生图形命令。|
| `setPersistentGraphics()` | 控制窗口隐藏后图形资源是否保留。|
| `setPersistentSceneGraph()` | 控制窗口隐藏后 Scene Graph 是否保留。|
| `beforeSynchronizing()` 到 `afterRendering()` | 渲染帧阶段信号，用于精确接入原生资源。|
| `sceneGraphInvalidated()` | 通知图形上下文/Scene Graph 已失效，应释放相关资源。|

## 使用场景
### 给窗口根项添加 C++ 项
```cpp
auto *item = new GaugeItem(window.contentItem());
item->setWidth(160);
item->setHeight(160);
item->setParentItem(window.contentItem());
```
构造时传入 QObject 父对象只解决释放问题；`setParentItem()` 才使它进入画面。

### 与原生图形 API 共存
在 Qt 6 中，Qt Quick 默认可以使用多种 RHI 后端。只有在 `beforeRenderPassRecording()` 等匹配阶段、并以 `beginExternalCommands()`/`endExternalCommands()` 包住原生命令时，才有机会安全共享渲染上下文。优先使用 `QRhi`，不要把 OpenGL 调用写死。

## 常见坑与经验
- 帧阶段信号的发射线程取决于渲染循环；连接后不要默认能安全读写 GUI 对象。必要时使用 `Qt::DirectConnection` 并只处理渲染线程安全资源，或投递回 GUI 线程。
- `grabWindow()` 会阻塞并产生读回成本，不能放进动画或高频事件。
- `QSGTexture` 与创建它的窗口/Scene Graph 生命周期绑定；收到 `sceneGraphInvalidated()` 后必须视为不可用。
- 外部命令必须遵守当前后端和 render pass 状态。无法明确控制时，选择 `QQuickRhiItem` 或 `QSGRenderNode` 更稳妥。

## 知识点覆盖
顶层窗口、Scene Graph、RHI 后端无关渲染、帧同步、图形资源失效、原生命令嵌入、截图和高 DPI。
