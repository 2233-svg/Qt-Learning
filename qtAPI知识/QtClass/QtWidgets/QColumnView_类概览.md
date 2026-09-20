# Qt QColumnView 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QColumnView>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QAbstractItemView -> QColumnView`  
> 定位：级联列视图

## 1. 先建立整体认识：它解决什么问题

`QColumnView` 不是“把树画出来”的另一种 `QTreeView`，而是把树模型按层级拆成一列一列的 `QListView` 风格界面。你在左边列里选中某个节点，右边就出现这个节点的下一层子节点；如果层级再深，右边继续往后展开。它常被叫做 `cascading list`，很适合“边选边深入”的浏览方式。

它解决的是这类问题：

- 文件浏览器里按目录逐级钻取；
- 商品分类、地区选择、组织架构这种层级导航；
- 想看“当前路径”而不是单纯的折叠树；
- 需要为最后一级额外放一个预览区域。

如果你的数据是扁平列表，或者你希望一次看到整棵树的展开状态，那 `QTreeView` 更合适。`QColumnView` 的价值在于“层级清楚、逐步深入、占宽可控”，不是“把所有分支同时摊开”。

```text
QAbstractItemView
  └─ QColumnView
       ├─ 每一层树节点对应一列
       └─ 可选 previewWidget 作为预览区
```

## 2. 最小可用代码

### 2.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

### 2.2 一个最小的级联浏览器

```cpp
#include <QApplication>
#include <QColumnView>
#include <QFileSystemModel>
#include <QDir>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QFileSystemModel model;
    model.setRootPath(QDir::homePath());

    QColumnView view;
    view.setModel(&model);
    view.setRootIndex(model.index(QDir::homePath()));
    view.resize(900, 500);
    view.show();

    return app.exec();
}
```

### 2.3 带预览区的写法

```cpp
#include <QLabel>

auto *preview = new QLabel;
preview->setMinimumWidth(220);
preview->setAlignment(Qt::AlignLeft | Qt::AlignTop);
view.setPreviewWidget(preview);

QObject::connect(&view, &QColumnView::updatePreviewWidget,
                 &view, [&view, preview](const QModelIndex &index) {
    preview->setText(index.data().toString());
});
```

预览区不是自动填充的。`QColumnView` 只负责告诉你“当前索引变了，快更新预览”，真正显示什么内容要你自己填。

## 3. 核心使用模型

### 3.1 一条选择链，拆成多列

`QColumnView` 的工作方式可以简单理解成：

1. 从 `rootIndex()` 开始显示第一列；
2. 当前列里选中一个节点；
3. 如果这个节点还有子节点，就在右侧生成下一列；
4. 新列继续显示下一层内容；
5. 没有子节点时，右侧就不会再长出新列。

所以它特别适合“从父到子逐级走”的界面，不适合那种需要在同一个面板里频繁折叠/展开整个树的场景。

### 3.2 `previewWidget` 是独立的一块区域

预览区的用途不是展示“另一列数据”，而是展示“当前选中项的详细信息”。比如文件浏览器里可以显示文件大小、修改时间、图标；分类浏览器里可以显示说明文字、统计值、缩略图。

它的生命周期也要单独对待：

- 通过 `setPreviewWidget()` 设置；
- 预览控件会成为 `QColumnView` 的子对象；
- 再次设置新控件时，旧控件会被替换并销毁。

### 3.3 列宽和拖拽手柄

`setColumnWidths()` 用来给列预设宽度，`resizeGripsVisible` 决定列之间的拖拽手柄要不要显示。

这两个东西放在一起理解最清楚：

- 想要稳定布局，就预设列宽并隐藏手柄；
- 想让用户自己调列宽，就保留手柄；
- 新创建的列会继承你缓存的宽度列表；
- 列宽列表比当前列数长，超出的值会留给以后新列用。

### 3.4 模型和选择模型

`QColumnView` 不拥有底层模型。你可以把同一个 `QAbstractItemModel` 共享给多个视图，也可以换成自己的 `QItemSelectionModel` 来同步多个界面。

