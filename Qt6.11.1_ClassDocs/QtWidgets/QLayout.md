# QLayout

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QLayout` 是 布局管理机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QLayout` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QLayout>`
- 继承自：QObject、QLayoutItem
- 直接派生类：QBoxLayout、QFormLayout、QGridLayout,、QStackedLayout

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

### 状态、生命周期和线程

**生命周期：** 顶层布局可以在构造时绑定到 QWidget，也可以通过 `setLayout()` 安装；嵌套布局加入父布局后所有权交给父布局。布局析构不会自动销毁普通 QWidget，动态移除项目时要分别处理控件、子布局和 spacer。

**状态与结果：** 布局的项目索引会随着 add、insert、remove 和 takeAt 改变；索引既包括控件，也包括子布局、固定空白和 stretch。修改项目或尺寸参数后 Qt 会使布局失效并重新计算。

**线程与事件循环：** 布局只应在 GUI 线程操作，因为它直接改变 QWidget 几何和可见界面。布局系统不负责业务线程同步，也不会把手动的跨线程控件访问变安全。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum SizeConstraint { SetDefaultConstraint, SetFixedSize, SetMinimumSize, SetMaximumSize, SetMinAndMaxSize, SetNoConstraint }`

### 属性

- `contentsMargins : QMargins`
- `(since 6.10) horizontalSizeConstraint : SizeConstraint`
- `sizeConstraint : SizeConstraint`
- `spacing : int`
- `(since 6.10) verticalSizeConstraint : SizeConstraint`

### 公有函数

- `QLayout(QWidget *parent = nullptr)`
- `bool activate()`
- `virtual void addItem(QLayoutItem *item) = 0`
- `void addWidget(QWidget *w)`
- `QMargins contentsMargins() const`
- `QRect contentsRect() const`
- `virtual int count() const = 0`
- `void getContentsMargins(int *left, int *top, int *right, int *bottom) const`
- `QLayout::SizeConstraint horizontalSizeConstraint() const`
- `virtual int indexOf(const QLayoutItem *layoutItem) const`
- `virtual int indexOf(const QWidget *widget) const`
- `bool isEnabled() const`
- `virtual QLayoutItem * itemAt(int index) const = 0`
- `QWidget * menuBar() const`
- `QWidget * parentWidget() const`
- `void removeItem(QLayoutItem *item)`
- `void removeWidget(QWidget *widget)`
- `virtual QLayoutItem * replaceWidget(QWidget *from, QWidget *to, Qt::FindChildOptions options = Qt::FindChildrenRecursively)`
- `bool setAlignment(QWidget *w, Qt::Alignment alignment)`
- `bool setAlignment(QLayout *l, Qt::Alignment alignment)`
- `void setContentsMargins(const QMargins &margins)`
- `void setContentsMargins(int left, int top, int right, int bottom)`
- `void setEnabled(bool enable)`
- `void setHorizontalSizeConstraint(QLayout::SizeConstraint constraint)`
- `void setMenuBar(QWidget *widget)`
- `void setSizeConstraint(QLayout::SizeConstraint constraint)`
- `(since 6.10) void setSizeConstraints(QLayout::SizeConstraint horizontal, QLayout::SizeConstraint vertical)`
- `virtual void setSpacing(int)`
- `void setVerticalSizeConstraint(QLayout::SizeConstraint constraint)`
- `QLayout::SizeConstraint sizeConstraint() const`
- `virtual int spacing() const`
- `virtual QLayoutItem * takeAt(int index) = 0`
- `(since 6.1) void unsetContentsMargins()`
- `void update()`
- `QLayout::SizeConstraint verticalSizeConstraint() const`

### 重实现的公有函数

- `virtual QSizePolicy::ControlTypes controlTypes() const override`
- `virtual Qt::Orientations expandingDirections() const override`
- `virtual QRect geometry() const override`
- `virtual void invalidate() override`
- `virtual bool isEmpty() const override`
- `virtual QLayout * layout() override`
- `virtual QSize maximumSize() const override`
- `virtual QSize minimumSize() const override`
- `virtual void setGeometry(const QRect &r) override`

