# QPrinter

> Qt 6.11.1 · Qt Print Support

## 1. 先建立直觉

**一句话定位：** 这是 Qt Print Support 中围绕“Printer”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Print Support 提供打印机、打印预览和打印作业相关接口。

### 这是什么

`QPrinter` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QPrinter>`
- 继承自：QPagedPaintDevice
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS PrintSupport)
target_link_libraries(mytarget PRIVATE Qt6::PrintSupport)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum ColorMode { Color, GrayScale }`
- `enum DuplexMode { DuplexNone, DuplexAuto, DuplexLongSide, DuplexShortSide }`
- `enum OutputFormat { NativeFormat, PdfFormat }`
- `enum PageOrder { FirstPageFirst, LastPageFirst }`
- `enum PaperSource { Auto, Cassette, Envelope, EnvelopeManual, FormSource, …, LastPaperSource }`
- `enum PrintRange { AllPages, Selection, PageRange, CurrentPage }`
- `enum PrinterMode { ScreenResolution, PrinterResolution, HighResolution }`
- `enum PrinterState { Idle, Active, Aborted, Error }`
- `enum Unit { Millimeter, Point, Inch, Pica, Didot, …, DevicePixel }`

### 公有函数

- `QPrinter(QPrinter::PrinterMode mode = ScreenResolution)`
- `QPrinter(const QPrinterInfo &printer, QPrinter::PrinterMode mode = ScreenResolution)`
- `virtual ~QPrinter()`
- `bool abort()`
- `bool collateCopies() const`
- `QPrinter::ColorMode colorMode() const`
- `int copyCount() const`
- `QString creator() const`
- `QString docName() const`
- `QPrinter::DuplexMode duplex() const`
- `bool fontEmbeddingEnabled() const`
- `int fromPage() const`
- `bool fullPage() const`
- `bool isValid() const`
- `QString outputFileName() const`
- `QPrinter::OutputFormat outputFormat() const`
- `QPrinter::PageOrder pageOrder() const`
- `QRectF pageRect(QPrinter::Unit unit) const`
- `QRectF paperRect(QPrinter::Unit unit) const`
- `QPrinter::PaperSource paperSource() const`
- `QPagedPaintDevice::PdfVersion pdfVersion() const`
- `QPrintEngine * printEngine() const`
- `QString printProgram() const`
- `QPrinter::PrintRange printRange() const`
- `QString printerName() const`
- `QString printerSelectionOption() const`
- `QPrinter::PrinterState printerState() const`
- `int resolution() const`
- `void setCollateCopies(bool collate)`
- `void setColorMode(QPrinter::ColorMode newColorMode)`
- `void setCopyCount(int count)`
- `void setCreator(const QString &creator)`
- `void setDocName(const QString &name)`
- `void setDuplex(QPrinter::DuplexMode duplex)`
- `void setFontEmbeddingEnabled(bool enable)`
- `void setFromTo(int from, int to)`
- `void setFullPage(bool fp)`
- `void setOutputFileName(const QString &fileName)`
- `void setOutputFormat(QPrinter::OutputFormat format)`
- `void setPageOrder(QPrinter::PageOrder pageOrder)`
- `void setPaperSource(QPrinter::PaperSource source)`
- `void setPdfVersion(QPagedPaintDevice::PdfVersion version)`
- `void setPrintProgram(const QString &printProg)`
- `void setPrintRange(QPrinter::PrintRange range)`
- `void setPrinterName(const QString &name)`
- `void setPrinterSelectionOption(const QString &option)`
- `void setResolution(int dpi)`
- `QList<QPrinter::PaperSource> supportedPaperSources() const`
- `QList<int> supportedResolutions() const`
- `bool supportsMultipleCopies() const`
- `int toPage() const`

### 重实现的公有函数

- `virtual bool newPage() override`
- `virtual QPaintEngine * paintEngine() const override`

### 保护函数

- `void setEngines(QPrintEngine *printEngine, QPaintEngine *paintEngine)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QPrinter::ColorMode`

**作用与语义：**

