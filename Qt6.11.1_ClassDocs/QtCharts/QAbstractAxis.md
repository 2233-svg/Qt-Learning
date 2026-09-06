# QAbstractAxis

> Qt 6.11.1 · Qt Charts

## 1. 先建立直觉

**一句话定位：** `QAbstractAxis` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Charts 提供折线、柱状、饼图、散点图和坐标轴等数据可视化组件。

### 这是什么

`QAbstractAxis` 是 Qt Charts 中的抽象协议类型，通常通过具体子类、模型、插件或工厂来使用。

**内部模型：** 抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

**适用场景：** 当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。

**典型调用链：** 选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

**先记住的坑：** 不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

## 2. 依赖与对象关系

- 头文件：`#include <QAbstractAxis>`
- 继承自：QObject
- 直接派生类：QBarCategoryAxis、QColorAxis、QDateTimeAxis、QLogValueAxis,、QValueAxis

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

### 状态、生命周期和线程

**生命周期：** 先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

**状态与结果：** QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

**线程与事件循环：** QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

## 3. 直接使用

当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。 使用时通常按这个过程组织：选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum AxisType { AxisTypeNoAxis, AxisTypeValue, AxisTypeBarCategory, AxisTypeCategory, AxisTypeDateTime, …, AxisTypeColor }`
- `flags AxisTypes`

### 属性

- `alignment : Qt::Alignment`
- `color : QColor`
- `gridLineColor : QColor`
- `gridLinePen : QPen`
- `gridVisible : bool`
- `labelsAngle : int`
- `labelsBrush : QBrush`
- `labelsColor : QColor`
- `labelsFont : QFont`
- `labelsTruncated : bool`
- `labelsVisible : bool`
- `linePen : QPen`
- `lineVisible : bool`
- `minorGridLineColor : QColor`
- `minorGridLinePen : QPen`
- `minorGridVisible : bool`
- `orientation : Qt::Orientation`
- `reverse : bool`
- `shadesBorderColor : QColor`
- `shadesBrush : QBrush`
- `shadesColor : QColor`
- `shadesPen : QPen`
- `shadesVisible : bool`
- `titleBrush : QBrush`
- `titleFont : QFont`
- `titleText : QString`
- `titleVisible : bool`
- `truncateLabels : bool`
- `visible : bool`

### 公有函数

- `virtual ~QAbstractAxis()`
- `Qt::Alignment alignment() const`
- `QColor gridLineColor()`
- `QPen gridLinePen() const`
- `void hide()`
- `bool isGridLineVisible() const`
- `bool isLineVisible() const`
- `bool isMinorGridLineVisible() const`
- `bool isReverse() const`
- `bool isTitleVisible() const`
- `bool isVisible() const`
- `int labelsAngle() const`
- `QBrush labelsBrush() const`
- `QColor labelsColor() const`
- `bool labelsEditable() const`
- `QFont labelsFont() const`
- `bool labelsTruncated() const`
- `bool labelsVisible() const`
- `QPen linePen() const`
- `QColor linePenColor() const`
- `QColor minorGridLineColor()`
- `QPen minorGridLinePen() const`
- `Qt::Orientation orientation() const`
- `void setGridLineColor(const QColor &color)`
- `void setGridLinePen(const QPen &pen)`
- `void setGridLineVisible(bool visible = true)`
- `void setLabelsAngle(int angle)`
- `void setLabelsBrush(const QBrush &brush)`
- `void setLabelsColor(QColor color)`
- `void setLabelsEditable(bool editable = true)`
- `void setLabelsFont(const QFont &font)`
- `void setLabelsVisible(bool visible = true)`
- `void setLinePen(const QPen &pen)`
- `void setLinePenColor(QColor color)`
- `void setLineVisible(bool visible = true)`
- `void setMax(const QVariant &max)`
- `void setMin(const QVariant &min)`
- `void setMinorGridLineColor(const QColor &color)`
- `void setMinorGridLinePen(const QPen &pen)`
- `void setMinorGridLineVisible(bool visible = true)`
- `void setRange(const QVariant &min, const QVariant &max)`
- `void setReverse(bool reverse = true)`
- `void setShadesBorderColor(QColor color)`
- `void setShadesBrush(const QBrush &brush)`
- `void setShadesColor(QColor color)`
- `void setShadesPen(const QPen &pen)`
- `void setShadesVisible(bool visible = true)`
- `void setTitleBrush(const QBrush &brush)`
- `void setTitleFont(const QFont &font)`
- `void setTitleText(const QString &title)`
- `void setTitleVisible(bool visible = true)`
- `void setTruncateLabels(bool truncateLabels = true)`
- `void setVisible(bool visible = true)`
- `QColor shadesBorderColor() const`
- `QBrush shadesBrush() const`
- `QColor shadesColor() const`
- `QPen shadesPen() const`
- `bool shadesVisible() const`
- `void show()`
- `QBrush titleBrush() const`
- `QFont titleFont() const`
- `QString titleText() const`
- `bool truncateLabels() const`
- `virtual QAbstractAxis::AxisType type() const = 0`

### 信号

- `void colorChanged(QColor color)`
- `void gridLineColorChanged(const QColor &color)`
- `void gridLinePenChanged(const QPen &pen)`
- `void gridVisibleChanged(bool visible)`
- `void labelsAngleChanged(int angle)`
- `void labelsBrushChanged(const QBrush &brush)`
- `void labelsColorChanged(QColor color)`
- `void labelsEditableChanged(bool editable)`
- `void labelsFontChanged(const QFont &font)`
- `(since 6.2) void labelsTruncatedChanged(bool labelsTruncated)`
- `void labelsVisibleChanged(bool visible)`
- `void linePenChanged(const QPen &pen)`
- `void lineVisibleChanged(bool visible)`
- `void minorGridLineColorChanged(const QColor &color)`
- `void minorGridLinePenChanged(const QPen &pen)`
- `void minorGridVisibleChanged(bool visible)`
- `void reverseChanged(bool reverse)`
- `void shadesBorderColorChanged(QColor color)`
- `void shadesBrushChanged(const QBrush &brush)`
- `void shadesColorChanged(QColor color)`
- `void shadesPenChanged(const QPen &pen)`
- `void shadesVisibleChanged(bool visible)`
- `void titleBrushChanged(const QBrush &brush)`
- `void titleFontChanged(const QFont &font)`
- `void titleTextChanged(const QString &text)`
- `void titleVisibleChanged(bool visible)`
- `(since 6.2) void truncateLabelsChanged(bool truncateLabels)`
- `void visibleChanged(bool visible)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QAbstractAxis::AxisTypeflags QAbstractAxis::AxisTypes`

**作用与语义：**

该枚举类型指定轴对象的类型。
- `QAbstractAxis::AxisTypeNoAxis`：`0x0`
- `QAbstractAxis::AxisTypeValue`：`0x1`
- `QAbstractAxis::AxisTypeBarCategory`：`0x2`
- `QAbstractAxis::AxisTypeCategory`：`0x4`
- `QAbstractAxis::AxisTypeDateTime`：`0x8`
- `QAbstractAxis::AxisTypeLogValue`：`0x10`
- `QAbstractAxis::AxisTypeColor`：`0x20`
AxisTypes 类型是 QFlags 的 typedef<AxisType>。它存储 AxisType 值的 OR 组合。

### `[read-only] alignment : Qt::Alignment`

**作用与语义：**

该属性表示轴的对齐。
可以是`Qt::AlignLeft`、`Qt::AlignRight`、`Qt::AlignBottom`或`Qt::AlignTop`。

**如何使用：** 调用 `alignment()` 读取当前值；它不会修改应用状态。

### `color : QColor`

**作用与语义：**

该属性包含轴和刻度标记的颜色。

**如何使用：** 调用 `color()` 读取当前值；它不会修改应用状态。

### `gridLineColor : QColor`

**作用与语义：**

该属性表示网格线的颜色。

**如何使用：** 调用 `gridLineColor()` 读取当前值；它不会修改应用状态。

### `gridLinePen : QPen`

**作用与语义：**

该属性决定了绘制网格线的笔。

**如何使用：** 调用 `gridLinePen()` 读取当前值；它不会修改应用状态。

### `gridVisible : bool`

**作用与语义：**

该特性保持网格线的可见性。

**如何使用：** 调用 `gridVisible()` 读取当前值；它不会修改应用状态。

### `labelsAngle : int`

**作用与语义：**

该属性表示轴标签的角度以度为单位。

**如何使用：** 调用 `labelsAngle()` 读取当前值；它不会修改应用状态。

### `labelsBrush : QBrush`

**作用与语义：**

该属性包含用于绘制标签的画刷。
只有画笔的颜色才相关。

**如何使用：** 调用 `labelsBrush()` 读取当前值；它不会修改应用状态。

### `labelsColor : QColor`

**作用与语义：**

该属性表示轴标签的颜色。

**如何使用：** 调用 `labelsColor()` 读取当前值；它不会修改应用状态。

### `labelsFont : QFont`

**作用与语义：**

该属性包含轴标签的字体。

**如何使用：** 调用 `labelsFont()` 读取当前值；它不会修改应用状态。

### `[read-only] labelsTruncated : bool`

**作用与语义：**

如果轴上至少有一个标签被截断，返回`true`。
在轴线显示之前，返回的值不会准确。

**如何使用：** 调用 `labelsTruncated()` 读取当前值；它不会修改应用状态。

### `labelsVisible : bool`

**作用与语义：**

该属性适用于轴标签是否可见。

**如何使用：** 调用 `labelsVisible()` 读取当前值；它不会修改应用状态。

### `linePen : QPen`

**作用与语义：**

该属性决定了用来划线的笔。

**如何使用：** 调用 `linePen()` 读取当前值；它不会修改应用状态。

### `lineVisible : bool`

**作用与语义：**

该属性决定了轴线的可见性。

**如何使用：** 调用 `lineVisible()` 读取当前值；它不会修改应用状态。

### `minorGridLineColor : QColor`

**作用与语义：**

该属性表示小网格线的颜色。
仅适用于支持次要网格线的轴线。

**如何使用：** 调用 `minorGridLineColor()` 读取当前值；它不会修改应用状态。

### `minorGridLinePen : QPen`

**作用与语义：**

该属性决定了绘制次要网格线的笔。
仅适用于支持次要网格线的轴线。

**如何使用：** 调用 `minorGridLinePen()` 读取当前值；它不会修改应用状态。

### `minorGridVisible : bool`

**作用与语义：**

该特性保留了次要网格线的可见性。
仅适用于支持次要网格线的轴线。

**如何使用：** 调用 `minorGridVisible()` 读取当前值；它不会修改应用状态。

### `[read-only] orientation : Qt::Orientation`

**作用与语义：**

该属性决定了轴的方向。
在图表中添加轴时，固定在`Qt::Horizontal`或`Qt::Vertical`。

**如何使用：** 调用 `orientation()` 读取当前值；它不会修改应用状态。

### `reverse : bool`

**作用与语义：**

该属性在使用反向轴时成立。
默认情况下，数值为`false`。
反向轴由线、样条和散点系列以及带有笛卡尔图的面积系列支持。所有连接同一系列的同方向轴，如果其中一个轴被反转或行为未定义，必须反转。

**如何使用：** 调用 `reverse()` 读取当前值；它不会修改应用状态。

### `shadesBorderColor : QColor`

**作用与语义：**

该属性表示轴阴影的边框（笔）颜色。

**如何使用：** 调用 `shadesBorderColor()` 读取当前值；它不会修改应用状态。

### `shadesBrush : QBrush`

**作用与语义：**

该属性包含用于绘制轴阴影（网格线之间的区域）的画笔。

**如何使用：** 调用 `shadesBrush()` 读取当前值；它不会修改应用状态。

### `shadesColor : QColor`

**作用与语义：**

该属性表示轴阴影的填充（画刷）颜色。

**如何使用：** 调用 `shadesColor()` 读取当前值；它不会修改应用状态。

### `shadesPen : QPen`

**作用与语义：**

该属性包含用于绘制轴阴影（网格线之间的区域）的笔。

**如何使用：** 调用 `shadesPen()` 读取当前值；它不会修改应用状态。

### `shadesVisible : bool`

**作用与语义：**

该属性表示轴阴影的可见性。

**如何使用：** 调用 `shadesVisible()` 读取当前值；它不会修改应用状态。

### `titleBrush : QBrush`

**作用与语义：**

该属性保留用于绘制标题文字的画笔。
只有画笔的颜色才相关。

**如何使用：** 调用 `titleBrush()` 读取当前值；它不会修改应用状态。

### `titleFont : QFont`

**作用与语义：**

该属性包含了轴标题的字体。

**如何使用：** 调用 `titleFont()` 读取当前值；它不会修改应用状态。

### `titleText : QString`

**作用与语义：**

该属性即为轴的名称。
默认为空。轴心标题支持HTML格式化。

**如何使用：** 调用 `titleText()` 读取当前值；它不会修改应用状态。

### `titleVisible : bool`

**作用与语义：**

该属性保留了轴线名称的可见性。
默认情况下，数值是`true`。

**如何使用：** 调用 `titleVisible()` 读取当前值；它不会修改应用状态。

### `truncateLabels : bool`

**作用与语义：**

该属性表示标签的截断状态。
表示如果全文空间不足，标签是否应被截断。默认等同于`true`。

**如何使用：** 调用 `truncateLabels()` 读取当前值；它不会修改应用状态。

### `visible : bool`

**作用与语义：**

该属性表示轴的可见性。

**如何使用：** 调用 `visible()` 读取当前值；它不会修改应用状态。

### `[virtual noexcept] QAbstractAxis::~QAbstractAxis()`

**作用与语义：**

销毁轴对象。当轴被添加到图表中时，图表对象获得所有权。

### `[signal] void QAbstractAxis::colorChanged(QColor color)`

**作用与语义：**

该属性包含轴和刻度标记的颜色。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `color` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QAbstractAxis::gridLineColorChanged(const QColor &color)`

