# Qt QDoubleValidator 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDoubleValidator>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QValidator -> QDoubleValidator`  
> 定位：浮点文本输入的范围、精度、记法与 locale 校验器

## 1. 它解决什么问题

`QDoubleValidator` 用于限制用户在文本控件中输入一个可解析的浮点数。它可同时约束：

- 最小值 `bottom`；
- 最大值 `top`；
- 小数点后的最大位数 `decimals`；
- 标准记法或科学记数法 `notation`；
- 数字、符号、小数点、分组符和指数符的 locale 规则。

它解决的是**编辑过程中的文本可接受性**，不是数据模型的最终业务校验。用户正在输入 `-`、`1.` 或 `1e` 时，文本可能暂时无法转换成最终 `double`，但仍应允许继续编辑。因此 `QDoubleValidator` 使用 `Acceptable`、`Intermediate`、`Invalid` 三态，而不是简单的 true/false。

常见场景：

1. `QLineEdit` 输入温度、坐标、比例、价格或阈值；
2. 属性面板编辑数值时限制单位范围和显示精度；
3. 导入向导中根据用户 locale 接受 `1,25` 或阿拉伯数字；
4. 允许科学计数法的工程/科研参数输入；
5. 在编辑完成时通过 `fixup()` 规范化文本。

## 2. 构建与生命周期

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Gui Qt6::Widgets)
```

```cpp
#include <QDoubleValidator>
#include <QLineEdit>
#include <QLocale>
```

`QDoubleValidator` 继承 `QObject`，不可复制。给 `QLineEdit` 设置 validator 时，确保 validator 的生命周期长于输入框；常见做法是将 line edit 作为 parent：

```cpp
auto *validator = new QDoubleValidator(0.0, 100.0, 2, lineEdit);
lineEdit->setValidator(validator);
```

不要把栈上的 validator 传给一个会在其之后继续存在的 `QLineEdit`：

```cpp
void configure(QLineEdit *lineEdit)
{
    QDoubleValidator validator(0.0, 100.0, 2);
    lineEdit->setValidator(&validator); // 函数返回后成为悬空指针。
}
```

## 3. 最小可用代码

```cpp
#include <QDoubleValidator>
#include <QLineEdit>
#include <QLocale>

