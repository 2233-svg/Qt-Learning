# Qt QRasterWindow 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QRasterWindow>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QPaintDeviceWindow -> QWindow`，同时实现 `QPaintDevice`  
> 定位：在原生 `QWindow` 上直接使用 `QPainter` 的 CPU 栅格窗口

## 1. 它解决什么问题

`QWindow` 代表一个窗口表面，但单独继承 `QWindow` 时，使用 `QPainter` 绘制需要自己管理 `QBackingStore`：窗口暴露时机、后备缓冲区尺寸、绘制区域、`beginPaint()`/`endPaint()` 和最终 `flush()` 都要自己串起来。

`QRasterWindow` 把这套栅格绘制基础设施封装起来，使子类可以像写普通绘制窗口一样，在 `paintEvent()` 中直接构造 `QPainter`：

```cpp
void paintEvent(QPaintEvent *event) override
{
    QPainter painter(this);
    painter.setClipRegion(event->region());
    painter.fillRect(event->rect(), Qt::white);
}
```

它的底层仍然是 `QWindow` 和 `QBackingStore`，绘制引擎是 raster，绘制工作主要由 CPU 完成。这个类的价值是减少窗口后端管理代码，而不是提供 GPU 加速。

如果核心需求是 OpenGL 上下文、纹理、着色器或 GPU 渲染，应选择 `QOpenGLWindow`；如果需要成熟的控件布局、样式和事件体系，通常应选择 `QWidget` 或 Qt Quick，而不是直接使用 `QRasterWindow`。

## 2. 真实使用场景

### 2.1 轻量级原生绘图窗口

适合做图表、波形、示波器画布、简单图像查看器、绘图工具或设备监视面板。这些场景通常希望直接控制绘制流程，又不想引入 `QWidget` 层级或 OpenGL 管线。

### 2.2 复用 `QPainter` 的现有绘图代码

如果已有绘制代码面向 `QPainter`，可以把它放进窗口子类的 `paintEvent()`，继续使用字体、路径、渐变、图片和区域裁剪等 Qt 绘图能力。

### 2.3 作为自定义渲染基础类

可以在 `QRasterWindow` 上增加模型状态、定时器和交互事件。状态变化后调用 `update()`，Qt 会在事件循环中安排后续绘制，而不是要求业务代码直接操纵后备缓冲区。

## 3. 最小可用示例

`QRasterWindow` 需要在 `QGuiApplication` 的事件循环中运行。窗口创建后要设置尺寸并显示；绘制则重写继承来的 `paintEvent()`：

```cpp
#include <QGuiApplication>
#include <QPainter>
#include <QPaintEvent>
#include <QRasterWindow>

class PaintWindow final : public QRasterWindow
{
public:
    explicit PaintWindow(QWindow *parent = nullptr)
        : QRasterWindow(parent)
    {
        resize(480, 320);
    }

protected:
    void paintEvent(QPaintEvent *event) override
    {
        QPainter painter(this);
        painter.setRenderHint(QPainter::Antialiasing);
        painter.fillRect(event->rect(), QColor("#18222d"));
        painter.setPen(Qt::white);
        painter.drawText(rect(), Qt::AlignCenter, QStringLiteral("QRasterWindow"));
    }
};

int main(int argc, char **argv)
{
    QGuiApplication app(argc, argv);
    PaintWindow window;
    window.show();
    return app.exec();
}
```

这里的 `event->rect()` 是本次绘制事件的矩形脏区。示例只填充该区域，避免无条件重绘整个窗口；如果绘制内容依赖整个画布状态，也可以使用 `event->region()` 设置裁剪区域后重绘必要对象。

## 4. 使用模型：更新状态，再请求重绘

一个典型子类会把“改变数据”和“绘制数据”分开：