### 静态公有成员

- `QSize closestAcceptableSize(const QWidget *widget, const QSize &size)`

### 保护函数

- `void addChildLayout(QLayout *childLayout)`
- `void addChildWidget(QWidget *w)`
- `QRect alignmentRect(const QRect &r) const`

### 重实现的保护函数

- `virtual void childEvent(QChildEvent *e) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QLayout::SizeConstraint`

**作用与语义：**

描述布局如何限制小部件的大小。
垂直约束影响小部件的高度，而水平约束则影响其宽度。
可能的数值如下：
- `QLayout::SetDefaultConstraint`：`0`;在受限方向下，控件的最小范围设置为`minimumSize()`，除非最小大小已被设置。
- `QLayout::SetFixedSize`：`3`;在受限方向下，控件的范围设置为`sizeHint()`，且不能在该方向调整大小。
- `QLayout::SetMinimumSize`：`2`;在受限方向下，控件的最小范围设置为`minimumSize()`。
- `QLayout::SetMaximumSize`：`4`;在受限方向下，小部件的最大范围设置为`maximumSize()`。
- `QLayout::SetMinAndMaxSize`：`5`;在受限方向下，控件的最小范围设置为`minimumSize()`，最大范围设置为`maximumSize()`。
- `QLayout::SetNoConstraint`：`1`;控件不施加大小约束。

### `contentsMargins : QMargins`

**作用与语义：**

该特性保留了布局周围的边界。
默认情况下，`QLayout`使用样式提供的数值。在大多数平台上，边界在所有方向上都是11像素。

**如何使用：** 调用 `contentsMargins()` 读取当前值；它不会修改应用状态。

### `[since 6.10] horizontalSizeConstraint : SizeConstraint`

**作用与语义：**

该属性表示水平尺寸约束。
默认模式是`QLayout::SetDefaultConstraint`。

**如何使用：** 调用 `horizontalSizeConstraint()` 读取当前值；它不会修改应用状态。

### `sizeConstraint : SizeConstraint`

**作用与语义：**

该属性保留了布局的缩放模式。设置对话框的大小约束。设置垂直或水平大小约束则覆盖此约束。
默认模式是`SetDefaultConstraint`。

**如何使用：** 调用 `sizeConstraint()` 读取当前值；它不会修改应用状态。

### `spacing : int`

**作用与语义：**

该属性保留了布局中小部件之间的间距。
如果没有明确设置值，布局的间距会继承自父布局，或父控件的样式设置。
对于`QGridLayout`和`QFormLayout`，可以使用`setHorizontalSpacing()`和`setVerticalSpacing()`设置不同的水平和垂直间距。此时，spacing() 返回 -1。

**如何使用：** 调用 `spacing()` 读取当前值；它不会修改应用状态。

### `[since 6.10] verticalSizeConstraint : SizeConstraint`

**作用与语义：**

该属性表示垂直尺寸约束。
默认模式是`QLayout::SetDefaultConstraint`。

**如何使用：** 调用 `verticalSizeConstraint()` 读取当前值；它不会修改应用状态。

### `[explicit] QLayout::QLayout(QWidget *parent = nullptr)`

**作用与语义：**

构建一个新的顶层QLayout，带有父`parent`。
布局直接设置为`parent`的顶层布局。一个小部件只能有一个顶层布局。它由`QWidget::layout()`返回。
如果`parent` `nullptr`，则必须将该布局插入另一个布局，或用`QWidget::setLayout()`将其设置为小部件的布局。

### `bool QLayout::activate()`

**作用与语义：**

如果需要，重新做布局以适应`parentWidget()`。
通常不需要调用，因为它会自动在最合适的时间调用。如果布局被重新设计，它会返回为真。

### `[protected] void QLayout::addChildLayout(QLayout *childLayout)`

