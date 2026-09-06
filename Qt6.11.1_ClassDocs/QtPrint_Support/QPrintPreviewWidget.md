# QPrintPreviewWidget

> Qt 6.11.1 · Qt Print Support

## 1. 先建立直觉

**一句话定位：** `QPrintPreviewWidget` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Print Support 提供打印机、打印预览和打印作业相关接口。

### 这是什么

`QPrintPreviewWidget` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QPrintPreviewWidget>`
- 继承自：QWidget
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS PrintSupport)
target_link_libraries(mytarget PRIVATE Qt6::PrintSupport)
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

- `enum ViewMode { SinglePageView, FacingPagesView, AllPagesView }`
- `enum ZoomMode { CustomZoom, FitToWidth, FitInView }`

### 公有函数

- `QPrintPreviewWidget(QPrinter *printer, QWidget *parent = nullptr, Qt::WindowFlags flags = Qt::WindowFlags())`
- `QPrintPreviewWidget(QWidget *parent = nullptr, Qt::WindowFlags flags = Qt::WindowFlags())`
- `virtual ~QPrintPreviewWidget()`
- `int currentPage() const`
- `QPageLayout::Orientation orientation() const`
- `int pageCount() const`
- `QPrintPreviewWidget::ViewMode viewMode() const`
- `qreal zoomFactor() const`
- `QPrintPreviewWidget::ZoomMode zoomMode() const`

### 重实现的公有函数

- `virtual void setVisible(bool visible) override`

### 公有槽函数

- `void fitInView()`
- `void fitToWidth()`
- `void print()`
- `void setAllPagesViewMode()`
- `void setCurrentPage(int page)`
- `void setFacingPagesViewMode()`
- `void setLandscapeOrientation()`
- `void setOrientation(QPageLayout::Orientation orientation)`
- `void setPortraitOrientation()`
- `void setSinglePageViewMode()`
- `void setViewMode(QPrintPreviewWidget::ViewMode mode)`
- `void setZoomFactor(qreal factor)`
- `void setZoomMode(QPrintPreviewWidget::ZoomMode zoomMode)`
- `void updatePreview()`
- `void zoomIn(qreal factor = 1.1)`
- `void zoomOut(qreal factor = 1.1)`

### 信号

- `void paintRequested(QPrinter *printer)`
- `void previewChanged()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QPrintPreviewWidget::ViewMode`

**作用与语义：**

该枚举用于描述预览小部件的视图模式。
- `QPrintPreviewWidget::SinglePageView`：`0`;预览中单页的模式。
- `QPrintPreviewWidget::FacingPagesView`：`1`;预览中对面页面的模式。
- `QPrintPreviewWidget::AllPagesView`：`2`;一种预览中所有页面的视图模式。

### `enum QPrintPreviewWidget::ZoomMode`

**作用与语义：**

该枚举用于描述预览小部件的缩放模式。
- `QPrintPreviewWidget::CustomZoom`：`0`;缩放设置为自定义缩放值。
- `QPrintPreviewWidget::FitToWidth`：`1`;该模式将当前页面贴合到视图宽度。
- `QPrintPreviewWidget::FitInView`：`2`;该模式可将当前页面放入视图内。

### `[explicit] QPrintPreviewWidget::QPrintPreviewWidget(QPrinter *printer, QWidget *parent = nullptr, Qt::WindowFlags flags = Qt::WindowFlags())`

**作用与语义：**

基于`printer`构造一个QPrintPreviewWidget，`parent`为父控件。控件标志`flags`传递给`QWidget`构造器。

### `[explicit] QPrintPreviewWidget::QPrintPreviewWidget(QWidget *parent = nullptr, Qt::WindowFlags flags = Qt::WindowFlags())`

**作用与语义：**

这会促使 QPrintPreviewWidget 创建一个内部默认构造的 `QPrinter` 对象，用于生成预览。

### `[virtual noexcept] QPrintPreviewWidget::~QPrintPreviewWidget()`

**作用与语义：**

摧毁了`QPrintPreviewWidget`。

### `int QPrintPreviewWidget::currentPage() const`

**作用与语义：**

返回预览中当前浏览的页面。

### `[slot] void QPrintPreviewWidget::fitInView()`

**作用与语义：**

这是一个方便函数，和调用`setZoomMode(QPrintPreviewWidget::FitInView)`相同。

### `[slot] void QPrintPreviewWidget::fitToWidth()`

**作用与语义：**

这是一个方便函数，和调用`setZoomMode(QPrintPreviewWidget::FitToWidth)`相同。

### `QPageLayout::Orientation QPrintPreviewWidget::orientation() const`

**作用与语义：**

返回预览当前的朝向。该值来自与预览关联的`QPrinter`对象。

### `int QPrintPreviewWidget::pageCount() const`

**作用与语义：**

返回预览中的页数。

### `[signal] void QPrintPreviewWidget::paintRequested(QPrinter *printer)`

**作用与语义：**

当预览小部件需要生成一组预览页面时，会发出该信号。`printer` 是与该预览小部件关联的打印机。

### `[signal] void QPrintPreviewWidget::previewChanged()`

**作用与语义：**

每当预览小部件改变了某些内部状态（如方向）时，就会发出该信号。

### `[slot] void QPrintPreviewWidget::print()`

**作用与语义：**

将预览打印到与预览相关的打印机上。

### `[slot] void QPrintPreviewWidget::setAllPagesViewMode()`

**作用与语义：**

这是一个方便函数，和调用`setViewMode(QPrintPreviewWidget::AllPagesView)`相同。

### `[slot] void QPrintPreviewWidget::setCurrentPage(int page)`

**作用与语义：**

在预览中设置当前页面。这会导致视图跳转到`page`的开头。

### `[slot] void QPrintPreviewWidget::setFacingPagesViewMode()`

**作用与语义：**

这是一个方便功能，和调用`setViewMode(QPrintPreviewWidget::FacingPagesView)`相同。

### `[slot] void QPrintPreviewWidget::setLandscapeOrientation()`

**作用与语义：**

这是一个方便功能，和调用`setOrientation(QPageLayout::Landscape)`相同。

### `[slot] void QPrintPreviewWidget::setOrientation(QPageLayout::Orientation orientation)`

**作用与语义：**

将当前方向设置为`orientation`。该值会设置在与预览相关的`QPrinter`对象上。

### `[slot] void QPrintPreviewWidget::setPortraitOrientation()`

**作用与语义：**

这是一个方便函数，类似于调用`setOrientation(QPageLayout::Portrait)`。

### `[slot] void QPrintPreviewWidget::setSinglePageViewMode()`

**作用与语义：**

这是一个方便功能，和调用`setViewMode(QPrintPreviewWidget::SinglePageView)`相同。

### `[slot] void QPrintPreviewWidget::setViewMode(QPrintPreviewWidget::ViewMode mode)`

**作用与语义：**

将视图模式设置为`mode`。默认视图模式为`SinglePageView`。

### `[slot] void QPrintPreviewWidget::setZoomFactor(qreal factor)`

**作用与语义：**

将视野的缩放因子设置为`factor`。例如，1.0表示视野未按比例，约为纸张视图的大小。0.5时视野大小减半，2.0时视野大小翻倍。

### `[slot] void QPrintPreviewWidget::setZoomMode(QPrintPreviewWidget::ZoomMode zoomMode)`

**作用与语义：**

将缩放模式设置为`zoomMode`。默认缩放模式为`FitInView`。

### `[slot] void QPrintPreviewWidget::updatePreview()`

**作用与语义：**

该功能会更新预览，从而发出`paintRequested()`信号。

### `QPrintPreviewWidget::ViewMode QPrintPreviewWidget::viewMode() const`

**作用与语义：**

返回当前的视图模式。默认视图模式是`SinglePageView`。

### `qreal QPrintPreviewWidget::zoomFactor() const`

**作用与语义：**

返回视角的缩放因子。

### `[slot] void QPrintPreviewWidget::zoomIn(qreal factor = 1.1)`

**作用与语义：**

将当前视图放大`factor`。`factor`默认值是1.1，这意味着视图会被放大10%。

### `QPrintPreviewWidget::ZoomMode QPrintPreviewWidget::zoomMode() const`

**作用与语义：**

返回当前的缩放模式。

### `[slot] void QPrintPreviewWidget::zoomOut(qreal factor = 1.1)`

**作用与语义：**

将当前视图缩放`factor`。`factor`默认值是1.1，这意味着视图会缩放10%。

### `virtual void setVisible(bool visible) override`

**作用与语义：**

设置打印预览控件是否可见。传入 `true` 显示控件并让预览保持可用，传入 `false` 隐藏；常规代码通常调用 `show()`、`hide()` 或布局管理器间接触发它，不应绕过控件生命周期直接调用基类实现。

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

`QPrintPreviewWidget` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
