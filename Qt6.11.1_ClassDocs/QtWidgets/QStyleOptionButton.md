# QStyleOptionButton

> Qt 6.11.1 · Qt Widgets · 来自 `QStyleOptionButton`

## 1. 先建立直觉

`QStyleOptionButton` 是按钮类控件交给 `QStyle` 的绘制参数包。`QPushButton`、`QCheckBox`、`QRadioButton` 等都需要描述文字、图标、按钮特性和勾选状态。

它不是按钮控件，只是“当前这个按钮应该怎么被画”的快照。

## 2. 类说明

`QStyleOptionButton` 继承自 `QStyleOption`。它增加 `features`、`text`、`icon`、`iconSize` 等字段。按钮按下、禁用、悬停、获得焦点这类通用状态仍放在 `state` 中。

style 会根据这些字段决定绘制普通按钮、默认按钮、扁平按钮、命令链接按钮、复选/单选指示器等。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `features` | 按钮特性，如默认按钮、auto default、flat、command link。 |
| `text` | 按钮显示文本。 |
| `icon` | 按钮图标。 |
| `iconSize` | 图标尺寸。 |
| `ButtonFeature` | 描述按钮特殊外观和语义的标志。 |
| `QStyle::CE_PushButton` | 绘制完整 push button。 |
| `QStyle::CE_CheckBox` | 绘制 checkbox。 |
| `QStyle::CE_RadioButton` | 绘制 radio button。 |
| `QStyle::State_On/Off/NoChange` | 勾选状态通常放在 `state` 中。 |

## 4. 关键用法

```cpp
QStyleOptionButton opt;
opt.initFrom(this);
opt.text = text();
opt.icon = icon();
opt.iconSize = iconSize();
if (isDefault())
    opt.features |= QStyleOptionButton::DefaultButton;

QStylePainter p(this);
p.drawControl(QStyle::CE_PushButton, opt);
```

复选状态：

```cpp
opt.state |= checked ? QStyle::State_On : QStyle::State_Off;
```

## 5. 使用场景

适合自定义按钮、按钮 delegate、style 实现、复用平台按钮绘制。

如果只是设置普通按钮属性，直接操作 `QAbstractButton` 子类即可，不需要手写 option。

## 6. 常见坑与经验

按钮文字、图标和状态要同时填。只设置 text，style 不知道默认按钮、按下状态或图标信息。

默认按钮和 auto default 影响尺寸和外观，尤其在对话框中很明显。

复选框/单选框的 checked 状态属于 `state`，不是 `features`。
