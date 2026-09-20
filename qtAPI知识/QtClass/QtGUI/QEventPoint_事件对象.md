# Qt QEventPoint 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QEventPoint>`  
> 所属模块：`Qt6::Gui`  
> 继承：无  
> 定位：描述一次指针、触摸点或触笔接触点的值对象

## 1. 它解决什么问题

`QEventPoint` 表示一个 `QPointerEvent` 中的单个点。多点触摸、触笔输入和鼠标等指针事件都可以用它记录：

- 哪个点：`id()`、`uniqueId()`、`device()`；
- 点处于什么阶段：`state()`；
- 当前、按下、上次和抓取时的位置；
- 时间、压力、旋转、接触椭圆和速度；
- 在 Qt Quick 中该点是否被某个 Item 或事件处理器接受。

它不是一个独立的事件分发器，也不负责决定点发给哪个对象。`QPointerEvent` 负责携带点集合和事件生命周期，`QEventPoint` 只提供每个点的状态快照。

常见场景：

1. 在 `QTouchEvent` 或 `QPointerEvent` 中区分多个手指；
2. 计算拖动位移、方向、速度和按住时长；
3. 在 Qt Quick 中只接受参与手势的部分触点；
4. 在自定义控件中统一处理鼠标、触摸和触笔坐标。

## 2. 构建与基本使用

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

```cpp
#include <QEventPoint>
#include <QPointerEvent>

void handlePointerEvent(const QPointerEvent *event)
{
    for (const QEventPoint &point : event->points()) {
        const QPointF current = point.position();
        const QPointF previous = point.lastPosition();
        const QPointF delta = current - previous;

        if (point.state() == QEventPoint::Pressed) {
            beginContact(point.id(), current);
        } else if (point.state() == QEventPoint::Updated) {
            updateContact(point.id(), delta);
        } else if (point.state() == QEventPoint::Released) {
            endContact(point.id(), current);
        }
    }
}
```

`QEventPoint` 是可复制的值类型，适合在事件处理期间复制到容器或业务结构中。它内部使用显式共享数据，复制本身成本较低；但不要把它理解成一个能脱离原始输入上下文持续更新的活动对象。

## 3. 点状态和事件处理

`State` 的含义：

| 状态 | 含义 |
| --- | --- |
| `Unknown` | 状态未知。 |
| `Stationary` | 本次事件中没有移动。 |
| `Pressed` | 点或按钮刚按下。 |
| `Updated` | 点的位置或其他属性更新。 |
| `Released` | 点或按钮刚释放。 |

`States` 是 `QFlags<State>`，可用位或组合多个状态。单个 `QEventPoint::state()` 返回一个状态，不要把它与 `QPointerEvent::pointingDevice()` 或事件类型混淆。

`accepted` 属性是**点级别**接受状态。在基于 widget 的应用中，通常应该接受或忽略完整的输入事件，点级接受状态一般不作为主要控制手段；在 Qt Quick 中，Item 或事件处理器可以只接受参与手势的点，其余点交给其他对象。

## 4. 三套坐标与四个时间位置

### 4.1 局部、场景、全局

- `position()`：相对于接收事件的 widget 或 item；
- `scenePosition()`：窗口、场景或图形场景坐标，具体取决于处理层；
- `globalPosition()`：屏幕或虚拟桌面坐标。

每套坐标都有按下、抓取、上次和当前版本。不要把 `scenePosition()` 当作固定含义：在 Qt Quick、Graphics View 和 Widgets 中，scene 的参考空间不同。

### 4.2 当前、按下、上次、抓取

- `position()`：本次事件的当前位置；
- `pressPosition()`：该点首次按下的位置；
- `lastPosition()`：上一次 press 或 move 事件的位置；
- `grabPosition()`：点被抓取时的位置。

位移通常使用 `position() - lastPosition()`；从手势起点计算总位移使用 `position() - pressPosition()`。如果对象中途改变了抓取者，`grabPosition()` 对应抓取时刻，不是最初按下位置。

## 5. 时间、速度与设备数据

`timestamp()` 是该点最近一次被包含在 `QPointerEvent` 中的时间；`pressTimestamp()` 是最近一次按下时间；`lastTimestamp()` 是上一次 press 或 move 的时间。`timeHeld()` 返回按下且尚未释放的持续时间，单位是秒。对已经释放的点，不应把它当作仍在增长的按住计时器。

`velocity()` 的单位是屏幕或桌面坐标系中的像素/秒。设备具备 `QInputDevice::Velocity` 能力时，速度可能来自系统；否则通常由 Qt 根据最近事件用平滑算法估算，因此它不是瞬时精确测量，适合手势反馈和惯性估计，不适合高精度物理测量。

`pressure()` 的文档范围是 `0.0` 到 `1.0`，但设备可能只提供有限精度。`rotation()` 以度为单位，零度表示指向上方，负值向左、正值向右；很多触摸设备不支持旋转，因此零值很常见。

