# QAbstractItemDelegate

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QAbstractItemDelegate` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QAbstractItemDelegate` 是 Qt Widgets 中的抽象协议类型，通常通过具体子类、模型、插件或工厂来使用。

**内部模型：** 抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

**适用场景：** 当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。

**典型调用链：** 选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

**先记住的坑：** 不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

## 2. 依赖与对象关系

- 头文件：`#include <QAbstractItemDelegate>`
- 继承自：QObject
- 直接派生类：QItemDelegate、QStyledItemDelegate

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
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

- `enum EndEditHint { NoHint, EditNextItem, EditPreviousItem, SubmitModelCache, RevertModelCache }`

### 公有函数

- `QAbstractItemDelegate(QObject *parent = nullptr)`
- `virtual ~QAbstractItemDelegate()`
- `virtual QWidget * createEditor(QWidget *parent, const QStyleOptionViewItem &option, const QModelIndex &index) const`
- `virtual void destroyEditor(QWidget *editor, const QModelIndex &index) const`
- `virtual bool editorEvent(QEvent *event, QAbstractItemModel *model, const QStyleOptionViewItem &option, const QModelIndex &index)`
- `(since 6.10) bool handleEditorEvent(QObject *editor, QEvent *event)`
- `virtual bool helpEvent(QHelpEvent *event, QAbstractItemView *view, const QStyleOptionViewItem &option, const QModelIndex &index)`
- `virtual void paint(QPainter *painter, const QStyleOptionViewItem &option, const QModelIndex &index) const = 0`
- `virtual void setEditorData(QWidget *editor, const QModelIndex &index) const`
- `virtual void setModelData(QWidget *editor, QAbstractItemModel *model, const QModelIndex &index) const`
- `virtual QSize sizeHint(const QStyleOptionViewItem &option, const QModelIndex &index) const = 0`
- `virtual void updateEditorGeometry(QWidget *editor, const QStyleOptionViewItem &option, const QModelIndex &index) const`

### 信号

- `void closeEditor(QWidget *editor, QAbstractItemDelegate::EndEditHint hint = NoHint)`
- `void commitData(QWidget *editor)`
- `void sizeHintChanged(const QModelIndex &index)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QAbstractItemDelegate::EndEditHint`

**作用与语义：**

该枚举描述了代表可以向模型和视图组件提供的不同提示，使模型中的数据编辑体验更舒适。
- `QAbstractItemDelegate::NoHint`：`0`;没有推荐的操作。
这些提示使代表能够影响观点的行为：
- `QAbstractItemDelegate::EditNextItem`：`1`;视图应使用代理在视图中的下一个项目中打开编辑器。
- `QAbstractItemDelegate::EditPreviousItem`：`2`;视图应使用代理在视图中上一个项目上打开编辑器。
注意，自定义视图可能对“下一”和“上一个”的概念有不同的解释。
以下提示在使用缓存数据的模型时最有用，例如那些通过本地操作数据以提升性能或节省网络带宽的模型。
- `QAbstractItemDelegate::SubmitModelCache`：`3`;如果模型缓存数据，应将缓存数据写入底层数据存储。
- `QAbstractItemDelegate::RevertModelCache`：`4`;如果模型缓存数据，应丢弃缓存数据，并用底层数据存储中的数据替换。
虽然模型和视图应以适当方式响应这些提示，但自定义组件如果不相关，可能会忽略其中任何或全部。

### `[explicit] QAbstractItemDelegate::QAbstractItemDelegate(QObject *parent = nullptr)`

**作用与语义：**

创建一个新的抽象项代理，并使用给定的`parent`。

### `[virtual noexcept] QAbstractItemDelegate::~QAbstractItemDelegate()`

**作用与语义：**

销毁抽象项委托。

### `[signal] void QAbstractItemDelegate::closeEditor(QWidget *editor, QAbstractItemDelegate::EndEditHint hint = NoHint)`

**作用与语义：**

当用户完成使用指定`editor`编辑项目时，该信号会发出。
`hint`为代理提供了一种方式，可以影响编辑完成后模型和视图的行为。它向这些组件指示下一步应执行的操作，以为用户提供舒适的编辑体验。例如，如果指定了`EditNextItem`，视图应使用代理在模型中的下一项开启编辑器。

### `[signal] void QAbstractItemDelegate::commitData(QWidget *editor)`

**作用与语义：**

当`editor`组件完成数据编辑并希望将其写回模型时，必须发出该信号。

### `[virtual] QWidget *QAbstractItemDelegate::createEditor(QWidget *parent, const QStyleOptionViewItem &option, const QModelIndex &index) const`

**作用与语义：**

返回用于编辑数据项的编辑器，并带有给定`index`。注意索引包含所用模型的信息。编辑器的父控件由`parent`指定，项目选项由`option`指定。
基础实现返回`nullptr`。如果你想要自定义编辑，就需要重新实现这个函数。
返回的编辑器小部件应有`Qt::StrongFocus`;否则，控件接收的`QMouseEvent`会传播到视图。视图的背景会透出，除非编辑器自己绘制背景（例如，用`setAutoFillBackground()`）。

