# QXYSeries

> Qt 6.11.1 · Qt Charts

## 1. 先建立直觉

**一句话定位：** `QXYSeries` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Charts 提供折线、柱状、饼图、散点图和坐标轴等数据可视化组件。

### 这是什么

`QXYSeries` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QXYSeries>`
- 继承自：QAbstractSeries
- 直接派生类：QLineSeries、QScatterSeries

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

### 状态、生命周期和线程

**生命周期：** 先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

**状态与结果：** QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

**线程与事件循环：** QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

## 3. 直接使用

使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `(since 6.2) enum class PointConfiguration { Color, Size, Visibility, LabelVisibility, LabelFormat }`

### 属性

- `(since 6.2) bestFitLineColor : QColor`
- `(since 6.2) bestFitLineVisible : bool`
- `color : QColor`
- `pointLabelsClipping : bool`
- `pointLabelsColor : QColor`
- `pointLabelsFont : QFont`
- `pointLabelsFormat : QString`
- `pointLabelsVisible : bool`
- `pointsVisible : bool`
- `(since 6.2) selectedColor : QColor`

### 公有函数

- `virtual ~QXYSeries()`
- `void append(qreal x, qreal y)`
- `void append(const QList<QPointF> &points)`
- `void append(const QPointF &point)`
- `const QPointF & at(int index) const`
- `QColor bestFitLineColor() const`
- `(since 6.2) QPair<qreal, qreal> bestFitLineEquation(bool &ok) const`
- `bool bestFitLineVisible() const`
- `QBrush brush() const`
- `void clear()`
- `(since 6.2) void clearPointConfiguration(const int index)`
- `(since 6.2) void clearPointConfiguration(const int index, const QXYSeries::PointConfiguration key)`
- `(since 6.2) void clearPointsConfiguration()`
- `(since 6.2) void clearPointsConfiguration(const QXYSeries::PointConfiguration key)`
- `virtual QColor color() const`
- `(since 6.2) void colorBy(const QList<qreal> &sourceData, const QLinearGradient &gradient = QLinearGradient())`
- `int count() const`
- `(since 6.2) void deselectAllPoints()`
- `(since 6.2) void deselectPoint(int index)`
- `(since 6.2) void deselectPoints(const QList<int> &indexes)`
- `void insert(int index, const QPointF &point)`
- `(since 6.2) bool isPointSelected(int index)`
- `(since 6.2) const QImage & lightMarker() const`
- `(since 6.2) qreal markerSize() const`
- `QPen pen() const`
- `(since 6.2) QHash<QXYSeries::PointConfiguration, QVariant> pointConfiguration(const int index) const`
- `bool pointLabelsClipping() const`
- `QColor pointLabelsColor() const`
- `QFont pointLabelsFont() const`
- `QString pointLabelsFormat() const`
- `bool pointLabelsVisible() const`
- `QList<QPointF> points() const`
- `(since 6.2) QXYSeries::PointsConfigurationHash pointsConfiguration() const`
- `bool pointsVisible() const`
- `void remove(const QPointF &point)`
- `void remove(int index)`
- `void remove(qreal x, qreal y)`
- `void removePoints(int index, int count)`
- `void replace(const QList<QPointF> &points)`
- `void replace(const QPointF &oldPoint, const QPointF &newPoint)`
- `void replace(int index, const QPointF &newPoint)`
- `void replace(int index, qreal newX, qreal newY)`
- `void replace(qreal oldX, qreal oldY, qreal newX, qreal newY)`
- `(since 6.2) void selectAllPoints()`
- `(since 6.2) void selectPoint(int index)`
- `(since 6.2) void selectPoints(const QList<int> &indexes)`
- `(since 6.2) const QImage & selectedLightMarker() const`
- `(since 6.2) QList<int> selectedPoints() const`
- `void setBestFitLineColor(const QColor &color)`
- `void setBestFitLineVisible(bool visible = true)`
- `virtual void setBrush(const QBrush &brush)`
- `virtual void setColor(const QColor &color)`
- `(since 6.2) void setLightMarker(const QImage &lightMarker)`
- `(since 6.2) void setMarkerSize(qreal size)`
- `virtual void setPen(const QPen &pen)`
- `(since 6.2) void setPointConfiguration(const int index, const QHash<QXYSeries::PointConfiguration, QVariant> &configuration)`
- `(since 6.2) void setPointConfiguration(const int index, const QXYSeries::PointConfiguration key, const QVariant &value)`
- `void setPointLabelsClipping(bool enabled = true)`
- `void setPointLabelsColor(const QColor &color)`
- `void setPointLabelsFont(const QFont &font)`
- `void setPointLabelsFormat(const QString &format)`
- `void setPointLabelsVisible(bool visible = true)`
- `(since 6.2) void setPointSelected(int index, bool selected)`
- `(since 6.2) void setPointsConfiguration(const QHash<int, QHash<QXYSeries::PointConfiguration, QVariant>> &pointsConfiguration)`
- `void setPointsVisible(bool visible = true)`
- `void setSelectedColor(const QColor &color)`
- `(since 6.2) void setSelectedLightMarker(const QImage &selectedLightMarker)`
- `(since 6.2) void sizeBy(const QList<qreal> &sourceData, const qreal minSize, const qreal maxSize)`
- `(since 6.2) void toggleSelection(const QList<int> &indexes)`
- `QXYSeries & operator<<(const QList<QPointF> &points)`
- `QXYSeries & operator<<(const QPointF &point)`

### 信号

- `void bestFitLineColorChanged(const QColor &color)`
- `void bestFitLineVisibilityChanged(bool visible)`
- `void clicked(const QPointF &point)`
- `void colorChanged(QColor color)`
- `void doubleClicked(const QPointF &point)`
- `void hovered(const QPointF &point, bool state)`
- `(since 6.2) void lightMarkerChanged(const QImage &lightMarker)`
- `void markerSizeChanged(qreal size)`
- `void penChanged(const QPen &pen)`
- `void pointAdded(int index)`
- `void pointLabelsClippingChanged(bool clipping)`
- `void pointLabelsColorChanged(const QColor &color)`
- `void pointLabelsFontChanged(const QFont &font)`
- `void pointLabelsFormatChanged(const QString &format)`
- `void pointLabelsVisibilityChanged(bool visible)`
- `void pointRemoved(int index)`
- `void pointReplaced(int index)`
- `void pointsRemoved(int index, int count)`
- `void pointsReplaced()`
- `void pressed(const QPointF &point)`
- `void released(const QPointF &point)`
- `void selectedColorChanged(const QColor &color)`
- `void selectedPointsChanged()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[since 6.2] enum class QXYSeries::PointConfiguration`

**作用与语义：**

这个枚举值描述了点的特定配置。
- `QXYSeries::PointConfiguration::Color`：`0`;该枚举值可用于改变点的颜色。若与`QXYSeries::setPointConfiguration`一起使用，配置值应为有效 `QColor`。
- `QXYSeries::PointConfiguration::Size`：`1`;该枚举值可用于改变点的大小。如果与`QXYSeries::setPointConfiguration`一起使用，配置值应为数字，如`qreal`或`int`。
- `QXYSeries::PointConfiguration::Visibility`：`2`;该枚举值可用于隐藏或显示点。若与`QXYSeries::setPointConfiguration`一起使用，配置值应为布尔值。
- `QXYSeries::PointConfiguration::LabelVisibility`：`3`;该枚举值可用于隐藏或显示点的标签。若与`QXYSeries::setPointConfiguration`一起使用，配置值应为布尔值。
- `QXYSeries::PointConfiguration::LabelFormat (since Qt 6.5)`：`4`;该枚举值可用于为每个点设置自定义标签文本。如果与`QXYSeries::setPointConfiguration`一起使用，配置值应为字符串。
注意：如果 LabelFormat 设置了空字符串，该字符串将被忽略，并使用系列`pointLabelsFormat`。
这个枚举是在Qt 6.2引入的。

### `[since 6.2] bestFitLineColor : QColor`

**作用与语义：**

该属性表示最佳拟合线的颜色。

**如何使用：** 调用 `bestFitLineColor()` 读取当前值；它不会修改应用状态。

### `[since 6.2] bestFitLineVisible : bool`

**作用与语义：**

该特性保持最佳拟合线的可见性。
该属性默认`false`。

**如何使用：** 调用 `bestFitLineVisible()` 读取当前值；它不会修改应用状态。

### `color : QColor`

**作用与语义：**

该属性表示该系列的颜色。
这是`QLineSeries`或`QSplineSeries`时的线条（笔）颜色，`QScatterSeries`或`QAreaSeries`时的填充（画笔）颜色。

**如何使用：** 调用 `color()` 读取当前值；它不会修改应用状态。

### `pointLabelsClipping : bool`

**作用与语义：**

该属性包含数据点标签的裁剪。
该属性默认`true`。当开启裁剪时，图区域边缘的标签会被裁切。

**如何使用：** 调用 `pointLabelsClipping()` 读取当前值；它不会修改应用状态。

### `pointLabelsColor : QColor`

**作用与语义：**

该属性包含用于数据点标签的颜色。默认情况下，颜色是主题中定义的标签画刷颜色。

**如何使用：** 调用 `pointLabelsColor()` 读取当前值；它不会修改应用状态。

### `pointLabelsFont : QFont`

**作用与语义：**

该属性包含用于数据点标签的字体。

**如何使用：** 调用 `pointLabelsFont()` 读取当前值；它不会修改应用状态。

### `pointLabelsFormat : QString`

**作用与语义：**

该属性表示显示带有数据点标签的格式。
`QXYSeries` 支持以下格式标签：
- `@index`：数据点序列中的索引。[自6.5起]
- `@xPoint`：数据点的x坐标。
- `@yPoint`：数据点的y坐标。
例如，以下格式标签的使用方式会产生标签，显示用逗号（x， y）分隔的括号内显示的数据点：
默认情况下，标签格式设置为`@xPoint, @yPoint`。标签显示在图区上，图区边缘的标签被裁切。如果点彼此接近，标签可能会重叠。

**如何使用：** 调用 `pointLabelsFormat()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 series->setPointLabelsFormat("@index: (@xPoint, @yPoint)");
```

### `pointLabelsVisible : bool`

**作用与语义：**

该特性保持了数据点标签的可见性。
该属性默认`false`。

**如何使用：** 调用 `pointLabelsVisible()` 读取当前值；它不会修改应用状态。

### `pointsVisible : bool`

**作用与语义：**

该属性决定数据点是否可见并应绘制。

**如何使用：** 调用 `pointsVisible()` 读取当前值；它不会修改应用状态。

### `[since 6.2] selectedColor : QColor`

**作用与语义：**

该属性保留所选点的颜色。
这是标记为已选中的点的填充（画刷）颜色。如果未指定，默认使用`QXYSeries::color`值。

**如何使用：** 调用 `selectedColor()` 读取当前值；它不会修改应用状态。

### `[virtual noexcept] QXYSeries::~QXYSeries()`

**作用与语义：**

删除该系列。添加到`QChart`实例的系列归其所有，`QChart`实例被删除时也被删除。

### `void QXYSeries::append(qreal x, qreal y)`

**作用与语义：**

将坐标为`x`和`y`的数据点添加到系列中。

### `void QXYSeries::append(const QList<QPointF> &points)`

**作用与语义：**

将`points`指定的数据点列表添加到序列中。

### `void QXYSeries::append(const QPointF &point)`

**作用与语义：**

将数据点`point`添加到该系列中。

### `const QPointF &QXYSeries::at(int index) const`

**作用与语义：**

返回内部点序列中`index`指定位置的数据点。

### `[signal] void QXYSeries::bestFitLineColorChanged(const QColor &color)`

**作用与语义：**

该属性表示最佳拟合线的颜色。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `bestFitLineColor` 的变化，不要把它当作普通函数主动调用。

### `[since 6.2] QPair<qreal, qreal> QXYSeries::bestFitLineEquation(bool &ok) const`

**作用与语义：**

返回一对数字，其中第一个数字是斜率因子，第二个数字是线性函数的截距，该数值为最佳拟合线。
这些因子是基于传递到系列的点，使用最小二乘法计算的。
参数`ok`用于通过将其值设为`false`来报告失败，并通过将其值设为`true`来报告成功。

### `[signal] void QXYSeries::bestFitLineVisibilityChanged(bool visible)`

**作用与语义：**

该特性保持最佳拟合线的可见性。
该属性默认`false`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `bestFitLineVisible` 的变化，不要把它当作普通函数主动调用。

### `QBrush QXYSeries::brush() const`

**作用与语义：**

返回用于填充系列数据点的画刷。

### `void QXYSeries::clear()`

**作用与语义：**

取消系列中的所有积分。

### `[since 6.2] void QXYSeries::clearPointConfiguration(const int index)`

**作用与语义：**

移除位于`index`点的配置，恢复系列设置的默认外观。
注意：它不会影响其他点的配置。

### `[since 6.2] void QXYSeries::clearPointConfiguration(const int index, const QXYSeries::PointConfiguration key)`

**作用与语义：**

移除`key`在`index`点识别的配置属性，并恢复由系列设置衍生的默认外观。
通过配置自定义，移除`key`在`index`点指定的配置类型（如颜色或大小），使该配置属性能够作为系列属性中的默认值渲染。
注意：它不会影响其他点的配置。

### `[since 6.2] void QXYSeries::clearPointsConfiguration()`

**作用与语义：**

移除系列中所有点的配置，恢复由系列设置衍生的默认外观。

### `[since 6.2] void QXYSeries::clearPointsConfiguration(const QXYSeries::PointConfiguration key)`

**作用与语义：**

移除`key`所有点的配置属性，并恢复由系列设置衍生的默认外观。
移除所有带有配置自定义的点中`key`指定的配置类型（如颜色或大小），使该配置属性能够作为系列属性中指定的默认值渲染。

### `[signal] void QXYSeries::clicked(const QPointF &point)`

**作用与语义：**

当用户点击图表中的点`point`触发鼠标事件时，会发出该信号。

### `[since 6.2] void QXYSeries::colorBy(const QList<qreal> &sourceData, const QLinearGradient &gradient = QLinearGradient())`

**作用与语义：**

根据传递的值列表设置点的颜色。`sourceData`的值被排序并映射到`gradient`。
如果系列附着`QColorAxis`，则会使用从该轴的梯度。

### `[signal] void QXYSeries::colorChanged(QColor color)`

**作用与语义：**

该属性表示该系列的颜色。
这是`QLineSeries`或`QSplineSeries`时的线条（笔）颜色，`QScatterSeries`或`QAreaSeries`时的填充（画笔）颜色。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `color` 的变化，不要把它当作普通函数主动调用。

### `int QXYSeries::count() const`

**作用与语义：**

返回序列中的数据点数。

### `[since 6.2] void QXYSeries::deselectAllPoints()`

**作用与语义：**

取消了该系列中的所有点。
注意：`QXYSeries::selectedPointsChanged`。

### `[since 6.2] void QXYSeries::deselectPoint(int index)`

**作用与语义：**

在给定`index`处取消选择。
注意：`QXYSeries::selectedPointsChanged`。

### `[since 6.2] void QXYSeries::deselectPoints(const QList<int> &indexes)`

**作用与语义：**

在`indexes`列表中标记多个被取消的积分。
注意：发出`QXYSeries::selectedPointsChanged`。

### `[signal] void QXYSeries::doubleClicked(const QPointF &point)`

**作用与语义：**

当用户双击图表中`point`的数据点时，会发出该信号。`point`是第一次按下的触发点。

### `[signal] void QXYSeries::hovered(const QPointF &point, bool state)`

**作用与语义：**

当鼠标悬停在图表`point`点上时，该信号会发出。当鼠标移动到该点时，`state`转`true`，当鼠标再次移开时，`false`转。

### `void QXYSeries::insert(int index, const QPointF &point)`

**作用与语义：**

将`index`指定位置插入系列中`point`的数据点。

### `[since 6.2] bool QXYSeries::isPointSelected(int index)`

**作用与语义：**

如果在给定点 `index` 在选定点中，则返回 为真;否则返回为假。
注意：如果指定了颜色，选中的点将使用所选颜色绘制。

### `[since 6.2] const QImage &QXYSeries::lightMarker() const`

**作用与语义：**

获取用于绘制系列每个点标记的图像。
默认值为 QImage()，意味着不会绘制任何光标记。
光标记显示该系列的数据点，因此是`setPointsVisible`（真）的替代。这两个功能可以独立启用。
与`QScatterSeries`的元素不同，光标记不以`QGraphicsItem`表示，而是被绘制（不创建物体）。不过，`QXYSeries`的鼠标事件信号表现相同，这意味着点击/按压/悬停光标时，你会得到该点的精确域值。点击线条时，仍然会得到中间域值。光线标记在绘画和事件上都位于线上方。

### `[signal, since 6.2] void QXYSeries::lightMarkerChanged(const QImage &lightMarker)`

**作用与语义：**

当光线标记图像变为`lightMarker`时，该信号会发出。

### `[since 6.2] qreal QXYSeries::markerSize() const`

**作用与语义：**

获取用于渲染系列点的标记大小。
默认尺寸取决于具体的 `QXYSeries` 类型。`QScatterSeries` 默认是 15.0 `QLineSeries`默认是系列笔尺寸 * 1.5。

### `[signal] void QXYSeries::markerSizeChanged(qreal size)`

**作用与语义：**

当标记尺寸变为`size`时，该信号会发出。

### `QPen QXYSeries::pen() const`

**作用与语义：**

返回用于绘制该系列数据点轮廓的笔。

### `[signal] void QXYSeries::penChanged(const QPen &pen)`

**作用与语义：**

当笔变为`pen`时，会发出这个信号。

### `[signal] void QXYSeries::pointAdded(int index)`

**作用与语义：**

当在`index`指定位置添加一个点时，会发出该信号。

### `[since 6.2] QHash<QXYSeries::PointConfiguration, QVariant> QXYSeries::pointConfiguration(const int index) const`

**作用与语义：**

返回一个表示点在`index`的配置的映射。
通过点配置，你可以改变每个点外观的各个方面。

### `[signal] void QXYSeries::pointLabelsClippingChanged(bool clipping)`

**作用与语义：**

该属性包含数据点标签的裁剪。
该属性默认`true`。当开启裁剪时，图区域边缘的标签会被裁切。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `pointLabelsClipping` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QXYSeries::pointLabelsColorChanged(const QColor &color)`

