# QNativeInterface::QGLXContext：把 Qt OpenGL 上下文接到 GLX

> 适用版本：Qt 6.0 起；本文按 Qt 6.11.1 说明  
> 头文件：`#include <QOpenGLContext>`  
> 模块：`Qt6::Gui`  
> 关联类型：`QOpenGLContext`、`GLXContext`、`GLXFBConfig`、`XVisualInfo`  
> 条件：Qt 构建启用了 XCB GLX 平台插件

## 它解决什么问题

在 X11 桌面上，Qt 的 `QOpenGLContext` 可能由 GLX 后端实现。`QNativeInterface::QGLXContext` 允许需要 Xlib/GLX 句柄的旧渲染器、捕获库或专有 SDK 与 Qt 上下文互通：

- 从 Qt 上下文取得底层 `GLXContext`；
- 将外部创建的 `GLXContext` 包装成 `QOpenGLContext`；
- 明确区分基于 `GLXFBConfig` 与基于 `XVisualInfo` 创建的两条 GLX 路径。

它不是可自行实例化或派生的应用接口。普通 OpenGL 使用仍应从 `QOpenGLContext`、`QSurface` 和 `QOpenGLFunctions` 开始。若程序跑在 Wayland、EGL 或软件后端，不能假设此接口存在。

## 从 Qt 取得 GLXContext

```cpp
#include <QOpenGLContext>

void passContextToLegacyGlxCode(QOpenGLContext *context)
{
    auto *glx = context->nativeInterface<QNativeInterface::QGLXContext>();
    if (!glx)
        return;

    GLXContext nativeContext = glx->nativeContext();
    // 仅传给必须接收 GLXContext 的 X11/GLX 代码。
}
```

`nativeInterface<T>()` 返回空指针表示当前 Qt 平台插件没有提供 GLX 接口。不能只根据“运行在 Linux”判断，因为 Linux 上还可能使用 Wayland/EGL、远程显示或软件渲染。

`nativeContext()` 的结果是由 `QOpenGLContext` 支撑的借用句柄。不要调用 `glXDestroyContext()`，也不要在 Qt 上下文销毁后使用它。原生接口不改变 `makeCurrent()`、`doneCurrent()` 与线程归属规则。

## 包装外部 GLX 上下文

`fromNative()` 有两个重载，必须按原生上下文的创建方式选择。

### 基于 framebuffer configuration 的上下文

若上下文由 `glXCreateNewContext()` 从 `GLXFBConfig` 创建：

```cpp
QOpenGLContext *qtContext =
    QNativeInterface::QGLXContext::fromNative(glxContext, shareContext);
qtContext->setParent(owner);
```

Qt 会接管该 `GLXContext`；返回的 `QOpenGLContext *` 归调用方管理。包装存在期间，外部代码不得再销毁同一个 GLX 上下文。

### 基于 X visual 的上下文

若上下文由 `glXCreateContext()` 从 X visual 创建，则必须使用第二个重载：

```cpp
QOpenGLContext *qtContext =
    QNativeInterface::QGLXContext::fromNative(glxContext, visualInfo,
                                               shareContext);
```

`visualInfo` 必须是指向创建该上下文时所用 **同一个** `XVisualInfo` 的指针。不能把 `GLXFBConfig` 路径的上下文塞进此重载，也不能给 visual 路径随便构造一个“类似”的 visual；Qt 需要正确的原生创建元数据来包装它。

可选的 `shareContext` 是一个 Qt `QOpenGLContext`。它必须和外部上下文具有真实且兼容的资源共享关系，不能把它当成“让两个上下文自动共享”的开关。

## 生命周期、线程与 X11 边界

- 上下文同一时刻只能在一个线程中 current；Qt 包装不会放宽 GLX 规则。
- 外部 `GLXContext` 一经传给 `fromNative()`，应视为 Qt 包装对象生命周期的一部分，不再由两套代码各自销毁。
- Qt 管理 X11 事件和连接。向 Qt 拥有的 X11/GLX 对象直接注入同步调用或手动改写状态，容易引入重入和死锁；将原生交互限制为目标 SDK 所需的最小操作。
- 原生接口 API 不保证长期的源码或二进制兼容，升级 Qt 时应集中复测这一适配层。

## 常见错误

### 以为所有 Unix 图形环境都能查询 QGLXContext

它取决于 Qt 的 GLX 平台插件，不取决于操作系统名称。运行时必须检查 native interface 是否存在。

### 混淆 `glXCreateNewContext()` 与 `glXCreateContext()`

前者对应无 `visualInfo` 的 FBConfig 重载，后者对应带 `XVisualInfo *` 的重载。选错重载会使 Qt 无法正确描述原生上下文。

### 对 Qt 借出的 GLXContext 再调用 `glXDestroyContext()`

这会让 Qt 保存悬空句柄。销毁应遵从 `QOpenGLContext` 或 `fromNative()` 包装对象的生命周期。

## API 速查表

| 类别 | API | 语义 | 边界与注意点 |
| --- | --- | --- | --- |
| 获取接口 | `context->nativeInterface<QNativeInterface::QGLXContext>()` | 从 Qt OpenGL 上下文查询 GLX 接口。 | 需要 Qt 的 XCB GLX 插件；可能为 `nullptr`。 |
| 静态工厂 | `QOpenGLContext *fromNative(GLXContext configBasedContext, QOpenGLContext *shareContext = nullptr)` | 包装由 `glXCreateNewContext()`、基于 FBConfig 创建的上下文。 | Qt 接管 GLX 上下文；返回 Qt 对象由调用方管理；共享上下文必须兼容。 |
| 静态工厂 | `QOpenGLContext *fromNative(GLXContext visualBasedContext, void *visualInfo, QOpenGLContext *shareContext = nullptr)` | 包装由 `glXCreateContext()`、基于 X visual 创建的上下文。 | `visualInfo` 必须指向创建时使用的同一个 `XVisualInfo`；不可与 FBConfig 路径混用。 |
| 成员函数 | `GLXContext nativeContext() const` | 返回底层 `GLXContext`。 | 借用句柄；不得手动销毁；仍受 current/线程规则约束。 |

## 一句话总结

`QGLXContext` 用于 GLX 专用集成，关键不是“拿到句柄”而是按原始创建路径正确包装，并始终让 Qt 管理已接管上下文的生命周期。
