# QPrinterInfo
> Qt 6.11.1 · Qt Print Support · 来自 `QPrinterInfo`

## 1. 先建立直觉

`QPrinterInfo` 是系统打印机的“信息快照”。它告诉你有哪些打印机、默认打印机是谁、某台设备支持哪些纸张/分辨率/颜色/双面模式，以及设备当前状态。

它不负责真正打印。要打印，把选中的 `QPrinterInfo` 交给 `QPrinter` 构造；要让用户自己选，用 `QPrintDialog`。

## 2. 类说明

保留类说明：这些 API 来自 `QPrinterInfo`，属于 Qt Print Support 模块，用于查询本机或远程打印机信息。

这是值类型，适合短期保存和展示。但打印机列表可能随系统变化、网络状态变化而过期，尤其是企业网络打印机环境。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `availablePrinterNames()` | 快速取得可用打印机名称列表，通常比完整对象列表轻。 |
| `availablePrinters()` | 取得每台打印机的完整 `QPrinterInfo`。 |
| `defaultPrinterName()` | 取得默认打印机名称。 |
| `defaultPrinter()` | 取得默认打印机信息；没有默认设备时可能为空。 |
| `printerInfo(name)` | 按名称取得打印机信息。 |
| `QPrinterInfo(QPrinter)` | 从已有 `QPrinter` 反查其设备信息。 |
| `isNull()` | 判断是否真的代表一台打印机。 |
| `isDefault()` / `isRemote()` | 判断是否默认设备、是否远程设备。 |
| `printerName()`、`description()`、`location()`、`makeAndModel()` | 展示用的名称、描述、位置、厂商型号。 |
| `state()` | 查询空闲、活动、错误等打印机状态。 |
| `defaultPageSize()` | 查询默认纸张。 |
| `minimumPhysicalPageSize()` / `maximumPhysicalPageSize()` | 查询物理纸张尺寸边界。 |
| `supportedPageSizes()` | 支持的标准纸张列表。 |
| `supportsCustomPageSizes()` | 是否支持自定义纸张。 |
| `defaultColorMode()` / `supportedColorModes()` | 默认和支持的颜色模式。 |
| `defaultDuplexMode()` / `supportedDuplexModes()` | 默认和支持的双面模式。 |
| `supportedResolutions()` | 支持的 DPI 列表。 |

## 4. 典型流程

```cpp
const QStringList names = QPrinterInfo::availablePrinterNames();
for (const QString &name : names) {
    QPrinterInfo info = QPrinterInfo::printerInfo(name);
    if (!info.isNull())
        addPrinterRow(info.printerName(), info.location(), info.state());
}
```

用指定打印机创建 `QPrinter`：

```cpp
QPrinterInfo info = QPrinterInfo::printerInfo(selectedName);
if (!info.isNull()) {
    QPrinter printer(info, QPrinter::HighResolution);
    printDocument(&printer);
}
```

## 5. 使用场景

| 场景 | 建议 |
| --- | --- |
| 自定义打印机选择界面 | 先用 `availablePrinterNames()`，需要详情时再取 `printerInfo()`。 |
| 自动选择某类打印机 | 根据名称、位置、型号或支持纸张筛选。 |
| 打印前能力校验 | 检查双面、彩色、自定义纸张、分辨率。 |
| 设备状态面板 | 展示 `state()`，但不要把它当实时监控保证。 |

## 6. 常见坑与经验

打印机信息可能很慢，尤其远程打印机。不要在 GUI 线程频繁调用完整 `availablePrinters()` 并逐项查所有能力；列表界面可先显示名称，再懒加载详情。

`defaultPrinter()` 和 `printerInfo(name)` 都可能返回空对象。系统没配置打印机、服务不可用、名称过期时都要检查 `isNull()`。

支持列表不等于作业一定成功。驱动、权限、纸张实际装载状态、网络队列都可能让最终打印失败；`QPrinterInfo` 只是能力和状态查询入口。

## 7. 知识点覆盖

- 打印机枚举、默认设备、按名称查询。
- 打印机能力：纸张、DPI、颜色、双面、自定义纸张。
- `QPrinterInfo` 与 `QPrinter` 的衔接。
- 远程打印机性能、信息过期和空对象处理。
