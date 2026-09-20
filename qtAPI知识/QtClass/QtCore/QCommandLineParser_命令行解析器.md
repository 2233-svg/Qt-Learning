# QCommandLineParser 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QCommandLineParser>`  
> 所属模块：`Qt6::Core`  
> 相关类型：`QCoreApplication`、`QCommandLineOption`、`QStringList`

## 它解决的不是“读取 argv”，而是建立命令行契约

`QCoreApplication::arguments()` 只能给出一串原始字符串，例如：

```text
archive-tool --output build/app.zip --verbose src include
```

应用还要回答几个更具体的问题：`--output` 是否需要一个值？`-v` 是否等价于 `--verbose`？未知参数应该报错还是交给子命令？用户输入 `--help` 时该显示什么？`QCommandLineParser` 就是把这些规则集中定义、解析并查询的类。

它与 `QCommandLineOption` 的分工很重要：

- `QCommandLineOption` 描述**一个选项的契约**，包括名称、说明、值名称和默认值。
- `QCommandLineParser` 登记全部契约，解析参数列表，记录哪些选项出现、它们的值和位置参数。

它不是 `QObject`：没有父对象、信号槽或线程亲和性，也不需要事件循环。它是不可复制的状态对象，通常在 `main()` 或专门的参数解析函数中创建；一次解析完成后读取结果即可。不要让多个线程同时修改或读取同一个实例，Qt 并未为这种共享并发访问提供保证。

## 先写出一个正常 CLI 的骨架

```cpp
#include <QCommandLineOption>
#include <QCommandLineParser>
#include <QCoreApplication>

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);
    QCoreApplication::setApplicationName("archive-tool");
    QCoreApplication::setApplicationVersion("1.2.0");

    QCommandLineParser parser;
    parser.setApplicationDescription("Pack source directories into an archive.");
    parser.addHelpOption();
    parser.addVersionOption();

    QCommandLineOption outputOption(
        {"o", "output"},
        "Write the archive to <file>.",
        "file");
    QCommandLineOption verboseOption(
        {"v", "verbose"},
        "Print each file as it is added.");

    if (!parser.addOptions({outputOption, verboseOption}))
        return 2;

    parser.addPositionalArgument(
        "sources",
        "Directories or files to pack.",
        "sources...");

    parser.process(app);

    const QString output = parser.value(outputOption);
    const bool verbose = parser.isSet(verboseOption);
    const QStringList sources = parser.positionalArguments();

    if (output.isEmpty() || sources.isEmpty())
        parser.showHelp(2);

    // 使用 output、verbose、sources 执行业务逻辑。
}
```

这里 `process(app)` 是一道明确的控制流分界线：成功时才会回到下一行；遇到未知选项、缺少必填值，或用户请求帮助、版本信息时，它会显示信息并调用 `exit()` 结束当前进程。因此，解析后的业务代码应写在它之后，清理工作不要只依赖栈对象析构。

## 参数是怎样被识别的

没有以 `-` 开头的参数会被收集为位置参数。单独的 `-` 不是选项，常可用来表示标准输入；`--` 之后的所有内容都会作为位置参数保留，即使它们看起来像 `--option`。

短选项通常是单字母，如 `-v`。长选项可用 `--verbose`，也接受单横线形式 `-verbose`。需要值的选项可写为 `--output=result.zip`，也可写为 `--output result.zip`；值以 `-` 开头也可以被当作值接收。

一个常见误会是“给带值选项不传值，就表示使用默认值”。不是这样。`QCommandLineParser` 没有“可选值”这一语义：一个选项要么不需要值，要么一旦出现就必须带值。需要“开关 + 可选参数”时，设计成两个选项，或改用位置参数并自行校验。

它也不会自动把 `--no-cache` 理解为 `--cache` 的反义。若业务需要显式关闭，应将 `no-cache` 作为独立选项名称加入，并自己决定与 `cache` 同时出现时的优先级。

## `parse()` 和 `process()`：错误由谁负责

日常命令行工具大多直接调用 `process()`：它负责解析、内建帮助与版本选项、错误输出和退出。GUI 程序或子命令程序往往需要保留控制权，此时改用 `parse()`。

```cpp
QCommandLineParser parser;
QCommandLineOption configOption({"c", "config"}, "Read <file>.", "file");
parser.addOption(configOption);

if (!parser.parse(QCoreApplication::arguments())) {
    const QString message = parser.errorText();
    // 可以显示自己的 QMessageBox、写日志，或返回一个可测试的错误结果。
    QCommandLineParser::showMessageAndExit(
        QCommandLineParser::MessageType::Error, message, 2);
}

const QString configPath = parser.value(configOption);
```

