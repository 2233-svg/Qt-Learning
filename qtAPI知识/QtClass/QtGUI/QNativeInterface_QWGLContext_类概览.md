# QNativeInterface::QWGLContext：连接 Qt 与 Windows WGL 上下文

> 适用版本：Qt 6.0 起；本文按 Qt 6.11.1 说明  
> 头文件：`#include <QOpenGLContext>`  
> 模块：`Qt6::Gui`  
> 关联类型：`QOpenGLContext`、`HGLRC`、`HWND`、`HMODULE`  
> 平台：仅 Windows

## 它解决什么问题

Windows 的传统 OpenGL API 使用 WGL：渲染上下文是 `HGLRC`，像素格式由窗口设备上下文关联。Qt 用 `QOpenGLContext` 屏蔽这套平台细节，但旧版图形 SDK、桌面录制库或 WGL 扩展加载器有时必须接收原生句柄。

`QNativeInterface::QWGLContext` 用于：

- 从 Qt 的 `QOpenGLContext` 取得底层 `HGLRC`；
- 将外部已有的 `HGLRC` 包装为 `QOpenGLContext`；
- 取得 Qt 当前使用的 OpenGL 实现模块 `HMODULE`。

它不是应用要派生的接口。常规上下文创建、函数解析、绑定 surface 与渲染仍优先使用 `QOpenGLContext`、`QOpenGLFunctions` 和 Qt 的 surface API。

## 读取已有 Qt 上下文的 HGLRC

```cpp
#include <QOpenGLContext>

#if defined(Q_OS_WIN)
HGLRC nativeHandleFor(QOpenGLContext *context)
{
    if (!context)
        return nullptr;

    auto *wgl = context->nativeInterface<QNativeInterface::QWGLContext>();
    return wgl ? wgl->nativeContext() : nullptr;
}
#endif
```

返回的 `HGLRC` 是借用句柄，不转移所有权。不得对 Qt 创建的上下文调用 `wglDeleteContext()`，也不要在 `QOpenGLContext` 销毁后继续保存它。`nativeInterface<T>()` 仍可能返回 `nullptr`，例如当前 Qt 没有使用 WGL 后端。

## 包装外部 HGLRC

```cpp
#if defined(Q_OS_WIN)
QOpenGLContext *qtContext =
    QNativeInterface::QWGLContext::fromNative(wglContext, nativeWindow,
                                               shareContext);
if (!qtContext)
    return;

qtContext->setParent(owner);
#endif
```

`fromNative()` 接管传入的 WGL 上下文；返回的 `QOpenGLContext *` 由调用方管理，可设置 QObject 父对象。包装成功后，不应由外部代码再次 `wglDeleteContext(wglContext)`。

`HWND window` 不是可有可无的参数。Qt 会查询该窗口的像素格式，并让 `QOpenGLContext::format()` 返回相应的 `QSurfaceFormat`。该窗口任一设备上下文必须已经通过 `SetPixelFormat()` 设置过与 `HGLRC` **兼容**的像素格式；否则包装失败。把任意现存窗口传进来，或拿未设置像素格式的窗口当占位符，都会导致失败或后续格式不一致。

`shareContext` 是已有的 Qt 共享上下文，并不负责临时地“打开共享”。真实的 WGL 对象共享关系、像素格式和使用时序仍必须相容。

## `openGLModuleHandle()` 的用途

```cpp
#if defined(Q_OS_WIN)
HMODULE module =
    QNativeInterface::QWGLContext::openGLModuleHandle();
#endif
```

它返回 Qt 当前实际使用的 OpenGL 实现模块句柄，可用于需要该模块句柄的扩展加载或诊断代码。必须先创建 `QGuiApplication`，因为 Qt 要先完成平台与 OpenGL 实现选择。

该 `HMODULE` 不归调用方所有，不要对它调用 `FreeLibrary()`。它也不是“系统总是 opengl32.dll”的保证；应把它视为 Qt 已选择实现的只读信息。

## 生命周期与线程

- 一个 WGL/OpenGL 上下文同一时刻只能在一个线程中 current；接口不会放宽 `QOpenGLContext::makeCurrent()`、`doneCurrent()` 和线程迁移限制。
- 将 `HGLRC` 交给 Qt 包装后，Qt 和外部代码不能各自管理一次销毁。
- 原生接口 API 有未来源码/二进制兼容风险。将 WGL 代码封装在 Windows 适配模块，不要让 `HGLRC` 进入跨平台业务接口。

## 常见错误

### 未创建 QGuiApplication 就调用 `openGLModuleHandle()`

此时 Qt 尚未确定当前 OpenGL 实现。应在 GUI 应用对象建立之后调用。

### 用像素格式不匹配的 HWND 包装 HGLRC

`fromNative()` 依赖窗口的像素格式推导 `QSurfaceFormat`。确认对应设备上下文已正确执行 `SetPixelFormat()`。

### 把 Qt 借出的 HGLRC 手动删除

`nativeContext()` 仅给出底层访问，不意味着 Qt 放弃生命周期控制。

## API 速查表

| 类别 | API | 语义 | 边界与注意点 |
| --- | --- | --- | --- |
| 获取接口 | `context->nativeInterface<QNativeInterface::QWGLContext>()` | 从 Qt OpenGL 上下文查询 WGL 接口。 | 仅 Windows；可能为 `nullptr`；接口对象由 Qt 管理。 |
| 静态工厂 | `QOpenGLContext *fromNative(HGLRC context, HWND window, QOpenGLContext *shareContext = nullptr)` | 包装外部 WGL 上下文。 | Qt 接管 `context`；`window` 必须有与上下文兼容的已设置像素格式；返回 Qt 对象由调用方管理。 |
| 成员函数 | `HGLRC nativeContext() const` | 返回底层 WGL 上下文句柄。 | 借用句柄；不得 `wglDeleteContext()`；受 Qt 上下文线程规则约束。 |
| 静态查询 | `HMODULE openGLModuleHandle()` | 返回 Qt 当前使用的 OpenGL 实现模块。 | `QGuiApplication` 创建后才可调用；不得 `FreeLibrary()`。 |

## 一句话总结

`QWGLContext` 用于必要的 WGL 互操作；正确传入已设像素格式的窗口、让 Qt 管理被接管的上下文，并把原生模块句柄视为只读借用资源。
