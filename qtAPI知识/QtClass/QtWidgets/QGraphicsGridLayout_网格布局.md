<!-- 依据 Qt 6.11.1 头文件 qgraphicsgridlayout.h 整理。 -->

# QGraphicsGridLayout 深入笔记

> 头文件：`#include <QGraphicsGridLayout>`  
> 模块：`Qt6::Widgets`  
> 继承：`QGraphicsLayoutItem -> QGraphicsLayout -> QGraphicsGridLayout`

## 1. 它解决什么问题

`QGraphicsGridLayout` 把 `QGraphicsLayoutItem` 放进二维的“行 x 列”网格。与 `QGraphicsLinearLayout` 只沿一条主轴排列不同，它能同时表达：

- 标签在第 0 列、编辑器在第 1 列。
- 一个标题跨越两列。
- 左列按内容宽度，右列吸收额外宽度。
- 某一行固定高度，另一行在面板变高时扩张。

它适合 Graphics View 中的属性表、带标签的表单、工具面板和节点详情区。普通 `QWidget` 界面应使用 `QGridLayout`；本类面向 `QGraphicsWidget`、`QGraphicsProxyWidget` 或其它 `QGraphicsLayoutItem`。

```text
QGraphicsWidget
  └─ QGraphicsGridLayout
       ├─ (0, 0) 标签
       ├─ (0, 1) 编辑器
       └─ (1, 0..1) 跨两列的说明
```

## 2. 最小使用路径

```cpp
#include <QGraphicsGridLayout>
#include <QGraphicsWidget>

auto *panel = new QGraphicsWidget;
auto *layout = new QGraphicsGridLayout(panel);

auto *nameLabel = new QGraphicsWidget;
auto *nameEdit = new QGraphicsWidget;
auto *hint = new QGraphicsWidget;

layout->setContentsMargins(12, 10, 12, 10);
layout->setHorizontalSpacing(8);
layout->setVerticalSpacing(6);
layout->addItem(nameLabel, 0, 0, Qt::AlignRight | Qt::AlignVCenter);
layout->addItem(nameEdit, 0, 1);
layout->addItem(hint, 1, 0, 1, 2);
layout->setColumnStretchFactor(1, 1);
```

`panel` 会接管顶层布局；布局会接管加入的 layout item。一个 item 不能同时属于两个布局。

## 3. 先分清四层规则

网格最终尺寸不是简单的“每格等分”，而是四层规则共同求解：

1. **item 自己的尺寸提示和 `QSizePolicy`**：内容至少需要多少，能否扩张。
2. **行/列最小、首选、最大尺寸**：限制整行或整列。
3. **行/列 stretch factor**：分配主容器剩余宽高的权重。
4. **item、行、列的 alignment**：当格子比 item 大时，决定 item 在格子中的位置。

因此，右侧编辑器没有变宽时，不要只加 `setColumnStretchFactor(1, 1)`；还要检查编辑器是否允许水平扩张、是否被最大宽度限制。

## 4. 放入单元格与跨行跨列

```cpp
layout->addItem(label, 0, 0);
layout->addItem(editor, 0, 1);
layout->addItem(description, 1, 0, 1, 2);
```

第二种 `addItem()` 的 `rowSpan` 和 `columnSpan` 指定占用范围。跨列标题、跨行预览图、底部横跨整个面板的操作栏都应使用它，而不是人为插入空 item。

坐标从 `0` 开始。网格的 `rowCount()`、`columnCount()` 由被占用的最大行/列索引确定，末尾没有 item 的空行空列不计数。动态删除末尾 item 后，行列数可能变小，不应把它当稳定业务 ID。

`itemAt(row, column)` 能查询某个格子所处的 item。该格子若属于一个跨行跨列 item，返回的仍是这个 item；未占用时返回 `nullptr`。

## 5. 间距：全局、行、列三个粒度

