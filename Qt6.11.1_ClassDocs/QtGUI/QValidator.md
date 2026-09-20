# QValidator

> Qt 6.11.1 · Qt GUI · 来自 `QValidator`

## 1. 先建立直觉

`QValidator` 是编辑过程中的输入规则接口。它不只回答“这个字符串最终对不对”，还要回答“用户还在输入时，这个半成品有没有可能变成正确结果”。

因此它有三个状态：

- `Acceptable`：当前文本已经是合法最终值。
- `Intermediate`：当前文本暂时不完整，但继续输入可能合法。
- `Invalid`：无论怎样继续输入都不符合规则，编辑控件通常应拒绝这次修改。

`Intermediate` 是校验器最重要的设计点。例如范围 10 到 99 时，用户刚输入 `"1"` 必须是 Intermediate，而不是 Invalid，否则他永远无法输入 `"10"`。

## 2. 类说明

`QValidator` 继承自 `QObject`，主要被 `QLineEdit` 等文本输入控件持有与调用。Qt 内置子类有 `QIntValidator`、`QDoubleValidator`、`QRegularExpressionValidator`，也可自行派生实现领域校验。

类说明只用于表明这些 API 来自 `QValidator`：控件如何展示错误、何时允许提交、是否在失焦时 fixup，是 UI/业务层的策略；validator 只给出文本状态和可选修正。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `enum State` | 定义 Invalid、Intermediate、Acceptable 三态。 |
| `QValidator(parent)` | 构造校验器并指定 QObject 父对象。 |
| `validate(input, pos)` | 纯虚函数，评估或修正当前文本及光标位置。 |
| `fixup(input)` | 尝试把输入修正为更合理的形式，默认不做事。 |
| `locale()` | 返回数字/本地化子类解析时使用的 locale。 |
| `setLocale(locale)` | 设置校验器 locale。 |
| `changed()` | 校验规则改变时发出，控件可重新评估现有输入。 |

## 4. 关键用法

### 让控件拥有 validator

```cpp
auto *validator = new QIntValidator(1, 65535, lineEdit);
lineEdit->setValidator(validator);
```

传入 `lineEdit` 作为 parent 可以让输入框销毁时自动销毁 validator。不要把栈对象 validator 传给长期存在的控件。

### 自定义校验器必须保留 Intermediate

```cpp
class PortValidator final : public QValidator
{
public:
    using QValidator::QValidator;

    State validate(QString &input, int &pos) const override
    {
        Q_UNUSED(pos);

        if (input.isEmpty())
            return Intermediate;

        bool ok = false;
        const int port = input.toInt(&ok);
        if (!ok || port < 0 || port > 65535)
            return Invalid;

        return port == 0 ? Intermediate : Acceptable;
    }
};
```

规则必须按“用户正在编辑”的实际过程设计，而不是只按表单提交时的完整值设计。

### `fixup()` 做温和规范化

```cpp
void HexValidator::fixup(QString &input) const
{
    input = input.trimmed().toUpper();
    if (!input.startsWith('#'))
        input.prepend('#');
}
```

`fixup()` 不能替代 `validate()`。修正后仍应能被重新验证，且不要在这里悄悄改变用户含义，例如把超范围金额直接截断却不给反馈。

### locale 影响数字子类

```cpp
validator->setLocale(QLocale(QLocale::German, QLocale::Germany));
```

对 `QIntValidator`、`QDoubleValidator`，小数点、分组分隔符、正负号等解析会受 locale 影响。不要用固定 `.` 假设所有用户输入都采用 C locale。

## 5. 使用场景

`QValidator` 适合端口号、ID、日期片段、颜色代码、坐标、账单金额、序列号、版本号、文件名规则、网络地址和自定义领域格式。

它适用于“限制编辑过程”，而不是最终业务验证的唯一防线。服务器范围、数据库唯一性、权限、跨字段关系、异步可用性检查仍应在提交阶段验证。

## 6. 常见坑与经验

不要把 Intermediate 显示为红色错误。它常意味着用户只输入了一半，过早报错会让输入体验非常差。

不要在 `validate()` 做数据库、网络或耗时正则工作。它可能每次按键触发，必须快速且无副作用。

不要让 `validate()` 随意重写 input。只有真正需要规范化输入时才修改文本和 `pos`，否则会造成光标跳动。

不要依赖 validator 自动阻止所有粘贴或程序设置文本的非法状态。提交时仍需调用业务校验。

不要跨线程共享同一个 validator。它是 QObject 且通常与 GUI 控件同线程使用。

## 7. 知识点覆盖

学习 `QValidator` 应覆盖三态输入校验、编辑中间态、`QLineEdit::setValidator()`、自定义派生、`fixup()`、光标位置、locale、QObject 所有权、输入体验和提交阶段二次验证。