这个枚举类型用于指示`QPrinter`是否应该以彩色印刷。
- `QPrinter::Color`：`1`;如果有彩色印刷，否则为灰度。
- `QPrinter::GrayScale`：`0`;即使是彩色打印机也能以灰度打印。

### `enum QPrinter::DuplexMode`

**作用与语义：**

枚举用于指示印刷是否会在每张纸的一面或两面进行（单工印刷或双面印刷）。
- `QPrinter::DuplexNone`：`0`;仅限单面（单人）印刷。
- `QPrinter::DuplexAuto`：`1`;打印机的默认设置用于判断是否使用双面打印。
- `QPrinter::DuplexLongSide`：`2`;每张纸的两面都用于印刷。纸张在印刷第二面之前，先翻过最长的边
- `QPrinter::DuplexShortSide`：`3`;每张纸的两面都用于印刷。纸张在印刷第二面之前，先翻转最短边

### `enum QPrinter::OutputFormat`

**作用与语义：**

OutputFormat 枚举用于描述`QPrinter`应使用的打印格式。
- `QPrinter::NativeFormat`：`0`;`QPrinter` 会根据其运行的平台定义的方法打印输出。该模式是直接向打印机打印时的默认模式。
- `QPrinter::PdfFormat`：`1`;`QPrinter` 将生成可搜索的 PDF 文件输出。该模式是打印文件时的默认模式。

### `enum QPrinter::PageOrder`

**作用与语义：**

`QPrinter` 用这个枚举类型来告诉应用程序如何打印。
- `QPrinter::FirstPageFirst`：`0`;应先打印编号最低的页面。
- `QPrinter::LastPageFirst`：`1`;应先打印编号最高的页面。

### `enum QPrinter::PaperSource`

**作用与语义：**

该枚举类型指定`QPrinter`应使用的纸源。`QPrinter`不检查纸张源是否可用;它仅利用这些信息尝试设置纸张源。是否会设置纸张源取决于打印机是否拥有该特定源。
警告：目前该功能仅在Windows上实现。
- `QPrinter::Auto`：`6`
- `QPrinter::Cassette`：`11`
- `QPrinter::Envelope`：`4`
- `QPrinter::EnvelopeManual`：`5`
- `QPrinter::FormSource`：`12`
- `QPrinter::LargeCapacity`：`10`
- `QPrinter::LargeFormat`：`9`
- `QPrinter::Lower`：`1`
- `QPrinter::MaxPageSource`：`13`;已弃用，请使用 LastPaperSource
- `QPrinter::Middle`：`2`
- `QPrinter::Manual`：`3`
- `QPrinter::OnlyOne`：`0`
- `QPrinter::Tractor`：`7`
- `QPrinter::SmallFormat`：`8`
- `QPrinter::Upper`：`OnlyOne`
- `QPrinter::CustomSource`：`14`;由打印机定义的 PaperSource，Qt 未知
- `QPrinter::LastPaperSource`：`CustomSource`;最高有效PaperSource值，目前为CustomSource

### `enum QPrinter::PrintRange`

**作用与语义：**

用于指定打印范围选择选项。
- `QPrinter::AllPages`：`0`;所有页面应印刷。
- `QPrinter::Selection`：`1`;仅应打印选出部分。
- `QPrinter::PageRange`：`2`;应打印指定的页数范围。
- `QPrinter::CurrentPage`：`3`;仅应打印当前页面。

### `enum QPrinter::PrinterMode`

**作用与语义：**

