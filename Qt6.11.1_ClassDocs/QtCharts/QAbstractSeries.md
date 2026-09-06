# QAbstractSeries

> Qt 6.11.1 · Qt Charts

## 1. 先建立直觉

**一句话定位：** `QAbstractSeries` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Charts 提供折线、柱状、饼图、散点图和坐标轴等数据可视化组件。

### 这是什么

`QAbstractSeries` 是 Qt Charts 中的抽象协议类型，通常通过具体子类、模型、插件或工厂来使用。

**内部模型：** 抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

**适用场景：** 当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。

**典型调用链：** 选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

**先记住的坑：** 不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

## 2. 依赖与对象关系

- 头文件：`#include <QAbstractSeries>`
- 继承自：QObject
- 直接派生类：QAbstractBarSeries、QAreaSeries、QBoxPlotSeries、QCandlestickSeries、QPieSeries,、QXYSeries

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

### 状态、生命周期和线程

**生命周期：** 先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

**状态与结果：** QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

**线程与事件循环：** QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

## 3. 直接使用

当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。 使用时通常按这个过程组织：选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum SeriesType { SeriesTypeLine, SeriesTypeArea, SeriesTypeBar, SeriesTypeStackedBar, SeriesTypePercentBar, …, SeriesTypeCandlestick }`

### 属性

- `name : QString`
- `opacity : qreal`
- `type : SeriesType`
- `useOpenGL : bool`
- `visible : bool`

### 公有函数

- `virtual ~QAbstractSeries()`
- `bool attachAxis(QAbstractAxis *axis)`
- `QList<QAbstractAxis *> attachedAxes()`
- `QChart * chart() const`
- `bool detachAxis(QAbstractAxis *axis)`
- `void hide()`
- `bool isVisible() const`
- `QString name() const`
- `qreal opacity() const`
- `void setName(const QString &name)`
- `void setOpacity(qreal opacity)`
- `void setUseOpenGL(bool enable = true)`
- `void setVisible(bool visible = true)`
- `void show()`
- `virtual QAbstractSeries::SeriesType type() const = 0`
- `bool useOpenGL() const`

### 信号

- `void nameChanged()`
- `void opacityChanged()`
- `void useOpenGLChanged()`
- `void visibleChanged()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QAbstractSeries::SeriesType`

**作用与语义：**

本枚举描述了该系列的类型。
- `QAbstractSeries::SeriesTypeLine`：`0`;折线图。
- `QAbstractSeries::SeriesTypeArea`：`1`;面积图。
- `QAbstractSeries::SeriesTypeBar`：`2`;一个竖柱形图。
- `QAbstractSeries::SeriesTypeStackedBar`：`3`;一个垂直堆叠条形图。
- `QAbstractSeries::SeriesTypePercentBar`：`4`;一个垂直百分比条形图。
- `QAbstractSeries::SeriesTypePie`：`5`;一个饼图。
- `QAbstractSeries::SeriesTypeScatter`：`6`;散点图。
- `QAbstractSeries::SeriesTypeSpline`：`7`;样条图。
- `QAbstractSeries::SeriesTypeHorizontalBar`：`8`;水平条形图。
- `QAbstractSeries::SeriesTypeHorizontalStackedBar`：`9`;水平堆叠柱状图。
- `QAbstractSeries::SeriesTypeHorizontalPercentBar`：`10`;水平百分比条形图。
- `QAbstractSeries::SeriesTypeBoxPlot`：`11`;一个箱形图。
- `QAbstractSeries::SeriesTypeCandlestick`：`12`;蜡烛图。

### `name : QString`

**作用与语义：**

该属性保存系列名称。
该名称显示在系列图例中，并支持 HTML 格式。

**如何使用：** 调用 `name()` 读取当前值；它不会修改应用状态。

### `opacity : qreal`

**作用与语义：**

该属性表示系列的不透明性。
默认情况下，不透明度为1.0。有效值范围为0.0（透明）到1.0（不透明）。

**如何使用：** 调用 `opacity()` 读取当前值；它不会修改应用状态。

### `[read-only] type : SeriesType`

**作用与语义：**

此属性保存系列的类型。

**如何使用：** 调用 `type()` 读取当前值；它不会修改应用状态。

### `useOpenGL : bool`

**作用与语义：**

指定是否通过使用 OpenGL 加速绘制系列。
仅支持使用 OpenGL 进行加速，适用于`QLineSeries`和 `QScatterSeries`。用作 `QAreaSeries` 边系列的线系列不能使用 OpenGL 加速。当图表包含任何用 OpenGL 绘制的系列时，图表区域顶部会创建一个透明的 QOpenGLWidget。加速序列不会绘制在底层`QGraphicsView`上，而是绘制在创建的 QOpenGLWidget 上。
使用OpenGL加速系列绘制所获得的性能取决于底层硬件，但在大多数情况下性能显著。例如，在标准台式机上，启用系列的OpenGL加速通常允许渲染至少一百倍的点数而不降低帧率。图表大小对帧率的影响也较小。
OpenGL的系列绘制加速适用于需要快速绘制大量点的场景。它以效率为优化，因此使用该系列的系列缺乏对许多非加速系列可实现的功能支持：
- 加速系列不支持系列动画。
- 加速系列不支持点标签。
- 笔型、马克笔形状和光线标记在加速串列中不考虑。仅支持实心线条和普通散点。散点点可以是圆形或矩形，具体取决于底层图形硬件和驱动程序。
- 极坐标图不支持加速系列。
- 在使用加速系列时，不建议启用图表阴影或使用透明图表背景色，因为这会显著降低帧率。
这些额外限制源于加速系列绘制在图表顶部的独立控件上：
- 如果你在包含加速系列的图表上绘制任何图形项，加速系列会绘制在这些项上。
- 为了使 QOpenGLWidget 部分透明，它需要叠加在所有其他控件之上。这意味着在使用加速系列时，不能让其他控件部分覆盖图表。
- 加速系列不支持图形场景连接多个图形视图的场景。
- 加速系列不支持在图表非默认几何体的场景中使用。例如，在图形视图中添加变换会导致加速系列绘制在与图表相关的错误位置。
默认值是`false`。

**如何使用：** 调用 `useOpenGL()` 读取当前值；它不会修改应用状态。

### `visible : bool`

**作用与语义：**

无论序列是否可见，这一属性都成立。
默认情况下，`true`。

**如何使用：** 调用 `visible()` 读取当前值；它不会修改应用状态。

### `[virtual noexcept] QAbstractSeries::~QAbstractSeries()`

**作用与语义：**

图表系列的虚拟毁灭者。

### `bool QAbstractSeries::attachAxis(QAbstractAxis *axis)`

**作用与语义：**

将`axis`指定的轴连接到系列上。
如果轴成功连接，回`true`，否则`false`。
注意：如果多个相同方向的轴连接到同一系列，它们的最小值和最大值会相同。

### `QList<QAbstractAxis *> QAbstractSeries::attachedAxes()`

**作用与语义：**

返回与系列相连的轴列表。通常，x轴和y轴都附加在一个系列上，唯独`QPieSeries`没有附加任何轴。

### `QChart *QAbstractSeries::chart() const`

**作用与语义：**

返回该系列所属的图表。
当该系列加入图表时自动设置，移除序列时自动重置。

### `bool QAbstractSeries::detachAxis(QAbstractAxis *axis)`

**作用与语义：**

将`axis`指定的轴从系列中分离。
如果轴线成功脱离，返回`true`，否则`false`。

### `void QAbstractSeries::hide()`

**作用与语义：**

这会让系列的可见度提升到`false`。

### `[signal] void QAbstractSeries::nameChanged()`

**作用与语义：**

该属性保存系列名称。
该名称显示在系列图例中，并支持 HTML 格式。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `name` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QAbstractSeries::opacityChanged()`

