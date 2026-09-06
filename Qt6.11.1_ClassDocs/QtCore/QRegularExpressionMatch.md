# QRegularExpressionMatch

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 一次正则匹配结果，负责判断是否匹配成功并读取捕获文本和位置。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QRegularExpressionMatch`：一次正则匹配结果，负责判断是否匹配成功并读取捕获文本和位置。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QRegularExpressionMatch>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QRegularExpressionMatch()`
- `QRegularExpressionMatch(const QRegularExpressionMatch &match)`
- `(since 6.1) QRegularExpressionMatch(QRegularExpressionMatch &&match)`
- `~QRegularExpressionMatch()`
- `QString captured(QAnyStringView name) const`
- `QString captured(int nth = 0) const`
- `qsizetype capturedEnd(QAnyStringView name) const`
- `qsizetype capturedEnd(int nth = 0) const`
- `qsizetype capturedLength(QAnyStringView name) const`
- `qsizetype capturedLength(int nth = 0) const`
- `qsizetype capturedStart(QAnyStringView name) const`
- `qsizetype capturedStart(int nth = 0) const`
- `QStringList capturedTexts() const`
- `QStringView capturedView(QAnyStringView name) const`
- `QStringView capturedView(int nth = 0) const`
- `(since 6.3) bool hasCaptured(QAnyStringView name) const`
- `(since 6.3) bool hasCaptured(int nth) const`
- `bool hasMatch() const`
- `bool hasPartialMatch() const`
- `bool isValid() const`
- `int lastCapturedIndex() const`
- `QRegularExpression::MatchOptions matchOptions() const`
- `QRegularExpression::MatchType matchType() const`
- `QRegularExpression regularExpression() const`
- `void swap(QRegularExpressionMatch &other)`
- `QRegularExpressionMatch & operator=(QRegularExpressionMatch &&match)`
- `QRegularExpressionMatch & operator=(const QRegularExpressionMatch &match)`

### 相关非成员函数

- `QDebug operator<<(QDebug debug, const QRegularExpressionMatch &match)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QRegularExpressionMatch::QRegularExpressionMatch()`

**作用与语义：**

构造一个有效且空的 QRegularExpressionMatch 对象。正则表达式设置为默认构造的;匹配类型为 `QRegularExpression::NoMatch`，匹配选项为 `QRegularExpression::NoMatchOption`。
对象会通过`hasMatch()`和 `hasPartialMatch()` 成员函数报告无匹配。

### `QRegularExpressionMatch::QRegularExpressionMatch(const QRegularExpressionMatch &match)`

**作用与语义：**

通过复制给定`match`的结果来构建比赛结果。

### `[constexpr noexcept, since 6.1] QRegularExpressionMatch::QRegularExpressionMatch(QRegularExpressionMatch &&match)`

**作用与语义：**

通过将结果从给定`match`中移动来构造比赛结果。
注意，移出 QRegularExpressionMatch 只能被销毁或分配到 。调用除解构器或赋值操作符外的其他函数效果尚未定义。

### `[noexcept] QRegularExpressionMatch::~QRegularExpressionMatch()`

**作用与语义：**

毁掉比赛结果。

### `QString QRegularExpressionMatch::captured(QAnyStringView name) const`

**作用与语义：**

返回被捕获群捕获的子串，名为`name`。
如果命名的捕获群`name`没有捕获字符串，或者没有名为`name`的捕获群，则返回空`QString`。
注意：在6.8之前的Qt版本中，该功能采用`QString`或`QStringView`，而非`QAnyStringView`。

### `QString QRegularExpressionMatch::captured(int nth = 0) const`

**作用与语义：**

返回`nth`捕获组捕获的子串。
如果`nth`捕获群没有捕获字符串，或者不存在这样的捕获群，则返回空`QString`。
注意：隐式捕获组编号0捕捉与整个模式匹配的子串。

### `qsizetype QRegularExpressionMatch::capturedEnd(QAnyStringView name) const`

**作用与语义：**