```cpp
class PlotWindow final : public QRasterWindow
{
public:
    void setSamples(QVector<QPointF> samples)
    {
        m_samples = std::move(samples);
        update();
    }

protected:
    void paintEvent(QPaintEvent *event) override
    {
        QPainter painter(this);
        painter.setClipRegion(event->region());
        painter.fillRect(event->rect(), Qt::black);
        painter.setPen(Qt::green);
        if (m_samples.size() >= 2)
            painter.drawPolyline(m_samples);
    }

private:
    QVector<QPointF> m_samples;
};
```

要点如下：

- `update()` 只标记内容过期并安排绘制，不会同步执行 `paintEvent()`。
- 在下一次绘制事件之前多次调用 `update()`，Qt 会合并请求；矩形或区域重载会把新的脏区域并入待更新区域。
- `paintEvent()` 中使用 `QPainter painter(this)`，绘制设备就是窗口本身，不需要应用代码显式创建 `QBackingStore`。
- `QPaintEvent` 的区域是优化线索，不是“只允许绘制这些像素”的替代品。若某个对象改变后会影响更大区域，应请求覆盖完整受影响区域。
- 不要在 `paintEvent()` 中修改会再次无条件触发 `update()` 的状态，否则容易形成持续重绘。

## 5. 关键语义与边界

### 5.1 这是 raster 窗口，不是 OpenGL 窗口

`QRasterWindow` 使用 CPU 栅格引擎。它适合 `QPainter` 的传统 2D 绘制，但不会因为窗口类叫“Window”就自动获得 GPU 加速。需要 OpenGL 的代码应使用 `QOpenGLWindow`，不能把 OpenGL 上下文 API 当成 `QRasterWindow` 的绘制接口。

### 5.2 `paintEvent()` 才是绘制入口

`QPaintDeviceWindow::paintEvent(QPaintEvent *)` 的默认实现不绘制任何内容。子类应重写它，并在其中打开 `QPainter`。不要把 `exposeEvent()` 当成普通绘制函数：

- `exposeEvent()` 用于观察窗口是否暴露给窗口系统。
- `isExposed()` 为 `false` 时，窗口可能已隐藏、最小化、移出屏幕或被完全遮挡。
- Qt 的 `QPaintDeviceWindow` 负责把需要重绘的内容转成绘制事件；绘制逻辑应放进 `paintEvent()`。

通常可以在 `paintEvent()` 中直接绘制，不需要自己判断 `isExposed()`；窗口系统会在适当时机发送绘制事件。若应用另有持续动画或昂贵计算，应使用 `isExposed()` 限制这些活动。

### 5.3 初始化尺寸和显示

窗口默认不可见。创建后需要调用 `resize()` 或 `setGeometry()`，再调用 `show()`、`showMaximized()` 等可见性 API。

如果只想指定尺寸而让窗口系统决定位置，使用 `resize()`；`setGeometry(x, y, w, h)` 会同时初始化位置和尺寸。第一次显示前会先收到 resize 事件，之后才可能收到 expose 事件。

### 5.4 逻辑坐标与设备像素

`width()`、`height()` 和 `QPaintEvent` 的几何信息使用窗口的逻辑坐标。高 DPI 屏幕上，底层后备缓冲区可能拥有更多设备像素；不要手工把逻辑尺寸乘 `devicePixelRatio()` 后再传给 `QPainter`，除非你正在操作明确以设备像素为单位的外部资源。

如果绘制图片、缓存或离屏内容，要检查对应资源的设备像素比，避免在高 DPI 下重复缩放或产生模糊。

### 5.5 绘制生命周期

`QPainter` 必须只在 `paintEvent()` 的同步调用范围内使用，并在离开函数前结束。不要把指向窗口或 painter 状态的引用保存到异步任务中，也不要跨事件循环持有活动的 `QPainter`。

窗口销毁时，Qt 会清理其内部后备缓冲区。`QRasterWindow` 不可拷贝，不能把它按值放入容器或通过赋值复制；通常以栈对象、父对象管理的对象或智能指针管理其生命周期。

### 5.6 线程边界

