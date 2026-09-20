# QPaintDeviceWindow：可由 QPainter 重绘的窗口基类

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPaintDeviceWindow>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Gui)`，并链接 `Qt6::Gui`  
> 继承：`QWindow`、`QPaintDevice`  
> 常用替代：`QRasterWindow`、`QOpenGLWindow`、`QWidget`

`QPaintDeviceWindow` 是同时具备 `QWindow` 和 `QPaintDevice` 能力的便利基类。它让一个窗口可以成为 `QPainter` 的绘制目标：当窗口需要刷新时，Qt 调用虚函数 `paintEvent()`，派生类可以在该函数中创建 `QPainter` 并完成绘制。

它不是面向应用直接实例化的窗口。Qt 文档明确说明，该类主要为 `QOpenGLWindow` 等子类服务；普通光栅窗口应直接使用 `QRasterWindow`，传统控件界面则通常继承 `QWidget`。

## 它解决的问题

`QWindow` 本身提供原生窗口、曝光、尺寸、屏幕和事件生命周期，但不天然是一个可直接交给 `QPainter` 的常规绘制设备。`QPaintDeviceWindow` 将窗口事件模型和 `QPaintDevice` 合并：

1. 外部状态变化时调用 `update()`，声明某块区域已过期；
2. Qt 合并多个更新请求，在合适的事件循环时机安排重绘；
3. Qt 向窗口发送 `QPaintEvent`；
4. 派生类在 `paintEvent(QPaintEvent *)` 中，以当前窗口为目标建立 `QPainter`；
5. 绘制结束后 `QPainter` 离开作用域，窗口显示新内容。

这避免了每次数据变化都立即进行昂贵绘制，也让窗口最小化、遮挡、尺寸变化和平台合成器协调在 Qt 的事件循环中完成。

## 实际使用场景

### 1. 选择合适的现成派生类

```cpp
#include <QGuiApplication>
#include <QRasterWindow>

class PreviewWindow : public QRasterWindow
{
protected:
    void paintEvent(QPaintEvent *event) override
    {
        QPainter painter(this);
        painter.fillRect(event->region().boundingRect(), Qt::white);
        painter.drawText(rect(), Qt::AlignCenter, QStringLiteral("Preview"));
    }
};

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);
    PreviewWindow window;
    window.resize(800, 500);
    window.show();
    return app.exec();
}
```

示例使用 `QRasterWindow`，因为它是面向应用的光栅绘制窗口。其重绘思想与 `QPaintDeviceWindow` 相同，但不需要接触后者的内部构造契约。

### 2. 数据变化后请求局部重绘

```cpp
void PreviewWindow::setCursorRect(const QRect &next)
{
    const QRect changed = m_cursorRect.united(next);
    m_cursorRect = next;
    update(changed);
}
```

局部 `update(rect)` 表示该矩形应在下一次绘制中刷新。连续请求会被合并，避免鼠标移动、动画或批量数据更新时为每个小变化单独触发一次同步绘制。

### 3. 在 `paintEvent()` 中仅重画脏区

```cpp
void PreviewWindow::paintEvent(QPaintEvent *event)
{
    QPainter painter(this);

    for (const QRect &dirtyRect : event->region())
        drawScenePart(painter, dirtyRect);
}
```

`event->region()` 给出当前需要更新的区域。复杂场景可以用它减少不必要的背景、曲线或缩略图绘制；简单场景也可以直接绘制完整 `rect()`，由裁剪和合成机制处理。

## 核心模型与边界

### 它不能直接作为应用窗口使用

`QPaintDeviceWindow` 没有面向应用的公开构造函数。不要试图直接创建：

```cpp
QPaintDeviceWindow window; // 不可用
```

需要纯 `QPainter` 光栅窗口时使用 `QRasterWindow`；需要 OpenGL 上下文和 OpenGL 绘制时使用 `QOpenGLWindow`；需要控件、布局和标准部件时使用 `QWidget`。

### `update()` 是异步请求，不是立即绘制

三种 `update()` 都只是把区域标为 dirty 并安排一次绘制：

- `update()` 标记整个窗口；
- `update(const QRect &)` 标记一个矩形；
- `update(const QRegion &)` 标记一个复杂区域。

下一次 `paintEvent()` 到来之前对 `update()` 的重复调用会被合并。无参数重载的后续请求会被忽略，因为整个窗口已经是 dirty；带矩形或区域的重载会把新区域加入待更新区域。

因此不能在 `update()` 返回后立即假定像素已经刷新，也不应把它写进需要同步读取渲染结果的逻辑。

### 真正绘制只在 `paintEvent()` 中做

`paintEvent()` 的默认实现什么也不做。派生窗口应在其中创建局部 `QPainter`：

```cpp
void PreviewWindow::paintEvent(QPaintEvent *event)
{
    QPainter painter(this);
    painter.setClipRegion(event->region());
    drawContent(painter);
}
```

不要从业务函数直接调用 `paintEvent(nullptr)`，也不要长期保存指向窗口的活跃 `QPainter`。窗口可能在曝光、遮挡恢复、缩放、尺寸变化或平台请求时重绘；把绘制集中在事件回调中，才能保证当前表面和脏区信息有效。

### 窗口生命周期与线程

`QPaintDeviceWindow` 是 `QWindow`，因此：

- 创建 `QGuiApplication` 后再创建窗口；
- 只在窗口所属的 GUI 线程创建、显示、销毁和绘制；
- 后台线程产生数据时，通过信号槽的队列连接或 `QMetaObject::invokeMethod()` 通知 GUI 线程调用 `update()`；
- 析构、隐藏或平台表面失效期间，不保存和复用旧的绘制资源或 `QPainter`。

`update()` 的合并依赖事件循环。没有运行 GUI 事件循环，或窗口尚未能接收绘制事件时，调用它不会让内容立刻出现在屏幕上。

### 多重继承带来的名字选择

类同时继承 `QWindow` 与 `QPaintDevice`，并显式采用 `QWindow` 的 `width()`、`height()` 与 `devicePixelRatio()`。在窗口几何或 High-DPI 场景中，使用当前窗口的这些值，并在每次 `paintEvent()` 时重新读取；不要缓存一次尺寸后假定窗口不会被用户、系统缩放或屏幕 DPR 改变。

## 关键 API 语义

### `paintEvent(QPaintEvent *event)`

这是唯一需要由应用派生类重写的文档化扩展点。`event` 包含本次脏区域，默认实现为空。

合适的做法：

- 根据 `event->region()` 裁剪或只绘制受影响对象；
- 让 `QPainter` 在函数结束时析构并结束绘制；
- 从窗口当前 `size()`、`devicePixelRatio()` 和业务模型重新计算画面。

不合适的做法：

- 在回调外部直接画窗口；
- 递归调用 `update()` 试图立即刷新；
- 将 `QPaintEvent *` 缓存到回调结束后使用；
- 在回调中执行长时间 I/O、网络请求或大规模模型计算，阻塞 GUI 线程。

### 重载信号槽连接

无参数 `update()` 是 public slot，而另两个是普通公有函数。由于 `QWindow` 等基类也可能存在同名重载，使用函数指针连接时必须选定无参数版本：

```cpp
connect(source, &Source::contentChanged,
        preview, qOverload<>(&QPaintDeviceWindow::update));
