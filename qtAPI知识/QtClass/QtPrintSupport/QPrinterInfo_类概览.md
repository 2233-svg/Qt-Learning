# QPrinterInfo 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPrinterInfo>`  
> 所属模块：`Qt6::PrintSupport`  
> 继承：无

## 它解决什么问题

`QPrinterInfo` 是“系统中已有打印机”的只读描述对象。它不执行打印，也不承载绘制设备；它负责枚举打印机、判断默认打印机、查询设备能力，并把选中的打印机信息交给 `QPrinter`。

常见流程是先快速取得名称，再按需构造详细信息：

```cpp
const QStringList names = QPrinterInfo::availablePrinterNames();
for (const QString &name : names) {
    const QPrinterInfo info = QPrinterInfo::printerInfo(name);
    if (!info.isNull())
        addPrinterToUi(info.printerName(), info.description());
}
```

Qt 建议优先使用 `availablePrinterNames()`。与 `availablePrinters()` 相比，它在多数系统上更快，尤其是存在远程网络打印机时。只有真正需要能力信息时，再针对名称调用 `printerInfo()`。

## 发现、快照与有效性

`QPrinterInfo` 是系统打印机配置的一份快照。网络打印机、系统默认打印机或驱动状态可能在之后发生变化，因此：

- `defaultPrinter()` 和 `printerInfo(name)` 的返回值先调用 `isNull()`；
- 在真正提交打印前，让 `QPrinter` 或 `QPainter::begin()` 再确认设备可用；
- 不要长期缓存 `availablePrinters()` 的结果，把它当作永久准确的设备清单。

`printerName()` 是系统标识，可能不适合显示给用户；显示名称更适合用 `description()`，位置可用 `location()`，型号可用 `makeAndModel()`。

## 选择设备后如何交给 `QPrinter`

```cpp
const QPrinterInfo selected = QPrinterInfo::printerInfo(selectedName);
if (selected.isNull())
    return;

QPrinter printer(selected);
```

在这里，`QPrinterInfo` 负责“发现和选择”，`QPrinter` 负责“配置和绘制”。不要试图通过 `QPrinterInfo` 修改纸张、份数或输出文件，它只提供查询能力。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QPrinterInfo()` | 创建空的打印机信息对象。 | `isNull()` 会返回 `true`；不应直接当作可用设备。 |
| 构造 | `QPrinterInfo(const QPrinter &printer)` | 从 `QPrinter` 构造对应的打印机信息。 | 仅描述当前设备选择，不等于复制打印作业设置。 |
| 构造 | `QPrinterInfo(const QPrinterInfo &other)` | 复制另一份打印机信息。 | 是值类型快照，系统设备状态仍可能随后变化。 |
| 析构 | `~QPrinterInfo()` | 销毁打印机信息对象。 | 由对象值语义管理，内部引用随对象销毁失效。 |
| 可用名称 | `availablePrinterNames()` | 返回系统可用打印机名称列表。 | 首选枚举 API，通常比构造全部 `QPrinterInfo` 更快。 |
| 可用设备 | `availablePrinters()` | 返回系统全部可用打印机的信息对象。 | 远程设备上可能很慢且快照易过期，按需使用。 |
| 默认颜色 | `defaultColorMode() const` | 返回该打印机的默认彩色或灰度模式。 | 默认能力不等于用户最终在对话框中选择的模式。 |
| 默认双面 | `defaultDuplexMode() const` | 返回该打印机的默认单双面模式。 | 以设备和驱动报告为准，实际任务仍要检查支持能力。 |
| 默认页面大小 | `defaultPageSize() const` | 返回该打印机当前默认页面大小。 | 与应用指定或用户选择的页面大小可能不同。 |
| 默认设备 | `defaultPrinter()` | 返回系统默认打印机的信息。 | 可能返回空对象，必须先 `isNull()`。 |
| 默认设备名 | `defaultPrinterName()` | 返回系统默认打印机名称。 | 空字符串可能表示系统没有默认打印机。 |
| 描述 | `description() const` | 返回面向用户的打印机描述。 | 适合显示 UI；不一定是稳定唯一标识。 |
| 是否默认 | `isDefault() const` | 判断此设备当前是否系统默认打印机。 | 默认设置可能在运行中变化。 |
| 是否为空 | `isNull() const` | 判断对象是否包含有效打印机定义。 | `defaultPrinter()`、`printerInfo()` 的结果都应先检查。 |
| 是否远程 | `isRemote() const` | 判断是否为远程网络打印机。 | 远程设备查询和实际打印可能更慢或更不稳定。 |
| 位置 | `location() const` | 返回面向用户的打印机位置描述。 | 不保证每个驱动都提供此字段。 |
| 厂商型号 | `makeAndModel() const` | 返回打印机的厂商与型号描述。 | 是人类可读信息，不适合作为设备唯一 ID。 |
| 最大物理纸张 | `maximumPhysicalPageSize() const` | 返回设备支持的最大物理页面尺寸。 | 用于限制自定义页面大小。 |
| 最小物理纸张 | `minimumPhysicalPageSize() const` | 返回设备支持的最小物理页面尺寸。 | 与最大尺寸一起校验自定义页面大小。 |
| 按名查设备 | `printerInfo(const QString &printerName)` | 返回指定系统名称的打印机信息。 | 找不到时返回空对象；调用后检查 `isNull()`。 |
| 系统名称 | `printerName() const` | 返回打印机唯一系统标识名称。 | 可能不适合用户显示；用于 `QPrinter::setPrinterName()` 或再次查询。 |
| 设备状态 | `state() const` | 返回设备当前状态。 | 受平台、驱动和网络限制，不能保证实时精确。 |
| 支持颜色 | `supportedColorModes() const` | 返回设备支持的颜色模式列表。 | 用户选择和驱动实际可用性仍可能进一步限制。 |
| 支持双面 | `supportedDuplexModes() const` | 返回设备支持的双面模式列表。 | 不支持时应用应禁用相关 UI 或降级。 |
| 支持页面尺寸 | `supportedPageSizes() const` | 返回设备支持的页面尺寸列表。 | 自定义页面还要结合 `supportsCustomPageSizes()`。 |
| 支持分辨率 | `supportedResolutions() const` | 返回设备支持的 dpi 列表。 | 实际打印分辨率可能由驱动协商，不要硬编码一个值。 |
| 自定义纸张 | `supportsCustomPageSizes() const` | 判断设备是否支持自定义页面大小。 | 原生页面设置对话框仍可能无法完整显示自定义大小。 |
| 赋值 | `operator=(const QPrinterInfo &other)` | 以另一份打印机信息替换当前对象。 | 替换后旧引用或派生的 UI 数据需要自行更新。 |

## 易错点

1. `availablePrinters()` 可能因为远程设备而很慢，优先用 `availablePrinterNames()`。
2. `QPrinterInfo` 是查询对象，不执行打印，也不能配置打印任务。
3. `printerName()` 适合设备标识，`description()` 更适合用户界面。
4. 默认打印机或按名查找的结果可能为空，必须检查 `isNull()`。

### 一句话总结

`QPrinterInfo` 用于发现、选择和查询系统打印机能力；它是 `QPrinter` 创建打印作业前的设备信息层。