这个枚举描述了打印机应采用的工作模式。它基本上预设了某个分辨率和工作模式。
- `QPrinter::ScreenResolution`：`0`;将打印设备的分辨率设置为屏幕分辨率。这有一个很大的优点，就是在打印机上绘画时，结果几乎完全匹配屏幕上的可见输出。这是最易使用的，因为屏幕上和打印机上的字体指标相同。这是默认值。ScreenResolution的输出质量低于高分辨率，且应仅用于草稿。
- `QPrinter::PrinterResolution`：`1`;该值已被弃用。对于打印机，它相当于Unix上的ScreenResolution和Windows和macOS上的HighResolution。对于PDF打印，不支持，可能导致行为不明确。使用该值可能导致打印机代码不可移植。
- `QPrinter::HighResolution`：`2`;在Windows上，将打印机分辨率设置为所用打印机定义的分辨率。对于PDF打印，将PDF驱动程序的分辨率设置为1200 dpi。
注意：在`QPrinter`设备上渲染文本时，需要注意的是，文字大小（以点为单位）与设备本身指定的分辨率无关。因此，在将文本与图形结合时，指定字体大小（像素）可能有助于确保它们的相对大小符合您的预期。

### `enum QPrinter::Unit`

**作用与语义：**

该枚举类型用于指定页面和纸张尺寸的测量单位。
- `QPrinter::Millimeter`：`0`
- `QPrinter::Point`：`1`
- `QPrinter::Inch`：`2`
- `QPrinter::Pica`：`3`
- `QPrinter::Didot`：`4`
- `QPrinter::Cicero`：`5`
- `QPrinter::DevicePixel`：`6`
请注意 Point 和 DevicePixel 的区别。Point 单元定义为 1/72 英寸，而 DevicePixel 单元依赖分辨率，基于打印机上的实际像素或点。

### `[explicit] QPrinter::QPrinter(QPrinter::PrinterMode mode = ScreenResolution)`

**作用与语义：**

创建一个带有给定`mode`的新打印机对象。

### `[explicit] QPrinter::QPrinter(const QPrinterInfo &printer, QPrinter::PrinterMode mode = ScreenResolution)`

**作用与语义：**

创建一个带有给定 `printer` 和 `mode` 的新打印机对象。

### `[virtual noexcept] QPrinter::~QPrinter()`

**作用与语义：**

销毁打印机对象并释放所有分配的资源。如果打印机在打印作业进行中被销毁，这可能会也可能不会影响打印任务。

### `bool QPrinter::abort()`

**作用与语义：**

中止当前打印批量。如果打印成功中止，返回`true`，`printerState()`返回`QPrinter::Aborted`;否则返回`false`。
打印作业并不总是可以中止。例如，所有数据都已送达打印机，但打印机在被要求取消时无法或不愿取消。

### `bool QPrinter::collateCopies() const`

**作用与语义：**

如果在选择多份时启用了排序，则返回 `true`。如果在选择多份时未启用排序，则返回 `false`。当排序关闭时，每个单独页面的打印将在开始下一页之前重复 numCopies() 次。启用排序时，所有页面打印完毕后才开始打印下一份这些页面。

### `QPrinter::ColorMode QPrinter::colorMode() const`

**作用与语义：**

返回当前的色彩模式。

### `int QPrinter::copyCount() const`

**作用与语义：**

返回将要打印的副本数量。默认值为1。

### `QString QPrinter::creator() const`

**作用与语义：**

返回创建文档的应用程序名称。

### `QString QPrinter::docName() const`

**作用与语义：**

返回文档名称。

### `QPrinter::DuplexMode QPrinter::duplex() const`

**作用与语义：**

返回当前的双工模式。

### `bool QPrinter::fontEmbeddingEnabled() const`

**作用与语义：**

如果启用了字体嵌入，返回`true`。

### `int QPrinter::fromPage() const`

**作用与语义：**

返回待打印页数中的第一页编号（“出页”设置）。文档中的页面编号遵循惯例，第一页为第1页。
默认情况下，该函数返回一个特殊的值 0，意味着“从页面开始”设置是未设置的。
注意：如果 fromPage() 和 `toPage()` 都返回 0，表示整个文档将被打印。

### `bool QPrinter::fullPage() const`

**作用与语义：**

如果打印机坐标系的原点位于页面角落，返回`true`;如果原点位于可打印区域的边缘，则返回为假。
详情和注意事项请参见`setFullPage()`。

### `bool QPrinter::isValid() const`

**作用与语义：**

