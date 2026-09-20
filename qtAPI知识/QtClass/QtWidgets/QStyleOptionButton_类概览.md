# Qt QStyleOptionButton 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QStyleOptionButton>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QStyleOption -> QStyleOptionButton`  
> 定位：把按钮的文字、图标、按钮类别与实时绘制状态交给 `QStyle` 的轻量数据对象

## 1. 它不是按钮，而是“按钮要怎么画”的说明

`QStyleOptionButton` 没有点击行为、没有 `clicked()` 信号，也不拥有窗口。它是一份临时的绘制状态，供 `QStyle` 画 `QPushButton`、`QCheckBox`、`QRadioButton` 等按钮类控件使用。

```text
QPushButton / QCheckBox / QRadioButton
  └─ initStyleOption(&option)
       ├─ text、icon、iconSize
       ├─ features：按钮属于哪一类
       └─ QStyleOption::state：按下、悬停、禁用、选中等实时状态
            └─ QStyle::drawControl(...)
```

它的价值在于把“控件模型”和“画面”解耦：

- `QAbstractButton` 管理点击、选中、自动重复、快捷键和信号；
- `QStyleOptionButton` 把此刻应该呈现的信息交给样式；
- `QStyle` 按操作系统主题、调色板、DPI 和 RTL 布局完成最终绘制。

普通业务代码使用 `QPushButton`、`QCheckBox` 和 `QRadioButton`。只有自定义控件外观、代理 style 或调试平台样式时才直接构造这个类。

## 2. 最容易混淆的两类信息

### 2.1 `features`：这个按钮是什么类型

`features` 是 `ButtonFeatures` 标志组合，描述相对稳定的按钮类别：

```text
Flat                 -> 扁平按钮
HasMenu              -> 带下拉菜单提示的按钮
DefaultButton        -> 当前对话框的默认按钮
AutoDefaultButton    -> 可随焦点成为默认按钮
CommandLinkButton    -> 命令链接式按钮
```

它影响边框、默认按钮高亮、菜单箭头或命令链接的布局，但不会描述用户此刻是否正在按鼠标。

### 2.2 `state`：此刻处于什么交互状态

`state` 继承自 `QStyleOption`，是另一组位标志。例如 `State_Enabled`、`State_MouseOver`、`State_Sunken`、`State_On`、`State_Off`、`State_NoChange`。

```text
features = Flat                  按钮的长期类别
state    = Enabled + MouseOver   此刻可用且鼠标悬停
```

对复选框的选中、未选中和半选状态，样式主要读取 `State_On`、`State_Off`、`State_NoChange`，不是读取 `features`。对单选框亦然。自定义 style 时如果只看 `features` 而忽略 `state`，通常会画出没有按下态、禁用态或半选态的控件。

## 3. 标准用法：保留平台样式

若你重写 `QPushButton` 的绘制，最稳妥的方式是先让控件自己填好 option，再交给当前 style：

```cpp
void AccentButton::paintEvent(QPaintEvent *)
{
    QStyleOptionButton option;
    initStyleOption(&option);

    QStylePainter painter(this);
    painter.drawControl(QStyle::CE_PushButton, option);

    if (option.state & QStyle::State_MouseOver)
        drawAccentUnderline(painter, option.rect);
}
```

`initStyleOption()` 不只是拷贝 `text` 和 `icon`。它还会填写调色板、字体度量、焦点状态、布局方向、按下状态及按钮特性。手工只填文字与矩形时，常见后果是：

- 默认按钮的视觉强调丢失；
- 高对比度或深色主题下文字颜色不对；
- 图标与文字在 RTL 界面里顺序错误；
- 禁用、悬停和按下状态不连贯。

对于复选框、单选框，要使用与其匹配的 control element，例如 `QStyle::CE_CheckBox` 或 `QStyle::CE_RadioButton`；不要把它们一律当 `CE_PushButton` 绘制。

## 4. `ButtonFeature` 各自解决什么问题

| 特性 | 样式应理解为 | 真实使用场景 |
| --- | --- | --- |
| `None` | 普通按钮，没有额外类别提示 | “确定”“保存”等常规按钮 |
| `Flat` | 默认不应呈现普通凸起按钮的边框效果 | 工具栏、嵌入式操作区 |
| `HasMenu` | 按钮附带可展开菜单，应为菜单指示符预留空间 | `QPushButton::setMenu()` |
| `DefaultButton` | 当前对话框中 Enter 默认触发的主操作 | “确定”“继续安装” |
| `AutoDefaultButton` | 能够根据焦点成为默认操作的按钮 | `QDialog` 中的普通 `QPushButton` |
| `CommandLinkButton` | 命令链接式按钮，需要不同的图标和文本层级布局 | 引导式设置页中的大操作入口 |

`ButtonFeatures` 是 `QFlags<ButtonFeature>`，可以按位组合。例如一个带菜单的扁平按钮可以同时拥有 `Flat` 和 `HasMenu`。不过不要为了“看起来像”就手工乱组合：option 最好由真实控件的 `initStyleOption()` 产生，保证绘制提示与控件行为一致。

`DefaultButton` 与 `AutoDefaultButton` 的区别尤其重要：前者表示它**当前已经是**默认按钮；后者表示它**具有自动成为**默认按钮的能力。前者通常应有更强的视觉提示。

## 5. 文字、图标和尺寸

`text`、`icon`、`iconSize` 是同一次绘制的内容输入：

```cpp
QStyleOptionButton option;
button->initStyleOption(&option);

// option.text      -> “保存”
// option.icon      -> 保存图标
// option.iconSize  -> style 或控件选择的目标尺寸
```

