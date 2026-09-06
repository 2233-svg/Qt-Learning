# QStackedLayout

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QStackedLayout` 是 布局管理机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QStackedLayout` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QStackedLayout>`
- 继承自：QLayout
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

**生命周期：** 顶层布局可以在构造时绑定到 QWidget，也可以通过 `setLayout()` 安装；嵌套布局加入父布局后所有权交给父布局。布局析构不会自动销毁普通 QWidget，动态移除项目时要分别处理控件、子布局和 spacer。

**状态与结果：** 布局的项目索引会随着 add、insert、remove 和 takeAt 改变；索引既包括控件，也包括子布局、固定空白和 stretch。修改项目或尺寸参数后 Qt 会使布局失效并重新计算。

**线程与事件循环：** 布局只应在 GUI 线程操作，因为它直接改变 QWidget 几何和可见界面。布局系统不负责业务线程同步，也不会把手动的跨线程控件访问变安全。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum StackingMode { StackOne, StackAll }`

### 属性

- `count : int`
- `currentIndex : int`
- `stackingMode : StackingMode`

### 公有函数

- `QStackedLayout()`
- `QStackedLayout(QLayout *parentLayout)`
- `QStackedLayout(QWidget *parent)`
- `virtual ~QStackedLayout()`
- `int addWidget(QWidget *widget)`
- `virtual int count() const override`
- `int currentIndex() const`
- `QWidget * currentWidget() const`
- `int insertWidget(int index, QWidget *widget)`
- `void setStackingMode(QStackedLayout::StackingMode stackingMode)`
- `QStackedLayout::StackingMode stackingMode() const`
- `QWidget * widget(int index) const`

### 重实现的公有函数

- `virtual void addItem(QLayoutItem *item) override`
- `virtual bool hasHeightForWidth() const override`
- `virtual int heightForWidth(int width) const override`
- `virtual QLayoutItem * itemAt(int index) const override`
- `virtual QSize minimumSize() const override`
- `virtual void setGeometry(const QRect &rect) override`
- `virtual QSize sizeHint() const override`
- `virtual QLayoutItem * takeAt(int index) override`

### 公有槽函数

- `void setCurrentIndex(int index)`
- `void setCurrentWidget(QWidget *widget)`

### 信号

- `void currentChanged(int index)`
- `(since 6.9) void widgetAdded(int index)`
- `void widgetRemoved(int index)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QStackedLayout::StackingMode`

**作用与语义：**

该枚举指定了布局如何处理其子控件的可见性。
- `QStackedLayout::StackOne`：`0`;仅当前控件可见。这是默认设置。
- `QStackedLayout::StackAll`：`1`;所有控件都可见。当前控件仅被抬高。

### `[read-only] count : int`

**作用与语义：**

该属性包含布局中包含的小部件数量。

**如何使用：** 调用 `count()` 读取当前值；它不会修改应用状态。

### `currentIndex : int`

**作用与语义：**

该属性表示可见控件的索引位置。
如果没有当前控件，当前索引为-1。

**如何使用：** 调用 `currentIndex()` 读取当前值；它不会修改应用状态。

### `stackingMode : StackingMode`

**作用与语义：**

决定了子控件的可见性处理方式。
默认值是`StackOne`。将属性设置为`StackAll`可以利用该布局来覆盖覆盖小部件，这些小部件在其他小部件之上进行额外绘图，例如图形编辑器。

**如何使用：** 调用 `stackingMode()` 读取当前值；它不会修改应用状态。

### `QStackedLayout::QStackedLayout()`

**作用与语义：**

构建一个没有父节点的 QStackedLayout。
该 QStackedLayout 必须在后续安装在小部件上才能生效。

### `[explicit] QStackedLayout::QStackedLayout(QLayout *parentLayout)`

**作用与语义：**

构建一个新的QStackedLayout并将其插入给定的`parentLayout`中。

### `[explicit] QStackedLayout::QStackedLayout(QWidget *parent)`

**作用与语义：**

用给定的`parent`构造一个新的QStackedLayout。
该布局会自行安装在`parent`小部件上，并管理其子组件的几何体。

### `[virtual noexcept] QStackedLayout::~QStackedLayout()`

**作用与语义：**

销毁该`QStackedLayout`。注意布局中的控件并未被销毁。

### `[override virtual] void QStackedLayout::addItem(QLayoutItem *item)`

**作用与语义：**

重实现自：`QLayout::addItem`（QLayoutItem *item）。
在子职业中实现以添加`item`。添加方式因子职业而异。
该函数通常不会在应用代码中调用。要向布局添加小部件，使用`addWidget()`函数;要添加子布局，使用相关`QLayout`子类提供的addLayout()函数。
注意：`item`的所有权转移到了布局上，删除它由布局负责。

### `int QStackedLayout::addWidget(QWidget *widget)`

**作用与语义：**

将给定`widget`添加到该布局末尾，返回`widget`的索引位置。
如果在调用该函数前`QStackedLayout`为空，则该`widget`即为当前控件。

### `[signal] void QStackedLayout::currentChanged(int index)`

**作用与语义：**

该属性表示可见控件的索引位置。
如果没有当前控件，当前索引为-1。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `currentIndex` 的变化，不要把它当作普通函数主动调用。

### `QWidget *QStackedLayout::currentWidget() const`

**作用与语义：**

返回当前控件，或者如果布局中没有控件，则返回`nullptr`。

### `[override virtual] bool QStackedLayout::hasHeightForWidth() const`

**作用与语义：**

