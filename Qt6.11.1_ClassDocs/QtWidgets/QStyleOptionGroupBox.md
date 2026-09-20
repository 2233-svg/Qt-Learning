# QStyleOptionGroupBox

> Qt 6.11.1 · Qt Widgets · 来自 `QStyleOptionGroupBox`

## 1. 先建立直觉

`QStyleOptionGroupBox` 是分组框绘制参数包。它描述 `QGroupBox` 的标题、标题对齐、是否可勾选、勾选状态、边框线宽和子控件区域。

GroupBox 看似只是一个框加标题，但标题位置、复选框指示器、内容边距都由 style 决定。

## 2. 类说明

`QStyleOptionGroupBox` 继承自 `QStyleOptionComplex`。它包含 `text`、`textAlignment`、`features`、`lineWidth`、`midLineWidth` 等字段。

因为 group box 可带复选框，所以它也会涉及子控件命中和绘制。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `text` | 分组标题。 |
| `textAlignment` | 标题对齐。 |
| `features` | 是否 flat、checkable 等特性。 |
| `lineWidth` / `midLineWidth` | 边框线宽。 |
| `subControls` / `activeSubControls` | 复杂控件子区域状态。 |
| `QStyle::CC_GroupBox` | 绘制完整 group box。 |
| `QStyle::SC_GroupBoxFrame` | 边框子控件。 |
| `QStyle::SC_GroupBoxLabel` | 标题子控件。 |
| `QStyle::SC_GroupBoxCheckBox` | 复选框子控件。 |
| `QStyle::State_On/Off` | 勾选状态。 |

## 4. 关键用法

```cpp
QStyleOptionGroupBox opt;
opt.initFrom(groupBox);
opt.text = groupBox->title();
opt.textAlignment = groupBox->alignment();
opt.lineWidth = 1;
opt.subControls = QStyle::SC_GroupBoxFrame | QStyle::SC_GroupBoxLabel;

if (groupBox->isCheckable()) {
    opt.subControls |= QStyle::SC_GroupBoxCheckBox;
    opt.state |= groupBox->isChecked() ? QStyle::State_On : QStyle::State_Off;
}

style()->drawComplexControl(QStyle::CC_GroupBox, &opt, painter, groupBox);
```

## 5. 使用场景

适合自定义 group box、设置页分区、style 实现、需要平台一致分组框视觉的复合控件。

如果只是视觉分隔，简单标题加布局留白有时比 group box 更现代。

## 6. 常见坑与经验

可勾选 group box 的 checked 状态要进入 option state，否则指示器会错。

标题会占用 frame 区域。内容布局边距不能只按普通矩形框计算。

flat group box 与普通 group box 的边框期望不同，不要忽略 features。
