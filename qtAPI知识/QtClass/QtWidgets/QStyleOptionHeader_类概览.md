# Qt QStyleOptionHeader 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStyleOptionHeader>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QStyleOption -> QStyleOptionHeader`  
> 常见协作者：`QHeaderView`、`QTableView`、`QTreeView`、`QStyle`

## 1. 它解决什么问题

`QTableView` 的列头、`QTreeView` 的表头看上去只是几个矩形，但一个表头 section 实际需要同时表达很多信息：

- 它是横向列头还是纵向行头。
- 它在一组相邻 section 的开头、中间、末尾，还是唯一的一段。
- 当前 section 与已选中 section 是否相邻。
- 文本、图标各是什么，以及如何对齐。
- 是否应显示升序或降序箭头。
- 当前主题下的调色板、字体、按下/悬停/启用等状态。

`QStyleOptionHeader` 就是这一整份“表头 section 绘制说明”。`QHeaderView` 把模型数据和交互状态整理到它中，再交给 `QStyle` 绘制表头背景、标签与排序箭头。

```text
QAbstractItemModel
  └─ 提供 headerData（文字、图标、对齐等）
QHeaderView
  └─ 为每个 logical section 组装 QStyleOptionHeader
QStyle
  ├─ CE_Header：绘制完整表头 section
  ├─ CE_HeaderSection：绘制背景/边框
  ├─ CE_HeaderLabel：绘制文本与图标
  └─ PE_IndicatorHeaderArrow：绘制排序方向箭头
```

它不是表头控件，不保存模型，也不会触发排序。它是一次绘制调用的**值类型参数对象**。

## 2. 什么时候会直接使用

普通的表格和树视图只需配置 `QHeaderView`，通常不必手工构造它：

```cpp
auto *view = new QTableView;
view->horizontalHeader()->setSectionsClickable(true);
view->horizontalHeader()->setSortIndicatorShown(true);
view->setSortingEnabled(true);
```

直接使用 `QStyleOptionHeader` 的典型场景是：

1. **继承 `QHeaderView` 并重写 `paintSection()`**：保留系统表头外观，再增加状态色、额外文字或徽标。
2. **实现 `QStyle` / `QProxyStyle`**：自定义 `CE_Header`、`CE_HeaderLabel` 或排序箭头的样式。
3. **自绘类似表头的复合控件**：希望用 Qt 当前 style 绘制，而不是把边框、图标、文字、RTL 和高对比度逻辑全部手写。

## 3. 构建与绘制入口

### 3.1 CMake 配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

qmake 工程使用 `QT += widgets`。

### 3.2 在 `QHeaderView` 子类中补充绘制

`QHeaderView` 提供了两个很重要的保护函数：

- `initStyleOption(QStyleOptionHeader *)`：填入整个 header 共用的状态。
- `initStyleOptionForIndex(QStyleOptionHeader *, int logicalIndex)`：再填入指定逻辑 section 的模型数据和局部状态。

下面的例子只在“状态”列添加一个细分色条，其余绘制仍交给系统 style：

```cpp
#include <QHeaderView>
#include <QPainter>
#include <QStyleOptionHeader>

class StatusHeader final : public QHeaderView
{
public:
    explicit StatusHeader(Qt::Orientation orientation, QWidget *parent = nullptr)
        : QHeaderView(orientation, parent)
    {
    }

protected:
    void paintSection(QPainter *painter,
                      const QRect &rect,
                      int logicalIndex) const override
    {
        QStyleOptionHeader option;
        initStyleOption(&option);
        initStyleOptionForIndex(&option, logicalIndex);
        option.rect = rect;

        style()->drawControl(QStyle::CE_Header, &option, painter, this);

        if (orientation() == Qt::Horizontal && logicalIndex == 2) {
            painter->fillRect(QRect(rect.left(), rect.bottom() - 3,
                                    rect.width(), 4),
                              QColor("#2d9d78"));
        }
    }
};
```

这里不要自行根据 `logicalIndex == 0` 推断 `position == Beginning`。用户可以拖动 section，模型的 logical index 和视觉顺序可能不同；Qt 填充的 `option.position` 才是 style 应使用的正确语义。

## 4. 一个 section 的数据模型

### 4.1 内容：文本、图标与对齐

