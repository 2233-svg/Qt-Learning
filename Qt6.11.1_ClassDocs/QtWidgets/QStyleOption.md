# QStyleOption

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QStyleOption` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QStyleOption` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QStyleOption>`
- 继承自：未在类页中列出
- 直接派生类：QStyleOptionButton、QStyleOptionComplex、QStyleOptionDockWidget、QStyleOptionFocusRect、QStyleOptionFrame、QStyleOptionGraphicsItem、QStyleOptionHeader、QStyleOptionMenuItem、QStyleOptionProgressBar、QStyleOptionRubberBand、QStyleOptionTab、QStyleOptionTabBarBase、QStyleOptionTabWidgetFrame、QStyleOptionToolBar、QStyleOptionToolBox,、QStyleOptionViewItem

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

- `enum OptionType { SO_Button, SO_ComboBox, SO_Complex, SO_Default, SO_DockWidget, …, SO_ComplexCustomBase }`
- `enum StyleOptionType { Type }`
- `enum StyleOptionVersion { Version }`

### 公有函数

- `QStyleOption(int version = QStyleOption::Version, int type = SO_Default)`
- `QStyleOption(const QStyleOption &other)`
- `~QStyleOption()`
- `void initFrom(const QWidget *widget)`
- `QStyleOption & operator=(const QStyleOption &other)`

### 相关非成员函数

- `T qstyleoption_cast(QStyleOption *option)`
- `T qstyleoption_cast(const QStyleOption *option)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QStyleOption::OptionType`

**作用与语义：**

这个枚举由`QStyleOption`、其子职业和`qstyleoption_cast()`内部使用，用来确定风格选项类型。一般来说，除非你想创建自己的`QStyleOption`子职业和风格，否则你不需要担心这个。
- `QStyleOption::SO_Button`：`2`;`QStyleOptionButton`
- `QStyleOption::SO_ComboBox`：`0xf0004`;`QStyleOptionComboBox`
- `QStyleOption::SO_Complex`：`0xf0000`;`QStyleOptionComplex`
- `QStyleOption::SO_Default`：`0`;`QStyleOption`
- `QStyleOption::SO_DockWidget`：`9`;`QStyleOptionDockWidget`
- `QStyleOption::SO_FocusRect`：`1`;`QStyleOptionFocusRect`
- `QStyleOption::SO_Frame`：`5`;`QStyleOptionFrame`
- `QStyleOption::SO_GraphicsItem`：`15`;`QStyleOptionGraphicsItem`
- `QStyleOption::SO_GroupBox`：`0xf0006`;`QStyleOptionGroupBox`
- `QStyleOption::SO_Header`：`8`;`QStyleOptionHeader`
- `QStyleOption::SO_MenuItem`：`4`;`QStyleOptionMenuItemV2`
- `QStyleOption::SO_ProgressBar`：`6`;`QStyleOptionProgressBar`
- `QStyleOption::SO_RubberBand`：`13`;`QStyleOptionRubberBand`
- `QStyleOption::SO_SizeGrip`：`0xf0007`;`QStyleOptionSizeGrip`
- `QStyleOption::SO_Slider`：`0xf0001`;`QStyleOptionSlider`
- `QStyleOption::SO_SpinBox`：`0xf0002`;`QStyleOptionSpinBox`
- `QStyleOption::SO_Tab`：`3`;`QStyleOptionTab`
- `QStyleOption::SO_TabBarBase`：`12`;`QStyleOptionTabBarBase`
- `QStyleOption::SO_TabWidgetFrame`：`11`;`QStyleOptionTabWidgetFrame`
- `QStyleOption::SO_TitleBar`：`0xf0005`;`QStyleOptionTitleBar`
- `QStyleOption::SO_ToolBar`：`14`;`QStyleOptionToolBar`
- `QStyleOption::SO_ToolBox`：`7`;`QStyleOptionToolBox`
- `QStyleOption::SO_ToolButton`：`0xf0003`;`QStyleOptionToolButton`
- `QStyleOption::SO_ViewItem`：`10`;`QStyleOptionViewItem`（访谈中使用）
以下数值用于自定义控制：
- `QStyleOption::SO_CustomBase`：`0xf00`;保留给自定义QStyleOptions;所有自定义控制值必须高于此值
- `QStyleOption::SO_ComplexCustomBase`：`0xf000000`;保留给自定义QStyleOptions;所有自定义复杂控制值必须高于此值

### `enum QStyleOption::StyleOptionType`

**作用与语义：**

该枚举用于保存样式选项类型的信息，并为每个`QStyleOption`子类定义。
- `QStyleOption::Type`：`SO_Default`;提供样式选项（`SO_Default`为本类别）。
类型由`QStyleOption`、其子职业和`qstyleoption_cast()`内部使用，用来确定风格类型选项。一般来说，除非你想创建自己的`QStyleOption`子职业和风格，否则不必担心这些。

### `enum QStyleOption::StyleOptionVersion`

**作用与语义：**

该枚举用于保存样式选项版本的信息，并为每个`QStyleOption`子类定义。
- `QStyleOption::Version`：`1`;1
该版本被`QStyleOption`子类用于实现扩展而不破坏兼容性。如果你使用`qstyleoption_cast()`，通常不需要检查。

### `QStyleOption::QStyleOption(int version = QStyleOption::Version, int type = SO_Default)`

**作用与语义：**

构建一个带有指定`version`和`type`的QStyleOption。
该版本对QStyleOption没有特殊含义;子类可以用它来区分同一期权类型的不同版本。
`state`成员变量初始化为`QStyle::State_None`。

### `QStyleOption::QStyleOption(const QStyleOption &other)`

**作用与语义：**

复制了`other`。

### `[noexcept] QStyleOption::~QStyleOption()`

**作用与语义：**

会破坏这个风格选项对象。

### `void QStyleOption::initFrom(const QWidget *widget)`

**作用与语义：**

根据指定的 `widget` 初始化 `state`、`direction`、`rect`、`palette`、`fontMetrics` 和 `styleObject` 成员变量。
这是一个方便函数;成员变量也可以手动初始化。

### `QStyleOption &QStyleOption::operator=(const QStyleOption &other)`

**作用与语义：**

把`other`分配到这个`QStyleOption`。

### `Qt::LayoutDirection QStyleOption::direction`

**作用与语义：**

该变量保留了在控件中绘制文本时应使用的文本布局方向。
默认情况下，布局方向是`Qt::LeftToRight`。

### `QFontMetrics QStyleOption::fontMetrics`

**作用与语义：**

该变量保存在控件中绘制文本时应使用字体度量。
默认情况下，使用应用程序的默认字体。

### `QPalette QStyleOption::palette`

**作用与语义：**

该变量包含绘制控件时应使用调色板。
默认情况下，应用的默认调色板被使用。

### `QRect QStyleOption::rect`

**作用与语义：**

该变量包含应用于各种计算和涂装的区域。
对于不同类型的元素，这可能有不同的含义。例如，对于`QStyle::CE_PushButton`元素，它代表整个按钮的矩形，而对于`QStyle::CE_PushButtonLabel`元素，它只是按钮标签的区域。
默认值为空矩形，即宽度和高度均为0的矩形。

### `QStyle::State QStyleOption::state`

**作用与语义：**

该变量保留绘制控件时使用的样式标志。
默认值是`QStyle::State_None`。

### `QObject *QStyleOption::styleObject`

**作用与语义：**

该变量保存被样式化的对象。
内置样式支持以下类型：`QWidget`、`QGraphicsObject`和`QQuickItem`。

### `int QStyleOption::type`

**作用与语义：**

该变量包含样式选项的期权类型。
默认值是`SO_Default`。

### `int QStyleOption::version`

**作用与语义：**

该变量保留样式选项的版本。
这个值可以被子类用来实现扩展而不破坏兼容性。如果你用`qstyleoption_cast()`函数，通常不需要检查它。
默认值是1。

### `template <typename T> T qstyleoption_cast(QStyleOption *option)`

**作用与语义：**

根据给定`option`类型返回T或T `nullptr`。

### `template <typename T> T qstyleoption_cast(const QStyleOption *option)`

**作用与语义：**

根据给定`option`的`type`和 `version`，返回 T 或 `nullptr`。

**官方示例：**

```cpp
 void MyStyle::drawPrimitive(PrimitiveElement element,
                             const QStyleOption *option,
                             QPainter *painter,
                             const QWidget *widget)
 {
     if (element == PE_FrameFocusRect) {
         const QStyleOptionFocusRect *focusRectOption =
                 qstyleoption_cast<const QStyleOptionFocusRect *>(option);
         if (focusRectOption) {
             // ...
         }
     }
     // ...
 }
```

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

`QStyleOption` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
