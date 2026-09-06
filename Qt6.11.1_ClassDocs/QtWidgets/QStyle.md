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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 48 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QStyle::ComplexControl`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QStyle` 暴露的类型声明 `Complex、Control`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ComplexControl`。
- 属性名：`QStyle`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QStyle::ContentsType`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QStyle` 暴露的类型声明 `Contents、类型`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ContentsType`。
- 属性名：`QStyle`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QStyle::ControlElement`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QStyle` 暴露的类型声明 `Control、Element`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ControlElement`。
- 属性名：`QStyle`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QStyle::PixelMetric`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QStyle` 暴露的类型声明 `Pixel、Metric`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:PixelMetric`。
- 属性名：`QStyle`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QStyle::PrimitiveElement`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QStyle` 暴露的类型声明 `Primitive、Element`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:PrimitiveElement`。
- 属性名：`QStyle`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QStyle::RequestSoftwareInputPanel`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QStyle` 暴露的类型声明 `请求、Software、Input、Panel`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:RequestSoftwareInputPanel`。
- 属性名：`QStyle`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QStyle::StandardPixmap`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QStyle` 暴露的类型声明 `Standard、Pixmap`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:StandardPixmap`。
- 属性名：`QStyle`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QStyle::StateFlagflags QStyle::State`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QStyle` 暴露的类型声明 `State、Flagflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:StateFlagflags QStyle::State`。
- 属性名：`QStyle`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QStyle::StyleHint`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QStyle` 暴露的类型声明 `Style、Hint`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:StyleHint`。
- 属性名：`QStyle`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QStyle::SubControlflags QStyle::SubControls`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QStyle` 暴露的类型声明 `Sub、Controlflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:SubControlflags QStyle::SubControls`。
- 属性名：`QStyle`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QStyle::SubElement`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QStyle` 暴露的类型声明 `Sub、Element`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:SubElement`。
- 属性名：`QStyle`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStyle::QStyle()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QStyle` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QStyle::~QStyle()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QStyle` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QRect QStyle::alignedRect(Qt::LayoutDirection direction, Qt::Alignment alignment, const QSize &size, const QRect &rectangle)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `alignedRect`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QRect`。
- 参数 `direction`：类型为 `Qt::LayoutDirection`。没有默认值，调用时必须提供。方向枚举，决定排列、遍历或坐标增长方向；要结合该类定义的枚举值判断实际方向。
- 参数 `alignment`：类型为 `Qt::Alignment`。没有默认值，调用时必须提供。对齐标志的组合，例如 `Qt::AlignLeft | Qt::AlignVCenter`；它描述内容在已分配区域中的位置，不负责分配剩余空间。
- 参数 `size`：类型为 `const QSize &`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。
- 参数 `rectangle`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QStyle::combinedLayoutSpacing(QSizePolicy::ControlTypes controls1, QSizePolicy::ControlTypes controls2, Qt::Orientation orientation, QStyleOption *option = nullptr, QWidget *widget = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** `QStyle::combinedLayoutSpacing` 用于计算、查询或取得与“combined、Layout、Spacing”相关的操作。调用时要先确认当前状态和 `controls1`、`controls2`、`orientation`、`option`、`widget` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `controls1`：类型为 `QSizePolicy::ControlTypes`。没有默认值，调用时必须提供。传入 `QSizePolicy::ControlTypes` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `controls2`：类型为 `QSizePolicy::ControlTypes`。没有默认值，调用时必须提供。传入 `QSizePolicy::ControlTypes` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `orientation`：类型为 `Qt::Orientation`。没有默认值，调用时必须提供。传入 `Qt::Orientation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `option`：类型为 `QStyleOption *`。默认值为 `nullptr`。选项或绘制/行为配置对象；调用前确认其中的状态、矩形和样式信息已经初始化。
- 参数 `widget`：类型为 `QWidget *`。默认值为 `nullptr`。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QStyle::drawComplexControl(QStyle::ComplexControl control, const QStyleOptionComplex *option, QPainter *painter, const QWidget *widget = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QStyle` 的核心操作 `drawComplexControl`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `control`：类型为 `QStyle::ComplexControl`。没有默认值，调用时必须提供。传入 `QStyle::ComplexControl` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `option`：类型为 `const QStyleOptionComplex *`。没有默认值，调用时必须提供。选项或绘制/行为配置对象；调用前确认其中的状态、矩形和样式信息已经初始化。
- 参数 `painter`：类型为 `QPainter *`。没有默认值，调用时必须提供。绘制上下文。要确认它已经绑定有效绘制设备，并处于允许绘制的阶段。
- 参数 `widget`：类型为 `const QWidget *`。默认值为 `nullptr`。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QStyle::drawControl(QStyle::ControlElement element, const QStyleOption *option, QPainter *painter, const QWidget *widget = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QStyle` 的核心操作 `drawControl`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `element`：类型为 `QStyle::ControlElement`。没有默认值，调用时必须提供。传入 `QStyle::ControlElement` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `option`：类型为 `const QStyleOption *`。没有默认值，调用时必须提供。选项或绘制/行为配置对象；调用前确认其中的状态、矩形和样式信息已经初始化。
- 参数 `painter`：类型为 `QPainter *`。没有默认值，调用时必须提供。绘制上下文。要确认它已经绑定有效绘制设备，并处于允许绘制的阶段。
- 参数 `widget`：类型为 `const QWidget *`。默认值为 `nullptr`。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] void QStyle::drawItemPixmap(QPainter *painter, const QRect &rectangle, int alignment, const QPixmap &pixmap) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QStyle` 的核心操作 `drawItemPixmap`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `painter`：类型为 `QPainter *`。没有默认值，调用时必须提供。绘制上下文。要确认它已经绑定有效绘制设备，并处于允许绘制的阶段。
- 参数 `rectangle`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `alignment`：类型为 `int`。没有默认值，调用时必须提供。对齐标志的组合，例如 `Qt::AlignLeft | Qt::AlignVCenter`；它描述内容在已分配区域中的位置，不负责分配剩余空间。
- 参数 `pixmap`：类型为 `const QPixmap &`。没有默认值，调用时必须提供。传入 `const QPixmap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] void QStyle::drawItemText(QPainter *painter, const QRect &rectangle, int alignment, const QPalette &palette, bool enabled, const QString &text, QPalette::ColorRole textRole = QPalette::NoRole) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QStyle` 的核心操作 `drawItemText`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `painter`：类型为 `QPainter *`。没有默认值，调用时必须提供。绘制上下文。要确认它已经绑定有效绘制设备，并处于允许绘制的阶段。
- 参数 `rectangle`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `alignment`：类型为 `int`。没有默认值，调用时必须提供。对齐标志的组合，例如 `Qt::AlignLeft | Qt::AlignVCenter`；它描述内容在已分配区域中的位置，不负责分配剩余空间。
- 参数 `palette`：类型为 `const QPalette &`。没有默认值，调用时必须提供。传入 `const QPalette &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `enabled`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `textRole`：类型为 `QPalette::ColorRole`。默认值为 `QPalette::NoRole`。传入 `QPalette::ColorRole` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QStyle::drawPrimitive(QStyle::PrimitiveElement element, const QStyleOption *option, QPainter *painter, const QWidget *widget = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QStyle` 的核心操作 `drawPrimitive`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `element`：类型为 `QStyle::PrimitiveElement`。没有默认值，调用时必须提供。传入 `QStyle::PrimitiveElement` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `option`：类型为 `const QStyleOption *`。没有默认值，调用时必须提供。选项或绘制/行为配置对象；调用前确认其中的状态、矩形和样式信息已经初始化。
- 参数 `painter`：类型为 `QPainter *`。没有默认值，调用时必须提供。绘制上下文。要确认它已经绑定有效绘制设备，并处于允许绘制的阶段。
- 参数 `widget`：类型为 `const QWidget *`。默认值为 `nullptr`。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QPixmap QStyle::generatedIconPixmap(QIcon::Mode iconMode, const QPixmap &pixmap, const QStyleOption *option) const`

**API 类别：** 成员函数说明

**中文解读：** `QStyle::generatedIconPixmap` 用于计算、查询或取得与“generated、Icon、Pixmap”相关的操作。调用时要先确认当前状态和 `iconMode`、`pixmap`、`option` 的有效范围；返回类型是 `QPixmap`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPixmap`。
- 参数 `iconMode`：类型为 `QIcon::Mode`。没有默认值，调用时必须提供。传入 `QIcon::Mode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pixmap`：类型为 `const QPixmap &`。没有默认值，调用时必须提供。传入 `const QPixmap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `option`：类型为 `const QStyleOption *`。没有默认值，调用时必须提供。选项或绘制/行为配置对象；调用前确认其中的状态、矩形和样式信息已经初始化。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QStyle::SubControl QStyle::hitTestComplexControl(QStyle::ComplexControl control, const QStyleOptionComplex *option, const QPoint &position, const QWidget *widget = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** `QStyle::hitTestComplexControl` 用于计算、查询或取得与“hit、Test、Complex、Control”相关的操作。调用时要先确认当前状态和 `control`、`option`、`position`、`widget` 的有效范围；返回类型是 `QStyle::SubControl`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStyle::SubControl`。
- 参数 `control`：类型为 `QStyle::ComplexControl`。没有默认值，调用时必须提供。传入 `QStyle::ComplexControl` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `option`：类型为 `const QStyleOptionComplex *`。没有默认值，调用时必须提供。选项或绘制/行为配置对象；调用前确认其中的状态、矩形和样式信息已经初始化。
- 参数 `position`：类型为 `const QPoint &`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `widget`：类型为 `const QWidget *`。默认值为 `nullptr`。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QRect QStyle::itemPixmapRect(const QRect &rectangle, int alignment, const QPixmap &pixmap) const`

**API 类别：** 成员函数说明

**中文解读：** `QStyle::itemPixmapRect` 用于计算、查询或取得与“项目访问、Pixmap、Rect”相关的操作。调用时要先确认当前状态和 `rectangle`、`alignment`、`pixmap` 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数 `rectangle`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `alignment`：类型为 `int`。没有默认值，调用时必须提供。对齐标志的组合，例如 `Qt::AlignLeft | Qt::AlignVCenter`；它描述内容在已分配区域中的位置，不负责分配剩余空间。
- 参数 `pixmap`：类型为 `const QPixmap &`。没有默认值，调用时必须提供。传入 `const QPixmap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QRect QStyle::itemTextRect(const QFontMetrics &metrics, const QRect &rectangle, int alignment, bool enabled, const QString &text) const`

**API 类别：** 成员函数说明

**中文解读：** `QStyle::itemTextRect` 用于计算、查询或取得与“项目访问、文本、Rect”相关的操作。调用时要先确认当前状态和 `metrics`、`rectangle`、`alignment`、`enabled`、`text` 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数 `metrics`：类型为 `const QFontMetrics &`。没有默认值，调用时必须提供。传入 `const QFontMetrics &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `rectangle`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `alignment`：类型为 `int`。没有默认值，调用时必须提供。对齐标志的组合，例如 `Qt::AlignLeft | Qt::AlignVCenter`；它描述内容在已分配区域中的位置，不负责分配剩余空间。
- 参数 `enabled`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] int QStyle::layoutSpacing(QSizePolicy::ControlType control1, QSizePolicy::ControlType control2, Qt::Orientation orientation, const QStyleOption *option = nullptr, const QWidget *widget = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** `QStyle::layoutSpacing` 用于计算、查询或取得与“layout、Spacing”相关的操作。调用时要先确认当前状态和 `control1`、`control2`、`orientation`、`option`、`widget` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `control1`：类型为 `QSizePolicy::ControlType`。没有默认值，调用时必须提供。传入 `QSizePolicy::ControlType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `control2`：类型为 `QSizePolicy::ControlType`。没有默认值，调用时必须提供。传入 `QSizePolicy::ControlType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `orientation`：类型为 `Qt::Orientation`。没有默认值，调用时必须提供。传入 `Qt::Orientation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `option`：类型为 `const QStyleOption *`。默认值为 `nullptr`。选项或绘制/行为配置对象；调用前确认其中的状态、矩形和样式信息已经初始化。
- 参数 `widget`：类型为 `const QWidget *`。默认值为 `nullptr`。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] QString QStyle::name() const`

**API 类别：** 成员函数说明

**中文解读：** `QStyle::name` 用于计算、查询或取得与“名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] int QStyle::pixelMetric(QStyle::PixelMetric metric, const QStyleOption *option = nullptr, const QWidget *widget = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** `QStyle::pixelMetric` 用于计算、查询或取得与“pixel、Metric”相关的操作。调用时要先确认当前状态和 `metric`、`option`、`widget` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `metric`：类型为 `QStyle::PixelMetric`。没有默认值，调用时必须提供。传入 `QStyle::PixelMetric` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `option`：类型为 `const QStyleOption *`。默认值为 `nullptr`。选项或绘制/行为配置对象；调用前确认其中的状态、矩形和样式信息已经初始化。
- 参数 `widget`：类型为 `const QWidget *`。默认值为 `nullptr`。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] void QStyle::polish(QWidget *widget)`

**API 类别：** 成员函数说明

**中文解读：** `QStyle::polish` 用于执行与“polish”相关的操作。调用时要先确认当前状态和 `widget` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `widget`：类型为 `QWidget *`。没有默认值，调用时必须提供。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] void QStyle::polish(QApplication *application)`

**API 类别：** 成员函数说明

**中文解读：** `QStyle::polish` 用于执行与“polish”相关的操作。调用时要先确认当前状态和 `application` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `application`：类型为 `QApplication *`。没有默认值，调用时必须提供。传入 `QApplication *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] void QStyle::polish(QPalette &palette)`

**API 类别：** 成员函数说明

**中文解读：** `QStyle::polish` 用于执行与“polish”相关的操作。调用时要先确认当前状态和 `palette` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `palette`：类型为 `QPalette &`。没有默认值，调用时必须提供。传入 `QPalette &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QStyle *QStyle::proxy() const`

**API 类别：** 成员函数说明

**中文解读：** `QStyle::proxy` 用于计算、查询或取得与“proxy”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QStyle *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QStyle *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QSize QStyle::sizeFromContents(QStyle::ContentsType type, const QStyleOption *option, const QSize &contentsSize, const QWidget *widget = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** `QStyle::sizeFromContents` 用于计算、查询或取得与“尺寸或数量、转换进入、Contents”相关的操作。调用时要先确认当前状态和 `type`、`option`、`contentsSize`、`widget` 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数 `type`：类型为 `QStyle::ContentsType`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `option`：类型为 `const QStyleOption *`。没有默认值，调用时必须提供。选项或绘制/行为配置对象；调用前确认其中的状态、矩形和样式信息已经初始化。
- 参数 `contentsSize`：类型为 `const QSize &`。没有默认值，调用时必须提供。传入 `const QSize &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `widget`：类型为 `const QWidget *`。默认值为 `nullptr`。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] int QStyle::sliderPositionFromValue(int min, int max, int logicalValue, int span, bool upsideDown = false)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `sliderPositionFromValue`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`int`。
- 参数 `min`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `max`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `logicalValue`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `span`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `upsideDown`：类型为 `bool`。默认值为 `false`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] int QStyle::sliderValueFromPosition(int min, int max, int position, int span, bool upsideDown = false)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `sliderValueFromPosition`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`int`。
- 参数 `min`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `max`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `position`：类型为 `int`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `span`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `upsideDown`：类型为 `bool`。默认值为 `false`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QIcon QStyle::standardIcon(QStyle::StandardPixmap standardIcon, const QStyleOption *option = nullptr, const QWidget *widget = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** `QStyle::standardIcon` 用于计算、查询或取得与“standard、Icon”相关的操作。调用时要先确认当前状态和 `standardIcon`、`option`、`widget` 的有效范围；返回类型是 `QIcon`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QIcon`。
- 参数 `standardIcon`：类型为 `QStyle::StandardPixmap`。没有默认值，调用时必须提供。传入 `QStyle::StandardPixmap` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `option`：类型为 `const QStyleOption *`。默认值为 `nullptr`。选项或绘制/行为配置对象；调用前确认其中的状态、矩形和样式信息已经初始化。
- 参数 `widget`：类型为 `const QWidget *`。默认值为 `nullptr`。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QPalette QStyle::standardPalette() const`

**API 类别：** 成员函数说明

**中文解读：** `QStyle::standardPalette` 用于计算、查询或取得与“standard、Palette”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPalette`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPalette`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] int QStyle::styleHint(QStyle::StyleHint hint, const QStyleOption *option = nullptr, const QWidget *widget = nullptr, QStyleHintReturn *returnData = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** `QStyle::styleHint` 用于计算、查询或取得与“style、Hint”相关的操作。调用时要先确认当前状态和 `hint`、`option`、`widget`、`returnData` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `hint`：类型为 `QStyle::StyleHint`。没有默认值，调用时必须提供。传入 `QStyle::StyleHint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `option`：类型为 `const QStyleOption *`。默认值为 `nullptr`。选项或绘制/行为配置对象；调用前确认其中的状态、矩形和样式信息已经初始化。
- 参数 `widget`：类型为 `const QWidget *`。默认值为 `nullptr`。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。
- 参数 `returnData`：类型为 `QStyleHintReturn *`。默认值为 `nullptr`。传入 `QStyleHintReturn *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QRect QStyle::subControlRect(QStyle::ComplexControl control, const QStyleOptionComplex *option, QStyle::SubControl subControl, const QWidget *widget = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** `QStyle::subControlRect` 用于计算、查询或取得与“sub、Control、Rect”相关的操作。调用时要先确认当前状态和 `control`、`option`、`subControl`、`widget` 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数 `control`：类型为 `QStyle::ComplexControl`。没有默认值，调用时必须提供。传入 `QStyle::ComplexControl` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `option`：类型为 `const QStyleOptionComplex *`。没有默认值，调用时必须提供。选项或绘制/行为配置对象；调用前确认其中的状态、矩形和样式信息已经初始化。
- 参数 `subControl`：类型为 `QStyle::SubControl`。没有默认值，调用时必须提供。传入 `QStyle::SubControl` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `widget`：类型为 `const QWidget *`。默认值为 `nullptr`。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QRect QStyle::subElementRect(QStyle::SubElement element, const QStyleOption *option, const QWidget *widget = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** `QStyle::subElementRect` 用于计算、查询或取得与“sub、Element、Rect”相关的操作。调用时要先确认当前状态和 `element`、`option`、`widget` 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数 `element`：类型为 `QStyle::SubElement`。没有默认值，调用时必须提供。传入 `QStyle::SubElement` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `option`：类型为 `const QStyleOption *`。没有默认值，调用时必须提供。选项或绘制/行为配置对象；调用前确认其中的状态、矩形和样式信息已经初始化。
- 参数 `widget`：类型为 `const QWidget *`。默认值为 `nullptr`。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] void QStyle::unpolish(QWidget *widget)`

**API 类别：** 成员函数说明

**中文解读：** `QStyle::unpolish` 用于执行与“unpolish”相关的操作。调用时要先确认当前状态和 `widget` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `widget`：类型为 `QWidget *`。没有默认值，调用时必须提供。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] void QStyle::unpolish(QApplication *application)`

**API 类别：** 成员函数说明

**中文解读：** `QStyle::unpolish` 用于执行与“unpolish”相关的操作。调用时要先确认当前状态和 `application` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `application`：类型为 `QApplication *`。没有默认值，调用时必须提供。传入 `QApplication *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] Qt::Alignment QStyle::visualAlignment(Qt::LayoutDirection direction, Qt::Alignment alignment)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `visualAlignment`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`Qt::Alignment`。
- 参数 `direction`：类型为 `Qt::LayoutDirection`。没有默认值，调用时必须提供。方向枚举，决定排列、遍历或坐标增长方向；要结合该类定义的枚举值判断实际方向。
- 参数 `alignment`：类型为 `Qt::Alignment`。没有默认值，调用时必须提供。对齐标志的组合，例如 `Qt::AlignLeft | Qt::AlignVCenter`；它描述内容在已分配区域中的位置，不负责分配剩余空间。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QPoint QStyle::visualPos(Qt::LayoutDirection direction, const QRect &boundingRectangle, const QPoint &logicalPosition)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `visualPos`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QPoint`。
- 参数 `direction`：类型为 `Qt::LayoutDirection`。没有默认值，调用时必须提供。方向枚举，决定排列、遍历或坐标增长方向；要结合该类定义的枚举值判断实际方向。
- 参数 `boundingRectangle`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `logicalPosition`：类型为 `const QPoint &`。没有默认值，调用时必须提供。传入 `const QPoint &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QRect QStyle::visualRect(Qt::LayoutDirection direction, const QRect &boundingRectangle, const QRect &logicalRectangle)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `visualRect`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QRect`。
- 参数 `direction`：类型为 `Qt::LayoutDirection`。没有默认值，调用时必须提供。方向枚举，决定排列、遍历或坐标增长方向；要结合该类定义的枚举值判断实际方向。
- 参数 `boundingRectangle`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `logicalRectangle`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags State`

**API 类别：** 公有类型

**中文解读：** 这是 `QStyle` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum StateFlag { State_None, State_Active, State_AutoRaise, State_Children, State_DownArrow, …, State_Small }`

**API 类别：** 公有类型

**中文解读：** 这是 `QStyle` 暴露的类型声明 `State、Flag`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum SubControl { SC_None, SC_ScrollBarAddLine, SC_ScrollBarSubLine, SC_ScrollBarAddPage, SC_ScrollBarSubPage, …, SC_All }`

**API 类别：** 公有类型

**中文解读：** 这是 `QStyle` 暴露的类型声明 `Sub、Control`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags SubControls`

**API 类别：** 公有类型

**中文解读：** 这是 `QStyle` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
