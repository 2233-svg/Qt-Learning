# Qt QStyleOptionViewItem 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStyleOptionViewItem>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QStyleOption -> QStyleOptionViewItem`  
> 关键词：`QStyledItemDelegate`、`QAbstractItemView`、模型角色、`CE_ItemViewItem`

## 1. 先说结论：它是一格模型数据的完整绘制上下文

`QStyleOptionViewItem` 是 Qt model/view 框架绘制一个 item 时传给 delegate 和 style 的值对象。

这里的 item 可以是：

- `QListView` 的一项；
- `QTableView` 的一个单元格；
- `QTreeView` 的一个节点在某列中的单元格；
- `QComboBox` 弹出列表中的一项。

它不是模型数据本身，也不是一个可见 `QWidget`。它把模型中与绘制有关的数据、view 的状态和当前单元格的几何整理为一份短生命周期参数：

```text
QAbstractItemModel
  └─ index 的 DisplayRole / DecorationRole / CheckStateRole ...
       |
QAbstractItemView
  └─ rect、选择、焦点、悬停、交替行、当前 widget ...
       |
QStyledItemDelegate::initStyleOption()
       |
QStyleOptionViewItem
       |
QStyle::drawControl(CE_ItemViewItem, ...)
```

普通业务代码一般不手工构造它；自定义 delegate 才会在 `paint()`、`sizeHint()`、编辑器几何更新中读取或修改它。

## 2. 它解决什么问题，和 QModelIndex 的边界在哪里

`QModelIndex` 负责定位模型中“哪一项数据”；`QStyleOptionViewItem` 负责说明“这项数据此刻应怎样画”。

| 对象 | 主要职责 | 是否应长期保存 |
| --- | --- | --- |
| `QModelIndex` | 定位模型中的行、列、父项。 | 模型修改后普通 index 可能失效；需要长期保存用 `QPersistentModelIndex`。 |
| `QAbstractItemModel` | 提供各角色的数据、可编辑性和勾选状态。 | 是数据源。 |
| `QAbstractItemView` | 管理可见区域、选择、焦点、交替行和交互。 | 是显示和交互容器。 |
| `QStyledItemDelegate` | 将模型数据变成绘制/编辑行为。 | 是默认 delegate 实现。 |
| `QStyleOptionViewItem` | 当前这一次绘制的完整视觉上下文。 | 只应在当前调用期间使用。 |

例如，模型里 `Qt::DisplayRole` 返回 `"完成"`，并不表示一定以黑色、左对齐、单行画出来。最终显示还取决于 option 中的字体、调色板、对齐、`textElideMode`、选择状态和可用矩形。

## 3. 最小可用场景：自定义 delegate，不从零手画所有细节

最安全的入门方式是复制 option，调用 `initStyleOption()` 让模型角色填充进去，再只叠加自己确实需要的效果：

```cpp
#include <QPainter>
#include <QStyledItemDelegate>

class PriorityDelegate final : public QStyledItemDelegate
{
public:
    using QStyledItemDelegate::QStyledItemDelegate;

    void paint(QPainter *painter,
               const QStyleOptionViewItem &option,
               const QModelIndex &index) const override
    {
        QStyleOptionViewItem itemOption(option);
        initStyleOption(&itemOption, index);

        QStyledItemDelegate::paint(painter, itemOption, index);

        if (index.data(Qt::UserRole).toString() == "high") {
            painter->save();
            painter->setPen(QPen(Qt::red, 2));
            painter->drawLine(itemOption.rect.topLeft(),
                              itemOption.rect.bottomLeft());
            painter->restore();
        }
    }
};
```

这里 `itemOption` 是当前绘制调用的局部副本。先让默认 delegate 按平台 style 绘制勾选框、图标、选中背景和文字，再加一条优先级标记，通常比从零复刻 item view 外观可靠得多。

## 4. 常用绘制入口：CE_ItemViewItem

完整单元格通常由：

```cpp
style->drawControl(QStyle::CE_ItemViewItem, &option, painter, option.widget);
```

绘制。style 可以通过子元素获取标准区域：

| 子元素 | 得到的矩形 |
| --- | --- |
| `SE_ItemViewItemCheckIndicator` | 勾选框区域。 |
| `SE_ItemViewItemDecoration` | 图标或 decoration 区域。 |
| `SE_ItemViewItemText` | 文字区域。 |
| `SE_ItemViewItemFocusRect` | 焦点框区域。 |