**作用与语义：**

该属性表示系列的不透明性。
默认情况下，不透明度为1.0。有效值范围为0.0（透明）到1.0（不透明）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `opacity` 的变化，不要把它当作普通函数主动调用。

### `void QAbstractSeries::show()`

**作用与语义：**

这会让该系列的可见度提升到`true`。

### `[signal] void QAbstractSeries::useOpenGLChanged()`

**作用与语义：**

指定是否通过使用 OpenGL 加速绘制系列。
仅支持使用 OpenGL 进行加速，适用于`QLineSeries`和 `QScatterSeries`。用作 `QAreaSeries` 边系列的线系列不能使用 OpenGL 加速。当图表包含任何用 OpenGL 绘制的系列时，图表区域顶部会创建一个透明的 QOpenGLWidget。加速序列不会绘制在底层`QGraphicsView`上，而是绘制在创建的 QOpenGLWidget 上。
使用OpenGL加速系列绘制所获得的性能取决于底层硬件，但在大多数情况下性能显著。例如，在标准台式机上，启用系列的OpenGL加速通常允许渲染至少一百倍的点数而不降低帧率。图表大小对帧率的影响也较小。
OpenGL的系列绘制加速适用于需要快速绘制大量点的场景。它以效率为优化，因此使用该系列的系列缺乏对许多非加速系列可实现的功能支持：
- 加速系列不支持系列动画。
- 加速系列不支持点标签。
- 笔型、马克笔形状和光线标记在加速串列中不考虑。仅支持实心线条和普通散点。散点点可以是圆形或矩形，具体取决于底层图形硬件和驱动程序。
- 极坐标图不支持加速系列。
- 在使用加速系列时，不建议启用图表阴影或使用透明图表背景色，因为这会显著降低帧率。
这些额外限制源于加速系列绘制在图表顶部的独立控件上：
- 如果你在包含加速系列的图表上绘制任何图形项，加速系列会绘制在这些项上。
- 为了使 QOpenGLWidget 部分透明，它需要叠加在所有其他控件之上。这意味着在使用加速系列时，不能让其他控件部分覆盖图表。
- 加速系列不支持图形场景连接多个图形视图的场景。
- 加速系列不支持在图表非默认几何体的场景中使用。例如，在图形视图中添加变换会导致加速系列绘制在与图表相关的错误位置。
默认值是`false`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `useOpenGL` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QAbstractSeries::visibleChanged()`

**作用与语义：**

无论序列是否可见，这一属性都成立。
默认情况下，`true`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `visible` 的变化，不要把它当作普通函数主动调用。

### `bool isVisible() const`

**作用与语义：**

无论序列是否可见，这一属性都成立。
默认情况下，`true`。

**如何使用：** 调用 `isVisible()` 读取当前值；它不会修改应用状态。

### `QString name() const`

**作用与语义：**

该属性保存系列名称。
该名称显示在系列图例中，并支持 HTML 格式。

**如何使用：** 调用 `name()` 读取当前值；它不会修改应用状态。

### `qreal opacity() const`

**作用与语义：**

该属性表示系列的不透明性。
默认情况下，不透明度为1.0。有效值范围为0.0（透明）到1.0（不透明）。

**如何使用：** 调用 `opacity()` 读取当前值；它不会修改应用状态。

### `void setName(const QString &name)`

**作用与语义：**

该属性保存系列名称。
该名称显示在系列图例中，并支持 HTML 格式。

**如何使用：** 调用 `setName(...)` 修改 `name`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setOpacity(qreal opacity)`

