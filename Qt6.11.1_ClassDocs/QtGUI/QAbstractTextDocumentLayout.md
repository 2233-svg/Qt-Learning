# QAbstractTextDocumentLayout

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QAbstractTextDocumentLayout` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QAbstractTextDocumentLayout` 是 Qt GUI 中的抽象协议类型，通常通过具体子类、模型、插件或工厂来使用。

**内部模型：** 抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

**适用场景：** 当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。

**典型调用链：** 选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

**先记住的坑：** 不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

## 2. 依赖与对象关系

- 头文件：`#include <QAbstractTextDocumentLayout>`
- 继承自：QObject
- 直接派生类：QPlainTextDocumentLayout

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。 使用时通常按这个过程组织：选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `struct PaintContext`
- `struct Selection`

### 公有函数

- `QAbstractTextDocumentLayout(QTextDocument *document)`
- `QString anchorAt(const QPointF &position) const`
- `virtual QRectF blockBoundingRect(const QTextBlock &block) const = 0`
- `QTextBlock blockWithMarkerAt(const QPointF &pos) const`
- `QTextDocument * document() const`
- `virtual QSizeF documentSize() const = 0`
- `virtual void draw(QPainter *painter, const QAbstractTextDocumentLayout::PaintContext &context) = 0`
- `QTextFormat formatAt(const QPointF &pos) const`
- `virtual QRectF frameBoundingRect(QTextFrame *frame) const = 0`
- `QTextObjectInterface * handlerForObject(int objectType) const`
- `virtual int hitTest(const QPointF &point, Qt::HitTestAccuracy accuracy) const = 0`
- `QString imageAt(const QPointF &pos) const`
- `virtual int pageCount() const = 0`
- `QPaintDevice * paintDevice() const`
- `void registerHandler(int objectType, QObject *component)`
- `void setPaintDevice(QPaintDevice *device)`
- `void unregisterHandler(int objectType, QObject *component = nullptr)`

### 信号

- `void documentSizeChanged(const QSizeF &newSize)`
- `void pageCountChanged(int newPages)`
- `void update(const QRectF &rect = QRectF(0., 0., 1000000000., 1000000000.))`
- `void updateBlock(const QTextBlock &block)`

### 保护函数

- `virtual void documentChanged(int position, int charsRemoved, int charsAdded) = 0`
- `virtual void drawInlineObject(QPainter *painter, const QRectF &rect, QTextInlineObject object, int posInDocument, const QTextFormat &format)`
- `QTextCharFormat format(int position)`
- `virtual void positionInlineObject(QTextInlineObject item, int posInDocument, const QTextFormat &format)`
- `virtual void resizeInlineObject(QTextInlineObject item, int posInDocument, const QTextFormat &format)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QAbstractTextDocumentLayout::QAbstractTextDocumentLayout(QTextDocument *document)`

**作用与语义：**

为给定`document`创建新的文本文档布局。

### `QString QAbstractTextDocumentLayout::anchorAt(const QPointF &position) const`

**作用与语义：**

返回锚点的引用给定`position`，如果该点不存在锚点，则返回空字符串。

### `[pure virtual] QRectF QAbstractTextDocumentLayout::blockBoundingRect(const QTextBlock &block) const`

**作用与语义：**

返回`block`的边界矩形。

### `QTextBlock QAbstractTextDocumentLayout::blockWithMarkerAt(const QPointF &pos) const`

**作用与语义：**

返回在给定位置`pos`找到`marker`的块（可能是列表项）。

### `QTextDocument *QAbstractTextDocumentLayout::document() const`

**作用与语义：**

返回该布局所操作的文本文档。

### `[pure virtual protected] void QAbstractTextDocumentLayout::documentChanged(int position, int charsRemoved, int charsAdded)`

**作用与语义：**

每当文档内容发生变化时，都会调用该函数。当文本插入、删除或两者结合时，会发生变更。变更由`position`、`charsRemoved`和`charsAdded`指定，分别对应变更的起始字符位置、从文档中移除的字符数以及新增字符数。
例如，当在空文档中插入文本“Hello”时，`charsRemoved`为0，`charsAdded`为5（字符串长度）。
替换文本是删除和插入的结合。例如，如果文本“Hello”被替换为“Hi”，`charsRemoved`是5，`charsAdded`是2。
对于`QAbstractTextDocumentLayout`子类，这是主要功能，负责布局和定位文档内容的大部分工作。
例如，在只排列文本块的子类中，该函数的实现需要完成以下操作：
- 利用提供的参数确定更改`QTextBlock`列表。
- 每个`QTextBlock`对象对应的`QTextLayout`对象都需要处理。你可以使用`QTextBlock::layout()`函数访问`QTextBlock`的布局。处理时应考虑文档的页面大小。
- 如果总页数发生变化，应发出`pageCountChanged()`信号。
- 如果总尺寸发生变化，应发射`documentSizeChanged()`信号。
- 应发射`update()`信号，以安排重新涂装中需要重新涂装的区域。

### `[pure virtual] QSizeF QAbstractTextDocumentLayout::documentSize() const`

**作用与语义：**

返回文档布局的总大小。
这些信息可以被显示控件用来正确更新滚动条。

### `[signal] void QAbstractTextDocumentLayout::documentSizeChanged(const QSizeF &newSize)`

**作用与语义：**

当文档布局大小变为`newSize`时，会发出该信号。
`QAbstractTextDocumentLayout`子类在文档整体布局大小变化时应会发出该信号。该信号对显示文本文档的小部件非常有用，因为它能正确更新滚动条。