自绘时不要把 `option.rect` 平均切三块来塞勾选框、图标和文字。不同 style、DPI、布局方向、树缩进和选择状态都会影响标准几何；应优先调用 `subElementRect()`。

## 5. 模型角色如何进入 option

`QStyledItemDelegate::initStyleOption(QStyleOptionViewItem *, const QModelIndex &)` 会按 index 填充绘制数据。常见对应关系如下：

| 模型角色 | 常见 option 字段 | 作用 |
| --- | --- | --- |
| `Qt::DisplayRole` | `text`、`features` 中的 `HasDisplay` | 要显示的文字或格式化后的值。 |
| `Qt::DecorationRole` | `icon`、`decorationSize`、`HasDecoration` | 图标或 decoration。 |
| `Qt::CheckStateRole` | `checkState`、`HasCheckIndicator` | 未选、半选、选中状态。 |
| `Qt::TextAlignmentRole` | `displayAlignment` | 文字的对齐策略。 |
| `Qt::FontRole` | `font` | 单元格字体。 |
| `Qt::BackgroundRole` | `backgroundBrush` | 单元格背景刷。 |
| `Qt::ForegroundRole` | `palette` 的文字颜色相关状态 | 前景色通常由调色板处理。 |

不要在 `paint()` 里重复从每个 role 手动组装全部字段，除非你确实要完全替代默认 delegate。正确的默认入口就是 `initStyleOption()`。

## 6. 文字、图标与勾选框

### 6.1 `text`、`displayAlignment`、`textElideMode`

| 字段 | 是什么 | 默认 / 注意点 |
| --- | --- | --- |
| `text` | 当前单元格要画的显示文本。 | 通常来自 `DisplayRole`，不是原始数据的唯一表示。 |
| `displayAlignment` | 文本的对齐方式。 | 默认 `Qt::AlignLeft`。 |
| `textElideMode` | 空间不足时省略号的位置。 | 默认 `Qt::ElideMiddle`；还会受 `SH_ItemView_EllipsisLocation` 影响。 |
| `font` | 当前 item 使用的字体。 | 默认使用应用默认字体；可来自 `FontRole`。 |
| `locale` | 格式化文字、数值和日期所用区域设置。 | 委托的 `displayText()` 应使用它。 |

`text` 并不保证已被省略。若你自行画文字，应根据真实文字区域和 `fontMetrics` 决定是否调用 `elidedText()`；不要将长文本直接画到 `rect`。

### 6.2 `icon`、`decorationPosition`、`decorationAlignment`、`decorationSize`

| 字段 | 是什么 |
| --- | --- |
| `icon` | 当前 item 的 decoration 图标。 |
| `decorationPosition` | decoration 相对文字的位置。 |
| `decorationAlignment` | decoration 在可用 decoration 区内的对齐。 |
| `decorationSize` | decoration 请求的尺寸。 |

`Position` 的取值为：

| 取值 | 含义 |
| --- | --- |
| `Left` | decoration 在文字左侧，默认值。 |
| `Right` | decoration 在文字右侧。 |
| `Top` | decoration 在文字上方。 |
| `Bottom` | decoration 在文字下方。 |

`decorationSize` 默认是 `QSize(-1, -1)`，即 invalid size，不能把它直接当作已确定的 pixmap 大小。图标实际绘制应让 `QIcon` 基于当前 mode、state、DPI 和 style 选择合适资源。

### 6.3 `checkState` 和 `HasCheckIndicator`

勾选框存在与否要先看：

```cpp
option.features.testFlag(QStyleOptionViewItem::HasCheckIndicator)
```

再读取：

```cpp
option.checkState // Qt::Unchecked / PartiallyChecked / Checked
```

不要把 `checkState` 只当作 bool。三态模型中 `Qt::PartiallyChecked` 有独立的视觉语义。

## 7. features：当前 item 具备哪些视觉特征

`features` 是 `ViewItemFeatures`，可组合多个 `ViewItemFeature`：

