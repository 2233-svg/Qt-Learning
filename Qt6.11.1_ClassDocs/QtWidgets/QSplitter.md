# QSplitter

> Qt 6.11.1 · Qt Widgets · 来自 `QSplitter`

## 1. 先建立直觉

`QSplitter` 是可拖拽调整比例的分割容器。它让用户自己决定左右面板、上下区域的空间分配，常见于文件树+编辑器、列表+详情、预览+日志等界面。

它和布局不同：布局通常由程序根据规则分配空间，splitter 把一部分控制权交给用户，并能保存恢复用户调好的尺寸。

## 2. 类说明

- 头文件：`#include <QSplitter>`
- 模块：`Qt6::Widgets`
- 继承自：`QFrame`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

加入 splitter 的 widget 会被 splitter 接管父子关系。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QSplitter(parent)` / `QSplitter(orientation, parent)` | 创建水平或垂直分割器。 |
| `addWidget()` / `insertWidget()` | 添加或插入面板。 |
| `replaceWidget(index, widget)` | 替换某个面板并返回旧 widget。 |
| `widget(index)` / `indexOf(widget)` / `count()` | 访问面板。 |
| `setOrientation()` / `orientation()` | 设置水平/垂直分割。 |
| `setSizes()` / `sizes()` | 设置或读取各面板尺寸。 |
| `setStretchFactor()` | 设置拉伸权重。 |
| `setCollapsible()` / `isCollapsible()` | 单个面板是否可被拖到 0。 |
| `setChildrenCollapsible()` / `childrenCollapsible()` | 默认是否允许所有子面板折叠。 |
| `setHandleWidth()` / `handleWidth()` | 设置手柄宽度。 |
| `handle(index)` | 获取指定手柄。 |
| `setOpaqueResize()` / `opaqueResize()` | 拖动时实时调整还是显示橡皮筋。 |
| `getRange()` | 获取某个手柄可移动范围。 |
| `saveState()` / `restoreState()` | 保存/恢复用户调整的布局。 |
| `splitterMoved(pos, index)` | 手柄移动信号。 |
| `createHandle()` | 子类化创建自定义手柄。 |
| `moveSplitter()` / `closestLegalPosition()` | 子类化或高级控制手柄位置。 |
| `setRubberBand()` | 显示橡皮筋位置。 |
| `refresh()` | 刷新 splitter 几何。 |

## 4. 关键用法

### 保存用户布局

`saveState()` / `restoreState()` 是 splitter 的核心实用能力。偏好设置里保存它，用户下次打开应用时能保持左右面板比例。恢复前应先按同样顺序创建并加入子控件。

### 初始比例用 `setSizes()`

`setStretchFactor()` 决定额外空间分配倾向，`setSizes()` 更适合设置初始可见比例。比如左侧导航 240，右侧编辑器 760。注意尺寸不是百分比，而是相对像素权重，最终会按可用空间缩放。

### 折叠要符合任务

允许把面板拖到 0 对侧边栏很方便，但对关键编辑区可能危险。用 `setCollapsible(index, false)` 保住必须可见的区域。

### 自定义手柄

需要在手柄上画图标、添加折叠按钮或扩大命中区域时，继承 `QSplitter` 并重写 `createHandle()`。普通样式调整优先用 style sheet 或 `handleWidth`。

## 5. 常见坑与经验

- 加入 splitter 的 widget 不要再由其他布局管理。
- `handle(0)` 通常没有实际意义，手柄在两个面板之间。
- `restoreState()` 依赖子控件结构相同，面板数量变了可能恢复失败。
- 嵌套 splitter 很强大，也很容易让界面碎裂；控制层级数量。
- 大型内容实时 resize 很卡时，可关闭 `opaqueResize`。
