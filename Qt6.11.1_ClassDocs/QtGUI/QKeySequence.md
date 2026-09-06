# QKeySequence

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QKeySequence` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QKeySequence>`
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

- `enum SequenceFormat { NativeText, PortableText }`
- `enum SequenceMatch { NoMatch, PartialMatch, ExactMatch }`
- `enum StandardKey { AddTab, Back, Backspace, Bold, Close, …, Cancel }`

### 公有函数

- `QKeySequence()`
- `QKeySequence(QKeySequence::StandardKey key)`
- `QKeySequence(const QString &key, QKeySequence::SequenceFormat format = NativeText)`
- `QKeySequence(QKeyCombination k1, QKeyCombination k2 = QKeyCombination::fromCombined(0), QKeyCombination k3 = QKeyCombination::fromCombined(0), QKeyCombination k4 = QKeyCombination::fromCombined(0))`
- `QKeySequence(int k1, int k2 = 0, int k3 = 0, int k4 = 0)`
- `QKeySequence(const QKeySequence &keysequence)`
- `~QKeySequence()`
- `int count() const`
- `bool isEmpty() const`
- `QKeySequence::SequenceMatch matches(const QKeySequence &seq) const`
- `void swap(QKeySequence &other)`
- `QString toString(QKeySequence::SequenceFormat format = PortableText) const`
- `operator QVariant() const`
- `bool operator!=(const QKeySequence &other) const`
- `bool operator<(const QKeySequence &other) const`
- `bool operator<=(const QKeySequence &other) const`
- `QKeySequence & operator=(QKeySequence &&other)`
- `QKeySequence & operator=(const QKeySequence &other)`
- `bool operator==(const QKeySequence &other) const`
- `bool operator>(const QKeySequence &other) const`
- `bool operator>=(const QKeySequence &other) const`
- `QKeyCombination operator[](uint index) const`

### 静态公有成员

- `QKeySequence fromString(const QString &str, QKeySequence::SequenceFormat format = PortableText)`
- `QList<QKeySequence> keyBindings(QKeySequence::StandardKey key)`
- `QList<QKeySequence> listFromString(const QString &str, QKeySequence::SequenceFormat format = PortableText)`
- `QString listToString(const QList<QKeySequence> &list, QKeySequence::SequenceFormat format = PortableText)`
- `QKeySequence mnemonic(const QString &text)`

### 相关非成员函数

- `size_t qHash(const QKeySequence &key, size_t seed = 0)`
- `void qt_set_sequence_auto_mnemonic(bool b)`
- `QDataStream & operator<<(QDataStream &stream, const QKeySequence &sequence)`
- `QDataStream & operator>>(QDataStream &stream, QKeySequence &sequence)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QKeySequence::StandardKey`

**作用与语义：**

