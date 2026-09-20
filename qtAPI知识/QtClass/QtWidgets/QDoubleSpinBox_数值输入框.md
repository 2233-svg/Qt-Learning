# Qt QDoubleSpinBox 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QDoubleSpinBox>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QWidget -> QAbstractSpinBox -> QDoubleSpinBox`  
> 定位：带范围、精度和步进规则的 `double` 输入控件

## 1. QDoubleSpinBox 解决什么问题

`QDoubleSpinBox` 用来编辑有确定取值范围的连续数值，例如不透明度、缩放比例、温度、时间间隔、旋转角度、阈值和物理尺寸。用户可以键入数值，也可以用箭头、滚轮或键盘逐步调整。

```text
缩放： [ 125.0 ][▲]
                 [▼] %
```

它解决的不是“如何显示一个小数”，而是把下面几件事放在同一个控件里：

- 限制合法范围，避免把负尺寸、超过 100% 的不透明度交给业务层；
- 用 `decimals` 统一输入精度和显示精度；
- 用 `singleStep` 让每次交互改变符合业务意义；
- 以 `value()` 交给程序，以带单位的文本交给人看。

精确离散值用 `QSpinBox`；日期、时间和日期时间用 `QDateEdit`、`QTimeEdit`、`QDateTimeEdit`。金额等要求十进制精确运算的领域，不应把 `double` 当作账务存储类型：业务层宜保存“分”等整数或十进制定点值，`QDoubleSpinBox` 仅负责输入和显示转换。

## 2. 最小可用示例：编辑缩放比例

```cpp
#include <QDoubleSpinBox>

auto *zoom = new QDoubleSpinBox(this);
zoom->setDecimals(1);
zoom->setRange(25.0, 400.0);
zoom->setSingleStep(5.0);
zoom->setSuffix("%");
zoom->setValue(100.0);

connect(zoom, &QDoubleSpinBox::valueChanged, this,
        [this](double percent) {
            preview->setScale(percent / 100.0);
        });
```

这里控件保存的是 `100.0`，不是 `1.0`；单位约定要由整个界面保持一致。`setSuffix("%")` 只改变显示，不会自动把值除以 100。

将控件传入父对象或添加到布局后，Qt 的父子对象机制会负责销毁它。不要在布局已管理控件后再手动 `delete`。

## 3. `decimals` 不只是外观：它会改变值

`decimals` 同时决定小数的显示和解释精度，默认是 `2`。这是 `QDoubleSpinBox` 与普通“把 `double` 格式化成字符串”最关键的差异。

```cpp
spin->setDecimals(2);
spin->setValue(2.555);
qDebug() << spin->value(); // 2.56
```

为了以当前精度显示，Qt 会对 `value` 做舍入；最小值和最大值也会按该精度舍入。更改 `decimals` 后，已有的 `minimum`、`maximum` 和 `value` 都可能变化。

```cpp
spin->setDecimals(3);             // 先确定精度
spin->setRange(0.125, 10.875);    // 再设置边界
spin->setValue(1.234);
```

因此应当**先设置 `decimals`，再设置范围和值**。`decimals` 最大可设为 `323`，但这只是 `double` 类型能力的上限；界面中通常只保留人能理解的精度。控件显示的数值部分最多 18 个字符，前缀和后缀不计入这个限制，极端大的数或极长精度不适合作为此控件的常规交互目标。

## 4. 数值、文本、区域设置和单位

```cpp
spin->setPrefix("温度 ");
spin->setSuffix(" °C");
spin->setValue(23.5);
```

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 数值 | `value()` | 返回已经校验并提交的 `double` 数值 | 业务计算、保存设置和模型同步应读它，不要从显示文本反解析 |
| 显示文本 | `text()` | 返回当前完整显示文本，包含 prefix、suffix 和本地化格式 | 适合展示或日志；文本可能受 locale、小数位数和特殊值文本影响 |
| 显示文本 | `cleanText()` | 返回去掉前后缀和首尾空白后的显示文本 | 仍然是文本，不是业务数值；小数分隔符可能受 locale 影响 |

业务逻辑应读取 `value()`，不要从 `text()` 或 `cleanText()` 反向解析数值。默认格式化与解析会使用控件的 `locale()`；例如某些区域设置把逗号作为小数点。需要给控件赋值时直接调用 `setValue()`，而不是构造带 `.` 的文本塞进内部 `QLineEdit`。

`prefix`、`suffix` 可以为空。若设置了继承而来的 `specialValueText`，并且值等于 `minimum()`，控件只显示特殊文本，不显示前缀或后缀：

```cpp
spin->setRange(0.0, 10.0);
spin->setSpecialValueText("自动");
// value() == 0.0 时，显示“自动”
```

特殊文本不是额外的值；业务层仍应使用 `value() == minimum()` 判断“自动”状态。