它擅长处理树模型，但数据来源并不局限于 `QFileSystemModel`。只要你的模型有父子关系，`QColumnView` 就能用。

## 4. 适合用在哪里

- 文件管理器的目录浏览区；
- 层级分类选择器；
- 行政区划、组织结构、目录树；
- 想让“当前路径”持续可见的导航界面；
- 需要给末级节点加预览的业务面板。

如果你的场景更像“看整棵树的全貌”，或者分支太多导致横向占位难以接受，那就别硬上 `QColumnView`。

## 5. 常见误区

### 5.1 以为它会像树一样自动展开

不会。它不是折叠树，而是列式导航。你选中什么，就在右边长出什么。

### 5.2 以为预览区会自动显示模型内容

不会。`updatePreviewWidget()` 只是通知信号，内容刷新要你自己连接。

### 5.3 以为 `setColumnWidths()` 只影响当前列

不是。它影响的是“未来会创建的列”也会用到的宽度缓存。

### 5.4 以为 `createColumn()` 可以随便返回一个 QWidget

不行。它返回的是 `QAbstractItemView *`，也就是一个真正的列视图。通常返回 `QListView` 或其子类。

### 5.5 以为 `setModel()` 会接管模型所有权

不会。模型对象仍然归你管理，`QColumnView` 只是使用它。

## 6. 关键 API 怎么理解

### `createColumn()` 和 `initializeColumn()`

这是 `QColumnView` 最核心的扩展点。

- `createColumn()` 负责“造出一列”；
- `initializeColumn()` 负责把主视图的显示风格、行为参数复制过去；
- 如果你重写 `createColumn()`，通常也要调用 `initializeColumn()`，否则新列的外观和主视图会不一致。

### `moveCursor()`

键盘导航是 `QColumnView` 很有味道的一部分：

- 左方向键：回到父节点；
- 右方向键：进入子节点；
- 如果没有子节点，右方向键就按“向下走一项”的逻辑处理。

这让它比普通树视图更像“路径浏览器”。

### `updatePreviewWidget()`

这个信号是你把“当前项变化”和“预览区更新”连起来的桥。

典型做法是：

1. 设置一个预览控件；
2. 连接 `updatePreviewWidget(const QModelIndex &index)`；
3. 在槽里从 `index` 读取数据；
4. 更新预览控件。

### `sizeHint()`