它们不是控件属性的反向通道。修改：

```cpp
option.text = "重新连接";
```

只会改变随后以 `option` 调用 `drawControl()` 的那一帧画面，不会调用 `button->setText()`。

`iconSize` 默认是无效的 `QSize(-1, -1)`，这意味着尚未指定目标尺寸，style 可以自行决定合适大小。要让实际按钮持久使用某个图标尺寸，应设置控件的图标尺寸；在 option 上硬写尺寸适合一次性的自定义绘制，不适合替代控件状态。

## 6. 自定义 QProxyStyle 时如何安全读取

`drawControl()` 接收的是 `const QStyleOption *`，可能对应许多控件。先检查 control element，再用 `qstyleoption_cast()`：

```cpp
void DialogStyle::drawControl(QStyle::ControlElement element,
                              const QStyleOption *option,
                              QPainter *painter,
                              const QWidget *widget) const
{
    if (element == QStyle::CE_PushButton) {
        const auto *button =
            qstyleoption_cast<const QStyleOptionButton *>(option);

        if (button && button->features.testFlag(
                          QStyleOptionButton::DefaultButton)) {
            drawDefaultHalo(*button, painter);
        }
    }

    QProxyStyle::drawControl(element, option, painter, widget);
}
```

不要把基类指针直接 `static_cast` 为 `QStyleOptionButton *`。`Type = SO_Button` 和 `Version = 1` 是 `qstyleoption_cast()` 判断 option 布局的依据，普通代码无须自行比较。

## 7. 常见错误

### 7.1 用 `features` 判断复选框是否选中

症状：复选框永远显示同一种勾选状态。

原因：`features` 描述按钮种类，不记录 check state。

处理：读取继承的 `option.state` 中的 `State_On`、`State_Off`、`State_NoChange`。

### 7.2 只把按钮画成“漂亮的静态图片”

症状：悬停、键盘焦点、按下、禁用后都没有视觉反馈。

原因：没有把 `state`、`palette` 和 `style` 的行为纳入绘制。

处理：优先 `initStyleOption()` 加 `drawControl()`，再在其基础上叠加少量定制。

### 7.3 修改 option 后期待按钮行为改变

症状：把 `HasMenu` 写进 `features`，但点击并没有弹出菜单。

原因：option 只描述当前绘制；菜单的创建、归属和触发仍由 `QPushButton` 及其 `QMenu` 管理。

处理：通过控件 API 配置真实行为，让 option 自然反映该行为。

## API 速查表
以下是 Qt 6.11.1 类文档中 `QStyleOptionButton` 直接声明的类型、构造函数和公开字段。继承自 `QStyleOption` 的 `state`、`rect`、`palette` 等通用绘制状态不在此表内。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举值 | `ButtonFeature::None = 0x00` | 标记普通按钮，没有额外功能提示。 | 可与其他 feature 组合时以位标志语义理解。 |
| 枚举值 | `ButtonFeature::Flat = 0x01` | 标记扁平按钮。 | 只影响 style 的视觉决策，不改变点击行为。 |
| 枚举值 | `ButtonFeature::HasMenu = 0x02` | 标记按钮带下拉菜单。 | 只提供菜单指示的绘制信息，真实菜单仍由控件管理。 |
| 枚举值 | `ButtonFeature::DefaultButton = 0x04` | 标记当前默认按钮。 | 应与 `AutoDefaultButton` 区分；它表示当前状态而非资格。 |
| 枚举值 | `ButtonFeature::AutoDefaultButton = 0x08` | 标记可自动成为默认按钮。 | 常见于对话框按钮，焦点变化可影响最终默认状态。 |
| 枚举值 | `ButtonFeature::CommandLinkButton = 0x10` | 标记命令链接式按钮。 | style 可据此使用不同的图标、标题和说明文字布局。 |
| 标志类型 | `ButtonFeatures` | 保存多个 `ButtonFeature` 的按位组合。 | 用 `testFlag()` 查询，避免把组合值当单一枚举比较。 |
| 枚举常量 | `StyleOptionType::Type = SO_Button` | 标记这是按钮 style option。 | 供 `qstyleoption_cast()` 和样式系统识别。 |
| 枚举常量 | `StyleOptionVersion::Version = 1` | 标记本结构版本。 | 普通 style 代码不需要手动检查。 |
| 构造 | `QStyleOptionButton()` | 创建并以默认值初始化 option。 | 默认图标和文字为空；从真实控件绘制时应接着调用 `initStyleOption()`。 |
| 构造 | `QStyleOptionButton(const QStyleOptionButton &other)` | 复制一份按钮绘制状态。 | 是值复制，不拥有也不复制实际按钮。 |
| 公开字段 | `ButtonFeatures features` | 保存描述按钮类别的 feature 标志。 | 不保存悬停、按下和选中状态，那些在基类 `state` 中。 |
| 公开字段 | `QIcon icon` | 保存本帧要绘制的图标。 | 默认是空图标；修改它不改变控件的 `icon` 属性。 |
| 公开字段 | `QSize iconSize` | 保存图标目标尺寸。 | 默认无效尺寸；无效时 style 可自行选择尺寸。 |
| 公开字段 | `QString text` | 保存本帧要绘制的标签文字。 | 修改它只影响这次绘制，不会调用控件的 `setText()`。 |

## 9. 一句话总结

`QStyleOptionButton` 是按钮控件与平台样式之间的一份绘制契约：`features` 说明按钮属于什么类别，继承的 `state` 说明它此刻处于什么交互状态，文字和图标则给样式提供实际内容。