**作用与语义：**

该属性表示系列的不透明性。
默认情况下，不透明度为1.0。有效值范围为0.0（透明）到1.0（不透明）。

**如何使用：** 调用 `setOpacity(...)` 修改 `opacity`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setUseOpenGL(bool enable = true)`

**作用与语义：**

指定是否通过使用 OpenGL 加速绘制系列。
仅支持使用 OpenGL 进行加速，适用于`QLineSeries`和 `QScatterSeries`。用作 `QAreaSeries` 边系列的线系列不能使用 OpenGL 加速。当图表包含任何用 OpenGL 绘制的系列时，图表区域顶部会创建一个透明的 QOpenGLWidget。加速序列不会绘制在底层`QGraphicsView`上，而是绘制在创建的 QOpenGLWidget 上。
使用OpenGL加速系列绘制所获得的性能取决于底层硬件，但在大多数情况下性能显著。例如，在标准台式机上，启用系列的OpenGL加速通常允许渲染至少一百倍的点数而不降低帧率。图表大小对帧率的影响也较小。
OpenGL的系列绘制加速适用于需要快速绘制大量点的场景。它以效率为优化，因此使用该系列的系列缺乏对许多非加速系列可实现的功能支持：
- 加速系列不支持系列动画。
- 加速系列不支持点标签。
- 笔型、马克笔形状和光线标记在加速串列中不考虑。仅支持实心线条和普通散点。散点点可以是圆形或矩形，具体取决于底层图形硬件和驱动程序。
- 极坐标图不支持加速系列。
- 在使用加速系列时，不建议启用图表阴影或使用透明图表背景色，因为这会显著降低帧率。
这些额外限制源于加速系列绘制在图表顶部的独立控件上：
- 如果你在包含加速系列的图表上绘制任何图形项，加速系列会绘制在这些项上。
- 为了使 QOpenGLWidget 部分透明，它需要叠加在所有其他控件之上。这意味着在使用加速系列时，不能让其他控件部分覆盖图表。
- 加速系列不支持图形场景连接多个图形视图的场景。
- 加速系列不支持在图表非默认几何体的场景中使用。例如，在图形视图中添加变换会导致加速系列绘制在与图表相关的错误位置。
默认值是`false`。

**如何使用：** 调用 `setUseOpenGL(...)` 修改 `useOpenGL`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setVisible(bool visible = true)`