`parse()` 只做解析，失败时返回 `false`；调用方应从 `errorText()` 取得未知选项或缺少值等错误原因。传给它的 `QStringList` 第一个元素必须是程序名，虽然该元素会被忽略。`QCoreApplication::arguments()` 已满足这条约定。

`process()` 则会再次处理整份参数。它在已调用 `addHelpOption()` 后识别 `--help`、`--help-all`，在已调用 `addVersionOption()` 后识别 `--version`；这些情况以及解析错误都会使进程结束。不要在单元测试或希望继续运行的图形程序中随手调用它。

## 子命令和转发程序：为什么需要两阶段解析

假设工具支持：

```text
tool resize --width 640 --height 480
tool run child-program --its-own-option
```

顶层解析器一开始只知道 `resize` 或 `run`，还不知道后续的专属选项。可先用 `parse()` 找到第一个位置参数，根据子命令补充选项与帮助说明，然后再 `process()` 做最终校验。

```cpp
QCommandLineParser parser;
parser.addPositionalArgument("command", "Command to execute.");

parser.parse(QCoreApplication::arguments());
const QStringList positional = parser.positionalArguments();
const QString command = positional.value(0);

if (command == "resize") {
    parser.clearPositionalArguments();
    parser.addPositionalArgument(
        "resize",
        "Resize an image.",
        "resize [options] input");
    parser.addOptions({
        QCommandLineOption("width", "Target width.", "pixels"),
        QCommandLineOption("height", "Target height.", "pixels")
    });
}

parser.process(QCoreApplication::arguments());
```

`clearPositionalArguments()` 清除的是**帮助文本里的位置参数定义**，不是上一次解析得到的 `positionalArguments()`。这正是它适合子命令帮助文本的原因。

若程序是包装器、调试器或启动器，还可在解析前设置 `ParseAsPositionalArguments`：遇到第一个位置参数后，余下的 `--child-option` 都保留给被启动程序或另一个解析器。默认模式则会继续把后面的 `--opt`、`-t` 解析成当前程序的选项；用户也可以在默认模式下用 `--` 强制切换到位置参数。

## 两种兼容性模式不能在解析后再改

这两个 setter 都必须在第一次 `parse()` 或 `process()` 之前调用。

- `setSingleDashWordOptionMode(ParseAsCompactedShortOptions)` 是默认模式。`-abc` 会解释为 `-a -b -c`；若 `a` 需要值，则解释为 `-a bc`。编译器风格工具常需要它，例如 `-DNAME=VALUE` 或 `-Iinclude/path`。
- `setSingleDashWordOptionMode(ParseAsLongOptions)` 将 `-abc` 当作长选项 `--abc`，主要用于兼容历史上这样解析的程序。若首个短选项使用了 `QCommandLineOption::ShortOptionStyle` 标志，仍按 `-a bc` 处理。
- `setOptionsAfterPositionalArgumentsMode(ParseAsOptions)` 是默认模式，位置参数之后仍会继续解析当前程序的选项。
- `setOptionsAfterPositionalArgumentsMode(ParseAsPositionalArguments)` 适合子命令或参数转发：第一个位置参数之后的选项字串都不再由当前解析器消费。

命令行语法一旦发布就是用户接口。不要为了“看起来更统一”而更换 `-abc` 的解释方式；这可能让脚本悄悄改变含义。

## 帮助、版本与 Windows 上的退出提示

`addHelpOption()` 自动注册 `-h`、`--help`；Windows 还支持 `-?`。`--help-all` 会额外显示并非本程序定义的通用 Qt 选项。先调用 `setApplicationDescription()`，该描述才会写入帮助内容。

`addVersionOption()` 自动注册 `-v`、`--version`，输出来自 `QCoreApplication::applicationVersion()`；因此应先设置应用版本。

`showHelp()`、`showVersion()` 与 Qt 6.9 引入的静态函数 `showMessageAndExit()` 都不会返回。后者以 `MessageType::Information` 输出普通消息，以 `MessageType::Error` 输出错误消息。Windows 上必要时 Qt 可能用消息框呈现这些内容；部署脚本或纯终端场景可设置环境变量 `QT_COMMAND_LINE_PARSER_NO_GUI_MESSAGE_BOXES` 禁用消息框。

## 查询结果时，区分“是否出现”和“取什么值”

```cpp
QCommandLineOption includeOption(
    {"I", "include"},
    "Add an include directory.",
    "directory");
parser.addOption(includeOption);
parser.parse({"tool", "-Iinc", "--include=third_party"});

const bool supplied = parser.isSet(includeOption);  // true
const QString last = parser.value(includeOption);    // "third_party"
const QStringList all = parser.values(includeOption); // {"inc", "third_party"}
```

