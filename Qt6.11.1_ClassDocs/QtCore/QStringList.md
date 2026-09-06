# QStringList

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“String列表”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QStringList` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QStringList>`
- 继承自：QList
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

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QStringList(const QList<QString> &other)`
- `QStringList(const QString &str)`
- `QStringList(QList<QString> &&other)`
- `bool contains(const QString &str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `bool contains(QLatin1StringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `bool contains(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `(since 6.9) QStringList filter(const QLatin1StringMatcher &matcher) const`
- `QStringList filter(const QString &str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `QStringList filter(const QRegularExpression &re) const`
- `(since 6.7) QStringList filter(const QStringMatcher &matcher) const`
- `(since 6.7) QStringList filter(QLatin1StringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `QStringList filter(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `qsizetype indexOf(QLatin1StringView str, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `qsizetype indexOf(QStringView str, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `qsizetype indexOf(const QString &str, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `qsizetype indexOf(const QRegularExpression &re, qsizetype from = 0) const`
- `QString join(const QString &separator) const`
- `QString join(QChar separator) const`
- `QString join(QLatin1StringView separator) const`
- `QString join(QStringView separator) const`
- `qsizetype lastIndexOf(QLatin1StringView str, qsizetype from = -1, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `qsizetype lastIndexOf(QStringView str, qsizetype from = -1, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `qsizetype lastIndexOf(const QString &str, qsizetype from = -1, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `qsizetype lastIndexOf(const QRegularExpression &re, qsizetype from = -1) const`
- `qsizetype removeDuplicates()`
- `QStringList & replaceInStrings(const QString &before, const QString &after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `QStringList & replaceInStrings(const QRegularExpression &re, const QString &after)`
- `QStringList & replaceInStrings(QStringView before, QStringView after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `QStringList & replaceInStrings(QStringView before, const QString &after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `QStringList & replaceInStrings(const QString &before, QStringView after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `void sort(Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `QStringList operator+(const QStringList &other) const`
- `QStringList & operator<<(const QString &str)`
- `QStringList & operator<<(const QList<QString> &other)`
- `QStringList & operator<<(const QStringList &other)`
- `QStringList & operator=(const QList<QString> &other)`
- `QStringList & operator=(QList<QString> &&other)`

### 相关非成员函数

- `QMutableStringListIterator`
- `QStringListIterator`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QStringList::QStringList(const QList<QString> &other)`

**作用与语义：**

构建了`other`的副本。
该操作耗时为常数，因为QStringList是隐式共享的。这使得从函数返回QStringList非常快速。如果共享实例被修改，它会被复制（写时复制），这需要线性时间。

### `QStringList::QStringList(const QString &str)`

**作用与语义：**

构建一个包含给定字符串 `str` 的字符串列表。像这样可以轻松创建更长的列表：

**官方示例：**

```cpp
     QStringList longerList = (QStringList() << str1 << str2 << str3);
```

### `QStringList::QStringList(QList<QString> &&other)`

**作用与语义：**

来自`QList`的移动构造<`QString`>。
施工成功后，`other`将空无一人。

### `[noexcept] bool QStringList::contains(const QString &str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

如果列表包含字符串 `str`，返回 `true`;否则返回 `false`。
如果`cs`是`Qt::CaseSensitive`（默认），则字符串比较区分大小写;否则比较不区分大小写。

### `[noexcept] bool QStringList::contains(QLatin1StringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

如果列表中包含`str`查看的拉丁1字符串，返回`true`;否则返回`false`。
如果`cs`是`Qt::CaseSensitive`（默认），则字符串比较是区分大小写的;否则比较不区分大小写。

### `[noexcept] bool QStringList::contains(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

如果列表包含字符串 `str`，返回 `true`;否则返回 `false`。
如果`cs`是`Qt::CaseSensitive`（默认），则字符串比较区分大小写;否则比较不区分大小写。

### `[since 6.9] QStringList QStringList::filter(const QLatin1StringMatcher &matcher) const`

**作用与语义：**

返回由`matcher`匹配的所有字符串列表（即`matcher.indexIn()`返回索引>= 0）。
在大列表和/或字符串较长的列表中搜索时，使用`QLatin1StringMatcher`可能更快（最好的方法是做基准测试）。

**官方示例：**

```cpp
     QStringList veryLargeList;
     QLatin1StringMatcher matcher("Street"_L1, Qt::CaseInsensitive);
     QStringList filtered = veryLargeList.filter(matcher);
```

### `QStringList QStringList::filter(const QString &str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回包含子字符串`str`的所有字符串列表。
如果`cs`是`Qt::CaseSensitive`（默认），则字符串比较区分大小写;否则比较不区分大小写。
这等价于。

**官方示例：**

```cpp
     QStringList list;
     list << "Bill Murray" << "John Doe" << "Bill Clinton";

     QStringList result;
     result = list.filter("Bill");
     // result: ["Bill Murray", "Bill Clinton"]
```

### `QStringList QStringList::filter(const QRegularExpression &re) const`

**作用与语义：**

返回所有与正则表达式`re`匹配的字符串列表。

### `[since 6.7] QStringList QStringList::filter(const QStringMatcher &matcher) const`

**作用与语义：**

返回与`matcher`匹配的所有字符串列表（即`matcher.indexIn()`返回索引>= 0）。
在大列表和/或字符串较长的列表中搜索时，使用`QStringMatcher`可能更快（最好的方法是基准测试）。

**官方示例：**

```cpp
     QStringList veryLongList;
     QStringMatcher matcher(u"Straße", Qt::CaseInsensitive);
     QStringList filtered = veryLongList.filter(matcher);
```

### `[since 6.7] QStringList QStringList::filter(QLatin1StringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回由`matcher`匹配的所有字符串列表（即`matcher.indexIn()`返回索引>= 0）。
在大列表和/或字符串较长的列表中搜索时，使用`QLatin1StringMatcher`可能更快（最好的方法是做基准测试）。

**官方示例：**

```cpp
     QStringList veryLargeList;
     QLatin1StringMatcher matcher("Street"_L1, Qt::CaseInsensitive);
     QStringList filtered = veryLargeList.filter(matcher);
```

### `QStringList QStringList::filter(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回由`matcher`匹配的所有字符串列表（即`matcher.indexIn()`返回索引>= 0）。
在大列表和/或字符串较长的列表中搜索时，使用`QLatin1StringMatcher`可能更快（最好的方法是做基准测试）。

**官方示例：**

```cpp
     QStringList veryLargeList;
     QLatin1StringMatcher matcher("Street"_L1, Qt::CaseInsensitive);
     QStringList filtered = veryLargeList.filter(matcher);
```

### `[noexcept] qsizetype QStringList::indexOf(QLatin1StringView str, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回列表中第一个匹配`str`的索引位置，从索引位置`from`向前搜索。如果没有匹配的项目，返回-1。
如果`cs`是`Qt::CaseSensitive`（默认），则字符串比较区分大小写;否则比较不区分大小写。
注意：`cs`参数是在Qt 6.7中添加的，也就是说，这些方法现在会超载从基类继承的方法。在此之前，这些方法只有两个参数。这一变化是源代码兼容的，现有代码应继续正常工作。

### `qsizetype QStringList::indexOf(const QRegularExpression &re, qsizetype from = 0) const`

**作用与语义：**

返回列表中第一个匹配`str`的索引位置，从索引位置`from`向前搜索。如果没有匹配的项目，返回-1。
如果`cs`是`Qt::CaseSensitive`（默认），则字符串比较区分大小写;否则比较不区分大小写。
注意：`cs`参数是在Qt 6.7中添加的，也就是说，这些方法现在会超载从基类继承的方法。在此之前，这些方法只有两个参数。这一变化是源代码兼容的，现有代码应继续正常工作。

### `QString QStringList::join(const QString &separator) const`

**作用与语义：**

将字符串列表中的所有字符串合并为一个字符串，每个元素之间由给定的 `separator` 分隔（该字符串可以是空字符串）。

### `QString QStringList::join(QChar separator) const`

**作用与语义：**

注意：该功能会让`QStringList::join()`重载。

### `QString QStringList::join(QLatin1StringView separator) const`

**作用与语义：**

注意：该功能会让`QStringList::join()`重载。

### `QString QStringList::join(QStringView separator) const`

**作用与语义：**

将字符串列表中的所有字符串合并为一个字符串，每个元素之间由给定的 `separator` 分隔（该字符串可以是空字符串）。

### `[noexcept] qsizetype QStringList::lastIndexOf(QLatin1StringView str, qsizetype from = -1, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回列表中最后一个匹配`str`的索引位置，从索引位置`from`向后搜索。如果`from`为-1（默认值），搜索从最后一项开始。如果没有匹配的项，返回-1。
如果`cs`是`Qt::CaseSensitive`（默认），则字符串比较是区分大小写的;否则比较是不区分大小写的。
注意：`cs`参数是在Qt 6.7中添加的，也就是说，这些方法现在会超载从基类继承的方法。在此之前，这些方法只有两个参数。这一变化是源代码兼容的，现有代码应继续正常工作。

### `qsizetype QStringList::lastIndexOf(const QRegularExpression &re, qsizetype from = -1) const`

**作用与语义：**

返回列表中最后一个匹配`str`的索引位置，从索引位置`from`向后搜索。如果`from`为-1（默认值），搜索从最后一项开始。如果没有匹配的项，返回-1。
如果`cs`是`Qt::CaseSensitive`（默认），则字符串比较是区分大小写的;否则比较是不区分大小写的。
注意：`cs`参数是在Qt 6.7中添加的，也就是说，这些方法现在会超载从基类继承的方法。在此之前，这些方法只有两个参数。这一变化是源代码兼容的，现有代码应继续正常工作。

### `qsizetype QStringList::removeDuplicates()`

**作用与语义：**

该函数会从列表中移除重复的条目。条目不必排序。它们会保持原始顺序。
返回被移除的条目数量。

### `QStringList &QStringList::replaceInStrings(const QString &before, const QString &after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**作用与语义：**

返回一个字符串列表，每个字符串的 `before` 文本都被 `after` 文本替换，无论在 `before` 文本所在之处。
注意：如果使用空的`before`参数，`after`参数会在字符串的每个字符前后插入。
如果`cs`是`Qt::CaseSensitive`（默认），则字符串比较区分大小写;否则比较不区分大小写。

**官方示例：**

```cpp
     QStringList list;
     list << "alpha" << "beta" << "gamma" << "epsilon";
     list.replaceInStrings("a", "o");
     // list == ["olpho", "beto", "gommo", "epsilon"]
```

### `QStringList &QStringList::replaceInStrings(const QRegularExpression &re, const QString &after)`

**作用与语义：**

将每个字符串列表字符串中所有正则表达式`re`的出现替换为 `after`。返回字符串列表的引用。
对于包含捕获群的正则表达式，`after`中出现的\1， \2， ...被对应捕获群捕获的字符串替换。

**官方示例：**

```cpp
     QStringList list;
     list << "alpha" << "beta" << "gamma" << "epsilon";
     list.replaceInStrings(QRegularExpression("^a"), "o");
     // list == ["olpha", "beta", "gamma", "epsilon"]
```

### `QStringList &QStringList::replaceInStrings(QStringView before, QStringView after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**作用与语义：**

返回一个字符串列表，每个字符串的 `before` 文本都被 `after` 文本替换，无论在 `before` 文本所在之处。
注意：如果使用空的`before`参数，`after`参数会在字符串的每个字符前后插入。
如果`cs`是`Qt::CaseSensitive`（默认），则字符串比较区分大小写;否则比较不区分大小写。

**官方示例：**

```cpp
     QStringList list;
     list << "alpha" << "beta" << "gamma" << "epsilon";
     list.replaceInStrings("a", "o");
     // list == ["olpho", "beto", "gommo", "epsilon"]
```

### `QStringList &QStringList::replaceInStrings(QStringView before, const QString &after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**作用与语义：**

返回一个字符串列表，每个字符串的 `before` 文本都被 `after` 文本替换，无论在 `before` 文本所在之处。
注意：如果使用空的`before`参数，`after`参数会在字符串的每个字符前后插入。
如果`cs`是`Qt::CaseSensitive`（默认），则字符串比较区分大小写;否则比较不区分大小写。

**官方示例：**

```cpp
     QStringList list;
     list << "alpha" << "beta" << "gamma" << "epsilon";
     list.replaceInStrings("a", "o");
     // list == ["olpho", "beto", "gommo", "epsilon"]
```

### `QStringList &QStringList::replaceInStrings(const QString &before, QStringView after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**作用与语义：**

返回一个字符串列表，每个字符串的 `before` 文本都被 `after` 文本替换，无论在 `before` 文本所在之处。
注意：如果使用空的`before`参数，`after`参数会在字符串的每个字符前后插入。
如果`cs`是`Qt::CaseSensitive`（默认），则字符串比较区分大小写;否则比较不区分大小写。

**官方示例：**

```cpp
     QStringList list;
     list << "alpha" << "beta" << "gamma" << "epsilon";
     list.replaceInStrings("a", "o");
     // list == ["olpho", "beto", "gommo", "epsilon"]
```

### `void QStringList::sort(Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**作用与语义：**

按升序排序字符串列表。
如果`cs`是`Qt::CaseSensitive`（默认），则字符串比较区分大小写;否则比较不区分大小写。
排序使用STL的std：：sort()算法，该算法平均线性对数时间，即O（n log n）。
如果你想按任意顺序排序字符串，可以考虑使用 `QMap` 类。例如，你可以用 `QMap`<`QString`，`QString`> 来创建不区分大小写的顺序（例如，键是字符串的小写版本，值是字符串），或者用 `QMap`<int，`QString`> 按整数索引排序字符串。

### `QStringList QStringList::operator+(const QStringList &other) const`

**作用与语义：**

返回一个字符串列表，该字符串列表是该字符串列表与`other`字符串列表的连接。

### `QStringList &QStringList::operator<<(const QString &str)`

**作用与语义：**

将给定字符串 `str` 附加到该字符串列表，并返回对字符串列表的引用。

### `QStringList &QStringList::operator<<(const QList<QString> &other)`

**作用与语义：**

将`other`字符串列表附加到字符串列表，并返回对后者字符串列表的引用。

### `QStringList &QStringList::operator<<(const QStringList &other)`

**作用与语义：**

将`other`字符串列表附加到字符串列表，并返回对后者字符串列表的引用。

### `QStringList &QStringList::operator=(const QList<QString> &other)`

**作用与语义：**

从`QList`复制赋值操作符<`QString`>。将`other`字符串列表分配给该字符串列表。
手术后，`other`和`*this`相等。

### `QStringList &QStringList::operator=(QList<QString> &&other)`

**作用与语义：**

将赋值算符从 `QList` <`QString`>移动。将字符串的`other`列表移动到该字符串列表。
手术结束后，`other`会空无一人。

### `[alias] QMutableStringListIterator`

**作用与语义：**

`QStringListIterator`类型定义提供了一个类似Java的非const迭代器用于`QStringList`。
`QStringList` 既提供 Java 风格的迭代器，也提供 STL 风格的叠代器。Java 风格的非 const 迭代器只是 `QMutableListIterator` 的类型定义<`QString`>。

### `[alias] QStringListIterator`

**作用与语义：**

QStringListIterator 类型定义为 `QStringList` 提供了一个类似 Java 的 const 迭代器。
`QStringList` 既提供 Java 风格的迭代器，也提供 STL 风格的叠代器。Java 风格的 const 迭代器只是 `QListIterator` 的类型定义<`QString`>。

### `qsizetype indexOf(QStringView str, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回列表中第一个匹配`str`的索引位置，从索引位置`from`向前搜索。如果没有匹配的项目，返回-1。
如果`cs`是`Qt::CaseSensitive`（默认），则字符串比较区分大小写;否则比较不区分大小写。
注意：`cs`参数是在Qt 6.7中添加的，也就是说，这些方法现在会超载从基类继承的方法。在此之前，这些方法只有两个参数。这一变化是源代码兼容的，现有代码应继续正常工作。

### `qsizetype indexOf(const QString &str, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回列表中第一个完全匹配的`re`的索引位置，从索引位置`from`向前搜索。如果没有匹配的项目，返回-1。

### `qsizetype lastIndexOf(QStringView str, qsizetype from = -1, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回列表中最后一个匹配`str`的索引位置，从索引位置`from`向后搜索。如果`from`为-1（默认值），搜索从最后一项开始。如果没有匹配的项，返回-1。
如果`cs`是`Qt::CaseSensitive`（默认），则字符串比较是区分大小写的;否则比较是不区分大小写的。
注意：`cs`参数是在Qt 6.7中添加的，也就是说，这些方法现在会超载从基类继承的方法。在此之前，这些方法只有两个参数。这一变化是源代码兼容的，现有代码应继续正常工作。

### `qsizetype lastIndexOf(const QString &str, qsizetype from = -1, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回列表中最后一个完全匹配的`re`的索引位置，从索引位置`from`向后搜索。如果`from`为-1（默认值），搜索从最后一个项目开始。如果没有匹配的项目，返回-1。

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

`QStringList` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
