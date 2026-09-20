# QPaintDeviceWindow

> Qt 6.11.1 · Qt GUI · 来自 `QPaintDeviceWindow`

## 1. 先建立直觉

`QPaintDeviceWindow` 把 `QWindow` 变成可以由 `QPainter` 直接绘制的窗口表面。它是 `QRasterWindow` 与 `QOpenGLWindow` 的共同基类，适合不使用 QWidget 层级、但仍想拥有窗口生命周期、曝光事件和局部重绘调度的场景。

它不等于 `QWidget`。没有 widget layout、样式系统或子控件树；你负责窗口内容与重绘模型。若只是做常规桌面 UI，优先用 Widgets 或 Qt Quick；若写一个独立绘图窗口/渲染视图，才考虑这一层。

## 2. 类说明

- 头文件：`#include <QPaintDeviceWindow>`
- CMake：`target_link_libraries(app PRIVATE Qt6::Gui)`
- 继承：`QWindow` 和 `QPaintDevice`。
- 直接派生：`QRasterWindow`、`QOpenGLWindow`。
- 重绘入口：重载保护函数 `paintEvent(QPaintEvent *)`；请求重绘用 `update()`，绝不手动直接调用 `paintEvent()`。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `update()` | 标记整个窗口脏，异步合并并安排绘制事件 |
| `update(QRect)` | 标记一个逻辑矩形脏，适合小区域变化 |
| `update(QRegion)` | 标记多个不连续区域脏 |
| `paintEvent(QPaintEvent *)` | 重载并在收到窗口系统重绘事件时实际绘制 |
| `QPaintEvent::region()` | 取得本次需要更新的脏区域 |
| `QPaintEvent::rect()` | 取得脏区域的包围矩形 |
| `QWindow::exposeEvent()` | 与窗口暴露/隐藏状态协作；不是普通每帧绘制回调 |
| `QWindow::isExposed()` | 判断窗口是否当前可见于屏幕 |

## 4. 关键用法

### 用 update 调度绘制

```cpp
class PlotWindow : public QPaintDeviceWindow
{
protected:
    void paintEvent(QPaintEvent *event) override
    {
        QPainter p(this);
        p.setClipRegion(event->region());
        drawPlot(p, event->region());
    }

public:
    void setSeries(Series series)
    {
        m_series = std::move(series);
        update(); // 合并到事件循环中的下一次绘制
    }
};
```

`update()` 不会立即执行绘制。Qt 会合并同一轮事件循环中的多个脏区域，再投递 `paintEvent()`；这正是避免拖动/数据变化时发生大量重复绘制的机制。

### 只重绘受影响区域

```cpp
void PlotWindow::hoverPointChanged(QPointF oldPos, QPointF newPos)
{
    const QRegion dirty(markerRect(oldPos).toAlignedRect());
    update(dirty | markerRect(newPos).toAlignedRect());
}
```

局部 update 只有在 `paintEvent()` 真正尊重脏区域时才有收益。使用 `event->region()` 设置 clip，或让绘制函数只遍历与该区域相交的项目；每次仍然整窗绘制会把局部更新变成徒有其表。

### 正确处理未暴露窗口

```cpp
void PlotWindow::setLiveData(Data data)
{
    m_data = std::move(data);
    update();
}
```

即使窗口还未暴露，也可以更新业务状态并请求重绘。Qt 可能在窗口可见前/后发送 paint event，未暴露时也可能推迟真正绘制；不要将“只有 `isExposed()` 为真才更新模型”作为条件。

## 5. 使用场景

- `QRasterWindow` 基础上的轻量 2D 可视化、仪表盘、绘图工具。
- `QOpenGLWindow` 中需要窗口系统事件、CPU/GL 混合绘制的独立窗口。
- 没有 widget 层级、只需单一渲染表面的专用桌面窗口。
- 使用 `QWindow` API 管理多屏、曝光和原生窗口属性的绘制应用。

## 6. 常见坑与经验

- **不要直接调用 `paintEvent()`。** 它绕过脏区合并、窗口系统调度和设备准备；状态改变后调用 `update()`。
- **不要在 paintEvent 中变更会触发下一次 update 的业务状态。** 这会形成无休止重绘循环。绘制应该读取模型，模型更新在事件/定时器回调中完成。
- **绘制只在所属 GUI 线程。** 后台可准备 `QImage`、路径或数据，但将结果投递到窗口线程，再 `update()`。
- **窗口暴露不等于尺寸稳定。** 同时处理 `resizeEvent()`、DPR/屏幕变化，丢弃与旧尺寸不匹配的缓存。
- **局部区域是提示而非借口。** 当背景有透明、混合、阴影或相互依赖图层时，要把必要的扩展区域一并标脏。
- **选择对的派生类。** 软件 2D 绘制用 `QRasterWindow`；OpenGL 上下文/帧机制用 `QOpenGLWindow`；它们会处理各自更具体的设备细节。

## 7. 知识点覆盖

QWindow 绘制、异步重绘、脏区域、局部裁剪、曝光事件、GUI 线程、缓存失效、窗口尺寸/DPR 变化、QRasterWindow、QOpenGLWindow。
