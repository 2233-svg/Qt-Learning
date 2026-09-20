# QNativeInterface::QAndroidOffscreenSurface：Android 原生离屏 Surface 桥接

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOffscreenSurface>`  
> 模块：`Qt6::Gui`  
> 平台：Android 专用  
> 自 Qt 6.0 提供  
> 相关类型：`QOffscreenSurface`、`QOpenGLContext`、`ANativeWindow`

`QNativeInterface::QAndroidOffscreenSurface` 是 `QOffscreenSurface` 的 Android 原生接口。它让代码在 Qt 的跨平台离屏 surface 与 Android NDK 的 `ANativeWindow *` 之间桥接。这个接口不是普通的离屏渲染 API；常规 OpenGL 资源创建、共享上下文与 FBO 渲染只需使用 `QOffscreenSurface` 本身。

## 它解决的问题

某些 Android 集成场景已经持有 NDK 层的 `ANativeWindow *`，或必须把 Qt 创建的离屏 surface 交给只接受原生窗口句柄的库。此时可通过这个接口：

- 从已有 `QOffscreenSurface` 取得关联的 Android 原生 surface。
- 将已有 `ANativeWindow *` 包装为 `QOffscreenSurface`，以便与 Qt 的 OpenGL 上下文 API 协作。

它不用于读取离屏像素。`QOffscreenSurface` 的本意是为 OpenGL context 提供可 `makeCurrent()` 的目标，常见用途是异步纹理上传或渲染到 FBO；其像素通常不可直接访问。

## 使用前的硬边界

1. **只在 Android 编译。** 该类型仅在 `Q_OS_ANDROID` 下声明；桌面构建必须用条件编译隔离。
2. **接口可能不可用。** `QOffscreenSurface::nativeInterface<T>()` 在请求接口不受当前平台插件支持时返回 `nullptr`。
3. **它是 native interface API。** Qt 头文件明确警告：使用该层可能导致未来 Qt 版本的源代码和二进制兼容性问题。将使用范围收敛在一个 Android 适配层，不要扩散到业务代码。
4. **surface 的创建和销毁在 GUI 线程。** 某些平台以隐藏 `QWindow` 实现离屏 surface；跨平台规则是 `create()` 与 `destroy()` 始终在主 GUI 线程执行。创建完成后，才可在其他线程用相应 context `makeCurrent()`。

## 从 Qt surface 取得 `ANativeWindow *`

```cpp
#include <QOffscreenSurface>

#if defined(Q_OS_ANDROID)
static ANativeWindow *nativeWindowFor(QOffscreenSurface *surface)
{
    if (!surface || !surface->isValid())
        return nullptr;

    auto *androidSurface =
        surface->nativeInterface<QNativeInterface::QAndroidOffscreenSurface>();

    return androidSurface ? androidSurface->nativeSurface() : nullptr;
}
#endif
```

`nativeSurface()` 返回的是由当前 Qt surface 背书的原生句柄视图。调用方不应把它缓存到 `QOffscreenSurface::destroy()` 之后，也不应假定可自行释放、替换或跨线程长期使用该句柄。原生句柄所有权、引用计数和可用线程还受 Android NDK 与具体平台后端约束。

若返回空指针，先区分两种情况：

- `nativeInterface<QAndroidOffscreenSurface>() == nullptr`：当前平台/插件没有该接口，或代码并非运行在可提供 Android 接口的路径上。
- 接口存在但 `nativeSurface() == nullptr`：底层可能采用无原生 surface 的实现，或 surface 尚未有效创建。`QOffscreenSurface` 文档明确允许某些平台使用 surfaceless context 扩展。

因此，原生句柄不是 `QOffscreenSurface` 正常工作的必要前提。只要目标是 FBO 渲染或共享纹理上传，优先继续使用 Qt 的 surface/context API。

## 从 `ANativeWindow *` 包装 surface

```cpp
#if defined(Q_OS_ANDROID)
ANativeWindow *nativeWindow = acquireWindowFromAndroidLayer();

QOffscreenSurface *surface =
    QNativeInterface::QAndroidOffscreenSurface::fromNative(nativeWindow);

