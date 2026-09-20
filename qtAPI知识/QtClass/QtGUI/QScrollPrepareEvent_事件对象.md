# Qt QScrollPrepareEvent：滚动开始前的几何协商

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QScrollPrepareEvent>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QEvent -> QScrollPrepareEvent`  
> 类型定位：滚动准备阶段的可写事件参数

## 1. 它解决什么问题

`QScrollPrepareEvent` 是滚动器在真正开始滚动前发送给目标对象的协商事件。它让目标对象告诉滚动器三类几何信息：

- 视口有多大：`setViewportSize()`；
- 内容位置允许落在哪个范围：`setContentPosRange()`；
- 当前内容位置在哪里：`setContentPos()`。

事件还携带了开始滚动的触摸或鼠标位置 `startPos()`。目标对象在准备事件中填好这些信息，并接受事件，表示它愿意由滚动器接管本次滚动。

它不负责执行滚动动画，也不直接移动内容。滚动器通常在准备事件被接受后，根据这些几何约束产生后续 `QScrollEvent`。如果没有可滚动距离，例如最大内容位置为 `(0, 0)`，即使准备事件被接受，也不保证会收到后续滚动事件。

## 2. 构建与包含

CMake：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

源码：

```cpp
#include <QScrollPrepareEvent>
#include <QPointF>
#include <QRectF>
#include <QSizeF>
```

qmake 工程使用：

```qmake
QT += gui
```

如果通过 `QScroller` 为 widget 提供触摸或惯性滚动，还需要使用对应的 `Qt6::Widgets` API。事件类型本身位于 `Qt6::Gui`。

## 3. 最小可用方式

下面的自定义 viewport 在收到准备事件时提供视口大小、内容位置范围和当前位置，并接受事件：

```cpp
#include <QEvent>
#include <QScrollPrepareEvent>
#include <QWidget>

