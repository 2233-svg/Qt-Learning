# QOpenGLContext：管理 OpenGL 上下文、surface 绑定与资源共享

> 头文件：`#include <QOpenGLContext>`  
> 模块：`Qt6::Gui`  
> 继承：`QObject`  
> 关联类型：`QSurface`、`QSurfaceFormat`、`QOpenGLFunctions`、`QOpenGLContextGroup`

## 它解决什么问题

OpenGL 调用并不天然属于某个 Qt 窗口；它们必须在一个当前的原生图形上下文中执行，并且上下文要绑定到某个 `QSurface`。`QOpenGLContext` 封装这层平台相关状态，统一处理：

- 根据 `QSurfaceFormat`、目标 `QScreen` 和共享对象创建原生上下文；
- 通过 `makeCurrent()` 将上下文绑定到 `QWindow` 或 `QOffscreenSurface`；
- 提供跨平台的 OpenGL 函数包装、默认 FBO 和扩展查询；
- 组织纹理、buffer、shader 等资源在多个上下文间共享；
- 处理线程归属、上下文销毁和可能发生的 context loss。

它适合编写基于 `QWindow` 的 OpenGL 渲染器、后台 GPU 上传器，以及与原生 OpenGL/WGL/EGL/GLX 集成的底层代码。若使用 `QOpenGLWidget`、`QOpenGLWindow` 或 Qt Quick，通常不应自行创建和接管它们内部的上下文；应在对应绘制/渲染回调中使用框架提供的 current context。

## 最小生命周期

创建顺序很重要：先配置，再 `create()`，然后才 `makeCurrent()`。

```cpp
#include <QGuiApplication>
#include <QOpenGLContext>
#include <QOpenGLFunctions>
#include <QWindow>

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    QWindow window;
    window.setSurfaceType(QSurface::OpenGLSurface);
    window.create();

    QOpenGLContext context;
    context.setFormat(window.format()); // 使用窗口创建后的实际格式
    if (!context.create())
        return 1;

    if (!context.makeCurrent(&window))
        return 1;

    QOpenGLFunctions *gl = context.functions();
    gl->glClearColor(0.08f, 0.10f, 0.14f, 1.0f);
    gl->glClear(GL_COLOR_BUFFER_BIT);
    context.swapBuffers(&window);

    return app.exec();
}
```

`swapBuffers()` 后，为了兼容所有 Qt 平台，下一帧开始发出 OpenGL 命令前应再次调用 `makeCurrent()`。若只是临时停止使用上下文，调用 `doneCurrent()` 解除当前线程的绑定。

## 配置、创建与实际格式

`setFormat()`、`setScreen()`、`setShareContext()` 都是创建配置，应在 `create()` **之前**设置。`create()` 会根据当前格式、共享上下文和目标屏幕尝试创建原生上下文；它会尽量选择兼容的版本，但驱动不必提供请求的精确版本、buffer 位数或 profile。

因此应在成功创建后读取 `format()`，以实际格式决定功能路径：

```cpp
QSurfaceFormat actual = context.format();
if (actual.majorVersion() < 3)
    return 1; // 示例：项目要求至少 OpenGL 3
```

再次调用 `create()` 会先销毁已经存在的原生上下文，再创建新的一个。这会使旧的 GL 对象和函数状态失效，不能把它当作无害的“刷新”。若需要重建，先安排资源清理，并在成功后完整初始化资源。

## 当前上下文与线程规则

OpenGL 上下文具有严格的线程限制：

- 一个 `QOpenGLContext` 同一时刻只能在一个线程、针对一个 `QSurface` current；
- 一个线程同一时刻只能有一个 current context；
- `makeCurrent()` 必须在 `QOpenGLContext` QObject 所属线程调用；
- 迁移到工作线程前，先在原线程 `doneCurrent()`，再 `moveToThread()`，然后只从新线程使用它。

Qt 默认检查这个约束。不要为了绕过错误而设置 `Qt::AA_DontCheckOpenGLContextThreadAffinity`；那只会关闭检查，并不会让底层 OpenGL、QObject 或驱动变得线程安全。