**作用与语义：**

该函数通过子类中的`addLayout()`或`insertLayout()`函数调用，以添加布局`childLayout`作为子布局。
只有在你实现了支持嵌套布局的自定义布局时，才需要直接调用它。

### `[protected] void QLayout::addChildWidget(QWidget *w)`

**作用与语义：**

该函数通过子类中的`addWidget()`函数调用，以添加`w`作为布局中的托管小部件。
如果`w`已经由布局管理，该函数会发出警告，并从布局中移除`w`。因此，必须在向布局数据结构添加`w`之前调用该函数。

### `[pure virtual] void QLayout::addItem(QLayoutItem *item)`

**作用与语义：**

在子职业中实现以添加`item`。添加方式因子职业而异。
该函数通常不会在应用代码中调用。要向布局添加小部件，使用`addWidget()`函数;添加子布局，使用相关`QLayout`子类提供的addLayout()函数。
注意：`item`的所有权转移到了布局上，删除它由布局负责。

### `void QLayout::addWidget(QWidget *w)`

**作用与语义：**

以特定布局的方式添加小部件`w`。该函数使用`addItem()`。

### `[protected] QRect QLayout::alignmentRect(const QRect &r) const`

**作用与语义：**

当该布局的几何体设置为`r`时，返回应覆盖的矩形，前提是该布局支持`setAlignment()`。
结果由`sizeHint()`和`expandingDirections()`推导出。它永远不会大于`r`。

### `[override virtual protected] void QLayout::childEvent(QChildEvent *e)`

**作用与语义：**

重实现自：`QObject::childEvent`（QChildEvent *event）。

### `[static] QSize QLayout::closestAcceptableSize(const QWidget *widget, const QSize &size)`

**作用与语义：**

返回一个满足`widget`所有大小约束的大小，包括`heightForWidth()`，并且尽可能接近`size`的大小。

### `QMargins QLayout::contentsMargins() const`

**作用与语义：**

返回布局周围使用的边距。
默认情况下，`QLayout`使用样式提供的数值。在大多数平台上，边界在所有方向上都是11像素。
注意：属性内容边距的获取函数。

### `QRect QLayout::contentsRect() const`

**作用与语义：**

返回布局的`geometry()`矩形，但考虑了内容页边余。

### `[override virtual] QSizePolicy::ControlTypes QLayout::controlTypes() const`

**作用与语义：**

重实现自：`QLayoutItem::controlTypes()` const.
返回布局项的控制类型。对于`QWidgetItem`，控制类型来自小部件的大小策略;对于`QLayoutItem`，控制类型是从布局内容中推导出来的。

### `[pure virtual] int QLayout::count() const`

**作用与语义：**

必须在子类中实现，以返回布局中的物品数量。

### `[override virtual] Qt::Orientations QLayout::expandingDirections() const`

**作用与语义：**

重装：`QLayoutItem::expandingDirections()` const.
返回该布局是否能利用超过`sizeHint()`的空间。值为`Qt::Vertical`或`Qt::Horizontal`表示它只想在一个维度上增长，而`Qt::Vertical` |`Qt::Horizontal`表示它想在两个维度上都增长。
默认实现返回`Qt::Horizontal` |`Qt::Vertical`。子类会根据子控件的大小策略重新实现，返回有意义的值。
返回该布局项目是否能利用超过`sizeHint()`的空间。值为`Qt::Vertical`或`Qt::Horizontal`表示它只想在一个维度上增长，而`Qt::Vertical` |`Qt::Horizontal`表示它想在两个维度上都增长。

### `[override virtual] QRect QLayout::geometry() const`

**作用与语义：**

重装：`QLayoutItem::geometry()` const.
返回该布局项目覆盖的矩形。

### `void QLayout::getContentsMargins(int *left, int *top, int *right, int *bottom) const`

**作用与语义：**

