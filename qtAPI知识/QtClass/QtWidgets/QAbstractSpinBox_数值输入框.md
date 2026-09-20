# Qt QAbstractSpinBox 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QAbstractSpinBox>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QWidget -> QAbstractSpinBox`  
> 定位：为整数、小数、日期时间等“可编辑文本 + 步进按钮”控件提供共同框架

## 1. QAbstractSpinBox 解决什么问题

`QAbstractSpinBox` 把 spin box 的共同行为抽出来，让不同类型的值都能拥有同一套输入体验：

```text
[  可编辑文本  ][ ▲ ]
                  [ ▼ ]
```

它负责：

- 显示和编辑文本；
- 接入 `QLineEdit` 的输入、选择、复制和输入法；
- 在输入过程中判断 `Acceptable` / `Intermediate` / `Invalid`；
- 按上、下、PageUp、PageDown、滚轮或按钮步进；
- 处理越界、环绕、特殊最小值文本和提交时机；
- 给 `QSpinBox`、`QDoubleSpinBox`、`QDateTimeEdit` 提供扩展钩子。

它不是具体的数值控件。它不知道“字符串 `12.5` 应怎样转换成 double”或“日期怎样格式化”；这些由派生类实现 `validate()`、`fixup()`、`stepBy()`、`stepEnabled()` 等函数完成。

## 2. 输入文本和已提交值是两件事

这是使用 spin box 时最容易混淆的地方：

```text
用户正在输入 "12e"
  text()             可能是 "12e"
  acceptableInput    可能为 false 或 intermediate
  派生类的数值 value 仍可能是上一次已提交值

用户按 Enter / 失去焦点
  interpretText()
  validate() / fixup()
  按 correctionMode 修正
  派生类更新 value
  发出 editingFinished，必要时发出 valueChanged
```

`keyboardTracking` 控制键入过程是否持续把文本解释为值：

| 设置 | 键入时 | 适合场景 |
| --- | --- | --- |
| `true`（默认） | 每次键入都可能发出派生类的 `valueChanged()`、`textChanged()`。 | 数值变化要实时驱动预览。 |
| `false` | 键入时不持续发值变化信号；按 Enter、失焦、按步进按钮等操作时再解释文本。 | 输入中间状态可能暂时无效，避免每个字符触发昂贵业务逻辑。 |

`acceptableInput` 只表示当前文本是否满足当前验证器，不等于“用户已经提交了一个新值”。需要最终提交时，监听派生类的 value signal 与 `editingFinished()`，不要只看 `text()`。

## 3. 校验、修正与 CorrectionMode

派生类的 `validate(QString &input, int &pos)` 返回 `QValidator::State`：

| 状态 | 含义 |
| --- | --- |
| `Acceptable` | 文本可以解释为合法值。 |
| `Intermediate` | 当前输入暂时不完整，但继续编辑可能变合法。 |
| `Invalid` | 当前文本不可能成为合法输入，或不满足格式。 |

当用户按 Enter 或调用 `interpretText()` 时，如果输入仍是 `Intermediate`，`correctionMode` 决定处理方式：

- `CorrectToPreviousValue`：退回上一次合法值，默认模式；
- `CorrectToNearestValue`：修正到最近的合法值。

`fixup(QString &input)` 是可重写的修正机会。它在输入不是 `Acceptable` 时尝试把文本改成合法形式，例如补齐单位、去掉多余字符或把可识别的近似文本改成标准格式。最终是否接受，仍需经过验证。

```cpp
class PortSpinBox : public QSpinBox
{
protected:
    void fixup(QString &input) const override
    {
        input.remove(' ');
    }
};
```

普通应用一般不需要直接调用这些函数；实现自定义 spin box 时，它们才是核心扩展点。

## 4. 步进模型与 modifier

```cpp
spin->stepUp();    // 等价于 stepBy(1)
spin->stepDown();  // 等价于 stepBy(-1)
```

`stepBy(int steps)` 是派生类必须理解的抽象操作。按键通常产生：

- Up：`stepBy(1)`；
- Down：`stepBy(-1)`；
- PageUp：`stepBy(10)`；
- PageDown：`stepBy(-10)`。

