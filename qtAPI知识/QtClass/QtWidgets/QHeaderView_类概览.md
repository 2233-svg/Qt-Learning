# Qt QHeaderView 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QHeaderView>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QAbstractItemView -> QHeaderView`  
> 常见搭档：`QTableView`、`QTreeView`

## 1. QHeaderView 解决什么问题

`QHeaderView` 是项目视图的表头：它显示列头或行头，负责列/行标题、排序箭头、拖动重排、列宽调整、隐藏显示和尺寸协商。

它不是一个独立业务控件，而是 `QTableView`、`QTreeView` 这类 item view 的配套部件。表头里的每一节都对应模型中的一个逻辑列或逻辑行，标题内容通常来自模型的 `headerData()`。

可以先记住一件事：

```text
logical index  = 模型中的固定编号
visual index   = 当前屏幕上的显示顺序
```

逻辑索引不会因为拖动改变；视觉索引会。  
这也是 `QHeaderView` 最核心的价值：把“模型顺序”和“显示顺序”分开。

## 2. 最小可用代码

```cpp
#include <QTableView>
#include <QStandardItemModel>

auto *view = new QTableView;
auto *model = new QStandardItemModel(3, 4, view);

view->setModel(model);
view->horizontalHeader()->setSectionsMovable(true);
view->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
view->horizontalHeader()->setSortIndicatorShown(true);
```

大多数时候你不会直接 new 一个 `QHeaderView` 再单独用，而是通过 `QTableView::horizontalHeader()` 或 `QTreeView::header()` 拿到现成的表头，再调整它的行为。

## 3. 先把两种索引讲清楚

`QHeaderView` 中最容易混淆的概念是 `logicalIndex` 和 `visualIndex`。

| 概念 | 含义 | 会不会因拖动改变 |
| --- | --- | --- |
| `logicalIndex` | 模型里的原始列/行编号。 | 不变。 |
| `visualIndex` | 现在屏幕上看到的顺序编号。 | 会变。 |

```cpp
int visual = header->visualIndex(2);   // 逻辑 2 现在显示在第几个位置
int logical = header->logicalIndex(1); // 视觉第 1 个位置对应哪个逻辑索引
```

查询位置时还会有两种“坐标系”：

- `logicalIndexAt(position)`：位置上的逻辑索引；
- `visualIndexAt(position)`：位置上的视觉索引。

如果 section 被隐藏，很多 API 会返回 `-1`。  
例如 `sectionPosition(logicalIndex)` 在 section 隐藏时返回 `-1`。

## 4. 尺寸和布局：表头为什么会变宽变窄

### 4.1 ResizeMode

`ResizeMode` 决定 section 怎么变宽：

| 模式 | 含义 |
| --- | --- |
| `Interactive` | 用户可以拖动调整，也可程序调整。 |
| `Fixed` | 用户不能拖，只能程序调整。 |
| `Stretch` | 自动吃掉剩余空间。 |
| `ResizeToContents` | 根据内容自动计算宽度或高度。 |
| `Custom` | 等价于 `Fixed`，只是历史别名。 |

例子：

```cpp
header->setSectionResizeMode(QHeaderView::Interactive);
header->setSectionResizeMode(0, QHeaderView::ResizeToContents);
header->setSectionResizeMode(3, QHeaderView::Stretch);
```

### 4.2 影响尺寸的属性

```cpp
header->setDefaultSectionSize(120);
header->setMinimumSectionSize(40);
header->setMaximumSectionSize(400);
header->setResizeContentsPrecision(100);
```

这些参数的作用分别是：

- `defaultSectionSize`：默认 section 尺寸；
- `minimumSectionSize`：最小 section 尺寸；
- `maximumSectionSize`：最大 section 尺寸；
- `resizeContentsPrecision`：`ResizeToContents` 计算内容尺寸时扫描多少数据，越大越准，也越慢。

`stretchLastSection` 很重要：

```cpp
header->setStretchLastSection(true);
```

最后一个可见 section 会吃掉剩余空间。`QTreeView` 的水平表头默认就是这样，避免右侧留下空白。

### 4.3 位置和滚动

```cpp
int off = header->offset();
int len = header->length();
header->setOffset(0);
header->setOffsetToLastSection();
header->setOffsetToSectionPosition(3);
```

