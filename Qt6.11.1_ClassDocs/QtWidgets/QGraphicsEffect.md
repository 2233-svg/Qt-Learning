# QGraphicsEffect

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QGraphicsEffect` 是 图形场景与项目机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QGraphicsEffect` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QGraphicsEffect>`
- 继承自：QObject
- 直接派生类：QGraphicsBlurEffect、QGraphicsColorizeEffect、QGraphicsDropShadowEffect,、QGraphicsOpacityEffect

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

### 状态、生命周期和线程

**生命周期：** 场景或父项目通常管理子项目，但视图只是观察者，不一定拥有场景。删除项目、改变父项目或切换场景时要确认索引、指针、选中状态和布局关系是否仍有效。

**状态与结果：** 区分局部坐标、场景坐标、视图/窗口坐标，区分选中、悬停、焦点、可见和碰撞状态。改变几何、变换或数据后通常请求更新，而不是手动强制调用绘制函数。

**线程与事件循环：** 图形对象通常只能在其所属 GUI/场景线程操作；后台线程负责数据准备，结果通过信号投递后再更新场景对象。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum ChangeFlag { SourceAttached, SourceDetached, SourceBoundingRectChanged, SourceInvalidated }`
- `flags ChangeFlags`
- `enum PixmapPadMode { NoPad, PadToTransparentBorder, PadToEffectiveBoundingRect }`

### 属性

- `enabled : bool`

### 公有函数

- `QGraphicsEffect(QObject *parent = nullptr)`
- `virtual ~QGraphicsEffect()`
- `QRectF boundingRect() const`
- `virtual QRectF boundingRectFor(const QRectF &rect) const`
- `bool isEnabled() const`

### 公有槽函数

- `void setEnabled(bool enable)`
- `void update()`

### 信号

- `void enabledChanged(bool enabled)`

### 保护函数

- `virtual void draw(QPainter *painter) = 0`
- `void drawSource(QPainter *painter)`
- `QRectF sourceBoundingRect(Qt::CoordinateSystem system = Qt::LogicalCoordinates) const`
- `virtual void sourceChanged(QGraphicsEffect::ChangeFlags flags)`
- `bool sourceIsPixmap() const`
- `QPixmap sourcePixmap(Qt::CoordinateSystem system = Qt::LogicalCoordinates, QPoint *offset = nullptr, QGraphicsEffect::PixmapPadMode mode = PadToEffectiveBoundingRect) const`
- `void updateBoundingRect()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QGraphicsEffect::ChangeFlagflags QGraphicsEffect::ChangeFlags`

**作用与语义：**

本枚举描述了QGraphicsEffectSource中发生的变化。
- `QGraphicsEffect::SourceAttached`：`0x1`;该效果安装在源上。
- `QGraphicsEffect::SourceDetached`：`0x2`;该效果在源代码中卸载。
- `QGraphicsEffect::SourceBoundingRectChanged`：`0x4`;源的边界矩阵发生变化。
- `QGraphicsEffect::SourceInvalidated`：`0x8`;源的视觉外观发生了变化。
ChangeFlags 类型是 QFlags 的 typedef<ChangeFlag>。它存储 ChangeFlag 值的 OR 组合。

### `enum QGraphicsEffect::PixmapPadMode`

**作用与语义：**

这个枚举描述了从`sourcePixmap`返回的像素图应如何填充。
- `QGraphicsEffect::NoPad`：`0`;像素地图不应获得任何额外的填充。
- `QGraphicsEffect::PadToTransparentBorder`：`1`;像素地图应进行填充，以确保边界完全透明。
- `QGraphicsEffect::PadToEffectiveBoundingRect`：`2`;像素贴图应填充以匹配效果的有效边界矩形。

### `enabled : bool`

**作用与语义：**

无论该效应是否被启用，这一属性都成立。
如果某个效果被禁用，源会像正常一样渲染，不会受到该效果的干扰。如果该效果被启用，源体也会以该效果的状态渲染。
该属性默认启用。
利用这个特性，你可以在慢速平台上禁用某些效果，以确保用户界面响应灵敏。

**如何使用：** 调用 `enabled()` 读取当前值；它不会修改应用状态。

