# Qt QStyleOptionGroupBox 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 与安装头文件整理）  
> 头文件：`#include <QStyleOptionGroupBox>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QStyleOption -> QStyleOptionComplex -> QStyleOptionGroupBox`  
> 定位：把分组框的标题、边框和可选复选标题状态交给 `QStyle` 的绘制快照

## 1. 它不是布局容器，而是分组框的绘制说明

`QStyleOptionGroupBox` 不会管理子控件，也不会创建布局。它描述 `QGroupBox` 在当前这一帧应该怎样画出标题、边框、可选的复选框和内容区域。

```text
QGroupBox
  ├─ 子控件与布局：由 QLayout 负责摆放
  ├─ checkable / checked：决定子控件默认启用状态
  └─ initStyleOption(&option)
       └─ QStyleOptionGroupBox
            └─ QStyle::drawComplexControl(CC_GroupBox, ...)
                 ├─ SC_GroupBoxFrame
                 ├─ SC_GroupBoxLabel
                 ├─ SC_GroupBoxCheckBox
                 └─ SC_GroupBoxContents
```

它适合的代码场景是：

- 自定义 `QGroupBox` 的外观，但保留当前 style 对标题缺口、边框与复选框的处理；
- 写 `QProxyStyle`，定制组框标题色、边框或复选标题的子控件区域；
- 通过 `subControlRect()` 取得标题、内容和可选复选框的准确几何，用于叠加绘制或命中判断。

正常业务代码应直接使用 `QGroupBox`，并为其设置布局。`QGroupBox` 不会自动摆放子控件；这件事与 style option 完全是两条职责线。

## 2. 四个子控件解释了为什么它继承 QStyleOptionComplex

一个分组框不只是一个矩形：

```text
  [ ] 连接设置
  ┌──────────────────────────────────┐
  │  主机： [example.com]             │
  │  端口： [443]                     │
  └──────────────────────────────────┘
  ^     ^                              ^
  |     |                              |
checkbox label                        frame / contents
```

当前 style 通过 `QStyle::CC_GroupBox` 处理四个子控件：

| 子控件 | 表示什么 |
| --- | --- |
| `SC_GroupBoxFrame` | 分组框外边框 |
| `SC_GroupBoxLabel` | 标题文字区域 |
| `SC_GroupBoxCheckBox` | `checkable` 时标题前的复选框 |
| `SC_GroupBoxContents` | 内容可用区域 |

标题可能会切开边框上沿，复选框又会占用标题左侧空间；这些都依赖当前 style、字体度量、标题对齐、RTL 和 DPI。自定义时不应假设“标题永远从 x=10 开始”。

## 3. `features` 与复选状态是两类不同信息

### 3.1 `features` 只描述边框特征

本类的 `features` 类型是 `QStyleOptionFrame::FrameFeatures`。它来自 `QStyleOptionFrame`，常见相关值为：

```text
QStyleOptionFrame::None
QStyleOptionFrame::Flat
QStyleOptionFrame::Rounded
```

对 group box 而言，`Flat` 反映 `QGroupBox::flat` 的绘制意图：多数 style 会仅画顶部边线或弱化左、右、下边框，以减少视觉占用。但这不是强制像素规范，不同平台 style 的平铺效果可以不同。

`features` **不表示**分组框是否有复选标题，也不表示是否已经勾选。

### 3.2 checkable/checked 进入继承状态

`QGroupBox::checkable` 决定是否在标题位置绘制复选框；`checked` 决定它是否勾选，以及组内子控件默认是否启用。

这两个信息通过 `QStyleOptionComplex` 继承的子控件标志和 `QStyleOption::state` 传给 style，而不是通过本类新增字段：

```text
是否存在复选框  -> subControls 包含 SC_GroupBoxCheckBox
复选框是否勾选  -> state 的 State_On / State_Off
是否可用        -> state 的 State_Enabled
```

要注意 `QGroupBox` 自己在未勾选时并不会被禁用；它仍然可以接收用户操作以重新勾选。手工把整个 group box 画成 disabled，会破坏这个交互。并且虽然可手动重新启用未勾选组框里的单个子控件，Qt 文档不建议这么做，因为会造成出人意料的体验。

## 4. 标准用法：让 style 计算标题与内容区域

```cpp
void AccentGroupBox::paintEvent(QPaintEvent *)
{
    QStyleOptionGroupBox option;
    initStyleOption(&option);

    QStylePainter painter(this);
    painter.drawComplexControl(QStyle::CC_GroupBox, option);

    const QRect titleRect = style()->subControlRect(
        QStyle::CC_GroupBox,
        &option,
        QStyle::SC_GroupBoxLabel,
        this);

    drawTitleAccent(painter, titleRect);
}
```

`initStyleOption()` 会同步标题、标题对齐、边框形态、线宽、文字颜色、复选状态、调色板、字体和布局方向。只有这样，样式系统才能正确处理：

- 标题文字中的 `&` 助记符；
- 可选复选框与标题之间的间距；
- 右对齐或居中标题切开边框的位置；
- RTL 下标题/复选框的相对位置；
- 禁用子控件与仍可点击标题复选框的状态区别。

如果只是想给标题下加一条强调线，应先调用 `drawComplexControl()`，再以 `SC_GroupBoxLabel` 的真实矩形叠加绘制。手工复刻整个边框通常会漏掉标题处的断口。

## 5. 标题相关字段

### 5.1 `text`

`text` 是样式当前要绘制的标题快照，对应 `QGroupBox::title()`。它可以包含 `&` 助记符，例如：

```cpp
groupBox->setTitle("&Connection");
```

真实 `QGroupBox` 会把它作为快捷键，`Alt+C` 可将焦点移到分组框的一个子控件。修改 `option.text` 仅改动本次绘制，并不会创建实际快捷键，也不会改动 `groupBox->title()`。

