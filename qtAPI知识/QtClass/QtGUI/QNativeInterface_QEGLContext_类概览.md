# QNativeInterface::QEGLContext：接入和检查底层 EGL 上下文

> 适用版本：Qt 6.0 起；本文按 Qt 6.11.1 说明  
> 头文件：`#include <QOpenGLContext>`  
> 模块：`Qt6::Gui`  
> 关联类型：`QOpenGLContext`、`EGLContext`、`EGLDisplay`、`EGLConfig`  
> 条件：Qt 构建启用了 EGL

## 它解决什么问题

`QOpenGLContext` 是 Qt 管理 OpenGL 或 OpenGL ES 上下文的跨平台入口。嵌入式 Linux、Android、EGLFS、部分 Wayland/X11 集成及第三方渲染库，有时必须使用原生的 `EGLContext`、`EGLDisplay` 或 `EGLConfig`。`QNativeInterface::QEGLContext` 提供这两个世界间的桥接：

- 从已创建的 `QOpenGLContext` 查询其原生 EGL 句柄、显示连接和配置；
- 将由外部 EGL 代码创建的 `EGLContext` 纳入 Qt 的 `QOpenGLContext` 生命周期；
- 在特定平台通知 Qt Quick 场景图上下文已失效。

它不是让应用派生的接口。普通绘制、上下文创建、`makeCurrent()` 与交换缓冲都应优先使用 `QOpenGLContext` 和 Qt 的 surface 类型；仅当原生 API 的参数确实是 EGL 类型时才使用它。

## 从 Qt 上下文读取 EGL 信息

先确保 `QOpenGLContext::create()` 成功，再查询接口：

```cpp
#include <QOpenGLContext>

void inspectEglContext(QOpenGLContext *context)
{
    auto *egl = context->nativeInterface<QNativeInterface::QEGLContext>();
    if (!egl)
        return; // 当前平台插件并未使用或公开 EGL。

    const auto nativeContext = egl->nativeContext();
    const auto nativeDisplay = egl->display(); // Qt 6.3 起
    const auto nativeConfig = egl->config();   // Qt 6.3 起

    // 仅将这些句柄传给必须使用 EGL 的原生库。
}
```

代码须能在 Qt 未启用 EGL 的构建中排除相关声明；不要只用操作系统宏判断。例如同为 Linux，实际后端可能是 GLX、EGL、软件渲染或其它集成。`nativeInterface<T>()` 返回空指针时，应回退到纯 Qt 路径或报告该功能不可用。

`nativeContext()`、`display()` 和 `config()` 返回的都是底层对象的借用句柄。不要对它们调用 `eglDestroyContext()`、`eglTerminate()` 或其它会改变 Qt 管理资源生命周期的操作。

## 包装外部创建的 EGLContext

```cpp
QOpenGLContext *qtContext =
    QNativeInterface::QEGLContext::fromNative(eglContext, eglDisplay,
                                               shareContext);
if (!qtContext)
    return;

qtContext->setParent(owner);
```

`fromNative()` 接管 `eglContext`，使 Qt 包装对象负责使用和销毁阶段的协调；包装尚存活时，外部代码不能再自行销毁同一个 `EGLContext`。返回的 `QOpenGLContext *` 则由调用方管理，可以设置父对象。

第二个参数必须是创建该 `EGLContext` 时传给 `eglCreateContext()` 的**同一个** `EGLDisplay`。传入另一个显示连接即使其看似对应同一设备，也会造成未定义或失败的 EGL 调用。可选 `shareContext` 是 Qt 的共享上下文，必须与原生上下文共享关系和配置兼容。

包装不自动解除 EGL 的线程限制。一个上下文同一时刻只能在一个线程中 current；移动 Qt 上下文到线程前必须遵守 `QOpenGLContext` 的规则，且不能让它仍处于 current 状态。

## `invalidateContext()` 何时使用

`invalidateContext()` 从 Qt 6.5 提供，用来将 EGL 上下文标为无效。如果该上下文正被 Qt Quick 场景图使用，Qt 会销毁并新建该上下文。它适合底层平台确认图形上下文不可继续使用的异常恢复路径。

这不是通用的“刷新 OpenGL”函数，也不是所有平台的上下文重置方案。Qt 文档明确指出，它只预期在某些平台有效，例如 eglfs。调用后应准备好处理资源重建：纹理、FBO、着色器缓存和与场景图相连的外部资源都不能假定仍有效。

## 版本与常见错误

- `nativeContext()` 和 `fromNative()` 自 Qt 6.0 可用。
- `config()`、`display()` 自 Qt 6.3 可用；项目的最低 Qt 版本若更低，需做版本条件编译或避免调用。
- `invalidateContext()` 自 Qt 6.5 可用，且平台效果有限。

### 将 `EGLDisplay` 和显示器概念混为一谈

`EGLDisplay` 是 EGL 的连接/显示对象，不是 Qt 的 `QScreen`，也不是物理显示器编号。它必须与 `eglCreateContext()` 使用的对象匹配。

### 从 native handle 反向手动销毁 Qt 资源

Qt 已管理其创建或接管的上下文。原生句柄只用于与必要的 EGL API 协作，不表示所有权回到调用方。

### 误以为 `invalidateContext()` 到处都能重建

它只针对支持该路径的平台。跨平台恢复策略仍需根据渲染后端和 Qt Quick 生命周期设计。

## API 速查表

| 类别 | API | 语义 | 边界与注意点 |
| --- | --- | --- | --- |
| 获取接口 | `context->nativeInterface<QNativeInterface::QEGLContext>()` | 从 Qt 上下文查询 EGL 原生接口。 | Qt 必须启用 EGL；可能为 `nullptr`；接口由 Qt 管理。 |
| 静态工厂 | `QOpenGLContext *fromNative(EGLContext context, EGLDisplay display, QOpenGLContext *shareContext = nullptr)` | 将外部 EGL 上下文包装为 Qt 上下文。 | 接管 `context`；`display` 必须与 `eglCreateContext()` 时完全相同；返回 Qt 对象由调用方管理。 |
| 成员函数 | `EGLContext nativeContext() const` | 返回底层 `EGLContext`。 | 借用句柄；不要手动销毁；受 `QOpenGLContext` 生命周期和线程规则约束。 |
| 成员函数，Qt 6.3 起 | `EGLConfig config() const` | 返回底层上下文关联的 EGL 配置。 | 用于原生 EGL 集成；低于 Qt 6.3 的构建不可调用。 |
| 成员函数，Qt 6.3 起 | `EGLDisplay display() const` | 返回底层上下文关联的 `EGLDisplay`。 | 不是 `QScreen`；不得混用不同 EGL 连接。 |
| 成员函数，Qt 6.5 起 | `void invalidateContext()` | 标记上下文无效；Qt Quick 场景图可能据此重建。 | 只预期在部分平台有效，例如 eglfs；调用后需处理图形资源重建。 |

## 一句话总结

`QEGLContext` 是 Qt 与 EGL 的受控桥梁：用它查询或接管必要的原生上下文，但让 `QOpenGLContext` 继续主导生命周期、线程规则和跨平台渲染逻辑。
