# Qt QAbstractItemView 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAbstractItemView>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QAbstractScrollArea -> QAbstractItemView`  
> 定位：抽象基类

## 1. 先建立整体认识：它解决什么问题

`QAbstractItemView` 是 Qt item view 体系的骨架。  
它不负责直接给你一个现成控件，而是定义了“视图应该怎么和模型、选择、代理、滚动条协作”的规则。

它解决的核心问题是：

- 模型里的数据如何映射成屏幕上的单元；
- 用户如何选择、编辑、拖拽、滚动、定位；
- 视图如何知道哪些地方需要重绘、重排、进入编辑状态；
- 一个 `QItemSelectionModel` 如何和多个视图协同工作。

典型派生类包括：

- `QListView`
- `QTableView`
- `QTreeView`
- `QHeaderView`

它们都继承这个骨架，只是在“如何摆放索引、如何计算位置、如何绘制”上给出不同策略。

## 2. 这类视图到底由什么组成

```text
QAbstractItemModel      提供数据
QItemSelectionModel     维护选择
QAbstractItemDelegate   绘制和编辑单元格
QAbstractItemView       把三者组织成可交互视图
```

再往下拆：

- `viewport()` 才是真正画东西的地方；
- 滚动条负责移动可见区域；
- `currentIndex` 表示当前焦点项；
- `selectedIndexes` 表示当前选中的项集合；
- `rootIndex` 决定树/列表从模型哪一层开始看。

所以它不是“列表控件”这么简单，而是一个完整的 item 浏览与编辑框架。

## 3. 什么时候该直接想到它

| 场景 | 说明 |
| --- | --- |
| 你要做自己的 item view | 继承它或继承现成派生类 |
| 你要控制选择、编辑、滚动逻辑 | 重点看它 |
| 你要让一组数据按行/列/树显示 | 它是底层基础 |
| 你要做拖拽排序、内联编辑、持久编辑器 | 它提供基础机制 |

不要把它和 `QWidget` 的普通容器思路混在一起。  
它的世界是“模型索引”，不是“摆几个子控件”。

## 4. 最小可用代码

`QAbstractItemView` 不能直接实例化，通常从 `QTableView`、`QListView` 或 `QTreeView` 开始。

```cpp
auto *view = new QTableView(this);
auto *model = new QStandardItemModel(3, 2, view);

model->setData(model->index(0, 0), "A");
model->setData(model->index(0, 1), 100);
model->setData(model->index(1, 0), "B");
model->setData(model->index(1, 1), 200);

view->setModel(model);
view->setSelectionBehavior(QAbstractItemView::SelectRows);
view->setSelectionMode(QAbstractItemView::SingleSelection);
view->setEditTriggers(QAbstractItemView::DoubleClicked | QAbstractItemView::EditKeyPressed);
```

这段代码体现了它的典型工作方式：

1. 模型先提供数据；
2. 视图决定如何展示；
3. 选择模型记录选中状态；
4. 代理负责画和编辑。

## 5. 这几个概念必须分清

### 5.1 `currentIndex` 和 `selectedIndexes`

- `currentIndex()` 是“当前焦点项”。
- `selectedIndexes()` 是“真正被选中的项集合”。

这两个东西经常同时存在，但语义不同。  
光标落在哪，不等于哪些项被选中。

### 5.2 `selectionMode` 和 `selectionBehavior`

- `selectionMode` 决定能选几个。
- `selectionBehavior` 决定按“项、行、列”哪种粒度选。

### 5.3 `editTriggers`

控制什么动作会启动编辑：

- 双击；
- 当前项变化；
- 键盘快捷键；
- 任意键；
- 已选项再次点击。

### 5.4 `scrollMode`

- `ScrollPerItem`：按项滚动；
- `ScrollPerPixel`：按像素滚动。

表格和树在精细滚动时，`ScrollPerPixel` 更平滑。

### 5.5 `setIndexWidget` 和持久编辑器

- `setIndexWidget()` 是把一个真正的 widget 钉在某个 index 上。
- `openPersistentEditor()` 是让 delegate 的编辑器一直留着。

前者更像静态嵌入，后者更像“永远打开的编辑状态”。

