# QCommandLineParser

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“CommandLineParser”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QCommandLineParser` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QCommandLineParser>`
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

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `(since 6.9) enum class MessageType { Information, Error }`
- `enum OptionsAfterPositionalArgumentsMode { ParseAsOptions, ParseAsPositionalArguments }`
- `enum SingleDashWordOptionMode { ParseAsCompactedShortOptions, ParseAsLongOptions }`

### 公有函数

- `QCommandLineParser()`
- `~QCommandLineParser()`
- `QCommandLineOption addHelpOption()`
- `bool addOption(const QCommandLineOption &option)`
- `bool addOptions(const QList<QCommandLineOption> &options)`
- `void addPositionalArgument(const QString &name, const QString &description, const QString &syntax = QString())`
- `QCommandLineOption addVersionOption()`
- `QString applicationDescription() const`
- `void clearPositionalArguments()`
- `QString errorText() const`
- `QString helpText() const`
- `bool isSet(const QString &name) const`
- `bool isSet(const QCommandLineOption &option) const`
- `QStringList optionNames() const`
- `bool parse(const QStringList &arguments)`
- `QStringList positionalArguments() const`
- `void process(const QStringList &arguments)`
- `void process(const QCoreApplication &app)`
- `void setApplicationDescription(const QString &description)`
- `void setOptionsAfterPositionalArgumentsMode(QCommandLineParser::OptionsAfterPositionalArgumentsMode parsingMode)`
- `void setSingleDashWordOptionMode(QCommandLineParser::SingleDashWordOptionMode singleDashWordOptionMode)`
- `void showHelp(int exitCode = 0)`
- `void showVersion()`
- `QStringList unknownOptionNames() const`
- `QString value(const QString &optionName) const`
- `QString value(const QCommandLineOption &option) const`
- `QStringList values(const QString &optionName) const`
- `QStringList values(const QCommandLineOption &option) const`

### 静态公有成员

- `(since 6.9) void showMessageAndExit(QCommandLineParser::MessageType type, const QString &message, int exitCode = 0)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[since 6.9] enum class QCommandLineParser::MessageType`

**作用与语义：**

枚举用于指定消息类型及其向用户展示的方式。
- `QCommandLineParser::MessageType::Information`：`0`;用于显示信息消息。消息将打印到`stdout`。
- `QCommandLineParser::MessageType::Error`：`1`;用于显示错误信息。消息将打印到`stderr`。
这个枚举是在Qt 6.9引入的。

### `enum QCommandLineParser::OptionsAfterPositionalArgumentsMode`

**作用与语义：**

该枚举描述了解析器如何解释位置参数之后出现的选项。
- `QCommandLineParser::ParseAsOptions`：`0`;`application argument --opt -t` 被解释为设置选项 `opt` 和 `t`，就像 `application --opt -t argument` 一样。这是默认的解析模式。为了指定 `--opt` 和 `-t` 是位置参数，用户可以使用 `--`，如 `application argument -- --opt -t`。
- `QCommandLineParser::ParseAsPositionalArguments`：`1`;`application argument --opt` 被解释为两个位置参数，分别是 `argument` 和 `--opt`。该模式适用于旨在启动其他可执行文件（如包装器、调试工具等）或支持内部命令后跟命令选项的可执行文件。`argument` 是命令的名称，之后出现的所有选项都可以被另一个命令行解析器收集和解析，可能存在于另一个可执行文件中。

### `enum QCommandLineParser::SingleDashWordOptionMode`

**作用与语义：**

该枚举描述了解析器如何解释使用单一破折号后接多个字母的命令行选项，如`-abc`。
- `QCommandLineParser::ParseAsCompactedShortOptions`：`0`;`-abc` 被解释为 `-a -b -c`，即三个在命令行中被压缩的空头期权，如果这些期权都不取值。如果 `a` 取值，则将其解释为 `-a bc`，即空头期权 `a` 后跟 value `bc`。这通常用于表现为编译器的工具，以处理诸如`-DDEFINE=VALUE`或`-I/include/path`等选项。这是默认的解析模式。建议新应用程序使用此模式。
- `QCommandLineParser::ParseAsLongOptions`：`1`;`-abc` 被解释为 `--abc`，即名为 `abc` 的长选项。这就是 Qt 自有工具（uic、rcc 等）一直用于解析参数的方式。该模式应用于在以此类方式解析参数的应用程序中保持兼容性。如果`a`选项设置了 `QCommandLineOption::ShortOptionStyle` 标志，则有例外，此时仍被解释为 `-a bc`。

