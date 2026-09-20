# Qt QCommandLineOption 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QCommandLineOption>`  
> 所属模块：`Qt6::Core`  
> 核心定位：定义一个命令行选项的名字、参数、默认值、帮助文本和解析标志

## 1. 它解决什么问题

命令行程序需要一份清晰的输入契约：用户可以写哪些选项、选项是否带值、帮助中怎样描述、重复出现时如何取值。`QCommandLineOption` 就是这份契约中的一个条目。

它只**描述**选项，不读取 `argv`，也不保存某次解析的结果。实际解析、错误提示、帮助输出、`isSet()` 和 `value()` 都由 `QCommandLineParser` 完成。

```text
QCommandLineOption
  describes --output <file>
          |
          | parser.addOption()
          v
QCommandLineParser
  parses argv and exposes values
```

因此应把 option 当作可复制的配置值，在调用 `parser.addOption()` 前完整设置；不要试图在 parser 已解析后修改 option 再期待解析结果自动改变。

## 2. 最小可用示例

```cpp
#include <QCommandLineOption>
#include <QCommandLineParser>
#include <QCoreApplication>

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);
    QCommandLineParser parser;

    QCommandLineOption outputOption(
        {"o", "output"},
        "Write generated data to <file>.",
        "file",
        "result.txt");

    parser.addOption(outputOption);
    parser.process(app);

    const QString path = parser.value(outputOption);
    writeOutput(path);
}
```

`{"o", "output"}` 表示一个选项有短名 `-o` 和长名 `--output`。`valueName` 是参数的占位名，它既告诉 parser 此选项需要一个值，也用于帮助文本展示为 `-o, --output <file>`。

## 3. 名称、值名和默认值的关系

### 3.1 选项名称

一个字符长的名称被视为短名，较长名称被视为长名。传给构造函数的名字本身不包含 `-`、`--` 或 `/`。

以下规则由 Qt 文档明确规定：

- 名称不能为空。
- 名称不能以 `-` 或 `/` 开头。
- 名称不能包含 `=`。
- 同一 option 的 names 列表中不能重复。

```cpp
QCommandLineOption verbose("verbose", "Enable verbose output.");
QCommandLineOption output({"o", "output"}, "Write to <file>.", "file");
```

名称是用户接口的一部分。短名应少而稳定；长名使用完整、可读的英文词；弃用旧名时可临时把新旧名字放在同一 `QStringList`，让它们映射到同一个选项。

### 3.2 `valueName` 不只是帮助文字

`valueName` 非空表示这个选项期待参数值。它应描述值的角色，而不是某个示例值：

```cpp
QCommandLineOption jobs("jobs", "Run at most <count> tasks.", "count");
QCommandLineOption format("format", "Select output <type>.", "type");
```

真正的字符串转整数、范围校验、文件是否可写等不属于 `QCommandLineOption`；在 parser 成功解析后由业务代码验证。

### 3.3 默认值

构造函数的 `defaultValue` 或 `setDefaultValue()` 定义“选项未出现时 parser 返回的值”。使用默认值不等于选项被用户显式设置，因此如果要区分“用户没传”和“用户传了与默认相同的值”，结合 `QCommandLineParser::isSet()` 判断。

`setDefaultValues()` 支持多个默认值，对应 parser 的 `values()` 使用场景。单值选项使用 `value()`，允许重复的选项用 `values()`。

## 4. Flags：改变解析器如何看待这个选项

`Flags` 是 `QFlags<Flag>`，可用按位或组合多个标志。

| 标志 | 作用 | 使用场景 | 重点注意 |
| --- | --- | --- | --- |
| `HiddenFromHelp` | 从用户可见帮助中隐藏该选项。 | 内部诊断、兼容旧选项或受控测试开关。 | 仍会被解析；不要把它当作安全机制。 |
| `ShortOptionStyle` | 强制按短选项解释。 | `-DNAME=VALUE`、`-I/path` 等编译器风格参数。 | 可覆盖 parser 的单连字符单词处理模式。 |
| `IgnoreOptionsAfter` | 遇到该选项后，后续参数不再按本 parser 的选项解析。 | 包装器把余下参数转交给子程序。 | Qt 6.9 起提供；该 option 自己带的值会被忽略。 |

```cpp
QCommandLineOption forwardOption(
    "run",
    "Run a secondary program; remaining arguments are forwarded.");
forwardOption.setFlags(QCommandLineOption::IgnoreOptionsAfter);
```

`IgnoreOptionsAfter` 与常见的 `--` 参数分隔需求相近，但它是绑定在某个明确 option 上的规则。设计 CLI 时要把转发边界写入帮助文本，避免用户误以为后续 `--foo` 仍会由主程序解释。

## 5. 描述文字是 CLI 的接口文档

`description` 会被 `QCommandLineParser::showHelp()` 使用。Qt 文档建议描述以句号结尾；更重要的是描述应清楚说明动作、参数含义、单位与默认行为。

好的描述：

```cpp
QCommandLineOption timeout(
    "timeout",
    "Abort the request after <milliseconds>; default is 5000.",
    "milliseconds",
    "5000");
```

不好的描述：

```text
Set timeout.
```

后者无法告诉用户单位、默认值和发生超时时的具体行为。

## 6. 值语义与 parser 的边界

`QCommandLineOption` 是隐式共享值类型，支持复制、赋值、移动赋值与交换。复制它很自然，例如把公共选项加入多个 parser 或在测试中复用。

