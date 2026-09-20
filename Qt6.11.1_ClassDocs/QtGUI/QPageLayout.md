# QPageLayout

> Qt 6.11.1 · Qt GUI · 来自 `QPageLayout`

## 1. 先建立直觉

`QPageLayout` 是分页输出中的页面几何模型。它把纸张大小、横竖方向、边距、单位、可绘区域和整页区域组合成一个值对象，供 `QPdfWriter`、`QPrinter`、`QPagedPaintDevice` 等使用。

不要把它和 QWidget 布局混淆。它不摆放控件，而是回答“这张纸多大、正文能画在哪个矩形里、边距是否合法”。

## 2. 类说明

- 头文件：`#include <QPageLayout>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 对象模型：值类型，可复制、比较和交换。
- 协作类：`QPageSize` 描述纸张规格，`QMarginsF` 描述边距，分页设备应用布局。

默认构造得到无效布局。实际输出前应设置有效 `QPageSize`、方向和边距。

## 3. API 速查

| API | 用途 |
|---|---|
| `QPageLayout(pageSize, orientation, margins, unit, minMargins)` | 构造标准页面布局。 |
| `isValid()` | 检查布局是否可用。 |
| `pageSize()` / `setPageSize()` | 读取或设置纸张大小。 |
| `orientation()` / `setOrientation()` | 读取或设置横向/纵向。 |
| `units()` / `setUnits()` | 设置当前边距和矩形查询使用的单位。 |
| `margins()` / `setMargins()` | 读取或设置页边距。 |
| `minimumMargins()` / `setMinimumMargins()` | 管理设备要求的最小边距。 |
| `maximumMargins()` | 查询在当前页大小和最小边距下允许的最大边距。 |
| `fullRect()` | 整张纸的矩形，不扣除边距。 |
| `paintRect()` | 可绘矩形，通常扣除边距。 |
| `fullRectPixels(resolution)` / `paintRectPixels(resolution)` | 按 DPI 转换为设备像素。 |
| `fullRectPoints()` / `paintRectPoints()` | 以 1/72 英寸点为单位返回整数矩形。 |
| `setLeft/Right/Top/BottomMargin()` | 单独设置某一侧边距。 |
| `isEquivalentTo()` | 判断页面尺寸、方向、边距是否等价。 |
| `operator==` / `!=` | 严格比较，包括单位、页面 ID/名称等。 |

## 4. 模式、方向与单位

| 枚举 | 说明 |
|---|---|
| `StandardMode` | 常规模式，`paintRect()` 扣除边距，边距受最小/最大值约束。 |
| `FullPageMode` | 全页模式，`paintRect()` 等同整页，边距由调用方手动处理。 |
| `Portrait` | 使用页面定义的默认方向。 |
| `Landscape` | 将页面尺寸旋转 90 度。 |
| `Millimeter` / `Point` / `Inch` | 最常用单位；Point 为 1/72 英寸。 |
| `Pica` / `Didot` / `Cicero` | 排版单位，适合印刷排版场景。 |
| `OutOfBoundsPolicy::Reject` | Qt 6.8 起，边距越界时拒绝设置。 |
| `OutOfBoundsPolicy::Clamp` | Qt 6.8 起，越界边距夹紧到合法范围。 |

## 5. 关键用法

```cpp
QPageLayout layout(
    QPageSize(QPageSize::A4),
    QPageLayout::Portrait,
    QMarginsF(15, 15, 15, 15),
    QPageLayout::Millimeter);

const QRectF body = layout.paintRect(QPageLayout::Millimeter);
```

正文排版通常使用 `paintRect()`，页眉页脚可以根据 `fullRect()` 和 margins 自己定位。若在 `FullPageMode` 下，`paintRect()` 不再帮你扣边距。

```cpp
layout.setMargins(QMarginsF(2, 2, 2, 2),
                  QPageLayout::OutOfBoundsPolicy::Clamp);
```

在物理打印设备上，最小可打印边距可能大于你设置的值。`Clamp` 适合“尽量贴边但必须有效”；`Reject` 适合需要明确知道设置失败的排版工具。

## 6. 常见坑与经验

- `QPageSize` 自身通常以纵向定义；要得到考虑方向后的尺寸，用 `fullRect()` 而不是直接看 page size。
- `operator==` 是严格相等，单位、名称或页面 ID 差异都可能导致 false；只关心实际几何时用 `isEquivalentTo()`。
- `setUnits()` 会影响后续以当前单位读取/设置边距的语义，混合毫米和点时要非常明确。
- `setMinimumMargins()` 不应随意覆盖打印机提供的物理边距，否则可能生成设备无法打印的布局。
- 像素矩形需要传入分辨率，同一纸张在 72 DPI、300 DPI、600 DPI 下像素尺寸完全不同。

## 7. 知识点覆盖

- 纸张大小、方向、边距和可绘矩形
- Standard/FullPage 两种页面模式
- 毫米、点、英寸和像素转换
- 最小边距、最大边距和越界策略
- 严格相等与几何等价的区别