`QWindow`、`QPainter` 对窗口本身的绘制以及 GUI 事件分发属于 GUI 线程模型。工作线程可以计算绘图数据、生成独立的 `QImage` 等资源，再通过信号槽把结果交给窗口线程；不要在工作线程直接对 `QRasterWindow` 打开 painter 或调用窗口更新相关 API。

## 6. 与手工 `QBackingStore` 方案的关系

直接继承 `QWindow` 时，典型流程需要自己完成：

1. 在构造函数中创建 `QBackingStore`。
2. 在 resize 事件中同步后备存储尺寸。
3. 在合适的暴露状态下调用 `beginPaint()`。
4. 从 `paintDevice()` 获取临时有效的绘制设备并创建 `QPainter`。
5. 调用 `endPaint()`，再调用 `flush()` 把区域提交到窗口。

`QRasterWindow` 把这条路径放入内部实现，并对外提供 `QPaintDevice` 接口和 `paintEvent()`。因此它适合常规的窗口绘制；只有需要自定义 backing store 调度、特殊子窗口刷新或极细粒度提交策略时，才有必要回到 `QWindow + QBackingStore` 的手工方案。

`QBackingStore::paintDevice()` 返回的设备只在 `beginPaint()` 与 `endPaint()` 之间有效；这是手工方案的生命周期约束，不应把从中取得的指针缓存起来。使用 `QRasterWindow` 时，应用代码不应绕过它的内部实现去操作未公开的后备存储。

## 7. 继承与覆盖建议

### 7.1 通常只需重写 `paintEvent()`

最小子类一般只需要：

```cpp
protected:
    void paintEvent(QPaintEvent *event) override;
```

在实现中使用 `QPainter painter(this)`，并根据 `event->rect()` 或 `event->region()` 限制绘制范围。

### 7.2 何时使用 `resizeEvent()`

如果子类拥有与窗口尺寸相关的缓存，例如预计算网格、布局结果或离屏 `QImage`，可以重写 `resizeEvent()` 更新这些数据。覆盖时要调用 `QRasterWindow::resizeEvent(event)`，让基类完成内部后备存储的尺寸处理。

仅为了调整窗口内部绘制坐标时，通常不需要重写 resize 事件，直接在 `paintEvent()` 中读取 `size()` 即可。

### 7.3 不要把 protected 内部扩展点当作普通业务 API

`metric(PaintDeviceMetric)` 和 `redirected(QPoint *)` 是 `QPaintDevice`/`QPaintDeviceWindow` 的绘制设备内部扩展点。它们服务于 Qt 的绘制引擎和设备转发，不是一般应用用来改变窗口行为的 setter。除非正在实现特殊的绘制设备包装，否则不应重写。

## 8. 常见错误与排查

### 窗口显示了但没有内容

检查是否创建了 `QGuiApplication`、调用了 `show()`、进入了 `app.exec()`，以及子类是否真的重写了 `paintEvent()`。只构造 `QRasterWindow` 不会自动显示窗口，也不会自动绘制业务内容。

### 在 `paintEvent()` 外直接绘制

不要把窗口当成任意时刻都可写的画布。状态变化时调用 `update()`，让 Qt 在绘制事件中重新绘制。把 `QPainter` 保存为成员或在定时器回调里长期持有，都会破坏绘制生命周期。

### 每次都画完整窗口导致卡顿

读取 `QPaintEvent::region()` 或 `rect()`，对绘制设置裁剪，并让状态变化只请求真正受影响的区域。若场景本身每帧都会变化，区域优化收益有限，此时应评估绘制内容、帧率和是否需要 GPU 后端。

### 把它当作 `QWidget`

`QRasterWindow` 是 `QWindow`，没有 QWidget 的父子控件布局、样式表和 `QWidget` 事件语义。需要把窗口嵌入 widget 层级时，应使用适合的窗口容器方案，而不是假设二者可以互换。

## 9. 逐项 API 说明

### `QRasterWindow::QRasterWindow(QWindow *parent = nullptr)`

**作用：** 构造一个使用 raster 绘制表面的窗口对象。

**参数语义：**

