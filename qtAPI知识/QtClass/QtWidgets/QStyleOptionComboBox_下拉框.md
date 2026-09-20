# Qt QStyleOptionComboBox 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 与安装头文件整理）  
> 头文件：`#include <QStyleOptionComboBox>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QStyleOption -> QStyleOptionComplex -> QStyleOptionComboBox`  
> 定位：把组合框的当前项、编辑状态、边框和下拉子控件状态交给 `QStyle` 的绘制快照

## 1. 它不是下拉数据模型，也不负责弹窗

`QStyleOptionComboBox` 不保存 `QComboBox` 的所有条目，不控制当前索引，也不会调用 `showPopup()`。它只描述组合框在某一次绘制中“当前选择项和外壳该如何呈现”。

```text
QComboBox
  ├─ model / view：管理候选项
  ├─ currentIndex：管理真实选择
  ├─ lineEdit：可编辑模式下处理输入
  └─ initStyleOption(&option)
       └─ QStyleOptionComboBox
            └─ QStyle::drawComplexControl(CC_ComboBox, ...)
```

这份 option 主要服务：

- `QComboBox` 子类重写 `paintEvent()`，但仍使用系统 style 的边框、箭头和文本布局；
- `QProxyStyle` 自定义下拉箭头、编辑区边距或当前项图标；
- 用 `subControlRect()` 得到 `SC_ComboBoxArrow`、`SC_ComboBoxEditField` 的准确矩形。

真实下拉列表的展示、关闭和内部状态由 `QComboBox::showPopup()`、`hidePopup()` 及其内部 view 管理。option 只参与控件主体的样式绘制。

## 2. 组合框为什么是复杂控件

一个组合框至少有两个可单独命中的视觉区域：

```text
[ 当前项图标 + 当前项文字                 ][v]
 └───────── 编辑/显示区域 ───────────────┘ └箭头┘
```

它继承 `QStyleOptionComplex`，因此除了本类字段，还有：

- `subControls`：哪些子区域需要画；
- `activeSubControls`：当前悬停或按下的是哪个区域；
- `state`：整体是否启用、是否有焦点、是否按下；
- `rect`、`palette`、`direction`：平台主题、可绘制矩形和布局方向。

例如 RTL 界面中下拉箭头通常在左侧。用 `style()->subControlRect()` 而不是硬编码“右边 20 像素”才能正确适配。

## 3. 标准用法：先初始化，再请求 style 的几何

```cpp
void SearchComboBox::paintEvent(QPaintEvent *)
{
    QStyleOptionComboBox option;
    initStyleOption(&option);

    QStylePainter painter(this);
    painter.drawComplexControl(QStyle::CC_ComboBox, option);

    const QRect arrowRect = style()->subControlRect(
        QStyle::CC_ComboBox,
        &option,
        QStyle::SC_ComboBoxArrow,
        this);

    drawSearchBadge(painter, arrowRect);
}
```

`initStyleOption()` 会统一填好：

- 当前项 `currentText`、`currentIcon`、`iconSize`；
- 是否 `editable`、是否 `frame`；
- 当前文字对齐方式；
- 从 `QStyleOption` 和 `QStyleOptionComplex` 继承的状态与子控件标志。

若手工构造 option，只填文字与图标，容易出现主题下文字颜色不对、可编辑组合框的编辑区域错位、RTL 箭头位置错误或禁用态不一致。

## 4. 当前项显示和真实模型状态的边界

`currentText`、`currentIcon` 是当前选中项的**绘制内容**，不是模型本身：

```cpp
QStyleOptionComboBox option;
combo->initStyleOption(&option);

// option.currentText 是当前显示文本的快照。
// option.currentIcon 是当前显示图标的快照。
```

修改 `option.currentText` 后再调用 `drawComplexControl()`，只能改变这次画面；不会：

- 修改 `QComboBox::currentIndex()`；
- 写入 model；
- 发出 `currentTextChanged()`；
- 改变弹出列表中的项目文字。

同理，`currentIcon` 和 `iconSize` 只影响当前闭合状态下组合框主体的图标绘制。要修改真实数据，应调用 `setItemText()`、`setItemIcon()`，或者直接修改模型。

## 5. `editable`、`frame` 与 `textAlignment`

### 5.1 `editable` 不是“文字可改”那么简单

`editable == true` 告诉 style：组合框有可编辑的输入区域。style 会据此调整编辑区、边框、文本留白和可能的焦点呈现。

它不是创建 `QLineEdit` 的命令。真实可编辑性应使用 `QComboBox::setEditable(true)`；在 option 上改这个字段只会让本次绘制看起来像可编辑状态，控件依旧可能没有可输入的 line edit。

### 5.2 `frame` 应与真实控件保持一致

`frame` 决定组合框是否应画外框，默认是 `true`。无框组合框常见于工具栏或嵌入式筛选器，但应通过 `QComboBox::setFrame(false)` 配置真实控件，让 option 自然同步。

只用样式表把边框涂透明、却让 option 仍声明有框，可能导致 style 为框保留内边距，文字区域看起来无端偏移。

### 5.3 `textAlignment` 是当前项的对齐提示

默认是 `Qt::AlignLeft | Qt::AlignVCenter`。它影响闭合状态下 `currentText` 的摆放，不代表 popup view 中每个 item 的排版，也不替代 model 的 `Qt::TextAlignmentRole`。

## 6. `popupRect`：文档明确说明当前未使用

