# QStyleOptionViewItem

> Qt 6.11.1 · Qt Widgets · 来自 `QStyleOptionViewItem`

## 1. 先建立直觉

`QStyleOptionViewItem` 是模型/视图 delegate 绘制单元格或条目的参数包。列表项、表格单元格、树节点显示时，delegate 会把文本、图标、勾选状态、装饰位置、选中状态等放进它。

如果你写过 `QStyledItemDelegate::paint()`，它就是最重要的输入之一。

## 2. 类说明

`QStyleOptionViewItem` 继承自 `QStyleOption`。它描述一个 item view 单元的视觉状态和内容，包括 `index`、`text`、`icon`、`checkState`、`features`、`viewItemPosition`、`decorationSize` 等。

默认 delegate 会用它调用当前 style 绘制 `CE_ItemViewItem`。自定义 delegate 最稳的做法是先让 style 画基础，再叠加自己的内容。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `index` | 当前模型索引。 |
| `text` | 显示文本。 |
| `icon` | 装饰图标。 |
| `checkState` | 复选状态。 |
| `features` | 是否有 display、decoration、check indicator 等特性。 |
| `decorationSize` / `decorationPosition` | 图标尺寸和位置。 |
| `displayAlignment` | 文本对齐。 |
| `textElideMode` | 文本省略方式。 |
| `viewItemPosition` | 在一组连续项中的位置，影响圆角/边界。 |
| `showDecorationSelected` | 选中时图标是否也呈选中态。 |
| `QStyle::CE_ItemViewItem` | style 绘制 item view 条目的控制元素。 |

## 4. 关键用法

```cpp
void MyDelegate::paint(QPainter *p, const QStyleOptionViewItem &option,
                       const QModelIndex &index) const
{
    QStyleOptionViewItem opt(option);
    initStyleOption(&opt, index);

    opt.text = elidedBusinessText(index);
    option.widget->style()->drawControl(QStyle::CE_ItemViewItem, &opt, p, option.widget);
}
```

自定义绘制前保留选中背景：

```cpp
QStyleOptionViewItem opt(option);
initStyleOption(&opt, index);
opt.text.clear();
style->drawControl(QStyle::CE_ItemViewItem, &opt, painter, option.widget);
```

## 5. 使用场景

适合列表、表格、树的 delegate 绘制，自定义单元格、进度条单元、带状态徽标条目、复杂搜索结果项。

如果只是改数据显示，用模型 roles 即可；只有视觉结构变了才需要自定义 delegate。

## 6. 常见坑与经验

在 delegate 中先调用 `initStyleOption()`。它会从模型 role 填充文本、图标、字体、颜色、勾选状态。

不要无视 `option.state`。选中、hover、focus、disabled 都在里面，漏掉会让视图体验不一致。

绘制时尽量使用 `option.widget->style()`，这样局部 style 和代理 style 才能生效。
