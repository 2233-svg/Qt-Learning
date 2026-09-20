# Qt QResizeEvent：读取尺寸变化的事件参数

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QResizeEvent>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QEvent -> QResizeEvent`  
> 类型定位：事件参数对象

## 1. 它解决什么问题

`QResizeEvent` 把一次尺寸变化中的两个快照交给事件处理器：

- `size()`：变化后的新尺寸。
- `oldSize()`：变化前的旧尺寸。

它不负责调整控件或窗口大小，也不负责绘制。它的作用是让 `QWidget::resizeEvent()`、`QWindow::resizeEvent()` 或自定义事件处理逻辑知道“这次从多大变成了多大”，从而重新计算布局、缓存、视口、纹理尺寸或其他依赖几何的状态。

事件类型是 `QEvent::Resize`。Qt 通常在对象尺寸变化后自动创建并投递它；应用也可以手动构造一个 `QResizeEvent`，但这只会创建事件对象，不会真的改变任何 widget 或 window 的几何。

## 2. 构建与包含

CMake：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

源码：

```cpp
#include <QResizeEvent>
#include <QWidget>
```

qmake 工程使用：

```qmake
QT += gui
```

如果重写的是 `QWidget`，工程还需要链接 `Widgets` 模块：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

## 3. 最小使用方式

### 3.1 QWidget 子类

```cpp
#include <QResizeEvent>
#include <QWidget>

class PreviewWidget : public QWidget
{
protected:
    void resizeEvent(QResizeEvent *event) override
    {
        const QSize newSize = event->size();
        const QSize previousSize = event->oldSize();

        if (newSize != previousSize)
            rebuildViewport(newSize);

        QWidget::resizeEvent(event);
    }

private:
    void rebuildViewport(const QSize &size);
};
```

这里的 `event->size()` 与 widget 当前的 `size()` 应一致。`oldSize()` 用于计算变化方向、增量或判断是否需要重新分配资源。

### 3.2 QWindow 子类

```cpp
#include <QResizeEvent>
#include <QWindow>