但是 parser 的解析结果属于 parser 实例和那次命令行输入。option 本身不会记录“是否出现”“取到什么值”或“是否解析失败”。保持这条边界可以避免把定义对象带进多线程或重复解析时造成状态混淆。

## 7. 常见错误

### 7.1 把 `--output` 作为 name 传入

错误的前缀会违反名称规则。构造时传 `"output"`，帮助和解析器会负责展示、识别 `--output`。

### 7.2 忘记设置 `valueName`

没有 valueName 的 option 会被当作无值开关。需要参数的选项必须提供像 `"file"`、`"count"` 这样的占位名。

### 7.3 只读 `value()`，不检查用户是否显式传入

有默认值时，`value()` 永远可能非空。要区分来源，用 `parser.isSet(option)`。

### 7.4 将 `HiddenFromHelp` 当成权限控制

隐藏只影响帮助输出，任何人仍可传入这个 option。敏感行为必须有真实认证、授权或构建配置限制。

### 7.5 用 `IgnoreOptionsAfter` 却仍期望解析后续主程序选项

该标志定义的就是终止点。放置它之前先确定哪一段参数属于主程序，哪一段属于被转发程序。

## API 速查表
### 构造、复制与交换

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `explicit QCommandLineOption(const QString &name)` | 用一个短名或长名创建空选项定义。 | 名称不能为空，不能带 `-`、`/` 或 `=`。 |
| 构造 | `explicit QCommandLineOption(const QStringList &names)` | 用多个别名创建选项定义。 | 一个字符名是短名；列表内名字不能重复。 |
| 构造 | `QCommandLineOption(const QString &name, const QString &description, const QString &valueName = {}, const QString &defaultValue = {})` | 一次设置单名称、帮助、值名和单个默认值。 | `valueName` 非空时该 option 期待值。 |
| 构造 | `QCommandLineOption(const QStringList &names, const QString &description, const QString &valueName = {}, const QString &defaultValue = {})` | 一次设置多个别名及其完整定义。 | 常用于 `-o` 与 `--output` 指向同一语义。 |
| 复制 | `QCommandLineOption(const QCommandLineOption &other)` | 复制选项定义。 | 不复制任何 parser 的解析结果。 |
| 析构 | `~QCommandLineOption() noexcept` | 销毁选项定义。 | 没有 QObject 生命周期或事件循环依赖。 |
| 赋值 | `QCommandLineOption &operator=(const QCommandLineOption &other)` | 用另一选项定义覆盖当前对象。 | 已添加到 parser 的定义不应靠修改旧变量来更新。 |
| 赋值 | `QCommandLineOption &operator=(QCommandLineOption &&other) noexcept` | 移动赋值另一选项定义。 | 移动后源对象进入部分形成状态。 |
| 交换 | `void swap(QCommandLineOption &other) noexcept` | 快速交换两个选项定义。 | 主要用于泛型代码；不要在 parser 解析期间改定义。 |

### 内容与标志

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 名称 | `QStringList names() const` | 返回该选项的所有短名和长名。 | 返回的是定义元数据，不含命令行中实际使用了哪一个别名。 |
| 值名 | `void setValueName(const QString &name)` | 设置帮助中显示的参数占位名。 | 非空 name 表示选项期待值，例如 `file` 或 `count`。 |
| 值名 | `QString valueName() const` | 返回参数占位名。 | 不返回实际解析到的值；实际值由 parser 查询。 |
| 描述 | `void setDescription(const QString &description)` | 设置帮助输出中的描述。 | 明确写动作、单位和默认行为，Qt 建议句末加句号。 |
| 描述 | `QString description() const` | 返回当前帮助描述。 | 用于生成自定义文档或检查定义。 |
| 默认 | `void setDefaultValue(const QString &defaultValue)` | 设置一个默认值。 | 默认值不代表用户显式传入，配合 `isSet()` 区分。 |
| 默认 | `void setDefaultValues(const QStringList &defaultValues)` | 设置多个默认值。 | 重复选项场景用 parser 的 `values()` 读取。 |
| 默认 | `QStringList defaultValues() const` | 返回定义的默认值列表。 | 这是契约信息，不是一次解析的结果。 |
| 标志 | `void setFlags(QCommandLineOption::Flags flags)` | 设置影响解析或帮助的 flags。 | 组合标志用按位或；目标 Qt 低于 6.9 时不能用 `IgnoreOptionsAfter`。 |
| 标志 | `QCommandLineOption::Flags flags() const` | 返回当前 flags。 | 用于检查是否隐藏、短选项强制或终止后续解析。 |

### 与解析器协作

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 注册 | `QCommandLineParser::addOption(const QCommandLineOption &option)` | 将选项定义加入 parser。 | 在 `process()` 或 `parse()` 前注册，配置好后再添加。 |
| 是否出现 | `QCommandLineParser::isSet(const QCommandLineOption &option)` | 判断用户是否显式提供某个选项。 | 有默认值时不要用 `value()` 是否为空代替它。 |
| 单值读取 | `QCommandLineParser::value(const QCommandLineOption &option)` | 读取单个解析值或默认值。 | 还要自行检查数字范围、路径合法性等业务规则。 |
| 多值读取 | `QCommandLineParser::values(const QCommandLineOption &option)` | 读取重复出现的全部值或默认值列表。 | 只对允许重复语义的选项使用。 |

---

### 一句话总结

`QCommandLineOption` 负责定义 CLI 的一个稳定、可说明的输入契约；它不解析参数，和 `QCommandLineParser` 配合后才形成“注册、解析、读取、验证”的完整流程。
