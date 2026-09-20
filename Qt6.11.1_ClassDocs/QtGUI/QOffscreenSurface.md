# QOffscreenSurface

> Qt 6.11.1 · Qt GUI · 来自 `QOffscreenSurface`

## 1. 先建立直觉

`QOffscreenSurface` 是一个没有窗口的 OpenGL surface。它常用于让 `QOpenGLContext` 在后台线程或无可见窗口时也能 `makeCurrent()`，从而创建纹理、缓冲、着色器等 OpenGL 资源，或进行离屏准备工作。

它本身不是 framebuffer，也不等同于 `QOpenGLFramebufferObject`。可以把它理解为“给 OpenGL 上下文附着的不可见平台表面”，让上下文有地方成为 current。

## 2. 类说明

- 头文件：`#include <QOffscreenSurface>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QObject`、`QSurface`
- 表面类型：始终返回 `QSurface::OpenGLSurface`
- 典型搭配：`QOpenGLContext::makeCurrent(surface)`。

底层平台资源直到调用 `create()` 后才存在。格式应在 `create()` 前通过 `setFormat()` 设置。

## 3. API 速查

| API | 用途 |
|---|---|
| `QOffscreenSurface(screen, parent)` | 创建 Qt 对象，尚未分配原生 surface。 |
| `setFormat(format)` | 设置请求的 surface 格式；必须在 `create()` 前设置。 |
| `create()` | 分配平台离屏 surface 资源。 |
| `destroy()` | 释放原生 surface 资源。 |
| `isValid()` | 检查原生 surface 是否创建成功。 |
| `requestedFormat()` | 返回请求格式。 |
| `format()` | 返回实际创建后的格式，可能不同于请求。 |
| `setScreen(screen)` / `screen()` | 设置或查询关联屏幕；已创建时可能重建。 |
| `screenChanged(screen)` | surface 关联屏幕改变时发出。 |
| `size()` | 返回 surface 像素大小。 |
| `nativeInterface<T>()` | 访问平台特定原生接口。 |

## 4. 关键用法

```cpp
auto *surface = new QOffscreenSurface;
surface->setFormat(context->format());
surface->create();

if (!surface->isValid())
    return;

context->makeCurrent(surface);
initializeTextures();
context->doneCurrent();
```

离屏 surface 的格式最好与要使用的 OpenGL context 兼容。若 context 要共享资源，通常让 surface 使用同一个 `QSurfaceFormat`，减少平台驱动因为格式不匹配导致 `makeCurrent()` 失败的概率。

## 5. 使用场景

| 场景 | 建议 |
|---|---|
| 后台线程预创建纹理/缓冲 | 用共享 `QOpenGLContext` + `QOffscreenSurface`。 |
| 应用启动时预热 OpenGL 资源 | 创建离屏 surface，上传资源后再在窗口中复用。 |
| 没有可见窗口但需要 GL context current | 用离屏 surface。 |
| 真正渲染到纹理 | 使用 `QOpenGLFramebufferObject`，离屏 surface 只负责让 context current。 |
| CPU 图像处理 | 不需要 OpenGL 时不要引入它。 |

## 6. 常见坑与经验

- `setFormat()` 在 `create()` 后不会重新解析原生 surface；需要改变格式时应销毁并重建。
- 某些平台要求 `create()` 和 `destroy()` 在 GUI 线程执行，即使之后的 OpenGL 渲染在工作线程。
- `requestedFormat()` 是你要的，`format()` 是平台实际给的；调试兼容性时看后者。
- `setScreen()` 在已创建 surface 上可能触发重建，正在 current 的 context 应先 `doneCurrent()`。
- surface 有效不代表 context 一定能在其上 current；仍要检查 `QOpenGLContext::makeCurrent()` 返回值。
- 平台原生接口不是可移植 API，只在确实需要接入 EGL、Android 等平台能力时使用。

## 7. 知识点覆盖

- OpenGL context 与 surface 的关系
- 离屏 surface 和 framebuffer object 的区别
- 请求格式、实际格式和平台兼容性
- GUI 线程创建与工作线程渲染边界
- 屏幕变化、surface 重建和原生接口
