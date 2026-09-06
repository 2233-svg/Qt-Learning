# QChart

> Qt 6.11.1 · Qt Charts

## 1. 先建立直觉

**一句话定位：** 这是 Qt Charts 中围绕“图表”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Charts 提供折线、柱状、饼图、散点图和坐标轴等数据可视化组件。

### 这是什么

`QChart` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QChart>`
- 继承自：QGraphicsWidget
- 直接派生类：QPolarChart

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum AnimationOption { NoAnimation, GridAxisAnimations, SeriesAnimations, AllAnimations }`
- `flags AnimationOptions`
- `enum ChartTheme { ChartThemeLight, ChartThemeBlueCerulean, ChartThemeDark, ChartThemeBrownSand, ChartThemeBlueNcs, …, ChartThemeQt }`
- `enum ChartType { ChartTypeUndefined, ChartTypeCartesian, ChartTypePolar }`

### 属性

- `animationDuration : int`
- `animationEasingCurve : QEasingCurve`
- `animationOptions : QChart::AnimationOptions`
- `backgroundRoundness : qreal`
- `backgroundVisible : bool`
- `chartType : QChart::ChartType`
- `dropShadowEnabled : bool`
- `locale : QLocale`
- `localizeNumbers : bool`
- `margins : QMargins`
- `plotArea : QRectF`
- `plotAreaBackgroundVisible : bool`
- `theme : QChart::ChartTheme`
- `title : QString`

### 公有函数

- `QChart(QGraphicsItem *parent = nullptr, Qt::WindowFlags wFlags = Qt::WindowFlags())`
- `virtual ~QChart()`
- `void addAxis(QAbstractAxis *axis, Qt::Alignment alignment)`
- `void addSeries(QAbstractSeries *series)`
- `int animationDuration() const`
- `QEasingCurve animationEasingCurve() const`
- `QChart::AnimationOptions animationOptions() const`
- `QList<QAbstractAxis *> axes(Qt::Orientations orientation = Qt::Horizontal|Qt::Vertical, QAbstractSeries *series = nullptr) const`
- `QBrush backgroundBrush() const`
- `QPen backgroundPen() const`
- `qreal backgroundRoundness() const`
- `QChart::ChartType chartType() const`
- `void createDefaultAxes()`
- `bool isBackgroundVisible() const`
- `bool isDropShadowEnabled() const`
- `bool isPlotAreaBackgroundVisible() const`
- `bool isZoomed()`
- `QLegend * legend() const`
- `QLocale locale() const`
- `bool localizeNumbers() const`
- `QPointF mapToPosition(const QPointF &value, QAbstractSeries *series = nullptr)`
- `QPointF mapToValue(const QPointF &position, QAbstractSeries *series = nullptr)`
- `QMargins margins() const`
- `QRectF plotArea() const`
- `QBrush plotAreaBackgroundBrush() const`
- `QPen plotAreaBackgroundPen() const`
- `void removeAllSeries()`
- `void removeAxis(QAbstractAxis *axis)`
- `void removeSeries(QAbstractSeries *series)`
- `void scroll(qreal dx, qreal dy)`
- `QList<QAbstractSeries *> series() const`
- `void setAnimationDuration(int msecs)`
- `void setAnimationEasingCurve(const QEasingCurve &curve)`
- `void setAnimationOptions(QChart::AnimationOptions options)`
- `void setBackgroundBrush(const QBrush &brush)`
- `void setBackgroundPen(const QPen &pen)`
- `void setBackgroundRoundness(qreal diameter)`
- `void setBackgroundVisible(bool visible = true)`
- `void setDropShadowEnabled(bool enabled = true)`
- `void setLocale(const QLocale &locale)`
- `void setLocalizeNumbers(bool localize)`
- `void setMargins(const QMargins &margins)`
- `void setPlotArea(const QRectF &rect)`
- `void setPlotAreaBackgroundBrush(const QBrush &brush)`
- `void setPlotAreaBackgroundPen(const QPen &pen)`
- `void setPlotAreaBackgroundVisible(bool visible = true)`
- `void setTheme(QChart::ChartTheme theme)`
- `void setTitle(const QString &title)`
- `void setTitleBrush(const QBrush &brush)`
- `void setTitleFont(const QFont &font)`
- `QChart::ChartTheme theme() const`
- `QString title() const`
- `QBrush titleBrush() const`
- `QFont titleFont() const`
- `void zoom(qreal factor)`
- `void zoomIn()`
- `void zoomIn(const QRectF &rect)`
- `void zoomOut()`
- `void zoomReset()`