如果当前选择的打印机是系统中的有效打印机，或纯 PDF 打印机，返回 `true`;否则返回 `false`。
要检测其他故障，可以检查`QPainter::begin()`或`QPrinter::newPage()`的输出。

**官方示例：**

```cpp
     QPrinter printer;
     printer.setOutputFormat(QPrinter::PdfFormat);
     printer.setOutputFileName("/foobar/nonwritable.pdf");
     QPainter painter;
     if (! painter.begin(&printer)) { // failed to open file
         qWarning("failed to open file, is it writable?");
         return 1;
     }
     painter.drawText(10, 10, "Test");
     if (! printer.newPage()) {
         qWarning("failed in flushing page to disk, disk full?");
         return 1;
     }
     painter.drawText(10, 10, "Test 2");
     painter.end();
```

### `[override virtual] bool QPrinter::newPage()`

**作用与语义：**

重装：`QPagedPaintDevice::newPage()`。
告诉打印机弹出当前页面并继续在新页面打印。如果成功，返回`true`;否则返回`false`。
调用非活跃`QPrinter`对象的newPage()总是失败。

### `QString QPrinter::outputFileName() const`

**作用与语义：**

返回输出文件的名称。默认情况下，这是空字符串（表示打印机不应打印到文件）。

### `QPrinter::OutputFormat QPrinter::outputFormat() const`

**作用与语义：**

返回该打印机的输出格式。

### `QPrinter::PageOrder QPrinter::pageOrder() const`

**作用与语义：**

返回当前的页面顺序。
默认的页面顺序是`FirstPageFirst`。

### `QRectF QPrinter::pageRect(QPrinter::Unit unit) const`

**作用与语义：**

返回页面的矩形`unit`;这通常比`paperRect()`小，因为页面边界和纸张之间通常有边距。

### `[override virtual] QPaintEngine *QPrinter::paintEngine() const`

**作用与语义：**

重装：`QPaintDevice::paintEngine()` const.
返回打印机使用的喷漆引擎。

### `QRectF QPrinter::paperRect(QPrinter::Unit unit) const`

**作用与语义：**

`unit`返回纸张的矩形;这通常比`pageRect()`大。

### `QPrinter::PaperSource QPrinter::paperSource() const`

**作用与语义：**

返回打印机的纸张源。这可以`Manual`打印机托盘或纸盒。

### `QPagedPaintDevice::PdfVersion QPrinter::pdfVersion() const`

**作用与语义：**

返回该打印机的PDF版本。默认是`PdfVersion_1_4`。

### `QPrintEngine *QPrinter::printEngine() const`

**作用与语义：**

返回打印机使用的打印引擎。

### `QString QPrinter::printProgram() const`

**作用与语义：**

返回发送打印输出到打印机的程序名称。
默认返回空字符串;这意味着`QPrinter`会尝试以系统依赖的方式智能。仅在X11上，你可以设置成不同的字符串以使用特定的打印程序。在其他平台上，这会返回空字符串。

### `QPrinter::PrintRange QPrinter::printRange() const`

**作用与语义：**

返回`QPrinter`的页面范围。打印设置对话框打开后，该函数返回用户选择的值。

### `QString QPrinter::printerName() const`

**作用与语义：**

返回打印机名称。该值最初被设置为默认打印机名称。

### `QString QPrinter::printerSelectionOption() const`

**作用与语义：**

返回打印机选项选择字符串。只有在打印命令被明确设置时才有用。
默认值（空字符串）意味着打印机应以系统依赖的方式选择。
任何其他值都意味着应使用给定值。
在Windows和Mac上，这个函数总是返回空字符串。

### `QPrinter::PrinterState QPrinter::printerState() const`

**作用与语义：**

返回打印机当前状态。这可能并不总是准确（例如打印机无法向操作系统报告状态）。

### `int QPrinter::resolution() const`

**作用与语义：**

返回打印机当前假设的分辨率，由`setResolution()`或打印机驱动程序设定。

### `void QPrinter::setCollateCopies(bool collate)`

**作用与语义：**