**作用与语义：**

该属性表示网格线的颜色。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `gridLineColor` 的变化，不要把它当作普通函数主动调用。

### `QPen QAbstractAxis::gridLinePen() const`

**作用与语义：**

返回用于绘制网格的笔。
注意：属性gridLinePen的获取函数。

### `[signal] void QAbstractAxis::gridLinePenChanged(const QPen &pen)`

**作用与语义：**

该属性决定了绘制网格线的笔。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `gridLinePen` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QAbstractAxis::gridVisibleChanged(bool visible)`

**作用与语义：**

该特性保持网格线的可见性。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `gridVisible` 的变化，不要把它当作普通函数主动调用。

### `void QAbstractAxis::hide()`

**作用与语义：**

让轴线、阴影、标签和网格线都不可见。

### `[signal] void QAbstractAxis::labelsAngleChanged(int angle)`

**作用与语义：**

该属性表示轴标签的角度以度为单位。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `labelsAngle` 的变化，不要把它当作普通函数主动调用。

### `QBrush QAbstractAxis::labelsBrush() const`

**作用与语义：**

还原用于绘制标签的画笔。
注意：property labelsBrush 的获取函数。

### `[signal] void QAbstractAxis::labelsBrushChanged(const QBrush &brush)`

**作用与语义：**

该属性包含用于绘制标签的画刷。
只有画笔的颜色才相关。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `labelsBrush` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QAbstractAxis::labelsColorChanged(QColor color)`

