# QOpenGLContext

> Qt 6.11.1 · Qt GUI · 来自 `QOpenGLContext`

## 1. 先建立直觉

`QOpenGLContext` 是 Qt 对 OpenGL / OpenGL ES 上下文的封装。真正的 OpenGL 调用必须发生在某个上下文已经对某个 `QSurface` 成为 current 的线程中；否则很多 GL 函数要么失败，要么操作到错误对象。

使用它的闭环是：选择 `QSurfaceFormat` -> 设置共享上下文/屏幕 -> `create()` -> `makeCurrent(surface)` -> 调用 GL -> `swapBuffers()` 或离屏收尾 -> `doneCurrent()` -> 在上下文销毁前清理资源。

## 2. 类说明

- 头文件：`#include <QOpenGLContext>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QObject`
- 相关 surface：`QWindow`、`QOffscreenSurface`、部分 Qt OpenGL 组件的内部 surface。
- 函数入口：`QOpenGLFunctions` / `QOpenGLExtraFunctions` 或 `getProcAddress()`。

上下文的请求格式和实际格式可能不同。驱动可能给你更高版本、更大缓冲，或在无法满足时失败。

## 3. API 速查

| API | 用途 |
|---|---|
| `setFormat(format)` / `format()` | 设置请求格式；创建后查询实际格式。 |
| `setShareContext(ctx)` / `shareContext()` | 创建前指定资源共享上下文。 |
| `create()` | 创建原生 OpenGL 上下文。 |
| `isValid()` | 检查上下文是否创建成功且未丢失。 |
| `makeCurrent(surface)` | 让上下文在当前线程绑定到 surface。 |
| `doneCurrent()` | 解除当前线程的 current 上下文。 |
| `surface()` | 查询当前绑定的 surface。 |
| `swapBuffers(surface)` | 交换 surface 前后缓冲，显示一帧。 |
| `functions()` / `extraFunctions()` | 取得已初始化的 Qt GL 函数包装。 |
| `getProcAddress(name)` | 查询平台 GL 函数指针。 |
| `extensions()` / `hasExtension()` | 查询扩展支持，要求上下文或共享上下文 current。 |
| `defaultFramebufferObject()` | 获取当前 surface 的默认 FBO。 |
| `isOpenGLES()` / `openGLModuleType()` | 判断 ES 或桌面 OpenGL 实现。 |
| `currentContext()` | 返回当前线程 current 的上下文。 |
| `globalShareContext()` | 返回全局共享上下文；不要直接 makeCurrent 它。 |
| `shareGroup()` / `areSharing()` | 查询资源共享组和共享关系。 |
| `supportsThreadedOpenGL()` | 平台是否支持非 GUI 线程 OpenGL。 |
| `aboutToBeDestroyed()` | 原生上下文销毁前清理 GL 资源。 |

## 4. 关键用法

### 创建并渲染一帧

```cpp
QOpenGLContext context;
context.setFormat(window->requestedFormat());
if (!context.create())
    return;

if (context.makeCurrent(window)) {
    QOpenGLFunctions *gl = context.functions();
    gl->glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    context.swapBuffers(window);
    context.doneCurrent();
}
```

每次渲染前都要确保目标 context 对目标 surface current。窗口最小化、surface 未暴露、设备暂停或上下文丢失时，`makeCurrent()` 可能失败，渲染代码必须检查返回值。

### 共享资源给后台上下文

```cpp
QOpenGLContext workerContext;
workerContext.setFormat(guiContext->format());
workerContext.setShareContext(guiContext);
workerContext.create();
```

共享上下文必须在 `create()` 前设置。共享通常覆盖纹理、缓冲、着色器等服务器端资源，但 framebuffer 绑定、VAO 状态、当前 program、viewport 等上下文状态仍各自独立；不要把“资源共享”误解成“状态共享”。

### 正确绑定默认 framebuffer

```cpp
gl->glBindFramebuffer(GL_FRAMEBUFFER,
                      context.defaultFramebufferObject());
```

跨平台代码不要硬编码 `glBindFramebuffer(..., 0)`。在 iOS、`QOpenGLWidget`、`QQuickWidget` 等场景中，Qt 可能把正确的默认 FBO 映射到非 0 值。

## 5. 线程与上下文丢失

| 问题 | 处理方式 |
|---|---|
| 想在工作线程上传纹理 | 使用共享 context + `QOffscreenSurface`，并把 context 移到该线程。 |
| `makeCurrent()` 失败 | 检查 surface 是否有效/暴露，再检查 `isValid()` 是否提示上下文丢失。 |
| 上下文丢失 | 重新 `create()`，重新初始化所有 GL 资源。 |
| 清理 GL 资源 | 连接 `aboutToBeDestroyed()`，确保清理时 context current。 |
| 想跨线程直接用同一 context | 先在原线程 `doneCurrent()`，再 `moveToThread()`，并理解 QObject 线程归属。 |

`supportsThreadedOpenGL()` 为 false 时，不要设计依赖后台 OpenGL 的渲染路径；即使为 true，也要遵守 context 只能在一个线程 current 的规则。

## 6. 常见坑与经验

- `setFormat()`、`setShareContext()`、`setScreen()` 都应在 `create()` 前调用。
- `format()` 创建前是请求值，创建后是实际值；诊断驱动问题时要看创建后的结果。
- `getProcAddress()` 返回非空不保证函数在当前上下文合法，仍要检查版本或扩展。
- `extraFunctions()` 暴露更多函数，但不代表运行时一定支持所有调用。
- `globalShareContext()` 只能作为共享源，不应直接拿来 current。
- `swapBuffers()` 后如果要继续绘制下一帧，通常重新 `makeCurrent()`，以适应平台状态变化。
- 析构当前线程 current 的 context 会隐式 `doneCurrent()`，但依赖析构顺序清理 GL 资源仍然脆弱。

## 7. 知识点覆盖

- OpenGL 上下文、surface 和 current 状态
- 请求格式、实际格式与 OpenGL / OpenGL ES 区分
- 资源共享组、全局共享上下文和后台上传
- GL 函数入口、扩展和版本检查
- 默认 framebuffer、buffer swap 和跨平台差异
- 线程归属、上下文丢失和资源清理时机
