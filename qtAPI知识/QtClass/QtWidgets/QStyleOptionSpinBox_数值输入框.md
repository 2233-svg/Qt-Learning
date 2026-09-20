# Qt QStyleOptionSpinBox 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QStyleOptionSpinBox>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QStyleOption -> QStyleOptionComplex -> QStyleOptionSpinBox`  
> 定位：把微调框的边框、编辑区和上下步进按钮状态交给 `QStyle` 的绘制参数

## 1. 它不是 QSpinBox，也不保存输入值

`QStyleOptionSpinBox` 是 style option：它描述“这一帧的微调框应如何画”，本身不是输入控件，没有文本、数值模型、信号和 QObject 生命周期。

Qt 不只用它来画 `QSpinBox`，也用它来画 `QDateTimeEdit`。这很合理：日期时间编辑器在外观上同样由一个编辑区域和可递增、递减的步进按钮组成。

```text
QAbstractSpinBox 的子类
  └─ initStyleOption(&option)
       └─ QStyleOptionSpinBox
            ├─ frame：是否绘制外框
            ├─ buttonSymbols：按钮画箭头、加减号还是不画
            └─ stepEnabled：上、下按钮此刻是否可用
                 └─ QStyle::drawComplexControl(CC_SpinBox, ...)
```

业务逻辑应调用 `QAbstractSpinBox`、`QSpinBox`、`QDoubleSpinBox` 或 `QDateTimeEdit` 的公共 API。直接使用这个类的场景是自定义绘制、实现 `QProxyStyle`，或从当前 style 取得编辑区和按钮的准确几何。

## 2. 为什么“能不能加一”要交给 style

微调框在最小值、最大值、特殊文本、循环（wrapping）或日期边界附近，按钮能否继续执行并不相同。`stepEnabled` 把这个决定传给 style：

```text
当前为 maximum，且 wrapping = false
  -> StepUpEnabled 不在 stepEnabled 中
  -> 上按钮应画为不可用状态

当前为 minimum，且 wrapping = false
  -> StepDownEnabled 不在 stepEnabled 中
  -> 下按钮应画为不可用状态
```

这比仅看 `widget->isEnabled()` 更细。控件整体可用，并不表示两个步进方向都可用；style 需要分别画出上、下按钮的禁用、悬停与按下状态。

`stepEnabled` 是 `QAbstractSpinBox::StepEnabled` 标志组合，常见含义如下：

| 标志 | 表示什么 |
| --- | --- |
| `StepUpEnabled` | 可以向上步进，例如数值加一或日期进入下一段 |
| `StepDownEnabled` | 可以向下步进 |
| `StepNone` | 两个方向都不能步进 |

它是控件状态的绘制快照，不要在 style 中靠修改该字段来改变真实范围或值。

## 3. 标准用法：让 style 画完整微调框

如果子类只是要叠加自己的内容，先让当前平台 style 画完复杂控件：

```cpp
void FancySpinBox::paintEvent(QPaintEvent *)
{
    QStyleOptionSpinBox option;
    initStyleOption(&option);

    QStylePainter painter(this);
    painter.drawComplexControl(QStyle::CC_SpinBox, option);

    const QRect editRect = style()->subControlRect(
        QStyle::CC_SpinBox,
        &option,
        QStyle::SC_SpinBoxEditField,
        this);
    drawUnitHint(painter, editRect);
}
```

不要根据控件宽度硬编码“右边 20 像素是按钮”。Windows、macOS、Fusion、代理 style、缩放比例与 RTL 布局都可能让按钮大小和位置不同。通过 `subControlRect()` 请求当前 style 的 `SC_SpinBoxUp`、`SC_SpinBoxDown`、`SC_SpinBoxEditField` 才是可靠做法。

从真实控件绘制时，始终优先调用 `initStyleOption(&option)`。除了本类的三个字段，它还会从基类填入 `rect`、`palette`、`state`、`direction`、`fontMetrics`、`subControls` 与 `activeSubControls` 等信息。

## 4. 三个公开字段各自解决什么

### 4.1 `buttonSymbols`

`buttonSymbols` 决定按钮采用哪种符号：

| 值 | 视觉含义 | 典型场景 |
| --- | --- | --- |
| `QAbstractSpinBox::UpDownArrows` | 上下箭头 | 常规数值、日期和时间编辑 |
| `QAbstractSpinBox::PlusMinus` | 加号、减号 | 需要强调增减概念的设置面板 |
| `QAbstractSpinBox::NoButtons` | 不显示步进按钮 | 仍可编辑文本，但不提供按钮步进 |

它改变的是样式输入，而非数值行为。把符号改为 `PlusMinus` 不会自动改动 `stepBy()`；使用 `NoButtons` 也不代表禁止键盘、滚轮或程序调用步进。

### 4.2 `frame`

`frame` 指定样式是否画微调框的外框。它对应 `QAbstractSpinBox::hasFrame()` 的视觉结果。

