# QStyleOptionTabBarBase

> Qt 6.11.1 · Qt Widgets · 来自 `QStyleOptionTabBarBase`

## 1. 先建立直觉

`QStyleOptionTabBarBase` 描述 tab bar 的底座区域。它不是单个 tab，而是标签条和页面框架之间那条基础线/背景。

当 `QTabBar` 需要绘制 base，style 会用它理解 tab bar 形状、当前选中 tab 区域和文档模式。

## 2. 类说明

`QStyleOptionTabBarBase` 继承自 `QStyleOption`。它包含 `shape`、`tabBarRect`、`selectedTabRect`、`documentMode` 等字段。

单个 tab 用 `QStyleOptionTab`；整个 tab widget frame 用 `QStyleOptionTabWidgetFrame`；base 则处在中间层。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `shape` | tab bar 形状和方向。 |
| `tabBarRect` | tab bar 整体矩形。 |
| `selectedTabRect` | 当前选中 tab 的矩形。 |
| `documentMode` | 是否文档模式。 |
| `QStyle::PE_FrameTabBarBase` | 绘制 tab bar base 的 primitive。 |

## 4. 关键用法

```cpp
QStyleOptionTabBarBase opt;
opt.initFrom(tabBar);
opt.shape = tabBar->shape();
opt.tabBarRect = tabBar->rect();
opt.selectedTabRect = tabBar->tabRect(tabBar->currentIndex());

style()->drawPrimitive(QStyle::PE_FrameTabBarBase, &opt, painter, tabBar);
```

## 5. 使用场景

适合自定义 tab bar、style 实现、文档标签条外观调整。

如果只是调整 tab 文本、图标、关闭按钮，通常不需要直接使用它。

## 6. 常见坑与经验

base 和 tab shape 要一致。顶部 tab、底部 tab、侧边 tab 的底座线位置不同。

documentMode 会改变视觉密度和边框感，尤其在 macOS/IDE 风格界面中明显。

选中 tab 区域会影响 base 是否在某段断开或衔接。
