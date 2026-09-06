# QSplitter

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QSplitter` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QSplitter` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QSplitter>`
- 继承自：QFrame
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

### 属性

- `childrenCollapsible : bool`
- `handleWidth : int`
- `opaqueResize : bool`
- `orientation : Qt::Orientation`

### 公有函数

- `QSplitter(QWidget *parent = nullptr)`
- `QSplitter(Qt::Orientation orientation, QWidget *parent = nullptr)`
- `virtual ~QSplitter()`
- `void addWidget(QWidget *widget)`
- `bool childrenCollapsible() const`
- `int count() const`
- `void getRange(int index, int *min, int *max) const`
- `QSplitterHandle * handle(int index) const`
- `int handleWidth() const`
- `int indexOf(QWidget *widget) const`
- `void insertWidget(int index, QWidget *widget)`
- `bool isCollapsible(int index) const`
- `bool opaqueResize() const`
- `Qt::Orientation orientation() const`
- `void refresh()`
- `QWidget * replaceWidget(int index, QWidget *widget)`
- `bool restoreState(const QByteArray &state)`
- `QByteArray saveState() const`
- `void setChildrenCollapsible(bool)`
- `void setCollapsible(int index, bool collapse)`
- `void setHandleWidth(int)`
- `void setOpaqueResize(bool opaque = true)`
- `void setOrientation(Qt::Orientation)`
- `void setSizes(const QList<int> &list)`
- `void setStretchFactor(int index, int stretch)`
- `QList<int> sizes() const`
- `QWidget * widget(int index) const`

### 重实现的公有函数

- `virtual QSize minimumSizeHint() const override`
- `virtual QSize sizeHint() const override`

### 信号

- `void splitterMoved(int pos, int index)`

### 保护函数

- `int closestLegalPosition(int pos, int index)`
- `virtual QSplitterHandle * createHandle()`
- `void moveSplitter(int pos, int index)`
- `void setRubberBand(int pos)`

### 重实现的保护函数

- `virtual void changeEvent(QEvent *ev) override`
- `virtual void childEvent(QChildEvent *c) override`
- `virtual bool event(QEvent *e) override`
- `virtual void resizeEvent(QResizeEvent *) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `childrenCollapsible : bool`

**作用与语义：**

该属性适用于用户是否可以将子部件大小调整为 0。
默认情况下，子部件可折叠。可以使用 `setCollapsible()` 启用或禁用单个子部件的折叠。

**如何使用：** 调用 `childrenCollapsible()` 读取当前值；它不会修改应用状态。

### `handleWidth : int`

**作用与语义：**

该属性决定了分线器手柄的宽度。
默认情况下，该属性包含一个取决于用户平台和风格偏好的值。
如果你把handleWidth设为1或0，实际抓取区域会扩大到与相应控件的几个像素重叠。

**如何使用：** 调用 `handleWidth()` 读取当前值；它不会修改应用状态。

### `opaqueResize : bool`

**作用与语义：**

如果控件在交互式移动分线器时动态（不透明度）调整大小，返回`true`。否则返回`false`。
默认的缩放行为依赖于样式（由SH_Splitter_OpaqueResize样式提示决定）。不过，你可以通过调用 setOpaqueResize() 来覆盖它。

**如何使用：** 调用 `opaqueResize()` 读取当前值；它不会修改应用状态。

### `orientation : Qt::Orientation`

**作用与语义：**

此属性保存分割器的方向。
默认情况下，方向为水平（即小部件并排排列）。可能的方向为 `Qt::Horizontal` 和 `Qt::Vertical`。

**如何使用：** 调用 `orientation()` 读取当前值；它不会修改应用状态。

### `[explicit] QSplitter::QSplitter(QWidget *parent = nullptr)`

**作用与语义：**

构造一个水平分路器，并将`parent`参数传递给`QFrame`构造器。

### `[explicit] QSplitter::QSplitter(Qt::Orientation orientation, QWidget *parent = nullptr)`

**作用与语义：**

