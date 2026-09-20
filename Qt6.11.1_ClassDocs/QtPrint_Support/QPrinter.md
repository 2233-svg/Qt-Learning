# QPrinter
> Qt 6.11.1 · Qt Print Support · 来自 `QPrinter`

## 1. 先建立直觉

`QPrinter` 是 Qt 打印体系里的分页绘图设备。你用 `QPainter` 在它上面画文字、图形、图片和页面内容；它负责把这些绘图命令送到系统打印机，或生成 PDF 文件。

它不是“打印对话框”，也不是“打印机列表”。用户选择打印机和页码通常由 `QPrintDialog` 完成；查询系统打印机能力用 `QPrinterInfo`；真正出页时，`QPrinter` 才是 `QPainter` 的目标设备。

## 2. 类说明

保留类说明：这些 API 来自 `QPrinter`，属于 Qt Print Support 模块，用于配置打印作业并作为 `QPagedPaintDevice` 接收分页绘制。

典型链路是：创建并配置 `QPrinter` -> 可选显示 `QPrintDialog` 或 `QPageSetupDialog` -> `QPainter painter(&printer)` -> 每页绘制 -> `newPage()` -> `painter.end()`。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QPrinter(mode)` | 创建打印设备；`ScreenResolution` 便于屏幕近似，`HighResolution` 更适合正式输出。 |
| `QPrinter(QPrinterInfo, mode)` | 基于指定系统打印机创建。 |
| `setOutputFormat(NativeFormat/PdfFormat)` / `outputFormat()` | 选择真实打印或生成 PDF。 |
| `setOutputFileName()` / `outputFileName()` | 指定 PDF 或打印到文件的目标路径。 |
| `setPrinterName()` / `printerName()` | 选择系统打印机。 |
| `isValid()` | 判断当前配置是否可用于绘制输出。 |
| `setDocName()`、`setCreator()` | 设置打印队列/PDF 元数据。 |
| `setResolution()` / `resolution()` | 设置 DPI；影响坐标、字体和图像输出。 |
| `setPageLayout()` 等继承自 `QPagedPaintDevice` 的页设置 | 设置纸张、方向、边距和页面范围的现代入口。 |
| `paperRect(unit)` / `pageRect(unit)` | 查询纸张区域和可绘制区域；后者通常扣除了不可打印边距。 |
| `setFullPage(bool)` / `fullPage()` | 控制坐标是否以整张纸为基准，而不是可打印区域。 |
| `setFromTo(from, to)`、`fromPage()`、`toPage()` | 设置/读取页码范围。 |
| `setPrintRange()` / `printRange()` | 指定全部、当前页、选区或页码范围。 |
| `setCopyCount()`、`setCollateCopies()` | 设置份数和逐份整理。 |
| `setColorMode()`、`setDuplex()`、`setPaperSource()` | 设置颜色、双面和纸盒等打印机选项。 |
| `supportedResolutions()`、`supportedPaperSources()`、`supportsMultipleCopies()` | 查询设备能力。 |
| `newPage()` | 结束当前页并开始下一页；失败时要停止作业或报错。 |
| `abort()` | 尝试中止当前打印作业。 |
| `printerState()` | 查询空闲、活动、中止或错误状态。 |
| `setPdfVersion()` / `pdfVersion()` | 生成 PDF 时选择 PDF 版本。 |
| `setFontEmbeddingEnabled()` / `fontEmbeddingEnabled()` | 控制 PDF/打印输出中的字体嵌入。 |
| `printEngine()` / `paintEngine()` | 访问底层打印/绘图引擎，通常只给框架或高级扩展用。 |

## 4. 典型流程

```cpp
QPrinter printer(QPrinter::HighResolution);
printer.setOutputFormat(QPrinter::PdfFormat);
printer.setOutputFileName("report.pdf");
printer.setDocName("Monthly report");

QPainter painter;
if (!painter.begin(&printer))
    return;

drawPage(&painter, 1);
if (!printer.newPage()) {
    painter.end();
    return;
}
drawPage(&painter, 2);
painter.end();
```

真实打印时，把 `QPrintDialog` 放在绘制前，让用户修改同一个 `QPrinter`：

```cpp
QPrintDialog dialog(&printer, parent);
if (dialog.exec() != QDialog::Accepted)
    return;
printDocument(&printer);
```

## 5. 使用场景

| 场景 | 配置重点 |
| --- | --- |
| 生成 PDF 报表 | `PdfFormat`、`setOutputFileName()`、PDF 版本、字体嵌入。 |
| 打印富文本或表格 | 页边距、分辨率、`newPage()`、页码范围。 |
| 打印图片/图纸 | 高 DPI、缩放策略、`pageRect()` 和单位换算。 |
| 企业批量打印 | 设备选择、双面、份数、纸盒、失败状态处理。 |

## 6. 常见坑与经验

`QPrinter` 的很多设置必须在 `QPainter::begin()` 之前完成。绘制已经开始后再改输出格式、文件名、分辨率、页布局，结果可能无效或平台相关。

`paperRect()` 是整张纸，`pageRect()` 是可绘制区域。默认坐标常以可绘制区域为参考；如果启用 `fullPage`，坐标改以整张纸为参考，但真实打印机的物理不可打印边距不会因此消失。

不要忽略 `newPage()` 返回值。PDF 写盘失败、打印队列错误、磁盘满，都可能在换页或结束时暴露。

打印和 PDF 不是屏幕截图。字体度量、DPI、分页算法和图片缩放都要单独测试，特别是中英文混排和高分辨率图片。

## 7. 知识点覆盖

- `QPrinter`、`QPainter`、`QPagedPaintDevice` 的关系。
- 打印机输出和 PDF 输出的分歧。
- 纸张、可绘制区域、页边距、DPI 和坐标单位。
- 页码范围、份数、双面、颜色、纸盒等打印作业属性。
- 多页绘制、失败检测和平台打印后端差异。
