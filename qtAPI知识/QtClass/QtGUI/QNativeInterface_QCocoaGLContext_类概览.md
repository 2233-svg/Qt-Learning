# QNativeInterface::QCocoaGLContext：连接 Qt 与 NSOpenGLContext

> 适用版本：Qt 6.0 起；本文按 Qt 6.11.1 说明  
> 头文件：`#include <QOpenGLContext>`  
> 模块：`Qt6::Gui`  
> 关联类型：`QOpenGLContext`、`NSOpenGLContext`  
> 平台：仅 macOS

## 它解决什么问题

`QOpenGLContext` 将 OpenGL 上下文抽象为跨平台 Qt 对象，但 macOS 上的旧有渲染代码、Cocoa 插件或 SDK 可能只接受 `NSOpenGLContext *`。`QNativeInterface::QCocoaGLContext` 提供双向桥接：

- 从 Qt 的 `QOpenGLContext` 取得底层 `NSOpenGLContext *`；
- 将已有的 `NSOpenGLContext *` 包装为 Qt 能识别的 `QOpenGLContext`。

它不是应用应自行派生的接口，实现由 Qt 的 macOS 平台层提供。日常的创建、当前上下文切换、交换缓冲和格式查询仍应使用 `QOpenGLContext`；只有必须和 Cocoa/OpenGL 原生 API 交互时才进入这层接口。

Apple 已弃用 macOS OpenGL。新项目若不受既有 SDK 限制，应优先评估 Qt 的 RHI、Metal 或 Qt Quick 渲染路径。此接口的价值主要在维护既有 OpenGL 集成。

## 从 Qt 取得 NSOpenGLContext

先正常创建 Qt 上下文，再查询 native interface：

```cpp
#include <QOpenGLContext>

#if defined(Q_OS_MACOS)
void useCocoaContext(QOpenGLContext *context)
{
    auto *cocoa =
        context->nativeInterface<QNativeInterface::QCocoaGLContext>();
    if (!cocoa)
        return;

    NSOpenGLContext *nativeContext = cocoa->nativeContext();
    // 将 nativeContext 仅传给需要它的 Cocoa / Objective-C++ 代码。
}
#endif
```

调用 Cocoa 方法的源文件通常应使用 `.mm` 后缀并导入 AppKit；纯 C++ 文件应将上面的原生细节隔离到 macOS 适配层。`nativeInterface<T>()` 可能返回 `nullptr`，因此即使编译目标是 macOS 也必须判空。

`nativeContext()` 返回由 Qt 上下文支撑的借用指针。不要 `release`、`delete` 或跨越 `QOpenGLContext` 的销毁期保存它。需要长期引用时，保存 Qt 对象或在使用点重新查询接口。

## 包装已有的 NSOpenGLContext

当上下文由 Cocoa 或旧 SDK 创建，而后续代码需要 `QOpenGLContext` 时，使用静态工厂：

```cpp
#if defined(Q_OS_MACOS)
QOpenGLContext *qtContext =
    QNativeInterface::QCocoaGLContext::fromNative(nativeContext, shareContext);
if (!qtContext)
    return;

qtContext->setParent(owner);
#endif
```

`fromNative()` 会接管并保留传入的 `NSOpenGLContext`，让 Qt 包装对象在其生命周期内使用它。创建后的 `QOpenGLContext *` 归调用方管理，通常设置 QObject 父对象或在适当时机删除。包装仍存活时，不要在外部以与 Qt 冲突的方式释放该原生上下文。

可选的 `shareContext` 表示要与其共享 OpenGL 对象的 Qt 上下文。它必须与原生上下文的像素格式、共享关系和使用时机兼容；传入一个“看起来同平台”但实际上不兼容的上下文，问题常在纹理或着色器创建时才暴露。

## 生命周期与线程边界

- `QOpenGLContext` 必须先成功创建，才有可查询的底层上下文。
- 一个 OpenGL 上下文同一时刻只能在一个线程中 current。`QCocoaGLContext` 不改变 `makeCurrent()`、`doneCurrent()` 和 `moveToThread()` 的规则。
- 通过 Qt 创建的上下文应由 Qt 控制其销毁顺序；原生 API 只是补充访问通道。
- 原生接口 API 可能随 Qt 版本发生源码或二进制不兼容。把它收敛在少量 `.mm` 平台适配文件中。

## 常见错误

### 将 `nativeContext()` 的返回值当成所有权转移

它只是借用的底层对象。手动释放会导致 Qt 后续使用悬空的 Cocoa 上下文。

### 在所有平台包含或调用 Cocoa 类型

`QCocoaGLContext` 仅在 macOS 上可用。用 `Q_OS_MACOS` 隔离声明和实现，避免 Linux、Windows 或移动端构建失败。

### 以为包装后不必遵守 OpenGL current 规则

`fromNative()` 只建立 Qt 包装关系，不会自动让上下文在正确线程中 current。渲染前仍应按照 `QOpenGLContext` 的线程和 surface 约束执行。

## API 速查表

| 类别 | API | 语义 | 边界与注意点 |
| --- | --- | --- | --- |
| 获取接口 | `context->nativeInterface<QNativeInterface::QCocoaGLContext>()` | 从 Qt OpenGL 上下文查询 macOS 原生接口。 | 仅 macOS；可能返回 `nullptr`；接口对象由 Qt 管理。 |
| 静态工厂 | `QOpenGLContext *fromNative(NSOpenGLContext *context, QOpenGLContext *shareContext = nullptr)` | 包装已有的 Cocoa OpenGL 上下文，并可指定 Qt 共享上下文。 | Qt 会保留/接管传入原生上下文；返回的 `QOpenGLContext` 由调用方管理；`shareContext` 必须兼容。 |
| 成员函数 | `NSOpenGLContext *nativeContext() const` | 返回底层 Cocoa OpenGL 上下文。 | 借用指针；不得释放；不能在 Qt 上下文销毁后使用。 |

## 一句话总结

`QCocoaGLContext` 用于在 macOS 的 Qt OpenGL 上下文和 `NSOpenGLContext` 之间互通；让 Qt 继续管理上下文生命周期，并把原生访问限制在必要的 Cocoa 适配层。
