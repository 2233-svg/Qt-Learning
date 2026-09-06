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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QPrinterInfo::QPrinterInfo()`

**作用与语义：**

构造一个空的 QPrinterInfo 对象。

### `[explicit] QPrinterInfo::QPrinterInfo(const QPrinter &printer)`

**作用与语义：**

从`printer`构造一个QPrinterInfo对象。

### `QPrinterInfo::QPrinterInfo(const QPrinterInfo &other)`

**作用与语义：**

复制了`other`。

### `[noexcept] QPrinterInfo::~QPrinterInfo()`

**作用与语义：**

销毁`QPrinterInfo`对象。对对象中值的引用将失效。

### `[static] QStringList QPrinterInfo::availablePrinterNames()`

**作用与语义：**

返回该系统中所有可用的打印机名称列表。
建议使用该方法代替 `availablePrinters()`，因为在大多数系统上会更快。
注意，如果在本地系统或远程打印服务器上进行更改，列表可能会过时。仅在需要时实例化所需的`QPrinterInfo`实例，并且调用前务必检查有效性。

### `[static] QList<QPrinterInfo> QPrinterInfo::availablePrinters()`

**作用与语义：**

返回该系统中所有可用打印机的 `QPrinterInfo` 对象列表。
不建议使用此方法，因为创建每个打印机实例可能耗时较长，尤其是当有远程联网打印机时，且如果在本地系统或远程打印服务器上做了更改，保留的实例可能会过时。请使用`availablePrinterNames()`，并且仅根据需要实例实例。

### `QPrinter::ColorMode QPrinterInfo::defaultColorMode() const`

**作用与语义：**

返回该打印机的默认色彩模式。

### `QPrinter::DuplexMode QPrinterInfo::defaultDuplexMode() const`

**作用与语义：**

返回该打印机的默认双工模式。

### `QPageSize QPrinterInfo::defaultPageSize() const`

**作用与语义：**

返回该打印机当前默认页面大小。

### `[static] QPrinterInfo QPrinterInfo::defaultPrinter()`

**作用与语义：**

返回系统默认打印机。
如果没有默认打印机，使用前应使用`isNull()`检查返回值。
在某些系统上，可能存在可用的打印机，但没有任何打印机被设置为默认打印机。

### `[static] QString QPrinterInfo::defaultPrinterName()`

**作用与语义：**

返回当前默认打印机名称。

### `QString QPrinterInfo::description() const`

**作用与语义：**

返回打印机的人类可读描述。

### `bool QPrinterInfo::isDefault() const`

**作用与语义：**

返回该打印机是否为默认打印机。

### `bool QPrinterInfo::isNull() const`

**作用与语义：**

返回该`QPrinterInfo`对象是否包含打印机定义。
例如，当系统中没有打印机时调用`defaultPrinter()`，可能会导致空`QPrinterInfo`对象。

### `bool QPrinterInfo::isRemote() const`

**作用与语义：**

返回该打印机是否为远程网络打印机。

### `QString QPrinterInfo::location() const`

**作用与语义：**

返回打印机的可读位置。

### `QString QPrinterInfo::makeAndModel() const`

**作用与语义：**

返回印刷机的可读品牌和型号。

### `QPageSize QPrinterInfo::maximumPhysicalPageSize() const`

**作用与语义：**

返回该打印机支持的最大物理页面大小。

### `QPageSize QPrinterInfo::minimumPhysicalPageSize() const`

**作用与语义：**

返回该打印机支持的最小物理页面大小。

### `[static] QPrinterInfo QPrinterInfo::printerInfo(const QString &printerName)`

**作用与语义：**

退回打印机`printerName`。
如果指定打印机不存在，使用前应使用`isNull()`检查返回值。

### `QString QPrinterInfo::printerName() const`

**作用与语义：**

返回打印机名称。
这是一个唯一标识，用于识别打印机，可能无法被人类读取。

### `QPrinter::PrinterState QPrinterInfo::state() const`

**作用与语义：**

返回打印机当前状态。
该状态可能并不总是准确，取决于平台、打印机驱动程序或打印机本身。

### `QList<QPrinter::ColorMode> QPrinterInfo::supportedColorModes() const`

**作用与语义：**

返回该打印机支持的色彩模式。

### `QList<QPrinter::DuplexMode> QPrinterInfo::supportedDuplexModes() const`

**作用与语义：**

返回该打印机支持的双工模式列表。

### `QList<QPageSize> QPrinterInfo::supportedPageSizes() const`

**作用与语义：**

返回该打印机支持的页面尺寸列表。

### `QList<int> QPrinterInfo::supportedResolutions() const`

**作用与语义：**

返回该打印机支持的分辨率列表。

### `bool QPrinterInfo::supportsCustomPageSizes() const`

**作用与语义：**

返回该打印机是否支持自定义页面大小。

### `QPrinterInfo &QPrinterInfo::operator=(const QPrinterInfo &other)`

**作用与语义：**

将`QPrinterInfo`对象设置为等于 `other`。

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
