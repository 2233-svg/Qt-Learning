# QPrintEngine

> Qt 6.11.1 · Qt Print Support

## 1. 先建立直觉

**一句话定位：** 这是 Qt Print Support 中围绕“Print引擎”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Print Support 提供打印机、打印预览和打印作业相关接口。

### 这是什么

`QPrintEngine` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QPrintEngine>`
- 继承自：未在类页中列出
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

- `enum PrintEnginePropertyKey { PPK_CollateCopies, PPK_ColorMode, PPK_Creator, PPK_Duplex, PPK_DocumentName, …, PPK_CustomBase }`

### 公有函数

- `virtual ~QPrintEngine()`
- `virtual bool abort() = 0`
- `virtual int metric(QPaintDevice::PaintDeviceMetric id) const = 0`
- `virtual bool newPage() = 0`
- `virtual QPrinter::PrinterState printerState() const = 0`
- `virtual QVariant property(QPrintEngine::PrintEnginePropertyKey key) const = 0`
- `virtual void setProperty(QPrintEngine::PrintEnginePropertyKey key, const QVariant &value) = 0`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QPrintEngine::PrintEnginePropertyKey`

**作用与语义：**

该枚举用于打印引擎与 `QPrinter` 之间的属性交流。某个属性可能被某个打印引擎支持，也可能不支持。
- `QPrintEngine::PPK_CollateCopies`：`0`;一个布尔值，指示打印输出是否应被整理。
- `QPrintEngine::PPK_ColorMode`：`1`;指`QPrinter::ColorMode`，颜色或单色。
- `QPrintEngine::PPK_Creator`：`2`;描述文档创建者的字符串。
- `QPrintEngine::PPK_Duplex`：`20`;一个布尔值，表示打印时打印时是否应使用打印机纸张的两面。
- `QPrintEngine::PPK_DocumentName`：`3`;描述加载器中文档名称的字符串。
- `QPrintEngine::PPK_FontEmbedding`：`19`;一个布尔值，表示文档字体的数据是否应嵌入发送到打印机的数据中。
- `QPrintEngine::PPK_FullPage`：`4`;描述打印机是否应为全页的布尔值。
- `QPrintEngine::PPK_NumberOfCopies`：`5`;过时。一个整数表示副本数量。改用PPK_CopyCount。
- `QPrintEngine::PPK_Orientation`：`6`;指定`QPageLayout::Orientation`值。
- `QPrintEngine::PPK_OutputFileName`：`7`;输出文件名作为字符串表示。空文件名表示打印机不应打印文件。
- `QPrintEngine::PPK_PageOrder`：`8`;指定`QPrinter::PageOrder`值。
- `QPrintEngine::PPK_PageRect`：`9`;指定页面矩形的`QRect`
- `QPrintEngine::PPK_PageSize`：`10`;已过时。改用PPK_PaperSize。
- `QPrintEngine::PPK_PaperRect`：`11`;一个指定纸张矩形的`QRect`。
- `QPrintEngine::PPK_PaperSource`：`12`;指定`QPrinter::PaperSource`值。
- `QPrintEngine::PPK_PaperSources`：`21`;指定多个`QPrinter::PaperSource`值。
- `QPrintEngine::PPK_PaperName`：`26`;一个表示论文名称的字符串。
- `QPrintEngine::PPK_PaperSize`：`PPK_PageSize`;指定QPrinter：:P aperSize值。
- `QPrintEngine::PPK_PrinterName`：`13`;表示打印机名称的字符串。
- `QPrintEngine::PPK_PrinterProgram`：`14`;一个字符串，指定用于打印的打印机程序名称，
- `QPrintEngine::PPK_Resolution`：`15`;描述该打印机每英寸点数的整数。
- `QPrintEngine::PPK_SelectionOption`：`16`
- `QPrintEngine::PPK_SupportedResolutions`：`17`;一串整数QVariant，描述打印机支持的分辨率集合。
- `QPrintEngine::PPK_WindowsPageSize`：`18`;在Windows上指定DM_PAPER条目的整数。
- `QPrintEngine::PPK_CustomPaperSize`：`22`;`QSizeF`指定`QPrinter::Point`中自定义纸张尺寸。
- `QPrintEngine::PPK_PageMargins`：`23`;<`QVariant`>包含`QPrinter::Point`单位中左边际、上边际、右边和底边距值的`QList`。
- `QPrintEngine::PPK_CopyCount`：`24`;一个整数表示要印刷的副本数量。
- `QPrintEngine::PPK_SupportsMultipleCopies`：`25`;一个布尔值，表示打印机是否支持在一个作业中打印多份副本。
- `QPrintEngine::PPK_QPageSize`：`27`;使用`QPageSize`对象设置页面大小。
- `QPrintEngine::PPK_QPageMargins`：`28`;使用`QMarginsF`和`QPageLayout::Unit`的std：:p air设置页边距。
- `QPrintEngine::PPK_QPageLayout`：`29`;使用`QPageLayout`对象设置页面布局。
- `QPrintEngine::PPK_CustomBase`：`0xff00`;扩展的基础。

### `[virtual noexcept] QPrintEngine::~QPrintEngine()`

**作用与语义：**

毁掉打印引擎。

### `[pure virtual] bool QPrintEngine::abort()`

**作用与语义：**

指示打印引擎中止打印过程。成功时返回真;否则返回`false`。

### `[pure virtual] int QPrintEngine::metric(QPaintDevice::PaintDeviceMetric id) const`

**作用与语义：**

返回给定`id`的度量。

### `[pure virtual] bool QPrintEngine::newPage()`

**作用与语义：**

指示打印引擎开始新页面。如果打印机能够创建新页面，返回`true`;否则返回`false`。

### `[pure virtual] QPrinter::PrinterState QPrintEngine::printerState() const`

**作用与语义：**

返回打印引擎当前使用的打印机状态。

### `[pure virtual] QVariant QPrintEngine::property(QPrintEngine::PrintEnginePropertyKey key) const`

**作用与语义：**

返回`key`指定打印引擎属性。

### `[pure virtual] void QPrintEngine::setProperty(QPrintEngine::PrintEnginePropertyKey key, const QVariant &value)`

**作用与语义：**

将`key`指定的打印引擎属性设置为给定的`value`。

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

`QPrintEngine` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