构建一个带有给定`orientation`和`parent`的分线器。

### `[virtual noexcept] QSplitter::~QSplitter()`

**作用与语义：**

摧毁分流器。所有子节点都被删除。

### `void QSplitter::addWidget(QWidget *widget)`

**作用与语义：**

在所有其他物品之后，将给定的`widget`添加到分配器的布局中。
如果`widget`已经在分线器里，它会被移到新位置。
注意：分配器会对小部件拥有所有权。

### `[override virtual protected] void QSplitter::changeEvent(QEvent *ev)`

**作用与语义：**

重实现自：`QFrame::changeEvent`（QEvent *ev）。

### `[override virtual protected] void QSplitter::childEvent(QChildEvent *c)`

**作用与语义：**

重实现自：`QObject::childEvent`（QChildEvent *event）。
告诉分路器`c`描述的子控件已入或移除。
这种方法也用于处理以分流器为父组件创建但未通过`insertWidget()`或`addWidget()`显式添加的控件的情况。这是为了兼容性，而非新代码中推荐的分拆器配置方式。请在新代码中使用`insertWidget()`或`addWidget()`。

### `[protected] int QSplitter::closestLegalPosition(int pos, int index)`

**作用与语义：**

返回`index`时最接近`pos`的法律位置。
对于从右到左的语言，如阿拉伯语和希伯来语，水平分线器的布局是相反的。位置从小部件的右侧边缘测量。

### `int QSplitter::count() const`

**作用与语义：**

返回分配器布局中包含的控件数量。

### `[virtual protected] QSplitterHandle *QSplitter::createHandle()`

**作用与语义：**

返回一个新的分流器句柄，作为该分流器的子控件。该函数可以在子类中重新实现，以支持自定义句柄。

### `[override virtual protected] bool QSplitter::event(QEvent *e)`

**作用与语义：**

重实现自：`QFrame::event`（QEvent *e）。

### `void QSplitter::getRange(int index, int *min, int *max) const`

**作用与语义：**

如果`min`和`max`不是0，则返回分线器在`index`*`min`和*`max`的有效范围，返回*和*的有效范围。

### `QSplitterHandle *QSplitter::handle(int index) const`

**作用与语义：**

在`index`分配器布局中，返回该物品左侧（或上方）的手柄，若无该物品则返回`nullptr`。索引0的手柄始终隐藏。
对于从右到左的语言，如阿拉伯语和希伯来语，水平分配器的布局相反。手柄位于小部件右侧，`index`。

### `int QSplitter::indexOf(QWidget *widget) const`

**作用与语义：**

返回分配器布局中指定`widget`的索引，若未找到索引则返回`widget` -1。这对句柄同样有效。
句柄编号从0开始。柄的数量与子控件的数量相当，但位置0的柄总是隐藏的。

### `void QSplitter::insertWidget(int index, QWidget *widget)`

**作用与语义：**

在指定`index`将指定的`widget`插入分配器的布局中。
如果`widget`已经在分线器里，它会被移到新位置。
如果`index`是无效索引，那么该控件会入到末尾。
注意：分配器会对小部件拥有所有权。

### `bool QSplitter::isCollapsible(int index) const`

**作用与语义：**

如果 在 `index` 的控件是可折叠的，返回 `true`，否则返回 `false`。

### `[override virtual] QSize QSplitter::minimumSizeHint() const`

**作用与语义：**

重新实现属性的访问函数：`QWidget::minimumSizeHint`。

### `[protected] void QSplitter::moveSplitter(int pos, int index)`

**作用与语义：**

将分流器手柄的左边或上边`index`移动到尽可能接近定位`pos`，即小部件左边或上边的距离。
对于从右到左的语言，如阿拉伯语和希伯来语，水平分配器的布局相反。`pos` 是小部件右边的距离。

### `void QSplitter::refresh()`

**作用与语义：**

更新分路器的状态。你不需要调用这个函数。

### `QWidget *QSplitter::replaceWidget(int index, QWidget *widget)`

**作用与语义：**

