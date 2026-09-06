# QInputDevice

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QInputDevice` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QInputDevice` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QInputDevice>`
- 继承自：QObject
- 直接派生类：QPointingDevice

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

### 状态、生命周期和线程

**生命周期：** 先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

**状态与结果：** QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

**线程与事件循环：** QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

## 3. 直接使用

使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `flags Capabilities`
- `enum class Capability { None, Position, Area, Pressure, Velocity, …, All }`
- `enum class DeviceType { Unknown, Mouse, TouchScreen, TouchPad, Stylus, …, AllDevices }`
- `flags DeviceTypes`

### 属性

- `availableVirtualGeometry : QRect`
- `capabilities : Capabilities`
- `name : const QString`
- `seatName : const QString`
- `systemId : const qint64`
- `type : const DeviceType`

### 公有函数

- `QInputDevice(QObject *parent = nullptr)`
- `QInputDevice(const QString &name, qint64 id, QInputDevice::DeviceType type, const QString &seatName = QString(), QObject *parent = nullptr)`
- `QRect availableVirtualGeometry() const`
- `QInputDevice::Capabilities capabilities() const`
- `bool hasCapability(QInputDevice::Capability capability) const`
- `QString name() const`
- `QString seatName() const`
- `qint64 systemId() const`
- `QInputDevice::DeviceType type() const`

### 信号

- `void availableVirtualGeometryChanged(QRect area)`
- `void capabilitiesChanged(QInputDevice::Capabilities capabilities)`

### 静态公有成员

- `QList<const QInputDevice *> devices()`
- `const QInputDevice * primaryKeyboard(const QString &seatName = QString())`
- `(since 6.3) QStringList seatNames()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum class QInputDevice::Capabilityflags QInputDevice::Capabilities`

**作用与语义：**

表示输入设备或其驱动程序能提供哪些信息。
- `QInputDevice::Capability::None`：`0`;没有关于输入设备能力的信息。
- `QInputDevice::Capability::Position`：`0x0001`;表示位置信息可用，意味着接触点中的位置()函数族返回有效点。
- `QInputDevice::Capability::Area`：`0x0002`;表示触控区域信息可用，意味着触点中的`QEventPoint::ellipseDiameters()`返回有效值。
- `QInputDevice::Capability::Pressure`：`0x0004`;表示压力信息可用，意味着`QEventPoint::pressure()`返回有效值。
- `QInputDevice::Capability::Velocity`：`0x0008`;表示速度信息可用，意味着`QEventPoint::velocity()`返回有效矢量。
- `QInputDevice::Capability::NormalizedPosition`：`0x0020`;表示归一化位置可用，意味着`QEventPoint::globalPosition()`返回有效值。
- `QInputDevice::Capability::MouseEmulation`：`0x0040`;表示该设备合成鼠标事件。
- `QInputDevice::Capability::Scroll`：`0x0100`;表示该设备具备滚动功能。
- `QInputDevice::Capability::PixelScroll (since Qt 6.2)`：`0x0080`;表示设备（通常是`touchpad`）以像素精度滚动。
- `QInputDevice::Capability::Hover`：`0x0200`;表示该装置具备悬停能力。
- `QInputDevice::Capability::Rotation`：`0x0400`;表示`rotation`信息可用。
- `QInputDevice::Capability::XTilt`：`0x0800`;表示X轴`tilt`信息可用。
- `QInputDevice::Capability::YTilt`：`0x1000`;表示Y轴`tilt`信息可用。
- `QInputDevice::Capability::TangentialPressure`：`0x2000`;表示切向压力信息可用。
- `QInputDevice::Capability::ZPosition`：`0x4000`;表示`Z-axis`位置信息可用。
- `QInputDevice::Capability::All`：`0x7FFFFFFF`
能力类型是QFlag的typedef<Capability>。它存储能力值的或组合。

### `enum class QInputDevice::DeviceTypeflags QInputDevice::DeviceTypes`

**作用与语义：**

这个枚举代表产生`QPointerEvent`的设备类型。
- `QInputDevice::DeviceType::Unknown`：`0x0000`;无法识别该装置。
- `QInputDevice::DeviceType::Mouse`：`0x0001`;一只老鼠。
- `QInputDevice::DeviceType::TouchScreen`：`0x0002`;在这种类型的设备中，触摸面和显示是集成的。这意味着表面和显示通常大小相同，因此触点的物理位置与`QEventPoint`报告的坐标之间存在直接关系。因此，Qt 允许用户同时直接与多个 QWidget、QGraphicsItems 或 Qt 快速项目交互。
- `QInputDevice::DeviceType::TouchPad`：`0x0004`;在这种类型的设备中，触摸面与显示屏是分开的。物理触摸位置与屏幕坐标之间没有直接关系。它们是相对于当前鼠标位置计算的，用户必须使用触摸板移动该参考点。与触摸屏不同，Qt 允许用户一次只能与单个`QWidget`或`QGraphicsItem`交互。
- `QInputDevice::DeviceType::Stylus`：`0x0010`;一种类似笔的设备，用于绘图板如Wacom绘图板，或在触摸屏上提供独立的触控笔感应功能。
- `QInputDevice::DeviceType::Airbrush`：`0x0020`;带有摇滚的触针，用于调节`tangentialPressure`。
- `QInputDevice::DeviceType::Puck`：`0x0008`;一种类似于扁平鼠标的装置，带有透明圆圈和十字准星。
- `QInputDevice::DeviceType::Keyboard`：`0x1000`;键盘。
- `QInputDevice::DeviceType::AllDevices`：`0x7FFFFFFF`;上述任意一种（作为默认滤波器值）。
DeviceTypes 类型是 QFlag 的 typedef<DeviceType>。它存储 DeviceType 值的 OR 组合。

### `[read-only] availableVirtualGeometry : QRect`

**作用与语义：**

该属性包含该设备可访问的虚拟桌面区域。
例如，`TouchScreen`输入设备固定在单个物理屏幕上，通常校准使该区域与`QScreen::geometry()`相同，而`Mouse`通常能够访问虚拟桌面上的所有屏幕。
另外，Wacom图形绘板也可以配置为映射到所有屏幕，或仅映射到用户偏好绘制的屏幕，或仅映射到绘图发生的窗口。
集成触摸屏的`Stylus`设备可能在物理上仅限于该屏幕。
如果返回的矩形是`null`的，说明该设备可以访问整个虚拟桌面。

**如何使用：** 调用 `availableVirtualGeometry()` 读取当前值；它不会修改应用状态。

### `[read-only] capabilities : Capabilities`

**作用与语义：**

此属性保存设备能力。

**如何使用：** 调用 `capabilities()` 读取当前值；它不会修改应用状态。

### `[read-only] name : const QString`

**作用与语义：**

此属性保存设备名称。

**如何使用：** 调用 `name()` 读取当前值；它不会修改应用状态。

### `[read-only] seatName : const QString`

**作用与语义：**

该属性包含与设备相关联的座椅。

**如何使用：** 调用 `seatName()` 读取当前值；它不会修改应用状态。

### `[read-only] systemId : const qint64`

**作用与语义：**

该属性包含平台特定的系统ID。

**如何使用：** 调用 `systemId()` 读取当前值；它不会修改应用状态。

### `[read-only] type : const DeviceType`

**作用与语义：**

此属性保存设备类型。

**如何使用：** 调用 `type()` 读取当前值；它不会修改应用状态。

### `QInputDevice::QInputDevice(QObject *parent = nullptr)`

**作用与语义：**

作为`parent`的子节点创建一个新的无效输入设备实例。

### `QInputDevice::QInputDevice(const QString &name, qint64 id, QInputDevice::DeviceType type, const QString &seatName = QString(), QObject *parent = nullptr)`

**作用与语义：**

创建一个新的输入设备实例。给定的`name`通常是制造商分配的型号名称（如有的话），或是其他可识别的名称;`id` 是一个平台特定的编号，每个设备都是唯一的（例如 X11 上的 xinput ID）;`type` 用于识别设备类型。在能够同时处理多个用户或多个输入设备组输入的窗口系统（如 Wayland 或 X11）上，`seatName` 标识将共同使用的设备集合名称。如果设备是子设备或从设备（例如可以轮流移动“核心指针”的几只鼠标之一），主设备应作为`parent`。
平台插件创建、注册并继续拥有每个设备实例;通常`parent`应为内存管理目的提供，即使某设备没有主节点。
默认情况下，`capabilities()`是`None`。

### `QInputDevice::Capabilities QInputDevice::capabilities() const`

**作用与语义：**

恢复设备功能。
注意：属性能力的获取函数。

### `[static] QList<const QInputDevice *> QInputDevice::devices()`

**作用与语义：**

返回所有注册输入设备（键盘和指向设备）的列表。
注意：设备列表并非所有平台都完整。目前，最完整的信息出现在Linux平台启动时及热插拔响应时。大多数其他平台只能在收到事件后提供各种类型的通用设备;大多数平台不会在运行时告知Qt设备已插入或拔除电源。
注意：返回的列表无法用于添加新设备。若要添加模拟触摸屏进行自动测试，可以使用`QTest::createTouchDevice()`。平台插件应调用QWindowSystemInterface：：registerInputDevice()以添加发现的设备。

### `bool QInputDevice::hasCapability(QInputDevice::Capability capability) const`

**作用与语义：**

返回设备能力是否包含给定`capability`。

### `QString QInputDevice::name() const`

**作用与语义：**

返回设备名称。
该字符串可能是空的。不过，在拥有多个输入设备的系统中，它非常有用：可以用来区分`QPointerEvent`的来源。
注意：物业名称的获取函数。

### `[static] const QInputDevice *QInputDevice::primaryKeyboard(const QString &seatName = QString())`

**作用与语义：**

将核心键盘或主键盘放回指定座位`seatName`。

### `QString QInputDevice::seatName() const`

**作用与语义：**

如果已知，返回该设备所关联的座位;否则为空。
原本打算由单一用户一起使用的设备，可以配置为相同的座椅名称。目前仅在Wayland和X11平台上支持此功能。
注意：属性 seatName 的获取函数。

### `[static, since 6.3] QStringList QInputDevice::seatNames()`

**作用与语义：**

返回所有注册输入设备（键盘和指点设备）的座位名称列表。

### `qint64 QInputDevice::systemId() const`

**作用与语义：**

返回平台特定的系统ID（例如X11平台上的xinput ID）。
所有平台都应为每个设备提供唯一的系统ID。
注意：属性systemId的Getter函数。

### `QInputDevice::DeviceType QInputDevice::type() const`

**作用与语义：**

返回设备类型。
注意：属性类型的 Getter 函数。

### `flags Capabilities`

**作用与语义：**

表示输入设备或其驱动程序能提供哪些信息。
- `QInputDevice::Capability::None`：`0`;没有关于输入设备能力的信息。
- `QInputDevice::Capability::Position`：`0x0001`;表示位置信息可用，意味着接触点中的位置()函数族返回有效点。
- `QInputDevice::Capability::Area`：`0x0002`;表示触控区域信息可用，意味着触点中的`QEventPoint::ellipseDiameters()`返回有效值。
- `QInputDevice::Capability::Pressure`：`0x0004`;表示压力信息可用，意味着`QEventPoint::pressure()`返回有效值。
- `QInputDevice::Capability::Velocity`：`0x0008`;表示速度信息可用，意味着`QEventPoint::velocity()`返回有效矢量。
- `QInputDevice::Capability::NormalizedPosition`：`0x0020`;表示归一化位置可用，意味着`QEventPoint::globalPosition()`返回有效值。
- `QInputDevice::Capability::MouseEmulation`：`0x0040`;表示该设备合成鼠标事件。
- `QInputDevice::Capability::Scroll`：`0x0100`;表示该设备具备滚动功能。
- `QInputDevice::Capability::PixelScroll (since Qt 6.2)`：`0x0080`;表示设备（通常是`touchpad`）以像素精度滚动。
- `QInputDevice::Capability::Hover`：`0x0200`;表示该装置具备悬停能力。
- `QInputDevice::Capability::Rotation`：`0x0400`;表示`rotation`信息可用。
- `QInputDevice::Capability::XTilt`：`0x0800`;表示X轴`tilt`信息可用。
- `QInputDevice::Capability::YTilt`：`0x1000`;表示Y轴`tilt`信息可用。
- `QInputDevice::Capability::TangentialPressure`：`0x2000`;表示切向压力信息可用。
- `QInputDevice::Capability::ZPosition`：`0x4000`;表示`Z-axis`位置信息可用。
- `QInputDevice::Capability::All`：`0x7FFFFFFF`
能力类型是QFlag的typedef<Capability>。它存储能力值的或组合。

### `enum class Capability { None, Position, Area, Pressure, Velocity, …, All }`

**作用与语义：**

表示输入设备或其驱动程序能提供哪些信息。
- `QInputDevice::Capability::None`：`0`;没有关于输入设备能力的信息。
- `QInputDevice::Capability::Position`：`0x0001`;表示位置信息可用，意味着接触点中的位置()函数族返回有效点。
- `QInputDevice::Capability::Area`：`0x0002`;表示触控区域信息可用，意味着触点中的`QEventPoint::ellipseDiameters()`返回有效值。
- `QInputDevice::Capability::Pressure`：`0x0004`;表示压力信息可用，意味着`QEventPoint::pressure()`返回有效值。
- `QInputDevice::Capability::Velocity`：`0x0008`;表示速度信息可用，意味着`QEventPoint::velocity()`返回有效矢量。
- `QInputDevice::Capability::NormalizedPosition`：`0x0020`;表示归一化位置可用，意味着`QEventPoint::globalPosition()`返回有效值。
- `QInputDevice::Capability::MouseEmulation`：`0x0040`;表示该设备合成鼠标事件。
- `QInputDevice::Capability::Scroll`：`0x0100`;表示该设备具备滚动功能。
- `QInputDevice::Capability::PixelScroll (since Qt 6.2)`：`0x0080`;表示设备（通常是`touchpad`）以像素精度滚动。
- `QInputDevice::Capability::Hover`：`0x0200`;表示该装置具备悬停能力。
- `QInputDevice::Capability::Rotation`：`0x0400`;表示`rotation`信息可用。
- `QInputDevice::Capability::XTilt`：`0x0800`;表示X轴`tilt`信息可用。
- `QInputDevice::Capability::YTilt`：`0x1000`;表示Y轴`tilt`信息可用。
- `QInputDevice::Capability::TangentialPressure`：`0x2000`;表示切向压力信息可用。
- `QInputDevice::Capability::ZPosition`：`0x4000`;表示`Z-axis`位置信息可用。
- `QInputDevice::Capability::All`：`0x7FFFFFFF`
能力类型是QFlag的typedef<Capability>。它存储能力值的或组合。

### `enum class DeviceType { Unknown, Mouse, TouchScreen, TouchPad, Stylus, …, AllDevices }`

**作用与语义：**

这个枚举代表产生`QPointerEvent`的设备类型。
- `QInputDevice::DeviceType::Unknown`：`0x0000`;无法识别该装置。
- `QInputDevice::DeviceType::Mouse`：`0x0001`;一只老鼠。
- `QInputDevice::DeviceType::TouchScreen`：`0x0002`;在这种类型的设备中，触摸面和显示是集成的。这意味着表面和显示通常大小相同，因此触点的物理位置与`QEventPoint`报告的坐标之间存在直接关系。因此，Qt 允许用户同时直接与多个 QWidget、QGraphicsItems 或 Qt 快速项目交互。
- `QInputDevice::DeviceType::TouchPad`：`0x0004`;在这种类型的设备中，触摸面与显示屏是分开的。物理触摸位置与屏幕坐标之间没有直接关系。它们是相对于当前鼠标位置计算的，用户必须使用触摸板移动该参考点。与触摸屏不同，Qt 允许用户一次只能与单个`QWidget`或`QGraphicsItem`交互。
- `QInputDevice::DeviceType::Stylus`：`0x0010`;一种类似笔的设备，用于绘图板如Wacom绘图板，或在触摸屏上提供独立的触控笔感应功能。
- `QInputDevice::DeviceType::Airbrush`：`0x0020`;带有摇滚的触针，用于调节`tangentialPressure`。
- `QInputDevice::DeviceType::Puck`：`0x0008`;一种类似于扁平鼠标的装置，带有透明圆圈和十字准星。
- `QInputDevice::DeviceType::Keyboard`：`0x1000`;键盘。
- `QInputDevice::DeviceType::AllDevices`：`0x7FFFFFFF`;上述任意一种（作为默认滤波器值）。
DeviceTypes 类型是 QFlag 的 typedef<DeviceType>。它存储 DeviceType 值的 OR 组合。

### `flags DeviceTypes`

**作用与语义：**

这个枚举代表产生`QPointerEvent`的设备类型。
- `QInputDevice::DeviceType::Unknown`：`0x0000`;无法识别该装置。
- `QInputDevice::DeviceType::Mouse`：`0x0001`;一只老鼠。
- `QInputDevice::DeviceType::TouchScreen`：`0x0002`;在这种类型的设备中，触摸面和显示是集成的。这意味着表面和显示通常大小相同，因此触点的物理位置与`QEventPoint`报告的坐标之间存在直接关系。因此，Qt 允许用户同时直接与多个 QWidget、QGraphicsItems 或 Qt 快速项目交互。
- `QInputDevice::DeviceType::TouchPad`：`0x0004`;在这种类型的设备中，触摸面与显示屏是分开的。物理触摸位置与屏幕坐标之间没有直接关系。它们是相对于当前鼠标位置计算的，用户必须使用触摸板移动该参考点。与触摸屏不同，Qt 允许用户一次只能与单个`QWidget`或`QGraphicsItem`交互。
- `QInputDevice::DeviceType::Stylus`：`0x0010`;一种类似笔的设备，用于绘图板如Wacom绘图板，或在触摸屏上提供独立的触控笔感应功能。
- `QInputDevice::DeviceType::Airbrush`：`0x0020`;带有摇滚的触针，用于调节`tangentialPressure`。
- `QInputDevice::DeviceType::Puck`：`0x0008`;一种类似于扁平鼠标的装置，带有透明圆圈和十字准星。
- `QInputDevice::DeviceType::Keyboard`：`0x1000`;键盘。
- `QInputDevice::DeviceType::AllDevices`：`0x7FFFFFFF`;上述任意一种（作为默认滤波器值）。
DeviceTypes 类型是 QFlag 的 typedef<DeviceType>。它存储 DeviceType 值的 OR 组合。

### `QRect availableVirtualGeometry() const`

**作用与语义：**

该属性包含该设备可访问的虚拟桌面区域。
例如，`TouchScreen`输入设备固定在单个物理屏幕上，通常校准使该区域与`QScreen::geometry()`相同，而`Mouse`通常能够访问虚拟桌面上的所有屏幕。
另外，Wacom图形绘板也可以配置为映射到所有屏幕，或仅映射到用户偏好绘制的屏幕，或仅映射到绘图发生的窗口。
集成触摸屏的`Stylus`设备可能在物理上仅限于该屏幕。
如果返回的矩形是`null`的，说明该设备可以访问整个虚拟桌面。

**如何使用：** 调用 `availableVirtualGeometry()` 读取当前值；它不会修改应用状态。

### `void availableVirtualGeometryChanged(QRect area)`

**作用与语义：**

该属性包含该设备可访问的虚拟桌面区域。
例如，`TouchScreen`输入设备固定在单个物理屏幕上，通常校准使该区域与`QScreen::geometry()`相同，而`Mouse`通常能够访问虚拟桌面上的所有屏幕。
另外，Wacom图形绘板也可以配置为映射到所有屏幕，或仅映射到用户偏好绘制的屏幕，或仅映射到绘图发生的窗口。
集成触摸屏的`Stylus`设备可能在物理上仅限于该屏幕。
如果返回的矩形是`null`的，说明该设备可以访问整个虚拟桌面。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `availableVirtualGeometry` 的变化，不要把它当作普通函数主动调用。

### `void capabilitiesChanged(QInputDevice::Capabilities capabilities)`

**作用与语义：**

此属性保存设备能力。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `capabilities` 的变化，不要把它当作普通函数主动调用。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

### 状态和错误边界

QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

### 线程边界

QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

### 最容易出现的错误

不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QInputDevice` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
