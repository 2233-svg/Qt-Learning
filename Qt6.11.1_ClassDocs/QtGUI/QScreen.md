# QScreen

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 屏幕信息对象，负责几何尺寸、DPI、刷新率和设备像素比查询。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QScreen`：屏幕信息对象，负责几何尺寸、DPI、刷新率和设备像素比查询。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QScreen>`
- 继承自：QObject
- 直接派生类：未在类页中列出

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

使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 属性

- `availableGeometry : QRect`
- `availableSize : QSize`
- `availableVirtualGeometry : QRect`
- `availableVirtualSize : QSize`
- `depth : const int`
- `devicePixelRatio : qreal`
- `geometry : QRect`
- `logicalDotsPerInch : qreal`
- `logicalDotsPerInchX : qreal`
- `logicalDotsPerInchY : qreal`
- `manufacturer : const QString`
- `model : const QString`
- `name : const QString`
- `nativeOrientation : Qt::ScreenOrientation`
- `orientation : Qt::ScreenOrientation`
- `physicalDotsPerInch : qreal`
- `physicalDotsPerInchX : qreal`
- `physicalDotsPerInchY : qreal`
- `physicalSize : QSizeF`
- `primaryOrientation : Qt::ScreenOrientation`
- `refreshRate : qreal`
- `serialNumber : const QString`
- `size : QSize`
- `virtualGeometry : QRect`
- `virtualSize : QSize`

### 公有函数

- `int angleBetween(Qt::ScreenOrientation a, Qt::ScreenOrientation b) const`
- `QRect availableGeometry() const`
- `QSize availableSize() const`
- `QRect availableVirtualGeometry() const`
- `QSize availableVirtualSize() const`
- `int depth() const`
- `qreal devicePixelRatio() const`
- `QRect geometry() const`
- `QPixmap grabWindow(WId window = 0, int x = 0, int y = 0, int width = -1, int height = -1)`
- `QPlatformScreen * handle() const`
- `bool isLandscape(Qt::ScreenOrientation o) const`
- `bool isPortrait(Qt::ScreenOrientation o) const`
- `qreal logicalDotsPerInch() const`
- `qreal logicalDotsPerInchX() const`
- `qreal logicalDotsPerInchY() const`
- `QString manufacturer() const`
- `QRect mapBetween(Qt::ScreenOrientation a, Qt::ScreenOrientation b, const QRect &rect) const`
- `QString model() const`
- `QString name() const`
- `QNativeInterface * nativeInterface() const`
- `Qt::ScreenOrientation nativeOrientation() const`
- `Qt::ScreenOrientation orientation() const`
- `qreal physicalDotsPerInch() const`
- `qreal physicalDotsPerInchX() const`
- `qreal physicalDotsPerInchY() const`
- `QSizeF physicalSize() const`
- `Qt::ScreenOrientation primaryOrientation() const`
- `qreal refreshRate() const`
- `QString serialNumber() const`
- `QSize size() const`
- `QTransform transformBetween(Qt::ScreenOrientation a, Qt::ScreenOrientation b, const QRect &target) const`
- `QRect virtualGeometry() const`
- `QScreen * virtualSiblingAt(QPoint point)`
- `QList<QScreen *> virtualSiblings() const`
- `QSize virtualSize() const`

### 信号

- `void availableGeometryChanged(const QRect &geometry)`
- `void geometryChanged(const QRect &geometry)`
- `void logicalDotsPerInchChanged(qreal dpi)`
- `void orientationChanged(Qt::ScreenOrientation orientation)`
- `void physicalDotsPerInchChanged(qreal dpi)`
- `void physicalSizeChanged(const QSizeF &size)`
- `void primaryOrientationChanged(Qt::ScreenOrientation orientation)`
- `void refreshRateChanged(qreal refreshRate)`
- `void virtualGeometryChanged(const QRect &rect)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[read-only] availableGeometry : QRect`

**作用与语义：**

