# QStyleOptionMenuItem

> Qt 6.11.1 · Qt Widgets · 来自 `QStyleOptionMenuItem`

## 1. 先建立直觉

`QStyleOptionMenuItem` 是菜单项绘制参数包。它描述菜单项文本、图标、快捷键、是否可勾选、是否选中、是否有子菜单、分隔线等。

菜单项看起来像一行文字，但里面包含图标列、勾选列、文本列、快捷键列、子菜单箭头和分隔线。

## 2. 类说明

`QStyleOptionMenuItem` 继承自 `QStyleOption`。`QMenu` 绘制每个 action 时会把 action 状态转换成这个 option，再交给 style 绘制。

自定义菜单或 style 时，要尽量使用它，避免硬编码各列宽度。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `menuItemType` | 菜单项类型：普通项、分隔线、子菜单、默认项等。 |
| `checkType` | 勾选类型：不可勾选、独占、非独占。 |
| `checked` | 是否勾选。 |
| `menuHasCheckableItems` | 菜单中是否存在可勾选项，影响对齐。 |
| `text` | 菜单文本，可能包含快捷键显示。 |
| `icon` | 菜单项图标。 |
| `maxIconWidth` | 图标列最大宽度。 |
| `reservedShortcutWidth` | 快捷键列预留宽度。 |
| `tabWidth` | 文本中 tab 分隔的宽度。 |
| `QStyle::CE_MenuItem` | 绘制菜单项。 |

## 4. 关键用法

```cpp
QStyleOptionMenuItem opt;
opt.initFrom(menu);
opt.text = action->text();
opt.icon = action->icon();
opt.checked = action->isChecked();
opt.menuItemType = action->menu() ? QStyleOptionMenuItem::SubMenu
                                  : QStyleOptionMenuItem::Normal;

style()->drawControl(QStyle::CE_MenuItem, &opt, painter, menu);
```

## 5. 使用场景

适合自定义菜单、菜单 delegate、style 实现、命令面板里复用菜单外观。

普通应用只需要配置 `QAction`，`QMenu` 会负责构造 option。

## 6. 常见坑与经验

勾选列要按整个菜单统一对齐。只看当前 action 会导致有些行文字错位。

快捷键显示通常和文本用 tab 分隔，style 会按 reserved shortcut width 排版。

分隔线、子菜单、普通 action 应按不同 `menuItemType` 处理，不要都当普通文本行。
