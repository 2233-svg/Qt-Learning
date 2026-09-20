# Qt QRegularExpressionValidator 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QRegularExpressionValidator>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QValidator -> QRegularExpressionValidator`  
> 定位：把 `QRegularExpression` 转换为适合编辑控件使用的三态输入校验器

## 1. 它解决什么问题

正则表达式可以描述字符串格式，但编辑控件需要的不只是“匹配/不匹配”两个结果。用户输入到一半时，文本可能暂时不完整，却仍然是一个合理的后续输入起点；如果验证器此时直接判定失败，输入体验会被破坏。

`QRegularExpressionValidator` 把正则表达式接入 `QValidator` 的三态协议：

- `Acceptable`：当前字符串已经是完整有效结果。
- `Intermediate`：当前字符串还不完整，但继续编辑有机会变成有效结果。
- `Invalid`：当前字符串不可能通过继续编辑变成有效结果。

它尤其适合 `QLineEdit`、可编辑 `QComboBox` 等文本输入控件。验证器并不负责提交业务数据、显示错误提示或自动修复字符串；它只负责根据当前规则判断输入状态。

## 2. 真实使用场景

### 2.1 固定格式编号

例如设备编号、工单号、版本号或内部短码：

```text
[A-Z][0-9]{4}
```

用户输入 `A` 时可以保持 `Intermediate`，输入完整的 `A1234` 后变成 `Acceptable`，输入小写 `a` 或额外空格则为 `Invalid`。

### 2.2 文件名和轻量文本格式

可以限制文件名后缀、标签、环境变量名或不允许空白的短字符串。需要注意，正则验证的是字符串格式，不会检查文件是否存在、路径是否安全或业务对象是否可用。

### 2.3 可编辑下拉框

给 `QComboBox` 的编辑器设置验证器，可以限制用户新建的文本格式；但验证器不会自动决定该文本是否插入模型，插入策略和业务提交仍由 `QComboBox`/应用代码负责。

### 2.4 输入协议的第一道筛选

网络地址、十六进制 token、简单日期片段等可以先用正则做格式筛选，再在提交时使用专门解析器做真正的语义校验。正则适合作为输入阶段的约束，不应替代完整解析器。

## 3. 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

```cpp
#include <QRegularExpressionValidator>
```

qmake 工程使用：`QT += gui`。

该类要求 Qt 构建启用 validator 和 regular expression 支持。它是 `QObject` 子类，不能复制，通常用父对象管理生命周期。

## 4. 最小可用示例

下面的示例限制 `QLineEdit` 接受一个大写字母加三位数字。验证器由编辑框作为父对象管理：

```cpp
#include <QApplication>
#include <QLineEdit>
#include <QRegularExpression>
#include <QRegularExpressionValidator>

int main(int argc, char **argv)
{
    QApplication app(argc, argv);

    QLineEdit edit;
    const QRegularExpression expression(QStringLiteral("[A-Z][0-9]{3}"));
    auto *validator = new QRegularExpressionValidator(expression, &edit);
    edit.setValidator(validator);

    edit.show();
    return app.exec();
}
```

验证器会把传入的正则按完整字符串匹配处理，因此这里不需要再写 `^` 和 `$`。用户输入 `A`、`A1` 或 `A12` 时通常是 `Intermediate`，`A123` 是 `Acceptable`，而 `a123` 或 `A1234` 是 `Invalid`。

## 5. 最重要的三态协议

### 5.1 `Acceptable`

字符串已经匹配验证器的完整正则，可以作为最终结果。对 `QLineEdit` 来说，`returnPressed()` 和 `editingFinished()` 只有在验证结果为 `Acceptable` 时才会发出。

### 5.2 `Intermediate`

字符串当前不是完整匹配，但可能通过继续输入、删除或编辑变成有效值。例如规则 `[A-Z][0-9]{3}` 下，空字符串、`A`、`A1` 和 `A12` 都可能是合理的中间状态。

`Intermediate` 不是错误，也不是最终通过。编辑控件通常允许用户停留在该状态，以便继续编辑。

### 5.3 `Invalid`

字符串已经不可能通过继续添加合法字符得到完整匹配，或者包含规则明确禁止的内容。例如上述规则下，`a`、`_`、`A-` 和 `A1234` 都是无效的。

注意，`Invalid` 的定义与“当前业务提交失败”不同。复杂业务规则可能需要允许用户先输入一个中间文本，再在提交阶段显示更具体的错误。

## 6. 正则会被自动锚定

`QRegularExpressionValidator` 会自动把表达式包在 `\A` 和 `\z` 之间，因此始终尝试匹配整个输入字符串，而不是在字符串中查找任意子串。

例如：

