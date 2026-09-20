# QAbstractSpinBox

> Qt 6.11.1 · Qt Widgets · 来自 `QAbstractSpinBox`

## 1. 先建立直觉

### 这是什么

`QAbstractSpinBox` 是所有“可输入、可用按钮步进调整”的控件基类。`QSpinBox`、`QDoubleSpinBox`、`QDateTimeEdit` 都继承它。它把一个内部 `QLineEdit`、一组上下步进按钮、验证/修正流程和键盘鼠标事件组织成统一控件。

它本身不是用来直接表示某个具体数值类型的；具体含义由子类决定。你应把它理解成“步进编辑器框架”：文本如何转成值、值如何显示成文本、哪些方向可以步进，都由子类或重写函数提供。

### 适合使用的场景

- 理解 `QSpinBox`、`QDoubleSpinBox`、`QDateTimeEdit` 的共同属性。
- 自定义一种可步进编辑控件，例如枚举值、版本号、带单位的特殊范围。
- 需要控制键盘跟踪、循环步进、特殊最小值文本、按钮符号、校正策略。
- 需要访问或替换内部 `QLineEdit`。

### 不适合的场景

- 普通整数输入直接用 `QSpinBox`。
- 普通浮点输入直接用 `QDoubleSpinBox`。
- 日期时间输入用 `QDateTimeEdit` 系列。
- 自由文本输入用 `QLineEdit`，不要为了两个按钮硬套 spin box。

## 2. 依赖与对象关系