| 标志 | 值 | 表示什么 |
| --- | --- | --- |
| `None` | `0x00` | 普通 item，没有额外特征。 |
| `WrapText` | `0x01` | 文本可换行。 |
| `Alternate` | `0x02` | 使用交替行背景，通常对应 `alternateBase`。 |
| `HasCheckIndicator` | `0x04` | item 有勾选状态指示器。 |
| `HasDisplay` | `0x08` | item 有显示文本。 |
| `HasDecoration` | `0x10` | item 有 decoration，例如图标。 |
| `IsDecoratedRootColumn` | `0x20` | Qt 6.9 引入；item 带有树视图 branch 绘制部分。 |
| `IsDecorationForRootColumn` | `0x40` | Qt 6.9 引入；item 保存树视图 branch 部分所需信息。 |

这些标志告诉 style“应考虑什么”，不是对模型的反向编辑命令。修改 `option.features` 不会给模型添加图标、勾选能力或自动换行。

树视图的最后两个标志尤其不要想当然地用于所有 column；它们服务于 root column 的分支绘制协作。树分支本身的 primitive 是 `PE_IndicatorBranch`，不要混到一般的 `CE_ItemViewItem` 内容绘制里。

## 8. 选择、焦点、交替行与 decoration 高亮

选择和焦点保存在基类 `state`：

| 状态 | 含义 |
| --- | --- |
| `State_Selected` | 当前 item 已选中。 |
| `State_HasFocus` | item / view 具有焦点相关状态。 |
| `State_Enabled` | item 可用。 |
| `State_MouseOver` | 鼠标悬停在 item 上。 |

`Alternate` 与 `State_Selected` 不是一回事：

- `Alternate` 是交替行背景信息；
- `State_Selected` 是选择模型的当前状态；
- 选中背景通常优先于交替背景，具体由 style 决定。

`showDecorationSelected` 决定 item 选中时图标和树分支 decoration 是否应一起高亮。默认值是 `false`，它与 style hint `QStyle::SH_ItemView_ShowDecorationSelected` 协作。

不要只因为 `State_Selected` 就手动给图标涂成 selection color；应尊重 `showDecorationSelected`、调色板和图标 mode。

## 9. `viewItemPosition` 不是模型列号

`ViewItemPosition` 描述 item 在一行中与同组 item 的位置，用于 style 画连续圆角或连接边界：

| 取值 | 含义 |
| --- | --- |
| `Invalid` | 位置未知，应忽略。 |
| `Beginning` | 该 item 位于一行的开头。 |
| `Middle` | 位于中间。 |
| `End` | 位于末尾。 |
| `OnlyOne` | 一行中唯一的 item，同时是开头和结尾。 |

它不等于 `index.column()`，也不等于当前列是否第一列。一个 style 可以把视觉上连续的多个 item 组合为一段，因此应使用 option 的实际值，不能从模型坐标强行推断。

## 10. `widget`、`index` 和 `backgroundBrush`

| 字段 | 作用 | 重要边界 |
| --- | --- | --- |
| `widget` | 当前 item 所属的 view widget。 | 是非拥有的裸指针，只在调用期间读取。 |
| `index` | 当前被画的模型 index。 | 用于查 role 或做 index 相关判断，不要保存普通 index。 |
| `backgroundBrush` | style 用于绘制 item 背景的刷子。 | 可来自 `BackgroundRole`，通常应让 style 决定与选择背景的组合。 |

`widget` 的存在是为了让 delegate/style 能读取 view 的必要属性，不是让 delegate 对 view 做任意状态修改的许可。绘制过程中改变模型、选择或 view 布局容易造成重入和闪烁。

## 11. 正确扩展 QStyledItemDelegate

### 11.1 修改 option 后继续使用默认绘制

```cpp
void MyDelegate::paint(QPainter *painter,
                       const QStyleOptionViewItem &option,
                       const QModelIndex &index) const
{
    QStyleOptionViewItem itemOption(option);
    initStyleOption(&itemOption, index);

    if (index.data(Qt::UserRole).toBool()) {
        itemOption.font.setBold(true);
    }

    QStyledItemDelegate::paint(painter, itemOption, index);
}
```

这种方式适合文字加粗、改变省略策略、根据业务状态改变调色板等小范围定制。

### 11.2 完整接管绘制时仍使用 style 的标准几何

```cpp
void MyDelegate::paint(QPainter *painter,
                       const QStyleOptionViewItem &option,
                       const QModelIndex &index) const
{
    QStyleOptionViewItem itemOption(option);
    initStyleOption(&itemOption, index);

    const QWidget *view = itemOption.widget;
    QStyle *style = view ? view->style() : QApplication::style();

    style->drawPrimitive(QStyle::PE_PanelItemViewItem,
                         &itemOption, painter, view);

    const QRect textRect = style->subElementRect(
        QStyle::SE_ItemViewItemText, &itemOption, view);

    painter->drawText(textRect, itemOption.displayAlignment, itemOption.text);
}
```

