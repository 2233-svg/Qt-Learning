# QSizePolicy

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QSizePolicy` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QSizePolicy` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QSizePolicy>`
- 继承自：未在类页中列出
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

- `enum ControlType { DefaultType, ButtonBox, CheckBox, ComboBox, Frame, …, ToolButton }`
- `flags ControlTypes`
- `enum Policy { Fixed, Minimum, Maximum, Preferred, Expanding, …, Ignored }`
- `enum PolicyFlag { GrowFlag, ExpandFlag, ShrinkFlag, IgnoreFlag }`

### 公有函数

- `QSizePolicy()`
- `QSizePolicy(QSizePolicy::Policy horizontal, QSizePolicy::Policy vertical, QSizePolicy::ControlType type = DefaultType)`
- `QSizePolicy::ControlType controlType() const`
- `Qt::Orientations expandingDirections() const`
- `bool hasHeightForWidth() const`
- `bool hasWidthForHeight() const`
- `QSizePolicy::Policy horizontalPolicy() const`
- `int horizontalStretch() const`
- `bool retainSizeWhenHidden() const`
- `void setControlType(QSizePolicy::ControlType type)`
- `void setHeightForWidth(bool dependent)`
- `void setHorizontalPolicy(QSizePolicy::Policy policy)`
- `void setHorizontalStretch(int stretchFactor)`
- `void setRetainSizeWhenHidden(bool retainSize)`
- `void setVerticalPolicy(QSizePolicy::Policy policy)`
- `void setVerticalStretch(int stretchFactor)`
- `void setWidthForHeight(bool dependent)`
- `void transpose()`
- `QSizePolicy transposed() const`
- `QSizePolicy::Policy verticalPolicy() const`
- `int verticalStretch() const`
- `operator QVariant() const`
- `bool operator!=(const QSizePolicy &other) const`
- `bool operator==(const QSizePolicy &other) const`

### 相关非成员函数

- `size_t qHash(QSizePolicy key, size_t seed = 0)`
- `QDataStream & operator<<(QDataStream &stream, const QSizePolicy &policy)`
- `QDataStream & operator>>(QDataStream &stream, QSizePolicy &policy)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QSizePolicy::ControlTypeflags QSizePolicy::ControlTypes`

**作用与语义：**

该枚举规定了不同类型的控件在布局交互方面：
- `QSizePolicy::DefaultType`：`0x00000001`;当未指定时，默认类型。
- `QSizePolicy::ButtonBox`：`0x00000002`;一个`QDialogButtonBox`实例。
- `QSizePolicy::CheckBox`：`0x00000004`;一个`QCheckBox`实例。
- `QSizePolicy::ComboBox`：`0x00000008`;一个`QComboBox`实例。
- `QSizePolicy::Frame`：`0x00000010`;一个`QFrame`实例。
- `QSizePolicy::GroupBox`：`0x00000020`;一个`QGroupBox`实例。
- `QSizePolicy::Label`：`0x00000040`;一个`QLabel`实例。
- `QSizePolicy::Line`：`0x00000080`;`QFrame` 实例，`QFrame::HLine` 或 `QFrame::VLine`。
- `QSizePolicy::LineEdit`：`0x00000100`;一个`QLineEdit`实例。
- `QSizePolicy::PushButton`：`0x00000200`;一个`QPushButton`实例。
- `QSizePolicy::RadioButton`：`0x00000400`;一个`QRadioButton`实例。
- `QSizePolicy::Slider`：`0x00000800`;一个`QAbstractSlider`实例。
- `QSizePolicy::SpinBox`：`0x00001000`;一个`QAbstractSpinBox`实例。
- `QSizePolicy::TabWidget`：`0x00002000`;一个`QTabWidget`实例。
- `QSizePolicy::ToolButton`：`0x00004000`;一个`QToolButton`实例。
ControlTypes 类型是 QFlag 的 typedef<ControlType>。它存储 ControlType 值的 OR 组合。

### `enum QSizePolicy::Policy`

**作用与语义：**

此枚举描述了构建 `QSizePolicy` 时每个维度使用的各种尺寸类型。
- `QSizePolicy::Fixed`: `0`; `QWidget::sizeHint()` 是唯一可接受的替代方案，因此控件永远不能增长或缩小（例如按钮的垂直方向）。
- `QSizePolicy::Minimum`: `GrowFlag`; sizeHint() 是最小且足够的。控件可以扩展，但它变大没有优势（例如按钮的水平方向）。它不能小于 sizeHint() 提供的尺寸。
- `QSizePolicy::Maximum`: `ShrinkFlag`; sizeHint() 是最大值。如果其他控件需要空间，控件可以任意缩小而不会有损（例如分隔线）。它不能大于 sizeHint() 提供的尺寸。
- `QSizePolicy::Preferred`: `GrowFlag | ShrinkFlag`; sizeHint() 是最佳值，但控件可以缩小且仍然有用。控件可以扩展，但比 sizeHint() 大没有优势（默认的 `QWidget` 策略）。
- `QSizePolicy::Expanding`: `GrowFlag | ShrinkFlag | ExpandFlag`; sizeHint() 是合理尺寸，但控件可以缩小且仍然有用。控件可以利用额外空间，因此应该尽可能获得更多空间（例如水平滑块的水平方向）。
- `QSizePolicy::MinimumExpanding`: `GrowFlag | ExpandFlag`; sizeHint() 是最小且足够的。控件可以利用额外空间，因此应该尽可能获得更多空间（例如水平滑块的水平方向）。
- `QSizePolicy::Ignored`: `ShrinkFlag | GrowFlag | IgnoreFlag`; 忽略 sizeHint()。控件将获得尽可能多的空间。

### `enum QSizePolicy::PolicyFlag`

**作用与语义：**

这些标志组合起来形成各种`Policy`值：
- `QSizePolicy::GrowFlag`：`1`;如有需要，小部件可以超过其尺寸提示。
- `QSizePolicy::ExpandFlag`：`2`;小部件应尽可能多地获得空间。
- `QSizePolicy::ShrinkFlag`：`4`;如有需要，小部件可以收缩到低于提示大小。
- `QSizePolicy::IgnoreFlag`：`8`;忽略控件的大小提示。控件会尽可能多地占用空间。

### `[constexpr noexcept] QSizePolicy::QSizePolicy()`

**作用与语义：**

构建一个QSizePolicy对象，`Fixed`作为其横向和纵向策略。
策略可以通过`setHorizontalPolicy()`和`setVerticalPolicy()`函数进行修改。如果控件的首选高度取决于控件的宽度（例如带有行环绕的 `QLabel`），则使用 `setHeightForWidth()` 函数。

### `[constexpr noexcept] QSizePolicy::QSizePolicy(QSizePolicy::Policy horizontal, QSizePolicy::Policy vertical, QSizePolicy::ControlType type = DefaultType)`

**作用与语义：**

构造一个包含给定`horizontal`和`vertical`策略及指定控制`type`的QSizePolicy对象。
如果小部件的首选高度取决于小部件的宽度（例如带有行`QLabel`），则使用`setHeightForWidth()`。

### `[noexcept] QSizePolicy::ControlType QSizePolicy::controlType() const`

**作用与语义：**

返回该大小策略所适用的小部件关联的控制类型。

### `[constexpr noexcept] Qt::Orientations QSizePolicy::expandingDirections() const`

**作用与语义：**

返回一个小部件是否能利用超过`QWidget::sizeHint()`函数所显示的空间。
`Qt::Horizontal`或`Qt::Vertical`的值表示该小部件可以水平或垂直增长（即水平或垂直策略是`Expanding`或`MinimumExpanding`垂直的），而`Qt::Horizontal` |`Qt::Vertical`表示它可以在两个维度上增长。

### `[constexpr noexcept] bool QSizePolicy::hasHeightForWidth() const`

**作用与语义：**

如果小部件的首选高度取决于宽度，则返回`true`;否则返回`false`。

### `[constexpr noexcept] bool QSizePolicy::hasWidthForHeight() const`

**作用与语义：**

如果小部件的宽度依赖于高度，则返回`true`;否则返回`false`。

### `[constexpr noexcept] QSizePolicy::Policy QSizePolicy::horizontalPolicy() const`

**作用与语义：**

返回规模政策的横向部分。

### `[constexpr noexcept] int QSizePolicy::horizontalStretch() const`

**作用与语义：**

返回尺寸政策的水平拉伸因子。

### `[constexpr noexcept] bool QSizePolicy::retainSizeWhenHidden() const`

**作用与语义：**

返回布局在隐藏时是否应保持控件大小。这是默认的`false`。

### `[noexcept] void QSizePolicy::setControlType(QSizePolicy::ControlType type)`

**作用与语义：**

设置该大小策略适用于`type`的控件控件类型。
控制类型指定该大小策略适用的小部件类型。某些样式，尤其是 QMacStyle，会用它来在小部件之间插入适当的间距。例如，macOS Aqua 指南规定按钮间距应为 12 像素，而垂直堆叠的单选按钮只需 6 像素。

### `[constexpr noexcept] void QSizePolicy::setHeightForWidth(bool dependent)`

**作用与语义：**

将决定控件首选高度是否依赖于宽度的标志设置为`dependent`。

### `[constexpr noexcept] void QSizePolicy::setHorizontalPolicy(QSizePolicy::Policy policy)`

**作用与语义：**

将水平分量设置为给定的`policy`。

### `[constexpr] void QSizePolicy::setHorizontalStretch(int stretchFactor)`

**作用与语义：**

将规模策略的水平拉伸因子设定为给定`stretchFactor`。`stretchFactor`必须在[0,255]区间内。
当两个小部件在水平布局中相邻时，将左侧小部件的水平拉伸因子设为2，右边小部件的因子设为1，可以确保左边的小部件总是右边小部件的两倍大。

### `[constexpr noexcept] void QSizePolicy::setRetainSizeWhenHidden(bool retainSize)`

**作用与语义：**

设置布局在隐藏时是否应保持小部件的大小。如果`retainSize` `true`，隐藏小部件不会改变布局。

### `[constexpr noexcept] void QSizePolicy::setVerticalPolicy(QSizePolicy::Policy policy)`

**作用与语义：**

将垂直分量设置为给定的`policy`。

### `[constexpr] void QSizePolicy::setVerticalStretch(int stretchFactor)`

**作用与语义：**

将尺寸策略的垂直拉伸因子设定为给定`stretchFactor`。`stretchFactor`必须在[0,255]区间内。
当两个小部件在垂直布局中相邻时，将顶部小部件的垂直拉伸因子设为2，底部小部件的因数设为1，可以确保顶部的小部件总是底部小部件的两倍大。

### `[constexpr noexcept] void QSizePolicy::setWidthForHeight(bool dependent)`

**作用与语义：**

将判断小部件宽度是否依赖于高度的标志设置为`dependent`。
这仅支持`QGraphicsLayout`的子类。不可能同时拥有高度对宽度和宽度对高度的限制。

### `[constexpr noexcept] void QSizePolicy::transpose()`

**作用与语义：**

可以交换水平和垂直政策并拉伸。

### `[constexpr noexcept] QSizePolicy QSizePolicy::transposed() const`

**作用与语义：**

返回一个大小策略对象，水平和垂直策略互换，拉伸。

### `[constexpr noexcept] QSizePolicy::Policy QSizePolicy::verticalPolicy() const`

**作用与语义：**

返回规模策略的垂直部分。

### `[constexpr noexcept] int QSizePolicy::verticalStretch() const`

**作用与语义：**

返回尺寸保单的垂直拉伸因子。

### `QSizePolicy::operator QVariant() const`

**作用与语义：**

还回一个存放该`QSizePolicy`的 `QVariant`。

### `[constexpr noexcept] bool QSizePolicy::operator!=(const QSizePolicy &other) const`

**作用与语义：**

如果该政策与`other`不同，则退货`true`;否则退货`false`。

### `[constexpr noexcept] bool QSizePolicy::operator==(const QSizePolicy &other) const`

**作用与语义：**

如果该策略等于`other`，则`true`回报;否则返回`false`。

### `[noexcept] size_t qHash(QSizePolicy key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `QDataStream &operator<<(QDataStream &stream, const QSizePolicy &policy)`

**作用与语义：**

将数据流`policy`大小写入数据流`stream`。

### `QDataStream &operator>>(QDataStream &stream, QSizePolicy &policy)`

**作用与语义：**

读取数据流中`policy`大小`stream`。

### `enum ControlType { DefaultType, ButtonBox, CheckBox, ComboBox, Frame, …, ToolButton }`

**作用与语义：**

该枚举规定了不同类型的控件在布局交互方面：
- `QSizePolicy::DefaultType`：`0x00000001`;当未指定时，默认类型。
- `QSizePolicy::ButtonBox`：`0x00000002`;一个`QDialogButtonBox`实例。
- `QSizePolicy::CheckBox`：`0x00000004`;一个`QCheckBox`实例。
- `QSizePolicy::ComboBox`：`0x00000008`;一个`QComboBox`实例。
- `QSizePolicy::Frame`：`0x00000010`;一个`QFrame`实例。
- `QSizePolicy::GroupBox`：`0x00000020`;一个`QGroupBox`实例。
- `QSizePolicy::Label`：`0x00000040`;一个`QLabel`实例。
- `QSizePolicy::Line`：`0x00000080`;`QFrame` 实例，`QFrame::HLine` 或 `QFrame::VLine`。
- `QSizePolicy::LineEdit`：`0x00000100`;一个`QLineEdit`实例。
- `QSizePolicy::PushButton`：`0x00000200`;一个`QPushButton`实例。
- `QSizePolicy::RadioButton`：`0x00000400`;一个`QRadioButton`实例。
- `QSizePolicy::Slider`：`0x00000800`;一个`QAbstractSlider`实例。
- `QSizePolicy::SpinBox`：`0x00001000`;一个`QAbstractSpinBox`实例。
- `QSizePolicy::TabWidget`：`0x00002000`;一个`QTabWidget`实例。
- `QSizePolicy::ToolButton`：`0x00004000`;一个`QToolButton`实例。
ControlTypes 类型是 QFlag 的 typedef<ControlType>。它存储 ControlType 值的 OR 组合。

### `flags ControlTypes`

**作用与语义：**

该枚举规定了不同类型的控件在布局交互方面：
- `QSizePolicy::DefaultType`：`0x00000001`;当未指定时，默认类型。
- `QSizePolicy::ButtonBox`：`0x00000002`;一个`QDialogButtonBox`实例。
- `QSizePolicy::CheckBox`：`0x00000004`;一个`QCheckBox`实例。
- `QSizePolicy::ComboBox`：`0x00000008`;一个`QComboBox`实例。
- `QSizePolicy::Frame`：`0x00000010`;一个`QFrame`实例。
- `QSizePolicy::GroupBox`：`0x00000020`;一个`QGroupBox`实例。
- `QSizePolicy::Label`：`0x00000040`;一个`QLabel`实例。
- `QSizePolicy::Line`：`0x00000080`;`QFrame` 实例，`QFrame::HLine` 或 `QFrame::VLine`。
- `QSizePolicy::LineEdit`：`0x00000100`;一个`QLineEdit`实例。
- `QSizePolicy::PushButton`：`0x00000200`;一个`QPushButton`实例。
- `QSizePolicy::RadioButton`：`0x00000400`;一个`QRadioButton`实例。
- `QSizePolicy::Slider`：`0x00000800`;一个`QAbstractSlider`实例。
- `QSizePolicy::SpinBox`：`0x00001000`;一个`QAbstractSpinBox`实例。
- `QSizePolicy::TabWidget`：`0x00002000`;一个`QTabWidget`实例。
- `QSizePolicy::ToolButton`：`0x00004000`;一个`QToolButton`实例。
ControlTypes 类型是 QFlag 的 typedef<ControlType>。它存储 ControlType 值的 OR 组合。

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

`QSizePolicy` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
