# QWidgetItem

> Qt 6.11.1 · Qt Widgets · 来自 `QWidgetItem`

## 1. 先建立直觉

`QWidgetItem` 是布局系统中包装 QWidget 的 `QLayoutItem`。当你把一个按钮、输入框、面板加入布局时，布局内部会用这种 item 统一处理它的 size hint、size policy、geometry 和 height-for-width。

普通应用很少直接创建 `QWidgetItem`；它主要出现在自定义布局实现和调试布局行为时。

## 2. 类说明

- 头文件：`#include <QWidgetItem>`
- 模块：`Qt6::Widgets`
- 继承自：`QLayoutItem`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

它包装一个 QWidget，但自身不是 QWidget。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QWidgetItem(widget)` | 创建包装指定 QWidget 的布局项。 |
| `widget()` | 返回被包装的 QWidget。 |
| `sizeHint()` | 返回 widget 的推荐尺寸。 |
| `minimumSize()` / `maximumSize()` | 返回 widget 的尺寸边界。 |
| `setGeometry(rect)` / `geometry()` | 给 widget 分配或读取几何。 |
| `expandingDirections()` | 根据 widget size policy 判断扩展方向。 |
| `hasHeightForWidth()` / `heightForWidth()` | 转发 widget 的 height-for-width 行为。 |
| `controlTypes()` | 返回 widget 的控件类型。 |
| `isEmpty()` | widget 隐藏或无效时供布局判断。 |

## 4. 关键用法

写自定义布局时，你通常保存 `QLayoutItem *` 列表，而不是 QWidget 列表。这样同一套布局既能管理 widget，也能管理 spacer 和子布局。需要访问真实控件时，再调用 `item->widget()`。

`QWidgetItem` 的尺寸信息来自 widget 自己：`sizeHint()`、minimum/maximum size、size policy、height-for-width。要改变布局结果，通常改 widget 的这些属性，而不是直接碰 `QWidgetItem`。

## 5. 常见坑与经验

- 不要把 `QWidgetItem` 当成控件加入界面，它只是布局内部包装。
- 删除 layout item 和删除 widget 是两个层面的事情，自定义布局析构要处理清楚。
- widget 隐藏后布局是否保留空间还受 `QSizePolicy::retainSizeWhenHidden` 影响。
- 自定义布局应通过 `QLayoutItem` 接口工作，减少对具体 item 类型的假设。
