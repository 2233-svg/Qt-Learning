# QPrinter 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPrinter>`  
> 所属模块：`Qt6::PrintSupport`  
> 继承：`QPagedPaintDevice`

## 它解决什么问题

`QPrinter` 是 Qt 的分页绘制设备。它把绘图 API 接到系统打印机或 PDF 文件：应用把 `QPainter` 指向 `QPrinter`，画出来的内容会成为打印页面或输出文件。

一份正常的打印作业分成两个阶段：

1. **配置期**：选择打印机、输出格式、文件名、页面布局、dpi、范围、份数等；
2. **绘制期**：`QPainter painter(&printer)` 成功开始后绘制第一页，后续每一页前调用 `printer.newPage()`，最后结束 painter。

```cpp
QPrinter printer(QPrinter::HighResolution);
printer.setOutputFormat(QPrinter::PdfFormat);
printer.setOutputFileName("report.pdf");
printer.setDocName("Report");

QPainter painter(&printer);
drawPageOne(&painter);

if (hasPageTwo()) {
    printer.newPage();
    drawPageTwo(&painter);
}
```

绝大多数配置必须在 `QPainter::begin()` 前完成。打印已经开始后再改纸张、分辨率、份数或输出设备，可能无效或导致未定义行为。

## 页面、纸张和可打印区域

- `paperRect(unit)`：整张物理纸张区域；
- `pageRect(unit)`：可绘制页面区域，通常因边距而小于纸张；
- `fullPage()` 为 `false` 时，坐标原点位于可打印区域左上角；
- `setFullPage(true)` 后，原点位于纸张左上角，但打印机物理边距仍可能让边缘无法输出。

这意味着启用 full page 后，应用必须自己处理不可打印边距。不要误以为 `setFullPage(true)` 就能保证绘制到纸张最边缘。

## 直接打印、PDF 与输出文件

`OutputFormat` 决定输出目标：

- `NativeFormat`：使用系统打印后端和选中的打印机；
- `PdfFormat`：使用 Qt 的 PDF 输出后端。

`setOutputFileName()` 用于将输出定向到文件。设置非空的 `.pdf` 文件名会生成 PDF；空文件名会关闭“打印到文件”。输出格式、文件名和打印机名称互相影响，配置后应通过 `outputFormat()`、`outputFileName()`、`printerName()` 核对最终状态。

## 页码范围、份数和设备能力

`setFromTo()` 与 `setPrintRange()` 是给打印对话框和应用分页逻辑的范围信息。它们不会自动跳过页面，应用要根据 `fromPage()`、`toPage()` 或 `pageRanges()` 决定绘制哪些页。

