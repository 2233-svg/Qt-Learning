# QPointingDevice：描述鼠标、触摸和数位板设备

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPointingDevice>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QInputDevice -> QPointingDevice`  
> 类型性质：`QObject` 平台输入设备描述对象

`QPointingDevice` 描述产生鼠标、触摸或数位板事件的输入设备。`QPointerEvent` 会携带一个设备指针，应用可以通过它查询设备类型、能力、最大触点数、按钮数量以及指针类型。

它解决的是“这组指针事件来自什么设备、设备具备什么能力”的问题，而不是保存某次触摸的坐标或状态。单个触点的坐标、压力、旋转、状态和唯一对象 ID，应从 `QEventPoint` 获取。

## 实际使用场景

### 从指针事件读取设备信息

```cpp
void Canvas::mousePressEvent(QMouseEvent *event)
{
    const QPointingDevice *device = event->device();
    if (!device)
        return;

    if (device->pointerType() == QPointingDevice::PointerType::Pen)
        beginStroke(event->position());
}
```

实际事件处理通常不需要自己创建 `QPointingDevice`。平台插件或通用输入插件会注册设备，事件中的 `device()` 返回对应的全局对象。

### 区分手指、笔尖和橡皮擦

```cpp
switch (event->device()->pointerType()) {
case QPointingDevice::PointerType::Finger:
    handleTouchGesture(event);
    break;
case QPointingDevice::PointerType::Pen:
    handlePenStroke(event);
    break;
case QPointingDevice::PointerType::Eraser:
    eraseStroke(event);
    break;
default:
    handleGenericPointer(event);
    break;
}
```

`QInputDevice::DeviceType` 描述设备本身，例如触摸屏或数位板；`PointerType` 描述当前交互端，例如手指、笔尖或橡皮擦。两者有一定重复，但不能完全互换。数位笔的两端尤其需要依赖 `PointerType` 区分。

## 生命周期与所有权

### 应用通常只读取注册设备

Qt 文档明确指出，平台或通用插件负责通过 `QWindowSystemInterface` 注册可用指向设备。应用不需要为了处理事件而自行实例化此类，应该使用 `QPointerEvent::device()`、`QInputEvent::device()` 或 `primaryPointingDevice()` 返回的对象。

这些设备对象通常由 Qt 的输入系统管理。不要删除事件中的设备指针，也不要把它当作应用拥有的临时对象。若要监听其信号，应使用合适的 context 对象，避免接收者生命周期结束后仍执行槽函数。

### 自定义设备构造

带完整参数的构造函数主要服务于平台插件、输入设备集成和测试。普通业务代码若构造了对象，它不会自动成为系统实际使用的设备，也不会自动产生输入事件。

默认构造创建一个无效的 pointing device 实例，适合内部初始化或测试，不代表真实鼠标、触摸屏或数位板。

## 属性与能力

`buttonCount` 是设备最多能检测的板载按钮数量；`maximumPoints` 是设备最多能同时检测的触点数量；`pointerType` 是设备当前交互端的类型；`uniqueId` 是设备级 ID，文档认为它的实用性有限，跟踪触摸对象时通常应关注 `QEventPoint::uniqueId()`。

这些属性都是只读常量属性。它们描述设备注册时的能力，不是当前事件中“实际按下了几个按钮”或“当前有几个触点”。当前事件的状态仍要从事件对象和事件点读取。

## `PointerType` 与 `PointerTypes`

`PointerType` 是强类型枚举，表示与设备交互的对象或设备端：

| 值 | 含义 |
| --- | --- |
| `Unknown` | 类型未知 |
| `Generic` | 鼠标或类似鼠标的指针 |
| `Finger` | 用户手指 |
| `Pen` | 数位笔的书写端 |
| `Eraser` | 数位笔的橡皮擦端 |
| `Cursor` | 带十字准星的 puck/cursor |
| `AllPointerTypes` | 所有上述类型，常用作过滤器默认值 |

`PointerTypes` 是 `QFlags<PointerType>`，可以保存多个类型的按位 OR 组合：

```cpp
QPointingDevice::PointerTypes accepted =
    QPointingDevice::PointerType::Finger
    | QPointingDevice::PointerType::Pen;