按住 `Ctrl` 时，Qt 默认把步长放大为 10 倍；macOS 上这个逻辑键对应 Command。style hint `QStyle::SH_SpinBox_StepModifier` 可以选择 modifier，`Qt::NoModifier` 可以关闭这个功能。

`stepEnabled()` 返回 `StepEnabled` flags，决定当前是否允许向上或向下步进，也影响上下按钮是否绘制为 disabled：

```cpp
if (stepEnabled() & QAbstractSpinBox::StepUpEnabled) {
    // 可以向上步进
}
```

默认情况下，非 wrapping 的 spin box 在 minimum 处不能向下，在 maximum 处不能向上；开启 wrapping 后两边都可继续步进，由派生类将一端绕到另一端。

## 5. wrapping、specialValueText 与按钮外观

### 5.1 wrapping

```cpp
spin->setRange(0, 100);
spin->setWrapping(true);
spin->setValue(100);
spin->stepUp(); // 回到 0
```

`wrapping` 只在有明确 minimum / maximum 时有意义。它适合月份、角度、循环索引等周期值，不适合金额、端口、文件大小这类越过边界就应停止的数值。

### 5.2 specialValueText

当当前值等于 `minimum()` 时，`specialValueText` 可以替代数字显示：

```cpp
spin->setRange(0, 1000);
spin->setSpecialValueText("自动");
```

此时值为 0 的业务含义仍由应用解释，例如“自动适配”；特殊文本只是显示层。特殊值显示时 prefix 和 suffix 不显示，设置空字符串即可关闭特殊文本。

### 5.3 buttonSymbols

按钮可以显示：

- `UpDownArrows`：经典上下箭头，默认；
- `PlusMinus`：加号与减号；
- `NoButtons`：不显示按钮，但键盘、滚轮和文本输入仍可用。

具体 style 可能把前两者绘制得相同，不要依赖符号外观做程序逻辑。

## 6. 替换内部 QLineEdit

自定义派生控件可以通过保护函数 `setLineEdit()` 替换内部编辑框：

```cpp
auto *edit = new QLineEdit;
edit->setPlaceholderText("输入值");
setLineEdit(edit);
```

新 line edit 不能是 `nullptr`，`QAbstractSpinBox` 会接管它的所有权。如果新 line edit 没有 validator，spin box 会把自己的内部 validator 设置上去。替换后还要检查输入法、selection、prefix/suffix、style 和信号行为是否仍符合控件契约。

普通使用不要通过 `findChild<QLineEdit *>()` 修改内部编辑框；这是依赖实现细节。若只需设置只读、对齐、选择等行为，优先使用 QAbstractSpinBox 的公开 API。

## API 速查表
下表按 Qt 6.11.1 的 `qabstractspinbox.h` 直接声明整理。它是编辑框和步进按钮的框架，真正的数值、日期或时间语义由派生类补上。