`offset()` 是表头当前滚动偏移。`length()` 是沿着表头方向的总长度。  
这些函数主要给视图内部和自定义行为使用，普通业务代码很少直接操作。

## 5. 移动、隐藏和重排

```cpp
header->setSectionsMovable(true);
header->setFirstSectionMovable(true);
header->moveSection(3, 1);
header->swapSections(0, 2);
header->setSectionHidden(4, true);
header->showSection(4);
```

几个关键点：

- `sectionsMovable` 控制用户能否拖动重排；
- `firstSectionMovable` 专门控制第一节是否可移动，`QTreeView` 中常见第一列固定；
- `hideSection()` / `showSection()` 是 `setSectionHidden()` 的便捷包装；
- `sectionsMoved()`、`sectionsHidden()` 这两个查询函数可用来判断 header 是否已经发生过重排或隐藏；
- `hiddenSectionCount()` 返回被隐藏的 section 数量。

在超大模型里要格外注意：从 Qt 6.9 起，只有在发生重排、隐藏或调整大小时，才会为 section 分配额外内存。也就是说，如果你想让一个超大模型的表头保持轻量，就尽量避免不必要的 `moveSection()`、`resizeSection()`、`hideSection()` 和 `stretchLastSection(true)`。

## 6. 排序指示器

`QHeaderView` 既能显示排序箭头，也能控制箭头是否可清除。

```cpp
header->setSectionsClickable(true);
header->setSortIndicatorShown(true);
header->setSortIndicator(2, Qt::AscendingOrder);
header->setSortIndicatorClearable(true);
```

说明：

- `sectionsClickable` 打开后，用户可以点击 section；
- `setSortIndicatorShown(true)` 显示排序箭头；
- `setSortIndicator(section, order)` 指定当前排序列和顺序；
- `setSortIndicator(-1, ...)` 可以清除排序指示并回到自然顺序，但并非所有模型都支持；
- `sortIndicatorClearable` 控制用户连续点击时能否清除排序指示；
- `sortIndicatorClearableChanged` 会在这个能力变化时发出。

`sortIndicatorSection()` 和 `sortIndicatorOrder()` 用来查询当前排序状态。  
`sectionClicked(int)`、`sortIndicatorChanged(int, Qt::SortOrder)` 是常用信号。

## 7. 点击、进入、按压和尺寸调整

```cpp
connect(header, &QHeaderView::sectionClicked, this, [](int logicalIndex) {
    qDebug() << "clicked:" << logicalIndex;
});
```

相关交互信号包括：

- `sectionPressed(int)`：按下；
- `sectionClicked(int)`：点击；
- `sectionDoubleClicked(int)`：双击；
- `sectionEntered(int)`：鼠标按下时移动到某节上；
- `sectionMoved(int, int, int)`：节被移动；
- `sectionResized(int, int, int)`：节被调整大小；
- `sectionHandleDoubleClicked(int)`：双击分隔条手柄；
- `geometriesChanged()`：几何变化完成；
- `sectionCountChanged(int, int)`：section 数量变化。

这些信号特别适合和自定义业务逻辑联动，比如保存列顺序、持久化列宽、联动搜索条件等。

## 8. 保存和恢复 header 状态

```cpp
settings.setValue("tableHeader", header->saveState());

header->restoreState(
    settings.value("tableHeader").toByteArray());
```

`saveState()` 和 `restoreState()` 会保存或恢复表头状态，包括顺序、宽度、隐藏状态等。  
这比自己手记一组列宽和顺序更稳妥，尤其适合用户可自定义列布局的表格。

## 9. QHeaderView 和模型

`QHeaderView` 依赖模型的 header 数据：

```cpp
model->setHeaderData(0, Qt::Horizontal, tr("Name"));
model->setHeaderData(1, Qt::Horizontal, tr("Size"));
```

当模型发出 `headerDataChanged()` 时，header 会更新对应 sections。  
`setModel()` 被重新实现，就是为了在模型切换时正确重建 header 状态。

如果你在自定义模型里修改了表头信息，别忘了发出正确的 `headerDataChanged()` 范围，否则 header 不会及时刷新。

## 10. 自定义绘制和高级扩展

