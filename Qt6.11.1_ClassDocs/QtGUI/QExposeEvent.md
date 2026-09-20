# QExposeEvent

> Qt 6.11.1 · Qt GUI · 来自 `QExposeEvent`

## 1. 先建立直觉

`QExposeEvent` 表示一个 `QWindow` 的部分区域已经暴露、需要能够呈现内容。窗口从被遮挡变为可见、最小化后恢复、移动到另一个屏幕或系统要求重新显示时，都可能出现 expose 事件。

它与 `QPaintEvent` 很像，但使用层级不同：`QPaintEvent` 面向 `QWidget` 和 `QPainter` 的重绘；`QExposeEvent` 面向 `QWindow`、OpenGL、Vulkan、QRhi 等底层窗口渲染。后者要先确认窗口是否真正 exposed，再安排渲染。

## 2. 类说明

`QExposeEvent` 继承自 `QEvent`，带有暴露区域。常见于重写 `QWindow::exposeEvent()` 的窗口渲染代码。

类说明只用于表明这个 API 来自 `QExposeEvent`：具体交换缓冲、提交帧、创建渲染目标等由 OpenGL、Vulkan、QRhi 或自定义渲染后端完成。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QExposeEvent(exposeRegion)` | 构造带局部暴露区域的 expose 事件。 |
| `region()` | 继承/关联的暴露区域信息，用于评估需要重新呈现的范围。 |
| `type()` | 来自 `QEvent`，通常为 `QEvent::Expose`。 |
| `QWindow::isExposed()` | 与事件配合，判断窗口当前是否适合提交可见帧。 |

## 4. 关键用法

### 只有 exposed 时提交帧

```cpp
void RenderWindow::exposeEvent(QExposeEvent *event)
{
    Q_UNUSED(event);

    if (isExposed())
        renderNow();
}
```

当窗口未暴露时，继续渲染并交换帧通常没有用户可见收益，还可能浪费 GPU/CPU。

### expose 是“允许呈现”的信号，不是唯一重绘来源

动画、输入、定时器或数据更新也会要求重新渲染。一个健壮的 `QWindow` 渲染器通常维护 `renderLater()` 请求，在窗口 exposed 时消费它；窗口重新 exposed 时，再补上一帧。

```cpp
void RenderWindow::renderLater()
{
    if (!m_updatePending) {
        m_updatePending = true;
        QCoreApplication::postEvent(this, new QEvent(QEvent::UpdateRequest));
    }
}
```

## 5. 使用场景

`QExposeEvent` 适合 OpenGL 窗口、Vulkan 窗口、QRhi 渲染窗口、游戏工具、视频输出窗口、无 Widgets 的高性能可视化程序。

使用 `QWidget` 和 `paintEvent()` 的普通应用通常不需要直接处理它。混合使用时应明确每个渲染表面属于 Widget 绘制还是 QWindow 渲染，避免在错误的生命周期里创建渲染器。

## 6. 常见坑与经验

不要把 expose 事件当作 resize 事件。窗口暴露不代表尺寸改变；渲染目标大小仍要在 resize 或 surface 状态变化时更新。

不要在 `isExposed()` 为 false 时盲目交换缓冲。最小化、被系统隐藏时通常应暂停或合并渲染请求。

不要假设 expose 区域总能让你的 GPU 后端做精确局部重绘。许多渲染器仍以整个 swapchain 图像为单位工作，区域更多是调度提示。

不要在 exposeEvent 里阻塞等待 GPU。窗口系统事件应尽快返回，耗时渲染应使用适当帧循环与异步资源准备。

## 7. 知识点覆盖

学习 `QExposeEvent` 应覆盖 `QWindow` 生命周期、exposed 状态、Widget paint 与 Window rendering 的区别、帧调度、交换缓冲、OpenGL/Vulkan/QRhi、最小化渲染暂停和窗口可见性。