后台纹理上传通常组合 `QOffscreenSurface` 和共享上下文：surface 在 GUI 线程创建，工作上下文正确迁移后在工作线程 `makeCurrent(offscreenSurface)`。先用 `supportsThreadedOpenGL()` 判断平台/驱动是否允许 GUI 线程外的 OpenGL 渲染。

## 资源共享

调用 `setShareContext(other)` 后再 `create()`，可请求共享纹理、buffer、shader 等 OpenGL 资源。共享是否真的建立要用 `shareContext()` 或 `areSharing()` 检查；底层平台不支持时，`shareContext()` 可能返回空。

`shareGroup()` 返回 Qt 维护的共享组，可用于了解哪些成功初始化的上下文属于同一资源组。非共享上下文也有一个只包含自己的组。不要自行销毁共享组对象。

共享对象并不消除同步和生命周期问题：在一个上下文创建纹理、另一个上下文立刻使用前，仍需按 OpenGL/驱动规则完成同步；资源销毁时也必须确保有正确的上下文 current。

`globalShareContext()` 仅在 Qt 创建了应用级共享上下文时才返回非空。它适合被用作新上下文的 `setShareContext()` 目标，以便在显示 `QOpenGLWidget` 或 `QQuickWidget` 前预上传资源。**不要**直接对它调用 `makeCurrent()`；应创建一个与它共享的新上下文并让新上下文 current。

## OpenGL 调用、扩展与默认 FBO

在成功 `makeCurrent()` 后，优先用：

- `functions()`：Qt 提供的标准 `QOpenGLFunctions`，已可直接使用，不需再手动 `initializeOpenGLFunctions()`；
- `extraFunctions()`：更完整的 `QOpenGLExtraFunctions`；
- `getProcAddress()`：解析平台上不一定作为链接符号出现的函数。

`getProcAddress()` 返回非空指针不等于函数一定受支持，部分平台可能给出无效但非空的地址。扩展函数先用 `hasExtension()` 验证扩展名；核心函数则检查 `format()` 的实际版本和 profile。`extensions()` 与 `hasExtension()` 要求当前上下文或与其共享的上下文处于 current 状态。

不要假设默认 framebuffer 总是 `0`。在某些平台，以及 `QOpenGLWidget`/`QQuickWidget` 的绘制期间，正确的默认 FBO 可能不是零。手写 OpenGL 时使用：

```cpp
glBindFramebuffer(GL_FRAMEBUFFER, context.defaultFramebufferObject());
```

若使用 `QOpenGLFunctions::glBindFramebuffer(..., 0)`，Qt 会自动替换为正确的默认 FBO。

## 销毁与 context loss

`aboutToBeDestroyed()` 在底层原生上下文即将销毁前发出，用于清理由 `QOpenGLContext` 以外对象持有的 GL 资源。若槽函数需要先把此上下文 current 才能删除资源，必须以 `Qt::DirectConnection` 连接该信号；排队连接会错过可用时机。

析构时，如果该上下文仍是当前线程的 current context，Qt 会调用 `doneCurrent()`。

`makeCurrent()` 返回 `false` 可能是 surface 未暴露、应用被挂起或图形硬件不可用。随后检查 `isValid()`：

1. 若仍为 `true`，等待适当时机再尝试绑定；
2. 若变为 `false`，上下文可能已丢失：调用 `create()` 重建、重新 `makeCurrent()`，并重新创建全部 GL 资源。

某些平台可在 `QSurfaceFormat` 请求中启用 `ResetNotification`，让 Qt 在 `makeCurrent()` 时监控图形重置状态；这不是所有平台都可用的通用保证。

## 平台边界

`openGLModuleType()` 返回 Qt 当前使用的基础实现：`LibGL` 是桌面 OpenGL，`LibGLES` 是 OpenGL ES 2.0 及以上。它要求 `QGuiApplication` 已创建，而且不必等同于某个具体上下文的 API 类型；桌面实现也可能创建 ES 兼容上下文。判断当前上下文时优先用 `isOpenGLES()` 或 `format().renderableType()`。