### 信号

- `void plotAreaChanged(const QRectF &plotArea)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QChart::AnimationOptionflags QChart::AnimationOptions`

**作用与语义：**

该枚举描述了图表中启用的动画。
- `QChart::NoAnimation`：`0x0`;图表中关闭动画。这是默认值。
- `QChart::GridAxisAnimations`：`0x1`;图表中启用了网格轴动画。
- `QChart::SeriesAnimations`：`0x2`;图表中启用了系列动画。
- `QChart::AllAnimations`：`0x3`;图表中启用了所有动画类型。
AnimationOptions 类型是 QFlags 的 typedef<AnimationOption>。它存储 AnimationOption 值的 OR 组合。

### `enum QChart::ChartTheme`

**作用与语义：**

这个枚举描述了图表所用的主题。
主题是内置的UI风格相关设置集合，应用于图表的所有视觉元素，如颜色、笔、画笔、系列字体，以及轴、标题和图例。带小部件的图表画廊展示了如何使用主题。
注意：更改主题会覆盖之前对系列应用的所有自定义。
- `QChart::ChartThemeLight`：`0`;光明主题，是默认主题。
- `QChart::ChartThemeBlueCerulean`：`1`;蔚蓝色主题。
- `QChart::ChartThemeDark`：`2`;黑暗主题。
- `QChart::ChartThemeBrownSand`：`3`;沙棕色主题。
- `QChart::ChartThemeBlueNcs`：`4`;自然色彩系统（NCS）蓝色主题。
- `QChart::ChartThemeHighContrast`：`5`;高对比度主题。
- `QChart::ChartThemeBlueIcy`：`6`;冰蓝色主题。
- `QChart::ChartThemeQt`：`7`;Qt主题。

### `enum QChart::ChartType`

**作用与语义：**

该枚举描述了图表类型。
- `QChart::ChartTypeUndefined`：`0`;图表类型未定义。
- `QChart::ChartTypeCartesian`：`1`;笛卡尔图表。
- `QChart::ChartTypePolar`：`2`;极地图。

### `animationDuration : int`

**作用与语义：**

该属性表示图表动画的持续时间。

**如何使用：** 调用 `animationDuration()` 读取当前值；它不会修改应用状态。

### `animationEasingCurve : QEasingCurve`

**作用与语义：**

该属性表示图表动画的缓和曲线。

**如何使用：** 调用 `animationEasingCurve()` 读取当前值；它不会修改应用状态。

### `animationOptions : QChart::AnimationOptions`

**作用与语义：**

该属性包含图表的动画选项。
动画会根据该设置开启或禁用。

**如何使用：** 调用 `animationOptions()` 读取当前值；它不会修改应用状态。

### `backgroundRoundness : qreal`

**作用与语义：**

此属性保存图表背景角处圆形的直径。

**如何使用：** 调用 `backgroundRoundness()` 读取当前值；它不会修改应用状态。

### `backgroundVisible : bool`

**作用与语义：**

该属性决定图表背景是否可见。

**如何使用：** 调用 `backgroundVisible()` 读取当前值；它不会修改应用状态。

### `[read-only] chartType : QChart::ChartType`

**作用与语义：**

无论该图是笛卡尔图还是极地图，这一属性都成立。
该属性在内部设置，且为只读。

**如何使用：** 调用 `chartType()` 读取当前值；它不会修改应用状态。

### `dropShadowEnabled : bool`

**作用与语义：**

该属性是否启用了背景投影效果。
如果设置为`true`，则启用了背景投影效果。设置为`false`时，则禁用。
注意：阴影效果取决于主题，因此如果主题变更，场景也可能发生变化。

**如何使用：** 调用 `dropShadowEnabled()` 读取当前值；它不会修改应用状态。

### `locale : QLocale`

**作用与语义：**

该物业是用于格式化各种排行榜标签的场所。
标签仅在`localizeNumbers`被`true`时局部化，`QDateTimeAxis`标签则始终使用具有该属性的`QLocale`集。
默认使用图表构建时的应用默认位置。

**如何使用：** 调用 `locale()` 读取当前值；它不会修改应用状态。

### `localizeNumbers : bool`

**作用与语义：**

该属性是否局域化。
`true`时，所有生成的数字出现在不同系列和轴标签中，将使用带有`locale`属性的`QLocale`集进行局部化。`false`时，始终使用C语言的区域。默认为`false`。
注意：该属性不影响`QDateTimeAxis`标签，标签总是使用带有locale属性的`QLocale`集。