## 6. 视图的核心工作流程

### 6.1 显示

视图需要知道：

- 某个索引在 viewport 上的矩形：`visualRect()`
- 某个坐标对应哪个索引：`indexAt()`
- 某个索引应该滚到哪里：`scrollTo()`

这三个函数是一组。  
做自定义 view 时，先把这三件事跑通，视图就有了空间映射能力。

### 6.2 选择

选择流程通常是：

1. 鼠标或键盘事件到来；
2. `selectionCommand()` 判断这次操作应该如何选择；
3. `setSelection()` 把矩形里的项标记为选中；
4. `selectionChanged()` 槽同步内部状态。

### 6.3 编辑

编辑流程通常是：

1. `edit()` 判断要不要进入编辑；
2. delegate 创建 editor；
3. `setEditorData()` 把模型值填给 editor；
4. `updateEditorGeometry()` 调整 editor 大小；
5. 用户编辑；
6. `commitData()` / `closeEditor()` 收尾。

### 6.4 滚动和重排

视图滚动时，不是简单移动像素：

- 要维护 dirty region；
- 要更新 scrollbar；
- 要考虑懒布局；
- 要让 current/selected/indexWidget 继续对得上。

所以它有 `scheduleDelayedItemsLayout()`、`executeDelayedItemsLayout()`、`updateGeometries()` 这些基础设施。

## 7. 这类 API 怎么读

`QAbstractItemView` 的 API 基本分成六条线：

1. 模型和选择模型
2. 选择行为
3. 编辑触发和代理
4. 索引与坐标映射
5. 滚动与布局
6. 拖拽和状态机

你只要抓住这六条线，成员再多也不会乱。

## 8. 常见坑

### 8.1 `setModel()` 会创建新的选择模型

视图替换模型时，会替你生成新的 `QItemSelectionModel`。  
旧选择模型不会被自动删除，要自己判断是否还被别的视图共享。

### 8.2 视图不拥有模型

`setModel()` 不代表视图接管模型所有权。  
模型通常由 parent 管理。

### 8.3 `setIndexWidget()` 不适合大表格

它会在每个索引上放真实 widget，成本很高。  
大量单元格应该靠 delegate 绘制，而不是靠 widget 堆出来。

### 8.4 row/column delegate 不能乱共享

同一个 delegate 实例不要随便挂给多个视图。  
`closeEditor()` 信号会让多个视图同时收到编辑结束通知，行为很容易混乱。

### 8.5 `update(index)` 和整体刷新不是一回事

它只更新某个索引占据的区域。  
视图全局布局变化应该走 `doItemsLayout()` 或相关的几何更新路径。

## API 速查表
这一节刻意把“给应用代码调用的接口”和“给派生视图实现框架契约的接口”分开。前者用于配置现成的 `QListView`、`QTableView`、`QTreeView`；后者只在你真正编写自定义 item view 时重写。不要为了改变一行的颜色、一个单元格的编辑方式就直接继承 `QAbstractItemView`，优先从现成视图、模型或 delegate 扩展。

