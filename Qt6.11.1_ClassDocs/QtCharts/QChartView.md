# QChartView

> Qt 6.11.1 · Qt Charts

## 1. 先建立直觉

**一句话定位：** `QChartView` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Charts 提供折线、柱状、饼图、散点图和坐标轴等数据可视化组件。

### 这是什么

`QChartView` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QChartView>`
- 继承自：QGraphicsView
- 直接派生类：未在类页中列出

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

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

- `(since 6.2) enum RubberBand { NoRubberBand, VerticalRubberBand, HorizontalRubberBand, RectangleRubberBand, ClickThroughRubberBand }`
- `flags RubberBands`

### 公有函数

- `QChartView(QWidget *parent = nullptr)`
- `QChartView(QChart *chart, QWidget *parent = nullptr)`
- `virtual ~QChartView()`
- `QChart * chart() const`
- `QChartView::RubberBands rubberBand() const`
- `void setChart(QChart *chart)`
- `void setRubberBand(const QChartView::RubberBands &rubberBand)`

### 重实现的保护函数

- `virtual void mouseMoveEvent(QMouseEvent *event) override`
- `virtual void mousePressEvent(QMouseEvent *event) override`
- `virtual void mouseReleaseEvent(QMouseEvent *event) override`
- `virtual void resizeEvent(QResizeEvent *event) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[since 6.2] enum QChartView::RubberBandflags QChartView::RubberBands`

**作用与语义：**

本枚举描述了可以应用于矩形缩放区域的不同类型的橡皮筋效应。
- `QChartView::NoRubberBand`：`0x0`;不指定缩放区域，因此不启用缩放。
- `QChartView::VerticalRubberBand`：`0x1`;橡皮筋水平锁定于图表大小，可垂直拉动以指定缩放区域。
- `QChartView::HorizontalRubberBand`：`0x2`;橡皮筋垂直锁定于图表大小，可水平拉动以指定缩放区域。
- `QChartView::RectangleRubberBand`：`0x3`;橡皮筋固定在被扣动的点，可以垂直或水平拉动。
- `QChartView::ClickThroughRubberBand`：`0x80`;上述橡皮筋选项中的一个选项，允许将左键传递到图表项目，前提是这些图表项目接受点击。选择该选项时，使用橡皮筋选择模式之一。
这个枚举是在Qt 6.2引入的。
RubberBands类型是QFlag的typedef<RubberBand>。它存储了橡皮筋值的或组合。

### `[explicit] QChartView::QChartView(QWidget *parent = nullptr)`

**作用与语义：**

构造一个带有父`parent`的图表视图对象。

### `[explicit] QChartView::QChartView(QChart *chart, QWidget *parent = nullptr)`

**作用与语义：**

构建一个带有父`parent`的图表视图对象以显示图表的`chart`。图表的所有权转移给图表视图。

### `[virtual noexcept] QChartView::~QChartView()`

**作用与语义：**

删除图表视图对象和相关的图表。

### `QChart *QChartView::chart() const`

**作用与语义：**

返回指向关联图表的指针。

### `[override virtual protected] void QChartView::mouseMoveEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QGraphicsView::mouseMoveEvent`（QMouseEvent *event）。
如果橡皮筋矩形出现在`event`指定的新闻事件中，事件数据用于更新橡皮筋几何形状。否则，调用默认`QGraphicsView::mouseMoveEvent()`实现。

### `[override virtual protected] void QChartView::mousePressEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QGraphicsView::mousePressEvent`（QMouseEvent *event）。
如果按下左键并启用橡皮筋，事件`event`会被接受，橡皮筋会显示在屏幕上。这使用户能够选择缩放区域。
如果按下其他鼠标按钮或禁用橡皮筋，事件会传递给`QGraphicsView::mousePressEvent()`。

### `[override virtual protected] void QChartView::mouseReleaseEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QGraphicsView::mouseReleaseEvent`（QMouseEvent *event）。
如果松开左键且橡皮筋已启用，事件`event`被接受，视角会缩放到橡皮筋指定的矩形区域。如果松开右键触发事件，视角会缩小。

### `[override virtual protected] void QChartView::resizeEvent(QResizeEvent *event)`

**作用与语义：**

重实现自：`QGraphicsView::resizeEvent`（QResizeEvent *event）。
利用`event`指定的数据调整和更新图表区域。

### `QChartView::RubberBands QChartView::rubberBand() const`

**作用与语义：**

返回当前图表视图使用的橡皮筋旗。

### `void QChartView::setChart(QChart *chart)`

**作用与语义：**

将当前图表设置为`chart`。新图表的所有权转移给图表视图，释放之前图表的所有权。
为避免内存泄漏，必须删除之前的图表。

### `void QChartView::setRubberBand(const QChartView::RubberBands &rubberBand)`

**作用与语义：**

将橡皮筋标志设置为`rubberBand`。所选标志决定了缩放的执行方式。
注意：极坐标图不支持橡皮筋缩放。

### `(since 6.2) enum RubberBand { NoRubberBand, VerticalRubberBand, HorizontalRubberBand, RectangleRubberBand, ClickThroughRubberBand }`

**作用与语义：**

本枚举描述了可以应用于矩形缩放区域的不同类型的橡皮筋效应。
- `QChartView::NoRubberBand`：`0x0`;不指定缩放区域，因此不启用缩放。
- `QChartView::VerticalRubberBand`：`0x1`;橡皮筋水平锁定于图表大小，可垂直拉动以指定缩放区域。
- `QChartView::HorizontalRubberBand`：`0x2`;橡皮筋垂直锁定于图表大小，可水平拉动以指定缩放区域。
- `QChartView::RectangleRubberBand`：`0x3`;橡皮筋固定在被扣动的点，可以垂直或水平拉动。
- `QChartView::ClickThroughRubberBand`：`0x80`;上述橡皮筋选项中的一个选项，允许将左键传递到图表项目，前提是这些图表项目接受点击。选择该选项时，使用橡皮筋选择模式之一。
这个枚举是在Qt 6.2引入的。
RubberBands类型是QFlag的typedef<RubberBand>。它存储了橡皮筋值的或组合。

### `flags RubberBands`

**作用与语义：**

本枚举描述了可以应用于矩形缩放区域的不同类型的橡皮筋效应。
- `QChartView::NoRubberBand`：`0x0`;不指定缩放区域，因此不启用缩放。
- `QChartView::VerticalRubberBand`：`0x1`;橡皮筋水平锁定于图表大小，可垂直拉动以指定缩放区域。
- `QChartView::HorizontalRubberBand`：`0x2`;橡皮筋垂直锁定于图表大小，可水平拉动以指定缩放区域。
- `QChartView::RectangleRubberBand`：`0x3`;橡皮筋固定在被扣动的点，可以垂直或水平拉动。
- `QChartView::ClickThroughRubberBand`：`0x80`;上述橡皮筋选项中的一个选项，允许将左键传递到图表项目，前提是这些图表项目接受点击。选择该选项时，使用橡皮筋选择模式之一。
这个枚举是在Qt 6.2引入的。
RubberBands类型是QFlag的typedef<RubberBand>。它存储了橡皮筋值的或组合。

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

`QChartView` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
