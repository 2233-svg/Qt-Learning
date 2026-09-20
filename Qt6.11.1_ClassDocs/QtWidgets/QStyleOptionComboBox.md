# QStyleOptionComboBox

> Qt 6.11.1 · Qt Widgets · 来自 `QStyleOptionComboBox`

## 1. 先建立直觉

`QStyleOptionComboBox` 是组合框绘制参数包。它告诉 style 当前 combo box 的文本、图标、是否可编辑、弹出框区域、frame 状态等。

组合框是复杂控件：外框、下拉箭头、编辑区域/显示区域都可能分别绘制和命中。

## 2. 类说明

`QStyleOptionComboBox` 继承自 `QStyleOptionComplex`。它用于 `QStyle::CC_ComboBox` 绘制，也可配合 `subControlRect()` 获取箭头和编辑区域。

自定义 combo box 或 delegate 中想复用平台绘制时，用它比手动画边框和箭头可靠。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `editable` | 是否是可编辑组合框。 |
| `frame` | 是否绘制 frame。 |
| `currentText` | 当前显示文本。 |
| `currentIcon` | 当前显示图标。 |
| `iconSize` | 图标尺寸。 |
| `popupRect` | 下拉弹出区域相关矩形。 |
| `subControls` | 常包含 frame、arrow、edit field 等子控件。 |
| `activeSubControls` | 当前 hover/pressed 的子控件。 |
| `QStyle::CC_ComboBox` | 绘制组合框 complex control。 |
| `QStyle::SC_ComboBoxArrow` | 下拉箭头子控件。 |
| `QStyle::SC_ComboBoxEditField` | 文本/编辑区域子控件。 |

## 4. 关键用法

```cpp
QStyleOptionComboBox opt;
opt.initFrom(this);
opt.editable = isEditable();
opt.currentText = currentText();
opt.currentIcon = itemIcon(currentIndex());
opt.iconSize = iconSize();
opt.frame = true;

QStylePainter p(this);
p.drawComplexControl(QStyle::CC_ComboBox, opt);
p.drawControl(QStyle::CE_ComboBoxLabel, opt);
```

查询编辑区域：

```cpp
QRect field = style()->subControlRect(QStyle::CC_ComboBox, &opt,
                                      QStyle::SC_ComboBoxEditField, this);
```

## 5. 使用场景

适合自定义 combo box、复合选择控件、style 实现、需要按平台规则画下拉按钮的控件。

普通使用 `QComboBox` 时不需要直接接触它。

## 6. 常见坑与经验

只画 `CC_ComboBox` 可能没有文字标签；很多 style 需要再画 `CE_ComboBoxLabel`。

editable 会影响内部区域和外观。自定义绘制时不要忽略。

下拉 popup 本身不是这个 option 负责，它只描述组合框主体。