**作用与语义：**

该属性表示轴标签的颜色。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `labelsColor` 的变化，不要把它当作普通函数主动调用。

### `bool QAbstractAxis::labelsEditable() const`

**作用与语义：**

如果轴标签可编辑，返回`true`。

### `[signal] void QAbstractAxis::labelsEditableChanged(bool editable)`

**作用与语义：**

当标签的`editable`状态发生变化时，会发出该信号。

### `QFont QAbstractAxis::labelsFont() const`

**作用与语义：**

返回用于绘制标签的字体。
注意：属性labelsFont的Getter函数。

### `[signal] void QAbstractAxis::labelsFontChanged(const QFont &font)`

**作用与语义：**

该属性包含轴标签的字体。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `labelsFont` 的变化，不要把它当作普通函数主动调用。

### `[signal, since 6.2] void QAbstractAxis::labelsTruncatedChanged(bool labelsTruncated)`

**作用与语义：**

如果轴上至少有一个标签被截断，返回`true`。
在轴线显示之前，返回的值不会准确。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `labelsTruncated` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QAbstractAxis::labelsVisibleChanged(bool visible)`

**作用与语义：**

该属性适用于轴标签是否可见。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `labelsVisible` 的变化，不要把它当作普通函数主动调用。

### `QPen QAbstractAxis::linePen() const`

**作用与语义：**

返回用于绘制轴线和刻度标记的笔。
注意：属性线笔的获取函数。

### `[signal] void QAbstractAxis::linePenChanged(const QPen &pen)`

**作用与语义：**

该属性决定了用来划线的笔。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `linePen` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QAbstractAxis::lineVisibleChanged(bool visible)`

