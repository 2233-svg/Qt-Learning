# QSpacerItem

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QSpacerItem` 是 布局管理机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QSpacerItem` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QSpacerItem>`
- 继承自：QLayoutItem
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

### 公有函数

- `QSpacerItem(int w, int h, QSizePolicy::Policy hPolicy = QSizePolicy::Minimum, QSizePolicy::Policy vPolicy = QSizePolicy::Minimum)`
- `virtual ~QSpacerItem()`
- `void changeSize(int w, int h, QSizePolicy::Policy hPolicy = QSizePolicy::Minimum, QSizePolicy::Policy vPolicy = QSizePolicy::Minimum)`
- `QSizePolicy sizePolicy() const`

### 重实现的公有函数

- `virtual Qt::Orientations expandingDirections() const override`
- `virtual QRect geometry() const override`
- `virtual bool isEmpty() const override`
- `virtual QSize maximumSize() const override`
- `virtual QSize minimumSize() const override`
- `virtual void setGeometry(const QRect &r) override`
- `virtual QSize sizeHint() const override`
- `virtual QSpacerItem * spacerItem() override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QSpacerItem::QSpacerItem(int w, int h, QSizePolicy::Policy hPolicy = QSizePolicy::Minimum, QSizePolicy::Policy vPolicy = QSizePolicy::Minimum)`

**作用与语义：**

构造具有首选宽度`w`、首选高度`h`、水平大小政策`hPolicy`和垂直尺寸策略`vPolicy`的间隔项。
默认值提供一个间隙，如果没有其他东西需要空间，可以拉伸。

### `[virtual noexcept] QSpacerItem::~QSpacerItem()`

**作用与语义：**

毁灭者。

### `void QSpacerItem::changeSize(int w, int h, QSizePolicy::Policy hPolicy = QSizePolicy::Minimum, QSizePolicy::Policy vPolicy = QSizePolicy::Minimum)`

**作用与语义：**

将该间隔项更改为首选宽度`w`、首选高度`h`、水平尺寸政策`hPolicy`和垂直尺寸政策`vPolicy`。
默认值提供一个间隙，如果没有其他东西需要空间，可以拉伸。
注意，如果在间隔项添加到布局后调用changeSize()，则需要使布局失效，才能使间隔项的新大小生效。

### `[override virtual] Qt::Orientations QSpacerItem::expandingDirections() const`

**作用与语义：**

重实现自：`QLayoutItem::expandingDirections()` const.
返回该布局项目是否能利用比`sizeHint()`更多的空间。值为`Qt::Vertical`或`Qt::Horizontal`表示它只想在一个维度上增长，而`Qt::Vertical` |`Qt::Horizontal`表示它想在两个维度上都增长。

### `[override virtual] QRect QSpacerItem::geometry() const`

**作用与语义：**

重装：`QLayoutItem::geometry()` const.
返回该布局项目覆盖的矩形。

### `[override virtual] bool QSpacerItem::isEmpty() const`

**作用与语义：**

重装：`QLayoutItem::isEmpty()` const.
`true`回归。
在子类中实现，返回该项是否为空，即是否包含任何控件。

### `[override virtual] QSize QSpacerItem::maximumSize() const`

**作用与语义：**

重实现自：`QLayoutItem::maximumSize()` const.
在子类中实现以返回该项的最大大小。

### `[override virtual] QSize QSpacerItem::minimumSize() const`

**作用与语义：**

重实现自：`QLayoutItem::minimumSize()` const.
在子类中实现，以返回该项的最小大小。

### `[override virtual] void QSpacerItem::setGeometry(const QRect &r)`

**作用与语义：**

重装：`QLayoutItem::setGeometry`（const QRect & r）。
在子类中实现，将该物品的几何体设置为`r`。

### `[override virtual] QSize QSpacerItem::sizeHint() const`

**作用与语义：**

重装：`QLayoutItem::sizeHint()` const.
在子类中实现，以返回该物品的首选大小。

### `QSizePolicy QSpacerItem::sizePolicy() const`

**作用与语义：**

退货，按本商品的尺寸政策。

### `[override virtual] QSpacerItem *QSpacerItem::spacerItem()`

**作用与语义：**

重装：`QLayoutItem::spacerItem()`。
返回指向该对象的指针。
如果该项是`QSpacerItem`，则返回为`QSpacerItem`;否则返回`nullptr`。该函数提供类型安全的铸造。

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

`QSpacerItem` 所属机制类型：布局管理机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