- `parent == nullptr`：通常创建顶层窗口，具体窗口类型和平台行为仍受 `QWindow` 默认设置影响。
- 非空 `parent`：把该窗口作为父窗口的 native child window；父对象销毁时，Qt 对象树会负责销毁子对象。

**关键边界：**

- 构造函数是 `explicit`，不能把 `QWindow *` 隐式转换成 `QRasterWindow`。
- 构造完成后窗口仍默认不可见，需要显式调用 `show()` 或其他可见性 API。
- 构造函数不替代 `QGuiApplication`，也不替代事件循环。
- 类不可拷贝；不要尝试复制窗口实例。

### `QRasterWindow::~QRasterWindow()`

**作用：** 销毁窗口及其由类内部管理的栅格绘制资源。

**使用边界：**

- 不要在析构后继续使用窗口指针、绘制设备或关联的异步回调。
- 如果窗口由父 `QWindow` 管理，通常不需要手动 `delete`；独立创建的对象则必须保证生命周期覆盖所有事件处理。

### `QPaintDeviceWindow::paintEvent(QPaintEvent *event)`

**作用：** 处理窗口内容需要更新时收到的绘制事件。`QRasterWindow` 子类通常重写此函数作为唯一绘制入口。

**参数与脏区：**

- `event->rect()` 返回本次事件的包围矩形。
- `event->region()` 返回更精确的脏区域，可用于 `QPainter::setClipRegion()`。
- 事件对象由 Qt 管理，不要保存指针。

**调用约束：**

- 在函数内创建 `QPainter painter(this)`，完成绘制后让 painter 离开作用域。
- 不要把绘制工作延迟到函数返回之后。
- 默认实现不绘制业务内容；重写时如果不需要基类行为，通常不必调用基类，但若基类版本在未来承担额外行为，保守做法是按 Qt 文档和当前版本实现决定是否调用。

### `QPaintDeviceWindow::update()`

**作用：** 把整个窗口标记为脏并异步安排一次重绘。

**语义边界：**

- 不是立即调用 `paintEvent()`；请求会在事件循环中合并后交付。
- 下一次绘制事件之前的重复调用会被合并，不会保证得到同样数量的绘制事件。
- 适合在数据、动画帧或交互状态改变后调用。

### `QPaintDeviceWindow::update(const QRect &rect)`

**作用：** 只把 `rect` 标记为需要重绘的窗口区域。

**注意：**

- 在下一次绘制事件前重复调用时，区域会并入待更新区域。
- `rect` 使用窗口逻辑坐标；超出窗口的部分没有可见绘制效果。
- 如果改变一个对象会影响阴影、抗锯齿边缘或相邻内容，应把完整受影响范围加入更新区域。

### `QPaintDeviceWindow::update(const QRegion &region)`

**作用：** 以多个矩形组成的 `QRegion` 标记脏区并异步安排重绘。

**适用场景：** 需要更新多个彼此分离的图元时，区域更新比反复调用整窗 `update()` 更准确。

### `QWindow::requestUpdate()`

**作用：** 请求窗口系统在合适的时机发送更新请求，常用于需要与窗口系统刷新节奏协调的场景。

**与 `update()` 的区别：**

- `update()` 是 `QPaintDeviceWindow` 面向脏区/绘制事件的更新接口。
- `requestUpdate()` 是 `QWindow` 的更新请求机制，典型处理方式是在 `event()` 中响应 `QEvent::UpdateRequest`，或使用类自身已有的绘制调度。
- 不要把两种机制混用成两个独立的渲染循环；选择一种调度方式并保持状态更新与绘制入口清晰。

### `QWindow::show()` / `QWindow::hide()`

**作用：** 改变应用希望窗口可见或不可见的状态。

**边界：** `isVisible()` 表示应用的可见性意图；真正是否暴露在窗口系统中应查看 `isExposed()`。隐藏、最小化或被完全遮挡时，不应继续做无意义的高成本动画计算。

### `QWindow::resize(const QSize &size)` / `QWindow::setGeometry(...)`

