# Qt QExposeEvent 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QExposeEvent>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QEvent -> QExposeEvent`  
> 定位：窗口暴露或遮挡状态变化时的通知事件

## 1. 它解决什么问题

`QExposeEvent` 通知 `QWindow`：窗口可见区域的暴露状态发生了变化，应用现在可能需要开始、恢复或停止渲染。它常见于窗口首次显示、从被完全遮挡状态重新出现、最小化后恢复，或平台改变窗口可见性时。

它解决的不是 QWidget 的局部重绘问题。Widgets 应使用 `QWidget::paintEvent(QPaintEvent *)` 与 `QPaintEvent::region()`；`QExposeEvent::region()` 在 Qt 6 已弃用，官方建议改为处理 `QPaintEvent`。

实际场景：

- `QWindow` 的 OpenGL、Vulkan 或 RHI 渲染循环只在窗口暴露时提交帧；
- 原生窗口恢复可见时重建或刷新交换链内容；
- 在窗口完全不可见时暂停昂贵动画或渲染任务。

## 2. 事件入口

```cpp
#include <QExposeEvent>
#include <QWindow>

class RenderWindow : public QWindow
{
protected:
    void exposeEvent(QExposeEvent *event) override
    {
        Q_UNUSED(event);
        if (isExposed())
            renderNow();
    }
};
```

关键查询来自 `QWindow::isExposed()`，而不是事件对象本身。事件只说明状态有变化；实际是否应渲染，要在处理时检查窗口当前状态。

在 Widgets 中若看到 `QExposeEvent`，通常不应据此写绘制逻辑。将重绘代码放在 `paintEvent()`，使用 `update()` 请求延后重绘。

## 3. 暴露、可见与生命周期不是一回事

`isExposed()` 为假不等于窗口已经销毁，也不等于图形资源一定不可用。它表示窗口没有可见区域，持续提交帧通常没有意义；是否释放图形资源还取决于 `QPlatformSurfaceEvent`、图形 API 及应用的恢复策略。

反过来，窗口 `show()` 后也不意味着立刻已有可绘制暴露区域。渲染初始化应能容忍先收到大小变化、平台表面创建或 expose 事件中的任意顺序。

不要把 expose 事件当成固定帧率回调。连续动画应使用定时器、渲染循环或帧同步机制驱动，expose 只用于根据可见性启动或暂停。

## 4. 旧 `region()` API 的边界

Qt 6 中 `QExposeEvent::region()` 已弃用，文档明确建议处理 `QPaintEvent`。它不适合让 `QWindow` 实现精细的局部失效绘制策略。

如果代码来自 Qt 5：

```cpp
void MyWindow::exposeEvent(QExposeEvent *event)
{
    repaint(event->region()); // Qt 6 中不应继续依赖
}
```

应重新设计为基于 `QWindow::isExposed()` 的完整帧渲染，或若组件本质是 QWidget，则迁移到 `paintEvent()`。

## 5. 线程与性能

`exposeEvent()` 在窗口所属 GUI 线程执行。GUI 或图形上下文相关对象不能由后台线程直接操作；后台线程可以准备数据，但资源提交、窗口状态读取和上下文绑定必须遵守所用图形 API 的线程规则。

完全遮挡时暂停 GPU 提交可减少资源消耗，但恢复时必须能处理尺寸变化、swap chain 失效或表面重建。不要仅凭一次 expose 事件永久假设窗口一直可见。

## 6. 常见错误

- 用 `QExposeEvent` 替代 QWidget 的 `paintEvent()`；
- 忽略 `isExposed()`，在不可见窗口上持续渲染；
- 把 expose 当作定时帧回调；
- 使用已弃用的 `region()` 制定新的 Qt 6 代码；
- 可见性变化时就释放全部资源，恢复时无法重建；
- 从工作线程处理窗口或图形上下文。

## 7. 逐项 API 说明

### `explicit QExposeEvent(const QRegion &exposeRegion)`

构造暴露事件。主要用于 Qt 内部或测试；`exposeRegion` 是旧接口所携带的暴露区域。正常 `QWindow` 实现不应依赖手工构造事件来模拟平台可见性状态。

### 从 `QEvent` 继承的常用成员

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `type() const` | 查询事件类型。 | 正常为 `QEvent::Expose`。 |
| `accept()` / `ignore()` | 设置事件处理状态。 | 不改变窗口实际是否暴露。 |
| `isAccepted() const` | 查询接受状态。 | 不能替代 `QWindow::isExposed()`。 |

### 已弃用成员

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `const QRegion &region() const` | 读取旧的暴露区域。 | Qt 6 已弃用；Widgets 使用 `QPaintEvent::region()`，QWindow 使用 `isExposed()`。 |

## API 速查表

| 类别 | API | 解决什么问题 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QExposeEvent(const QRegion &)` | 手动创建暴露事件。 | 主要用于测试，不模拟完整平台状态。 |
| 窗口状态 | `QWindow::isExposed()` | 判断当前是否值得渲染。 | 在 `exposeEvent()` 中检查真实当前状态。 |
| 事件入口 | `QWindow::exposeEvent()` | 响应窗口暴露变化。 | 不是固定帧率渲染回调。 |
| 兼容 | `region()` | 读取旧暴露区域。 | Qt 6 已弃用。 |
| 事件状态 | `accept()` / `ignore()` | 设置处理状态。 | 不改变暴露状态。 |

---

### 一句话总结

`QExposeEvent` 是 `QWindow` 可见性变化的渲染提示：用 `isExposed()` 决定是否出帧，局部 QWidget 重绘仍应交给 `QPaintEvent`。