| 字段 | 作用 | 默认值 |
| --- | --- | --- |
| `text` | 表头显示的文字。 | 空字符串 |
| `textAlignment` | 文本对齐方式。 | `Qt::AlignLeft` |
| `icon` | 表头图标。 | 空 `QIcon` |
| `iconAlignment` | 图标对齐方式。 | `Qt::AlignLeft` |

这些字段通常来自模型的 `headerData()`。特别是 `textAlignment` 与 `iconAlignment` 是给 style 的意图，不保证所有 style 对所有组合都做像素级相同的排版。

若只想调整业务表格的表头文本，优先在模型里返回合适的 `Qt::DisplayRole`、`Qt::DecorationRole` 与 `Qt::TextAlignmentRole`，不要在绘制代码中硬编码每个标题。

### 4.2 位置：`section`、`orientation` 与 `position`

| 字段 | 回答的问题 | 默认值 |
| --- | --- | --- |
| `section` | 正在画哪个**逻辑** section？ | `0` |
| `orientation` | 这是横向列头还是纵向行头？ | `Qt::Horizontal` |
| `position` | 它在视觉相邻 section 中处于开头、中间、末尾还是唯一项？ | `Beginning` |

`section` 是模型意义上的 logical index；用户拖动列后，它不随视觉位置改变。`position` 反映的是当前视觉相邻关系，主要帮助 style 正确处理首尾圆角、连接边框和分隔线。

```text
视觉顺序：  [逻辑列 3] [逻辑列 0] [逻辑列 2]
position：  Beginning    Middle      End
section：      3           0          2
```

这也是为什么自绘表头应调用 `initStyleOptionForIndex()`，而不是只填一个数字 section。

### 4.3 选择邻接关系：`selectedPosition`

`selectedPosition` 不表示“当前 section 是否被选中”，而是说明它与选中 section 的**相邻关系**。style 可用它把一段连续选中区域画成视觉上连续的块。

| 枚举值 | 含义 |
| --- | --- |
| `NotAdjacent` | 前后都没有选中 section。 |
| `NextIsSelected` | 视觉上的下一个 section 被选中。 |
| `PreviousIsSelected` | 视觉上的上一个 section 被选中。 |
| `NextAndPreviousAreSelected` | 前后两个相邻 section 都被选中。 |

当前 section 的启用、鼠标按下、悬停、焦点、是否处于选择状态等基础状态由继承而来的 `QStyleOption::state` 表示。`selectedPosition` 是给相邻边界绘制的额外信息，不能替代 `state`。

## 5. 排序箭头：外观与业务排序是两回事

`sortIndicator` 只告诉 style 需不需要画箭头、画上箭头还是下箭头：

| 枚举值 | 含义 |
| --- | --- |
| `None` | 不画排序箭头。 |
| `SortUp` | 画向上箭头。 |
| `SortDown` | 画向下箭头。 |

它**不会**排序模型数据。实际排序一般由 `QHeaderView` 的用户操作产生 `sortIndicatorChanged(int, Qt::SortOrder)`，随后连接到模型或代理模型的 `sort()`：

```cpp
auto *header = view->horizontalHeader();
header->setSortIndicatorShown(true);

QObject::connect(header, &QHeaderView::sortIndicatorChanged,
                 proxyModel, &QSortFilterProxyModel::sort);
```

`QTableView::setSortingEnabled(true)` 会处理常见的点击表头排序流程，但数据源仍需支持相应的排序行为。看到箭头不等于数据已经重新排列，手写视图或自定义模型时尤其要确认这一点。

## 6. 枚举与兼容性字段

### 6.1 `SectionPosition`

| 值 | 含义 | 主要影响 |
| --- | --- | --- |
| `Beginning` | 视觉上的第一个 section。 | 首端边框、圆角、分隔线。 |
| `Middle` | 位于中间。 | 与两侧连续 section 的连接。 |
| `End` | 视觉上的最后一个 section。 | 末端边框、圆角。 |
| `OnlyOneSection` | 当前只有一个 section。 | 同时具备首尾边界语义。 |

### 6.2 `StyleOptionType` 与 `StyleOptionVersion`

| 常量 | 值 | 作用 |
| --- | --- | --- |
| `QStyleOptionHeader::Type` | `QStyleOption::SO_Header` | 标识本对象是表头 option。 |
| `QStyleOptionHeader::Version` | `1` | 标识本数据布局版本。 |

自定义 style 从 `QStyleOption *` 接收参数时，可用 `qstyleoption_cast<const QStyleOptionHeader *>(option)` 同时检查 type 与 version。普通 `QHeaderView` 子类不需要手工判断。

