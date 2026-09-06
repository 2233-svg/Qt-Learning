# QPageLayout

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QPageLayout` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QPageLayout` 是 Qt Widgets 界面机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Widgets 通过父子控件树、布局系统、事件分发和重绘请求组成界面。控件的可见区域、sizeHint、sizePolicy、字体和平台 style 共同影响最终几何；用户输入先进入 Qt 事件系统，再由控件的事件函数、信号或快捷键处理。

**适用场景：** 创建 QApplication 后创建控件，设置 parent 或把控件加入布局，连接用户操作信号，再显示顶层窗口。复合界面用布局嵌套；控件尺寸异常时同时检查 sizePolicy、minimum/maximum size、layout stretch、margins 和 spacing。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要用固定坐标拼接响应式界面；不要给已经加入布局的控件反复 `setGeometry()`；不要在 `paintEvent()` 中修改业务状态；不要忘记窗口关闭、对象销毁和应用退出是三个不同事件。

## 2. 依赖与对象关系

- 头文件：`#include <QPageLayout>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

Widgets 通过父子控件树、布局系统、事件分发和重绘请求组成界面。控件的可见区域、sizeHint、sizePolicy、字体和平台 style 共同影响最终几何；用户输入先进入 Qt 事件系统，再由控件的事件函数、信号或快捷键处理。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

创建 QApplication 后创建控件，设置 parent 或把控件加入布局，连接用户操作信号，再显示顶层窗口。复合界面用布局嵌套；控件尺寸异常时同时检查 sizePolicy、minimum/maximum size、layout stretch、margins 和 spacing。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum Mode { StandardMode, FullPageMode }`
- `enum Orientation { Portrait, Landscape }`
- `(since 6.8) enum class OutOfBoundsPolicy { Reject, Clamp }`
- `enum Unit { Millimeter, Point, Inch, Pica, Didot, Cicero }`

### 公有函数

- `QPageLayout()`
- `QPageLayout(const QPageSize &pageSize, QPageLayout::Orientation orientation, const QMarginsF &margins, QPageLayout::Unit units = Point, const QMarginsF &minMargins = QMarginsF(0, 0, 0, 0))`
- `QPageLayout(const QPageLayout &other)`
- `~QPageLayout()`
- `QRectF fullRect() const`
- `QRectF fullRect(QPageLayout::Unit units) const`
- `QRect fullRectPixels(int resolution) const`
- `QRect fullRectPoints() const`
- `bool isEquivalentTo(const QPageLayout &other) const`
- `bool isValid() const`
- `QMarginsF margins() const`
- `QMarginsF margins(QPageLayout::Unit units) const`
- `QMargins marginsPixels(int resolution) const`
- `QMargins marginsPoints() const`
- `QMarginsF maximumMargins() const`
- `QMarginsF minimumMargins() const`
- `QPageLayout::Mode mode() const`
- `QPageLayout::Orientation orientation() const`
- `QPageSize pageSize() const`
- `QRectF paintRect() const`
- `QRectF paintRect(QPageLayout::Unit units) const`
- `QRect paintRectPixels(int resolution) const`
- `QRect paintRectPoints() const`
- `bool setBottomMargin(qreal bottomMargin, QPageLayout::OutOfBoundsPolicy outOfBoundsPolicy = OutOfBoundsPolicy::Reject)`
- `bool setLeftMargin(qreal leftMargin, QPageLayout::OutOfBoundsPolicy outOfBoundsPolicy = OutOfBoundsPolicy::Reject)`
- `bool setMargins(const QMarginsF &margins, QPageLayout::OutOfBoundsPolicy outOfBoundsPolicy = OutOfBoundsPolicy::Reject)`
- `void setMinimumMargins(const QMarginsF &minMargins)`
- `void setMode(QPageLayout::Mode mode)`
- `void setOrientation(QPageLayout::Orientation orientation)`
- `void setPageSize(const QPageSize &pageSize, const QMarginsF &minMargins = QMarginsF(0, 0, 0, 0))`
- `bool setRightMargin(qreal rightMargin, QPageLayout::OutOfBoundsPolicy outOfBoundsPolicy = OutOfBoundsPolicy::Reject)`
- `bool setTopMargin(qreal topMargin, QPageLayout::OutOfBoundsPolicy outOfBoundsPolicy = OutOfBoundsPolicy::Reject)`
- `void setUnits(QPageLayout::Unit units)`
- `void swap(QPageLayout &other)`
- `QPageLayout::Unit units() const`
- `QPageLayout & operator=(QPageLayout &&other)`
- `QPageLayout & operator=(const QPageLayout &other)`