`ellipseDiameters()` 是接触点包围椭圆的宽高，单位是逻辑像素。鼠标、触笔和多数触摸屏通常返回空尺寸，不要把空尺寸当成错误。

## 6. ID、设备与 normalizedPosition

`id()` 是事件流中的点编号，用于在连续的 press、move、release 事件之间匹配同一个点。它只应在相关设备和事件流上下文中解释，不要把它当作跨会话永久 ID。

`uniqueId()` 在没有设备支持时可能无效。触摸屏通常无法唯一识别一根手指；触笔事件中它可能代表笔的序列号，支持 TUIO 时也可能对应 token。使用前应调用 `isValid()`。

`device()` 返回产生该点的 `QPointingDevice`。使用它可以了解设备类型和能力，尤其是是否提供压力、旋转、速度或接触面积。

`normalizedPosition()` 把 `globalPosition()` 映射到 `QInputDevice::availableVirtualGeometry()`，左上角为 `(0, 0)`，右下角为 `(1, 1)`。它是相对于整个虚拟桌面的归一化位置，不是当前窗口或当前屏幕客户区的归一化位置。

## 7. 构造、复制和线程边界

公开构造函数主要用于测试和创建简单的点值。`QEventPoint(int id = -1, const QPointingDevice *device = nullptr)` 可以先创建一个无完整位置历史的点，并可附带借用的设备指针；默认 `id` 为 `-1`，不能当作真实事件流中的有效触点编号。需要直接指定状态和坐标时使用四参数构造函数：

```cpp
QEventPoint point(
    7,
    QEventPoint::Pressed,
    QPointF(100, 80),
    QPointF(1120, 640));
```

该构造函数只直接提供点 ID、状态、场景位置和全局位置；设备、历史位置、压力、速度等完整运行时数据由 Qt 的指针事件系统维护。若要模拟复杂手势，单独构造一个点并不能替代真实平台事件序列。

复制构造和复制赋值是浅复制，移动构造和移动赋值为 `noexcept`。值对象可以跨线程传递，但其中的 `device()` 是指向 Qt 设备对象的借用指针，不能因此绕过输入对象的线程和生命周期约束。后台线程应使用已经复制出的数值快照。

## 8. 常见错误

- 把 `id()` 当成永久用户或手指身份；
- 把 `uniqueId()` 当成必然有效；
- 混用局部、场景和全局坐标；
- 用 `position() - pressPosition()` 代替每帧增量，导致速度或路径累计逻辑错误；
- 把 `velocity()` 当成硬件瞬时测量；
- 用 `ellipseDiameters().isNull()` 判断触点无效；
- 在 Widgets 中依赖点级 `accepted` 代替完整事件的接受状态；
- 在事件返回后继续依赖未复制的设备或事件上下文；
- 用 `normalizedPosition()` 计算当前窗口内比例，忽略它参考的是虚拟桌面。

## 9. 逐项 API 说明

### 类型与接受状态

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `enum State` | 表示点的阶段。 | `Stationary` 与 `Updated` 不是“是否仍按下”的简单布尔值。 |
| `Q_DECLARE_FLAGS(States, State)` | 组合多个点状态。 | 使用位运算；单点 `state()` 返回单个状态。 |
| `bool isAccepted() const` | 查询点级接受状态。 | Qt Quick 更常用；Widgets 通常处理完整事件。 |
| `void setAccepted(bool accepted = true)` | 设置点级接受状态。 | 不等价于设置整个 `QPointerEvent` 的接受状态。 |

### 构造、复制和比较

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `QEventPoint(int pointId = -1, const QPointingDevice *device = nullptr)` | 构造空的基础点，可附带输入设备。 | 默认 ID 为 `-1`；`device` 为借用指针，复杂事件历史仍未建立。 |
| `QEventPoint(int pointId, State state, const QPointF &scenePosition, const QPointF &globalPosition)` | 构造基本点值。 | 只提供基础位置和状态，历史与设备数据不完整。 |
| `QEventPoint(const QEventPoint &other)` | 浅复制点值。 | 显式共享数据，适合值传递。 |
| `QEventPoint(QEventPoint &&other)` | 移动点值。 | `noexcept`。 |
| `QEventPoint &operator=(const QEventPoint &other)` | 复制赋值。 | 复制的是点状态快照。 |
| `QEventPoint &operator=(QEventPoint &&other)` | 移动赋值。 | `noexcept`。 |
| `bool operator==(const QEventPoint &other) const` | 判断两个点是否相等。 | 不要据此判断是否属于同一实时输入流。 |
| `bool operator!=(const QEventPoint &other) const` | 判断两个点是否不相等。 | 与 `operator==` 语义对应。 |
| `void swap(QEventPoint &other)` | 交换两个点值。 | 不改变外部事件流的点身份。 |

