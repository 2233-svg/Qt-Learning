# QWidgetItem

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QWidgetItem` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QWidgetItem` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QWidgetItem>`
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

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QWidgetItem(QWidget *widget)`
- `virtual ~QWidgetItem()`

### 重实现的公有函数

- `virtual QSizePolicy::ControlTypes controlTypes() const override`
- `virtual Qt::Orientations expandingDirections() const override`
- `virtual QRect geometry() const override`
- `virtual bool hasHeightForWidth() const override`
- `virtual int heightForWidth(int w) const override`
- `virtual bool isEmpty() const override`
- `virtual QSize maximumSize() const override`
- `virtual QSize minimumSize() const override`
- `virtual void setGeometry(const QRect &rect) override`
- `virtual QSize sizeHint() const override`
- `virtual QWidget * widget() const override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QWidgetItem::QWidgetItem(QWidget *widget)`

**作用与语义：**

创建包含该`widget`的物品。

### `[virtual noexcept] QWidgetItem::~QWidgetItem()`

**作用与语义：**

毁灭者。

### `[override virtual] QSizePolicy::ControlTypes QWidgetItem::controlTypes() const`

**作用与语义：**

重装：`QLayoutItem::controlTypes()` const.
返回该大小策略所适用的小部件关联的控制类型。
返回布局项的控制类型。对于`QWidgetItem`，控制类型来自控件的大小策略;对于`QLayoutItem`，控制类型是从布局内容中推导出来的。

### `[override virtual] Qt::Orientations QWidgetItem::expandingDirections() const`

**作用与语义：**

重实现自：`QLayoutItem::expandingDirections()` const.
返回该布局项目是否能利用比`sizeHint()`更多的空间。值为`Qt::Vertical`或`Qt::Horizontal`表示它只想在一个维度上增长，而`Qt::Vertical` |`Qt::Horizontal`表示它想在两个维度上都增长。

### `[override virtual] QRect QWidgetItem::geometry() const`

**作用与语义：**

重装：`QLayoutItem::geometry()` const.
返回该布局项目覆盖的矩形。

### `[override virtual] bool QWidgetItem::hasHeightForWidth() const`

**作用与语义：**

重装：`QLayoutItem::hasHeightForWidth()` const.
如果该布局的首选高度取决于宽度，则返回`true`;否则返回`false`。默认实现返回false。
在支持宽度高度的布局管理器中重新实现这个功能。

### `[override virtual] int QWidgetItem::heightForWidth(int w) const`

**作用与语义：**

重装：`QLayoutItem::heightForWidth`（int） const.
返回该布局项的首选高度，基于宽度，但默认实现中未使用宽度。
默认实现返回 -1，表示首选高度与项目宽度无关。使用函数 `hasHeightForWidth()` 通常比调用该函数并测试 -1 快得多。
在支持宽度高度的布局管理器中重新实现该函数。典型的实现如下：
强烈建议缓存;没有缓存，布局将耗费指数级时间。

### `[override virtual] bool QWidgetItem::isEmpty() const`

**作用与语义：**

重实现自：`QLayoutItem::isEmpty()` const.
如果控件隐藏，返回`true`;否则返回`false`。
在子类中实现，返回该项是否为空，即是否包含任何控件。

### `[override virtual] QSize QWidgetItem::maximumSize() const`

**作用与语义：**

重实现自：`QLayoutItem::maximumSize()` const.
在子类中实现以返回该项的最大大小。

### `[override virtual] QSize QWidgetItem::minimumSize() const`

**作用与语义：**

重实现自：`QLayoutItem::minimumSize()` const.
在子类中实现，以返回该项的最小大小。

### `[override virtual] void QWidgetItem::setGeometry(const QRect &rect)`

**作用与语义：**

重装：`QLayoutItem::setGeometry`（const QRect & r）。
在子类中实现，将该物品的几何体设置为`r`。

### `[override virtual] QSize QWidgetItem::sizeHint() const`

**作用与语义：**

重装：`QLayoutItem::sizeHint()` const.
在子类中实现，以返回该物品的首选大小。

### `[override virtual] QWidget *QWidgetItem::widget() const`

**作用与语义：**

重装：`QLayoutItem::widget()` const.
返回由该项目管理的小部件。
如果该项管理`QWidget`，返回该控件。否则，返回`nullptr`。
注意：虽然函数`layout()`和`spacerItem()`执行cast，但该函数返回另一个对象：`QLayout`和`QSpacerItem`继承`QLayoutItem`，而`QWidget`则不继承。

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

`QWidgetItem` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