**如何使用：** 调用 `localizeNumbers()` 读取当前值；它不会修改应用状态。

### `margins : QMargins`

**作用与语义：**

该属性表示了图表矩形边缘与图面积之间允许的最小间距。
页边用于绘制标题、轴和图例。

**如何使用：** 调用 `margins()` 读取当前值；它不会修改应用状态。

### `plotArea : QRectF`

**作用与语义：**

该属性包含图表所绘制的矩形。
图区不包括边界定义的区域。默认情况下，如果在`QChartView`内，这个尺寸会调整大小。如果为图区设置了显式大小，则会遵守这一点，恢复默认行为时调用`setPlotArea(QRectF());`即可实现。

**如何使用：** 调用 `plotArea()` 读取当前值；它不会修改应用状态。

### `plotAreaBackgroundVisible : bool`

**作用与语义：**

该属性决定图表区域背景是否可见。
注意：默认情况下，图区背景是不可见的，图区使用通用的图表背景。

**如何使用：** 调用 `plotAreaBackgroundVisible()` 读取当前值；它不会修改应用状态。

### `theme : QChart::ChartTheme`

**作用与语义：**

该属性包含了图表所用的主题。

**如何使用：** 调用 `theme()` 读取当前值；它不会修改应用状态。

### `title : QString`

**作用与语义：**

该地产拥有该图表的标题。
标题以标题显示在图表顶部。图表标题支持 HTML 格式。

**如何使用：** 调用 `title()` 读取当前值；它不会修改应用状态。

### `[explicit] QChart::QChart(QGraphicsItem *parent = nullptr, Qt::WindowFlags wFlags = Qt::WindowFlags())`

**作用与语义：**

构造一个 Chart 对象，该对象是 `parent` 的子节点。`wFlags` 指定的属性传递给 `QGraphicsWidget` 构造器。

### `[virtual noexcept] QChart::~QChart()`

**作用与语义：**

删除图表对象及其子节点，如添加到其上的系列和轴对象。

### `void QChart::addAxis(QAbstractAxis *axis, Qt::Alignment alignment)`

**作用与语义：**

将`axis`轴添加到按`alignment`指定的对齐图表上。图表拥有该轴的所有权。

### `void QChart::addSeries(QAbstractSeries *series)`

**作用与语义：**

把系列`series`加到排行榜上，并拥有它。
注意：新添加的系列默认不会附加到任何轴线上，即使是那些在该系列加入图表前用`createDefaultAxes()`创建的轴线也不会。如果在图表显示前没有附加任何轴线，该系列会被绘制成其轴线的范围与图表区域完全匹配。如果同一图表还显示其他系列有正确连接轴，可能会造成混淆，因此请务必在添加系列后调用`createDefaultAxes()`，或者明确为该系列附加轴。

### `QList<QAbstractAxis *> QChart::axes(Qt::Orientations orientation = Qt::Horizontal|Qt::Vertical, QAbstractSeries *series = nullptr) const`

**作用与语义：**

返回与`orientation`指定方向相关联的`series`系列轴。若未指定系列，则返回所有添加到指定方向的轴。

### `QBrush QChart::backgroundBrush() const`

**作用与语义：**

拿到用于绘制图表背景的画笔。

### `QPen QChart::backgroundPen() const`

**作用与语义：**

拿到用来绘制图表背景的笔。

### `void QChart::createDefaultAxes()`

**作用与语义：**

根据已添加到图表中的系列创建图表的轴。之前添加到图表中的轴将被删除。
注意：该函数必须在所有系列加入图表后调用。该函数创建的轴不会被自动附加到图表中添加的任何序列。没有连接轴的系列默认会利用图表的整个图区，如果还有其他系列也有正确连接的轴，这会造成混淆。
- `Series type`：水平轴（X）;垂直轴（Y）
- `QXYSeries`：`QValueAxis`;`QValueAxis`
- `QBarSeries`：`QBarCategoryAxis`;`QValueAxis`
- `QPieSeries`：无;无
如果图表中添加了多个`QXYSeries`衍生系列，且没有添加其他类型的系列，则只会生成一对轴。如果图表中添加了多个不同类型的系列，则每个系列都有自己的轴对。
该系列的具体轴可以从图表中获得，方法是将该系列作为`axes()`函数调用的参数。`QPieSeries`不生成任何轴。

