# QStyleOptionToolBox

> Qt 6.11.1 · Qt Widgets · 来自 `QStyleOptionToolBox`

## 1. 先建立直觉

`QStyleOptionToolBox` 是 `QToolBox` 页签绘制参数包。ToolBox 像折叠分类面板，每一页的 tab 需要文字、图标、位置和选中状态。

它关注的是页签，不是页内容。

## 2. 类说明

`QStyleOptionToolBox` 继承自 `QStyleOption`。它包含 `text`、`icon`、`position`、`selectedPosition` 等字段。

style 用它绘制 toolbox tab 的背景、标签和相邻边界。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `text` | 页签文字。 |
| `icon` | 页签图标。 |
| `position` | 页签在序列中的位置：开始、中间、结束、唯一。 |
| `selectedPosition` | 与当前选中页签的相邻关系。 |
| `QStyle::CE_ToolBoxTab` | 绘制完整 toolbox 页签。 |
| `QStyle::CE_ToolBoxTabShape` | 绘制页签形状。 |
| `QStyle::CE_ToolBoxTabLabel` | 绘制页签标签。 |

## 4. 关键用法

```cpp
QStyleOptionToolBox opt;
opt.initFrom(toolBox);
opt.text = toolBox->itemText(index);
opt.icon = toolBox->itemIcon(index);

style()->drawControl(QStyle::CE_ToolBoxTab, &opt, painter, toolBox);
```

## 5. 使用场景

适合自定义 `QToolBox`、设置页分类面板、style 实现、需要平台一致折叠页签外观的控件。

如果只是普通标签页切换，用 `QTabWidget` 更常见；ToolBox 更适合纵向分类。

## 6. 常见坑与经验

position 和 selectedPosition 会影响边框衔接。忽略它们会出现重复线或圆角不连续。

ToolBox 页签不等同于 TabBar tab，二者有不同 style element 和 option。

内容页的布局由对应 widget 自己管理，不由这个 option 表达。