### 9.1 枚举和值域

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 选择模式 | `NoSelection` | 禁止用户选择项目 | 仍可有 current index |
| 选择模式 | `SingleSelection` | 一次只允许选择一个项目 | 适合属性表、单选列表 |
| 选择模式 | `MultiSelection` | 允许多选，通常点击切换选中 | 没有 Shift 连续选择语义 |
| 选择模式 | `ExtendedSelection` | 支持 Ctrl、Shift 等扩展选择 | 桌面文件列表和表格常用 |
| 选择模式 | `ContiguousSelection` | 只允许连续区域选择 | 表格块选择场景 |
| 选择粒度 | `SelectItems` | 按单元/项目选择 | 默认粒度，最细 |
| 选择粒度 | `SelectRows` | 点击任意单元时选择整行 | 表格记录列表常用 |
| 选择粒度 | `SelectColumns` | 点击任意单元时选择整列 | 数据分析或列操作工具 |
| 滚动提示 | `EnsureVisible` | 只保证目标 index 可见 | 不强制把它对齐到固定位置 |
| 滚动提示 | `PositionAtTop` | 将目标 index 滚到顶部 | 表格跳转常用 |
| 滚动提示 | `PositionAtBottom` | 将目标 index 滚到底部 | 查看追加日志时有用 |
| 滚动提示 | `PositionAtCenter` | 将目标 index 滚到中间 | 定位搜索结果更醒目 |
| 编辑触发 | `NoEditTriggers` | 不由用户动作自动进入编辑 | 仍可用 `edit(index)` 程序化编辑 |
| 编辑触发 | `CurrentChanged` | current index 改变时尝试编辑 | 容易让导航变成编辑，谨慎使用 |
| 编辑触发 | `DoubleClicked` | 双击进入编辑 | 桌面表格常见默认体验 |
| 编辑触发 | `SelectedClicked` | 已选中项目再次点击进入编辑 | 类似文件重命名体验 |
| 编辑触发 | `EditKeyPressed` | 按平台编辑键进入编辑 | 保留键盘可达性 |
| 编辑触发 | `AnyKeyPressed` | 任意按键都可能启动编辑 | 表格录入快，但会改变导航体验 |
| 编辑触发 | `AllEditTriggers` | 启用全部编辑触发 | 只在明确需要强编辑体验时使用 |
| 滚动模式 | `ScrollPerItem` | 按整项滚动 | 行高固定或项目粒度清楚时使用 |
| 滚动模式 | `ScrollPerPixel` | 按像素滚动 | 平滑滚动；大模型下要关注绘制性能 |
| 拖放模式 | `NoDragDrop` | 禁止拖放 | 默认保守模式 |
| 拖放模式 | `DragOnly` | 只允许从视图拖出数据 | 只做导出或拖到外部时 |
| 拖放模式 | `DropOnly` | 只允许把数据放到视图 | 导入目标列表 |
| 拖放模式 | `DragDrop` | 同时允许拖出和放入 | 模型必须实现对应 MIME 和 drop 支持 |
| 拖放模式 | `InternalMove` | 视图内部移动项目 | 排序/重排列表，模型要正确处理移动 |
| 光标动作 | `MoveUp` / `MoveDown` / `MoveLeft` / `MoveRight` | 方向键导航动作 | 自定义视图在 `moveCursor()` 中解释 |
| 光标动作 | `MoveHome` / `MoveEnd` | 首尾导航动作 | 行列视图语义由派生类决定 |
| 光标动作 | `MovePageUp` / `MovePageDown` | 翻页导航动作 | 通常结合可见区域计算 |
| 光标动作 | `MoveNext` / `MovePrevious` | Tab 或逻辑前后导航 | 受 `tabKeyNavigation` 影响 |
| 内部状态 | `NoState` | 空闲状态 | 子类不要长期停在临时状态 |
| 内部状态 | `DraggingState` | 正在拖拽 | 与 drag/drop 事件配合 |
| 内部状态 | `DragSelectingState` | 正在橡皮筋选择 | 选择区域未最终提交 |
| 内部状态 | `EditingState` | 正在编辑 | delegate editor 存活 |
| 内部状态 | `ExpandingState` | 树节点展开过程中 | `QTreeView` 相关 |
| 内部状态 | `CollapsingState` | 树节点折叠过程中 | `QTreeView` 相关 |
| 内部状态 | `AnimatingState` | 视图正在动画状态 | 少数派生视图使用 |
| 拖放指示 | `OnItem` | drop 指示落在项目上 | 表示覆盖或作为子项，取决于模型语义 |
| 拖放指示 | `AboveItem` | drop 指示在项目上方 | 插入位置在目标前 |
| 拖放指示 | `BelowItem` | drop 指示在项目下方 | 插入位置在目标后 |
| 拖放指示 | `OnViewport` | drop 指示在空白 viewport | 常表示追加或放到根层级 |

