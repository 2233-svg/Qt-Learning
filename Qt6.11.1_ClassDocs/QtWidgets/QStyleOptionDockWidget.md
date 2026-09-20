# QStyleOptionDockWidget

> Qt 6.11.1 · Qt Widgets · 来自 `QStyleOptionDockWidget`

## 1. 先建立直觉

`QStyleOptionDockWidget` 是停靠窗口标题栏绘制参数包。它告诉 style 这个 dock 的标题、是否可关闭、可浮动、可移动，以及当前是垂直标题还是水平标题。

它主要服务 `QDockWidget` 的标题栏和按钮绘制。

## 2. 类说明

`QStyleOptionDockWidget` 继承自 `QStyleOption`。它保存 title、closable、movable、floatable、verticalTitleBar 等字段。

Dock widget 的内容区由普通 widget 管理；这个 option 关注的是 dock 外壳，尤其是标题栏。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `title` | dock 标题文本。 |
| `closable` | 是否显示/允许关闭。 |
| `movable` | 是否可拖动停靠。 |
| `floatable` | 是否可浮动成独立窗口。 |
| `verticalTitleBar` | 是否使用垂直标题栏。 |
| `QStyle::CE_DockWidgetTitle` | 绘制 dock 标题栏。 |
| `QStyle::PE_IndicatorDockWidgetResizeHandle` | 绘制相关指示元素。 |

## 4. 关键用法

```cpp
QStyleOptionDockWidget opt;
opt.initFrom(dock);
opt.title = dock->windowTitle();
opt.closable = dock->features() & QDockWidget::DockWidgetClosable;
opt.movable = dock->features() & QDockWidget::DockWidgetMovable;
opt.floatable = dock->features() & QDockWidget::DockWidgetFloatable;

style()->drawControl(QStyle::CE_DockWidgetTitle, &opt, painter, dock);
```

## 5. 使用场景

适合自定义 dock title bar、style 实现、主窗口框架外观统一、专业工具软件的停靠面板定制。

普通 `QDockWidget` 使用者只需要设置 features 和 windowTitle。

## 6. 常见坑与经验

features 会影响按钮可见性和行为，绘制时要和真实 `QDockWidget::features()` 保持一致。

垂直标题栏不仅是旋转文字，按钮位置和布局也会变化。

自定义标题栏时别丢掉可访问性和键盘操作，dock 面板在专业软件里经常被重度使用。