该属性以像素单位表示屏幕可用的几何形状。
可用的几何体是不包括窗口管理器保留区域（如任务栏和系统菜单）的几何体。
注意，在 X11 上，只有在只有一个显示器且窗口管理器设置了 Atom 时，这才会返回真实可用几何体_NET_WORKAREA。在其他情况下，这等同于 `geometry()`。这是 X11 窗口管理器规范中的一个限制。

**如何使用：** 调用 `availableGeometry()` 读取当前值；它不会修改应用状态。

### `[read-only] availableSize : QSize`

**作用与语义：**

该属性包含屏幕的可用像素大小。
可用大小是不包括窗口管理器预留区域（如任务栏和系统菜单）的大小。

**如何使用：** 调用 `availableSize()` 读取当前值；它不会修改应用状态。

### `[read-only] availableVirtualGeometry : QRect`

**作用与语义：**

该属性包含该屏幕所属虚拟桌面的可用几何形状。
返回对应该屏幕的虚拟桌面可用几何体。
这是虚拟兄弟姐妹各自可用几何体的合并。

**如何使用：** 调用 `availableVirtualGeometry()` 读取当前值；它不会修改应用状态。

### `[read-only] availableVirtualSize : QSize`

**作用与语义：**

该属性包含该屏幕所属虚拟桌面的可用大小。
返回对应该屏幕的虚拟桌面可用的像素大小。
这是虚拟兄弟姐妹各自可用几何体的总和大小。

**如何使用：** 调用 `availableVirtualSize()` 读取当前值；它不会修改应用状态。

### `[read-only] depth : const int`

**作用与语义：**

该属性决定了屏幕的色深。

**如何使用：** 调用 `depth()` 读取当前值；它不会修改应用状态。

### `[read-only] devicePixelRatio : qreal`

**作用与语义：**

该特性决定了屏幕物理像素与设备无关像素的比例。
返回屏幕的物理像素与设备无关像素的比例。
该函数可能返回与`QWindow::devicePixelRatio()`不同的值，例如在Wayland使用分数缩放时，或设置了影响表面分辨率的窗口属性。建议使用`QWindow::devicePixelRatio()`。
注意：在某些平台上，窗口的 devicePixelRatio 和它所在的屏幕可能不同。只有在你不知道目标窗口时才使用这个函数。如果你知道目标窗口，就用 `QWindow::devicePixelRatio()`。

**如何使用：** 调用 `devicePixelRatio()` 读取当前值；它不会修改应用状态。

### `[read-only] geometry : QRect`

**作用与语义：**

该属性将屏幕几何体以像素单位保持。
例如，这可能返回 `QRect`（0， 0， 1280， 1024），或者在虚拟桌面设置 `QRect`（1280， 0， 1280， 1024）中返回。

**如何使用：** 调用 `geometry()` 读取当前值；它不会修改应用状态。

### `[read-only] logicalDotsPerInch : qreal`

**作用与语义：**

该属性表示每英寸逻辑点数或像素数。
该值可用于将字体点大小转换为像素大小。
这是一种便利房产，仅仅是`logicalDotsPerInchX`和`logicalDotsPerInchY`房产的平均值。

**如何使用：** 调用 `logicalDotsPerInch()` 读取当前值；它不会修改应用状态。

### `[read-only] logicalDotsPerInchX : qreal`

**作用与语义：**

该属性表示水平方向上逻辑点数或每英寸的像素数。
该值用于将字体点大小转换为像素大小。

**如何使用：** 调用 `logicalDotsPerInchX()` 读取当前值；它不会修改应用状态。

### `[read-only] logicalDotsPerInchY : qreal`

**作用与语义：**

该属性表示垂直方向上每英寸逻辑点数或像素数。
该值用于将字体点大小转换为像素大小。

**如何使用：** 调用 `logicalDotsPerInchY()` 读取当前值；它不会修改应用状态。

### `[read-only] manufacturer : const QString`

**作用与语义：**

该物业是屏幕制造商所在。

**如何使用：** 调用 `manufacturer()` 读取当前值；它不会修改应用状态。

### `[read-only] model : const QString`

**作用与语义：**

该属性表示了屏幕的模型。

**如何使用：** 调用 `model()` 读取当前值；它不会修改应用状态。

