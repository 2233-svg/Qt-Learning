# QHeaderView

> Qt 6.11.1 · Qt Widgets · 来自 `QHeaderView`

## 1. 先建立直觉

`QHeaderView` 是 `QTableView` 和 `QTreeView` 里的表头控件：水平表头管理列，垂直表头管理行。它不只是显示标题，还负责列宽/行高、用户拖动、隐藏、移动、排序指示器、保存恢复列布局。

很多表格体验问题其实都在 header：列太窄、最后一列留白、用户调整后下次丢失、点击表头排序不明显、树的第一列被拖走。掌握 `QHeaderView`，表格和树才会像专业桌面应用。

## 2. 类说明

- 头文件：`#include <QHeaderView>`
- 模块：`Qt6::Widgets`
- 继承自：`QAbstractItemView`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

表头数据通常来自 model 的 `headerData()`。`QHeaderView` 负责显示和交互，不负责保存业务列定义。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QHeaderView(orientation, parent)` | 创建水平或垂直表头。 |
| `orientation()` | 获取方向。 |
| `count()` | section 数量。 |
| `length()` | 所有 section 总长度。 |
| `setSectionResizeMode(mode)` | 设置所有 section 的尺寸模式。 |
| `setSectionResizeMode(index, mode)` | 设置某个逻辑 section 的尺寸模式。 |
| `sectionResizeMode()` | 查询尺寸模式。 |
| `resizeSection()` / `sectionSize()` | 设置或读取单个 section 尺寸。 |
| `resizeSections(mode)` | 按某种模式批量调整。 |
| `setDefaultSectionSize()` / `defaultSectionSize()` | 默认 section 尺寸。 |
| `resetDefaultSectionSize()` | 恢复样式默认尺寸。 |
| `setMinimumSectionSize()` / `setMaximumSectionSize()` | 限制 section 尺寸范围。 |
| `sectionSizeHint()` / `sectionSizeFromContents()` | 获取基于内容/样式的建议尺寸。 |
| `setResizeContentsPrecision()` | 控制 ResizeToContents 检查多少行列，影响性能。 |
| `hideSection()` / `showSection()` | 隐藏或显示 section。 |
| `setSectionHidden()` / `isSectionHidden()` | 程序化控制隐藏状态。 |
| `hiddenSectionCount()` / `sectionsHidden()` | 查询隐藏情况。 |
| `setSectionsMovable()` / `sectionsMovable()` | 允许用户移动 section。 |
| `moveSection()` / `swapSections()` | 程序移动或交换 section。 |
| `setFirstSectionMovable()` | 控制第一列是否可移动，树视图中特别重要。 |
| `logicalIndex()` / `visualIndex()` | 逻辑位置和视觉位置互转。 |
| `logicalIndexAt()` / `visualIndexAt()` | 根据坐标找 section。 |
| `sectionPosition()` / `sectionViewportPosition()` | 获取 section 位置。 |
| `offset()` / `setOffset()` | 表头滚动偏移。 |
| `setOffsetToLastSection()` / `setOffsetToSectionPosition()` | 快速滚动到指定 section。 |
| `setSectionsClickable()` / `sectionsClickable()` | section 是否可点击。 |
| `setHighlightSections()` | 选中对应行列时是否高亮表头。 |
| `setSortIndicator()` | 设置排序箭头所在 section 和方向。 |
| `setSortIndicatorShown()` / `isSortIndicatorShown()` | 是否显示排序指示器。 |
| `setSortIndicatorClearable()` | Qt 6.1 起允许再次点击清除排序状态。 |
| `sortIndicatorSection()` / `sortIndicatorOrder()` | 查询当前排序指示器。 |
| `setStretchLastSection()` / `stretchLastSection()` | 最后一节是否拉伸填满剩余空间。 |
| `stretchSectionCount()` | 当前 stretch section 数量。 |
| `setCascadingSectionResizes()` | 用户拖到最小宽度后是否级联调整后续 section。 |
| `setDefaultAlignment()` / `defaultAlignment()` | 表头文本默认对齐。 |
| `saveState()` / `restoreState()` | 保存和恢复列宽、顺序、隐藏状态。 |
| `sectionClicked()` / `sectionDoubleClicked()` / `sectionPressed()` | section 交互信号。 |
| `sectionMoved()` / `sectionResized()` | section 被移动或调整。 |
| `sectionCountChanged()` / `geometriesChanged()` | 表头结构或几何变化。 |
| `sortIndicatorChanged()` | 排序指示器变化。 |
| `paintSection()` | 子类化自定义 section 绘制。 |
| `initStyleOption()` / `initStyleOptionForIndex()` | 初始化表头绘制选项。 |

## 4. 关键用法

### ResizeMode 决定列宽策略

`Interactive` 允许用户拖，也允许程序 `resizeSection()`；`Fixed` 禁止用户拖；`Stretch` 自动吃掉可用空间；`ResizeToContents` 根据内容算尺寸。真实应用里常常混用：关键名称列 stretch，窄状态列 fixed，备注列 interactive。

`ResizeToContents` 在大模型上可能很贵。用 `setResizeContentsPrecision()` 限制检查数量，或只在加载完成后对少数列调用一次。

### 逻辑索引和视觉索引必须分清

逻辑索引是 model 的列号/行号，视觉索引是用户拖动后看到的位置。隐藏、移动、排序都可能让二者不同。业务访问数据永远用逻辑索引；处理用户看到的列顺序时才用视觉索引。

### 保存用户列布局

`saveState()` 和 `restoreState()` 可以保存列宽、顺序、隐藏等状态。典型做法是在窗口关闭时保存到 `QSettings`，下次构建完 model/header 后恢复。恢复失败时要能接受默认布局，因为列数或版本可能已经变化。

### 排序指示器只是 UI 状态

`setSortIndicator()` 显示箭头并发出信号，但真正排序仍要 view/model/proxy 配合。通常连接 `sortIndicatorChanged()` 或使用 `QTableView::setSortingEnabled(true)`，让排序请求到达模型或代理模型。

### 树视图第一列有特殊意义

`QTreeView` 的第一列通常承载展开箭头和层级缩进，因此默认第一 section 不可移动。只有当你明确把树结构放到其他列，或设计了稳定的多列表头交互时，再考虑 `setFirstSectionMovable(true)`。

## 5. 使用场景

`QHeaderView` 最常用于数据表、文件列表、属性表、数据库浏览器和树形资源管理器：让用户调整列宽、拖动列顺序、隐藏低频字段、点击表头排序，并把这些偏好保存到下次启动。它也是大模型性能调优点，尤其是 `ResizeToContents`、stretch 列和恢复列布局的时机。

## 6. 常见坑与经验

- `stretchLastSection(true)` 会覆盖最后一列的很多手动宽度直觉。
- 隐藏 section 后，逻辑索引仍然存在；不要把可见列号当 model 列号。
- 频繁 `resizeSections(ResizeToContents)` 会拖慢大表格。
- `restoreState()` 要在列数建立后调用，太早恢复可能失败或无效。
- 自定义表头绘制时用 `initStyleOptionForIndex()` 保留平台样式、排序箭头和状态。
