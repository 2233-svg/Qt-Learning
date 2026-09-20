# Qt QScrollEvent：滚动过程中的位置事件

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QScrollEvent>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QEvent -> QScrollEvent`  
> 类型定位：滚动状态与位置事件参数

## 1. 它解决什么问题

`QScrollEvent` 表示一次滚动活动中的位置更新。它把三个信息交给事件接收者：

- 当前内容位置 `contentPos()`；
- 当前越界距离 `overshootDistance()`；
- 这次事件处于滚动开始、滚动中间还是滚动结束阶段的 `scrollState()`。

它解决的是“内容应该移动到哪里、是否发生越界回弹、滚动序列是否开始或结束”的事件通信问题。它不负责保存内容、不负责修改滚动条、不负责执行动画，也不自动替接收者更新视口。

通常它由 Qt 的滚动机制发送，常见来源是 `QScroller`。自定义接收者可以在事件处理函数中读取位置和状态，再更新自己的内容偏移、重绘区域或滚动条模型。

`QScrollEvent` 和 `QScrollPrepareEvent` 是配套但职责不同的两个事件：

- `QScrollPrepareEvent`：滚动开始前，接收者告诉滚动器视口大小、内容位置和可滚动范围，并通过接受事件表示“可以开始滚动”。
- `QScrollEvent`：滚动过程中，滚动器把新的内容位置和越界距离发送给接收者。

## 2. 构建与包含

CMake：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

源码：

```cpp
#include <QScrollEvent>
#include <QPointF>
```

qmake 工程使用：

```qmake
QT += gui
```

如果滚动由 `QScroller` 驱动，通常还会使用 `Qt6::Widgets` 中的滚动控件或 `QScroller`。事件类本身属于 `Gui`，不需要为了构造和读取它而创建 widget。

## 3. 最小使用方式

### 3.1 在 `event()` 中接收滚动事件

```cpp
#include <QEvent>
#include <QScrollEvent>
#include <QWidget>