class ScrollViewport : public QWidget
{
protected:
    bool event(QEvent *event) override
    {
        if (event->type() == QEvent::ScrollPrepare) {
            auto *prepare = static_cast<QScrollPrepareEvent *>(event);

            prepare->setViewportSize(size());
            prepare->setContentPosRange(
                QRectF(0.0, 0.0,
                       qMax(0.0, contentSize().width() - width()),
                       qMax(0.0, contentSize().height() - height())));
            prepare->setContentPos(contentPosition());
            prepare->accept();
            return true;
        }

        return QWidget::event(event);
    }

private:
    QSizeF contentSize() const;
    QPointF contentPosition() const;
};
```

这里的范围示例采用“内容偏移从 `(0, 0)` 到最大偏移”的约定。实际项目可能使用相反的 Y 方向或不同的内容坐标原点，关键是 `contentPos()`、`contentPosRange()` 和后续 `QScrollEvent::contentPos()` 必须使用同一约定。

## 4. 核心使用模型

### 4.1 准备事件是几何信息的单次协商

滚动器发送 `QScrollPrepareEvent` 时，目标对象应根据当前内容和视口状态立即填入几何信息：

1. `startPos()` 告诉你触摸或鼠标开始位置；
2. `setViewportSize()` 告诉滚动器可滚动的视口大小；
3. `setContentPosRange()` 告诉滚动器内容位置的合法范围；
4. `setContentPos()` 告诉滚动器滚动开始前的当前位置；
5. `accept()` 表示目标对象支持这次滚动。

这些值是滚动器建立后续滚动模型的输入，不是属性绑定。内容大小或 viewport 改变后，应在下一次准备事件中重新计算。

### 4.2 `contentPosRange()` 是位置范围，不是内容尺寸

`contentPosRange()` 返回一个 `QRectF`，表示内容位置允许所在的坐标范围。它不是内容本身的宽高，也不是 viewport 矩形。

在常见的左上角原点、内容向左上方移动为正偏移的模型中：

```text
内容尺寸 = (contentWidth, contentHeight)
视口尺寸 = (viewportWidth, viewportHeight)
最大内容偏移 = (
    max(0, contentWidth  - viewportWidth),
    max(0, contentHeight - viewportHeight)
)
contentPosRange = QRectF(0, 0, maxX, maxY)
```

这是常见约定，不是 `QScrollPrepareEvent` 强制规定的坐标方向。应用应让范围、当前位置和绘制变换保持一致。

### 4.3 `viewportSize()` 使用浮点尺寸

视口尺寸是 `QSizeF`，适合高 DPI、缩放内容或非整数布局。应传入真正用于裁剪和显示滚动内容的区域尺寸，而不是整个窗口尺寸，也不是内容尺寸。

如果滚动条、边框或内边距占用空间，`viewportSize()` 应使用剩余的实际可视区域。视口尺寸过大或过小都会让滚动器计算出错误的最大位置。

### 4.4 接受事件表示“可以开始滚动”

Qt 文档要求目标对象在填好几何信息后接受该事件，以表示允许开始滚动。未接受时，滚动器可以认为目标不支持这次滚动，后续滚动流程不会按预期建立。

但接受准备事件不是“承诺一定收到 `QScrollEvent`”。没有可滚动距离、滚动被取消、目标销毁或滚动状态改变时，后续事件可能不出现。

### 4.5 `startPos()` 是输入手势的起点

`startPos()` 是开始滚动的触摸或鼠标事件位置。它通常用于自定义目标判断手势起点、计算内容抓取位置或记录诊断信息。

它不是当前内容位置，也不是 viewport 中应显示的内容原点。不要把它写入 `setContentPos()`，除非你的内容坐标模型明确规定两者相同。

## 5. 实际使用场景

### 5.1 自定义可滚动视图

自定义 widget 或 QObject 可以在准备事件中报告内容范围和当前位置，再在后续 `QScrollEvent` 中应用新的内容位置。这样滚动器只负责手势、惯性和运动曲线，目标对象负责实际绘制。

### 5.2 触摸拖拽内容

`startPos()` 可以帮助目标对象识别滚动手势开始位置。准备阶段应读取当前内容偏移并设置范围，而不是在这里根据单个触摸点直接移动内容。

### 5.3 内容尺寸动态变化

列表、图片、文档或视频内容可能在滚动过程中改变尺寸。可以在合适时机让滚动器重新发送准备事件，然后重新设置 viewport、范围和当前位置。`QScroller::resendPrepareEvent()` 就是用于重新请求这类几何信息的协作入口。

### 5.4 没有可滚动距离的视口

当内容尺寸不超过视口尺寸时，最大内容偏移通常为 `(0, 0)`。这时可以接受准备事件以表明目标支持滚动协议，但不应把“接受”理解为必然产生一条滚动更新。

### 5.5 浮点内容布局

缩放画布、地图、图像查看器和高 DPI 文档视图可能使用浮点内容坐标。使用 `QRectF`、`QPointF` 和 `QSizeF` 保留精度，等到绘制或滚动条显示时再根据目标 API 需要取整。

## 6. 生命周期、所有权和线程

### 6.1 事件指针只在处理期间有效

由 Qt 或滚动器发送的 `QScrollPrepareEvent *` 是事件处理期间的借用指针。不要把它保存到成员变量、定时器或异步任务中，也不要在处理函数返回后继续调用它。

如果需要在稍后使用数据，应复制必要值：

```cpp
const QPointF start = event->startPos();
const QPointF current = event->contentPos();
const QRectF range = event->contentPosRange();
const QSizeF viewport = event->viewportSize();
```

### 6.2 自行投递时遵守事件所有权

测试或自定义事件路径可以直接构造准备事件：

```cpp
QScrollPrepareEvent event(QPointF(20.0, 30.0));
event.setViewportSize(QSizeF(800.0, 600.0));
event.setContentPosRange(QRectF(0.0, 0.0, 1200.0, 900.0));
event.setContentPos(QPointF(100.0, 50.0));
event.accept();
```

如果用 `QCoreApplication::postEvent()` 投递动态分配的事件，投递后由 Qt 事件队列负责销毁；不要重复释放。测试栈对象时，事件处理必须在它仍然存活期间完成。

### 6.3 GUI 滚动模型通常在 GUI 线程

目标 widget、`QScroller` 和事件分发通常在 GUI 线程。工作线程可以计算内容尺寸，但应通过 queued signal/slot 把尺寸或范围的值传给 GUI 线程，再由 GUI 线程修改和接受事件。

不要从工作线程直接向 widget 发送同步事件，也不要在线程之间共享一个可变的准备事件对象。

## 7. 如何计算内容位置范围

### 7.1 常见偏移模型

假设内容左上角在视口中完全可见时偏移为 `(0, 0)`，向右或向下查看内容时偏移增加，则：

```cpp
const QSizeF content = contentSize();
const QSizeF viewport = size();

