# QOffscreenSurface：为 OpenGL 提供无窗口的目标 surface

> 头文件：`#include <QOffscreenSurface>`  
> 模块：`Qt6::Gui`  
> 继承：`QObject`、`QSurface`  
> 关联类型：`QOpenGLContext`、`QSurfaceFormat`、`QScreen`

## 它解决什么问题

`QOffscreenSurface` 表示底层平台上的离屏 surface。它让 `QOpenGLContext` 能在没有可见 `QWindow` 的情况下变为 current，常用于把耗时 GPU 工作移出主渲染路径：

- 后台线程异步上传纹理、缓冲或着色器资源；
- 在 `QOpenGLFramebufferObject` 中离屏渲染；
- 为共享上下文创建资源，再交给主窗口或 Qt Quick 使用。

它的重点不是“得到一张可读图片”。虽然通常可渲染，surface 像素并不对应用开放；要读回或组织离屏图像，应使用 FBO、纹理和 `glReadPixels()` 等 OpenGL 手段。

平台实现可能是 pbuffer、无形 `QWindow`，或无原生 surface 的 surfaceless context。因此代码不能假设存在原生窗口、固定尺寸或可直接访问的后备像素。

## 典型工作流

先在 GUI 线程创建 `QOffscreenSurface` 和共享的 `QOpenGLContext`，再将上下文移至工作线程执行 GPU 工作：

```cpp
// GUI 线程：窗口和主 OpenGL 上下文均已成功创建。
QOffscreenSurface *surface = new QOffscreenSurface;
surface->setFormat(mainContext->format()); // 使用实际格式
surface->create();
if (!surface->isValid())
    return;

QOpenGLContext *workerContext = new QOpenGLContext;
workerContext->setFormat(mainContext->format());
workerContext->setShareContext(mainContext);
if (!workerContext->create())
    return;

// 将 workerContext 移到工作线程后，工作线程可调用：
// workerContext->makeCurrent(surface);
// 创建共享纹理或 FBO，随后 workerContext->doneCurrent();
```

真正的线程切换还要在上下文不处于 current 状态时调用 `moveToThread()`，并确保对象销毁回到正确线程。是否能在 GUI 线程外渲染也应先用 `QOpenGLContext::supportsThreadedOpenGL()` 检查。

## 最重要的线程规则

为跨平台安全，`create()`、`destroy()` 和对象析构必须在主 GUI 线程执行。某些平台会用隐藏 `QWindow` 实现离屏 surface，若在工作线程初始化或释放，可能只在某个后端或驱动上随机失败。

完成 `create()` 后，surface 可以作为 `QOpenGLContext::makeCurrent()` 的参数在其它线程使用，但前提是：

- 对应 `QOpenGLContext` 已正确归属到该线程；
- 同一上下文没有在别的线程 current；
- 不在工作线程调用 `setScreen()` 或触发需要重建 surface 的操作；
- 结束时先 `doneCurrent()`，再由 GUI 线程销毁相关平台资源。

`QOffscreenSurface` 是 QObject；若设置 parent，要确保 parent 在 GUI 线程析构。否则隐式析构同样会踩到上述销毁线程限制。

## 格式协商：requested 与 actual 不能混为一谈

`setFormat()` 只设置**请求**，`create()` 时平台才会将其协商为实际格式。应在 `create()` 后读取 `format()`，不要把请求值当作已经兑现的能力。

为了让离屏 surface 与既有窗口/上下文兼容，应使用它们创建后的实际格式：

```cpp
surface.setFormat(mainContext->format());
// 或 surface.setFormat(window->format());
surface.create();
```

不要传 `QWindow::requestedFormat()` 期待“同一份请求必然生成兼容对象”。窗口 surface 与 pbuffer 支持的配置集合可能不同，最终导致 `makeCurrent()` 失败或资源无法共享。

`setFormat()` 在 `create()` 后不会重新协商已有原生 surface；需要新格式时，正确流程是 GUI 线程 `destroy()`、重新设置格式、再 `create()`。

## 屏幕与生命周期