### `QGraphicsEffect::QGraphicsEffect(QObject *parent = nullptr)`

**作用与语义：**

构建一个具有指定`parent`的新QGraphicsEffect实例。

### `[virtual noexcept] QGraphicsEffect::~QGraphicsEffect()`

**作用与语义：**

这样可以从源端移除效果，同时破坏图形效果。

### `QRectF QGraphicsEffect::boundingRect() const`

**作用与语义：**

返回该效应的有效边界矩形，即源在设备坐标下的边界矩形，并由效果本身施加的边际调整。

### `[virtual] QRectF QGraphicsEffect::boundingRectFor(const QRectF &rect) const`

**作用与语义：**

根据设备坐标中提供的`rect`返回该效果的有效边界矩形。在编写自定义效果时，每当参数发生变化可能导致该函数返回不同值时，必须调用`updateBoundingRect()`。

### `[pure virtual protected] void QGraphicsEffect::draw(QPainter *painter)`

**作用与语义：**

这个纯虚拟函数绘制该效应，并在需要绘制源时调用。
在`QGraphicsEffect`子类中重新实现该函数，以提供该效果的绘制实现，使用`painter`。
用户不应明确调用该函数，因为它仅用于重实现。

**官方示例：**

```cpp
 MyGraphicsEffect::draw(QPainter *painter)
 {
     ...
     QPoint offset;
     if (sourceIsPixmap()) {
         // No point in drawing in device coordinates (pixmap will be scaled anyways).
         const QPixmap pixmap = sourcePixmap(Qt::LogicalCoordinates, &offset);
         ...
         painter->drawPixmap(offset, pixmap);
     } else {
         // Draw pixmap in device coordinates to avoid pixmap scaling;
         const QPixmap pixmap = sourcePixmap(Qt::DeviceCoordinates, &offset);
         painter->setWorldTransform(QTransform());
         ...
         painter->drawPixmap(offset, pixmap);
     }
     ...
 }
```

### `[protected] void QGraphicsEffect::drawSource(QPainter *painter)`

**作用与语义：**

直接使用给定的 `painter` 绘制源。
该函数应仅从`QGraphicsEffect::draw()`调用。

**官方示例：**

```cpp
 MyGraphicsOpacityEffect::draw(QPainter *painter)
 {
     // Fully opaque; draw directly without going through a pixmap.
     if (qFuzzyCompare(m_opacity, 1)) {
         drawSource(painter);
         return;
     }
     ...
 }
```

### `[signal] void QGraphicsEffect::enabledChanged(bool enabled)`

**作用与语义：**

无论该效应是否被启用，这一属性都成立。
如果某个效果被禁用，源会像正常一样渲染，不会受到该效果的干扰。如果该效果被启用，源体也会以该效果的状态渲染。
该属性默认启用。
利用这个特性，你可以在慢速平台上禁用某些效果，以确保用户界面响应灵敏。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `enabled` 的变化，不要把它当作普通函数主动调用。

### `[protected] QRectF QGraphicsEffect::sourceBoundingRect(Qt::CoordinateSystem system = Qt::LogicalCoordinates) const`

**作用与语义：**

返回映射到给定`system`的源的边界矩形。
在`QGraphicsEffect::draw()`之外调用`Qt::DeviceCoordinates`该函数时，会得到未定义的结果，因为没有可用的设备上下文。

### `[virtual protected] void QGraphicsEffect::sourceChanged(QGraphicsEffect::ChangeFlags flags)`

**作用与语义：**

`QGraphicsEffect`调用该虚拟函数以通知该效果源发生变化。如果该效果应用于任何缓存，则必须清除该缓存以反映源的新样貌。
`flags`描述了发生了哪些变化。

### `[protected] bool QGraphicsEffect::sourceIsPixmap() const`

**作用与语义：**

如果源实际上是像素图，例如`QGraphicsPixmapItem`，则返回`true`。
这个函数对优化很有用。例如，如果这个函数返回`true`，为了避免像素映射缩放，在设备坐标中绘制源图毫无意义——源像素映射无论如何都会被缩放。

### `[protected] QPixmap QGraphicsEffect::sourcePixmap(Qt::CoordinateSystem system = Qt::LogicalCoordinates, QPoint *offset = nullptr, QGraphicsEffect::PixmapPadMode mode = PadToEffectiveBoundingRect) const`