这个枚举代表标准按键绑定。它们可以用来为`QAction`分配与平台相关的快捷键。
请注意，按键绑定是依赖于平台的。当前绑定的快捷键可以用`keyBindings()`查询。
- `QKeySequence::AddTab`：`19`;添加新标签页。
- `QKeySequence::Back`：`13`;返回导航。
- `QKeySequence::Backspace`：`69`;删除之前的角色。
- `QKeySequence::Bold`：`27`;加粗字体。
- `QKeySequence::Close`：`4`;关闭文档/标签页。
- `QKeySequence::Copy`：`9`;收到。
- `QKeySequence::Cut`：`8`;停。
- `QKeySequence::Delete`：`7`;删除。
- `QKeySequence::DeleteEndOfLine`：`60`;删除行尾。
- `QKeySequence::DeleteEndOfWord`：`59`;删除光标末尾的单词。
- `QKeySequence::DeleteStartOfWord`：`58`;删除单词开头直到光标。
- `QKeySequence::DeleteCompleteLine`：`68`;删除整行。
- `QKeySequence::Find`：`22`;在文档中查找。
- `QKeySequence::FindNext`：`23`;查找下一个结果。
- `QKeySequence::FindPrevious`：`24`;查找之前的结果。
- `QKeySequence::Forward`：`14`;向前导航。
- `QKeySequence::HelpContents`：`1`;打开帮助内容。
- `QKeySequence::InsertLineSeparator`：`62`;插入新行。
- `QKeySequence::InsertParagraphSeparator`：`61`;插入新段落。
- `QKeySequence::Italic`：`28`;斜体文本。
- `QKeySequence::MoveToEndOfBlock`：`41`;将光标移动到方块末尾。该快捷键仅在苹果平台上使用。
- `QKeySequence::MoveToEndOfDocument`：`43`;将光标移动到文档末尾。
- `QKeySequence::MoveToEndOfLine`：`39`;将光标移动到行尾。
- `QKeySequence::MoveToNextChar`：`30`;将光标移动到下一个字符。
- `QKeySequence::MoveToNextLine`：`34`;将光标移至下一行。
- `QKeySequence::MoveToNextPage`：`36`;将光标移至下一页。
- `QKeySequence::MoveToNextWord`：`32`;将光标移至下一个单词。
- `QKeySequence::MoveToPreviousChar`：`31`;将光标移动到上一个角色。
- `QKeySequence::MoveToPreviousLine`：`35`;将光标移至上一行。
- `QKeySequence::MoveToPreviousPage`：`37`;将光标移至上一页。
- `QKeySequence::MoveToPreviousWord`：`33`;将光标移至上一个单词。
- `QKeySequence::MoveToStartOfBlock`：`40`;将光标移动到方块起始。该快捷键仅在苹果平台上使用。
- `QKeySequence::MoveToStartOfDocument`：`42`;将光标移动到文档起始。
- `QKeySequence::MoveToStartOfLine`：`38`;将光标移至行首。
- `QKeySequence::New`：`6`;创建新文档。
- `QKeySequence::NextChild`：`20`;导航到下一个标签页或子窗口。
- `QKeySequence::Open`：`3`;打开文档。
- `QKeySequence::Paste`：`10`;粘贴。
- `QKeySequence::Preferences`：`64`;打开偏好设置对话框。
- `QKeySequence::PreviousChild`：`21`;导航到上一个标签页或子窗口。
- `QKeySequence::Print`：`18`;印刷文档。
- `QKeySequence::Quit`：`65`;退出应用。
- `QKeySequence::Redo`：`12`;重来。
- `QKeySequence::Refresh`：`15`;刷新或重新加载当前文档。
- `QKeySequence::Replace`：`25`;查找并替换。
- `QKeySequence::SaveAs`：`63`;在提示用户输入文件名后保存文档。
- `QKeySequence::Save`：`5`;保存文档。
- `QKeySequence::SelectAll`：`26`;选择所有文本。
- `QKeySequence::Deselect`：`67`;取消选择文本。自5.1版本起
- `QKeySequence::SelectEndOfBlock`：`55`;将选择范围扩展到文本块的末尾。该快捷键仅在苹果平台上使用。
- `QKeySequence::SelectEndOfDocument`：`57`;将选择范围扩展到文档末尾。
- `QKeySequence::SelectEndOfLine`：`53`;将选择范围扩展到行尾。
- `QKeySequence::SelectNextChar`：`44`;将选择范围扩展到下一个角色。
- `QKeySequence::SelectNextLine`：`48`;将选择范围扩展到下一行。
- `QKeySequence::SelectNextPage`：`50`;将选择范围扩展到下一页。
- `QKeySequence::SelectNextWord`：`46`;将选择范围扩展到下一个单词。
- `QKeySequence::SelectPreviousChar`：`45`;将选择范围扩展到之前的角色。
- `QKeySequence::SelectPreviousLine`：`49`;将选择范围扩展到上一行。
- `QKeySequence::SelectPreviousPage`：`51`;将选择范围扩展到上一页。
- `QKeySequence::SelectPreviousWord`：`47`;将选择范围扩展到前一个词。
- `QKeySequence::SelectStartOfBlock`：`54`;将选择范围扩展到文本块的开头。该快捷键仅在苹果平台上使用。
- `QKeySequence::SelectStartOfDocument`：`56`;将选择范围扩展到文档起始。
- `QKeySequence::SelectStartOfLine`：`52`;将选择范围扩展到行首。
- `QKeySequence::Underline`：`29`;下划线文字。
- `QKeySequence::Undo`：`11`;撤销。
- `QKeySequence::UnknownKey`：`0`;未绑定钥匙。
- `QKeySequence::WhatsThis`：`2`;启动“这是什么”。
- `QKeySequence::ZoomIn`：`16`;放大。
- `QKeySequence::ZoomOut`：`17`;拉远。
- `QKeySequence::FullScreen`：`66`;切换窗口状态为全屏。
- `QKeySequence::Cancel`：`70`;取消当前操作。

### `QKeySequence::QKeySequence()`

**作用与语义：**

构造一个空密钥序列。

