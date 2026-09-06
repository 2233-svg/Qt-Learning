# QScrollerProperties

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QScrollerProperties` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QScrollerProperties` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QScrollerProperties>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum FrameRates { Fps60, Fps30, Fps20, Standard }`
- `enum OvershootPolicy { OvershootWhenScrollable, OvershootAlwaysOff, OvershootAlwaysOn }`
- `enum ScrollMetric { MousePressEventDelay, DragStartDistance, DragVelocitySmoothingFactor, AxisLockThreshold, ScrollingCurve, …, ScrollMetricCount }`

### 公有函数

- `QScrollerProperties()`
- `QScrollerProperties(const QScrollerProperties &sp)`
- `virtual ~QScrollerProperties()`
- `QVariant scrollMetric(QScrollerProperties::ScrollMetric metric) const`
- `void setScrollMetric(QScrollerProperties::ScrollMetric metric, const QVariant &value)`
- `bool operator!=(const QScrollerProperties &sp) const`
- `QScrollerProperties & operator=(const QScrollerProperties &sp)`
- `bool operator==(const QScrollerProperties &sp) const`

### 静态公有成员

- `void setDefaultScrollerProperties(const QScrollerProperties &sp)`
- `void unsetDefaultScrollerProperties()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QScrollerProperties::FrameRates`

**作用与语义：**

这个枚举描述了拖曳或滚动时可用的帧率。
- `QScrollerProperties::Fps60`：`1`;每秒60帧
- `QScrollerProperties::Fps30`：`2`;每秒30帧
- `QScrollerProperties::Fps20`：`3`;每秒20帧
- `QScrollerProperties::Standard`：`0`;默认值为每秒60帧（对应`QAbstractAnimation`帧）。

### `enum QScrollerProperties::OvershootPolicy`

**作用与语义：**

此枚举描述了各种超出滚动范围的模式。
- `QScrollerProperties::OvershootWhenScrollable`: `0`; 当内容可滚动时，可能发生超出滚动。这是默认设置。
- `QScrollerProperties::OvershootAlwaysOff`: `1`; 即使内容可滚动，也永远不会启用超出滚动。
- `QScrollerProperties::OvershootAlwaysOn`: `2`; 始终启用超出滚动，即使内容不可滚动。

### `enum QScrollerProperties::ScrollMetric`

**作用与语义：**

该枚举包含不同的滚动度量类型。若未另有说明，`setScrollMetric`函数期望`QVariant`为qreal。
有关不同数值背后的更多概念，请参见`QScroller`文档。
- `QScrollerProperties::MousePressEventDelay`：`0`;这是指在`[s]`中开始弹动手势时，鼠标按键事件被延迟的时间。如果手势在该时间内触发，则不会向滚动对象发送鼠标按压或释放。如果延迟后触发，则发送延迟鼠标按压加上全局位置`QPoint(-QWIDGETSIZE_MAX, -QWIDGETSIZE_MAX)`的假释放事件。如果手势被取消，则延迟鼠标按压和真实释放事件都会同时传递。
- `QScrollerProperties::DragStartDistance`：`1`;这是触发`m`弹动手势前，触摸或鼠标点移动的最小距离。
- `QScrollerProperties::DragVelocitySmoothingFactor`：`2`;一个描述新阻力速度被纳入最终滚动速度的程度的值。该值应在`0`到`1`之间。值越低，拖拽速度被施加的平滑处理越多。
- `QScrollerProperties::AxisLockThreshold`：`3`;如果移动在绕轴的角度内，则限制运动仅在一个轴上。阈值必须在`0`到`1`范围内。
- `QScrollerProperties::ScrollingCurve`：`4`;用户发起弹动后减速滚动速度时使用的`QEasingCurve`。请注意，这是位置的缓慢曲线，而非速度：默认为`QEasingCurve::OutQuad`，导致速度线性下降（一阶导数）和恒定减速（二阶导数）。
- `QScrollerProperties::DecelerationFactor`：`5`;该因素影响滚动器减速至0速度所需的时间。实际值取决于所选的滚动曲线。对于大多数类型，该值应在`0.1`到`2.0`之间
- `QScrollerProperties::MinimumVelocity`：`6`;结束触控或松开鼠标后，开始滚动所需的最低速度`m/s`。
- `QScrollerProperties::MaximumVelocity`：`7`;这是`m/s`中能达到的最大速度。
- `QScrollerProperties::MaximumClickThroughVelocity`：`8`;这是`m/s`中点击时允许的最大滚动速度。这意味着点击当前（缓慢）滚动对象不仅会停止滚动，点击事件也会传递到UI控件。这在使用指数式滚动曲线时非常有用。
- `QScrollerProperties::AcceleratingFlickMaximumTime`：`9`;这是弹动手势被识别为加速弹动的最`seconds`长时间。如果设置为零，则不会检测到该手势。“加速弹动”是指在已经滚动的物体上执行的弹动手势。在这种情况下，滚动速度乘以AcceleratingFlickSpeedupFactor以加速。
- `QScrollerProperties::AcceleratingFlickSpeedupFactor`：`10`;如果检测到加速的弹跳，将当前速度乘以该数值。应为`>= 1`。
- `QScrollerProperties::SnapPositionRatio`：`11`;这是用户必须拖动两个吸附点之间的距离，才能吸附到下一个位置。`0.33`意味着卷轴只需拖到两个吸附点之间距离的三分之一即可吸附到下一个。比例必须在`0`和`1`之间。
- `QScrollerProperties::SnapTime`：`12`;这是滚动曲线的时间因子。值越小表示滚动时间越长。滚动距离与该值无关。
- `QScrollerProperties::OvershootDragResistanceFactor`：`13`;该值是拖动鼠标与实际滚动区域移动（超冲时）之间的系数。系数必须介于`0`到`1`之间。
- `QScrollerProperties::OvershootDragDistanceFactor`：`14`;这是拖曳时超冲移动的最大距离。实际超跃距离是通过将该值乘以卷动对象的视口大小计算得出的。因子必须介于`0`和`1`之间。
- `QScrollerProperties::OvershootScrollDistanceFactor`：`15`;这是滚动时超冲移动的最大距离。实际超冲距离是通过将该值乘以被滚动物体的视口大小计算得出的。该因子必须介于`0`到`1`之间。
- `QScrollerProperties::OvershootScrollTime`：`16`;这是用于播放完整超跃动画的 `seconds` 时间。
- `QScrollerProperties::HorizontalOvershootPolicy`：`17`;这就是水平超转策略（见`OvershootPolicy`）。
- `QScrollerProperties::VerticalOvershootPolicy`：`18`;这是水平超转策略（见`OvershootPolicy`）。
- `QScrollerProperties::FrameRate`：`19`;这是拖动或滚动时应使用的帧率。`QScroller` 内部使用`QAbstractAnimation`计时器，将所有滚动操作同步到可能同时激活的其他动画。如果标准的 60 帧每秒过快，可以用此设置降低帧率，同时保持与 `QAbstractAnimation` 同步。请注意，这里只允许使用`FrameRates`枚举的值。
- `QScrollerProperties::ScrollMetricCount`：`20`;这总是最后一篇。

### `QScrollerProperties::QScrollerProperties()`

**作用与语义：**

构建新的滚动器属性。

### `QScrollerProperties::QScrollerProperties(const QScrollerProperties &sp)`

**作用与语义：**

构建了`sp`的复制品。

### `[virtual noexcept] QScrollerProperties::~QScrollerProperties()`

**作用与语义：**

会破坏滚动器的属性。

### `QVariant QScrollerProperties::scrollMetric(QScrollerProperties::ScrollMetric metric) const`

**作用与语义：**

查询滚动器属性的 `metric` 值。

### `[static] void QScrollerProperties::setDefaultScrollerProperties(const QScrollerProperties &sp)`

**作用与语义：**

将所有新`QScrollerProperties`对象的滚动属性设置为`sp`。
使用这个函数来覆盖默认构造函数返回的平台默认属性。如果你只想更改单个滚动器的滚动属性，可以使用`QScroller::setScrollerProperties()`。
注意：调用该函数不会改变已有`QScrollerProperties`对象的内容。

### `void QScrollerProperties::setScrollMetric(QScrollerProperties::ScrollMetric metric, const QVariant &value)`

**作用与语义：**

将`metric`滚动计量的具体值设置为`value`。

### `[static] void QScrollerProperties::unsetDefaultScrollerProperties()`

**作用与语义：**

将默认构造函数返回的滚动器属性设回平台默认属性。

### `bool QScrollerProperties::operator!=(const QScrollerProperties &sp) const`

**作用与语义：**

如果这些滚动器属性与`sp`不同，返回`true`;否则返回`false`。

### `QScrollerProperties &QScrollerProperties::operator=(const QScrollerProperties &sp)`

**作用与语义：**

将`sp`分配给这些滚动属性，并返回对这些滚动属性的引用。

### `bool QScrollerProperties::operator==(const QScrollerProperties &sp) const`

**作用与语义：**

如果这些滚动器属性等于 `sp`，返回`true`;否则返回 `false`。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QScrollerProperties` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
