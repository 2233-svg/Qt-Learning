# QItemDelegate

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QItemDelegate` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QItemDelegate` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QItemDelegate>`
- 继承自：QAbstractItemDelegate
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

### 属性

- `clipping : bool`

### 公有函数

- `QItemDelegate(QObject *parent = nullptr)`
- `virtual ~QItemDelegate()`
- `bool hasClipping() const`
- `QItemEditorFactory * itemEditorFactory() const`
- `void setClipping(bool clip)`
- `void setItemEditorFactory(QItemEditorFactory *factory)`

### 重实现的公有函数

- `virtual QWidget * createEditor(QWidget *parent, const QStyleOptionViewItem &option, const QModelIndex &index) const override`
- `virtual void paint(QPainter *painter, const QStyleOptionViewItem &option, const QModelIndex &index) const override`
- `virtual void setEditorData(QWidget *editor, const QModelIndex &index) const override`
- `virtual void setModelData(QWidget *editor, QAbstractItemModel *model, const QModelIndex &index) const override`
- `virtual QSize sizeHint(const QStyleOptionViewItem &option, const QModelIndex &index) const override`
- `virtual void updateEditorGeometry(QWidget *editor, const QStyleOptionViewItem &option, const QModelIndex &index) const override`

### 保护函数

- `void drawBackground(QPainter *painter, const QStyleOptionViewItem &option, const QModelIndex &index) const`
- `virtual void drawCheck(QPainter *painter, const QStyleOptionViewItem &option, const QRect &rect, Qt::CheckState state) const`
- `virtual void drawDecoration(QPainter *painter, const QStyleOptionViewItem &option, const QRect &rect, const QPixmap &pixmap) const`
- `virtual void drawDisplay(QPainter *painter, const QStyleOptionViewItem &option, const QRect &rect, const QString &text) const`
- `virtual void drawFocus(QPainter *painter, const QStyleOptionViewItem &option, const QRect &rect) const`

### 重实现的保护函数

- `virtual bool editorEvent(QEvent *event, QAbstractItemModel *model, const QStyleOptionViewItem &option, const QModelIndex &index) override`
- `virtual bool eventFilter(QObject *object, QEvent *event) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `clipping : bool`

**作用与语义：**

如果代表应该剪辑画画事件。
该属性会将绘画剪辑设置为物品大小。默认值为开启。它在图片大于物品大小等情况下非常有用。

**如何使用：** 调用 `clipping()` 读取当前值；它不会修改应用状态。

### `[explicit] QItemDelegate::QItemDelegate(QObject *parent = nullptr)`

**作用与语义：**

用给定的`parent`构造一个物品代理。

### `[virtual noexcept] QItemDelegate::~QItemDelegate()`

**作用与语义：**

摧毁物品授权者。

### `[override virtual] QWidget *QItemDelegate::createEditor(QWidget *parent, const QStyleOptionViewItem &option, const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractItemDelegate::createEditor`（QWidget *parent， const QStyleOptionViewItem &option， const QModelIndex &index） const.
返回用于编辑`index`指定编辑项目的控件。`parent`控件和样式`option`用于控制编辑器控件的显示方式。
返回用于编辑数据项的编辑器，并使用给定`index`。注意索引包含所用模型的信息。编辑器的父控件由`parent`指定，项目选项由`option`指定。
基础实现返回`nullptr`。如果你想要自定义编辑，就需要重新实现这个函数。
返回的编辑器小部件应有`Qt::StrongFocus`;否则，小部件接收的`QMouseEvent`会传播到视图。视图的背景会透出，除非编辑器自己绘制背景（例如用`setAutoFillBackground()`）。

### `[protected] void QItemDelegate::drawBackground(QPainter *painter, const QStyleOptionViewItem &option, const QModelIndex &index) const`

**作用与语义：**

使用给定的`painter`和样式`option`渲染给定`index`的物品背景。

### `[virtual protected] void QItemDelegate::drawCheck(QPainter *painter, const QStyleOptionViewItem &option, const QRect &rect, Qt::CheckState state) const`

**作用与语义：**

在`rect`指定的矩形内渲染检查指示器，使用给定的`painter`和样式`option`，使用给定的`state`。

### `[virtual protected] void QItemDelegate::drawDecoration(QPainter *painter, const QStyleOptionViewItem &option, const QRect &rect, const QPixmap &pixmap) const`

**作用与语义：**

在`rect`指定的矩形范围内渲染装饰`pixmap`，使用给定的`painter`和样式`option`。

### `[virtual protected] void QItemDelegate::drawDisplay(QPainter *painter, const QStyleOptionViewItem &option, const QRect &rect, const QString &text) const`

**作用与语义：**

使用给定的`painter`和样式`option`渲染物品视图`text` `rect`指定的矩形内。

### `[virtual protected] void QItemDelegate::drawFocus(QPainter *painter, const QStyleOptionViewItem &option, const QRect &rect) const`

**作用与语义：**

使用给定的`painter`和样式`option`渲染`rect`指定矩形内的区域，表示该区域具有焦点。

### `[override virtual protected] bool QItemDelegate::editorEvent(QEvent *event, QAbstractItemModel *model, const QStyleOptionViewItem &option, const QModelIndex &index)`

**作用与语义：**