普通项目一般只调属性和信号，不需要重写表头绘制。但如果你要做特殊表头外观，可以关注：

- `initStyleOption(QStyleOptionHeader *)`：填充整张表头的样式信息；
- `initStyleOptionForIndex(QStyleOptionHeader *, int)`：为某个 section 填充样式信息；
- `paintSection(QPainter *, const QRect &, int)`：绘制单个 section；
- `sectionSizeFromContents(int)`：根据内容计算 section 尺寸；
- `paintEvent(QPaintEvent *)`：整体绘制入口。

此外，`updateGeometries()`、`scrollContentsBy()`、`horizontalOffset()`、`verticalOffset()`、`visualRect()`、`scrollTo()`、`indexAt()`、`isIndexHidden()`、`moveCursor()`、`setSelection()`、`visualRegionForSelection()` 都是 `QAbstractItemView` 体系的实现点，主要给派生类或 Qt 内部使用。

## API 速查表
### 11.1 构造、类型和基础查询

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `ResizeMode` | 定义 section 的尺寸计算和交互方式。 | `Interactive`、`Fixed`、`Stretch`、`ResizeToContents`、`Custom` 面向不同表头策略。 |
| 构造 | `QHeaderView(Qt::Orientation orientation, QWidget *parent = nullptr)` | 创建水平或垂直表头。 | 水平表头对应列，垂直表头对应行；大多数时候从 `QTableView/QTreeView` 取得。 |
| 析构 | `~QHeaderView()` | 销毁表头对象。 | 通常由所属 view 的对象树管理。 |
| 方向 | `orientation() const` | 返回表头是水平还是垂直。 | 决定 position、size、logical index 对应列还是行。 |
| 数量 | `count() const` | 返回 section 数量。 | 对应模型的列数或行数。 |
| 滚动 | `offset() const` | 返回表头当前滚动偏移。 | 主要给视图内部和高级定制使用。 |
| 总长度 | `length() const` | 返回所有 section 沿表头方向的总长度。 | 包括当前可见布局下的 section 尺寸累计。 |
| 尺寸 | `sizeHint() const` | 返回表头推荐尺寸。 | 由布局系统读取，不应当成固定尺寸。 |

### 11.2 逻辑/视觉索引和位置

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 索引映射 | `logicalIndex(int visualIndex) const` | 从屏幕显示顺序反查模型逻辑索引。 | 用户拖动列后，视觉顺序会变，但模型仍认逻辑索引。 |
| 索引映射 | `visualIndex(int logicalIndex) const` | 从模型逻辑索引查询当前显示位置。 | section 隐藏或无效时可能返回 -1。 |
| 命中测试 | `logicalIndexAt(int position) const` | 从表头方向上的像素位置找到逻辑索引。 | 用于鼠标点中哪一列/行。 |
| 命中测试 | `logicalIndexAt(const QPoint &pos) const` | 从点坐标找到逻辑索引。 | 内部会按表头方向使用 x 或 y。 |
| 命中测试 | `logicalIndexAt(int x, int y) const` | 从 x/y 坐标找到逻辑索引。 | 横向表头看 x，纵向表头看 y。 |
| 命中测试 | `visualIndexAt(int position) const` | 从像素位置找到视觉索引。 | 适合处理显示顺序相关交互。 |
| 位置 | `sectionPosition(int logicalIndex) const` | 返回逻辑 section 在整条 header 中的位置。 | section 隐藏时返回 -1。 |
| 位置 | `sectionViewportPosition(int logicalIndex) const` | 返回 section 在 viewport 坐标中的位置。 | 已考虑滚动偏移，适合定位可见区域。 |
| 尺寸 | `sectionSize(int logicalIndex) const` | 返回某个 section 当前宽度或高度。 | 方向为水平时是宽度，垂直时是高度。 |
| 尺寸 | `sectionSizeHint(int logicalIndex) const` | 返回某个 section 推荐尺寸。 | 受模型 header 数据、delegate/style 和默认尺寸影响。 |