### `[pure virtual] void QAbstractTextDocumentLayout::draw(QPainter *painter, const QAbstractTextDocumentLayout::PaintContext &context)`

**作用与语义：**

用给定的`painter`用给定的`context`绘制布局。

### `[virtual protected] void QAbstractTextDocumentLayout::drawInlineObject(QPainter *painter, const QRectF &rect, QTextInlineObject object, int posInDocument, const QTextFormat &format)`

**作用与语义：**

调用该函数绘制内联对象 `object`，其矩形内的`painter`由 `rect` 使用指定的文本`format`。
`posInDocument`指定了该对象在文档中的位置。
默认实现调用对象处理程序上的 drawObject()。该函数仅在 Qt 内调用。子类可以重新实现该函数以自定义内联对象的绘制。

### `[protected] QTextCharFormat QAbstractTextDocumentLayout::format(int position)`

**作用与语义：**

返回给定`position`适用的字符格式。

### `QTextFormat QAbstractTextDocumentLayout::formatAt(const QPointF &pos) const`

**作用与语义：**

返回给定位置的文本格式`pos`。

### `[pure virtual] QRectF QAbstractTextDocumentLayout::frameBoundingRect(QTextFrame *frame) const`

**作用与语义：**

返回`frame`的边界矩形。

### `QTextObjectInterface *QAbstractTextDocumentLayout::handlerForObject(int objectType) const`

**作用与语义：**

返回给定`objectType`对象的处理程序。

### `[pure virtual] int QAbstractTextDocumentLayout::hitTest(const QPointF &point, Qt::HitTestAccuracy accuracy) const`

**作用与语义：**

返回指定`point`的光标位置，并返回指定`accuracy`。如果未找到有效的光标位置，返回-1。

### `QString QAbstractTextDocumentLayout::imageAt(const QPointF &pos) const`

**作用与语义：**

返回给定位置图像的源头，`pos`，如果该点无图像则返回空字符串。

### `[pure virtual] int QAbstractTextDocumentLayout::pageCount() const`

**作用与语义：**

返回布局中包含的页数。

### `[signal] void QAbstractTextDocumentLayout::pageCountChanged(int newPages)`

**作用与语义：**

当排版页数发生变化时，会发出该信号;`newPages` 是更新后的页数。
`QAbstractTextDocumentLayout`子类在布局页数变化时应发出该信号。页数的变化由布局或文档内容本身的变化引起。

### `QPaintDevice *QAbstractTextDocumentLayout::paintDevice() const`

**作用与语义：**

返回用于渲染文档布局的绘图设备。

### `[virtual protected] void QAbstractTextDocumentLayout::positionInlineObject(QTextInlineObject item, int posInDocument, const QTextFormat &format)`

**作用与语义：**

用给定的文本`format`布局内联对象`item`。
`posInDocument` 指定了对象在文档中的位置。
默认实现不做任何操作。该函数仅在 Qt 中调用。子类可以重新实现该函数以自定义内联对象的位置。

### `void QAbstractTextDocumentLayout::registerHandler(int objectType, QObject *component)`

**作用与语义：**

将给定`component`注册为给定`objectType`项的处理程序。
注意：registerHandler() 必须对每个对象类型调用一次。这意味着同一对象类型的多个替换字符只有一个处理器。
文本文档布局不对`component`拥有所有权。

### `[virtual protected] void QAbstractTextDocumentLayout::resizeInlineObject(QTextInlineObject item, int posInDocument, const QTextFormat &format)`

**作用与语义：**

设置内联对象的大小`item`对应文本 `format`。
`posInDocument` 指定了该对象在文档中的位置。
默认实现会将`item`调整为对象处理程序的 intrinsicSize() 函数返回的大小。该函数仅在 Qt 中被调用。子类可以重新实现该函数以自定义内联对象的大小调整。

### `void QAbstractTextDocumentLayout::setPaintDevice(QPaintDevice *device)`

**作用与语义：**

将用于渲染文档布局的绘图设备设置为给定的`device`。

### `void QAbstractTextDocumentLayout::unregisterHandler(int objectType, QObject *component = nullptr)`

**作用与语义：**

取消将给定`component`作为该`objectType`项的处理程序，或者如果未指定`component`，则取消注册任何处理程序。

### `[signal] void QAbstractTextDocumentLayout::update(const QRectF &rect = QRectF(0., 0., 1000000000., 1000000000.))`

**作用与语义：**

当矩形`rect`更新时，该信号会发出。
`QAbstractTextDocumentLayout`子类在内容布局发生变化以便重新绘制时应发出该信号。

### `[signal] void QAbstractTextDocumentLayout::updateBlock(const QTextBlock &block)`

**作用与语义：**

当指定`block`更新时，该信号会发出。
`QAbstractTextDocumentLayout`子类在`block`布局发生变化以重新涂装时应发出该信号。

### `struct PaintContext`

**作用与语义：**

QAbstractTextDocumentLayout::PaintContext 类是一个便利类，用于定义在绘制文档布局时使用的参数。
绘制上下文在使用 `QAbstractTextDocumentLayout::draw()` 函数渲染 QTextDocument 的自定义布局时使用。它由光标位置、默认文本颜色、`clip` 矩形和一组 `selections` 指定。

### `struct Selection`

**作用与语义：**

QAbstractTextDocumentLayout::Selection 类是一个便利类，用于定义选择的参数。
选择可用于指定在使用 `QAbstractTextDocumentLayout::draw()` 函数绘制 QTextDocument 的自定义布局时应高亮显示的文档部分。它是通过 `cursor` 和 `format` 指定的。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QAbstractTextDocumentLayout` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
