# QStyleOptionTab

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QStyleOptionTab` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QStyleOptionTab` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QStyleOptionTab>`
- 继承自：QStyleOption
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

### 公有类型

- `enum CornerWidget { NoCornerWidgets, LeftCornerWidget, RightCornerWidget }`
- `flags CornerWidgets`
- `enum SelectedPosition { NotAdjacent, NextIsSelected, PreviousIsSelected }`
- `enum StyleOptionType { Type }`
- `enum StyleOptionVersion { Version }`
- `enum TabFeature { None, HasFrame, MinimumSizeHint }`
- `flags TabFeatures`
- `enum TabPosition { Beginning, Middle, End, OnlyOneTab, Moving }`

### 公有函数

- `QStyleOptionTab()`
- `QStyleOptionTab(const QStyleOptionTab &other)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QStyleOptionTab::CornerWidgetflags QStyleOptionTab::CornerWidgets`

**作用与语义：**

这些标志表示标签页中的角落控件。
- `QStyleOptionTab::NoCornerWidgets`：`0x00`;没有角控件
- `QStyleOptionTab::LeftCornerWidget`：`0x01`;左角控件
- `QStyleOptionTab::RightCornerWidget`：`0x02`;右角小部件
CornerWidgets 类型是 QFlags 的 typedef<CornerWidget>。它存储 CornerWidget 值的 OR 组合。

### `enum QStyleOptionTab::SelectedPosition`

**作用与语义：**

该枚举描述了所选制表的位置。有些样式需要根据是否与所选制表相邻的不同方式绘制制表表。
- `QStyleOptionTab::NotAdjacent`：`0`;标签不邻接选中的标签（或是被选中的标签）。
- `QStyleOptionTab::NextIsSelected`：`1`;选择下一个标签（通常是右侧的标签）。
- `QStyleOptionTab::PreviousIsSelected`：`2`;选择上一个标签（通常是左侧的标签）。

### `enum QStyleOptionTab::StyleOptionType`

**作用与语义：**

该枚举用于保存样式选项类型的信息，并为每个`QStyleOption`子类定义。
- `QStyleOptionTab::Type`：`SO_Tab`;提供样式选项（`SO_Tab`为本类别）。
类型由`QStyleOption`、其子职业和`qstyleoption_cast()`内部使用，用来确定风格类型选项。一般来说，除非你想创建自己的`QStyleOption`子职业和风格，否则不必担心这些。

### `enum QStyleOptionTab::StyleOptionVersion`

**作用与语义：**

该枚举用于保存样式选项版本的信息，并为每个`QStyleOption`子类定义。
- `QStyleOptionTab::Version`：`1`;3
该版本被`QStyleOption`子类用于实现扩展而不破坏兼容性。如果你使用 `qstyleoption_cast()`，通常不需要检查。

### `enum QStyleOptionTab::TabFeatureflags QStyleOptionTab::TabFeatures`

**作用与语义：**

描述了Tab键可能具备的各种功能。
- `QStyleOptionTab::None`：`0x00`;一个普通的Tab键。
- `QStyleOptionTab::HasFrame`：`0x01`;标签键位于标签框上
- `QStyleOptionTab::MinimumSizeHint (since Qt 6.9)`：`0x02`;正在测量制表按钮的最小尺寸提示，这与其常规尺寸提示不同。
TabFeatures 类型是 QFlags 的 typedef<TabFeature>。它存储 TabFeature 值的 OR 组合。

### `enum QStyleOptionTab::TabPosition`

**作用与语义：**

这个枚举描述了制表表的位置。
- `QStyleOptionTab::Beginning`：`0`;标签是标签栏中的第一个标签。
- `QStyleOptionTab::Middle`：`1`;该制表符既不是制表栏的第一个，也不是最后一个。
- `QStyleOptionTab::End`：`2`;标签是标签栏中的最后一个标签。
- `QStyleOptionTab::OnlyOneTab`：`3`;该标签既是标签栏的第一个也是最后一个标签。
- `QStyleOptionTab::Moving (since Qt 6.6)`：`4`;标签通过鼠标拖曳或动画移动。

### `QStyleOptionTab::QStyleOptionTab()`

**作用与语义：**

构建一个 QStyleOptionTab 对象，将成员变量初始化为默认值。

### `QStyleOptionTab::QStyleOptionTab(const QStyleOptionTab &other)`

**作用与语义：**

构建`other`样式选项的副本。

### `QStyleOptionTab::CornerWidgets QStyleOptionTab::cornerWidgets`

**作用与语义：**

该变量包含一个由`CornerWidget`值组成的或组合，指示标签栏的角落控件。
默认值是`NoCornerWidgets`。

### `bool QStyleOptionTab::documentMode`

**作用与语义：**

该变量决定标签栏是否处于文档模式。
默认值为假;

### `QIcon QStyleOptionTab::icon`

**作用与语义：**

该变量保留标签的图标。
默认值为空图标，即既无像素图也无文件名的图标。

### `QSize QStyleOptionTab::iconSize`

**作用与语义：**

该变量用于确定图标的大小。
默认值为 `QSize`（-1， -1），即无效大小;使用 `QStyle::pixelMetric()` 查找标签栏的默认图标大小。

### `QSize QStyleOptionTab::leftButtonSize`

**作用与语义：**

该变量记录标签页左侧小部件的大小。
默认值为`QSize`（-1， -1），即无效大小;

### `QStyleOptionTab::TabPosition QStyleOptionTab::position`

**作用与语义：**

该变量保持标签栏中标签的位置。
默认值是`Beginning`，也就是说标签栏中的第一个标签。

### `QSize QStyleOptionTab::rightButtonSize`

**作用与语义：**

该变量用于保持标签页中正确控件的大小。
默认值为 `QSize`（-1， -1），即无效大小;

### `int QStyleOptionTab::row`

**作用与语义：**

该变量表示标签当前所在的行。
默认值为0，表示前排。目前该属性只能为0。

### `QStyleOptionTab::SelectedPosition QStyleOptionTab::selectedPosition`

**作用与语义：**

该变量保持所选标签相对于该标签的位置。
默认值为`NotAdjacent`，即标签既不邻近选中的标签，也不是所选标签。

### `QTabBar::Shape QStyleOptionTab::shape`

**作用与语义：**

该变量保留用于绘制标签的标签形状;默认`QTabBar::RoundedNorth`。

### `int QStyleOptionTab::tabIndex`

**作用与语义：**

该变量包含所表示制表表的索引。
默认值为 -1，即不在标签栏上的制表符;

### `QString QStyleOptionTab::text`

**作用与语义：**

该变量保存制表符的文本。
默认值是空字符串。

### `enum CornerWidget { NoCornerWidgets, LeftCornerWidget, RightCornerWidget }`

**作用与语义：**

这些标志表示标签页中的角落控件。
- `QStyleOptionTab::NoCornerWidgets`：`0x00`;没有角控件
- `QStyleOptionTab::LeftCornerWidget`：`0x01`;左角控件
- `QStyleOptionTab::RightCornerWidget`：`0x02`;右角小部件
CornerWidgets 类型是 QFlags 的 typedef<CornerWidget>。它存储 CornerWidget 值的 OR 组合。

### `flags CornerWidgets`

**作用与语义：**

这些标志表示标签页中的角落控件。
- `QStyleOptionTab::NoCornerWidgets`：`0x00`;没有角控件
- `QStyleOptionTab::LeftCornerWidget`：`0x01`;左角控件
- `QStyleOptionTab::RightCornerWidget`：`0x02`;右角小部件
CornerWidgets 类型是 QFlags 的 typedef<CornerWidget>。它存储 CornerWidget 值的 OR 组合。

### `enum TabFeature { None, HasFrame, MinimumSizeHint }`

**作用与语义：**

描述了Tab键可能具备的各种功能。
- `QStyleOptionTab::None`：`0x00`;一个普通的Tab键。
- `QStyleOptionTab::HasFrame`：`0x01`;标签键位于标签框上
- `QStyleOptionTab::MinimumSizeHint (since Qt 6.9)`：`0x02`;正在测量制表按钮的最小尺寸提示，这与其常规尺寸提示不同。
TabFeatures 类型是 QFlags 的 typedef<TabFeature>。它存储 TabFeature 值的 OR 组合。

### `flags TabFeatures`

**作用与语义：**

描述了Tab键可能具备的各种功能。
- `QStyleOptionTab::None`：`0x00`;一个普通的Tab键。
- `QStyleOptionTab::HasFrame`：`0x01`;标签键位于标签框上
- `QStyleOptionTab::MinimumSizeHint (since Qt 6.9)`：`0x02`;正在测量制表按钮的最小尺寸提示，这与其常规尺寸提示不同。
TabFeatures 类型是 QFlags 的 typedef<TabFeature>。它存储 TabFeature 值的 OR 组合。

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

`QStyleOptionTab` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
