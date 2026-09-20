# QPointerEvent：统一描述鼠标、触控和笔输入的多点事件

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPointerEvent>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QInputEvent`

`QPointerEvent` 是指针输入事件的公共基类，承载一个或多个 `QEventPoint`、来源设备、指针类型、事件时间戳，以及每个点的接受状态和抓取关系。`QSinglePointEvent`、`QMouseEvent`、`QTabletEvent`、`QTouchEvent` 等具体事件在它之上提供更符合输入设备语义的接口。

它解决的是“同一套处理逻辑如何同时理解鼠标、手指和触控笔”的问题：事件处理代码可以统一遍历点、读取位置和状态，再根据具体事件类型决定按钮、压力、旋转或手势行为。

## 通常在哪里使用

应用代码很少直接实例化或继承 `QPointerEvent`。更常见的是在 `QWidget`、`QWindow`、`QGraphicsItem` 或 Qt Quick 输入处理器收到派生事件后，通过基类接口读取点：

```cpp
void CanvasWidget::touchEvent(QTouchEvent *event)
{
    for (const QEventPoint &point : event->points()) {
        switch (point.state()) {
        case QEventPoint::Pressed:
            beginStroke(point.id(), point.position());
            break;
        case QEventPoint::Updated:
            continueStroke(point.id(), point.position());
            break;
        case QEventPoint::Released:
            finishStroke(point.id(), point.position());
            break;
        default:
            break;
        }
    }

    event->accept();
}
```

对于鼠标或平板事件，点列表通常只有一个点，但 `QSinglePointEvent` 已经提供了 `position()`、`scenePosition()`、`globalPosition()` 和按钮状态等便利函数。只有在需要跨设备共用代码、处理多点触控或访问抓取关系时，才直接使用 `QPointerEvent` 的接口。

## 点列表、索引和 ID 不是一回事

`points()` 返回当前事件包含的所有 `QEventPoint`。`point(i)` 按当前列表索引访问；`pointById(id)` 按点的稳定标识查找。触摸点在后续事件中可能改变列表顺序，因此需要维护某根手指、某支笔的状态时，应保存 `QEventPoint::id()`，下一次用 `pointById()` 查找，而不是假设索引不变。

```cpp
if (QEventPoint *point = event->pointById(activePointId)) {
    updateCursor(point->position());
}
```

`points()` 是事件当下的快照引用，不是持续更新的设备状态。事件返回后不要保存其中的 `QEventPoint &`、列表引用或事件指针；需要异步处理时，复制出业务真正需要的坐标、ID、状态和时间戳。

列表可能为空，例如某些 `QTouchEvent::TouchCancel` 场景。调用 `point(0)` 或 `QSinglePointEvent::position()` 前，必须确认事件契约保证存在点；通用代码应先检查 `pointCount()` 或 `points().isEmpty()`。

## 事件接受与点接受

这里存在两套容易混淆的状态：

- `QEvent` / `QInputEvent` 的整体 accepted 状态表示接收者是否处理整个事件。
- `QEventPoint::accepted` 表示单个点是否被某个 Qt Quick Item 或 Handler 接受参与其手势。

在 Widgets 应用中，点级 accepted 通常不用于决定事件分发；应对完整的 `QTouchEvent`、`QMouseEvent` 等调用 `accept()` / `ignore()`。Qt Quick 可以让一个 Handler 只接受多点事件中的部分点，只有所有点都接受时才把整个事件交给对应的接收链路。

`allPointsAccepted()` 是对当前点列表逐点检查的汇总，不是“事件对象一定已接受”的替代。`setAccepted(bool)` 是 `QPointerEvent` 重载的整体操作入口；若代码需要 Qt Quick 的部分点手势语义，应使用 `QEventPoint::setAccepted()` 针对点处理，并在调用前确认框架的交付规则。

## 独占抓取与被动抓取

指针抓取解决“按下后指针离开原目标，后续移动和释放仍送给谁”的问题：

- **exclusive grabber**：某个对象独占后续更新和释放，其他目标可以被跳过。
- **passive grabbers**：对象也接收后续更新和释放，但不排除其他对象继续接收。

```cpp
const QEventPoint &point = event->points().first();
event->setExclusiveGrabber(point, handler);