- `isSet()` 适合无值开关；传入原先保存的 `QCommandLineOption` 最不容易把别名写错。
- `value()` 对重复出现的选项只返回最后一个值；未出现时返回该选项的默认值。若选项不接收值，返回空字符串。
- `values()` 返回每一次出现的全部值；未出现时返回默认值列表。若选项不接收值，返回空列表。
- 以名称查询时，可以使用同一个已登记选项的短名或长名；未知名称得到 `false`、空字符串或空列表。
- `optionNames()` 按遇到顺序列出成功识别的名称，保留重复项且不带前导横线。`--mode=fast` 只记录 `mode`。
- `unknownOptionNames()` 用相同形式列出未识别名称，适合在 `parse()` 失败后补充诊断。

## 生命周期、边界与常见坑

- 先构造 `QCoreApplication`，再取 `arguments()` 或调用 `process(app)`。应用名、版本也应在 `addHelpOption()`、`addVersionOption()` 和生成帮助文本前设置好。
- `addOption()` 失败的原因是选项没有名称，或任一名称与已登记名称冲突。不要忽略返回值。批量 `addOptions()` 也应检查结果，文档没有承诺失败时会回滚已加入的项。
- `QCoreApplication` 及其 GUI 子类会先解析某些 Qt 内建参数。若某个选项的值恰好长得像 Qt 内建参数，例如 `--profile -reverse`，后者可能在 `QCommandLineParser` 看见参数前被应用对象消费。需要这种值时，重新设计命令行接口或仔细验证目标应用类型。
- `addPositionalArgument()` 只是声明 Usage 和 Arguments 帮助文本，不会替你保证“至少一个输入文件”或“数值范围合法”。解析后仍要检查位置参数数量、路径、枚举值和数值范围。
- `helpText()` 只生成文本，不退出。需要嵌入自定义 UI 或日志时使用它；需要遵循 CLI 的标准退出行为时使用 `showHelp()`。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造与寿命 | `QCommandLineParser()` | 创建空解析器，随后登记选项和位置参数规则。 | 非 `QObject` 且不可复制；通常局部创建，在解析后读取结果。 |
| 构造与寿命 | `~QCommandLineParser()` | 销毁解析器及其内部解析状态。 | 不依赖父对象机制；不要在多个线程并发访问同一实例。 |
| 枚举 | `MessageType`（Qt 6.9 起） | 指定 `showMessageAndExit()` 的消息类别。 | `Information` 对应普通信息，`Error` 对应错误信息；函数会退出。 |
| 枚举值 | `MessageType::Information` | 表示信息消息，通常写到标准输出。 | Windows 上必要时也可能显示为带信息图标的消息框。 |
| 枚举值 | `MessageType::Error` | 表示错误消息，通常写到标准错误输出。 | 传入非零退出码，便于脚本或调用方识别失败。 |
| 枚举 | `OptionsAfterPositionalArgumentsMode` | 决定位置参数之后看似选项的字符串如何解释。 | 必须在 `parse()` 或 `process()` 前设置。 |
| 枚举值 | `ParseAsOptions` | 继续把位置参数后的 `--opt`、`-t` 当作当前程序选项。 | 默认模式；要把后续内容强制当位置参数可让用户输入 `--`。 |
| 枚举值 | `ParseAsPositionalArguments` | 在首个位置参数后停止消费选项字串。 | 适用于子命令、包装器、调试器和转发参数的工具。 |
| 枚举 | `SingleDashWordOptionMode` | 决定 `-abc` 这种单横线多字符写法的语义。 | 必须在首次解析前设置；改动会影响既有脚本兼容性。 |
| 枚举值 | `ParseAsCompactedShortOptions` | 将 `-abc` 当作紧凑短选项，或在 `a` 需值时理解为 `-a bc`。 | 默认且推荐给新程序；适合编译器风格参数。 |
| 枚举值 | `ParseAsLongOptions` | 将 `-abc` 当作长选项 `--abc`。 | 主要用于兼容旧程序；`ShortOptionStyle` 有特殊例外。 |
| 解析策略 | `setSingleDashWordOptionMode(SingleDashWordOptionMode)` | 设置单横线多字符选项的解释规则。 | 必须在 `parse()` 或 `process()` 前调用；选错会改变 `-abc` 的含义。 |
| 解析策略 | `setOptionsAfterPositionalArgumentsMode(OptionsAfterPositionalArgumentsMode)` | 设置位置参数之后的选项字串是否仍由当前解析器处理。 | 必须在首次解析前调用；子命令转发通常选择 `ParseAsPositionalArguments`。 |
| 选项登记 | `addOption(const QCommandLineOption &)` | 登记一个要识别的选项定义。 | 无名称或名称与既有项冲突会返回 `false`；应立即检查。 |
| 选项登记 | `addOptions(const QList<QCommandLineOption> &)` | 批量登记多个选项。 | 只有全部成功才返回 `true`；失败时不要假定已登记项被回滚。 |
| 内建选项 | `addHelpOption()` | 登记 `-h`、`--help`，并支持 `--help-all`。 | `process()` 遇到它会显示帮助并退出；Windows 还支持 `-?`。 |
| 内建选项 | `addVersionOption()` | 登记 `-v`、`--version` 并返回对应选项对象。 | 版本文本来自 `QCoreApplication::applicationVersion()`；应先设置版本。 |
| 帮助文本 | `setApplicationDescription(const QString &)` | 设置帮助内容中显示的程序说明。 | 在展示帮助前设置，避免帮助页只有选项而没有用途说明。 |
| 帮助文本 | `applicationDescription() const` | 读取已设置的程序说明。 | 未设置时得到空字符串；它不读取应用对象的其他描述字段。 |
| 帮助文本 | `addPositionalArgument(const QString &, const QString &, const QString &)` | 声明位置参数在 Usage 和 Arguments 中的名称、说明与语法。 | 仅影响帮助文本；不验证参数数量和业务合法性。 |
| 帮助文本 | `clearPositionalArguments()` | 清除位置参数的帮助定义。 | 不清空已解析的位置参数；常用于按子命令重建帮助。 |
| 解析 | `parse(const QStringList &)` | 只解析参数并保存结果或错误。 | 参数首项必须是程序名；失败返回 `false`，调用方读取 `errorText()`。 |
| 解析 | `process(const QStringList &)` | 解析指定列表，并处理内建选项与错误。 | 帮助、版本或解析错误都会调用 `exit()`；成功时才继续执行。 |
| 解析 | `process(const QCoreApplication &)` | 使用应用对象提供的命令行参数执行 `process()`。 | 应在 `QCoreApplication` 创建后调用；退出语义与另一重载相同。 |
| 解析结果 | `errorText() const` | 返回最近一次解析失败的错误文本。 | 主要配合 `parse()`；可交给自定义 GUI、日志或错误输出。 |
| 解析结果 | `positionalArguments() const` | 返回未被识别为选项的位置参数。 | `--` 后的所有参数也会出现在此处；仍需自行校验数量和内容。 |
| 解析结果 | `optionNames() const` | 返回已识别选项的名称列表。 | 保留遇到顺序和重复项，不带横线；`--x=value` 只记录 `x`。 |
| 解析结果 | `unknownOptionNames() const` | 返回未识别选项的名称列表。 | 用于 `parse()` 失败后的诊断；格式与 `optionNames()` 相同。 |
| 出现检查 | `isSet(const QString &) const` | 按一个已登记的短名或长名判断选项是否出现。 | 名称未知或未出现都返回 `false`；传 `QCommandLineOption` 重载更稳妥。 |
| 出现检查 | `isSet(const QCommandLineOption &) const` | 按选项对象判断是否出现。 | 无值布尔开关推荐用此重载，能避免别名拼写错误。 |
| 取单个值 | `value(const QString &) const` | 按选项名称取得最后一个值。 | 未出现时返回默认值；无值选项、未知名称均得到空字符串。 |
| 取单个值 | `value(const QCommandLineOption &) const` | 按选项对象取得最后一个值。 | 重复选项只取最后一次；需要全部值时使用 `values()`。 |
| 取全部值 | `values(const QString &) const` | 按选项名称取得每次出现的值。 | 未出现时返回默认值列表；无值选项和未知名称得到空列表。 |
| 取全部值 | `values(const QCommandLineOption &) const` | 按选项对象取得每次出现的值。 | 适用于可重复选项，例如多次 `--include <dir>`。 |
| 帮助输出 | `helpText() const` | 生成完整帮助文本而不改变控制流。 | 适合嵌入自定义界面、日志或测试断言。 |
| 终止输出 | `showHelp(int)` | 显示帮助并以指定退出码结束进程。 | 用户主动请求帮助通常传 `0`；用法错误传非零值。 |
| 终止输出 | `showVersion()` | 显示应用版本并以成功状态结束进程。 | 版本来自 `QCoreApplication::applicationVersion()`；该函数不返回。 |
| 终止输出 | `showMessageAndExit(MessageType, const QString &, int)`（Qt 6.9 起） | 显示普通信息或错误信息，再以指定码退出。 | Windows 可能弹消息框；设 `QT_COMMAND_LINE_PARSER_NO_GUI_MESSAGE_BOXES` 可禁用。 |

## 一句话记忆

`QCommandLineParser` 负责把原始参数变成可查询的选项和位置参数；简单 CLI 用 `process()`，需要自行展示错误、支持子命令或保留控制流时用 `parse()`。