WebAssembly 有额外限制：建议一个 `QSurface` 的整个生命周期只与一个 `QOpenGLContext` 绑定。多个 Qt 上下文可能实际复用同一个原生上下文，导致第二个 `makeCurrent()` 后修改的 GL 状态影响第一个对象的预期状态。

`nativeInterface<T>()` 可查询 WGL、EGL、GLX、Cocoa 等平台接口。它可能返回 `nullptr`，返回对象由 Qt 管理，并带有未来 Qt 版本的源码/二进制兼容风险；原生代码应收敛在平台适配层。

## 常见错误

### 用 `requested` 格式假定驱动能力

驱动可以降级或升级版本、profile 和 buffer 配置。功能选择必须依据 `context.format()` 的实际结果。

### 在 `swapBuffers()` 后直接画下一帧

跨平台代码要重新 `makeCurrent()`。这在某些平台表面上可运行，但并非 Qt 的可移植契约。

### 直接绑定 FBO 0

这在常规桌面窗口上常常可行，却会破坏 iOS 或 Qt widget 的渲染目标。使用 `defaultFramebufferObject()` 或 `QOpenGLFunctions` 包装。

### 认为共享上下文等于自动并发安全

共享只共享资源命名空间，不处理并发写入、同步或资源删除时序。

### 直接让 global share context current

Qt 文档明确禁止。以它为共享源创建自己的工作上下文。

## API 速查表