QObject *owner = event->exclusiveGrabber(point);
```

这些 grabber API 主要供 Qt Quick Input Handlers 使用。Widgets 中的鼠标和触摸抓取通常由 Qt 的窗口/控件事件系统自动管理；不要在普通 `QWidget::mouseMoveEvent()` 中随意修改 `setExclusiveGrabber()`，以免绕过控件自己的抓取和传播规则。

`addPassiveGrabber()` 重复添加同一个对象时返回 `false`；首次加入返回 `true`。`removePassiveGrabber()` 只有在此前确实存在该对象时返回 `true`。`clearPassiveGrabbers()` 只清除给定点的被动抓取者，不会清除独占抓取者。

## 来源设备和统一指针类型

`pointingDevice()` 是 `QInputEvent::device()` 的 `QPointingDevice` 类型便利访问器；`pointerType()` 返回鼠标、手指、笔、橡皮等指针类型。若需要能力、按钮、轴、触控区域或设备名称，应继续查询返回的 `QPointingDevice`，不能仅凭 `pointerType()` 推断压力或旋转数据一定可用。

设备对象由 Qt 管理。不要删除返回的指针，也不要把它当作每个事件都新建的临时对象。若在异步任务中保存设备身份，保存所需的稳定信息或使用 Qt 对象关系管理，不要无条件持有裸指针。

## 继承事件与生命周期

`QPointerEvent` 继承 `QInputEvent`，因此还带有：

- `device()` / `deviceType()`：输入设备来源。
- `modifiers()` / `setModifiers()`：键盘修饰键。
- `timestamp()` / `setTimestamp()`：事件时间戳。
- `accept()`、`ignore()`、`isAccepted()`：整体事件接受状态。

事件对象由 Qt 在事件分发期间管理。自定义事件测试时可以使用公开构造器传入事件类型、指针设备、修饰键和点列表，但生产代码不应伪造系统输入事件来驱动控件；应调用控件公开的业务接口或使用真正的测试事件路径。

`QPointerEvent` 的可变操作应发生在事件所属线程的事件处理过程中。不要把同一个事件对象同时交给多个线程或在处理返回后继续修改；异步手势识别应复制必要数据后在线程间传递。

## 常见错误

- 用 `point(i)` 的索引作为手指身份：应保存 `QEventPoint::id()`。
- 假设每个指针事件至少有一个点：取消事件或平台特殊事件可能为空。
- 在 Widgets 中只设置某个点的 accepted，却没有接受整个 `QTouchEvent`：事件传播仍可能按整体 accepted 状态决定。
- 把 passive grabber 当作 exclusive grabber：前者不阻止其他接收者，后者才是独占后续交付。
- 在普通 QWidget 代码中手动修改抓取关系：通常应依赖 Qt 的鼠标/触摸抓取机制。
- 保存事件中的引用或 `pointingDevice()` 裸指针到异步任务：事件和设备的生命周期不能这样假定。
- 仅根据 `pointerType()` 就读取压力、倾斜或旋转：先检查设备能力和 `QEventPoint` 数据是否有效。

## API 速查表

### 构造与基础集合

| API | 语义与使用边界 |
| --- | --- |
| `QPointerEvent(Type type, const QPointingDevice *device, modifiers, points)` | 构造指针事件；应用通常读取派生事件，不直接伪造生产输入。 |
| `pointingDevice()` | 返回来源 `QPointingDevice`，等价于基类设备的类型化访问；不转移所有权。 |
| `pointerType()` | 返回来源设备的 `PointerType`；不能替代能力检查。 |
| `pointCount()` | 返回当前事件中的点数，可能为 `0`。 |
| `points()` | 返回所有 `QEventPoint` 的只读列表引用；只在事件处理期间使用。 |
| `point(qsizetype i)` | 按列表索引返回可修改点引用；索引必须有效，不能假设跨事件稳定。 |
| `pointById(int id)` | 按点 ID 查找，找不到返回 `nullptr`；适合追踪同一接触点。 |
| `setTimestamp(quint64)` | 设置整体时间戳并覆盖基类接口；通常由 Qt 输入系统或测试代码使用。 |

### 状态判断与接受

| API | 语义与使用边界 |
| --- | --- |
| `isBeginEvent()` | 判断是否代表指针/按钮开始；基类默认 `false`，由派生事件重载。 |
| `isUpdateEvent()` | 判断是否为没有按钮状态变化的更新事件；基类默认 `false`。 |
| `isEndEvent()` | 判断是否代表指针/按钮结束；基类默认 `false`。 |
| `allPointsAccepted()` | 只有当所有点的 `QEventPoint::isAccepted()` 都为真时才返回真。 |
| `setAccepted(bool)` | 设置整体事件接受状态的重载；Widgets 中优先使用事件整体 `accept()` / `ignore()`。 |
| `QEventPoint::isAccepted()` / `setAccepted(bool)` | 读取/设置单点接受状态；主要用于 Qt Quick 的部分点手势分流。 |

### 抓取关系

| API | 语义与使用边界 |
| --- | --- |
| `exclusiveGrabber(point)` | 返回为该点设置的独占接收对象；主要供 Qt Quick 使用。 |
| `setExclusiveGrabber(point, object)` | 使对象接收该点的后续更新和释放，并可跳过其他交付目标。 |
| `passiveGrabbers(point)` | 返回该点的被动接收对象列表；返回的是 `QPointer<QObject>`，对象销毁后可变为空指针。 |
| `addPassiveGrabber(point, object)` | 添加被动接收对象；已存在返回 `false`，首次添加返回 `true`；主要供 Qt Quick 使用。 |
| `removePassiveGrabber(point, object)` | 删除被动接收对象；确实删除返回 `true`，否则返回 `false`。 |
| `clearPassiveGrabbers(point)` | 清除给定点全部被动接收对象，不影响独占接收对象。 |
| `allPointsGrabbed()` | 当每个点都有独占抓取者或至少一个被动抓取者时返回真。 |

### 继承自 `QInputEvent` 的常用接口

| API | 语义与使用边界 |
| --- | --- |
| `device()` / `deviceType()` | 获取原始输入设备和设备类别。 |
| `modifiers()` / `setModifiers()` | 获取或设置键盘修饰键。 |
| `timestamp()` | 返回整体输入事件时间戳；单位和来源由 Qt 输入系统约定。 |
| `accept()` / `ignore()` / `isAccepted()` | 接受、忽略或查询完整输入事件；与点级 accepted 不是同一层状态。 |
