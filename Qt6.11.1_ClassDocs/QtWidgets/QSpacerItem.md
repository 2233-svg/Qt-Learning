# QSpacerItem

> Qt 6.11.1 · Qt Widgets · 来自 `QSpacerItem`

## 1. 先建立直觉

`QSpacerItem` 是布局里的空白弹簧。它不显示内容，只用尺寸和 size policy 告诉布局“这里需要固定空隙”或“这里可以吸收多余空间”。

它适合把按钮推到右侧、在表单中制造弹性留白、控制控件之间的最小间隔。日常开发更多通过 `layout->addStretch()`、`addSpacing()` 间接创建它。

## 2. 类说明

- 头文件：`#include <QSpacerItem>`
- 模块：`Qt6::Widgets`
- 继承自：`QLayoutItem`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

它不是 QWidget，不绘制、不接收事件。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QSpacerItem(w, h, hPolicy, vPolicy)` | 创建指定基础尺寸和伸缩策略的空白项。 |
| `changeSize(w, h, hPolicy, vPolicy)` | 修改 spacer 尺寸和策略；之后通常要让布局失效。 |
| `sizePolicy()` | 返回 spacer 的尺寸策略。 |
| `sizeHint()` / `minimumSize()` / `maximumSize()` | 布局计算尺寸时使用。 |
| `expandingDirections()` | 返回 spacer 愿意扩展的方向。 |
| `geometry()` / `setGeometry()` | 读取或设置布局分配给它的矩形。 |
| `isEmpty()` | 对 spacer 来说通常表示它没有可见内容。 |
| `spacerItem()` | 返回自身，便于从 `QLayoutItem` 识别。 |

## 4. 关键用法

水平按钮行常用“弹簧”把按钮推到右侧：左边加 stretch，右边放按钮。固定间距用 `addSpacing()`；可伸缩空白用 `addStretch()` 或显式 `QSpacerItem`。

`changeSize()` 后，如果 spacer 已经在布局中，要调用布局的 `invalidate()` 或触发布局重新计算，否则界面可能不会马上按新尺寸布局。

## 5. 常见坑与经验

- spacer 不是控件，不能设置样式表或背景。
- 想要可见分隔线用 `QFrame`，不要用 spacer。
- 固定空白太多会破坏响应式布局，优先使用 spacing、margins、stretch。
- 修改 spacer 尺寸后记得让布局重新计算。
