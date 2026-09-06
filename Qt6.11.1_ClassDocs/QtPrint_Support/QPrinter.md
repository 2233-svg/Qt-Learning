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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 63 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QPrinter::ColorMode`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QPrinter` 暴露的类型声明 `Color、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ColorMode`。
- 属性名：`QPrinter`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QPrinter::DuplexMode`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QPrinter` 暴露的类型声明 `Duplex、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:DuplexMode`。
- 属性名：`QPrinter`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QPrinter::OutputFormat`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QPrinter` 暴露的类型声明 `Output、格式化`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:OutputFormat`。
- 属性名：`QPrinter`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QPrinter::PageOrder`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QPrinter` 暴露的类型声明 `Page、Order`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:PageOrder`。
- 属性名：`QPrinter`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QPrinter::PaperSource`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QPrinter` 暴露的类型声明 `Paper、来源`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:PaperSource`。
- 属性名：`QPrinter`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QPrinter::PrintRange`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QPrinter` 暴露的类型声明 `Print、Range`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:PrintRange`。
- 属性名：`QPrinter`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QPrinter::PrinterMode`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QPrinter` 暴露的类型声明 `Printer、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:PrinterMode`。
- 属性名：`QPrinter`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QPrinter::Unit`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QPrinter` 暴露的类型声明 `Unit`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Unit`。
- 属性名：`QPrinter`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QPrinter::QPrinter(QPrinter::PrinterMode mode = ScreenResolution)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPrinter` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `mode`：类型为 `QPrinter::PrinterMode`。默认值为 `ScreenResolution`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QPrinter::QPrinter(const QPrinterInfo &printer, QPrinter::PrinterMode mode = ScreenResolution)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPrinter` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `printer`：类型为 `const QPrinterInfo &`。没有默认值，调用时必须提供。传入 `const QPrinterInfo &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mode`：类型为 `QPrinter::PrinterMode`。默认值为 `ScreenResolution`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QPrinter::~QPrinter()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPrinter` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPrinter::abort()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `abort`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPrinter::collateCopies() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinter::collateCopies` 用于计算、查询或取得与“collate、Copies”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPrinter::ColorMode QPrinter::colorMode() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinter::colorMode` 用于计算、查询或取得与“color、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPrinter::ColorMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPrinter::ColorMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QPrinter::copyCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinter::copyCount` 用于计算、查询或取得与“copy、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QPrinter::creator() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinter::creator` 用于计算、查询或取得与“creator”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QPrinter::docName() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinter::docName` 用于计算、查询或取得与“doc、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPrinter::DuplexMode QPrinter::duplex() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinter::duplex` 用于计算、查询或取得与“duplex”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPrinter::DuplexMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPrinter::DuplexMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPrinter::fontEmbeddingEnabled() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinter::fontEmbeddingEnabled` 用于计算、查询或取得与“字体、Embedding、启用状态”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QPrinter::fromPage() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `fromPage`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPrinter::fullPage() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinter::fullPage` 用于计算、查询或取得与“full、Page”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPrinter::isValid() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isValid`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QPrinter::newPage()`

**API 类别：** 成员函数说明