### 相关非成员函数

- `bool operator!=(const QPageLayout &lhs, const QPageLayout &rhs)`
- `bool operator==(const QPageLayout &lhs, const QPageLayout &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QPageLayout::Mode`

**作用与语义：**

定义页面布局模式。
- `QPageLayout::StandardMode`：`0`;Paint Rect 包含边距，边距必须位于最小和最大之间。
- `QPageLayout::FullPageMode`：`1`;Paint Rect 排除边距，边距可以是任意值，必须手动管理。
在StandardMode中，设置裕量时，使用`Clamp`自动夹紧裕量，使其落在最小允许值和最大值之间。

### `enum QPageLayout::Orientation`

**作用与语义：**

该枚举类型定义了页面方向。
- `QPageLayout::Portrait`：`0`;页面大小以其默认方向使用
- `QPageLayout::Landscape`：`1`;页面尺寸旋转90度
注意，一些标准页面尺寸定义宽度大于其高度，因此方向相对于标准页面尺寸定义，而非使用相对页面尺寸。

### `[since 6.8] enum class QPageLayout::OutOfBoundsPolicy`

**作用与语义：**

定义了边界外的政策。
- `QPageLayout::OutOfBoundsPolicy::Reject`：`0`;边距必须落在最小值和最大值内，否则将被拒绝。
- `QPageLayout::OutOfBoundsPolicy::Clamp`：`1`;边缘被夹在最小值和最大值之间，以确保其有效。
注意：该政策在接受所有保证金的 `FullPageMode` 中无效。
这个枚举是在Qt 6.8引入的。

### `enum QPageLayout::Unit`

**作用与语义：**

该枚举类型用于指定页面布局和边距的计量单位。
- `QPageLayout::Millimeter`：`0`
- `QPageLayout::Point`：`1`;1/72英寸
- `QPageLayout::Inch`：`2`
- `QPageLayout::Pica`：`3`;1/72英尺，1/6英寸，12分
- `QPageLayout::Didot`：`4`;1/72法式英寸，0.375毫米
- `QPageLayout::Cicero`：`5`;1/6英镑，12迪多特，4.5毫米

### `QPageLayout::QPageLayout()`

**作用与语义：**

生成一个无效的QPageLayout。

### `QPageLayout::QPageLayout(const QPageSize &pageSize, QPageLayout::Orientation orientation, const QMarginsF &margins, QPageLayout::Unit units = Point, const QMarginsF &minMargins = QMarginsF(0, 0, 0, 0))`

**作用与语义：**

创建包含给定`pageSize`、`orientation`和`margins`的QPageLayout，`units`中。
可选地定义最小允许的边际，例如物理打印设备能打印的最小边际`minMargins`。
构建好的QPageLayout将会在`StandardMode`中。
所给`margins`将根据页面大小限制在最小边距和最大边距。

### `QPageLayout::QPageLayout(const QPageLayout &other)`

**作用与语义：**

复制构造器，复制`other`到这里。

### `[noexcept] QPageLayout::~QPageLayout()`

**作用与语义：**

这会破坏页面布局。

### `QRectF QPageLayout::fullRect() const`

**作用与语义：**

返回当前布局单元中的整页矩形。
页面矩形考虑了页面大小和页面方向，但不考虑页边距。

### `QRectF QPageLayout::fullRect(QPageLayout::Unit units) const`

**作用与语义：**

以所需`units`返回整页矩形。
页面矩形考虑了页面大小和页面方向，但不考虑页边距。

### `QRect QPageLayout::fullRectPixels(int resolution) const`

**作用与语义：**

返回给定`resolution`的整页矩形（单位为设备像素）。
页面矩形考虑了页面大小和页面方向，但不考虑页边距。

### `QRect QPageLayout::fullRectPoints() const`

**作用与语义：**

返回整页矩形（Postscript Points，1/72英寸）。
页面矩形考虑了页面大小和页面方向，但不考虑页边距。

