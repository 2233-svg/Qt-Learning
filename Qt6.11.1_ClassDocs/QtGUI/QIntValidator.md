# QIntValidator

> Qt 6.11.1 · Qt GUI · 来自 `QIntValidator`

## 1. 先建立直觉

`QIntValidator` 验证一个符合 locale 规则的有符号整数是否在指定闭区间内。它适合端口、页码、数量、优先级、年龄、帧号等文本输入。

它并不是简单的 `min <= toInt() <= max`。输入框要允许用户逐步编辑，因此某些当前越界的文本仍可能返回 `Intermediate`。例如范围 46 到 53，用户把 `"49"` 改成 `"51"` 时，短暂输入 `"59"` 需要保留为 Intermediate，否则编辑过程会被卡死。

## 2. 类说明

`QIntValidator` 继承自 `QValidator`，增加 `bottom` 和 `top` 两个范围属性。它使用自身 `locale()` 识别数字、符号与可能的分组分隔符。

类说明只用于表明这些 API 来自 `QIntValidator`：范围判断由本类负责，最终业务语义，例如库存是否仍足够、端口是否被占用，仍需要提交时额外验证。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QIntValidator(parent)` | 构造接受全部 `int` 范围的校验器。 |
| `QIntValidator(minimum, maximum, parent)` | 构造指定闭区间校验器。 |
| `bottom() const` / `top() const` | 查询最小值与最大值。 |
| `setBottom(value)` / `setTop(value)` | 单独更新范围端点。 |
| `setRange(bottom, top)` | 一次更新完整闭区间。 |
| `validate(input, pos)` | 评估当前输入为 Invalid、Intermediate 或 Acceptable。 |
| `fixup(input)` | 继承重实现，尝试规范化输入。 |
| `bottomChanged()` / `topChanged()` | 范围端点变化时发出。 |
| `setLocale()` | 来自父类，设置数字解析 locale。 |

## 4. 关键用法

### 给输入框限制端口范围

```cpp
auto *portValidator = new QIntValidator(1, 65535, ui->portEdit);
portValidator->setLocale(QLocale::c());
ui->portEdit->setValidator(portValidator);
```

网络端口通常要求 ASCII 数字与固定格式，使用 `QLocale::c()` 能避免界面 locale 的分组符号或本地数字格式带来歧义。

### 理解 Intermediate 是正常编辑状态

```cpp
QIntValidator validator(10, 99);
int pos = 0;
QString text = "1";

Q_ASSERT(validator.validate(text, pos) == QValidator::Intermediate);
```

`"1"` 不是最终合法值，却是 `"10"` 到 `"19"` 的前缀。不要把这类文本立即清空或提示为错误。

### 范围变化后 UI 要重新解释当前值

```cpp
connect(spinRangeController, &RangeController::maximumChanged,
        this, [validator](int max) {
            validator->setTop(max);
        });
```

validator 发出 `changed()` / `topChanged()` 后，编辑控件可重新评估当前文本。业务层仍应决定如果已有值落在新范围外，是否自动修正、标红或阻止保存。

## 5. 使用场景

`QIntValidator` 适合端口、页码、数量、百分比整数、年龄、重试次数、帧号、优先级、RGB 8-bit 通道和整数型配置字段。

需要带单位、进制前缀、千位分隔格式或超出 `int` 的数字时，往往应自定义 `QValidator`，或使用更贴近数据模型的 `QSpinBox` / `QAbstractSpinBox`。

## 6. 常见坑与经验

不要把 validator 当作数值转换。提交时仍使用 `QLocale::toInt()` 并检查 `ok`，不要直接 `QString::toInt()` 假设格式一致。

不要期待范围外输入必然是 Invalid。为保持可编辑性，部分越界值可能是 Intermediate。

不要允许 locale 分组符后又用 `QString::toInt()` 解析。两套规则不同会造成“输入框显示合法但提交失败”。

不要用 `QIntValidator` 校验无符号 64-bit、十六进制或固定长度编码；这些需求使用自定义规则更准确。

不要反复新建 validator。输入规则不变时让控件长期持有同一个对象即可。

## 7. 知识点覆盖

学习 `QIntValidator` 应覆盖整数闭区间、Intermediate、locale 数字解析、分组分隔符、`QLineEdit`、范围动态更新、提交时转换、QSpinBox 选择和领域数值校验。