void configureAmountEditor(QLineEdit *edit)
{
    auto *validator = new QDoubleValidator(0.0, 9999.99, 2, edit);
    validator->setNotation(QDoubleValidator::StandardNotation);
    validator->setLocale(QLocale::system());

    edit->setValidator(validator);
}
```

编辑提交时，不要用与 validator 不同的规则解析：

```cpp
const QLocale locale = validator->locale();
bool ok = false;
const double value = locale.toDouble(edit->text(), &ok);
```

若 validator 使用德语 locale，`"1,25"` 可以是合法输入；用 `QString::toDouble()` 或 `QLocale::C` 解析它就可能失败或解释错误。

## 4. 三态校验模型

### 4.1 `Acceptable`

文本格式正确、可解析为 `double`、位于闭区间 `[bottom, top]`，且小数位数不超过 `decimals` 时返回 `Acceptable`。

这是通常允许提交或保存的状态，但业务层仍可能需要额外规则，例如值不能为零、必须是某个步长的倍数、不能是 NaN，或必须与其他字段保持关系。

### 4.2 `Intermediate`

`Intermediate` 表示“当前不能提交，但继续输入仍可能变为合法”。它是用户输入体验的一部分，不等价于错误。

常见情况：

- 输入还只是 `-`、小数点或未完成的指数；
- 数字格式暂不完整；
- 数值暂时超出范围，但用户仍可能通过补充指数或其它数字使其进入范围；
- 使用科学记数法时，尾数或指数还在编辑。

例如科学记数法输入值暂时不在范围内时，Qt 返回 `Intermediate`，因为用户可能通过修改指数让它变为有效。

### 4.3 `Invalid`

无法表示 `double`、小数位数过多，或已不可能通过继续输入变为合法时返回 `Invalid`。例如只允许非负区间 `[0, 100]` 时，负数输入被视为 `Invalid`，而不是可继续的中间状态。

`QLineEdit` 会据此拒绝用户的编辑操作。自定义控件直接调用 `validate()` 时，应区分 `Intermediate` 和 `Invalid`，不要把二者都显示为“格式错误”。

## 5. 范围、精度与记法

### 5.1 范围是闭区间

构造函数和 `setRange()` 都接受最小值与最大值，边界值本身有效：

```cpp
QDoubleValidator validator(-10.0, 10.0, 3);
```

`-10.0` 与 `10.0` 都可接受。默认构造时：

- `bottom` 默认为负无穷；
- `top` 默认为正无穷；
- 因而默认范围允许任意可接受的 `double`。

设置 `bottom` 大于 `top` 没有实际业务意义，应在应用层保证范围顺序正确，而不要依赖验证器替你修复配置错误。

### 5.2 `decimals` 限制的是小数点后的位数

`decimals` 的默认值是 `-1`，表示不限制小数点后的位数。非负值表示最多允许多少位小数：

```cpp
validator.setDecimals(2);
```

它不是有效数字总数，也不是显示格式设置。`123456.78` 仍可能合法，只要范围允许；而 `1.234` 在 `decimals == 2` 时会被拒绝。

设置为 `-1` 相当于无限制。若小数位超过 `double` 的可靠十进制精度，`fixup()` 输出可能改变额外的尾数，但仍应编码为解析后相同的浮点值。

### 5.3 `Notation`

| 枚举值 | 允许格式 | 适用场景 |
| --- | --- | --- |
| `StandardNotation` | 整数部分，可选小数部分，例如 `0.015`。 | 常规表单、价格、尺寸、百分比。 |
| `ScientificNotation` | 标准格式后可带指数，例如 `1.5E-2`。 | 科学、工程与跨度很大的数值。 |

默认值是 `ScientificNotation`。如果产品只希望用户看到普通十进制，务必显式调用：

```cpp
validator.setNotation(QDoubleValidator::StandardNotation);
```

不要把 `StandardNotation` 理解为“禁止所有符号”。正负号、小数点、指数符号、分组符和数字字符是否被接受，仍受 locale 规则影响。

## 6. Locale 是输入契约的一部分

`QDoubleValidator` 使用 `QValidator::locale()` 解释输入。不同 locale 的小数点、指数标记、负号、数字字符和分组符可能不同：

- 德语 locale 中 `"1,234"` 可以表示 `1.234`；
- 阿拉伯 locale 可以接受阿拉伯数字；
- 分组分隔符默认通常被接受；
- `"C"` locale 默认拒绝分组分隔符。

Qt 不检查分组分隔符位置是否完全符合书写规范；若 locale 的 `numberOptions()` 未启用 `QLocale::RejectGroupSeparator`，出现的分组符可能被接受。对财务、配置文件或机器可读输入，若不希望接受分组符，应明确配置 locale：

```cpp
QLocale locale = QLocale::c();
locale.setNumberOptions(locale.numberOptions()
                        | QLocale::RejectGroupSeparator);