**作用：** 设置窗口尺寸，或同时设置位置和尺寸。

**边界：**

- `resize()` 适合只指定大小并让窗口系统决定初始位置。
- `setGeometry()` 同时初始化位置和尺寸。
- 尺寸变化会触发 resize 事件；子类若维护自己的尺寸相关缓存，应在 `resizeEvent()` 中更新。

### `QWindow::isExposed() const`

**作用：** 判断窗口当前是否暴露给窗口系统、具有潜在可见性。

**不要误解：** 它不是“应用是否调用过 `show()`”的同义词。窗口可以 `isVisible() == true` 但 `isExposed() == false`，例如被完全遮挡、最小化或移出屏幕。

### `QPaintDevice::width()` / `height()` / `devicePixelRatio()`

**作用：** 查询绘制设备的逻辑尺寸和设备像素比。

**注意：** `width()`/`height()` 通常用于窗口逻辑坐标中的布局和绘制；设备像素比用于处理高 DPI 资源。不要在普通 `QPainter` 绘制中重复手动缩放窗口几何。

## API 速查表

| 类别 | API | 解决什么问题 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `explicit QRasterWindow(QWindow *parent = nullptr)` | 创建一个可由 `QPainter` 直接绘制的 raster 窗口 | 不会自动显示；需要 `QGuiApplication`、尺寸和事件循环；窗口不可拷贝 |
| 析构 | `~QRasterWindow()` | 释放窗口及内部栅格资源 | 销毁后不能继续使用窗口或其异步回调 |
| 绘制入口 | `void paintEvent(QPaintEvent *event)` | 在窗口内容需要更新时执行 `QPainter` 绘制 | 子类重写；使用 `event` 的脏区；不要保存事件或 painter |
| 全窗刷新 | `void update()` | 异步请求重绘整个窗口 | 请求会合并，不会同步调用 `paintEvent()` |
| 矩形刷新 | `void update(const QRect &rect)` | 异步请求重绘一个矩形区域 | 使用窗口逻辑坐标；受影响范围不能估小 |
| 区域刷新 | `void update(const QRegion &region)` | 异步请求重绘多个离散区域 | 适合局部、多块区域更新；Qt 会合并后续请求 |
| 系统刷新请求 | `void requestUpdate()` | 请求窗口系统在合适时机产生更新请求 | 属于 `QWindow` 机制；不要与 `update()` 混成重复调度 |
| 显示控制 | `void show()` / `void hide()` | 显示或隐藏窗口 | `isVisible()` 不等于 `isExposed()` |
| 尺寸设置 | `void resize(const QSize &size)` | 只设置窗口大小 | 适合让平台决定初始位置；会触发 resize 事件 |
| 几何设置 | `void setGeometry(...)` | 同时设置窗口位置和大小 | 位置也会被初始化，不再完全交给窗口系统 |
| 暴露状态 | `bool isExposed() const` | 判断窗口是否可能被用户看到 | 不暴露时应减少动画和昂贵图形活动 |
| 脏区矩形 | `QRect QPaintEvent::rect() const` | 获取本次绘制事件的包围矩形 | 可作为快速裁剪范围，但可能比精确区域更大 |
| 脏区区域 | `QRegion QPaintEvent::region() const` | 获取本次绘制事件的精确区域 | 可传给 `QPainter::setClipRegion()` |
| 设备尺寸 | `int width() const` / `int height() const` | 获取窗口逻辑尺寸 | 用于逻辑坐标布局；不要随意乘设备像素比 |
| 设备像素比 | `qreal devicePixelRatio() const` | 处理高 DPI 资源和设备像素换算 | 只在需要设备像素语义时使用，避免重复缩放 |

---

### 一句话总结

`QRasterWindow` 适合需要直接在原生 `QWindow` 上用 `QPainter` 做 CPU 栅格绘制的轻量场景：子类重写 `paintEvent()`，状态变化后调用 `update()`，让 Qt 负责后备缓冲和脏区调度；需要 GPU 加速时应改用 `QOpenGLWindow`。