`QStyleOptionHeaderV2` 是 `QStyleOptionHeader` 的扩展版本；需要读取 Qt 6 增加的 `textElideMode` 或拖拽目标状态时，再处理 V2。仅需要基础表头信息时，使用本类即可。

## 7. 生命周期、所有权与性能

该类型刻意设计为公开字段、很少成员函数的轻量值类型。一次 `paintSection()` 中在栈上创建、初始化、绘制后离开作用域即可：

```cpp
QStyleOptionHeader option;
initStyleOption(&option);
initStyleOptionForIndex(&option, logicalIndex);
option.rect = rect;
style()->drawControl(QStyle::CE_Header, &option, painter, this);
```

- 它不继承 `QObject`，没有父对象，也不拥有 `QHeaderView`、模型或 `QPainter`。
- 复制构造会复制各字段；不会转移资源所有权。
- 不要缓存指向 `option` 的指针到下一次事件循环。它是当前绘制调用的数据快照。
- 不需要 `new`，更不需要手动 `delete`。

## 8. 常见误区与排查

### 8.1 “自定义表头后，排序箭头、悬停效果都丢了”

通常是重写 `paintSection()` 后用 `QPainter` 直接画了文本。先调用 `initStyleOption()` 与 `initStyleOptionForIndex()`，再调用 `style()->drawControl(QStyle::CE_Header, ...)`；只在这之后叠加自己真正需要的内容。

### 8.2 “拖动列之后，首尾边框画错”

不要由 logical index 判断位置。`section == 0` 不代表视觉上的第一列。应使用 `option.position`，或让 Qt style 按 option 绘制。

### 8.3 “我把 `sortIndicator` 设为 `SortDown`，数据却没排序”

该字段只控制绘制。连接 `sortIndicatorChanged` 到排序逻辑，或启用视图的标准排序支持，并确保 model/proxy model 实现排序。

### 8.4 “文字和图标总是挤在一起”

不要假设 `textAlignment` 与 `iconAlignment` 可以独立提供任意复杂布局。它们是 style 参数；若要做“图标 + 两行文字 + 右侧徽标”这样的复合表头，在保留 `CE_Header` 背景后，自行计算内容矩形并绘制附加层。

### 8.5 “选中列的接缝不自然”

