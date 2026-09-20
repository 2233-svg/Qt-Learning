# QStyleOptionToolButton

> Qt 6.11.1 · Qt Widgets · 来自 `QStyleOptionToolButton`

## 1. 先建立直觉

`QStyleOptionToolButton` 是工具按钮绘制参数包。工具按钮常出现在工具栏里，可能只有图标，也可能有文字、箭头、下拉菜单或 split-button 行为。

它比普通 button option 更关注工具栏场景和菜单弹出模式。

## 2. 类说明

`QStyleOptionToolButton` 继承自 `QStyleOptionComplex`。它描述 icon、text、toolButtonStyle、arrowType、features、popupMode 等。

style 使用它绘制 `QStyle::CC_ToolButton`，并区分主按钮区域和菜单区域。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `icon` / `iconSize` | 工具按钮图标和尺寸。 |
| `text` | 工具按钮文字。 |
| `toolButtonStyle` | 图标/文字组合方式。 |
| `arrowType` | 箭头按钮类型。 |
| `features` | 是否有菜单、箭头、弹出延迟等特性。 |
| `popupMode` | 菜单弹出模式。 |
| `pos` | 鼠标位置相关字段。 |
| `font` | 绘制文字使用的字体。 |
| `QStyle::CC_ToolButton` | 绘制工具按钮。 |
| `QStyle::SC_ToolButton` | 主按钮子控件。 |
| `QStyle::SC_ToolButtonMenu` | 菜单子控件。 |

## 4. 关键用法

```cpp
QStyleOptionToolButton opt;
opt.initFrom(this);
opt.icon = icon();
opt.iconSize = iconSize();
opt.text = text();
opt.toolButtonStyle = toolButtonStyle();
opt.popupMode = popupMode();

QStylePainter p(this);
p.drawComplexControl(QStyle::CC_ToolButton, opt);
```

## 5. 使用场景

适合自定义 `QToolButton`、工具栏按钮、带下拉菜单的工具按钮、style 实现。

普通工具按钮只需要配置 `QToolButton` 的 icon、text、popupMode、defaultAction。

## 6. 常见坑与经验
工具按钮菜单区域和主按钮区域可能不同。split button 行为必须用 sub-control 命中测试处理。

`toolButtonStyle` 可能来自应用或工具栏统一设置，不要只按图标按钮假设。

箭头按钮不一定有普通 icon；`arrowType` 和 `features` 要配合判断。
