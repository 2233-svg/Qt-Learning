# QValidator 深入笔记

> 适用版本：Qt 6.11.1
> 头文件：`#include <QValidator>`
> 所属模块：`Qt6::Gui`
> 继承：`QObject -> QValidator`

## 它解决什么问题

`QValidator` 解决的是“用户正在输入时如何判断文本是否可接受”的问题。普通布尔校验只适合提交后的最终检查，而交互式输入框需要允许用户处在半成品状态：例如范围是 `10` 到 `99` 时，用户刚输入 `4`，它不是最终合法值，但继续输入 `2` 后就会变成 `42`。`QValidator` 用 `Invalid`、`Intermediate`、`Acceptable` 三态模型表达这种过程。

它本身是抽象基类，真正常用的是 `QIntValidator`、`QDoubleValidator`、`QRegularExpressionValidator`，或者业务代码自定义的派生类。Qt Widgets 中的 `QLineEdit`、`QSpinBox`、可编辑 `QComboBox` 会按这个三态结果决定是否允许继续编辑、是否接受回车、以及是否尝试修正内容。

## 实际使用场景

- 输入框只允许用户输入端口号、年龄、金额、坐标等有范围的数值。
- 表单字段需要正则约束，但输入过程中仍要允许半成品文本。
- 用户按回车提交前，先尝试把 ` 123-456 `、本地化数字或轻微格式错误修正成可接受值。
- 校验规则依赖语言环境，例如小数点、千位分隔符、数字字符集随 `QLocale` 改变。

## 使用模型

校验器通常作为 `QObject` 放在使用它的控件同一线程，并通过 parent 交给控件或窗口管理生命周期。自定义校验器至少要实现 `validate(QString &input, int &pos) const`；如果能做温和修正，再重写 `fixup(QString &input) const`。

`validate()` 不是单纯的只读函数：签名允许它修改 `input` 和 `pos`。`pos` 是编辑光标位置，如果校验器删除、补全或重排了字符，就应同步更新光标位置，避免控件下一次编辑跳到错误位置。

校验规则变化时应发出 `changed()`。内置数值校验器在范围、精度等属性改变时会发出对应通知；自定义类如果有影响结果的属性，也应在 setter 中发出 `changed()`，让控件刷新 `acceptableInput` 等状态。

## 三态语义

`Invalid` 表示当前字符串明确不可能成为合法结果，例如整数输入框中出现字母。

`Intermediate` 表示它还不是最终结果，但像是编辑过程中的合理中间态。空字符串通常应视为 `Intermediate`，因为用户可能正在清空后重新输入；范围校验中超出位数或暂时小于下界的文本也常常是 `Intermediate`，取决于继续输入是否可能变成合法值。

`Acceptable` 表示字符串已经可以作为最终结果提交。按钮启用、回车提交、`QLineEdit::hasAcceptableInput()` 一类逻辑应以这个状态为准，而不是把 `Intermediate` 当成成功。

## 关键语义与边界

`fixup()` 是“尝试修正”，不是“保证修正”。调用者必须在 `fixup()` 后再次调用 `validate()`。默认实现什么都不做；派生类可以只做裁剪空白、删除无关字符、补全前缀这类低风险操作。

`locale()` 影响依赖本地化解析的派生类，尤其是 `QIntValidator` 与 `QDoubleValidator`。没有显式调用 `setLocale()` 时，校验器使用默认 `QLocale`；如果默认 locale 也未设置，则来自操作系统环境。

`QValidator` 是 `QObject`，不可拷贝。跨线程直接操作一个正在被 GUI 控件使用的校验器没有必要也容易出错；需要跨线程更新规则时，用 queued signal/slot 把变更投递回对象所属线程。

## 常见误区

- 把 `Intermediate` 当作失败。交互式输入中它通常是“继续让用户输入”的正常状态。
- 在 `fixup()` 后不复查。修正函数可能仍然留下无效文本。
- `validate()` 修改了字符串却不更新 `pos`，导致光标跳动或插入位置错乱。
- 自定义校验器有范围、模式等属性变化，却忘记发出 `changed()`。
- 用正则写成“必须完整匹配”后，把所有前缀都判成 `Invalid`，用户连合法内容也输不进去。

## API 速查表

| API | 作用 | 重点注意 |
| --- | --- | --- |
| `enum QValidator::State` | 描述校验结果的三态枚举。 | `Invalid` 是明确无效，`Intermediate` 是可继续编辑的中间态，`Acceptable` 才是可提交结果。 |
| `QValidator::Invalid` | 当前字符串按规则明确不可接受。 | 不要把所有未完成输入都归为此状态，否则控件会过早拒绝用户编辑。 |
| `QValidator::Intermediate` | 当前字符串尚非最终合法值，但可能通过继续编辑变合法。 | 空字符串、范围输入的前缀、轻微格式残缺常属于此类。 |
| `QValidator::Acceptable` | 当前字符串已经满足规则，可作为最终结果。 | 提交、启用确认按钮、响应回车通常应检查此状态。 |
| `[explicit] QValidator(QObject *parent = nullptr)` | 创建校验器，并把 parent 传给 `QObject`。 | 常把 parent 设为使用它的控件或窗口；对象不可拷贝。 |
| `[virtual noexcept] ~QValidator()` | 销毁校验器并释放内部资源。 | 控件不应继续持有已析构校验器；使用 parent 管理可减少悬空指针。 |
| `[signal] void changed()` | 通知外部：影响校验结果的属性已经改变。 | 自定义 setter 改变规则后应发出；让控件刷新可接受状态。 |
| `[virtual] void fixup(QString &input) const` | 尝试把输入修正得更接近可接受形式。 | 默认不做任何事；调用后必须再次 `validate()`，不能假设已经成功。 |
| `QLocale locale() const` | 返回校验器用于本地化解析的 locale。 | 未显式设置时使用默认 `QLocale`，再退到系统 locale。 |
| `void setLocale(const QLocale &locale)` | 设置校验器的本地化环境。 | 会影响数字、分隔符等解析规则；动态修改后注意 UI 状态刷新。 |
| `[pure virtual] State validate(QString &input, int &pos) const` | 按规则校验输入，并返回三态结果。 | 必须由派生类实现；允许修改 `input` 与光标位置 `pos`。 |

## 一句话总结

`QValidator` 的核心不是“合法/非法”二选一，而是给正在编辑的文本一套能保留用户输入路径的三态契约。
