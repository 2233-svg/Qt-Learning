# QPrinterInfo

> Qt 6.11.1 · Qt Print Support

## 1. 先建立直觉

**一句话定位：** `QPrinterInfo` 是 Qt 的值类型，围绕“PrinterInfo”保存可复制的数据，并提供查询、转换或修改 API。

**模块背景：** Qt Print Support 提供打印机、打印预览和打印作业相关接口。

### 这是什么

`QPrinterInfo` 是 Qt 值类型与隐式共享机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

**适用场景：** 先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

## 2. 依赖与对象关系

- 头文件：`#include <QPrinterInfo>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS PrintSupport)
target_link_libraries(mytarget PRIVATE Qt6::PrintSupport)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

### 状态、生命周期和线程

**生命周期：** 值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

**状态与结果：** 重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

**线程与事件循环：** 值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

## 3. 直接使用

先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QPrinterInfo()`
- `QPrinterInfo(const QPrinter &printer)`
- `QPrinterInfo(const QPrinterInfo &other)`
- `~QPrinterInfo()`
- `QPrinter::ColorMode defaultColorMode() const`
- `QPrinter::DuplexMode defaultDuplexMode() const`
- `QPageSize defaultPageSize() const`
- `QString description() const`
- `bool isDefault() const`
- `bool isNull() const`
- `bool isRemote() const`
- `QString location() const`
- `QString makeAndModel() const`
- `QPageSize maximumPhysicalPageSize() const`
- `QPageSize minimumPhysicalPageSize() const`
- `QString printerName() const`
- `QPrinter::PrinterState state() const`
- `QList<QPrinter::ColorMode> supportedColorModes() const`
- `QList<QPrinter::DuplexMode> supportedDuplexModes() const`
- `QList<QPageSize> supportedPageSizes() const`
- `QList<int> supportedResolutions() const`
- `bool supportsCustomPageSizes() const`
- `QPrinterInfo & operator=(const QPrinterInfo &other)`

### 静态公有成员

- `QStringList availablePrinterNames()`
- `QList<QPrinterInfo> availablePrinters()`
- `QPrinterInfo defaultPrinter()`
- `QString defaultPrinterName()`
- `QPrinterInfo printerInfo(const QString &printerName)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 28 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QPrinterInfo::QPrinterInfo()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPrinterInfo` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QPrinterInfo::QPrinterInfo(const QPrinter &printer)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPrinterInfo` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `printer`：类型为 `const QPrinter &`。没有默认值，调用时必须提供。传入 `const QPrinter &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPrinterInfo::QPrinterInfo(const QPrinterInfo &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPrinterInfo` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QPrinterInfo &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QPrinterInfo::~QPrinterInfo()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPrinterInfo` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QStringList QPrinterInfo::availablePrinterNames()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `availablePrinterNames`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QStringList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QList<QPrinterInfo> QPrinterInfo::availablePrinters()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `availablePrinters`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QList<QPrinterInfo>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPrinter::ColorMode QPrinterInfo::defaultColorMode() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinterInfo::defaultColorMode` 用于计算、查询或取得与“default、Color、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPrinter::ColorMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPrinter::ColorMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPrinter::DuplexMode QPrinterInfo::defaultDuplexMode() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinterInfo::defaultDuplexMode` 用于计算、查询或取得与“default、Duplex、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPrinter::DuplexMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPrinter::DuplexMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPageSize QPrinterInfo::defaultPageSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinterInfo::defaultPageSize` 用于计算、查询或取得与“default、Page、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPageSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPageSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QPrinterInfo QPrinterInfo::defaultPrinter()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `defaultPrinter`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QPrinterInfo`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QPrinterInfo::defaultPrinterName()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `defaultPrinterName`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QPrinterInfo::description() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinterInfo::description` 用于计算、查询或取得与“description”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPrinterInfo::isDefault() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isDefault`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPrinterInfo::isNull() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isNull`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPrinterInfo::isRemote() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isRemote`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QPrinterInfo::location() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinterInfo::location` 用于计算、查询或取得与“location”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QPrinterInfo::makeAndModel() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinterInfo::makeAndModel` 用于计算、查询或取得与“make、And、Model”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPageSize QPrinterInfo::maximumPhysicalPageSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinterInfo::maximumPhysicalPageSize` 用于计算、查询或取得与“最大值、Physical、Page、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPageSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPageSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPageSize QPrinterInfo::minimumPhysicalPageSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinterInfo::minimumPhysicalPageSize` 用于计算、查询或取得与“最小值、Physical、Page、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPageSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPageSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QPrinterInfo QPrinterInfo::printerInfo(const QString &printerName)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `printerInfo`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QPrinterInfo`。
- 参数 `printerName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QPrinterInfo::printerName() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinterInfo::printerName` 用于计算、查询或取得与“printer、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPrinter::PrinterState QPrinterInfo::state() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinterInfo::state` 用于计算、查询或取得与“state”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPrinter::PrinterState`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPrinter::PrinterState`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QPrinter::ColorMode> QPrinterInfo::supportedColorModes() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinterInfo::supportedColorModes` 用于计算、查询或取得与“supported、Color、Modes”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QPrinter::ColorMode>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QPrinter::ColorMode>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QPrinter::DuplexMode> QPrinterInfo::supportedDuplexModes() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinterInfo::supportedDuplexModes` 用于计算、查询或取得与“supported、Duplex、Modes”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QPrinter::DuplexMode>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QPrinter::DuplexMode>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QPageSize> QPrinterInfo::supportedPageSizes() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinterInfo::supportedPageSizes` 用于计算、查询或取得与“supported、Page、Sizes”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QPageSize>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QPageSize>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<int> QPrinterInfo::supportedResolutions() const`

**API 类别：** 成员函数说明

**中文解读：** `QPrinterInfo::supportedResolutions` 用于计算、查询或取得与“supported、Resolutions”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<int>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<int>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QPrinterInfo::supportsCustomPageSizes() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `supportsCustomPageSizes`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPrinterInfo &QPrinterInfo::operator=(const QPrinterInfo &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPrinterInfo` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QPrinterInfo &`。
- 参数 `other`：类型为 `const QPrinterInfo &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

### 状态和错误边界

重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

### 线程边界

值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

### 最容易出现的错误

不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QPrinterInfo` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