### 9.2 模型、选择和代理

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QAbstractItemView(QWidget *parent = nullptr)` | 构造 item view 基类 | 有纯虚函数，不能直接实例化 |
| 生命周期 | `~QAbstractItemView()` | 销毁视图 | 视图不等于模型所有者；旧模型/选择模型按外部所有权处理 |
| 模型 | `setModel(QAbstractItemModel *model)` | 绑定数据模型 | 会影响选择模型和所有 index 语义；替换模型前处理旧选择模型 |
| 模型 | `model() const` | 返回当前模型 | 可能为空；不要长期保存旧 index 跨模型替换使用 |
| 选择模型 | `setSelectionModel(QItemSelectionModel *selectionModel)` | 设置视图使用的选择模型 | 多视图共享选择时使用；模型必须匹配 |
| 选择模型 | `selectionModel() const` | 返回当前选择模型 | 可能由 `setModel()` 自动创建 |
| 默认代理 | `setItemDelegate(QAbstractItemDelegate *delegate)` | 设置默认绘制/编辑代理 | 不要在多个视图之间共享同一个 delegate 实例 |
| 默认代理 | `itemDelegate() const` | 返回默认代理 | 行/列/index 专用代理可能覆盖它 |
| 行代理 | `setItemDelegateForRow(int row, QAbstractItemDelegate *delegate)` | 为某一行设置专用代理 | 适合整行编辑/绘制规则特殊 |
| 行代理 | `itemDelegateForRow(int row) const` | 查询某行专用代理 | 没有专用代理时返回空或默认路径 |
| 列代理 | `setItemDelegateForColumn(int column, QAbstractItemDelegate *delegate)` | 为某一列设置专用代理 | 表格中不同字段类型常用 |
| 列代理 | `itemDelegateForColumn(int column) const` | 查询某列专用代理 | 行代理和列代理冲突时要理解视图选择规则 |
| 索引代理 | `itemDelegateForIndex(const QModelIndex &index) const` | 返回某个 index 实际使用的代理 | 调试编辑器创建和绘制差异时有用 |
| 索引代理 | `itemDelegate(const QModelIndex &index) const` | Qt 6 废弃的按索引查询代理入口 | 使用 `itemDelegateForIndex()` 替代 |
| 选择配置 | `setSelectionMode(SelectionMode mode)` | 设置允许选择几个项目/区域 | 只改变选择规则，不改变模型数据 |
| 选择配置 | `selectionMode() const` | 读取选择模式 | |
| 选择配置 | `setSelectionBehavior(SelectionBehavior behavior)` | 设置按项、行或列选择 | 表格型视图常设置为 `SelectRows` |
| 选择配置 | `selectionBehavior() const` | 读取选择粒度 | |
| 当前项 | `currentIndex() const` | 返回键盘焦点/当前操作 index | 当前项不等于已选项 |
| 根索引 | `rootIndex() const` | 返回当前视图显示的模型根 | 树/列表可从子树开始展示 |

### 9.3 编辑、滚动、外观和交互配置

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 编辑 | `setEditTriggers(EditTriggers triggers)` | 设置哪些用户动作会启动编辑 | 快速录入和只读浏览的触发策略应不同 |
| 编辑 | `editTriggers() const` | 读取编辑触发 flags | |
| 纵向滚动 | `setVerticalScrollMode(ScrollMode mode)` | 设置纵向按项或按像素滚动 | 像素滚动更平滑，但更考验绘制和布局 |
| 纵向滚动 | `verticalScrollMode() const` | 读取纵向滚动模式 | |
| 纵向滚动 | `resetVerticalScrollMode()` | 恢复纵向滚动模式默认值 | 默认由 style 或派生类决定 |
| 横向滚动 | `setHorizontalScrollMode(ScrollMode mode)` | 设置横向按项或按像素滚动 | 宽列表、树视图横向滚动常相关 |
| 横向滚动 | `horizontalScrollMode() const` | 读取横向滚动模式 | |
| 横向滚动 | `resetHorizontalScrollMode()` | 恢复横向滚动模式默认值 | |
| 自动滚动 | `setAutoScroll(bool enable)` | 拖选或拖放到边缘时自动滚动 | 大列表拖拽选择常需要 |
| 自动滚动 | `hasAutoScroll() const` | 查询自动滚动是否开启 | getter 名称不是 `autoScroll()` |
| 自动滚动 | `setAutoScrollMargin(int margin)` | 设置触发自动滚动的边缘范围 | 太大容易误触发，太小拖放困难 |
| 自动滚动 | `autoScrollMargin() const` | 读取自动滚动边距 | |
| Tab 导航 | `setTabKeyNavigation(bool enable)` | 设置 Tab 是否在项目间移动 | 表单嵌套视图时要避免抢走外层焦点导航 |
| Tab 导航 | `tabKeyNavigation() const` | 查询 Tab 导航状态 | |
| 拖放 | `setDropIndicatorShown(bool enable)` | 设置是否显示 drop 指示器 | 只影响视觉反馈，不代表模型能接收 drop |
| 拖放 | `showDropIndicator() const` | 查询 drop 指示器是否显示 | |
| 拖放 | `setDragEnabled(bool enable)` | 设置是否允许从视图拖出 | 模型仍需提供 MIME 数据 |
| 拖放 | `dragEnabled() const` | 查询拖出是否开启 | |
| 拖放 | `setDragDropOverwriteMode(bool overwrite)` | 设置放下时倾向覆盖还是插入 | 表格和列表语义不同，需配合模型实现 |
| 拖放 | `dragDropOverwriteMode() const` | 查询覆盖式 drop 状态 | |
| 拖放 | `setDragDropMode(DragDropMode behavior)` | 设置整体拖放模式 | 只是视图侧开关，模型 flags/MIME/drop 也要配套 |
| 拖放 | `dragDropMode() const` | 读取整体拖放模式 | |
| 拖放 | `setDefaultDropAction(Qt::DropAction dropAction)` | 设置默认 drop action | 与模型支持动作和用户修饰键共同决定最终 action |
| 拖放 | `defaultDropAction() const` | 读取默认 drop action | |
| 外观 | `setAlternatingRowColors(bool enable)` | 开关交替行色 | 适合表格/列表扫描；具体颜色由 palette/style 决定 |
| 外观 | `alternatingRowColors() const` | 查询交替行色状态 | |
| 外观 | `setIconSize(const QSize &size)` | 设置项图标尺寸 | 会影响 delegate 绘制和行高 |
| 外观 | `iconSize() const` | 读取图标尺寸 | |
| 外观 | `setTextElideMode(Qt::TextElideMode mode)` | 设置文本过长时如何省略 | 只影响显示，不改变模型数据 |
| 外观 | `textElideMode() const` | 读取文本省略模式 | |
| 搜索 | `keyboardSearch(const QString &search)` | 根据键盘输入搜索并移动 current index | 匹配规则受 `keyboardSearchFlags` 影响 |
| 搜索 | `keyboardSearchFlags() const` | 读取键盘搜索匹配 flags | |
| 搜索 | `setKeyboardSearchFlags(Qt::MatchFlags searchFlags)` | 设置键盘搜索匹配规则 | 不等于模型过滤，只影响键盘定位 |
| 更新 | `updateThreshold() const` | 读取大范围 `dataChanged()` 更新阈值 | 用于权衡局部索引查找和整体刷新成本 |
| 更新 | `setUpdateThreshold(int threshold)` | 设置更新阈值 | 大模型里可减少极大范围 dataChanged 的计算成本 |

### 9.4 索引定位、编辑器和公共槽

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 坐标映射 | `visualRect(const QModelIndex &index) const` | 返回 index 在 viewport 中的矩形 | 纯虚；自定义视图必须实现，返回 viewport 坐标 |
| 滚动定位 | `scrollTo(const QModelIndex &index, ScrollHint hint = EnsureVisible)` | 把 index 滚动到可见区域 | 纯虚；滚动条 value 应与布局保持一致 |
| 坐标反查 | `indexAt(const QPoint &point) const` | 根据 viewport 坐标返回 index | 纯虚；鼠标命中和悬停依赖它 |
| 尺寸 | `sizeHintForIndex(const QModelIndex &index) const` | 返回某个 index 的建议尺寸 | 通常委托给 delegate |
| 尺寸 | `sizeHintForRow(int row) const` | 返回某行建议高度 | 大模型中频繁调用可能昂贵 |
| 尺寸 | `sizeHintForColumn(int column) const` | 返回某列建议宽度 | 表格列宽计算常用 |
| 持久编辑器 | `openPersistentEditor(const QModelIndex &index)` | 让某个 index 的 delegate editor 一直打开 | 大量使用会创建许多 QWidget，成本高 |
| 持久编辑器 | `closePersistentEditor(const QModelIndex &index)` | 关闭持久编辑器 | 确保未提交数据按 delegate 协议处理 |
| 持久编辑器 | `isPersistentEditorOpen(const QModelIndex &index) const` | 查询持久编辑器是否打开 | 用于避免重复创建 |
| 索引控件 | `setIndexWidget(const QModelIndex &index, QWidget *widget)` | 把真实 QWidget 放到某个 index 上 | 视图接管该 widget；不适合大表格批量使用 |
| 索引控件 | `indexWidget(const QModelIndex &index) const` | 查询某个 index 上的真实 widget | 返回空表示没有 index widget |
| 输入法 | `inputMethodQuery(Qt::InputMethodQuery query) const` | 向输入法报告光标、文本等状态 | 可编辑视图和代理编辑器相关 |
| 公共槽 | `reset()` | 重置视图内部状态 | 模型重置后同步视图缓存 |
| 公共槽 | `setRootIndex(const QModelIndex &index)` | 设置视图显示的根索引 | 只显示模型某个子树时使用 |
| 公共槽 | `doItemsLayout()` | 立即重新布局项目 | 结构或尺寸策略变化后使用 |
| 公共槽 | `selectAll()` | 选中所有可选项目 | 受 selection mode、model flags 影响 |
| 公共槽 | `edit(const QModelIndex &index)` | 程序化进入某项编辑 | 无视用户触发条件，但仍受 index 有效性和 flags 影响 |
| 公共槽 | `clearSelection()` | 清空当前选择 | 不一定清掉 current index |
| 公共槽 | `setCurrentIndex(const QModelIndex &index)` | 设置当前 index | 不等于选择它；必要时同时操作 selection model |
| 公共槽 | `scrollToTop()` | 滚到顶部 | 对大模型可触发布局/加载 |
| 公共槽 | `scrollToBottom()` | 滚到底部 | 日志/列表追加场景常用 |
| 公共槽 | `update(const QModelIndex &index)` | 更新某个 index 对应的 viewport 区域 | 只重绘该项，不重排整个视图 |

### 9.5 信号和模型变化槽

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 鼠标信号 | `pressed(const QModelIndex &index)` | 鼠标按下某项时发出 | 按下不代表激活或选择已完成 |
| 鼠标信号 | `clicked(const QModelIndex &index)` | 单击某项后发出 | 空白处不会产生有效 index |
| 鼠标信号 | `doubleClicked(const QModelIndex &index)` | 双击某项后发出 | 常与编辑触发交叠，避免重复业务动作 |
| 激活信号 | `activated(const QModelIndex &index)` | 项被平台语义激活时发出 | 回车、双击等都可能激活 |
| 悬停信号 | `entered(const QModelIndex &index)` | 鼠标进入某项时发出 | 需要 mouse tracking 才有连续 hover 体验 |
| 悬停信号 | `viewportEntered()` | 鼠标进入 viewport 空白或区域时发出 | 可清除项级 hover 状态 |
| 外观信号 | `iconSizeChanged(const QSize &size)` | 图标尺寸改变时发出 | 同步自定义代理或外部控件 |
| 模型槽 | `dataChanged(const QModelIndex &topLeft, const QModelIndex &bottomRight, const QList<int> &roles = {})` | 模型数据变化后的视图响应 | 子类重写时要处理大范围更新与 roles |
| 模型槽 | `rowsInserted(const QModelIndex &parent, int start, int end)` | 模型插入行后的视图响应 | 更新几何、滚动条和选择状态 |
| 模型槽 | `rowsAboutToBeRemoved(const QModelIndex &parent, int start, int end)` | 模型删除行前的视图响应 | 先处理 current、selection、editor，再让模型删除完成 |
| 选择槽 | `selectionChanged(const QItemSelection &selected, const QItemSelection &deselected)` | 选择变化后的视图响应 | 自定义视图可更新脏区域而非整视图重绘 |
| 当前项槽 | `currentChanged(const QModelIndex &current, const QModelIndex &previous)` | current index 变化后的视图响应 | current 变化不一定伴随 selection 变化 |
| 编辑器槽 | `updateEditorData()` | 用模型数据刷新活动编辑器 | 模型数据变化后保持 editor 同步 |
| 编辑器槽 | `updateEditorGeometries()` | 重新定位活动编辑器 | 滚动、resize、列宽变化后使用 |
| 几何槽 | `updateGeometries()` | 更新滚动条、header、viewport 周边几何 | 子类改变布局后应触发对应更新 |
| 滚动条槽 | `verticalScrollbarAction(int action)` | 响应垂直滚动条动作 | 自定义滚动行为可扩展 |
| 滚动条槽 | `horizontalScrollbarAction(int action)` | 响应水平滚动条动作 | |
| 滚动条槽 | `verticalScrollbarValueChanged(int value)` | 垂直滚动值变化后的响应 | 同步 viewport 偏移和重绘 |
| 滚动条槽 | `horizontalScrollbarValueChanged(int value)` | 水平滚动值变化后的响应 | |
| 编辑器槽 | `closeEditor(QWidget *editor, QAbstractItemDelegate::EndEditHint hint)` | 处理 delegate 请求关闭 editor | `hint` 决定是否提交、移动到下一项等 |
| 编辑器槽 | `commitData(QWidget *editor)` | 处理 delegate 请求提交 editor 数据 | 应进入模型的 `setData()` 流程 |
| 编辑器槽 | `editorDestroyed(QObject *editor)` | editor 对象销毁后的清理 | 防止视图保存悬空 editor 状态 |

### 9.6 自定义视图必须理解的受保护 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 派生构造 | `QAbstractItemView(QAbstractItemViewPrivate &, QWidget *parent = nullptr)` | Qt 内部派生类传入私有实现 | 普通自定义视图使用公开构造 |
| 光标 | `moveCursor(CursorAction action, Qt::KeyboardModifiers modifiers)` | 根据导航动作返回新的 current index | 纯虚；必须结合布局、隐藏项和模型边界 |
| 滚动偏移 | `horizontalOffset() const` | 返回水平滚动偏移 | 纯虚；影响绘制、命中和可见区域 |
| 滚动偏移 | `verticalOffset() const` | 返回垂直滚动偏移 | 纯虚；与滚动条 value 保持一致 |
| 隐藏判断 | `isIndexHidden(const QModelIndex &index) const` | 判断 index 是否隐藏 | 纯虚；选择和命中要跳过隐藏项 |
| 选择区域 | `setSelection(const QRect &rect, QItemSelectionModel::SelectionFlags command)` | 把 viewport 矩形转换为模型选择 | 纯虚；橡皮筋选择核心 |
| 选择区域 | `visualRegionForSelection(const QItemSelection &selection) const` | 把模型选择转换成 viewport 区域 | 纯虚；用于局部重绘 |
| 选择读取 | `selectedIndexes() const` | 返回当前选中的 index 列表 | 可重写以控制返回顺序或过滤隐藏项 |
| 编辑 | `edit(const QModelIndex &index, EditTrigger trigger, QEvent *event)` | 带触发源地尝试进入编辑 | 返回是否成功进入编辑 |
| 选择命令 | `selectionCommand(const QModelIndex &index, const QEvent *event = nullptr) const` | 根据事件推导选择模型命令 | 自定义 Ctrl/Shift/单击规则时重写 |
| 拖拽 | `startDrag(Qt::DropActions supportedActions)` | 启动拖出操作 | 模型 MIME 数据和 supportedActions 要匹配 |
| 样式选项 | `initViewItemOption(QStyleOptionViewItem *option) const` | 初始化 delegate 绘制选项 | 自定义视图传给 delegate 前应正确填充 |
| 状态 | `state() const` | 读取视图内部状态 | 用于调试或派生类避免状态冲突 |
| 状态 | `setState(State state)` | 设置视图内部状态 | 状态改变要成对收尾，避免卡在拖拽/编辑态 |
| 布局调度 | `scheduleDelayedItemsLayout()` | 延迟安排项目布局 | 大量模型变化时合并重排 |
| 布局调度 | `executeDelayedItemsLayout()` | 立即执行延迟布局 | 需要立刻得到准确几何时使用 |
| 脏区域 | `setDirtyRegion(const QRegion &region)` | 标记 viewport 区域需要重绘 | 比整视图 update 更精确 |
| 脏区域 | `scrollDirtyRegion(int dx, int dy)` | 随滚动移动脏区域 | 自定义滚动优化使用 |
| 脏区域 | `dirtyRegionOffset() const` | 读取脏区域偏移 | 绘制优化细节 |
| 自动滚动 | `startAutoScroll()` | 启动拖拽边缘自动滚动 | 与 auto scroll margin 配合 |
| 自动滚动 | `stopAutoScroll()` | 停止自动滚动 | 拖拽结束必须收尾 |
| 自动滚动 | `doAutoScroll()` | 执行一次自动滚动 | 通常由定时器驱动 |
| 焦点 | `focusNextPrevChild(bool next)` | 处理 Tab/Shift+Tab 焦点移动 | `tabKeyNavigation` 会影响是否留在视图内 |

### 9.7 事件扩展点

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 事件 | `event(QEvent *event)` | 处理视图自身通用事件 | 与 viewport 事件分发不同 |
| 事件 | `viewportEvent(QEvent *event)` | 处理 viewport 事件总入口 | 专用事件函数能覆盖的场景优先用专用函数 |
| 鼠标 | `mousePressEvent(QMouseEvent *event)` | 处理按下、选择和编辑准备 | 保留基类可维持默认选择逻辑 |
| 鼠标 | `mouseMoveEvent(QMouseEvent *event)` | 处理拖动、拖选或 hover 移动 | 需要区分拖拽启动和选择框 |
| 鼠标 | `mouseReleaseEvent(QMouseEvent *event)` | 处理鼠标释放收尾 | 清理状态并可能发出 clicked/activated |
| 鼠标 | `mouseDoubleClickEvent(QMouseEvent *event)` | 处理双击 | 与 `DoubleClicked` 编辑触发可能交叠 |
| 拖放 | `dragEnterEvent(QDragEnterEvent *event)` | 拖入视图时触发 | 检查模型是否接受数据 |
| 拖放 | `dragMoveEvent(QDragMoveEvent *event)` | 拖动经过视图时触发 | 更新 drop indicator 和目标 index |
| 拖放 | `dragLeaveEvent(QDragLeaveEvent *event)` | 拖离视图时触发 | 清除 drop indicator |
| 拖放 | `dropEvent(QDropEvent *event)` | 放下数据时触发 | 交给模型完成插入、移动或覆盖 |
| 焦点 | `focusInEvent(QFocusEvent *event)` | 视图获得焦点时触发 | current index 的视觉状态可能变化 |
| 焦点 | `focusOutEvent(QFocusEvent *event)` | 视图失去焦点时触发 | 可能需要关闭编辑器或更新选择外观 |
| 键盘 | `keyPressEvent(QKeyEvent *event)` | 处理导航、选择、编辑快捷键 | 未处理按键要交给基类或忽略 |
| 尺寸 | `resizeEvent(QResizeEvent *event)` | viewport 尺寸变化时触发 | 重算几何和滚动条 |
| 定时器 | `timerEvent(QTimerEvent *event)` | 处理自动滚动、编辑延迟等内部定时 | 子类不要误杀基类定时器 |
| 输入法 | `inputMethodEvent(QInputMethodEvent *event)` | 处理输入法预编辑/提交 | 可编辑视图或自定义编辑逻辑相关 |
| 事件过滤 | `eventFilter(QObject *object, QEvent *event)` | 过滤 editor、viewport 等相关对象事件 | 重写时谨慎保留基类处理 |
| 拖放状态 | `dropIndicatorPosition() const` | 返回当前 drop 指示器位置 | 仅拖放支持启用时有意义 |
| 尺寸 | `viewportSizeHint() const` | 返回 viewport 推荐尺寸 | 从 `QAbstractScrollArea` 继承并重写 |

## 10. 一句话总结

`QAbstractItemView` 是 item view 的总骨架：它把模型、选择模型、代理、滚动、编辑和拖放串成一个完整的视图系统。应用侧配置关注模型、选择和 delegate；自定义 view 则必须保证 index 到 viewport 坐标的映射始终正确。