这只是几何关系示例。完整绘制还要处理勾选框、icon、文本省略、选中调色板、RTL、焦点和禁用状态；无明确需求时，优先复用 `QStyledItemDelegate::paint()`。

## 12. 生命周期与线程边界

`QStyleOptionViewItem` 是值类型：

- 不继承 `QObject`，没有 parent；
- 不拥有 model、view、delegate、`widget` 指针或 `QPainter`；
- 复制构造和赋值复制字段值；
- `index` 是普通 `QModelIndex`，模型结构变化后可能失效；
- 从 `paint()` 得到的 `option` 引用和其中 `widget` 指针只应在本次调用中使用；
- model/view 和绘制操作必须在 GUI 线程中完成。

不要缓存 `option.widget` 或传入的 `option` 地址。需要延后处理时，保存稳定业务 key，或根据场景保存 `QPersistentModelIndex`，而不是保存绘制临时数据。

## 13. 默认值与版本勘误

Qt 6.11.1 文档明确给出的常见默认值：

| 字段 | 默认值 |
| --- | --- |
| `displayAlignment` | `Qt::AlignLeft` |
| `decorationAlignment` | `Qt::AlignLeft` |
| `decorationPosition` | `Left` |
| `decorationSize` | `QSize(-1, -1)`，invalid size |
| `textElideMode` | `Qt::ElideMiddle` |
| `showDecorationSelected` | `false` |

类型常量为：

```cpp
QStyleOptionViewItem::Type    // SO_ViewItem
QStyleOptionViewItem::Version // 1
```

Qt 6.11.1 安装头文件将 `Version` 定义为 `1`；离线类页的说明列写成 `4`，与头文件不一致。本笔记以 `C:\Qt\6.11.1\msvc2022_64\include\QtWidgets\qstyleoption.h` 为准。

## 14. 常见误区与排查

### 14.1 “我修改 option，模型数据为什么没变”

option 是绘制副本。修改数据应使用 model 的 `setData()`，或通过编辑器与 delegate 的 `setModelData()` 回写。

### 14.2 “我只画了 text，为什么勾选框和图标不见了”

它们分别依赖 `HasCheckIndicator`、`checkState`、`HasDecoration`、`icon` 和对应的标准几何。除非有意接管全部绘制，否则调用基类 delegate。

### 14.3 “我用 `checkState != 0` 判断勾选”

`PartiallyChecked` 也是有效状态。应明确处理 `Unchecked`、`PartiallyChecked`、`Checked`。

### 14.4 “我的自定义 delegate 在高 DPI 或 RTL 下错位”

不要硬编码 icon、check、text 的坐标。使用 `subElementRect()`、`fontMetrics`、`direction` 和 `QStyle` 的视觉矩形辅助函数。

### 14.5 “我用 `index.column()` 代替 `viewItemPosition`”

两者语义不同。列号是模型坐标；`viewItemPosition` 是 style 需要的视觉连接位置。