### `QKeySequence::QKeySequence(QKeySequence::StandardKey key)`

**作用与语义：**

为给定`key`构建一个QKeySequence对象。结果取决于当前运行的平台。
最终生成的对象将基于`key`按键绑定列表中的第一个元素。

### `QKeySequence::QKeySequence(const QString &key, QKeySequence::SequenceFormat format = NativeText)`

**作用与语义：**

基于`format`，从`key`字符串创建密钥序列。
例如，“Ctrl O” 会得到 CTRL 'O'。字符串“Ctrl”、“Shift”、“Alt”和“Meta”都能识别，以及在“`QShortcut`”上下文中（使用 `QObject::tr()`）中翻译后的对应词。
最多可通过逗号分隔四个键码，例如“Alt X，Ctrl S，Q”。
该构造函数通常与`tr()`结合使用，以便在平译中替换快捷键：
请注意“File|打开”译者评论。这绝非必要，但它为人工翻译者提供了一些背景信息。

**官方示例：**

```cpp
 QMenu *file = new QMenu(this);
 file->addAction(tr("&Open..."), QKeySequence(tr("Ctrl+O", "File|Open")),
                 this, &MainWindow::open);
```

### `QKeySequence::QKeySequence(QKeyCombination k1, QKeyCombination k2 = QKeyCombination::fromCombined(0), QKeyCombination k3 = QKeyCombination::fromCombined(0), QKeyCombination k4 = QKeyCombination::fromCombined(0))`

**作用与语义：**

构建一个最多4个键的键序列，`k1`、`k2`、`k3`和`k4`。

### `QKeySequence::QKeySequence(int k1, int k2 = 0, int k3 = 0, int k4 = 0)`

**作用与语义：**

构建一个最多4个键的键序列，`k1`、`k2`、`k3`和`k4`。
关键代码以`Qt::Key`形式列出，并可与修饰符（见 `Qt::KeyboardModifier`）如`Qt::ShiftModifier`、`Qt::ControlModifier`、`Qt::AltModifier`或`Qt::MetaModifier`组合。

### `QKeySequence::QKeySequence(const QKeySequence &keysequence)`

**作用与语义：**

复制构造器。复制`keysequence`。

### `[noexcept] QKeySequence::~QKeySequence()`

**作用与语义：**

会破坏关键序列。

### `int QKeySequence::count() const`

**作用与语义：**

返回键序列中的键数。最大数值为4个。

### `[static] QKeySequence QKeySequence::fromString(const QString &str, QKeySequence::SequenceFormat format = PortableText)`

**作用与语义：**

根据`format`返回字符串`str`的`QKeySequence`。

### `bool QKeySequence::isEmpty() const`

**作用与语义：**

如果密钥序列为空，则返回`true`;否则返回 false。

### `[static] QList<QKeySequence> QKeySequence::keyBindings(QKeySequence::StandardKey key)`

**作用与语义：**

返回给定`key`的快捷键绑定列表。调用该函数的结果会根据目标平台而异。列表的第一个元素表示该平台的主要快捷方式。如果结果包含多个结果，这些可以视为同一平台上该`key`的替代快捷方式。

### `[static] QList<QKeySequence> QKeySequence::listFromString(const QString &str, QKeySequence::SequenceFormat format = PortableText)`

**作用与语义：**

返回字符串`str`中的`QKeySequence`列表，基于`format`。

### `[static] QString QKeySequence::listToString(const QList<QKeySequence> &list, QKeySequence::SequenceFormat format = PortableText)`

**作用与语义：**

返回基于`format`的`list`字符串表示。

### `QKeySequence::SequenceMatch QKeySequence::matches(const QKeySequence &seq) const`

**作用与语义：**

与 `seq` 匹配序列。成功时返回 `ExactMatch`，若匹配不完全`seq`返回`PartialMatch`，序列无共同点则返回`NoMatch`。若 `seq` 较短，返回 `NoMatch`。

### `[static] QKeySequence QKeySequence::mnemonic(const QString &text)`

**作用与语义：**

返回`text`中助记法的快捷键序列，若未找到助记符则返回空键序列。
例如，mnemonic（“E&xit”）返回`Qt::ALT+Qt::Key_X`，助记词（“&Quit”）返回`ALT+Key_Q`，mnemonic（“Quit”）返回空`QKeySequence`。

### `[noexcept] void QKeySequence::swap(QKeySequence &other)`

**作用与语义：**