### `bool QPageLayout::isEquivalentTo(const QPageLayout &other) const`

**作用与语义：**

返回`true`，如果该页面布局与`other`版面布局等价，即页面大小、边距和方向是否相同。

### `bool QPageLayout::isValid() const`

**作用与语义：**

如果该页面布局有效，返回`true`。

### `QMarginsF QPageLayout::margins() const`

**作用与语义：**

返回使用当前设置单位的页面布局页边距。

### `QMarginsF QPageLayout::margins(QPageLayout::Unit units) const`

**作用与语义：**

返回页面布局的页边距，使用请求的 `units`。

### `QMargins QPageLayout::marginsPixels(int resolution) const`

**作用与语义：**

返回给定 `resolution` 页面布局的边距（设备像素）。

### `QMargins QPageLayout::marginsPoints() const`

**作用与语义：**

返回页面布局的边距（Postscript Points，1/72英寸）。

### `QMarginsF QPageLayout::maximumMargins() const`

**作用与语义：**

返回如果页面布局为`StandardMode`时应用的最大边距。
允许的最大边距计算为页面总尺寸减去设定的最小边距。例如，如果页宽为100分，右边距最小为10分，那么左边距最大为90分。

### `QMarginsF QPageLayout::minimumMargins() const`

**作用与语义：**

返回页面布局的最小边距。

### `QPageLayout::Mode QPageLayout::mode() const`

**作用与语义：**

返回页面布局模式。

### `QPageLayout::Orientation QPageLayout::orientation() const`

**作用与语义：**

返回页面布局的页面方向。

### `QPageSize QPageLayout::pageSize() const`

**作用与语义：**

返回页面布局的页面大小。
注意`QPageSize`始终以竖向方向定义。要获得考虑该集合方向的尺寸，必须使用`fullRect()`。

### `QRectF QPageLayout::paintRect() const`

**作用与语义：**

返回当前布局单元中的页面矩形。
可绘制的矩形会考虑页面大小、方向和边距。
如果设置了`FullPageMode`模式，则`fullRect()`返回，边距必须手动管理。

### `QRectF QPageLayout::paintRect(QPageLayout::Unit units) const`

**作用与语义：**

返回页面矩形，按要求的`units`返回。
可绘制的矩形会考虑页面大小、方向和边距。
如果设置了`FullPageMode`模式，则`fullRect()`返回，边距必须手动管理。

### `QRect QPageLayout::paintRectPixels(int resolution) const`

**作用与语义：**

在给定`resolution`下返回可绘制的矩形，以圆角的设备像素表示。
可绘制的矩形会考虑页面大小、方向和边距。
如果设置了`FullPageMode`模式，则返回`fullRect()`，且必须手动管理边距。

### `QRect QPageLayout::paintRectPoints() const`

**作用与语义：**

返回可绘制的矩形，以圆角的后记点（1/72英寸）表示。
可绘制的矩形会考虑页面大小、方向和边距。
如果设置了`FullPageMode`模式，则返回`fullRect()`，边距必须手动管理。

### `bool QPageLayout::setBottomMargin(qreal bottomMargin, QPageLayout::OutOfBoundsPolicy outOfBoundsPolicy = OutOfBoundsPolicy::Reject)`

**作用与语义：**

将页面布局的底部页距设置为`bottomMargin`。如果边界成功设置，则返回为真。
所使用的单位是当前为布局定义的单位。要使用不同单位，请先调用`setUnits()`。
自Qt 6.8起，可选`outOfBoundsPolicy`可用于指定边界外的处理方式。

### `bool QPageLayout::setLeftMargin(qreal leftMargin, QPageLayout::OutOfBoundsPolicy outOfBoundsPolicy = OutOfBoundsPolicy::Reject)`

**作用与语义：**

将页面布局的左侧页距设为`leftMargin`。如果页距成功设置，则返回为真。
所用单位为当前布局中定义的单位。要使用不同单位，请先调用`setUnits()`。
自Qt 6.8起，可选`outOfBoundsPolicy`可用于指定边界外的处理方式。

### `bool QPageLayout::setMargins(const QMarginsF &margins, QPageLayout::OutOfBoundsPolicy outOfBoundsPolicy = OutOfBoundsPolicy::Reject)`

**作用与语义：**

