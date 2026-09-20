# QDoubleValidator

> Qt 6.11.1 · Qt GUI · 来自 `QDoubleValidator`

## 1. 先建立直觉

`QDoubleValidator` 验证浮点数字符串是否在指定范围内、是否满足小数位数限制，以及是否允许科学计数法。它面向“用户输入的文本”，所以处理的是 locale、小数点、分组符、正负号、指数符号和不完整编辑状态，而不只是 C++ `double` 值。

最容易忽略的是默认 notation：`QDoubleValidator` 默认允许 `ScientificNotation`。如果你的金额、尺寸、百分比输入不应接受 `1e6`，必须显式设置为 `StandardNotation`。

## 2. 类说明

`QDoubleValidator` 继承自 `QValidator`，增加最小值、最大值、小数位数和记数法属性。它依据 `locale()` 解析文本，因此小数点不一定是 `.`，分组符是否允许也由 locale number options 决定。

类说明只用于表明这些 API 来自 `QDoubleValidator`：它保证文本形态和数值范围，金额精度、舍入规则、NaN/Infinity 业务语义、单位换算和数据库精度仍需提交层验证。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `enum Notation` | 选择 `StandardNotation` 或 `ScientificNotation`。 |
| `QDoubleValidator(parent)` | 构造不限范围、任意小数位的校验器。 |
| `QDoubleValidator(min, max, decimals, parent)` | 构造指定范围和小数位上限的校验器。 |
| `bottom()` / `top()` | 查询最小值与最大值。 |
| `setBottom()` / `setTop()` | 单独修改数值范围端点。 |
| `setRange(min, max, decimals)` | 同时设置范围和小数位上限。 |
| `setRange(min, max)` | 设置范围，保留现有小数位上限。 |
| `decimals()` / `setDecimals()` | 查询或设置小数部分最大位数；`-1` 表示不限。 |
| `notation()` / `setNotation()` | 查询或设置标准/科学记数法。 |
| `validate(input, pos)` | 返回输入三态。 |
| `fixup(input)` | 按 locale、notation 与 decimals 规范化浮点文本。 |
| `bottomChanged()` / `topChanged()` / `decimalsChanged()` / `notationChanged()` | 配置改变通知。 |
| `setLocale()` | 来自父类，设置解析的 locale。 |

## 4. 关键用法

### 金额或尺寸输入禁用科学记数法

```cpp
auto *validator = new QDoubleValidator(0.0, 100000.0, 2, ui->priceEdit);
validator->setNotation(QDoubleValidator::StandardNotation);
validator->setLocale(QLocale::system());
ui->priceEdit->setValidator(validator);
```

否则默认科学记数法可能接受 `"1e3"`。对科研或工程输入这很有用，对普通金额字段通常不符合用户预期。

### locale 决定小数点

```cpp
validator->setLocale(QLocale(QLocale::German, QLocale::Germany));
```

在某些 locale 中，逗号是小数点，点是分组符。提交时也应使用同一个 locale 解析：

```cpp
bool ok = false;
const double amount = validator->locale().toDouble(ui->priceEdit->text(), &ok);
```

不要校验按德语规则、提交却用 `QString::toDouble()` 按 C 规则解析。

### `fixup()` 用于失焦规范化

```cpp
connect(ui->priceEdit, &QLineEdit::editingFinished, this, [validator] {
    QString text = ui->priceEdit->text();
    validator->fixup(text);
    ui->priceEdit->setText(text);
});
```

`fixup()` 可归一化科学计数法或按小数位数舍入文本。调用后仍要确认结果 `Acceptable`，并慎重决定是否自动覆盖用户输入。

### 科学计数法下超范围可能仍是 Intermediate

例如允许科学计数法时，当前 `"999"` 可能通过添加 `e-2` 变为合法值，因此不应按普通十进制直觉判断它一定是 Invalid。这个差异正是 `notation()` 会改变交互体验的原因。

## 5. 使用场景

`QDoubleValidator` 适合价格、距离、比例、坐标、温度、速度、容差、缩放比例、工程参数、科学测量值和百分比。

金额等精确小数业务通常应考虑整数最小货币单位或十进制库。`double` 与二进制浮点误差不适合直接承担严格财务计算，validator 只能限制输入文本，不能解决精度模型问题。

## 6. 常见坑与经验

不要忘记显式设置 notation。默认科学记数法常常出乎普通表单的预期。

不要把 `decimals` 当作存储精度保证。它只限制文本小数位，后续转换为 `double` 仍有浮点表示误差。

不要用 C locale 解析本地化输入。校验和转换必须共享同一 `QLocale`。

不要忽略 `Intermediate`。`"-"`、`"1."`、`"1e"` 等在编辑过程中可能是合理中间状态。

不要把 `fixup()` 作为强制截断工具。对用户输入自动舍入金额、比例等内容应有清晰产品规则。

不要用它校验带单位的字符串，例如 `"12 px"` 或 `"3.5 kg"`。可以拆分数值和单位，或写自定义 validator。

## 7. 知识点覆盖

学习 `QDoubleValidator` 应覆盖浮点范围、小数位、标准与科学记数法、locale 小数点、分组符、Intermediate、`fixup()`、文本到 double 转换、金额精度边界和工程参数输入。