### 5.2 `textAlignment`

默认是 `Qt::AlignLeft`。对于 `QGroupBox`，通常只需要设置水平对齐：`AlignLeft`、`AlignRight` 或 `AlignHCenter`。尽管类型是完整的 `Qt::Alignment`，不要期待垂直对齐在所有 style 中都有同样效果；组框标题一般由 style 固定在边框上方区域。

### 5.3 `textColor`

默认是无效 `QColor`。这不是“黑色标题”的意思，而是让 style/调色板决定合适文字颜色。手工设置有效颜色会覆盖这次绘制的标题颜色，但要特别注意禁用态、深色主题和高对比度主题：硬编码颜色容易降低可读性。

## 6. 边框字段：不要把当前实现细节当作可配置 API

`lineWidth` 用于面板边线宽度，Qt 6.11.1 文档说明它当前总是 `1`；`midLineWidth` 用于凹陷或凸起边框的中间线，当前总是 `0`。

```text
lineWidth    = 1
midLineWidth = 0
```

它们是绘制数据，不是建议业务代码改成任意粗细的主题 API。若需要稳定的视觉定制，优先由自定义 `QStyle` 定义相应控件绘制，或审慎使用样式表；手改 option 的这两个值只影响一次 style 调用，也未必被每种 style 采用。

## 7. 自定义 style：安全读取并保留基类行为

```cpp
void SectionStyle::drawComplexControl(
    QStyle::ComplexControl control,
    const QStyleOptionComplex *option,
    QPainter *painter,
    const QWidget *widget) const
{
    if (control == QStyle::CC_GroupBox) {
        const auto *group =
            qstyleoption_cast<const QStyleOptionGroupBox *>(option);

        if (group && group->features.testFlag(QStyleOptionFrame::Flat)) {
            drawFlatTopRule(*group, painter);
        }
    }

    QProxyStyle::drawComplexControl(control, option, painter, widget);
}
```

基类指针也可能指向滑块、组合框、滚动条等复杂控件，不能直接 `static_cast`。`Type = SO_GroupBox` 和 `Version = 1` 是 `qstyleoption_cast()` 识别布局的标签。

### 7.1 Qt 6.11.1 离线文档的笔误

本类详细说明的第一句误写为 `QStyleOptionButton contains...`，这里应当理解为 `QStyleOptionGroupBox`。安装头文件和类成员定义可作为实际 API 依据。

## 8. 常见错误

### 8.1 以为 QGroupBox 会替子控件自动布局

症状：组框标题和边框正常，内部控件却全部重叠在左上角。

原因：group box 只是父控件与视觉分组，不是布局管理器。

处理：为它设置 `QVBoxLayout`、`QFormLayout` 等布局。

### 8.2 未勾选时禁用整个 group box

症状：用户无法重新勾选启用分组。

原因：把子控件不可用误解为 group box 本身不可用。

处理：让 `QGroupBox` 管理 checkable/checked，绘制时通过 `state` 区分复选框和内容状态。

### 8.3 固定坐标画标题和复选框

症状：RTL、标题居中、字体变大后文字压住边框或复选框。

原因：忽略 style 对标题区域和边框断口的计算。

处理：使用 `QStyle::SC_GroupBoxLabel`、`SC_GroupBoxCheckBox`、`SC_GroupBoxContents` 获取矩形。

## API 速查表
以下列出 Qt 6.11.1 类文档中 `QStyleOptionGroupBox` 直接声明的类型、构造函数和公开字段。`QStyleOptionComplex` 的子控件状态及 `QStyleOption` 的通用状态不在此表内。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举常量 | `StyleOptionType::Type = SO_GroupBox` | 标识这是分组框 style option。 | 供样式系统与 `qstyleoption_cast()` 识别。 |
| 枚举常量 | `StyleOptionVersion::Version = 1` | 标识本结构版本。 | 普通 style 代码不必手工检查版本。 |
| 构造 | `QStyleOptionGroupBox()` | 创建并以默认值初始化分组框绘制数据。 | 从真实 `QGroupBox` 绘制时，应紧接着调用 `initStyleOption()`。 |
| 构造 | `QStyleOptionGroupBox(const QStyleOptionGroupBox &other)` | 复制另一份分组框绘制状态。 | 是值复制，不拥有组框、布局或子控件。 |
| 公开字段 | `QStyleOptionFrame::FrameFeatures features` | 保存分组框边框特征，例如 `Flat`。 | 不表示可选复选框或勾选状态；后者在继承状态和子控件标志中。 |
| 公开字段 | `int lineWidth` | 保存面板边线宽度。 | Qt 6.11.1 当前为 `1`；不要将它当稳定主题配置接口。 |
| 公开字段 | `int midLineWidth` | 保存凹陷/凸起边框可能用到的中间线宽度。 | Qt 6.11.1 当前为 `0`。 |
| 公开字段 | `QString text` | 保存当前标题文字。 | 修改只影响本次绘制，不会改变真实 title 或快捷键。 |
| 公开字段 | `Qt::Alignment textAlignment` | 指定标题对齐方式。 | 默认左对齐；主要使用水平对齐值。 |
| 公开字段 | `QColor textColor` | 指定标题文字颜色。 | 默认无效颜色，让 style/调色板决定；硬编码时注意禁用与高对比度主题。 |

## 10. 一句话总结

`QStyleOptionGroupBox` 是分组框的绘制契约：边框特征在 `features`，标题内容在 `text` 等字段，可选复选框及其选中状态则由继承的复杂子控件和 `state` 描述；通过 `initStyleOption()` 和 `CC_GroupBox` 才能完整保留 Qt 的标题、边框和交互细节。