`widget`在分配器布局中替换该小部件，`index`。
如果`index`有效且`widget`不是分频器的子组件，则返回刚刚被替换的控件。否则返回空，且不进行替换或加法。
新插入的控件的几何体将与它替换的控件相同。其可见和折叠状态也会继承。
注意：分流器会获得`widget`的所有权，并将被替换小部件的父节点设置为空。
注意：由于`widget`会`reparented`分线器，其`geometry`可能不会立即设置，只有在`widget`收到相应事件后才会设置。

### `[override virtual protected] void QSplitter::resizeEvent(QResizeEvent *)`

**作用与语义：**

重实现自：`QWidget::resizeEvent`（QResizeEvent *event）。
该事件处理程序可以在子类中重新实现，以接收通过 `event` 参数传递的控件调整大小事件。当调用 resizeEvent() 时，控件已经拥有新的几何体。旧的大小可以通过 `QResizeEvent::oldSize()` 访问。
控件会被擦除，并在处理调整尺寸事件后立即接收绘图事件。不需要（也不应该）在这个处理程序中进行绘图。

### `bool QSplitter::restoreState(const QByteArray &state)`

**作用与语义：**

恢复分配器的布局至指定`state`。如果状态恢复，返回`true`;否则返回`false`。
通常这与`QSettings`结合使用，以恢复上一次会话的大小。这里有一个例子：
恢复分配器的状态：
无法恢复分配器的布局可能是由于提供的字节数组中存在无效或过时的数据。

**官方示例：**

```cpp
 QSettings settings;
 splitter->restoreState(settings.value("splitterSizes").toByteArray());
```

### `QByteArray QSplitter::saveState() const`

**作用与语义：**

这样可以避免分流器的布局状态。
通常这与`QSettings`结合使用，以记住未来会话的大小。版本号作为数据的一部分被存储。这里有一个示例：

**官方示例：**

```cpp
 QSettings settings;
 settings.setValue("splitterSizes", splitter->saveState());
```

### `void QSplitter::setCollapsible(int index, bool collapse)`

**作用与语义：**

设置子控件在`index`是否可折叠为`collapse`。
默认情况下，子节点是可折叠的，这意味着用户可以将其缩小到大小为0，即使其`minimumSize()`或`minimumSizeHint()`非零。这种行为可以通过调用该函数在每个控件上更改，或者通过设置`childrenCollapsible`属性对分流器中所有控件进行全局调整。

### `[protected] void QSplitter::setRubberBand(int pos)`

**作用与语义：**

在位置`pos`显示橡皮筋。如果`pos`为负，橡皮筋将被移除。

### `void QSplitter::setSizes(const QList<int> &list)`

**作用与语义：**

将子控件的大小设置为`list`中给出的值。
如果分路器是水平的，值会设置每个小部件的宽度（像素数），从左到右。如果分路器是垂直的，则每个小部件的高度从上到下固定。
`list`中多余的值被忽略。如果`list`包含的值太少，结果是未定义的，但程序仍然表现良好。
分配器小部件的整体大小不受影响。相反，任何额外或缺失的空间会根据大小的相对权重分配到各个小部件之间。
如果你指定大小为0，小部件将是不可见的。小部件的大小策略会被保留。也就是说，小于该小部件最小大小提示的值将被提示值替代。

### `void QSplitter::setStretchFactor(int index, int stretch)`

**作用与语义：**

更新位置`index`的组件大小策略，使其伸缩因子为`stretch`。
`stretch`不是有效伸缩因子;有效伸缩因子是通过取小部件的初始尺寸乘以`stretch`计算得出的。
该功能仅为方便而提供。它等价于。

**官方示例：**

```cpp
 QWidget *widget = splitter->widget(index);
 QSizePolicy policy = widget->sizePolicy();
 policy.setHorizontalStretch(stretch);
 policy.setVerticalStretch(stretch);
 widget->setSizePolicy(policy);
```

### `[override virtual] QSize QSplitter::sizeHint() const`

**作用与语义：**

