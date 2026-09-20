# Qt Print Support：打印机、预览、分页与 PDF

> Qt Print Support 以 `QPrinter` 作为分页绘图设备，配合 `QPrintDialog`、`QPrintPreviewDialog` 和 `QPageSetupDialog` 完成打印工作流。Qt 6 将页面尺寸、方向和边距统一到 `QPageLayout` 等 Qt Gui 类型中。

## 1. 模块与最小打印

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui Widgets PrintSupport)
target_link_libraries(mytarget PRIVATE Qt6::Gui Qt6::Widgets Qt6::PrintSupport)
```

```cpp
#include <QPainter>
#include <QPrintDialog>
#include <QPrinter>

QPrinter printer(QPrinter::HighResolution);
QPrintDialog dialog(&printer, parentWidget);
if (dialog.exec() == QDialog::Accepted) {
    QPainter painter(&printer);
    painter.drawText(100, 100, QStringLiteral("打印内容"));
}
```

对话框接受后，`QPrinter` 已包含用户选择的打印机、页面范围、份数和方向。只有在接受后才创建 `QPainter` 并绘制，取消时不要输出半成品。

## 2. QPrinter 的输出模式

`QPrinter::OutputFormat` 主要包括 `NativeFormat` 和 `PdfFormat`：

```cpp
QPrinter printer(QPrinter::HighResolution);
printer.setOutputFormat(QPrinter::PdfFormat);
printer.setOutputFileName(QStringLiteral("report.pdf"));
```

PDF 输出不需要真实打印机，但仍然是分页 paint device。应检查 `QPainter::begin()` 返回值，结束时调用 `end()` 或让 painter 析构。

## 3. 页面布局与尺寸

```cpp
QPageLayout layout(QPageSize(QPageSize::A4),
                   QPageLayout::Portrait,
                   QMarginsF(15, 15, 15, 15),
                   QPageLayout::Millimeter);
printer.setPageLayout(layout);
```

Qt 6 推荐使用 `setPageLayout()`、`setPageSize()`、`setPageOrientation()` 和 `setPageMargins()`，不要依赖旧版纸张 API。绘制区域可通过 `printer.pageRect(QPrinter::DevicePixel)` 或 `pageLayout().paintRectPixels(resolution)` 获取。

## 4. 分页绘制

```cpp
QPainter painter(&printer);
const QRect page = printer.pageRect(QPrinter::DevicePixel);
const int lineHeight = painter.fontMetrics().height();
int y = page.top();

for (const QString &line : lines) {
    if (y + lineHeight > page.bottom()) {
        if (!printer.newPage())
            break;
        y = printer.pageRect(QPrinter::DevicePixel).top();
    }
    painter.drawText(page.left(), y, line);
    y += lineHeight;
}
```

`newPage()` 成功后才继续绘制。分页算法应使用字体度量和实际绘制高度，不能用固定字符数估算。表格、图片和段落通常需要先计算布局，再决定是否换页。

## 5. QPrintPreviewDialog

```cpp
#include <QPrintPreviewDialog>

QPrinter printer(QPrinter::HighResolution);
QPrintPreviewDialog preview(&printer, parentWidget);
QObject::connect(&preview, &QPrintPreviewDialog::paintRequested,
                 [&](QPrinter *p) {
    QPainter painter(p);
    drawReport(painter, p->pageRect(QPrinter::DevicePixel));
});
preview.exec();
```

预览对话框会在需要刷新时发出 `paintRequested`。绘制函数应幂等：每次从第一页开始，根据当前页面布局重新生成内容，不能依赖上一次绘制留下的光标位置。

## 6. 页面设置和打印选项

```cpp
QPageSetupDialog setup(&printer, parentWidget);
if (setup.exec() == QDialog::Accepted) {
    const QPageLayout current = printer.pageLayout();
    Q_UNUSED(current);
}
```

页面设置可能使用平台原生对话框，部分自定义纸张和边距在 Windows/macOS 原生界面中显示能力有限。重要布局应在应用内预览中再次确认。

## 7. 打印机枚举：QPrinterInfo

```cpp
const QList<QPrinterInfo> printers = QPrinterInfo::availablePrinters();
for (const QPrinterInfo &info : printers) {
    qDebug() << info.printerName()
             << info.location()
             << info.supportsColor();
}

