# QGraphicsBlurEffect

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QGraphicsBlurEffect` 是 图形场景与项目机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QGraphicsBlurEffect` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QGraphicsBlurEffect>`
- 继承自：QGraphicsEffect
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

**生命周期：** 场景或父项目通常管理子项目，但视图只是观察者，不一定拥有场景。删除项目、改变父项目或切换场景时要确认索引、指针、选中状态和布局关系是否仍有效。

**状态与结果：** 区分局部坐标、场景坐标、视图/窗口坐标，区分选中、悬停、焦点、可见和碰撞状态。改变几何、变换或数据后通常请求更新，而不是手动强制调用绘制函数。

**线程与事件循环：** 图形对象通常只能在其所属 GUI/场景线程操作；后台线程负责数据准备，结果通过信号投递后再更新场景对象。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum BlurHint { PerformanceHint, QualityHint, AnimationHint }`
- `flags BlurHints`

### 属性

- `blurHints : BlurHints`
- `blurRadius : qreal`

### 公有函数

- `QGraphicsBlurEffect(QObject *parent = nullptr)`
- `virtual ~QGraphicsBlurEffect()`
- `QGraphicsBlurEffect::BlurHints blurHints() const`
- `qreal blurRadius() const`

### 重实现的公有函数

- `virtual QRectF boundingRectFor(const QRectF &rect) const override`

### 公有槽函数

- `void setBlurHints(QGraphicsBlurEffect::BlurHints hints)`
- `void setBlurRadius(qreal blurRadius)`

### 信号

- `void blurHintsChanged(QGraphicsBlurEffect::BlurHints hints)`
- `void blurRadiusChanged(qreal radius)`

### 重实现的保护函数

- `virtual void draw(QPainter *painter) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QGraphicsBlurEffect::BlurHintflags QGraphicsBlurEffect::BlurHints`

**作用与语义：**

这个枚举描述了可以用来控制模糊效果应用的可能提示。这些提示可能在所有喷漆引擎中都会产生效果。
- `QGraphicsBlurEffect::PerformanceHint`：`0x00`;表示渲染性能是最重要的因素，但可能以较低的质量为代价。
- `QGraphicsBlurEffect::QualityHint`：`0x01`;表示渲染质量是最重要的因素，但这可能带来性能下降的代价。
- `QGraphicsBlurEffect::AnimationHint`：`0x02`;表示模糊半径将被动画化，暗示实现可以缓存模糊的源版本。如果源将动态变化，请勿使用此提示。
BlurHints 类型是 QFlags 的 typedef<BlurHint>。它存储 BlurHint 值的 OR 组合。

### `blurHints : BlurHints`

**作用与语义：**

这种特性保留了模糊效果的暗示。
用`PerformanceHint`提示表示你想要更快的模糊，`QualityHint`提示表示你喜欢更高质量的模糊，或者用`AnimationHint`来表示你想动画化模糊半径。
默认情况下，模糊提示是`PerformanceHint`。

**如何使用：** 调用 `blurHints()` 读取当前值；它不会修改应用状态。

### `blurRadius : qreal`

**作用与语义：**

该特性保持了该效果的模糊半径。
使用较小的半径会让画面更清晰，而大半径则会让画面更模糊。
默认的模糊半径是5像素。
半径以设备坐标表示，意味着不受比例尺影响。

**如何使用：** 调用 `blurRadius()` 读取当前值；它不会修改应用状态。

### `QGraphicsBlurEffect::QGraphicsBlurEffect(QObject *parent = nullptr)`

**作用与语义：**

构建一个新的 QGraphicsBlurEffect 实例。`parent`参数传递给 `QGraphicsEffect` 的构造器。

### `[virtual noexcept] QGraphicsBlurEffect::~QGraphicsBlurEffect()`

**作用与语义：**

破坏效果。

### `[signal] void QGraphicsBlurEffect::blurHintsChanged(QGraphicsBlurEffect::BlurHints hints)`

**作用与语义：**

