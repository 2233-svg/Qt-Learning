# QRegularExpressionValidator

> Qt 6.11.1 · Qt GUI · 来自 `QRegularExpressionValidator`

## 1. 先建立直觉

`QRegularExpressionValidator` 用 `QRegularExpression` 限制输入文本格式。它适合固定格式编号、邀请码、十六进制颜色、短标签、简化用户名等“字符串形态”规则。

它不是一次提交时的普通正则判断。作为 validator，它还要区分 partial match：用户输入了前缀但还没完成时返回 `Intermediate`，完全符合时才返回 `Acceptable`，不可能继续合法时才返回 `Invalid`。

## 2. 类说明

`QRegularExpressionValidator` 继承自 `QValidator`，持有一个 `QRegularExpression` 属性。它会把正则作为整串约束使用，业务上应把模式写成对完整输入的规则，而不是假设它像搜索 API 一样只找子串。

类说明只用于表明这些 API 来自 `QRegularExpressionValidator`：正则语法和编译状态属于 `QRegularExpression`；字段之间的关系、数据库唯一性、权限和远程存在性检查不属于 validator 能力。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QRegularExpressionValidator(parent)` | 构造默认校验器；空 pattern 通常接受任意字符串。 |
| `QRegularExpressionValidator(re, parent)` | 构造使用指定正则表达式的校验器。 |
| `regularExpression() const` | 返回当前用于验证的正则。 |
| `setRegularExpression(re)` | 更新正则表达式，随后发出规则变化通知。 |
| `validate(input, pos)` | 根据完整匹配、部分匹配或失败返回三态。 |
| `regularExpressionChanged(re)` | 正则规则变化时发出。 |
| `fixup(input)` | 继承默认行为；复杂规范化需自行派生。 |

## 4. 关键用法

### 限制 ASCII 标识符

```cpp
QRegularExpression pattern(R"([A-Za-z][A-Za-z0-9_]{0,31})");
auto *validator = new QRegularExpressionValidator(pattern, ui->nameEdit);
ui->nameEdit->setValidator(validator);
```

用户刚输入 `"A"`、`"ab_"` 时可能都是 `Intermediate` 或 `Acceptable`，取决于模式最小长度。validator 会在完整和部分匹配之间自动区分。

### 明确表达完整格式

```cpp
QRegularExpression hexColor(R"(#[0-9A-Fa-f]{6})");
```

当规则表达的是完整值，模式本身应完整描述所有字符。不要把 `QRegularExpressionValidator` 当成“文本包含某段合法字符即可”的搜索器。

### 动态切换规则

```cpp
validator->setRegularExpression(
    advancedMode
        ? QRegularExpression(R"([A-Z]{3}-\d{4})")
        : QRegularExpression(R"(\d{4})"));
```

切换后应重新审视现有文本：它可能变为 Invalid，也可能只是 Intermediate。UI 需要决定显示提示、清空、保留等待用户修改，还是阻止提交。

### 正则有效性也要检查

```cpp
QRegularExpression pattern(userProvidedPattern);
if (!pattern.isValid()) {
    showPatternError(pattern.errorString());
    return;
}
validator->setRegularExpression(pattern);
```

正则来自配置或编辑器时，不能假设总是可编译。无效模式会让验证行为不可预期，也会影响用户输入。

## 5. 使用场景

`QRegularExpressionValidator` 适合邀请码、批次号、车牌简化格式、设备编号、十六进制颜色、固定长度 token、文件名片段、基础用户名和版本字符串。

它不适合邮箱地址、URL、密码安全策略、国际化姓名、日期合法性、复杂电话号码等需要语义、国际规则或用户友好修正的字段。此类场景常需要组合更高层校验与服务器验证。

## 6. 常见坑与经验

不要忘记它处理完整输入。模式写成 `\d+` 与用匹配 API 搜索数字子串是不同语义。

不要在每次按键执行灾难性回溯正则。validator 高频运行，模式应避免嵌套贪婪量词等高风险结构。

不要把空字符串自动当 Invalid。很多可选字段应允许空输入，或将空输入保留为 Intermediate，具体取决于提交规则。

不要只靠正则验证“邮箱地址”或“URL 完全正确”。正则能约束形态，但不验证域名存在、协议安全、业务权限等。

不要在 validator 中修改 input 实现复杂格式化。需要插入分隔符、自动大写、光标修正时，应谨慎自定义 `QValidator` 或在编辑事件中处理。

## 7. 知识点覆盖

学习 `QRegularExpressionValidator` 应覆盖完整匹配、部分匹配、三态输入、正则编译有效性、模式性能、固定格式字段、动态规则、`QLineEdit` 集成和正则与业务校验的边界。