```cpp
QRegularExpressionValidator validator(
    QRegularExpression(QStringLiteral("\\d+")));
```

它接受 `123`，但不接受 `abc123` 或 `123xyz`。如果需求是“字符串中包含一个数字序列”，应使用 `QRegularExpression` 的匹配 API 或其它专门逻辑，而不是直接把同一个表达式交给验证器。

手工再写 `^`/`$` 通常没有必要，还可能让表达式在多行选项、换行输入或复杂分组下更难理解。验证器的完整匹配边界应作为规则设计的一部分明确记录。

## 7. 部分匹配为什么能产生 `Intermediate`

验证器内部不仅检查完整匹配，还会判断当前输入是否是一个可能继续完成的前缀。对规则 `[A-Z][0-9]`：

| 输入 | 状态 | 原因 |
| --- | --- | --- |
| `A7` | `Acceptable` | 已完整匹配 |
| `A` | `Intermediate` | 再输入一个数字即可完成 |
| 空字符串 | `Intermediate` | 仍可能从头输入有效值 |
| `_` | `Invalid` | 首字符已经不可能满足 `[A-Z]` |
| `A-` | `Invalid` | 第二个字符不是数字 |

中间态判断依赖正则结构。可选分支、量词、字符类、锚点、换行和 Unicode 选项都会影响结果；不要只根据“正则看起来能匹配”猜测 `Intermediate` 的边界，应通过实际输入表测试。

## 8. `QRegularExpression` 的配置边界

### 8.1 pattern 与 pattern options

正则的大小写、Unicode 字符属性、非捕获行为和其它规则由 `QRegularExpression` 的 pattern/options 决定。`QRegularExpressionValidator` 不会把正则改写成业务语言，也不会把不合法的数字或日期自动解析出来。

例如，`\d` 是否只匹配 ASCII 数字、是否使用 Unicode 属性，取决于 `QRegularExpression` 的选项；如果输入协议必须严格限制 ASCII，应在字符类和选项层面明确表达。

### 8.2 无效正则

`QRegularExpression` 自身可能因为语法错误而无效。构造验证器前应检查 `expression.isValid()`，必要时记录 `errorString()` 和 `patternErrorOffset()`。不要把一个编译失败的表达式交给输入控件后，再把所有输入都归因于用户错误。

更换正则时也应先构造、检查和测试新的 `QRegularExpression`，再调用 `setRegularExpression()`。

### 8.3 空 pattern

默认构造的验证器持有空 pattern；Qt 文档规定它匹配任何字符串，包括空字符串。因此“没有设置规则”和“拒绝所有输入”不是同一个状态。若业务要求必须输入内容，应显式使用 `.+` 或更准确的业务规则。

## 9. 与输入控件的协作

### 9.1 `QLineEdit`

`QLineEdit::setValidator()` 保存验证器用于约束用户编辑：

- `Acceptable`：允许作为最终输入。
- `Intermediate`：允许用户继续编辑。
- `Invalid`：用户编辑到该值时通常会被阻止。
- `returnPressed()` 和 `editingFinished()` 只在内容为 `Acceptable` 时发出。

这不等于所有对 `QLineEdit` 的编程赋值都会被自动拒绝。应用在调用 `setText()`、加载配置或恢复草稿后，仍应主动检查 `hasAcceptableInput()` 或重新调用验证器。

### 9.2 可编辑 `QComboBox`

可编辑的 `QComboBox` 可以使用验证器约束编辑文本，但验证器只负责文本状态；当前文本是否插入列表、插入位置以及重复项策略由组合框的模型和插入策略决定。关闭 editable 状态时，Qt 文档说明验证器和 completer 会被移除。

### 9.3 提交阶段仍要重新校验

输入控件的状态可能受规则变更、程序赋值、剪贴板粘贴和业务上下文变化影响。保存前应再次验证并进行真正解析，不能只依赖用户编辑阶段曾经出现过 `Acceptable`。

## 10. 生命周期、线程和可复制性

`QRegularExpressionValidator` 是 `QObject`，构造函数的 `parent` 会传给 `QObject`。把验证器设置为编辑控件或窗口的子对象可以避免悬空指针：

```cpp
auto *validator = new QRegularExpressionValidator(expression, lineEdit);
lineEdit->setValidator(validator);
```

不要把同一个 QObject 验证器按值复制，也不要在它被控件使用时提前 `delete`。如果验证器和控件不在同一线程，跨线程直接调用其 QObject 方法或把它挂到不同线程对象上会破坏 Qt 的对象线程规则；输入控件和验证器通常都应留在 GUI 线程。

## 11. 常见错误与排查

### 以为验证器做的是子串搜索

验证器自动执行完整匹配。需要部分字符串搜索时用 `QRegularExpression::match()`，不要把验证器当搜索器。

