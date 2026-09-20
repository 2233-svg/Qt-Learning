# Qt QTileRules 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTileRules>`  
> 所属模块：`Qt6::Widgets`  
> 继承：无  
> 定位：九宫格绘制规则

## 1. 先建立整体认识：它解决什么问题

`QTileRules` 不是绘图器，也不是控件，它只是一个很小的规则包：告诉 `qDrawBorderPixmap()` 在横向和纵向上该怎么铺图。  
它解决的是“边框图要拉伸、平铺，还是按整数格子缩放平铺”这类问题。

它最常见的场景是做九宫格式边框：

- 四个角保持原样；
- 上下边和左右边按规则铺开；
- 中间区域按目标尺寸填满。

如果你在做皮肤、面板、按钮底图、装饰框，这个结构就很有用。

## 2. 它和谁一起用

`QTileRules` 基本总是和 `qDrawBorderPixmap()` 一起出现。

```cpp
QPainter painter(this);
QTileRules rules(Qt::RepeatTile, Qt::StretchTile);
qDrawBorderPixmap(&painter, targetRect, targetMargins,
                  pixmap, sourceRect, sourceMargins, rules);
```

`Qt::TileRule` 决定规则本身：

- `StretchTile`：把图块拉伸到目标空间；
- `RepeatTile`：重复铺满，末尾可能被裁掉；
- `RoundTile`：按整数块数铺满，再把单块尺寸略微调整到刚好填满。

## 3. 什么时候该选它

- 你要画一张“可缩放的边框图”，但四角不能变形；
- 你想让边缘纹理保持原始密度，不想被硬拉伸；
- 你做的是 UI 皮肤，而不是普通图片缩放。

如果只是普通图片缩放，直接用 `QPainter::drawPixmap()` 就够了；`QTileRules` 是给“带边框语义的图片”准备的。

## 4. 核心理解

`QTileRules` 只保存两条规则：

- `horizontal`：横向铺法；
- `vertical`：纵向铺法。

一个参数版本会把两边设成同一种规则；两个参数版本则可以分别控制。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造函数 | `QTileRules::QTileRules(Qt::TileRule rule = Qt::StretchTile)` | 用同一种 tile 规则同时设置横向和纵向。 | 适合大多数“整张图都按同一规则铺”的场景。 |
| 构造函数 | `QTileRules::QTileRules(Qt::TileRule horizontalRule, Qt::TileRule verticalRule)` | 分别设置横向和纵向 tile 规则。 | 适合边缘条带在两个方向上需要不同处理的情况。 |
| 数据成员 | `Qt::TileRule QTileRules::horizontal` | 保存横向铺法。 | 通常影响上边和下边的平铺方式。 |
| 数据成员 | `Qt::TileRule QTileRules::vertical` | 保存纵向铺法。 | 通常影响左边和右边的平铺方式。 |

## 6. 一句话总结

`QTileRules` 就是一组给九宫格边框图用的铺法规则，专门回答“横向和纵向怎么铺才不变形”。