**作用与语义：**

该属性包含用于数据点标签的颜色。默认情况下，颜色是主题中定义的标签画刷颜色。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `pointLabelsColor` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QXYSeries::pointLabelsFontChanged(const QFont &font)`

**作用与语义：**

该属性包含用于数据点标签的字体。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `pointLabelsFont` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QXYSeries::pointLabelsFormatChanged(const QString &format)`

**作用与语义：**

该属性表示显示带有数据点标签的格式。
`QXYSeries` 支持以下格式标签：
- `@index`：数据点序列中的索引。[自6.5起]
- `@xPoint`：数据点的x坐标。
- `@yPoint`：数据点的y坐标。
例如，以下格式标签的使用方式会产生标签，显示用逗号（x， y）分隔的括号内显示的数据点：
默认情况下，标签格式设置为`@xPoint, @yPoint`。标签显示在图区上，图区边缘的标签被裁切。如果点彼此接近，标签可能会重叠。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `pointLabelsFormat` 的变化，不要把它当作普通函数主动调用。

**官方示例：**

```cpp
 series->setPointLabelsFormat("@index: (@xPoint, @yPoint)");
```

### `[signal] void QXYSeries::pointLabelsVisibilityChanged(bool visible)`

**作用与语义：**

该特性保持了数据点标签的可见性。
该属性默认`false`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `pointLabelsVisible` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QXYSeries::pointRemoved(int index)`

**作用与语义：**

当某点从`index`指定位置移除时，该信号会发出。

### `[signal] void QXYSeries::pointReplaced(int index)`

**作用与语义：**

当点被替换到`index`指定位置时，该信号会发出。

### `QList<QPointF> QXYSeries::points() const`

**作用与语义：**

返回系列中的点数。

### `[since 6.2] QXYSeries::PointsConfigurationHash QXYSeries::pointsConfiguration() const`

**作用与语义：**

返回一个地图，键为点的索引，点的配置为值。

### `[signal] void QXYSeries::pointsRemoved(int index, int count)`

**作用与语义：**

当从`index`指定的位置开始移除`count`指定的点数时，该信号会发出。

### `[signal] void QXYSeries::pointsReplaced()`

**作用与语义：**

当所有点被其他点替换时，该信号会发出。

### `[signal] void QXYSeries::pressed(const QPointF &point)`

**作用与语义：**

当用户按下图表中的数据点`point`并按住鼠标按钮时，会发出该信号。

### `[signal] void QXYSeries::released(const QPointF &point)`

**作用与语义：**

当用户松开鼠标按压`point`指定的数据点时，该信号会发出。

### `void QXYSeries::remove(const QPointF &point)`

**作用与语义：**

将该数据点`point`从序列中移除。

### `void QXYSeries::remove(int index)`

**作用与语义：**

将`index`指定位置的点从系列中移除。

### `void QXYSeries::remove(qreal x, qreal y)`

**作用与语义：**

将坐标为`x`和`y`的点从系列中移除。

### `void QXYSeries::removePoints(int index, int count)`

**作用与语义：**

从`index`指定位置开始的系列中移除`count`指定的点数。

### `void QXYSeries::replace(const QList<QPointF> &points)`

**作用与语义：**

用`points`指定的点替换当前点。
注意：这比逐个替换数据点或先清除所有数据再添加新数据要快得多。当点被替换时会发出`QXYSeries::pointsReplaced()`。

### `void QXYSeries::replace(const QPointF &oldPoint, const QPointF &newPoint)`

**作用与语义：**

用`newPoint`指定的点替换`oldPoint`指定的点。

### `void QXYSeries::replace(int index, const QPointF &newPoint)`

**作用与语义：**

将`index`指定位置的点替换为`newPoint`指定的点。

### `void QXYSeries::replace(int index, qreal newX, qreal newY)`

**作用与语义：**

将`index`指定位置的点替换为坐标为`newX`和`newY`的点。

### `void QXYSeries::replace(qreal oldX, qreal oldY, qreal newX, qreal newY)`

**作用与语义：**

用坐标`oldX`替换点，`oldY`坐标为`newX`和`newY`。如果旧点不存在，则无效。

### `[since 6.2] void QXYSeries::selectAllPoints()`

**作用与语义：**

标记序列中的所有点为已选中，。
注意：会发出`QXYSeries::selectedPointsChanged`。

### `[since 6.2] void QXYSeries::selectPoint(int index)`

**作用与语义：**

标记指向`index`所选。
注意：`QXYSeries::selectedPointsChanged`。

### `[since 6.2] void QXYSeries::selectPoints(const QList<int> &indexes)`

**作用与语义：**

将`indexes`列表中通过的多个分标记为已选中。
注意：发出`QXYSeries::selectedPointsChanged`。

### `[since 6.2] const QImage &QXYSeries::selectedLightMarker() const`

**作用与语义：**

返回用于在选定系列点上绘制标记的图像。
默认值为 QImage()，意味着会绘制常规`lightMarker()`。
如果你更喜欢光线标记而非普通点，但仍想区分选中的点，这相当于`selectedColor`。

### `[since 6.2] QList<int> QXYSeries::selectedPoints() const`

**作用与语义：**

返回标记为已选中的点索引列表。无论点是否可见，选中的点都是可见的。

### `[signal] void QXYSeries::selectedPointsChanged()`

**作用与语义：**

当点选择发生变化时，会发出该信号。

### `[virtual] void QXYSeries::setBrush(const QBrush &brush)`

**作用与语义：**

将用于绘制图表点的画笔设置为`brush`。如果画笔未定义，则使用图表主题设置中的画笔。

### `[since 6.2] void QXYSeries::setLightMarker(const QImage &lightMarker)`

**作用与语义：**

将用于绘制系列中每个点标记的图像设置为`lightMarker`值。
默认值是 default-QImage() （`QImage::isNull()` == true），意味着不会被绘制光标记。你可以通过调用该函数并用空`QImage`（QImage()）重置回默认值（禁用）。
光标显示该系列的数据点，因此是`setPointsVisible(true)`的替代方案。如果用该方法设置光标，`setPointsVisible(true)`设置的可见点不会显示。
与`QScatterSeries`元素不同，光标记不以`QGraphicsItem`表示，只是被绘制（没有创建物体）。不过，`QXYSeries`的鼠标事件信号表现相同，这意味着如果你点击/按压/悬停光标记，会得到该点的精确域值。点击线条时，你仍然会得到介于两者之间的领域值。光线标记在绘制和事件上都位于线上方。

### `[since 6.2] void QXYSeries::setMarkerSize(qreal size)`

**作用与语义：**

设置用于渲染系列中点的标记器的标记值`size`。
默认大小是15.0。

### `[virtual] void QXYSeries::setPen(const QPen &pen)`

**作用与语义：**

将用于绘制图表点的笔设置为`pen`。如果笔未定义，则使用图表主题中的笔。

### `[since 6.2] void QXYSeries::setPointConfiguration(const int index, const QHash<QXYSeries::PointConfiguration, QVariant> &configuration)`

**作用与语义：**

允许自定义位于`index`且具有所需`configuration`的点的外观。
通过点配置，你可以改变每个点外观的各个方面。
点的配置表示为带有`QXYSeries::pointConfiguration`键和`QVariant`值的哈希映射。例如：
在这个例子中，你可以看到一个默认`QLineSeries`，有10个点，并且两个点的配置发生了变化。这两个变化后的点都明显比其他点大，外观是基于系列配置的。默认情况下，点没有标签，但索引4的点由于`QXYSeries::PointConfiguration::LabelVisibility`和`QXYSeries::PointConfiguration::LabelFormat`配置值而有标签。索引6的点由于`QXYSeries::PointConfiguration::LabelFormat`配置值，有自定义标签“此点”。下面是一个以此方式创建的图表示例：

**官方示例：**

```cpp
 QLineSeries *series = new QLineSeries();
 series->setName("Customized series");
 series->setPointsVisible(true);

 *series << QPointF(0, 6) << QPointF(2, 4) << QPointF(3, 6) << QPointF(7, 4) << QPointF(10, 5)
         << QPointF(11, 1) << QPointF(13, 3) << QPointF(17, 6) << QPointF(18, 3)
         << QPointF(20, 2);

 QChart *chart = new QChart();
 chart->addSeries(series);
 chart->createDefaultAxes();

 QHash<QXYSeries::PointConfiguration, QVariant> conf;
 conf[QXYSeries::PointConfiguration::Color] = QColor(Qt::red);
 conf[QXYSeries::PointConfiguration::Size] = 8;
 conf[QXYSeries::PointConfiguration::LabelVisibility] = true;

 series->setPointConfiguration(4, conf);

 conf.remove(QXYSeries::PointConfiguration::Color);
 conf[QXYSeries::PointConfiguration::LabelFormat] = "This Point";
 series->setPointConfiguration(6, conf);