### 把 `Intermediate` 当成错误

编辑中的空字符串、前缀和暂不完整的合法结构通常应该是 `Intermediate`。如果正则把所有前缀都判成 `Invalid`，用户可能无法从空输入逐步编辑到有效值。

### 用正则代替语义解析

一个匹配 `YYYY-MM-DD` 的表达式仍可能接受 `2026-99-99`。验证器只说明格式匹配，提交时还要使用 `QDate::fromString()` 或业务解析器检查实际含义。

### 忽略光标位置参数

`validate(QString &input, int &pos)` 的 `pos` 是输入光标位置。`QRegularExpressionValidator` 在输入不匹配时会把它设置为输入长度；匹配时不修改它。自定义调用代码不要假设验证器永远不会改变 `pos`。

### 期待 `fixup()` 自动修复

`QRegularExpressionValidator` 没有重写 `QValidator::fixup()`；基类默认实现什么也不做。按 Enter 时，如果输入不是 `Acceptable`，验证器不会自动补零、删空格或修复大小写。需要修复功能时，应在提交逻辑中显式规范化，或编写自定义 `QValidator` 子类重写 `fixup()`。

### 改了表达式却没有处理现有文本

`setRegularExpression()` 只改变验证规则并发出相关通知，不会替应用决定如何迁移当前输入。修改规则后，应重新检查编辑控件当前文本，并决定保留、清空、修复还是提示用户。

## 12. 逐项 API 说明

### `enum QValidator::State`

`QRegularExpressionValidator` 继承 `QValidator::State`：

- `Invalid = 0`：字符串明显无效。
- `Intermediate = 1`：字符串是可能继续完成的中间值。
- `Acceptable = 2`：字符串可作为最终有效值。

输入控件应按这三态协议处理，而不是把 `Intermediate` 简化成 `Invalid`。

### `regularExpression : QRegularExpression`

**作用：** 保存用于验证的正则表达式。

**默认值：** 空 pattern，匹配任何字符串，包括空字符串。

**注意：** 属性保存的是 `QRegularExpression` 值；真正的完整匹配边界由验证器自动添加。若表达式无效，应用应在设置前检查。

### `QRegularExpressionValidator::QRegularExpressionValidator(QObject *parent = nullptr)`

**作用：** 构造验证器，并将 `parent` 传给 `QObject`。

**默认规则：** 持有空 pattern，因此接受任何字符串，包括空字符串。

**生命周期：** 如果传入编辑控件作为父对象，控件销毁时会自动销毁验证器。

### `QRegularExpressionValidator::QRegularExpressionValidator(const QRegularExpression &re, QObject *parent = nullptr)`

**作用：** 构造一个使用 `re` 的验证器。

**注意：** `re` 应是有效表达式；构造不会把表达式注册到其它对象，也不会负责显示编译错误。验证器按完整输入匹配处理 `re`。

### `QRegularExpressionValidator::~QRegularExpressionValidator()`

**作用：** 销毁验证器。

**边界：** 销毁前应先确保仍持有该指针的编辑控件不再使用它；使用父对象管理可以减少悬空指针风险。

### `QRegularExpression QRegularExpressionValidator::regularExpression() const`

**作用：** 返回当前验证器使用的正则表达式副本。

**用途：** 读取 pattern、pattern options 或检查表达式状态。返回的是值类型，修改返回值不会自动改变验证器；需要修改规则时调用 `setRegularExpression()`。

### `void QRegularExpressionValidator::setRegularExpression(const QRegularExpression &re)`

**作用：** 替换当前验证规则。

**语义：**

- 新规则会影响之后的 `validate()` 结果。
- 规则变化会发出 `regularExpressionChanged(const QRegularExpression &)`。
- 作为 `QValidator`，影响有效性的属性变化也可通过基类 `changed()` 观察。

**注意：** 设置后要重新考虑控件中已经存在的文本；无效表达式应在调用前处理。

### `void QRegularExpressionValidator::regularExpressionChanged(const QRegularExpression &re)`

**作用：** 在 `regularExpression` 属性发生变化时通知监听者。

**适用场景：** 规则切换、动态表单和调试面板。信号参数是新表达式的值，不是旧值。

### `QValidator::State QRegularExpressionValidator::validate(QString &input, int &pos) const`

**作用：** 根据当前正则判断输入处于 `Acceptable`、`Intermediate` 还是 `Invalid`。

**完整匹配语义：** 验证器自动使用 `\A` 和 `\z`，因此 `input` 必须整体匹配；部分匹配且可以继续完成时返回 `Intermediate`。

**`pos` 语义：**

- 输入不匹配时，`pos` 会被设置为 `input.length()`。
- 输入匹配时，`pos` 不被修改。