### 坐标

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `position()` | 当前局部位置。 | 相对于接收 widget 或 item。 |
| `pressPosition()` | 按下时局部位置。 | 适合计算从起点的位移。 |
| `grabPosition()` | 抓取时局部位置。 | 抓取时刻不一定等于按下时刻。 |
| `lastPosition()` | 上次局部位置。 | 适合计算逐事件增量。 |
| `scenePosition()` | 当前场景位置。 | 参考空间依处理层级而定。 |
| `scenePressPosition()` | 按下时场景位置。 | 用于场景级起点计算。 |
| `sceneGrabPosition()` | 抓取时场景位置。 | 与 grab 生命周期对应。 |
| `sceneLastPosition()` | 上次场景位置。 | 适合场景拖动增量。 |
| `globalPosition()` | 当前屏幕或虚拟桌面位置。 | 多屏幕下属于虚拟桌面坐标。 |
| `globalPressPosition()` | 按下时全局位置。 | 不等于窗口局部位置。 |
| `globalGrabPosition()` | 抓取时全局位置。 | 屏幕级拖动起点。 |
| `globalLastPosition()` | 上次全局位置。 | 计算全局速度或增量。 |
| `normalizedPosition()` | 虚拟桌面归一化坐标。 | 范围概念是整个 `availableVirtualGeometry()`。 |

### 设备与动态属性

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `device()` | 获取产生该点的指针设备。 | 返回借用指针；设备能力决定数据可靠性。 |
| `id()` | 获取事件流中的点编号。 | 不保证跨会话稳定。 |
| `uniqueId()` | 获取设备提供的唯一点或笔标识。 | 触摸手指场景经常无效。 |
| `state()` | 获取当前点状态。 | 使用 `State` 枚举解释。 |
| `timestamp()` | 获取当前点时间戳。 | 由输入事件时间语义定义。 |
| `pressTimestamp()` | 获取最近按下时间戳。 | 与 `timeHeld()` 配合使用。 |
| `lastTimestamp()` | 获取上次 press 或 move 时间戳。 | 适合计算事件间隔。 |
| `timeHeld()` | 获取按下未释放的持续秒数。 | 释放后不要当作持续计时器。 |
| `pressure()` | 获取压力。 | 文档范围 `0.0` 到 `1.0`；设备可能不支持。 |
| `rotation()` | 获取接触方向角。 | 单位度；不支持的设备通常为零。 |
| `ellipseDiameters()` | 获取接触椭圆尺寸。 | 多数设备返回空尺寸。 |
| `velocity()` | 获取屏幕坐标系速度。 | 可能是系统值，也可能是 Qt 平滑估算。 |

## API 速查表

| 类别 | API | 解决什么问题 | 使用时重点注意 |
| --- | --- | --- | --- |
| 状态 | `state()` / `State` | 判断按下、移动、释放阶段。 | `Stationary`、`Updated` 是事件点状态。 |
| 接受 | `isAccepted()` / `setAccepted()` | 在 Qt Quick 中选择性接受点。 | Widgets 通常处理完整输入事件。 |
| 位置 | `position()` / `lastPosition()` | 计算局部逐帧位移。 | 两者必须属于同一坐标系。 |
| 位置 | `pressPosition()` | 计算从按下点的总位移。 | 不适合代替逐帧增量。 |
| 位置 | `grabPosition()` | 计算从抓取时刻的位移。 | 抓取时刻可能晚于按下。 |
| 坐标 | `scenePosition()` 系列 | 做场景或窗口级命中。 | 具体 scene 参考空间依处理层而变。 |
| 坐标 | `globalPosition()` 系列 | 做屏幕或虚拟桌面级定位。 | 多屏幕仍属于虚拟桌面坐标。 |
| 归一化 | `normalizedPosition()` | 得到虚拟桌面中的 `(0, 0)` 到 `(1, 1)` 位置。 | 不是当前窗口归一化坐标。 |
| 身份 | `id()` | 在连续事件中匹配同一点。 | 不当作永久身份。 |
| 身份 | `uniqueId()` | 获取硬件提供的点或笔标识。 | 先用 `isValid()` 检查。 |
| 设备 | `device()` | 获取输入设备及其能力。 | 返回借用指针。 |
| 时间 | `timestamp()` / `lastTimestamp()` | 计算事件时间间隔。 | 使用事件时间语义，不是 wall clock。 |
| 按住 | `pressTimestamp()` / `timeHeld()` | 实现长按和持续时间判断。 | 释放后状态不再表示“仍按住”。 |
| 物理属性 | `pressure()` / `rotation()` | 使用压力或方向输入。 | 设备可能不支持，默认值不代表真实测量。 |
| 形状 | `ellipseDiameters()` | 估算接触面积。 | 空尺寸是常见正常结果。 |
| 速度 | `velocity()` | 实现拖动或惯性反馈。 | 可能是 Qt 平滑估算值。 |
| 值语义 | 复制、移动、`operator==` | 保存或比较点快照。 | 不等于跨输入会话的身份比较。 |
| 构造 | `QEventPoint(id, device)` | 创建测试用或待填充的基础点。 | 默认 ID 为 `-1`，设备指针不转移所有权。 |

---

### 一句话总结

`QEventPoint` 是指针事件里的一个点快照：先确认状态和坐标系，再根据 press、last、grab 三类历史位置选择正确的位移算法。