对于`left`、`top`、`right`和`bottom`中未被`nullptr`的每个，都存储指针所指位置所命名边距的大小。
默认情况下，`QLayout`使用样式提供的数值。在大多数平台上，边界为所有方向的11像素。

### `[virtual] int QLayout::indexOf(const QLayoutItem *layoutItem) const`

**作用与语义：**

在此布局中搜索布局项目`layoutItem`（不包括子布局）。
返回`layoutItem`的索引，若未找到`layoutItem`则返回-1。

### `[virtual] int QLayout::indexOf(const QWidget *widget) const`

**作用与语义：**

在此布局中搜索小部件`widget`（不包括子布局）。
返回`widget`的索引，若未找到`widget`则返回-1。
默认实现会对所有使用`itemAt()`的项目进行迭代。

### `[override virtual] void QLayout::invalidate()`

**作用与语义：**

重装：`QLayoutItem::invalidate()`。
使该布局项中缓存的信息失效。

### `[override virtual] bool QLayout::isEmpty() const`

**作用与语义：**

重装：`QLayoutItem::isEmpty()` const.
在子类中实现，返回该项是否为空，即是否包含任何控件。

### `bool QLayout::isEnabled() const`

**作用与语义：**

如果启用了布局，返回`true`;否则返回`false`。

### `[pure virtual] QLayoutItem *QLayout::itemAt(int index) const`

**作用与语义：**

必须在子类中实现以返回 `index` 的布局项。如果没有这样的项，函数必须返回 `nullptr`。项从零开始连续编号。如果某个项被删除，其他项将重新编号。
该函数可用于遍历布局。以下代码将为小部件布局结构中的每个布局项绘制一个矩形。

**官方示例：**

```cpp
 static void paintLayout(QPainter *painter, QLayoutItem *item)
 {
     QLayout *layout = item->layout();
     if (layout) {
         for (int i = 0; i < layout->count(); ++i)
             paintLayout(painter, layout->itemAt(i));
     }
     painter->drawRect(item->geometry());
 }

 void MyWidget::paintEvent(QPaintEvent *)
 {
     QPainter painter(this);
     if (layout())
         paintLayout(&painter, layout());
 }
```

### `[override virtual] QLayout *QLayout::layout()`

**作用与语义：**

重装：`QLayoutItem::layout()`。
如果该项是`QLayout`，则返回为`QLayout`;否则返回`nullptr`。该函数提供类型安全的铸造。

### `[override virtual] QSize QLayout::maximumSize() const`

**作用与语义：**

重装：`QLayoutItem::maximumSize()` const.
返回该布局的最大尺寸。这是布局在遵守规范的前提下的最大尺寸。
返回的值不包括`QWidget::setContentsMargins()`或`menuBar()`所需的空间。
默认实现允许无限调整尺寸。
在子类中实现以返回该项的最大大小。

### `QWidget *QLayout::menuBar() const`

**作用与语义：**

返回该布局设置的菜单栏，若未设置菜单栏则返回`nullptr`。

### `[override virtual] QSize QLayout::minimumSize() const`

**作用与语义：**

重装：`QLayoutItem::minimumSize()` const.
返回该布局的最小尺寸。这是布局在仍能遵守规范的前提下能有的最小尺寸。
返回的值不包括`QWidget::setContentsMargins()`或`menuBar()`所需的空间。
默认实现允许无限调整尺寸。
在子类中实现，以返回该项的最小大小。

### `QWidget *QLayout::parentWidget() const`

**作用与语义：**

返回该布局的父控件，或者如果该布局未安装在任何控件上，则返回`nullptr`。
如果布局是子布局，该函数返回父布局的父控件。

### `void QLayout::removeItem(QLayoutItem *item)`

**作用与语义：**

将布局中的项目`item`从布局中移除。删除该项目由调用者负责。
注意`item`可以是布局（因为`QLayout`继承了`QLayoutItem`）。

### `void QLayout::removeWidget(QWidget *widget)`

**作用与语义：**