| 类别 | API | 语义 | 边界与注意点 |
| --- | --- | --- | --- |
| 枚举 | `OpenGLModuleType::{LibGL, LibGLES}` | 表示 Qt 使用桌面 OpenGL 或 OpenGL ES 2.0+ 基础实现。 | 不是当前上下文 API 类型的唯一依据；优先 `isOpenGLES()` 或实际 `format()`。 |
| 构造 | `QOpenGLContext(QObject *parent = nullptr)` | 创建尚未初始化的 Qt 上下文对象。 | 配置 format、screen、share context 后再 `create()`。 |
| 生命周期 | `~QOpenGLContext()` | 销毁对象及原生上下文。 | 若自身仍为当前线程 current，会自动 `doneCurrent()`；销毁前清理外部持有的 GL 资源。 |
| 生命周期 | `bool create()` | 按当前 format、share context、screen 创建原生上下文。 | 返回值必须检查；再次调用会先销毁旧上下文；实际格式以 `format()` 为准。 |
| 状态 | `bool isValid() const` | 判断原生上下文是否成功创建且仍有效。 | `makeCurrent()` 失败后若为 `false`，重建上下文并重建全部 GL 资源。 |
| 配置 | `void setFormat(const QSurfaceFormat &format)` | 设置希望兼容的上下文格式。 | `create()` 前才生效；未设置时使用 `QSurfaceFormat::defaultFormat()`。 |
| 查询 | `QSurfaceFormat format() const` | 创建前返回请求格式，创建后返回实际格式。 | 请求不保证逐项兑现；按实际版本/profile/缓冲能力走功能分支。 |
| 配置 | `void setScreen(QScreen *screen)` | 设置创建原生上下文时关联的屏幕。 | 作为创建配置在 `create()` 前设置；屏幕指针不归调用方所有。 |
| 查询 | `QScreen *screen() const` | 返回关联的屏幕。 | 可能为空；不应用于替代 `QSurface` 的屏幕管理。 |
| 共享 | `void setShareContext(QOpenGLContext *shareContext)` | 请求与指定上下文共享 GL 资源。 | 必须在 `create()` 前调用；共享可因平台限制失败。 |
| 共享 | `QOpenGLContext *shareContext() const` | 返回创建时实际共享的上下文。 | 平台无法建立共享时为 `nullptr`。 |
| 共享 | `QOpenGLContextGroup *shareGroup() const` | 返回所属共享组。 | 由 Qt 管理；非共享上下文的组也只含自身。 |
| 共享 | `static bool areSharing(QOpenGLContext *first, QOpenGLContext *second)` | 判断两上下文是否共享 GL 资源。 | 只判断共享关系，不解决并发访问和同步。 |
| 共享 | `static QOpenGLContext *globalShareContext()` | 返回应用级共享上下文，若有。 | 只可作为新上下文的共享源；不得直接 `makeCurrent()`。 |
| 绑定 | `bool makeCurrent(QSurface *surface)` | 在当前线程将上下文绑定到指定 surface。 | 失败可能因未暴露/挂起；对象必须属于当前线程；传 `nullptr` 等价 `doneCurrent()`。 |
| 绑定 | `void doneCurrent()` | 解除当前线程中该上下文的绑定。 | 迁移线程、销毁或停止渲染前使用。 |
| 查询 | `static QOpenGLContext *currentContext()` | 返回调用线程当前上下文。 | 没有 current context 时为 `nullptr`；结果只对当前线程有意义。 |
| 查询 | `QSurface *surface() const` | 返回最近 `makeCurrent()` 绑定的 surface。 | 无 current 绑定时可能为空；不转移 surface 所有权。 |
| 呈现 | `void swapBuffers(QSurface *surface)` | 交换 surface 的前后缓冲，使已绘制内容可见。 | 下一帧发 GL 命令前重新 `makeCurrent()`；仅用于可交换缓冲的 surface。 |
| FBO | `GLuint defaultFramebufferObject() const` | 返回当前 surface 正确的默认 framebuffer。 | 不要硬编码 `0`；widget/某些平台可能使用不同 FBO。 |
| 函数 | `QOpenGLFunctions *functions() const` | 返回已初始化的标准 OpenGL 函数包装。 | 在上下文 current 时调用其 GL 函数；无需手动初始化。 |
| 函数 | `QOpenGLExtraFunctions *extraFunctions() const` | 返回更完整的 OpenGL 函数包装。 | 仍需在正确的 current context 下使用。 |
| 函数 | `QFunctionPointer getProcAddress(const QByteArray &name) const` | 解析扩展或非通用链接符号的 GL 函数。 | 非空地址不保证函数受支持；先检查扩展或实际核心版本。 |
| 函数 | `QFunctionPointer getProcAddress(const char *name) const` | 上一函数的 C 字符串重载。 | 同样需验证能力，避免仅按指针非空调用。 |
| 扩展 | `QSet<QByteArray> extensions() const` | 返回上下文支持的扩展集合。 | 当前上下文或共享上下文必须 current。 |
| 扩展 | `bool hasExtension(const QByteArray &extension) const` | 判断是否支持指定扩展。 | 当前上下文或共享上下文必须 current；扩展名大小写及版本语义要正确。 |
| API 类型 | `bool isOpenGLES() const` | 判断此上下文是否为 OpenGL ES。 | 比 `openGLModuleType()` 更适合当前上下文的分支。 |
| 模块 | `static OpenGLModuleType openGLModuleType()` | 查询 Qt 当前底层 OpenGL 实现类型。 | `QGuiApplication` 创建后才可调用；不替代 per-context 判断。 |
| 线程 | `static bool supportsThreadedOpenGL()` | 判断平台/驱动是否支持 GUI 线程外渲染。 | 只是能力前提；仍需遵守 QObject、current 和 surface 线程规则。 |
| 原生 | `template <typename T> T *nativeInterface() const` | 查询平台专用 OpenGL 上下文接口。 | 可能为 `nullptr`；返回对象由 Qt 管理；隔离平台代码。 |
| 信号 | `void aboutToBeDestroyed()` | 原生上下文销毁前通知，用于释放外部持有的 GL 资源。 | 若需 `makeCurrent()` 清理，必须使用 `Qt::DirectConnection`。 |

## 一句话总结

`QOpenGLContext` 的核心是“正确配置后创建、在正确线程绑定正确 surface、按实际格式和共享结果做决策”；任何 GL 调用、资源生命周期和恢复策略都必须围绕这三个事实安排。
