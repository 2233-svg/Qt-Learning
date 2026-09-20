# QSurfaceFormat
> Qt 6.11.1 · Qt GUI · 来自 `QSurfaceFormat`

## 1. 先建立直觉

`QSurfaceFormat` 是窗口或离屏 surface 的图形格式请求：颜色/深度/模板位数，OpenGL 版本和 profile，MSAA samples，swap 行为，调试上下文，颜色空间等。

它不是“保证书”，更像“向平台申请的配置”。实际拿到什么，要看平台、驱动和窗口系统。

## 2. 类说明

- 头文件：`#include <QSurfaceFormat>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 类型：值类型
- 协作类：`QWindow`、`QOffscreenSurface`、`QOpenGLContext`、`QSurface`

全局默认格式应在创建 `QGuiApplication` 后、创建任何窗口或 OpenGL context 前尽早设置；很多平台一旦创建底层资源，后改格式就不再影响已有对象。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `setDefaultFormat()` / `defaultFormat()` | 设置或读取全局默认 surface format |
| `setVersion()` / `version()` | 设置或读取 OpenGL 主次版本 |
| `setMajorVersion()` / `setMinorVersion()` | 分别设置版本 |
| `setProfile()` / `profile()` | 设置 OpenGL core/compatibility/no profile |
| `setRenderableType()` / `renderableType()` | 指定 OpenGL、OpenGLES、OpenVG 或默认 |
| `setSamples()` / `samples()` | 设置 MSAA 采样数 |
| `setDepthBufferSize()` / `depthBufferSize()` | 设置深度缓冲位数 |
| `setStencilBufferSize()` / `stencilBufferSize()` | 设置模板缓冲位数 |
| `setRed/Green/Blue/AlphaBufferSize()` | 设置颜色通道位数 |
| `hasAlpha()` | 是否请求或拥有 alpha 通道 |
| `setSwapBehavior()` / `swapBehavior()` | 单/双/三缓冲策略 |
| `setSwapInterval()` / `swapInterval()` | 垂直同步间隔 |
| `setColorSpace()` / `colorSpace()` | 设置颜色空间，如 sRGB/HDR 相关输出 |
| `setOption()` / `testOption()` | 设置或查询 debug、stereo、protected content 等选项 |

## 4. 枚举速查

| 枚举 | 说明 |
| --- | --- |
| `DebugContext` | 请求 OpenGL debug context，便于调试输出 |
| `DeprecatedFunctions` | 请求兼容旧 OpenGL 废弃函数 |
| `ResetNotification` | 请求上下文丢失通知 |
| `ProtectedContent` | 请求受保护内容支持，主要 EGL 场景 |
| `StereoBuffers` | 请求立体缓冲 |
| `CoreProfile` | OpenGL core profile |
| `CompatibilityProfile` | OpenGL compatibility profile |
| `OpenGL` / `OpenGLES` | 桌面 OpenGL 或 OpenGL ES |
| `SingleBuffer` / `DoubleBuffer` / `TripleBuffer` | 交换链缓冲策略 |

## 5. 关键用法

请求 OpenGL 4.5 core debug context：

```cpp
QSurfaceFormat fmt;
fmt.setVersion(4, 5);
fmt.setProfile(QSurfaceFormat::CoreProfile);
fmt.setOption(QSurfaceFormat::DebugContext);
fmt.setDepthBufferSize(24);
fmt.setStencilBufferSize(8);
fmt.setSamples(4);
QSurfaceFormat::setDefaultFormat(fmt);
```

对单个窗口设置：

```cpp
QWindow window;
window.setSurfaceType(QSurface::OpenGLSurface);
window.setFormat(fmt);
window.create();
```

创建后应读取实际格式：

```cpp
QSurfaceFormat actual = window.format();
```

不要只看请求值判断能力。

## 6. 使用场景

- 创建 OpenGL core profile 应用。
- 开启 MSAA、深度模板缓冲。
- 启用 OpenGL debug 输出和上下文丢失检测。
- 设置 OpenGL ES 而非桌面 OpenGL。
- 请求 sRGB 或特定颜色空间的 surface。
- 调整 swap interval 来控制 vsync 行为。

## 7. 常见坑与经验

- `setDefaultFormat()` 要早；已有窗口和 context 不会自动重建。
- `samples()` 请求 4 不代表实际就是 4，平台可能降级。
- OpenGL 3.2 以下 profile 设置通常无意义。
- `swapInterval(0)` 不一定能关闭 vsync，驱动和平台可能强制策略。
- `DebugContext` 只是请求，真正调试还要结合 `QOpenGLDebugLogger` 或后端调试层。
- 三缓冲可能降低掉帧但增加延迟和内存，别当无脑优化。

## 8. 知识点覆盖

本页覆盖：OpenGL 版本/profile、颜色/深度/模板缓冲、MSAA、swap behavior、vsync、debug context、颜色空间、实际格式协商。