构造函数可指定 `targetScreen`，但不创建平台资源；`create()` 前仍可用 `setScreen()` 改变目标屏幕。若在已创建后调用 `setScreen()`，Qt 会在新屏幕上重建离屏 surface，因而应只在 GUI 线程和渲染暂停期执行。

屏幕被移除时，Qt 可能自动调整关联屏幕并发出 `screenChanged(QScreen *)`。长期运行的后台渲染器应在该信号到来后停止使用旧状态，必要时重新检查 `isValid()` 和实际格式。

## 常见错误

### 以为可以从 QOffscreenSurface 直接取图像

它只提供 OpenGL 的绑定目标，不提供像素访问接口。离屏结果应渲染到 FBO/纹理，再通过 OpenGL 读回或共享。

### 在工作线程调用 `create()` 或让对象在那里析构

即使某台机器可用，隐藏窗口实现会让这种代码失去跨平台性。初始化和销毁固定在 GUI 线程。

### 使用 `requestedFormat()` 建立共享兼容性

共享必须按实际平台格式判断。把已创建的 `QOpenGLContext::format()` 或 `QWindow::format()` 传给 `setFormat()`。

### 忽略 `isValid()`

`create()` 无返回值，平台资源是否成功分配由 `isValid()` 判断。失败时不要继续 `makeCurrent()`。

## API 速查表

| 类别 | API | 语义 | 边界与注意点 |
| --- | --- | --- | --- |
| 构造 | `QOffscreenSurface(QScreen *targetScreen = nullptr, QObject *parent = nullptr)` | 创建对象并可指定目标屏幕；尚未分配原生资源。 | 必须再调用 `create()`；parent 的析构线程应是 GUI 线程。 |
| 生命周期 | `void create()` | 分配离屏 surface 的平台资源，并将请求格式协商为实际格式。 | 跨平台时仅在 GUI 线程调用；随后检查 `isValid()`。 |
| 生命周期 | `void destroy()` | 释放关联的原生平台资源。 | 在 GUI 线程调用；使用该 surface 的上下文应先 `doneCurrent()`。 |
| 生命周期 | `~QOffscreenSurface()` | 销毁对象及其尚存的平台资源。 | 等价地受 GUI 线程销毁限制；留意 QObject parent。 |
| 状态 | `bool isValid() const` | 判断平台资源是否成功创建。 | `create()` 后检查；为 `false` 时不能用于 `makeCurrent()`。 |
| 格式 | `void setFormat(const QSurfaceFormat &format)` | 设置待协商的格式请求。 | 在 `create()` 前设置才影响现有资源；推荐传已创建上下文/窗口的实际格式。 |
| 格式 | `QSurfaceFormat requestedFormat() const` | 返回请求的格式。 | 不是平台实际可用格式。 |
| 格式 | `QSurfaceFormat format() const` | 返回实际 surface 格式；创建前则为当前请求。 | 创建后可能和 `requestedFormat()` 不同。 |
| 屏幕 | `QScreen *screen() const` | 返回当前关联屏幕。 | 指针不归调用方所有；屏幕移除后可能变化。 |
| 屏幕 | `void setScreen(QScreen *newScreen)` | 设置关联屏幕。 | 创建后调用会重建 surface；仅 GUI 线程、渲染暂停时操作。 |
| 信号 | `void screenChanged(QScreen *screen)` | 屏幕显式更改或原屏幕移除时发出。 | 接收后重新检查 surface 的有效性、格式和后台渲染状态。 |
| Surface | `QSurface::SurfaceType surfaceType() const` | 返回 surface 类型。 | 始终为 `QSurface::OpenGLSurface`。 |
| Surface | `QSize size() const` | 返回离屏 surface 尺寸。 | 不代表一个可直接读回的像素图像。 |
| 原生接口 | `template <typename T> T *nativeInterface() const` | 查询平台专用 surface 接口。 | 不可用时为 `nullptr`；返回对象由 Qt 管理，例如 Android 专用接口。 |

## 一句话总结

`QOffscreenSurface` 是让 `QOpenGLContext` 在无窗口情况下进行资源创建和 FBO 渲染的工具；格式用实际值匹配，创建和销毁留在 GUI 线程，后台线程只负责已创建对象上的受控 GPU 工作。