### `QCommandLineParser::QCommandLineParser()`

**作用与语义：**

构建一个命令行解析器对象。

### `[noexcept] QCommandLineParser::~QCommandLineParser()`

**作用与语义：**

摧毁命令行解析器对象。

### `QCommandLineOption QCommandLineParser::addHelpOption()`

**作用与语义：**

为命令行解析器添加帮助选项。
该命令行指定的选项由 `-h` 或 `--help` 描述。在 Windows 上，也支持替代`-?`。选项 `--help-all` 扩展到输出中包含未由该命令定义的通用 Qt 选项。
这些选项由`QCommandLineParser`自动处理。
记得使用`setApplicationDescription()`设置应用描述，使用该选项时会显示。
返回选项实例，可用于调用`isSet()`。

**官方示例：**

```cpp
 int main(int argc, char *argv[])
 {
     QCoreApplication app(argc, argv);
     QCoreApplication::setApplicationName("my-copy-program");
     QCoreApplication::setApplicationVersion("1.0");

     QCommandLineParser parser;
     parser.setApplicationDescription("Test helper");
     parser.addHelpOption();
     parser.addVersionOption();
     parser.addPositionalArgument("source", QCoreApplication::translate("main", "Source file to copy."));
     parser.addPositionalArgument("destination", QCoreApplication::translate("main", "Destination directory."));

     // A boolean option with a single name (-p)
     QCommandLineOption showProgressOption("p", QCoreApplication::translate("main", "Show progress during copy"));
     parser.addOption(showProgressOption);

     // A boolean option with multiple names (-f, --force)
     QCommandLineOption forceOption(QStringList() << "f" << "force",
             QCoreApplication::translate("main", "Overwrite existing files."));
     parser.addOption(forceOption);

     // An option with a value
     QCommandLineOption targetDirectoryOption(QStringList() << "t" << "target-directory",
             QCoreApplication::translate("main", "Copy all source files into <directory>."),
             QCoreApplication::translate("main", "directory"));
     parser.addOption(targetDirectoryOption);

     // Process the actual command line arguments given by the user
     parser.process(app);

     const QStringList args = parser.positionalArguments();
     // source is args.at(0), destination is args.at(1)

     bool showProgress = parser.isSet(showProgressOption);
     bool force = parser.isSet(forceOption);
     QString targetDir = parser.value(targetDirectoryOption);
     // ...
 }
```

### `bool QCommandLineParser::addOption(const QCommandLineOption &option)`

**作用与语义：**

它增加了解析时需要寻找的选项`option`。
如果添加选项成功，返回`true`;否则返回`false`。
如果选项没有附加名称，或者该选项名称与之前添加的选项名称冲突，则添加该选项失败。

### `bool QCommandLineParser::addOptions(const QList<QCommandLineOption> &options)`

**作用与语义：**

添加解析时需要寻找的选项。选项由参数`options`指定。
如果所有选项都成功添加，返回`true`;否则返回`false`。
请参阅文档`addOption()`该功能可能失效的说明。

### `void QCommandLineParser::addPositionalArgument(const QString &name, const QString &description, const QString &syntax = QString())`

**作用与语义：**

为帮助文本定义了额外的论据。
参数`name`和`description`会出现在帮助的`Arguments:`部分。如果指定了`syntax`，则会附加在使用行，否则`name`将被附加。

**官方示例：**

```cpp
 // Usage: image-editor file
 //
 // Arguments:
 //   file                  The file to open.
 parser.addPositionalArgument("file", QCoreApplication::translate("main", "The file to open."));

 // Usage: web-browser [urls...]
 //
 // Arguments:
 //   urls                URLs to open, optionally.
 parser.addPositionalArgument("urls", QCoreApplication::translate("main", "URLs to open, optionally."), "[urls...]");

 // Usage: cp source destination
 //
 // Arguments:
 //   source                Source file to copy.
 //   destination           Destination directory.
 parser.addPositionalArgument("source", QCoreApplication::translate("main", "Source file to copy."));
 parser.addPositionalArgument("destination", QCoreApplication::translate("main", "Destination directory."));
```

### `QCommandLineOption QCommandLineParser::addVersionOption()`

**作用与语义：**

