# QDoubleSpinBox

> Qt 6.11.1 · Qt Widgets · 来自 `QDoubleSpinBox`

## 1. 先建立直觉

### 这是什么

`QDoubleSpinBox` 是浮点数输入控件。它和 `QSpinBox` 一样提供范围、步进、前缀后缀、特殊最小值文本和变化信号，但值类型是 `double`，并由 `decimals` 控制显示和解释时的小数位数。

它适合需要精确到小数的桌面参数：比例、阈值、坐标、透明度、速度、金额、物理单位。它不是无限精度小数控件；显示和设置值都会受到 `decimals` 舍入影响。

### 适合使用的场景

- 小数参数输入，例如 0.0 到 1.0 的比例。
- 有单位的浮点值，例如 `m/s`、`kg`、`%`。
- 需要按步长微调的数值。
- 需要限制范围并给用户即时反馈的数值字段。

### 不适合的场景

- 整数输入用 `QSpinBox`。
- 金融高精度计算不要把 `double` 当最终业务精度；可用整数分、定点数或专门 decimal 类型保存。
- 科学计数法、表达式输入、单位换算复杂时，可能需要自定义编辑器。

## 2. 依赖与对象关系

- 头文件：`#include <QDoubleSpinBox>`
- 模块：Qt Widgets
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QAbstractSpinBox`
- 直接派生类：类页未列出

`QDoubleSpinBox` 继承 `QAbstractSpinBox` 的步进编辑框架，自己负责浮点范围、精度、文本和值之间的转换。`decimals` 会影响最小值、最大值和值的舍入，这是它和整数 spin box 最大的差别。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `value : double` | 当前浮点值。 |
| `decimals : int` | 显示和解释的小数位数。 |
| `minimum : double` / `maximum : double` | 有效范围上下界，会按 decimals 舍入。 |
| `singleStep : double` | 默认步进量。 |
| `stepType : StepType` | 固定步进或自适应十进制步进。 |
| `prefix : QString` / `suffix : QString` | 显示在数值前后的文本。 |
| `cleanText : QString` | 去掉前缀、后缀和空白后的显示文本。 |
| `QDoubleSpinBox(QWidget *parent)` | 创建默认范围 0.0 到 99.99、精度 2、步长 1.0 的控件。 |
| `setRange(min, max)` | 一次设置范围。 |
| `setValue(double)` | 设置当前值，变化时发出 `valueChanged(double)`。 |
| `valueChanged(double)` | 当前浮点值变化时发出。 |
| `textChanged(QString)` | 显示文本变化时发出，包含前后缀。 |
| `textFromValue(double)` | 把值转换为显示文本，子类可重写。 |
| `valueFromText(QString)` | 把文本转换为浮点值，子类可重写。 |
| `validate(QString &, int &)` | 判断输入文本是否合法。 |
| `fixup(QString &)` | 结束编辑时尝试修正输入。 |

## 4. API 逐项说明

### `value`

当前浮点值。设置新值时会按范围限制，并按当前 `decimals` 舍入显示和存储语义处理。变化时发出 `valueChanged(double)`。

需要显示字符串时用 `text()` 或 `textChanged()`；需要业务数值时用 `value()`。

### `decimals`

控制小数位数。默认通常为 2。改变它可能导致当前值、最小值、最大值被重新舍入。

这点非常重要：如果你先设置范围和值，再把 decimals 改小，数值可能变掉。初始化时通常先设置 decimals，再设置范围和值。

### `minimum` / `maximum` / `setRange()`

控制有效范围。设置范围端点时，会按当前 decimals 舍入。默认范围是 0.0 到 99.99。

浮点范围边界要考虑舍入后的结果，例如 decimals 为 2 时，`0.005` 这类值不会按无限精度保留。

### `singleStep` / `stepType`

`singleStep` 是固定步长，默认 1.0。`AdaptiveDecimalStepType` 可根据当前值数量级调整步进。

微调参数时常用 0.1、0.01；跨度大时自适应步进更顺手。

### `prefix` / `suffix`

前后缀用于显示单位或货币符号，例如 `$`、` kg`、` %`。它们不属于 `value()`。

单位最好放 suffix，并包含必要空格，例如 `" ms"`，让数值和单位可读。

### `cleanText`

返回去掉前缀、后缀和空白后的文本。它仍受 locale、小数位和分组分隔符影响。

解析业务值不要依赖它，除非你明确在做文本处理；普通代码读 `value()`。

### 构造和析构

构造函数创建默认浮点 spin box：最小 0.0、最大 99.99、步长 1.0、两位小数、初始值 0.00。

创建后建议按顺序设置 `decimals`、`range`、`singleStep`、`suffix/prefix`、`value`。

### `valueChanged(double)` / `textChanged(QString)`

`valueChanged(double)` 是数值变化信号；`textChanged(QString)` 是显示文本变化信号，包含前后缀和格式化结果。

如果你需要响应用户最终提交，结合 `keyboardTracking(false)` 或 `editingFinished()` 可以减少中间值噪声。

### `textFromValue(double)` / `valueFromText(QString)`

默认按当前 locale、固定小数格式和 decimals 转换。重写可支持百分比缩放、枚举文字、特殊单位格式等。

如果显示格式不是普通数字，务必让反向解析也能理解用户输入。

### `validate()` / `fixup()`

验证和修正用户文本。自定义格式、单位输入、宽松输入规则时会用到。

验证过程应快速、无副作用。真正的业务校验放到提交逻辑中。

## 5. 深入实践与常见坑

### decimals 会改变值

`setDecimals(1)` 后，`1.26` 可能变成 `1.3`。不要在用户编辑过程中随意改 decimals。

### double 不适合最终金融精度

界面上用 `QDoubleSpinBox` 输入金额可以，但核心计算和存储最好使用整数分或定点类型，避免浮点误差。

### 初始化顺序很关键

推荐顺序：`setDecimals()`、`setRange()`、`setSingleStep()`、`setValue()`。这样范围和值都会按最终精度解释。

### 文本信号包含格式

`textChanged()` 可能给你 `"12.50 kg"`，不是纯数字。业务逻辑连接 `valueChanged(double)` 更安全。