当打印对话框出现时，设置默认的汇合复选框。如果`collate`为真，将启用 setCollateCopiesEnabled()。默认值为假。该值会根据用户在打印对话框中的点击键改变。

### `void QPrinter::setColorMode(QPrinter::ColorMode newColorMode)`

**作用与语义：**

将打印机的色彩模式设置为`newColorMode`，颜色可以是`Color`或`GrayScale`。

### `void QPrinter::setCopyCount(int count)`

**作用与语义：**

将印刷的印制数量设定为`count`。
打印机驱动程序读取该设置并打印指定数量的副本。

### `void QPrinter::setCreator(const QString &creator)`

**作用与语义：**

将创建文档的应用程序名称设置为`creator`。
该功能仅适用于 X11 版本的 Qt。如果未指定创建者名称，创建者将被设置为“Qt”，后面跟某个版本号。

### `void QPrinter::setDocName(const QString &name)`

**作用与语义：**

将文档名称设置为`name`。
在 X11 上，例如文档名称作为默认输出文件名`QPrintDialog`。注意，如果打印机打印到文件，文档名称不会影响文件名。使用setOutputFile() 函数来实现此操作。

### `void QPrinter::setDuplex(QPrinter::DuplexMode duplex)`

**作用与语义：**

基于`duplex`模式实现双面打印。

### `[protected] void QPrinter::setEngines(QPrintEngine *printEngine, QPaintEngine *paintEngine)`

**作用与语义：**

该函数被`QPrinter`子类用于指定自定义打印和绘画引擎（分别为`printEngine`和`paintEngine`）。
`QPrinter`不拥有引擎的所有权，所以你需要自己管理这些引擎实例。
注意更换发动机会重置打印机状态及其所有属性。

### `void QPrinter::setFontEmbeddingEnabled(bool enable)`

**作用与语义：**

根据具体情况启用或禁用字体嵌入`enable`。

### `void QPrinter::setFromTo(int from, int to)`

**作用与语义：**

设置打印页面范围以覆盖`from`和`to`指定数字的页面，其中`from`对应范围的第一页，`to`对应最后一页。
注意：文档中的页面编号遵循惯例，即第一页为第1页。但如果`from`和`to`都设为0，则整个文档将被打印。
这个函数主要用于设置默认值，用户在打印对话框中调用 setup()时可以覆盖该值。

### `void QPrinter::setFullPage(bool fp)`

**作用与语义：**

如果`fp`为真，则支持覆盖整页;否则，绘制限制在设备报告的可打印区域内。
默认情况下，全页打印被禁用。在这种情况下，`QPrinter`坐标系的起点与可打印区域的左上角重合。
如果启用整页打印，`QPrinter`坐标系的原点与纸张左上角一致。在这种情况下，设备度量报告的尺寸与{`QPageSize`}所示完全相同。由于打印机的边距限制，可能无法在整页纸上打印，因此应用程序必须考虑边距本身。

### `void QPrinter::setOutputFileName(const QString &fileName)`

**作用与语义：**

将输出文件的名称设置为`fileName`。
设置空名（0或“”）会禁用打印到文件。设置非空名称则允许打印到文件。
这可能会改变`outputFormat()`的值。如果文件名带有“.pdf”后缀，则生成PDF。如果文件名后缀非“.pdf”，则使用带有`setOutputFormat()`的输出格式。
`QPrinter`分别使用Qt的跨平台PDF打印引擎。如果你能原生生成这种格式，比如macOS可以从打印引擎生成PDF，那么输出格式就要恢复为`NativeFormat`。

### `void QPrinter::setOutputFormat(QPrinter::OutputFormat format)`

**作用与语义：**

将该打印机的输出格式设置为`format`。
如果`format`值与当前设定相同，则不会有更改。
如果`format` `NativeFormat`，`printerName`会被设置为默认打印机。如果没有有效打印机配置，则不会有更改。如果你想用特定`printerName`设置`NativeFormat`，可以用`setPrinterName()`。

### `void QPrinter::setPageOrder(QPrinter::PageOrder pageOrder)`

**作用与语义：**