无边框控件经常放在工具栏、表格代理编辑器或自定义表单中。不要仅将 CSS 边框设为透明就认为状态一致；style option 的 `frame` 能让平台 style 有机会相应调整内边距、编辑区和按钮区域。

### 4.3 `stepEnabled`

这个字段告诉 style 哪个方向的按钮应该呈现为不可点。它与 `buttonSymbols` 配合，但职责不同：

```text
buttonSymbols = PlusMinus      -> 决定按钮看起来像 + / -
stepEnabled = StepDownEnabled  -> 决定只有减号此刻可用
```

对于 `QDateTimeEdit`，某一节能否继续递增还可能受最小/最大日期时间、当前 section 和 wrapping 设置影响；不能用简单的整数比较代替控件已经算出的 `stepEnabled`。

## 5. 自定义 style：安全转换和局部替换

`QStyle::drawComplexControl()` 的参数是 `QStyleOptionComplex *`，它可能属于多种复杂控件。自定义 style 应先检查控件类别，再用 `qstyleoption_cast()`：

```cpp
void FlatStyle::drawComplexControl(
    QStyle::ComplexControl control,
    const QStyleOptionComplex *option,
    QPainter *painter,
    const QWidget *widget) const
{
    if (control == QStyle::CC_SpinBox) {
        const auto *spin =
            qstyleoption_cast<const QStyleOptionSpinBox *>(option);

        if (spin && !(spin->stepEnabled & QAbstractSpinBox::StepUpEnabled)) {
            // 根据当前 style 规则，弱化上按钮的视觉。
        }
    }

    QProxyStyle::drawComplexControl(control, option, painter, widget);
}
```

不要用 `static_cast` 假定所有 `QStyleOptionComplex` 都是微调框。`Type = SO_SpinBox` 和 `Version = 1` 是 `qstyleoption_cast()` 用来检查布局的标签；普通 style 代码不必自行比较它们。

## 6. 常见错误

### 6.1 只画按钮，不画编辑区

症状：文本光标、选择态、调色板和输入法预编辑文字表现异常。

原因：微调框的编辑区通常由内部 `QLineEdit` 及 style 协作完成。只手绘两个按钮无法复刻完整行为。

处理：除非你也接管编辑器与输入事件，否则让 `QStyle::drawComplexControl()` 完成基础绘制，只叠加少量装饰。

### 6.2 把 `StepNone` 当成控件整体禁用

症状：边界值时整个控件被画灰，用户甚至不能选中文本复制。

原因：不能步进不等于不能编辑或不能获得焦点。

处理：仅针对相应方向的子按钮呈现禁用效果，控件整体可用状态仍应读取继承的 `QStyleOption::state`。

### 6.3 手工创建 option 却忘了 frame

症状：独立绘制时微调框没有边框或内边距不正确。

原因：默认 `frame` 是 `false`，默认 `stepEnabled` 也是 `StepNone`。

处理：手工 option 必须填入完整、相互一致的字段；优先从实际控件初始化。

## API 速查表
以下列出 Qt 6.11.1 类文档中 `QStyleOptionSpinBox` 直接声明的类型、构造函数和公开字段。`QStyleOptionComplex` 继承来的子控件标志与 `QStyleOption` 的通用绘制字段不在此表内。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举常量 | `StyleOptionType::Type = SO_SpinBox` | 标识这是微调框的 style option。 | 用于样式系统和 `qstyleoption_cast()` 的类型识别。 |
| 枚举常量 | `StyleOptionVersion::Version = 1` | 标识本结构的版本。 | 普通使用不需要手工检查版本。 |
| 构造 | `QStyleOptionSpinBox()` | 创建并以默认值初始化 option。 | 默认无框且两个方向都不可步进，真实绘制前应初始化状态。 |
| 构造 | `QStyleOptionSpinBox(const QStyleOptionSpinBox &other)` | 复制一份微调框绘制状态。 | 是值复制，不拥有或复制实际控件。 |
| 公开字段 | `QAbstractSpinBox::ButtonSymbols buttonSymbols` | 指定步进按钮画箭头、加减号或不画按钮。 | 默认 `UpDownArrows`；只影响外观符号。 |
| 公开字段 | `bool frame` | 指定是否绘制微调框外框。 | 默认 `false`；也会影响 style 对内部几何的处理。 |
| 公开字段 | `QAbstractSpinBox::StepEnabled stepEnabled` | 指定上、下步进方向哪些当前可用。 | 默认 `StepNone`；不等于控件整体禁用。 |

## 8. 一句话总结

`QStyleOptionSpinBox` 是微调框绘制时的状态说明：`buttonSymbols` 决定按钮像什么，`frame` 决定外框是否存在，`stepEnabled` 决定哪一个方向此刻能操作；真实控件状态应由 `initStyleOption()` 交给样式系统，而不是手工猜测。
