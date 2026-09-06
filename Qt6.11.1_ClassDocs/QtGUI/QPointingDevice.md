# QPointingDevice

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QPointingDevice` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QPointingDevice>`
- 继承自：QInputDevice
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum GrabTransition { GrabExclusive, UngrabExclusive, CancelGrabExclusive, GrabPassive, UngrabPassive, …, OverrideGrabPassive }`
- `enum class PointerType { Unknown, Generic, Finger, Pen, Eraser, …, AllPointerTypes }`
- `flags PointerTypes`

### 属性

- `buttonCount : const int`
- `maximumPoints : const int`
- `pointerType : const PointerType`
- `uniqueId : const QPointingDeviceUniqueId`

### 公有函数

- `QPointingDevice(QObject *parent = nullptr)`
- `QPointingDevice(const QString &name, qint64 id, QInputDevice::DeviceType deviceType, QPointingDevice::PointerType pointerType, QInputDevice::Capabilities capabilities, int maxPoints, int buttonCount, const QString &seatName = QString(), QPointingDeviceUniqueId uniqueId = QPointingDeviceUniqueId(), QObject *parent = nullptr)`
- `int buttonCount() const`
- `int maximumPoints() const`
- `QPointingDevice::PointerType pointerType() const`
- `QPointingDeviceUniqueId uniqueId() const`

### 信号

- `void grabChanged(QObject *grabber, QPointingDevice::GrabTransition transition, const QPointerEvent *event, const QEventPoint &point) const`

### 静态公有成员

- `const QPointingDevice * primaryPointingDevice(const QString &seatName = QString())`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QPointingDevice::GrabTransition`

**作用与语义：**

该枚举表示从一个对象（可能是`nullptr`）到另一个对象（可能是`nullptr`）的专属或被动抓取的过渡。它作为`QPointingDevice::grabChanged()`信号的参数发出。
有效数值如下：
- `QPointingDevice::GrabExclusive`：`0x10`;`QPointerEvent::setExclusiveGrabber()`后发射。
- `QPointingDevice::UngrabExclusive`：`0x20`;当抓取器设为`nullptr`时，发出`QPointerEvent::setExclusiveGrabber()`后发出，以通知抓取已正常终止。
- `QPointingDevice::CancelGrabExclusive`：`0x30`;当抓取器设置为其他物体时，`QPointerEvent::setExclusiveGrabber()`后发出，以通知旧抓取器的抓取被“偷走”。
- `QPointingDevice::GrabPassive`：`0x01`;在`QPointerEvent::addPassiveGrabber()`后发射。
- `QPointingDevice::UngrabPassive`：`0x02`;当被动抓斗正常终止时发射，例如`QPointerEvent::removePassiveGrabber()`后。
- `QPointingDevice::CancelGrabPassive`：`0x03`;当被动抓取异常终止（手势被取消）时发出。
- `QPointingDevice::OverrideGrabPassive`：`0x04`;该值目前未被使用。

### `enum class QPointingDevice::PointerTypeflags QPointingDevice::PointerTypes`

**作用与语义：**

这个枚举代表与指向设备交互的内容。
该属性与`QInputDevice::DeviceType`之间存在一定的冗余。例如，如果使用触摸屏，则`DeviceType`为`TouchScreen`，而`PointerType`为`Finger`（始终如此）。但在绘图板上，通常可以同时使用触控笔的两端，程序需要区分它们。因此，该概念被扩展为每个`QPointerEvent`都有一个PointerType，并且可以简化一些事件处理代码，使得忽略DeviceType，并根据仅PointerType的不同做出不同的反应。
有效数值如下：
- `QPointingDevice::PointerType::Unknown`：`0`;指针类型未知。
- `QPointingDevice::PointerType::Generic`：`0x0001`;一个鼠标或类似鼠标的物体（X11 上的 core 指针）。
- `QPointingDevice::PointerType::Finger`：`0x0002`;使用者的手指。
- `QPointingDevice::PointerType::Pen`：`0x0004`;笔尖的绘图端。
- `QPointingDevice::PointerType::Eraser`：`0x0008`;唱针的另一端（如果另一端有虚拟橡皮擦）。
- `QPointingDevice::PointerType::Cursor`：`0x0010`;一个带有十字线的透明圆圈，类似于`Puck`装置上的。
- `QPointingDevice::PointerType::AllPointerTypes`：`0x7FFF`;上述任意一种（用作默认滤波器值）。
PointerTypes 类型是 QFlag 的 typedef<PointerType>。它存储 PointerType 值的 OR 组合。

### `[read-only] buttonCount : const int`

**作用与语义：**

该属性包含了可检测到的最大设备内按钮数量。

**如何使用：** 调用 `buttonCount()` 读取当前值；它不会修改应用状态。

### `[read-only] maximumPoints : const int`

**作用与语义：**

该特性包含了可检测的最大同时触点数（手指）。

**如何使用：** 调用 `maximumPoints()` 读取当前值；它不会修改应用状态。

### `[read-only] pointerType : const PointerType`

**作用与语义：**

此属性保存指针类型。

**如何使用：** 调用 `pointerType()` 读取当前值；它不会修改应用状态。

### `[read-only] uniqueId : const QPointingDeviceUniqueId`

**作用与语义：**

该属性为该设备保留了唯一的ID（效用存疑）。
你可能更应该关注的是QPointerEventPoint：：uniqueId()。

**如何使用：** 调用 `uniqueId()` 读取当前值；它不会修改应用状态。

### `QPointingDevice::QPointingDevice(QObject *parent = nullptr)`

**作用与语义：**

作为`parent`的子节点创建一个新的无效指向设备实例。