将页面顺序设置为`pageOrder`。
页码顺序可以是`QPrinter::FirstPageFirst`或`QPrinter::LastPageFirst`。应用程序负责读取页面顺序并相应打印。
该函数主要用于设置用户可在打印对话框中覆盖的默认值。
此功能仅支持X11。

### `void QPrinter::setPaperSource(QPrinter::PaperSource source)`

**作用与语义：**

把纸张来源设置设为`source`。
仅限Windows：此选项可在打印时更改，并将从下一次调用起生效`newPage()`。

### `void QPrinter::setPdfVersion(QPagedPaintDevice::PdfVersion version)`

**作用与语义：**

将该打印机的PDF版本设置为`version`。
如果`version`值与当前设定相同，则不会有更改。

### `void QPrinter::setPrintProgram(const QString &printProg)`

**作用与语义：**

将执行打印任务的程序名称设置为`printProg`。
在X11上，这个函数会让程序调用PDF输出。在其他平台上，它没有任何效果。

### `void QPrinter::setPrintRange(QPrinter::PrintRange range)`

**作用与语义：**

将打印范围选项设置为`range`。

### `void QPrinter::setPrinterName(const QString &name)`

**作用与语义：**

将打印机名称设置为`name`。
如果`name`为空，输出格式将设置为`PdfFormat`。
如果`name`不是有效的打印机，则不会有更改。
如果`name`是有效的打印机，输出格式将设置为`NativeFormat`。

### `void QPrinter::setPrinterSelectionOption(const QString &option)`

**作用与语义：**

设置打印机使用`option`来选择打印机。`option`默认为空（这意味着Qt应该足够智能来正确猜测），但可以设置为其他值以使用特定的打印机选择选项。
如果打印机选择选项在打印机激活时被更改，当前打印作业可能会受到影响，也可能不会。
这个功能在Windows和Mac上没有影响。

### `void QPrinter::setResolution(int dpi)`

**作用与语义：**

要求打印机打印速度达到`dpi`或尽可能接近`dpi`。
该设置影响坐标系，例如返回`QPainter::viewport()`。
该函数必须在 `QPainter::begin()` 前调用，才能对所有平台产生影响。

### `QList<QPrinter::PaperSource> QPrinter::supportedPaperSources() const`

**作用与语义：**

返回该打印机支持的纸张尺寸。
这些值要么是与`QPrinter::PaperSource`枚举中的某个条目相匹配的值，要么是驱动程序特殊值。驱动程序特殊值大于wingdi.h中声明的常数DMBIN_USER。
警告：此功能仅在Windows中提供。

### `QList<int> QPrinter::supportedResolutions() const`

**作用与语义：**

返回打印机表示支持的分辨率列表（每英寸点数整数列表）。
对于所有打印都直接转为 PDF 的 X11，该函数总是返回一个仅包含 PDF 分辨率的项目列表，即 72（72 dpi——但见`PrinterMode`）。

### `bool QPrinter::supportsMultipleCopies() const`

**作用与语义：**

如果打印机支持在同一个作业中打印多份同一文档，返回`true`;否则返回为false。
在大多数系统上，该函数会返回true。然而，在不支持CUPS的X11系统中，该函数会返回false。这意味着应用程序必须通过打印同一份文档所需的次数来处理副本数量。

### `int QPrinter::toPage() const`

**作用与语义：**

返回待打印页数中最后一页的编号（“To page”设置）。文档中的页面编号按照惯例，即第一页为第1页。
默认情况下，该函数返回一个特殊的值 0，意味着“访问页面”设置是未设置的。
注意：如果`fromPage()`和toPage()都返回0，表示整个文档将被打印。
程序员负责读取该设置并相应打印。

### `enum PrinterState { Idle, Active, Aborted, Error }`

**作用与语义：**

表示打印机当前状态：`Idle` 空闲、`Active` 正在打印、`Aborted` 已中止、`Error` 出错。用 `printerState()` 查询；这是状态快照，打印失败时还应结合返回值和系统打印服务诊断。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QPrinter` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
