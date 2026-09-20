# QAbstractPrintDialog 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAbstractPrintDialog>`  
> 所属模块：`Qt6::PrintSupport`  
> 继承：`QDialog`

## 它解决什么问题

`QAbstractPrintDialog` 是 Qt 打印对话框的公共配置基类。它把“页码范围、对话框选项、关联的 `QPrinter`”这类通用逻辑放在一个抽象层中，`QPrintDialog` 则在此基础上提供用户真正会看到的打印对话框。

应用代码通常不直接创建它，而是使用 `QPrintDialog`。理解它仍很有价值，因为 `QPrintDialog` 的页码范围和选项控制都来自这里。

```cpp
QPrinter printer;
QPrintDialog dialog(&printer, this);

dialog.setMinMax(1, totalPages);
dialog.setFromTo(1, totalPages);
dialog.setPrintRange(QAbstractPrintDialog::PageRange);
```

当用户接受 `QPrintDialog` 后，选择会写回同一个 `QPrinter`。应用应根据 `printer.printRange()`、`fromPage()`、`toPage()` 或 `pageRanges()` 决定绘制哪些页面；对话框只收集意图，不会自动替你遍历文档页。

## 页码范围的两个层次

`setMinMax(min, max)` 是“允许用户输入的页码边界”，并会启用 `PrintPageRange` 选项。`setFromTo(from, to)` 是“当前页码范围的默认值”。两者不要混淆：

- 文档共 20 页：通常设 `setMinMax(1, 20)`；
- 希望默认打印第 3 到第 8 页：再设 `setFromTo(3, 8)`；
- 用户最终是否选“全部页”“当前页”还是“页码范围”，由 `printRange()` 查询。

`fromPage()` 与 `toPage()` 默认可能为 `0`，表示没有显式页码范围；不要把 `0` 当作文档第一页。

## 平台差异和额外标签页

`PrintDialogOption` 控制打印对话框中哪些区域可见，但本机原生对话框可能忽略部分设置。`setOptionTabs()` 还可加入自定义标签页，不过 Qt 文档指出它目前仅 X11 支持，并且所有权会转移给打印对话框。

因此不能依赖所有平台都能显示同一套自定义控件。若业务必须展示附加打印选项，最好在打印前后使用自己的配置界面，并将结果明确写入打印逻辑。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `enum PrintDialogOption` | 控制打印对话框中哪些功能区域可见。 | 组合为 `PrintDialogOptions` 使用；原生对话框可能不支持所有选项。 |
| 类型 | `PrintDialogOptions` | `QFlags<PrintDialogOption>` 组合类型。 | 可同时启用多个对话框选项。 |
| 枚举值 | `None` | 不指定额外选项。 | 通常作为空 flags 的语义。 |
| 枚举值 | `PrintToFile` | 显示打印到文件选项。 | 是否真正可用取决于平台和打印后端。 |
| 枚举值 | `PrintSelection` | 显示“打印选中内容”选项。 | 应用仍需根据选择范围实现实际绘制。 |
| 枚举值 | `PrintPageRange` | 显示页码范围控件。 | `setMinMax()` 会自动启用它。 |
| 枚举值 | `PrintCollateCopies` | 显示逐份打印选项。 | 设备不支持多份时应用可能需要自行处理。 |
| 枚举值 | `PrintShowPageSize` | 显示页面大小控件。 | 原生实现可能忽略显示细节。 |
| 枚举值 | `PrintCurrentPage` | 显示“当前页”选项。 | 应用必须定义“当前页”在自身文档中的含义。 |
| 类型 | `enum PrintRange` | 表示用户选择的打印范围。 | 与 `QPrinter::PrintRange` 对应，但对话框负责选择 UI。 |
| 枚举值 | `AllPages` | 用户选择打印全部页面。 | 不应用 `fromPage()` 和 `toPage()` 限制文档。 |
| 枚举值 | `Selection` | 用户选择打印选中内容。 | 需要应用自己知道什么是选区及如何分页。 |
| 枚举值 | `PageRange` | 用户选择指定页码区间。 | 使用 `fromPage()`、`toPage()` 或 `QPrinter` 范围信息。 |
| 枚举值 | `CurrentPage` | 用户选择打印当前页。 | 对话框不掌握文档当前页，应用负责映射。 |
| 构造 | `QAbstractPrintDialog(QPrinter *printer, QWidget *parent = nullptr)` | 构造关联指定 `QPrinter` 的抽象打印对话框。 | 实际使用 `QPrintDialog`；`printer` 必须在对话框期间存活。 |
| 起始页 | `fromPage() const` | 返回当前打印范围的起始页。 | 默认 `0` 表示未设置，不是第一页。 |
| 最大页 | `maxPage() const` | 返回用户可输入的最大页码。 | 设为实际文档页数，避免无效范围。 |
| 最小页 | `minPage() const` | 返回用户可输入的最小页码。 | 默认是 `1`；文档页码通常从 1 开始。 |
| 范围选择 | `printRange() const` | 返回当前选择的打印范围类型。 | 执行打印前检查它，不能只看 from 和 to。 |
| 关联打印机 | `printer() const` | 返回该对话框操作的 `QPrinter`。 | 不转移所有权，用户接受后配置会写入这个对象。 |
| 设置当前范围 | `setFromTo(int from, int to)` | 设置页码范围的默认起始页和结束页。 | 需落在 min/max 范围内；不等于用户最终选择。 |
| 设置允许范围 | `setMinMax(int min, int max)` | 设置可选页码边界，并启用页码范围选项。 | 使用实际页数；不要把它当作当前打印范围。 |
| 额外标签页 | `setOptionTabs(const QList<QWidget *> &tabs)` | 设置显示在打印对话框中的自定义标签页。 | 目前仅 X11 支持，且对话框接管这些 widget 的所有权。 |
| 设置范围类型 | `setPrintRange(PrintRange range)` | 设置默认打印范围选择。 | 用户仍可在对话框中改选，打印前重新查询。 |
| 结束页 | `toPage() const` | 返回当前打印范围的结束页。 | 默认 `0` 表示未设置，不是页码零。 |

## 易错点

1. 不直接使用 `QAbstractPrintDialog`；向用户展示对话框应使用 `QPrintDialog`。
2. `setMinMax()` 是允许范围，`setFromTo()` 才是默认选择范围。
3. 用户选择“页码范围”后，应用仍要自己筛选和绘制相应页面。
4. `setOptionTabs()` 有平台限制，并会接管传入 widget 的所有权。

### 一句话总结

`QAbstractPrintDialog` 提供打印对话框的范围和选项模型；它负责收集用户意图，实际页面筛选与绘制仍由应用和 `QPrinter` 完成。
