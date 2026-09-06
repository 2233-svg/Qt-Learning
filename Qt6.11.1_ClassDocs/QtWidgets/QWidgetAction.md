# QWidgetAction

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QWidgetAction` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QWidgetAction` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QWidgetAction>`
- 继承自：QAction
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

- `QWidgetAction(QObject *parent)`
- `virtual ~QWidgetAction()`
- `QWidget * defaultWidget() const`
- `void releaseWidget(QWidget *widget)`
- `QWidget * requestWidget(QWidget *parent)`
- `void setDefaultWidget(QWidget *widget)`

### 保护函数

- `virtual QWidget * createWidget(QWidget *parent)`
- `QList<QWidget *> createdWidgets() const`
- `virtual void deleteWidget(QWidget *widget)`

### 重实现的保护函数

- `virtual bool event(QEvent *event) override`
- `virtual bool eventFilter(QObject *obj, QEvent *event) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QWidgetAction::QWidgetAction(QObject *parent)`

**作用与语义：**

构造一个带有`parent`的动作。

### `[virtual noexcept] QWidgetAction::~QWidgetAction()`

**作用与语义：**

摧毁该物体并释放分配的资源。

### `[virtual protected] QWidget *QWidgetAction::createWidget(QWidget *parent)`

**作用与语义：**

每当该动作被添加到支持自定义控件的容器控件时，都会调用该函数。如果你不希望自定义控件作为指定 `parent` 控件中动作的表示，则应返回 0。

### `[protected] QList<QWidget *> QWidgetAction::createdWidgets() const`

**作用与语义：**

返回已使用`createWidget()`且当前被添加该动作的小部件使用的控件列表。

### `QWidget *QWidgetAction::defaultWidget() const`

**作用与语义：**

返回默认控件。

### `[virtual protected] void QWidgetAction::deleteWidget(QWidget *widget)`

**作用与语义：**

每当操作从容器控件中移除时，该控件使用之前用 `createWidget()` 创建的自定义`widget`显示该动作时，都会调用该函数。默认实现会隐藏该`widget`，并用 `QObject::deleteLater()` 调度删除。

### `[override virtual protected] bool QWidgetAction::event(QEvent *event)`

**作用与语义：**

重装：`QAction::event`（QEvent *e）。

### `[override virtual protected] bool QWidgetAction::eventFilter(QObject *obj, QEvent *event)`

**作用与语义：**

重装：`QObject::eventFilter`（QObject *已观看，QEvent *事件）。

### `void QWidgetAction::releaseWidget(QWidget *widget)`

**作用与语义：**

释放指定的`widget`。
支持动作的容器小部件在小部件动作被移除时调用该函数。

### `QWidget *QWidgetAction::requestWidget(QWidget *parent)`

**作用与语义：**

返回一个表示动作的小部件，`parent`。
支持动作的容器小部件可以调用该函数，请求小部件作为动作的可视化表示。

### `void QWidgetAction::setDefaultWidget(QWidget *widget)`

**作用与语义：**

将`widget`设置为默认控件。所有权转移给`QWidgetAction`。除非子类重新实现`createWidget()`返回新控件，否则当容器控件通过`requestWidget()`请求控件时，默认控件会被使用。

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

`QWidgetAction` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
