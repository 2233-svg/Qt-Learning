# QIntValidator：面向编辑过程的本地化整数范围校验

> Qt 版本：6.11.1  
> 模块：`Qt6::Gui`  
> 头文件：`#include <QIntValidator>`  
> 继承：`QValidator`

## 它解决什么问题

`QIntValidator` 判断一个正在编辑的字符串能否成为指定闭区间内的整数。它服务于 `QLineEdit` 一类逐字符编辑控件，因此结果不是简单的“能解析/不能解析”，而是 `QValidator` 的三态：

- `Acceptable`：当前字符串已是范围内的完整整数。
- `Intermediate`：当前字符串还不合格，但用户继续编辑后仍可能变成合法整数。
- `Invalid`：当前字符串不可能通过合理继续编辑变为合法整数。

这意味着它不是提交时的业务规则引擎。输入框在编辑中应允许 `Intermediate`，表单提交、配置保存或数值计算前则必须要求 `Acceptable` 并完成 locale 一致的解析。

## 实际使用场景

- 端口、帧率、重试次数、页码、年龄、缩放百分比等整数范围输入。
- 设置面板中让用户逐字输入数字而不会因半成品立刻被拒绝。
- 支持阿拉伯数字、本地分组分隔符等 `QLocale` 数字表示。
- 将范围改变同步到多个编辑控件或 QML/属性绑定。
- 对提交的文本进行一次与编辑器相同规则的最终校验。

## 最常见用法

将 validator 设为编辑控件子对象，控件销毁时会一并释放它：

```cpp
auto *validator = new QIntValidator(1, 65535, lineEdit);
lineEdit->setValidator(validator);
```

范围两端都包含。默认构造的范围是整个 `int` 域，即从 `INT_MIN` 到 `INT_MAX`，并不等于“只允许正整数”。

提交时不要仅用 `QString::toInt()`，因为 validator 按自身 `locale()` 解释数字；默认 locale 通常接受 group separator，某些 locale 也接受非拉丁数字。

```cpp
QString text = lineEdit->text();
int pos = 0;

if (validator->validate(text, pos) != QValidator::Acceptable) {
    showRangeError();
    return;
}

bool ok = false;
const int value = validator->locale().toInt(text, &ok);
if (!ok) {
    showFormatError();
    return;
}

applyPort(value);
```

## 为什么范围外也可能是 Intermediate

对编辑器而言，“现在不在范围内”不一定意味着“用户不能继续修改成合法值”。例如范围为 `100` 到 `900`：

| 输入 | 状态 | 原因 |
| --- | --- | --- |
| `"1"` | `Intermediate` | 可以继续输入为 `100` 等合法数。 |
| `"012"` | `Intermediate` | 前导零的半成品仍可能通过继续编辑变成合法数。 |
| `"123"` | `Acceptable` | 已在闭区间内。 |
| `"999"` | `Intermediate` | 位数不超过最大值位数，用户可修改中间位而非只在末尾追加。 |
| `"1234"` | `Invalid` | 位数已超出能编辑为该范围值的合理界限。 |
| `"-123"` | `Invalid` | 当范围只含正数时，负整数不能成为合法输入。 |

类似地，范围为 `46` 到 `53` 时，`"41"` 和 `"59"` 可以是 `Intermediate`，否则用户难以在光标位于中间时把 `"49"` 修改为 `"51"`。

当范围只含负数时，没有前导 `+` 的正数可以暂时是 `Intermediate`，因为用户可能正要补输入负号，尤其在从右到左语言环境中。不要把三态误简化为“数值 < bottom 就 Invalid，数值 > top 就 Invalid”。

## locale 是校验契约的一部分

`QIntValidator` 使用从 `QValidator` 继承的 `locale()` 解释文本：

- 阿拉伯 locale 可以接受阿拉伯数字。
- 默认 `QLocale::NumberOptions` 通常未启用 `RejectGroupSeparator`，因此诸如千位分隔符可能被接受。
- 同一字符串在不同 locale 下可能具有不同的合法性或数值。

若产品协议要求机器可移植的 ASCII 数字，例如网络端口、命令行参数或配置文件，显式给 validator 设置固定 locale，并在最终解析时使用同一个 locale。若希望拒绝分组分隔符，修改该 locale 的 `NumberOptions` 后再 `setLocale()`，不要只在提交时做额外字符串替换。