增加了`-v` / `--version`选项，显示应用程序的版本字符串。
这个选项由`QCommandLineParser`自动处理。
你可以用`QCoreApplication::setApplicationVersion()`设置实际版本字符串。
返回选项实例，可用于调用`isSet()`。

### `QString QCommandLineParser::applicationDescription() const`

**作用与语义：**

返回`setApplicationDescription()`中设置的应用描述。

### `void QCommandLineParser::clearPositionalArguments()`

**作用与语义：**

清除帮助文本中额外参数的定义。
这仅在支持多个具有不同选项的命令的工具的特殊情况下需要。一旦确定实际命令，即可定义该命令的选项，并相应调整命令的帮助文本。

**官方示例：**

```cpp
 QCoreApplication app(argc, argv);
 QCommandLineParser parser;

 parser.addPositionalArgument("command", "The command to execute.");

 // Call parse() to find out the positional arguments.
 parser.parse(QCoreApplication::arguments());

 const QStringList args = parser.positionalArguments();
 const QString command = args.isEmpty() ? QString() : args.first();
 if (command == "resize") {
     parser.clearPositionalArguments();
     parser.addPositionalArgument("resize", "Resize the object to a new size.", "resize [resize_options]");
     parser.addOption(QCommandLineOption("size", "New size.", "new_size"));
     parser.process(app);
     // ...
 }

 /*
 This code results in context-dependent help:

 $ tool --help
 Usage: tool command

 Arguments:
   command  The command to execute.

 $ tool resize --help
 Usage: tool resize [resize_options]

 Options:
   --size <size>  New size.

 Arguments:
   resize         Resize the object to a new size.
 */
```

### `QString QCommandLineParser::errorText() const`

**作用与语义：**

返回翻译后的错误文本。只有当`parse()`返回`false`时才应调用此错误文本。

### `QString QCommandLineParser::helpText() const`

**作用与语义：**

返回包含完整帮助信息的字符串。

### `bool QCommandLineParser::isSet(const QString &name) const`

**作用与语义：**

检查选项`name`是否被传递给了申请。
如果选项`name`设置，返回`true`，否则返回 false。
所提供的名称可以是任何添加`addOption()`选项的长或短名称。所有选项名称均视为等价。如果未识别该名称或该选项不存在，则返回false。

**官方示例：**

```cpp
 bool verbose = parser.isSet("verbose");
```

### `bool QCommandLineParser::isSet(const QCommandLineOption &option) const`

**作用与语义：**

检查`option`是否已传递给申请。
如果`option`被设置，返回`true`，否则返回假。
这是检查无数值选项的推荐方法。

**官方示例：**

```cpp
 QCoreApplication app(argc, argv);
 QCommandLineParser parser;
 QCommandLineOption verboseOption("verbose");
 parser.addOption(verboseOption);
 parser.process(app);
 bool verbose = parser.isSet(verboseOption);
```

### `QStringList QCommandLineParser::optionNames() const`

**作用与语义：**

返回一份已找到的期权名称列表。
该列表返回解析器找到的所有识别期权名称列表，按发现顺序排列。对于任何形式为{–option=value}的多头期权，价值部分将被剔除。
该列表中的名称不包含前面的破折号字符。如果解析器多次遇到名称，该列表可能会出现多个。
列表中的任何条目都可以与`value()`或`values()`一起使用，以获得任何相关的期权值。

### `bool QCommandLineParser::parse(const QStringList &arguments)`

**作用与语义：**

解析命令行`arguments`。
大多数程序不需要调用这个，简单调用`process()`就足够了。
parse() 是更低层的，只负责解析。应用程序需要处理错误，如果 parse() 返回 `false`，则使用 `errorText()`。这在图形程序中显示图形错误消息时非常有用。
调用parse()代替`process()`也有助于暂时忽略未知选项，因为在调用`process()`之前，会根据某个参数提供更多选项定义。
别忘了`arguments`必须以可执行文件的名称开头（但可以忽略）。
在解析错误（未知选项或缺失值）时返回`false`;否则返回`true`。

### `QStringList QCommandLineParser::positionalArguments() const`

**作用与语义：**

返回一个位置论元列表。
这些都是未被纳入选项的论点。

### `void QCommandLineParser::process(const QStringList &arguments)`

**作用与语义：**

处理命令行`arguments`。
除了解析选项（如`parse()`），该函数还处理内置选项并处理错误。
内置选项如果被调用`addVersionOption` `--version`，如果`addHelpOption`调用则`--help`/`--help-all`。
当调用这些选项之一，或发生错误（例如传递未知选项）时，当前进程将停止，使用exit()函数。