返回主语串内的偏移量，紧接着被捕获组捕获的子串`name`的终点位置。如果捕获组 `name` 未捕获或不存在字符串，返回 -1。
注意：在6.8之前的Qt版本中，该功能采用`QString`或`QStringView`，而非使用`QAnyStringView`。

### `qsizetype QRegularExpressionMatch::capturedEnd(int nth = 0) const`

**作用与语义：**

返回主语字符串内的偏移量，紧接着被`nth`捕获组捕获的子串的结束位置。如果`nth`捕获组未捕获或不存在字符串，返回 -1。

### `qsizetype QRegularExpressionMatch::capturedLength(QAnyStringView name) const`

**作用与语义：**

返回被捕获群捕获的子串长度，称为`name`。
注意：如果名为 `name` 的捕获组没有捕获字符串或不存在，则该函数返回 0。
注意：在6.8之前的Qt版本中，该功能采用`QString`或`QStringView`，而非使用`QAnyStringView`。

### `qsizetype QRegularExpressionMatch::capturedLength(int nth = 0) const`

**作用与语义：**

返回`nth`捕获群捕获的子串长度。
注意：如果`nth`捕获组没有捕获字符串或不存在，该函数返回0。

### `qsizetype QRegularExpressionMatch::capturedStart(QAnyStringView name) const`

**作用与语义：**

返回主语字符串内对应捕获组 `name` 捕获子串起始位置的偏移量。如果捕获组 `name` 未捕获或不存在字符串，返回 -1。
注意：在6.8之前的Qt版本中，这个功能需要`QString`或`QStringView`，而不是`QAnyStringView`。

### `qsizetype QRegularExpressionMatch::capturedStart(int nth = 0) const`

**作用与语义：**

返回主语字符串内对应`nth`捕获组捕获子串起始位置的偏移量。如果`nth`捕获组未捕获或不存在字符串，返回 -1。

### `QStringList QRegularExpressionMatch::capturedTexts() const`

**作用与语义：**

返回捕获群捕获的所有字符串列表，按组本身出现在模式字符串中的顺序排列。列表包含隐式捕获组编号0，捕获与整个模式匹配的子串。

### `QStringView QRegularExpressionMatch::capturedView(QAnyStringView name) const`

**作用与语义：**

返回被捕获组名为`name`的字符串视图。
如果命名的捕获群`name`没有捕获字符串，或者没有名为`name`的捕获群，则返回空`QStringView`。
注意：在6.8之前的Qt版本中，该功能采用`QString`或`QStringView`，而非使用`QAnyStringView`。

### `QStringView QRegularExpressionMatch::capturedView(int nth = 0) const`

**作用与语义：**

返回`nth`捕获组捕获子串的视图。
如果`nth`捕获群没有捕获字符串，或者不存在这样的捕获群，则返回空`QStringView`。
注意：隐式捕获组编号0捕捉与整个模式匹配的子串。

### `[since 6.3] bool QRegularExpressionMatch::hasCaptured(QAnyStringView name) const`

**作用与语义：**

如果捕获群名为`name`捕获了主语串中的某物，则返回true;否则返回false（或不存在名为`name`的捕获群）。
注意：即使正则表达式匹配，正则表达式中某些捕获群也可能未捕获任何内容。例如，如果在模式中使用条件算子，就可能发生这种情况：
类似地，捕获群可以捕获长度为0的子串;该函数将返回该捕获群的 `true`。
注意：在6.8之前的Qt版本中，该功能采用`QString`或`QStringView`，而非`QAnyStringView`。

**官方示例：**

```cpp
 QRegularExpression re("([a-z]+)|([A-Z]+)");
 QRegularExpressionMatch m = re.match("UPPERCASE");
 if (m.hasMatch()) {
     qDebug() << m.hasCaptured(0); // true
     qDebug() << m.hasCaptured(1); // false
     qDebug() << m.hasCaptured(2); // true
 }
```

### `[since 6.3] bool QRegularExpressionMatch::hasCaptured(int nth) const`

