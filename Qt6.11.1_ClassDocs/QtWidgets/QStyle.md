# QStyle

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QStyle` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QStyle` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QStyle>`
- 继承自：QObject
- 直接派生类：QCommonStyle

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

- `enum ComplexControl { CC_SpinBox, CC_ComboBox, CC_ScrollBar, CC_Slider, CC_ToolButton, …, CC_CustomBase }`
- `enum ContentsType { CT_CheckBox, CT_ComboBox, CT_HeaderSection, CT_LineEdit, CT_Menu, …, CT_MdiControls }`
- `enum ControlElement { CE_PushButton, CE_PushButtonBevel, CE_PushButtonLabel, CE_DockWidgetTitle, CE_Splitter, …, CE_ShapedFrame }`
- `enum PixelMetric { PM_ButtonMargin, PM_DockWidgetTitleBarButtonMargin, PM_ButtonDefaultIndicator, PM_MenuButtonIndicator, PM_ButtonShiftHorizontal, …, PM_CustomBase }`
- `enum PrimitiveElement { PE_PanelButtonCommand, PE_FrameDefaultButton, PE_PanelButtonBevel, PE_PanelButtonTool, PE_PanelLineEdit, …, PE_PanelMenu }`
- `enum RequestSoftwareInputPanel { RSIP_OnMouseClickAndAlreadyFocused, RSIP_OnMouseClick }`
- `enum StandardPixmap { SP_TitleBarMinButton, SP_TitleBarMenuButton, SP_TitleBarMaxButton, SP_TitleBarCloseButton, SP_TitleBarNormalButton, …, SP_CustomBase }`
- `flags State`
- `enum StateFlag { State_None, State_Active, State_AutoRaise, State_Children, State_DownArrow, …, State_Small }`
- `enum StyleHint { SH_EtchDisabledText, SH_DitherDisabledText, SH_ScrollBar_ContextMenu, SH_ScrollBar_MiddleClickAbsolutePosition, SH_ScrollBar_LeftClickAbsolutePosition, …, SH_Table_AlwaysDrawLeftTopGridLines }`
- `enum SubControl { SC_None, SC_ScrollBarAddLine, SC_ScrollBarSubLine, SC_ScrollBarAddPage, SC_ScrollBarSubPage, …, SC_All }`
- `flags SubControls`
- `enum SubElement { SE_PushButtonContents, SE_PushButtonFocusRect, SE_PushButtonLayoutItem, SE_PushButtonBevel, SE_CheckBoxIndicator, …, SE_ToolBarHandle }`

### 公有函数

- `QStyle()`
- `virtual ~QStyle()`
- `int combinedLayoutSpacing(QSizePolicy::ControlTypes controls1, QSizePolicy::ControlTypes controls2, Qt::Orientation orientation, QStyleOption *option = nullptr, QWidget *widget = nullptr) const`
- `virtual void drawComplexControl(QStyle::ComplexControl control, const QStyleOptionComplex *option, QPainter *painter, const QWidget *widget = nullptr) const = 0`
- `virtual void drawControl(QStyle::ControlElement element, const QStyleOption *option, QPainter *painter, const QWidget *widget = nullptr) const = 0`
- `virtual void drawItemPixmap(QPainter *painter, const QRect &rectangle, int alignment, const QPixmap &pixmap) const`
- `virtual void drawItemText(QPainter *painter, const QRect &rectangle, int alignment, const QPalette &palette, bool enabled, const QString &text, QPalette::ColorRole textRole = QPalette::NoRole) const`
- `virtual void drawPrimitive(QStyle::PrimitiveElement element, const QStyleOption *option, QPainter *painter, const QWidget *widget = nullptr) const = 0`
- `virtual QPixmap generatedIconPixmap(QIcon::Mode iconMode, const QPixmap &pixmap, const QStyleOption *option) const = 0`
- `virtual QStyle::SubControl hitTestComplexControl(QStyle::ComplexControl control, const QStyleOptionComplex *option, const QPoint &position, const QWidget *widget = nullptr) const = 0`
- `virtual QRect itemPixmapRect(const QRect &rectangle, int alignment, const QPixmap &pixmap) const`
- `virtual QRect itemTextRect(const QFontMetrics &metrics, const QRect &rectangle, int alignment, bool enabled, const QString &text) const`
- `virtual int layoutSpacing(QSizePolicy::ControlType control1, QSizePolicy::ControlType control2, Qt::Orientation orientation, const QStyleOption *option = nullptr, const QWidget *widget = nullptr) const = 0`
- `(since 6.1) QString name() const`
- `virtual int pixelMetric(QStyle::PixelMetric metric, const QStyleOption *option = nullptr, const QWidget *widget = nullptr) const = 0`
- `virtual void polish(QWidget *widget)`
- `virtual void polish(QApplication *application)`
- `virtual void polish(QPalette &palette)`
- `const QStyle * proxy() const`
- `virtual QSize sizeFromContents(QStyle::ContentsType type, const QStyleOption *option, const QSize &contentsSize, const QWidget *widget = nullptr) const = 0`
- `virtual QIcon standardIcon(QStyle::StandardPixmap standardIcon, const QStyleOption *option = nullptr, const QWidget *widget = nullptr) const = 0`
- `virtual QPalette standardPalette() const`
- `virtual int styleHint(QStyle::StyleHint hint, const QStyleOption *option = nullptr, const QWidget *widget = nullptr, QStyleHintReturn *returnData = nullptr) const = 0`
- `virtual QRect subControlRect(QStyle::ComplexControl control, const QStyleOptionComplex *option, QStyle::SubControl subControl, const QWidget *widget = nullptr) const = 0`
- `virtual QRect subElementRect(QStyle::SubElement element, const QStyleOption *option, const QWidget *widget = nullptr) const = 0`
- `virtual void unpolish(QWidget *widget)`
- `virtual void unpolish(QApplication *application)`

### 静态公有成员

- `QRect alignedRect(Qt::LayoutDirection direction, Qt::Alignment alignment, const QSize &size, const QRect &rectangle)`
- `int sliderPositionFromValue(int min, int max, int logicalValue, int span, bool upsideDown = false)`
- `int sliderValueFromPosition(int min, int max, int position, int span, bool upsideDown = false)`
- `Qt::Alignment visualAlignment(Qt::LayoutDirection direction, Qt::Alignment alignment)`
- `QPoint visualPos(Qt::LayoutDirection direction, const QRect &boundingRectangle, const QPoint &logicalPosition)`
- `QRect visualRect(Qt::LayoutDirection direction, const QRect &boundingRectangle, const QRect &logicalRectangle)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QStyle::ComplexControl`

**作用与语义：**

本枚举描述了可用的复杂控件。复杂控件的行为会根据用户点击的位置或按键的不同而有所不同。
- `QStyle::CC_SpinBox`：`0`;一个旋转盒，类似`QSpinBox`。
- `QStyle::CC_ComboBox`：`1`;一个组合盒，类似`QComboBox`。
- `QStyle::CC_ScrollBar`：`2`;一个滚动条，类似`QScrollBar`。
- `QStyle::CC_Slider`：`3`;一个滑球，像`QSlider`。
- `QStyle::CC_ToolButton`：`4`;一个工具按钮，类似`QToolButton`。
- `QStyle::CC_TitleBar`：`5`;标题栏，类似于`QMdiSubWindow`中使用的。
- `QStyle::CC_GroupBox`：`7`;一个像`QGroupBox`一样的团体盒子。
- `QStyle::CC_Dial`：`6`;一个旋钮，类似`QDial`。
- `QStyle::CC_MdiControls`：`8`;菜单栏中用于最大化MDI子窗口的最小化、关闭和普通按钮。
- `QStyle::CC_CustomBase`：`0xf0000000`;自定义复杂控制的基础值。自定义值必须大于此值。

### `enum QStyle::ContentsType`

**作用与语义：**

该枚举描述了可用的内容类型。这些类型用于计算各种控件内容的大小。
- `QStyle::CT_CheckBox`：`1`;一个复选框，类似`QCheckBox`。
- `QStyle::CT_ComboBox`：`4`;一个组合盒，类似`QComboBox`。
- `QStyle::CT_HeaderSection`：`19`;一个头部部分，类似QHeader。
- `QStyle::CT_LineEdit`：`14`;线条编辑，类似`QLineEdit`。
- `QStyle::CT_Menu`：`10`;菜单，类似`QMenu`。
- `QStyle::CT_MenuBar`：`9`;菜单栏，类似`QMenuBar`。
- `QStyle::CT_MenuBarItem`：`8`;菜单栏中的一项，类似于`QMenuBar`中的按钮。
- `QStyle::CT_MenuItem`：`7`;菜单项，类似QMenuItem。
- `QStyle::CT_ProgressBar`：`6`;进度条，类似`QProgressBar`。
- `QStyle::CT_PushButton`：`0`;一个按钮，就像`QPushButton`。
- `QStyle::CT_RadioButton`：`2`;一个单选按钮，类似`QRadioButton`。
- `QStyle::CT_SizeGrip`：`16`;握把大小，类似`QSizeGrip`。
- `QStyle::CT_Slider`：`12`;一个滑球，就像`QSlider`。
- `QStyle::CT_ScrollBar`：`13`;一个卷轴条，类似`QScrollBar`。
- `QStyle::CT_SpinBox`：`15`;一个旋转盒，类似`QSpinBox`。
- `QStyle::CT_Splitter`：`5`;一个分流器，就像`QSplitter`。
- `QStyle::CT_TabBarTab`：`11`;标签栏上的一个标签，类似于`QTabBar`。
- `QStyle::CT_TabWidget`：`17`;一个标签小部件，类似于`QTabWidget`。
- `QStyle::CT_ToolButton`：`3`;一个工具按钮，类似`QToolButton`。
- `QStyle::CT_GroupBox`：`20`;一个像`QGroupBox`一样的团体盒子。
- `QStyle::CT_ItemViewItem`：`22`;项目视图中的一个项目。
- `QStyle::CT_CustomBase`：`0xf0000000`;自定义内容类型的基础值。自定义值必须大于此值。
- `QStyle::CT_MdiControls`：`21`;菜单栏中的最小化、正常化和关闭按钮，用于最大化 MDI 子窗口。

### `enum QStyle::ControlElement`

**作用与语义：**

这个枚举代表一个控制元素。控制元素是小部件中执行某些操作或向用户显示信息的一部分。
- `QStyle::CE_PushButton`：`0`;一个`QPushButton`，抽取CE_PushButtonBevel、CE_PushButtonLabel和`PE_FrameFocusRect`。
- `QStyle::CE_PushButtonBevel`：`1`;`QPushButton`的斜面和默认指示器。
- `QStyle::CE_PushButtonLabel`：`2`;`QPushButton`的标签（带有文字或像素图的图标）。
- `QStyle::CE_DockWidgetTitle`：`30`;码头窗户标题。
- `QStyle::CE_Splitter`：`28`;分流器手柄;参见`QSplitter`。
- `QStyle::CE_CheckBox`：`3`;`QCheckBox`抽取`PE_IndicatorCheckBox`、CE_CheckBoxLabel和`PE_FrameFocusRect`。
- `QStyle::CE_CheckBoxLabel`：`4`;`QCheckBox`的标签（文本或像素图）。
- `QStyle::CE_RadioButton`：`5`;`QRadioButton`抽取`PE_IndicatorRadioButton`、CE_RadioButtonLabel和`PE_FrameFocusRect`。
- `QStyle::CE_RadioButtonLabel`：`6`;`QRadioButton`的标签（文本或像素地图）。
- `QStyle::CE_TabBarTab`：`7`;`QTabBar`中的标签和标签。
- `QStyle::CE_TabBarTabShape`：`8`;标签栏内的制表表。
- `QStyle::CE_TabBarTabLabel`：`9`;标签内的标签。
- `QStyle::CE_ProgressBar`：`10`;`QProgressBar`，抽取CE_ProgressBarGroove、CE_ProgressBarContents和CE_ProgressBarLabel。
- `QStyle::CE_ProgressBarGroove`：`11`;`QProgressBar`中绘制进度指示器的凹槽。
- `QStyle::CE_ProgressBarContents`：`12`;`QProgressBar`的进度指示器。
- `QStyle::CE_ProgressBarLabel`：`13`;`QProgressBar`的文本标签。
- `QStyle::CE_ToolButtonLabel`：`22`;工具按钮的标签。
- `QStyle::CE_MenuBarItem`：`20`;`QMenuBar`中的菜单项。
- `QStyle::CE_MenuBarEmptyArea`：`21`;`QMenuBar`的空白区域。
- `QStyle::CE_MenuItem`：`14`;`QMenu`中的菜单项。
- `QStyle::CE_MenuScroller`：`15`;当样式支持滚动时，`QMenu`中的滚动区域。
- `QStyle::CE_MenuTearoff`：`18`;代表`QMenu`撕下部分的菜单项。
- `QStyle::CE_MenuEmptyArea`：`19`;菜单中没有菜单项的区域。
- `QStyle::CE_MenuHMargin`：`17`;菜单左右侧的水平额外空格。
- `QStyle::CE_MenuVMargin`：`16`;菜单顶部/底部的垂直额外空间。
- `QStyle::CE_ToolBoxTab`：`26`;工具箱的标签和标签，位于`QToolBox`内。
- `QStyle::CE_SizeGrip`：`27`;窗口缩小手柄;参见`QSizeGrip`。
- `QStyle::CE_Header`：`23`;一个头部。
- `QStyle::CE_HeaderSection`：`24`;标题部分。
- `QStyle::CE_HeaderLabel`：`25`;头部标签。
- `QStyle::CE_ScrollBarAddLine`：`31`;滚动条线条增加指示器。（即向下滚动）;另见`QScrollBar`。
- `QStyle::CE_ScrollBarSubLine`：`32`;滚动条的行条减少指示器（即向上滚动）。
- `QStyle::CE_ScrollBarAddPage`：`33`;Scolllbar 页面递增指示器（即向下页）。
- `QStyle::CE_ScrollBarSubPage`：`34`;滚动条页面减少指示器（即翻页）。
- `QStyle::CE_ScrollBarSlider`：`35`;滚动条滑块。
- `QStyle::CE_ScrollBarFirst`：`36`;滚动条首行指示器（即主页）。
- `QStyle::CE_ScrollBarLast`：`37`;滚动条最后一行指示器（即结束）。
- `QStyle::CE_RubberBand`：`29`;例如用于图标视图的橡皮筋。
- `QStyle::CE_FocusFrame`：`38`;风格控制的焦点框。
- `QStyle::CE_ItemViewItem`：`45`;项目视图中的一个项目。
- `QStyle::CE_CustomBase`：`0xf0000000`;自定义控制元素的基础值;自定义值必须大于此值。
- `QStyle::CE_ComboBoxLabel`：`39`;不可编辑`QComboBox`的标签。
- `QStyle::CE_ToolBar`：`40`;类似`QToolBar`的工具栏。
- `QStyle::CE_ToolBoxTabShape`：`41`;工具箱的卡片形状。
- `QStyle::CE_ToolBoxTabLabel`：`42`;工具箱的标签标签。
- `QStyle::CE_HeaderEmptyArea`：`43`;标题视图中没有头部部分的区域。
- `QStyle::CE_ShapedFrame`：`46`;`QStyleOptionFrame`中指定的形状框架;参见`QFrame`。

### `enum QStyle::PixelMetric`

**作用与语义：**

该枚举描述了各种可用的像素度量。像素度量是一种样式相关的尺寸，由单个像素值表示。
- `QStyle::PM_ButtonMargin`：`0`;按钮标签与框架之间的空白量。
- `QStyle::PM_DockWidgetTitleBarButtonMargin`：`73`;码头小部件标题栏按钮标签与框架之间的空白量。
- `QStyle::PM_ButtonDefaultIndicator`：`1`;默认按钮指示框的宽度。
- `QStyle::PM_MenuButtonIndicator`：`2`;菜单按钮指示器的宽度与控件高度成正比。
- `QStyle::PM_ButtonShiftHorizontal`：`3`;按钮按下时，按钮的水平内容移动。
- `QStyle::PM_ButtonShiftVertical`：`4`;按钮按下时，按钮内容的垂直方向移动。
- `QStyle::PM_DefaultFrameWidth`：`5`;默认帧宽度（通常为2）。
- `QStyle::PM_SpinBoxFrameWidth`：`6`;自旋盒的帧宽度，默认为PM_DefaultFrameWidth。
- `QStyle::PM_ComboBoxFrameWidth`：`7`;组合盒的帧宽，默认为PM_DefaultFrameWidth。
- `QStyle::PM_MdiSubWindowFrameWidth`：`44`;MDI窗口的框架宽度。
- `QStyle::PM_MdiSubWindowMinimizedWidth`：`45`;最小化MDI窗口的宽度。
- `QStyle::PM_LayoutLeftMargin`：`75`;`QLayout`默认左边距。
- `QStyle::PM_LayoutTopMargin`：`76`;`QLayout`默认的顶端边距。
- `QStyle::PM_LayoutRightMargin`：`77`;`QLayout`的默认右边距。
- `QStyle::PM_LayoutBottomMargin`：`78`;`QLayout`的默认底部边距。
- `QStyle::PM_LayoutHorizontalSpacing`：`79`;`QLayout`的默认水平间距。
- `QStyle::PM_LayoutVerticalSpacing`：`80`;`QLayout`默认的垂直间距。
- `QStyle::PM_MaximumDragDistance`：`8`;拖动时鼠标与滚动条的最大允许距离。超过指定距离时，滑块会跳回原位;值为-1则禁用此行为。
- `QStyle::PM_ScrollBarExtent`：`9`;垂直滚动条的宽度和水平滚动条的高度。
- `QStyle::PM_ScrollBarSliderMin`：`10`;垂直滚动条滑块的最小高度和水平滚动条滑块的最小宽度。
- `QStyle::PM_SliderThickness`：`11`;滑块总厚度。
- `QStyle::PM_SliderControlThickness`：`12`;滑块手柄的厚度。
- `QStyle::PM_SliderLength`：`13`;滑块长度。
- `QStyle::PM_SliderTickmarkOffset`：`14`;刻度标记与滑块之间的偏移量。
- `QStyle::PM_SliderSpaceAvailable`：`15`;滑块可移动的可用空间。
- `QStyle::PM_DockWidgetSeparatorExtent`：`16`;水平码头窗中分隔符的宽度和垂直码头窗中分隔符的高度。
- `QStyle::PM_DockWidgetHandleExtent`：`17`;水平码头窗中手柄宽度，垂直码头窗口中手柄高度。
- `QStyle::PM_DockWidgetFrameWidth`：`18`;码头窗户的框架宽度。
- `QStyle::PM_DockWidgetTitleMargin`：`70`;码头窗标题的边缘。
- `QStyle::PM_MenuBarPanelWidth`：`33`;菜单栏的帧宽，默认为PM_DefaultFrameWidth。
- `QStyle::PM_MenuBarItemSpacing`：`34`;菜单栏条项之间的间距。
- `QStyle::PM_MenuBarHMargin`：`36`;菜单栏项与栏的左右之间的间距。
- `QStyle::PM_MenuBarVMargin`：`35`;菜单栏项与条的上下间距。
- `QStyle::PM_ToolBarFrameWidth`：`52`;工具栏周围框架宽度。
- `QStyle::PM_ToolBarHandleExtent`：`53`;水平工具栏中工具栏手柄的宽度和垂直工具栏手柄高度。
- `QStyle::PM_ToolBarItemMargin`：`55`;工具栏框架与物品之间的间距。
- `QStyle::PM_ToolBarItemSpacing`：`54`;工具栏物品之间的间距。
- `QStyle::PM_ToolBarSeparatorExtent`：`56`;水平工具栏中工具栏分隔器的宽度和垂直工具栏分隔器的高度。
- `QStyle::PM_ToolBarExtensionExtent`：`57`;水平工具栏中工具栏扩展按钮的宽度，垂直工具栏中按钮的高度。
- `QStyle::PM_TabBarTabOverlap`：`19`;标签页应重叠的像素数。（目前仅用于样式，未用于`QTabBar`内）
- `QStyle::PM_TabBarTabHSpace`：`20`;为制表宽度增加额外空间。
- `QStyle::PM_TabBarTabVSpace`：`21`;为标签高度增加额外空间。
- `QStyle::PM_TabBarBaseHeight`：`22`;标签栏与标签页之间的区域高度。
- `QStyle::PM_TabBarBaseOverlap`：`23`;标签栏与标签栏底部重叠的像素数。
- `QStyle::PM_TabBarScrollButtonWidth`：`51`
- `QStyle::PM_TabBarTabShiftHorizontal`：`49`;选中标签时水平像素偏移。
- `QStyle::PM_TabBarTabShiftVertical`：`50`;选中标签时的垂直像素偏移。
- `QStyle::PM_ProgressBarChunkWidth`：`24`;进度条指示器中块的宽度。
- `QStyle::PM_SplitterWidth`：`25`;分配器的宽度。
- `QStyle::PM_TitleBarHeight`：`26`;标题栏高度。
- `QStyle::PM_IndicatorWidth`：`37`;复选框指示器的宽度。
- `QStyle::PM_IndicatorHeight`：`38`;复选框指示器的高度。
- `QStyle::PM_ExclusiveIndicatorWidth`：`39`;单选按钮指示器的宽度。
- `QStyle::PM_ExclusiveIndicatorHeight`：`40`;单选按钮指示器的高度。
- `QStyle::PM_MenuPanelWidth`：4 `30`;`QMenu`的边框宽度（适用于所有边）。
- `QStyle::PM_MenuHMargin`：`28`;`QMenu`的额外边框（用于左右）。
- `QStyle::PM_MenuVMargin`：`29`;`QMenu`的额外边框（用于底部和顶部）。
- `QStyle::PM_MenuScrollerHeight`：`27`;`QMenu`中滚动区域的高度。
- `QStyle::PM_MenuTearoffHeight`：`31`;`QMenu`中撕下区域的高度。
- `QStyle::PM_MenuDesktopFrameWidth`：`32`;桌面菜单的框架宽度。
- `QStyle::PM_HeaderMarkSize`：`47`;头部中排序指示器的大小。
- `QStyle::PM_HeaderGripMargin`：`48`;头部中调整握把的尺寸。
- `QStyle::PM_HeaderMargin`：`46`;排序指示器与文本之间的边距大小。
- `QStyle::PM_SpinBoxSliderHeight`：`58`;可选旋转盒滑块的高度。
- `QStyle::PM_ToolBarIconSize`：`59`;默认工具栏图标大小
- `QStyle::PM_SmallIconSize`：`62`;默认小图标大小
- `QStyle::PM_LargeIconSize`：`63`;默认大图标大小
- `QStyle::PM_FocusFrameHMargin`：`65`;焦点框将比控件更突出的水平边距。
- `QStyle::PM_FocusFrameVMargin`：`64`;焦点框将比小部件高出的垂直边距。
- `QStyle::PM_IconViewIconSize`：`61`;图标视图中图标的默认大小。
- `QStyle::PM_ListViewIconSize`：`60`;列表视图中图标的默认大小。
- `QStyle::PM_ToolTipLabelFrameWidth`：`66`;工具提示标签的框架宽度。
- `QStyle::PM_CheckBoxLabelSpacing`：`67`;复选框指示器与标签之间的间距。
- `QStyle::PM_RadioButtonLabelSpacing`：`74`;指无线电按钮指示器与标签之间的间距。
- `QStyle::PM_TabBarIconSize`：`68`;标签栏的默认图标大小。
- `QStyle::PM_SizeGripSize`：`69`;握把尺寸的大小。
- `QStyle::PM_MessageBoxIconSize`：`71`;消息框中标准图标的大小
- `QStyle::PM_ButtonIconSize`：`72`;按钮图标的默认大小
- `QStyle::PM_TextCursorWidth`：`82`;行编辑或文本编辑中光标的宽度
- `QStyle::PM_TabBar_ScrollButtonOverlap`：`81`;标签栏中左右按钮之间的距离。
- `QStyle::PM_TabCloseIndicatorWidth`：`83`;标签栏中关闭按钮的默认宽度。
- `QStyle::PM_TabCloseIndicatorHeight`：`84`;标签栏中关闭按钮的默认高度。
- `QStyle::PM_ScrollView_ScrollBarSpacing`：`85`;设置`SH_ScrollView_FrameOnlyAroundContents`时，帧与滚动条之间的距离。
- `QStyle::PM_ScrollView_ScrollBarOverlap`：`86`;滚动条与滚动内容的重叠
- `QStyle::PM_SubMenuOverlap`：`87`;子菜单与其父菜单之间的水平重叠。
- `QStyle::PM_TreeViewIndentation (since Qt 5.4)`：`88`;树状视图中项目的缩进。
- `QStyle::PM_HeaderDefaultSectionSizeHorizontal`：`89`;水平头部中部分的默认大小。该枚举值在Qt 5.5中引入。
- `QStyle::PM_HeaderDefaultSectionSizeVertical`：`90`;垂直头部中部分的默认大小。该枚举值在Qt 5.5中引入。
- `QStyle::PM_TitleBarButtonIconSize (since Qt 5.8)`：`91`;标题栏按钮图标的大小。
- `QStyle::PM_TitleBarButtonSize (since Qt 5.8)`：`92`;标题栏按钮的大小。
- `QStyle::PM_LineEditIconSize (since Qt 6.2)`：`93`;行编辑中图标的默认大小。
- `QStyle::PM_LineEditIconMargin (since Qt 6.3)`：`94`;线编辑中图标周围的边距。
- `QStyle::PM_CustomBase`：`0xf0000000`;自定义像素指标的基础值。自定义值必须大于此值。

### `enum QStyle::PrimitiveElement`

**作用与语义：**

该枚举描述了各种原始元素。原始元素是常见的图形用户界面元素，如复选框指示器或按钮倒角。
- `QStyle::PE_PanelButtonCommand`：`13`;用于发起动作的按钮，例如，`QPushButton`。
- `QStyle::PE_FrameDefaultButton`：`1`;该框架围绕默认按钮，例如对话框中。
- `QStyle::PE_PanelButtonBevel`：`14`;带有按钮斜面的通用面板。
- `QStyle::PE_PanelButtonTool`：`15`;工具按钮面板，配合`QToolButton`使用。
- `QStyle::PE_PanelLineEdit`：`18`;`QLineEdit`面板。
- `QStyle::PE_IndicatorButtonDropDown`：`24`;下拉按钮的指示器，例如显示菜单的工具按钮。
- `QStyle::PE_FrameFocusRect`：`3`;通用对焦指示器。
- `QStyle::PE_IndicatorArrowUp`：`22`;通用向上箭头。
- `QStyle::PE_IndicatorArrowDown`：`19`;通用下箭头。
- `QStyle::PE_IndicatorArrowRight`：`21`;通用右箭头。
- `QStyle::PE_IndicatorArrowLeft`：`20`;通用左箭头。
- `QStyle::PE_IndicatorSpinUp`：`35`;旋转控件（例如`QSpinBox`）的上升符号。
- `QStyle::PE_IndicatorSpinDown`：`32`;旋转小工具的向下符号。
- `QStyle::PE_IndicatorSpinPlus`：`34`;增加旋转控件的符号。
- `QStyle::PE_IndicatorSpinMinus`：`33`;旋转小部件的减小符号。
- `QStyle::PE_IndicatorItemViewItemCheck`：`25`;用于查看项的开关指示器。
- `QStyle::PE_IndicatorCheckBox`：`26`;开关指示器，例如`QCheckBox`。
- `QStyle::PE_IndicatorRadioButton`：`31`;独占开关指示器，例如`QRadioButton`。
- `QStyle::PE_IndicatorDockWidgetResizeHandle`：`27`;底座窗户手柄大小调整。
- `QStyle::PE_Frame`：`0`;通用框架
- `QStyle::PE_FrameMenu`：`6`;弹出窗口/菜单的框架;参见`QMenu`。
- `QStyle::PE_PanelMenuBar`：`16`;菜单栏面板。
- `QStyle::PE_PanelScrollAreaCorner`：`40`;卷轴区域右下角（或左下角）的面板。
- `QStyle::PE_FrameDockWidget`：`2`;用于底座窗口和工具栏的面板框架。
- `QStyle::PE_FrameTabWidget`：`8`;用于制表小部件的框架。
- `QStyle::PE_FrameLineEdit`：`5`;用于行编辑的面板框架。
- `QStyle::PE_FrameGroupBox`：`4`;分组盒子周围的面板框架。
- `QStyle::PE_FrameButtonBevel`：`10`;用于按键斜角的面板框架。
- `QStyle::PE_FrameButtonTool`：`11`;用于工具按钮的面板框架。
- `QStyle::PE_IndicatorHeaderArrow`：`28`;用于表示列表或表头的排序方向的箭头。
- `QStyle::PE_FrameStatusBarItem`：`7`;状态栏中的物品框架;另见`QStatusBar`。
- `QStyle::PE_FrameWindow`：`9`;围绕MDI窗口或对接窗口框架。
- `QStyle::PE_IndicatorMenuCheckMark`：`29`;菜单中使用的勾选标记。
- `QStyle::PE_IndicatorProgressChunk`：`30`;进度条指示器的部分;另见`QProgressBar`。
- `QStyle::PE_IndicatorBranch`：`23`;用于表示树状视图中树枝的线条。
- `QStyle::PE_IndicatorToolBarHandle`：`36`;工具栏的把手。
- `QStyle::PE_IndicatorToolBarSeparator`：`37`;工具栏中的分隔器。
- `QStyle::PE_PanelToolBar`：`17`;工具栏面板。
- `QStyle::PE_PanelTipLabel`：`38`;小费标签面板。
- `QStyle::PE_FrameTabBarBase`：`12`;为制表列绘制的框架，通常为非制表控件的制表列绘制。
- `QStyle::PE_IndicatorTabTear`：`39`;已弃用。改用PE_IndicatorTabTearLeft。
- `QStyle::PE_IndicatorTabTearLeft`：`PE_IndicatorTabTear`;当有多个标签时，表示可见标签栏左侧的标签部分被滚动出去。
- `QStyle::PE_IndicatorTabTearRight`：`49`;当有许多标签时，表示可见标签栏右侧的标签部分滚动。
- `QStyle::PE_IndicatorColumnViewArrow`：`42`;`QColumnView`中的箭。
- `QStyle::PE_Widget`：`41`;一个普通`QWidget`。
- `QStyle::PE_CustomBase`：`0xf000000`;自定义原元素的基础值。所有高于此值的值保留用于自定义使用。自定义值必须大于此值。
- `QStyle::PE_IndicatorItemViewItemDrop`：`43`;一个指示器，用于显示在物品视图中拖放操作中，物品即将被投放的位置。
- `QStyle::PE_PanelItemViewItem`：`44`;物品视图中的物品背景。
- `QStyle::PE_PanelItemViewRow`：`45`;在项目视图中，行的背景。
- `QStyle::PE_PanelStatusBar`：`46`;状态栏面板。
- `QStyle::PE_IndicatorTabClose`：`47`;标签栏上的关闭按钮。
- `QStyle::PE_PanelMenu`：`48`;菜单面板。

### `enum QStyle::RequestSoftwareInputPanel`

**作用与语义：**

该枚举描述了在何种情况下，支持输入的小部件会请求软件输入面板。
- `QStyle::RSIP_OnMouseClickAndAlreadyFocused`：`0`;用户点击小部件时请求输入面板，但前提是控件已被聚焦。
- `QStyle::RSIP_OnMouseClick`：`1`;如果用户点击小部件，则请求输入面板。

### `enum QStyle::StandardPixmap`

**作用与语义：**

本枚举描述了可用的标准像素地图。标准像素地图是指可以遵循某些现有图形界面风格或指南的像素地图。
- `QStyle::SP_TitleBarMinButton`：`1`;标题栏上的最小化按钮（例如，`QMdiSubWindow`中）。
- `QStyle::SP_TitleBarMenuButton`：`0`;标题栏上的菜单按钮。
- `QStyle::SP_TitleBarMaxButton`：`2`;标题栏上的最大化按钮。
- `QStyle::SP_TitleBarCloseButton`：`3`;标题栏上的关闭按钮。
- `QStyle::SP_TitleBarNormalButton`：`4`;标题栏上的普通（恢复）按钮。
- `QStyle::SP_TitleBarShadeButton`：`5`;标题栏上的阴影按钮。
- `QStyle::SP_TitleBarUnshadeButton`：`6`;标题栏上的“解除着色”按钮。
- `QStyle::SP_TitleBarContextHelpButton`：`7`;标题栏上的上下文帮助按钮。
- `QStyle::SP_MessageBoxInformation`：`9`;“信息”图标。
- `QStyle::SP_MessageBoxWarning`：`10`;“警告”图标。
- `QStyle::SP_MessageBoxCritical`：`11`;“关键”图标。
- `QStyle::SP_MessageBoxQuestion`：`12`;“问题”图标。
- `QStyle::SP_DesktopIcon`：`13`;“桌面”图标。
- `QStyle::SP_TrashIcon`：`14`;“垃圾”图标。
- `QStyle::SP_ComputerIcon`：`15`;“我的电脑”图标。
- `QStyle::SP_DriveFDIcon`：`16`;软盘图标。
- `QStyle::SP_DriveHDIcon`：`17`;硬盘图标。
- `QStyle::SP_DriveCDIcon`：`18`;CD图标。
- `QStyle::SP_DriveDVDIcon`：`19`;DVD图标。
- `QStyle::SP_DriveNetIcon`：`20`;网络图标。
- `QStyle::SP_DirHomeIcon`：`56`;家庭目录图标。
- `QStyle::SP_DirOpenIcon`：`21`;开放目录图标。
- `QStyle::SP_DirClosedIcon`：`22`;封闭目录图标。
- `QStyle::SP_DirIcon`：`38`;目录图标。
- `QStyle::SP_DirLinkIcon`：`23`;目录图标的链接。
- `QStyle::SP_DirLinkOpenIcon`：`24`;指向打开目录图标的链接。
- `QStyle::SP_FileIcon`：`25`;文件图标。
- `QStyle::SP_FileLinkIcon`：`26`;文件链接图标。
- `QStyle::SP_FileDialogStart`：`29`;文件对话框中的“开始”图标。
- `QStyle::SP_FileDialogEnd`：`30`;文件对话框中的“结束”图标。
- `QStyle::SP_FileDialogToParent`：`31`;文件对话框中的“父目录”图标。
- `QStyle::SP_FileDialogNewFolder`：`32`;文件对话框中的“创建新文件夹”图标。
- `QStyle::SP_FileDialogDetailedView`：`33`;文件对话框中的详细视图图标。
- `QStyle::SP_FileDialogInfoView`：`34`;文件对话框中的文件信息图标。
- `QStyle::SP_FileDialogContentsView`：`35`;文件对话框中的目录视图图标。
- `QStyle::SP_FileDialogListView`：`36`;文件对话框中的列表视图图标。
- `QStyle::SP_FileDialogBack`：`37`;文件对话框中的返回箭头。
- `QStyle::SP_DockWidgetCloseButton`：`8`;停靠台窗口的关闭按钮（另见`QDockWidget`）。
- `QStyle::SP_ToolBarHorizontalExtensionButton`：`27`;用于水平工具栏的扩展按钮。
- `QStyle::SP_ToolBarVerticalExtensionButton`：`28`;垂直工具栏的扩展按钮。
- `QStyle::SP_DialogOkButton`：`39`;`QDialogButtonBox`中标准确定按钮的图标。
- `QStyle::SP_DialogCancelButton`：`40`;`QDialogButtonBox`中标准取消按钮的图标。
- `QStyle::SP_DialogHelpButton`：`41`;`QDialogButtonBox`中标准帮助按钮的图标。
- `QStyle::SP_DialogOpenButton`：`42`;`QDialogButtonBox`中标准的打开按钮图标。
- `QStyle::SP_DialogSaveButton`：`43`;`QDialogButtonBox`中标准保存按钮的图标。
- `QStyle::SP_DialogCloseButton`：`44`;`QDialogButtonBox`中标准关闭按钮的图标。
- `QStyle::SP_DialogApplyButton`：`45`;`QDialogButtonBox`中标准应用按钮的图标。
- `QStyle::SP_DialogResetButton`：`46`;`QDialogButtonBox`中标准重置按钮的图标。
- `QStyle::SP_DialogDiscardButton`：`47`;`QDialogButtonBox`中标准弃牌按钮的图标。
- `QStyle::SP_DialogYesButton`：`48`;`QDialogButtonBox`中标准“是”按钮的图标。
- `QStyle::SP_DialogNoButton`：`49`;`QDialogButtonBox`中标准“否”按钮的图标。
- `QStyle::SP_ArrowUp`：`50`;图标箭头指向上方。
- `QStyle::SP_ArrowDown`：`51`;图标箭头指向下方。
- `QStyle::SP_ArrowLeft`：`52`;图标箭头指向左侧。
- `QStyle::SP_ArrowRight`：`53`;图标箭头指向右侧。
- `QStyle::SP_ArrowBack`：`54`;当当前布局方向为`Qt::LeftToRight`时，相当于SP_ArrowLeft，否则SP_ArrowRight。
- `QStyle::SP_ArrowForward`：`55`;当当前布局方向`Qt::LeftToRight`时，相当于SP_ArrowRight，否则SP_ArrowLeft。
- `QStyle::SP_CommandLink`：`57`;用于表示Vista风格命令链接字形的图标。
- `QStyle::SP_VistaShield`：`58`;用于表示 Windows Vista 上 UAC 提示的图标。在所有其他平台上，这会返回空像素地图或图标。
- `QStyle::SP_BrowserReload`：`59`;表示当前页面应重新加载的图标。
- `QStyle::SP_BrowserStop`：`60`;表示页面加载应停止的图标。
- `QStyle::SP_MediaPlay`：`61`;图标表示媒体应开始播放。
- `QStyle::SP_MediaStop`：`62`;表示媒体应停止播放的图标。
- `QStyle::SP_MediaPause`：`63`;表示媒体应暂停播放的图标。
- `QStyle::SP_MediaSkipForward`：`64`;图标表示媒体应跳过。
- `QStyle::SP_MediaSkipBackward`：`65`;图标表示媒体应向后跳。
- `QStyle::SP_MediaSeekForward`：`66`;图标表示媒体应向前推进。
- `QStyle::SP_MediaSeekBackward`：`67`;图标表示媒体应向后寻求。
- `QStyle::SP_MediaVolume`：`68`;表示音量控制的图标。
- `QStyle::SP_MediaVolumeMuted`：`69`;表示音量控制静音的图标。
- `QStyle::SP_LineEditClearButton (since Qt 5.2)`：`70`;`QLineEdit`中标准清除按钮的图标。
- `QStyle::SP_DialogYesToAllButton (since Qt 5.14)`：`71`;`QDialogButtonBox`中标准YesToAll按钮的图标。
- `QStyle::SP_DialogNoToAllButton (since Qt 5.14)`：`72`;`QDialogButtonBox`中标准 NoToAll 按钮的图标。
- `QStyle::SP_DialogSaveAllButton (since Qt 5.14)`：`73`;`QDialogButtonBox`中标准的“全部保存”按钮图标。
- `QStyle::SP_DialogAbortButton (since Qt 5.14)`：`74`;`QDialogButtonBox`中标准中止按钮的图标。
- `QStyle::SP_DialogRetryButton (since Qt 5.14)`：`75`;`QDialogButtonBox`中标准重试按钮的图标。
- `QStyle::SP_DialogIgnoreButton (since Qt 5.14)`：`76`;`QDialogButtonBox`中标准忽略按钮的图标。
- `QStyle::SP_RestoreDefaultsButton (since Qt 5.14)`：`77`;`QDialogButtonBox`中标准的恢复默认按钮图标。
- `QStyle::SP_TabCloseButton (since Qt 6.3)`：`78`;`QTabBar`标签页中的关闭按钮图标。
- `QStyle::SP_CustomBase`：`0xf0000000`;自定义标准像素图的基础值;自定义值必须大于此值。

### `enum QStyle::StateFlagflags QStyle::State`

**作用与语义：**

该枚举描述了绘制原始元素时使用的标志。
注意，并非所有原语都使用所有这些标志，而且这些标志对不同物品的含义可能不同。
- `QStyle::State_None`：`0x00000000`;表示该小部件没有状态。
- `QStyle::State_Active`：`0x00010000`;表示该小部件处于激活状态。
- `QStyle::State_AutoRaise`：`0x00001000`;用于指示工具按钮是否应使用自动抬高外观。
- `QStyle::State_Children`：`0x00080000`;用于表示项目视图分支是否有子节点。
- `QStyle::State_DownArrow`：`0x00000040`;用于指示小部件上是否应显示下箭头。
- `QStyle::State_Editing`：`0x00400000`;已弃用。不再使用，因为编辑器被绘制在物品视图单元格上。
- `QStyle::State_Enabled`：`0x00000001`;用于表示小部件是否被启用。
- `QStyle::State_HasEditFocus`：`0x01000000`;用于表示小部件当前是否具有编辑焦点。
- `QStyle::State_HasFocus`：`0x00000100`;用于表示小部件是否有焦点。
- `QStyle::State_Horizontal`：`0x00000080`;用于表示小部件是否水平布局，例如。工具栏。
- `QStyle::State_KeyboardFocusChange`：`0x00800000`;用于表示是否通过键盘更改了焦点，例如Tab、BackTab或快捷键。
- `QStyle::State_MouseOver`：`0x00002000`;用于表示小部件是否位于鼠标下方。
- `QStyle::State_NoChange`：`0x00000010`;用于表示三州复选框。
- `QStyle::State_Off`：`0x00000008`;用于表示小部件未被检查。
- `QStyle::State_On`：`0x00000020`;用于表示控件是否被检查。
- `QStyle::State_Raised`：`0x00000002`;用于表示按钮是否被抬起。
- `QStyle::State_ReadOnly`：`0x02000000`;用于表示小部件是否为只读。
- `QStyle::State_Selected`：`0x00008000`;用于表示是否选中了某个小部件。
- `QStyle::State_Item`：`0x00100000`;用于项目视图，指示是否应绘制水平分支。
- `QStyle::State_Open`：`0x00040000`;用于项目视图，表示树枝是否开放。
- `QStyle::State_Sibling`：`0x00200000`;用于项目视图，表示是否需要绘制垂直线（对于兄弟姐妹）。
- `QStyle::State_Sunken`：`0x00000004`;用于表示小部件是否被按下或沉入。
- `QStyle::State_UpArrow`：`0x00004000`;用于指示小部件上是否应显示上箭头。
- `QStyle::State_Mini`：`0x08000000`;用于表示迷你风格的Mac小部件或按钮。
- `QStyle::State_Small`：`0x04000000`;用于表示小型风格的 Mac 小部件或按钮。
状态类型是QFlag的typedef<StateFlag>。它存储StateFlag值的OR组合。

### `enum QStyle::StyleHint`

**作用与语义：**

本枚举描述了可用的风格提示。风格提示是一种通用的外观和/或感觉提示。
- `QStyle::SH_EtchDisabledText`：`0`;禁用的文本会像Windows一样“蚀刻”。
- `QStyle::SH_DitherDisabledText`：`1`;禁用文本与Motif版本相同抖动。
- `QStyle::SH_ScrollBar_ContextMenu`：`62`;滚动条是否带有上下文菜单。
- `QStyle::SH_ScrollBar_MiddleClickAbsolutePosition`：`2`;一个布尔值。如果为真，中键点击滚动条会使滑块跳到该位置。如果为假，中键点击被忽略。
- `QStyle::SH_ScrollBar_LeftClickAbsolutePosition`：`39`;一个布尔值。如果为真，左键点击滚动条会使滑块跳到该位置。如果为假，左键点击将根据每个控制项的行为调整。
- `QStyle::SH_ScrollBar_ScrollWhenPointerLeavesControl`：`3`;一个布尔值。如果为真，当点击滚动条`SubControl`，按住鼠标按钮并将指针移出`SubControl`时，滚动条会继续滚动。如果为假，当指针离开`SubControl`时，滑动条停止滚动。
- `QStyle::SH_ScrollBar_RollBetweenButtons`：`63`;一个布尔值。如果为真，点击滚动条按钮（`SC_ScrollBarAddLine`或`SC_ScrollBarSubLine`）并拖动到对面按钮（滚动）时，会按下新按钮并松开旧按钮。当错误时，原按钮会松开，但没有任何反应（类似按键）。
- `QStyle::SH_TabBar_Alignment`：`5`;`QTabWidget`中制表符的对齐。可能的值有`Qt::AlignLeft`、`Qt::AlignCenter`和`Qt::AlignRight`。
- `QStyle::SH_Header_ArrowAlignment`：`6`;排序指示器的位置可能出现在列表或表头部。可能的值是`Qt::Alignment`值（即`Qt::AlignmentFlag`标志的或组合）。
- `QStyle::SH_Slider_SnapToValue`：`7`;滑块在移动时会自动吸附到数值，就像Windows上一样。
- `QStyle::SH_Slider_SloppyKeyEvents`：`8`;按键操作不够松散，即在垂直滑块上左转时会减去一行。
- `QStyle::SH_ProgressDialog_CenterCancelButton`：`9`;进度对话框的中心按钮，其他位置为右键。
- `QStyle::SH_ProgressDialog_TextLabelAlignment`：`10`;进行中对话框中文本标签的对齐;Windows上`Qt::AlignCenter`，`Qt::AlignVCenter`其他方式。
- `QStyle::SH_PrintDialog_RightAlignButtons`：`11`;在打印对话框中右对齐按钮，类似Windows操作。
- `QStyle::SH_MainWindow_SpaceBelowMenuBar`：`12`;菜单栏与 Dock 区域之间有一到两个像素空间，类似 Windows 版本。
- `QStyle::SH_FontDialog_SelectAssociatedText`：`13`;在行编辑中选择文本，或在从列表框中选择项目时，或在行编辑获得焦点时（如Windows版本）选择文本。
- `QStyle::SH_Menu_KeyboardSearch`：`66`;输入时会在菜单中搜索相关项目，否则仅考虑助记法。
- `QStyle::SH_Menu_AllowActiveAndDisabled`：`14`;允许禁用菜单项激活。
- `QStyle::SH_Menu_SpaceActivatesItem`：`15`;按下空格键即可激活该物品，就像Motif的操作一样。
- `QStyle::SH_Menu_SubMenuPopupDelay`：`16`;在打开子菜单前等待的毫秒数（Windows 为 256，Motif 为 96）。
- `QStyle::SH_Menu_Scrollable`：`30`;弹出菜单是否必须支持滚动。
- `QStyle::SH_Menu_SloppySubMenus`：`33`;弹出菜单是否必须支持用户在跨越菜单其他项时将鼠标光标移动到子菜单。大多数现代桌面平台支持此功能。
- `QStyle::SH_Menu_SubMenuUniDirection`：`105`;自Qt 5.5起。如果光标必须朝子菜单移动（像macOS那样），或者只要在超时前到达子菜单，光标就可以任意移动。
- `QStyle::SH_Menu_SubMenuUniDirectionFailCount`：`106`;自第5.5个Q开始。当定义SH_Menu_SubMenuUniDirection时，该枚举定义了在丢弃粗糙子菜单前失败的鼠标移动次数。这可以用来控制单方向算法的“严格性”。
- `QStyle::SH_Menu_SubMenuSloppySelectOtherActions`：`107`;自第5.5个Q开始。当鼠标移动到一个杂乱的子菜单时，是否应该选择其他动作项？
- `QStyle::SH_Menu_SubMenuSloppyCloseTimeout`：`108`;自第5.5个Q起。超时过去用来关闭粗糙的子菜单。
- `QStyle::SH_Menu_SubMenuResetWhenReenteringParent`：`109`;自第5.5个Q开始。当从子子菜单进入父菜单时，是否应该重置马虎状态，从而实际上关闭子菜单并使当前子菜单处于激活状态？
- `QStyle::SH_Menu_SubMenuDontStartSloppyOnLeave`：`110`;自第5.5学期起。鼠标离开子菜单时不要启动马虎计时器。
- `QStyle::SH_ScrollView_FrameOnlyAroundContents`：`17`;滚动视图是仅围绕内容绘制框架（如Motif），还是围绕内容、滚动条和角落控件绘制（如Windows）。
- `QStyle::SH_MenuBar_AltKeyNavigation`：`18`;菜单栏的项目可按Alt键导航，然后用方向键选择所需项目。
- `QStyle::SH_ComboBox_ListMouseTracking_Current`：`SH_ComboBox_ListMouseTracking`;鼠标追踪组合框下拉菜单中，光标下方的项被指定为当前项（`QStyle::State_Selected`）。
- `QStyle::SH_ComboBox_ListMouseTracking`：`19`;已弃用。改用SH_ComboBox_ListMouseTracking_Current。
- `QStyle::SH_ComboBox_ListMouseTracking_Active`：`120`;鼠标追踪组合框下拉列表，光标下方的物品不会变成当前物品，而是激活（`QStyle::State_MouseOver`）。
- `QStyle::SH_Menu_MouseTracking`：`20`;弹出菜单中的鼠标追踪功能。
- `QStyle::SH_MenuBar_MouseTracking`：`21`;菜单栏中的鼠标追踪。
- `QStyle::SH_Menu_FillScreenWithScroll`：`45`;滚动弹窗是否应在滚动时填满屏幕。
- `QStyle::SH_Menu_SelectionWrap`：`73`;弹出窗口是否应允许选择进行包裹，即选择是否应为第一个选项。
- `QStyle::SH_ItemView_ChangeHighlightOnFocus`：`22`;失去焦点时选定物品变灰。
- `QStyle::SH_Widget_ShareActivation`：`23`;启用与浮动无模式对话框的共享激活。
- `QStyle::SH_TabBar_SelectMouseType`：`4`;哪种类型的鼠标事件应导致选择标签页。
- `QStyle::SH_ListViewExpand_SelectMouseType`：`40`;选择列表视图扩展的鼠标类型事件。
- `QStyle::SH_TabBar_PreferNoArrows`：`38`;标签栏是否应建议尺寸以防止滚动箭头。
- `QStyle::SH_ComboBox_Popup`：`25`;支持组合框下拉菜单弹出。
- `QStyle::SH_Workspace_FillSpaceOnMaximize`：`24`;工作区应最大化客户区域。
- `QStyle::SH_TitleBar_NoBorder`：`26`;标题栏没有边框。
- `QStyle::SH_Slider_StopMouseOverSlider`：`27`;滑块到达鼠标位置时停止自动重复。
- `QStyle::SH_BlinkCursorWhenTextSelected`：`28`;选择文本时光标是否应该闪烁。
- `QStyle::SH_RichText_FullWidthSelection`：`29`;富文本选择是否应扩展至文档的全宽。
- `QStyle::SH_GroupBox_TextLabelVerticalAlignment`：`31`;如何垂直对齐分组框的文本标签。
- `QStyle::SH_GroupBox_TextLabelColor`：`32`;如何绘制组框的文本标签。
- `QStyle::SH_DialogButtons_DefaultButton`：`36`;哪个按钮在对话框的按钮控件中获得默认状态。
- `QStyle::SH_ToolBox_SelectedPageTitleBold`：`37`;`QToolBox`中所选页面标题的粗体度。
- `QStyle::SH_LineEdit_PasswordCharacter`：`35`;用于密码的Unicode字符。
- `QStyle::SH_LineEdit_PasswordMaskDelay`：`103`;确定可见字符被密码字符遮罩前的延迟，单位为毫秒。该枚举值在Qt 5.4中添加。
- `QStyle::SH_Table_GridLineColor`：`34`;表的网格RGBA值。
- `QStyle::SH_UnderlineShortcut`：`41`;是否会有下划线。
- `QStyle::SH_SpinBox_AnimateButton`：`42`;在旋转框中按下上或下时，动画中点击。
- `QStyle::SH_SpinBox_KeyPressAutoRepeatRate`：`43`;旋转盒键按键的自动重复间隔。
- `QStyle::SH_SpinBox_ClickAutoRepeatRate`：`44`;旋转盒鼠标点击的自动重复间隔。
- `QStyle::SH_SpinBox_ClickAutoRepeatThreshold`：`83`;旋转盒鼠标点击的自动重复阈值。
- `QStyle::SH_SpinBox_SelectOnStep (since Qt 6.3)`：`119`;无论使用按钮还是上下键更改数值，都会自动选择文本。
- `QStyle::SH_ToolTipLabel_Opacity`：`46`;表示尖端标签0的不透明度整数表示完全透明，255表示完全不透明。
- `QStyle::SH_DrawMenuBarSeparator`：`47`;表示菜单栏是否绘制分隔符。
- `QStyle::SH_TitleBar_ModifyNotification`：`48`;表示标题栏是否应显示“*”表示被修改的窗口。
- `QStyle::SH_Button_FocusPolicy`：`49`;按钮的默认聚焦策略。
- `QStyle::SH_CustomBase`：`0xf0000000`;自定义样式提示的基础值。自定义值必须大于此值。
- `QStyle::SH_MessageBox_UseBorderForButtonSpacing`：`50`;一个布尔值，指示按钮的边界（计算为按钮高度的一半）来确定消息框中按钮的间距。
- `QStyle::SH_MessageBox_CenterButtons`：`72`;一个布尔值，指示消息框中的按钮是否应居中（参见QDialogButtonBox：：setCentered()）。
- `QStyle::SH_MessageBox_TextInteractionFlags`：`70`;一个布尔，表示消息框中的文本是否应允许用户进行交互（例如选择）。
- `QStyle::SH_TitleBar_AutoRaise`：`51`;一个布尔值，表示当鼠标悬停在标题栏上的控件时是否应更新。
- `QStyle::SH_ToolButton_PopupDelay`：`52`;一个int，表示附在工具按钮上的菜单弹出延迟（毫秒）。
- `QStyle::SH_FocusFrame_Mask`：`53`;焦点框的遮罩。
- `QStyle::SH_RubberBand_Mask`：`54`;橡皮筋面具。
- `QStyle::SH_WindowFrame_Mask`：`55`;窗框的遮罩。
- `QStyle::SH_SpinControls_DisableOnBounds`：`56`;确定当达到旋转范围边界时，旋转控制是否显示为禁用。
- `QStyle::SH_Dial_BackgroundRole`：`57`;定义样式中拨盘控件的首选背景角色（如 `QPalette::ColorRole`）。
- `QStyle::SH_ComboBox_LayoutDirection`：`58`;连招盒的布局方向。默认情况下应与`QStyleOption::direction`变量所示相同。
- `QStyle::SH_ItemView_EllipsisLocation`：`59`;对于过长无法放入视图项的条目文本，应添加省略号的位置。
- `QStyle::SH_ItemView_ShowDecorationSelected`：`60`;当选择物品视图中的物品时，也要高亮该分支或其他装饰。
- `QStyle::SH_ItemView_ActivateItemOnSingleClick`：`61`;当用户在物品视图中单击物品时发出激活信号。否则，当用户双击物品时发出该信号。
- `QStyle::SH_Slider_AbsoluteSetButtons`：`64`;哪些鼠标按钮会触发滑块将数值设置为点击的位置。
- `QStyle::SH_Slider_PageSetButtons`：`65`;哪些鼠标按钮会让滑块按页面移动到数值上。
- `QStyle::SH_TabBar_ElideMode`：`67`;制表栏的默认省略风格。
- `QStyle::SH_DialogButtonLayout`：`68`;控制按钮在`QDialogButtonBox`中的布局，返回`QDialogButtonBox::ButtonLayout`枚举。
- `QStyle::SH_WizardStyle`：`78`;控制`QWizard`的外观和感觉。返回`QWizard::WizardStyle`枚举。
- `QStyle::SH_FormLayoutWrapPolicy`：`85`;提供行如何包裹在`QFormLayout`中的默认值。返回`QFormLayout::RowWrapPolicy`枚举。
- `QStyle::SH_FormLayoutFieldGrowthPolicy`：`88`;为字段在`QFormLayout`中增长提供默认值。返回`QFormLayout::FieldGrowthPolicy`枚举。
- `QStyle::SH_FormLayoutFormAlignment`：`89`;为`QFormLayout`在可用空间内对齐内容提供了默认值。返回`Qt::Alignment`枚举。
- `QStyle::SH_FormLayoutLabelAlignment`：`90`;为`QFormLayout`在可用空间内如何对齐标签提供了默认值。返回`Qt::Alignment`枚举。
- `QStyle::SH_ItemView_ArrowKeysNavigateIntoChildren`：`79`;控制树视图在被剔除并按下右箭头键时是否会选择第一个子节点。
- `QStyle::SH_ComboBox_PopupFrameStyle`：`69`;绘制组合盒弹出菜单时使用的框架风格。
- `QStyle::SH_DialogButtonBox_ButtonsHaveIcons`：`71`;指示 `QDialogButtonBox` 中的 StandardButton 是否应带有图标。
- `QStyle::SH_ItemView_MovementWithoutUpdatingSelection`：`74`;项目视图能够在不改变选择的情况下指示当前项目。
- `QStyle::SH_ToolTip_Mask`：`75`;工具尖端的遮罩。
- `QStyle::SH_FocusFrame_AboveWidget`：`76`;焦点帧被叠放在它正在“聚焦”的小部件上方。
- `QStyle::SH_TextControl_FocusIndicatorTextCharFormat`：`77`;指定用于高亮（例如在`QTextBrowser`中显示的富文本文档中聚焦锚点的文本格式。该格式必须是`QStyleHintReturnVariant`返回值变体中返回的 一个`QTextCharFormat`。`QTextFormat::OutlinePen`属性用于轮廓，`QTextFormat::BackgroundBrush`用于高亮区域的背景。
- `QStyle::SH_Menu_FlashTriggeredItem`：`81`;闪光触发物品。
- `QStyle::SH_Menu_FadeOutOnHide`：`82`;菜单逐渐淡出，而不是立即隐藏。
- `QStyle::SH_TabWidget_DefaultTabPosition`：`86`;标签栏在标签小部件中的默认位置。
- `QStyle::SH_ToolBar_Movable`：`87`;决定工具栏是否默认可移动。
- `QStyle::SH_ItemView_PaintAlternatingRowColorsForEmptyArea`：`84`;`QTreeView`是否为没有任何物品的区域绘制交替颜色的行。
- `QStyle::SH_Menu_Mask`：`80`;弹出菜单的遮罩。
- `QStyle::SH_ItemView_DrawDelegateFrame`：`91`;决定是否应为代理小部件设置框架。
- `QStyle::SH_TabBar_CloseButtonPosition`：`92`;决定标签栏中关闭按钮的位置。
- `QStyle::SH_DockWidget_ButtonsHaveFrame`：`93`;决定dockwidget按钮是否应有框架。默认为真。
- `QStyle::SH_ToolButtonStyle`：`94`;确定使用`Qt::ToolButtonFollowStyle`的工具按钮的默认系统样式。
- `QStyle::SH_RequestSoftwareInputPanel`：`95`;决定输入控件何时应请求软件输入面板。返回类型为`QStyle::RequestSoftwareInputPanel`的枚举。
- `QStyle::SH_ScrollBar_Transient`：`96`;确定样式是否支持暂时滚动条。当内容滚动时出现瞬态滚动条，不再需要时消失。
- `QStyle::SH_Menu_SupportsSections`：`97`;决定样式是否在菜单中显示部分，或将其视为纯分隔符。分区是带有文本和图标提示的分隔符。
- `QStyle::SH_ToolTip_WakeUpDelay`：`98`;确定显示提示前的延迟，单位为毫秒。
- `QStyle::SH_ToolTip_FallAsleepDelay`：`99`;确定显示提示时需要新唤醒时间的延迟（以毫秒计）（注意：显示而非隐藏）。当不需要新唤醒时，用户请求的工具提示几乎会即时显示。
- `QStyle::SH_Widget_Animate`：`100`;已弃用。请使用SH_Widget_Animation_Duration。
- `QStyle::SH_Splitter_OpaqueResize`：`101`;确定在交互式移动分路器时，控件是否会动态（不透明）调整大小。该枚举值于Qt 5.2引入。
- `QStyle::SH_TabBar_ChangeCurrentDelay`：`104`;在拖动标签栏时，确定当前制表符更换前的延迟，单位为毫秒。该枚举值于Qt 5.4引入
- `QStyle::SH_ItemView_ScrollMode`：`111`;样式指定的默认垂直和水平滚动模式。可以用`QAbstractItemView::setVerticalScrollMode()`和`QAbstractItemView::setHorizontalScrollMode()`覆盖。该枚举值在Qt 5.7中引入。
- `QStyle::SH_TitleBar_ShowToolTipsOnButtons`：`112`;决定工具提示是否显示在窗口标题栏按钮上。例如，Mac 风格将此设置为 false。该枚举值于 Qt 5.10 中引入。
- `QStyle::SH_Widget_Animation_Duration`：`113`;决定动画应持续多久（以毫秒计）。值为零表示动画将被禁用。该枚举值于第5.10季度引入。
- `QStyle::SH_ComboBox_AllowWheelScrolling`：`114`;决定是否可以用鼠标滚轮在`QComboBox`内滚动。除了Mac样式外，所有样式默认启用。该枚举值在Qt 5.10中引入。
- `QStyle::SH_SpinBox_ButtonsInsideFrame`：`115`;判断旋转盒按钮是否位于行编辑框内。该枚举值在Qt 5.11中引入。
- `QStyle::SH_SpinBox_StepModifier`：`116`;确定哪个`Qt::KeyboardModifier`增加`QAbstractSpinBox`的步进率。可能的值有`Qt::NoModifier`、默认的`Qt::ControlModifier`或`Qt::ShiftModifier`。`Qt::NoModifier`会禁用此功能。该枚举值在Qt 5.12中引入。
- `QStyle::SH_TabBar_AllowWheelScrolling`：`117`;决定鼠标滚轮是否可用于循环切换`QTabBar`的标签页。该枚举值在Qt 6.1中引入。
- `QStyle::SH_Table_AlwaysDrawLeftTopGridLines`：`118`;当隐藏头部时，确定最左边和最顶边的网格线是否绘制在表格中。默认为false。该枚举值在Qt 6.3中引入。

### `enum QStyle::SubControlflags QStyle::SubControls`

**作用与语义：**

该枚举描述了可用的子控制。子控制是复杂控制（`ComplexControl`）中的控制元素。
- `QStyle::SC_None`：`0x00000000`;与其他子控制组不匹配的特殊值。
- `QStyle::SC_ScrollBarAddLine`：`0x00000001`;滚动条加行（即下/右箭头）;另见`QScrollBar`。
- `QStyle::SC_ScrollBarSubLine`：`0x00000002`;滚动条子行（即上/左箭头）。
- `QStyle::SC_ScrollBarAddPage`：`0x00000004`;滚动条添加页面（即向下页）。
- `QStyle::SC_ScrollBarSubPage`：`0x00000008`;滚动条子页面（即翻页）。
- `QStyle::SC_ScrollBarFirst`：`0x00000010`;卷轴第一行（即主页）。
- `QStyle::SC_ScrollBarLast`：`0x00000020`;滚动条最后一行（即结尾）。
- `QStyle::SC_ScrollBarSlider`：`0x00000040`;滚动条滑块手柄。
- `QStyle::SC_ScrollBarGroove`：`0x00000080`;特殊的子控制，包含滑块手柄可能移动的区域。
- `QStyle::SC_SpinBoxUp`：`0x00000001`;旋转小部件的提升/增加;参见`QSpinBox`。
- `QStyle::SC_SpinBoxDown`：`0x00000002`;旋转控件向下/减少。
- `QStyle::SC_SpinBoxFrame`：`0x00000004`;旋转控件框架。
- `QStyle::SC_SpinBoxEditField`：`0x00000008`;旋转控件编辑字段。
- `QStyle::SC_ComboBoxEditField`：`0x00000002`;组合盒编辑字段;另见`QComboBox`。
- `QStyle::SC_ComboBoxArrow`：`0x00000004`;组合盒箭头按钮。
- `QStyle::SC_ComboBoxFrame`：`0x00000001`;组合盒框架。
- `QStyle::SC_ComboBoxListBoxPopup`：`0x00000008`;组合盒弹出的参考矩形。用于计算弹出窗口的位置。
- `QStyle::SC_SliderGroove`：`0x00000001`;特殊的子控制，包含滑块手柄可移动的区域。
- `QStyle::SC_SliderHandle`：`0x00000002`;滑块手柄。
- `QStyle::SC_SliderTickmarks`：`0x00000004`;滑块勾选标记。
- `QStyle::SC_ToolButton`：`0x00000001`;工具按钮（另见`QToolButton`）。
- `QStyle::SC_ToolButtonMenu`：`0x00000002`;子控制键，用于在工具按钮中打开弹出菜单。
- `QStyle::SC_TitleBarSysMenu`：`0x00000001`;系统菜单按钮（即恢复、关闭等）。
- `QStyle::SC_TitleBarMinButton`：`0x00000002`;最小化按钮。
- `QStyle::SC_TitleBarMaxButton`：`0x00000004`;最大化按钮。
- `QStyle::SC_TitleBarCloseButton`：`0x00000008`;关闭按钮。
- `QStyle::SC_TitleBarLabel`：`0x00000100`;窗户标题标签。
- `QStyle::SC_TitleBarNormalButton`：`0x00000010`;普通（恢复）按钮。
- `QStyle::SC_TitleBarShadeButton`：`0x00000020`;遮阳按钮。
- `QStyle::SC_TitleBarUnshadeButton`：`0x00000040`;解除着色按钮。
- `QStyle::SC_TitleBarContextHelpButton`：`0x00000080`;上下文帮助按钮。
- `QStyle::SC_DialHandle`：`0x00000002`;旋钮的手柄（即你用来控制旋钮的装置）。
- `QStyle::SC_DialGroove`：`0x00000001`;拨盘槽。
- `QStyle::SC_DialTickmarks`：`0x00000004`;刻度盘的刻度标记。
- `QStyle::SC_GroupBoxFrame`：`0x00000008`;团体盒子的框架。
- `QStyle::SC_GroupBoxLabel`：`0x00000002`;团体盒子的标题。
- `QStyle::SC_GroupBoxCheckBox`：`0x00000001`;组框的可选复选框。
- `QStyle::SC_GroupBoxContents`：`0x00000004`;组内内容。
- `QStyle::SC_MdiNormalButton`：`0x00000002`;菜单栏中MDI子窗口的正常按钮。
- `QStyle::SC_MdiMinButton`：`0x00000001`;菜单栏中MDI子窗口的最小化按钮。
- `QStyle::SC_MdiCloseButton`：`0x00000004`;菜单栏中MDI子窗口的关闭按钮。
- `QStyle::SC_All`：`0xffffffff`;与所有子控制点匹配的特殊值。
SubControls 类型是 QFlags 的 typedef<SubControl>。它存储 SubControl 值的 OR 组合。

### `enum QStyle::SubElement`

**作用与语义：**

这个枚举代表小部件的一个子区域。样式实现利用这些区域来绘制小部件的不同部分。
- `QStyle::SE_PushButtonContents`：`0`;包含标签（带文字或像素地图图标）的区域。
- `QStyle::SE_PushButtonFocusRect`：`1`;焦点矩形块的面积（通常大于内容块）。
- `QStyle::SE_PushButtonLayoutItem`：`37`;计入父布局的区域。
- `QStyle::SE_PushButtonBevel`：`56`;[自5.15起]用于按钮斜角的区域。
- `QStyle::SE_CheckBoxIndicator`：`2`;状态指示器区域（例如，勾选标记）。
- `QStyle::SE_CheckBoxContents`：`3`;标签区域（文本或像素地图）。
- `QStyle::SE_CheckBoxFocusRect`：`4`;焦点指示区。
- `QStyle::SE_CheckBoxClickRect`：`5`;可点击区域，默认为SE_CheckBoxFocusRect。
- `QStyle::SE_CheckBoxLayoutItem`：`32`;计入父布局的区域。
- `QStyle::SE_DateTimeEditLayoutItem`：`34`;计入父布局的区域。
- `QStyle::SE_RadioButtonIndicator`：`6`;状态指示器区域。
- `QStyle::SE_RadioButtonContents`：`7`;标签区域。
- `QStyle::SE_RadioButtonFocusRect`：`8`;焦点指示区。
- `QStyle::SE_RadioButtonClickRect`：`9`;可点击区域，默认为SE_RadioButtonFocusRect。
- `QStyle::SE_RadioButtonLayoutItem`：`38`;计入父布局的区域。
- `QStyle::SE_ComboBoxFocusRect`：`10`;对焦指示区。
- `QStyle::SE_SliderFocusRect`：`11`;对焦指示区。
- `QStyle::SE_SliderLayoutItem`：`39`;计入父布局的区域。
- `QStyle::SE_SpinBoxLayoutItem`：`40`;计入父布局的区域。
- `QStyle::SE_ProgressBarGroove`：`12`;槽区。
- `QStyle::SE_ProgressBarContents`：`13`;进度指示区。
- `QStyle::SE_ProgressBarLabel`：`14`;用于文字标签的区域。
- `QStyle::SE_ProgressBarLayoutItem`：`36`;计入父布局的区域。
- `QStyle::SE_FrameContents`：`27`;帧内容物的区域。
- `QStyle::SE_ShapedFrameContents`：`51`;使用`QStyleOptionFrame`形状表示框架内容的面积;参见`QFrame`
- `QStyle::SE_FrameLayoutItem`：`42`;计入父布局的区域。
- `QStyle::SE_HeaderArrow`：`17`;用于头部排序指示器的区域。
- `QStyle::SE_HeaderLabel`：`16`;标题中标签的区域。
- `QStyle::SE_LabelLayoutItem`：`35`;计入父布局的区域。
- `QStyle::SE_LineEditContents`：`26`;用于行编辑内容的区域。
- `QStyle::SE_TabWidgetLeftCorner`：`21`;标签小部件中左角小部件的区域。
- `QStyle::SE_TabWidgetRightCorner`：`22`;标签小部件中右角小部件的区域。
- `QStyle::SE_TabWidgetTabBar`：`18`;标签栏小部件的区域。
- `QStyle::SE_TabWidgetTabContents`：`20`;标签控件内容的区域。
- `QStyle::SE_TabWidgetTabPane`：`19`;用于标签控件面板的区域。
- `QStyle::SE_TabWidgetLayoutItem`：`44`;计入父布局的区域。
- `QStyle::SE_ToolBoxTabContents`：`15`;工具箱标签页图标和标签的区域。
- `QStyle::SE_ToolButtonLayoutItem`：`41`;计入父布局的区域。
- `QStyle::SE_ItemViewItemCheckIndicator`：`23`;查看项目的勾选标记区域。
- `QStyle::SE_TabBarTearIndicator`：`24`;已弃用。请使用SE_TabBarTearIndicatorLeft。
- `QStyle::SE_TabBarTearIndicatorLeft`: `SE_TabBarTearIndicator`; 带有滚动箭头的选项卡栏左侧的拆分指示器区域。
- `QStyle::SE_TabBarTearIndicatorRight`: `55`; 带有滚动箭头的选项卡栏右侧的拆分指示器区域。
- `QStyle::SE_TabBarScrollLeftButton`: `53`; 带有滚动按钮的选项卡栏左滚动按钮区域。
- `QStyle::SE_TabBarScrollRightButton`: `54`; 带有滚动按钮的选项卡栏右滚动按钮区域。
- `QStyle::SE_TreeViewDisclosureItem`: `25`; 树枝中实际展开项的区域。
- `QStyle::SE_GroupBoxLayoutItem`: `43`; 计入父布局的区域。
- `QStyle::SE_CustomBase`: `0xf0000000`; 自定义子元素的基值。自定义值必须大于此值。
- `QStyle::SE_DockWidgetFloatButton`: `29`; 停靠窗口的浮动按钮。
- `QStyle::SE_DockWidgetTitleBarText`: `30`; 停靠窗口标题的文本边界。
- `QStyle::SE_DockWidgetCloseButton`: `28`; 停靠窗口的关闭按钮。
- `QStyle::SE_DockWidgetIcon`: `31`; 停靠窗口的图标。
- `QStyle::SE_ComboBoxLayoutItem`: `33`; 计入父布局的区域。
- `QStyle::SE_ItemViewItemDecoration`: `45`; 视图项装饰（图标）区域。
- `QStyle::SE_ItemViewItemText`: `46`; 视图项文本区域。
- `QStyle::SE_ItemViewItemFocusRect`: `47`; 视图项焦点矩形区域。
- `QStyle::SE_TabBarTabLeftButton`: `48`; 选项卡栏中选项卡左侧的小部件区域。
- `QStyle::SE_TabBarTabRightButton`: `49`; 选项卡栏中选项卡右侧的小部件区域。
- `QStyle::SE_TabBarTabText`: `50`; 选项卡栏中选项卡文本区域。
- `QStyle::SE_ToolBarHandle`: `52`; 工具栏的拖动柄区域。

### `QStyle::QStyle()`

**作用与语义：**

构建一个样式对象。

### `[virtual noexcept] QStyle::~QStyle()`

**作用与语义：**

破坏样式对象。

### `[static] QRect QStyle::alignedRect(Qt::LayoutDirection direction, Qt::Alignment alignment, const QSize &size, const QRect &rectangle)`

**作用与语义：**

返回一个指定`size`的新矩形，该矩形根据指定的`alignment`和`direction`对齐到给定的`rectangle`。

### `int QStyle::combinedLayoutSpacing(QSizePolicy::ControlTypes controls1, QSizePolicy::ControlTypes controls2, Qt::Orientation orientation, QStyleOption *option = nullptr, QWidget *widget = nullptr) const`

**作用与语义：**

返回布局中应使用`controls1`与`controls2`之间的间距。`orientation`指定控件是并排排列还是垂直堆叠。`option`参数可用于传递关于父控件的额外信息。`widget`参数为可选，若`option` `nullptr`也可用。
`controls1`和`controls2`是零种或多个对照类型的运筹组合。
该函数由布局系统调用。仅在`PM_LayoutHorizontalSpacing`或`PM_LayoutVerticalSpacing`返回负值时使用。

### `[pure virtual] void QStyle::drawComplexControl(QStyle::ComplexControl control, const QStyleOptionComplex *option, QPainter *painter, const QWidget *widget = nullptr) const`

**作用与语义：**

使用提供的`painter`并按照`option`指定的样式选项绘制给定的`control`。
`widget`论证是可选的，可以作为绘制控制的辅助工具。
`option`参数是指向`QStyleOptionComplex`对象的指针，可以用`qstyleoption_cast()`函数将其转换为正确的子类。注意，指定`option`的`rect`成员必须处于逻辑坐标中。该函数的重现应使用`visualRect()`将逻辑坐标改为屏幕坐标，然后再调用`drawPrimitive()`或`drawControl()`函数。
下表列出了复杂的控制元素及其相关的样式选项子类。样式选项包含绘制控件所需的所有参数，包括保存绘制时使用的样式标志的`QStyleOption::state`。表格还描述了在将给定`option`铸造到相应子类时设置的标志。
- `Complex Control`：`QStyleOptionComplex`子类;风格标志;备注
- `CC_SpinBox`：`QStyleOptionSpinBox`;`State_Enabled`;如果旋转盒被启用，则设置为。
- `State_HasFocus`：如果旋转盒有输入焦点，则设置。
- `CC_ComboBox`：`QStyleOptionComboBox`;`State_Enabled`;如果组合盒被启用，则设置为。
- `State_HasFocus`：如果组合盒有输入焦点，则设置。
- `CC_ScrollBar`：`QStyleOptionSlider`;`State_Enabled`;如果启用滚动条，则设置。
- `State_HasFocus`：如果滚动条有输入焦点，则设置为。
- `CC_Slider`：`QStyleOptionSlider`;`State_Enabled`;启用滑块时设置。
- `State_HasFocus`：如果滑块有输入焦点，则设置为。
- `CC_Dial`：`QStyleOptionSlider`;`State_Enabled`;如果表盘被启用，则设置。
- `State_HasFocus`：如果旋钮有输入焦点，则设置。
- `CC_ToolButton`：`QStyleOptionToolButton`;`State_Enabled`;如果工具按钮被启用，则设置为。
- `State_HasFocus`：如果工具按钮有输入焦点，则设置为。
- `State_DownArrow`：当工具按钮按下时设置（如按住鼠标或空格键）。
- `State_On`：如果工具按钮是切换按钮并且已开启，则设置。
- `State_AutoRaise`：如果工具按钮启用自动抬起，则设置。
- `State_Raised`：如果按钮未按下、未开启且在启用自动抬起时不包含鼠标，则设置为不存在。
- `CC_TitleBar`：`QStyleOptionTitleBar`;`State_Enabled`;如果标题栏启用，则设置。

### `[pure virtual] void QStyle::drawControl(QStyle::ControlElement element, const QStyleOption *option, QPainter *painter, const QWidget *widget = nullptr) const`

**作用与语义：**

用`option`指定的样式选项，绘制给定`element`，并附带提供的 `painter`。
`widget`参数是可选的，可以作为绘制控制项的辅助工具。`option`参数是一个指向`QStyleOption`对象的指针，可以用`qstyleoption_cast()`函数将其转换为正确的子类。
下表列出了控制元素及其相关的样式选项子类。样式选项包含绘制控件所需的所有参数，包括保存绘制时使用的样式标志的 `QStyleOption::state`。表格还描述了将指定选项转换为相应子类时设置的标志。
注意，如果这里没有列出控制元素，那是因为它使用了纯 `QStyleOption` 对象。
- `Control Element`：`QStyleOption`子类;风格标志;备注
- `CE_MenuItem`，`CE_MenuBarItem`：`QStyleOptionMenuItem`;`State_Selected`;菜单项目前为选中项。
- `State_Enabled`：该物品已启用。
- `State_DownArrow`：表示应绘制向下滚动箭头。
- `State_UpArrow`：表示应绘制向上滚动箭头
- `State_HasFocus`：如果菜单栏有输入焦点，则设置为。
- `CE_PushButton`、`CE_PushButtonBevel`、`CE_PushButtonLabel`：`QStyleOptionButton`;`State_Enabled`;如果按钮被启用，则设置为。
- `State_HasFocus`：如果按钮有输入焦点，则设置为。
- `State_Raised`：如果按钮未按下、未开启且未平放，则设置。
- `State_On`：如果按钮是切换按钮且已开启，则设置为。
- `State_Sunken`：当按钮按下时设置（即按住鼠标或空格键）。
- `CE_RadioButton`、`CE_RadioButtonLabel`、`CE_CheckBox`、`CE_CheckBoxLabel`：`QStyleOptionButton`;`State_Enabled`;如果按钮被启用，则设置为。
- `State_HasFocus`：按钮是否带有输入焦点，则设置为。
- `State_On`：如果按钮被勾选，则设置。
- `State_Off`：如果按钮未被勾选，则设置。
- `State_NoChange`：如果按钮处于 NoChange 状态，则设置为 NoChange。
- `State_Sunken`：当按钮按下时设置（即鼠标或空格键被按下）。
- `CE_ProgressBarContents`、`CE_ProgressBarLabel`、`CE_ProgressBarGroove`：`QStyleOptionProgressBar`;`State_Enabled`;如果进度条已启用，则设置为。
- `State_HasFocus`：如果进度条有输入焦点，则设置为。
- `CE_Header`，`CE_HeaderSection`，`CE_HeaderLabel`：`QStyleOptionHeader`
- `CE_TabBarTab`、`CE_TabBarTabShape`、`CE_TabBarTabLabel`：`QStyleOptionTab`;`State_Enabled`;如果标签栏被启用，则设置为。
- `State_Selected`：标签栏是当前选择的标签栏。
- `State_HasFocus`：如果标签栏标签页有输入焦点，则设置为。
- `CE_ToolButtonLabel`：`QStyleOptionToolButton`;`State_Enabled`;如果工具按钮被启用，则设置为。
- `State_HasFocus`：设置工具按钮是否带有输入焦点。
- `State_Sunken`：当工具按钮按下时设置（如鼠标键或空格键被按下）。
- `State_On`：如果工具按钮是切换按钮且已开启，则设置为。
- `State_AutoRaise`：如果工具按钮启用了自动抬高，则设置为。
- `State_MouseOver`：如果鼠标指针位于工具按钮上方，则设置。
- `State_Raised`：如果按钮未按下且未开启，则设置。
- `CE_ToolBoxTab`：`QStyleOptionToolBox`;`State_Selected`;标签是当前选择的标签。
- `CE_HeaderSection`：`QStyleOptionHeader`;`State_Sunken`;表示段落被压制。
- `State_UpArrow`：表示排序指示器应指向上方。
- `State_DownArrow`：表示排序指示器应指向下方。

### `[virtual] void QStyle::drawItemPixmap(QPainter *painter, const QRect &rectangle, int alignment, const QPixmap &pixmap) const`

**作用与语义：**

根据指定`alignment`，使用提供的`painter`，在指定`rectangle`中绘制给定`pixmap`。

### `[virtual] void QStyle::drawItemText(QPainter *painter, const QRect &rectangle, int alignment, const QPalette &palette, bool enabled, const QString &text, QPalette::ColorRole textRole = QPalette::NoRole) const`

**作用与语义：**

在指定`rectangle`中，使用提供的`painter`和`palette`抽取给定的`text`。
文本由画家用钢笔绘制，并根据指定`alignment`对齐和包裹。如果指定了明确的`textRole`，文本将使用该`palette`的颜色绘制。`enabled`参数表示该物品是否启用;在重新实现该功能时，`enabled`参数应影响该物品的绘制方式。

### `[pure virtual] void QStyle::drawPrimitive(QStyle::PrimitiveElement element, const QStyleOption *option, QPainter *painter, const QWidget *widget = nullptr) const`

**作用与语义：**

利用`option`指定样式选项，用提供的`painter`绘制给定的原基`element`。
`widget`参数是可选的，可能包含一个小部件，帮助绘制原元素。
下表列出了原始元素及其相关的样式选项子类。样式选项包含绘制元素所需的所有参数，包括保存绘制时使用的样式标志的`QStyleOption::state`。表格还描述了将指定选项铸造到相应子类时设置的标志。
注意，如果这里没有列出原始元素，那是因为它使用了普通`QStyleOption`对象。
- 1 `Primitive Element`：`QStyleOption`子类;风格标志;备注
- `PE_FrameFocusRect`：`QStyleOptionFocusRect`;`State_FocusAtBorder`;焦点是在边框还是在控件内部。
- `PE_IndicatorCheckBox`：`QStyleOptionButton`;`State_NoChange`;表示“三州”复选框。
- `State_On`：表示指示器已检查。
- `PE_IndicatorRadioButton`：`QStyleOptionButton`;`State_On`;表示选择了单选按钮。
- `State_NoChange`：表示“三态”控制器。
- `State_Enabled`：表示控制器已启用。
- `PE_IndicatorBranch`：`QStyleOption`;`State_Children`;表示应绘制扩展树以显示子项的控制。
- `State_Item`：表示应绘制水平分支（用于显示子项）。
- `State_Open`：表示树枝已扩展。
- `State_Sibling`：表示应绘制一条垂直线（以显示兄弟项目）。
- `PE_IndicatorHeaderArrow`：`QStyleOptionHeader`;`State_UpArrow`;表示箭头应向上拉;否则箭头应向下拉。
- `PE_FrameGroupBox`、`PE_Frame`、`PE_FrameLineEdit`、`PE_FrameMenu`、`PE_FrameDockWidget`、`PE_FrameWindow`：`QStyleOptionFrame`;`State_Sunken`;表示框架应被下沉。
- `PE_IndicatorToolBarHandle`：`QStyleOption`;`State_Horizontal`;表示窗户把手是水平而非垂直。
- `PE_IndicatorSpinPlus`，`PE_IndicatorSpinMinus`，`PE_IndicatorSpinUp`，`PE_IndicatorSpinDown`，`: `QStyleOptionSpinBox`; `State_Sunken';表示按钮被按下。
- `PE_PanelButtonCommand`：`QStyleOptionButton`;`State_Enabled`;如果按钮被启用，则设置为。
- `State_HasFocus`：如果按钮有输入焦点，则设置为。
- `State_Raised`：设置按钮未按下、未开且未平放。
- `State_On`：如果按钮是切换按钮并且已开启，则设置为。
- `State_Sunken`：当按钮按下时设置（即按住鼠标或空格键）。

### `[pure virtual] QPixmap QStyle::generatedIconPixmap(QIcon::Mode iconMode, const QPixmap &pixmap, const QStyleOption *option) const`

**作用与语义：**

返回给定`pixmap`的副本，样式符合指定`iconMode`并考虑`option`指定的调色板。
`option`参数可以传递额外信息，但必须包含调色板。
注意并非所有像素映射都符合，此时返回的像素映射是普通的副本。

### `[pure virtual] QStyle::SubControl QStyle::hitTestComplexControl(QStyle::ComplexControl control, const QStyleOptionComplex *option, const QPoint &position, const QWidget *widget = nullptr) const`

**作用与语义：**

返回给定复`control`中给定`position`的子控制（样式选项由`option`指定）。
注意`position`以屏幕坐标表示。
`option`参数是指向`QStyleOptionComplex`对象（或其子类之一）的指针。对象可以通过`qstyleoption_cast()`函数转换为相应类型。详情请参见 `drawComplexControl()`。`widget`参数是可选的，可以包含函数的额外信息。

### `[virtual] QRect QStyle::itemPixmapRect(const QRect &rectangle, int alignment, const QPixmap &pixmap) const`

**作用与语义：**

返回给定`rectangle`内根据定义`alignment`绘制指定`pixmap`的面积。

### `[virtual] QRect QStyle::itemTextRect(const QFontMetrics &metrics, const QRect &rectangle, int alignment, bool enabled, const QString &text) const`

**作用与语义：**

返回给定字体 `metrics` 和 `alignment` 在给定`rectangle`内绘制该`text`的区域。`enabled` 参数表示该关联项是否被启用。
如果给定`rectangle`大于渲染`text`所需的面积，返回的矩形将根据指定的`alignment`在`rectangle`范围内偏移。例如，如果`alignment` `Qt::AlignCenter`，返回的矩形将置中于`rectangle`内。如果给定`rectangle`小于所需面积，返回的矩形将是足够渲染`text`最小的矩形。

### `[pure virtual] int QStyle::layoutSpacing(QSizePolicy::ControlType control1, QSizePolicy::ControlType control2, Qt::Orientation orientation, const QStyleOption *option = nullptr, const QWidget *widget = nullptr) const`

**作用与语义：**

返回布局中应使用在`control1`与`control2`之间的间距。`orientation` 指定控件是并排排列还是垂直堆叠。`option`参数可用于传递关于父控件的额外信息。`widget`参数为可选，若`option`为`nullptr`也可以使用。
该函数由布局系统调用。仅当`PM_LayoutHorizontalSpacing`或`PM_LayoutVerticalSpacing`返回负值时使用。

### `[since 6.1] QString QStyle::name() const`

**作用与语义：**

还原了风格名称。
这个数值可以用来创建带有`QStyleFactory::create()`的风格。

### `[pure virtual] int QStyle::pixelMetric(QStyle::PixelMetric metric, const QStyleOption *option = nullptr, const QWidget *widget = nullptr) const`

**作用与语义：**

返回给定像素`metric`的值。
指定的`option`和`widget`可用于计算度量。`option`可以通过`qstyleoption_cast()`函数转换为相应类型。请注意，即使是可以使用该函数的PixelMetrics，`option`也可能为零。请参见下表，了解相应的`option`铸造：
- `Pixel Metric`：`QStyleOption`子类
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

### `[virtual] void QStyle::polish(QWidget *widget)`

**作用与语义：**

初始化给定`widget`的外观。
该函数会在每个小部件完全创建后、首次展示之前的某个时间点调用。
注意默认实现不做任何操作。该函数中的合理操作可能是调用 QWidget：：setBackgroundMode() 函数来设置控件。不要使用该函数设置，例如几何体。重新实现该函数提供了一个后门，可以通过它更改控件的外观，但使用 Qt 的样式引擎，通常不需要实现该函数;而是重新实现 `drawItemPixmap()`、`drawItemText()`、`drawPrimitive()` 等。
`QWidget::inherits()`函数可能提供足够的信息，允许针对类别的定制。但由于新的`QStyle`子类预计能与所有当前和未来的控件合理兼容，建议有限度地使用硬编码自定义。

### `[virtual] void QStyle::polish(QApplication *application)`

**作用与语义：**

给定`application`对象的初始化延迟。

### `[virtual] void QStyle::polish(QPalette &palette)`

**作用与语义：**

根据风格特定的色彩调色板需求（如果有的话）更改`palette`。

### `const QStyle *QStyle::proxy() const`

**作用与语义：**

该函数返回该样式当前的代理。默认情况下，大多数样式会返回自身。但当代理样式正在使用时，它会允许样式调用回其代理。

### `[pure virtual] QSize QStyle::sizeFromContents(QStyle::ContentsType type, const QStyleOption *option, const QSize &contentsSize, const QWidget *widget = nullptr) const`

**作用与语义：**

返回指定`option`和`type`描述的元素大小，基于提供的`contentsSize`。
`option`参数是指向`QStyleOption`或其子类之一的指针。`option`可以通过 `qstyleoption_cast()` 函数转换为相应类型。`widget` 是可选参数，可以包含用于计算大小的额外信息。
下表显示了合适的`option`铸件：
- `Contents Type`：`QStyleOption` 子类
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

### `[static] int QStyle::sliderPositionFromValue(int min, int max, int logicalValue, int span, bool upsideDown = false)`

**作用与语义：**

将给定`logicalValue`转换为像素位置。`min`参数映射为0，`max`映射为`span`，其他值均匀分布于中间。
该函数可以在`span`小于4096的情况下处理整数范围而不溢出。
默认情况下，该函数假设最大值在右侧用于水平物品，最大值在底部用于垂直物品。将`upsideDown`参数设置为true以反转此行为。

### `[static] int QStyle::sliderValueFromPosition(int min, int max, int position, int span, bool upsideDown = false)`

**作用与语义：**

将给定像素`position`转换为逻辑值。0映射为`min`参数，`span`映射到`max`，其他值均匀分布。
该函数可以处理整个整数范围而不溢出。
默认情况下，该函数假设最大值位于水平项的右侧，垂直项的最大值位于底部。将`upsideDown`参数设置为true以逆转此行为。

### `[pure virtual] QIcon QStyle::standardIcon(QStyle::StandardPixmap standardIcon, const QStyleOption *option = nullptr, const QWidget *widget = nullptr) const`

**作用与语义：**

返回给定`standardIcon`的图标。
`standardIcon`是一个标准像素映射，可以遵循某些现有的图形界面风格或指南。`option`参数可用于传递定义适当图标时所需的额外信息。`widget`参数是可选的，也可用于辅助确定图标。

### `[virtual] QPalette QStyle::standardPalette() const`

**作用与语义：**

回归该风格的标准调色板。
请注意，在支持系统颜色的系统中，样式的标准调色板不被使用。特别是，Windows Vista 和 Mac 样式不使用标准调色板，而是使用原生主题引擎。对于这些样式，你不应用 `QApplication::setPalette()` 来设置调色板。

### `[pure virtual] int QStyle::styleHint(QStyle::StyleHint hint, const QStyleOption *option = nullptr, const QWidget *widget = nullptr, QStyleHintReturn *returnData = nullptr) const`

**作用与语义：**

返回一个整数，代表指定样式`hint`，针对给定样式`widget`，由提供的样式`option`描述。
`returnData`用于查询小部件需要比 styleHint() 返回的整数更详细的数据。详情请参见 `QStyleHintReturn`类描述。

### `[pure virtual] QRect QStyle::subControlRect(QStyle::ComplexControl control, const QStyleOptionComplex *option, QStyle::SubControl subControl, const QWidget *widget = nullptr) const`

**作用与语义：**

返回包含给定复数 `control`指定`subControl`的矩形（样式由 `option` 指定）。矩形定义在屏幕坐标中。
`option`参数是指向`QStyleOptionComplex`或其子类之一的指针，可以使用`qstyleoption_cast()`函数转换为相应类型。详情请参见 `drawComplexControl()`。`widget`是可选的，可以包含函数的额外信息。

### `[pure virtual] QRect QStyle::subElementRect(QStyle::SubElement element, const QStyleOption *option, const QWidget *widget = nullptr) const`

**作用与语义：**

返回给定`element`的子区域，如所提供样式`option`所述。返回的矩形定义为屏幕坐标。
`widget`参数是可选的，可用于辅助确定面积。`QStyleOption`对象可以通过`qstyleoption_cast()`函数转换为相应类型。下表了解了相应的`option`铸造：
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

### `[virtual] void QStyle::unpolish(QWidget *widget)`

**作用与语义：**

取消给定`widget`的初始化。
该函数是`polish()`的对应功能。每当样式动态变化时，每个抛光小部件都会调用它;前者必须先恢复其设置，新样式才能再次抛光。
注意，unpolish() 只有在控件被销毁时才会被调用。这在某些情况下可能会引发问题，例如，如果你从界面中移除一个控件，缓存它，然后在样式改变后重新插入;Qt 的一些类会缓存他们的控件。

### `[virtual] void QStyle::unpolish(QApplication *application)`

**作用与语义：**

取消初始化给定的`application`。

### `[static] Qt::Alignment QStyle::visualAlignment(Qt::LayoutDirection direction, Qt::Alignment alignment)`

**作用与语义：**

`alignment`根据布局`direction`，将`Qt::AlignLeft`或`Qt::AlignRight`的无`Qt::AlignAbsolute`转换为`Qt::AlignLeft`或`Qt::AlignRight`，并`Qt::AlignAbsolute`。其他对齐旗保持不变。
如果没有指定水平对齐，函数返回给定布局`direction`的默认对齐。
`QWidget::layoutDirection`。

### `[static] QPoint QStyle::visualPos(Qt::LayoutDirection direction, const QRect &boundingRectangle, const QPoint &logicalPosition)`

**作用与语义：**

返回给定`logicalPosition`并根据指定`direction`转换为屏幕坐标。执行平移时使用`boundingRectangle`。

### `[static] QRect QStyle::visualRect(Qt::LayoutDirection direction, const QRect &boundingRectangle, const QRect &logicalRectangle)`

**作用与语义：**

返回给定`logicalRectangle`转换为基于指定`direction`的屏幕坐标。执行翻译时使用`boundingRectangle`。
该函数用于支持从右到左的桌面，通常用于`subControlRect()`函数的实现中。

### `flags State`

**作用与语义：**

该枚举描述了绘制原始元素时使用的标志。
注意，并非所有原语都使用所有这些标志，而且这些标志对不同物品的含义可能不同。
- `QStyle::State_None`：`0x00000000`;表示该小部件没有状态。
- `QStyle::State_Active`：`0x00010000`;表示该小部件处于激活状态。
- `QStyle::State_AutoRaise`：`0x00001000`;用于指示工具按钮是否应使用自动抬高外观。
- `QStyle::State_Children`：`0x00080000`;用于表示项目视图分支是否有子节点。
- `QStyle::State_DownArrow`：`0x00000040`;用于指示小部件上是否应显示下箭头。
- `QStyle::State_Editing`：`0x00400000`;已弃用。不再使用，因为编辑器被绘制在物品视图单元格上。
- `QStyle::State_Enabled`：`0x00000001`;用于表示小部件是否被启用。
- `QStyle::State_HasEditFocus`：`0x01000000`;用于表示小部件当前是否具有编辑焦点。
- `QStyle::State_HasFocus`：`0x00000100`;用于表示小部件是否有焦点。
- `QStyle::State_Horizontal`：`0x00000080`;用于表示小部件是否水平布局，例如。工具栏。
- `QStyle::State_KeyboardFocusChange`：`0x00800000`;用于表示是否通过键盘更改了焦点，例如Tab、BackTab或快捷键。
- `QStyle::State_MouseOver`：`0x00002000`;用于表示小部件是否位于鼠标下方。
- `QStyle::State_NoChange`：`0x00000010`;用于表示三州复选框。
- `QStyle::State_Off`：`0x00000008`;用于表示小部件未被检查。
- `QStyle::State_On`：`0x00000020`;用于表示控件是否被检查。
- `QStyle::State_Raised`：`0x00000002`;用于表示按钮是否被抬起。
- `QStyle::State_ReadOnly`：`0x02000000`;用于表示小部件是否为只读。
- `QStyle::State_Selected`：`0x00008000`;用于表示是否选中了某个小部件。
- `QStyle::State_Item`：`0x00100000`;用于项目视图，指示是否应绘制水平分支。
- `QStyle::State_Open`：`0x00040000`;用于项目视图，表示树枝是否开放。
- `QStyle::State_Sibling`：`0x00200000`;用于项目视图，表示是否需要绘制垂直线（对于兄弟姐妹）。
- `QStyle::State_Sunken`：`0x00000004`;用于表示小部件是否被按下或沉入。
- `QStyle::State_UpArrow`：`0x00004000`;用于指示小部件上是否应显示上箭头。
- `QStyle::State_Mini`：`0x08000000`;用于表示迷你风格的Mac小部件或按钮。
- `QStyle::State_Small`：`0x04000000`;用于表示小型风格的 Mac 小部件或按钮。
状态类型是QFlag的typedef<StateFlag>。它存储StateFlag值的OR组合。

### `enum StateFlag { State_None, State_Active, State_AutoRaise, State_Children, State_DownArrow, …, State_Small }`

**作用与语义：**

该枚举描述了绘制原始元素时使用的标志。
注意，并非所有原语都使用所有这些标志，而且这些标志对不同物品的含义可能不同。
- `QStyle::State_None`：`0x00000000`;表示该小部件没有状态。
- `QStyle::State_Active`：`0x00010000`;表示该小部件处于激活状态。
- `QStyle::State_AutoRaise`：`0x00001000`;用于指示工具按钮是否应使用自动抬高外观。
- `QStyle::State_Children`：`0x00080000`;用于表示项目视图分支是否有子节点。
- `QStyle::State_DownArrow`：`0x00000040`;用于指示小部件上是否应显示下箭头。
- `QStyle::State_Editing`：`0x00400000`;已弃用。不再使用，因为编辑器被绘制在物品视图单元格上。
- `QStyle::State_Enabled`：`0x00000001`;用于表示小部件是否被启用。
- `QStyle::State_HasEditFocus`：`0x01000000`;用于表示小部件当前是否具有编辑焦点。
- `QStyle::State_HasFocus`：`0x00000100`;用于表示小部件是否有焦点。
- `QStyle::State_Horizontal`：`0x00000080`;用于表示小部件是否水平布局，例如。工具栏。
- `QStyle::State_KeyboardFocusChange`：`0x00800000`;用于表示是否通过键盘更改了焦点，例如Tab、BackTab或快捷键。
- `QStyle::State_MouseOver`：`0x00002000`;用于表示小部件是否位于鼠标下方。
- `QStyle::State_NoChange`：`0x00000010`;用于表示三州复选框。
- `QStyle::State_Off`：`0x00000008`;用于表示小部件未被检查。
- `QStyle::State_On`：`0x00000020`;用于表示控件是否被检查。
- `QStyle::State_Raised`：`0x00000002`;用于表示按钮是否被抬起。
- `QStyle::State_ReadOnly`：`0x02000000`;用于表示小部件是否为只读。
- `QStyle::State_Selected`：`0x00008000`;用于表示是否选中了某个小部件。
- `QStyle::State_Item`：`0x00100000`;用于项目视图，指示是否应绘制水平分支。
- `QStyle::State_Open`：`0x00040000`;用于项目视图，表示树枝是否开放。
- `QStyle::State_Sibling`：`0x00200000`;用于项目视图，表示是否需要绘制垂直线（对于兄弟姐妹）。
- `QStyle::State_Sunken`：`0x00000004`;用于表示小部件是否被按下或沉入。
- `QStyle::State_UpArrow`：`0x00004000`;用于指示小部件上是否应显示上箭头。
- `QStyle::State_Mini`：`0x08000000`;用于表示迷你风格的Mac小部件或按钮。
- `QStyle::State_Small`：`0x04000000`;用于表示小型风格的 Mac 小部件或按钮。
状态类型是QFlag的typedef<StateFlag>。它存储StateFlag值的OR组合。

### `enum SubControl { SC_None, SC_ScrollBarAddLine, SC_ScrollBarSubLine, SC_ScrollBarAddPage, SC_ScrollBarSubPage, …, SC_All }`

**作用与语义：**

该枚举描述了可用的子控制。子控制是复杂控制（`ComplexControl`）中的控制元素。
- `QStyle::SC_None`：`0x00000000`;与其他子控制组不匹配的特殊值。
- `QStyle::SC_ScrollBarAddLine`：`0x00000001`;滚动条加行（即下/右箭头）;另见`QScrollBar`。
- `QStyle::SC_ScrollBarSubLine`：`0x00000002`;滚动条子行（即上/左箭头）。
- `QStyle::SC_ScrollBarAddPage`：`0x00000004`;滚动条添加页面（即向下页）。
- `QStyle::SC_ScrollBarSubPage`：`0x00000008`;滚动条子页面（即翻页）。
- `QStyle::SC_ScrollBarFirst`：`0x00000010`;卷轴第一行（即主页）。
- `QStyle::SC_ScrollBarLast`：`0x00000020`;滚动条最后一行（即结尾）。
- `QStyle::SC_ScrollBarSlider`：`0x00000040`;滚动条滑块手柄。
- `QStyle::SC_ScrollBarGroove`：`0x00000080`;特殊的子控制，包含滑块手柄可能移动的区域。
- `QStyle::SC_SpinBoxUp`：`0x00000001`;旋转小部件的提升/增加;参见`QSpinBox`。
- `QStyle::SC_SpinBoxDown`：`0x00000002`;旋转控件向下/减少。
- `QStyle::SC_SpinBoxFrame`：`0x00000004`;旋转控件框架。
- `QStyle::SC_SpinBoxEditField`：`0x00000008`;旋转控件编辑字段。
- `QStyle::SC_ComboBoxEditField`：`0x00000002`;组合盒编辑字段;另见`QComboBox`。
- `QStyle::SC_ComboBoxArrow`：`0x00000004`;组合盒箭头按钮。
- `QStyle::SC_ComboBoxFrame`：`0x00000001`;组合盒框架。
- `QStyle::SC_ComboBoxListBoxPopup`：`0x00000008`;组合盒弹出的参考矩形。用于计算弹出窗口的位置。
- `QStyle::SC_SliderGroove`：`0x00000001`;特殊的子控制，包含滑块手柄可移动的区域。
- `QStyle::SC_SliderHandle`：`0x00000002`;滑块手柄。
- `QStyle::SC_SliderTickmarks`：`0x00000004`;滑块勾选标记。
- `QStyle::SC_ToolButton`：`0x00000001`;工具按钮（另见`QToolButton`）。
- `QStyle::SC_ToolButtonMenu`：`0x00000002`;子控制键，用于在工具按钮中打开弹出菜单。
- `QStyle::SC_TitleBarSysMenu`：`0x00000001`;系统菜单按钮（即恢复、关闭等）。
- `QStyle::SC_TitleBarMinButton`：`0x00000002`;最小化按钮。
- `QStyle::SC_TitleBarMaxButton`：`0x00000004`;最大化按钮。
- `QStyle::SC_TitleBarCloseButton`：`0x00000008`;关闭按钮。
- `QStyle::SC_TitleBarLabel`：`0x00000100`;窗户标题标签。
- `QStyle::SC_TitleBarNormalButton`：`0x00000010`;普通（恢复）按钮。
- `QStyle::SC_TitleBarShadeButton`：`0x00000020`;遮阳按钮。
- `QStyle::SC_TitleBarUnshadeButton`：`0x00000040`;解除着色按钮。
- `QStyle::SC_TitleBarContextHelpButton`：`0x00000080`;上下文帮助按钮。
- `QStyle::SC_DialHandle`：`0x00000002`;旋钮的手柄（即你用来控制旋钮的装置）。
- `QStyle::SC_DialGroove`：`0x00000001`;拨盘槽。
- `QStyle::SC_DialTickmarks`：`0x00000004`;刻度盘的刻度标记。
- `QStyle::SC_GroupBoxFrame`：`0x00000008`;团体盒子的框架。
- `QStyle::SC_GroupBoxLabel`：`0x00000002`;团体盒子的标题。
- `QStyle::SC_GroupBoxCheckBox`：`0x00000001`;组框的可选复选框。
- `QStyle::SC_GroupBoxContents`：`0x00000004`;组内内容。
- `QStyle::SC_MdiNormalButton`：`0x00000002`;菜单栏中MDI子窗口的正常按钮。
- `QStyle::SC_MdiMinButton`：`0x00000001`;菜单栏中MDI子窗口的最小化按钮。
- `QStyle::SC_MdiCloseButton`：`0x00000004`;菜单栏中MDI子窗口的关闭按钮。
- `QStyle::SC_All`：`0xffffffff`;与所有子控制点匹配的特殊值。
SubControls 类型是 QFlags 的 typedef<SubControl>。它存储 SubControl 值的 OR 组合。

### `flags SubControls`

**作用与语义：**

该枚举描述了可用的子控制。子控制是复杂控制（`ComplexControl`）中的控制元素。
- `QStyle::SC_None`：`0x00000000`;与其他子控制组不匹配的特殊值。
- `QStyle::SC_ScrollBarAddLine`：`0x00000001`;滚动条加行（即下/右箭头）;另见`QScrollBar`。
- `QStyle::SC_ScrollBarSubLine`：`0x00000002`;滚动条子行（即上/左箭头）。
- `QStyle::SC_ScrollBarAddPage`：`0x00000004`;滚动条添加页面（即向下页）。
- `QStyle::SC_ScrollBarSubPage`：`0x00000008`;滚动条子页面（即翻页）。
- `QStyle::SC_ScrollBarFirst`：`0x00000010`;卷轴第一行（即主页）。
- `QStyle::SC_ScrollBarLast`：`0x00000020`;滚动条最后一行（即结尾）。
- `QStyle::SC_ScrollBarSlider`：`0x00000040`;滚动条滑块手柄。
- `QStyle::SC_ScrollBarGroove`：`0x00000080`;特殊的子控制，包含滑块手柄可能移动的区域。
- `QStyle::SC_SpinBoxUp`：`0x00000001`;旋转小部件的提升/增加;参见`QSpinBox`。
- `QStyle::SC_SpinBoxDown`：`0x00000002`;旋转控件向下/减少。
- `QStyle::SC_SpinBoxFrame`：`0x00000004`;旋转控件框架。
- `QStyle::SC_SpinBoxEditField`：`0x00000008`;旋转控件编辑字段。
- `QStyle::SC_ComboBoxEditField`：`0x00000002`;组合盒编辑字段;另见`QComboBox`。
- `QStyle::SC_ComboBoxArrow`：`0x00000004`;组合盒箭头按钮。
- `QStyle::SC_ComboBoxFrame`：`0x00000001`;组合盒框架。
- `QStyle::SC_ComboBoxListBoxPopup`：`0x00000008`;组合盒弹出的参考矩形。用于计算弹出窗口的位置。
- `QStyle::SC_SliderGroove`：`0x00000001`;特殊的子控制，包含滑块手柄可移动的区域。
- `QStyle::SC_SliderHandle`：`0x00000002`;滑块手柄。
- `QStyle::SC_SliderTickmarks`：`0x00000004`;滑块勾选标记。
- `QStyle::SC_ToolButton`：`0x00000001`;工具按钮（另见`QToolButton`）。
- `QStyle::SC_ToolButtonMenu`：`0x00000002`;子控制键，用于在工具按钮中打开弹出菜单。
- `QStyle::SC_TitleBarSysMenu`：`0x00000001`;系统菜单按钮（即恢复、关闭等）。
- `QStyle::SC_TitleBarMinButton`：`0x00000002`;最小化按钮。
- `QStyle::SC_TitleBarMaxButton`：`0x00000004`;最大化按钮。
- `QStyle::SC_TitleBarCloseButton`：`0x00000008`;关闭按钮。
- `QStyle::SC_TitleBarLabel`：`0x00000100`;窗户标题标签。
- `QStyle::SC_TitleBarNormalButton`：`0x00000010`;普通（恢复）按钮。
- `QStyle::SC_TitleBarShadeButton`：`0x00000020`;遮阳按钮。
- `QStyle::SC_TitleBarUnshadeButton`：`0x00000040`;解除着色按钮。
- `QStyle::SC_TitleBarContextHelpButton`：`0x00000080`;上下文帮助按钮。
- `QStyle::SC_DialHandle`：`0x00000002`;旋钮的手柄（即你用来控制旋钮的装置）。
- `QStyle::SC_DialGroove`：`0x00000001`;拨盘槽。
- `QStyle::SC_DialTickmarks`：`0x00000004`;刻度盘的刻度标记。
- `QStyle::SC_GroupBoxFrame`：`0x00000008`;团体盒子的框架。
- `QStyle::SC_GroupBoxLabel`：`0x00000002`;团体盒子的标题。
- `QStyle::SC_GroupBoxCheckBox`：`0x00000001`;组框的可选复选框。
- `QStyle::SC_GroupBoxContents`：`0x00000004`;组内内容。
- `QStyle::SC_MdiNormalButton`：`0x00000002`;菜单栏中MDI子窗口的正常按钮。
- `QStyle::SC_MdiMinButton`：`0x00000001`;菜单栏中MDI子窗口的最小化按钮。
- `QStyle::SC_MdiCloseButton`：`0x00000004`;菜单栏中MDI子窗口的关闭按钮。
- `QStyle::SC_All`：`0xffffffff`;与所有子控制点匹配的特殊值。
SubControls 类型是 QFlags 的 typedef<SubControl>。它存储 SubControl 值的 OR 组合。

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

`QStyle` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
