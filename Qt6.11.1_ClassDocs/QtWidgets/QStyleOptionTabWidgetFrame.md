# QStyleOptionTabWidgetFrame

> Qt 6.11.1 · Qt Widgets · 来自 `QStyleOptionTabWidgetFrame`

## 1. 先建立直觉

`QStyleOptionTabWidgetFrame` 是 `QTabWidget` 页面框架的绘制参数包。它描述 tab bar 的位置、选中 tab、左右角落 widget、内容区域和整体形状。

单个标签由 `QStyleOptionTab` 描述；tab widget 周围的框架由这个类描述。

## 2. 类说明

`QStyleOptionTabWidgetFrame` 继承自 `QStyleOption`。style 用它绘制 `QStyle::PE_FrameTabWidget`，也会用相关字段调整 tab bar 与页面框架的衔接。

它常出现在 `QTabWidget` 或自定义分页容器的绘制实现中。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `shape` | tab 形状和方向。 |
| `tabBarSize` | tab bar 尺寸。 |
| `rightCornerWidgetSize` | 右角落 widget 尺寸。 |
| `leftCornerWidgetSize` | 左角落 widget 尺寸。 |
| `selectedTabRect` | 当前选中 tab 区域。 |
| `tabBarRect` | tab bar 区域。 |
| `lineWidth` / `midLineWidth` | 框架线宽。 |
| `QStyle::PE_FrameTabWidget` | 绘制 tab widget frame。 |

## 4. 关键用法

```cpp
QStyleOptionTabWidgetFrame opt;
opt.initFrom(tabWidget);
opt.shape = tabWidget->tabShape() == QTabWidget::Rounded
          ? QTabBar::RoundedNorth
          : QTabBar::TriangularNorth;
opt.tabBarSize = tabWidget->tabBar()->size();
opt.selectedTabRect = tabWidget->tabBar()->tabRect(tabWidget->currentIndex());

style()->drawPrimitive(QStyle::PE_FrameTabWidget, &opt, painter, tabWidget);
```

## 5. 使用场景

适合自定义 `QTabWidget`、分页框架、style 实现、带角落工具按钮的标签页容器。

普通页面切换只需要 `QTabWidget` API，不需要直接构造它。

## 6. 常见坑与经验

TabBar、页面 frame、corner widget 三者尺寸要一致，否则会出现边框断裂或内容压住标签。

选中 tab 的矩形会影响 frame 与 tab 的衔接，不能省略。

不同 tab position 下 frame 的开口方向不同，绘制逻辑不能只按 North tab 写。