### `bool QChart::isZoomed()`

**作用与语义：**

如果有序列具有缩放域，返回`true`。

### `QLegend *QChart::legend() const`

**作用与语义：**

返回图表中的图例对象。所有权仍保留在图表上。

### `QPointF QChart::mapToPosition(const QPointF &value, QAbstractSeries *series = nullptr)`

**作用与语义：**

返回图表上对应`series`指定系列中`value`值的位置。

### `QPointF QChart::mapToValue(const QPointF &position, QAbstractSeries *series = nullptr)`

**作用与语义：**

返回`series`指定在图表中`position`位置的系列值。

### `QBrush QChart::plotAreaBackgroundBrush() const`

**作用与语义：**

返回用于填充图表图区域背景的画笔。

### `QPen QChart::plotAreaBackgroundPen() const`

**作用与语义：**

返回用于绘制图表区域背景的笔。

### `void QChart::removeAllSeries()`

**作用与语义：**

移除并删除所有添加到图表中的系列对象。

### `void QChart::removeAxis(QAbstractAxis *axis)`

**作用与语义：**

将轴`axis`从图表中移除。图表释放了对指定`axis`对象的所有权。

### `void QChart::removeSeries(QAbstractSeries *series)`

**作用与语义：**

将序列`series`从图表中移除。图表释放了指定`series`对象的所有权。

### `void QChart::scroll(qreal dx, qreal dy)`

**作用与语义：**

按`dx`和`dy`指定的距离滚动图表可见区域。
对于极坐标图，`dx`表示角轴上的角度，而非距离。

### `QList<QAbstractSeries *> QChart::series() const`

**作用与语义：**

返回所有新增到图表中的系列。

### `void QChart::setBackgroundBrush(const QBrush &brush)`

**作用与语义：**

将用于绘制图表背景的画笔设置为`brush`。

### `void QChart::setBackgroundPen(const QPen &pen)`

**作用与语义：**

将用于绘制图表背景的笔设置为`pen`。

### `void QChart::setPlotAreaBackgroundBrush(const QBrush &brush)`

**作用与语义：**

将用于填充图表背景的画笔设置为`brush`。

### `void QChart::setPlotAreaBackgroundPen(const QPen &pen)`

**作用与语义：**

将用于绘制图表背景的笔设置为`pen`。

### `void QChart::setTitleBrush(const QBrush &brush)`

**作用与语义：**

将用于绘制标题文字的画笔设置为`brush`。

### `void QChart::setTitleFont(const QFont &font)`

**作用与语义：**

将用于绘制图表标题的字体设置为`font`。

### `QBrush QChart::titleBrush() const`

**作用与语义：**

返回用于绘制标题文字的画笔。

### `QFont QChart::titleFont() const`

**作用与语义：**

获得用于绘制图表标题的字体。

### `void QChart::zoom(qreal factor)`

**作用与语义：**

按自定义系数`factor`来放大视图。
超过1.0的倍数会放大视野，而0.0到1.0之间的倍数则会缩放出画面。

### `void QChart::zoomIn()`

**作用与语义：**

视野放大了两倍。

### `void QChart::zoomIn(const QRectF &rect)`

**作用与语义：**

将视角放大到矩形`rect`仍完全可见的最大视角。
注意：应用缩放可能会修改附加轴的属性，例如 QAbstractAxis：：min 和 QAbstractAxis：：max。
注意：极坐标图不支持此功能。

### `void QChart::zoomOut()`

**作用与语义：**

画面放大了两倍。
注意：如果结果包含无效的对数轴范围，这个方法就没有用。

### `void QChart::zoomReset()`

**作用与语义：**

将系列域重置到调用任何缩放方法之前的状态。
注意：这也会重置在第一次缩放操作和调用该方法之间指定的滚动和显式轴距设置。如果没有进行过变放操作，该方法则无效。

### `enum AnimationOption { NoAnimation, GridAxisAnimations, SeriesAnimations, AllAnimations }`

**作用与语义：**

该枚举描述了图表中启用的动画。
- `QChart::NoAnimation`：`0x0`;图表中关闭动画。这是默认值。
- `QChart::GridAxisAnimations`：`0x1`;图表中启用了网格轴动画。
- `QChart::SeriesAnimations`：`0x2`;图表中启用了系列动画。
- `QChart::AllAnimations`：`0x3`;图表中启用了所有动画类型。
AnimationOptions 类型是 QFlags 的 typedef<AnimationOption>。它存储 AnimationOption 值的 OR 组合。