`copyCount()` 表示请求份数，`supportsMultipleCopies()` 表示设备能否在单个作业中复制多份。若不支持，应用可能需要自行重复整个文档绘制流程。逐份打印由 `collateCopies()` 控制。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `ColorMode` | 指定彩色或灰度打印。 | 设备驱动可能限制最终输出能力。 |
| 类型 | `DuplexMode` | 指定单面或双面打印方式。 | 先用 `QPrinterInfo` 查询设备支持的双面模式。 |
| 类型 | `OutputFormat` | 指定系统原生输出或 PDF 输出。 | 输出格式应在开始绘制前设置。 |
| 类型 | `PageOrder` | 表示正序或逆序打印。 | 某些平台需要应用自行按该顺序输出页面。 |
| 类型 | `PaperSource` | 指定手动进纸、纸盒等来源。 | 平台支持有限，Qt 文档特别说明主要是 Windows。 |
| 类型 | `PrintRange` | 表示全部、选区或指定页码范围。 | 应用仍需按此范围决定实际绘制哪些页。 |
| 类型 | `PrinterMode` | 预设打印机的分辨率与工作模式。 | `HighResolution` 适合高质量输出，文本点大小不随 dpi 等比例变化。 |
| 类型 | `PrinterState` | 表示空闲、活动、错误、中止等设备状态。 | 驱动或远程设备报告可能不精确。 |
| 类型 | `Unit` | 指定 `pageRect()`、`paperRect()` 的测量单位。 | `Point` 为每英寸 72 点，`DevicePixel` 依赖 dpi。 |
| 构造 | `QPrinter(PrinterMode mode = ScreenResolution)` | 创建一个使用指定预设模式的打印机对象。 | 配置后再创建 `QPainter`；默认设备可能无效。 |
| 构造 | `QPrinter(const QPrinterInfo &printer, PrinterMode mode = ScreenResolution)` | 基于指定系统打印机信息创建打印机对象。 | 先确认 `QPrinterInfo` 非空，设备也可能随后离线。 |
| 析构 | `~QPrinter()` | 销毁打印机并释放资源。 | 作业进行中销毁对系统队列的影响依后端而定。 |
| 中止作业 | `abort()` | 尝试取消当前打印作业，成功返回 `true`。 | 数据已提交到系统队列时可能无法取消。 |
| 逐份打印 | `collateCopies() const` | 查询多份打印是否按完整文档逐份输出。 | 设备不支持多份时应用可能要自行处理。 |
| 颜色模式 | `colorMode() const` | 返回当前彩色或灰度设置。 | 结果是请求值，实际设备可用性另行确认。 |
| 份数 | `copyCount() const` | 返回请求打印份数。 | 是否由设备完成取决于 `supportsMultipleCopies()`。 |
| 创建者 | `creator() const` | 返回创建文档的应用名称。 | 主要是元数据，平台支持有差异。 |
| 文档名 | `docName() const` | 返回打印作业或文档名称。 | 不等同输出文件路径。 |
| 双面模式 | `duplex() const` | 返回当前单双面设置。 | 设备不支持时可能被忽略或降级。 |
| 字体嵌入 | `fontEmbeddingEnabled() const` | 查询是否启用字体嵌入。 | 只对支持的输出后端有意义。 |
| 起始页 | `fromPage() const` | 返回页码范围起始页。 | 与 `toPage()` 都为 0 通常表示未设置范围或全篇。 |
| 整页坐标 | `fullPage() const` | 查询原点是否位于完整纸张左上角。 | 即使为真，物理边距仍可能不可打印。 |
| 有效性 | `isValid() const` | 判断选中系统打印机或 PDF 后端是否有效。 | 设置纸张、分辨率等前先检查；绘制失败还要检查 `QPainter::begin()`。 |
| 新建页面 | `newPage()` | 完成当前页并开始新页，成功返回 `true`。 | 仅在活动绘制作业中调用；首张页前不需要调用。 |
| 输出文件 | `outputFileName() const` | 返回当前输出文件路径。 | 空字符串表示不打印到文件。 |
| 输出格式 | `outputFormat() const` | 返回当前输出格式。 | `setOutputFileName()` 和 `setPrinterName()` 可能改变它。 |
| 页面顺序 | `pageOrder() const` | 返回正序或逆序输出设置。 | 应用需按需要调整文档页遍历顺序。 |
| 可绘制区域 | `pageRect(Unit unit) const` | 返回页面可绘制区域矩形。 | 通常小于 `paperRect()`，要考虑页边距。 |
| 绘图引擎 | `paintEngine() const` | 返回底层 `QPaintEngine`。 | 仅用于底层扩展或诊断，普通绘制用 `QPainter`。 |
| 物理纸张区域 | `paperRect(Unit unit) const` | 返回完整纸张区域矩形。 | 不代表每个坐标都可实际打印。 |
| 纸张来源 | `paperSource() const` | 返回当前纸张来源。 | 支持受平台和驱动限制。 |
| PDF 版本 | `pdfVersion() const` | 返回 PDF 输出版本设置。 | 仅在 PDF 输出路径中有意义。 |
| 打印引擎 | `printEngine() const` | 返回底层 `QPrintEngine`。 | 应用代码优先使用 `QPrinter`，不直接改引擎属性。 |
| 打印程序 | `printProgram() const` | 返回提交打印任务的外部程序名。 | 主要用于 X11 特定后端。 |
| 打印范围 | `printRange() const` | 返回全部、选区或页码范围选择。 | 只记录意图，分页绘制仍由应用实现。 |
| 打印机名称 | `printerName() const` | 返回当前目标打印机系统名称。 | 名称无效时配置可能不会改变。 |
| 选择选项 | `printerSelectionOption() const` | 返回平台特定的打印机选择选项。 | Windows 和 macOS 上通常没有效果。 |
| 打印机状态 | `printerState() const` | 返回当前打印机状态。 | 状态可能不完全可靠，尤其是网络设备。 |
| 分辨率 | `resolution() const` | 返回当前请求或驱动协商的 dpi。 | dpi 影响绘制坐标系，应在开始绘制前确定。 |
| 设置逐份 | `setCollateCopies(bool collate)` | 设置多份打印默认是否逐份。 | 对话框可让用户改写；设备能力可能限制。 |
| 设置颜色 | `setColorMode(ColorMode newColorMode)` | 设置彩色或灰度模式。 | 在 `QPainter::begin()` 前调用。 |
| 设置份数 | `setCopyCount(int count)` | 设置请求打印的份数。 | 非正值无意义；后端不支持时应用自己重复输出。 |
| 设置创建者 | `setCreator(const QString &creator)` | 设置创建文档的应用名称。 | 主要是 X11 元数据，跨平台不要依赖。 |
| 设置文档名 | `setDocName(const QString &name)` | 设置打印作业显示的文档名。 | 不会设置输出文件名。 |
| 设置双面 | `setDuplex(DuplexMode duplex)` | 设置单双面打印方式。 | 先检查打印机支持，且在开始绘制前设置。 |
| 设置引擎 | `setEngines(QPrintEngine *printEngine, QPaintEngine *paintEngine)` | 为 `QPrinter` 子类指定自定义打印和绘图引擎。 | 受保护接口；`QPrinter` 不接管引擎所有权，替换会重置打印机状态。 |
| 设置字体嵌入 | `setFontEmbeddingEnabled(bool enable)` | 开启或关闭字体嵌入。 | 依赖输出后端和格式支持。 |
| 设置页码范围 | `setFromTo(int from, int to)` | 设置打印范围起始页和结束页。 | 只设默认或作业范围，应用必须自行跳过不在范围的页。 |
| 设置整页坐标 | `setFullPage(bool fp)` | 控制坐标原点在纸张边缘还是可打印区。 | 开启后应用须自己处理物理边距。 |
| 设置输出文件 | `setOutputFileName(const QString &fileName)` | 设置打印到文件的目标路径。 | 空路径关闭文件输出；`.pdf` 后缀会选择 PDF 输出。 |
| 设置输出格式 | `setOutputFormat(OutputFormat format)` | 设置原生打印或 PDF 输出格式。 | 切换到 NativeFormat 需有有效系统打印机。 |
| 设置页序 | `setPageOrder(PageOrder pageOrder)` | 设置正序或逆序打印。 | 某些后端只保存设置，应用要据此调整输出页顺序。 |
| 设置纸张来源 | `setPaperSource(PaperSource source)` | 设置纸盒或手动进纸来源。 | 平台支持有限；Windows 可在打印中影响下一页。 |
| 设置 PDF 版本 | `setPdfVersion(QPagedPaintDevice::PdfVersion version)` | 设置 PDF 输出版本。 | 仅 PDF 输出时有效，开始绘制前设置。 |
| 设置打印程序 | `setPrintProgram(const QString &printProg)` | 设置提交 PDF 输出的外部打印程序。 | 仅 X11 有效果，其它平台通常忽略。 |
| 设置打印范围 | `setPrintRange(PrintRange range)` | 设置全部、选区或页码范围选择。 | 不自动筛选页面，应用根据该值绘制。 |
| 设置打印机名 | `setPrinterName(const QString &name)` | 选择指定系统打印机。 | 无效名称不会改变配置；空名会转为 PDF 格式。 |
| 设置选择选项 | `setPrinterSelectionOption(const QString &option)` | 设置平台特定的打印机选择参数。 | Windows 和 macOS 无效果；活动作业中修改可能不可靠。 |
| 设置分辨率 | `setResolution(int dpi)` | 请求打印机使用指定 dpi。 | 必须在 `QPainter::begin()` 前调用。 |
| 支持纸张来源 | `supportedPaperSources() const` | 返回支持的纸张来源列表。 | Qt 文档指出此 API 仅 Windows 可用。 |
| 支持分辨率 | `supportedResolutions() const` | 返回设备声明支持的 dpi 列表。 | PDF 或 X11 后端的结果可能固定，不能假定硬件原生能力。 |
| 多份能力 | `supportsMultipleCopies() const` | 判断能否在单一作业中输出多份。 | 为 false 时应用需重复整个文档输出。 |
| 结束页 | `toPage() const` | 返回页码范围结束页。 | 与 `fromPage()` 都为 0 表示没有显式范围。 |

## 易错点

1. 所有会影响页面或设备的设置尽量放在 `QPainter::begin()` 之前。
2. 第一页不调用 `newPage()`；每张后续页开始前调用一次，最后多调一次会多出空白页。
3. `setFromTo()`、`setPrintRange()` 不会自动筛页，应用必须在绘制文档时落实。
4. `fullPage` 改的是坐标原点，不会消除打印机物理边距。
5. `isValid()` 只是前置检查，真正开始打印还应检查 `QPainter::begin()` 和 `newPage()` 返回值。

### 一句话总结

`QPrinter` 是 Qt 的分页输出设备：先在绘制前配置目标和页面，再用 `QPainter` 绘制并以 `newPage()` 推进文档页面。