```cpp
layout->setSpacing(8);          // 横向和纵向默认都是 8
layout->setHorizontalSpacing(10);
layout->setVerticalSpacing(6);
layout->setColumnSpacing(0, 14);
layout->setRowSpacing(2, 18);
```

- `setSpacing()`：统一设置横纵默认间距。
- `setHorizontalSpacing()` / `setVerticalSpacing()`：按方向设置默认间距。
- `setColumnSpacing(column, ...)`：设置该列右侧到下一列的局部水平间距。
- `setRowSpacing(row, ...)`：设置该行下方到下一行的局部垂直间距。

局部行列间距以索引为准，动态增删后含义可能移动。内容与面板边缘之间的空白仍由继承的 `setContentsMargins()` 管理，别把它和格子之间的 spacing 混在一起。

## 6. 行列尺寸和 stretch

### 尺寸边界

```cpp
layout->setColumnMinimumWidth(0, 72);
layout->setColumnPreferredWidth(1, 220);
layout->setColumnMaximumWidth(0, 120);
layout->setRowFixedHeight(3, 32);
```

- minimum：该行/列不会低于此下限。
- preferred：有足够空间时的理想目标，不是强制固定值。
- maximum：限制该行/列不再增长。
- fixed：把 minimum 和 maximum 同时设为同一个值。

行列约束会与其中 item 的尺寸要求一起参与求解。硬编码 fixed 尺寸适合图标栏、固定按钮行；正文、编辑器和翻译文本一般应优先使用 preferred + stretch。

### 剩余空间

```cpp
layout->setColumnStretchFactor(0, 0);
layout->setColumnStretchFactor(1, 1);
layout->setRowStretchFactor(2, 1);
```

多余宽度按列 stretch 分配，多余高度按行 stretch 分配。因子为 `0` 表示没有显式优先权，不代表绝不增长；最终还受 item 的 `QSizePolicy`、最小/最大尺寸影响。

## 7. 三种对齐级别

```cpp
layout->setAlignment(button, Qt::AlignRight);
layout->setColumnAlignment(0, Qt::AlignRight);
layout->setRowAlignment(0, Qt::AlignVCenter);
```

- `setAlignment(item, ...)`：只影响一个 item。
- `setColumnAlignment(column, ...)`：给这一列的 item 设默认对齐倾向。
- `setRowAlignment(row, ...)`：给这一行的 item 设默认对齐倾向。

item 对齐最具体。对齐只有在 cell 大于 item 时才明显；允许扩张的编辑器通常会填满格子，固定宽度按钮才更容易看出 `AlignRight` 或 `AlignHCenter`。

## 8. 移除与生命周期

```cpp
QGraphicsLayoutItem *item = layout->itemAt(0);
layout->removeAt(0);
delete item; // 仅在 item 不再被图元父子树拥有且不再使用时
```

`removeAt()` 与 `removeItem()` 会将 item 从布局摘下，并将其所有权转交给调用者；它们不销毁 item。若 item 同时有 `QGraphicsItem` 父对象，仍要按图元树实际所有权处理，避免重复释放。