class ScrollViewport : public QWidget
{
protected:
    bool event(QEvent *event) override
    {
        if (event->type() == QEvent::Scroll) {
            auto *scroll = static_cast<QScrollEvent *>(event);
            setContentOffset(scroll->contentPos());
            setOvershoot(scroll->overshootDistance());
            update();
            return true;
        }

        return QWidget::event(event);
    }

private:
    void setContentOffset(const QPointF &position);
    void setOvershoot(const QPointF &distance);
};
```

实际使用时，事件接收者还要按照自己的事件分发方式确认滚动事件能到达该对象。`QScrollEvent` 本身只提供数据，不会自动调用 `update()` 或改变任何内容位置。

### 3.2 根据滚动阶段处理状态

```cpp
void ScrollViewport::handleScroll(const QScrollEvent &event)
{
    const QPointF position = event.contentPos();

    switch (event.scrollState()) {
    case QScrollEvent::ScrollStarted:
        beginScroll(position);
        break;
    case QScrollEvent::ScrollUpdated:
        updateScroll(position, event.overshootDistance());
        break;
    case QScrollEvent::ScrollFinished:
        finishScroll(position);
        break;
    }
}
```

头文件中的 `ScrollState` 是普通枚举，取值为 `ScrollStarted = 0`、`ScrollUpdated = 1`、`ScrollFinished = 2`。应使用 `switch` 或枚举比较，不要把它当作可以任意按位组合的 flags。

## 4. 核心使用模型

### 4.1 `contentPos()` 是内容位置，不是手指位置

`contentPos()` 是滚动器计算出的新内容位置。它通常表示内容相对于视口的滚动坐标，具体正负方向取决于接收者和滚动框架采用的内容坐标约定。

不要把它直接当成触摸点、鼠标点或滚动增量。若业务需要增量，应自行保存上一事件的位置并计算：

```cpp
const QPointF delta = event.contentPos() - previousPosition;
previousPosition = event.contentPos();
```

在处理第一条事件前，`previousPosition` 应由 `ScrollStarted` 的位置初始化。

### 4.2 `overshootDistance()` 是越界量

`overshootDistance()` 表示内容位置相对于正常可滚动范围的越界距离，用于实现橡皮筋、回弹或边界反馈效果。它不是速度、加速度、滚轮角度或手指移动距离。

没有越界时通常为 `(0, 0)`。如果接收者不支持越界反馈，可以忽略它，但不能用它代替内容位置。

### 4.3 `scrollState()` 描述事件在序列中的位置

一个连续滚动活动通常包含：

1. 一个 `ScrollStarted` 事件；
2. 零个或多个 `ScrollUpdated` 事件；
3. 一个 `ScrollFinished` 事件。

应用层应考虑滚动活动只产生单个事件的情况。Qt 文档说明单事件活动可能同时具有开始和结束语义；但 Qt 6.11.1 头文件将 `ScrollState` 声明为普通枚举，不能像位标志那样用 `ScrollStarted | ScrollFinished` 表达两个独立状态。实际接收代码应以当前 Qt 版本的枚举值和事件发送路径为准，并避免写出依赖位组合的判断。

如果使用 `switch`，应为每个公开枚举值提供分支，并在默认分支中处理未来版本或异常输入：

```cpp
switch (state) {
case QScrollEvent::ScrollStarted:
    // ...
    break;
case QScrollEvent::ScrollUpdated:
    // ...
    break;
case QScrollEvent::ScrollFinished:
    // ...
    break;
default:
    break;
}
```

### 4.4 事件本身不会更新内容

即使 `contentPos()` 已经变化，接收者也必须把它写入自己的内容模型、移动子项、调整绘制变换或触发重绘。事件的作用是传输状态，而不是替接收者完成滚动实现。

## 5. 实际使用场景

### 5.1 自定义视口的平滑滚动

自定义视口可以把 `contentPos()` 保存为浮点偏移，在 `paintEvent()` 中根据这个偏移绘制内容。使用 `QPointF` 可以保留亚像素滚动位置，避免每次事件都过早取整。

### 5.2 惯性滚动和回弹效果

移动设备或触控板滚动时，`overshootDistance()` 可用来绘制边界拉伸、阴影或回弹视觉效果。滚动内容位置和越界效果应分开保存，避免把越界距离永久写入正常内容坐标。

### 5.3 滚动条同步

接收 `ScrollUpdated` 后，可把 `contentPos()` 转换成滚动条的整数范围。转换时应明确浮点到整数的舍入规则，并在 `ScrollFinished` 时进行最终校正，避免累计舍入误差。

### 5.4 事件序列诊断

在调试滚动问题时，记录 `scrollState()`、`contentPos()` 和 `overshootDistance()` 的序列，比只记录鼠标或触摸事件更接近滚动器最终交给视口的结果。

### 5.5 与 `QScrollPrepareEvent` 配合

如果接收者自己支持基于 `QScroller` 的滚动，通常先处理 `QScrollPrepareEvent`，设置视口大小、内容位置和内容位置范围，并接受事件；滚动真正开始后再处理 `QScrollEvent`。

接受 `QScrollPrepareEvent` 也不保证一定会收到 `QScrollEvent`。例如最大内容位置是 `(0, 0)` 时没有实际可滚动距离，滚动器可能不会再发送滚动事件。

## 6. 生命周期、所有权和线程

### 6.1 事件指针只在处理期间借用

在 `event(QEvent *)` 或其他事件处理函数中，传入的 `QScrollEvent *` 通常由 Qt 的事件分发流程管理。不要在处理完成后保存指针，也不要手动 `delete` Qt 正在分发的事件对象。

如果需要异步使用数据，应立即复制值：

```cpp
const QPointF position = event->contentPos();
const QPointF overshoot = event->overshootDistance();
const auto state = event->scrollState();

