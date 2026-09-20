# QQuickFramebufferObject::Renderer：在 FBO 内绘制并把状态交回 Qt Quick

> Qt 6.11.1 | `#include <QQuickFramebufferObject>` | CMake: `Qt6::Quick` | OpenGL 专用

`QQuickFramebufferObject::Renderer` 承担 FBO item 的渲染线程职责。它不直接暴露给 QML；它存在的意义是隔离 GUI 线程的 item 状态和 OpenGL render state，让自定义绘制在 Quick 的帧调度内发生。

## 正确的一帧节奏

1. GUI 线程的 item 属性改变，调用 `QQuickItem::update()`。
2. 同步阶段调用 `synchronize(item)`，此时 GUI 线程已被阻塞；复制 item 的状态到 renderer。
3. 需要时调用 `createFramebufferObject(size)` 创建或重建目标。
4. 调用 `render()`，FBO 已绑定且 viewport 已设为 FBO 尺寸。
5. `render()` 返回前恢复 Quick 依赖的 OpenGL 状态。

```cpp
void ScopeRenderer::synchronize(QQuickFramebufferObject *item)
{
    auto *scope = static_cast<ScopeItem *>(item);
    m_gain = scope->gain();
}

void ScopeRenderer::render()
{
    drawWaveform(m_gain);
    QQuickOpenGLUtils::resetOpenGLState();
}
```

`synchronize()` 是 renderer 和 item 可以相互读写成员的唯一安全点。不要用“两个线程大概不会同时访问”的假设代替这条规则。

## FBO 与 GL 状态

`createFramebufferObject(size)` 默认创建合适 FBO，也可以重写来指定格式、深度附件或 multisample。传入尺寸已考虑小 FBO 兼容性；随意固定极小尺寸并不可靠，64x64 是 Qt 文档给出的保守下限。

若请求 multisample FBO，内部会额外创建并 blit 到用于显示的 FBO。性能与显存代价因此不只取决于你返回的对象。

`render()` 开始时不保证 OpenGL state 是默认值，也不能假定该状态在两次调用间保留。Quick 与自定义代码使用同一个 context。绘制结束调用 `QQuickOpenGLUtils::resetOpenGLState()` 是最稳妥的收尾。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `synchronize(QQuickFramebufferObject *)` | 将 GUI item 状态复制到 renderer | GUI 线程此时被阻塞；是唯一安全的直接交接点 |
| `render()` | 向已绑定 FBO 发出 OpenGL 绘制 | 纯虚；viewport 已设置，但其他 GL state 不保证默认 |
| `createFramebufferObject(QSize)` | 创建/重建渲染目标 | item resize 时可能频繁调用；返回对象由 Qt 管理 |
| `framebufferObject()` | 获取当前渲染 FBO | 只在 renderer 生命周期和渲染线程内使用 |
| `invalidateFramebufferObject()` | 请求重新创建 FBO | 在 `synchronize()` 中调用 |
| `update()` | 从 renderer 请求再渲一帧 | 只在 renderer 内使用；GUI 线程请求请调用 item 的 `update()` |
| `QQuickOpenGLUtils::resetOpenGLState()` | 恢复 Quick 所需的 GL 状态 | 建议在 `render()` 结束前调用 |

## 使用边界

- `finished` 式的异步回调不能在 renderer 外随意操作 GL，context 归 scene graph 管理。
- `render()` 中创建 QObject、发信号或启计时器会产生渲染线程亲和性对象，通常不是想要的结果。
- 类本身跟随 `QQuickFramebufferObject` 的 OpenGL-only 限制。
