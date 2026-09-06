# QCommonStyle

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QCommonStyle` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QCommonStyle` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QCommonStyle>`
- 继承自：QStyle
- 直接派生类：QProxyStyle

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

- `QCommonStyle()`
- `virtual ~QCommonStyle()`

### 重实现的公有函数

- `virtual void drawComplexControl(QStyle::ComplexControl cc, const QStyleOptionComplex *opt, QPainter *p, const QWidget *widget = nullptr) const override`
- `virtual void drawControl(QStyle::ControlElement element, const QStyleOption *opt, QPainter *p, const QWidget *widget = nullptr) const override`
- `virtual void drawPrimitive(QStyle::PrimitiveElement pe, const QStyleOption *opt, QPainter *p, const QWidget *widget = nullptr) const override`
- `virtual QPixmap generatedIconPixmap(QIcon::Mode iconMode, const QPixmap &pixmap, const QStyleOption *opt) const override`
- `virtual QStyle::SubControl hitTestComplexControl(QStyle::ComplexControl cc, const QStyleOptionComplex *opt, const QPoint &pt, const QWidget *widget = nullptr) const override`
- `virtual int layoutSpacing(QSizePolicy::ControlType control1, QSizePolicy::ControlType control2, Qt::Orientation orientation, const QStyleOption *option = nullptr, const QWidget *widget = nullptr) const override`
- `virtual int pixelMetric(QStyle::PixelMetric m, const QStyleOption *opt = nullptr, const QWidget *widget = nullptr) const override`
- `virtual void polish(QApplication *app) override`
- `virtual void polish(QPalette &pal) override`
- `virtual void polish(QWidget *widget) override`
- `virtual QSize sizeFromContents(QStyle::ContentsType contentsType, const QStyleOption *opt, const QSize &contentsSize, const QWidget *widget = nullptr) const override`
- `virtual QPixmap standardPixmap(QStyle::StandardPixmap sp, const QStyleOption *option = nullptr, const QWidget *widget = nullptr) const override`
- `virtual int styleHint(QStyle::StyleHint sh, const QStyleOption *opt = nullptr, const QWidget *widget = nullptr, QStyleHintReturn *hret = nullptr) const override`
- `virtual QRect subControlRect(QStyle::ComplexControl cc, const QStyleOptionComplex *opt, QStyle::SubControl sc, const QWidget *widget = nullptr) const override`
- `virtual QRect subElementRect(QStyle::SubElement sr, const QStyleOption *opt, const QWidget *widget = nullptr) const override`
- `virtual void unpolish(QApplication *application) override`
- `virtual void unpolish(QWidget *widget) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QCommonStyle::QCommonStyle()`

**作用与语义：**

构建一个QCommonStyle。

### `[virtual noexcept] QCommonStyle::~QCommonStyle()`

**作用与语义：**

毁了风格。

### `[override virtual] void QCommonStyle::drawComplexControl(QStyle::ComplexControl cc, const QStyleOptionComplex *opt, QPainter *p, const QWidget *widget = nullptr) const`

**作用与语义：**

Reimplements： `QStyle::drawComplexControl`（QStyle：：ComplexControl control， const QStyleOptionComplex *option， QPainter *painter， const QWidget *widget） const.
使用提供的`painter`并按照`option`指定的样式选项绘制给定的`control`。
`widget`论证是可选的，可以作为绘制控制的辅助工具。
`option`参数是指向`QStyleOptionComplex`对象的指针，可以用`qstyleoption_cast()`函数将其转换为正确的子类。注意，指定`option`的`rect`成员必须处于逻辑坐标中。该函数的重现应使用`visualRect()`将逻辑坐标转换为屏幕坐标，然后再调用`drawPrimitive()`或`drawControl()`函数。
下表列出了复杂的控制元素及其相关的样式选项子类。样式选项包含绘制控件所需的所有参数，包括保存绘制时使用的样式标志的`QStyleOption::state`。表格还描述了在将给定`option`铸造成相应子类时设置的标志。
- `Complex Control`：`QStyleOptionComplex`子类;风格标志;备注
- `CC_SpinBox`：`QStyleOptionSpinBox`;`State_Enabled`;如果启用自旋盒，则设置。
- `State_HasFocus`：如果旋转盒有输入焦点，则设置为。
- `CC_ComboBox`：`QStyleOptionComboBox`;`State_Enabled`;如果组合盒被启用，则设置为。
- `State_HasFocus`：如果组合盒有输入焦点，则设置。
- `CC_ScrollBar`：`QStyleOptionSlider`;`State_Enabled`;如果启用滚动条，则设置。
- `State_HasFocus`：如果滚动条有输入焦点，则设置为。
- `CC_Slider`：`QStyleOptionSlider`;`State_Enabled`;如果启用滑块，则设置。
- `State_HasFocus`：如果滑块有输入焦点，则设置为。
- `CC_Dial`：`QStyleOptionSlider`;`State_Enabled`;如果拨盘被启用，则设置为。
- `State_HasFocus`：如果转盘有输入焦点，则设置。
- `CC_ToolButton`：`QStyleOptionToolButton`;`State_Enabled`;如果工具按钮被启用，则设置为。
- `State_HasFocus`：如果工具按钮有输入焦点，则设置为。
- `State_DownArrow`：当工具键按下时设置（如按鼠标键或空格键）。
- `State_On`：如果工具按钮是切换按钮且已开启，则设置为切换。
- `State_AutoRaise`：如果工具按钮启用了自动抬起，则设置。
- `State_Raised`：当按钮未按下、未开启且启用自动抬起时不包含鼠标时，则设置为。
- `CC_TitleBar`：`QStyleOptionTitleBar`;`State_Enabled`;如果标题栏已启用，则设置。

### `[override virtual] void QCommonStyle::drawControl(QStyle::ControlElement element, const QStyleOption *opt, QPainter *p, const QWidget *widget = nullptr) const`

**作用与语义：**

Reimplements： `QStyle::drawControl`（QStyle：：ControlElement element， const QStyleOption *option， QPainter *painter， const QWidget *widget） const.
用`option`指定的样式选项，绘制给定`element`，`painter`。
`widget`参数是可选的，可以作为绘制控制项的辅助工具。`option`参数是指向`QStyleOption`对象的指针，可以用`qstyleoption_cast()`函数将其转换为正确的子类。
下表列出了控制元素及其相关的样式选项子类。样式选项包含绘制控件所需的所有参数，包括保存绘制时样式标志的 `QStyleOption::state`。表格还描述了在将指定选项投射到相应子类时设置的标志。
注意，如果这里没有列出控制元素，那是因为它使用了纯`QStyleOption`对象。
- `Control Element`：`QStyleOption`子类;风格标志;备注
- `CE_MenuItem`，`CE_MenuBarItem`：`QStyleOptionMenuItem`;`State_Selected`;菜单项目前为选中项。
- `State_Enabled`：该物品已启用。
- `State_DownArrow`：表示应绘制向下滚动的箭头。
- `State_UpArrow`：表示应绘制向上滚动箭头
- `State_HasFocus`：如果菜单栏有输入焦点，则设置。
- `CE_PushButton`、`CE_PushButtonBevel`、`CE_PushButtonLabel`：`QStyleOptionButton`;`State_Enabled`;启用按钮时设置。
- `State_HasFocus`：如果按钮有输入焦点，则设置为。
- `State_Raised`：设置为按钮未按下、未开启且未平放。
- `State_On`：如果按钮是切换按钮且已开启，则设置。
- `State_Sunken`：当按钮按下时设置（即按住鼠标或空格键）。
- `CE_RadioButton`、`CE_RadioButtonLabel`、`CE_CheckBox`、`CE_CheckBoxLabel`：`QStyleOptionButton`;`State_Enabled`;如果按钮被启用，则设置为。
- `State_HasFocus`：如果按钮有输入焦点，则设置为。
- `State_On`：如果按钮被勾选，则设置。
- `State_Off`：如果按钮未被勾选，则设置为。
- `State_NoChange`：如果按钮处于NoChange状态，则设置。
- `State_Sunken`：如果按钮按下（即鼠标或空格键被按下），则设置。
- `CE_ProgressBarContents`、`CE_ProgressBarLabel`、`CE_ProgressBarGroove`：`QStyleOptionProgressBar`;`State_Enabled`;如果进度条被启用，则设置为。
- `State_HasFocus`：如果进度条有输入焦点，则设置为。
- `CE_Header`，`CE_HeaderSection`，`CE_HeaderLabel`：`QStyleOptionHeader`
- `CE_TabBarTab`、`CE_TabBarTabShape`、`CE_TabBarTabLabel`：`QStyleOptionTab`;`State_Enabled`;如果标签栏被启用，则设置为。
- `State_Selected`：标签栏是当前选择的标签栏。
- `State_HasFocus`：如果标签栏标签页有输入焦点，则设置为。
- `CE_ToolButtonLabel`：`QStyleOptionToolButton`;`State_Enabled`;如果工具按钮被启用，则设置为。
- `State_HasFocus`：如果工具按钮有输入焦点，则设置为。
- `State_Sunken`：当工具按钮按下时设置（即按鼠标或空格键）。
- `State_On`：如果工具按钮是切换按钮并且已开启，则设置为切换。
- `State_AutoRaise`：如果工具按钮启用了自动抬起，则设置为。
- `State_MouseOver`：如果鼠标指针位于工具按钮上方，则设置。
- `State_Raised`：当按钮未按下且未开启时设置。
- `CE_ToolBoxTab`：`QStyleOptionToolBox`;`State_Selected`;标签是当前选择的标签。
- `CE_HeaderSection`：`QStyleOptionHeader`；`State_Sunken`；表示该节处于压缩状态。
- `State_UpArrow`：表示排序指示器应指向上方。
- `State_DownArrow`：表示排序指示器应指向下方。

### `[override virtual] void QCommonStyle::drawPrimitive(QStyle::PrimitiveElement pe, const QStyleOption *opt, QPainter *p, const QWidget *widget = nullptr) const`

**作用与语义：**

Reimplements： `QStyle::drawPrimitive`（QStyle：:P rimitiveElement element， const QStyleOption *option， QPainter *painter， const QWidget *widget） const.
利用`option`指定样式选项，用提供的`painter`绘制给定的原元体`element`。
`widget`参数是可选的，可能包含一个小部件，有助于绘制原元素。
下表列出了原始元素及其相关的样式选项子类。样式选项包含绘制元素所需的所有参数，包括保存绘制时使用的样式标志的`QStyleOption::state`。表格还描述了在将给定选项转换为相应子类时设置的标志。
注意，如果这里没有列出原始元素，那是因为它使用了普通`QStyleOption`对象。
- `Primitive Element`：`QStyleOption`子类;风格标志;备注
- `PE_FrameFocusRect`：`QStyleOptionFocusRect`;`State_FocusAtBorder`;焦点是在边框还是在小部件内部。
- `PE_IndicatorCheckBox`：`QStyleOptionButton`;`State_NoChange`;表示“三州”复选框。
- `State_On`：表示指示器已检查。
- `PE_IndicatorRadioButton`：`QStyleOptionButton`;`State_On`;表示选择了单选按钮。
- `State_NoChange`：表示“三态”控制器。
- `State_Enabled`：表示控制器已启用。
- `PE_IndicatorBranch`：`QStyleOption`;`State_Children`;表示应绘制扩展树以显示子项的控制。
- `State_Item`：表示应绘制一个水平分支（用于显示子项）。
- `State_Open`：表示树枝已扩展。
- `State_Sibling`：表示应绘制一条垂直线（以显示兄弟项目）。
- `PE_IndicatorHeaderArrow`：`QStyleOptionHeader`;`State_UpArrow`;表示箭头应向上拉;否则箭头应向下拉。
- `PE_FrameGroupBox`、`PE_Frame`、`PE_FrameLineEdit`、`PE_FrameMenu`、`PE_FrameDockWidget`、`PE_FrameWindow`：`QStyleOptionFrame`;`State_Sunken`;表示框架应被沉没。
- `PE_IndicatorToolBarHandle`：`QStyleOption`;`State_Horizontal`;表示窗户把手是水平的，而非垂直的。
- `PE_IndicatorSpinPlus`，`PE_IndicatorSpinMinus`，`PE_IndicatorSpinUp`，`PE_IndicatorSpinDown`，`: `QStyleOptionSpinBox`; `State_Sunken';表示按钮已被按下。
- `PE_PanelButtonCommand`：`QStyleOptionButton`;`State_Enabled`;按钮启用时设置。
- `State_HasFocus`：按钮有输入焦点时设置。
- `State_Raised`：设置按钮未按下、未开启且未平放。
- `State_On`：设置按钮为切换按钮且开启。
- `State_Sunken`：当按键按下时设置（即按住鼠标或空格键）。

### `[override virtual] QPixmap QCommonStyle::generatedIconPixmap(QIcon::Mode iconMode, const QPixmap &pixmap, const QStyleOption *opt) const`

**作用与语义：**

重实现自：`QStyle::generatedIconPixmap`（QIcon：：Mode iconMode， const QPixmap & pixmap， const QStyleOption *option） const.
返回给定`pixmap`的副本，样式符合指定`iconMode`并考虑`option`指定的调色板。
`option`参数可以传递额外信息，但必须包含调色板。
注意并非所有像素映射都符合，此时返回的像素映射是普通的副本。

### `[override virtual] QStyle::SubControl QCommonStyle::hitTestComplexControl(QStyle::ComplexControl cc, const QStyleOptionComplex *opt, const QPoint &pt, const QWidget *widget = nullptr) const`

**作用与语义：**

Reimplements： `QStyle::hitTestComplexControl`（QStyle：：ComplexControl control， const QStyleOptionComplex *option， const QPoint &position， const QWidget *widget） const.
返回给定复`control`中给定`position`的子控制（样式选项由`option`指定）。
注意`position`以屏幕坐标表示。
`option`参数是指向`QStyleOptionComplex`对象（或其子类之一）的指针。对象可以通过`qstyleoption_cast()`函数转换为相应类型。详情请参见 `drawComplexControl()`。`widget`参数是可选的，可以包含该函数的额外信息。

### `[override virtual] int QCommonStyle::layoutSpacing(QSizePolicy::ControlType control1, QSizePolicy::ControlType control2, Qt::Orientation orientation, const QStyleOption *option = nullptr, const QWidget *widget = nullptr) const`

**作用与语义：**

重实现自：`QStyle::layoutSpacing`（QSizePolicy：：ControlType control1， QSizePolicy：：ControlType control2， Qt：：Orientation orientation， const QStyleOption *option， const QWidget *widget） const.
返回布局中应使用`control1`与`control2`之间的间距。`orientation` 指定控件是并排排列还是垂直堆叠。`option`参数可用于传递关于父控件的额外信息。`widget`参数为可选，若`option` `nullptr`也可用。
该函数由布局系统调用。仅在`PM_LayoutHorizontalSpacing`或 `PM_LayoutVerticalSpacing`返回负值时使用。

### `[override virtual] int QCommonStyle::pixelMetric(QStyle::PixelMetric m, const QStyleOption *opt = nullptr, const QWidget *widget = nullptr) const`

**作用与语义：**

Reimplements： `QStyle::pixelMetric`（QStyle：:P ixelMetric metric， const QStyleOption *option， const QWidget *widget） const.
返回给定像素`metric`的值。
指定的`option`和`widget`可用于计算度量。`option`可以通过`qstyleoption_cast()`函数转换为相应类型。注意，即使是可以使用`option`的PixelMetrics，也可能为零。请参见下表，了解相应的`option`铸造：
- `Pixel Metric`：`QStyleOption` 子类
- `PM_SliderControlThickness`：`QStyleOptionSlider`
- `PM_SliderLength`：`QStyleOptionSlider`
- `PM_SliderTickmarkOffset`：`QStyleOptionSlider`
- `PM_SliderSpaceAvailable`：`QStyleOptionSlider`
- `PM_ScrollBarExtent`：`QStyleOptionSlider`
- `PM_TabBarTabOverlap`：`QStyleOptionTab`
- `PM_TabBarTabHSpace`：`QStyleOptionTab`
- `PM_TabBarTabVSpace`：`QStyleOptionTab`
- `PM_TabBarBaseHeight`：`QStyleOptionTab`
- `PM_TabBarBaseOverlap`：`QStyleOptionTab`
有些像素度量是从小部件调用的，有些则仅由样式内部调用。如果控件未调用该度量，样式作者自行决定是否使用。对于某些样式，这可能不合适。

### `[override virtual] void QCommonStyle::polish(QApplication *app)`

**作用与语义：**

重实现自：`QStyle::polish`（QApplication *应用）。
初始化给定`widget`的外观。
该函数会在每个小部件完全创建后、首次展示之前的某个时间点调用。
请注意，默认实现不做任何操作。该函数中的合理操作可能是调用控件的 QWidget：：setBackgroundMode() 函数。不要使用该函数设置，例如设置几何体。重新实现该函数提供了一个后门，可以通过它改变控件的外观，但使用 Qt 的样式引擎，很少需要实现该函数;而是重新实现 `drawItemPixmap()`、`drawItemText()`、`drawPrimitive()` 等。
`QWidget::inherits()`函数可能提供足够的信息，使得特定类别的自定义能够实现。但由于新的`QStyle`子类预计能与所有当前和未来的控件兼容，因此建议有限度地使用硬编码的自定义。

### `[override virtual] void QCommonStyle::polish(QPalette &pal)`

**作用与语义：**

重实现自：`QStyle::polish`（QPalette 和调色板）。
初始化给定`widget`的外观。
该函数会在每个小部件完全创建后、首次展示之前的某个时间点调用。
请注意，默认实现不做任何操作。该函数中合理的操作可能是调用控件的 QWidget：：setBackgroundMode() 函数。不要使用该函数设置，例如设置几何体。重新实现该函数提供了一个后门，可以通过它改变控件的外观，但使用 Qt 的样式引擎，很少需要实现该函数;而是重新实现 `drawItemPixmap()`、`drawItemText()`、`drawPrimitive()` 等。
`QWidget::inherits()`函数可能提供足够的信息，使得特定类别的自定义能够实现。但由于新的`QStyle`子类预计能与所有当前和未来的控件合理兼容，建议有限度地使用硬编码自定义。

### `[override virtual] void QCommonStyle::polish(QWidget *widget)`

**作用与语义：**

重实现自：`QStyle::polish`（QWidget *控件）。
初始化给定`widget`的外观。
该函数会在每个小部件完全创建后、首次展示之前的某个时间点调用。
请注意，默认实现不做任何操作。该函数中的合理操作可能是调用控件的 QWidget：：setBackgroundMode() 函数。不要使用该函数来设置例如几何体。重新实现该函数提供了一个后门，可以通过它改变控件的外观，但使用 Qt 的样式引擎，几乎不需要实现该函数;而是重新实现 `drawItemPixmap()`、`drawItemText()`、`drawPrimitive()` 等。
`QWidget::inherits()`函数可能提供足够的信息，支持针对类别的定制。但由于新的`QStyle`子类预计能与所有当前和未来的控件兼容，建议有限度地使用硬编码自定义。

### `[override virtual] QSize QCommonStyle::sizeFromContents(QStyle::ContentsType contentsType, const QStyleOption *opt, const QSize &contentsSize, const QWidget *widget = nullptr) const`

**作用与语义：**

重实现自：`QStyle::sizeFromContents`（QStyle：：ContentsType type， const QStyleOption *option， const QSize &contentsSize， const QWidget *widget） const.
返回由指定`option`和`type`描述的元素大小，基于提供的`contentsSize`。
`option`参数是指向`QStyleOption`或其子类之一的指针。`option`可以通过`qstyleoption_cast()`函数转换为相应类型。`widget`是可选参数，可以包含用于计算大小的额外信息。
请参见下表，了解合适的`option`铸件：
- `Contents Type`：`QStyleOption`子类
- `CT_CheckBox`：`QStyleOptionButton`
- `CT_ComboBox`：`QStyleOptionComboBox`
- `CT_GroupBox`：`QStyleOptionGroupBox`
- `CT_HeaderSection`：`QStyleOptionHeader`
- `CT_ItemViewItem`：`QStyleOptionViewItem`
- `CT_LineEdit`：`QStyleOptionFrame`
- `CT_MdiControls`：`QStyleOptionComplex`
- `CT_Menu`：`QStyleOption`
- `CT_MenuItem`：`QStyleOptionMenuItem`
- `CT_MenuBar`：`QStyleOptionMenuItem`
- `CT_MenuBarItem`：`QStyleOptionMenuItem`
- `CT_ProgressBar`：`QStyleOptionProgressBar`
- `CT_PushButton`：`QStyleOptionButton`
- `CT_RadioButton`：`QStyleOptionButton`
- `CT_ScrollBar`：`QStyleOptionSlider`
- `CT_SizeGrip`：`QStyleOption`
- `CT_Slider`：`QStyleOptionSlider`
- `CT_SpinBox`：`QStyleOptionSpinBox`
- `CT_Splitter`：`QStyleOption`
- `CT_TabBarTab`：`QStyleOptionTab`
- `CT_TabWidget`：`QStyleOptionTabWidgetFrame`
- `CT_ToolButton`：`QStyleOptionToolButton`

### `[override virtual] QPixmap QCommonStyle::standardPixmap(QStyle::StandardPixmap sp, const QStyleOption *option = nullptr, const QWidget *widget = nullptr) const`

**作用与语义：**

重实现自：`QStyle::standardPixmap`（QStyle：：StandardPixmap standardPixmap， const QStyleOption *option， const QWidget *widget） const.

### `[override virtual] int QCommonStyle::styleHint(QStyle::StyleHint sh, const QStyleOption *opt = nullptr, const QWidget *widget = nullptr, QStyleHintReturn *hret = nullptr) const`

**作用与语义：**

Reimplements： `QStyle::styleHint`（QStyle：：StyleHint hint， const QStyleOption *option， const QWidget *widget， QStyleHintReturn *returnData） const.
返回一个整数，代表指定样式`hint`，`widget`该样式由提供的样式`option`描述。
`returnData`用于查询小部件需要比 styleHint() 返回的整数更详细的数据。详情请参见 `QStyleHintReturn` 类描述。

### `[override virtual] QRect QCommonStyle::subControlRect(QStyle::ComplexControl cc, const QStyleOptionComplex *opt, QStyle::SubControl sc, const QWidget *widget = nullptr) const`

**作用与语义：**

Reimplementation s： `QStyle::subControlRect`（QStyle：：ComplexControl control， const QStyleOptionComplex *option， QStyle：：SubControl subControl， const QWidget *widget） const.
返回包含给定复`control`指定`subControl`的矩形（样式由`option`指定）。矩形定义为屏幕坐标。
`option`参数是指向`QStyleOptionComplex`或其子类之一的指针，可以使用`qstyleoption_cast()`函数转换为相应类型。详情请参见 `drawComplexControl()`。`widget`是可选的，可以包含函数的额外信息。

### `[override virtual] QRect QCommonStyle::subElementRect(QStyle::SubElement sr, const QStyleOption *opt, const QWidget *widget = nullptr) const`

**作用与语义：**

Reimplements： `QStyle::subElementRect`（QStyle：：SubElement element， const QStyleOption *option， const QWidget *widget） const.
返回给定`element`的子区域，如所提供样式`option`所述。返回的矩形定义为屏幕坐标。
`widget`参数是可选的，可用于辅助确定面积。`QStyleOption`对象可以用`qstyleoption_cast()`函数铸造为相应类型。下表了解了相应的`option`铸造：
- `Sub Element`：`QStyleOption` 子类
- `SE_PushButtonContents`：`QStyleOptionButton`
- `SE_PushButtonFocusRect`：`QStyleOptionButton`
- `SE_PushButtonBevel`：`QStyleOptionButton`
- `SE_CheckBoxIndicator`：`QStyleOptionButton`
- `SE_CheckBoxContents`：`QStyleOptionButton`
- `SE_CheckBoxFocusRect`：`QStyleOptionButton`
- `SE_RadioButtonIndicator`：`QStyleOptionButton`
- `SE_RadioButtonContents`：`QStyleOptionButton`
- `SE_RadioButtonFocusRect`：`QStyleOptionButton`
- `SE_ComboBoxFocusRect`：`QStyleOptionComboBox`
- `SE_ProgressBarGroove`：`QStyleOptionProgressBar`
- `SE_ProgressBarContents`：`QStyleOptionProgressBar`
- `SE_ProgressBarLabel`：`QStyleOptionProgressBar`

### `[override virtual] void QCommonStyle::unpolish(QApplication *application)`

**作用与语义：**

重实现自：`QStyle::unpolish`（QApplication *应用）。
取消初始化给定`widget`的外观。
该函数是`polish()`的对应功能。每当样式动态变化时，每个抛光小部件都会调用它;前者必须先恢复其设置，新样式才能再次抛光。
注意，unpolish() 只有在控件被销毁时才会被调用。这在某些情况下可能会引发问题，例如，如果你从界面中移除一个控件，缓存它，然后在样式改变后重新插入;Qt 的一些类会缓存他们的控件。

### `[override virtual] void QCommonStyle::unpolish(QWidget *widget)`

**作用与语义：**

重实现自：`QStyle::unpolish`（QWidget *控件）。
取消初始化给定`widget`的外观。
该函数是`polish()`的对应功能。每当样式动态变化时，每个抛光小部件都会调用它;前者必须先恢复设置，新样式才能再次抛光。
注意，unpolish() 只有在控件被销毁时才会被调用。这在某些情况下可能会引发问题，例如，如果你从界面中移除一个控件，缓存它，然后在样式改变后重新插入;Qt 的一些类会缓存他们的控件。

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

`QCommonStyle` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
