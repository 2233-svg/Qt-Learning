# QSGRendererInterface：查询 Qt Quick 正在使用的图形后端

> Qt 6.11.1 · `#include <QSGRendererInterface>` · 模块：`Qt6::Quick`

`QSGRendererInterface` 是 Qt Quick 对图形后端的查询入口。它不负责绘制，而是让高级集成代码知道当前场景图选择了 OpenGL、Vulkan、Metal、Direct3D、软件渲染或 QRhi 路径，并在合适时机取得设备、命令队列、命令缓冲等资源。

## 使用场景

实现 `QSGRenderNode`、接入第三方渲染器、或需要依据后端决定资源创建策略时，从 `QQuickWindow::rendererInterface()` 获取它。图形 API 与着色语言能力在窗口构造后即可查询，适合做初始化分支；实际设备和命令资源则不能这么早取。

```cpp
auto *ri = window->rendererInterface();
if (ri->graphicsApi() == QSGRendererInterface::Software)
    return; // 第三方 GPU 路径在此后端不可用
```

## 最重要的有效期规则

`getResource()` 仅在场景图已初始化后才有意义，而且保证成功的时机是节点正在准备下一帧命令时，实践中就是 `QSGRenderNode::render()`。它返回的 `void *` 可能是对象指针，也可能是指向不透明句柄的指针；Vulkan 句柄等情形必须按文档所示再解引用，不能把 `void *` 直接强转为任意句柄。

命令列表、编码器、当前渲染通道等资源仅在当前帧准备/录制期间有效，绝不能缓存到下帧。`isApiRhiBased()` 是例外，它可以从任意线程调用。

## API 速查表

| API | 语义与边界 |
|---|---|
| `graphicsApi()` | 返回当前场景图图形 API；窗口创建后即可查询。 |
| `shaderType()` | 返回当前后端使用/支持的着色语言类型，如 `GLSL`、`HLSL`、`RhiShader`。 |
| `shaderCompilationType()` | 返回可用的编译方式位集：运行时编译和/或离线编译。 |
| `shaderSourceType()` | 返回 `ShaderEffect` 可接受的源码形式位集：字符串、文件、字节码。 |
| `getResource(window, Resource)` | 查询标准图形资源；未支持或当前不可用时返回空，仅限渲染线程。 |
| `getResource(window, const char *key)` | 用后端特有键查询扩展资源；仅限渲染线程。 |
| `isApiRhiBased(api)` | 静态函数，判断 API 是否经 QRhi 图形抽象层；可从任意线程调用。 |
| `GraphicsApi` | 包含 `Software`、`OpenGL`、`Direct3D11/12`、`Vulkan`、`Metal`、`Null` 与 `Unknown`。 |
| `Resource::DeviceResource` | 取得图形设备；Vulkan 等情况下可能是“句柄变量的地址”。 |
| `Resource::CommandQueueResource` | 取得当前图形命令队列。 |
| `Resource::CommandListResource` | 取得当前命令列表/缓冲，只有准备下一帧期间有效。 |
| `Resource::RhiResource` | 取得 `QRhi` 实例；使用 Qt 跨后端图形抽象时优先考虑。 |
| `Resource::PainterResource` | 软件后端中的活动 `QPainter`。 |
| `Resource::OpenGLContextResource` / `RenderPassResource` | 查询特定后端的上下文或主渲染通道；可用性随后端和时机变化。 |
| `RenderMode` | 供 `QSGMaterial::createShader()` 区分普通 2D、无深度 2D 与 3D 渲染模式。 |