## 5. 范围、步长与循环

构造后默认范围是 `0.0` 到 `99.99`，默认值为 `0.00`，默认步长为 `1.0`。

```cpp
spin->setDecimals(2);
spin->setRange(-12.50, 12.50);
spin->setSingleStep(0.25);
```

- `setRange(min, max)` 一次设置两端，适合初始化；
- `setMinimum()` 和 `setMaximum()` 适合只改一端；若新边界会让范围失效，另一端会随之调整；
- 每次步进增加或减少 `singleStep`；负步长设置无效；
- 范围和当前值都会按 `decimals` 舍入，所以不要把“内部精度比显示精度高”的需求交给一个 `QDoubleSpinBox`。

`wrapping` 是 `QAbstractSpinBox` 的属性。开启后，从最大值向上步进会回到最小值，反向亦然。它适合色相角度、循环档位等有环形语义的值；温度、音量上限、比例等通常不应循环，否则用户轻易越过边界回到另一端。

### 自适应十进制步进

```cpp
spin->setStepType(QAbstractSpinBox::AdaptiveDecimalStepType);
```

此时 Qt 忽略 `singleStep`，改为根据当前值的数量级自动选择约低一位的 10 的幂：

```text
1100    向上 -> 1200
0.041   向上 -> 0.042
100     向下 -> 99
99      向上 -> 100
```

方向会参与边界处理，因此“向上一步再向下一步”会回到原值。它适合可跨多个数量级粗调的采样数、缓存大小或物理参数；需要固定增量的百分比、角度和步进档位应使用默认 `DefaultStepType`。

## 6. 信号与“用户还在输入”的状态

```cpp
connect(spin, &QDoubleSpinBox::valueChanged, this,
        &Controller::setThreshold);

connect(spin, &QDoubleSpinBox::textChanged, this,
        [](const QString &shown) {
            qDebug() << shown;
        });
```

| 信号 | 何时使用 | 注意点 |
| --- | --- | --- |
| `valueChanged(double)` | 更新模型、预览或配置。 | 参数是已经接受并按 `decimals` 舍入的数值。 |
| `textChanged(const QString &)` | 观察显示字符串。 | 参数包含 prefix 和 suffix，不适合作为业务数值。 |
| `editingFinished()` | 用户按 Enter 或控件失焦后统一提交。 | 来自 `QAbstractSpinBox`，适合触发耗时计算或一次性校验。 |

继承的 `keyboardTracking` 默认开启，用户每输入一个可解释的中间值就可能发出 `valueChanged()` 和 `textChanged()`。若改变数值会启动昂贵计算、网络请求或写入磁盘，可以关闭它，并在 `editingFinished()` 中提交：

```cpp
spin->setKeyboardTracking(false);
connect(spin, &QAbstractSpinBox::editingFinished, this,
        [spin, this] { applyThreshold(spin->value()); });
```

`interpretText()` 可让程序立即尝试把当前编辑文本解释为数值；`hasAcceptableInput()` 用于判断输入是否可接受。不要把它们当作跨字段业务校验的替代品。

## 7. 自定义文本与解析：必须成对设计

当内置前缀、后缀不足以表达值时，可以继承并重写：

| 可重写 API | 职责 |
| --- | --- |
| `textFromValue(double)` | 把内部数值转换为要显示的核心文本。默认实现按 `locale()` 和 `decimals` 格式化。 |
| `valueFromText(const QString &)` | 将用户输入的核心文本解析成数值。 |
| `validate(QString &, int &)` | 在输入过程中回答“可接受、尚可继续输入、无效”。 |
| `fixup(QString &)` | 用户提交时，尝试把尚未可接受的文本修正为可接受形式。 |

`textFromValue()` 的返回值**不要包含** `prefix` 或 `suffix`，因为 Qt 会单独拼接它们；`specialValueText` 也由 Qt 单独处理，不会调用这两个转换函数。只改显示而不改解析，或只改解析而不改校验，都会让用户看到“能显示却不能输入”或“能输入却回显异常”的控件。

例如需让用户输入 `1.5k`、`750ms`、`32 x 32` 这类领域文本，应一起设计可逆的显示、解析和输入中间态；如果只是常规单位，优先使用 `setSuffix()`，不必为此创建子类。

## API 速查表
下表按 Qt 6.11.1 的 `qspinbox.h` 中 `QDoubleSpinBox` 部分整理。注意：本类的头文件包含写法仍是 `#include <QDoubleSpinBox>`，但声明与 `QSpinBox` 同在 `qspinbox.h`。