**作用与语义：**

无论序列是否可见，这一属性都成立。
默认情况下，`true`。

**如何使用：** 调用 `setVisible(...)` 修改 `visible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `virtual QAbstractSeries::SeriesType type() const = 0`

**作用与语义：**

此属性保存系列的类型。

**如何使用：** 调用 `type()` 读取当前值；它不会修改应用状态。

### `bool useOpenGL() const`

**作用与语义：**

指定是否通过使用 OpenGL 加速绘制系列。
仅支持使用 OpenGL 进行加速，适用于`QLineSeries`和 `QScatterSeries`。用作 `QAreaSeries` 边系列的线系列不能使用 OpenGL 加速。当图表包含任何用 OpenGL 绘制的系列时，图表区域顶部会创建一个透明的 QOpenGLWidget。加速序列不会绘制在底层`QGraphicsView`上，而是绘制在创建的 QOpenGLWidget 上。
使用OpenGL加速系列绘制所获得的性能取决于底层硬件，但在大多数情况下性能显著。例如，在标准台式机上，启用系列的OpenGL加速通常允许渲染至少一百倍的点数而不降低帧率。图表大小对帧率的影响也较小。
OpenGL的系列绘制加速适用于需要快速绘制大量点的场景。它以效率为优化，因此使用该系列的系列缺乏对许多非加速系列可实现的功能支持：
- 加速系列不支持系列动画。
- 加速系列不支持点标签。
- 笔型、马克笔形状和光线标记在加速串列中不考虑。仅支持实心线条和普通散点。散点点可以是圆形或矩形，具体取决于底层图形硬件和驱动程序。
- 极坐标图不支持加速系列。
- 在使用加速系列时，不建议启用图表阴影或使用透明图表背景色，因为这会显著降低帧率。
这些额外限制源于加速系列绘制在图表顶部的独立控件上：
- 如果你在包含加速系列的图表上绘制任何图形项，加速系列会绘制在这些项上。
- 为了使 QOpenGLWidget 部分透明，它需要叠加在所有其他控件之上。这意味着在使用加速系列时，不能让其他控件部分覆盖图表。
- 加速系列不支持图形场景连接多个图形视图的场景。
- 加速系列不支持在图表非默认几何体的场景中使用。例如，在图形视图中添加变换会导致加速系列绘制在与图表相关的错误位置。
默认值是`false`。

**如何使用：** 调用 `useOpenGL()` 读取当前值；它不会修改应用状态。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

### 状态和错误边界

QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

### 线程边界

QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

### 最容易出现的错误

不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QAbstractSeries` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
