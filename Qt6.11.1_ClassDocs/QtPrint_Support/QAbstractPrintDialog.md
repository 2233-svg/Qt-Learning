# QAbstractPrintDialog

> Qt 6.11.1 · Qt Print Support

## 1. 先建立直觉

**一句话定位：** `QAbstractPrintDialog` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Print Support 提供打印机、打印预览和打印作业相关接口。

### 这是什么

`QAbstractPrintDialog` 是 Qt Print Support 中的抽象协议类型，通常通过具体子类、模型、插件或工厂来使用。

**内部模型：** 抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

**适用场景：** 当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。

**典型调用链：** 选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

**先记住的坑：** 不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

## 2. 依赖与对象关系

- 头文件：`#include <QAbstractPrintDialog>`
- 继承自：QDialog
- 直接派生类：QPrintDialog

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS PrintSupport)
target_link_libraries(mytarget PRIVATE Qt6::PrintSupport)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

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

- `enum PrintDialogOption { PrintToFile, PrintSelection, PrintPageRange, PrintShowPageSize, PrintCollateCopies, PrintCurrentPage }`
- `flags PrintDialogOptions`
- `enum PrintRange { AllPages, Selection, PageRange, CurrentPage }`

### 公有函数

- `QAbstractPrintDialog(QPrinter *printer, QWidget *parent = nullptr)`
- `int fromPage() const`
- `int maxPage() const`
- `int minPage() const`
- `QAbstractPrintDialog::PrintRange printRange() const`
- `QPrinter * printer() const`
- `void setFromTo(int from, int to)`
- `void setMinMax(int min, int max)`
- `void setOptionTabs(const QList<QWidget *> &tabs)`
- `void setPrintRange(QAbstractPrintDialog::PrintRange range)`
- `int toPage() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QAbstractPrintDialog::PrintDialogOptionflags QAbstractPrintDialog::PrintDialogOptions`

**作用与语义：**

用于指定打印对话框中哪些部分应可见。
- `QAbstractPrintDialog::PrintToFile`：`0x0001`;已启用打印到文件的选项。
- `QAbstractPrintDialog::PrintSelection`：`0x0002`;已启用打印选择选项。
- `QAbstractPrintDialog::PrintPageRange`：`0x0004`;页面范围选择选项已启用。
- `QAbstractPrintDialog::PrintShowPageSize`：在`0x0008`;仅在启用页边距时显示页面页边距。
- `QAbstractPrintDialog::PrintCollateCopies`：`0x0010`;已启用“整理复制”选项
- `QAbstractPrintDialog::PrintCurrentPage`：`0x0040`;启用了打印当前页面选项
PrintDialogOptions 类型是 QFlags 的 typedef<PrintDialogOption>。它存储 PrintDialogOption 值的 OR 组合。

### `enum QAbstractPrintDialog::PrintRange`

**作用与语义：**

用于指定打印范围选择选项。
- `QAbstractPrintDialog::AllPages`：`0`;所有页面应印刷。
- `QAbstractPrintDialog::Selection`：`1`;仅应打印选出部分。
- `QAbstractPrintDialog::PageRange`：`2`;应打印指定的页数范围。
- `QAbstractPrintDialog::CurrentPage`：`3`;仅应打印当前可见的页面。

### `[explicit] QAbstractPrintDialog::QAbstractPrintDialog(QPrinter *printer, QWidget *parent = nullptr)`

**作用与语义：**

构建一个以 `parent` 为父控件的 `printer` 的抽象打印对话。

### `int QAbstractPrintDialog::fromPage() const`

**作用与语义：**

返回第一页要打印的页面。默认情况下，该值设为0。

### `int QAbstractPrintDialog::maxPage() const`

**作用与语义：**

返回页区内的最大页面。从Qt 4.4起，该函数默认返回INT_MAX。之前版本默认返回1。

### `int QAbstractPrintDialog::minPage() const`

**作用与语义：**

返回页区间内的最小页面。默认情况下，该值设置为1。

### `QAbstractPrintDialog::PrintRange QAbstractPrintDialog::printRange() const`

**作用与语义：**

退回打印系列。

### `QPrinter *QAbstractPrintDialog::printer() const`

**作用与语义：**

返回该打印机对话框所操作的打印机。

### `void QAbstractPrintDialog::setFromTo(int from, int to)`

**作用与语义：**

在打印对话框中设置范围为从`from`到`to`。

### `void QAbstractPrintDialog::setMinMax(int min, int max)`

**作用与语义：**

将该对话框中的页面范围设置为从`min`到`max`。这也启用了`PrintPageRange`选项。

### `void QAbstractPrintDialog::setOptionTabs(const QList<QWidget *> &tabs)`

**作用与语义：**

如果支持，请将打印对话框中显示的控件列表设置为 `tabs`。
目前这个选项只支持X11。
设置选项标签页会把它们的所有权转移到打印对话框。

### `void QAbstractPrintDialog::setPrintRange(QAbstractPrintDialog::PrintRange range)`

**作用与语义：**

将打印范围选项设置为`range`。

### `int QAbstractPrintDialog::toPage() const`

**作用与语义：**

返回最后一页要打印的页面。默认情况下，这个值设置为0。

### `enum PrintDialogOption { PrintToFile, PrintSelection, PrintPageRange, PrintShowPageSize, PrintCollateCopies, PrintCurrentPage }`

**作用与语义：**

用于指定打印对话框中哪些部分应可见。
- `QAbstractPrintDialog::PrintToFile`：`0x0001`;已启用打印到文件的选项。
- `QAbstractPrintDialog::PrintSelection`：`0x0002`;已启用打印选择选项。
- `QAbstractPrintDialog::PrintPageRange`：`0x0004`;页面范围选择选项已启用。
- `QAbstractPrintDialog::PrintShowPageSize`：在`0x0008`;仅在启用页边距时显示页面页边距。
- `QAbstractPrintDialog::PrintCollateCopies`：`0x0010`;已启用“整理复制”选项
- `QAbstractPrintDialog::PrintCurrentPage`：`0x0040`;启用了打印当前页面选项
PrintDialogOptions 类型是 QFlags 的 typedef<PrintDialogOption>。它存储 PrintDialogOption 值的 OR 组合。

### `flags PrintDialogOptions`

**作用与语义：**

用于指定打印对话框中哪些部分应可见。
- `QAbstractPrintDialog::PrintToFile`：`0x0001`;已启用打印到文件的选项。
- `QAbstractPrintDialog::PrintSelection`：`0x0002`;已启用打印选择选项。
- `QAbstractPrintDialog::PrintPageRange`：`0x0004`;页面范围选择选项已启用。
- `QAbstractPrintDialog::PrintShowPageSize`：在`0x0008`;仅在启用页边距时显示页面页边距。
- `QAbstractPrintDialog::PrintCollateCopies`：`0x0010`;已启用“整理复制”选项
- `QAbstractPrintDialog::PrintCurrentPage`：`0x0040`;启用了打印当前页面选项
PrintDialogOptions 类型是 QFlags 的 typedef<PrintDialogOption>。它存储 PrintDialogOption 值的 OR 组合。

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

`QAbstractPrintDialog` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