### `[read-only] name : const QString`

**作用与语义：**

该属性包含一个用户可呈现的字符串，代表屏幕。
例如，在X11上，这些对应的是XRandr的屏幕名，通常是“VGA1”、“HDMI1”等。
注意：用户可呈现字符串不保证与任何本地API的结果匹配，也不应用于唯一标识屏幕。

**如何使用：** 调用 `name()` 读取当前值；它不会修改应用状态。

### `[read-only] nativeOrientation : Qt::ScreenOrientation`

**作用与语义：**

此属性保存本地屏幕方向。
屏幕的本地方向是设备标志贴纸显示正确方向的位置，如果平台不支持此功能，则为 `Qt::PrimaryOrientation`。
本地方向是硬件的属性，不会更改。

**如何使用：** 调用 `nativeOrientation()` 读取当前值；它不会修改应用状态。

### `[read-only] orientation : Qt::ScreenOrientation`

**作用与语义：**

该属性表示屏幕方向。
`orientation`属性告诉了从窗户系统角度看屏幕的方向。
大多数移动设备和平板都内置加速度计传感器。Qt传感器模块提供直接读取该传感器的能力。然而，窗口系统可能会根据屏幕的握持方式自动旋转整个屏幕;此时，这一`orientation`特性将发生变化。

**如何使用：** 调用 `orientation()` 读取当前值；它不会修改应用状态。

### `[read-only] physicalDotsPerInch : qreal`

**作用与语义：**

该属性决定了每英寸的物理点数或像素数。
该值代表屏幕显示上的像素密度。根据底层系统提供的信息，该值可能不完全准确。
这是一种便利房产，仅仅是`physicalDotsPerInchX`和`physicalDotsPerInchY`房产的平均值。
注意：物理DPI以设备无关的点表示。乘以`QScreen::devicePixelRatio()`即可得到设备相关的密度。

**如何使用：** 调用 `physicalDotsPerInch()` 读取当前值；它不会修改应用状态。

### `[read-only] physicalDotsPerInchX : qreal`

**作用与语义：**

该属性表示水平方向上每英寸物理点数或像素数。
该值代表屏幕显示上的实际水平像素密度。根据底层系统提供的信息，该值可能不完全准确。
注意：物理DPI以设备无关的点表示。乘以`QScreen::devicePixelRatio()`即可得到设备相关的密度。

**如何使用：** 调用 `physicalDotsPerInchX()` 读取当前值；它不会修改应用状态。

### `[read-only] physicalDotsPerInchY : qreal`

**作用与语义：**

该属性决定垂直方向上每英寸的物理点数或像素数。
该值代表屏幕显示上的实际垂直像素密度。根据底层系统提供的信息，该值可能不完全准确。
注意：物理DPI以设备无关的点表示。乘以`QScreen::devicePixelRatio()`即可得到设备相关的密度。

**如何使用：** 调用 `physicalDotsPerInchY()` 读取当前值；它不会修改应用状态。

### `[read-only] physicalSize : QSizeF`

**作用与语义：**

该特性保持屏幕的物理尺寸（以毫米计）。
物理尺寸代表屏幕显示的实际物理尺寸。
根据底层系统提供的信息，这个数值可能并不完全准确。

**如何使用：** 调用 `physicalSize()` 读取当前值；它不会修改应用状态。

### `[read-only] primaryOrientation : Qt::ScreenOrientation`

**作用与语义：**

该属性表示主屏幕朝向。
如果屏幕几何形状的宽度大于或等于其高度，或`Qt::PortraitOrientation`其他情况，则主要屏幕方向为`Qt::LandscapeOrientation`。当屏幕方向改变（即显示器旋转时），该特性可能会发生变化。然而，这种行为依赖于平台，通常可以在应用清单文件中指定。

**如何使用：** 调用 `primaryOrientation()` 读取当前值；它不会修改应用状态。

### `[read-only] refreshRate : qreal`

**作用与语义：**

该特性保持了屏幕的大致垂直刷新率（Hz）。
警告：请避免利用屏幕刷新率通过计时器（如`QChronoTimer`）来驱动动画。请使用`QWindow::requestUpdate()`。