将该密钥序列与`other`交换。该操作非常快且从未失败。

### `QString QKeySequence::toString(QKeySequence::SequenceFormat format = PortableText) const`

**作用与语义：**

返回基于`format`的密钥序列的字符串表示。
例如，`Qt::CTRL` `Qt::Key_O` 的值为“Ctrl O”。如果按键序列包含多个按键代码，每个按键在返回的字符串中用逗号分隔，如“Alt X， Ctrl Y， Z”。字符串如“Ctrl”、“Shift”等在“`QShortcut`”上下文中用`QObject::tr()`进行翻译。
如果密钥序列没有密钥，则返回一个空字符串。
在苹果平台上，返回的字符串类似于菜单栏中显示的序列，如果`format` `QKeySequence::NativeText`;否则，字符串使用“便携”格式，适合写入文件。

### `QKeySequence::operator QVariant() const`

**作用与语义：**

返回密钥序列作为`QVariant`。

### `bool QKeySequence::operator!=(const QKeySequence &other) const`

**作用与语义：**

如果该密钥序列与`other`密钥序列不等于，返回`true`;否则返回`false`。

### `bool QKeySequence::operator<(const QKeySequence &other) const`

**作用与语义：**

提供了该密钥序列与`other`密钥序列的任意比较。唯一保证`false`的是，如果两个密钥序列相等且（ks1 < ks2） == ！（ ks2 < ks1） 如果密钥序列不相等。
该函数在某些情况下非常有用，例如你想在`QMap`中使用`QKeySequence`对象作为键。

### `bool QKeySequence::operator<=(const QKeySequence &other) const`

**作用与语义：**

如果该密钥序列小于或等于`other`密钥序列，返回`true`;否则返回`false`。

### `[noexcept] QKeySequence &QKeySequence::operator=(QKeySequence &&other)`

**作用与语义：**

Move-assign `other`到该`QKeySequence`实例。

### `QKeySequence &QKeySequence::operator=(const QKeySequence &other)`

**作用与语义：**

赋值算符。将`other`键序列分配给该对象。

### `bool QKeySequence::operator==(const QKeySequence &other) const`

**作用与语义：**

如果该密钥序列等于`other`密钥序列，返回`true`;否则返回`false`。

### `bool QKeySequence::operator>(const QKeySequence &other) const`

**作用与语义：**

如果该密钥序列大于`other`密钥序列，返回`true`;否则返回`false`。

### `bool QKeySequence::operator>=(const QKeySequence &other) const`

**作用与语义：**

如果该密钥序列大于或等于`other`密钥序列，返回`true`;否则返回`false`。

### `QKeyCombination QKeySequence::operator[](uint index) const`

**作用与语义：**

返回键序列中位置`index`的元素的引用。这只能用于读取元素。

### `[noexcept] size_t qHash(const QKeySequence &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `void qt_set_sequence_auto_mnemonic(bool b)`

**作用与语义：**

规定菜单项、标签等的助记词是否应被使用。在Windows和X11上，该功能默认开启;macOS上关闭此功能。当此功能关闭（即`b`为假时），`QKeySequence::mnemonic()`总是返回空字符串。
注意：该函数未在 Qt 的任何头文件中声明。要在应用中使用，请在调用前声明该函数原型。

### `QDataStream &operator<<(QDataStream &stream, const QKeySequence &sequence)`

**作用与语义：**

把密钥写入`sequence` `stream`。

### `QDataStream &operator>>(QDataStream &stream, QKeySequence &sequence)`

**作用与语义：**

从`stream`读取密钥序列到密钥`sequence`。

### `enum SequenceFormat { NativeText, PortableText }`

**作用与语义：**

- `QKeySequence::NativeText`：`0`;按键序列作为平台特定的字符串。这意味着它会以翻译形式显示，在苹果平台上它会类似于菜单栏中的按键序列。当你想向用户展示字符串时，这个枚举最好使用。
- `QKeySequence::PortableText`：`1`;密钥序列以“便携”格式呈现，适合读写文件。在许多情况下，它看起来与Windows和X11的原生文本相似。

### `enum SequenceMatch { NoMatch, PartialMatch, ExactMatch }`

**作用与语义：**

- `QKeySequence::NoMatch`：`0`;密钥序列不同;甚至不部分匹配。
- `QKeySequence::PartialMatch`：`1`;密钥序列部分匹配，但不相同。
- `QKeySequence::ExactMatch`：`2`;密钥序列相同。

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

`QKeySequence` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
