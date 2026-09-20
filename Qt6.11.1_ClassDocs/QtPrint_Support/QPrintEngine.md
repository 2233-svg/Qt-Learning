# QPrintEngine
> Qt 6.11.1 · Qt Print Support · 来自 `QPrintEngine`

## 1. 先建立直觉

`QPrintEngine` 是 Qt 打印后端的抽象接口。普通应用几乎不会直接使用它；你平时操作的是 `QPrinter`，而 `QPrinter` 内部通过 print engine 和 paint engine 把页面命令送到 PDF、系统打印服务或自定义后端。

只有在实现自定义打印设备、扩展打印后端、或调试 Qt 打印内部时，才需要认真看它。

## 2. 类说明

保留类说明：这些 API 来自 `QPrintEngine`，属于 Qt Print Support 模块，用于抽象打印作业属性、分页、状态和底层输出。

它是纯虚接口，核心职责是接收属性键值、报告设备指标、翻页、终止作业和返回状态。绘制本身还要配合 `QPaintEngine`。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `abort()` | 中止当前打印作业。 |
| `newPage()` | 切换到下一页。 |
| `metric(QPaintDevice::PaintDeviceMetric)` | 返回设备指标，如尺寸、DPI。 |
| `printerState()` | 返回打印机状态。 |
| `property(PrintEnginePropertyKey)` | 读取打印属性。 |
| `setProperty(PrintEnginePropertyKey, QVariant)` | 写入打印属性。 |
| `PrintEnginePropertyKey` | 属性键枚举，覆盖份数、颜色、纸张、边距、输出文件、打印机名等。 |
| `PPK_QPageLayout` | 现代页布局属性，承载 `QPageLayout`。 |
| `PPK_QPageSize`、`PPK_QPageMargins` | 现代纸张和页边距属性。 |
| `PPK_CustomBase` | 自定义扩展属性的起点。 |

## 4. 属性键的理解方式

`PrintEnginePropertyKey` 是打印后端和 `QPrinter` 之间的字典协议。比如：

| 属性组 | 典型键 |
| --- | --- |
| 作业身份 | `PPK_DocumentName`、`PPK_Creator`、`PPK_PrinterName` |
| 输出目标 | `PPK_OutputFileName`、`PPK_PrinterProgram` |
| 页面设置 | `PPK_QPageLayout`、`PPK_QPageSize`、`PPK_QPageMargins` |
| 打印选项 | `PPK_ColorMode`、`PPK_Duplex`、`PPK_CopyCount`、`PPK_CollateCopies` |
| 设备能力 | `PPK_SupportedResolutions`、`PPK_PaperSources`、`PPK_SupportsMultipleCopies` |

## 5. 使用场景

| 场景 | 是否该直接用 |
| --- | --- |
| 普通应用打印/PDF | 不该，使用 `QPrinter`。 |
| 自定义分页绘图设备 | 可能需要，实现引擎并接入 `QPrinter::setEngines()`。 |
| 调试 Qt 打印后端 | 可以通过 `QPrinter::printEngine()` 观察属性。 |
| 跨平台打印抽象开发 | 需要理解属性键和平台后端映射。 |

## 6. 常见坑与经验

不要把 `QPrintEngine` 当稳定业务 API 来堆功能。它更接近后端接口，平台差异明显，属性类型也依赖约定；业务层应尽量停留在 `QPrinter`、`QPageLayout`、`QPrinterInfo`。

`setProperty()` 里的 `QVariant` 类型必须和键匹配。传错类型不一定马上崩，但后端可能忽略、回退默认值，或到真正输出时才失败。

自定义引擎需要同时考虑 `QPaintEngine`。只有 print engine 负责属性和分页还不够，`QPainter` 的绘图命令必须有 paint engine 承接。

## 7. 知识点覆盖

- Qt 打印后端接口和 `QPrinter` 的关系。
- 打印属性键值协议。
- 分页、终止、状态、设备指标。
- 自定义打印后端与 `QPaintEngine` 的配合。