**作用与语义：**

该属性决定了轴线的可见性。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `lineVisible` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QAbstractAxis::minorGridLineColorChanged(const QColor &color)`

**作用与语义：**

该属性表示小网格线的颜色。
仅适用于支持次要网格线的轴线。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `minorGridLineColor` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QAbstractAxis::minorGridLinePenChanged(const QPen &pen)`

**作用与语义：**

该属性决定了绘制次要网格线的笔。
仅适用于支持次要网格线的轴线。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `minorGridLinePen` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QAbstractAxis::minorGridVisibleChanged(bool visible)`

**作用与语义：**

该特性保留了次要网格线的可见性。
仅适用于支持次要网格线的轴线。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `minorGridVisible` 的变化，不要把它当作普通函数主动调用。

### `Qt::Orientation QAbstractAxis::orientation() const`

**作用与语义：**

返回轴的方向（垂直或水平）。
注意：属性方向的Getter函数。

### `void QAbstractAxis::setGridLinePen(const QPen &pen)`

**作用与语义：**

该属性决定了绘制网格线的笔。

**如何使用：** 调用 `setGridLinePen(...)` 修改 `gridLinePen`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QAbstractAxis::setLabelsBrush(const QBrush &brush)`

**作用与语义：**

该属性包含用于绘制标签的画刷。
只有画笔的颜色才相关。