将小部件`widget`从布局中移除。调用后，调用者负责为小部件提供合理的几何形状，或将小部件重新放入布局，必要时显式隐藏。
注：`widget`的所有权与加入时保持不变。

### `[virtual] QLayoutItem *QLayout::replaceWidget(QWidget *from, QWidget *to, Qt::FindChildOptions options = Qt::FindChildrenRecursively)`

**作用与语义：**

搜索控件 `from`，若找到则用控件 `to` 替换。成功时返回包含控件`from`的布局项目。否则返回 `nullptr`。如果`options`包含 `Qt::FindChildrenRecursively`（默认），则搜索子布局进行替换。`options` 中的其他标志被忽略。
请注意，退回的物品可能不属于该布局，而是属于子布局。
返回的布局项目不再属于布局，应被删除或插入到另一个布局中。控件`from`不再由布局管理，可能需要删除或隐藏。控件 `from` 的父节点保持不变。
这个功能适用于内置的 Qt 布局，但可能不适用于自定义布局。

### `bool QLayout::setAlignment(QWidget *w, Qt::Alignment alignment)`

**作用与语义：**

将控件 `w` 的对齐设置为 `alignment`，如果在该布局中找到 `w`（不包括子布局），则返回 true;否则返回 `false`。

### `bool QLayout::setAlignment(QLayout *l, Qt::Alignment alignment)`

**作用与语义：**

将布局`l`的对齐设置为`alignment`，如果在该布局中找到`l`（不包括子布局），则返回`true`;否则返回`false`。

### `void QLayout::setContentsMargins(const QMargins &margins)`

**作用与语义：**

该特性保留了布局周围的边界。
默认情况下，`QLayout`使用样式提供的数值。在大多数平台上，边界在所有方向上都是11像素。

**如何使用：** 调用 `setContentsMargins(...)` 修改 `contentsMargins`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QLayout::setContentsMargins(int left, int top, int right, int bottom)`

**作用与语义：**

该特性保留了布局周围的边界。
默认情况下，`QLayout`使用样式提供的数值。在大多数平台上，边界在所有方向上都是11像素。

**如何使用：** 调用 `setContentsMargins(...)` 修改 `contentsMargins`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QLayout::setEnabled(bool enable)`

**作用与语义：**

如果`enable`为真，则启用该布局，否则禁用。
启用的布局会动态调整变化;禁用的布局则视同不存在。
默认情况下，所有布局都是启用的。

### `[override virtual] void QLayout::setGeometry(const QRect &r)`

**作用与语义：**

重装：`QLayoutItem::setGeometry`（const QRect & r）。
在子类中实现，将该物品的几何体设置为`r`。

### `void QLayout::setMenuBar(QWidget *widget)`

**作用与语义：**

告诉几何管理器将菜单栏放在`parentWidget()`顶部，`QWidget::contentsMargins()`外`widget`。所有子控件都放在菜单栏底部下方。

### `[since 6.10] void QLayout::setSizeConstraints(QLayout::SizeConstraint horizontal, QLayout::SizeConstraint vertical)`

**作用与语义：**

设置了`horizontal`和`vertical`尺寸约束。

### `[pure virtual] QLayoutItem *QLayout::takeAt(int index)`

**作用与语义：**

必须在子类中实现，以从布局中移除`index`的布局项并返回该项。如果没有这样的项，函数必须什么都不做，返回0。项编号从0开始依次排列。如果一个项被移除，其他项将被重新编号。
以下代码片段展示了一种安全移除所有布局物品的方法：

**官方示例：**

```cpp
 QLayoutItem *child;
 while ((child = layout->takeAt(0)) != nullptr) {
     ...
     delete child->widget(); // delete the widget
     delete child;   // delete the layout item
 }
```

### `[since 6.1] void QLayout::unsetContentsMargins()`

**作用与语义：**

该特性保留了布局周围的边界。
默认情况下，`QLayout`使用样式提供的数值。在大多数平台上，边界在所有方向上都是11像素。

