# QQuickGraphicsDevice
> Qt 6.11.1 · Qt Quick · 来自 `QQuickGraphicsDevice`

## 作用定位
`QQuickGraphicsDevice` 把应用已拥有的原生图形设备交给 Qt Quick 使用。它解决的是“宿主已有 Vulkan、Metal、D3D 或 OpenGL 设备，Qt Quick 不应另起一套”的嵌入式渲染需求。

## API 速查
| API | 是做什么的 |
|---|---|
| `fromOpenGLContext()` | 从现有 `QOpenGLContext` 创建描述。|
| `fromVulkanPhysicalDevice()` | 提供 Vulkan 物理设备和逻辑设备信息。|
| `fromD3D11Device()` / `fromD3D12Device()` | 使用现有 Direct3D 设备。|
| `fromMetalDevice()` | 使用现有 Metal 设备。|
| `isNull()` | 判断是否包含有效设备描述。|

## 使用场景
游戏引擎、CAD 宿主或专用渲染框架需要在同一个 GPU 设备上叠加 QML HUD 时，在创建窗口早期设置 `QQuickWindow::setGraphicsDevice()`。

## 常见坑与经验
- 设备、队列和上下文的线程及所有权规则仍由原生 API 约束；这个类不会替你同步。
- 后端必须与 Qt Quick 实际选择的 RHI 后端兼容。
- 普通桌面应用没有理由手动设置设备，保留 Qt Quick 自动创建通常更可靠。

## 知识点覆盖
原生设备互操作、Vulkan/Metal/D3D/OpenGL、资源所有权、GPU 同步、Qt Quick 嵌入。