const qreal maxX = qMax<qreal>(0.0, content.width() - viewport.width());
const qreal maxY = qMax<qreal>(0.0, content.height() - viewport.height());

event->setViewportSize(viewport);
event->setContentPosRange(QRectF(0.0, 0.0, maxX, maxY));
event->setContentPos(currentOffset);
```

`QRectF` 的 width 和 height 表示范围的宽度和高度，而不是右下角坐标本身。对“从 0 到 maxX”的范围，用 `QRectF(0, 0, maxX, maxY)` 是 Qt 滚动模型中常见的写法；应用应结合自身所用的 `QScroller` 内容坐标约定验证边界。

### 7.2 内容比视口小时的处理

内容小于视口时，最大偏移应钳制为零，不要传入负的范围宽度或高度：

```cpp
const qreal maxX = qMax(0.0, content.width() - viewport.width());
```

如果应用希望内容居中、允许负偏移或使用边缘留白，应把这些规则明确编码到范围和当前位置中，而不是依赖滚动器猜测。

### 7.3 当前内容位置必须与范围一致

设置 `contentPos()` 时，最好保证它位于 `contentPosRange()` 内，除非你有意支持初始越界或特殊回弹状态。范围和当前位置不一致会让滚动器在开始时立即校正或产生出乎预期的运动。

## 8. 与 `QScrollEvent` 的衔接

准备事件负责提供滚动器建立运动模型所需的几何；滚动事件负责报告实际滚动中的新位置：

```text
QScrollPrepareEvent
    -> 设置 viewportSize、contentPosRange、contentPos
    -> accept()
QScrollEvent
    -> 读取 contentPos、overshootDistance、scrollState
    -> 更新内容模型并重绘
