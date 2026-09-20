# Qt QStyleOptionFrame 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 与安装头文件整理）  
> 头文件：`#include <QStyleOptionFrame>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QStyleOption -> QStyleOptionFrame`  
> 定位：把边框形状、线宽和外观提示传给 `QStyle` 的通用 frame 绘制数据

## 1. 它不是 QFrame，而是一份边框绘制快照

`QStyleOptionFrame` 不显示控件，也不设置布局边距，更不会保存 widget 的长期边框配置。它是一次绘制时交给 `QStyle` 的数据对象。

Qt 用它绘制多种内建控件的 frame，包括：

```text
QFrame
QGroupBox
QLineEdit
QMenu
以及需要 frame primitive 的其他控件
```

典型调用方向是：

```text
真实控件的属性
  └─ initStyleOption(&option)
       └─ QStyleOptionFrame
            └─ QStyle::drawPrimitive(PE_Frame... )
                或 QStyle::drawControl(CE_ShapedFrame, ...)
```

它的意义是：控件提供“我要画什么类型的框、线多宽、当前是否凹陷”等语义，具体的颜色、像素、阴影和平台习惯由当前 style 决定。

普通代码想给控件加框，应使用控件自己的 API，例如 `QFrame::setFrameShape()`、`setFrameStyle()`、`QLineEdit::setFrame()` 或样式表。直接改 option 字段只影响随后发生的一次 style 绘制。

## 2. 框的“形状”“额外特征”“实时状态”是三件事

这三个来源经常被混淆。

### 2.1 `frameShape`：框的基本类别

`frameShape` 的类型为 `QFrame::Shape`，表示基本外形：

```text
NoFrame       不画框
Box           矩形盒子
Panel         矩形面板
StyledPanel   随当前 GUI style 呈现的面板
HLine/VLine   水平或垂直分隔线
WinPanel      兼容旧 Windows 面板效果
```

例如，`HLine` 与 `VLine` 的语义不是“缩窄的矩形边框”，而是没有内容的分隔线。`StyledPanel` 的目标是交给 style 选择合适外观，通常比兼容性用途的 `WinPanel` 更适合新代码。

### 2.2 `features`：附加绘制提示

`features` 是 `FrameFeatures` 位标志，可组合：

| feature | 表示什么 |
| --- | --- |
| `None` | 普通 frame，没有额外提示 |
| `Flat` | 平面化 frame 提示 |
| `Rounded` | 圆角 frame 提示 |

这不是样式表意义上的完整 border-radius 系统。`Rounded` 只是传给 style 的语义标志；某个 style 可以采用、弱化或在特定控件上忽略它。若产品视觉要求在所有平台都呈现固定圆角，应由自己的 style 或明确的样式表体系负责，而不是假定这个 flag 有像素级保证。

### 2.3 `state`：这一帧的实时互动状态

`state` 继承自 `QStyleOption`。例如 frame primitive 的 style 契约会用 `QStyle::State_Sunken` 表示凹陷 frame。

```text
frameShape = StyledPanel      -> 这是什么形状
features = Rounded            -> 额外外观提示
state = State_Sunken          -> 当前要以凹陷状态画
```

`QStyleOptionFrame` 没有独立的 `shadow` 字段。真实 `QFrame` 的 `Raised`、`Sunken` 等阴影概念，应让 `QFrame::initStyleOption()` 连同继承状态一起填写；手工绘制时只设置 `frameShape` 而忽略 `state`，可能画不出正确的凹陷效果。

## 3. 标准用法：从真实 QFrame 初始化

```cpp
void AccentFrame::paintEvent(QPaintEvent *)
{
    QStyleOptionFrame option;
    initStyleOption(&option);

    QStylePainter painter(this);
    painter.drawControl(QStyle::CE_ShapedFrame, option);

    if (option.features.testFlag(QStyleOptionFrame::Rounded))
        drawCornerAccent(painter, option.rect);
}
```

`initStyleOption()` 会填充：

- `frameShape`、`lineWidth`、`midLineWidth`、frame feature；
- 继承的 `rect`、`palette`、`direction`、`state`、字体度量等；
- 从实际控件得到的凹陷、启用、焦点和布局方向信息。

只手工填一个 `QRect` 和线宽，往往会在深色主题、禁用态、RTL 布局或高 DPI 下偏离当前平台风格。

根据要画的元素，style 可能使用 `PE_Frame`、`PE_FrameLineEdit`、`PE_FrameMenu`、`PE_FrameGroupBox` 等 primitive，也可能使用 `CE_ShapedFrame`。应匹配真实控件所使用的 element，不要把所有 frame 一律画成 `PE_Frame`。

## 4. 线宽不是边距，也不是最终 frameWidth

### 4.1 `lineWidth`

`lineWidth` 是边框主线的宽度，默认 `0`。它是绘制参数，并不自动等于控件最终占用的外边距。

### 4.2 `midLineWidth`

`midLineWidth` 是凹陷或凸起框可能使用的中间额外线宽，默认 `0`。在 `QFrame` 的语义中，它主要对 raised/sunken 的 `Box`、`HLine`、`VLine` 等样式有意义，借助调色板中间色形成传统 3D 效果。

### 4.3 `frameWidth`

真实 `QFrame::frameWidth()` 是由 frame style 决定的最终可见宽度，不能简单理解成：

```text
frameWidth == lineWidth + midLineWidth
```

例如 `NoFrame` 的最终 frame width 为 0，而 `Panel` 与分隔线的计算又有各自的 style 规则。要设置控件内容与边框的间距，应使用 `QWidget::setContentsMargins()` 或布局 margins，不要改 option 的线宽来“挤出空间”。

## 5. `FrameFeatures` 与 `QFrame::Shape` 的实际组合

