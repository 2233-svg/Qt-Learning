# QTextBlock

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QTextBlock` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QTextBlock>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

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

- `class iterator`
- `Iterator`

### 公有函数

- `QTextBlock(const QTextBlock &other)`
- `QTextBlock::iterator begin() const`
- `QTextBlockFormat blockFormat() const`
- `int blockFormatIndex() const`
- `int blockNumber() const`
- `QTextCharFormat charFormat() const`
- `int charFormatIndex() const`
- `void clearLayout()`
- `bool contains(int position) const`
- `const QTextDocument * document() const`
- `QTextBlock::iterator end() const`
- `int firstLineNumber() const`
- `bool isValid() const`
- `bool isVisible() const`
- `QTextLayout * layout() const`
- `int length() const`
- `int lineCount() const`
- `QTextBlock next() const`
- `int position() const`
- `QTextBlock previous() const`
- `int revision() const`
- `void setLineCount(int count)`
- `void setRevision(int rev)`
- `void setUserData(QTextBlockUserData *data)`
- `void setUserState(int state)`
- `void setVisible(bool visible)`
- `QString text() const`
- `Qt::LayoutDirection textDirection() const`
- `QList<QTextLayout::FormatRange> textFormats() const`
- `QTextList * textList() const`
- `QTextBlockUserData * userData() const`
- `int userState() const`
- `bool operator!=(const QTextBlock &other) const`
- `bool operator<(const QTextBlock &other) const`
- `QTextBlock & operator=(const QTextBlock &other)`
- `bool operator==(const QTextBlock &other) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QTextBlock::Iterator`

**作用与语义：**

Qt风格的`QTextBlock::iterator`同义词。

### `QTextBlock::QTextBlock(const QTextBlock &other)`

**作用与语义：**

将`other`文本块的属性复制到该文本块上。

### `QTextBlock::iterator QTextBlock::begin() const`

**作用与语义：**

返回一个指向文本块起始的文本块迭代器。

### `QTextBlockFormat QTextBlock::blockFormat() const`

**作用与语义：**

返回描述特定区块属性的`QTextBlockFormat`。

### `int QTextBlock::blockFormatIndex() const`

**作用与语义：**

返回文档内部块格式列表中的索引，针对文本块的格式。

### `int QTextBlock::blockNumber() const`

**作用与语义：**

返回该块的编号，若块无效则返回-1。

### `QTextCharFormat QTextBlock::charFormat() const`

**作用与语义：**

返回描述区块字符格式的`QTextCharFormat`。在插入文本到空块时，使用块的字符格式。

### `int QTextBlock::charFormatIndex() const`

**作用与语义：**

返回文档内部字符格式列表中文本块字符格式的索引。

### `void QTextBlock::clearLayout()`

**作用与语义：**

清除用于布局和显示区块内容的 `QTextLayout`。

### `bool QTextBlock::contains(int position) const`

**作用与语义：**

如果给定`position`位于文本块内，返回`true`;否则返回`false`。

### `const QTextDocument *QTextBlock::document() const`

**作用与语义：**

返回该文本块所属的文本文档，或者如果文本块不属于任何文档，则返回`nullptr`。

### `QTextBlock::iterator QTextBlock::end() const`

**作用与语义：**

返回一个指向文本块末尾的迭代器。

### `int QTextBlock::firstLineNumber() const`

**作用与语义：**

返回该块的首行号，若块无效则返回-1。除非布局支持，否则行号与块号相同。

### `bool QTextBlock::isValid() const`

**作用与语义：**

如果此文本块有效，则返回 `true`；否则返回 `false`。

### `bool QTextBlock::isVisible() const`

**作用与语义：**

如果块可见，返回`true`;否则返回`false`。

### `QTextLayout *QTextBlock::layout() const`

**作用与语义：**

返回用于布局和显示区块内容的`QTextLayout`。
注意，返回的`QTextLayout`对象只能修改自 `QAbstractTextDocumentLayout` 子类的 documentChanged 实现。外部施加的任何更改都会导致行为未定义。

### `int QTextBlock::length() const`

**作用与语义：**

返回方块的字符长度。
注意：返回的长度包括所有格式化字符，例如换行。

### `int QTextBlock::lineCount() const`

**作用与语义：**

返回行数。并非所有文档布局都支持此功能。

### `QTextBlock QTextBlock::next() const`

**作用与语义：**

返回文档中的文本块，回到该块之后;如果是最后一个块，则返回空文本块。
注意，下一个方块可能位于与该方块不同的帧或表格中。

### `int QTextBlock::position() const`

**作用与语义：**

返回文档中块第一个字符的索引。

### `QTextBlock QTextBlock::previous() const`

**作用与语义：**

返回文档中该块之前的文本块，如果是第一个块，则返回一个空文本块。
注意，前一个块可能位于与该块不同的帧或表格中。

### `int QTextBlock::revision() const`

**作用与语义：**

返回该模块的修订版本。

### `void QTextBlock::setLineCount(int count)`

**作用与语义：**

将行数设置为`count`。

### `void QTextBlock::setRevision(int rev)`

**作用与语义：**

将一个块的修订设置为`rev`。

### `void QTextBlock::setUserData(QTextBlockUserData *data)`

**作用与语义：**

将给定的`data`对象附加到文本块上。
`QTextBlockUserData` 可用于存储自定义设置。所有权会传递给底层文本文档，即如果相应的文本块被删除，提供的`QTextBlockUserData`对象也会被删除。用户数据对象不存储在撤销历史中，因此在撤销删除文本块后该对象将无法访问。
例如，如果你在集成开发环境（IDE）中编写编程编辑器，你可能希望允许用户在代码中可视化地设置断点，以便集成调试器使用。在编程编辑器中，一行文本通常对应一个`QTextBlock`。`QTextBlockUserData`界面允许开发者存储每个`QTextBlock`的数据，比如用户在源代码的哪些行中有断点集。当然，这些数据也可以存储在外部，但通过存储在`QTextDocument`中，用户删除相关行时断点会自动被删除。这其实就是在`QTextDocument`中存储自定义信息，而不使用自定义属性`QTextFormat`因为这会影响撤销/重做堆栈。

### `void QTextBlock::setUserState(int state)`

**作用与语义：**

将指定的`state`整数值存储在文本块中。例如，这在语法高亮器中可能有用，用于存储文本解析状态。

### `void QTextBlock::setVisible(bool visible)`

**作用与语义：**

将方块的可见度设置为`visible`。

### `QString QTextBlock::text() const`

**作用与语义：**

将块内容以纯文本返回。

### `Qt::LayoutDirection QTextBlock::textDirection() const`

**作用与语义：**

返回已解析的文本方向。
如果块没有明确设置方向，它会根据块内容解析方向。返回`Qt::LeftToRight`或`Qt::RightToLeft`。

### `QList<QTextLayout::FormatRange> QTextBlock::textFormats() const`

**作用与语义：**

返回块内的文本格式选项，作为连续`QTextCharFormat`范围的列表。在插入文本时使用该范围的字符格式。

### `QTextList *QTextBlock::textList() const`

**作用与语义：**

如果块代表列表项，则返回该项所属的列表;否则返回`nullptr`。

### `QTextBlockUserData *QTextBlock::userData() const`

**作用与语义：**

如果`QTextBlockUserData`对象被设置为`setUserData()`或`nullptr`，则返回指向一个指向的指针。

### `int QTextBlock::userState() const`

**作用与语义：**

返回之前设置的整数值，`setUserState()`或-1。

### `bool QTextBlock::operator!=(const QTextBlock &other) const`

**作用与语义：**

如果此文本块与 `other` 文本块不同，则返回 `true`。

### `bool QTextBlock::operator<(const QTextBlock &other) const`

**作用与语义：**

如果此文本块出现在文档中的 `other` 文本块之前，则返回 `true`。

### `QTextBlock &QTextBlock::operator=(const QTextBlock &other)`

**作用与语义：**

将`other`文本块分配给该文本块。

### `bool QTextBlock::operator==(const QTextBlock &other) const`

**作用与语义：**

如果此文本块与 `other` 文本块相同，则返回 `true`。

### `class iterator`

**作用与语义：**

QTextBlock::iterator 类提供了用于读取 QTextBlock 内容的迭代器。
一个块由一系列文本片段组成。该类提供了一种方法来迭代这些片段并读取其内容，但不提供修改块的内部结构或内容的方法。
可以通过以下方式构建并使用迭代器来访问文本块内的片段：

**官方示例：**

```cpp
     QTextBlock::iterator it;
     for (it = currentBlock.begin(); !(it.atEnd()); ++it) {
         QTextFragment currentFragment = it.fragment();
         if (currentFragment.isValid())
             processFragment(currentFragment);
     }
```

### `Iterator`

**作用与语义：**

Qt风格的`QTextBlock::iterator`同义词。

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

`QTextBlock` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