### `flags AnimationOptions`

**作用与语义：**

该枚举描述了图表中启用的动画。
- `QChart::NoAnimation`：`0x0`;图表中关闭动画。这是默认值。
- `QChart::GridAxisAnimations`：`0x1`;图表中启用了网格轴动画。
- `QChart::SeriesAnimations`：`0x2`;图表中启用了系列动画。
- `QChart::AllAnimations`：`0x3`;图表中启用了所有动画类型。
AnimationOptions 类型是 QFlags 的 typedef<AnimationOption>。它存储 AnimationOption 值的 OR 组合。

### `int animationDuration() const`

**作用与语义：**

该属性表示图表动画的持续时间。

**如何使用：** 调用 `animationDuration()` 读取当前值；它不会修改应用状态。

### `QEasingCurve animationEasingCurve() const`

**作用与语义：**

该属性表示图表动画的缓和曲线。

**如何使用：** 调用 `animationEasingCurve()` 读取当前值；它不会修改应用状态。

### `QChart::AnimationOptions animationOptions() const`

**作用与语义：**

该属性包含图表的动画选项。
动画会根据该设置开启或禁用。

**如何使用：** 调用 `animationOptions()` 读取当前值；它不会修改应用状态。

### `qreal backgroundRoundness() const`

**作用与语义：**

此属性保存图表背景角处圆形的直径。

**如何使用：** 调用 `backgroundRoundness()` 读取当前值；它不会修改应用状态。

### `QChart::ChartType chartType() const`

**作用与语义：**

无论该图是笛卡尔图还是极地图，这一属性都成立。
该属性在内部设置，且为只读。

**如何使用：** 调用 `chartType()` 读取当前值；它不会修改应用状态。

### `bool isBackgroundVisible() const`

**作用与语义：**

该属性决定图表背景是否可见。

**如何使用：** 调用 `isBackgroundVisible()` 读取当前值；它不会修改应用状态。

### `bool isDropShadowEnabled() const`

**作用与语义：**

该属性是否启用了背景投影效果。
如果设置为`true`，则启用了背景投影效果。设置为`false`时，则禁用。
注意：阴影效果取决于主题，因此如果主题变更，场景也可能发生变化。

**如何使用：** 调用 `isDropShadowEnabled()` 读取当前值；它不会修改应用状态。

### `bool isPlotAreaBackgroundVisible() const`

**作用与语义：**

该属性决定图表区域背景是否可见。
注意：默认情况下，图区背景是不可见的，图区使用通用的图表背景。

**如何使用：** 调用 `isPlotAreaBackgroundVisible()` 读取当前值；它不会修改应用状态。

### `QLocale locale() const`

**作用与语义：**

该物业是用于格式化各种排行榜标签的场所。
标签仅在`localizeNumbers`被`true`时局部化，`QDateTimeAxis`标签则始终使用具有该属性的`QLocale`集。
默认使用图表构建时的应用默认位置。

**如何使用：** 调用 `locale()` 读取当前值；它不会修改应用状态。

### `bool localizeNumbers() const`

**作用与语义：**

该属性是否局域化。
`true`时，所有生成的数字出现在不同系列和轴标签中，将使用带有`locale`属性的`QLocale`集进行局部化。`false`时，始终使用C语言的区域。默认为`false`。
注意：该属性不影响`QDateTimeAxis`标签，标签总是使用带有locale属性的`QLocale`集。

**如何使用：** 调用 `localizeNumbers()` 读取当前值；它不会修改应用状态。

### `QMargins margins() const`

**作用与语义：**

该属性表示了图表矩形边缘与图面积之间允许的最小间距。
页边用于绘制标题、轴和图例。

**如何使用：** 调用 `margins()` 读取当前值；它不会修改应用状态。

### `QRectF plotArea() const`

**作用与语义：**

该属性包含图表所绘制的矩形。
图区不包括边界定义的区域。默认情况下，如果在`QChartView`内，这个尺寸会调整大小。如果为图区设置了显式大小，则会遵守这一点，恢复默认行为时调用`setPlotArea(QRectF());`即可实现。

**如何使用：** 调用 `plotArea()` 读取当前值；它不会修改应用状态。

### `void setAnimationDuration(int msecs)`

**作用与语义：**

该属性表示图表动画的持续时间。