**如何使用：** 调用 `setLabelsBrush(...)` 修改 `labelsBrush`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QAbstractAxis::setLabelsEditable(bool editable = true)`

**作用与语义：**

将轴标签可编辑性设置为`editable`。
当标签可编辑时，用户可以通过编辑任意标签方便地更改轴的范围。此功能仅支持`QValueAxis`和`QDateTimeAxis`。
默认情况下，标签是不可编辑的。

### `void QAbstractAxis::setLabelsFont(const QFont &font)`

**作用与语义：**

该属性包含轴标签的字体。

**如何使用：** 调用 `setLabelsFont(...)` 修改 `labelsFont`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QAbstractAxis::setLinePen(const QPen &pen)`

**作用与语义：**

该属性决定了用来划线的笔。

**如何使用：** 调用 `setLinePen(...)` 修改 `linePen`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QAbstractAxis::setLineVisible(bool visible = true)`

**作用与语义：**

该属性决定了轴线的可见性。

**如何使用：** 调用 `setLineVisible(...)` 修改 `lineVisible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QAbstractAxis::setMax(const QVariant &max)`

**作用与语义：**

设置轴上显示的最大值。根据实际轴类型，`max`参数会转换为相应类型的值。如果无法转换，函数调用无效。

### `void QAbstractAxis::setMin(const QVariant &min)`

**作用与语义：**

设置轴上显示的最小值。根据实际轴类型，`min`参数会转换为相应类型的值。如果无法转换，函数调用则无效。

### `void QAbstractAxis::setRange(const QVariant &min, const QVariant &max)`

**作用与语义：**

设置轴上显示的范围。根据实际轴类型，`min`和`max`参数会转换为合适的值类型。如果无法转换，函数调用则无效。

### `void QAbstractAxis::setShadesBrush(const QBrush &brush)`

**作用与语义：**

该属性包含用于绘制轴阴影（网格线之间的区域）的画笔。

**如何使用：** 调用 `setShadesBrush(...)` 修改 `shadesBrush`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QAbstractAxis::setShadesPen(const QPen &pen)`

**作用与语义：**

该属性包含用于绘制轴阴影（网格线之间的区域）的笔。

**如何使用：** 调用 `setShadesPen(...)` 修改 `shadesPen`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QAbstractAxis::setTitleBrush(const QBrush &brush)`

**作用与语义：**

该属性保留用于绘制标题文字的画笔。
只有画笔的颜色才相关。

**如何使用：** 调用 `setTitleBrush(...)` 修改 `titleBrush`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QAbstractAxis::setTitleFont(const QFont &font)`

**作用与语义：**

该属性包含了轴标题的字体。

**如何使用：** 调用 `setTitleFont(...)` 修改 `titleFont`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QAbstractAxis::setVisible(bool visible = true)`

**作用与语义：**

该属性表示轴的可见性。

**如何使用：** 调用 `setVisible(...)` 修改 `visible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `[signal] void QAbstractAxis::shadesBorderColorChanged(QColor color)`

**作用与语义：**

该属性表示轴阴影的边框（笔）颜色。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `shadesBorderColor` 的变化，不要把它当作普通函数主动调用。

### `QBrush QAbstractAxis::shadesBrush() const`

**作用与语义：**

还原用于绘制阴影的画笔。
注意：属性shadesBrush的Getter函数。

