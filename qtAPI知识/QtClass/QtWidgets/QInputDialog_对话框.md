# Qt QInputDialog 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）
> 头文件：`#include <QInputDialog>`
> 所属模块：`Qt6::Widgets`
> 继承：`QDialog -> QInputDialog`
> 常见搭档：`QLineEdit`、`QSpinBox`、`QDoubleSpinBox`、`QComboBox`

## 1. QInputDialog 解决什么问题

`QInputDialog` 用来向用户要一个简单值，而不是整张自定义表单。它适合这类需求：

- 输入一段文本；
- 输入整数或小数；
- 从列表里选一个项；
- 做一个轻量的即时输入框；
- 不想专门写一整个 `QDialog`。

它本质上是“单值输入器”，不是通用表单容器。  
如果你要收集很多字段，还是自己做对话框更清楚。

## 2. 最小可用代码

```cpp
#include <QApplication>
#include <QInputDialog>
#include <QPushButton>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QPushButton button("输入名字");
    QObject::connect(&button, &QPushButton::clicked, [&] {
        bool ok = false;
        QString text = QInputDialog::getText(
            &button, QObject::tr("用户名"), QObject::tr("请输入用户名："),
            QLineEdit::Normal, QString(), &ok);
        if (ok)
            qDebug() << text;
    });

    button.show();
    return app.exec();
}
```

## 3. 输入模式

```cpp
dialog.setInputMode(QInputDialog::TextInput);
dialog.setInputMode(QInputDialog::IntInput);
dialog.setInputMode(QInputDialog::DoubleInput);
```

三种模式分别对应：

- `TextInput`：文本；
- `IntInput`：整数；
- `DoubleInput`：浮点数。

模式切换后，内部控件和可用属性会跟着变，所以不要把它当成普通的状态位。

## 4. 三类常见输入

### 4.1 文本输入

```cpp
dialog.setLabelText(tr("请输入名称"));
dialog.setTextValue("Alice");
dialog.setTextEchoMode(QLineEdit::Normal);
```

如果是密码，就改成：

```cpp
dialog.setTextEchoMode(QLineEdit::Password);
```

还可以让文本输入变成多行：

```cpp
dialog.setOption(QInputDialog::UsePlainTextEditForTextInput, true);
```

### 4.2 整数输入

```cpp
dialog.setInputMode(QInputDialog::IntInput);
dialog.setIntRange(0, 100);
dialog.setIntStep(5);
dialog.setIntValue(20);
```

### 4.3 小数输入

```cpp
dialog.setInputMode(QInputDialog::DoubleInput);
dialog.setDoubleRange(0.0, 100.0);
dialog.setDoubleDecimals(2);
dialog.setDoubleStep(0.5);
dialog.setDoubleValue(12.5);
```

## 5. 列表选择和 live dialog

```cpp
dialog.setInputMode(QInputDialog::TextInput);
dialog.setComboBoxItems({"A", "B", "C"});
dialog.setComboBoxEditable(true);
```

如果你想让用户从候选项里挑，可以用 `getItem()` 或把输入模式切到文本并给 `comboBoxItems`。

`NoButtons` 是很实用的选项：

```cpp
dialog.setOption(QInputDialog::NoButtons, true);
```

它会把对话框变成“实时输入”模式，输入一变就可以即时响应，适合做过滤、搜索和即时预览。

## 6. 静态便捷函数

```cpp
QString text = QInputDialog::getText(...);
QString multi = QInputDialog::getMultiLineText(...);
QString item = QInputDialog::getItem(...);
int value = QInputDialog::getInt(...);
double number = QInputDialog::getDouble(...);
```

这几类函数是最常见的入口：

- `getText()`：单行文本；
- `getMultiLineText()`：多行文本；
- `getItem()`：从列表选一项；
- `getInt()`：整数；
- `getDouble()`：浮点数。

如果你只是要一个确认后的值，这些静态函数比手工创建对象更省事。

## 7. 结果和信号

`QInputDialog` 有一组“变化中”的信号和一组“最终选中”的信号：

- `textValueChanged()` / `textValueSelected()`
- `intValueChanged()` / `intValueSelected()`
- `doubleValueChanged()` / `doubleValueSelected()`

变化中信号适合 live 预览；选中信号适合最终提交。

`open(QObject *receiver, const char *member)` 则适合异步打开。用户点确认后，结果会通过对应的 selected 信号送出去。

## 8. 什么时候该用它

适合：

- 单值输入；
- 临时设置参数；
- 选一个简单候选项；
- 想要快速写一个交互很轻的对话框。

不适合：