**如何使用：** 调用 `setAnimationDuration(...)` 修改 `animationDuration`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setAnimationEasingCurve(const QEasingCurve &curve)`

**作用与语义：**

该属性表示图表动画的缓和曲线。

**如何使用：** 调用 `setAnimationEasingCurve(...)` 修改 `animationEasingCurve`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setAnimationOptions(QChart::AnimationOptions options)`

**作用与语义：**

该属性包含图表的动画选项。
动画会根据该设置开启或禁用。

**如何使用：** 调用 `setAnimationOptions(...)` 修改 `animationOptions`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setBackgroundRoundness(qreal diameter)`

**作用与语义：**

此属性保存图表背景角处圆形的直径。

**如何使用：** 调用 `setBackgroundRoundness(...)` 修改 `backgroundRoundness`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setBackgroundVisible(bool visible = true)`

**作用与语义：**

该属性决定图表背景是否可见。

**如何使用：** 调用 `setBackgroundVisible(...)` 修改 `backgroundVisible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDropShadowEnabled(bool enabled = true)`

**作用与语义：**

该属性是否启用了背景投影效果。
如果设置为`true`，则启用了背景投影效果。设置为`false`时，则禁用。
注意：阴影效果取决于主题，因此如果主题变更，场景也可能发生变化。

**如何使用：** 调用 `setDropShadowEnabled(...)` 修改 `dropShadowEnabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLocale(const QLocale &locale)`

**作用与语义：**

该物业是用于格式化各种排行榜标签的场所。
标签仅在`localizeNumbers`被`true`时局部化，`QDateTimeAxis`标签则始终使用具有该属性的`QLocale`集。
默认使用图表构建时的应用默认位置。

**如何使用：** 调用 `setLocale(...)` 修改 `locale`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLocalizeNumbers(bool localize)`

**作用与语义：**

该属性是否局域化。
`true`时，所有生成的数字出现在不同系列和轴标签中，将使用带有`locale`属性的`QLocale`集进行局部化。`false`时，始终使用C语言的区域。默认为`false`。
注意：该属性不影响`QDateTimeAxis`标签，标签总是使用带有locale属性的`QLocale`集。

**如何使用：** 调用 `setLocalizeNumbers(...)` 修改 `localizeNumbers`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMargins(const QMargins &margins)`

**作用与语义：**

该属性表示了图表矩形边缘与图面积之间允许的最小间距。
页边用于绘制标题、轴和图例。

**如何使用：** 调用 `setMargins(...)` 修改 `margins`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPlotArea(const QRectF &rect)`

**作用与语义：**

该属性包含图表所绘制的矩形。
图区不包括边界定义的区域。默认情况下，如果在`QChartView`内，这个尺寸会调整大小。如果为图区设置了显式大小，则会遵守这一点，恢复默认行为时调用`setPlotArea(QRectF());`即可实现。

**如何使用：** 调用 `setPlotArea(...)` 修改 `plotArea`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPlotAreaBackgroundVisible(bool visible = true)`

**作用与语义：**

该属性决定图表区域背景是否可见。
注意：默认情况下，图区背景是不可见的，图区使用通用的图表背景。

**如何使用：** 调用 `setPlotAreaBackgroundVisible(...)` 修改 `plotAreaBackgroundVisible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTheme(QChart::ChartTheme theme)`

**作用与语义：**

该属性包含了图表所用的主题。

**如何使用：** 调用 `setTheme(...)` 修改 `theme`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTitle(const QString &title)`

**作用与语义：**

该地产拥有该图表的标题。
标题以标题显示在图表顶部。图表标题支持 HTML 格式。

**如何使用：** 调用 `setTitle(...)` 修改 `title`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QChart::ChartTheme theme() const`

**作用与语义：**

该属性包含了图表所用的主题。

**如何使用：** 调用 `theme()` 读取当前值；它不会修改应用状态。

### `QString title() const`

**作用与语义：**

该地产拥有该图表的标题。
标题以标题显示在图表顶部。图表标题支持 HTML 格式。

**如何使用：** 调用 `title()` 读取当前值；它不会修改应用状态。

### `void plotAreaChanged(const QRectF &plotArea)`

**作用与语义：**

该属性包含图表所绘制的矩形。
图区不包括边界定义的区域。默认情况下，如果在`QChartView`内，这个尺寸会调整大小。如果为图区设置了显式大小，则会遵守这一点，恢复默认行为时调用`setPlotArea(QRectF());`即可实现。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `plotArea` 的变化，不要把它当作普通函数主动调用。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QChart` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
