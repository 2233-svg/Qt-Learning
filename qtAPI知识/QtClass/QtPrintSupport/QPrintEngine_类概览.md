# QPrintEngine 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPrintEngine>`  
> 所属模块：`Qt6::PrintSupport`  
> 继承：无

## 它解决什么问题

`QPrintEngine` 定义了 `QPrinter` 与具体打印子系统之间的接口。`QPrinter` 面向应用层，负责提供统一的纸张、份数、页面范围和输出格式 API；`QPrintEngine` 面向后端，负责把这些设置映射到原生打印机、PDF 输出或自定义打印系统。

普通应用不直接使用或继承它。只有要接入新的打印后端时才需要实现，例如把 Qt 的绘制结果交给一个专有打印服务或虚拟输出设备。常见实现方式是同时派生：

```text
QPaintEngine
  + QPrintEngine
       └─ 自定义打印引擎
```

`QPaintEngine` 接收实际绘制命令，`QPrintEngine` 接收打印机配置与分页控制。两者缺一不可：只有打印属性而没有绘制实现，无法输出页面；只有绘制实现而没有打印属性桥接，`QPrinter` 无法正确配置后端。

## 属性键是后端协议，不是应用设置界面

`PrintEnginePropertyKey` 用于 `QPrinter` 和引擎之间交换属性。每个后端可以只支持其中一部分键，调用 `property()` 得到无效值并不一定是异常，而可能是该后端不支持该能力。

实现方应保证 `property(key)` 与 `setProperty(key, value)` 对支持的键成对工作，并对 `QVariant` 类型做校验。不要把用户输入的任意 QVariant 直接强转成后端参数，否则错误的值可能在真正开始打印时才暴露。

## 作业状态与分页

- `newPage()`：要求后端完成当前页并开始新页；
- `abort()`：尽力取消当前作业，可能因数据已交给系统队列而失败；
- `printerState()`：返回后端报告的打印机状态；
- `metric()`：返回 `QPaintDevice` 所需的尺寸、分辨率等度量。

