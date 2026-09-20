# QQuickWindow::GraphicsStateInfo：与 Qt Quick 对齐的多帧资源槽

> Qt 6.11.1 | `#include <QQuickWindow>` | CMake: `Qt6::Quick`

`QQuickWindow::GraphicsStateInfo` 是一个只有两个整数字段的只读状态快照，来自 `QQuickWindow::graphicsStateInfo()`。它解决的是原生 Vulkan/Metal 等外部渲染代码与 Qt Quick 的多帧并发策略对齐的问题：CPU 已开始录制下一帧时，前面提交的 GPU 帧可能仍在执行，不能立刻覆写仍在使用的 uniform buffer、动态顶点缓冲或描述符资源。

普通 QML 应用、纯 `QSGMaterial`/QRhi renderer 通常不需要读取它。真正的使用者是通过 `QSGRendererInterface` 直接录制 native graphics command，并且自己维护每帧变化资源的程序。

## 用帧槽索引选择自己的资源副本

```cpp
const auto &state = window->graphicsStateInfo();
auto &perFrame = m_frames[state.currentFrameSlot];

updateUniformBuffer(perFrame.uniformBuffer, parameters);
recordNativeCommands(perFrame);
```

如果 `framesInFlight` 为 2 或 3，应用至少准备同样数量的可写资源副本。`currentFrameSlot` 在 `0` 到 `framesInFlight - 1` 之间循环，用它选择本帧专属的 buffer/内存分配；不要用单份 uniform buffer 在每次 CPU 帧开始时直接覆写，否则 GPU 尚未完成旧帧时会产生数据竞争、等待或画面异常。

这不是 GPU 已完成帧数，也不是用于显示 FPS 的计数器。Qt Quick 负责限制 CPU 不会无限领先 GPU；外部代码仍须用相同的多缓冲布局管理自身的频繁更新资源。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `QQuickWindow::graphicsStateInfo()` | 取得当前窗口的帧槽信息引用 | 在需要与 scene graph frame 对齐的原生渲染阶段读取 |
| `currentFrameSlot` | 当前正在录制帧的槽索引 | 范围为 `0 .. framesInFlight - 1`，循环使用 |
| `framesInFlight` | Qt Quick 最多保持的并发 GPU 帧数 | 常见为 2 或 3；为频繁改写资源准备至少等量副本 |

## 使用边界

- 最适合 Vulkan、Metal 等显式多帧模型；OpenGL/D3D11 的此类同步细节通常由 API 实现隐藏。
- 槽位只解决“本帧用哪份资源”，不替代外部 API 对 queue、fence、layout 和资源所有权的要求。
- 若窗口重建 scene graph 或更换后端，原生资源与多帧数组都应按新的图形环境重新创建。