Reimplements： `QAbstractItemDelegate::editorEvent`（QEvent *event， QAbstractItemModel *model， const QStyleOptionViewItem &option， const QModelIndex &index）.
当开始编辑项目时，调用触发编辑的`event`、`model`、物品的`index`以及用于渲染该物品的`option`。
鼠标事件会发送到 editorEvent()，即使它们没有开始编辑该项目。例如，如果你想在右键点击物品时打开上下文菜单，这会很有用。
基础实现返回`false`（表示尚未处理该事件）。

### `[override virtual protected] bool QItemDelegate::eventFilter(QObject *object, QEvent *event)`

**作用与语义：**

重装：`QObject::eventFilter`（QObject *已观看，QEvent *事件）。
详情见`QAbstractItemDelegate::handleEditorEvent()`。

### `QItemEditorFactory *QItemDelegate::itemEditorFactory() const`

**作用与语义：**

返回项目代理使用的编辑器工厂。如果没有编辑器工厂设置，函数将返回空。

### `[override virtual] void QItemDelegate::paint(QPainter *painter, const QStyleOptionViewItem &option, const QModelIndex &index) const`

**作用与语义：**

Reimplements： `QAbstractItemDelegate::paint`（QPainter *painter， const QStyleOptionViewItem &option， const QModelIndex &index） const.
使用`index`指定的项目的指定`painter`和样式`option`渲染代理。
在子类中重新实现该函数时，你应该更新该选项`rect`变量所占领的区域，利用该选项的`state`变量确定要显示的物品状态，并相应调整其绘制方式。
例如，选中的项目可能需要以不同方式显示，如下代码所示：
涂漆后，应确保油漆工恢复到调用该函数时的状态。例如，涂漆前调用`QPainter::save()`，涂漆后再调用`QPainter::restore()`会很有用。
如果你想提供自定义渲染，这个纯抽象函数必须重新实现。使用`painter`和样式`option`来渲染物品`index`指定的项目。
如果你重新实现这个，你也必须重新实现`sizeHint()`。

**官方示例：**

```cpp
 if (option.state & QStyle::State_Selected)
     painter->fillRect(option.rect, option.palette.highlight());
```

### `[override virtual] void QItemDelegate::setEditorData(QWidget *editor, const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractItemDelegate::setEditorData`（QWidget *编辑器，const QModelIndex & index）const.
设置数据由模型`index`指定的数据模型项中的`editor`显示和编辑。
默认实现将数据存储在`editor`小部件的用户属性中。
将给定`editor`的内容设置为该项目在指定`index`的数据。注意，索引包含所用模型的信息。
基础实现没有任何功能。如果你想要自定义编辑，就需要重新实现这个函数。

### `void QItemDelegate::setItemEditorFactory(QItemEditorFactory *factory)`

**作用与语义：**

将编辑器工厂设置为物品代理使用的`factory`。如果没有设置编辑器工厂，物品代理将使用默认编辑器工厂。

### `[override virtual] void QItemDelegate::setModelData(QWidget *editor, QAbstractItemModel *model, const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractItemDelegate::setModelData`（QWidget *editor， QAbstractItemModel *model， const QModelIndex &index） const.
从`editor`小部件获取数据，并将其存储在指定`model`中，即物品`index`。
默认实现从`editor`小部件的用户属性中获取数据模型中要存储的值。
将`model`中给定`index`项的数据映射为给定`editor`的内容。
基础实现没有任何功能。如果你想要自定义编辑，就需要重新实现这个函数。

### `[override virtual] QSize QItemDelegate::sizeHint(const QStyleOptionViewItem &option, const QModelIndex &index) const`

**作用与语义：**

Reimplements： `QAbstractItemDelegate::sizeHint`（const QStyleOptionViewItem &option， const QModelIndex &index） const.
返回代理显示`index`指定项项所需的大小，并考虑`option`提供的样式信息。
在重新实现该函数时，注意对于文本项，文本长度会`QItemDelegate`增加一个边距（即2 * `QStyle::PM_FocusFrameHMargin`）。
如果你想提供自定义渲染，必须重新实现这个纯抽象函数。选项由`option`指定，模型项由`index`定义。
如果你重新实现这个，你也必须重新实现`paint()`。

### `[override virtual] void QItemDelegate::updateEditorGeometry(QWidget *editor, const QStyleOptionViewItem &option, const QModelIndex &index) const`

**作用与语义：**

Reimplementation s： `QAbstractItemDelegate::updateEditorGeometry`（QWidget *editor， const QStyleOptionViewItem &option， const QModelIndex &index） const.
根据`index`给出的样式更新指定的物品`editor` `option`。
根据`option`中指定的矩形，更新该项的`editor`几何体，`index`。如果物品内部布局，编辑器将相应布局。注意索引包含所用模型的信息。
基础实现没有任何作用。如果你想要自定义编辑，必须重新实现这个函数。

### `bool hasClipping() const`

**作用与语义：**

如果代表应该剪辑画画事件。
该属性会将绘画剪辑设置为物品大小。默认值为开启。它在图片大于物品大小等情况下非常有用。

**如何使用：** 调用 `hasClipping()` 读取当前值；它不会修改应用状态。

### `void setClipping(bool clip)`

**作用与语义：**

如果代表应该剪辑画画事件。
该属性会将绘画剪辑设置为物品大小。默认值为开启。它在图片大于物品大小等情况下非常有用。

**如何使用：** 调用 `setClipping(...)` 修改 `clipping`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QItemDelegate` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