不要只依赖当前 section 的选中状态。连续选中区域的边界依赖 `selectedPosition`，应让 `QHeaderView` 填充 option，或在完全自绘时计算视觉相邻关系。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QStyleOptionHeader()` | 创建并以默认值初始化一份表头 section 绘制参数。 | 直接构造只得到默认快照；自定义 `QHeaderView` 中应继续调用初始化函数。 |
| 构造 | `QStyleOptionHeader(const QStyleOptionHeader &other)` | 创建另一个表头 option 的值副本。 | 复制字段，不关联或接管 `QHeaderView`、模型和 painter。 |
| 枚举 | `SectionPosition` | 描述当前 section 在视觉相邻 section 序列中的位置。 | 用户移动列后，不能用 logical index 推导首尾，应使用该字段。 |
| 枚举值 | `Beginning` | 表示视觉顺序中的第一个 section。 | style 可据此处理首端边框、圆角或分隔线。 |
| 枚举值 | `Middle` | 表示视觉顺序中间的 section。 | 通常前后都有相邻 section，边界绘制应与两侧衔接。 |
| 枚举值 | `End` | 表示视觉顺序中的最后一个 section。 | style 可据此处理末端边框、圆角或收尾分隔线。 |
| 枚举值 | `OnlyOneSection` | 表示 header 当前只有一个 section。 | 同时具备首端和末端语义，不应只按 `Beginning` 处理。 |
| 枚举 | `SelectedPosition` | 描述当前 section 与视觉相邻选中 section 的关系。 | 它不是当前 section 是否选中的布尔值，整体选择仍看 `state`。 |
| 枚举值 | `NotAdjacent` | 当前 section 前后都没有与选中区域相邻的 section。 | 常见于连续选择块的外侧或未参与相邻选择的 section。 |
| 枚举值 | `NextIsSelected` | 视觉上的下一个 section 被选中。 | style 可据此绘制与右侧或下侧选择区域相接的边界。 |
| 枚举值 | `PreviousIsSelected` | 视觉上的上一个或前一个 section 被选中。 | style 可据此绘制与左侧或上侧选择区域相接的边界。 |
| 枚举值 | `NextAndPreviousAreSelected` | 视觉上的前后两个 section 都被选中。 | 当前 section 位于连续选择区域内部，通常不应画外侧边界。 |
| 枚举 | `SortIndicator` | 指定排序箭头是否显示以及显示方向。 | 只表达绘制语义，不会触发模型排序。 |
| 枚举值 | `None` | 表示不绘制排序箭头。 | 不代表模型一定没有排序状态，只表示当前 option 不要求画箭头。 |
| 枚举值 | `SortUp` | 表示绘制向上的排序箭头。 | “向上”与升序的对应关系应以应用和 style 的约定为准。 |
| 枚举值 | `SortDown` | 表示绘制向下的排序箭头。 | 只改变表头视觉提示，实际排序需连接视图和模型逻辑。 |
| 类型常量 | `StyleOptionType::Type` | 提供值为 `SO_Header` 的运行时 option 类型标识。 | style 接收基类指针时优先使用 `qstyleoption_cast()`。 |
| 类型常量 | `StyleOptionVersion::Version` | 表示表头 option 数据布局版本，Qt 6.11.1 中为 `1`。 | 用于 option 兼容识别，不要手工改写。 |
| 公共字段 | `QIcon icon` | 提供当前 section 要绘制的表头图标。 | 通常来自模型的 decoration/header data；空图标仍可能需要保留图标列布局。 |
| 公共字段 | `Qt::Alignment iconAlignment` | 指定图标在 section 中的对齐意图。 | 默认通常是 `Qt::AlignLeft`，具体像素排版由 style 决定。 |
| 公共字段 | `Qt::Orientation orientation` | 指定这是横向列头还是纵向行头。 | 会影响文字、排序箭头和边框的几何方向。 |
| 公共字段 | `SectionPosition position` | 提供当前 section 的视觉首、中、尾位置。 | 与 `section` 的 logical index 不同，列拖动后尤其要区分。 |
| 公共字段 | `int section` | 提供正在绘制的逻辑 section 索引。 | 它是模型意义的索引，不一定等于当前视觉位置。 |
| 公共字段 | `SelectedPosition selectedPosition` | 提供当前 section 与选中邻接区域的关系。 | 用于处理连续选择块的接缝，不能替代 `State_Selected`。 |
| 公共字段 | `SortIndicator sortIndicator` | 提供本次绘制的排序箭头状态。 | 改字段不会改变排序顺序；实际排序由 `QHeaderView`、model 或 proxy model 完成。 |
| 公共字段 | `QString text` | 提供当前 section 的表头标题文字。 | 通常来自模型 header data；改 option 不会持久修改模型。 |
| 公共字段 | `Qt::Alignment textAlignment` | 指定标题文字的对齐意图。 | 默认通常是 `Qt::AlignLeft`；复杂的多行复合表头仍需自定义绘制。 |
| 继承字段 | `QStyleOption::rect` | 指定当前 section 的绘制矩形。 | 在 `paintSection()` 中通常设置为传入的 `rect`，不是整个 header 的矩形。 |
| 继承字段 | `QStyleOption::state` | 提供启用、悬停、按下、选中和焦点等通用状态。 | 通过 `QHeaderView` 初始化取得真实状态，避免只填业务字段而丢交互反馈。 |
| 初始化 | `QHeaderView::initStyleOption(QStyleOptionHeader *)` | 填充 header 级别的通用样式状态。 | 仅在 `QHeaderView` 子类中可调用，通常先调用它。 |
| 初始化 | `QHeaderView::initStyleOptionForIndex(QStyleOptionHeader *, int logicalIndex)` | 填充指定 logical section 的文本、图标、位置和局部状态。 | Qt 6 提供的专用入口，避免手工重建模型数据与视觉映射。 |
| 绘制 | `QStyle::drawControl(QStyle::CE_Header, ...)` | 使用当前 style 绘制完整表头 section。 | 先保留系统绘制，再叠加自定义内容，才能保住主题、RTL 和交互状态。 |

---

### 一句话总结

`QStyleOptionHeader` 是 `QHeaderView` 对“一格表头应如何画”的完整描述：内容字段表达文字和图标，`section` 与 `position` 区分逻辑索引和视觉位置，`selectedPosition` 处理连续选择边界，`sortIndicator` 只画箭头而不排序；自定义表头时先让 `QHeaderView` 填满它，再让 `QStyle` 完成原生绘制。
