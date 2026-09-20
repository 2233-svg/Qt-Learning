# QStyleOptionHeader

> Qt 6.11.1 · Qt Widgets · 来自 `QStyleOptionHeader`

## 1. 先建立直觉

`QStyleOptionHeader` 是 header section 的绘制参数包。表格列头、树视图表头、列表 header 都需要描述文字、图标、排序箭头、相邻 section 位置。

它让 `QHeaderView` 或 delegate 风格代码能按平台规则画出表头。

## 2. 类说明

`QStyleOptionHeader` 继承自 `QStyleOption`。它包含 `section`、`text`、`icon`、`position`、`selectedPosition`、`sortIndicator`、`orientation` 等字段。

header 的视觉不仅取决于当前 section，还取决于它在整组 section 中的位置，例如第一个、中间、最后一个，选中邻居也会影响边界绘制。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `section` | 当前 section 索引。 |
| `text` | 表头文本。 |
| `icon` / `iconAlignment` | 表头图标和对齐。 |
| `textAlignment` | 文本对齐。 |
| `orientation` | 水平表头或垂直表头。 |
| `position` | 当前 section 在连续区域中的位置。 |
| `selectedPosition` | 与选中 section 的相邻关系。 |
| `sortIndicator` | 排序箭头状态。 |
| `QStyle::CE_Header` | 绘制完整 header section。 |
| `QStyle::CE_HeaderSection` | 绘制 section 背景。 |
| `QStyle::CE_HeaderLabel` | 绘制 header 文本/图标。 |

## 4. 关键用法

```cpp
QStyleOptionHeader opt;
opt.initFrom(header);
opt.section = logicalIndex;
opt.text = model->headerData(logicalIndex, Qt::Horizontal).toString();
opt.orientation = Qt::Horizontal;
opt.sortIndicator = QStyleOptionHeader::SortDown;

style()->drawControl(QStyle::CE_Header, &opt, painter, header);
```

## 5. 使用场景

适合自定义 `QHeaderView`、表格/树 header 绘制、style 实现、带排序/筛选状态的表头。

普通表格只设置模型 headerData 即可，不需要直接操作它。

## 6. 常见坑与经验

排序箭头不是文本的一部分。用 `sortIndicator` 交给 style 画，位置和尺寸更稳。

section 的首尾位置会影响边框。自绘 header 时忽略 `position` 容易出现双线或漏线。

垂直 header 和水平 header 的布局规则不同，orientation 要准确。