这种特性保留了模糊效果的暗示。
用`PerformanceHint`提示表示你想要更快的模糊，`QualityHint`提示表示你喜欢更高质量的模糊，或者用`AnimationHint`来表示你想动画化模糊半径。
默认情况下，模糊提示是`PerformanceHint`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `blurHints` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QGraphicsBlurEffect::blurRadiusChanged(qreal radius)`

**作用与语义：**

该特性保持了该效果的模糊半径。
使用较小的半径会让画面更清晰，而大半径则会让画面更模糊。
默认的模糊半径是5像素。
半径以设备坐标表示，意味着不受比例尺影响。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `blurRadius` 的变化，不要把它当作普通函数主动调用。

### `[override virtual] QRectF QGraphicsBlurEffect::boundingRectFor(const QRectF &rect) const`

**作用与语义：**

重装：`QGraphicsEffect::boundingRectFor`（const QRectF &rect） const.
根据设备坐标中提供的`rect`，返回该效果的有效边界矩形。编写自定义效果时，每当参数变化可能导致该函数返回不同值时，必须调用`updateBoundingRect()`。

### `[override virtual protected] void QGraphicsBlurEffect::draw(QPainter *painter)`

**作用与语义：**

重实现自：`QGraphicsEffect::draw`（QPainter *画师）。
这个纯虚拟函数绘制该效应，并在需要绘制源时调用。
在`QGraphicsEffect`子类中重新实现该函数，以提供该效果的绘制实现，使用`painter`。
用户不应明确调用该函数，因为它仅用于重实现。

### `enum BlurHint { PerformanceHint, QualityHint, AnimationHint }`

**作用与语义：**

这个枚举描述了可以用来控制模糊效果应用的可能提示。这些提示可能在所有喷漆引擎中都会产生效果。
- `QGraphicsBlurEffect::PerformanceHint`：`0x00`;表示渲染性能是最重要的因素，但可能以较低的质量为代价。
- `QGraphicsBlurEffect::QualityHint`：`0x01`;表示渲染质量是最重要的因素，但这可能带来性能下降的代价。
- `QGraphicsBlurEffect::AnimationHint`：`0x02`;表示模糊半径将被动画化，暗示实现可以缓存模糊的源版本。如果源将动态变化，请勿使用此提示。
BlurHints 类型是 QFlags 的 typedef<BlurHint>。它存储 BlurHint 值的 OR 组合。

### `flags BlurHints`

**作用与语义：**

这个枚举描述了可以用来控制模糊效果应用的可能提示。这些提示可能在所有喷漆引擎中都会产生效果。
- `QGraphicsBlurEffect::PerformanceHint`：`0x00`;表示渲染性能是最重要的因素，但可能以较低的质量为代价。
- `QGraphicsBlurEffect::QualityHint`：`0x01`;表示渲染质量是最重要的因素，但这可能带来性能下降的代价。
- `QGraphicsBlurEffect::AnimationHint`：`0x02`;表示模糊半径将被动画化，暗示实现可以缓存模糊的源版本。如果源将动态变化，请勿使用此提示。
BlurHints 类型是 QFlags 的 typedef<BlurHint>。它存储 BlurHint 值的 OR 组合。

### `QGraphicsBlurEffect::BlurHints blurHints() const`

**作用与语义：**

这种特性保留了模糊效果的暗示。
用`PerformanceHint`提示表示你想要更快的模糊，`QualityHint`提示表示你喜欢更高质量的模糊，或者用`AnimationHint`来表示你想动画化模糊半径。
默认情况下，模糊提示是`PerformanceHint`。

**如何使用：** 调用 `blurHints()` 读取当前值；它不会修改应用状态。

### `qreal blurRadius() const`

**作用与语义：**

该特性保持了该效果的模糊半径。
使用较小的半径会让画面更清晰，而大半径则会让画面更模糊。
默认的模糊半径是5像素。
半径以设备坐标表示，意味着不受比例尺影响。

**如何使用：** 调用 `blurRadius()` 读取当前值；它不会修改应用状态。

### `void setBlurHints(QGraphicsBlurEffect::BlurHints hints)`

**作用与语义：**

这种特性保留了模糊效果的暗示。
用`PerformanceHint`提示表示你想要更快的模糊，`QualityHint`提示表示你喜欢更高质量的模糊，或者用`AnimationHint`来表示你想动画化模糊半径。
默认情况下，模糊提示是`PerformanceHint`。

**如何使用：** 调用 `setBlurHints(...)` 修改 `blurHints`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setBlurRadius(qreal blurRadius)`

**作用与语义：**

该特性保持了该效果的模糊半径。
使用较小的半径会让画面更清晰，而大半径则会让画面更模糊。
默认的模糊半径是5像素。
半径以设备坐标表示，意味着不受比例尺影响。

**如何使用：** 调用 `setBlurRadius(...)` 修改 `blurRadius`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QGraphicsBlurEffect` 所属机制类型：图形场景与项目机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