| 目标 | 更合适的真实控件配置 | option 中可能看到的结果 |
| --- | --- | --- |
| 普通分隔线 | `QFrame::HLine` / `VLine` | `frameShape` 为线形状 |
| 跟随平台的面板 | `QFrame::StyledPanel` | style 根据 shape、palette、state 绘制 |
| 传统凹陷输入槽 | 对应控件/`QFrame` 设置 Sunken | shape 配合 `State_Sunken` |
| 分组框的弱化边线 | `QGroupBox::setFlat(true)` | group box option 的 `features` 包含 `Flat` |
| 一次性自定义圆角提示 | 自定义 style 中设置 `Rounded` | 是否呈现圆角由 style 决定 |

不要因为 `features` 中包含 `Flat` 就把 `frameShape` 改成 `NoFrame`。前者通常表示仍有 frame 语义、但视觉更弱；后者是明确不绘制 frame。

## 6. 自定义 style：安全地读取 option

```cpp
void SoftFrameStyle::drawControl(QStyle::ControlElement element,
                                 const QStyleOption *option,
                                 QPainter *painter,
                                 const QWidget *widget) const
{
    if (element == QStyle::CE_ShapedFrame) {
        const auto *frame =
            qstyleoption_cast<const QStyleOptionFrame *>(option);

        if (frame && frame->features.testFlag(QStyleOptionFrame::Rounded)) {
            drawRoundedFrame(*frame, painter);
            return;
        }
    }

    QProxyStyle::drawControl(element, option, painter, widget);
}
```

`QStyle` 绘制函数接收的是基类 `QStyleOption *`。必须用 `qstyleoption_cast()` 先检查类型；不要将 line edit、菜单或焦点矩形的 option 直接 `static_cast` 为 `QStyleOptionFrame`。

`Type = SO_Frame` 与 `Version = 1` 是安全转换使用的运行时标签。

### 6.1 Qt 6.11.1 文档与头文件的版本不一致

Qt 6.11.1 离线页面的详细说明写着 “version 3”，枚举表的描述列也写 `3`；但该版本安装头文件声明 `QStyleOptionFrame::Version = 1`。编译代码时应以实际使用的 Qt 头文件为准，不能将文档说明段中的 `3` 写死。

## 7. 常见错误

### 7.1 把 `Rounded` 当作跨 style 的圆角保证

症状：在一个主题圆角正常，换主题后变成直角或效果变化。

原因：它是 style feature，不是强制绘制协议。

处理：视觉必须固定时在自己的 style 或样式表体系里明确实现；想保持平台一致则交给 style。

### 7.2 调大 `lineWidth` 来增加内容留白

症状：边框变粗，内容位置却不符合预期。

原因：边线厚度和 layout/content margins 是不同层次。

处理：用 `setContentsMargins()` 或布局边距控制内容区域。

### 7.3 手工 option 缺少 `State_Sunken`

症状：希望画凹陷输入槽，结果像普通平面框。

原因：只填了 `frameShape`，没有同步继承的实时 state。

处理：从真实控件调用 `initStyleOption()`，或明确按目标 primitive 的 state 契约配置。

## API 速查表
以下列出 Qt 6.11.1 类文档中 `QStyleOptionFrame` 直接声明的类型、构造函数和公开字段。继承自 `QStyleOption` 的 `rect`、`palette`、`state` 等通用绘制状态不在此表内。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举值 | `FrameFeature::None = 0x00` | 表示普通 frame，没有额外 feature。 | 是默认语义，可与其他 feature 的空组合对照理解。 |
| 枚举值 | `FrameFeature::Flat = 0x01` | 提示 style 以平面化形式绘制 frame。 | 不等于 `NoFrame`，具体视觉由 style 决定。 |
| 枚举值 | `FrameFeature::Rounded = 0x02` | 提示 style 以圆角 frame 呈现。 | 不是跨平台强制的 border-radius。 |
| 标志类型 | `FrameFeatures` | 保存多个 `FrameFeature` 的按位组合。 | 用 `testFlag()` 查询；不要把组合值当作单个枚举。 |
| 枚举常量 | `StyleOptionType::Type = SO_Frame` | 标识这是 frame style option。 | 供 `qstyleoption_cast()` 和样式系统识别。 |
| 枚举常量 | `StyleOptionVersion::Version = 1` | 标识本结构版本。 | 以编译所用头文件为准；离线页有 version 3 的不一致文字。 |
| 构造 | `QStyleOptionFrame()` | 创建并以默认值初始化 frame 绘制数据。 | 默认线宽和中线宽均为 0；通常应从真实控件初始化。 |
| 构造 | `QStyleOptionFrame(const QStyleOptionFrame &other)` | 复制一份 frame 绘制状态。 | 是值复制，不拥有控件。 |
| 公开字段 | `FrameFeatures features` | 保存 flat、rounded 等外观提示。 | 是样式输入，不保存控件的所有边框行为。 |
| 公开字段 | `QFrame::Shape frameShape` | 保存 frame 的基本形状。 | 与 `features` 和继承的 `state` 分工不同。 |
| 公开字段 | `int lineWidth` | 保存主边线宽度。 | 不等于布局边距，也不必等于最终 `frameWidth()`。 |
| 公开字段 | `int midLineWidth` | 保存凹陷/凸起 frame 的中间附加线宽。 | 通常只对某些 raised/sunken `QFrame` shape 有意义。 |

## 9. 一句话总结

`QStyleOptionFrame` 是通用边框的绘制契约：`frameShape` 说明基本形状，`features` 提供 flat/rounded 等提示，继承的 `state` 表示凹陷与实时状态；真实边框配置交给控件 API，最终像素外观交给当前 `QStyle`。