`QColumnView` 的推荐尺寸会随着当前列数变化。列越多，它的宽度通常越大，所以在布局里不要把它当成固定宽度控件。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 属性 | `previewColumnVisible : bool` | 控制预览列是否显示。 | Qt 6.11 新增，默认 `true`。 |
| 属性 | `resizeGripsVisible : bool` | 控制列之间的拖拽手柄是否显示。 | 默认 `true`；关掉后列宽更固定。 |
| 构造 | `QColumnView(QWidget *parent = nullptr)` | 创建一个列视图控件。 | 先建视图，再用 `setModel()` 填数据。 |
| 析构 | `~QColumnView()` | 销毁列视图并释放它拥有的子视图和预览控件。 | 不会替你销毁外部传入但不归它管的模型。 |
| 查询 | `columnWidths() const` | 返回当前记录的列宽列表。 | 可用于保存布局，也会影响后续新列。 |
| 查询 | `isPreviewColumnVisible() const` | 查询预览列当前是否可见。 | 和 `setPreviewColumnVisible()` 配对。 |
| 查询 | `previewWidget() const` | 返回当前预览控件。 | 没设置时返回 `nullptr`。 |
| 查询 | `resizeGripsVisible() const` | 查询列间拖拽手柄是否可见。 | 适合保存/恢复 UI 状态。 |
| 修改 | `setColumnWidths(const QList<int> &list)` | 设置列宽缓存。 | 多出来的值会留给未来新列用，少了则不改后面的列。 |
| 修改 | `setPreviewColumnVisible(bool visible)` | 显示或隐藏预览列。 | 6.11 新增属性接口。 |
| 修改 | `setPreviewWidget(QWidget *widget)` | 设置预览控件。 | 控件会被视图接管并随视图销毁。 |
| 修改 | `setResizeGripsVisible(bool visible)` | 显示或隐藏列间拖拽手柄。 | 想限制用户调宽度时很有用。 |
| 重写公共函数 | `indexAt(const QPoint &point) const` | 根据坐标找出对应的索引。 | 用于命中测试和交互定位。 |
| 重写公共函数 | `scrollTo(const QModelIndex &index, ScrollHint hint = EnsureVisible)` | 滚动到指定索引可见。 | 一般配合路径跳转、程序化定位。 |
| 重写公共函数 | `selectAll()` | 选中当前视图中可选的项。 | 在多列视图里要留意当前焦点列。 |
| 重写公共函数 | `setModel(QAbstractItemModel *model)` | 替换底层模型。 | 视图不接管模型所有权。 |
| 重写公共函数 | `setRootIndex(const QModelIndex &index)` | 设置第一列显示的根索引。 | 相当于决定整条列链从哪一层开始。 |
| 重写公共函数 | `setSelectionModel(QItemSelectionModel *newSelectionModel)` | 替换选择模型。 | 适合同一数据源的多个视图共享选择状态。 |
| 重写公共函数 | `sizeHint() const` | 返回视图的推荐尺寸。 | 会受列数和预览区影响，不要硬当固定值。 |
| 重写公共函数 | `visualRect(const QModelIndex &index) const` | 返回索引在视图中的可见矩形。 | 需要做自定义绘制或定位时才常用。 |
| 信号 | `updatePreviewWidget(const QModelIndex &index)` | 通知外部更新预览控件。 | 预览内容刷新要靠你自己连接这个信号。 |
| 受保护函数 | `createColumn(const QModelIndex &rootIndex)` | 创建一列视图。 | 重写时通常返回 `QListView` 或其子类，且由 `QColumnView` 接管所有权。 |
| 受保护函数 | `initializeColumn(QAbstractItemView *column) const` | 复制主视图的外观和行为到新列。 | 重写 `createColumn()` 时很适合调用它。 |
| 受保护重写 | `isIndexHidden(const QModelIndex &index) const` | 判断某个索引是否应被视图隐藏。 | 影响命中和显示逻辑，子类化时才会碰到。 |
| 受保护重写 | `moveCursor(CursorAction cursorAction, Qt::KeyboardModifiers modifiers)` | 处理键盘光标移动。 | 左右方向键的层级跳转逻辑主要在这里。 |
| 受保护重写 | `resizeEvent(QResizeEvent *event)` | 处理视图尺寸变化。 | 列宽和预览区布局会跟着重算。 |
| 受保护重写 | `setSelection(const QRect &rect, QItemSelectionModel::SelectionFlags command)` | 按矩形范围更新选择。 | 负责拖拽框选之类的选择行为。 |
| 受保护重写 | `visualRegionForSelection(const QItemSelection &selection) const` | 返回选择对应的绘制区域。 | 主要给重绘和高亮逻辑用。 |
| 受保护重写 | `horizontalOffset() const` | 返回水平滚动偏移。 | 属于视图内部滚动计算。 |
| 受保护重写 | `verticalOffset() const` | 返回垂直滚动偏移。 | 属于视图内部滚动计算。 |
| 受保护重写 | `rowsInserted(const QModelIndex &parent, int start, int end)` | 模型插入行后更新列链。 | 用来跟踪模型动态变化。 |
| 受保护重写 | `currentChanged(const QModelIndex &current, const QModelIndex &previous)` | 当前索引变化时同步列和预览。 | 这是列链联动的核心入口之一。 |
| 受保护重写 | `scrollContentsBy(int dx, int dy)` | 处理内容滚动。 | 列区域滚动时由它接手。 |

## 8. 一句话总结

`QColumnView` 是把树模型拆成逐级展开的多列浏览器，特别适合文件浏览、分类导航和带预览的层级选择界面。
