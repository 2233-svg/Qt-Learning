# QCommandLineOption

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QCommandLineOption` 是 Qt 的值类型，围绕“CommandLineOption”保存可复制的数据，并提供查询、转换或修改 API。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QCommandLineOption` 是 Qt 值类型与隐式共享机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

**适用场景：** 先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

## 2. 依赖与对象关系

- 头文件：`#include <QCommandLineOption>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

### 状态、生命周期和线程

**生命周期：** 值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

**状态与结果：** 重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

**线程与事件循环：** 值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

## 3. 直接使用

先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum Flag { HiddenFromHelp, ShortOptionStyle, IgnoreOptionsAfter }`
- `flags Flags`

### 公有函数

- `QCommandLineOption(const QString &name)`
- `QCommandLineOption(const QStringList &names)`
- `QCommandLineOption(const QString &name, const QString &description, const QString &valueName = QString(), const QString &defaultValue = QString())`
- `QCommandLineOption(const QStringList &names, const QString &description, const QString &valueName = QString(), const QString &defaultValue = QString())`
- `QCommandLineOption(const QCommandLineOption &other)`
- `~QCommandLineOption()`
- `QStringList defaultValues() const`
- `QString description() const`
- `QCommandLineOption::Flags flags() const`
- `QStringList names() const`
- `void setDefaultValue(const QString &defaultValue)`
- `void setDefaultValues(const QStringList &defaultValues)`
- `void setDescription(const QString &description)`
- `void setFlags(QCommandLineOption::Flags flags)`
- `void setValueName(const QString &valueName)`
- `void swap(QCommandLineOption &other)`
- `QString valueName() const`
- `QCommandLineOption & operator=(QCommandLineOption &&other)`
- `QCommandLineOption & operator=(const QCommandLineOption &other)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QCommandLineOption::Flagflags QCommandLineOption::Flags`

**作用与语义：**

- `QCommandLineOption::HiddenFromHelp`：`0x1`;在用户可见的帮助输出中隐藏此选项。所有选项默认可见。为特定选项设置此标志使该选项处于内部状态，即不在帮助输出中列出。
- `QCommandLineOption::ShortOptionStyle`：`0x2`;无论`QCommandLineParser::setSingleDashWordOptionMode`设置了什么，该选项始终被视为短选项。这使得即使解析器处于`QCommandLineParser::ParseAsLongOptions`模式，`-DDEFINE=VALUE`或`-I/include/path`等标志仍可被解释为短标志。
- `QCommandLineOption::IgnoreOptionsAfter`：`0x4`;[自6.9起]此选项之后不会解析其他选项。对于需要向次级应用程序发送额外命令行参数的情况非常有用。如果为该选项提供了值，则会被忽略。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `[explicit] QCommandLineOption::QCommandLineOption(const QString &name)`

**作用与语义：**

构建一个名为 `name` 的命令行选项对象。
名称可以是短的也可以是长的。如果名字只有一个字符，则被视为短名字。选项名称不得为空，不得以破折号或斜杠开头，不得包含`=`，且不得重复。

### `[explicit] QCommandLineOption::QCommandLineOption(const QStringList &names)`

**作用与语义：**

构建一个命令行选项对象，名称为 `names`。
这种重载允许为期权设置多个名称，例如`o`和`output`。
名称可以是短的或长的。列表中任何一个字符长度的名称都是短名字。选项名称不得为空，不能以破折号或斜杠开头，不能包含`=`，且不得重复。

### `QCommandLineOption::QCommandLineOption(const QString &name, const QString &description, const QString &valueName = QString(), const QString &defaultValue = QString())`

**作用与语义：**

构建一个包含给定参数的命令行选项对象。
选项名称设置为`name`。名称可以是短或长。如果名字长度为一个字符，则视为短名称。选项名称不得为空，不能以破折号或斜杠开头，不能包含`=`，且不能重复。
描述设置为`description`。通常在描述末尾加上“.”。
此外，如果期权期望某值，则需要设置`valueName`。期权的默认值设为`defaultValue`。
在 5.4 之前的 Qt 版本中，该构造器被`explicit`。在 Qt 5.4 及以后版本中，该构造函数不再存在，且可用于统一初始化：

**官方示例：**

```cpp
 QCommandLineParser parser;
 parser.addOption({"verbose", "Verbose mode. Prints out more information."});
```

### `QCommandLineOption::QCommandLineOption(const QStringList &names, const QString &description, const QString &valueName = QString(), const QString &defaultValue = QString())`

**作用与语义：**

构建一个包含给定参数的命令行选项对象。
这种重载允许为期权设置多个名称，例如`o`和`output`。
选项名称设置为`names`。名称可以是短的或长的。列表中任何长度为一个字符的名字都是短名称。选项名称不得为空，不得以破折号或斜杠开头，不能包含`=`，且不得重复。
描述设置为`description`。通常在描述末加上“.”。
此外，如果期权期望某值，则需要设置`valueName`值。期权的默认值设为`defaultValue`。
在 5.4 之前的 Qt 版本中，该构造器被`explicit`。在 Qt 5.4 及以后版本中，该构造器不再存在，且可用于统一初始化：