这组接口都是引擎契约。对应用而言，应该调用 `QPrinter::newPage()`、`QPrinter::abort()` 等高层 API，而不是直接接触引擎。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `enum PrintEnginePropertyKey` | 定义 `QPrinter` 与打印引擎交换配置的属性键。 | 并非每个后端支持全部键；实现方需为支持的键维护 QVariant 类型约定。 |
| 枚举值 | `PPK_CollateCopies` | 表示逐份打印设置。 | 后端不支持多份时可能需要上层重复输出。 |
| 枚举值 | `PPK_ColorMode` | 表示彩色或灰度模式。 | 设备能力可能限制最终输出。 |
| 枚举值 | `PPK_Creator` | 表示创建文档的应用名称。 | 多为元数据，平台支持度不同。 |
| 枚举值 | `PPK_DocumentName` | 表示打印作业或文档名称。 | 适合在系统队列中显示，非输出文件名。 |
| 枚举值 | `PPK_Duplex` | 表示单双面打印模式。 | 要结合设备支持的双面模式。 |
| 枚举值 | `PPK_FontEmbedding` | 表示字体嵌入设置。 | 仅对支持相应输出格式的后端有效。 |
| 枚举值 | `PPK_FullPage` | 表示是否以整张纸为坐标原点。 | 启用后应用要自行考虑设备不可打印边距。 |
| 枚举值 | `PPK_NumberOfCopies` | 表示输出份数。 | 后端不支持时应用可能需要自行重复渲染。 |
| 枚举值 | `PPK_Orientation` | 表示页面方向。 | 通常应在开始绘制前设置。 |
| 枚举值 | `PPK_OutputFileName` | 表示输出文件路径。 | 需处理写权限、输出格式与扩展名一致性。 |
| 枚举值 | `PPK_PageOrder` | 表示正序或逆序打印。 | 部分平台由应用自己根据此设置控制分页顺序。 |
| 枚举值 | `PPK_PageRect` | 表示可绘制页面矩形。 | 与完整纸张矩形及页边距不同。 |
| 枚举值 | `PPK_PaperRect` | 表示完整纸张矩形。 | 可能大于实际可打印区域。 |
| 枚举值 | `PPK_PaperSource` | 表示纸盒或进纸来源。 | 平台和驱动支持差异很大。 |
| 枚举值 | `PPK_PrinterName` | 表示目标打印机系统名称。 | 选中无效名称时应保持或报告失败。 |
| 枚举值 | `PPK_PrinterProgram` | 表示提交打印任务的外部程序。 | 主要用于特定 Unix 后端。 |
| 枚举值 | `PPK_Resolution` | 表示目标 dpi。 | 应在开始绘制前确定，影响坐标系。 |
| 枚举值 | `PPK_SupportedResolutions` | 表示设备支持的 dpi 列表。 | 类型和内容由后端约定，返回前保持稳定。 |
| 枚举值 | `PPK_WindowsPageSize` | 表示 Windows 特定页面大小信息。 | 仅用于平台后端，不应写进跨平台应用逻辑。 |
| 枚举值 | `PPK_CustomPaperSize` | 表示自定义纸张尺寸。 | 与后端能力和页面布局协商一致。 |
| 枚举值 | `PPK_PageMargins` | 表示页边距信息。 | 需区分逻辑边距和物理不可打印边距。 |
| 枚举值 | `PPK_PageSize` | 表示标准页面尺寸。 | 与 `QPageSize` 和页面布局保持同步。 |
| 枚举值 | `PPK_PrinterState` | 表示当前设备状态。 | 驱动或远程设备可能无法报告精确状态。 |
| 枚举值 | `PPK_OutputFormat` | 表示原生或 PDF 等输出格式。 | 切换格式可能需要重置后端配置。 |
| 枚举值 | `PPK_PaperName` | 表示纸张名称。 | 通常是后端或驱动层描述。 |
| 枚举值 | `PPK_CustomBase` | 自定义打印属性键的起始值。 | 扩展键应避免与 Qt 保留键冲突。 |
| 析构 | `~QPrintEngine()` | 销毁打印引擎。 | 引擎实例所有权由具体 `QPrinter` 子类或后端设计决定。 |
| 取消作业 | `abort()` | 尝试中止当前打印作业，成功返回 `true`。 | 系统队列已接收全部数据时可能无法取消。 |
| 查询度量 | `metric(QPaintDevice::PaintDeviceMetric id) const` | 返回指定绘制设备度量，例如分辨率或尺寸。 | 必须与真实输出设备一致，否则 Qt 绘制坐标会出错。 |
| 新建页面 | `newPage()` | 完成当前页并开始新页，成功返回 `true`。 | 只能在活跃打印作业中成功；绘制下一页前调用。 |
| 打印机状态 | `printerState() const` | 返回后端报告的 `QPrinter::PrinterState`。 | 状态受驱动和平台限制，不能保证实时准确。 |
| 读取属性 | `property(PrintEnginePropertyKey key) const` | 返回指定打印属性的 QVariant 值。 | 不支持的键可返回无效值；调用方需处理。 |
| 设置属性 | `setProperty(PrintEnginePropertyKey key, const QVariant &value)` | 设置指定打印属性。 | 实现方校验 key 和 QVariant 类型；应用优先用 `QPrinter` 高层 API。 |

## 易错点

1. 应用开发中使用 `QPrinter`，只有实现新打印后端时才直接处理 `QPrintEngine`。
2. 自定义后端通常需要同时实现 `QPaintEngine` 和 `QPrintEngine`。
3. `property()` 不支持某个键不一定是错误，可能是设备能力限制。
4. 引擎度量必须与真实输出一致，否则字体、边距和分页都会偏差。

### 一句话总结

`QPrintEngine` 是 `QPrinter` 与具体打印后端之间的协议层：它承接打印属性、页面推进、取消和设备度量，让同一套 Qt 绘制代码能够落到不同输出系统。