class RenderWindow : public QWindow
{
protected:
    void resizeEvent(QResizeEvent *event) override
    {
        updateSwapChain(event->size());
        QWindow::resizeEvent(event);
    }

private:
    void updateSwapChain(const QSize &size);
};
```

`QWindow::resizeEvent()` 既可能对应程序调用 `resize()`、`setGeometry()` 后窗口系统确认的变化，也可能对应用户拖动窗口边框造成的变化。

## 4. 事件到达时发生了什么

### 4.1 尺寸在处理器调用前已经改变

Qt 文档明确说明，调用 `QWidget::resizeEvent()` 时 widget 已经拥有新几何；`QWindow::resizeEvent()` 则在窗口发生尺寸变化时调用。处理器的职责是响应变化，不是决定变化是否发生。

因此下面这些操作通常是不正确的：

- 在 `resizeEvent()` 中通过 `ignore()` 试图否决本次 resize。
- 把 `oldSize()` 当成当前控件尺寸。
- 在还没完成尺寸计算时读取另一个异步事件中保存的裸 `QResizeEvent *`。

如果需要限制大小，应使用 `QWidget::setMinimumSize()`、`setMaximumSize()`、size policy、窗口最小/最大尺寸等几何约束，而不是依赖 resize 事件的接受状态。

### 4.2 QWidget 随后会收到绘制事件

对于 widget，Qt 会在处理 resize 事件后擦除并紧接着发送 paint event。不要在 `resizeEvent()` 里直接绘制控件内容：

- 在这里更新布局、缓存尺寸、滚动范围或绘制所需的数据。
- 在 `paintEvent()` 中根据最新状态真正绘图。

这样可以避免把绘制逻辑和尺寸通知耦合在一起，也避免 resize 过程中的重复绘制。

### 4.3 一次拖动可能产生多次事件

用户拖动窗口边框时，尺寸通常会连续变化。每次事件都可能代表一个中间尺寸，不应假设只收到一次最终尺寸。

昂贵的操作可以考虑：

- 只更新轻量的逻辑尺寸，把昂贵重建延迟到合适时机。
- 使用 `QTimer::singleShot(0, ...)` 合并同一轮事件循环中的后续工作。
- 在渲染场景中区分“立即更新 viewport”与“延后重建大型资源”。

但不要因为想合并事件而保存事件指针；应复制需要的 `QSize`。

## 5. `size()` 与 `oldSize()` 的边界

### 5.1 返回的是事件内部的 `QSize` 引用

两个函数的返回类型都是 `const QSize &`。引用指向事件对象中的成员：

```cpp
const QSize &newSize = event->size();
```

只要事件仍然存活，这个引用可用于当前处理过程。若要在 lambda、定时器或异步任务中使用，复制成值：

```cpp
const QSize newSize = event->size();
QTimer::singleShot(0, this, [this, newSize] {
    rebuildViewport(newSize);
});
```

不要把 `&event->size()` 或其引用捕获到事件处理函数之外。

### 5.2 构造函数不替调用方验证尺寸

构造函数只是保存传入的新旧 `QSize`。手工构造时可以传入任意 `QSize`，包括无效尺寸或新旧尺寸相同的值；它不会改变目标对象，也不会自动校验“新尺寸必须不同于旧尺寸”。

Qt 正常生成的 resize 事件代表真实的尺寸变化，但应用创建测试事件时应自己提供有意义的数据。

`QSize` 的宽高通常以逻辑像素表示。高 DPI 下，widget/window 的逻辑尺寸和底层物理像素尺寸不是同一个概念；若要分配图像或 framebuffer，还要结合设备像素比进行换算。

## 6. 实际使用场景

### 6.1 重新计算自定义控件布局

自定义控件可以在 resize 时根据新尺寸更新子区域、文本换行宽度、图表坐标轴或命中测试区域。尺寸计算放在这里，绘制放在 `paintEvent()`。

### 6.2 更新滚动区域与视口

滚动区域通常需要在 viewport 尺寸改变后重新计算可见范围、滚动条范围和内容位置。此时 `oldSize()` 能帮助判断是横向、纵向还是同时变化。

### 6.3 调整 OpenGL、RHI 或视频输出资源

窗口尺寸变化时，渲染目标、视口、交换链或视频帧显示区域可能需要更新。`QResizeEvent` 提供逻辑尺寸，但具体资源的像素尺寸仍需结合 `QWindow::devicePixelRatio()`、`QWidget::devicePixelRatioF()` 或使用中的图形 API 约定。

### 6.4 编写尺寸变化单元测试

可以手工构造事件并调用自定义处理逻辑，验证“旧尺寸到新尺寸”的状态转换：

```cpp
QResizeEvent event(QSize(800, 600), QSize(640, 480));
Q_ASSERT(event.size() == QSize(800, 600));
Q_ASSERT(event.oldSize() == QSize(640, 480));
```

这类测试验证的是事件参数和业务处理，不会让真实 widget 产生 resize。需要测试真正的窗口系统行为时，应调用目标对象的 `resize()` 并让事件循环运行。

## 7. 生命周期、所有权和线程

### 7.1 事件对象通常由 Qt 管理

在 `resizeEvent(QResizeEvent *event)` 中，指针由 Qt 在事件分发期间提供。处理函数通常只借用它：

- 不要 `delete event`。
- 不要把指针保存为成员变量。
- 不要假设处理器返回后它仍然有效。

如果通过 `QCoreApplication::postEvent()` 投递自己创建的事件，事件队列通常负责在投递完成后销毁事件对象；仍应遵守 Qt 事件投递接口的所有权规则，不要重复释放。

### 7.2 不要跨线程直接操作 GUI 对象

`QResizeEvent` 自身只是值和 `QEvent` 状态的组合，但 widget/window 的几何和事件分发属于 GUI 线程。工作线程不应直接调用 GUI 对象的 `resize()`、`setGeometry()` 或其事件处理器。

跨线程通信时，传递一个复制出来的 `QSize` 或通过 queued signal 请求 GUI 线程更新；不要把事件指针跨线程传递。

### 7.3 继承和复制边界

`QResizeEvent` 使用 Qt 事件类的通用事件声明，公开提供构造函数和 `QEvent` 的事件状态接口。事件对象不应通过移动语义在应用层转移，也不应把它当作长期业务模型。需要长期保存的数据应转换为自己的值对象。

## 8. `QEvent` 基类语义

### 8.1 事件类型

`type()` 返回 `QEvent::Resize`。用 `QObject::event()` 统一拦截事件时，可以这样判断：

```cpp
bool MyWidget::event(QEvent *event)
{
    if (event->type() == QEvent::Resize) {
        auto *resize = static_cast<QResizeEvent *>(event);
        handleSize(resize->size());
        return true;
    }
    return QWidget::event(event);
}
```

如果已经在 `resizeEvent()` 中处理，就不需要再通过 `event()` 重复处理同一个事件。

### 8.2 接受状态不能撤销 resize

`QEvent` 提供 `accept()`、`ignore()`、`isAccepted()` 和 `setAccepted()`。这些是通用事件状态，但对 `QResizeEvent` 不应理解为“接受才调整大小，忽略就恢复旧大小”。

尺寸变化在处理器执行前已经发生。除非某个具体接收者文档明确给出事件接受的特殊行为，否则 resize 处理器只需完成自己的响应并按继承链需要调用基类实现。

### 8.3 `spontaneous()`

`spontaneous()` 可用于判断事件是否由底层系统自发产生，而不是普通应用事件投递路径产生。它是事件来源信息，不是“用户一定拖动了窗口”的精确业务判断；程序调用后由窗口系统确认的 resize 也可能经历平台相关的事件路径。

## 9. 常见误区与排查顺序

### 9.1 在 `resizeEvent()` 中绘图

这里适合更新绘图所需状态。widget 的实际内容应在 `paintEvent()` 中绘制，Qt 会在 resize 后安排绘制事件。

### 9.2 把新尺寸和物理像素尺寸混用

`QResizeEvent::size()` 返回对象的逻辑尺寸。高 DPI 应用分配像素缓冲区或 GPU 资源时，必须另行考虑设备像素比。

### 9.3 调用 `resize()` 导致递归或事件风暴

在 resize handler 中无条件再次调用 `resize()`，可能产生新的 resize 事件，甚至形成递归式尺寸调整。只有在确实需要约束或修正尺寸时才调用，并确保目标尺寸稳定。

### 9.4 保存 `const QSize &`

返回的是事件内部引用，不是独立拥有的 `QSize`。要跨越当前调用栈保存，使用 `QSize value = event->size()`。

### 9.5 认为 `oldSize()` 总是一个有效的历史窗口尺寸

手工构造事件时，旧尺寸由调用方提供；应用不能把任意测试事件的 `oldSize()` 当作真实对象历史状态。某些初始化阶段的旧尺寸也可能是空尺寸或尚未有意义的尺寸。

### 9.6 忽略基类处理器的继承链

重写 `QWidget::resizeEvent()` 或 `QWindow::resizeEvent()` 时，是否调用基类取决于基类和子类职责。对通用自定义控件，通常在自己的逻辑前后调用基类是稳妥做法；不要把“必须调用”当成 `QResizeEvent` 本身的规则，应查看所继承具体类的文档和实现约定。

## 10. 逐项 API 说明

### 构造函数

#### `QResizeEvent::QResizeEvent(const QSize &size, const QSize &oldSize)`

创建一个尺寸变化事件，并把新尺寸 `size` 与旧尺寸 `oldSize` 保存到事件内部。构造函数不调整 widget/window 的几何，也不检查两个尺寸是否不同或有效。

传入的是 `const QSize &`，但事件保存的是自己的 `QSize` 成员；临时对象可以安全地作为构造参数：

```cpp
QResizeEvent event(QSize(1024, 768), QSize(800, 600));
```

### 尺寸查询

#### `const QSize &QResizeEvent::size() const`

返回新尺寸。对于 Qt 调用 `QWidget::resizeEvent()` 的场景，它与 widget 当前的 `size()` 相同；对于 `QWindow::resizeEvent()`，它表示这次窗口尺寸变化后的尺寸。

返回引用只在事件对象存活期间有效。需要异步使用时立即复制。

#### `const QSize &QResizeEvent::oldSize() const`

返回旧尺寸，用于计算尺寸差、判断方向或决定是否重建依赖几何的资源。它也是事件内部 `QSize` 的只读引用，不能通过它修改事件。

### 继承自 QEvent 的常用 API

#### `QEvent::Type QResizeEvent::type() const`

返回事件类型，正常的 `QResizeEvent` 为 `QEvent::Resize`。在统一 `event()` 入口中可据此安全识别事件类型。

#### `bool QResizeEvent::isAccepted() const`、`void QResizeEvent::accept()`、`void QResizeEvent::ignore()`、`void QResizeEvent::setAccepted(bool)`

读写 `QEvent` 的通用接受状态。它们不会把已经发生的尺寸变化回滚，也不是尺寸约束 API。

#### `bool QResizeEvent::spontaneous() const`

查询事件是否由底层系统自发产生。该信息适合辅助诊断事件来源，不应直接等同于用户拖动窗口。

#### `QEvent *QResizeEvent::clone() const`

通过 Qt 事件基类接口复制事件。应用通常不需要手动克隆 resize 事件；若确实需要复制，仍应把副本当作临时事件对象管理，不要复制其中 `size()` / `oldSize()` 返回引用的地址。

## API 速查表

| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 构造 | `QResizeEvent(const QSize &size, const QSize &oldSize)` | 创建带新旧尺寸快照的 resize 事件 | 只创建事件，不改变任何 widget/window；不校验尺寸 |
| 查询 | `const QSize &size() const` | 获取变化后的尺寸 | 返回事件内部引用；逻辑尺寸，不自动转换为物理像素 |
| 查询 | `const QSize &oldSize() const` | 获取变化前的尺寸 | 返回事件内部引用；手工构造时由调用方决定其内容 |
| 基类状态 | `type()` | 查询事件类型 | 正常值是 `QEvent::Resize` |
| 基类状态 | `isAccepted()` | 查询通用接受状态 | 不能用来判断 resize 是否成功 |
| 基类状态 | `accept()` / `ignore()` / `setAccepted(bool)` | 修改通用事件接受状态 | 不会撤销已完成的几何变化，也不是最小/最大尺寸约束 |
| 基类状态 | `spontaneous()` | 查询事件是否由系统自发产生 | 不是“用户拖动”的精确业务标志 |
| 基类复制 | `clone()` | 复制事件对象 | 通常只由事件框架或特殊测试使用，不要保存事件内部引用 |
| QWidget 入口 | `QWidget::resizeEvent(QResizeEvent *)` | 接收 widget 尺寸变化 | 调用时新几何已生效；更新状态，绘图放到 `paintEvent()` |
| QWindow 入口 | `QWindow::resizeEvent(QResizeEvent *)` | 接收窗口尺寸变化 | 可能来自程序请求或用户交互；渲染资源要考虑设备像素比 |

---

### 一句话总结

`QResizeEvent` 是一次尺寸变化的只读参数快照：用 `size()` 和 `oldSize()` 做布局或资源更新，用约束 API 决定允许的尺寸，用 `paintEvent()` 完成 widget 绘制，并且不要把事件指针或内部 `QSize` 引用带出当前处理过程。
