# QStyleOptionTitleBar

> Qt 6.11.1 · Qt Widgets · 来自 `QStyleOptionTitleBar`

## 1. 先建立直觉

`QStyleOptionTitleBar` 是标题栏绘制参数包。它描述窗口标题、图标、窗口状态、可用按钮，以及当前活动的标题栏子控件。

它常用于 MDI 子窗口、自绘窗口壳、style 实现中的标题栏绘制。

## 2. 类说明

`QStyleOptionTitleBar` 继承自 `QStyleOptionComplex`。标题栏是复杂控件，包含系统菜单、最小化、最大化、关闭、上下文帮助等子控件。

style 使用它绘制 `QStyle::CC_TitleBar`，并通过 sub-control 计算按钮区域和命中结果。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `text` | 标题文字。 |
| `icon` | 窗口图标。 |
| `titleBarState` | 当前窗口状态，如最小化/最大化。 |
| `titleBarFlags` | 窗口 flags，决定按钮集合。 |
| `subControls` | 要绘制的标题栏子控件。 |
| `activeSubControls` | 当前活动/按下的子控件。 |
| `QStyle::CC_TitleBar` | 绘制标题栏。 |
| `QStyle::SC_TitleBarCloseButton` | 关闭按钮。 |
| `QStyle::SC_TitleBarMinButton` | 最小化按钮。 |
| `QStyle::SC_TitleBarMaxButton` | 最大化按钮。 |
| `QStyle::SC_TitleBarSysMenu` | 系统菜单区域。 |

## 4. 关键用法

```cpp
QStyleOptionTitleBar opt;
opt.initFrom(this);
opt.text = windowTitle();
opt.icon = windowIcon();
opt.titleBarFlags = windowFlags();
opt.titleBarState = windowState();
opt.subControls = QStyle::SC_All;

style()->drawComplexControl(QStyle::CC_TitleBar, &opt, painter, this);
```

命中关闭按钮：

```cpp
auto sc = style()->hitTestComplexControl(QStyle::CC_TitleBar, &opt, pos, this);
```

## 5. 使用场景

适合自绘 MDI 标题栏、自定义无边框窗口壳、style 实现、嵌入式窗口管理 UI。

普通顶层窗口标题栏通常由操作系统管理，不需要用它重画。

## 6. 常见坑与经验

标题栏按钮集合应由 flags 决定。画了关闭按钮但窗口不可关闭，会造成行为和视觉不一致。

系统标题栏涉及平台习惯和可访问性。自绘窗口壳要补齐拖动、双击最大化、系统菜单、键盘操作等行为。

标题文本省略、图标和按钮区域都应交给 style 计算，不要写死像素。