- 多字段表单；
- 复杂校验流程；
- 多步骤输入。那是 `QWizard` 的地盘。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QInputDialog(QWidget *parent = nullptr, Qt::WindowFlags flags = {})` | 创建可配置的单值输入对话框。 | 先设 `inputMode`，再配置对应模式的属性。 |
| 析构 | `~QInputDialog()` | 销毁输入对话框。 | 一般交给父对象或局部对象管理。 |
| 模式 | `setInputMode(InputMode mode)` / `inputMode() const` | 选择文本、整数或小数输入模式。 | 切换模式会改变内部控件和有效属性。 |
| 文本 | `setLabelText(const QString &text)` / `labelText() const` | 设置或读取输入提示。 | 说明应直接告诉用户需要输入什么。 |
| 选项 | `setOption(InputDialogOption option, bool on = true)` / `testOption(...) const` | 开关单个输入选项。 | `NoButtons` 适合实时输入；纯文本编辑选项只对文本模式有意义。 |
| 选项 | `setOptions(InputDialogOptions options)` / `options() const` | 批量设置或读取选项集合。 | 初始化阶段设置更清楚。 |
| 文本值 | `setTextValue(const QString &text)` / `textValue() const` | 设置或读取当前文本。 | 只在 `TextInput` 模式下作为主要值使用。 |
| 文本回显 | `setTextEchoMode(QLineEdit::EchoMode mode)` / `textEchoMode() const` | 控制文本显示为普通、密码或其他回显方式。 | 密码输入不要把文本值写入日志。 |
| 候选项 | `setComboBoxEditable(bool editable)` / `isComboBoxEditable() const` | 控制候选项下拉框是否允许用户输入新值。 | 可编辑时要额外校验用户输入是否属于业务范围。 |
| 候选项 | `setComboBoxItems(const QStringList &items)` / `comboBoxItems() const` | 设置或读取文本模式下的候选列表。 | 适合少量选项；选项很多时应使用专用选择控件。 |
| 整数值 | `setIntValue(int value)` / `intValue() const` | 设置或读取当前整数。 | 值会被限制在当前整数范围内。 |
| 整数范围 | `setIntMinimum(int min)` / `intMinimum() const`、`setIntMaximum(int max)` / `intMaximum() const` | 分别设置或查询整数上下限。 | 上下限关系要保持有效。 |
| 整数范围 | `setIntRange(int min, int max)` | 一次设置整数上下限。 | 适合初始化配置，比分开调用更直观。 |
| 整数步进 | `setIntStep(int step)` / `intStep() const` | 设置或读取整数微调步长。 | 步长影响用户操作，不改变允许范围。 |
| 小数值 | `setDoubleValue(double value)` / `doubleValue() const` | 设置或读取当前浮点数。 | 会受范围和小数位数限制。 |
| 小数范围 | `setDoubleMinimum(double min)` / `doubleMinimum() const`、`setDoubleMaximum(double max)` / `doubleMaximum() const` | 分别设置或查询浮点上下限。 | 注意浮点边界和显示精度不是同一个概念。 |
| 小数范围 | `setDoubleRange(double min, double max)` | 一次设置浮点数范围。 | 初始化时优先使用。 |
| 小数精度 | `setDoubleDecimals(int decimals)` / `doubleDecimals() const` | 设置或读取显示的小数位数。 | 控制显示和输入精度，不是简单的字符串格式化。 |
| 小数步进 | `setDoubleStep(double step)` / `doubleStep() const` | 设置或读取浮点微调步长。 | 步长应与业务允许精度匹配。 |
| 按钮文字 | `setOkButtonText(const QString &text)` / `okButtonText() const` | 设置或读取确认按钮文字。 | “应用”“选择”“导入”等业务语义可比“确定”更清楚。 |
| 按钮文字 | `setCancelButtonText(const QString &text)` / `cancelButtonText() const` | 设置或读取取消按钮文字。 | 本地化和业务流程可自定义。 |
| 尺寸 | `sizeHint() const` / `minimumSizeHint() const` | 返回对话框推荐尺寸和最小尺寸。 | 一般交给布局系统。 |
| 显示 | `setVisible(bool visible)` | 控制对话框显示。 | 对象式用法可配合 `open()`，不要重复调用静态入口。 |
| 异步打开 | `open(QObject *receiver, const char *member)` | 非阻塞打开并把最终结果接到旧式槽。 | 根据输入模式连接对应的 selected 信号。 |
| 结果 | `done(int result)` | 处理对话框关闭和结果提交。 | 重写时正确区分 Accepted/Rejected。 |
| 信号 | `textValueChanged(const QString &text)` / `textValueSelected(const QString &text)` | 分别表示文本实时变化和最终确认。 | 前者适合预览/过滤，后者适合落地。 |
| 信号 | `intValueChanged(int value)` / `intValueSelected(int value)` | 分别表示整数实时变化和最终确认。 | 不要把 changed 当作用户已经提交。 |
| 信号 | `doubleValueChanged(double value)` / `doubleValueSelected(double value)` | 分别表示小数实时变化和最终确认。 | 业务提交通常接 selected。 |
| 静态入口 | `getText()` / `getMultiLineText()` / `getItem()` / `getInt()` / `getDouble()` | 一次性弹出对话框并返回一个值。 | 用 `ok` 指针区分确认和取消；复杂流程用对象式 API。 |

### 一句话总结

`QInputDialog` 就是“单值输入的快速方案”：模式选对了，按钮和返回值就简单；想要多字段或复杂校验，就别硬塞进它。