### 8.1 构造、文本和值

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDoubleSpinBox(QWidget *parent = nullptr)` | 创建小数输入控件 | 默认范围是 `0.0..99.99`，默认精度 2，默认步长 1.0 |
| 生命周期 | `~QDoubleSpinBox()` | 销毁控件 | 通常交给 QWidget 父子对象树 |
| 值 | `value() const` | 读取当前业务数值 | 已受范围和 `decimals` 舍入约束，业务计算优先读它 |
| 值 | `setValue(double value)` | 设置当前业务数值 | 公共槽；会夹到范围内并按当前 `decimals` 舍入 |
| 前缀 | `prefix() const` | 读取数值前的显示文本 | 前缀只是 UI，不改变 `value()` |
| 前缀 | `setPrefix(const QString &prefix)` | 设置数值前的显示文本 | 适合货币符号、标签；特殊最小值文本显示时不显示前缀 |
| 后缀 | `suffix() const` | 读取数值后的显示文本 | 常用于 `%`、`ms`、`px`、单位 |
| 后缀 | `setSuffix(const QString &suffix)` | 设置数值后的显示文本 | 不负责单位换算，`100%` 的 value 仍由你约定 |
| 文本 | `cleanText() const` | 返回去掉前缀、后缀和首尾空白后的显示文本 | 可用于日志或展示；不要反向解析做业务计算 |

### 8.2 范围、精度与步进

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 步进 | `singleStep() const` | 读取固定步进值 | 自适应十进制步进开启时会被保留但暂不参与步进 |
| 步进 | `setSingleStep(double value)` | 设置固定步进值 | 负数无效；固定百分比、角度、尺寸增量常用 |
| 范围 | `minimum() const` | 读取下界 | 已按当前 `decimals` 舍入 |
| 范围 | `setMinimum(double min)` | 设置下界 | 可能为维持合法范围而调整 maximum 和 value |
| 范围 | `maximum() const` | 读取上界 | 已按当前 `decimals` 舍入 |
| 范围 | `setMaximum(double max)` | 设置上界 | 可能为维持合法范围而调整 minimum 和 value |
| 范围 | `setRange(double min, double max)` | 一次设置上下界 | 初始化时推荐用它；先设 `decimals` 再设范围 |
| 步进类型 | `stepType() const` | 读取固定步进或自适应十进制步进模式 | 类型来自 `QAbstractSpinBox::StepType` |
| 步进类型 | `setStepType(StepType stepType)` | 设置步进模式 | `AdaptiveDecimalStepType` 会按当前数值量级自动选步长 |
| 精度 | `decimals() const` | 读取小数位数 | 同时影响显示、解析和值/边界舍入 |
| 精度 | `setDecimals(int precision)` | 设置小数位数 | 会改变已有 minimum、maximum 和 value；应优先于范围和值设置 |

### 8.3 自定义显示、解析与信号

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 校验 | `validate(QString &input, int &pos) const` | 判断正在输入的文本是否可接受 | 重写时要允许合理中间态，例如 `-`、`.`、局部单位文本 |
| 解析 | `valueFromText(const QString &text) const` | 把用户输入文本转换为 double | 与 `textFromValue()` 和 `validate()` 成对设计 |
| 显示 | `textFromValue(double value) const` | 把 double 转为核心显示文本 | 返回值不要包含 prefix、suffix 或 special value text |
| 修正 | `fixup(QString &input) const` | 提交时尝试修正尚未完全有效的文本 | 可补单位、修剪空白；不应偷偷做复杂业务修正 |
| 信号 | `valueChanged(double value)` | 已接受的业务数值改变时发出 | 参数已按范围和精度处理；业务层最常连接 |
| 信号 | `textChanged(const QString &text)` | 显示文本变化时发出 | 文本包含 prefix/suffix，适合 UI 观察，不适合数值计算 |

### 8.4 常用继承 API

这些 API 定义在 `QAbstractSpinBox`，但使用 `QDoubleSpinBox` 时经常一起考虑：

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 提交时机 | `setKeyboardTracking(bool tracking)` | 控制键入过程中是否实时更新 value | 耗时计算可设为 false，再监听 `editingFinished()` |
| 提交信号 | `editingFinished()` | Enter 或失焦后发出 | 适合最终提交和跨字段校验 |
| 文本解释 | `interpretText()` | 立即解释当前编辑文本 | 程序需要强制提交内部 line edit 文本时使用 |
| 特殊值 | `setSpecialValueText(const QString &text)` | 让 minimum 显示为特殊含义 | 业务上仍是 `value() == minimum()` |
| 循环 | `setWrapping(bool wrap)` | 让步进越过边界时从另一端继续 | 只适合角度、色相等环形语义 |
| 步进 | `stepUp()` / `stepDown()` | 以当前步进规则增加或减少 | 遵守范围、wrapping 和 step type |

## 9. 一句话总结

`QDoubleSpinBox` 是“小数输入 + 范围约束 + 显示精度”的控件；先确定 `decimals`，再设置范围和值，业务层始终使用 `value()`，而不是显示文本。
