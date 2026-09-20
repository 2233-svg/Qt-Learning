# QPointingDevice

> Qt 6.11.1 · Qt GUI · 来自 `QPointingDevice`

## 1. 先建立直觉

`QPointingDevice` 是 `QInputDevice` 的指针输入子类，描述能在界面中产生位置点的设备：鼠标、手指、笔尖、橡皮擦端、puck 和类似设备。

它把两件容易混淆的事分开：

- `QInputDevice::DeviceType` 表示硬件或输入设备类别，例如触摸屏、触摸板、手写笔。
- `QPointingDevice::PointerType` 表示当前实际参与输入的“指针端”，例如手指、笔尖、橡皮擦、光标型 puck。

一支平板笔就是典型例子：设备类型可以是 `Stylus`，但不同事件的 pointer type 可以是 `Pen` 或 `Eraser`。

## 2. 类说明

`QPointingDevice` 继承自 `QInputDevice`。从 `QPointerEvent::pointingDevice()` 得到的就是这个类型，`QMouseEvent`、`QTouchEvent`、`QTabletEvent` 等指针事件都与它关联。

类说明只用于表明这些 API 来自 `QPointingDevice`：设备能力、名称和 seat 来自父类；最大触点数、按钮数、指针端类型、唯一 ID 与 point grab 通知由本类提供。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `enum PointerType` | 区分 Generic、Finger、Pen、Eraser、Cursor 等指针端类型。 |
| `enum GrabTransition` | 描述独占或被动 grab 的开始、结束、取消转换。 |
| `primaryPointingDevice(seatName)` | 返回指定 seat 的主指针设备。 |
| `pointerType() const` | 返回此设备当前代表的指针端类型。 |
| `maximumPoints() const` | 返回设备理论支持的最大并发触点数量。 |
| `buttonCount() const` | 返回设备可报告的按钮数量。 |
| `uniqueId() const` | 返回设备或工具唯一 ID 包装对象。 |
| `grabChanged(grabber, transition, event, point)` | grab 状态变化时发出，主要供高级输入处理和 Qt Quick 使用。 |
| `type() const` | 来自父类，返回设备大类。 |
| `hasCapability(capability) const` | 来自父类，判断是否支持压力、倾斜、滚动等扩展数据。 |

## 4. 关键用法

### 根据 pointer type 切换工具

```cpp
void DrawingSurface::tabletEvent(QTabletEvent *event)
{
    switch (event->pointerType()) {
    case QPointingDevice::PointerType::Eraser:
        erase(event->position(), event->pressure());
        break;
    case QPointingDevice::PointerType::Pen:
        draw(event->position(), event->pressure());
        break;
    default:
        break;
    }
    event->accept();
}
```

相比只判断 `deviceType() == Stylus`，pointer type 能识别同一设备的笔尖与橡皮擦端。

### 为多点设备设置合理上限

```cpp
void GestureController::configure(const QPointingDevice *device)
{
    m_supportsPinch = device && device->maximumPoints() >= 2;
    m_supportsThreeFingerAction = device && device->maximumPoints() >= 3;
}
```

`maximumPoints()` 是设备能力描述，不代表每次事件都会带来这么多点。运行时手势仍要以 `QPointerEvent::pointCount()` 为准。

### 了解 grab 变化而不是滥用 grab

`grabChanged()` 适合调试和高级输入框架。例如手势竞争中，一个对象失去独占 grab，说明后续点更新可能不再发送给它。普通 Widgets 应用通常无需监听或主动修改 grab，正确地接受/忽略事件已经足够。

## 5. 使用场景

`QPointingDevice` 适合绘画、签名、白板、地图、手势编辑器、多点触控工作台、工业触控屏和复杂 Qt Quick 输入组件。

它也适合可配置输入策略。比如应用可以检测设备支持的最大点数，只在多点可用时展示双指旋转或三指快捷手势；在只有鼠标的环境自动退回单点模式。

对专业绘图应用，`uniqueId()` 和 pointer type 可以辅助识别不同笔或不同笔端，但应用逻辑仍应保留未知/无效 ID 的降级路径。

## 6. 常见坑与经验

不要把 `maximumPoints()` 当成当前触点数。它是设备上限；当前事件的实际点数应看 `pointCount()`。

不要把 pointer type 和 device type 视为同一枚举。一个回答“是什么设备”，一个回答“哪种指针端在输入”。

不要认为 `uniqueId()` 一定有效。某些平台或设备无法提供稳定工具 ID，此时应通过无效 ID 分支正常工作。

不要主动干预 grab，除非你在写输入分发层或理解 Qt Quick 手势竞争模型。对常规 Widgets，grab 改错会导致后续 release 或 move 消失。

## 7. 知识点覆盖

学习 `QPointingDevice` 应覆盖设备类型与指针类型、最大触点数、按钮数、笔尖与橡皮擦、工具唯一标识、独占/被动 grab、手势竞争、多设备降级策略和 Qt 6 指针输入模型。