调用者应把 `pos` 当作输入输出参数，不能只把它当作只读光标位置。

### `QValidator::QValidator(QObject *parent = nullptr)`

**作用：** 初始化基类验证器，并设置 QObject 父对象。

**注意：** `QRegularExpressionValidator` 应通过自己的构造函数创建，不直接调用基类构造。

### `QValidator::changed()`

**作用：** 通知监听者验证规则中影响有效性的属性发生变化。

**注意：** 对 `QRegularExpressionValidator`，需要监听具体正则内容时优先使用 `regularExpressionChanged()`；不要把信号当作每次输入变化的通知。

### `void QValidator::fixup(QString &input) const`

**作用：** 为可以修复用户输入的验证器提供修正入口。

**在本类中的语义：** `QRegularExpressionValidator` 使用基类默认实现，不自动改变输入。需要规范化文本时应自定义验证器或在业务层显式处理，并在修复后重新调用 `validate()`。

### `QLocale QValidator::locale() const`

**作用：** 读取验证器的 locale。

**边界：** locale 主要服务于数值类验证器的本地化解析；不要期待 `QRegularExpressionValidator` 会因为 locale 自动改变正则字符类、大小写或业务格式。

### `void QValidator::setLocale(const QLocale &locale)`

**作用：** 设置基类验证器的 locale。

**边界：** 它不会改写当前 `QRegularExpression` pattern。对正则验证通常不是改变匹配规则的主要 API。

## API 速查表

| 类别 | API | 解决什么问题 | 使用时重点注意 |
| --- | --- | --- | --- |
| 状态类型 | `QValidator::State { Invalid, Intermediate, Acceptable }` | 表达编辑中的无效、中间和最终有效状态 | `Intermediate` 不是错误；提交通常要求 `Acceptable` |
| 属性 | `regularExpression : QRegularExpression` | 保存文本验证规则 | 默认空 pattern 接受任何字符串；验证器自动做完整匹配 |
| 构造 | `explicit QRegularExpressionValidator(QObject *parent = nullptr)` | 创建默认验证器 | 默认接受任何字符串；使用 parent 管理生命周期 |
| 构造 | `explicit QRegularExpressionValidator(const QRegularExpression &re, QObject *parent = nullptr)` | 创建指定正则验证器 | 设置前检查 `re.isValid()`；不要把验证器当搜索器 |
| 析构 | `~QRegularExpressionValidator()` | 释放验证器对象 | 控件仍持有指针时不要提前销毁；优先使用 QObject 父对象 |
| 属性读取 | `QRegularExpression regularExpression() const` | 读取当前正则 | 返回值类型副本，修改副本不会修改验证器 |
| 属性写入 | `void setRegularExpression(const QRegularExpression &re)` | 动态更换验证规则 | 规则变化会影响现有文本；先检查新表达式 |
| 属性通知 | `void regularExpressionChanged(const QRegularExpression &re)` | 观察正则属性变化 | 参数是新表达式；不是每次输入变化信号 |
| 核心验证 | `QValidator::State validate(QString &input, int &pos) const` | 判断完整、可继续或明显无效的输入 | 自动 `\A...\z`；未匹配时 `pos` 设为输入长度 |
| 基类生命周期 | `QValidator(QObject *parent = nullptr)` | 初始化验证器 QObject | 由派生类构造函数间接使用 |
| 基类通知 | `void QValidator::changed()` | 通知有效性相关规则变化 | 不要当作文本输入变化通知 |
| 基类修复 | `void QValidator::fixup(QString &input) const` | 为可修复验证器提供修正入口 | 本类默认不修复；修复后必须重新验证 |
| 基类 locale | `QLocale locale() const` | 读取验证器 locale | 对正则匹配通常不改变 pattern 语义 |
| 基类 locale | `void setLocale(const QLocale &locale)` | 设置验证器 locale | 不会自动本地化正则；主要供数值验证器使用 |
| 控件协作 | `QLineEdit::setValidator(const QValidator *v)` | 将验证器接入单行编辑 | 用户可编辑到 `Intermediate`，最终信号要求 `Acceptable` |
| 控件协作 | `QLineEdit::hasAcceptableInput() const` | 检查当前文本是否最终有效 | 程序赋值、加载草稿后也应主动检查 |
| 控件协作 | `QComboBox::setValidator(const QValidator *validator)` | 限制可编辑组合框文本 | 只约束文本，不决定是否插入模型 |

---

### 一句话总结

`QRegularExpressionValidator` 把正则转换成适合交互式输入的三态验证器：它自动做整串匹配，用 `Intermediate` 保留合理的编辑前缀，用 `Acceptable` 表示可提交结果；格式验证之后仍要进行真正的业务解析，且 `fixup()` 默认不会替你修复文本。