**如何使用：** 调用 `refreshRate()` 读取当前值；它不会修改应用状态。

### `[read-only] serialNumber : const QString`

**作用与语义：**

该属性包含屏幕序列号。

**如何使用：** 调用 `serialNumber()` 读取当前值；它不会修改应用状态。

### `[read-only] size : QSize`

**作用与语义：**

该属性表示屏幕的像素分辨率。

**如何使用：** 调用 `size()` 读取当前值；它不会修改应用状态。

### `[read-only] virtualGeometry : QRect`

**作用与语义：**

该属性包含该屏幕所属虚拟桌面的像素几何体。
返回对应该屏幕的虚拟桌面像素几何体。
这是虚拟兄弟姐妹各个几何体的合并。

**如何使用：** 调用 `virtualGeometry()` 读取当前值；它不会修改应用状态。

### `[read-only] virtualSize : QSize`

**作用与语义：**

该属性包含该屏幕所属虚拟桌面的像素大小。
返回对应该屏幕的虚拟桌面像素大小。
这是虚拟兄弟姐妹各自几何体的总和大小。

**如何使用：** 调用 `virtualSize()` 读取当前值；它不会修改应用状态。

### `int QScreen::angleBetween(Qt::ScreenOrientation a, Qt::ScreenOrientation b) const`

**作用与语义：**

方便函数用于计算从旋转`a`到旋转`b`的旋转角度。
结果会是0、90、180或270。
`Qt::PrimaryOrientation`被解读为屏幕的“`primaryOrientation()`”。

### `QPixmap QScreen::grabWindow(WId window = 0, int x = 0, int y = 0, int width = -1, int height = -1)`

**作用与语义：**

创建并返回一个像素映射，该映射通过抓取受`QRect`（`x`， `y`， `width`， `height`）限制的给定`window`内容构建。如果`window`为0，则整个屏幕将被抓取。
参数（`x`、`y`）指定窗口中的偏移量，而参数（`width`、`height`）指定要复制的区域。如果`width`为负，函数会将所有内容复制到窗口右侧边界。如果`height`为负，函数将所有内容复制到窗口底部。
偏移和大小参数以设备无关像素表示。从高DPI屏幕抓取时，返回的像素映射可能大于请求的尺寸。调用`QPixmap::devicePixelRatio()`以确定是否属实。
窗口系统标识符（`WId`）可以通过`QWidget::winId()`函数检索。使用窗口标识符而非`QWidget`的理由是实现抓取非应用程序部分的窗口、窗口系统框架等。
警告：在 iOS 等系统中不支持抓取非应用窗口，因为沙箱/安全机制阻止读取应用程序不拥有的窗口像素。
grabWindow() 函数是从屏幕抓取像素，而不是从窗口抓取，也就是说，如果在你抓取的窗口上方有另一个部分或完全覆盖的窗口，你也会从覆盖窗口获得像素。鼠标光标通常不会被抓取。
注意在X11上，如果给定`window`的深度与根窗口不同，且另一个窗口部分或完全遮挡了你抓取的窗口，你将无法获得覆盖窗口的像素。像素映射中被遮挡区域的内容将是未定义且未初始化的。
在 Windows Vista 及以上版本中，抓取通过设置 `Qt::WA_TranslucentBackground` 属性创建的分层窗口是不行的。取而代之的是抓取桌面小部件应该可以。
警告：一般来说，抓屏外区域是不安全的。这取决于底层的窗户系统。

### `QPlatformScreen *QScreen::handle() const`

**作用与语义：**

拿到平台屏幕的手柄。

### `bool QScreen::isLandscape(Qt::ScreenOrientation o) const`

**作用与语义：**

便利函数，如果`o`是横向或倒置横向，则返回`true`;否则返回`false`。
`Qt::PrimaryOrientation`被解读为屏幕的“`primaryOrientation()`”。

### `bool QScreen::isPortrait(Qt::ScreenOrientation o) const`

**作用与语义：**