### `[signal] void QAbstractAxis::shadesBrushChanged(const QBrush &brush)`

**作用与语义：**

该属性包含用于绘制轴阴影（网格线之间的区域）的画笔。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `shadesBrush` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QAbstractAxis::shadesColorChanged(QColor color)`

**作用与语义：**

该属性表示轴阴影的填充（画刷）颜色。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `shadesColor` 的变化，不要把它当作普通函数主动调用。

### `QPen QAbstractAxis::shadesPen() const`

**作用与语义：**

归还用来画阴影的笔。
注意：属性 shadesPen 的获取函数。

### `[signal] void QAbstractAxis::shadesPenChanged(const QPen &pen)`

**作用与语义：**

该属性包含用于绘制轴阴影（网格线之间的区域）的笔。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `shadesPen` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QAbstractAxis::shadesVisibleChanged(bool visible)`

**作用与语义：**

该属性表示轴阴影的可见性。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `shadesVisible` 的变化，不要把它当作普通函数主动调用。

### `void QAbstractAxis::show()`

**作用与语义：**

使轴线、阴影、标签和网格线可见。

### `QBrush QAbstractAxis::titleBrush() const`

**作用与语义：**

还原用于绘制标题的画笔。
注意：property titleBrush 的获取函数。

### `[signal] void QAbstractAxis::titleBrushChanged(const QBrush &brush)`

**作用与语义：**

该属性保留用于绘制标题文字的画笔。
只有画笔的颜色才相关。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `titleBrush` 的变化，不要把它当作普通函数主动调用。

### `QFont QAbstractAxis::titleFont() const`

**作用与语义：**

返回用于绘制标题的字体。
注意：property titleFont 的获取函数。

### `[signal] void QAbstractAxis::titleFontChanged(const QFont &font)`

**作用与语义：**

该属性包含了轴标题的字体。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `titleFont` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QAbstractAxis::titleTextChanged(const QString &text)`

**作用与语义：**

该属性即为轴的名称。
默认为空。轴心标题支持HTML格式化。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `titleText` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QAbstractAxis::titleVisibleChanged(bool visible)`

**作用与语义：**

该属性保留了轴线名称的可见性。
默认情况下，数值是`true`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `titleVisible` 的变化，不要把它当作普通函数主动调用。

### `[signal, since 6.2] void QAbstractAxis::truncateLabelsChanged(bool truncateLabels)`

**作用与语义：**

该属性表示标签的截断状态。
表示如果全文空间不足，标签是否应被截断。默认等同于`true`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `truncateLabels` 的变化，不要把它当作普通函数主动调用。

### `[pure virtual] QAbstractAxis::AxisType QAbstractAxis::type() const`

**作用与语义：**

返回轴的类型。

### `[signal] void QAbstractAxis::visibleChanged(bool visible)`

**作用与语义：**

该属性表示轴的可见性。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `visible` 的变化，不要把它当作普通函数主动调用。

### `enum AxisType { AxisTypeNoAxis, AxisTypeValue, AxisTypeBarCategory, AxisTypeCategory, AxisTypeDateTime, …, AxisTypeColor }`

**作用与语义：**

该枚举类型指定轴对象的类型。
- `QAbstractAxis::AxisTypeNoAxis`：`0x0`
- `QAbstractAxis::AxisTypeValue`：`0x1`
- `QAbstractAxis::AxisTypeBarCategory`：`0x2`
- `QAbstractAxis::AxisTypeCategory`：`0x4`
- `QAbstractAxis::AxisTypeDateTime`：`0x8`
- `QAbstractAxis::AxisTypeLogValue`：`0x10`
- `QAbstractAxis::AxisTypeColor`：`0x20`
AxisTypes 类型是 QFlags 的 typedef<AxisType>。它存储 AxisType 值的 OR 组合。

### `flags AxisTypes`

**作用与语义：**

该枚举类型指定轴对象的类型。
- `QAbstractAxis::AxisTypeNoAxis`：`0x0`
- `QAbstractAxis::AxisTypeValue`：`0x1`
- `QAbstractAxis::AxisTypeBarCategory`：`0x2`
- `QAbstractAxis::AxisTypeCategory`：`0x4`
- `QAbstractAxis::AxisTypeDateTime`：`0x8`
- `QAbstractAxis::AxisTypeLogValue`：`0x10`
- `QAbstractAxis::AxisTypeColor`：`0x20`
AxisTypes 类型是 QFlags 的 typedef<AxisType>。它存储 AxisType 值的 OR 组合。