**中文解读：** `QPrinter::newPage` 用于计算、查询或取得与“new、Page”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QPrinter::outputFileName() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinter::outputFileName` 用于计算、查询或取得与“output、File、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPrinter::OutputFormat QPrinter::outputFormat() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinter::outputFormat` 用于计算、查询或取得与“output、格式化”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPrinter::OutputFormat`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPrinter::OutputFormat`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPrinter::PageOrder QPrinter::pageOrder() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinter::pageOrder` 用于计算、查询或取得与“page、Order”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPrinter::PageOrder`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPrinter::PageOrder`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRectF QPrinter::pageRect(QPrinter::Unit unit) const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinter::pageRect` 用于计算、查询或取得与“page、Rect”相关的操作。调用时要先确认当前状态和 `unit` 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数 `unit`：类型为 `QPrinter::Unit`。没有默认值，调用时必须提供。传入 `QPrinter::Unit` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QPaintEngine *QPrinter::paintEngine() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPrinter` 的核心操作 `paintEngine`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QPaintEngine *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRectF QPrinter::paperRect(QPrinter::Unit unit) const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinter::paperRect` 用于计算、查询或取得与“paper、Rect”相关的操作。调用时要先确认当前状态和 `unit` 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数 `unit`：类型为 `QPrinter::Unit`。没有默认值，调用时必须提供。传入 `QPrinter::Unit` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPrinter::PaperSource QPrinter::paperSource() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinter::paperSource` 用于计算、查询或取得与“paper、来源”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPrinter::PaperSource`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPrinter::PaperSource`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPagedPaintDevice::PdfVersion QPrinter::pdfVersion() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinter::pdfVersion` 用于计算、查询或取得与“pdf、Version”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPagedPaintDevice::PdfVersion`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPagedPaintDevice::PdfVersion`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPrintEngine *QPrinter::printEngine() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinter::printEngine` 用于计算、查询或取得与“print、Engine”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPrintEngine *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPrintEngine *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QPrinter::printProgram() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinter::printProgram` 用于计算、查询或取得与“print、Program”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPrinter::PrintRange QPrinter::printRange() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinter::printRange` 用于计算、查询或取得与“print、Range”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPrinter::PrintRange`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPrinter::PrintRange`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QPrinter::printerName() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinter::printerName` 用于计算、查询或取得与“printer、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QPrinter::printerSelectionOption() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinter::printerSelectionOption` 用于计算、查询或取得与“printer、Selection、Option”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPrinter::PrinterState QPrinter::printerState() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinter::printerState` 用于计算、查询或取得与“printer、State”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPrinter::PrinterState`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPrinter::PrinterState`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QPrinter::resolution() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinter::resolution` 用于计算、查询或取得与“resolution”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPrinter::setCollateCopies(bool collate)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setCollateCopies`。调用它会改变 `QPrinter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `collate`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPrinter::setColorMode(QPrinter::ColorMode newColorMode)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setColorMode`。调用它会改变 `QPrinter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `newColorMode`：类型为 `QPrinter::ColorMode`。没有默认值，调用时必须提供。传入 `QPrinter::ColorMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPrinter::setCopyCount(int count)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setCopyCount`。调用它会改变 `QPrinter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `count`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPrinter::setCreator(const QString &creator)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setCreator`。调用它会改变 `QPrinter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `creator`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPrinter::setDocName(const QString &name)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDocName`。调用它会改变 `QPrinter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPrinter::setDuplex(QPrinter::DuplexMode duplex)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDuplex`。调用它会改变 `QPrinter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `duplex`：类型为 `QPrinter::DuplexMode`。没有默认值，调用时必须提供。传入 `QPrinter::DuplexMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QPrinter::setEngines(QPrintEngine *printEngine, QPaintEngine *paintEngine)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setEngines`。调用它会改变 `QPrinter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `printEngine`：类型为 `QPrintEngine *`。没有默认值，调用时必须提供。传入 `QPrintEngine *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `paintEngine`：类型为 `QPaintEngine *`。没有默认值，调用时必须提供。传入 `QPaintEngine *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPrinter::setFontEmbeddingEnabled(bool enable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFontEmbeddingEnabled`。调用它会改变 `QPrinter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPrinter::setFromTo(int from, int to)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFromTo`。调用它会改变 `QPrinter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `from`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `to`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPrinter::setFullPage(bool fp)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFullPage`。调用它会改变 `QPrinter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `fp`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPrinter::setOutputFileName(const QString &fileName)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setOutputFileName`。调用它会改变 `QPrinter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPrinter::setOutputFormat(QPrinter::OutputFormat format)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setOutputFormat`。调用它会改变 `QPrinter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `format`：类型为 `QPrinter::OutputFormat`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPrinter::setPageOrder(QPrinter::PageOrder pageOrder)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPageOrder`。调用它会改变 `QPrinter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `pageOrder`：类型为 `QPrinter::PageOrder`。没有默认值，调用时必须提供。传入 `QPrinter::PageOrder` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPrinter::setPaperSource(QPrinter::PaperSource source)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPaperSource`。调用它会改变 `QPrinter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `source`：类型为 `QPrinter::PaperSource`。没有默认值，调用时必须提供。源对象、源索引或源数据；它通常决定操作的输入，转换后要确认源的生命周期和线程归属。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPrinter::setPdfVersion(QPagedPaintDevice::PdfVersion version)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPdfVersion`。调用它会改变 `QPrinter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `version`：类型为 `QPagedPaintDevice::PdfVersion`。没有默认值，调用时必须提供。传入 `QPagedPaintDevice::PdfVersion` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPrinter::setPrintProgram(const QString &printProg)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPrintProgram`。调用它会改变 `QPrinter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `printProg`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPrinter::setPrintRange(QPrinter::PrintRange range)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPrintRange`。调用它会改变 `QPrinter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `range`：类型为 `QPrinter::PrintRange`。没有默认值，调用时必须提供。传入 `QPrinter::PrintRange` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPrinter::setPrinterName(const QString &name)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPrinterName`。调用它会改变 `QPrinter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPrinter::setPrinterSelectionOption(const QString &option)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPrinterSelectionOption`。调用它会改变 `QPrinter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `option`：类型为 `const QString &`。没有默认值，调用时必须提供。选项或绘制/行为配置对象；调用前确认其中的状态、矩形和样式信息已经初始化。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QPrinter::setResolution(int dpi)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setResolution`。调用它会改变 `QPrinter` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `dpi`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QPrinter::PaperSource> QPrinter::supportedPaperSources() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinter::supportedPaperSources` 用于计算、查询或取得与“supported、Paper、Sources”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QPrinter::PaperSource>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QPrinter::PaperSource>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<int> QPrinter::supportedResolutions() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinter::supportedResolutions` 用于计算、查询或取得与“supported、Resolutions”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<int>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<int>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPrinter::supportsMultipleCopies() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `supportsMultipleCopies`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QPrinter::toPage() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toPage`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum PrinterState { Idle, Active, Aborted, Error }`

**API 类别：** 公有类型

**中文解读：** 这是 `QPrinter` 暴露的类型声明 `Printer、State`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
