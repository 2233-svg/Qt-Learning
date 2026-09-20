# QSurface
> Qt 6.11.1 · Qt GUI · 来自 `QSurface`

## 1. 先建立直觉

`QSurface` 是可被图形 API 渲染到的表面的抽象基类。实际对象通常是 `QWindow` 或 `QOffscreenSurface`：前者有屏幕窗口，后者用于离屏上下文或资源共享。

它回答的问题是：这个 surface 是窗口还是离屏？适合哪种渲染 API？大小和格式是什么？底层平台句柄在哪里？

## 2. 类说明

- 头文件：`#include <QSurface>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 直接派生：`QWindow`、`QOffscreenSurface`
- 类型：抽象基类
- 协作类：`QSurfaceFormat`、`QOpenGLContext`、Vulkan/Metal/Direct3D 平台接口

应用一般不直接继承 `QSurface`，而是使用 `QWindow` 或 `QOffscreenSurface`。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `surfaceClass()` | 返回 `Window` 或 `Offscreen` |
| `surfaceType()` | 返回 raster/OpenGL/Vulkan/Metal/Direct3D 等 surface 类型 |
| `format()` | 返回实际或请求的 surface format |
| `size()` | 返回 surface 像素尺寸 |
| `supportsOpenGL()` | 是否能配合 `QOpenGLContext` |
| `surfaceHandle()` | 返回平台层 surface 句柄 |

## 4. 类型速查

| 枚举 | 说明 |
| --- | --- |
| `SurfaceClass::Window` | 实际对象是 `QWindow` |
| `SurfaceClass::Offscreen` | 实际对象是 `QOffscreenSurface` |
| `RasterSurface` | 软件光栅绘制 surface |
| `OpenGLSurface` | OpenGL 兼容 surface |
| `VulkanSurface` | Vulkan 兼容 surface |
| `MetalSurface` | Apple 平台 Metal surface |
| `Direct3DSurface` | Windows Direct3D surface |
| `OpenVGSurface` | OpenVG surface |

## 5. 关键用法

OpenGL 代码常先检查 surface：

```cpp
if (!surface->supportsOpenGL())
    return;

context->makeCurrent(surface);
```

离屏资源初始化通常用 `QOffscreenSurface`：

```cpp
QOffscreenSurface surface;
surface.setFormat(format);
surface.create();
context->makeCurrent(&surface);
```

`format()` 可能是平台协商后的结果，不一定和你请求的 `QSurfaceFormat` 完全一致。

## 6. 使用场景

- OpenGL context 绑定窗口或离屏 surface。
- 后台创建纹理、FBO、shader 等 GL 资源。
- 检查 `QWindow` 当前图形 API 类型。
- 平台集成层拿到底层 surface handle。
- 多后端渲染框架区分 Vulkan/Metal/D3D/OpenGL。

## 7. 常见坑与经验

- `QSurface` 不是 `QObject`，不要期待信号或 parent 生命周期。
- surface 类型要在窗口创建前设置；创建后再改通常无效或需要重建。
- `size()` 通常是像素尺寸，高 DPI 下不要直接混用逻辑尺寸。
- `surfaceHandle()` 是平台私有层，除非写平台集成代码，否则不要依赖。
- OpenGL context 的 format 与 surface format 需要兼容，否则 `makeCurrent()` 可能失败。

## 8. 知识点覆盖

本页覆盖：窗口/离屏 surface、渲染 API 类型、surface format、OpenGL current surface、平台句柄、高 DPI 像素尺寸。