重装：`QLayoutItem::hasHeightForWidth()` const.
如果该布局的首选高度取决于宽度，则返回`true`;否则返回`false`。默认实现返回false。
在支持宽度高度的布局管理器中重新实现这个功能。

### `[override virtual] int QStackedLayout::heightForWidth(int width) const`

**作用与语义：**

重装：`QLayoutItem::heightForWidth`（int） const.
返回该布局项的首选高度，基于宽度，但默认实现中未使用宽度。
默认实现返回 -1，表示首选高度与项目宽度无关。使用函数 `hasHeightForWidth()` 通常比调用该函数并测试 -1 快得多。
在支持宽度高度的布局管理器中重新实现该函数。典型的实现如下：
强烈建议缓存;没有缓存，布局将耗费指数级时间。

### `int QStackedLayout::insertWidget(int index, QWidget *widget)`

**作用与语义：**

在此`QStackedLayout`中，将给定的`widget`插入给定的`index`。如果`index`超出范围，则添加该控件（此时返回的是实际返回的`widget`索引）。
如果在调用该函数前`QStackedLayout`为空，给定的`widget`即为当前的控件。
在索引大小于或等于当前索引处插入新控件，会递增当前索引，但保留当前控件。

### `[override virtual] QLayoutItem *QStackedLayout::itemAt(int index) const`

**作用与语义：**

重实现自：`QLayout::itemAt`（int index）const.
必须在子类中实现以返回`index`的布局项。如果没有这样的项，函数必须返回`nullptr`。项编号从0依次排列。如果一个项被删除，其他项将被重新编号。
该函数可用于遍历布局。以下代码将为小部件布局结构中的每个布局项绘制一个矩形。

### `[override virtual] QSize QStackedLayout::minimumSize() const`

**作用与语义：**

重装：`QLayout::minimumSize()` const.

### `[slot] void QStackedLayout::setCurrentWidget(QWidget *widget)`

**作用与语义：**

将当前控件设置为指定的`widget`。新的当前控件必须已经包含在这个堆叠布局中。

### `[override virtual] void QStackedLayout::setGeometry(const QRect &rect)`

**作用与语义：**

重装：`QLayout::setGeometry`（const QRect & r）。

### `[override virtual] QSize QStackedLayout::sizeHint() const`

**作用与语义：**

重装：`QLayoutItem::sizeHint()` const.
在子类中实现，以返回该物品的首选大小。

### `[override virtual] QLayoutItem *QStackedLayout::takeAt(int index)`

**作用与语义：**

重实现自：`QLayout::takeAt`（整数索引）。
必须在子类中实现，以从布局中移除`index`的布局项并返回该项。如果没有这样的项，函数必须什么都不做，返回0。项编号从0开始依次编号。如果一个项被移除，其他项将被重新编号。
以下代码片段展示了一种安全移除所有布局物品的方法：

### `QWidget *QStackedLayout::widget(int index) const`

**作用与语义：**

返回给定`index`的控件，若无控件则返回`nullptr`。

### `[signal, since 6.9] void QStackedLayout::widgetAdded(int index)`

**作用与语义：**

每当添加或插入小部件时，该信号都会发出。小部件的`index`作为参数传递。

### `[signal] void QStackedLayout::widgetRemoved(int index)`

**作用与语义：**

每当小部件从布局中移除时，该信号都会发出。小部件的 `index` 作为参数传递。

### `virtual int count() const override`

**作用与语义：**

该属性包含布局中包含的小部件数量。

**如何使用：** 调用 `count()` 读取当前值；它不会修改应用状态。

### `int currentIndex() const`

**作用与语义：**

该属性表示可见控件的索引位置。
如果没有当前控件，当前索引为-1。

**如何使用：** 调用 `currentIndex()` 读取当前值；它不会修改应用状态。

### `void setStackingMode(QStackedLayout::StackingMode stackingMode)`

**作用与语义：**

决定了子控件的可见性处理方式。
默认值是`StackOne`。将属性设置为`StackAll`可以利用该布局来覆盖覆盖小部件，这些小部件在其他小部件之上进行额外绘图，例如图形编辑器。

**如何使用：** 调用 `setStackingMode(...)` 修改 `stackingMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QStackedLayout::StackingMode stackingMode() const`

**作用与语义：**

决定了子控件的可见性处理方式。
默认值是`StackOne`。将属性设置为`StackAll`可以利用该布局来覆盖覆盖小部件，这些小部件在其他小部件之上进行额外绘图，例如图形编辑器。

**如何使用：** 调用 `stackingMode()` 读取当前值；它不会修改应用状态。

### `void setCurrentIndex(int index)`

**作用与语义：**

该属性表示可见控件的索引位置。
如果没有当前控件，当前索引为-1。

**如何使用：** 调用 `setCurrentIndex(...)` 修改 `currentIndex`；传入的新值会成为后续查询和相关界面行为所使用的值。

## 6. 深入实践与常见坑

### 生命周期和资源边界

顶层布局可以在构造时绑定到 QWidget，也可以通过 `setLayout()` 安装；嵌套布局加入父布局后所有权交给父布局。布局析构不会自动销毁普通 QWidget，动态移除项目时要分别处理控件、子布局和 spacer。

### 状态和错误边界

布局的项目索引会随着 add、insert、remove 和 takeAt 改变；索引既包括控件，也包括子布局、固定空白和 stretch。修改项目或尺寸参数后 Qt 会使布局失效并重新计算。

### 线程边界

布局只应在 GUI 线程操作，因为它直接改变 QWidget 几何和可见界面。布局系统不负责业务线程同步，也不会把手动的跨线程控件访问变安全。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QStackedLayout` 所属机制类型：布局管理机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