临时隐藏一块内容时，优先让对应图元不可见或调整其尺寸策略；频繁删除、重建网格结构会让行列规则和局部间距更难维护。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QGraphicsGridLayout(QGraphicsLayoutItem *parent = nullptr)` | 创建网格布局。 | 传入根 `QGraphicsWidget` 时成为其顶层布局。 |
| 析构 | `virtual ~QGraphicsGridLayout()` | 销毁网格布局。 | 已安装时通常由宿主 widget 管理。 |
| 添加 | `void addItem(QGraphicsLayoutItem *item, int row, int column, Qt::Alignment alignment = {})` | 将 item 放入单个格子。 | 行列从 `0` 开始；item 不能已属于其它布局。 |
| 添加 | `void addItem(QGraphicsLayoutItem *item, int row, int column, int rowSpan, int columnSpan, Qt::Alignment alignment = {})` | 将 item 放入跨行/跨列区域。 | span 定义占用范围，适合标题、预览区和操作栏。 |
| item 对齐 | `void setAlignment(QGraphicsLayoutItem *item, Qt::Alignment alignment)` | 设置一个 item 在其 cell 中的对齐。 | 最具体的对齐规则；填满 cell 时不明显。 |
| item 对齐 | `Qt::Alignment alignment(QGraphicsLayoutItem *item) const` | 查询 item 对齐。 | 仅对本布局的直接 item 有意义。 |
| 行对齐 | `void setRowAlignment(int row, Qt::Alignment alignment)` | 设置一行的默认对齐。 | 可能被 item 级对齐覆盖。 |
| 行对齐 | `Qt::Alignment rowAlignment(int row) const` | 查询行对齐。 | 传入有效行索引。 |
| 列对齐 | `void setColumnAlignment(int column, Qt::Alignment alignment)` | 设置一列的默认对齐。 | 常用于标签列右对齐。 |
| 列对齐 | `Qt::Alignment columnAlignment(int column) const` | 查询列对齐。 | 不等于每个 item 的最终 visual geometry。 |
| 行数 | `int rowCount() const` | 返回最后被占用行决定的行数。 | 尾部空行不计入；动态删除后值可变。 |
| 列数 | `int columnCount() const` | 返回最后被占用列决定的列数。 | 尾部空列不计入。 |
| 格子查询 | `QGraphicsLayoutItem *itemAt(int row, int column) const` | 返回占用指定格子的 item。 | 未占用返回 `nullptr`；跨度中的任一格都能查到该 item。 |
| 容器查询 | `int count() const` | 返回布局直接管理的 item 数量。 | 跨行跨列 item 仍只计一次。 |
| 容器查询 | `QGraphicsLayoutItem *itemAt(int index) const` | 按插入索引返回 item。 | 越界返回空；不转移所有权。 |
| 移除 | `void removeItem(QGraphicsLayoutItem *item)` | 摘下指定 item。 | 所有权交回调用者，不会自动删除。 |
| 移除 | `void removeAt(int index)` | 按索引摘下 item。 | 同样转移所有权；先核实索引。 |
| 默认间距 | `void setSpacing(qreal spacing)` | 同时设置横向、纵向默认间距。 | 只影响未做局部覆盖的行列间距。 |
| 横向间距 | `void setHorizontalSpacing(qreal spacing)` | 设置默认列间距。 | 与 `setColumnSpacing()` 的局部覆盖不同。 |
| 横向间距 | `qreal horizontalSpacing() const` | 查询默认列间距。 | 不代表每一列后的最终局部间距。 |
| 纵向间距 | `void setVerticalSpacing(qreal spacing)` | 设置默认行间距。 | 与 `setRowSpacing()` 的局部覆盖不同。 |
| 纵向间距 | `qreal verticalSpacing() const` | 查询默认行间距。 | 不代表每一行后的最终局部间距。 |
| 行间距 | `void setRowSpacing(int row, qreal spacing)` | 设置该行后的局部垂直间距。 | 增删行后检查索引语义。 |
| 行间距 | `qreal rowSpacing(int row) const` | 查询该行后的间距。 | 通常用于排查局部覆盖。 |
| 列间距 | `void setColumnSpacing(int column, qreal spacing)` | 设置该列后的局部水平间距。 | 增删列后检查索引语义。 |
| 列间距 | `qreal columnSpacing(int column) const` | 查询该列后的间距。 | 仅影响与下一列之间空隙。 |
| 行伸缩 | `void setRowStretchFactor(int row, int stretch)` | 设置行的剩余高度权重。 | `0` 不等于禁止增长；受 item 策略影响。 |
| 行伸缩 | `int rowStretchFactor(int row) const` | 查询行伸缩权重。 | 主用于解释多余高度如何分配。 |
| 列伸缩 | `void setColumnStretchFactor(int column, int stretch)` | 设置列的剩余宽度权重。 | 编辑器列通常设正值。 |
| 列伸缩 | `int columnStretchFactor(int column) const` | 查询列伸缩权重。 | 主用于解释多余宽度如何分配。 |
| 行最小值 | `void setRowMinimumHeight(int row, qreal height)` | 设置行最小高度。 | 过大将挤压其它行。 |
| 行最小值 | `qreal rowMinimumHeight(int row) const` | 查询行最小高度。 | 与 item 自身最小高度一起生效。 |
| 行首选值 | `void setRowPreferredHeight(int row, qreal height)` | 设置行首选高度。 | 是建议值，不是固定值。 |
| 行首选值 | `qreal rowPreferredHeight(int row) const` | 查询行首选高度。 | 用于诊断尺寸协商。 |
| 行最大值 | `void setRowMaximumHeight(int row, qreal height)` | 设置行最大高度。 | 可能阻止该行吸收剩余空间。 |
| 行最大值 | `qreal rowMaximumHeight(int row) const` | 查询行最大高度。 | 需与 minimum 保持合理关系。 |
| 行固定值 | `void setRowFixedHeight(int row, qreal height)` | 将行高固定为一个值。 | 同时约束最小和最大高度；谨慎用于可翻译内容。 |
| 列最小值 | `void setColumnMinimumWidth(int column, qreal width)` | 设置列最小宽度。 | 标签列可设下限，避免文字过度压缩。 |
| 列最小值 | `qreal columnMinimumWidth(int column) const` | 查询列最小宽度。 | 与 item 最小宽度一起生效。 |
| 列首选值 | `void setColumnPreferredWidth(int column, qreal width)` | 设置列首选宽度。 | 适合编辑器列的初始期望。 |
| 列首选值 | `qreal columnPreferredWidth(int column) const` | 查询列首选宽度。 | 不是强制宽度。 |
| 列最大值 | `void setColumnMaximumWidth(int column, qreal width)` | 设置列最大宽度。 | 防止小控件列吞掉剩余宽度。 |
| 列最大值 | `qreal columnMaximumWidth(int column) const` | 查询列最大宽度。 | 需与 minimum 保持合理关系。 |
| 列固定值 | `void setColumnFixedWidth(int column, qreal width)` | 将列宽固定为一个值。 | 同时设置最小和最大宽度；响应式界面少用。 |
| 布局生命周期 | `void invalidate()` | 作废网格内部计算缓存。 | 常规 setter 已会触发；业务代码很少显式调用。 |
| 布局生命周期 | `void setGeometry(const QRectF &rect)` | 根据行列规则为所有 item 分配矩形。 | 框架调用，不要用它替代行列约束。 |
| 尺寸协商 | `QSizeF sizeHint(Qt::SizeHint which, const QSizeF &constraint = QSizeF()) const` | 返回网格的尺寸建议。 | 由父布局用来协商最小、首选和最大尺寸。 |

## 10. 排查清单

1. item 跑到错误位置：核对 row、column 和 span，不要把“第几项”误当成格子坐标。
2. 右列不扩张：检查列 stretch、编辑器的 `QSizePolicy` 与最大宽度。
3. 间距不一致：分别检查 contents margins、默认 spacing、row/column 局部 spacing。
4. 固定行列导致文本裁切：把 `setRowFixedHeight()` / `setColumnFixedWidth()` 换成首选值和合理下限。
5. 删除后泄漏或崩溃：`removeAt()` / `removeItem()` 不删除 item，调用者要按实际图元树处理。

### 一句话总结

`QGraphicsGridLayout` 用行列规则组织 Graphics View 面板：span 表达跨格，行列尺寸与 stretch 管空间分配，对齐处理 cell 内余量，局部 spacing 负责少数例外，而 item 移除后的生命周期必须由调用者明确接管。