### `void QCommandLineParser::process(const QCoreApplication &app)`

**作用与语义：**

命令行是从 `QCoreApplication` 实例 `app` 获取的。

### `void QCommandLineParser::setApplicationDescription(const QString &description)`

**作用与语义：**

`helpText()` 表示应用`description`。

### `void QCommandLineParser::setOptionsAfterPositionalArgumentsMode(QCommandLineParser::OptionsAfterPositionalArgumentsMode parsingMode)`

**作用与语义：**

将解析模式设置为`parsingMode`。必须在`process()`或`parse()`之前调用。

### `void QCommandLineParser::setSingleDashWordOptionMode(QCommandLineParser::SingleDashWordOptionMode singleDashWordOptionMode)`

**作用与语义：**

将解析模式设置为`singleDashWordOptionMode`。必须在`process()`或`parse()`之前调用。

### `void QCommandLineParser::showHelp(int exitCode = 0)`

**作用与语义：**

显示帮助信息，并退出应用程序。该选项由 –help 选项自动触发，但用户未正确调用应用时也可用来显示帮助。退出代码设置为 `exitCode`。如果用户请求查看帮助，应设置为 0，错误时应设置为其他值。

### `[static, since 6.9] void QCommandLineParser::showMessageAndExit(QCommandLineParser::MessageType type, const QString &message, int exitCode = 0)`

**作用与语义：**

显示一个`message`，并以给定的`exitCode`退出应用。
`message`通常会根据给定的`type`直接打印到`stdout`或`stderr`，或者在必要时会显示在Windows的消息框中，并根据`type`显示信息图标或错误图标（如果不想要消息框，请设置`QT_COMMAND_LINE_PARSER_NO_GUI_MESSAGE_BOXES`环境变量）。
这和`showHelp`、`showVersion`和内置选项使用的消息显示方式相同（如果`addVersionOption`被调用`--version`，`addHelpOption`则`--help` / `--help-all`）。

### `void QCommandLineParser::showVersion()`

**作用与语义：**

显示`QCoreApplication::applicationVersion()`的版本信息，并退出应用程序。该功能由 –version 选项自动触发，但不使用 `process()` 时也可用于显示版本。退出代码设为 EXIT_SUCCESS（0）。

### `QStringList QCommandLineParser::unknownOptionNames() const`

**作用与语义：**

返回一个未知期权名称列表。
本列表将包含未被识别的长名和短名选项。对于任何格式为{–option=value}的长选项，价值部分已被省略，只添加了长名称。
该列表中的名称不包含前面的破折号字符。如果解析器多次遇到名称，该列表可能会出现多个。

### `QString QCommandLineParser::value(const QString &optionName) const`

**作用与语义：**

返回给定期权名称的期权值 `optionName`，若未找到则返回空字符串。
所提供的名称可以是任何添加`addOption()`选项的长或短名称。所有选项名称都被视为等价。如果名称未被识别或该选项不存在，则返回空字符串。
对于解析器找到的选项，返回该选项的最后一个值。如果命令行中未指定该选项，则返回默认值。
如果选项没有取值，会打印警告，并返回空字符串。

### `QString QCommandLineParser::value(const QCommandLineOption &option) const`

**作用与语义：**

返回给定`option`的选项值，若未找到则返回空字符串。
对于解析器找到的选项，返回该选项的最后一个值。如果命令行中未指定该选项，则返回默认值。
如果选项不取值，则返回空字符串。

### `QStringList QCommandLineParser::values(const QString &optionName) const`

**作用与语义：**

返回给定期权名称`optionName`的选项值列表，若未找到则返回空列表。
所提供的名称可以是任何添加`addOption()`选项的长短名称。所有选项名称都被视为等价。如果名称未被识别或该选项不存在，则返回一个空列表。
对于解析器找到的选项，列表会包含每次该选项被解析器遇到的时间条目。如果命令行中未指定该选项，则返回默认值。
如果期权不取值，则返回一个空列表。

### `QStringList QCommandLineParser::values(const QCommandLineOption &option) const`

**作用与语义：**

返回给定`option`的选项值列表，若未找到则返回空列表。
对于解析器找到的选项，列表会包含每次该选项被解析器遇到的时间条目。如果命令行中未指定该选项，则返回默认值。
如果期权不取值，则返回一个空列表。

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

`QCommandLineParser` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