**作用与语义：**

返回一个带有源图的像素图。
`system`指定了源图应使用的坐标系。可选的`offset`参数返回使用当前画师绘制像素图应绘制的偏移量。控制像素图填充方式请使用`mode`参数。
当`system`被`Qt::DeviceCoordinates`时，返回的像素映射会被裁剪到当前画家设备的矩形上。
在`QGraphicsEffect::draw()`之外调用该函数时，`Qt::DeviceCoordinates`调用该函数会得到未定义的结果，因为没有可用的设备上下文。

### `[slot] void QGraphicsEffect::update()`

**作用与语义：**

安排对效果的重新绘制。每当需要重新绘制效果时调用此函数。该函数不会触发对源的重新绘制。

### `[protected] void QGraphicsEffect::updateBoundingRect()`

**作用与语义：**

该函数会在效果边界矩形发生变化时通知效果框架。作为自定义特效作者，每当你更改任何会导致虚拟`boundingRectFor()`函数返回不同值的参数时，都必须调用这个函数。
如果需要，该函数会调用`update()`。

### `enum ChangeFlag { SourceAttached, SourceDetached, SourceBoundingRectChanged, SourceInvalidated }`

**作用与语义：**

本枚举描述了QGraphicsEffectSource中发生的变化。
- `QGraphicsEffect::SourceAttached`：`0x1`;该效果安装在源上。
- `QGraphicsEffect::SourceDetached`：`0x2`;该效果在源代码中卸载。
- `QGraphicsEffect::SourceBoundingRectChanged`：`0x4`;源的边界矩阵发生变化。
- `QGraphicsEffect::SourceInvalidated`：`0x8`;源的视觉外观发生了变化。
ChangeFlags 类型是 QFlags 的 typedef<ChangeFlag>。它存储 ChangeFlag 值的 OR 组合。

### `flags ChangeFlags`

**作用与语义：**

本枚举描述了QGraphicsEffectSource中发生的变化。
- `QGraphicsEffect::SourceAttached`：`0x1`;该效果安装在源上。
- `QGraphicsEffect::SourceDetached`：`0x2`;该效果在源代码中卸载。
- `QGraphicsEffect::SourceBoundingRectChanged`：`0x4`;源的边界矩阵发生变化。
- `QGraphicsEffect::SourceInvalidated`：`0x8`;源的视觉外观发生了变化。
ChangeFlags 类型是 QFlags 的 typedef<ChangeFlag>。它存储 ChangeFlag 值的 OR 组合。

### `bool isEnabled() const`

**作用与语义：**

无论该效应是否被启用，这一属性都成立。
如果某个效果被禁用，源会像正常一样渲染，不会受到该效果的干扰。如果该效果被启用，源体也会以该效果的状态渲染。
该属性默认启用。
利用这个特性，你可以在慢速平台上禁用某些效果，以确保用户界面响应灵敏。

**如何使用：** 调用 `isEnabled()` 读取当前值；它不会修改应用状态。

### `void setEnabled(bool enable)`

**作用与语义：**

无论该效应是否被启用，这一属性都成立。
如果某个效果被禁用，源会像正常一样渲染，不会受到该效果的干扰。如果该效果被启用，源体也会以该效果的状态渲染。
该属性默认启用。
利用这个特性，你可以在慢速平台上禁用某些效果，以确保用户界面响应灵敏。

**如何使用：** 调用 `setEnabled(...)` 修改 `enabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

## 6. 深入实践与常见坑

### 生命周期和资源边界

场景或父项目通常管理子项目，但视图只是观察者，不一定拥有场景。删除项目、改变父项目或切换场景时要确认索引、指针、选中状态和布局关系是否仍有效。

### 状态和错误边界

区分局部坐标、场景坐标、视图/窗口坐标，区分选中、悬停、焦点、可见和碰撞状态。改变几何、变换或数据后通常请求更新，而不是手动强制调用绘制函数。

### 线程边界

图形对象通常只能在其所属 GUI/场景线程操作；后台线程负责数据准备，结果通过信号投递后再更新场景对象。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QGraphicsEffect` 所属机制类型：图形场景与项目机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
