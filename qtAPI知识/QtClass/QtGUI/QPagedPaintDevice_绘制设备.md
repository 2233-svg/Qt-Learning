# QPagedPaintDevice：多页打印与 PDF 输出的基础契约

> 头文件：`#include <QPagedPaintDevice>`  
> 模块：`Qt6::Gui`  
> 继承：`QPaintDevice`  
> 常用派生类：`QPdfWriter`、`QPrinter`

## 它解决什么问题

`QPagedPaintDevice` 表示可以容纳多页绘制结果的 `QPaintDevice`。它定义了 PDF 文件和打印设备共同需要的页面控制契约：页面布局、纸张尺寸、方向、边距、页面范围和开始下一页。

应用通常不直接派生或实例化它，而是使用：

- `QPdfWriter`：生成 PDF 文件；
- `QPrinter`：输出到系统打印机或打印对话框选定的目标。

`QPainter` 负责在当前页绘制；`QPagedPaintDevice` 负责“当前页是什么尺寸、可绘制区域在哪、何时提交并开始下一页”。两者应配合使用。

## 实际使用流程

```cpp
#include <QPdfWriter>
#include <QPainter>

QPdfWriter writer("report.pdf");
writer.setPageLayout(QPageLayout(QPageSize(QPageSize::A4),
                                 QPageLayout::Portrait,
                                 QMarginsF(15, 15, 15, 15)));

QPainter painter(&writer);
painter.drawText(writer.pageLayout().paintRectPixels(writer.resolution()),
                 Qt::AlignCenter, "Page 1");

if (!writer.newPage())
    return; // 输出设备无法开始下一页，停止继续绘制。

painter.drawText(writer.pageLayout().paintRectPixels(writer.resolution()),
                 Qt::AlignCenter, "Page 2");
painter.end();
```

`newPage()` 是页与页之间的提交边界。只有当它成功返回 `true`，后续绘制才属于新页面。失败时继续画没有可靠语义，应停止任务并报告输出错误。

## 页面布局改变的时机

页面尺寸、方向、边距和完整 `QPageLayout` 都会影响 `QPainter` 的 device metrics、坐标换算和可绘制区域。Qt 要求这些设置：

1. 在 `QPainter::begin()` 之前调用；或
2. 在下一次 `newPage()` **紧前**调用，以便新设置应用到新页。

设置与 `newPage()` 之间不能再调用任何绘图 API，否则可能使用错误的 paint metrics。

```cpp
// painter 已在上一页完成绘制。
writer.setPageOrientation(QPageLayout::Landscape);
if (!writer.newPage())
    return;

// 现在才开始绘制横向新页。
```

不能通过修改 `pageLayout()` 的返回值改变设备配置。它返回的是布局副本；应调用 `setPageLayout()`、`setPageSize()`、`setPageOrientation()` 或 `setPageMargins()`，并检查返回值。

## 页面范围的含义

`setPageRanges()` / `pageRanges()` 自 Qt 6.0 起提供，用于在设备上关联目标页范围，例如打印 UI 中用户选择的范围。它本身不是“自动跳过你的绘制循环”的通用保证：生成器仍需根据当前后端和业务逻辑决定哪些逻辑页要绘制、哪些页需调用 `newPage()`。

对打印任务，尤其要区分：

- 文档中的逻辑页号；
- 用户选择的实际输出范围；
- 设备产生的物理页序和副本策略。

不要把 `QPageRanges` 当作一组已经执行完筛选的页面。

## PDF 版本枚举

`PdfVersion` 描述 `QPdfWriter` 或 `QPrinter` 所产出 PDF 的目标兼容级别：

- `PdfVersion_1_4`：PDF 1.4；
- `PdfVersion_A1b`：PDF/A-1b 归档兼容输出；
- `PdfVersion_1_6`：PDF 1.6；
- `PdfVersion_X4`：PDF/X-4，Qt 6.8 起。

该枚举只是基础设备声明的类型；实际由具体派生类提供对应的 PDF 版本设置 API。归档、印前或合规交付还涉及字体嵌入、色彩管理、透明度和元数据等要求，不能仅凭选择一个枚举值就假设文档完全合规。

## 常见错误

### 绘制中途改页面边距或方向

当前页的 painter metrics 已建立。应完成当前页，设置新布局，立即 `newPage()`，再画新页。

### 忽略 `newPage()` 的失败结果

失败代表设备未能开始下一页。继续绘制可能丢失页面或损坏任务的预期结构。

### 修改 pageLayout() 返回的副本

读取布局可以用 `pageLayout()`，写回必须调用设备 setter。

### 把页面范围当自动过滤器

页面范围是设备配置/意图；生成循环是否跳页和如何编号仍由应用负责。

## API 速查表

| 类别 | API | 语义 | 边界与注意点 |
| --- | --- | --- | --- |
| 枚举 | `PdfVersion::{PdfVersion_1_4, PdfVersion_A1b, PdfVersion_1_6, PdfVersion_X4}` | 描述 PDF 输出兼容级别。 | 由具体 `QPdfWriter`/`QPrinter` API 选择；`PdfVersion_X4` 自 Qt 6.8 起。 |
| 生命周期 | `~QPagedPaintDevice()` | 销毁多页绘制设备。 | 先结束仍在使用的 `QPainter`，确保输出对象生命周期完整。 |
| 分页 | `bool newPage()` | 提交当前页并开始下一页。 | 仅成功返回 `true` 后继续绘制；通常在活动 `QPainter` 会话中调用。 |
| 布局查询 | `QPageLayout pageLayout() const` | 返回当前页的布局副本，含纸张、方向、边距、full/paint rect。 | 修改副本不会回写设备。 |
| 布局设置 | `bool setPageLayout(const QPageLayout &layout)` | 整体设置纸张、方向和边距。 | 在 `begin()` 前或紧邻 `newPage()` 前调用；之间不可绘制；检查返回值。 |
| 尺寸设置 | `bool setPageSize(const QPageSize &size)` | 设置页面纸张尺寸。 | 同样只在安全页面边界调整；用 `pageLayout().pageSize()` 查询实际配置。 |
| 方向设置 | `bool setPageOrientation(QPageLayout::Orientation orientation)` | 设置页面方向并影响 page rect。 | 仅对后续新页安全生效；检查返回值。 |
| 边距设置 | `bool setPageMargins(const QMarginsF &margins, QPageLayout::Unit unit = Millimeter)` | 以指定单位设置页面边距。 | 不要在当前页绘制间改动；检查设备是否接受该边距。 |
| 范围查询，Qt 6.0 起 | `QPageRanges pageRanges() const` | 返回设备关联的页范围。 | 是范围配置，不保证自动跳过绘制。 |
| 范围设置，Qt 6.0 起 | `void setPageRanges(const QPageRanges &ranges)` | 设置设备关联的页范围。 | 生成逻辑仍要明确怎样应用范围、页号和 `newPage()`。 |

## 一句话总结

`QPagedPaintDevice` 管理多页输出的页面边界而非绘图内容；在 painter 开始前配置布局，或在无绘制间隙的 `newPage()` 边界切换布局，并始终检查新页是否成功创建。