将页面布局的页边距设置为`margins`。如果边距成功设置，则返回为真。
所用单位为当前布局定义的单位。如需使用不同单位，请先联系`setUnits()`。
自Qt 6.8起，可选`outOfBoundsPolicy`可用于指定边界外的处理方式。

### `void QPageLayout::setMinimumMargins(const QMarginsF &minMargins)`

**作用与语义：**

将页面布局的最小页距设置为`minMargins`。
不建议覆盖页面尺寸的默认值，因为这可能是物理打印设备的最小可打印区域。
如果设置了`StandardMode`模式，则现有边距将被固定到新`minMargins`和页面大小允许的最大值上。如果`FullPageMode`设置好，则现有边距保持不变。

### `void QPageLayout::setMode(QPageLayout::Mode mode)`

**作用与语义：**

将页面布局模式设置为`mode`。

### `void QPageLayout::setOrientation(QPageLayout::Orientation orientation)`

**作用与语义：**

将页面布局的页面方向设置为`orientation`。
改变方向不会影响当前的裕度或最小的裕度。

### `void QPageLayout::setPageSize(const QPageSize &pageSize, const QMarginsF &minMargins = QMarginsF(0, 0, 0, 0))`

**作用与语义：**

将页面布局的页面大小设置为`pageSize`。
可选地定义最小允许边距`minMargins`，例如物理打印设备可打印的最小边际，否则最小边距默认为0。
如果`StandardMode`设置，现有边距将被固定为新的最小边距和页码允许的最大边距。如果`FullPageMode`设定，则现有边距保持不变。

### `bool QPageLayout::setRightMargin(qreal rightMargin, QPageLayout::OutOfBoundsPolicy outOfBoundsPolicy = OutOfBoundsPolicy::Reject)`

**作用与语义：**

将页面布局的右页边距设置为`rightMargin`。如果边距成功设置，则返回为真。
所使用的单位是当前布局中定义的单位。要使用不同单位，首先调用`setUnits()`。
自Qt 6.8起，可选`outOfBoundsPolicy`可用于指定边界外的处理方式。

### `bool QPageLayout::setTopMargin(qreal topMargin, QPageLayout::OutOfBoundsPolicy outOfBoundsPolicy = OutOfBoundsPolicy::Reject)`

**作用与语义：**

将页面布局的顶页边距设置为`topMargin`。如果边距成功设置，则返回真。
所用单位为当前布局定义的单位。要使用不同单位，请先调用`setUnits()`。
自Qt 6.8起，可选`outOfBoundsPolicy`可用于指定边界外的管理方式。

### `void QPageLayout::setUnits(QPageLayout::Unit units)`

**作用与语义：**

设置用于定义页面布局的`units`。

### `[noexcept] void QPageLayout::swap(QPageLayout &other)`

**作用与语义：**

将页面布局与`other`互换。这个操作非常快，从未出错。

### `QPageLayout::Unit QPageLayout::units() const`

**作用与语义：**

返回当前定义页面布局的单位。

### `[noexcept] QPageLayout &QPageLayout::operator=(QPageLayout &&other)`

**作用与语义：**

Move-Assign `other`到该`QPageLayout`实例，将管理指针的所有权转移到该实例。

### `QPageLayout &QPageLayout::operator=(const QPageLayout &other)`

**作用与语义：**

赋值操作员，将`other`分配到这里。

### `bool operator!=(const QPageLayout &lhs, const QPageLayout &rhs)`

**作用与语义：**

如果页面布局`lhs`与页面布局`rhs`不相同，即任何属性不同，返回`true`。
注意，这是一个严格的等值，尤其是在页面大小上，`QPageSize` ID、名称和大小必须完全匹配，边距也必须匹配单位。

### `bool operator==(const QPageLayout &lhs, const QPageLayout &rhs)`

**作用与语义：**

返回`true`：如果页面布局`lhs`等于页面布局`rhs`，即所有属性完全相等。
注意这是一个严格的等式，尤其是在页面大小中，`QPageSize` ID、名称和大小必须完全匹配，边距也必须单位匹配。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

不要用固定坐标拼接响应式界面；不要给已经加入布局的控件反复 `setGeometry()`；不要在 `paintEvent()` 中修改业务状态；不要忘记窗口关闭、对象销毁和应用退出是三个不同事件。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QPageLayout` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
