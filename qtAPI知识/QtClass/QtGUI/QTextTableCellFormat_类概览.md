# QTextTableCellFormat 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTextTableCellFormat>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QTextCharFormat`

## 1. 它解决什么问题

`QTextTableCellFormat` 描述单元格的外观与盒模型：四边独立的 padding、边框宽度、边框样式和边框画刷，同时继承字符格式的背景、前景、字体等属性。

它解决“同一张表中某个单元格怎样和其他单元格有不同边距、底色或边框”的问题。整表的 cell spacing、通用 cell padding 和列宽属于 `QTextTableFormat`；单元格正文仍由 `QTextCursor` 编辑。

## 2. 四边属性与批量设置

每一边都有独立的 padding、border、border style 和 border brush。`setPadding()`、`setBorder()`、`setBorderStyle()`、`setBorderBrush()` 是批量便利函数，分别把同一个值写到上、下、左、右四边；之后调用 `setTopBorder()` 等单边函数可覆盖其中一边。

```cpp
QTextTableCellFormat format;
format.setPadding(4);
format.setBorder(1);
format.setBorderStyle(QTextFrameFormat::BorderStyle_Solid);
format.setTopBorderBrush(Qt::darkBlue);
format.setBackground(QColor("#eef6ff"));

cell.setFormat(format);
```

边框可见效果同时受宽度、样式与画刷影响。设置宽度但使用 `BorderStyle_None` 不会按实线绘制；当表格启用 `borderCollapse` 时，相邻格边框还要与邻格和表格布局策略合成。

## 3. 写回、生命周期和线程

本类是值类型。可以由 `cell.format().toTableCellFormat()` 得到，也可单独创建后交给 `cell.setFormat()`。读取到的是副本，任何修改都要显式写回当前 cell。

格式值本身不拥有表格或资源。把它写入 cell 时要在文档所属线程完成；表格结构变化后应重新取得单元格，再写入格式。

## API 速查表

| API | 用途与关键语义 | 边界、默认值或注意事项 |
| --- | --- | --- |
| `QTextTableCellFormat()` | 创建单元格格式值。 | 不会自动应用到任意 cell。 |
| `isValid()` | 判断是否为单元格格式类别。 | 不表示四边属性都已设置。 |
| `setPadding(qreal)` | 一次设置四边内边距。 | 后续单边 padding 会覆盖对应一侧。 |
| `setTopPadding()` / `topPadding()` | 设置或读取上内边距。 | 是内容到上边框的距离。 |
| `setBottomPadding()` / `bottomPadding()` | 设置或读取下内边距。 | 不等于表格的 cell spacing。 |
| `setLeftPadding()` / `leftPadding()` | 设置或读取左内边距。 | 文字方向不改变其物理边命名。 |
| `setRightPadding()` / `rightPadding()` | 设置或读取右内边距。 | 与 `QTextTableFormat::cellPadding` 属于不同优先级层次。 |
| `setBorder(qreal)` | 一次设置四边边框宽度。 | 单边 border 可随后覆盖。 |
| `setTopBorder()` / `topBorder()` | 设置或读取上边框宽度。 | 还需样式和画刷共同决定可见效果。 |
| `setBottomBorder()` / `bottomBorder()` | 设置或读取下边框宽度。 | 折叠边框表格中与邻格边框合成。 |
| `setLeftBorder()` / `leftBorder()` | 设置或读取左边框宽度。 | 是逻辑排版长度。 |
| `setRightBorder()` / `rightBorder()` | 设置或读取右边框宽度。 | 不是单元格间距。 |
| `setBorderStyle(BorderStyle)` | 一次设置四边边框样式。 | `BorderStyle_None` 会使边框不按普通线条显示。 |
| `setTopBorderStyle()` / `topBorderStyle()` | 设置或读取上边框样式。 | 使用 `QTextFrameFormat::BorderStyle`。 |
| `setBottomBorderStyle()` / `bottomBorderStyle()` | 设置或读取下边框样式。 | 可与其他三边不同。 |
| `setLeftBorderStyle()` / `leftBorderStyle()` | 设置或读取左边框样式。 | 复杂表格要验证折叠边框结果。 |
| `setRightBorderStyle()` / `rightBorderStyle()` | 设置或读取右边框样式。 | 与边框宽度和画刷共同生效。 |
| `setBorderBrush(const QBrush &)` | 一次设置四边边框画刷。 | 后续单边画刷可覆盖。 |
| `setTopBorderBrush()` / `topBorderBrush()` | 设置或读取上边框画刷。 | 画刷可为颜色、渐变或纹理。 |
| `setBottomBorderBrush()` / `bottomBorderBrush()` | 设置或读取下边框画刷。 | 不等于单元格背景。 |
| `setLeftBorderBrush()` / `leftBorderBrush()` | 设置或读取左边框画刷。 | 返回值是画刷副本。 |
| `setRightBorderBrush()` / `rightBorderBrush()` | 设置或读取右边框画刷。 | 修改返回值不回写格式。 |
| 继承的 `setBackground()` / `setForeground()` | 设置单元格背景或前景相关字符属性。 | 与边框画刷是不同属性。 |

## 4. 记忆重点

`QTextTableCellFormat` 是单元格四边样式和内边距的值对象。批量 setter 会写四边，单边 setter 可以覆盖；边框最终是否可见还取决于宽度、样式、画刷和表格的边框折叠策略。