便利函数，如果`o`是竖向或倒置直向，返回`true`;否则返回`false`。
`Qt::PrimaryOrientation`被解读为屏幕的“光`primaryOrientation()`”。

### `QRect QScreen::mapBetween(Qt::ScreenOrientation a, Qt::ScreenOrientation b, const QRect &rect) const`

**作用与语义：**

将rect映射到两个屏幕方向之间。
如果方向`a`是`Qt::PortraitOrientation`还是`Qt::InvertedPortraitOrientation`，方向`b`是`Qt::LandscapeOrientation`或`Qt::InvertedLandscapeOrientation`，反之亦然，`rect`会将矩形的x和y维反转。
`Qt::PrimaryOrientation`被解读为屏幕的“光`primaryOrientation()`”。

### `template <typename QNativeInterface> QNativeInterface *QScreen::nativeInterface() const`

**作用与语义：**

返回该屏幕的本地接口。
该功能提供访问`QScreen`特定平台的功能，定义在`QNativeInterface`命名空间中：
- `QNativeInterface::QAndroidScreen`：屏幕的原生接口
- `QNativeInterface::QCocoaScreen`：macOS 屏幕上的原生界面
- `QNativeInterface::QWaylandScreen`：Wayland 屏幕上的原生界面
- `QNativeInterface::QWindowsScreen`：屏幕的原生接口
如果请求的接口不可用，则返回`nullptr`。

### `[signal] void QScreen::orientationChanged(Qt::ScreenOrientation orientation)`

**作用与语义：**