重实现自：`QFrame::sizeHint()` const.
重新实现了属性的访问函数：`QWidget::sizeHint`。

### `QList<int> QSplitter::sizes() const`

**作用与语义：**

返回该分路器中所有控件的大小参数列表。
如果分流器的方向是水平的，列表包含控件的宽度（像素单位，从左到右）;如果方向是垂直的，列表包含控件的高度（像素单位，从上到下）。
将这些值赋予另一个分流器的`setSizes()`函数，会生成一个布局与此分流器相同的分流器。
注意，隐形小部件的大小为0。

### `[signal] void QSplitter::splitterMoved(int pos, int index)`

**作用与语义：**

当特定`index`的分路器手柄被移动到位置`pos`时，会发出该信号。
对于从右到左的语言，如阿拉伯语和希伯来语，水平分流器的布局相反。`pos` 是小部件右边的距离。

### `QWidget *QSplitter::widget(int index) const`

**作用与语义：**

在分配器布局中的指定`index`返回小部件，若没有该小部件则返回`nullptr`。

### `bool childrenCollapsible() const`

**作用与语义：**

该属性适用于用户是否可以将子部件大小调整为 0。
默认情况下，子部件可折叠。可以使用 `setCollapsible()` 启用或禁用单个子部件的折叠。

**如何使用：** 调用 `childrenCollapsible()` 读取当前值；它不会修改应用状态。

### `int handleWidth() const`

**作用与语义：**

该属性决定了分线器手柄的宽度。
默认情况下，该属性包含一个取决于用户平台和风格偏好的值。
如果你把handleWidth设为1或0，实际抓取区域会扩大到与相应控件的几个像素重叠。

**如何使用：** 调用 `handleWidth()` 读取当前值；它不会修改应用状态。

### `bool opaqueResize() const`

**作用与语义：**

如果控件在交互式移动分线器时动态（不透明度）调整大小，返回`true`。否则返回`false`。
默认的缩放行为依赖于样式（由SH_Splitter_OpaqueResize样式提示决定）。不过，你可以通过调用 setOpaqueResize() 来覆盖它。

**如何使用：** 调用 `opaqueResize()` 读取当前值；它不会修改应用状态。

### `Qt::Orientation orientation() const`

**作用与语义：**

此属性保存分割器的方向。
默认情况下，方向为水平（即小部件并排排列）。可能的方向为 `Qt::Horizontal` 和 `Qt::Vertical`。

**如何使用：** 调用 `orientation()` 读取当前值；它不会修改应用状态。

### `void setChildrenCollapsible(bool)`

**作用与语义：**

该属性适用于用户是否可以将子部件大小调整为 0。
默认情况下，子部件可折叠。可以使用 `setCollapsible()` 启用或禁用单个子部件的折叠。

**如何使用：** 调用 `setChildrenCollapsible(...)` 修改 `childrenCollapsible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setHandleWidth(int)`

**作用与语义：**

该属性决定了分线器手柄的宽度。
默认情况下，该属性包含一个取决于用户平台和风格偏好的值。
如果你把handleWidth设为1或0，实际抓取区域会扩大到与相应控件的几个像素重叠。

**如何使用：** 调用 `setHandleWidth(...)` 修改 `handleWidth`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setOpaqueResize(bool opaque = true)`

**作用与语义：**

如果控件在交互式移动分线器时动态（不透明度）调整大小，返回`true`。否则返回`false`。
默认的缩放行为依赖于样式（由SH_Splitter_OpaqueResize样式提示决定）。不过，你可以通过调用 setOpaqueResize() 来覆盖它。

**如何使用：** 调用 `setOpaqueResize(...)` 修改 `opaqueResize`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setOrientation(Qt::Orientation)`

**作用与语义：**

此属性保存分割器的方向。
默认情况下，方向为水平（即小部件并排排列）。可能的方向为 `Qt::Horizontal` 和 `Qt::Vertical`。

**如何使用：** 调用 `setOrientation(...)` 修改 `orientation`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QSplitter` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
