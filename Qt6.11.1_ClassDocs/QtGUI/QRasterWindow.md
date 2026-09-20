# QRasterWindow

> Qt 6.11.1 · Qt GUI · 来自 `QRasterWindow`

## 1. 先建立直觉

`QRasterWindow` 是一个可以用 `QPainter` 做 raster 绘制的 `QWindow`。它适合想直接使用 Qt GUI 的窗口系统和绘图能力、但不想引入 QWidget 控件树的场景。和 `QWidget` 不同，它没有布局、子控件、style 控件绘制那套高层设施；和 `QOpenGLWindow` 不同，它的绘制目标是 raster paint engine。

你可以把它看作“一个轻量窗口 + 一个可被 `QPainter` 绘制的表面”。需要按钮、表格、复杂控件时用 Widgets；需要底层窗口、简单 2D 绘图、嵌入自定义渲染循环时再考虑它。

## 2. 类说明

- 头文件：`#include <QRasterWindow>`
- CMake：`Qt6::Gui`
- 继承自：`QPaintDeviceWindow`
- 使用方式：重写绘制相关事件，在其中使用 `QPainter`
- 父对象：构造函数接收 `QWindow *parent`

`QRasterWindow` 属于 Qt GUI 层，不是 Qt Widgets 层。它仍然要在 GUI 线程使用，并由窗口系统事件驱动重绘；改变内容后通常请求更新，而不是手动调用绘制函数。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `QRasterWindow(QWindow *parent = nullptr)` | 创建一个 raster 绘制窗口，可指定父窗口。 |
| 继承的 `QWindow` API | 控制窗口标题、大小、可见性、屏幕、事件等。 |
| 继承的 `QPaintDeviceWindow` 能力 | 让窗口成为 `QPainter` 可绘制的 paint device。 |

## 4. 关键用法

### 创建一个自绘窗口

```cpp
class CanvasWindow : public QRasterWindow
{
protected:
    void paintEvent(QPaintEvent *) override
    {
        QPainter p(this);
        p.fillRect(0, 0, width(), height(), Qt::white);
        p.setRenderHint(QPainter::Antialiasing);
        p.drawEllipse(QRectF(20, 20, 120, 80));
    }
};
```

绘制代码和 QWidget 的 `paintEvent()` 很像，但窗口类型完全不同：这里没有 QWidget parent/child 布局系统。

### 何时选它

如果界面主体是一个画布、可视化面板、简单仪表或自绘窗口，且不需要 QWidget 控件树，`QRasterWindow` 比 `QWidget` 更贴近底层窗口模型。如果你要混用大量标准控件，还是用 QWidget 更省心。

## 5. 使用场景

- 独立 2D 绘图窗口。
- 教学、调试或工具类可视化窗口。
- 不需要控件树的简单 raster 画布。
- 需要直接使用 `QWindow` 特性但仍想用 `QPainter` 绘制。
- 和其他底层窗口/渲染系统组合时的轻量 Qt 绘图层。

## 6. 常见坑与经验

- **它不是 QWidget。** 不能加入 `QLayout`，也没有 QWidget 的 style、child widget、size policy 语义。
- **绘制仍然事件驱动。** 内容变化时请求更新，不要把绘制函数当普通业务函数直接调用。
- **GUI 线程限制仍然存在。** 不要从 worker 线程直接访问窗口或绘制到窗口。
- **复杂 UI 不适合硬写在这里。** 一旦需要按钮、输入框、菜单、表格，Widgets 或 Qt Quick 更合适。
- **高 DPI 要按逻辑坐标处理。** 和其他 Qt 绘制一样，注意 device pixel ratio 与资源尺寸。

## 7. 知识点覆盖

- `QWindow`、`QPaintDeviceWindow` 与 raster 绘制的关系
- `QRasterWindow` 和 `QWidget`、`QOpenGLWindow` 的选择边界
- `QPainter` 在底层窗口上的绘制生命周期
- GUI 线程、更新请求、高 DPI 与 paint device
- 轻量自绘窗口的组织方式