该属性表示屏幕方向。
`orientation`属性告诉了从窗户系统角度看屏幕的方向。
大多数移动设备和平板都内置加速度计传感器。Qt传感器模块提供直接读取该传感器的能力。然而，窗口系统可能会根据屏幕的握持方式自动旋转整个屏幕;此时，这一`orientation`特性将发生变化。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `orientation` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QScreen::primaryOrientationChanged(Qt::ScreenOrientation orientation)`

**作用与语义：**

该属性表示主屏幕朝向。
如果屏幕几何形状的宽度大于或等于其高度，或`Qt::PortraitOrientation`其他情况，则主要屏幕方向为`Qt::LandscapeOrientation`。当屏幕方向改变（即显示器旋转时），该特性可能会发生变化。然而，这种行为依赖于平台，通常可以在应用清单文件中指定。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `primaryOrientation` 的变化，不要把它当作普通函数主动调用。

### `QTransform QScreen::transformBetween(Qt::ScreenOrientation a, Qt::ScreenOrientation b, const QRect &target) const`

**作用与语义：**

方便函数，计算一个变换，将由方向`a`定义的坐标系映射到由方向`b`和目标维度`target`定义的坐标系。
例如，`a` 是 Qt：：Landscape，`b` 是 Qt：:P ortrait，`target` 是 `QRect`（0， 0， w， h），得到的变换将使得点 `QPoint`（0， 0） 映射到 `QPoint`（0， w），`QPoint`（h， w） 映射到 `QPoint`（0， h）。因此，横向坐标系`QRect`（0， 0， h， w）被映射到直向坐标系`QRect`（0， 0， w， h）。
`Qt::PrimaryOrientation`被解读为屏幕的“`primaryOrientation()`”。

### `QScreen *QScreen::virtualSiblingAt(QPoint point)`

**作用与语义：**

在`QScreen::virtualSiblings()`集内返回`point`，或者如果在屏幕外，则返回`nullptr`。
`point`与每组虚拟兄弟姐妹的`virtualGeometry()`有关。

### `QList<QScreen *> QScreen::virtualSiblings() const`

**作用与语义：**

获取屏幕的虚拟兄弟姐妹。
虚拟兄弟姐妹是共享同一虚拟桌面的屏幕实例。它们共享一个坐标系，窗口可以自由移动或定位，无需重新创建。

### `QRect availableGeometry() const`

**作用与语义：**

该属性以像素单位表示屏幕可用的几何形状。
可用的几何体是不包括窗口管理器保留区域（如任务栏和系统菜单）的几何体。
注意，在 X11 上，只有在只有一个显示器且窗口管理器设置了 Atom 时，这才会返回真实可用几何体_NET_WORKAREA。在其他情况下，这等同于 `geometry()`。这是 X11 窗口管理器规范中的一个限制。

**如何使用：** 调用 `availableGeometry()` 读取当前值；它不会修改应用状态。

### `QSize availableSize() const`

**作用与语义：**

该属性包含屏幕的可用像素大小。
可用大小是不包括窗口管理器预留区域（如任务栏和系统菜单）的大小。

**如何使用：** 调用 `availableSize()` 读取当前值；它不会修改应用状态。

### `QRect availableVirtualGeometry() const`

**作用与语义：**

该属性包含该屏幕所属虚拟桌面的可用几何形状。
返回对应该屏幕的虚拟桌面可用几何体。
这是虚拟兄弟姐妹各自可用几何体的合并。

**如何使用：** 调用 `availableVirtualGeometry()` 读取当前值；它不会修改应用状态。

### `QSize availableVirtualSize() const`

**作用与语义：**

该属性包含该屏幕所属虚拟桌面的可用大小。
返回对应该屏幕的虚拟桌面可用的像素大小。
这是虚拟兄弟姐妹各自可用几何体的总和大小。

**如何使用：** 调用 `availableVirtualSize()` 读取当前值；它不会修改应用状态。

### `int depth() const`

**作用与语义：**

该属性决定了屏幕的色深。

**如何使用：** 调用 `depth()` 读取当前值；它不会修改应用状态。

### `qreal devicePixelRatio() const`

**作用与语义：**

该特性决定了屏幕物理像素与设备无关像素的比例。
返回屏幕的物理像素与设备无关像素的比例。
该函数可能返回与`QWindow::devicePixelRatio()`不同的值，例如在Wayland使用分数缩放时，或设置了影响表面分辨率的窗口属性。建议使用`QWindow::devicePixelRatio()`。
注意：在某些平台上，窗口的 devicePixelRatio 和它所在的屏幕可能不同。只有在你不知道目标窗口时才使用这个函数。如果你知道目标窗口，就用 `QWindow::devicePixelRatio()`。

**如何使用：** 调用 `devicePixelRatio()` 读取当前值；它不会修改应用状态。

### `QRect geometry() const`

**作用与语义：**

该属性将屏幕几何体以像素单位保持。
例如，这可能返回 `QRect`（0， 0， 1280， 1024），或者在虚拟桌面设置 `QRect`（1280， 0， 1280， 1024）中返回。

**如何使用：** 调用 `geometry()` 读取当前值；它不会修改应用状态。

### `qreal logicalDotsPerInch() const`

**作用与语义：**

该属性表示每英寸逻辑点数或像素数。
该值可用于将字体点大小转换为像素大小。
这是一种便利房产，仅仅是`logicalDotsPerInchX`和`logicalDotsPerInchY`房产的平均值。

**如何使用：** 调用 `logicalDotsPerInch()` 读取当前值；它不会修改应用状态。

### `qreal logicalDotsPerInchX() const`

**作用与语义：**

该属性表示水平方向上逻辑点数或每英寸的像素数。
该值用于将字体点大小转换为像素大小。

**如何使用：** 调用 `logicalDotsPerInchX()` 读取当前值；它不会修改应用状态。

### `qreal logicalDotsPerInchY() const`

**作用与语义：**

该属性表示垂直方向上每英寸逻辑点数或像素数。
该值用于将字体点大小转换为像素大小。

**如何使用：** 调用 `logicalDotsPerInchY()` 读取当前值；它不会修改应用状态。

### `QString manufacturer() const`

**作用与语义：**

该物业是屏幕制造商所在。

**如何使用：** 调用 `manufacturer()` 读取当前值；它不会修改应用状态。

### `QString model() const`

**作用与语义：**

该属性表示了屏幕的模型。

**如何使用：** 调用 `model()` 读取当前值；它不会修改应用状态。

### `QString name() const`

**作用与语义：**

该属性包含一个用户可呈现的字符串，代表屏幕。
例如，在X11上，这些对应的是XRandr的屏幕名，通常是“VGA1”、“HDMI1”等。
注意：用户可呈现字符串不保证与任何本地API的结果匹配，也不应用于唯一标识屏幕。

**如何使用：** 调用 `name()` 读取当前值；它不会修改应用状态。

### `Qt::ScreenOrientation nativeOrientation() const`

**作用与语义：**

此属性保存本地屏幕方向。
屏幕的本地方向是设备标志贴纸显示正确方向的位置，如果平台不支持此功能，则为 `Qt::PrimaryOrientation`。
本地方向是硬件的属性，不会更改。

**如何使用：** 调用 `nativeOrientation()` 读取当前值；它不会修改应用状态。

### `Qt::ScreenOrientation orientation() const`

**作用与语义：**

该属性表示屏幕方向。
`orientation`属性告诉了从窗户系统角度看屏幕的方向。
大多数移动设备和平板都内置加速度计传感器。Qt传感器模块提供直接读取该传感器的能力。然而，窗口系统可能会根据屏幕的握持方式自动旋转整个屏幕;此时，这一`orientation`特性将发生变化。

**如何使用：** 调用 `orientation()` 读取当前值；它不会修改应用状态。

### `qreal physicalDotsPerInch() const`

**作用与语义：**

该属性决定了每英寸的物理点数或像素数。
该值代表屏幕显示上的像素密度。根据底层系统提供的信息，该值可能不完全准确。
这是一种便利房产，仅仅是`physicalDotsPerInchX`和`physicalDotsPerInchY`房产的平均值。
注意：物理DPI以设备无关的点表示。乘以`QScreen::devicePixelRatio()`即可得到设备相关的密度。

**如何使用：** 调用 `physicalDotsPerInch()` 读取当前值；它不会修改应用状态。

### `qreal physicalDotsPerInchX() const`

**作用与语义：**

该属性表示水平方向上每英寸物理点数或像素数。
该值代表屏幕显示上的实际水平像素密度。根据底层系统提供的信息，该值可能不完全准确。
注意：物理DPI以设备无关的点表示。乘以`QScreen::devicePixelRatio()`即可得到设备相关的密度。

**如何使用：** 调用 `physicalDotsPerInchX()` 读取当前值；它不会修改应用状态。

### `qreal physicalDotsPerInchY() const`

**作用与语义：**

该属性决定垂直方向上每英寸的物理点数或像素数。
该值代表屏幕显示上的实际垂直像素密度。根据底层系统提供的信息，该值可能不完全准确。
注意：物理DPI以设备无关的点表示。乘以`QScreen::devicePixelRatio()`即可得到设备相关的密度。

**如何使用：** 调用 `physicalDotsPerInchY()` 读取当前值；它不会修改应用状态。

### `QSizeF physicalSize() const`

**作用与语义：**

该特性保持屏幕的物理尺寸（以毫米计）。
物理尺寸代表屏幕显示的实际物理尺寸。
根据底层系统提供的信息，这个数值可能并不完全准确。

**如何使用：** 调用 `physicalSize()` 读取当前值；它不会修改应用状态。

### `Qt::ScreenOrientation primaryOrientation() const`

**作用与语义：**

该属性表示主屏幕朝向。
如果屏幕几何形状的宽度大于或等于其高度，或`Qt::PortraitOrientation`其他情况，则主要屏幕方向为`Qt::LandscapeOrientation`。当屏幕方向改变（即显示器旋转时），该特性可能会发生变化。然而，这种行为依赖于平台，通常可以在应用清单文件中指定。

**如何使用：** 调用 `primaryOrientation()` 读取当前值；它不会修改应用状态。

### `qreal refreshRate() const`

**作用与语义：**

该特性保持了屏幕的大致垂直刷新率（Hz）。
警告：请避免利用屏幕刷新率通过计时器（如`QChronoTimer`）来驱动动画。请使用`QWindow::requestUpdate()`。

**如何使用：** 调用 `refreshRate()` 读取当前值；它不会修改应用状态。

### `QString serialNumber() const`

**作用与语义：**

该属性包含屏幕序列号。

**如何使用：** 调用 `serialNumber()` 读取当前值；它不会修改应用状态。

### `QSize size() const`

**作用与语义：**

该属性表示屏幕的像素分辨率。

**如何使用：** 调用 `size()` 读取当前值；它不会修改应用状态。

### `QRect virtualGeometry() const`

**作用与语义：**

该属性包含该屏幕所属虚拟桌面的像素几何体。
返回对应该屏幕的虚拟桌面像素几何体。
这是虚拟兄弟姐妹各个几何体的合并。

**如何使用：** 调用 `virtualGeometry()` 读取当前值；它不会修改应用状态。

### `QSize virtualSize() const`

**作用与语义：**

该属性包含该屏幕所属虚拟桌面的像素大小。
返回对应该屏幕的虚拟桌面像素大小。
这是虚拟兄弟姐妹各自几何体的总和大小。

**如何使用：** 调用 `virtualSize()` 读取当前值；它不会修改应用状态。

### `void availableGeometryChanged(const QRect &geometry)`

**作用与语义：**

该属性以像素单位表示屏幕可用的几何形状。
可用的几何体是不包括窗口管理器保留区域（如任务栏和系统菜单）的几何体。
注意，在 X11 上，只有在只有一个显示器且窗口管理器设置了 Atom 时，这才会返回真实可用几何体_NET_WORKAREA。在其他情况下，这等同于 `geometry()`。这是 X11 窗口管理器规范中的一个限制。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `availableGeometry` 的变化，不要把它当作普通函数主动调用。

### `void geometryChanged(const QRect &geometry)`

**作用与语义：**

该属性将屏幕几何体以像素单位保持。
例如，这可能返回 `QRect`（0， 0， 1280， 1024），或者在虚拟桌面设置 `QRect`（1280， 0， 1280， 1024）中返回。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `geometry` 的变化，不要把它当作普通函数主动调用。

### `void logicalDotsPerInchChanged(qreal dpi)`

**作用与语义：**

该属性表示每英寸逻辑点数或像素数。
该值可用于将字体点大小转换为像素大小。
这是一种便利房产，仅仅是`logicalDotsPerInchX`和`logicalDotsPerInchY`房产的平均值。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `logicalDotsPerInch` 的变化，不要把它当作普通函数主动调用。

### `void physicalDotsPerInchChanged(qreal dpi)`

**作用与语义：**

该特性决定了屏幕物理像素与设备无关像素的比例。
返回屏幕的物理像素与设备无关像素的比例。
该函数可能返回与`QWindow::devicePixelRatio()`不同的值，例如在Wayland使用分数缩放时，或设置了影响表面分辨率的窗口属性。建议使用`QWindow::devicePixelRatio()`。
注意：在某些平台上，窗口的 devicePixelRatio 和它所在的屏幕可能不同。只有在你不知道目标窗口时才使用这个函数。如果你知道目标窗口，就用 `QWindow::devicePixelRatio()`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `devicePixelRatio` 的变化，不要把它当作普通函数主动调用。

### `void physicalSizeChanged(const QSizeF &size)`

**作用与语义：**

该特性保持屏幕的物理尺寸（以毫米计）。
物理尺寸代表屏幕显示的实际物理尺寸。
根据底层系统提供的信息，这个数值可能并不完全准确。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `physicalSize` 的变化，不要把它当作普通函数主动调用。

### `void refreshRateChanged(qreal refreshRate)`

**作用与语义：**

该特性保持了屏幕的大致垂直刷新率（Hz）。
警告：请避免利用屏幕刷新率通过计时器（如`QChronoTimer`）来驱动动画。请使用`QWindow::requestUpdate()`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `refreshRate` 的变化，不要把它当作普通函数主动调用。

### `void virtualGeometryChanged(const QRect &rect)`

**作用与语义：**

该属性包含该屏幕所属虚拟桌面的可用几何形状。
返回对应该屏幕的虚拟桌面可用几何体。
这是虚拟兄弟姐妹各自可用几何体的合并。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `availableVirtualGeometry` 的变化，不要把它当作普通函数主动调用。

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

`QScreen` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