```

### `[since 6.2] void QXYSeries::setPointConfiguration(const int index, const QXYSeries::PointConfiguration key, const QVariant &value)`

**作用与语义：**

允许自定义点配置的特定方面。
注意：点配置概念为配置点外观的各个方面提供了灵活的方式。因此，值需要有弹性类型，如`QVariant`。参见`QXYSeries::PointConfiguration`以了解某些`key`应传递哪些 `value`。

### `[since 6.2] void QXYSeries::setPointSelected(int index, bool selected)`

**作用与语义：**

标记在指定`index`中被选中或取消，均由`selected`指定。
注意：选中的点如果指定了颜色，则使用选定颜色绘制。发射`QXYSeries::selectedPointsChanged`。

### `[since 6.2] void QXYSeries::setPointsConfiguration(const QHash<int, QHash<QXYSeries::PointConfiguration, QVariant>> &pointsConfiguration)`

**作用与语义：**

允许根据`pointsConfiguration`指定自定义多点配置。

### `[since 6.2] void QXYSeries::setSelectedLightMarker(const QImage &selectedLightMarker)`

**作用与语义：**

将用于在选定系列点上绘制标记的图像设置为`selectedLightMarker`。
默认值为 QImage()，意味着会绘制常用的 `lightMarker()`。
如果你喜欢光线标记而非普通点，但仍想区分选中的点，这对`selectedColor`来说是相当的。

### `[since 6.2] void QXYSeries::sizeBy(const QList<qreal> &sourceData, const qreal minSize, const qreal maxSize)`

**作用与语义：**

根据传递的值列表设置点的大小。`sourceData`的值被排序并映射到介于`minSize`到`maxSize`之间的点大小。
注意：如果`sourceData`长度小于系列中的点数，则系列结束时点数的大小保持不变。

### `[since 6.2] void QXYSeries::toggleSelection(const QList<int> &indexes)`

**作用与语义：**

将给定`indexes`点的选择状态变为相反的点。制造。
注意：发出`QXYSeries::selectedPointsChanged`。

### `QXYSeries &QXYSeries::operator<<(const QList<QPointF> &points)`

**作用与语义：**

流算子，用于将`points`指定的数据点列表添加到系列中。

### `QXYSeries &QXYSeries::operator<<(const QPointF &point)`

**作用与语义：**

用于将数据点`point`添加到系列中的流算子。

### `QColor bestFitLineColor() const`

**作用与语义：**

该属性表示最佳拟合线的颜色。

**如何使用：** 调用 `bestFitLineColor()` 读取当前值；它不会修改应用状态。

### `bool bestFitLineVisible() const`

**作用与语义：**

该特性保持最佳拟合线的可见性。
该属性默认`false`。

**如何使用：** 调用 `bestFitLineVisible()` 读取当前值；它不会修改应用状态。

### `virtual QColor color() const`

**作用与语义：**

该属性保留所选点的颜色。
这是标记为已选中的点的填充（画刷）颜色。如果未指定，默认使用`QXYSeries::color`值。

**如何使用：** 调用 `color()` 读取当前值；它不会修改应用状态。

### `bool pointLabelsClipping() const`

**作用与语义：**

该属性包含数据点标签的裁剪。
该属性默认`true`。当开启裁剪时，图区域边缘的标签会被裁切。

**如何使用：** 调用 `pointLabelsClipping()` 读取当前值；它不会修改应用状态。

### `QColor pointLabelsColor() const`

**作用与语义：**

该属性包含用于数据点标签的颜色。默认情况下，颜色是主题中定义的标签画刷颜色。

**如何使用：** 调用 `pointLabelsColor()` 读取当前值；它不会修改应用状态。

### `QFont pointLabelsFont() const`

**作用与语义：**

该属性包含用于数据点标签的字体。

**如何使用：** 调用 `pointLabelsFont()` 读取当前值；它不会修改应用状态。

### `QString pointLabelsFormat() const`

**作用与语义：**

该属性表示显示带有数据点标签的格式。
`QXYSeries` 支持以下格式标签：
- `@index`：数据点序列中的索引。[自6.5起]
- `@xPoint`：数据点的x坐标。
- `@yPoint`：数据点的y坐标。
例如，以下格式标签的使用方式会产生标签，显示用逗号（x， y）分隔的括号内显示的数据点：
默认情况下，标签格式设置为`@xPoint, @yPoint`。标签显示在图区上，图区边缘的标签被裁切。如果点彼此接近，标签可能会重叠。

**如何使用：** 调用 `pointLabelsFormat()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 series->setPointLabelsFormat("@index: (@xPoint, @yPoint)");
```

### `bool pointLabelsVisible() const`

**作用与语义：**

该特性保持了数据点标签的可见性。
该属性默认`false`。

**如何使用：** 调用 `pointLabelsVisible()` 读取当前值；它不会修改应用状态。

### `bool pointsVisible() const`

**作用与语义：**

该属性决定数据点是否可见并应绘制。

**如何使用：** 调用 `pointsVisible()` 读取当前值；它不会修改应用状态。

### `void setBestFitLineColor(const QColor &color)`

**作用与语义：**

该属性表示最佳拟合线的颜色。

**如何使用：** 调用 `setBestFitLineColor(...)` 修改 `bestFitLineColor`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setBestFitLineVisible(bool visible = true)`