## API 速查表
### 15.1 本类直接 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `StyleOptionType` / `Type` | 提供本类运行时类型，值为 `SO_ViewItem`。 | 供 `qstyleoption_cast()` 和 style 识别，不是模型 item 类型。 |
| 类型 | `StyleOptionVersion` / `Version` | 提供 option 数据布局版本，Qt 6.11.1 头文件中为 `1`。 | 以安装头文件为准；版本用于兼容识别。 |
| 枚举 | `Position` | 指定 decoration 相对显示文字的方位。 | 该枚举用于 `decorationPosition`，不是 item 在视图中的位置。 |
| 枚举值 | `Left`、`Right`、`Top`、`Bottom` | 表示 decoration 位于文字左、右、上或下方。 | 默认 `Left`；实际视觉左右还要考虑 RTL 和 style。 |
| 公共字段 | `displayAlignment` | 指定显示文本在文字区域中的对齐方式。 | 默认 `Qt::AlignLeft`；自绘时还要配合 `fontMetrics` 和文本省略。 |
| 公共字段 | `decorationAlignment` | 指定图标或 decoration 在其区域中的对齐方式。 | 默认 `Qt::AlignLeft`；不等于 decoration 的最终矩形。 |
| 公共字段 | `textElideMode` | 指定文本空间不足时省略号出现的位置。 | 默认 `Qt::ElideMiddle`；它是绘制策略，不会修改模型文本。 |
| 公共字段 | `decorationPosition` | 指定 decoration 与显示文本的相对位置。 | 只表达布局意图，实际几何应由 style 或 delegate 计算。 |
| 公共字段 | `decorationSize` | 提供 decoration 的请求尺寸。 | 默认是 invalid size；不能直接当作最终 pixmap 尺寸。 |
| 公共字段 | `font` | 提供当前 item 使用的字体。 | 通常来自 view 或 `FontRole`，字体变化可能影响 size hint。 |
| 公共字段 | `showDecorationSelected` | 指定 item 选中时图标和树 branch decoration 是否跟随高亮。 | 默认 `false`；要结合 `SH_ItemView_ShowDecorationSelected` 和 palette 理解。 |
| 枚举 | `ViewItemFeature` | 定义 item 具备哪些可组合的视觉特征。 | 使用 `ViewItemFeatures::testFlag()` 查询，不要把它当成模型能力开关。 |
| 标志值 | `None` | 表示没有额外视觉特征。 | 普通 item 的基础状态。 |
| 标志值 | `WrapText` | 表示文本允许换行。 | size hint 和绘制都要按多行文本处理。 |
| 标志值 | `Alternate` | 表示使用交替行背景。 | 不等于选中；选中背景通常由 style 另行优先处理。 |
| 标志值 | `HasCheckIndicator` | 表示 item 需要绘制勾选指示器。 | 只有该标志存在时才应读取 `checkState` 进行绘制。 |
| 标志值 | `HasDisplay` | 表示 item 有可显示文本。 | 文本内容位于 `text`，没有该标志时不要强行画空文字区。 |
| 标志值 | `HasDecoration` | 表示 item 有图标或其他 decoration。 | 具体 decoration 通常位于 `icon` 等字段。 |
| 标志值 | `IsDecoratedRootColumn` | Qt 6.9 起表示该 item 带有树视图 branch 绘制部分。 | 仅用于树视图 root-column 协作，不要用于普通 list/table item。 |
| 标志值 | `IsDecorationForRootColumn` | Qt 6.9 起表示该 item 保存 root column branch 所需 decoration 信息。 | 只服务树视图分支绘制，不是普通图标存在性的判断。 |
| 标志类型 | `ViewItemFeatures` | `ViewItemFeature` 的 `QFlags` 集合。 | 多个特征可以同时存在，使用 flags 操作。 |
| 公共字段 | `features` | 提供当前 item 的视觉特征集合。 | 反映当前绘制上下文，不会给模型添加图标、勾选或换行能力。 |
| 公共字段 | `locale` | 提供显示文本、数值和日期格式化使用的区域设置。 | delegate 的 `displayText()` 等逻辑应尊重它。 |
| 公共字段 | `widget` | 指向所属 item view 的非拥有指针。 | 只在当前 paint/sizeHint 调用期间读取，不能缓存或删除。 |
| 枚举 | `ViewItemPosition` | 描述 item 在一行中与其他 item 的视觉连接位置。 | 不等于模型列号，也不能从 `index.column()` 强行推导。 |
| 枚举值 | `Invalid` | 表示视觉位置未知。 | style 应忽略该位置信息，不要当成首项。 |
| 枚举值 | `Beginning`、`Middle`、`End` | 表示 item 位于视觉行的开头、中间或末尾。 | style 可据此连接边框、圆角和连续选择背景。 |
| 枚举值 | `OnlyOne` | 表示 item 是该行中唯一项目。 | 同时具有视觉开头和结尾语义。 |
| 公共字段 | `index` | 提供正在绘制的模型 index。 | 模型结构变化后普通 index 可能失效，不要跨调用长期保存。 |
| 公共字段 | `checkState` | 提供 `Unchecked`、`PartiallyChecked` 或 `Checked` 状态。 | 必须明确处理三态，不要只转换成 bool。 |
| 公共字段 | `icon` | 提供 item 的 decoration 图标。 | `QIcon` 会按 mode、state、DPI 和 style 选择实际资源。 |
| 公共字段 | `text` | 提供 item 的显示文字。 | 自绘时要根据标准 text rect 和 `textElideMode` 处理省略。 |
| 公共字段 | `viewItemPosition` | 提供 item 在视觉行中的位置。 | 不是 `index.column()`，由 view/delegate 的实际布局语义决定。 |
| 公共字段 | `backgroundBrush` | 提供 item 背景绘制使用的画刷。 | 要与选中背景、palette 和 style 的优先级协作。 |
| 构造 | `QStyleOptionViewItem()` | 创建一份带默认值的 item 绘制 option。 | 不会自动读取任何 model index 的角色数据。 |
| 构造 | `QStyleOptionViewItem(const QStyleOptionViewItem &other)` | 创建另一个 item option 的字段副本。 | 不复制 model、view、delegate 或 `widget` 指向对象的所有权。 |
| 赋值 | `operator=(const QStyleOptionViewItem &other)` | 将另一个 item option 的字段复制到当前对象。 | 仍然只是当前绘制状态的值复制。 |
| 保护构造 | `QStyleOptionViewItem(int version)` | 按指定版本构造 option，供兼容扩展使用。 | `protected`，普通 delegate 通常直接使用默认构造。 |

