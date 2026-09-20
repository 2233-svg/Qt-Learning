# QPagedPaintDevice

> Qt 6.11.1 · Qt GUI · 来自 `QPagedPaintDevice`

## 1. 先建立直觉

`QPagedPaintDevice` 是“按页绘制”的 `QPaintDevice` 抽象基类。`QPdfWriter` 和 `QPrinter` 都建立在它之上：你用 `QPainter` 画当前页，调用 `newPage()` 后开始下一页。

它解决的是分页输出的共同问题：页面大小、方向、页边距、页面范围和 PDF 版本。和屏幕绘制不同，分页设备的几何指标会随页面设置变化，设置时机不对会导致内容落在错误位置。

## 2. 类说明

- 头文件：`#include <QPagedPaintDevice>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QPaintDevice`
- 派生：`QPdfWriter`、`QPrinter`
- 典型使用：报表、导出 PDF、打印文档、批量标签输出。

页面布局通常应在 `QPainter::begin()` 前设置；若要在文档中途改变下一页布局，应先设置布局，再立即 `newPage()`，中间不要绘制。

## 3. API 速查

| API | 用途 |
|---|---|
| `newPage()` | 结束当前页并开始新页；纯虚，由具体设备实现。 |
| `pageLayout()` | 返回当前 `QPageLayout`，用于查询纸张、方向、边距、可绘区域。 |
| `setPageLayout(layout)` | 一次性设置页面大小、方向、边距等。 |
| `setPageSize(size)` | 设置纸张大小。 |
| `setPageOrientation(orientation)` | 设置横向或纵向。 |
| `setPageMargins(margins, units)` | 设置页边距。 |
| `pageRanges()` / `setPageRanges()` | Qt 6 起设置或查询页码范围。 |
| `PdfVersion_1_4` | 生成 PDF 1.4。 |
| `PdfVersion_A1b` | 生成 PDF/A-1b，偏长期归档。 |
| `PdfVersion_1_6` | 生成 PDF 1.6。 |
| `PdfVersion_X4` | Qt 6.8 起，生成 PDF/X-4。 |

## 4. 关键用法

```cpp
QPdfWriter writer("report.pdf");
writer.setPageSize(QPageSize(QPageSize::A4));
writer.setPageMargins(QMarginsF(15, 15, 15, 15),
                      QPageLayout::Millimeter);

QPainter painter(&writer);
drawFirstPage(&painter, writer.pageLayout());

writer.newPage();
drawSecondPage(&painter, writer.pageLayout());
```

`newPage()` 不是保存文件，也不是刷新屏幕，而是分页设备进入下一页。调用失败时应停止后续绘制或提示输出失败。

## 5. 页面设置时机

| 时机 | 结果 |
|---|---|
| `QPainter::begin()` 前设置页面 | 最稳妥，第一页按设置绘制。 |
| 已开始绘制当前页后改页面布局 | 当前页的度量可能已经使用旧值，不推荐。 |
| 设置布局后马上 `newPage()` | 新设置应用到下一页。 |
| `setPageLayout()` 和 `newPage()` 之间继续绘制 | 容易用错页面指标，应避免。 |

`pageLayout()` 返回的是布局值对象；不能修改返回对象后期待设备跟着改变。要通过 `setPageLayout()` 或单项 setter 写回设备。

## 6. 常见坑与经验

- `paintRect()` 是考虑边距后的可绘区域，`fullRect()` 是整张纸。排版正文通常用 `paintRect()`。
- PDF 版本影响兼容性、归档和印刷工作流；不是越新越好。
- `setPageRanges()` 表示设备相关的页码范围，具体解释还取决于打印/输出流程。
- 打印机有物理不可打印边距，设置过小可能被拒绝或被设备夹紧。
- 分页输出没有屏幕的自动布局魔法，应用要自己决定何时换页、重复页眉页脚和重置坐标。

## 7. 知识点覆盖

- 分页 `QPaintDevice` 与 `QPainter` 的协作
- 页面大小、方向、边距和可绘区域
- `newPage()` 的调用时机和错误处理
- PDF 版本、归档/印刷兼容性
- `QPdfWriter`、`QPrinter` 与页面布局值对象