### 11.3 让 section 可移动、可见和可点击

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 移动 | `sectionsMovable() const` / `setSectionsMovable(bool movable)` | 控制用户是否可以拖动 section 改变显示顺序。 | 大模型表头开启移动会产生额外状态记录。 |
| 移动 | `isFirstSectionMovable() const` / `setFirstSectionMovable(bool movable)` | 单独控制第一节是否可移动。 | `QTreeView` 常把第一列固定，避免树列被拖走。 |
| 点击 | `sectionsClickable() const` / `setSectionsClickable(bool clickable)` | 控制 section 是否响应点击。 | 排序、筛选菜单、列操作通常需要打开。 |
| 高亮 | `highlightSections() const` / `setHighlightSections(bool highlight)` | 控制相关 section 是否高亮显示。 | 主要是外观反馈，具体效果受 style 影响。 |
| 隐藏 | `isSectionHidden(int logicalIndex) const` / `setSectionHidden(int logicalIndex, bool hide)` | 查询或设置某个 section 是否隐藏。 | 隐藏只影响视图，不删除模型列/行。 |
| 隐藏 | `hideSection(int logicalIndex)` / `showSection(int logicalIndex)` | 隐藏或显示 section 的便捷函数。 | 等价于设置 `setSectionHidden()`。 |
| 隐藏查询 | `hiddenSectionCount() const` | 返回当前隐藏 section 的数量。 | 判断用户是否做过列隐藏设置时有用。 |
| 状态查询 | `sectionsMoved() const` | 判断 section 顺序是否被移动过。 | 可决定是否需要保存表头布局。 |
| 状态查询 | `sectionsHidden() const` | 判断是否有 section 被隐藏。 | 与 `hiddenSectionCount()` 配合检查表头状态。 |
| 移动 | `moveSection(int from, int to)` | 把一个视觉位置上的 section 移到另一个视觉位置。 | 参数是视觉索引，不是逻辑索引。 |
| 移动 | `swapSections(int first, int second)` | 交换两个 section 的显示位置。 | 参数按 section 索引语义使用，交换后模型逻辑编号不变。 |

### 11.4 尺寸模式和边界

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 尺寸模式 | `sectionResizeMode(int logicalIndex) const` | 查询某个 section 当前 resize mode。 | 单节模式可能覆盖全局模式。 |
| 尺寸模式 | `setSectionResizeMode(ResizeMode mode)` | 为所有 section 设置统一 resize mode。 | 初始化表格列宽策略时最常用。 |
| 尺寸模式 | `setSectionResizeMode(int logicalIndex, ResizeMode mode)` | 为某个 section 设置单独 resize mode。 | 例如前几列按内容、最后一列 stretch。 |
| 内容适配 | `setResizeContentsPrecision(int precision)` / `resizeContentsPrecision() const` | 设置或读取 `ResizeToContents` 扫描数据的精度。 | 值越大越准也越慢，大模型要保守。 |
| 尺寸修改 | `resizeSection(int logicalIndex, int size)` | 直接把 section 改成指定像素尺寸。 | 尺寸为 0 不推荐，想隐藏应使用 `hideSection()`。 |
| 尺寸修改 | `resizeSections(ResizeMode mode)` | 按指定模式重新计算所有 section 尺寸。 | 适合初始化或模型结构大变后重排。 |
| 默认尺寸 | `setDefaultSectionSize(int size)` / `defaultSectionSize() const` | 设置或读取 section 默认尺寸。 | 影响 `Interactive/Fixed` 等不按内容自动计算的场景。 |
| 默认尺寸 | `resetDefaultSectionSize()` | 恢复 style 提供的默认 section 尺寸。 | 想撤销程序手动默认值时用。 |
| 尺寸边界 | `setMinimumSectionSize(int size)` / `minimumSectionSize() const` | 设置或读取 section 最小尺寸。 | 防止列宽/行高被拖到不可读。 |
| 尺寸边界 | `setMaximumSectionSize(int size)` / `maximumSectionSize() const` | 设置或读取 section 最大尺寸。 | 防止某列吃掉过多空间。 |
| Stretch | `setStretchLastSection(bool stretch)` / `stretchLastSection() const` | 控制最后一个可见 section 是否吃满剩余空间。 | 会覆盖最后一节 resize mode；`QTreeView` 常默认开启。 |
| 级联调整 | `setCascadingSectionResizes(bool enable)` / `cascadingSectionResizes() const` | 控制拖动一节时是否连带调整后续节。 | 只对 `Interactive` 模式有意义。 |
| Stretch 查询 | `stretchSectionCount() const` | 返回当前 stretch section 数量。 | 判断是否存在自动吃空间的 section。 |

