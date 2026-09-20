# QStyleOptionTab

> Qt 6.11.1 · Qt Widgets · 来自 `QStyleOptionTab`

## 1. 先建立直觉

`QStyleOptionTab` 是单个标签页 tab 的绘制参数包。它描述 tab 的文字、图标、形状、位置、是否选中、左右按钮和相邻 tab 状态。

Tab 的外观非常依赖上下文：第一个、中间、最后一个、唯一一个、旁边是否选中，都会影响边框和圆角。

## 2. 类说明

`QStyleOptionTab` 继承自 `QStyleOption`。`QTabBar` 绘制每个 tab 时会构造它，style 使用它绘制 `CE_TabBarTab`、`CE_TabBarTabShape`、`CE_TabBarTabLabel`。

它不管理页面，只描述标签条上的一个标签。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `text` | tab 文本。 |
| `icon` / `iconSize` | tab 图标和尺寸。 |
| `shape` | tab 形状和方向。 |
| `position` | tab 在连续区间中的位置。 |
| `selectedPosition` | 与选中 tab 的相邻关系。 |
| `cornerWidgets` | 角落 widget 情况。 |
| `leftButtonSize` / `rightButtonSize` | tab 左右按钮尺寸，如关闭按钮。 |
| `row` | 多行 tab 中所在行。 |
| `documentMode` | 是否文档模式。 |
| `QStyle::CE_TabBarTab` | 绘制完整 tab。 |

## 4. 关键用法

```cpp
QStyleOptionTab opt;
tabBar->initStyleOption(&opt, index);

QStylePainter p(tabBar);
p.drawControl(QStyle::CE_TabBarTab, opt);
```

通常让 `QTabBar::initStyleOption()` 填充它，比手动拼字段更可靠。

## 5. 使用场景

适合自定义 `QTabBar`、浏览器式标签、文档标签、style 实现。

普通使用 `QTabWidget` / `QTabBar` 时，只设置 tab text、icon、closable 等即可。

## 6. 常见坑与经验

不要忽略相邻关系。选中 tab 与旁边 tab 的边界通常需要特殊处理。

关闭按钮尺寸会影响 label 区域。自定义 tab 绘制时要给左右按钮留空间。

不同 shape 意味着 tab 可能在上、下、左、右，文本和图标布局不能只按顶部 tab 假设。