**如何使用：** 调用 `unsetContentsMargins()` 读取当前值；它不会修改应用状态。

### `void QLayout::update()`

**作用与语义：**

更新版面以`parentWidget()`。
通常你不需要打电话，因为它会自动在最合适的时间被叫。

### `QLayout::SizeConstraint horizontalSizeConstraint() const`

**作用与语义：**

该属性表示水平尺寸约束。
默认模式是`QLayout::SetDefaultConstraint`。

**如何使用：** 调用 `horizontalSizeConstraint()` 读取当前值；它不会修改应用状态。

### `void setHorizontalSizeConstraint(QLayout::SizeConstraint constraint)`

**作用与语义：**

该属性表示水平尺寸约束。
默认模式是`QLayout::SetDefaultConstraint`。

**如何使用：** 调用 `setHorizontalSizeConstraint(...)` 修改 `horizontalSizeConstraint`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSizeConstraint(QLayout::SizeConstraint constraint)`

**作用与语义：**

该属性保留了布局的缩放模式。设置对话框的大小约束。设置垂直或水平大小约束则覆盖此约束。
默认模式是`SetDefaultConstraint`。

**如何使用：** 调用 `setSizeConstraint(...)` 修改 `sizeConstraint`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `virtual void setSpacing(int)`

**作用与语义：**

该属性保留了布局中小部件之间的间距。
如果没有明确设置值，布局的间距会继承自父布局，或父控件的样式设置。
对于`QGridLayout`和`QFormLayout`，可以使用`setHorizontalSpacing()`和`setVerticalSpacing()`设置不同的水平和垂直间距。此时，spacing() 返回 -1。

**如何使用：** 调用 `setSpacing(...)` 修改 `spacing`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setVerticalSizeConstraint(QLayout::SizeConstraint constraint)`

**作用与语义：**

该属性表示垂直尺寸约束。
默认模式是`QLayout::SetDefaultConstraint`。

**如何使用：** 调用 `setVerticalSizeConstraint(...)` 修改 `verticalSizeConstraint`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QLayout::SizeConstraint sizeConstraint() const`

**作用与语义：**

该属性保留了布局的缩放模式。设置对话框的大小约束。设置垂直或水平大小约束则覆盖此约束。
默认模式是`SetDefaultConstraint`。

**如何使用：** 调用 `sizeConstraint()` 读取当前值；它不会修改应用状态。

### `virtual int spacing() const`

**作用与语义：**

该属性保留了布局中小部件之间的间距。
如果没有明确设置值，布局的间距会继承自父布局，或父控件的样式设置。
对于`QGridLayout`和`QFormLayout`，可以使用`setHorizontalSpacing()`和`setVerticalSpacing()`设置不同的水平和垂直间距。此时，spacing() 返回 -1。

**如何使用：** 调用 `spacing()` 读取当前值；它不会修改应用状态。

### `QLayout::SizeConstraint verticalSizeConstraint() const`

**作用与语义：**

该属性表示垂直尺寸约束。
默认模式是`QLayout::SetDefaultConstraint`。

**如何使用：** 调用 `verticalSizeConstraint()` 读取当前值；它不会修改应用状态。

## 6. 深入实践与常见坑

### 生命周期和资源边界

顶层布局可以在构造时绑定到 QWidget，也可以通过 `setLayout()` 安装；嵌套布局加入父布局后所有权交给父布局。布局析构不会自动销毁普通 QWidget，动态移除项目时要分别处理控件、子布局和 spacer。

### 状态和错误边界

布局的项目索引会随着 add、insert、remove 和 takeAt 改变；索引既包括控件，也包括子布局、固定空白和 stretch。修改项目或尺寸参数后 Qt 会使布局失效并重新计算。

### 线程边界

布局只应在 GUI 线程操作，因为它直接改变 QWidget 几何和可见界面。布局系统不负责业务线程同步，也不会把手动的跨线程控件访问变安全。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QLayout` 所属机制类型：布局管理机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