### 11.5 排序和对齐

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 排序显示 | `setSortIndicatorShown(bool show)` / `isSortIndicatorShown() const` | 控制是否显示排序箭头。 | 只是显示状态，真正排序通常由 view/model 协作完成。 |
| 排序显示 | `setSortIndicator(int logicalIndex, Qt::SortOrder order)` | 设置排序箭头所在逻辑 section 和方向。 | `logicalIndex` 可为 -1 表示清除排序指示。 |
| 排序查询 | `sortIndicatorSection() const` | 查询当前排序指示所在 section。 | 没有排序指示时可能为 -1。 |
| 排序查询 | `sortIndicatorOrder() const` | 查询当前排序方向。 | 只有配合有效排序 section 才有业务意义。 |
| 排序清除 | `setSortIndicatorClearable(bool clearable)` / `isSortIndicatorClearable() const` | 控制用户能否把排序状态点回无排序。 | 通常需要 section 可点击。 |
| 信号 | `sortIndicatorClearableChanged(bool clearable)` | 排序可清除能力变化时通知。 | Qt 6.1 起可用。 |
| 对齐 | `setDefaultAlignment(Qt::Alignment alignment)` / `defaultAlignment() const` | 设置或读取 section 文本默认对齐方式。 | 模型 headerData 的对齐角色可能覆盖具体 section。 |

### 11.6 状态保存、模型连接和槽

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 状态保存 | `saveState() const` | 保存 section 顺序、宽度、隐藏等布局状态。 | 适合写入 `QSettings`，恢复时模型结构要匹配。 |
| 状态恢复 | `restoreState(const QByteArray &state)` | 恢复之前保存的表头布局状态。 | 返回 `false` 时用默认布局兜底。 |
| 重置 | `reset()` | 重置 header 视图状态。 | 不会改模型数据，只重建视图侧状态。 |
| 模型 | `setModel(QAbstractItemModel *model)` | 设置或切换 header 读取的模型。 | 表头文字、图标、对齐通常来自模型 `headerData()`。 |
| 模型变化 | `headerDataChanged(Qt::Orientation orientation, int logicalFirst, int logicalLast)` | 响应模型表头数据变化。 | 自定义模型改表头后必须发对应信号。 |
| 滚动 | `setOffset(int offset)` | 设置 header 滚动偏移。 | 高级用法，普通业务通常不直接操作。 |
| 滚动 | `setOffsetToSectionPosition(int visualIndex)` | 把滚动偏移定位到某个视觉 section。 | 参数是视觉顺序位置。 |
| 滚动 | `setOffsetToLastSection()` | 把 header 滚到最后一个 section 附近。 | 常用于内部或特殊导航需求。 |