**作用与语义：**

如果`nth`捕获组捕获了主语字符串中的某部分，返回真;否则返回假（或不存在此类捕获组）。
注意：隐式捕获组编号0捕捉与整个模式匹配的子串。
注意：即使正则表达式匹配，正则表达式中某些捕获群也可能未捕获任何内容。例如，如果在模式中使用条件算子，就可能发生这种情况：
类似地，捕获群可以捕获长度为0的子串;该函数将返回该捕获群的 `true`。

**官方示例：**

```cpp
 QRegularExpression re("([a-z]+)|([A-Z]+)");
 QRegularExpressionMatch m = re.match("UPPERCASE");
 if (m.hasMatch()) {
     qDebug() << m.hasCaptured(0); // true
     qDebug() << m.hasCaptured(1); // false
     qDebug() << m.hasCaptured(2); // true
 }
```

### `bool QRegularExpressionMatch::hasMatch() const`

**作用与语义：**

如果正规表达式与主语字符串匹配，则返回`true`;否则返回 false。

### `bool QRegularExpressionMatch::hasPartialMatch() const`

**作用与语义：**

如果正则表达式与主语字符串部分匹配，则返回`true`;否则返回为假。
注意：只有明确使用部分匹配类型之一的匹配才能产生部分匹配。不过，如果匹配完全成功，该函数返回假，而`hasMatch()`返回真。

### `bool QRegularExpressionMatch::isValid() const`

**作用与语义：**

如果匹配对象是通过对有效`QRegularExpression`对象调用的`QRegularExpression::match()`函数获得的，返回`true`;如果`QRegularExpression`无效，返回`false`。

### `int QRegularExpressionMatch::lastCapturedIndex() const`

**作用与语义：**

返回最后捕获某物的捕获组索引，包括隐式捕获群0。这可以用来提取所有捕获的子串：
注意，一些索引小于lastCapturedIndex()的捕获组可能不匹配，因此什么都没捕获。
如果正则表达式不匹配，该函数返回 -1。

**官方示例：**

```cpp
 QRegularExpressionMatch match = re.match(string);
 for (int i = 0; i <= match.lastCapturedIndex(); ++i) {
     QString captured = match.captured(i);
     // ...
 }
```

### `QRegularExpression::MatchOptions QRegularExpressionMatch::matchOptions() const`

**作用与语义：**

返回用于获得该`QRegularExpressionMatch`对象的匹配选项，即传递给`QRegularExpression::match()`或`QRegularExpression::globalMatch()`的匹配选项。

### `QRegularExpression::MatchType QRegularExpressionMatch::matchType() const`

**作用与语义：**

返回用于获得该`QRegularExpressionMatch`对象的匹配类型，即传递给`QRegularExpression::match()`或`QRegularExpression::globalMatch()`的匹配类型。

### `QRegularExpression QRegularExpressionMatch::regularExpression() const`

**作用与语义：**

返回 match() 函数返回该对象的 `QRegularExpression` 对象。

### `[noexcept] void QRegularExpressionMatch::swap(QRegularExpressionMatch &other)`

**作用与语义：**

将该匹配结果与`other`交换。此操作非常快速且从未失败。

### `[noexcept] QRegularExpressionMatch &QRegularExpressionMatch::operator=(QRegularExpressionMatch &&match)`

**作用与语义：**

Move-将匹配结果`match`分配给该对象，并返回对结果的引用。
注意，移出的 `QRegularExpressionMatch` 只能被销毁或分配到 。调用除解构器或赋值算符外的其他函数效果尚无定义。

### `QRegularExpressionMatch &QRegularExpressionMatch::operator=(const QRegularExpressionMatch &match)`

**作用与语义：**

将匹配结果`match`分配给该对象，并返回对该副本的引用。

### `QDebug operator<<(QDebug debug, const QRegularExpressionMatch &match)`

**作用与语义：**

将匹配对象`match`写入调试对象的`debug`以便调试。

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

`QRegularExpressionMatch` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
