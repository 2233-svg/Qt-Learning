# QSyntaxHighlighter

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QSyntaxHighlighter` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QSyntaxHighlighter` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QSyntaxHighlighter>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

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

### 公有函数

- `QSyntaxHighlighter(QObject *parent)`
- `QSyntaxHighlighter(QTextDocument *parent)`
- `virtual ~QSyntaxHighlighter()`
- `QTextDocument * document() const`
- `void setDocument(QTextDocument *doc)`

### 公有槽函数

- `void rehighlight()`
- `void rehighlightBlock(const QTextBlock &block)`

### 保护函数

- `QTextBlock currentBlock() const`
- `int currentBlockState() const`
- `QTextBlockUserData * currentBlockUserData() const`
- `QTextCharFormat format(int position) const`
- `virtual void highlightBlock(const QString &text) = 0`
- `int previousBlockState() const`
- `void setCurrentBlockState(int newState)`
- `void setCurrentBlockUserData(QTextBlockUserData *data)`
- `void setFormat(int start, int count, const QTextCharFormat &format)`
- `void setFormat(int start, int count, const QColor &color)`
- `void setFormat(int start, int count, const QFont &font)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QSyntaxHighlighter::QSyntaxHighlighter(QObject *parent)`

**作用与语义：**

构建一个带有给定`parent`的QSyntaxHighlighter。
如果父节点是`QTextEdit`，则会在父文档上安装语法高亮。指定的`QTextEdit`也成为QSyntaxHighlighter的所有者。

### `[explicit] QSyntaxHighlighter::QSyntaxHighlighter(QTextDocument *parent)`

**作用与语义：**

构建一个QSyntaxHighlighter并将其安装在`parent`上。指定的`QTextDocument`也成为QSyntaxHighlighter的所有者。

### `[virtual noexcept] QSyntaxHighlighter::~QSyntaxHighlighter()`

**作用与语义：**

Destructor。卸载了文本文档中的语法高亮。

### `[protected] QTextBlock QSyntaxHighlighter::currentBlock() const`

**作用与语义：**

返回当前文本块。

### `[protected] int QSyntaxHighlighter::currentBlockState() const`

**作用与语义：**

返回当前文本块的状态。如果未设置值，返回值为-1。

### `[protected] QTextBlockUserData *QSyntaxHighlighter::currentBlockUserData() const`

**作用与语义：**

返回之前附加在当前文本块上的`QTextBlockUserData`对象。

### `QTextDocument *QSyntaxHighlighter::document() const`

**作用与语义：**

返回安装该语法高亮的`QTextDocument`。

### `[protected] QTextCharFormat QSyntaxHighlighter::format(int position) const`

**作用与语义：**

返回格式在语法高亮当前文本块内的 `position`。

### `[pure virtual protected] void QSyntaxHighlighter::highlightBlock(const QString &text)`

**作用与语义：**

高亮给定的文本块。当富文本引擎需要时调用此功能，即文本块已更改。
要提供自己的语法高亮，你需要子类 `QSyntaxHighlighter` 并重新实现 highlightBlock()。在重实现中，你应解析该块的 `text`，并根据需要多次调用 `setFormat()`，以应用所需的字体和颜色更改。例如：
详见详细说明，了解如何使用`setCurrentBlockState()`、`currentBlockState()`和`previousBlockState()`来处理跨多个文本块的句法结构。

**官方示例：**

```cpp
 void MyHighlighter::highlightBlock(const QString &text)
 {
     QTextCharFormat myClassFormat;
     myClassFormat.setFontWeight(QFont::Bold);
     myClassFormat.setForeground(Qt::darkMagenta);

     QRegularExpression expression("\\bMy[A-Za-z]+\\b");
     QRegularExpressionMatchIterator i = expression.globalMatch(text);
     while (i.hasNext()) {
         QRegularExpressionMatch match = i.next();
         setFormat(match.capturedStart(), match.capturedLength(), myClassFormat);
     }
 }
```

### `[protected] int QSyntaxHighlighter::previousBlockState() const`

**作用与语义：**

返回语法高亮器当前区块之前文本块的结束状态。如果之前没有设置过值，返回值为-1。

### `[slot] void QSyntaxHighlighter::rehighlight()`

**作用与语义：**

把高亮重新应用到整个文档上。

### `[slot] void QSyntaxHighlighter::rehighlightBlock(const QTextBlock &block)`

**作用与语义：**

重新应用高光给给出的`QTextBlock` `block`。

### `[protected] void QSyntaxHighlighter::setCurrentBlockState(int newState)`

**作用与语义：**

将当前文本块的状态设置为`newState`。

### `[protected] void QSyntaxHighlighter::setCurrentBlockUserData(QTextBlockUserData *data)`

**作用与语义：**

将给定`data`附加到当前文本块上。所有权转移给底层文本文档，即当相应的文本块被删除时，提供的`QTextBlockUserData`对象将被删除。
`QTextBlockUserData` 可以用来存储自定义设置。在语法高亮方面，它作为缓存存储特别有趣，方便你在解析段落文本时发现这些信息。
例如，在解析文本时，你可以跟踪遇到的括号字符（'{[（' 等），并将其相对位置和实际 `QChar` 存储在由 `QTextBlockUserData` 衍生的简单类中：
在相关编辑器的光标导航中，你可以询问当前`QTextBlock`（通过`QTextCursor::block()`函数检索）是否有用户数据对象，并将其投射到你的`BlockData`对象。然后你可以检查当前光标位置是否与之前记录的括号位置匹配，并根据括号类型（开或闭）找到同一层的下一个开或闭合括号。
这样你可以做视觉上的括号匹配，并从当前光标位置高亮到匹配的括号。这样你更容易发现代码中缺少的括号，并在编辑大量括号的代码时找到对应的开闭括号位置。

**官方示例：**

```cpp
 struct ParenthesisInfo
 {
     QChar character;
     int position;
 };

 struct BlockData : public QTextBlockUserData
 {
     QList<ParenthesisInfo> parentheses;
 };
```

### `void QSyntaxHighlighter::setDocument(QTextDocument *doc)`

**作用与语义：**

在给定的`QTextDocument` `doc`上安装语法高亮器。一个`QSyntaxHighlighter`一次只能与一个文档一起使用。

### `[protected] void QSyntaxHighlighter::setFormat(int start, int count, const QTextCharFormat &format)`

**作用与语义：**

该功能应用于语法高亮器的当前文本块（即传递给`highlightBlock()`函数的文本）。
指定的`format`从`start`位置应用到文本，持续约`count`个字符（如果`count`为0，则不做任何操作）。`format`中设置的格式属性在显示时与文档中直接存储的格式信息合并，例如之前在`QTextCursor`函数中设置的。注意文档本身不会被通过该函数设置的格式修改。

### `[protected] void QSyntaxHighlighter::setFormat(int start, int count, const QColor &color)`

**作用与语义：**

从`start`位置开始，将指定的`color`应用到当前文本块，长度为`count`个字符。
当前文本块的其他属性，例如字体和背景颜色，重置为默认值。

### `[protected] void QSyntaxHighlighter::setFormat(int start, int count, const QFont &font)`

**作用与语义：**

从`start`位置开始，将指定的`font`应用到当前文本块，长度为`count`个字符。
当前文本块的其他属性，例如字体和背景颜色，重置为默认值。

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

`QSyntaxHighlighter` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