### `Qt::Alignment alignment() const`

**作用与语义：**

该属性表示轴的对齐。
可以是`Qt::AlignLeft`、`Qt::AlignRight`、`Qt::AlignBottom`或`Qt::AlignTop`。

**如何使用：** 调用 `alignment()` 读取当前值；它不会修改应用状态。

### `QColor gridLineColor()`

**作用与语义：**

该属性表示网格线的颜色。

**如何使用：** 调用 `gridLineColor()` 读取当前值；它不会修改应用状态。

### `bool isGridLineVisible() const`

**作用与语义：**

该特性保持网格线的可见性。

**如何使用：** 调用 `isGridLineVisible()` 读取当前值；它不会修改应用状态。

### `bool isLineVisible() const`

**作用与语义：**

该属性决定了轴线的可见性。

**如何使用：** 调用 `isLineVisible()` 读取当前值；它不会修改应用状态。

### `bool isMinorGridLineVisible() const`

**作用与语义：**

该特性保留了次要网格线的可见性。
仅适用于支持次要网格线的轴线。

**如何使用：** 调用 `isMinorGridLineVisible()` 读取当前值；它不会修改应用状态。

### `bool isReverse() const`

**作用与语义：**

该属性在使用反向轴时成立。
默认情况下，数值为`false`。
反向轴由线、样条和散点系列以及带有笛卡尔图的面积系列支持。所有连接同一系列的同方向轴，如果其中一个轴被反转或行为未定义，必须反转。

**如何使用：** 调用 `isReverse()` 读取当前值；它不会修改应用状态。

### `bool isTitleVisible() const`

**作用与语义：**

该属性保留了轴线名称的可见性。
默认情况下，数值是`true`。

**如何使用：** 调用 `isTitleVisible()` 读取当前值；它不会修改应用状态。

### `bool isVisible() const`

**作用与语义：**

该属性表示轴的可见性。

**如何使用：** 调用 `isVisible()` 读取当前值；它不会修改应用状态。

### `int labelsAngle() const`

**作用与语义：**

该属性表示轴标签的角度以度为单位。

**如何使用：** 调用 `labelsAngle()` 读取当前值；它不会修改应用状态。

### `QColor labelsColor() const`

**作用与语义：**

该属性表示轴标签的颜色。

**如何使用：** 调用 `labelsColor()` 读取当前值；它不会修改应用状态。

### `bool labelsTruncated() const`

**作用与语义：**

如果轴上至少有一个标签被截断，返回`true`。
在轴线显示之前，返回的值不会准确。

**如何使用：** 调用 `labelsTruncated()` 读取当前值；它不会修改应用状态。

### `bool labelsVisible() const`

**作用与语义：**

该属性适用于轴标签是否可见。

**如何使用：** 调用 `labelsVisible()` 读取当前值；它不会修改应用状态。

### `QColor linePenColor() const`

**作用与语义：**

该属性包含轴和刻度标记的颜色。

**如何使用：** 调用 `linePenColor()` 读取当前值；它不会修改应用状态。

### `QColor minorGridLineColor()`

**作用与语义：**

该属性表示小网格线的颜色。
仅适用于支持次要网格线的轴线。

**如何使用：** 调用 `minorGridLineColor()` 读取当前值；它不会修改应用状态。

### `QPen minorGridLinePen() const`

**作用与语义：**

该属性决定了绘制次要网格线的笔。
仅适用于支持次要网格线的轴线。

**如何使用：** 调用 `minorGridLinePen()` 读取当前值；它不会修改应用状态。

### `void setGridLineColor(const QColor &color)`

**作用与语义：**

该属性表示网格线的颜色。

**如何使用：** 调用 `setGridLineColor(...)` 修改 `gridLineColor`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setGridLineVisible(bool visible = true)`

**作用与语义：**

该特性保持网格线的可见性。

**如何使用：** 调用 `setGridLineVisible(...)` 修改 `gridVisible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLabelsAngle(int angle)`

**作用与语义：**

该属性表示轴标签的角度以度为单位。

**如何使用：** 调用 `setLabelsAngle(...)` 修改 `labelsAngle`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLabelsColor(QColor color)`

**作用与语义：**

该属性表示轴标签的颜色。