```

`Unknown` 的值是 0，不能把它和其他类型进行有意义的按位组合；`AllPointerTypes` 更适合作为过滤条件，而不是某个设备的实际单一类型。

## 抓取变化信号

### `grabChanged`

`grabChanged` 在某个对象获得或失去某个事件点的 exclusive/passive grab 时发出。`transition` 说明是获得、正常释放、取消还是被其他对象接管；`event` 和 `point` 指向发生变化的输入上下文。

从一个对象转移到另一个对象时，通常会产生两次通知：旧 grabber 收到失去通知，新 grabber 收到获得通知。连接信号时不要只处理“获得”而忽略取消和正常释放，否则状态表容易泄漏。

## 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

```cpp
#include <QPointingDevice>
#include <QPointerEvent>
#include <QEventPoint>
```

## API 逐项说明

### 枚举与标志

#### `enum QPointingDevice::GrabTransition`

用于描述 exclusive 或 passive grab 在对象之间的转移，并作为 `grabChanged` 的参数。

| 常量 | 值 | 语义 |
| --- | --- | --- |
| `GrabPassive` | `0x01` | `QPointerEvent::addPassiveGrabber()` 之后发出 |
| `UngrabPassive` | `0x02` | passive grab 正常结束时发出 |
| `CancelGrabPassive` | `0x03` | passive grab 异常结束，例如手势取消 |
| `OverrideGrabPassive` | `0x04` | 当前未使用 |
| `GrabExclusive` | `0x10` | `QPointerEvent::setExclusiveGrabber()` 之后发出 |
| `UngrabExclusive` | `0x20` | exclusive grabber 设置为 `nullptr`，正常结束 |
| `CancelGrabExclusive` | `0x30` | exclusive grabber 被另一个对象替换，旧 grab 被接管 |

不要只判断“是否有 grabber”，应根据 transition 区分正常释放和取消。

#### `enum class QPointingDevice::PointerType`

表示当前与 pointing device 交互的指针端或对象。它和 `QInputDevice::DeviceType` 不完全等价；例如同一个数位板设备的笔尖和橡皮擦端可以具有不同的 `PointerType`。

#### `QPointingDevice::PointerTypes`

`QFlags<PointerType>` 的别名，用于组合多个 `PointerType`。使用 `testFlag()`、按位 OR 等 `QFlags` API 操作。

### 属性

#### `[read-only] PointerType QPointingDevice::pointerType`

返回设备交互端类型。属性只读，使用 `pointerType()` 获取。未知、通用鼠标、手指、笔、橡皮擦和准星 cursor 的语义见 `PointerType`。

#### `[read-only] int QPointingDevice::maximumPoints`

返回设备可同时检测的最大触点数。它是设备能力上限，不是当前事件中的触点数；当前触点数量应从事件点集合读取。

#### `[read-only] int QPointingDevice::buttonCount`

返回设备最多能检测的板载按钮数量。它不是当前按下按钮的数量，按键状态应从具体鼠标或指针事件读取。

#### `[read-only] QPointingDeviceUniqueId QPointingDevice::uniqueId`

返回设备级 unique ID。该 ID 的用途有限，文档建议跟踪触摸对象时使用 `QEventPoint::uniqueId()`，不要把设备级 ID 和触点级 ID 混为一谈。

### 构造与对象语义

#### `QPointingDevice::QPointingDevice(QObject *parent = nullptr)`

创建一个无效的 pointing device 子对象。父对象遵循 `QObject` 所有权规则，但该对象不会因为构造就自动注册为系统输入设备。

#### `QPointingDevice::QPointingDevice(const QString &name, qint64 systemId, QInputDevice::DeviceType deviceType, PointerType pointerType, QInputDevice::Capabilities capabilities, int maxPoints, int buttonCount, const QString &seatName = QString(), QPointingDeviceUniqueId uniqueId = QPointingDeviceUniqueId(), QObject *parent = nullptr)`

按名称、系统 ID、设备类型、指针类型、能力、最大触点数、按钮数、seat、设备级 unique ID 和父对象创建设备描述。主要供平台或输入插件注册设备使用；普通应用构造后仍不会自动接入事件分发。

`maxPoints`、`buttonCount` 是声明的设备能力，不会动态反映当前状态。`deviceType` 和 `capabilities` 来自 `QInputDevice`，应使用与具体平台设备一致的值。

#### `QPointingDevice::~QPointingDevice()`

销毁设备描述对象。应用不应删除由 Qt 输入系统管理、且仍可能被事件引用的全局设备对象。

#### `QPointingDevice(const QPointingDevice &) = delete`

该 QObject 派生类不可复制。

#### `QPointingDevice &operator=(const QPointingDevice &) = delete`

该 QObject 派生类不可复制赋值。

### 属性访问器

#### `QPointingDevice::PointerType QPointingDevice::pointerType() const`

读取 `pointerType` 属性。用它区分手指、笔尖、橡皮擦和通用指针；若业务只关心设备类别，再读取继承自 `QInputDevice` 的 `type()`。

#### `int QPointingDevice::maximumPoints() const`

读取最大同时触点数。鼠标等非多点设备的值不应被解释为当前触点数量。

#### `int QPointingDevice::buttonCount() const`

读取最大板载按钮数。它不替代事件中的按钮状态查询。

#### `QPointingDeviceUniqueId QPointingDevice::uniqueId() const`

读取设备级 unique ID。跟踪单个触点或触控对象时，优先使用 `QEventPoint::uniqueId()`。

### 全局设备查询

#### `static const QPointingDevice *QPointingDevice::primaryPointingDevice(const QString &seatName = QString())`

返回指定 seat 上的主 pointing device，传统上通常是鼠标或触控板。

Qt 会优先选择与 seat 匹配、且没有另一个父设备的鼠标或触控板。如果没有找到，函数可能创建一个虚拟的“核心指针”鼠标，以便没有完整设备发现机制的平台仍能工作。返回指针由 Qt 管理，调用方不能删除。

空 `seatName` 使用默认 seat；多 seat 平台应传入明确名称，避免查到错误设备。

### 信号

#### `void QPointingDevice::grabChanged(QObject *grabber, GrabTransition transition, const QPointerEvent *event, const QEventPoint &point) const`

当 `grabber` 对 `point` 获得或失去 exclusive/passive grab 时发出。`transition` 区分获得、释放、取消和接管。

从旧对象转移到新对象通常会发出两次信号。处理槽函数时要考虑 `event`、`point` 的上下文只在通知期间有效，并使用 context 连接管理接收者生命周期。

### 已弃用的修改接口

#### `void setType(QInputDevice::DeviceType type)`（已弃用）

Qt 6.0 起弃用。设备类型应在构造函数中提供，不要在对象建立后修改。

#### `void setCapabilities(QInputDevice::Capabilities capabilities)`（已弃用）

Qt 6.0 起弃用。设备能力应在构造函数中声明。

#### `void setMaximumTouchPoints(int count)`（已弃用）

Qt 6.0 起弃用。最大触点数应在构造函数中提供。

## 常见错误排查

1. **自己创建设备后期待收到事件**：构造对象不会自动注册；使用事件里的 `device()` 或平台注册机制。
2. **删除 `event->device()` 返回的指针**：这些对象通常由 Qt 输入系统管理，应用不拥有它们。
3. **把 `pointerType` 当成 `DeviceType`**：前者描述交互端，后者描述设备类别；数位板尤其需要区分两者。
4. **把 `maximumPoints` 当作当前触点数量**：它只是硬件能力上限。
5. **把 `buttonCount` 当作当前按下按钮数**：按钮状态要从具体输入事件读取。
6. **跟踪触点时使用设备的 `uniqueId`**：应使用 `QEventPoint::uniqueId()`；设备级 ID 不等于对象级 ID。
7. **忽略 `grabChanged` 的取消通知**：正常释放和异常取消都要清理应用自己的 grab 状态。
8. **在多 seat 环境使用空 seat 名称**：传递明确 `seatName`，避免依赖默认 seat。
9. **继续调用弃用 setter**：在构造函数中一次性传入类型、能力和最大触点数。

## API 速查表

| 类别 | API | 作用 | 关键边界与注意事项 |
| --- | --- | --- | --- |
| 枚举 | `GrabTransition` | 描述 grab 获得、释放、取消和接管 | 作为 `grabChanged` 参数；不要只判断是否有 grabber |
| 枚举 | `PointerType` | 描述手指、鼠标、笔尖、橡皮擦等交互端 | 与 `QInputDevice::DeviceType` 不完全等价 |
| 标志 | `PointerTypes` | 组合多个 `PointerType` | 是 `QFlags<PointerType>` |
| 属性 | `pointerType` | 读取指针类型 | 只读；未知值要保留兼容分支 |
| 属性 | `maximumPoints` | 读取最大同时触点数 | 是能力上限，不是当前点数 |
| 属性 | `buttonCount` | 读取最大板载按钮数 | 不是当前按下按钮数 |
| 属性 | `uniqueId` | 读取设备级 ID | 触点跟踪应使用 `QEventPoint::uniqueId()` |
| 构造 | `QPointingDevice(QObject *)` | 创建无效设备描述对象 | 不会自动注册到输入系统 |
| 构造 | 完整参数构造函数 | 创建带平台能力信息的设备描述 | 主要供平台/通用插件使用 |
| 生命周期 | `~QPointingDevice()` | 销毁设备描述 | 不要删除 Qt 管理的全局设备 |
| 访问器 | `pointerType()` | 获取指针类型 | 用于区分手指、笔尖和橡皮擦 |
| 访问器 | `maximumPoints()` | 获取最大触点数 | 非当前状态 |
| 访问器 | `buttonCount()` | 获取最大按钮数 | 非当前状态 |
| 访问器 | `uniqueId()` | 获取设备级 unique ID | 不等于触点级 ID |
| 查询 | `primaryPointingDevice(seatName)` | 获取 seat 的主指针设备 | 返回对象由 Qt 管理；无设备时可能创建虚拟核心鼠标 |
| 信号 | `grabChanged(grabber, transition, event, point)` | 通知 grab 状态变化 | 转移可能产生两次信号；处理正常释放和取消 |
| 弃用 | `setType()` | 修改设备类型 | Qt 6.0 起弃用，改用构造函数 |
| 弃用 | `setCapabilities()` | 修改设备能力 | Qt 6.0 起弃用，改用构造函数 |
| 弃用 | `setMaximumTouchPoints()` | 修改最大触点数 | Qt 6.0 起弃用，改用构造函数 |
| 对象语义 | 禁止拷贝/赋值 | 遵守 QObject 身份语义 | 设备对象通过指针引用 |

### 一句话总结

`QPointingDevice` 是输入设备的能力和身份描述对象：通常从 `QPointerEvent` 读取而不是自行创建，使用 `PointerType` 处理交互端，使用 `QEventPoint` 处理具体触点，并把 Qt 管理的设备对象视为非拥有指针。