`popupRect` 的名字很像“弹出列表应该出现在哪里”，但 Qt 6.11.1 类文档明确写明它**当前未使用，可以安全忽略**。默认值是空矩形。

因此：

```text
不要用 popupRect 决定下拉窗口位置
不要期待修改 popupRect 改变 QComboBox 的 popup
不要把它当作 SC_ComboBoxListBoxPopup 的替代品
```

需要查询与 style 有关的子控件区域时，使用 `QStyle::subControlRect()`；需要定制 popup 行为时，重写 `showPopup()` 并同时正确处理 `hidePopup()`。Qt 文档特别要求：若自定义 `showPopup()` 显示了自己的弹窗，隐藏它时仍要调用基类 `hidePopup()` 重置内部状态。

## 7. 在 QProxyStyle 中安全读取 option

```cpp
void CompactComboStyle::drawComplexControl(
    QStyle::ComplexControl control,
    const QStyleOptionComplex *option,
    QPainter *painter,
    const QWidget *widget) const
{
    if (control == QStyle::CC_ComboBox) {
        const auto *combo =
            qstyleoption_cast<const QStyleOptionComboBox *>(option);

        if (combo && !combo->editable && combo->currentIcon.isNull()) {
            drawTextOnlyIndicator(*combo, painter);
        }
    }

    QProxyStyle::drawComplexControl(control, option, painter, widget);
}
```

不能把 `QStyleOptionComplex *` 直接转换为这个类：同一套 style API 还会收到 `QStyleOptionSlider`、`QStyleOptionSpinBox` 等数据。`Type = SO_ComboBox` 与 `Version = 1` 是 `qstyleoption_cast()` 进行布局识别的标签。

### 7.1 Qt 6.11.1 离线文档的两个瑕疵

- `QStyleOptionComboBox` 的详细说明段误写成 `QStyleOptionButton contains...`，应理解为本类；
- `Version` 枚举表的常量值为 `1`，但描述列出现 `2`。安装头文件 `qstyleoption.h` 定义的是 `Version = 1`，代码应以编译使用的头文件为准。

## 8. 常见错误

### 8.1 用 option 改当前项

症状：本次重绘文字变了，下一次重绘又恢复。

原因：option 是绘制快照，不是 `QComboBox` 的选择模型。

处理：要变更真实选择，调用 `setCurrentIndex()`、`setCurrentText()` 或修改 model。

### 8.2 以为 `popupRect` 能控制下拉列表

症状：设置矩形后没有任何变化。

原因：该字段在 Qt 6.11.1 中未使用。

处理：使用 `subControlRect()` 处理主体几何；需要自定义 popup 时成对重写 `showPopup()` 与 `hidePopup()`。

### 8.3 手工计算箭头区域

症状：高 DPI 或 RTL 下箭头重叠、点击区域错位。

原因：忽略不同 style 的子控件尺寸与布局规则。

处理：用 `QStyle::SC_ComboBoxArrow` 和 `SC_ComboBoxEditField` 查询当前 style 的实际矩形。

## API 速查表
以下列出 Qt 6.11.1 类文档中 `QStyleOptionComboBox` 直接声明的类型、构造函数和公开字段。`QStyleOptionComplex` 的子控件状态以及 `QStyleOption` 的通用状态不在此表内。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举常量 | `StyleOptionType::Type = SO_ComboBox` | 标识这是组合框 style option。 | 供样式系统和 `qstyleoption_cast()` 识别。 |
| 枚举常量 | `StyleOptionVersion::Version = 1` | 标识本结构版本。 | 以编译所用头文件为准；Qt 6.11.1 离线页描述列有不一致数字。 |
| 构造 | `QStyleOptionComboBox()` | 创建并以默认值初始化 option。 | 默认不可编辑、有边框、当前文字和图标为空。 |
| 构造 | `QStyleOptionComboBox(const QStyleOptionComboBox &other)` | 复制一份组合框绘制状态。 | 是值复制，不复制模型、view、line edit 或 popup。 |
| 公开字段 | `QIcon currentIcon` | 保存当前项在闭合组合框中的图标。 | 修改它只影响本次绘制，不改变 model 的 item icon。 |
| 公开字段 | `QString currentText` | 保存当前项在闭合组合框中的文字。 | 修改它不会改变 current index 或发出选择变化信号。 |
| 公开字段 | `bool editable` | 指示组合框是否应呈现为可编辑。 | 不会创建真实 `QLineEdit`；应通过 `setEditable()` 改变控件行为。 |
| 公开字段 | `bool frame` | 指示是否应绘制组合框外框。 | 默认 `true`；和真实 `hasFrame()` 保持一致。 |
| 公开字段 | `QSize iconSize` | 保存当前项图标的目标尺寸。 | 默认无效尺寸，style 可自行决定尺寸。 |
| 公开字段 | `QRect popupRect` | 预留的 popup 矩形字段。 | Qt 6.11.1 文档明确说当前未使用，可安全忽略。 |
| 公开字段 | `Qt::Alignment textAlignment` | 指定当前显示文本的对齐方式。 | 默认左对齐、垂直居中；不控制 popup view 每项的对齐。 |

## 10. 一句话总结

`QStyleOptionComboBox` 是组合框闭合状态与子控件几何的绘制说明，不是数据模型或 popup 控制器；从真实控件调用 `initStyleOption()`，把几何交给 `QStyle`，并忽略目前未使用的 `popupRect`，才能稳定适配不同平台样式。
