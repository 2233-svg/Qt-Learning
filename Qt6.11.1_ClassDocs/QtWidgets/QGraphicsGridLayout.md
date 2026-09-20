# QGraphicsGridLayout

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsGridLayout`

## 1. 先建立直觉

`QGraphicsGridLayout` 是 Graphics View 的行列布局。它把 `QGraphicsLayoutItem` 放到网格单元里，支持跨行跨列、行列间距、拉伸因子和对齐方式。

它适合场景内复杂面板：左边标签、右边值，多行属性，节点内部端口矩阵，或者小型仪表盘。

## 2. 类说明

`QGraphicsGridLayout` 继承自 `QGraphicsLayout`。它管理的是图形布局项，而不是 QWidget。每个 item 可以占一个单元，也可以 span 多行多列。

布局尺寸来自子项的 minimum/preferred/maximum size、size policy、行列 stretch 和 spacing。它的思路和 `QGridLayout` 相似，但全部使用浮点几何。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `addItem(item, row, column)` | 把 item 放到指定单元。 |
| `addItem(item, row, column, rowSpan, columnSpan)` | 放入跨行跨列区域。 |
| `itemAt(row, column)` | 读取某个单元中的 item。 |
| `itemAt(int)` / `count()` | 按布局索引读取 item 或数量。 |
| `removeAt(int)` | 移除指定索引 item。 |
| `setRowSpacing()` / `rowSpacing()` | 设置或读取某行后的间距。 |
| `setColumnSpacing()` / `columnSpacing()` | 设置或读取某列后的间距。 |
| `setHorizontalSpacing()` / `horizontalSpacing()` | 设置统一水平间距。 |
| `setVerticalSpacing()` / `verticalSpacing()` | 设置统一垂直间距。 |
| `setRowStretchFactor()` / `rowStretchFactor()` | 设置或读取行拉伸权重。 |
| `setColumnStretchFactor()` / `columnStretchFactor()` | 设置或读取列拉伸权重。 |
| `setAlignment(item, alignment)` | 设置 item 在单元区域中的对齐。 |
| `setRowMinimumHeight()` / `setColumnMinimumWidth()` | 设置行/列最小尺寸。 |
| `setRowPreferredHeight()` / `setColumnPreferredWidth()` | 设置行/列首选尺寸。 |
| `setRowMaximumHeight()` / `setColumnMaximumWidth()` | 设置行/列最大尺寸。 |

## 4. 关键用法

```cpp
auto *grid = new QGraphicsGridLayout;
grid->setHorizontalSpacing(8);
grid->setVerticalSpacing(4);

grid->addItem(nameLabel, 0, 0);
grid->addItem(nameEditor, 0, 1);
grid->addItem(typeLabel, 1, 0);
grid->addItem(typeEditor, 1, 1);
grid->setColumnStretchFactor(1, 1);

panel->setLayout(grid);
```

跨列标题：

```cpp
grid->addItem(title, 0, 0, 1, 2);
```

## 5. 使用场景

适合属性表单、节点内部参数区、图形工具面板、场景内仪表、小型数据矩阵、需要标签和值对齐的 UI。

如果只是单列或单行，`QGraphicsLinearLayout` 更简单。网格适合有明确行列关系的内容。

## 6. 常见坑与经验

span 会影响整行整列的尺寸分配。复杂 span 很多时，布局结果不直观，最好把面板拆成几个子布局。

行列 stretch 和 item size policy 要一起看。只设置 stretch，但 item 不愿扩展，也不会得到预期效果。

图形场景里表单不宜过密。缩放后文字和控件需要仍然可读，间距要比普通桌面表单更有余量。