- 头文件：`#include <QAbstractSpinBox>`
- 模块：Qt Widgets
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QWidget`
- 直接派生类：`QDateTimeEdit`、`QDoubleSpinBox`、`QSpinBox`

### 内部编辑器

spin box 内部有一个 `QLineEdit`。用户可以键入文本，也可以通过按钮、方向键、滚轮调用步进。文本提交时，控件会验证、必要时修正，再把文本解释为子类的值。

### 三个阶段

输入阶段由用户编辑文本；解释阶段由 `interpretText()`、`validate()`、`fixup()` 处理；步进阶段由 `stepBy()` 和 `stepEnabled()` 控制。弄清这三个阶段，才容易写出自定义 spin box。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `enum ButtonSymbols` | 步进按钮显示箭头、加减号或不显示按钮。 |
| `enum CorrectionMode` | 编辑结束时如何修正中间态文本。 |
| `flags StepEnabled` / `enum StepEnabledFlag` | 当前是否允许向上或向下步进。 |
| `enum StepType` | 默认步进或自适应十进制步进。 |
| `accelerated : bool` | 长按按钮时步进是否加速。 |
| `acceptableInput : bool` | 当前文本是否可接受。 |
| `alignment : Qt::Alignment` | 内部文本对齐方式。 |
| `buttonSymbols : ButtonSymbols` | 步进按钮符号样式。 |
| `correctionMode : CorrectionMode` | 中间输入结束后的修正方式。 |
| `frame : bool` | 是否绘制边框。 |
| `keyboardTracking : bool` | 键入过程中是否即时发出值变化。 |
| `readOnly : bool` | 是否禁止用户编辑。 |
| `showGroupSeparator : bool` | 是否显示数字分组分隔符。 |
| `specialValueText : QString` | 最小值对应的特殊显示文本。 |
| `text : QString` | 当前显示文本。 |
| `wrapping : bool` | 到最大/最小值后是否循环。 |
| `fixup(QString &input)` | 尝试把不可接受输入修正为可接受输入。 |
| `validate(QString &input, int &pos)` | 判断输入是可接受、中间态还是非法。 |
| `interpretText()` | 强制解释当前编辑文本。 |
| `stepBy(int steps)` | 按指定步数改变值，子类通常重写。 |
| `stepEnabled() const` | 返回当前允许哪些步进方向。 |
| `stepUp()` / `stepDown()` | 向上或向下步进一格。 |
| `clear()` / `selectAll()` | 清空编辑文本或全选。 |
| `lineEdit()` / `setLineEdit()` | 访问或替换内部编辑器。 |
| `editingFinished()` | 编辑完成时发出。 |
| `returnPressed()` | Qt 6.10 起，按回车时发出。 |
| `initStyleOption(QStyleOptionSpinBox *)` | 为绘制准备 style option。 |
| 事件函数 | 处理输入法、键盘、鼠标、滚轮、按钮按住、绘制和焦点。 |

## 4. API 逐项说明

### `ButtonSymbols`

控制右侧按钮画什么：经典上下箭头、加减号，或不显示按钮。某些平台 style 可能把不同符号画得很接近。

`NoButtons` 适合只保留键盘输入和滚轮/快捷键步进的紧凑界面，但可发现性会下降。

### `CorrectionMode`

当用户输入处于 `Intermediate`，并结束编辑时，控件需要决定怎么修正。`CorrectToPreviousValue` 回到上一个有效值；`CorrectToNearestValue` 尝试修正到最接近有效值。

表单里需要避免用户误提交时，回到旧值更保守；连续数值调节器则可能更适合修正到最近值。

### `StepEnabled` / `StepEnabledFlag`

描述当前能否向上或向下步进。到达最小值时通常禁用向下，到达最大值时禁用向上；如果 `wrapping` 为真，则两端可能继续允许步进。

自定义 spin box 应正确实现它，否则按钮禁用状态和键盘行为会与实际值不一致。

### `StepType`

`DefaultStepType` 使用固定步长；`AdaptiveDecimalStepType` 根据当前数值数量级自适应步长，适合跨数量级调节。

具体行为由子类实现，整数和浮点 spin box 的体验会不同。

### `accelerated`

长按步进按钮时逐渐加快变化速度。适合范围较大的数值，例如页码、缩放、音量。

精细参数不一定适合加速，否则用户容易越过目标值。

### `acceptableInput`

只读属性，说明当前文本是否通过子类验证。它反映的是编辑器层面的合法性，不代表业务上一定可提交。

例如数值在范围内是 acceptable，但业务可能仍不允许当前值。

### `alignment` / `frame` / `buttonSymbols`

这些控制外观：文本对齐、是否有边框、按钮符号。数字输入通常右对齐，但 Qt 默认可能随 style 保持左对齐。

外观修改不要掩盖控件语义。去掉按钮后，用户可能不知道它还能步进。

### `keyboardTracking`

开启时，用户每次键入导致有效值变化都会发出子类的 `valueChanged()` / `textChanged()`；关闭时，通常等回车、失焦或步进动作后才提交变化。

如果数值变化会触发昂贵计算，关闭 keyboard tracking 很有价值。

### `readOnly`

只读时内部 line edit 不可编辑，但用户仍可复制文本。它不同于禁用控件，禁用会让整个控件不可交互并弱化显示。

只读适合展示可复制的数值结果，同时保留统一外观。

### `showGroupSeparator`

控制是否显示千分位等本地化分组分隔符。它会影响显示文本，但不应改变真实值。

处理 `textChanged(QString)` 时要记得文本可能包含分隔符、前缀、后缀。

### `specialValueText`

当值等于最小值时，用特殊文本替代数值显示，常见语义是“自动”“无限制”“默认”。设置后，前缀后缀不会应用在这个特殊文本上。

业务代码必须知道最小值代表这个特殊语义，不要只看显示文本。

### `text`

当前显示文本，包含前缀、后缀、分隔符或特殊文本。读取真实值应使用具体子类的 `value()`。

`text()` 适合展示、日志或调试 UI，不适合当作稳定数据源。

### `wrapping`

开启后，步进越过最大值会回到最小值，越过最小值会回到最大值。它只在有限范围内有意义。

时间、月份、循环枚举适合 wrapping；金额、数量、百分比通常不适合。

### `fixup()` / `validate()`

`validate()` 判断输入状态，`fixup()` 在结束编辑时尝试修正。自定义 spin box 经常需要同时重写这两个函数，再配合 `valueFromText()` / `textFromValue()`。

不要在 `validate()` 里做昂贵业务检查；它会在编辑过程中频繁调用。

### `interpretText()`

强制解释当前编辑文本。通常在你需要立即提交编辑器内容时调用，例如读取值前确保文本已经被解释。

普通用户交互中，回车、失焦、步进动作会触发解释流程。

### `stepBy(int steps)` / `stepUp()` / `stepDown()`

`stepUp()` 和 `stepDown()` 是便利槽，内部按一步调用步进；`stepBy()` 是核心虚函数，子类通过它定义正负步数如何改变值。

自定义非数值 spin box 时，`steps` 可能不是简单加减数字，而是移动到枚举列表的前后项。

### `lineEdit()` / `setLineEdit()`

访问或替换内部编辑器。替换后要确保 validator、输入法、选择、只读等行为仍能配合 spin box。

多数场景不需要替换 line edit；设置属性和重写虚函数通常足够。

### `editingFinished()` / `returnPressed()`

`editingFinished()` 表示编辑完成。Qt 6.10 起 `returnPressed()` 表示按下回车。具体子类值变化信号不一定和它们同一时刻发出，尤其在 keyboard tracking 关闭时。

提交表单时更适合监听具体值变化或统一表单提交，而不是只依赖一个 spin box 的回车。

### 事件与绘制函数

spin box 重写了大量事件：键盘、鼠标、滚轮、定时器、输入法、焦点、显示隐藏、绘制和大小变化。它们共同支撑按钮按住、滚轮步进、文本编辑和平台外观。

滚轮尤其要谨慎：表单中鼠标滚过 spin box 导致值变化是常见误操作。需要时可以子类化过滤 `wheelEvent()`。

## 5. 深入实践与常见坑

### 键盘跟踪决定信号频率

`keyboardTracking` 开启时，输入 `600` 可能在中途产生多个值变化。昂贵计算、预览刷新、网络请求应关闭它或做防抖。

### 特殊文本不是特殊值类型

`specialValueText` 只是显示层约定，真实值仍然是最小值。业务层要明确这个最小值代表什么。

### 自定义 spin box 至少要成对重写

如果你让显示文本不再是普通数字，通常要同时重写 `textFromValue()`、`valueFromText()`、`validate()`，必要时加 `fixup()`。

### 滚轮误触很常见

在滚动表单里，用户可能只是想滚页面，却改变了数值。对关键数值，可以要求控件有焦点时才响应滚轮。