**作用与语义：**

该特性保持最佳拟合线的可见性。
该属性默认`false`。

**如何使用：** 调用 `setBestFitLineVisible(...)` 修改 `bestFitLineVisible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `virtual void setColor(const QColor &color)`

**作用与语义：**

该属性表示该系列的颜色。
这是`QLineSeries`或`QSplineSeries`时的线条（笔）颜色，`QScatterSeries`或`QAreaSeries`时的填充（画笔）颜色。

**如何使用：** 调用 `setColor(...)` 修改 `color`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPointLabelsClipping(bool enabled = true)`

**作用与语义：**

该属性包含数据点标签的裁剪。
该属性默认`true`。当开启裁剪时，图区域边缘的标签会被裁切。

**如何使用：** 调用 `setPointLabelsClipping(...)` 修改 `pointLabelsClipping`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPointLabelsColor(const QColor &color)`

**作用与语义：**

该属性包含用于数据点标签的颜色。默认情况下，颜色是主题中定义的标签画刷颜色。

**如何使用：** 调用 `setPointLabelsColor(...)` 修改 `pointLabelsColor`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPointLabelsFont(const QFont &font)`

**作用与语义：**

该属性包含用于数据点标签的字体。

**如何使用：** 调用 `setPointLabelsFont(...)` 修改 `pointLabelsFont`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPointLabelsFormat(const QString &format)`

**作用与语义：**

该属性表示显示带有数据点标签的格式。
`QXYSeries` 支持以下格式标签：
- `@index`：数据点序列中的索引。[自6.5起]
- `@xPoint`：数据点的x坐标。
- `@yPoint`：数据点的y坐标。
例如，以下格式标签的使用方式会产生标签，显示用逗号（x， y）分隔的括号内显示的数据点：
默认情况下，标签格式设置为`@xPoint, @yPoint`。标签显示在图区上，图区边缘的标签被裁切。如果点彼此接近，标签可能会重叠。

**如何使用：** 调用 `setPointLabelsFormat(...)` 修改 `pointLabelsFormat`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 series->setPointLabelsFormat("@index: (@xPoint, @yPoint)");
```

### `void setPointLabelsVisible(bool visible = true)`

**作用与语义：**

该特性保持了数据点标签的可见性。
该属性默认`false`。

**如何使用：** 调用 `setPointLabelsVisible(...)` 修改 `pointLabelsVisible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPointsVisible(bool visible = true)`

**作用与语义：**

该属性决定数据点是否可见并应绘制。

**如何使用：** 调用 `setPointsVisible(...)` 修改 `pointsVisible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSelectedColor(const QColor &color)`

**作用与语义：**

该属性保留所选点的颜色。
这是标记为已选中的点的填充（画刷）颜色。如果未指定，默认使用`QXYSeries::color`值。

**如何使用：** 调用 `setSelectedColor(...)` 修改 `selectedColor`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void selectedColorChanged(const QColor &color)`

**作用与语义：**

该属性保留所选点的颜色。
这是标记为已选中的点的填充（画刷）颜色。如果未指定，默认使用`QXYSeries::color`值。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `selectedColor` 的变化，不要把它当作普通函数主动调用。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

### 状态和错误边界

QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

### 线程边界

QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

### 最容易出现的错误

不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QXYSeries` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