### 15.2 协作 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 初始化 | `QStyledItemDelegate::initStyleOption(QStyleOptionViewItem *, const QModelIndex &)` | 根据模型角色、index 和 view 状态填充完整 item option。 | 自定义 delegate 的首选入口；不要在 paint 中重复手工拼装所有字段。 |
| 绘制 | `QStyledItemDelegate::paint(...)` | 按当前 style 绘制完整 item，包括背景、check、icon、文字和焦点。 | 只改少量字段时优先调用它，避免丢失平台和 RTL 细节。 |
| 尺寸 | `QStyledItemDelegate::sizeHint(...)` | 计算 item 的推荐尺寸。 | `WrapText`、图标、字体和 editor 状态变化时要同步考虑。 |
| 绘制 | `QStyle::drawControl(QStyle::CE_ItemViewItem, ...)` | 让当前 style 绘制完整单元格。 | option 应为本类，且 `widget` 要指向合适的 view 或为空。 |
| 几何 | `QStyle::subElementRect(QStyle::SE_ItemViewItemText, ...)` | 获取标准文字绘制区域。 | 适合自绘文字，避免硬编码 icon/check/text 的位置。 |
| 几何 | `QStyle::subElementRect(QStyle::SE_ItemViewItemCheckIndicator, ...)` / `SE_ItemViewItemDecoration` | 获取勾选框或 decoration 的标准区域。 | 只有完整接管绘制时才需要自己画这些区域。 |
| 绘制 | `QStyle::drawPrimitive(QStyle::PE_PanelItemViewItem, ...)` | 绘制 item 面板背景。 | 完整自绘时可先绘制面板，再处理 check、icon 和文字。 |
| 样式提示 | `QStyle::styleHint(QStyle::SH_ItemView_ShowDecorationSelected, ...)` | 查询 decoration 是否随 item 选择状态高亮。 | 与 `showDecorationSelected` 共同决定图标/branch 的选择外观。 |
| 样式提示 | `QStyle::styleHint(QStyle::SH_ItemView_EllipsisLocation, ...)` | 查询 item 默认的文本省略位置偏好。 | 影响默认 `textElideMode`，但自绘时仍要用实际文字区域计算。 |
| 模型 | `QAbstractItemModel::data(const QModelIndex &, int role)` | 读取 Display、Decoration、CheckState、Font 等角色数据。 | delegate 应优先让 `initStyleOption()` 统一读取。 |
| 模型 | `QAbstractItemModel::setData(const QModelIndex &, const QVariant &, int role)` | 将编辑结果写回模型。 | 修改 option 不会回写模型；写入要走 model 的 setData。 |
| 视图 | `QAbstractItemView::setItemDelegate(QAbstractItemDelegate *)` | 为 view 安装自定义 delegate。 | delegate 的生命周期通常由 view 管理，仍要注意替换旧 delegate 的所有权。 |

---

### 一句话总结

`QStyleOptionViewItem` 是 item view 的“一格绘制合同”：模型角色提供文字、图标、勾选和字体，view 提供矩形、选择和交互状态，delegate 把它们填入 option，style 再用 `CE_ItemViewItem` 画出最终效果。自定义 delegate 应先复制并初始化 option，再只改变确实需要的字段。