const QPrinterInfo defaultPrinter = QPrinterInfo::defaultPrinter();
```

设备列表可能为空（无打印服务或权限不足）。持久化打印机选择时保存名称或系统标识，并在设备消失时回退到默认打印机。

## 8. 颜色、双面和份数

```cpp
printer.setColorMode(QPrinter::Color);
printer.setDuplex(QPrinter::DuplexAuto);
printer.setCopyCount(2);
printer.setCollateCopies(true);
```

这些设置是否生效取决于打印机能力。UI 应从 `QPrinterInfo` 查询支持情况，不能把控件状态直接当作硬件已接受。

## 9. 打印富文本和文档

`QTextDocument` 可以直接绘制到 QPrinter：

```cpp
QTextDocument document;
document.setHtml(html);
document.setPageSize(QSizeF(printer.pageRect(QPrinter::Point).size()));
document.print(&printer);
```

文档页面尺寸应与打印机页面逻辑单位匹配。复杂 HTML/CSS 并不等同浏览器渲染，打印前用预览检查分页、字体和图片。

## 10. QPainter 坐标和 DPI

QPrinter 的逻辑坐标、设备像素和点/毫米单位可能不同。固定尺寸绘制优先使用 `QPageLayout` 和 `QPainter::setViewport`/`setWindow` 做转换，不要假设一英寸永远是 96 像素。

```cpp
const qreal scale = printer.logicalDpiX() / 96.0;
painter.scale(scale, scale);
```

如果使用缩放，所有边距、字体和图片尺寸都要在同一坐标体系中计算。

## 11. 错误处理和取消

打印可能在 `newPage()`、`QPainter::begin()` 或系统提交阶段失败。绘制函数应返回成功状态并记录页码；用户取消预览或打印时及时停止生成大文档，避免阻塞 UI。

```cpp
if (!painter.begin(&printer)) {
    emit printFailed(tr("无法打开打印设备"));
    return;
}
const bool ok = drawAllPages(painter, printer);
painter.end();
if (!ok)
    emit printFailed(tr("分页或输出失败"));
```

## 12. 常见问题

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| PDF 页面被裁切 | 使用窗口尺寸而非 printer pageRect | 根据打印区域布局 |
| 预览和实际打印不同 | paintRequested 中使用了外部状态 | 绘制函数幂等并读取当前 QPrinter |
| 中文乱码 | 字体不可用或未嵌入 | 指定可用字体并验证 PDF |
| 分页重叠 | 未使用实际字体高度 | 用 QFontMetrics 计算行高 |
| 自定义纸张不显示 | 原生页面对话框限制 | 在应用内设置 QPageLayout 并预览 |
| 打印机列表为空 | 系统打印服务不可用 | 检查平台服务和权限 |

## 13. 自测题

1. QPrintDialog 接受后 QPrinter 发生了什么？
2. Qt 6 页面方向和边距应通过什么 API 设置？
3. 为什么预览的 paintRequested 处理器应幂等？
4. `newPage()` 返回 false 时应该怎样处理？
5. QPrinter 的逻辑坐标为什么不能简单当作屏幕像素？

### 参考答案

1. 用户的打印机和页面配置写入 QPrinter，可据此开始绘制。
2. `setPageLayout`、`setPageSize`、`setPageOrientation` 和 `setPageMargins`。
3. 预览会多次请求重绘，必须每次从确定状态重新生成页面。
4. 停止继续绘制，报告输出失败并清理 painter。
5. 打印设备 DPI、逻辑单位和屏幕 DPI 不同。

## 14. 小结

Qt 打印开发的主线是“配置 QPrinter → 用 QPainter 分页绘制 → 通过对话框或 PDF 输出”。以页面布局和实际绘制区域为基准，使用幂等的文档绘制函数，并对设备能力、字体、权限和取消路径做验证，才能得到稳定的打印与 PDF 结果。