**官方示例：**

```cpp
 QCommandLineParser parser;
 parser.addOption({{"o", "output"}, "Write generated data into <file>.", "file"});
```

### `QCommandLineOption::QCommandLineOption(const QCommandLineOption &other)`

**作用与语义：**

构建一个QCommandLineOption对象，该对象是QCommandLineOption对象`other`的复制品。

### `[noexcept] QCommandLineOption::~QCommandLineOption()`

**作用与语义：**

摧毁命令行选项对象。

### `QStringList QCommandLineOption::defaultValues() const`

**作用与语义：**

返回该选项设置的默认值。

### `QString QCommandLineOption::description() const`

**作用与语义：**

返回该选项的描述设置。

### `QCommandLineOption::Flags QCommandLineOption::flags() const`

**作用与语义：**

返回一组影响该命令行选项的标志。

### `QStringList QCommandLineOption::names() const`

**作用与语义：**

返回该选项设置的名称。

### `void QCommandLineOption::setDefaultValue(const QString &defaultValue)`

**作用与语义：**

将该选项的默认值设置为`defaultValue`。
如果应用程序用户未在命令行中指定该选项，则使用默认值。
如果`defaultValue`空，则该选项没有默认值。

### `void QCommandLineOption::setDefaultValues(const QStringList &defaultValues)`

**作用与语义：**

将该选项默认值列表设置为`defaultValues`。
如果应用程序用户未在命令行中指定该选项，则使用默认值。

### `void QCommandLineOption::setDescription(const QString &description)`

**作用与语义：**

将该选项使用的描述设置为`description`。
通常在描述末尾加上“.”。
`QCommandLineParser::showHelp()`使用了该描述。

### `void QCommandLineOption::setFlags(QCommandLineOption::Flags flags)`

**作用与语义：**

将影响该命令行选项的标志设置为`flags`。

### `void QCommandLineOption::setValueName(const QString &valueName)`

**作用与语义：**

将文档的期望值命名为`valueName`。
未分配值的选项具有类似布尔的行为：用户要么指定 –option，要么不指定。
赋予值的选项需要为期望值设置名称，以在帮助输出中的选项文档中。名称为`o`和`output`，值名为`file`的选项将显示为`-o, --output <file>`。
如果你预计该选项只出现一次，就打电话给`QCommandLineParser::value()`;如果你预计该选项会多次出现，`QCommandLineParser::values()`。

### `[noexcept] void QCommandLineOption::swap(QCommandLineOption &other)`

**作用与语义：**

将该选项替换为`other`。这个操作非常快，从未失败过。

### `QString QCommandLineOption::valueName() const`

**作用与语义：**

返回期望值的名称。
如果是空的，期权不会取值。

### `[noexcept] QCommandLineOption &QCommandLineOption::operator=(QCommandLineOption &&other)`

**作用与语义：**

Move-assign `other`到该`QCommandLineOption`实例。

### `QCommandLineOption &QCommandLineOption::operator=(const QCommandLineOption &other)`

**作用与语义：**

复制`other`对象并将其分配给该`QCommandLineOption`对象。

### `enum Flag { HiddenFromHelp, ShortOptionStyle, IgnoreOptionsAfter }`

**作用与语义：**

- `QCommandLineOption::HiddenFromHelp`：`0x1`;在用户可见的帮助输出中隐藏此选项。所有选项默认可见。为特定选项设置此标志使该选项处于内部状态，即不在帮助输出中列出。
- `QCommandLineOption::ShortOptionStyle`：`0x2`;无论`QCommandLineParser::setSingleDashWordOptionMode`设置了什么，该选项始终被视为短选项。这使得即使解析器处于`QCommandLineParser::ParseAsLongOptions`模式，`-DDEFINE=VALUE`或`-I/include/path`等标志仍可被解释为短标志。
- `QCommandLineOption::IgnoreOptionsAfter`：`0x4`;[自6.9起]此选项之后不会解析其他选项。对于需要向次级应用程序发送额外命令行参数的情况非常有用。如果为该选项提供了值，则会被忽略。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `flags Flags`

**作用与语义：**

- `QCommandLineOption::HiddenFromHelp`：`0x1`;在用户可见的帮助输出中隐藏此选项。所有选项默认可见。为特定选项设置此标志使该选项处于内部状态，即不在帮助输出中列出。
- `QCommandLineOption::ShortOptionStyle`：`0x2`;无论`QCommandLineParser::setSingleDashWordOptionMode`设置了什么，该选项始终被视为短选项。这使得即使解析器处于`QCommandLineParser::ParseAsLongOptions`模式，`-DDEFINE=VALUE`或`-I/include/path`等标志仍可被解释为短标志。
- `QCommandLineOption::IgnoreOptionsAfter`：`0x4`;[自6.9起]此选项之后不会解析其他选项。对于需要向次级应用程序发送额外命令行参数的情况非常有用。如果为该选项提供了值，则会被忽略。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

## 6. 深入实践与常见坑

### 生命周期和资源边界

值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

### 状态和错误边界

重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

### 线程边界

值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

### 最容易出现的错误

不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QCommandLineOption` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