## 范围、属性与动态更新

`bottom` 和 `top` 是可读写属性。`setRange(bottom, top)` 一次性定义闭区间；`setBottom()`、`setTop()` 适合单侧联动。范围变动后，输入框当前文本不会自动变成合法值，应用可重新校验并给出反馈。

```cpp
connect(modeCombo, &QComboBox::currentIndexChanged, this,
        [validator](int mode) {
            validator->setRange(mode == Advanced ? -9999 : 0,
                                mode == Advanced ? 9999 : 999);
        });
```

监听 `bottomChanged(int)`、`topChanged(int)` 可让外部 UI 更新提示文本或步进控件边界。不要同时在这些信号的槽中无条件反向设置 range，否则容易制造重复更新或循环。

## validate() 与 fixup() 的职责

`validate(QString &input, int &pos)` 是核心判断。此 validator 默认不使用 `pos`，但仍必须按签名传入，因为 `QValidator` 的其他实现可能依赖光标位置。

`fixup(QString &input)` 是失去编辑焦点等时机允许控件修复文本的扩展点。`QIntValidator` 提供该 override，但业务代码不应假定它会替你把任意非法值自动夹到范围内或弹出错误提示。需要“离焦自动补默认值/截断/夹取”的产品规则时，显式实现该行为，或派生自己的 validator 并配套测试。

## 常见错误

- 把 `Intermediate` 当作错误，导致用户无法逐步输入合法值。
- 只把 validator 绑定到输入框，提交时却不再检查 `Acceptable`。
- 使用 `QString::toInt()` 解析由本地化 validator 接受的文本。
- 假设默认范围只允许正数。
- 手动正则限制 ASCII 数字，又期望 validator 按 locale 接受本地数字。
- 用 `value < bottom` / `value > top` 推导三态，破坏中间编辑语义。
- 依赖 `fixup()` 自动纠正所有非法值，却没有验证实际行为。
- 改变范围后不重新检查当前输入。
- 用 `QIntValidator` 校验超出 `int` 表示范围的业务 ID 或 64 位金额。

## API 速查表

| 类别 | API | 语义与边界 |
| --- | --- | --- |
| 构造 | `explicit QIntValidator(QObject *parent = nullptr)` | 构造接受整个 `int` 范围的 validator。 |
| 构造 | `QIntValidator(int minimum, int maximum, QObject *parent = nullptr)` | 构造接受闭区间 `[minimum, maximum]` 的 validator。 |
| 析构 | `virtual ~QIntValidator()` | 销毁 validator；通常交给 parent 编辑控件管理。 |
| 属性 | `bottom()` / `setBottom(int)` | 读取/设置最小可接受整数。默认是 `INT_MIN`。 |
| 属性 | `top()` / `setTop(int)` | 读取/设置最大可接受整数。默认是 `INT_MAX`。 |
| 范围 | `setRange(int bottom, int top)` | 一次设置包含两端的合法范围。 |
| 验证 | `validate(QString &input, int &pos) const` | 返回 `Acceptable`、`Intermediate` 或 `Invalid`；本类默认不使用 `pos`。 |
| 修复 | `fixup(QString &input) const` | 由编辑框在适当时机调用的修复接口；不要假定会自动夹取到业务范围。 |
| 信号 | `bottomChanged(int)` | 最小值属性变化时发出。 |
| 信号 | `topChanged(int)` | 最大值属性变化时发出。 |
| 继承 | `locale()` / `setLocale(QLocale)` | 从 `QValidator` 继承；控制数字字符与分隔符解释，解析时应使用同一 locale。 |
| 继承 | `changed()` | 从 `QValidator` 继承的通用变化通知；通常优先在明确需要时监听范围属性信号。 |

## 相关类

- `QValidator`：三态验证、locale 与 `changed()` 信号的基类。
- `QDoubleValidator`：有小数位与科学计数法需求时使用。
- `QRegularExpressionValidator`：格式规则优先于数值范围时使用。
- `QLineEdit`：最常见的 validator 使用者。
- `QLocale`：解释本地数字与 group separator，并负责最终 `toInt()`。

`QIntValidator` 的核心价值是允许用户完成一次编辑，而不是在每个字符上苛刻地判错。让编辑阶段尊重 `Intermediate`，让提交阶段要求 `Acceptable` 并按相同 locale 解析，整数输入才能既顺手又可靠。