validator.setLocale(locale);
```

输入校验、`fixup()` 和最终 `toDouble()` 必须使用同一个 `QLocale`，否则“能输入却无法解析”或“显示格式变化”的问题很常见。

## 7. `fixup()` 不是范围裁剪

Qt 6.3 起，`QDoubleValidator::fixup(QString &)` 会尝试把输入规范为可接受的 `double` 表示。它依据：

- `notation()`；
- `decimals()`；
- `locale()`；
- locale 的 `numberOptions()`。

示例：

```cpp
QString input = "0.98765e2";
QDoubleValidator validator;
validator.setLocale(QLocale::c());
validator.setNotation(QDoubleValidator::ScientificNotation);
validator.fixup(input);
// input 为 "9.8765e+01"
```

科学记数法会被规范到非零数在小数点前只有一个非零数字的形式。`decimals` 非负时，超出的有效小数部分会进行适当舍入：

```cpp
QString input = "-1234.6789";
QDoubleValidator validator;
validator.setDecimals(2);
validator.setLocale(QLocale::c());
validator.setNotation(QDoubleValidator::StandardNotation);
validator.fixup(input);
// input 为 "-1234.68"
```

`fixup()` 的目的不是把 `1000` 强行夹到最大值 `100`，也不应被当作无提示的数据修正机制。用户提交前仍应检查最终状态，并决定范围外内容是提示、拒绝还是采用业务定义的裁剪规则。

## 8. 与 `QLineEdit` 的交互

`QLineEdit` 在编辑过程中调用 validator 的 `validate()`，必要时在编辑结束路径调用 `fixup()`。这意味着：

- 输入时可能存在 `Intermediate` 文本；
- 不能只在 `textChanged` 中假设每个文本都可 `toDouble()`；
- `editingFinished()` 不应替代最终状态检查；
- locale 或范围运行时变化后，已有文本可能变为不再可接受。

如果要在 UI 中显示即时状态，可以在 `textChanged` 中复制字符串和光标位置后调用：

```cpp
QString input = edit->text();
int pos = edit->cursorPosition();
const auto state = validator->validate(input, pos);
```

`validate()` 的 `pos` 参数按 Qt 文档默认不被 `QDoubleValidator` 使用，但仍应传入有效变量；自定义派生 validator 可能使用它。

## 9. 属性变更与线程

`bottom`、`top`、`decimals`、`notation` 是可写属性，分别有对应的变更信号：

- `bottomChanged(double)`；
- `topChanged(double)`；
- `decimalsChanged(int)`；
- `notationChanged(QDoubleValidator::Notation)`。

它们适合在属性面板、数据绑定或配置变化后同步显示。`QValidator` 是 `QObject`，通常应在其所属线程中配置并与同线程的 `QLineEdit` 一起使用。不要从工作线程直接修改一个正在 GUI 线程验证输入的对象；需要跨线程更新配置时，使用 queued signal/slot 或在 GUI 线程创建新 validator 后替换。

## 10. 常见误区与排查顺序

### 10.1 用 `QString::toDouble()` 解析 validator 接受的文本

先检查 validator locale。应使用 `validator->locale().toDouble()`，尤其在小数逗号、非拉丁数字和分组符场景。

### 10.2 把范围外状态当作绝对错误

范围外输入经常是 `Intermediate`，让用户还有机会继续输入。UI 应区分“尚未完成”和“无法成为合法数字”。

### 10.3 忘记默认允许科学记数法

若字段不应接受 `1e6`，显式设为 `StandardNotation`；不要仅凭 placeholder 或提示文字假定输入会被拒绝。

### 10.4 以为 `decimals` 决定显示位数

它只限制可输入的小数位数，不会自动把文本显示成固定 `N` 位。需要格式化显示时使用 `QLocale::toString()` 或业务自己的格式规则。

### 10.5 在错误路径遗漏 validator 生命周期

`QLineEdit` 持有 validator 指针以供后续调用。让 validator 成为 line edit 的子对象，或由更长寿命的对象持有它。

### 10.6 将 `fixup()` 当成无声纠错

`fixup()` 会改变字符串表示，并可能舍入小数。对金额、科学数据或审计值，应先明确舍入规则和用户确认流程。

## 11. 与相关类型的协作

- `QValidator`：三态 `State`、`locale()`、`fixup()` 和共用生命周期接口。
- `QLineEdit`：最常见的 validator 使用者。
- `QLocale`：定义数字输入和解析规则。
- `QIntValidator`：整数范围输入。
- `QRegularExpressionValidator`：自定义文本格式。
- `QDoubleSpinBox`：需要步进按钮、显示格式和数值模型的场景通常比 `QLineEdit + QDoubleValidator` 更适合。

## 12. 逐项 API 说明

### 构造函数

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `explicit QDoubleValidator(QObject *parent = nullptr)` | 创建接受任意浮点范围的 validator。 | 默认范围为负无穷到正无穷，默认 `decimals == -1`，默认允许科学记数法。 |
| `QDoubleValidator(double bottom, double top, int decimals, QObject *parent = nullptr)` | 创建指定闭区间和小数位上限的 validator。 | `bottom`、`top` 都包含在有效范围；`decimals == -1` 表示不限制。 |
| `virtual ~QDoubleValidator() noexcept` | 销毁 validator。 | 与使用它的文本控件保持正确生命周期顺序。 |

### 属性与设置函数

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `double bottom() const` / `setBottom(double)` | 获取或设置最小可接受值。 | 默认负无穷；变更会发出 `bottomChanged`。 |
| `double top() const` / `setTop(double)` | 获取或设置最大可接受值。 | 默认正无穷；变更会发出 `topChanged`。 |
| `int decimals() const` / `setDecimals(int)` | 获取或设置最多小数位数。 | `-1` 表示无限制，不是零位小数。 |
| `Notation notation() const` / `setNotation(Notation)` | 获取或设置允许的数字记法。 | 默认是 `ScientificNotation`。 |
| `void setRange(double minimum, double maximum, int decimals)` | 一次设置范围和小数位。 | 范围为闭区间；`-1` 不限制小数位。 |
| `void setRange(double minimum, double maximum)` | 一次设置范围而保留现有小数位限制。 | 不会修改 `decimals()`。 |

### 校验与修复

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `State validate(QString &input, int &pos) const` | 返回 `Acceptable`、`Intermediate` 或 `Invalid`。 | `Intermediate` 是可继续编辑状态；解析使用 validator locale。 |
| `void fixup(QString &input) const` | 尝试规范化输入为可接受表示。 | Qt 6.3 起；会按 locale、记法和小数位舍入/规范化，不能替代业务确认。 |

### 信号

| 信号 | 何时发出 | 用途 |
| --- | --- | --- |
| `bottomChanged(double)` | 最小值变化时。 | 同步范围显示或业务配置。 |
| `topChanged(double)` | 最大值变化时。 | 同步范围显示或业务配置。 |
| `decimalsChanged(int)` | 小数位上限变化时。 | 更新格式提示或配置面板。 |
| `notationChanged(Notation)` | 记法变化时。 | 同步输入模式。 |

## API 速查表

| 类别 | API | 解决什么问题 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDoubleValidator(parent)` | 创建默认浮点校验器。 | 默认范围无限、精度无限、允许科学计数法。 |
| 构造 | `QDoubleValidator(bottom, top, decimals, parent)` | 同时设定范围与精度。 | 边界包含；`decimals == -1` 不限制。 |
| 配置 | `setBottom()` / `setTop()` / `setRange()` | 限制数值闭区间。 | 外部业务保证最小值不大于最大值。 |
| 配置 | `setDecimals()` | 限制小数点后的位数。 | 不决定显示格式。 |
| 配置 | `setNotation()` | 选择标准或科学记数法。 | 默认科学记数法；普通表单常需显式设标准记法。 |
| 校验 | `validate()` | 在编辑过程区分可提交、可继续、无效。 | 不要把 `Intermediate` 误当作错误。 |
| 修复 | `fixup()` | 规范化字符串表示。 | Qt 6.3 起；可能舍入，不能替代范围裁剪策略。 |
| Locale | `setLocale()` / `locale()` | 定义数字、分组符、小数点与解析规则。 | 用相同 locale 调用 `toDouble()`。 |
| 观察 | `bottomChanged` 等信号 | 监听校验规则变更。 | 在对象所属线程中修改与使用。 |

---

### 一句话总结

`QDoubleValidator` 管理的是“用户正在输入的浮点文本”；正确使用它要接受三态结果，显式选择记法和 locale，并用同一 locale 完成最终解析。