QMetaObject::invokeMethod(this, [this, position, overshoot, state] {
    applyScroll(position, overshoot, state);
}, Qt::QueuedConnection);
```

这里跨事件循环传递的是 `QPointF` 和枚举值，不是事件指针。

### 6.2 自行构造事件时由调用方管理

构造函数可以用于测试或自定义事件投递：

```cpp
auto *event = new QScrollEvent(QPointF(10.5, 0.0),
                               QPointF(0.0, 0.0),
                               QScrollEvent::ScrollUpdated);
QCoreApplication::postEvent(viewport, event);
```

通过 `postEvent()` 投递后，事件所有权按 Qt 事件队列规则转移给 Qt；不要在投递后再次释放它。手动直接调用处理逻辑时，可以使用栈对象，但不要把它当成真实滚动器已经更新过状态的证明。

### 6.3 GUI 对象和滚动模型的线程边界

事件分发和 widget/window 更新应在 GUI 线程完成。工作线程可以计算目标位置或动画参数，然后通过 queued signal/slot 把值传给 GUI 线程；不要从工作线程直接向 widget 发送同步滚动调用，也不要在多个线程同时修改同一滚动状态。

### 6.4 事件不可拷贝为长期模型

`QScrollEvent` 适合表达一次瞬时事件，不应作为长期滚动状态对象。需要保存的状态应转换成自己的结构，例如当前位置、越界量、滚动是否活动和时间戳。

## 7. `ScrollState` 的逐项语义

### 7.1 `ScrollStarted`

表示滚动活动中的第一条滚动事件。接收者可以在这里初始化上一位置、清除旧的回弹状态、开始记录手势或暂停冲突的滚动源。

### 7.2 `ScrollUpdated`

表示滚动活动中间的更新事件。它通常带来连续的内容位置变化，接收者应更新偏移并请求重绘。

### 7.3 `ScrollFinished`

表示滚动活动中的最后一条滚动事件。接收者可以在这里完成最终校正、提交滚动位置、恢复交互状态或启动回弹收尾。

### 7.4 不要假设三种状态一定完整出现

平台输入、内容范围和滚动器状态可能导致事件序列短于预期。接收者不要把资源释放、状态提交或业务逻辑只绑定到“必然收到一个 `ScrollFinished`”这一假设上；对滚动源停止、对象销毁和事件被过滤等路径也应保持状态可恢复。

## 8. 与多个滚动源协作时的冲突

Qt 文档提醒，不应让两个来源发送相互冲突的 `QScrollEvent`。例如，应用自己在处理触摸滚动时更新内容位置，同时又让另一个滚动器向同一目标发送位置事件，可能造成跳动、回弹状态错乱或滚动结束时位置被覆盖。

推荐做法是为同一视口确定一个主滚动源：

- 由 `QScroller` 统一产生滚动事件；
- 或由应用自己的滚动控制器产生位置更新；
- 如果必须切换来源，先明确停止前一个活动并同步当前位置。

Qt 文档特别指出，使用 `QScroller::scrollTo()` 是安全的滚动方式。这里的“安全”是指滚动器内部协调其滚动活动，不代表可以同时向同一对象注入另一套相冲突的事件。

## 9. 常见误区与排查顺序

### 9.1 把 `contentPos()` 当成增量

它是新的内容位置，不是本次移动了多少。需要增量时与上一次位置相减，并处理第一条事件没有旧位置的情况。

### 9.2 把 `overshootDistance()` 当成速度

越界距离表示位置超出正常范围的空间量。速度和加速度不由 `QScrollEvent` 提供，不能用越界距离直接驱动物理动画。

### 9.3 收到事件后什么也不更新

`QScrollEvent` 不会自动修改视口。接收者必须更新自己的模型或绘制状态，并在需要时调用 `update()`、调整滚动条或触发布局。

### 9.4 用按位运算判断 `ScrollState`

`ScrollState` 在头文件中是普通枚举，取值为 0、1、2。使用 `state & ScrollFinished` 这类 flags 写法会产生误导，甚至把 `ScrollStarted` 的零值当成“没有状态”。

### 9.5 把事件指针保存给定时器

事件处理返回后，指针的生命周期可能已经结束。保存 `QPointF` 和枚举值的副本，不要保存 `QScrollEvent *`。

### 9.6 同时让两个来源控制一个视口

手势控制器、滚动条、`QScroller` 和自定义动画如果没有明确仲裁，可能互相覆盖位置。排查时先记录事件来源和状态序列，再确定唯一的状态拥有者。

### 9.7 过早把浮点位置取整

`contentPos()` 和 `overshootDistance()` 使用 `QPointF`。如果每个事件都直接转换为整数，慢速或高 DPI 滚动中可能出现停顿和抖动。只在绘制目标或滚动条接口确实要求整数时再按统一规则取整。

### 9.8 认为接受事件会自动启动滚动

`QScrollEvent` 本身没有“接受后开始滚动”的机制。接受语义主要出现在 `QScrollPrepareEvent`，并且即使接受准备事件，也不保证一定收到后续 `QScrollEvent`。

## 10. 继承自 `QEvent` 的常用边界

`QScrollEvent` 继承 `QEvent`，因此可以使用事件类型和通用事件状态接口：

```cpp
if (event->type() == QEvent::Scroll) {
    auto *scroll = static_cast<QScrollEvent *>(event);
    // 只有确认 type() 后才能进行这种静态转换。
}
```

`type()` 用于识别这是滚动事件；`accept()`、`ignore()`、`isAccepted()` 和 `setAccepted()` 是 `QEvent` 的通用状态。不要把这些通用状态误解为“接受就执行滚动、忽略就回滚内容”。具体接收者是否继续传播事件，取决于其事件处理实现。

事件对象通常在接收者处理期间有效。若要将事件转发到另一个对象，复制位置、越界量和状态后创建新的事件，或直接调用另一个对象的值接口；不要把同一个事件指针异步转交给多个生命周期不明的对象。

## 11. 逐项 API 说明

### 成员类型

#### `enum QScrollEvent::ScrollState`

表示一次滚动事件在滚动活动中的阶段。Qt 6.11.1 的枚举值为：

| 枚举值 | 数值 | 语义 |
| --- | ---: | --- |
| `QScrollEvent::ScrollStarted` | `0` | 一次滚动活动的第一条事件 |
| `QScrollEvent::ScrollUpdated` | `1` | 第一条和最后一条之间的更新事件 |
| `QScrollEvent::ScrollFinished` | `2` | 一次滚动活动的最后一条事件 |

它不是声明为 `Q_ENUMS` 或 flags 的位集合。业务代码应按枚举值处理，并为异常或未来值保留默认分支。

### 构造函数

#### `QScrollEvent::QScrollEvent(const QPointF &contentPos, const QPointF &overshootDistance, QScrollEvent::ScrollState scrollState)`

创建一个滚动事件。`contentPos` 是新的内容位置，`overshootDistance` 是新的越界距离，`scrollState` 说明该事件在滚动活动中的阶段。

构造函数只保存这些参数并建立一个滚动事件对象，不会移动任何 widget，不会改变滚动条，不会启动 `QScroller`，也不会验证位置是否位于某个内容范围内。

### 位置查询

#### `QPointF QScrollEvent::contentPos() const`

返回事件携带的新内容位置。它是值返回，不依赖事件内部引用，可以安全地复制到自己的滚动模型。它的正负方向由接收者的内容坐标约定决定，不应擅自假定“向下滚动必然是正 Y”。

#### `QPointF QScrollEvent::overshootDistance() const`

返回事件携带的越界距离。没有越界时通常为零向量；出现橡皮筋效果时可用它绘制边界反馈。它不表示速度，也不会自动限制在内容范围内。

#### `QScrollEvent::ScrollState QScrollEvent::scrollState() const`

返回当前事件的滚动状态。使用 `ScrollStarted`、`ScrollUpdated` 和 `ScrollFinished` 分支处理滚动生命周期；不要依赖按位组合判断。

### 继承自 `QEvent` 的常用 API

#### `QEvent::Type QScrollEvent::type() const`

返回事件类型，正常的 `QScrollEvent` 为 `QEvent::Scroll`。在统一 `event()` 入口中，确认类型后再将 `QEvent *` 转换为 `QScrollEvent *`。

#### `bool QScrollEvent::isAccepted() const`

读取 `QEvent` 的通用接受状态。它不是“内容已经滚动”的判断，也不是滚动器状态查询。

#### `void QScrollEvent::accept()`

将通用事件接受状态设为已接受。是否影响后续事件传播取决于接收者和事件分发路径，不会自动应用 `contentPos()`。

#### `void QScrollEvent::ignore()`

将通用事件接受状态设为未接受。它不会把内容位置恢复到上一值，也不会撤销已经发生的滚动器状态更新。

#### `void QScrollEvent::setAccepted(bool accepted)`

直接设置通用接受状态。只有在明确理解目标接收者事件传播契约时才使用；不要把它当作滚动范围或滚动许可配置。

#### `bool QScrollEvent::spontaneous() const`

查询事件是否由底层系统自发产生。这个信息适合辅助诊断事件来源，不能替代 `scrollState()`，也不能单独说明事件来自触摸、鼠标或惯性滚动。

#### `QEvent *QScrollEvent::clone() const`

通过 `QEvent` 的通用事件复制接口创建副本。应用通常不需要克隆滚动事件；若确实要转发，应确认副本的所有权，并把它视为一次新的临时事件。

## API 速查表

| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 枚举 | `enum QScrollEvent::ScrollState` | 描述滚动开始、更新和结束阶段 | 普通枚举，不是可任意组合的位标志 |
| 枚举值 | `ScrollStarted = 0` | 标记滚动活动的第一条事件 | 初始化上一位置和滚动会话状态 |
| 枚举值 | `ScrollUpdated = 1` | 标记滚动活动中的中间更新 | 主要用于连续更新内容和请求重绘 |
| 枚举值 | `ScrollFinished = 2` | 标记滚动活动的最后一条事件 | 做最终校正，但不要假设所有路径必然收到它 |
| 构造 | `QScrollEvent(const QPointF &contentPos, const QPointF &overshootDistance, ScrollState scrollState)` | 创建带位置、越界量和阶段的滚动事件 | 不会自动移动内容、启动滚动器或校验范围 |
| 查询 | `QPointF contentPos() const` | 获取新的内容位置 | 不是滚动增量、手指位置或速度 |
| 查询 | `QPointF overshootDistance() const` | 获取内容越过正常范围的距离 | 不是速度；没有越界时通常为零 |
| 查询 | `ScrollState scrollState() const` | 获取滚动序列阶段 | 使用枚举比较或 `switch`，不要按位运算 |
| 事件基类 | `type()` | 查询事件类型 | 正常值是 `QEvent::Scroll` |
| 事件基类 | `isAccepted()` | 查询通用接受状态 | 不表示内容是否已滚动 |
| 事件基类 | `accept()` | 设置通用接受状态 | 不会自动应用内容位置 |
| 事件基类 | `ignore()` | 清除通用接受状态 | 不会撤销滚动或恢复上一位置 |
| 事件基类 | `setAccepted(bool)` | 直接设置接受状态 | 不是滚动范围或滚动许可 API |
| 事件基类 | `spontaneous()` | 查询事件是否由系统自发产生 | 不能替代滚动阶段和来源判断 |
| 事件基类 | `clone()` | 创建事件副本 | 通常不需要；副本仍按临时事件管理 |
| 相关事件 | `QScrollPrepareEvent` | 在滚动开始前设置视口、内容位置和范围 | 接受准备事件也不保证一定有后续 `QScrollEvent` |
| 相关滚动器 | `QScroller` | 产生和协调滚动活动 | 同一视口不要再注入冲突的第二个滚动源 |

---

### 一句话总结

`QScrollEvent` 是一次滚动更新的瞬时数据包：`contentPos()` 给出新的内容位置，`overshootDistance()` 给出越界量，`scrollState()` 给出滚动阶段；接收者需要自己更新模型和绘制，并避免多个滚动源同时控制同一视口。
