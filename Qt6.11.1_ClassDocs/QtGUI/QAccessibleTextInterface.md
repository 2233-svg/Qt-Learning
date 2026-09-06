# QAccessibleTextInterface

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是一个抽象接口或框架基类，重点是理解它定义的协议，并通过具体子类、工厂或回调来使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QAccessibleTextInterface` 是 Qt GUI 中的抽象协议类型，通常通过具体子类、模型、插件或工厂来使用。

**内部模型：** 抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

**适用场景：** 当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。

**典型调用链：** 选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

**先记住的坑：** 不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

## 2. 依赖与对象关系

- 头文件：`#include <QAccessibleTextInterface>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。 使用时通常按这个过程组织：选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `virtual ~QAccessibleTextInterface()`
- `virtual void addSelection(int startOffset, int endOffset) = 0`
- `virtual QString attributes(int offset, int *startOffset, int *endOffset) const = 0`
- `virtual int characterCount() const = 0`
- `virtual QRect characterRect(int offset) const = 0`
- `virtual int cursorPosition() const = 0`
- `virtual int offsetAtPoint(const QPoint &point) const = 0`
- `virtual void removeSelection(int selectionIndex) = 0`
- `virtual void scrollToSubstring(int startIndex, int endIndex) = 0`
- `virtual void selection(int selectionIndex, int *startOffset, int *endOffset) const = 0`
- `virtual int selectionCount() const = 0`
- `virtual void setCursorPosition(int position) = 0`
- `virtual void setSelection(int selectionIndex, int startOffset, int endOffset) = 0`
- `virtual QString text(int startOffset, int endOffset) const = 0`
- `virtual QString textAfterOffset(int offset, QAccessible::TextBoundaryType boundaryType, int *startOffset, int *endOffset) const`
- `virtual QString textAtOffset(int offset, QAccessible::TextBoundaryType boundaryType, int *startOffset, int *endOffset) const`
- `virtual QString textBeforeOffset(int offset, QAccessible::TextBoundaryType boundaryType, int *startOffset, int *endOffset) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[virtual noexcept] QAccessibleTextInterface::~QAccessibleTextInterface()`

**作用与语义：**

摧毁了`QAccessibleTextInterface`。

### `[pure virtual] void QAccessibleTextInterface::addSelection(int startOffset, int endOffset)`

**作用与语义：**

从`startOffset`到`endOffset`选择文本。`startOffset`是第一个被选中的字符。`endOffset`是第一个不会被选中的字符。
当对象支持多个选择（例如在文字处理器中），这会添加一个新的选择，否则会替换之前的选择。
选角将`endOffset` `startOffset`字。

### `[pure virtual] QString QAccessibleTextInterface::attributes(int offset, int *startOffset, int *endOffset) const`

**作用与语义：**

返回位于位置`offset`的文本属性。此外，属性的范围以 `startOffset` 和 `endOffset` 返回。

### `[pure virtual] int QAccessibleTextInterface::characterCount() const`

**作用与语义：**

返回文本长度（包含空格的总大小）。

### `[pure virtual] QRect QAccessibleTextInterface::characterRect(int offset) const`

**作用与语义：**

返回角色在屏幕坐标中位置`offset`的位置和大小。

### `[pure virtual] int QAccessibleTextInterface::cursorPosition() const`

**作用与语义：**

返回当前光标位置。

### `[pure virtual] int QAccessibleTextInterface::offsetAtPoint(const QPoint &point) const`

**作用与语义：**

返回`point`位置字符的偏移量，映射屏幕坐标。

### `[pure virtual] void QAccessibleTextInterface::removeSelection(int selectionIndex)`

**作用与语义：**

用索引`selectionIndex`清除选择。

### `[pure virtual] void QAccessibleTextInterface::scrollToSubstring(int startIndex, int endIndex)`

**作用与语义：**

确保`startIndex`与`endIndex`之间的文字是可见的。

### `[pure virtual] void QAccessibleTextInterface::selection(int selectionIndex, int *startOffset, int *endOffset) const`

**作用与语义：**

返回一个选择。选择的大小以 `startOffset` 和 `endOffset` 返回。如果没有选择，`startOffset` 和 `endOffset` 都`nullptr`。
无障碍API支持多重选择。但大多数控件只支持一个选择，且`selectionIndex`等于0。

### `[pure virtual] int QAccessibleTextInterface::selectionCount() const`

**作用与语义：**

返回本文本中的选段数量。

### `[pure virtual] void QAccessibleTextInterface::setCursorPosition(int position)`

**作用与语义：**

将光标移到`position`。

### `[pure virtual] void QAccessibleTextInterface::setSelection(int selectionIndex, int startOffset, int endOffset)`

**作用与语义：**

选择`selectionIndex`设置为`startOffset`到`endOffset`的范围。

### `[pure virtual] QString QAccessibleTextInterface::text(int startOffset, int endOffset) const`

**作用与语义：**

返回文本从`startOffset`到`endOffset`。`startOffset`是第一个返回的字符。`endOffset`是第一个不会返回的字符。

### `[virtual] QString QAccessibleTextInterface::textAfterOffset(int offset, QAccessible::TextBoundaryType boundaryType, int *startOffset, int *endOffset) const`

**作用与语义：**

返回偏移`offset`之后的类型`boundaryType`文本项，并将`startOffset`和`endOffset`值设置为该项的起始和结束位置;如果没有空项，则返回空字符串。错误时将`startOffset`和`endOffset`值设为-1。
该默认实现用于小范围文本编辑。文字处理器或文本编辑器应提供其高效的实现。该功能不区分段落和行。
注意：该函数无法考虑光标位置。按照惯例，`offset`为-2意味着该函数应使用光标位置作为偏移。因此，在调用该函数之前，必须将偏移转换为光标位置。偏移量为-1用于文本长度，该函数的自定义实现必须返回结果，就像长度作为偏移传递一样。

### `[virtual] QString QAccessibleTextInterface::textAtOffset(int offset, QAccessible::TextBoundaryType boundaryType, int *startOffset, int *endOffset) const`

**作用与语义：**

返回偏移`offset`的类型为`boundaryType`的文本项，并将`startOffset`和`endOffset`值设为该项的起始和结束位置;如果没有空项，则返回空字符串。错误时将`startOffset`和`endOffset`值设为-1。
该默认实现用于小范围文本编辑。文字处理器或文本编辑器应提供其高效的实现。该功能不区分段落和行。
注意：该函数无法考虑光标位置。按照惯例，`offset`为-2意味着该函数应使用光标位置作为偏移。因此，在调用该函数之前，必须将偏移量为-2的光标位置。偏移量为-1用于文本长度，该函数的自定义实现必须返回结果，就像长度作为偏移传递一样。

### `[virtual] QString QAccessibleTextInterface::textBeforeOffset(int offset, QAccessible::TextBoundaryType boundaryType, int *startOffset, int *endOffset) const`

**作用与语义：**

返回类型为`boundaryType`且接近偏移`offset`的文本项，并将`startOffset`和`endOffset`值设置为该项的起始和结束位置;如果没有空项，返回空字符串。错误时将`startOffset`和`endOffset`值设为-1。
该默认实现用于小范围文本编辑。文字处理器或文本编辑器应提供其高效的实现。该功能不区分段落和行。
注意：该函数无法考虑光标位置。按照惯例，`offset`为-2意味着该函数应使用光标位置作为偏移。因此，必须先将偏移转换为光标位置，才能调用该函数。偏移量为-1用于文本长度，该函数的自定义实现必须返回结果，就像长度作为偏移传递一样。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QAccessibleTextInterface` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