**如何使用：** 调用 `setLabelsColor(...)` 修改 `labelsColor`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLabelsVisible(bool visible = true)`

**作用与语义：**

该属性适用于轴标签是否可见。

**如何使用：** 调用 `setLabelsVisible(...)` 修改 `labelsVisible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLinePenColor(QColor color)`

**作用与语义：**

该属性包含轴和刻度标记的颜色。

**如何使用：** 调用 `setLinePenColor(...)` 修改 `color`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMinorGridLineColor(const QColor &color)`

**作用与语义：**

该属性表示小网格线的颜色。
仅适用于支持次要网格线的轴线。

**如何使用：** 调用 `setMinorGridLineColor(...)` 修改 `minorGridLineColor`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMinorGridLinePen(const QPen &pen)`

**作用与语义：**

该属性决定了绘制次要网格线的笔。
仅适用于支持次要网格线的轴线。

**如何使用：** 调用 `setMinorGridLinePen(...)` 修改 `minorGridLinePen`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMinorGridLineVisible(bool visible = true)`

**作用与语义：**

该特性保留了次要网格线的可见性。
仅适用于支持次要网格线的轴线。

**如何使用：** 调用 `setMinorGridLineVisible(...)` 修改 `minorGridVisible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setReverse(bool reverse = true)`

**作用与语义：**

该属性在使用反向轴时成立。
默认情况下，数值为`false`。
反向轴由线、样条和散点系列以及带有笛卡尔图的面积系列支持。所有连接同一系列的同方向轴，如果其中一个轴被反转或行为未定义，必须反转。

**如何使用：** 调用 `setReverse(...)` 修改 `reverse`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setShadesBorderColor(QColor color)`

**作用与语义：**

该属性表示轴阴影的边框（笔）颜色。

**如何使用：** 调用 `setShadesBorderColor(...)` 修改 `shadesBorderColor`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setShadesColor(QColor color)`

**作用与语义：**

该属性表示轴阴影的填充（画刷）颜色。

**如何使用：** 调用 `setShadesColor(...)` 修改 `shadesColor`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setShadesVisible(bool visible = true)`

**作用与语义：**

该属性表示轴阴影的可见性。

**如何使用：** 调用 `setShadesVisible(...)` 修改 `shadesVisible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTitleText(const QString &title)`

**作用与语义：**

该属性即为轴的名称。
默认为空。轴心标题支持HTML格式化。

**如何使用：** 调用 `setTitleText(...)` 修改 `titleText`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTitleVisible(bool visible = true)`

**作用与语义：**

该属性保留了轴线名称的可见性。
默认情况下，数值是`true`。

**如何使用：** 调用 `setTitleVisible(...)` 修改 `titleVisible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTruncateLabels(bool truncateLabels = true)`

**作用与语义：**

该属性表示标签的截断状态。
表示如果全文空间不足，标签是否应被截断。默认等同于`true`。

**如何使用：** 调用 `setTruncateLabels(...)` 修改 `truncateLabels`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QColor shadesBorderColor() const`

**作用与语义：**

该属性表示轴阴影的边框（笔）颜色。

**如何使用：** 调用 `shadesBorderColor()` 读取当前值；它不会修改应用状态。

### `QColor shadesColor() const`

**作用与语义：**

该属性表示轴阴影的填充（画刷）颜色。

**如何使用：** 调用 `shadesColor()` 读取当前值；它不会修改应用状态。

### `bool shadesVisible() const`

**作用与语义：**

该属性表示轴阴影的可见性。

**如何使用：** 调用 `shadesVisible()` 读取当前值；它不会修改应用状态。

### `QString titleText() const`

**作用与语义：**

该属性即为轴的名称。
默认为空。轴心标题支持HTML格式化。

**如何使用：** 调用 `titleText()` 读取当前值；它不会修改应用状态。

### `bool truncateLabels() const`

**作用与语义：**

该属性表示标签的截断状态。
表示如果全文空间不足，标签是否应被截断。默认等同于`true`。

**如何使用：** 调用 `truncateLabels()` 读取当前值；它不会修改应用状态。

### `void reverseChanged(bool reverse)`

**作用与语义：**

该属性在使用反向轴时成立。
默认情况下，数值为`false`。
反向轴由线、样条和散点系列以及带有笛卡尔图的面积系列支持。所有连接同一系列的同方向轴，如果其中一个轴被反转或行为未定义，必须反转。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `reverse` 的变化，不要把它当作普通函数主动调用。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

### 状态和错误边界

QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

### 线程边界

QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

### 最容易出现的错误

不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QAbstractAxis` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
