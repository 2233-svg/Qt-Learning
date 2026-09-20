# QStyleOptionToolBar

> Qt 6.11.1 · Qt Widgets · 来自 `QStyleOptionToolBar`

## 1. 先建立直觉

`QStyleOptionToolBar` 是工具栏绘制参数包。它告诉 style 工具栏在主窗口区域中的位置、方向、相邻关系以及是否可移动。

工具栏的外观不只取决于水平/垂直，还取决于它是独占一行、在开头/中间/末尾、是否有拖拽 handle。

## 2. 类说明

`QStyleOptionToolBar` 继承自 `QStyleOption`。它包含 `positionOfLine`、`positionWithinLine`、`toolBarArea`、`features`、`lineWidth`、`midLineWidth` 等字段。

style 用这些信息绘制工具栏背景、分隔和拖动手柄。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `toolBarArea` | 工具栏所在区域：上、下、左、右。 |
| `positionOfLine` | 该工具栏所在行相对其他行的位置。 |
| `positionWithinLine` | 该工具栏在当前行内的位置。 |
| `features` | 工具栏特性，如 movable。 |
| `lineWidth` / `midLineWidth` | 边线相关宽度。 |
| `QStyle::CE_ToolBar` | 绘制工具栏。 |
| `QStyle::PE_IndicatorToolBarHandle` | 绘制拖动手柄。 |
| `QStyle::PE_IndicatorToolBarSeparator` | 绘制分隔符。 |

## 4. 关键用法

```cpp
QStyleOptionToolBar opt;
opt.initFrom(toolBar);
opt.toolBarArea = Qt::TopToolBarArea;
opt.features = QStyleOptionToolBar::Movable;

style()->drawControl(QStyle::CE_ToolBar, &opt, painter, toolBar);
```

## 5. 使用场景

适合自定义工具栏、主窗口框架 style、专业软件工具区外观统一。

普通 `QToolBar` 使用者主要通过 actions、icon size、movable、allowed areas 等 API 配置。

## 6. 常见坑与经验

工具栏在不同行/不同区域的边缘绘制不同。硬画一条矩形背景容易和主窗口 dock 区域不协调。

可移动工具栏需要明确手柄区域，否则用户不知道哪里能拖。

工具栏里按钮的绘制通常由 `QStyleOptionToolButton` 负责，不是这个 option。