### `QPointingDevice::QPointingDevice(const QString &name, qint64 id, QInputDevice::DeviceType deviceType, QPointingDevice::PointerType pointerType, QInputDevice::Capabilities capabilities, int maxPoints, int buttonCount, const QString &seatName = QString(), QPointingDeviceUniqueId uniqueId = QPointingDeviceUniqueId(), QObject *parent = nullptr)`

**作用与语义：**

创建一个新的指向设备实例，包含给定的`name`、`deviceType`、`pointerType`、`capabilities`、`maxPoints`、`buttonCount`、`seatName`、`uniqueId`和`parent`。

### `int QPointingDevice::buttonCount() const`

**作用与语义：**

返回可检测到的最大设备上按钮数量。
注意：属性buttonCount的Getter函数。

### `[signal] void QPointingDevice::grabChanged(QObject *grabber, QPointingDevice::GrabTransition transition, const QPointerEvent *event, const QEventPoint &point) const`

**作用与语义：**

当`grabber`对象在传递`event`时获得或失去专属或被动的`point`抓取时，该信号会发出。`transition`从`grabber`对象的角度讲述发生了什么。
注意：从一个物体切换到另一个物体时，会产生两个信号，分别通知一个物体失去抓取，以及通知有另一个抓取器存在。在其他情况下，当从非抓取状态过渡到或转换时，只发出一个信号：`grabber`参数永远不会`nullptr`。

### `int QPointingDevice::maximumPoints() const`

**作用与语义：**

返回可检测的最大同时触点数（手指）。
注意：属性最大点的获取函数。

### `QPointingDevice::PointerType QPointingDevice::pointerType() const`

**作用与语义：**

返回指针类型。
注意：属性指针Type的Getter函数。

### `[static] const QPointingDevice *QPointingDevice::primaryPointingDevice(const QString &seatName = QString())`

**作用与语义：**

返回主指针装置（核心指针，传统上被认为是鼠标）在指定座椅`seatName`上。
如果注册了多个指向设备，该功能会优先选择与给定`seatName`匹配且没有其他设备作为父设备的鼠标或触摸板。通常只有一个主设备或核心设备没有父设备。但如果找不到此类设备，该功能会创建一个新的虚拟“核心指针”鼠标。因此，Qt 继续在尚未进行输入设备发现和注册的平台上工作。

### `QPointingDeviceUniqueId QPointingDevice::uniqueId() const`

**作用与语义：**

它会返回一个设备的唯一ID（实用性存疑）。
你可能更应该关注的是QPointerEventPoint：：uniqueId()。
注意：属性 uniqueId 的 Getter 函数。

### `enum class PointerType { Unknown, Generic, Finger, Pen, Eraser, …, AllPointerTypes }`

**作用与语义：**

这个枚举代表与指向设备交互的内容。
该属性与`QInputDevice::DeviceType`之间存在一定的冗余。例如，如果使用触摸屏，则`DeviceType`为`TouchScreen`，而`PointerType`为`Finger`（始终如此）。但在绘图板上，通常可以同时使用触控笔的两端，程序需要区分它们。因此，该概念被扩展为每个`QPointerEvent`都有一个PointerType，并且可以简化一些事件处理代码，使得忽略DeviceType，并根据仅PointerType的不同做出不同的反应。
有效数值如下：
- `QPointingDevice::PointerType::Unknown`：`0`;指针类型未知。
- `QPointingDevice::PointerType::Generic`：`0x0001`;一个鼠标或类似鼠标的物体（X11 上的 core 指针）。
- `QPointingDevice::PointerType::Finger`：`0x0002`;使用者的手指。
- `QPointingDevice::PointerType::Pen`：`0x0004`;笔尖的绘图端。
- `QPointingDevice::PointerType::Eraser`：`0x0008`;唱针的另一端（如果另一端有虚拟橡皮擦）。
- `QPointingDevice::PointerType::Cursor`：`0x0010`;一个带有十字线的透明圆圈，类似于`Puck`装置上的。
- `QPointingDevice::PointerType::AllPointerTypes`：`0x7FFF`;上述任意一种（用作默认滤波器值）。
PointerTypes 类型是 QFlag 的 typedef<PointerType>。它存储 PointerType 值的 OR 组合。

### `flags PointerTypes`

**作用与语义：**

这个枚举代表与指向设备交互的内容。
该属性与`QInputDevice::DeviceType`之间存在一定的冗余。例如，如果使用触摸屏，则`DeviceType`为`TouchScreen`，而`PointerType`为`Finger`（始终如此）。但在绘图板上，通常可以同时使用触控笔的两端，程序需要区分它们。因此，该概念被扩展为每个`QPointerEvent`都有一个PointerType，并且可以简化一些事件处理代码，使得忽略DeviceType，并根据仅PointerType的不同做出不同的反应。
有效数值如下：
- `QPointingDevice::PointerType::Unknown`：`0`;指针类型未知。
- `QPointingDevice::PointerType::Generic`：`0x0001`;一个鼠标或类似鼠标的物体（X11 上的 core 指针）。
- `QPointingDevice::PointerType::Finger`：`0x0002`;使用者的手指。
- `QPointingDevice::PointerType::Pen`：`0x0004`;笔尖的绘图端。
- `QPointingDevice::PointerType::Eraser`：`0x0008`;唱针的另一端（如果另一端有虚拟橡皮擦）。
- `QPointingDevice::PointerType::Cursor`：`0x0010`;一个带有十字线的透明圆圈，类似于`Puck`装置上的。
- `QPointingDevice::PointerType::AllPointerTypes`：`0x7FFF`;上述任意一种（用作默认滤波器值）。
PointerTypes 类型是 QFlag 的 typedef<PointerType>。它存储 PointerType 值的 OR 组合。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QPointingDevice` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