```

也可使用 lambda：

```cpp
connect(source, &Source::contentChanged, preview, [preview] {
    preview->update();
});
```

捕获指针时仍须保证接收对象生命周期有效；使用 QObject 成员函数连接形式通常能在接收者销毁时自动断开连接。

## 常见错误

### 误用 `QPaintDeviceWindow` 作为普通窗口类

它没有可直接使用的公开构造函数。不要为了“能用 QPainter”绕过这一点；`QRasterWindow` 已经提供了应用需要的光栅窗口入口。

### 调用 `update()` 后立刻读取屏幕结果

`update()` 是请求，不是同步渲染。若需求确实需要离屏、可立即读取的像素结果，使用 `QImage` 配合 `QPainter` 完成离屏渲染，再在下一次窗口重绘中显示它。

### 每帧都 `update()` 整个窗口

整窗更新对简单场景没问题，但大型时间线、地图、表格或绘图应用应尽量传入变化的 `QRect` / `QRegion`。同时不要过度细分到成千上万个微小区域；根据场景复杂度选择合理粒度。

### 绘制时忽略 DPR 和窗口变化

窗口可在不同缩放比例的屏幕之间移动。绘制逻辑应在 `paintEvent()` 中读取当前指标，并使用 Qt 提供的 `QPainter` 坐标映射；不要把某个显示器上的原始像素坐标永久写入模型。

## API 速查表

### 本类声明的 API

| API | 说明 | 使用时重点 |
| --- | --- | --- |
| `update()` | 将整个窗口标记为 dirty，并安排一次异步重绘；同时是 public slot。 | 下一次 paint event 前的重复整窗请求会合并；连接重载时用 `qOverload<>`。 |
| `update(const QRect &rect)` | 将一个矩形标记为 dirty，并安排重绘。 | 连续调用时矩形会加入待更新区域；用于局部内容变化。 |
| `update(const QRegion &region)` | 将复杂区域标记为 dirty，并安排重绘。 | 适合不连续变化区域；不要为极细碎区域制造过高管理开销。 |
| `paintEvent(QPaintEvent *event)` | Qt 发送绘制事件时调用的受保护虚函数。 | 默认不画任何内容；派生类在此创建临时 `QPainter`，可读取 `event->region()`。 |

### 重要继承能力

| 来源 | 常用 API / 能力 | 使用时重点 |
| --- | --- | --- |
| `QWindow` | `show()`、`hide()`、`resize()`、`setGeometry()`、`screen()`、曝光和窗口事件。 | 所有窗口操作在 GUI 线程执行；窗口表面可能因曝光或屏幕变化而需要重绘。 |
| `QWindow` | `width()`、`height()`、`devicePixelRatio()`。 | 本类选择这些窗口语义；每次绘制读取当前值。 |
| `QPaintDevice` | `paintingActive()`、逻辑/物理 DPI、`depth()`、设备像素比。 | 用于理解目标绘制环境；无需手动管理其 `paintEngine()`。 |

## 与相邻类型的选择

| 目标 | 推荐类型 | 原因 |
| --- | --- | --- |
| 最普通的窗口部件界面 | `QWidget` | 有布局、控件、样式和成熟的 `paintEvent()` 模型。 |
| 无控件的 2D 光栅窗口 | `QRasterWindow` | 面向应用、可直接继承，适合用 `QPainter` 绘制。 |
| OpenGL 窗口 | `QOpenGLWindow` | 管理 OpenGL 上下文和渲染生命周期。 |
| 只想在内存中生成图像 | `QImage` | 没有窗口和事件循环重绘成本，适合后台准备像素。 |
| Qt 内部窗口绘制基类机制 | `QPaintDeviceWindow` | 主要作为现成派生类的共同基础，通常不直接使用。 |

一句话记忆：调用 `update()` 是“请 Qt 稍后重画”，重写 `paintEvent()` 才是“现在把窗口画出来”。