### 7.1 构造、显示属性和文本状态

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QAbstractSpinBox(QWidget *parent = nullptr)` | 创建带内部编辑框和步进按钮区域的抽象 spin box | 通常不直接用，而是使用 `QSpinBox`、`QDoubleSpinBox`、`QDateTimeEdit` |
| 生命周期 | `~QAbstractSpinBox()` | 销毁 spin box 和它管理的内部对象 | 内部 line edit 由它管理 |
| 按钮外观 | `buttonSymbols() const` | 读取步进按钮显示形式 | 只影响外观，不改变步进语义 |
| 按钮外观 | `setButtonSymbols(ButtonSymbols symbols)` | 设置上下箭头、加减号或不显示按钮 | `NoButtons` 仍保留键盘、滚轮和文本输入 |
| 修正模式 | `setCorrectionMode(CorrectionMode mode)` | 设置编辑结束时如何修正中间态文本 | 默认回到上一次合法值 |
| 修正模式 | `correctionMode() const` | 读取修正模式 | 影响 `interpretText()` 和失焦提交 |
| 输入状态 | `hasAcceptableInput() const` | 判断当前文本是否通过验证 | 不代表用户已经提交新值 |
| 文本 | `text() const` | 返回当前显示文本 | 包含 prefix/suffix 或特殊值文本，具体由派生类决定 |
| 特殊值 | `specialValueText() const` | 读取最小值的替代显示文本 | 空字符串表示未设置 |
| 特殊值 | `setSpecialValueText(const QString &text)` | 设置 minimum 值的特殊显示 | 不改变实际 value；特殊文本显示时 prefix/suffix 通常不显示 |
| 循环 | `wrapping() const` | 查询步进到边界后是否循环 | 只适合有环形语义的值 |
| 循环 | `setWrapping(bool wrapping)` | 设置步进是否从最大/最小绕回 | 派生类要配合自己的范围语义 |
| 只读 | `setReadOnly(bool readOnly)` | 设置是否禁止用户编辑文本 | 仍可显示、复制文本；程序仍可改值 |
| 只读 | `isReadOnly() const` | 查询只读状态 | 不等于 disabled |
| 键盘跟踪 | `setKeyboardTracking(bool tracking)` | 设置键入过程中是否实时解释并提交值 | 昂贵计算或复杂中间态建议关闭 |
| 键盘跟踪 | `keyboardTracking() const` | 查询键盘跟踪状态 | 默认开启 |
| 对齐 | `setAlignment(Qt::Alignment alignment)` | 设置文本水平对齐 | 非法组合不会产生有意义结果 |
| 对齐 | `alignment() const` | 读取文本对齐方式 | |
| 边框 | `setFrame(bool on)` | 设置是否绘制 frame | 不会改变编辑语义 |
| 边框 | `hasFrame() const` | 查询 frame 是否开启 | |
| 加速 | `setAccelerated(bool on)` | 设置长按按钮时是否加速步进 | 大范围值方便，精细调参可能不适合 |
| 加速 | `isAccelerated() const` | 查询加速状态 | |
| 分组符 | `setGroupSeparatorShown(bool shown)` | 设置是否显示数字分组分隔符 | 实际格式依赖派生类和 locale |
| 分组符 | `isGroupSeparatorShown() const` | 查询分组分隔符显示状态 | |

### 7.2 尺寸、解释、校验和步进

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 尺寸 | `sizeHint() const` | 返回推荐尺寸 | 受按钮、frame、字体和当前文本影响 |
| 尺寸 | `minimumSizeHint() const` | 返回最小推荐尺寸 | 给布局协商，不是业务最小值 |
| 文本解释 | `interpretText()` | 立即解释当前编辑文本，必要时修正并提交 | 程序想强制提交内部文本时使用 |
| 事件 | `event(QEvent *event)` | 通用事件入口 | 普通业务不直接调用 |
| 输入法 | `inputMethodQuery(Qt::InputMethodQuery query) const` | 向输入法报告编辑状态 | 输入法光标、选区和周围文本相关 |
| 校验 | `validate(QString &input, int &pos) const` | 判断当前文本是否可接受 | 自定义派生类必须允许合理的 `Intermediate` 状态 |
| 修正 | `fixup(QString &input) const` | 在提交时尝试修正未完全合法文本 | 修正后仍要再次验证 |
| 步进 | `stepBy(int steps)` | 根据步数改变派生类的值 | 派生类实现核心；必须处理范围、循环和禁用状态 |
| 公共槽 | `stepUp()` | 向上步进一格 | 等价于 `stepBy(1)` |
| 公共槽 | `stepDown()` | 向下步进一格 | 等价于 `stepBy(-1)` |
| 公共槽 | `selectAll()` | 选中可编辑文本 | 常用于获得焦点后快速替换 |
| 公共槽 | `clear()` | 清空编辑框文本 | 虚函数；派生类可保持自己的值语义 |

### 7.3 内部编辑框、样式和步进能力

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 样式 | `initStyleOption(QStyleOptionSpinBox *option) const` | 填充当前 spin box 的样式选项 | 自定义绘制时交给 `QStyle` 前调用 |
| 内部编辑框 | `lineEdit() const` | 返回内部 `QLineEdit` | 受保护函数；普通使用不要依赖 `findChild` 修改内部实现 |
| 内部编辑框 | `setLineEdit(QLineEdit *edit)` | 替换内部编辑框并接管所有权 | 不能传空；新编辑框无 validator 时会安装内部 validator |
| 步进能力 | `stepEnabled() const` | 返回当前是否允许向上/向下步进 | 影响按钮 enabled 状态和边界行为 |
| 派生构造 | `QAbstractSpinBox(QAbstractSpinBoxPrivate &dd, QWidget *parent = nullptr)` | Qt 内部派生类传入私有实现 | 普通业务派生类不用 |

### 7.4 信号

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 提交信号 | `editingFinished()` | 编辑结束时发出 | Enter、失焦等提交路径；适合最终处理 |
| 按键信号 | `returnPressed()` | 用户按 Return/Enter 时发出 | Qt 6.10 起；可区分按键提交和普通失焦 |

### 7.5 枚举与 flags

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 步进能力 | `StepNone` | 当前不允许任何步进 | 到达边界且未开启 wrapping 时可能出现 |
| 步进能力 | `StepUpEnabled` | 允许向上步进 | 用按位与检查 |
| 步进能力 | `StepDownEnabled` | 允许向下步进 | 可与 `StepUpEnabled` 同时存在 |
| 按钮外观 | `UpDownArrows` | 使用上下箭头按钮 | 默认且最常见 |
| 按钮外观 | `PlusMinus` | 使用加号和减号按钮 | style 可能绘制得和箭头差别不大 |
| 按钮外观 | `NoButtons` | 不显示步进按钮 | 键盘和滚轮步进仍可用 |
| 修正模式 | `CorrectToPreviousValue` | 结束编辑时退回上一次合法值 | 默认模式，避免把半输入状态变成新值 |
| 修正模式 | `CorrectToNearestValue` | 结束编辑时修正到最近合法值 | 数值边界明确时较友好 |
| 步进类型 | `DefaultStepType` | 使用派生类默认步进方式 | `QSpinBox` / `QDoubleSpinBox` 的普通 `singleStep` 路线 |
| 步进类型 | `AdaptiveDecimalStepType` | 使用自适应十进制步进 | 主要给数值 spin box 用，跨数量级调整更自然 |

### 7.6 事件扩展点

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 尺寸事件 | `resizeEvent(QResizeEvent *event)` | 尺寸变化时重新安排编辑框和按钮 | 自定义布局时保留基类处理 |
| 键盘 | `keyPressEvent(QKeyEvent *event)` | 处理输入、Enter、方向键和 Page 键 | `Up/Down` 通常进入 `stepBy()` |
| 键盘 | `keyReleaseEvent(QKeyEvent *event)` | 处理按键释放 | 长按或 modifier 状态相关 |
| 滚轮 | `wheelEvent(QWheelEvent *event)` | 处理滚轮步进 | 受 step、modifier 和当前可步进状态影响 |
| 焦点 | `focusInEvent(QFocusEvent *event)` | 获得焦点时处理编辑状态 | 可能影响选中文本和输入法 |
| 焦点 | `focusOutEvent(QFocusEvent *event)` | 失去焦点时解释或修正文本 | 不要绕过基类，否则可能漏提交 |
| 菜单 | `contextMenuEvent(QContextMenuEvent *event)` | 处理编辑框上下文菜单 | 复制、粘贴、撤销等编辑动作 |
| 状态事件 | `changeEvent(QEvent *event)` | 响应 style、字体、语言等变化 | 子类重写后通常调用基类 |
| 关闭 | `closeEvent(QCloseEvent *event)` | 控件关闭时收尾 | 少数自定义场景使用 |
| 隐藏 | `hideEvent(QHideEvent *event)` | 控件隐藏时收尾 | 可清理弹出或临时状态 |
| 鼠标 | `mousePressEvent(QMouseEvent *event)` | 处理按钮区和编辑区按下 | 维持按钮状态和焦点 |
| 鼠标 | `mouseReleaseEvent(QMouseEvent *event)` | 处理鼠标释放 | 结束按钮长按或步进 |
| 鼠标 | `mouseMoveEvent(QMouseEvent *event)` | 处理鼠标移动 | 自定义 hover/拖动时使用 |
| 定时器 | `timerEvent(QTimerEvent *event)` | 处理按钮长按和加速步进定时 | 不要误处理基类定时器 |
| 绘制 | `paintEvent(QPaintEvent *event)` | 绘制 frame、按钮和编辑区域 | 自定义绘制时优先使用 style option |
| 显示 | `showEvent(QShowEvent *event)` | 首次显示或重新显示时处理状态 | 延迟初始化场景 |
