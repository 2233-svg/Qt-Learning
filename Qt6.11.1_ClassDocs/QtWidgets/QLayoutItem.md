# QLayoutItem

> Qt 6.11.1 · Qt Widgets · 来自 `QLayoutItem`

## 1. 先建立直觉

`QLayoutItem` 是布局系统里的抽象“占位项”。布局管理的不是只有 QWidget，还包括子布局和 spacer；它们都通过 `QLayoutItem` 统一暴露尺寸、几何、是否为空、是否可扩展等信息。

你通常不直接用它，除非写自定义布局。理解它能帮助你看懂 `QLayout::itemAt()`、`takeAt()` 为什么返回 layout item，而不是直接返回 widget。

## 2. 类说明

- 头文件：`#include <QLayoutItem>`
- 模块：`Qt6::Widgets`
- 继承自：无
- 直接派生类：`QLayout`、`QSpacerItem`、`QWidgetItem`

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

这是布局协议对象，不是 QWidget。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QLayoutItem(alignment)` | 创建带对齐方式的布局项。 |
| `alignment()` / `setAlignment()` | 读取或设置此项在分配区域内的对齐。 |
| `sizeHint()` | 纯虚函数；推荐尺寸。 |
| `minimumSize()` / `maximumSize()` | 纯虚函数；尺寸边界。 |
| `setGeometry(rect)` / `geometry()` | 纯虚函数；布局分配和读取几何。 |
| `expandingDirections()` | 纯虚函数；愿意扩展的方向。 |
| `isEmpty()` | 纯虚函数；此项是否为空。 |
| `hasHeightForWidth()` / `heightForWidth()` | 宽度影响高度的布局支持。 |
| `minimumHeightForWidth()` | 给定宽度下的最小高度。 |
| `controlTypes()` | 返回控件类型，帮助 style 计算间距。 |
| `invalidate()` | 缓存尺寸失效。 |
| `widget()` | 如果此项包装 QWidget，返回它。 |
| `layout()` | 如果此项包装子布局，返回它。 |
| `spacerItem()` | 如果此项是 spacer，返回它。 |

## 4. 关键用法

自定义布局的核心流程是：遍历内部 `QLayoutItem`，读取 `sizeHint()`、`minimumSize()`、`expandingDirections()`，根据可用矩形计算每一项位置，再调用 `setGeometry()` 分配空间。

从布局取出 item 时，要分清 item 和它包装的对象。`takeAt()` 返回的 `QLayoutItem` 需要删除；若里面有 widget，是否删除 widget 是另一个决定。

height-for-width 是布局质量的高级点。自动换行 label、按比例内容等都可能宽度变窄高度变高，自定义布局如果忽略它，界面会出现截断。

## 5. 常见坑与经验

- `QLayoutItem` 不是 QObject，没有 parent 自动销毁模型。
- 删除 layout item 不一定删除其中 widget，要看具体所有权和你的代码。
- 自定义布局必须正确实现纯虚函数，否则 size hint 和实际几何会打架。
- `invalidate()` 用来告诉布局重新计算，不要靠手动 repaint 解决几何问题。
