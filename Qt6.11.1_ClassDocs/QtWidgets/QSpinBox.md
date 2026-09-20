# QSpinBox

> Qt 6.11.1 · Qt Widgets · 来自 `QSpinBox`

## 1. 先建立直觉

### 这是什么

`QSpinBox` 是整数输入控件：用户既可以键入整数，也可以通过上下按钮、方向键或滚轮按步长增减。它继承 `QAbstractSpinBox` 的编辑器、验证、步进按钮和键盘跟踪机制，并把值类型固定为 `int`。

它适合输入有上下界、步长明确的整数。相比 `QLineEdit + QIntValidator`，`QSpinBox` 的优势是范围、步进、显示文本、特殊最小值语义和变化信号都已经整合好。

### 适合使用的场景

- 数量、次数、页码、端口、缩放百分比、延迟毫秒。
- 需要限制最小/最大值，并让用户用按钮逐步调整。
- 需要显示单位、货币符号、百分号等前后缀。
- 需要用最小值表达“自动”“无限制”等特殊选项。
- 需要以非十进制显示整数，例如十六进制。

### 不适合的场景

- 小数输入用 `QDoubleSpinBox`。
- 日期时间输入用 `QDateTimeEdit`。
- 范围很大且用户主要键入，不常步进时，`QLineEdit` 加 validator 可能更轻。
- 复杂枚举值可考虑 `QComboBox`；自定义文本枚举才考虑继承 spin box。

## 2. 依赖与对象关系

- 头文件：`#include <QSpinBox>`
- 模块：Qt Widgets
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QAbstractSpinBox`
- 直接派生类：类页未列出

`QSpinBox` 的输入框、按钮、滚轮、校正、键盘跟踪等行为来自 `QAbstractSpinBox`。它自己主要负责整数范围、步长、前缀后缀、进制显示，以及整数和文本之间的转换。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `value : int` | 当前整数值。 |
| `minimum : int` / `maximum : int` | 有效范围上下界。 |
| `singleStep : int` | 默认步进量。 |
| `stepType : StepType` | 固定步进或自适应十进制步进。 |
| `prefix : QString` / `suffix : QString` | 显示在数值前后的文本。 |
| `cleanText : QString` | 去掉前缀、后缀和空白后的显示文本。 |
| `displayIntegerBase : int` | 整数显示进制，默认 10。 |
| `QSpinBox(QWidget *parent)` | 创建默认范围 0 到 99、步长 1 的整数 spin box。 |
| `setRange(min, max)` | 一次设置最小值和最大值。 |
| `setValue(int)` | 设置当前值，变化时发出 `valueChanged(int)`。 |
| `valueChanged(int)` | 当前整数值变化时发出。 |
| `textChanged(QString)` | 显示文本变化时发出，包含前后缀。 |
| `textFromValue(int)` | 把整数值转换为显示文本，子类可重写。 |
| `valueFromText(QString)` | 把用户文本转换回整数，子类可重写。 |
| `validate(QString &, int &)` | 判断输入文本是否合法。 |
| `fixup(QString &)` | 结束编辑时尝试修正输入。 |
| `event(QEvent *)` | 处理特定事件入口。 |

## 4. API 逐项说明

### `value`

当前整数值。调用 `setValue()` 时，如果值超出范围，会被限制到有效范围内；如果新值不同，会发出 `valueChanged(int)` 和相关文本变化信号。

业务代码读取值时用 `value()`，不要解析 `text()`；`text()` 可能包含单位、前缀、分隔符或特殊文本。

### `minimum` / `maximum` / `setRange()`

范围决定用户能输入和步进到哪些值。单独设置最小值或最大值时，Qt 会必要时调整另一端，保证范围有效。`setRange()` 可一次设置两端，语义更清楚。

默认范围是 0 到 99。很多 bug 来自忘记设置范围，导致用户无法输入预期的大数或负数。

### `singleStep` / `stepType`

`singleStep` 是默认步长，通常为 1。`stepType` 可以切换为自适应十进制步进，让步长随当前数量级变化。

固定步长适合数量、页码；自适应步长适合跨度很大的数值调节。步长小于 0 无效。

### `prefix` / `suffix`

前缀和后缀只影响显示文本。货币符号常用 prefix，单位和百分号常用 suffix。设置了 `specialValueText` 且当前值等于最小值时，前后缀不会显示。

如果你连接 `textChanged(QString)`，收到的文本包含前后缀；连接 `valueChanged(int)` 才是纯数值。

### `cleanText`

返回去掉前缀、后缀和前后空白后的文本。它仍然是文本，不一定是最终业务值。

当你自定义显示文本时，`cleanText()` 可用于展示或调试，但值转换仍应走 `valueFromText()`。

### `displayIntegerBase`

控制整数显示进制，默认十进制。可用于十六进制地址、颜色分量、位掩码等场景。

更改进制只改变显示/解释方式，不改变 `value()` 的真实整数值。

### 构造和析构

构造函数创建范围 0 到 99、步长 1、初始值 0 的控件。析构通常由父控件负责。

创建后应尽快设置业务范围、单位和默认值，让控件从一开始就表达正确约束。

### `valueChanged(int)` / `textChanged(QString)`

`valueChanged(int)` 是业务上最常用的信号。`textChanged(QString)` 反映显示文本变化，包含 prefix/suffix/special text。

如果只关心数值，使用 `valueChanged(int)`；如果要同步界面显示字符串或日志展示，才考虑 `textChanged()`。

### `textFromValue(int)` / `valueFromText(QString)`

这两个虚函数成对定义显示和解析。默认实现使用 locale 把整数转字符串；重写后可以显示枚举名、带格式的编号、十六进制文本等。

只重写 `textFromValue()` 而不重写 `valueFromText()`，用户可能看得到文本却输不回去。

### `validate()` / `fixup()`

`validate()` 判断当前输入状态；`fixup()` 在编辑结束时尝试修正。自定义文本格式时通常也要重写它们。

不要在这里做数据库查询或网络检查，它们会在编辑过程中频繁触发。

## 5. 深入实践与常见坑

### 先设置范围再设置值

如果先 `setValue(1000)`，但范围仍是默认 0 到 99，值会被截到 99。初始化顺序应是 `setRange()`、`setSingleStep()`、`setValue()`。

### 单位显示用 suffix，不要拼进业务值

`setSuffix(" ms")` 比把 `"100 ms"` 塞进文本更稳。业务侧始终读取 `value()`。

### specialValueText 是显示约定

用最小值表示“自动”很方便，但最小值仍是真实 `int`。保存配置时要明确这个映射。

### 自定义格式要保证可逆

如果 `textFromValue(3)` 显示 `"High"`，就要让 `valueFromText("High")` 能回到 3，并让 `validate()` 接受它。
