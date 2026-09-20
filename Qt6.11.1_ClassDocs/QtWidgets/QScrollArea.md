# QScrollArea

> Qt 6.11.1 · Qt Widgets · 来自 `QScrollArea`

## 1. 先建立直觉

`QScrollArea` 是把一个普通 QWidget 放进可滚动视口的容器。内容控件比视口大时出现滚动条；内容控件小于视口时可以按对齐方式放置，或让它自动拉伸填满。

典型场景包括设置页、图片查看、表单超长页面、自定义面板、固定大小预览。它只管理一个直接内容控件；多个控件应先放进一个容器 QWidget 的布局里，再把这个容器交给 `setWidget()`。

## 2. 类说明

- 头文件：`#include <QScrollArea>`
- 模块：`Qt6::Widgets`
- 继承自：`QAbstractScrollArea`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QScrollArea(parent)` | 创建空滚动区域。 |
| `setWidget(widget)` / `widget()` | 设置或读取唯一内容控件。 |
| `takeWidget()` | 取出内容控件，调用者重新获得所有权。 |
| `setWidgetResizable()` / `widgetResizable()` | 内容控件是否随视口调整大小。 |
| `setAlignment()` / `alignment()` | 内容小于视口时如何对齐。 |
| `ensureVisible(x, y, xmargin, ymargin)` | 滚动到内容坐标附近。 |
| `ensureWidgetVisible(childWidget, xmargin, ymargin)` | 滚动到内容控件的某个子控件可见。 |
| `focusNextPrevChild()` | 管理 Tab 焦点穿过滚动区域。 |

## 4. 关键用法

### 一个内容控件，里面再布局

如果要滚动一组表单控件，创建 `content = new QWidget`，给 content 设置布局，把所有控件加进去，然后 `scrollArea->setWidget(content)`。不要反复 `setWidget()` 多个控件，后者会替换唯一内容。

### `widgetResizable` 决定谁控制尺寸

`widgetResizable(false)` 时，内容控件自己的 size 决定滚动范围，适合图片、画布、固定尺寸预览。`true` 时，滚动区域会调整内容控件大小，适合响应式表单和设置页。滚动条是否出现取决于内容的 size hint、minimum size 和布局约束。

### 滚动到子控件

表单校验失败后，可以用 `ensureWidgetVisible(errorField)` 把第一个错误输入框滚到视口内。这比手动操作滚动条值更可靠。

## 5. 常见坑与经验

- `QScrollArea` 只直接管理一个 widget；多个子控件必须包一层容器。
- `setWidget()` 会接管内容控件并设置 parent。
- 内容控件的布局必须有合理 size hint，否则滚动范围会怪。
- `alignment` 只在内容小于视口时明显。
- 大量数据列表不要用一堆 QWidget 塞进 scroll area，使用 item view 更高效。