### 11.7 信号和 protected 扩展点

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 信号 | `sectionMoved(int logicalIndex, int oldVisualIndex, int newVisualIndex)` | section 被移动时通知。 | 保存用户列顺序时最常用。 |
| 信号 | `sectionResized(int logicalIndex, int oldSize, int newSize)` | section 尺寸变化时通知。 | 保存列宽/行高偏好时使用。 |
| 信号 | `sectionPressed(int logicalIndex)` / `sectionClicked(int logicalIndex)` | section 被按下或点击时通知。 | 排序、筛选菜单、列操作入口常用。 |
| 信号 | `sectionEntered(int logicalIndex)` | 鼠标按下后进入某 section 时通知。 | hover 提示或拖动反馈。 |
| 信号 | `sectionDoubleClicked(int logicalIndex)` / `sectionHandleDoubleClicked(int logicalIndex)` | section 或分隔手柄被双击时通知。 | 常用于自动调整列宽。 |
| 信号 | `sectionCountChanged(int oldCount, int newCount)` | section 数量变化时通知。 | 模型列/行数变化后触发。 |
| 信号 | `geometriesChanged()` | 表头几何布局变化完成时通知。 | 调整外部覆盖层或保存状态时可用。 |
| 信号 | `sortIndicatorChanged(int logicalIndex, Qt::SortOrder order)` | 排序指示列或方向变化时通知。 | 可连接到排序模型或业务排序逻辑。 |
| 保护槽 | `updateSection(int logicalIndex)` | 请求更新指定 section。 | 通常由模型 header 数据变化触发。 |
| 保护槽 | `resizeSections()` | 重新计算 section 尺寸。 | 内部布局更新使用。 |
| 保护槽 | `sectionsInserted(...)` / `sectionsAboutToBeRemoved(...)` | 响应模型 section 插入和删除。 | 派生类维护缓存时要同步处理。 |
| 初始化 | `initialize()` / `initializeSections()` / `initializeSections(int start, int end)` | 初始化或重建 section 内部结构。 | 高级派生类才会关注。 |
| 当前项 | `currentChanged(const QModelIndex &current, const QModelIndex &old)` | 当前索引变化的视图扩展点。 | 继承自 item view 体系，普通业务很少重写。 |
| 事件 | `event(...)` / `viewportEvent(...)` | 处理 header 和 viewport 事件。 | 深度定制时保留基类行为。 |
| 绘制 | `paintEvent(QPaintEvent *event)` / `paintSection(QPainter *painter, const QRect &rect, int logicalIndex) const` | 绘制整体表头和单个 section。 | 自定义外观时优先使用 style option。 |
| 尺寸计算 | `sectionSizeFromContents(int logicalIndex) const` | 根据内容计算 section 推荐尺寸。 | `ResizeToContents` 的关键扩展点。 |
| 鼠标 | `mousePressEvent(...)` / `mouseMoveEvent(...)` / `mouseReleaseEvent(...)` / `mouseDoubleClickEvent(...)` | 处理点击、拖动、调整大小和双击。 | 重写时要保留移动、排序、resize 等默认交互。 |
| 偏移 | `horizontalOffset() const` / `verticalOffset() const` | 返回 item view 体系里的滚动偏移。 | 表头作为特殊 item view 的内部实现。 |
| 几何 | `updateGeometries()` / `scrollContentsBy(int dx, int dy)` | 更新内部几何并响应滚动。 | 通常由视图系统驱动。 |
| 模型变化 | `dataChanged(...)` / `rowsInserted(...)` | 响应模型数据或结构变化。 | 表头主要关心 header 数据和 section 数量。 |
| 视图实现 | `visualRect(...)` / `scrollTo(...)` / `indexAt(...)` / `isIndexHidden(...)` | 实现 `QAbstractItemView` 所需的定位接口。 | 普通业务不要把表头当普通数据视图使用。 |
| 导航/选择 | `moveCursor(...)` / `setSelection(...)` / `visualRegionForSelection(...)` | 实现键盘导航和选择区域换算。 | 属于内部和派生类扩展点。 |
| 样式 | `initStyleOption(QStyleOptionHeader *option) const` / `initStyleOptionForIndex(QStyleOptionHeader *option, int logicalIndex) const` | 填充整体或单个 section 的绘制状态。 | 自定义绘制时调用，避免遗漏排序、禁用、方向和位置状态。 |

## 12. 常见误区

### 12.1 把逻辑索引和视觉索引混为一谈

模型永远认逻辑索引，用户看到的是视觉索引。列被拖动后，真正变化的是显示顺序，不是模型编号。

### 12.2 ResizeToContents 不加精度控制

数据很多时，`ResizeToContents` 可能很慢。`resizeContentsPrecision()` 太大时会拖慢首次布局，太小时又可能不够准。

### 12.3 以为 hideSection 就是删除列

隐藏只是视觉上不显示，模型里数据还在。需要真正删列，要改模型。

### 12.4 只改 view 不改模型 headerData

表头文字、图标、对齐等本质上来自模型的 `headerData()`。UI 代码只调表头属性不够时，要回到模型层改数据。

### 12.5 在超大模型上随便 move / resize / hide

这些操作会让表头记录更多 section 状态。大模型下应尽量少做用户可见布局变更，除非确实需要。

---

### 一句话总结

`QHeaderView` 是 item view 的表头：用 logical/visual index 区分模型顺序和显示顺序，用 resize mode 控制列宽策略，用 sorting 和 hide/move API 管理交互，用 saveState()/restoreState() 记住用户布局。