### `[virtual] void QAbstractItemDelegate::destroyEditor(QWidget *editor, const QModelIndex &index) const`

**作用与语义：**

当 `editor` 不再用于编辑具有给定 `index` 的数据项时，应销毁该编辑器。默认行为是对编辑器调用 deleteLater。例如，可以通过重新实现此函数来避免此删除。

### `[virtual] bool QAbstractItemDelegate::editorEvent(QEvent *event, QAbstractItemModel *model, const QStyleOptionViewItem &option, const QModelIndex &index)`

**作用与语义：**

当项目编辑开始时，调用触发编辑的`event`、`model`、物品的`index`以及用于渲染该物品的`option`。
鼠标事件会发送到 editorEvent()，即使它们没有开始编辑该项目。例如，如果你想在右键点击物品时打开上下文菜单，这会很有用。
基础实现返回`false`（表示尚未处理该事件）。

### `[since 6.10] bool QAbstractItemDelegate::handleEditorEvent(QObject *editor, QEvent *event)`

**作用与语义：**

实现代表当前活动的 `editor` 的事件的标准处理。从 `QAbstractItemModel` 子类中 `eventFilter()` 的重写中调用此函数，并返回其结果。为避免重复事件处理，在调用此函数后不要调用 `eventFilter()` 的父类实现。
如果给定的 `editor` 是有效的 `QWidget` 并且给定的 `event` 已被处理，则返回 `true`；否则返回 `false`。默认情况下处理以下按键事件：
- Tab
- Backtab
- Enter
- Return
- Esc
如果 `editor` 的类型是 `QTextEdit` 或 `QPlainTextEdit`，则不处理 Tab、Backtab、Enter 和 Return 键。
在 Tab、Backtab、Enter 和 Return 键按下事件的情况下，`editor` 的数据会提交到模型中并关闭编辑器。如果 `event` 是 Tab 键按下，则视图将在视图中的下一个项目上打开编辑器。同样，如果 `event` 是 Backtab 键按下，视图将在视图中的上一个项目上打开编辑器。
如果事件是 Esc 键按下事件，则 `editor` 会关闭而不提交其数据。

### `[virtual] bool QAbstractItemDelegate::helpEvent(QHelpEvent *event, QAbstractItemView *view, const QStyleOptionViewItem &option, const QModelIndex &index)`

**作用与语义：**

每当发生帮助事件时，会调用该函数，并调用对应事件发生项的 `event` `view` `option` 和`index`。
如果代理能够处理事件，返回`true`;否则返回`false`。返回值为真表示使用索引获得的数据具有所需的角色。
对于成功处理的`QEvent::ToolTip`和`QEvent::WhatsThis`事件，相关弹窗可能会根据用户的系统配置显示。

### `[pure virtual] void QAbstractItemDelegate::paint(QPainter *painter, const QStyleOptionViewItem &option, const QModelIndex &index) const`

**作用与语义：**

如果你想提供自定义渲染，必须重新实现这个纯抽象函数。使用`painter`和样式`option`来渲染物品`index`指定的物品。
如果你重新实现这个，你也必须重新实现`sizeHint()`。

### `[virtual] void QAbstractItemDelegate::setEditorData(QWidget *editor, const QModelIndex &index) const`

**作用与语义：**

将给定`editor`的内容设置为该项目在指定`index`的数据。注意索引包含所用模型的信息。
基础实现没有任何功能。如果你想要自定义编辑，就需要重新实现这个函数。

### `[virtual] void QAbstractItemDelegate::setModelData(QWidget *editor, QAbstractItemModel *model, const QModelIndex &index) const`

**作用与语义：**

将`model`中给定`index`项的数据设置为给定`editor`的内容。
基础实现没有任何功能。如果你想要自定义编辑，就需要重新实现这个函数。

### `[pure virtual] QSize QAbstractItemDelegate::sizeHint(const QStyleOptionViewItem &option, const QModelIndex &index) const`

**作用与语义：**

如果你想提供自定义渲染，必须重新实现这个纯抽象函数。选项由`option`指定，模型项由`index`指定。
如果你重新实现这个，你也必须重新实现`paint()`。

### `[signal] void QAbstractItemDelegate::sizeHintChanged(const QModelIndex &index)`

**作用与语义：**

当`index` `sizeHint()`变化时必须发出该信号。
视图会自动连接到该信号，并根据需要重新布局项目。

### `[virtual] void QAbstractItemDelegate::updateEditorGeometry(QWidget *editor, const QStyleOptionViewItem &option, const QModelIndex &index) const`

**作用与语义：**

根据`option`中指定的矩形，更新该项的`editor`几何体，并附带给定的`index`。如果该项内部布局，编辑器将相应地布局。注意索引包含所用模型的信息。
基础实现没有任何作用。如果你想要自定义编辑，必须重新实现这个函数。

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

`QAbstractItemDelegate` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