```

不要在 `QScrollPrepareEvent` 中完成每一帧的滚动绘制，也不要把 `QScrollEvent::contentPos()` 反写成下一次准备事件的唯一来源而忽略内容尺寸变化。每次准备阶段都应从当前真实内容和 viewport 重新计算。

## 9. 常见误区与排查顺序

### 9.1 只接受事件，不设置几何

接受事件只是表示愿意滚动。没有 viewport、内容范围和当前位置，滚动器无法得到可靠的运动边界。处理时应先设置三个几何值，再调用 `accept()`。

### 9.2 把内容尺寸传给 `setContentPosRange()`

该函数需要的是内容位置范围。若内容是 `2000 x 1200`、视口是 `800 x 600`，常见最大偏移是 `1200 x 600`，而不是把 `2000 x 1200` 直接作为位置范围。

### 9.3 把 viewport 尺寸设置成内容尺寸

`setViewportSize()` 描述可见滚动窗口，不描述被滚动内容。传错后最大偏移会被错误计算。

### 9.4 忽略内容小于视口的情况

直接计算 `content - viewport` 可能得到负范围。应按滚动模型将最大偏移钳制到零，或显式处理居中和留白策略。

### 9.5 把 `startPos()` 当成 `contentPos()`

一个是手势起点，一个是当前内容偏移。它们通常处于不同的坐标语义中，不能互换。

### 9.6 认为接受后一定有 `QScrollEvent`

如果没有可滚动距离，或者滚动在准备后被取消，后续滚动事件可能没有。资源和状态清理不能只依赖后续滚动事件。

### 9.7 保存事件指针或引用

本类的查询函数返回值对象，但事件指针本身仍只在分发期间有效。需要稍后使用时复制 `QPointF`、`QRectF` 和 `QSizeF`。

### 9.8 与第二个滚动源同时修改位置

`QScroller`、滚动条、自定义手势和应用动画若同时控制同一内容，准备事件中的范围与实际位置可能互相覆盖。应明确一个滚动状态拥有者，并在切换来源时同步位置。

### 9.9 把 `ignore()` 当作回滚

事件接受状态只影响事件是否被接收或传播，不会自动恢复内容位置，也不会撤销已经建立的外部手势状态。是否接受应表示目标是否支持这次滚动，而不是用作业务回滚按钮。

## 10. 继承自 `QEvent` 的常用语义

`QScrollPrepareEvent` 的事件类型是 `QEvent::ScrollPrepare`。统一事件入口中应先判断类型，再进行转换：

```cpp
if (event->type() == QEvent::ScrollPrepare) {
    auto *prepare = static_cast<QScrollPrepareEvent *>(event);
    // 读取并设置准备参数。
}
```

它继承 `QEvent` 的接受状态接口：

- `accept()`：表示目标愿意接收并参与滚动准备；
- `ignore()`：表示目标不接受这次准备事件；
- `isAccepted()`：读取当前接受状态；
- `setAccepted(bool)`：直接设置接受状态；
- `spontaneous()`：判断事件是否来自应用外部系统路径；
- `clone()`：复制事件对象；
- `type()`：读取事件类型。

`QScrollPrepareEvent` 的业务关键不是事件基类默认的接受状态，而是处理器是否按滚动协议填好三个几何值并明确调用 `accept()`。

## 11. 逐项 API 说明

### 构造函数

#### `[explicit] QScrollPrepareEvent::QScrollPrepareEvent(const QPointF &startPos)`

创建一个滚动准备事件。`startPos` 是启动滚动的触摸或鼠标事件位置。

构造函数只建立事件并保存起点，不会设置 viewport 大小、内容范围或当前内容位置，也不会自动接受事件。目标对象仍需在处理阶段填入其余信息。

### 起点与几何查询

#### `QPointF QScrollPrepareEvent::startPos() const`

返回开始滚动的触摸或鼠标位置。它是输入起点，不是内容位置，也不是滚动增量。

#### `QSizeF QScrollPrepareEvent::viewportSize() const`

返回通过 `setViewportSize()` 设置的可滚动视口尺寸。事件刚构造时不要假设它已经是目标 widget 的尺寸；只有接收者设置后，滚动器才能读取到有意义的值。

#### `QRectF QScrollPrepareEvent::contentPosRange() const`

返回通过 `setContentPosRange()` 设置的内容位置范围。它描述内容位置坐标的合法区域，不是内容的实际尺寸。

#### `QPointF QScrollPrepareEvent::contentPos() const`

返回通过 `setContentPos()` 设置的当前内容位置。它用于告诉滚动器从哪里开始建立滚动运动。

### 几何写入

#### `void QScrollPrepareEvent::setViewportSize(const QSizeF &size)`

设置用于滚动的 viewport 尺寸。传入应是内容真正可见的区域，而不是整个窗口或内容尺寸。函数只写入事件字段，不会调整目标对象的 geometry。

#### `void QScrollPrepareEvent::setContentPosRange(const QRectF &rect)`

设置内容位置允许所在的矩形范围。应用负责根据内容尺寸、viewport 尺寸、坐标原点和留白策略计算它。函数不会替调用方验证范围，也不会自动修正当前内容位置。

#### `void QScrollPrepareEvent::setContentPos(const QPointF &pos)`

设置滚动开始前的当前内容位置。它只写入事件字段，不会直接移动视口或触发绘制。应让该位置与 `contentPosRange()` 使用同一坐标系统。

### 继承自 `QEvent` 的常用 API

#### `QEvent::Type QScrollPrepareEvent::type() const`

返回 `QEvent::ScrollPrepare`。在通用 `event()` 入口中先检查该类型，再把 `QEvent *` 转换为 `QScrollPrepareEvent *`。

#### `bool QScrollPrepareEvent::isAccepted() const`

读取事件接受状态。它表示接收者是否声明愿意处理该准备事件，不表示已经产生了滚动，也不表示一定会产生后续 `QScrollEvent`。

#### `void QScrollPrepareEvent::accept()`

设置接受状态，表示目标对象愿意参与本次滚动准备。通常应在设置 viewport、范围和当前位置之后调用。

#### `void QScrollPrepareEvent::ignore()`

清除接受状态，表示目标不接受本次滚动准备。它不会恢复内容位置，也不会撤销其他输入系统已经记录的触摸状态。

#### `void QScrollPrepareEvent::setAccepted(bool accepted)`

直接设置事件接受状态。用于表达目标是否支持滚动协议；不要把它当作滚动开关或范围校验函数。

#### `bool QScrollPrepareEvent::spontaneous() const`

判断事件是否由应用外部的系统事件路径产生。它辅助说明事件来源，不提供触摸、鼠标或 `QScroller` 的完整来源分类。

#### `QEvent *QScrollPrepareEvent::clone() const`

创建一个等价的事件副本。应用一般不需要克隆它；若用于测试或转发，应自行管理动态副本并确认接受状态和已设置几何值是否符合目标逻辑。

## API 速查表

| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 构造 | `QScrollPrepareEvent(const QPointF &startPos)` | 创建滚动准备事件并保存手势起点 | 不设置 viewport、范围或当前位置，也不自动启动滚动 |
| 查询 | `QPointF startPos() const` | 获取开始滚动的触摸或鼠标位置 | 不是内容位置、偏移或速度 |
| 查询 | `QSizeF viewportSize() const` | 获取已设置的可滚动视口尺寸 | 构造后不要假设已初始化；应由接收者设置 |
| 查询 | `QRectF contentPosRange() const` | 获取内容位置的合法范围 | 不是内容尺寸；坐标方向由应用模型决定 |
| 查询 | `QPointF contentPos() const` | 获取滚动开始前的内容位置 | 必须与范围和绘制模型使用同一坐标系 |
| 写入 | `setViewportSize(const QSizeF &size)` | 设置可见滚动区域大小 | 传 viewport，不传内容尺寸或整个窗口尺寸 |
| 写入 | `setContentPosRange(const QRectF &rect)` | 设置内容位置允许范围 | 内容小于 viewport 时通常要把最大偏移钳制为零 |
| 写入 | `setContentPos(const QPointF &pos)` | 设置当前内容位置 | 只修改事件参数，不直接移动内容或重绘 |
| 事件基类 | `type()` | 获取事件类型 | 正常值为 `QEvent::ScrollPrepare` |
| 事件基类 | `isAccepted()` | 查询是否已接受 | 接受不保证一定有后续 `QScrollEvent` |
| 事件基类 | `accept()` | 声明目标支持本次滚动准备 | 通常在三个几何值设置完成后调用 |
| 事件基类 | `ignore()` | 声明目标不接受本次准备 | 不会回滚内容位置或输入状态 |
| 事件基类 | `setAccepted(bool)` | 直接设置接受状态 | 不是滚动开关或范围校验 API |
| 事件基类 | `spontaneous()` | 判断是否来自系统事件路径 | 不能精确区分触摸、鼠标和滚动器来源 |
| 事件基类 | `clone()` | 创建等价事件副本 | 通常不需要；副本需按事件所有权规则管理 |
| 相关事件 | `QScrollEvent` | 在准备完成后报告实际滚动位置 | 接受准备事件也不保证一定收到它 |
| 相关滚动器 | `QScroller::resendPrepareEvent()` | 重新请求目标提供滚动几何 | 适合内容尺寸或 viewport 在滚动中变化时使用 |

---

### 一句话总结

`QScrollPrepareEvent` 是滚动开始前的几何协商包：目标对象设置 viewport 大小、内容位置范围和当前内容位置，再接受事件表示可以滚动；它不执行动画，也不保证一定产生后续 `QScrollEvent`。