if (!surface || !surface->isValid()) {
    // 建立桥接失败；不要继续传给 QOpenGLContext::makeCurrent()。
}
#endif
```

`fromNative()` 只适合已经明确需要把 NDK surface 带入 Qt 的低层集成代码。接口页没有声明 `ANativeWindow *` 的所有权转移规则，因此不能假定 Qt 会替调用方 `ANativeWindow_release()`，也不能在 Qt 仍使用时提前释放外部句柄。应把“谁获取、谁持有、谁释放 nativeWindow”和“谁删除返回的 QOffscreenSurface”写在封装层的 API 契约中，并在目标 Android/Qt 组合上实测。

## 与 QOffscreenSurface 的正确生命周期

```cpp
// GUI 线程：配置实际兼容的 format 后创建。
auto *surface = new QOffscreenSurface;
surface->setFormat(context.format()); // 使用已创建 context 的实际格式
surface->create();

if (!surface->isValid()) {
    delete surface;
    return;
}

// 其他线程可在正确的 QOpenGLContext 管理下 makeCurrent(surface)。
// GUI 线程：停止所有使用后销毁。
surface->destroy();
delete surface;
```

`setFormat()` 必须在 `create()` 前调用。为保证和已有 context/window 兼容，应使用已创建对象的 `QOpenGLContext::format()` 或 `QWindow::format()`，而不是只使用 `requestedFormat()`；窗口 surface 与 pbuffer/surfaceless surface 可支持不同配置。

在另一个线程使用时，先保证没有其他线程让同一个 `QOpenGLContext` current，且所有 GPU 工作与共享资源同步都已处理。`QAndroidOffscreenSurface` 不会替你解决 OpenGL context 互斥、EGL 当前线程绑定或 Android 生命周期暂停/恢复的问题。

## 常见错误

1. **在所有平台包含或实例化 Android 接口。** 用 `#if defined(Q_OS_ANDROID)` 隔离类型和 NDK 头文件。
2. **不判空就解引用 `nativeInterface()`。** native interface 是可选能力。
3. **在 `create()` 前索取原生句柄。** 先创建并检查 `isValid()`。
4. **销毁 surface 后继续保存 `ANativeWindow *`。** 这是悬空原生资源风险。
5. **误以为离屏 surface 可直接读取像素。** 用 FBO、纹理或专门的读回路径。
6. **在工作线程 create/destroy。** 跨平台规则要求初始化和销毁留在 GUI 线程。
7. **用 `requestedFormat()` 假设实际兼容。** 以已创建 context/window 的实际 `format()` 配置 surface。
8. **将 native interface 扩散到业务层。** 把兼容性风险封在 Android 平台适配模块内。

## API 速查表

| API | 作用 | 使用时的语义与边界 |
| --- | --- | --- |
| `QNativeInterface::QAndroidOffscreenSurface` | Android 的 `QOffscreenSurface` 原生接口类型。 | Qt 6.0 起提供，仅 Android 编译可见；native interface API 不保证未来源码/二进制兼容。 |
| `QOffscreenSurface::nativeInterface<QAndroidOffscreenSurface>()` | 查询 Android 原生接口。 | 接口不可用时返回 `nullptr`；先创建并验证 surface，再检查接口和句柄。 |
| `nativeSurface()` | 取得对应的 `ANativeWindow *`。 | 非拥有式的底层句柄视图；仅在 backing surface 仍有效且 Android 后端提供原生 surface 时使用。 |
| `fromNative(ANativeWindow *)` | 从外部 NDK surface 创建 Qt 的 `QOffscreenSurface` 桥接。 | 仅限低层 Android 集成；外部句柄和返回对象的所有权必须由封装层明确管理。 |
| `QOffscreenSurface::create()` | 分配实际平台资源。 | 在 GUI 线程调用；`setFormat()`/`setScreen()` 应在创建前完成。 |
| `QOffscreenSurface::destroy()` | 释放实际平台资源。 | 在 GUI 线程调用；之后不能再使用或缓存原生句柄。 |
| `QOffscreenSurface::isValid()` | 检查平台资源是否成功创建。 | `false` 时不要传给 `QOpenGLContext::makeCurrent()` 或索取 native handle。 |
| `QOffscreenSurface::setFormat()` / `format()` | 设定请求格式并查询实际格式。 | 实际格式可能不同；优先与已创建的 context/window 的实际格式匹配。 |
| `QOpenGLContext::makeCurrent(surface)` | 将 context 绑定到离屏 surface。 | 与 context 线程归属和并发规则一起使用；不是 `QAndroidOffscreenSurface` 自动完成的工作。 |

## 一句话总结

`QNativeInterface::QAndroidOffscreenSurface` 是 Android NDK 与 Qt 离屏 surface 的窄桥接层：先让 `QOffscreenSurface` 正常创建，再通过可空的 native interface 获取借用句柄；所有权、线程和版本兼容风险都应封装在平台代码中。
